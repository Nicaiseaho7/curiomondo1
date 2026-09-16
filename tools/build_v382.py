#!/usr/bin/env python3
"""Pubblica l'annuncio sul bollo auto, mantenendo espliciti i punti ancora aperti."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article
VERSION = 382
SLUG = "bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026"
PUBLISHED = "2026-09-16T16:48:39+02:00"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
FEATURED_URL = "/notizie/pride-and-prejudice-netflix-3-dicembre-2026.html"
IMAGE_KEY = f"{SLUG}-ai-openai-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / "bollo-auto-v382.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Bollo auto, il governo annuncia l’esenzione per 14,5 milioni di veicoli",
    "sommario": "Palazzo Chigi annuncia l’esenzione per tutti i motocicli e oltre il 70% delle auto piccole e medie, limitata a un veicolo per cittadino. Mancano ancora testo normativo, soglie di potenza, decorrenza e costo per i conti pubblici.",
    "categoria": "Italia",
    "luogo": "Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["Bollo auto", "14,5 milioni"],
    "dati_chiave": [
        {"icona": "◆", "valore": "14,5 milioni", "etichetta": "veicoli indicati dal governo"},
        {"icona": "●", "valore": ">70%", "etichetta": "auto piccole e medie coinvolte"},
        {"icona": "1", "valore": "un veicolo", "etichetta": "agevolabile per cittadino"},
    ],
    "paragrafi": [
        "Il governo italiano ha annunciato mercoledì 16 settembre 2026 l’esenzione dal bollo per circa 14,5 milioni di veicoli. Secondo le informazioni diffuse da Palazzo Chigi, la misura riguarderebbe tutti i motocicli e oltre il 70% delle auto di piccola e media potenza, con il limite di un solo veicolo agevolato per ciascun cittadino.",
        "L’annuncio è arrivato mentre la misura veniva presentata come parte dei provvedimenti destinati al Consiglio dei ministri. La presidente del Consiglio Giorgia Meloni ha dichiarato che l’esecutivo intende cancellare una delle tasse più odiate dagli italiani. Questa dichiarazione documenta l’impegno politico, ma non sostituisce il testo della norma.",
        "Al momento della pubblicazione non risultavano disponibili il provvedimento approvato, le soglie di potenza che separeranno i veicoli inclusi da quelli esclusi, la data di decorrenza e le modalità con cui il beneficiario dovrà indicare il mezzo prescelto. Non è stato comunicato neppure il costo complessivo per i conti pubblici.",
        "Per i proprietari, quindi, non cambia ancora l’obbligo di pagare le scadenze già dovute. Il bollo è una tassa automobilistica regionale o provinciale legata al possesso del veicolo: l’ACI ricorda che importi, scadenze ed esenzioni dipendono anche dalle regole applicabili nel territorio di residenza.",
        "L’estensione a tutti i motocicli e alla maggior parte delle auto piccole e medie darebbe alla misura una portata nazionale molto ampia. Il vincolo di un veicolo per cittadino significa però che chi possiede più mezzi non potrebbe applicare l’agevolazione a ciascuno di essi.",
        "Resta da chiarire come sarà trattato un veicolo cointestato, quali categorie tecniche rientreranno nella definizione di piccola e media potenza e se l’esenzione opererà automaticamente attraverso gli archivi pubblici oppure richiederà una scelta del contribuente. Qualsiasi risposta prima del testo ufficiale sarebbe soltanto un’ipotesi.",
        "Un altro nodo riguarda i rapporti finanziari con Regioni e Province autonome, destinatarie del gettito ordinario della tassa automobilistica. L’annuncio non specifica quale compensazione verrà prevista né attraverso quale strumento legislativo sarà introdotta. Questi dettagli saranno decisivi per valutare la copertura e l’applicazione uniforme della misura.",
        "Reuters ha confermato i dati centrali diffusi dall’ufficio della presidente del Consiglio: 14,5 milioni di veicoli, tutti i motocicli, oltre il 70% delle auto piccole e medie e un solo mezzo agevolato per persona. L’agenzia precisa che il governo non ha indicato l’impatto sui conti pubblici.",
        "La notizia resta IN SVILUPPO. È ufficiale che Palazzo Chigi ha annunciato la misura e ne ha indicato la platea generale; non è ancora accertata l’entrata in vigore dell’esenzione. I contribuenti dovranno attendere il testo approvato e le successive istruzioni degli enti competenti prima di modificare i pagamenti.",
    ],
    "fonti": [
        {"url": "https://www.ansa.it/sito/notizie/topnews/2026/09/16/fonti-chigi-oggi-in-cdm-via-il-bollo-per-auto-piccole-e-medie_1b5355cb-7110-4a5c-824f-314b8bed52da.html", "descrizione": "Palazzo Chigi, dichiarazione e dati della misura riportati da ANSA il 16 settembre 2026 alle 16:12."},
        {"url": "https://www.reuters.com/business/italy-scraps-road-tax-most-cars-election-nears-2026-09-16/", "descrizione": "Reuters — conferma indipendente della platea annunciata e dell’assenza di una stima ufficiale del costo."},
        {"url": "https://www.aci.it/servizi/guida-al-bollo-auto/", "descrizione": "Automobile Club d’Italia — disciplina vigente e guida istituzionale alla tassa automobilistica."},
    ],
    "correlati": [
        {"url": "/notizie/bonus-colonnine-domestiche-2026-domande-dal-22-settembre.html", "titolo": "Bonus colonnine domestiche 2026: domande dal 22 settembre"},
        {"url": "/notizie/codice-strada-patente-17-anni-superamento-destra-proposte-mit-2026.html", "titolo": "Codice della Strada, patente a 17 anni e superamento a destra: le proposte del MIT"},
        {"url": "/notizie/diesel-sconto-accise-proroga-17-settembre-2026.html", "titolo": "Diesel, prorogato fino al 17 settembre lo sconto di 17 centesimi"},
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
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=84, method=6)
        variants.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return variants


def main() -> None:
    image = {
        "key": IMAGE_KEY,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "variants": save_image_variants(),
        "alt": "Illustrazione editoriale di un’auto compatta e uno scooter parcheggiati in una strada italiana, non fotografia dell’annuncio.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
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
        "slug": SLUG, "title": ARTICLE["titolo"], "excerpt": ARTICLE["sommario"],
        "category": "Italia", "published_at": PUBLISHED, "updated_at": PUBLISHED,
        "status": "IN SVILUPPO", "body": ARTICLE["paragrafi"], "sources": ARTICLE["fonti"],
        "image": image,
    })

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION, "date": "2026-09-16", "type": "content-release",
        "news_added": [SLUG], "news_updated": [],
        "change": "Nuovo articolo sull’annuncio governativo relativo all’esenzione dal bollo auto",
        "image_policy_applied": "new-openai-editorial-image",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if path.exists():
            state = json.loads(path.read_text(encoding="utf-8"))
            state.update({"currentVersion": VERSION, "site_version": VERSION, "version": str(VERSION), "date": "2026-09-16", "release_date": "2026-09-16", "last_update": "bollo-auto-annuncio-v382"})
            write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260916T164839-Europe-Rome.json", {
        "run_at": PUBLISHED, "production_branch": "main",
        "production_base_commit": "7bf94d69ce8f0e7ab4a3aa5a5a6faa089f74be07",
        "coverage": {"target_distinct_full_contents": 500, "distinct_full_contents_actually_read": 3, "target_reached": False, "note": "Conteggio prudenziale: Reuters, ANSA e guida ACI letti; esclusi titoli, snippet, risultati di ricerca e duplicati. Obiettivo non raggiunto; nessuna consultazione inventata."},
        "processed": [{"slug": SLUG, "action": "new_article", "score": 9.1, "status": "IN SVILUPPO", "public_url": PUBLIC_URL, "sources": [s["url"] for s in ARTICLE["fonti"]], "publication_state": "pending_deploy"}],
    })

    from lxml import html
    doc = html.fromstring(article_path.read_text(encoding="utf-8"))
    assert doc.xpath('//main//h1[1]')[0].text_content() == ARTICLE["titolo"]
    assert len(doc.xpath('//article[contains(@class,"art-body")]/p')) == len(ARTICLE["paragrafi"])
    assert len(doc.xpath('//section[contains(@class,"curio-related")]//a')) == 3
    assert any(i["url"] == f"/notizie/{SLUG}.html" for i in items)
    print(json.dumps({"status": "ok", "version": VERSION, "slug": slug}, ensure_ascii=False))


if __name__ == "__main__":
    main()
