#!/usr/bin/env python3
"""Release v824: dieci ultime notizie Italia e mondo del 9 ottobre 2026."""
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

VERSION = 824
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"
LOGO = ROOT / "curiomondo-logo-512.png"

IMAGE_SOURCES = {
    "comporti": GENERATED / "exec-7cc5769d-89f1-4891-ab47-c40515e9fe08.png",
    "ican": GENERATED / "exec-84c4575d-b11b-4bb0-a37d-a97506a6a22b.png",
    "guadalajara": GENERATED / "exec-509c0454-12fe-4f64-be95-563679f26a96.png",
    "industria": GENERATED / "exec-1608166f-23ef-4c0d-a38d-f2197b458ec6.png",
    "pillay": GENERATED / "exec-40d57cbb-9cb4-47a5-a2f1-c5f0bfd8e49d.png",
    "ets2": GENERATED / "exec-00821839-fa1c-4ada-ae33-da29be1d0db6.png",
    "grasslands": GENERATED / "exec-14e5b655-578d-4b9a-8637-61e74dd39152.png",
    "zambia": GENERATED / "exec-ebd5729d-0a87-4a32-932c-49c45fcf5987.png",
    "australia": GENERATED / "exec-f2a6d11a-90a7-4703-b6cc-bc67a91b5524.png",
    "salute_mentale": GENERATED / "exec-936fc8c7-459c-480b-9867-d7ec9873a7ef.png",
}


