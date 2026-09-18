#!/usr/bin/env python3
"""Pubblica convocati Mancini e ticket sanitari (v436)."""
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

VERSION = 436


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


def persist(article: dict, image: dict, published: str, public_figure: bool = False) -> str:
    slug = write_article(article, image, VERSION)
    stamp_dates(slug, published)
    article["published"] = published
    if public_figure:
        p = ROOT / "notizie" / f"{slug}.html"
        html = p.read_text(encoding="utf-8")
        html = html.replace(
            '<figure class="article-image" data-ai-generated="true">',
            '<figure class="article-image" data-ai-generated="true" data-synthetic-likeness="public-figure" data-sensitive-context="false">',
        )
        p.write_text(html, encoding="utf-8")
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


MANCINI = {
    "slug": "convocati-italia-mancini-nations-league-34-nomi-18-settembre-2026",
    "titolo": "Mancini convoca 34 azzurri: 9 esordienti, tornano Zaniolo e Maldini",
    "sommario": "Lista FIGC per la Nations League. Raduno domenica a Coverciano. Si comincia il 25 all’Olimpico contro il Belgio.",
    "categoria": "Sport",
    "luogo": "Coverciano",
    "formato": "standard",
    "stato": "UFFICIALE",
    "parole_chiave_titolo": ["Mancini", "convocati"],
    "dati_chiave": [
        {"icona": "◆", "valore": "34", "etichetta": "convocati per quattro gare in 11 giorni"},
        {"icona": "●", "valore": "9", "etichetta": "prime chiamate, tra cui Pessina e Vergara"},
        {"icona": "↗", "valore": "25/09", "etichetta": "Italia-Belgio all’Olimpico"},
    ],
    "paragrafi": [
        "Roberto Mancini ha diramato la prima lista da commissario tecnico di ritorno. Sono 34 convocati per la Nations League. Lo comunica la FIGC il 18 settembre. Nove volti nuovi: Massimo Pessina (Bologna), Daniele Ghilardi (Roma), Michael Kayode (Brentford), Eddy Kouadio (Monza), Issa Doumbia (Sporting), Alessandro Romano (Cagliari), Sebastiano Esposito (Sassuolo), Antonio Vergara (Napoli) e Mohamed Alì Zoma (Norimberga).",
        "Tornano Nicolò Zaniolo (Udinese) e Daniel Maldini (Cagliari). C’è anche Nicolò Fagioli (Fiorentina). Il raduno è domenica sera a Coverciano. Quattro partite in undici giorni: 25 settembre Italia-Belgio all’Olimpico, 28 Turchia a Bursa, 2 ottobre Francia a Parigi, 5 ottobre Turchia a Bologna.",
        "I portieri sono quattro: Carnesecchi, Donnarumma, Pessina e Vicario. In difesa restano i punti fermi Bastoni, Calafiori, Di Lorenzo, Dimarco, Gianluca Mancini e Scalvini, con Ahanor e Coppola. Kayode e Kouadio arrivano alla prima chiamata. Ghilardi è la novità romanista.",
        "A centrocampo: Barella, Cristante, Doumbia, Fagioli, Frattesi, Mandragora, Romano, Tonali. In attacco: Cambiaghi, Pio Esposito, Sebastiano Esposito, Inacio, Kean, Maldini, Raspadori, Scamacca, Vergara, Zaniolo, Zoma. La lista è allargata proprio per il turnover: non è la formazione del 25.",
        "Mancini non ha indicato titolari. Repubblica segnala Diana Bianchedi come capo delegazione. La FIGC è la fonte primaria; Il Fatto e Il Mattino pubblicano lo stesso elenco di 34 nomi. Non confondere questa lista con vecchie convocazioni di Gattuso.",
        "Il numero 34 serve a coprire Belgio, doppia Turchia e Francia senza svuotare i club tra una gara e l’altra. Non è una rosa da tenere ferma per tutte e quattro le partite.",
        "Kean è al Como, Donnarumma al Manchester City, Tonali al Tottenham, Calafiori all’Arsenal. I club esteri sono parte della lista, non un’eccezione. Chi non è scritto sopra non è convocato.",
        "L’elenco è quello comunicato dalla FIGC il 18 settembre. Il raduno è previsto domenica sera a Coverciano. Mancini non ha indicato i titolari per Italia-Belgio.",
    ],
    "fonti": [
        {
            "url": "https://www.figc.it/it/nazionali/azzurri/nazionale-a",
            "descrizione": "FIGC — 34 convocati, 9 volti nuovi, raduno a Coverciano, 18 settembre 2026.",
        },
        {
            "url": "https://www.ilfattoquotidiano.it/2026/09/18/convocati-italia-nations-league-mancini-lista-ufficiale-nomi/8510718/",
            "descrizione": "Il Fatto Quotidiano — elenco completo dei 34 convocati.",
        },
        {
            "url": "https://www.repubblica.it/sport/calcio/nazionale/2026/09/18/news/mancini_convocazioni_daniel_maldini_zaniolo_fagioli_nazionale-425593779/",
            "descrizione": "la Repubblica — Zaniolo, Maldini, nove esordienti.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/serie-a-quinta-giornata-orari-tv-monza-sassuolo-roma-inter-18-settembre-2026.html",
            "titolo": "Serie A, quinta giornata: orari e tv",
        },
        {
            "url": "/notizie/sinner-us-open-ritiro-ginocchio-2026.html",
            "titolo": "Sinner rinuncia agli US Open per il ginocchio",
        },
        {
            "url": "/notizie/kimi-antonelli-vince-gp-italia-monza-19esimo-6-settembre-2026.html",
            "titolo": "Antonelli vince il GP d’Italia a Monza",
        },
    ],
}

