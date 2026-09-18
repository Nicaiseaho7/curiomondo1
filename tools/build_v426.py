#!/usr/bin/env python3
"""Pubblica lettera Schlein-Meloni e speronamento Mar Cinese (v426)."""
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

VERSION = 426
SCHLEIN_PUBLISHED = "2026-09-18T09:50:00+02:00"
CINA_PUBLISHED = "2026-09-18T09:46:00+02:00"

SCHLEIN_SLUG = "schlein-lettera-meloni-14-miliardi-energia-conte-17-settembre-2026"
CINA_SLUG = "mar-cinese-cina-sperona-nave-bfar-palawan-18-settembre-2026"


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
            path, "WEBP", quality=84, method=6
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


SCHLEIN = {
    "slug": SCHLEIN_SLUG,
    "titolo": "Schlein propone a Meloni 14 miliardi per clima ed energia. Conte: non ci sono le condizioni",
    "sommario": "La segretaria Pd indica lo 0,6% di Pil in deroga ai vincoli di bilancio entro il 2028. Da Oslo la premier dice che approfondirà senza pregiudizi. M5s e Avs chiudono.",
    "categoria": "Politica",
    "luogo": "Roma / Oslo",
    "formato": "standard",
    "parole_chiave_titolo": ["Schlein", "Meloni"],
    "dati_chiave": [
        {"icona": "◆", "valore": "14 mld", "etichetta": "spazio fiscale indicato dal Pd"},
        {"icona": "●", "valore": "0,6%", "etichetta": "del Pil in tre anni, stima Pd"},
        {"icona": "↗", "valore": "2028", "etichetta": "scadenza indicata per l’impiego"},
    ],
    "paragrafi": [
        "Elly Schlein ha scritto a Giorgia Meloni proponendo di usare circa 14 miliardi di euro per clima ed energia entro il 2028. La lettera è stata pubblicata su Repubblica il 17 settembre. Da Oslo la premier ha detto che intende approfondirla «senza pregiudizi».",
        "I 14 miliardi non sono un nuovo trasferimento da Bruxelles. Schlein cita la possibilità, prevista dalla Commissione europea, di usare fino allo 0,6% del Pil in tre anni in deroga ai vincoli di bilancio per la transizione energetica. È spazio fiscale nazionale, non un fondo già assegnato.",
        "Il Pd indica cinque voci: 2 miliardi per raddoppiare il Conto Termico, 3 miliardi in più sul Piano casa per gli alloggi Erp, 4 miliardi per le imprese, 3 miliardi per metropolitane e bus elettrici, 2 miliardi per reti e accumuli. Open riporta lo stesso elenco.",
        "La lettera chiede anche di rivedere la tassazione sull’elettricità, oggi più alta di quella sul gas. Schlein la definisce in contrasto con le indicazioni della Commissione. Non è un disegno di legge: è una proposta politica al governo.",
        "Meloni, dopo il bilaterale con Støre, ha detto di non avere ancora approfondito il testo. «Se ci saranno delle proposte utili le prenderò in considerazione». Ha letto un «implicito riconoscimento» del Piano casa, che il Pd aveva contestato.",
        "Giuseppe Conte ha chiuso su Dritto e Rovescio. «Oggi non ci sono le condizioni per lavorare insieme» con chi, ha detto, vuole le trivellazioni. Ha aggiunto che Meloni «è meglio che vada a casa». ANSA riporta le frasi.",
        "Angelo Bonelli, per Avs, ha detto all’Adnkronos di non condividere «questa mano tesa». Distingue il merito delle proposte, che giudica condivisibili, dalla richiesta di collaborare con il governo.",
        "Meloni non ha accettato il piano da 14 miliardi né aperto un tavolo. Il fatto politico è lo strappo nel campo largo: Pd chiede un’intesa settoriale, M5s e Avs la respingono. I prossimi passi dipendono da un eventuale esame formale a Palazzo Chigi.",
    ],
    "fonti": [
        {
            "url": "https://www.open.online/2026/09/17/elly-schlein-lettera-giorgia-meloni-miliardi-energia/",
            "descrizione": "Open — testo della proposta Pd, 0,6% del Pil e le cinque voci di spesa.",
        },
        {
            "url": "https://www.repubblica.it/politica/2026/09/17/news/meloni_risponde_lettera_schlein_non_ho_pregiudizi-425591428/",
            "descrizione": "la Repubblica — risposta di Meloni da Oslo e pubblicazione della lettera.",
        },
        {
            "url": "https://www.ansa.it/sito/notizie/politica/2026/09/17/conte-schlein-non-ci-sono-le-condizioni-per-lavorare-insieme-a-meloni_fe0983cc-c330-46e9-9549-d58a6e069aa5.html",
            "descrizione": "ANSA — Conte a Dritto e Rovescio: non ci sono le condizioni.",
        },
        {
            "url": "https://www.adnkronos.com/politica/schlein-lettera-meloni-conte-governo_5TavQ6kWfmHTy1lzUZC3vG",
            "descrizione": "Adnkronos — gelata di Conte e Bonelli, Meloni non chiude.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/meloni-oslo-norvegia-gas-fen-saipem-17-settembre-2026.html",
            "titolo": "Meloni a Oslo: la Norvegia resta il quarto fornitore di gas",
        },
        {
            "url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html",
            "titolo": "Bollo auto, esenzione per 14,5 milioni di veicoli",
        },
        {
            "url": "/notizie/pd-primarie-centrosinistra-schlein-conte-26-agosto-2026.html",
            "titolo": "Pd, primarie del centrosinistra: Schlein e Conte",
        },
    ],
}

