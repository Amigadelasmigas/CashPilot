# Settings page: five layouts to choose from

## The problem

The Settings page is hard to scan. Most sections start with a long paragraph, so you read before you find a control. "Earner credentials on each box" is the worst. It has a paragraph about `docker inspect`, then one long sentence per box, then a raw YAML block. The status of each box (its mode, how many earners are safe, what to do next) is in that text. You cannot see it at a glance. Also, "Import from another tool" is in the Settings index like a section, but it opens a different page.

Each design below fixes these problems. Import becomes a card on the Settings page, and `/import` redirects to `/settings#set-import`. Every action and fact that is on the page today is still there. `BRIEF.md` section 14 is the checklist. Each design keeps a marked slot for the Notifications section. Another PR designs that section.

## The designs

Three judges scored designs 1 to 4. Design 0 combines design 1 with the best parts of the others. Nobody scored design 0, because it came after the judges.

| # | Direction | Best for | Cost to build | Judge total |
|---|---|---|---|---|
| 0 | Design 1, plus a "Needs your attention" block at the top, a status line under each index item, and an earner meter. | What design 1 gives, plus a quick view of what needs work. | About +330 / -170 lines of JS, +200 of CSS, about 85 new strings, one new API field (`kind`). | Not scored |
| 1 | Tidy in place: the same page, the same order. Each section is one card with a title, a status chip, one summary line, the controls, then "Learn more". | The smallest change. Section titles and ids stay the same, so the docs and most tests stay the same. | About +260 / -150 lines of JS, +170 of CSS. Only backend change: the redirect. | 22 |
| 2 | Sticky side menu in five groups. Each menu item shows its status. The main button of each section sits next to its title. | Moving quickly around a long page. | About 300 lines of JS, 180 of CSS. | 21 |
| 3 | Five tabs (Overview, Data, Security, Notifications, About). Overview is a checklist. | Showing one task at a time. | About 550 to 650 lines. The section names in the docs change (about 25 lines). | 21 |
| 4 | Status first: the "Needs your attention" list leads. Each section is a card of short rows: label, value, action. | Seeing what is wrong first. | About 900 lines, including tests. | 21.5 |

Each folder has `index.html` (open it in a browser), `NOTES.md` (the changes, why, the checklist and the build plan), and screenshots at 1440, 900 and 390 px wide.

## Our recommendation: design 0

- It starts from design 1. Design 1 had the top score, and it is the cheapest safe path to build.
- It adds the parts that all three judges asked for. A "Needs your attention" block shows first, and each row has a button that goes to the control. Each index item has a status line, for example "0 of 23 protected".
- Earner credentials becomes a table with one row per box. Each row shows the box kind, the mode, two counts and what to do. "Show steps" opens three numbered steps for that box, with Copy buttons and the undo line.
- It fixes every problem the judges found in designs 1 to 4. `0-recommended/NOTES.md` lists each problem and its fix.
- Section titles do not change, so the docs keep the names they use today.

## Next step

These mockups are a proposal. Choose a design. Then this same PR builds that design in `app/` and deletes `design/settings-page/`.

`design/` is outside `docs/`, so the docs site (`zensical.toml`, which builds `docs/` only) does not publish these files.
