# Shapes: 24 forms a creative can take

Pick the shape from the CONTENT, not from the last thing you built. Every shape below builds on the HTML kit
(`scripts/creative.py`); shapes 1–10 are the everyday ones, 11–24 are for denser teaching creatives.
Rules from `rules.md` apply to all of them: the title names the thing, one accent per card, positive colour
only for real wins, 6–9 blocks, every number has an address.

Wherever a recipe below says «coral» or «forest», read the brand's `primary` and `positive` colours.

## Selection table

| # | shape | serves content that is… | anatomy in one line | how it gets ruined |
|---|---|---|---|---|
| 1 | Comparison Table | 2–3 columns × 4–6 rows, weak vs strong | dark header row, coral dot per row label, 3 punchy bullets per cell | bullets over 6 words; the rhythm dies |
| 2 | Step Grid 3×3 | 6/9/12 parallel tips | equal cards, badge + title + 2 lines | 7, 8, 10 or 11 items; they never fit 3 columns |
| 3 | Donut / Pie | 4–6 parts of a whole summing to 100 | donut left, legend right, biggest slice coral | slices that do not sum to the stated total |
| 4 | Funnel | 3–5 stages that narrow | trapezoids, opacity ramp, last tier forest | drop-off percentages invented to make the shape |
| 5 | Growth Curve | one metric over time | bezier in the lower band, milestone dots | a curve with no axis; it reads as decoration |
| 6 | Timeline (axis) | two opposed states on one horizontal axis | axis + zones below + tick quotes above | three zones; the contrast needs exactly two |
| 7 | Block Grid | a whole framework, 6–9 blocks each with its own diagram | badge + title + descriptor + mini-visual per card | the mini-visuals turn into text in boxes |
| 8 | Vertical Steps | 3–5 ordered steps, each deserving one concrete band | number + title + caption + full-width band | reusing chart atoms; these bands are interface-like |
| 9 | Ladder | 4–7 ranked tiers | staircase indent, coral fade, 6-dot meter | the state line written as a category, not a fact |
| 10 | Timeline Rows | 5–7 periods with a hidden inside and a visible outside | badge + built + quote pill + what they see | the right column holding labels instead of answers |
| 11 | **Spine + Satellites** | 4–6 stages that each need context on both sides | centre stage column, left = where/what to measure, right = stat + play | satellites that repeat the stage name instead of adding a number |
| 12 | **Hub & Flows** | an architecture: inputs → core → outputs, over a base layer | 3–4 in-cards → framed core → 3–4 out-cards, base layer arrow up | drawing it before the core is actually the core |
| 13 | **Tier List** | a ranked verdict over 15–25 named things | S→F coloured rail on the left, chips wrapping per row | every tier equally full; the shape only works if S is nearly empty |
| 14 | **Claim + Evidence** | N tactics where each needs proof | 3 columns: what it is, when it works, who grew this way | the evidence column carrying opinions instead of names |
| 15 | **Diagnostic Cards** | 3–5 checks a reader runs on themselves | numbered card, red flag / green flag / one real example | flags that are opposites of each other word for word |
| 16 | **Roster Grid** | 12–16 named people or items in 3–4 categories | category rail rotated on the left, 4 cards per row, one number each | a roster with no number under each name |
| 17 | **Panel Grid** | a curriculum or plan of 4–6 blocks, each holding 2+ entries | numbered dark header per panel, entries with 3 labelled lines | entries with different label sets per panel |
| 18 | **Centre + Orbit** | one system whose blocks all feed a shared core | ring or square core in the middle, 6–8 numbered blocks around it, connectors | an orbit that is really a list; if order matters use Vertical Steps |
| 19 | **Spec Rail** | 4–5 variants of one thing, compared on identical criteria | vertical rail with numbered nodes, one card per variant, the SAME 4 labelled lines in each | the label set drifting between cards; then it stops being a spec |
| 20 | **Rail + Artifact** | 4 concepts that each need a picture and something to copy | rail node, concept + one-line definition, real mini-flow diagram, grey strip with the exact prompt or command | a strip that paraphrases instead of giving the literal text |
| 21 | **Maturity Staircase** | 4–5 stages where the system itself gets more complex | descending panels with folded tab labels; inside each panel the diagram grows | drawing the same diagram at every stage; the growing complexity IS the data |
| 22 | **Step Spine** | 5 steps where each one needs a real diagram, not a sentence | narrow left card says WHAT the step is, wide right panel shows HOW, arrows down the page | the right panel repeating the left card as prose |
| 23 | **Onion + Sectors** | one core everything downstream depends on | nested rings out from the core, radial lines cutting the outer rings into owner sectors | rings that are categories rather than layers of dependency |
| 24 | **Named Venn** | 3 inputs whose combinations are the actual point | 3 circles, each = name + what it is made of; every overlap labelled with the capability it unlocks | overlaps labelled with nouns; they must name what becomes possible |

