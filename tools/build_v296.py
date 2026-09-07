#!/usr/bin/env python3
from pathlib import Path
from html import escape
import hashlib, json, runpy

ROOT = Path(__file__).resolve().parents[1]
VERSION = 296
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

articles = [
    {
        "slug": "bolzano-primo-giorno-scuola-7-settembre-2026",
        "title": "Bolzano apre l’anno scolastico: primi studenti italiani di nuovo in classe",
        "excerpt": "L’Alto Adige è il primo territorio italiano a riaprire le scuole nel 2026/27. Negli istituti in lingua italiana sono attesi 22.080 studenti; alle 9 l’avvio istituzionale alle Manzoni.",
        "section": "Italia / Scuola / Alto Adige",
        "published": "2026-09-07T08:15:00+02:00",
        "key": "scuola-bolzano-primo-giorno-7-settembre-2026-ai-v296",
        "alt": "Scena editoriale contestuale generata con IA di studenti e famiglie all’ingresso di una scuola primaria di Bolzano nel primo giorno dell’anno scolastico",
        "insights": [("22.080", "studenti nelle scuole in lingua italiana"), ("7 settembre", "primo giorno di lezione"), ("ore 9", "appuntamento alle scuole Manzoni")],
        "body": [
            "Questa mattina, lunedì 7 settembre 2026, riaprono le scuole dell’Alto Adige. Sono le prime in Italia ad avviare le lezioni dell’anno scolastico 2026/27. La partenza riguarda gli istituti dei tre gruppi linguistici della provincia e anticipa il rientro previsto nei giorni successivi nelle altre regioni italiane.",
            "Nelle scuole in lingua italiana sono iscritti 22.080 bambini e ragazzi, dalla scuola dell’infanzia alla formazione professionale. Il dato diffuso dalla Provincia autonoma di Bolzano comprende quindi percorsi diversi e non va letto come il numero dei soli alunni delle elementari o delle sole scuole statali.",
            "Il primo appuntamento istituzionale è fissato alle 9 alle scuole Manzoni di Bolzano, in via Rovigo 50/A. La sovrintendente scolastica Vincenza Gullotta e il direttore provinciale per l’Istruzione e Formazione italiana Franco Galateo incontrano studenti, famiglie e personale per accompagnare l’avvio delle lezioni.",
            "Il sistema scolastico altoatesino è organizzato in strutture per lingua italiana, tedesca e ladina. Secondo i dati raccolti alla vigilia della riapertura, agli oltre 22 mila iscritti del sistema italiano si affiancano 64.749 studenti nelle scuole in lingua tedesca e 2.895 in quelle delle località ladine. Le cifre restituiscono la dimensione plurilingue del territorio, pur riferendosi a reti amministrative distinte.",
            "Per le scuole italiane la Provincia indica 3.275,75 posti di personale calcolati a tempo pieno, 85,25 in più rispetto all’anno precedente. L’incremento comprende 22 posti aggiuntivi per l’inclusione, in un sistema che segue 3.701 studenti con certificazione. I numeri descrivono le risorse assegnate, non garantiscono da soli che ogni classe inizi senza assenze o supplenze da coprire.",
            "L’avvio dell’anno coincide anche con 127 nuove immissioni in ruolo e con 101 proposte formative rivolte al personale. Tra le priorità annunciate figurano la lettura, il teatro, l’educazione ambientale, la cittadinanza e un uso consapevole dell’intelligenza artificiale. Sono linee di lavoro annuali: i risultati potranno essere valutati soltanto osservando attività, partecipazione e continuità nel corso dei mesi.",
            "Per le famiglie il calendario provinciale resta il riferimento pratico. Indica inizio e fine delle lezioni, vacanze e sospensioni comuni, mentre le singole scuole comunicano orari, accoglienza delle prime classi, servizi mensa e possibili adattamenti. Il giorno di apertura non implica quindi che ogni plesso segua lo stesso orario fin dalla prima mattina.",
            "Il fatto che Bolzano cominci prima del resto d’Italia dipende dall’autonomia con cui Regioni e Province autonome definiscono il calendario scolastico nel rispetto del quadro nazionale. Le date tengono conto del territorio, delle festività e dell’organizzazione locale. Per questo non esiste un unico giorno di rientro valido per tutte le scuole italiane.",
            "L’appuntamento odierno alle Manzoni segna l’avvio operativo delle lezioni, mentre la cerimonia provinciale ufficiale di apertura dell’anno scolastico è un evento distinto e può essere fissata in una data successiva. Separare i due momenti evita di confondere il primo giorno effettivo in classe con le iniziative istituzionali di rappresentanza.",
            "Per verificare informazioni su orari, trasporti e servizi è consigliabile partire dal sito del proprio istituto e dal calendario pubblicato dalla Provincia. Comunicazioni diffuse nelle chat di classe possono essere utili, ma devono essere confrontate con gli avvisi ufficiali, soprattutto nei primi giorni, quando entrate scaglionate e variazioni organizzative sono più frequenti."
        ],
        "evergreen_title": "Perché la scuola non ricomincia lo stesso giorno in tutta Italia",
        "evergreen_text": "Regioni e Province autonome stabiliscono i calendari nel quadro nazionale. Il sito dell’istituto resta il riferimento per orari, accoglienza e servizi del singolo plesso.",
        "sources": [
            ("https://scuola-italiana.provincia.bz.it/it/news/il-7-settembre-primo-giorno-di-scuola-in-alto-adige", "Provincia autonoma di Bolzano — primo giorno di scuola e appuntamento alle Manzoni"),
            ("https://news.provincia.bz.it/it/news/scuola-italiana-oltre-22-000-studenti-al-via-il-nuovo-anno", "Provincia autonoma di Bolzano — iscritti, personale e priorità 2026/27"),
            ("https://www.provinz.bz.it/formazione-lingue/scuola-italiana/downloads/calendario_scolastico_2026_27.pdf", "Provincia autonoma di Bolzano — calendario scolastico 2026/27"),
            ("https://www.ansa.it/trentino/notizie/2026/09/02/scuola-in-alto-adige-il-7-settembre-tornano-in-classe-in-90mila_.html", "ANSA — conferma dei dati nei tre gruppi linguistici")
        ],
        "related": [
            ("/notizie/sciopero-fs-nazionale-7-8-settembre-2026-orari-treni-garantiti.html", "Servizi", "Sciopero FS: orari e treni da controllare"),
            ("/notizie/marche-bando-1-2-milioni-videosorveglianza-control-room-4-settembre-2026.html", "Territori", "Il bando delle Marche per la sicurezza urbana"),
            ("/notizie/lavoro-divario-nord-sud-cgia-5-settembre-2026.html", "Italia", "Il divario del lavoro tra Nord e Sud")
        ],
        "prompt": "Ultra-realistic contextual editorial photograph, morning outside an Italian-language primary school in Bolzano on the first day of school, children with backpacks and parents entering, Alpine setting, Italian and European flags appearing naturally, warm documentary-style light; ordinary contextual people only, no identifiable public figure, no added headline, no watermark, no claim that this is a real event photograph."
    },
    {
        "slug": "inps-case-del-maestro-domande-soggiorni-invernali-7-settembre-2026",
        "title": "INPS, dalle 12 le domande per i soggiorni invernali nelle Case del Maestro",
        "excerpt": "La finestra online apre il 7 settembre a mezzogiorno e chiude il 23 settembre alla stessa ora. Il bando riguarda iscritti alla Gestione Assistenza Magistrale e familiari ammessi.",
        "section": "Italia / INPS / Servizi",
        "published": "2026-09-07T08:05:00+02:00",
        "key": "inps-case-maestro-soggiorni-invernali-2026-ai-v296",
        "alt": "Scena editoriale contestuale generata con IA di una donna che prepara al computer la domanda per un soggiorno invernale nelle Case del Maestro",
        "insights": [("7 settembre, ore 12", "apertura delle domande"), ("23 settembre, ore 12", "scadenza della finestra"), ("5 strutture", "le Case del Maestro disponibili")],
        "body": [
            "Dalle 12 di oggi, lunedì 7 settembre 2026, è possibile presentare la domanda per i soggiorni invernali 2026/27 nelle Case del Maestro dell’INPS. La procedura resta disponibile fino alle 12 del 23 settembre e deve essere completata attraverso il Portale Prestazioni Welfare dell’Istituto.",
            "Il concorso è rivolto agli iscritti alla Gestione Assistenza Magistrale in servizio o in pensione e ai loro parenti entro il secondo grado. Il bando disciplina anche la partecipazione di vedovi e orfani di iscritti o pensionati nelle condizioni previste. Prima dell’invio è quindi necessario controllare la propria categoria e il rapporto familiare ammesso, senza basarsi su bandi di anni precedenti.",
            "Le strutture disponibili sono la Casa del Maestro di Fiuggi, con 146 posti letto; Roma in piazza dei Giuochi Delfici, con 94; Lorica di Pedace, con 98; Silvi Marina, con 132; e San Cristoforo al Lago, con 73. Il numero dei posti indica la capienza pubblicata, non l’accettazione automatica di tutte le richieste.",
            "I soggiorni hanno una durata di dieci giorni e nove notti, con pensione completa e servizi accessori inclusi secondo quanto stabilito dal bando. Le consumazioni al bar restano a carico degli ospiti. Periodi, assegnazioni e condizioni economiche devono essere letti negli allegati ufficiali, che prevalgono su ogni riepilogo giornalistico.",
            "La pubblicazione del bando è avvenuta il 4 settembre; l’apertura della procedura è invece fissata al 7 settembre alle 12. Sono due momenti diversi. Prima di mezzogiorno la pagina informativa può essere consultata, ma la finestra utile per trasmettere la domanda non è ancora operativa.",
            "La richiesta online non equivale all’assegnazione del soggiorno. Dopo la chiusura, l’INPS applica i criteri previsti dal concorso e pubblica gli esiti nei canali collegati al bando. Conviene conservare la ricevuta e verificare lo stato della pratica, perché un modulo compilato ma non trasmesso entro la scadenza non partecipa alla procedura.",
            "Le Case del Maestro sono strutture di proprietà dell’INPS destinate a soggiorni climatico-termali per gli iscritti alla Gestione Assistenza Magistrale e per gli altri beneficiari indicati. Ogni anno l’Istituto pubblica concorsi separati per diversi periodi: requisiti, durata e termini possono cambiare, quindi il servizio generale non sostituisce il bando specifico 2026/27.",
            "Per ridurre gli errori è utile preparare in anticipo credenziali di accesso, dati del richiedente e dei partecipanti, eventuali informazioni economiche richieste e ordine delle preferenze. Nomi, date di nascita e legami familiari devono corrispondere ai documenti. Se il portale segnala campi mancanti, la domanda va corretta e inviata prima delle 12 del 23 settembre.",
            "Non è prudente attendere gli ultimi minuti. Un’interruzione della connessione o un passaggio non confermato può impedire la trasmissione entro il termine. Dopo l’invio è opportuno scaricare la ricevuta, annotare il numero della domanda e tornare nella propria area personale per controllare che lo stato registrato sia quello atteso.",
            "Aggiornamenti, graduatorie e comunicazioni successive saranno pubblicati dall’INPS nella pagina del concorso. CurioMondo aggiornerà questo articolo quando saranno disponibili gli esiti, mantenendo separati i dati già ufficiali dalle informazioni che dipenderanno dal numero delle domande e dalle procedure di assegnazione."
        ],
        "evergreen_title": "Come evitare gli errori nelle domande INPS a scadenza",
        "evergreen_text": "Usa il bando dell’anno corretto, prepara i dati prima di iniziare, invia con anticipo e conserva la ricevuta. Una bozza salvata non sempre equivale a una domanda trasmessa.",
        "sources": [
            ("https://www.inps.it/it/it/inps-comunica/notizie/dettaglio-news-page.news.2026.09.case-del-maestro-pubblicato-il-bando-soggiorni-invernali-2026-2027.html", "INPS — comunicazione sul bando soggiorni invernali 2026/27"),
            ("https://www.inps.it/it/it/avvisi-bandi-e-fatturazione/welfare-assistenza-e-mutualita/welfare-bandi/cerca-bandi.html", "INPS — banca dati ufficiale dei bandi welfare"),
            ("https://www.inps.it/it/it/dettaglio-scheda.it.schede-servizio-strumento.schede-servizi.ospitalit-presso-case-del-maestro-per-iscritti-gestione-assistenza-magistrale-50037.ospitalit-presso-case-del-maestro-per-iscritti-gestione-assistenza-magistrale.html", "INPS — servizio Ospitalità presso le Case del Maestro"),
            ("https://www.inps.it/it/it/dettaglio-scheda.it.schede-servizio-strumento.schede-aree-tematiche.portale-prestazioni-welfare.html", "INPS — Portale Prestazioni Welfare")
        ],
        "related": [
            ("/notizie/bolzano-primo-giorno-scuola-7-settembre-2026.html", "Scuola", "Bolzano, primi studenti di nuovo in classe"),
            ("/notizie/sciopero-fs-nazionale-7-8-settembre-2026-orari-treni-garantiti.html", "Servizi", "Sciopero FS: orari e collegamenti garantiti"),
            ("/notizie/marche-bando-1-2-milioni-videosorveglianza-control-room-4-settembre-2026.html", "Bandi", "Marche, 1,2 milioni per la sicurezza urbana")
        ],
        "prompt": "Ultra-realistic contextual editorial photograph of a mature Italian woman completing an online public-service application on a laptop at home, travel documents and a winter bag nearby, a welcoming mountain lodge and snow visible through the window, natural neutral interface shapes without readable personal data, no added headline, no watermark, no false documentary claim."
    }
]

