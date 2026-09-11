from pathlib import Path
import json
import re
import html

TODAY = "2026-09-11"
DATE_LABEL = "11 settembre 2026"
NUMBER = 88
QUESTION = "La consapevolezza della morte ci rende più buoni o soltanto più precipitosi?"
SLUG = "la-consapevolezza-della-morte-ci-rende-piu-buoni-o-soltanto-piu-precipitosi"
URL = f"/domanda-del-giorno/{SLUG}/"
EXCERPT = "Una riflessione su ciò che cambia quando ricordiamo che il tempo è limitato: priorità, urgenza, cura degli altri e rischio di confondere intensità con fretta."

manifest_path = Path("curiomondo-site-manifest.json")
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
state = manifest.setdefault("daily_state", {})
if state.get("last_question_date") == TODAY:
    print("Domanda del giorno già aggiornata: nessuna modifica necessaria.")
    raise SystemExit(0)
used = list(state.get("used_question_source_numbers", []))
if NUMBER in used:
    raise SystemExit(f"Numero {NUMBER} già usato: blocco fail-closed.")

page = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{html.escape(QUESTION)} | CurioMondo</title><meta name="description" content="Domanda del giorno dell’11 settembre 2026: {html.escape(EXCERPT)}"><meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#f5f9ff"><link rel="canonical" href="https://curiomondo.it{URL}"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="/assets/css/site-base-v210.css"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=308"><link rel="stylesheet" href="/assets/css/daily-question-v273.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body class="cm-daily-page"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="cm-q-page"><section class="cm-q-hero" aria-labelledby="question-title"><div class="cm-q-topline"><span class="cm-q-badge">Domanda del giorno</span><time class="cm-q-date" datetime="{TODAY}">{DATE_LABEL}</time></div><p class="cm-q-eyebrow">Uno spazio per fermarsi e pensare.</p><h1 id="question-title">{html.escape(QUESTION)}</h1><p class="cm-q-meta"><span>3 min di lettura</span><span class="cm-q-dot" aria-hidden="true"></span><span>CurioMondo</span></p></section><article class="q-flow cm-daily-flow" aria-label="Risposta alla Domanda del giorno"><p>Ricordare che la vita finisce non produce automaticamente una persona migliore. Può renderci più attenti, ma può anche spingerci a voler recuperare tutto insieme. La stessa consapevolezza che invita a chiedere scusa può alimentare l’ansia di non perdere un’occasione, trasformando una priorità autentica in una corsa.</p><p>Essere più buoni, in questo senso, non significa diventare improvvisamente più gentili perché il tempo è poco. Significa forse attribuire un peso diverso alle conseguenze delle nostre azioni. Se una giornata non è infinita, anche il modo in cui trattiamo chi la attraversa con noi acquista importanza: una parola evitabile, un rancore mantenuto per abitudine o un gesto di cura rimandato non occupano più uno spazio astratto.</p><p>Ma la finitezza può produrre l’effetto opposto. Sapere che non avremo tempo per tutto può farci scegliere in fretta relazioni, lavori, viaggi o decisioni che richiederebbero invece lucidità. L’urgenza diventa problematica quando la domanda smette di essere «che cosa conta?» e diventa «che cosa posso ancora accumulare?». Una vita più intensa non coincide necessariamente con una vita più piena.</p><p>La consapevolezza della morte può funzionare come una luce laterale: non cambia gli oggetti nella stanza, ma rende più visibili alcune forme che prima ignoravamo. Può mostrarci quali conflitti hanno ancora un significato, quali ambizioni appartengono davvero a noi e quali persone continuiamo a dare per scontate. Quella luce, però, non decide al posto nostro.</p><p>C’è anche una differenza tra fretta e decisione. La fretta vuole eliminare l’incertezza il prima possibile; una decisione matura può riconoscere che il tempo è limitato senza fingere di sapere già tutto. Possiamo smettere di rimandare una conversazione e, nello stesso tempo, non prendere una scelta irreversibile soltanto perché abbiamo paura di arrivare tardi.</p><p>Forse la misura più interessante non è quanto la morte ci renda migliori, ma che cosa rivela delle nostre priorità. Se il pensiero della fine ci rende più presenti, più capaci di distinguere il necessario dal rumore e più responsabili verso gli altri, allora può cambiare il modo in cui viviamo. Se ci costringe soltanto ad accelerare, rischia invece di sottrarci proprio l’attenzione che volevamo salvare.</p><p class="q-pull cm-daily-question">Se sapessi con certezza che il tuo tempo è più breve di quanto immagini, che cosa rallenteresti invece di accelerare?</p><p>Oggi la domanda resta concreta: non quanto tempo abbiamo in assoluto, ma a che cosa stiamo scegliendo di dare il tempo che abbiamo davanti.</p></article></main><footer class="cm-q-footer" aria-label="Collegamenti informativi"><a href="/pagine/privacy.html">Privacy</a><a href="/pagine/chi-siamo.html">Chi siamo</a></footer><script src="/assets/js/site-common-v210.js" defer></script></body></html>'''
page_path = Path("domanda-del-giorno") / SLUG / "index.html"
page_path.parent.mkdir(parents=True, exist_ok=True)
page_path.write_text(page, encoding="utf-8")

