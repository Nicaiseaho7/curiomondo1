#!/usr/bin/env python3
"""Pubblica tre notizie di politica italiana dell'8 ottobre 2026, senza manifest."""
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

VERSION = 803
ROME = ZoneInfo("Europe/Rome")
CAPTION = site.CAPTION
GENERATED = ROOT.parent / "generated_images"

IMAGES = {
    "ilva": GENERATED / "exec-d293b9ac-8697-45f9-a406-e4c9b3b162c5.png",
    "impianti": GENERATED / "exec-5897e2d5-46c8-4283-b280-a902a73eb153.png",
    "farmaci": GENERATED / "exec-16e5ac96-911e-485e-9e89-abaaf156c104.png",
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


def image_record(slug: str, source: Path, alt: str, prompt: str) -> dict:
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
        "sensitiveContext": False,
        "weatherMap": False,
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
            "slug": "decreto-ex-ilva-senato-73-si-camera-08-10-2026",
            "titolo": "Decreto ex Ilva, il Senato approva: 73 sì e testo alla Camera",
            "sommario": (
                "Il provvedimento sulla continuità degli impianti strategici è stato modificato a Palazzo Madama. "
                "Non è ancora legge: serve il voto della Camera entro i termini di conversione."
            ),
            "luogo": "Roma",
            "categoria": "Politica",
            "formato": "flash",
            "parole_chiave_titolo": ["73 sì", "testo alla Camera"],
            "dati_chiave": [
                {"icona": "◆", "valore": "73", "etichetta": "voti favorevoli"},
                {"icona": "▲", "valore": "49", "etichetta": "voti contrari"},
                {"icona": "●", "valore": "3", "etichetta": "astensioni"},
            ],
            "paragrafi": [
                "Il Senato ha approvato con modificazioni il disegno di legge di conversione del decreto-legge 154 del 2026 sulla continuità operativa degli impianti di interesse strategico nazionale, noto come decreto ex Ilva. Il voto del 7 ottobre si è chiuso con 73 favorevoli, 49 contrari e tre astensioni.",
                "Il testo passa ora alla Camera. Poiché Palazzo Madama lo ha modificato, Montecitorio dovrà esaminare la nuova versione: il voto del Senato non conclude quindi la conversione e non rende definitive le modifiche introdotte.",
                "Il provvedimento riguarda la continuità produttiva e il percorso industriale degli stabilimenti. Durante la replica in Aula, la sottosegretaria alle Imprese Fausta Bergamotto ha indicato due scenari ancora possibili: la cessione dei soli impianti per i laminati oppure la cessione insieme all'area a caldo di Taranto.",
                "Bergamotto ha inoltre sostenuto che il percorso per salvare l'impianto è ancora aperto e che il decreto non elimina presìdi ambientali. Sono affermazioni del Governo rese nel dibattito parlamentare, non l'esito già acquisito della procedura di vendita.",
                "Il passaggio decisivo è ora alla Camera, che dovrà approvare il testo entro la scadenza costituzionale del decreto. Se Montecitorio introducesse altre modifiche, sarebbe necessario un nuovo esame del Senato.",
            ],
            "fonti": [
                {"url": "https://www.senato.it/attualita/in-copertina", "nome": "Senato della Repubblica — esito ufficiale della seduta del 7 ottobre 2026."},
                {"url": "https://www.agenzianova.com/news/decreto-ex-ilva-con-73-si-via-libera-dal-senato-il-testo-passa-alla-camera/", "nome": "Agenzia Nova — conferma indipendente del voto e del passaggio alla Camera."},
            ],
            "image": image_record(
                "decreto-ex-ilva-senato-73-si-camera-08-10-2026", IMAGES["ilva"],
                "Illustrazione editoriale IA dell'Aula del Senato durante una seduta istituzionale; scena non documentaria.",
                "Aula di Palazzo Madama con senatori rivolti verso la presidenza, bandiere italiana ed europea, fotografia editoriale fotorealistica e neutrale, nessun testo.",
            ),
            "published": now - timedelta(minutes=2),
        },
        {
            "slug": "registro-dispositivi-medici-impiantabili-senato-08-10-2026",
            "titolo": "Dispositivi impiantabili, il Senato approva il registro nazionale",
            "sommario": (
                "Il RUNDMI dovrà collegare tracciabilità, vigilanza e monitoraggio clinico. "
                "Il disegno di legge passa alla Camera e non è ancora entrato in vigore."
            ),
            "luogo": "Roma",
            "categoria": "Politica",
            "formato": "flash",
            "parole_chiave_titolo": ["registro nazionale", "dispositivi impiantabili"],
            "dati_chiave": [
                {"icona": "◆", "valore": "RUNDMI", "etichetta": "nuovo registro unico"},
                {"icona": "▲", "valore": "12 mesi", "etichetta": "per il decreto attuativo"},
                {"icona": "●", "valore": "940 mila €", "etichetta": "oneri previsti nel 2027"},
            ],
            "paragrafi": [
                "Il Senato ha approvato il disegno di legge che istituisce il Registro unico nazionale dei dispositivi medici impiantabili, denominato RUNDMI. Il voto del 7 ottobre è avvenuto in prima lettura: il provvedimento passa alla Camera e non è ancora legge.",
                "Il registro sarà collocato presso la direzione generale competente del Ministero della Salute. Dovrà sostenere il monitoraggio clinico delle persone sottoposte a impianto o rimozione, la tracciabilità dei dispositivi e le attività di vigilanza e sorveglianza previste dalle norme europee e nazionali.",
                "La struttura comprenderà la sezione già esistente sugli impianti protesici mammari e ulteriori sezioni dedicate alle altre tipologie. Un decreto del Ministro della Salute, da adottare entro dodici mesi dall'entrata in vigore della futura legge e previa intesa con le Regioni, dovrà individuare i dispositivi inclusi.",
                "Il testo prevede che medici, professionisti sanitari e operatori economici inseriscano i dati richiesti. Per gli incidenti collegati a un impianto, la decodifica del codice identificativo dovrà avvenire secondo regole attuative e nel rispetto della protezione dei dati personali.",
                "Gli oneri indicati sono pari a 100 mila euro per il 2026, 940 mila per il 2027 e 260 mila per il 2028, oltre a 300 mila euro annui dal 2028. Le risorse sono poste a carico del fondo per il governo dei dispositivi medici.",
                "La Camera potrà approvare il testo, modificarlo o respingerlo. Soltanto un voto conforme dei due rami e la successiva promulgazione renderanno operative l'istituzione del registro e le scadenze previste.",
            ],
            "fonti": [
                {"url": "https://www.senato.it/show-doc?id=0&leg=0&part=doc_dc-allegatoa_aa-ddltit_ddlntfdc1875&tipodoc=hotresaula", "nome": "Senato della Repubblica — testo approvato e resoconto definitivo del ddl n. 1875."},
                {"url": "https://parlamento19.openpolis.it/attivita_legislativa/disegni_di_legge?government=135225&initiative=GOV&type=ORD", "nome": "Openpolis — monitoraggio indipendente dell'iter del ddl sul registro dei dispositivi impiantabili."},
            ],
            "image": image_record(
                "registro-dispositivi-medici-impiantabili-senato-08-10-2026", IMAGES["impianti"],
                "Illustrazione editoriale IA di una bioingegnera e un chirurgo con dispositivi medici impiantabili; scena non documentaria.",
                "Bioingegnera e chirurgo in ambiente ospedaliero italiano esaminano pacemaker e protesi, volti visibili, fotografia sanitaria fotorealistica, nessun testo o paziente.",
            ),
            "published": now - timedelta(minutes=1),
        },
        {
            "slug": "riforma-farmaceutica-senato-delega-governo-08-10-2026",
            "titolo": "Riforma farmaceutica, il Senato approva la delega al Governo",
            "sommario": (
                "Il testo interviene su accesso ai medicinali, spesa, carenze e farmacie territoriali. "
                "Passa alla Camera: le nuove regole richiederanno anche decreti legislativi."
            ),
            "luogo": "Roma",
            "categoria": "Politica",
            "formato": "flash",
            "parole_chiave_titolo": ["riforma farmaceutica", "delega al Governo"],
            "dati_chiave": [
                {"icona": "◆", "valore": "A.S. 1786", "etichetta": "disegno di legge delega"},
                {"icona": "▲", "valore": "4 aree", "etichetta": "accesso, spesa, dati e farmacie"},
                {"icona": "●", "valore": "2° passaggio", "etichetta": "esame ora alla Camera"},
            ],
            "paragrafi": [
                "Il Senato ha approvato il disegno di legge delega per la riforma e il riordino della legislazione farmaceutica. Il testo, collegato alla manovra di finanza pubblica, passa alla Camera: il voto di Palazzo Madama non modifica ancora le regole per cittadini, farmacie e imprese.",
                "La delega indica al Governo i criteri per intervenire sull'accesso ai medicinali, sul monitoraggio e controllo della spesa, sui servizi sanitari territoriali delle farmacie e sull'integrazione della rete farmaceutica con l'assistenza locale.",
                "Tra gli obiettivi figurano la revisione dei tetti di spesa e del payback, oltre al riordino della distribuzione dei farmaci. Il testo richiama anche la produzione nazionale di principi attivi, eccipienti e prodotti finiti, con attenzione ai medicinali destinati a patologie rare, croniche o invalidanti.",
                "Sul versante digitale è prevista una maggiore integrazione dei dati su prescrizioni, dispensazione, prezzi, consumi e scorte. L'obiettivo dichiarato è migliorare il monitoraggio delle carenze e l'interoperabilità con il fascicolo sanitario elettronico e il dossier farmaceutico.",
                "La delega punta inoltre a rafforzare le farmacie territoriali nella rete sanitaria, favorendo la collaborazione con medici di medicina generale, pediatri e altri professionisti. Modalità e limiti concreti dipenderanno dai successivi decreti legislativi.",
                "Prima dell'attuazione serve il via libera della Camera sul medesimo testo. Dopo l'eventuale entrata in vigore della legge delega, il Governo dovrà adottare i decreti previsti rispettando princìpi, tempi e confini fissati dal Parlamento.",
            ],
            "fonti": [
                {"url": "https://www.senato.it/show-doc?id=0&leg=0&part=doc_dc&tipodoc=hotresaula", "nome": "Senato della Repubblica — resoconto definitivo della seduta e contenuto del ddl n. 1786."},
                {"url": "https://parlamento19.openpolis.it/attivita_legislativa/disegni_di_legge?branch=&government=&initiative=GOV&ordering=-law_publication_date&type=ORD", "nome": "Openpolis — monitoraggio indipendente dell'iter della delega farmaceutica."},
            ],
            "image": image_record(
                "riforma-farmaceutica-senato-delega-governo-08-10-2026", IMAGES["farmaci"],
                "Illustrazione editoriale IA di farmacisti al banco con un paziente in una farmacia italiana; scena non documentaria.",
                "Farmacista italiana informa un paziente anziano in farmacia mentre un collega controlla le scorte, volti visibili, fotografia editoriale fotorealistica, nessun testo leggibile.",
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