MONTHS = {9: "settembre"}

def page(a):
    canonical = f"https://curiomondo.it/notizie/{a['slug']}.html"
    image = f"https://curiomondo.it/assets/images/editorial-auto/{a['key']}-1200.webp"
    schema = {"@context":"https://schema.org","@type":"NewsArticle","headline":a["title"],"description":a["excerpt"],"datePublished":a["published"],"dateModified":a["published"],"mainEntityOfPage":canonical,"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo","url":"https://curiomondo.it/pagine/redazione.html"},"publisher":{"@type":"Organization","name":"CurioMondo","logo":{"@type":"ImageObject","url":"https://curiomondo.it/curiomondo-logo-512.png"}},"image":[image]}
    insights = "".join(f'<div><b>{escape(x)}</b><small>{escape(y)}</small></div>' for x,y in a["insights"])
    related = "".join(f'<a href="{u}"><small>{escape(k)}</small><strong>{escape(t)}</strong></a>' for u,k,t in a["related"])
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(t)}</a></li>' for u,t in a["sources"])
    tm = a["published"][11:16]
    date_label = "7 settembre 2026"
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(a['title'])} | CurioMondo</title><meta name="description" content="{escape(a['excerpt'],quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(a['title'],quote=True)}"><meta property="og:description" content="{escape(a['excerpt'],quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{escape(a['alt'],quote=True)}"><meta name="theme-color" content="#eaf8ff"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=296"><link rel="stylesheet" href="../assets/css/editorial-trust-v263.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{a['slug']}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="wrap"><div class="badge">{escape(a['section'])}</div><h1>{escape(a['title'])}</h1><p class="subtitle">{escape(a['excerpt'])}</p><div class="meta">{date_label} · aggiornato alle {tm} · {escape(a['section'])} · <span id="readTime">5 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html" rel="author">Redazione CurioMondo</a> · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></p><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-sensitive-context="false" data-portrait-format="contextual-editorial-scene"><picture><img src="../assets/images/editorial-auto/{a['key']}-800.webp" srcset="../assets/images/editorial-auto/{a['key']}-480.webp 480w, ../assets/images/editorial-auto/{a['key']}-800.webp 800w, ../assets/images/editorial-auto/{a['key']}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(a['alt'],quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{insights}</div></section><article class="art-body" data-length-policy="3000-7000">{''.join(f'<p>{escape(x)}</p>' for x in a['body'])}</article><section class="cm-evergreen-reader"><small>Da conservare</small><h2>{escape(a['evergreen_title'])}</h2><p>{escape(a['evergreen_text'])}</p></section><section class="curio-related" aria-labelledby="rel-{a['slug']}"><h2 id="rel-{a['slug']}">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Ultimo aggiornamento editoriale: {date_label}, ore {tm} italiane.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=296" defer></script></body></html>'''

for article in articles:
    (ROOT / "notizie" / f"{article['slug']}.html").write_text(page(article), encoding="utf-8")

registry_path = ROOT / "assets/data/editorial-images-v210.json"
registry = json.loads(registry_path.read_text(encoding="utf-8"))
for article in reversed(articles):
    registry["items"] = [item for item in registry["items"] if item.get("key") != article["key"]]
    variants = []
    for width in (480, 800, 1200):
        file_path = ROOT / "assets/images/editorial-auto" / f"{article['key']}-{width}.webp"
        variants.append({"w": width, "src": f"/assets/images/editorial-auto/{file_path.name}", "sha256": hashlib.sha256(file_path.read_bytes()).hexdigest(), "bytes": file_path.stat().st_size})
    registry["items"].insert(0, {"key":article["key"],"article":f"/notizie/{article['slug']}.html","aiGenerated":True,"sensitiveContext":False,"documentaryPhoto":False,"prompt":article["prompt"],"variants":variants,"alt":article["alt"],"disclosure":CAPTION,"portraitOnly":False,"portraitFormat":"contextual-editorial-scene","reenactedEvent":False})
registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

runpy.run_path(str(ROOT / "tools/finalize_articles_20260906.py"), run_name="__main__")
for rel in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json", "assets/data/editorial-images-v210.json"):
    path = ROOT / rel
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

index_path = ROOT / "index.html"
index_text = index_path.read_text(encoding="utf-8")
import re
index_text = re.sub(r'home-bundle-v291\.css\?v=\d+', f'home-bundle-v291.css?v={VERSION}', index_text)
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
