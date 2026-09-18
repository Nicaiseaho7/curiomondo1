#!/usr/bin/env python3
"""Pubblica Meloni a Oslo e la petroliera Trend a Hormuz (v425)."""
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

VERSION = 425
MELONI_PUBLISHED = "2026-09-18T07:50:00+02:00"
HORMUZ_PUBLISHED = "2026-09-18T07:46:00+02:00"

MELONI_SLUG = "meloni-oslo-norvegia-gas-fen-saipem-17-settembre-2026"
HORMUZ_SLUG = "hormuz-pasdaran-petroliera-trend-togo-17-settembre-2026"


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


MELONI = {
    "slug": MELONI_SLUG,
    "titolo": "Meloni a Oslo: la Norvegia resta il quarto fornitore di gas, sul tavolo Fen e l’industria",
    "sommario": "Prima visita ufficiale di un premier italiano in Norvegia dopo quasi 15 anni. Meloni e Støre parlano di energia, materie critiche e cantieristica; non è stato firmato un nuovo trattato.",
    "categoria": "Italia",
    "luogo": "Oslo",
    "formato": "standard",
    "parole_chiave_titolo": ["Meloni", "Oslo"],
    "dati_chiave": [
        {"icona": "◆", "valore": "15 anni", "etichetta": "dall’ultima visita ufficiale italiana"},
        {"icona": "●", "valore": "4°", "etichetta": "posto della Norvegia tra i fornitori di gas"},
        {"icona": "↗", "valore": "Fen", "etichetta": "giacimento citato per le materie critiche"},
    ],
    "paragrafi": [
        "Giorgia Meloni è stata a Oslo giovedì 17 settembre, ospite del primo ministro norvegese Jonas Gahr Støre. È la prima visita ufficiale di un presidente del Consiglio italiano in Norvegia dopo quasi 15 anni. Sul tavolo: energia, materie prime critiche, difesa e industria.",
        "«Per noi la Norvegia è un partner di primo piano in Europa, lo è certamente per il ruolo che ha nella diversificazione degli approvvigionamenti energetici italiani, nostro quarto fornitore di gas», ha detto Meloni. Il testo è sul sito di Palazzo Chigi.",
        "La premier ha indicato il giacimento di Fen come risorsa per le materie prime critiche. L’obiettivo dichiarato è costruire filiere più corte e più resistenti agli shock. Non è stato annunciato un contratto di fornitura.",
        "Meloni ha citato la fusione tra Saipem e Subsea7 come esempio di complementarità industriale. Il gruppo, ha detto, diventerà il secondo operatore mondiale nei servizi offshore. Il Sole 24 Ore riporta la stessa indicazione.",
        "Støre ha definito Eni «un partner con competenze molto significative» nella ricerca di gas nell’Artico. Sky TG24 elenca Leonardo, Fincantieri e Saipem tra i partecipanti alla cena di lavoro. La lista non equivale a un accordo firmato.",
        "Meloni ha detto di riportare a Roma «un partenariato industriale e strategico» centrato sull’energia e esteso ad altri settori di sicurezza. Resta da tradurre l’intesa politica in atti, scadenze e impegni finanziari.",
        "Italia e Norvegia festeggiano nel 2026 il centenario del volo artico del dirigibile Norge, con Umberto Nobile e Roald Amundsen. La ricorrenza è contestuale alla visita, non un nuovo trattato.",
        "I prossimi passaggi saranno gli eventuali accordi su gas, minerali e cantieristica. Finché non esistono testi firmati, la missione resta un allineamento politico, non una svolta già misurabile sui prezzi energetici.",
    ],
    "fonti": [
        {
            "url": "https://www.governo.it/it/articolo/conferenza-stampa-con-il-primo-ministro-norvegese-st-re-lintroduzione-del-presidente-meloni",
            "descrizione": "Presidenza del Consiglio — testo ufficiale della conferenza stampa a Oslo, 17 settembre 2026.",
        },
        {
            "url": "https://en.ilsole24ore.com/art/energy-defence-critical-raw-materials-meloni-strengthens-ties-with-norway-with-an-eye-on-the-arctic-AJ5v0OGB",
            "descrizione": "Il Sole 24 Ore — Fen, Saipem-Subsea7, Eni nell’Artico e quadro della visita.",
        },
        {
            "url": "https://tg24.sky.it/mondo/2026/09/17/meloni-norvegia-oggi",
            "descrizione": "Sky TG24 — prima visita ufficiale dopo 15 anni, bilaterale con Støre e cena con imprese.",
        },
        {
            "url": "https://www.lastampa.it/politica/2026/09/18/news/meloni_caccia_italiani_contro_jet_russi_non_dobbiamo_rispondere-15741981/",
            "descrizione": "La Stampa — riscontro dalla missione a Oslo e contesto energetico della visita.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/lituania-jet-russi-eurofighter-italiani-scramble-17-settembre-2026.html",
            "titolo": "Lituania, due jet russi nello spazio aereo: decollano gli Eurofighter italiani",
        },
        {
            "url": "/notizie/bab-el-mandeb-crosetto-missione-navale-mercantili-italiani-17-settembre-2026.html",
            "titolo": "Bab el-Mandeb, Crosetto attiva la Marina per i mercantili italiani",
        },
        {
            "url": "/notizie/norvegia-funerali-stato-re-harald-v-oslo-9-settembre-2026.html",
            "titolo": "Norvegia, funerali di Stato per re Harald V a Oslo",
        },
    ],
}

