# Design 3: Row opens detail

A closed row shows only what you need to act: the tag, the service, the task,
the date, and three controls. The controls are **Open {name}**, the row's
**Done** button, and **Details**. When you select the row, it opens in place.
The open row shows what to do, what you can lose, and the provider's rule with
the date we last checked it. It also shows every other action, on one line.

The Notifications section in Settings sorts every alert by what it is about:
**Money**, **Machines** and **App**. Each group has one level (Off, Bell only,
Bell and push) and its own quiet hours. You can override the level of each
kind inside a group.

Files: `index.html` (the mockup), `shot-1440.png`, `shot-900.png`,
`shot-390.png`.

## 1. What changed versus today, and why

| Today | This design | Why |
|---|---|---|
| Up to four buttons and a **More** menu share a 320 px cell, so they wrap onto two or three lines (`style.css:1453-1458`). | A closed row has three controls that never wrap: Open {name}, Done (or Requested, or It arrived), Details. | One line on a desktop, the same three controls in every row, so the columns line up. |
| Snooze a week, Not for me, Mute all and Source hide in **More**. | They sit in the open row, on one line: Remind me tomorrow · Remind me in a week │ Mute this reminder · Mute all {name} reminders. | Nothing is hidden behind a second menu on a desktop. The row is the menu. |
| **Source, checked 2026-11-24** is a button with no hint of what it opens. The date is the raw ISO string. | Under the heading **The rule**: "MystNodes states this rule on its own help site." Then the link "Read the rule on help.mystnodes.com ↗". Then "We last checked it on 24 Nov 2026". | The label says what the page is, and the domain shows that the link goes to the provider and not to a fake claim site. The date is a formatted calendar day. |
| **Not for me** does not say what it does. | **Mute this reminder**, with one line below: "Mute stops a reminder and its pushes, for everyone here. You can unmute it at the foot of this list." | Plain verb. It is the same word as **Mute all {name} reminders** and the Muted list in Settings. |
| The loss text and the How disclosure stretch every row to three or four lines. | The closed row shows the title and the date. The open row shows the loss text and the How text. The overdue and recheck lines stay on the closed row, because they ask for an answer. | Five reminders fit on one screen. The explanation is one select away. |
| The muted foot is a run-on line: "Not for me: Honeygain, Keep a … Unmute · Repocket, …". | A disclosure: "2 muted reminders". It opens a list with one line for each mute: service, reminder, when, who, **Unmute**. Then a link: "See every mute in Settings, Notifications". | It reads as a list. The date and the name of the person who muted it come from `obligation_state` (`updated_at`, `updated_by`), which already exists. |
| A mute gives only a toast. | The row folds into one line in the same place: "PacketStream: '…' is muted. No more reminders or pushes about it." with **Undo**. The toast says the same. | You see what you muted, and you can undo it there. Undo calls the unmute route that exists today. |
| Notifications cannot be configured. | One Settings section: an on/off switch, pause, three groups with levels and quiet hours, a level for each kind, a minimum urgency for pushes, channels with which groups each one gets, and one list of every mute. | Section 3. |

## 2. How each problem in the brief is solved

- **Actions wrap and hide in More on a desktop.** The closed row has three
  controls. The open row has four more, on one line. Both lines use
  `flex-wrap: nowrap` at 1440 and 900 px. The action line has `wrap` only as a
  fallback for a very long translation. The 1440 and 900 shots show every row on
  one line. The More menu is gone.
- **Collapse only on phones.** At 560 px of row width and below (container
  query, so it also works inside narrow panels), the row takes three lines.
  Details moves to the top right. In the open row, the four other actions become
  a stacked list of full-width, 34 px tall buttons. That list is the phone menu.
- **"Source" says nothing.** Now it is "Read the rule on {domain}" under **The
  rule**, with "We last checked it on {date}". Viewers see the same link and
  date. Today they see a bare "Source" with no date.
- **"Not for me" is unclear.** Now it is **Mute this reminder**, with a one-line
  meaning under the buttons. **Mute all {name} reminders** keeps its label.
- **Notifications cannot be configured.** Section 3.

### Where this departs from the direction, and why

- The direction says "Stop reminding me about this". I used **Mute this
  reminder**. Reason: the app already has "Mute all {name} reminders", the API
  action is `mute`, and the Settings list needs one word for reminders and
  services together. "Stop" on the row with "Muted" in Settings would be two
  words for one thing. If you prefer "Stop reminding me about this", it is one
  key to change.
- The direction says the closed row shows "the one primary action". I kept
  **Done** (or Requested, or It arrived) beside **Open {name}** on the closed
  row. Done is what you press right after you come back from the provider.
  Hiding it behind Details would add a click to the most common path. The closed
  row still never goes past three controls.

