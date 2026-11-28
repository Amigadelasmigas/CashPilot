# Design 3: tabs by task

Settings becomes five tabs: **Overview**, **Data**, **Security**, **Notifications** and **About**. You see one tab at a time. The URL hash keeps the open tab. Overview is a checklist of what needs attention. Each line has a button that opens the right tab at the right control.

Files in this folder:

- `index.html`: the mockup. The live page at the top opens on Overview, and you can click the tabs. State panels (a) to (h) sit below it.
- `shot-1440.png`, `shot-900.png`, `shot-390.png`: full-page renders from the MacMini.

## What changed, and why

| Today | This design | Why |
|---|---|---|
| A 176 px side index with nine links. One of them, Import, opens another page. | A tab strip with five tabs. Import is a section inside the Data tab. Each tab shows a count when something in it needs you. | A page with nine long sections reads as one wall. Tabs group the sections by the job you came to do. A count on a tab tells you where to look before you open it. |
| No summary. You read every section to find the problems. | **Overview**: four figures (needs attention, collectors set up, boxes with passwords in a file, version), then "Needs attention" and "In order" lists. | The question on arrival is "is anything wrong?". The Overview answers it in one glance. It reuses the dashboard's attention rows (`.attn-row`), so it looks familiar. |
| Every section opens with a paragraph of 25 to 91 words. | Every section has the same head: a title, a state (a coloured square and 2 to 4 words), one or two short sentences (about 20 words), and the main buttons on the right. Everything else goes into **Learn more** disclosures, one per question ("Why this matters", "How to turn on file mode, and how to undo it"). | You see the state and the action first. The explanation stays one click away, and its summary line says what it answers. |
| "Earner credentials on each box" is 228 words of prose, one run-on sentence per box and a bare YAML block, with no control. | "Earner passwords on each box": four figures, a table with one row per box (box and kind, where passwords go, in a file, in Docker, what to do), a primary **Turn on file mode** button, and per-row buttons (**Show steps**, **Go to updates**). The steps are numbered, each code block has a **Copy** button, and undo is one line under them. | Per box, the status is a glance: mode, how many are protected, the next step. The how-to and the threat model sit in two disclosures. |
| Environment shows a "Save anyway" button that, by its own text, changes nothing. | Environment is a read-only list. "Store a value here anyway (it does not take effect)" is a disclosure that holds the inputs and **Save anyway**. | The control stays reachable, but it no longer looks like the way to change a setting. |
| One **Save credentials** button saves all 20 collectors at once. | Each open collector has its own **Save** and **Clear credentials**. Configured collectors show first. The 9 not set up fold into "Not set up yet (9): …". | You save what you just typed, next to where you typed it. The list is 11 rows, not 20. |
| Credential health **Update** opens nothing on Settings (brief §11.1). | **Update** opens that collector in the Data tab and focuses its first field. | It was a dead button. |
| Restore and the key steps put rules and steps into paragraphs. | Rules are short bullet facts. Steps are numbered. Risky steps (delete the key copy) get an inline confirm box in the section, in place of the browser's `confirm()`. | Numbered steps are easier to follow. An inline confirm can say exactly which file goes, and it matches the dark theme. |

### Term used on the page

- **File mode**: the worker setting `CASHPILOT_EARNER_SECRETS=file`. The section lede defines it on first use.
- **Docker settings / In Docker**: the container settings that `docker inspect` shows. The "What file mode protects against" disclosure explains it.

## How each listed problem is solved

