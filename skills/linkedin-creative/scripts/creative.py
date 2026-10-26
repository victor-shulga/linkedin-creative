#!/usr/bin/env python3
"""linkedin-creative render kit.

Brand file (JSON) + HTML body -> PNG (single image, carousel slides) and PDF
(carousel document, lead magnet) through headless Chrome. No Figma, no MCP.

Use from a build script:

    import sys; sys.path.insert(0, "<skill dir>/scripts")
    import creative as cr
    brand = cr.load_brand("<skill dir>/brands/victor-shulga.json")
    html = cr.page(brand, body, title=("КАРТА GTM-СИСТЕМИ", "АГЕНЦІЇ"), chip="gtm")
    cr.render(html, "out/creative.png")
    print(cr.qa(html))          # fonts loaded? anything sticking out?

CLI:
    python3 creative.py doctor                    # Chrome found? fonts reachable?
    python3 creative.py render page.html out.png  # screenshot an HTML file
    python3 creative.py qa page.html              # layout + font check
"""
from __future__ import annotations

import base64
import html as _html
import json
import math
import mimetypes
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile

KIT_DIR = pathlib.Path(__file__).resolve().parent
SKILL_DIR = KIT_DIR.parent

SIZES = {
    "post": (1080, 1350),    # LinkedIn single image and carousel slide, 4:5
    "square": (1080, 1080),
    "a4": (1240, 1754),      # lead-magnet document page, A4 at 150 dpi
}

# The two flags without which webfonts miss the frame and Cyrillic drops to a serif.
CHROME_FLAGS = ["--headless", "--disable-gpu", "--hide-scrollbars", "--no-sandbox",
                "--virtual-time-budget=6000", "--run-all-compositor-stages-before-draw"]


# ---------------------------------------------------------------- brand

def load_brand(path) -> dict:
    """Read a brand JSON. Relative asset paths resolve against the brand file."""
    path = pathlib.Path(path).expanduser().resolve()
    brand = json.loads(path.read_text(encoding="utf-8"))
    brand["_dir"] = str(path.parent)
    c = brand.setdefault("colors", {})
    c.setdefault("bg", "#FFFFFF")
    c.setdefault("on_primary", "#FFFFFF")
    c.setdefault("primary_deep", c.get("primary"))
    c.setdefault("primary_soft", c.get("card", "#F5F5F5"))
    c.setdefault("positive", c.get("primary"))
    c.setdefault("positive_soft", c.get("primary_soft"))
    c.setdefault("accent", c.get("primary"))
    c.setdefault("accent_soft", c.get("primary_soft"))
    c.setdefault("neutral", "#B9B6AE")
    brand.setdefault("title", {})
    brand.setdefault("chip", {"enabled": False})
    brand.setdefault("footer", {})
    return brand


def asset(brand: dict, rel: str | None) -> str | None:
    """Asset path from the brand file -> data: URI (file:// images are flaky in headless)."""
    if not rel:
        return None
    p = pathlib.Path(rel).expanduser()
    if not p.is_absolute():
        p = pathlib.Path(brand["_dir"]) / p
    if not p.exists():
        raise FileNotFoundError(f"brand asset not found: {p}")
    mime = mimetypes.guess_type(str(p))[0] or "image/png"
    return f"data:{mime};base64,{base64.b64encode(p.read_bytes()).decode()}"


def rgba(hex_color: str, alpha: float) -> str:
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


def esc(s) -> str:
    return _html.escape(str(s), quote=False)


# ---------------------------------------------------------------- css

