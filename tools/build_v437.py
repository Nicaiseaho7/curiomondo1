#!/usr/bin/env python3
"""Pubblica Monza-Sassuolo 2-1, pacchetto cooperazione 260 mln, Di Liegro."""
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

VERSION = 437


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


def assert_body(article: dict) -> None:
    paras = article["paragrafi"]
    words = sum(len(p.split()) for p in paras)
    fmt = article["formato"]
    ranges = {"flash": (100, 250), "standard": (300, 600), "feature": (800, 1500)}
    lo, hi = ranges[fmt]
    if not lo <= words <= hi:
        raise SystemExit(f"{article['slug']} {fmt} {words} parole")
    for i, p in enumerate(paras, 1):
        n = len(p.split())
        if n > 60:
            raise SystemExit(f"{article['slug']} p{i} {n} parole")


MONZA = {
    "slug": "monza-sassuolo-2-1-varela-juric-prima-vittoria-18-settembre-2026",
    "titolo": "Monza-Sassuolo 2-1: doppio Varela, prima vittoria per Juric",
    "sommario": "Testa e rigore del portoghese nel secondo tempo. Adzic accorcia su punizione. Primo successo in campionato per i brianzoli.",
    "categoria": "Sport",
    "luogo": "Monza",
    "formato": "standard",
    "stato": "CONFERMATA DA PIÙ FONTI",
    "parole_chiave_titolo": ["Monza", "Sassuolo"],
    "dati_chiave": [
        {"icona": "◆", "valore": "2-1", "etichetta": "risultato finale all’U-Power Stadium"},
        {"icona": "●", "valore": "2", "etichetta": "gol di Gustavo Varela (51’ e 63’ rigore)"},
        {"icona": "↗", "valore": "1ª", "etichetta": "vittoria in campionato per Juric"},
    ],
    "paragrafi": [
        "Il Monza ha battuto il Sassuolo 2-1 nell’anticipo della quinta giornata di Serie A. La gara si è disputata venerdì 18 settembre all’U-Power Stadium, con inizio alle 20.45. È la prima vittoria in campionato per Ivan Juric.",
        "Gustavo Varela ha realizzato entrambi i gol dei padroni di casa nel secondo tempo. Al 51’ ha segnato di testa su corner di Samuele Birindelli, con Muric rimasto sulla linea. Al 63’ ha trasformato un rigore concesso per un fallo di Sebastiano Esposito su Dany Mota.",
        "Vasilije Adzic ha accorciato all’88’ su calcio di punizione. Nel recupero Kieron Bowie ha colpito un palo. Il primo tempo si era chiuso senza reti. Ha diretto Daniele Perenzoni. La gara è finita dopo sei minuti di recupero.",
        "Prima di questa gara il Monza aveva tre sconfitte e un pari in quattro giornate. Con i tre punti sale a quattro in classifica. È la quarta vittoria in cinque gare di Serie A contro il Sassuolo. I neroverdi di Alberto Aquilani arrivano al secondo ko in campionato.",
        "Varela è al quarto gol in cinque partite di Serie A. Tra i pali dei brianzoli ha giocato Noel Tornqvist, terzo portiere impiegato dal Monza in cinque giornate. Dany Mota, subentrato, ha ottenuto il rigore; Esposito è rimasto in campo.",
        "Adzic, entrato dalla panchina, ha segnato per la terza gara consecutiva, dopo il gol alla Juventus. Aquilani ha chiuso con un 4-2-4 per recuperare dopo il doppio vantaggio del Monza.",
        "Il Sassuolo ha avuto più possesso, 63% contro 37%, e più tiri in porta, 8 a 7. Eddy Kouadio è stato ammonito nel primo tempo. Birindelli, autore dell’assist del 51’, ha visto il giallo nel finale.",
        "La quinta giornata prosegue sabato alle 18 con Roma-Inter. Domenica chiudono il turno Juventus-Atalanta e Milan-Lecce, oltre alle altre gare già in calendario del campionato.",
    ],
    "fonti": [
        {
            "url": "https://www.gazzetta.it/Calcio/Serie-A/18-09-2026/monza-sassuolo-live-diretta-serie-a-risultato-gol.shtml",
            "descrizione": "La Gazzetta dello Sport — 2-1, doppietta Varela, Adzic, inviato da Monza.",
        },
        {
            "url": "https://www.corrieredellosport.it/live/partita/monza-sassuolo-2638167",
            "descrizione": "Corriere dello Sport — tabellino 2-1, minuti e marcatori.",
        },
        {
            "url": "https://www.eurosport.it/calcio/serie-a/2026-2027/live-monza-sassuolo_mtc21874331/live.shtml",
            "descrizione": "Eurosport — Varela 51’ e 63’ rigore, Adzic 88’.",
        },
        {
            "url": "https://www.legaseriea.it/serie-a/news/le-designazioni-arbitrali-della-5a-giornata",
            "descrizione": "Lega Serie A — designazione Perenzoni per Monza-Sassuolo.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/serie-a-quinta-giornata-orari-tv-monza-sassuolo-roma-inter-18-settembre-2026.html",
            "titolo": "Serie A, quinta giornata: orari e tv",
        },
        {
            "url": "/notizie/convocati-italia-mancini-nations-league-34-nomi-18-settembre-2026.html",
            "titolo": "Mancini convoca 34 azzurri, tra cui Kouadio",
        },
        {
            "url": "/notizie/juventus-nec-5-0-europa-league-17-settembre-2026.html",
            "titolo": "Juventus-NEC 5-0 in Europa League",
        },
    ],
}