1. **Import looks like a section but is a different page.** It is now a real section in the Data tab (`#set-import`), with a three-step strip: add your old config, pick what comes over, deploy it. The `/import` route becomes a redirect to `/settings#set-import`, so the 80 doc links keep working.
2. **Walls of text.** Each section has one or two short sentences on the main view, about 20 words. The longest is 26 words (the earner section, because it defines "file mode"). All longer text moved into disclosures. The Overview tab shows about 177 words, the whole page today shows about 890.
3. **Earner credentials is the worst.** The section is a status table with four figures, one row per box and one action per row. The realistic data reads: watchtower and geiserback "Docker settings", 0 in a file, 8 in Docker, "Turn on file mode, then redeploy 8 earners"; geiserct "Unknown: old worker", 0 and 7, "Update the worker first"; the two phones "Unknown: old worker", "Not reported", "Update the app on the phone". Panel (b) opens the steps. Panel (b2) shows a fleet halfway through the fix, plus the "Image cannot" state. Panel (c) shows every box protected.
4. **Status buried in prose.** Every section head has a state, and the Overview collects them. Example: "23 visible in Docker" next to the earner title, and "Earner passwords are visible" as the first Overview line.
5. **Inconsistent structure, explanations before controls, actions hard to spot.** Every section uses the same head (title, state, a short lede, buttons on the right). Then come the controls, then the disclosures. There is at most one primary (pink) button per section.

## Every action today, and where it lives now (BRIEF.md §14)

| # | Item | Where it is now |
|---|---|---|
| 1 | A way to every section, Credential health when it has rows, Notifications slot | The tab strip. Each tab with more than one section has an "On this tab:" jump line. The Credential health link hides with its section, as today. The Notifications tab is the slot. |
| 2 | Page-wide load error | Panel (h): one red box above the tab strip. Each section keeps its own error. |
| 3 | Deep links `#collector-<slug>`, `?highlight=<slug>`, `#set-restore`, `/import` | The tab script finds the element with that id, opens its tab, opens a `<details>`, and scrolls to it. Every section keeps its id. `?highlight=` runs after the tab opens. `/import` redirects to `#set-import`. |
| 4 | Collector name, badge, hint, fields, optional marker, "set — leave blank to keep" | Data › Earnings collection, unchanged inside each collector. |
| 5 | Save credentials | **Save** inside each collector. Same route (`POST /api/config`), sends only that collector's fields. |
| 6 | Collect now, running and triggered status | Data › Earnings collection head, right side. The status text sits before the button. |
| 7 | Clear credentials, with confirm | Inside each configured collector, next to **Save**. |
| 8 | "No collectors available." | Same place as the list. |
| 9 | Health per credential: service, field, age, lifetime, expiry, status, reason, durable hint | Data › Credential health. One row each; the reason and the durable hint are the small line under the age. |
| 10 | Update on a failing row | Same row. Now it opens the collector. |
| 11 | Hidden with no rows | Unchanged. The jump link hides too. |
| 12 | Device id row: service, field, masked value, box, copy, state, first/last seen, node/backup/unconfirmed hints, unreadable | Security › Device ids. One row each; hints are the small line under the value. |
| 13 | Show, Copy, Change (with "Use one this service had before", Use), Forget (both confirms) | Buttons at the end of each row. The Change form opens under its row, as today. |
| 14 | Add an id (form, "Add a box and a service first") | **Add an id** in the section head. The form opens under the head. |
| 15 | Download all (password) | **Download all** in the section head. |
| 16 | Empty, load error, reload error | Unchanged, in the list's place. |
| 17 | Restore: services covered, create-only rule, replace steps, CLI link | Section lede (services) and state ("Creates only, never overwrites"). The rule, the 3 replace steps and the CLI link are in "How restore works…". |
| 18 | File picker, Check file, checking, error | Data › Restore, on the main view. |
| 19 | Preview: container, volumes, rule, history or typed name, warnings, box select, passphrase, plain HTTP, Restore | Panel (f). The preview is a green-edged box; the unknown-file question is a yellow confirm box; the live-elsewhere warning is red. Plain-HTTP marks and the checkbox stay as today. |
| 20 | Done messages, not-checked error | Panel (f), "Done". |
| 21 | Why the key matters | Security › Key: lede + "Why this matters". |
| 22 | Every key status line | The status box under the head. Panel (e) shows the default, copy-left and done lines. |
| 23 | Move the key: Show (password), Copy, Hide, the steps with code, guide link, come-back step | **Move the key out of the data folder** opens four numbered steps (panel (e)). Each code block has **Copy**. |
| 24 | Delete the copy (confirm + password) | Panel (e): the button, then an inline confirm, then the password prompt. |
| 25 | Loading and load error | Unchanged. |
| 26 | What file mode protects against, and what not; guide link | "What file mode protects against, and what it does not". |
| 27 | Per box: name, mode, in file, in Docker, or "does not report" | The box table. |
| 28 | The variable line, recreate, redeploy, undo | "How to turn on file mode, and how to undo it", opened by **Turn on file mode** and by every **Show steps**. |
| 29 | Loading, error, "No workers yet." | Panel (b2) lists them. The error gets its own string (brief §11.3). |
| 30 | Env row: label, variable, lock, badge, value, description | About › Environment, the same `.kv-row` rows. |
| 31 | A value saved here does not take effect; where to set it | Section lede, and the disclosure's own title. |
| 32 | Save anyway and its messages | Inside "Store a value here anyway (it does not take effect)". |
| 33 | Empty state | Unchanged. |
| 34 | Server select, running, images, latest | About › About and updates. The server select moves to the section head. |
| 35 | The update button in three labels, notes, worker-only, UPGRADING link, already-running, not-Compose | Same place. The 86-word intro moves into "What the update button does". |
| 36 | Proxy policy warning, two commands, link | Same place, under the rows, when present (not in the realistic data). |
| 37 | Confirm, starting, started, failed; no worker; read error | Unchanged. |
| 38 | Import: what it does and does not do | Section lede + "Which files to add, and what CashPilot does with them". |
| 39 | Files per tool, 4 files and 64 KiB, guides | Hint under Files (the limits). The disclosure has the files per tool, and the guides are now real links (brief §11.7). |
| 40 | Tool select, files, paste, Check what comes over, three input errors | Step 1 on the main view. Paste folds into "Or paste one file instead". |
| 41 | Preview: Read as, notices, rows, field states, fill-in inputs, extras, Not imported, no-service state | Panel (d1). |
| 42 | Save the ticked services and its messages | Panel (d1). The button label carries the count ("Save the 3 ticked services"). |
| 43 | Drafts: Deploy to, each draft, Deploy, Forget, Deploy all, "Nothing imported yet.", stop-the-old-tool warning | "Saved imports" on the main view (empty state), and panel (d2) with drafts. The warning is above the box ticks. |
| 44 | Notifications slot | The Notifications tab, a dashed box labelled "Notifications (designed in the other PR)", plus one Overview line. |