def make_variants(source: Path, slug: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 16 / 9
    if image.width / image.height > ratio:
        crop_width = round(image.height * ratio)
        left = (image.width - crop_width) // 2
        image = image.crop((left, 0, left + crop_width, image.height))
    else:
        crop_height = round(image.width / ratio)
        top = (image.height - crop_height) // 2
        image = image.crop((0, top, image.width, top + crop_height))

    logo = Image.open(LOGO).convert("RGBA")
    output = ROOT / "assets/images/editorial-auto"
    variants = []
    for width in (480, 800, 1200):
        height = round(width / ratio)
        canvas = image.resize((width, height), Image.Resampling.LANCZOS).convert("RGBA")
        logo_size = max(48, round(width * 0.105))
        mark = logo.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        mark.putalpha(mark.getchannel("A").point(lambda value: round(value * 0.92)))
        margin = max(10, round(width * 0.018))
        canvas.alpha_composite(mark, (width - logo_size - margin, height - logo_size - margin))
        path = output / f"{slug}-v{VERSION}-{width}.webp"
        canvas.convert("RGB").save(path, "WEBP", quality=89, method=6)
        variants.append({
            "w": width,
            "h": height,
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
        "sensitiveContext": article.pop("image_sensitive", False),
        "weatherMap": False,
        "reenactedEvent": False,
        "logoApplied": True,
    }
    likeness = article.pop("image_likeness", None)
    if likeness:
        image["syntheticLikeness"] = likeness
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
        "Le notizie più utili sono quelle che chiariscono cosa accade dopo.",
        "Una rete funziona quando ogni nodo condivide informazioni affidabili.",
        "Un libro attraversa i confini prima ancora di essere tradotto.",
        "Dietro un dato economico ci sono imprese, lavoro e scelte quotidiane.",
        "La giustizia diventa pace quando protegge davvero le persone.",
        "Le regole sul clima contano quando rendono prevedibile il cambiamento.",
        "Proteggere un paesaggio significa custodire anche l'acqua che lo attraversa.",
        "La stabilità cresce quando i numeri restano verificabili.",
        "Riparare la natura richiede tempo, cura e continuità.",
        "La salute mentale appartiene alla comunità, non all'isolamento.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


ARTICLES = [
    {
        "slug": "carlo-comporti-presidente-esma-1-novembre-2026",
        "titolo": "ESMA, Carlo Comporti presidente dal 1° novembre",
        "sommario": "Il Consiglio dell'UE ha formalizzato la nomina dell'attuale commissario Consob. Il mandato durerà cinque anni e potrà essere rinnovato una volta.",
        "categoria": "Economia", "luogo": "Unione europea", "formato": "flash",
        "parole_chiave_titolo": ["Carlo Comporti", "ESMA"],
        "dati_chiave": [
            {"valore": "1° novembre", "etichetta": "inizio del mandato"},
            {"valore": "5 anni", "etichetta": "durata dell'incarico"},
            {"valore": "15 settembre", "etichetta": "via libera del Parlamento UE"},
        ],
        "paragrafi": [
            "Il Consiglio dell'Unione europea ha nominato formalmente Carlo Comporti presidente dell'Autorità europea degli strumenti finanziari e dei mercati, l'ESMA. L'incarico inizierà il 1° novembre 2026 e durerà cinque anni, con la possibilità di un solo rinnovo.",
            "Comporti è attualmente commissario della Consob e fa già parte sia del consiglio delle autorità di vigilanza sia del consiglio di gestione dell'ESMA. La procedura era partita da una rosa di due candidati selezionata dall'autorità europea.",
            "Gli ambasciatori dei Ventisette avevano raggiunto un accordo preliminare a luglio. Il Parlamento europeo ha poi approvato la scelta il 15 settembre, aprendo la strada alla decisione definitiva del Consiglio.",
            "L'ESMA, con sede a Parigi, coordina la vigilanza sui mercati finanziari europei. Tra le sue priorità rientrano la protezione degli investitori, la stabilità dei mercati, la convergenza dei controlli nazionali e l'uso efficace dei dati.",
            "Per risparmiatori e intermediari la nomina non modifica subito regole o prodotti. Indica però chi guiderà per il prossimo quinquennio l'autorità chiamata a intervenire su mercati, finanza sostenibile e innovazione digitale.",
        ],
        "fonti": [
            {"url": "https://www.consilium.europa.eu/en/press/press-releases/2026/10/09/carlo-comporti-appointed-chair-of-the-european-securities-and-markets-authority/", "nome": "Consiglio dell'UE — nomina e procedura per la presidenza ESMA."},
            {"url": "https://www.esteri.it/it/sala_stampa/archivionotizie/comunicati/2026/10/tajani-si-congratula-con-carlo-comporti-per-la-nomina-alla-presidenza-dellesma/", "nome": "Farnesina — comunicato sulla nomina di Carlo Comporti."},
        ],
        "image_source": "comporti", "image_likeness": "public-figure",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di Carlo Comporti in una sede europea di vigilanza finanziaria; scena non documentaria.",
        "image_prompt": "Carlo Comporti nella sede di un'autorità finanziaria europea a Parigi, ritratto istituzionale ultrarealistico con volto riconoscibile e logo CurioMondo applicato in post-produzione.",
    },
    {
        "slug": "ndrangheta-progetto-i-can-181-arresti-32-paesi-2026",
        "titolo": "’Ndrangheta, il progetto I-CAN arriva a 181 arresti",
        "sommario": "Il Viminale aggiorna i risultati della cooperazione internazionale coordinata con Interpol. Il progetto collega forze di polizia e banche dati in 32 Paesi.",
        "categoria": "Italia", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["I-CAN", "181 arresti"],
        "dati_chiave": [
            {"valore": "181", "etichetta": "arresti indicati dal Viminale"},
            {"valore": "32 Paesi", "etichetta": "rete internazionale coinvolta"},
            {"valore": "dal 2020", "etichetta": "progetto operativo"},
        ],
        "paragrafi": [
            "Il progetto I-CAN per il contrasto internazionale alla 'ndrangheta ha raggiunto 181 arresti in 32 Paesi, secondo l'aggiornamento pubblicato dal Ministero dell'Interno. L'iniziativa è coordinata dal Dipartimento della Pubblica Sicurezza italiano insieme a Interpol.",
            "I-CAN, avviato nel 2020, mette in collegamento le forze di polizia per condividere informazioni, analisi e strumenti utili a rintracciare persone ricercate e ricostruire reti criminali che operano oltre i confini nazionali.",
            "Interpol indica che il progetto ha sviluppato un archivio analitico criminale con più di 75.000 entità collegate alla 'ndrangheta. Il numero comprende persone, società, luoghi e relazioni utilizzati dagli investigatori per confrontare casi diversi.",
            "Il dato sugli arresti descrive risultati cumulativi del progetto e non una singola operazione svolta oggi. Ogni persona coinvolta resta soggetta alle regole processuali del Paese competente e alla presunzione di innocenza fino a sentenza definitiva.",
            "La novità riguarda soprattutto l'estensione della cooperazione: la capacità di incrociare segnalazioni e movimenti in tempi rapidi riduce gli spazi in cui i latitanti possono sottrarsi alle ricerche cambiando Stato.",
        ],
        "fonti": [
            {"url": "https://www.interno.gov.it/it/notizie/contrasto-alla-ndrangheta-181-arresti-32-paesi-grazie-progetto-i-can", "nome": "Ministero dell'Interno — aggiornamento sui risultati del progetto I-CAN."},
            {"url": "https://www.interpol.int/Crimes/Organized-crime/Projects/INTERPOL-Cooperation-against-Ndrangheta-I-CAN-Phase-2", "nome": "Interpol — struttura, Paesi e strumenti della seconda fase I-CAN."},
        ],
        "image_source": "ican", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una sala internazionale di coordinamento di polizia per il progetto I-CAN; scena non documentaria.",
        "image_prompt": "Analisti italiani e internazionali in una sala di coordinamento contro la criminalità organizzata, scena neutrale senza arresti né sospetti, logo CurioMondo in post-produzione.",
    },
    {
        "slug": "italia-ospite-onore-fiera-libro-guadalajara-2026-programma",
        "titolo": "Guadalajara, l'Italia svela il programma della Fiera del Libro",
        "sommario": "Dal 28 novembre al 6 dicembre sono previsti oltre 120 incontri, nove concerti e più di quindici mostre e performance. Baricco aprirà il programma letterario.",
        "categoria": "Cultura", "luogo": "Guadalajara", "formato": "flash",
        "parole_chiave_titolo": ["Guadalajara", "Italia ospite d'onore"],
        "dati_chiave": [
            {"valore": "28 nov-6 dic", "etichetta": "date della Fiera"},
            {"valore": "120+", "etichetta": "incontri italiani"},
            {"valore": "30+", "etichetta": "editori nel padiglione"},
        ],
        "paragrafi": [
            "È online il programma completo della partecipazione italiana alla quarantesima Fiera internazionale del Libro di Guadalajara, in calendario dal 28 novembre al 6 dicembre. L'Italia torna ospite d'onore dopo diciotto anni.",
            "Il cartellone comprende oltre 120 incontri letterari e professionali con circa sessanta autrici e autori. Alessandro Baricco, in dialogo con la scrittrice messicana Valeria Luiselli, aprirà il programma letterario il 29 novembre alle 12:30 nell'Auditorium Juan Rulfo.",
            "Il padiglione italiano ospiterà più di trenta editori e una libreria con opere in lingua originale e traduzioni spagnole. Sono annunciati anche nove concerti e oltre quindici mostre e performance, oltre ad appuntamenti dedicati a cinema, gastronomia e scambi accademici.",
            "Il filo conduttore scelto per la presenza italiana è una frase di Umberto Eco: «Il mondo ci parla come un grande libro». Una parte del programma sarà dedicata ai rapporti tra editoria italiana e latinoamericana e a nuovi progetti di traduzione.",
            "La FIL riunisce ogni anno più di 800 scrittori, 18.000 professionisti e 2.800 case editrici da oltre sessanta Paesi. Il Ministero della Cultura indica un pubblico atteso vicino al milione di visitatori nei nove giorni della manifestazione.",
        ],
        "fonti": [
            {"url": "https://cultura.gov.it/comunicato/29387", "nome": "Ministero della Cultura — programma dell'Italia ospite d'onore alla FIL 2026."},
        ],
        "image_source": "guadalajara",
        "image_alt": "Illustrazione editoriale IA ultrarealistica del padiglione italiano alla Fiera del Libro di Guadalajara con editori e visitatori; scena non documentaria.",
        "image_prompt": "Padiglione italiano contemporaneo alla Fiera internazionale del Libro di Guadalajara, editori e visitatori con volti visibili, logo CurioMondo in post-produzione.",
    },
    {
        "slug": "produzione-industriale-italia-agosto-2026-calo-istat",
        "titolo": "Industria italiana, produzione -1,3% ad agosto",
        "sommario": "L'indice destagionalizzato arretra rispetto a luglio e cala dell'1,1% nel trimestre giugno-agosto. Su base annua il livello resta invariato.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Produzione industriale", "-1,3%"],
        "dati_chiave": [
            {"valore": "-1,3%", "etichetta": "rispetto a luglio"},
            {"valore": "-1,1%", "etichetta": "nel trimestre"},
            {"valore": "0,0%", "etichetta": "su agosto 2025"},
        ],
        "paragrafi": [
            "La produzione industriale italiana è diminuita dell'1,3% ad agosto 2026 rispetto a luglio, secondo l'indice destagionalizzato diffuso da Istat. Nella media del trimestre giugno-agosto il livello è sceso dell'1,1% rispetto ai tre mesi precedenti.",
            "Il confronto con agosto 2025, corretto per gli effetti di calendario, mostra invece una variazione nulla. I giorni lavorativi sono stati ventuno in entrambi i periodi, rendendo il confronto annuale meno influenzato dal calendario.",
            "Tra i raggruppamenti principali, la lettura mensile misura l'andamento complessivo di beni di consumo, beni strumentali, intermedi ed energia. Il comunicato va interpretato come un indicatore dell'attività delle fabbriche, non come una misura diretta del Pil o dell'occupazione.",
            "Su base annua gli aumenti maggiori riguardano la fornitura di energia elettrica e gas, in crescita del 14,5%, le altre industrie manifatturiere e riparazioni, al 2%, e i mezzi di trasporto, all'1%.",
            "Un solo mese può risentire di fermate produttive e calendario estivo. Per capire se la flessione anticipi una fase più debole serviranno i dati di settembre e il confronto con ordini, fatturato ed esportazioni.",
        ],
        "fonti": [
            {"url": "https://www.istat.it/comunicato-stampa/produzione-industriale-agosto-2026/", "nome": "Istat — produzione industriale di agosto 2026."},
        ],
        "image_source": "industria",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di tecnici in uno stabilimento industriale italiano automatizzato; scena non documentaria.",
        "image_prompt": "Tecnici in uno stabilimento italiano moderno osservano una linea produttiva, atmosfera analitica non allarmistica, logo CurioMondo in post-produzione.",
    },
    {
        "slug": "navi-pillay-premio-nobel-pace-2026",
        "titolo": "Nobel per la Pace 2026 a Navi Pillay",
        "sommario": "Il Comitato norvegese premia la giurista sudafricana per l'impegno a favore della pace e del diritto internazionale. La motivazione richiama il contrasto ai crimini più gravi.",
        "categoria": "Mondo", "luogo": "Oslo", "formato": "flash",
        "parole_chiave_titolo": ["Navi Pillay", "Nobel per la Pace"],
        "dati_chiave": [
            {"valore": "2026", "etichetta": "edizione del premio"},
            {"valore": "1999-2003", "etichetta": "presidenza del Tribunale per il Ruanda"},
            {"valore": "2008-2014", "etichetta": "guida dei diritti umani ONU"},
        ],
        "paragrafi": [
            "Il Premio Nobel per la Pace 2026 è stato assegnato a Navanethem «Navi» Pillay per i suoi sforzi a favore della pace e del diritto internazionale. L'annuncio è arrivato il 9 ottobre dal Comitato norvegese per il Nobel.",
            "La motivazione sottolinea il contributo della giurista sudafricana alla costruzione di un ordine giuridico capace di perseguire crimini di guerra, crimini contro l'umanità e genocidio. Il premio riconosce un percorso sviluppato tra avvocatura, tribunali internazionali e Nazioni Unite.",
            "Pillay ha difeso attivisti anti-apartheid, è stata giudice e presidente del Tribunale penale internazionale per il Ruanda e ha fatto parte della Camera d'appello della Corte penale internazionale. In seguito ha guidato l'Alto commissariato ONU per i diritti umani.",
            "Oggi opera anche come giudice ad hoc presso la Corte internazionale di giustizia. La presidenza sudafricana ha accolto il riconoscimento come un tributo al coraggio, all'integrità e all'impegno della giurista per la dignità umana.",
            "L'assegnazione è il risultato ufficiale dell'edizione 2026, non una previsione. Cerimonia, consegna e discorso della vincitrice seguiranno il calendario stabilito dalla Fondazione Nobel.",
        ],
        "fonti": [
            {"url": "https://www.nobelprize.org/prizes/peace/2026/press-release/", "nome": "Nobel Prize — annuncio e motivazione del Premio per la Pace 2026."},
            {"url": "https://www.gov.za/news/media-statements/president-cyril-ramaphosa-congratulates-justice-navy-pillay-laureate-2026", "nome": "Presidenza del Sudafrica — profilo e congratulazioni a Navi Pillay."},
        ],
        "image_source": "pillay", "image_likeness": "public-figure",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di Navi Pillay in una biblioteca con Oslo sullo sfondo; scena non documentaria.",
        "image_prompt": "Ritratto riconoscibile e dignitoso di Navi Pillay in una biblioteca dedicata al diritto internazionale, senza cerimonia o medaglia, logo CurioMondo in post-produzione.",
    },
    {
        "slug": "ets2-riserva-stabilita-prezzi-carbonio-ue-2028",
        "titolo": "ETS2, l'UE rafforza la riserva contro i picchi di prezzo",
        "sommario": "Il Consiglio approva in via definitiva le modifiche per edifici e trasporti. Con CO2 oltre 45 euro saranno liberate 40 milioni di quote.",
        "categoria": "Ambiente", "luogo": "Unione europea", "formato": "flash",
        "parole_chiave_titolo": ["ETS2", "40 milioni di quote"],
        "dati_chiave": [
            {"valore": "40 milioni", "etichetta": "quote liberabili"},
            {"valore": "45 euro", "etichetta": "soglia in prezzi 2020"},
            {"valore": "2028", "etichetta": "avvio completo previsto"},
        ],
        "paragrafi": [
            "Il Consiglio dell'Unione europea ha approvato definitivamente la modifica della riserva di stabilità dell'ETS2, il sistema di scambio delle emissioni destinato a edifici, trasporto stradale e altri settori. L'obiettivo è rendere più regolare l'avvio completo previsto nel 2028.",
            "La riserva regola automaticamente il numero di quote disponibili, intervenendo quando l'offerta è troppo alta o troppo bassa. Le nuove norme ne prolungano la durata oltre il 2030 e puntano a ridurre volatilità e aumenti eccessivi del prezzo del carbonio.",
            "Se il costo supera 45 euro per tonnellata di CO2 equivalente, espresso in prezzi del 2020, le quote liberabili raddoppiano da 20 a 40 milioni. È prevista anche un'uscita più graduale quando le quote in circolazione scendono sotto 260 milioni.",
            "L'ETS2 si applica a monte ai distributori di combustibili, che dovranno monitorare le emissioni dei prodotti venduti e restituire quote equivalenti. Questo non equivale a una nuova tassa applicata oggi direttamente alla singola famiglia o al singolo automobilista.",
            "La decisione sarà firmata e pubblicata nella Gazzetta ufficiale dell'UE. Entrerà in vigore venti giorni dopo la pubblicazione, in tempo per preparare il funzionamento della riserva prima del lancio del sistema.",
        ],
        "fonti": [
            {"url": "https://www.consilium.europa.eu/en/press/press-releases/2026/10/09/ets2-council-signs-off-on-rules-strengthening-the-market-stability-reserve/", "nome": "Consiglio dell'UE — adozione finale delle nuove regole per la riserva ETS2."},
        ],
        "image_source": "ets2",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di edifici efficienti e trasporti in una città europea davanti alle istituzioni UE; scena non documentaria.",
        "image_prompt": "Edifici, trasporti e istituzioni europee in una scena urbana che rappresenta il mercato ETS2, professionisti con volti visibili, logo CurioMondo in post-produzione.",
    },
    {
        "slug": "sudafrica-nuovo-grasslands-national-park-eastern-cape-2026",
        "titolo": "Sudafrica, nasce il Grasslands National Park",
        "sommario": "Diciotto proprietà per oltre 10.225 ettari diventano parco nazionale nell'Eastern Cape. I proprietari mantengono i terreni con accordi di conservazione.",
        "categoria": "Ambiente", "luogo": "Eastern Cape", "formato": "flash",
        "parole_chiave_titolo": ["Grasslands National Park", "10.225 ettari"],
        "dati_chiave": [
            {"valore": "10.225,9 ha", "etichetta": "superficie dichiarata"},
            {"valore": "18", "etichetta": "proprietà coinvolte"},
            {"valore": "1°", "etichetta": "parco nato soprattutto da stewardship"},
        ],
        "paragrafi": [
            "Il Sudafrica ha istituito il Grasslands National Park nell'Eastern Cape, riunendo diciotto proprietà per una superficie complessiva di 10.225,9242 ettari. La dichiarazione è stata pubblicata nella Gazzetta governativa numero 55531.",
            "Il parco si trova sugli altopiani tra Nqanqarhu e Rhodes. Protegge ecosistemi di prateria ancora poco rappresentati nella rete nazionale e una parte dell'area strategica per le risorse idriche dei Drakensberg orientali.",
            "La gestione è stata affidata a South African National Parks. Il progetto coinvolge anche il dipartimento nazionale dell'Ambiente, WWF South Africa e proprietari locali attraverso accordi di lungo periodo.",
            "Il modello è quello della biodiversity stewardship: i proprietari conservano la titolarità dei terreni, ma si impegnano a rispettare piani concordati di tutela e gestione. Le attività agricole compatibili potranno continuare.",
            "Secondo il governo, è il primo parco nazionale sudafricano creato principalmente con questo modello. La misura mira quindi a combinare protezione di biodiversità e acqua con la continuità delle economie rurali già presenti.",
        ],
        "fonti": [
            {"url": "https://www.gov.za/news/media-statements/minister-david-maynier-declares-new-national-park-eastern-cape-09-oct-2026", "nome": "Governo del Sudafrica — dichiarazione del Grasslands National Park."},
        ],
        "image_source": "grasslands",
        "image_alt": "Illustrazione editoriale IA ultrarealistica delle praterie dell'Eastern Cape con ranger e proprietari nel nuovo Grasslands National Park; scena non documentaria.",
        "image_prompt": "Praterie montane dell'Eastern Cape nel nuovo Grasslands National Park con ranger e proprietari, paesaggio centrale, logo CurioMondo in post-produzione.",
    },
    {
        "slug": "zambia-fmi-accordo-nuovo-programma-36-mesi-2026",
        "titolo": "Zambia e FMI, accordo tecnico su un programma da 36 mesi",
        "sommario": "L'intesa prevede accesso potenziale a 1,472 miliardi di dollari, ma deve ancora ricevere l'approvazione del Consiglio esecutivo del Fondo.",
        "categoria": "Economia", "luogo": "Lusaka", "formato": "flash",
        "parole_chiave_titolo": ["Zambia e FMI", "36 mesi"],
        "dati_chiave": [
            {"valore": "36 mesi", "etichetta": "durata proposta"},
            {"valore": "$1,472 mld", "etichetta": "accesso potenziale"},
            {"valore": "5,6%", "etichetta": "crescita 2026 stimata"},
        ],
        "paragrafi": [
            "Lo staff del Fondo monetario internazionale e le autorità dello Zambia hanno raggiunto un accordo tecnico su un nuovo programma triennale nell'ambito dell'Extended Credit Facility. L'intesa riguarda politiche economiche e riforme da attuare nei prossimi 36 mesi.",
            "L'accesso proposto ammonta a 1,076 miliardi di diritti speciali di prelievo, equivalenti a circa 1,472 miliardi di dollari. Le risorse non sono ancora disponibili: servono alcune azioni preliminari concordate e l'approvazione del Consiglio esecutivo del FMI.",
            "Il Fondo prevede una crescita reale del Pil zambiano del 5,6% nel 2026, sostenuta da agricoltura, miniere ed esportazioni. Le riserve lorde sono indicate a 6,1 miliardi di dollari in settembre.",
            "L'inflazione è scesa al 6,1% in settembre. Il dato è coerente con l'aggiornamento dell'agenzia statistica zambiana, che segnala un'inflazione alimentare annua del 5,8%, in calo dal 6% di agosto.",
            "Il programma proposto punta a ricostruire margini fiscali e riserve, tutelare la sostenibilità del debito e rafforzare trasparenza e gestione delle finanze pubbliche. Questi sono obiettivi negoziali: risultati e condizioni effettive dipenderanno dall'approvazione e dall'attuazione delle misure.",
        ],
        "fonti": [
            {"url": "https://www.imf.org/en/news/articles/2026/10/09/pr26331-zambia-new-ecf", "nome": "FMI — accordo tecnico per il nuovo programma ECF dello Zambia."},
            {"url": "https://www.zamstats.gov.zm/annual-food-and-non-food-inflation-september-2026/", "nome": "Zambia Statistics Agency — inflazione alimentare e non alimentare di settembre 2026."},
        ],
        "image_source": "zambia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di funzionari zambiani e internazionali riuniti a Lusaka; scena non documentaria.",
        "image_prompt": "Funzionari economici zambiani e internazionali in riunione a Lusaka, scena di lavoro neutrale senza cerimonia, logo CurioMondo in post-produzione.",
    },
    {
        "slug": "australia-nature-repair-cooplacurripa-1230-ettari-2026",
        "titolo": "Australia, 1.230 ettari entrano nel Nature Repair Market",
        "sommario": "Il quarto progetto registrato ripristinerà foreste e praterie native nel New South Wales. Il pascolo potrà riprendere quando le piantagioni saranno stabilizzate.",
        "categoria": "Ambiente", "luogo": "New South Wales", "formato": "flash",
        "parole_chiave_titolo": ["1.230 ettari", "Nature Repair Market"],
        "dati_chiave": [
            {"valore": "1.230 ha", "etichetta": "area da ripristinare"},
            {"valore": "4° progetto", "etichetta": "registrato nel mercato"},
            {"valore": "3 ecosistemi", "etichetta": "foresta, eucalipti e praterie"},
        ],
        "paragrafi": [
            "L'Australia ha registrato il quarto progetto del Nature Repair Market, il mercato nazionale dedicato agli interventi misurabili sulla biodiversità. L'area si trova a Cooplacurripa Station, nel nord-est del New South Wales.",
            "Il progetto Silva Capital Cooplacurripa Biodiversity Project No. 2 punta a ripristinare 1.230 ettari con piantagioni scaglionate. Gli interventi riguarderanno foresta pluviale, boschi di eucalipto e praterie boscate native.",
            "È il secondo progetto del programma registrato nella stessa proprietà. Il promotore intende affiancare ai risultati di biodiversità attività di assorbimento del carbonio previste dal sistema australiano delle unità di credito ACCU.",
            "Questa combinazione, definita stacking, permette di far convivere nello stesso intervento risultati ambientali diversi. La registrazione non certifica in anticipo i risultati: il ripristino dovrà essere realizzato e monitorato secondo il metodo approvato.",
            "Il terreno continuerà a essere usato anche per la produzione agricola. Il regolatore prevede che il pascolo possa riprendere dopo l'attecchimento delle nuove piante, mostrando come tutela e attività rurali possano essere organizzate nella stessa area.",
        ],
        "fonti": [
            {"url": "https://cer.gov.au/news-and-media/news/2026/october/fourth-project-registered-under-nature-repair-market", "nome": "Clean Energy Regulator australiano — quarto progetto del Nature Repair Market."},
        ],
        "image_source": "australia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di operatori che piantano specie native a Cooplacurripa Station nel New South Wales; scena non documentaria.",
        "image_prompt": "Ripristino di foreste e praterie native a Cooplacurripa Station con operatori e paesaggio australiano, logo CurioMondo in post-produzione.",
    },
    {
        "slug": "oms-salute-mentale-cure-comunita-guida-9-ottobre-2026",
        "titolo": "Salute mentale, l'OMS chiede più cure nella comunità",
        "sommario": "La nuova guida propone di ridurre ricoveri lunghi e istituzionalizzazione. Solo il 9% dei Paesi dichiara di aver completato il passaggio ai servizi territoriali.",
        "categoria": "Salute", "luogo": "Ginevra", "formato": "flash",
        "parole_chiave_titolo": ["Salute mentale", "cure nella comunità"],
        "dati_chiave": [
            {"valore": "9%", "etichetta": "Paesi con passaggio completato"},
            {"valore": "53%", "etichetta": "ancora nelle fasi iniziali"},
            {"valore": "28%", "etichetta": "ricoveri oltre sei mesi"},
        ],
        "paragrafi": [
            "L'Organizzazione mondiale della sanità ha pubblicato una guida per aiutare i Paesi a spostare la salute mentale dai grandi istituti con lunghe permanenze verso servizi radicati nella comunità e rispettosi delle scelte delle persone.",
            "Il processo riguarda in particolare chi trascorre almeno sei mesi in ospedali psichiatrici o strutture sociali. La guida propone di ridurre ricoveri eccessivamente lunghi, modificare pratiche che limitano i diritti e preparare il ritorno alla vita quotidiana.",
            "Secondo il Mental Health Atlas dell'OMS, soltanto il 9% dei Paesi che hanno risposto dichiara di avere completato la transizione verso cure territoriali. Il 53% è ancora in una fase iniziale e il 28% delle persone ricoverate resta in ospedale per più di sei mesi.",
            "L'OMS chiarisce che dimettere non basta. Servono alloggi, assistenza sanitaria, sostegno sociale, istruzione, lavoro e supporto alle famiglie, costruiti insieme alle persone con esperienza diretta dei servizi.",
            "La guida è destinata soprattutto a governi e responsabili degli ospedali e non sostituisce una valutazione clinica individuale. Il messaggio operativo è trasferire risorse e competenze senza interrompere le cure necessarie o lasciare sole le persone più fragili.",
        ],
        "fonti": [
            {"url": "https://www.who.int/news/item/09-10-2026-who-urges-shift-from-institutional-to-community-based-mental-health-care", "nome": "Organizzazione mondiale della sanità — nuova guida sulle cure di salute mentale nella comunità."},
        ],
        "image_source": "salute_mentale",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un incontro rispettoso in un centro di salute mentale di comunità; scena non documentaria.",
        "image_prompt": "Centro di salute mentale integrato nel quartiere con utenti e operatori in conversazione, scena dignitosa e non stigmatizzante, logo CurioMondo in post-produzione.",
    },
]


def main() -> None:
    append_name_phrases()
    base = datetime.now(ROME).replace(microsecond=0)
    minute_offsets = (0, 7, 16, 27, 39, 51, 64, 78, 92, 108)
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
        "last_update": f"italia-mondo-v{VERSION}",
        "date": base.date().isoformat(),
        "release_date": base.date().isoformat(),
        "updated_at": base.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
