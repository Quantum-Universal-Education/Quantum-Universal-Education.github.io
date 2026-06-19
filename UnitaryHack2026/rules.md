# Rules of Play: Cluck & Crow

This document covers the game itself: setup, turn structure, win
conditions, and every mechanic. For an explanation of the quantum
computing concepts behind the Crow Hive's "thinking," see
[`QUANTUM_COMPUTING.mdx`](./QUANTUM_COMPUTING.mdx). For installation and
controls, see [`README.md`](./README.md).

## Setup

Before play begins you choose two things:

1. **Flock size** — Easy (2 Hens vs. 2 Crows), Medium (3 vs. 3), or Hard (5
   vs. 5). Larger flocks mean more birds to track and a bigger, slower-to-
   compute Max-Cut graph for the Hive's quantum circuit each turn.
2. **Hive Intelligence** — how many quantum annealing steps the Crow Hive's
   circuit gets each turn (Erratic / Balanced / Sharp / Ruthless). This can
   also be adjusted live during play with the `+` and `-` keys.

Each bird starts with three **feather genes** (slots `a`, `b`, `c`), each
either Hen-colored, Crow-colored, or unexpressed. Starting birds are mostly
homogeneous (e.g. all-Hen-colored or all-Crow-colored) with a few
unexpressed slots mixed in, so there's room for genetic drift once
breeding starts.

## The Coops and the Fence

The field is split into two coops by a fence, drawn horizontally across
the middle of the screen. A bird's **side** (which coop it's currently
standing in) is independent of its **species** (which team it ultimately
counts toward). At the start of the game, side and species match — every
Hen starts in the Hen-coop, every Crow starts in the Crow-coop — but this
can and will diverge as birds cross the fence and breeding mixes things up.

## Turn Structure

A full round has three phases, always in this order:

### 1. Flap Phase

You click one of your Hens, then click it again to send it across the
fence to the opposite coop. (You can only move birds whose species is
Hen — clicking a Crow does nothing, even if it happens to be standing on
your side.)

Immediately after your move, the **Crow Hive takes its turn**. It builds a
fresh quantum circuit encoding the entire current flock arrangement, runs
it, and moves one Crow according to what the circuit's measurement
suggests. See `QUANTUM_COMPUTING.mdx` for exactly how this decision gets
made. If Full Tutorial Mode is on, a non-blocking corner overlay walks
through each stage of that process while it happens.

### 2. Breed Phase (every round)

Breeding and molting happen after every single flap-phase turn — your move
and the Hive's response both count as one full round, and breeding/molting
follows immediately after.

On each coop side, if there are two or more birds present, a chick is
born. The chick's three feather genes are inherited from its two parents:

- If only one parent expresses a given gene, the chick inherits that
  parent's value.
- If both parents express it, the chick randomly inherits one parent's
  version (50/50).
- If neither parent expresses it, the chick's gene stays unexpressed.

The chick's overall **species** is then decided by majority vote across
its three genes: whichever color (Hen or Crow) appears in more of its
expressed genes wins. A tie defaults to the species of the first parent
breeding pair listed (effectively a coin flip in practice, since parent
order is randomized when pairing is automatic).

**Who picks the parents?** If a coop side has two or more **Hen-species**
birds standing on it, you get to choose: click any two birds on that side
to pair them up, or press `SPACE` to skip and let the game pick randomly
instead. The Crow Hive's own side always breeds randomly — only you get
to choose breeding pairs, and only on sides where you have birds present.

This is the core strategic lever of the whole game: since breeding pairs
are grouped by **current coop side**, not fixed species, a coop that's
accumulated a mix of Hens and Crows (because of fence-crossings) can be
deliberately bred back toward one species by choosing two strong same-
colored parents — or left to chance if you skip.

### 3. Molt Phase (same rounds as Breed)

Right after breeding, one bird "retires" from each coop side that has
**more than one bird present**. Older birds are more likely to be picked:
the chance of being chosen for retirement is weighted by each bird's age
(every bird ages by one each cycle). A brand-new chick (age 0, weighted
minimum of 1) can still occasionally be picked, but it's far less likely
than an old-timer.

A coop side with only one bird never molts — it's protected until either
that bird crosses the fence again or a chick joins it through breeding.
This keeps the flock from accidentally dwindling to nothing on one side
while play is still in progress.

## Winning and Losing

The game checks, after every Breed+Molt cycle (i.e. after every round),
whether every single bird remaining on the field is now the same species.
If every bird is a Hen, **you win**. If every bird is a Crow, **you
lose**. If both species are still present, play continues to the next
round.

Because breeding pairs by coop side rather than fixed species, and because
every starting bird has at least one unexpressed gene (making cross-
species chicks genuinely possible rather than vanishingly rare), species
composition converges fairly quickly in practice — typically within about
5-15 rounds on Easy, and proportionally longer for bigger flocks (Medium
and Hard), though it still depends on luck (random pairing when you skip a
breeding choice, random molt victim) and on how well you use your
breeding choices to reinforce the species you want to win.

## On-Screen Information

- **Bird circles**: gold/cream = Hen, deep indigo = Crow. A small label
  under each bird shows its three genes as letters (`H`/`C`/`_`).
  A white ring means that bird is currently selected for a move.
- **Phase message** (top-left): tells you what's currently happening —
  whose turn it is, or which phase is active.
- **Max-Cut graph panel** (right side, toggle with `G`): a live view of the
  graph the Hive's quantum circuit is solving each turn. Gold nodes are on
  one side of the most recent measured split, dark nodes on the other.
  During the entanglement step, connected nodes glow and pulse to show
  where RZZ gates are acting.
- **Probability bar chart** (below the graph, appears after each
  measurement): the top 5 most-frequently-measured outcomes out of 2000
  simulated shots, with their probabilities. This is the direct evidence
  that the Hive's answer is a statistical likelihood, not a guaranteed
  certainty — watch how the bars sharpen (one dominant bar) at high Hive
  Intelligence settings versus flatten out (several similar-sized bars) at
  low settings.

## Controls Quick Reference

| Input | Effect |
|---|---|
| Click a Hen, then click it again | Move that Hen across the fence |
| Click two birds during Breed phase | Choose them as breeding parents |
| `SPACE` (during breeding choice) | Skip choosing — pair randomly instead |
| `SPACE` (during tutorial / intro) | Advance immediately, skip the wait |
| `G` | Toggle the Max-Cut graph panel |
| `T` | Toggle Full Tutorial Mode on/off |
| `+` / `-` | Raise/lower the Hive's annealing steps mid-game |
| `ESC` / close window | Quit |
