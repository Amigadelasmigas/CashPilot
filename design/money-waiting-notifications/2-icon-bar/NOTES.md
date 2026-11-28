# Design 2: Compact icon bar

Files: `index.html` (the mockup), `shot-1440.png`, `shot-900.png`, `shot-390.png`
(full page, shot on the MacMini). The states are stacked in this order:
(a) Dashboard, (a2) icon key, viewer row and failed check, (b) phone,
(c) just muted, (d) muted list, (e) Notifications defaults, (f) Notifications
customised, (g) everything off, (g2) bell states, (h) no channel set.

## The idea in one paragraph

Each Money waiting row ends in two things. First comes the pink **Open {name}**
button. Then comes one bar of small icon buttons, in fixed slots. Each icon
shows a text label on hover and on keyboard focus, and its `aria-label` holds
the same text. The slots are the same on every row, so the icons line up from
row to row. Nothing hides in a menu on a desktop. On a phone, Open and Done
stay on the row with full text, and the rest go into one menu with full
labels. In Settings, a new **Notifications** section is a grid. The rows are
the kinds of alert and the columns are the places an alert can reach you.

## What changed versus today, and why

### Money waiting rows

| Today | This design | Why |
|---|---|---|
| Actions cell capped at 320 px, buttons wrap onto 2 or 3 lines (`style.css:1453-1475`) | One bar, never wraps. About 330 px of icons plus the Open button | The owner wants every action on one line on a desktop |
| Each row is its own grid, so buttons sit at different x positions | The list is the grid and each row is a CSS `subgrid`. Open buttons start at the same x. Icons sit in fixed slots; a missing action (no rule page on cash-out rows) leaves an empty slot | Alignment makes the rows easy to scan |
| **More** menu on desktop holds Snooze a week, Not for me, Mute all, Source | No menu on desktop. Every action is one click | The owner does not like "More" on a desktop |
| **Source** / **Source, checked 2026-11-24** | Document icon. Label **"{name} rule page"**, second line **"Provider's own terms, new tab. Checked 24 Nov 2026."** | Says what it opens and that it leaves CashPilot. The date is formatted, not raw ISO |
| Viewers see a bare **Source** with no date | Viewers see the same rule-page icon and the checked date | The date helps everyone judge the rule |
| **Not for me** | Bell-off icon. Label **"Mute this {name} reminder"**, second line "Hides it and stops its messages. Undo any time." | Says what happens. "Mute" is a word people know from phones |
| **Mute all {name} reminders** | Bell-off icon with the short text **all**. Label unchanged | The two mutes look related but different |
| **Snooze a day** and **Snooze a week** split across row and menu | Two clock icons with the short text **1d** and **7d** side by side | Same action, same place |
| Snooze buttons vanish when `can_snooze` is false | The two snooze icons stay, greyed, and the label says "Too close to the deadline to snooze" | The user learns why, and the slots stay aligned |
| **How** disclosure inside the text | Question-mark icon in the bar. It opens the How text under the row (`aria-expanded`) | All actions in one place. The text keeps its own line |
| Muted foot: "Not for me: {list}" with Unmute links in one long line | Disclosure **"Muted reminders 2 · Honeygain, Repocket"**. Open, it is a small table: service, reminder, muted by, since, Unmute. Link to Settings | Readable, and it says who muted what |
| Mute shows a toast "Muted. Unmute it at the foot of Money waiting." | The row folds into one line in place, "Muted: {name}, {title}…", with **Undo**, for 10 seconds. The toast has **Undo** too | A mistake costs one click to fix |
| No key for the icons | **"What do the icons do?"** disclosure in the panel head. It lists every icon with its label | First-time users can learn the icons without hovering each one |

Grouping inside the bar, with thin separators: finish (Done, Requested or It
arrived) | delay (1d, 7d) | learn (How, rule page) | silence (mute, mute all).

### Widths

- **1440 px:** five columns: tag, service, text, Open, icon bar. Every action
  on the row's own line.
- **About 900 px** (container under 1060 px): the tag sits above the service
  name. The Open button and the icon bar take one line under the text. The
  text keeps its full width. Still one line of actions.
- **Phone** (container under 600 px): tag and service on the first line, then
  the text, then **Open {name}** (full width), **Done** with its text, and a
  menu button. The menu shows every other action with a full label, the
  snooze reason, and the rule page with its checked date. Touch targets are
  32 px or more. The icon key is hidden on phones, because the menu has labels.
- The breakpoints are **container queries** on the panel, not viewport media
  queries. The panel looks right in any column width. That is also how the
  390 px frame in state (b) renders inside the 1440 px shot.

### Bell

- Header "Collector Alerts" becomes **"Alerts"**, because it holds every kind,
  not only collectors. A **Notification settings** link sits in the header.
