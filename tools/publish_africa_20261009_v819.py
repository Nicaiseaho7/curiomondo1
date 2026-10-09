#!/usr/bin/env python3
"""Release v819: dieci notizie su Africa e rapporti con i paesi occidentali."""
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

VERSION = 819
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"

IMAGE_SOURCES = {
    "etiopia": GENERATED / "exec-71db812b-a766-4e93-a81b-93ca8278273e.png",
    "sudafrica": GENERATED / "exec-3b356402-59bd-48c0-99d1-bd573e21cbba.png",
    "zambia": GENERATED / "exec-0b0065a7-a691-44ca-b04a-77fe2ae85238.png",
    "goma": GENERATED / "exec-f5080546-a985-4430-9638-84f2deb350d8.png",
    "olimpiadi": GENERATED / "exec-28720b22-1589-4bbf-912b-678770f221c3.png",
    "fifa": GENERATED / "exec-c5939421-36e3-4490-86bb-d7f63af149bf.png",
    "afcra": GENERATED / "exec-267d50dd-a6f1-48b5-8244-ab433f3fefcc.png",
    "crescita": GENERATED / "exec-c002f910-91db-4341-b3ce-a69e1c81459e.png",
    "dfc": GENERATED / "exec-eb13cea0-9e98-4816-b284-feefec90d8fb.png",
    "somalia": GENERATED / "exec-d8ee3c27-2019-4e12-8edb-9ebb3f439323.png",
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
    return {
        "key": f"{article['slug']}-v{VERSION}",
        "alt": article.pop("image_alt"),
        "prompt": article.pop("image_prompt"),
        "variants": make_variants(IMAGE_SOURCES[article.pop("image_source")], article["slug"]),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": article.pop("sensibile", False),
        "weatherMap": False,
        "reenactedEvent": False,
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


def append_name_phrases() -> None:
    path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        "Quando le notizie preoccupano, cerca prima i fatti confermati.",
        "Difendi la dignità delle persone anche quando il confronto si accende.",
        "Prima di condividere un allarme, controlla chi lo ha diffuso.",
        "La pace richiede pazienza, ma anche impegni verificabili.",
        "Un progetto ambizioso vale di più quando lascia benefici duraturi.",
        "Sostieni lo sport senza rinunciare a fare domande a chi lo governa.",
        "I numeri aiutano a decidere soltanto quando il metodo è trasparente.",
        "La crescita conta davvero quando migliora la vita di più persone.",
        "Valuta ogni investimento insieme ai suoi effetti sulle comunità.",
        "Il futuro si costruisce rafforzando capacità che restano nel Paese.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


ARTICLES = [
    {
        "slug": "etiopia-accusa-eritrea-invasione-tigray-60-km-9-ottobre-2026",
        "titolo": "Etiopia accusa l’Eritrea di invasione: truppe fino a 60 km",
        "sommario": "Una lettera del ministro degli Esteri etiope all'ONU denuncia un'avanzata nel Tigray. Asmara respinge l'accusa e parla di un pretesto per la guerra.",
        "categoria": "Mondo", "luogo": "Tigray", "formato": "flash", "sensibile": True,
        "parole_chiave_titolo": ["Etiopia", "Eritrea", "60 km"],
        "dati_chiave": [
            {"valore": "60 km", "etichetta": "avanzata denunciata da Addis Abeba"},
            {"valore": "8 ottobre", "etichetta": "data della lettera all'ONU"},
            {"valore": "2018", "etichetta": "anno dell'accordo di pace"},
        ],
        "paragrafi": [
            "L'Etiopia ha accusato l'Eritrea di avere lanciato un'invasione nel nord del Paese e di essere avanzata fino a 60 chilometri nel Tigray. L'affermazione è contenuta in una lettera datata 8 ottobre del ministro degli Esteri Gedion Timothewos, inviata ai membri del Consiglio di sicurezza dell'ONU e condivisa con Reuters.",
            "Il documento presenta l'azione come un'aggressione e sostiene che Addis Abeba sia costretta a difendersi. Si tratta della prima posizione ufficiale del governo etiope sulle incursioni segnalate questa settimana; la distanza di 60 chilometri resta una stima attribuita alle autorità etiopi e non una misura verificata in modo indipendente.",
            "Il ministro dell'Informazione eritreo Yemane Gebremeskel aveva respinto le ricostruzioni su un'incursione, definendole parte di un piano etiope per giustificare una guerra contro Asmara. Le due versioni sono quindi direttamente contrapposte.",
            "Reuters riferisce che residenti di Adigrat hanno udito esplosioni nella notte e che il monitor ACLED ha segnalato attacchi con droni contro forze eritree in ripiegamento. Questi elementi indicano un'escalation sul terreno, ma non consentono da soli di stabilire la responsabilità di ogni singolo attacco.",
            "La Commissione africana dei diritti umani ha espresso profonda preoccupazione per le rinnovate tensioni nel nord dell'Etiopia. L'organismo dell'Unione Africana ha richiamato la necessità di proteggere i civili e di evitare un nuovo ampliamento del conflitto.",
            "Etiopia ed Eritrea combatterono una guerra tra il 1998 e il 2000 e firmarono la pace nel 2018. Asmara sostenne poi le forze federali etiopi durante la guerra del Tigray del 2020-2022, ma i rapporti si sono nuovamente deteriorati, anche sul tema dell'accesso etiope al Mar Rosso.",
        ],
        "fonti": [
            {"url": "https://www.reuters.com/world/africa/ethiopia-says-it-must-defend-itself-against-eritreas-all-out-invasion-2026-10-09/", "nome": "Reuters — lettera etiope all'ONU, posizione eritrea e riscontri dal Tigray, 9 ottobre 2026."},
            {"url": "https://achpr.au.int/", "nome": "Commissione africana dei diritti umani — dichiarazione sulle nuove tensioni nel nord dell'Etiopia, 8 ottobre 2026."},
        ],
        "image_source": "etiopia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica del paesaggio di confine fra Etiopia ed Eritrea, senza combattimenti; scena non documentaria.",
        "image_prompt": "Paesaggio di confine tra Etiopia ed Eritrea nel Tigray, strada e bandiere, nessuna persona o azione militare, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 9, 48, tzinfo=ROME),
    },
    {
        "slug": "sudafrica-ritira-direttiva-asilo-dopo-violenze-9-ottobre-2026",
        "titolo": "Sudafrica ritira la direttiva sull’asilo dopo le violenze",
        "sommario": "Gli uffici per i rifugiati erano stati sopraffatti dalle richieste. Il governo prepara un nuovo metodo per applicare la sentenza della Corte costituzionale.",
        "categoria": "Mondo", "luogo": "Sudafrica", "formato": "flash", "sensibile": True,
        "parole_chiave_titolo": ["Sudafrica", "direttiva sull’asilo", "violenze"],
        "dati_chiave": [
            {"valore": "28 settembre", "etichetta": "direttiva ora ritirata"},
            {"valore": "24 veicoli", "etichetta": "incendiati fra Durban e Soweto"},
            {"valore": "7 luglio", "etichetta": "sentenza costituzionale"},
        ],
        "paragrafi": [
            "Il Dipartimento degli Affari interni del Sudafrica ha ritirato il 9 ottobre la direttiva che consentiva di ricevere nuove domande di asilo in attuazione di una sentenza della Corte costituzionale. La decisione arriva dopo le violenze registrate durante proteste anti-migranti a Johannesburg e Durban.",
            "La direttiva era stata emanata il 28 settembre per tradurre in pratica la sentenza del 7 luglio nel caso Scalabrini of Cape Town. La Corte aveva stabilito che l'ingresso irregolare non può, da solo, impedire a una persona di accedere alla procedura d'asilo.",
            "Il governo precisa che il provvedimento non concedeva automaticamente lo status di rifugiato, la residenza permanente o altri diritti alle persone prive di documenti. Il Dipartimento attribuisce parte delle tensioni a informazioni false diffuse sul significato della sentenza.",
            "Secondo la nota ufficiale, gli uffici di accoglienza per i rifugiati sono stati sopraffatti in pochi giorni, gli operatori sono stati esposti a rischi e sono emerse minacce per l'ordine pubblico. L'amministrazione avvierà ora un nuovo processo operativo per rispettare la decisione della Corte in modo sostenibile.",
            "Reuters ha documentato l'incendio di 14 veicoli a Durban e di altri dieci a Soweto, oltre a saccheggi ai danni di negozi di proprietà straniera. La polizia ha riferito il 9 ottobre che la situazione si era stabilizzata in entrambe le aree.",
            "Il ritiro della direttiva non annulla la sentenza costituzionale. Il passaggio successivo sarà quindi definire una procedura capace di garantire l'accesso al sistema d'asilo senza riprodurre il sovraccarico che ha bloccato gli uffici.",
        ],
        "fonti": [
            {"url": "https://www.gov.za/news/media-statements/home-affairs-director-general-withdraws-asylum-directive-09-oct-2026", "nome": "Governo del Sudafrica — ritiro della direttiva e motivazioni operative, 9 ottobre 2026."},
            {"url": "https://www.reuters.com/world/africa/south-africa-withdraws-asylum-directive-after-anti-migrant-violence-2026-10-09/", "nome": "Reuters — violenze, danni e aggiornamento della polizia, 9 ottobre 2026."},
        ],
        "image_source": "sudafrica",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una strada di Soweto dopo disordini, senza persone ferite; scena non documentaria.",
        "image_prompt": "Strada di Soweto con barriere e mezzi della polizia sudafricana dopo disordini, senza persone o fiamme, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 10, 1, tzinfo=ROME),
    },
    {
        "slug": "zambia-usa-intesa-sanitaria-2-49-miliardi-senza-dati-8-ottobre-2026",
        "titolo": "Zambia-USA, intesa sanitaria da 2,49 miliardi senza dati",
        "sommario": "Washington contribuirà con 1,52 miliardi di dollari e Lusaka con 975 milioni in cinque anni. Eliminati gli obblighi su campioni biologici e dati dei pazienti.",
        "categoria": "Mondo", "luogo": "Lusaka", "formato": "flash", "sensibile": True,
        "parole_chiave_titolo": ["Zambia-USA", "2,49 miliardi", "senza dati"],
        "dati_chiave": [
            {"valore": "$2,49 mld", "etichetta": "valore complessivo"},
            {"valore": "$1,52 mld", "etichetta": "contributo statunitense"},
            {"valore": "5 anni", "etichetta": "durata dell'intesa"},
        ],
        "paragrafi": [
            "Stati Uniti e Zambia hanno firmato l'8 ottobre a Lusaka un memorandum sanitario quinquennale da 2,49 miliardi di dollari. Il Dipartimento di Stato indica un contributo statunitense di 1,52 miliardi e un investimento aggiuntivo dello Zambia pari a 975 milioni.",
            "L'accordo è stato chiuso dopo la rimozione delle clausole che avrebbero riguardato la condivisione di campioni biologici e dati dei pazienti. Il ministro della Salute zambiano Roma Chilengi ha dichiarato che il testo finale non compromette la sicurezza dei dati del Paese.",
            "Il governo di Lusaka ha inoltre separato il dossier sanitario dai negoziati sui minerali critici. Le parti continueranno a discutere rame e altre risorse in un tavolo distinto, senza collegarle al finanziamento della sanità.",
            "Secondo Associated Press, il programma dovrebbe sostenere il reclutamento di 40.000 operatori sanitari in cinque anni. Le risorse sono destinate anche alla prevenzione e alla risposta alle malattie infettive, al rafforzamento delle strutture e alla continuità dei servizi.",
            "La cifra definitiva è inferiore ai 3,6 miliardi inizialmente prospettati da funzionari zambiani. La differenza rende necessario riferirsi al valore contenuto nella comunicazione successiva alla firma, non alle stime diffuse durante la trattativa.",
            "L'intesa rientra nella strategia sanitaria bilaterale degli Stati Uniti, che chiede ai Paesi partner di aumentare gradualmente la spesa domestica. L'impatto effettivo dipenderà dai fondi autorizzati ogni anno e dalla capacità di trasformarli in personale, farmaci e servizi verificabili.",
        ],
        "fonti": [
            {"url": "https://www.state.gov/releases/office-of-the-spokesman/2026/10/united-states-and-zambia-sign-five-year-global-health-partnership-under-the-trump-administrations-america-first-global-health-strategy/", "nome": "Dipartimento di Stato USA — memorandum sanitario con lo Zambia, 8 ottobre 2026."},
            {"url": "https://apnews.com/article/926edb9ab38b144bb1b83f73e5645f1b", "nome": "Associated Press — testo finale, rimozione delle clausole e piano per il personale sanitario."},
        ],
        "image_source": "zambia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica della firma di un accordo sanitario fra Zambia e Stati Uniti; scena non documentaria.",
        "image_prompt": "Firma istituzionale di un accordo sanitario con bandiere reali di Zambia e Stati Uniti, mani e documenti senza volti, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 10, 13, tzinfo=ROME),
    },
    {
        "slug": "rdc-mediatori-unione-africana-afc-m23-goma-7-ottobre-2026",
        "titolo": "RDC, i mediatori africani incontrano l’AFC/M23 a Goma",
        "sommario": "Tre ex presidenti hanno consultato ribelli, ONU e organismi umanitari. Il panel chiede rispetto del cessate il fuoco e accesso agli aiuti.",
        "categoria": "Mondo", "luogo": "Goma", "formato": "flash", "sensibile": True,
        "parole_chiave_titolo": ["RDC", "mediatori africani", "AFC/M23"],
        "dati_chiave": [
            {"valore": "3", "etichetta": "ex presidenti nella delegazione"},
            {"valore": "5 ottobre", "etichetta": "consultazioni a Goma"},
            {"valore": "Doha", "etichetta": "processo da proseguire"},
        ],
        "paragrafi": [
            "Una delegazione del panel di facilitatori dell'Unione Africana ha incontrato il 5 ottobre a Goma rappresentanti dell'AFC/M23, delle Nazioni Unite e delle organizzazioni umanitarie. Le consultazioni puntano a sostenere il processo di pace per l'est della Repubblica Democratica del Congo.",
            "La missione era guidata dall'ex presidente etiope Sahle-Work Zewde e comprendeva gli ex presidenti Uhuru Kenyatta del Kenya e Mokgweetsi Masisi del Botswana. Il gruppo ha ascoltato anche MONUSCO, OCHA, Comitato internazionale della Croce Rossa e meccanismo congiunto di verifica.",
            "Il panel ha chiesto alle parti di proseguire in buona fede il processo di Doha, rispettare gli impegni sul cessate il fuoco e collaborare con i meccanismi di controllo. Non è stato annunciato un nuovo accordo né un calendario definitivo per la cessazione delle ostilità.",
            "La dichiarazione richiama la protezione dei civili, con particolare attenzione a donne e ragazze, la prevenzione della violenza sessuale e l'accesso sicuro e senza ostacoli agli aiuti. Viene chiesta anche la tutela di scuole e servizi essenziali.",
            "Reuters riferisce che gli scontri proseguono nonostante le iniziative diplomatiche. L'incontro con i dirigenti dell'AFC/M23 rappresenta quindi un canale di dialogo, ma non equivale a una tregua sul terreno.",
            "Il panel trasmetterà l'esito delle consultazioni al mediatore dell'Unione Africana e al governo congolese. I prossimi segnali concreti saranno la cooperazione con i verificatori, la riduzione degli attacchi e il miglioramento dell'accesso umanitario.",
        ],
        "fonti": [
            {"url": "https://www.peaceau.org/en/article/statement-by-the-african-union-panel-of-facilitators-following-consultations-in-goma-drc", "nome": "Unione Africana — dichiarazione del panel dopo le consultazioni di Goma, 7 ottobre 2026."},
            {"url": "https://www.reuters.com/world/africa/african-union-delegation-meets-congo-rebels-calls-continued-peace-efforts-2026-10-07/", "nome": "Reuters — incontro con l'AFC/M23 e quadro dei combattimenti nell'est della RDC."},
        ],
        "image_source": "goma",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una sala di mediazione dell'Unione Africana a Goma; scena non documentaria.",
        "image_prompt": "Sala vuota di mediazione dell'Unione Africana a Goma con Lago Kivu e Nyiragongo sullo sfondo, senza persone, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 10, 26, tzinfo=ROME),
    },
    {
        "slug": "olimpiadi-2036-sudafrica-sette-progetti-corsa-6-ottobre-2026",
        "titolo": "Olimpiadi 2036, il Sudafrica fra i sette progetti in corsa",
        "sommario": "Il CIO ha pubblicato il percorso di selezione: presentazioni a novembre, prima scelta nel marzo 2027 ed elezione della sede a metà 2029.",
        "categoria": "Sport", "luogo": "Sudafrica", "formato": "flash",
        "parole_chiave_titolo": ["Olimpiadi 2036", "Sudafrica", "sette progetti"],
        "dati_chiave": [
            {"valore": "7", "etichetta": "progetti nel dialogo continuo"},
            {"valore": "marzo 2027", "etichetta": "prima selezione"},
            {"valore": "2029", "etichetta": "elezione della sede"},
        ],
        "paragrafi": [
            "Il Sudafrica è uno dei sette Paesi che hanno dichiarato al Comitato Olimpico Internazionale l'interesse a ospitare i Giochi del 2036. Gli altri progetti arrivano da Germania, Ungheria, India, Qatar, Corea del Sud e Turchia.",
            "L'elenco non è una shortlist definitiva. I sette comitati si trovano nella fase di dialogo continuo, durante la quale il CIO offre assistenza tecnica e valuta i progetti senza avere ancora scelto una candidatura preferita.",
            "Le parti interessate presenteranno i propri piani alla Future Host Commission a novembre 2026. Dopo il 31 ottobre non saranno accettati nuovi progetti per l'edizione 2036.",
            "Entro marzo 2027 il CIO produrrà valutazioni di fattibilità; nello stesso mese il comitato esecutivo potrà ammettere alcuni progetti al dialogo strategico. Le sedi preferite entreranno nel dialogo mirato nel dicembre 2028.",
            "L'elezione finale è prevista durante una sessione del CIO a metà 2029. Saranno esaminati impianti, esperienza degli atleti, finanziamento, sostegno politico e pubblico, capacità organizzativa e benefici di lungo periodo per le comunità.",
            "Per il Sudafrica il percorso può aprire la possibilità di portare per la prima volta i Giochi estivi nel continente africano. La partecipazione alla procedura, però, non garantisce né la candidatura finale né l'assegnazione.",
        ],
        "fonti": [
            {"url": "https://www.olympics.com/ioc/news/ioc-sets-out-next-steps-for-selecting-2036-olympic-games-host", "nome": "Comitato Olimpico Internazionale — candidati interessati e calendario di selezione per il 2036."},
        ],
        "image_source": "olimpiadi",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di uno stadio sudafricano con la Table Mountain; scena non documentaria.",
        "image_prompt": "Cape Town Stadium e Table Mountain al tramonto, atmosfera da futura candidatura olimpica, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 10, 38, tzinfo=ROME),
    },
    {
        "slug": "calcio-africano-54-federazioni-sostengono-infantino-8-ottobre-2026",
        "titolo": "Calcio africano, 54 federazioni sostengono Infantino",
        "sommario": "Patrice Motsepe annuncia il sostegno unanime alla rielezione del presidente FIFA. Infantino promette più risorse dopo un miliardo investito in dieci anni.",
        "categoria": "Sport", "luogo": "Capo Verde", "formato": "flash",
        "parole_chiave_titolo": ["Calcio africano", "54 federazioni", "Infantino"],
        "dati_chiave": [
            {"valore": "54", "etichetta": "federazioni CAF"},
            {"valore": "$1 mld", "etichetta": "investimenti FIFA dichiarati"},
            {"valore": "124", "etichetta": "progetti FIFA Forward"},
        ],
        "paragrafi": [
            "Le 54 federazioni della Confederazione africana di calcio sosterranno Gianni Infantino nella corsa alla presidenza della FIFA del marzo 2027. Lo ha annunciato il presidente della CAF Patrice Motsepe durante la conferenza strategica tenuta l'8 ottobre a Capo Verde.",
            "Motsepe ha descritto la scelta come unanime e senza condizioni. Il blocco africano rappresenta più di un quarto dei 211 voti nell'assemblea FIFA e offre quindi a Infantino un vantaggio rilevante nella competizione elettorale.",
            "Il presidente FIFA ha ricordato che il programma FIFA Forward avrebbe investito un miliardo di dollari in Africa in dieci anni, attraverso 124 progetti e altre iniziative. Le cifre provengono dalla federazione internazionale e descrivono impegni aggregati, non un nuovo stanziamento approvato durante la conferenza.",
            "Infantino ha promesso di cercare ulteriori risorse e ha invitato la CAF a indicare priorità e bisogni. FIFA segnala anche che nove delle dieci nazionali africane presenti all'ultimo Mondiale hanno raggiunto la fase a eliminazione diretta.",
            "La scelta africana arriva mentre alcune federazioni europee e nordamericane hanno criticato il progetto, poi accantonato, di cedere una quota delle competizioni FIFA. L'ex nazionale svizzero Ramon Vega ha intanto dichiarato l'intenzione di candidarsi contro Infantino.",
            "Il sostegno annunciato a Capo Verde è politico e non costituisce ancora l'esito della votazione. Il congresso del 2027 resta il passaggio formale nel quale ciascuna federazione esprimerà il proprio voto.",
        ],
        "fonti": [
            {"url": "https://inside.fifa.com/news/caf-strategy-conference-cape-verde-africa-infantino-motsepe", "nome": "FIFA — intervento di Infantino alla conferenza strategica CAF, 8 ottobre 2026."},
            {"url": "https://www.reuters.com/sports/soccer/infantino-promises-further-fifa-support-african-football-2026-10-08/", "nome": "Reuters — sostegno delle 54 federazioni e contesto della corsa alla presidenza FIFA."},
        ],
        "image_source": "fifa",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di Gianni Infantino alla conferenza strategica CAF a Capo Verde; scena non documentaria.",
        "image_prompt": "Gianni Infantino riconoscibile sul palco della conferenza strategica CAF a Capo Verde con marchi FIFA e CAF autentici, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 10, 53, tzinfo=ROME),
    },
    {
        "slug": "africa-lancia-afcra-prima-agenzia-rating-continentale-7-ottobre-2026",
        "titolo": "L’Africa lancia AfCRA, la sua prima agenzia di rating",
        "sommario": "La nuova istituzione ha sede a Mauritius e punta a valutare Stati e imprese con maggiore copertura locale. Ventitré economie non hanno oggi rating dalle tre grandi agenzie.",
        "categoria": "Economia", "luogo": "Port Louis", "formato": "flash",
        "parole_chiave_titolo": ["Africa", "AfCRA", "prima agenzia di rating"],
        "dati_chiave": [
            {"valore": "23", "etichetta": "economie senza rating delle big three"},
            {"valore": "2018", "etichetta": "via libera politico iniziale"},
            {"valore": "Mauritius", "etichetta": "sede dell'agenzia"},
        ],
        "paragrafi": [
            "L'Unione Africana ha lanciato il 7 ottobre a Port Louis l'Africa Credit Rating Agency, la prima agenzia di rating promossa a livello continentale. AfCRA avrà sede a Mauritius e si propone di valutare emittenti sovrani, enti pubblici e imprese africane.",
            "Il progetto era stato approvato politicamente dall'assemblea dell'Unione Africana nel 2018. I ministri economici hanno sostenuto la creazione dell'agenzia nel 2023, mentre fra il 2024 e il 2025 sono stati sviluppati governance e metodo sotto il coordinamento dell'African Peer Review Mechanism.",
            "L'obiettivo dichiarato è aumentare la copertura e usare dati e conoscenze locali nelle valutazioni. Secondo l'Unione Africana, 23 economie del continente non ricevono oggi un rating sovrano dalle tre maggiori agenzie internazionali.",
            "Una maggiore copertura può facilitare l'accesso ai mercati, ma un nuovo soggetto non riduce automaticamente gli interessi pagati dagli Stati. Investitori e creditori valuteranno indipendenza, qualità dei dati, stabilità del metodo e capacità di evitare pressioni politiche.",
            "Reuters ricorda che una propria indagine del 2024 non aveva trovato prove di un pregiudizio sistematico nei rating sovrani assegnati all'Africa dalle tre grandi agenzie. AfCRA dovrà quindi dimostrare il valore del proprio approccio attraverso risultati comparabili e trasparenti.",
            "Il lancio istituzionale apre ora la fase operativa. Le prime valutazioni, la pubblicazione dei criteri e il modo in cui verranno gestiti eventuali conflitti d'interesse saranno i passaggi decisivi per costruire credibilità.",
        ],
        "fonti": [
            {"url": "https://au.int/en/newsevents/20261007/launch-africa-credit-rating-agency", "nome": "Unione Africana — lancio, percorso istituzionale e obiettivi di AfCRA."},
            {"url": "https://www.reuters.com/world/africa/african-union-launch-continents-first-credit-rating-agency-2026-10-07/", "nome": "Reuters — copertura dei rating e questioni di credibilità della nuova agenzia."},
        ],
        "image_source": "afcra",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un centro finanziario a Port Louis con la bandiera dell'Unione Africana; scena non documentaria.",
        "image_prompt": "Distretto finanziario di Port Louis a Mauritius con bandiera dell'Unione Africana e simboli di analisi del credito, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 11, 7, tzinfo=ROME),
    },
    {
        "slug": "africa-subsahariana-crescita-4-3-poverta-47-8-6-ottobre-2026",
        "titolo": "Africa subsahariana al 4,3%, ma la povertà resta al 47,8%",
        "sommario": "La Banca Mondiale alza la previsione di crescita per il 2026. Debito, poco spazio fiscale e scarsità di lavoro frenano l'impatto sulle famiglie.",
        "categoria": "Economia", "luogo": "Africa subsahariana", "formato": "flash",
        "parole_chiave_titolo": ["Africa subsahariana", "4,3%", "povertà"],
        "dati_chiave": [
            {"valore": "4,3%", "etichetta": "crescita prevista nel 2026"},
            {"valore": "47,8%", "etichetta": "povertà stimata nel 2026"},
            {"valore": "1,8%", "etichetta": "crescita pro capite"},
        ],
        "paragrafi": [
            "La Banca Mondiale prevede che l'economia dell'Africa subsahariana cresca del 4,3% nel 2026, rispetto al 4,1% del 2025. La stima dell'aggiornamento economico di ottobre è stata aumentata di 0,3 punti rispetto alla previsione pubblicata in aprile.",
            "Le prospettive sono state migliorate per quasi tre quarti dei Paesi della regione. La tenuta arriva nonostante tensioni geopolitiche, conflitti interni, shock climatici e condizioni finanziarie ancora difficili.",
            "La crescita del reddito pro capite dovrebbe salire dall'1,6% del 2025 all'1,8% nel 2026, per poi attestarsi in media intorno al 2% nel 2027-2028. Il progresso è più lento dell'espansione complessiva perché la popolazione aumenta rapidamente.",
            "Il rapporto avverte che il ritmo non basta a creare occupazione in misura adeguata né a ridurre fortemente la povertà estrema. Usando la soglia di 3 dollari al giorno a parità di potere d'acquisto del 2021, l'incidenza è stimata al 47,8% nel 2026 e al 47,1% nel 2027.",
            "Debito elevato e spazio fiscale limitato riducono la capacità dei governi di finanziare infrastrutture, capitale umano e protezione sociale. Il dato medio regionale nasconde inoltre differenze ampie tra economie esportatrici di materie prime, Paesi fragili e mercati più diversificati.",
            "La Banca Mondiale invita ad aumentare la preparazione all'intelligenza artificiale senza trascurare elettricità, connettività, competenze e regole. Per trasformare la crescita in redditi più alti serviranno investimenti produttivi e posti di lavoro, non soltanto un miglioramento del PIL aggregato.",
        ],
        "fonti": [
            {"url": "https://www.worldbank.org/en/region/afr/publication/africa-economic-update", "nome": "Banca Mondiale — Africa Economic Update, ottobre 2026."},
            {"url": "https://documents1.worldbank.org/curated/en/099553010072527291/pdf/IDU-1c39832f-80d1-49e8-9f45-41fc23bf5820.pdf", "nome": "Banca Mondiale — rapporto completo Africa's Pulse, ottobre 2026."},
        ],
        "image_source": "crescita",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una città africana con infrastrutture digitali ed energia solare; scena non documentaria.",
        "image_prompt": "Città africana moderna con data center, pannelli solari e grafico economico astratto senza cifre, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 11, 19, tzinfo=ROME),
    },
    {
        "slug": "usa-dfc-piu-investimenti-diretti-africa-minerali-9-ottobre-2026",
        "titolo": "Gli USA aumenteranno gli investimenti diretti in Africa",
        "sommario": "La DFC ha oltre 14 miliardi di dollari impegnati nel continente, più di tre nei minerali critici. Il debito resterà comunque lo strumento principale.",
        "categoria": "Economia", "luogo": "Africa", "formato": "flash",
        "parole_chiave_titolo": ["USA", "investimenti diretti", "Africa"],
        "dati_chiave": [
            {"valore": "$14 mld+", "etichetta": "impegni DFC in Africa"},
            {"valore": "$3 mld+", "etichetta": "legati ai minerali critici"},
            {"valore": "$155 mln", "etichetta": "quota prevista in WIOCC"},
        ],
        "paragrafi": [
            "La U.S. International Development Finance Corporation prevede di aumentare gli investimenti azionari diretti in Africa, con attenzione ai minerali critici e alle infrastrutture. Lo ha dichiarato a Reuters la responsabile regionale Vibhuti Jain il 9 ottobre.",
            "L'agenzia statunitense conta più di 14 miliardi di dollari di impegni nel continente. Oltre tre miliardi riguardano progetti minerari o attività collegate, tra cui terre rare, grafite e corridoi logistici.",
            "La DFC ha annunciato a settembre un investimento fino a 155 milioni di dollari nel fornitore africano di infrastrutture digitali WIOCC. Sarebbe il maggiore impegno azionario diretto mai assunto dall'agenzia.",
            "Jain ha precisato che prestiti, garanzie e assicurazioni contro il rischio politico resteranno gli strumenti prevalenti nel prossimo futuro. L'aumento delle partecipazioni non significa quindi che la DFC sostituirà il proprio modello di finanziamento con acquisti sistematici di quote societarie.",
            "La strategia è legata alla competizione per catene di approvvigionamento necessarie a veicoli elettrici, reti energetiche e tecnologie avanzate. Gli Stati Uniti cercano di ridurre la dipendenza dalla lavorazione cinese di molti minerali strategici.",
            "Tra i progetti sostenuti figura la riabilitazione del Corridoio di Lobito, che collega aree minerarie di Zambia e Repubblica Democratica del Congo ai porti atlantici dell'Angola. L'effetto locale dipenderà da occupazione, trasformazione industriale sul territorio e condizioni ambientali, oltre che dal volume di capitale mobilitato.",
        ],
        "fonti": [
            {"url": "https://www.reuters.com/world/africa/us-agency-do-more-equity-investing-africa-official-says-2026-10-09/", "nome": "Reuters — intervista alla responsabile Africa della DFC, 9 ottobre 2026."},
            {"url": "https://www.dfc.gov/", "nome": "U.S. International Development Finance Corporation — mandato, portafoglio e strumenti finanziari dell'agenzia."},
        ],
        "image_source": "dfc",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un treno merci lungo il Corridoio di Lobito; scena non documentaria.",
        "image_prompt": "Treno merci sul Corridoio di Lobito con infrastrutture portuali e bandiere USA e africana, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 11, 34, tzinfo=ROME),
    },
    {
        "slug": "somalia-afdb-finanza-sviluppo-crescita-privata-8-ottobre-2026",
        "titolo": "Somalia, AfDB punta su finanza e crescita privata",
        "sommario": "La Banca africana di sviluppo sostiene il passaggio dalla dipendenza dagli aiuti a investimenti di lungo periodo, istituzioni più forti e produzione interna.",
        "categoria": "Economia", "luogo": "Mogadiscio", "formato": "flash",
        "parole_chiave_titolo": ["Somalia", "AfDB", "crescita privata"],
        "dati_chiave": [
            {"valore": "1968", "etichetta": "nascita della banca nazionale"},
            {"valore": "2014", "etichetta": "ricostituzione della SDRB"},
            {"valore": "2060", "etichetta": "orizzonte della visione nazionale"},
        ],
        "paragrafi": [
            "La Banca africana di sviluppo ha confermato il sostegno alla transizione della Somalia dalla dipendenza dagli aiuti verso una crescita guidata dal settore privato. L'istituzione indica come priorità il rafforzamento delle strutture nazionali e la mobilitazione di finanziamenti di lungo periodo.",
            "L'impegno è stato presentato al Somalia Development Finance Forum, organizzato a Mogadiscio il 19 settembre dalla Somali Development and Reconstruction Bank e ripreso in una nota dell'AfDB pubblicata l'8 ottobre.",
            "La banca somala per lo sviluppo fu creata nel 1968 e ricostituita nel 2014. Il suo compito è usare capitale pubblico e partnership per sostenere investimenti, imprese e progetti che il credito commerciale fatica a finanziare da solo.",
            "Il presidente Hassan Sheikh Mohamud ha collegato la strategia alla National Vision 2060. Le aree indicate comprendono agricoltura, allevamento, pesca, energia, infrastrutture e attività capaci di creare occupazione.",
            "Il vicepremier Salah Jama ha sottolineato che il passaggio a una nuova finanza per lo sviluppo richiede capacità interne, non soltanto la sostituzione di un donatore con un altro. Questo significa migliorare gestione pubblica, selezione dei progetti e responsabilità sui risultati.",
            "La nota non annuncia un nuovo prestito con importo e scadenze già definiti. Il fatto nuovo è l'indirizzo operativo: usare istituzioni nazionali e capitale paziente per attirare investimenti privati, con l'efficacia che dovrà essere misurata sui progetti effettivamente finanziati.",
        ],
        "fonti": [
            {"url": "https://www.afdb.org/en/news-and-events/press-releases/african-development-bank-group-supports-somalias-97369", "nome": "Banca africana di sviluppo — sostegno alla transizione finanziaria della Somalia, 8 ottobre 2026."},
            {"url": "https://www.sonna.so/en/article/President-Hassan-Sheikh-Opens-Somalia-Development-Financing-Conference", "nome": "Agenzia nazionale somala SONNA — apertura e priorità del forum finanziario di Mogadiscio."},
        ],
        "image_source": "somalia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica del porto e delle infrastrutture di Mogadiscio; scena non documentaria.",
        "image_prompt": "Porto e skyline di Mogadiscio con infrastrutture in sviluppo e bandiere somala e AfDB, illustrazione editoriale ultrarealistica non documentaria.",
        "published": datetime(2026, 10, 9, 11, 49, tzinfo=ROME),
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
        "last_update": f"africa-news-v{VERSION}",
        "date": "2026-10-09",
        "release_date": "2026-10-09",
        "updated_at": "2026-10-09T11:49:00+02:00",
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
