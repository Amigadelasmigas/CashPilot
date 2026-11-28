# Design 1: tidy in place

The blocks and their order stay as they are today: Running costs, Proxies (list, exit IPs, Add a proxy, Run a copy), Add a box. Only the layout changes. Text that holds numbers goes into real tables with aligned columns. Forms go into a 2-column grid with grouped fieldsets. Run a copy gets one lead sentence and a small diagram.

Files:

- `index.html`: the mockup. It links `app/static/css/style.css` and adds about 150 lines of CSS for the new parts. The only JS flips the Heat toggle.
- `shot.png`: 1440 px wide, full page. `shot-narrow.png`: 900 px wide. Both rendered on the MacMini.

## 1. What changed, and why

### Running costs

| Today | This design | Why |
|---|---|---|
| One full-width block per machine, with a 30-word sentence that repeats the name and the amount | One table, **By machine, per month**: Machine, Earned, Power draw, Electricity, Net, Heat | Five sentences said one thing five times. A column says it once per row. |
| The reason "no power draw" inside every sentence | A **not set · Set in Boxes** cell per row, and **one** note under the table | The reason is the same for all five machines. The link goes to the place where the watts are typed (`docs/fleet.md:235`). |
| `Heat` disclosure under each machine | A **Heat** column. The button shows the current source ("None", "A heat pump"). It opens the heat form in a row under the machine. | The setting is readable without opening it. The form gets the full table width, so the 12 months sit on one line. |
| Per service: name left, `$0.08 − $0.88 = −$0.80` far right | A second table, **By service, where the cost can be attributed**: Service, Earned, Electricity, Net. Numbers right-aligned in mono, next to the names. Negative net in red. | Columns can be scanned and compared. At 1440 px the two tables sit side by side, so the numbers are never far from their labels. |
| Nothing says why service costs exist while machine costs are unknown | One note: "A machine with no watts set counts as 65 W, or as the rated power of its processor. The service costs are an estimate until you set the watts." | The page showed a contradiction with no explanation (`docs/fleet.md:241`). |
| Price, currency and Save on one row, help text in the same row | The same three controls, with the help text as a hint line under them | Less crowding. Same actions. |

The machine sentence (`summary`) still shows under the machine name when it holds a fact the columns do not: a break-even price, a loss ("turning it off would save that"), "not reporting", "not billed per kWh", "earned nothing". When the only fact is "power draw missing" or "price missing", the shared note replaces it. Panel (f) shows a known-cost table with a profit row, a loss row, an open heat form and a tracked device with its watts input.

### Proxies

| Today | This design | Why |
|---|---|---|
| 4 columns. The Copies cell holds 7 lines of text, each with Stop and Remove buttons of different widths | One table. A proxy row (shaded) and one compact row per copy under it. Columns: Proxy and its copies, Box, State, Exit IP, Traffic, actions. | Each fact has its own column, so the rows align. |
| Copy line "earnfm on watchtower: running via 203.0.113.71 · ES [Stop] [Remove]" | Status dot, slug, box, state word, exit IP, two icon buttons in fixed slots | The buttons no longer zig-zag. The same exit IP as the proxy shows muted. A different one shows bright. |
| Test, Edit, Delete float far right | One joined button group, the same width on every proxy | One place for proxy actions. Under 1000 px the group stacks. |
| Traffic as one sentence | The sentence, plus a small bar with a mark at the stop percentage, plus Reset next to the bar | The bar shows how near the cap is. It turns amber within 5 points of the stop line and red when the cap holds. |
| Bullet list "Proxied copies by the exit IP providers see" that repeats every copy | A small table, **Exit IPs that providers see**: one row per exit IP, the count, the services, a **shared** flag. One note: what sharing an IP means. | One line per IP, not one bullet per copy. The proxy row also carries a flag "7 copies share it". The note says why it matters. |
| Add a proxy: fields of mixed widths, checkboxes under inputs, cap/stop/reset/rotating on one crammed row | Three fieldsets on a 2-column grid: **Proxy** (Name, Type), **Connection** (Host, Port, User, Password, or Auth key, Exit node, Login server), **Traffic** (cap, stop %, reset day, rotating). A short help column on the right explains the chosen type. | Every field has the same width in its column. The help text that today lives only in `docs/proxies.md` shows next to the form. |
| Edit mode shows only empty secret boxes | A muted **stored** label next to User and Password when a secret is stored. The Remove ticks sit under their own input. A **Cancel** button leaves edit mode. | The user can see that a secret exists. Cancel calls the existing `editForm(null)`. |

