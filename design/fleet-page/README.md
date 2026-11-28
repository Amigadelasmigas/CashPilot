# Fleet page below Boxes: five design proposals

The top of the Fleet page works: the four stats and the Boxes table stay as they are. The three blocks under the Boxes table are hard to read. Running costs gives each machine a full-width block, and each block repeats the same long sentence with the machine name and the amount. The per-service figures sit far to the right of their names. In Proxies, one table cell holds seven copy lines, and their Stop and Remove buttons have different widths, so they zig-zag. A bullet list under the table shows every copy again. The Add a proxy form has fields of mixed widths. Run a copy through a proxy gives three selects and one grey line. It does not say what a copy is or what happens to the original. It does not say why a service is missing from the list, what the result looks like, or which providers forbid proxies. These five mockups show different ways to fix the three blocks. Every action that the page has today is still in each design.

## The five designs

| Design | Direction | Best for | Build cost | Judge total |
|---|---|---|---|---|
| [0-recommended](0-recommended/) | Design 1 as the base, plus the ideas that the judges agreed on from designs 2, 3 and 4 | Building now | Low to medium. Only `fleet.html` and `style.css`, about +230 / -25 lines of CSS. No change in `app.js` and no API change. One optional server addition of about 25 lines. | Not judged (made after the judging) |
| [1-tidy](1-tidy/) | The same blocks in the same order. Text with numbers goes into tables. Forms go into a 2-column grid. | The smallest change | Lowest. About 290 template and script lines, +150 / -25 lines of CSS. No change in `app.js` and no server change. | 22.5 |
| [2-cards](2-cards/) | One card per proxy, with its copies as tiles of one width. Add and edit open a drawer on the right. | A page with many proxies | High. About 900 lines touched. The copy drawer needs one eligibility call for each service, or a new batch endpoint. | 21 |
| [3-flow](3-flow/) | A guided flow: pick a box, pick a service, read a preview, then run. A ledger for Running costs. | An owner who runs a copy for the first time | Medium to high. 500 to 650 template and script lines, 170 lines of CSS, and 60 to 90 lines of Python for a batch eligibility endpoint. | 21 |
| [4-matrix](4-matrix/) | A grid with services as rows and exits as columns. Each copy is a cell. | Seeing which IP each service leaves from | High. About 200 more lines of script, and a batch eligibility endpoint of about 60 lines plus tests. | 18 |

Each folder holds `index.html` (the mockup), `shot.png` (1440 px wide), `shot-narrow.png` (900 px wide) and `NOTES.md`. The notes hold the full comparison with today, the build plan and the translation keys. In each mockup the main view is at the top. The panels under it show the other states. The cyan labels and the dashed boxes are mockup furniture and not part of the design.

The mockups use real names and figures from a running fleet. The public IP addresses are documentation addresses (203.0.113.x, 198.51.100.x and 100.64.0.x), so no real address goes into the repository.

## Recommendation

We recommend design 0. Two of the three judges picked design 1, and design 1 is the cheapest to build. Design 0 keeps it as the base: it keeps every element id, form and handler of today, so it needs no change in `app.js` and no API change. Its copy check box sits where PR #940 puts `#copy-needs`, so #940 can rebase onto it. Design 0 then adds the parts that the judges liked in the other designs:

- A card per proxy, with a visible "Test on [box]" button and one row for each copy. The Stop, Start and Remove buttons have one width, so they form a straight column.
- A short explainer of what a copy is, open until the owner hides it.
- A check box under the copy selects. Before Run, it shows a preview with real names and the facts: the new container, the exit IP, what the provider sees and what happens to the original. It also shows each risk tick and a "Tick N more lines" counter.
- A warning when the proxy leaves from the same IP as a box's own line.
- Two cost tables, by machine and by service. The service table is sorted by net, with one shared note in place of five repeated sentences.

Design 0 does not take the pick flow of design 3 or the grid of design 4. Both need the eligibility of every service, so they need a new batch endpoint. Both also make the page much longer or wider.

## Next step

These mockups are a proposal. After a design is chosen, this PR implements it in `app/templates/fleet.html`, `app/static/js/app.js` and `app/static/css/style.css`, and deletes `design/fleet-page/`.

The docs site does not publish these files. `zensical.toml` builds the site from `docs/`, and `design/` sits at the repository root, outside `docs/`. The `exclude_docs` list in `zensical.toml` also excludes `design/` under `docs/`.
