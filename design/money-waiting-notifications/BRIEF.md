# Brief: Money waiting actions, and a Notifications section in Settings

Every designer in this lane works from this file. It states what exists today,
from the code at `origin/main` `aa543a48`. It holds no design opinions. Every
claim cites `file:line`. Paths are relative to the worktree root
(`/Users/sergio/repos/personal/CashPilot-wt-design-notify`).

This lane is a design proposal. Never edit `app/`. Write only under
`design/money-waiting-notifications/`.

## 1. The problem, in our words

**Money waiting rows.** Each reminder row has a primary link and up to two
buttons. The other actions sit in a **More** menu, even on a wide desktop.
The buttons wrap and do not line up. On a desktop, every action should sit on
one line. Only at phone widths (about 390 px) may they collapse into a menu.

**Two labels say nothing about what they do.**

- **Source** gives no hint of what it opens. It opens the provider's own page
  that states the payout or expiry rule. The row also knows the date we last
  read that page.
- **Not for me** is unclear. It mutes this one reminder rule, for this one
  service, for the whole household.

**Notifications.** The user cannot configure them at all. There is no way to
say "no warnings from this app", "only payouts", or "not at night". The
channels exist only as environment variables (section 6.3).

## 2. Hard constraints for every design

- Dark theme. Mockups use the default theme, `data-theme="classic"` (pink
  primary buttons, section 3).
- Every action and every piece of information that exists today stays
  reachable somewhere. Section 9 is the checklist.
- Plain English in ASD-STE style: short sentences, one idea each. Define a term
  the first time you use it.
- Long explanations go behind a disclosure or a "Learn more" link. Never a wall
  of text on the main view.
- All labels are real text, so they can be translated (19 locales besides
  English). No text inside images.
- Every control is keyboard reachable, with a visible focus ring.
- Muted text has a contrast of at least 4.5:1 on its background.
- On a desktop (1440 and 900 px), the actions of one Money waiting row sit on
  one line. At 390 px they may collapse into a menu.
- The Notifications section is one self-contained section. It must drop into
  any Settings layout, because a parallel lane (`design/settings-page`) owns the
  Settings layout. Show it inside a plain Settings frame (section 7).

## 3. Mockup setup and rendering

### Theme and styles

- Put `data-theme="classic"` on `<html>`. `app/themes.json` names `classic` as
  the default theme. Without the attribute, the page gets the grey `:root`
  theme with white primary buttons (`app/static/css/style.css:13-80`,
  `:1660`).
- The classic tokens are at `app/static/css/style.css:2294-2307`: background
  `#0b0b14`, card `#11111d`, text `#e8e6f0` / `#bdb6cf` / `#a59cb5` (muted),
  accent pink `#f472b6`, focus cyan `#22d3ee` (`:2334-2335`). The status
  colours come from `:root`: success `#46b37f`, warning `#e0a53c`, error
  `#f06a5f` (`:38-45`).
- Fonts: IBM Plex Sans for the UI, IBM Plex Mono for figures and dates
  (`:63-64`, loaded from Google Fonts in `app/templates/base.html:15`). Font
  sizes `--fs-1` 14 px to `--fs-5` 23 px (`:67-73`). Radius 2 px (`:77`).
- Classes to reuse:
  - Rows: `.attn-list`, `.attn-row` with `.attn-fail`, `.attn-warn`,
    `.attn-ask` or `.attn-unknown`, `.attn-tag`, `.attn-what`, `.attn-why`,
    `.attn-actions`, `.attn-foot` (`:1449-1478`).
  - Money waiting: `.money-waiting`, `.mw-why`, `.mw-title`, `.mw-when`,
    `.mw-loss`, `.mw-how`, `.mw-more`, `.mw-menu` (`:1481-1496`).
  - Section heads: `.block-head`, `.block-title`, `.count` (`:1398-1403`).
  - Buttons: `.btn` plus `.btn-primary`, `.btn-secondary`, `.btn-ghost`,
    `.btn-link`, `.btn-sm` (`:1658-1670`).
  - Forms: `.form-label`, `.form-input`, `.form-input-sm` (`:1674-1688`).
    Checkboxes take the accent colour (`:1689`).
  - Tabs: `.tab-strip`, `.tab-btn`, `.tab-btn.active` (`:1560-1564`).
  - Settings: `.settings-layout`, `.settings-index`, `.settings-body`,
    `.card.settings-section`, `.settings-section-title`,
    `.settings-section-desc`, `.settings-actions` (`:1871-1880`).
  - Bell: `.notify-badge`, `.notify-dropdown`, `.notify-item` and its children
    (`:299-400`). Toasts: `.toast-container`, `.toast.success|error|warning|info`
    (`:873-905`). Update banner: `.update-banner` (`:1242-1290`).
- Add your own `<style>` only for the parts that are new.

### Where each mockup goes

One folder per design: `design/money-waiting-notifications/<sub>/index.html`.
From there, the stylesheet is at `../../../app/static/css/style.css`.

### Rendering (never on the MacBook)

The stock command in the lane task copies `app/static` to `wt/static` on the
MacMini, which breaks the `../../../app/static/...` path. Copy it to
`wt/app/static` instead, so the same relative link works on both machines:

