#!/usr/bin/env python3
"""Pubblica dieci notizie recenti da fonti primarie, senza usare il manifest."""
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

VERSION = 804
ROME = ZoneInfo("Europe/Rome")
CAPTION = site.CAPTION
GENERATED = ROOT.parent / "generated_images"

IMAGES = {
    "nobel": GENERATED / "exec-d547510e-bcd2-4ba9-be73-d736a7a9fca7.png",
    "chimici": GENERATED / "exec-ee3268af-5244-440f-9705-4d524cc85454.png",
    "allargamento": GENERATED / "exec-45efeefa-6c49-458b-9fe7-5aadabe7f83a.png",
    "kenya": GENERATED / "exec-2da31746-48bf-4866-917a-7587f909b72e.png",
    "amr": GENERATED / "exec-154aaa43-107e-4cdb-8aae-714fe01332a5.png",
    "mimit": GENERATED / "exec-9f185d56-0afa-4dc0-b8b4-ae60cb99c5b8.png",
    "pagamenti": GENERATED / "exec-4fd73d09-2471-49f4-bc01-3b2131f27ab7.png",
    "kids": GENERATED / "exec-8e1cc13d-1653-4efb-bead-b29c7544a68f.png",
    "fai": GENERATED / "exec-bc9803df-866a-43a4-be99-5261b96cfa2f.png",
    "pacemaker": GENERATED / "exec-2819be6c-4acf-41be-aa00-1668f3920fbb.png",
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
            "w": width, "h": height,
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return result


def image_record(slug: str, source: Path, alt: str, prompt: str, *, public=False, sensitive=False) -> dict:
    record = {
        "key": f"{slug}-v{VERSION}", "alt": alt, "prompt": prompt,
        "variants": variants(source, slug), "disclosure": CAPTION,
        "generator": "OpenAI image generation", "aiGenerated": True,
        "documentaryPhoto": False, "officialArtwork": False,
        "sensitiveContext": sensitive, "weatherMap": False,
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
            "slug": "pacemaker-autosincronizzante-pisa-escort-60-anni-08-10-2026",
            "titolo": "Pacemaker ESCORT, il prototipo pisano compie 60 anni",
            "sommario": "Nel 1966 il dispositivo del CNR imparò ad ascoltare il battito spontaneo e a intervenire solo quando serviva. Il prototipo entra ora in esposizione permanente a Pisa.",
            "luogo": "Pisa", "categoria": "Scienza", "formato": "flash",
            "parole_chiave_titolo": ["ESCORT", "60 anni"],
            "dati_chiave": [
                {"icona": "◆", "valore": "1966", "etichetta": "anno dei primi schemi"},
                {"icona": "▲", "valore": "20 casi", "etichetta": "entro la fine del 1966"},
                {"icona": "●", "valore": "60 anni", "etichetta": "dalla nascita del prototipo"},
            ],
            "paragrafi": [
                "Sessant'anni fa a Pisa nacque un pacemaker capace di riconoscere il battito spontaneo e di stimolare il cuore soltanto quando necessario. Il prototipo ESCORT, sviluppato nel 1966 da clinici ed elettronici del CNR, viene ora ricordato con un incontro pubblico e una nuova teca permanente al Museo degli Strumenti per il Calcolo.",
                "Il problema clinico fu posto da Luigi Donato, allora alla guida del gruppo di Fisiologia della Clinica Medica universitaria. Il giovane fisico Franco Denoth e i tecnici del Centro Studi Calcolatrici Elettroniche del CNR cercarono una soluzione che evitasse il conflitto fra ritmo naturale e impulso artificiale.",
                "L'idea decisiva era usare lo stesso filo per portare lo stimolo elettrico al cuore e per ascoltarne l'attività. Se il dispositivo rilevava un battito spontaneo, attendeva; in sua assenza interveniva con l'impulso programmato.",
                "I primi schemi risalgono al febbraio 1966 e la domanda di brevetto fu depositata in giugno. Entro la fine dell'anno ESCORT era stato utilizzato in 20 casi senza guasti registrati; il CNR ne produsse poi alcune decine per centri cardiologici italiani e stranieri.",
                "La valorizzazione industriale passò nel 1967 a Sorin Biomedica. Da allora la cardiostimolazione è arrivata a dispositivi miniaturizzati e senza fili, sensori impiantabili, monitoraggio remoto e strumenti di intelligenza artificiale per individuare le aritmie.",
                "La teca con il prototipo originale viene inaugurata l'8 ottobre alle 12 nella sezione Non solo calcolo del museo pisano, al termine dell'incontro Battiti Elettronici inserito nell'Internet Festival 2026.",
            ],
            "fonti": [{"url": "https://ifc.cnr.it/battiti-elettronici-a-pisa-60-anni-del-pacemaker-autosincronizzante-nato-al-cnr-di-pisa/", "nome": "CNR-Istituto di Fisiologia Clinica — storia del pacemaker ESCORT e programma dell'8 ottobre 2026."}],
            "image": image_record("pacemaker-autosincronizzante-pisa-escort-60-anni-08-10-2026", IMAGES["pacemaker"], "Illustrazione editoriale IA del prototipo ESCORT del 1966 accanto a un pacemaker moderno; scena non documentaria.", "Prototipo storico di pacemaker sotto teca accanto a dispositivo moderno in laboratorio museale, fotografia editoriale fotorealistica, nessun testo."),
            "published": now - timedelta(minutes=9),
        },
        {
            "slug": "banca-italia-apre-firenze-sassari-giornate-fai-08-10-2026",
            "titolo": "Banca d'Italia apre le filiali di Firenze e Sassari per il FAI",
            "sommario": "Le visite straordinarie sono in programma il 10 e l'11 ottobre. Orari diversi nelle due città per scoprire architettura e patrimonio delle sedi.",
            "luogo": "Firenze / Sassari", "categoria": "Cultura", "formato": "flash",
            "parole_chiave_titolo": ["Firenze e Sassari", "FAI"],
            "dati_chiave": [
                {"icona": "◆", "valore": "2 filiali", "etichetta": "aperte al pubblico"},
                {"icona": "▲", "valore": "10-11 ott", "etichetta": "giorni di visita"},
                {"icona": "●", "valore": "10:00", "etichetta": "inizio delle aperture"},
            ],
            "paragrafi": [
                "Le filiali della Banca d'Italia di Firenze e Sassari aprono al pubblico per le Giornate FAI d'Autunno 2026. Le visite straordinarie sono previste sabato 10 e domenica 11 ottobre, con fasce orarie differenti nelle due sedi.",
                "A Firenze l'appuntamento è in via dell'Oriuolo 37/39. La filiale sarà visitabile in entrambe le giornate dalle 10 alle 17.",
                "A Sassari l'ingresso è in largo Molino a Vento 2. Sabato 10 l'apertura va dalle 10 alle 18, mentre domenica 11 termina alle 13.",
                "L'iniziativa permette di entrare in edifici normalmente legati all'attività istituzionale della banca centrale e di osservarne spazi, architettura e patrimonio culturale. Le modalità concrete di accesso e gli eventuali turni sono pubblicati nelle schede locali del FAI.",
                "La Banca d'Italia partecipa alle giornate nazionali dedicate a luoghi storici e culturali con queste due aperture. Chi intende visitarle deve quindi verificare sul sito FAI la disponibilità aggiornata prima di partire.",
            ],
            "fonti": [
                {"url": "https://www.bancaditalia.it/media/notizia/giornate-fai-d-autunno-2026/", "nome": "Banca d'Italia — sedi, indirizzi e orari delle aperture FAI 2026."},
                {"url": "https://fondoambiente.it/il-fai/grandi-campagne/giornate-fai-autunno/", "nome": "FAI — programma nazionale delle Giornate d'Autunno 2026 e informazioni per le visite."},
            ],
            "image": image_record("banca-italia-apre-firenze-sassari-giornate-fai-08-10-2026", IMAGES["fai"], "Illustrazione editoriale IA di visitatori in una storica sede bancaria italiana; scena non documentaria.", "Visitatori adulti guidati in un grande atrio bancario storico italiano, fotografia editoriale fotorealistica, nessun testo o logo."),
            "published": now - timedelta(minutes=8),
        },
        {
            "slug": "eu-kids-act-consultazione-online-sicurezza-minori-08-10-2026",
            "titolo": "EU Kids Act, consultazione aperta fino al 26 novembre",
            "sommario": "La Commissione raccoglie osservazioni da minori, famiglie, insegnanti e piattaforme. La proposta prevede rinvio dell'accesso ai social e verifiche dell'età rispettose della privacy.",
            "luogo": "Bruxelles", "categoria": "Tecnologia", "formato": "flash",
            "parole_chiave_titolo": ["26 novembre", "consultazione"],
            "dati_chiave": [
                {"icona": "◆", "valore": "26 nov", "etichetta": "termine per i contributi"},
                {"icona": "▲", "valore": "5 gruppi", "etichetta": "chiamati a partecipare"},
                {"icona": "●", "valore": "1 sintesi", "etichetta": "destinata a Parlamento e Consiglio"},
            ],
            "paragrafi": [
                "La Commissione europea ha aperto la raccolta di osservazioni sull'EU Kids Act, la proposta dedicata alla sicurezza dei minori online. I contributi possono essere inviati fino alla mezzanotte di Bruxelles del 26 novembre 2026.",
                "La consultazione è rivolta direttamente a bambini e ragazzi, genitori, tutori, insegnanti ed educatori, oltre alle piattaforme online interessate dalle nuove regole. Le risposte saranno riassunte dalla Commissione e trasmesse al Parlamento europeo e al Consiglio per alimentare il confronto legislativo.",
                "La proposta, adottata a settembre, introduce un rinvio dell'accesso ai social media per i più giovani, obblighi di sicurezza fin dalla progettazione dei servizi e sistemi di verifica dell'età pensati per preservare la privacy.",
                "Il testo punta anche a rendere effettiva l'applicazione delle norme. Le misure dovranno quindi essere valutate insieme agli obblighi già esistenti per le piattaforme e alle soluzioni tecniche necessarie per distinguere le fasce d'età senza raccogliere più dati del necessario.",
                "La Commissione precisa che la fase di feedback si aggiunge alle consultazioni già svolte con minori, famiglie ed educatori e alla ricerca europea sulle esperienze online dei più giovani pubblicata nel 2026.",
                "La consultazione non conclude l'iter: serve a raccogliere elementi prima delle decisioni dei due colegislatori dell'Unione. Fino al 26 novembre, cittadini e soggetti interessati possono usare il portale europeo dedicato.",
            ],
            "fonti": [{"url": "https://digital-strategy.ec.europa.eu/en/news/commission-seeks-feedback-eu-kids-act", "nome": "Commissione europea — avviso ufficiale sulla consultazione EU Kids Act, aggiornato il 5 ottobre 2026."}],
            "image": image_record("eu-kids-act-consultazione-online-sicurezza-minori-08-10-2026", IMAGES["kids"], "Illustrazione editoriale IA di una madre e un adolescente che controllano insieme le impostazioni di sicurezza online; scena non documentaria.", "Genitore e adolescente controllano insieme impostazioni di sicurezza su tablet in casa, fotografia editoriale fotorealistica, schermo illeggibile."),
            "published": now - timedelta(minutes=7),
        },
        {
            "slug": "pagamenti-italiani-profili-ia-banca-italia-contante-digitale-08-10-2026",
            "titolo": "Pagamenti in Italia, il 24% dei consumatori non usa contante",
            "sommario": "Banca d'Italia combina diari di spesa e intelligenza artificiale per definire cinque profili. Solo il 15% risulta pienamente integrato nell'economia digitale.",
            "luogo": "Roma", "categoria": "Economia", "formato": "flash",
            "parole_chiave_titolo": ["24%", "non usa contante"],
            "dati_chiave": [
                {"icona": "◆", "valore": "24%", "etichetta": "non usa contante"},
                {"icona": "▲", "valore": "15%", "etichetta": "integrato nel digitale"},
                {"icona": "●", "valore": "5 profili", "etichetta": "comportamentali individuati"},
            ],
            "paragrafi": [
                "Quasi un consumatore italiano su quattro non usa contante, ma soltanto il 15% risulta pienamente integrato nell'economia digitale. È il quadro che emerge da un nuovo studio della Banca d'Italia, costruito combinando diari di pagamento, valutazione umana e tecniche di intelligenza artificiale.",
                "I ricercatori hanno definito cinque profili che coprono l'intero spettro delle abitudini, dall'uso prevalente del contante alle soluzioni digitali più avanzate. I partecipanti all'indagine SPACE 2024 dell'Eurosistema sono stati poi assegnati ai gruppi con una procedura che integra modelli linguistici e apprendimento supervisionato.",
                "La maggioranza mantiene un comportamento tradizionale: usa contante e carte nei punti vendita fisici, ma ricorre poco ai pagamenti a distanza. Abbandonare il contante, quindi, non coincide automaticamente con l'adozione degli strumenti più innovativi.",
                "Il 7% si affida soprattutto alle banconote e alle monete. Un ulteriore 4% usa esclusivamente una combinazione di contante e carte prepagate.",
                "I profili differiscono anche per età: fra gli utenti inseriti nell'ecosistema digitale ci sono più giovani, mentre nel gruppo orientato al contante prevalgono gli anziani. Il dato segnala una transizione non uniforme fra generazioni e abitudini quotidiane.",
                "Secondo lo studio, le politiche sui pagamenti — comprese quelle relative alle valute digitali delle banche centrali — dovrebbero tenere conto di questa eterogeneità, evitando di considerare tutti i consumatori allo stesso punto del percorso digitale.",
            ],
            "fonti": [
                {"url": "https://www.bancaditalia.it/media/notizia/come-paghi-profilazione-dei-consumatori-tramite-diari-di-pagamento-e-intelligenza-artificiale/", "nome": "Banca d'Italia — sintesi dello studio Come paghi?, 6 ottobre 2026."},
                {"url": "https://www.bancaditalia.it/pubblicazioni/mercati-infrastrutture-e-sistemi-di-pagamento/approfondimenti/2026-095/", "nome": "Banca d'Italia — studio MISP numero 95 con metodo e risultati completi."},
            ],
            "image": image_record("pagamenti-italiani-profili-ia-banca-italia-contante-digitale-08-10-2026", IMAGES["pagamenti"], "Illustrazione editoriale IA di consumatori che pagano con contante, carta e smartphone in un locale italiano; scena non documentaria.", "Consumatori adulti pagano con contante, carta e smartphone in un bar italiano, fotografia editoriale fotorealistica, nessun testo o logo."),
            "published": now - timedelta(minutes=6),
        },
        {
            "slug": "investimenti-sostenibili-4-0-fondi-esauriti-sportello-chiuso-08-10-2026",
            "titolo": "Investimenti sostenibili 4.0, sportello chiuso per fondi esauriti",
            "sommario": "Dal 7 ottobre non si possono più presentare domande per la misura destinata alle PMI del Mezzogiorno. La dotazione superava 447,5 milioni di euro.",
            "luogo": "Roma", "categoria": "Economia", "formato": "flash",
            "parole_chiave_titolo": ["sportello chiuso", "fondi esauriti"],
            "dati_chiave": [
                {"icona": "◆", "valore": "447,6 mln €", "etichetta": "dotazione complessiva"},
                {"icona": "▲", "valore": "25%", "etichetta": "riservato a micro e piccole imprese"},
                {"icona": "●", "valore": "7 regioni", "etichetta": "del Mezzogiorno ammesse"},
            ],
            "paragrafi": [
                "Lo sportello di Investimenti sostenibili 4.0 è chiuso dal 7 ottobre 2026 dopo l'esaurimento delle risorse finanziarie. Il Ministero delle Imprese e del Made in Italy ha fermato la presentazione di nuove domande con un decreto direttoriale del 6 ottobre.",
                "La misura disponeva di 447.595.808,76 euro per sostenere programmi innovativi e tecnologicamente avanzati delle piccole e medie imprese del Mezzogiorno. Il 25% della dotazione era riservato ai progetti proposti da micro e piccole imprese.",
                "Potevano partecipare aziende con unità produttive in Basilicata, Calabria, Campania, Molise, Puglia, Sicilia e Sardegna. Gli investimenti dovevano usare in misura prevalente tecnologie del piano Transizione 4.0 e contribuire anche alla sostenibilità ambientale.",
                "I programmi ammissibili partivano da 750.000 euro e potevano arrivare a 5 milioni, senza superare il 70% del fatturato dell'ultimo bilancio o dell'ultima dichiarazione disponibile. Il termine di realizzazione era fissato entro 18 mesi dalla concessione.",
                "La chiusura riguarda soltanto l'invio di nuove richieste. Le domande già presentate restano soggette all'istruttoria e alle regole previste dal bando; l'esaurimento dello stanziamento non equivale all'accoglimento automatico di tutte le istanze.",
                "Il Ministero non ha indicato una data di riapertura. Le imprese interessate devono quindi fare riferimento agli aggiornamenti ufficiali della misura per eventuali rifinanziamenti o nuove finestre.",
            ],
            "fonti": [{"url": "https://www.mimit.gov.it/it/incentivi/investimenti-sostenibili-4-0-2026", "nome": "Ministero delle Imprese e del Made in Italy — scheda ufficiale e avviso di chiusura del 6 ottobre 2026."}],
            "image": image_record("investimenti-sostenibili-4-0-fondi-esauriti-sportello-chiuso-08-10-2026", IMAGES["mimit"], "Illustrazione editoriale IA di una PMI del Mezzogiorno con robotica e impianti solari; scena non documentaria.", "Manager e ingegnera in fabbrica robotizzata sostenibile del Sud Italia, fotografia editoriale fotorealistica, nessun testo o logo."),
            "published": now - timedelta(minutes=5),
        },
        {
            "slug": "resistenza-antimicrobica-asia-pacifico-piani-senza-fondi-08-10-2026",
            "titolo": "Resistenza antimicrobica, quasi metà dei piani non ha costi stimati",
            "sommario": "L'analisi di 28 Paesi dell'Asia-Pacifico mostra strategie più solide ma finanziamenti insufficienti. Solo otto coprono tutte le attività con risorse nazionali.",
            "luogo": "Manila / Tokyo / Nuova Delhi", "categoria": "Scienza", "formato": "flash",
            "parole_chiave_titolo": ["quasi metà", "senza costi stimati"],
            "dati_chiave": [
                {"icona": "◆", "valore": "49%", "etichetta": "piani senza stima dei costi"},
                {"icona": "▲", "valore": "8 Paesi", "etichetta": "con pieno finanziamento nazionale"},
                {"icona": "●", "valore": "28 Paesi", "etichetta": "inclusi nell'analisi"},
            ],
            "paragrafi": [
                "I Paesi dell'Asia-Pacifico stanno costruendo piani più completi contro la resistenza antimicrobica, ma quasi metà delle strategie nazionali non contiene ancora una stima dei costi. L'analisi riguarda dati pubblicati da 28 Paesi e misura i progressi verso gli obiettivi fissati dalle Nazioni Unite per il 2030.",
                "Ventisette Paesi hanno approvato almeno un piano multisettoriale. Quattordici sono già alla seconda generazione e tre alla terza, segno che l'organizzazione della risposta sta diventando più strutturata.",
                "I secondi piani hanno più probabilità di essere quantificati economicamente rispetto ai primi: 67% contro 33%. Includono inoltre più spesso sistemi di monitoraggio, 93% contro 33%, e obiettivi misurabili, 71% contro 8%.",
                "Il salto di qualità non è però accompagnato da risorse equivalenti. Il 49% dei 27 piani non è affatto costificato, il 44% lo è integralmente e il 7% soltanto in parte.",
                "Solo otto Paesi dichiarano di finanziare interamente le attività con risorse nazionali. In 15 casi la quota domestica copre meno del 30% del fabbisogno complessivo, aumentando la dipendenza dai partner esterni.",
                "Restano lacune anche nella prevenzione: soltanto 16 Paesi su 28 riferiscono servizi essenziali di acqua, igiene e sanificazione in oltre tre quarti delle strutture sanitarie. Nove superano il 70% di uso degli antibiotici del gruppo Access, quelli a spettro più ristretto indicati per molte infezioni comuni.",
                "Il comunicato congiunto dell'OMS e del governo giapponese invita a finanziare pienamente i piani, ampliare i servizi igienici nelle strutture sanitarie, rafforzare la sorveglianza e migliorare l'uso degli antibiotici. La resistenza antimicrobica riduce infatti l'efficacia dei farmaci contro le infezioni.",
            ],
            "fonti": [
                {"url": "https://www.who.int/southeastasia/news/detail/06-10-2026-asia-pacific-countries-sharpen-plans-to-fight-antimicrobial-resistance--but-most-remain-unfunded", "nome": "OMS Asia sud-orientale e Pacifico occidentale — comunicato congiunto del 6 ottobre 2026."},
                {"url": "https://bmjpublichealth.bmj.com/content/4/1/e004693", "nome": "BMJ Public Health — studio regionale sui piani nazionali contro la resistenza antimicrobica."},
            ],
            "image": image_record("resistenza-antimicrobica-asia-pacifico-piani-senza-fondi-08-10-2026", IMAGES["amr"], "Illustrazione editoriale IA di ricercatori dell'Asia-Pacifico che analizzano colture batteriche e piani sanitari; scena non documentaria.", "Ricercatori adulti in laboratorio analizzano colture batteriche con documenti di pianificazione, fotografia editoriale fotorealistica, nessun testo."),
            "published": now - timedelta(minutes=4),
        },
        {
            "slug": "kenya-primo-caso-importato-virus-bundibugyo-contatti-08-10-2026",
            "titolo": "Kenya, primo caso importato di Bundibugyo: 55 persone da seguire",
            "sommario": "Il paziente era arrivato dalla Repubblica Democratica del Congo ed è morto il 5 ottobre. Le autorità tracciano 28 contatti, 23 passeggeri e quattro membri dell'equipaggio.",
            "luogo": "Nairobi", "categoria": "Scienza", "formato": "flash",
            "parole_chiave_titolo": ["primo caso importato", "55 persone"],
            "dati_chiave": [
                {"icona": "◆", "valore": "1 caso", "etichetta": "primo importato in Kenya"},
                {"icona": "▲", "valore": "55 persone", "etichetta": "fra contatti, passeggeri ed equipaggio"},
                {"icona": "●", "valore": "652.584", "etichetta": "viaggiatori già controllati"},
            ],
            "paragrafi": [
                "Il Kenya ha confermato il primo caso importato di malattia da virus Bundibugyo nel Paese. Il paziente, cittadino kenyano residente nella Repubblica Democratica del Congo, era arrivato a Nairobi il 3 ottobre ed è morto nella notte del 5 dopo il ricovero in isolamento.",
                "La diagnosi è stata confermata in modo indipendente dal National Virology Reference Laboratory e dal Kenya Medical Research Institute. Le autorità hanno notificato il caso all'Organizzazione mondiale della sanità il 6 ottobre secondo il Regolamento sanitario internazionale.",
                "Sono stati identificati 28 contatti fra familiari e operatori sanitari. Il tracciamento comprende inoltre 23 passeggeri e quattro membri dell'equipaggio del volo con cui il paziente è arrivato da Kampala: in totale 55 persone da valutare e seguire secondo il livello di esposizione.",
                "Il paziente si era ammalato nella Repubblica Democratica del Congo e aveva attraversato su strada Beni e Kampala il 2 ottobre. Dopo l'atterraggio a Nairobi è stato portato in ospedale e rapidamente isolato.",
                "Il Kenya era in allerta da maggio per i focolai regionali. Al 6 ottobre aveva sottoposto a screening 652.584 viaggiatori, analizzato 267 campioni e formato 4.971 operatori sanitari nella prevenzione e nella gestione dell'Ebola.",
                "Il virus Bundibugyo si trasmette attraverso il contatto diretto con sangue o fluidi corporei di una persona infetta o con materiali contaminati. Non esistono vaccini o trattamenti specifici approvati per questa specie, anche se sono in valutazione prodotti candidati; le cure disponibili sono di supporto.",
                "L'OMS non raccomanda restrizioni ai viaggi o agli scambi commerciali con Kenya, Uganda o Repubblica Democratica del Congo sulla base delle informazioni disponibili. La priorità resta individuare rapidamente eventuali nuovi casi e interrompere possibili catene di trasmissione.",
            ],
            "fonti": [
                {"url": "https://health.go.ke/kenya-confirms-first-imported-case-bundibugyo-ebola-virus-disease", "nome": "Ministero della Salute del Kenya — conferma ufficiale del primo caso importato, 6 ottobre 2026."},
                {"url": "https://afro.who.int/countries/kenya/news/kenya-confirms-first-imported-bundibugyo-virus-disease-case-who-supports-control-efforts", "nome": "OMS Africa — aggiornamento su tracciamento, preparazione e raccomandazioni di viaggio."},
            ],
            "image": image_record("kenya-primo-caso-importato-virus-bundibugyo-contatti-08-10-2026", IMAGES["kenya"], "Illustrazione editoriale IA di operatori sanitari in un punto di controllo ospedaliero in Kenya; scena non documentaria.", "Operatori sanitari in dispositivi di protezione controllano campioni sigillati all'ingresso di un ospedale kenyano, fotografia editoriale fotorealistica.", sensitive=True),
            "published": now - timedelta(minutes=3),
        },
        {
            "slug": "ue-allargamento-misure-voto-maggioranza-salvaguardie-08-10-2026",
            "titolo": "Allargamento UE, la Commissione propone più voto a maggioranza",
            "sommario": "Il pacchetto punta a rendere più rapide alcune decisioni negoziali e introduce salvaguardie per i futuri trattati di adesione. Roadmap previste per quattro Paesi candidati.",
            "luogo": "Bruxelles", "categoria": "Mondo", "formato": "flash",
            "parole_chiave_titolo": ["voto a maggioranza", "allargamento UE"],
            "dati_chiave": [
                {"icona": "◆", "valore": "4 roadmap", "etichetta": "per Paesi candidati"},
                {"icona": "▲", "valore": "4 settori", "etichetta": "per l'integrazione graduale"},
                {"icona": "●", "valore": "Articolo 7", "etichetta": "procedure da rendere più efficaci"},
            ],
            "paragrafi": [
                "La Commissione europea propone di usare più spesso il voto a maggioranza qualificata per preparare l'Unione a futuri allargamenti. Le nuove misure riguardano governo, politiche e bilancio e puntano a evitare che l'ingresso di altri Stati rallenti ulteriormente le decisioni comuni.",
                "Il pacchetto indica la possibilità di superare l'unanimità in aree chiave già consentite dai trattati, compresa l'apertura dei gruppi negoziali con i Paesi candidati. Non è una modifica immediata delle regole: la Commissione invita Consiglio europeo e Parlamento ad avviare il confronto istituzionale.",
                "Un secondo intervento riguarda le procedure dell'articolo 7 contro le violazioni gravi dei valori dell'Unione. Bruxelles propone una gestione più efficace, anche attraverso tempi definiti.",
                "Per i futuri trattati di adesione sono previste salvaguardie specifiche. Nei casi più seri di violazione dei valori fondamentali o del principio di leale cooperazione potrebbe essere sospeso il diritto di voto in Consiglio.",
                "La Commissione vuole anche integrare gradualmente i candidati in energia, trasporti, digitale e difesa, accompagnando il percorso con dialoghi annuali. Potranno essere usati periodi transitori per libera circolazione dei lavoratori e dei servizi, agricoltura, prodotti sensibili, fondi e sistemi comuni.",
                "Secondo l'analisi dell'esecutivo europeo, l'attuale quadro dei trattati e del bilancio può accogliere nuovi membri, ma servono più capacità amministrativa e strumenti di attuazione. Le priorità esistenti dovrebbero continuare a essere finanziate.",
                "I prossimi passaggi comprendono roadmap per Montenegro, Albania, Moldova e Ucraina. I negoziati di adesione restano separati e dipendono dai progressi di ciascun Paese: le nuove misure preparano l'Unione, non fissano una data d'ingresso.",
            ],
            "fonti": [
                {"url": "https://commission.europa.eu/news-and-media/news/preparing-wider-european-union-2026-10-06_en", "nome": "Commissione europea — sintesi delle misure per preparare un'Unione più ampia, 6 ottobre 2026."},
                {"url": "https://ec.europa.eu/commission/presscorner/detail/en/ip_26_4786", "nome": "Commissione europea — comunicato ufficiale sul pacchetto di preparazione all'allargamento."},
            ],
            "image": image_record("ue-allargamento-misure-voto-maggioranza-salvaguardie-08-10-2026", IMAGES["allargamento"], "Illustrazione editoriale IA di una sala negoziale europea preparata per l'allargamento; scena non documentaria.", "Sala negoziale europea vuota con tavolo circolare, bandiere e mappa luminosa dell'Europa, fotografia editoriale fotorealistica, nessun testo."),
            "published": now - timedelta(minutes=2),
        },
        {
            "slug": "ue-limiti-esposizione-chimici-lavoratori-cobalto-08-10-2026",
            "titolo": "Sostanze chimiche sul lavoro, l'UE fissa nuovi limiti di esposizione",
            "sommario": "Il Parlamento approva valori più severi per agenti usati in batterie, acciaio, chimica e tessile. Le nuove regole chiariscono anche l'impiego dei dispositivi di protezione.",
            "luogo": "Strasburgo", "categoria": "Mondo", "formato": "flash",
            "parole_chiave_titolo": ["nuovi limiti", "esposizione"],
            "dati_chiave": [
                {"icona": "◆", "valore": "1.700", "etichetta": "casi di tumore polmonare da prevenire"},
                {"icona": "▲", "valore": "4 settori", "etichetta": "industriali interessati"},
                {"icona": "●", "valore": "3 letture", "etichetta": "per misurare l'esposizione"},
            ],
            "paragrafi": [
                "Il Parlamento europeo ha approvato nuove soglie per proteggere i lavoratori esposti a sostanze chimiche pericolose. Le regole interessano in particolare attività legate a batterie, acciaio, industria chimica e tessile e rafforzano le indicazioni sui dispositivi di protezione individuale.",
                "Il provvedimento aggiorna le norme europee sugli agenti cancerogeni, mutageni e tossici per la riproduzione. Introduce o riduce valori limite professionali per sostanze presenti nei processi industriali, fra cui composti del cobalto e idrocarburi policiclici aromatici.",
                "Le soglie indicano la concentrazione massima alla quale un lavoratore può essere esposto nell'aria durante periodi definiti. Servono ai datori di lavoro per organizzare misurazioni, ventilazione, contenimento dei processi e protezioni aggiuntive.",
                "Il testo chiarisce che i dispositivi individuali non sostituiscono gli interventi alla fonte. Prima vengono eliminazione o sostituzione dell'agente pericoloso, impianti chiusi e aspirazione; maschere, guanti e tute completano le misure quando resta un rischio residuo.",
                "Secondo la stima citata dalle istituzioni europee, le modifiche potrebbero contribuire a prevenire circa 1.700 casi di tumore polmonare. Il beneficio dipende però dal rispetto concreto delle soglie e dai controlli nei luoghi di lavoro.",
                "Dopo l'approvazione parlamentare, gli Stati membri dovranno recepire le prescrizioni nei tempi previsti dalla direttiva. Le imprese interessate dovranno quindi adeguare valutazioni del rischio, monitoraggio e procedure operative alle nuove soglie.",
            ],
            "fonti": [
                {"url": "https://www.europarl.europa.eu/news/en/press-room/20261002IPR47899/updated-rules-to-protect-workers-from-exposure-to-dangerous-chemicals", "nome": "Parlamento europeo — comunicato sulle nuove regole contro l'esposizione professionale a sostanze pericolose, 6 ottobre 2026."},
                {"url": "https://european-union.europa.eu/index_en", "nome": "Portale ufficiale dell'Unione europea — sintesi della misura e stima dei casi prevenibili."},
            ],
            "image": image_record("ue-limiti-esposizione-chimici-lavoratori-cobalto-08-10-2026", IMAGES["chimici"], "Illustrazione editoriale IA di un lavoratore protetto in un impianto industriale europeo; scena non documentaria.", "Lavoratore adulto con respiratore, guanti, occhiali e casco controlla linea industriale sigillata, fotografia editoriale fotorealistica, nessun testo."),
            "published": now - timedelta(minutes=1),
        },
        {
            "slug": "nobel-chimica-2026-kagan-soai-sintesi-asimmetrica-08-10-2026",
            "titolo": "Nobel per la Chimica 2026 a Kagan e Soai per la sintesi asimmetrica",
            "sommario": "Il premio riconosce gli effetti non lineari e l'autocatalisi asimmetrica. Le loro ricerche hanno mostrato come piccole differenze molecolari possano amplificarsi.",
            "luogo": "Stoccolma", "categoria": "Scienza", "formato": "flash",
            "parole_chiave_titolo": ["Kagan e Soai", "sintesi asimmetrica"],
            "dati_chiave": [
                {"icona": "◆", "valore": "2 premiati", "etichetta": "Henri B. Kagan e Kenso Soai"},
                {"icona": "▲", "valore": "1 reazione", "etichetta": "capace di autoamplificarsi"},
                {"icona": "●", "valore": "7 ott", "etichetta": "giorno dell'annuncio"},
            ],
            "paragrafi": [
                "Il Nobel per la Chimica 2026 è stato assegnato congiuntamente a Henri B. Kagan e Kenso Soai per gli effetti non lineari e l'autocatalisi asimmetrica nella sintesi organica. L'annuncio della Royal Swedish Academy of Sciences è arrivato il 7 ottobre a Stoccolma.",
                "Molte molecole esistono in due forme speculari, simili a una mano destra e una sinistra. In chimica e in biologia le due versioni possono avere effetti diversi, perciò produrre selettivamente quella desiderata è essenziale per farmaci, materiali e altre sintesi complesse.",
                "Kagan ha mostrato che una piccola differenza iniziale fra le due forme può produrre un risultato molto più grande del previsto. Questi effetti non lineari hanno dato ai chimici uno strumento per capire e controllare l'amplificazione della chiralità.",
                "Soai ha scoperto una reazione autocatalitica asimmetrica in cui il prodotto aiuta a formare altro prodotto della stessa configurazione. Il processo può quindi rafforzare progressivamente uno squilibrio molecolare inizialmente minimo.",
                "Insieme, i due filoni spiegano come la selettività possa emergere e autoamplificarsi in un sistema chimico. Il valore della ricerca non sta in una sola applicazione commerciale, ma in un principio generale usato per progettare reazioni più precise.",
                "Il premio sarà consegnato il 10 dicembre, anniversario della morte di Alfred Nobel. I due scienziati condivideranno il riconoscimento secondo le modalità stabilite dall'Accademia.",
            ],
            "fonti": [
                {"url": "https://www.nobelprize.org/prizes/chemistry/2026/summary/", "nome": "Nobel Prize — motivazione e riepilogo ufficiale del premio per la Chimica 2026."},
                {"url": "https://www.kva.se/en/news/the-nobel-prize-in-chemistry-2026/", "nome": "Royal Swedish Academy of Sciences — comunicato ufficiale sui laureati e sul contributo scientifico."},
            ],
            "image": image_record("nobel-chimica-2026-kagan-soai-sintesi-asimmetrica-08-10-2026", IMAGES["nobel"], "Illustrazione editoriale IA di Henri B. Kagan e Kenso Soai in un laboratorio di chimica; scena non documentaria.", "Henri B. Kagan e Kenso Soai riconoscibili insieme in laboratorio con modelli molecolari chirali, fotografia editoriale fotorealistica, nessun testo o logo.", public=True),
            "published": now,
        },
    ]

    for article in articles:
        article_path = ROOT / "notizie" / f"{article['slug']}.html"
        article_path.unlink(missing_ok=True)
        published = article["published"]
        site.write_article(article, article["image"], VERSION)
        register_image_once(article["image"], article["slug"])
        set_published(article["slug"], published)

    latest_url = f"/notizie/{articles[-1]['slug']}.html"
    site.sync_surfaces(articles, latest_url, VERSION, update_manifest=False)


if __name__ == "__main__":
    main()
