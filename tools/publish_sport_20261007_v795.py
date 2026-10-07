#!/usr/bin/env python3
"""Release v795: Serie A, MotoGP Indonesia e Masters 1000 Shanghai."""
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

VERSION = 795
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"
IMAGES = {
    "serie_a": GENERATED / "exec-30d9516a-f8fd-4dbb-9dba-c2925432a0db.png",
    "motogp": GENERATED / "exec-c692dcd4-a393-4c65-9554-c29124c02774.png",
    "shanghai": GENERATED / "exec-91152c1b-fa3b-4690-a29f-3f6ed5c5e21a.png",
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
    result = []
    out = ROOT / "assets/images/editorial-auto"
    for width in (480, 800, 1200):
        height = round(width / ratio)
        path = out / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, height), Image.Resampling.LANCZOS).save(path, "WEBP", quality=90, method=6)
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
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": False,
        "weatherMap": False,
    }


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
    articles = [
        {
            "slug": "serie-a-sesta-giornata-orari-tv-biglietti-10-12-ottobre-2026",
            "titolo": "Serie A, 6ª giornata: orari, dirette TV e biglietti",
            "sommario": (
                "Il campionato riparte dal 10 al 12 ottobre con dieci partite. Tutte sono su DAZN; "
                "Napoli-Frosinone, Lazio-Monza e Torino-Udinese anche su Sky."
            ),
            "luogo": "Italia",
            "categoria": "Sport",
            "formato": "standard",
            "parole_chiave_titolo": ["6ª giornata", "dirette TV e biglietti"],
            "dati_chiave": [
                {"icona": "◆", "valore": "10 partite", "etichetta": "dal 10 al 12 ottobre"},
                {"icona": "▲", "valore": "3 partite", "etichetta": "anche su Sky"},
                {"icona": "●", "valore": "DAZN", "etichetta": "tutto il turno in diretta"},
            ],
            "paragrafi": [
                "La Serie A 2026-2027 riparte sabato 10 ottobre dopo la pausa con la sesta giornata. Il programma ufficiale distribuisce le dieci partite su tre giorni, da Genoa-Fiorentina alle 15 di sabato fino a Torino-Udinese alle 20:45 di lunedì.",
                "Sabato 10 ottobre si giocano Genoa-Fiorentina alle 15, Inter-Parma alle 18 e Napoli-Frosinone alle 20:45. Le prime due sono trasmesse in diretta esclusiva da DAZN; la gara di Napoli è disponibile su DAZN e anche sui canali Sky Sport e in streaming su NOW.",
                "Domenica 11 ottobre apre Como-Roma alle 12:30 su DAZN. Alle 15 sono in programma Lazio-Monza, visibile su DAZN, Sky e NOW, e Lecce-Bologna, in esclusiva su DAZN. Sassuolo-Milan delle 18 e Cagliari-Juventus delle 20:45 completano la giornata su DAZN.",
                "Lunedì 12 ottobre restano due posticipi. Atalanta-Venezia comincia alle 18:30 ed è in esclusiva su DAZN; Torino-Udinese chiude il turno alle 20:45 con diretta su DAZN, Sky e NOW.",
                "Per assistere allo stadio, il riferimento corretto è sempre la biglietteria ufficiale della squadra di casa: Genoa, Inter, Napoli, Como, Lazio, Lecce, Sassuolo, Cagliari, Atalanta e Torino. Disponibilità, settore ospiti, eventuale tessera del tifoso e limiti territoriali possono cambiare fino al giorno della partita.",
                "Prima dell’acquisto conviene controllare che il dominio sia quello del club e che il circuito di vendita sia indicato dalla società. I biglietti dei rivenditori non autorizzati possono essere annullati; il nome sul titolo di accesso deve inoltre coincidere con il documento richiesto ai tornelli.",
                "La programmazione televisiva deriva dal prospetto pubblicato dalla Lega Serie A. Le app di DAZN, Sky Go e NOW consentono la visione sui dispositivi compatibili secondo il proprio abbonamento; orari e canali vanno ricontrollati il giorno della gara in caso di variazioni ufficiali.",
            ],
            "fonti": [
                {"url": "https://www.legaseriea.it/serie-a/news/quando-si-gioca-anticipi-e-posticipi-fino-alla-12a-giornata", "nome": "Lega Serie A — date e orari ufficiali dalla 6ª alla 12ª giornata."},
                {"url": "https://images.legaseriea.it/image/private/fl_attachment/prd/emzdipx98pkg0lgeqgrt.pdf", "nome": "Lega Serie A — prospetto ufficiale con programmazione DAZN e Sky della 6ª giornata."},
                {"url": "https://www.legaseriea.it/serie-a", "nome": "Lega Serie A — calendario, risultati e collegamenti ufficiali dei club."},
            ],
            "image": image_record(
                "serie-a-sesta-giornata-orari-tv-biglietti-10-12-ottobre-2026",
                IMAGES["serie_a"],
                "Illustrazione editoriale IA di uno stadio italiano al tramonto prima di una partita di Serie A; scena non documentaria.",
                "Stadio italiano moderno al tramonto, campo pronto, spalti pieni e tornelli in primo piano, senza loghi o testo leggibile.",
            ),
            "published": now - timedelta(minutes=2),
        },
        {
            "slug": "motogp-indonesia-2026-orari-tv-biglietti-espargaro-mir",
            "titolo": "MotoGP Indonesia: orari TV, biglietti e cambio Honda",
            "sommario": (
                "Mandalika ospita il Mondiale dal 9 all’11 ottobre. La Sprint è sabato alle 9 italiane, "
                "la gara domenica alla stessa ora; Aleix Espargaró sostituisce Joan Mir."
            ),
            "luogo": "Mandalika, Indonesia",
            "categoria": "Sport",
            "formato": "flash",
            "parole_chiave_titolo": ["MotoGP Indonesia", "cambio Honda"],
            "dati_chiave": [
                {"icona": "◆", "valore": "9-11 ott", "etichetta": "weekend di Mandalika"},
                {"icona": "▲", "valore": "09:00", "etichetta": "Sprint e gara in Italia"},
                {"icona": "●", "valore": "2 punti", "etichetta": "tra Martin e Márquez"},
            ],
            "paragrafi": [
                "La MotoGP torna subito in pista dal 9 all’11 ottobre 2026 per il Gran Premio d’Indonesia a Mandalika. Il circuito di Lombok ospita il diciassettesimo appuntamento della stagione, con Jorge Martin e Marc Márquez separati da appena due punti dopo Motegi.",
                "La novità ufficiale riguarda Honda: Aleix Espargaró sostituirà Joan Mir nel team HRC Castrol. Mir salterà anche il fine settimana indonesiano su consiglio dei medici; per Espargaró sarà la prima gara dalla finale di Valencia 2025.",
                "Venerdì 9 ottobre la MotoGP disputa la prima sessione alle 4:45 italiane e le pre-qualifiche alle 9. Sabato 10 sono previste le qualifiche dalle 4:50, mentre la Sprint parte alle 9. Domenica 11 la gara della classe regina scatta alle 9 italiane, dopo Moto3 alle 6 e Moto2 alle 7:15.",
                "Sky Sport MotoGP e NOW trasmettono in diretta tutte le sessioni del weekend. TV8 propone in chiaro le qualifiche e la Sprint sabato mattina; domenica manda le gare in differita, con Moto3 alle 11, Moto2 alle 12:15 e MotoGP alle 14.",
                "Il servizio ufficiale MotoGP VideoPass offre inoltre prove, qualifiche e gare in diretta o on demand. Gli orari sono espressi nel fuso italiano e possono subire modifiche operative: prima della visione è consigliato controllare la guida aggiornata dell’emittente.",
                "I biglietti e i pacchetti ufficiali per Mandalika sono raggiungibili dalla pagina calendario MotoGP. L’acquisto deve essere completato tramite il portale collegato dall’organizzatore; prezzi, tribune disponibili e modalità di ritiro dipendono dalla categoria scelta.",
                "Sul piano sportivo, Márquez arriva da sei vittorie nelle ultime nove gare ma non ha ancora concluso la gara lunga a Mandalika. Martin resta leader con 333 punti contro 331: Sprint e Gran Premio possono quindi cambiare la testa della classifica nello stesso weekend.",
            ],
            "fonti": [
                {"url": "https://www.motogp.com/it", "nome": "MotoGP — calendario ufficiale, biglietteria, VideoPass e aggiornamenti del GP d’Indonesia."},
                {"url": "https://www.motogp.com/it/news/2026/10/06/aleix-espargaro-to-replace-mir-at-the-indonesian-gp/1171111", "nome": "MotoGP — comunicazione ufficiale sulla sostituzione di Joan Mir con Aleix Espargaró."},
                {"url": "https://sport.sky.it/motogp/calendario", "nome": "Sky Sport — calendario 2026 e diretta del GP d’Indonesia su Sky e NOW."},
                {"url": "https://www.quotidianomotori.com/motogp/motogp-indonesia-2026-orari-tv8-sky-mandalika/", "nome": "Quotidiano Motori — verifica degli orari italiani e della programmazione in chiaro su TV8."},
            ],
            "image": image_record(
                "motogp-indonesia-2026-orari-tv-biglietti-espargaro-mir",
                IMAGES["motogp"],
                "Illustrazione editoriale IA di motociclette sul circuito costiero di Mandalika in Indonesia; scena non documentaria.",
                "Circuito di Mandalika a Lombok in piena luce, gruppo di motociclette in curva, mare e colline tropicali sullo sfondo, senza loghi o testo.",
            ),
            "published": now - timedelta(minutes=1),
        },
        {
            "slug": "masters-shanghai-2026-date-biglietti-diretta-tennis-tv",
            "titolo": "Masters Shanghai al via: date, biglietti e diretta ufficiale",
            "sommario": (
                "Il Masters 1000 si gioca dal 7 al 18 ottobre sul cemento. Tennis TV trasmette "
                "126 incontri in diretta e on demand; i biglietti sono collegati dal calendario ATP."
            ),
            "luogo": "Shanghai, Cina",
            "categoria": "Sport",
            "formato": "flash",
            "parole_chiave_titolo": ["Masters Shanghai", "diretta ufficiale"],
            "dati_chiave": [
                {"icona": "◆", "valore": "7-18 ott", "etichetta": "date del torneo"},
                {"icona": "▲", "valore": "126", "etichetta": "partite su Tennis TV"},
                {"icona": "●", "valore": "Masters 1000", "etichetta": "categoria ATP"},
            ],
            "paragrafi": [
                "Il Rolex Shanghai Masters 2026 comincia mercoledì 7 ottobre e prosegue fino a domenica 18. Il torneo maschile si disputa sul cemento ed è l’unico Masters 1000 del calendario ATP in programma in Cina.",
                "Il servizio ufficiale Tennis TV indica 126 incontri complessivi disponibili in diretta e on demand. La piattaforma richiede un abbonamento Premium per le partite integrali; con un account gratuito restano accessibili alcuni contenuti, interviste e sintesi.",
                "Per seguire un giocatore specifico è utile consultare ogni giorno l’ordine di gioco ATP, perché campo e orario vengono definiti sessione per sessione. Shanghai è sei ore avanti rispetto all’Italia il 7 ottobre: un incontro serale locale può quindi iniziare nel primo pomeriggio italiano.",
                "I biglietti sono disponibili attraverso il collegamento Tickets presente nel calendario ufficiale ATP del torneo. Prima di pagare vanno controllati giorno, sessione, campo e condizioni di rimborso: un titolo per la sessione diurna non garantisce necessariamente l’accesso a quella serale.",
                "L’edizione 2026 si sviluppa su dodici giorni, un formato che distribuisce i primi turni e concede alle teste di serie tempi di ingresso diversi. Per questo la presenza di un giocatore nel tabellone non basta a stabilire in anticipo la data precisa del suo debutto.",
                "Tennis TV è il canale streaming ufficiale dell’ATP Tour e consente la visione su web e sulle app compatibili. Eventuali trasmissioni televisive nazionali possono avere palinsesti differenti; per evitare errori conviene controllare la guida del proprio operatore insieme all’ordine di gioco ufficiale.",
                "Tra i contenuti pubblicati alla vigilia figurano interviste ad Alexander Zverev, Félix Auger-Aliassime, Frances Tiafoe e all’italiano Flavio Cobolli. Dichiarazioni e presenza nelle interviste non sostituiscono però il programma giornaliero, che resta la fonte decisiva per sapere quando scendono in campo.",
            ],
            "fonti": [
                {"url": "https://www.atptour.com/en/tournaments?month=10", "nome": "ATP Tour — calendario ufficiale di ottobre 2026 e collegamento alla biglietteria di Shanghai."},
                {"url": "https://www.tennistv.com/tournaments/shanghai-open", "nome": "Tennis TV — date, superficie, 126 incontri e streaming ufficiale del Masters di Shanghai."},
                {"url": "https://www.tennistv.com/live-atp-streaming", "nome": "Tennis TV — condizioni generali della diretta ufficiale ATP e disponibilità on demand."},
            ],
            "image": image_record(
                "masters-shanghai-2026-date-biglietti-diretta-tennis-tv",
                IMAGES["shanghai"],
                "Illustrazione editoriale IA di un grande campo da tennis a Shanghai illuminato di sera; scena non documentaria.",
                "Grande stadio di tennis sul cemento a Shanghai, partita serale con skyline sullo sfondo, nessun logo o testo leggibile.",
            ),
            "published": now,
        },
    ]

    for article in articles:
        image = article.pop("image")
        published = article.pop("published")
        existing = ROOT / "notizie" / f"{article['slug']}.html"
        if existing.exists():
            set_published(article["slug"], published, article["formato"])
            continue
        slug = site.write_article(article, image, VERSION)
        site.register_image(image, slug, VERSION)
        set_published(slug, published, article["formato"])

    site.sync_surfaces(
        articles,
        "/notizie/masters-shanghai-2026-date-biglietti-diretta-tennis-tv.html",
        VERSION,
        update_manifest=False,
    )
    print(json.dumps({"version": VERSION, "articles": [a["slug"] for a in articles]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