```sh
SUB=<sub>
ssh MacMini 'mkdir -p /Volumes/Data/scratch/design-notify/wt/app'
rsync -a /Users/sergio/repos/personal/CashPilot-wt-design-notify/app/static MacMini:/Volumes/Data/scratch/design-notify/wt/app/
rsync -a /Users/sergio/repos/personal/CashPilot-wt-design-notify/design MacMini:/Volumes/Data/scratch/design-notify/wt/
ssh MacMini "cd /Volumes/Data/scratch/design-notify && for w in 1440 900 390; do node /Volumes/Data/scratch/fleet-design/shoot.cjs wt/design/money-waiting-notifications/$SUB/index.html wt/design/money-waiting-notifications/$SUB/shot-\$w.png \$w; done"
rsync -a "MacMini:/Volumes/Data/scratch/design-notify/wt/design/money-waiting-notifications/$SUB/shot-*.png" /Users/sergio/repos/personal/CashPilot-wt-design-notify/design/money-waiting-notifications/$SUB/
```

`shoot.cjs` takes the HTML path, the output PNG and the width. It shoots the
full page with `colorScheme: 'dark'`, a 900 px tall viewport and a 300 ms wait
(`MacMini:/Volumes/Data/scratch/fleet-design/shoot.cjs`). Open states
(an open menu, an open disclosure) must be drawn open in the HTML, because the
script does not click.

## 4. Part 1: the Money waiting panel

### 4.1 Where it lives

| Piece | Location |
|---|---|
| Template block | `app/templates/dashboard.html:52-61` |
| Row renderer `obligationRow` | `app/static/js/app.js:834-887` |
| Loader `loadMoneyWaiting` | `app/static/js/app.js:889-918` |
| Action handlers | `app/static/js/app.js:920-945` |
| Tag map `OBLIGATION_TAGS` | `app/static/js/app.js:816` |
| Date and countdown text | `app/static/js/app.js:818-832` |
| Styles | `app/static/css/style.css:1449-1496`, phone rules `:2151`, `:2177-2179` |
| API router | `app/routers/obligations.py` |
| Engine (what is due, sort order, push text) | `app/obligations.py` |
| Scheduler job and push | `app/main.py:3424-3435`, `:10015-10200` |
| User doc | `docs/reminders.md` |
| Catalog rules | `obligations:` in `services/bandwidth/{honeygain,repocket,bitping,mysterium}.yml`, `services/compute/salad.yml`, `services/depin/grass.yml`; schema `services/_schema.yml:435-476` |

The panel sits on the Dashboard below the money strip and above **Needs
attention** (`app/templates/dashboard.html:15-66`).

### 4.2 Elements

| Element | id / class | Notes |
|---|---|---|
| Section | `section#money-waiting.attention.money-waiting`, `aria-labelledby="money-waiting-title"`, starts `hidden` | `dashboard.html:55` |
| Head | `.block-head` > `h2#money-waiting-title.block-title` | Text `dashboard.waiting.title` = "Money waiting" (`en.json:1358`) |
| Count | `span#money-waiting-count.count` inside the title | Number of rows, empty at 0 (`app.js:909`) |
| List | `div#money-waiting-list.attn-list` | One `.attn-row` per reminder (`app.js:908`) |
| Muted foot | `div#money-waiting-muted.attn-foot`, starts `hidden` | The muted list (`app.js:910-914`) |
| Row | `div.attn-row.attn-{level}.mw-row[data-obligation="{slug}:{rule}"]` | `app.js:881` |
| Tag cell | `span.attn-tag` | Section 4.4 |
| Service cell | `span.attn-what` | The service name, `item.name` |
| Detail cell | `span.attn-why.mw-why` | A column of parts (section 4.4) |
| Actions cell | `span.attn-actions` | Section 4.5 |
| How disclosure | `details.mw-how` > `summary` "How" + text | Inside the detail cell (`app.js:857`) |
| More menu | `details.mw-more` > `summary.btn.btn-ghost.btn-sm` "More" + `div.mw-menu` | Absolute, right-aligned, z-index 20, min width 200 px, items stacked (`style.css:1489-1495`) |

The row grid on a desktop has four columns: tag `minmax(92px, max-content)`,
service `minmax(150px, 220px)`, detail `minmax(0, 1fr)`, actions
`fit-content(320px)` (`style.css:1453-1458`). The actions cell is a wrapping
flex row, right-aligned, gap 6 px. Its buttons may wrap their own label
(`style.css:1474-1475`). The 320 px cap is why the buttons wrap on a desktop.

### 4.3 Data fields

`GET /api/obligations` returns `{evaluated_at, items[], muted[]}`
(`app/routers/obligations.py:56-67`). Each item is `Item.as_dict()`
(`app/obligations.py:81-111`):

