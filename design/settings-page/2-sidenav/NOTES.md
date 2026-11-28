# Design 2: sticky side navigation

Open `index.html`. The top of the file is the whole Settings page at full width (state a). The state panels (b) to (h) sit under the footer. The screenshots are `shot-1440.png`, `shot-900.png` and `shot-390.png`, rendered on the MacMini.

## The idea in one paragraph

A sticky menu on the left groups the sections into five groups: General, Data and import, Security, Notifications and About. Each menu item shows its own status under its name, for example "0 of 5 protected". Every section on the right has the same five parts, in the same order: a small group label, the title, one status line, one or two short sentences, and a "Learn more" link that opens the long text. The controls come right after that. A "3 things need you" box at the top lists what needs attention and links to it. On a phone the menu turns into one "Go to" select that stays under the top bar. Import is now a section of the page, under Data and import, next to Device ids and Restore.

## What changed against today, and why

| Today | Design 2 | Why |
|---|---|---|
| Nine plain links on the left. One of them, "Import from another tool", leaves the page. No current-section mark. | Five groups with a mono label. Each item has a status mark (a square plus words). The current section gets a pink left bar. Import is an anchor like the rest. | You see the state of the page before you scroll. Every link stays on the page. |
| Each section opens with a paragraph of 50 to 90 words. | One status line and one or two sentences of at most 25 words. The rest is behind "Learn more". | The first view tells you the state and the next step. The details are one click away. |
| Earner credentials: 76 words of intro, one long sentence per box, a raw YAML block, 32 more words, and no control. | A status line ("0 of 5 boxes protected · 23 earners keep their passwords in Docker settings"), a table with one row per box (mode, count in a file, count in Docker settings, what to do), and the steps behind "How to turn on file mode on a box", each with a Copy button. | The status is a glance. Each box says what to do next. The steps are numbered and the code is copyable. |
| Section titles are plain text, all in the same weight. | Titles in IBM Plex Mono, with a small group label above them. | The section starts are easy to find when you scroll, and the page matches the app's mono figures. |
| Buttons sit at the end of each section, after the text. | The main action of a section sits on the right of its title (Collect now, Add an id, Move the key out, Re-pull images). | You find the action without reading the text first. |
| Import is a separate page with three numbered card titles. | One section with a three-step track: Add the files, Check what comes over, Deploy. | Import belongs to the same job as backup and restore. The track shows where you are. |
| One "Save credentials" button saves the fields of all 20 collectors (brief, fact 13). | Each open collector has its own "Save <service>" button next to "Clear credentials". | You save what you see. A field typed in a closed collector no longer goes out with an unrelated save. |
| The 20 collectors show as one long list. | "Set up (11)" shows first. "Not set up (9)" is closed and lists the names in its summary line. | The services you use come first. The others stay one click away. |
| Credential health "Update" opens nothing on Settings (brief, fact 11). | "Update" opens that service in Earnings collection, with its fields ready. | The button does what it says, on the same page. |
| Environment shows six inputs that look editable, and a note that says a save does nothing. | A read-only table (setting, value, source). The two editable rows sit behind "Store a value that does not take effect", with Save anyway. | The page no longer offers an edit that has no effect. The action still exists. |
| Earner credentials borrows the key section's loading and error text (brief, fact 3). | Its own text: "Could not load the box report: {error}". | The error names the right thing. |

## How each listed problem is solved

1. **Import looks like a section but opens another page.** It is now a section (`#set-import`) under Data and import. `/import` keeps working: the route answers with a redirect to `/settings#set-import` (one line in `app/routers/pages.py`), so the 3 English and 76 translated doc links still land on it.
2. **Walls of text.** Each section has one status line and at most two short sentences. Long text goes behind "Learn more" or a named disclosure ("Which files to add", "To replace a running identity, or for other files"). Before any row data, the first view has about 590 words. Today it has about 1,050 with Import added (brief, section 13). The 590 includes Import, the status lines, the attention box and the disclosure summaries. Earner credentials has 149 words with its five rows, against 228 today. It also has a table and a button now, where today it has no control at all.
3. **Earner credentials is the worst.** See the table above, and panels (b) and (c). Every fact in the old prose is still there. Mode is a word plus a coloured square. The counts are numbers in their own columns. "Too old to say" is "Not known" with "Worker too old to say" under it. A worker that does not report its earners one by one shows "not reported", with the meaning written once under the table. The YAML block, the recreate command and the undo step are in the numbered steps.
4. **Status buried in prose.** Every section has a status line, and the menu repeats it, for example: 11 of 20 set up, 1 expiring soon, 5 ids and 3 in use, In the data folder, 0 of 5 protected, v3.1.0 and up to date, 6 variables.
5. **Inconsistent structure, explanation before controls, actions hard to find.** The same five-part frame is used in every section. The primary action is on the right of the title. Disclosures always use the same underlined summary with a chevron.

## Things this design adds (all optional, no new data)