## 3. The Notifications section

One `section.card.settings-section#set-notifications`. It uses no layout class
outside itself, so the `design/settings-page` lane can place it anywhere.
Settings is owner only today (`pages.py:94-101`), so this section is owner only.
Every choice applies to the whole household, because pushes go to shared
channels and the Money waiting state is already shared (`obligation_state`).

### 3.1 Parts, top to bottom

1. **Master row.** "Notifications are on" with an On/Off switch, and "Pause
   pushes for [1 day | 3 days | 1 week | 2 weeks] [Pause]". A pause shows
   "Paused until {date} {time}" with **Resume now**.
2. **What to tell you.** Three groups:
   - **Money**: cash out ready, deadlines (claim, keep active, withdraw,
     overdue), "Did the payout arrive?", "Was this a payout?" (`payout`).
   - **Machines**: worker offline, Docker unreachable, earner stopped or missing
     (`container`, `missing`), proxy problem (`proxied`, `proxy_cap`), low
     traffic (`stall`), account disabled, collector alerts (`collector`),
     collection notes (`notice`), balance gone quiet (`flatline`), login about
     to expire (credential forecast), earner sent mail or reached your network
     (`activity_mail`, `activity_lan`, owner only), unusual hour of traffic
     (`activity_spike`, owner only, its push choice is disabled because it never
     pushes).
   - **App**: new CashPilot version. Here "Bell" means the update banner. The
     per-version dismiss on the banner stays. If `CASHPILOT_UPDATE_CHECK=off`,
     this group says so and is disabled.

   Each group has a level: **Off**, **Bell only**, **Bell and push**. "Choose
   kinds (n)" opens one row per kind with the same three choices. When kinds
   differ, the group shows "mixed". Each group has "Quiet hours" with **Change**.
   That opens From, To, the days of the week, the time zone, and (for Machines)
   "Urgent ones still come through".
3. **How urgent before a push.** "Push only when it is at least: Info | Warning
   | Urgent". A disclosure explains each level. The bell still counts all kinds
   that are on.
4. **Where pushes go.** One row per channel that the code has: Telegram, ntfy,
   Webhook. Each row shows Set or Not set and the variable name, "Gets: Money,
   Machines, App" check boxes, and **Send a test**. With no channel set: "No push
   channel is set. Alerts show only in the bell and on the Dashboard."
5. **Muted.** One table of every mute: reminder mutes (from Money waiting) and
   service mutes (new). Each row: service, what is muted, the date and who
   muted it, **Unmute**. Under it: "Mute a service: [service] [Machines alerts |
   Money reminders | Everything] [Mute]". Filter: All, Reminders, Services.
6. **Save notifications**, with a status line, as in every Settings section.

### 3.2 What Off means

**Off** stops the badge, the update banner and every push. It does not hide
facts. The Dashboard still lists Money waiting and Needs attention, and the bell
still opens to the list, with a line on top: "Notifications are off. The bell
shows no count, but this list still shows what is wrong. Turn them on". The bell
icon is crossed out. Money waiting shows "Notifications are off: no pushes go
out. Settings" in its head. Reason: the app's rule is that a failure is never
shown as an all-clear. Hiding the list itself would break that rule. The "?"
badge (server unreachable) still shows when off, because it says the page
itself is broken.

### 3.3 Defaults (panel e) keep today's behaviour

- Money: Bell and push, quiet hours 21:00–09:00 every day. That is today's
  fixed 09:00–21:00 push window (`main.py:10019`), now visible and changeable.
  One change: Money reminders also count on the bell when the level is Bell
  only or Bell and push. Today they never reach the bell.
- Machines: Bell and push, no quiet hours (as today).
- App: Bell only, which is the banner (as today: the update never pushes).
- Minimum urgency: Info (everything pushes, as today).
- Every channel gets every group (as today).
- The "more than 3 at once become one summary" rule stays. The Money kinds list
  says so.

### 3.4 Urgency, defined (there is no severity field today)

| Level | Kinds |
|---|---|
| Urgent | Overdue reminders, `account_disabled`, `worker`, `collector` with category `auth` |
| Warning | Reminders with 7 days or fewer left, "Did the payout arrive?", `container`, `missing`, `docker`, `proxied`, `proxy_cap`, `stall`, `flatline`, `collector` (other categories), `activity_mail`, `activity_lan` |
| Info | Cash out ready, `payout`, `notice`, credential forecast, update available |

This table lives in one place in the code (a dict next to `_push_alert`).

## 4. Checklist against BRIEF.md section 9

Money waiting, per row:

- [x] Tag and level colour: closed row, left border and tag colour unchanged.
- [x] Service name: closed row.
- [x] Title, with balance and "≈": closed row (Storj sample shows "≈ $9.15").
- [x] Due date, "or earlier", days left / today / days ago: closed row (EarnFM
  "or earlier", Bitping "3 days ago").
- [x] Overdue line and recheck line: closed row, in the level colour.
- [x] Loss text: open row, "What you can lose".
- [x] How text: open row, "What to do". It is no longer a nested disclosure.
- [x] Open {name}: closed row, primary, new tab.
- [x] Done / Requested / It arrived: closed row.
- [x] Snooze a day: open row, "Remind me tomorrow".
- [x] Snooze a week: open row, "Remind me in a week".
- [x] Not for me: open row, "Mute this reminder".
- [x] Mute all {name} reminders: open row, same label.
- [x] Source link and checked date: open row, "The rule". Writers and viewers
  both get the date now.
- [x] Viewer variant: panel (b), middle frame. Open {name} and Details. The open
  row has the facts and the rule, no write actions, and one line: "You can read
  reminders. The owner or a writer marks them done, snoozes or mutes them."
- [x] Snooze hidden when `can_snooze` is false: panel (b), right frame. The
  snooze buttons give way to "Too close to its deadline to snooze."

Money waiting, panel:

- [x] Title and count: unchanged.
- [x] Muted list with Unmute per entry: the foot disclosure (panels a, d), and
  Settings, Muted (panels d, f).
- [x] Hidden when empty; foot only when only mutes exist: unchanged logic.
- [x] "Could not check" row: panel (b), right frame. Same texts, no actions,
  never an all-clear.
- [x] Toasts after each action: kept. The mute toast has new text (panel c).

Notifications:

- [x] Bell, badge states (count, grey, "?"), empty texts: panel (g), "The bell
  badge in every state", plus the crossed bell when off or paused. The empty
  texts are unchanged.
- [x] Every alert kind in section 6.2, by name: section 3.1 above. Panel (f)
  lists every Machines kind.
- [x] Money waiting pushes, 09:00–21:00, summary rule: default Money quiet hours
  21:00–09:00, and the summary line in the Money kinds list.
- [x] Update banner and per-version dismiss: App group. The dismiss on the banner
  stays.
- [x] The three channels, set by environment: Where pushes go, with the variable
  names.
- [x] No channel configured: panel (e), the warning line.
- [x] Activity alerts owner only; `activity_spike` never pushes: "owner only"
  marks, and the disabled push choice on the spike row.
- [x] Per-reminder and per-service mutes in one place, and on the row: Settings,
  Muted, plus the row and the foot.

## 5. Implementation cost

Rough lines, added or changed.

| Part | Work | Lines |
|---|---|---|
| `dashboard.html` | Foot becomes a `<details>`. A head note slot. | ~10 |
| `app.js` Money waiting | `obligationRow` builds the closed line and the detail. A row toggle: click on the line, Enter or Space on Details, Escape closes, `aria-expanded`. The undo line after a mute. The foot list. Format `checked` with `obligationDate`. | ~120 |
| `style.css` Money waiting | `rd-*` rules: the grid, the detail, the container queries at 1000 and 560 px. Remove `.mw-more`, `.mw-menu`. | ~70 |
| API, Money waiting | `GET /api/obligations` `muted[]` gains `muted_at` and `muted_by` from `obligation_state.updated_at` / `updated_by`. A `source_host` field, or derive the host in JS. | ~15 |
| `settings.html` + `app.js` Notifications | The section, load and save, the segmented controls, quiet hours editor, channel status, test button, mute table. | ~350 |
| `style.css` Notifications | `nt-*` rules. | ~120 |
| Backend, Notifications | A `notification_settings` row (one JSON blob for the household) and a `notification_mutes` table (slug, scope, by, at). `GET/POST /api/notifications` (owner). `GET /api/notifications/channels` (which env vars are set, never their values). `POST /api/notifications/test`. A gate in `_push_alert` and the obligation push job: master switch, pause, group and kind level, minimum urgency, quiet hours (hold and release as one summary), per-channel groups, service mutes. The bell endpoint filters by kind level and service mute, and returns `off: true` for the crossed bell. The update banner reads the App level. | ~400 |
| `app/notify.py` | `send()` takes the group and skips channels that do not get it. | ~25 |
| Tests | Gate decisions (quiet hours across midnight, pause, urgent pass-through, mutes, off), API auth, channel status without secret values. | ~300 |
| Docs | `docs/reminders.md` (new labels, foot, undo), `docs/configuration.md` and `docs/fleet.md` (Notifications section). | ~80 |

