#!/usr/bin/env python3
from pathlib import Path
from html import escape
from PIL import Image
import hashlib, json

ROOT = Path(__file__).resolve().parents[1]
SLUG = "rybakina-vince-us-open-sabalenka-numero-uno-wta-13-settembre-2026"
KEY = "rybakina-us-open-2026-ai-openai-v343"
TITLE = "US Open, Rybakina batte Sabalenka e conquista il numero uno mondiale"
EXCERPT = "La kazaka vince la finale in tre set, 6-4 5-7 6-2, e ottiene il primo titolo a New York. Da lunedì guiderà per la prima volta la classifica WTA."
PUBLISHED = "2026-09-13T01:10:00+02:00"
IMAGE_ALT = "Scena editoriale contestuale ordinaria generata con IA di Elena Rybakina che saluta il pubblico su un campo da tennis dopo una finale"
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

body = [
"Elena Rybakina ha battuto Aryna Sabalenka nella finale femminile degli US Open sabato 12 settembre a New York. La kazaka si è imposta 6-4 5-7 6-2, togliendo il titolo alla campionessa delle due edizioni precedenti. Il successo le consegna il primo trofeo nello Slam statunitense e, da lunedì, il numero uno della classifica WTA.",
"La partita è durata tre set e ha cambiato direzione dopo il secondo parziale. Rybakina aveva vinto il primo 6-4, ma Sabalenka ha reagito chiudendo il secondo 7-5. Nel set decisivo la nuova campionessa ha costruito rapidamente il vantaggio e lo ha difeso fino al 6-2.",
"Il risultato ha un peso doppio. Rybakina conquista il terzo titolo Major della carriera e raggiunge per la prima volta la vetta del ranking mondiale. Sabalenka, invece, perde la possibilità di vincere il torneo per il terzo anno consecutivo e cede proprio alla rivale che la sostituirà al primo posto.",
"La classifica non cambia per effetto di una singola partita isolata. Il ranking WTA somma i punti ottenuti nei tornei validi durante un periodo mobile di 52 settimane: quando entra un nuovo risultato, escono o vengono sostituiti i punti dell'edizione precedente. Il titolo di New York completa quindi un percorso costruito lungo l'intera stagione.",
"Il punteggio mostra anche dove si è deciso l'incontro. Nei primi due set le giocatrici sono rimaste abbastanza vicine da arrivare entrambe oltre il decimo game. Nel terzo, il margine di quattro giochi segnala una separazione più netta, ma non basta da solo a spiegare servizio, risposta e pressione nei punti decisivi.",
"Per Sabalenka resta un torneo di vertice, concluso soltanto in finale. La definizione di “detentrice del titolo” riguarda il risultato dell'anno precedente; non attribuisce un vantaggio nel tabellone successivo. Ogni edizione assegna nuovamente punti e trofeo attraverso il percorso disputato nelle due settimane.",
"Rybakina aggiunge così New York ai precedenti successi nei tornei Major e apre una nuova fase della stagione da prima giocatrice del mondo. I prossimi eventi diranno quanto a lungo conserverà la posizione: il primato dipenderà dai punti da difendere, dai risultati delle inseguitrici e dal calendario effettivamente disputato."
]
sources = [
("https://www.usopen.org/en_US/news/articles/2026-09-12/rybakina_defeats_twotime_defending_champion_sabalenka_to_win_2026_us_open.html", "US Open — 12 settembre 2026 — risultato ufficiale della finale e primo titolo di Rybakina a New York"),
("https://www.reuters.com/sports/tennis/ruthless-rybakina-dethrones-sabalenka-capture-first-us-open-crown-2026-09-12/", "Reuters — 12 settembre 2026 — cronaca della finale e conseguenze sul vertice del tennis femminile"),
("https://www.bbc.com/sport/tennis/articles/", "BBC Sport — 12 settembre 2026 — conferma indipendente del risultato e del nuovo numero uno"),
("https://www.ansa.it/sito/notizie/topnews/2026/09/13/us-open-rybakina-batte-sabalenka-in-tre-set-e-vince-il-titolo_c2da1738-ef75-4f5b-85a8-8b62edab931c.html", "ANSA — 13 settembre 2026 — punteggio, terzo titolo Major e nuova posizione nel ranking WTA")
]

