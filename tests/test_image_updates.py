"""Automatic app image updates: the worker's check and check period, and the UI's decisions.

The design is in app/image_updates.py. These pin the rules that keep it safe:
an unchanged build is never recreated, a build that fails its check period is
undone and never tried again on that box, Off checks nothing and Notify only
changes nothing, and only a copy the blank redeploy rebuilds as it runs is
updated by itself.
"""

from __future__ import annotations

import asyncio
import json
import sys
from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from app import database, image_updates, orchestrator
from tests import test_mysterium_fenced as fenced
from tests.test_mysterium_fenced import _FakeDocker, _raw_deploy, _running_old

# The fixture the fenced tests use, shared rather than copied.
markers = fenced.markers
HONEYGAIN = {"cashpilot.service": "honeygain", "cashpilot.managed": "true"}


# ---------------------------------------------------------------------------
# The worker: a check period after the new container starts
# ---------------------------------------------------------------------------


def _deploy(docker, old, **kwargs):
    return _raw_deploy(client=docker.client, old=old, slug="honeygain", **kwargs)


def _docker(new_status="running", **new_attrs):
    old = _running_old("cashpilot-honeygain", HONEYGAIN)
    old.attrs = {"Mounts": [], "Image": "sha256:old"}
    docker = _FakeDocker(old)
    docker.created.status = new_status
    docker.created.attrs = {"Image": "sha256:new", "State": {"Status": new_status}, "RestartCount": 0, **new_attrs}
    docker.created.logs.return_value = b""
    return old, docker


@pytest.fixture
def fast(monkeypatch):
    monkeypatch.setattr(orchestrator, "_SETTLE_POLL_SECONDS", 0)


@pytest.fixture(autouse=True)
def no_unsaved_rows(monkeypatch):
    """Each test starts with no row waiting to be written (image_updates._unsaved_rows),
    and no judged definition or unanswered outcome left in the dashboard by another."""
    monkeypatch.setattr(image_updates, "_unsaved_rows", {})
    main = sys.modules.get("app.main")
    if main is not None:
        monkeypatch.setattr(main, "_image_update_checked", {})
        monkeypatch.setattr(main, "_image_update_unanswered", {})


@pytest.fixture(autouse=True)
def create_answers_an_id(monkeypatch):
    """Docker's create answer, as orchestrator._create_container_id reads it: the ID only."""
    monkeypatch.setattr(orchestrator, "_create_container_id", lambda client, kw: client.containers.create(**kw).id)


