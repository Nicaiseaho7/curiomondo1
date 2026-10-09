#!/usr/bin/env python3
"""Release v816: mobilità, scadenze, cultura e sport del 9 ottobre 2026."""
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

VERSION = 816
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"

IMAGE_SOURCES = {
    "pisa_empoli": GENERATED / "exec-a2c7555f-e859-4250-ac0c-28d5162e3760.png",
    "domestici": GENERATED / "exec-7d5a728e-a7b8-489c-92c4-f8c2a64004e5.png",
    "scoperta": GENERATED / "exec-e1b74d6b-f084-4405-b53d-ee295ad1bf3e.png",
    "vive": GENERATED / "exec-2f6f81be-b846-426f-b629-d4c3ba39db1a.png",
    "firenze": GENERATED / "exec-1133ffb8-3693-4246-a73d-bea0437462ad.png",
    "carta": GENERATED / "exec-e42a1d7e-822b-42be-8211-9534d1a65f55.png",
    "basket": GENERATED / "exec-b75ae56d-05ae-4018-8357-9105700c6a3f.png",
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
    return {
        "key": f"{article['slug']}-v{VERSION}",
        "alt": article.pop("image_alt"),
        "prompt": article.pop("image_prompt"),
        "variants": make_variants(IMAGE_SOURCES[article.pop("image_source")], article["slug"]),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": False,
        "weatherMap": False,
        "reenactedEvent": False,
    }


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
    if slug == "serie-a-basket-10-11-ottobre-2026-orari-dirette-biglietti":
        for node in doc.xpath('//main//div[contains(concat(" ",normalize-space(@class)," ")," badge ")][1]'):
            node.text = "Sport"
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )


def correct_olimpia_time() -> None:
    paths = [
        ROOT / "notizie/olimpia-milano-treviso-11-ottobre-2026-biglietti-inclusione.html",
        ROOT / "tools/publish_eventi_avvisi_20261009_v815.py",
        ROOT / "index.html",
        ROOT / "notizie/index.html",
        ROOT / "categorie/sport/index.html",
        ROOT / "categorie/italia/index.html",
        ROOT / "feed.xml",
        ROOT / "assets/data/home-feed-v210.json",
        ROOT / "assets/data/search-index-v210.json",
    ]
    replacements = (
        ("Olimpia Milano-Treviso domenica: partita alle 16 e iniziativa inclusiva",
         "Olimpia Milano-Treviso domenica: partita alle 14 e iniziativa inclusiva"),
        ("Olimpia Milano-Treviso si gioca domenica 11 ottobre 2026 alle 16 all'Unipol Forum",
         "Olimpia Milano-Treviso si gioca domenica 11 ottobre 2026 alle 14 all'Unipol Forum"),
        ('{"valore": "ore 16", "etichetta": "inizio della partita"}',
         '{"valore": "ore 14", "etichetta": "inizio della partita"}'),
        ('<strong>ore 16</strong>', '<strong>ore 14</strong>'),
    )
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for old, new in replacements:
            text = text.replace(old, new)
        path.write_text(text, encoding="utf-8")


