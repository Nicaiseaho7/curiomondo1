#!/usr/bin/env python3
from pathlib import Path
import ast, hashlib, json, re, runpy

ROOT = Path(__file__).resolve().parents[1]
VERSION = 302
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."

articles = [
    {
        "slug": "friuli-venezia-giulia-2-7-milioni-disabilita-bes-dsa-scuola-7-settembre-2026",
        "title": "Friuli Venezia Giulia, 2,7 milioni per alunni con disabilità, BES e DSA",
        "excerpt": "Il pacchetto regionale per il 2026/27 finanzia sostegno, progetti per bisogni educativi speciali e DSA, libri accessibili e formazione sulla gestione delle crisi comportamentali.",
        "section": "Italia / Friuli Venezia Giulia / Scuola / Inclusione",
        "published": "2026-09-07T17:18:00+02:00",
        "key": "friuli-inclusione-scolastica-disabilita-bes-dsa-7-settembre-2026-ai-v302",
        "alt": "Docente al lavoro con una classe inclusiva e studenti che utilizzano strumenti didattici accessibili, illustrazione editoriale fotorealistica generata con IA",
        "insights": [("circa 2,7 milioni €", "le risorse dirette annunciate per il 2026/27"), ("900.000 €", "la quota per BES, dispersione e criticità"), ("4 scuole CTS", "i capofila della nuova rete formativa")],
        "body": [
            "La Regione Friuli Venezia Giulia ha presentato un pacchetto di risorse dirette vicino a 2,7 milioni di euro per rafforzare l’inclusione scolastica nell’anno 2026/2027. Gli interventi riguardano alunni con disabilità, bisogni educativi speciali e disturbi specifici dell’apprendimento, ma non confluiscono in un unico fondo indistinto: ogni quota ha una destinazione precisa e canali di attuazione differenti.",
            "La voce più consistente, pari a 1.050.000 euro, sostiene l’inclusione nelle scuole paritarie. Di questa somma, 750.000 euro sono destinati alle scuole dell’infanzia e 300.000 alle primarie e secondarie. Le paritarie sono istituti non statali che fanno parte del sistema nazionale di istruzione e rispettano requisiti stabiliti dalla legge; il finanziamento regionale punta a sostenere il servizio scolastico rivolto agli alunni con disabilità anche in queste strutture.",
            "Altri 500.000 euro serviranno ad aumentare il sostegno nelle scuole statali attraverso il “Pacchetto scuola”, realizzato d’intesa con l’Ufficio scolastico regionale. Il comunicato del 4 settembre, che descrive il protocollo complessivo da 4,5 milioni, precisa che queste risorse incrementano le ore dei docenti di sostegno. Il pacchetto da 2,7 milioni annunciato oggi concentra invece l’attenzione sulle misure direttamente legate all’inclusione.",
            "Per gli studenti con disturbi specifici dell’apprendimento sono previsti 250.000 euro destinati al personale nelle scuole in cui l’incidenza degli alunni con DSA supera l’8%. Rientrano tra i DSA, per esempio, dislessia, disgrafia, disortografia e discalculia: caratteristiche che interessano abilità specifiche dell’apprendimento e non misurano l’intelligenza dello studente. Gli interventi scolastici possono includere strumenti compensativi, modalità didattiche personalizzate e personale formato.",
            "La quota di 900.000 euro riguarda gli alunni con bisogni educativi speciali, il contrasto alla dispersione e situazioni di particolare criticità. BES è una categoria educativa più ampia di DSA e disabilità certificata: indica la necessità, anche temporanea, di una particolare attenzione didattica dovuta a condizioni personali, sociali, linguistiche o di apprendimento. Non è quindi una diagnosi medica unica e non tutti gli studenti classificati come BES hanno gli stessi bisogni.",
            "Il programma comprende inoltre 40.000 euro per rendere disponibili libri scolastici accessibili ad alunni ipovedenti o non vedenti. L’accessibilità può richiedere formati digitali compatibili con tecnologie assistive, caratteri ingranditi, versioni Braille o adattamenti concordati con la scuola e la famiglia. A queste risorse si affiancano laboratori PCTO e un futuro avviso per BES, DSA e plusdotazioni, il cui fabbisogno biennale stimato in 225.163,06 euro dovrà essere integrato successivamente.",
            "Una novità distinta è il progetto dei Centri territoriali di supporto, finanziato in via straordinaria con 36.000 euro. Ciascuno dei quattro istituti capofila — Pertini di Monfalcone, Kennedy di Pordenone, Copernico di Udine e Roiano Gretta-Margherita Hack di Trieste — riceverà 9.000 euro. La rete dovrà formare i docenti e costruire modalità condivise per prevenire e gestire crisi comportamentali associate a disabilità complesse, evitando che ogni scuola affronti da sola situazioni delicate.",
            "Formazione e rete territoriale sono importanti perché una crisi comportamentale non coincide automaticamente con aggressività o cattiva condotta. Può essere una risposta a sovraccarico sensoriale, difficoltà comunicative, dolore, ansia o cambiamenti improvvisi. Un intervento competente cerca prima di tutto le cause, riduce i fattori scatenanti e tutela lo studente, i compagni e il personale, con procedure preparate e non improvvisate nel momento di maggiore tensione.",
            "Il dato da conservare è quindi la struttura del piano, non soltanto il totale. Le risorse coprono sostegno nelle paritarie e nelle statali, personale per DSA, interventi BES, materiali accessibili e una nuova rete CTS. L’efficacia potrà essere valutata con indicatori concreti: ore aggiuntive effettivamente erogate, studenti raggiunti, disponibilità tempestiva dei libri, partecipazione dei docenti alla formazione e riduzione delle situazioni in cui scuole e famiglie restano senza supporto.",
        ],
        "evergreen_title": "Inclusione non significa proporre a tutti lo stesso percorso",
        "evergreen_text": "Una scuola inclusiva mantiene obiettivi formativi comuni ma adatta strumenti, tempi, comunicazione e supporti affinché ciascuno possa partecipare e apprendere realmente.",
        "sources": [
            ("https://www.regione.fvg.it/rafvg/comunicati/comunicato.act?dir=%2Frafvg%2Fcms%2FRAFVG%2Fnotiziedallagiunta%2F&nm=20260907121925001", "Regione Friuli Venezia Giulia — comunicato ufficiale del 7 settembre 2026, ore 12:19"),
            ("https://www.regione.fvg.it/rafvg/comunicati/comunicato.act?dir=%2Frafvg%2Fcms%2FRAFVG%2Fnotiziedallagiunta%2F&nm=20260904135945005", "Regione Friuli Venezia Giulia — protocollo scuola 2026/27 e ripartizione delle risorse"),
            ("https://usrfvg.gov.it/it/home/menu/aree/Percorsi-educativi/inclusione/BES/index.html", "Ufficio scolastico regionale FVG — area ufficiale inclusione e BES"),
            ("https://usrfvg.gov.it/archivio/export/sites/default/USRFVG/Progetti_scuola/Inclusione_disabilita/OrganizzTerr/CTS_CTI", "Ufficio scolastico regionale FVG — Centri territoriali di supporto"),
        ],
        "related": [
            ("/notizie/bolzano-primo-giorno-scuola-7-settembre-2026.html", "Scuola", "Bolzano, primo giorno di scuola per oltre 90.000 studenti"),
            ("/categorie/italia/", "Italia", "Le ultime notizie dall’Italia"),
            ("/notizie/", "Archivio", "Tutte le notizie verificate da CurioMondo"),
        ],
        "prompt": "Ultra-realistic premium editorial image of a contemporary inclusive classroom in Friuli Venezia Giulia, a female teacher supporting diverse students including one wheelchair user and accessible learning materials, respectful natural interaction, bright morning light, no readable text, logos, captions or watermark."
    },
    {
        "slug": "italia-estate-2026-piu-calda-dal-1950-battuto-2003-cnr",
        "title": "Italia, l’estate 2026 è la più calda dal 1950: battuto il 2003",
        "excerpt": "Il CNR-IBE calcola una temperatura media nazionale di 24,3 °C. Agosto ha raggiunto 25,6 °C, con un’anomalia di 3,5 °C rispetto al periodo 1991-2020.",
        "section": "Italia / Ambiente / Clima / Scienza",
        "published": "2026-09-07T17:16:00+02:00",
        "key": "italia-estate-2026-piu-calda-dal-1950-cnr-ai-v302",
        "alt": "Stazione meteorologica in un paesaggio agricolo italiano durante una giornata estiva molto calda, illustrazione editoriale fotorealistica generata con IA",
        "insights": [("24,3 °C", "la temperatura media nazionale dell’estate 2026"), ("25,6 °C", "la media italiana registrata in agosto"), ("+3,5 °C", "l’anomalia di agosto sul periodo 1991-2020")],
        "body": [
            "L’estate meteorologica 2026 è stata la più calda in Italia dall’inizio della serie analizzata, nel 1950. La certificazione arriva dall’Istituto per la BioEconomia del Consiglio nazionale delle ricerche: la temperatura media calcolata sull’intero territorio nazionale è stata di 24,3 °C a due metri dal suolo, superando i 23,6 °C dell’estate 2003, che fino a oggi rappresentava il riferimento record.",
            "Il valore di 24,3 °C non è la massima raggiunta in una città né la media delle sole ore più calde. È una media territoriale e stagionale ricavata da elaborazioni del dataset ERA5-Land del Centro europeo per le previsioni meteorologiche a medio termine. Questo sistema combina osservazioni e modelli per descrivere in modo coerente le condizioni del suolo e dell’atmosfera; consente confronti tra anni diversi anche dove le stazioni sono distribuite in modo irregolare.",
            "Agosto è stato il mese più estremo della stagione, con una media nazionale di 25,6 °C. Lo scarto è di 5,2 °C rispetto alla media di agosto del periodo 1951-1980, pari a 20,4 °C, e di 3,5 °C rispetto alla climatologia 1991-2020, pari a 22,1 °C. La parola “anomalia”, in climatologia, indica proprio questa differenza rispetto a un periodo di riferimento: non significa errore nella misurazione.",
            "La media di agosto 2026 supera nettamente i precedenti primati mensili: 24,6 °C nel 2024 e 24,0 °C nel 2017. Le mappe elaborate dal CNR-IBE mostrano inoltre un fatto mai rilevato prima nella serie: luglio e agosto sono risultati consecutivamente i più caldi in assoluto per il rispettivo mese. È la continuità del calore, oltre al singolo picco, a determinare il nuovo record estivo.",
            "Anche il resto dell’anno ha mantenuto valori elevati. Tra gennaio e agosto ogni mese ha registrato temperature superiori allo stesso periodo del 2025. La primavera aveva già eguagliato il record stagionale con una media di 12,1 °C. Secondo il ricercatore Lorenzo Arcidiaco, questi dati fanno pensare che il 2026 possa chiudersi come l’anno più caldo dal 1950; è però una proiezione, non ancora un risultato definitivo, perché mancano gli ultimi quattro mesi.",
            "L’aumento non è distribuito in modo uniforme. Nel periodo gennaio-agosto circa il 70% del territorio nazionale ha mostrato anomalie superiori a un grado e circa il 40% anomalie oltre i due gradi. Le concentrazioni più significative riguardano le pianure del Nord-Ovest e le aree appenniniche. Molte di queste superfici sono coltivate e l’unione di temperature elevate e siccità aumenta lo stress per colture, suolo e disponibilità idrica.",
            "Analisi basate sui dati GSOD e OGIMET confermano ripetute ondate di calore a Roma, Firenze e Torino nei mesi di giugno, luglio e agosto. Nella metodologia richiamata dal CNR, un’ondata di calore è un periodo di almeno sei giorni consecutivi in cui le temperature massime superano il novantesimo percentile locale. Il percentile confronta ogni giornata con il clima abituale di quel luogo: la stessa temperatura può quindi essere eccezionale in una città e meno insolita in un’altra.",
            "Il record italiano è coerente con un’estate molto calda in diverse parti d’Europa, ma non dimostra da solo la causa di ogni singolo episodio meteorologico. Per attribuire quantitativamente un evento al cambiamento climatico servono studi specifici. La tendenza di fondo, tuttavia, va letta su serie lunghe: il superamento del 2003 e la successione dei primati recenti sono segnali che acquistano significato proprio perché confrontati con oltre settantacinque anni di dati.",
            "Il prossimo passaggio sarà verificare come evolveranno autunno e inverno e quale posizione occuperà il 2026 nella classifica annuale completa. Nel frattempo, il dato ufficiale da conservare è netto: 24,3 °C di media nazionale per l’estate, 25,6 °C in agosto e il primo doppio primato consecutivo di luglio e agosto. Sono valori utili non soltanto per descrivere il caldo percepito, ma per programmare agricoltura, gestione dell’acqua, salute pubblica e adattamento delle città.",
        ],
        "evergreen_title": "Meteo e clima misurano scale diverse",
        "evergreen_text": "Il meteo descrive condizioni ed eventi di breve durata. Il clima emerge da serie lunghe e confronti omogenei: per questo un record nazionale richiede dati, metodi e periodi di riferimento dichiarati.",
        "sources": [
            ("https://www.cnr.it/it/nota-stampa/n-14606", "Consiglio nazionale delle ricerche — nota stampa ufficiale del 7 settembre 2026"),
            ("https://www.reuters.com/business/environment/italy-logs-hottest-summer-more-than-75-years-institute-says-2026-09-07/", "Reuters — conferma indipendente dei dati CNR-IBE"),
            ("https://www.ansa.it/canale_scienza/notizie/terra_poli/2026/09/07/il-cnr-lestate-2026-la-piu-calda-in-italia-dal-1950_f3f1a86a-df4a-47fc-95fe-0e9c27fa80f7.html", "ANSA Scienza — metodologia, confronto con il 2003 e anomalie"),
            ("https://www.ecmwf.int/en/era5-land", "ECMWF — documentazione ufficiale del dataset ERA5-Land"),
        ],
        "related": [
            ("/notizie/caldo-estremo-32000-decessi-eccesso-europa-2026.html", "Clima", "Caldo estremo e mortalità in Europa"),
            ("/notizie/siccita-po-lombardia-piemonte-record-autobotti-1-settembre-2026.html", "Italia", "Il nuovo minimo del Po e la crisi idrica"),
            ("/categorie/ambiente/", "Ambiente", "Tutte le notizie su clima e ambiente"),
        ],
        "prompt": "Ultra-realistic premium editorial image of a scientific weather station in a heat-shimmering Italian agricultural landscape, dry field edges and distant Apennine foothills, harsh summer daylight, sober factual mood, no readable displays, text, logos, captions, flags or watermark."
    },
]