| Field | Meaning | Shown where |
|---|---|---|
| `slug`, `rule` | Service id and rule id. `rule` is a catalog id, `cash-out`, or `credential:<field>` | `data-obligation`, action arguments |
| `name` | Service display name | Service cell, "Open {name}", "Mute all {name} reminders" |
| `kind` | `rule`, `cash-out` or `credential` | Tag; the panel drops `credential` items (`app.js:906`) |
| `action` | `claim`, `withdraw`, `keep-active` or `renew` | Tag, Done label |
| `title` | One instruction from the catalog, or "Cash out your {name} balance" | First detail line |
| `loss` | What is lost, as a general fact | Detail line, muted |
| `how` | One or two sentences (catalog `how`, or `cashout.notes` for cash-out) | "How" disclosure |
| `url` | Where the user acts, on the provider's own domain | "Open {name}" primary button |
| `source` | The provider's terms or help page that states the rule | "Source" link |
| `checked` | The date someone last read `source` (ISO, e.g. `2026-11-24`) | "Source, checked {date}" (writers only) |
| `occurrence` | ISO date that identifies this occurrence | Done argument |
| `stage` | `d<N>` (inside the N-day warning), `overdue`, `recheck`, `ready`, `still-ready`, `expiring`, `expired` | Tag, level, extra line |
| `due` | ISO due date or null | "by {date}" |
| `days_left` | Integer or null; negative when past | Countdown, level |
| `censored` | The clock started before CashPilot's first reading | "by {date} or earlier" |
| `can_done` | False for credential items | Done button shown |
| `can_snooze` | False when the next snooze would run past the last warning (`obligations.py:258-262`) | Snooze buttons shown |
| `balance`, `currency`, `balance_usd` | Cash-out items only, never in a push | Appended to the title, plus "≈" in the display currency (`app.js:844-849`) |

Each `muted[]` entry is `{slug, rule, name, title}` (`obligations.py:458-471`).
`title` is the catalog rule title, or "Every reminder" (`*`), "Cash-out
reminder", or "Credential reminder ({field})" (`en.json:2118-2120`).

Sort order (`obligations.py:412-427`): overdue or expired first, then 7 days
or fewer left, then cash-out by balance (largest first), then the rest by days
left, then by name.

### 4.4 Row anatomy

**Tag** (`app.js:836-839`), last match wins:

1. `OBLIGATION_TAGS[action]`: claim → "Claim", withdraw → "Withdraw",
   keep-active → "Keep active"; anything else → "Act" (`en.json:906-912`).
2. Cash-out → "Cash out".
3. Stage `overdue` → "Overdue".
4. Stage `recheck` → "Arrived?".

**Level** (left border and tag colour, `app.js:840-841`, `style.css:1460-1467`):

| Level | When | Colour |
|---|---|---|
| `attn-fail` | stage `overdue` | error red |
| `attn-warn` | `days_left <= 7`, or stage `recheck` | warning amber |
| `attn-ask` | everything else | secondary grey |
| `attn-unknown` | the check failed (section 4.7) | muted grey |

**Detail cell parts, in order** (`app.js:851-857`):

1. `.mw-title`: the title. A cash-out row appends ": {amount} {currency}" and,
   when the display currency differs, " (≈ {converted})".
2. `.mw-when` (mono): "{by}, {n} days left", "{by}, today" or "{by}, {n} days
   ago". `{by}` is "by {date}" or "by {date} or earlier". The date is drawn as
   a calendar day, for example "22 Jan 2027". Absent when there is no due date
   (cash-out).
3. `.mw-loss`, only at stage `recheck`: "You marked this requested two weeks
   ago. Did the payout arrive?" Only at stage `overdue`: "The provider may
   already have written this off, and the balance may be gone."
4. `.mw-loss`: the `loss` text.
5. `details.mw-how`, only when `how` is set: summary "How", body the `how` text.

### 4.5 Actions

Roles: `_isOwner` is the owner; `_canWrite` is owner or writer
(`app.js:8-9`). Viewers (and the read-only API key) see the reminders but
no buttons (`docs/reminders.md:78-79`).

| Control | Label key → text | Shown when | Placement today | Calls | Toast on success |
|---|---|---|---|---|---|
| Open provider | `app.obl.open` → "Open {name}" | `item.url` set, every role | Row, `btn-primary`, new tab | `item.url` (external) | none |
| Done | `app.obl.done` → "Done" | `_canWrite` and `can_done`, and not cash-out, not withdraw, not recheck | Row, `btn-ghost` | `POST /api/obligations/{slug}/{rule}` `{action:"done", occurrence}` | `app.obl.marked_done` "Marked done." |
| Requested | `app.obl.requested` → "Requested" | same, for cash-out or `action: withdraw` | Row | same as Done | "Marked done." |
| It arrived | `app.obl.arrived` → "It arrived" | same, at stage `recheck` | Row | same as Done | "Marked done." |
| Snooze a day | `app.obl.snooze_day` → "Snooze a day" | `_canWrite` and `can_snooze` | Row | `{action:"snooze", days:1}` | `app.obl.snoozed_day` "Snoozed for a day." |
| More | `app.obl.more` → "More" | `_canWrite` | Row, `<details>` | opens `.mw-menu` | none |
| Snooze a week | `app.obl.snooze_week` → "Snooze a week" | `_canWrite` and `can_snooze` | More menu | `{action:"snooze", days:7}` | `app.obl.snoozed_week` "Snoozed for a week." |
| Not for me | `app.obl.not_for_me` → "Not for me" | `_canWrite` | More menu | `{action:"mute"}` on `{slug}/{rule}` | `app.obl.muted` "Muted. Unmute it at the foot of Money waiting." |
| Mute all | `app.obl.mute_all` → "Mute all {name} reminders" | `_canWrite` | More menu | `{action:"mute"}` on `{slug}/*` | same |
| Source, with date | `app.obl.source_checked` → "Source, checked {date}" | `_canWrite` and `item.source` | More menu, new tab | `item.source` (external) | none |
| Source, no date | `app.obl.source` → "Source" | not `_canWrite`, and `item.source` | Row, new tab | `item.source` (external) | none |
| Unmute | `app.obl.unmute` → "Unmute" | `_canWrite`, per muted entry | Muted foot, `btn-link` | `{action:"unmute"}` | `app.obl.unmuted` "Unmuted." |
| How | `app.obl.how` → "How" | `item.how` set, every role | Detail cell disclosure | none | none |