class TestCheckPeriod:
    def test_a_new_build_that_stops_is_undone_and_the_old_container_runs_again(self, markers, fast):
        old, docker = _docker("exited", State={"Status": "exited", "ExitCode": 1})
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=0.01)
        assert "undone" in str(failed.value) and "put back and is running again" in str(failed.value)
        assert docker.get("cashpilot-honeygain") is old and not old.removed
        old.start.assert_called_once()
        assert docker.created.removed
        docker.client.images.remove.assert_not_called()

    def test_a_restart_by_docker_fails_the_check(self, markers, fast):
        old, docker = _docker(RestartCount=2)
        with pytest.raises(orchestrator.ImageUpdateFailed, match=r"restarted by Docker \(2x\)"):
            _deploy(docker, old, settle_seconds=0.01)
        assert docker.get("cashpilot-honeygain") is old

    def test_an_unhealthy_image_health_check_fails_the_check(self, markers, fast):
        old, docker = _docker(State={"Status": "running", "Health": {"Status": "unhealthy"}})
        with pytest.raises(orchestrator.ImageUpdateFailed, match="unhealthy"):
            _deploy(docker, old, settle_seconds=0.01)

    def test_a_health_check_still_starting_at_the_end_does_not_pass(self, markers, fast, monkeypatch):
        monkeypatch.setattr(orchestrator, "_SETTLE_GRACE_SECONDS", 0.05)
        old, docker = _docker(State={"Status": "running", "Health": {"Status": "starting"}})
        with pytest.raises(orchestrator.ImageUpdateFailed, match="had not passed its own health check"):
            _deploy(docker, old, settle_seconds=0.01)
        assert docker.get("cashpilot-honeygain") is old and not old.removed

    def test_a_health_check_that_turns_healthy_in_the_grace_passes(self, markers, fast, monkeypatch):
        monkeypatch.setattr(orchestrator, "_SETTLE_GRACE_SECONDS", 5)
        old, docker = _docker(State={"Status": "running", "Health": {"Status": "starting"}})
        looks = []

        def reload():
            looks.append(1)
            if len(looks) > 3:
                docker.created.attrs["State"]["Health"]["Status"] = "healthy"

        docker.created.reload.side_effect = reload
        _deploy(docker, old, settle_seconds=0.01)
        assert old.removed

    def test_a_stop_while_the_final_log_is_read_fails_the_check(self, markers, fast, monkeypatch):
        signal = {"pattern": "cannot be reached", "means": "It cannot start."}
        monkeypatch.setattr(orchestrator, "get_service", lambda slug: {"docker": {"health_signals": [signal]}})
        old, docker = _docker()

        def logs(**kwargs):
            # The container exits while Docker streams its log, with no failure line.
            docker.created.status = "exited"
            docker.created.attrs["State"] = {"Status": "exited", "ExitCode": 3}
            return b"starting\n"

        docker.created.logs.side_effect = logs
        with pytest.raises(orchestrator.ImageUpdateFailed, match="exit code 3"):
            _deploy(docker, old, settle_seconds=0.01)
        assert docker.get("cashpilot-honeygain") is old

    def test_a_fence_that_goes_during_an_update_puts_the_old_node_back(self, markers, fast):
        # A manual deploy leaves the new node to the fence guard. An update must
        # not: the guard would start a build nobody checked.
        old = fenced._running_old()
        docker = _FakeDocker(old)
        with (
            patch.object(orchestrator, "_require_fence", side_effect=orchestrator.ContainerNetworkError("gone")),
            pytest.raises(orchestrator.ContainerRuntimeError) as failed,
        ):
            fenced._raw_deploy(client=docker.client, old=old, settle_seconds=0.01)
        assert not isinstance(failed.value, orchestrator.ImageUpdateFailed)
        assert docker.get("cashpilot-mysterium") is old and not old.removed
        assert docker.created.removed
        # The control: a manual deploy keeps the old behaviour.
        old = fenced._running_old()
        docker = _FakeDocker(old)
        with (
            patch.object(orchestrator, "_require_fence", side_effect=orchestrator.ContainerNetworkError("gone")),
            pytest.raises(orchestrator.ContainerNetworkError),
        ):
            fenced._raw_deploy(client=docker.client, old=old)
        assert old.removed and not docker.created.removed

    def test_a_catalog_failure_signal_in_the_new_log_fails_the_check(self, markers, fast, monkeypatch):
        old, docker = _docker()
        docker.created.logs.return_value = b"update server cannot be reached\n"
        signal = {"pattern": "cannot be reached", "unless": "connected to server", "means": "It cannot start."}
        monkeypatch.setattr(orchestrator, "get_service", lambda slug: {"docker": {"health_signals": [signal]}})
        with pytest.raises(orchestrator.ImageUpdateFailed, match="It cannot start"):
            _deploy(docker, old, settle_seconds=0.01)
        assert docker.get("cashpilot-honeygain") is old

    def test_an_unless_line_or_an_idle_signal_is_not_a_failure(self, markers, fast, monkeypatch):
        old, docker = _docker()
        docker.created.logs.return_value = b"cannot be reached\nconnected to server\nno traffic yet\n"
        signals = [
            {"pattern": "cannot be reached", "unless": "connected to server"},
            {"pattern": "no traffic", "state": "idle"},
        ]
        monkeypatch.setattr(orchestrator, "get_service", lambda slug: {"docker": {"health_signals": signals}})
        _deploy(docker, old, settle_seconds=0.01)
        assert old.removed

    def test_an_unless_line_written_later_in_the_period_still_cancels_the_signal(self, markers, monkeypatch):
        # The failure line is in the log from the start, its unless line only
        # from halfway through the 60 s period, on a simulated clock. The log is
        # judged once the period is over, so the later line counts.
        clock = [0.0]
        monkeypatch.setattr(orchestrator.time, "monotonic", lambda: clock[0])
        monkeypatch.setattr(orchestrator.time, "sleep", lambda s: clock.__setitem__(0, clock[0] + max(s, 0)))
        monkeypatch.setattr(orchestrator, "_SETTLE_POLL_SECONDS", 5.0)
        signal = {"pattern": "cannot be reached", "unless": "connected to server", "means": "It cannot start."}
        monkeypatch.setattr(orchestrator, "get_service", lambda slug: {"docker": {"health_signals": [signal]}})
        began: list[float] = []
        real_settle = orchestrator._settle

        def settle(*args, **kwargs):
            began.append(clock[0])
            return real_settle(*args, **kwargs)

        monkeypatch.setattr(orchestrator, "_settle", settle)

        def run(written_at: float) -> tuple:
            began.clear()

            def logs(**kwargs):
                later = bool(began) and clock[0] - began[0] >= written_at
                return b"update server cannot be reached\n" + (b"connected to server\n" if later else b"")

            old, docker = _docker()
            docker.created.logs.side_effect = logs
            docker.created.reload.side_effect = lambda: clock.__setitem__(0, clock[0] + 0.1)
            _deploy(docker, old, settle_seconds=60)
            return old, docker

        old, _ = run(30)
        assert began and old.removed
        # Control: the same line written only after the period does not count.
        with pytest.raises(orchestrator.ImageUpdateFailed, match="It cannot start"):
            run(200)

    def test_a_failure_line_with_no_unless_line_by_the_end_fails_the_check(self, markers, fast, monkeypatch):
        signal = {"pattern": "cannot be reached", "unless": "connected to server", "means": "It cannot start."}
        monkeypatch.setattr(orchestrator, "get_service", lambda slug: {"docker": {"health_signals": [signal]}})
        old, docker = _docker()
        docker.created.logs.return_value = b"update server cannot be reached\n"
        with pytest.raises(orchestrator.ImageUpdateFailed, match="It cannot start"):
            _deploy(docker, old, settle_seconds=0.02)
        assert docker.get("cashpilot-honeygain") is old

    def test_a_healthy_build_replaces_the_old_and_its_image_goes(self, markers, fast):
        old, docker = _docker()
        report: dict = {}
        _deploy(docker, old, settle_seconds=0.01, image_update=report)
        assert old.removed and docker.get("cashpilot-honeygain") is docker.created
        docker.client.images.remove.assert_called_once_with("sha256:old")
        assert report == {"old_image": "sha256:old", "new_image": "sha256:new", "old_kept": ""}

    def test_the_proxy_refusing_the_delete_keeps_the_image_and_says_why(self, markers, fast):
        old, docker = _docker()
        refused = orchestrator.APIError("403 Forbidden", response=MagicMock(status_code=403))
        docker.client.images.remove.side_effect = refused
        report: dict = {}
        _deploy(docker, old, settle_seconds=0.01, image_update=report)
        assert old.removed
        assert "socket proxy" in report["old_kept"]

    def test_a_plain_deploy_has_no_check_period_and_deletes_no_image(self, markers, fast):
        old, docker = _docker("exited")
        _deploy(docker, old)
        assert old.removed
        docker.client.images.remove.assert_not_called()

    def test_a_tag_that_moved_after_the_check_is_refused_before_anything_changes(self, markers, fast):
        old, docker = _docker()
        docker.client.images.get.return_value.id = "sha256:" + "b" * 64
        with pytest.raises(orchestrator.ContainerRuntimeError, match="moved to another build") as refused:
            _deploy(docker, old, settle_seconds=0.01, expect_image="sha256:" + "a" * 64)
        assert refused.value.status_code == 409
        assert docker.get("cashpilot-honeygain") is old and not old.removed
        old.stop.assert_not_called()
        docker.client.containers.create.assert_not_called()

    def test_the_checked_build_is_installed(self, markers, fast):
        old, docker = _docker(Image="sha256:" + "a" * 64)
        docker.client.images.get.return_value.id = "sha256:" + "a" * 64
        _deploy(docker, old, settle_seconds=0.01, expect_image="sha256:" + "a" * 64)
        assert old.removed

    def test_a_tag_moved_between_the_inspect_and_the_create_is_undone_and_not_held(self, markers, fast):
        # Docker reads the tag again at create time; another pull in between
        # gives the new container another build. It is undone, the previous
        # container runs again, and the error is not ImageUpdateFailed, so the
        # dashboard does not hold a build nobody tried.
        old, docker = _docker(Image="sha256:" + "b" * 64)
        docker.client.images.get.return_value.id = "sha256:" + "a" * 64
        with pytest.raises(orchestrator.ContainerRuntimeError, match="moved to another build") as refused:
            _deploy(docker, old, settle_seconds=0.01, expect_image="sha256:" + "a" * 64)
        assert not isinstance(refused.value, orchestrator.ImageUpdateFailed)
        assert refused.value.status_code == 409
        assert docker.get("cashpilot-honeygain") is old and not old.removed
        assert docker.created.removed
        # Created, checked and never started: the other build never ran on the volumes.
        docker.client.containers.run.assert_not_called()
        docker.created.start.assert_not_called()
        old.start.assert_called_once()

    def test_an_update_whose_create_gets_no_answer_is_undone_and_not_held(self, markers, fast, monkeypatch):
        # No answer to the create: whether Docker made it is unknown, and nothing
        # started it, so there is no start to wait out. The previous container
        # comes back at once.
        waited = MagicMock(side_effect=AssertionError("waited for a start nobody made"))
        monkeypatch.setattr(orchestrator, "_await_start", waited)
        old, docker = _docker(Image="sha256:" + "a" * 64)
        docker.client.images.get.return_value.id = "sha256:" + "a" * 64
        docker.client.containers.create.side_effect = orchestrator.requests.exceptions.ReadTimeout("no answer")
        with pytest.raises(orchestrator.ContainerRuntimeError) as failed:
            _deploy(docker, old, settle_seconds=0.01, expect_image="sha256:" + "a" * 64)
        waited.assert_not_called()
        assert not isinstance(failed.value, orchestrator.ImageUpdateFailed)
        assert docker.get("cashpilot-honeygain") is old
        docker.created.start.assert_not_called()
        old.start.assert_called_once()

    def test_only_a_look_that_starts_after_the_period_passes_it(self, markers, fast, monkeypatch):
        # The first look reads "running" but Docker takes 20 s to answer it, so
        # it ends after the 15 s period; the container stopped meanwhile. That
        # look cannot pass the period: the next one, which sees the stop, decides.
        clock = [0.0]
        monkeypatch.setattr(orchestrator.time, "monotonic", lambda: clock[0])
        old, docker = _docker()
        looks = iter(["running"])

        def reload():
            status = next(looks, "exited")
            if status == "running":
                clock[0] += 20
            docker.created.status = status
            docker.created.attrs["State"] = {"Status": status, "ExitCode": 1}

        docker.created.reload.side_effect = reload
        with pytest.raises(orchestrator.ImageUpdateFailed, match="stopped"):
            _deploy(docker, old, settle_seconds=15)
        assert docker.get("cashpilot-honeygain") is old

    def test_a_log_that_cannot_be_read_is_undone_when_it_has_signals(self, markers, fast, monkeypatch):
        monkeypatch.setattr(orchestrator, "_SETTLE_GRACE_SECONDS", 0.05)
        old, docker = _docker()
        docker.created.logs.side_effect = orchestrator.APIError("500 Server Error")
        signal = {"pattern": "cannot be reached", "means": "It cannot start."}
        monkeypatch.setattr(orchestrator, "get_service", lambda slug: {"docker": {"health_signals": [signal]}})
        with pytest.raises(orchestrator.ImageUpdateFailed, match="did not describe"):
            _deploy(docker, old, settle_seconds=0.01)
        assert docker.get("cashpilot-honeygain") is old

    def test_a_failure_line_far_back_in_a_long_log_still_counts(self, markers, fast, monkeypatch):
        old, docker = _docker()
        docker.created.logs.return_value = b"update server cannot be reached\n" + b"ordinary line\n" * 5000
        signal = {"pattern": "cannot be reached", "means": "It cannot start."}
        monkeypatch.setattr(orchestrator, "get_service", lambda slug: {"docker": {"health_signals": [signal]}})
        with pytest.raises(orchestrator.ImageUpdateFailed, match="It cannot start"):
            _deploy(docker, old, settle_seconds=0.01)
        assert "tail" not in docker.created.logs.call_args.kwargs

    def test_a_copy_stopped_after_the_check_is_not_started_by_the_update(self, markers, fast):
        old, docker = _docker()
        old.status = "exited"
        with pytest.raises(orchestrator.ContainerRuntimeError, match="was stopped after the check"):
            _deploy(docker, old, settle_seconds=0.01)
        assert docker.get("cashpilot-honeygain") is old and not old.removed
        old.start.assert_not_called()
        docker.client.containers.create.assert_not_called()

    def test_a_replacement_docker_cannot_describe_at_the_end_is_undone(self, markers, fast, monkeypatch):
        monkeypatch.setattr(orchestrator, "_SETTLE_GRACE_SECONDS", 0.05)
        old, docker = _docker()
        docker.created.reload.side_effect = orchestrator.APIError("500 Server Error")
        with pytest.raises(orchestrator.ImageUpdateFailed, match="did not describe") as failed:
            _deploy(docker, old, settle_seconds=0.01)
        assert docker.get("cashpilot-honeygain") is old and not old.removed
        old.start.assert_called_once()
        # Nobody knows the build is bad: it is not held (worker_api answers image_update_unverified).
        assert failed.value.verified is False and failed.value.restored is True

    def test_a_health_check_still_starting_is_a_known_failure(self, markers, fast, monkeypatch):
        monkeypatch.setattr(orchestrator, "_SETTLE_GRACE_SECONDS", 0.05)
        old, docker = _docker(State={"Status": "running", "Health": {"Status": "starting"}})
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=0.01)
        assert failed.value.verified is True

    def test_a_health_check_that_passes_after_the_grace_does_not_pass(self, markers, monkeypatch):
        # A 120 s check and a 30 s grace, with Docker taking 0.1 s per look: the
        # looks fall at 147.9 s and, unbounded, at 153 s. The build turns healthy
        # at 152 s, after the grace, so it must not pass.
        clock = [0.0]
        monkeypatch.setattr(orchestrator.time, "monotonic", lambda: clock[0])
        monkeypatch.setattr(orchestrator.time, "sleep", lambda s: clock.__setitem__(0, clock[0] + max(s, 0)))
        monkeypatch.setattr(orchestrator, "_SETTLE_POLL_SECONDS", 5.0)
        old, docker = _docker(State={"Status": "running", "Health": {"Status": "starting"}})
        began: list[float] = []
        real_settle = orchestrator._settle

        def settle(*args, **kwargs):
            began.append(clock[0])
            return real_settle(*args, **kwargs)

        monkeypatch.setattr(orchestrator, "_settle", settle)

        def reload():
            clock[0] += 0.1
            healthy = bool(began) and clock[0] - began[0] >= 152
            docker.created.attrs["State"]["Health"]["Status"] = "healthy" if healthy else "starting"

        docker.created.reload.side_effect = reload
        with pytest.raises(orchestrator.ImageUpdateFailed, match="had not passed its own health check"):
            _deploy(docker, old, settle_seconds=120)
        assert docker.get("cashpilot-honeygain") is old and not old.removed
        assert clock[0] - began[0] < 151

    def test_a_look_that_starts_after_the_grace_never_passes(self, markers, monkeypatch):
        # Each sleep runs 3 s long, so the last look starts at 153 s, after the
        # 150 s grace, and sees a healthy build. That look cannot pass it.
        clock = [0.0]
        monkeypatch.setattr(orchestrator.time, "monotonic", lambda: clock[0])
        monkeypatch.setattr(orchestrator.time, "sleep", lambda s: clock.__setitem__(0, clock[0] + max(s, 0) + 3))
        monkeypatch.setattr(orchestrator, "_SETTLE_POLL_SECONDS", 5.0)
        old, docker = _docker(State={"Status": "running", "Health": {"Status": "starting"}})
        began: list[float] = []
        real_settle = orchestrator._settle

        def settle(*args, **kwargs):
            began.append(clock[0])
            return real_settle(*args, **kwargs)

        monkeypatch.setattr(orchestrator, "_settle", settle)

        def reload():
            clock[0] += 0.1
            healthy = bool(began) and clock[0] - began[0] >= 152
            docker.created.attrs["State"]["Health"]["Status"] = "healthy" if healthy else "starting"

        docker.created.reload.side_effect = reload
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=120)
        # Docker answered too late to tell: undone, and not held.
        assert failed.value.verified is False
        assert docker.get("cashpilot-honeygain") is old and not old.removed

    def test_a_refused_update_that_leaves_the_old_container_down_needs_the_owner(self, markers, fast):
        old, docker = _docker()
        docker.client.containers.create.side_effect = orchestrator.APIError("500 Server Error")
        docker.client.containers.run.side_effect = orchestrator.APIError("500 Server Error")
        old.start.side_effect = orchestrator.APIError("500 Server Error")
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=0.01)
        # Nobody judged the build, so it is not held, but the owner is told.
        assert failed.value.restored is False and failed.value.verified is False
        assert "500 Server Error" in str(failed.value)
        # Control: the same refusal with the old container back is a plain refusal.
        old, docker = _docker()
        docker.client.containers.create.side_effect = orchestrator.APIError("500 Server Error")
        docker.client.containers.run.side_effect = orchestrator.APIError("500 Server Error")
        with pytest.raises(orchestrator.ContainerRuntimeError) as refused:
            _deploy(docker, old, settle_seconds=0.01)
        assert not isinstance(refused.value, orchestrator.ImageUpdateFailed)

    def test_an_update_whose_old_container_cannot_be_moved_aside_or_started_needs_the_owner(self, markers, fast):
        # Docker refuses the rename that sets the old container aside, and then its
        # start: the app is down, and no new build ran.
        old, docker = _docker()
        old.rename.side_effect = orchestrator.APIError("500 Server Error")
        old.start.side_effect = orchestrator.APIError("500 Server Error")
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=0.01)
        assert failed.value.restored is False and failed.value.verified is False
        assert "could not be started again" in str(failed.value)
        docker.client.containers.create.assert_not_called()
        # Control: the same refused rename with the old container running again.
        old, docker = _docker()
        old.rename.side_effect = orchestrator.APIError("500 Server Error")
        with pytest.raises(orchestrator.ContainerRuntimeError) as refused:
            _deploy(docker, old, settle_seconds=0.01)
        assert not isinstance(refused.value, orchestrator.ImageUpdateFailed)
        old.start.assert_called_once()

    def test_an_old_container_left_under_its_set_aside_name_needs_the_owner(self, markers, fast):
        # Docker renamed it aside and then timed out, and the rename back fails:
        # it runs, but under a name the dashboard does not find.
        old, docker = _docker()
        renames = iter([orchestrator.APIError("timed out"), orchestrator.APIError("refused")])

        def rename(new):
            old.name = "cashpilot-honeygain" + orchestrator.REPLACED_SUFFIX
            raise next(renames)

        old.rename.side_effect = rename
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=0.01)
        assert failed.value.restored is False and failed.value.verified is False
        assert "could not be given back its name" in str(failed.value)
        old.start.assert_called_once()

    def test_an_update_that_needs_the_owner_still_removes_the_refused_container_s_secrets(self, markers, fast):
        # CASHPILOT_EARNER_SECRETS=file: the new container's credentials live in
        # their own volume, and the refused container is gone, so they go too.
        plan = MagicMock(env={}, entrypoint=None, command=None, volume="cashpilot-honeygain-secrets")
        plan.labels.return_value = {}
        for old_starts in (False, True):
            old, docker = _docker()
            docker.client.containers.create.side_effect = orchestrator.APIError("500 Server Error")
            docker.client.containers.run.side_effect = orchestrator.APIError("500 Server Error")
            if not old_starts:
                old.start.side_effect = orchestrator.APIError("500 Server Error")
            with (
                patch.object(orchestrator.secret_env, "plan", return_value=plan),
                patch.object(orchestrator.secret_env, "mount", return_value=MagicMock()),
                patch.object(orchestrator.secret_env, "create_volume"),
                patch.object(orchestrator.secret_env, "remove_volume") as remove,
                pytest.raises(orchestrator.ContainerRuntimeError) as failed,
            ):
                _deploy(docker, old, settle_seconds=0.01)
            assert isinstance(failed.value, orchestrator.ImageUpdateFailed) is not old_starts
            remove.assert_called_once_with(docker.client, "cashpilot-honeygain-secrets")

    def test_a_final_look_that_ends_after_the_grace_does_not_pass(self, markers, monkeypatch):
        # The look after the 120 s period starts at 122 s, and Docker answers it 31 s
        # later, after the 150 s grace. It cannot pass: undone, and not held.
        clock = [0.0]
        monkeypatch.setattr(orchestrator.time, "monotonic", lambda: clock[0])
        monkeypatch.setattr(orchestrator.time, "sleep", lambda s: clock.__setitem__(0, clock[0] + max(s, 0)))
        monkeypatch.setattr(orchestrator, "_SETTLE_POLL_SECONDS", 5.0)
        old, docker = _docker()
        began: list[float] = []
        real_settle = orchestrator._settle

        def settle(*args, **kwargs):
            began.append(clock[0])
            return real_settle(*args, **kwargs)

        monkeypatch.setattr(orchestrator, "_settle", settle)

        def reload():
            late = bool(began) and clock[0] - began[0] >= 120
            clock[0] += 31 if late else 0.1

        docker.created.reload.side_effect = reload
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=120)
        assert failed.value.verified is False
        assert docker.get("cashpilot-honeygain") is old and not old.removed

    def test_an_old_container_that_does_not_start_again_needs_the_owner(self, markers, fast):
        old, docker = _docker("exited", State={"Status": "exited", "ExitCode": 1})
        old.start.side_effect = orchestrator.APIError("500 Server Error")
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=0.01)
        assert failed.value.restored is False and "could not be started again" in str(failed.value)
        # Control: the same failure with the old container back is restored.
        old, docker = _docker("exited", State={"Status": "exited", "ExitCode": 1})
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=0.01)
        assert failed.value.restored is True

    def test_one_unreadable_look_then_a_good_one_passes(self, markers, fast, monkeypatch):
        monkeypatch.setattr(orchestrator, "_SETTLE_GRACE_SECONDS", 5)
        old, docker = _docker()
        looks = iter([orchestrator.APIError("500 Server Error")])

        def reload():
            if (error := next(looks, None)) is not None:
                raise error

        docker.created.reload.side_effect = reload
        _deploy(docker, old, settle_seconds=0.01)
        assert old.removed

    def test_stop_waits_for_a_deploy_that_holds_the_route_lock(self):
        # A deploy holds the route lock (deploy_raw, through its check period);
        # a Stop sent meanwhile stops the container only once it is released.
        import threading

        # The deploy replaces the container: a lookup before it publishes the
        # new one finds the old one, so a Stop that looked early stops the wrong one.
        old = MagicMock(name="cashpilot-honeygain old")
        container = MagicMock(name="cashpilot-honeygain new")
        current = {"container": old}
        holding, release, done = threading.Event(), threading.Event(), threading.Event()
        lock = orchestrator.route_gate.deploying("honeygain")
        free_during_stop: list[bool] = []

        def stop_call(**kwargs):
            # Another thread cannot take the route lock while the container stops.
            def probe():
                got = lock.acquire(blocking=False)
                if got:
                    lock.release()
                free_during_stop.append(got)

            prober = threading.Thread(target=probe)
            prober.start()
            prober.join()

        container.stop.side_effect = stop_call

        def deploy():
            with orchestrator.route_gate.deploying("honeygain"):
                holding.set()
                release.wait(5)
                current["container"] = container

        def stop():
            with (
                patch.object(orchestrator, "_find_container", side_effect=lambda *a: current["container"]),
                patch.object(orchestrator, "fence_gated", return_value=False),
            ):
                orchestrator.stop_service("honeygain")
            done.set()

        deployer = threading.Thread(target=deploy)
        deployer.start()
        assert holding.wait(5)
        stopper = threading.Thread(target=stop)
        stopper.start()
        assert not done.wait(0.3), "Stop ran while a deploy held the route lock"
        container.stop.assert_not_called()
        old.stop.assert_not_called()
        release.set()
        assert done.wait(5)
        container.stop.assert_called_once()
        old.stop.assert_not_called()
        assert free_during_stop == [False], "the container stopped outside the route lock"
        deployer.join()
        stopper.join()

    def test_a_stop_that_waits_past_its_limit_is_refused_and_stops_nothing(self, monkeypatch):
        # A deploy still pulling a big image holds the route lock past what the
        # dashboard waits for a Stop: the Stop is refused, never carried out later.
        import threading

        from app import main

        monkeypatch.setattr(orchestrator, "_stop_wait_seconds", lambda slug: 0.2)
        container = MagicMock(name="cashpilot-honeygain")
        holding, release = threading.Event(), threading.Event()

        def deploy():
            with orchestrator.route_gate.deploying("honeygain"):
                holding.set()
                release.wait(5)

        deployer = threading.Thread(target=deploy)
        deployer.start()
        assert holding.wait(5)
        try:
            with (
                patch.object(orchestrator, "_find_container", return_value=container),
                patch.object(orchestrator, "fence_gated", return_value=False),
                pytest.raises(orchestrator.ContainerRuntimeError) as refused,
            ):
                orchestrator.stop_service("honeygain")
        finally:
            release.set()
            deployer.join()
        assert refused.value.status_code == 409
        container.stop.assert_not_called()
        # The lock is free again for the next deploy or Stop.
        assert orchestrator.route_gate.deploying("honeygain").acquire(blocking=False)
        orchestrator.route_gate.deploying("honeygain").release()
        # The dashboard waits longer than the worker's limit plus the stop itself.
        monkeypatch.undo()
        stop = orchestrator._get_stop_timeout("honeygain")
        budget = 30 + main._catalog_stop_timeout("honeygain") + main._deploy_timeout("honeygain")
        budget += image_updates.SETTLE_SECONDS + 30
        assert orchestrator._stop_wait_seconds("honeygain") + stop < budget
        assert orchestrator._IMAGE_UPDATE_SETTLE_SECONDS == image_updates.SETTLE_SECONDS

    def test_a_restart_waits_for_a_deploy_and_is_refused_past_its_limit(self, monkeypatch):
        # A restart inside an image update's check period would read as a failure
        # and put the old container back. It waits as a Stop does.
        import threading

        from app import main

        monkeypatch.setattr(orchestrator, "_stop_wait_seconds", lambda slug: 0.2)
        restarted: list[bool] = []
        monkeypatch.setattr(orchestrator, "_restart_service", lambda slug, instance: restarted.append(True))
        holding, release = threading.Event(), threading.Event()

        def deploy():
            with orchestrator.route_gate.deploying("honeygain"):
                holding.set()
                release.wait(5)

        deployer = threading.Thread(target=deploy)
        deployer.start()
        assert holding.wait(5)
        try:
            with pytest.raises(orchestrator.ContainerRuntimeError) as refused:
                orchestrator.restart_service("honeygain")
        finally:
            release.set()
            deployer.join()
        assert refused.value.status_code == 409 and "not restarted" in str(refused.value)
        assert not restarted
        # Once the deploy is done, the restart runs, and frees the lock after.
        orchestrator.restart_service("honeygain")
        assert restarted == [True]
        assert orchestrator.route_gate.deploying("honeygain").acquire(blocking=False)
        orchestrator.route_gate.deploying("honeygain").release()
        # The dashboard waits for it as long as for a Stop.
        monkeypatch.undo()
        call = AsyncMock(return_value={})
        with patch.object(main, "_proxy_to_worker", call):
            asyncio.run(main._proxy_worker_command(1, "stop", "honeygain"))
            asyncio.run(main._proxy_worker_command(1, "restart", "honeygain"))
        stop_wait, restart_wait = (c.kwargs["timeout"] for c in call.call_args_list)
        assert restart_wait == stop_wait
        assert restart_wait > orchestrator._stop_wait_seconds("honeygain") + orchestrator._get_stop_timeout("honeygain")

    def test_a_failure_line_the_old_build_logged_too_does_not_fail_the_new_one(self, markers, fast, monkeypatch):
        # storj logs a dial-back failure for days when the box's address is wrong:
        # every build logs it, so the new one is not blamed for it.
        signal = {"pattern": "failed to dial storage node", "state": "failing", "means": "no dial-back"}
        monkeypatch.setattr(orchestrator, "get_service", lambda slug: {"docker": {"health_signals": [signal]}})
        line = b"ping satellite failed to dial storage node\n"
        old, docker = _docker()
        old.logs.return_value = line
        docker.created.logs.return_value = line
        _deploy(docker, old, settle_seconds=0.01)
        assert old.removed and docker.get("cashpilot-honeygain") is docker.created
        assert old.logs.call_args.kwargs["tail"] == orchestrator._SIGNALS_ALREADY_LINES
        # Control: a line the old build never logged fails the new one.
        old, docker = _docker()
        old.logs.return_value = b"all fine\n"
        docker.created.logs.return_value = line
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=0.01)
        assert failed.value.verified is True and docker.get("cashpilot-honeygain") is old

    def test_an_undone_replacement_gets_a_clean_stop_before_it_is_removed(self, markers, fast, monkeypatch):
        signal = {"pattern": "fatal", "state": "failing"}
        monkeypatch.setattr(orchestrator, "get_service", lambda slug: {"docker": {"health_signals": [signal]}})
        old, docker = _docker()
        docker.created.logs.return_value = b"fatal\n"
        with pytest.raises(orchestrator.ImageUpdateFailed):
            _deploy(docker, old, settle_seconds=0.01)
        steps = [(name, kwargs) for name, _, kwargs in docker.created.mock_calls if name in ("stop", "remove")]
        assert steps == [
            ("stop", {"timeout": orchestrator._get_stop_timeout("honeygain")}),
            ("remove", {"force": True}),
        ]
        assert docker.created.removed and docker.get("cashpilot-honeygain") is old

    def test_a_replacement_a_backup_paused_is_undone_unjudged(self, markers, fast, monkeypatch):
        # A backup pauses the container while it reads its volumes: not a stop of the build.
        monkeypatch.setattr(orchestrator, "_SETTLE_GRACE_SECONDS", 0.05)
        old, docker = _docker("paused", State={"Status": "paused", "Paused": True})
        with pytest.raises(orchestrator.ImageUpdateFailed) as failed:
            _deploy(docker, old, settle_seconds=0.01)
        assert failed.value.verified is False and docker.get("cashpilot-honeygain") is old

    def test_a_stop_while_the_lan_fence_is_broken_is_not_held(self, monkeypatch):
        # The fence guard stops every gated node while the fence is broken.
        container = MagicMock(status="exited")
        container.attrs = {"State": {"Status": "exited", "ExitCode": 0}}
        monkeypatch.setattr(orchestrator, "fence_gated", lambda slug: True)
        monkeypatch.setattr(orchestrator, "_get_client", lambda: MagicMock())
        for problem, verified in (("the host firewall dropped the rules", False), (None, True)):
            with (
                patch("app.lan_fence.fence_problem", return_value=problem),
                pytest.raises(orchestrator.ImageUpdateFailed) as failed,
            ):
                orchestrator._settle(container, "mysterium", 0.01, 0, "cashpilot-mysterium")
            assert failed.value.verified is verified, problem

    def test_a_backup_during_a_deploy_is_refused_and_pauses_nothing(self, monkeypatch):
        import threading

        container = MagicMock(status="running")
        monkeypatch.setattr(orchestrator, "_critical_volume_targets", lambda slug: ["/data"])
        monkeypatch.setattr(orchestrator, "_find_container", lambda slug, instance=1: container)
        holding, release = threading.Event(), threading.Event()

        def deploy():
            with orchestrator.route_gate.deploying("storj"):
                holding.set()
                release.wait(5)

        deployer = threading.Thread(target=deploy)
        deployer.start()
        assert holding.wait(5)
        try:
            with pytest.raises(orchestrator.ContainerRuntimeError) as refused:
                orchestrator.read_critical_state("storj")
        finally:
            release.set()
            deployer.join()
        assert refused.value.status_code == 409 and "not read for a backup" in str(refused.value)
        container.pause.assert_not_called()


