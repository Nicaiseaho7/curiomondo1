#!/usr/bin/env python3
from pathlib import Path
from html import escape
import hashlib, json, re, runpy

ROOT = Path(__file__).resolve().parents[1]
VERSION = 297
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

articles = [
    {
        "slug": "ucraina-zelenskyy-riavviare-negoziati-inviati-usa-7-settembre-2026",
        "title": "Ucraina, Zelenskyy: riavviare i negoziati dopo l’incontro con gli inviati USA",
        "excerpt": "Dopo i colloqui a Kyiv con Steve Witkoff e Jared Kushner, il presidente ucraino considera importante riprendere il processo diplomatico. Sul tavolo sicurezza, territori, ricostruzione e sostegno invernale.",
        "section": "Mondo / Ucraina / Diplomazia",
        "published": "2026-09-07T06:01:00+02:00",
        "key": "zelensky-witkoff-kushner-negoziati-7-settembre-2026-ai-v297",
        "alt": "Scena editoriale contestuale generata con IA di Volodymyr Zelenskyy a colloquio con Steve Witkoff e Jared Kushner in una sala istituzionale a Kyiv",
        "insights": [("3 incontri", "i cicli di colloqui svolti a Kyiv"), ("00:24", "l’ora della comunicazione ufficiale"), ("3 parti", "Ucraina, Stati Uniti ed Europa al prossimo confronto")],
        "body": [
            "Volodymyr Zelenskyy ha indicato come importante il riavvio del processo negoziale per porre fine alla guerra, dopo l’incontro a Kyiv con gli inviati del presidente degli Stati Uniti Steve Witkoff e Jared Kushner. La Presidenza ucraina ha pubblicato la comunicazione alle 00:24 del 7 settembre 2026, al termine di una giornata di colloqui diplomatici.",
            "Il presidente ucraino ha sostenuto che i negoziati sono utili in qualsiasi formato capace di produrre passi concreti. Ha riconosciuto il ruolo dei due inviati statunitensi nel tentativo di riattivare un confronto rimasto fermo a lungo. La dichiarazione esprime una disponibilità politica, ma non annuncia ancora una nuova sessione con data e sede già concordate.",
            "Witkoff e Kushner erano arrivati a Kyiv dopo il colloquio avuto a Mosca con il presidente russo Vladimir Putin. Secondo il resoconto ucraino, la delegazione americana ha discusso con Zelenskyy le possibilità per riprendere il processo. Reuters riferisce che gli inviati sperano nell’annuncio in tempi brevi di un nuovo ciclo di colloqui mediati dagli Stati Uniti, senza indicare però un risultato definitivo.",
            "A Kyiv si sono svolti tre momenti di confronto. Il primo ha coinvolto Zelenskyy e gli inviati statunitensi; il secondo ha riunito le delegazioni ucraina e americana; al terzo hanno partecipato anche consiglieri per la sicurezza nazionale di Francia, Regno Unito e Germania. Le parti hanno concordato di lavorare a un prossimo incontro tra Ucraina, Europa e Stati Uniti, senza fissarne pubblicamente il luogo.",
            "Tra i temi affrontati figurano le garanzie di sicurezza per l’Ucraina, il futuro dell’esercito, la ricostruzione economica e un piano di prosperità per il dopoguerra. Zelenskyy ha ribadito che le garanzie dovranno impedire il ritorno del conflitto. Il contenuto concreto di queste misure resta da negoziare e non è stato presentato come un accordo già concluso.",
            "La questione territoriale rimane aperta. Il presidente ucraino ha sostenuto che i problemi più complessi su questo fronte possono essere risolti soltanto a livello di leader. Questa posizione segnala che il dossier non è stato escluso dai colloqui, ma non permette di dedurre concessioni o intese che le comunicazioni ufficiali non riportano.",
            "Una parte rilevante dell’incontro ha riguardato l’inverno. Kyiv chiede sostegno per la difesa aerea e per il sistema energetico, oltre alla possibilità di ricevere volumi consistenti di gas naturale liquefatto statunitense. Sono misure pensate per proteggere servizi e infrastrutture nel caso in cui la guerra continui, non elementi che dimostrano da soli un avvicinamento delle posizioni militari.",
            "Il passaggio diplomatico segue la disponibilità ucraina a sospendere temporaneamente gli attacchi contro Mosca durante i giorni dei colloqui, chiedendo alla Russia di fare lo stesso con Kyiv. La pausa riguarda gli attacchi aerei sulle capitali indicate e non equivale a un cessate il fuoco generale: i combattimenti lungo il fronte e gli attacchi in altre aree richiedono verifiche separate.",
            "Witkoff ha collegato il riavvio dei negoziati alla priorità attribuita dal presidente statunitense alla fine della guerra. Kushner ha parlato della costruzione di un quadro capace di condurre a una pace duratura e della possibilità di nuovi colloqui trilaterali. Sono dichiarazioni d’intento che dovranno tradursi in convocazioni, partecipanti e un’agenda condivisa.",
            "Il dato verificato oggi è quindi l’apertura ucraina a rimettere in moto il processo e il lavoro diplomatico avviato dagli inviati americani tra Mosca e Kyiv. Per parlare di svolta serviranno passaggi successivi: una nuova riunione formalmente annunciata, impegni verificabili e progressi sui nodi territoriali e di sicurezza. CurioMondo aggiornerà l’articolo quando questi elementi saranno pubblicati dalle parti."
        ],
        "evergreen_title": "Riavviare i negoziati non significa aver già raggiunto un accordo",
        "evergreen_text": "La ripresa di un processo diplomatico apre un canale e definisce possibili incontri. Un’intesa richiede invece partecipanti, agenda, impegni verificabili e decisioni accettate dalle parti.",
        "sources": [
            ("https://www.president.gov.ua/en/news/vidnovlennya-peregovornogo-procesu-ye-vazhlivim-i-ukrayina-v-106273", "Presidenza dell’Ucraina — comunicazione delle 00:24 del 7 settembre"),
            ("https://www.president.gov.ua/en/news/zayava-prezidenta-ukrayini-pid-chas-spilnogo-z-predstavnikam-106269", "Presidenza dell’Ucraina — conferenza stampa con gli inviati USA"),
            ("https://www.president.gov.ua/en/news/ukrayina-gotova-dotrimuvatisya-rezhimu-pripinennya-povitryan-106265", "Presidenza dell’Ucraina — comunicazione sulla sospensione temporanea degli attacchi alle capitali"),
            ("https://www.reuters.com/business/aerospace-defense/us-envoys-make-first-kyiv-visit-amid-ukraine-war-peace-push-2026-09-06/", "Reuters — conferma dei colloqui e dei temi discussi")
        ],
        "related": [
            ("/notizie/ucraina-tregua-aerea-72-ore-witkoff-kushner-kyiv-6-settembre-2026.html", "Diplomazia", "La pausa aerea durante la missione americana"),
            ("/notizie/papa-leone-angelus-ucraina-dialogo-diplomazia-6-settembre-2026.html", "Ucraina", "L’appello del Papa per dialogo e diplomazia"),
            ("/notizie/iran-economia-nuovi-attacchi-risposta-piu-dolorosa-6-settembre-2026.html", "Geopolitica", "Iran, economia e tensioni militari")
        ],
        "prompt": "Ultra-realistic contextual editorial scene of Ukrainian President Volodymyr Zelenskyy meeting U.S. envoys Steve Witkoff and Jared Kushner in Kyiv after diplomatic talks, recognizable real public figures, Ukrainian and U.S. flags naturally present, sober institutional lighting; no added headline, caption, watermark, fabricated document text or false claim that this is an authentic documentary photograph."
    },
    {
        "slug": "germania-afd-vince-sassonia-anhalt-43-8-7-settembre-2026",
        "title": "Germania, AfD vince in Sassonia-Anhalt con il 43,8%",
        "excerpt": "Il risultato provvisorio completo assegna all’AfD 39 seggi su 83, tre meno della maggioranza assoluta. La CDU scende al 17,2%; la formazione del governo resta incerta.",
        "section": "Mondo / Germania / Elezioni",
        "published": "2026-09-07T05:59:00+02:00",
        "key": "afd-sassonia-anhalt-vittoria-7-settembre-2026-ai-v297",
        "alt": "Scena editoriale contestuale generata con IA di Ulrich Siegmund sul palco elettorale dell’AfD in Sassonia-Anhalt dopo il risultato regionale",
        "insights": [("43,8%", "i voti di lista ottenuti dall’AfD"), ("39 su 83", "i seggi assegnati al partito"), ("42", "i seggi necessari per la maggioranza")],
        "body": [
            "Alternative für Deutschland ha vinto le elezioni regionali in Sassonia-Anhalt con il 43,8% dei voti di lista. Il risultato provvisorio completo della responsabile elettorale del Land assegna all’AfD 39 seggi su 83. Il partito diventa nettamente la prima forza politica regionale, ma resta tre seggi sotto la maggioranza assoluta di 42.",
            "Il dato rappresenta un salto rispetto al 2021, quando l’AfD aveva ottenuto il 20,8%. In cinque anni la percentuale è quindi più che raddoppiata. La vittoria ha una portata storica nel sistema politico tedesco, perché porta un partito di estrema destra vicino alla guida di un governo regionale per la prima volta dal secondo dopoguerra.",
            "La CDU, che governava il Land dal 2002, scende al 17,2% e ottiene 15 seggi. Nel 2021 aveva raggiunto il 37,1%. La distanza con l’AfD misura sia l’avanzata del partito guidato nel Land da Ulrich Siegmund sia il forte arretramento dei cristiano-democratici, che hanno riconosciuto la sconfitta.",
            "Nel nuovo parlamento regionale entrano anche SPD con il 9,3%, Verdi con l’8,9% e Linke con l’8,6%; ciascuna di queste forze ottiene otto seggi. Il BSW supera la soglia con il 5,3% e conquista cinque seggi. La composizione frammentata rende complessa la costruzione di una maggioranza alternativa.",
            "L’affluenza ha raggiunto il 76,5%, un livello record per il Land secondo i dati riportati dopo lo scrutinio. La partecipazione elevata rafforza il peso politico del risultato, ma non modifica le regole parlamentari: per eleggere il capo del governo servono i voti previsti dalla procedura del Landtag.",
            "Siegmund ha rivendicato un mandato a governare. Il risultato, tuttavia, non consegna automaticamente la presidenza regionale all’AfD. Gli altri principali partiti hanno escluso una coalizione con la formazione di estrema destra e la CDU ha ribadito il rifiuto di governare insieme all’AfD.",
            "Questa esclusione reciproca, spesso descritta in Germania come una barriera politica contro la cooperazione con l’AfD, lascia aperti diversi scenari. Potrebbero essere tentate alleanze molto ampie tra le altre forze, forme di sostegno esterno o soluzioni di minoranza. Nessuna di queste ipotesi risulta già definita dal solo esito elettorale.",
            "Il risultato del voto è distinto dalla formazione dell’esecutivo. Le elezioni determinano la distribuzione dei seggi; il Landtag deve poi eleggere il ministro-presidente. Un partito può arrivare primo e restare all’opposizione se non trova i numeri necessari, mentre più partiti possono costruire una maggioranza pur avendo singolarmente meno voti.",
            "L’AfD della Sassonia-Anhalt è classificata come estremista di destra dall’ufficio regionale per la protezione della Costituzione. Questa qualificazione fa parte del contesto politico e istituzionale in cui gli altri partiti motivano il rifiuto di collaborare. Non annulla il risultato elettorale né sostituisce le procedure previste per la costituzione del nuovo parlamento.",
            "Il dato ufficiale da conservare è il risultato provvisorio completo: 43,8%, 39 seggi e prima posizione per l’AfD; 17,2% e 15 seggi per la CDU. La domanda su chi governerà resta invece aperta. CurioMondo aggiornerà la pagina quando saranno formalizzati accordi, candidature alla presidenza del Land o decisioni del nuovo Landtag."
        ],
        "evergreen_title": "Vincere un’elezione non basta sempre per formare il governo",
        "evergreen_text": "Il primo partito ottiene più seggi degli altri, ma per governare deve raggiungere la maggioranza prevista, da solo o con alleati. Senza quei voti può restare all’opposizione.",
        "sources": [
            ("https://wahlergebnisse.sachsen-anhalt.de/wahlen/lt26/erg_land.html", "Landeswahlleiterin Sachsen-Anhalt — risultato provvisorio completo a livello regionale"),
            ("https://wahlen.sachsen-anhalt.de/", "Landeswahlleiterin Sachsen-Anhalt — portale ufficiale delle elezioni"),
            ("https://www.reuters.com/world/europe/far-right-afd-posts-historic-german-state-election-win-exit-polls-show-2026-09-06/", "Reuters — risultato e conseguenze politiche"),
            ("https://apnews.com/article/c538060710a2495c72425b6468df0d40", "Associated Press — seggi, maggioranza e quadro dei partiti")
        ],
        "related": [
            ("/notizie/sassonia-anhalt-voto-afd-favorita-urne-6-settembre-2026.html", "Elezioni", "La giornata del voto in Sassonia-Anhalt"),
            ("/approfondimenti/elezioni-land-germania-landtag-coalizioni-brandmauer.html", "Da conservare", "Come funzionano Landtag, coalizioni e maggioranze"),
            ("/notizie/ucraina-zelenskyy-riavviare-negoziati-inviati-usa-7-settembre-2026.html", "Europa", "Zelenskyy chiede di riavviare i negoziati")
        ],
        "prompt": "Ultra-realistic contextual editorial scene of real AfD lead candidate Ulrich Siegmund at an election-night podium in Magdeburg after the 2026 Saxony-Anhalt vote, accurate AfD branding and German and Saxony-Anhalt flags naturally present, press and supporters softly out of focus, sober stage lighting; no invented vote numbers, added headline, caption, watermark or false claim that this is an authentic documentary photograph."
    }
]

