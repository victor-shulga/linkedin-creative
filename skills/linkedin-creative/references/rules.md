# Rules that hold for every brand

These come from a year of creatives that were rejected and remade. Brand files change colours and fonts;
they never switch these rules off.

## 1. The title names the thing. It is not the hook.

The hook is the first line of the **post**. The title on the **image** says what the image is:
`<artifact type> + <subject>`.

Good: «Калькулятор потужності аутрічу», «Карта GTM-системи», «Плейбук GTM-системи агенції»,
«24 скіли для Claude Code», «Automation business case template», «Outbound upgrade plan».
The genre word (плейбук, карта, калькулятор, чекліст, шаблон, план, template, map) beats a description of the contents.

Rewrite the title if ANY test fires:

1. it would work as the first line of the post (a scroll-stopper) → it is a hook
2. it carries a result or a promise-number («10 зустрічей на місяць», «−1 година», «83% бюджету»)
3. it has an action verb or asks/promises an answer («як зібрати», «що для цього треба», «чому ...»)
4. a number in it is not the subject itself («24 скіли», «9 місяців» pass; «8 зон. Закрита одна» fails)

Also: no slogans («один X з п'яти Y»), no metaphors, no presentation jargon a person would not say out loud.
The figure and the thesis go one line lower, in the subheading. Post text and title never share a sentence.
The highlighted part of the title is **one word**, and it carries the subject.

## 2. A chart wherever the data has a shape

Text in boxes is the fallback, not the default.

| task | form |
|---|---|
| parts of 100% | donut, **max 4 slices**: top 3 + grey «other» (name what is inside it) |
| stages that narrow | funnel, conversion printed between stages |
| change over time | line or columns; colour only 1–2 main series, the rest grey |
| comparison / ranking | horizontal bars (long labels) or columns, value printed on every bar |
| one number vs plan / last year | KPI card: number + difference + «з чого» |
| plan vs fact, a norm | bar/line + a benchmark tick or band |
| a system | hub, orbit, spine, layers (see `shapes.md`) |

Colour only for the main item; everything else grey. One Y axis, never two. Legend markers are circles.
The «positive» colour is for a genuinely positive outcome only, never a second accent.

## 3. Density: 6–9 blocks, each with its own mini-visual

Under 6 reads as low effort, over 9 stops being readable at feed size. A block that is only a title and two
lines needs a visual: a bar, a chip row, a mini-flow, a skeleton, a dot grid. No dead space: a hole in the
grid gets a useful slice (a breakdown, a forecast) or the rows grow.

## 4. The payoff lives inside the image

A list of what exists reads as a reference page. Add the «what it changed» column or a final band with
the result («блок → файл → що це змінило», not «блок → файл»). The dark rule band at the bottom states a
**fact from the image above it**, not a summary or an image («Зустрічі з'являються на тижні 7» passes,
«Перші тижні оплачують шар даних» fails).

Pick ONE message before the template. Pouring content into a nice layout without a message gives a clean,
empty creative.

## 5. Every promise has an address

Every number, count and claim on the creative must be findable: in the post, on the landing page, inside
the magnet. Walk the reader's path yourself before posting: comment → link → gate → file → open it
**without a terminal**. A number with no public source does not go on the creative. Write the source of
every number as a comment in `build.py`. Never invent example data; if it is illustrative, say so on the image
(«Example inside», «приклад»).

## 6. Words

- Plain words a person says out loud. Abbreviations only if the audience knows them without help
  (ICP, KPI, CRM, SEO); otherwise write the phrase («дохід з клієнтів росте рік до року», not «NRR»).
- Real tool names are fine on your own creatives; generic categories kill recognition. No client names,
  client logos or client cases on anything public.
- Blocks about a team work for every role (marketing too), not only sales.
- Ukrainian creatives: no anglicisms where a Ukrainian word exists; brand and tool names stay Latin.
- Run all visible copy through an AI-pattern detector before render (em dashes, rule-of-three triads,
  «не X, а Y» are the usual hits).

## 7. Variety

Do not use the same shape twice in a row, and not more than twice in any five creatives. Keep a one-line log
per shipped creative (date · topic · shape) next to your brand file.

## Pre-publish checklist (report every line as ✓ / ✗)

- [ ] canvas colour = the brand's background (white unless the brand says otherwise)
- [ ] brand chip on top, if the brand uses chips (`chip.required`)
- [ ] title passes the 4 tests; highlight on one word; centred
- [ ] a chart or diagram, not only text in boxes; donut ≤ 4 slices
- [ ] 6–9 blocks (carousel: one thought per slide, 5–10 slides)
- [ ] payoff band / «what it changed» inside the image
- [ ] every number has a source and an address the reader can reach; illustrative data is labelled
- [ ] colours and fonts come only from the brand file
- [ ] footer present and correct for this brand (whose post is it?)
- [ ] `qa()` = ok: fonts loaded (Cyrillic not in a serif), nothing sticks out or hides under the footer, no empty band
- [ ] you opened the PNG and read every word
- [ ] no client names, logos or cases on a public creative; no names of dead brands
- [ ] lead magnet: the gate word + what arrives in DM; the asset exists and opens; single image, not a carousel
