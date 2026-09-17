#!/usr/bin/env python3
"""Pubblica il profilo italiano del Global Gender Gap Report 2026."""
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

VERSION = 397
SLUG = "parita-genere-italia-83-rapporto-wef-2026"
PUBLISHED = "2026-09-17T04:53:12+02:00"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-v{VERSION}"
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-96c9a2f8-9154-4391-9d4a-356045f64ee0.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Parità di genere, Italia 83ª nel rapporto WEF: è 121ª nell'economia",
    "sommario": "L'Italia sale di due posizioni nell'indice globale del World Economic Forum, ma resta 83ª su 145 economie. Il risultato più debole è nella partecipazione economica e nelle opportunità, dove il Paese si colloca al 121° posto.",
    "categoria": "Italia",
    "luogo": "Italia",
    "formato": "standard",
    "parole_chiave_titolo": ["Italia 83ª", "121ª nell'economia"],
    "dati_chiave": [
        {"icona": "◆", "valore": "83ª", "etichetta": "posizione complessiva dell'Italia"},
        {"icona": "↓", "valore": "121ª", "etichetta": "partecipazione economica e opportunità"},
        {"icona": "↑", "valore": "+2", "etichetta": "posizioni rispetto al 2025"},
    ],
    "paragrafi": [
        "L'Italia è all'83° posto su 145 economie nel Global Gender Gap Report 2026, pubblicato dal World Economic Forum il 16 settembre. Il Paese guadagna due posizioni rispetto all'edizione precedente, ma il profilo nazionale mostra un divario particolarmente ampio nella partecipazione economica e nelle opportunità.",
        "In questa componente l'Italia occupa infatti il 121° posto. Il sottoindice considera differenze tra donne e uomini nella partecipazione al lavoro, nel reddito stimato, nella presenza tra professionisti e tecnici e nell'accesso ai ruoli di legislazione, alta amministrazione e gestione d'impresa.",
        "Il risultato è migliore nella dimensione dell'empowerment politico, dove l'Italia si colloca al 61° posto. Le due graduatorie descrivono aspetti diversi: la presenza di una donna alla guida del governo non elimina automaticamente gli squilibri nella forza lavoro, nelle retribuzioni o nelle posizioni aziendali con maggiore potere decisionale.",
        "L'indice WEF non misura un livello assoluto di benessere e non assegna voti alle politiche dei governi. Confronta invece quanta parte del divario tra donne e uomini risulta chiusa in quattro aree: economia, istruzione, salute e sopravvivenza, rappresentanza politica. I punteggi sono costruiti su una scala da zero a uno e servono soprattutto a confrontare paesi e andamento nel tempo.",
        "Il quadro globale copre 145 economie. Secondo il WEF, nel 2026 è stato chiuso in media il 69,2% del divario complessivo, quattro decimi di punto in più rispetto al 2025. Al ritmo osservato nei vent'anni di serie storica, la parità mondiale resterebbe distante circa 120 anni: è una proiezione, non una scadenza certa.",
        "A livello mondiale le aree più vicine alla parità sono istruzione e salute, entrambe oltre il 96%. Le distanze maggiori rimangono nella partecipazione economica, al 61,7%, e soprattutto nel potere politico, al 22,1%. Il rapporto segnala inoltre che la presenza femminile diminuisce con l'aumento della seniority nelle organizzazioni.",
        "Per l'Italia, il 121° posto economico è rilevante anche per la crescita. Una precedente analisi nazionale rilanciata da Reuters indicava nel 2024 un tasso di occupazione femminile del 53,2%, con 17,8 punti di distanza dagli uomini. Sono dati di un'altra fonte e di un altro anno, ma aiutano a leggere il punto debole che riemerge nella graduatoria WEF.",
        "Il rapporto è quindi una fotografia comparativa, non una spiegazione causale completa. Per valutare gli interventi necessari occorre affiancare all'indice dati nazionali su occupazione, salari, lavoro involontariamente part-time, congedi, servizi di cura e carriere. L'83° posto registra un miglioramento relativo, mentre il 121° nella dimensione economica indica che il ritardo strutturale resta ampio.",
    ],
    "fonti": [
        {
            "url": "https://www.weforum.org/publications/global-gender-gap-report-2026/digest/",
            "descrizione": "World Economic Forum — rapporto ufficiale, metodologia, risultati globali e data di pubblicazione.",
        },
        {
            "url": "https://www.weforum.org/publications/global-gender-gap-report-2026/economy-profiles-global-gender-gap-report-2026/",
            "descrizione": "World Economic Forum — profili ufficiali delle 145 economie incluse nell'edizione 2026.",
        },
        {
            "url": "https://www.ansa.it/donne/notizie/2026/09/16/il-global-gender-gap-report-2026-la-parita-di-genere-fa-progressi-record-nel_94f9ce45-cfef-436d-a323-418f9e6a3eca.html",
            "descrizione": "ANSA — riscontro indipendente delle posizioni italiane complessiva, economica e politica.",
        },
        {
            "url": "https://www.reuters.com/business/italy-lags-peers-womens-employment-hampering-growth-report-shows-2026-03-18/",
            "descrizione": "Reuters — contesto indipendente sull'occupazione femminile italiana e sul divario con gli uomini.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/violenza-prima-dei-16-anni-l-istat-stima-3-milioni-di-donne-italiane-coinvolte-16-09-2026.html",
            "titolo": "Violenza prima dei 16 anni: i nuovi dati nazionali Istat",
        },
        {
            "url": "/notizie/lavoro-divario-nord-sud-cgia-5-settembre-2026.html",
            "titolo": "Lavoro, il divario tra Nord e Sud nei dati CGIA",
        },
        {
            "url": "/notizie/istat-economia-italiana-pil-industria-inflazione-luglio-agosto-2026.html",
            "titolo": "Economia italiana: PIL, industria e inflazione nei dati Istat",
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
        "alt": "Illustrazione editoriale IA di professioniste e professionisti riuniti in un ambiente di lavoro italiano; non rappresenta un evento specifico.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-realistic non-documentary editorial scene of diverse Italian professionals collaborating in a contemporary workplace, with women active in decision-making; natural morning light; no text, charts, logos or watermark.",
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
        "development_at": "2026-09-16",
        "development_time_note": "Il WEF indica la data del 16 settembre 2026, senza un orario esatto di pubblicazione.",
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
        "change": "Nuovo articolo sul profilo italiano del Global Gender Gap Report 2026",
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
            "last_update": "parita-genere-italia-wef-v397",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260917T044838-Europe-Rome.json", {
        "run_at": "2026-09-17T04:48:38+02:00",
        "scope": "Italia",
        "production_branch": "main",
        "base_commit": "92ddb34357bfbbfea3b589fc6a57b7954808c16b",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 8,
            "headlines_or_snippets_excluded_from_count": True,
            "target_reached": False,
            "note": "Conteggio prudenziale dei documenti effettivamente aperti e letti; la copertura è inferiore all'obiettivo e non include titoli o snippet.",
        },
        "processed": [{
            "title": ARTICLE["titolo"],
            "territorial_filter": "passed",
            "editorial_score": 8.2,
            "category": "Italia",
            "status": "UFFICIALE",
            "decision": "publish",
            "reason": "Rapporto ufficiale appena pubblicato con graduatorie nazionali rilevanti per lavoro, crescita e rappresentanza.",
            "sources": [source["url"] for source in ARTICLE["fonti"]],
            "public_url": PUBLIC_URL,
            "publication_state": "pending_deploy",
        }],
        "excluded": [
            {"topic": "Milano Greco Pirelli", "reason": "Nessun nuovo comunicato ufficiale sul ripristino completo rispetto all'articolo già pubblicato."},
            {"topic": "Lavoratore su una gru a Milano", "reason": "Evento locale senza elementi sufficienti per la soglia di rilevanza nazionale."},
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