ARTICLES = [
    {
        "slug": "treni-pisa-empoli-sospesi-9-12-ottobre-2026-cancellazioni",
        "titolo": "Treni sospesi tra Pisa ed Empoli: cancellazioni fino al 12 ottobre",
        "sommario": "I lavori interrompono la linea dalle 2:15 del 9 ottobre alle 2:15 del 12. Cambiano regionali, Frecciargento e Intercity Notte.",
        "categoria": "Cronaca", "luogo": "Toscana", "formato": "flash",
        "parole_chiave_titolo": ["Pisa ed Empoli", "cancellazioni"],
        "dati_chiave": [
            {"valore": "9-12 ottobre", "etichetta": "interruzione della linea"},
            {"valore": "02:15", "etichetta": "inizio e fine dei lavori"},
            {"valore": "6 Frecciargento", "etichetta": "coinvolti da cancellazioni o deviazioni"},
        ],
        "paragrafi": [
            "La circolazione ferroviaria è sospesa tra Pisa Centrale ed Empoli dalle 2:15 di venerdì 9 ottobre alle 2:15 di lunedì 12 ottobre 2026. RFI indica lavori di potenziamento infrastrutturale che modificano collegamenti regionali e a lunga percorrenza.",
            "I Frecciargento 8551 e 8583 Genova-Roma sono cancellati il 9, 10 e 12 ottobre; il 8591 sulla stessa relazione è cancellato negli stessi giorni, mentre l'11 segue un itinerario alternativo via Pisa, Livorno e Grosseto. Anche i 8556 e 8596 Roma-Genova subiscono cancellazioni nelle giornate indicate dall'avviso.",
            "Nelle notti tra l'8 e il 10 ottobre l'Intercity Notte 796 Salerno-Torino viene deviato via Firenze, Prato, Bologna e Piacenza. Non effettua diverse fermate lungo la costa ligure e toscana, comprese Pisa Centrale e Genova Piazza Principe.",
            "I regionali e regionali veloci sono cancellati totalmente o parzialmente fra Firenze Santa Maria Novella e Pisa Centrale. È prevista un'offerta alternativa attraverso Empoli, Lucca e Grosseto, ma durata e coincidenze possono essere diverse rispetto al viaggio originario.",
            "I sistemi di vendita Trenitalia risultano aggiornati. Prima della partenza è necessario ricontrollare il numero del treno e l'intero itinerario, soprattutto per viaggi con coincidenze o arrivo in aeroporto e porto.",
        ],
        "fonti": [{"url": "https://www.rfi.it/it/news-e-media/infomobilita/avvisi/2026/10/9/linee-firenze---empoli---pisa---livorno--firenze---piombino--fir.html", "nome": "Rete Ferroviaria Italiana — interruzione Pisa-Empoli e modifiche ai treni."}],
        "image_source": "pisa_empoli",
        "image_alt": "Illustrazione editoriale IA ultrarealistica dei lavori ferroviari tra Pisa ed Empoli con treno e bus sostitutivo; scena non documentaria.",
        "image_prompt": "Railway works between Pisa and Empoli, Italian regional train, maintenance crews and replacement bus, ultra-realistic editorial illustration, authentic railway identity, no text overlay.",
    },
    {
        "slug": "contributi-colf-badanti-scadenza-10-ottobre-2026-pagopa",
        "titolo": "Contributi colf e badanti, pagamento entro il 10 ottobre: cambia l’avviso",
        "sommario": "Scade sabato il versamento INPS del terzo trimestre. Per molti datori sotto i 76 anni il bollettino non arriva più per posta.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["colf e badanti", "10 ottobre"],
        "dati_chiave": [
            {"valore": "10 ottobre", "etichetta": "scadenza del versamento"},
            {"valore": "3° trimestre", "etichetta": "periodo contributivo"},
            {"valore": "76 anni", "etichetta": "soglia per gli avvisi cartacei"},
        ],
        "paragrafi": [
            "I datori di lavoro domestico hanno tempo fino a sabato 10 ottobre 2026 per pagare i contributi INPS relativi al terzo trimestre. Il periodo utile è iniziato il 1° ottobre e riguarda rapporti come colf, badanti e assistenti familiari regolarmente dichiarati.",
            "Dal 2026 i datori con meno di 76 anni non ricevono più a domicilio bollettini e avvisi pagoPA in formato cartaceo. Il pagamento deve essere gestito attraverso i canali digitali, in particolare il servizio Lavoratori domestici del Portale dei pagamenti INPS.",
            "Nel portale il bollettino precompilato dovrebbe comparire nel carrello durante il periodo di versamento. Se non è visibile, l'INPS indica di generarlo nella sezione Calcolo contributi selezionando trimestre 3 e anno 2026.",
            "Il pagamento può essere completato online tramite pagoPA oppure stampando l'avviso per utilizzare uno dei canali abilitati. Prima di confermare vanno verificati rapporto di lavoro, periodo e importo, evitando di usare collegamenti ricevuti da mittenti non riconosciuti.",
            "Nell'area MyINPS è disponibile anche una video guida personalizzata per alcuni datori che risultano in arretrato. Gli avvisi possono comparire nel Centro notifiche, nell'app INPS Mobile e nell'app IO quando i contatti e i consensi sono aggiornati.",
        ],
        "fonti": [{"url": "https://www.inps.it/it/it/inps-comunica/notizie/dettaglio-news-page.news.2026.10.lavoratori-domestici-contributi-terzo-trimestre-e-nuova-video-guida.html", "nome": "INPS — scadenza, pagamento digitale e video guida per i contributi domestici."}],
        "image_source": "domestici",
        "image_alt": "Illustrazione editoriale IA ultrarealistica del pagamento digitale dei contributi per il lavoro domestico tramite pagoPA; scena non documentaria.",
        "image_prompt": "Italian household employer paying domestic worker contributions through pagoPA on a laptop, ultra-realistic editorial home-office illustration, no personal data or text overlay.",
    },
    {
        "slug": "scoperta-imprenditoriale-ii-domande-sospese-8-ottobre-2026",
        "titolo": "Scoperta imprenditoriale II, domande sospese: risorse esaurite",
        "sommario": "Il Mimit ha fermato dall'8 ottobre le nuove richieste di agevolazione. Il decreto ufficiale precede il relativo comunicato in Gazzetta Ufficiale.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Scoperta imprenditoriale II", "risorse esaurite"],
        "dati_chiave": [
            {"valore": "8 ottobre", "etichetta": "decorrenza della sospensione"},
            {"valore": "risorse esaurite", "etichetta": "motivo del provvedimento"},
            {"valore": "nuove domande", "etichetta": "invii non più disponibili"},
        ],
        "paragrafi": [
            "Il Ministero delle Imprese e del Made in Italy ha sospeso dall'8 ottobre 2026 la presentazione delle domande per Scoperta imprenditoriale II. Il decreto direttoriale motiva il provvedimento con l'esaurimento delle risorse finanziarie disponibili.",
            "La sospensione riguarda i nuovi invii e non equivale automaticamente al rigetto delle domande già trasmesse. Imprese e consulenti che hanno completato la procedura devono fare riferimento alle comunicazioni ricevute e alla pagina ufficiale della misura per lo stato della pratica.",
            "Scoperta imprenditoriale II sostiene progetti di ricerca industriale e sviluppo sperimentale nelle regioni interessate dal programma. La chiusura anticipata dello sportello indica che le richieste hanno raggiunto la disponibilità prevista dal finanziamento.",
            "Il Mimit segnala che il comunicato relativo al decreto è in corso di pubblicazione nella Gazzetta Ufficiale. Eventuali riaperture, rifinanziamenti o scorrimenti richiederebbero un nuovo atto: non vanno considerati disponibili finché non sono annunciati ufficialmente.",
            "Chi stava preparando la domanda dovrebbe conservare documentazione tecnica e preventivi, ma evitare invii attraverso siti o intermediari che promettono accessi riservati. L'unico aggiornamento valido resta quello pubblicato dal Ministero o dal soggetto gestore indicato dalla misura.",
        ],
        "fonti": [{"url": "https://www.mimit.gov.it/it/normativa/decreti-direttoriali/decreto-direttoriale-8-ottobre-2026-scoperta-imprenditoriale-ii-sospensione-dei-termini-di-presentazione-delle-domande-di-agevolazione", "nome": "Mimit — decreto di sospensione delle domande per Scoperta imprenditoriale II."}],
        "image_source": "scoperta",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una piccola impresa innovativa che verifica una domanda di agevolazione sospesa; scena non documentaria.",
        "image_prompt": "Italian startup founders reviewing a closed innovation funding application beside a technical prototype, ultra-realistic editorial workshop illustration, no readable data or text overlay.",
    },
    {
        "slug": "palazzo-venezia-vittoriano-chiusi-9-ottobre-2026-avviso",
        "titolo": "Palazzo Venezia chiuso oggi, stop temporaneo anche al Vittoriano",
        "sommario": "Il museo resta chiuso per l'intera giornata del 9 ottobre. Al Vittoriano l'accesso è sospeso temporaneamente dalle 9:30.",
        "categoria": "Cultura", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["Palazzo Venezia", "Vittoriano"],
        "dati_chiave": [
            {"valore": "9 ottobre", "etichetta": "chiusura di Palazzo Venezia"},
            {"valore": "dalle 9:30", "etichetta": "stop temporaneo al Vittoriano"},
            {"valore": "2 siti", "etichetta": "coinvolti nel centro di Roma"},
        ],
        "paragrafi": [
            "Il Museo di Palazzo Venezia resta chiuso al pubblico oggi, venerdì 9 ottobre 2026. L'avviso dell'istituto VIVE comprende le giornate dell'8 e del 9 ottobre e interessa chi aveva programmato una visita nel centro di Roma.",
            "Nella stessa mattina è prevista anche una chiusura temporanea del Vittoriano a partire dalle 9:30. L'avviso non indica nella pagina riepilogativa un orario certo di riapertura, quindi la visita non dovrebbe essere organizzata facendo affidamento su un rientro immediato.",
            "Palazzo Venezia e Vittoriano appartengono allo stesso sistema museale, ma hanno accessi e percorsi distinti. La chiusura di uno spazio non autorizza a presumere che terrazze, museo e aree monumentali seguano automaticamente lo stesso orario.",
            "Chi possiede già un biglietto o una prenotazione dovrebbe controllare le condizioni del circuito ufficiale e le comunicazioni ricevute. Per informazioni operative è preferibile usare i contatti VIVE, evitando rivenditori o pagine non collegate al museo.",
            "Gli avvisi possono essere aggiornati nel corso della giornata. Prima di raggiungere piazza Venezia è utile consultare nuovamente la pagina istituzionale, soprattutto se la visita è inserita in un itinerario con orari stretti.",
        ],
        "fonti": [{"url": "https://vive.cultura.gov.it/it/avvisi", "nome": "VIVE — avvisi ufficiali di chiusura per Palazzo Venezia e Vittoriano."}],
        "image_source": "vive",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di Palazzo Venezia e del Vittoriano durante la chiusura temporanea; scena non documentaria.",
        "image_prompt": "Palazzo Venezia and Vittoriano in Rome during a temporary public closure, calm barriers and visitors, ultra-realistic editorial illustration, accurate architecture, no text overlay.",
    },
    {
        "slug": "firenze-globale-mostra-francesco-carletti-9-ottobre-2026",
        "titolo": "Firenze globale apre oggi: 69 opere raccontano il viaggio di Carletti",
        "sommario": "La mostra alla Biblioteca Medicea Laurenziana segue la circumnavigazione del mercante fiorentino tra il 1594 e il 1602. Aperta fino al 9 gennaio.",
        "categoria": "Cultura", "luogo": "Firenze", "formato": "flash",
        "parole_chiave_titolo": ["Firenze globale", "69 opere"],
        "dati_chiave": [
            {"valore": "69 opere", "etichetta": "nel percorso espositivo"},
            {"valore": "9 ottobre-9 gennaio", "etichetta": "periodo di apertura"},
            {"valore": "1594-1602", "etichetta": "anni del viaggio di Carletti"},
        ],
        "paragrafi": [
            "Apre oggi, 9 ottobre 2026, alla Biblioteca Medicea Laurenziana la mostra Firenze globale. Il mondo di Francesco Carletti, dedicata al mercante fiorentino che compì una circumnavigazione tra il 1594 e il 1602. L'esposizione resta visitabile fino al 9 gennaio 2027.",
            "Il percorso riunisce 69 opere fra manoscritti, mappe, stampe, strumenti di navigazione, manufatti, tessuti e libri. Il viaggio di Carletti collega Americhe, Giappone, Cina e India e diventa una chiave per osservare le relazioni commerciali e culturali intorno al 1600.",
            "La mostra affronta anche le contraddizioni dell'espansione europea, compreso il coinvolgimento del mercante nella tratta degli schiavi. Il racconto non presenta quindi la circumnavigazione soltanto come avventura, ma la inserisce nella storia economica e umana della prima globalizzazione.",
            "L'iniziativa nasce dalla collaborazione tra Biblioteca Medicea Laurenziana, Istituto Universitario Europeo, Stanford University, Syracuse University e University of Warwick. La sede è in piazza San Lorenzo 9, nel centro storico di Firenze.",
            "L'apertura ordinaria indicata è dal lunedì al venerdì, dalle 10 alle 13:30; sabato, domenica e festivi la mostra è chiusa. La prenotazione è consigliata e può essere effettuata attraverso i riferimenti pubblicati nella pagina del Ministero della Cultura.",
        ],
        "fonti": [{"url": "https://cultura.gov.it/evento/mostra-firenze-globale-il-mondo-di-francesco-carletti-c-1573-1636", "nome": "Ministero della Cultura — programma, opere, sede e orari di Firenze globale."}],
        "image_source": "firenze",
        "image_alt": "Illustrazione editoriale IA ultrarealistica della mostra Firenze globale con mappe e strumenti di navigazione alla Biblioteca Medicea Laurenziana; scena non documentaria.",
        "image_prompt": "Firenze globale exhibition at Biblioteca Medicea Laurenziana with historic maps, manuscripts and navigation instruments, ultra-realistic museum editorial illustration, no text overlay.",
    },
    {
        "slug": "carta-dedicata-a-te-negozi-domande-9-ottobre-2026-sconto-15",
        "titolo": "Carta Dedicata a Te, adesioni dei negozi entro oggi: previsto lo sconto del 15%",
        "sommario": "Il termine del 9 ottobre riguarda esercizi commerciali e associazioni. La misura per i beneficiari parte il 4 novembre.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["adesioni dei negozi", "sconto del 15%"],
        "dati_chiave": [
            {"valore": "9 ottobre", "etichetta": "termine dell'avviso pubblico"},
            {"valore": "15%", "etichetta": "sconto indicato per la grande distribuzione"},
            {"valore": "4 novembre", "etichetta": "inizio della misura"},
        ],
        "paragrafi": [
            "Scade oggi, 9 ottobre 2026, il termine dell'avviso pubblico per la partecipazione di esercizi commerciali e associazioni di categoria alla Carta Dedicata a Te 2026-2027. La scadenza riguarda gli operatori, non una domanda che le famiglie beneficiarie devono presentare entro oggi.",
            "Il Ministero dell'Agricoltura ha pubblicato modelli distinti per gli esercizi e per le associazioni. Chi intende aderire deve utilizzare la documentazione collegata all'avviso e verificare requisiti, modalità di invio e sottoscrizione prima della scadenza.",
            "La misura di sostegno per i possessori della carta parte il 4 novembre 2026. La pagina ministeriale indica che la grande distribuzione organizzata garantisce uno sconto del 15% sugli acquisti, cumulabile con le altre offerte proposte.",
            "Sono pubblicate convenzioni con Federdistribuzione, ANCD Conad, ANCC-Coop e Lidl. La presenza di una catena nell'elenco non significa necessariamente che ogni prodotto o servizio sia ammesso: restano valide le condizioni della carta e della singola convenzione.",
            "Per i beneficiari non cambia il meccanismo di individuazione automatica già comunicato da INPS e Comuni. Un ulteriore termine operativo riguarda il consolidamento delle liste comunali, indicato entro il 13 ottobre alle 14, ma non richiede una domanda diretta delle famiglie.",
        ],
        "fonti": [{"url": "https://www.masaf.gov.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/25162", "nome": "Masaf — avviso per gli esercizi, avvio della misura e convenzioni commerciali."}],
        "image_source": "carta",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un acquisto alimentare con carta di pagamento in un supermercato italiano; scena non documentaria.",
        "image_prompt": "Italian grocery store checkout with customer using a payment card for basic food purchases, ultra-realistic editorial illustration, no personal data or invented logos, no text overlay.",
    },
    {
        "slug": "serie-a-basket-10-11-ottobre-2026-orari-dirette-biglietti",
        "titolo": "Serie A basket, partite del weekend: orari, dirette e biglietti",
        "sommario": "La terza giornata parte sabato con Udine-Trento e Varese-Trieste. Domenica sette incontri, compresi Milano-Treviso e il derby romano.",
        "categoria": "Sport", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Serie A basket", "orari"],
        "dati_chiave": [
            {"valore": "9 partite", "etichetta": "nel programma del weekend"},
            {"valore": "2 sabato", "etichetta": "gli anticipi del 10 ottobre"},
            {"valore": "7 domenica", "etichetta": "le gare dell'11 ottobre"},
        ],
        "paragrafi": [
            "La terza giornata della Serie A di basket 2026-2027 si apre sabato 10 ottobre con Udine-Trento alle 18 e Varese-Trieste alle 18:30. Entrambe le partite risultano disponibili su LBATV, con collegamenti ai biglietti nella pagina ufficiale della Lega Basket.",
            "Domenica 11 ottobre il programma parte alle 14 con Olimpia Milano-Treviso, trasmessa su LBATV, Sky Sport Basket e Sky Sport Uno. Alle 15 si giocano Cantù-Napoli e Reggio Emilia-Tortona, mentre Scafati-Verona è fissata alle 16.",
            "Il derby Maxima Roma-BC Roma comincia alle 16:15 ed è indicato su LBATV e sui due canali Sky. Venezia-Virtus Bologna chiude il programma alle 17; anche questa gara è disponibile attraverso il servizio streaming della Lega.",
            "Orari e piattaforme possono subire variazioni dell'ultimo momento. La pagina LBA permette di aprire la scheda della singola partita, verificare il palazzetto e raggiungere la biglietteria collegata dalla squadra organizzatrice.",
            "Per le dirette è necessario controllare le condizioni del proprio abbonamento a LBATV o Sky. Chi va al palazzetto dovrebbe verificare apertura porte, settore e regole di accesso sui canali ufficiali del club, senza affidarsi a rivendite non autorizzate.",
        ],
        "fonti": [{"url": "https://www.legabasket.it/calendario/1/serie-a", "nome": "Lega Basket Serie A — calendario, orari, dirette e collegamenti ai biglietti."}],
        "image_source": "basket",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un palazzetto italiano con pallone, biglietto e telecamera per le dirette della Serie A basket; scena non documentaria.",
        "image_prompt": "Italian Serie A basketball arena with professional ball, ticket and broadcast camera, ultra-realistic editorial sports illustration, no invented team logos or text overlay.",
    },
]


def main() -> None:
    correct_olimpia_time()
    base = datetime.now(ROME).replace(microsecond=0)
    images = []
    written = []
    for index, article in enumerate(ARTICLES):
        image = make_image(article)
        slug = site.write_article(article, image, VERSION)
        set_published(slug, base - timedelta(seconds=index))
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
        "last_update": f"servizi-scadenze-cultura-sport-v{VERSION}",
        "date": base.date().isoformat(),
        "release_date": base.date().isoformat(),
        "updated_at": base.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
