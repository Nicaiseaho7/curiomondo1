#!/usr/bin/env python3
"""Pubblica la notizia sullo sfratto di Maricarmen a Madrid."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 530
SLUG = "maricarmen-87-anni-sfrattata-madrid-proteste-23-settembre-2026"
SOURCE_IMAGE = ROOT.parent / "generated_images/exec-775faeaf-d0df-4eee-b413-060d1c3eb770.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Madrid, sfrattata a 87 anni tra le proteste di centinaia di persone",
    "sommario": "Maricarmen Abascal ha lasciato la casa nel quartiere Retiro dove viveva dal 1956. Lo sgombero è stato eseguito al quarto tentativo mentre un ampio dispositivo di polizia allontanava i manifestanti.",
    "categoria": "Mondo",
    "luogo": "Madrid",
    "formato": "standard",
    "parole_chiave_titolo": ["87 anni", "proteste"],
    "dati_chiave": [
        {"valore": "87 anni", "etichetta": "l’età di Maricarmen"},
        {"valore": "71 anni", "etichetta": "trascorsi nella stessa casa"},
        {"valore": "4° tentativo", "etichetta": "quello eseguito oggi"},
    ],
    "paragrafi": [
        "Maricarmen Abascal, 87 anni, è stata sfrattata mercoledì 23 settembre dalla casa nel quartiere Retiro di Madrid in cui viveva dal 1956. La commissione giudiziaria ha eseguito il provvedimento al quarto tentativo, mentre centinaia di persone riunite davanti all’edificio cercavano di opporsi allo sgombero.",
        "La polizia ha predisposto un ampio cordone nella calle del Alcalde Sainz de Baranda e ha progressivamente allontanato manifestanti e operatori dell’informazione dall’ingresso. Le cronache sul posto riferiscono di momenti di tensione e spinte. Gli attivisti del Sindicato de Inquilinas hanno contestato la gestione del dispositivo; la Delegazione del Governo ha precisato che l’intervento rispondeva a un mandato giudiziario.",
        "Al termine delle operazioni Maricarmen ha lasciato l’abitazione assistita dai sanitari. El País riferisce che si trasferirà presso alcuni familiari. Le ricostruzioni pubblicate prima dello sgombero indicavano invece che una sistemazione stabile e adeguata non era stata ancora definita.",
        "Il contratto di affitto era stato firmato dai genitori nel 1956. Dopo la morte del padre era passato alla madre e, nel 2005, a Maricarmen. La controversia nasce dalla seconda successione: la proprietà ne ha chiesto la cessazione, mentre la difesa dell’inquilina ha sostenuto che la normativa dell’epoca non permetteva alla madre di figurare come cointestataria.",
        "L’edificio è passato nel 2018 a Urbagestión Desarrollo e Inversión. Secondo il Sindicato de Inquilinas, la società aveva proposto un canone di 2.650 euro, contro i circa 500 versati fino ad allora da Maricarmen. La donna percepisce una pensione indicata dalle fonti in circa 1.350 euro al mese e ha una disabilità riconosciuta del 50 per cento.",
        "Alla vigilia dello sgombero una donatrice anonima si era offerta di coprire la differenza fra il vecchio canone e quello richiesto, oltre agli arretrati. La proposta non ha fermato il procedimento. Il Ministero dell’Edilizia aveva chiesto alle amministrazioni locali di intervenire e appoggiato la richiesta dell’ONU di sospendere il rilascio fino alla disponibilità di una soluzione abitativa adeguata.",
        "Il Comune e la Comunità di Madrid hanno sostenuto di aver proposto forme di assistenza, fra cui soluzioni residenziali e l’intervento dei servizi sociali. I rappresentanti dell’inquilina hanno giudicato quelle opzioni insufficienti o incompatibili con le sue condizioni economiche e personali. Le diverse versioni restano parte del confronto politico seguito al caso.",
        "La mobilitazione, iniziata con un presidio notturno e proseguita durante lo sgombero, ha trasformato la vicenda individuale in un simbolo della crisi abitativa di Madrid. Il fatto nuovo del 23 settembre è però concreto: dopo tre rinvii, Maricarmen non vive più nell’appartamento che era stato la sua casa per 71 anni.",
    ],
    "fonti": [
        {"url": "https://efe.com/espana/2026-09-23/desahucio-casa-maricarmen-madrid/", "descrizione": "EFE — esecuzione dello sfratto, dispositivo di polizia e reazioni istituzionali, 23 settembre 2026."},
        {"url": "https://www.europapress.es/madrid/noticia-desahucian-maricarmen-vivienda-retiro-residia-hace-70-anos-arropada-cientos-personas-20260923130936.html", "descrizione": "Europa Press — cronaca sul posto, storia del contratto e quarto tentativo di sgombero."},
        {"url": "https://www.rtve.es/noticias/20260923/lagrimas-maricarmen-desahucio-imposible/17237227.shtml", "descrizione": "RTVE — testimonianze dalla mobilitazione e consistenza del presidio."},
        {"url": "https://elpais.com/espana/madrid/2026-09-23/maricarmen-se-queda-un-centenar-de-activistas-espera-junto-a-la-anciana-a-la-comision-judicial.html", "descrizione": "El País — sviluppo finale del caso e trasferimento presso familiari."},
    ],
}


def make_image() -> dict:
    image = Image.open(SOURCE_IMAGE).convert("RGB")
    target = 1.5
    width, height = image.size
    if width / height > target:
        new_width = round(height * target)
        left = (width - new_width) // 2
        image = image.crop((left, 0, left + new_width, height))
    else:
        new_height = round(width / target)
        top = (height - new_height) // 2
        image = image.crop((0, top, width, top + new_height))
    variants = []
    directory = ROOT / "assets/images/editorial-auto"
    for out_width in (480, 800, 1200):
        path = directory / f"{SLUG}-v{VERSION}-{out_width}.webp"
        resized = image.resize((out_width, round(out_width / target)), Image.Resampling.LANCZOS)
        resized.save(path, "WEBP", quality=87, method=6)
        variants.append({"w": out_width, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return {
        "key": f"{SLUG}-v{VERSION}",
        "alt": "Illustrazione editoriale IA con una sedia e una valigia davanti a un edificio di Madrid, mentre una folla pacifica resta dietro un cordone di polizia; scena simbolica non documentaria.",
        "variants": variants,
        "disclosure": site.CAPTION,
        "generator": "OpenAI image tool",
        "sensitiveContext": True,
    }


def main() -> None:
    image = make_image()
    site.write_article(ARTICLE, image, VERSION)
    site.register_image(image, SLUG, VERSION)

    cfg_path = ROOT / "assets/data/homepage-config-v504.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    cfg["version"] = VERSION
    cfg["articles"][f"/notizie/{SLUG}.html"] = {
        "firstPublishedAt": ARTICLE["published"],
        "homepagePriority": 94,
        "primaryCategory": "mondo",
    }
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces([ARTICLE], f"/notizie/{SLUG}.html", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = VERSION
    manifest["site"]["site_version"] = VERSION
    manifest["site_version"] = VERSION
    manifest["version"] = manifest["release_version"] = f"v{VERSION}"
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-23",
        "type": "world-housing-news",
        "news_added": [SLUG],
        "news_updated": [],
        "change": "Sfratto di Maricarmen Abascal a Madrid",
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(site_version=VERSION, version=str(VERSION), currentVersion=VERSION,
                     release_date="2026-09-23", last_update="maricarmen-madrid-v530")
        if "articleCount" in state:
            state["articleCount"] += 1
        if "generatedEditorialImages" in state:
            state["generatedEditorialImages"] += 1
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"published": f"/notizie/{SLUG}.html", "version": VERSION}, ensure_ascii=False))


if __name__ == "__main__":
    main()