COOP = {
    "slug": "cirielli-comitato-congiunto-260-milioni-cooperazione-18-settembre-2026",
    "titolo": "Cooperazione, Cirielli firma 260 milioni: Ghana, Ucraina e Armenia",
    "sommario": "Quinta riunione del Comitato congiunto. 20 milioni all’agricoltura digitale in Ghana, 15 alla ricostruzione ucraina, 2 milioni per i rifugiati in Armenia.",
    "categoria": "Politica",
    "luogo": "Roma",
    "formato": "standard",
    "stato": "UFFICIALE",
    "parole_chiave_titolo": ["Cirielli", "cooperazione"],
    "dati_chiave": [
        {"icona": "◆", "valore": "260 mln", "etichetta": "pacchetto approvato dal Comitato congiunto"},
        {"icona": "●", "valore": "20 mln", "etichetta": "programma agricolo digitale in Ghana"},
        {"icona": "↗", "valore": "15 mln", "etichetta": "fondo europeo per la ricostruzione in Ucraina"},
    ],
    "paragrafi": [
        "Edmondo Cirielli ha presieduto alla Farnesina la quinta riunione del 2026 del Comitato Congiunto per la Cooperazione allo Sviluppo. Lo comunica il ministero degli Esteri il 18 settembre. Il comitato ha approvato un pacchetto di circa 260 milioni di euro, in linea con la programmazione 2026.",
        "In Africa è stato approvato un finanziamento di 20 milioni di euro per il programma Agbledu Smart-Agri Markets in Ghana, con le autorità ghanesi e l’UNDP. L’iniziativa punta a mercati agricoli digitali e a strumenti di accesso al credito, nel quadro del Piano Mattei.",
        "Per l’Ucraina il comitato ha destinato 15 milioni di euro all’European Flagship Fund for the Reconstruction of Ukraine. Lo scopo dichiarato è favorire capitali privati per la ripresa, non un trasferimento diretto al bilancio di Kiev. Per l’Armenia sono stati deliberati 2 milioni di euro, con UNHCR e FAO, per l’inclusione dei rifugiati.",
        "In Asia è prevista un’iniziativa con la Banca asiatica di sviluppo a sostegno del bilancio pubblico del Vietnam, per accelerare competitività e commercio del settore privato. È stato inoltre approvato un progetto da 3,5 milioni di euro sulla rigenerazione di acqua e suolo nella valle del Fergana.",
        "Il pacchetto comprende 9 milioni di euro di contributi a organismi multilaterali. Emilia-Romagna, Lombardia e Friuli Venezia Giulia hanno ottenuto tre progetti per circa 15,5 milioni di euro dal Fondo Regioni, destinati a Paesi partner della Cooperazione italiana.",
        "Il comunicato indica l’importo complessivo e i capitoli principali. Non pubblica la ripartizione integrale dei 260 milioni né i calendari di erogazione. L’apertura della sede AICS a Jerevan resta un atto distinto da questi finanziamenti.",
        "Cirielli è vice ministro con delega alla cooperazione. Il Comitato congiunto adotta i finanziamenti della Cooperazione italiana in linea con la programmazione 2026, adottata a maggio. I calendari di erogazione non sono indicati nel comunicato odierno della Farnesina.",
    ],
    "fonti": [
        {
            "url": "https://www.esteri.it/it/sala_stampa/archivionotizie/comunicati/2026/09/irielli-presiede-la-quinta-riunione-del-comitato-congiunto-per-la-cooperazione-allo-sviluppo-per-il-2026/",
            "descrizione": "MAECI — comunicato 18 settembre 2026, pacchetto da circa 260 milioni.",
        },
        {
            "url": "https://www.esteri.it/it/sala_stampa/archivionotizie/comunicati/",
            "descrizione": "MAECI — elenco comunicati del 18 settembre, inclusa la missione in Armenia.",
        },
        {
            "url": "https://www.esteri.it/en/sala_stampa/archivionotizie/comunicati/2026/06/il-vice-ministro-cirielli-presiede-il-comitato-congiunto-per-la-cooperazione-allo-sviluppo/",
            "descrizione": "MAECI — precedente riunione del Comitato congiunto, contesto di programmazione.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/cirielli-armenia-aics-jerevan-18-settembre-2026.html",
            "titolo": "Cirielli in Armenia: AICS apre a Jerevan da ottobre",
        },
        {
            "url": "/notizie/tajani-bolat-turchia-farnesina-hormuz-commercio-18-settembre-2026.html",
            "titolo": "Tajani vede Bolat alla Farnesina",
        },
        {
            "url": "/notizie/ue-33-miliardi-ucraina-missili-droni-17-settembre-2026.html",
            "titolo": "Ue, 33 miliardi per l’Ucraina",
        },
    ],
}

