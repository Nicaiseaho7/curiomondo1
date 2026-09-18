#!/usr/bin/env python3
"""Pubblica Euro 5 Salvini, sciopero Apple e no della Corea all'Iran (v427)."""
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

VERSION = 427
SALVINI_PUBLISHED = "2026-09-18T12:40:00+02:00"
APPLE_PUBLISHED = "2026-09-18T12:36:00+02:00"
COREA_PUBLISHED = "2026-09-18T12:32:00+02:00"

SALVINI_SLUG = "salvini-rinvio-blocco-diesel-euro-5-2027-18-settembre-2026"
APPLE_SLUG = "sciopero-apple-store-italia-iphone-18-pro-18-settembre-2026"
COREA_SLUG = "corea-sud-lee-niente-truppe-guerra-iran-18-settembre-2026"


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


SALVINI = {
    "slug": SALVINI_SLUG,
    "titolo": "Diesel Euro 5, Salvini: nel prossimo Cdm un decreto per rinviare lo stop al 2027",
    "sommario": "Il vicepremier lo ha detto a Mattino 5. Il blocco scatterebbe dal 1° ottobre in comuni sopra i 100mila abitanti. Il rinvio non è ancora legge.",
    "categoria": "Politica",
    "luogo": "Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["Salvini", "Euro 5"],
    "dati_chiave": [
        {"icona": "◆", "valore": "1/10", "etichetta": "data prevista dello stop auto"},
        {"icona": "●", "valore": "2027", "etichetta": "orizzonte indicato da Salvini"},
        {"icona": "↗", "valore": "4", "etichetta": "regioni del decreto 121/2023"},
    ],
    "paragrafi": [
        "Matteo Salvini ha detto venerdì 18 settembre che porterà al prossimo Consiglio dei ministri un decreto con il rinvio dello stop alle diesel Euro 5. L’annuncio è a Mattino 5. ANSA, Sky TG24 e Open coincidono sul punto: il testo non è ancora approvato.",
        "«Nel prossimo Consiglio dei ministri personalmente porto un decreto all’interno del quale c’è anche il rinvio di questo stop insensato», ha detto il vicepremier. La norma, ha aggiunto, deve «dare ossigeno» per tutto il 2027.",
        "Lo stop deriva dal decreto-legge 121 del 2023, dopo sentenze della Corte di giustizia Ue sulla qualità dell’aria. Riguarda Piemonte, Lombardia, Veneto ed Emilia-Romagna. Today.it precisa che le altre tre regioni avevano già aggirato il divieto; restava la Lombardia.",
        "Le limitazioni per le autovetture dovrebbero partire dal 1° ottobre 2026 nei comuni sopra i 100mila abitanti. Per altre categorie di veicoli le scadenze indicate arrivano al 2027 e al 2028. Salvini parla di «centinaia di migliaia» di persone.",
        "Open stima oltre tre milioni di veicoli coinvolti. È una cifra di testata, non un dato ministeriale nel comunicato. Il rinvio, se approvato, coprirebbe l’incertezza fino a tutto il 2027, non cancella lo stop in via definitiva.",
        "Salvini ha attaccato «l’ideologia pseudo-green di Bruxelles». È una valutazione politica, non un fatto. Sky TG24 gli attribuisce anche: se l’Ue «continua», «il governo italiano si mette di traverso».",
        "Il Cdm non ha ancora votato. Finché manca il testo in Gazzetta, lo stop del 1° ottobre resta il quadro vigente nelle aree non coperte da deroghe regionali. I sindaci e le prefetture attendono l’atto, non l’intervista.",
        "I passaggi successivi sono la data del Consiglio dei ministri, il testo del decreto e l’eventuale conversione. Distinguere l’annuncio televisivo dalla norma approvata evita di presentare come già deciso un rinvio ancora politico.",
    ],
    "fonti": [
        {
            "url": "https://www.ansa.it/sito/notizie/economia/2026/09/18/salvini-in-prossimo-cdm-decreto-per-altro-rinvio-a-stop-diesel-euro_c49dbc6e-0172-4eee-9014-e064e04eeb7d.html",
            "descrizione": "ANSA — Salvini a Mattino 5: decreto al prossimo Cdm e rinvio per il 2027.",
        },
        {
            "url": "https://tg24.sky.it/politica/2026/09/18/blocco-diesel-euro-5-proroga-salvini",
            "descrizione": "Sky TG24 — obiettivo 2027 e frasi su Bruxelles.",
        },
        {
            "url": "https://www.open.online/2026/09/18/blocco-diesel-euro-5-salvini-rinvio/",
            "descrizione": "Open — quattro regioni, comuni over 100mila e stima sui veicoli.",
        },
        {
            "url": "https://www.today.it/motori/news/blocco-auto-diesel-euro5-decreto-salvini-2027.html",
            "descrizione": "Today — solo la Lombardia senza aggiramento regionale del divieto.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html",
            "titolo": "Bollo auto, esenzione per 14,5 milioni di veicoli",
        },
        {
            "url": "/notizie/diesel-sconto-accise-proroga-17-settembre-2026.html",
            "titolo": "Diesel, prorogato lo sconto sulle accise",
        },
        {
            "url": "/notizie/schlein-lettera-meloni-14-miliardi-energia-conte-17-settembre-2026.html",
            "titolo": "Schlein propone a Meloni 14 miliardi per clima ed energia",
        },
    ],
}

