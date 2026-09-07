#!/usr/bin/env python3
from pathlib import Path
from html import escape
import hashlib, json, re, runpy

ROOT = Path(__file__).resolve().parents[1]
VERSION = 301
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

articles = [
    {
        "slug": "toscana-bando-15-milioni-economia-circolare-rifiuti-7-settembre-2026",
        "title": "Toscana, apre il bando da 15 milioni per trasformare i rifiuti in risorse",
        "excerpt": "Dalle 9 del 7 settembre le imprese possono chiedere contributi per impianti di recupero e riciclo. Le domande restano aperte fino alle 12 del 23 ottobre 2026.",
        "section": "Italia / Toscana / Ambiente / Economia circolare",
        "published": "2026-09-07T07:52:00+02:00",
        "key": "toscana-economia-circolare-bando-rifiuti-7-settembre-2026-ai-v301",
        "alt": "Impianto moderno di selezione e recupero dei rifiuti inserito nel paesaggio toscano, illustrazione editoriale fotorealistica generata con IA",
        "insights": [("15 milioni €", "la dotazione complessiva del bando"), ("7 settembre", "l’apertura delle domande alle ore 9"), ("23 ottobre", "la chiusura alle ore 12")],
        "body": [
            "Da questa mattina le imprese possono presentare domanda per il nuovo bando della Regione Toscana dedicato all’economia circolare. Lo sportello è aperto dalle ore 9 del 7 settembre 2026 e chiuderà alle ore 12 del 23 ottobre. La misura dispone di 15 milioni di euro del Programma regionale FESR 2021-2027 e finanzia progetti capaci di aumentare il recupero e il riciclo dei rifiuti, riducendo la quantità destinata allo smaltimento.",
            "Il bando era stato annunciato il 25 agosto e si rivolge alle imprese private che operano nel trattamento, nel recupero e nel riciclo. Gli interventi possono riguardare la realizzazione di nuovi impianti oppure il potenziamento di strutture già esistenti. Non si tratta quindi di un incentivo rivolto ai singoli cittadini: la domanda deve essere collegata a un progetto industriale ammissibile e presentata attraverso i canali indicati nel portale ufficiale regionale.",
            "Il contributo è definito “in conto capitale”. In parole semplici, è un aiuto pubblico destinato a coprire una parte delle spese di investimento — per esempio macchinari, linee di selezione o attrezzature — e non un prestito da restituire con interessi. L’importo effettivamente riconosciuto dipenderà dalle regole del bando, dai costi considerati ammissibili e dalla valutazione del progetto: la dotazione di 15 milioni non è la somma assegnata automaticamente a ciascuna impresa.",
            "L’obiettivo è far rientrare nel ciclo produttivo materiali che altrimenti verrebbero eliminati. Recupero, riciclo e smaltimento non sono sinonimi. Il recupero comprende le operazioni che permettono di ottenere una nuova utilità da un rifiuto; il riciclo lo trasforma in materiali o prodotti da usare di nuovo; lo smaltimento è invece la fase finale, come il conferimento in discarica, quando il valore del materiale non viene più recuperato. Spostare volumi dallo smaltimento al recupero significa conservare materie prime più a lungo e diminuire la pressione sugli impianti finali.",
            "La Regione collega la misura alla chiusura delle filiere: il materiale raccolto deve trovare una lavorazione e, successivamente, un mercato in cui essere riutilizzato. Un impianto più efficiente può separare meglio le diverse frazioni, ridurre gli scarti o trattare materiali che oggi vengono inviati lontano. Il risultato ambientale, tuttavia, non dipende soltanto dalla presenza di nuovi macchinari; conta anche la qualità della raccolta, la domanda di materia riciclata e la capacità di dimostrare dove finiscono i materiali recuperati.",
            "Il programma si inserisce nel percorso europeo che punta, entro il 2035, a riciclare effettivamente almeno il 65% dei rifiuti urbani e a contenere sotto il 10% la quota collocata in discarica. Questi valori sono obiettivi generali e non costituiscono il risultato già prodotto dal bando toscano. Gli effetti della misura potranno essere misurati solo dopo la selezione dei progetti, la realizzazione degli impianti e la verifica delle quantità realmente recuperate.",
            "Per le imprese interessate, la data da non confondere è quella del 23 ottobre 2026: il termine è fissato alle ore 12, non alla fine della giornata. Prima dell’invio è utile controllare sul portale regionale requisiti del beneficiario, spese ammissibili, documenti tecnici, modalità di firma e criteri di valutazione. L’apertura dello sportello non garantisce l’ammissione e una sintesi giornalistica non sostituisce il testo ufficiale del bando e i suoi eventuali aggiornamenti.",
            "La notizia verificata è dunque l’avvio operativo di una misura già annunciata: da oggi è possibile presentare le domande. I prossimi dati rilevanti saranno il numero dei progetti ricevuti, la graduatoria, gli investimenti attivati e la capacità aggiuntiva di recupero. Sono questi indicatori, più della sola dotazione iniziale, che permetteranno di capire quanto il programma avrà trasformato rifiuti in risorse utilizzabili.",
        ],
        "evergreen_title": "Economia circolare: il valore nasce quando il materiale torna davvero in uso",
        "evergreen_text": "Raccogliere separatamente è solo il primo passaggio. Un ciclo si chiude quando selezione, trattamento e mercato consentono alla materia recuperata di sostituire nuove risorse.",
        "sources": [
            ("https://www.regione.toscana.it/it/-/economia-circolare-il-bando-per-trasformare-i-rifiuti-in-risorse", "Regione Toscana — comunicazione ufficiale e calendario del bando"),
            ("https://www.regione.toscana.it/it/-/contributi-per-la-realizzazione-e-potenziamento-di-impianti-di-trattamento.dei-rifiuti-per-il-loro-recupero", "Regione Toscana — scheda ufficiale del bando Economia circolare"),
            ("https://www.regione.toscana.it/pr-fesr-2021-2027/bandi-aperti", "Regione Toscana — portale ufficiale dei bandi aperti del PR FESR 2021-2027"),
            ("https://environment.ec.europa.eu/topics/waste-and-recycling/landfill-waste_en", "Commissione europea — obiettivi UE sulla riduzione dei rifiuti in discarica"),
        ],
        "related": [
            ("/notizie/plastic-overshoot-day-6-settembre-2026.html", "Ambiente", "Plastic Overshoot Day: il peso dei rifiuti di plastica"),
            ("/categorie/ambiente/", "Categoria", "Tutte le notizie su ambiente e sostenibilità"),
            ("/notizie/", "Archivio", "Le ultime notizie verificate da CurioMondo"),
        ],
        "prompt": "Ultra-realistic wide editorial photograph-style scene of a modern indoor recycling and materials recovery facility in Tuscany, clean conveyor systems sorting paper plastic and metal, two adult technicians in safety equipment inspecting the line, subtle Tuscan hills visible through large windows, natural morning light, credible industrial details, no logos, no readable text, no watermark, no dumping, no disaster imagery."
    },
    {
        "slug": "australia-un-milione-donne-farmaci-piu-economici-7-settembre-2026",
        "title": "Australia, oltre un milione di donne accede a farmaci più economici",
        "excerpt": "Il governo attribuisce al pacchetto federale per la salute femminile oltre quattro milioni di prescrizioni agevolate e risparmi superiori a 150 milioni di dollari australiani.",
        "section": "Mondo / Australia / Salute",
        "published": "2026-09-07T07:50:00+02:00",
        "key": "australia-farmaci-donne-pbs-7-settembre-2026-ai-v301",
        "alt": "Farmacista in una moderna farmacia australiana assiste diverse donne adulte, illustrazione editoriale fotorealistica generata con IA",
        "insights": [("oltre 1 milione", "le donne raggiunte dalle misure"), ("oltre 4 milioni", "le prescrizioni agevolate da marzo 2025"), (">150 milioni A$", "i risparmi dichiarati dal governo")],
        "body": [
            "Più di un milione di donne in Australia ha ottenuto medicinali a costo ridotto per contraccezione, endometriosi e menopausa. Lo ha comunicato il governo federale il 7 settembre 2026, facendo il punto sul Women’s Health Package da quasi 800 milioni di dollari australiani. Secondo i dati ufficiali, da marzo 2025 sono state dispensate oltre quattro milioni di prescrizioni agevolate, con un risparmio complessivo dichiarato superiore a 150 milioni di dollari.",
            "La riduzione passa soprattutto dal Pharmaceutical Benefits Scheme, abbreviato PBS. È il programma pubblico australiano che sovvenziona i medicinali inclusi nel suo elenco: il governo copre una parte del prezzo e il paziente paga una quota massima prevista. Dal 1° gennaio 2026 il costo generale di una prescrizione PBS è stato limitato a 25 dollari australiani; per chi possiede i requisiti di concessione la quota indicata dal governo è 7,70 dollari. Non significa che ogni farmaco in farmacia abbia quel prezzo: il beneficio riguarda i prodotti e le condizioni compresi nel programma.",
            "Per la contraccezione, la comunicazione ufficiale parla di oltre 400.000 donne che hanno risparmiato complessivamente circa 55 milioni di dollari attraverso 1,27 milioni di prescrizioni. L’ampliamento delle opzioni sovvenzionate mira a rendere più accessibile una scelta terapeutica adatta alla singola persona. Prescrizione, benefici e possibili effetti indesiderati restano comunque materia da discutere con un professionista sanitario.",
            "Sul fronte della menopausa, più di 520.000 donne avrebbero risparmiato circa 110 milioni di dollari grazie a tre milioni di prescrizioni per terapie ormonali inserite nel PBS. Il governo riferisce inoltre oltre 137.000 valutazioni sanitarie dedicate a menopausa e perimenopausa. Quest’ultima è la fase di transizione che precede la menopausa e può iniziare anni prima dell’ultima mestruazione, con sintomi e necessità molto diversi da persona a persona.",
            "Per l’endometriosi, oltre 11.000 pazienti avrebbero ottenuto un risparmio totale di 11,7 milioni di dollari attraverso circa 600.000 prescrizioni agevolate. L’endometriosi è una malattia cronica in cui tessuto simile al rivestimento interno dell’utero cresce in altre aree, provocando in alcuni casi dolore, infiammazione e difficoltà riproduttive. La disponibilità di un medicinale più economico amplia l’accesso, ma non elimina la necessità di diagnosi, controlli e percorsi personalizzati.",
            "I numeri delle singole aree non vanno sommati per calcolare quante donne uniche abbiano beneficiato del programma: una stessa persona può aver ricevuto più prescrizioni o rientrare in più gruppi. Anche il totale delle ricette misura le dispensazioni, non il numero di pazienti. Il dato “oltre un milione” pubblicato dal governo è quindi l’indicatore da usare per le beneficiarie, mentre gli oltre quattro milioni descrivono il volume delle prescrizioni agevolate.",
            "Il pacchetto non riguarda soltanto i prezzi in farmacia. Il governo segnala una rete di 33 Endometriosis and Pelvic Pain Clinics e altre misure per diagnosi, consulti e cure. Nella conferenza stampa diffusa lo stesso giorno, l’Assistant Minister for Health Rebecca White ha collegato la riduzione dei costi alla possibilità di scegliere trattamenti che in passato potevano risultare troppo onerosi. Si tratta di una conferma istituzionale distinta, ma proveniente dallo stesso esecutivo che ha prodotto i dati.",
            "Le cifre sono ufficiali e descrivono l’attuazione del programma fino al momento del comunicato; non equivalgono da sole a una valutazione indipendente degli esiti clinici. Per misurare l’impatto sanitario serviranno dati su continuità delle cure, diagnosi, qualità della vita e differenze di accesso tra aree urbane, rurali e comunità remote. Il risultato documentato oggi è economico e operativo: più farmaci sovvenzionati, milioni di prescrizioni e minori spese dichiarate per oltre un milione di donne.",
        ],
        "evergreen_title": "PBS: una sovvenzione pubblica riduce il prezzo, non sostituisce la prescrizione",
        "evergreen_text": "Il Pharmaceutical Benefits Scheme negozia e sostiene il costo dei medicinali ammessi. L’idoneità clinica e la scelta del trattamento restano affidate al confronto tra paziente e professionista sanitario.",
        "sources": [
            ("https://www.health.gov.au/ministers/the-hon-mark-butler-mp/media/more-choice-lower-costs-for-one-million-women?language=en", "Australian Government Department of Health — comunicato del 7 settembre 2026"),
            ("https://www.health.gov.au/ministers/the-hon-rebecca-white-mp/media/press-conference-with-assistant-minister-white-canberra-7-september-2026?language=en", "Australian Government Department of Health — conferenza stampa del 7 settembre 2026"),
            ("https://www.pbs.gov.au/info/about-the-pbs", "Pharmaceutical Benefits Scheme — guida ufficiale al programma"),
            ("https://www.health.gov.au/our-work/womens-health-package", "Australian Government Department of Health — Women’s Health Package"),
        ],
        "related": [
            ("/categorie/scienza/", "Salute", "Notizie su salute, ricerca e scienza"),
            ("/categorie/mondo/", "Mondo", "Le ultime notizie internazionali"),
            ("/notizie/", "Archivio", "Le ultime notizie verificate da CurioMondo"),
        ],
        "prompt": "Ultra-realistic wide editorial photograph-style scene inside a contemporary Australian community pharmacy, an adult female pharmacist professionally assisting a diverse group of adult women of different ages, discreet medicine packages with no readable labels, bright natural daylight, authentic Australian pharmacy atmosphere, respectful health context, no logos, no readable text, no watermark, no medical procedure."
    },
]