CINA = {
    "slug": CINA_SLUG,
    "titolo": "Mar Cinese, Manila: una nave della Guardia costiera cinese sperona un’unità della BFAR",
    "sommario": "Secondo la Guardia costiera filippina il contatto è avvenuto venerdì mattina al largo di Palawan, durante una missione di carburante ai pescatori. Pechino non ha ancora risposto.",
    "categoria": "Mondo",
    "luogo": "Mar Cinese meridionale",
    "formato": "standard",
    "parole_chiave_titolo": ["Manila", "Palawan"],
    "dati_chiave": [
        {"icona": "◆", "valore": "54 mn", "etichetta": "da Palawan, secondo Manila"},
        {"icona": "●", "valore": "11:13", "etichetta": "ora locale del contatto"},
        {"icona": "↗", "valore": "0", "etichetta": "feriti nei resoconti consultati"},
    ],
    "paragrafi": [
        "La Guardia costiera filippina ha detto che venerdì 18 settembre una nave della China Coast Guard ha speronato un’unità del Bureau of Fisheries and Aquatic Resources. La BRP Datu Magat Salamat distribuiva carburante ai pescatori. Reuters e Bloomberg riportano il comunicato di Manila.",
        "L’episodio è collocato a circa 54 miglia nautiche da Palawan, nelle acque che Manila considera zona economica esclusiva. GMA News indica 6,36 miglia a nord-nordovest dell’Abad Santos Shoal, nello Spratly.",
        "Secondo il portavoce Jay Tarriela, alle 11:04 la CCG-21585 ha tagliato la poppa a circa 10 metri. Alle 11:13 ha ripetuto la manovra e ha fatto contatto. AFP e Manila Times riportano gli orari del comunicato.",
        "Il comunicato elenca danni a ringhiere di dritta, stantie e attrezzature di coperta, con detriti sul ponte. Nei testi consultati non risultano feriti. L’ammiraglio Ronnie Gil Gavan ha inviato mezzi di superficie e aerei per assistere l’equipaggio.",
        "Manila parla di speronamento «deliberato» di «una nave civile del governo» in missione «umanitaria e di sostentamento». È la ricostruzione filippina. Non è una sentenza su intenzioni o diritto del mare.",
        "L’ambasciata cinese a Manila non ha risposto subito a Reuters. Nei testi consultati manca una versione di Pechino su scafo, orari e manovre. I dettagli operativi restano quindi a fonte unica, pur coincidendo tra testate.",
        "A luglio Manila aveva accusato Pechino di idranti vicino a Scarborough e di un colpo di bastone a un militare a Second Thomas Shoal. Sono episodi precedenti, non una prova di questo contatto.",
        "Un video diffuso dalla Guardia costiera, secondo Manila Times, mostra la nave cinese vicina alla poppa; l’impatto non è visibile. Restano da verificare una replica cinese e l’esito dei soccorsi. Pechino rivendica gran parte del Mar Cinese; un lodo del 2016 ha detto che quella pretesa non ha base giuridica.",
    ],
    "fonti": [
        {
            "url": "https://www.reuters.com/world/china/china-vessel-rams-damages-philippine-fishing-boat-coast-guard-says-2026-09-18/",
            "descrizione": "Reuters — comunicato filippino, danni, missione carburante, nessuna replica cinese immediata.",
        },
        {
            "url": "https://www.bloomberg.com/news/articles/2026-09-18/philippines-says-china-coast-guard-rammed-its-fisheries-boat",
            "descrizione": "Bloomberg — conferma indipendente del comunicato e del post di Tarriela.",
        },
        {
            "url": "https://www.manilatimes.net/2026/09/18/news/chinese-ship-rams-philippine-vessel-in-south-china-sea/2428073",
            "descrizione": "Manila Times / AFP — CCG-21585, orari 11:04 e 11:13, video senza impatto visibile.",
        },
        {
            "url": "https://www.gmanetwork.com/news/topstories/nation/1002818/chinese-vessel-rams-ph-ship-on-fuel-subsidy-mission-near-palawan/story/",
            "descrizione": "GMA News — 6,36 miglia dall’Abad Santos Shoal e 54 miglia da Palawan.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/cina-taiwan-forum-isole-pacifico-palau-1-settembre-2026.html",
            "titolo": "Cina e Taiwan al forum delle isole del Pacifico a Palau",
        },
        {
            "url": "/notizie/forum-pacifico-cina-missile-nauru-palau-4-settembre-2026.html",
            "titolo": "Forum del Pacifico, missile cinese e tensioni a Nauru e Palau",
        },
        {
            "url": "/notizie/filippine-incendio-traghetto-june-aster-76-morti-12-settembre-2026.html",
            "titolo": "Filippine, incendio sul traghetto June Aster: 76 morti",
        },
    ],
}


