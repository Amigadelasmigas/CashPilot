# Design 4: Presets first

Mockup: `index.html` in this folder. Screenshots: `shot-1440.png`,
`shot-900.png`, `shot-390.png` (full page, dark, rendered on the MacMini).
Panels (a) to (h) are stacked in that order on one page.

## The idea in four lines

- **Money waiting.** Each row has two controls, always in the same place: a
  pink "Open {name}" link, and a split button. The split button says what you
  did at the provider (Done, Requested, It arrived). Its caret holds "Later"
  (snooze) and "Stop reminding me" (mute).
- **Source becomes a "Provider's rule" chip.** It sits next to the date. It
  opens a small panel that says whose rule it is, links to the provider's own
  page, and gives the date we last read that page.
- **Notifications start with four presets:** Everything (today's behaviour),
  Only money, Only problems, Nothing. Everything else is behind one "Advanced"
  disclosure: each kind by surface, a minimum level, each channel, quiet hours,
  and the mute list.
- **The Dashboard never hides a fault.** Notification choices change only what
  interrupts you (badge, pop-up, browser notification, push). The bell list,
  Needs attention and Money waiting always show everything. A check that cannot
  go red is not a check, so "off" never means "all clear".

## What changed versus today, and why

### Money waiting rows

| Today | This design | Why |
|---|---|---|
| Up to four buttons plus a "More" menu, capped at 320 px, so they wrap onto two or three lines | Two controls: "Open {name}" and a split button. One line at 1440 and 900 px. The list is one CSS grid and each row is a subgrid, so the buttons line up in columns across rows | The owner wants one line on a desktop. Two fixed controls cannot wrap, and every row reads the same way |
| "More" holds Snooze a week, Not for me, Mute all, Source | The caret holds two labelled groups: **Later** (Snooze a day, Snooze a week) and **Stop reminding me** (Mute this reminder, Mute all {name} reminders). Each mute has one hint line that says what it stops | A caret on the action it belongs to says "other ways to answer this reminder". "More" said nothing |
| "Source" (viewers) or "Source, checked 2026-11-24" (writers), a bare link | A chip **Provider's rule** in the detail cell. Its panel: "Where this rule comes from", a button "Read it on {domain}", and "We last read that page on 24 Nov 2026" | The label now says what it is. The domain shows before the click, which matters because fake claim sites exist. The date is a calendar day, not raw ISO |
| "Not for me" | **Mute this reminder**, hint: Only "claim" for EarnFM | Says the action and its scope |
| "How" disclosure below the text | A small **How** chip on the date line. It opens the text in place | The row stays short until you ask |
| At 900 px the detail column is squeezed | Between 641 and 1060 px of panel width, the service name moves under the tag, so the detail keeps room | Container queries, not media queries: the panel adapts to its own width wherever it sits |
| At 390 px the actions wrap left-aligned | Same two controls, 32 px tall, "Open" fills the line, the split button keeps 132 px. The caret menu opens below, inside the screen | Nothing moves to a new place between desktop and phone |
| Mute removes the row at once; the toast says "Unmute it at the foot of Money waiting" | The row turns into a grey "Muted" line with **Undo** until the next reload. The toast also has **Undo** | A mute by mistake costs one click to undo, where you made it |
| Foot: "Not for me: {list}" with Unmute links | "{n} reminders are muted" disclosure (with Unmute per entry) and a link **Manage mutes in Settings** | Short by default. Full list in one place |
| `can_snooze` false hides the snooze buttons | The snooze item shows, disabled, with "Too close to the deadline to snooze." | The user learns why, instead of wondering where it went |
| The More menu has no Escape and no click-outside close | Caret menu and rule panel close on Escape and on a click outside; focus returns to the caret or chip. Arrow keys move inside the menu | Fixes a keyboard gap listed in BRIEF 4.11 |

### The trade-off, said plainly

The owner asked for every button on one line on a desktop. This design keeps
Snooze and Mute one click behind the caret, even on a desktop. All controls
still sit on one line and nothing wraps. The bet is that a row reads better as
"one thing to do here, one way to answer it". If the owner wants Snooze
visible too, the cheapest change is a third ghost button "Snooze a day" at
panel widths above 1060 px; the caret then holds only Snooze a week and the
mutes. That adds one column to the same grid.

### Notifications (new section in Settings)

- **Presets.** Four radio cards. "Everything" is selected after an upgrade,
  because it is what CashPilot does today. Each card says in one line what you
  get, plus a two-line "Badge / Push" summary on wide screens.
- **Pause for a while.** 1 day, 3 days, 1 week. While paused, a status line
  says until when, with **Resume now** (panel h).
- **Push channels line.** ntfy, Telegram, webhook, each with an on/off dot.
  With none set: "No push channel is set. Alerts show only in the bell and on
  the Dashboard." (panel h).
- **Advanced** (closed by default; its summary says what is not default, e.g.
  "Now: reminders push only 09:00 to 21:00"):
  1. **What tells you, and how.** One row per kind group, four columns:
     Badge, Pop-up, Browser (on your account) and Push (household). Each row
     shows a real example ("geiserback — Docker unreachable"). "Learn more"
     lists every alert kind by name.
  2. **Minimum level for pushes:** Info and up, Warnings and up, Urgent only.
     "What is urgent?" explains the three levels.
  3. **Channels.** Status, the environment variable that sets it, a
     per-channel filter (All chosen kinds, Urgent only, Money only, Off), and
     **Send a test**.
  4. **Quiet hours.** From, to, days, time zone. During quiet hours: send one
     summary when they end, or drop them. "Urgent ones still come through".
     This replaces the fixed 09:00 to 21:00 window for reminders; the default
     is 21:00 to 09:00 for reminders only, so nothing changes on upgrade.
  5. **Muted services and reminders.** One table: service, what is muted, who
     muted it and when, when it ends, Unmute. An add row: service or box, what
     (reminders, alerts, both), how long.
- **Custom.** Any change under Advanced clears the preset and shows a
  "Custom" pill: "You changed choices under Advanced, so no preset fits."
  Picking a preset again sets every choice to that preset.
- **"Nothing"** (panel g). A status line: "Notifications are off. Nothing
  interrupts you. The Dashboard still shows everything." with **Turn on
  everything**. The bell shows a crossed-out icon and no badge. Its list still
  opens, with a line "Notifications are off. These alerts stay here without a
  badge or push." Money waiting keeps its rows and shows a pill "Reminders do
  not push" that links to the section. The update banner does not show.
- **The bell header** gets a **Notification settings** link (owner).

#### What each preset sets

Badge and Push per kind group. Pop-up and Browser start off in every preset,
because they are new; you turn them on under Advanced.

| Kind group | Everything | Only money | Only problems | Nothing |
|---|---|---|---|---|
| Money waiting reminders | badge, push | badge, push | none | none |
| Payout questions | badge, push | badge, push | none | none |
| Earnings reading problems (collector alerts) | badge, push | none | badge, push | none |
| Earner problems | badge, push | none | badge, push | none |
| Box problems | badge, push | none | badge, push | none |
| Activity alerts (owner only) | badge, push (spike: badge only) | none | badge, push | none |
| Update notices | banner | banner | banner | none |

"None" never removes an entry from the bell list or the Dashboard.

#### Kind groups (every alert kind from BRIEF 6.2)

| Group | Kinds |
|---|---|
| Money waiting reminders | `obligation` (never in the bell today; the badge column then counts Money waiting rows) |
| Payout questions | `payout` |
| Earnings reading problems | `collector`, `notice`, `flatline`, `account_disabled`, credential forecast |
| Earner problems | `container`, `missing`, `proxied`, `stall`, `proxy_cap` |
| Box problems | `worker`, `docker` |
| Activity alerts | `activity_mail`, `activity_lan`, `activity_spike` (spike never pushes) |
| Update notices | update available |

#### Levels (there is no severity field today, so this is new)

| Level | Members |
|---|---|
| Urgent | Money waiting at stage `overdue` or `expired`, or 3 days or fewer left; `account_disabled`; `collector` with category `auth`; `worker`; `docker`; `activity_mail`; `activity_lan` |
| Warning | Money waiting inside 7 days, or `recheck`; `container`, `missing`, `proxied`, `stall`, `proxy_cap`; `payout`; `collector` `transient` or `shape`; `flatline` |
| Info | Everything else: cash-out `ready` and `still-ready`, reminders more than 7 days out, `notice`, credential forecast, `activity_spike`, update available |

#### Who owns which choice

- **Your account** (stored per user, next to theme and language in
  `user_preferences`): Badge, Pop-up, Browser.
- **The household** (one new table): Push per kind, minimum level, channel
  filters, quiet hours, pause, alert mutes. Money waiting mutes stay in
  `obligation_state`, as today.
- Picking a preset writes both parts for the person who saves.
- Open decision: `/settings` is owner only today. Writers and viewers then
  cannot set their own badge. Two options: (1) accept it for now, or (2) open
  the same section from the avatar menu for every role, with the household
  part read-only. This mockup shows the owner's view.

## How each listed problem is solved

| Problem | Where it is solved |
|---|---|
| Secondary actions hide in "More" even on a wide desktop | "More" is gone. The caret on the split button holds them, grouped and labelled (panel a, open) |
| Buttons wrap and misalign | Two fixed controls in grid columns shared by every row (panel a at 1440, and 900 in `shot-900.png`) |
| Only phones may collapse into a menu | At 390 px the same two controls stack under the text; the caret menu is the only menu (panel b) |
| "Source" says nothing | "Provider's rule" chip with an explaining panel, the domain and the formatted date (panel a, open) |
| "Not for me" is unclear | "Mute this reminder" plus a scope hint; "Mute all {name} reminders" plus its hint; a menu footer says a mute is for the whole household |
| Notifications cannot be configured | New Notifications section: presets, pause, Advanced (panels e, f, g) |
| "No warnings from this app" | Preset "Nothing", or "Pause for a while" |
| "Only payouts" | Preset "Only money" |
| "Not at night" | Quiet hours with days and time zone (panel f) |

## Checklist against BRIEF section 9

Money waiting, per row:

- [x] Tag and level colour: unchanged (`.attn-tag`, `.attn-warn` and so on).
- [x] Service name: unchanged; at mid widths it sits under the tag.
- [x] Title with balance and "≈" conversion: unchanged (Storj row).
- [x] Due date, "or earlier", days left / today / days ago: unchanged, on the
  date line, no wrapping.
- [x] Overdue line and recheck line: unchanged (Storj row shows recheck).
- [x] Loss text: unchanged.
- [x] How text: "How" chip, opens in place.
- [x] Open {name}: pink, new tab, now with an external-link icon.
- [x] Done / Requested / It arrived: the main half of the split button.
- [x] Snooze a day: caret menu, "Later".
- [x] Snooze a week: caret menu, "Later".
- [x] Not for me: caret menu, "Mute this reminder".
- [x] Mute all {name} reminders: caret menu, same name.
- [x] Source link and checked date: "Provider's rule" chip panel.
- [x] Viewer variant: "Open" and the chips; no split button (panel h).
  Change: viewers now also see the checked date.
- [x] Snooze when `can_snooze` is false: shown disabled with the reason
  (panel h). Change: today it is hidden.

Money waiting, panel:

- [x] Title and count: unchanged; plus a "Notification settings" link.
- [x] Muted list with Unmute per entry: foot disclosure (panel d) and the
  Settings table.
- [x] Hidden when empty; foot only when only muted entries exist: unchanged
  behaviour.
- [x] "Could not check" row, never an all-clear: unchanged (panel h).
- [x] Success and error toasts: unchanged, plus Undo on the mute toast
  (panels c and h).

Notifications:

- [x] Bell, badge states, empty texts: the badge count, grey and "?" states
  stay; new crossed-out state when off; the empty texts are unchanged.
- [x] Every alert kind by name: "Learn more: what each kind holds".
- [x] Money waiting pushes, 09:00 to 21:00, summary rule: the default quiet
  hours keep that window; the summary rule is in "Learn more".
- [x] Update banner and per-version dismiss: "Update notices" row (banner
  column); per-version dismiss stays.
- [x] ntfy, webhook, Telegram, set by environment: the channel list shows each
  with its variable name; this design keeps them as environment variables.
- [x] No channel configured: status line in panel h.
- [x] Activity alerts owner only; `activity_spike` never pushes: the row says
  "owner only"; the kind list says a spike never pushes.
- [x] Per-reminder and per-service mutes in one place and on the row: the
  Settings table (panels d and f) plus the caret menu and the foot.

## Implementation cost (rough)

Money waiting (no backend change except one field):

| Part | Work | Lines |
|---|---|---|
| Template | `dashboard.html`: the "Notification settings" link in the head | ~3 |
| JS | Rewrite `obligationRow` (split button, chips, how toggle); one menu and popover handler (Escape, click outside, arrow keys, focus return); "just muted" row; toast with an action button; new foot; format `checked` as a date | ~200 |
| CSS | Subgrid list, split button, menu, chip, popover, mid and phone container queries | ~120 |
| Backend | Add `updated_by` and `updated_at` to each `muted[]` entry (`obligations.py`) for "Muted by" | ~8 |

Notifications:

| Part | Work | Lines |
|---|---|---|
| Database | Table `notification_settings` (household, one JSON row); three new keys in `user_preferences` | ~50 |
| API | `GET/POST /api/notifications` (owner for household keys, any role for own keys); `POST /api/notifications/test/{channel}` | ~120 |
| Push gate | In `_push_alert`: kind to group, group and level filter, per-service mute, pause, quiet hours with a held queue and one summary at the end, per-channel filter in `notify.py` | ~200 |
| Money waiting push | Use quiet hours instead of the fixed window (`main.py:10019`) | ~20 |
| Bell | Badge counts only enabled groups; crossed-out icon; header link; `aria-expanded` and Escape | ~60 |
| Pop-ups and browser notifications | Compare each 60 s poll with the last one; toast or `Notification` for new entries; ask permission on first enable. Only while a CashPilot tab is open (no service worker) | ~90 |
| Settings section | Template, load and save, preset to matrix sync, "Custom" detection, mute table and add row | ~150 template, ~220 JS |
| CSS | Presets, segmented control, matrix and its phone layout, channel grid, quiet hours, mute table | ~150 |
| Tests | Push gate (each filter can block and can pass), quiet-hour summary, API roles | ~300 |

Total, roughly 1,700 lines with tests. It splits into three PRs that each ship
alone: (1) Money waiting rows, (2) Notifications section and push gate,
(3) pop-ups and browser notifications.

## What it needs from i18n

New keys, about 95, each into the 19 locales. Groups:

- `app.obl.*`: `mute_this` "Mute this reminder", `mute_this_hint` "Only
  \"{rule}\" for {name}.", `mute_all_hint` "Every reminder for this service.",
  `menu_later` "Later", `menu_stop` "Stop reminding me", `menu_foot` "A mute is
  for everyone in this household. Undo it in Settings, Notifications.",
  `caret_aria` "Snooze or mute this reminder", `rule` "Provider's rule",
  `rule_title` "Where this rule comes from", `rule_body` "{name} states this
  rule on its own site. Read it there to check it.", `rule_link` "Read it on
  {domain}", `rule_checked` "We last read that page on {date}.",
  `muted_now` "You will get no more {name} {rule} reminders, here or as
  pushes.", `muted_tag` "Muted", `undo` "Undo", `muted_count` "{n, plural, one
  {# reminder is muted} other {# reminders are muted}}", `manage_mutes`
  "Manage mutes in Settings", `cannot_snooze` "Too close to the deadline to
  snooze.", `settings_link` "Notification settings", `no_push` "Reminders do
  not push".
- Changed texts: `app.obl.muted` (toast) becomes "Muted the {name} {rule}
  reminder."; `app.obl.muted_list` is replaced by `muted_count`.
  `app.obl.not_for_me`, `app.obl.source`, `app.obl.source_checked` and
  `app.obl.more` are no longer used.
- `settings.notify.*`: title, description, the four presets (name, one-line
  description, summary), "Custom" and its line, pause and its status, channel
  names and states, Advanced and its summary, the seven kind groups with their
  examples, the four column heads and two group heads, the three levels and
  their explanations, channel filter options, "Send a test", quiet hours
  labels and options, the mute table heads, add row options, save and status
  texts, the "off" status and "Turn on everything".
- `base.alerts.*`: "Notification settings", the "off" line in the bell list,
  the crossed-out bell's aria label.
- Weekday short names come from `Intl.DateTimeFormat`, not from new keys.

## Contrast check (classic theme)

Muted text `#a59cb5` on every background this design uses: 7.48:1 on
`#0b0b14`, 7.15:1 on `#11111d`, 6.25:1 on the selected preset card, 6.32:1 on
the warning status band, 6.44:1 on the cyan status band. Dark text on the pink
button: 7.40:1. Focus ring: the theme's cyan `:focus-visible` outline on every
control, including the preset cards (`:has(input:focus-visible)`).

## Mockup limits

- The page shows open states drawn open, because the screenshot script does
  not click. In the app only one menu or panel is open at a time.
- On the phone matrix, the column names are drawn with CSS `attr()`. The real
  template uses a `<label>` per checkbox.
- The 900 px topbar clips "Settings": that is today's topbar, not this design.
