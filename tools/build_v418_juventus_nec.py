#!/usr/bin/env python3
"""Pubblica il 5-0 della Juventus sul NEC in Europa League."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 418
PUBLISHED = "2026-09-17T23:55:56+02:00"
DEVELOPMENT = "2026-09-17T22:50:00+02:00"
SLUG = "juventus-nec-5-0-europa-league-17-settembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / f"{SLUG}.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Juventus-NEC 5-0, goleada all'esordio in Europa League",
    "sommario": "A Torino segnano Nico González, Alajbegović, Woltemade, Çelik e Kolo Muani. I bianconeri chiudono la prima giornata al comando per differenza reti.",
    "categoria": "Sport",
    "luogo": "Torino",
    "formato": "standard",
    "parole_chiave_titolo": ["5-0", "Europa League"],
    "dati_chiave": [
        {"icona": "◆", "valore": "5-0", "etichetta": "risultato finale a Torino"},
        {"icona": "↗", "valore": "5", "etichetta": "marcatori diversi"},
        {"icona": "●", "valore": "+5", "etichetta": "differenza reti iniziale"},
    ],
    "paragrafi": [
        "La Juventus ha battuto 5-0 il NEC giovedì 17 settembre all'Allianz Stadium di Torino, nella prima giornata della fase campionato di Europa League. La squadra di Luciano Spalletti ha conquistato tre punti con cinque marcatori diversi e senza subire reti.",
        "Nico González ha aperto il risultato al 9', sfruttando un lancio del portiere Kamil Grabara. Kerim Alajbegović ha raddoppiato al 24' dopo uno scambio con Weston McKennie; al 35' Nick Woltemade ha trasformato il rigore assegnato per un fallo su González.",
        "Il 3-0 dell'intervallo ha permesso ai bianconeri di gestire la ripresa. Zeki Çelik ha segnato al 75' su assist di Randal Kolo Muani, che all'82' ha superato il portiere avversario e fissato il risultato sul 5-0 dopo il lancio di Jhon Lucumí.",
        "Grabara ha debuttato con la Juventus dal primo minuto, secondo la ricostruzione di ANSA. Spalletti ha schierato McKennie alle spalle di Woltemade e ha inserito Kolo Muani al 71': il francese ha prodotto un assist e un gol nei venti minuti finali.",
        "Il successo assegna alla Juventus la migliore differenza reti della prima giornata. La classifica UEFA la colloca al primo posto con tre punti e +5, davanti al Crystal Palace, vincitore 4-0 sul Lech Poznań. È un vantaggio iniziale, non un risultato decisivo nella corsa alla qualificazione.",
        "La fase campionato comprende otto partite per ciascuna squadra e terminerà il 28 gennaio 2027. Il prossimo impegno europeo della Juventus è in programma il 15 ottobre in casa del Celta Vigo; seguirà la gara interna con il Rennes il 22 ottobre.",
        "Il 5-0 arriva quattro giorni dopo la sconfitta per 3-2 sul campo del Sassuolo in Serie A. Il confronto tra i due risultati misura la reazione immediata della squadra, ma competizione e avversario sono diversi e non consentono di trarre conclusioni sul rendimento stagionale.",
        "Sono ufficiali il risultato, i marcatori e il calendario pubblicato dalla UEFA. L'orario preciso del fischio finale non è indicato nelle fonti ufficiali consultate; le cronache in tempo reale hanno registrato la conclusione della gara intorno alle 22:50, ora italiana.",
    ],
    "fonti": [
        {"url": "https://www.uefa.com/uefaeuropaleague/match/2050066--juventus-vs-n-e-c/", "descrizione": "UEFA — referto ufficiale di Juventus-NEC nella prima giornata di Europa League."},
        {"url": "https://www.juventus.com/it/news/articoli/uefa-europa-league-juventus-nec-la-partita", "descrizione": "Juventus — risultato, sequenza dei gol, formazioni e tabellino della partita."},
        {"url": "https://www.ansa.it/sito/notizie/sport/calcio/2026/09/17/europa-league-la-juventus-asfalta-5-0-il-nec_6e175d87-1b2f-479a-89bb-cc9982cc094c.html", "descrizione": "ANSA — conferma indipendente del risultato e contesto sul debutto di Grabara."},
        {"url": "https://www.theguardian.com/football/live/2026/sep/17/real-sociedad-v-bournemouth-crystal-palace-v-lech-poznan-and-more-europa-league-live", "descrizione": "The Guardian — risultati finali e classifica completa dopo la prima giornata."},
    ],
    "correlati": [
        {"url": "/notizie/europa-league-oggi-milan-benfica-e-tutte-le-partite-del-16-settembre-orari-e-tv-16-09-2026.html", "titolo": "Europa League, risultati e calendario della prima giornata"},
        {"url": "/notizie/rally-italia-sardegna-finale-mondiale-wrc-2026.html", "titolo": "Rally Italia Sardegna diventa la finale del Mondiale WRC 2026"},
        {"url": "/notizie/italia-semifinale-mondiali-basket-carrozzina-2026.html", "titolo": "Mondiali di basket in carrozzina: Italia in semifinale dopo 16 anni"},
    ],
}


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def save_image_variants() -> list[dict]:
    image = Image.open(SOURCE_IMAGE).convert("RGB")
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
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{IMAGE_KEY}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=84, method=6
        )
        variants.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return variants


def main() -> None:
    image = {
        "key": IMAGE_KEY,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(),
        "alt": "Scena editoriale contestuale generata con IA con Nico González e Randal Kolo Muani insieme ad altri giocatori della Juventus in uno stadio di Torino dopo una partita europea; non documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "syntheticLikeness": "public-figure",
        "reenactedEvent": False,
        "prompt": "Scena editoriale contestuale ultrarealistica con Nico González, Randal Kolo Muani e compagni della Juventus in uno stadio di Torino; nessun testo o watermark; non documentaria.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page = re.sub(r'Ultimo aggiornamento editoriale: [^.<]+\.', "Ultimo aggiornamento editoriale: 17 settembre 2026, ore 23:55 italiane.", page)
    page_path.write_text(page, encoding="utf-8")

    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], "", VERSION)

    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": ARTICLE["titolo"],
        "excerpt": ARTICLE["sommario"],
        "category": "Sport",
        "published_at": PUBLISHED,
        "updated_at": PUBLISHED,
        "development_at": DEVELOPMENT,
        "development_time_precision": "circa; l'orario esatto del fischio finale non è indicato nelle fonti ufficiali",
        "status": "UFFICIALE",
        "public_url": PUBLIC_URL,
        "publication_state": "pending_deploy",
        "body": ARTICLE["paragrafi"],
        "sources": ARTICLE["fonti"],
        "image": image,
    })

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-17",
        "type": "content-release",
        "news_added": [SLUG],
        "news_updated": [],
        "change": "Pubblicato il 5-0 della Juventus sul NEC in Europa League",
        "image_policy_applied": "new-openai-contextual-public-figure-editorial-image-no-text",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": "2026-09-17",
            "release_date": "2026-09-17",
            "articleCount": int(state.get("articleCount", 0)) + 1,
            "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 1,
            "last_update": "sport-juventus-nec-europa-league-v418",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260917T234953-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Italia / Sport",
        "production_branch": "main",
        "base_commit": "d72e4ae4d55854cf325efc35a5c247e5d823a012",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 4,
            "distinct_domains": 4,
            "target_reached": False,
            "note": "Conteggio prudenziale: letti integralmente referto e calendario UEFA, resoconto ufficiale Juventus, cronaca ANSA e diretta The Guardian. Titoli e snippet non sono conteggiati.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "slug": SLUG,
            "editorial_score": 8.5,
            "status": "UFFICIALE",
            "decision": "publish",
            "development_at": DEVELOPMENT,
            "sources": [x["url"] for x in ARTICLE["fonti"]],
            "public_url": PUBLIC_URL,
            "publication_state": "pending_deploy",
        }],
        "excluded": [
            {"candidate": "Nuovi dettagli sul finanziamento del decreto bollo auto", "editorial_score": 6.8, "reason": "sviluppo secondario già coperto nell'articolo aggiornato alle 22:17; nessun nuovo atto autonomo"},
            {"candidate": "Studio IMBIE sui ghiacci polari", "reason": "già presente nel ramo di produzione corrente; escluso come duplicato"},
        ],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })
    print(json.dumps({"status": "ok", "version": VERSION, "added": SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