Code: `app.js:859-879`, `:912-913`, `:920-945`. Every action goes through
`obligationPost` (`app.js:920-928`): on success a `success` toast, on failure
an `error` toast with the API message, then the panel reloads.

The `checked` date in "Source, checked {date}" is the raw ISO string from the
catalog (`2026-11-24`), not formatted (`app.js:875`).

On a writer's desktop a typical row today has: Open {name} (pink), Done or
Requested, Snooze a day, More. Inside More: Snooze a week, Not for me, Mute
all {name} reminders, Source, checked {date}.

### 4.6 The muted foot

Shown when `muted[]` is not empty (`app.js:910-914`). Text:
`app.obl.muted_list` = "Not for me: {list}" (`en.json:894`). Each entry is
"{name}, {title}", followed for writers by an **Unmute** link button. Entries
are joined with " · ". Example: "Not for me: Honeygain, Keep a Honeygain device
sharing, or make a payout Unmute · Repocket, Every reminder Unmute".

### 4.7 States

| State | What shows | Code |
|---|---|---|
| Loading (first load) | Nothing. The section stays `hidden` until the first answer. No spinner. | `dashboard.html:55` |
| Empty (no items, nothing muted) | Section hidden | `app.js:917` |
| Only muted entries | Section shown, empty list hidden by `.attn-list:empty`, foot shown | `app.js:917`, `style.css:1452` |
| List | One row per item, count in the title | `app.js:908-909` |
| Check failed | Section shown, one row: tag "Unknown" (`app.obl.unknown_tag`), what "Money waiting" (`app.obl.money_waiting`), why "Could not check. Reload the page to try again." (`app.obl.check_failed`), level `attn-unknown`, no actions, foot hidden, count empty. Never an all-clear. | `app.js:898-904` |
| Action failed | Error toast with the API detail; panel reloads | `app.js:924-927` |
| Viewer | Rows without Done, Snooze or More; bare "Source" link; foot without Unmute | `app.js:860-879`, `:912` |
| Stage `d<N>` | Normal row; amber at 7 days or fewer | `obligations.py:131-136` |
| Stage `overdue` | Tag "Overdue", red, extra written-off line. Stays until Done, mute, or a payout resets the clock | `docs/reminders.md:71-74` |
| Stage `recheck` | 14 days after Done or Requested, if the condition still holds: tag "Arrived?", amber, extra line, button "It arrived" | `obligations.py:47`, `:251-256` |
| Cash-out `ready` / `still-ready` | Tag "Cash out", balance on the title, no date. After 30 days it becomes `still-ready` and pushes once more | `obligations.py:41-44`, `:336-373` |
| `can_snooze` false | No snooze buttons (too close to the last warning) | `obligations.py:258-262` |
| Snoozed or done | Row gone until the snooze ends or the next occurrence | `obligations.py:244-270` |

The panel loads with the Dashboard and reloads every hour (`app.js:378-397`),
and after every action.

### 4.8 API

| Route | Role | Body | Answers |
|---|---|---|---|
| `GET /api/obligations` | reader and up | none | `{evaluated_at, items, muted}`. Credential items and credential mutes go to owners only. 503 `api.could_not_check` "Could not check" on any failure. (`routers/obligations.py:56-67`, `:44-53`) |
| `POST /api/obligations/{slug}/{rule}` | writer and up; owner for `credential:*` | `{action: "done"\|"snooze"\|"mute"\|"unmute", days?: 1\|7, occurrence?}` | `{slug, rule, action, occurrence?, snoozed_until?}` (`routers/obligations.py:99-146`) |

POST errors, all with an `en.json` text:

| Code | Key | Text |
|---|---|---|
| 400 | `api.action_must_one` | "action must be one of {actions}" |
| 404 | `api.no_such_reminder` | "No such reminder" (unknown or dead service, unknown rule, or a writer on a credential rule) |
| 404 | `api.reminder_not_due_now` | "This reminder is not due now" (done or snooze on an item not in today's list) |
| 400 | `api.one_clears_itself_once_fixed` | "This one clears by itself once it is fixed" (done on a credential item) |
| 400 | `api.days_must_1_7` | "days must be 1 or 7" |
| 409 | `api.too_close_deadline_snooze` | "Too close to its deadline to snooze" |

The snooze lengths are fixed at 1 and 7 days on the server
(`routers/obligations.py:35`). Any other length needs a server change.

Every POST writes an audit row `obligation_{action}` with the actor's name
(`routers/obligations.py:143-145`). The state lives in the `obligation_state`
table, one row per `(slug, rule)`: `anchor_at`, `anchor_censored`, `done_for`,
`done_at`, `snoozed_until`, `muted`, `updated_by`, `updated_at`
(`app/database.py:1040-1052`). It is shared by the whole household, not per
user (`docs/reminders.md:92-94`).

### 4.9 Every message text

`app.obl.*` (`app/i18n/en.json:881-916`):

| Key | Text |
|---|---|
| `app.obl.arrived` | It arrived |
| `app.obl.by` | by {date} |
| `app.obl.by_or_earlier` | by {date} or earlier |
| `app.obl.check_failed` | Could not check. Reload the page to try again. |
| `app.obl.days_ago` | {by}, {n, plural, one {# day} other {# days}} ago |
| `app.obl.days_left` | {by}, {n, plural, one {# day left} other {# days left}} |
| `app.obl.done` | Done |
| `app.obl.how` | How |
| `app.obl.marked_done` | Marked done. |
| `app.obl.money_waiting` | Money waiting |
| `app.obl.more` | More |
| `app.obl.mute_all` | Mute all {name} reminders |
| `app.obl.muted` | Muted. Unmute it at the foot of Money waiting. |
| `app.obl.muted_list` | Not for me: {list} |
| `app.obl.not_for_me` | Not for me |
| `app.obl.open` | Open {name} |
| `app.obl.overdue` | The provider may already have written this off, and the balance may be gone. |
| `app.obl.recheck` | You marked this requested two weeks ago. Did the payout arrive? |
| `app.obl.requested` | Requested |
| `app.obl.snooze_day` | Snooze a day |
| `app.obl.snooze_week` | Snooze a week |
| `app.obl.snoozed_day` | Snoozed for a day. |
| `app.obl.snoozed_week` | Snoozed for a week. |
| `app.obl.source` | Source |
| `app.obl.source_checked` | Source, checked {date} |
| `app.obl.tag.act` | Act |
| `app.obl.tag.arrived` | Arrived? |
| `app.obl.tag.cash_out` | Cash out |
| `app.obl.tag.claim` | Claim |
| `app.obl.tag.keep_active` | Keep active |
| `app.obl.tag.overdue` | Overdue |
| `app.obl.tag.withdraw` | Withdraw |
| `app.obl.today` | {by}, today |
| `app.obl.unknown_tag` | Unknown |
| `app.obl.unmute` | Unmute |
| `app.obl.unmuted` | Unmuted. |

Other keys the panel or its pushes use:

| Key | Text | Line |
|---|---|---|
| `dashboard.waiting.title` | Money waiting | `en.json:1358` |
| `obligations.cash_out.title` | Cash out your {name} balance | `en.json:2100` |
| `obligations.cash_out.loss` | Money left at a provider can be lost if it bans the account, stalls payouts or closes. | `en.json:2099` |
| `obligations.credential.title` | Renew the {name} {field} in CashPilot | `en.json:2103` |
| `obligations.credential.loss` | CashPilot stops reading this balance, so its other reminders go stale. | `en.json:2102` |
| `obligations.credential.how` | Paste a fresh value under Settings, Earnings collection. | `en.json:2101` |
| `obligations.muted.every` / `.cash_out` / `.credential` | Every reminder / Cash-out reminder / Credential reminder ({field}) | `en.json:2118-2120` |
| `obligations.push.*` | Push titles, e.g. "CashPilot: {name}, claim within {days} days" | `en.json:2121-2129` |
| `obligations.summary.title` | CashPilot: {n} things to do before you lose money | `en.json:2131` |
| `obligations.summary.body` | {names}. Open the CashPilot dashboard, Money waiting, to see each one. | `en.json:2130` |

Catalog rule texts (title, loss, how) are English YAML in `services/*/*.yml`,
translated through `services/_i18n`.

### 4.10 Layout at each width today

- Above 768 px: the four-column grid of section 4.2. The actions cell is capped
  at 320 px, so four or five buttons wrap onto two or three lines.
- At 768 px and below (`style.css:2151`, `:2177-2179`): the row becomes two
  columns (tag, service). The detail and the actions each take a full line.
  The actions are left-aligned.
- The More menu opens as an absolute panel under its button, right-aligned
  (`style.css:1492-1495`).

### 4.11 Keyboard and accessibility facts today

- All controls are native `<a>`, `<button>`, `<details>`/`<summary>`, so they
  are in the tab order. Focus ring: `:focus-visible` 2 px outline
  (`style.css:1352`), cyan in the classic theme (`style.css:2334`).
- The More menu does not close on Escape or on a click outside. It closes only
  when its summary is toggled again. No code handles `.mw-more` beyond the
  markup (`app.js:876`; the only Escape handler closes modals, `app.js:263`).
- The bell button has no `aria-expanded` and no Escape handler
  (`app.js:6774-6788`).

## 5. What Source and Not for me do

**Source.** It is a plain link to the provider's own page that states the
rule: their terms of use or a help article. Examples: Honeygain's terms
(`https://www.honeygain.com/terms-of-use/`), the MystNodes rewards help page
(`services/bandwidth/honeygain.yml`, `services/bandwidth/mysterium.yml`). It
opens in a new tab. It changes nothing in CashPilot. It exists so the user can
check the rule themselves. The catalog requires it to be `https` on the
provider's domain, because fake claim sites exist (`services/_schema.yml:447-455`,
`docs/reminders.md:122-124`). Writers see it in the More menu with the date
someone last read that page ("Source, checked 2026-11-24"). Viewers see it on
the row as "Source", without the date (`app.js:875-878`). Cash-out rows and
credential rows have no source, so they have no Source link
(`obligations.py:357-373`, `:389-402`).

**Not for me.** It mutes one reminder rule for one service, for the whole
household (`POST .../{slug}/{rule}` with `action: "mute"`). A muted rule:

- leaves the panel at once, and every later occurrence stays hidden too;
- sends no more pushes, because the evaluation skips it
  (`obligations.py:319-320`, `:348-349`);
- is listed at the foot of the panel as "Not for me: {name}, {title}", with
  **Unmute**;
- is recorded in the audit log with the person's name.

The catalog's own example is Honeygain in JumpTask mode, where a flat balance
is normal, so "Keep a device sharing" does not apply. That rule's `how` text
says "choose Not for me" (`services/bandwidth/honeygain.yml`,
`docs/reminders.md:87-90`).

**Mute all {name} reminders** does the same for the rule `*`. It mutes every
reminder of that service: catalog rules, the cash-out nudge and credential
reminders (`obligations.py:228-231`). The foot lists it as "{name}, Every
reminder".

Mute is not the same as Done or Snooze. Done hides one occurrence; a monthly
window comes back next month. Snooze hides it for 1 or 7 days and holds its
pushes, and never runs past the last warning. Mute hides the rule until
someone unmutes it.

## 6. What notifies the user today

### 6.1 Surfaces

| Surface | Where | Who sees it | Source of data | Configurable today |
|---|---|---|---|---|
| **Bell** (topbar) | `base.html:102-113`; `app.js:6774-7024` | every signed-in role; activity alerts owner only | `GET /api/collector-alerts` every 60 s (`main.py:12021-12080`), plus credential forecasts from `GET /api/credentials/health` added in the browser (`app.js:6884-6903`) | No. No mute, no dismiss, no filter. Entries clear only when the fault clears. |
| Bell badge | `#notify-badge` | same | count of bell entries | No. Grey when every entry is a credential forecast, "?" when the fetch failed (`app.js:6931-6936`, `:7015-7022`) |
| **Needs attention** (Dashboard) | `dashboard.html:66-81` | every role | the same bell alerts, plus workers and services (`app.js:1925-1935`) | No |
| Payout queue (inside Needs attention) | `#payout-queue-card`, `dashboard.html:76-79` | every role; Yes/No buttons for writers | `GET /api/earnings/payouts` (`app.js:756`) | No |
| **Money waiting** (Dashboard) | section 4 | every role; actions for writers | `GET /api/obligations` | Per reminder: Done, Snooze 1 or 7 days, mute one rule, mute a whole service |
| **Update banner** | `base.html:158-162`; `app.js:6808-6851` | every signed-in role | `GET /api/update-status` (`main.py:11965`), once per page load | Dismiss per version, stored in this browser only (`localStorage cp-update-dismissed`). Off for everyone with `CASHPILOT_UPDATE_CHECK=off` (`docs/configuration.md:270-296`) |
| **Toasts** | `.toast-container`, `app.js:116-140` | the person who acted | the result of an action in the page | No |
| **External push** | `app/notify.py` | whoever reads the channel | `notify.send` from `_push_alert` (`main.py:1464-1500`) | Only by environment variables (section 6.3) |

CashPilot does not use browser notifications. There is no `Notification` API
call and no service worker in `app/static/js` (grep, 2026-11-28).

### 6.2 Alert kinds

Each kind is recorded with `database.record_alert(kind, subject, message)`
(`app/database.py:4190`). The row is the dedupe: a new row means "push now".
The default cooldown is 24 hours per kind and subject
(`database.py:3960`). A cleared fault deletes its row, so the next failure
pushes again (`docs/fleet.md:325-329`).

| Kind | What it means | Bell | Push | Repeats at most | Code |
|---|---|---|---|---|---|
| `collector` | A collector failed. Category `auth` (credential rejected), `transient` (provider unreachable), `shape` (the page changed: our bug), or none | yes | yes | once per 24 h, until it recovers | `main.py:2299-2310` |
| `notice` | A caveat on a reading that worked, or a device not on the account | yes | yes | 24 h | `main.py:2064`, `:2339` |
| `payout` | The balance dropped: was this a payout? | yes, and payout queue | yes | one pending per service | `main.py:1566-1580` |
| `flatline` | The balance has gone quiet | yes | yes | once per episode | `main.py:1711`, `:1771` |
| `container` | A container stopped running | yes | yes | 24 h | `main.py:684-685` |
| `missing` | Recorded as deployed but runs on no box, or gone from one box | yes | yes | 24 h | `main.py:938-945` |
| `account_disabled` | The provider disabled the account | yes | yes | once a year | `main.py:756`, `:830` |
| `proxied` | A proxied copy or its tunnel is down | yes | yes | 24 h | `main.py:1160-1161` |
| `stall` | A running copy carries almost no traffic | yes | yes | once per episode | `main.py:1234`, `:1327` |
| `docker` | A worker cannot reach Docker | yes, with "How to fix" | yes | 24 h | `main.py:1404-1405` |
| `worker` | A worker went offline | yes | yes, at most once per 6 h per worker | 24 h | `main.py:2599`, `:3141-3170` |
| `proxy_cap` | A proxy reached its traffic cap | yes | yes | 24 h | `main.py:9497-9499` |
| `activity_mail` | An earner sent mail | yes, owner only | yes | once a day per container | `main.py:13398-13409`, `activity_ui.py:51` |
| `activity_lan` | An earner reached into the LAN | yes, owner only | yes | every 6 h per container and kind | same, `activity_ui.py:52` |
| `activity_spike` | An unusual hour of traffic | yes, owner only | **no** | every 12 h | `main.py:13475-13481`, `activity_ui.py:53` |
| credential forecast | A saved credential expires soon or is past its usual life | yes (built in the browser, category `expiring`) | yes, as a Money waiting credential reminder | once per stage | `app.js:6895-6903`; `obligations.py:376-409` |
| `obligation` | A Money waiting reminder reached a new warning stage | **no** (never in the bell) | yes, 09:00-21:00 only; more than 3 at once become one summary | once per stage of each occurrence | `main.py:10152-10200` |
| update available | A newer CashPilot release exists | banner, not the bell | **no** | per version | `app.js:6808-6851` |

The bell entry text is `{platform}{suffix}`, then the message. The suffixes
are `app.bell.s.*` (`en.json:511-528`), for example " — credential expired",
" — not running", " — payout?". The empty-bell texts are "All collectors
healthy" (`app.bell.healthy`), "No collection has run yet — nothing has been
checked." (`app.bell.never_ran`) and "No collection in {mins} minutes — status
unknown. Check the server." (`app.bell.stale`). A failed fetch shows "Alerts
unavailable — could not reach the server" (`app.bell.unavailable_text`). The
bell's title is "Collector alerts" and its header "Collector Alerts"
(`en.json:1267-1268`), although it holds every kind above except `obligation`.

Bell buttons per entry: "Fix credential" or "Update" (opens the credential
form, owner only, `app.js:6998`, `:7009`), "How to fix" for `docker`
(`app.js:7010`), "Add to account" links for unlinked devices, owner only
(`app.js:6854-6865`). The credential button also shows on `worker` entries,
because `showFix` does not exclude that kind (`app.js:6998`).

There is no severity field. The nearest things are the bell's icon choice
(warning triangle, info circle, payout coin; `app.js:6940-6993`), the grey
badge for forecasts only, the failure `category`, and the Money waiting level
(red, amber, grey).

### 6.3 External channels

Three channels exist. All are set only by environment variables on the UI
container. All are off until set (`app/notify.py:1-17`, `:117-126`):

| Channel | Variables | What is sent |
|---|---|---|
| ntfy | `CASHPILOT_NTFY_URL` (full topic URL) | body = message, header `Title` (`notify.py:133-136`) |
| Webhook | `CASHPILOT_WEBHOOK_URL` | JSON `{title, message, kind, subject}`; Money waiting uses `kind: "obligation"` (`notify.py:139-141`, `docs/reminders.md:114-115`) |
| Telegram | `CASHPILOT_TELEGRAM_BOT_TOKEN` and `CASHPILOT_TELEGRAM_CHAT_ID` | `"{title}\n\n{message}"` (`notify.py:144-150`) |

Facts about delivery:

- Every configured channel gets every push. There is no per-channel or
  per-kind choice (`notify.py:153-181`).
- Every push is redacted first (tokens, header values, device ids) and cut to
  400 characters (`notify.py:55-56`, `:101-114`).
- A push that reaches no channel releases its dedupe row, so the next run
  retries (`main.py:1464-1500`).
- With no channel set, CashPilot logs one warning at start-up and the bell is
  the only place alerts show (`main.py:3272-3282`).
- The Settings page cannot show or set these variables. The Environment
  section lists only `CASHPILOT_API_KEY`, `CASHPILOT_SECRET_KEY`,
  `CASHPILOT_HOSTNAME_PREFIX`, `CASHPILOT_COLLECT_INTERVAL`,
  `CASHPILOT_DATA_DIR` and `TZ` (`main.py:12534-12566`).
- Documented in `docs/configuration.md:51-54` and `docs/fleet.md:320-329`.

Channels that do **not** exist in the code: Apprise, email (SMTP), browser
notifications, Pushover, Discord, Slack, Matrix. (The words "SMTP" in
`app/procnet.py` and `app/activity_ui.py` are about detecting earners that
send mail, not about sending it.)

### 6.4 Everything a user can change today

| Choice | How | Scope |
|---|---|---|
| Channels on or off | Environment variables, then restart | the install |
| Money waiting push hours | Fixed 09:00-21:00 (`main.py:10019`), in the first owner's saved timezone, then `TZ`, then UTC (`main.py:10036-10047`). The timezone is saved once by the setup wizard from the browser (`app.js:3652`); no screen changes it | the install |
| One reminder | Done, Snooze 1 or 7 days, mute, unmute (section 4.5) | the household |
| All reminders of a service | Mute all {name} reminders | the household |
| Update banner | Dismiss per version (this browser), or `CASHPILOT_UPDATE_CHECK=off` | browser, or install |
| Activity alerts | Turn Activity off per worker on the Activity page, owner only (`routers/activity.py:142-163`). That stops the data, so it also stops the alerts | per worker |

Nothing else exists: no quiet hours for the other kinds, no "only payouts", no
minimum severity, no per-kind or per-service mute outside Money waiting, no
"pause everything for N days", no per-user choice.

## 7. The Settings frame for the Notifications section

- `GET /settings` is owner only (`app/routers/pages.py:94-101`). A writer or a
  viewer gets 403. A Notifications section placed there is therefore owner only
  unless it moves.
- Today's layout: `.settings-layout` with a sticky left index
  `nav.settings-index` (links to `#set-…` anchors) and `.settings-body` with one
  `.card.settings-section` per topic (`app/templates/settings.html:8-164`).
  Sections today, in order: Earnings collection (`#set-collection`),
  Credential health (`#credential-health-card`), Device ids
  (`#set-identities`), Restore (`#set-restore`), Encryption key (`#set-key`),
  Earner credentials (`#set-earner-secrets`), Environment (`#set-env`), About
  and updates (`#set-about`), plus a link to Import.
- Each section is `h3.settings-section-title`, `p.settings-section-desc`, a
  body `div`, and `div.settings-actions` with a `btn-primary` save button and
  a `span.muted` status (`settings.html:23-38`).
- For the mockup, use this frame: topbar, the index with a "Notifications"
  entry added, and the new section in the body. Keep the section free of
  layout assumptions, so the `design/settings-page` lane can move it.
- Where preferences are stored today: `user_preferences` holds per-user
  `timezone`, `theme`, `language` and setup fields (`database.py:729-744`,
  `GET/POST /api/preferences`, `main.py:12398-12460`). Household-wide state
  lives in tables such as `obligation_state`. No table holds notification
  choices.

## 8. Sample data (the owner's live setup)

Use these names and numbers so the mockups look real.

- Topbar total: **$52.07**. CashPilot **v3.1.0**.
- Boxes: **watchtower**, **geiserback**, **geiserct** (Unraid/Linux servers);
  phones **OPPO CPH1951 (5bdadbc5)** and **motorola one fusion+ (1414f972)**.
- Earners: honeygain, earnfm, mysterium, packetstream, traffmonetizer,
  repocket, proxyrack, storj, bitping, bytelixir, iproyal, proxybase, proxylite.

Money waiting rows (use the `app.obl.tag.*` tags):

| Service | Tag | Title | When | Primary |
|---|---|---|---|---|
| Honeygain | Cash out | Cash out your Honeygain balance: 18.76 USD | (no date) | Open Honeygain |
| Storj | Arrived? | Cash out your Storj balance | (no date) + "You marked this requested two weeks ago. Did the payout arrive?" | Open Storj |
| PacketStream | Keep active | Log in to PacketStream to keep the balance | by 10 Dec 2026, 12 days left | Open PacketStream |
| EarnFM | Claim | Claim your EarnFM balance | by {date}, {n} days left | Open EarnFM |
| MystNodes | Claim | Claim last month's MystNodes rewards | by 1 Dec 2026, 3 days left (the November window; amber) | Open MystNodes |

How these compare with what the code would show today, so nobody mistakes a
sample for a feature:

- Only Honeygain, Repocket, Bitping, MystNodes, Salad and Grass have catalog
  rules. PacketStream, EarnFM and Storj rules are samples only.
- A cash-out row appears only at or above the provider minimum and at least
  $5. Honeygain's minimum is $20 (`services/bandwidth/honeygain.yml`), so
  $18.76 would show no row. Honeygain also has a withdraw rule, which replaces
  the generic cash-out row while it is visible (`obligations.py:451-453`).
- The "Arrived?" recheck comes 14 days after Requested, not 9
  (`obligations.py:47`).
- MystNodes pays out by itself (`cashout.method: auto`), so it gets no cash-out
  row, only the monthly claim rule.

A designer may adjust the samples to match the code. Keep the names.

A muted foot sample: "Not for me: Honeygain, Keep a Honeygain device sharing,
or make a payout · Repocket, Every reminder".

Bell samples: "geiserback — Docker unreachable", "earnfm — credential
expired", "storj — payout?", "worker 'OPPO CPH1951 (5bdadbc5)' went offline".

## 9. Checklist: everything that must stay reachable

Money waiting, per row:

- [ ] Tag (Claim, Withdraw, Keep active, Act, Cash out, Overdue, Arrived?) and level colour
- [ ] Service name
- [ ] Title, with balance and "≈" conversion on cash-out rows
- [ ] Due date, "or earlier" when censored, days left / today / days ago
- [ ] Overdue line and recheck line
- [ ] Loss text
- [ ] How text (disclosure)
- [ ] Open {name} (primary, new tab)
- [ ] Done / Requested / It arrived
- [ ] Snooze a day
- [ ] Snooze a week
- [ ] Not for me (mute this rule)
- [ ] Mute all {name} reminders
- [ ] Source link, and the checked date
- [ ] Viewer variant: no write actions, Source still reachable
- [ ] Snooze hidden when `can_snooze` is false

Money waiting, panel:

- [ ] Title and count
- [ ] Muted list with Unmute per entry
- [ ] Hidden when empty; shown with only the foot when only muted entries exist
- [ ] "Could not check" row on a failed check, never an all-clear
- [ ] Success and error toasts after each action

Notifications (today's facts the Settings section must account for):

- [ ] Bell, its badge states (count, grey, "?"), its empty texts
- [ ] Every alert kind in section 6.2, by name
- [ ] Money waiting pushes and their 09:00-21:00 window and summary rule
- [ ] Update banner and its per-version dismiss
- [ ] The three channels (ntfy, webhook, Telegram), set by environment today
- [ ] The state with no channel configured
- [ ] Activity alerts are owner only; `activity_spike` never pushes
- [ ] Per-reminder and per-service mutes, managed in one place as well as on the row