class TestRepoDigest:
    def test_only_the_checked_repository_s_digest_is_named(self):
        image = MagicMock(attrs={"RepoDigests": ["mirror.example/other@sha256:" + "c" * 64]})
        assert orchestrator._repo_digest(image, "honeygain/honeygain:latest") == ""
        # Another registry's copy of the same path is another repository.
        image.attrs["RepoDigests"].append("mirror.example/honeygain/honeygain@sha256:" + "e" * 64)
        assert orchestrator._repo_digest(image, "honeygain/honeygain:latest") == ""
        image.attrs["RepoDigests"].append("docker.io/honeygain/honeygain@sha256:" + "d" * 64)
        assert orchestrator._repo_digest(image, "honeygain/honeygain:latest") == "sha256:" + "d" * 64
        # Docker's old name for Docker Hub is the same repository.
        image.attrs["RepoDigests"] = ["honeygain/honeygain@sha256:" + "f" * 64]
        assert orchestrator._repo_digest(image, "index.docker.io/honeygain/honeygain:latest") == "sha256:" + "f" * 64

    @pytest.mark.parametrize(
        ("name", "full"),
        [
            ("busybox", "docker.io/library/busybox"),
            ("library/busybox", "docker.io/library/busybox"),
            ("docker.io/busybox", "docker.io/library/busybox"),
            ("index.docker.io/busybox", "docker.io/library/busybox"),
            ("index.docker.io/honeygain/honeygain", "docker.io/honeygain/honeygain"),
            ("honeygain/honeygain", "docker.io/honeygain/honeygain"),
            ("localhost/mine", "localhost/mine"),
            ("127.0.0.1:5000/mine", "127.0.0.1:5000/mine"),
            ("ghcr.io/org/app", "ghcr.io/org/app"),
            ("mirror.example/docker.io/busybox", "mirror.example/docker.io/busybox"),
        ],
    )
    def test_a_repository_is_spelled_in_full(self, name, full):
        assert orchestrator._repo_name(name) == full


def _image(image_id, digest="", ref="honeygain/honeygain"):
    return MagicMock(id=image_id, attrs={"RepoDigests": [f"{ref}@{digest}"] if digest else []})


class TestCheckImage:
    def _client(self, running_id, latest_id, ref="honeygain/honeygain:latest"):
        c = MagicMock(id="c1", status="running", labels=HONEYGAIN)
        c.attrs = {"Image": running_id, "Config": {"Image": ref}}
        client = MagicMock()
        client.containers.list.return_value = [c]
        images = {ref: _image(latest_id, "sha256:" + latest_id[-4:]), running_id: _image(running_id, "sha256:aaaa")}
        client.images.get.side_effect = lambda r: images[r]
        return client

    def test_an_unchanged_build_says_so(self):
        client = self._client("sha256:same", "sha256:same")
        with patch.object(orchestrator, "_get_client", return_value=client):
            answer = orchestrator.check_image("honeygain")
        client.api.pull.assert_called_once_with("honeygain/honeygain", tag="latest", stream=True, decode=True)
        assert answer["floating"] and answer["latest"]["id"] == answer["containers"][0]["image_id"]

    def test_a_moved_tag_names_both_builds(self):
        client = self._client("sha256:old", "sha256:beef")
        with patch.object(orchestrator, "_get_client", return_value=client):
            answer = orchestrator.check_image("honeygain")
        assert answer["latest"] == {"id": "sha256:beef", "digest": "sha256:beef"}
        assert answer["containers"][0]["digest"] == "sha256:aaaa"

    def test_a_previous_container_left_after_an_update_is_not_a_copy(self):
        # Its cleanup failed: stopped, on the old build, with the same labels.
        client = self._client("sha256:new", "sha256:new")
        live = client.containers.list.return_value[0]
        live.name = "cashpilot-honeygain"
        left = MagicMock(id="c0", status="exited", labels=HONEYGAIN)
        left.name = "cashpilot-honeygain" + orchestrator.REPLACED_SUFFIX
        left.attrs = {"Image": "sha256:old", "Config": {"Image": "honeygain/honeygain:latest"}}
        client.containers.list.return_value = [live, left]
        with patch.object(orchestrator, "_get_client", return_value=client):
            answer = orchestrator.check_image("honeygain")
        assert [c["container_id"] for c in answer["containers"]] == ["c1"]
        # A copy renamed by hand, or one that runs under that name, is still a copy.
        for name, status in (("cashpilot-honeygain-manually-replaced", "exited"), (left.name, "running")):
            other = MagicMock(id="c2", status=status, labels=HONEYGAIN)
            other.name = name
            other.attrs = left.attrs
            client.containers.list.return_value = [live, other]
            with patch.object(orchestrator, "_get_client", return_value=client):
                answer = orchestrator.check_image("honeygain")
            assert [c["container_id"] for c in answer["containers"]] == ["c1", "c2"], name

    def test_a_pull_that_fails_in_its_stream_is_a_failed_check(self):
        # Docker sends progress, then the error, in one answer; the old build is still cached.
        client = self._client("sha256:old", "sha256:old")
        client.api.pull.return_value = iter(
            [{"status": "Pulling fs layer"}, {"error": "unexpected EOF", "errorDetail": {"message": "unexpected EOF"}}]
        )
        with (
            patch.object(orchestrator, "_get_client", return_value=client),
            pytest.raises(orchestrator.ContainerRuntimeError) as failed,
        ):
            orchestrator.check_image("honeygain")
        assert failed.value.status_code == 502 and "unexpected EOF" in str(failed.value)
        # Control: the same stream without the error is a check.
        client.api.pull.return_value = iter([{"status": "Pulling fs layer"}, {"status": "Download complete"}])
        with patch.object(orchestrator, "_get_client", return_value=client):
            assert orchestrator.check_image("honeygain")["floating"] is True

    def test_a_check_joins_the_pull_an_earlier_check_left_running(self, monkeypatch):
        # A pull past its check's deadline keeps running in its thread. The next
        # check of the same image waits for it rather than starting another beside it.
        import threading

        monkeypatch.setattr(orchestrator, "_PULLS", {})
        release, started = threading.Event(), threading.Event()
        client = MagicMock()

        def pull(*args, **kwargs):
            started.set()
            release.wait(5)
            return iter([{"status": "Download complete"}])

        client.api.pull.side_effect = pull
        image = "honeygain/honeygain:latest"
        try:
            with pytest.raises(orchestrator.PastDeadline):
                orchestrator._pull_until(client, image, orchestrator.time.monotonic() + 0.1, strict=True)
            assert started.wait(5)
            with pytest.raises(orchestrator.PastDeadline):
                orchestrator._pull_until(client, image, orchestrator.time.monotonic() + 0.1, strict=True)
            assert client.api.pull.call_count == 1
            # One still running an hour after it began is stuck: the next check starts its own.
            monkeypatch.setattr(orchestrator, "_PULL_JOIN_SECONDS", 0)
            with pytest.raises(orchestrator.PastDeadline):
                orchestrator._pull_until(client, image, orchestrator.time.monotonic() + 0.1, strict=True)
            assert client.api.pull.call_count == 2
            monkeypatch.setattr(orchestrator, "_PULL_JOIN_SECONDS", 3600)
            # The pull is let go only once this check has chosen it, so it is
            # still running when chosen, and the check takes its result.
            real_lock = orchestrator._PULLS_LOCK

            class _ReleaseAfterChoice:
                def __enter__(self):
                    return real_lock.__enter__()

                def __exit__(self, *exc):
                    real_lock.__exit__(*exc)
                    release.set()

            monkeypatch.setattr(orchestrator, "_PULLS_LOCK", _ReleaseAfterChoice())
            assert orchestrator._pull_until(client, image, orchestrator.time.monotonic() + 5, strict=True) is None
            assert client.api.pull.call_count == 2
            monkeypatch.setattr(orchestrator, "_PULLS_LOCK", real_lock)
        finally:
            release.set()
        # Once it ended, the next check pulls again.
        assert orchestrator._pull_until(client, image, orchestrator.time.monotonic() + 5, strict=True) is None
        assert client.api.pull.call_count == 3

    def test_a_stopped_copy_of_an_app_whose_name_ends_in_replaced_is_a_copy(self):
        # A custom app named "Foo Replaced" gets the slug custom-foo-replaced, so
        # its own container name ends in -replaced. Only its set-aside name is skipped.
        slug = "custom-foo-replaced"
        client = self._client("sha256:new", "sha256:new")
        copy = client.containers.list.return_value[0]
        copy.name, copy.status = orchestrator._container_name(slug), "exited"
        aside = MagicMock(id="c0", status="exited", labels=HONEYGAIN)
        aside.name = copy.name + orchestrator.REPLACED_SUFFIX
        aside.attrs = {"Image": "sha256:old", "Config": copy.attrs["Config"]}
        with (
            patch.object(orchestrator, "_get_client", return_value=client),
            patch.object(orchestrator, "service_instances", return_value=[copy, aside]),
        ):
            answer = orchestrator.check_image(slug)
        assert [c["container_id"] for c in answer["containers"]] == ["c1"]

    @pytest.mark.parametrize("ref", ["honeygain/honeygain@sha256:" + "a" * 64, "sha256:" + "b" * 64])
    def test_a_pinned_image_is_not_pulled(self, ref):
        client = self._client("sha256:old", "sha256:new", ref=ref)
        with patch.object(orchestrator, "_get_client", return_value=client):
            assert orchestrator.check_image("honeygain")["floating"] is False
        client.api.pull.assert_not_called()
        client.images.pull.assert_not_called()

    def test_floating_refs(self):
        assert orchestrator.floating_ref("busybox")
        assert orchestrator.floating_ref("localhost:5000/x:latest")
        assert not orchestrator.floating_ref("x@sha256:" + "a" * 64)
        assert not orchestrator.floating_ref("")


