#!/usr/bin/env python3
"""Pubblica Istat produzione costruzioni luglio 2026 (v429)."""
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

VERSION = 429
PUBLISHED = "2026-09-18T17:40:00+02:00"
SLUG = "istat-produzione-costruzioni-luglio-calo-14-18-settembre-2026"


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
    "titolo": "Istat: produzione nelle costruzioni -1,4% a luglio, seconda flessione di fila",
    "sommario": "Calo anche dell’1,2% su base annua. Nei primi sette mesi l’indice resta in crescita. Comunicato ufficiale uscito stamattina alle 10.",
    "categoria": "Economia",
    "luogo": "Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["Istat", "costruzioni"],
    "dati_chiave": [
        {"icona": "◆", "valore": "-1,4%", "etichetta": "luglio su giugno, destagionalizzato"},
        {"icona": "●", "valore": "-1,2%", "etichetta": "luglio su luglio 2025"},
        {"icona": "↗", "valore": "+2,0%", "etichetta": "primi sette mesi, indice grezzo"},
    ],
    "paragrafi": [
        "L’Istat ha stimato venerdì 18 settembre che a luglio la produzione nelle costruzioni è scesa dell’1,4% rispetto a giugno. È la seconda flessione consecutiva dell’indice destagionalizzato. Il comunicato è uscito alle 10, ora di Roma, dal sito ufficiale.",
        "Su base annua, sia l’indice grezzo sia quello corretto per il calendario segnano -1,2%. I giorni lavorativi di luglio 2026 sono 23, come a luglio 2025. Non è un effetto di calendario: il confronto è a parità di giornate.",
        "Nella media maggio-luglio la produzione cala dello 0,8% sui tre mesi precedenti. Il trimestre è quindi già in contrazione, non solo il mese. L’Istat lo scrive nello stesso comunicato.",
        "Nei primi sette mesi del 2026 il quadro resta diverso. L’indice grezzo sale del 2,0% sullo stesso periodo del 2025. Quello corretto per il calendario cresce dell’1,3%. Il calo di luglio non cancella il livello accumulato da gennaio.",
        "Il valore aggiunto è questo scarto. Un mese e un trimestre in discesa, un cumulato ancora positivo. Chi legge solo il -1,4% descrive una caduta; chi legge solo i sette mesi descrive una crescita. Entrambi i numeri sono dell’Istituto.",
        "DPA ha ripreso gli stessi dati Istat, confermando il secondo calo mensile consecutivo. Non è una fonte indipendente sul cantiere: è un’agenzia che rilancia il comunicato. La fonte primaria resta Istat.",
        "Il comunicato non scompone edilizia e opere pubbliche. Non indica occupati né prezzi delle case. Non è un verdetto sul Superbonus né sul Piano casa. È un indice di volume della produzione.",
        "La prossima diffusione è fissata al 20 ottobre, per agosto. Fino ad allora luglio resta l’ultimo dato. Istat, Roma, 18 settembre 2026, ore 10.",
    ],
    "fonti": [
        {
            "url": "https://www.istat.it/comunicato-stampa/produzione-nelle-costruzioni-luglio-2026/",
            "descrizione": "Istat — produzione nelle costruzioni, luglio 2026. Comunicato ufficiale ore 10.",
        },
        {
            "url": "https://www.nampa.org/text/23019002",
            "descrizione": "DPA via NAMPA — stesso nucleo: secondo calo consecutivo a luglio.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/italia-produzione-industriale-giugno-2026-calo-istat.html",
            "titolo": "Produzione industriale, -1% a giugno secondo l’Istat",
        },
        {
            "url": "/notizie/istat-economia-italiana-pil-industria-inflazione-luglio-agosto-2026.html",
            "titolo": "Istat, economia italiana: Pil, industria e inflazione",
        },
        {
            "url": "/notizie/giorgetti-eurogruppo-shock-energia-bollette-18-settembre-2026.html",
            "titolo": "Giorgetti: lo shock delle guerre peserà sulle bollette",
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
            ROOT / "generated_images" / "istat-costruzioni-v429.jpg", f"{SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: cantiere italiano con ponteggi, senza persone riconoscibili; non è una fotografia documentaria di un cantiere specifico.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Photorealistic Italian construction site, scaffolding, no identifiable people, no text.",
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
        "change": "Pubblicato il dato Istat sulla produzione nelle costruzioni di luglio",
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
                "last_update": "istat-costruzioni-v429",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "scoop-20260918T174000-Europe-Rome.json",
        {
            "run_at": PUBLISHED,
            "skill": "ultime-notizie-scoop",
            "primary_first": True,
            "processed": [
                {
                    "title": ARTICLE["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "primary_source": "https://www.istat.it/comunicato-stampa/produzione-nelle-costruzioni-luglio-2026/",
                    "primary_time": "2026-09-18T10:00:00+02:00",
                    "public_url": f"https://curiomondo.it/notizie/{SLUG}.html",
                }
            ],
            "discarded": [
                {
                    "topic": "Meloni a Gardone per i 500 anni Beretta",
                    "reason": "cerimonia confermata da agenda e Radiocor, ma senza testo ufficiale del discorso: materia insufficiente senza riempitivo",
                },
                {
                    "topic": "Monza-Sassuolo",
                    "reason": "partita alle 20:45, nessun risultato",
                },
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
