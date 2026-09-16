#!/usr/bin/env python3
"""Pubblica la delibera CSM sui test psicoattitudinali per i magistrati."""
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

VERSION = 386
SLUG = "csm-test-psicoattitudinali-magistrati-criteri-16-settembre-2026"
PUBLISHED = "2026-09-16T18:56:43+02:00"
PUBLIC_URL = f"https://curiomondo.it/notizie/{SLUG}.html"
FEATURED_URL = "/notizie/pride-and-prejudice-netflix-3-dicembre-2026.html"
IMAGE_KEY = f"{SLUG}-ai-openai-v{VERSION}"
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-79fddf16-22ed-471a-bd2f-c9da44521b7c.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Test psicoattitudinali per i magistrati: il CSM approva i criteri",
    "sommario": "La delibera individua cinque aree da valutare nei futuri magistrati. I quesiti saranno elaborati, collaudati e sottoposti a un nuovo via libera del Consiglio.",
    "categoria": "Politica",
    "luogo": "Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["CSM", "approva i criteri"],
    "dati_chiave": [
        {"icona": "◆", "valore": "5 aree", "etichetta": "ambiti di idoneità individuati"},
        {"icona": "●", "valore": "6", "etichetta": "astensioni nel voto del plenum"},
        {"icona": "→", "valore": "4 docenti", "etichetta": "esperti incaricati di preparare i quesiti"},
    ],
    "paragrafi": [
        "Il plenum del Consiglio superiore della magistratura ha approvato mercoledì 16 settembre 2026, a Roma, la delibera che fissa i criteri per i test psicoattitudinali degli aspiranti magistrati. Il voto ha registrato sei astensioni. La decisione attua la disciplina introdotta nel 2024, ma non rende ancora disponibili i questionari.",
        "Il documento individua cinque aree di valutazione: cognitiva, emotiva, relazionale, etico-valoriale e organizzativa. Una grave carenza in uno di questi ambiti potrà essere considerata rilevante per l'idoneità, dopo l'esame del risultato nel colloquio previsto dalla selezione.",
        "Nell'area cognitiva rientrano ragionamento analitico, pensiero critico, capacità decisionale e soluzione dei problemi. Le altre aree comprendono equilibrio emotivo, gestione dello stress, ascolto, collaborazione, equità, autonomia di giudizio, organizzazione e gestione del tempo.",
        "Il risultato del test non costituisce una diagnosi clinica né una bocciatura automatica. Serve a orientare il colloquio psicoattitudinale, che si colloca dopo il superamento delle prove scritte e all'interno della fase orale del concorso.",
        "Una commissione composta da quattro docenti esperti di psicologia e psicometria dovrà ora predisporre le batterie di quesiti. Prima dell'uso saranno necessari un collaudo con partecipanti volontari e una nuova approvazione del CSM, passaggi che separano i criteri votati oggi dall'applicazione concreta.",
        "La nuova disciplina dovrebbe essere richiamata nel prossimo bando atteso in autunno, ma i test non saranno immediatamente operativi. I resoconti sul programma di attuazione indicano una fase sperimentale nel 2027 e l'avvio effettivo tra la fine del 2027 e il 2028; il calendario resta subordinato allo sviluppo e alla validazione degli strumenti.",
        "I criteri riguardano i candidati dei concorsi banditi dal 2026 e non introducono una valutazione retroattiva dei magistrati già in servizio. La distinzione è importante perché il voto odierno definisce requisiti e procedura per l'accesso futuro, senza modificare lo status professionale delle toghe in attività.",
        "Il confronto nel plenum ha mantenuto le divergenze politiche e istituzionali che accompagnano la misura. I consiglieri favorevoli hanno richiamato l'obbligo di applicare la legge; le posizioni critiche hanno segnalato il rischio che il meccanismo venga percepito come una delegittimazione della magistratura.",
    ],
    "fonti": [
        {
            "url": "https://www.radioradicale.it/scheda/798664/plenum-dl-csm",
            "descrizione": "Radio Radicale — registrazione integrale del plenum del CSM del 16 settembre 2026, svolto dalle 10:25 alle 14:27.",
        },
        {
            "url": "https://www.ansa.it/sito/notizie/cronaca/2026/09/16/il-csm-approva-la-delibera-sui-test-psicoattitudinali-per-i-magistrati_f3f027b2-fd28-493a-afae-65e78bfa2c75.html",
            "descrizione": "ANSA — esito del voto, sei astensioni, commissione incaricata e necessità di una successiva approvazione dei test.",
        },
        {
            "url": "https://www.ilfattoquotidiano.it/2026/09/16/test-psicoattitudinali-magistrati-csm-criteri-notizie/8507980/",
            "descrizione": "Il Fatto Quotidiano — criteri nelle cinque aree, procedura concorsuale e tempi previsti per collaudo e applicazione.",
        },
        {
            "url": "https://www.repubblica.it/politica/2026/09/16/news/csm_test_psicoattitudinali_magistrati-425588342/",
            "descrizione": "la Repubblica — conferma indipendente del via libera e distinzione tra inserimento nel bando e operatività effettiva.",
        },
    ],
    "correlati": [
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
    out = ROOT / "assets" / "images" / "editorial-politica"
    out.mkdir(parents=True, exist_ok=True)
    variants = []
    for width in (480, 800, 1200):
        path = out / f"{IMAGE_KEY}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=84, method=6
        )
        variants.append({
            "w": width,
            "src": f"/assets/images/editorial-politica/{path.name}",
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
        "alt": "Scena editoriale contestuale generata con IA in una sala istituzionale italiana, con toga da magistrato e schede astratte di valutazione; non documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ordinary contextual editorial scene about the CSM criteria for magistrates' aptitude tests; empty Italian institutional room, judicial robe and abstract assessment cards; no real vote reenacted, no text or watermark.",
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
        "change": "Nuovo articolo sui criteri CSM per i test psicoattitudinali dei magistrati",
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
            "articleCount": int(state.get("articleCount", 262)) + 1,
            "generatedEditorialImages": int(state.get("generatedEditorialImages", 145)) + 1,
            "last_update": "csm-test-psicoattitudinali-v386",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "italia-20260916T185643-Europe-Rome.json", {
        "run_at": PUBLISHED,
        "production_branch": "main",
        "coverage": {
            "target_distinct_full_contents": 500,
            "distinct_full_contents_actually_read": 4,
            "target_reached": False,
            "note": "Conteggio prudenziale: registrazione integrale del plenum, ANSA, Il Fatto Quotidiano e la Repubblica. Esclusi titoli, snippet e riprese della stessa agenzia; nessuna consultazione inventata.",
        },
        "processed": [{
            "slug": SLUG,
            "action": "new_article",
            "score": 8.4,
            "status": "CONFERMATA DA PIÙ FONTI",
            "public_url": PUBLIC_URL,
            "sources": [source["url"] for source in ARTICLE["fonti"]],
            "publication_state": "pending_deploy",
        }],
    })

    from lxml import html
    doc = html.fromstring(article_path.read_text(encoding="utf-8"))
    assert doc.xpath('//main//h1[1]')[0].text_content() == ARTICLE["titolo"]
    assert len(doc.xpath('//article[contains(@class,"art-body")]/p')) == len(ARTICLE["paragrafi"])
    assert len(doc.xpath('//section[contains(@class,"curio-related")]//a')) == 1
    assert doc.xpath('//figure[@data-ai-generated="true"][@data-sensitive-context="false"]') == []
    assert any(item["url"] == f"/notizie/{SLUG}.html" for item in items)
    print(json.dumps({"status": "ok", "version": VERSION, "slug": slug}, ensure_ascii=False))


if __name__ == "__main__":
    main()
