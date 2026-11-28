# Design 1: Inline actions

The mockup is `index.html`. The shots are `shot-1440.png`, `shot-900.png` and
`shot-390.png`, rendered on the MacMini. Every claim about today's code cites
`BRIEF.md` (section numbers) or `file:line` at `aa543a48`.

## The idea in one line

Keep the row (tag, service, detail). Move the actions from a 320 px column
into one line under the row's text. That line never wraps on a desktop. Only
a phone collapses part of it into a menu.

## What changed versus today, and why

| Today | This design | Why |
|---|---|---|
| Actions sit in a fourth grid column capped at 320 px (`style.css:1453-1458`), so four or five buttons wrap onto two or three lines. | Actions sit on one line under the detail text, left-aligned, `flex-wrap: nowrap`. The row grid has three columns. | A line under the text has room for every button. Left alignment puts **Open {name}** at the same x on every row, so the rows line up. |
| A **More** menu on every writer's row, even at 1440 px. | No menu on a desktop. Snooze is a two-button group (`Snooze [1 day][1 week]`). **Stop reminding me** sits at the right end of the line, apart from the doing actions. | The owner wants every action visible on a desktop. Splitting "do" (left) from "stop" (right) makes the line easy to scan. |
| **More** menu at phone width too (same markup). | At ≤600 px of panel width, Snooze and Stop reminding me move into **More**. Open and the main answer (Done, Requested, It arrived) stay on the row. | Allowed at phone widths. The two most common actions stay one tap away. |
| **Source** (viewers) or **Source, checked 2026-11-24** (writers, inside More). | A link in the row's text: **Claim rules at MystNodes, checked 24 Nov 2026 ↗**. Same text for every role. The date is a calendar day, not raw ISO. | The label now says what the page is and whose site it is on. The ↗ and a screen-reader suffix say it opens a new tab. |
| **Not for me** inside More. | **Stop reminding me** on the line. | The words say what happens. |
| A plain success toast "Muted. Unmute it at the foot of Money waiting." | An undo toast: what was stopped, "for everyone here", **Undo**, and **Stop all {name} reminders**. It stays 10 s, and pauses while hovered or focused. | Undo is next to the action. The wider stop is offered at the moment it makes sense. |
| Muted foot: "Not for me: Honeygain, Keep a … Unmute · Repocket, Every reminder Unmute" in one run of text. | A closed disclosure **2 stopped reminders**. Open, it lists one row per stop: service, rule, who and when, **Remind me again**. Under the list: "Stop every reminder for [service] [Stop reminders]". | A list reads better than a joined sentence. The panel stays short when closed. |
| A snooze button disappears when `can_snooze` is false. | The snooze group is replaced by the muted text "Too close to snooze". | The user sees why snooze is missing. The line keeps its shape. |
| No Notifications settings. | A new **Notifications** section, one self-contained block (`.nt`). | Section 2 below. |

### The one action that left the row

**Mute all {name} reminders** is not on the desktop line. It lives in three
places instead:

1. The undo toast, right after **Stop reminding me** ("Stop all MystNodes
   reminders").
2. The stopped list at the foot of Money waiting: "Stop every reminder for
   [service]". Writers reach it here.
3. Settings, Notifications, Muted (owner).

Reason: with it, the line is about 230 px longer. At 900 px it would not fit
next to the others without wrapping. It is the rarest action, and it is the
wider form of Stop reminding me, so it sits one step behind it. **Your call:**
if you want it on the line too, it fits at 1440 px only. Then 900 px needs a
menu again.

## How each listed problem is solved

| Problem | Solution | Where in the mockup |
|---|---|---|
| Secondary actions hide in More on a wide desktop. | No More menu on a desktop. Every action is a visible button. | (a) at 1440 and 900 |
| Buttons wrap and misalign. | One `nowrap` line under the text. Open is always first and left-aligned. Stop is always last and right-aligned. | (a) |
| Only phones may collapse. | A container query at 600 px of panel width. The same markup serves both. | (b), and (a) in `shot-390.png` |
| "Source" gives no hint. | "Claim rules at MystNodes, checked 24 Nov 2026 ↗". The link text names the page type, the provider and the check date. | (a), (b), (h) |
| "Not for me" is unclear. | "Stop reminding me". The toast says "for everyone here". The help line in the stopped list says it again. | (a), (c), (d) |
| Notifications cannot be configured. | A Notifications section in Settings: master switch, pause, six kinds, single alert types, minimum level, quiet hours, ways to tell, channels, muted list. | (e), (f), (g) |

## Checklist against BRIEF.md section 9

### Money waiting, per row

| Item | Where it lives now |
|---|---|
| Tag and level colour | Unchanged: `.attn-tag`, `.attn-fail/warn/ask/unknown`. |
| Service name | Unchanged: `.attn-what`. |
| Title, balance, "≈" conversion | Unchanged: first detail line (Storj row shows "≈ $15.32"). |
| Due date, "or earlier", days left / today / days ago | Unchanged: `.mw-when` (EarnFM row shows "or earlier"). |
| Overdue line and recheck line | Unchanged: `.mw-loss` (Storj row shows the recheck line). |
| Loss text | Unchanged. |
| How (disclosure) | Unchanged label, now on the meta line next to the rules link. Open on the PacketStream row. |
| Open {name} | First on the action line, pink, new tab, ↗. |
| Done / Requested / It arrived | Second on the action line, on desktop and phone. |
| Snooze a day | Desktop: `Snooze [1 day]`, with `aria-label="Snooze a day"`. Phone: More. |
| Snooze a week | Desktop: `[1 week]`, with `aria-label="Snooze a week"`. Phone: More. |
| Not for me (mute one rule) | **Stop reminding me**. Desktop: end of the line. Phone: More. |
| Mute all {name} reminders | Undo toast; stopped list "Stop every reminder for"; Settings, Notifications, Muted. Not on the line (see above). |
| Source link and checked date | "{Kind} rules at {name}, checked {date} ↗" in the row's text, for every role. Absent on rows with no `source` (cash-out), as today. |
| Viewer variant | (h): Open and the rules link only. The stopped list shows without its buttons. |
| Snooze hidden when `can_snooze` is false | Replaced by the muted note "Too close to snooze" (MystNodes row). |

### Money waiting, panel

| Item | Where |
|---|---|
| Title and count | Unchanged. |
| Muted list with Unmute per entry | Foot disclosure "N stopped reminders", one row each, **Remind me again**. (d). |
| Hidden when empty; foot only when only muted entries | Unchanged rules. The foot is a disclosure, so it stays one line. |
| "Could not check" row | (h). Unchanged text, never an all-clear. |
| Success and error toasts | Unchanged for Done and Snooze. Stop gets the undo toast (c). Errors unchanged. |

### Notifications (today's facts)

| Fact | Where the section handles it |
|---|---|
| Bell, badge states, empty texts | "A number on the bell" turns the count off. Badge "?" and grey stay as today. When notifications are off, the bell shows the bell-off glyph and no number, and the open list starts with "Notifications are off. Nothing is sent. Turn on" (g). The empty texts do not change. The bell header gets a "Notification settings" link (owner only). |
| Every alert kind by name | "Choose single alert types (18)": every kind in BRIEF 6.2, grouped under the six kinds, with its code name (`collector`, `notice`, `credential`, `payout`, `flatline`, `account_disabled`, `container`, `missing`, `proxied`, `stall`, `proxy_cap`, `docker`, `worker`, `activity_mail`, `activity_lan`, `activity_spike`, `obligation`, `update`). (f). The code name is the `kind` a webhook receives. |
| Money waiting pushes, 09:00-21:00 window, summary rule | Default quiet hours are 21:00-09:00, every day, with "Let problems through" ticked. That reproduces today: reminders only by day, faults at any hour. The summary rule (more than 3 at once become one) stays in the engine and needs no setting. |
| Update banner and per-version dismiss | Kind "CashPilot updates". Off hides the banner. The per-browser dismiss stays. `CASHPILOT_UPDATE_CHECK=off` still wins. |
| ntfy, webhook, Telegram, set by environment | "A push to your channels": one row per channel with Set up / Not set up, the variable name, an on/off switch and **Send a test**. Values stay in the environment. |
| No channel configured | Each row says "Not set up" with "How to set it up". With none set, the push box shows only those rows. |
| Activity alerts owner only; `activity_spike` never pushes | The kind says "Owner only". The single type says "Unusual hour of traffic, bell only". |
| Per-reminder and per-service mutes in one place | Settings, Notifications, Muted lists both, with Remind me again / Unmute, and an add form "[service] [Reminders and alerts / Reminders only / Alerts only] [Mute]". The Money waiting foot still manages reminder stops for writers. |

Channels that do not exist in the code (Apprise, email, Pushover, Discord,
Slack, Matrix) are not shown. Browser notifications and in-page pop-ups for new
alerts are new, so they carry a **New** chip.

## The Notifications section

One block, `div.card.settings-section.nt#set-notifications`, with no layout
assumption. It drops into any Settings layout. Its parts, top to bottom:

1. **Master switch.** "Notifications are on / off". Off sends nothing and hides
   the bell number. The bell list and the Dashboard still show every problem.
   Off keeps every other choice (g).
2. **Pause.** [1 day / 3 days / 1 week / 30 days] [Pause everything]. While
   paused: "Paused until {date, time}. [Resume now]" (g).
3. **What to tell me about.** One switch per kind: Money waiting reminders,
   Collection problems, Payouts and quiet balances, Earners and workers,
   Activity alerts, CashPilot updates. "Choose single alert types" opens the
   18 kinds.
4. **Minimum level.** Everything / Warnings and problems / Problems only.
   "Which alert has which level" explains the three levels.
5. **Quiet hours.** Switch, from and to, days of the week, "Let problems
   through". Times use the owner's saved time zone.
6. **How to tell me.** A number on the bell; a pop-up in the page (new); a
   browser notification (new); a push to your channels, with the channel rows.
7. **Muted.** Services and reminder rules, with the add form.
8. **Save notifications** and a status, as every Settings section does.

The choices apply to the whole install, as `obligation_state` does today.
Settings is owner only (`app/routers/pages.py:94-101`), so writers keep only the
Money waiting stop list.

## Implementation cost

Rough lines of new or changed code. Tests not counted.

| Part | Work | Lines |
|---|---|---|
| Money waiting template | None. The panel is built in JS. | 0 |
| Money waiting JS (`obligationRow`, `loadMoneyWaiting`, handlers) | New action line, rules link with formatted date, snooze group, phone More, undo toast (a toast variant with buttons and a 10 s life), stopped list with add form. | ~120 |
| Money waiting CSS | `.mwx-*` rules in the mockup's `<style>`, one container query. | ~60 |
| Money waiting backend | Optional: add `updated_by` and `updated_at` to each `muted[]` entry for "sergio, 12 Nov 2026" (`obligations.py:458-471`). Without it, drop that column. | ~10 |
| Settings template | One new section and one index link. | ~150 |
| Settings JS | Load and save, switch states, pause, test-send button. | ~150 |
| Settings CSS | `.nt-*` rules. | ~90 |
| Backend: storage | One table or one JSON row: master, pause_until, kinds, types, level, quiet hours, ways, channel switches, service mutes. | ~60 |
| Backend: API | `GET/POST /api/notifications` (owner), `POST /api/notifications/test/{channel}`, channel status (set or not, never the value). | ~120 |
| Backend: delivery gate | One function in front of `notify.send` (`main.py:1464-1500`): drop or hold by master, pause, kind, level, quiet hours, channel switch, service mute. Held pushes flush when quiet hours end. A level map per kind. The Money waiting window (`main.py:10019`) reads quiet hours instead of its constants. | ~150 |
| Bell JS | Bell-off glyph and state line, no badge when off or when "number on the bell" is off, settings link, header "Alerts". | ~40 |
| Update banner | Hide when the kind is off. | ~5 |
| Browser notifications and pop-ups (new) | `Notification` permission and display while a tab is open, no service worker. Can ship later; the switches can wait for it. | ~80 |

Total: about 1,000 lines. The Money waiting half (about 190 lines) ships alone,
with no backend change.

The action line must not overflow in a long locale. Use a small
`ResizeObserver` on each line: when it overflows, move the right-most actions
into More, the same way the phone does. On English it never triggers on a
desktop. Close More on Escape and on a click outside (BRIEF 4.11 says it does
neither today).

## What it needs from i18n

New keys (English text), then translation into the 19 locales:

- `app.obl.stop` "Stop reminding me"
- `app.obl.remind_again` "Remind me again" (replaces `app.obl.unmute` on the panel)
- `app.obl.snooze` "Snooze", `app.obl.snooze_1d` "1 day", `app.obl.snooze_7d` "1 week" (the existing `app.obl.snooze_day` / `_week` stay as aria-labels and phone menu items)
- `app.obl.too_close` "Too close to snooze"
- `app.obl.rules.claim` "Claim rules at {name}", `app.obl.rules.withdraw` "Payout rules at {name}", `app.obl.rules.keep_active` "Inactivity rules at {name}", `app.obl.rules.renew` "Renewal rules at {name}", `app.obl.rules.act` "Rules at {name}"
- `app.obl.checked` "{rules}, checked {date}", `app.obl.new_tab` "(opens the {name} website in a new tab)"
- `app.obl.stopped_toast` "{name}: \"{title}\" is stopped.", `app.obl.stopped_toast_sub` "No more reminders or pushes for it, for everyone here.", `app.obl.undo` "Undo", `app.obl.stop_all` "Stop all {name} reminders"
- `app.obl.stopped_count` "{n, plural, one {# stopped reminder} other {# stopped reminders}}", `app.obl.stopped_by` "{user}, {date}", `app.obl.stop_every_for` "Stop every reminder for", `app.obl.stop_every_btn` "Stop reminders", `app.obl.stopped_help` "A stopped reminder stays hidden and sends no pushes, for everyone here, until someone starts it again."
- `app.obl.notify_off` "Notifications are off, so no reminder is sent. The list still updates."
- About 70 keys under `settings.notify.*` for the section: titles, the six kinds and their one-line texts, 18 single-type labels, levels and their texts, quiet hours, ways, channel states, muted list, pause, master switch.
- Bell: `app.bell.off_state` "Notifications are off. Nothing is sent.", `app.bell.turn_on` "Turn on", `app.bell.settings` "Notification settings". We suggest renaming `base.alerts` / `base.alerts.header` from "Collector alerts" to "Alerts", because the bell holds every kind (BRIEF 6.2).

Keys that can go: `app.obl.more` stays (phone). `app.obl.not_for_me`,
`app.obl.source`, `app.obl.source_checked`, `app.obl.muted`,
`app.obl.muted_list` are no longer used. The catalog `how` text for
Honeygain's keep-active rule says "choose Not for me"
(`services/bandwidth/honeygain.yml`); it must change to "choose Stop reminding
me", and `docs/reminders.md` with it.

## Sample data, adjusted to the code

- Honeygain shows 20.76 USD, not 18.76. A cash-out row appears only at or
  above the provider minimum, and Honeygain's is $20 (BRIEF section 8).
- PacketStream, EarnFM and Storj rules are samples. Only Honeygain, Repocket,
  Bitping, MystNodes, Salad and Grass have catalog rules.

## Seen on the way, not in scope

At 900 px the real top bar lets the **+ Add service** button overlap the
"Settings" tab (visible in `shot-900.png`; the mockup uses the real
`style.css`). That belongs to the top bar, not to this lane.