TICKET = {
    "slug": "aumento-ticket-sanitari-21-settembre-2026-tariffario-visite",
    "titolo": "Ticket sanitari, dal 21 settembre il nuovo tariffario: +5,8% medio",
    "sommario": "448 prestazioni di specialistica e 222 codici di protesica. Tetto 36,15 euro a ricetta in molte Regioni. Non tutte le visite costano di più al paziente.",
    "categoria": "Economia",
    "luogo": "Italia",
    "formato": "standard",
    "stato": "CONFERMATA DA PIÙ FONTI",
    "parole_chiave_titolo": ["ticket sanitari", "tariffe"],
    "dati_chiave": [
        {"icona": "◆", "valore": "21/09", "etichetta": "entrata in vigore del nuovo tariffario"},
        {"icona": "●", "valore": "+5,8%", "etichetta": "aumento medio delle tariffe riviste"},
        {"icona": "↗", "valore": "36,15 €", "etichetta": "tetto ticket ordinario a ricetta in molte Regioni"},
    ],
    "paragrafi": [
        "Dal lunedì 21 settembre 2026 scatta il nuovo tariffario nazionale per una parte delle prestazioni del Servizio sanitario. Riguarda 448 voci di specialistica ambulatoriale e 222 codici di assistenza protesica. L’intesa è della Conferenza Stato-Regioni del 23 luglio. Sostituisce il decreto del 25 novembre 2024, annullato dal Tar del Lazio.",
        "L’aumento medio delle tariffe toccate è circa il 5,8%. Impatto stimato: 210,7 milioni l’anno, di cui 183,1 sulla specialistica. Si aggiungono ai circa 550 milioni già previsti per il decreto 2024. Otto prestazioni su dieci, scrive il Corriere, non cambiano prezzo.",
        "Molte prime visite passano da 25 a 26 euro: neurologia, ginecologia, ortopedia, pneumologia, endocrinologia, gastroenterologia. La prima visita cardiologica con ECG va da 33,60 a 38 euro. Agoaspirato della mammella: da 31,25 a 36,50.",
        "Il rincaro della tariffa non è il ticket pagato dal paziente. In molte Regioni il tetto ordinario resta 36,15 euro a ricetta. Chi è esente non paga. Chi ha già prenotato prima del 21 settembre va verificato in Regione: le prestazioni fino al 20 restano sul vecchio nomenclatore.",
        "Il decreto rimborsa le strutture accreditate, non «alza il ticket» in blocco. Sky TG24, Corriere, Il Fatto e Quotidiano Sanità allineano i numeri. Manca, al momento della verifica, il PDF unico in evidenza su salute.gov.it: restiamo sulle conferme incrociate e sull’intesa del 23 luglio.",
        "Il provvedimento riguarda il rimborso delle strutture accreditate. Le esenzioni per reddito, patologia o invalidità restano quelle già previste dalle Regioni e non sono toccate da questo tariffario.",
        "Fonti: Quotidiano Sanità (intesa 23 luglio), Il Sole 24 Ore, Sky TG24 e Corriere del 18 settembre. 18 settembre 2026, ore 21.52 Europe/Rome.",
        "Le prestazioni erogate fino al 20 settembre restano sul nomenclatore precedente. Dal 21 settembre le strutture accreditate applicano le nuove tariffe. Le esenzioni già riconosciute restano valide e non vanno chieste di nuovo solo per il cambio di tariffario.",
    ],
    "fonti": [
        {
            "url": "https://www.quotidianosanita.it/governo-e-parlamento/lea-c-l-ok-della-stato-regioni-al-nuovo-decreto-con-le-tariffe-per-specialistica-ambulatoriale-e-protesica-impatto-da-210-milioni-di-euro/",
            "descrizione": "Quotidiano Sanità — intesa Stato-Regioni 23 luglio 2026, in vigore 21 settembre.",
        },
        {
            "url": "https://tg24.sky.it/economia/2026/09/18/aumento-ticket-sanitari-prezzi",
            "descrizione": "Sky TG24 — elenco aumenti e tetto 36,15 euro.",
        },
        {
            "url": "https://www.corriere.it/economia/consumi/26_settembre_18/visite-specialistiche-scattano-gli-aumenti-del-ticket-dal-21-settembre-via-al-nuovo-tariffario-d33b3e68-05a7-4611-9500-e8587ab35xlk.shtml",
            "descrizione": "Corriere — 448+222 prestazioni, +5,8%, otto su dieci invariate.",
        },
        {
            "url": "https://en.ilsole24ore.com/art/healthcare-new-charges-for-consultations-and-tests-to-be-introduced-in-september-AJOR1iT",
            "descrizione": "Il Sole 24 Ore — decreto 23 luglio, 210,7 milioni a regime.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/tari-dichiarazione-90-giorni-decreto-147-imu-sanzioni-18-settembre-2026.html",
            "titolo": "TARI, dichiarazione entro 90 giorni: decreto 147",
        },
        {
            "url": "/notizie/giorgetti-eurogruppo-shock-energia-bollette-18-settembre-2026.html",
            "titolo": "Giorgetti all’Eurogruppo: shock energia e bollette",
        },
        {
            "url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html",
            "titolo": "Bollo auto, esenzione 2027 fino a 80 kW",
        },
    ],
}


