# Recommended design: tidy tables, a card per proxy, a checked copy

This design is the one to build. It takes design 1 (tidy) as the base and adds the ideas that the three judges agreed on. It fixes every defect that they listed for the parts it keeps.

Files:

- `index.html`: the mockup. It links `app/static/css/style.css` and adds about 240 lines of CSS for the new parts. The only JS flips the Heat toggles and makes the risk ticks of panel (b1) and (b4) turn Run on and off.
- `shot.png` (1440 px) and `shot-narrow.png` (900 px), full page, rendered on the MacMini.
- The main view is at the top. Panels (a) to (g) under it show the other states. The cyan labels and dashed boxes are mockup furniture.

## 1. Why design 1 is the base

Two of the three judges picked design 1. The third picked design 3, and his grafts move design 3 toward design 1's tables. Design 1 is also the cheapest to build:

- It keeps every element id, form and handler that exists today.
- It needs no change in `app/static/js/app.js` and no API change.
- Its copy check box sits where PR #940 puts `#copy-needs`, so #940 rebases onto it.
- It already draws the most states, close to today's text.

## 2. What changed from today

### Running costs

| Today | This design |
|---|---|
| Five full-width blocks. Each repeats "X earned N last month. Without this machine's power draw…" | One table, **By machine, per month**: Machine, Earned, Power draw, Electricity, Net, Heat. One shared note under it. |
| No way to fix a missing power draw from here | **— Set in Boxes** in each row. The button scrolls to that machine's watts field in the Boxes table and puts the cursor in it. Its screen-reader name holds the machine: "Set the power draw of geiserback in the Boxes table". |
| A Heat disclosure under every machine | A **Heat** column. The button shows the current source ("None", "A heat pump"). It opens the form in a full-width row under the machine. Its screen-reader name is "Heat of {machine}: {source}", and `aria-controls` points at that row. |
| Heat credit only as "+ credit" in a sentence | The Net cell has a muted second line, "incl. heat +$1.12". |
| `$0.08 − $0.88 = −$0.80` far right of the name | A second table, **By service**: Service, Earned, Electricity, Net. Sorted by net, highest first. The head says "6 of 11 earn more than their electricity". Red only for a negative net. No green, and no minus sign on the electricity cost. |
| Nothing says why service costs exist while machine costs are unknown | One note: a machine with no watts counts as 65 W or its processor's rated power, so these costs are an estimate. |

At 1440 px the two tables sit side by side. Under 1100 px they stack. The service table stays at most 640 px wide, so its numbers stay near the service names when it stacks.

No totals row and no "Earned" tile. The machine total ($51.08) and the header total ($52.07) differ, and two totals that disagree raise a question this block cannot answer.

No net bar. With the owner's data, honeygain ($17.88) sets the scale, so the five losers get bars of 2 to 5 px. That hides exactly the rows that need attention. The sort and the red number carry the same fact.

### Proxies