home_path = Path("index.html")
home = home_path.read_text(encoding="utf-8")
new_card = f'''<section class="cm-qday" aria-label="Domanda del giorno">\n<a aria-label="Scopri la Domanda del giorno del {DATE_LABEL}" class="cm-qday-link" href="{URL}">\n<div class="cm-qday-card">\n<time class="cm-qday-date" datetime="{TODAY}"><strong>11</strong><span>SET · 2026</span></time>\n<span class="cm-qday-k">Domanda del giorno</span>\n<span class="cm-qday-cta">Scopri <i aria-hidden="true">→</i></span>\n</div>\n</a>\n</section>'''
home2, n = re.subn(r'<section class="cm-qday" aria-label="Domanda del giorno">.*?</section>', new_card, home, count=1, flags=re.S)
if n != 1:
    raise SystemExit("Card Domanda del giorno non trovata in homepage: blocco fail-closed.")
home_path.write_text(home2, encoding="utf-8")

archive_path = Path("domanda-del-giorno/index.html")
archive = archive_path.read_text(encoding="utf-8")
card = f'<a class="cb-subcard" href="{URL}"><span class="cb-kicker">{DATE_LABEL}</span><h2>{html.escape(QUESTION)}</h2><p>{html.escape(EXCERPT)}</p><b>Leggi →</b></a>'
marker = '<section class="cb-subgrid">'
if marker not in archive:
    raise SystemExit("Archivio Domanda del giorno non riconosciuto: blocco fail-closed.")
archive_path.write_text(archive.replace(marker, marker + card, 1), encoding="utf-8")

search_path = Path("assets/data/search-index-v210.json")
search = json.loads(search_path.read_text(encoding="utf-8"))
items = [x for x in search.get("items", []) if x.get("url") != URL]
items.insert(0, {"title": QUESTION, "excerpt": EXCERPT, "url": URL, "section": "Domanda del giorno"})
search["items"] = items
search["version"] = max(int(search.get("version", 0)), 318)
search_path.write_text(json.dumps(search, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

sitemap_path = Path("sitemap.xml")
sitemap = sitemap_path.read_text(encoding="utf-8")
full_url = "https://curiomondo.it" + URL
if full_url not in sitemap:
    entry = f"  <url>\n    <loc>{full_url}</loc>\n    <lastmod>{TODAY}</lastmod>\n  </url>\n"
    sitemap = re.sub(r'(<urlset[^>]*>\s*)', lambda m: m.group(1) + entry, sitemap, count=1)
sitemap_path.write_text(sitemap, encoding="utf-8")

used.append(NUMBER)
state["current_question_source_number"] = NUMBER
state["used_question_source_numbers"] = used
state["last_question_date"] = TODAY
state["last_question_slug"] = SLUG
manifest.setdefault("site", {})["current_site_version"] = max(int(manifest.get("site", {}).get("current_site_version", 0)), 318)
manifest["site"]["site_version"] = max(int(manifest["site"].get("site_version", 0)), 318)
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

assert QUESTION in page_path.read_text(encoding="utf-8")
assert f'datetime="{TODAY}"' in home_path.read_text(encoding="utf-8")
assert full_url in sitemap_path.read_text(encoding="utf-8")
assert json.loads(manifest_path.read_text(encoding="utf-8"))["daily_state"]["last_question_date"] == TODAY
print("Daily question files prepared.")
