# Recommended design: Money waiting and Notifications

The mockup is `index.html`. The shots are `shot-1440.png`, `shot-900.png` and
`shot-390.png`, rendered on the MacMini and checked by eye at each width.
Claims about today's code cite `BRIEF.md` (section numbers) or `file:line` at
`aa543a48`.

## In one paragraph

Design 1 (inline actions) is the base. All three judges picked it, because it
is the only design that puts every row action on one line as real text on a
desktop. This version keeps that line and fixes the four things the judges
held against it. **Mute all {name}** is back on the line. One word, **Mute**,
is used everywhere. Undo stays next to the row instead of in a short-lived
toast. The Notifications section starts from four presets and has one simple
choice per kind (**Bell number** and **Push**), in place of three filter
layers that overlapped.

## Base and grafts

| From | What we took | Where in the mockup |
|---|---|---|
| 1 inline (base) | Action line under the row text. Open first, the answer button second, `Snooze [1 day] [1 week]`, the stop control at the right end. The rules link becomes row text with a formatted date. Quiet hours sit at the top level. Channel rows have **Send a test**. The bell-off state. | (a), (b), (g), (i) |
| 4 presets | Four preset cards: Everything (as today), Only money, Only problems, Nothing. A **Custom** pill when the choices below match no preset. A per-channel filter "Gets: All pushes / Urgent only / Money only / Nothing". Mutes with an **Ends** date, mutes per box, and a duration in the add form. "When quiet hours end: send one summary, or drop it". A **Notification settings** link in the Money waiting head. One rule: these choices change only what interrupts you, never what the lists show. | (a), (g), (h), (i) |
| 3 row detail | The provider's domain in the rules link ("Claim rules on **help.mystnodes.com**"). One word for the action: **Mute / Muted / Unmute**, the same as the API and Settings. The scope ("for everyone here") stated before the click. The row folds in place with **Undo**. Few kinds with one simple choice each, in place of 18 single types plus a level. | (a), (c), (d), (g) |
| 2 icon bar | Fixed slots, so the buttons line up on every row. The live quiet-hours line ("Now … Next quiet time …"). **Mute** on each bell entry. The bell header "Alerts" with a settings link. Paused and off badge states. **Muted by** and **since** in the mute lists. | (a), (f), (g), (h) |

We did not take design 2's icon buttons, design 3's **Details** toggle, or
design 4's caret menu. Each hides actions on a desktop.

## Defects the judges listed, and what we did

### Money waiting

| Defect | Fix |
|---|---|
| **Mute all {name} reminders** was off the desktop line (all three judges). | The stop control is now a group, `Mute [This reminder] [All {name}]`, the same shape as `Snooze [1 day] [1 week]`. It is on the line at 1440 and 900. On a phone it is in More with **Snooze**. |
| At 900 px the line was full and ran 2 px past the edge. A longer locale would overflow. | When the panel is 1000 px wide or less, the tag and the service name go on one line above the text. The text and the action line then get the full width. At 900 px the longest line (PacketStream) has about 100 px to spare. If a locale still does not fit, a whole group (never half of one) moves to a second line. No ResizeObserver is needed, and no desktop More menu comes back. |
| "Stop reminding me" hid that a mute applies to the whole household. | The word is now **Mute**. A muted line under the panel title says: "Done, Snooze and Mute apply to everyone who uses this CashPilot." The Mute group points to that line (`aria-describedby`). The phone menu and the folded row say "for everyone here" again. |
| Three names for one action (Stop reminding me, stopped, Muted, Remind me again, Unmute). | **Mute** on the row, **Muted reminders** in the foot, **Muted** in Settings, **Unmute** for the way back, everywhere. |
| The undo toast needed a new toast type with buttons and a 10 s timer. Undo ran out with the toast. | No new toast. After Done, Requested, It arrived, Snooze or Mute, the row folds in place to one line (`role="status"`) with **Undo**. It stays until the next reload. After a mute, the line also offers **Mute all {name} reminders**. The plain error toast stays as today. |
| No undo for Done, Requested or Snooze (all four designs). | The same folded line with **Undo**. Mute undo uses the existing `unmute` action. Done and Snooze undo need one new API action, `undo` (implementation step 2). |
| The rules link and How moved around between rows. | One fixed order on one meta line: **How**, then the rules link. An open How puts its text on the next line, so the link never moves (PacketStream row, How open). The trick is CSS only: `display: contents` on the `<details>` and its `::details-content` (Chrome 131+, Safari 18.4+, Firefox 143+). In an older browser the How text shows to the right of the link instead. Nothing is lost. |
| The rules link named the provider but not the domain. | "Claim rules on help.mystnodes.com, checked 24 Nov 2026 ↗". The host comes from `new URL(item.source).hostname` in the browser, so no API change. |
| Open and the next buttons started at different x on each row. | Open and the answer button each sit in a cell with a minimum width. In the app, the JS sets the two widths once per render from the widest Open and answer button in the list (CSS variables `--mw-open-w`, `--mw-answer-w`). Done, Snooze and Mute then start at the same x on every row. |
| On the phone, the open More menu was drawn over the next row. | More opens in the flow, under the line. It pushes the next row down and covers nothing. It needs no outside-click code. Escape closes it (one key handler). |
| When snooze is not allowed, the buttons vanished with no reason. | Kept from design 1: "Too close to snooze" takes their place. On a phone the More menu says the same. |
| Rows got a line taller than today. | True at 1440 (one action line under the text). In exchange, nothing wraps and there is no menu. The loss text and the date stay on the main view, as the warning needs them. |
| Error toast, grey and "?" badges, and the viewer's foot were claimed but not drawn. | All drawn: error toast in (c), badge states in (f), viewer foot in (e). |
| The MystNodes loss text was shorter on the phone than on the desktop. | Same text at every width. |

