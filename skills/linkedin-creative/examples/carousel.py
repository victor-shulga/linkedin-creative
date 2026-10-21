#!/usr/bin/env python3
"""Example: 4-slide carousel (cover, content, stat, last slide) -> slide-01..04.png + slides.pdf.
LinkedIn takes a carousel as a PDF «document» upload. Run: python3 examples/carousel.py [brand.json]"""
import pathlib, sys
SKILL = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import creative as cr

brand = cr.load_brand(sys.argv[1] if len(sys.argv) > 1 else SKILL / "brands/victor-shulga.json")
OUT = pathlib.Path.cwd() / "out-carousel"
N = 4

def no(i):  # page counter + swipe arrow on every slide but the last
    return f'<div class="pageno">{i:02d} / {N:02d}</div>' + ('<div class="swipe">→</div>' if i < N else "")

slides = [
    # 1 · COVER: the title is the NAME of what the carousel is, the hook lives in the post
    cr.canvas(brand, f'''<div class="cover">{cr.header(brand, ("ЧЕКЛІСТ КРЕАТИВУ ПЕРЕД", "ПОСТОМ"),
              "6 перевірок · 5 хвилин", chip_key="process")}
              <div class="big">6</div><div class="cap">перевірок, які відсіюють<br>креатив-довідник</div></div>''',
              extra=no(1)),
    # 2 · CONTENT: one thought per slide
    cr.canvas(brand, '''<div class="slide"><div class="eyebrow">Перевірка 1</div>
              <h2>Заголовок називає річ</h2>
              <p>«Калькулятор потужності аутрічу», а не «10 зустрічей на місяць». Якщо заголовок годиться першим рядком поста, це хук, і його місце в пості.</p>
              <div class="flow"><span class="pill">тип артефакту</span><span class="arr">+</span><span class="pill hot">предмет</span></div></div>''',
              extra=no(2)),
    # 3 · STAT: one big number + what it is. Forest/positive colour only for a real win
    cr.canvas(brand, f'''<div class="slide"><div class="eyebrow">Перевірка 4 · щільність</div>
              <h2>Скільки блоків тримає один кадр</h2>
              <div class="scale">{"".join(f'<div class="{"on" if 6 <= k <= 9 else ""}"><i></i><span>{k}</span></div>' for k in range(1, 13))}</div>
              <p>Менше шести читається як «нашвидкуруч». Понад дев'ять стрічка не дочитує.</p></div>''',
              extra=no(3)),
    # 4 · LAST: no swipe arrow, a directive or the comment gate (gate only on lead-magnet posts)
    cr.canvas(brand, '''<div class="slide end"><h2>Збережіть, щоб звіряти перед кожним постом</h2>
              <p>Повний чекліст у тексті поста.</p></div>''', extra=no(4)),
]
EXTRA = """
.cover{display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;padding-top:40px}
.cover .big{font-family:var(--display);font-weight:800;font-size:300px;line-height:1;color:var(--primary);margin-top:40px}
.cover .cap{font-size:30px;text-align:center;color:var(--ink);margin-top:10px;line-height:1.3}
.slide{display:flex;flex-direction:column;justify-content:center;flex:1;gap:26px;padding:60px 0 0}
.slide h2{font-family:var(--display);font-weight:800;font-size:64px;line-height:1.08;color:var(--ink);letter-spacing:-.02em}
.slide p{font-size:30px;line-height:1.4}
.slide .pill{font-size:22px;padding:10px 20px}
.slide .bars .row{grid-template-columns:200px minmax(0,1fr) 60px;margin:16px 0}
.slide .bars .lab{font-size:22px}.slide .bars .track{height:40px}
.end{text-align:center;align-items:center}
.scale{display:grid;grid-template-columns:repeat(12,1fr);gap:8px}
.scale div{text-align:center}.scale i{display:block;height:70px;border-radius:10px;background:var(--line)}
.scale .on i{background:var(--primary)}.scale span{font-family:var(--display);font-weight:700;font-size:22px;color:var(--muted)}
.scale .on span{color:var(--ink)}
"""
for f in cr.render_pages(brand, slides, OUT, extra_css=EXTRA):
    print(f)
print(cr.qa(OUT / "slides.html"))
