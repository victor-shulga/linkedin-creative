# linkedin-creative

A **Claude skill** for every LinkedIn visual: a single-image infographic, a carousel (PNG slides + the PDF
LinkedIn wants), and a lead magnet (cover with the comment gate + the magnet itself as an A4 PDF).

The brand is a separate JSON file. The default is the Victor Shulga brand; any company drops in its own
colours, fonts, title style and footer, and the same rules apply: the title names the thing (the hook stays
in the post), charts instead of text in boxes, 6–9 blocks, a payoff inside the image, every number has an
address, and a pre-publish checklist.

Rendering is HTML → PNG/PDF with headless Chrome. No Figma, no MCP servers. A built-in check confirms the
webfonts loaded (no serif fallback on Cyrillic), nothing sticks out of the canvas or hides under the footer,
and there are no empty bands.

## Install

```bash
npx skills add victor-shulga/linkedin-creative
```

claude.ai: download the repo as ZIP → Settings → Capabilities → Upload a skill (`skills/linkedin-creative`).

Then: «зроби інфографіку з цього тексту», «карусель на 6 слайдів», «обкладинка лід-магніту»,
«креатив у бренді <company>, ось наш бренд-файл».

Check the setup: `python3 skills/linkedin-creative/scripts/creative.py doctor`.

## Your own brand

Copy `skills/linkedin-creative/brands/_template.json`, fill in your colours, fonts and footer
(`references/brand-kit.md` explains every field), keep it in your project folder and tell Claude the path.

## Requirements & integrations

| Integration | Used for | Required? | Auth/setup |
|---|---|---|---|
| Google Chrome (or Chromium / Edge) | headless render of HTML to PNG and PDF | Yes | installed locally; or set `CHROME=/path/to/chrome` |
| Python 3.9+ | runs `scripts/creative.py` (standard library only) | Yes | none |
| Internet access | loads webfonts (Google Fonts or the brand's font URL) at render time | Yes | none |
| Figma connector | optional: build the same plan on a Figma canvas for hand edits | No | official Figma connector in Claude |
| Claude Code or Claude desktop | running the skill with a local shell | Yes | `npx skills add` or «Upload a skill» |

## License

MIT