| Today | This design |
|---|---|
| "Add a proxy" only at the bottom of the block | **+ Add a proxy** in the block head. The disclosure at the bottom stays, and Edit opens it and scrolls to it. |
| Nothing on the page says what a copy is | **What is a copy?** box under the head, open until the owner presses Hide once (`localStorage`). After Hide, a **What is a copy?** link in the block head and in the Run a copy lead opens it again (panel c2). A small grid with column heads (Service, Leaves through, Exit IP, Provider sees) and two rows, Original and Copy, built from the owner's own names. Beside it, five short facts. |
| One table. The Copies cell holds seven lines with buttons of different widths. | **One card per proxy.** The head holds the proxy's facts: name and target, **Exit IP providers see**, **Traffic**, and the actions. Under it, a table of the copies: Copy, Box, State, actions. |
| Test borrows the Box of the copy form, which nobody can see | **Test on [box ▾] Test** in the card head. |
| Test, Edit, Delete float far right | One action group in the card head, with a divider between Test and Edit/Delete. Each carries `aria-label="{action} {proxy name}"`, because a page can hold several cards. |
| Copy line "earnfm on watchtower: running via 203.0.113.71 · ES [Stop] [Remove]" | Status dot, slug, box, state word. **Stop/Start** and **Remove/Withdraw** are text buttons of one fixed width (86 px). Each carries `aria-label="{action} {slug}"`. |
| The exit IP repeats on every copy line | The exit shows once, in the card head. A copy line shows an exit only when it differs ("Exit not seen yet"). |
| Raw Docker words (`exited`, `dead`) | Translated state words, and one muted line under them that says what it means. The line comes from the copy's open alert when there is one, else from the state word. |
| "Proxied copies by the exit IP providers see", a bullet list that repeats every copy and says "(shared)" for 7 different services | **Exit IPs that providers see**: one row per IP. Columns: Exit IP, Who leaves from it, **What it means**. Amber only when the **same service** leaves from one IP twice. |
| Nothing says that this proxy exits from geiserct's own line | **"Same IP as geiserct's own line"** under the exit in the card head. The exit table counts box lines too, so a service that runs on geiserct and has a copy through this proxy shows as a clash. |
| No way to add a copy from the proxy | **+ Add a copy through this proxy** at the foot of each card. It opens Run a copy with that proxy chosen and scrolls to it. |

### Run a copy through a proxy

- One lead line: "Pick a box, a service that runs on it and a proxy. CashPilot checks the service before you run the copy."
- The same three selects. Under them, one hint that holds both rules, before any button: "The list holds only the services deployed on watchtower. A service that uses the host's network, publishes ports, keeps data in a host folder or needs a GPU cannot run through a proxy." The PR #940 tail "Each copy gets data volumes of its own" moves to the check box, where it shows only for a service that has volumes (b4).
- The selects, the check box and Run are in one `<form id="proxy-copy-form">`, so Enter submits and the PR #940 ticks belong to the form. `#copy-needs` has `aria-live="polite"`, so a screen reader hears the result of each check.
- The Service select has two option groups: "No copy through this proxy yet" and "Has a copy through this proxy". The page knows this from `GET /api/proxies`, with no new call.
- **A check box under the selects.** It holds the PR #940 `fillNeeds()` result, and Run moves into its foot. Each state:
  - Loading: a spinner and "Checking what iproyal needs behind this proxy…". Run is off.
  - Can run: green edge. "iproyal can run through this proxy. It needs no tick." Then four facts: New container `cashpilot-iproyal-p1`, Leaves from, Provider sees a new device `watchtower-p1`, The original keeps running on watchtower's own line. These facts replace design 1's diagram in this box, so nothing is cut at 900 px. No sentence repeats them.
  - Needs ticks: amber edge, the same four facts, then the heading "Read each risk. Tick it to accept it and run the copy:" and the PR #940 ticks. Next to the disabled Run: "Tick 1 more line to run the copy." Run has `aria-describedby` on that counter. The counter recounts on each tick, and Run turns on only when every tick is set (the mockup's (b1) panel works). The PR #940 heading "Behind a proxy this service is less isolated" is wrong for Honeygain, whose tick is an account risk, not isolation. So the copy form gets its own key, `fleet.copy.ack_title`.
  - Refused: red edge and the refusal text. Run is off.
  - Could not load: red edge, the PR #940 text, a **Retry** button. Run is off.
  - Already has a copy: "earnfm already has a copy through this proxy on watchtower. Run deploys that copy again with the current settings…". The button reads **Deploy the copy again**. This is what the API does today (`app/main.py:8865-8868`). It never promises a second copy.
  - Same service already leaves from this IP: an amber line inside the box ("earnfm already leaves from 203.0.113.71: from geiserct's own line, and from the copy on watchtower…"). Run stays on. Today this warning comes only as a toast after Run.