### Run a copy through a proxy

- **Lead sentence**: "A copy is a second container of a service that already runs on a box. Its traffic leaves through the proxy, so the provider sees one more device on a different IP."
- **Diagram**, two lanes, built from HTML text (all labels translatable):
  - Original: `earnfm` → watchtower's own connection → watchtower's IP → device `watchtower`
  - Copy: `earnfm` → geiserct exit node (Tailscale) → `203.0.113.71 · ES` → device `watchtower-p1`
  - Footer: "The original keeps running as before. If the proxy stops, the copy stops too. It never falls back to the box's own IP."
  - The labels follow the three selects, so the diagram always shows the copy the user is about to run.
- **The same three selects** on one row, with **Run the copy** at the end.
- **A check box under the selects** (green, amber or red left edge). It holds the PR #940 `fillNeeds()` result: "earnfm can run through this proxy. It needs no tick.", or the refusal text, or the tick list, or the "could not read" error with Retry. Run is off while it loads, when refused, and until every tick is set.
- **Three hint lines**: only services deployed on the chosen box are listed (this answers "why is my service missing"); the eligibility rule (`fleet.copy.limits`); what happens after Run (tunnel first, up to a minute, then the copy shows under its proxy).

### Add a box

- Two columns at 1440 px. Left: the server or phone line and the Desktop line, each with a short bold label. Right: the Docker line, then the env block with the key status left and Reveal and Copy right, then the key note.
- No text changed. Panel (g) shows the revealed key, the clipboard fallback textarea and the loopback note.

## 2. Each complaint, and how this design answers it

| Complaint | Answer |
|---|---|
| After Running costs the page starts to look odd | Every block after the Boxes table now uses the same table style as the Boxes table: hairline rows, muted heads, right-aligned mono figures. |
| Running costs repeats the same sentence five times | One table row per machine and one shared note. |
| Per-service figures sit far from their labels | A 4-column table, beside the machine table at 1440 px, full width under it below 1100 px. |
| The Proxies view is not good | One aligned table, a compact row per copy, one action group per proxy, one line per exit IP. |
| The add-proxy form is a mess | Fieldsets on a 2-column grid. Help next to the form. |
| How "Run a copy" works is unclear | The lead sentence, the diagram with the user's own names, the check box that says yes or why not before Run, and the "what happens next" line. |

## 3. How a first-time user learns what a copy is

1. The Proxies meta line (unchanged): "Copies of a service that leave through a proxy instead of the box's own connection."
2. With no proxy yet (panel c): "A proxy gives a box one more public IP. A copy of a service runs through it, and the provider counts it as one more device." plus an **Add a proxy** button. Run a copy says "Add a proxy first."
3. Opening Run a copy: the lead sentence and the diagram, with the user's own box, service and proxy.
4. Choosing a service: the check box says at once if it can run, why not, or which risk to accept.
5. After Run: the hint says where the copy appears. It appears as a new row under its proxy.

## 4. Every action today, and where it lives now

Checked against BRIEF.md sections 1, 2 and 3.

