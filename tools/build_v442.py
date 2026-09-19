#!/usr/bin/env python3
"""Pubblica il Codice doganale UE e la nomina di Luke Lindberg al WFP."""
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

VERSION = 442


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
        variants.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return variants


def stamp_dates(slug: str, published: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{published}"', page)
    path.write_text(page, encoding="utf-8")


def persist(article: dict, image: dict, published: str) -> str:
    slug = write_article(article, image, VERSION)
    stamp_dates(slug, published)
    article["published"] = published
    register_image(image, slug, VERSION)
    write_json(ROOT / "contenuti" / "notizie" / f"{slug}.json", {
        "slug": slug,
        "title": article["titolo"],
        "excerpt": article["sommario"],
        "category": article["categoria"],
        "published_at": published,
        "updated_at": published,
        "development_at": "2026-09-19",
        "status": article["stato"],
        "public_url": f"https://curiomondo.it/notizie/{slug}.html",
        "publication_state": "pending_deploy",
        "body": article["paragrafi"],
        "sources": article["fonti"],
        "image": image,
    })
    return slug


def assert_body(article: dict) -> None:
    words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in article["paragrafi"])
    lo, hi = {"flash": (100, 250), "standard": (300, 600), "feature": (800, 1500)}[article["formato"]]
    if not lo <= words <= hi:
        raise SystemExit(f"{article['slug']}: {words} parole, attese {lo}-{hi}")
    for i, paragraph in enumerate(article["paragrafi"], 1):
        count = len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", paragraph))
        if count > 60:
            raise SystemExit(f"{article['slug']} paragrafo {i}: {count} parole")


def fix_preexisting_publication_dates() -> None:
    """Allinea due articoli v438 alla prima commit realmente presente su main."""
    fixes = {
        "sandro-mazzola-morto-83-anni-inter-nazionale-19-settembre-2026.html": (
            "2026-09-19T07:18:00+02:00", "2026-09-19T08:58:00+02:00"
        ),
        "allerta-gialla-sei-regioni-temporali-19-settembre-2026.html": (
            "2026-09-19T07:16:00+02:00", "2026-09-19T08:57:00+02:00"
        ),
    }
    for filename, (old, new) in fixes.items():
        path = ROOT / "notizie" / filename
        page = path.read_text(encoding="utf-8").replace(old, new)
        path.write_text(page, encoding="utf-8")


DOGANE = {
    "slug": "nuovo-codice-doganale-ue-autorita-data-hub-19-settembre-2026",
    "titolo": "L’UE vara il nuovo Codice doganale e un’autorità comune",
    "sommario": "Il regolamento 2026/2108 è stato pubblicato oggi. Introduce un Data Hub europeo, nuove responsabilità per l’e-commerce e controlli coordinati.",
    "categoria": "Economia",
    "luogo": "Unione europea",
    "formato": "standard",
    "stato": "UFFICIALE",
    "parole_chiave_titolo": ["Codice doganale", "autorità comune"],
    "dati_chiave": [
        {"icona": "◆", "valore": "2027", "etichetta": "applicazione generale dal 21 settembre"},
        {"icona": "●", "valore": "2028", "etichetta": "regole chiave su vendite a distanza e autorità UE"},
        {"icona": "↗", "valore": "2034", "etichetta": "Data Hub pienamente operativo entro febbraio"},
    ],
    "paragrafi": [
        "L’Unione europea ha pubblicato sabato 19 settembre il nuovo Codice doganale. Il regolamento 2026/2108 sostituisce il testo del 2013, istituisce l’Autorità doganale europea e definisce il quadro del nuovo Data Hub comune. L’atto entra in vigore il giorno successivo alla pubblicazione.",
        "La maggior parte delle disposizioni si applicherà dal 21 settembre 2027. Le norme principali sulle vendite a distanza e alcune funzioni dell’Autorità scatteranno dal 1° luglio 2028. Il calendario evita un passaggio immediato per amministrazioni e imprese, mentre i poteri necessari a preparare l’attuazione partono prima.",
        "Il Data Hub dovrà concentrare in un ambiente unico le informazioni oggi distribuite tra numerosi sistemi nazionali. Importatori, esportatori e operatori del transito potranno usarlo dal marzo 2031; l’impiego diventerà obbligatorio dal marzo 2034. Tutte le funzionalità previste dovranno essere operative entro il 1° febbraio dello stesso anno.",
        "La riforma risponde soprattutto alla crescita dei piccoli pacchi acquistati online da Paesi extra-UE. Il regolamento introduce la figura dell’importatore per le vendite a distanza e attribuisce a piattaforme o venditori precise responsabilità sulla conformità delle merci. L’obiettivo è rendere identificabile l’operatore responsabile prima che il prodotto entri nel mercato europeo.",
        "Per le aziende considerate affidabili nasce lo status «Trust and Check». Gli operatori ammessi dovranno consentire alle dogane un accesso proporzionato ai sistemi elettronici che registrano movimenti e conformità. In cambio potranno ottenere procedure più fluide, compreso il rilascio delle merci senza intervento attivo quando non servono altre autorizzazioni.",
        "L’Autorità europea coordinerà analisi dei rischi, decisioni operative e applicazione uniforme delle regole. Le dogane manterranno anche compiti di tutela non finanziaria: sicurezza dei prodotti, salute, ambiente, proprietà intellettuale e misure restrittive. Il regolamento punta così a ridurre le differenze tra controlli nazionali.",
        "Per le imprese italiane il cambiamento non modifica oggi dazi o formalità. Apre invece un periodo di adattamento tecnico che interesserà operatori logistici, importatori, piattaforme digitali e rappresentanti doganali. Gli atti attuativi della Commissione definiranno diversi passaggi, compresa la tariffa europea di gestione prevista per alcuni invii.",
        "Il vecchio Codice resterà quindi il riferimento operativo durante la transizione. Le autorizzazioni e gli atti applicativi esistenti continueranno a valere finché non saranno sostituiti. La prima scadenza concreta indicata nel nuovo testo riguarda gli atti necessari a costruire il sistema e avviare la nuova Autorità.",
    ],
    "fonti": [
        {"url": "https://eur-lex.europa.eu/eli/reg/2026/2108/oj", "descrizione": "EUR-Lex — Regolamento (UE) 2026/2108, Gazzetta ufficiale del 19 settembre 2026."},
        {"url": "https://eur-lex.europa.eu/oj/daily-view/L-series/default.html", "descrizione": "Gazzetta ufficiale dell’Unione europea — Serie L del 19 settembre 2026."},
        {"url": "https://taxation-customs.ec.europa.eu/customs/eu-customs-reform_en", "descrizione": "Commissione europea — quadro della riforma doganale, Data Hub e Autorità UE."},
        {"url": "https://european-union.europa.eu/priorities-and-actions/actions-topic/customs_en", "descrizione": "Unione europea — funzioni e controlli dell’unione doganale."},
    ],
    "correlati": [
        {"url": "/notizie/tari-dichiarazione-90-giorni-decreto-147-imu-sanzioni-18-settembre-2026.html", "titolo": "TARI, dichiarazione entro 90 giorni: le nuove regole"},
        {"url": "/notizie/trump-ue-canada-associazione-dazi-17-settembre-2026.html", "titolo": "Trump, UE e Canada: il nuovo confronto sui dazi"},
        {"url": "/notizie/ue-alleanza-assicurativa-clima-eventi-estremi-16-settembre-2026.html", "titolo": "UE, la nuova alleanza contro i rischi climatici"},
    ],
}


