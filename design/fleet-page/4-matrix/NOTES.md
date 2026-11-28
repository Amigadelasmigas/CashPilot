# Design 4: Exit matrix

Files: `index.html` (the mockup), `shot.png` (1440 px, full page), `shot-narrow.png` (900 px, full page). Both were rendered on the MacMini with `shoot.cjs`.

## The idea in one paragraph

Providers pay per device, and they count devices per public IP. So the question behind the Proxies block is: *from which IP does each service leave, and how many times?* Today the page answers it in three places. The proxy table has a Copies cell with seven lines. A bullet list repeats the same copies grouped by IP. The copy form sits apart, and it does not say what a copy is. This design answers the question once, as a grid. Rows are services. Columns are exits: each box's own line, then each proxy. Columns that leave from the same public IP sit under one IP header. A copy is a cell in a proxy's column. An empty cell where a copy can run says **+ copy**. A cell where a copy cannot run says **not possible**, and it shows the reason on hover or focus. A panel beside the grid explains copies until you pick a cell. Then the panel shows that cell: the copy's state and its buttons, or the run-a-copy flow.

The real data shows why this matters. The one proxy is a Tailscale exit node on geiserct. Its exit, 203.0.113.71, is also geiserct's own line. So every service that geiserct runs directly already leaves from that IP. In the grid this shows at once: the proxy column and the geiserct column share one IP header, and a service in both is outlined in amber. Today the page says "(shared)" for any two copies on one IP, whatever the services are, and it says nothing about the box's own line.

Note on data: proxies, copies, machines, costs and the header total are the owner's real figures. The list of which services run directly on each box is assumed (the brief has no deploy list). The own-line IPs of watchtower and geiserback are documentation addresses (203.0.113.x, 198.51.100.x), so no home IP goes into the repo.

## What changed against today, and why

### Running costs