| Action (BRIEF ref) | Where in this design | Shown in |
|---|---|---|
| Electricity price, currency, Save (1.2) | Settings row over the tables, same ids | main view |
| Help text `fleet.costs.help` | Hint line under the settings row | main view |
| Quality line `economics.summary` | Block meta, unchanged | main view |
| Per-machine watts | Stays in the Boxes table (as today). The Power draw cell links there. | main view |
| Device watts form (1.5), miner hint | Inside the Power draw cell of a device row | panel (f) |
| Heat form (1.4): source, COP, fuel price, 12 months, Save | Heat column toggle, form in a row under the machine | panel (f) |
| Break-even, heat credit, expected-hashrate lines | Small line under the machine name / in the heat row | panel (f) |
| Per-service costs (1.6) and their notes (withheld, unmetered, unknown, no heat) | Second table and notes under it | main view |
| Proxy list (2.2): name, target, exit, rotating, last test failed, traffic, Reset | Proxy row | main view, panel (e) |
| Test, Edit, Delete (2.6) | Button group on the proxy row | main view |
| Copy Stop / Start / Remove (2.6) | Icon buttons on the copy row (title and aria-label carry the words) | main view, panel (d) |
| Withdraw and "reduced isolation" (PR #940) | Same icon slot, title "Withdraw"; amber flag after the slug | panel (d) |
| Recovery skipped, tripped (2.2, PR #940) | Amber line under the slug | panel (d) |
| Copy removing | "removing…" in State, empty action slots | panel (d) |
| Stopped by the cap | Muted line under the slug; Start disabled while the cap holds | panel (e) |
| Start confirmations (2.7) | Unchanged: the same confirm dialogs | n/a |
| Shared-exit groups (2.3), rotating and unseen groups | Exit IPs table (one row per group) and the flag on the proxy row | main view |
| Add / edit proxy (2.4): Name, Type, Host, Port, User, Password, Remove user, Remove password, Auth key, Exit node, Login server, cap, stop %, reset day, rotating, Save | Three fieldsets | panels (a1) SOCKS5 edit, (a2) Tailscale add |
| Keep-or-remove stored secrets | "stored" label, placeholder, Remove ticks | panel (a1) |
| Run a copy (2.5): Box, Service, Proxy, Run, eligibility rule | Copy form, rule as a hint | main view |
| Eligibility check, refusal, ticks, own volume, load error with Retry (2.9, PR #940) | Check box under the selects | panels (b1) honeygain, (b2) storj, (b3) mysterium, (b4) error |
| Empty proxies (2.8) | Empty state with Add a proxy | panel (c) |
| Add a box (3): image line, Desktop line, Docker line, env block, key status, Reveal/Hide, Copy, fallback textarea, loopback note, key note | Two columns | main view, panel (g) |
| Viewer role | No Proxies block, no Heat form, no device watts form, no Reveal or Copy (as today) | note in panel (g) |

## 5. Implementation cost (rough)

| File | Change | Lines |
|---|---|---|
| `app/templates/fleet.html`, template | Running costs body container; proxy form into fieldsets plus help column; copy form with lead, diagram, check box, hints; Add a box in two columns | about 90 changed |
| `app/templates/fleet.html`, `loadFleetEconomics()` | Rows become `<tr>`; heat form moves into a detail row with a toggle; per-service rows become `<tr>`; one shared "missing" note (the client already knows the tariff from `economics.tariff_price_per_kwh`, so it can tell "price missing" from "watts missing" with no API change) | about 90 of the 220 rewritten |
| `app/templates/fleet.html`, Proxies script | `render()` builds proxy rows and copy rows; a state-word map; `renderExits()` builds a table; a 15-line `fillDiagram()`; the "ok" branch added to PR #940's `fillNeeds()` | about 110 |
| `app/static/js/app.js` | Nothing. `CP.formatCurrency` stays. | 0 |
| `app/static/css/style.css` | New: table cell helpers, copy row, status-dot grey, button group, meter, fieldset grid, help column, diagram, check box, two-column Add a box (about 150). Dead after the change: `.economics-row`, `.economics-figures`, `.economics-service-row` and the 760 px override (about 25). | +150 / −25 |
| Server | None. | 0 |

Two traps found while building the mockup:

- `style.css:2257-2258` turns every `.fleet-table` into `display:block` and hides its `<thead>` under 1100 px, for the Boxes table cards. The new tables must opt out (the mockup uses `.fleet-table.tidy { display: table }`), or the column heads vanish and the cells lose their grid.
- `.fleet-table td` breaks words anywhere (`overflow-wrap:anywhere`). At 900 px that split "watchtower" and "running" mid-word. The copy rows set `overflow-wrap: normal` and keep the box, the state word and the IP unbroken.

The design works with or without PR #940. Without it, the check box shows nothing until Run, as today.

## 6. What it needs from i18n

New keys (English text in the mockup):

- Running costs: `fleet.econ.by_machine`, column heads (`fleet.econ.col.machine`, `.earned`, `.power`, `.electricity`, `.net`, `.heat`, `.service`), `fleet.econ.power_not_set` "not set", `fleet.econ.set_in_boxes` "Set in Boxes", `fleet.econ.needs_watts` (shared note), `fleet.econ.needs_price` (same, for a missing tariff), `fleet.econ.estimate_note` (65 W), `fleet.heat.short.none` "None" (the other three sources reuse `fleet.heat.source.*`).
- Proxies: column heads `fleet.proxy.col.name` "Proxy and its copies", `.box`, `.state` (the existing `.exit` reads "Exit IP"), `fleet.proxy.copies_n` (plural), `fleet.proxy.tested`, `fleet.proxy.last_failed` plus `fleet.proxy.last_failed_sub` "on {worker}, {at}: {error}", `fleet.proxy.shared_by` "{n} copies share it" (plural), `fleet.proxy.exits_hint`, exit table heads, `fleet.proxy.empty_text`, `fleet.proxy.test_on` "Test on {box}" (title, so the Test box is no longer hidden).
- Copy states: `fleet.copy.state.running`, `.stopped`, `.restarting`, `.dead`, `.missing`, `.unknown`. Today the raw Docker word shows untranslated.
- Proxy form: fieldset legends `fleet.proxy.fs.proxy`, `.connection`, `.traffic`; `fleet.proxy.stored` "stored"; the help column (`fleet.proxy.help.net_title`, `.net`, `.secrets_title`, `.secrets`, `.rotating_title`, `.rotating`, `.ts_title`, `.ts`, `.authkey_title`, `.authkey`, `.exitnode_title`, `.exitnode`); Cancel reuses `app.cancel`.
- Run a copy: `fleet.copy.lead`, diagram labels (`fleet.copy.dg.original`, `.copy`, `.own_connection` "{box}'s own connection", `.own_ip` "{box}'s IP", `.device` "device {name}", `.foot`), `fleet.copy.ok` "{name} can run through this proxy.", `fleet.copy.no_tick`, `fleet.copy.only_deployed`, `fleet.copy.after_run`, `fleet.copy.need_proxy`, `fleet.copy.ticks_needed`.
- Add a box: `fleet.add.way.server` "Server or phone", `.desktop`, `.docker`.

Changed: `fleet.proxy.exits_title` becomes "Exit IPs that providers see". `fleet.proxy.shared` loses its brackets.

No longer used: `fleet.proxy.copy_on`, `fleet.proxy.copy_via` (the columns replace them). `fleet.econ.per_service` stays as the second table's title.

All labels are HTML text. The diagram is HTML, not an image. In languages with longer words the help column and the diagram wrap, and both fall below 1100 px and 1000 px.

## 7. Open choices for the owner

- A totals row under each table. Left out: the machine total ($51.08) and the header total ($52.07) differ because the header counts more than machines, and two totals that disagree would raise a question this page cannot answer.
- The Exit IPs table could hide when every IP group already shows in the proxy table (one proxy, one IP). Kept, because a shared exit is a warning and it should not depend on how many proxies exist.
- The flag "7 copies share it" counts all services, as `shared` does today (`app/proxies.py:615`). A warning for the same service twice on one IP would need the server to send it in `exits`.
