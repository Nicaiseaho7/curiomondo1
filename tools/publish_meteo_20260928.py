#!/usr/bin/env python3
"""Bollettino meteo del 28 settembre 2026 e tendenza fino al 4 ottobre."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

SOURCE = Path("/workspace/artifacts/imagine_images/b064a31b-abd3-4410-848f-8b24cdc9076b.jpg")
SLUG = "meteo-italia-28-settembre-4-ottobre-2026"
PARAGRAFI = [
    (
        "Lunedì 28 settembre 2026 l’Italia resta sotto anticiclone. Repubblica, citando iLMeteo, "
        "prevede stabilità e sole su gran parte della Penisola, con massime fino a 30 gradi "
        "in diverse regioni e temperature sopra le medie del periodo."
    ),
    (
        "Al Nord, al Centro e al Sud-Isole il bollettino di oggi indica soleggiamento prevalente. "
        "A Milano iLMeteo aggiornato alle 0:04 parla di cielo sereno, pioggia assente e massime "
        "intorno ai 24-26 gradi; a Roma sereno e massime vicine ai 25-28 gradi."
    ),
    (
        "Martedì 29 e mercoledì 30 settembre il quadro resta simile: sole o nubi sparse, senza "
        "un peggioramento generale. Mercoledì al Nord-Ovest possono comparire più nubi, "
        "ma le precipitazioni restano assenti o molto localizzate secondo le città campione."
    ),
    (
        "iLMeteo e MeteoLive segnalano caldo anomalo d’autunno, con punte di 27-28 gradi e oltre "
        "su Valpadana, Toscana, Sardegna e aree interne del Centro. Le notti restano più fresche "
        "al Nord rispetto alle ore centrali del giorno."
    ),
    (
        "L’Aeronautica Militare, per il periodo 28 settembre–4 ottobre, descrive un anticiclone "
        "di blocco e temperature superiori alla media su tutto il Paese, più marcate su Alpi, "
        "pianura padana e levante ligure. La Sicilia centro-orientale resta più vicina alle medie."
    ),
    (
        "Nella stessa tendenza le piogge restano vicine alla media su Sicilia, gran parte della "
        "Sardegna e Nord, sotto media su Friuli Venezia Giulia, medio Adriatico e Sud. "
        "Nella seconda parte della settimana può crescere l’instabilità al Nord-Ovest e in Sardegna."
    ),
    (
        "Da giovedì 1 ottobre iLMeteo indica più nubi e possibili piovaschi isolati su Alpi "
        "centro-occidentali e Sicilia. Venerdì e sabato le nubi aumentano; verso domenica 4 "
        "ottobre la tendenza resta da ricalibrare giorno per giorno."
    ),
    (
        "Repubblica avverte che oltre i 5-7 giorni il margine di incertezza cresce. Il weekend "
        "potrebbe portare le prime piogge dal Nord-Ovest, poi altrove: non è ancora un dettaglio "
        "orario, ma un’indicazione di scenario."
    ),
    (
        "I venti restano deboli su gran parte del Paese, con mari calmi o poco mossi e Ionio "
        "localmente più mosso. Non risulta un’allerta nazionale diffusa per lunedì e martedì: "
        "restano utili i bollettini regionali per mare e montagna."
    ),
    (
        "Fino a domenica 4 ottobre lo scenario più probabile è sole e caldo nelle ore diurne, "
        "con primi disturbi da metà settimana. Questa sintesi non sostituisce le previsioni "
        "locali: per viaggi e mare ricontrollare i bollettini aggiornati della giornata."
    ),
]


def make_variants(version: int) -> list[dict]:
    image = Image.open(SOURCE).convert("RGB")
    target = 1.5
    width, height = image.size
    if abs(width / height - target) > 0.02:
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
    directory.mkdir(parents=True, exist_ok=True)
    for size in (480, 800, 1200):
        path = directory / f"{SLUG}-v{version}-{size}.webp"
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
    counts = [len(p.split()) for p in PARAGRAFI]
    total = sum(counts)
    print("parole", counts, "totale", total)
    if any(n > 60 for n in counts) or not 300 <= total <= 600:
        raise SystemExit(f"lunghezza non conforme: {counts} tot={total}")
    version = max(site._version(), 642)
    article = {
        "slug": SLUG,
        "titolo": "Meteo Italia oggi e 7 giorni: sole e fino a 30 gradi fino al 4 ottobre",
        "sommario": (
            "Lunedì 28 settembre anticiclone e sole su quasi tutta l’Italia, con massime fino a "
            "30 gradi. La settimana resta stabile; da giovedì più nubi e possibili piovaschi "
            "al Nord-Ovest e in Sicilia."
        ),
        "categoria": "Meteo",
        "luogo": "Italia",
        "formato": "standard",
        "parole_chiave_titolo": ["fino a 30 gradi", "4 ottobre"],
        "dati_chiave": [
            {"icona": "◆", "valore": "28 settembre", "etichetta": "oggi, sole prevalente"},
            {"icona": "▲", "valore": "fino a 30 °C", "etichetta": "picchi previsti"},
            {"icona": "●", "valore": "28 set–4 ott", "etichetta": "tendenza 7 giorni"},
        ],
        "paragrafi": PARAGRAFI,
        "published": "2026-09-28T03:30:00+02:00",
        "modified": "2026-09-28T03:30:00+02:00",
        "fonti": [
            {
                "url": "https://www.repubblica.it/cronaca/2026/09/28/news/previsioni_meteo_settimana_30_gradi_caldo-425611506/",
                "descrizione": "Repubblica / iLMeteo — 28 settembre 2026: settimana stabile, massime fino a 30 gradi, dettaglio giornaliero e possibile ritorno piogge dal weekend.",
            },
            {
                "url": "https://www.ilmeteo.it/",
                "descrizione": "iLMeteo — 28 settembre 2026: tempo stabile e caldo, più nubi da giovedì, possibile peggioramento dal 4-5 ottobre.",
            },
            {
                "url": "https://www.ilmeteo.it/pdf/meteo-milano.pdf",
                "descrizione": "iLMeteo Milano — bollettino 28 settembre 2026 ore 0:04: sereno, precipitazioni assenti, massime 24-26 gradi nei primi giorni.",
            },
            {
                "url": "https://www.meteoam.it/it/previsioni-fine-settimana",
                "descrizione": "Aeronautica Militare — tendenza 28 settembre–4 ottobre 2026: anticiclone di blocco, temperature sopra media, piogge vicine o sotto media.",
            },
            {
                "url": "https://www.meteolive.it/news/prima-pagina/caldo-estremo-europa-morti-eccesso-2026/",
                "descrizione": "MeteoLive — caldo d’autunno 27-28 settembre 2026: massime 27-28 gradi su più regioni e aumento termico di lunedì.",
            },
        ],
    }
    # fix meteolive url to the actual search result
    article["fonti"][4]["url"] = "https://www.meteolive.it/news/prima-pagina/caldo-estremo-europa-morti-eccesso-2026/"
    article["fonti"][4] = {
        "url": "https://www.meteolive.it/news/prima-pagina/caldo-dautunno-27-28su-queste-regioni-tra-domenica-e-lunedi/",
        "descrizione": "MeteoLive — 27 settembre 2026: caldo d’autunno, massime 27-28 gradi e rialzo termico di lunedì 28.",
    }
    image = {
        "key": f"{SLUG}-v{version}",
        "alt": (
            "Mappa meteo editoriale dell’Italia per lunedì 28 settembre 2026, con loghi di sole "
            "e nubi sulle regioni, città principali e striscia dei sette giorni fino al 4 ottobre."
        ),
        "prompt": (
            "Mappa meteorologica editoriale dell’Italia 28 settembre–4 ottobre 2026 con loghi "
            "sole e nubi, città leggibili e striscia settimanale."
        ),
        "variants": make_variants(version),
        "disclosure": site.CAPTION,
        "generator": "agente editoriale Imagine (Grok)",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": False,
    }
    site.write_article(article, image, version)
    site.register_image(image, article["slug"], version)
    config_path = ROOT / "assets/data/homepage-config-v504.json"
    if config_path.exists():
        config = json.loads(config_path.read_text(encoding="utf-8"))
        config["version"] = max(int(config.get("version") or 0), version)
        config.setdefault("articles", {})
        config["articles"][f"/notizie/{article['slug']}.html"] = {
            "firstPublishedAt": article["published"],
            "homepagePriority": 96,
            "primaryCategory": "meteo",
        }
        config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.sync_surfaces([article], f"/notizie/{article['slug']}.html", version)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.setdefault("site", {})
    manifest["site"]["current_site_version"] = version
    manifest["site"]["site_version"] = version
    manifest["site_version"] = version
    manifest["version"] = f"v{version}"
    manifest["release_version"] = f"v{version}"
    manifest["last_release"] = {
        "version": version,
        "date": "2026-09-28",
        "type": "weather-service",
        "news_added": [article["slug"]],
        "news_updated": [],
        "change": "Meteo Italia 28 settembre–4 ottobre 2026 con mappa e loghi",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for filename in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / filename
        if not path.exists():
            continue
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            site_version=version,
            version=str(version),
            currentVersion=version,
            release_date="2026-09-28",
            last_update=f"{SLUG}-v{version}",
        )
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"slug": article["slug"], "version": version}, ensure_ascii=False))


if __name__ == "__main__":
    main()
