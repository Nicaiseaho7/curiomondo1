#!/usr/bin/env python3
"""Pubblica Buffett chairman e Giorgetti bollette (v428)."""
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

VERSION = 428
BUFFETT_PUBLISHED = "2026-09-18T14:25:00+02:00"
GIORGETTI_PUBLISHED = "2026-09-18T14:28:00+02:00"
BUFFETT_SLUG = "buffett-lascia-presidenza-berkshire-howard-18-settembre-2026"
GIORGETTI_SLUG = "giorgetti-eurogruppo-shock-energia-bollette-18-settembre-2026"


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


BUFFETT = {
    "slug": BUFFETT_SLUG,
    "titolo": "Buffett lascia la presidenza di Berkshire: Howard al posto del padre, Abel resta ceo",
    "sommario": "Il 96enne diventa chairman emeritus con effetto immediato. Resta in cda. La società vale oltre mille miliardi di dollari. I titoli sono rimasti poco mossi.",
    "categoria": "Economia",
    "luogo": "Omaha",
    "formato": "standard",
    "parole_chiave_titolo": ["Buffett", "Berkshire"],
    "dati_chiave": [
        {"icona": "◆", "valore": "96", "etichetta": "anni, compiuti il 30 agosto"},
        {"icona": "●", "valore": "1993", "etichetta": "Howard in cda da allora"},
        {"icona": "↗", "valore": ">1.000 mld $", "etichetta": "valore del conglomerato"},
    ],
    "paragrafi": [
        "Berkshire Hathaway ha detto venerdì 18 settembre che Warren Buffett lascia la presidenza del cda. Diventa chairman emeritus con effetto immediato e resta consigliere. Il figlio Howard G. Buffett, 71 anni, è il nuovo chairman. Reuters, New York Times e il comunicato Business Wire coincidono.",
        "«Father Time always wins. He has, however, been generous with me», ha scritto Buffett, 96 anni, in una lettera agli azionisti. Aveva compiuto gli anni il 30 agosto. Non è un ritiro totale: resta in board e, ha detto la società, continuerà a offrire giudizio e prospettiva.",
        "Greg Abel è già amministratore delegato dalla fine del 2025. Buffett ha scritto che Abel ha superato attese «sky-high» e che «prende da tempo le decisioni che contano». Per questo «il momento è giusto per completare la transizione». Abel ha detto che Howard sarà «il guardiano» della cultura Berkshire.",
        "Howard è in cda dal 1993, 33 anni. Buffett ha notato che è un apprendistato più lungo di quello che lui stesso fece prima di prendere il controllo a 34 anni. Non gestirà il quotidiano: il ruolo è presidiare valori e cultura, non sostituire Abel.",
        "Buffett ha presieduto il cda dal 1970. Il controllo risale al 1965, quando Berkshire era un lanificio in crisi. Oggi vale oltre mille miliardi. Geico, Burlington Northern Santa Fe, pacchetti in Apple e Coca-Cola restano i pezzi noti. Susan Decker resta lead independent director.",
        "Il New York Times indica una cassa superiore a 360 miliardi di dollari. CNN attribuisce a Bloomberg un patrimonio personale di 145 miliardi. I titoli Berkshire, secondo CNN, sono rimasti poco mossi sulla notizia. Non è un crollo né un balzo.",
        "La successione è pianificata da anni. Buffett l’aveva annunciata da ceo al meeting del maggio 2025. Il passaggio di oggi chiude la presidenza, non l’azienda. Abel ha già iniziato a usare la liquidità, anche con riacquisti di azioni.",
        "I passaggi successivi sono il primo board con Howard presidente e i conti trimestrali firmati da Abel. Fino ad allora Buffett resta il volto, non il capo operativo. Il comunicato è di Omaha, 18 settembre 2026.",
    ],
    "fonti": [
        {
            "url": "https://www.businesswire.com/news/home/20260918239653/en/Berkshire-Hathaway-Inc.-News-Release",
            "descrizione": "Business Wire — comunicato ufficiale: chairman emeritus, Howard eletto, Decker lead independent.",
        },
        {
            "url": "https://www.reuters.com/business/retail-consumer/berkshire-hathaway-names-warren-buffett-chairman-emeritus-2026-09-18/",
            "descrizione": "Reuters — lettera «Father Time always wins» e passaggio da Abel.",
        },
        {
            "url": "https://www.nytimes.com/2026/09/18/business/warren-buffett-berkshire-chairman.html",
            "descrizione": "New York Times — cassa oltre 360 miliardi e transizione pianificata.",
        },
        {
            "url": "https://www.cnn.com/2026/09/18/business/buffett-retires-as-chairman-of-berkshire-hathaway",
            "descrizione": "CNN — titoli poco mossi e patrimonio Bloomberg da 145 miliardi.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/banca-giappone-tassi-125-massimo-31-anni-18-settembre-2026.html",
            "titolo": "Banca del Giappone, tassi all’1,25%, massimo da 31 anni",
        },
        {
            "url": "/notizie/wall-street-record-speranze-accordo-iran.html",
            "titolo": "Wall Street ai record sulle speranze di un accordo con l’Iran",
        },
        {
            "url": "/notizie/usa-f35-arabia-saudita-48-caccia-24-miliardi-18-settembre-2026.html",
            "titolo": "Usa, via libera a 48 F-35 per l’Arabia Saudita",
        },
    ],
}

