#!/usr/bin/env python3
"""Pubblica l'articolo sulla minaccia tariffaria USA dopo la proposta UE-Canada."""
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

VERSION = 398
SLUG = "trump-ue-canada-associazione-dazi-17-settembre-2026"
PUBLISHED = "2026-09-17T05:24:00+02:00"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-560bc53f-7fbd-481c-a5df-c40288b9eb2c.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Trump minaccia nuovi dazi all’UE per il progetto di associazione del Canada",
    "sommario": "Il presidente statunitense ha definito potenzialmente ostile la proposta di avvicinare il Canada all'Unione europea e ha minacciato dazi pesanti o restrizioni commerciali. Nessuna nuova tariffa è stata però adottata e il progetto UE-Canada non ha ancora regole definite.",
    "categoria": "Mondo",
    "luogo": "Charlotte / Bruxelles",
    "formato": "standard",
    "parole_chiave_titolo": ["nuovi dazi all’UE", "associazione del Canada"],
    "dati_chiave": [
        {"icona": "◆", "valore": "0", "etichetta": "nuovi dazi già adottati"},
        {"icona": "→", "valore": "1°", "etichetta": "associato UE proposto"},
        {"icona": "↔", "valore": "70%", "etichetta": "export canadese diretto agli USA"},
    ],
    "paragrafi": [
        "Donald Trump ha minacciato nuovi dazi pesanti contro l'Unione europea se il progetto di associare il Canada al blocco fosse diretto contro gli Stati Uniti. Il presidente statunitense è intervenuto nella serata del 16 settembre a Charlotte, in North Carolina, quando in Italia era già il 17 settembre. Nessuna nuova tariffa è stata però adottata.",
        "Trump ha definito l'ipotesi di un Canada associato all'UE potenzialmente un atto ostile e ha evocato anche la possibilità di interrompere gli scambi in alcuni settori. Associated Press, Financial Times e Guardian riportano la stessa minaccia formulata durante un comizio. Le dichiarazioni non precisano aliquote, merci interessate o tempi di applicazione.",
        "Il bersaglio politico è la proposta presentata il 16 settembre dalla presidente della Commissione europea Ursula von der Leyen. Nel discorso sullo Stato dell'Unione ha proposto di aprire al Canada una prima forma di associazione all'UE. La Commissione vuole estendere la cooperazione a industria, tecnologia, difesa, Artico, energia e materie prime critiche.",
        "Quella annunciata a Bruxelles non è un'adesione del Canada all'Unione europea. Non esiste ancora uno statuto definito di membro associato, né un testo normativo sottoposto ai Ventisette. Reuters e Financial Times segnalano che contenuti, base giuridica e percorso di approvazione devono essere costruiti; un'intesa di questa portata richiederebbe probabilmente l'accordo unanime degli Stati membri.",
        "UE e Canada dispongono già del CETA, applicato in via provvisoria dal 2017, e Ottawa ha aderito al programma europeo SAFE per gli acquisti comuni nella difesa. Von der Leyen propone ora una più ampia Alleanza per il futuro. Il vertice UE-Canada previsto in ottobre dovrebbe chiarire quali elementi possano diventare negoziati concreti.",
        "Per Ottawa la diversificazione ha un peso immediato: circa il 70% delle esportazioni canadesi è diretto negli Stati Uniti, secondo Associated Press. Le relazioni si sono deteriorate dopo l'aumento dei dazi statunitensi e il fallimento dei negoziati bilaterali. Un legame più stretto con l'Europa ridurrebbe la dipendenza, ma non sostituirebbe rapidamente il mercato americano.",
        "Per le imprese europee e italiane, l'effetto diretto oggi è soprattutto un aumento dell'incertezza politica. I dazi minacciati da Trump non sono in vigore e non si possono ancora stimare costi o comparti coinvolti. Eventuali conseguenze dipenderanno da atti formali degli Stati Uniti e dalla struttura che Bruxelles, Ottawa e i governi europei riusciranno eventualmente a negoziare.",
        "Il nuovo sviluppo è quindi l'escalation verbale tra Washington e Bruxelles, non la nascita di un nuovo regime commerciale. La proposta UE-Canada resta allo stadio politico e la risposta americana resta una minaccia. Separare questi piani è essenziale per evitare di trasformare una trattativa ancora senza regole in un accordo già concluso o in tariffe già applicate.",
    ],
    "fonti": [
        {
            "url": "https://cyprus.representation.ec.europa.eu/news/2026-state-union-address-president-von-der-leyen-2026-09-16_en",
            "descrizione": "Commissione europea — testo ufficiale del discorso sullo Stato dell'Unione e proposta di associazione del Canada.",
        },
        {
            "url": "https://apnews.com/article/4078e9549ff9caa5ded08f7dd2f99065",
            "descrizione": "Associated Press — riscontro delle dichiarazioni di Trump a Charlotte e delle minacce commerciali all'UE.",
        },
        {
            "url": "https://www.reuters.com/world/eu-opens-door-canada-become-first-associate-member-eu-commission-president-says-2026-09-16/",
            "descrizione": "Reuters — verifica indipendente della proposta europea, del contesto e degli elementi ancora da definire.",
        },
        {
            "url": "https://www.ft.com/content/7b0f8f90-b3ad-4640-916a-f8b5495920a3",
            "descrizione": "Financial Times — conferma indipendente della minaccia tariffaria e analisi del possibile iter europeo.",
        },
        {
            "url": "https://www.theguardian.com/world/2026/sep/17/trump-calls-eu-offer-to-canada-associate-membership-laughable-threatens-tariffs",
            "descrizione": "The Guardian — ulteriore conferma delle dichiarazioni durante il comizio in North Carolina.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/canada-ritorsioni-dazi-usa-8-settembre-22-agosto-2026.html",
            "titolo": "Canada, ritorsione sui dazi USA: nuove tariffe dall'8 settembre",
        },
        {
            "url": "/notizie/usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026.html",
            "titolo": "USA, la Camera approva le sanzioni alla Russia e possibili dazi fino al 100%",
        },
        {
            "url": "/notizie/ue-social-media-divieto-sotto-13-anni-proposta-von-der-leyen-16-settembre-2026.html",
            "titolo": "Social media, von der Leyen propone il divieto UE sotto i 13 anni",
        },
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
    out.mkdir(parents=True, exist_ok=True)
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
        "alt": "Illustrazione editoriale IA di un tavolo negoziale con bandiere di Unione europea, Canada e Stati Uniti davanti a un porto commerciale; non documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Photorealistic conceptual editorial meeting room with EU, Canadian and US flags, cargo port in the background, no people, text, graphics or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    article_path = ROOT / "notizie" / f"{slug}.html"
    page = article_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    article_path.write_text(page, encoding="utf-8")
    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    items = sync_surfaces([ARTICLE], "", VERSION)

    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": ARTICLE["titolo"],
        "excerpt": ARTICLE["sommario"],
        "category": ARTICLE["categoria"],
        "published_at": PUBLISHED,
        "updated_at": PUBLISHED,
        "development_at": "2026-09-17",
        "development_time_note": "Le dichiarazioni sono state rese la sera del 16 settembre a Charlotte, quando in Italia era già il 17 settembre; l'ora esatta non è indicata dalle fonti consultate.",
        "status": "CONFERMATA DA PIÙ FONTI",
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
        "change": "Nuovo articolo sulla minaccia tariffaria USA dopo la proposta UE-Canada",
        "image_policy_applied": "new-openai-contextual-editorial-image",
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
            "last_update": "trump-ue-canada-dazi-v398",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "mondo-20260917T050727-Europe-Rome.json", {
        "run_at": "2026-09-17T05:07:27+02:00",
        "scope": "Italia e mondo",
        "production_branch": "main",
        "base_commit": "f984e33",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 9,
            "headlines_or_snippets_excluded_from_count": True,
            "target_reached": False,
            "note": "Conteggio prudenziale dei documenti aperti e letti integralmente o nelle sezioni pertinenti; non include titoli, snippet o duplicati.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "editorial_score": 8.7,
            "category": "Mondo",
            "status": "CONFERMATA DA PIÙ FONTI",
            "decision": "publish",
            "reason": "Escalation commerciale tra Stati Uniti e UE su una proposta strategica che riguarda commercio, difesa e autonomia canadese.",
            "sources": [source["url"] for source in ARTICLE["fonti"]],
            "public_url": PUBLIC_URL,
            "publication_state": "pending_deploy",
        }],
        "excluded": [
            {"topic": "Bollo auto 2027", "reason": "Già pubblicato nel repository; escluso come duplicato."},
            {"topic": "Voto della Camera USA sulla guerra con l'Iran", "reason": "Sviluppo del 16 settembre in Italia, fuori dalla finestra di freschezza del giorno corrente."},
        ],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })

    from lxml import html
    doc = html.fromstring(article_path.read_text(encoding="utf-8"))
    assert doc.xpath('//main//h1[1]')[0].text_content() == ARTICLE["titolo"]
    assert len(doc.xpath('//article[contains(@class,"art-body")]/p')) == len(ARTICLE["paragrafi"])
    assert len(doc.xpath('//section[contains(@class,"curio-related")]//a')) == 3
    assert doc.xpath('//figure[@data-ai-generated="true"]')
    assert any(item["url"] == f"/notizie/{SLUG}.html" for item in items)
    print(json.dumps({"status": "ok", "version": VERSION, "slug": slug}, ensure_ascii=False))


if __name__ == "__main__":
    main()
