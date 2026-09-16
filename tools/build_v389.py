#!/usr/bin/env python3
"""Pubblica la decisione FOMC del 16 settembre 2026."""
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

VERSION = 389
SLUG = "federal-reserve-alza-tassi-3-75-4-percento-16-settembre-2026"
PUBLISHED = "2026-09-16T21:14:24+02:00"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-ai-openai-v{VERSION}"
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-941f8adb-1189-4fa5-b4fd-64952851355f.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "La Federal Reserve alza i tassi al 3,75–4% e segnala un'altra stretta",
    "sommario": "Il FOMC ha aumentato il costo del denaro di 0,25 punti con voto unanime. Le nuove proiezioni indicano che sedici responsabili su diciotto prevedono almeno un altro rialzo entro fine anno, ma il percorso non è vincolante.",
    "categoria": "Mondo",
    "luogo": "Washington",
    "formato": "standard",
    "parole_chiave_titolo": ["Federal Reserve", "tassi al 3,75–4%"],
    "dati_chiave": [
        {"icona": "↑", "valore": "+0,25 punti", "etichetta": "rialzo deciso dal FOMC"},
        {"icona": "◆", "valore": "3,75–4,00%", "etichetta": "nuova fascia obiettivo"},
        {"icona": "●", "valore": "12–0", "etichetta": "voto unanime"},
    ],
    "paragrafi": [
        "La Federal Reserve ha aumentato mercoledì 16 settembre 2026 il tasso sui federal funds di un quarto di punto, portando la fascia obiettivo al 3,75–4%. La decisione è stata approvata all'unanimità dai dodici membri votanti. Reuters e Associated Press la indicano come il primo rialzo statunitense dal 2023.",
        "Il Federal Open Market Committee ha motivato la stretta con un'inflazione ancora elevata, nonostante un'attività economica definita solida. Nel comunicato ufficiale la banca centrale segnala consumi resilienti, investimenti produttivi robusti e un tasso di disoccupazione poco cambiato negli ultimi mesi.",
        "Le proiezioni pubblicate insieme alla decisione mostrano un tasso mediano del 4,1% sia a fine 2026 sia a fine 2027. Sedici dei diciotto responsabili prevedono per dicembre un livello almeno un quarto di punto sopra quello attuale. Queste stime individuali non costituiscono però un calendario promesso dal FOMC.",
        "La stessa tabella prevede per il 2026 una crescita reale del PIL del 2,3%, disoccupazione al 4,1% e inflazione PCE al 3,7%. La misura di fondo, che esclude alimentari ed energia, è stimata al 3,4%. Il ritorno dell'inflazione complessiva al 2% è indicato soltanto nel 2029.",
        "Il tasso deciso dalla Fed riguarda il mercato interbancario a brevissimo termine, ma influenza progressivamente il costo del credito nell'economia. Carte revolving, prestiti a tasso variabile e finanziamenti alle imprese possono diventare più cari; mutui e titoli a lunga scadenza dipendono anche da aspettative, rischio e domanda di mercato.",
        "Il nuovo intervallo non coincide quindi con il rendimento del Treasury decennale, che il 15 settembre ha superato il 5% negli scambi asiatici. Quel rendimento è formato sul mercato obbligazionario. La decisione della banca centrale può condizionarlo, ma non lo fissa direttamente e non produce un trasferimento automatico di pari ampiezza.",
        "È stata la prima variazione dei tassi sotto la presidenza di Kevin Warsh. La scelta contrasta con le richieste pubbliche del presidente Donald Trump per una riduzione del costo del denaro, ma il comunicato non entra nel confronto politico e concentra la motivazione sul mandato di stabilità dei prezzi e massima occupazione.",
        "Il voto unanime riduce l'incertezza sull'azione di settembre, non sul passo successivo. Le proiezioni mostrano differenze interne: due responsabili indicano un tasso fermo al livello attuale a dicembre, dodici un altro rialzo e quattro un livello ancora più alto. Dati su prezzi e lavoro potranno cambiare queste valutazioni.",
        "Per famiglie e imprese il dato più utile da seguire non è soltanto il prossimo annuncio della Fed. Conta anche la velocità con cui banche e mercati trasferiranno la stretta ai nuovi contratti. Il FOMC continuerà a valutare dati economici, rischi e condizioni finanziarie prima di decidere ulteriori mosse.",
    ],
    "fonti": [
        {
            "url": "https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm",
            "descrizione": "Federal Reserve — comunicato ufficiale del FOMC: rialzo, nuova fascia obiettivo, motivazioni e voto.",
        },
        {
            "url": "https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm",
            "descrizione": "Federal Reserve — proiezioni economiche di settembre 2026 e distribuzione delle attese sui tassi.",
        },
        {
            "url": "https://www.reuters.com/business/warshs-words-may-matter-more-than-anticipated-fed-rate-hike-2026-09-16/",
            "descrizione": "Reuters — conferma indipendente della decisione, del contesto storico e delle indicazioni per fine anno.",
        },
        {
            "url": "https://apnews.com/article/bab1bcb07e973bfb2dd0c3e5fbbb73b1",
            "descrizione": "Associated Press — conferma indipendente del primo rialzo in tre anni e del contesto politico ed economico.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/titoli-di-stato-il-rendimento-usa-a-10-anni-tocca-il-massimo-dal-2007.html",
            "titolo": "Titoli di Stato, il rendimento USA a 10 anni tocca il massimo dal 2007",
        },
        {
            "url": "/notizie/usa-inflazione-agosto-34-percento-fed-tassi-11-settembre-2026.html",
            "titolo": "USA, inflazione al 3,4% in agosto: aumenta la pressione sulla Fed",
        },
        {
            "url": "/notizie/usa-lavoro-luglio-posti-persi-mercati-fed-tassi.html",
            "titolo": "USA, il lavoro perde posti a luglio e riapre il dibattito sui tassi",
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
        "alt": "Scena editoriale ordinaria generata con IA della sede della Federal Reserve al crepuscolo, con simbolo percentuale e blocchi in crescita; non documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-realistic ordinary contextual editorial scene of the Federal Reserve headquarters at dusk, with a restrained percentage sculpture and unmarked rising blocks; no people, readable text, data, logo or watermark; not documentary.",
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
        "development_at": "2026-09-16T20:00:00+02:00",
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
        "change": "Nuovo articolo sulla decisione della Federal Reserve di alzare i tassi",
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
            "date": "2026-09-16",
            "release_date": "2026-09-16",
            "articleCount": 266,
            "generatedEditorialImages": 149,
            "last_update": "federal-reserve-rialzo-tassi-v389",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "mondo-20260916T211424-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "production_branch": "main",
        "production_commit_checked": "41cde0c",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 4,
            "target_reached": False,
            "note": "Conteggio prudenziale dei contenuti aperti integralmente per la notizia pubblicata: comunicato FOMC, proiezioni ufficiali, Reuters e Associated Press. Titoli e snippet non sono conteggiati.",
        },
        "processed": [{
            "slug": SLUG,
            "action": "new_article",
            "score": 9.5,
            "status": "UFFICIALE",
            "public_url": PUBLIC_URL,
            "sources": [source["url"] for source in ARTICLE["fonti"]],
            "publication_state": "pending_deploy",
        }],
        "excluded": [
            {"topic": "Attacco con drone contro un autobus in Ucraina", "reason": "Sviluppo del mattino, meno recente della decisione FOMC e con dettagli operativi ancora attribuiti alle parti in conflitto."},
            {"topic": "Francia e rinnovo delle sanzioni UE ad Alisher Usmanov", "reason": "Aggiornamento negoziale della vicenda già trattata, senza decisione finale nuova."},
        ],
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
