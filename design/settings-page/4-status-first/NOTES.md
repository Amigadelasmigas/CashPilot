# Design 4: Status first

The page opens with what needs you. A short list says what is wrong, and each item has a **Show me** link to its section. Under it, every section is a card of compact rows. Each row has a label on the left, then the current value, then the action on the right. Each section has one short sentence on top. The rest of the text is behind **Learn more**, a **How** link or a **?** button. Earner credentials becomes a progress meter plus one chip per box.

Files:

- `index.html`: the mockup. It links `../../../app/static/css/style.css` and adds a `<style>` block for the new parts only.
- `shot-1440.png`, `shot-900.png`, `shot-390.png`: full-page renders, shot on the MacMini.
- `phone-390.png`: the main view alone at 390 px (`index.html?embed=1`). Panel (g) shows it as a picture. An iframe painted blank in a full-page screenshot, because Chrome does not paint a frame that is outside the viewport. In the real app, panel (g) is simply the page on a phone.

## What changed against today, and why

| Today | This design | Why |
|---|---|---|
| The page opens on Earnings collection. Problems sit inside each section's prose. | A **Needs your attention** strip comes first: one line per problem, with a one-line reason and **Show me**. A footer line lists what looks fine. When nothing is wrong, it says "Nothing needs your attention" in green (panel c). | The owner opens Settings to fix something. The page should say what to fix before anything else. |
| A flat index of nine links. Import looks like a section but opens `/import`. | The index has five groups: Earnings, Security, Move and restore, Alerts, System. Each link that needs work has a status dot, and the current section is marked. Import is a real section, `#set-import`. Under 1100 px the index becomes wrapped chips. | You see at a glance where the problems are. Import is no longer a disguised link to another page. |
| Each section opens with a paragraph of 25 to 91 words. | One sentence, up to about 15 words. **Learn more** opens the rest as short bullets. Nothing is cut. | The walls of text are the main complaint. The facts stay, one disclosure away. |
| Controls sit under the explanations. | Every control is on its row, at the right. The main action of a section is in its header, next to a status chip. | Actions are easy to find, and they are always in the same place. |
| Earner credentials: 228 words of prose, a YAML block, no control. | A meter "0 of 23 earners protected", then one chip per box (mode, count, mini bar, next step), then the steps behind **How to protect them**. Each step has a Copy button. Undo is one line. | Status becomes a glance. The fix becomes three numbered steps. |
| The Environment intro and its note repeat "a stored value does not take effect" (131 words). | A chip says "Read when CashPilot starts". One line says where to change values. The words beside **Save anyway** say "Stores the value only. It does not take effect." Locked values show as plain text with a lock chip, not as disabled inputs. | The same warning is not said three times. Read-only facts no longer look editable. |

## How each listed problem is solved

1. **Import is a separate page.** It is now section `#set-import` in "Move and restore". The collapsed section shows two rows: "Start an import" and "Saved imports". Its three steps open inside the card as a stepper (panel d). `/import` redirects to `/settings#set-import`, so the 4 English and 76 translated doc links keep working.
2. **Sections open with walls of text.** Every intro is now one sentence. The rest moved behind Learn more. On first view, without row data, the page has about 300 words. Today it has about 1,050 with Import added (BRIEF section 13).
3. **Earner credentials is the worst section.** The run-on sentence for each box becomes a chip:
   - mode in words: "Off: passwords in container settings", "Worker too old to say", "On", "This worker image cannot keep passwords in a file"
   - the count, for example "0 of 8 protected", with a mini bar
   - the next step: "Turn on", "Update the worker", "Redeploy 3", "Nothing to do"

   Click a chip to open the steps for that box (panel b). The YAML block is now one copyable line. The full compose snippet is behind "Show it in a compose file".
4. **Status is buried in prose.** Status now shows three times, in the same words: in the attention strip, as the dot in the index, and as the chip in the section header.
5. **Inconsistent structure.** Every section has the same structure: a header (mono title, status chip, actions), one sentence, then rows.

## Checklist against BRIEF.md section 14

