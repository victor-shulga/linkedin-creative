#!/usr/bin/env python3
"""Example: 5-slide carousel (cover, content, stat, content, cta) -> slide-01..05.png + slides.pdf.
LinkedIn takes a carousel as a PDF «document» upload. Run: python3 examples/carousel.py [brand.json]"""
import pathlib, sys
SKILL = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL / "scripts"))
import creative as cr

brand = cr.load_brand(sys.argv[1] if len(sys.argv) > 1 else SKILL / "brands/victor-shulga.json")
OUT = pathlib.Path.cwd() / "out-carousel"

slides = [
    # COVER: the title is the NAME of what the carousel is, the hook lives in the post
    cr.slide_cover(brand, [("Чекліст", False), ("креативу", True), ("перед постом", False)], "6 перевірок · 5 хвилин"),
    # CONTENT: one thought per slide
    cr.slide_content(brand, "Крок 1. Назва",
        "<p>Заголовок називає річ: «Калькулятор потужності аутрічу», а не «10 зустрічей на місяць».</p>"
        "<p>Якщо заголовок годиться першим рядком поста, це хук, і його місце в пості.</p>"),
    # STAT: one huge number + what it is. Positive colour only for a real win
    cr.slide_stat(brand, "Щільність", "6–9", "блоків тримає один кадр. Менше читається як «нашвидкуруч»"),
    cr.slide_content(brand, "Крок 2. Цифри",
        "<p>Кожна цифра на креативі має адресу:</p><ul><li>файл</li><li>звіт</li><li>сторінка на сайті</li></ul>"),
    # CTA: no swipe box
    cr.slide_cta(brand, "", "Корисно?", "Збережіть, щоб звіряти перед кожним постом.", "+Лайк і коменти"),
]
for f in cr.render_pages(brand, slides, OUT):
    print(f)
print(cr.qa(OUT / "slides.html"))
