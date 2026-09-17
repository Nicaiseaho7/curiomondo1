#!/usr/bin/env python3
"""Pubblica il record nordamericano di Spider-Man: Brand New Day."""
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

VERSION = 409
PUBLISHED = "2026-09-17T15:42:27+02:00"
SLUG = "spider-man-brand-new-day-record-box-office-nord-america-17-settembre-2026"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / f"{SLUG}.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Spider-Man supera Star Wars: record da 936,8 milioni in Nord America",
    "sommario": "Brand New Day raggiunge 936,77 milioni di dollari tra Stati Uniti e Canada e supera di circa 111 mila dollari Il risveglio della Forza. In Italia il film resta al cinema, con oltre 38,2 milioni di euro registrati da Cinetel.",
    "categoria": "Film e serie TV",
    "luogo": "Los Angeles",
    "formato": "standard",
    "parole_chiave_titolo": ["Spider-Man supera Star Wars", "936,8 milioni"],
    "dati_chiave": [
        {"icona": "◆", "valore": "$936,77 mln", "etichetta": "incasso Nord America"},
        {"icona": "↗", "valore": "+$110.909", "etichetta": "sul precedente primato"},
        {"icona": "●", "valore": "€38,28 mln", "etichetta": "incasso complessivo in Italia"},
    ],
    "paragrafi": [
        "Spider-Man: Brand New Day è diventato il film con il maggiore incasso nominale di sempre al box office nordamericano. Il totale aggiornato da Box Office Mojo al 15 settembre è di 936.773.134 dollari tra Stati Uniti e Canada, sopra i 936.662.225 dollari accumulati da Star Wars: Il risveglio della Forza.",
        "Lo scarto è di appena 110.909 dollari, calcolato sui due totali disponibili. Il primato riguarda gli incassi lordi non corretti per l'inflazione: non misura quindi il numero di biglietti venduti e non consente di confrontare direttamente il potere d'acquisto del 2026 con quello del 2015.",
        "Anche il dato mondiale va tenuto separato. Brand New Day ha raggiunto 2.453.024.087 dollari complessivi, dei quali 1.516.250.953 fuori da Stati Uniti e Canada. Sono valori ancora suscettibili di aumento, perché la programmazione nelle sale prosegue.",
        "In Italia il film è distribuito da Eagle Pictures ed è arrivato nei cinema il 29 luglio. Cinetel registra, fino al 15 settembre, 38.279.671 euro e 4.753.835 presenze complessive; nel periodo stagionale iniziato il 1° agosto, l'incasso è di 28.582.510 euro con 3.529.447 spettatori.",
        "Per chi deve ancora vederlo, le pagine ufficiali di Sony Pictures ed Eagle Pictures lo indicano ancora in programmazione cinematografica. Nelle fonti controllate non risulta invece una data italiana ufficiale per noleggio, acquisto digitale o streaming: eventuali annunci esteri non vanno trasferiti automaticamente al catalogo italiano.",
        "Il film è diretto da Destin Daniel Cretton e scritto da Chris McKenna ed Erik Sommers. Tom Holland torna nel ruolo di Peter Parker accanto a Zendaya, Sadie Sink, Jacob Batalon, Jon Bernthal, Tramell Tillman, Michael Mando e Mark Ruffalo, secondo il cast pubblicato da Sony.",
        "Il sorpasso è stato riportato il 16 settembre da più testate statunitensi, dopo che Associated Press aveva documentato l'avvicinamento del film al precedente massimo. CurioMondo ha verificato il dato sui totali disponibili il 17 settembre: il margine molto ridotto rende importante indicare sempre la data dell'ultimo aggiornamento.",
    ],
    "fonti": [
        {"url": "https://www.boxofficemojo.com/release/rl2299756545/", "descrizione": "Box Office Mojo — incassi nordamericani, internazionali e mondiali di Spider-Man: Brand New Day aggiornati al 15 settembre 2026."},
        {"url": "https://amministrazione.cinetel.it/pages/boxoffice.php?edperiodo=c3RhZ2lvbmFsZQ%3D%3D", "descrizione": "Cinetel — incassi e presenze ufficialmente rilevati in Italia fino al 15 settembre 2026."},
        {"url": "https://www.sonypictures.com/movies/spidermanbrandnewday", "descrizione": "Sony Pictures — scheda ufficiale con cast, regia e disponibilità nelle sale."},
        {"url": "https://eaglepictures.com/spiderman-brand-new-day", "descrizione": "Eagle Pictures — pagina del distributore italiano e stato della programmazione nazionale."},
        {"url": "https://people.com/spider-man-beats-star-wars-the-force-awakens-as-top-movie-ever-in-north-america-12124189", "descrizione": "People — riscontro indipendente del sorpasso, pubblicato il 16 settembre 2026."},
        {"url": "https://www.hollywoodreporter.com/movies/movie-news/spider-man-brand-new-day-domestic-box-office-force-awakens-1236703398/", "descrizione": "The Hollywood Reporter — conferma indipendente del nuovo primato nordamericano."},
    ],
    "correlati": [
        {"url": "/notizie/cinema-uscite-italia-14-20-settembre-2026.html", "titolo": "Cinema, sette uscite tra 16 e 17 settembre: film e streaming in Italia"},
        {"url": "/notizie/pride-and-prejudice-netflix-3-dicembre-2026.html", "titolo": "Pride and Prejudice arriva su Netflix il 3 dicembre 2026"},
        {"url": "/notizie/stranger-things-tales-from-85-2-arriva-il-17-settembre-su-netflix-16-09-2026.html", "titolo": "Stranger Things: Tales From ’85 2 arriva il 17 settembre su Netflix"},
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
        "alt": "Ritratto editoriale fotorealistico generato con IA di Tom Holland in un foyer cinematografico, con abito blu scuro e illuminazione rossa e blu.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "syntheticLikeness": "public-figure",
        "portraitFormat": "editorial-contextual-portrait",
        "reenactedEvent": False,
        "prompt": "Neutral ultrarealistic editorial portrait of adult actor Tom Holland standing alone in a contemporary cinema foyer; dark navy suit, warm red and blue ambient light; no text, logos, charts, posters or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    page_path = ROOT / "notizie" / f"{slug}.html"
    page = page_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    page = page.replace('<div class="badge">Mondo / Film e serie TV</div>', '<div class="badge">Film e serie TV</div>', 1)
    page = page.replace(
        'data-sensitive-context="false">',
        'data-sensitive-context="false" data-portrait-format="editorial-contextual-portrait">',
        1,
    )
    page_path.write_text(page, encoding="utf-8")
    ARTICLE["published"] = PUBLISHED
    ARTICLE["category_full"] = "Film e serie TV"
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], "", VERSION)
    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": ARTICLE["titolo"],
        "excerpt": ARTICLE["sommario"],
        "category": "Film e serie TV",
        "published_at": PUBLISHED,
        "updated_at": PUBLISHED,
        "development_at": "2026-09-16T18:44:00+02:00",
        "status": "CONFERMATA DA PIÙ FONTI",
        "status_note": "Il totale è verificato sui dati di box office e riscontrato da più testate indipendenti; il record riguarda dollari nominali non corretti per l'inflazione.",
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
        "change": "Pubblicato il record nordamericano di Spider-Man: Brand New Day",
        "image_policy_applied": "new-openai-public-figure-contextual-portrait-no-text-no-logo",
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
            "last_update": "cinema-spider-man-box-office-v409",
        })
        write_json(path, state)
    write_json(ROOT / "automation" / "logs" / "cinema-20260917T154227-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "scope": "Cinema e serie / box office",
        "production_branch": "main",
        "base_commit": "13188db5e2e1dd2b4b088ecd58eaf8ae8910fb05",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 9,
            "distinct_domains": 7,
            "target_reached": False,
            "note": "Conteggio prudenziale: esclusi snippet, duplicati e pagine bloccate da paywall. Sono state lette le schede dati Box Office Mojo e Cinetel, le pagine ufficiali Sony ed Eagle, il riscontro completo di People e ulteriori pagine editoriali; candidature meno recenti o insufficientemente rilevanti sono state scartate.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "editorial_score": 9.1,
            "status": "CONFERMATA DA PIÙ FONTI",
            "decision": "publish",
            "sources": [x["url"] for x in ARTICLE["fonti"]],
            "public_url": PUBLIC_URL,
            "publication_state": "pending_deploy",
        }],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })
    print(json.dumps({"status": "ok", "version": VERSION, "added": SLUG}, ensure_ascii=False))


if __name__ == "__main__":
    main()