- Each entry gets a bell-off icon, **"Mute alerts like this"**. It adds a mute
  for that service and kind. The mute shows in Settings.
- When notifications are off, the bell icon is crossed and has no badge. The
  dropdown still lists every alert, under a line "Notifications are off…
  Turn on".
- New badge state: **paused** shows a small "z". The count, grey and "?" states
  stay as today.

### Notifications section (new)

One self-contained `.settings-section`. It has no layout of its own beyond its
own blocks, so the `design/settings-page` lane can put it anywhere. It has
five blocks:

1. **Master switch** "Notifications On/Off", and **Pause everything for
   1 day / 3 days / 7 days**.
2. **What and where**, the grid.
   - Rows: kinds in six groups. Money (Money waiting reminders, payouts to
     confirm). Collection (login rejected, provider unreachable, page changed,
     note on a reading, login expires soon). Earners (account disabled,
     container stopped, missing from a box, proxied copy down, balance gone
     quiet, almost no traffic, traffic cap). Boxes (box offline, Docker
     unreachable). Activity, owners only (sent mail, reached the home network,
     unusual hour). CashPilot (new version). Every kind in BRIEF section 6.2 is
     a row.
   - Each group row has a three-state checkbox per column, so one click turns
     a whole group off ("collection alerts off" in state f). Groups fold.
   - Columns: **Bell** (top bar, you), **Pop-up** (a toast on the open page,
     you), **Browser** (system notice, this device), **Sent out** (Telegram,
     ntfy, webhook; everyone), **Quiet hours** (holds this kind at night;
     everyone).
   - A level tag per kind: Money, Problem, Warning, Info. **Quick choice:
     Everything / Money and problems / Money only / Custom** and a **Lowest
     level** select cover "only payouts" and "no warnings". Money counts as
     the top level, so the level filter never drops it; its own row does.
   - A dash marks a cell that cannot work, for example "Unusual hour" under
     Sent out (it never pushes today).
3. **Quiet hours:** from, to, days, "quiet all day on" days, time zone,
   "send one summary when quiet hours end", "let a deadline that ends today
   through", "group 4 or more messages into one". A live line says what the
   setting means now ("Next quiet time: tonight 22:00 to Sat 08:00…").
4. **Where messages go:** Telegram, ntfy, webhook and this browser, each with
   its state (Connected / Not set), the variable that sets it, and **Send a
   test** or **How to set it**. A line says what every message gets
   (400-character cut, redaction).
5. **Muted:** every mute in one table, Money waiting mutes and alert mutes
   alike: service, what is muted, by, since, Unmute. Plus a "Mute {service}
   {what}" row to add one.

**Defaults reproduce today exactly** (state e): Bell on for every kind except
Money waiting (today it is never in the bell). Pop-up and Browser off. Sent
out on for every kind that pushes today, off for "Unusual hour" (cannot) and
"New version" (new, off). Quiet hours 21:00 to 09:00, ticked only for Money
waiting, which is today's 09:00-21:00 push window. Group 4 or more is today's
"more than 3 become one summary" rule.

**Scope:** Bell, Pop-up and Browser are per user (Browser is per device).
Sent out, quiet hours and mutes are household-wide, the same as
`obligation_state` today. The block titles say "you" or "everyone".

## How each problem is solved

| Problem | Solution |
|---|---|
| Secondary actions hide in "More" on a wide desktop | No menu above 600 px of panel width. Every action is a visible icon |
| Buttons wrap and misalign | One non-wrapping bar, fixed slots, subgrid columns across rows |
| On phones, actions may collapse | Open and Done stay; one menu with full labels holds the rest |
| "Source" says nothing | "{name} rule page", "Provider's own terms, new tab. Checked {date}." |
| "Not for me" is unclear | "Mute this {name} reminder", "Hides it and stops its messages. Undo any time." Undo in place and in the toast |
| No way to configure notifications | Settings, Notifications: master switch, pause, kind-by-channel grid, presets, lowest level, quiet hours and days, channel status and test, one list of every mute |
| "No warnings from this app" | Master switch off (state g), or Quick choice "Money only" |
| "Only payouts" | Quick choice "Money only", or untick every row except Payouts to confirm |
| "Not at night" | Quiet hours, with days and all-day days (state f) |

## Checklist against BRIEF.md section 9

Money waiting, per row:

