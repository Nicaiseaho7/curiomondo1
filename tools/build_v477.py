#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
import sys
sys.path[:0] = [str(ROOT), str(ROOT / "tools")]

from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 477
DATE = "2026-09-21"
SOURCE = Path("/workspace/scratch/f0880b1dfc7b/generated_images/exec-e0398e91-9135-4cd9-b231-2d005ed512dd.png")
SLUG = "papa-leone-xiv-intelligenza-artificiale-pace-ai4peace-21-settembre-2026"


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def variants() -> list[dict[str, object]]:
    image = Image.open(SOURCE).convert("RGB")
    ratio = 1.5
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    folder = ROOT / "assets/images/editorial-auto"
    key = f"{SLUG}-v{VERSION}"
    output = []
    for width in (480, 800, 1200):
        target = folder / f"{key}-{width}.webp"
        resized = image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS)
        resized.save(target, "WEBP", quality=86, method=6)
        output.append({"w": width, "src": f"/assets/images/editorial-auto/{target.name}",
                       "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
                       "bytes": target.stat().st_size})
    return output


ARTICLE = {
    "slug": SLUG,
    "titolo": "Leone XIV all’AI4Peace: l’intelligenza artificiale deve unire, non dividere",
    "sommario": "Nel messaggio al simposio di Roma, il Papa chiede che lo sviluppo tecnologico tuteli la dignità umana. Il testo non propone nuove norme, ma indica un criterio etico preciso.",
    "categoria": "Tecnologia",
    "luogo": "Roma",
    "formato": "standard",
    "stato": "CONFERMATO",
    "parole_chiave_titolo": ["Leone XIV", "intelligenza artificiale"],
    "dati_chiave": [
        {"icona": "◆", "valore": "20-22 set", "etichetta": "giorni del simposio AI4Peace a Roma"},
        {"icona": "●", "valore": "1ª edizione", "etichetta": "dell’incontro internazionale"},
        {"icona": "▲", "valore": "4 aree", "etichetta": "pace, conflitti, diritti e governance"},
    ],
    "paragrafi": [
        "Papa Leone XIV ha chiesto che l’intelligenza artificiale sia sviluppata per rafforzare la pace e i legami tra le persone, non le divisioni. Il messaggio è stato letto lunedì 21 settembre alla Pontificia Università Lateranense di Roma, durante il simposio internazionale AI4Peace.",
        "Il Pontefice ha collegato l’innovazione alla dignità di ogni persona e al bene comune. La sua indicazione riguarda quindi sia chi progetta i sistemi sia le istituzioni che ne regolano l’uso, soprattutto quando gli strumenti digitali possono amplificare conflitti, disinformazione o polarizzazione.",
        "Leone XIV non ha annunciato una legge, un organismo di controllo o nuovi obblighi tecnici. Il messaggio stabilisce invece un criterio pubblico: valutare una tecnologia anche per gli effetti che produce sulle relazioni umane, non soltanto per velocità, capacità o rendimento economico.",
        "Il simposio, in programma dal 20 al 22 settembre, riunisce ricercatori ed esperti su costruzione della pace, prevenzione e soluzione dei conflitti, diritti umani e governo dell’intelligenza artificiale. Tra gli interventi figurano rappresentanti accademici e istituzionali internazionali.",
        "Il nuovo richiamo si inserisce nella linea già adottata dal Papa sui rischi dell’IA. La continuità sta nel rapporto tra potere tecnologico e responsabilità: un sistema può essere efficace e insieme dannoso se riduce le persone a dati, favorisce discriminazioni o rende più facile manipolare l’informazione.",
        "Per cittadini e imprese, il messaggio non modifica nell’immediato regole o servizi. Il suo peso è culturale e diplomatico: porta nel confronto internazionale una domanda misurabile, cioè se un’applicazione protegga la persona e riduca i conflitti oppure aumenti esclusione e sfiducia.",
        "Il confronto riguarda anche la progettazione concreta. Trasparenza, controllo umano e verifica degli impatti permettono di distinguere una dichiarazione di principio da criteri applicabili nelle decisioni pubbliche e aziendali.",
        "Il programma di AI4Peace prosegue fino a martedì 22 settembre. Gli eventuali documenti conclusivi chiariranno se dal confronto emergeranno proposte operative, impegni condivisi o soltanto linee di ricerca per le prossime edizioni.",
    ],
    "fonti": [
        {"url": "https://www.vaticannews.va/en/pope/news/2026-09/pope-leo-message-ai-conference-lateran-ai4peace.html", "descrizione": "Vatican News — 21 settembre 2026 — messaggio di Leone XIV, sede e contenuti del richiamo su dignità umana e pace."},
        {"url": "https://www.ai4peace.ai/program", "descrizione": "AI4Peace — programma ufficiale del simposio del 20-22 settembre e aree di lavoro della conferenza."},
        {"url": "https://www.reuters.com/technology/pope-leo-calls-ai-systems-that-dont-foster-divisions-2026-09-21/", "descrizione": "Reuters — 21 settembre 2026, ore 12:09 italiane — conferma indipendente del messaggio e del contesto dell’evento."},
    ],
    "correlati": [
        {"url": "/notizie/google-multa-403-milioni-dpc-irlanda-geolocalizzazione-21-settembre-2026.html", "titolo": "Google, multa da 403 milioni in Irlanda sui dati di geolocalizzazione"},
        {"url": "/notizie/comitato-parlamentare-britannico-chiede-una-legge-sull-ai-per-tutelare-i-diritti-umani-14-09-2026.html", "titolo": "Regno Unito, richiesta una legge sull’IA per tutelare i diritti umani"},
        {"url": "/notizie/vaticano-impianto-agrivoltaico-100-milioni-autosufficienza-energetica-22-agosto-2026.html", "titolo": "Vaticano, impianto agrivoltaico per l’autosufficienza energetica"},
    ],
}


