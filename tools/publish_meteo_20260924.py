#!/usr/bin/env python3
"""Pubblica il bollettino meteo nazionale del 24 settembre 2026."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parent / "generated_images/exec-b9d85c3d-b221-46db-bd37-157f21af389e.png"
VERSION = 539
SLUG = "meteo-italia-24-settembre-1-ottobre-2026"

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
    else:
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
        "titolo": "Meteo Italia, rovesci locali oggi e venerdì: poi sole fino a mercoledì",
        "sommario": (
            "Giovedì 24 settembre resta variabile tra Nord, Lazio e Sardegna. "
            "Venerdì l’instabilità si sposta al Centro-Sud; dal weekend prevalgono "
            "schiarite e temperature miti, prima di un possibile cambiamento il 1° ottobre."
        ),
        "categoria": "Meteo",
        "luogo": "Italia",
        "formato": "standard",
        "parole_chiave_titolo": ["rovesci locali", "sole"],
        "dati_chiave": [
            {"valore": "24 settembre", "etichetta": "variabilità locale", "icona": "◆"},
            {"valore": "26–30", "etichetta": "fase più stabile", "icona": "●"},
            {"valore": "1° ottobre", "etichetta": "possibile cambiamento", "icona": "▲"},
        ],
        "paragrafi": [
            (
                "Giovedì 24 settembre l’Italia resta divisa tra ampie schiarite e instabilità locale. "
                "Le precipitazioni più probabili riguardano Sardegna e alcuni settori del Centro, "
                "mentre al Nord le nubi aumentano senza un peggioramento uniforme. Sud peninsulare "
                "e Sicilia conservano spazi soleggiati."
            ),
            (
                "Il bollettino nazionale di criticità pubblicato dalla Protezione Civile il 23 settembre "
                "non indica allerte per oggi. L’assenza di un codice colore non esclude brevi rovesci o "
                "temporali circoscritti: prima di spostarsi va controllato il successivo aggiornamento, "
                "soprattutto nelle aree costiere e montane."
            ),
            (
                "In Valle d’Aosta, Piemonte, Liguria e Lombardia prevalgono alternanze di sole e nuvole. "
                "Torino può raggiungere 28 gradi, Milano 26 e Genova 23. Sulle Alpi, comprese le aree del "
                "Trentino-Alto Adige, gli addensamenti risultano più frequenti e possono produrre fenomeni isolati."
            ),
            (
                "Veneto e Friuli-Venezia Giulia vedono un cielo più chiuso con il passare delle ore, mentre "
                "l’Emilia-Romagna resta in gran parte asciutta. Venezia si ferma intorno a 23 gradi e Bologna "
                "può arrivare a 26. Venerdì e sabato aumentano le schiarite sulle pianure settentrionali."
            ),
            (
                "In Toscana, Umbria e Marche la nuvolosità cresce senza piogge diffuse. Firenze raggiunge "
                "circa 27 gradi e Perugia 23. Nel Lazio sono possibili temporali localizzati, anche se Roma "
                "mantiene una massima vicina a 27 gradi; venerdì resta il rischio di brevi rovesci."
            ),
            (
                "Abruzzo e Molise risentono maggiormente dell’instabilità venerdì, con possibili temporali e "
                "un calo delle massime nelle zone interne. L’Aquila passa dai 23 gradi di oggi a circa 19, "
                "con minime basse nelle conche appenniniche. Da sabato torna un tempo più stabile."
            ),
            (
                "Campania, Puglia, Basilicata e Calabria iniziano con condizioni generalmente discrete, ma "
                "venerdì possono comparire piogge e temporali. Napoli e Reggio Calabria oscillano oggi tra "
                "26 e 27 gradi, mentre Bari si attesta intorno a 25. In Calabria qualche rovescio può durare fino a sabato."
            ),
            (
                "In Sicilia prevale il sole, con Palermo intorno a 27 gradi, prima di rovesci venerdì e di "
                "nuova variabilità domenica. La Sardegna è più instabile già oggi, mentre Cagliari può toccare "
                "29 gradi. Sull’isola le massime restano vicine ai 30 gradi anche all’inizio della prossima settimana."
            ),
            (
                "Sabato 26 il quadro migliora sulla maggior parte del Paese. Domenica 27 resta qualche incertezza "
                "sulla Sicilia, ma Nord, Centro e gran parte del Sud vedono prevalere il sole. Le temperature "
                "diurne risalgono gradualmente, senza indicazioni di caldo eccezionale per il periodo."
            ),
            (
                "Tra lunedì 28 e martedì 29 l’alta pressione favorisce giornate stabili e luminose. Le massime "
                "si portano verso 27-29 gradi a Milano, Roma e Firenze, fino a 30 in Sardegna. Venezia e Genova "
                "restano più miti, con valori generalmente compresi tra 24 e 25 gradi."
            ),
            (
                "Mercoledì 30 rimane soleggiato su buona parte del Centro-Sud e dell’Adriatico. Rovesci locali "
                "possono raggiungere Liguria e Toscana, mentre sulle aree interne abruzzesi è possibile un calo "
                "termico più marcato. Intensità e posizione dei fenomeni hanno ancora un margine elevato di incertezza."
            ),
            (
                "Giovedì 1° ottobre aumenta la probabilità di piogge e temporali al Nord e in parte del Centro, "
                "con possibili episodi anche in Sardegna e Puglia. Il Sud tirrenico conserva condizioni migliori. "
                "La tendenza a sette giorni descrive uno scenario, non un dettaglio affidabile per ogni comune."
            ),
        ],
        "fonti": [
            {
                "url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/index.html",
                "descrizione": "Protezione Civile — bollettino di criticità del 23 settembre 2026, con nessuna allerta nazionale prevista per giovedì 24.",
            },
            {
                "url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-vigilanza/",
                "descrizione": "Protezione Civile — vigilanza meteorologica nazionale e fenomeni previsti per il 24 settembre.",
            },
            {
                "url": "https://www.meteoam.it/it/previsioni-fine-settimana",
                "descrizione": "Aeronautica Militare — tendenza ufficiale per il periodo 21-27 settembre 2026.",
            },
            {
                "url": "https://www.meteoam.it/it/previsioni-mensili",
                "descrizione": "Aeronautica Militare — indicazioni probabilistiche e limiti delle previsioni oltre pochi giorni.",
            },
        ],
    }

    image = {
        "key": f"{SLUG}-v{VERSION}",
        "alt": (
            "Vista satellitare editoriale IA dell’Italia con schiarite sulla penisola e nubi più dense "
            "tra Sardegna, Sicilia e settori tirrenici; scena meteorologica non documentaria."
        ),
        "variants": make_variants(),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image tool",
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
        "date": "2026-09-24",
        "type": "weather-service",
        "news_added": [article["slug"]],
        "news_updated": [],
        "change": "Meteo Italia dal 24 settembre al 1 ottobre 2026 con quadro nazionale, temperature e limiti previsionali",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for filename in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            site_version=VERSION,
            version=str(VERSION),
            currentVersion=VERSION,
            release_date="2026-09-24",
            last_update="meteo-italia-24-settembre-1-ottobre-v539",
        )
        if "articleCount" in state:
            state["articleCount"] += 1
        if "generatedEditorialImages" in state:
            state["generatedEditorialImages"] += 1
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"slug": article["slug"], "version": VERSION}, ensure_ascii=False))


if __name__ == "__main__":
    main()