def publish(article: dict, image: dict, published: str, status: str) -> str:
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
            "status": status,
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": article["paragrafi"],
            "sources": article["fonti"],
            "image": image,
        },
    )
    return slug


def main() -> None:
    schlein_image = {
        "key": f"{SCHLEIN_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "schlein-v426.jpg", f"{SCHLEIN_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Elly Schlein riconoscibile all’aperto a Roma; somiglianza sintetica, non una fotografia documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": "Photorealistic editorial photograph of Elly Schlein in Rome, ordinary contextual political scene, no text.",
    }
    cina_image = {
        "key": f"{CINA_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "cina-filippine-v426.jpg", f"{CINA_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale del luogo generata con IA: due navi governative distanti nel Mar Cinese, senza collisione; non è una fotografia documentaria dello speronamento.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Photorealistic distant Chinese coast guard cutter and Philippine fisheries vessel at sea, no collision, no text.",
    }

    publish(SCHLEIN, schlein_image, SCHLEIN_PUBLISHED, "UFFICIALE")
    publish(CINA, cina_image, CINA_PUBLISHED, "CONFERMATA DA PIÙ FONTI")
    sync_surfaces([SCHLEIN, CINA], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update(
        {
            "site_version": VERSION,
            "version": f"v{VERSION}",
            "release_version": f"v{VERSION}",
        }
    )
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-18",
        "type": "content-release",
        "news_added": [SCHLEIN_SLUG, CINA_SLUG],
        "news_updated": [],
        "change": "Pubblicate la lettera Schlein-Meloni sui 14 miliardi e lo speronamento nel Mar Cinese",
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
                "last_update": "schlein-meloni-mar-cinese-v426",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "editoriale-20260918T095000-Europe-Rome.json",
        {
            "run_at": SCHLEIN_PUBLISHED,
            "scope": "Italia+Mondo",
            "production_branch": "main",
            "processed": [
                {
                    "title": SCHLEIN["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "sources": [x["url"] for x in SCHLEIN["fonti"]],
                    "public_url": f"https://curiomondo.it/notizie/{SCHLEIN_SLUG}.html",
                },
                {
                    "title": CINA["titolo"],
                    "status": "CONFERMATA DA PIÙ FONTI",
                    "decision": "publish",
                    "sources": [x["url"] for x in CINA["fonti"]],
                    "public_url": f"https://curiomondo.it/notizie/{CINA_SLUG}.html",
                },
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [SCHLEIN_SLUG, CINA_SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