# Riusa il template articolo già validato senza eseguire il builder precedente.
tree = ast.parse((ROOT / "tools/build_v301.py").read_text(encoding="utf-8"))
nodes = [n for n in tree.body if isinstance(n, (ast.Import, ast.ImportFrom)) or (isinstance(n, ast.FunctionDef) and n.name == "page")]
scope = {"ROOT": ROOT, "VERSION": VERSION, "CAPTION": CAPTION, "articles": articles}
exec(compile(ast.Module(body=nodes, type_ignores=[]), "build_v301.py", "exec"), scope)
for article in articles:
    (ROOT / "notizie" / f"{article['slug']}.html").write_text(scope["page"](article), encoding="utf-8")

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
    path = ROOT / rel; data = json.loads(path.read_text(encoding="utf-8")); data["version"] = VERSION
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
runpy.run_path(str(ROOT / "tools/generate_category_pages.py"), run_name="__main__")
index_path = ROOT / "index.html"
index_path.write_text(re.sub(r'home-bundle-v291\.css\?v=\d+', f'home-bundle-v291.css?v={VERSION}', index_path.read_text(encoding="utf-8")), encoding="utf-8")
manifest_path = ROOT / "curiomondo-site-manifest.json"
manifest = json.loads(manifest_path.read_text(encoding="utf-8")); manifest["site"]["current_site_version"] = VERSION; manifest["site"]["site_version"] = VERSION
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status":"ok","version":VERSION,"articles":[f"/notizie/{a['slug']}.html" for a in articles]}, ensure_ascii=False))
