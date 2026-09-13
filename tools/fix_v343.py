#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "notizie/rybakina-vince-us-open-sabalenka-numero-uno-wta-13-settembre-2026.html"
text = path.read_text(encoding="utf-8")
text = text.replace(
    '<a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo">←</a>',
    '<a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a>',
)
text = text.replace('href="/categorie/sport.html"', 'href="/categorie/sport/"')
text = text.replace(
    'https://www.bbc.com/sport/tennis/articles/',
    'https://www.olympics.com/en/news/us-open-2026-elena-rybakina-wins-first-title-world-number-one',
).replace(
    'BBC Sport — 12 settembre 2026 — conferma indipendente del risultato e del nuovo numero uno',
    'Olympics.com — 12 settembre 2026 — conferma indipendente del titolo e del nuovo numero uno',
)
path.write_text(text, encoding="utf-8")
