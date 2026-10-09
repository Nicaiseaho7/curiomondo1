#!/usr/bin/env python3
"""Release v817: dieci ultimissime italiane del 9 ottobre 2026."""
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

VERSION = 817
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"

IMAGE_SOURCES = {
    "lotteria": GENERATED / "exec-bc28b3f0-5c2a-4325-a0f8-3e6ee6c50ee5.png",
    "riparazione": GENERATED / "exec-a86abe34-3aab-4069-b30e-5cbd20694963.png",
    "meraviglia": GENERATED / "exec-845db51b-d1bf-4229-b473-8f41b539cd6f.png",
    "archivi": GENERATED / "exec-5d246ff9-3f41-42ea-b5fe-9829c9bf0210.png",
    "firenze_famu": GENERATED / "exec-ba09e451-0098-4819-8b36-2a83eaa80a3f.png",
    "egnazia": GENERATED / "exec-c39bb797-ddb0-4a60-aabf-3df822a2d8a8.png",
    "chiaroscuro": GENERATED / "exec-e1e20936-00ef-4bfe-b2f5-e91b38700af4.png",
    "vespucci": GENERATED / "exec-6d6e4c13-5ea3-4ce3-a178-dc8db2cf219a.png",
    "italia_cultura": GENERATED / "exec-1717b5e9-114d-472a-a475-b0cbf7d53908.png",
    "biblioteca_roma": GENERATED / "exec-5055a2b6-35a6-4158-b893-6f4e91b5be09.png",
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
        "sensitiveContext": False,
        "weatherMap": False,
        "reenactedEvent": False,
    }
    if article["slug"].startswith("chiaroscuro-"):
        image["syntheticLikeness"] = "public-figure"
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
        "Concediti il tempo di controllare bene prima di decidere.",
        "Puoi scegliere la soluzione che ti fa spendere meno energia.",
        "Oggi fai una cosa utile e poi fermati senza sensi di colpa.",
        "Se un programma cambia, puoi riorganizzarti con calma.",
        "Chiedere informazioni precise è un modo concreto di proteggerti.",
        "Puoi rimandare ciò che non richiede davvero una risposta oggi.",
        "Una pausa breve può aiutarti a vedere meglio la prossima scelta.",
        "Tieni vicino ciò che ti serve e lascia andare il resto.",
        "Hai il diritto di capire le condizioni prima di accettarle.",
        "Scegli un appuntamento che ti lasci anche il tempo di respirare.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


