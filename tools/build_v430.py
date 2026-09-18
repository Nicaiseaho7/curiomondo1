#!/usr/bin/env python3
"""Pubblica visita Meloni a Beretta, 500 anni (v430)."""
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

VERSION = 430
PUBLISHED = "2026-09-18T17:50:00+02:00"
SLUG = "meloni-beretta-500-anni-gardone-val-trompia-18-settembre-2026"


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
    "titolo": "Meloni a Gardone per i 500 anni della Beretta. Poi le Frecce Tricolori",
    "sommario": "La premier è arrivata allo stabilimento con Lollobrigida. Visita al reparto produttivo, inaugurazione della Sala Innovation Habitat, sorvolo della Pattuglia acrobatica alle 16.45.",
    "categoria": "Politica",
    "luogo": "Gardone Val Trompia",
    "formato": "standard",
    "parole_chiave_titolo": ["Meloni", "Beretta"],
    "dati_chiave": [
        {"icona": "◆", "valore": "500", "etichetta": "anni della Fabbrica d’Armi Pietro Beretta"},
        {"icona": "●", "valore": "15:30", "etichetta": "orario in agenda a Palazzo Chigi"},
        {"icona": "↗", "valore": "16:45", "etichetta": "sorvolo delle Frecce Tricolori"},
    ],
    "paragrafi": [
        "Giorgia Meloni ha partecipato venerdì 18 settembre alle celebrazioni per i 500 anni della Fabbrica d’Armi Pietro Beretta a Gardone Val Trompia, in provincia di Brescia. L’agenda di Palazzo Chigi indicava le 15.30. Radiocor ha dato l’arrivo allo stabilimento alle 15.16.",
        "La premier era accompagnata dal ministro dell’Agricoltura Francesco Lollobrigida. Ad accoglierla il sottosegretario alla Difesa Matteo Perego di Cremnago, Pietro Gussalli Beretta, presidente di Beretta Holding, Franco Gussalli Beretta, presidente e ad della Fabbrica d’Armi, Carlo Ferlito, ad e direttore generale, e una delegazione di operai.",
        "Il programma ufficiale prevedeva la visita dell’area produttiva e l’inaugurazione della Sala Innovation Habitat. Presenti il sindaco Giuliano Brunori e il presidente della Comunità montana di Valle Trompia, Massimo Otelli. Sono fatti di presenza, non un decreto.",
        "Alle 16.45 Meloni è stata attesa al Centro sportivo Oratorio San Giovanni Bosco. Radiocor elenca il prefetto di Brescia Andrea Polichetti, il capo di Stato maggiore dell’Aeronautica, generale Antonio Conserva, e don Piero Minelli, parroco di Gardone. Lì la premier ha assistito al sorvolo della Pattuglia acrobatica nazionale.",
        "Il Comune di Gardone aveva già chiuso strade e parcheggi dalle 13. Per pochi minuti, indicativamente tra le 16.20 e le 16.40, era prevista la chiusura della ex SP BS345 per il passaggio delle Frecce. L’ordinanza è del municipio, non di Palazzo Chigi.",
        "Beretta ha sede a Gardone dal 1526. Il cinquecentenario cade nel 2026. L’azienda ha già messo in vendita, a settembre, un’edizione limitata SL3 da 150 pezzi per l’anniversario. Non è il tema della visita di governo: è un fatto di catalogo.",
        "Al momento della stesura Palazzo Chigi non ha pubblicato il testo di un discorso. Non attribuiamo quindi a Meloni frasi sul riarmo europeo o sui conti della difesa. Quello che è verificato è l’itinerario: cantiere, sala Innovation, Frecce.",
        "La fonte primaria dell’appuntamento è l’agenda della Presidenza. La conferma dell’arrivo e dei nomi è Radiocor, 15.16 e 15.28. Il Fatto Quotidiano ripete lo stesso elenco. Gardone Val Trompia, 18 settembre 2026.",
    ],
    "fonti": [
        {
            "url": "https://www.governo.it/it/agenda/2026-09-18t000000/celebrazioni-il-500-anniversario-della-fabbrica-beretta/32613",
            "descrizione": "Presidenza del Consiglio — agenda 18 settembre, 15.30, Gardone Val Trompia.",
        },
        {
            "url": "https://www.borsaitaliana.it/borsa/notizie/radiocor/finanza/dettaglio/beretta-meloni-giunta-allo-stabilimento-di-gardone-val-trompia-nRC_18092026_1516_406114664.html",
            "descrizione": "Radiocor 15:16 — arrivo, Lollobrigida, Gussalli Beretta, Ferlito, operai.",
        },
        {
            "url": "https://www.borsaitaliana.it/borsa/notizie/radiocor/finanza/dettaglio/beretta-meloni-giunta-allo-stabilimento-di-gardone-val-trompia-2-nRC_18092026_1528_417138827.html",
            "descrizione": "Radiocor 15:28 — Frecce Tricolori alle 16.45, Conserva, prefetto Polichetti.",
        },
        {
            "url": "https://www.ilfattoquotidiano.it/2026/09/18/meloni-beretta-500-anni-fondazione-notizie/8510772/",
            "descrizione": "Il Fatto Quotidiano — stesso elenco di presenze e programma.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/meloni-oslo-norvegia-gas-fen-saipem-17-settembre-2026.html",
            "titolo": "Meloni a Oslo: gas norvegese e intesa con FEN e Saipem",
        },
        {
            "url": "/notizie/bab-el-mandeb-crosetto-missione-navale-mercantili-italiani-17-settembre-2026.html",
            "titolo": "Crosetto, scorta della Marina ai mercantili italiani",
        },
        {
            "url": "/notizie/usa-f35-arabia-saudita-48-caccia-24-miliardi-18-settembre-2026.html",
            "titolo": "Usa, via libera a 48 F-35 per l’Arabia Saudita",
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
            ROOT / "generated_images" / "meloni-beretta-v430.jpg", f"{SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Giorgia Meloni riconoscibile all’aperto; somiglianza sintetica, non una fotografia documentaria della visita a Gardone.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": "Photorealistic editorial photograph of Giorgia Meloni outdoors with Italian flags, ordinary contextual portrait, no text.",
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
        "change": "Pubblicata la visita di Meloni a Gardone per i 500 anni Beretta",
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
                "last_update": "meloni-beretta-v430",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "scoop-20260918T175000-Europe-Rome.json",
        {
            "run_at": PUBLISHED,
            "skill": "ultime-notizie-scoop",
            "desks": ["sport", "cinema-serie", "politica", "cronaca"],
            "processed": [
                {
                    "title": ARTICLE["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "primary_source": "https://www.governo.it/it/agenda/2026-09-18t000000/celebrazioni-il-500-anniversario-della-fabbrica-beretta/32613",
                    "primary_time": "2026-09-18T13:11:00+02:00",
                    "arrival_confirmed": "2026-09-18T15:16:00+02:00",
                    "public_url": f"https://curiomondo.it/notizie/{SLUG}.html",
                }
            ],
            "discarded": [
                {"topic": "Monza-Sassuolo / Serie A", "reason": "partita alle 20:45, nessun risultato ufficiale"},
                {"topic": "Coppa Davis qualificazioni", "reason": "tie in corso, Italia già qualificata, parziali non chiudono la notizia"},
                {"topic": "Netflix Best of the Best", "reason": "uscita catalogo ufficiale ma impatto basso per il lettore italiano rispetto al protocollo 8/10"},
                {"topic": "Tajani Forum Acqua", "reason": "conferenza 16:00 in agenda, manca il comunicato post-evento con dichiarazioni verificabili"},
                {"topic": "cronaca questure", "reason": "nessun comunicato di polizia/carabinieri di oggi con fatto verificato e senza dati di vittime"},
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
