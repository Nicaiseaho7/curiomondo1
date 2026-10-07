#!/usr/bin/env python3
"""v798: completa i due placeholder Meloni accise e Sondrio 6 arresti."""
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

VERSION = 798
ROME = ZoneInfo("Europe/Rome")
GENERATED = Path("/tmp/generated_images")


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
    result = []
    out = ROOT / "assets/images/editorial-auto"
    out.mkdir(parents=True, exist_ok=True)
    for width in (480, 800, 1200):
        height = round(width / ratio)
        path = out / f"{slug}-v{VERSION}-{width}.webp"
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


def image_record(slug: str, source: Path, alt: str, prompt: str, synthetic: bool = False) -> dict:
    rec = {
        "key": f"{slug}-v{VERSION}",
        "alt": alt,
        "prompt": prompt,
        "variants": variants(source, slug),
        "disclosure": site.CAPTION,
        "generator": "Grok Imagine",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": False,
        "weatherMap": False,
    }
    if synthetic:
        rec["syntheticLikeness"] = "public-figure"
    return rec


def set_published(slug: str, published: datetime, article_format: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    iso = published.isoformat(timespec="seconds")
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data["datePublished"] = iso
            data["dateModified"] = iso
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    for node in doc.xpath('//article[contains(@class,"art-body")]'):
        node.set("data-article-format", article_format)
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )


def main() -> None:
    now = datetime.now(ROME).replace(second=0, microsecond=0)

    # remove broken placeholders so write_article can create them
    for slug in (
        "meloni-accise-mobili-160-milioni-iva-settembre-med9-spalato-07-10-2026",
        "sondrio-6-arresti-tentato-omicidio-castione-spaccio-07-10-2026",
    ):
        p = ROOT / "notizie" / f"{slug}.html"
        if p.exists() and p.stat().st_size < 500:
            p.unlink()
            print("removed placeholder", slug)

    articles = [
        {
            "slug": "meloni-accise-mobili-160-milioni-iva-settembre-med9-spalato-07-10-2026",
            "titolo": "Meloni al Med9: pronti a usare le accise mobili, 160-170 milioni a settembre",
            "sommario": (
                "Dal vertice di Spalato la premier conferma che il governo valuta se usare subito "
                "l'extragettito Iva di settembre o tenerlo di riserva. Domani il voto segreto sulla legge elettorale."
            ),
            "luogo": "Spalato",
            "categoria": "Politica",
            "formato": "standard",
            "parole_chiave_titolo": ["accise mobili", "160-170 milioni"],
            "dati_chiave": [
                {"icona": "◆", "valore": "160-170 mln", "etichetta": "extragettito Iva settembre"},
                {"icona": "▲", "valore": "Med9", "etichetta": "vertice a Spalato"},
                {"icona": "●", "valore": "8 ott", "etichetta": "voto segreto legge elettorale"},
            ],
            "paragrafi": [
                "La presidente del Consiglio Giorgia Meloni ha dichiarato mercoledì 7 ottobre a Spalato, al termine del vertice Med9 dei Paesi mediterranei dell'Unione europea, che il governo è pronto a intervenire di nuovo sul caro carburanti con il meccanismo delle accise mobili. Ha indicato che a settembre sono disponibili circa 160-170 milioni di euro di extragettito Iva destinabili a questo obiettivo.",
                "«Noi siamo sempre pronti a intervenire di nuovo, particolarmente con il meccanismo delle accise mobili. Al mese di settembre abbiamo circa 170 milioni che possono essere spesi per questo obiettivo. Ci stiamo interrogando se sia più efficace spenderli in questo momento, in cui comunque ci sono misure di contenimento, o tenerle come provvista quando dovessero terminare quelle misure», ha detto Meloni rispondendo a una domanda sul prezzo dei carburanti.",
                "La premier ha collegato la decisione anche all'andamento del price cap e ha auspicato che nelle ore successive si possa ripristinare pienamente quel meccanismo, dopo di che «la valutazione andrà fatta a valle». Non ha annunciato un decreto immediato né una data certa di reintroduzione dello sconto.",
                "Il Med9 riunisce a Spalato, in Croazia, i leader di Italia, Francia, Portogallo, Grecia, Cipro, Malta, Slovenia, Croazia e Spagna, con i vertici delle istituzioni europee. All'ordine del giorno figurano energia, immigrazione e stabilità del vicinato. L'agenda ufficiale di Palazzo Chigi aveva indicato la partecipazione di Meloni al vertice per mercoledì 7 ottobre.",
                "Sul fronte interno, il rialzo del gasolio dopo la scadenza dell'ultimo taglio delle accise ha riaperto il dibattito in maggioranza. Il vicepremier Matteo Salvini aveva già evitato, al question time alla Camera, l'ipotesi di prorogare le misure di riduzione delle accise attingendo all'extragettito Iva di settembre. Le dichiarazioni di Spalato restano una valutazione politica: finché non c'è un provvedimento pubblicato, lo sconto non è in vigore.",
                "Parallelamente a Montecitorio prosegue l'esame della riforma della legge elettorale. La Camera ha approvato mercoledì la terza questione di fiducia sull'articolo 3 con 228 voti a favore, 144 contrari e 3 astenuti. Il voto finale a scrutinio segreto è fissato per giovedì 8 ottobre: finché quel passaggio non c'è, e finché il testo non risulta approvato in modo conforme dalle due Camere, la riforma non è legge.",
            ],
            "fonti": [
                {"url": "https://www.governo.it/it/media/il-presidente-meloni-al-vertice-med9-di-spalato/32781", "nome": "Presidenza del Consiglio — Il Presidente Meloni al Vertice MED9 di Spalato"},
                {"url": "https://www.governo.it/it/agenda/2026-10-07t000000/vertice-med9/32729", "nome": "Presidenza del Consiglio — agenda ufficiale Vertice MED9, 7 ottobre 2026"},
                {"url": "https://www.rainews.it/articoli/2026/10/al-via-il-med9-con-meloni-e-macron-plankovic-la-stabilita-dellue-legata-a-quella-nostri-vicini-6df8beb7-f820-4d6d-885a-db3e7aed9b83.html", "nome": "RaiNews — Meloni: valutiamo accise mobili, spero si ripristini il price cap"},
                {"url": "https://www.ilsole24ore.com/art/legge-elettorale-ok-camera-fiducia-sull-articolo-1-AJgbkraB", "nome": "Il Sole 24 Ore — terza fiducia Camera e voto segreto di giovedì"},
            ],
            "image": image_record(
                "meloni-accise-mobili-160-milioni-iva-settembre-med9-spalato-07-10-2026",
                GENERATED / "meloni-med9.jpg",
                "Illustrazione editoriale IA di Giorgia Meloni al podio durante una conferenza stampa internazionale; somiglianza sintetica non documentaria.",
                "Giorgia Meloni at podium after Med9 summit press conference, ultra-realistic editorial, European flags background.",
                synthetic=True,
            ),
            "published": now - timedelta(minutes=5),
        },
        {
            "slug": "sondrio-6-arresti-tentato-omicidio-castione-spaccio-07-10-2026",
            "titolo": "Sondrio, 6 arresti per tentato omicidio a Castione e spaccio in Valtellina",
            "sommario": (
                "La Squadra mobile ha eseguito sei custodie cautelari dopo l'agguato del 2 luglio nell'area commerciale. "
                "Sequestrati circa 3,5 kg di cocaina e 4 kg di hashish."
            ),
            "luogo": "Sondrio",
            "categoria": "Cronaca",
            "formato": "standard",
            "parole_chiave_titolo": ["6 arresti", "Castione"],
            "dati_chiave": [
                {"icona": "◆", "valore": "6 arresti", "etichetta": "custodie cautelari"},
                {"icona": "▲", "valore": "3,5+4 kg", "etichetta": "cocaina e hashish sequestrati"},
                {"icona": "●", "valore": "2 luglio", "etichetta": "data dell'agguato a Castione"},
            ],
            "paragrafi": [
                "La Polizia di Stato ha eseguito mercoledì 7 ottobre sei ordinanze di custodia cautelare in carcere firmate dal gip del Tribunale di Sondrio su richiesta della Procura. Gli indagati sono ritenuti responsabili, a vario titolo, di due tentati omicidi, rapina aggravata, tentata estorsione aggravata, lesioni personali aggravate, traffico di sostanze stupefacenti e porto illegale di arma da fuoco.",
                "Secondo il comunicato della Polizia di Stato, gli investigatori della Questura di Sondrio, con il supporto della Questura di Crotone, hanno individuato il mandante e gli esecutori materiali del tentato omicidio consumato il 2 luglio nell'area commerciale di Castione Andevenno, in provincia di Sondrio.",
                "Il quadro ricostruito dalle indagini descrive un commando di quattro persone di origine calabrese giunto in Valtellina per un regolamento di conti legato al commercio di stupefacenti con un cittadino albanese. Nel pomeriggio del 2 luglio un sicario avrebbe fatto fuoco contro la vittima; la pistola si sarebbe inceppata e la persona bersaglio si è salvata. L'aggressore, sempre secondo l'accusa, si era impossessato dell'auto della vittima.",
                "Le indagini hanno ricostruito anche precedenti episodi di pestaggio, rapina ed estorsione e numerosi viaggi di droga collegati all'agguato. È emerso inoltre un ulteriore episodio di tentato omicidio, avvenuto qualche giorno prima del 2 luglio e attribuito agli stessi ambienti. È stata infine disvelata un'attività di spaccio di sostanze stupefacenti di diversa natura sul territorio valtellinese.",
                "Nel corso delle perquisizioni, estese a più province (tra cui Sondrio, Crotone, Salerno, Verona, Bolzano, Roma e Aosta secondo le ricostruzioni di stampa basate sul comunicato), sono stati sequestrati circa tre chili e mezzo di cocaina e quattro chili di hashish, una pistola scacciacani, due cartucce calibro 7,65, circa 2.500 euro in contanti e numerosi dispositivi informatici. Tre dei destinatari delle misure sono stati arrestati in flagranza di reato.",
                "I soggetti destinatari delle misure restano presunti innocenti fino a sentenza definitiva. Le indagini restano a carico della Procura di Sondrio; non risultano, al momento della stesura, comunicati che indichino condanne o patteggiamenti collegati a questa operazione.",
            ],
            "fonti": [
                {"url": "https://www.poliziadistato.it/articolo/sondrio--tentato-omicidio-al-centro-commerciale--6-arresti", "nome": "Polizia di Stato — Sondrio: tentato omicidio al centro commerciale, 6 arresti (7/10/2026)"},
                {"url": "https://milano.corriere.it/notizie/cronaca/26_ottobre_07/sondrio-gli-sparano-dopo-averlo-accecato-con-lo-spray-si-salva-perche-la-pistola-si-inceppa-sei-arresti-f6768d83-e39e-4492-91c9-6d33cb6fdxlk.shtml", "nome": "Corriere della Sera Milano — sei arresti e sequestri di droga"},
                {"url": "https://www.ilgiorno.it/sondrio/cronaca/tentato-omicidio-castione-andevenno-droga-328b10b3", "nome": "Il Giorno — tentato omicidio a Castione Andevenno e sei arresti"},
                {"url": "https://www.rainews.it/tgr/lombardia/articoli/2026/10/tentato-omicidio-a-castione-andevenno-6-arresti-1b02cf41-b5b6-4d67-8384-2801710a8830.html", "nome": "RaiNews TGR Lombardia — tentato omicidio Castione, 6 arresti"},
            ],
            "image": image_record(
                "sondrio-6-arresti-tentato-omicidio-castione-spaccio-07-10-2026",
                GENERATED / "sondrio-polizia.jpg",
                "Illustrazione editoriale IA di auto della polizia con lampeggianti blu in un parcheggio commerciale al crepuscolo; scena non documentaria, senza volti identificabili.",
                "Italian police cars blue lights commercial parking lot dusk operation, no identifiable faces.",
            ),
            "published": now - timedelta(minutes=2),
        },
    ]

    written = []
    for article in articles:
        image = article.pop("image")
        published = article.pop("published")
        slug = site.write_article(article, image, VERSION)
        site.register_image(image, slug, VERSION)
        set_published(slug, published, article["formato"])
        written.append(slug)
        print("written", slug, "bytes", (ROOT / "notizie" / f"{slug}.html").stat().st_size)

    site.sync_surfaces(
        articles,
        f"/notizie/{written[0]}.html",
        VERSION,
        update_manifest=False,
    )
    print(json.dumps({"version": VERSION, "articles": written}, ensure_ascii=False))


if __name__ == "__main__":
    main()
