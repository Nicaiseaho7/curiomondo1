#!/usr/bin/env python3
"""Pubblica Uffizi/Caravaggio e le dimissioni di Kristersson (v415)."""
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

VERSION = 415
UFFIZI_PUBLISHED = "2026-09-17T20:52:00+02:00"
SVEZIA_PUBLISHED = "2026-09-17T20:48:00+02:00"

UFFIZI_SLUG = "uffizi-infiltrazione-teca-bacco-caravaggio-17-settembre-2026"
SVEZIA_SLUG = "svezia-kristersson-si-dimette-andersson-176-seggi-17-settembre-2026"


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


UFFIZI = {
    "slug": UFFIZI_SLUG,
    "titolo": "Uffizi, la pioggia bagna la teca del Bacco di Caravaggio: nessuna opera danneggiata",
    "sommario": "Un temporale con oltre 45 millimetri in un'ora ha provocato un'infiltrazione sotto il lucernario della sala del Seicento. Il museo ha rimosso il dipinto per i controlli e riaprirà la sala venerdì mattina.",
    "categoria": "Cronaca",
    "luogo": "Firenze",
    "formato": "standard",
    "parole_chiave_titolo": ["Uffizi", "Caravaggio"],
    "dati_chiave": [
        {"icona": "◆", "valore": "45,5 mm", "etichetta": "pioggia in un'ora a Boboli"},
        {"icona": "●", "valore": "0", "etichetta": "opere danneggiate secondo il museo"},
        {"icona": "↗", "valore": "7", "etichetta": "dipinti del Seicento in sala"},
    ],
    "paragrafi": [
        "Un temporale su Firenze ha provocato giovedì 17 settembre un'infiltrazione d'acqua alla Galleria degli Uffizi. L'acqua è filtrata sotto il lucernario della sala del Seicento e ha schizzato il vetro esterno della teca del Bacco di Caravaggio. Il museo riferisce che nessuna opera è danneggiata.",
        "Il Centro funzionale regionale ha misurato 44,6 millimetri in un'ora all'Orto Botanico e 45,5 millimetri al Giardino di Boboli. Il comunicato del museo parla di una bomba d'acqua con oltre 45 millimetri nello stesso intervallo.",
        "Gli schizzi hanno colpito il vetro esterno della vetrina protettiva, non la tela. Visitatori hanno visto il vetro appannato da scie d'acqua, secondo Corriere Fiorentino e La Nazione. Il Bacco, olio su tela del 1598, restava separato dagli schizzi dalla teca.",
        "I tecnici delle Gallerie hanno chiuso la sala, rimosso il dipinto e poi riaperto lo spazio con la teca vuota. La teca vuota è una misura precauzionale. Non equivale a un danno accertato sul quadro.",
        "«A seguito delle dovute verifiche non è risultato alcun danno a nessuna delle opere», ha fatto sapere il museo. Nella stessa sala sono esposti sette dipinti del Seicento. La sala riaprirà all'orario ordinario di venerdì mattina.",
        "Le verifiche riguardano anche gli altri sei dipinti della sala. Il museo non ha segnalato danni a questi. Resta da mettere in sicurezza il lucernario e l'infisso che incombe sul vano espositivo.",
        "Lo stesso temporale ha prodotto allagamenti in più zone della Toscana. Questo episodio, però, è un'infiltrazione puntuale da copertura, non un allagamento delle sale. Il comunicato non indica danni strutturali all'edificio oltre lo schizzo sulla teca.",
        "Non è ancora pubblico un piano di lavori sul lucernario né la data di ricollocazione del Bacco. I prossimi riscontri saranno la riapertura della sala, l'esito dei controlli conservativi e l'eventuale intervento sull'infisso.",
    ],
    "fonti": [
        {
            "url": "https://www.ansa.it/sito/notizie/cronaca/2026/09/17/la-pioggia-si-infiltra-agli-uffizi-e-bagna-la-teca-del-bacco-di-caravaggio_073cc186-e20b-422e-a5d7-ea3397fda99b.html",
            "descrizione": "ANSA — comunicato del museo, assenza di danni e riapertura della sala venerdì mattina.",
        },
        {
            "url": "https://corrierefiorentino.corriere.it/notizie/cronaca/26_settembre_17/firenze-al-museo-degli-uffizi-piove-sulla-teca-del-bacco-di-caravaggio-d488c5d3-c019-47fa-8d4a-a678f6a63xlk.shtml",
            "descrizione": "Corriere Fiorentino — cronaca in sala, teca vuota dopo i controlli e testo del comunicato.",
        },
        {
            "url": "https://www.ilmessaggero.it/italia/firenze_bomba_d_acqua_galleria_uffizi_ultima_ora-9769523.html",
            "descrizione": "Il Messaggero — dati del Centro funzionale regionale su Orto Botanico e Boboli.",
        },
        {
            "url": "https://www.lanazione.it/firenze/cronaca/nubifragio-a-firenze-piove-dentro-la-galleria-degli-uffizi-acqua-sulla-teca-del-bacco-di-caravaggio-jr9vxsqc",
            "descrizione": "La Nazione — chiusura precauzionale della sala e riapertura con teca vuota.",
        },
        {
            "url": "https://www.open.online/2026/09/17/uffizi-infiltrazione-teca-bacco-caravaggio-firenze/",
            "descrizione": "Open — riscontro indipendente su infiltrazione, schizzi sul vetro esterno e verifiche.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/maltempo-allerta-arancione-liguria-emilia-romagna-17-settembre-2026.html",
            "titolo": "Maltempo, allerta arancione su Liguria ed Emilia-Romagna",
        },
        {
            "url": "/notizie/come-si-rintracciano-recuperano-opere-arte-rubate.html",
            "titolo": "Come si rintracciano e recuperano le opere d'arte rubate",
        },
        {
            "url": "/notizie/nubifragio-a-firenze-piove-dentro-la-galleria-degli-uffizi-acqua-sulla-teca-del-bacco-di-caravaggio.html",
            "titolo": "",
        },
    ],
}

