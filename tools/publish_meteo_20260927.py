#!/usr/bin/env python3
"""Bollettino meteo del 27 settembre 2026 e tendenza fino al 3 ottobre."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

SOURCE = Path("/workspace/artifacts/imagine_images/3f604899-9ba5-452a-8a60-566f5d59dfea.jpg")
SLUG = "meteo-italia-27-settembre-3-ottobre-2026"
PARAGRAFI = [
    (
        "Domenica 27 settembre l’alta pressione copre l’Italia. Il Corriere della Sera, "
        "citando iLMeteo, descrive cieli sereni o poco nuvolosi quasi ovunque e massime "
        "fino a 28 gradi al Sud. Nelle pianure del Nord le minime notturne restano fra 12 e 14 gradi."
    ),
    (
        "Meteo.it, aggiornato oggi alle 7:09, conferma una giornata stabile. Nubi più estese "
        "possono formarsi sulle Alpi occidentali e nelle zone interne del Sud e della Sicilia. "
        "Le massime superano i 26 gradi al Centro-Nord e sulle isole."
    ),
    (
        "I venti restano deboli, con rinforzi da nord-est all’estremo Sud. Il basso Ionio è molto mosso, "
        "gli altri mari meridionali sono localmente mossi e i bacini restanti poco mossi. "
        "Non risulta un’allerta diffusa, ma il mare del Sud va controllato prima di uscire."
    ),
    (
        "A Roma il bollettino iLMeteo delle 7 indica cielo poco nuvoloso, pioggia assente e una massima "
        "di 27 gradi, con minima intorno ai 16. È una lettura di città, non una media nazionale: "
        "altrove lo scarto fra notte e pomeriggio può essere più ampio."
    ),
    (
        "Lunedì 28 il bel tempo prosegue. Il Corriere segnala cielo sereno o poco nuvoloso, "
        "con qualche breve rovescio pomeridiano possibile sui rilievi calabresi centromeridionali "
        "e su quelli orientali della Sicilia. Non è un peggioramento generale."
    ),
    (
        "Martedì 29 il quadro resta simile e le temperature aumentano di poco. Addensamenti locali "
        "su Alpi e Appennini possono dare isolati piovaschi. In pianura la giornata dovrebbe "
        "restare in prevalenza asciutta e soleggiata."
    ),
    (
        "iLMeteo indica sole prevalente almeno fino al 2 ottobre, con massime di 27-29 gradi "
        "su molte città. Da giovedì 1 ottobre le nubi aumentano e qualche piovasco può interessare "
        "la Sicilia e le Alpi centro-occidentali. Una tendenza a cinque giorni va sempre riletta."
    ),
    (
        "L’Aeronautica Militare, per il periodo dal 28 settembre al 4 ottobre, descrive un anticiclone "
        "di blocco e temperature sopra la media in tutto il Paese. Lo scarto è più marcato su Alpi, "
        "pianura padana e costa ligure. La Sicilia centro-orientale resta più vicina alle medie."
    ),
    (
        "Nella stessa tendenza le piogge restano vicine alla media su Sicilia, gran parte della Sardegna "
        "e Nord, mentre il Friuli Venezia Giulia è indicato sotto media. Sotto media anche l’Adriatico "
        "centrale e il Sud. In coda al periodo l’instabilità può crescere al Nord-Ovest e in Sardegna."
    ),
    (
        "Fino a sabato 3 ottobre lo scenario più probabile è sole e caldo nelle ore centrali, "
        "con notti più fresche al Nord e primi disturbi isolati da giovedì. Chi si sposta al mare "
        "o in montagna deve ricontrollare i bollettini regionali: la settimana non sostituisce l’aggiornamento del giorno."
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
        raise SystemExit("lunghezza non conforme")
    version = max(site._version(), 627)
    article = {
        "slug": SLUG,
        "titolo": "Meteo Italia, sole e massime fino a 28 gradi fino al 3 ottobre",
        "sommario": (
            "Domenica 27 settembre il sole copre l’Italia, con massime fino a 28 gradi al Sud "
            "e notti fresche al Nord. La settimana resta in gran parte stabile: da giovedì "
            "qualche piovasco può tornare su Sicilia e Alpi."
        ),
        "categoria": "Meteo",
        "luogo": "Italia",
        "formato": "standard",
        "parole_chiave_titolo": ["fino a 28 gradi", "3 ottobre"],
        "dati_chiave": [
            {"valore": "27 settembre", "etichetta": "sole su tutta l’Italia", "icona": "◆"},
            {"valore": "fino a 28°", "etichetta": "massime al Sud", "icona": "▲"},
            {"valore": "da giovedì", "etichetta": "piovaschi su Sicilia e Alpi", "icona": "●"},
        ],
        "correlati": [
            {
                "url": "/notizie/meteo-italia-26-settembre-3-ottobre-2026.html",
                "titolo": "Meteo Italia, sole nel weekend: tendenza fino al 3 ottobre",
            },
            {
                "url": "/notizie/meteo-italia-25-settembre-2-ottobre-2026.html",
                "titolo": "Meteo Italia, rovesci e vento al Sud: weekend più stabile",
            },
            {
                "url": "/notizie/meteo-italia-24-settembre-1-ottobre-2026.html",
                "titolo": "Meteo Italia, rovesci locali oggi e venerdì: poi sole fino a mercoledì",
            },
        ],
        "paragrafi": PARAGRAFI,
        "fonti": [
            {
                "url": "https://www.corriere.it/cronache/26_settembre_27/domenica-di-sole-ovunque-massime-fino-a-28-gradi-al-sud-escursione-termica-di-notte-nelle-pianure-del-nord-317264b9-ba57-4170-8a4f-d37131178xlk.shtml",
                "descrizione": "Corriere della Sera — domenica 27 settembre 2026: sole, massime fino a 28 gradi al Sud, minime di 12-14 gradi al Nord; lunedì e martedì ancora stabili, con rovesci isolati sui rilievi.",
            },
            {
                "url": "https://www.meteo.it/notizie/meteo-weekend-stabile-con-caldo-di-nuovo-in-aumento-le-previsioni-ee74228b",
                "descrizione": "Meteo.it — aggiornamento del 27 settembre 2026, ore 7:09: tempo stabile, massime oltre i 26 gradi al Centro-Nord e sulle isole, venti e stato del mare.",
            },
            {
                "url": "https://www.ilmeteo.it/",
                "descrizione": "iLMeteo — 27 settembre 2026: sole prevalente almeno fino al 2 ottobre, massime di 27-29 gradi su molte città e più nubi da giovedì su Sicilia e Alpi centro-occidentali.",
            },
            {
                "url": "https://www.ilmeteo.it/meteo/Roma",
                "descrizione": "iLMeteo — bollettino di Roma aggiornato alle 7 del 27 settembre 2026: cielo poco nuvoloso, precipitazioni assenti, massima di 27 gradi.",
            },
            {
                "url": "https://www.meteoam.it/it/previsioni-fine-settimana",
                "descrizione": "Aeronautica Militare — tendenza dal 28 settembre al 4 ottobre 2026: anticiclone, temperature sopra la media e precipitazioni vicine o sotto la media secondo le zone.",
            },
        ],
    }
    image = {
        "key": f"{SLUG}-v{version}",
        "alt": "Mappa meteo editoriale dell’Italia per domenica 27 settembre 2026, con regioni, città principali, sole prevalente e tendenza fino al 3 ottobre.",
        "prompt": (
            "Mappa meteorologica editoriale dell’Italia per il 27 settembre 2026, orizzontale, "
            "con Sicilia e Sardegna, città principali, simboli di sole e qualche nube su Alpi "
            "occidentali, Calabria e Sicilia, più la striscia dei sette giorni fino al 3 ottobre."
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
    config = json.loads(config_path.read_text(encoding="utf-8"))
    config["version"] = max(int(config.get("version") or 0), version)
    config["articles"][f"/notizie/{article['slug']}.html"] = {
        "firstPublishedAt": article["published"],
        "homepagePriority": 94,
        "primaryCategory": "meteo",
    }
    config_path.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.sync_surfaces([article], f"/notizie/{article['slug']}.html", version)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = version
    manifest["site"]["site_version"] = version
    manifest["site_version"] = version
    manifest["version"] = f"v{version}"
    manifest["release_version"] = f"v{version}"
    manifest["last_release"] = {
        "version": version,
        "date": "2026-09-27",
        "type": "weather-service",
        "news_added": [article["slug"]],
        "news_updated": [],
        "change": "Meteo Italia dal 27 settembre al 3 ottobre 2026",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for filename in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            site_version=version,
            version=str(version),
            currentVersion=version,
            release_date="2026-09-27",
            last_update=f"{SLUG}-v{version}",
        )
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"slug": article["slug"], "version": version}, ensure_ascii=False))


if __name__ == "__main__":
    main()
