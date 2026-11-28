# Design 1: tidy in place

One long page in the same order as today. Every section becomes a card with the same four parts:

1. A title (mono, as the brand asks) and a status chip on the right that says the state in a few words.
2. One summary line under the title. It says what the section is for.
3. The controls, at once. No paragraph comes before them.
4. A "Learn more" disclosure at the bottom. The explanation goes there.

Import moves into the page as a card. The index gets four small group labels and a dot on each section that needs attention.

Files:

- `index.html`: the mockup. Panel (a) at the top is the whole page. Panels (b) to (j) under it show the states.
- `shot-1440.png`, `shot-900.png`, `shot-390.png`: full-page screenshots, rendered on the MacMini.

## What changed, and why

| Today | In this design | Why |
|---|---|---|
| Each section starts with a paragraph of 25 to 131 words. | One summary line (13 to 25 words). The rest goes under "Learn more". | The intros total about 735 words. The summaries total 163. Each fact is kept, either in the summary or behind the disclosure. |
| Sections look the same whether they are fine or need work. | A chip in the card header ("0 of 5 boxes use a file", "In the data folder", "Up to date"). The same dot shows in the index. | You can see what needs attention without reading. A chip always has words, so colour is never the only signal. |
| "Import from another tool" is the last index link, but it opens `/import`. | Import is a card on this page (`#set-import`), under Restore. The `/import` route redirects to `/settings#set-import`. | The index now holds only things that are on the page. Old links in the docs keep working. |
| The index is one flat list of nine links, and none is marked as the current one. | Four groups: Earnings, Devices and backups, Security, System. The current section has a pink left border (`aria-current`). The Notifications slot has a dashed border. | Ten sections are easier to scan in groups. The section order stays the same. |
| Earner credentials is 228 words of prose and a YAML block, with no control. | A table with one row per box. "How to turn on file mode" is a disclosure with three numbered steps, copy buttons and the undo line. | See the next section. |
| One "Save credentials" button sends the fields of all 20 collectors, open or closed (brief, fact 13). | Each open collector has its own "Save {service}" button, next to "Clear credentials". | You can see what you save. It uses the same route (`POST /api/config`). |
| 20 collectors in one list. | Filter tabs: All 20, Collecting 11, Not set up 9. "Collect now" and the last run time are on the same toolbar. | It is faster to find the ones you use. |
| "Update" in Credential health opens nothing on this page (fact 1). | "Update" opens the matching collector on this page (`#collector-<slug>`). | The button now does something. The deep link already exists. |
| Credential health, Device ids and Environment are stacks of text rows. | Each one is a table with real column heads. On a phone each row becomes a block with its labels. | Values line up and are easy to compare. |
| Environment shows locked values as disabled inputs, and the description twice. | A locked value is plain mono text with a lock and its source. Only the fields you can edit are inputs. The description shows once, under the name. | You can see at once what you can edit and what you cannot. |
| The encryption key steps are a numbered list with loose code blocks. | The same four steps, in the step style used everywhere on the page, with a copy button on each code block. | The look is the same as the Earner credentials how-to. |
| Each warning is a sentence inside a paragraph. | One warning line (a callout) above the controls it is about. | You see it before you act. |
| The page-wide load error is written twice, once into Environment and once into Collection. | It shows once, as a red callout at the top of the page (panel j). | One message for one problem. |

## Each problem from the brief, solved

- **Import looks like a section but is a separate page.** It is now a section on this page. It has the same three steps as today: add your old config, see what CashPilot found, deploy what you imported. Step 2 shows only after a check. The file list for each tool and the guide links are in a "Which files to add" disclosure next to the file picker. This also fixes fact 7: today the guides are named but not linked.
- **Walls of text.** No section opens with more than one summary line. The longest one is Restore, at 25 words, because the never-overwrites rule must stay on the main view.
- **Earner credentials is the worst.** Now it is a table you can read at a glance:
  - **Box**: the box name.
  - **Passwords go in**: a chip that shows the mode. "A file" (green), "Container settings" (amber), "Cannot use a file" (grey) or "Worker too old to say" (grey).
  - **In a file** and **In container settings**: the two counts. A count that needs a redeploy is amber and bold. A count the box does not report shows as a dash.
  - **Next step**: one short phrase for that row. For example: "Turn on file mode, then redeploy 8" (this opens the how-to), "Update the worker first" (this goes to About and updates), "Redeploy 3 earners" (this goes to the dashboard), or "Nothing to do".
  - The header chip counts how many boxes use a file.
  - The YAML block, the recreate command, the redeploy step and the undo line are all in "How to turn on file mode". It is closed by default.
  - What the setting protects against, what it does not protect against (root), the list of covered services and the guide link are in "Learn more". The term "container settings" is explained there the first time it is used.
- **Status buried in prose.** Each card header has a chip. The index shows a dot for each card that needs attention. Mode, counts and the next step for each box are table cells.
- **Inconsistent structure, explanations before controls, actions hard to see.** Every card has the same structure. The main action for each card sits in a fixed place: in the header for list sections (Add an id, Download all), on the toolbar for Collection (Collect now), or under the content (Save anyway, Re-pull images, Restore). Pink is used only for the one action the card recommends.