GIORGETTI = {
    "slug": GIORGETTI_SLUG,
    "titolo": "Giorgetti: lo shock delle guerre peserà sulle bollette. Chiesta all’Ue la deroga 0,6%",
    "sommario": "Dal Eurogruppo di Dublino il ministro dice che l’inflazione è da offerta, non da domanda. Sul bollo: coperture nazionali da risparmi Pnrr, obiettivo renderlo strutturale.",
    "categoria": "Politica",
    "luogo": "Dublino / Portofino",
    "formato": "standard",
    "parole_chiave_titolo": ["Giorgetti", "bollette"],
    "dati_chiave": [
        {"icona": "◆", "valore": "0,6%", "etichetta": "spazio fiscale energia chiesto all’Ue"},
        {"icona": "●", "valore": "~2 mld", "etichetta": "costo del taglio bollo, stima Mef"},
        {"icona": "↗", "valore": "2 guerre", "etichetta": "Ucraina e Medio Oriente citati"},
    ],
    "paragrafi": [
        "Giancarlo Giorgetti ha detto venerdì 18 settembre che «lo shock delle guerre peserà sulle bollette». Parlava in collegamento da Dublino, dopo l’Eurogruppo, ai Portofino Talks. ANSA, Repubblica e Sole 24 Ore riportano le stesse frasi. Non è un decreto sulle tariffe: è un avviso politico.",
        "All’Eurogruppo ha definito l’energia «una autentica emergenza» per competitività e conti. Ha detto di aver mandato già la lettera per la deroga al patto di stabilità sulle spese energetiche. Il tetto indicato è lo 0,6% del Pil. «Credo che la Commissione sarà aperta a concederci questo spazio».",
        "Lo 0,6% è lo stesso ordine di grandezza citato da Elly Schlein sui 14 miliardi. Giorgetti parla di procedura già avviata, non di un via libera di Bruxelles. Distinguere la lettera italiana da un’autorizzazione Ue evita di vendere come ottenuto uno spazio ancora da concedere.",
        "Sull’inflazione ha detto che deriva da uno shock di offerta, non da domanda da raffreddare. La stretta Bce «può contribuire, ma di per sé non risolve il problema». Se le due guerre continuano, l’inflazione «inesorabilmente è destinata ad aumentare». È una previsione del ministro, non un dato Istat.",
        "Ha aggiunto l’onere del debito, «salito in modo preoccupante». Il carburante è già salito per le famiglie. «In prospettiva, a breve, si rifletterà inesorabilmente sulle bollette delle famiglie e delle imprese». Non ha indicato un incremento in euro o in percentuale.",
        "Sulla Commissione e il bollo: i risparmi sui prestiti Pnrr «sono soldi nazionali, non risorse europee». Il termine per ricollocarli su altri progetti Pnrr è scaduto. Quindi, ha detto, governo e Parlamento ne dispongono. Repubblica lo colloca in risposta al faro acceso da un portavoce Ue.",
        "Giorgetti vuole il taglio del bollo «strutturale». Ha osservato che i circa 2 miliardi del bollo hanno fatto «più clamore» dei 40-50 miliardi di tagli a tasse e contributi degli anni scorsi. L’obiettivo dichiarato è chiudere la legislatura sul manifesto elettorale, con un quadro «più complicato».",
        "I passaggi successivi sono la risposta della Commissione sulla deroga 0,6% e i conti delle bollette nei prossimi mesi. Oggi c’è l’allarme del Mef, non un nuovo scostamento votato. L’Eurogruppo di Dublino è del 18 settembre 2026.",
    ],
    "fonti": [
        {
            "url": "https://www.ansa.it/sito/notizie/economia/2026/09/18/giorgetti-credo-bruxelles-aperta-a-concederci-spazio-flessibilita-energia_523a71b4-ee25-44e2-9894-a264fb7afea2.html",
            "descrizione": "ANSA — lettera per la deroga 0,6% e shock energetico su carburanti e bollette.",
        },
        {
            "url": "https://www.repubblica.it/economia/2026/09/18/news/giorgetti_guerre_energia_bollette_eurogruppo_tassi_bce-425593064/",
            "descrizione": "la Repubblica — coperture bollo da risparmi Pnrr nazionali e avviso sulle bollette.",
        },
        {
            "url": "https://www.ilsole24ore.com/art/giorgetti-eurogruppo-richiamato-emergenza-energia-e-aumento-tassi-debito-AJKO4EHB",
            "descrizione": "Il Sole 24 Ore — inflazione da offerta e onere del debito in salita.",
        },
        {
            "url": "https://www.ilsole24ore.com/art/giorgetti-taglio-bollo-auto-ha-fatto-piu-clamore-che-40-50-mld-riduzione-tasse-AJCsqFHB",
            "descrizione": "Il Sole 24 Ore — bollo da circa 2 miliardi e obiettivo di renderlo strutturale.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html",
            "titolo": "Bollo auto, esenzione per 14,5 milioni di veicoli",
        },
        {
            "url": "/notizie/schlein-lettera-meloni-14-miliardi-energia-conte-17-settembre-2026.html",
            "titolo": "Schlein propone a Meloni 14 miliardi per clima ed energia",
        },
        {
            "url": "/notizie/salvini-rinvio-blocco-diesel-euro-5-2027-18-settembre-2026.html",
            "titolo": "Diesel Euro 5, Salvini annuncia il rinvio al 2027",
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
    buffett_image = {
        "key": f"{BUFFETT_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "buffett-v428.jpg", f"{BUFFETT_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Warren Buffett riconoscibile a una scrivania; somiglianza sintetica, non una fotografia documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": "Photorealistic editorial photograph of Warren Buffett at a desk, ordinary contextual portrait, no text.",
    }
    giorgetti_image = {
        "key": f"{GIORGETTI_SLUG}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(
            ROOT / "generated_images" / "giorgetti-v428.jpg", f"{GIORGETTI_SLUG}-v{VERSION}"
        ),
        "alt": "Scena editoriale contestuale generata con IA: Giancarlo Giorgetti riconoscibile in un interno istituzionale; somiglianza sintetica, non una fotografia documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "syntheticLikeness": "public-figure",
        "prompt": "Photorealistic editorial photograph of Giancarlo Giorgetti in an institutional interior, no text.",
    }

    publish(BUFFETT, buffett_image, BUFFETT_PUBLISHED, "UFFICIALE")
    publish(GIORGETTI, giorgetti_image, GIORGETTI_PUBLISHED, "UFFICIALE")
    sync_surfaces([BUFFETT, GIORGETTI], "", VERSION)

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
        "news_added": [BUFFETT_SLUG, GIORGETTI_SLUG],
        "news_updated": [],
        "change": "Pubblicati il passaggio di presidenza Berkshire e l’allarme di Giorgetti sulle bollette",
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
                "last_update": "buffett-giorgetti-v428",
            }
        )
        write_json(path, state)

    write_json(
        ROOT / "automation" / "logs" / "editoriale-20260918T142800-Europe-Rome.json",
        {
            "run_at": GIORGETTI_PUBLISHED,
            "scope": "Economia+Politica",
            "production_branch": "main",
            "processed": [
                {
                    "title": BUFFETT["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "public_url": f"https://curiomondo.it/notizie/{BUFFETT_SLUG}.html",
                },
                {
                    "title": GIORGETTI["titolo"],
                    "status": "UFFICIALE",
                    "decision": "publish",
                    "public_url": f"https://curiomondo.it/notizie/{GIORGETTI_SLUG}.html",
                },
            ],
            "publication": {"site_version": VERSION, "state": "pending_deploy"},
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [BUFFETT_SLUG, GIORGETTI_SLUG]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