HORMUZ = {
    "slug": HORMUZ_SLUG,
    "titolo": "Hormuz, i pasdaran dicono di aver colpito la petroliera Trend: incendio e nave ferma",
    "sommario": "IRNA e Reuters riportano la rivendicazione iraniana sulla nave battente bandiera del Togo. UKMTO ha segnalato un incidente vicino a Khasab; non è confermato che sia lo stesso caso.",
    "categoria": "Mondo",
    "luogo": "Stretto di Hormuz",
    "formato": "standard",
    "parole_chiave_titolo": ["Hormuz", "Trend"],
    "dati_chiave": [
        {"icona": "◆", "valore": "Trend", "etichetta": "petroliera Togo secondo IRNA"},
        {"icona": "●", "valore": "16 mn", "etichetta": "da Khasab l’incidente UKMTO"},
        {"icona": "↗", "valore": "3", "etichetta": "transiti AIS mercoledì, da 12"},
    ],
    "paragrafi": [
        "La Marina delle Guardie della rivoluzione islamica ha dichiarato di aver colpito giovedì 17 settembre la petroliera Trend, battente bandiera del Togo, nello Stretto di Hormuz. Secondo IRNA la nave ha preso fuoco e si è fermata. Reuters riporta la stessa versione iraniana.",
        "Il comandante della Marina dei pasdaran, ammiraglio Ali Azmai, ha detto che la Trend tentava un «passaggio illegale» «con l’istigazione» delle forze statunitensi. È una tesi iraniana. Nei testi consultati non compare una conferma indipendente di quella istigazione.",
        "Le fonti consultate non indicano feriti, morti o lo stato dell’equipaggio. Non è pubblico un comunicato dell’armatore né l’identità commerciale completa della nave oltre nome e bandiera.",
        "UK Maritime Trade Operations ha segnalato giovedì sera un incidente di sicurezza nello stretto, 16 miglia nautiche a nord-est di Khasab, in Oman. Al Jazeera precisa che non è chiaro se coincida con la Trend.",
        "I dati AIS citati da Al Jazeera indicano tre transiti di navi di materie prime mercoledì, contro 12 il giorno precedente e una media di circa 17 nelle ultime dieci giornate. Prima della guerra in Iran, a fine febbraio, i transiti quotidiani di grandi navi commerciali erano intorno a 125.",
        "Attraverso Hormuz passa circa il 20% delle forniture mondiali giornaliere di greggio e gas naturale liquefatto. Il dato descrive l’esposizione della rotta, non un effetto già misurato di questo singolo attacco.",
        "La differenza tra le fonti è sostanziale. Teheran nomina la Trend, parla di sequestro dopo l’incendio e attribuisce il transito a un’istigazione americana. UKMTO registra un incidente senza il nome della nave. Manca un riscontro degli Stati Uniti nei testi consultati.",
        "Restano da verificare identità dell’armatore, condizioni dell’equipaggio e se l’incidente UKMTO e la Trend siano lo stesso caso. Finché manca un riscontro indipendente, l’attacco resta una rivendicazione iraniana, non una ricostruzione completa dell’evento.",
    ],
    "fonti": [
        {
            "url": "https://www.thehindu.com/news/international/togo-flagged-tanker-stuck-in-strait-of-hormuz-iran-guards/article71478387.ece",
            "descrizione": "The Hindu / Reuters — rivendicazione dei pasdaran su attacco, incendio e nave ferma.",
        },
        {
            "url": "https://www.repubblica.it/esteri/2026/09/18/diretta/guerra_iran_usa_israele_news_oggi-425591966/",
            "descrizione": "la Repubblica — IRNA: Trend colpita e sequestrata dopo l’incendio a Hormuz.",
        },
        {
            "url": "https://www.aljazeera.net/news/2026/9/18/5187",
            "descrizione": "Al Jazeera — Azmai, UKMTO a 16 miglia da Khasab e calo dei transiti AIS.",
        },
        {
            "url": "https://en.wikipedia.org/wiki/Portal:Current_events/2026_September_18",
            "descrizione": "Wikipedia Current events — IRNA: petroliera Trend battente bandiera del Togo.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/stretto-hormuz-traffico-sette-navi-11-settembre-2026.html",
            "titolo": "Stretto di Hormuz, colpita una nave commerciale iraniana: un morto",
        },
        {
            "url": "/notizie/brent-oltre-100-dollari-attacchi-navi-stretto-hormuz-10-settembre-2026.html",
            "titolo": "Brent oltre i 100 dollari dopo gli attacchi alle navi a Hormuz",
        },
        {
            "url": "/notizie/usa-iran-nuovi-raid-hormuz-2-settembre-2026.html",
            "titolo": "Usa e Iran, nuovi raid nello Stretto di Hormuz",
        },
    ],
}


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
            "development_at": "2026-09-18",
            "status": "CONFERMATA DA PIÙ FONTI" if article is HORMUZ else "UFFICIALE",
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": article["paragrafi"],
            "sources": article["fonti"],
            "image": image,
        },
    )
    return slug