## Things I did not invent

- The lane task asks for "API key revealed and regenerated". No regenerate action exists today for the encryption key or the fleet API key. Panel (e) shows the real actions: key revealed and copied, then **Delete the copy in the data folder**, with its confirm and its done state. Adding a regenerate would need a backend change and a key rotation for every stored credential, so it is out of scope.
- The earner table's **Open Dashboard** button (panel (b2)) links to the Dashboard. A link that filters to "earners still in Docker on this box" would help, but the Dashboard has no such filter today.
- "This page counts down as each one moves to a file" is true already: the counts come from each heartbeat.

## Implementation cost

| Part | Work | Rough lines |
|---|---|---|
| `settings.html` | Tab strip and five panels; Overview markup; new section heads; disclosures; Import markup moved in from `import.html`, with its ids kept (`import-source`, `import-files`, `import-paste`, `import-preview`, `import-drafts-body`, …) so `import.js` works unchanged. | 165 → about 300 |
| `import.html` / `pages.py` | `/import` answers 302 to `/settings#set-import`. Delete `import.html`. Load `import.js` on the Settings page. | −62, +4 |
| `app.js` | Tabs: role, aria, arrow keys, hash, open the tab of any section id (about 50). Overview builder from data already loaded on start (about 90). `earnerSecretsHtml` rewritten as table rows plus figures (about 70). Per-collector Save (about 15). Health **Update** opens the collector (about 10). Inline confirm helper for Delete key copy, Forget, Clear, and the unknown restore file (about 40, optional: the native `confirm()` still works). Counts on tabs (about 20). | about +300, −60 |
| `style.css` | The `st-` block from the mockup: tabs, section head, state, disclosure, steps, code block with copy, box table, rows, stepper, confirm, responsive rules. | about +200 |
| Backend | None. Every figure comes from routes the page already calls. The earner table uses the `status` field that is returned and not shown today (brief §11.4) only if we add an "offline" note; the mockup does not need it. | 0 |
| Docs | Section names in docs change: "Settings > Earner credentials" becomes "Settings > Security > Earner passwords on each box"; "Settings > Restore from a backup" becomes "Settings > Data > Restore from a backup", and so on (brief §9). The `/import` links keep working through the redirect. | about 25 doc lines |
| Tests | The 12 tests in brief §10 that read the markup by id or class. Most ids stay; the earner and import tests change the most. | moderate |

