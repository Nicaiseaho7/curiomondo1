#!/usr/bin/env python3
"""Pubblica la sentenza Thaçi delle Camere specializzate per il Kosovo."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 384
SLUG = "kosovo-hashim-thaci-condannato-25-anni-crimini-guerra-16-settembre-2026"
PUBLISHED = "2026-09-16T17:37:18+02:00"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
FEATURED_URL = f"/notizie/{SLUG}.html"
IMAGE_KEY = f"hashim-thaci-ritratto-neutro-sentenza-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / "hashim-thaci-ritratto-neutro-v384.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Kosovo, l’ex presidente Hashim Thaçi condannato a 25 anni per crimini di guerra",
    "sommario": "Le Camere specializzate per il Kosovo hanno riconosciuto l’ex capo dell’UCK colpevole di omicidio, tortura, trattamento crudele e detenzione arbitraria. È stato assolto dalle accuse di crimini contro l’umanità e può presentare appello.",
    "categoria": "Mondo",
    "luogo": "L’Aia",
    "formato": "standard",
    "parole_chiave_titolo": ["Hashim Thaçi", "25 anni"],
    "dati_chiave": [
        {"icona": "◆", "valore": "25 anni", "etichetta": "la pena inflitta a Thaçi"},
        {"icona": "●", "valore": "4", "etichetta": "i crimini di guerra accertati"},
        {"icona": "▲", "valore": "96", "etichetta": "gli omicidi riconosciuti dal collegio"},
    ],
    "paragrafi": [
        "Le Camere specializzate per il Kosovo hanno condannato mercoledì 16 settembre 2026 l’ex presidente Hashim Thaçi a 25 anni di carcere. Il collegio dell’Aia lo ha riconosciuto colpevole di quattro crimini di guerra — omicidio, tortura, trattamento crudele e detenzione arbitraria — commessi durante il conflitto del 1998-1999.",
        "Secondo la sentenza, Thaçi partecipò attivamente e incoraggiò un’impresa criminale congiunta diretta contro oppositori politici e persone considerate collaboratrici delle forze serbe. Il tribunale ha accertato 96 omicidi, 385 detenzioni arbitrarie, 303 casi di tortura e 49 di trattamento crudele; le vittime non partecipavano alle ostilità quando furono colpite.",
        "Thaçi era il principale comandante dell’Esercito di liberazione del Kosovo, noto con la sigla UCK, e dopo la guerra divenne primo ministro e presidente. Si dimise dalla presidenza nel novembre 2020 per affrontare il processo. Ha sempre negato ogni accusa e potrà impugnare sia la condanna sia la pena.",
        "Il collegio ha assolto Thaçi e gli altri tre imputati da sei accuse di crimini contro l’umanità. I giudici hanno ritenuto non provato il requisito specifico di un attacco generalizzato o sistematico contro la popolazione civile. L’assoluzione su quei capi non cancella quindi l’accertamento dei quattro crimini di guerra.",
        "Kadri Veseli è stato condannato a 18 anni, Rexhep Selimi a 13 e Jakup Krasniqi a 25. La procura aveva chiesto 45 anni per ciascuno dei quattro ex dirigenti dell’UCK. Le pene potranno essere riesaminate in appello e la sentenza non è ancora definitiva.",
        "Il presidente del collegio, Charles Smith, ha precisato che il procedimento riguardava la responsabilità penale individuale degli imputati, non la legittimità dell’UCK o l’obiettivo dell’indipendenza. Questa distinzione è centrale perché in Kosovo gli ex comandanti sono considerati eroi da una parte rilevante della popolazione.",
        "Le Camere specializzate fanno parte dell’ordinamento kosovaro, ma hanno sede nei Paesi Bassi e impiegano giudici e personale internazionali. Furono istituite nel 2015 per esaminare presunti crimini commessi da membri dell’UCK, anche alla luce dei timori sulla protezione dei testimoni e delle difficoltà a celebrare i processi in Kosovo.",
        "La decisione ha provocato proteste all’Aia e manifestazioni a Pristina. Il suo impatto supera il destino personale di Thaçi: interviene su una memoria della guerra ancora contesa e può aggravare le tensioni politiche fra Kosovo e Serbia, che continua a non riconoscere l’indipendenza proclamata da Pristina nel 2008.",
    ],
    "fonti": [
        {"url": "https://www.scp-ks.org/en/hashim-thaci-and-co-defendants-found-guilty-war-crimes", "descrizione": "Camere specializzate per il Kosovo — comunicato ufficiale del 16 settembre 2026 con verdetto e pene."},
        {"url": "https://www.reuters.com/world/kosovo-ex-president-thaci-faces-war-crimes-verdict-hague-2026-09-16/", "descrizione": "Reuters — dettagli della sentenza, numeri delle vittime, motivazione e reazioni a Pristina e all’Aia."},
        {"url": "https://apnews.com/article/thaci-kosovo-serbia-war-crimes-0b24b81d6e1ca8f01d8b8b54bb465ee9", "descrizione": "Associated Press — conferma indipendente delle condanne, delle assoluzioni e delle pene per i quattro imputati."},
    ],
    "correlati": [
        {"url": "/notizie/ratko-mladic-morto-genocidio-srebrenica-27-agosto-2026.html", "titolo": "Ratko Mladić è morto all’Aia: resta la condanna definitiva per genocidio"},
        {"url": "/notizie/sudan-droni-sostegno-estero-crimini-guerra-rapporto-onu-3-settembre-2026.html", "titolo": "Sudan, il rapporto ONU documenta droni esteri e possibili crimini di guerra"},
        {"url": "/notizie/guerra-usa-iran-rapporto-ufficiale-scorte-sotto-pressione-e-basi-danneggiate-15-09-2026.html", "titolo": "Guerra USA-Iran, rapporto ufficiale su scorte e basi danneggiate"},
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
        "alt": "Ritratto editoriale neutrale generato con IA di Hashim Thaçi su sfondo blu scuro, realizzato per una notizia sensibile e non documentario.",
        "disclosure": CAPTION,
        "syntheticLikeness": "public-figure",
        "sensitiveContext": True,
        "portraitOnly": True,
        "portraitFormat": "neutral-isolated",
        "reenactedEvent": False,
        "prompt": "Sensitive-context neutral editorial portrait of Hashim Thaci, neutral isolated studio background, no reenacted event, no text or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    article_path = ROOT / "notizie" / f"{slug}.html"
    page = article_path.read_text(encoding="utf-8")
    import re
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    article_path.write_text(page, encoding="utf-8")
    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    items = sync_surfaces([ARTICLE], FEATURED_URL, VERSION)

    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": ARTICLE["titolo"],
        "excerpt": ARTICLE["sommario"],
        "category": "Mondo",
        "published_at": PUBLISHED,
        "updated_at": PUBLISHED,
        "status": "UFFICIALE",
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
        "date": "2026-09-16",
        "type": "content-release",
        "news_added": [SLUG],
        "news_updated": [],
        "change": "Nuovo articolo sulla condanna di Hashim Thaçi per crimini di guerra",
        "image_policy_applied": "new-openai-sensitive-public-figure-neutral-portrait",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": "2026-09-16",
            "release_date": "2026-09-16",
            "articleCount": int(state.get("articleCount", 261)) + 1,
            "generatedEditorialImages": int(state.get("generatedEditorialImages", 143)) + 1,
            "last_update": "hashim-thaci-sentenza-v384",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "mondo-20260916T173718-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "production_branch": "main",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 4,
            "target_reached": False,
            "note": "Conteggio prudenziale: comunicato e aggiornamento ufficiale KSC, Reuters e Associated Press; esclusi titoli, snippet e duplicati. Obiettivo non raggiunto; nessuna consultazione inventata.",
        },
        "processed": [{
            "slug": SLUG,
            "action": "new_article",
            "score": 9.2,
            "status": "UFFICIALE",
            "public_url": PUBLIC_URL,
            "sources": [source["url"] for source in ARTICLE["fonti"]],
            "publication_state": "pending_deploy",
        }],
    })

    from lxml import html
    doc = html.fromstring(article_path.read_text(encoding="utf-8"))
    assert doc.xpath('//main//h1[1]')[0].text_content() == ARTICLE["titolo"]
    assert len(doc.xpath('//article[contains(@class,"art-body")]/p')) == len(ARTICLE["paragrafi"])
    assert len(doc.xpath('//section[contains(@class,"curio-related")]//a')) == 3
    assert doc.xpath('//figure[@data-synthetic-likeness="public-figure"][@data-sensitive-context="true"][@data-portrait-format="neutral-isolated"]')
    assert any(item["url"] == f"/notizie/{SLUG}.html" for item in items)
    print(json.dumps({"status": "ok", "version": VERSION, "slug": slug}, ensure_ascii=False))


if __name__ == "__main__":
    main()
