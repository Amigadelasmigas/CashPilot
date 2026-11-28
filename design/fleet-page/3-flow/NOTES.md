# Design 3: guided flow

Direction: optimise for understanding. A first-time owner should know what a copy is, and what it will do, before pressing Run.

Files: `index.html` (mockup), `shot.png` (1440 px), `shot-narrow.png` (900 px). The main view is at the top. The state panels sit under it, each one under a dashed cyan label. The cyan labels are mockup furniture, not part of the design.

The mockup builds on PR #940: it shows the per-service ticks and "reduced isolation". Without PR #940 the same layout works. Step 2 then shows the `main` refusals, and the preview has no tick box.

## 1. What changed, and why

### Running costs: a ledger

| Today | Design 3 | Why |
|---|---|---|
| Five full-width blocks. Each one repeats "X earned N last month. Without this machine's power draw CashPilot cannot say…". | One call-out, said once: **Why no cost yet.** Five grey squares show 0 of 5 machines with watts. Under it, one table row per machine. | The reason is the same for all five. Say it once. The table then shows only what differs between machines. |
| Gross figure far right, nothing else. | Columns **Earned · Electricity · Heat credit · Net**. An unknown value reads `not known` or `—`. | The columns stay the same when watts arrive. A known machine fills the empty cells. The layout does not jump. |
| No direct way to fix the unknown cost. | **Add watts** button on each row. It scrolls to that machine's watts field in the Boxes table and puts the cursor in it. | The watts field stays in one place (the Boxes table). No second copy of the rule. |
| A **Heat** disclosure under every machine, always visible. | **Heat ▾** link in the row's action cell. It opens a full-width detail row under the machine. | The form gets the full width, so the 12 months fit on one line. Closed rows cost no height. |
| Per service: `$0.08 − $0.88 = −$0.80`, right-aligned, far from the name. | A second ledger beside the first: **Service · Earned · Electricity · Net**, plus a small bar around zero. Sorted by net, highest first. One line: "6 services earn more than their electricity. 5 earn less." | Columns line up the numbers. The name sits next to its figures. The sort puts winners on top and losers at the bottom. |
| Per-service costs show while every machine cost is unknown. Nothing says why. | Note: "These costs are estimates. No machine has its watts yet, so CashPilot assumes 65 W per machine, or the processor's rated power…" | Today the two blocks look like they disagree. The note says where the per-service figure comes from. |
| Price, currency and Save on one line, with help text beside them. | The same, with help text under the inputs. Save is 30 px high, the same as the inputs. | Small fix. Owner said the first part is fine. |

At 1440 px the two ledgers sit side by side. Under 1180 px they stack.

### Proxies: a card per proxy, a route line per copy

| Today | Design 3 | Why |
|---|---|---|
| A 4-column table. The Copies cell holds seven lines, each with buttons of different widths. | One card per proxy. The head shows **name and target · Exit IP · Traffic · actions**. Under it, a small table of copies: **Copy · Route out · State · buttons**. | Each copy gets its own row. Every button has the same width (86 px), so the buttons form one straight column. |
| Test, Edit, Delete float far right of a tall row. | Test, Edit, Delete sit in the card head, next to the facts they act on. | The actions stay near their object. |
| **Test** tests on the box picked in the copy form. That link is not visible. | **Test on [box ▾] Test** in the card head. | The box choice is visible where it is used. The copy form no longer has a hidden second job. |
| "Proxied copies by the exit IP providers see": a bullet list that repeats every copy. It says "(shared)" for 7 different services. | **Exit IPs the providers see**: one table row per exit IP. A column **What it means** says it in words: "Shared by 7 different services. No service leaves from it twice…". A warning only shows when the **same** service leaves from one IP twice. | "(shared)" for 7 different services is noise. The real problem is the same service twice on one IP. The page now finds that from data it already has (`exits[].members`). |
| A failing copy shows only the raw Docker word. The reason sits in the bell. | The raw word stays. Under it, one muted line with the reason from the open alert, such as "The tunnel of this proxy on watchtower has not been running since 09:12 UTC". | The owner sees why it fails next to the Start button. |
| Cap: one text line. | A meter with a stop line, "46.00 of 50 GB (92%)", "Stops at 95%, resets on day 1", and **Reset** next to it. Over cap: red text, full red meter, and Start disabled with the reason as a tooltip. | The owner sees how close it is at a glance. |

### What is a copy: the route diagram

A **What is a copy?** box sits under the Proxies head. Left side: two lanes.