APPLE = {
    "slug": APPLE_SLUG,
    "titolo": "Sciopero Apple in Italia nel giorno dell’iPhone 18 Pro: 1.600 addetti, i negozi restano aperti",
    "sommario": "Filcams, Fisascat e Uiltucs fermano l’intero turno nei 17 store. L’azienda dice che vendita e online funzionano. I sindacati chiedono assunzioni e stabilizzazioni.",
    "categoria": "Italia",
    "luogo": "Milano / Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["Apple", "iPhone"],
    "dati_chiave": [
        {"icona": "◆", "valore": "1.600", "etichetta": "addetti coinvolti, stima Cisl"},
        {"icona": "●", "valore": "17", "etichetta": "Apple Store in Italia"},
        {"icona": "↗", "valore": "1.489 €", "etichetta": "prezzo di partenza iPhone 18 Pro"},
    ],
    "paragrafi": [
        "I dipendenti degli Apple Store italiani scioperano venerdì 18 settembre, giorno del lancio dell’iPhone 18 Pro. Filcams Cgil, Fisascat Cisl e Uiltucs hanno proclamato l’intero turno. Reuters e LaPresse confermano presidi a Milano e in altre città.",
        "Fisascat Cisl indica più di 1.600 addetti in 17 negozi. A Milano il presidio è in piazza Liberty. A Roma è previsto in piazza Capranica, a Torino in via Roma 82. Sky TG24 aveva anticipato la proclamazione il 17 settembre.",
        "I sindacati chiedono più assunzioni, la stabilizzazione di una parte dei contratti a termine e più ore per chi è part-time. Dicono di carichi in aumento e organici insufficienti. Sono rivendicazioni, non un accertamento ispettivo.",
        "Apple, tramite un portavoce citato da Reuters, ha detto che i negozi e lo store online «sono aperti oggi». L’azienda si dice «orgogliosa» di retribuzioni e benefit, inclusi copertura sanitaria e supporto psicologico. Non risulta una risposta puntuale sulle assunzioni.",
        "In Italia l’iPhone 18 Pro parte da 1.489 euro, secondo il listino Apple riportato da Reuters. Il pieghevole Duo, presentato la scorsa settimana, è atteso il 23 ottobre. Lo sciopero cade sul giorno di vendita, non sulla presentazione.",
        "HdBlog segnala che Apple non ha comunicato cancellazioni dei ritiri prenotati. Consiglia di aspettare la notifica di ordine pronto. Orari ridotti e servizi non disponibili restano possibili, secondo le pagine dei negozi.",
        "La vertenza, secondo i sindacati, segue l’integrativo del 2024 e assemblee del 7 settembre. Ad agosto i buoni pasto sono saliti a 10 euro: le sigle li hanno accolti, ma li tengono distinti da organici e ritmi.",
        "Il fatto di oggi è lo sciopero e la replica aziendale sulla continuità di vendita. Non è ancora un accordo. I prossimi passi sono l’affluenza reale, l’effetto sugli store e un eventuale tavolo su assunzioni e contratti.",
    ],
    "fonti": [
        {
            "url": "https://www.reuters.com/business/retail-consumer/italian-apple-store-employees-strike-iphone18-pro-launch-day-2026-09-18/",
            "descrizione": "Reuters — 1.600 addetti, 17 store, prezzo 1.489 euro e replica Apple.",
        },
        {
            "url": "https://www.lapresse.it/economia/2026/09/18/sciopero-dipendenti-apple-nel-giorno-degli-iphone-18-pro-la-protesta-a-milano/",
            "descrizione": "LaPresse — presidio in piazza Liberty a Milano nel giorno del lancio.",
        },
        {
            "url": "https://tg24.sky.it/cronaca/2026/09/17/sciopero-apple-18-settembre-uscita-iphone-18",
            "descrizione": "Sky TG24 — proclamazione Filcams, Fisascat e Uiltucs e assemblee del 7 settembre.",
        },
        {
            "url": "https://www.hdblog.it/smartphone/articoli/n670787/apple-store-confermato-sciopero-domani/",
            "descrizione": "HdBlog — presidi a Roma, Milano, Torino e ritiri prenotati non cancellati.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/electrolux-sciopero-15-settembre-esuberi-chiusura-cerreto-desi-2026.html",
            "titolo": "Electrolux, sciopero contro esuberi e chiusura",
        },
        {
            "url": "/notizie/medici-famiglia-sciopero-oggi-cosa-resta-garantito-16-settembre-2026.html",
            "titolo": "Sciopero dei medici di famiglia: cosa resta garantito",
        },
        {
            "url": "/notizie/apple-event-9-settembre-iphone-fold-cosa-aspettarsi.html",
            "titolo": "Evento Apple, iPhone e pieghevole: cosa aspettarsi",
        },
    ],
}