LIEGRO = {
    "slug": "papa-leone-inchiesta-diocesana-don-luigi-di-liegro-18-settembre-2026",
    "titolo": "Leone XIV avvia l’inchiesta diocesana su don Luigi Di Liegro",
    "sommario": "Il Papa lo ha detto in Laterano. È il primo passo sulla fama di santità del fondatore della Caritas di Roma, morto nel 1997. Non è ancora una beatificazione.",
    "categoria": "Cultura",
    "luogo": "Roma",
    "formato": "flash",
    "stato": "UFFICIALE",
    "parole_chiave_titolo": ["Di Liegro", "Leone XIV"],
    "dati_chiave": [
        {"icona": "◆", "valore": "18/09", "etichetta": "annuncio in San Giovanni in Laterano"},
        {"icona": "●", "valore": "1997", "etichetta": "morte di don Luigi Di Liegro"},
        {"icona": "↗", "valore": "1°", "etichetta": "passo: inchiesta diocesana, non beatificazione"},
    ],
    "paragrafi": [
        "Papa Leone XIV ha approvato l’avvio dell’inchiesta diocesana sulla vita, le virtù e la fama di santità di don Luigi Di Liegro. Lo ha detto venerdì 18 settembre all’assemblea diocesana di Roma, in San Giovanni in Laterano.",
        "«Ho approvato con gioia la decisione di compiere i passi necessari», ha detto il Papa, secondo il testo pubblicato sul sito della Santa Sede. Don Di Liegro, presbitero della diocesi di Roma, è morto il 12 ottobre 1997. Aveva fondato la Caritas diocesana.",
        "L’inchiesta diocesana è il primo passaggio del processo. Non equivale a una beatificazione già proclamata. Il giudizio sulle virtù e su un eventuale miracolo spetta alle fasi successive, presso la Santa Sede.",
        "Il Papa ha ricordato che nel 1969 don Luigi commissionò un’indagine sulla religiosità dei romani. «Non c’è incarnazione del messaggio senza ascolto della realtà», ha detto Leone XIV citando quel metodo.",
        "Poche settimane prima di morire, don Di Liegro disse agli operatori: «Il discernimento è questa domanda: Signore, dove sei?». L’assemblea in Laterano ha accolto l’annuncio con un applauso.",
    ],
    "fonti": [
        {
            "url": "https://www.vatican.va/content/leo-xiv/it/speeches/2026/september/documents/20260918-apertura-anno-pastorale.html",
            "descrizione": "Santa Sede — discorso di Leone XIV, 18 settembre 2026, Laterano.",
        },
        {
            "url": "https://www.ansa.it/vaticano/notizie/chiesa_italia/2026/09/18/il-papa-ricorda-don-di-liegro-sapeva-ascoltare-la-realta_79187a19-aad2-4139-b33d-5e4bb81200f4.html",
            "descrizione": "ANSA — il Papa benedice l’inchiesta per don Di Liegro.",
        },
        {
            "url": "https://www.repubblica.it/cronaca/2026/09/18/news/beatificazione_luigi_di_liegro_caritas_roma_poveri_migranti_malati_aids-425593827/",
            "descrizione": "la Repubblica — contesto su Di Liegro e la Caritas di Roma.",
        },
    ],
    "correlati": [
        {
            "url": "/notizie/papa-leone-angelus-ucraina-dialogo-diplomazia-6-settembre-2026.html",
            "titolo": "Leone XIV all’Angelus: dialogo sull’Ucraina",
        },
        {
            "url": "/notizie/vaticano-impianto-agrivoltaico-100-milioni-autosufficienza-energetica-22-agosto-2026.html",
            "titolo": "Vaticano, impianto agrivoltaico da 100 milioni",
        },
        {
            "url": "/notizie/byd-music-awards-arena-verona-conti-incontrada-rai1-18-settembre-2026.html",
            "titolo": "Music Awards stasera all’Arena di Verona",
        },
    ],
}


