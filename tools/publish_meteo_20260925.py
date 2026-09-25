#!/usr/bin/env python3
"""Pubblica il bollettino meteo nazionale del 25 settembre 2026."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "generated_images/exec-0466d9fd-4bd6-4c0e-a516-bbc48d9815cf.png"
VERSION = 557
SLUG = "meteo-italia-25-settembre-2-ottobre-2026"

import sys

sys.path.insert(0, str(ROOT))
from automation.newsroom import site


def make_variants() -> list[dict]:
    image = Image.open(SOURCE).convert("RGB")
    target = 1.5
    width, height = image.size
    if width / height > target:
        new_width = round(height * target)
        left = (width - new_width) // 2
        image = image.crop((left, 0, left + new_width, height))
    elif width / height < target:
        new_height = round(width / target)
        top = (height - new_height) // 2
        image = image.crop((0, top, width, top + new_height))

    result = []
    directory = ROOT / "assets/images/editorial-auto"
    for size in (480, 800, 1200):
        path = directory / f"{SLUG}-v{VERSION}-{size}.webp"
        image.resize((size, round(size / target)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=90, method=6
        )
        result.append({
            "w": size,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return result


def main() -> None:
    article = {
        "slug": SLUG,
        "titolo": "Meteo Italia, rovesci e vento al Sud: weekend più stabile",
        "sommario": (
            "Venerdì 25 settembre piogge e temporali interessano soprattutto Adriatico, "
            "Campania, Puglia, Calabria e Sicilia. Da sabato l’alta pressione riporta "
            "ampie schiarite, con temperature miti fino ai primi giorni di ottobre."
        ),
        "categoria": "Meteo",
        "luogo": "Italia",
        "formato": "standard",
        "parole_chiave_titolo": ["rovesci e vento", "weekend più stabile"],
        "dati_chiave": [
            {"valore": "25 settembre", "etichetta": "instabilità al Sud", "icona": "◆"},
            {"valore": "26–27", "etichetta": "weekend più stabile", "icona": "●"},
            {"valore": "fino a 31°", "etichetta": "massima a Cagliari", "icona": "▲"},
        ],
        "paragrafi": [
            (
                "Venerdì 25 settembre il tempo resta più instabile lungo il versante adriatico e al Sud. "
                "Rovesci o temporali possono interessare Marche meridionali, Abruzzo, Molise, Campania, "
                "Puglia, Basilicata, Calabria e Sicilia, mentre al Nord prevalgono schiarite e nuvolosità variabile."
            ),
            (
                "Il bollettino di vigilanza della Protezione Civile segnala precipitazioni localmente moderate "
                "nelle aree più esposte e forti venti di Grecale tra medio-basso Adriatico, Puglia e Basilicata. "
                "L’Adriatico può risultare localmente molto mosso; chi si sposta deve controllare gli aggiornamenti regionali."
            ),
            (
                "Al Nord la giornata è in gran parte asciutta. Torino e Milano raggiungono circa 24 gradi, "
                "Venezia 22 e Bologna 25. Tra sabato e martedì aumentano sole e temperature, con massime che "
                "possono arrivare a 27-28 gradi nelle pianure occidentali ed emiliane."
            ),
            (
                "Toscana e alto Lazio conservano ampie pause soleggiate, ma rovesci isolati possono raggiungere "
                "i settori orientali di Umbria e Lazio. Firenze sale verso 27 gradi e Roma verso 28. "
                "Da sabato il quadro diventa più stabile su gran parte del Centro."
            ),
            (
                "Marche, Abruzzo e Molise sono più esposti a piogge e temporali nella prima parte del periodo. "
                "Sulle regioni adriatiche le temperature diminuiscono e il vento accentua la sensazione di fresco. "
                "Il miglioramento è atteso tra sabato pomeriggio e domenica."
            ),
            (
                "In Campania sono possibili brevi rovesci, con Napoli intorno a 26 gradi. Puglia e Basilicata "
                "restano sotto nubi più compatte e vento sostenuto; Bari si ferma vicino a 23 gradi. "
                "Sabato persistono fenomeni residui soprattutto sul Salento e sui tratti ionici."
            ),
            (
                "Calabria e Sicilia alternano schiarite a rovesci, più probabili sui versanti ionici e sulla Sicilia "
                "settentrionale e orientale. Palermo raggiunge circa 27 gradi. Domenica il cielo diventa sereno o "
                "poco nuvoloso quasi ovunque, salvo addensamenti locali sulla Calabria ionica."
            ),
            (
                "La Sardegna resta ai margini dell’instabilità e conserva condizioni più soleggiate. Cagliari può "
                "toccare 31 gradi oggi, poi le massime scendono verso 28-29 nel weekend. Anche nella prima parte "
                "della prossima settimana il tempo resta generalmente asciutto."
            ),
            (
                "Sabato 26 l’alta pressione torna a dominare su Nord, Centro e Sardegna. Al Sud rimangono nubi e "
                "qualche rovescio al mattino tra Salento, coste ioniche e Sicilia settentrionale, seguiti da schiarite. "
                "La ventilazione settentrionale resta vivace e i mari ancora mossi."
            ),
            (
                "Domenica 27 il sole prevale da nord a sud. Le eccezioni riguardano poche nubi al mattino sulla "
                "Calabria ionica e addensamenti pomeridiani sull’Appennino meridionale. Le massime tornano ad aumentare, "
                "mentre il vento si attenua rispetto a sabato."
            ),
            (
                "Tra lunedì 28 e mercoledì 30 settembre la fase stabile prosegue su gran parte dell’Italia. "
                "Milano e Bologna si portano verso 27-28 gradi, Firenze può raggiungere 30 e Roma resta intorno a 28. "
                "Le notti risultano più fresche nelle pianure interne e nelle vallate."
            ),
            (
                "Tra giovedì 1 e venerdì 2 ottobre aumenta l’incertezza, soprattutto al Sud e sulle isole, dove "
                "aria più umida può favorire nuovi rovesci locali. La tendenza dell’Aeronautica Militare mantiene "
                "precipitazioni sotto la media al Centro-Nord e temperature sopra la media in tutto il Paese."
            ),
        ],
        "fonti": [
            {
                "url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-vigilanza/",
                "descrizione": "Protezione Civile — bollettino di vigilanza meteorologica nazionale del 24 settembre 2026 per i fenomeni attesi il 25 e 26 settembre.",
            },
            {
                "url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/",
                "descrizione": "Protezione Civile — bollettino nazionale di criticità aggiornato il 24 settembre 2026.",
            },
            {
                "url": "https://www.meteoam.it/it/previsioni-fine-settimana",
                "descrizione": "Aeronautica Militare — previsione ufficiale per il weekend del 26-27 settembre 2026.",
            },
            {
                "url": "https://www.meteoam.it/it/previsioni-mensili",
                "descrizione": "Aeronautica Militare — tendenza probabilistica dal 28 settembre al 4 ottobre 2026 e limiti delle previsioni a più giorni.",
            },
        ],
    }

    image = {
        "key": f"{SLUG}-v{VERSION}",
        "alt": (
            "Mappa meteo editoriale IA dell’Italia del 25 settembre 2026 con confini regionali, "
            "città principali, temperature massime, sole al Nord e rovesci sul versante adriatico e al Sud."
        ),
        "prompt": (
            "Mappa meteorologica editoriale dell’Italia per il 25 settembre 2026, con confini regionali "
            "chiari, dieci città e temperature, simboli di sole, rovesci e vento, testo italiano leggibile."
        ),
        "variants": make_variants(),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation tool",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "sensitiveContext": False,
    }

    site.write_article(article, image, VERSION)
    site.register_image(image, article["slug"], VERSION)

    config_path = ROOT / "assets/data/homepage-config-v504.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["version"] = VERSION
    config["articles"][f"/notizie/{article['slug']}.html"] = {
        "firstPublishedAt": article["published"],
        "homepagePriority": 94,
        "primaryCategory": "meteo",
    }
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces([article], f"/notizie/{article['slug']}.html", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = VERSION
    manifest["site"]["site_version"] = VERSION
    manifest["site_version"] = VERSION
    manifest["version"] = f"v{VERSION}"
    manifest["release_version"] = f"v{VERSION}"
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-25",
        "type": "weather-service",
        "news_added": [article["slug"]],
        "news_updated": [],
        "change": "Meteo Italia dal 25 settembre al 2 ottobre 2026 con mappa regionale, città principali e tendenza a sette giorni",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for filename in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            site_version=VERSION,
            version=str(VERSION),
            currentVersion=VERSION,
            release_date="2026-09-25",
            last_update="meteo-italia-25-settembre-2-ottobre-v557",
        )
        if "articleCount" in state:
            state["articleCount"] += 1
        if "generatedEditorialImages" in state:
            state["generatedEditorialImages"] += 1
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"slug": article["slug"], "version": VERSION}, ensure_ascii=False))


if __name__ == "__main__":
    main()