# ---------------------------------------------------------------------------
# The UI: what a run does with the worker's answer
# ---------------------------------------------------------------------------


def _answer(running="sha256:old", latest="sha256:new", status="running", floating=True):
    return {
        "floating": floating,
        "ref": "honeygain/honeygain:latest",
        "latest": {"id": latest, "digest": "sha256:" + latest[-3:]},
        "containers": [{"instance": 1, "container_id": "c1", "status": status, "image_id": running, "digest": "d"}],
    }


class _Hooks:
    def __init__(self, answer, *, blocker="", deploy=None, seen=()):
        self.rows: list[tuple] = []
        self.deploys: list[tuple] = []
        self.checks = 0
        self._seen = set(seen)
        self._answer, self._blocker, self._deploy = answer, blocker, deploy

    def hooks(self):
        async def check(wid, slug):
            self.checks += 1
            return self._answer

        async def blocker(wid, slug, answer):
            return self._blocker

        async def deploy(wid, slug, expected, new_image):
            self.deploys.append((wid, slug, expected, new_image))
            if isinstance(self._deploy, Exception):
                raise self._deploy
            # The worker installs the checked build.
            return self._deploy or {"image_update": {"new_image": new_image, "old_kept": ""}}

        async def record(wid, slug, result, **facts):
            self.rows.append((result, facts))
            self._seen.add((result, facts.get("new_image")))

        async def seen(wid, slug, new_image, results):
            return any((r, new_image) in self._seen for r in results)

        async def latest(wid, slug):
            if not self.rows:
                return None
            result, facts = self.rows[-1]
            return {"result": result, "new_image": facts.get("new_image", "")}

        return image_updates.Hooks(
            check=check, blocker=blocker, deploy=deploy, record=record, seen=seen, sleep=AsyncMock(), latest=latest
        )


async def _run(state, mode):
    return await image_updates.update_service(state.hooks(), 1, "honeygain", mode)


@pytest.mark.asyncio
class TestDecisions:
    async def test_off_checks_nothing(self):
        state = _Hooks(_answer())
        assert await _run(state, image_updates.OFF) == "off"
        assert state.checks == 0 and not state.deploys and not state.rows

    async def test_an_unchanged_build_is_a_no_op(self):
        state = _Hooks(_answer(running="sha256:new"))
        assert await _run(state, image_updates.AUTO) == "current"
        assert not state.deploys and not state.rows

    async def test_a_pinned_image_is_left_to_releases(self):
        state = _Hooks(_answer(floating=False))
        assert await _run(state, image_updates.AUTO) == "pinned"
        assert not state.deploys

    async def test_notify_only_records_once_and_deploys_nothing(self):
        state = _Hooks(_answer())
        assert await _run(state, image_updates.NOTIFY) == "available"
        assert await _run(state, image_updates.NOTIFY) == "available"
        assert [r for r, _ in state.rows] == ["available"]
        assert not state.deploys

    async def test_auto_runs_the_blank_redeploy_against_the_checked_containers(self):
        state = _Hooks(_answer())
        assert await _run(state, image_updates.AUTO) == "updated"
        # The checked build is the only one the worker may install.
        assert state.deploys == [(1, "honeygain", {"1": "c1"}, "sha256:new")]
        result, facts = state.rows[0]
        assert result == "updated" and facts["old_image"] == "sha256:old" and facts["new_image"] == "sha256:new"

    async def test_a_rolled_back_build_is_held_so_it_never_loops(self):
        state = _Hooks(_answer(), deploy=image_updates.DeployRefused("undone", rolled_back=True))
        assert await _run(state, image_updates.AUTO) == "rolled_back"
        for _ in range(3):
            assert await _run(state, image_updates.AUTO) == "held"
        assert len(state.deploys) == 1
        # A newer build is tried.
        state._answer = _answer(latest="sha256:newer")
        state._deploy = None
        assert await _run(state, image_updates.AUTO) == "updated"
        assert state.deploys[-1][3] == "sha256:newer"
        assert state.rows[-1][0] == "updated" and state.rows[-1][1]["new_image"] == "sha256:newer"

    async def test_an_old_container_that_did_not_start_again_holds_the_build_and_says_so(self):
        refused = image_updates.DeployRefused("not started again", rolled_back=True, restore_failed=True)
        state = _Hooks(_answer(), deploy=refused)
        assert await _run(state, image_updates.AUTO) == image_updates.RESTORE_FAILED
        assert state.rows[0][0] == image_updates.RESTORE_FAILED and state.rows[0][1]["detail"] == "not started again"
        assert await _run(state, image_updates.AUTO) == "held"
        assert len(state.deploys) == 1

    async def test_a_failed_restore_of_a_build_nobody_judged_needs_the_owner_and_holds_nothing(self):
        refused = image_updates.DeployRefused("refused, not started again", rolled_back=False, restore_failed=True)
        state = _Hooks(_answer(), deploy=refused)
        assert await _run(state, image_updates.AUTO) == image_updates.RESTORE_FAILED
        result, facts = state.rows[0]
        assert result == image_updates.RESTORE_FAILED and facts["new_image"] == "" and facts["new_digest"]
        # Once the owner has it running again, the same build is tried.
        state._deploy = None
        assert await _run(state, image_updates.AUTO) == "updated"

    async def test_a_hold_whose_row_fails_to_save_still_holds_and_is_saved_later(self):
        state = _Hooks(_answer(), deploy=image_updates.DeployRefused("undone", rolled_back=True))
        hooks = state.hooks()
        real_record = hooks.record
        writes = {"fail": True}

        async def record(*args, **kwargs):
            if writes["fail"]:
                raise RuntimeError("database is locked")
            await real_record(*args, **kwargs)

        hooks.record = record
        # The undo is reported as such, so the box still pauses after it (run_worker).
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "rolled_back"
        # The write keeps failing: the build is still held, not deployed again.
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "held"
        assert len(state.deploys) == 1 and not state.rows
        # Once the database takes it, the row is written and the hold is in it.
        writes["fail"] = False
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "held"
        assert [r[0] for r in state.rows] == ["rolled_back"] and state.rows[0][1]["detail"] == "undone"
        assert not image_updates._unsaved_rows
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "held"
        assert len(state.deploys) == 1 and len(state.rows) == 1

    @staticmethod
    def _failing_writes(state):
        hooks = state.hooks()
        real_record = hooks.record
        writes = {"fail": True}

        async def record(*args, **kwargs):
            if writes["fail"]:
                raise RuntimeError("database is locked")
            await real_record(*args, **kwargs)

        hooks.record = record
        return hooks, writes

    async def test_a_needs_you_row_of_an_unjudged_build_is_saved_later_and_holds_nothing(self):
        refused = image_updates.DeployRefused("refused, not started again", rolled_back=False, restore_failed=True)
        state = _Hooks(_answer(), deploy=refused)
        hooks, writes = self._failing_writes(state)
        done = await image_updates.run_worker(hooks, {"mode": "auto", "workers": {}, "services": {}}, 1, ["honeygain"])
        # The outcome stays, so the box pauses after it.
        assert done == {"honeygain": image_updates.RESTORE_FAILED}
        hooks.sleep.assert_awaited_once_with(image_updates.GAP_SECONDS)
        # The next check writes the row first, and the build is tried again: nobody judged it.
        writes["fail"], state._deploy = False, None
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "updated"
        assert [(r[0], r[1]["new_image"]) for r in state.rows] == [
            (image_updates.RESTORE_FAILED, ""),
            (image_updates.UPDATED, "sha256:new"),
        ]

    async def test_an_undo_docker_could_not_judge_pauses_the_box_and_is_tried_again(self):
        changed = image_updates.DeployRefused("not described", rolled_back=False, changed=True)
        state = _Hooks(_answer(), deploy=changed)
        settings = {"mode": "auto", "workers": {}, "services": {}}
        hooks = state.hooks()
        assert await image_updates.run_worker(hooks, settings, 1, ["honeygain"]) == {"honeygain": "unverified"}
        hooks.sleep.assert_awaited_once_with(image_updates.GAP_SECONDS)
        assert [r[0] for r in state.rows] == [image_updates.FAILED]
        state._deploy = None
        assert await _run(state, image_updates.AUTO) == "updated"
        # Its row waiting to be saved does not hold the build either.
        state = _Hooks(_answer(), deploy=changed)
        hooks, writes = self._failing_writes(state)
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "unverified"
        # Still unsaved at the next check, and the build is tried again.
        state._deploy = None
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "updated"
        writes["fail"] = False
        state._answer = _answer(running="sha256:new")
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "current"
        assert sorted(r[0] for r in state.rows) == [image_updates.FAILED, image_updates.UPDATED]
        # Control: a refusal that changed nothing does not pause the box.
        state = _Hooks(_answer(), deploy=image_updates.DeployRefused("refused", rolled_back=False))
        hooks = state.hooks()
        assert await image_updates.run_worker(hooks, settings, 1, ["honeygain"]) == {"honeygain": "failed"}
        hooks.sleep.assert_not_awaited()

    async def test_an_update_whose_row_cannot_be_saved_still_pauses_and_is_saved_later(self):
        state = _Hooks(_answer())
        hooks, writes = self._failing_writes(state)
        done = await image_updates.run_worker(hooks, {"mode": "auto", "workers": {}, "services": {}}, 1, ["honeygain"])
        assert done == {"honeygain": "updated"}
        hooks.sleep.assert_awaited_once_with(image_updates.GAP_SECONDS)
        writes["fail"] = False
        state._answer = _answer(running="sha256:new")
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "current"
        assert [(r[0], r[1]["new_image"]) for r in state.rows] == [(image_updates.UPDATED, "sha256:new")]

    async def test_an_unsaved_hold_is_written_whatever_the_tag_names_now(self):
        state = _Hooks(_answer(), deploy=image_updates.DeployRefused("undone", rolled_back=True))
        hooks = state.hooks()
        real_record = hooks.record
        writes = {"fail": True}

        async def record(*args, **kwargs):
            if writes["fail"]:
                raise RuntimeError("database is locked")
            await real_record(*args, **kwargs)

        hooks.record = record
        await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO)
        writes["fail"] = False
        # The tag went back to the running build: the row of the undone one is written anyway.
        state._answer = _answer(latest="sha256:old")
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "current"
        assert [(r[0], r[1]["new_image"]) for r in state.rows] == [("rolled_back", "sha256:new")]
        # And a newer build is not held by it.
        state._answer, state._deploy = _answer(latest="sha256:newer"), None
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "updated"

    async def test_two_unsaved_rows_of_one_build_are_both_written_in_order(self):
        # The same build fails twice while the database is locked: each attempt
        # keeps its own row, and they are written oldest first.
        state = _Hooks(_answer(), deploy=image_updates.DeployRefused("first", rolled_back=False, changed=True))
        hooks, writes = self._failing_writes(state)
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "unverified"
        state._deploy = image_updates.DeployRefused("second", rolled_back=False, changed=True)
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "unverified"
        assert len(image_updates._unsaved_rows) == 2
        writes["fail"] = False
        await image_updates.flush_all(hooks)
        assert [(r[0], r[1]["detail"]) for r in state.rows] == [
            (image_updates.FAILED, "first"),
            (image_updates.FAILED, "second"),
        ]
        assert not image_updates._unsaved_rows

    async def test_a_newer_row_waits_behind_an_older_one_that_is_not_saved_yet(self):
        # The restore failure cannot be saved; the next check updates the app and
        # could save that row. Written first, it would leave the failure as the latest result.
        refused = image_updates.DeployRefused("not started again", rolled_back=False, restore_failed=True)
        state = _Hooks(_answer(), deploy=refused)
        hooks = state.hooks()
        real_record = hooks.record
        failing = {image_updates.RESTORE_FAILED}

        async def record(wid, slug, result, **facts):
            if result in failing:
                raise RuntimeError("database is locked")
            await real_record(wid, slug, result, **facts)

        hooks.record = record
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "restore_failed"
        state._deploy = None
        assert await image_updates.update_service(hooks, 1, "honeygain", image_updates.AUTO) == "updated"
        assert not state.rows and len(image_updates._unsaved_rows) == 2
        failing.clear()
        assert await image_updates.flush_all(hooks) == 2
        assert [r[0] for r in state.rows] == [image_updates.RESTORE_FAILED, image_updates.UPDATED]

    @pytest.mark.parametrize("mode", [image_updates.NOTIFY, image_updates.AUTO])
    async def test_an_app_an_update_left_down_keeps_its_needs_you_row(self, mode):
        # Nobody judged the build, so it is not held; the app is still down the next day.
        state = _Hooks(_answer(status="exited"))
        state.rows.append((image_updates.RESTORE_FAILED, {"new_image": ""}))
        assert await _run(state, mode) == "needs_owner"
        assert [r for r, _ in state.rows] == [image_updates.RESTORE_FAILED] and not state.deploys
        # Waiting to be saved counts the same.
        state = _Hooks(_answer(status="exited"))
        image_updates._unsaved_rows[(1, "honeygain", "", image_updates.RESTORE_FAILED, 0)] = {"new_image": ""}
        hooks = state.hooks()
        hooks.record = AsyncMock(side_effect=RuntimeError("database is locked"))
        assert await image_updates.update_service(hooks, 1, "honeygain", mode) == "needs_owner"
        # Control: once the owner started it, the check goes on.
        state = _Hooks(_answer())
        state.rows.append((image_updates.RESTORE_FAILED, {"new_image": ""}))
        assert await _run(state, mode) in ("available", "updated")

    async def test_an_app_turned_off_during_the_run_is_not_checked(self):
        state = _Hooks(_answer(running="sha256:new"))
        hooks = state.hooks()
        hooks.mode = AsyncMock(
            side_effect=lambda wid, slug: image_updates.OFF if slug == "earnapp" else image_updates.AUTO
        )
        settings = {"mode": "auto", "workers": {}, "services": {}}
        done = await image_updates.run_worker(hooks, settings, 1, ["honeygain", "earnapp"])
        assert done == {"honeygain": "current", "earnapp": "off"} and state.checks == 1

    @pytest.mark.parametrize("mode", [image_updates.NOTIFY, image_updates.AUTO])
    async def test_a_build_the_tag_went_back_to_is_announced_again(self, mode):
        # The bell shows the newest row. Once it names another build, the build the
        # tag went back to is recorded again, or the bell names the wrong one.
        result = image_updates.AVAILABLE if mode == image_updates.NOTIFY else image_updates.SKIPPED
        state = _Hooks(_answer(), blocker="" if mode == image_updates.NOTIFY else "it has a custom image")
        assert await _run(state, mode) in ("available", "skipped")
        state._answer = _answer(latest="sha256:newer")
        await _run(state, mode)
        state._answer = _answer()
        await _run(state, mode)
        assert [(r, f["new_image"]) for r, f in state.rows] == [
            (result, "sha256:new"),
            (result, "sha256:newer"),
            (result, "sha256:new"),
        ]
        # Control: while it is still the newest row, it is not recorded twice.
        await _run(state, mode)
        assert len(state.rows) == 3

    async def test_a_box_pauses_after_an_undo_whose_row_could_not_be_written(self):
        state = _Hooks(_answer(), deploy=image_updates.DeployRefused("undone", rolled_back=True))
        hooks = state.hooks()

        async def record(*args, **kwargs):
            raise RuntimeError("database is locked")

        hooks.record = record
        done = await image_updates.run_worker(hooks, {"mode": "auto", "workers": {}, "services": {}}, 1, ["honeygain"])
        assert done == {"honeygain": "rolled_back"}
        hooks.sleep.assert_awaited_once_with(image_updates.GAP_SECONDS)

    async def test_a_mode_changed_during_the_check_deploys_and_records_nothing(self):
        state = _Hooks(_answer(), deploy=image_updates.ModeChanged("off"))
        assert await _run(state, image_updates.AUTO) == "off"
        assert not state.rows

    async def test_a_switch_to_notify_during_the_check_announces_the_build(self):
        # "off" would answer the bell's notice of a build that is still on offer.
        state = _Hooks(_answer(), deploy=image_updates.ModeChanged("notify"))
        assert await _run(state, image_updates.AUTO) == "available"
        assert [r[0] for r in state.rows] == ["available"]
        assert await _run(state, image_updates.AUTO) == "available"
        assert len(state.rows) == 1

    async def test_a_failed_deploy_is_not_held_and_is_tried_at_the_next_run(self):
        state = _Hooks(_answer(), deploy=image_updates.DeployRefused("registry down", rolled_back=False))
        assert await _run(state, image_updates.AUTO) == "failed"
        assert await _run(state, image_updates.AUTO) == "failed"
        assert len(state.deploys) == 2

    async def test_several_copies_are_reported_and_never_recreated(self):
        answer = _answer()
        answer["containers"].append({**answer["containers"][0], "instance": 2, "container_id": "c2"})
        state = _Hooks(answer)
        assert await _run(state, image_updates.AUTO) == "skipped"
        assert not state.deploys
        result, facts = state.rows[0]
        assert result == "skipped" and "2 copies" in facts["detail"]

    async def test_a_blocked_copy_is_reported_once_and_never_recreated(self):
        state = _Hooks(_answer(), blocker="it differs from what a redeploy builds")
        assert await _run(state, image_updates.AUTO) == "skipped"
        assert await _run(state, image_updates.AUTO) == "skipped"
        assert [r for r, _ in state.rows] == ["skipped"] and not state.deploys

    async def test_a_stopped_copy_is_not_started_by_an_update(self):
        state = _Hooks(_answer(status="exited"))
        assert await _run(state, image_updates.AUTO) == "skipped"
        assert not state.deploys

    async def test_a_box_pauses_after_each_real_update(self):
        state = _Hooks(_answer())
        hooks = state.hooks()
        settings = image_updates.parse_settings({"mode": "auto"})
        out = await image_updates.run_worker(hooks, settings, 1, ["a", "b"])
        assert out == {"a": "updated", "b": "updated"}
        assert hooks.sleep.await_count == 2