def main() -> None:
    for art in (MONZA, COOP, LIEGRO):
        assert_body(art)

    img_m = {
        "key": f"{MONZA['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "syntheticLikeness": "public-figure",
        "variants": save_image_variants(ROOT / "generated_images" / "juric-v437.jpg", f"{MONZA['slug']}-v{VERSION}"),
        "alt": "Scena editoriale contestuale generata con IA: Ivan Juric riconoscibile, occhiali e capelli grigi, in panchina con tuta rosso-bianca; somiglianza sintetica, non è una fotografia documentaria della partita.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-photorealistic Ivan Juric, glasses, Monza sideline, no text.",
    }
    img_c = {
        "key": f"{COOP['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "syntheticLikeness": "public-figure",
        "variants": save_image_variants(ROOT / "generated_images" / "cirielli-v437.jpg", f"{COOP['slug']}-v{VERSION}"),
        "alt": "Scena editoriale contestuale generata con IA: Edmondo Cirielli riconoscibile, occhiali e abito scuro, a un tavolo della Farnesina; somiglianza sintetica, non è una fotografia documentaria della riunione.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-photorealistic Edmondo Cirielli, glasses, Farnesina table, no text.",
    }
    img_d = {
        "key": f"{LIEGRO['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "syntheticLikeness": "public-figure",
        "variants": save_image_variants(ROOT / "generated_images" / "leone-v437.jpg", f"{LIEGRO['slug']}-v{VERSION}"),
        "alt": "Scena editoriale contestuale generata con IA: Papa Leone XIV riconoscibile in abito bianco, al pulpito in San Giovanni in Laterano; somiglianza sintetica, non è una fotografia documentaria dell’assemblea.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ultra-photorealistic Pope Leo XIV, Lateran basilica, no text.",
    }

    slug_m = persist(MONZA, img_m, "2026-09-18T23:10:00+02:00", public_figure=True)
    slug_c = persist(COOP, img_c, "2026-09-18T23:08:00+02:00", public_figure=True)
    slug_d = persist(LIEGRO, img_d, "2026-09-18T23:06:00+02:00", public_figure=True)
    sync_surfaces([MONZA, COOP, LIEGRO], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-18",
        "type": "content-release",
        "news_added": [slug_m, slug_c, slug_d],
        "news_updated": [],
        "change": "Monza-Sassuolo 2-1, pacchetto cooperazione 260 mln, inchiesta Di Liegro",
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
                "last_update": "scoop-v437",
            }
        )
        write_json(path, state)
    write_json(
        ROOT / "automation" / "logs" / "scoop-20260918T231000-Europe-Rome.json",
        {
            "run_at": "2026-09-18T23:10:00+02:00",
            "skill": "ultime-notizie-scoop",
            "desks": ["sport", "esteri", "vaticano"],
            "processed": [
                {"title": MONZA["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_m}.html"},
                {"title": COOP["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_c}.html"},
                {"title": LIEGRO["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_d}.html"},
            ],
            "discarded": [
                {"topic": "Kohat Pakistan bombing", "reason": "bilancio vittime discordante 21/27, non fissato"},
                {"topic": "Tripodi Astana forum", "reason": "comunicato sottile, impatto sotto il Comitato congiunto"},
                {"topic": "Music Awards vincitori", "reason": "serata in corso, Rai senza elenco ufficiale"},
                {"topic": "UniCredit AT1", "reason": "mercato, materia insufficiente per pezzo autonomo utile"},
            ],
        },
    )


if __name__ == "__main__":
    main()