- The service: `watchtower → your own IP → honeygain (device 1)`
- Its copy: `watchtower → geiserct exit node (proxy) → 203.0.113.71 · ES → honeygain (device 2)`

Right side: five short facts. A copy is a second container. It leaves through the proxy, so the provider sees and pays a second device. The original does not change. If the proxy goes down, the copy stops. Some providers forbid proxies.

The diagram uses the owner's real box, proxy and exit. With no proxy yet (state c), it uses generic words: `your box → proxy → another IP → service`.

Proposed rule: the box is open until the first copy runs. Then it starts closed, and the browser remembers what the owner chose (localStorage).

### Run a copy: three steps and a preview

Today: three selects, a Run button, and one grey sentence. Design 3: three columns, numbered 1, 2, 3, then a preview row.

1. **Pick the box.** Each box shows "12 services · 7 copies". A box that cannot run a copy stays in the list, greyed and dashed, with the reason: "A phone runs no containers, so it cannot run a copy." The page has the data for three reasons: `device_type == "android"`, `docker_available == false`, no `proxy_tunnel` feature ("Update the worker first").
2. **Pick a service on that box.** Three groups:
   - Can run: each with a tag when it needs more, such as `account risk`, `1 tick`, `3 ticks`, and one line that says what that is.
   - Already has a copy through every proxy: small chips. Picking one deploys it again, as the API does today.
   - Cannot run through a proxy: greyed and dashed, with the refusal text from `refusal()`, such as storj "It needs inbound connections on a published port…".
   This answers "why is my service missing": either it is not on this box, or it is in the third group with its reason.
3. **Pick the proxy.** Each proxy shows exit, cap, and whether this service already leaves from that exit. A proxy that cannot carry the service is greyed with the reason. Example: mysterium on a SOCKS5 proxy, "carries its traffic over UDP, which a SOCKS5 or HTTP proxy does not pass".

**Preview** (full width): the route diagram for this choice, then one sentence: "honeygain on watchtower gets a second device. It leaves through 203.0.113.71 · ES. The original honeygain keeps your own IP." Then four short steps: start the tunnel, check the exit is not the box's own IP, start the copy as `watchtower-p1`, the copy shows under the proxy. The tick boxes sit on the right, in an amber box. **Run the copy** stays disabled until every tick is set. A line next to it counts what is left: "Tick 1 more line to run the copy."

After all three picks, each step can fold to its choice and a **Change** link (state b shows this). The main view shows the lists open, so the eligibility is visible in the screenshot.

After Run (state b2): the panel shows the steps as a checklist. The toasts say the same.

### Add a box

The content is today's text. Only the layout changes. Three small boxes answer "where does the box run": a server with Docker, a computer with CashPilot Desktop, an Android phone. Under them, the env block with the key status, Reveal and Copy on the left, and the enrolment-key note on the right. The loopback note and the clipboard fallback stay where they are today. They show only in their states.

### Add or edit a proxy

- Two groups: **The proxy** and **Traffic limit (optional)**.
- **Type** is a three-way switch, not a select. One help line under it changes with the type. "SOCKS5 carries TCP only, not UDP. It is not encrypted." or "A Tailscale exit node carries TCP and UDP…".
- A 4-column grid, so every field has a width from one set. The form is at most 1000 px wide, so inputs do not stretch across 1400 px.
- Edit mode: under each secret field, "A user is stored." Then its **Remove the stored user** box. Add mode shows neither.
- Add mode no longer shows the placeholder "kept if empty, unless the host or port changes". That text has no meaning for a new proxy. For a new Tailscale proxy the auth key says "Needed for a new Tailscale proxy. CashPilot never shows it again."
- **Rotating exit IP** gets one sentence that says when to tick it.
- One line next to Save says what the cap does: "When the cap is reached, every copy through this proxy stops until the reset day."

## 2. The owner's complaints, one by one

| Complaint | Fix |
|---|---|
| Running costs repeats the name and amount in a long sentence five times. | One call-out says the reason once. The machines become ledger rows. |
| A Heat disclosure under each machine. | A Heat link in the action cell, which opens a full-width row. |
| Per-service figures are right-aligned strings far from their labels. | Columns next to the name, sorted by net, with a bar. |
| The proxy Copies cell is 7 lines with buttons that zig-zag. | One row per copy. The buttons have one width and form one column. |
| Test, Edit and Delete float far right. | They sit in the card head. |
| "Proxied copies by the exit IP providers see" repeats every copy. | A table with one row per exit IP and a sentence that says what it means. A warning only for the same service twice. |
| The add-proxy form has mixed widths, the check boxes sit under the inputs, and cap, stop, reset and rotating are crammed onto one row. | Grouped grid, equal columns, a type switch, the Remove boxes under their own field, the traffic limit as its own group. |
| "Run a copy" does not say what a copy is, which services can run, or what happens. | Route diagram, three steps with reasons, and a preview sentence with the risk tick. |