- No service on the box: the Service select reads "Nothing is deployed on this box yet" and the check says "Deploy a service on this box first. A copy uses the settings of that service." Run is off.

### Add a box

- Every string is word for word as today. Reveal and Copy stay ghost buttons, as today (`fleet.html:147-148`).
- Two columns at 1440 px: the two ways (server or phone, Desktop) on the left, Docker with the env block on the right.
- Panel (g) draws "Checking…", the revealed key with Hide API Key, the clipboard fallback textarea, the loopback note, "Not set", and the viewer's view. Its note covers "Unknown" and "(error)".

## 3. Grafts, and where each came from

| Graft | From | Where |
|---|---|---|
| Fixed-width labelled Stop/Start/Remove/Withdraw text buttons | 3-flow (judges 1 and 2) | copy rows |
| Visible **Test on [box ▾]** | 3-flow, 4-matrix (all three judges) | card head |
| "Same IP as {box}'s own line", and box lines in the clash check | 4-matrix (all three judges) | card head, exit table, check box |
| "What it means" column, amber only for the same service twice | 3-flow (all three judges) | exit table |
| "Each copy is a different service, so no provider sees two of its own devices here" | 2-cards (judge 1) | exit table, normal case |
| **+ Add a copy through this proxy** on each proxy, plus **+ Add a proxy** in the head | 2-cards (all three judges) | card foot, block head |
| Explainer open by default until hidden once | 2-cards, 3-flow (judge 1) | Proxies, under the head |
| Preview sentence with real names, and "Tick N more line(s)" counter | 3-flow (all three judges) | check box |
| Fact list before Run (New container, Leaves from, Provider sees, The original) | 4-matrix (judge 3) | check box, can-run state |
| Live check box with ok / ticks / refusal / error + Retry | 1-tidy (judge 1) | under the selects |
| Muted reason line under a copy's state word | 3-flow (judge 2) | copy rows |
| Service table sorted by net, with a "6 of 11" line | 2-cards, 3-flow, 4-matrix (judge 2) | Running costs |
| Plain colours in the ledger: red for a negative net only | 1-tidy (judge 1) | Running costs |
| "Set in Boxes" scrolls to and focuses that machine's watts field | 3-flow (judge 2) | Running costs |
| One help line per proxy type under the Type select (kept a select, not radio cards) | 2-cards (judge 3) | proxy form |
| "A user is stored." wording | 3-flow (judge 1) | proxy form |

Not taken: design 3's three-column pick flow and design 4's services × exits grid. Both need eligibility for every service, so a new batch endpoint. Both make the page much longer or wider. The select row plus the check box gives the same answer for the one service the owner picks.

## 4. Judge defects and how this design answers them

Design 1 defects (the base):

| Defect | Fix |
|---|---|
| Icon-only Stop/Start/Remove, about 12 px, a square that reads as a checkbox | Text buttons, 86 px wide, in fixed slots |
| aria-label only on the first copy row | Every copy button has `aria-label="{action} {slug}"` (new key `fleet.copy.action_label`) |
| The proxy row reused the copy columns ("Box" read "7 copies", "State" read "tested") | The proxy is a card head with its own labelled facts. The copy table has its own head: Copy (7), Box, State. |
| "7 copies share it" and "shared" fire for any services | Removed. The exit table says what sharing means in words, and warns only for the same service twice |
| The diagram cut its device column at 900 px | The explainer is a grid that fits 900 px whole (shot-narrow). The check box uses a fact list, which wraps |
| Run a copy and Add a proxy collapsed at the bottom, explainer not open | The explainer is open by default. **+ Add a proxy** and **+ Add a copy through this proxy** open and scroll to the forms |
| Test box hidden in the copy form | **Test on [box ▾]** in each card |
| "not tested" not drawn | Panel (e), third card |
| PR #940 "tripped" line and per-service notes not drawn | Panel (d) bitping row; panel (f) notes |
| Fuel price field not drawn | Panel (f), geiserct heat row |
| Test/Edit/Delete stacked into 3 rows and "No cap" wrapped at 900 px | The card head goes to two rows at 900 px: name and actions, then exit and traffic. The actions stay on one line |
| Exit table right edge did not line up with the proxy table | Both are full width |
| Device watts input had no visible label | "Wall draw (W)" label, `for` the input |
| `.fleet-table` card rule under 1100 px hides the heads | `.fleet-table.tidy` sets `display: table` and keeps its `thead` (in the mockup CSS) |
| The exit table repeated every slug | It still lists members, because that is how the owner finds the clashing pair. The copy rows no longer repeat the exit, so each fact shows once |