def css(brand: dict, size=(1080, 1350)) -> str:
    c, f = brand["colors"], brand.get("fonts", {})
    w, h = size
    disp = f.get("display", "Inter Tight")
    body = f.get("body", "Inter")
    mono = f.get("mono", "JetBrains Mono")
    t = brand["title"]
    upper = "uppercase" if t.get("uppercase", True) else "none"
    align = t.get("align", "center")
    hl = t.get("highlight", "pill")
    mark = (f"background:{c['primary']};color:{c['on_primary']};padding:2px 14px 6px;border-radius:10px;"
            "display:inline-block;line-height:1.02" if hl == "pill" else
            f"background:none;color:{c['primary']}" if hl == "color" else "background:none;color:inherit")
    rule_color = c["primary"] if brand["footer"].get("rule", True) else "transparent"
    return f"""
{f.get('font_face', '')}
:root{{--bg:{c['bg']};--ink:{c['ink']};--body:{c['body']};--muted:{c['muted']};--line:{c['line']};
--card:{c['card']};--primary:{c['primary']};--primary-deep:{c['primary_deep']};--primary-soft:{c['primary_soft']};
--on-primary:{c['on_primary']};--positive:{c['positive']};--positive-soft:{c['positive_soft']};
--accent:{c['accent']};--accent-soft:{c['accent_soft']};--neutral:{c['neutral']};
--display:'{disp}',system-ui,sans-serif;--sans:'{body}',system-ui,sans-serif;--mono:'{mono}',ui-monospace,monospace}}
@page{{size:{w}px {h}px;margin:0}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{background:var(--bg);font-family:var(--sans);color:var(--body);-webkit-font-smoothing:antialiased}}
.canvas{{width:{w}px;height:{h}px;overflow:hidden;position:relative;background:var(--bg);
  padding:46px 56px 0;break-after:page;page-break-after:always;display:flex;flex-direction:column}}
.canvas:last-child{{break-after:auto;page-break-after:auto}}
.content{{flex:1;display:flex;flex-direction:column;min-height:0;padding-bottom:24px}}
.hdr{{text-align:{align}}}
.chip{{display:inline-flex;align-items:center;gap:8px;font-family:var(--display);font-weight:700;font-size:14px;
  letter-spacing:.12em;text-transform:uppercase;padding:9px 18px;border-radius:999px}}
.chip i{{width:7px;height:7px;border-radius:50%;background:currentColor;opacity:.9}}
h1.title{{font-family:var(--display);font-weight:800;font-size:44px;line-height:1.14;letter-spacing:-.015em;
  color:var(--ink);text-align:{align};text-transform:{upper};margin-top:20px;text-wrap:balance}}
h1.title mark{{{mark}}}
.sub{{font-family:var(--mono);font-weight:500;font-size:14px;letter-spacing:.06em;color:var(--muted);
  text-align:{align};margin-top:16px;text-transform:uppercase}}
.eyebrow{{font-family:var(--mono);font-weight:600;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:var(--muted)}}
.grid{{display:grid;gap:16px}}
.g2{{grid-template-columns:repeat(2,minmax(0,1fr))}} .g3{{grid-template-columns:repeat(3,minmax(0,1fr))}}
.g4{{grid-template-columns:repeat(4,minmax(0,1fr))}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 20px}}
.card.white{{background:#fff}}
.card h3{{font-family:var(--display);font-weight:800;font-size:20px;color:var(--ink);line-height:1.15;letter-spacing:-.01em}}
.card p{{font-size:15px;line-height:1.4;margin-top:6px}}
.num{{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:9px;
  background:var(--primary);color:var(--on-primary);font-family:var(--display);font-weight:800;font-size:17px;flex:none}}
.kpi .v{{font-family:var(--display);font-weight:800;font-size:46px;line-height:1;color:var(--ink);letter-spacing:-.02em}}
.kpi .v.pos{{color:var(--positive)}} .kpi .v.hot{{color:var(--primary)}}
.kpi .l{{font-size:14px;line-height:1.35;color:var(--muted);margin-top:8px}}
.rule{{background:var(--ink);border-radius:13px;padding:18px 24px;display:flex;align-items:center;gap:18px;margin-top:auto}}
.rule .rn{{font-family:var(--display);font-weight:800;font-size:15px;color:var(--on-primary);background:var(--primary);
  border-radius:8px;padding:7px 12px;letter-spacing:.08em;text-transform:uppercase;flex:none}}
.rule .rt{{font-weight:500;font-size:16.5px;color:#fff;line-height:1.4}}
.rule .rt span{{color:{rgba('#FFFFFF', .62)}}}
.rule .rx{{margin-left:auto;font-family:var(--display);font-weight:800;font-size:30px;color:var(--primary);flex:none}}
.gate{{border:2px dashed var(--primary);border-radius:16px;padding:20px 24px;text-align:center;background:var(--primary-soft)}}
.gate .w{{display:inline-block;background:var(--primary);color:var(--on-primary);font-family:var(--display);font-weight:800;
  font-size:30px;letter-spacing:.04em;padding:6px 18px;border-radius:10px;margin:0 6px}}
.gate .t{{font-family:var(--display);font-weight:700;font-size:24px;color:var(--ink)}}
.gate .s{{font-size:15px;color:var(--muted);margin-top:10px}}
.pill{{display:inline-block;font-weight:600;font-size:13px;padding:5px 11px;border-radius:999px;background:#fff;
  border:1px solid var(--line);color:var(--ink);white-space:nowrap}}
.pill.hot{{background:var(--primary);border-color:var(--primary);color:var(--on-primary)}}
.pill.pos{{background:var(--positive-soft);border-color:transparent;color:var(--positive)}}
.bars .row{{display:grid;grid-template-columns:230px minmax(0,1fr) 70px;align-items:center;gap:14px;margin:9px 0}}
.bars .lab{{font-weight:600;font-size:15.5px;color:var(--ink);line-height:1.2}}
.bars .track{{height:26px;background:var(--card);border-radius:7px;overflow:hidden}}
.bars .fill{{height:100%;border-radius:7px;background:var(--neutral)}}
.bars .fill.main{{background:var(--primary)}} .bars .fill.pos{{background:var(--positive)}}
.bars .val{{font-family:var(--display);font-weight:800;font-size:19px;color:var(--ink);text-align:right}}
.funnel .st{{margin:0 auto 8px;border-radius:10px;color:#fff;display:flex;align-items:center;justify-content:space-between;
  padding:0 22px;height:58px;font-family:var(--display);font-weight:700;font-size:18px}}
.funnel .cv{{text-align:center;font-family:var(--mono);font-size:12.5px;color:var(--muted);margin:-2px 0 8px}}
.dots{{display:flex;flex-wrap:wrap;gap:6px}} .dots i{{width:14px;height:14px;border-radius:50%;background:var(--line)}}
.dots i.on{{background:var(--primary)}}
.legend{{display:flex;flex-direction:column;gap:10px}}
.legend div{{display:flex;align-items:center;gap:10px;font-size:15.5px;color:var(--ink)}}
.legend i{{width:12px;height:12px;border-radius:50%;flex:none}}
.legend b{{font-family:var(--display);margin-left:auto;padding-left:14px;white-space:nowrap}}
.flow{{display:flex;align-items:center;gap:8px;flex-wrap:wrap}}
.flow .arr{{color:var(--muted);font-weight:700}}
.swipe{{position:absolute;top:46px;right:56px;width:58px;height:58px;border-radius:14px;background:var(--primary);
  color:var(--on-primary);display:flex;align-items:center;justify-content:center;font-size:30px;font-weight:800}}
.pageno{{position:absolute;top:58px;left:56px;font-family:var(--mono);font-size:13px;letter-spacing:.12em;color:var(--muted)}}
.footer{{height:150px;flex:none;margin:0 -56px;padding:0 56px;background:var(--bg);border-bottom:4px solid {rule_color};
  display:flex;align-items:center;justify-content:space-between}}
.footer .fl,.footer .fr{{display:flex;align-items:center;gap:15px}}
.footer .ava{{width:56px;height:56px;border-radius:50%;object-fit:cover}}
.footer .ava.ring{{border:3px solid var(--primary)}}
.footer .logo{{height:46px;width:auto}}
.footer .badge{{width:50px;height:50px;border-radius:12px;background:var(--ink);color:#fff;display:flex;align-items:center;
  justify-content:center;font-family:var(--display);font-weight:800;font-size:15px;letter-spacing:.03em}}
.footer .fname{{font-family:var(--display);font-weight:700;color:var(--ink);font-size:20px;line-height:1;letter-spacing:-.01em}}
.footer .frole{{display:table;margin-top:8px;background:var(--primary);color:var(--on-primary);font-weight:600;
  font-size:11.5px;letter-spacing:.06em;padding:6px 12px;border-radius:8px;text-transform:uppercase}}
.footer .frole.plain{{background:none;color:var(--muted);padding:0;letter-spacing:.02em;text-transform:none;font-size:14px;font-weight:500}}
.footer .fr img{{height:44px;width:44px}}
.footer .site{{font-weight:600;color:var(--primary);font-size:16px}}
.cs .content{{padding-top:94px}}
.cs .content:has(.cb){{justify-content:flex-start}}
.cs .go{{position:absolute;top:56px;right:56px;width:100px;height:92px;border-radius:4px;background:var(--primary);
  color:var(--on-primary);display:flex;align-items:center;justify-content:center;font-family:var(--display);font-weight:800;font-size:56px}}
.cs .mark{{position:absolute;top:66px;left:56px;display:flex;align-items:center;gap:12px}}
.cs .mark img{{height:52px;width:52px}} .cs .mark span{{font-weight:600;font-size:19px;color:var(--primary)}}
.cs .hl{{background:var(--primary);color:var(--on-primary);padding:4px 18px;display:inline-block}}
.cs h2.st{{font-family:var(--display);font-weight:800;font-size:72px;line-height:1.15;color:var(--ink);letter-spacing:-.015em}}
.cs .cb{{font-size:40px;line-height:1.38;color:var(--ink);margin:auto 0;padding-bottom:40px}}
.cs .cb p+p,.cs .cb ul+p,.cs .cb p+ul{{margin-top:34px}}
.cs .cb ul{{list-style:none}} .cs .cb li{{margin:18px 0}} .cs .cb li:before{{content:"→ ";color:var(--primary);font-weight:800}}
.cs .big{{font-family:var(--display);font-weight:800;font-size:240px;line-height:1;text-align:center;letter-spacing:-.03em;margin-top:auto}}
.cs .big.ink{{color:var(--ink)}} .cs .big.pos{{color:var(--positive)}} .cs .big.warn{{color:var(--primary)}}
.cs .bigc{{font-size:36px;line-height:1.4;color:var(--ink);text-align:center;margin:30px 0 auto}}
.cs.cover{{padding-top:0}}
.cs.cover .hd{{position:absolute;left:56px;top:280px;width:640px;z-index:2;display:flex;flex-direction:column;gap:12px;align-items:flex-start}}
.cs.cover .hd div{{font-family:var(--display);font-weight:800;font-size:96px;line-height:1.05;color:var(--ink);letter-spacing:-.02em}}
.cs.cover .hd p{{font-size:36px;line-height:1.3;color:var(--ink);margin-top:18px}}
.cs.cover .plate{{position:absolute;right:0;bottom:0;width:580px;height:640px}}
.cs.cover .photo{{position:absolute;right:0;bottom:0;width:470px;height:805px;object-fit:contain;object-position:bottom}}
.cs.cover .nm{{position:absolute;left:56px;bottom:90px;font-family:var(--display);font-weight:800;font-size:56px;line-height:1.05;color:var(--ink)}}
.cs.cover .nm .hl{{padding:4px 12px}}
.cs .ctah{{font-family:var(--display);font-weight:800;font-size:96px;line-height:1.05;color:var(--ink);letter-spacing:-.02em;margin-top:120px}}
.cs .ctap{{font-size:32px;line-height:1.4;color:var(--ink);margin-top:110px}}
.cs .ctaa{{display:inline-block;align-self:flex-start;background:var(--primary);color:var(--on-primary);font-family:var(--display);
  font-weight:800;font-size:56px;padding:14px 24px;margin-top:40px}}
"""


