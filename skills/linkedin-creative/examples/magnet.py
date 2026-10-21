#!/usr/bin/env python3
"""Example: lead magnet = (1) cover image for the post, with the comment gate,
(2) the magnet itself as an A4 PDF that goes out in DM. Run: python3 examples/magnet.py [brand.json]"""
import pathlib, sys
SKILL = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import creative as cr

brand = cr.load_brand(sys.argv[1] if len(sys.argv) > 1 else SKILL / "brands/victor-shulga.json")
OUT = pathlib.Path.cwd() / "out-magnet"

CHECKS = [  # (check, how to tell it failed)
    ("Заголовок = назва речі", "він годиться першим рядком поста або обіцяє результат"),
    ("Графік, де дані мають форму", "частки, етапи чи динаміка лежать текстом у рамках"),
    ("6–9 блоків", "менше шести або понад дев'ять"),
    ("Пейоф у самому кадрі", "список того, що є, без «що це змінило»"),
    ("Кожне число має адресу", "цифру не знайти в пості, на сторінці чи в магніті"),
    ("Бренд з одного файлу", "колір чи шрифт вписані руками повз бренд-файл"),
]

# (1) cover: a picture of the magnet + what is inside + the gate. Never a carousel.
rows = "".join(f'<div class="ck"><span class="box"></span><div><b>{a}</b><p>провал: {b}</p></div></div>' for a, b in CHECKS)
cover = cr.page(brand, f'''<div class="doc">{rows}</div>
  {cr.gate("ЧЕКЛІСТ", "PDF на 1 сторінку прийде в особисті")}''',
  title=("ЧЕКЛІСТ КРЕАТИВУ ПЕРЕД", "ПОСТОМ"), sub="6 перевірок · PDF", chip="process",
  extra_css=""".doc{margin:30px 40px 0;background:#fff;border:1px solid var(--line);border-radius:16px;padding:22px 28px;
  box-shadow:0 18px 40px rgba(0,0,0,.08);display:flex;flex-direction:column;justify-content:space-evenly;flex:1}
.doc .ck b{font-size:26px}.doc .ck p{font-size:18px}
.ck{display:flex;gap:16px;align-items:flex-start}.ck b{font-family:var(--display);font-size:22px;color:var(--ink)}
.ck p{font-size:16px;color:var(--muted);margin-top:4px}
.box{width:26px;height:26px;border:2.5px solid var(--primary);border-radius:7px;flex:none;margin-top:2px}
.gate{margin-top:26px}""")
cr.render(cover, OUT / "cover.png")

# (2) the magnet: A4 pages, same brand file, no gate
page = cr.canvas(brand, f'<div class="a4">{rows}</div>', title=("ЧЕКЛІСТ КРЕАТИВУ ПЕРЕД", "ПОСТОМ"),
                 sub="Пройдіть перед кожною публікацією", chip_key="process")
doc = cr.document(brand, [page], size="a4", extra_css=""".a4{display:flex;flex-direction:column;justify-content:space-evenly;flex:1;margin-top:30px}
.ck{display:flex;gap:18px}.ck b{font-family:var(--display);font-size:28px;color:var(--ink)}.ck p{font-size:20px;color:var(--muted);margin-top:6px}
.box{width:32px;height:32px;border:3px solid var(--primary);border-radius:8px;flex:none}""")
(OUT / "magnet.html").write_text(doc, encoding="utf-8")
print(cr.render_pdf(doc, OUT / "magnet.pdf"))
print(cr.qa(OUT / "cover.html"))
print(cr.qa(OUT / "magnet.html", size="a4"))