| # | Item | Where it lives now |
|---|---|---|
| 1 | A way to every section, Credential health, the Notifications slot | Grouped index. Credential health is hidden when it has no rows, as today. The Notifications slot has its own index link, in Alerts. |
| 2 | Page-wide load error | Panel (h): a red banner across the top of the page. The words stay the same. |
| 3 | `#collector-<slug>`, `?highlight=`, `#set-restore`, `/import` | Collectors keep the `collector-<slug>` ids. `#set-restore` stays. `/import` redirects to `#set-import`. |
| 4 | Per collector: name, badge, hint, fields, optional, set-keep placeholder | Collector rows in two columns. Bytelixir is open in panel (a). The hint is behind **How**. |
| 5 | Save credentials | **Save <service>** inside each open collector. See "Behaviour changes". |
| 6 | Collect now + status | In the section header, with `#collector-save-status` beside it. |
| 7 | Clear credentials + confirm | Inside each configured collector, at the right. |
| 8 | "No collectors available." | Same text in the rows area. |
| 9 | Per credential: service, field, age, lifetime, expiry, status, reason, durable hint | Credential health rows. The reason and the durable hint are behind **?**. |
| 10 | Update on a failing row | **Update** jumps to that collector on this page. See "Behaviour changes". |
| 11 | Hidden with no rows | Same as today. |
| 12 | Per id: service, field, masked value, box, copy, state, seen times, hints, unreadable | Device id rows open like details. The summary line shows service, field, masked value, box, copy and state. The open row shows the seen times, the hints and the unreadable line. |
| 13 | Show, Copy, Change (+ earlier ids, Use), Forget | In the open row. The Change form opens under it, as today. |
| 14 | Add an id form | **Add an id** in the header. The form opens at the top of the rows. |
| 15 | Download all | In the header. The password prompt is unchanged. |
| 16 | Empty, load error, reload error | Panel (h) shows the empty text. The errors keep their keys. |
| 17 | Covered services, create-only, replace steps, command-line link | The lede names the services. The rest is under Learn more. |
| 18 | File picker, Check file, checking, error | The "Backup file" row. |
| 19 | Preview: container, volumes, never-overwrites, known/unknown, warnings, box select, passphrase, plain HTTP, Restore | Panel (f), both columns. |
| 20 | Done messages, not-checked error | Panel (f) toasts. |
| 21 | Why the key matters | Lede + Learn more. |
| 22 | Every status line | The rows "Where the key is" and "Copy in the data folder" (panel e). Status chips: "In the data folder", "Copy still in the data folder", "Protected". The env-same and old-copy lines become the sub-line of the copy row. |
| 23 | Move: Show, Copy, Hide, steps with code, guide link, come-back step | **Move the key out** opens four numbered steps. Each code block has Copy. The compose snippet is behind a link (panel e). |
| 24 | Delete the copy (confirm + password) | The copy row, then the confirm dialog (panel e). |
| 25 | Loading, load error | Same keys. |
| 26 | What it protects and what it does not; guide | Learn more, as four bullets. |
| 27 | Per box: name, mode, counts or "does not report" | Box chips (panels a, b, c). |
| 28 | The variable line, recreate, redeploy, undo | **How to protect them** steps, the Undo line, and the full compose snippet behind a link. |
| 29 | Loading, error, "No workers yet." | Panel (h). |
| 30 | Per variable: label, name, lock, badge, value, description | Environment rows. The badge is the chip at the right. |
| 31 | A stored value does not take effect | Header chip, lede, the words beside Save anyway, and Learn more. |
| 32 | Save anyway + messages | At the bottom of the section, with the title tooltip kept. |
| 33 | Empty state | Same text. |
| 34 | Server select, running, images, latest | About rows. "Latest release" is the chip on the Running row. |
| 35 | Button in three labels, note, worker-only note, UPGRADING link, already-running, not-Compose | The "Update" row. The note is the row's sub-line. The UPGRADING link is in Learn more. Other states replace the row content. |
| 36 | Proxy policy warning | An extra row under Images, drawn when `proxy_policy_fix` is set. It has its two commands in copy blocks. |
| 37 | Confirm, starting, started, failed, no worker, read error | Same flow. Panel (h) shows the no-worker state. |
| 38 | What Import does and does not do | Learn more in the Import section. |
| 39 | Files per tool, 4 files / 64 KiB, guides | The step 1 hint, the row sub-line, and **links to the three guides** in Learn more. Fact 7 is fixed. |
| 40 | Tool, files, paste, Check, three input errors | Panel (d) step 1. |
| 41 | Preview rows, states, fields, extras, not imported, none | Panel (d) step 2. |
| 42 | Save the ticked services + messages | Panel (d) step 2. |
| 43 | Drafts: deploy to, each draft, Deploy, Forget, Deploy all, none, stop-the-old-tool warning | Panel (d) step 3. The warning is a yellow note above the list. The collapsed section has a "Saved imports" row. |
| 44 | Notifications slot | A dashed box, "Notifications (designed in the other PR)", in its own Alerts group, with an index link. |

## Behaviour changes (small, each one deliberate)

- **Save per collector.** Today one Save sends every non-empty field of all 20 collectors (fact 13). Here each open collector has its own **Save <name>**. It sends only that collector's fields to the same `POST /api/config`. You can no longer save two collectors with one click, but you always know what you saved.
- **Credential health "Update" works.** Today it opens `#cred-modal`, which Settings does not have (fact 1). Here it is a link to `#collector-<slug>` on this page. The existing `openCollectorSection` opens and flashes that collector.
- **The attention strip** is computed in the browser from the responses the page already loads: `/api/settings/earner-secrets`, `/api/settings/encryption-key`, `/api/credentials/health`, `/api/update-info`. It shows at most five items, worst first. It has no Dismiss button, because that would need a stored state. When the problem is fixed, the item goes away.
- **No "regenerate" action.** The lane task asked for "API key revealed and regenerated confirmation". Today Settings has no regenerate action for either key. The encryption key can only be shown, copied, hidden and moved out. The fleet API key (`CASHPILOT_API_KEY`) comes from the environment and cannot be shown. Panel (e) shows the real flow instead: key revealed, then copied, then the delete-the-copy confirm, then the done state. A regenerate action would need a backend route and a key re-encryption, so it stays out of this redesign.