## Recipes for the new shapes

### 11 · Spine + Satellites

The densest teaching shape on the list. A vertical column of stages down the middle;
each stage has a left satellite (where it happens, what to measure) and a right
satellite (one hard number, then the play). Reads as a lesson, not a menu.

```python
# (stage no, name, question, [where it happens], [what to measure], stat, stat line, [plays])
STAGES = [("1", "Отримати показ", "Чи модель узагалі дістає вашу сторінку?",
           ["краулери", "індекси"], ["активність бота", "зібрано проти пропущено"],
           "28,3%", "цитованих сторінок мали нуль видимості за ключами",
           ["Ранг перестає бути табло.", "Сторінку, яку не дістали, не цитують."])]
```

Budget: 5 stages at 1350px means ~200px per band. The stage shape itself is a
flattened cylinder, 2 ellipses plus a body; at 4 stages it can be a real trapezoid.
The right-hand stat card is ink with the number in the accent colour, and it is the
only place a percentage appears.

Ruined by: satellites that restate the stage. Each satellite must carry something the
stage name does not: a tool, a number, an instruction.

### 12 · Hub & Flows

An architecture diagram. Left column = what comes in, centre = the system of record,
right column = what work goes out, bottom = the data layer with an arrow pointing up
into the core.

Rules: in-cards and out-cards are the same size and count (3–4 each), or the diagram
reads as lopsided. The core gets a coloured frame and a two-line label; everything
else is white on card. Arrows are plain, one per row, no curves.

Use it when the point is **where things live**, not what happens in what order. If a
reader could ask "and then what?", the content belongs in Vertical Steps.

### 13 · Tier List

Dark canvas, S→F rail on the left in a colour ramp, one row per tier, chips wrapping
inside each row. Each chip = icon + name.

Non-negotiable: **the distribution is the argument.** S holds one item, F holds the
things you are calling out. A tier list with five items in every row says nothing.
The F row is where the opinion lives, so it must name real things.

This is the one shape that ships on a dark background. Keep the brand accent for the
S rail and let the rest of the ramp be neutral steps, not a rainbow.

### 14 · Claim + Evidence

Three columns with a thin rule between rows: what the tactic is, the one condition
under which it works, and who actually grew that way. The third column is logos or
names, three per row.

The whole value is column 3. If a row has no real name to put there, the row does not
go on the creative. This is the shape to use when the post's job is credibility
rather than instruction.

### 15 · Diagnostic Cards

3–5 stacked white cards. Each: number badge, icon, question as the card title, then
three panels: red flag (what a bad answer looks like), green flag (what a good one
looks like), and one real example pinned to the right.

Rules: red and green must not be word-for-word inversions, or the reader learns
nothing. The example panel carries a name and a number. A card without an example is a
card with two opinions.

### 16 · Roster Grid

Four rows, each a category with its label rotated vertically on a coloured rail at the
left, then four cards. Each card: portrait or logo, name, one number, one unit line.

Works for "who to follow", "who we scanned", "which accounts". The number under each
name is mandatory: without it the grid is a collage.

### 17 · Panel Grid

4–6 panels in a 2-column layout. Each panel has a dark header with a circled number
and a title, then two entries. Each entry: cover thumbnail on the left, name, and
three labelled lines that use the SAME three labels in every panel.

The repeated label set is what makes it scannable. Pick three labels and never vary
them: for example пастка / як насправді / що робити.

### 18 · Centre + Orbit

The shape Maja Voje's GTM architecture uses; good for any «map of the system».
A core in the middle (ring, square or the bowtie band), numbered blocks placed
around it, dashed connectors from block to core.

Each block: number badge, title, 2 bullets, one TRACK line naming the metric, then a
row of tool chips. The tool chips are what the current Block Grid lacks and are the
reason that card reads as a system rather than a list.

Budget at 1080×1350: a centre of ~380px leaves two columns of ~300px on each side, so
six blocks fit around it comfortably and eight only if the bullets drop to one line.
Blocks that do not fit go into a full-width band below the orbit.

### 19 · Spec Rail

Reads like a documentation page, which is exactly why it lands: a thin vertical rail
down the left with numbered nodes, and one white card per variant. Each card carries an
eyebrow, the variant name, a one-line hand-off note, and then **four numbered lines with
the same four labels in every card**.

