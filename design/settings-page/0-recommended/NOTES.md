# Design 0: the recommended Settings page

This design builds on design 1 (tidy in place). It adds the ideas that the three judges agreed on, and it fixes every defect they listed.

Files:

- `index.html`: the mockup. Panel (a) at the top is the whole page as it loads. Panels (b) to (k) under it show the other states.
- `shot-1440.png`, `shot-900.png`, `shot-390.png`: full-page screenshots, rendered on the MacMini and checked at each width.

## The page in one look

1. **Needs your attention** comes first. It uses the dashboard's attention rows (`.attention`, `.attn-row`). Each row has a tag (Fix, Soon, Old), a short title, one sentence, and a button that lands on the control. A green "In order" line follows. When nothing is wrong, the block shrinks to "Nothing needs your attention" (panel d).
2. **The index** has five groups and a status line under each item ("11 of 20 collecting", "1 expiring soon", "0 of 23 protected"). On a wide screen it is sticky. Under 1100 px it folds into one sticky **Sections** bar. The bar shows the current section and "4 to fix". "Sections" opens the same list of links (panel k).
3. **Every section is one card** with the same parts: a mono title, a status chip with words, one summary line, the controls, then disclosures. Each "Learn more" is titled by the question it answers ("Learn more: how to replace a running identity").
4. **Import is a card on this page** (`#set-import`). Step 1 is open on the main view. Steps 2 and 3 are always visible and keep their numbers.
5. **Earner credentials** opens with two defined terms ("File mode", "Container settings"), then a meter ("0 of 23 earners protected"), then one row per box with its kind, its mode, both counts as numbers and what to do. "Show steps" opens the steps for that box under its row. The steps tick themselves from what the box reports. The 4-line compose YAML sits behind "Show it in a compose file", with a Copy button, both in the per-box steps and in "How to turn on file mode".

The section summaries hold 179 words in total. None is longer than 25 words. Today the intros hold about 735 words, including Import. All other text is behind a named disclosure.

## Base

Design 1 (tidy in place) is the base. It had the top total (22). Judge 3 chose it as the cheapest safe path to build. It keeps every section id, every section title and the real components (`settings-layout`, `settings-index`, `collectors-grid`, `collector-section`, the `badge-*` classes). So the doc section names (brief section 9) and most of the 12 markup-bound tests stay as they are. It is also the only design that drew the Device ids Change and Add forms.

## Grafts

| Idea | From | Judges who asked for it |
|---|---|---|
| A "Needs your attention" block at the top. It uses the dashboard's `.attn-row` with Fix, Soon and Old tags and a real action button on each row. It has an "In order" line and an all-clear state. It is built only from responses the page already loads, with no Dismiss state. | 4 (strip, all-clear), 3 (tags, action buttons), 2 (box) | 1, 2, 3 |
| A status line under each index item. Under 1100 px, a sticky bar opens the same index. | 2 | 1, 2 |
| An earner meter with a three-part legend above the table | 4 | 1, 3 |
| The box kind under each name ("Docker server", "Android phone"). Phones say "Update the app on the phone". A per-row button ("Show steps", "Go to updates"). The lede defines "file mode" and "container settings". Two named disclosures ("How to turn on file mode, and how to undo it", "What file mode protects against, and what it does not"). | 3 | 1, 2 |
| Steps scoped to one box ("Protect the earners on watchtower") with the one-line variable first, the compose snippet behind "Show it in a compose file", and a dashboard button | 4 | 1, 2, 3 |
| Step ticks, now per box: steps 1 and 2 tick when that box reports mode `file`, step 3 when its `in_config` is 0 | 2 (ticks), fixed per box as judge 2 asked | 1, 2 |
| Import step 1 open on the main view, "Or paste one file instead" as a disclosure, steps 2 and 3 always visible | 1, 3 | 1 |
| The three-step strip for Import, the count in the button ("Save the 3 ticked services") and a reason line | 4 (strip), 3 (count, reason) | 1, 2 |
| Environment as a read-only table. The inputs and "Save anyway" sit behind "Store a value that does not take effect". | 2 | 1, 3 |
| "Set up (11)" first, then one "Not set up (9): names" disclosure, in place of filter tabs | 2 | 3 (judge 1 liked tabs; the fold gives the same result with less JS state) |
| "Last collection 12 min ago" next to Collect now | 1 | 1, 2 |
| An inline confirm that names the exact thing ("Delete /data/.fernet_key?") for Delete the copy, Forget an id, Clear credentials and Forget an import | 3 | 1, 2 |
| An "Expires soon" chip on the collector header when Credential health flags it | 3 | 3 |
| Notifications in its own index group, with a dashed card | 2, 4 | 1, 3 |
| A card edge on every section | 1 | 2 |

