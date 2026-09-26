#!/usr/bin/env python3
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets/data/search-index-v210.json"
FEED = ROOT / "assets/data/home-feed-v210.json"

CATEGORIES = {
    "italia": ("Italia", "Notizie dall’Italia: istituzioni, territori, servizi e società.", ["italia"]),
    "mondo": ("Mondo", "Notizie internazionali, geopolitica e avvenimenti dai diversi continenti.", ["mondo", "europa", "medio oriente", "asia", "africa", "gaza"]),
    "politica": ("Politica", "Elezioni, governi, parlamenti, diplomazia e relazioni internazionali.", ["politica", "elezioni", "diplomazia", "geopolitica", "governo", "parlamento"]),
    "cronaca": ("Cronaca", "Fatti di cronaca, giustizia, sicurezza e avvenimenti dai territori.", ["cronaca", "giustizia", "sicurezza"]),
    "economia": ("Economia", "Mercati, lavoro, imprese, energia e finanza spiegati con chiarezza.", ["economia"]),
    "sport": ("Sport", "Risultati, competizioni, protagonisti e storie dal mondo dello sport.", ["sport"]),
    "meteo": ("Meteo", "Previsioni, allerte e fenomeni meteorologici spiegati con fonti verificabili.", ["meteo", "previsioni", "maltempo"]),
    "tecnologia": ("Tecnologia", "Innovazione, intelligenza artificiale, piattaforme e industria digitale.", ["tecnologia"]),
    "cultura": ("Cultura", "Arte, libri e patrimonio culturale.", ["cultura"]),
    "film-serie-tv": ("Film e Serie TV", "Uscite, produzioni e protagonisti del cinema e delle serie televisive.", ["film e serie tv", "film e serie TV"]),
    "scienza": ("Scienza", "Ricerca, spazio, salute e scoperte scientifiche.", ["scienza", "spazio", "salute"]),
    "ambiente": ("Ambiente", "Clima, natura, sostenibilità, vulcani e fenomeni ambientali.", ["ambiente", "clima", "natura", "sostenibilita", "alluvione", "vulcani", "economia circolare", "rifiuti", "riciclo", "economia circolare", "rifiuti", "riciclo"]),
}


def normalize(value):
    return (value or "").lower().translate(str.maketrans("àèéìòù", "aeeiou"))


COVERS = {
    "italia": ("/assets/images/categorie/italia.jpg", "Roma al tramonto, con il Colosseo tra i tetti di cotto"),
    "mondo": ("/assets/images/categorie/mondo.jpg", "La Terra vista dallo spazio, con Europa, Africa e Asia"),
    "politica": ("/assets/images/categorie/politica.jpg", "Emiciclo parlamentare vuoto, con banchi di legno e sedute blu"),
    "cronaca": ("/assets/images/categorie/cronaca.jpg", "Strada cittadina bagnata all'imbrunire, con un lampeggiante lontano"),
    "economia": ("/assets/images/categorie/economia.jpg", "Grattacieli di un distretto finanziario al crepuscolo, riflessi sull'acqua"),
    "sport": ("/assets/images/categorie/sport.jpg", "Stadio di calcio di notte, con il prato illuminato dai riflettori"),
    "meteo": ("/assets/images/categorie/meteo.jpg", "Temporale su un borgo, con un fulmine e pioggia sugli olivi"),
    "tecnologia": ("/assets/images/categorie/tecnologia.jpg", "Primo piano di un processore e dei circuiti, senza marchi"),
    "cultura": ("/assets/images/categorie/cultura.jpg", "Galleria di un museo, con una scultura in marmo e quadri alle pareti"),
    "film-serie-tv": ("/assets/images/categorie/film-serie-tv.jpg", "Sala cinematografica con poltrone rosse e schermo illuminato"),
    "scienza": ("/assets/images/categorie/scienza.jpg", "Banco di un laboratorio, con microscopio e vetreria"),
    "ambiente": ("/assets/images/categorie/ambiente.jpg", "Lago alpino all'alba, tra bosco e cime dolomitiche"),
}


def piu_piccola(item):
    """Indirizzo del taglio piu leggero dell'immagine dell'articolo.

    Nell'elenco la figura e grande come un'icona: scaricare il taglio da 800
    pixel per mostrarlo a 112 sarebbe uno spreco su una pagina con trenta voci.
    """
    for candidato in str(item.get("srcset", "")).split(","):
        pezzi = candidato.strip().split()
        if len(pezzi) == 2 and pezzi[1] == "480w":
            return pezzi[0]
    return item.get("image", "")


