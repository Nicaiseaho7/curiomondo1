#!/usr/bin/env python3
"""Aggiorna l'articolo EU KIDS Act con la proposta ufficiale del 17 settembre."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys

from lxml import etree, html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 404
SLUG = "ue-social-media-divieto-sotto-13-anni-proposta-von-der-leyen-16-settembre-2026"
PATH = ROOT / "notizie" / f"{SLUG}.html"
URL = f"/notizie/{SLUG}.html"
CANONICAL = f"https://curiomondo.it{URL}"
PUBLISHED = "2026-09-16T19:48:39+02:00"
UPDATED = "2026-09-17T10:16:00+02:00"
TITLE = "EU Kids Act, adottata la proposta sul divieto social sotto i 13 anni"
SUMMARY = (
    "Il testo prevede account autonomi dai 15 anni, profili supervisionati a 13 e 14 anni e "
    "obblighi di sicurezza per piattaforme, videogiochi e chatbot. Non è ancora legge: servirà "
    "l'accordo di Parlamento europeo e Consiglio."
)
SECTION = "Italia / Politica"
IMAGE_KEY = f"eu-kids-act-famiglie-italia-ai-openai-v{VERSION}"
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-0a07dc45-2882-48ee-95e4-3202f7cd0efd.png"
IMAGE_ALT = (
    "Scena editoriale contestuale generata con IA di una madre e un adolescente italiani che "
    "controllano insieme le impostazioni di uno smartphone; non documentaria."
)

BODY = [
    "La Commissione europea ha adottato giovedì 17 settembre 2026, a Bruxelles, la proposta di regolamento EU Kids Act. Il testo stabilisce regole comuni per proteggere i minori sui servizi digitali in tutti gli Stati membri, Italia compresa. Non è ancora legge e non modifica subito gli account esistenti.",
    "La proposta vieta gli account sui social media sotto i 13 anni. A 13 e 14 anni sarebbe ammesso soltanto un profilo limitato, creato e supervisionato da un genitore o tutore, con approvazione dei contatti e un limite giornaliero massimo di un'ora. Dai 15 anni si potrebbe aprire un account autonomo.",
    "Le soglie anagrafiche riguardano social network e piattaforme di condivisione video con caratteristiche considerate rischiose. Gli obblighi di progettazione sicura si estendono anche a giochi online, chatbot e assistenti di intelligenza artificiale, app store e sistemi operativi. Enciclopedie, piattaforme educative e siti di notizie rientrano tra le esenzioni proposte.",
    "Per i minori sarebbero vietati meccanismi progettati per favorire un uso compulsivo, come lo scorrimento infinito senza pause, alcune notifiche non richieste e le ricompense che penalizzano chi non torna ogni giorno. I sistemi di raccomandazione dovrebbero privilegiare sicurezza e qualità, mentre profili, contatti e dirette avrebbero impostazioni più restrittive.",
    "La verifica dell'età non potrebbe più basarsi soltanto sulla data di nascita dichiarata. La Commissione propone soluzioni certificate, compresa l'app europea di verifica, capaci di comunicare alla piattaforma soltanto il superamento o meno della soglia. Ogni Stato dovrebbe offrire almeno un metodo gratuito, anche a chi non dispone di identità digitale.",
    "Se il regolamento entrerà in vigore nella forma proposta, le piattaforme dovranno controllare entro sei mesi anche gli account già aperti. Gli utenti sotto i 15 anni, o quelli di cui non è possibile accertare l'età, dovrebbero passare al regime previsto o vedere disabilitato il profilo.",
    "Per la maggior parte degli adulti già riconosciuti come tali non sarebbe richiesto un nuovo controllo. L'obbligo scatterebbe quando il servizio non dispone di segnali sufficienti per stimare in modo affidabile l'età dell'utente.",
    "Le piattaforme con almeno 45 milioni di utenti attivi mensili nell'Unione dovrebbero presentare un piano di conformità e farlo verificare da revisori indipendenti. La proposta indica sanzioni fino al 6% del fatturato mondiale annuo e procedure accelerate, con rilievi preliminari entro 30 giorni e una decisione finale mirata entro 90.",
    "Il nuovo sviluppo è l'adozione formale della proposta da parte della Commissione, dopo l'annuncio politico del giorno precedente. Parlamento europeo e Consiglio dovranno ora negoziare e approvare il testo; soglie, controlli, sanzioni e tempi possono quindi cambiare. Fino alla conclusione dell'iter, in Italia non nasce alcun nuovo divieto operativo.",
]

SOURCES = [
    (
        "https://digital-strategy.ec.europa.eu/en/news/eu-kids-act-restrict-social-media-platforms-access-children-eu",
        "Commissione europea — comunicato ufficiale del 17 settembre 2026 sull'adozione della proposta EU KIDS Act.",
    ),
    (
        "https://digital-strategy.ec.europa.eu/en/faqs/kids-act-explained",
        "Commissione europea — domande e risposte ufficiali su fasce d'età, verifica, privacy, obblighi, sanzioni e iter.",
    ),
    (
        "https://www.ansa.it/sito/notizie/topnews/2026/09/17/lue-approva-il-kids-act-divieto-dei-social-per-gli-under_e9ce2fd4-9b14-4c10-9c2e-23200167950d.html",
        "ANSA — conferma dell'adozione della proposta e delle principali regole annunciate dalla Commissione.",
    ),
    (
        "https://www.reuters.com/legal/litigation/eu-is-set-propose-ban-social-media-ai-chatbots-under-15s-2026-09-14/",
        "Reuters — riscontro indipendente sul testo preparatorio, sul perimetro dei servizi e sull'iter necessario prima dell'entrata in vigore.",
    ),
    (
        "https://www.wired.com/story/the-eu-bans-social-media-for-under-13s/",
        "WIRED — conferma indipendente delle fasce d'età e analisi delle difficoltà di verifica, privacy e applicazione.",
    ),
]

RELATED = [
    ("/notizie/meta-accordo-1668-miliardi-danni-minori-social-26-agosto-2026.html", "Meta, accordo fino a 16,68 miliardi sulle accuse di danni ai minori"),
    ("/notizie/tiktok-bytedance-400-milioni-privacy-minori-usa-22-agosto-2026.html", "TikTok e ByteDance, accordo da 400 milioni sulla privacy dei minori"),
    ("/notizie/come-funziona-coppa-privacy-minori-online.html", "Privacy dei minori online: che cos'è la COPPA e quali obblighi impone"),
]


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
        target = out / f"{IMAGE_KEY}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            target, "WEBP", quality=84, method=6
        )
        variants.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{target.name}",
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "bytes": target.stat().st_size,
        })
    return variants


def update_article(image: dict) -> None:
    doc = html.fromstring(PATH.read_text(encoding="utf-8"))
    doc.xpath("//title")[0].text = TITLE + " | CurioMondo"
    for xpath, value in [
        ('//meta[@name="description"]', SUMMARY),
        ('//meta[@property="og:title"]', TITLE),
        ('//meta[@property="og:description"]', SUMMARY),
        ('//meta[@property="og:image"]', f"https://curiomondo.it{image['variants'][-1]['src']}"),
        ('//meta[@property="og:image:alt"]', IMAGE_ALT),
    ]:
        node = doc.xpath(xpath)
        if node:
            node[0].set("content", value)

    schema_node = doc.xpath('//script[@type="application/ld+json"]')[0]
    schema = json.loads(schema_node.text)
    schema.update({
        "headline": TITLE,
        "description": SUMMARY,
        "datePublished": PUBLISHED,
        "dateModified": UPDATED,
        "image": [f"https://curiomondo.it{image['variants'][-1]['src']}"],
        "creditText": site.CAPTION,
    })
    schema_node.text = json.dumps(schema, ensure_ascii=False, separators=(",", ":"))

    doc.xpath('//main//div[contains(@class,"badge")][1]')[0].text = SECTION
    doc.xpath('//main//h1[1]')[0].text = TITLE
    doc.xpath('//main//p[contains(@class,"subtitle")][1]')[0].text = SUMMARY
    meta = doc.xpath('//main//div[contains(@class,"meta")][1]')[0]
    for child in list(meta):
        meta.remove(child)
    meta.text = "16 settembre 2026 · aggiornato il 17 settembre 2026 alle 10:16 · Bruxelles · "
    etree.SubElement(meta, "span", id="readTime").text = "3 min di lettura"

    figure = doc.xpath('//figure[contains(@class,"article-image")][1]')[0]
    variants = {v["w"]: v["src"] for v in image["variants"]}
    replacement = html.fragment_fromstring(
        f'<figure class="article-image" data-ai-generated="true" data-sensitive-context="false"><picture>'
        f'<img src="..{variants[800]}" srcset="..{variants[480]} 480w, ..{variants[800]} 800w, '
        f'..{variants[1200]} 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" '
        f'width="800" height="533" alt="{IMAGE_ALT}" loading="eager" decoding="async" '
        f'fetchpriority="high"></picture><figcaption>{site.CAPTION}</figcaption></figure>'
    )
    figure.getparent().replace(figure, replacement)

    insight = doc.xpath('//section[contains(@class,"cm-insight")][1]')[0]
    replacement = html.fragment_fromstring(
        '<section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span>'
        '<div class="cm-insight-grid"><div><strong>&lt; 13</strong><span>nessun account social</span></div>'
        '<div><strong>13–14</strong><span>solo profili supervisionati</span></div>'
        '<div><strong>15 anni</strong><span>età minima per un account autonomo</span></div></div></section>'
    )
    insight.getparent().replace(insight, replacement)

    body = doc.xpath('//article[contains(@class,"art-body")][1]')[0]
    for child in list(body):
        body.remove(child)
    for paragraph in BODY:
        etree.SubElement(body, "p").text = paragraph

    related = doc.xpath('//section[contains(@class,"curio-related")]//div[contains(@class,"curio-related-grid")]')[0]
    for child in list(related):
        related.remove(child)
    for href, label in RELATED:
        anchor = etree.SubElement(related, "a", href=href)
        etree.SubElement(anchor, "strong").text = label

    sources = doc.xpath('//div[contains(@class,"art-sources")][1]')[0]
    ul = sources.xpath('./ul')[0]
    for child in list(ul):
        ul.remove(child)
    for href, label in SOURCES:
        li = etree.SubElement(ul, "li")
        etree.SubElement(li, "a", href=href, rel="noopener noreferrer", target="_blank").text = label
    note = sources.xpath('.//p[small]')[0]
    for child in list(note):
        note.remove(child)
    small = etree.SubElement(note, "small")
    strong = etree.SubElement(small, "strong")
    strong.text = "Redazione CurioMondo · "
    etree.SubElement(strong, "a", href="/pagine/metodo-editoriale.html").text = "Come lavoriamo"
    strong[-1].tail = (
        "\nTesto originale CurioMondo. Aggiornamento sostanziale verificato il 17 settembre 2026 "
        "alle 10:16 italiane. " + site.CAPTION
    )

    for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'):
        link.set("href", f"../assets/css/curiomondo-article-v211.css?v={VERSION}")
    for script in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'):
        script.set("src", f"../assets/js/curiomondo-article-v210.js?v={VERSION}")
    PATH.write_text("<!doctype html>\n" + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")


def prime_feed_metadata() -> None:
    path = ROOT / "assets" / "data" / "home-feed-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for item in data.get("items", []):
        if item.get("url") == URL:
            item["title"] = TITLE
            item["excerpt"] = SUMMARY
            item["section"] = SECTION
            break
    write_json(path, data)


def update_records(image: dict, items: list[dict]) -> None:
    image_record = dict(image)
    image_record["article"] = URL
    path = ROOT / "assets" / "data" / "editorial-images-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = VERSION
    data["items"] = [image_record] + [i for i in data.get("items", []) if i.get("article") != URL]
    write_json(path, data)

    live_path = ROOT / "automation" / "live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    live["updated_at"] = "2026-09-17T08:16:00+00:00"
    live["items"] = [
        {"title": i["title"], "url": i["url"], "published_at": i["dateISO"], "source": "CurioMondo", "article_exists": True}
        for i in items[:10]
    ]
    write_json(live_path, live)

    write_json(ROOT / "contenuti" / "notizie" / f"{SLUG}.json", {
        "slug": SLUG,
        "title": TITLE,
        "excerpt": SUMMARY,
        "category": SECTION,
        "published_at": PUBLISHED,
        "updated_at": UPDATED,
        "development_at": "2026-09-17T10:16:00+02:00",
        "status": "UFFICIALE",
        "status_note": "È ufficiale l'adozione della proposta da parte della Commissione; il regolamento non è ancora approvato né in vigore.",
        "body": BODY,
        "sources": [{"url": href, "label": label} for href, label in SOURCES],
        "image": image_record,
    })

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-17",
        "type": "content-update",
        "news_added": [],
        "news_updated": [SLUG],
        "change": "EU KIDS Act: proposta ufficiale adottata dalla Commissione, dettagli applicativi e iter legislativo",
        "image_policy_applied": "new-openai-contextual-editorial-image-for-substantive-update",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        state_path = ROOT / filename
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": "2026-09-17",
            "release_date": "2026-09-17",
            "generatedEditorialImages": max(int(state.get("generatedEditorialImages", 0)), 196),
            "last_update": "eu-kids-act-proposta-ufficiale-v404",
        })
        write_json(state_path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260917T105331-Europe-Rome.json", {
        "run_at": "2026-09-17T10:53:31+02:00",
        "production_branch": "main",
        "production_base_commit": "a250e9a1f5055faf250d440c56f243dce5395b98",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 6,
            "headlines_or_snippets_excluded_from_count": True,
            "target_reached": False,
            "note": "Conteggio prudenziale: comunicato, panoramica e FAQ della Commissione, ANSA, Reuters e WIRED. Esclusi titoli, snippet, paywall e duplicati; nessuna consultazione inventata.",
        },
        "processed": [{
            "slug": SLUG,
            "action": "updated_existing_article",
            "editorial_score": 9.1,
            "category": "Politica",
            "status": "UFFICIALE",
            "status_note": "Ufficiale l'adozione della proposta da parte della Commissione; non ancora legge.",
            "sources": [href for href, _ in SOURCES],
            "public_url": CANONICAL,
            "publication_state": "pending_deploy",
        }],
        "excluded": [
            {"topic": "Prezzi dei carburanti del 17 settembre", "reason": "Rialzo quotidiano rilevante ma senza sviluppo autonomo sufficiente rispetto all'articolo già pubblicato su bollo e accise; voto inferiore a 8/10."},
            {"topic": "Caso Roggero, rigettato il differimento pena", "reason": "Sviluppo giudiziario locale sotto la soglia di rilevanza nazionale."},
        ],
        "publication": {"site_version": VERSION, "state": "pending_deploy"},
    })


def qa(items: list[dict]) -> None:
    doc = html.fromstring(PATH.read_text(encoding="utf-8"))
    schema = json.loads(doc.xpath('//script[@type="application/ld+json"]')[0].text)
    assert doc.xpath('//h1')[0].text == TITLE
    assert doc.xpath('//main//div[contains(@class,"badge")][1]')[0].text == SECTION
    assert schema["datePublished"] == PUBLISHED and schema["dateModified"] == UPDATED
    assert len(doc.xpath('//article[contains(@class,"art-body")]/p')) == len(BODY)
    assert len(doc.xpath('//div[contains(@class,"art-sources")]//li')) == len(SOURCES)
    assert len(doc.xpath('//section[contains(@class,"curio-related")]//a')) == 3
    assert doc.xpath('//figure[@data-ai-generated="true"][@data-sensitive-context="false"]')
    assert any(i["url"] == URL and i["section"] == SECTION for i in items)
    assert len({i["url"] for i in items}) == len(items)
    politica = (ROOT / "categorie" / "politica" / "index.html").read_text(encoding="utf-8")
    mondo = (ROOT / "categorie" / "mondo" / "index.html").read_text(encoding="utf-8")
    assert URL in politica and URL not in mondo


def main() -> None:
    image = {
        "key": IMAGE_KEY,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(),
        "alt": IMAGE_ALT,
        "disclosure": site.CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ordinary contextual editorial scene of an Italian parent and a 14-year-old reviewing smartphone privacy settings at home; generic representation, no public figure, text, logo or watermark.",
    }
    update_article(image)
    prime_feed_metadata()
    metadata = {
        "slug": SLUG,
        "parole_chiave_titolo": ["EU Kids Act", "social vietati"],
        "dati_chiave": [
            {"icona": "◆", "valore": "< 13", "etichetta": "nessun account social"},
            {"icona": "●", "valore": "13–14", "etichetta": "solo profili supervisionati"},
            {"icona": "↗", "valore": "15 anni", "etichetta": "account autonomo"},
        ],
    }
    items = site.sync_surfaces([metadata], "", VERSION)
    update_records(image, items)
    qa(items)
    position = next(i for i, item in enumerate(items, 1) if item["url"] == URL)
    print(json.dumps({"version": VERSION, "updated": URL, "feed_position": position, "status": "ok"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