## Defects the judges found, and what this design does

**Design 1's own defects**

| Defect | Fix |
|---|---|
| No summary of what needs attention | The attention block at the top, plus a status line on every index item |
| The Notifications slot sat in the Earnings group | Notifications has its own index group and its own dashed card |
| At 390 px the index was 11 wrapped chips that did not stick | One sticky Sections bar under 1100 px |
| "Container settings" had no definition on the main view | The earner summary defines "file mode" and "container settings" |
| Phone rows said "Update the app. It does not report earners one by one." (two ideas, jargon) | "Update the app on the phone", and the counts say "not reported" |
| The Bytelixir hint (about 60 words) showed on the main view | Each collector hint sits behind "Where to find these values". It is open for a collector that is not set up and closed for a configured one. It needs no new data. |
| The page was long because every card was open | Long text is behind disclosures. The nine collectors that are not set up fold into one line. |
| States not drawn: proxy policy warning, Incomplete, collect running and triggered, unreadable and unconfirmed id hints, no collectors, files with no service, no workers online | All drawn: panels (j2), (h1), (h2), (i2), (h3), (e3), (e5) |
| Guide links were `href="#"` | Real URLs for the three import guides, the earner-secrets guide, the encryption-key guide, the restore command-line steps and UPGRADING.md (fixes brief fact 7) |
| Import step numbers changed with the state | The steps are always 1, 2, 3. Step 2 is grey until a check. |
| Panel c2 showed the phones as "A file" | The phones keep their real state, "Too old to say", in every panel |
| Chips set in mono looked like code | Chips use the UI font |
| Environment inputs on the main view looked like the way to change a setting | Read-only table. The inputs are behind their own disclosure. |
| Worker status (fact 4) not shown | The earner table shows the box kind. The plan adds an "offline" tag in the Box cell from `status`. It is not drawn, because every box is online in the owner's data. |

**Shared defects, and defects of the grafted parts**

| Defect | Fix |
|---|---|
| Multi-line code collapsed onto one line, and Copy covered the text (design 2) | `.codebox` is a flex row: the `pre` keeps `white-space: pre` and scrolls, and the Copy button sits beside it. On a phone, Copy moves above the code. Panel (b1) shows the four-line YAML. |
| Code cut off behind the Copy button (design 4) | Same fix. Long lines scroll inside the box. |
| Box counts that disagree ("0 of 5 protected" against "3 boxes") | The chip, the index and the meter all count earners: "0 of 23". The legend names the 2 phones that do not report. |
| A mixed message: "Up to date" next to "too old" (designs 3, 4) | The "In order" line says "watchtower runs v3.1.0, the newest release". It names the server the About card loaded. The Old row names geiserct and the phones. |
| Invented data: earner names to redeploy, a deployed state on drafts (design 3) | Not used. Drafts show name, source, time and keys only. The redeploy step gives a count and an "Open the dashboard" button. |
| Too many pink buttons (design 4) | At most one pink button per section, and only for its next step. On first view only "Save Bytelixir" and "Check what comes over" are pink. "Re-pull images" is secondary when up to date. |
| Device id actions hidden in collapsed rows (design 4) | Show, Copy, Change and Forget stay visible on each row. Forget shows only on rows the server marks as forgettable. |
| The reason behind an icon-only "?" (design 4) | The reason is a sub-line under the login |
| On a phone, "Check file" came before "Choose File" (design 4) | The file input comes first, then the button |
| A per-collector hint summary with no data source (design 4) | Not used. The real YAML hint sits behind a generic disclosure. |
| A sticky select for navigation (design 2; judge 3: weaker than links) | The Sections bar opens real links |
| The earner table cramped at 900 px (design 2) | Under 1000 px each box becomes one block: name and mode, then the counts, then what to do |
| "Next to: the database it decrypts" read badly (design 2) | Not used |
| The Repocket placeholder said "(optional)" on a required field (design 4) | The missing field has a plain placeholder and the word "missing" |
| Tabs hide content and rename sections (design 3) | One page. Section titles are unchanged. |