class TestSettings:
    def test_the_most_specific_choice_wins(self):
        s = image_updates.parse_settings({"mode": "auto", "workers": {"2": "notify"}, "services": {"proxyrack": "off"}})
        assert image_updates.effective_mode(s, 1, "honeygain") == "auto"
        assert image_updates.effective_mode(s, 2, "honeygain") == "notify"
        assert image_updates.effective_mode(s, 2, "proxyrack") == "off"

    @pytest.mark.parametrize("bad", [["2"], "auto", 3, None])
    def test_an_override_that_is_not_a_map_is_none(self, bad):
        s = image_updates.parse_settings({"mode": "auto", "workers": bad, "services": bad})
        assert s["workers"] == {} and s["services"] == {}

    def test_anything_unreadable_is_off(self):
        assert image_updates.parse_settings("not json")["mode"] == "off"
        assert image_updates.parse_settings({"mode": "always", "hour": 99}) == {
            "mode": "off",
            "hour": image_updates.DEFAULT_HOUR,
            "workers": {},
            "services": {},
        }

    def test_a_run_is_due_once_a_day_from_the_hour(self):
        from datetime import datetime

        s = image_updates.parse_settings({"mode": "auto", "hour": 4})
        assert not image_updates.due(s, datetime(2026, 11, 28, 3, 59))
        assert image_updates.due(s, datetime(2026, 11, 28, 4, 0))
        s["last_run"] = "2026-11-28"
        assert not image_updates.due(s, datetime(2026, 11, 28, 23, 0))
        assert image_updates.due(s, datetime(2026, 11, 29, 4, 5))


@pytest_asyncio.fixture
async def db(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DB_DIR", tmp_path)
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "cashpilot.db")
    return tmp_path


@pytest.mark.asyncio
class TestDefaults:
    async def test_a_new_install_updates_by_itself(self, db):
        await database.init_db()
        settings = image_updates.parse_settings(await database.get_config(image_updates.CONFIG_KEY))
        assert settings["mode"] == "auto" and "offer" not in settings

    async def test_an_upgraded_install_is_offered_and_stays_off(self, db):
        await database.init_db()
        # The install as it was before this release: no table, no setting.
        connection = await database._get_db()
        try:
            await connection.execute("DROP TABLE image_updates")
            await connection.execute("DELETE FROM config WHERE key = ?", (image_updates.CONFIG_KEY,))
            await connection.commit()
        finally:
            await connection.close()
        await database.init_db()
        settings = image_updates.parse_settings(await database.get_config(image_updates.CONFIG_KEY))
        assert settings["mode"] == "off" and settings["offer"] is True
        # A later start never changes the owner's choice.
        await database.set_config(image_updates.CONFIG_KEY, json.dumps({"mode": "notify", "hour": 3}))
        await database.init_db()
        assert image_updates.parse_settings(await database.get_config(image_updates.CONFIG_KEY))["mode"] == "notify"

    async def test_a_first_start_cut_off_before_the_setting_leaves_no_table(self, db, monkeypatch):
        # A start that fails after the schema and before the setting: nothing is
        # kept, so the next start still sees a new install and writes its setting.
        monkeypatch.setattr(database, "_image_updates_seed", lambda fresh: "\nINSERT INTO no_such_table VALUES (1);")
        with pytest.raises(Exception, match="no_such_table"):
            await database.init_db()
        connection = await database._get_db()
        try:
            cursor = await connection.execute("SELECT name FROM sqlite_master WHERE name = 'image_updates'")
            assert await cursor.fetchone() is None
        finally:
            await connection.close()
        monkeypatch.undo()
        monkeypatch.setattr(database, "DB_DIR", db)
        monkeypatch.setattr(database, "DB_PATH", db / "cashpilot.db")
        await database.init_db()
        settings = image_updates.parse_settings(await database.get_config(image_updates.CONFIG_KEY))
        assert settings["mode"] == "auto" and "offer" not in settings

    async def test_pruning_never_releases_a_held_build(self, db, monkeypatch):
        monkeypatch.setattr(database, "IMAGE_UPDATE_ROWS", 3)
        await database.init_db()
        await database.record_image_update(1, "honeygain", "rolled_back", new_image="sha256:bad")
        await database.record_image_update(1, "honeygain", "restore_failed", new_image="sha256:worse")
        for n in range(6):
            await database.record_image_update(1, "honeygain", "available", new_image=f"sha256:{n}")
        assert await database.image_update_seen(1, "honeygain", "sha256:bad", ("rolled_back",))
        assert await database.image_update_seen(1, "honeygain", "sha256:worse", image_updates.HOLDS)
        assert not await database.image_update_seen(1, "honeygain", "sha256:0", ("available",))

    async def test_rows_are_recorded_and_found(self, db):
        await database.init_db()
        await database.record_image_update(1, "honeygain", "rolled_back", new_image="sha256:new", detail="x")
        assert await database.image_update_seen(1, "honeygain", "sha256:new", ("rolled_back",))
        assert not await database.image_update_seen(2, "honeygain", "sha256:new", ("rolled_back",))
        assert (await database.list_image_updates())[0]["result"] == "rolled_back"


def _worker_answer(status, payload):
    resp = MagicMock()
    resp.status_code = status
    resp.json.return_value = payload
    return resp