## Checklist against BRIEF.md section 14

| # | Item | Where it is now |
|---|---|---|
| 1 | A way to every section, including Credential health and the Notifications slot | Index, in four groups. The Credential health link stays hidden when it has no rows. Notifications has a dashed link. |
| 2 | Page-wide load error | One red callout at the top of the body (panel j). It uses the same `app.settings.load_failed*` text. |
| 3 | Deep links | `#collector-<slug>` and `?highlight=` still open that collector. `#set-restore` is unchanged. `/import` redirects to `#set-import`. |
| 4 | Collector name, badge, hint, fields, optional marker, keep placeholder | Unchanged inside each collector (the Bytelixir collector is open in panel a). The badges now have a square, like the chips. |
| 5 | Save credentials | "Save {service}" inside each open collector. |
| 6 | Collect now, running and triggered status | Collection toolbar, with the last run time next to it. The status text goes in the same place. |
| 7 | Clear credentials and its confirm | Inside each configured collector, next to Save. Same confirm. |
| 8 | "No collectors available." | Same empty line, in the list area. |
| 9 | Credential health row data | Table: login (service and field), Age, Expected to last (or expiry date), Status chip (4 tones). The reason and the durable-alternative hint are a sub-line (panels a and h). |
| 10 | Update on a failing row | Last column. It now opens the collector on this page. |
| 11 | Hidden with no rows | Same as today: the card and its index link stay hidden. |
| 12 | Device id row data | Table: service and field, masked id, box and copy, state. First and last seen, node, backup and unconfirmed hints are a sub-line. "Unreadable: the encryption key changed" goes in the actions cell. |
| 13 | Show, Copy, Change (with earlier ids and Use), Forget | Row buttons. The Change form opens as a row under its row (panel i), with "Use one this service had before", the offers and "What Change does". Both Forget confirms are unchanged. |
| 14 | Add an id form | "Add an id" in the card header opens the form under the table (panel i). All five fields, Save, Cancel and the "Add a box and a service first" line are kept. |
| 15 | Download all, with the password prompt | Card header. Same step-up prompt. |
| 16 | Empty, load error, reload error | Same texts, in the table area. Reload errors are toasts, as today. |
| 17 | What Restore covers, the create-only rule, how to replace, command-line link | The summary has the services and the create-only rule. "Learn more" has the passphrase rule, the replace steps and the command-line link. |
| 18 | File picker, Check file, checking, error | Main view. The checking text and errors show under the picker. |
| 19 | Preview contents | Panels f1 and f2: container and volumes, the never-overwrites rule, known-file history or unknown file with the typed name, the runs-elsewhere and live warnings as callouts, the box select with disabled reasons and plain-HTTP marks, the passphrase, the plain-HTTP checkbox and Restore. |
| 20 | Done messages, not-checked error | Panel f2 shows the done line. The not-checked error uses the same place. |
| 21 | Why the key matters | Summary line and "Learn more". |
| 22 | Every status line | The callout above the button. Several lines become stacked callouts (panel e2). The header chip names the state. |
| 23 | Move the key: Show, Copy, Hide, file, compose and restart steps, guide link, come-back step | "Move the key out of the data folder" opens the four steps (panel e1). Each code block has a copy button. |
| 24 | Delete the copy (confirm and password) | Panel e2: the button, the confirm text and the password prompt. Panel e3: done. |
| 25 | Loading and load error | Same texts, in the callout area. |
| 26 | What file mode protects against and what it does not; guide | Earner credentials "Learn more". |
| 27 | Per box: name, mode, both counts or "does not report" | The table (panels a, b, c1, c2). |
| 28 | The variable line, recreate, redeploy, undo | "How to turn on file mode" (panel b). |
| 29 | Loading, error, "No workers yet." | Same places. They now use their own keys, not the key section's (fixes fact 3). Panel c2 caption. |
| 30 | Per variable: label, name, lock, badge, value or secret state, description | Environment table: Setting (label, `NAME`, description), Value (input, or locked text, or dots for a secret), Source (lock icon and badge). |
| 31 | A value saved here does not take effect | Summary line, and a short line next to Save anyway. The rest is in "Learn more". |
| 32 | Save anyway and its messages | Bottom right of the card. Same title and same toasts. |
| 33 | Empty state | Same line, in the table area. |
| 34 | Server select, versions, images | Server select on the toolbar, then a four-cell grid: Running, Latest release, Worker image, Dashboard image. |
| 35 | Update button (3 labels), notes, worker-only note, UPGRADING link, already-running and not-Compose states | Under the grid. The note for each state goes next to the button. The UPGRADING.md link is in the note when a newer series exists, and in "Learn more". |
| 36 | Proxy policy warning with two commands | An amber callout above the grid, with the two commands in a code box with a copy button. Not drawn: it is the same pattern as the other callouts and code boxes. |
| 37 | Confirm, starting, started, failed; no worker; read error | Same messages and places. |
| 38 | What Import does and does not do | Summary line, and "Learn more" (nothing is run or fetched, the files are not kept). |
| 39 | Files per tool, the limits, the guides | The limits are in the Files label. The files for each tool and the guide links are in "Which files to add". |
| 40 | Tool select, files, paste, Check, the three errors | Step 1. "Or paste one file" is a disclosure. The errors go in the status place next to the button. |
| 41 | Preview rows, fields, extras, Not imported, no-service state | Panel d1. Same data, as a table. "Not imported" is a disclosure that shows its count. |
| 42 | Save the ticked services and its messages | Panel d1. A ticked count shows next to the button. |
| 43 | Drafts: Deploy to, each draft, Deploy, Forget, Deploy all, empty, the stop-the-old-tool warning | Panel d2. The warning is now an amber callout above "Deploy to", not a sentence in an intro. |
| 44 | Notifications slot | A dashed card under Credential health, labelled "Notifications (designed in the other PR)", with a dashed link in the index. |

