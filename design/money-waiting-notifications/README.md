# Money waiting actions and Notifications settings: design proposal

## The problem

The Dashboard's **Money waiting** panel lists reminders about money you can
lose or claim, for example a Honeygain cash-out or a PacketStream balance
that expires. Each row hides some actions in a **More** menu, even on a wide
desktop. The buttons wrap and do not line up. On a desktop, every action
should sit on one line. Only a phone may fold them into a menu. Two labels
also say nothing. **Source** opens the provider's own page with the payout
or expiry rule, and the row knows when we last checked it, but the label
does not say so. **Not for me** mutes one reminder rule for one service, for
everyone who uses this CashPilot, but the label does not say so either.
Last, you cannot configure notifications at all. You cannot say "no warnings
from this app", "only payouts" or "not at night". The three push channels
that exist (ntfy, webhook, Telegram) can only be set with environment
variables. Apprise and email do not exist in the code.

## The designs

Each folder has an `index.html` mockup, a `NOTES.md` with the reasons and an
implementation plan, and shots at 1440, 900 and 390 px. The judges scored
designs 1 to 4. Design 0 is design 1 with the best parts of the other three,
so it has no score of its own.

| Design | Direction | Best for | Cost | Judge total |
|---|---|---|---|---|
| [0-recommended](0-recommended/) | Design 1's action line, plus fixed slots (from 2), the provider's domain in the rules link and one word, **Mute** (from 3), and four presets (from 4). Undo stays next to the row. | The whole ask: one-line actions, clear labels and notifications you control. | Six PRs that each ship alone. The row change is about 250 lines and needs no new storage. | None (built from 1 to 4) |
| [1-inline](1-inline/) | Every action is a text button on one line under the row's text. Snooze and Stop reminding me fold into More only on a phone. | Seeing every action as words, with no hidden menu. | About 1,000 lines. The Money waiting half is about 190 lines, with no backend change. | 23.5 |
| [2-icon-bar](2-icon-bar/) | One bar of small icons in fixed slots. Each icon shows its label on hover and focus. Settings is a grid of kinds by places. | The narrowest row, for people who learn icons. | About 1,850 lines with tests. The Money waiting half is about 300 lines. | 14.5 |
| [3-row-detail](3-row-detail/) | A closed row shows Open, Done and Details. The row opens in place and shows the rule and every other action on one line. Alerts sort into Money, Machines and App. | The calmest list, with five rows on one screen. | About 1,500 lines. The Money waiting half is about 215 lines. | 17.5 |
| [4-presets](4-presets/) | Open and a split button (Done with a caret for Later and Stop reminding me). A **Provider's rule** chip. Notifications start with four presets, and the rest is under Advanced. | People who want one click and no detail. | About 1,700 lines with tests, in three PRs. | 18.5 |

## Recommendation: design 0

All three judges picked design 1, because it is the only one that puts every
action on one line, as real text, on a desktop. Design 0 keeps that line and
fixes what the judges held against design 1:

- **Mute all {name}** is back on the desktop line, as a group:
  `Mute [This reminder] [All {name}]`, the same shape as
  `Snooze [1 day] [1 week]`.
- One word, **Mute**, is used on the row, in the foot, in the API and in
  Settings. A line under the panel title says that Done, Snooze and Mute
  apply to everyone here.
- **Source** becomes a link in the row text, for example "Claim rules on
  help.mystnodes.com, checked 24 Nov 2026".
- After Done, Snooze or Mute, the row folds to one line with **Undo**. You
  do not have to catch a toast before it goes.
- Notifications start from four presets: **Everything** (as today), **Only
  money**, **Only problems** and **Nothing**. Under them, each of six kinds
  has two boxes: **Bell number** and **Push**. A **Pause** sets 1 day to 30
  days with one click. Quiet hours sit at the top level and show what is
  quiet now and when quiet time starts next. Each channel has **Send a
  test**. Every mute is in one list.
- These choices change only what interrupts you. The bell list and the
  Dashboard always show every problem.

The full checklist against `BRIEF.md`, the backend model and the steps are in
[0-recommended/NOTES.md](0-recommended/NOTES.md).

## What happens next

These mockups are a proposal. Nothing in `app/` changes in this PR. When the
owner picks a design, the same PR implements it and deletes
`design/money-waiting-notifications/`.

The folder is outside `docs/`. `zensical.toml` sets no `docs_dir`, so the
docs site builds only `docs/` and never publishes these files.
