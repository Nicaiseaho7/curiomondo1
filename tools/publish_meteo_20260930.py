#!/usr/bin/env python3
"""Bollettino meteo del 30 settembre 2026 e tendenza fino al 6 ottobre."""
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
SLUG = "meteo-italia-30-settembre-6-ottobre-2026"
PARAGRAFI = [
    (
        "Mercoledì 30 settembre 2026 l’Italia resta sotto anticiclone. Sole prevalente al Centro "
        "e al Sud, nubi più frequenti al Nord-Ovest, massime tra 24 e 29 gradi e punte ancora "
        "elevate per il periodo."
    ),
    (
        "Al Nord il cielo è nuvoloso in Piemonte e sulle Alpi occidentali, sereno o poco nuvoloso "
        "altrove. Milano e Torino intorno ai 24-25 gradi; Venezia e Trieste 23-26. Piogge assenti "
        "o isolate solo in alta quota."
    ),
    (
        "Al Centro tempo soleggiato. Toscana e Lazio raggiungono 28-29 gradi; Roma e Firenze "
        "restano miti di giorno, con minime più fresche per l’ampia escursione termica."
    ),
    (
        "Al Sud e sulle Isole prevale il sole. Isolati rovesci restano possibili sulla Sicilia "
        "sud-orientale e sulla Calabria meridionale, senza allerta nazionale. In Sardegna "
        "massime ancora elevate, fino a circa 30-31 gradi nelle zone interne."
    ),
    (
        "La Protezione Civile, nel bollettino di criticità del 29 settembre, indica assenza di "
        "fenomeni significativi e nessuna allerta nazionale per oggi 30 settembre e per la "
        "giornata precedente."
    ),
    (
        "Secondo iLMeteo e la Repubblica, su Roma si delineano le condizioni tipiche "
        "dell’«ottobrata»: stabilità, scarso vento e valori diurni sopra la media per l’inizio "
        "di ottobre."
    ),
    (
        "Giovedì 1 e venerdì 2 ottobre il quadro resta stabile e in prevalenza soleggiato su "
        "quasi tutta la Penisola, con nubi variabili al Nord-Ovest. Il weekend 3-4 ottobre "
        "conferma stabilità e qualche nube in più al Nord."
    ),
    (
        "La tendenza a medio termine posticipa un possibile fronte atlantico verso martedì 6 "
        "ottobre. Fino a tale data l’alta pressione dovrebbe mantenere tempo asciutto su gran "
        "parte d’Italia; oltre i 5-7 giorni l’incertezza cresce."
    ),
    (
        "Di notte i termometri scendono: in montagna minime fino a 8-9 gradi, in pianura "
        "13-15. Di giorno i valori restano sopra le medie. Venti deboli e mari calmi o poco "
        "mossi sulla maggior parte dei bacini."
    ),
    (
        "Fino a lunedì 5 ottobre lo scenario più probabile è sole e caldo diurno, senza "
        "allerta nazionale. Questa sintesi non sostituisce i bollettini locali: per viaggi e "
        "mare ricontrollare le previsioni aggiornate della giornata."
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
    version = max(site._version(), 702)
    article = {
        "slug": SLUG,
        "titolo": "Meteo Italia oggi e 7 giorni: sole e ottobrata, nessuna allerta nazionale",
        "sommario": (
            "Mercoledì 30 settembre anticiclone e sole al Centro-Sud, nubi al Nord-Ovest. "
            "Massime fino a 28-29 gradi; Protezione Civile senza allerta. Stabile fino al 5-6 ottobre."
        ),
        "categoria": "Meteo",
        "luogo": "Italia",
        "formato": "standard",
        "parole_chiave_titolo": ["sole e ottobrata", "nessuna allerta"],
        "dati_chiave": [
            {"icona": "◆", "valore": "30 settembre", "etichetta": "oggi, sole prevalente"},
            {"icona": "▲", "valore": "28-29 °C", "etichetta": "massime al Centro"},
            {"icona": "●", "valore": "nessuna allerta", "etichetta": "bollettino PC nazionale"},
        ],
        "paragrafi": PARAGRAFI,
        "published": "2026-09-30T05:20:00+02:00",
        "modified": "2026-09-30T05:20:00+02:00",
        "fonti": [
            {
                "url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/",
                "descrizione": "Protezione Civile — bollettino criticità 29 settembre 2026: nessuna allerta per il 29 e il 30 settembre.",
            },
            {
                "url": "https://www.repubblica.it/cronaca/2026/09/30/news/previsioni_meteo_stabilita_sole_escursione_termica-425615794/",
                "descrizione": "la Repubblica — 30 settembre 2026: stabilità fino a lunedì, ottobrata a Roma, fronte possibile dal 6 ottobre.",
            },
            {
                "url": "https://www.gazzettadiparma.it/italia-mondo/2026/09/29/news/bel-tempo-massime-fino-a-29-31c-con-decisa-escursione-termica-970979/",
                "descrizione": "ANSA / Gazzetta di Parma — iLMeteo: bel tempo, massime 29-31°C, dettaglio 30 settembre e 1 ottobre.",
            },
            {
                "url": "https://www.ilmeteo.it/portale/meteo-domani",
                "descrizione": "iLMeteo — meteo 30 settembre 2026: anticiclone, sole e massime 28-29°C al Centro.",
            },
            {
                "url": "https://www.meteo2.it/previsioni-meteo-mercoledi-30-settembre-sole-al-centro-e-al-sud-nuvole-al-nord-fino-a-26-gradi-sulle-isole/",
                "descrizione": "Meteo2 — 30 settembre 2026: sole Centro-Sud, nubi al Nord, pioggia improbabile su scala nazionale.",
            },
        ],
    }
    image = {
        "key": f"{SLUG}-v{version}",
        "alt": (
            "Mappa meteo editoriale dell’Italia per mercoledì 30 settembre 2026, con sole "
            "sulle regioni, temperature sulle città principali e nubi leggere al Nord-Ovest."
        ),
        "prompt": (
            "Mappa meteorologica editoriale dell’Italia 30 settembre–6 ottobre 2026 con loghi "
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