def page(a):
    canonical = f"https://curiomondo.it/notizie/{a['slug']}.html"
    image = f"https://curiomondo.it/assets/images/editorial-auto/{a['key']}-1200.webp"
    schema = {"@context":"https://schema.org","@type":"NewsArticle","headline":a["title"],"description":a["excerpt"],"datePublished":a["published"],"dateModified":a["published"],"mainEntityOfPage":canonical,"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo","url":"https://curiomondo.it/pagine/redazione.html"},"publisher":{"@type":"Organization","name":"CurioMondo","logo":{"@type":"ImageObject","url":"https://curiomondo.it/curiomondo-logo-512.png"}},"image":[image]}
    insights = "".join(f'<div><b>{escape(x)}</b><small>{escape(y)}</small></div>' for x,y in a["insights"])
    related = "".join(f'<a href="{u}"><small>{escape(k)}</small><strong>{escape(t)}</strong></a>' for u,k,t in a["related"])
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(t)}</a></li>' for u,t in a["sources"])
    tm = a["published"][11:16]
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(a['title'])} | CurioMondo</title><meta name="description" content="{escape(a['excerpt'],quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(a['title'],quote=True)}"><meta property="og:description" content="{escape(a['excerpt'],quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{escape(a['alt'],quote=True)}"><meta name="theme-color" content="#eaf8ff"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=301"><link rel="stylesheet" href="../assets/css/editorial-trust-v263.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{a['slug']}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="wrap"><div class="badge">{escape(a['section'])}</div><h1>{escape(a['title'])}</h1><p class="subtitle">{escape(a['excerpt'])}</p><div class="meta">7 settembre 2026 · aggiornato alle {tm} · {escape(a['section'])} · <span id="readTime">5 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html" rel="author">Redazione CurioMondo</a> · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></p><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-sensitive-context="false" data-portrait-format="contextual-editorial-scene"><picture><img src="../assets/images/editorial-auto/{a['key']}-800.webp" srcset="../assets/images/editorial-auto/{a['key']}-480.webp 480w, ../assets/images/editorial-auto/{a['key']}-800.webp 800w, ../assets/images/editorial-auto/{a['key']}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(a['alt'],quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{insights}</div></section><article class="art-body" data-length-policy="3000-7000">{''.join(f'<p>{escape(x)}</p>' for x in a['body'])}</article><section class="cm-evergreen-reader"><small>Da conservare</small><h2>{escape(a['evergreen_title'])}</h2><p>{escape(a['evergreen_text'])}</p></section><section class="curio-related" aria-labelledby="rel-{a['slug']}"><h2 id="rel-{a['slug']}">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 7 settembre 2026, ore {tm} italiane.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=301" defer></script></body></html>'''

for article in articles:
    (ROOT / "notizie" / f"{article['slug']}.html").write_text(page(article), encoding="utf-8")

registry_path = ROOT / "assets/data/editorial-images-v210.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
for article in reversed(articles):
    registry["items"] = [item for item in registry["items"] if item.get("key") != article["key"]]
    variants = []
    for width in (480, 800, 1200):
        file_path = ROOT / "assets/images/editorial-auto" / f"{article['key']}-{width}.webp"
        variants.append({"w":width,"src":f"/assets/images/editorial-auto/{file_path.name}","sha256":hashlib.sha256(file_path.read_bytes()).hexdigest(),"bytes":file_path.stat().st_size})
    registry["items"].insert(0, {"key":article["key"],"article":f"/notizie/{article['slug']}.html","aiGenerated":True,"sensitiveContext":False,"documentaryPhoto":False,"prompt":article["prompt"],"variants":variants,"alt":article["alt"],"disclosure":CAPTION,"portraitOnly":False,"portraitFormat":"contextual-editorial-scene","reenactedEvent":False})
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

runpy.run_path(str(ROOT / "tools/finalize_articles_20260906.py"), run_name="__main__")
for rel in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json", "assets/data/editorial-images-v210.json"):
    path = ROOT / rel
    data = json.loads(path.read_text(encoding="utf-8")); data["version"] = VERSION
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

category_tool = ROOT / "tools/generate_category_pages.py"
category_text = category_tool.read_text(encoding="utf-8").replace('"alluvione", "vulcani"', '"alluvione", "vulcani", "economia circolare", "rifiuti", "riciclo"')
category_tool.write_text(category_text, encoding="utf-8")
runpy.run_path(str(category_tool), run_name="__main__")

index_path = ROOT / "index.html"
index_text = re.sub(r'home-bundle-v291\.css\?v=\d+', f'home-bundle-v291.css?v={VERSION}', index_path.read_text(encoding="utf-8"))
index_path.write_text(index_text, encoding="utf-8")

manifest_path = ROOT / "curiomondo-site-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["site"]["current_site_version"] = VERSION; manifest["site"]["site_version"] = VERSION
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status":"ok","version":VERSION,"articles":[f"/notizie/{a['slug']}.html" for a in articles]}, ensure_ascii=False))