## Implementation cost (rough)

| Part | Work | Lines |
|---|---|---|
| `settings.html` | Rewrite the layout: grouped index, attention strip container, section cards with the header/lede/rows structure, Learn more blocks, the Import section and the Notifications slot. Keep every id that the JS and tests use (`collectors-container`, `restore-file`, `key-*`, `update-*`, `env-vars-container`...). | about 250 changed |
| `import.html` / `import.js` | Move the three steps into the Import section in `settings.html`. Load `import.js` on Settings. Its handlers stay `window.*` globals. Replace `pages.py` `/import` with a 307 to `/settings#set-import`. | about 60 template lines moved, 10 Python lines |
| `app.js` | `earnerSecretsHtml`: draw the meter and the chips (about 80 lines, replacing 17). The attention strip: one function that reads the four responses (about 70). Per-collector Save (about 15). Health Update as a link (about 5). Index status dots and current section with an IntersectionObserver (about 30). Learn more / `?` toggles through `delegate.js` (about 15). Env rows as text plus a chip for locked values (about 20 changed). | about 250 new or changed |
| `style.css` | The `sf-*` block from the mockup: index groups, attention strip, section card, rows, chips, meter, box chips, steps, stepper, slot. Uses only existing tokens. | about 190 |
| Backend | None, apart from the `/import` redirect. Every number on the page comes from routes that exist today. | 10 |
| Tests | Update the twelve tests listed in BRIEF section 10 where they match markup. `test_importers.py` and `test_frontend_wiring.py` change the most. | about 100 |
| Docs | "Settings > Earner credentials" and the other section names stay. Change the `/import` links to `/settings#set-import`, or keep them and rely on the redirect. | 0 to 80 files |

Total: about 900 lines across template, JS, CSS and tests. No new route, apart from the redirect.

## What it needs from i18n

New keys in `en.json` (about 55). Each one is a short sentence or a label:

- **Index groups:** `settings.group.earnings`, `.security`, `.move`, `.alerts`, `.system`; `settings.index.attention`.
- **Attention strip:** `settings.attn.title`, `settings.attn.clear`, `settings.attn.count` (plural), `settings.attn.show_me`; one ICU message per item with a sub-line:
  - `settings.attn.earner_secrets` "{n, plural, ...} keep their passwords in container settings." + `_sub` "On {boxes}. Anyone who can read Docker there can see them."
  - `settings.attn.key_in_data` + `_sub`
  - `settings.attn.cred_expiring` "The {service} login expires on {date}." + `_sub`
  - `settings.attn.old_workers` "Workers on {n, plural, ...} are too old to report." + `_sub`
  - the "fine" line items: `settings.attn.fine.version`, `.collected`, `.ids`, `.protected`, `.key_outside`
- **Shared:** `settings.learn_more`, `settings.how`, `settings.copy`; `settings.section_chip.*`: "Up to date", "Not protected", "All protected", "In the data folder", "Copy still in the data folder", "Protected", "{n} expiring soon", "{a} of {b} set up", "{n} kept · {m} in use", "Read when CashPilot starts".
- **Short ledes:** one per section, replacing the long `*.desc` keys on the main view. The long texts stay as the Learn more bullets, split into short sentences. That means editing the existing keys, not adding new ones.
- **Earner credentials:**
  - meter: `settings.earner_secrets.meter` "{n} of {total} earners protected", `.not_reported` "{n, plural, ...} do not report their earners", legend labels
  - chip modes: `.mode.env` "Off: passwords in container settings", `.mode.file` "On", `.mode.file_left` "On: {n} still in container settings", `.mode.unavailable`, `.mode.unknown` "Worker too old to say"
  - chip kinds: `.kind.server`, `.kind.phone`, `.kind.desktop`
  - next steps: `.next.turn_on`, `.next.update_worker`, `.next.redeploy` "Redeploy {n}", `.next.use_image`, `.next.none`
  - steps: `.steps_title` "Protect the earners on {box}", `.step1`, `.step2`, `.step3`, `.undo`, `.too_old`
  - its own `settings.earner_secrets.loading` and `.load_failed`, so it no longer borrows the key section's strings (fact 3)

  These replace `app.earner_secrets.row` and `row_mode`.
- **Encryption key:** `settings.key.where`, `settings.key.copy_row`, `settings.key.move_short` "Move the key out", `settings.key.hide_steps`.
- **Import:** `settings.import.start`, `.start_sub`, `.saved`, `.saved_sub`, `.waiting` "{n} waiting to deploy", the stepper labels, and `import.guides` with the three guide links. The existing `import.*` keys stay.
- **Environment:** `settings.env.save_note` "Stores the value only. It does not take effect."

All new text is real text in templates or JS, so the 19 locales translate it as usual. The server-side English labels (Environment rows, collector field labels, health `why`) stay as they are today (fact 5).
