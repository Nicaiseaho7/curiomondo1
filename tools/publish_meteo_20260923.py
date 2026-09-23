#!/usr/bin/env python3
"""Pubblica il bollettino meteo nazionale del 23 settembre 2026."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("/workspace/scratch/d40ad21643e3/generated_images/exec-58b67604-b82a-4447-9d78-165d141a74c7.png")
VERSION = 523
SLUG = "meteo-italia-oggi-settimana-23-28-settembre-2026"

import sys
sys.path.insert(0, str(ROOT))
from automation.newsroom import site


def make_variants() -> list[dict]:
    image = Image.open(SOURCE).convert("RGB")
    target = 1.5
    w, h = image.size
    if w / h > target:
        nw = round(h * target)
        left = (w - nw) // 2
        image = image.crop((left, 0, left + nw, h))
    else:
        nh = round(w / target)
        top = (h - nh) // 2
        image = image.crop((0, top, w, top + nh))
    out = []
    directory = ROOT / "assets/images/editorial-auto"
    for width in (480, 800, 1200):
        path = directory / f"{SLUG}-v{VERSION}-{width}.webp"
        image.resize((width, round(width / target)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=87, method=6)
        out.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}",
                    "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return out


def main() -> None:
    article = {
        "slug": SLUG,
        "titolo": "Meteo Italia, sole oggi e nuovi rovesci al Centro-Sud da giovedì",
        "sommario": "Mercoledì 23 settembre prevale il tempo stabile. Tra giovedì e venerdì aumenta l’instabilità su Isole e regioni centro-meridionali; il weekend torna più soleggiato.",
        "categoria": "Meteo",
        "luogo": "Italia",
        "formato": "standard",
        "parole_chiave_titolo": ["sole oggi", "Centro-Sud"],
        "dati_chiave": [
            {"valore": "23 settembre", "etichetta": "sole prevalente oggi", "icona": "◆"},
            {"valore": "24–25", "etichetta": "fase più instabile", "icona": "◆"},
            {"valore": "26–27", "etichetta": "weekend più stabile", "icona": "◆"},
        ],
        "paragrafi": [
            "Mercoledì 23 settembre il tempo resta stabile su gran parte dell’Italia, con sole prevalente al Centro e al Sud e nubi sparse al Nord. L’aria più fresca da nord-est contiene le temperature, mentre rovesci localizzati possono interessare soprattutto Sardegna e Sicilia.",
            "In Valle d’Aosta, Piemonte, Liguria e Lombardia sono previste schiarite alternate a passaggi nuvolosi. Torino si muove fra 15 e 27 gradi, Milano fra 13 e 24 e Genova fra 18 e 23. Sulle Alpi gli addensamenti saranno più frequenti rispetto alle pianure.",
            "Trentino-Alto Adige, Veneto e Friuli-Venezia Giulia iniziano con qualche nube, seguita da aperture più ampie. Venezia è prevista fra 15 e 23 gradi. In Emilia-Romagna prevale il sole, con Bologna fra 13 e 26 gradi e nessuna allerta nel bollettino regionale valido per oggi.",
            "Toscana, Umbria e Marche trascorrono una giornata in gran parte asciutta. Firenze raggiunge 27 gradi dopo una minima di 13. Nel Lazio il cielo resta generalmente sereno: a Roma sono attesi valori fra 15 e 27 gradi, senza piogge significative durante la giornata.",
            "In Abruzzo il mattino è più fresco nelle aree interne, con L’Aquila fra 6 e 20 gradi. Molise e Basilicata mantengono condizioni prevalentemente asciutte. Gli addensamenti pomeridiani lungo l’Appennino non escludono fenomeni isolati, ma non indicano un peggioramento uniforme.",
            "Campania, Puglia e Calabria vedono ampie zone soleggiate, accompagnate da venti nordorientali più avvertibili sulle coste adriatiche e ioniche. Napoli è prevista fra 17 e 27 gradi; Bari fra 17 e 23. Sul Salento la ventilazione può risultare più sostenuta.",
            "In Sicilia il sole prevale a Palermo, con temperature fra 16 e 27 gradi, ma restano possibili rovesci locali in altri settori dell’isola. In Sardegna le precipitazioni sono più probabili nelle ore notturne e in forma intermittente; Cagliari è prevista fra 19 e 29 gradi.",
            "Giovedì 24 aumenta l’instabilità su Sardegna, Lazio e Campania, con temporali possibili solo in parte dei territori interessati. Il Nord resta tra nubi e schiarite, mentre Puglia e Sicilia conservano intervalli soleggiati. Le temperature massime restano generalmente miti.",
            "Venerdì 25 i rovesci possono raggiungere più diffusamente il Centro-Sud, compresi Lazio, Campania, Puglia e Sicilia. Al Nord il tempo appare più stabile, con massime intorno a 23 gradi a Milano. L’Aquila può scendere a circa 17 gradi nelle ore diurne.",
            "Sabato 26 e domenica 27 è atteso un miglioramento su gran parte del Paese. Milano, Roma, Napoli e Bari tornano verso condizioni prevalentemente soleggiate; in Sicilia resta possibile qualche episodio domenicale. In Sardegna prevalgono schiarite con massime ancora vicine ai 29 gradi.",
            "Lunedì 28 la nuvolosità tende ad aumentare al Nord e sul Lazio, senza un segnale uniforme di maltempo nazionale. Sud peninsulare e Puglia restano più stabili. A questa distanza temporale posizione e intensità delle precipitazioni possono cambiare e richiedono nuovi aggiornamenti.",
            "Le indicazioni meteorologiche non equivalgono alle allerte di protezione civile, che valutano gli effetti possibili sul territorio. Per temporali intensi, vento e rischio idrogeologico vanno consultati i bollettini nazionali, regionali e comunali aggiornati prima degli spostamenti.",
        ],
        "fonti": [
            {"url": "https://www.meteoam.it/it/home", "descrizione": "Aeronautica Militare — osservazioni e previsioni meteorologiche nazionali consultate il 23 settembre 2026."},
            {"url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/", "descrizione": "Dipartimento della Protezione Civile — bollettino nazionale di criticità e distinzione tra previsione meteorologica e allerta."},
            {"url": "https://allertameteo.regione.emilia-romagna.it/", "descrizione": "Regione Emilia-Romagna — bollettino di vigilanza 144/2026 valido dal 23 settembre, senza allerta."},
            {"url": "https://www.meteo.it/", "descrizione": "Meteo.it — tendenza nazionale dal 23 settembre: aria fresca balcanica e successiva instabilità al Centro-Sud."},
        ],
    }
    image = {
        "key": f"{SLUG}-v{VERSION}",
        "alt": "Vista editoriale IA fotorealistica dell’Italia dal satellite con cielo sereno sulla penisola e nubi più dense vicino a Sardegna e Sicilia; scena non documentaria.",
        "variants": make_variants(),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image tool",
        "sensitiveContext": False,
    }
    site.write_article(article, image, VERSION)
    site.register_image(image, article["slug"], VERSION)
    cfg_path = ROOT / "assets/data/homepage-config-v504.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg["version"] = VERSION
    cfg["articles"][f"/notizie/{article['slug']}.html"] = {
        "firstPublishedAt": article["published"], "homepagePriority": 92, "primaryCategory": "meteo"
    }
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.sync_surfaces([article], f"/notizie/{article['slug']}.html", VERSION)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = VERSION
    manifest["site"]["site_version"] = VERSION
    manifest["site_version"] = VERSION
    manifest["version"] = f"v{VERSION}"
    manifest["release_version"] = f"v{VERSION}"
    manifest["last_release"] = {"version": VERSION, "date": "2026-09-23", "type": "weather-service",
        "news_added": [article["slug"]], "news_updated": [],
        "change": "Previsioni meteo nazionali per il 23-28 settembre 2026 con copertura delle 20 regioni"}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(site_version=VERSION, version=str(VERSION), currentVersion=VERSION,
                     release_date="2026-09-23", last_update="meteo-italia-settimana-v523")
        if "articleCount" in state:
            state["articleCount"] += 1
        if "generatedEditorialImages" in state:
            state["generatedEditorialImages"] += 1
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"slug": article["slug"], "version": VERSION}, ensure_ascii=False))


if __name__ == "__main__":
    main()