- **"3 things need you" box.** It is built from data the page already loads: the earner-secrets report, the key status and credential health. It shows only when something needs action. With nothing to show, it is hidden.
- **Status marks in the menu.** These use the same data as the section status lines.
- **Ticks on the earner-credentials steps** (panel b). Steps 1 and 2 tick when a box reports `mode: file`. Step 3 ticks when `in_config` is 0. The data is the same as the table's.
- **"Redeploy 3 earners" link** (panel b). It opens the dashboard. The dashboard has no per-box filter today (`app.js` reads only `?service=` and `?highlight=`), so a `?worker=` filter would be a small follow-up. It is not needed for this design.
- **Inline confirm** for "Delete the copy in the data folder" (panel e). It shows the full warning text next to the button. Today's native `confirm()` can stay if we want a smaller change.

## Checklist against BRIEF.md section 14

Where each item lives in design 2. "Page" means the main view at the top of `index.html`.

**Page**
1. Every section is in the menu and in the phone "Go to" select. Credential health hides with its link when it has no rows, as today (panel h). The Notifications slot is in the menu under Notifications, and on the page.
2. The page-wide load error: panel (h), "Whole page: config failed". Same text and keys.
3. `#collector-<slug>` and `?highlight=<slug>` work as today, because the collectors keep their ids (`collector-bytelixir` is shown). `#set-restore` keeps its id. `/import` redirects to `#set-import`.

**Earnings collection**
4. Page. Name, badge, hint, every field, "(optional)", "set — leave blank to keep" (Bytelixir is shown open). The Incomplete badge uses the same `badge-warning` as today.
5. "Save <service>" in each open collector. It uses the same `POST /api/config` route.
6. "Collect now" on the right of the title, with `#collector-save-status` beside it for "Running collection..." and "Collection triggered".
7. "Clear credentials" in each set-up collector. It keeps the same confirm.
8. Panel (h), "No collectors available."

**Credential health**
9. Page table: service, field, age, expected lifetime or expiry, status with its mark (the four tones), reason as a sub-line. The durable-alternative hint shows as a sub-line in the same place.
10. "Update" on the failing row. It now opens the collector on this page.
11. Hidden when it has no rows: panel (h).

**Device ids**
12. Page table: service, field, masked value, box, copy, state, first and last seen, node and backup hints as sub-lines. The unconfirmed and unreadable hints use the same sub-line slot.
13. Show, Copy, Change and Forget per row. They keep their confirms. Change opens today's change form under the row, with "Use one this service had before" and Use (not drawn, unchanged).
14. "Add an id" on the right of the title. It opens today's add form (not drawn, unchanged).
15. "Download all" on the right of the title. Its tooltip says it asks for your password.
16. Empty: panel (h). The load error and reload error are unchanged (same keys).

**Restore**
17. Page: the status line names the services. The lede has the create-only rule. "To replace a running identity, or for other files" holds the three steps and the command-line link.
18. Page: file picker and Check file. Panel (f): "Checking the file..." and the not-checked error.
19. Panel (f): container and volumes, the never-overwrites rule, the known-file history (behind a disclosure), the unknown file with the typed name, live elsewhere, the box select with disabled reasons, the passphrase, the plain-HTTP checkbox, and Restore.
20. Panel (f): the "Done" toast and the LAN-fence variant. The not-checked error.

**Credential encryption key**
21. Page: the lede and the status line.
22. Page: "In the data folder" and its path. Panel (e): "Outside the data folder · a copy is still inside" and "no copy left inside". The env-same and different-copy lines use the same facts block.
23. Panel (e): the four steps, Show, Copy, Hide, the code blocks with Copy, "Use a secret manager instead" with the guide link, and "Come back to this page".
24. Panel (e): "Delete the copy in the data folder", its confirm and the password note.
25. Panel (h): loading. The load error is unchanged.

**Earner credentials**
26. Page, "Learn more": what Docker settings expose, that root can still read the file, which earners it covers, and the guide link.
27. Page and panels (b) and (c): name, mode (File, Docker settings, Not known; "Not possible on this image" for `unavailable`), count in a file, count in Docker settings, or "not reported".
28. Page: "How to turn on file mode on a box" (open in panel b): the variable line, the recreate command, redeploy, and "To undo".
29. Panel (h): loading, error (its own text now) and "No workers yet."

**Environment**
30. Page table: label, variable name, lock, badge (From env, Read-only, Default; Stored not applied and Not set use the same badge slot), value or dots, description.
31. Page: the lede says a change here does not take effect, and where to set it. "Learn more" explains why some values can never change while CashPilot runs.
32. Page: "Store a value that does not take effect", then Save anyway. Same messages.
33. Panel (h): "No environment variable info available."

**About and updates**
34. Page: Server select, Running, Worker image, Dashboard image, Latest release.
35. Page: the update button on the right of the title. The label changes with the state, as today. The note sits under the facts. UPGRADING.md is under "Learn more". The already-running and not-Compose notes take the same place as the note.
36. The proxy policy warning: not drawn, unchanged. It goes under the facts as a `sn-callout warn` with its two commands in a `sn-code` block.
37. Confirm, starting, started and failed are unchanged. No worker online: panel (h).