def main() -> None:
    meloni_image = {
        "key": f"{MELONI_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "meloni-oslo-v425.jpg", f"{MELONI_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Giorgia Meloni riconoscibile all’aperto a Oslo con bandiere norvegesi; somiglianza sintetica, non una fotografia documentaria della visita.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": "Photorealistic editorial photograph of Giorgia Meloni in Oslo with Norwegian flags; ordinary contextual scene, no text or watermark.",
    }
    hormuz_image = {
        "key": f"{HORMUZ_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "hormuz-trend-v425.jpg", f"{HORMUZ_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale del luogo generata con IA: petroliera intatta a distanza nello Stretto di Hormuz, senza incendio né persone; non è una fotografia documentaria dell’attacco.",
        "disclosure": CAPTION,
        "sensitiveContext": True,
        "reenactedEvent": False,
        "prompt": "Photorealistic distant oil tanker intact in the Strait of Hormuz, no fire, no crew, no attack reconstruction, no text.",
    }

    publish(MELONI, meloni_image, MELONI_PUBLISHED)
    publish(HORMUZ, hormuz_image, HORMUZ_PUBLISHED)
    sync_surfaces([MELONI, HORMUZ], "", VERSION)

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
        "news_added": [MELONI_SLUG, HORMUZ_SLUG],
        "news_updated": [],
        "change": "Pubblicate la visita di Meloni a Oslo e la rivendicazione iraniana sulla petroliera Trend a Hormuz",
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
                "last_update": "meloni-oslo-hormuz-trend-v425",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "editoriale-20260918T075000-Europe-Rome.json",
        {
            "run_at": MELONI_PUBLISHED,
            "scope": "Italia+Mondo",
            "production_branch": "main",
            "processed": [
                {
                    "title": MELONI["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "sources": [x["url"] for x in MELONI["fonti"]],
                    "public_url": f"https://curiomondo.it/notizie/{MELONI_SLUG}.html",
                },
                {
                    "title": HORMUZ["titolo"],
                    "status": "CONFERMATA DA PIÙ FONTI",
                    "decision": "publish",
                    "sources": [x["url"] for x in HORMUZ["fonti"]],
                    "public_url": f"https://curiomondo.it/notizie/{HORMUZ_SLUG}.html",
                },
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [MELONI_SLUG, HORMUZ_SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