@pytest.mark.asyncio
class TestTheDashboardSide:
    """What the UI makes of the worker's answers, and the settings routes."""

    async def test_the_workers_undo_reaches_the_dashboard_with_its_reason(self):
        from app.main import _safe_worker_detail

        message = (
            "The new cashpilot-x crashed and was restarted by Docker (1x) within its 120 s check, so it was undone."
        )
        detail = _safe_worker_detail(
            _worker_answer(409, {"detail": {"error": "image_update_rolled_back", "message": message}})
        )
        assert detail == {"error": "image_update_rolled_back", "message": message}

    async def test_an_undone_update_is_recorded_as_undone_and_so_held(self):
        """Seen live: without the worker's code the undo read as a plain failure, which is retried."""
        from fastapi import HTTPException

        from app import main

        refusal = HTTPException(
            status_code=409,
            detail=main._safe_worker_detail(
                _worker_answer(409, {"detail": {"error": "image_update_rolled_back", "message": "undone"}})
            ),
        )
        failed = HTTPException(status_code=502, detail="pull")
        auto = {"mode": "auto", "workers": {}, "services": {}}
        with (
            patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
            patch.object(main, "_deploy", AsyncMock(side_effect=refusal)),
            pytest.raises(image_updates.DeployRefused) as caught,
        ):
            await main._image_update_deploy(1, "honeygain", {"1": "abc"}, "sha256:" + "a" * 64)
        assert caught.value.rolled_back and str(caught.value) == "undone"
        with (
            patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
            patch.object(main, "_deploy", AsyncMock(side_effect=failed)),
            pytest.raises(image_updates.DeployRefused) as caught,
        ):
            await main._image_update_deploy(1, "honeygain", {"1": "abc"}, "sha256:" + "a" * 64)
        assert not caught.value.rolled_back

    @pytest.mark.parametrize(
        ("code", "rolled_back", "restore_failed", "changed"),
        [
            ("image_update_restore_failed", True, True, False),
            ("image_update_restore_failed_unverified", False, True, False),
            ("image_update_unverified", False, False, True),
            ("image_update_unsupported", False, False, False),
        ],
    )
    async def test_each_worker_code_is_recorded_as_what_it_means(self, code, rolled_back, restore_failed, changed):
        from fastapi import HTTPException

        from app import main

        refusal = HTTPException(
            status_code=409,
            detail=main._safe_worker_detail(_worker_answer(409, {"detail": {"error": code, "message": "why"}})),
        )
        auto = {"mode": "auto", "workers": {}, "services": {}}
        with (
            patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
            patch.object(main, "_deploy", AsyncMock(side_effect=refusal)),
            pytest.raises(image_updates.DeployRefused) as caught,
        ):
            await main._image_update_deploy(1, "honeygain", {"1": "abc"}, "sha256:" + "a" * 64)
        assert str(caught.value) == "why"
        assert (caught.value.rolled_back, caught.value.restore_failed) == (rolled_back, restore_failed)
        assert caught.value.changed is changed

    async def test_a_worker_without_the_checked_route_gets_no_image_update(self):
        """The old route ignores the check period and the expected build, so nothing is sent."""
        from fastapi import HTTPException

        from app import main

        current = "a" * 12
        send = AsyncMock(return_value={"container_id": "x"})
        with (
            patch.object(main, "_worker_deploy_target", AsyncMock(return_value=(current, False))),
            patch.object(main, "_proxy_to_worker", send),
        ):
            spec = {"image": "honeygain/honeygain:latest", "settle_seconds": 120, "expect_image": "sha256:" + "b" * 64}
            with pytest.raises(HTTPException) as refused:
                await main._send_worker_deploy(1, "honeygain", spec, expected=current)
            assert refused.value.status_code == 409
            assert refused.value.detail["error"] == "image_update_unsupported"
            send.assert_not_awaited()
            # Control: a plain deploy still takes the old route.
            await main._send_worker_deploy(1, "honeygain", {"image": "honeygain/honeygain:latest"}, expected=current)
        assert send.await_args.args[2] == "/api/containers/honeygain/deploy"

    async def test_a_worker_with_the_checked_route_but_no_image_updates_gets_none(self):
        """Such a worker drops the check period and the expected build too: it says so in its heartbeat."""
        from fastapi import HTTPException

        from app import main

        current = "a" * 12
        spec = {"image": "honeygain/honeygain:latest", "settle_seconds": 120, "expect_image": "sha256:" + "b" * 64}
        for features, sent in ((set(), False), ({image_updates.FEATURE}, True)):
            send = AsyncMock(return_value={"container_id": "x"})
            with (
                patch.object(main, "_worker_deploy_target", AsyncMock(return_value=(current, True))),
                patch.object(main, "_worker_features", AsyncMock(return_value=features)),
                patch.object(main, "_worker_is_desktop", AsyncMock(return_value=False)),
                patch.object(main, "_proxy_to_worker", send),
            ):
                if sent:
                    await main._send_worker_deploy(1, "honeygain", spec, expected=current)
                else:
                    with pytest.raises(HTTPException) as refused:
                        await main._send_worker_deploy(1, "honeygain", spec, expected=current)
                    assert refused.value.detail["error"] == "image_update_unsupported"
            assert send.await_count == (1 if sent else 0), features

    async def test_an_update_the_worker_made_is_recorded_when_the_records_after_it_fail(self):
        from app import main

        done = {"container_id": "new", "image_update": {"new_image": "sha256:" + "a" * 64, "old_kept": ""}}

        async def deploy(*args, **kwargs):
            # The worker's answer arrives through _proxy_worker_deploy, then a record fails.
            with patch.object(main, "_send_worker_deploy", AsyncMock(return_value=done)):
                assert await main._proxy_worker_deploy(1, "honeygain", {"image": "x"}, settle_seconds=120) == done
            raise RuntimeError("database is locked")

        auto = {"mode": "auto", "workers": {}, "services": {}}
        with (
            patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
            patch.object(main, "_image_for_worker", AsyncMock(side_effect=lambda w, s, spec: spec)),
            patch.object(main, "_deploy", deploy),
        ):
            assert await main._image_update_deploy(1, "honeygain", {"1": "abc"}, "sha256:" + "a" * 64) == done
        assert main._image_update_answer.get() is None
        # Control: a failure before the worker answered is still a failure.
        with (
            patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
            patch.object(main, "_deploy", AsyncMock(side_effect=RuntimeError("database is locked"))),
            pytest.raises(RuntimeError),
        ):
            await main._image_update_deploy(1, "honeygain", {"1": "abc"}, "sha256:" + "a" * 64)

    async def test_a_box_whose_worker_is_too_old_is_not_checked_and_says_why(self):
        from app import main

        old = {"id": 1, "status": "online", "system_info": json.dumps({"features": []}), "containers": "[]"}
        new = {**old, "id": 2, "system_info": json.dumps({"features": [image_updates.FEATURE]})}
        # A current worker that cannot reach Docker sends no features either.
        nodock = {**old, "id": 3, "system_info": json.dumps({"features": [], "docker_available": False})}
        assert main._image_update_targets(old) is None and main._image_update_targets(new) == []
        with (
            patch.object(main.database, "list_workers", AsyncMock(return_value=[old, new, nodock])),
            patch.object(main.database, "list_custom_services", AsyncMock(return_value=[])),
            patch.object(main.database, "list_image_updates", AsyncMock(return_value=[])),
            patch.object(main, "_image_update_settings", AsyncMock(return_value=image_updates.parse_settings({}))),
        ):
            response = main.Response()
            page = await main.api_image_updates(response, _auth={"r": "owner"})
        assert response.headers["Cache-Control"] == "no-store"
        assert [(w["id"], w["supported"], w["online"]) for w in page["workers"]] == [
            (1, False, True),
            (2, True, True),
            (3, False, True),
        ]
        assert [w["docker"] for w in page["workers"]] == [True, True, False]
        # The Fleet page names the reason for that box.
        from pathlib import Path

        english = json.loads(Path("app/i18n/en.json").read_text(encoding="utf-8"))
        assert "Update this worker" in english["fleet.updates.box.too_old"]

    async def test_the_update_deploys_the_custom_definition_it_checked(self):
        """An edit saved while the deploy starts must not ride in with the update."""
        from app import main

        checked = {"custom": True, "docker": {"image": "example/mine:latest", "env": [{"key": "A", "default": "old"}]}}
        edited = {"custom": True, "docker": {"image": "example/mine:latest", "env": [{"key": "A", "default": "new"}]}}
        reads = iter([checked, edited, edited])
        deploy = AsyncMock(return_value={})
        auto = {"mode": "auto", "workers": {}, "services": {}}
        main._image_update_checked[(1, "custom-mine")] = {"custom": True, "docker": {"image": "example/mine:latest"}}
        with (
            patch.object(main, "_custom_service", AsyncMock(side_effect=lambda *a, **k: next(reads))),
            patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
            patch.object(main.database, "get_deployment_spec", AsyncMock(return_value={"env": {"A": "old"}})),
            patch.object(main, "_deploy", deploy),
        ):
            await main._image_update_deploy(1, "custom-mine", {"1": "abc"}, "sha256:" + "a" * 64)
        assert deploy.await_args.kwargs["checked_svc"] is checked

    async def test_the_update_deploys_the_catalog_definition_the_blocker_judged(self):
        """A catalog reloaded between the blocker and the deploy cannot bring in a command."""
        from app import main

        judged = {"slug": "honeygain", "docker": {"image": "honeygain/honeygain", "command": "old"}}
        reloaded = {"slug": "honeygain", "docker": {"image": "honeygain/honeygain", "command": "new"}}
        entry = {"slug": "honeygain", "container_id": "abc123def456", "shape": {"image": "honeygain/honeygain"}}
        answer = {"ref": "honeygain/honeygain", "containers": [{"container_id": "abc123def456" + "0" * 52}]}
        with (
            patch.object(main.catalog, "get_service", return_value=judged),
            patch.object(
                main.database, "get_deployment_spec", AsyncMock(return_value={"image": "honeygain/honeygain"})
            ),
            patch.object(main, "_image_for_worker", AsyncMock(side_effect=lambda w, s, asked: asked)),
            patch.object(main.database, "get_worker", AsyncMock(return_value={"containers": json.dumps([entry])})),
            patch.object(main.egress, "container_slug", lambda e: e["slug"]),
            patch.object(main.drift, "container_drift", lambda *a, **k: []),
        ):
            # The blocker lets the update through, then the catalog is reloaded.
            assert await main._image_update_blocker(1, "honeygain", answer) == ""
        deploy = AsyncMock(return_value={})
        auto = {"mode": "auto", "workers": {}, "services": {}}
        with (
            patch.object(main.catalog, "get_service", return_value=reloaded),
            patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
            patch.object(main, "_deploy", deploy),
        ):
            await main._image_update_deploy(1, "honeygain", {"1": "abc"}, "sha256:" + "a" * 64)
        assert deploy.await_args.kwargs["checked_svc"] is judged
        assert (1, "honeygain") not in main._image_update_checked

    async def test_a_catalog_deploy_builds_from_the_definition_it_is_given(self):
        """The catalog reloaded after the check: the deploy still builds from the checked copy."""
        from app import main

        judged = {"slug": "honeygain", "docker": {"image": "honeygain/honeygain", "command": "old"}}
        reloaded = {"slug": "honeygain", "docker": {"image": "honeygain/honeygain", "command": "new"}}
        built = AsyncMock(side_effect=RuntimeError("stop here"))
        with (
            patch.object(main, "_resolve_worker_id", AsyncMock(return_value=1)),
            patch.object(main.catalog, "get_service", return_value=reloaded),
            patch.object(main.database, "get_deployment_spec", AsyncMock(return_value=None)),
            patch.object(main, "_device_names", built),
            pytest.raises(RuntimeError, match="stop here"),
        ):
            await main._deploy("honeygain", main.DeployRequest(), 1, checked_svc=judged)
        assert built.await_args.args[1] is judged["docker"]

    async def test_the_deploy_uses_the_definition_it_is_given(self):
        from app import main

        given = {"custom": True, "name": "Mine", "docker": {"image": "example/mine:latest"}}
        reread = AsyncMock(side_effect=AssertionError("read the definition again"))
        with (
            patch.object(main, "_resolve_worker_id", AsyncMock(return_value=1)),
            patch.object(main, "_custom_service", reread),
            patch.object(main.catalog, "get_service", return_value=None),
            pytest.raises(Exception) as stopped,
        ):
            # An image in the body of a custom deploy is refused right after the
            # definition is read, so the deploy stops there.
            await main._deploy("custom-mine", main.DeployRequest(image="other/image"), 1, checked_svc=given)
        assert "read the definition again" not in str(stopped.value)
        reread.assert_not_awaited()

    async def test_a_choice_saved_during_the_check_is_the_one_that_decides(self):
        """The owner turned the app off while its check ran: nothing is deployed."""
        from app import main

        deploy = AsyncMock()
        saved = {"mode": "auto", "workers": {}, "services": {"honeygain": "off"}}
        with (
            patch.object(main, "_image_update_settings", AsyncMock(return_value=saved)),
            patch.object(main, "_deploy", deploy),
            pytest.raises(image_updates.ModeChanged),
        ):
            await main._image_update_deploy(1, "honeygain", {"1": "abc"}, "sha256:" + "a" * 64)
        deploy.assert_not_called()

    async def test_off_saved_while_the_custom_check_runs_is_the_one_that_decides(self):
        from app import main

        deploy = AsyncMock()
        settings = {"mode": "auto", "workers": {}, "services": {}}

        async def owner_turns_it_off(*_args):
            settings["services"] = {"custom-mine": "off"}
            return False

        with (
            patch.object(main, "_image_update_settings", AsyncMock(side_effect=lambda: dict(settings))),
            patch.object(main.database, "get_deployment_spec", AsyncMock(return_value={"env": {}})),
            patch.object(main, "_custom_service", AsyncMock(return_value={"custom": True, "docker": {}})),
            patch.dict(main._image_update_checked, {(1, "custom-mine"): {"custom": True, "docker": {}}}),
            patch.object(main, "_custom_values_unsaved", owner_turns_it_off),
            patch.object(main, "_deploy", deploy),
            pytest.raises(image_updates.ModeChanged),
        ):
            await main._image_update_deploy(1, "custom-mine", {"1": "abc"}, "sha256:" + "a" * 64)
        deploy.assert_not_called()

    async def test_a_custom_definition_saved_during_the_check_is_not_deployed(self):
        """The blocker judged one command; the owner saved another before the deploy."""
        from app import custom_services, main

        slug = "custom-mine"
        old, _ = custom_services.validate({"name": "Mine", "image": "example/mine:latest", "command": "run --fast"})
        new, _ = custom_services.validate({"name": "Mine", "image": "example/mine:latest", "command": "run --slow"})
        auto = {"mode": "auto", "workers": {}, "services": {}}
        for saved, refused in ((new, True), (old, False)):
            main._image_update_checked[(1, slug)] = custom_services.as_service(slug, old, reveal=False)
            deploy = AsyncMock(return_value={})
            with (
                patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
                patch.object(main.database, "get_deployment_spec", AsyncMock(return_value={"env": {}})),
                patch.object(
                    main,
                    "_custom_service",
                    AsyncMock(return_value=custom_services.as_service(slug, saved, reveal=True)),
                ),
                patch.object(main, "_custom_values_unsaved", AsyncMock(return_value=False)),
                patch.object(main, "_deploy", deploy),
            ):
                if refused:
                    with pytest.raises(image_updates.DeployRefused) as caught:
                        await main._image_update_deploy(1, slug, {"1": "abc"}, "sha256:" + "a" * 64)
                    assert "saved again" in str(caught.value) and not caught.value.rolled_back
                    deploy.assert_not_called()
                else:
                    # Control: the definition it judged is deployed.
                    await main._image_update_deploy(1, slug, {"1": "abc"}, "sha256:" + "a" * 64)
                    deploy.assert_awaited_once()

    async def test_a_bell_rebuild_that_fails_keeps_the_runs_answer_for_the_next_one(self, db):
        from app import main

        await database.init_db()
        await database.record_image_update(1, "honeygain", "available", new_image="sha256:new")
        workers = AsyncMock(return_value=[{"id": 1, "name": "alpha"}])
        with patch.object(main.database, "list_workers", workers), patch.object(main, "_collector_alerts", []):
            await main._refresh_image_update_bell()
            assert "1|honeygain" in main._image_update_bell
            real = main.database.list_newest_image_updates
            with patch.object(
                main.database, "list_newest_image_updates", AsyncMock(side_effect=RuntimeError("locked"))
            ):
                await main._refresh_image_update_bell({1: {"honeygain": "current"}})
            assert main._image_update_bell_loaded is False
            # The next tick rebuilds it, with no outcomes of its own: the run's answer still counts.
            with patch.object(main.database, "list_newest_image_updates", real):
                await main._refresh_image_update_bell()
            assert "1|honeygain" not in main._image_update_bell
            assert main._image_update_bell_loaded is True

    async def test_a_custom_value_saved_after_the_blocker_is_not_deployed(self):
        from app import main

        deploy = AsyncMock()
        auto = {"mode": "auto", "workers": {}, "services": {}}
        with (
            patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
            patch.object(main.database, "get_deployment_spec", AsyncMock(return_value={"env": {"A": "old"}})),
            patch.object(main, "_custom_service", AsyncMock(return_value={"custom": True, "docker": {}})),
            patch.dict(main._image_update_checked, {(1, "custom-mine"): {"custom": True, "docker": {}}}),
            patch.object(main, "_custom_values_unsaved", AsyncMock(return_value=True)),
            patch.object(main, "_deploy", deploy),
            pytest.raises(image_updates.DeployRefused) as caught,
        ):
            await main._image_update_deploy(1, "custom-mine", {"1": "abc"}, "sha256:" + "a" * 64)
        deploy.assert_not_called()
        assert "not deployed yet" in str(caught.value) and not caught.value.rolled_back

    async def test_saving_keeps_the_last_run_and_ends_the_offer(self, db):
        from app import main

        await database.init_db()
        await database.set_config(
            image_updates.CONFIG_KEY, json.dumps({"mode": "off", "hour": 4, "offer": True, "last_run": "2026-11-28"})
        )
        body = main.ImageUpdateSettingsBody(mode="auto", hour=2, workers={"3": "notify", "4": None}, services={})
        saved = (await main.api_set_image_updates(body, _auth={"r": "owner"}))["settings"]
        assert saved["mode"] == "auto" and saved["hour"] == 2 and saved["workers"] == {"3": "notify"}
        assert saved["last_run"] == "2026-11-28" and "offer" not in saved

    async def test_check_now_does_not_use_up_the_daily_run(self, db):
        from zoneinfo import ZoneInfo

        from app import main

        # 05:00 for the owner, in their own zone; the server's clock is not asked.
        five_am = datetime(2026, 11, 28, 5, 0, tzinfo=ZoneInfo("Asia/Singapore"))
        await database.init_db()
        with (
            patch.object(main, "_obligations_now", AsyncMock(return_value=five_am)),
            patch.object(main.database, "list_workers", AsyncMock(return_value=[])),
            patch.object(main, "_refresh_image_update_bell", AsyncMock()),
        ):
            await main._run_image_updates(force=True)
            assert "last_run" not in await main._image_update_settings()
            # A new install is on Update automatically, and 05:00 is past its hour.
            await main._run_image_updates()
            assert (await main._image_update_settings())["last_run"] == "2026-11-28"

    async def test_a_current_check_keeps_the_old_warning_out_of_the_bell_after_a_restart(self, db):
        from app import main

        await database.init_db()
        await database.record_image_update(1, "honeygain", "available", new_image="sha256:new")
        workers = AsyncMock(return_value=[{"id": 1, "name": "alpha"}])
        with patch.object(main.database, "list_workers", workers), patch.object(main, "_collector_alerts", []):
            await main._refresh_image_update_bell()
            assert "1|honeygain" in main._image_update_bell
            await main._refresh_image_update_bell({1: {"honeygain": "current"}})
            assert "1|honeygain" not in main._image_update_bell
            # A restart rebuilds the bell with no run's outcomes.
            main._image_update_bell.clear()
            await main._refresh_image_update_bell()
            assert "1|honeygain" not in main._image_update_bell
            # A newer row comes back.
            await database.record_image_update(1, "honeygain", "failed", new_image="sha256:newer", detail="x")
            await main._refresh_image_update_bell()
            assert "1|honeygain" in main._image_update_bell

    async def test_a_build_seen_again_after_the_tag_went_back_opens_its_notice_again(self, db):
        from app import main

        await database.init_db()
        await database.set_config(image_updates.CONFIG_KEY, json.dumps({"mode": "notify", "hour": 4}))
        await database.record_image_update(1, "honeygain", "available", new_image="sha256:b")
        workers = AsyncMock(return_value=[{"id": 1, "name": "alpha"}])
        with patch.object(main.database, "list_workers", workers), patch.object(main, "_collector_alerts", []):
            # The tag went back to the running build: the notice is answered.
            await main._refresh_image_update_bell({1: {"honeygain": "current"}})
            assert "1|honeygain" not in main._image_update_bell
            # It moved to B again; Notify finds B's row and writes no new one.
            await main._refresh_image_update_bell({1: {"honeygain": "available"}})
            assert "1|honeygain" in main._image_update_bell
            # And it stays open across a restart.
            main._image_update_bell.clear()
            await main._refresh_image_update_bell()
            assert "1|honeygain" in main._image_update_bell

    async def test_two_bell_rebuilds_at_once_keep_the_answer_of_the_run(self, db):
        from app import main

        await database.init_db()
        await database.record_image_update(1, "honeygain", "available", new_image="sha256:b")
        # An answered row a newer one replaced since: each rebuild drops it, so
        # each one writes, and the later write must not lose the run's answer.
        await database.record_image_update(1, "earnapp", "available", new_image="sha256:c")
        await database.set_config(main._IMAGE_UPDATE_CLEARED_KEY, json.dumps({"1|earnapp": 999}))
        delays = iter([0.05, 0.1])

        async def slow_workers():
            await asyncio.sleep(next(delays, 0))
            return [{"id": 1, "name": "alpha"}]

        with (
            patch.object(main.database, "list_workers", side_effect=slow_workers),
            patch.object(main, "_collector_alerts", []),
        ):
            # A run's rebuild, and a settings save's rebuild that started after it.
            await asyncio.gather(
                main._refresh_image_update_bell({1: {"honeygain": "current"}}), main._refresh_image_update_bell()
            )
            main._image_update_bell.clear()
            await main._refresh_image_update_bell()
        assert "1|honeygain" not in main._image_update_bell

    async def test_off_takes_the_notice_away_at_once_and_keeps_the_history(self, db):
        from app import main

        await database.init_db()
        await database.record_image_update(1, "honeygain", "available", new_image="sha256:b")
        await database.record_image_update(1, "earnapp", "available", new_image="sha256:c")
        workers = AsyncMock(return_value=[{"id": 1, "name": "alpha"}])
        with patch.object(main.database, "list_workers", workers), patch.object(main, "_collector_alerts", []):
            await main._refresh_image_update_bell()
            assert {"1|honeygain", "1|earnapp"} <= set(main._image_update_bell)
            # Fleet Off, with an override that keeps one app on.
            body = main.ImageUpdateSettingsBody(mode="off", hour=4, workers={}, services={"earnapp": "notify"})
            await main.api_set_image_updates(body, _auth={"r": "owner"})
            assert "1|honeygain" not in main._image_update_bell and "1|earnapp" in main._image_update_bell
            main._image_update_bell.clear()
            await main._refresh_image_update_bell()
            assert "1|honeygain" not in main._image_update_bell
        assert len(await database.list_image_updates()) == 2

    async def test_an_old_container_that_did_not_start_again_rings_the_bell_for_the_owner(self, db):
        from app import main

        await database.init_db()
        await database.record_image_update(1, "honeygain", "restore_failed", new_image="sha256:b", detail="x")
        workers = AsyncMock(return_value=[{"id": 1, "name": "alpha"}])
        pushed = []
        push = MagicMock(side_effect=lambda *a: asyncio.sleep(0))
        with (
            patch.object(main.database, "list_workers", workers),
            patch.object(main, "_collector_alerts", []),
            patch.object(main, "_spawn", lambda coro: (pushed.append(coro), coro.close())),
            patch.object(main, "_push_alert", push),
        ):
            await main._refresh_image_update_bell()
        entry = main._image_update_bell["1|honeygain"]
        assert "did not start again" in entry["error"] and entry.get("category") != "notice"
        assert pushed and "needs you" in push.call_args.args[2]
        # Held like an undone build, and never pruned.
        assert await database.image_update_seen(1, "honeygain", "sha256:b", image_updates.HOLDS)

    async def test_a_held_build_answers_its_undo_and_off_does_not(self, db):
        from app import main

        await database.init_db()
        await database.record_image_update(1, "honeygain", "rolled_back", new_image="sha256:b", detail="undone")
        workers = AsyncMock(return_value=[{"id": 1, "name": "alpha"}])
        with (
            patch.object(main.database, "list_workers", workers),
            patch.object(main, "_collector_alerts", []),
            patch.object(main, "_spawn", lambda coro: coro.close()),
            patch.object(main, "_push_alert", MagicMock(side_effect=lambda *a: asyncio.sleep(0))),
        ):
            # Off for a run does not answer it: the entry comes back with the app.
            await main._refresh_image_update_bell({1: {"honeygain": "off"}})
            await main._refresh_image_update_bell()
            assert "1|honeygain" in main._image_update_bell
            # The next check saw the old build back and the new one held: answered.
            await main._refresh_image_update_bell({1: {"honeygain": "held"}})
            assert "1|honeygain" not in main._image_update_bell
            await main._refresh_image_update_bell()
            assert "1|honeygain" not in main._image_update_bell

    async def test_a_held_row_is_pushed_once_not_once_a_day(self, db):
        from app import main

        await database.init_db()
        await database.record_image_update(1, "honeygain", "restore_failed", new_image="sha256:b", detail="x")
        workers = AsyncMock(return_value=[{"id": 1, "name": "alpha"}])
        alert = AsyncMock(return_value=7)
        with (
            patch.object(main.database, "list_workers", workers),
            patch.object(main.database, "record_alert", alert),
            patch.object(main, "_collector_alerts", []),
            patch.object(main, "_spawn", lambda coro: coro.close()),
            patch.object(main, "_push_alert", MagicMock(side_effect=lambda *a: asyncio.sleep(0))),
        ):
            for _ in range(3):
                await main._refresh_image_update_bell()
            assert alert.await_count == 1
            # A newer row of the same app is pushed in its turn.
            await database.record_image_update(1, "honeygain", "rolled_back", new_image="sha256:c", detail="y")
            await main._refresh_image_update_bell()
            assert alert.await_count == 2

    def test_the_bell_texts_name_the_dashboard_and_what_happened(self):
        from app import main

        unjudged = main._image_update_alert_text({"result": "restore_failed", "new_image": "", "detail": ""}, "alpha")
        judged = main._image_update_alert_text({"result": "restore_failed", "new_image": "sha256:b"}, "alpha")
        notice = main._image_update_alert_text({"result": "available", "new_image": "sha256:b"}, "alpha")
        assert unjudged.startswith("An update on alpha left the old container stopped")
        assert judged.startswith("A new build failed on alpha")
        assert all("dashboard" in text and "Fleet page" not in text for text in (unjudged, judged, notice))

    def test_viewers_get_no_image_update_entry(self):
        from app import main

        alerts = [
            {"kind": "collector", "platform": "honeygain", "error": "login failed"},
            {"kind": "image_update", "platform": "Honeygain", "error": "A new build is out"},
        ]

        async def call(role):
            with (
                patch.object(main, "_collector_alerts", alerts),
                patch("app.auth.get_current_user", return_value={"uid": 1, "u": "x", "r": role}),
            ):
                return await main.api_collector_alerts(MagicMock())

        assert [a["kind"] for a in asyncio.run(call("viewer"))["alerts"]] == ["collector"]
        assert [a["kind"] for a in asyncio.run(call("owner"))["alerts"]] == ["collector", "image_update"]

    async def test_a_needs_you_row_stays_in_the_bell_under_long_newer_history(self, db):
        import sqlite3

        from app import main

        await database.init_db()
        await database.record_image_update(1, "honeygain", "restore_failed", new_image="sha256:b", detail="x")
        # More newer rows of other apps than one page of history holds.
        with sqlite3.connect(database.DB_PATH) as raw:
            raw.executemany(
                "INSERT INTO image_updates (worker_id, slug, result, new_image) VALUES (1, ?, 'updated', 'sha256:c')",
                [(f"app{n}",) for n in range(1100)],
            )
        newest = await database.list_newest_image_updates()
        assert len(newest) == 1101 and newest[-1]["result"] == "restore_failed"
        assert await database.newest_image_update(1, "honeygain") == newest[-1]
        assert await database.newest_image_update(1, "nothing") is None
        workers = AsyncMock(return_value=[{"id": 1, "name": "alpha"}])
        with (
            patch.object(main.database, "list_workers", workers),
            patch.object(main, "_collector_alerts", []),
            patch.object(main, "_spawn", lambda coro: coro.close()),
            patch.object(main, "_push_alert", MagicMock(side_effect=lambda *a: asyncio.sleep(0))),
        ):
            await main._refresh_image_update_bell()
        assert "did not start again" in main._image_update_bell["1|honeygain"]["error"]
        # A run asks the same question of the newest row before it announces a build again.
        assert main._image_update_hooks().latest is database.newest_image_update
        assert main._image_update_hooks().mode is main._image_update_mode_now

    async def test_every_tick_writes_the_rows_left_unsaved_even_with_every_app_off(self, db):
        from app import main

        await database.init_db()
        key = (1, "honeygain", "", image_updates.RESTORE_FAILED, 0)
        image_updates._unsaved_rows[key] = {"old_image": "sha256:a", "new_image": "", "detail": "not started"}
        off = image_updates.parse_settings({"mode": "off"})
        with (
            patch.object(main, "_image_update_settings", AsyncMock(return_value=off)),
            patch.object(main, "_obligations_now", AsyncMock(return_value=datetime(2026, 11, 28, 5, 0))),
            patch.object(main.database, "list_workers", AsyncMock(side_effect=AssertionError("no run when Off"))),
        ):
            assert await main._run_image_updates() == {}
        rows = await database.list_image_updates()
        assert [(r["result"], r["detail"]) for r in rows] == [(image_updates.RESTORE_FAILED, "not started")]
        assert not image_updates._unsaved_rows

    async def test_a_row_the_tick_writes_reaches_the_bell_at_once(self, db):
        from app import main

        await database.init_db()
        off = image_updates.parse_settings({"mode": "off"})
        refresh = AsyncMock()
        for pending, rebuilt in ((True, 1), (False, 0)):
            if pending:
                image_updates._unsaved_rows[(1, "honeygain", "", image_updates.RESTORE_FAILED, 0)] = {"new_image": ""}
            with (
                patch.object(main, "_image_update_settings", AsyncMock(return_value=off)),
                patch.object(main, "_obligations_now", AsyncMock(return_value=datetime(2026, 11, 28, 5, 0))),
                patch.object(main, "_refresh_image_update_bell", refresh),
            ):
                await main._run_image_updates()
            assert refresh.await_count == rebuilt
            refresh.reset_mock()

    async def test_a_run_whose_day_cannot_be_stamped_still_answers_the_bell(self, db):
        from zoneinfo import ZoneInfo

        from app import main

        five_am = datetime(2026, 11, 28, 5, 0, tzinfo=ZoneInfo("UTC"))
        await database.init_db()
        auto = image_updates.parse_settings({"mode": "auto", "hour": 5})
        refresh = AsyncMock()
        with (
            patch.object(main, "_obligations_now", AsyncMock(return_value=five_am)),
            patch.object(main, "_image_update_settings", AsyncMock(return_value=auto)),
            patch.object(main.database, "list_workers", AsyncMock(return_value=[])),
            patch.object(main, "_save_image_update_settings", AsyncMock(side_effect=RuntimeError("locked"))),
            patch.object(main, "_refresh_image_update_bell", refresh),
            pytest.raises(RuntimeError),
        ):
            await main._run_image_updates()
        refresh.assert_awaited_once_with({})

    async def test_a_history_row_whose_prune_fails_is_not_left_half_written(self, db, monkeypatch):
        await database.init_db()
        real = database._get_db

        async def failing_prune():
            db_ = await real()

            class _Wrapped:
                def __getattr__(self, name):
                    return getattr(db_, name)

                async def execute(self, sql, *args):
                    if sql.startswith("DELETE FROM image_updates"):
                        raise RuntimeError("database is locked")
                    return await db_.execute(sql, *args)

            return _Wrapped()

        monkeypatch.setattr(database, "_get_db", failing_prune)
        with pytest.raises(RuntimeError):
            await database.record_image_update(1, "honeygain", "updated", new_image="sha256:a")
        monkeypatch.setattr(database, "_get_db", real)
        # The insert went back with the prune: a later write cannot make two of it.
        await database.record_image_update(1, "earnapp", "updated", new_image="sha256:b")
        assert [r["slug"] for r in await database.list_image_updates()] == ["earnapp"]

    async def test_the_prune_keeps_the_newest_row_of_each_app(self, db, monkeypatch):
        monkeypatch.setattr(database, "IMAGE_UPDATE_ROWS", 2)
        await database.init_db()
        await database.record_image_update(1, "honeygain", "restore_failed", new_image="")
        await database.record_image_update(1, "honeygain", "updated", new_image="sha256:a")
        for n in range(4):
            await database.record_image_update(1, f"app{n}", "updated", new_image="sha256:b")
        # The app recovered: its latest result is the update, not the older failure.
        assert (await database.newest_image_update(1, "honeygain"))["result"] == "updated"
        # Older rows that are not the newest of their app still go.
        await database.record_image_update(1, "app0", "updated", new_image="sha256:c")
        assert len([r for r in await database.list_image_updates() if r["slug"] == "app0"]) == 1

    async def test_a_run_that_cannot_list_the_boxes_does_not_use_up_the_day(self, db):
        from zoneinfo import ZoneInfo

        from app import main

        five_am = datetime(2026, 11, 28, 5, 0, tzinfo=ZoneInfo("UTC"))
        await database.init_db()
        with (
            patch.object(main, "_obligations_now", AsyncMock(return_value=five_am)),
            patch.object(main.database, "list_workers", AsyncMock(side_effect=RuntimeError("database is locked"))),
            patch.object(main, "_refresh_image_update_bell", AsyncMock()),
            pytest.raises(RuntimeError),
        ):
            await main._run_image_updates()
        assert "last_run" not in await main._image_update_settings()
        # Control: a run that lists them (none here) counts as the day's run.
        with (
            patch.object(main, "_obligations_now", AsyncMock(return_value=five_am)),
            patch.object(main.database, "list_workers", AsyncMock(return_value=[])),
            patch.object(main, "_refresh_image_update_bell", AsyncMock()),
        ):
            await main._run_image_updates()
        assert (await main._image_update_settings())["last_run"] == "2026-11-28"

    async def test_check_now_waits_for_a_run_in_progress_and_then_checks(self, db):
        from zoneinfo import ZoneInfo

        from app import main

        five_am = datetime(2026, 11, 28, 5, 0, tzinfo=ZoneInfo("UTC"))
        await database.init_db()
        listed = AsyncMock(return_value=[])
        with (
            patch.object(main, "_obligations_now", AsyncMock(return_value=five_am)),
            patch.object(main.database, "list_workers", listed),
            patch.object(main, "_refresh_image_update_bell", AsyncMock()),
        ):
            await main._image_update_lock.acquire()
            try:
                forced = asyncio.create_task(main._run_image_updates(force=True))
                # A tick while the run holds the lock does nothing.
                assert await main._run_image_updates() == {}
                await asyncio.sleep(0.01)
                assert not forced.done()
            finally:
                main._image_update_lock.release()
            await forced
        listed.assert_awaited_once()

    async def test_a_save_during_a_run_is_not_overwritten_by_its_last_run_stamp(self, db):
        from zoneinfo import ZoneInfo

        from app import main

        await database.init_db()
        five_am = datetime(2026, 11, 28, 5, 0, tzinfo=ZoneInfo("UTC"))
        real_get = main._image_update_settings
        saving = asyncio.Event()

        async def slow_get():
            settings = await real_get()
            # The owner saves Off while the run holds its copy of the settings.
            saving.set()
            await asyncio.sleep(0.05)
            return settings

        body = main.ImageUpdateSettingsBody(mode="off", hour=4, workers={}, services={})

        async def owner_saves():
            await saving.wait()
            await main.api_set_image_updates(body, _auth={"r": "owner"})

        with (
            patch.object(main, "_obligations_now", AsyncMock(return_value=five_am)),
            patch.object(main, "_image_update_settings", side_effect=slow_get),
            patch.object(main.database, "list_workers", AsyncMock(return_value=[])),
            patch.object(main, "_refresh_image_update_bell", AsyncMock()),
        ):
            await asyncio.gather(main._run_image_updates(), owner_saves())
        settings = await real_get()
        assert settings["mode"] == "off" and settings["last_run"] == "2026-11-28"