def font_links(brand: dict) -> str:
    urls = brand.get("fonts", {}).get("css", [])
    pre = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
           '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>') if urls else ""
    return pre + "".join(f'<link href="{u}" rel="stylesheet">' for u in urls)


# ---------------------------------------------------------------- blocks

def chip(brand: dict, key: str | None) -> str:
    cfg = brand.get("chip", {})
    if not key or not cfg.get("enabled"):
        return ""
    r = cfg.get("rubrics", {}).get(key)
    if r is None:  # free-text chip in the primary colour
        r = {"label": key, "bg": brand["colors"]["primary"], "fg": brand["colors"]["on_primary"]}
    return f'<span class="chip" style="background:{r["bg"]};color:{r["fg"]}"><i></i>{esc(r["label"])}</span>'


def header(brand: dict, title, sub: str | None = None, chip_key: str | None = None) -> str:
    """title = "One line" or (line, highlighted_word). The highlight is ONE word."""
    if isinstance(title, (tuple, list)):
        line, hl = title
        h1 = f"{esc(line)} <mark>{esc(hl)}</mark>" if hl else esc(line)
    else:
        h1 = esc(title)
    ch = chip(brand, chip_key)
    return (f'<div class="hdr">{ch}<h1 class="title"{" style=margin-top:0" if not ch else ""}>{h1}</h1>'
            + (f'<div class="sub">{esc(sub)}</div>' if sub else "") + "</div>")