def main() -> None:
    img_m = {
        "key": f"{MANCINI['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "syntheticLikeness": "public-figure",
        "variants": save_image_variants(ROOT / "generated_images" / "mancini-v436.jpg", f"{MANCINI['slug']}-v{VERSION}"),
        "alt": "Scena editoriale contestuale generata con IA: Roberto Mancini riconoscibile in tuta azzurra su un campo di allenamento; somiglianza sintetica, non è una fotografia documentaria del raduno.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-photorealistic Roberto Mancini, Italy tracksuit, training pitch, no text.",
    }
    img_t = {
        "key": f"{TICKET['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(ROOT / "generated_images" / "ticket-v436.jpg", f"{TICKET['slug']}-v{VERSION}"),
        "alt": "Scena editoriale contestuale generata con IA: sala d’attesa di un ambulatorio italiano, tessera sanitaria e dispensatore di numeri; non è una fotografia documentaria di una ASL specifica.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Photorealistic Italian public clinic waiting room, health cards, no gore, no text.",
    }
    slug_m = persist(MANCINI, img_m, "2026-09-18T21:50:00+02:00", public_figure=True)
    slug_t = persist(TICKET, img_t, "2026-09-18T21:52:00+02:00")
    sync_surfaces([TICKET, MANCINI], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-18",
        "type": "content-release",
        "news_added": [slug_m, slug_t],
        "news_updated": [],
        "change": "Pubblicati convocati Mancini e nuovo tariffario ticket dal 21 settembre",
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
                "last_update": "mancini-ticket-v436",
            }
        )
        write_json(path, state)
    write_json(
        ROOT / "automation" / "logs" / "scoop-20260918T215000-Europe-Rome.json",
        {
            "run_at": "2026-09-18T21:50:00+02:00",
            "skill": "ultime-notizie-scoop",
            "desks": ["ricerche-google-italia"],
            "processed": [
                {"title": MANCINI["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_m}.html"},
                {"title": TICKET["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_t}.html"},
            ],
            "discarded": [
                {"topic": "perth squalo", "reason": "già pubblicato oggi"},
                {"topic": "tassa rifiuti TARI IMU", "reason": "già pubblicato oggi"},
                {"topic": "accise diesel", "reason": "articoli esistenti, niente nuovo prezzo ufficiale di oggi"},
                {"topic": "eurofighter", "reason": "già coperto scramble Lituania"},
                {"topic": "barbara d'urso", "reason": "gossip, niente Rai"},
                {"topic": "chanel totti", "reason": "Verissimo/gossip"},
                {"topic": "ranucci boccia", "reason": "smentita di una foto, non fatto verificabile oltre la querela"},
                {"topic": "freddo settembre", "reason": "PC: temperature nessun fenomeno significativo"},
                {"topic": "bonus trasporti 2027", "reason": "decreto attuativo atteso marzo 2027, misura non operativa"},
                {"topic": "bonus ristrutturazioni 2027", "reason": "norma già nota, non breaking di oggi"},
                {"topic": "de rossi genoa", "reason": "conferenza, impatto sotto i convocati FIGC"},
                {"topic": "pignoramento / università / sagre / bruzzone", "reason": "evergreen o senza primaria del giorno"},
            ],
        },
    )
    print(json.dumps({"status": "ok", "version": VERSION, "added": [slug_m, slug_t]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