LINDBERG = {
    "slug": "luke-lindberg-nuovo-direttore-programma-alimentare-mondiale-19-settembre-2026",
    "titolo": "Luke Lindberg guiderà il Programma alimentare mondiale",
    "sommario": "La nomina è stata annunciata da ONU e FAO dopo il via libera del consiglio WFP. Succede a Cindy McCain in una fase di forti tagli agli aiuti.",
    "categoria": "Mondo",
    "luogo": "Roma",
    "formato": "standard",
    "stato": "CONFERMATA DA PIÙ FONTI",
    "parole_chiave_titolo": ["Luke Lindberg", "Programma alimentare mondiale"],
    "dati_chiave": [
        {"icona": "◆", "valore": "37", "etichetta": "anni, attuale sottosegretario USDA al commercio"},
        {"icona": "●", "valore": "266 mln", "etichetta": "persone esposte a insicurezza alimentare acuta"},
        {"icona": "↗", "valore": "83", "etichetta": "Paesi raggiunti dagli aiuti WFP"},
    ],
    "paragrafi": [
        "Luke Lindberg è stato nominato nuovo direttore esecutivo del Programma alimentare mondiale delle Nazioni Unite. La decisione è stata annunciata da António Guterres e dal direttore generale della FAO Qu Dongyu dopo la consultazione con il consiglio dell’agenzia. Il WFP ha sede a Roma.",
        "Lindberg succederà a Cindy McCain, dimessasi per motivi di salute. Fino al passaggio di consegne resterà in carica ad interim il vice direttore Carl Skau. La data esatta dell’insediamento non è stata indicata nelle comunicazioni disponibili sabato mattina.",
        "Il nuovo responsabile ha 37 anni ed è sottosegretario statunitense all’Agricoltura per il commercio e gli affari agricoli esteri. In precedenza ha guidato la South Dakota Trade Association e ha lavorato ai vertici della Export-Import Bank durante la prima amministrazione Trump.",
        "La nomina arriva mentre l’agenzia affronta una forte riduzione delle risorse. Il WFP stima che circa 266 milioni di persone siano esposte a insicurezza alimentare acuta per conflitti, eventi meteorologici estremi e difficoltà economiche. I programmi attuali assistono più di 100 milioni di persone in 83 Paesi.",
        "Il consiglio esecutivo ha accolto la scelta sottolineando l’urgenza di una collaborazione stabile tra direzione, Stati finanziatori e Paesi destinatari. Il WFP dipende da contributi volontari: quando le entrate diminuiscono, l’organizzazione deve ridurre beneficiari, razioni o durata degli interventi.",
        "Gli Stati Uniti sono da molti anni il principale donatore dell’agenzia e dagli anni Novanta la guida del WFP è affidata a un cittadino americano. Lindberg era il candidato sostenuto dall’amministrazione statunitense. La procedura richiede una nomina congiunta dei vertici ONU e FAO dopo il confronto con il consiglio esecutivo.",
        "La sfida immediata sarà conciliare i bisogni umanitari con finanziamenti più limitati. Il WFP opera nelle emergenze, gestisce trasporti e catene logistiche per l’intero sistema ONU e sostiene programmi alimentari e scolastici. Ogni riduzione di capacità può quindi incidere anche sul lavoro di altre organizzazioni.",
        "Nel 2020 il Programma alimentare mondiale ha ricevuto il Nobel per la pace per l’azione contro la fame e per il contributo a impedire che il cibo venga usato come strumento di guerra. Il mandato di Lindberg inizierà in un contesto nel quale conflitti e crisi climatiche continuano ad ampliare la domanda di assistenza.",
    ],
    "fonti": [
        {"url": "https://www.wfp.org/news/statement-by-world-food-programme-executive-board-president-on-appointment-of-new-executive-director", "descrizione": "World Food Programme — dichiarazione del presidente del consiglio esecutivo sulla nomina."},
        {"url": "https://apnews.com/article/96aa238f519ef1ab7f8bf71217324867", "descrizione": "Associated Press — annuncio congiunto ONU-FAO e profilo di Luke Lindberg."},
        {"url": "https://www.reuters.com/world/un-appoints-trump-nominee-lindberg-head-world-food-programme-2026-09-18/", "descrizione": "Reuters — conferma indipendente della nomina e dati sull’attività del WFP."},
        {"url": "https://www.wfp.org/who-we-are", "descrizione": "World Food Programme — mandato, dimensioni e attività dell’organizzazione."},
    ],
    "correlati": [
        {"url": "/notizie/afghanistan-crisi-alimentare-14-milioni-wfp.html", "titolo": "Afghanistan, la crisi alimentare coinvolge 14 milioni di persone"},
        {"url": "/notizie/cirielli-comitato-congiunto-260-milioni-cooperazione-18-settembre-2026.html", "titolo": "Cooperazione italiana, approvato un pacchetto da 260 milioni"},
        {"url": "/notizie/fao-prezzi-alimentari-massimi-2022-4-settembre-2026.html", "titolo": "FAO, i prezzi alimentari e la pressione sulle famiglie"},
    ],
}