ARTICLES = [
    {
        "slug": "lotteria-italia-biglietto-vincente-acireale-8-ottobre-2026",
        "titolo": "Lotteria Italia, ad Acireale il biglietto da 10 mila euro",
        "sommario": "Il premio giornaliero dell'8 ottobre va al tagliando F 251917. La verifica è disponibile sul sito ufficiale e nell'app My Lotteries.",
        "categoria": "Economia", "luogo": "Acireale", "formato": "flash",
        "parole_chiave_titolo": ["Lotteria Italia", "Acireale"],
        "dati_chiave": [
            {"valore": "F 251917", "etichetta": "serie e numero vincente"},
            {"valore": "10.000 euro", "etichetta": "premio giornaliero"},
            {"valore": "13 dicembre", "etichetta": "termine per registrare i biglietti"},
        ],
        "paragrafi": [
            "Il biglietto F 251917, venduto ad Acireale in provincia di Catania, ha vinto il premio giornaliero da 10.000 euro della Lotteria Italia comunicato nella puntata di Affari tuoi dell'8 ottobre. L'elenco ufficiale è stato aggiornato il 9 ottobre 2026.",
            "Il titolare deve verificare il tagliando attraverso il sito Lotteria Italia o l'app My Lotteries e seguire la procedura di riscossione. Per un biglietto cartaceo servono l'originale integro, documento d'identità, codice fiscale e IBAN.",
            "I premi giornalieri da 10.000 euro proseguono fino al 20 dicembre; dal 21 al 27 dicembre l'importo indicato dal regolamento sale a 20.000 euro. Per concorrere è obbligatorio registrare il biglietto entro le 23:59 del 13 dicembre.",
            "La comunicazione televisiva non sostituisce il controllo personale. Chi possiede un tagliando dovrebbe confrontare serie e numero soltanto con gli strumenti ufficiali, evitando messaggi o siti che chiedono pagamenti per sbloccare una vincita.",
        ],
        "fonti": [{"url": "https://www.lotteria-italia.it/news/2026/8-ottobre-premio-giornaliero-lotteria-italia", "nome": "Lotteria Italia — biglietto vincente dell'8 ottobre e modalità di verifica."}],
        "image_source": "lotteria",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un biglietto della Lotteria Italia ad Acireale con l'Etna sullo sfondo; scena non documentaria.",
        "image_prompt": "Biglietto Lotteria Italia in un locale di Acireale con Etna e architettura barocca, illustrazione editoriale ultrarealistica, nessun numero vincente visibile.",
    },
    {
        "slug": "diritto-riparazione-beni-decreto-22-ottobre-2026",
        "titolo": "Diritto alla riparazione, nuove regole in vigore dal 22 ottobre",
        "sommario": "Il decreto aggiorna il Codice del consumo: preventivo standard, prezzi ragionevoli e accesso ai ricambi per i prodotti coperti.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Diritto alla riparazione", "22 ottobre"],
        "dati_chiave": [
            {"valore": "22 ottobre", "etichetta": "entrata in vigore"},
            {"valore": "30 giorni", "etichetta": "validità minima delle condizioni nel modulo"},
            {"valore": "5.000-50.000 euro", "etichetta": "fascia delle sanzioni"},
        ],
        "paragrafi": [
            "Il decreto legislativo 176 del 25 settembre 2026, pubblicato in Gazzetta Ufficiale il 7 ottobre, entra in vigore il 22 ottobre. Il provvedimento recepisce la direttiva europea che promuove la riparazione dei beni e inserisce nuove norme nel Codice del consumo.",
            "Per i prodotti coperti dalle specifiche europee di riparabilità, il fabbricante deve offrire la riparazione gratuitamente o a un prezzo ragionevole e in tempi ragionevoli, salvo che l'intervento sia impossibile. Ricambi e strumenti messi a disposizione non devono avere prezzi tali da scoraggiare la riparazione.",
            "Il riparatore può consegnare un modulo europeo gratuito con difetto, intervento proposto, prezzo o limite massimo, tempi, luogo di consegna e servizi accessori. Le condizioni indicate non possono essere cambiate per almeno trenta giorni; un eventuale costo di diagnosi deve essere comunicato prima.",
            "La sezione italiana della futura piattaforma europea sarà gratuita per i consumatori e avrà il Mimit come punto di contatto. Le violazioni degli obblighi principali possono comportare sanzioni amministrative da 5.000 a 50.000 euro, raddoppiabili nei casi più gravi o reiterati.",
        ],
        "fonti": [
            {"url": "https://www.gazzettaufficiale.it/eli/id/2026/10/07/26G00191/sg", "nome": "Gazzetta Ufficiale — decreto legislativo 176/2026 e data di entrata in vigore."},
            {"url": "https://www.gazzettaufficiale.it/atto/serie_generale/caricaArticoloDefault/originario?atto.codiceRedazionale=26G00191&atto.dataPubblicazioneGazzetta=2026-10-07&atto.tipoProvvedimento=DECRETO+LEGISLATIVO", "nome": "Gazzetta Ufficiale — testo completo delle nuove norme sulla riparazione."},
        ],
        "image_source": "riparazione",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un tecnico che ripara elettrodomestici e dispositivi in un laboratorio italiano; scena non documentaria.",
        "image_prompt": "Laboratorio italiano per riparazione di elettrodomestici e smartphone, tecnico al lavoro, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "giornata-nazionale-meraviglia-seconda-domenica-ottobre-2026",
        "titolo": "Nasce la Giornata nazionale della meraviglia: sarà ogni ottobre",
        "sommario": "La nuova ricorrenza cade la seconda domenica di ottobre e richiama l'attenzione sui bambini che vivono in guerra.",
        "categoria": "Cultura", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Giornata nazionale", "meraviglia"],
        "dati_chiave": [
            {"valore": "2ª domenica", "etichetta": "ricorrenza ogni ottobre"},
            {"valore": "8 ottobre", "etichetta": "legge entrata in vigore"},
            {"valore": "non festiva", "etichetta": "nessun effetto civile da giorno festivo"},
        ],
        "paragrafi": [
            "L'Italia riconosce la seconda domenica di ottobre come Giornata nazionale della meraviglia. La legge 175 del 5 ottobre 2026 è stata pubblicata in Gazzetta Ufficiale il 7 ottobre ed è entrata in vigore l'8 ottobre.",
            "La ricorrenza ha l'obiettivo di sensibilizzare sulle sofferenze e sulle difficoltà dei bambini che vivono in guerra, invitando a riflettere sul valore del diritto alla meraviglia nella vita dei minori e degli adulti.",
            "La legge precisa che la giornata non produce gli effetti civili delle festività nazionali. Non determina quindi chiusure automatiche di scuole, uffici o attività e non modifica il calendario lavorativo.",
            "Il testo è essenziale e non assegna nella stessa norma un programma unico di iniziative. Eventuali appuntamenti pubblici, scolastici o associativi dovranno essere verificati sui canali degli enti organizzatori.",
        ],
        "fonti": [
            {"url": "https://www.gazzettaufficiale.it/eli/id/2026/10/07/26G00195/sg", "nome": "Gazzetta Ufficiale — legge 175/2026 e data di entrata in vigore."},
            {"url": "https://www.gazzettaufficiale.it/atto/serie_generale/caricaArticoloDefault/originario?atto.codiceRedazionale=26G00195&atto.dataPubblicazioneGazzetta=2026-10-07&atto.tipoProvvedimento=LEGGE", "nome": "Gazzetta Ufficiale — testo della Giornata nazionale della meraviglia."},
        ],
        "image_source": "meraviglia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica e simbolica della Giornata nazionale della meraviglia con libri, stelle e bolle di sapone; scena non documentaria.",
        "image_prompt": "Installazione simbolica italiana con libri, stelle di carta e bolle di sapone per il diritto alla meraviglia, illustrazione editoriale ultrarealistica e rispettosa.",
    },
    {
        "slug": "archivi-di-vetta-belluno-presentazione-11-ottobre-2026",
        "titolo": "Archivi di Vetta debutta a Belluno: online la memoria delle Alpi",
        "sommario": "Domenica 11 ottobre viene presentata la piattaforma che riunisce fotografie e documenti delle comunità di montagna.",
        "categoria": "Cultura", "luogo": "Belluno", "formato": "flash",
        "parole_chiave_titolo": ["Archivi di Vetta", "Belluno"],
        "dati_chiave": [
            {"valore": "11 ottobre", "etichetta": "presentazione pubblica"},
            {"valore": "17:00", "etichetta": "inizio all'Auditorium"},
            {"valore": "ingresso libero", "etichetta": "prenotazione non richiesta"},
        ],
        "paragrafi": [
            "Archivi di Vetta viene presentato al pubblico domenica 11 ottobre 2026 alle 17 nell'Auditorium di piazza Duomo 1 a Belluno. L'incontro, pubblicato oggi dal Ministero della Cultura, non richiede prenotazione ed è previsto fino alle 19:30.",
            "Il progetto della Soprintendenza archivistica e bibliografica del Veneto e Trentino-Alto Adige nasce dalla mappatura dei patrimoni documentari della montagna. La prima fase ha coinvolto soprattutto sezioni venete del Club Alpino Italiano e archivi di associazioni sportive amatoriali.",
            "La piattaforma raccoglie una selezione di fotografie provenienti da fondi diversi: ascensioni, pratiche sportive, paesaggi e attività delle comunità alpine diventano consultabili in uno spazio comune destinato ad ampliarsi.",
            "Marco Spagni e Francesca Crema illustreranno il censimento e il ruolo degli archivi nella conservazione della memoria delle Alpi. Per chi arriva da fuori Belluno è utile verificare direttamente con l'ente eventuali variazioni logistiche dell'ultima ora.",
        ],
        "fonti": [{"url": "https://cultura.gov.it/evento/archivi-di-vetta-gli-archivi-e-le-montagne-tutela-e-valorizzazione-dei-patrimoni-per-le-comunita", "nome": "Ministero della Cultura — presentazione, orari e contenuti di Archivi di Vetta."}],
        "image_source": "archivi",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un archivio alpino a Belluno con fotografie storiche e Dolomiti; scena non documentaria.",
        "image_prompt": "Archivio alpino di Belluno con fotografie storiche di montagna e Dolomiti alle finestre, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "famiglie-museo-firenze-detective-passato-10-ottobre-2026",
        "titolo": "Famiglie al Museo a Firenze: due laboratori da detective",
        "sommario": "Sabato 10 ottobre il Museo Archeologico propone attività per bambini dai 7 agli 11 anni. Prenotazione obbligatoria.",
        "categoria": "Cultura", "luogo": "Firenze", "formato": "flash",
        "parole_chiave_titolo": ["Famiglie al Museo", "Firenze"],
        "dati_chiave": [
            {"valore": "9:30 e 11:30", "etichetta": "i due turni"},
            {"valore": "7-11 anni", "etichetta": "età prevista"},
            {"valore": "90 minuti", "etichetta": "durata del laboratorio"},
        ],
        "paragrafi": [
            "Il Museo Archeologico Nazionale di Firenze organizza sabato 10 ottobre 2026 il laboratorio Detective del passato: dai frammenti al mito. L'attività, inserita nella Giornata nazionale delle famiglie al museo, è rivolta ai bambini dai 7 agli 11 anni.",
            "Sono previsti due turni, alle 9:30 e alle 11:30, della durata di circa un'ora e mezza. I partecipanti osservano materiali, confrontano immagini e fonti scritte e ricostruiscono il percorso con cui gli archeologi interpretano i reperti.",
            "La prenotazione è obbligatoria e l'attività è compresa nel costo del biglietto di ingresso. Nella stessa mattina il museo presenta Al Museo con Musetta, una guida dei Servizi educativi che sarà regalata ai piccoli visitatori.",
            "La sede è in via della Colonna 38. Prima di raggiungere il museo è opportuno verificare la conferma della prenotazione e l'orario assegnato, perché la pagina ufficiale non indica accesso libero ai laboratori.",
        ],
        "fonti": [{"url": "https://cultura.gov.it/evento/giornata-nazionale-delle-famiglie-al-museo-maf", "nome": "Ministero della Cultura — laboratorio per famiglie al Museo Archeologico di Firenze."}],
        "image_source": "firenze_famu",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un tavolo didattico con reperti e strumenti nel Museo Archeologico di Firenze; scena non documentaria.",
        "image_prompt": "Tavolo didattico con reperti, lenti e pennelli nel Museo Archeologico di Firenze, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "egnazia-caccia-tesoro-famiglie-museo-11-ottobre-2026",
        "titolo": "Egnazia, caccia al tesoro tra i reperti: prenotazioni entro sabato",
        "sommario": "Domenica 11 ottobre due turni per bambini dai 5 ai 10 anni. L'attività è gratuita per i piccoli partecipanti.",
        "categoria": "Cultura", "luogo": "Fasano", "formato": "flash",
        "parole_chiave_titolo": ["Egnazia", "caccia al tesoro"],
        "dati_chiave": [
            {"valore": "10:00 e 11:30", "etichetta": "i due turni"},
            {"valore": "5-10 anni", "etichetta": "età consigliata"},
            {"valore": "sabato ore 19", "etichetta": "termine di prenotazione"},
        ],
        "paragrafi": [
            "Il Museo archeologico nazionale Giuseppe Andreassi di Egnazia propone domenica 11 ottobre 2026 una caccia al tesoro fra reperti e testimonianze dell'antica città. L'iniziativa per la Giornata delle famiglie al museo prevede enigmi, indizi e un premio finale.",
            "I turni iniziano alle 10 e alle 11:30 e durano un'ora e mezza. L'età consigliata è dai 5 ai 10 anni. La prenotazione è obbligatoria entro le 19 di sabato 10 ottobre, fino a esaurimento posti, chiamando lo 080 4829056.",
            "Per i bambini l'ingresso al museo e la caccia al tesoro sono gratuiti. Gli adulti pagano 8 euro per museo e attività, oppure 10 euro se intendono visitare anche il parco archeologico, compatibilmente con gli orari indicati dal sito.",
            "Il complesso si trova in via delle Carceri a Fasano, in provincia di Brindisi. La disponibilità della visita al parco va verificata al momento della prenotazione, perché non coincide automaticamente con il turno del laboratorio.",
        ],
        "fonti": [{"url": "https://cultura.gov.it/evento/f-at-mu-2026-caccia-al-tesoro-al-museo", "nome": "Ministero della Cultura — turni, prezzi e prenotazioni per la caccia al tesoro di Egnazia."}],
        "image_source": "egnazia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica del parco archeologico di Egnazia con mappa e bussola; scena non documentaria.",
        "image_prompt": "Parco archeologico di Egnazia in Puglia con mappa e bussola, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "chiaroscuro-netflix-trailer-uscita-11-novembre-2026",
        "titolo": "ChiaroScuro, il trailer svela il crime con Pierpaolo Spollon",
        "sommario": "La serie italiana in otto episodi debutta l'11 novembre su Netflix dopo l'anteprima alla Festa del Cinema di Roma.",
        "categoria": "Film e serie TV", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["ChiaroScuro", "Pierpaolo Spollon"],
        "dati_chiave": [
            {"valore": "11 novembre", "etichetta": "uscita su Netflix"},
            {"valore": "8 episodi", "etichetta": "formato della serie"},
            {"valore": "Festa di Roma", "etichetta": "anteprima fuori concorso"},
        ],
        "paragrafi": [
            "Netflix ha pubblicato il trailer ufficiale di ChiaroScuro, serie italiana light crime in otto episodi in arrivo l'11 novembre 2026. Prima dello streaming sarà presentata in anteprima assoluta alla Festa del Cinema di Roma, fuori concorso nella sezione Freestyle.",
            "Pierpaolo Spollon interpreta Cosmo Speranza, consulente d'arte capace di riconoscere le opere false dai dettagli. La sua competenza lo porta a collaborare con la Squadra Mobile di Roma e con l'ispettore Angelo Tiberi, interpretato da Andrea Lattanzi.",
            "Nel cast figurano anche Matilde Gioli, Romana Maggiora Vergano e Aurora Giovinazzo, con Paz Vega e Alessandro Preziosi. La storia unisce indagini e mondo dell'arte, mentre un quadro legato all'infanzia di Cosmo riapre il caso della morte del padre.",
            "La serie è prodotta da Lux Vide, società del gruppo Fremantle. Il trailer, il poster e le nuove immagini sono disponibili nella newsroom ufficiale di Netflix; l'orario di pubblicazione dell'11 novembre non è specificato nel comunicato.",
        ],
        "fonti": [{"url": "https://about.netflix.com/it/news/chiaroscuro-the-official-trailer-of-the-new-series-premiering-at-the-rome-film-festival-and-coming-to-netflix-on-november-11th", "nome": "Netflix — trailer, cast, trama e data di uscita di ChiaroScuro."}],
        "image_source": "chiaroscuro",
        "image_alt": "Illustrazione editoriale IA ultrarealistica con somiglianza sintetica di Pierpaolo Spollon in una galleria d'arte romana; non è una fotografia documentaria.",
        "image_prompt": "Pierpaolo Spollon in una galleria d'arte romana con indizi investigativi, key art editoriale IA ultrarealistica, logo Netflix accurato.",
    },
    {
        "slug": "amerigo-vespucci-trieste-barcolana-inclusione-9-11-ottobre-2026",
        "titolo": "Amerigo Vespucci a Trieste, tre giorni di sport e inclusione",
        "sommario": "Dal 9 all'11 ottobre, durante Barcolana, visite a bordo, associazioni e incontri dedicati ai talenti delle persone con disabilità.",
        "categoria": "Sport", "luogo": "Trieste", "formato": "flash",
        "parole_chiave_titolo": ["Amerigo Vespucci", "Trieste"],
        "dati_chiave": [
            {"valore": "9-11 ottobre", "etichetta": "programma dedicato"},
            {"valore": "3 panel", "etichetta": "sport e disabilità"},
            {"valore": "58ª Barcolana", "etichetta": "edizione della regata"},
        ],
        "paragrafi": [
            "L'Amerigo Vespucci conclude a Trieste la Campagna Nord America 2026 in concomitanza con la 58ª Barcolana. Dal 9 all'11 ottobre il programma del Ministero per le Disabilità unisce visite a bordo, stand associativi, arte e incontri sullo sport inclusivo.",
            "Venerdì 9 ottobre alle 14:30 è previsto un approfondimento sul progetto Velando. Sabato 10 alle 10 il focus passa a Tip Top Mountain, mentre domenica 11 dalle 11:30 si tiene il convegno Sport e disabilità nella conference room.",
            "Negli spazi dedicati si alternano Fondazione Bambini e Autismo per il Futuro, ANFFAS, Progetto Riabilitazione e Progetto Noemi. Le associazioni presentano attività e prodotti, affiancando il programma di incontri.",
            "La comunicazione istituzionale non dettaglia in questa pagina le modalità di prenotazione delle visite a bordo. Chi vuole partecipare deve controllare il programma operativo della tappa e gli aggiornamenti Barcolana prima di raggiungere il porto.",
        ],
        "fonti": [{"url": "https://www.disabilita.governo.it/it/notizie/amerigo-vespucci-locatelli-a-trieste-inclusione-sport-e-valorizzazione-dei-talenti/", "nome": "Ministero per le Disabilità — programma inclusivo sulla Vespucci durante Barcolana."}],
        "image_source": "vespucci",
        "image_alt": "Illustrazione editoriale IA ultrarealistica dell'Amerigo Vespucci nel porto di Trieste durante Barcolana; scena non documentaria.",
        "image_prompt": "Amerigo Vespucci ormeggiata a Trieste durante Barcolana, attrezzature per vela accessibile, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "italia-e-cultura-torino-conferenza-aici-9-10-ottobre-2026",
        "titolo": "Italia è cultura a Torino: archivi e biblioteche sfidano l’IA",
        "sommario": "Il 9 e 10 ottobre la decima conferenza AICI riunisce gli istituti culturali al Polo del ’900 e al Museo del Risorgimento.",
        "categoria": "Cultura", "luogo": "Torino", "formato": "flash",
        "parole_chiave_titolo": ["Italia è cultura", "Torino"],
        "dati_chiave": [
            {"valore": "9-10 ottobre", "etichetta": "le due giornate"},
            {"valore": "10ª edizione", "etichetta": "conferenza nazionale AICI"},
            {"valore": "2 sedi", "etichetta": "Polo del ’900 e Museo del Risorgimento"},
        ],
        "paragrafi": [
            "La decima conferenza nazionale dell'Associazione delle istituzioni di cultura italiane si svolge il 9 e 10 ottobre 2026 a Torino, tra Polo del ’900 e Museo Nazionale del Risorgimento Italiano. Il titolo dell'edizione è Italia è cultura.",
            "I lavori affrontano il ruolo attuale di biblioteche, archivi, fondazioni e accademie, con particolare attenzione alle trasformazioni digitali e all'intelligenza artificiale. Un altro asse riguarda il rapporto tra storia, memoria e democrazia a ottant'anni dall'Assemblea Costituente.",
            "L'appuntamento coincide con i trent'anni della legge 534 del 1996, riferimento per il riconoscimento e il sostegno degli istituti culturali. L'apertura è fissata venerdì alle 15 al Polo del ’900 con la relazione della presidente AICI Flavia Piccoli Nardelli.",
            "Il programma completo delle due giornate è collegato dalla pagina della Direzione generale Biblioteche e istituti culturali. Sedi e orari dei singoli interventi vanno controllati prima dell'accesso, perché il convegno utilizza più spazi.",
        ],
        "fonti": [{"url": "https://biblioteche.cultura.gov.it/it/notizie/notizia/Italia-e-cultura/", "nome": "Direzione generale Biblioteche e istituti culturali — sedi e temi della conferenza Italia è cultura."}],
        "image_source": "italia_cultura",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una sala culturale torinese con archivi e schermi dedicati all'intelligenza artificiale; scena non documentaria.",
        "image_prompt": "Sala conferenze al Polo del '900 di Torino con archivi e visualizzazioni astratte di intelligenza artificiale, illustrazione ultrarealistica.",
    },
    {
        "slug": "domenica-biblioteca-nazionale-roma-11-ottobre-2026-gratis",
        "titolo": "Roma, Domenica in Biblioteca: concerti e Spazi900 gratis",
        "sommario": "L'11 ottobre la Biblioteca nazionale centrale apre dalle 9:30 alle 19. Tutti gli eventi sono gratuiti con prenotazione.",
        "categoria": "Cultura", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["Domenica in Biblioteca", "Roma"],
        "dati_chiave": [
            {"valore": "9:30-19:00", "etichetta": "apertura straordinaria"},
            {"valore": "ingresso gratuito", "etichetta": "con prenotazione obbligatoria"},
            {"valore": "31° convegno", "etichetta": "appuntamento internazionale di chitarra"},
        ],
        "paragrafi": [
            "La Biblioteca nazionale centrale di Roma apre domenica 11 ottobre 2026 dalle 9:30 alle 19 con incontri, presentazioni e concerti. Tutti gli appuntamenti sono a ingresso gratuito, ma richiedono la prenotazione indicata dal sito ufficiale.",
            "Il programma comprende il 31° Convegno Internazionale di Chitarra e una mostra di liuteria. Durante l'apertura straordinaria è visitabile anche il Museo Spazi900, dedicato alla letteratura italiana contemporanea.",
            "Restano attivi l'ufficio accoglienza per emissione e rinnovo delle tessere e la sala di pubblica lettura, aperta agli utenti che vogliono studiare con materiale proprio. La sede è in viale Castro Pretorio 105.",
            "La gratuità non sostituisce la prenotazione per gli eventi. Prima di partire conviene aprire il programma collegato dalla Direzione generale Biblioteche, scegliere l'appuntamento e verificare la disponibilità residua.",
        ],
        "fonti": [{"url": "https://biblioteche.cultura.gov.it/it/calendario-eventi/evento/Domenica-in-Biblioteca-00002/", "nome": "Direzione generale Biblioteche e istituti culturali — programma e prenotazioni di Domenica in Biblioteca."}],
        "image_source": "biblioteca_roma",
        "image_alt": "Illustrazione editoriale IA ultrarealistica della Biblioteca nazionale centrale di Roma preparata per concerti e mostra di liuteria; scena non documentaria.",
        "image_prompt": "Biblioteca Nazionale Centrale di Roma con libri, chitarre e strumenti di liuteria per un'apertura domenicale, illustrazione ultrarealistica.",
    },
]


def main() -> None:
    append_name_phrases()
    base = datetime.now(ROME).replace(microsecond=0)
    minute_offsets = (0, 7, 18, 26, 41, 50, 64, 76, 88, 103)
    images = []
    written = []
    for article, minutes in zip(ARTICLES, minute_offsets):
        image = make_image(article)
        slug = site.write_article(article, image, VERSION)
        published = base - timedelta(minutes=minutes)
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

    site.sync_surfaces(written, f"/notizie/{written[0]['slug']}.html", VERSION, update_manifest=False)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION,
        "currentVersion": VERSION,
        "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": f"ultimissime-italia-v{VERSION}",
        "date": base.date().isoformat(),
        "release_date": base.date().isoformat(),
        "updated_at": base.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