SVEZIA = {
    "slug": SVEZIA_SLUG,
    "titolo": "Svezia, Kristersson si dimette: il centrosinistra chiude 176-173 e Andersson forma il governo",
    "sommario": "Dopo quattro giorni di scrutinio il blocco rosso-verde ottiene 176 seggi su 349. Il premier uscente ha chiesto al presidente del Parlamento di essere sollevato dall'incarico.",
    "categoria": "Mondo",
    "luogo": "Stoccolma",
    "formato": "standard",
    "parole_chiave_titolo": ["Kristersson", "Andersson"],
    "dati_chiave": [
        {"icona": "◆", "valore": "176-173", "etichetta": "seggi centrosinistra-destra"},
        {"icona": "●", "valore": "175", "etichetta": "soglia di maggioranza nel Riksdag"},
        {"icona": "↗", "valore": "29/9", "etichetta": "data indicata per la nomina"},
    ],
    "paragrafi": [
        "Ulf Kristersson si è dimesso giovedì 17 settembre da primo ministro della Svezia. Il conteggio definitivo delle elezioni del 13 settembre assegna 176 seggi su 349 al centrosinistra e 173 alla coalizione di destra. Lo ha certificato l'Autorità elettorale dopo quattro giorni di scrutinio.",
        "L'ultimo dei 6.626 seggi ha chiuso a Göteborg, con i voti dall'estero. Il vantaggio di tre seggi, già indicato dai dati preliminari del 14 settembre, è così ufficiale. Nel Riksdag la maggioranza minima è 175.",
        "In una lettera pubblicata su X, Kristersson ha chiesto al presidente del Parlamento di essere sollevato dall'incarico «affinché questo lavoro possa iniziare senza ritardi». La mossa apre la procedura di formazione del governo.",
        "Magdalena Andersson, leader dei Socialdemocratici ed ex premier sconfitta nel 2022, riceve ora l'incarico di formare l'esecutivo. Il blocco rosso-verde comprende Socialdemocratici, Sinistra, Centro e Verdi.",
        "Tre seggi di scarto bastano sulla carta, ma non garantiscono un governo rapido. All'interno del blocco restano distanze su tasse, welfare e ruolo della sinistra. Gli osservatori indicano trattative potenzialmente lunghe settimane.",
        "I Democratici Svedesi, alleati uscenti di Kristersson, hanno perso consensi rispetto al 2022. Non entreranno in un governo di centrosinistra. Sky TG24 riferisce che il nuovo premier potrebbe non essere nominato prima del 29 settembre.",
        "Quattro anni fa le prime proiezioni diedero Andersson in vantaggio, poi superata nel conteggio finale da Kristersson. Stavolta il dato definitivo conferma il margine. Reuters, ANSA e Il Sole 24 Ore coincidono su seggi e dimissioni.",
        "I passaggi successivi dipendono dal presidente del Parlamento e dalle trattative tra i quattro partiti del blocco vincente. Restano da definire composizione, programma e tempi del nuovo esecutivo.",
    ],
    "fonti": [
        {
            "url": "https://www.reuters.com/fr/affaires/sude-le-centre-gauche-majoritaire-aprs-les-lgislatives-2026-09-17/",
            "descrizione": "Reuters — dimissioni di Kristersson, 176-173 e testo della lettera al presidente del Parlamento.",
        },
        {
            "url": "https://www.ansa.it/sito/notizie/mondo/2026/09/17/terminato-lo-scrutinio-il-centro-sinistra-vince-di-misura-in-svezia_8ab52f09-7bf3-4618-bed2-54a92d9552ec.html",
            "descrizione": "ANSA — scrutinio concluso a Göteborg, composizione del blocco rosso-verde e incarico ad Andersson.",
        },
        {
            "url": "https://tg24.sky.it/mondo/2026/09/17/elezioni-svezia-risultato",
            "descrizione": "Sky TG24 — lettera di dimissioni, trattative e possibile nomina non prima del 29 settembre.",
        },
        {
            "url": "https://www.ilsole24ore.com/art/svezia-centro-sinistra-vince-fotofinish-andersson-avanti-tre-seggi-kristersson-si-dimette-AJZk5DGB",
            "descrizione": "Il Sole 24 Ore — conferma dei seggi, flessione dei Democratici Svedesi e difficoltà interne al centrosinistra.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/svezia-centrosinistra-avanti-elezioni-14-settembre-2026.html",
            "titolo": "Svezia, centrosinistra avanti di tre seggi: risultato ancora provvisorio",
        },
        {
            "url": "/notizie/trump-ue-canada-associazione-dazi-17-settembre-2026.html",
            "titolo": "Trump minaccia dazi se l'Ue assocerà il Canada",
        },
        {
            "url": "/notizie/brics-dichiarazione-new-delhi-medio-oriente-12-settembre-2026.html",
            "titolo": "Brics, a New Delhi la dichiarazione sul Medio Oriente",
        },
    ],
}