def main() -> None:
    for article in (DOGANE, LINDBERG):
        assert_body(article)

    img_dogane = {
        "key": f"{DOGANE['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "variants": save_image_variants(ROOT / "generated_images" / "dogane-ue-v442.png", f"{DOGANE['slug']}-v{VERSION}"),
        "alt": "Scena editoriale contestuale generata con IA: terminal merci europeo con varco doganale, camion, container e bandiera UE; non è una fotografia documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Photorealistic European cargo terminal and customs checkpoint at blue hour, freight trucks, containers, EU flag, no text or watermark.",
    }
    img_lindberg = {
        "key": f"{LINDBERG['slug']}-v{VERSION}",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "generator": "ChatGPT/OpenAI image generation",
        "syntheticLikeness": "public-figure",
        "variants": save_image_variants(ROOT / "generated_images" / "luke-lindberg-v442.png", f"{LINDBERG['slug']}-v{VERSION}"),
        "alt": "Scena editoriale contestuale generata con IA: Luke Lindberg riconoscibile in un centro logistico umanitario, con bandiera ONU sfocata; somiglianza sintetica, non è una fotografia documentaria.",
        "disclosure": CAPTION,
        "sensitiveContext": False,
        "reenactedEvent": False,
        "prompt": "Ordinary contextual editorial portrait of Luke Lindberg in a humanitarian logistics warehouse, UN-blue atmosphere, no ceremony, no text or watermark.",
    }

    fix_preexisting_publication_dates()
    slug_dogane = persist(DOGANE, img_dogane, "2026-09-19T09:20:00+02:00")
    slug_lindberg = persist(LINDBERG, img_lindberg, "2026-09-19T09:22:00+02:00")
    sync_surfaces([DOGANE, LINDBERG], "", VERSION)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-19",
        "type": "content-release",
        "news_added": [slug_dogane, slug_lindberg],
        "news_updated": [],
        "change": "Nuovo Codice doganale UE e nomina Luke Lindberg al WFP",
        "image_policy_applied": "new-openai-contextual-editorial-images",
    }
    write_json(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if not path.exists():
            continue
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": "2026-09-19",
            "release_date": "2026-09-19",
            "articleCount": int(state.get("articleCount", 0)) + 2,
            "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 2,
            "last_update": "news-v442",
        })
        write_json(path, state)

    write_json(ROOT / "automation" / "logs" / "editoriale-20260919T092200-Europe-Rome.json", {
        "run_at": "2026-09-19T09:22:00+02:00",
        "skill": "editoriale-fonti-primarie",
        "processed": [
            {"title": DOGANE["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_dogane}.html"},
            {"title": LINDBERG["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{slug_lindberg}.html"},
        ],
    })


if __name__ == "__main__":
    main()
