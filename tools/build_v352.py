#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from PIL import Image

from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

ROOT = Path(__file__).resolve().parents[1]
VERSION = 352
SLUG = "yemen-houthi-isole-hanish-mar-rosso-14-settembre-2026"
PUBLISHED = "2026-09-14T13:18:00+02:00"
IMAGE_KEY = f"{SLUG}-ai-openai-v{VERSION}"
SOURCE_IMAGE = ROOT.parent / "generated_images" / "exec-15153297-fbc8-48a3-9136-d76ae5fe791f.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Yemen, gli Houthi conquistano le isole Hanish nel Mar Rosso",
    "sommario": "Grande Hanish e Piccola Hanish passano sotto il controllo dei ribelli, rafforzandone la presenza lungo una rotta decisiva tra Mar Rosso e Golfo di Aden.",
    "categoria": "Mondo",
    "luogo": "Yemen",
    "formato": "standard",
    "parole_chiave_titolo": ["isole Hanish", "Mar Rosso"],
    "dati_chiave": [
        {"icona": "◆", "valore": "2", "etichetta": "isole conquistate"},
        {"icona": "↔", "valore": "30 km", "etichetta": "estensione dell’arcipelago"},
        {"icona": "●", "valore": "80.000+", "etichetta": "sfollati nell’escalation"},
    ],
    "paragrafi": [
        "Gli Houthi hanno conquistato lunedì 14 settembre le isole di Grande Hanish e Piccola Hanish, nel Mar Rosso meridionale. Funzionari del governo yemenita e del movimento hanno confermato ad Associated Press il passaggio di controllo, avvenuto durante la nuova avanzata attorno allo stretto di Bab el-Mandeb.",
        "L’arcipelago si estende per circa 30 chilometri tra la costa yemenita e quella eritrea. La sua posizione permette di osservare una parte del corridoio marittimo che collega il Mar Rosso al Golfo di Aden, utilizzato da navi commerciali e petroliere dirette tra Asia, Medio Oriente ed Europa.",
        "La conquista segue la presa di Mokha e dell’isola di Mayun, situata all’imboccatura dello stretto. Reuters aveva documentato nei giorni precedenti la rapida avanzata degli Houthi lungo la costa occidentale e l’aumento degli attacchi contro infrastrutture e obiettivi sauditi.",
        "Il valore strategico delle Hanish deriva soprattutto dalla geografia. Lo stretto di Hormuz resta sottoposto a forti restrizioni, mentre Bab el-Mandeb è diventato ancora più importante per le esportazioni saudite verso i mercati asiatici. Un controllo territoriale più ampio aumenta la capacità di sorvegliare o minacciare le rotte, ma non equivale automaticamente alla chiusura del passaggio.",
        "Le conseguenze possono riguardare assicurazioni, noli e tempi di viaggio. Le compagnie devono valutare il rischio di attraversare l’area oppure deviare attorno al Capo di Buona Speranza, con più giorni di navigazione e maggior consumo di carburante. Le Monde ha segnalato che alcune navi hanno già ridotto la propria visibilità elettronica durante il transito.",
        "La nuova offensiva ha anche un costo umanitario. Associated Press riferisce che oltre 80.000 persone sono state costrette a lasciare le proprie case nelle ultime settimane. Il dato descrive gli spostamenti prodotti dall’intera escalation yemenita e non può essere attribuito soltanto alla conquista delle due isole.",
        "Le Hanish erano state presidiate in passato da forze sostenute dagli Emirati Arabi Uniti, ritiratesi nel corso del 2026. La loro acquisizione amplia quindi la profondità marittima degli Houthi, mentre le forze governative riconosciute internazionalmente cercano di riorganizzarsi nel sud e nell’est del Paese.",
        "Resta incerto quanto stabilmente il movimento riuscirà a mantenere le nuove posizioni e quali capacità militari vi installerà. Le fonti disponibili confermano il controllo territoriale, ma non documentano ancora un blocco totale del traffico commerciale presso le Hanish. La distinzione è essenziale per valutare l’impatto reale sui flussi mondiali.",
    ],
    "fonti": [
        {"url": "https://apnews.com/article/8c18d82c109a8ea91347ce53c0096c53", "descrizione": "Associated Press — conferma della conquista di Grande Hanish e Piccola Hanish tramite fonti governative e Houthi, quadro umanitario e geografico."},
        {"url": "https://www.reuters.com/business/energy/diplomacy-stumbles-with-postponement-meeting-strait-hormuz-proposal-2026-09-13/", "descrizione": "Reuters — avanzata degli Houthi attorno a Bab el-Mandeb, attacchi regionali e conseguenze per le rotte petrolifere."},
        {"url": "https://www.lemonde.fr/en/economy/article/2026/09/14/houthi-control-of-bab-al-mandab-strait-poses-new-threat-to-global-economy_6757506_19.html", "descrizione": "Le Monde — rischi per il traffico commerciale, costi delle deviazioni e comportamento delle compagnie di navigazione."},
    ],
}


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
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=88, method=6)
        variants.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return variants


def main() -> None:
    image = {
        "key": IMAGE_KEY,
        "aiGenerated": True,
        "documentaryPhoto": False,
        "variants": save_image_variants(),
        "alt": "Scena editoriale ordinaria ultrarealistica delle isole Hanish nel Mar Rosso con una nave commerciale in lontananza.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
    }
    slug = write_article(ARTICLE, image, VERSION)
    article_path = ROOT / "notizie" / f"{slug}.html"
    page = article_path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{PUBLISHED}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{PUBLISHED}"', page)
    article_path.write_text(page, encoding="utf-8")
    ARTICLE["published"] = PUBLISHED
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], f"/notizie/{slug}.html", VERSION)
    for state_name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        state_path = ROOT / state_name
        if state_path.exists():
            state = json.loads(state_path.read_text(encoding="utf-8"))
            if "version" in state:
                state["version"] = VERSION
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "ok", "version": VERSION, "slug": slug}, ensure_ascii=False))


if __name__ == "__main__":
    main()