# Drop the empty correlato placeholder if the third Uffizi related URL does not exist.
UFFIZI["correlati"] = [
    item
    for item in UFFIZI["correlati"]
    if item.get("titolo") and (ROOT / "notizie" / Path(item["url"]).name).exists()
]
if len(UFFIZI["correlati"]) < 3:
    extra = ROOT / "notizie" / "cinema-uscite-italia-14-20-settembre-2026.html"
    if extra.exists():
        UFFIZI["correlati"].append(
            {
                "url": "/notizie/cinema-uscite-italia-14-20-settembre-2026.html",
                "titolo": "Cinema, le uscite in Italia dal 14 al 20 settembre",
            }
        )


def publish(article: dict, image: dict, published: str) -> str:
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
            "development_at": "2026-09-17",
            "status": "UFFICIALE",
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": article["paragrafi"],
            "sources": article["fonti"],
            "image": image,
        },
    )
    return slug


def main() -> None:
    uffizi_image = {
        "key": f"{UFFIZI_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "uffizi-bacco-v415.jpg", f"{UFFIZI_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: sala della Galleria degli Uffizi con teca vuota e pavimento bagnato sotto un lucernario; non è una fotografia documentaria dell'infiltrazione.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-realistic editorial news photograph of Uffizi Gallery interior, empty glass display case, wet marble floor under a skylight after rain; no text, watermark or infographic.",
    }
    svezia_image = {
        "key": f"{SVEZIA_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "svezia-kristersson-v415.jpg", f"{SVEZIA_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Ulf Kristersson fuori da un edificio governativo a Stoccolma; somiglianza sintetica, non una fotografia documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": "Ultra-realistic editorial photograph of Ulf Kristersson outside Rosenbad in Stockholm; contextual ordinary political scene, no text or watermark.",
    }

    publish(UFFIZI, uffizi_image, UFFIZI_PUBLISHED)
    publish(SVEZIA, svezia_image, SVEZIA_PUBLISHED)
    sync_surfaces([UFFIZI, SVEZIA], "", VERSION)

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
        "date": "2026-09-17",
        "type": "content-release",
        "news_added": [UFFIZI_SLUG, SVEZIA_SLUG],
        "news_updated": [],
        "change": "Pubblicate l'infiltrazione agli Uffizi sul Bacco di Caravaggio e le dimissioni di Kristersson in Svezia",
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
                "date": "2026-09-17",
                "release_date": "2026-09-17",
                "articleCount": int(state.get("articleCount", 0)) + 2,
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 2,
                "last_update": "uffizi-svezia-v415",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "editoriale-20260917T205200-Europe-Rome.json",
        {
            "run_at": UFFIZI_PUBLISHED,
            "scope": "Italia+Mondo",
            "production_branch": "main",
            "processed": [
                {
                    "title": UFFIZI["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "sources": [x["url"] for x in UFFIZI["fonti"]],
                    "public_url": f"https://curiomondo.it/notizie/{UFFIZI_SLUG}.html",
                },
                {
                    "title": SVEZIA["titolo"],
                    "status": "CONFERMATA DA PIÙ FONTI",
                    "decision": "publish",
                    "sources": [x["url"] for x in SVEZIA["fonti"]],
                    "public_url": f"https://curiomondo.it/notizie/{SVEZIA_SLUG}.html",
                },
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [UFFIZI_SLUG, SVEZIA_SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
