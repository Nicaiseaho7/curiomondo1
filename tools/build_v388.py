#!/usr/bin/env python3
"""Pubblica il verdetto dell'appello ter per l'omicidio di Carol Maltesi."""
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

VERSION = 388
SLUG = "carol-maltesi-ergastolo-davide-fontana-appello-ter-16-settembre-2026"
PUBLISHED = "2026-09-16T19:50:59+02:00"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
IMAGE_KEY = f"{SLUG}-ai-openai-v{VERSION}"
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-7eef4708-4565-47ac-b9e2-bb44f0a965fa.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Carol Maltesi, ergastolo a Davide Fontana nell'appello ter",
    "sommario": "La Corte d'assise d'appello di Milano ha riconosciuto di nuovo la premeditazione. Le motivazioni arriveranno entro 60 giorni e la difesa ha annunciato ricorso.",
    "categoria": "Cronaca",
    "luogo": "Milano",
    "formato": "standard",
    "parole_chiave_titolo": ["Carol Maltesi", "ergastolo nell'appello ter"],
    "dati_chiave": [
        {"icona": "◆", "valore": "Ergastolo", "etichetta": "pena pronunciata in appello"},
        {"icona": "●", "valore": "60 giorni", "etichetta": "termine per le motivazioni"},
        {"icona": "→", "valore": "Ricorso", "etichetta": "annunciato dalla difesa"},
    ],
    "paragrafi": [
        "La Corte d'assise d'appello di Milano ha condannato mercoledì 16 settembre 2026 Davide Fontana all'ergastolo per l'omicidio di Carol Maltesi. Nel processo d'appello ter i giudici hanno riconosciuto nuovamente l'aggravante della premeditazione. Le motivazioni saranno depositate entro 60 giorni e la difesa ha già annunciato un ricorso in Cassazione.",
        "Il verdetto riguarda il punto rimasto aperto dopo due annullamenti con rinvio della Corte di Cassazione. La responsabilità di Fontana per l'omicidio, commesso a Rescaldina l'11 gennaio 2022, non era oggetto di una nuova valutazione completa: il collegio doveva pronunciarsi soprattutto sulla premeditazione e sul conseguente trattamento sanzionatorio.",
        "La Corte ha confermato l'ergastolo senza isolamento diurno e ha mantenuto la valutazione delle attenuanti generiche come subvalenti rispetto alle aggravanti. La decisione accoglie la richiesta della Procura generale, che aveva sostenuto l'esistenza di una preparazione del delitto e delle condotte successive.",
        "La difesa aveva chiesto di escludere la premeditazione e di considerare anche il percorso di giustizia riparativa intrapreso dall'imputato. Fontana ha reso dichiarazioni spontanee in aula, esprimendo scuse e dolore per quanto commesso. Queste dichiarazioni documentano la sua posizione processuale, ma non modificano da sole l'accertamento giudiziario.",
        "Il caso è arrivato al sesto giudizio tra primo grado, appelli e passaggi in Cassazione. In primo grado Fontana era stato condannato a 30 anni; le successive corti d'appello avevano applicato l'ergastolo riconoscendo la premeditazione, ma la Suprema Corte aveva rilevato carenze nella motivazione di quell'aggravante e disposto nuovi esami.",
        "Il pronunciamento di oggi non è definitivo. Il ricorso annunciato dalla difesa aprirà un nuovo controllo di legittimità, nel quale la Cassazione potrà valutare la correttezza giuridica e la motivazione della sentenza, senza trasformarsi in un ulteriore giudizio generale sui fatti.",
        "La sorella della vittima, costituita parte civile con altri familiari, ha accolto la condanna ricordando la lunga durata del percorso processuale. Ha inoltre escluso la disponibilità a un incontro nell'ambito della giustizia riparativa. La scelta delle persone offese resta distinta dal procedimento penale e non determina la pena.",
        "Fino all'eventuale decisione della Cassazione, lo stato corretto della vicenda è quindi quello di una condanna all'ergastolo pronunciata in appello e ancora impugnabile. La pubblicazione delle motivazioni sarà il prossimo passaggio essenziale per comprendere come il collegio abbia argomentato la premeditazione dopo i precedenti rinvii.",
    ],
    "fonti": [
        {
            "url": "https://www.ilfattoquotidiano.it/2026/09/16/femminicidio-carol-maltesi-fontana-ergastolo-notizie/8508027/",
            "descrizione": "Il Fatto Quotidiano — cronaca d'aula, dispositivo, percorso processuale e ricorso annunciato dalla difesa.",
        },
        {
            "url": "https://milano.repubblica.it/cronaca/2026/09/16/news/femminicidio_carol_maltesi_processo_appello_ter_chiesto_ergastolo_premeditazione_fontana-425588374/",
            "descrizione": "la Repubblica Milano — conferma indipendente dell'ergastolo e del riconoscimento della premeditazione.",
        },
        {
            "url": "https://milano.corriere.it/notizie/cronaca/26_settembre_16/omicidio-carol-maltesi-ergastolo-per-davide-fontana-nell-appello-ter-a-milano-confermata-la-premeditazione-d991ced9-c63a-4358-a17a-afd7f9660xlk_amp.shtml",
            "descrizione": "Corriere della Sera Milano — pena, termine per le motivazioni e dichiarazioni delle parti dopo il verdetto.",
        },
        {
            "url": "https://www.corrierealpi.it/italia/omicidio-carol-maltesi-ergastolo-per-davide-fontana-nellappello-ter-tlsuq7fg",
            "descrizione": "ANSA, ripresa dal Corriere delle Alpi — esito del processo d'appello ter e ruolo dell'aggravante della premeditazione.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/violenza-prima-dei-16-anni-l-istat-stima-3-milioni-di-donne-italiane-coinvolte-16-09-2026.html",
            "titolo": "Violenza prima dei 16 anni: l'Istat stima 3 milioni di donne italiane coinvolte",
        },
        {
            "url": "/notizie/decreto-giustizia-governo-fiducia-camera.html",
            "titolo": "Decreto Giustizia, il governo pone la questione di fiducia alla Camera",
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
    out = ROOT / "assets" / "images" / "editorial-cronaca"
    out.mkdir(parents=True, exist_ok=True)
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{IMAGE_KEY}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=84, method=6
        )
        variants.append({
            "w": width,
            "src": f"/assets/images/editorial-cronaca/{path.name}",
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
        "alt": "Scena editoriale contestuale generata con IA in un tribunale italiano vuoto, con fascicolo neutro e bilancia; non documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "reenactedEvent": False,
        "prompt": "Respectful contextual editorial image of an empty Italian courthouse corridor with a neutral case file and brass balance; no people, no reenactment, no readable text or watermark.",
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
        "status": "CONFERMATA DA PIÙ FONTI",
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
        "change": "Nuovo articolo sul verdetto dell'appello ter per l'omicidio di Carol Maltesi",
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
            "articleCount": 265,
            "generatedEditorialImages": 148,
            "last_update": "carol-maltesi-appello-ter-v388",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260916T195059-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "production_branch": "main",
        "production_commit_checked": "042954577625ee8d0b0e2473a6ea16035a26ab29",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 8,
            "target_reached": False,
            "note": "Conteggio prudenziale dei contenuti aperti integralmente nel controllo corrente: quattro cronache indipendenti sul verdetto e quattro fonti complete su candidate poi escluse. Titoli, snippet e riprese d'agenzia non sono conteggiati.",
        },
        "processed": [{
            "slug": SLUG,
            "action": "new_article",
            "score": 8.3,
            "status": "CONFERMATA DA PIÙ FONTI",
            "public_url": PUBLIC_URL,
            "sources": [source["url"] for source in ARTICLE["fonti"]],
            "publication_state": "pending_deploy",
        }],
        "excluded": [
            {"topic": "Revolut, verifiche del Garante e nuove indagini", "reason": "Sviluppo rilevante ma privo, al momento del controllo, di una fonte primaria pubblica e di conferma indipendente sufficiente sui nuovi atti investigativi."},
            {"topic": "Inflazione definitiva di agosto al 3,3%", "reason": "Dato già coperto da un articolo sullo stesso evento; la conferma definitiva non modifica il valore principale."},
            {"topic": "Meloni intende arrivare a fine legislatura", "reason": "Dichiarazione politica senza conseguenza istituzionale immediata; punteggio inferiore a 8."},
        ],
    })

    from lxml import html
    doc = html.fromstring(article_path.read_text(encoding="utf-8"))
    assert doc.xpath('//main//h1[1]')[0].text_content() == ARTICLE["titolo"]
    assert len(doc.xpath('//article[contains(@class,"art-body")]/p')) == len(ARTICLE["paragrafi"])
    assert len(doc.xpath('//section[contains(@class,"curio-related")]//a')) == 2
    assert doc.xpath('//figure[@data-ai-generated="true"][@data-sensitive-context="true"]')
    assert any(item["url"] == f"/notizie/{SLUG}.html" for item in items)
    print(json.dumps({"status": "ok", "version": VERSION, "slug": slug}, ensure_ascii=False))


if __name__ == "__main__":
    main()
