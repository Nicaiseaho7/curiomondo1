#!/usr/bin/env python3
"""Release manuale v794: nuova hero Hormuz, meteo e due notizie primarie."""
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

VERSION = 794
ROME = ZoneInfo("Europe/Rome")
CAPTION = site.CAPTION
GENERATED = ROOT.parent / "generated_images"

IMAGES = {
    "hormuz": GENERATED / "exec-cb5aa4dc-5597-4eae-818d-b35b41d92c99.png",
    "meteo": GENERATED / "exec-c5b62dee-ba82-4896-b254-6a2afd4afa36.png",
    "nasa": GENERATED / "exec-d76ca623-5d8e-43ca-9ff0-610e1ca3fab8.png",
    "bce": GENERATED / "exec-6ee3d296-60c7-4f23-9779-e818b66e1b64.png",
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
    result = []
    out = ROOT / "assets/images/editorial-auto"
    for width in (480, 800, 1200):
        height = round(width / ratio)
        path = out / f"{slug}-v{VERSION}-{width}.webp"
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


def image_record(slug: str, source: Path, alt: str, prompt: str, sensitive: bool = False) -> dict:
    return {
        "key": f"{slug}-v{VERSION}",
        "alt": alt,
        "prompt": prompt,
        "variants": variants(source, slug),
        "disclosure": CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": sensitive,
        "weatherMap": False,
    }


def set_published(slug: str, published: datetime, remove_name_card: bool = False) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    iso = published.isoformat(timespec="seconds")
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data["datePublished"] = iso
            data["dateModified"] = iso
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    if remove_name_card:
        for node in doc.xpath('//aside[contains(@class,"cm-name-card")]'):
            node.getparent().remove(node)
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )


def replace_hormuz() -> None:
    slug = "hormuz-petroliera-on-peace-12-feriti-evacuati-oman-07-10-2026"
    alt = (
        "Illustrazione editoriale IA di una petroliera nello Stretto di Hormuz in piena luce, "
        "con la costa montuosa dell’Oman sullo sfondo; scena non documentaria."
    )
    prompt = (
        "Petroliera moderna in navigazione nello Stretto di Hormuz, costa del Musandam e Oman "
        "visibile, luce chiara del mattino, scena contestuale sobria senza attacco, feriti, fumo o testo."
    )
    image = image_record(slug, IMAGES["hormuz"], alt, prompt, sensitive=True)
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    v = image["variants"]
    doc.xpath('//meta[@property="og:image"]')[0].set("content", f"https://curiomondo.it{v[-1]['src']}")
    doc.xpath('//meta[@property="og:image:alt"]')[0].set("content", alt)
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data["image"] = [f"https://curiomondo.it{v[-1]['src']}"]
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    figure = doc.xpath('//figure[contains(@class,"article-image")]')[0]
    figure.set("data-ai-generated", "true")
    figure.set("data-sensitive-context", "true")
    img = figure.xpath('.//img')[0]
    img.set("src", f"..{v[1]['src']}")
    img.set("srcset", ", ".join(f"..{row['src']} {row['w']}w" for row in v))
    img.set("width", "800")
    img.set("height", "450")
    img.set("alt", alt)
    figure.xpath('.//figcaption')[0].text = CAPTION
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = VERSION
    image["article"] = f"/notizie/{slug}.html"
    registry.setdefault("items", []).insert(0, image)
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    now = datetime.now(ROME).replace(second=0, microsecond=0)
    articles = [
        {
            "slug": "meteo-italia-7-14-ottobre-2026",
            "titolo": "Meteo Italia 7-14 ottobre: più piogge, temperature ancora miti",
            "sommario": (
                "La tendenza dell’Aeronautica Militare indica precipitazioni sopra la media in diverse regioni e valori termici generalmente elevati. "
                "Le indicazioni oltre 48–72 ore restano probabilistiche."
            ),
            "luogo": "Italia",
            "categoria": "Meteo",
            "formato": "standard",
            "parole_chiave_titolo": ["più piogge", "temperature ancora miti"],
            "dati_chiave": [
                {"icona": "◆", "valore": "7-14 ott", "etichetta": "periodo della tendenza"},
                {"icona": "▲", "valore": "12-18 ott", "etichetta": "seconda fase più incerta"},
                {"icona": "●", "valore": "sopra media", "etichetta": "temperature prevalenti"},
            ],
            "paragrafi": [
                "Mercoledì 7 ottobre 2026 apre una fase più variabile sull’Italia. L’Aeronautica Militare colloca il Paese tra l’alta pressione sull’Europa centro-settentrionale e una circolazione più instabile sul Mediterraneo, con differenze marcate tra Nord-Est, regioni tirreniche e Isole.",
                "Fino a domenica 11 ottobre la tendenza ufficiale segnala piogge complessivamente superiori alla media su basso Piemonte, Liguria, coste venete e friulane, Emilia-Romagna, Toscana, Marche, Umbria, Lazio, Sardegna e Sicilia meridionale. Sul resto del territorio i quantitativi settimanali sono indicati vicino ai valori tipici del periodo.",
                "Il dato non significa pioggia continua in tutte le aree elencate. Una previsione settimanale descrive il bilancio probabile del periodo, mentre orari, intensità e localizzazione dei fenomeni richiedono i bollettini regionali e gli aggiornamenti a breve termine.",
                "In Alto Adige, il servizio meteorologico provinciale prevede per oggi condizioni abbastanza soleggiate, con massime tra 17 e 22 gradi. Per giovedì 8 indica precipitazioni a tratti e il passaggio serale di un fronte freddo, seguito venerdì 9 da nuvolosità variabile e da un possibile miglioramento nel fine settimana.",
                "Sabato 10 e domenica 11, quindi, possono offrire pause più asciutte su una parte dell’arco alpino, mentre la tendenza nazionale mantiene un segnale più piovoso in diverse zone del Centro, sulle coste del Nord-Est e sulle Isole. Le condizioni locali possono divergere anche tra province vicine.",
                "Da lunedì 12 a mercoledì 14 aumenta l’incertezza. L’Aeronautica Militare prevede per la settimana 12–18 ottobre una maggiore influenza della circolazione ciclonica sul Mediterraneo, con precipitazioni sopra la media più probabili su Lazio, medio Adriatico, Sud e Isole Maggiori.",
                "Le temperature dovrebbero rimanere nel complesso superiori ai valori abituali su gran parte del Paese. Le eccezioni indicate riguardano soprattutto la Sicilia centro-orientale nella prima fase e, nella settimana successiva, i rilievi altoatesini e la Sicilia sud-orientale, più vicini alle medie stagionali.",
                "Per viaggi, mare e attività all’aperto è utile controllare ogni giorno le previsioni della propria regione. L’emissione mensile dell’Aeronautica Militare è uno scenario probabilistico e non sostituisce avvisi, allerte o bollettini operativi aggiornati.",
            ],
            "fonti": [
                {"url": "https://www.meteoam.it/it/previsioni-mensili", "nome": "Aeronautica Militare — tendenza ufficiale per il 6–11 e il 12–18 ottobre 2026."},
                {"url": "https://meteo.provincia.bz.it/it/meteo-alto-adige", "nome": "Provincia autonoma di Bolzano — previsione ufficiale 7–11 ottobre e livelli di affidabilità."},
            ],
            "image": image_record(
                "meteo-italia-7-14-ottobre-2026", IMAGES["meteo"],
                "Illustrazione editoriale IA della costa ligure sotto nubi variabili e schiarite, senza dati o simboli nei pixel; scena non documentaria.",
                "Costa ligure in ottobre con nubi stratificate e una schiarita luminosa sul mare; scena fotorealistica, senza mappe, icone, temperature, date o testo.",
            ),
            "published": now - timedelta(minutes=2),
            "remove_name_card": True,
        },
        {
            "slug": "bce-imprese-ia-europee-finanziamento-mercato-07-10-2026",
            "titolo": "Imprese IA europee, la BCE rileva più debito di mercato",
            "sommario": (
                "Le aziende dei settori più legati all’intelligenza artificiale usano ancora molto capitale interno, ma il finanziamento obbligazionario sta crescendo. "
                "I dati arrivano fino al secondo trimestre 2025."
            ),
            "luogo": "Eurozona",
            "categoria": "Economia",
            "formato": "standard",
            "parole_chiave_titolo": ["Imprese IA europee", "debito di mercato"],
            "dati_chiave": [
                {"icona": "◆", "valore": "2023-2025", "etichetta": "adozione IA più che raddoppiata"},
                {"icona": "▲", "valore": "2° trim 2025", "etichetta": "ultimi dati societari"},
                {"icona": "●", "valore": "mercati", "etichetta": "debito in crescita"},
            ],
            "paragrafi": [
                "Le imprese dell’area euro attive nei settori più intensivi di intelligenza artificiale stanno aumentando il ricorso al debito raccolto sui mercati. L’indicazione emerge da un’analisi pubblicata il 6 ottobre da quattro economisti della Banca centrale europea, basata su bilanci societari, brevetti e variabili finanziarie.",
                "Tra il 2023 e il 2025 la quota di aziende dell’area euro che utilizza almeno una tecnologia di IA è più che raddoppiata. L’aumento riguarda soprattutto strumenti per generare o analizzare linguaggio, immagini e video, ma l’adozione di una tecnologia non coincide con lo sviluppo di modelli propri.",
                "Le aziende più esposte all’IA continuano a usare in misura rilevante risorse interne e capitale di rischio. Software, dati, algoritmi e organizzazione sono attività difficili da offrire come garanzia bancaria rispetto a macchinari o immobili, un limite che può ridurre l’accesso ai prestiti tradizionali.",
                "I bilanci mostrano però uno spostamento recente verso forme di debito di mercato. Il risultato riguarda gli ultimi dati disponibili, fermi al secondo trimestre 2025, e non dimostra che tutte le imprese tecnologiche europee abbiano la stessa struttura finanziaria.",
                "La BCE osserva anche una forte crescita dei brevetti legati all’IA nell’area euro nell’ultimo decennio, ancora inferiore ai livelli statunitensi. Le imprese europee e americane lavorano in campi simili, tra apprendimento automatico, elaborazione dei dati, comunicazioni e automazione dei processi.",
                "Secondo gli autori, mercati dei capitali europei più profondi e integrati potrebbero sostenere le aziende nelle diverse fasi di crescita. La conclusione è analitica: il testo specifica che le opinioni espresse appartengono agli autori e non rappresentano necessariamente la posizione della BCE o dell’Eurosistema.",
                "Un rapporto della Banca europea per gli investimenti pubblicato a gennaio collega le scelte di trasferimento all’estero di startup e scaleup innovative a più fattori. Tra questi figurano accesso ai mercati, disponibilità di finanziamenti, regole e capacità di attrarre personale qualificato.",
                "Per i lettori e le imprese, il punto operativo è distinguere il costo del capitale dalla sola disponibilità di credito. La crescita dell’IA richiede investimenti immateriali e lunghi tempi di sviluppo, quindi fonti di finanziamento diverse possono diventare complementari anziché sostituirsi del tutto.",
            ],
            "fonti": [
                {"url": "https://www.ecb.europa.eu/press/blog/date/2026/html/ecb.blog20261006~35bf3c24cb.en.html", "nome": "Banca centrale europea — analisi del 6 ottobre 2026 su IA, bilanci, brevetti e finanziamento."},
                {"url": "https://www.eib.org/en/publications/20250217-drivers-of-relocation-by-innovative-eu-startups-and-scaleups", "nome": "Banca europea per gli investimenti — rapporto sui fattori di trasferimento di startup e scaleup innovative."},
            ],
            "image": image_record(
                "bce-imprese-ia-europee-finanziamento-mercato-07-10-2026", IMAGES["bce"],
                "Illustrazione editoriale IA di un gruppo europeo di tecnologia e finanza riunito davanti a dati aziendali; scena non documentaria.",
                "Team europeo di professionisti della tecnologia e della finanza in riunione, volti visibili, laptop e grafici neutri, nessun logo o testo leggibile.",
            ),
            "published": now - timedelta(minutes=1),
        },
        {
            "slug": "crew-12-lascia-iss-ammaraggio-8-ottobre-2026",
            "titolo": "Crew-12 lascia la ISS: ammaraggio previsto l’8 ottobre",
            "sommario": (
                "NASA ed ESA programmano il distacco della capsula Dragon alle 14:05 italiane del 7 ottobre. "
                "Il rientro al largo della California resta subordinato al meteo e alla prontezza dei sistemi."
            ),
            "luogo": "Stazione spaziale internazionale",
            "categoria": "Scienza",
            "formato": "flash",
            "parole_chiave_titolo": ["Crew-12", "8 ottobre"],
            "dati_chiave": [
                {"icona": "◆", "valore": "14:05", "etichetta": "distacco del 7 ottobre"},
                {"icona": "▲", "valore": "17:34", "etichetta": "ammaraggio previsto l’8"},
                {"icona": "●", "valore": "4", "etichetta": "membri dell’equipaggio"},
            ],
            "paragrafi": [
                "La missione Crew-12 è pronta a lasciare la Stazione spaziale internazionale mercoledì 7 ottobre 2026. NASA ed ESA indicano il distacco della capsula Dragon intorno alle 14:05 italiane, dopo la chiusura dei portelli e i controlli finali dell’equipaggio.",
                "A bordo viaggiano gli astronauti NASA Jessica Meir e Jack Hathaway, l’astronauta ESA Sophie Adenot e il cosmonauta Roscosmos Andrei Fedyaev. L’ammaraggio è previsto al largo della California giovedì 8 ottobre alle 17:34 italiane.",
                "Gli orari possono cambiare. I responsabili di missione stanno verificando la prontezza della capsula, delle squadre di recupero e delle condizioni meteorologiche nel Pacifico, fattori che devono essere compatibili prima di autorizzare il rientro.",
                "Dopo il distacco dal modulo Harmony, Dragon eseguirà una serie di manovre per allontanarsi dalla stazione. Durante il ritorno lo scudo termico proteggerà la capsula dal plasma prodotto dall’ingresso atmosferico, con temperature che l’ESA indica fino a 1.600 gradi.",
                "Per Sophie Adenot il rientro chiude la missione εpsilon, iniziata con il lancio del 13 febbraio. Il 3 settembre ha superato 200 giorni consecutivi nello spazio, stabilendo il primato europeo per un singolo volo, e ha svolto tre attività extraveicolari per un totale di 19 ore e 42 minuti.",
                "Il programma scientifico europeo ha compreso esperimenti su salute, materiali, biologia, fluidi e radiazioni. Adenot ha inoltre contribuito alla prova del dispositivo di esercizio E4D e alla stampa tridimensionale di metallo in orbita, tecnologie pensate anche per missioni future.",
                "NASA trasmetterà la chiusura dei portelli, il distacco e l’ammaraggio sulle proprie piattaforme. Anche ESA Web TV seguirà le fasi principali; tra il distacco e l’avvio del rientro saranno disponibili comunicazioni audio con i controllori di volo.",
            ],
            "fonti": [
                {"url": "https://www.nasa.gov/news-release/nasa-to-stream-spacex-crew-12-return-splashdown-live/", "nome": "NASA — programma ufficiale del rientro Crew-12, orari e condizioni operative."},
                {"url": "https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/epsilon/Watch_Sophie_Adenot_return_to_Earth", "nome": "ESA — rientro di Sophie Adenot, programma scientifico e dati della missione εpsilon."},
            ],
            "image": image_record(
                "crew-12-lascia-iss-ammaraggio-8-ottobre-2026", IMAGES["nasa"],
                "Illustrazione editoriale IA della capsula Dragon Crew-12 in allontanamento dalla Stazione spaziale internazionale; scena non documentaria.",
                "Capsula Crew Dragon separata dalla Stazione spaziale internazionale sopra la Terra, geometria plausibile, luce orbitale, nessun testo o logo inventato.",
            ),
            "published": now,
        },
    ]

    replace_hormuz()
    for article in articles:
        image = article.pop("image")
        published = article.pop("published")
        remove_name_card = bool(article.pop("remove_name_card", False))
        slug = site.write_article(article, image, VERSION)
        site.register_image(image, slug, VERSION)
        set_published(slug, published, remove_name_card)

    site.sync_surfaces(articles, "/notizie/crew-12-lascia-iss-ammaraggio-8-ottobre-2026.html", VERSION)
    print(json.dumps({"version": VERSION, "articles": [a["slug"] for a in articles]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
