# Formats

All sizes in CSS pixels; `render()` doubles them (scale 2) for a sharp upload.

## Infographic: 1080×1350, one PNG

Top to bottom: chip (if the brand has one) → title → subheading (mono, one line: context or source) →
6–9 blocks → payoff band → footer. `cr.page(brand, body, title=..., sub=..., chip=...)`.

Budget: header ≈ 230 px, footer 150 px, so the body gets ≈ 930 px. A 3-column grid holds two rows of
cards of ≈ 200 px plus one chart band of ≈ 300 px. Measure with `qa()`, do not guess.

## Carousel: 1080×1350 × 5–10 slides, PNGs + PDF

LinkedIn posts a carousel as a **document**: upload `slides.pdf`. The PNGs are for preview and for other networks.

| slide | contents |
|---|---|
| 1 · cover | chip + title (the NAME of the carousel) + one big visual or number; swipe arrow top-right |
| 2…N-1 · content | one thought per slide: eyebrow («Крок 2»), a short slide title, 1–3 lines of body OR one visual |
| stat slide | one huge number + what it is; «positive» colour only for a real win |
| last | no swipe arrow; a directive («Збережіть…») or, on a lead-magnet post only, the gate |

Every slide: page counter `<div class="pageno">03 / 08</div>`, footer. Build each slide with
`cr.canvas(brand, body, title=None, extra=...)`, then `cr.render_pages(brand, slides, out_dir, extra_css=...)`.
Body text on slides is big: 28–32 px; slide titles 56–72 px. See `examples/carousel.py`.

## Lead magnet: cover + the magnet

**Cover (1080×1350, single image, never a carousel).** Shows the magnet itself (a picture of the document,
the template, the table) + what is inside + the gate: `cr.gate("СЛОВО", "що саме прийде в особисті")`.
The title names the magnet. Numbers on the cover must exist inside the magnet.

**The magnet.** A working template the reader fills in beats a checklist they read once. One of:
- an A4 PDF in the same brand: `cr.document(brand, pages, size="a4")` + `cr.render_pdf()`; 1–5 pages,
  each page a `cr.canvas()`. Checklists, templates, one-pagers, scorecards.
- a link (a page, a sheet, a skill). Then check that the link opens for a stranger, logged out.

**The post** (not this skill's job, but the cover must fit it): gift first, then what's inside as `→` bullets,
one line of trust with a source, «Забирайте», the gate word. ~100–130 words. See `examples/magnet.py`.

## Sizes available

`"post"` 1080×1350 · `"square"` 1080×1080 · `"a4"` 1240×1754 · or any `(w, h)` tuple.