- [x] Tag and level colour: unchanged (`.attn-tag`, left border).
- [x] Service name: unchanged.
- [x] Title with balance and "≈": unchanged (Storj row shows "≈ $5.11").
- [x] Due date, "or earlier", days left / today / days ago: unchanged (`.mw-when`).
- [x] Overdue line and recheck line: unchanged (Storj shows the recheck line).
- [x] Loss text: unchanged.
- [x] How text: question-mark icon opens it under the row; phone menu item "How to do it".
- [x] Open {name}: pink button, new tab; `aria-label` "Open {name} (new tab)".
- [x] Done / Requested / It arrived: first slot (check, paper plane, inbox icons); on phone a text button.
- [x] Snooze a day: "1d" clock icon; phone menu.
- [x] Snooze a week: "7d" clock icon; phone menu.
- [x] Not for me: "Mute this {name} reminder" bell-off icon; phone menu; Settings, Muted.
- [x] Mute all {name} reminders: bell-off "all" icon; phone menu; Settings, Muted.
- [x] Source link and checked date: rule-page icon, date in its label; phone menu with date.
- [x] Viewer variant: Open, How and rule page only (state a2); the date now shows for viewers too.
- [x] Snooze when `can_snooze` is false: shown greyed with the reason (MystNodes), instead of hidden.

Money waiting, panel:

- [x] Title and count: unchanged.
- [x] Muted list with Unmute: "Muted reminders" disclosure with table (state d), and Settings, Muted.
- [x] Hidden when empty; foot only when only muted entries exist: state (d) shows that case.
- [x] "Could not check" row: state (a2), never an all-clear.
- [x] Success and error toasts: unchanged; the mute toast gains Undo (state c).

Notifications:

- [x] Bell, badge states (count, grey, "?"), empty texts: state (g2), plus new paused and off states.
- [x] Every alert kind of section 6.2 by name: one grid row each (collector split by category; credential forecast; `obligation` is Money waiting reminders; update is New CashPilot version).
- [x] Money waiting pushes, 09:00-21:00 window, summary rule: the default quiet hours and "group 4 or more" box; the preview line says so.
- [x] Update banner and per-version dismiss: "New CashPilot version" row, Bell cell marked "banner"; dismiss per version stays on the banner.
- [x] ntfy, webhook, Telegram set by environment: "Where messages go" names each variable.
- [x] No channel configured: state (h); Sent out column disabled with "no channel set".
- [x] Activity owner only; `activity_spike` never pushes: group "Activity (owners only)"; dash in its Sent out cell.
- [x] Per-reminder and per-service mutes in one place and on the row: Settings, Muted, plus the row icons and the bell icon.

## Implementation cost (rough)

| Part | Work | Lines |
|---|---|---|
| `app/static/js/app.js` `obligationRow` | Render the icon bar with fixed slots, the phone menu, the How toggle, the undo fold; Escape and outside-click close for the menu; Escape hides a hover label (WCAG 1.4.13) | +140, -40 |
| `app/static/css/style.css` | Subgrid list, icon bar, labels, container queries, undo row, muted table | +130, -10 |
| `app/templates/dashboard.html` | Icon key disclosure in the panel head; `container` on the section | +10 |
| Bell (`base.html`, `app.js` 6774-7024) | Header rename and settings link, per-entry mute icon, off and paused states, toast and `Notification` for new alerts when enabled | +120 |
| `app/templates/settings.html` + JS | The Notifications section: grid, presets, level, quiet hours, channels, mutes, save | +150 template, +300 JS, +150 CSS |
| Backend: storage | Household table `notification_settings` (JSON: per-kind sent/quiet, quiet hours, days, time zone, summary flags, paused_until). Per-user choices (bell, pop-up, browser per kind) in `user_preferences`. New table `alert_mutes(slug, kind, muted_by, muted_at)`; Money waiting mutes stay in `obligation_state` | +120 |
| Backend: delivery | `_push_alert` and the obligation job check kind, level, mutes, pause and quiet hours before `notify.send`; hold and summarise at the end of quiet hours; `/api/collector-alerts` drops muted and per-user-off kinds and adds a `muted` flag | +150 |
| Backend: API | `GET/PUT /api/notifications`, `POST /api/notifications/test/{channel}`, mute add/remove, `muted_by` and `muted_at` on each `muted[]` entry in `/api/obligations` (from `obligation_state.updated_by/updated_at`) | +120 |
| Tests | Delivery filter matrix, quiet hours across midnight and time zones, mutes, defaults equal today's behaviour, API roles | +350 |
| Docs | `docs/reminders.md` (Source and More are gone, new names), `docs/configuration.md` (Settings, Notifications), a new `docs/notifications.md` | +120 |
| Catalog | `services/bandwidth/honeygain.yml` how text says "choose Not for me": change to "choose Mute this reminder", and its `services/_i18n` entries. CashPilot-Desktop syncs the catalog, so it needs the follow-up sync | 1 line + 19 translations |

The Money waiting part alone (rows, phone menu, undo, muted table) is about
300 lines of front end and one small API field. It can ship first, without the
Notifications section.

Limits to know:

