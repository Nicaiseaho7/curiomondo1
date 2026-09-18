#!/usr/bin/env python3
"""Pubblica programma 5a giornata Serie A (v431)."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 431
PUBLISHED = "2026-09-18T18:10:00+02:00"
SLUG = "serie-a-quinta-giornata-orari-tv-monza-sassuolo-roma-inter-18-settembre-2026"


def save_image_variants(source: Path, key: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 3 / 2
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    out = ROOT / "assets" / "images" / "editorial-auto"
    out.mkdir(parents=True, exist_ok=True)
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=84, method=6
        )
        variants.append(
            {
                "w": width,
                "src": f"/assets/images/editorial-auto/{path.name}",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
        )
    return variants


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stamp_dates(slug: str, published: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{published}"', page)
    path.write_text(page, encoding="utf-8")


ARTICLE = {
    "slug": SLUG,
    "titolo": "Serie A, quinta giornata: stasera Monza-Sassuolo, sabato Roma-Inter",
    "sommario": "Anticipo alle 20.45 al Brianteo, diretta DAZN, Sky e NOW. Juric convoca 25 giocatori. Il weekend si chiude domenica con Juventus-Atalanta e Milan-Lecce.",
    "categoria": "Sport",
    "luogo": "Monza",
    "formato": "standard",
    "parole_chiave_titolo": ["Serie A", "Monza"],
    "dati_chiave": [
        {"icona": "◆", "valore": "20:45", "etichetta": "Monza-Sassuolo, venerdì 18 settembre"},
        {"icona": "●", "valore": "18:00", "etichetta": "Roma-Inter, sabato 19 settembre"},
        {"icona": "↗", "valore": "25", "etichetta": "convocati ufficiali del Monza"},
    ],
    "paragrafi": [
        "La quinta giornata di Serie A Enilive si apre stasera, venerdì 18 settembre, con Monza-Sassuolo alle 20.45 allo stadio Brianteo. Lo ha messo in calendario la Lega Serie A. La partita è in diretta su DAZN, Sky Sport e NOW.",
        "Il Monza ha pubblicato i convocati: 25 nomi. Portieri Tornqvist, Thiam e Strajnar. In lista anche Mangas, Folorunsho, Colpani, Varela, Zeballos, Cutrone e Carboni. Ivan Juric, in conferenza, ha detto che in porta giocherà Tornqvist. Non è la distinta gara.",
        "Il Sassuolo non ha messo online una lista ufficiale. Alberto Aquilani ha indicato sette indisponibili: Boloca, Pieragnolo, Koné, Candé, Walukiewicz, Volpato e Idzes. Idzes ha una lesione al quadricipite sinistro dopo Sassuolo-Juventus. Sono assenze da conferenza, non da comunicato federale.",
        "Sabato 19 settembre: Bologna-Torino e Udinese-Cagliari alle 15, Roma-Inter alle 18, Venezia-Lazio alle 20.45. La Lega ha definito Roma-Inter «supersfida». Tutte le gare sono su DAZN; Venezia-Lazio anche su Sky e NOW.",
        "Domenica 20 settembre: Fiorentina-Napoli alle 12.30, Frosinone-Como e Parma-Genoa alle 15, Juventus-Atalanta alle 18, Milan-Lecce alle 20.45. Juventus-Atalanta e il posticipo di San Siro chiudono il turno. Sky copre anche Juventus-Atalanta.",
        "Non pubblichiamo formazioni di giornale come undici ufficiale. La distinta arriva un’ora prima del fischio. Monza-Sassuolo non è ancora iniziata: niente risultato, niente voto.",
        "NBA: questo weekend non ci sono partite. I training camp aprono il 29 settembre, il preseason il 3 ottobre, la regular season il 20-21 ottobre, secondo il calendario NBA. I Grizzlies hanno annunciato il camp a Belmont, Nashville, dal 29 settembre al 2 ottobre: non è un match.",
        "Stasera, quindi, il solo palinsesto italiano da seguire è il Brianteo. Fonti: Lega Serie A per gli orari, sito Monza per i convocati, conferenza Aquilani per i sette out. 18 settembre 2026, ore 18 Europe/Rome.",
    ],
    "fonti": [
        {
            "url": "https://www.legaseriea.it/serie-a/news/date-orari-e-programmazione-tv-delle-prime-cinque-giornate",
            "descrizione": "Lega Serie A — date e orari delle prime cinque giornate, inclusa la quinta.",
        },
        {
            "url": "https://www.acmonza.com/it/news/monza-sassuolo-i-convocati-170926/",
            "descrizione": "AC Monza — convocati ufficiali per Monza-Sassuolo, 20.45 al Brianteo.",
        },
        {
            "url": "https://www.today.it/sport/calcio/serie-a-quinta-giornata-orari-sky-dazn.html",
            "descrizione": "Today — orari e diritti TV DAZN/Sky della quinta giornata.",
        },
        {
            "url": "https://pr.nba.com/",
            "descrizione": "NBA Communications — preseason dal 3 ottobre, nessuna gara il 18-20 settembre.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/juventus-nec-5-0-europa-league-17-settembre-2026.html",
            "titolo": "Juventus-NEC 5-0, esordio in Europa League",
        },
        {
            "url": "/notizie/nba-kawhi-leonard-torna-a-toronto-trade-ufficiale-con-i-raptors-15-09-2026.html",
            "titolo": "NBA, Kawhi Leonard torna a Toronto",
        },
        {
            "url": "/notizie/milan-benfica-oggi-16-settembre-2026-europa-league-orario-tv.html",
            "titolo": "Milan-Benfica, orario e TV in Europa League",
        },
    ],
}


def main() -> None:
    image = {
        "key": f"{SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "serie-a-5a-v431.jpg", f"{SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: stadio italiano illuminato in serata, senza stemmi di club; non è la fotografia documentaria di una partita.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Photorealistic Italian football stadium at dusk, floodlights, empty pitch, no crests, no text.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    stamp_dates(slug, PUBLISHED)
    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    write_json(
        ROOT / "contenuti" / "notizie" / f"{slug}.json",
        {
            "slug": slug,
            "title": ARTICLE["titolo"],
            "excerpt": ARTICLE["sommario"],
            "category": ARTICLE["categoria"],
            "published_at": PUBLISHED,
            "updated_at": PUBLISHED,
            "development_at": "2026-09-18",
            "status": "UFFICIALE",
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": ARTICLE["paragrafi"],
            "sources": ARTICLE["fonti"],
            "image": image,
        },
    )
    sync_surfaces([ARTICLE], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-18",
        "type": "content-release",
        "news_added": [SLUG],
        "news_updated": [],
        "change": "Pubblicato il programma della quinta giornata di Serie A",
        "image_policy_applied": "new-openai-contextual-editorial-images",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if not path.exists():
            continue
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            {
                "currentVersion": VERSION,
                "site_version": VERSION,
                "version": str(VERSION),
                "date": "2026-09-18",
                "release_date": "2026-09-18",
                "articleCount": int(state.get("articleCount", 0)) + 1,
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 1,
                "last_update": "serie-a-5a-v431",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "scoop-20260918T181000-Europe-Rome.json",
        {
            "run_at": PUBLISHED,
            "skill": "ultime-notizie-scoop",
            "desks": ["nba", "calcio", "programmi-partite"],
            "processed": [
                {
                    "title": ARTICLE["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "primary_source": "https://www.legaseriea.it/serie-a/news/date-orari-e-programmazione-tv-delle-prime-cinque-giornate",
                    "kickoff": "2026-09-18T20:45:00+02:00",
                    "public_url": f"https://curiomondo.it/notizie/{SLUG}.html",
                }
            ],
            "discarded": [
                {
                    "topic": "NBA partite del weekend",
                    "reason": "nessuna gara NBA il 18-20 settembre; training camp dal 29, preseason dal 3 ottobre",
                },
                {
                    "topic": "formazioni Monza-Sassuolo",
                    "reason": "solo convocati ufficiali e conferenze; distinta non ancora pubblicata",
                },
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