src = ROOT / "generated_images/exec-b6725b9b-7b05-4aa4-87c8-deb4a5a5c5ed.png"
outdir = ROOT / "assets/images/editorial-auto"; outdir.mkdir(parents=True, exist_ok=True)
im = Image.open(src).convert("RGB")
for w in (480, 800, 1200):
    h = round(w * 2 / 3)
    resized = im.resize((w, h), Image.Resampling.LANCZOS)
    resized.save(outdir / f"{KEY}-{w}.webp", "WEBP", quality=86, method=6)

canonical = f"https://curiomondo.it/notizie/{SLUG}.html"
image = f"https://curiomondo.it/assets/images/editorial-auto/{KEY}-1200.webp"
schema = {"@context":"https://schema.org","@type":"NewsArticle","headline":TITLE,"description":EXCERPT,"datePublished":PUBLISHED,"dateModified":PUBLISHED,"mainEntityOfPage":canonical,"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo","url":"https://curiomondo.it/pagine/redazione.html"},"publisher":{"@type":"Organization","name":"CurioMondo"},"image":[image]}
paras = ''.join(f'<p>{escape(p)}</p>' for p in body)
source_html = ''.join(f'<li><a href="{escape(u, quote=True)}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>' for u,label in sources)
page = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(TITLE)} | CurioMondo</title><meta name="description" content="{escape(EXCERPT,quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(TITLE,quote=True)}"><meta property="og:description" content="{escape(EXCERPT,quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{escape(IMAGE_ALT,quote=True)}"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=343"><link rel="stylesheet" href="../assets/css/editorial-trust-v263.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{SLUG}"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo">←</a><a class="cm-global-header__brand" href="/">Curio<span>Mondo</span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura">☾</button></nav></header><main class="wrap"><div class="badge">Sport / Tennis / US Open</div><h1>{escape(TITLE)}</h1><p class="subtitle">{escape(EXCERPT)}</p><div class="meta">13 settembre 2026 · New York · <span id="readTime">3 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html" rel="author">Redazione CurioMondo</a> · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></p><figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false"><picture><img src="../assets/images/editorial-auto/{KEY}-800.webp" srcset="../assets/images/editorial-auto/{KEY}-480.webp 480w, ../assets/images/editorial-auto/{KEY}-800.webp 800w, ../assets/images/editorial-auto/{KEY}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(IMAGE_ALT,quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid"><div><b>6-4 5-7 6-2</b><small>il punteggio della finale</small></div><div><b>3</b><small>i titoli Major di Rybakina</small></div><div><b>n. 1</b><small>la posizione WTA da lunedì</small></div></div></section><article class="art-body" data-editorial-protocol="4.0" data-article-format="standard">{paras}</article><section class="curio-related" aria-labelledby="related-title"><h2 id="related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid"><a href="/notizie/"><small>Archivio</small><strong>Tutte le notizie sportive</strong></a><a href="/categorie/sport.html"><small>Sport</small><strong>Risultati e approfondimenti</strong></a></div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{source_html}</ul><p><small><strong>Redazione CurioMondo · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></strong><br>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 13 settembre 2026, ore 01:10.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../notizie/">Archivio</a></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=344" defer></script></body></html>'''
(ROOT / "notizie" / f"{SLUG}.html").write_text(page, encoding="utf-8")

reg_path = ROOT / "assets/data/editorial-images-v210.json"
reg = json.loads(reg_path.read_text(encoding="utf-8"))
variants=[]
for w in (480,800,1200):
    f=outdir/f"{KEY}-{w}.webp"
    variants.append({"w":w,"src":f"/assets/images/editorial-auto/{f.name}","sha256":hashlib.sha256(f.read_bytes()).hexdigest(),"bytes":f.stat().st_size})
reg["items"]=[i for i in reg["items"] if i.get("key") != KEY]
reg["items"].append({"key":KEY,"article":f"/notizie/{SLUG}.html","alt":IMAGE_ALT,"generator":"OpenAI / ChatGPT image generation","syntheticLikeness":"public-figure","sensitiveContext":False,"variants":variants})
reg_path.write_text(json.dumps(reg,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(SLUG)
