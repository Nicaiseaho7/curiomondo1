#!/usr/bin/env python3
"""Pubblica cinque notizie del 7 ottobre 2026 da fonti primarie, senza manifest."""
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

VERSION = 800
ROME = ZoneInfo("Europe/Rome")
CAPTION = site.CAPTION
GENERATED = ROOT.parent / "generated_images"

IMAGES = {
    "usato": GENERATED / "exec-a802c706-4dc7-4c1c-9a4f-93fbac5d615f.png",
    "cef": GENERATED / "exec-53e127ef-7027-40f4-9761-877789a8d211.png",
    "rally": GENERATED / "exec-849e62e8-4ad0-4fff-a389-f14440fdf808.png",
    "cinema": GENERATED / "exec-7106eb1c-7c1a-4d4b-9ff8-2ad54687a0f9.png",
    "sole": GENERATED / "exec-4e9529a4-0292-4beb-82e5-6836501f5b49.png",
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


def image_record(slug: str, source: Path, alt: str, prompt: str, *, public=False) -> dict:
    record = {
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
    if public:
        record["syntheticLikeness"] = "public-figure"
    return record


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
    article_path = f"/notizie/{slug}.html"
    data["items"] = [
        item for item in data.get("items", [])
        if item.get("key") != image["key"] and item.get("article") != article_path
    ]
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.register_image(image, slug, VERSION)


def main() -> None:
    now = datetime.now(ROME).replace(second=0, microsecond=0)
    articles = [
        {
            "slug": "auto-usate-settembre-213-ogni-100-nuove-07-10-2026",
            "titolo": "Auto usate, a settembre 213 passaggi ogni 100 nuove",
            "sommario": (
                "I trasferimenti scendono dell'1,2%, ma ibride ed elettriche guadagnano spazio. "
                "Le vetture con almeno vent'anni rappresentano quasi un passaggio su cinque."
            ),
            "luogo": "Roma",
            "categoria": "Economia",
            "formato": "standard",
            "parole_chiave_titolo": ["213 passaggi", "100 nuove"],
            "dati_chiave": [
                {"icona": "◆", "valore": "284.708", "etichetta": "passaggi di auto a settembre"},
                {"icona": "▲", "valore": "12%", "etichetta": "quota delle ibride benzina"},
                {"icona": "●", "valore": "19,9%", "etichetta": "auto usate con almeno 20 anni"},
            ],
            "paragrafi": [
                "A settembre 2026 in Italia sono state trasferite 213 auto usate ogni 100 immatricolate nuove. I passaggi di proprietà delle autovetture, al netto delle minivolture, sono stati 284.708: l'1,2% in meno rispetto ai 288.065 dello stesso mese del 2025.",
                "Il nuovo bollettino Auto-Trend dell'Automobile Club d'Italia descrive quindi un mercato dell'usato ancora molto più ampio del nuovo, ma con volumi mensili in lieve arretramento. Nei primi nove mesi il rapporto è stato di 188 vetture usate ogni 100 nuove e i trasferimenti sono scesi dello 0,5% su base annua.",
                "Le moto seguono una direzione diversa. I passaggi sono aumentati del 2,5%, da 56.960 a 58.378. Considerando tutti i veicoli, le pratiche sono state 383.716, in calo dello 0,9% rispetto a settembre 2025.",
                "La composizione del mercato cambia più rapidamente del totale. Le ibride a benzina hanno raggiunto il 12% dei passaggi, contro il 9,6% di un anno prima, con un aumento dei volumi del 22,5%. Le elettriche restano all'1,4% del mercato, ma crescono del 20,1%; nei primi nove mesi la loro quota sale dall'1% all'1,4%.",
                "Benzina e diesel conservano insieme la maggioranza, ma il diesel scende dal 39,3% al 36,2% dei trasferimenti mensili. La benzina resta quasi stabile al 37,1%. Il dato mostra una transizione dell'usato più lenta rispetto al nuovo: le alimentazioni elettrificate avanzano, senza ancora avvicinarsi ai volumi delle motorizzazioni tradizionali.",
                "Un altro segnale riguarda l'età delle vetture. Le auto tra 20 e 29 anni costituiscono il 17% dei passaggi, in aumento dal 15,4%; quelle con almeno 30 anni pesano il 2,9%. Insieme rappresentano il 19,9% del mercato, quasi un'auto usata su cinque.",
                "Le radiazioni delle autovetture sono salite dello 0,7% a 106.883 pratiche. L'aumento deriva soprattutto dalle demolizioni, cresciute del 7,3%, mentre le esportazioni sono diminuite dell'11%. A settembre sono state radiate 80 auto ogni 100 nuove: il ricambio del parco prosegue, ma resta inferiore alle nuove immatricolazioni.",
            ],
            "fonti": [{
                "url": "https://aci.gov.it/comunicati-stampa/mercato-a-settembre-ogni-100-auto-nuove-vendute-213-usate/",
                "nome": "Automobile Club d'Italia — bollettino Auto-Trend sui dati del PRA, 7 ottobre 2026.",
            }],
            "image": image_record(
                "auto-usate-settembre-213-ogni-100-nuove-07-10-2026", IMAGES["usato"],
                "Illustrazione editoriale IA di acquirenti che esaminano automobili usate in un piazzale italiano; scena non documentaria.",
                "Piazzale italiano di auto usate vicino Roma, acquirenti e addetto con volti visibili esaminano numerose vetture, fotografia editoriale fotorealistica, nessun testo sovrapposto.",
            ),
            "published": now - timedelta(minutes=4),
        },
        {
            "slug": "cef-trasporti-246-progetti-tre-miliardi-07-10-2026",
            "titolo": "Trasporti UE, 246 progetti chiedono 3 miliardi: budget da 1,1",
            "sommario": (
                "Le domande superano di 2,69 volte i fondi CEF disponibili. La selezione riguarda reti TEN-T "
                "e mobilità militare; risultati previsti a marzo 2027."
            ),
            "luogo": "Bruxelles",
            "categoria": "Mondo",
            "formato": "flash",
            "parole_chiave_titolo": ["246 progetti", "3 miliardi"],
            "dati_chiave": [
                {"icona": "◆", "valore": "246", "etichetta": "domande ricevute da CINEA"},
                {"icona": "▲", "valore": "€3 mld", "etichetta": "cofinanziamento richiesto"},
                {"icona": "●", "valore": "€1,1 mld", "etichetta": "budget disponibile"},
            ],
            "paragrafi": [
                "Duecentoquarantasei progetti europei di trasporto hanno chiesto quasi 3 miliardi di euro al Connecting Europe Facility. La dotazione disponibile per il bando 2026 è di 1,1 miliardi: le richieste valgono quindi circa 2,69 volte il budget.",
                "I numeri sono stati pubblicati il 7 ottobre dalla CINEA, l'agenzia esecutiva europea che gestisce il programma, dopo la chiusura delle candidature del 6 ottobre. Non si tratta ancora di finanziamenti assegnati: tutte le proposte devono superare i controlli di ammissibilità e una valutazione tecnica.",
                "Gli esperti esterni, la Commissione europea e la stessa CINEA esamineranno i progetti idonei. I candidati dovrebbero ricevere l'esito nel marzo 2027; la firma degli accordi per le proposte selezionate è prevista entro giugno.",
                "Il bando sostiene costruzione e modernizzazione delle infrastrutture collegate alla rete transeuropea dei trasporti, la TEN-T. Tra gli ambiti indicati rientra anche la mobilità militare, cioè l'adeguamento di collegamenti e nodi affinché possano servire sia esigenze civili sia spostamenti logistici della difesa.",
                "Il rapporto tra domanda e risorse implica che, anche se tutte le candidature fossero ammissibili, il programma potrebbe coprire in media poco più di un terzo dell'importo richiesto. È soltanto un confronto aritmetico: la selezione non distribuirà automaticamente la stessa percentuale a ogni progetto e alcune proposte potranno ricevere l'intero contributo richiesto, altre una quota o nessun finanziamento.",
                "Nel ciclo 2021-2027 il CEF dispone complessivamente di 25,8 miliardi di euro per interventi di interesse comune sulla rete TEN-T. Circa l'80% dei fondi assegnati contribuisce agli obiettivi climatici dell'Unione, secondo la Commissione.",
                "Dal 2014 lo strumento ha sostenuto 1.943 progetti di trasporto con 46,54 miliardi di euro. Il prossimo passaggio utile non è dunque l'avvio immediato dei cantieri, ma la verifica delle domande e la graduatoria attesa a marzo 2027.",
            ],
            "fonti": [
                {"url": "https://cinea.ec.europa.eu/news-events/news/cef-transport-almost-eur3-billion-requested-transport-infrastructure-projects-2026-10-07_en", "nome": "CINEA — dati ufficiali sulle candidature CEF Transport 2026."},
                {"url": "https://cinea.ec.europa.eu/programmes/connecting-europe-facility_en", "nome": "Commissione europea — quadro e obiettivi del Connecting Europe Facility."},
            ],
            "image": image_record(
                "cef-trasporti-246-progetti-tre-miliardi-07-10-2026", IMAGES["cef"],
                "Illustrazione editoriale IA di tre ingegneri davanti a una rete ferroviaria e a un ponte europeo in costruzione; scena non documentaria.",
                "Tre ingegneri con volti visibili esaminano un progetto davanti a ferrovie ad alta velocità e un ponte europeo in costruzione, fotografia editoriale fotorealistica, nessun testo.",
            ),
            "published": now - timedelta(minutes=3),
        },
        {
            "slug": "rallylegend-somaschini-lancia-rally2-gryazin-07-10-2026",
            "titolo": "Rallylegend, Somaschini debutta sulla Lancia Rally2 con Gryazin",
            "sommario": (
                "A San Marino dall'8 all'11 ottobre correranno due Ypsilon Rally2 HF Integrale. "
                "Somaschini e Daiana Darderi formeranno il primo equipaggio femminile sulla nuova vettura."
            ),
            "luogo": "San Marino",
            "categoria": "Sport",
            "formato": "flash",
            "parole_chiave_titolo": ["Somaschini", "Lancia Rally2"],
            "dati_chiave": [
                {"icona": "◆", "valore": "2", "etichetta": "Ypsilon Rally2 schierate"},
                {"icona": "▲", "valore": "8-11 ott", "etichetta": "date di Rallylegend 2026"},
                {"icona": "●", "valore": "17", "etichetta": "prove vinte da Gryazin tra Croazia e Giappone"},
            ],
            "paragrafi": [
                "Rachele Somaschini guiderà per la prima volta la Lancia Ypsilon Rally2 HF Integrale a Rallylegend 2026, in programma a San Marino dall'8 all'11 ottobre. La seconda vettura sarà affidata a Nikolay Gryazin, pilota ufficiale Lancia Corse HF nel WRC2.",
                "Somaschini correrà con la copilota Daiana Darderi. Saranno il primo equipaggio interamente femminile a competere con la nuova Rally2 del marchio torinese, introdotta nella stagione del ritorno ufficiale di Lancia nei rally mondiali.",
                "La pilota italiana, 32 anni, ha vinto quattro titoli italiani femminili e la classifica assoluta del Tour European Rally 2024. Nel 2025 ha disputato cinque gare del WRC2 con una Citroën C3 Rally2; nel 2026 ha partecipato alla Dakar Classic su un Mercedes-Benz Unimog del 1988, chiudendo quinta tra i mezzi pesanti con un equipaggio femminile italiano.",
                "La partecipazione è collegata anche a Correre per un Respiro, il progetto con cui Somaschini sostiene la Fondazione per la ricerca sulla fibrosi cistica. Lancia aveva già affiancato l'iniziativa durante il Trofeo Lancia della stagione.",
                "Gryazin arriva a San Marino dopo avere contribuito al titolo mondiale a squadre WRC2 conquistato da Lancia nel primo anno del rientro. Con Konstantin Aleksandrov ha ottenuto una vittoria di categoria in Giappone, il terzo posto in Croazia e il secondo in Portogallo.",
                "Il dato più indicativo della sua velocità sono le prove speciali vinte: sette in Croazia e dieci in Giappone. Rallylegend, tuttavia, è un evento distinto dalle gare valide per il Mondiale e riunisce vetture e protagonisti contemporanei e storici; la presenza a San Marino non aggiunge punti alla classifica WRC2.",
                "Le due Ypsilon metteranno così nello stesso evento la stagione sportiva attuale e la tradizione Lancia rappresentata da Fulvia HF, Stratos, 037, Delta S4 e Delta Integrale. L'apertura è fissata per l'8 ottobre, con il programma concentrato fino a domenica 11.",
            ],
            "fonti": [{
                "url": "https://www.media.stellantis.com/em-en/lancia-corse/press/lancia-corse-hf-heads-to-rallylegend-with-two-lancia-ypsilon-rally2-hf-integrale-gryazin-and-somaschini-to-take-part",
                "nome": "Lancia Corse HF — comunicato ufficiale su equipaggi, vetture e programma di Rallylegend.",
            }],
            "image": image_record(
                "rallylegend-somaschini-lancia-rally2-gryazin-07-10-2026", IMAGES["rally"],
                "Illustrazione editoriale IA di Nikolay Gryazin e Rachele Somaschini davanti a due Lancia Ypsilon Rally2 a San Marino; scena non documentaria.",
                "Nikolay Gryazin e Rachele Somaschini, volti visibili, davanti a due Lancia Ypsilon Rally2 HF Integrale a San Marino, fotografia motorsportiva fotorealistica, nessun testo aggiunto.",
                public=True,
            ),
            "published": now - timedelta(minutes=2),
        },
        {
            "slug": "cinema-italia-francia-gruppo-esperti-mia-07-10-2026",
            "titolo": "Cinema europeo, Italia e Francia avviano un gruppo sulle nuove regole",
            "sommario": (
                "La prima riunione si terrà al MIA di Roma dal 19 al 23 ottobre. "
                "Al centro sostegni alla produzione, circolazione delle opere, concentrazioni e intelligenza artificiale."
            ),
            "luogo": "Roma",
            "categoria": "Film e serie TV",
            "formato": "flash",
            "parole_chiave_titolo": ["Italia e Francia", "nuove regole"],
            "dati_chiave": [
                {"icona": "◆", "valore": "19-23 ott", "etichetta": "date del MIA a Roma"},
                {"icona": "▲", "valore": "2 Paesi", "etichetta": "industrie coinvolte"},
                {"icona": "●", "valore": "12ª", "etichetta": "edizione del mercato audiovisivo"},
            ],
            "paragrafi": [
                "Italia e Francia istituiranno un gruppo di esperti dedicato alle politiche europee per cinema e audiovisivo. La prima riunione è prevista durante il Mercato Internazionale Audiovisivo di Roma, in programma dal 19 al 23 ottobre.",
                "L'organismo nasce dal programma di cooperazione rafforzata firmato ad Antibes il 25 giugno 2026 dai ministri della Cultura dei due Paesi. Riunirà rappresentanti istituzionali e professionisti per confrontare posizioni su norme europee, sostegni alla creazione e alla produzione e nuove modalità di distribuzione delle opere.",
                "L'annuncio è stato pubblicato il 7 ottobre dalla Direzione generale Cinema e audiovisivo del Ministero della Cultura. Il direttore generale Giorgio Carlo Brugnoni ha indicato l'obiettivo di mettere in comune competenze italiane e francesi per contribuire alle decisioni europee di settore.",
                "Il gruppo non è un nuovo fondo e non assegna automaticamente risorse alle produzioni. È uno spazio di coordinamento politico e tecnico: eventuali misure concrete dovranno passare attraverso i processi nazionali o dell'Unione europea previsti per ciascun intervento.",
                "Tra i nodi richiamati dal ministero ci sono la tutela della produzione indipendente, la circolazione internazionale dei contenuti e la valorizzazione delle identità culturali. Il confronto arriva mentre l'industria affronta concentrazioni societarie, cambiamenti nelle abitudini del pubblico e l'impatto dell'intelligenza artificiale sulla produzione audiovisiva.",
                "La prima riunione durante il MIA permetterà di trasformare l'accordo politico di giugno in un'agenda di lavoro. Non sono stati ancora comunicati l'elenco completo dei componenti, un calendario successivo o proposte normative già definite.",
                "La dodicesima edizione del MIA si svolgerà in parallelo alla Festa del Cinema di Roma e coinvolgerà Auditorium Parco della Musica, Casa del Cinema, Palazzo Barberini e altre sedi della città. Il prossimo elemento verificabile sarà quindi la composizione del gruppo e il contenuto della riunione di ottobre.",
            ],
            "fonti": [{
                "url": "https://cinema.cultura.gov.it/notizie/mia-al-via-il-gruppo-di-esperti-italo-francese-sulle-politiche-europee/",
                "nome": "Direzione generale Cinema e audiovisivo — annuncio ufficiale del gruppo italo-francese, 7 ottobre 2026.",
            }],
            "image": image_record(
                "cinema-italia-francia-gruppo-esperti-mia-07-10-2026", IMAGES["cinema"],
                "Illustrazione editoriale IA di professionisti italiani e francesi dell'audiovisivo riuniti a Roma; scena non documentaria.",
                "Professionisti italiani e francesi del cinema discutono in una sala ispirata a Palazzo Barberini con attrezzature audiovisive, fotografia editoriale fotorealistica, nessun testo.",
            ),
            "published": now - timedelta(minutes=1),
        },
        {
            "slug": "sole-quattro-regioni-attive-attivita-moderata-07-10-2026",
            "titolo": "Sole, quattro regioni attive e attività moderata il 7 ottobre",
            "sommario": (
                "INAF registra due brillamenti di classe M nella giornata precedente e nessuna perturbazione geomagnetica entro le 8:30. "
                "Un buco coronale può generare vento solare veloce."
            ),
            "luogo": "Italia",
            "categoria": "Scienza",
            "formato": "flash",
            "parole_chiave_titolo": ["quattro regioni attive", "attività moderata"],
            "dati_chiave": [
                {"icona": "◆", "valore": "4", "etichetta": "regioni attive visibili"},
                {"icona": "▲", "valore": "2", "etichetta": "brillamenti di classe M il 6 ottobre"},
                {"icona": "●", "valore": "0", "etichetta": "perturbazioni geomagnetiche entro le 8:30"},
            ],
            "paragrafi": [
                "Quattro regioni attive con macchie erano visibili sulla superficie del Sole il 7 ottobre 2026. Il bollettino quotidiano Sorvegliati Spaziali dell'Istituto nazionale di astrofisica classifica come moderato il livello dell'attività solare.",
                "Nella giornata del 6 ottobre gli strumenti hanno rilevato un brillamento di classe B, tredici di classe C e due di classe M. Fino alle 8:30 CEST del 7 ottobre erano stati registrati altri due brillamenti di classe C.",
                "La scala dei brillamenti procede dalle classi più deboli A e B verso C, M e X. Il passaggio alla classe M segnala eventi più energetici delle comuni emissioni di classe C, ma il bollettino non riporta per la mattina del 7 ottobre effetti geomagnetici sulla Terra.",
                "Il campo geomagnetico risultava infatti non perturbato entro l'orario di osservazione. Il dato descrive la situazione misurata nella prima parte della giornata e non costituisce una previsione valida per tutte le ore successive.",
                "INAF segnala inoltre attività magnetica localizzata sul lembo orientale del Sole, sia nell'emisfero nord sia in quello sud. Le mappe della parte non visibile dalla Terra indicano altre quattro regioni attive intense, che potranno ruotare verso il lato osservabile nei giorni successivi.",
                "Nell'emisfero sud, a est del meridiano centrale, è presente un buco coronale in grado di produrre flussi di vento solare veloce. La presenza della struttura non implica automaticamente una tempesta geomagnetica: direzione, velocità e interazione del flusso con il campo magnetico terrestre determinano l'eventuale risposta.",
                "Il monitoraggio resta utile per satelliti, comunicazioni radio e reti tecnologiche esposte agli eventi di meteorologia spaziale. Il quadro delle 8:30 è però quello di un Sole moderatamente attivo e di un ambiente geomagnetico terrestre ancora quieto.",
            ],
            "fonti": [{
                "url": "https://sorvegliatispaziali.inaf.it/il-sole-oggi-4/",
                "nome": "INAF Sorvegliati Spaziali — bollettino del Sole del 7 ottobre 2026.",
            }],
            "image": image_record(
                "sole-quattro-regioni-attive-attivita-moderata-07-10-2026", IMAGES["sole"],
                "Illustrazione editoriale IA di due ricercatori che osservano immagini del Sole in un osservatorio; scena non documentaria.",
                "Due ricercatori solari con volti visibili in un osservatorio italiano monitorano il disco solare e quattro regioni attive, fotografia scientifica fotorealistica, nessun testo leggibile.",
            ),
            "published": now,
        },
    ]

    for article in articles:
        article_path = ROOT / "notizie" / f"{article['slug']}.html"
        # Una precedente esecuzione interrotta può aver lasciato la sola pagina
        # prima della sincronizzazione: il lotto è idempotente e la rigenera.
        article_path.unlink(missing_ok=True)
        published = article["published"]
        site.write_article(article, article["image"], VERSION)
        register_image_once(article["image"], article["slug"])
        set_published(article["slug"], published)

    latest_url = f"/notizie/{articles[-1]['slug']}.html"
    site.sync_surfaces(articles, latest_url, VERSION, update_manifest=False)


if __name__ == "__main__":
    main()
