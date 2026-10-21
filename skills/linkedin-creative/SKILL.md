---
name: linkedin-creative
description: One entry point for every LinkedIn creative - single-image infographic, carousel (PNG slides + PDF for upload), and lead-magnet cover plus the magnet itself (A4 PDF). Works for any brand - the brand is a separate JSON file (colours, fonts, title style, chip, footer); default is the Victor Shulga brand, any company can drop in its own kit. Builds HTML and renders PNG/PDF with headless Chrome - no Figma or MCP needed - and runs a layout check (fonts loaded, nothing sticking out, no empty bands). Brand-independent rules are enforced before render - title names the thing and is never the post's hook, charts instead of text in boxes, 6-9 blocks, a payoff inside the image, every number has an address, pre-publish checklist. Use when someone asks for "інфографіка", "карусель", "креатив для поста", "обкладинка лід-магніту", "лід-магніт", "креатив у нашому бренді", "infographic", "carousel", "LinkedIn creative", "lead magnet cover", or pastes post text and wants a visual.
---

# /linkedin-creative

One skill for every LinkedIn visual: **infographic**, **carousel**, **lead magnet** (cover + the file).
The **brand** is a separate file. The **rules** are the same for every brand.

```
brand file (JSON) ──┐
                    ├──> build.py (HTML) ──> scripts/creative.py ──> PNG / PDF + layout check
rules (references) ─┘
```

Files in this skill:

| file | what it is |
|---|---|
| `references/rules.md` | the rules that hold for EVERY brand + the pre-publish checklist. **Read before every creative.** |
| `references/formats.md` | infographic / carousel / lead magnet: sizes, anatomy, what goes where |
| `references/shapes.md` | 24 visual shapes: which content each serves and how each gets ruined |
| `references/brand-kit.md` | how to make a brand file for a new company (from its site or brand book) |
| `brands/victor-shulga.json` | default brand. `brands/_template.json` = empty kit to copy |
| `scripts/creative.py` | render kit: `page()`, `canvas()`, `document()`, `render()`, `render_pages()`, `render_pdf()`, `qa()`, chart helpers |
| `examples/carousel.py`, `examples/magnet.py` | runnable examples (run from any folder; output lands in the current folder) |

## Step 0: which brand

1. The user named a brand file or a company → use that file. A client's kit lives in **their** project
   folder (e.g. `./brand/<company>.json`), not inside this skill.
2. No kit for that company → build one first (`references/brand-kit.md`, ~5 minutes), save it next to their work.
3. Nothing said and the user is Victor Shulga → `brands/victor-shulga.json`.
4. Creative for **another person or company** → **their** brand and **their** audience's language. Never
   put Victor's coral, chip, bowtie or victorshulga.com on someone else's post.

## Step 1: which format

| the post… | format | output |
|---|---|---|
| explains one idea that has a shape (proportion, stages, change over time, a system) | **infographic** 1080×1350 | 1 PNG |
| teaches step by step, one thought per slide, the value IS the post | **carousel** 1080×1350 × 5–10 | PNG per slide + `slides.pdf` (upload as a document) |
| gives something away for a comment | **lead magnet**: cover 1080×1350 with the comment gate + the magnet (A4 PDF, or a link) | `cover.png` + `magnet.pdf` |

A lead-magnet post is **never** a carousel: a carousel hands the value over in the feed, the magnet must
arrive in DM. Content that is only 2–3 short things → offer a 3-slide carousel instead of a sparse infographic.

## Step 2: message, title, shape (before any code)

Write these four lines down and show them to the user if anything is unclear:

1. **One message**: what should stay in the reader's head. If you cannot say it in one sentence, stop.
2. **Title** = the NAME of the artifact: `<what it is> + <subject>` («Калькулятор потужності аутрічу»,
   «Automation business case template»). Run the 4 title tests in `rules.md`. The hook stays in the post.
3. **Shape**: pick from `references/shapes.md`. Prefer a chart whenever the data has a shape.
   Not the same shape as the last creative.
4. **Blocks**: list 6–9 blocks, each with its own mini-visual, plus the payoff band. Every number gets a
   source written next to it in the build script comment.

## Step 3: build

Create a folder for the creative, write `build.py` there:

```python
import sys, pathlib
SKILL = pathlib.Path("<absolute path of this skill>")
sys.path.insert(0, str(SKILL / "scripts"))
import creative as cr

brand = cr.load_brand(SKILL / "brands/victor-shulga.json")    # or the client's kit
body = f"""
  <div class="card white">{cr.hbars([("Канал А", 42, "main"), ("Канал Б", 30), ("Канал В", 12)])}</div>
  ...
  {cr.rule("Факт", "One sentence stating a fact from the image.", "Second, quieter line.")}
"""
html = cr.page(brand, body, title=("НАЗВА КРЕАТИВУ", "СЛОВО"), sub="контекст · джерело", chip="gtm",
               extra_css=".card{...}")
png = cr.render(html, "creative.png")           # 2160×2700, retina
print(cr.qa(png.with_suffix(".html")))          # must say ok: True
```

Kit cheat-sheet (all classes take colours from the brand file, never hard-code a hex in the body):

- Layout: `.grid .g2/.g3/.g4`, `.card` (`.white`), `.eyebrow`, `.num`, `.pill` (`.hot`, `.pos`), `.flow`, `.kpi .v/.l`
- Charts: `cr.donut(parts)` (≤4 slices: top 3 + grey "other") + `cr.legend(parts)`, `cr.hbars(rows)`,
  `cr.funnel(stages)` (conversion between stages printed), `cr.dots(total, on)`
- Bands: `cr.rule(label, text, muted, number)` is the dark payoff band; `cr.gate(word, what)` is the comment gate
- Pages: `cr.page(...)` one image; `cr.canvas(...)` one slide → `cr.render_pages(brand, [slides], out_dir)`
  writes `slide-01.png…` + `slides.pdf`; `cr.document(brand, pages, size="a4")` + `cr.render_pdf()` for a magnet
- Carousel furniture: `<div class="pageno">02 / 08</div>`, `<div class="swipe">→</div>` (not on the last slide)
- `title=("LINE", "WORD")` → the highlighted part is ONE word; `title="Line"` → no highlight

Rows are the shock absorber: if `qa()` reports an empty band, grow rows, enlarge charts or add a block;
if something runs into the footer, shrink rows. Re-render until `ok: True`.

**Figma (optional).** If the user wants to edit on canvas and a Figma connector is available, build the same
plan in Figma (load the `figma-use` skill first). HTML stays the default: it needs nothing but Chrome.

**No Chrome?** `python3 scripts/creative.py doctor` tells you. Install Google Chrome or set `CHROME=/path`.
Last resort: open the saved `.html` in any browser at 1080 px width and screenshot it.

## Step 4: check, then hand over

1. `qa()` = `ok: True` (webfonts loaded, nothing sticks out, nothing under the footer, no empty band ≥ 90 px).
2. **Open the PNG and look at it.** QA cannot see empty space inside a card, a chart that lies, or a wrong word.
3. Copy pass: dump every visible string into a `.md` and run the humanizer/AI-pattern detector if you have one
   (`anticopywriting-ai`), Ukrainian or English.
4. Walk the **pre-publish checklist** in `rules.md`, every line, and report it as ✓ / ✗.
5. Hand over: PNG (and PDF for carousel/magnet) + the checklist + the path to `build.py` for edits.

Output template:

```
✅ <format> · «<title>» · brand: <brand name> · shape: <shape>
📁 <folder>/creative.png  (+ slides.pdf / magnet.pdf)
✓ title names the thing · ✓ chart, not text boxes · ✓ N blocks · ✓ payoff band · ✓ numbers sourced · ✓ fonts · ✓ QA
Що змінити? (заголовок / форма / цифри / блок)
```

## Victor Shulga brand: extra rules (only when that brand is used)

- Rubric chip on top is mandatory, one of the 7 pillars in the brand file (`chip="gtm" | "outreach" | "social" |
  "sales" | "am" | "team" | "process"`). Design / tools / process / "my stack" → `process`.
- Title FULL CAPS, centred, coral pill on ONE word with white text. Footer: photo with coral ring + name +
  FRACTIONAL CRO pill left, bowtie + victorshulga.com right. White canvas only.
- Coral is never the majority colour. Forest green only for a genuinely positive outcome.
- No dead brand names, no client names, logos or cases on any public creative.
- Lead-magnet gate («Напишіть СЛОВО у коментарях») only on the Thursday lead-magnet post.