def footer(brand: dict) -> str:
    ft = brand.get("footer", {})
    if ft.get("enabled") is False:
        return ""
    L, R = ft.get("left", {}), ft.get("right", {})
    left = ""
    if L.get("photo"):
        ring = " ring" if L.get("ring", True) else ""
        left += f'<img class="ava{ring}" src="{asset(brand, L["photo"])}">'
    elif L.get("logo"):
        left += f'<img class="logo" src="{asset(brand, L["logo"])}">'
    elif L.get("badge"):
        left += f'<div class="badge">{esc(L["badge"])}</div>'
    role = ""
    if L.get("role"):
        plain = " plain" if L.get("role_style") == "plain" else ""
        role = f'<div class="frole{plain}">{esc(L["role"])}</div>'
    if L.get("name"):
        left += f'<div><div class="fname">{esc(L["name"])}</div>{role}</div>'
    right = ""
    if R.get("logo"):
        right += f'<img src="{asset(brand, R["logo"])}">'
    if R.get("text"):
        right += f'<span class="site">{esc(R["text"])}</span>'
    return f'<div class="footer"><div class="fl">{left}</div><div class="fr">{right}</div></div>'


def rule(label: str, text: str, muted: str = "", number: str = "") -> str:
    """Dark payoff band. The text states a fact from the creative, not a summary."""
    m = f"<br><span>{esc(muted)}</span>" if muted else ""
    x = f'<div class="rx">{esc(number)}</div>' if number else ""
    return f'<div class="rule"><div class="rn">{esc(label)}</div><div class="rt">{esc(text)}{m}</div>{x}</div>'