### Notifications

| Defect | Fix |
|---|---|
| No one-step "only payouts" or "no warnings". | Four preset cards head the section: **Everything (as today)**, **Only money**, **Only problems**, **Nothing**. Each takes one click. |
| Three filter layers overlapped with no rule (kind switch, 18 single types, minimum level). | One layer. Each of six kinds has two checkboxes: **Bell number** (counts on the bell badge) and **Push** (sent to your channels and, if turned on, this browser). There is no separate level control. "Urgent" is used in two places only: quiet hours and a channel filter. One disclosure defines it. |
| "Payouts and quiet balances" bundled two different things. | Two kinds: **Payout questions** and **Earning slowed**. |
| The 18 single types showed internal codes. | No single-type layer. **What each kind includes** lists every alert kind in plain words, with its webhook `kind` name in grey, behind a disclosure. |
| The kind list missed `image_update` (open PR #946). | Listed under **Earners and workers**: "An automatic app update was undone, or the old app did not start again". The urgency map counts the failed restore as urgent. |
| Master switch Off and a group Off meant different things. | No master switch. **Nothing** is a preset. **Pause** is the temporary version. |
| Quiet-hours trap in design 2: quiet hours held only ticked kinds. | Quiet hours apply to every kind. One plain choice says what still gets through: "Every alert. Only reminders wait." (today's behaviour), "Urgent problems only", or "Nothing". |
| Quiet hours were buried under Advanced (design 4), or per group (design 3). | One quiet-hours block at the top level, with a live line: "Now: Sat 28 Nov, 10:42 (Europe/Madrid). Outside quiet hours. Next quiet time: tonight 21:00 to Sun 09:00." |
| Day chips looked the same on and off. | On: pink fill, dark text, a tick. Off: dashed grey outline, muted text. A hint says "A day means the quiet time that starts that evening." |
| At 390 px the quiet-hours "to" field wrapped alone, and the channel rows fell apart. | "from [21:00] to [09:00]" is one unbreakable unit. At phone width each channel row becomes name + **Send a test** on line 1, status and variable on line 2, **Gets** on line 3. |
| Pop-up and browser notification were offered as install-wide, but browser permission is per device. | They sit in their own box, **On this browser only**, saved in `localStorage`. |
| Design 3 dropped pop-up and browser notification. | Both are here, marked **New**. |
| The "Everything" preset in design 4 changed today's bell (Money waiting would count). | Money waiting reminders have no **Bell number** box. The cell says **Dashboard**, because reminders show on the Dashboard and never in the bell list (`main.py:10152-10160`). A box there would let the badge count entries the list does not show. |
| Panel counts and samples disagreed between panels. | Same names and dates in every panel. Counts match the rows drawn. |

## Checklist against BRIEF.md section 9

### Money waiting, per row

| Item | Where it lives now |
|---|---|
| Tag and level colour | Unchanged (`.attn-tag`, `.attn-fail/warn/ask/unknown`). |
| Service name | Unchanged. Beside the tag at 1000 px and less. |
| Title, balance, "≈" | Unchanged (Storj: "41.20 STORJ (≈ $15.32)"). |
| Due date, "or earlier", days left / today / days ago | Unchanged `.mw-when` (EarnFM: "or earlier"). |
| Overdue line and recheck line | Unchanged `.mw-loss`: Storj recheck line (a), Bitping overdue row with "8 days ago" (e). |
| Loss text | Unchanged, on the main view at every width. |
| How (disclosure) | Unchanged label, first on the meta line. |
| Open {name} | First on the action line, pink, new tab, ↗. |
| Done / Requested / It arrived | Second on the line at every width. Folds the row, with Undo. |
| Snooze a day / a week | `Snooze [1 day] [1 week]`, aria-labels "Snooze 1 day" and "Snooze 1 week" (the name holds the visible words, WCAG 2.5.3). Phone: "Snooze a day" and "Snooze a week" in More. |
| Not for me (mute one rule) | `Mute [This reminder]`, aria-label "Mute this reminder". Phone: More. |
| Mute all {name} reminders | `Mute [All {name}]`, aria-label "Mute all {name} reminders". Phone: More. Also on the folded line after a single mute. |
| Source link and checked date | "{Kind} rules on {host}, checked {date} ↗" on the meta line, for every role. None on cash-out rows, as today. |
| Viewer variant | (e): Open, How and the rules link. The muted list without Unmute. |
| Snooze hidden when `can_snooze` is false | Replaced by "Too close to snooze", or "Too late to snooze" on an overdue row (e). |

### Money waiting, panel

| Item | Where |
|---|---|
| Title and count | Unchanged. A **Notification settings** link on the right (owner only). |
| Muted list with Unmute per entry | Foot disclosure **Muted reminders (N)**: service, rule, who and when, end date, **Unmute** (d). After Unmute the line stays with **Mute again** until the next reload (Bitping in (d)). |
| Hidden when empty; foot only when only muted entries | Unchanged rules (e). |
| "Could not check" row | Unchanged (e). Never an all-clear. |
| Success and error toasts | Success: the folded row replaces the success toast for Done, Snooze and Mute, and the "Unmuted" line replaces it for Unmute. Error: today's error toast (c). |

### Notifications (today's facts)

| Fact | Where the section handles it |
|---|---|
| Bell, its badge states, its empty texts | (f): the list while paused (state line, "All collectors healthy") and with the preset Nothing; the other empty texts quoted as today; red count, grey count (forecasts only), grey "?" (fetch failed), no number (nothing counts), bell-off glyph (preset Nothing), grey "z" (paused). Empty texts unchanged. Header renamed "Alerts" (it holds every kind, BRIEF 6.2), with a settings link. |
| Every alert kind by name | **What each kind includes** (h): all 17 kinds of BRIEF 6.2 plus `image_update`, each in plain words with its code. The update notice is its own checkbox. |
| Money waiting pushes, 09:00-21:00, summary rule | Default quiet hours 21:00 to 09:00 every day, with "Every alert. Only reminders wait." That is exactly today. The summary rule (more than 3 at once) stays in the engine and is stated in the kind's explanation. |
| Update banner and per-version dismiss | "Show a banner when a new CashPilot version is out". The per-browser dismiss stays. `CASHPILOT_UPDATE_CHECK=off` still wins. |
| ntfy, webhook, Telegram, set by environment | **Where pushes go**: Set up / Not set up, the variable name, **Gets**, **Send a test**. Values stay in the environment. |
| No channel configured | (i): "No channel is set up, so no push leaves CashPilot. The bell is the only place alerts show." Each row says "Not set up." with "How to set it up". |
| Activity owner only; `activity_spike` never pushes | **Owner only** chip on the kind. The explanation says the unusual hour never pushes. |
| Per-reminder and per-service mutes in one place | **Muted** in Settings lists reminder mutes, service mutes, box mutes and bell mutes, with who, when, end date and **Unmute**. The add form takes a service or box, what, and how long. The Money waiting foot still manages reminder mutes for writers. |

## The Notifications section

One block, `div.card.settings-section.nt#set-notifications`. It is a CSS size
container, so it lays out by its own width and drops into any Settings
layout. Top to bottom:

1. **Start from**: four preset cards. A preset writes the two checkboxes of
   every kind. It does not touch quiet hours, channels or mutes. **Custom**
   shows when the checkboxes match no preset.

   | Preset | Bell number | Push |
   |---|---|---|
   | Everything (as today) | every kind (reminders have no bell box) | every kind |
   | Only money | Payout questions | Money waiting reminders, Payout questions |
   | Only problems | Collection problems, Earning slowed, Earners and workers, Activity | the same |
   | Nothing | none | none |

2. **Pause**: 1 day, 3 days, 1 week or 30 days, one click. While paused:
   "Paused until Tue 1 Dec, 18:40. Pushes and the bell number come back then.
   [Resume now]". The pause starts at once and needs no Save. With the
   preset **Nothing**, the pause buttons are off and say "Nothing pushes now, so
   there is nothing to pause." (i).
3. **What to tell me about**: six kinds × **Bell number** × **Push** (reminders: Push only), each with
   a real example. **What each kind includes** behind a disclosure. The update
   banner checkbox.
4. **Quiet hours**: switch, from/to, day chips, "still push" choice, "when
   quiet hours end" choice (shown only when something is held), the live
   "Now / Next" line, and **Which problems are urgent**.
5. **Where pushes go**: one row per channel, the redaction note, and the
   **On this browser only** box.
6. **Muted**: the table and the add form.
7. **Save notifications** and a status, as every Settings section does.

Settings is owner only (`app/routers/pages.py:94-101`). The choices apply to
the whole install, like `obligation_state`. Writers keep the Money waiting
foot and the bell's **Mute**.

## Implementation plan

Each step is one PR and ships alone. Steps 1 and 2 need no notification
storage.

### Step 1. Money waiting row (frontend, one small backend field)

- `app/static/js/app.js` `obligationRow` (`:834-887`), `loadMoneyWaiting`
  (`:889-918`), handlers (`:920-945`): the meta line (How, then the rules link
  with `new URL(source).hostname` and `obligationDate(checked)`), the action
  line with fixed cells, the two groups, the phone More, the scope line, the
  folded row after each action with Undo (Mute undo = `unmute`), the muted
  foot as a disclosure. One delegated `keydown` closes an open `.mwx-overflow`
  on Escape. One measure pass sets `--mw-open-w` and `--mw-answer-w`. About
  150 lines.
- `app/static/css/style.css`: the `.mwx-*` rules from the mockup, and the
  container on `.money-waiting`. Replace the 320 px actions column for Money
  waiting rows only. Needs attention keeps its own grid. About 80 lines.
- `app/obligations.py` `muted` (`:458-471`): add `updated_by` and
  `updated_at` from `obligation_state` to each entry, for "sergio,
  12 Nov 2026".
- `app/i18n/en.json`: the `app.obl.*` keys below.
- `docs/reminders.md`: Mute replaces Not for me; describe the rules link.
- `services/bandwidth/honeygain.yml`: the keep-active `how` text says "choose
  Not for me". Change it to "choose Mute this reminder", then the
  `services/_i18n/*.yml` copies.
- Tests: `tests/test_obligations*.py` for the new muted fields.

### Step 2. Undo for Done and Snooze

- `app/database.py` `obligation_state` (`:1040-1052`): add `prev_done_for`,
  `prev_done_at`, `prev_snoozed_until`, written by every `done` and `snooze`.
- `app/routers/obligations.py` (`:99-146`): action `undo` restores the `prev_*`
  values, within 15 minutes of the action, by the same role that may act.
  Audit row `obligation_undo`. 409 when there is nothing to undo.
- Frontend: the folded row's Undo calls it.

### Step 3. Notification settings: storage, API, gate, Settings section

The backend model is in the next section. Files:

- `app/database.py`: table `notification_settings` (one JSON row),
  table `alert_mutes`, table `held_pushes`, migration.
- New `app/notify_prefs.py`: load and validate the settings, `KIND_GROUP`,
  `is_urgent()`, `decide()`, `channels_for()`, quiet-hours maths and the
  "Now / Next" text.
- New `app/routers/notifications.py`: the routes below.
- `app/notify.py` `send` (`:153`): take an optional `targets=` list; add
  `send_one(target, …)` for **Send a test**.
- `app/main.py` `_push_alert` (`:1464-1500`): call the gate first (details
  below). `_run_obligations` (`:10152-10185`): replace `OBLIGATION_PUSH_HOURS`
  (`:10019`) with `notify_prefs.in_quiet_hours(now, "reminders")`.
  `_push_obligation_summary` (`:10186`): pass through the same gate.
- `app/templates/settings.html`: the section and its index link.
- `app/static/js/app.js`: load, presets, Custom pill, pause, quiet-hours
  preview (the server returns the Now/Next text, so the browser does no time
  zone maths), channel rows, Send a test, the mute table. About 200 lines.
- `app/static/css/style.css`: the `.nt-*` rules. About 110 lines.
- `docs/configuration.md` (channels), new `docs/notifications.md`.

### Step 4. The bell

- `app/main.py` `GET /api/collector-alerts` (`:12021-12080`): add per alert
  `counts` (bell number on, not muted) and `muted`, and top-level `state`
  (`on` / `nothing` / `paused`) and `paused_until`.
- `app/static/js/app.js` bell (`:6774-7024`): count only `counts` alerts,
  keep the grey and "?" rules, add the off and paused states, the header
  "Alerts" with a settings link (owner only), **Mute** per entry with the
  folded Undo line, `aria-expanded` and Escape on the bell button (BRIEF
  4.11 says both are missing today).
- Update banner (`app.js:6808-6851`): `GET /api/update-status`
  (`main.py:11965`) returns `banner: false` when the checkbox is off.

### Step 5. Mute end dates and box mutes

- `obligation_state.muted_until`, `alert_mutes.until`. A sweep in the hourly
  job unmutes what has ended. Box mutes match alerts whose subject is a worker.

### Step 6. Pop-up and browser notification (optional, last)

- `app/static/js/app.js`: on each bell poll, alerts with a new id and
  `push: true` raise a toast or `new Notification(...)`, if the user turned
  that on in this browser (`localStorage`). No service worker, as the repo's
  CLAUDE.md asks.

## Backend for notification preferences

### Model

`notification_settings`: one row, household-wide, JSON with a version:

```json
{
  "version": 1,
  "kinds": {
    "reminders":  {"push": true},
    "payouts":    {"badge": true,  "push": true},
    "collection": {"badge": true,  "push": true},
    "slowed":     {"badge": true,  "push": true},
    "fleet":      {"badge": true,  "push": true},
    "activity":   {"badge": true,  "push": true}
  },
  "update_banner": true,
  "paused_until": null,
  "quiet": {"on": true, "from": "21:00", "to": "09:00", "days": [0,1,2,3,4,5,6],
            "let_through": "alerts", "on_end": "summary"},
  "channels": {"ntfy": "all", "telegram": "all", "webhook": "all"}
}
```

`let_through` is `alerts` (only reminders wait: today), `urgent` or `none`.
`on_end` is `summary` or `drop`. A channel value is `all`, `urgent`, `money`
or `off`. A missing row means the defaults above, so an upgrade changes
nothing. The preset is not stored. The browser works it out from `kinds`.

`alert_mutes(id, subject_type 'service'|'worker', subject, grp NULL=every
group, muted_by, muted_at, until NULL)`. Reminder mutes stay in
`obligation_state.muted`. Settings lists both.

`held_pushes(id, kind, subject, title, message, created_at)`: pushes held by
quiet hours.

`KIND_GROUP` (in `notify_prefs.py`):

| Group | Kinds |
|---|---|
| reminders | `obligation` |
| payouts | `payout` |
| collection | `collector`, `notice`, `account_disabled`, credential forecast (bell only: its push is an `obligation` credential reminder, so the reminders group's `push` controls it; the Settings text says so) |
| slowed | `flatline`, `stall` |
| fleet | `container`, `missing`, `proxied`, `proxy_cap`, `docker`, `worker`, `image_update` |
| activity | `activity_mail`, `activity_lan`, `activity_spike` |

`is_urgent(kind, category, stage)`: `collector` with category `auth`,
`account_disabled`, `container`, `missing`, `worker`, `docker`, `proxied`,
`image_update` with result `restore_failed`, and an `obligation` at stage
`overdue`. Everything else is not urgent.

### API

| Route | Role | Does |
|---|---|---|
| `GET /api/notifications` | owner | Settings, channel status (`configured: true/false`, never the value), the Now/Next quiet text, and every mute (reminder and alert) with who, when and end. |
| `PUT /api/notifications` | owner | Validate and save. Audit `notifications_saved`. |
| `POST /api/notifications/pause` `{days: 1\|3\|7\|30}` / `DELETE` | owner | Set or clear `paused_until`. |
| `POST /api/notifications/test/{channel}` | owner | One test message to that channel only. 400 when it is not set up. |
| `POST /api/notifications/mutes` `{subject_type, subject, what, until}` | owner | Add a service or box mute from Settings. `what` = reminders and alerts / reminders only / alerts only. Reminders go to `obligation_state` (rule `*`). |
| `DELETE /api/notifications/mutes/{id}` | owner | Unmute an alert mute. Reminder mutes keep using `POST /api/obligations/{slug}/{rule}` `unmute`. |
| `POST /api/collector-alerts/mute` `{subject, kind}` / `DELETE` | writer and up | The bell's **Mute** and its Undo. Stores the alert's group for that subject. Writer, because writers may already mute reminders. |
| `POST /api/obligations/{slug}/{rule}` | as today | New action `undo` (step 2). `mute` takes an optional `until` (step 5). |

### Where each alert source checks the preferences

Every push already goes through one function, `_push_alert`
(`main.py:1464`), called from the container (`:685`), account disabled
(`:835`), missing (`:945`), proxied (`:1161`), stall (`:1328`), docker
(`:1405`), payout (`:1574`), flatline (`:1775`), notice (`:2066`, `:2341`),
collector (`:2306`), worker (`:3152`), proxy cap (`:9499`), obligation
(`:10183`) and activity (`:13409`) sites. So the gate lives in one place:

1. At the top of `_push_alert`: `decision = notify_prefs.decide(kind,
   subject, category=…, urgent=…)`. It checks, in order: paused, the kind's
   `push`, `alert_mutes` (and reminder mutes for `obligation`), then quiet
   hours with `let_through`.
2. `drop`: return at once. **Do not delete the alert row.** Today a push that
   reaches no channel deletes its dedupe row so the next cycle retries
   (`main.py:1488-1505`). A push dropped on purpose must keep its row, or
   every collection cycle would try it again.
3. `hold`: insert into `held_pushes` and return. The row stays.
4. `send`: `notify.send(…, targets=notify_prefs.channels_for(kind,
   urgent))`. A channel set to `urgent` gets only urgent pushes; `money` gets
   only the reminders and payouts groups; `off` gets nothing. If the list is
   empty, treat it as `drop`, not as a failed delivery.
5. `_push_obligation_summary` (`main.py:10186`) calls `notify.send` directly.
   It goes through the same gate with kind `obligation`.
6. `_run_obligations`: the hour check (`:10166-10168`) becomes
   `notify_prefs.in_quiet_hours(now)`. Reminders are worked out again every
   hour, so they wait without the held queue. That is why "Every alert. Only
   reminders wait." reproduces today exactly.
7. A job every 5 minutes: when quiet hours have ended, send the held pushes
   as one summary (`on_end: summary`) or delete them (`drop`).
8. The bell does not push. `GET /api/collector-alerts` adds `counts` from the
   kind's `badge` and the mutes. The list itself is never filtered.
9. `activity_spike` already never pushes (BRIEF 6.2). The gate does not
   change that.
10. The update banner reads `banner` from `/api/update-status`.

Tests: one table test for `decide()` (every kind × paused × kind off × muted ×
quiet × let_through), one for `channels_for()`, one that a dropped push keeps
its alert row, one that held pushes flush as one summary, and one that the
missing row gives today's behaviour.

## i18n

New English keys, then the 19 locales:

- Money waiting: `app.obl.mute` "Mute", `app.obl.mute_this` "This reminder",
  `app.obl.mute_all_short` "All {name}", `app.obl.mute_this_long` "Mute this
  reminder", `app.obl.snooze` "Snooze", `app.obl.snooze_1d` "1 day",
  `app.obl.snooze_7d` "1 week", `app.obl.too_close` "Too close to snooze", `app.obl.too_late` "Too late to snooze",
  `app.obl.scope` "Done, Snooze and Mute apply to everyone who uses this
  CashPilot.", `app.obl.rules.claim` "Claim rules on {host}",
  `app.obl.rules.withdraw` "Payout rules on {host}",
  `app.obl.rules.keep_active` "Inactivity rules on {host}",
  `app.obl.rules.renew` "Renewal rules on {host}", `app.obl.rules.act` "Rules
  on {host}", `app.obl.checked` "{rules}, checked {date}", `app.obl.new_tab`
  "(opens in a new tab)", `app.obl.undo` "Undo", the folded lines
  (`app.obl.fold.done`, `.requested`, `.arrived`, `.snoozed`, `.muted`,
  `.muted_all`, `.unmuted`), `app.obl.mute_again` "Mute again", `app.obl.muted_count` "Muted reminders ({n})",
  `app.obl.muted_by` "{user}, {date}", `app.obl.until_unmute` "until
  unmuted", `app.obl.until` "until {date}", `app.obl.muted_help`,
  `app.obl.menu_hint`, `app.obl.no_push` "Reminders do not push: notifications are set to Nothing. …", `app.obl.no_push_paused` "Reminders do not push until {date}: notifications are paused. …",
  `app.obl.settings_link` "Notification settings".
- Kept: `app.obl.mute_all` (aria-label and phone menu), `app.obl.snooze_day`,
  `app.obl.snooze_week`, `app.obl.unmute`, `app.obl.more`, `app.obl.how`.
- No longer used: `app.obl.not_for_me`, `app.obl.source`,
  `app.obl.source_checked`, `app.obl.muted`, `app.obl.muted_list`.
- Bell: `base.alerts` and `base.alerts.header` become "Alerts";
  `app.bell.mute` "Mute", `app.bell.muted_line`, `app.bell.state_off`,
  `app.bell.state_paused` "Paused until {date}", `app.bell.settings`.
- Settings: about 60 keys under `settings.notify.*` (title, description,
  four presets with their summaries, Custom, pause, six kinds with examples
  and explanations, update banner, quiet hours and its choices, the Now/Next
  text, urgent definition, channels and their states, the browser box, the
  mute table and add form, the save statuses that say when a change works: "A preset ticks the boxes below. Nothing changes until you save.", "It starts at once. It does not need Save.", "Mute and Unmute here work at once.", "Not saved yet. Your changes work from the moment you save.", "Saved at {time}. In effect now.", the pause-off text, the test-sent line, and `app.bell.state_nothing`).
- Server-side texts: the API errors (`api.nothing_to_undo`,
  `api.channel_not_set_up`), the test push text, and the held-pushes summary
  title.

## Open PRs that touch the same files

None of them touches `app/templates/dashboard.html`,
`app/templates/settings.html`, `app/obligations.py`,
`app/routers/obligations.py` or `app/notify.py`. The overlaps are in the
big shared files:

| PR | Touches | Effect on this work |
|---|---|---|
| #946 floating image updates | `app.js` (bell renderer), `main.py`, `database.py`, `en.json`, `style.css` | Adds the `image_update` alert kind and a bell branch. Build step 4 (bell) after it merges. Add `image_update` to `KIND_GROUP` and `is_urgent`. |
| #940 proxies for Bitping, Mysterium, URnetwork | `honeygain.yml`, `app.js`, `main.py`, `database.py`, `en.json` | Edits `honeygain.yml`. Change the "choose Not for me" text after it merges. |
| #933 Secure VM from the Fleet page | `services/_i18n/*.yml`, `app.js`, `style.css`, `main.py`, `en.json` | Same `_i18n` files as the Honeygain text change. Merge first. |
| #947 layers per earner, gVisor per earner | `services/_i18n/*.yml`, `app.js`, `style.css`, `main.py`, `en.json` | Same as #933. |
| #895 gVisor from the Fleet page | `base.html`, `routers/pages.py`, `docs/configuration.md`, `app.js`, `style.css`, `main.py`, `database.py`, `en.json` | `base.html` holds the bell markup; `docs/configuration.md` holds the channel docs. Rebase step 3 and 4 on it. |
| #949 web UI in 19 more languages | `app/i18n/*.json` (the locales) | Every new key above must reach these files. Add our keys after it merges, so the locale check passes. |

The `design/settings-page` lane owns the Settings layout. This section is
self-contained and assumes no column, index or card around it.

## Sample data, adjusted to the code

- Honeygain shows 20.76 USD. A cash-out row appears only at or above the
  provider minimum, which is $20 for Honeygain (BRIEF section 8).
- PacketStream, EarnFM and Storj rules are samples. Only Honeygain, Repocket,
  Bitping, MystNodes, Salad and Grass have catalog rules.
- The Storj recheck comes 14 days after Requested (`obligations.py:47`).

## Adversarial check (2026-11-28)

A second pass went through BRIEF.md section 9 item by item, and through the
lane's own checks, against `index.html` and the shots. A script on the MacMini
also measured every width: horizontal overflow, action lines that wrap, and the
contrast of every text node on its real background. Gaps found, all fixed in
this folder:

| Gap | Fix |
|---|---|
| The weekdays were wrong. 28 Nov 2026 is a Saturday, not a Friday. 1 Dec is a Tuesday, 29 Nov a Sunday. The (h) "next quiet time" therefore named the wrong night. | Every date fixed. (h) now reads "Sun 29 Nov, 22:30 to Mon 30 Nov, 07:30. Tonight is not quiet, because Sat is off." |
| No Overdue row was drawn: no red level, no written-off line, no "days ago". | (e) adds a Bitping overdue row from its real catalog rule, with "Too late to snooze". |
| Settings never said when a change takes effect. | Presets: "Nothing changes until you save." Pause: "It starts at once. It does not need Save." Mutes: "work at once". Save status: not saved, saved at a time, in effect now. Send a test reports "Test sent at 10:44" beside the channel, and the button keeps its label. |
| (i) drew a pause running on top of the preset Nothing, and said "your other choices come back then", which made no sense. | (i) now shows two states. A pause on top of Everything, with no channel, just after a save. And Nothing, where the pause buttons are off and say why. Money waiting shows the line for each. |
| Money waiting reminders had a **Bell number** box, but reminders never appear in the bell list. Ticked, the badge would count entries the list does not show. (h) also ticked it while its label said only two kinds changed. | The cell says **Dashboard**. The model drops `badge` for reminders. |
| Credential forecasts sat under Collection problems, but they push as Money waiting credential reminders. Unticking Collection Push would not stop them. | The Collection explanation says so, and `KIND_GROUP` in this file records it. |
| Unmute had no way back. | The Unmute line stays with **Mute again** until the next reload (d). |
| The bell's empty texts and its paused and Nothing list states were claimed, not drawn. The `.notify-state` style existed but nothing used it. | (f) draws the list while paused (state line, "All collectors healthy") and with the preset Nothing, and quotes the other empty texts. |
| The snooze buttons' screen-reader names ("Snooze a day") did not contain their visible words ("1 day"). A voice user saying "click 1 day" would miss. | The names are now "Snooze 1 day" and "Snooze 1 week". |
| Phone panel (b) drew only the no-snooze menu open, and its closed menus held one item each. | Honeygain's menu is drawn open with all four actions. Every closed menu holds its real items. |
| (c) counted 2 open rows while only 1 was open. The MystNodes folded line put its two buttons on a second line at 900 px. | Count 1. The folded text is shorter ("No more reminders or pushes for this claim.") and fits on one line at 900. |
| (i) put Money waiting in a half-width column, so at 1440 its Mute group fell to a second line. | Money waiting in (i) is full width, as on the Dashboard. |
| "(≈ $15.32)" broke after "(≈" at 390 and 1440. | The converted amount never breaks. |
| The viewer's muted list dropped the Repocket end date. "until you unmute it" spoke to a person who may not be allowed to. | The end date is back. The text is "until unmuted" everywhere, and Settings says "Until unmuted". |
| (a) was labelled "owner or writer" but drew the owner-only "Notification settings" link. | The label says a writer sees the same view without the link. |
| Disabled pause buttons would use the stock 0.4 opacity, about 3.6:1. | Disabled pause buttons use the muted text colour and a dashed border, 7.5:1. |

Checked and found sound: every action is on one line at 1440 and 900 (script
count: 0 wrapped action lines; only the folded status lines wrap, at 390).
There is no horizontal overflow at 390, 900 or 1440. No text is below 4.5:1
(muted `#a59cb5` on `#0b0b14` is 7.5:1). The focus order follows the reading
order: head link, How, rules link, Open, answer, Snooze, Mute, More. Every
source in BRIEF.md 6.1 and 6.2 has a control or an explicit "always shown"
statement.

The lane scope asked for "a minimum severity". This design has no separate
level control on purpose: the kinds already carry the meaning, and a level
would be a third filter layer. "Urgent" covers the two places where a level
matters: quiet hours ("Urgent problems only") and each channel ("Gets: Urgent
only"). Setting every channel to Urgent only is the install-wide minimum.

## Seen on the way, not in scope

At 900 px the real top bar lets **+ Add service** cover the "Settings" tab
(visible in `shot-900.png`). That belongs to the top bar, not this lane.