def main() -> None:
    if not SOURCE.exists():
        raise SystemExit(f"immagine sorgente assente: {SOURCE}")
    words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in ARTICLE["paragrafi"])
    if not 300 <= words <= 600:
        raise SystemExit(f"word gate: {words}")
    image = {
        "key": f"{SLUG}-v{VERSION}", "aiGenerated": True, "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation", "variants": variants(),
        "alt": "Scena editoriale contestuale ordinaria generata con IA: Papa Leone XIV riconoscibile in un interno istituzionale romano, con espressione serena; somiglianza sintetica, non è una fotografia documentaria.",
        "disclosure": CAPTION, "sensitiveContext": False, "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": "Pope Leo XIV in a dignified Roman university interior, ordinary contextual editorial scene about AI and peace; no fabricated action, text or watermark.",
    }
    slug = write_article(ARTICLE, image, VERSION)
    register_image(image, slug, VERSION)
    sync_surfaces([ARTICLE], f"/notizie/{slug}.html", VERSION)

    content = {"slug": slug, "title": ARTICLE["titolo"], "excerpt": ARTICLE["sommario"],
               "category": ARTICLE["categoria"], "published_at": ARTICLE["published"],
               "updated_at": ARTICLE["published"], "development_at": DATE,
               "status": ARTICLE["stato"], "public_url": f"https://curiomondo.it/notizie/{slug}.html",
               "publication_state": "pending_deploy", "body": ARTICLE["paragrafi"],
               "sources": ARTICLE["fonti"], "image": image}
    write_json(ROOT / "contenuti/notizie" / f"{slug}.json", content)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["daily_state"].update({"current_question_source_number": 453,
        "last_question_date": DATE,
        "last_question_slug": "lamore-e-un-sentimento-una-decisione-o-una-pratica-quotidiana"})
    used = manifest["daily_state"].setdefault("used_question_source_numbers", [])
    if 453 not in used:
        used.append(453)
    manifest["last_release"] = {"version": VERSION, "date": DATE, "type": "notizia-tecnologia",
        "news_added": [slug], "news_updated": [], "evergreen_added": [],
        "change": "Messaggio di Leone XIV all’AI4Peace sull’intelligenza artificiale al servizio della pace"}
    write_json(manifest_path, manifest)
    print(json.dumps({"added": slug, "words": words, "published": ARTICLE["published"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
