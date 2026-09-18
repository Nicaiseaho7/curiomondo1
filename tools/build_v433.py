#!/usr/bin/env python3
"""Pubblica BYD Music Awards stasera Arena (v433)."""
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

VERSION = 433
PUBLISHED = "2026-09-18T19:05:00+02:00"
SLUG = "byd-music-awards-arena-verona-conti-incontrada-rai1-18-settembre-2026"


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
            path, "WEBP", quality=86, method=6
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
    "titolo": "Music Awards stasera all’Arena: Conti, Incontrada e i big su Rai 1",
    "sommario": "Ventesima edizione, diretta alle 21.30. Premi FIMI e SIAE, non una gara. Palco sold out con Mengoni, Emma, Annalisa, Geolier, Elisa e Pooh.",
    "categoria": "Cultura",
    "luogo": "Verona",
    "formato": "standard",
    "parole_chiave_titolo": ["Music Awards", "Conti"],
    "dati_chiave": [
        {"icona": "◆", "valore": "21:30", "etichetta": "diretta Rai 1, venerdì 18 settembre"},
        {"icona": "●", "valore": "20ª", "etichetta": "edizione, Conti e Incontrada al quindicesimo anno"},
        {"icona": "↗", "valore": "FIMI/SIAE", "etichetta": "premi su certificazioni, non classifica di gara"},
    ],
    "paragrafi": [
        "Stasera, venerdì 18 settembre, l’Arena di Verona ospita la prima delle due serate dei BYD Music Awards. Diretta su Rai 1 alle 21.30, anche su RaiPlay. Conducono Carlo Conti e Vanessa Incontrada, insieme per il quindicesimo anno. È la ventesima edizione della manifestazione nata nel 2007.",
        "Non è un festival a classifica. I riconoscimenti copiano le certificazioni FIMI/NIQ: album Oro, Platino e Multiplatino, singoli Platino e Multiplatino usciti tra settembre 2025 e settembre 2026. I tour, certificati SIAE, valgono Oro a 100 mila presenze, Platino a 200 mila, Diamante a 300 mila.",
        "Sky TG24 elenca il palco delle due sere: tra gli altri Achille Lauro, Annalisa, Biagio Antonacci, Elisa, Emma, Geolier, Giorgia, Marco Mengoni, Max Pezzali, Olly, Pooh, Negramaro, Madame, Irama, Il Volo. L’Arena è sold out da mesi. Produzione FriendsTv per Rai Intrattenimento Prime Time.",
        "Il Fatto Quotidiano ha pubblicato una scaletta della serata del 18. Tra i nomi di stasera: Mengoni (medley con coro gospel), Emma, Antonacci, Olly, Annalisa, Alfa, Coez, Gigi D’Alessio, Notre Dame de Paris con Riccardo Cocciante. Non è la distinta ufficiale Rai: può cambiare in diretta.",
        "La seconda serata è sabato 19, stesso orario. Tra gli altri artisti del weekend: Elisa, Giorgia, Pooh, Geolier, Madame, Achille Lauro, The Kolors. Enrico Brignano e Giorgio Panariello sono indicati come presenza comica. Non pubblichiamo vincitori: i premi si consegnano in Arena.",
        "Conti e Incontrada restano i volti fissi. Il format premia i numeri di mercato, non una giuria da festival. Per questo sul palco convivono artisti da classifica e nomi di catalogo, dai Pooh a Kid Yugi.",
        "Resident Evil di Zach Cregger è uscito ieri in Italia e oggi negli Stati Uniti: è un’altra notizia di personaggi, già in sala, non un evento di stasera. Sinner si allena a Montecarlo: il rientro a Pechino non è confermato dal suo staff.",
        "Fonti: Sky TG24 (cast e criteri), Repubblica (edizione e date), Il Fatto (scaletta del 18). 18 settembre 2026, ore 19.05 Europe/Rome. Lo show non è ancora iniziato.",
    ],
    "fonti": [
        {
            "url": "https://tg24.sky.it/spettacolo/musica/2026/09/18/byd-music-awards-2026",
            "descrizione": "Sky TG24 — ventesima edizione, conduttori, cast, FIMI/SIAE, RaiPlay.",
        },
        {
            "url": "https://www.repubblica.it/spettacoli/musica/2026/09/11/news/bydmusic_awards_rai_arena_verona_date_programma-425579415/",
            "descrizione": "la Repubblica — date 18-19 settembre, Arena, elenco artisti.",
        },
        {
            "url": "https://www.ilfattoquotidiano.it/2026/09/18/byd-music-awards-con-marco-mengoni-biagio-antonacci-olly-annalisa-emma-per-festeggiare-il-ventennale-allarena-di-verona-la-scaletta-del-18-settembre/8509368/",
            "descrizione": "Il Fatto Quotidiano — scaletta indicata per la serata del 18 settembre.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/cinema-uscite-italia-14-20-settembre-2026.html",
            "titolo": "Cinema, le uscite in Italia dal 14 al 20 settembre",
        },
        {
            "url": "/notizie/stranger-things-tales-from-85-2-arriva-il-17-settembre-su-netflix-16-09-2026.html",
            "titolo": "Stranger Things: Tales from ’85, stagione 2 su Netflix",
        },
        {
            "url": "/notizie/pride-and-prejudice-netflix-3-dicembre-2026.html",
            "titolo": "Orgoglio e pregiudizio, la serie Netflix a dicembre",
        },
    ],
}


def main() -> None:
    image = {
        "key": f"{SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "syntheticLikeness": "public-figure",
        "variants": save_image_variants(
            ROOT / "generated_images" / "conti-music-awards-v433.jpg", f"{SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Carlo Conti riconoscibile, occhiali e abito scuro, palco notturno ispirato all’Arena di Verona; somiglianza sintetica, non è una fotografia documentaria della serata.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-photorealistic Carlo Conti with glasses, Arena di Verona stage lights, no text.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    stamp_dates(slug, PUBLISHED)
    ARTICLE["published"] = PUBLISHED
    html = (ROOT / "notizie" / f"{slug}.html").read_text(encoding="utf-8")
    html = html.replace(
        '<figure class="article-image" data-ai-generated="true">',
        '<figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false">',
    )
    (ROOT / "notizie" / f"{slug}.html").write_text(html, encoding="utf-8")
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
            "status": "CONFERMATA DA PIÙ FONTI",
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
        "change": "Pubblicati i Music Awards stasera all’Arena di Verona",
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
                "last_update": "music-awards-v433",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "scoop-20260918T190500-Europe-Rome.json",
        {
            "run_at": PUBLISHED,
            "skill": "ultime-notizie-scoop",
            "desks": ["personaggi-famosi"],
            "processed": [
                {
                    "title": ARTICLE["titolo"],
                    "status": "CONFERMATA DA PIÙ FONTI",
                    "decision": "publish",
                    "primary_source": "https://tg24.sky.it/spettacolo/musica/2026/09/18/byd-music-awards-2026",
                    "public_url": f"https://curiomondo.it/notizie/{SLUG}.html",
                }
            ],
            "discarded": [
                {"topic": "Sinner-Ferrero", "reason": "indiscrezione su allenatore, rientro non confermato dallo staff"},
                {"topic": "Mattarella Maschere teatro", "reason": "in agenda Quirinale 17.30, manca resoconto post-udienza"},
                {"topic": "Matano giuria Ballando", "reason": "annuncio tv, impatto sotto soglia rispetto ai Music Awards"},
                {"topic": "Resident Evil Cregger", "reason": "uscita italiana 17 settembre, già in sala"},
                {"topic": "Malika Ayane album", "reason": "intervista, non breaking"},
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