Total: about 550 to 650 changed lines, no backend change.

## What it needs from i18n

New keys in `en.json` (then the 19 locales):

- Tabs: `settings.tab.overview`, `settings.tab.data`, `settings.tab.security`, `settings.tab.notifications`, `settings.tab.about`, `settings.tab.count_aria` ("{n, plural, one {# needs attention} other {# need attention}}"), `settings.jump` ("On this tab:").
- Overview: `settings.ov.attention`, `settings.ov.in_order`, the four figure labels, one title + one line + one button per check (earner passwords, key, expiring credential, old workers, collection, device ids, version, import, notifications slot). About 30 keys, ICU plurals for the counts.
- Section states: about 20 short labels ("In the data folder", "Outside the data folder", "Copy left in the data folder", "{n} visible in Docker", "All in files", "Creates only, never overwrites", "Up to date", "Read when CashPilot starts", "Nothing saved", "{n} saved", …).
- Learn-more titles: about 12 keys. Their bodies reuse today's long strings split into short facts (for example `settings.earner_secrets.desc_html` becomes four `settings.earner_secrets.fact_*` keys).
- Earner table: column heads (5), mode labels (`file`, `env`, `unavailable`, unknown), "Not reported", the next-step lines (4 to 5), "Show steps", "Go to updates", "Turn on file mode", step titles (3), undo line, and its own loading and error keys (fixes brief §11.3). This replaces `app.earner_secrets.row` and `row_mode`.
- Import inside Settings: stepper labels (3), "Or paste one file instead", "Saved imports", the guide link labels. The existing `import.*` keys stay.
- Inline confirm: title and body for each confirm that moves out of `confirm()` (4 pairs). Optional.
- Old keys that go: `settings.index.*`, the long `*.desc*` intros once split, `app.env.note_html` (folded into the disclosure).

All labels are real text. The tab counts are numbers with an `aria-label` from the plural key.

## Accessibility notes

- The tab strip is `role="tablist"` with `role="tab"` buttons, `aria-selected`, `aria-controls` and a roving `tabindex`. Left and right arrows move between tabs. Focus uses the theme's cyan `:focus-visible` outline.
- Disclosures are native `<details>`, so the keyboard and screen readers work with no script.
- State is never colour alone: each coloured square comes with words.
- Muted text is `--text-muted` `#a59cb5`, 7.15:1 on the card background. Warning text is 8.57:1, success 7.14:1.
- At 390 px the tab strip scrolls sideways with a fade on the right edge. Box rows stack: name and state, then the two counts, then what to do.

## Seen in the renders, not part of this design

- At 900 px the app's own top bar lets "+ Add service" cover the "Settings" nav link. That is the current `base.html` top bar, the same on every page.
- The (g) frames embed the same page as `srcdoc`, so the full-page screenshot paints them. The script that does it is mockup scaffolding only.