**A finding from building this:** `style.css` has no rule for `.badge-warning`. Today "Incomplete" and "Stored, not applied" look like plain grey text. The mockup adds a one-line rule. The implementation should add it to `style.css`.

## Checklist against BRIEF.md section 14

| # | Item | Where it is |
|---|---|---|
| 1 | A way to every section, Credential health when it has rows, the Notifications slot | The index (wide) and the Sections bar (narrow). The Credential health item hides with its card, as today. Notifications has its own group. |
| 2 | Page-wide load error | One red callout at the top of the settings body (panel h3) |
| 3 | `#collector-<slug>`, `?highlight=`, `#set-restore`, `/import` | Unchanged ids. `openCollectorSection` must first open the "Not set up" fold when the collector is in it. `/import` redirects to `/settings#set-import`. |
| 4 | Collector name, badge (Configured, Incomplete, Not configured), hint, fields, optional marker, keep placeholder | Panel (a), Bytelixir open. Incomplete in panel (h1). The hint is behind "Where to find these values". |
| 5 | Save credentials | "Save {service}" in each open collector |
| 6 | Collect now, running and triggered | Collection toolbar. "Running collection..." and "Collection triggered" in panel (h2). |
| 7 | Clear credentials and its confirm | Each configured collector. The confirm is inline (panel h1). |
| 8 | "No collectors available." | Panel (h3) |
| 9 | Service, field, age, lifetime, expiry, status in 4 tones, reason, durable hint | Credential health table. The reason and the durable hint are sub-lines (panels a, i1). |
| 10 | Update on a failing row | It now opens `#collector-<slug>` on this page (fixes brief fact 1) |
| 11 | Hidden with no rows | Unchanged |
| 12 | Id row: service, field, masked value, box, copy, state, seen times, node, backup and unconfirmed hints, unreadable | Device ids table (panel a). Unconfirmed and unreadable rows in panel (i2). |
| 13 | Show, Copy, Change (earlier ids, Use), Forget (both texts) | Row buttons. The Change form opens under its row, with the offers and "In use on" (panel i2). Forget is an inline confirm that keeps both texts. |
| 14 | Add an id form, "Add a box and a service first" | Panel (i2) |
| 15 | Download all, with the password | Card header. Same step-up prompt. |
| 16 | Empty, load error, reload error | Same texts and places (caption in panel i2) |
| 17 | What Restore covers, create-only, how to replace, command-line link | Summary line, and "Learn more: how to replace a running identity" |
| 18 | File picker, Check file, checking, error | Main view. "Checking the file..." in panel (g3). |
| 19 | Preview: container, volumes, never-overwrites, known or unknown file, live and elsewhere warnings, box select with reasons and plain-HTTP marks, passphrase, plain-HTTP box, Restore | Panels (g1), (g2), (g4), (g6) |
| 20 | Done messages, not-checked error | Panels (g2), (g5) |
| 21 | Why the key matters | Summary, and "Learn more: why the key's place matters" |
| 22 | Every status line | Callouts above the button (panels a, f2, f3 and the caption in f3) |
| 23 | Show, Copy, Hide, file, compose and restart steps, the guide, the come-back step | Panel (f1) |
| 24 | Delete the copy, with confirm and password | Panel (f2). The confirm is inline and names the file. The password prompt follows. |
| 25 | Loading, load error | Caption in panel (f3) |
| 26 | What file mode protects against and what it does not, the guide | "What file mode protects against, and what it does not" |
| 27 | Per box: name, mode (file, env, cannot, too old), both counts or "not reported" | The table (panels a, b2, c1). "Cannot use a file" in panel (b2). |
| 28 | The variable line, recreate, redeploy, undo | Per box in panels (b1) and (b2). For all boxes in "How to turn on file mode, and how to undo it". |
| 29 | Loading, error, "No workers yet." | Panels (c2), (c3), (c4). They get their own keys (fixes brief fact 3). |
| 30 | Per variable: label, name, lock, badge, value or secret state, description | Environment table. "Stored, not applied" in panel (j1). |
| 31 | A saved value does not take effect, where to set it | Summary line, the disclosure title, and the note next to Save anyway |
| 32 | Save anyway and its messages | Panel (j1) |
| 33 | Empty state | Caption in panel (j1) |
| 34 | Server select, running, images, latest or unknown | About card (panel a). "unknown" in the caption of panel (j3). |
| 35 | Three button labels, note, worker-only note, UPGRADING link, already running, not Compose | Panels (a), (j2), (j3) |
| 36 | Proxy policy warning with two commands and the link | Panel (j2) |
| 37 | Confirm, starting, started, failed, no worker, read error | Panel (j3) and its caption. Update keeps the native confirm. |
| 38 | What Import does and does not do | Summary, and "Learn more: what happens to your files" |
| 39 | Files per tool, the limits, the guides | The limits are in the Files label. "Which files to add, and the guide for each tool" has real links. |
| 40 | Tool select, files, paste, Check, the three errors | Step 1 on the main view. Errors in panel (e4). |
| 41 | Read as, notices, rows, fields, fill-ins, reason, extras, Not imported, no service | Panels (e1), (e3) |
| 42 | Save the ticked services, with its messages | Panel (e1). The button carries the count. "Check the files before saving." and "Tick at least one service." stay. |
| 43 | Deploy to (or "No workers online."), drafts, Deploy, Forget, Deploy all, "Nothing imported yet.", stop-the-old-tool | Panels (a), (e2), (e5). The warning is a callout above "Deploy to". |
| 44 | Notifications slot | A dashed card and its own index group, labelled "Notifications (designed in the other PR)" |