The labels are chosen once for the whole creative. For a comparison of approaches:
що запускає · коли зупиняється · для чого підходить · як не переплатити.

Close with a full-width band split into two columns of short bullets, under a single
heading. That band is where the advice that applies to all variants goes.

The repeated label set is the whole mechanic. A reader scans one card, learns the
grammar, then reads the other three at speed.

### 20 · Rail + Artifact

The teaching shape with the highest save rate: four concepts, each with a name, a
one-line definition, **a real mini-flow diagram** (boxes, arrows, a decision node), and
under it a grey strip holding the literal text the reader can copy.

Rules: the diagram is a mechanism, not decoration, so it must contain at least one
arrow that goes backwards or a decision that branches. The strip is monospace, prefixed
with a small label, and holds the exact prompt or command, never a summary of it.

This is the shape for «як це працює і що ввести». If there is nothing to copy, it is
shape 19 instead.

### 21 · Maturity Staircase

Stages descend left to right and top to bottom, each a wide panel with a coloured
folded tab carrying the stage number and name. Inside the panel sits that stage's
architecture, drawn with real tool logos.

The mechanic: **stage 1's panel holds one box, stage 5's holds fifteen.** The reader
sees the complexity grow down the page without reading a word. If every panel has the
same number of boxes, the shape is wasted and Panel Grid is the honest choice.

Budget: five stages at 1350px means ~230px per panel, so stage 1 and 2 will have dead
space on the right. Leave it. That emptiness is what makes stage 5 read as dense.

### 22 · Step Spine

Five rows down the page. Each row: a narrow left card (step number, name, two lines of
why, sometimes a small legend or test box) and a wide right panel holding the actual
content as a diagram: chips, grouped boxes, a formula, a matrix. An arrow runs left
into the panel, and another runs from the row down into the next step.

Two mechanics make it work:

- **Colour carries meaning across the whole image.** One row holds a legend
  («звідки береться цей елемент»), and every fill in every other row obeys it. Colour
  stops being decoration and becomes a second axis the reader can read without text.
- **Each row has its own tint**, so the five steps separate at a glance even before
  anything is read.

Credit the source of a borrowed framework in small italics under the panel it belongs
to, not in the header. The rule against borrowed numbered frameworks still
applies to the *voice*: use the shape, rewrite the content.

The densest shape on this list. Budget 5 rows in 1350px only if the left cards stay at
2–3 lines; at 4 rows the panels can hold a real matrix.

### 23 · Onion + Sectors

Concentric rings out from a named core, with two or three radial lines cutting the
outer rings into owner sectors labelled along the arcs. Chips sit inside each
ring-sector.

The argument it makes: **everything in the outer rings inherits from the core**, so a
wrong core breaks hundreds of artifacts. That is the only argument this shape makes
well. If the rings are just categories of equal standing, use Block Grid.

Rules: the core is the smallest circle and carries the shortest label. Ring count 3–4.
Chips in the outer ring can be many and slightly scattered; the density is the point,
because it shows how much depends on the middle.

Build mechanics (HTML backend). Place every chip by polar coordinates from the centre:
`x = cx + r·cos(θ−90°)`, `y = cy + r·sin(θ−90°)`, with θ measured clockwise from 12
o'clock, and `transform: translate(-50%,-50%)` so the chip centres on the point. Outer
chips sit on two arcs at about 0.40 and 0.86 of the way across the annulus. Ring labels
are ink pills pinned at the top of each ring on the vertical axis; sector labels sit
just outside the outer circle, and their angles are set **by hand**, not at the sector
midpoint, because the midpoint lands on a chip more often than not. Count the outer
chips and make any number in the rule band match that count.

### 24 · Named Venn

Three circles. Each carries a name and a one-line note on what it is made of. **Every
pairwise overlap is labelled with the capability it unlocks**, and the triple centre is
the thing being defined, pinned with a callout label outside the diagram.

The discipline: overlap labels are verbs, not nouns. «краще кваліфікуємо», «точніше
пишемо»: what becomes possible when those two inputs exist together. An overlap
labelled with a noun teaches nothing and the shape collapses into a decorative diagram.

Use it for definitions the reader thinks they already know.

## Anti-monotony rule

Do not use the same shape twice in a row, and not more than twice in any five creatives. Keep a log next
to your brand file (`creatives-log.md`: date · topic · shape) and read it before picking.

## Credit

Shapes 11–24 were read off public LinkedIn creatives by GTM authors (Maja Voje, Charlie Hills, Dan Rosenthal,
Douwe Wester). Only the shape is borrowed: content, colours and voice stay yours.
