#!/usr/bin/env python3
"""Pubblica la proposta UE sui limiti di età per i social media."""
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

VERSION = 387
SLUG = "ue-social-media-divieto-sotto-13-anni-proposta-von-der-leyen-16-settembre-2026"
PUBLISHED = "2026-09-16T19:48:39+02:00"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
FEATURED_URL = f"/notizie/{SLUG}.html"
IMAGE_KEY = f"von-der-leyen-social-minori-ue-ai-openai-v{VERSION}"
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-75a1356e-a309-4530-8234-808f522af4bf.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Social media, von der Leyen propone il divieto UE sotto i 13 anni",
    "sommario": "La presidente della Commissione propone account vietati sotto i 13 anni, profili supervisionati fino a 15 e progettazione sicura fino a 18. Il piano non è ancora legge e dovrà essere definito, discusso e approvato.",
    "categoria": "Mondo",
    "luogo": "Strasburgo",
    "formato": "standard",
    "parole_chiave_titolo": ["divieto UE", "sotto i 13 anni"],
    "dati_chiave": [
        {"icona": "◆", "valore": "< 13", "etichetta": "accesso ai social da vietare"},
        {"icona": "●", "valore": "13–15", "etichetta": "solo account supervisionati"},
        {"icona": "▲", "valore": "15–18", "etichetta": "design sicuro obbligatorio"},
    ],
    "paragrafi": [
        "La presidente della Commissione europea Ursula von der Leyen ha proposto mercoledì 16 settembre 2026, a Strasburgo, di vietare l’accesso ai social media ai minori di 13 anni in tutta l’Unione. L’annuncio è arrivato durante il discorso sullo stato dell’Unione, ma non introduce ancora un divieto operativo.",
        "Il piano distingue tre fasce. Sotto i 13 anni non sarebbero ammessi account; tra 13 e 15 anni sarebbero consentiti soltanto profili limitati, creati e supervisionati dai genitori. Per gli utenti tra 15 e 18 anni, le piattaforme dovrebbero garantire servizi progettati in modo sicuro fin dall’origine.",
        "Von der Leyen ha collegato la proposta alle funzioni che favoriscono un uso compulsivo, alla diffusione di contenuti estremi e all’impiego delle fotografie delle ragazze per immagini sessualizzate generate con intelligenza artificiale. La Commissione vuole inoltre trasferire sulle piattaforme l’onere di dimostrare che i servizi destinati ai minori sono sicuri.",
        "La misura non è ancora una legge europea. I dettagli devono essere presentati e trasformati in una proposta normativa, che dovrà poi attraversare il normale negoziato fra Parlamento europeo e governi dei 27 Stati membri. Tempi, controlli sull’età, sanzioni e modalità tecniche restano quindi da definire.",
        "Molte piattaforme dichiarano già un’età minima di 13 anni, ma questa soglia dipende spesso dalla data di nascita inserita dall’utente. Il nodo pratico sarà verificare l’età senza raccogliere più dati personali del necessario e senza escludere ingiustamente chi non dispone degli strumenti richiesti.",
        "Il progetto europeo sarebbe più ampio di un semplice limite anagrafico perché disciplina anche le caratteristiche dei profili adolescenziali. Le funzioni disponibili, il tempo di utilizzo e la supervisione parentale diventerebbero elementi della regola, mentre per i maggiori di 15 anni resterebbe l’obbligo di un ambiente digitale sicuro.",
        "Il percorso può incontrare ostacoli politici, industriali e giuridici. Le grandi piattaforme statunitensi potrebbero opporsi a nuovi obblighi europei, mentre eventuali restrizioni dovranno essere compatibili con privacy, libertà di espressione e accesso all’informazione. In Francia, una precedente legge nazionale sui minori è stata bocciata dai giudici per problemi legati ai diritti fondamentali.",
        "Per famiglie e adolescenti non cambia nulla nell’immediato: gli account esistenti non vengono sospesi e non nasce oggi un nuovo controllo obbligatorio. La rilevanza dell’annuncio sta nell’intenzione della Commissione di uniformare regole oggi frammentate e di spostare la responsabilità della sicurezza dai soli genitori alle aziende tecnologiche.",
    ],
    "fonti": [
        {
            "url": "https://cyprus.representation.ec.europa.eu/news/2026-state-union-address-president-von-der-leyen-2026-09-16_en",
            "descrizione": "Commissione europea — testo ufficiale del discorso sullo stato dell’Unione con le tre fasce di età e l’onere di sicurezza per le piattaforme.",
        },
        {
            "url": "https://apnews.com/article/europe-leyen-social-media-ban-kids-3e7176ea409ba4af0a069f5ca7dd9680",
            "descrizione": "Associated Press — conferma della proposta, dell’iter ancora necessario e dei principali ostacoli politici e giuridici.",
        },
        {
            "url": "https://www.reuters.com/world/eus-von-der-leyen-invite-frontier-labs-talks-tackling-ai-risks-2026-09-16/",
            "descrizione": "Reuters — riscontro indipendente sul divieto sotto i 13 anni, sui profili personali sotto i 15 e sul contesto digitale del discorso.",
        },
        {
            "url": "https://www.euronews.com/my-europe/2026/09/16/state-of-the-union-five-takeaways-from-ursula-von-der-leyens-speech",
            "descrizione": "Euronews — ricostruzione del piano UE per la sicurezza digitale dei minori e del principio di sicurezza predefinita.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/tiktok-bytedance-400-milioni-privacy-minori-usa-22-agosto-2026.html",
            "titolo": "TikTok e ByteDance, accordo da 400 milioni negli USA sulla privacy dei minori",
        },
        {
            "url": "/notizie/come-funziona-coppa-privacy-minori-online.html",
            "titolo": "Privacy dei minori online: che cos’è la COPPA e quali obblighi impone",
        },
        {
            "url": "/notizie/comitato-parlamentare-britannico-chiede-una-legge-sull-ai-per-tutelare-i-diritti-umani-14-09-2026.html",
            "titolo": "Regno Unito, un comitato parlamentare chiede una legge sull’IA e i diritti umani",
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
        "alt": "Scena editoriale contestuale generata con IA con Ursula von der Leyen in un ambiente istituzionale europeo e uno smartphone con simbolo astratto di protezione dei minori; non documentaria.",
        "disclosure": CAPTION,
        "syntheticLikeness": "public-figure",
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ordinary contextual editorial synthetic likeness of Ursula von der Leyen in a European institutional setting, with a generic smartphone and child-safety shield; no specific speech reenacted, no text or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    article_path = ROOT / "notizie" / f"{slug}.html"
    page = article_path.read_text(encoding="utf-8")
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
        "category": ARTICLE["categoria"],
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
        "change": "Nuovo articolo sulla proposta UE per l’accesso dei minori ai social media",
        "image_policy_applied": "new-openai-ordinary-public-figure-contextual-image",
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
            "articleCount": int(state.get("articleCount", 263)) + 1,
            "generatedEditorialImages": int(state.get("generatedEditorialImages", 146)) + 1,
            "last_update": "ue-social-minori-v387",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "mondo-20260916T194839-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "production_branch": "main",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 4,
            "target_reached": False,
            "note": "Conteggio prudenziale: discorso ufficiale della Commissione europea, Associated Press, Reuters ed Euronews. Esclusi titoli, snippet e duplicati; nessuna consultazione inventata.",
        },
        "processed": [{
            "slug": SLUG,
            "action": "new_article",
            "score": 9.0,
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
    assert doc.xpath('//figure[@data-synthetic-likeness="public-figure"][@data-sensitive-context="false"]')
    assert any(item["url"] == f"/notizie/{SLUG}.html" for item in items)
    print(json.dumps({"status": "ok", "version": VERSION, "slug": slug}, ensure_ascii=False))


if __name__ == "__main__":
    main()
