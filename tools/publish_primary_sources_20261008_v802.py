#!/usr/bin/env python3
"""Pubblica cinque notizie dell'8 ottobre 2026 da fonti primarie, senza manifest."""
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

VERSION = 802
ROME = ZoneInfo("Europe/Rome")
CAPTION = site.CAPTION
GENERATED = ROOT.parent / "generated_images"

IMAGES = {
    "sna": GENERATED / "exec-91667fd1-eb7a-43b4-ba78-0bb6be538556.png",
    "windows": GENERATED / "exec-50d916af-063f-44e7-b0fc-3c6506e9edd8.png",
    "artico": GENERATED / "exec-4b2300f1-7f95-425c-863c-70c7ad381644.png",
    "h5": GENERATED / "exec-fe4bc199-c65d-4e8e-8a8b-052a36914140.png",
    "fifa": GENERATED / "exec-326a5462-1acf-40dd-8085-1614858e51cf.png",
}


def variants(source: Path, slug: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 16 / 9
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = max(0, (image.height - height) // 2)
        image = image.crop((0, top, image.width, top + height))

    output = ROOT / "assets/images/editorial-auto"
    result = []
    for width in (480, 800, 1200):
        height = round(width / ratio)
        path = output / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, height), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=90, method=6
        )
        result.append({
            "w": width,
            "h": height,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return result


def image_record(slug: str, source: Path, alt: str, prompt: str, *, public=False) -> dict:
    record = {
        "key": f"{slug}-v{VERSION}",
        "alt": alt,
        "prompt": prompt,
        "variants": variants(source, slug),
        "disclosure": CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": False,
        "weatherMap": False,
    }
    if public:
        record["syntheticLikeness"] = "public-figure"
    return record


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


def register_image_once(image: dict, slug: str) -> None:
    path = ROOT / "assets/data/editorial-images-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    article_path = f"/notizie/{slug}.html"
    data["items"] = [
        item for item in data.get("items", [])
        if item.get("key") != image["key"] and item.get("article") != article_path
    ]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.register_image(image, slug, VERSION)


def main() -> None:
    now = datetime.now(ROME).replace(second=0, microsecond=0)
    articles = [
        {
            "slug": "concorso-sna-quesito-errato-neutralizzato-punto-tutti-08-10-2026",
            "titolo": "Concorso SNA, quesito errato neutralizzato: un punto a tutti",
            "sommario": (
                "L'anomalia ha riguardato una delle 60 domande della preselettiva per dirigenti. "
                "La commissione conferma la validità degli altri 59 quesiti e della graduatoria."
            ),
            "luogo": "Roma",
            "categoria": "Italia",
            "formato": "flash",
            "parole_chiave_titolo": ["quesito errato", "un punto a tutti"],
            "dati_chiave": [
                {"icona": "◆", "valore": "60", "etichetta": "quesiti nella prova"},
                {"icona": "▲", "valore": "59", "etichetta": "domande confermate corrette"},
                {"icona": "●", "valore": "1 punto", "etichetta": "assegnato a ogni candidato"},
            ],
            "paragrafi": [
                "La Scuola nazionale dell'amministrazione ha neutralizzato uno dei 60 quesiti della prova preselettiva del 6 ottobre per il dodicesimo corso-concorso da dirigente pubblico. A tutti i candidati sarà attribuito un punto per quella domanda, anche in caso di risposta errata o non data.",
                "Il comunicato pubblicato dalla SNA alle 21 del 7 ottobre descrive un'anomalia tecnica nella domanda di diritto amministrativo relativa all'articolo 10-bis della legge 241 del 1990. Il quesito era stato caricato senza il testo corretto e il sistema mostrava, accanto alle opzioni di risposta, il testo incongruente di un'altra domanda.",
                "Secondo le verifiche effettuate da Formez su un campione significativo delle prove, gli altri 59 quesiti risultano esatti. La commissione esaminatrice ha quindi stabilito nel verbale numero 5 che la domanda difettosa non era valutabile, senza annullare l'intera preselettiva.",
                "La soluzione uniforme tutela i candidati dall'effetto dell'errore, ma non modifica l'ordine della graduatoria: tutti ricevono lo stesso punto e la posizione continua a dipendere dalle risposte alle altre 59 domande. L'ammissione alle prove scritte avviene infatti in base alla posizione raggiunta, come previsto dal bando.",
                "Il punteggio della preselettiva serve soltanto a selezionare chi accede alla fase successiva. La SNA precisa che non concorre al punteggio finale di merito del corso-concorso, perciò il punto assegnato automaticamente non produce un vantaggio nella graduatoria conclusiva.",
                "Il passaggio successivo sarà la pubblicazione degli esiti della preselezione secondo il calendario della procedura. Il comunicato non segnala errori nelle restanti domande né dispone la ripetizione della prova.",
            ],
            "fonti": [{
                "url": "https://sna.gov.it/home/2026/10/07/comunicato-ii-12-corso-concorso-per-dirigenti/",
                "nome": "Scuola Nazionale dell'Amministrazione — comunicato ufficiale del 7 ottobre 2026, ore 21:00.",
            }],
            "image": image_record(
                "concorso-sna-quesito-errato-neutralizzato-punto-tutti-08-10-2026", IMAGES["sna"],
                "Illustrazione editoriale IA di candidati e personale durante una prova informatica in un'aula pubblica; scena non documentaria.",
                "Aula italiana per concorso pubblico con candidati ai computer e vigilante che controlla una postazione con interfaccia incompleta; fotografia editoriale fotorealistica, volti visibili, nessun testo leggibile.",
            ),
            "published": now - timedelta(minutes=4),
        },
        {
            "slug": "windows-11-ricerca-azioni-rapide-widget-batteria-08-10-2026",
            "titolo": "Windows 11 prova ricerca con azioni rapide e widget batteria",
            "sommario": (
                "Le novità arrivano nei canali Insider Beta ed Experimental. Dalla ricerca si potranno "
                "cambiare luminosità, Bluetooth e modalità scura senza aprire altre schermate."
            ),
            "luogo": "Redmond",
            "categoria": "Tecnologia",
            "formato": "flash",
            "parole_chiave_titolo": ["azioni rapide", "widget batteria"],
            "dati_chiave": [
                {"icona": "◆", "valore": "5 build", "etichetta": "pubblicate per gli Insider"},
                {"icona": "▲", "valore": "2 canali", "etichetta": "Beta ed Experimental"},
                {"icona": "●", "valore": "1 widget", "etichetta": "per PC e periferiche"},
            ],
            "paragrafi": [
                "Microsoft ha iniziato a distribuire agli iscritti al programma Windows Insider una nuova ricerca di Windows 11 capace di eseguire azioni rapide direttamente dai risultati. Nello stesso ciclo di test arriva un widget che riunisce lo stato della batteria del computer e delle periferiche collegate.",
                "La ricerca, costruita su WinUI 3, viene provata nei canali Experimental ed Experimental 26H1. Microsoft la descrive come più veloce ed efficiente, con risultati più facili da esaminare e una migliore comprensione di errori di battitura e sinonimi.",
                "Le azioni integrate consentono di attivare la modalità scura o il Bluetooth, regolare la luminosità, silenziare il dispositivo e disporre le finestre senza passare dalle relative pagine delle Impostazioni. La funzione riduce quindi i passaggi necessari per i comandi di uso frequente.",
                "Il widget Battery Status, per ora destinato al canale Experimental, mostra in un solo riquadro la carica del PC e quella degli accessori compatibili. Può essere aggiunto dalla bacheca Widget e punta a evitare il controllo separato di cuffie, mouse e altri dispositivi.",
                "Il rilascio del 7 ottobre comprende le build 26220.9606 e 26340.9616, più le versioni 28020.3172 e 28120.3181 per 26H1 e la 29683.1000 per piattaforme future. I numeri distinguono rami e canali di prova: non indicano che tutte le funzioni arriveranno contemporaneamente a ogni utente.",
                "Essere nel programma Insider significa ricevere software preliminare che può cambiare prima del rilascio stabile. Microsoft prevede ulteriori regolazioni nelle prossime settimane e non ha indicato una data per la distribuzione generale delle due novità.",
            ],
            "fonti": [{
                "url": "https://blogs.windows.com/windows-insider/2026/10/07/announcing-new-builds-for-7-october-2026/",
                "nome": "Microsoft Windows Insider Blog — annuncio delle build e delle nuove funzioni del 7 ottobre 2026.",
            }],
            "image": image_record(
                "windows-11-ricerca-azioni-rapide-widget-batteria-08-10-2026", IMAGES["windows"],
                "Illustrazione editoriale IA di un tester davanti a un portatile con Windows 11 e indicatori di batteria; scena non documentaria.",
                "Tester in home office italiano accanto a Microsoft Surface con Windows 11 Search e indicatori batteria iconici; fotografia tecnologica fotorealistica, volto visibile, nessun testo editoriale.",
            ),
            "published": now - timedelta(minutes=3),
        },
        {
            "slug": "ghiaccio-artico-minimo-2026-4-6-milioni-km2-08-10-2026",
            "titolo": "Ghiaccio artico a 4,6 milioni di km², decimo minimo più basso",
            "sommario": (
                "Il minimo annuale è stato raggiunto il 12 settembre e pareggia 2008, 2010 e 2025. "
                "Tutte le ultime 20 estati rientrano fra le 20 meno estese dell'era satellitare."
            ),
            "luogo": "Artico",
            "categoria": "Ambiente",
            "formato": "standard",
            "parole_chiave_titolo": ["4,6 milioni di km²", "decimo minimo"],
            "dati_chiave": [
                {"icona": "◆", "valore": "4,6 mln km²", "etichetta": "estensione il 12 settembre"},
                {"icona": "▲", "valore": "10°", "etichetta": "minimo più basso dal 1978"},
                {"icona": "●", "valore": "20 estati", "etichetta": "consecutive tra le 20 più basse"},
            ],
            "paragrafi": [
                "Il ghiaccio marino artico ha raggiunto il minimo annuale il 12 settembre 2026, quando copriva circa 4,6 milioni di chilometri quadrati. La stima congiunta di NASA e National Snow and Ice Data Center colloca l'anno al decimo posto fra i minimi meno estesi osservati dai satelliti.",
                "Il valore è statisticamente alla pari con quelli del 2008, del 2010 e del 2025. Non è quindi un nuovo record assoluto: il minimo più basso della serie resta quello del settembre 2012.",
                "La sequenza di lungo periodo rimane però netta. Tutte le 20 estati dal 2007 al 2026 figurano fra le 20 con la minore estensione minima dall'inizio delle osservazioni satellitari continue, avviate alla fine del 1978.",
                "L'estensione misura la superficie oceanica in cui il ghiaccio copre almeno il 15% di ciascuna cella osservata. Non equivale né al volume né allo spessore: due anni possono avere una superficie simile ma quantità complessive di ghiaccio differenti.",
                "Le osservazioni indicano infatti che il ghiaccio residuo è mediamente più giovane e sottile. La quota pluriennale, capace di superare almeno una stagione di fusione, è diminuita e l'Artico è sempre più dominato dal ghiaccio formatosi nell'ultimo inverno.",
                "Anche la stagione fredda ha mostrato un segnale estremo. Il massimo del marzo 2026 ha pareggiato statisticamente quello del 2025 come il più basso dell'intera serie satellitare, secondo i dati citati da NASA e NSIDC.",
                "Il tempo atmosferico può amplificare o rallentare la fusione da un'estate all'altra. Negli ultimi dieci anni una maggiore copertura nuvolosa ha limitato in alcuni periodi l'energia solare disponibile; questa variabilità spiega le oscillazioni recenti, ma non annulla il calo osservato nel lungo periodo.",
                "Il monitoraggio usa sensori satellitari a microonde passive, in grado di distinguere ghiaccio e acqua anche attraverso le nuvole. Dal 2025 la serie integra inoltre le osservazioni del satellite giapponese GCOM-W, mantenendo il confronto con le missioni precedenti.",
            ],
            "fonti": [
                {"url": "https://science.nasa.gov/earth/earth-observatory/arctic-sea-ice-shrinks-to-its-2026-minimum/", "nome": "NASA Earth Observatory — aggiornamento sul minimo artico 2026 e metodo satellitare."},
                {"url": "https://nsidc.org/sea-ice-today/analyses/arctic-sea-ice-minimum-ties-tenth-lowest-0", "nome": "National Snow and Ice Data Center — analisi indipendente del minimo del 12 settembre 2026."},
            ],
            "image": image_record(
                "ghiaccio-artico-minimo-2026-4-6-milioni-km2-08-10-2026", IMAGES["artico"],
                "Illustrazione editoriale IA del ghiaccio marino artico frammentato alla fine dell'estate; scena non documentaria.",
                "Vista aerea fotorealistica del ghiaccio marino sul Mar Glaciale Artico al minimo di fine estate, acqua libera tra le banchise, luce naturale, nessun testo o mappa.",
            ),
            "published": now - timedelta(minutes=2),
        },
        {
            "slug": "influenza-aviaria-h5-vaccini-umani-cinque-paesi-ue-08-10-2026",
            "titolo": "Influenza H5, campagne umane avviate in cinque Paesi UE",
            "sommario": (
                "La valutazione ECDC riguarda soprattutto lavoratori esposti ad animali infetti. "
                "Il rischio resta basso per la popolazione generale e basso-moderato per gli esposti."
            ),
            "luogo": "Stoccolma",
            "categoria": "Scienza",
            "formato": "standard",
            "parole_chiave_titolo": ["campagne umane", "cinque Paesi UE"],
            "dati_chiave": [
                {"icona": "◆", "valore": "5 Paesi", "etichetta": "con campagne già avviate"},
                {"icona": "▲", "valore": "27 su 30", "etichetta": "Paesi che hanno risposto"},
                {"icona": "●", "valore": "8", "etichetta": "con raccomandazioni nazionali"},
            ],
            "paragrafi": [
                "Cinque Paesi dell'Unione europea e dello Spazio economico europeo hanno già avviato campagne di vaccinazione umana contro l'influenza zoonotica A(H5): Austria, Finlandia, Lituania, Paesi Bassi e Portogallo. La nuova ricognizione dell'ECDC riguarda programmi mirati, non una vaccinazione della popolazione generale.",
                "Ventisette dei 30 Paesi interpellati hanno risposto al Centro europeo per la prevenzione e il controllo delle malattie. Otto riferiscono raccomandazioni nazionali già operative, altri otto le stanno preparando e 11 non avevano piani al momento dell'indagine.",
                "I gruppi indicati più spesso sono veterinari, personale sanitario animale, squadre addette all'abbattimento, lavoratori di laboratorio e addetti ad allevamenti e settore avicolo. Tre Paesi, oltre ai cinque già attivi, prevedono di iniziare entro un anno.",
                "L'H5N1 ad alta patogenicità continua a circolare fra uccelli selvatici e a causare focolai in pollame e altri animali europei. L'ECDC segnala tuttavia che le infezioni umane restano rare e che nell'UE e nello Spazio economico europeo non risultano casi umani confermati fino alla data della valutazione.",
                "Per questo il rischio è classificato basso per la popolazione generale e basso-moderato per chi è esposto per lavoro o per altre attività ad animali infetti o ambienti contaminati. La classificazione non significa rischio zero e può cambiare se mutano circolazione, esposizioni o caratteristiche del virus.",
                "L'adesione alle campagne è risultata generalmente bassa fuori dai laboratori, ma i dati disponibili sono incompleti e non confrontabili fra Paesi. Differiscono anche obiettivi, modalità di consegna dei vaccini e sistemi di registrazione.",
                "La vaccinazione mirata è una misura complementare. Restano centrali biosicurezza negli allevamenti, dispositivi di protezione, sorveglianza degli esposti e individuazione rapida di eventuali infezioni; la Commissione europea ricorda che l'H5N1 è anzitutto una malattia degli uccelli e che i casi umani osservati sono collegati soprattutto a contatti molto ravvicinati.",
                "L'ECDC invita i Paesi a definire in anticipo obiettivi, scenari che attivano i programmi, percorsi di distribuzione, comunicazione e controllo dell'adesione. La valutazione non introduce un obbligo uniforme europeo: le decisioni operative restano nazionali e dipendono dal rischio concreto.",
            ],
            "fonti": [
                {"url": "https://www.ecdc.europa.eu/en/publications-data/zoonotic-influenza-ah5-vaccination-humans-eueea", "nome": "ECDC — valutazione sui programmi di vaccinazione umana A(H5) nell'UE/SEE, 7 ottobre 2026."},
                {"url": "https://food.ec.europa.eu/animals/animal-diseases/diseases-and-control-measures/avian-influenza_en", "nome": "Commissione europea — quadro sanitario indipendente sull'influenza aviaria e sulle implicazioni per l'uomo."},
            ],
            "image": image_record(
                "influenza-aviaria-h5-vaccini-umani-cinque-paesi-ue-08-10-2026", IMAGES["h5"],
                "Illustrazione editoriale IA di veterinari, ricercatori e un addetto avicolo che esaminano campioni e un vaccino; scena non documentaria.",
                "Veterinaria, ricercatore e lavoratore avicolo con volti visibili in laboratorio europeo collegato a un allevamento, campioni e flacone neutro, fotografia sanitaria fotorealistica, nessuna iniezione o testo.",
            ),
            "published": now - timedelta(minutes=1),
        },
        {
            "slug": "ranking-fifa-italia-quindicesima-5-55-punti-08-10-2026",
            "titolo": "Ranking FIFA, Italia ancora 15ª ma guadagna 5,55 punti",
            "sommario": (
                "Gli Azzurri restano nella stessa posizione dopo quattro gare di Nations League, "
                "ma riducono il distacco da Germania e Croazia. La Spagna conserva il primo posto."
            ),
            "luogo": "Roma",
            "categoria": "Sport",
            "formato": "flash",
            "parole_chiave_titolo": ["Italia ancora 15ª", "5,55 punti"],
            "dati_chiave": [
                {"icona": "◆", "valore": "15ª", "etichetta": "posizione dell'Italia"},
                {"icona": "▲", "valore": "+5,55", "etichetta": "punti guadagnati"},
                {"icona": "●", "valore": "18 nov", "etichetta": "prossimo aggiornamento"},
            ],
            "paragrafi": [
                "L'Italia resta al quindicesimo posto nel ranking FIFA maschile pubblicato il 7 ottobre, ma guadagna 5,55 punti dopo le quattro partite di Nations League. La posizione non cambia; si riduce però il distacco dalle nazionali immediatamente davanti.",
                "La classifica è guidata ancora dalla Spagna, seguita da Argentina e Francia. Germania e Croazia scendono rispettivamente al tredicesimo e al quattordicesimo posto, entrambe superate dalla Svizzera, ora dodicesima.",
                "Il Portogallo entra fra le prime cinque con un doppio sorpasso su Brasile e Marocco. Più indietro, Mali e Sudafrica avanzano di sei posizioni e raggiungono il 47° e il 48° posto; la Grecia sale al 41° dopo quattro partite senza sconfitte.",
                "Il ranking non è una semplice graduatoria basata sulle vittorie. Il sistema assegna o sottrae punti considerando forza dell'avversaria, importanza della partita e risultato atteso: per questo una nazionale può guadagnare punti senza salire, se anche le squadre davanti mantengono un margine sufficiente.",
                "Il dato di ottobre registra quindi un miglioramento numerico dell'Italia, non un avanzamento nella gerarchia mondiale. Il prossimo aggiornamento ufficiale è previsto per il 18 novembre, dopo il nuovo blocco di partite internazionali.",
            ],
            "fonti": [
                {"url": "https://www.figc.it/it/nazionali/news/ranking-fifa-litalia-rimane-al-15-posto-la-spagna-si-conferma-prima-klvfkh95", "nome": "FIGC — comunicato sul ranking FIFA dell'Italia, 7 ottobre 2026, ore 16:49."},
                {"url": "https://inside.fifa.com/fifa-world-ranking/men", "nome": "FIFA — classifica mondiale maschile e metodologia ufficiale."},
            ],
            "image": image_record(
                "ranking-fifa-italia-quindicesima-5-55-punti-08-10-2026", IMAGES["fifa"],
                "Illustrazione editoriale IA contestuale di Gianluigi Donnarumma e altri calciatori dell'Italia in uno stadio; scena non documentaria.",
                "Gianluigi Donnarumma riconoscibile in maglia ufficiale dell'Italia con compagni veri sul campo dopo una partita, volti visibili, fotografia sportiva fotorealistica, nessun testo o tabellone.",
                public=True,
            ),
            "published": now,
        },
    ]

    for article in articles:
        article_path = ROOT / "notizie" / f"{article['slug']}.html"
        article_path.unlink(missing_ok=True)
        published = article["published"]
        site.write_article(article, article["image"], VERSION)
        register_image_once(article["image"], article["slug"])
        set_published(article["slug"], published)

    latest_url = f"/notizie/{articles[-1]['slug']}.html"
    site.sync_surfaces(articles, latest_url, VERSION, update_manifest=False)


if __name__ == "__main__":
    main()