def gate(word: str, what: str, lead: str = "Напишіть", tail: str = "у коментарях") -> str:
    """Comment-gate band for a lead-magnet cover: 'write WORD in the comments' + what arrives in DM."""
    return (f'<div class="gate"><div class="t">{esc(lead)} <span class="w">{esc(word)}</span> {esc(tail)}</div>'
            f'<div class="s">{esc(what)}</div></div>')


# ---------------------------------------------------------------- charts

def donut(parts, size=300, hole=0.58, center="", center_sub="") -> str:
    """parts = [(label, value, colour or None)], max 4 slices: top 3 + grey 'other'.
    None colour -> first slice primary, rest neutral greys. Returns SVG."""
    if len(parts) > 4:
        raise ValueError("donut: max 4 slices (top 3 + grey 'other')")
    total = sum(v for _, v, *_ in parts) or 1
    r, cx = size / 2, size / 2
    ri = r * hole
    greys = ["var(--neutral)", "var(--line)", "#D9D6CF"]
    out, a0 = [], -math.pi / 2
    for i, p in enumerate(parts):
        col = p[2] if len(p) > 2 and p[2] else ("var(--primary)" if i == 0 else greys[(i - 1) % 3])
        a1 = a0 + 2 * math.pi * p[1] / total
        large = 1 if a1 - a0 > math.pi else 0
        if p[1] >= total:
            a1 = a0 + 2 * math.pi - 1e-4
            large = 1
        x0, y0, x1, y1 = cx + r * math.cos(a0), cx + r * math.sin(a0), cx + r * math.cos(a1), cx + r * math.sin(a1)
        xi1, yi1, xi0, yi0 = cx + ri * math.cos(a1), cx + ri * math.sin(a1), cx + ri * math.cos(a0), cx + ri * math.sin(a0)
        out.append(f'<path d="M{x0:.2f} {y0:.2f} A{r} {r} 0 {large} 1 {x1:.2f} {y1:.2f} L{xi1:.2f} {yi1:.2f} '
                   f'A{ri} {ri} 0 {large} 0 {xi0:.2f} {yi0:.2f} Z" fill="{col}" stroke="#fff" stroke-width="3"/>')
        a0 = a1
    txt = ""
    if center:
        txt = (f'<text x="{cx}" y="{cx + 4}" text-anchor="middle" font-family="var(--display)" font-weight="800" '
               f'font-size="{size * .17:.0f}" fill="var(--ink)">{esc(center)}</text>')
    if center_sub:
        txt += (f'<text x="{cx}" y="{cx + size * .13:.0f}" text-anchor="middle" font-family="var(--sans)" '
                f'font-size="{size * .055:.0f}" fill="var(--muted)">{esc(center_sub)}</text>')
    return f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">{"".join(out)}{txt}</svg>'


def legend(parts, fmt="{:g}%") -> str:
    greys = ["var(--neutral)", "var(--line)", "#D9D6CF"]
    rows = []
    for i, p in enumerate(parts):
        col = p[2] if len(p) > 2 and p[2] else ("var(--primary)" if i == 0 else greys[(i - 1) % 3])
        rows.append(f'<div><i style="background:{col}"></i>{esc(p[0])}<b>{fmt.format(p[1])}</b></div>')
    return f'<div class="legend">{"".join(rows)}</div>'


def hbars(rows, max_value=None, fmt="{:g}") -> str:
    """rows = [(label, value, kind)] kind: 'main' | 'pos' | '' (grey). Colour only for the main item."""
    mx = max_value or max(v for _, v, *_ in rows) or 1
    out = []
    for lab, v, *k in rows:
        kind = k[0] if k else ""
        out.append(f'<div class="row"><div class="lab">{esc(lab)}</div><div class="track">'
                   f'<div class="fill {kind}" style="width:{100 * v / mx:.1f}%"></div></div>'
                   f'<div class="val">{fmt.format(v)}</div></div>')
    return f'<div class="bars">{"".join(out)}</div>'


def funnel(stages, width=860, min_ratio=0.42) -> str:
    """stages = [(label, value)]; conversion 'X% з етапу' printed between stages. Last stage positive."""
    n = len(stages)
    out = []
    for i, (lab, v) in enumerate(stages):
        w = width * (1 - (1 - min_ratio) * i / max(n - 1, 1))
        bg = "var(--positive)" if i == n - 1 else rgba_var_ramp(i, n)
        num = f"{v:,}".replace(",", " ")
        out.append(f'<div class="st" style="width:{w:.0f}px;background:{bg}"><span>{esc(lab)}</span><span>{num}</span></div>')
        if i < n - 1 and v:
            out.append(f'<div class="cv">↓ {100 * stages[i + 1][1] / v:.1f}% з етапу «{esc(lab)}»</div>')
    return f'<div class="funnel">{"".join(out)}</div>'


