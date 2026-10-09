#!/usr/bin/env python3
"""Release v818: tre breaking news italiane del 9 ottobre 2026."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site  # noqa: E402

VERSION = 818
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"

IMAGE_SOURCES = {
    "mutui": GENERATED / "exec-2a5b61f0-1852-4412-b013-73e2ac8b7b29.png",
    "industria": GENERATED / "exec-d986c1f4-93b9-45db-b2ec-97c3f413b0b3.png",
    "askatasuna": GENERATED / "exec-b3a55537-28ba-4164-8b67-4d9c5bdc3c41.png",
}


def make_variants(source: Path, slug: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 16 / 9
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    output = ROOT / "assets/images/editorial-auto"
    variants = []
    for width in (480, 800, 1200):
        path = output / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, round(width / ratio)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=89, method=6
        )
        variants.append({
            "w": width,
            "h": round(width / ratio),
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return variants


def make_image(article: dict) -> dict:
    image = {
        "key": f"{article['slug']}-v{VERSION}",
        "alt": article.pop("image_alt"),
        "prompt": article.pop("image_prompt"),
        "variants": make_variants(IMAGE_SOURCES[article.pop("image_source")], article["slug"]),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": article["categoria"] == "Cronaca",
        "weatherMap": False,
        "reenactedEvent": article["categoria"] == "Cronaca",
    }
    return image


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


def append_name_phrases() -> None:
    path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        "Prima di firmare, prenditi il tempo di confrontare tutte le condizioni.",
        "Anche un dato difficile diventa utile quando sai con cosa confrontarlo.",
        "Proteggi la tua serenità distinguendo i fatti dalle ipotesi.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


ARTICLES = [
    {
        "slug": "mutui-taeg-3-99-agosto-2026-massimi-dal-2024",
        "titolo": "Mutui al 3,99% ad agosto: il TAEG torna ai massimi dal 2024",
        "sommario": "Banca d'Italia registra un aumento dal 3,81% di luglio. Sale anche il costo del credito al consumo, mentre calano i tassi per le imprese.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Mutui", "3,99%", "massimi dal 2024"],
        "dati_chiave": [
            {"valore": "3,99%", "etichetta": "TAEG sui nuovi mutui"},
            {"valore": "3,81%", "etichetta": "dato di luglio"},
            {"valore": "10,78%", "etichetta": "TAEG del credito al consumo"},
        ],
        "paragrafi": [
            "Il Tasso annuale effettivo globale sui nuovi prestiti alle famiglie per l'acquisto di abitazioni è salito al 3,99% ad agosto 2026, dal 3,81% di luglio. Il dato pubblicato il 9 ottobre dalla Banca d'Italia riporta il costo dei nuovi mutui ai livelli più elevati dall'agosto 2024, quando aveva raggiunto il 4,09%.",
            "La quota delle nuove operazioni con un periodo iniziale di determinazione del tasso non superiore a un anno è scesa al 23,9%, rispetto al 29% del mese precedente. Il confronto descrive la composizione dei finanziamenti erogati nel mese, non una variazione automatica delle rate dei contratti già in corso.",
            "È aumentato anche il TAEG sulle nuove erogazioni di credito al consumo, passato dal 10,38% al 10,78%. Il tasso passivo medio sull'insieme dei depositi è rimasto invece fermo allo 0,69%.",
            "Per le società non finanziarie, il tasso sulle nuove operazioni è diminuito dal 3,79% al 3,71%. Il livello è stato del 4,40% per i prestiti fino a un milione di euro e del 3,30% per quelli di importo superiore.",
            "Nello stesso mese i prestiti alle famiglie sono cresciuti del 2,9% sui dodici mesi, dopo il 2,6% di luglio. Quelli alle società non finanziarie sono aumentati del 4,2%, mentre i depositi del settore privato hanno rallentato all'1,8% dal 2,4% precedente.",
            "Per chi sta valutando un finanziamento, il dato medio nazionale non coincide necessariamente con l'offerta personale: durata, importo, rapporto tra prestito e valore dell'immobile e profilo del richiedente possono modificare le condizioni. Il confronto utile resta quello tra TAEG indicati nei preventivi riferiti allo stesso importo e alla stessa durata.",
        ],
        "fonti": [
            {"url": "https://www.bancaditalia.it/pubblicazioni/moneta-banche/2026-moneta/statistiche_BAM_20261009.pdf", "nome": "Banca d'Italia — Banche e moneta: serie nazionali, agosto 2026."},
            {"url": "https://www.ansa.it/sito/notizie/economia/2026/10/09/bankitalia-ad-agosto-il-tasso-sui-mutui-a-un-passo-dal-4-ai-massimi-dal-2024_99bf60c4-fe92-4392-b91c-82574ecbe916.html", "nome": "ANSA — confronto del TAEG dei mutui con agosto 2024."},
        ],
        "image_source": "mutui",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una consulenza per un mutuo in un ufficio bancario italiano; scena non documentaria.",
        "image_prompt": "Consulenza per un mutuo in un moderno ufficio bancario italiano, coppia vista da dietro e consulente, modello di abitazione e grafico senza dati leggibili, fotografia editoriale ultrarealistica.",
        "published": datetime(2026, 10, 9, 11, 12, tzinfo=ROME),
    },
    {
        "slug": "produzione-industriale-agosto-2026-calo-1-3-istat",
        "titolo": "Industria, produzione giù dell’1,3%: energia unica eccezione",
        "sommario": "Istat rileva una flessione mensile ad agosto e un calo dell'1,1% nel trimestre. Su base annua l'indice resta invariato.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Industria", "1,3%", "energia"],
        "dati_chiave": [
            {"valore": "-1,3%", "etichetta": "variazione su luglio"},
            {"valore": "-1,1%", "etichetta": "media giugno-agosto"},
            {"valore": "+2,8%", "etichetta": "energia nel mese"},
        ],
        "paragrafi": [
            "La produzione industriale italiana è diminuita dell'1,3% ad agosto 2026 rispetto a luglio, secondo la stima diffusa dall'Istat il 9 ottobre. Nella media del periodo giugno-agosto il livello della produzione è sceso dell'1,1% rispetto ai tre mesi precedenti.",
            "L'energia è stato l'unico raggruppamento principale in crescita nel confronto mensile, con un aumento del 2,8%. Sono calati i beni strumentali dello 0,9%, i beni di consumo dell'1,2% e i beni intermedi dell'1,8%.",
            "Al netto degli effetti di calendario, l'indice è rimasto invariato rispetto ad agosto 2025. I giorni lavorativi sono stati 21, uno in più rispetto allo stesso mese dell'anno precedente.",
            "Nel confronto annuale l'energia è cresciuta dell'11,5% e i beni strumentali dello 0,7%. Le diminuzioni hanno interessato i beni intermedi, in calo del 4%, e i beni di consumo, scesi del 4,4%.",
            "Tra i singoli settori, la fornitura di energia elettrica, gas, vapore e aria ha segnato l'incremento tendenziale più ampio, pari al 14,5%. Le flessioni maggiori hanno riguardato tessile, abbigliamento, pelli e accessori (-14%), prodotti chimici (-11,4%) e computer, elettronica e ottica (-9,9%).",
            "Il dato mensile indica il volume della produzione realizzata e non misura direttamente fatturato, prezzi o occupazione. La prossima diffusione dell'Istat, riferita a settembre, è programmata per l'11 novembre 2026.",
        ],
        "fonti": [
            {"url": "https://www.istat.it/comunicato-stampa/produzione-industriale-agosto-2026/", "nome": "Istat — Produzione industriale, agosto 2026."},
            {"url": "https://www.ansa.it/sito/notizie/economia/2026/10/09/istat-produzione-industriale-agosto-13-su-mese-invariata-su-anno_41764f6d-7f24-4b5d-af76-bc4e47d90074.html", "nome": "ANSA — lancio sui dati Istat della produzione industriale."},
        ],
        "image_source": "industria",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un impianto manifatturiero italiano con una linea automatizzata; scena non documentaria.",
        "image_prompt": "Impianto manifatturiero italiano moderno, lavoratore con dispositivi di sicurezza e linea automatizzata, fotografia editoriale ultrarealistica senza marchi.",
        "published": datetime(2026, 10, 9, 11, 24, tzinfo=ROME),
    },
    {
        "slug": "askatasuna-14-perquisizioni-19-misure-richieste-9-ottobre-2026",
        "titolo": "Askatasuna, 14 perquisizioni: il pm chiede 19 misure",
        "sommario": "L'operazione della Polizia di Stato riguarda le indagini sui fatti del corteo del 31 gennaio a Torino. Le richieste attendono la valutazione giudiziaria.",
        "categoria": "Cronaca", "luogo": "Torino", "formato": "flash",
        "parole_chiave_titolo": ["Askatasuna", "14 perquisizioni", "19 misure"],
        "dati_chiave": [
            {"valore": "14", "etichetta": "perquisizioni domiciliari"},
            {"valore": "19", "etichetta": "misure cautelari richieste"},
            {"valore": "31 gennaio", "etichetta": "corteo oggetto dell'indagine"},
        ],
        "paragrafi": [
            "La Polizia di Stato di Torino ha eseguito dalle prime ore del 9 ottobre 14 perquisizioni domiciliari in diverse parti d'Italia. L'operazione riguarda militanti dell'area antagonista coinvolti nell'indagine sui fatti avvenuti durante la manifestazione nazionale del 31 gennaio contro lo sgombero di Askatasuna.",
            "Nell'ambito dello stesso procedimento, il pubblico ministero ha richiesto 19 misure cautelari per ipotesi di reato contestate a vario titolo in relazione al corteo. La Questura di Torino ha comunicato separatamente il numero delle perquisizioni e quello delle richieste.",
            "Le misure risultano richieste dal pm: questa formulazione non equivale alla loro applicazione. La decisione spetta all'autorità giudiziaria competente e le persone coinvolte devono essere considerate non colpevoli fino a un'eventuale sentenza definitiva.",
            "Le perquisizioni costituiscono attività d'indagine e non dimostrano da sole la responsabilità degli interessati. Le comunicazioni disponibili nelle prime ore dell'operazione non indicano l'esito dei singoli accertamenti né riportano una decisione definitiva sulle richieste cautelari.",
            "L'indagine è collegata alla manifestazione tenuta a Torino il 31 gennaio 2026 dopo lo sgombero del centro sociale. Eventuali sviluppi sulle posizioni individuali richiederanno atti giudiziari o nuove comunicazioni ufficiali.",
        ],
        "fonti": [
            {"url": "https://questure.poliziadistato.it/it/Torino/articolo/35286ac8a161252a7922260964", "nome": "Polizia di Stato, Questura di Torino — 14 perquisizioni e 19 misure cautelari richieste."},
            {"url": "https://www.ansa.it/sito/notizie/topnews/2026/10/09/scontri-askatasuna-perquisizioni-in-tutta-italia-chieste-19-misure_e9631841-2d3c-4882-a3f7-b0ffdad04813.html", "nome": "ANSA — riscontro indipendente sull'operazione e sul procedimento."},
        ],
        "image_source": "askatasuna",
        "image_alt": "Illustrazione editoriale IA ultrarealistica e non documentaria di agenti della Polizia di Stato davanti a un edificio di Torino, senza persone indagate visibili.",
        "image_prompt": "Agenti della Polizia di Stato visti da dietro davanti a un edificio di Torino all'alba, Mole Antonelliana sullo sfondo, nessun sospettato e nessuna targa, fotografia editoriale ultrarealistica e neutrale.",
        "published": datetime(2026, 10, 9, 11, 36, tzinfo=ROME),
    },
]


def main() -> None:
    append_name_phrases()
    images = []
    written = []
    for article in ARTICLES:
        published = article.pop("published")
        image = make_image(article)
        slug = site.write_article(article, image, VERSION)
        set_published(slug, published)
        article["published"] = published.isoformat(timespec="seconds")
        image["article"] = f"/notizie/{slug}.html"
        images.append(image)
        written.append(article)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    new_urls = {row["article"] for row in images}
    registry["items"] = images + [row for row in registry.get("items", []) if row.get("article") not in new_urls]
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces(written, f"/notizie/{written[-1]['slug']}.html", VERSION, update_manifest=False)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION,
        "currentVersion": VERSION,
        "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": f"breaking-news-v{VERSION}",
        "date": "2026-10-09",
        "release_date": "2026-10-09",
        "updated_at": "2026-10-09T11:36:00+02:00",
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