| Today | This design | Why |
|---|---|---|
| Five full-width blocks, each with the same long sentence. | One table, one row per machine: Machine, Earned, Power, Net, Heat. When every row misses the same input, one notice above the table says it once and links to the Boxes table. The full server sentence stays as the row's tooltip. | The sentence was the same five times. The figures were far from the names. |
| Electricity price, currency and Save on one row, help text below. | Same fields, same row. The help text sits on the same line, after Save. | It kept its function and lost a line. |
| "Heat" disclosure under each machine. | A **Heat** link at the end of each row. It opens the heat form as a full-width row under that machine (panel f). | The form keeps its place next to its machine, but it takes no space when closed. |
| "Per service" rows: name on the left, `$0.08 - $0.88 = -$0.80` at the far right. | A table: Service, Earned, Power, Net, and a net bar. The bar has a zero line, green to the right and red to the left, on one honest scale. Headers sort (default: Net, high to low). The meta line says "5 of 11 cost more than they earn". | The formula string was hard to scan and far from its label. A table puts each figure in its column. The bar shows the size of each result next to the others. |
| Notes under the per-service list. | Same notes, under the table. One new line says the power figure is an estimate (65 W per box or the CPU's rated power) until the watts are set. | Per-service costs show while every machine cost is unknown. Without that line the two halves seem to disagree. |

Machine rows with more to say (break-even tariff, "you pay", heat credit, expected earnings for a device) show it as a second, muted line under the machine name. The Net cell shows the net, and `+ $x heat` under it when there is a heat credit. Short status words replace the sentence in the Power cell: *needs watts*, *needs a price*, *not billed per kWh*, *not reporting*. A device row has its **Wall draw (W)** input and Save in the Power cell (panel f).

### Proxies

| Today | This design | Why |
|---|---|---|
| A 4-column table whose Copies cell holds one line per copy, with buttons of different widths. | A compact table: Proxy (name and type), Goes through (host:port or the 100.x node), Exit IP, Traffic, Copies (a count), and Test, Edit, Delete. The three buttons are a grid of equal widths, so they line up from row to row. | The copies move to the grid. The table holds only what belongs to the proxy. |
| Exit cell: the IP. | Same, plus "Same IP as geiserct's own line" when a proxy's exit equals a box's own egress IP. | This is the fact that makes a copy worthless, and today nothing says it. |
| Traffic cell: one text line, Reset button after it. | A thin bar with a mark at the stop percentage. Amber when the use is near the stop point, red when the cap stopped the copies. Reset stays next to the bar. The text line under it is today's text (panel e). | The bar makes "92% of 50 GB, stops at 95%" readable in one look. |
| Test uses the Box select of the copy form. | A "Test from" select above the table, next to **+ Add a proxy**. | The copy form no longer has a Box select at the top level, and Test needs a box of its own. |
| "Proxied copies by the exit IP providers see" bullet list. | Removed. The grid's IP headers do this job. One amber line above the grid names each service that leaves twice from one IP. | The list repeated every copy. Its "(shared)" flag fired for any two services on one IP, so it warned about nothing. |
| Add a proxy form: mixed widths, one cramped row. | Three columns: **Proxy** (name, type as three radio cards with one line each on what the type carries), **Where it connects** (host and port on one row, then user and password with their Remove ticks; or auth key, exit node, login server for Tailscale), **Traffic limit** (cap, stop %, reset day in three equal fields, one hint, then the rotating tick with its explanation). Save and Cancel at the bottom (panel a). | Each field gets the width of its column. The type choice says what each type does. |
| "kept if empty…" shows on a new proxy too. | Shows only in edit mode, next to a "stored" mark. | A new proxy has nothing stored. |

### Run a copy

| Today | This design |
|---|---|
| Three selects (Box, Service deployed there, Proxy), Run, and one grey rule line. | Pick a cell. The column is the proxy and the row is the service. The panel asks only for the box (preselected when one box qualifies) and shows: the new container name, the exit it will leave from, the device name the provider sees, and "the original keeps running on watchtower's own line". Then the warnings and the ticks, then **Run the copy** (panel b). |
| Every deployed service is listed. A refused one fails only after Run, as a toast. | A service that cannot run a copy shows **not possible** in its cell. Hover or focus shows the refusal text. Picking it shows the same text in the panel, with the rule line. |
| A service missing from the list has no explanation. | Every service on any box has a row. A dot means "not deployed on this box". |
| The shared-IP warning arrives as a toast after the copy started. | The cell says "IP in use" before you pick it. The panel repeats today's warning text before Run. |
| PR #940 ticks appear under the form. | The cell says how many ticks the copy needs ("1 tick", "3 ticks", "risk"). The panel lists them, with today's heading. Run stays disabled until each one is ticked. |

After Run, the cell shows "starting the tunnel" with a spinner, then "running, from watchtower". The toasts stay as they are.

### Add a box

Same content, laid out in two columns: the three ways to add a box on the left (server, phone, Desktop), and the env block with its status, Reveal and Copy on the right. The key note sits under the three ways. Under 960 px the columns stack.

## How each problem is solved

| Problem | Solution |
|---|---|
| Running costs repeats the machine name and amount five times. | One table. One notice when every row misses the same input. |
| The "Heat" disclosures stack under every machine. | A Heat link at the row's end. The form opens under that row only. |
| Per-service figures are far from their labels, as formula strings. | A sorted table with Earned, Power, Net columns and a net bar. |
| The Copies cell zig-zags with buttons of different widths. | Copies leave the proxy table. Test, Edit and Delete sit in an equal-width grid. Per-copy Stop, Start and Remove move to the panel beside the grid, so no table cell holds buttons. |
| The "Proxied copies by exit IP" list repeats every copy. | Removed. The IP headers group the exits. One alert line names the real conflict. |
| The proxy form has mixed widths and a cramped row. | Three labelled columns with full-width fields. |
| It is not clear how "Run a copy through a proxy" works. | The panel explains it before anything is picked. Picking a cell shows exactly what will run, where it leaves from, what the provider sees, and what stays the same. |
| It is not clear which services qualify, or why one is missing. | Every service has a row. Cells say "+ copy", "not possible" (with the reason) or show a dot (not deployed). |
| The account risk is not visible. | The cell says "risk". The panel shows the tick text. Run stays off until it is ticked. |

## How a first-time user learns what a copy is

1. The Proxies meta line: "A proxy gives your boxes one more public IP."
2. The grid's meta line: "Rows are services. Columns are the public IPs that providers see." The column headers show each box's own line next to the proxy, so a proxy reads as one more exit.
3. The panel beside the grid, before anything is picked, explains it in five numbered lines. A copy is a second container of a service that already runs on a box. Its traffic leaves through the proxy. The provider sees a new device on a new IP. The original keeps running. If the proxy goes down, the copy stops and never falls back to the box's IP. Under that: how to start one, and the two risks (an IP that already carries the service, and providers that forbid proxies).
4. The run panel makes it concrete before Run: container `cashpilot-honeygain-p1` on watchtower, leaves from 203.0.113.71, the provider sees device `watchtower-p1`, the original keeps running on watchtower's own line.
5. With no proxies (panel c), the grid still shows each box's own IP. A dashed column says: "A proxy adds a column here: one more IP for every service that can run a copy."

## Checklist against BRIEF.md: every action today, and where it lives now

### Running costs

- [x] Quality line (`economics.summary`): block meta, unchanged.
- [x] Electricity price, currency, Save, help text: the settings row (same ids, same handler).
- [x] Validation and toasts on save: unchanged.
- [x] Machine name, Device label: Machine column (panel f shows a device row).
- [x] Summary sentence: one shared notice when all rows miss the same input; otherwise a short status word, with the full sentence as the row tooltip.
- [x] Gross (and accrued title), cost, heat credit, net, red when losing: Earned, Power, Net columns. Heat credit is a second line in the Net cell.
- [x] Break-even line, "you pay", heating line, heat credit line, expected line: second muted line under the machine name.
- [x] Heat form (source, COP shown only for heat pump, fuel price shown only for fuel, 12 months, Save): row expansion from the Heat link (panel f). Owner only, hidden for not-metered rows, as today.
- [x] Device watts form: in the Power cell of a device row (panel f).
- [x] Per-machine watts, Dedicated, Not billed per kWh: still in the Boxes table (out of scope). The notice links there.
- [x] Per-service rows (gross, cost, net, negative, accrued title): the Per service table.
- [x] Notes `no_heat_per_service`, `withheld`, `unmetered`, `unknown`: under the table, same text.
- [x] The 60 s refresh waits while a heat or watts form is being edited: unchanged.

### Proxies

- [x] Load, error, spinner: unchanged, in the proxy table.
- [x] Empty: "No proxies yet" with what a proxy adds, and **+ Add a proxy** (panel c).
- [x] Proxy name and target (`Tailscale exit {node}` or `{kind} {host}:{port}`): Proxy and Goes through columns.
- [x] Exit, "not tested", "(rotating)", "Last test failed on…": Exit IP column (rotating shown in panel e).
- [x] Traffic: `No cap`, cap line, "Stopped: {reason}", Reset: Traffic column with a bar (panel e).
- [x] Test (with the test box), Edit, Delete (with confirm and the 409 texts): action grid; the test box is the "Test from" select.
- [x] Per-copy line `{slug} on {box}: {status} via {via}`: the grid cell (status, box) plus the panel (via, container).
- [x] Stop / Start / Remove: panel, after a cell is picked (panels in d). Withdraw replaces Remove when the copy has ticks (PR #940, panel d).
- [x] "(stopped by the cap)": cell says "stopped", the panel says why; the proxy's Copies cell says "stopped by the cap" (panel e).
- [x] `recovery_skipped` and `tripped` warning lines: the panel, as a red box under the status (panel d shows the tunnel-down case).
- [x] "removing…", no buttons: the cell, with a spinner (panel d).
- [x] Exit not seen: the panel says "exit not seen yet". The proxy column stands alone, with no IP group.
- [x] Shared-exit warning: IP headers group exits; the amber alert line; amber outline on the clashing cells; the panel repeats today's warning text before Run.
- [x] Rotating proxy: its column header says "rotating" and its cells are never grouped with another column.
- [x] Start confirmations (`confirm_proxy_start_targets`, `deploy_target_changed`): unchanged dialogs, triggered from Start in the panel.
- [x] Routed services: a cell in the proxy's column labelled "routed", with no direct cell for that box.
- [x] Add or edit form: Name, Type (SOCKS5, HTTP CONNECT, Tailscale exit node), Host, Port, User, Password, Remove stored user, Remove stored password, Auth key, Exit node, Login server, Traffic cap, Stop at, Reset day, Rotating exit IP, Save (panels a1 and a2). Kind switch shows and hides the same field sets as today.
- [x] Edit mode: title "Edit {name}", secrets empty, Remove ticks shown, "stored" mark; the meta line says a new host or port needs the secrets again (`host_changed_type_again`).
- [x] Server validation toasts: unchanged.

### Run a copy

- [x] Box: "Run it on" select in the panel. Only boxes with `proxy_tunnel` where the service is deployed. With none: the panel says "No box can run proxied copies yet" and the cells show "deploy first".
- [x] Service: the row. Proxy: the column.
- [x] Run the copy, with the "can take up to a minute" hint and today's toasts.
- [x] Eligibility rule text (`fleet.copy.limits`): bottom of the panel for a refused service (panel b).
- [x] Refusal text per service: tooltip on "not possible" and the panel (panel b).
- [x] PR #940 needs: tick list in the panel, Run disabled until each is ticked; "needs failed" text plus Retry in the panel; the own-volume line as a "Data" row in the panel's list.
- [x] Risk tick for Honeygain (`account_risk`): panel b.

### Add a box

- [x] Image line, Desktop line, Docker line: the three ways on the left.
- [x] Env block, key status badge, Reveal / Hide, Copy: the right column (same ids, same handlers).
- [x] Clipboard fallback textarea, loopback note, key note: unchanged places (fallback under the env block; notes under the three ways).
- [x] Viewer: no Reveal, no Copy, as today.

## Implementation cost (rough)

| Part | Work |
|---|---|
| `fleet.html` template | Replace lines 52-170 (about 120 lines) with about 150. |
| Running costs JS (`loadFleetEconomics`) | Rewrite the row builder as table rows, about 180 of its 220 lines. Add header sort, about 25 lines. |
| Proxies JS | Replace `render()`, `renderExits()` and the copy form wiring (about 150 lines) with: a grid builder (about 150), the panel (about 150), cell states (about 50). Net about +200 lines. The handlers (Test, Edit, Delete, Reset, Stop, Start, Remove, add, edit, the start confirmations) stay as they are. |
| `style.css` | About 170 new lines for the grid, the panel, the cap bar, the form columns and the cost tables. Use new class names for the two tables (`.costs-table`, `.proxy-table`), because `.fleet-table` stacks and hides its head under 1100 px for the Boxes table. |
| Server | Nothing for the data the grid shows: deployed services per box come from `/api/workers` `containers`, own IPs from `system_info.egress_ip`, copy state and `held` (stopped by the owner or the cap) from `system_info.proxied`. One addition is needed so cells can say "+ copy", "not possible" or "1 tick" without one request per cell: return the refusal and the needs for each (box, service, proxy) in `GET /api/proxies`, or add one batch endpoint next to PR #940's `copies/needs`. About 60 lines plus tests. The cheaper path is to call `copies/needs` on hover or focus, but then cells cannot show the tick count up front. |
| Shared-IP logic | Client side, from the same egress data and the same rules as `app/egress.py`: an unseen exit or a private address is never grouped. A conflict is the *same service* twice on one IP, not any two services. About 40 lines. |
| Desktop | Probably none. The mirror rule in `CLAUDE.md` covers the catalog, the deploy route and the deploy form, not the Fleet page. I did not check Desktop's own code. |

Scaling: with many proxies the grid gets wide. It should scroll sideways inside `.table-scroll` with a sticky first column (not built in the mockup). Past about six exits, the own-line columns could fold into one "own lines" column that lists boxes per cell. That is not built in this mockup.

## What it needs from i18n

About 70 new keys under `fleet.costs.*`, `fleet.proxy.*`, `fleet.copy.*` and a new `fleet.matrix.*`. Each needs all locales in `app/i18n/`. No text sits in an image. Every label is HTML text, so it stays translatable.

- Running costs: sub-titles (Machines, Per service), "Last month", "Last 30 days", column heads (Machine, Earned, Power, Net), sort label, short statuses (needs watts, needs a price, not billed per kWh, not reporting), the shared notice for missing watts, the estimate note, "{n} of {total} cost more than they earn" (plural).
- Proxies: "Test from", "Goes through", "Exit IP", "Same IP as {box}'s own line", "{n} running" and "{n} stopped by the cap" (plural), "See them in the matrix", the new meta line.
- Grid: title, meta, six legend labels, "box, own line", "proxy, {kind}", "{n} exits share this IP" (plural), "from {box}", "same IP", "IP in use", "risk", "{n} tick(s)" (plural), "not possible", "deploy first", "routed", "removing…" (exists), the alert line "{service} leaves twice from {ip}: …", the phones note.
- Panel: the intro (title, five lines, two closing lines), labels (Run it on, New container, Leaves from, Provider sees, The original, Status, Runs on, Container, Data), "keeps running on {box}'s own line", "a new device, {name}", "stopped by you", "{name} cannot run through a proxy", Close, Cancel, "Test the proxy".
- Form: three fieldset legends, three type hints, "stored", the cap hint, the rotating hint, the edit meta line.
- Add a box: three way titles. The existing `deploy_image_html` and `desktop_html` split into a title and a line each.

Reused as they are: every toast, confirm, validation error, refusal (`api.*`), tick text (PR #940), cap text (`cap_reason`), and the env block strings.

## Open points for the owner

- The panel beside the grid takes 400 px at 1440. Under 1100 px it moves under the grid. On a phone the grid scrolls sideways.
- The grid is owner only, like the Proxies block today. It also shows direct deployments and shared IPs between boxes, so a read-only version for viewers is possible later.
- "Stopped by you" against "failing" uses the heartbeat's `held` flag. An older worker does not send it. Then the cell shows the raw Docker status word, as today.
