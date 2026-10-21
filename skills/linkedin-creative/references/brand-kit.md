# Brand kit: one JSON file per company

The kit decides how a creative looks; `rules.md` decides what it says. Copy `brands/_template.json`,
fill it, save it in the company's own folder (`./brand/<company>.json`), and pass that path to `load_brand()`.

## Where the values come from (in this order)

1. The company's brand book or design system page: take the hexes and font names as written.
2. Their website CSS: `curl -sL https://site.com | grep -o '#[0-9A-Fa-f]\{6\}' | sort | uniq -c | sort -rn | head`
   and the `font-family` / `@font-face` lines. Ignore CMS default palettes (WordPress/Gutenberg presets).
3. Ask the person. Never invent a brand colour; write where each value came from in `"source"`.

## Fields

| field | what it is |
|---|---|
| `colors.bg` | canvas. White unless the brand is truly dark |
| `colors.ink / body / muted` | title text / body text / captions |
| `colors.line / card` | borders / card fill |
| `colors.primary` (+ `_deep`, `_soft`) | the brand colour: title highlight, main bar, numbers, gate |
| `colors.on_primary` | text on primary, usually white |
| `colors.positive` (+ `_soft`) | wins and growth only. If the brand has no green, use primary |
| `colors.accent` (+ `_soft`) | optional second colour, used sparingly (one element per creative) |
| `colors.neutral` | grey for «other» and non-main bars |
| `fonts.display / body / mono` | font family names |
| `fonts.css` | stylesheet URLs (Google Fonts) |
| `fonts.font_face` | raw `@font-face` rules for fonts not on Google Fonts (point `src` at a `.woff2` URL) |
| `title.uppercase` | `true` = FULL CAPS titles |
| `title.align` | `center` (default) |
| `title.highlight` | `pill` (word on a primary-colour pill, white text) · `color` (word in primary colour) · `none` |
| `chip.enabled / required / rubrics` | category chip above the title; `rubrics` = `{key: {label, bg, fg}}` |
| `footer.left` | `photo` (+ `ring`) or `logo` (image) or `badge` (text in a dark square), then `name`, `role`, `role_style: "plain"` |
| `footer.right` | `logo` (image path) and/or `text` (site) |
| `footer.rule` | coloured line along the bottom edge |
| `language` | `uk`, `en`, … sets `<html lang>`; write the copy in the audience's language |

Image paths are relative to the brand file. Logos: SVG or PNG with a transparent background.

## Check a new kit

Render one test creative and look for: the font is really the brand font (QA `missing_fonts` empty),
Cyrillic is not a serif, the highlight colour has enough contrast with white text, the footer matches what
the company uses on its own posts. Show it to someone from the company before the first post.
