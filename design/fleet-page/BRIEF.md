# Fleet page, lower half: design brief

This brief is the one source for every design of the lower half of the Fleet page. It lists what the page has today, and nothing else. It holds no design opinions.

The facts come from `main` at `aa543a48`. Paths are relative to the repository root. `fleet.html` means `app/templates/fleet.html`. `en.json` means `app/i18n/en.json`.

## 0. Scope and how to build a mockup

### 0.1 In scope

Three blocks, in page order, after the Boxes table:

1. **Running costs**: `fleet.html:52-75`, rendered by `loadFleetEconomics()` at `fleet.html:284-503`.
2. **Proxies**: `fleet.html:77-126`, rendered by the second script at `fleet.html:1300-1542`. Owner only.
3. **Add a box**: `fleet.html:128-165`, script at `fleet.html:181-226` and `fleet.html:1016-1033`, `1252-1293`.

Out of scope, and must stay as it is: the four stats at the top (`fleet.html:9-33`) and the Boxes table (`fleet.html:36-44`, `renderWorkers()` at `fleet.html:530-650`).

### 0.2 Files and rendering

- Put each design in `design/fleet-page/<dir>/index.html`.
- Link the real stylesheet relatively: `<link rel="stylesheet" href="../../../app/static/css/style.css">`.
- Set `<html data-theme="classic">`. Classic night is the default theme (`app/themes.json`). It gives the pink primary buttons (`--accent: #f472b6`) and the blue-black surfaces (`style.css:2294-2317`). Without the attribute, `.btn-primary` is light grey (`style.css:1659`).
- Wrap the content in `<main class="page-content">` (`style.css:1384`: max width 1600 px, padding 18 px 24 px). Every `section` gets `margin-bottom: 28px` (`style.css:1413`).
- Fonts: IBM Plex Sans and IBM Plex Mono (`--font-ui`, `--font-mono`, `style.css:66-67`). The app loads them from Google Fonts (`app/templates/base.html:15`). A mockup may load the same URL.
- Add your own `<style>` only for new parts.
- Render on the MacMini, never on the MacBook. The command is in the task text. `shoot.cjs` opens the file in Chromium with `colorScheme: "dark"`, a 900 px high viewport and a full-page screenshot.

### 0.3 Design tokens in use (Classic night)

| Token | Value | Used for |
|---|---|---|
| `--bg-primary` | `#0b0b14` | page |
| `--bg-secondary` / `--bg-card` | `#11111d` | table heads, cards |
| `--bg-tertiary` | `#171726` | default button |
| `--bg-hover` | `#1d1d2f` | row hover |
| `--bg-input` | `#08080f` | inputs, env block |
| `--border-color` / `--border-light` / `--border-strong` | `#25233a` / `#322f4b` / `#4b4670` | hairlines |
| `--text-primary` / `--text-secondary` / `--text-muted` | `#e8e6f0` / `#bdb6cf` / `#a59cb5` | text |
| `--accent` | `#f472b6` | primary buttons, focus of links |
| `--accent-secondary` | `#22d3ee` | focus outline |
| `--success` / `--warning` / `--error` | `#46b37f` / `#e0a53c` / `#f06a5f` | state only |
| `--fs-1` ... `--fs-5` | 14 / 15 / 16 / 18 / 23 px | type scale; nothing under 14 px |
| `--radius` | 2 px | every corner |

The stylesheet header says: "Colour carries state and nothing else: ok, warn, fail" (`style.css:10-12`).

### 0.4 Shared classes these blocks use today

| Class | Rule | Where |
|---|---|---|
| `.block-head`, `.block-title`, `.block-meta` | flex row, title 16 px 600, meta 15 px muted, 1 px bottom border | `style.css:1398-1404` |
| `.power-settings` | `display:flex; flex-wrap:wrap; gap:12px; align-items:flex-end; padding:10px 0; border-bottom` | `style.css:1826-1827` |
| `.add-worker` (a `<details>`) | top border, summary 600 weight, body `max-width: 90ch` | `style.css:1836-1839` |
| `.fleet-table` | full width table, top-aligned cells, `overflow-wrap:anywhere` | `style.css:1567-1598`, `1782-1805` |
| `.economics-row` | grid `minmax(0,1fr) auto`, bottom border | `style.css:1155-1164`, `1829-1830` |
| `.economics-figures` | mono, 15 px, `white-space:nowrap`, flex gap 8 px | `style.css:1167-1176` |
| `.economics-service-row` | flex `space-between`, 14 px | `style.css:1194-1197` |
| `.economics-note` | 15 px muted, `max-width:72ch` | `style.css:1198` |
| `.econ-heat`, `.heat-form`, `.heat-months` | details plus a wrapping flex form | `style.css:1179-1186` |
| `.env-block`, `#worker-env`, `.env-actions`, `.env-fallback` | input-coloured box, pre-wrap mono, action row | `style.css:1840-1843`, `1994-1995` |
| `.btn`, `.btn-sm`, `.btn-primary`, `.btn-ghost`, `.btn-danger`, `.btn-link` | 28 px / 24 px high; danger is red text on no fill | `style.css:1653-1670` |
| `.form-label`, `.form-input`, `.form-hint`, `.form-input-price` (9 rem), `.form-input-code` (5.5 rem) | | `style.css:1674-1675`, `1986-1987` |
| `.badge`, `.badge-deployed`, `.badge-category` | text with no pill | `style.css:1628-1634` |
| `.flag`, `.flag-warn` | small bordered tag | `style.css:1808-1809` |
| `.cell`, `.cell-ok`, `.cell-warn`, `.cell-fail`, `.cell-unknown` | 18x14 px status square | `style.css:1500-1506` |
| `.text-ok`, `.text-warn`, `.text-fail`, `.muted`, `.mono`, `.num` | state text colours | `style.css:1354-1356`, `1973-1974` |

Facts about the layout today:

- The proxy form and the copy form reuse `.power-settings` (`fleet.html:91`, `117`). That class is the flex row of the electricity price. Each field keeps the width of its own input class, so the fields have mixed widths.
- The proxy form, the copy form and Add a box all use `<details class="add-worker">` (`fleet.html:89`, `115`, `128`).
- `.fleet-proxies` and `.fleet-economics` have no CSS rule of their own.
- PR #940 uses the class `badge-warning` (section 2.9). `style.css` has no rule for it on `main`.

### 0.5 Roles and refresh

- `user.r == 'owner'` gates the whole Proxies block (`fleet.html:77`, `126`, `1300`, `1542`). A viewer never sees it.
- Running costs shows for every role. The heat form and the device watts form show only for the owner (`fleet.html:370`, `445`).
- The electricity price inputs and Save show for every role (`fleet.html:58-72`). The save calls `POST /api/config`, which needs the owner (`app/main.py:12675-12677`). A viewer's save gets an error toast.
- In Add a box, Reveal and Copy show only for the owner (`fleet.html:146-149`).
- `loadFleet()` runs every 60 s (`fleet.html:1297`). It calls `loadFleetEconomics()` and `loadPowerSettings()` (`fleet.html:259-260`).
- The Proxies script has its own `load()`, every 60 s (`fleet.html:1538-1539`).
- Both refreshes re-render with `innerHTML`. Running costs skips a refresh while the user edits a device watts form or a heat form (`fleet.html:291-300`). The copy form keeps the box choice across a refresh (`fleet.html:1374-1377`). On `main` it does not keep the service or the proxy choice (`fleet.html:1378`, `1386`).