COREA = {
    "slug": COREA_SLUG,
    "titolo": "Corea del Sud, Lee: nessuna truppa nella guerra in Iran. Si valuta solo la scorta alle navi",
    "sommario": "Il presidente esclude dispiegamenti che coinvolgano Seul nel conflitto. Resta aperta un’estensione della missione anti-pirateria Cheonghae per proteggere i mercantili coreani.",
    "categoria": "Mondo",
    "luogo": "Seul",
    "formato": "standard",
    "parole_chiave_titolo": ["Lee", "Iran"],
    "dati_chiave": [
        {"icona": "◆", "valore": "0", "etichetta": "truppe in guerra, detto da Lee"},
        {"icona": "●", "valore": "Cheonghae", "etichetta": "unità già al largo della Somalia"},
        {"icona": "↗", "valore": "Hormuz", "etichetta": "rotta energetica sotto esame"},
    ],
    "paragrafi": [
        "Il presidente sudcoreano Lee Jae Myung ha detto venerdì 18 settembre che Seul non invierà truppe né mezzi militari per entrare nella guerra tra Stati Uniti e Iran. Lo ha detto in conferenza stampa a Cheong Wa Dae. Reuters, New York Times e Guardian riportano la stessa linea.",
        "«Non ci sarà un dispiegamento che coinvolga o intervenga nella guerra. Posso dirlo con chiarezza», ha detto Lee. Ha ripetuto il principio di non coinvolgimento. Non è un voto parlamentare: è una dichiarazione del capo dello Stato.",
        "Lee ha tenuto distinta la guerra dalla protezione delle navi coreane. Ha detto che il Paese deve fare «il minimo» che fanno altri per scortare petrolio, mercantili e connazionali. Questa parte resta in valutazione, non è un ordine di missione già firmato.",
        "Seul esamina un’estensione della Cheonghae Unit, già al largo della Somalia per l’anti-pirateria. Un cacciatorpediniere e navi di supporto potrebbero avvicinarsi al Mar Rosso o a Hormuz, ha detto Lee. L’incarico sarebbe solo la scorta, non il sostegno alla guerra.",
        "Donald Trump, secondo il New York Times, a agosto gli aveva chiesto «un piccolo aiuto», ricordando la presenza militare Usa in Corea. Washington non ha specificato in pubblico quale contributo pretenda. Quest’estate ha ridotto le esercitazioni congiunte.",
        "In Corea l’ipotesi Hormuz è impopolare. Il Guardian cita proteste a Seul contro un eventuale invio. Lee risponde alla pressione interna e a quella americana nello stesso passaggio, senza chiudere la scorta civile-commerciale.",
        "La differenza è operativa. Un’unità anti-pirateria che scorta petroliere coreane non equivale a un contingente sotto comando di guerra. Lee ha detto che non metterà militari sotto comando straniero in modo da esporli al conflitto.",
        "I passaggi successivi sono un eventuale mandato formale alla Cheonghae e la reazione di Washington. Fino ad allora vale l’esclusione della guerra, non un nuovo schieramento a Hormuz. Reuters colloca l’annuncio al 18 settembre, ora di Seul.",
    ],
    "fonti": [
        {
            "url": "https://www.reuters.com/world/asia-pacific/south-koreas-lee-says-will-not-deploy-military-get-involved-middle-east-conflict-2026-09-18/",
            "descrizione": "Reuters — Lee esclude mezzi che trascinino Seul nel conflitto e valuta Hormuz.",
        },
        {
            "url": "https://www.nytimes.com/2026/09/18/world/asia/south-korea-president-lee-jae-myung-trump-iran.html",
            "descrizione": "New York Times — no a truppe e assetti di guerra; Cheonghae e richiesta di Trump.",
        },
        {
            "url": "https://www.theguardian.com/world/2026/sep/18/south-korea-will-not-send-military-to-support-us-war-on-iran-defying-trump-pressure",
            "descrizione": "The Guardian — conferenza stampa e proteste interne contro l’invio.",
        },
        {
            "url": "https://www.koreatimes.co.kr/southkorea/politics/20260918/lee-rules-out-korean-troop-deployment-in-iran-war",
            "descrizione": "Korea Times — testo della conferenza a Cheong Wa Dae e principio di non intervento.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/corea-sud-misure-militari-hormuz-navigazione-4-settembre-2026.html",
            "titolo": "Corea del Sud, misure militari per la navigazione a Hormuz",
        },
        {
            "url": "/notizie/hormuz-pasdaran-petroliera-trend-togo-17-settembre-2026.html",
            "titolo": "Hormuz, i pasdaran dicono di aver colpito la petroliera Trend",
        },
        {
            "url": "/notizie/bab-el-mandeb-crosetto-missione-navale-mercantili-italiani-17-settembre-2026.html",
            "titolo": "Bab el-Mandeb, Crosetto attiva la Marina per i mercantili italiani",
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
    salvini_image = {
        "key": f"{SALVINI_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "salvini-v427.jpg", f"{SALVINI_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Matteo Salvini riconoscibile all’aperto a Roma; somiglianza sintetica, non una fotografia documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": "Photorealistic editorial photograph of Matteo Salvini in Rome, ordinary contextual political scene, no text.",
    }
    apple_image = {
        "key": f"{APPLE_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "apple-sciopero-v427.jpg", f"{APPLE_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: presidio di lavoratori davanti a un Apple Store in una piazza italiana; non è una fotografia documentaria dello sciopero.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Photorealistic picket outside an Apple Store on a European square, blank signs, no text in pixels.",
    }
    corea_image = {
        "key": f"{COREA_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "lee-corea-v427.jpg", f"{COREA_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Lee Jae Myung riconoscibile a un podio con bandiere sudcoreane; somiglianza sintetica, non una fotografia documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": "Photorealistic editorial photograph of Lee Jae Myung at a press-conference lectern, no text.",
    }

    publish(SALVINI, salvini_image, SALVINI_PUBLISHED, "UFFICIALE")
    publish(APPLE, apple_image, APPLE_PUBLISHED, "CONFERMATA DA PIÙ FONTI")
    publish(COREA, corea_image, COREA_PUBLISHED, "UFFICIALE")
    sync_surfaces([SALVINI, APPLE, COREA], "", VERSION)

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
        "news_added": [SALVINI_SLUG, APPLE_SLUG, COREA_SLUG],
        "news_updated": [],
        "change": "Pubblicati rinvio Euro 5, sciopero Apple e no sudcoreano alla guerra in Iran",
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
                "articleCount": int(state.get("articleCount", 0)) + 3,
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 3,
                "last_update": "euro5-apple-corea-v427",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "editoriale-20260918T124000-Europe-Rome.json",
        {
            "run_at": SALVINI_PUBLISHED,
            "scope": "Politica+Italia+Mondo",
            "production_branch": "main",
            "processed": [
                {
                    "title": SALVINI["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "public_url": f"https://curiomondo.it/notizie/{SALVINI_SLUG}.html",
                },
                {
                    "title": APPLE["titolo"],
                    "status": "CONFERMATA DA PIÙ FONTI",
                    "decision": "publish",
                    "public_url": f"https://curiomondo.it/notizie/{APPLE_SLUG}.html",
                },
                {
                    "title": COREA["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "public_url": f"https://curiomondo.it/notizie/{COREA_SLUG}.html",
                },
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [SALVINI_SLUG, APPLE_SLUG, COREA_SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