## 3. How a first-time owner learns what a copy is

1. The Proxies head has today's line, "Copies of a service that leave through a proxy instead of the box's own connection", and the **How it works** link.
2. With no proxy, the empty state says "A proxy gives your boxes another public IP. Add one, then run copies of your services through it. Each copy earns as one more device." **Run a copy** is visible but disabled, with "Add a proxy first."
3. The **What is a copy?** diagram is open. It shows two lanes from one box: the original on your own IP, and the copy through the proxy as device 2.
4. In the flow, step 2 says "Only a service already on this box can get a copy." That is the core rule in one sentence.
5. The preview says what happens, with the owner's real names, before anything runs: second device, which exit IP, the original keeps your IP.
6. After Run, the new copy shows as a route line, `watchtower → 203.0.113.71 · ES`, the same shape as the diagram.

## 4. Every action today, and where it lives now

Checked against BRIEF.md.

**Running costs**

- [x] Load and save the electricity price and currency: tariff strip, same ids (`#power-price`, `#power-currency`, `#power-save`), same toasts.
- [x] Per-machine watts: still in the Boxes table (BRIEF 1.2). **Add watts** scrolls there and focuses the field. No new save path.
- [x] Device watts form (device rows only): same form, in the device row's action cell, or in its detail row like Heat. A device row has no Add watts button; its own watts input replaces it.
- [x] Heat form per machine (owner, not `not_metered`): **Heat ▾** detail row, the same `.heat-form` with source, COP, fuel price and 12 months.
- [x] Per-service figures and their notes (`no_heat_per_service`, `withheld`, `unmetered`, `unknown`): per-service ledger and the notes under it.
- [x] Break-even line, heat credit line, expected line, verdict colour: in the machine row, under the name (`m-sub`) when known. The net cell is red for `losing_money`.
- [x] Fleet summary (`economics.summary`): block meta, unchanged.

**Proxies**