Defects of the other designs that this design avoids:

| Defect | How it is avoided |
|---|---|
| 2-cards: $51.08 tile against the $52.07 header | No totals |
| 2-cards: drawers with focus traps, More ▾ menu | No drawers, no menu. Edit and Delete stay one click |
| 2-cards, 4-matrix: Add a box text cut | Word for word |
| 2-cards: flag emoji | None |
| 2-cards: explainer line unclear for honeygain | "CashPilot refuses those services, or asks you to accept the risk first" |
| 3-flow: invented heat state in the main view | Main view shows the owner's state: Heat "None" on every machine |
| 3-flow: Running costs repeated "No watts yet" plus a button on every row, plus a callout | One short cell per row and one note |
| 3-flow: "deploy it again" promised a refused action | The API redeploys a copy record. It refuses only when the service itself is routed through that proxy. The check box says "Deploy the copy again" for the first case and shows the refusal for the second |
| 3-flow: progress panel that one 180 s POST cannot feed | Not drawn. The toasts stay as today |
| 3-flow: strikethrough for refused items | Refused text is plain, in the check box |
| 3-flow: needs two server additions | One optional addition (copy alert line, section 7) |
| 4-matrix: reasons only on hover | Every reason is visible text |
| 4-matrix: Stop takes two actions | One click |
| 4-matrix: assumed deploy list shown as fact | The main view states its one assumption in a cyan mockup note. The clash shows in panel (d), labelled as example data |

## 5. Action checklist against BRIEF.md

