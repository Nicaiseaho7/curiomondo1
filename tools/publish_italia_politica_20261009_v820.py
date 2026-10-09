#!/usr/bin/env python3
"""Release v820: dieci notizie recenti dall'Italia, inclusa politica."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site  # noqa: E402

VERSION = 820
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"

IMAGE_SOURCES = {
    "tornado": GENERATED / "exec-f705633e-a26e-4f1a-a8e8-b6427919ad3f.png",
    "meteo": GENERATED / "exec-a6980f2a-b923-4e58-a8f0-844a22b014a5.png",
    "nato": GENERATED / "exec-96e42fe5-9078-4f1d-bbc1-7eb782afcb58.png",
    "intesa": GENERATED / "exec-e8e66078-106a-4571-ab2e-c9a6b2eec648.png",
    "privacy": GENERATED / "exec-02ac4970-a9cf-4200-8fed-108ce65bcdcf.png",
    "cagliari": GENERATED / "exec-ca6f86e0-cb6a-4800-af75-d4b5471a924d.png",
    "trieste": GENERATED / "exec-47696b57-d7d6-41d2-b2b1-0b42a8ea1744.png",
    "salvini": GENERATED / "exec-52ee2294-bb0a-44c5-bc11-4032d42b975a.png",
    "meloni": GENERATED / "exec-1666a82e-d30a-441b-ba15-c9ddd421b116.png",
    "data_center": GENERATED / "exec-b1092f3d-50c4-436d-a6cd-312e905c5016.png",
}


def make_variants(source: Path, slug: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 16 / 9
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    output = ROOT / "assets/images/editorial-auto"
    variants = []
    for width in (480, 800, 1200):
        path = output / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, round(width / ratio)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=89, method=6
        )
        variants.append({
            "w": width,
            "h": round(width / ratio),
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return variants


def make_image(article: dict) -> dict:
    image = {
        "key": f"{article['slug']}-v{VERSION}",
        "alt": article.pop("image_alt"),
        "prompt": article.pop("image_prompt"),
        "variants": make_variants(IMAGE_SOURCES[article.pop("image_source")], article["slug"]),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": bool(article.pop("sensitive_image", False)),
        "weatherMap": False,
        "reenactedEvent": False,
    }
    if article.pop("public_figure", False):
        image["syntheticLikeness"] = "public-figure"
        if image["sensitiveContext"]:
            image["portraitOnly"] = True
            image["portraitFormat"] = "neutral-isolated"
    return image


def set_published(slug: str, published: datetime) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    iso = published.isoformat(timespec="seconds")
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data["datePublished"] = iso
            data["dateModified"] = iso
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )


def append_name_phrases() -> None:
    path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        "Oggi puoi occuparti di ciò che è davvero urgente.",
        "Se il tempo cambia, scegli il percorso più sicuro.",
        "Puoi informarti bene prima di prendere posizione.",
        "Una scelta prudente può proteggere il lavoro di domani.",
        "Hai il diritto di sapere come vengono usati i tuoi dati.",
        "Questa sera puoi concederti un'ora per la bellezza.",
        "Prenotare in anticipo può rendere più semplice la tua serata.",
        "Ascolta i numeri, ma controlla sempre anche le condizioni.",
        "Prepararti prima ti aiuta a seguire meglio le decisioni.",
        "Una stima è utile quando ne conosci anche i limiti.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


ARTICLES = [
    {
        "slug": "tromba-aria-trapanese-marsala-petrosino-due-feriti-9-ottobre-2026",
        "titolo": "Tromba d'aria nel Trapanese: scuola colpita e due feriti",
        "sommario": "Danni tra Marsala, Petrosino e Mazara del Vallo. Alla scuola De Gasperi alunni e personale sono al sicuro; in campo cinque squadre dei Vigili del fuoco.",
        "categoria": "Cronaca", "luogo": "Trapani", "formato": "flash",
        "parole_chiave_titolo": ["Tromba d'aria", "Trapanese"],
        "dati_chiave": [
            {"valore": "3 comuni", "etichetta": "Marsala, Petrosino e Mazara"},
            {"valore": "2 feriti", "etichetta": "bilancio comunicato dai soccorritori"},
            {"valore": "5 squadre", "etichetta": "Vigili del fuoco impegnati"},
        ],
        "paragrafi": [
            "Una tromba d'aria ha colpito nella mattinata del 9 ottobre il Trapanese, provocando danni tra Marsala, Petrosino e Mazara del Vallo. I Vigili del fuoco riferiscono di tetti scoperchiati, alberi e pali abbattuti e veicoli danneggiati o ribaltati.",
            "A Marsala è stata interessata anche la scuola Alcide De Gasperi. La dirigente ha comunicato che alunni e personale sono al sicuro grazie all'intervento tempestivo; le verifiche sull'edificio e sulle aree circostanti restano affidate alle autorità competenti.",
            "La situazione più grave segnalata dai soccorritori riguarda Petrosino, dove un'auto è finita in un dirupo. Il bilancio diffuso dai Vigili del fuoco è di due persone ferite.",
            "Sul territorio operano cinque squadre, con rinforzi arrivati dai comandi di Palermo e Agrigento. Chi si trova nelle zone coinvolte dovrebbe evitare strade con alberi o linee elettriche danneggiate e attenersi alle indicazioni dei comuni e della Protezione civile.",
        ],
        "fonti": [
            {"url": "https://www.vigilfuoco.it/media/notizie/tromba-daria-devasta-il-trapanese", "nome": "Vigili del fuoco — interventi e primo bilancio nel Trapanese."},
            {"url": "https://www.ansa.it/sicilia/notizie/2026/10/09/tromba-daria-nel-trapanese-colpita-una-scuola_f9fbc764-3c89-468c-a2d6-3f959d2adf87.html", "nome": "ANSA — aggiornamento dalla scuola Alcide De Gasperi."},
        ],
        "image_source": "tornado", "sensitive_image": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica dei danni causati da una tromba d'aria vicino a una scuola nel Trapanese, senza persone ferite; scena non documentaria.",
        "image_prompt": "Danni da tromba d'aria nel Trapanese presso una scuola, palme piegate e mezzi dei vigili del fuoco, scena sobria senza feriti né veicoli ribaltati, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "maltempo-allerta-arancione-lazio-campania-9-ottobre-2026",
        "titolo": "Maltempo, allerta arancione in Lazio e Campania: le zone a rischio",
        "sommario": "Temporali forti, grandine e raffiche interessano il Centro-Sud. La Protezione civile indica criticità arancione in alcuni settori e gialla in quattordici regioni.",
        "categoria": "Meteo", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Allerta arancione", "Lazio e Campania"],
        "dati_chiave": [
            {"valore": "2 regioni", "etichetta": "settori in allerta arancione"},
            {"valore": "14 regioni", "etichetta": "aree interessate dall'allerta gialla"},
            {"valore": "9 ottobre", "etichetta": "giornata di validità"},
        ],
        "paragrafi": [
            "La Protezione civile ha valutato per venerdì 9 ottobre un'allerta arancione su settori del Lazio e della Campania. Nel Lazio le zone indicate comprendono il Bacino del Liri, i Bacini costieri meridionali e l'Aniene; in Campania la criticità più alta riguarda la Piana campana, Napoli, le isole e l'area vesuviana.",
            "Le precipitazioni possono assumere carattere di rovescio o temporale, con raffiche di vento, grandinate e attività elettrica. Il quadro interessa anche Basilicata, Calabria e Sicilia, oltre alle aree interne di Abruzzo e Molise.",
            "L'allerta gialla coinvolge porzioni di quattordici regioni. Il livello effettivo varia però da zona a zona: per spostamenti e attività all'aperto bisogna consultare il bollettino regionale e gli avvisi del proprio comune.",
            "Durante i temporali è prudente evitare sottopassi, corsi d'acqua, litorali esposti e aree alberate. Gli aggiornamenti locali possono cambiare con l'evoluzione delle celle temporalesche e prevalgono sempre sulle indicazioni generali.",
        ],
        "fonti": [
            {"url": "https://www.protezionecivile.gov.it/it/comunicato-stampa/maltempo-allerta-arancione-su-lazio-e-campania/", "nome": "Dipartimento della Protezione civile — comunicato e fenomeni previsti."},
            {"url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/", "nome": "Protezione civile — bollettino nazionale delle criticità."},
        ],
        "image_source": "meteo",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un temporale sul Centro-Sud Italia con Napoli e il Vesuvio riconoscibili; scena non documentaria.",
        "image_prompt": "Forte temporale sul Golfo di Napoli e Vesuvio, pioggia intensa e fulmini lontani, illustrazione editoriale ultrarealistica senza testo né mappa.",
    },
    {
        "slug": "nato-steadfast-noon-italia-13-ottobre-2026",
        "titolo": "NATO, Steadfast Noon parte dall'Italia: coinvolti 17 Paesi",
        "sommario": "L'esercitazione nucleare annuale inizia il 13 ottobre. L'Alleanza precisa che non saranno impiegate armi reali e che l'attività era pianificata da tempo.",
        "categoria": "Italia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Steadfast Noon", "17 Paesi"],
        "dati_chiave": [
            {"valore": "13 ottobre", "etichetta": "inizio dell'esercitazione"},
            {"valore": "17 Paesi", "etichetta": "alleati partecipanti"},
            {"valore": "0 armi reali", "etichetta": "munizionamento nucleare escluso"},
        ],
        "paragrafi": [
            "La NATO avvierà martedì 13 ottobre Steadfast Noon, la sua esercitazione nucleare annuale. L'attività si svolgerà con l'Italia come paese ospitante e coinvolgerà personale e mezzi di diciassette nazioni alleate.",
            "L'Alleanza descrive l'appuntamento come un'attività di addestramento ordinaria e pianificata da tempo. Non saranno utilizzate armi nucleari reali e lo scenario non è collegato a eventi internazionali in corso né diretto contro un paese specifico.",
            "Le manovre servono a verificare procedure, comunicazioni e capacità convenzionali connesse alla missione di deterrenza. La NATO non diffonde tutti i dettagli operativi, anche per ragioni di sicurezza.",
            "Per il pubblico italiano l'elemento concreto sarà soprattutto una maggiore attività militare nelle aree interessate. Eventuali limitazioni locali a traffico o spazi aerei dovranno essere comunicate dalle autorità competenti attraverso avvisi dedicati.",
        ],
        "fonti": [{"url": "https://www.nato.int/en/news-and-events/articles/news/2026/10/08/nato-holds-annual-nuclear-exercise-steadfast-noon", "nome": "NATO — comunicato ufficiale su Steadfast Noon 2026."}],
        "image_source": "nato",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di velivoli e personale NATO in una base italiana, con volti visibili; scena non documentaria.",
        "image_prompt": "Base aerea italiana con velivoli e personale NATO multinazionale rivolto verso la camera, bandiere ufficiali riconoscibili, illustrazione editoriale ultrarealistica e neutrale.",
    },
    {
        "slug": "intesa-sanpaolo-20-miliardi-piccole-imprese-pos-2026",
        "titolo": "Intesa Sanpaolo, 20 miliardi alle piccole imprese e POS agevolati",
        "sommario": "Il nuovo programma per commercio, turismo e artigianato prevede credito e commissioni azzerate sui pagamenti fisici fino a 20 euro.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["20 miliardi", "Piccole imprese"],
        "dati_chiave": [
            {"valore": "20 miliardi", "etichetta": "nuovo credito annunciato"},
            {"valore": "fino a 20 euro", "etichetta": "pagamenti POS senza commissione"},
            {"valore": "800.000", "etichetta": "clienti del comparto"},
        ],
        "paragrafi": [
            "Intesa Sanpaolo ha annunciato un programma da 20 miliardi di euro di nuovo credito per piccole imprese di commercio, turismo e artigianato. La banca stima che in Italia operino oltre 4,4 milioni di attività di piccola dimensione e dichiara circa 800.000 clienti nei comparti interessati.",
            "Sul fronte dei pagamenti, il piano azzera le commissioni sui POS fisici per le transazioni fino a 20 euro. Secondo l'istituto, l'iniziativa può evitare fino a 100 milioni di euro di costi nell'arco di quattordici mesi, con un beneficio medio stimato in circa 450 euro per esercente.",
            "Per alcune formule di finanziamento la banca prevede inoltre di farsi carico degli interessi sulla prima rata e sulle rate di fine 2027 e fine 2028. Il risparmio medio indicato è di circa 600 euro per impresa.",
            "Importi, durata e accesso dipendono dalle condizioni dei singoli prodotti e dalla valutazione del credito. Le aziende interessate devono quindi verificare con la banca i requisiti, le scadenze e l'effettiva applicazione delle agevolazioni al proprio contratto.",
        ],
        "fonti": [{"url": "https://group.intesasanpaolo.com/it/newsroom/comunicati-stampa/2026/10/intesa-sanpaolo-e-le-associazioni-di-categoria-del-commercio--tu", "nome": "Intesa Sanpaolo — programma per commercio, turismo e artigianato."}],
        "image_source": "intesa",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di piccoli imprenditori italiani con un terminale POS in una filiale Intesa Sanpaolo; scena non documentaria.",
        "image_prompt": "Piccoli imprenditori italiani in filiale Intesa Sanpaolo con terminale POS, volti visibili e logo riconoscibile, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "email-tracking-pixel-linee-guida-garante-29-ottobre-2026",
        "titolo": "Tracking nelle email, adeguamento obbligatorio entro il 29 ottobre",
        "sommario": "Il Garante privacy fissa il termine per informative, consenso e revoca relativi a pixel e tecnologie che misurano aperture e interazioni.",
        "categoria": "Tecnologia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Tracking nelle email", "29 ottobre"],
        "dati_chiave": [
            {"valore": "29 ottobre", "etichetta": "termine per l'adeguamento"},
            {"valore": "consenso preventivo", "etichetta": "regola generale per il tracciamento"},
            {"valore": "2° semestre", "etichetta": "ispezioni programmate nel 2026"},
        ],
        "paragrafi": [
            "Imprese, piattaforme e gestori di newsletter hanno tempo fino al 29 ottobre 2026 per adeguarsi alle linee guida del Garante privacy sul tracciamento nelle email. Le regole riguardano pixel invisibili e tecnologie simili che rilevano apertura dei messaggi, dispositivo, indirizzo IP o interazioni.",
            "Quando il monitoraggio non è strettamente necessario, il consenso deve essere preventivo, libero, specifico e informato. L'informativa deve spiegare quali dati vengono raccolti, per quali finalità, per quanto tempo e con quali eventuali soggetti terzi vengono condivisi.",
            "La revoca deve risultare semplice quanto la concessione. Restano possibili eccezioni limitate per esigenze tecniche, di sicurezza o per comunicazioni di servizio, ma non possono diventare una giustificazione generica per attività promozionali o di profilazione.",
            "Il Garante ha inserito il tema tra le attività ispettive del secondo semestre 2026. Chi invia campagne dovrebbe quindi censire gli strumenti effettivamente attivi, aggiornare informative e meccanismi di consenso e documentare le scelte compiute.",
        ],
        "fonti": [{"url": "https://www.garanteprivacy.it/web/guest/home/docweb/-/docweb-display/docweb/10303585", "nome": "Garante per la protezione dei dati personali — linee guida e termine di adeguamento."}],
        "image_source": "privacy",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una professionista italiana davanti a un computer con simbolo di protezione dei dati; scena non documentaria.",
        "image_prompt": "Professionista italiana in ufficio davanti a email e simbolo astratto di privacy, bandiere italiana ed europea, volto visibile, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "musei-cagliari-apertura-notturna-9-ottobre-2026-orari",
        "titolo": "Musei di Cagliari aperti fino alle 23: l'ingresso parte dalle 14",
        "sommario": "L'apertura serale del 9 ottobre resta confermata, ma i lavori di accessibilità spostano l'apertura diurna. Biglietteria fino alle 22.",
        "categoria": "Cultura", "luogo": "Cagliari", "formato": "flash",
        "parole_chiave_titolo": ["Musei di Cagliari", "fino alle 23"],
        "dati_chiave": [
            {"valore": "14:00-23:00", "etichetta": "orario effettivo del 9 ottobre"},
            {"valore": "22:00", "etichetta": "chiusura della biglietteria"},
            {"valore": "dalle 19", "etichetta": "visite guidate serali"},
        ],
        "paragrafi": [
            "I Musei nazionali di Cagliari restano aperti venerdì 9 ottobre fino alle 23 per una serata speciale. L'orario effettivo della giornata parte però alle 14, e non alle 8:30 indicate nella scheda generale dell'evento, a causa dei lavori per migliorare l'accessibilità in corso dal 6 al 10 ottobre.",
            "La biglietteria chiude alle 22. Dalle 19 sono previste visite all'Ex Regio Museo e al Cannoniere piemontese; la pagina ufficiale indica accesso senza prenotazione, nei limiti della capienza.",
            "Il biglietto costa 10 euro nella tariffa intera e 5 euro nella ridotta, ferme restando le gratuità previste dalla normativa. Chi arriva per la sola fascia serale dovrebbe presentarsi con margine prima dell'ultima emissione dei biglietti.",
            "L'avviso dedicato al cambio d'orario prevale sulla pagina generale per l'apertura del mattino. Prima di partire è comunque utile controllare i canali del museo, soprattutto per eventuali modifiche legate ai lavori o alla sicurezza degli spazi.",
        ],
        "fonti": [
            {"url": "https://cultura.gov.it/index.php/evento/notte-del-9-ottobre-ai-musei-nazionali-di-cagliari", "nome": "Ministero della Cultura — apertura serale, biglietti e visite guidate."},
            {"url": "https://museinazionalicagliari.cultura.gov.it/attivita/cambio-orario-di-apertura-6-10-ottobre/", "nome": "Musei nazionali di Cagliari — apertura alle 14 dal 6 al 10 ottobre."},
        ],
        "image_source": "cagliari",
        "image_alt": "Illustrazione editoriale IA ultrarealistica dei Musei nazionali di Cagliari aperti al pubblico al tramonto; scena non documentaria.",
        "image_prompt": "Musei nazionali di Cagliari al tramonto con visitatori rivolti verso la camera e paesaggio sardo riconoscibile, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "concerto-benandanti-trieste-9-ottobre-2026-prenotazione",
        "titolo": "Benandanti a Palazzo Economo: concerto gratuito con prenotazione",
        "sommario": "A Trieste, dalle 20 alle 22, musica del Cinque e Seicento friulano con la Camerata Strumentale Italiana. Il posto va riservato online.",
        "categoria": "Cultura", "luogo": "Trieste", "formato": "flash",
        "parole_chiave_titolo": ["Palazzo Economo", "Concerto gratuito"],
        "dati_chiave": [
            {"valore": "20:00-22:00", "etichetta": "orario del concerto"},
            {"valore": "ingresso gratuito", "etichetta": "prenotazione obbligatoria"},
            {"valore": "9 ottobre", "etichetta": "appuntamento a Trieste"},
        ],
        "paragrafi": [
            "Palazzo Economo a Trieste ospita venerdì 9 ottobre, dalle 20 alle 22, il concerto L'età dei Benandanti. Viaggio nel Friuli del XVI e XVII secolo. L'ingresso è gratuito, ma la prenotazione è obbligatoria attraverso il collegamento Eventbrite indicato nella pagina del Ministero della Cultura.",
            "La Camerata Strumentale Italiana propone un percorso musicale ispirato al mondo raccontato dallo storico Carlo Ginzburg: credenze popolari, ritualità contadina e repertori dell'area friulana tra Cinquecento e Seicento.",
            "La sede è in piazza della Libertà 7, vicino alla stazione ferroviaria di Trieste. La prenotazione gratuita non garantisce l'accesso in caso di arrivo oltre l'orario indicato dagli organizzatori o di variazioni comunicate all'ultimo momento.",
            "Chi intende partecipare dovrebbe completare subito la registrazione e conservare la conferma sul telefono. Eventuali disponibilità residue o cambi di programma vanno controllati esclusivamente sulla pagina ufficiale dell'evento.",
        ],
        "fonti": [{"url": "https://cultura.gov.it/evento/trieste-palazzo-economo-venerdi-9-ottobre-h-2000-concerto-leta-dei-benandanti-viaggio-nel-friuli-del-xvi-e-xvii-secolo", "nome": "Ministero della Cultura — programma, sede e prenotazione del concerto."}],
        "image_source": "trieste",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di musicisti della Camerata Strumentale in concerto a Palazzo Economo a Trieste, con volti visibili; scena non documentaria.",
        "image_prompt": "Ensemble di musica antica a Palazzo Economo di Trieste, musicisti con volti visibili e strumenti storici plausibili, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "salvini-contributo-volontario-banche-assicurazioni-5-miliardi-2027",
        "titolo": "Salvini auspica 5 miliardi volontari da banche e assicurazioni",
        "sommario": "Il vicepremier indica la cifra per la manovra 2027, ma al momento si tratta di una proposta politica: importo e strumenti non sono stati approvati.",
        "categoria": "Politica", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["5 miliardi", "Banche e assicurazioni"],
        "dati_chiave": [
            {"valore": "5 miliardi", "etichetta": "obiettivo indicato da Salvini"},
            {"valore": "volontario", "etichetta": "metodo auspicato dal vicepremier"},
            {"valore": "manovra 2027", "etichetta": "provvedimento ancora da definire"},
        ],
        "paragrafi": [
            "Matteo Salvini ha detto di auspicare un contributo volontario complessivo da cinque miliardi di euro da parte di banche e assicurazioni per la manovra 2027. Il vicepremier ha escluso, nella sua formulazione, l'idea di una nuova tassa e ha parlato di dialogo con i settori interessati.",
            "La cifra non è una misura approvata né un importo già concordato. Il governo sta discutendo con banche e gruppi energetici possibili contributi al bilancio, ma modalità, platea e valore finale dovranno essere definiti nei documenti della manovra.",
            "Il confronto si inserisce in un quadro in cui il settore finanziario è già coinvolto da misure di bilancio con effetti pluriennali. Reuters ricorda che gli interventi esistenti erano stati stimati in circa 12 miliardi di euro fino al 2028.",
            "Per valutare l'impatto reale bisognerà attendere il testo ufficiale, le relazioni tecniche e l'iter parlamentare. Fino ad allora i cinque miliardi restano un obiettivo politico dichiarato, non una nuova entrata certa per lo Stato.",
        ],
        "fonti": [
            {"url": "https://www.ansa.it/sito/notizie/politica/2026/10/09/salvini-da-banche-assicurazioni-spero-contributo-volontario-di-5-miliardi_b34bf85d-5c9f-4f48-8f85-027ddbc40f5c.html", "nome": "ANSA — dichiarazione di Matteo Salvini sul contributo volontario."},
            {"url": "https://www.reuters.com/business/energy/italy-talking-banks-energy-groups-over-contribution-2027-budget-2026-10-08/", "nome": "Reuters — contesto dei colloqui sulla manovra 2027."},
        ],
        "image_source": "salvini", "public_figure": True, "sensitive_image": True,
        "image_alt": "Ritratto editoriale neutrale IA ultrarealistico con somiglianza sintetica di Matteo Salvini durante una dichiarazione istituzionale; scena non documentaria.",
        "image_prompt": "Neutral editorial portrait of Matteo Salvini, riconoscibile in posa istituzionale neutra durante una dichiarazione, bandiere italiana ed europea, somiglianza sintetica ultrarealistica, nessuna caricatura.",
    },
    {
        "slug": "meloni-senato-14-ottobre-2026-consiglio-europeo",
        "titolo": "Meloni in Senato il 14 ottobre prima del Consiglio europeo",
        "sommario": "Le comunicazioni della presidente del Consiglio sono fissate alle 9. L'intervento precede la riunione dei leader europei del 15 e 16 ottobre.",
        "categoria": "Politica", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["Meloni in Senato", "14 ottobre"],
        "dati_chiave": [
            {"valore": "14 ottobre", "etichetta": "comunicazioni al Senato"},
            {"valore": "ore 9:00", "etichetta": "inizio della seduta"},
            {"valore": "15-16 ottobre", "etichetta": "Consiglio europeo"},
        ],
        "paragrafi": [
            "La presidente del Consiglio Giorgia Meloni terrà mercoledì 14 ottobre alle 9 le comunicazioni al Senato in vista del Consiglio europeo. L'appuntamento è inserito nel calendario ufficiale di Palazzo Madama.",
            "Il dibattito parlamentare precede la riunione dei capi di Stato e di governo dell'Unione europea prevista per il 15 e 16 ottobre. Le comunicazioni servono a presentare la posizione italiana sui principali dossier in agenda e ad aprire il confronto con i gruppi.",
            "L'ordine preciso degli interventi, la durata della discussione e le eventuali risoluzioni saranno definiti secondo i lavori dell'Aula. Non è quindi corretto anticipare come già assunte decisioni che emergeranno soltanto nel corso della seduta.",
            "La diretta e i documenti parlamentari saranno disponibili attraverso i canali del Senato. Chi vuole seguire l'intervento può controllare il programma la mattina stessa, perché gli orari d'Aula possono subire aggiustamenti.",
        ],
        "fonti": [
            {"url": "https://www.senato.it/", "nome": "Senato della Repubblica — calendario delle comunicazioni del 14 ottobre."},
            {"url": "https://www.borsaitaliana.it/borsa/notizie/radiocor/economia/dettaglio/ue-comunicazioni-meloni-in-aula-senato-14-ottobre-su-consiglio-europeo-nRC_30092026_1822_663126346.html", "nome": "Il Sole 24 Ore Radiocor — orario e contesto dell'intervento."},
        ],
        "image_source": "meloni", "public_figure": True, "sensitive_image": True,
        "image_alt": "Ritratto editoriale neutrale IA ultrarealistico con somiglianza sintetica di Giorgia Meloni nell'Aula del Senato; scena non documentaria.",
        "image_prompt": "Neutral editorial portrait of Giorgia Meloni, riconoscibile nell'Aula del Senato italiano in posa istituzionale neutra, somiglianza sintetica ultrarealistica, nessuna caricatura.",
    },
    {
        "slug": "data-center-italia-investimenti-potenziali-37-miliardi-2036",
        "titolo": "Data center, IDA stima investimenti potenziali per 37 miliardi",
        "sommario": "La previsione dell'associazione di settore copre il periodo 2026-2036. Non sono fondi già impegnati: rete elettrica, autorizzazioni e siti restano decisivi.",
        "categoria": "Tecnologia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Data center", "37 miliardi potenziali"],
        "dati_chiave": [
            {"valore": "36,9 miliardi", "etichetta": "investimenti potenziali in dieci anni"},
            {"valore": "26.000", "etichetta": "occupati equivalenti stimati"},
            {"valore": "2 GW", "etichetta": "capacità commerciale possibile al 2031"},
        ],
        "paragrafi": [
            "L'Italian Data Center Association stima per l'Italia fino a 36,9 miliardi di euro di investimenti infrastrutturali potenziali tra il 2026 e il 2036. Il dato è stato presentato a Roma durante il Data Center Symposium e proviene dalla ricerca di mercato 2026 dell'associazione di settore.",
            "Secondo lo studio, il comparto potrebbe generare ogni anno 3,87 miliardi di valore aggiunto operativo diretto e sostenere circa 26.000 occupati equivalenti a tempo pieno. Nel 2025 la capacità installata complessiva viene indicata in 760 megawatt, di cui 460 commerciali.",
            "Lo scenario più espansivo porta la capacità commerciale a circa 2 gigawatt entro il 2031. Si tratta però di una proiezione, non di cantieri già finanziati o autorizzati.",
            "La stessa analisi lega la crescita alla disponibilità di energia e connessioni di rete, alla rapidità delle autorizzazioni e all'accesso a siti idonei. Per questo la cifra dei 37 miliardi va letta come potenziale condizionato, non come investimento certo.",
        ],
        "fonti": [
            {"url": "https://italiandatacenter.com/en/data-center-symposium-2026-event-programme-12568/", "nome": "Italian Data Center Association — presentazione della ricerca 2026."},
            {"url": "https://www.ansa.it/ansacom/notizie/economia/italiandatacenterassociation/2026/10/08/data-center-in-italia-37-miliardi-di-investimenti-potenziali-in-dieci-anni_ba2322d2-cb9f-42fc-bfad-98c074b48f2d.html", "nome": "ANSAcom — valori e condizioni della stima IDA."},
        ],
        "image_source": "data_center",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di tecnici italiani in un data center moderno, con volti visibili; scena non documentaria.",
        "image_prompt": "Data center moderno in Italia con due tecnici rivolti verso la camera, infrastruttura server realistica, illustrazione editoriale ultrarealistica.",
    },
]


def main() -> None:
    append_name_phrases()
    base = datetime.now(ROME).replace(microsecond=0)
    minute_offsets = (0, 7, 16, 27, 39, 51, 64, 78, 92, 108)
    images = []
    written = []
    for article, minutes in zip(ARTICLES, minute_offsets):
        image = make_image(article)
        slug = site.write_article(article, image, VERSION)
        published = base - timedelta(minutes=minutes)
        set_published(slug, published)
        article["published"] = published.isoformat(timespec="seconds")
        image["article"] = f"/notizie/{slug}.html"
        images.append(image)
        written.append(article)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    new_urls = {row["article"] for row in images}
    registry["items"] = images + [row for row in registry.get("items", []) if row.get("article") not in new_urls]
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces(written, f"/notizie/{written[0]['slug']}.html", VERSION, update_manifest=False)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION,
        "currentVersion": VERSION,
        "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": f"italia-politica-v{VERSION}",
        "date": base.date().isoformat(),
        "release_date": base.date().isoformat(),
        "updated_at": base.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