## Implementation plan

One PR, in this order. Each step names its files.

1. **Route.** `app/routers/pages.py:104-112`: `GET /import` returns `RedirectResponse("/settings#set-import", status_code=308)`. Browsers follow a fragment in `Location`, so the 4 English and 76 translated doc links land on the Import card. The route keeps its owner-only guard, the same as Settings. Delete `app/templates/import.html`. `import.js` starts with `DOMContentLoaded` → `loadDrafts` (import.js:242) and checks no `data-page`, so loading it on the Settings page needs no change there.
2. **One API field.** `app/routers/credential_storage.py:143-151`: add `"kind": info.get("device_type") or "docker"` to each worker entry. `info` is already parsed there. The table uses it for "Docker server", "Android phone" and "Desktop". Nothing else on the server changes. "Last collection" comes from `last_run_age_seconds` and `collected` in `GET /api/collector-alerts` (main.py:12074-12080), which the bell already polls.
3. **Template.** `app/templates/settings.html`: the attention block, the index with groups and status lines, the Sections bar, a card per section with the same ids and titles, the Import card (the ids of `import.html` move as they are), the Notifications slot. Load `import.js` on this page. About 165 lines become about 330.
4. **JS, section by section** (`app/static/js/app.js`, Settings code at 5500-6600 and 7220):
   - `earnerSecretsHtml`: meter, legend and table rows; "Show steps" draws the per-box steps under the row; ticks from `mode` and `in_config`. Own loading and error keys.
   - `renderCollectors`: split "Set up" and "Not set up"; put each hint in a disclosure (open when the collector is not configured); one Save per collector; an "Expires soon" chip from the credential-health rows. `openCollectorSection` opens the fold first.
   - `loadCredentialHealth`: table rows; Update calls `openCollectorSection` in place of `openCredentialModal`.
   - `identityRowsHtml`: table rows; the Change form goes in a row under its row.
   - `renderEnvVars`: read-only table; the inputs go into the "Store a value" disclosure.
   - `renderUpdateCard`: the four-cell grid.
   - New, small: `settingsAttention()` builds the attention rows, the "In order" line, the index status lines and the header chips from the responses already loaded (earner-secrets, encryption-key, credentials/health, update-info, collectors). One helper writes all three places, so the words always match. An IntersectionObserver sets `aria-current` on the index item and fills the Sections bar. One `inlineConfirm()` helper replaces `confirm()` for Clear credentials, Forget an id, Delete the key copy and Forget an import. Copy buttons on code boxes.
   - Size: about +330 / -170 lines.
