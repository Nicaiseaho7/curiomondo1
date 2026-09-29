#!/usr/bin/env python3
"""Bollettino meteo del 29 settembre 2026 e tendenza fino al 5 ottobre."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

SOURCE = Path("/workspace/artifacts/tmp/editorial/meteo-source.jpg")
SLUG = "meteo-italia-29-settembre-5-ottobre-2026"
PARAGRAFI = [
    (
        "Martedì 29 settembre 2026 l’Italia resta sotto anticiclone. Sole o poco nuvoloso su gran "
        "parte della Penisola, con massime tra 24 e 31 gradi e valori sopra le medie del periodo."
    ),
    (
        "Al Nord prevale il sole; nubi più compatte solo su Alpi occidentali e Cuneese, senza piogge "
        "rilevanti. A Milano e Torino massime intorno ai 25 gradi; a Venezia e Trieste 23-24."
    ),
    (
        "Al Centro e in Sardegna il cielo è sereno o poco nuvoloso. Firenze e Roma toccano 27-28 "
        "gradi; in Sardegna iLMeteo e Meteo.it segnalano picchi di 30-31 gradi."
    ),
    (
        "Al Sud bel tempo con qualche nube pomeridiana sull’Appennino. In Sicilia sud-orientale "
        "è in vigore allerta gialla della Protezione Civile nazionale e regionale per temporali "
        "e rischio idrogeologico."
    ),
    (
        "L’allerta gialla copre le zone Sud-Orientale, Stretto di Sicilia, bacino del Simeto, "
        "centro-meridionale e isole Pelagie. Possibili rovesci intensi, fulmini e grandine "
        "localizzata, senza allerta nazionale sul resto del Paese."
    ),
    (
        "L’Aeronautica Militare, per il periodo 28 settembre–4 ottobre, conferma anticiclone di "
        "blocco e temperature superiori alla media, più marcate su Alpi, pianura padana e levante "
        "ligure. La Sicilia centro-orientale resta più vicina alle medie."
    ),
    (
        "Mercoledì 30 settembre e giovedì 1 ottobre il quadro resta stabile: sole prevalente, "
        "nubi sparse al Nord-Ovest. Venerdì 2 ottobre cresce l’instabilità su Alpi occidentali "
        "e Sardegna, con possibili rovesci isolati."
    ),
    (
        "Nel weekend 3-5 ottobre la tendenza, ancora da ricalibrare, indica prime piogge dal "
        "Nord-Ovest. Oltre i 5-7 giorni il margine di incertezza cresce, come avvertono i bollettini."
    ),
    (
        "I venti restano deboli o moderati, con Scirocco sul Canale di Sardegna. Mari calmi o poco "
        "mossi; Canale di Sardegna e Ionio localmente più mossi. Niente allerta nazionale diffusa "
        "fuori dalla Sicilia."
    ),
    (
        "Fino a domenica 5 ottobre lo scenario più probabile è sole e caldo diurno, con primi "
        "disturbi da venerdì. Questa sintesi non sostituisce le previsioni locali: per viaggi e "
        "mare ricontrollare i bollettini aggiornati della giornata."
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
    version = max(site._version(), 679)
    article = {
        "slug": SLUG,
        "titolo": "Meteo Italia oggi e 7 giorni: sole fino a 31 gradi, allerta gialla in Sicilia",
        "sommario": (
            "Martedì 29 settembre anticiclone e sole su quasi tutta l’Italia, con massime fino a "
            "31 gradi in Sardegna. Allerta gialla per temporali in Sicilia sud-orientale; "
            "da venerdì possibili primi disturbi al Nord-Ovest."
        ),
        "categoria": "Meteo",
        "luogo": "Italia",
        "formato": "standard",
        "parole_chiave_titolo": ["fino a 31 gradi", "allerta gialla"],
        "dati_chiave": [
            {"icona": "◆", "valore": "29 settembre", "etichetta": "oggi, sole prevalente"},
            {"icona": "▲", "valore": "fino a 31 °C", "etichetta": "picchi in Sardegna"},
            {"icona": "●", "valore": "allerta gialla", "etichetta": "Sicilia SE, temporali"},
        ],
        "paragrafi": PARAGRAFI,
        "published": "2026-09-29T04:45:00+02:00",
        "modified": "2026-09-29T04:45:00+02:00",
        "fonti": [
            {
                "url": "https://www.meteoam.it/it/previsioni-fine-settimana",
                "descrizione": "Aeronautica Militare — tendenza 28 settembre–4 ottobre 2026: anticiclone di blocco, temperature sopra media.",
            },
            {
                "url": "https://www.ilmeteo.it/pdf/meteo-milano.pdf",
                "descrizione": "iLMeteo Milano — bollettino 29 settembre 2026 ore 0:08: nubi sparse, precipitazioni assenti, massime 24-25 gradi.",
            },
            {
                "url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/",
                "descrizione": "Protezione Civile — bollettino criticità 28 settembre 2026: allerta gialla temporali e idrogeologico in Sicilia per il 29 settembre.",
            },
            {
                "url": "https://www.meteo.it/notizie/meteo-settimana-al-via-con-tempo-stabile-e-caldo-fuori-stagione-eb9f4033",
                "descrizione": "Meteo.it — 28 settembre 2026: settimana stabile, caldo fuori stagione, picchi 30-31 in Sardegna, instabilità da venerdì.",
            },
            {
                "url": "https://www.meteo2.it/allerta-meteo-gialla-martedi-29-settembre-temporali-su-sicilia/",
                "descrizione": "Meteo2 — allerta gialla 29 settembre 2026: temporali e rischio idrogeologico su zone sud-orientali della Sicilia.",
            },
        ],
    }
    image = {
        "key": f"{SLUG}-v{version}",
        "alt": (
            "Mappa meteo editoriale dell’Italia per martedì 29 settembre 2026, con sole sulle "
            "regioni, temperature sulle città principali, allerta gialla in Sicilia e striscia "
            "dei sette giorni fino al 5 ottobre."
        ),
        "prompt": (
            "Mappa meteorologica editoriale dell’Italia 29 settembre–5 ottobre 2026 con loghi "
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
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest.setdefault("site", {})
        manifest["site"]["current_site_version"] = version
        manifest["site"]["site_version"] = version
        manifest["site_version"] = version
        manifest["version"] = f"v{version}"
        manifest["release_version"] = f"v{version}"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "pronto", "slug": SLUG, "version": version,
                      "url": f"https://curiomondo.it/notizie/{SLUG}.html"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