class TestImageCheckEndpoint:
    def test_a_pull_error_never_carries_a_login(self, monkeypatch):
        from fastapi import HTTPException

        from app import worker_api

        monkeypatch.setattr(worker_api, "_verify_api_key", lambda request: None)

        def refused(slug):
            raise orchestrator.ContainerRuntimeError(
                "pull from https://me:hunter2@registry.example/x failed; "
                "blob at https://cdn.example/b?X-Amz-Signature=s3cr3t&X-Amz-Credential=key failed",
                502,
            )

        monkeypatch.setattr(orchestrator, "check_image", refused)
        with pytest.raises(HTTPException) as err:
            asyncio.run(worker_api.api_image_check(MagicMock(), "honeygain"))
        detail = str(err.value.detail)
        assert "hunter2" not in detail and "registry.example" in detail
        assert "s3cr3t" not in detail and "key" not in detail and "cdn.example/b" in detail
        assert err.value.status_code == 502 and err.value.detail["error"] == "image_check_failed"

    @pytest.mark.parametrize(
        ("restored", "verified", "code"),
        [
            (True, True, "image_update_rolled_back"),
            (False, True, "image_update_restore_failed"),
            (True, False, "image_update_unverified"),
            (False, False, "image_update_restore_failed_unverified"),
        ],
    )
    def test_the_worker_names_how_an_undone_update_ended(self, monkeypatch, restored, verified, code):
        from fastapi import HTTPException

        from app import worker_api

        for name in ("_verify_api_key", "_validate_deploy_spec", "_validate_critical_spec", "_validate_route_approval"):
            monkeypatch.setattr(worker_api, name, lambda *args, **kwargs: None)

        def undone(**kwargs):
            raise orchestrator.ImageUpdateFailed("undone", verified=verified, restored=restored)

        monkeypatch.setattr(worker_api, "_deploy_direct", undone)
        spec = worker_api.CheckedDeploySpec(image="honeygain/honeygain:latest")
        with pytest.raises(HTTPException) as err:
            asyncio.run(worker_api.api_deploy_container_checked(MagicMock(), "honeygain", spec))
        assert err.value.status_code == 409 and err.value.detail == {"error": code, "message": "undone"}

    def test_a_refused_stop_answers_409_with_its_reason(self, monkeypatch):
        from fastapi import HTTPException

        from app import worker_api

        monkeypatch.setattr(worker_api, "_verify_api_key", lambda request: None)

        def refused(slug, instance):
            raise orchestrator.ContainerRuntimeError("A deploy of honeygain is still running", 409)

        monkeypatch.setattr(orchestrator, "stop_service", refused)
        with pytest.raises(HTTPException) as err:
            asyncio.run(worker_api.api_stop_container(MagicMock(), "honeygain"))
        assert err.value.status_code == 409 and "still running" in err.value.detail

    def test_the_dashboard_forwards_the_reason_of_a_failed_pull(self):
        from app import main

        resp = MagicMock(status_code=502)
        resp.json.return_value = {"detail": {"error": "image_check_failed", "message": "manifest unknown"}}
        assert main._safe_worker_detail(resp) == {"error": "image_check_failed", "message": "manifest unknown"}

    def test_a_failed_check_names_the_workers_reason(self, monkeypatch):
        from fastapi import HTTPException

        from app import main

        async def refused(*args, **kwargs):
            raise HTTPException(status_code=502, detail={"error": "image_check_failed", "message": "manifest unknown"})

        monkeypatch.setattr(main, "_proxy_to_worker", refused)
        with pytest.raises(RuntimeError, match="manifest unknown"):
            asyncio.run(main._image_update_check(1, "honeygain"))