### 0.6 Real data for every mockup

From the owner's v3.1.0 screenshots, dark theme, about 1700 px wide.

- Header total: **$52.07**.
- Boxes: watchtower, geiserback, geiserct, plus two phones.
- Electricity: price `0,17`, currency `EUR`. Money shows in USD (`$`).
- `economics.summary` (block meta): "Costs are known for 0 of 5 machines."

Machines (`economics.machines[]`, all `kind: "machine"`, `verdict: "unknown"`, `monthly_cost: null`):

| machine | monthly_gross | summary (`machine_economics.earned_last_month_without_cashpilot`, `missing=power_draw`) |
|---|---|---|
| OPPO CPH1951 (5bdadbc5) | 1.90 | "OPPO CPH1951 (5bdadbc5) earned 1.90 last month. Without this machine's power draw CashPilot cannot say whether that covers the electricity, and guessing would be worse than not saying." |
| geiserback | 15.95 | same sentence with geiserback, 15.95 |
| geiserct | 15.38 | same sentence with geiserct, 15.38 |
| motorola one fusion+ (1414f972) | 1.90 | same sentence |
| watchtower | 15.95 | same sentence |

Each machine row also shows a **Heat** disclosure for the owner, because each has a `heat_prefix` and is not `not_metered` (`fleet.html:368-391`).

Per service (`net.services[]` with `cost_attributable: true`), earned − cost = net:

| platform | gross | cost | net | negative |
|---|---|---|---|---|
| bitping | 0.08 | 0.88 | −0.80 | yes |
| bytelixir | 1.12 | 2.03 | −0.92 | yes |
| earnfm | 4.32 | 0.88 | 3.43 | no |
| honeygain | 18.76 | 0.88 | 17.88 | no |
| iproyal | 0.03 | 0.88 | −0.86 | yes |
| mysterium | 6.40 | 1.04 | 5.36 | no |
| packetstream | 1.62 | 0.88 | 0.74 | no |
| proxyrack | 0.60 | 0.91 | −0.31 | yes |
| repocket | 0.15 | 0.88 | −0.72 | yes |
| storj | 1.12 | 0.79 | 0.33 | no |
| traffmonetizer | 6.72 | 0.88 | 5.84 | no |

The per-service costs exist while every machine cost is unknown. They come from `/api/earnings/net`, which falls back to a 65 W estimate or a host TDP when no watts are typed (`docs/fleet.md:241`, `app/main.py:10500-10543`).

Proxy (`proxies[0]`):

- `name`: "geiserct exit node (Tailscale)"
- `kind`: `tailscale`, `exit_node`: `100.64.0.22`
- `last_exit_ip`: `203.0.113.71`, `last_country`: `ES`, `rotating`: false
- `cap.enabled`: false → "No cap"
- `copies`: 7, all on watchtower, all `running` via `203.0.113.71 · ES`: earnfm, packetstream, proxybase, proxylite, proxyrack, repocket, traffmonetizer.
- `exits[0]`: `{exit_ip: "203.0.113.71", known: true, shared: true, members: [those 7]}`.

---

## 1. Running costs

### 1.1 Elements

| Element | id / class | Line | Notes |
|---|---|---|---|
| Section | `#fleet-economics-card`, `.fleet-economics` | `fleet.html:52` | Starts `display:none`. |
| Title | `.block-title` | `fleet.html:54` | `fleet.costs.title` "Running costs" |
| Quality line | `#fleet-economics-quality`, `.block-meta` | `fleet.html:55` | Text = `economics.summary` (`fleet.html:497-499`) |
| Settings row | `#power-settings`, `.power-settings` | `fleet.html:58` | |
| Price input | `#power-price`, `.form-input-price`, `type=number step=0.001 min=0`, placeholder `0.30` | `fleet.html:60-62` | Label `fleet.costs.price` "Electricity price per kWh" |
| Currency input | `#power-currency`, `.form-input-code`, `maxlength=4`, placeholder `EUR` | `fleet.html:65-66` | Label `fleet.costs.currency` "Currency" |
| Save | `#power-save`, `.btn-primary.btn-sm` | `fleet.html:68` | `fleet.save` "Save" |
| Help | `#power-help`, `.muted` | `fleet.html:69-71` | `fleet.costs.help` "Your tariff, as it appears on your bill. Figures below are converted to USD." |
| Body | `#fleet-economics-body` | `fleet.html:74` | Machine rows, then the per-service block and notes |

Money is drawn by `CP.formatCurrency` (`app/static/js/app.js:6659`), in the viewer's display currency. `null` money shows as `—` (`fleet.html:324`).

### 1.2 Actions and APIs

| Action | Handler | API | Validation and messages |
|---|---|---|---|
| Load price | `loadPowerSettings()` `fleet.html:1057-1072` | `GET /api/config` | Reads `power_price_per_kwh`, falls back to `electricity_price_per_kwh`; reads `power_currency`. A failure only logs. |
| Save price | `savePowerSettings()` `fleet.html:1074-1098`, bound at `1100` | `POST /api/config` body `{data:{power_price_per_kwh, power_currency}}` | Empty: warning toast `fleet.costs.enter_price` "Enter your price per kWh first". Not a number ≥ 0: error `fleet.costs.bad_price` "That is not a price per kWh". Currency empty → `EUR`, uppercased. Success `fleet.costs.saved` "Electricity price saved", then reload. Failure `fleet.save_failed` "Could not save: {error}". |
| Load figures | `loadFleetEconomics()` `fleet.html:284-503` | `GET /api/fleet/economics` (`app/main.py:11227`) and `GET /api/earnings/net?days=30` (`app/main.py:10333`) | A failure of the first leaves the card hidden ("unknown is not free", `fleet.html:308-311`). A failure of the second hides only the per-service block. |
| Save device watts | submit on `#fleet-economics-body` `fleet.html:1102-1125` | `POST /api/config` `{data:{power_device_<slug>_watts}}` | Toast `fleet.econ.device_saved` "Device power saved". Button disabled and input read-only while saving. |
| Save heat | `saveHeat()` `fleet.html:1127-1165` | `POST /api/config` `{data:{<prefix>_heat, <prefix>_heat_cop, <prefix>_heat_price, <prefix>_heat_months}}` | Source not `none` and no month: `fleet.heat.pick_months` "Pick the months you heat". Heat pump COP not 1-10: `fleet.heat.bad_cop`. Fuel price not > 0: `fleet.heat.bad_price`. Success `fleet.heat.saved` "Heat setting saved". The server also refuses a source with no months (`app/main.py:12372`). |
| Show COP / fuel field | change on `.heat-source` `fleet.html:1168-1173` | none | COP field only for `heat_pump`, fuel price only for `fuel`. |

Per-machine watts, "Dedicated" and "Not billed per kWh" are entered in the Boxes table, not here (`fleet.html:607-623`, saved by `fleet.html:1179-1221`). `docs/fleet.md:235` says: "Set each machine's wall draw in the Boxes table." Only a tracked **device** row has a watts input inside Running costs.

