#!/usr/bin/env python3
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/search-index-v210.json"

CATEGORIES = {
    "italia": ("Italia", "Notizie dall’Italia: istituzioni, territori, servizi e società.", ["italia"]),
    "mondo": ("Mondo", "Notizie internazionali, geopolitica e avvenimenti dai diversi continenti.", ["mondo", "europa", "medio oriente", "asia", "africa", "gaza"]),
    "politica": ("Politica", "Elezioni, governi, parlamenti, diplomazia e relazioni internazionali.", ["politica", "elezioni", "diplomazia", "geopolitica", "governo", "parlamento"]),
    "cronaca": ("Cronaca", "Fatti di cronaca, giustizia, sicurezza e avvenimenti dai territori.", ["cronaca", "giustizia", "sicurezza"]),
    "economia": ("Economia", "Mercati, lavoro, imprese, energia e finanza spiegati con chiarezza.", ["economia"]),
    "sport": ("Sport", "Risultati, competizioni, protagonisti e storie dal mondo dello sport.", ["sport"]),
    "tecnologia": ("Tecnologia", "Innovazione, intelligenza artificiale, piattaforme e industria digitale.", ["tecnologia"]),
    "cultura": ("Cultura", "Arte, spettacolo, televisione, libri e patrimonio culturale.", ["cultura"]),
    "scienza": ("Scienza", "Ricerca, spazio, salute e scoperte scientifiche.", ["scienza", "spazio", "salute"]),
    "ambiente": ("Ambiente", "Clima, natura, sostenibilità, vulcani e fenomeni ambientali.", ["ambiente", "clima", "natura", "sostenibilita", "alluvione", "vulcani", "economia circolare", "rifiuti", "riciclo", "economia circolare", "rifiuti", "riciclo"]),
}


def normalize(value):
    return (value or "").lower().translate(str.maketrans("àèéìòù", "aeeiou"))


def article_card(item):
    return f'''<li><a href="{html.escape(item["url"], quote=True)}"><span class="category-card-copy"><small>{html.escape(item.get("section", "Notizie"))}</small><strong>{html.escape(item["title"])}</strong><span>{html.escape(item.get("excerpt", ""))}</span></span><span class="category-card-arrow" aria-hidden="true">→</span></a></li>'''


def render(slug, label, description, items):
    cards = "".join(article_card(item) for item in items)
    schema_items = [{"@type": "ListItem", "position": index + 1, "url": f'https://curiomondo.it{item["url"]}', "name": item["title"]} for index, item in enumerate(items)]
    schema = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{label} | CurioMondo", "description": description, "url": f"https://curiomondo.it/categorie/{slug}/", "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": schema_items}}, ensure_ascii=False, separators=(",", ":"))
    switches = "".join(f'<a href="/categorie/{key}/"{" aria-current=\"page\"" if key == slug else ""}>{value[0]}</a>' for key, value in CATEGORIES.items())
    return f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{label}: ultime notizie e approfondimenti | CurioMondo</title><meta name="description" content="{html.escape(description, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="https://curiomondo.it/categorie/{slug}/"><link rel="stylesheet" href="/assets/css/site-base-v210.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><link rel="stylesheet" href="/assets/css/category-pages-v300.css"><script type="application/ld+json">{schema}</script><script defer src="/assets/js/global-header-v275.js"></script></head>
<body><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header>
<main class="category-shell"><nav class="category-breadcrumb" aria-label="Percorso"><a href="/">Home</a><span>›</span><a href="/notizie/">Notizie</a><span>›</span><span>{label}</span></nav><header class="category-hero"><span class="category-kicker">CATEGORIA</span><h1>{label}</h1><p>{html.escape(description)}</p><strong>{len(items)} articoli</strong></header><nav class="category-switcher" aria-label="Altre categorie">{switches}</nav><section aria-labelledby="category-latest"><div class="category-section-head"><h2 id="category-latest">Ultimi articoli</h2><span>Dal più recente</span></div><ul class="category-list">{cards}</ul></section></main>
</body></html>
'''


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    news = [item for item in data["items"] if item.get("url", "").startswith("/notizie/")]
    for slug, (label, description, terms) in CATEGORIES.items():
        selected = [item for item in news if any(term in normalize(item.get("section")) for term in terms)]
        target = ROOT / "categorie" / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(slug, label, description, selected), encoding="utf-8")


if __name__ == "__main__":
    main()