Total: about 1,500 lines. The Money waiting half alone is about 215 lines and
needs one small API field. It can ship first, without the Notifications half.

Catalog: `services/bandwidth/honeygain.yml` `keep-active-6-months` `how` says
"choose Not for me". It must say "choose Mute this reminder", and its
translations in `services/_i18n` too. CashPilot-Desktop vendors `services/`, so
it needs a catalog sync after that change.

## 6. What it needs from i18n

New keys (English text). All need the 19 locales.

| Key | Text |
|---|---|
| `app.obl.details` | Details |
| `app.obl.what_to_do` | What to do |
| `app.obl.what_you_lose` | What you can lose |
| `app.obl.rule` | The rule |
| `app.obl.rule_where` | {name} states this rule on its own site. |
| `app.obl.rule_link` | Read the rule on {host} |
| `app.obl.rule_checked` | We last checked it on {date} |
| `app.obl.remind_tomorrow` | Remind me tomorrow |
| `app.obl.remind_week` | Remind me in a week |
| `app.obl.mute_this` | Mute this reminder |
| `app.obl.mute_hint` | Mute stops a reminder and its pushes, for everyone here. You can unmute it at the foot of this list. |
| `app.obl.no_snooze` | Too close to its deadline to snooze. |
| `app.obl.viewer_hint` | You can read reminders. The owner or a writer marks them done, snoozes or mutes them. |
| `app.obl.select_hint` | Select a row to see what to do and the provider's rule. |
| `app.obl.just_muted` | {name}: "{title}" is muted. No more reminders or pushes about it. |
| `app.obl.undo` | Undo |
| `app.obl.muted_count` | {n, plural, one {# muted reminder} other {# muted reminders}} |
| `app.obl.muted_when` | muted {date} by {user} |
| `app.obl.see_all_mutes` | See every mute in Settings, Notifications |
| `app.obl.off_note` | Notifications are off: no pushes go out. |
| `app.bell.off` | Notifications are off. The bell shows no count, but this list still shows what is wrong. |
| `app.bell.turn_on` / `app.bell.settings` | Turn them on / Notification settings |
| `settings.notify.*` | About 70 keys: the section title and description, master row, pause lengths, three group names and descriptions, three levels, 17 kind names and descriptions, quiet hours labels and the 7 day names, urgency labels and their three explanations, channel labels and states, the no-channel warning, the Muted block, save and status texts. |

Changed text, same key:

| Key | Old | New |
|---|---|---|
| `app.obl.muted` (toast) | Muted. Unmute it at the foot of Money waiting. | Reminder muted. Undo it here, or unmute it at the foot of this list. |

Keys that go away: `app.obl.more`, `app.obl.not_for_me`, `app.obl.source`,
`app.obl.source_checked`, `app.obl.how`, `app.obl.snooze_day`,
`app.obl.snooze_week`, `app.obl.muted_list`. The toasts `app.obl.snoozed_day`
and `app.obl.snoozed_week` stay.

## 7. Accessibility

- The row line is clickable for the mouse. The keyboard path is the **Details**
  button: a real `<button>` with `aria-expanded` and `aria-controls`. Escape
  closes an open row and returns focus to Details. Links and buttons inside the
  line do not toggle the row.
- On phones, Details is the same button in a second slot. Only one of the two is
  visible at a time.
- Segmented controls are native radio groups (`role="radiogroup"`, one name per
  group). The focus ring is the cyan `--accent-secondary`, drawn on the label.
- Muted text is `--text-muted` `#a59cb5` on `#0b0b14` and `#11111d`, which the
  classic theme lists at 4.5:1 or more. Disabled state in panel (g) dims the
  whole block and sets `aria-disabled`. The live app should use `disabled` on
  the fieldset.
- The undo line has `role="status"`, so a screen reader announces it.

## 8. Sample data I changed to match the code

- Honeygain cash out: 20.62 USD, not 18.76. At 18.76 the code shows no row,
  because Honeygain's minimum is $20. (The live code would show the Honeygain
  withdraw rule instead of the generic cash-out row.)
- Storj: shown at the "Arrived?" stage with the balance in STORJ, so the "≈"
  conversion appears. The code asks 14 days after Requested, so the text says
  "two weeks ago".
- Panel (b) adds Bitping at the Overdue stage, to show the red level, the
  written-off line and the no-snooze state.

## 9. Questions for you

1. **Mute** or **Stop reminding me**? Section 2 explains why I picked Mute.
2. Should **Off** also hide the Money waiting panel? I say no (section 3.2).
3. Channels stay in environment variables in this design, with status only.
   Entering them in the UI (stored encrypted, like earner credentials) is a
   possible next step. It is not drawn here.