### 1.3 Data per machine row

From `GET /api/fleet/economics` → `machines[]` (`app/main.py:11320-11372`, `app/machine_economics.py:92-219`):

| Field | Shown as | Line |
|---|---|---|
| `machine` | name, mono 600 | `fleet.html:431` |
| `kind` | `"device"` adds a muted "Device" (`fleet.econ.device`) | `fleet.html:426`, `431` |
| `summary` | the sentence under the name | `fleet.html:432` |
| `monthly_gross` | first figure; title `fleet.econ.gross` "Gross earnings per month", or `fleet.econ.accrued` when `gross_basis == "accrued"` | `fleet.html:427`, `436` |
| `monthly_cost` | `− cost`; only when not null | `fleet.html:436-438` |
| `heat_credit` | `+ credit`; only when not null | `fleet.html:438-440` |
| `monthly_net` | `= net`, red (`.text-fail`) when `verdict == "losing_money"` | `fleet.html:441-443` |
| `verdict` | `losing_money`, `marginal`, `profitable`, `unknown`, `not_metered` (`machine_economics.py:52-56`) | |
| `break_even_tariff` `{price_per_kwh, currency}` | line `fleet.econ.break_even_html` "Earns more than its electricity below **{price} {currency}/kWh**{yours}{heating}" | `fleet.html:330-343` |
| `tariff_price_per_kwh`, `tariff_currency` (top level) | `{yours}` = `fleet.econ.you_pay` " (you pay {price})" when the currencies match | `fleet.html:333-335` |
| `break_even_tariff_heating`, `heat_covers_all_in_season` | `{heating}` = `fleet.econ.heat_below_html` or `fleet.econ.heat_covers_all` | `fleet.html:336-341` |
| `heat`, `heat_credit` | line `fleet.heat.credit_line` "Heat credit {money} a month: its heat replaces {source} in {months}" | `fleet.html:363-367` |
| `heat_prefix`, `heat_settings` | the Heat form (1.4) | `app/main.py:12354-12366` |
| `expected` (device rows) | line `fleet.expected.line_html` or `fleet.expected.none` | `fleet.html:402-421` |
| `slug`, `watts` (device rows) | device watts form | `fleet.html:445-452` |

The figures sit in a second grid column, right of the text, with `white-space:nowrap` (`style.css:1155-1176`). Under 760 px they go under the text (`style.css:2209-2210`).

### 1.4 Heat form (owner, per machine)

Built by `heatForm()` `fleet.html:368-391`. Shown when the viewer is the owner, the row has a `heat_prefix`, and `verdict != "not_metered"`.

- `<details class="econ-heat">`, summary `fleet.heat.title` "Heat".
- `<form class="heat-form" data-prefix="…">`.
- Select `.heat-source`, label `fleet.heat.replaces` "Its heat replaces". Options: `none` "Nothing (no heat credit)", `resistive` "Electric resistive heating", `heat_pump` "A heat pump", `fuel` "Gas, oil or another fuel" (`fleet.heat.source.*`).
- Number `.heat-cop` (1-10), label `fleet.heat.cop` "Heat pump COP". Hidden unless `heat_pump`.
- Number `.heat-price` (≥ 0), label `fleet.heat.fuel_price` "Fuel cost per kWh of heat ({currency})". Hidden unless `fuel`.
- Fieldset `.heat-months`, legend `fleet.heat.months` "Months you heat", 12 checkboxes `.heat-month` value 1-12, labels `fleet.month.jan` ... `fleet.month.dec`. None is ticked by default: "users are worldwide, and the southern hemisphere heats in June" (`fleet.html:345-346`).
- Submit `.btn-link` "Save".

### 1.5 Device watts form (owner, device rows only)

`fleet.html:445-452`. `<form class="device-power-form">`, label `fleet.econ.wall_draw` "Wall draw (W)", number `.power-device-watts` `min=1 step=1 data-slug`, `.btn-link` "Save". When a LAN miner reports watts and the row is accrued, it adds `fleet.econ.miner_hint`.

### 1.6 Per-service block

`fleet.html:457-495`. Built only when `/api/earnings/net` answered.

- Rows: services with `cost_attributable && cost != null`, minus the platforms that are device rows.
- Heading `.detail-label` `fleet.econ.per_service` "Per service, where the cost can be attributed".
- Each row `.economics-service-row`: platform name left, `"{gross} − {cost} = {net}"` right in `.num`, red when `negative`. Title `fleet.econ.accrued` when accrued.
- Notes after it, each `.economics-note`:
  - `fleet.econ.no_heat_per_service` when some machine has a heat credit.
  - `fleet.econ.withheld` (plural) for services whose share is too small to mean anything. Their cost still counts in the machine totals.
  - `fleet.econ.unmetered` (plural) for services on boxes with no per-kWh bill.
  - `fleet.econ.unknown` (plural) for services with unknown cost, only when a price is set.

Fields per service (`app/main.py:10518-10584`): `platform`, `gross`, `cost`, `net`, `negative`, `watts`, `watts_source`, `unmetered`, `gross_basis`, `cost_attributable`, `cost_quality`, optional `break_even_price_per_kwh`.

### 1.7 States

