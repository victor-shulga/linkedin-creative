# Formats

All sizes in CSS pixels; `render()` doubles them (scale 2) for a sharp upload.

## Infographic: 1080×1350, one PNG

Top to bottom: chip (if the brand has one) → title → subheading (mono, one line: context or source) →
6–9 blocks → payoff band → footer. `cr.page(brand, body, title=..., sub=..., chip=...)`.

Budget: header ≈ 230 px, footer 150 px, so the body gets ≈ 930 px. A 3-column grid holds two rows of
cards of ≈ 200 px plus one chart band of ≈ 300 px. Measure with `qa()`, do not guess.

## Carousel: 1080×1350 × 7–10 slides, PNGs + PDF

LinkedIn posts a carousel as a **document**: upload `slides.pdf`. The PNGs are for preview and for other networks.
Structure ported from the Figma `linkedin-carousel` skill (Viktor's own carousels). Rule: **one thought = one slide**.

| slide | builder | contents |
|---|---|---|
| 1 · cover | `cr.slide_cover(brand, [(text, hl), ...], sub)` | brand mark + site top-left, swipe box top-right, headline 96 px left (1–2 highlighted words: the main noun), subline 36 px, cover photo bottom-right (`brand.carousel.cover_photo`), stacked name bottom-left with the last name highlighted. No footer |
| content | `cr.slide_content(brand, "Крок 2. Вейтлист", "<p>одна думка</p>", visual=html)` | section title 72 px top-left («Контекст», «Проблема», «Крок 1.», «Приклад», «Висновок»), 1–2 lines of text, then the slide's **visual** (timeline, bars, dots, funnel, mock-up, ✓/✕ table); footer. **Every slide carries a visual**: a text-only slide is a defect |
| stat | `cr.slide_stat(brand, title, "7 з 17", caption, tone)` | section title + one 240 px number + caption. `pos` only for a real win, `warn` for a loss, `ink` otherwise |
| last · cta | `cr.slide_cta(brand, post_text)` | no swipe box; «Було корисно?», a mock of the LinkedIn post menu with «Save» pointed at, «**Збережіть** собі на потім.», «І підтримайте цей пост / **лайком і коментом**» («ви», never «ти») |

Slide titles and the CTA are centered; the cover headline stays left (Viktor's reference) and fits 1–2 lines.
Swipe box (coral, white →) on every slide but the last. Then `cr.render_pages(brand, slides, out_dir)`.
`qa()` skips the density checks on these slides: one-thought slides keep air by design. See `examples/carousel.py`.

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