def rgba_var_ramp(i: int, n: int) -> str:
    # ink -> primary across the stages; keeps colour meaning without inventing hues
    return "var(--ink)" if i < n - 2 else "var(--primary)"


def dots(total: int, on: int) -> str:
    return '<div class="dots">' + "".join(f'<i class="{"on" if k < on else ""}"></i>' for k in range(total)) + "</div>"


# ---------------------------------------------------------------- carousel slides
# Four slide types: cover, content, stat, cta. One thought per slide, 7-10 slides.
# Swipe box top-right on every slide but the cta. Highlight = 1-2 words on the cover, 1 on the cta.

def _go() -> str:
    return '<div class="go">→</div>'


def _hl(text: str, on: bool) -> str:
    return f'<span class="hl">{esc(text)}</span>' if on else esc(text)


def slide_cover(brand: dict, lines, sub: str = "") -> str:
    """lines = [(text, highlighted), ...], one per headline row. Photo from brand carousel.cover_photo,
    name from footer.left.name (last word highlighted). No footer on the cover."""
    ft = brand.get("footer", {})
    R, name = ft.get("right", {}), ft.get("left", {}).get("name", "")
    mark = ""
    if R.get("logo") or R.get("text"):
        logo = f'<img src="{asset(brand, R["logo"])}">' if R.get("logo") else ""
        mark = f'<div class="mark">{logo}<span>{esc(R.get("text", ""))}</span></div>'
    rows = "".join(f"<div>{_hl(t, h)}</div>" for t, h in lines)
    photo = brand.get("carousel", {}).get("cover_photo")
    # plate = primary-colour shape behind the cut-out photo (rounded corners via a same-colour stroke)
    plate = ('<svg class="plate" viewBox="0 0 580 640"><path d="M40 680 L40 250 L400 40 L620 160 L620 680 Z" '
             'fill="var(--primary)" stroke="var(--primary)" stroke-width="70" stroke-linejoin="round"/></svg>')
    img = f'{plate}<img class="photo" src="{asset(brand, photo)}">' if photo else ""
    first, _, last = name.rpartition(" ")
    nm = f'<div class="nm">{esc(first)}<br>{_hl(last, True)}</div>' if name else ""
    return (f'<section class="canvas cs cover">{mark}{_go()}{img}<div class="hd">{rows}'
            + (f"<p>{esc(sub)}</p>" if sub else "") + f"</div>{nm}</section>")


def slide_content(brand: dict, title: str, body: str, last: bool = False) -> str:
    """title = section name («Крок 1.», «Контекст»), body = HTML (<p>, <ul><li>) at 32 px."""
    return canvas(brand, f'<h2 class="st">{esc(title)}</h2><div class="cb">{body}</div>',
                  extra=("" if last else _go())).replace('class="canvas"', 'class="canvas cs"', 1)


def slide_stat(brand: dict, title: str, number: str, caption: str, tone: str = "ink") -> str:
    """tone: ink (neutral) | pos (a real win, positive colour) | warn (a loss, primary colour)."""
    return canvas(brand, f'<h2 class="st">{esc(title)}</h2><div class="big {tone}">{esc(number)}</div>'
                         f'<div class="bigc">{esc(caption)}</div>', extra=_go()).replace('class="canvas"', 'class="canvas cs"', 1)


def slide_cta(brand: dict, plain: str, hl: str, prompt: str, action: str) -> str:
    """Last slide: no swipe box. «Корисно?» style headline + prompt + one action block."""
    h = f"{esc(plain)} {_hl(hl, True)}" if plain else _hl(hl, True)
    return canvas(brand, f'<div class="ctah">{h}</div><div class="ctap">{esc(prompt)}</div>'
                         f'<div class="ctaa">{esc(action)}</div>').replace('class="canvas"', 'class="canvas cs"', 1)


# ---------------------------------------------------------------- pages

def canvas(brand: dict, body: str, title=None, sub=None, chip_key=None, with_footer=True, extra="") -> str:
    """One page: header (optional) + body + footer, sized by the document."""
    hdr = header(brand, title, sub, chip_key) if title else ""
    return (f'<section class="canvas">{extra}{hdr}<div class="content">{body}</div>'
            f'{footer(brand) if with_footer else ""}</section>')


def document(brand: dict, pages: list[str], size="post", extra_css: str = "") -> str:
    """Wrap one or more canvas() sections into a full HTML document."""
    wh = SIZES[size] if isinstance(size, str) else size
    lang = brand.get("language", "uk")
    return (f'<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8">{font_links(brand)}'
            f'<style>{css(brand, wh)}{extra_css}</style></head><body>{"".join(pages)}</body></html>')


def page(brand: dict, body: str, title=None, sub=None, chip=None, size="post", extra_css="", with_footer=True) -> str:
    return document(brand, [canvas(brand, body, title, sub, chip, with_footer)], size, extra_css)


