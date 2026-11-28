# Design 2: proxy cards

Files: `index.html` (the mockup), `shot.png` (1440 px, full page), `shot-narrow.png` (900 px).

## The idea in one paragraph

Each proxy becomes one card. The card answers three questions in a fixed row: which IP do providers see, how much traffic is left, and how many copies run. Under that row are the copies, grouped by box, as equal-width tiles. All proxy actions sit in the card header. Adding or editing a proxy, and adding a copy, open a drawer on the right side, so the page does not grow a long inline form. You start a copy from the card ("Add a copy here"), so the proxy is already chosen. Running costs become four tiles and two side-by-side tables, with the "power draw unknown" sentence said once.

## What changed, and why

### Running costs

| Today | Design 2 | Why |
|---|---|---|
| Price, currency and Save on a row above the body | The fourth tile: "Electricity price per kWh", inputs, "/ kWh", Save, help line | The price is an input to the three figures beside it, so it sits with them. |
| One full-width block per machine. Each repeats "X earned N last month. Without this machine's power draw…" | A table: Machine, Earned / month, Power draw, Cost, Net, Heat. One callout under it says the missing-draw sentence once, with a "Go to Boxes" button | Five copies of one sentence become one. The numbers line up in columns. |
| A "Heat" disclosure under every machine | The Heat cell of each row is a button ("Not set ▸", or the source, for example "Heat pump ▾"). It opens a detail row under the machine with the same form | The form exists for the owner as today, but takes one cell until someone opens it. |
| "Per service…" as right-aligned "$0.08 − $0.88 = −$0.80" strings | A table: Service, Earned, Cost, Net, and a small net bar. Sorted by net, best first. Losses in red | The labels sit next to their numbers. The bar shows at a glance which services pay and which do not. |
| No word on why per-service costs exist when machine costs do not | A footnote: per-service costs use an estimate (65 W, or the processor's rated power) where no draw is set | The page showed both "costs unknown" and "costs: $0.88" with no reason. |

At 1440 px the two tables sit side by side (7:5). Under 1100 px they stack. The tiles go to three across plus the price tile on its own row.

### Proxies

| Today | Design 2 | Why |
|---|---|---|
| A 4-column table; the Copies cell holds 7 lines, each with buttons of different widths | A card per proxy. Copies are tiles in a grid (`minmax(300px, 1fr)`): status square, slug, state word under it, then Stop and Remove at the right of the tile | Every tile has the same width, so the buttons line up in columns. Nothing zig-zags. |
| Each copy line repeats "via 203.0.113.71 · ES" | The exit shows once, in the card's facts row. A tile shows the exit only when it differs ("exit not seen yet") | Seven copies of one IP become one. |
| Test, Edit, Delete float at the far right of the row | Header: "Test on watchtower" stays visible. "More ▾" holds Test on another box, Edit, Reset traffic count and Delete (Delete last, in red, after a rule) | Test is the frequent action. Delete is far from a stray click. |
| A separate bullet list "Proxied copies by the exit IP providers see" | A "shared exit" note inside the card, under the facts row | The list repeated every copy again. The note says what sharing means. |
| Traffic as one text line | A meter: filled share, a tick at the stop %, the numbers in text ("46.00 of 50 GB · 92%"), and "Stops at 95% (47.50 GB). Resets on day 1." Warn colour near the stop, red once stopped. Reset is a visible button when a cap is on | Colour never carries the state alone: the numbers and the words are always there. |
| Add a proxy: an inline form, mixed widths, checkboxes under inputs, cap/stop/reset/rotating on one row | A drawer in three groups: Proxy (name, type), Connection, Limits. The type is three radio cards, each with one line of help. Host and port share a row. User and password share a row, each with its "Remove the stored…" tick under it. Cap, stop % and reset day are three equal fields with a hint each. Rotating has its own line and a hint | One column, fixed grid, every field with its help. |

### Run a copy

Today it is three selects and one grey line. Design 2 makes it a drawer in three numbered steps. You open it from a card ("+ Add a copy here"), so the proxy shows in the drawer head with a "Change" link. The section "Run a copy through a proxy" stays on the page, with a two-sentence definition and an "Add a copy…" button; that button opens the same drawer with step 0, the proxy choice.

1. **Pick the box.** Every box, with "7 copies here" or "no copies yet". A box that cannot run copies is shown greyed with its reason, instead of hidden.
2. **Pick a service deployed on that box.** Three groups: "Can run" (each with "ready" or "needs your OK" and one line of why), "Already runs through this proxy" (one muted line of slugs), "Cannot run through a proxy" (greyed, with the refusal text). A line under the list says a missing service is not deployed on that box.
3. **Check and run.** "What happens" lists four facts for the picked service: the new container name, the exit IP and the new device name, that the original keeps running, and that the copy stops if the proxy stops. Then a box with the risk ticks. Run stays disabled until every tick is set, and the footer says why.

After Run, the drawer closes, the toast shows, and the new tile appears with a pink border until the next refresh.

### Add a box

Same content and actions. The three ways (Docker server, Android phone, CashPilot Desktop) become three small boxes on the left. The env block, key status, Reveal and Copy sit on the right. It stacks under 1100 px.

## How each problem we saw is solved

- **The sentence repeated five times.** Said once, in one callout, with a button to where you fix it.
- **Heat under every machine.** One cell per row; the form opens in place.
- **Per-service numbers far from their labels.** A real table with columns, plus a bar.
- **Copies zig-zag.** Equal tiles in a grid; buttons line up.
- **Test/Edit/Delete far right.** Header actions, Delete in a menu.
- **The exit list repeats every copy.** Replaced by one note in the card.
- **The proxy form has mixed widths.** A drawer with a fixed grid.
- **"Run a copy" explains nothing.** A definition on the page, a "What is a copy?" panel with a diagram, and a step-by-step drawer that shows the eligibility of every service, the reason a service cannot run, what happens, and the risk.

## How a first-time user learns what a copy is

1. The Proxies block opens "What is a copy?" by itself until the user closes it once (stored in `localStorage`). It has five facts and a diagram: one box, the original leaving from the box's own IP as device 1, the copy (`cashpilot-earnfm-p1`) leaving from the proxy's IP as device 2. The diagram is HTML boxes, so every label is a translatable string.
2. With no proxy, the empty state shows the same facts and what each proxy type is (panel c).
3. The card footer says what "Add a copy here" does.
4. The drawer's "What happens" box says it again for the exact service, box and proxy picked.

## Checklist: every action today, and where it lives

| Action today (BRIEF.md) | Where in Design 2 |
|---|---|
| Electricity price, currency, Save (every role) | Running costs, fourth tile |
| Price help text | Under the inputs in the tile |
| Per-machine watts, Dedicated, Not billed per kWh | Unchanged in the Boxes table; the callout's "Go to Boxes" button takes you there |
| Device watts form (owner, device rows) | The Power draw cell of a device row: "W" input and Save (panel f) |
| Heat form (owner): source, COP, fuel price, 12 months, Save | Heat cell button opens a detail row with the same form (panel f) |
| Break-even line, heat credit line, expected line | Top line of the same detail row (panel f) |
| Gross, cost, heat credit, net, verdict colours | Table columns; net red for losing money, amber for marginal |
| Fleet summary ("Costs are known for 0 of 5 machines.") | Block meta, as today |
| Per-service rows and the notes (withheld, unmetered, unknown, no heat per service) | Per-service table; the notes go in the footnote under it |
| Proxy list, name, target | Card title, kind flag, target line |
| Exit IP, country, rotating, not tested, last test failed | Card facts, "Exit IP providers see" (panels d and e) |
| Test (on the box picked) | Header "Test on {box}"; other boxes in More |
| Edit | More, Edit: opens the proxy drawer filled in |
| Delete, with its confirm | More, Delete (last, red) |
| Reset usage | Visible "Reset" in the traffic fact when a cap is on; also in More |
| Cap line, no cap, cap holds | Traffic fact: meter plus text (panels e) |
| Per copy: status word, via exit, stopped by the cap | Tile: status square, slug, state word; exit only when it differs; "stopped by the cap" in the state line |
| Stop / Start / Remove per copy | Tile buttons; Start replaces Stop when not running |
| Removing… (no buttons) | Tile with "removing…" and no buttons (panel d) |
| recovery_skipped line | Amber line in the tile (panel d) |
| Start confirmations (replace containers) | Unchanged: the same confirm dialogs |
| Exit groups: shared, rotating, not seen yet | Shared: note in the card. Rotating: the exit says "(rotating)" with "copies are not grouped by IP". Not seen: on the tile. An exit shared by two proxies needs a page-level line; see open points |
| Add a proxy: name, SOCKS5 / HTTP CONNECT / Tailscale | Proxy drawer, "Proxy" group, type as radio cards |
| Host, port, user, password | "Connection" group (SOCKS5 or HTTP) |
| Keep or remove stored user / password | "· stored" next to the label, placeholder "kept if empty…", "Remove the stored…" tick under each field, and the host-changed rule as a hint |
| Auth key, exit node, login server | "Connection" group (Tailscale) |
| Traffic cap, stop %, reset day, rotating | "Limits" group |
| Run a copy: box, service, proxy | Copy drawer, steps 1 and 2; the proxy comes from the card or step 0 |
| Eligibility rule | Group "Cannot run through a proxy" with the refusal text per service, and a line on missing services |
| Needs check: loading, failed with Retry, volumes | Drawer states in panel b; "Gets its own data volume…" on the service row |
| Risk ticks (account_risk, net_admin, net_raw, tun_device, no_inbound) | Step 3 risk box; Run disabled until all are ticked |
| Reduced isolation badge, Withdraw | Flag on the tile, Withdraw replaces Remove (panel d) |
| Tripped by the watchdog | Same amber line slot as recovery_skipped |
| Add a box: image line, Desktop line, env block, key status, Reveal, Copy, clipboard fallback, loopback note, key note | Add a box, left and right columns; fallback textarea and loopback note stay where they are today |
| Empty state "No proxies yet" | Panel c |
| Loading / error | Same spinner and error line, inside the block where the cards go |

## Implementation cost (rough)

- **`fleet.html` template:** Running costs markup about 40 lines changed. Proxies, the copy form and Add a box about 120 lines replaced with the cards container, two drawer shells and the explainer.
- **`fleet.html` scripts:** `loadFleetEconomics()` render about 120 of its 220 lines rewritten (tiles, two tables, detail rows). The Proxies `render()` and `renderExits()` about 150 lines rewritten as `renderCard()` and `renderTile()`. A new drawer controller (open, close, focus trap, Escape) about 60 lines. The copy drawer about 150 lines; it reuses `fillNeeds()` from PR #940 and needs every box's deployed services with their eligibility, so it calls `/copies/needs` once per service shown, or a new batch endpoint (about 40 lines in `app/main.py`).
- **`app.js`:** none required. A shared drawer helper there would let other pages use it.
- **`style.css`:** about 180 lines (tiles, cost tables, card, facts row, meter, tiles grid, drawer, pick list). No new colours; it uses the existing state tokens.
- **Tests:** the template tests that look for `#proxy-form`, `#proxy-copy-form` and their ids need updating; the ids can stay on the drawer forms so most handlers keep working.
- **Total:** about 900 lines touched, mostly in `fleet.html`.

## What it needs from i18n

- **Kept keys:** all `fleet.proxy.*`, `fleet.copy.*`, `fleet.costs.*`, `fleet.econ.*`, `fleet.heat.*` that exist today. Copy state words stay as they are (they are Docker words and are not translated today).
- **New keys, about 45:** tile labels (earned last month, electricity cost, net, the notes), the callout sentence and "Go to Boxes", table headings (power draw, heat, not set), the per-service summary and footnote, the explainer's five facts and the diagram labels (your box, the original, device 1, device 2 via the proxy), card fact labels (exit IP providers see, traffic, copies, one fixed IP, on {n} box), the shared-exit note, "More", "Test on another box", "Reset traffic count", "Set a cap", "Add a copy here" and its line, the drawer group legends (Proxy, Connection, Limits), the three type descriptions, the field hints, the copy drawer step titles, the group headings (can run, already runs through this proxy, cannot run through a proxy), "ready", "needs your OK", "not possible", the four "What happens" lines, "Tick the risk line to run it", the empty-state text.
- **Plurals:** "{n} copies", "{n} running", "on {n} box(es)", "{n} of {m} earn more than their power cost". These need plural forms in each language.
- **Width:** the tile buttons have a minimum width of 4.6 em and the tiles are at least 300 px, so "Supprimer" or "Entfernen" fit. The type radio cards wrap their help line.
- The "What happens" lines take values (service, box, container name, exit, device name); they must be full sentences with placeholders, never joined pieces.

## Open points

- **An exit IP shared by two proxies.** A card cannot see the other cards. The design adds one line under the cards only when that happens ("Two proxies leave from 203.0.113.71: …"). It is not drawn in the mockup.
- **The shared-exit note** today flags any two copies on one IP. The more useful warning (the same service already on that IP) exists only as a toast at add time. The card could show it as an amber note if `/api/proxies` returned it per exit.
- **The account-risk tick** in PR #940 covers only services with `proxy_risk` (Honeygain). The drawer shows whatever ticks the needs endpoint returns.
- **The copy drawer's eligibility per service** costs one needs call per deployed service. A batch endpoint would make step 2 one call.
- **Mockup data** for panels d and e (Residential DE, Mobile ES, 203.0.113.50, 198.51.100.7) are invented to show the states. Panel f's figures are invented too. Everything else uses the owner's real figures.