**Import**
38. Page: the lede ("runs nothing from the files and does not keep them").
39. Page: "Which files to add" lists the files per tool, with a guide link for each (this fixes brief fact 7), and the limits. The limits also show next to the file picker.
40. Page: Tool select, file picker, "Or paste one file", Check what comes over. The three input errors use `#import-status` beside the button, as today.
41. Panel (d), first block: "Read as", the notices, the rows with tick, state, field states and the fill-in input, the reasons, the extras, "Not imported (2)", and the "no service" text in panel (h).
42. Panel (d): "Save the 3 ticked services". The check-first, tick and saved messages are unchanged.
43. Panel (d), second block: Deploy to, the drafts with source, time and keys, Deploy, Forget, Deploy all, the stop-the-old-tool warning as a callout, and "Nothing imported yet" in panel (h).

**Notifications**
44. Page and menu: a dashed slot labelled "Notifications (designed in the other PR)". Its contents are not designed.

## Implementation cost

| Part | Work | Rough size |
|---|---|---|
| `settings.html` | New layout: the menu with five groups, the phone select, and the five-part frame in each section. Move the `import.html` body into a `#set-import` section. Collector, id and health containers keep their ids. | about 250 lines changed, plus about 60 moved from `import.html` |
| `import.html`, `pages.py` | The `/import` route answers `RedirectResponse("/settings#set-import")`. Delete `import.html`, or keep it as a stub. | 5 lines |
| `import.js` | Load it on the Settings page. Its ids stay the same, so it keeps working. Add the step-track state (one class per step). | about 15 lines |
| `app.js` | Status-line and menu-status writers, about 8 small functions fed by the data already loaded. Earner secrets: render a table instead of `<p>` rows, plus the step ticks. Credential health and device ids: render table rows instead of divs. Per-collector Save (scope `saveCollectorCredentials` to one `details`). Credential health "Update": scroll to and open `#collector-<slug>`. Environment: read-only table, with the inputs in the disclosure. Attention box. A scroll-spy (IntersectionObserver) to set `aria-current` in the menu. | about 300 lines changed |
| `style.css` | The `sn-*` rules from the mockup's `<style>`: menu, section frame, status mark, disclosure, tables that stack (container queries), code-with-copy, steps, callout, track. All use the existing tokens. Remove `.settings-index` rules. | about 180 lines |
| Backend | Only the `/import` redirect. Every number comes from routes the page calls today. | 5 lines |
| Tests | Update the 12 test files listed in BRIEF section 10, mostly id and class lookups and the import page tests. | moderate |
| Docs | "Settings > Earner credentials" and the other section names stay the same. The migrate guides can keep `/import`, because it redirects. | none needed |

## What it needs from i18n

New keys in `en.json` (then the 19 locales):

- Menu groups: `settings.group.general`, `.data`, `.security`, `.notifications`, `.about`. Phone select label `settings.jump` ("Go to").
- Status lines, one ICU message per section, for example `settings.status.collection` "{n} of {total} services are collected", `settings.status.earner_secrets` "{protected} of {boxes} boxes protected", `settings.status.earner_secrets_in_config` "{n, plural, ...} keep their passwords in Docker settings", `settings.status.key.data`, `settings.status.key.outside`, `settings.status.ids`, `settings.status.health`, `settings.status.import`, `settings.status.about`, `settings.status.env`. Each also has a short menu form.
- New ledes: the short sentences in each section, one key each (`settings.<section>.lede`). The long text moves into `settings.<section>.more_html`. Most of it can reuse today's `desc_html` text, split into list items.
- Earner credentials table: column heads, mode words (`file`, `env` "Docker settings", `unavailable` "Not possible on this image", `null` "Not known" plus "Worker too old to say"), "not reported", the three step titles, "To undo", the next-step words ("Turn on file mode", "Redeploy {n} earners", "Update the worker first", "Update the worker app"), and its own loading and error keys (brief fact 3).
- Attention box title `settings.attention` "{n, plural, ...} need you" and one line per kind.
- Shared: "Learn more", "Copy", "Save {service}", "Store a value that does not take effect", "Not set up ({n})", "Set up ({n})", the three import step names.
- Removed or replaced: `app.earner_secrets.row`, `app.earner_secrets.row_mode`, `settings.earner_secrets.desc_html`, `settings.earner_secrets.how`, `settings.index.import` (the name moves to the section title).

The environment labels and descriptions stay in English from the server, as today (brief fact 5). Moving them into `en.json` is a separate change.

## Notes from rendering

- The lane's rsync command puts `app/static` at `wt/static` on the MacMini, but the mockup links `../../../app/static/css/style.css`. I also copied it to `wt/app/static`, so the shots use the real stylesheet.
- A full-page shot does not paint a `file://` iframe, because the browser treats each file URL as cross-origin. The two phone frames in panel (g) are a `srcdoc` copy of the same page, made by a few lines of inline script.
- At 900 px the app's own top bar runs "Settings" into "+ Add service". The real app does the same at that width; this design does not cause it.
- The key shown in panel (e) is made up. It is not a real key.