# ---------------------------------------------------------------- chrome

def find_chrome() -> str:
    cands = [os.environ.get("CHROME", ""),
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Chromium.app/Contents/MacOS/Chromium",
             "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
             r"C:\Program Files\Google\Chrome\Application\chrome.exe",
             r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]
    for c in cands:
        if c and pathlib.Path(c).exists():
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome", "msedge"):
        p = shutil.which(name)
        if p:
            return p
    raise RuntimeError("Chrome/Chromium not found. Install Google Chrome or set CHROME=/path/to/chrome. "
                       "Fallback: open the .html in a browser at 1080px width and take a screenshot.")


def _to_file(html_or_path, tmpdir) -> pathlib.Path:
    p = pathlib.Path(str(html_or_path))
    if len(str(html_or_path)) < 1024 and p.suffix == ".html" and p.exists():
        return p.resolve()
    f = pathlib.Path(tmpdir) / "creative.html"
    f.write_text(html_or_path, encoding="utf-8")
    return f


def render(html_or_path, png, size="post", scale=2, keep_html=True) -> pathlib.Path:
    """Screenshot the FIRST page. scale=2 -> 2160x2700, retina-sharp for LinkedIn."""
    w, h = SIZES[size] if isinstance(size, str) else size
    png = pathlib.Path(png).resolve()
    png.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        src = _to_file(html_or_path, td)
        if keep_html and src.parent != png.parent:
            shutil.copy(src, png.with_suffix(".html"))
        subprocess.run([find_chrome(), *CHROME_FLAGS, f"--force-device-scale-factor={scale}",
                        f"--window-size={w},{h}", f"--screenshot={png}", src.as_uri()],
                       check=True, capture_output=True, timeout=120)
    return png


