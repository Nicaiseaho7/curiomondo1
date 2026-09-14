#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

from PIL import Image

from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

ROOT = Path(__file__).resolve().parents[1]
VERSION = 351
SLUG = "borse-asiatiche-sell-off-titoli-intelligenza-artificiale-14-settembre-2026"
PUBLISHED = "2026-09-14T06:51:05+02:00"
IMAGE_KEY = f"{SLUG}-ai-openai-v{VERSION}"
SOURCE_IMAGE = ROOT / "generated_images" / "exec-5bd27c04-5b53-44da-a323-d680079b85a3.png"

ARTICLE = {
    "slug": SLUG,
    "titolo": "Borse asiatiche, forte sell-off sui titoli legati all’intelligenza artificiale",
    "sommario": "SoftBank perde fino al 13,2% e scendono anche Kioxia, SK Hynix e Samsung. Gli investitori reagiscono agli appelli dei vertici di Anthropic, OpenAI e xAI per rallentare lo sviluppo dei modelli più avanzati.",
    "categoria": "Economia",
    "luogo": "Asia",
    "formato": "standard",
    "parole_chiave_titolo": ["forte sell-off", "intelligenza artificiale"],
    "dati_chiave": [
        {"icona": "▼", "valore": "−13,2%", "etichetta": "calo massimo di SoftBank"},
        {"icona": "◆", "valore": "−9,8%", "etichetta": "ribasso iniziale di Kioxia"},
        {"icona": "●", "valore": "−5,3%", "etichetta": "flessione di SK Hynix"},
    ],
    "paragrafi": [
        "Le azioni asiatiche più esposte all’intelligenza artificiale sono scese con forza nelle prime contrattazioni di lunedì 14 settembre. Le vendite sono arrivate dopo che i vertici di Anthropic, OpenAI e xAI hanno sostenuto la necessità di rallentare lo sviluppo dei modelli più avanzati per affrontarne i rischi.",
        "A Tokyo, SoftBank ha perso fino al 13,2%, mentre Kioxia ha ceduto inizialmente il 9,8%. Tokyo Electron è arretrata del 3,7%. A Seul, SK Hynix ha segnato un calo del 5,3% e Samsung Electronics del 3,7%; a Taiwan, TSMC è scesa dell’1,2%.",
        "Il movimento non ha colpito tutte le società nella stessa misura. SoftBank è particolarmente sensibile alle aspettative sull’AI per la sua esposizione a OpenAI, mentre Kioxia, SK Hynix e Samsung forniscono memorie utilizzate nell’infrastruttura tecnologica. Per questo una revisione dei tempi di sviluppo può modificare le attese sulla domanda futura.",
        "Il Financial Times ha rilevato che le imprese asiatiche legate all’infrastruttura dell’AI erano state tra le principali vincitrici dei mercati globali nel 2026. Il ribasso mostra quindi quanto le valutazioni dipendano dalla continuità degli investimenti e dalla velocità con cui nuovi sistemi arrivano sul mercato.",
        "Dario Amodei, amministratore delegato di Anthropic, ha chiesto alle aziende di ridurre il ritmo con cui aumentano le capacità dei modelli. Sam Altman di OpenAI ed Elon Musk, alla guida di xAI, hanno espresso accordo. Le dichiarazioni riguardano i rischi della tecnologia, ma non costituiscono ancora un piano coordinato o una sospensione generale dei progetti.",
        "La reazione è stata amplificata da un quadro già prudente sui mercati asiatici. Reuters ha segnalato anche il rialzo del petrolio e l’attesa per possibili aumenti dei tassi negli Stati Uniti e in Giappone. Questi fattori rendono più costoso finanziare investimenti di lungo periodo e possono pesare sui titoli con valutazioni elevate.",
        "I ribassi citati rappresentano i minimi registrati durante la seduta iniziale, non necessariamente i prezzi di chiusura. La loro ampiezza può cambiare nel corso della giornata. Un solo giorno di contrattazioni, inoltre, non dimostra che la crescita dell’industria sia terminata: segnala un rapido adeguamento delle aspettative a nuove informazioni.",
        "Per gli investitori il nodo riguarda ora l’effetto concreto degli appelli: tempi di lancio più lunghi, maggiori controlli o investimenti spostati dalla capacità di calcolo alla sicurezza. Finché le aziende non tradurranno le dichiarazioni in decisioni operative, il mercato continuerà a valutare soprattutto il rischio di un rallentamento della domanda di chip e infrastrutture.",
    ],
    "fonti": [
        {"url": "https://www.reuters.com/world/china/ai-linked-asian-stocks-slump-after-top-lab-ceos-call-slowing-down-technologys-2026-09-14/", "descrizione": "Reuters — ribassi intraday dei titoli asiatici e dichiarazioni dei vertici delle aziende di intelligenza artificiale."},
        {"url": "https://www.ft.com/content/aa8a1be7-abe0-44b7-bcd3-31fd0a44de08", "descrizione": "Financial Times — conferma del calo globale dei titoli AI e del ruolo delle società asiatiche nella crescita del settore."},
        {"url": "https://www.reuters.com/world/china/global-markets-global-markets-2026-09-13/", "descrizione": "Reuters — quadro generale dei mercati asiatici, petrolio e attese sui tassi di interesse."},
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
        "alt": "Scena editoriale ordinaria in una sala mercati asiatica con grafici in forte calo e componenti per semiconduttori.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
    }
    slug = write_article(ARTICLE, image, VERSION)
    article_path = ROOT / "notizie" / f"{slug}.html"
    page = article_path.read_text(encoding="utf-8")
    # datePublished indica la prima pubblicazione CurioMondo; l'ora dello sviluppo resta nel testo.
    import re
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