- [x] Proxy list, loading, error, empty: cards. Loading and error replace the cards. The empty state is panel (c).
- [x] Test (with a box), Edit, Delete: card head. Test now picks its box in its own select.
- [x] Reset usage: next to the traffic figure, when the cap is on or holds.
- [x] Per copy Stop / Start / Remove: buttons on each copy line. Start shows when the state is not `running`. Remove reads **Withdraw** with PR #940 ticks.
- [x] Removing state: "removing…" with no buttons. The buttons keep their space, so the line does not shift.
- [x] Recovery skipped (`.text-warn`), tripped (PR #940), stopped by the cap: one warning line under the state.
- [x] Start confirmations (`replace_many`, `replace_one`): unchanged, they are `confirm()` dialogs.
- [x] Shared-exit warning: the exit table, and the add-time toast, unchanged.
- [x] Rotating and exit-not-seen groups: rows in the exit table.
- [x] Add and edit a proxy: SOCKS5, HTTP CONNECT, Tailscale and their fields; keep or remove the stored user and password; auth key kept unless the login server changes; traffic cap, stop %, reset day, rotating exit IP. Panels (a1) and (a2).

**Run a copy**

- [x] Box, service, proxy, Run: steps 1-3 and the panel footer.
- [x] "No box can run proxied copies yet": panel (b3).
- [x] The eligibility rule: each refused service shows its own refusal text. The general rule (`fleet.copy.limits`) moves to the hint under step 2's third group, or to the docs.
- [x] Risk ticks (PR #940 `account_risk`, `net_admin`, `net_raw`, `tun_device`, `no_inbound`): the amber box in the preview. Run stays disabled until all are set.
- [x] Needs-failed and Retry (PR #940): same place as the ticks, `.text-warn` plus Retry.
- [x] Own volumes line (PR #940): in the preview, under the sentence (panel b).
- [x] The box, service, proxy and ticks survive the 60 s refresh. Today only the box does. The flow must keep all four.

**Add a box**

- [x] Image line, Desktop line, Docker env line: the three path boxes and the env head.
- [x] Env block, key status badge, Reveal / Hide, Copy, clipboard fallback, loopback note, key note: unchanged ids, new layout.
- [x] Viewer: no Reveal, no Copy, as today.

## 5. Implementation cost (rough)

| Part | Where | Size |
|---|---|---|
| Running costs renderer | `loadFleetEconomics()` in `fleet.html` | Rewrite the machine rows as a table and add the call-out: about 120 lines changed, 40 added. Per-service: about 30 lines. **Add watts**: a scroll and focus to the Boxes row, about 15 lines. |
| Proxy cards and copy lines | `render()` in `fleet.html` | About 30 lines today become about 90. |
| Exit table and same-service check | `renderExits()` | About 8 lines today become about 40. Pure client-side, from `exits[].members`. |
| Failing copy reason | `render()` plus data | Needs the open alert per copy. Either the page reads `/api/collector-alerts` and matches proxy, box and slug, or `/api/proxies` adds `copies[].alert`. The second is cleaner: about 30 lines of Python plus a test. |
| Test on a box | card head | Small. `data-act="test"` reads its own select, not `#copy-worker`. About 10 lines. |
| Proxy form | template | About 22 lines today become about 60 (the grid, the type switch, the help lines, the "stored" lines). `showKind()` and `editForm()` keep their logic. The "stored" lines come from `secrets` booleans, which the API already sends. |
| Run-a-copy flow | template plus JS | The biggest part. About 200 lines of new JS. Step 2 needs the eligibility of every service on the box. PR #940's `GET /api/proxies/{id}/copies/needs?slug=` answers one service at a time, for one proxy. Two options: call it once per service (about 12 calls for watchtower), or add one call `GET /api/proxies/eligibility?worker_id=` that returns each slug's refusal and needs, per proxy kind. The second is about 60 lines of Python plus tests, and keeps `refusal()` as the single rule. |
| Progress in place (b2) | JS | Optional. The POST is one request of up to 180 s, so the page cannot see each step today. Without a new status call, the panel shows "Starting the tunnel, this can take up to a minute" and then the result. |
| Add a box | template | About 15 lines moved. No JS change. |
| CSS | `style.css` | About 170 new lines (the mockup `<style>` has about 230 with the mockup furniture). Rename `f3-` to the app's own names. Three rules for the narrow layout. |

Total, rough: 500 to 650 lines of template and JS changed or added, 170 of CSS, and 60 to 90 of Python if the two API helpers are taken.

## 6. What it needs from i18n

New keys (about 45), all plain strings, with placeholders where a name or number goes:

- Running costs: column heads (`Earned`, `Electricity`, `Heat credit`, `Net`), `not known`, `No watts yet`, `Add watts` and its tooltip, the call-out (two sentences), the "known watts" note, `Sorted by net`, the "{n} services earn more…, {m} earn less" line (plural), the estimate note.
- Proxies: `What is a copy?`, the lane labels and node labels (`your box`, `your own IP`, `the proxy`, `another IP`, `device {n}`), the five facts, `Exit IP the providers see`, `Traffic`, `Test on`, the column heads `Copy`, `Route out`, `State`, the copies summary ("{n} copies · {r} running, {s} stopped…", plural), the exit table heads and its three "What it means" sentences, the empty-state text, `Add a proxy first.`
- Proxy form: the two group names, the three type help lines, `A user is stored.`, `A password is stored.`, the auth-key hint, the rotating hint, the cap line next to Save.
- Run a copy: the three step titles and hints, the box reasons (phone, no Docker, too old), the service tags (`account risk`, `{n} tick(s)` plural), the two group labels, the preview sentence ("{slug} on {box} gets a second device. It leaves through {exit}. The original {slug} keeps your own IP."), the four step lines, "Tick {n} more line(s) to run the copy." (plural), `Change`, "{n} more boxes" and "{n} more services" (plural).

Reused as they are: every `fleet.costs.*`, `fleet.econ.*`, `fleet.heat.*`, `fleet.proxy.*` action and field label, all `api.*` refusal texts, PR #940's tick texts, every `fleet.add.*` and `fleet.key.*`.

Removed or unused: `fleet.proxy.exits_title`, `fleet.proxy.shared`, `fleet.proxy.copy_on`, `fleet.proxy.copy_via`, and `fleet.copy.limits` (it can stay as a hint).

Nothing is baked into an image. The diagram is HTML boxes with text. It wraps when a translation is longer.

The Docker state word (`running`, `exited`, …) stays untranslated, as today. The reason line under it is translated.

## 7. Invented data in the mockup

The real data comes from BRIEF 0.6. These parts are invented to show states: the service counts per box ("12 services"), the services on watchtower outside the 7 copies (honeygain, iproyal, bitping, mysterium, storj, earnapp), the proxies "Residential pool" and "Mobile pool" with their example hosts and exit IPs, the times and dates, the env block's UI URL, and the image tag `3.1`.