| Action (BRIEF ref) | Where | Drawn in |
|---|---|---|
| Price, currency, Save, help (1.1, 1.2) | Settings row, same ids | main |
| Quality line `economics.summary` | Block meta | main |
| Machine rows: name, gross, cost, heat credit, net, verdict (1.3) | Machine table; verdict line under the name when it adds a fact | main, (f) |
| Not reporting, not billed per kWh, earned nothing, losing money (1.7) | Verdict line; gross "—" when not reporting; Electricity "not billed" and no Heat button when not billed | (f) |
| Price missing; watts set with no price (1.7) | Electricity "needs a price"; break-even line kept | (f2) |
| Break-even, you pay, heating months (1.3) | Verdict line | (f) |
| Per-machine watts | Stays in the Boxes table. "Set in Boxes" jumps there | main |
| Device watts form, miner hint, accrued title (1.5, 1.3) | Power draw cell of a device row; title on the Earned cell | (f) |
| Expected line for a device (1.3) | Verdict line | (f) |
| Heat form: source, COP, fuel price, 12 months, Save (1.4) | Heat column toggle, form row | (f) heat pump and fuel |
| Not billed per kWh: no Heat form | Stated | (f) note |
| Per-service rows and their four notes (1.6) | Service table and notes | main, (f) |
| Proxy list: name, target, Tailscale exit, exit, rotating, not tested, last test failed (2.2) | Card head | main, (e) |
| Traffic: no cap, cap line, stopped by the cap, Reset (2.2) | Card head, with a meter | main, (e) |
| Test (2.6) with its box | Card head, Test on select | main |
| Edit, Delete (2.6) | Card head | main |
| Copy Stop / Start / Remove (2.6) | Copy row | main, (d) |
| Withdraw, reduced isolation (PR #940) | Copy row | (d) |
| Recovery skipped, tripped (2.2, PR #940) | Amber line under the state | (d) |
| Copy removing | "removing…", buttons hidden but keep their slot | (d) |
| Stopped by the cap; Start off while the cap holds | Reason line, disabled Start with the cap reason as title | (e) |
| Start confirmations (2.7) | Unchanged confirm dialogs | n/a |
| Exit groups, rotating group, unseen group (2.3) | Exit table rows | main, (d), (e) |
| Same-service warning (2.3) | Exit table and check box, before Run | (d), (b7) |
| Add / edit proxy, all fields, three kinds (2.4) | Three fieldsets, help column | (a1) SOCKS5 edit, (a2) Tailscale add |
| Keep or remove stored user and password | "A user is stored.", placeholder, Remove ticks, Cancel | (a1) |
| Traffic cap, stop %, reset day, rotating | Traffic fieldset | (a1), (a2) |
| Run a copy: Box, Service, Proxy, Run, rule (2.5) | Copy form and check box | main |
| Needs check: refusal, ticks, own volume, error + Retry (2.9, PR #940) | Check box | (b1) to (b5) |
| UDP through SOCKS5 refused (PR #940) | Check box | (b3) |
| Honeygain account-risk tick | Check box | (b1) |
| No proxies; no box can run copies; no service on the box (2.8) | Empty state; Box and Service select texts and check text | (c) |
| Proxies loading, load error (2.8) | Spinner line; muted error line | (c2) |
| Explainer hidden, and back | "What is a copy?" link | (c2) |
| Add a box: image, Desktop, Docker lines, env block, key status, Reveal/Hide, Copy, fallback, loopback, key note (3) | Two columns | main, (g) |
| Viewer: no Proxies, no Heat, no device form, no Reveal or Copy (0.5) | As today | (g) note |

## 6. Implementation plan

All in `app/templates/fleet.html` and `app/static/css/style.css`. No change in `app/static/js/app.js`.

1. **CSS** (`style.css`, about +230 / −25). Add: `.fleet-table.tidy` (keeps its head under 1100 px), `.costs-grid`, `.heat-row`, `.heat-grid`, `.explain` and `.lanes`, `.px-card`, `.px-head`, `.px-acts`, `.cp-table`, `.cp-acts`, `.why`, `.meter`, `.exits-table`, `.fs` and `.form-grid`, `.aside`, `.copy-check` states and `.copy-foot`, `.addbox-layout`. Remove the dead `.economics-row`, `.economics-figures`, `.economics-service-row` rules and their 760 px override. Add the missing `.badge-warning` rule for PR #940, or use `.flag.flag-warn` as the mockup does.
2. **Running costs** (`loadFleetEconomics()`, about 90 of 220 lines rewritten). Build `<tr>` rows. Show the summary line only when it holds a fact the columns lack. The client tells "price missing" from "watts missing" with `economics.tariff_price_per_kwh`, so no API change. Move the heat form into a detail row with a toggle. Keep the "skip refresh while editing" guard: it already checks for an open heat or device form. Sort `net.services` by `net`. "Set in Boxes" calls `scrollIntoView` and `focus()` on `#watts-{client id}`, the watts input of that worker's row in the Boxes table (`fleet.html:609`).
3. **Proxies list** (`render()`, about 110 lines). One `<article>` per proxy: head, then a copies table. A state-word map (`fleet.copy.state.*`) and a meaning map (`fleet.copy.why.*`). Text buttons with `data-copy` and `data-cmd`, as today, so the click handler does not change. Test reads its box from the card's own select, not from `#copy-worker` (about 10 lines).
4. **Own-line IPs and the clash check** (`renderExits()`, about 40 lines). From `GET /api/workers`, which this script already loads, build `{egress_ip → box}` from `system_info.egress_ip` and `{box → deployed slugs}` from `containers` (use `egress.container_slug` logic: the key is `slug`). Skip IPs that are missing or private, as the "undetected is not shared" invariant demands. Then: mark a proxy whose `last_exit_ip` equals a box line; add box lines to the exit group of that IP; flag a group where one slug appears twice. Never flag a rotating or unseen exit.
5. **Explainer** (about 15 lines). Fill the Copy row from the first proxy and its first copy. With no copy, use the generic words of panel (c). Hide writes `cp.fleet.copyExplainHidden=1` to `localStorage`.
6. **Run a copy** (about 60 lines on top of PR #940's `fillNeeds()`). Add the option groups from the proxy's copies. Add the "can run" branch with the sentence and fact list. Add the counter that recounts on each tick. Add the "has a copy" and "same IP" branches; both use data already on the page. "+ Add a copy through this proxy" sets `#copy-proxy`, opens `#proxy-copy-box` and scrolls to it. Without PR #940 the check box shows only the client-side branches until Run, as today.
7. **Proxy form** (template only, about 40 lines). Fieldsets and the help column. The help line under Type follows `showKind()`. "A user is stored." shows when `secrets.username` is true. Cancel calls `editForm(null)`. Edit now also scrolls the form into view.
8. **Add a box** (template only). Wrap the existing nodes in the two-column grid. Keep every id and string.
9. **Optional server addition** (about 25 lines plus a test). Put `alert: {key, params}` on each copy in `GET /api/proxies` from the open `alert.proxied.*` row, so the reason line can say "The tunnel of this proxy on watchtower has not been running since 09:12 UTC." Without it the line uses the state-word meaning. Ship the rest first.
10. **Checks.** Update the template tests that look for the copy-line text (`fleet.proxy.copy_on`, `copy_via`). Extend `scripts/copy_needs_check.mjs` (PR #940) for the counter and the new branches. Drive the page at 1440 and 900 px in a real browser before merge.

## 7. i18n needs

New keys (English is in the mockup):

- Running costs: `fleet.econ.by_machine`, column heads `fleet.econ.col.{machine,earned,power,electricity,net,heat,service}`, `fleet.econ.power_not_set`, `fleet.econ.set_in_boxes`, `fleet.econ.needs_watts`, `fleet.econ.needs_price`, `fleet.econ.estimate_note`, `fleet.econ.sorted_by_net`, `fleet.econ.earn_more` (plural: "{n} of {total} earn more than their electricity"), `fleet.econ.incl_heat` ("incl. heat +{money}"), `fleet.econ.not_billed`, `fleet.econ.set_in_boxes_label` ("Set the power draw of {machine} in the Boxes table"), `fleet.heat.toggle_label` ("Heat of {machine}: {source}"), `fleet.heat.short.none`.
- Explainer: `fleet.copy.explain.title`, `.hide`, column heads `.service`, `.through`, `.exit`, `.sees`, row labels `.original`, `.copy`, values `.own_line` ("{box}'s own line"), `.own_ip`, `.device` ("device {name}"), the five facts `.f1` to `.f5`, and the generic values for panel (c).
- Proxy card: `fleet.proxy.add_button` ("+ Add a proxy"), `fleet.proxy.exit_seen_label` ("Exit IP providers see"), `fleet.proxy.traffic_label`, `fleet.proxy.test_on`, `fleet.proxy.same_as_line` ("Same IP as {box}'s own line"), `fleet.proxy.press_test`, `fleet.proxy.col.copy` ("Copy ({n})"), `fleet.proxy.col.box`, `fleet.proxy.col.state`, `fleet.proxy.add_copy_here`, `fleet.proxy.no_copies`, `fleet.proxy.action_label` ("{action} {proxy}").
- Copy states: `fleet.copy.state.{running,stopped,restarting,failed,missing,no_report,removing}` and meanings `fleet.copy.why.{stopped,missing,no_report,restarting,failed,cap}`, `fleet.copy.action_label` ("{action} {slug}").
- Exit table: `fleet.proxy.exits_title` (changed: "Exit IPs that providers see"), `fleet.proxy.exits_meta`, heads `fleet.proxy.exits.{ip,who,means}`, `fleet.proxy.exits.copies_on` (plural), `fleet.proxy.exits.and_line`, `fleet.proxy.exits.ok` (plural), `fleet.proxy.exits.twice` (plural count of leaves), `fleet.proxy.exits.rotating`, `fleet.proxy.exits.unseen`.
- Proxy form: fieldset legends `fleet.proxy.fs.{proxy,connection,traffic}`, `fleet.proxy.user_stored`, `fleet.proxy.password_stored`, `fleet.proxy.kind_help.{net,tailscale}`, the help column `fleet.proxy.help.*` (eight keys). Cancel reuses `app.cancel`.
- Run a copy: `fleet.copy.lead`, `fleet.copy.only_deployed` (now holds both rules), `fleet.copy.ack_title`, `fleet.copy.all_accepted`, `fleet.copy.no_service`, `fleet.copy.no_service_hint`, `fleet.copy.explain.show`, option groups `fleet.copy.group.{new,has_copy}`, `fleet.copy.checking`, `fleet.copy.ok`, `fleet.copy.no_tick`, `fleet.copy.risks` (plural: "after you accept {n} risks"), `fleet.copy.say_html`, fact labels `fleet.copy.fact.{container,leaves,sees,original}` and values, `fleet.copy.after_run`, `fleet.copy.ticks_left` (plural), `fleet.copy.cannot`, `fleet.copy.cannot_here`, `fleet.copy.has_copy`, `fleet.copy.deploy_again`, `fleet.copy.ip_in_use`, `fleet.copy.warning_no_block`, `fleet.copy.need_proxy`, `fleet.copy.no_box_hint`.
- Add a box: `fleet.add.way.{server,desktop,docker}`. No existing string changes.

No longer used: `fleet.proxy.copy_on`, `fleet.proxy.copy_via`, `fleet.proxy.shared`, `fleet.proxy.col.copies`. `fleet.proxy.col.proxy`, `col.exit`, `col.traffic` are replaced by the card-head labels.

About 110 new keys. Every locale needs them. The diff is mechanical. All labels are HTML text, so longer languages wrap. The explainer grid and the card head fall to one or two columns under 1100 px.

## 8. Rebase over the open PRs

All four touch `fleet.html`. Order of least pain: merge this after #940, then rebase #933, #946 and #947 over it, or the other way round. None of them edits the same lines as this design except #940.

- **#940 (proxies, ticks).** The only real overlap. It edits the copy form (`#copy-needs`, `#copy-run`, `fillNeeds()`, the ack ticks), the copy line (badge, Withdraw, tripped) and `fleet.copy.limits`. This design keeps every one of those ids and moves `#copy-run` into the check box foot. The copy-line changes move from a `<div>` string into a `<tr>` builder. Best order: merge #940 first, then build this on top. Its `badge-warning` gets a CSS rule here, or becomes `.flag.flag-warn`.
- **#933 (Secure VM) and #947 (security layers).** Both add rows inside the Boxes table and touch `style.css` and `app.js` elsewhere. No line overlap with these three blocks. One link: "Set in Boxes" must find the watts input of a worker row, and both PRs add sub-rows under each worker. Select the input by its id, `#watts-{client id}` (`fleet.html:609`), never by row position. The economics row needs that client id; `machines[]` carries the machine name, so the builder maps name to client id from `GET /api/workers`. #947 adds the refusal `api.runtime_choice_routed`; it shows in the check box only after Run, as a toast, like today.
- **#946 (image updates).** It adds a new owner-only section, **App image updates**, between Proxies and Add a box, and a script tag. This design does not move that boundary. The new section uses `.block-head` and fits the same rhythm. The `style.css` edits sit in other rules; a rebase there is a plain merge.

## 9. Open points for the owner

- The main view assumes that none of the seven copied services also runs directly on geiserct. If one does, the page shows the amber clash of panel (d), and that copy earns nothing for a provider with one device per IP. The page computes this from the Boxes data; the screenshots do not show it.
- The explainer is open until hidden once. It could also close by itself after the first copy runs. We kept one rule: the owner decides.

## 10. Adversarial check, 2026-11-28

We went through BRIEF.md element by element and drove the mockup in Chromium on the MacMini at 1440 and 900 px. These gaps were found and fixed:

| Gap | Fix |
|---|---|
| The ok check box said each fact twice: a sentence ("gets a second device… leaves through… keeps watchtower's own IP"), then the fact list with the same facts | The sentence is gone. Every can-run state (ok, ticks, same IP) shows the same four facts and nothing else |
| The eligibility rule sat under the box, after Run | One hint under the selects holds both rules, before any button |
| `#copy-run` and the ticks were outside `<form id="proxy-copy-form">`, so the submit button had no form | The form wraps the selects, the check box and Run |
| Run gated by the ticks only on paper | The (b1) and (b4) panels run a small script: Run turns on only with every tick set, and off again on untick. Proved in Chromium |
| The PR #940 heading "less isolated" over the Honeygain account-risk tick | Own heading, `fleet.copy.ack_title`: "Read each risk. Tick it to accept it and run the copy:" |
| Hide on the explainer had no way back | "What is a copy?" link in the block head and the Run a copy lead (c2) |
| "Has a copy through this proxy" listed 3 of the 7 copies | All 7 |
| Panel (d) put a restarting copy in the "Exit not seen yet" group, but only running copies are grouped | The restarting copy is proxybase; proxyrack on geiserback runs with an unseen exit |
| 900 px: the machine table was 3 px wider than its box (the Heat chevron past a zero right padding), and panel (f) 194 px wider | Right padding on the action cell; "— Set in Boxes" replaces "not set Set in Boxes"; Heat labels and the device form wrap under 1000 px. Both widths now have scrollWidth equal to the viewport and no element past its box |
| (f) machine verdicts wrapped to 4-6 lines in a narrow column | The Machine column takes 40% |
| Stacked at 900 px, the service numbers sat 470 px from their names | The service table is at most 640 px wide |
| Screen readers heard "Set in Boxes", "None", "Test", "Edit", "Delete" with no machine or proxy | `aria-label` with the machine or proxy name on each |
| Not drawn: not reporting, not billed per kWh, earned nothing, price missing, miner hint, accrued title | Rows in (f), panel (f2) |
| Not drawn: Proxies loading and load error; no service on the box | (c2), (c) note |
| A new Tailscale proxy showed "kept if empty, unless the login server changes" for an auth key that is not stored yet | Add mode shows no placeholder; edit mode keeps it |
| NOTES said Copy "stays the pink primary button"; today it is a ghost button | Ghost, as today |

Checked and found right: every action of BRIEF.md sections 1 to 3 has a place (section 5); muted text `#a59cb5` is 7.15:1 on cards (`#11111d`), 7.48:1 on the page and 6.32:1 on a hovered row; the automated pass found no text under 4.5:1 (disabled buttons are exempt and use the app's own 0.4 opacity); the tab order follows the page: price, currency, Save, each machine row, How it works, Add a proxy, Hide, each card's Test on, Test, Edit, Delete, each copy's Stop and Remove, Add a copy, then the forms and Add a box.

Left as is: at 1440 px the Stop and Remove buttons of a copy sit at the right edge of the card, about 600 px from the state word. They line up in one column, and the row hover of `.fleet-table` joins them to their copy.