def render_pages(brand: dict, pages: list[str], out_dir, stem="slide", size="post", extra_css="",
                 pdf=True, scale=2) -> list[pathlib.Path]:
    """Carousel / magnet: one PNG per page + (optionally) one PDF with all pages.
    LinkedIn takes a carousel as a PDF document upload."""
    out = pathlib.Path(out_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    files = []
    for i, pg in enumerate(pages, 1):
        files.append(render(document(brand, [pg], size, extra_css), out / f"{stem}-{i:02d}.png",
                            size, scale, keep_html=False))
    full = document(brand, pages, size, extra_css)
    (out / f"{stem}s.html").write_text(full, encoding="utf-8")
    if pdf:
        files.append(render_pdf(full, out / f"{stem}s.pdf"))
    return files


def render_pdf(html_or_path, pdf) -> pathlib.Path:
    pdf = pathlib.Path(pdf).resolve()
    with tempfile.TemporaryDirectory() as td:
        src = _to_file(html_or_path, td)
        subprocess.run([find_chrome(), *CHROME_FLAGS, "--no-pdf-header-footer", "--print-to-pdf-no-header",
                        f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True, timeout=180)
    return pdf


QA_JS = r"""<script>
window.addEventListener('load', async () => {
  try { await document.fonts.ready; } catch(e) {}
  const out = {fonts:{}, problems:[]};
  document.fonts.forEach(ff => {
    const fam = ff.family.replace(/["']/g,'');
    out.fonts[fam] = out.fonts[fam] || {loaded:0, failed:0};
    if (ff.status === 'loaded') out.fonts[fam].loaded++;
    if (ff.status === 'error') out.fonts[fam].failed++;
  });
  out.used = {};
  document.querySelectorAll('.canvas *').forEach(el => {
    const hasText = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
    if (!hasText) return;
    const fam = getComputedStyle(el).fontFamily.split(',')[0].replace(/["']/g,'').trim();
    out.used[fam] = (out.used[fam] || 0) + 1;
  });
  const label = el => (el.className && typeof el.className === 'string' ? '.'+el.className.split(' ')[0] : el.tagName.toLowerCase())
                      + ' «' + (el.textContent||'').trim().slice(0,40) + '»';
  document.querySelectorAll('.canvas').forEach((c, pi) => {
    const cr = c.getBoundingClientRect();
    const foot = c.querySelector('.footer');
    const fr = foot ? foot.getBoundingClientRect() : null;
    const seen = new Set();
    c.querySelectorAll('*').forEach(el => {
      if (el.closest('.bleed') || (foot && foot.contains(el))) return;
      if (['SCRIPT','STYLE'].includes(el.tagName)) return;
      const r = el.getBoundingClientRect();
      if (!r.width || !r.height) return;
      let why = '';
      if (el.closest('.cs.cover .photo, .cs.cover .plate')) return;  // bleed to the edge by design
      if (r.right > cr.right - 8 || r.left < cr.left + 8) why = 'sticks out sideways';
      else if (r.bottom > cr.bottom + 1) why = 'below the canvas';
      else if (fr && r.bottom > fr.top + 1 && !el.closest('.canvas > .swipe')) why = 'runs into the footer';
      if (!why && el.scrollWidth > el.clientWidth + 2 && getComputedStyle(el).overflow === 'hidden' &&
          !el.classList.contains('canvas') && !el.classList.contains('track')) why = 'text clipped';
      if (why) {
        // report the outermost offender only
        let p = el.parentElement, dup = false;
        while (p && p !== c) { if (seen.has(p)) { dup = true; break; } p = p.parentElement; }
        seen.add(el);
        if (!dup) out.problems.push({page: pi+1, why, el: label(el), bottom_px: Math.round(r.bottom - cr.top)});
      }
    });
  });
  document.querySelectorAll('.canvas').forEach((c, pi) => {
    const content = c.querySelector('.content'); if (!content) return;
    if (c.classList.contains('cs')) return;  // one-thought carousel slides keep air by design
    const foot = c.querySelector('.footer');
    const limit = foot ? foot.getBoundingClientRect().top : c.getBoundingClientRect().bottom;
    let maxB = content.getBoundingClientRect().top;
    content.querySelectorAll('*').forEach(el => { const r = el.getBoundingClientRect(); if (r.height) maxB = Math.max(maxB, r.bottom); });
    const gap = Math.round(limit - maxB);
    if (gap > 70) out.problems.push({page: pi+1, why: 'empty space above the footer: ' + gap + 'px (grow rows or add a block)'});
    // holes between stacked blocks (a block pushed down by margin-top:auto leaves one)
    const kids = [...content.children].map(k => k.getBoundingClientRect()).filter(r => r.height).sort((a, b) => a.top - b.top);
    for (let i = 1; i < kids.length; i++) {
      const hole = Math.round(kids[i].top - Math.max(...kids.slice(0, i).map(r => r.bottom)));
      if (hole > 90) out.problems.push({page: pi+1, why: 'empty band of ' + hole + 'px between blocks ' + i + ' and ' + (i+1) + ' (grow a block or add one)'});
    }
  });
  document.body.setAttribute('data-qa', JSON.stringify(out));
});
</script>"""


def qa(html_or_path, size="post") -> dict:
    """Layout + font check in a real Chrome. Returns {'fonts': {...}, 'problems': [...], 'ok': bool}.
    A family with loaded == 0 means the webfont did not arrive (Cyrillic will fall back)."""
    w, h = SIZES[size] if isinstance(size, str) else size
    with tempfile.TemporaryDirectory() as td:
        src = _to_file(html_or_path, td)
        text = src.read_text(encoding="utf-8").replace("</body>", QA_JS + "</body>")
        probe = pathlib.Path(td) / "qa.html"
        probe.write_text(text, encoding="utf-8")
        res = subprocess.run([find_chrome(), *CHROME_FLAGS, f"--window-size={w},{h}", "--dump-dom", probe.as_uri()],
                             check=True, capture_output=True, text=True, timeout=120)
    import re
    m = re.search(r'data-qa="([^"]*)"', res.stdout)
    if not m:
        return {"ok": False, "problems": [{"why": "QA script did not run"}], "fonts": {}}
    data = json.loads(_html.unescape(m.group(1)))
    bad_fonts = [f for f in data.get("used", {}) if data["fonts"].get(f, {"loaded": 0})["loaded"] == 0]
    data["missing_fonts"] = bad_fonts
    data["ok"] = not data["problems"] and not bad_fonts
    return data


# ---------------------------------------------------------------- cli

def _doctor():
    try:
        print("chrome:", find_chrome())
    except RuntimeError as e:
        print("chrome: MISSING:", e)
        return 1
    brands = sorted(p.name for p in (SKILL_DIR / "brands").glob("*.json"))
    print("brands in skill:", ", ".join(brands))
    b = load_brand(SKILL_DIR / "brands" / "victor-shulga.json")
    r = qa(page(b, "<div class='card'><h3>Перевірка кирилиці: їжак ґудзик</h3></div>", title=("ТЕСТ", "ШРИФТІВ")))
    print("fonts:", {k: v["loaded"] for k, v in r["fonts"].items()}, "missing:", r["missing_fonts"] or "none")
    return 0 if r["ok"] else 2


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "doctor"
    if cmd == "doctor":
        sys.exit(_doctor())
    elif cmd == "render":
        print(render(sys.argv[2], sys.argv[3]))
    elif cmd == "pdf":
        print(render_pdf(sys.argv[2], sys.argv[3]))
    elif cmd == "qa":
        print(json.dumps(qa(sys.argv[2]), ensure_ascii=False, indent=2))
    else:
        print(__doc__)