def article_thumb(item):
    """Miniatura dell'articolo, decorativa: il titolo la segue subito dopo."""
    src = piu_piccola(item)
    if not src:
        return ""
    return (f'<span class="category-card-thumb">'
            f'<img src="{html.escape(src, quote=True)}" alt="" width="112" height="75" '
            f'loading="lazy" decoding="async"></span>')


def article_card(item):
    return f'''<li><a href="{html.escape(item["url"], quote=True)}">{article_thumb(item)}<span class="category-card-copy"><small>{html.escape(item.get("section", "Notizie"))}</small><strong>{html.escape(item["title"])}</strong><span>{html.escape(item.get("excerpt", ""))}</span></span><span class="category-card-arrow" aria-hidden="true">→</span></a></li>'''


def render(slug, label, description, items):
    cards = "".join(article_card(item) for item in items)
    schema_items = [{"@type": "ListItem", "position": index + 1, "url": f'https://curiomondo.it{item["url"]}', "name": item["title"]} for index, item in enumerate(items)]
    schema = json.dumps({"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{label} | CurioMondo", "description": description, "url": f"https://curiomondo.it/categorie/{slug}/", "mainEntity": {"@type": "ItemList", "numberOfItems": len(items), "itemListElement": schema_items}}, ensure_ascii=False, separators=(",", ":"))
    # L'attributo viene composto fuori dalla f-string: con la barra rovesciata
    # dentro, il file non si compila sulle versioni di Python precedenti alla 3.12.
    corrente = ' aria-current="page"'
    switches = "".join(
        f'<a href="/categorie/{key}/"{corrente if key == slug else ""}>{value[0]}</a>'
        for key, value in CATEGORIES.items()
    )
    cover_src, cover_alt = COVERS[slug]
    cover = (f'<img class="category-hero-cover" src="{html.escape(cover_src, quote=True)}" '
             f'alt="{html.escape(cover_alt, quote=True)}" width="1600" height="900" '
             f'fetchpriority="high" decoding="async">')
    return f'''<!doctype html>
<html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{label}: ultime notizie e approfondimenti | CurioMondo</title><meta name="description" content="{html.escape(description, quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="https://curiomondo.it/categorie/{slug}/"><link rel="stylesheet" href="/assets/css/site-base-v210.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><link rel="stylesheet" href="/assets/css/category-pages-v301.css"><script type="application/ld+json">{schema}</script><script defer src="/assets/js/global-header-v275.js"></script></head>
<body><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header>
<main class="category-shell"><nav class="category-breadcrumb" aria-label="Percorso"><a href="/">Home</a><span>›</span><a href="/notizie/">Notizie</a><span>›</span><span>{label}</span></nav><header class="category-hero"><div class="category-hero-copy"><span class="category-kicker">CATEGORIA</span><h1>{label}</h1><p>{html.escape(description)}</p><strong>{len(items)} articoli</strong></div>{cover}</header><nav class="category-switcher" aria-label="Altre categorie">{switches}</nav><section aria-labelledby="category-latest"><div class="category-section-head"><h2 id="category-latest">Ultimi articoli</h2><span>Dal più recente</span></div><ul class="category-list">{cards}</ul></section></main>
</body></html>
'''


def immagini_per_url():
    """Le figure degli articoli, prese dal feed della home.

    L'indice di ricerca non le contiene: senza questa lettura l'elenco della
    categoria resterebbe di solo testo.
    """
    try:
        feed = json.loads(FEED.read_text(encoding="utf-8"))
    except Exception:
        return {}
    return {voce["url"]: voce for voce in feed.get("items", []) if voce.get("url")}


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    figure = immagini_per_url()
    news = [item for item in data["items"] if item.get("url", "").startswith("/notizie/")]
    for item in news:
        voce = figure.get(item["url"], {})
        if voce.get("image"):
            item.setdefault("image", voce["image"])
            item.setdefault("srcset", voce.get("srcset", ""))
    for slug, (label, description, terms) in CATEGORIES.items():
        selected = [item for item in news if any(term in normalize(" ".join((item.get("section", ""), item.get("title", "")))) for term in terms)]
        target = ROOT / "categorie" / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(render(slug, label, description, selected), encoding="utf-8")


if __name__ == "__main__":
    main()
