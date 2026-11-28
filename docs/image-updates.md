# App image updates

Most apps in the catalog follow a tag, such as `latest`, `lite` or no tag at
all. The provider ships each new build under the same tag. CashPilot checks
these tags once a day and installs the new builds. You control this on the
**Fleet** page, in the **App image updates** section.

This page is about the images of the apps that CashPilot deploys. To update
CashPilot itself, see [Updating CashPilot](getting-started.md#updating-cashpilot).

## The three choices

| Choice | What CashPilot does |
|---|---|
| **Off** | Nothing. No check, no pull. |
| **Notify only** | It checks each app and shows a new build in the bell and in the table on the Fleet page. It changes no container. The check downloads the new build, so it is on the box when you redeploy. |
| **Update automatically** | It checks each app and installs a new build. |

You make one choice for the whole fleet, and you pick the hour of the daily
check. It is 04:00 by default, in your account's time zone, else in the
dashboard's. Under **Choices per box and per app** you can give one box or one
app its own choice:

1. An app's own choice wins.
2. Else the choice of its box wins.
3. Else the fleet's choice applies.

For example, set the fleet to **Update automatically** and one app to
**Notify only**. That app then waits for you on every box.

A new install starts on **Update automatically**. An install that you upgrade
from an older release starts on **Off**, and the Fleet page offers one button
to turn the updates on. CashPilot never turns them on for you.

**Check now** runs the daily check at once.

## How one update works

1. The worker pulls the tag that the app runs. If the registry has no new
   build, the pull changes nothing and the container is not touched.
   CashPilot installs only the build that this check found. If the tag moves
   again before the update starts, nothing changes, and the next check tries
   the newer build.
2. With a new build, CashPilot runs the same redeploy as the **Redeploy**
   button. The container gets the settings that it was deployed with. These
   are the variables, the volumes and the app's identity, the network and the
   LAN fence, the runtime, the labels and the resource limits.
3. The worker watches the new container for 2 minutes. During that time the
   old container stays on the box, stopped.
4. If the new container stops, restarts, shows an unhealthy Docker health
   check, or logs one of the app's known failure lines, the worker removes it.
   A health check that has still not passed 30 seconds after the period counts
   as a failure too.
   Then it starts the old container again, with its old image. The table and
   the bell show **Undone**. An undo puts back the container, not the data:
   the old and the new container use the same volume, so anything the new
   build wrote there stays.
   If the old container does not start again either, the table and the bell
   show **Needs you**. The same goes for an update that Docker refused after
   it had set the old container aside. The app is down on that box until you start or
   redeploy it from the dashboard.
   Sometimes Docker cannot show how the new container did. Then the worker
   undoes it the same way, but the table shows **Failed**. The next daily
   check tries that build again.
5. If the new container passes, the worker removes the old container and its
   image.

CashPilot never tries a build that failed its check again on that box, even
when it also needed you. It tries the next new build. So an app that fails after each update cannot go round in a
loop.

Each box updates one app at a time, with a minute between two updates. All
boxes run their checks at the same hour.

## When an app is not updated by itself

With **Update automatically**, CashPilot still leaves some apps for you. The
table shows **Not installed** and the reason:

- The container differs from what a redeploy builds. For example, the catalog
  added a capability after you deployed the app, or you changed the command or
  data path of your own app and did not redeploy it yet. Redeploy it from the
  dashboard once, and the next build installs by itself.
- The app runs an image other than the one that a redeploy would use.
- The app is stopped. An update would start it.
- The app runs more than one copy on the box. Use **Redeploy** to update the
  copies.
- The app runs through a proxy. CashPilot does not yet update a copy behind a
  proxy by itself.
- Your own app keeps data in a folder outside its data path. The image
  declares that folder, so Docker gives each new container an empty one. Set
  the folder as the data path and redeploy, and the next build installs by
  itself.
- The box has no deployment record of the app, for example because you made
  the container by hand.

An update that did not go through for another reason, such as a registry that
did not answer, shows **Failed**. CashPilot tries again at the next daily check.

## Limits

These are known limits of this release:

- **The tag decides the build.** Automatic mode installs whatever the app's
  publisher puts under the tag that the app follows, such as `:latest`.
  CashPilot checks that the new container runs, not who made the build. If
  you do not trust a publisher to do this, choose **Notify only** for that app.
- **Data is not undone.** An undo puts back the old container and its image.
  It does not put back the files in the app's volume. A new build that changes
  its data, for example with a migration, leaves the changed data to the old
  build.
- **Apps run without you watching.** Apps that keep state in a volume are
  updated by themselves too, against their live volume. CashPilot keeps the
  volume. Choose **Notify only** for an app where you want to be there.
- **A lost answer counts as Failed.** If the dashboard loses the worker's
  answer during an update, the table shows **Failed**, even when the update
  went through. The next daily check sees the build that runs and says so.
- **A worker that stops during the check period.** The worker can restart
  during the 2 minutes. Then the new container keeps running without the rest
  of its check. The old one stays stopped as `<name>-replaced`. Remove that
  container when the new build works. To go back to the old build, stop the
  new container first, because it still holds the app's ports, and then start
  the old one.
- **A dashboard that restarts before it can save an undo.** The database
  can fail to save the row of an undone update. Then the dashboard keeps the
  hold in memory and saves it on a later check. If the dashboard restarts
  before that, the hold is lost. The next daily run then tries that build once
  more, and its check undoes it again.

## What CashPilot does not update

- **An image pinned by digest.** Some catalog entries pin one exact build, such
  as `image@sha256:...`. A CashPilot release moves those pins, and a redeploy
  then installs the new build.
- **A box with an older worker.** Update the worker first. The Fleet page says
  which boxes are too old.
- **CashPilot Desktop.** Desktop updates its own apps. Set it in Desktop's own
  settings.

## Old images

After an update, the worker deletes the image that the old container ran, if
no other container uses it. The worker can do this only when it has the raw
Docker socket, as the Unraid and TrueNAS listings give it.

With the shipped compose files, the worker reaches Docker through the socket
proxy. The proxy refuses every image delete, because it cannot tell which
program an image belongs to. So the old images stay on disk, and the table
says so. Remove them from time to time with the steps in
[Cleaning up old images](getting-started.md#cleaning-up-old-images). Step 1
there (`docker image prune`) removes the old builds that no tag names any
more, which is what an update over a moving tag leaves. An old build that
still has another tag stays. Step 2 there removes those.

## Turn the updates off

- For the whole fleet: on the Fleet page, set **Every app on every box** to
  **Off**. A box or an app with its own choice keeps it, so open **Choices per
  box and per app** and set each of those to **Off** too. Then press **Save**.
- For one box or one app: open **Choices per box and per app**, set that box
  or app to **Off** and press **Save**. An app with its own choice keeps it on
  a box set to **Off**, because the app's choice wins. To stop that app on that
  box too, set the app to **Off**. That stops the app on every box.

Off stops the daily check at once. It does not undo an update that already
happened. To go back to an older build, deploy the app with that image from its
service page.