## Implementation cost

| Part | Work | Rough size |
|---|---|---|
| `settings.html` | Card markup for 9 sections, index groups, the Import card (moved from `import.html`), the Notifications slot. | About 165 lines become about 300. |
| `import.html` | Deleted. | -62 |
| `app/routers/pages.py` | `GET /import` returns a redirect to `/settings#set-import`. | About 5 lines. |
| `import.js` | Loaded on the Settings page. The ids stay the same, so most of it does not change. The drafts list moves into the card. | About 20 lines change. |
| `app.js` | Earner credentials table and next step for each row (`earnerSecretsHtml`). Credential health, Device ids and Environment as tables. About grid. Save for each collector and the filter tabs. Header chips and index dots, from data already loaded. `aria-current` with an IntersectionObserver. Copy buttons on code blocks. One page-wide error banner. Update calls `openCollectorSection` in place of `openCredentialModal`. | About +260 / -150. |
| `style.css` | Cards, chips, callouts, disclosures, numbered steps, code boxes, card tables and their phone layout, index groups. Everything uses the existing tokens. | About +170. |
| Backend | Only the `/import` redirect. `/api/settings/earner-secrets` already returns everything the table needs. | Small. |
| Tests | Update the tests listed in BRIEF section 10, mainly `test_frontend_wiring.py`, `test_credential_storage_js.py`, `test_importers.py` and `test_tracking_without_deploying.py` (Save button text and behaviour). | Medium. |
| Docs | The section titles stay the same, so "Settings > Earner credentials" and similar names still match. The links to `/import` keep working through the redirect. We can point them at `/settings#set-import` later. | Optional. |

## What it needs from i18n

New keys, all in `en.json`, then translated by the i18n lane (about 75 keys):

- Index: 4 group labels and "needs attention" (screen-reader text for the dot).
- Shared: "Learn more", "about {section}" (screen-reader text), "Copy", "Copied".
- Each section: one `summary` key and 2 to 4 short "Learn more" paragraphs. These come from today's intros, split into short sentences.
- Chips: for example "{n} of {total} collecting", "{n} expiring soon", "{n} likely expired", "In the data folder", "Copy still in the data folder", "Outside the data folder", "{n} of {total} boxes use a file", "All {total} boxes use a file", "Up to date".
- Collection: 3 filter labels, "Last collection {time}", "Save {name}".
- Table column heads for Credential health, Device ids, Earner credentials and Environment.
- Earner credentials: 4 mode labels, 6 next-step phrases (with ICU plurals for the counts), the how-to title, 3 steps (title and body), the undo line, the "too old" line, and its own loading and error keys.
- Import: "Add your old config", "Saved imports", "Or paste one file", "Which files to add", one line for each tool, and the Files limit hint. The existing `import.*` keys are reused.
- Environment: "A value saved here is stored but not used."

Retired keys: `settings.earner_secrets.desc_html`, `settings.earner_secrets.how`, `app.earner_secrets.row`, `app.earner_secrets.row_mode`, the long `settings.*.desc*` intros (each one is replaced by its summary and its "Learn more" keys), `settings.index.import` as a link label (it stays as the card title), `import.title` and `import.lede`.

Not changed: the Environment labels and descriptions, and the collector field labels. They still come in English from the server (fact 5). The new layout does not make this better or worse.

## Notes and open points

- The lane task asks for "API key revealed and regenerated confirmation". The brief says this section is the credential encryption key. CashPilot has no regenerate action, so none is drawn. Panel (e) shows the key revealed and the one confirm the section has: "Delete the copy in the data folder".
- Panel c2 shows the phones as "A file" with no counts. A phone's real mode comes from its worker. Its row reads correctly in any mode, because the counts are dashes.
- The worker `status` (fact 4) is still not shown. All five boxes are online in the owner's data. An "offline" tag in the Box cell would cost one line if we want it.
- At 900 px the app's own top bar overlaps "Settings" and "+ Add service". The real `base.html` and `style.css` do this too, so it is not part of this design.
