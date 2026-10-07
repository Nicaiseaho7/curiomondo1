#!/usr/bin/env python3
"""Pubblica due approfondimenti serali del 7 ottobre 2026 senza aggiornare il manifest."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site  # noqa: E402

VERSION = 799
ROME = ZoneInfo("Europe/Rome")
CAPTION = site.CAPTION
GENERATED = ROOT.parent / "generated_images"

IMAGES = {
    "editoria": GENERATED / "exec-bc5d9356-ad91-435a-9975-f20840270d6f.png",
    "sovracapacita": GENERATED / "exec-fe6a3933-a0a9-4763-9534-8d2234efc2fc.png",
}


def variants(source: Path, slug: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 16 / 9
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = max(0, (image.height - height) // 2)
        image = image.crop((0, top, image.width, top + height))

    output = ROOT / "assets/images/editorial-auto"
    result = []
    for width in (480, 800, 1200):
        height = round(width / ratio)
        path = output / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, height), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=90, method=6
        )
        result.append({
            "w": width,
            "h": height,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return result


def image_record(slug: str, source: Path, alt: str, prompt: str) -> dict:
    return {
        "key": f"{slug}-v{VERSION}",
        "alt": alt,
        "prompt": prompt,
        "variants": variants(source, slug),
        "disclosure": CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": False,
        "weatherMap": False,
    }


def set_published(slug: str, published: datetime) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    iso = published.isoformat(timespec="seconds")
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data["datePublished"] = iso
            data["dateModified"] = iso
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )


def register_image_once(image: dict, slug: str) -> None:
    path = ROOT / "assets/data/editorial-images-v210.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    key = image["key"]
    article_path = f"/notizie/{slug}.html"
    data["items"] = [
        item for item in data.get("items", [])
        if item.get("key") != key and item.get("article") != article_path
    ]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.register_image(image, slug, VERSION)


def main() -> None:
    now = datetime.now(ROME).replace(second=0, microsecond=0)
    articles = [
        {
            "slug": "libri-italiani-record-traduzioni-mercato-trade-2026",
            "titolo": "Libri italiani, record di 8.645 traduzioni e mercato trade +3,2%",
            "sommario": (
                "Alla Buchmesse l'AIE registra un massimo storico per i diritti venduti all'estero. "
                "Nei primi nove mesi del 2026 torna a crescere anche il mercato italiano di narrativa e saggistica a stampa."
            ),
            "luogo": "Francoforte",
            "categoria": "Cultura",
            "formato": "standard",
            "parole_chiave_titolo": ["8.645 traduzioni", "mercato trade +3,2%"],
            "dati_chiave": [
                {"icona": "◆", "valore": "8.645", "etichetta": "contratti di traduzione nel 2025"},
                {"icona": "▲", "valore": "+3,2%", "etichetta": "vendite trade a valore nel 2026"},
                {"icona": "●", "valore": "64", "etichetta": "Paesi raggiunti dai libri italiani"},
            ],
            "paragrafi": [
                "I libri italiani non erano mai stati venduti così tanto all'estero sotto forma di diritti di traduzione. Nel 2025 gli editori hanno firmato 8.645 contratti, il livello più alto da quando l'Associazione Italiana Editori ha iniziato la rilevazione nel 2001.",
                "Il dato è stato presentato il 7 ottobre alla Fiera del libro di Francoforte insieme ai numeri più recenti del mercato interno.",
                "Le opere italiane hanno raggiunto 64 Paesi e sono state tradotte in 45 lingue. Il segmento più esportato è quello per bambini e ragazzi, con 3.133 titoli; seguono la narrativa con 1.753 e la saggistica generale con 1.585. L'Europa resta la prima destinazione con 5.401 titoli, mentre l'Asia ne assorbe 1.088.",
                "Il record internazionale arriva dopo un 2025 meno brillante sul mercato domestico. Considerando l'intera editoria italiana, le vendite dell'anno scorso sono state pari a 3,198 miliardi di euro, in calo dell'1,2%. La fotografia del 2026 mostra però una ripartenza nel perimetro trade, cioè narrativa e saggistica a stampa acquistate in libreria, online e nella grande distribuzione.",
                "Nei primi nove mesi dell'anno il mercato trade ha generato 1.026,5 milioni di euro, il 3,2% in più rispetto allo stesso periodo del 2025. Le copie vendute sono state 69,8 milioni, con un aumento del 2,6%.",
                "La differenza tra crescita a valore e crescita dei volumi è contenuta e non basta, da sola, a stabilire quanto abbiano inciso prezzi, promozioni o composizione degli acquisti.",
                "Le librerie fisiche sono il canale più dinamico: le vendite aumentano del 6,2% e arrivano al 57% del mercato. Gli store online restano quasi fermi, con un progresso dello 0,1% e una quota del 39%. La grande distribuzione perde invece il 7,5% e pesa ormai per il 4%.",
                "Anche i generi si muovono in modo diverso. I fumetti crescono del 14,9%, i libri per bambini e ragazzi del 9,1%, la narrativa straniera del 6,9% e quella italiana del 4,9%. La saggistica specialistica scende dell'1,8%, mentre manualistica pratica e self help arretrano del 6,7%.",
                "Secondo il presidente dell'AIE Innocenzo Cipolletta, alla ripresa ha contribuito anche la domanda pubblica alimentata dal bonus biblioteche da 60 milioni di euro. È una valutazione dell'associazione, non una misura isolata dell'effetto del provvedimento: i dati diffusi non separano infatti il peso del bonus dagli altri fattori che hanno sostenuto le vendite.",
                "Sul fronte internazionale l'Italia destina 1,5 milioni di euro l'anno al sostegno delle traduzioni. A Francoforte partecipano 134 espositori italiani, 66 dei quali riuniti nello Spazio Italia. La combinazione di promozione, acquisto di diritti e presenza nelle fiere aiuta a spiegare il percorso di lungo periodo: rispetto ai 1.800 contratti del 2001, il numero è quasi quintuplicato.",
                "I due segnali vanno letti insieme ma non confusi. Il record delle traduzioni misura l'interesse degli editori stranieri per i titoli italiani; il +3,2% misura invece le vendite trade sul mercato nazionale nei primi nove mesi del 2026. Entrambi indicano una fase favorevole, ma con perimetri e tempi differenti.",
            ],
            "fonti": [
                {
                    "url": "https://www.aie.it/Cosafacciamo/AIEtiinforma/News/Leggilanotizia.aspx?IDUNI=jmjaniqe4t25z0yiv0zhojws5626&MDId=10597&RAE=10635%3B1%3B102-71-2007.3.16%3B102-6332-2026.10.7%3B-1%3B102%3B&Skeda=MODIF102-6332-2026.10.7",
                    "nome": "Associazione Italiana Editori — rapporto e dati presentati alla Buchmesse il 7 ottobre 2026.",
                },
                {
                    "url": "https://www.ansa.it/amp/sito/notizie/cultura/libri/approfondimenti/2026/10/07/ansa-vendite-record-nel-2025-di-diritti-di-traduzione-dei-libri-italiani_49a031f4-d529-4999-a983-8ff91797f3e9.html",
                    "nome": "ANSA — riscontro indipendente sui dati AIE e sui canali di vendita.",
                },
            ],
            "image": image_record(
                "libri-italiani-record-traduzioni-mercato-trade-2026",
                IMAGES["editoria"],
                "Illustrazione editoriale IA di professionisti dei diritti editoriali tra libri alla Fiera di Francoforte; scena non documentaria.",
                "Fiera internazionale del libro a Francoforte, professionisti editoriali di diverse nazionalità discutono diritti di traduzione attorno a volumi aperti, fotografia editoriale realistica, luce naturale, nessun testo sovrapposto.",
            ),
            "published": now - timedelta(minutes=1),
        },
        {
            "slug": "g20-sovracapacita-auto-elettriche-chip-07-10-2026",
            "titolo": "Auto elettriche e chip, 15 partner G20 aprono il dossier sovracapacità",
            "sommario": (
                "Una dichiarazione congiunta avvia piattaforme tecniche su cinque filiere industriali. "
                "Non è un accordo dell'intero G20 e, per ora, non introduce dazi o limiti alla produzione."
            ),
            "luogo": "Milwaukee / Parigi",
            "categoria": "Economia",
            "formato": "standard",
            "parole_chiave_titolo": ["15 partner G20", "sovracapacità"],
            "dati_chiave": [
                {"icona": "◆", "valore": "15", "etichetta": "firmatari della dichiarazione"},
                {"icona": "▲", "valore": "5", "etichetta": "filiere industriali indicate"},
                {"icona": "●", "valore": "dicembre", "etichetta": "termine per il prossimo incontro tecnico"},
            ],
            "paragrafi": [
                "Quindici partecipanti al G20 hanno aperto un confronto tecnico sulla sovracapacità produttiva in alcune filiere manifatturiere strategiche. La dichiarazione, resa pubblica il 7 ottobre dopo la riunione dei ministri del Commercio a Milwaukee, è firmata anche da Italia e Unione Europea, ma non rappresenta un'intesa unanime dell'intero gruppo.",
                "I firmatari sono Argentina, Australia, Canada, Unione Europea, Francia, Germania, India, Italia, Giappone, Corea, Messico, Polonia, Turchia, Regno Unito e Stati Uniti. Il documento concentra l'attenzione su automobili e veicoli elettrici, batterie, prodotti chimici di base, semiconduttori di base e pannelli solari.",
                "La preoccupazione espressa è che capacità produttiva e offerta possano restare stabilmente superiori alla domanda mondiale grazie a politiche o interventi pubblici non orientati dal mercato. Secondo i firmatari, una simile situazione può comprimere i prezzi, scoraggiare nuovi investimenti e concentrare la produzione in pochi Paesi, aumentando anche la dipendenza delle catene di fornitura.",
                "Si tratta della posizione politica contenuta nella dichiarazione, non di una misurazione condivisa da tutti i membri del G20. Il testo non attribuisce soglie numeriche ai singoli Paesi e non pubblica stime della capacità eccedente per le cinque filiere. Per questo la fase annunciata è anzitutto di raccolta e confronto dei dati.",
                "Gli alti funzionari dei firmatari si sono incontrati a margine del Comitato commercio dell'OCSE. Entro dicembre dovranno definire i termini di lavoro delle piattaforme settoriali, condividere informazioni non riservate, individuare le lacune informative e valutare possibili misure efficaci e complementari.",
                "Il passaggio operativo è quindi ancora preliminare. La dichiarazione non stabilisce nuovi dazi, quote, divieti di importazione o limiti alla produzione. Non crea neppure, al momento, un organismo permanente paragonabile al Forum globale sulla sovracapacità siderurgica nato dopo il confronto del G20 del 2016.",
                "Il precedente dell'acciaio è richiamato esplicitamente. A Shanghai e Hangzhou i Paesi del G20 avevano riconosciuto che sussidi e altri sostegni statali potevano alimentare distorsioni e sovrapproduzione. I quindici firmatari sostengono che da allora il problema si sia esteso ad altri comparti industriali e chiedono di riportarlo al centro della cooperazione economica.",
                "Per l'Italia il dossier tocca filiere in cui produzione nazionale e componenti importati sono strettamente intrecciati. Auto, batterie, pannelli solari e chip entrano in investimenti industriali e transizione energetica: eventuali misure future potrebbero incidere sia sulla concorrenza dei produttori sia sui costi degli input per le imprese utilizzatrici.",
                "La data da osservare è dicembre 2026, quando il gruppo tecnico dovrebbe precisare metodo, dati e possibili strumenti. Fino ad allora il risultato concreto è un coordinamento tra una parte dei partecipanti al G20, non una decisione commerciale già applicabile.",
            ],
            "fonti": [
                {
                    "url": "https://www.esteri.it/it/sala_stampa/archivionotizie/comunicati/2026/10/dichiarazione-ministeriale-congiunta-sulla-risoluzione-del-problema-della-sovracapacita-strutturale-e-produttiva/",
                    "nome": "Ministero degli Affari Esteri — testo ufficiale della dichiarazione congiunta pubblicata il 7 ottobre 2026.",
                },
            ],
            "image": image_record(
                "g20-sovracapacita-auto-elettriche-chip-07-10-2026",
                IMAGES["sovracapacita"],
                "Illustrazione editoriale IA di una fabbrica integrata di auto elettriche, batterie e pannelli solari; scena non documentaria.",
                "Grande fabbrica moderna con linea di assemblaggio di veicoli elettrici, moduli batteria e pannelli solari, tecnici al lavoro, fotografia industriale realistica, nessun logo e nessun testo.",
            ),
            "published": now,
        },
    ]

    for article in articles:
        published = article["published"]
        article_path = ROOT / "notizie" / f"{article['slug']}.html"
        if article_path.exists():
            article_path.unlink()
        site.write_article(article, article["image"], VERSION)
        register_image_once(article["image"], article["slug"])
        set_published(article["slug"], published)

    latest_url = f"/notizie/{articles[-1]['slug']}.html"
    site.sync_surfaces(articles, latest_url, VERSION, update_manifest=False)


if __name__ == "__main__":
    main()