5. **Import JS.** `app/static/js/import.js`: the same ids, so few changes. Move the step-strip state (1, 2, 3), the count in the Save button and the reason line. Forget uses `inlineConfirm()`. About 30 lines change.
6. **CSS.** `app/static/css/style.css`: a `--stuck-top` variable (the top bar's real height, set by a ResizeObserver, because the top bar wraps to two rows under 768 px), used by the Sections bar and by `scroll-margin-top` under 1100 px; the card frame, chips, callouts, disclosures, steps, code boxes, card tables and their phone layout, the earner meter and table, the index status lines, the Sections bar, the inline confirm, the step strip, and `.badge-warning`. Everything uses the existing tokens. About +200 lines.
7. **i18n.** `app/i18n/en.json`: see the next section.
8. **Tests.** Update the 12 files in brief section 10. The main ones: `test_frontend_wiring.py`, `test_credential_storage_js.py`, `test_importers.py` (import page gone, redirect), `test_tracking_without_deploying.py` (Save per collector). Add tests for the `/import` redirect, the `kind` field, and the attention builder with an all-clear case and a mixed case.
9. **Docs.** Section titles do not change, so the "Settings > …" names in the docs still match. The `/import` links keep working through the redirect. We can point them at `/settings#set-import` in a later docs PR.
10. **Desktop.** CashPilot-Desktop has its own frontend. This change touches no deploy route, no deploy form and no catalog file, so Desktop needs no follow-up. The PR body says so.

## i18n needs

New keys in `en.json` (about 85), then translated by the i18n lane:

- Attention: block title, the three tags, one title and one sentence per kind of row (earners in Docker, key in the data folder, login expiring, login likely expired, boxes too old), the action labels, "In order:", "Nothing needs your attention.", and the "In order" facts.
- Index: 5 group labels, one status line per section (ICU plurals), "Sections", "{n} to fix", "Nothing to fix".
- Shared: one "Learn more: …" title per section, "Copy", "Copied", the inline-confirm buttons.
- Collection: "Set up", "Not set up", "Where to find these values", "Save {name}", "Last collection {time} ago", "Not collected yet", "Expires soon".
- Earner credentials: the summary, the meter and legend (plurals), column heads, 4 mode labels, 3 box kinds, the action phrases, "Show steps" and "Hide steps", the steps title "Protect the earners on {box}", 3 step titles, "Done", "{n} left", "Open the dashboard", the undo line, the two disclosure titles and their text, loading and error.
- Import: the 3 step names, "Or paste one file instead", "Which files to add, and the guide for each tool", one line per tool, "Save the {n} ticked services", the reason line, "Deploy all {n} to {boxes} boxes".
- Environment: "Read only", "Store a value that does not take effect", its sentence, "Stores the value only. It does not take effect."
- Table column heads for Credential health, Device ids and Environment.

Retired keys: `settings.earner_secrets.desc_html`, `settings.earner_secrets.how`, `app.earner_secrets.row`, `app.earner_secrets.row_mode`, the long `settings.*.desc*` intros (each becomes a summary and "Learn more" keys), `import.title`, `import.lede`, and `settings.index.import` as a link label (it stays as the card title).

Not changed: the Environment labels and descriptions and the collector field labels still come in English from the server (brief fact 5). The "Fleet API Key" description still differs from the docs (fact 6). Both are out of scope for this lane.

## Open PRs that touch the same files

Checked on 2026-11-28 with `gh pr diff --name-only`.

| PR | Files it shares with this plan | Collision |
|---|---|---|
| #947 gVisor per earner | `app.js`, `style.css`, `en.json` | Different functions (Fleet page). Only appends in `style.css` and `en.json` can conflict. |
| #946 floating app images | `app.js`, `style.css`, `en.json` | Same as above |
| #940 proxies for Bitping, Mysterium, URnetwork | `app.js`, `en.json` | Same as above |
| #933 Secure VM from the Fleet page | `app.js`, `style.css`, `en.json` | Same as above |
| #895 gVisor docs and the layers page | `pages.py`, `base.html`, `app.js`, `style.css`, `en.json` | `pages.py`: it changes `_page`; this plan changes only the `/import` route. Separate hunks. |
| #949 web UI in 19 more languages | Locale files only | Every new key above needs those 19 locales, or it falls back to English. Merge order decides who adds them. |

None of these PRs touches `settings.html`, `import.html`, `import.js`, `credential_storage.py` or the Settings functions in `app.js`.

## Adversarial check (2026-11-28)

We went through BRIEF.md section 14 line by line against `index.html` and the screenshots, and ran a script on the MacMini at 1440, 900, 390 and 360 px. It measured page overflow, the words before each section's first control, the contrast of every text colour against its background, and where an anchor jump lands. Every muted text passes 4.5:1 (the lowest is `--text-muted` at 6.76:1). The gaps we found, all fixed in this folder:

| Gap | Fix |
|---|---|
| Under 768 px the top bar wraps to 74 px, but the Sections bar stuck at 48 px, so the top bar hid it. Under 1100 px an anchor jump (index link, attention button, `/import` redirect) landed the section title under the bars (title at 64 px, bars end at 89 or 114 px). | `--stuck-top` from the top bar's real height; the Sections bar sticks there; `scroll-margin-top` adds the Sections bar. Measured after: the title lands at 106 px (bars end 89) and 131 px (bars end 114). |
| At 390 px the Traffmonetizer header ran out of its box: "Configured" was cut off. | The badges wrap under the name. The name stays one word. |
| The Earner credentials summary was 33 words, in two long sentences. | Two defined terms, 25 words. |
| Credential encryption key: 15 words of summary plus a 19-word status line before the Move button. | The summary is 7 words. "Keep it outside the folder" stays in "Learn more". |
| The 4-line compose YAML was only in state panel (b1). The main "How to turn on file mode" disclosure had the one-line variable only. | "Show it in a compose file", with Copy, in the main disclosure too. |
| Earner counts did not line up from box to box under 1000 px ("In a file: 0" inline, then the next count on another line). | Under 1000 px each count is a fixed column with its label above the number. At 900 px the action sits to the right on the same line. |
| The "Not configured" badge (checklist 4) was never drawn. The "Not set up" fold was never shown open. | Panel (h0): the fold open, nine "Not configured" collectors, Anyone Protocol open with its real catalog hint open and its own Save. |
| Import step 2 lacked the row state "Nothing to deploy", the field states "still the example value" and "needs retyping", and the extras "already deployed by CashPilot" and "part of the earnings login is already in Settings" (checklist 41). | Panel (e6). |
| Restore showed a made-up done message, and no "waits for the LAN fence" message (checklist 20). | The real `done_started` text, and `done_fenced` in a caption. The check error ("Error {status}") is in (g3). |
| The held device-id row said "deploy" in its hint but "Restore sent here" as its state. Its Forget confirm used made-up text instead of `app.ids.forget_pending`. | The row is a held deploy. It uses the real `forget_pending` text. The held-restore text and the plain Forget text are in the caption. |
| Two device-id rows (node, backup) had lost their first and last seen times (checklist 12). | Both lines show. |
| The "Store a value that does not take effect" disclosure on the main view held no inputs and no Save anyway. Only panel (j1) had them. | The main disclosure holds the two unlocked inputs and Save anyway. |
| (f1) drew the key already revealed. The "Show the key" button was never drawn (checklist 23). | Step 1 shows the button, then what replaces it. |
| The About chip said "Up to date" while the attention block says geiserct is too old. | The chip says "watchtower up to date", the same as the index. "Update geiserct" in the attention block calls `selectUpdateWorker` with geiserct before it scrolls. |
| Messages with no place in the mockup: collector save, clear and collect failures; device-id toasts; key delete and 409 errors; Import check-first, tick, imported, deploy-failed and drafts-error; About unknown note and worker-only started toast. | Each one is in a caption next to its control, with the real `en.json` text. |
| The phone label on Credential health said "Lasts"; the column says "Expected to last". | Same words in both. |
| At 360 px two long paths in code pushed the page 19 px wide. | Code in callouts, confirms and steps can break anywhere. Checked again: no overflow at 360, 390, 900 or 1440. |

Changed on purpose, from the brief's facts: a failed Import deploy names the box ("honeygain on worker geiserct: {error}"), not its id (fact 8).

## Open points

- "Open the dashboard" goes to the dashboard as a whole. No per-box filter exists today, so the button cannot open one box. A `?worker=` filter on the dashboard would be a separate change.
- Update keeps the native `confirm()`. It restarts the dashboard, so it stays a blocking dialog. Change and Use an id also keep `confirm()`, because their text depends on the server's answer.
- At 900 px the app's own top bar overlaps "Settings" and "+ Add service". The real `base.html` does this too, so it is not part of this design.
