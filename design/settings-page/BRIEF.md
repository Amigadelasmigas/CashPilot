# Settings page redesign: the brief

This file is the single source for every design in `design/settings-page/`.
It records what the Settings page and the Import page are today: every
element, control, action, API route, state, data field and message. It holds
no design opinions.

- Base: branch `design/settings-page`, off `origin/main` at `aa543a48`.
- All paths are relative to the repository root. `file:line` points at that commit.
- "Words" counts every word a person reads (HTML tags removed, code blocks not counted).

## Contents

1. [How to build a mockup](#1-how-to-build-a-mockup)
2. [The page frame](#2-the-page-frame)
3. [The section index](#3-the-section-index)
4. [Loading order and page-wide states](#4-loading-order-and-page-wide-states)
5. [Sections, one by one](#5-sections-one-by-one)
6. [The Import page, which must move into Settings](#6-the-import-page-which-must-move-into-settings)
7. [The Notifications slot](#7-the-notifications-slot)
8. [Shared dialogs, prompts and toasts](#8-shared-dialogs-prompts-and-toasts)
9. [Links into this page that must keep working](#9-links-into-this-page-that-must-keep-working)
10. [Tests bound to the current markup](#10-tests-bound-to-the-current-markup)
11. [Facts found while reading the code](#11-facts-found-while-reading-the-code)
12. [Realistic data for the mockups](#12-realistic-data-for-the-mockups)
13. [Word count per section](#13-word-count-per-section)
14. [Checklist: everything that must stay reachable](#14-checklist-everything-that-must-stay-reachable)

---

## 1. How to build a mockup

- One folder per design: `design/settings-page/<sub>/index.html`.
- Link the real stylesheet relatively: `<link rel="stylesheet" href="../../../app/static/css/style.css">`.
- Put `data-theme="classic"` on `<html>`. Classic night is the default theme (`app/themes.json:2`). Its tokens are at `app/static/css/style.css:2294-2306`. Its primary button is pink (`style.css:2313-2316`).
- The fonts come from Google Fonts in production (`app/templates/base.html:15-16`): IBM Plex Sans and IBM Plex Mono. Add the same `<link>` to the mockup, or the system fallback shows.
- Add your own `<style>` only for new parts.
- Render on the MacMini, never on the MacBook. The command is in the lane task: rsync `app/static` and `design` to `MacMini:/Volumes/Data/scratch/design-settings/wt/`, then run `node /Volumes/Data/scratch/fleet-design/shoot.cjs <html> <png> <width>` at 1440, 900 and 390.

### Classic night tokens (style.css:2294-2306)

| Token | Value |
|---|---|
| `--bg-primary` | `#0b0b14` |
| `--bg-secondary`, `--bg-card` | `#11111d` |
| `--bg-tertiary` | `#171726` |
| `--bg-hover` | `#1d1d2f` |
| `--bg-input` | `#08080f` |
| `--border-color` | `#25233a` |
| `--border-light` | `#322f4b` |
| `--border-strong` | `#4b4670` |
| `--text-primary` | `#e8e6f0` |
| `--text-secondary` | `#bdb6cf` |
| `--text-muted` | `#a59cb5` |
| `--accent` (pink) | `#f472b6`, hover `#f9a8d4` |
| `--accent-secondary` (cyan) | `#22d3ee` |
| `--success` / `--warning` / `--error` | `#46b37f` / `#e0a53c` / `#f06a5f` (from `:root`, style.css:38-45) |
| `--font-ui` / `--font-mono` | IBM Plex Sans / IBM Plex Mono (style.css:63-64) |
| `--radius` | `2px` (style.css:77) |
| `--topbar-height` | `48px` (style.css:75) |

Measured contrast (WCAG ratio, computed for this brief):

| Text | on `#0b0b14` | on `#11111d` | on `#171726` |
|---|---|---|---|
| `--text-muted` `#a59cb5` | 7.48 | 7.15 | 6.76 |
| `--text-secondary` `#bdb6cf` | 10.03 | 9.59 | 9.06 |
| `--accent` `#f472b6` | 7.40 | 7.07 | 6.68 |
| `--warning` `#e0a53c` | 8.97 | 8.57 | 8.10 |
| `--error` `#f06a5f` | 6.47 | 6.18 | 5.84 |
| `--success` `#46b37f` | 7.48 | 7.14 | 6.75 |

Button text `#0b0b14` on pink `#f472b6`: 7.40.

Page title (`.page-title`, style.css:1386) uses the UI font, `--fs-5`, weight 600. Section titles (`.settings-section-title`, style.css:1880) use the UI font, `--fs-4`, weight 600. The mono font is used for figures, keys and code (for example `.kv-sub mono`, `.stat-value`).

---

## 2. The page frame

| What | Where |
|---|---|
| Route `GET /settings` | `app/routers/pages.py:94-101`. Signed-in owner only; any other role gets 403 `api.owner_access_required`. |
| Template | `app/templates/settings.html` (165 lines), extends `base.html`. |
| `<title>` | `settings.title` = "Settings - CashPilot" (`en.json:2320`), settings.html:3 |
| `<body data-page>` | `settings` (settings.html:4). `app.js:7220-7228` runs the page code on it. |
| Page heading `h1.page-title` | `settings.heading` = "Settings" (`en.json:2292`), settings.html:5, rendered by base.html:167 |
| Layout | `.settings-layout` (grid, 176 px index + content, style.css:1871), `.settings-index` (sticky, style.css:1872-1877), `.settings-body` (max 1080 px, style.css:1878). Under the mobile breakpoint the index becomes a wrapped row of links (style.css:2098-2100). |
| Section box | `.card.settings-section` (top border only, 30 px gap, `scroll-margin-top: 60px`, style.css:1879). |
| Section title | `h3.settings-section-title` (style.css:1880). |
| Section intro | `p.settings-section-desc` (`--fs-2`, `--text-secondary`, max 82ch, style.css:1881). |
| Button row | `.settings-actions` (flex, 8 px gap, style.css:1882). |
| Loading line | `p.loading-line` (style.css:1406). |
| Empty line | `p.block-empty` (style.css:1405). |

The top bar comes from `base.html` and is the same on every page: logo, nav (Dashboard, Fleet, Catalog, Payouts, Activity, Settings for the owner), "+ Add service" button, total earnings with currency select (`#topbar-total`, `#topbar-currency`), alerts bell, avatar menu with theme picker (`base.html:66-140`).

---

## 3. The section index

`nav.settings-index`, `aria-label` = `settings.index.aria` "Settings sections" (`en.json:2299`). settings.html:9-19. Nine links, in this order:

| # | Label key and text | `href` | Line | Note |
|---|---|---|---|---|
| 1 | `settings.collection.title` "Earnings collection" | `#set-collection` | :10 | |
| 2 | `settings.health.title` "Credential health" | `#credential-health-card` | :11 | `id="credential-health-link"`, `hidden` until rows exist (app.js:5525-5531) |
| 3 | `settings.identities.title` "Device ids" | `#set-identities` | :12 | |
| 4 | `settings.index.restore` "Restore" | `#set-restore` | :13 | Short label; the section title is "Restore from a backup" |
| 5 | `settings.key.title` "Credential encryption key" | `#set-key` | :14 | The lane task calls this "API key". The fleet API key itself is a row in Environment. |
| 6 | `settings.earner_secrets.title` "Earner credentials on each box" | `#set-earner-secrets` | :15 | |
| 7 | `settings.env.title` "Environment" | `#set-env` | :16 | |
| 8 | `settings.about.title` "About and updates" | `#set-about` | :17 | |
| 9 | `settings.index.import` "Import from another tool" | `/import` | :18 | Leaves the page. Looks the same as the eight anchors. |

Words: 23 (21 while the health link is hidden).
Controls: 9 links. No active-section highlight; only `:hover` (style.css:1877).

---

## 4. Loading order and page-wide states

`loadSettings()` (app.js:5574-5606), called at page start (app.js:7221):

1. `populateCurrencyDropdown()` (app.js:7044). It looks for `#settings-currency`, which settings.html does not contain, so it returns at once (see section 11).
2. `loadUpdateCard()` (About), independent.
3. `loadIdentities()` (Device ids), independent.
4. `loadEncryptionKey()` (Credential encryption key), independent.
5. `loadEarnerSecrets()` (Earner credentials), independent.
6. Together: `GET /api/config`, `GET /api/env-info` (errors become `[]`), `GET /api/collectors/meta` (errors become `[]`). Then `renderEnvVars`, `renderCollectors`, then `loadCredentialHealth()`.

Page-wide error: if `GET /api/config` fails, `settingsPanelsFailed()` (app.js:6260-6266) writes the same message in red (`p.text-fail`) into both `#env-vars-container` and `#collectors-container`:

- `app.settings.load_failed` (`en.json:1078`): "Could not load settings. Your session may have expired — reload the page, and sign in again if you are asked to."
- `app.settings.load_failed_detail` (`en.json:1079`): "Could not load settings: {error}. Your session may have expired — reload the page, and sign in again if you are asked to."

Every other section writes its own error into its own container (listed per section below).

Other start-up code for this page (app.js:7220-7228):

- `#restore-file` gets a `change` listener: `restoreFileChanged` (app.js:6164).
- `?highlight=<slug>` in the URL opens that collector after 300 ms: `openCollectorSection` (app.js:7026-7033) sets `open`, scrolls it to the centre and adds `.highlight-flash` for 2 s (style.css:403).

---

## 5. Sections, one by one

### 5.1 Earnings collection (`#set-collection`)

settings.html:22-38. JS: `renderCollectors` app.js:6502-6582, `saveCollectorCredentials` :6584-6607, `clearServiceCredentials` :6609-6621, `testCollectors` :6623-6634.

**Elements**

| Element | id / class | Line |
|---|---|---|
| Title | `h3.settings-section-title` `settings.collection.title` "Earnings collection" (`en.json:2286`) | :24 |
| Intro | `p.settings-section-desc` `settings.collection.desc` (`en.json:2284`) | :25-27 |
| List container | `#collectors-container`, first holds `p.loading-line` `settings.loading` "Loading..." (`en.json:2315`) | :29-31 |
| Save button | `button.btn.btn-primary[data-action=saveCollectorCredentials]` `settings.collection.save` "Save credentials" (`en.json:2285`) | :34 |
| Collect button | `button.btn.btn-secondary[data-action=testCollectors]` `settings.collection.collect_now` "Collect now" (`en.json:2283`) | :35 |
| Status text | `span#collector-save-status.muted` | :36 |

Intro text, quoted: "Credentials for automated earnings tracking. Only services with a built-in collector are shown. You don't need to deploy containers through CashPilot — just add your credentials."

**What the JS draws** (app.js:6554-6573): a two-column grid `div.collectors-grid` > two `div.collectors-col` (style.css:1085-1099; one column on a phone, `display: contents`, CSS `order` keeps the reading order). One `details.collector-section#collector-<slug>` per collector, closed by default:

- `summary.collector-header`: `span.collector-name` (service name) and one status badge.
- `div.collector-body`: optional `div.form-hint.collector-hint` (the service's `collector.credential_hint` from its YAML, run through `sanitizeHint`), then one `div.form-group` per field: `label.form-label` (field label, plus `span.optional` `app.cred.optional` "(optional)" `en.json:636` when not required), `input.form-input.collector-input#cred-<config_key>[data-config]` (type `password` for secret fields, `text` otherwise).
- A configured collector, for the owner, also gets `div.kv-actions.kv-actions-end` > `button.btn.btn-danger.btn-sm[data-action=clearServiceCredentials]` `app.coll.clear` "Clear credentials" (`en.json:613`).

There are 20 collectors (`app/collectors/__init__.py:37-58`): anyone-protocol, honeygain, earnapp, iproyal, mysterium, storj, traffmonetizer, repocket, proxyrack, bitping, earnfm, packetstream, grass, bytelixir, salad, ocean, supportxmr, herominers-kas, 2miners-etc, unmineable. Sorted by slug (`main.py:12615`). Fields per collector: `_COLLECTOR_ARGS`, `app/collectors/__init__.py:61-91` (for example honeygain: Email, Password; bytelixir: Session Cookie, optional Remember Web, optional Xsrf Token; unmineable: Address, Coin). Field labels are the arg name in Title Case, built in English on the server (`main.py:12627`).

**Data fields** (`GET /api/collectors/meta`, main.py:12598-12641): `slug`, `name`, `fields[] {key, label, secret, required}`, `currency`, optional `hint`. Values from `GET /api/config` (main.py:12649-12654): non-secret values in clear, secrets only as a yes/no map under `_secrets`.

**States**

| State | What shows | Key |
|---|---|---|
| Loading | "Loading..." | `settings.loading` |
| No collectors | `p.block-empty` "No collectors available." | `app.coll.none` (`en.json:621`) |
| Config failed | red page-wide message (section 4) | `app.settings.load_failed*` |
| Collector badge: all required fields set | `badge.badge-deployed` "Configured" | `app.coll.configured` (`en.json:617`) |
| Badge: some required set | `badge.badge-warning` "Incomplete", title "Some required credentials are missing, so this service is not being collected" | `app.coll.incomplete`, `app.coll.incomplete_title` (`en.json:619-620`) |
| Badge: none set | `badge.badge-category` "Not configured" | `app.coll.not_configured` (`en.json:622`) |
| Secret field already stored | empty input, placeholder "•••••••• (set — leave blank to keep)" | `app.cred.set_keep` (`en.json:639`) |
| Secret field not stored | placeholder "Not set" | `app.env.not_set` (`en.json:762`) |
| Non-secret field | value filled in, placeholder = field label | |
| Deep link `#collector-<slug>` | that collector opens and scrolls to the centre (app.js:6574-6581) | |

**Actions**

| Action | Route | Messages |
|---|---|---|
| Save credentials: sends every non-empty `.collector-input` | `POST /api/config` `{data}` (main.py:12675) | none typed: toast warning "No credentials to save" `app.coll.nothing` (`en.json:623`); success toast "Credentials saved" `app.coll.saved` (`en.json:625`), then the whole page reloads its data; failure toast "Save failed: {error}" `app.save_failed` (`en.json:1066`) |
| Collect now | `POST /api/collect` (main.py:9969, writer role) | status "Running collection..." `app.coll.running` (`en.json:624`); toast "Collection started. Check dashboard in a moment." `app.coll.started` (`en.json:626`); status "Collection triggered" `app.coll.triggered` (`en.json:627`); failure toast "Collection failed: {error}" `app.coll.failed` (`en.json:618`) |
| Clear credentials (per collector) | `confirm()` "Remove all credentials for {name}? This will stop earnings collection for this service." `app.coll.clear_confirm` (`en.json:614`), then `DELETE /api/config/{slug}` (main.py:12740) | toast "{name} credentials cleared" `app.coll.cleared` (`en.json:616`); failure "Clear failed: {error}" `app.coll.clear_failed` (`en.json:615`) |
| Open or close one collector | native `<details>` toggle | |

**Words:** 31 static (intro 25). Closed list: 20 names + 20 badges, about 50 more. Hints inside the 20 collectors total 462 words (11 to 70 each; bytelixir is the longest at 70).
**Can do:** open a collector, type credentials, Save credentials (one button for all 20), Collect now, Clear credentials per configured collector.
**Explanation only:** the 25-word intro; each collector's hint.

---

### 5.2 Credential health (`#credential-health-card`)

settings.html:40-51. JS: `loadCredentialHealth` app.js:5511-5572.

| Element | id / class | Line |
|---|---|---|
| Card | `#credential-health-card`, `style="display:none;"` | :45 |
| Title | `settings.health.title` "Credential health" (`en.json:2294`) | :46 |
| Intro | `settings.health.desc` (`en.json:2293`) | :47-49 |
| Body | `#credential-health-body` | :50 |

Intro text, quoted: "How old each stored credential is, and when it is expected to stop working. Credential values are never shown here — only which one it is and how it is doing."

**Data** (`GET /api/credentials/health`, main.py:10206; rows built in `app/credential_expiry.py:63-170`): per stored credential `service` (slug), `field`, `age_hours`, `expected_lifetime_hours`, `status`, optional `expires_at`, optional `why` (English text from the server, not translated), optional `durable_alternative_missing[]`. One row per configured credential field. Rows are sorted worst first.

**Row** (`div.credential-health-item`, style.css:1134-1151):

- `div.credential-health-name`: slug (CSS `text-transform: capitalize`) and `span.optional` field name.
- `div.credential-health-detail`: age + lifetime + expiry, joined.
  - `app.credh.hours_old` "{n} hours old" / `app.credh.days_old` "{n, plural, one {# day} other {# days}} old" (`en.json:649`, `:644`). Days from 48 h.
  - `app.credh.lasts_hours` " · expected to last about {n, plural, ...hour...}" / `app.credh.lasts_days` (`en.json:651`, `:650`).
  - `app.credh.expires` " · expires {date}" (`en.json:646`).
- `div.credential-health-hint` with `why`, and one with `app.credh.durable` "A longer-lived credential exists for this service ({fields}) — setting it means not having to do this again." (`en.json:645`).
- `div.credential-health-actions`: `span.credential-health-status` with tone class, and for the owner when status is likely_expired or expiring_soon, `button.btn.btn-ghost.btn-sm[data-action=openCredentialModal][data-a1=<slug>]` `app.credh.update` "Update" (`en.json:654`).

**Statuses** (app.js:5504-5509):

| status | Label | Tone class |
|---|---|---|
| `likely_expired` | "Likely expired" `app.credh.likely_expired` (`en.json:652`) | `text-fail` |
| `expiring_soon` | "Expiring soon" `app.credh.expiring_soon` (`:647`) | `text-warn` |
| `no_known_expiry` | "No known expiry" `app.credh.no_known_expiry` (`:653`) | `muted` |
| `fresh` | "Fresh" `app.credh.fresh` (`:648`) | `text-ok` |

**States:** hidden while loading; hidden with no rows (index link hidden too); hidden on a load error (only `console.warn`, app.js:5519-5523); shown with rows.
**Words:** 32 static (intro 30) + rows.
**Can do:** Update on a failing row (see section 11: it opens nothing on this page).
**Explanation only:** the intro; each row is read-only status.

---

### 5.3 Device ids (`#set-identities`)

settings.html:53-67. JS: app.js:5608-5860 and 5995-6105. Docs: `docs/backup.md:282-339` ("The Device ids list").

| Element | id / class | Line |
|---|---|---|
| Title | `settings.identities.title` "Device ids" (`en.json:2298`) | :55 |
| Intro | `settings.identities.desc` (`en.json:2296`) | :56-58 |
| List | `#identities-container`, first "Loading..." | :59-61 |
| Add button | `button.btn.btn-secondary.btn-sm[data-action=openIdentityForm]` `settings.identities.add` "Add an id" (`en.json:2295`) | :63 |
| Download button | `button.btn.btn-ghost.btn-sm[data-action=exportIdentities]` `settings.identities.download` "Download all" (`en.json:2297`) | :64 |
| Add form slot | `#identity-add` | :66 |

Intro text, quoted (91 words): "The device names and ids CashPilot deployed each service with, per box. They stay here after you remove a service, so you can find the device at the provider or give a new box the same id. Each value is hidden until you show or copy it, and every show is written to the audit log. Passwords, keys and wallet seeds are never kept here. You can change the id a box runs, add an id CashPilot did not deploy with, and download the whole list after you enter your password."

**Data** (`GET /api/identities`, main.py:14091-14096, owner signed in, not an API key): per row `id`, `service`, `slug`, `label` (field), `key`, `masked`, `worker`, `worker_id`, `copy`, `kind` (`backup`, `manual`, or a deploy), `source` (`restore`, `pending`, `node`, ...), `status` (`active`, `retired`), `first_seen`, `last_seen`, `readable`, `pending`, `forgettable`, `changeable`.

**Row** (`identityRowsHtml`, app.js:5612-5659), `div.credential-health-item.identity-row[data-identity]`:

- Name: service + `span.optional` field label.
- Detail: `code.identity-value#identity-value-<id>` (masked value) · box, copy · state.
- State text: `app.ids.in_use` "In use", `app.ids.removed` "Removed", `app.ids.entered` "Entered by you", `app.ids.restored_here` "Restored here", `app.ids.restore_sent` "Restore sent here, no answer yet", `app.ids.downloaded` "Downloaded from here" (`en.json:813, 822, 803, 824, 823, 802`).
- Hint: `app.ids.seen` "First seen {first} · last seen {last}" (`:827`), times as `app.ids.utc` "{time} UTC" (`:837`) or `app.place.status_unknown` "unknown" (`:941`).
- Hint: `app.ids.by_node` "Reported by the node itself, not checked by CashPilot." (`:792`) or `app.ids.backup` "A backup file this CashPilot made or restored. Restoring it again needs no typed confirmation." (`:790`).
- Hint while held: `app.ids.unconfirmed_deploy` "The worker did not confirm this deploy, so the box may still start with this id. You can forget it {hours} h after the deploy." / `app.ids.unconfirmed_restore` "...this restore..." (`:832-833`). `{hours}` = 6 (app.js:5614).
- Buttons, readable row: `[data-action=revealIdentity]` "Show" `app.ids.show` (`:829`), `[data-action=copyIdentity]` "Copy" `app.ref.copy` (`:971`). Unreadable row: `span.muted` "Unreadable: the encryption key changed" `app.ids.unreadable` (`:834`).
- `[data-action=openIdentityChange]` "Change" `app.ids.change` (`:793`) when `changeable`.
- `[data-action=forgetIdentity]` "Forget" `app.attn.forget` (`:465`) when `forgettable`; `data-a2="pending"` on a held row.
- Change form slot `div.identity-change#identity-change-<id>` when `changeable`.

**Change form** (`identityChangeHtml`, app.js:5664-5679): label "New {label}" `app.ids.new_label` (`:817`); `button.btn-link[data-action=pickPreviousIdentity]` "Use one this service had before" `app.dep.pick_identity` (`:711`); `input#identity-change-value-<id>`; `div.identity-pick`; hint `app.ids.change_hint` (62 words, `:796`): "CashPilot makes the {service} container on {box} again with the new id, and changes nothing else. To the provider it is a new device. Its extra copies and its proxied copies on this box take ids made from the new one: running ones change now, and a stopped proxied copy keeps its old id until you add it to its proxy again."; buttons `[data-action=changeIdentity]` primary "Change", `[data-action=closeIdentityChange]` "Cancel" `app.cancel` (`:532`). One Change form open at a time; what you typed survives a list reload (app.js:5728-5736).

**Earlier ids offered** (`identityOffersHtml`, app.js:6036-6049): per offer `code` masked value · `app.ids.last_on` "last on {where}" (`:815`), `span.text-warn` `app.ids.in_use_on` "In use on {boxes}" (`:814`), button `[data-action=useIdentity]` "Use" `app.ids.use` (`:835`). None: `app.ids.no_offers` "CashPilot has no earlier id kept for this field." (`:818`).

**Add form** (`identityFormHtml`, app.js:5688-5717), opened into `#identity-add`: hint `app.ids.add_hint` (37 words, `:789`) "An id CashPilot did not deploy with, such as one from before you used CashPilot. It is kept here and offered when you deploy this service again. CashPilot does not treat it as running on the box."; `select#identity-add-service` "Service" `app.ids.service` (`:828`); `select#identity-add-worker` "Box" `app.ids.box` (`:791`); `input#identity-add-copy` number 1-32 "Copy" `app.ids.copy` (`:799`); `input#identity-add-label` with `datalist#identity-add-fields` "Field" `app.ids.field` (`:806`), placeholder "Pick one, or type a name" `app.ids.field_placeholder` (`:807`); `input#identity-add-value` "Id" `app.ids.id` (`:812`); buttons `[data-action=addIdentity]` primary "Save" `app.save` (`:1065`), `[data-action=closeIdentityForm]` "Cancel". With no service or no box: `app.ids.add_first` "Add a box and a service to CashPilot first." (`:788`).

**Actions**

| Action | Route | Messages |
|---|---|---|
| Show | `POST /api/identities/{id}/reveal` (main.py:14204), audit row first | value replaces the masked text; error toast "Could not show the id: {error}" `app.ids.show_failed` (`:830`) |
| Copy | same reveal route, then clipboard | error "Could not copy the id: {error}" `app.ids.copy_failed` (`:800`) |
| Forget | `confirm()` `app.ids.forget` "Forget this device id? CashPilot will not be able to show it or offer it again." or `app.ids.forget_pending` (`:808`, `:810`), then `DELETE /api/identities/{id}` (main.py:14283) | error "Could not forget the id: {error}" (`:809`) |
| Change | `confirm()` `app.ids.change_confirm` (`:794`), then `POST /api/identities/{id}/change` `{value, replace_existing: true}` (main.py:14316) | empty: "Type the new id first" `app.ids.type_first` (`:831`); notes toast `app.ids.change_notes` (`:797`); device-link toast `app.redeploy.link_device` (`:970`); success "{service} on {box} now runs with the new {label}" `app.ids.changed` (`:798`); error `app.ids.change_failed` (`:795`) |
| Use one this service had before | `GET /api/identities/reuse/{slug}?key=&worker_id=` (main.py:14415) | error `app.ids.offers_failed` (`:819`) |
| Use (an offer) | `confirm()` `app.ids.use_confirm` when the id runs elsewhere (`:836`), then the reveal route | error `app.ids.read_failed` (`:820`) |
| Add an id | `GET /api/services/available` (main.py:4305) + `GET /api/workers` (main.py:13520) | error `app.ids.form_failed` (`:811`) |
| Save (add form) | `POST /api/identities` `{slug, worker_id, copy, label, value}` (main.py:14108) | "Device id saved" `app.ids.saved` (`:826`); error `app.ids.save_failed` (`:825`) |
| Download all | `POST /api/identities/export`; the server asks for the password first (step-up, message `api.download_holds_every_device_id` `en.json:265`) | file `cashpilot-device-ids-YYYY-MM-DD.json`; toast "Downloaded {name}. It holds every id in full: keep it somewhere safe." `app.ids.exported` (`:805`); error `app.ids.export_failed` (`:804`) |

**States:** loading; empty `p.muted` `app.ids.empty` "No device ids yet. They appear here once you deploy a service that has one, or add one below." (`:802`); first-load error `p.text-fail` `app.ids.load_failed` (`:816`); reload error with a list already drawn: toast `app.ids.reload_failed` (`:821`), list stays.
**Words:** 98 static (intro 91). Add form +37. Change form +62.
**Can do:** Add an id, Download all, and per row Show, Copy, Change (with pick earlier id / Use), Forget.
**Explanation only:** the 91-word intro; the hints under each row.

---

### 5.4 Restore from a backup (`#set-restore`)

settings.html:69-79. JS: `restorePreviewHtml` app.js:6113-6151, `restoreFileChanged` :6164, `checkRestoreFile` :6171-6201, `submitRestore` :6203-6251. Docs: `docs/backup.md:106-206` and `:207` (command line).

| Element | id / class | Line |
|---|---|---|
| Title | `settings.restore.title` "Restore from a backup" (`en.json:2319`) | :71 |
| Intro | `settings.restore.desc_html` (`en.json:2317`) | :72-74 |
| File label | `label.form-label[for=restore-file]` `settings.restore.file` "Backup file" (`:2318`) | :75 |
| File input | `input#restore-file[type=file][accept=".cpbackup,application/octet-stream"]` | :76 |
| Check button | `button.btn.btn-ghost.btn-sm[data-action=checkRestoreFile]` `settings.restore.check` "Check file" (`:2316`) | :77 |
| Preview slot | `#restore-preview` | :78 |

Intro text, quoted (87 words): "Put a node identity or wallet back from a `.cpbackup` file made with a passphrase: Mysterium, ProxyBase or Anyone. The restore only creates a new container on a box that does not run the service, and never writes over a running one. To replace a running identity, download its backup first, then remove the service from that box on the dashboard and say yes when it asks to delete its data. Then restore here. Files sealed to a key, Storj and Sia use the command line steps." The last three words link to `https://geiserx.github.io/CashPilot/backup/#restore-a-backup-from-the-command-line`.

**Preview** (after Check file): `POST /api/restore/upload`, raw file body, `Content-Type: application/octet-stream` (main.py:14717). Data: `service`, `container`, `creates[] {volume, target}`, `known`, `history[] {what, worker, when}`, `live_on[]`, `runs_on[]`, `workers[] {id, name, ok, why, plain_http}`, `upload_id`. Shows:

- `app.restore.creates_html` "Restoring **{service}** creates a new container `{container}` with:" (`en.json:986`), list of `app.restore.volume_html` "volume `{volume}` at `{target}`" (`:1001`).
- `p.form-hint` `app.restore.never_overwrites` "It never writes over anything: the box must not run {service} and these volumes must not exist. The backup is written and read back before the container first starts." (`:993`).
- Known file: `app.restore.known` "This CashPilot knows this file:" (`:991`) + list `app.restore.history` "{what} on {box}, {when}" (`:990`).
- Unknown file: `p.text-warn` `app.restore.unknown_html` "This CashPilot did not make this file, so it cannot tell whose identity or wallet is inside. Restore only a file you made yourself. To go on, type **{service}**:" (`:1000`) + `input#restore-confirm`.
- `p.text-fail` `app.restore.live` (`:992`) when the identity runs somewhere.
- `p.text-warn` `app.restore.elsewhere` (`:989`) for an unknown file whose service runs elsewhere.
- `select#restore-worker` "Box" (`app.ids.box`); unusable boxes disabled with `({why})`; plain-HTTP boxes get `app.restore.plain_option` (`:998`); none: `app.restore.no_box` "No box" (`:994`).
- `input#restore-passphrase[type=password]` "Passphrase of the backup" `app.restore.passphrase` (`:996`).
- `input#restore-plain-http[type=checkbox]` `app.restore.plain_http` "Send the passphrase to a box on plain HTTP anyway: anyone on the network between can read it." (`:997`), only when a usable box is on plain HTTP.
- `button.btn.btn-primary.btn-sm[data-action=submitRestore][data-a1=<upload_id>]` "Restore" `app.restore.restore` (`:999`), disabled when no box is usable.

**Actions**

| Action | Route | Messages |
|---|---|---|
| Pick a file | none; clears the preview (app.js:6164-6169) | |
| Check file | `POST /api/restore/upload` | "Checking the file..." `app.restore.checking` (`:985`); error `p.text-fail` with the server message or `app.api.error_status` "Error {status}" (`:445`) |
| Restore | `POST /api/restore` `{upload_id, worker_id, passphrase, confirm_name?, allow_plain_http?}` (main.py:14793); the server asks for the password (step-up, `api.restoring_puts_node_identity_wallet` `en.json:361`) | file changed since the check: "The file chosen now is not the one checked. Press Check file again before you restore." `app.restore.not_checked` (`:995`); success `app.restore.done_started` or `app.restore.done_fenced` (`:988`, `:987`); error toast with the server message. Button disabled while it runs. Passphrase field cleared on send. Device ids list reloads. |

**States:** idle (file picker only); checking; preview (known / unknown / live elsewhere / no usable box); check error; restoring; done.
**Words:** 95 static (intro 87). Preview adds about 60 to 120.
**Can do:** pick a file, Check file, then pick a box, type the passphrase (and the service name for an unknown file), tick plain HTTP, Restore.
**Explanation only:** the 87-word intro; the never-overwrites hint.

---

### 5.5 Credential encryption key (`#set-key`)

settings.html:81-126. JS: `encryptionKeyStatusHtml` app.js:5866-5883, `loadEncryptionKey` :5885-5907, `toggleEncryptionKeyMove` :5909, `revealEncryptionKey` :5917-5932, `copyEncryptionKey` :5934-5944, `hideEncryptionKey` :5946-5951, `removeEncryptionKeyCopy` :5953-5964. Routes: `app/routers/credential_storage.py:58-102`. Docs: `docs/encryption-key.md` (guide linked as `https://geiserx.github.io/CashPilot/encryption-key/`).

| Element | id / class | Line |
|---|---|---|
| Title | `settings.key.title` "Credential encryption key" (`en.json:2313`) | :83 |
| Intro | `settings.key.desc` (`:2303`) | :84 |
| Status | `#key-status`, first `settings.key.loading` "Loading..." (`:2305`) | :85-87 |
| Action row | `div.settings-actions#key-actions` (filled by JS) | :88 |
| Steps panel | `#key-move` `hidden`, an `<ol>` of four steps | :89-125 |
| Step 1 text | `settings.key.step_reveal` (`:2312`) | :91 |
| Show button | `[data-action=revealEncryptionKey]` `btn-secondary btn-sm` "Show the key" `settings.key.reveal` (`:2306`) | :93 |
| Revealed box | `#key-revealed` `hidden` > `input#key-value.form-input[readonly]` (aria-label `settings.key.value_label` "Credential encryption key" `:2314`) + `[data-action=copyEncryptionKey]` "Copy" (`:2302`) + `[data-action=hideEncryptionKey]` "Hide" (`:2304`) | :95-101 |
| Step 2 text | `settings.key.step_file` (`:2309`) + shell block (3 lines: `mkdir -p secrets`, `chown 1000:1000`, `chmod 400`) + `settings.key.step_compose` "Then add the secret to your compose file:" (`:2308`) + compose YAML block (10 lines) + `settings.key.step_file_other_html` (`:2310`, links the guide) | :103-119 |
| Step 3 text | `settings.key.step_restart` "Recreate the UI container, so it reads the new setting:" (`:2311`) + `docker compose up -d cashpilot-ui` | :120-122 |
| Step 4 text | `settings.key.step_check` (`:2307`) | :123 |

Intro text, quoted (52 words): "One key decrypts every credential CashPilot stores. On a default install it sits in the data folder, next to the database it decrypts, so anyone with a copy of that folder can read your credentials. Keep the key outside the folder and a copy of the folder alone is no longer enough."

**Data** (`GET /api/settings/encryption-key`, never the key): `source` (`data`, `file`, `env`), `file`, `file_inside`, `data_file`, `data_copy` (`same`, `different`), `env_same`, `outside`, `removable`.

**Status lines** (each a `<p>`):

| Condition | Key and text |
|---|---|
| key in the data folder (default), or a file inside it | `app.key.status.data` "The key is in the data folder ({path}). A copy of that folder can decrypt every stored credential." (`en.json:863`) |
| from a file outside | `app.key.status.file` "The key comes from {path}, outside the data folder." (`:865`) |
| from the variable | `app.key.status.env` "The key comes from the CASHPILOT_ENCRYPTION_KEY environment variable, outside the data folder." (`:864`) |
| data source and the variable holds the same key | `app.key.env_same` (`:854`) |
| file outside and the same copy still in data | `app.key.copy_same` "A copy of the key is still in the data folder ({path}). Delete it, so a copy of the folder cannot decrypt your credentials." (`:853`) |
| an older, different key file still in data | `app.key.copy_different` (`:851`) |
| done | `app.key.outside` "Done: the data folder holds no copy of the key. Keep the key safe where it is now, because without it nothing can be decrypted." (`:857`) |

**Buttons drawn into `#key-actions`:** `removable` → `btn-primary btn-sm [data-action=removeEncryptionKeyCopy]` "Delete the copy in the data folder" `app.key.remove_copy` (`:859`). Not outside and not removable → `btn-secondary btn-sm [data-action=toggleEncryptionKeyMove]` "Move the key out of the data folder" `app.key.move` (`:856`). Outside → no button, `#key-move` stays hidden.

**Actions**

| Action | Route | Messages |
|---|---|---|
| Move the key out of the data folder | none; shows or hides `#key-move` | |
| Show the key | `POST /api/settings/encryption-key/reveal`; password first (step-up message, credential_storage.py:69), audit row | key in `#key-value`, selected; error "Could not show the key: {error}" `app.key.reveal_failed` (`:862`) |
| Copy | clipboard | "Key copied. Paste it into your secret store, then clear your clipboard." `app.key.copied` (`:850`); "Could not copy it. The key is selected: copy it by hand." `app.key.copy_failed` (`:852`) |
| Hide | none; clears and hides | |
| Delete the copy in the data folder | `confirm()` `app.key.remove_confirm` (`:858`), then `POST /api/settings/encryption-key/remove-data-copy`; password first (credential_storage.py:88-92) | "The copy in the data folder is deleted." `app.key.removed` (`:861`); error `app.key.remove_failed` (`:860`); a 409 says the file is the only copy (credential_storage.py:84-87) |

**States:** loading; load error `p.muted` "Could not load the key status: {error}" `app.key.load_failed` (`:855`); key in data (Move button); steps open; key revealed; file outside with a copy left (Delete button); different old copy; done.
**Words:** default view 81 (intro 52, status line about 19, button 7). Steps panel adds 138 words and three code blocks (3 + 10 + 1 lines).
**Can do:** Move (open steps), Show the key, Copy, Hide, Delete the copy.
**Explanation only:** the intro, the status lines, all four step texts and the three code blocks (copy-and-run instructions; nothing on the page runs them).

---

### 5.6 Earner credentials on each box (`#set-earner-secrets`)

settings.html:128-140. JS: `earnerSecretsHtml` app.js:5967-5983, `loadEarnerSecrets` :5985-5993. Route: `GET /api/settings/earner-secrets`, `app/routers/credential_storage.py:105-153`. Docs: `docs/earner-secrets.md` (guide linked as `https://geiserx.github.io/CashPilot/earner-secrets/`), variable reference `docs/configuration.md:82`.

| Element | id / class | Line |
|---|---|---|
| Title | `settings.earner_secrets.title` "Earner credentials on each box" (`en.json:2289`) | :130 |
| Intro | `p.settings-section-desc` `settings.earner_secrets.desc_html` (`:2287`) | :131 |
| Rows | `#earner-secrets-container`, first `settings.key.loading` "Loading..." | :132-134 |
| YAML block | `<pre><code>` 4 lines: `services:` / `cashpilot-worker:` / `environment:` / `- CASHPILOT_EARNER_SECRETS=file` | :135-138 |
| How-to | `p.settings-section-desc` `settings.earner_secrets.how` (`:2288`) | :139 |

Intro text, quoted (76 words): "Docker keeps a container's environment and command line in its settings, so `docker inspect`, a backup of Docker's folder and any tool with the Docker socket show every earner password in plain text. With `CASHPILOT_EARNER_SECRETS=file` on a worker, the earners it deploys get their passwords from a file that only the earner reads. Root on that machine can still read them, so this is not a wall against root. The guide lists which earners it covers."

How-to, quoted (32 words): "Set it on the worker, recreate the worker container, then redeploy each earner from the dashboard. Remove the line to undo it: the next redeploy puts the values back in the environment."

**Data, one entry per worker** (credential_storage.py:143-151):

| Field | Meaning |
|---|---|
| `worker_id` | worker id |
| `worker` | worker name |
| `status` | worker status (for example `online`). Returned, not shown today. |
| `mode` | `file`, `env`, `unavailable` (worker image has no start program), or `null` (worker older than this report) |
| `in_file` | earners of covered services whose credentials are in a file; `null` when the worker reports no container shapes (CashPilot-Desktop, phones, or `CASHPILOT_DRIFT_WARNINGS=off`) |
| `in_config` | covered earners whose credentials are still in Docker's container settings: these need a redeploy (or the setting first); `null` as above |

Only covered services count (`secret_env.covers`). Covered: Bitping, Earn.fm, Honeygain, IPRoyal Pawns, ProxyBase, ProxyRack, Repocket, Traffmonetizer, URnetwork, Sia hostd (`docs/earner-secrets.md:61-74`). Not covered: custom services, services with no secret, `docker.secrets_in_file: false`, Sia's wallet seed (`:76-84`).

**Row text.** Each worker is one `<p>`, built from one ICU message:

- With counts: `app.earner_secrets.row` (`en.json:754`): "{worker}: {mode, select, file {credentials go in a file} env {credentials go in the container settings} unavailable {this worker image cannot keep credentials in a file} other {this worker is too old to say}}. {in_file, plural, =0 {No earner has its credentials in a file} one {# earner has its credentials in a file} other {# earners have their credentials in a file}}, {in_config, plural, =0 {none still has them in its container settings.} one {# still has them in its container settings: redeploy it.} other {# still have them in their container settings: redeploy them.}}"
- Without counts: `app.earner_secrets.row_mode` (`en.json:755`): "{worker}: {mode, select, ...same four...}. It does not report its earners one by one."

**Live render with the owner's fleet** (see section 12), exactly as the page shows it today, 115 words:

> OPPO CPH1951 (5bdadbc5): this worker is too old to say. It does not report its earners one by one.
>
> geiserback: credentials go in the container settings. No earner has its credentials in a file, 8 still have them in their container settings: redeploy them.
>
> geiserct: this worker is too old to say. No earner has its credentials in a file, 7 still have them in their container settings: redeploy them.
>
> motorola one fusion+ (1414f972): this worker is too old to say. It does not report its earners one by one.
>
> watchtower: credentials go in the container settings. No earner has its credentials in a file, 8 still have them in their container settings: redeploy them.

**States**

| State | What shows | Key |
|---|---|---|
| Loading | "Loading..." | `settings.key.loading` (shared with the key section) |
| Error | `p.muted` "Could not load the key status: {error}" | `app.key.load_failed` (`en.json:855`), the key section's message |
| No workers | `p.muted` "No workers yet." | `app.earner_secrets.no_workers` (`:753`) |
| Per worker, mode | file / env / unavailable / too old (null) | inside `app.earner_secrets.row*` |
| Per worker, counts | known (0, 1, many for each of `in_file`, `in_config`) / unknown | `row` vs `row_mode` |

**The fix, in order** (`docs/earner-secrets.md:13-34`): add `CASHPILOT_EARNER_SECRETS=file` to the worker's environment; recreate the worker (`docker compose up -d cashpilot-worker`); redeploy each earner with a secret (its service page, **Redeploy**). Undo: remove the line, recreate the worker, redeploy. A worker "too old to say" needs a newer worker image before it can report.

**Words:** 113 static (title 5, intro 76, how-to 32) + 115 for the five live rows = 228 words of prose, plus the 4-line YAML block. No control at all.
**Can do:** nothing on the page. Follow the guide link. Every step (set the variable, recreate, redeploy) happens outside this section; redeploy happens on the dashboard.
**Explanation only:** all of it.

---

### 5.7 Environment (`#set-env`)

settings.html:142-151. JS: `renderEnvVars` app.js:6408-6468, `saveEnvSettings` :6481-6500. Route: `GET /api/env-info` (main.py:12534-12590). Reference: `docs/configuration.md:23-59`.

| Element | id / class | Line |
|---|---|---|
| Title | `settings.env.title` "Environment" (`en.json:2291`) | :144 |
| Intro | `settings.env.desc_html` (`:2290`) | :145-147 |
| Rows | `#env-vars-container`, first "Loading..." | :148-150 |

Intro text, quoted (79 words): "These are read from the environment when CashPilot starts. Variables set via Docker `-e` flags are shown locked; the rest can be stored here, but **a stored value does not take effect** — set it in your compose file or Unraid template and restart. Several of them cannot change at runtime at all: the session key signs logins already in use, the data directory is where the open database lives, and the fleet key is what enrolled workers already hold."

**Rows**, `div.kv-row` (240 px key column, style.css:2050-2058; one column on a phone, style.css:2211). Six variables, labels and descriptions in English from the server, not translated (main.py:12538-12566):

| Label | Key | Secret | Read-only | Default | Description |
|---|---|---|---|---|---|
| Fleet API Key | `CASHPILOT_API_KEY` | yes | no | "" | Bearer token for worker-to-UI authentication |
| Session Secret Key | `CASHPILOT_SECRET_KEY` | yes | forced yes | changeme-generate-a-random-secret | Secret for JWT session tokens — change from default for security |
| Hostname Prefix | `CASHPILOT_HOSTNAME_PREFIX` | no | no | cashpilot | Containers named {prefix}-{service} |
| Collect Interval (min) | `CASHPILOT_COLLECT_INTERVAL` | no | no | 60 | Minutes between automatic earnings collection |
| Data Directory | `CASHPILOT_DATA_DIR` | no | yes | /data | Directory containing the SQLite database |
| System Timezone | `TZ` | no | no | "" | Container timezone in IANA format (e.g. Europe/Madrid) |

Each row: `div.kv-key` (label + lock icon `svg.kv-lock` aria-label "Locked" `app.env.locked` `:759` when locked + one badge), `div.kv-sub.mono` (variable name), `input.form-input.env-var-input#env-<KEY>[data-env-key]` (password for secrets, disabled when locked), `div.form-hint` (description). Non-secret inputs use the description as placeholder too, so it can show twice.

Badges: "From env" `app.env.from_env` (`badge-deployed`, `:757`); "Read-only" `app.env.read_only` (`:764`); "Stored, not applied" `app.env.stored` (`badge-warning`, title `app.env.stored_title` "Stored in the database but NOT in use — these are read from the environment at startup", `:768-769`); "Default" `app.env.default` (`:756`); "Not set" `app.env.not_set` (`:762`).

After the rows: `div.form-hint.kv-note` `app.env.note_html` (52 words, `:763`): "These are read from the environment when CashPilot starts, so changing one here does not take effect. Set it in your `docker-compose.yml` (or Unraid template) and restart the container. Saving stores the value but nothing reads it back — the field is kept so an existing stored value stays visible rather than disappearing." Then `div.kv-actions.kv-actions-end` > `button.btn.btn-ghost[data-action=saveEnvSettings]` "Save anyway" `app.env.save_anyway` (`:765`), title `app.env.save_title` "Stores the value; it will not take effect until it is set in the environment and the container restarts" (`:766`).

**Actions:** Save anyway → `POST /api/config` `{data}` with every non-empty enabled input. Messages: "No changes to save" `app.env.no_changes` (`:760`); "Variables saved" `app.env.saved` (`:767`); "Save failed: {error}" `app.save_failed`.
**States:** loading; none: `p.block-empty` "No environment variable info available." `app.env.none` (`:761`); config failed (section 4); per row: from env (locked) / read-only (locked) / stored not applied / default / not set.
**Words:** 134 static (intro 79, note 52, button 2, title 1) + 56 in the six rows.
**Can do:** type into unlocked rows and Save anyway (which, by its own text, changes nothing that runs).
**Explanation only:** the intro, the note, the descriptions. The values themselves are read-only facts.

---

### 5.8 About and updates (`#set-about`)

settings.html:153-162. JS: `loadUpdateCard` app.js:6276-6296, `selectUpdateWorker` :6298-6301, `renderUpdateCard` :6312-6383, `runSelfUpdate` :6385-6406. Routes: `GET /api/update-info?worker_id=` (main.py:12479), `POST /api/update?worker_id=` (main.py:12505), `GET /api/workers`. Docs: `docs/configuration.md:270-297` (update check), `UPGRADING.md`.

| Element | id / class | Line |
|---|---|---|
| Title | `settings.about.title` "About and updates" (`en.json:2282`) | :155 |
| Intro | `settings.about.desc_html` (`:2281`) | :156-158 |
| Card | `#update-card-container`, first "Loading..." | :159-161 |

Intro text, quoted (86 words): "CashPilot checks GitHub for the latest release. The update button below (**Update to** a version, **Pull newest patches** or **Re-pull images**) runs the documented `docker compose pull && docker compose up -d` for you, from a one-shot helper container — it installs the newest patch of the image series your compose file pins. Moving to a newer series still means editing the image tags: read UPGRADING.md first, then update the UI host first and every worker after it. Installs not managed by Compose get the manual commands instead." (UPGRADING.md links to `https://github.com/GeiserX/CashPilot/blob/main/UPGRADING.md`.)

**Card** (`div.kv-row` lines):

- With more than one online Docker worker: "Server" `app.update.server` (`:1138`) + `select#update-worker-select.form-input.form-input-select` (worker names). Only online workers with a URL that are not CashPilot-Desktop (app.js:2265-2271, 6282).
- "Running" `app.update.running` (`:1137`): `current_display`.
- "Worker image" `app.update.worker_image` (`:1145`), "Dashboard image" `app.update.ui_image` (`:1142`), when known.
- "Latest release" `app.update.latest` (`:1124`): `vX.Y.Z` or `app.update.latest_unknown` "unknown — check disabled, not yet run, or GitHub unreachable" (`:1125`).
- Proxy policy warning when `proxy_policy_fix` is set: `p.form-hint.text-warn` `app.update.proxy_policy` (`:1131`), `pre.mono` with two commands, `app.update.proxy_copy` (`:1130`) + link.

**Action area**, one of:

| Condition | Shows |
|---|---|
| `updater_running` | `p.kv-note` `app.update.already_running` (`:1119`) |
| not Compose-managed | `p.kv-note.muted` `app.update.not_compose_html` (`:1128`) |
| patch available | `button.btn.btn-primary[data-action=runSelfUpdate]` "Update to {version}" `app.update.update_to` (`:1144`) + `app.update.patch_note` (`:1129`) |
| newer series only | button "Pull newest patches" `app.update.pull_patches` (`:1132`) + `app.update.behind_note` (`:1120`) + link "Read UPGRADING.md" `app.update.read_upgrading` (`:1135`) |
| up to date | button "Re-pull images" `app.update.repull` (`:1136`) + `app.update.newest_note` (`:1126`) or `app.update.unknown_note` (`:1143`) |
| dashboard updated by hand on that server | the note gets `app.update.worker_only_note` (`:1146`) |

Status span `#update-run-status.form-hint` next to the button.

**Actions**

| Action | Route | Messages |
|---|---|---|
| Pick a server | reloads the card for that worker | |
| Update / Pull / Re-pull | `confirm()` `app.update.confirm` or `app.update.confirm_worker` (`:1121-1122`), then `POST /api/update?worker_id=` | "Starting update…" `app.update.starting` (`:1141`); "Update started — the dashboard will restart. Reload this page in a minute." `app.update.started` (`:1139`) or `app.update.started_worker` (`:1140`); error: the server's 409 text, or "Update failed to start." `app.update.failed` (`:1123`) |

**States:** loading; no Docker worker online: `p.block-empty` `app.update.no_worker` "No Docker worker is online, so the install cannot be inspected or updated right now." (`:1127`); read error: `app.update.read_failed` / `app.update.read_failed_detail` (`:1133-1134`); the five action states above; proxy policy warning.
**Words:** 89 static (intro 86) + about 24 in the card when up to date, about 48 when a newer series exists.
**Can do:** pick a server, run the update button, follow UPGRADING.md.
**Explanation only:** the 86-word intro, the notes under the button.

---

## 6. The Import page, which must move into Settings

Today it is a separate page. The Settings index links to it like a section (settings.html:18).

| What | Where |
|---|---|
| Route `GET /import` | `app/routers/pages.py:104-112`, owner only like Settings |
| Template | `app/templates/import.html` (62 lines) |
| `<title>` | `import.title` "Import - CashPilot" (`en.json:2035`) |
| `<body data-page>` | `import` (import.html:4) |
| Page heading | `settings.index.import` "Import from another tool" (`en.json:2300`) |
| Script | `app/static/js/import.js` (243 lines), loaded only on this page (import.html:60-62). Handlers are `window.*` globals called by `data-action` through `delegate.js`. It uses `CP.api`, `CP.toast`, `CP.confirmPreflight` from app.js. |
| Routes | `app/routers/importers.py`: `POST /api/import/preview` (:93), `GET /api/import/drafts` (:207), `DELETE /api/import/drafts/{slug}` (:216). `app/main.py`: `POST /api/import/apply` (:15001), `POST /api/import/drafts/{slug}/deploy?worker_id=` (:15019). |
| Guides | `docs/migrate/money4band.md`, `cashfactory.md`, `internetincome.md`. Not linked from the page. |

There is no link back to Settings on the Import page.

### Lede

`p.page-lede` (style.css:1388) `import.lede` (`en.json:2019`, 40 words): "Coming from money4band, CashFactory or InternetIncome? Add the config files from that tool and CashPilot shows what it can bring over before it saves anything. Nothing in the files is run or fetched, and the files themselves are not kept."

### Step 1: `#import-input` (import.html:12-38)

| Element | id / class | Key and text |
|---|---|---|
| Title | `h3.settings-section-title` | `import.step1.title` "1. Your old config" (`:2031`) |
| Intro | `p.settings-section-desc` | `import.step1.desc_html` (`:2030`, 44 words): "money4band: `config/user-config.json` (or its `.env`). CashFactory: `.env`. InternetIncome: `properties.conf`, plus `earnapp.txt` and `proxyrack.txt` if you have them, so your linked devices come over. Up to 4 files, 64 KiB in total. The guides under "Moving from another tool" in the docs explain each tool." |
| Tool select | `select#import-source.form-input` | label `import.tool` "Tool" (`:2036`); options `auto` "Tell from the files" `import.tool.auto` (`:2037`), `money4band`, `cashfactory` "CashFactory", `internetincome` "InternetIncome" (brand names, not keys) |
| Files | `input#import-files[type=file][multiple]` | label `import.files` "Files" (`:2017`) |
| Paste | `textarea#import-paste[rows=8]` | label `import.paste` "Or paste one file here" (`:2022`) |
| Button | `button.btn.btn-primary[data-action=importPreview]` | `import.preview` "Check what comes over" (`:2023`) |
| Status | `span#import-status.muted` | |

### Step 2: `#import-preview`, `hidden` until a preview (import.html:40-49)

| Element | id / class | Key and text |
|---|---|---|
| Title | | `import.step2.title` "2. What CashPilot found" (`:2032`) |
| Notices | `#import-notices` | `p.setup-line` `import.read_as_html` "Read as **{tool}**." (`:2024`) + one `p.setup-line` per server notice |
| Table | `#import-rows.table-scroll` > `table.breakdown-table` | columns: tick, "Service" `import.col.service` (`:1989`), "Settings" `import.col.settings` (`:1990`) |
| Skipped | `#import-skipped` | `h4` "Not imported" `import.not_imported` (`:2021`) + list `code key: reason` |
| Button | `button.btn.btn-primary[data-action=importApply]` | `import.apply` "Save the ticked services" (`:1984`) |
| Status | `span#import-apply-status.muted` | |

**Row** (import.js:84-102): `input.import-pick[type=checkbox][data-import-slug]` (absent for unusable rows), service name + row state, one `div.import-field` per field, optional reason, optional extras.

Row states (`import.row.*`, `en.json:2025-2029`): `ready` "Ready", `missing_fields` "Needs a value", `invalid` "Check a value", `unusable` "Cannot bring over", `not_deployable` "Nothing to deploy".

Field states (`import.field.*`, `en.json:2010-2016`): `imported` "imported", `missing` "missing", `placeholder` "still the example value", `retype` "needs retyping (uses $ or quotes a shell would change)", `invalid` "not in the format this service needs". An imported secret shows "set" (`import.field.set`), a non-secret shows its value in `code`. A field not imported gets `input.form-input.import-extra` (password for secrets, `pattern` when given), placeholder = label + "(optional)" `import.field.optional` (`:2013`).

Extras (`import.extra.*`, `en.json:2005-2009`): `deployed` "already deployed by CashPilot", `draft` "an earlier import is saved; saving replaces it", `will_set` "earnings tracking will use this login too", `already_set` "earnings login already set; left as it is", `partly_set` "part of the earnings login is already in Settings; left as it is, finish it there".

No rows: `p.setup-line` "These files set up no service CashPilot can bring over." `import.none` (`:2020`).

**Preview data** (`POST /api/import/preview`, importers.py:93-119): `source`, `source_name`, `notices[]`, `rows[] {slug, name, state, selected, reason, fields[] {key, label, state, secret, required, pattern, value (non-secret only)}, collector, existing {deployed, draft}}`, `not_imported[] {key, reason}`. Secrets never come back.

### Step 3: `#import-drafts` (import.html:51-57)

| Element | id / class | Key and text |
|---|---|---|
| Title | | `import.step3.title` "3. Deploy what you imported" (`:2034`) |
| Intro | `p.settings-section-desc` | `import.step3.desc` (`:2033`, 41 words): "Saved imports stay here, encrypted, so you can deploy them to more workers later. Stop the old tool on a machine before you deploy there: two copies behind one connection earn as one, and a device id must not run twice." |
| Body | `#import-drafts-body`, first "Loading..." | |

Body (import.js:215-240): "Deploy to" `import.drafts.deploy_to` (`:1997`) + one `label.checkbox-label > input.import-worker[data-wid]` per online worker, or "No workers online." `import.drafts.no_workers` (`:2000`); `ul.import-drafts` with one `li[data-import-draft=<slug>]` per draft: name, `span.muted` `import.drafts.meta` "from {source}, {at} UTC; {keys}" (`:1999`), `[data-action=importDeploy]` "Deploy" (`:1995`), `[data-action=importForget]` "Forget" (`:1998`); then `[data-action=importDeployAll]` primary "Deploy all" (`:1996`). Empty: `p.setup-line.muted` "Nothing imported yet." `import.drafts.none` (`:2001`). Load error: `p.setup-line` with the error text. Drafts data: `slug`, `name`, `source`, `imported_at`, `keys[]`.

### Import actions

| Action | Route | Messages |
|---|---|---|
| Check what comes over | browser checks first: at most 4 files, 64 KiB total (import.js:10-11, 39-57); then `POST /api/import/preview` `{source, files[{name, content}]}` | "Add a file or paste one." `import.err.none` (`:2002`); "At most {max} files at a time." `import.err.too_many` (`:2004`); "The files add up to more than {kib} KiB." `import.err.too_big` (`:2003`); server errors in `#import-status`. A failed preview hides step 2. |
| Save the ticked services | `POST /api/import/apply` `{source, files, slugs, extra}` | "Check the files before saving." `import.apply.check_first` (`:1985`); "Tick at least one service." `import.apply.tick` (`:1988`); invalid extra field: native validity bubble; status "Saved {n, plural, ...}." `import.apply.saved` (`:1987`); toast "Imported {n, plural, ...}" `import.apply.imported` (`:1986`); then the drafts reload |
| Deploy (one draft) | preflight per worker (`GET /api/services/{slug}/preflight`, app.js:4099-4135, `confirm()` `app.dep.preflight_confirm` `en.json:714`), then `POST /api/import/drafts/{slug}/deploy?worker_id=` per ticked worker | "Tick at least one worker" `import.deploy.tick` (`:1994`); device link toast with `import.deploy.device_id` "Device id: {id}." (`:1991`); per failure "{slug} on worker {worker}: {error}" `import.deploy.failed` (`:1993`); "{slug} deployed to {n, plural, ...}" `import.deploy.done` (`:1992`). The shared-id and password prompts of `api()` apply. |
| Deploy all | the same, one draft after another | same |
| Forget | `confirm()` "Forget the imported settings for {slug}? Running containers are not touched." `import.forget.confirm` (`:2018`), then `DELETE /api/import/drafts/{slug}` | error toast with the server message |

**Words:** 160 static (lede 40, step 1 intro 44, step 3 intro 41).
**Can do:** pick tool, add files, paste, Check what comes over; tick services, fill missing fields, Save the ticked services; tick workers, Deploy, Deploy all, Forget.
**Explanation only:** the lede, the step 1 file list, the step 3 intro.

---

## 7. The Notifications slot

A parallel lane (`design/money-waiting-notifications`) designs a new Notifications section. Every layout leaves a clearly marked slot for it, labelled **Notifications (designed in the other PR)**. Do not design its contents. It needs a place in the index and in the page.

---

## 8. Shared dialogs, prompts and toasts

- **Password prompt (step-up).** `#stepup-modal` in `base.html:273-292`. Title "Confirm with your password" `base.stepup.title` (`en.json:1301`), message from the server or "Enter your password to continue." `app.stepup.default` (`:1096`), field "Password" `base.stepup.password` (`:1300`), buttons "Cancel" `base.cancel` (`:1269`) and "Confirm" `base.stepup.confirm` (`:1299`). `api()` opens it when a route answers `step_up_required` and sends the request again (app.js:26-35, 73-104). Used by: Download all (device ids), Show the key, Delete the copy, Restore, and deploys that need it.
- **Shared id question.** `api()` asks `confirm()` with the server message + "Deploy anyway?" `app.api.deploy_anyway` (`en.json:444`) when an id runs on another box (app.js:40-44).
- **Native `confirm()`** is used for: Clear credentials, Forget id, Change id, Use an id in use, Delete the key copy, Update, Forget import draft, preflight warnings.
- **Toasts** (`toast()` / `CP.toast()`): success, warning, error, info. Most results above are toasts.
- **Network failure** in any `api()` call: "Network error — is the server running?" `app.api.network_error` (`en.json:446`).

---

## 9. Links into this page that must keep working

| Link | From |
|---|---|
| `/settings#collector-<slug>` (opens that collector) | Setup wizard "Add your payout address" button, `app.js:3975`; handled at app.js:6574-6581 |
| `/settings?highlight=<slug>` | handled at app.js:7224-7226 |
| `/settings#set-restore` | Payouts page text `payouts.critical.desc_html`, `en.json:2194` |
| `/import` | `docs/migrate/cashfactory.md:30`, `docs/migrate/internetincome.md:49`, `docs/migrate/money4band.md:44,52`, and 76 translated doc files under `docs/i18n/` |
| Section names used in docs | "Settings > Restore from a backup" (`docs/backup.md:108`), "Settings > Device ids" (`docs/backup.md:286`), "Settings > Credential encryption key" (`docs/encryption-key.md:61`), "Settings > Earner credentials" (`docs/earner-secrets.md:31`), "Settings, About and updates" (`docs/getting-started.md:192`), "Update button in Settings" (`docs/configuration.md:158`), "Settings > Earnings collection" (about 15 service guides in `docs/guides/`, for example `grass.md:49`, `ocean.md:44`, `salad.md:50`) |

A rename or a move of a section changes these docs too.

---

## 10. Tests bound to the current markup

These tests read `settings.html`, `import.html` or the settings JS by id, class or function name. An implementation that changes the markup updates them:

`tests/test_frontend_wiring.py`, `tests/test_credential_storage_js.py`, `tests/test_restore_from_ui.py`, `tests/test_identity_change.py`, `tests/test_tracking_without_deploying.py`, `tests/test_upgrading_3_0_steps.py`, `tests/test_getting_started_matches_compose.py`, `tests/test_beads_batch_12.py`, `tests/test_beads_batch_49.py`, `tests/test_beads_batch_71.py`, `tests/test_importers.py`, `tests/test_compose_passes_ui_settings.py`.

---

## 11. Facts found while reading the code

Recorded as found. No fix is proposed here.

1. **Credential health "Update" opens nothing on Settings.** The button calls `openCredentialModal` (app.js:5567, 2818), which opens `#cred-modal`. That modal exists only in `dashboard.html:165`. `openModal` does nothing when the element is missing (app.js:244-247).
2. **`#settings-currency` does not exist.** `populateCurrencyDropdown` (app.js:7044-7046) and the top-bar sync (app.js:7190-7191) look for it; settings.html has no currency control. The currency is chosen only in the top bar (`#topbar-currency`).
3. **The earner credentials section borrows the key section's strings.** Its loading line is `settings.key.loading` (settings.html:133) and its error is "Could not load the key status: {error}" `app.key.load_failed` (app.js:5991).
4. **Worker status is returned but not shown.** `/api/settings/earner-secrets` returns `status` per worker (credential_storage.py:147); the row text does not use it.
5. **Environment labels and descriptions are English only.** They come from `main.py:12538-12566`, not from `en.json`. Collector field labels are built in English the same way (`main.py:12627`). Credential health `why` texts are English from the server (`credential_expiry.py:126-139`, `collectors/__init__.py` lifetimes table).
6. **"Fleet API Key" description differs from the docs.** The row says "Bearer token for worker-to-UI authentication" (main.py:12539). `docs/configuration.md:32` calls `CASHPILOT_API_KEY` the shared enrolment key that reads nothing.
7. **The Import page names the guides but does not link them.** `import.step1.desc_html` ends "The guides under "Moving from another tool" in the docs explain each tool." with no link.
8. **Import deploy errors name the worker by id.** `import.deploy.failed` gets `worker: wid` (import.js:190).
9. **`toggleEnvSecret` is exported but nothing calls it** (app.js:6470, 7285).
10. **Only `en.json` exists at this base.** `app/i18n/` holds `en.json` alone at `aa543a48`; other locales arrive from another lane. Every new string still goes into `en.json` as a key.
11. **Two "Loading..." keys** carry the same text: `settings.loading` (`en.json:2315`) and `settings.key.loading` (`:2305`).
12. **The index has no current-section state**, only hover (style.css:1873-1877).
13. **One Save button for 20 collectors.** "Save credentials" sends every non-empty field of every collector, open or closed (app.js:6584-6593).

---

## 12. Realistic data for the mockups

Use these values so every design shows the same fleet.

- **Version:** CashPilot v3.1.0. **Header total:** $52.07.
- **Boxes:** `watchtower`, `geiserback`, `geiserct` (Unraid or Linux servers, Docker workers with a URL), and two Android phones: `OPPO CPH1951 (5bdadbc5)`, `motorola one fusion+ (1414f972)`. The phones have no URL, so the About card does not list them (app.js:2265-2266).
- **Earners:** honeygain, earnfm, mysterium, packetstream, traffmonetizer, repocket, proxyrack, storj, bitping, bytelixir, iproyal, proxybase, proxylite.

**Earner credentials, per box:**

| Box | mode | in a file | in container settings | Row today |
|---|---|---|---|---|
| OPPO CPH1951 (5bdadbc5) | null (too old) | unknown | unknown | `row_mode` |
| geiserback | `env` | 0 | 8 | `row` |
| geiserct | null (too old) | 0 | 7 | `row` |
| motorola one fusion+ (1414f972) | null (too old) | unknown | unknown | `row_mode` |
| watchtower | `env` | 0 | 8 | `row` |

The fix: set `CASHPILOT_EARNER_SECRETS=file` on the worker, recreate the worker container, then redeploy each earner. Remove the line to undo.

**Earnings collection, plausible badges** for the owner's earners that have a collector: honeygain, earnfm, mysterium, packetstream, traffmonetizer, repocket, proxyrack, bitping, bytelixir, iproyal "Configured"; storj "Configured" (optional field only); the other nine collectors "Not configured". Bytelixir needs `session_cookie` plus the optional `remember_web` and `xsrf_token`.

**Credential health, plausible rows** (lifetimes from `app/collectors/__init__.py`): bytelixir `session_cookie` (2 h lifetime; "No known expiry" when the remember-me cookie is saved, with the "re-created on every run" reason); traffmonetizer `token` (a JWT with its own expiry, for example "Expiring soon · expires" a date); packetstream `auth_token` "No known expiry"; honeygain `password` "No known expiry".

**Device ids, plausible rows:** proxyrack device UUID on watchtower "In use"; proxybase device ID on geiserback "In use"; mysterium node identity "Reported by the node itself"; one removed proxyrack UUID from an older box; one `.cpbackup` SHA-256 row "Downloaded from here".

**Encryption key:** default install, "The key is in the data folder (/data/.fernet_key)…", Move button shown.

**Environment:** `CASHPILOT_API_KEY` from env (locked); `CASHPILOT_SECRET_KEY` read-only; `CASHPILOT_HOSTNAME_PREFIX` `cashpilot` default; `CASHPILOT_COLLECT_INTERVAL` `60` default; `CASHPILOT_DATA_DIR` `/data` read-only; `TZ` `Europe/Madrid` from env.

**About:** three servers in the select (watchtower, geiserback, geiserct); Running v3.1.0; Latest release v3.1.0; "Re-pull images".

---

## 13. Word count per section

| Section | Words on first view | Of that, intro paragraphs | Hidden or conditional text | Controls on first view |
|---|---|---|---|---|
| Index | 23 | 0 | | 9 links |
| Earnings collection | 31 + about 50 (20 closed headers) | 25 | 462 in hints inside the 20 collectors | 20 toggles, 2 buttons |
| Credential health | 32 + rows | 30 | | 0 to n Update buttons |
| Device ids | 98 + rows | 91 | add form 37, change form 62, row hints | 2 buttons + up to 4 per row |
| Restore from a backup | 95 | 87 | preview about 60 to 120 | 1 file input, 1 button |
| Credential encryption key | 81 | 52 | steps 138 + 3 code blocks | 1 button |
| Earner credentials on each box | 228 (live fleet) | 108 (intro 76 + how-to 32) | | **0** |
| Environment | 190 (134 + 56 in rows) | 131 (intro 79 + note 52) | | 4 inputs, 1 button |
| About and updates | about 113 | 86 | proxy policy warning, behind note | 1 select (several servers), 1 button |
| Import page (separate today) | 160 | 125 (lede 40 + step 1 44 + step 3 41) | preview table, drafts | 1 select, 1 file input, 1 textarea, 1 button; then ticks, Save, worker ticks, Deploy, Deploy all, Forget |

Settings today, all sections open as they load, about 890 words before any row data. With Import added, about 1,050.

---

## 14. Checklist: everything that must stay reachable

Every design ticks every line. "Reachable" means one click or one disclosure away, on the Settings page.

**Page**
- [ ] 1. A way to every section, including Credential health when it has rows, and the Notifications slot.
- [ ] 2. Page-wide load error message (`app.settings.load_failed*`).
- [ ] 3. Deep links `#collector-<slug>`, `?highlight=<slug>`, `#set-restore` still land on the right place; `/import` still reaches the import flow.

**Earnings collection**
- [ ] 4. Per collector: name, status badge (Configured / Incomplete / Not configured), hint, every field, optional marker, "set — leave blank to keep" placeholder.
- [ ] 5. Save credentials.
- [ ] 6. Collect now, with its running / triggered status.
- [ ] 7. Clear credentials per configured collector, with its confirm.
- [ ] 8. Empty state "No collectors available."

**Credential health**
- [ ] 9. Per credential: service, field, age, expected lifetime, expiry date, status (4 tones), reason, durable-alternative hint.
- [ ] 10. Update on a failing row.
- [ ] 11. Hidden when there are no rows.

**Device ids**
- [ ] 12. Per id: service, field, masked value, box, copy, state, first and last seen, node / backup / unconfirmed hints, unreadable state.
- [ ] 13. Show, Copy, Change (with "Use one this service had before" and Use), Forget (both confirm texts).
- [ ] 14. Add an id (service, box, copy, field with suggestions, id; Save, Cancel; "Add a box and a service first").
- [ ] 15. Download all (password prompt).
- [ ] 16. Empty, load error, reload error.

**Restore**
- [ ] 17. Which services it covers, the create-only rule, how to replace a running identity, the command-line link for key-sealed files, Storj and Sia.
- [ ] 18. File picker, Check file, checking state, error.
- [ ] 19. Preview: container and volumes, never-overwrites rule, known file history or unknown file with typed name, live-elsewhere and runs-elsewhere warnings, box select with disabled reasons and plain-HTTP marks, passphrase, plain-HTTP checkbox, Restore (disabled with no usable box).
- [ ] 20. Done messages (started / waits for LAN fence), not-checked error.

**Credential encryption key**
- [ ] 21. Why the key matters (the intro's facts).
- [ ] 22. Where the key comes from now: every status line.
- [ ] 23. Move the key: Show the key (password), Copy, Hide; the file, compose and restart steps with their code; the secret-manager guide link; the "come back to check" step.
- [ ] 24. Delete the copy in the data folder (confirm + password).
- [ ] 25. Loading and load error.

**Earner credentials on each box**
- [ ] 26. What the setting protects against and what it does not (root still reads them); guide link.
- [ ] 27. Per box: name, mode (file / env / image cannot / too old), count in a file, count still in container settings, or "does not report its earners one by one".
- [ ] 28. What to do: the variable line (`CASHPILOT_EARNER_SECRETS=file`), recreate the worker, redeploy each earner; how to undo.
- [ ] 29. Loading, error, "No workers yet."

**Environment**
- [ ] 30. Per variable: label, variable name, lock, badge (From env / Read-only / Stored, not applied / Default / Not set), value or secret state, description.
- [ ] 31. The fact that a value saved here does not take effect, and where to set it instead.
- [ ] 32. Save anyway, with its no-changes / saved / failed messages.
- [ ] 33. Empty state.

**About and updates**
- [ ] 34. Server select (several Docker workers), running version, worker image, dashboard image, latest release or unknown.
- [ ] 35. The update button in its three labels, its note, the worker-only note, the UPGRADING.md link, the already-running and not-Compose states.
- [ ] 36. Proxy policy warning with its two commands and link.
- [ ] 37. Confirm, starting, started, failed; no-worker and read-error states.

**Import (moved into Settings)**
- [ ] 38. What it does and what it does not do (nothing run or fetched, files not kept).
- [ ] 39. Which files per tool, the 4-file and 64 KiB limits; the guides.
- [ ] 40. Tool select (auto + three tools), files, paste, Check what comes over, and the three input errors.
- [ ] 41. Preview: "Read as", notices, rows with tick, state, fields with their state and fill-in inputs, reason, extras; "Not imported" list; "no service" state.
- [ ] 42. Save the ticked services, with check-first / tick / saved messages.
- [ ] 43. Drafts: Deploy to (online workers or "No workers online."), each draft with source, time and keys, Deploy, Forget (confirm), Deploy all; "Nothing imported yet."; the stop-the-old-tool warning.

**Notifications**
- [ ] 44. A marked slot labelled "Notifications (designed in the other PR)", empty of design.