| State | What shows | Line |
|---|---|---|
| Loading | Card hidden. No spinner. | `fleet.html:52`, `284-317` |
| Economics API fails | Card stays hidden. | `fleet.html:308-311` |
| No machines | Card hidden. The price inputs are inside the card, so they are hidden too. | `fleet.html:315` |
| Tariff missing | Machine sentence with `missing=price`. | `machine_economics.py:158-176` |
| Watts missing (the owner's case) | Machine sentence with `missing=power_draw`. Only the gross figure, no `−`, `=`. | `machine_economics.py:158-176`, `fleet.html:436` |
| Watts set, no price | Adds the break-even line. | `machine_economics.py:178-184` |
| Earned nothing | `machine_economics.earned_nothing_measurable`. | `machine_economics.py:183-184` |
| Known cost | `earns_against`, `marginal` or `losing_money` sentence, then `gross − cost (+ heat) = net`. | `machine_economics.py:192-219`, `231-252` |
| Losing money | Net in red. The sentence says "turning it off would save that" when dedicated. | `fleet.html:442`, `en.json` `machine_economics.losing_money` |
| Not billed per kWh | `machine_economics.not_billed_kilowatt_hour_electricity`. No Heat form. | `machine_economics.py:139-156`, `fleet.html:370` |
| Machine not reporting | `machine_economics.not_reporting_cashpilot_cannot_see`, gross `—`. | `machine_economics.py:127-136` |
| No FX rate | `cost_unavailable_reason` in the API (not shown by `fleet.html` today). | `app/main.py:11404-11410` |
| Editing heat or device watts | The 60 s refresh waits. | `fleet.html:290-300` |
| Saving | The form's button is disabled. | `fleet.html:1108-1124`, `1150-1164` |

Fleet summary strings (`machine_economics.py:269-326`): `fleet_total` when everything is known; otherwise a join of `fleet_costs_known` "Costs are known for {known} of {n} machine(s).", `fleet_not_metered`, `fleet_not_reporting`.

---

## 2. Proxies (owner only)

### 2.1 Elements

| Element | id / class | Line | Text |
|---|---|---|---|
| Section | `#fleet-proxies`, `.fleet-proxies` | `fleet.html:81` | |
| Title | `#proxies-title` | `fleet.html:83` | `fleet.proxies.title` "Proxies" |
| Meta | `.block-meta` | `fleet.html:84` | `fleet.proxies.meta_html` "Copies of a service that leave through a proxy instead of the box's own connection. How it works" (link to `https://geiserx.github.io/CashPilot/proxies/`) |
| Proxy list | `#proxy-list`, `.table-scroll` | `fleet.html:86` | Spinner plus `fleet.proxies.loading` "Loading proxies" |
| Exit groups | `#proxy-exits` | `fleet.html:87` | |
| Add or edit form | `<details id="proxy-form-box">`, summary `#proxy-form-title` | `fleet.html:89-113` | `fleet.proxy.add` "Add a proxy", or `fleet.proxy.edit_name` "Edit {name}" |
| Copy form | `<details id="proxy-copy-box">` | `fleet.html:115-124` | `fleet.copy.title` "Run a copy through a proxy" |

### 2.2 Proxy list

Rendered by `render()` `fleet.html:1331-1360`, as one `<table class="fleet-table">`, one row per proxy.

Columns (`fleet.proxy.col.*`): **Proxy**, **Exit**, **Traffic**, **Copies**, and an unlabelled action column.

| Cell | Content | Line |
|---|---|---|
| Proxy | `<strong>{name}</strong>`, then muted target: `fleet.proxy.tailscale_exit` "Tailscale exit {node}" for Tailscale, else `"{kind} {host}:{port}"` (for example `socks5 gate.example.net:7000`) | `fleet.html:1339`, `1353` |
| Exit | `"{last_exit_ip} · {last_country}"`, plus `fleet.proxy.rotating_suffix` " (rotating)". Not tested: muted `fleet.proxy.not_tested` "not tested". A failed last test adds a muted line `fleet.proxy.test_failed` "Last test failed on {worker} ({at}): {error}" | `fleet.html:1340-1342` |
| Traffic | `capLine(p)`, plus a **Reset** button (`fleet.proxy.reset_usage`) when the cap is on or holds | `fleet.html:1313-1320`, `1354` |
| Copies | one `<div>` per copy (below), or muted `fleet.row.none` | `fleet.html:1343-1352`, `1355` |
| Actions | **Test** (`.btn-ghost`), **Edit** (`.btn-ghost`), **Delete** (`.btn-danger`) | `fleet.html:1356-1358` |

`capLine(p)` texts (`fleet.html:1313-1320`):

- Cap holds: `fleet.proxy.capped` "Stopped: {reason}". `{reason}` is `proxies.cap_reason()`: "{name} reached {pct}% of its {cap} GB cap on {date}; it resets on day {n} of the month" or "; reset it by hand to start the copies again" (`app/proxies.py:500-507`).
- No cap: `fleet.proxy.no_cap` "No cap".
- Cap on: `fleet.proxy.cap_line` "{used} of {cap} GB, stops at {pct}%, {reset}", with `fleet.proxy.resets_day` "resets on day {day}" or `fleet.proxy.resets_hand` "resets by hand". GB are 10^9 bytes, 2 decimals under 10 GB (`fleet.html:1304`).

One copy line (`fleet.html:1343-1351`), in this order:

1. `fleet.proxy.copy_on` "{slug} on {box}:" (`box` from `workerName()`, or `fleet.proxy.box_n` "box {id}").
2. `fleet.proxy.copy_via` "{status} via {via}". `status` is the raw Docker word from the box's heartbeat (`running`, `exited`, `created`, `restarting`, `paused`, `dead`), `missing` when the box lists no container, or `unknown` when the box sent no entry (`fleet.html:1322-1329`, `app/proxy_tunnel.py:3605-3612`). It is not translated. `via` is `"{exit_ip} · {exit_country}"` or `fleet.proxy.exit_unseen` "exit not seen yet".
3. Muted `fleet.proxy.stopped_by_cap` "(stopped by the cap)" when the cap stopped it.
4. Button: **Stop** (`fleet.proxy.stop`) when `status == "running"`, else **Start** (`fleet.proxy.start`). `.btn-ghost.btn-sm`, `data-copy="{proxy}:{worker}:{slug}"`, `data-cmd`.
5. Button: **Remove** (`fleet.row.remove`), `.btn-danger.btn-sm`, `data-cmd="remove"`.
6. Warning line `.text-warn` with `recovery_skipped` text, when the box sent one.

A copy being removed shows only "{slug} on {box}:" and muted `fleet.proxy.removing` "removing…", with no buttons (`fleet.html:1346`).

Routed services (deployed with a Route through this proxy, `docs/proxies.md:14-72`) are saved as copy records too (`app/main.py:5714-5717`). So they appear in this list as copy lines, with the same text and buttons.

### 2.3 "Proxied copies by the exit IP providers see"

Rendered by `renderExits()` `fleet.html:1362-1369` from `GET /api/proxies` → `exits` (`app/proxies.py:585-621`). Only running copies count.

- Title: `.block-meta` `fleet.proxy.exits_title` "Proxied copies by the exit IP providers see".
- One `<li>` per known exit IP: `"{ip}: {slug} on {box}, {slug} on {box}, …"`, then `<strong>` `fleet.proxy.shared` "(shared)" when the group has more than one member.
- One `<li>` `fleet.proxy.rotating_group` "Rotating, not grouped: {list}" for copies through a rotating proxy.
- One `<li>` `fleet.proxy.unseen_group` "Exit not seen yet: {list}" for copies with no public exit seen.
- Nothing shows when there are no running copies.

Fact: `shared` is `len(members) > 1` (`app/proxies.py:615`), whatever the services are. Seven different services on one exit read "(shared)". The warning that matters (the **same** service already leaves from that IP) is computed only when a copy is added, and comes back as a toast (`app/main.py:8936-8944`, `fleet.html:1462`): "{name} already leaves from {ip} on {list}. Its provider allows one device per IP, so this copy earns nothing there." or "... Copies on one IP share its bandwidth, and the provider may limit devices per IP."

The same IP rules as boxes apply: an exit not seen, or a private address, is never grouped (`docs/proxies.md:578-597`, `CLAUDE.md` "Egress IP awareness").

### 2.4 Add or edit a proxy form

`<form id="proxy-form" class="add-worker-body power-settings" autocomplete="off">` (`fleet.html:91-112`).

| Field | id | Type and limits | Label | Shown for | Placeholder |
|---|---|---|---|---|---|
| (hidden) | `#proxy-id` | hidden | | | empty = add, set = edit |
| Name | `#proxy-name` | text, required, max 80 | `fleet.proxy.name` "Name" | all | |
| Type | `#proxy-kind` | select: `socks5` "SOCKS5", `http` "HTTP CONNECT", `tailscale` `fleet.proxy.kind_tailscale` "Tailscale exit node" | `fleet.proxy.kind` "Type" | all | |
| Host | `#proxy-host` | text | `fleet.proxy.host` "Host" | `.proxy-net` | |
| Port | `#proxy-port` | number 1-65535 | `fleet.proxy.port` "Port" | `.proxy-net` | |
| User | `#proxy-username` | text | `fleet.proxy.user` "User" | `.proxy-net` | `fleet.proxy.kept_host` "kept if empty, unless the host or port changes" |
| Remove stored user | `#proxy-clear-username` | checkbox, `.proxy-clear` | `fleet.proxy.clear_user` "Remove the stored user" | `.proxy-net`, edit mode only | |
| Password | `#proxy-password` | password | `fleet.proxy.password` "Password" | `.proxy-net` | `fleet.proxy.kept_host` |
| Remove stored password | `#proxy-clear-password` | checkbox, `.proxy-clear` | `fleet.proxy.clear_password` "Remove the stored password" | `.proxy-net`, edit mode only | |
| Auth key | `#proxy-authkey` | password | `fleet.proxy.authkey` "Auth key (reusable, ephemeral, tagged)" | `.proxy-ts` | `fleet.proxy.kept_login` "kept if empty, unless the login server changes" |
| Exit node | `#proxy-exitnode` | text | `fleet.proxy.exitnode` "Exit node" | `.proxy-ts` | `fleet.proxy.exitnode_hint` "100.x address, not the name" |
| Login server | `#proxy-login` | text | `fleet.proxy.login` "Login server" | `.proxy-ts` | `fleet.proxy.login_hint` "empty for Tailscale's own" |
| Traffic cap | `#proxy-cap` | number ≥ 0, step 0.1 | `fleet.proxy.cap` "Traffic cap (GB)" | all | `fleet.proxy.cap_none` "none" |
| Stop at | `#proxy-pct` | number 10-100, default 90 | `fleet.proxy.pct` "Stop at (%)" | all | |
| Reset day | `#proxy-reset` | number 1-28 | `fleet.proxy.reset` "Resets on day" | all | `fleet.proxy.reset_hand` "by hand" |
| Rotating | `#proxy-rotating` | checkbox inside its label | `fleet.proxy.rotating` "Rotating exit IP" | all | |
| Save | submit `.btn-primary.btn-sm` | | `fleet.save` "Save" | | |

Kind switch: `showKind()` (`fleet.html:1402-1406`) shows `.proxy-ts` and hides `.proxy-net` for `tailscale`, and the reverse otherwise. The cap, stop %, reset day and rotating fields show for every kind.

Edit mode: `editForm(p)` (`fleet.html:1408-1427`) fills the fields, leaves User, Password and Auth key empty, unticks both Remove boxes, shows them, sets the summary to "Edit {name}" and opens the `<details>`. It does not scroll. `editForm(null)` resets to add mode.

Secrets: the API never sends them back, only `secrets: {username, password, auth_key: bool}` (`app/proxies.py:182-212`). An empty box keeps the stored value. A changed host or port (or Tailscale login server) refuses the save unless the secret is typed again or Remove is ticked: `err.proxies.host_changed_type_again` "The host or port changed, so type the {what} again, or tick Remove to save without it. CashPilot never sends a stored secret to a server it was not entered for." (`app/proxies.py:170-179`, `docs/proxies.md:100-112`).

The placeholders `kept_host` and `kept_login` show on a new proxy too (they are in the template, `fleet.html:100-104`).

Server validation (`app/proxies.py:54-144`), each an error toast with the text of the key:

- `err.proxies.give_proxy_name` "Give the proxy a name"
- `err.proxies.type_must_socks5_http_tailscale`
- `err.proxies.tailscale_proxy_needs_auth_key` "A Tailscale proxy needs an auth key"
- `err.proxies.give_exit_node_s_tailscale` "Give the exit node's Tailscale 100.x address, not its name"
- `err.proxies.login_server_must_https_url`
- `err.proxies.host_must_host_name_ipv4` "The host must be a host name or an IPv4 address"
- `err.proxies.port_must_between_1_65535`
- `err.proxies.traffic_cap_number_gb_empty`, `err.proxies.traffic_cap_must_between_0` (0.001 to 1,000,000 GB)
- `err.proxies.stop_threshold_percentage`, `err.proxies.stop_threshold_must_between_10`
- `err.proxies.reset_day_day_month`, `err.proxies.reset_day_must_between_1` "The reset day must be between 1 and 28, so every month has it"
- `err.proxies.login_server_changed_type_again`

Kind facts for help text (`docs/proxies.md:89-133`): SOCKS5 and HTTP CONNECT carry TCP only and are not encrypted. A Tailscale exit node carries UDP too. A Tailscale proxy needs a reusable, ephemeral, tagged (and, with device approval on, pre-approved) auth key and the exit node's 100.x address (`docs/proxies.md:649-710`). A provider that rotates the exit IP per connection needs **Rotating exit IP** ticked, because the shown exit is sampled once (`docs/proxies.md:127-133`).

### 2.5 Run a copy through a proxy form (main)

`<form id="proxy-copy-form" class="add-worker-body power-settings">` (`fleet.html:117-123`).

| Field | id | Label | Options |
|---|---|---|---|
| Box | `#copy-worker` | `fleet.copy.box` "Box" | Workers whose `system_info.features` has `proxy_tunnel`. None: one option `fleet.copy.no_box` "No box can run proxied copies yet" (`fleet.html:1375-1376`) |
| Service | `#copy-slug` | `fleet.copy.service` "Service deployed there" | The distinct, sorted slugs of the chosen box's `containers` (`fleet.html:1382-1387`). Every deployed slug is listed, eligible or not. |
| Proxy | `#copy-proxy` | `fleet.copy.proxy` "Proxy" | Every proxy, capped ones included (`fleet.html:1378`) |
| Run | submit `.btn-primary.btn-sm` | `fleet.copy.run` "Run the copy" | |
| Rule | `.muted` | `fleet.copy.limits` "Only services without host networking, ports, volumes or devices can run through a proxy." | |

Changing the box refills the services (`fleet.html:1430`). On `main` the form never checks eligibility before submit. With no proxy, the Proxy select is empty and Run still posts.

The Box select is also the box the **Test** button tests on (`fleet.html:1524-1526`, `docs/proxies.md:114-119`). With no box chosen it tests on `fleet.proxy.default_box` "the default box".

### 2.6 Actions and APIs

All owner only (`_require_owner`). All refresh the block with `load()` after.

| Action | Trigger | API | Messages |
|---|---|---|---|
| Load | `load()` `fleet.html:1389-1400` | `GET /api/proxies` (`app/main.py:8461`), `GET /api/workers` | Failure: `#proxy-list` shows the error text, muted |
| Add | form submit, no id | `POST /api/proxies` (`app/main.py:8476`) | `fleet.proxy.saved` "Proxy saved"; form resets and closes |
| Edit | form submit, id set | `PATCH /api/proxies/{id}` (`app/main.py:8493`) | same. A cap turned off or raised starts the copies the cap stopped (`app/main.py:8510-8521`) |
| Delete | `data-act="delete"` | `DELETE /api/proxies/{id}` (`app/main.py:8524`) | confirm `fleet.proxy.delete_confirm` "Delete the proxy {name}?". 409 `api.remove_copies_running_through_proxy` "Remove the copies running through this proxy first", or `api.copies_through_proxy_still_being` |
| Test | `data-act="test"` | `POST /api/proxies/{id}/test?worker_id={box}` (`app/main.py:8542`), up to 90 s | info `fleet.proxy.testing` "Testing on {box} through a throwaway tunnel"; success `fleet.proxy.tested` "Exit {exit} in {ms} ms"; failure stored and shown in the Exit cell |
| Reset usage | `data-act="reset"` | `POST /api/proxies/{id}/reset-usage` (`app/main.py:9217`) | starts the copies the cap stopped |
| Run a copy | copy form submit | `POST /api/proxies/{id}/copies` body `{worker_id, slug}` (`app/main.py:8813`), up to 180 s | info `fleet.copy.starting` "Starting the tunnel, this can take up to a minute"; success `fleet.copy.running` "Running through {exit}"; then `out.warning` (shared exit, 2.3); then the device-link toast `fleet.copy.device_retrying` or `fleet.copy.device_steps` |
| Stop copy | `data-cmd="stop"` | `POST /api/proxies/{id}/copies/{worker}/{slug}/stop` (`app/main.py:8960`) | `out.warning` toast when the box could not save the stop through a power cut |
| Start copy | `data-cmd="start"` | `POST …/start` | may ask (2.7) |
| Remove copy | `data-cmd="remove"` | `DELETE /api/proxies/{id}/copies/{worker}/{slug}` (`app/main.py:9096`) | confirm `fleet.copy.remove_confirm` "Remove the proxied copy of {slug}?"; 202 → `fleet.copy.removing` "Removing {slug}… the worker has not confirmed yet; the copy disappears once it does." |

Every failure shows `err.message` as an error toast (`fleet.html:1451`, `1468`, `1531-1535`).

Copy refusals from `POST /api/proxies/{id}/copies` (`app/main.py:8813-8862`):

- Cap holds: 409 with the cap reason, or `api.proxy_reached_traffic_cap`.
- Service not found or retired: `api.service_not_found`, `api.service_no_longer_available_deployment_2`.
- Not eligible: 400 with the `refusal()` text (2.8).
- Box too old or no Docker: `api.worker_too_old_run_copies` "This worker is too old to run copies through a proxy, or has no Docker socket. Update it first."
- Not deployed on that box: `api.deploy_worker_first_proxied_copy` "Deploy {name} on this worker first; the proxied copy runs with its settings."
- Already routed through this proxy: `api.already_runs_through_proxy_worker`.
- Removed meanwhile: `api.copy_removed_meanwhile_add_again`.
- A wallet-seed service on a Desktop: `_desktop_wallet_refusal`.

### 2.7 Start confirmations

`fleet.html:1483-1510`. A Start can need the owner's approval to replace containers:

- Code `confirm_proxy_start_targets`: confirm `fleet.copy.replace_many` "Start needs to replace these containers on {box}:\n\n{list}\n\nReplace them and start {slug}?", then retry with `{expected_containers, group_approval}`.
- Code `deploy_target_changed`: confirm `fleet.copy.replace_one` "Start may need to replace container {id} for {slug} on {box}. Allow CashPilot to replace it?", then retry with `{expected_container}`.

These come from the 3.0 move to one tunnel per proxy (`docs/proxies.md:278-297`).

### 2.8 States

| State | Today | Where |
|---|---|---|
| Loading | spinner "Loading proxies" in `#proxy-list` | `fleet.html:86` |
| Error | the error text, muted | `fleet.html:1397-1399` |
| No proxies | `fleet.proxy.empty` "No proxies yet. Add one below." | `fleet.html:1333-1335` |
| Proxy with no copies | Copies cell `fleet.row.none` | `fleet.html:1352` |
| Not tested | Exit cell "not tested" | `fleet.html:1340` |
| Last test failed | Exit cell adds "Last test failed on …" | `fleet.html:1341-1342` |
| Rotating | Exit cell " (rotating)"; exits list "Rotating, not grouped: …" | `fleet.html:1340`, `1366` |
| Tailscale kind | Proxy cell "Tailscale exit {node}"; form shows auth key, exit node, login server | `fleet.html:1339`, `1402-1406` |
| Edit mode | summary "Edit {name}", secrets empty, Remove boxes shown | `fleet.html:1408-1427` |
| Cap on | Traffic cell "{used} of {cap} GB, stops at {pct}%, …" plus Reset | `fleet.html:1319`, `1354` |
| Over cap | Traffic cell "Stopped: {reason}" plus Reset; each copy "(stopped by the cap)"; new copies and starts refused; bell alert `proxy_cap` (`app/static/js/app.js:6961`) | `fleet.html:1316`, `1347`, `docs/proxies.md:617-647` |
| Copy running | "running via {ip} · {cc}" plus Stop, Remove | `fleet.html:1348-1350` |
| Copy stopped (by owner) | e.g. "exited via …" plus Start, Remove | same |
| Copy failing | status word (`exited`, `restarting`, `missing`, `unknown`) plus Start, Remove. The reason is in a bell alert: `alert.proxied.copy_down`, `copy_missing`, `tunnel_down`, `tunnel_gone`, `tunnel_stuck`, `needs_approval`, `recovery_skipped` (`app/main.py:1060-1240`) | `fleet.html:1344-1351` |
| Recovery skipped | `.text-warn` line under the copy | `fleet.html:1351` |
| Copy removing | "removing…", no buttons | `fleet.html:1346` |
| Exit not seen | "exit not seen yet"; exits list "Exit not seen yet: …" | `fleet.html:1327`, `1367` |
| Shared exit | exits list "(shared)" when more than one running copy leaves from one IP; toast at add time for the same service | 2.3 |
| No eligible box | Box select "No box can run proxied copies yet" | `fleet.html:1376` |
| No deployed service on the box | Service select empty | `fleet.html:1386` |
| Service not eligible | main: refused only after Run, as a toast | 2.6 |

### 2.9 Eligibility and risk rules for a copy

**On `main`** (`refusal()`, `app/proxies.py:241-268`), a service is refused when its catalog entry has, in this order:

| Rule | Message key | Text |
|---|---|---|
| `network_mode: host` | `api.uses_host_s_network_cannot` | "{name} uses the host's network, so it cannot be moved behind a proxy." |
| published `ports` | `api.publishes_port_host_which_proxied` | "{name} publishes a port on the host, which a proxied copy cannot do." |
| any `volumes` | `api.keeps_data_volume_host_directory_2` | "{name} keeps data in a volume or host directory, which a proxied copy would share." |
| any `devices` | `api.needs_device_host_which_proxied` | "{name} needs a device on the host, which a proxied copy does not get." |
| a GPU | `api.needs_machine_s_gpu_which` | "{name} needs this machine's GPU, which a proxied copy does not get." |
| `NET_ADMIN`, `NET_RAW`, `SYS_ADMIN` or `ALL` | `api.asks_which_would_let_change` | "{name} asks for {risky}, which would let it change or bypass the tunnel's firewall, so it cannot run behind a proxy." |
| `requirements.proxy_prohibited` | `api.terms_forbid_proxy(_source)` | "{name}'s terms forbid running it through a proxy or VPN ({source})." |

Docs: `docs/proxies.md:460-475`. Services that need UDP do not work through SOCKS5 or HTTP.

**With PR #940** (open, "Ten of the 21 Docker earners could not use a proxy"), `refusal(svc, kind=…)` changes to (diff of `app/proxies.py`):

1. `requirements.container_prohibited` → `api.terms_forbid_container(_source)` "{name}'s terms forbid running it in Docker, a virtual machine or a hosting service, so CashPilot does not run it through a proxy." (EarnApp)
2. `requirements.proxy_prohibited` → as before.
3. host network → new text "… uses the host's own network, and a proxied copy has a network of its own, so it cannot run behind a proxy. Run it directly on the box instead."
4. published ports → new text "… needs inbound connections on a published port. Those reach this box, never the proxy's address, so it cannot work behind a proxy. Run it directly on the box instead."
5. a host folder (`/`, `.`, `~`, `$` source) → `api.keeps_data_host_folder`. Named volumes are allowed: each copy gets its own, named `<volume>-p<proxy id>`.
6. a GPU → as before.
7. a device other than `/dev/net/tun` → as before.
8. `SYS_ADMIN` or `ALL` → `api.asks_reaches_past_namespace`.
9. UDP inbound (`udp_port_range`) through `socks5` or `http` → `api.udp_needs_tailscale` "{name} carries its traffic over UDP, which a SOCKS5 or HTTP proxy does not pass. Use a Tailscale exit node instead."

PR #940 then asks for one tick per risk (`acknowledgements()`, `ACK_KEYS = net_admin, net_raw, tun_device, no_inbound, account_risk`). The UI and the worker both refuse without every tick needed.

| Key | When | Tick text (`en.json` in PR #940) |
|---|---|---|
| `net_admin` | `cap_add` has `NET_ADMIN` | "It holds NET_ADMIN, so it can change the network of its own namespace. CashPilot gives it a namespace of its own whose only way out is a gate that holds the proxy's firewall. It is still less contained than a service without it." |
| `net_raw` | `cap_add` has `NET_RAW` | "It holds NET_RAW, so it can send raw packets. They reach only its gate, but it is less contained than a service without it." |
| `tun_device` | `devices` has `/dev/net/tun` | "It gets this box's /dev/net/tun, to make tunnels of its own inside its namespace." |
| `no_inbound` | `udp_port_range` set | "It waits for connections from the internet. Behind a proxy nobody can reach it, so it can earn less or nothing." |
| `account_risk` | `requirements.proxy_risk` set (only Honeygain in the PR) | "Your Honeygain account may be suspended. Honeygain's help centre strictly prohibits VPNs and wants your regular home or mobile connection. It does not support data-center IPs, and one shared IP can get several accounts suspended at once: https://support.honeygain.com/hc/en-us/articles/30688484350492-Does-Honeygain-work-with-VPNs" |

Heading over the ticks: `app.route.ack_title` "Behind a proxy this service is less isolated. Tick each line to run it anyway:".

Per service, from the catalog on `main` (`services/*/*.yml`) and the PR #940 rules:

| Service | On `main` | With PR #940 |
|---|---|---|
| earnfm, iproyal, packetstream, proxybase, proxylite, proxyrack, repocket, traffmonetizer, unmineable, xmrig | allowed | allowed, no tick |
| honeygain | allowed | allowed after the `account_risk` tick |
| urnetwork, proxybase-xyz | refused (volume) | allowed; own volume `urnetwork-data-p<id>` / `proxybase-data-p<id>`, no tick |
| bitping | refused (volume) | allowed; own volume; `net_raw` tick |
| mysterium | refused (volume) | allowed only through a Tailscale exit node; own volume; `net_admin`, `tun_device`, `no_inbound` ticks |
| earnapp | refused (volume) | refused (`container_prohibited`) |
| kryptex-pearl, srbminer-multi | refused (volume) | refused (GPU) |
| anyone-protocol, sia-hostd, storj | refused (ports) | refused (ports) |

The task text said the account-risk tick covers Honeygain, Bitping, Mysterium and URnetwork. The PR #940 code gives that tick only to services with `proxy_risk`, which is Honeygain alone. Bitping and Mysterium get the isolation ticks above. URnetwork gets no tick.

PR #940 copy form changes (diff of `fleet.html`):

- New `#copy-needs` box under the three selects, full width, and the Run button gets `id="copy-run"`.
- On every change of service or proxy, `fillNeeds()` calls `GET /api/proxies/{id}/copies/needs?slug=` → `{refusal, needs[], volumes[]}`.
- While it loads, Run is disabled.
- Load fails: `.text-warn` `fleet.copy.needs_failed` "CashPilot could not read what this service needs behind this proxy ({error}). The copy cannot run until it can." plus a **Retry** button `#copy-needs-retry` (`app.retry`). Run stays disabled.
- Refused: `.text-warn` with the refusal text. Run disabled.
- Volumes: muted `fleet.copy.own_volume` "This copy gets data volumes of its own ({names}). The provider sees a new device, not the original."
- Needs: the heading and one checkbox per key (`input[data-ack]`). Ticks survive the 60 s refresh for the same service and proxy. The service and proxy choices survive it too.
- Submit sends `acknowledged: [keys]`.
- New rule text `fleet.copy.limits`: "A service that uses the host's network, publishes ports, keeps data in a host folder or needs a GPU cannot run through a proxy. Each copy gets data volumes of its own."

PR #940 copy line changes:

- `copies[].acknowledged` from the API. With any, a badge `.badge.badge-warning` `fleet.copy.reduced` "reduced isolation", its title the tick texts plus `fleet.copy.withdraw_hint` "Withdraw removes this copy. Its data volumes stay, so the copy keeps its identity if you add it again."
- The Remove button reads **Withdraw** (`fleet.copy.withdraw`) when the copy has ticks. It calls the same DELETE.
- `tripped` from the heartbeat adds `.text-warn` `fleet.copy.tripped` "The watchdog of its tunnel stopped it: the tunnel's firewall changed, or traffic left from this box's own IP. It stays stopped until you start it."

### 2.10 What other open PRs add to the Fleet page

- **PR #933** "add, check and remove a Secure VM from the Fleet page": a Secure VM panel per host with KVM, and a "Secure VM on <host>" flag. It adds rows inside the Boxes table (`CPSecureVM.row()` after each worker row) and includes `_secure_vm.html` in the scripts block. Nothing in the three blocks of this brief.
- **PR #947** "show the layers each earner got, and choose gVisor per earner": a **Security layers** `<details class="layers">` row per worker, inside the Boxes table (`renderLayers()`). It adds one copy refusal: `api.runtime_choice_routed` "This earner is set to run under gVisor on {worker}, and a copy routed through a proxy runs under Standard only. Set it back to Standard on the Fleet page to route it. Nothing was deployed." It is raised for any deploy with a `proxy_id`, so a new proxied copy of an earner set to gVisor is refused with it.

Both stack more rows under each box in the Boxes table. Neither adds a block after it.

---

## 3. Add a box

### 3.1 Elements

| Element | id / class | Line | Text |
|---|---|---|---|
| Disclosure | `<details id="add-worker" class="add-worker">` | `fleet.html:128` | summary `fleet.add.title` "Add a box" |
| Image line | `.add-worker-text` | `fleet.html:131-133` | `fleet.add.deploy_image_html` "Deploy `drumsergio/cashpilot-worker:X.Y` on each server, or install the Android app on your phone." Dev build: `fleet.add.deploy_unversioned_html` |
| Desktop line | `.add-worker-text` | `fleet.html:134-136` | `fleet.add.desktop_html` "On a computer with CashPilot Desktop, pick **Join my CashPilot** … paste the block into **Paste from Add a box**." |
| Docker line | `.add-worker-text` | `fleet.html:137-139` | `fleet.add.docker_env` "For Docker workers, set these environment variables:" |
| Env block | `.env-block`, `<code id="worker-env">` | `fleet.html:140-143` | `CASHPILOT_UI_URL=<span id="env-ui-url">`, `CASHPILOT_API_KEY=<span id="env-api-key">••••••••</span>`, `CASHPILOT_WORKER_NAME=server-name` |
| Key status | `#api-key-status`, `.badge` | `fleet.html:145` | starts `fleet.add.key_checking` "Checking…" |
| Reveal | `#reveal-btn`, `.btn-ghost.btn-sm`, `data-action="toggleApiKey"` | `fleet.html:147` | owner only; `fleet.add.reveal` "Reveal API Key" / `fleet.add.revealing` "Revealing…" / `fleet.add.hide` "Hide API Key" |
| Copy | `.btn-ghost.btn-sm`, `data-action="copyWorkerEnv"` | `fleet.html:148` | owner only; `fleet.add.copy` "Copy" |
| Fallback | `#worker-env-fallback`, readonly `<textarea>` | `fleet.html:154-156` | hidden until the clipboard fails |
| Loopback note | `#env-ui-url-loopback`, `.muted` | `fleet.html:158-160` | `fleet.add.loopback_html` |
| Key note | `.muted.add-worker-text` | `fleet.html:161-163` | `fleet.add.key_note_html` "This is the enrolment key. … Use the same key on all workers. Each worker uses it only to join, then gets its own key." |

### 3.2 Actions and APIs

| Action | Handler | API | Result |
|---|---|---|---|
| Fill the UI URL | inline `fleet.html:183-188` | none | `window.location.origin`, or `{protocol}//<this-server-address>:{port}` on a loopback host, which also shows the loopback note |
| Key status | `loadApiKeyStatus()` `fleet.html:192-212` | `GET /api/fleet/api-key` (`app/main.py:13947`) | `is_set` and `source`: `fleet.key.generated` "Generated in /fleet/.fleet_key" (file), `fleet.key.from_env` "From CASHPILOT_API_KEY" (env), `fleet.key.configured` "Configured"; class `badge-deployed`. Not set: `fleet.key.not_set` "Not set", class `badge-category`. Failure: `fleet.key.unknown` "Unknown" |
| Reveal / Hide | `toggleApiKey()` `fleet.html:1016-1033` | `POST /api/fleet/api-key/reveal` (`app/main.py:13958`, owner only, audit-logged), fetched once | Shows the key, or `fleet.key.not_configured` "(not configured)", or `fleet.key.error` "(error)" with toast `fleet.key.reveal_failed` |
| Copy | `copyWorkerEnv()` `fleet.html:1252-1279` | reveal, if not fetched yet | No key: error toast `fleet.add.nothing_to_copy` "Nothing to copy: the API key reads {value}. Reveal it first." Success: `fleet.add.copied` "Copied". No clipboard (plain http): shows the textarea, selects it, warning toast `fleet.add.copy_selected` "This page is not on https, so CashPilot cannot reach the clipboard. The text is selected, press Ctrl/Cmd+C." |

### 3.3 States

| State | What shows |
|---|---|
| Closed | Default. |
| No boxes at all | The Boxes table shows `fleet.empty.*` and opens Add a box by itself (`fleet.html:539-547`). |
| Key checking / set / not set / unknown | The status badge, 3.2. |
| Key hidden / revealed | `••••••••` / the key; the button label flips. |
| Loopback origin | URL placeholder plus the loopback note. |
| Clipboard blocked | Textarea with the block, selected. |
| Viewer | No Reveal and no Copy. |

---

## 4. What a copy is

These facts come from `app/proxies.py:328-359`, `app/main.py:8813-8946`, `app/proxy_tunnel.py` and `docs/proxies.md`.

- **A copy is a second container of a service that already runs on a box.** You pick a box, a service already deployed on that box, and a proxy. CashPilot builds the copy from that service's own deploy record on that box: same image, same account credentials, same limits.
- **Its traffic leaves through the proxy.** The copy has no network of its own. It joins a tunnel container (`cashpilot-tunnel-p<id>`) whose only way out is the proxy. All copies through one proxy on one box share one tunnel. Seven copies are eight containers.
- **The provider sees another device on another IP.** The copy gets its own device name (the box's name plus `-p<proxy id>`) and its own device id where the catalog marks one per device. With PR #940 it also gets its own data volumes. Providers count devices per public IP, so one box can earn on its own IP plus one IP per proxy.
- **The original does not change.** It keeps running from the box's own connection. A copy runs beside it. Removing the original service from a box also removes its copies (`app/worker_api.py:3185-3207`).
- **One copy per service, per proxy, per box.** Adding the same one again deploys it again over the record (`app/main.py:8865-8868`).
- **It fails closed.** If the proxy or the tunnel goes down, the copy has no way out. It stops earning. It never sends from the box's own IP (`docs/proxies.md:193-205`).
- **Before the copy starts, the tunnel must prove its exit.** The tunnel must see an exit IP within 45 s. When the box knows its own IP, the exit must be a different one. Otherwise the copy is refused (`docs/proxies.md:160-175`).
- **What it looks like after Run.** A toast "Running through 203.0.113.71 · ES". A new line under the proxy: "earnfm on watchtower: running via 203.0.113.71 · ES [Stop] [Remove]". The copy joins its exit group in "Proxied copies by the exit IP providers see". The container is `cashpilot-<slug>-p<id>`. If the provider needs the new device added to the account, a second toast says so or says CashPilot keeps trying for a day.
- **Which services can be copied.** Only those whose catalog entry passes the rules in 2.9. On `main`, the Service list shows every deployed service, and a service that does not qualify is refused only after Run. The list is per box, so a service missing from it is not deployed on that box.
- **Copy and Route are two ways.** A copy runs beside a service that already started once from the box's own IP. A Route, chosen on the deploy form, runs the service itself only through the proxy, from its first start (`docs/proxies.md:14-72`). A routed service also shows as a copy line in the proxy list.
- **The risks.** Some providers forbid proxies or VPNs. On `main`, a catalog `proxy_prohibited` refuses the copy. With PR #940, Honeygain's terms (`proxy_risk`) need the owner's tick "Your Honeygain account may be suspended…". Services that hold `NET_ADMIN`, `NET_RAW` or `/dev/net/tun`, or wait for inbound UDP, need one tick each, because behind a proxy they are less isolated or cannot be reached. A commercial proxy service can also refuse to carry earner traffic, so a copy can run and earn nothing (`docs/proxies.md:477-494`).
- **The traffic cap.** A proxy can have a cap in GB. At the stop percentage (90% by default), every copy through that proxy stops. They start again on the reset day or with **Reset**. A copy the owner stopped stays stopped (`docs/proxies.md:617-647`).