def page(a):
    canonical = f"https://curiomondo.it/notizie/{a['slug']}.html"
    image = f"https://curiomondo.it/assets/images/editorial-auto/{a['key']}-1200.webp"
    schema = {"@context":"https://schema.org","@type":"NewsArticle","headline":a["title"],"description":a["excerpt"],"datePublished":a["published"],"dateModified":a["published"],"mainEntityOfPage":canonical,"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo","url":"https://curiomondo.it/pagine/redazione.html"},"publisher":{"@type":"Organization","name":"CurioMondo","logo":{"@type":"ImageObject","url":"https://curiomondo.it/curiomondo-logo-512.png"}},"image":[image]}
    insights = "".join(f'<div><b>{escape(x)}</b><small>{escape(y)}</small></div>' for x,y in a["insights"])
    related = "".join(f'<a href="{u}"><small>{escape(k)}</small><strong>{escape(t)}</strong></a>' for u,k,t in a["related"])
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(t)}</a></li>' for u,t in a["sources"])
    tm = a["published"][11:16]
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(a['title'])} | CurioMondo</title><meta name="description" content="{escape(a['excerpt'],quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(a['title'],quote=True)}"><meta property="og:description" content="{escape(a['excerpt'],quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{escape(a['alt'],quote=True)}"><meta name="theme-color" content="#eaf8ff"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=297"><link rel="stylesheet" href="../assets/css/editorial-trust-v263.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{a['slug']}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="wrap"><div class="badge">{escape(a['section'])}</div><h1>{escape(a['title'])}</h1><p class="subtitle">{escape(a['excerpt'])}</p><div class="meta">7 settembre 2026 · aggiornato alle {tm} · {escape(a['section'])} · <span id="readTime">5 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html" rel="author">Redazione CurioMondo</a> · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></p><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-sensitive-context="false" data-portrait-format="contextual-editorial-scene"><picture><img src="../assets/images/editorial-auto/{a['key']}-800.webp" srcset="../assets/images/editorial-auto/{a['key']}-480.webp 480w, ../assets/images/editorial-auto/{a['key']}-800.webp 800w, ../assets/images/editorial-auto/{a['key']}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(a['alt'],quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{insights}</div></section><article class="art-body" data-length-policy="3000-7000">{''.join(f'<p>{escape(x)}</p>' for x in a['body'])}</article><section class="cm-evergreen-reader"><small>Da conservare</small><h2>{escape(a['evergreen_title'])}</h2><p>{escape(a['evergreen_text'])}</p></section><section class="curio-related" aria-labelledby="rel-{a['slug']}"><h2 id="rel-{a['slug']}">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 7 settembre 2026, ore {tm} italiane.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=297" defer></script></body></html>'''

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
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

index_path = ROOT / "index.html"
index_text = re.sub(r'home-bundle-v291\.css\?v=\d+', f'home-bundle-v291.css?v={VERSION}', index_path.read_text(encoding="utf-8"))
index_path.write_text(index_text, encoding="utf-8")

manifest_path = ROOT / "curiomondo-site-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
manifest["site"]["current_site_version"] = VERSION
manifest["site"]["site_version"] = VERSION
manifest["images"]["real_public_figures_allowed"] = True
manifest["images"]["real_brands_logos_and_places_allowed_when_editorially_relevant"] = True
manifest["images"]["no_false_sponsorship_or_documentary_claim"] = True
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(json.dumps({"status":"ok","version":VERSION,"articles":[f"/notizie/{a['slug']}.html" for a in articles]}, ensure_ascii=False))