@pytest.mark.asyncio
class TestStartupBell:
    async def test_the_startup_bell_waits_for_a_run_in_progress(self, monkeypatch):
        from app import main

        refresh, run = AsyncMock(), AsyncMock()
        monkeypatch.setattr(main, "_refresh_image_update_bell", refresh)
        monkeypatch.setattr(main, "_run_image_updates", run)
        monkeypatch.setattr(main, "_image_update_bell_loaded", False)
        async with main._image_update_lock:
            # A forced run holds the lock, and rebuilds the bell when it ends.
            await main._image_update_tick()
        refresh.assert_not_awaited()
        # Control: with no run in progress, the startup read happens.
        await main._image_update_tick()
        refresh.assert_awaited_once()


@pytest.mark.asyncio
class TestCustomServiceBlocker:
    """An edit to a custom service waits for the owner's Redeploy (api_update_custom_service).

    So an update, which is a redeploy too, must not be what brings it in: the
    blocker judges the container against the saved definition.
    """

    async def _blocker(
        self,
        monkeypatch,
        saved,
        made_with,
        *,
        instances=1,
        deployed_env=None,
        image_volumes=(),
        reported_id="abc123def456",
        live_id="abc123def456" + "0" * 52,
    ):
        from app import custom_services, main

        slug = custom_services.SLUG_PREFIX + "mine"
        definition, _ = custom_services.validate(saved)
        recorded = {
            "image": made_with["image"],
            "env": deployed_env or {},
            "command": made_with["command"],
            "instances": instances,
        }
        shape = {
            "image": made_with["image"],
            "mounts": ([made_with["data_path"]] if made_with["data_path"] else []) + list(image_volumes),
            "env_keys": [],
            "restart_policy": "unless-stopped",
        }

        async def custom_service(s, reveal):
            return custom_services.as_service(s, definition, reveal=reveal)

        async def image_for_worker(worker_id, s, asked):
            return asked

        monkeypatch.setattr(main, "_custom_service", custom_service)
        monkeypatch.setattr(main, "_image_for_worker", image_for_worker)
        monkeypatch.setattr(main.database, "get_deployment_spec", AsyncMock(return_value=recorded))
        entry = {"slug": slug, "container_id": reported_id, "shape": shape}
        monkeypatch.setattr(main.database, "get_worker", AsyncMock(return_value={"containers": json.dumps([entry])}))
        # The box reports the short ID; the check answers with the full one.
        answer = {"ref": made_with["image"], "containers": [{"container_id": live_id}]}
        return await main._image_update_blocker(1, slug, answer)

    async def test_an_unchanged_definition_is_updated(self, monkeypatch):
        made = {"image": "example/mine:latest", "command": "run --fast", "data_path": "/data"}
        saved = {"name": "Mine", "image": "example/mine:latest", "command": "run --fast", "data_path": "/data"}
        assert await self._blocker(monkeypatch, saved, made) == ""
        # The definition it judged waits for the deploy, which refuses any other.
        from app import main

        assert main._image_update_checked[(1, "custom-mine")]["docker"]["command"] == "run --fast"

    async def test_a_container_the_last_report_does_not_describe_is_left_for_the_next_run(self, monkeypatch):
        # The box replaced it after its last report: that report's shape is of another container.
        made = {"image": "example/mine:latest", "command": "", "data_path": ""}
        saved = {"name": "Mine", "image": "example/mine:latest", "command": "", "data_path": ""}
        why = await self._blocker(monkeypatch, saved, made, live_id="fff000" + "0" * 58)
        assert "does not describe the container that runs now" in why

    async def test_a_saved_command_not_deployed_yet_is_left_to_the_owner(self, monkeypatch):
        made = {"image": "example/mine:latest", "command": "run --fast", "data_path": ""}
        saved = {"name": "Mine", "image": "example/mine:latest", "command": "run --slow", "data_path": ""}
        assert "older command" in await self._blocker(monkeypatch, saved, made)

    async def test_a_saved_data_path_not_deployed_yet_is_left_to_the_owner(self, monkeypatch):
        made = {"image": "example/mine:latest", "command": "", "data_path": ""}
        saved = {"name": "Mine", "image": "example/mine:latest", "command": "", "data_path": "/data"}
        assert "/data" in await self._blocker(monkeypatch, saved, made)

    async def test_a_box_recorded_with_several_copies_is_left_to_the_owner(self, monkeypatch):
        # Only one copy runs now, but a redeploy rebuilds every recorded copy.
        made = {"image": "example/mine:latest", "command": "", "data_path": ""}
        saved = {"name": "Mine", "image": "example/mine:latest", "command": "", "data_path": ""}
        assert "2 copies" in await self._blocker(monkeypatch, saved, made, instances=2)

    async def test_a_saved_value_not_deployed_yet_is_left_to_the_owner_without_naming_it(self, monkeypatch):
        made = {"image": "example/mine:latest", "command": "", "data_path": ""}
        saved = {"name": "Mine", "image": "example/mine:latest", "env": [{"key": "GREETING", "value": "new-value"}]}
        why = await self._blocker(monkeypatch, saved, made, deployed_env={"GREETING": "old-value"})
        assert "not deployed yet" in why and "new-value" not in why and "old-value" not in why
        assert await self._blocker(monkeypatch, saved, made, deployed_env={"GREETING": "new-value"}) == ""

    async def test_a_hostname_value_compares_as_the_redeploy_fills_it(self, monkeypatch):
        from app import main

        made = {"image": "example/mine:latest", "command": "", "data_path": ""}
        saved = {"name": "Mine", "image": "example/mine:latest", "env": [{"key": "NAME", "value": "box-{hostname}"}]}
        own = main._device_hostname({}, 1)
        assert await self._blocker(monkeypatch, saved, made, deployed_env={"NAME": f"box-{own}"}) == ""
        # The template changed since the deploy: the redeploy would bring it in.
        why = await self._blocker(monkeypatch, saved, made, deployed_env={"NAME": f"node-{own}"})
        assert "not deployed yet" in why

    async def test_a_device_with_the_old_shared_name_keeps_it_as_the_redeploy_does(self, monkeypatch):
        from app import main

        made = {"image": "example/mine:latest", "command": "", "data_path": ""}
        saved = {"name": "Mine", "image": "example/mine:latest", "env": [{"key": "NAME", "value": "box-{hostname}"}]}
        legacy = f"box-{main.HOSTNAME_PREFIX}"
        assert await self._blocker(monkeypatch, saved, made, deployed_env={"NAME": legacy}) == ""
        # Control: an edited template is still a saved value not deployed yet.
        edited = {**saved, "env": [{"key": "NAME", "value": "node-{hostname}"}]}
        assert "not deployed yet" in await self._blocker(monkeypatch, edited, made, deployed_env={"NAME": legacy})

    async def test_data_in_an_image_volume_outside_the_data_path_is_left_to_the_owner(self, monkeypatch):
        # The new container would get an empty anonymous volume, and the old one
        # goes with the old container.
        made = {"image": "example/mine:latest", "command": "", "data_path": "/data"}
        saved = {"name": "Mine", "image": "example/mine:latest", "data_path": "/data"}
        why = await self._blocker(monkeypatch, saved, made, image_volumes=["/var/lib/mine"])
        assert "/var/lib/mine" in why and "empty" in why
        assert await self._blocker(monkeypatch, saved, made) == ""