- **Browser** notices use the `Notification` API. They work while any CashPilot
  tab is open, also in the background. With no tab open, nothing arrives,
  because there is no service worker and no web push server. The column
  sub-label says "this device"; the channel row says so too.
- **Pop-up** for a new alert works only while a page is open (the bell polls
  every 60 s).
- Settings is owner only (`routers/pages.py:94-101`). Writers and viewers need
  their per-user columns somewhere. Proposal: the same section, with only the
  Bell, Pop-up and Browser columns, opened from the avatar menu.
- Channel values stay environment variables in this design. Setting them in the
  UI is a separate change (secret storage, restart-free reload).
- In the mockup the top bar at 900 px hides two nav links. That is a mockup
  shortcut, not part of the design.

## Accessibility

- Every icon button is a native `<button>` or `<a>` with `aria-label`. The
  visible label is the same text and is `aria-hidden`. It shows on `:hover`
  and `:focus-visible`, so a keyboard user sees it.
- Greyed snooze uses `aria-disabled="true"`, not `disabled`, so it stays
  focusable and its reason can be read.
- How uses `aria-expanded` and `aria-controls`. The phone menu button uses
  `aria-haspopup` and `aria-expanded`; focus returns to it on close.
- Focus ring: the classic theme's cyan `:focus-visible` outline, unchanged.
- Contrast on `#0b0b14`: muted text `#a59cb5` 7.5:1, secondary `#bdb6cf`
  10.0:1, label text on the label box `#171726` 6.8:1 (muted) and 9.1:1
  (secondary), cyan links 10.8:1, dark text on pink 7.4:1.
- Nothing is under 14 px. The short texts "1d", "7d" and "all" are 14 px mono.

## What it needs from i18n

New or changed keys (English shown). All are real strings, translated in the 19
locales. The three short keys need a translator note: "at most 3 characters".

Money waiting (`app.obl.*`):

| Key | English |
|---|---|
| `app.obl.how` (changed) | How to do it |
| `app.obl.rule_page` (replaces `source`) | {name} rule page |
| `app.obl.rule_page_hint` (replaces `source_checked`) | Provider's own terms, new tab. Checked {date}. |
| `app.obl.mute_one` (replaces `not_for_me`) | Mute this {name} reminder |
| `app.obl.mute_one_menu` | Mute this reminder |
| `app.obl.mute_one_hint` | Hides it and stops its messages. Undo any time. |
| `app.obl.mute_all_hint` | Every reminder from this service |
| `app.obl.done_hint` | Hides it until the next time it is due |
| `app.obl.requested_hint` | You asked for the payout. CashPilot asks again in 14 days. |
| `app.obl.snooze_day_hint` / `snooze_week_hint` | Hidden until tomorrow. No messages meanwhile. / Hidden for 7 days. No messages meanwhile. |
| `app.obl.snooze_blocked` | Too close to the deadline to snooze |
| `app.obl.snooze_day_short` / `snooze_week_short` / `mute_all_short` | 1d / 7d / all |
| `app.obl.open_new_tab` | Open {name} (new tab) |
| `app.obl.other_actions` | Other actions for {name} |
| `app.obl.legend` | What do the icons do? |
| `app.obl.muted_title` (replaces `muted_list`) | Muted reminders |
| `app.obl.muted_note` | A muted reminder does not show here and sends no messages. It stays muted for the whole household until someone unmutes it. |
| `app.obl.manage_mutes` | Manage every mute in Settings |
| `app.obl.muted_by` / `app.obl.muted_since` | Muted by / Since |
| `app.obl.muted_row` | Muted: {name}, {title}. It will not show here or send messages. |
| `app.obl.muted` (changed) | Muted {name}: {title}. |
| `app.obl.undo` | Undo |
| `app.obl.notify_off` | Notifications are off, so these reminders are not sent anywhere. |

Removed: `app.obl.more`, `app.obl.not_for_me`, `app.obl.source`,
`app.obl.source_checked`, `app.obl.muted_list`.

Bell: `base.alerts.header` "Alerts" (was "Collector Alerts"),
`base.alerts.settings` "Notification settings", `app.bell.mute_like` "Mute
alerts like this", `app.bell.off_strip` "Notifications are off. Alerts still
show here, with no badge and no messages.", `app.bell.paused` "Paused until
{date}".

Settings (`settings.notify.*`, about 70 keys): section title and description;
master switch and its on/off state; pause and the three lengths; the five
column names with their sub-labels and "you / this device / everyone"; the six
group names; one label and one hint per kind (19 kinds); the four level names;
the four quick choices; lowest level; quiet hours labels, the day names (from
the locale, not new keys), the three checkboxes and the preview sentences;
channel names, states, "Send a test", "How to set it", the redaction line, the
"no channel set" note; the muted table heads, "Mute", the "what" options; save,
reset, saved and unsaved status; the everything-off note.
