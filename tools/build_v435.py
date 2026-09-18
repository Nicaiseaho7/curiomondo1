#!/usr/bin/env python3
"""Pubblica Cirielli in Armenia e regole TARI (v435)."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 435


def save_image_variants(source: Path, key: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
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
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=86, method=6
        )
        variants.append(
            {
                "w": width,
                "src": f"/assets/images/editorial-auto/{path.name}",
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                "bytes": path.stat().st_size,
            }
        )
    return variants


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def stamp_dates(slug: str, published: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{published}"', page)
    path.write_text(page, encoding="utf-8")


def mark_public_figure(slug: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    html = path.read_text(encoding="utf-8")
    html = html.replace(
        '<figure class="article-image" data-ai-generated="true">',
        '<figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false">',
    )
    path.write_text(html, encoding="utf-8")


def persist_article(article: dict, image: dict, published: str) -> str:
    slug = write_article(article, image, VERSION)
    stamp_dates(slug, published)
    article["published"] = published
    register_image(image, slug, VERSION)
    write_json(
        ROOT / "contenuti" / "notizie" / f"{slug}.json",
        {
            "slug": slug,
            "title": article["titolo"],
            "excerpt": article["sommario"],
            "category": article["categoria"],
            "published_at": published,
            "updated_at": published,
            "development_at": "2026-09-18",
            "status": article.get("stato", "UFFICIALE"),
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": article["paragrafi"],
            "sources": article["fonti"],
            "image": image,
        },
    )
    return slug


ARMENIA = {
    "slug": "cirielli-armenia-aics-jerevan-18-settembre-2026",
    "titolo": "Cirielli chiude la missione in Armenia: AICS apre a Jerevan da ottobre",
    "sommario": "Consultazioni con Kostanyan e Simonyan. Sul tavolo anche la normalizzazione con l’Azerbaigian. La nuova sede coprirà Armenia, Kirghizistan e Tagikistan.",
    "categoria": "Politica",
    "luogo": "Jerevan",
    "formato": "standard",
    "stato": "UFFICIALE",
    "parole_chiave_titolo": ["Cirielli", "Armenia"],
    "dati_chiave": [
        {"icona": "◆", "valore": "2 giorni", "etichetta": "missione del vice ministro a Jerevan"},
        {"icona": "●", "valore": "ottobre", "etichetta": "apertura della sede AICS"},
        {"icona": "↗", "valore": "3 Paesi", "etichetta": "competenza: Armenia, Kirghizistan, Tagikistan"},
    ],
    "paragrafi": [
        "Edmondo Cirielli ha concluso una missione di due giorni in Armenia. Lo comunica il ministero degli Esteri il 18 settembre. Il vice ministro ha tenuto consultazioni con l’omologo Vahan Kostanyan e ha incontrato Alen Simonyan, segretario del Consiglio di sicurezza armeno.",
        "I colloqui, scrive la Farnesina, hanno messo in evidenza rapporti «in forte crescita» e il ruolo di Roma tra i principali partner commerciali di Jerevan. Il comunicato non indica l’importo dell’interscambio. In agenda anche il processo di normalizzazione con l’Azerbaigian.",
        "I due vice ministri hanno annunciato l’apertura della nuova sede dell’Agenzia italiana per la cooperazione allo sviluppo a Jerevan. Sarà operativa dai primi di ottobre. Avrà competenza su Armenia, Kirghizistan e Tagikistan, non solo sul Caucaso.",
        "La Farnesina la definisce un nuovo presidio della cooperazione italiana nella regione. Alla missione hanno partecipato anche l’ICCROM, il centro internazionale per il restauro dei beni culturali, e l’IDLO, organizzazione per il diritto dello sviluppo. Con loro sono in studio iniziative in Armenia su patrimonio e istituzioni. Il comunicato non pubblica accordi firmati.",
        "Non confondere l’annuncio con un ufficio già aperto: la sede parte a ottobre. Né con un trattato di pace: la normalizzazione con Baku è «passata in rassegna», senza esito descritto. Resta un fatto politico, non un cessate-il-fuoco.",
        "Cirielli è vice ministro, non il titolare della Farnesina. Tajani, lo stesso 18 settembre, ha ricevuto a Roma il ministro del Commercio turco Ömer Bolat, con Hormuz e Mar Rosso sul tavolo. Sono due missioni distinte.",
        "Conferma: il comunicato MAECI in italiano e la scheda in inglese della stessa data. Nessuna cifra commerciale nel testo ufficiale. 18 settembre 2026, ore 19.50 Europe/Rome.",
        "Restano fuori da questo pezzo le indiscrezioni su Barbara D’Urso a Ballando: niente annuncio Rai. La TARI, invece, è coperta a parte con il decreto 147 già in Gazzetta.",
    ],
    "fonti": [
        {
            "url": "https://www.esteri.it/it/sala_stampa/archivionotizie/comunicati/2026/09/missione-del-vice-ministro-cirielli-in-armenia/",
            "descrizione": "MAECI — missione Cirielli in Armenia, AICS a Jerevan da ottobre.",
        },
        {
            "url": "https://www.esteri.it/en/sala_stampa/archivionotizie/comunicati/",
            "descrizione": "MAECI in inglese — Deputy Minister Cirielli’s mission to Armenia, 18 September 2026.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/tajani-bolat-turchia-farnesina-hormuz-commercio-18-settembre-2026.html",
            "titolo": "Tajani vede Bolat alla Farnesina: Hormuz e Mar Rosso",
        },
        {
            "url": "/notizie/meloni-oslo-norvegia-gas-fen-saipem-17-settembre-2026.html",
            "titolo": "Meloni a Oslo: gas, FEN e Saipem",
        },
        {
            "url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html",
            "titolo": "Bollo auto, esenzione 2027 fino a 80 kW",
        },
    ],
}

TARI = {
    "slug": "tari-dichiarazione-90-giorni-decreto-147-imu-sanzioni-18-settembre-2026",
    "titolo": "TARI, dichiarazione entro 90 giorni: le regole del decreto 147 già in vigore",
    "sommario": "Dal 12 agosto chi inizia a occupare un immobile ha tre mesi per dichiarare. Dal 2027 multe più basse su TARI e IMU. Non è una delibera di oggi.",
    "categoria": "Economia",
    "luogo": "Italia",
    "formato": "standard",
    "stato": "UFFICIALE",
    "parole_chiave_titolo": ["TARI", "rifiuti"],
    "dati_chiave": [
        {"icona": "◆", "valore": "90 giorni", "etichetta": "termine per la dichiarazione TARI"},
        {"icona": "●", "valore": "12/08", "etichetta": "entrata in vigore del D.Lgs. 147/2026"},
        {"icona": "↗", "valore": "2027", "etichetta": "sanzioni ridotte per omessa o infedele"},
    ],
    "paragrafi": [
        "La tassa sui rifiuti ha un termine nuovo: 90 giorni dall’inizio del possesso o della detenzione dei locali, e altrettanti in caso di variazione. Lo prevede il decreto legislativo 7 agosto 2026, n. 147, in Gazzetta Ufficiale n. 185 dell’11 agosto, in vigore dal 12 agosto. Non è una legge di oggi: è già operativa.",
        "Prima si poteva dichiarare entro il 30 giugno dell’anno successivo. Il Sole 24 Ore, il 12 agosto, ha scritto che imprese e cittadini devono aggiornare il calendario. Il Messaggero lo ha ripreso il 18 settembre. Chi apre un’attività o prende in affitto un immobile deve contare 90 giorni, non l’anno dopo.",
        "Dal 1° gennaio 2027 cambiano le multe. Per la dichiarazione omessa la sanzione è il 100% del tributo non versato, minimo 50 euro, non più la forbice 100-200%. Per l’infedele è il 40%, sempre con minimo 50 euro. Vale anche per IMU, imposta di soggiorno e contributo di sbarco. Le violazioni 2026 restano sul vecchio regime.",
        "Sull’IMU l’articolo 26 del decreto impone la dichiarazione solo telematica, su modello nazionale, di regola entro il 30 giugno dell’anno successivo. Fino al nuovo modello restano quelli già approvati dal MEF.",
        "Per le utenze non domestiche che avviano rifiuti urbani a riciclo o recupero fuori dal servizio pubblico, la quota variabile si riduce in proporzione. La scelta tra servizio pubblico e mercato dura almeno due anni e va comunicata entro il 30 giugno, con effetto dal 1° gennaio successivo.",
        "Il decreto chiude la delega sul federalismo fiscale regionale. Non azzera la TARI e non fissa le tariffe comunali: quelle restano dei Comuni e di ARERA. Chi cerca l’importo 2026 deve aprire l’avviso del proprio Comune, non questo decreto.",
        "Fonti primarie: Normattiva e Gazzetta 185/2026. Letture: PMI.it, Il Sole 24 Ore del 12 agosto, Il Messaggero del 18 settembre. 18 settembre 2026, ore 19.52 Europe/Rome.",
        "Barbara D’Urso a Ballando resta un’indiscrezione di gossip: niente comunicato Rai, quindi niente articolo. L’Armenia, con Cirielli e AICS, è coperta a parte.",
    ],
    "fonti": [
        {
            "url": "https://www.normattiva.it/eli/id/2026/08/11/26G00168/ORIGINAL",
            "descrizione": "Normattiva — D.Lgs. 7 agosto 2026, n. 147, in vigore dal 12 agosto.",
        },
        {
            "url": "https://www.pmi.it/impresa/normativa/470210/riforma-tributi-locali-cosa-cambia-per-imu-e-tari.html",
            "descrizione": "PMI.it — sintesi di TARI 90 giorni, sanzioni 2027 e IMU telematica.",
        },
        {
            "url": "https://www.ilsole24ore.com/art/dichiarazione-imu-telematica-solo-se-ci-sono-variazioni-AJZEOAk",
            "descrizione": "Il Sole 24 Ore — dichiarazione TARI a 90 giorni, in vigore dal 12 agosto.",
        },
        {
            "url": "https://www.ilmessaggero.it/economia/news/imu_tari_taglio_multe_invio_telematico_entro_90_giorni_cosa_cambia-9771680.html",
            "descrizione": "Il Messaggero — ripresa del 18 settembre su IMU, TARI e sanzioni.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/toscana-bando-15-milioni-economia-circolare-rifiuti-7-settembre-2026.html",
            "titolo": "Toscana, 15 milioni per economia circolare e rifiuti",
        },
        {
            "url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html",
            "titolo": "Bollo auto, esenzione 2027 fino a 80 kW",
        },
        {
            "url": "/notizie/istat-produzione-costruzioni-luglio-calo-14-18-settembre-2026.html",
            "titolo": "Istat: produzione nelle costruzioni −1,4% a luglio",
        },
    ],
}


def main() -> None:
    img_a = {
        "key": f"{ARMENIA['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "syntheticLikeness": "public-figure",
        "variants": save_image_variants(
            ROOT / "generated_images" / "cirielli-armenia-v435.jpg", f"{ARMENIA['slug']}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Edmondo Cirielli riconoscibile, occhiali e abito scuro, bandiere di Italia e Armenia; somiglianza sintetica, non è una fotografia documentaria della missione.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-photorealistic Edmondo Cirielli with glasses, Italy and Armenia flags, diplomatic room, no text.",
    }
    img_t = {
        "key": f"{TARI['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "tari-rifiuti-v435.jpg", f"{TARI['slug']}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: raccolta rifiuti urbani in una via italiana, camion arancione e operatori in alta visibilità; non è una fotografia documentaria di un Comune specifico.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Photorealistic Italian municipal waste collection, orange truck, high-vis workers, ordinary street, no text.",
    }

    slug_a = persist_article(ARMENIA, img_a, "2026-09-18T19:50:00+02:00")
    mark_public_figure(slug_a)
    slug_t = persist_article(TARI, img_t, "2026-09-18T19:52:00+02:00")
    sync_surfaces([TARI, ARMENIA], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-18",
        "type": "content-release",
        "news_added": [slug_a, slug_t],
        "news_updated": [],
        "change": "Pubblicati Cirielli in Armenia e regole TARI del decreto 147",
        "image_policy_applied": "new-openai-contextual-editorial-images",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if not path.exists():
            continue
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(
            {
                "currentVersion": VERSION,
                "site_version": VERSION,
                "version": str(VERSION),
                "date": "2026-09-18",
                "release_date": "2026-09-18",
                "articleCount": int(state.get("articleCount", 0)) + 2,
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 2,
                "last_update": "armenia-tari-v435",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "scoop-20260918T195000-Europe-Rome.json",
        {
            "run_at": "2026-09-18T19:50:00+02:00",
            "skill": "ultime-notizie-scoop",
            "desks": ["tassa-rifiuti", "barbara-durso", "armenia"],
            "processed": [
                {"title": ARMENIA["titolo"], "status": "UFFICIALE", "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_a}.html"},
                {"title": TARI["titolo"], "status": "UFFICIALE", "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_t}.html"},
            ],
            "discarded": [
                {"topic": "Barbara D'Urso a Ballando", "reason": "solo Vanity Fair/Libero; nessun comunicato Rai o Ballando"},
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [slug_a, slug_t]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
