#!/usr/bin/env python3
"""Release v814: sport, film e serie TV, cronaca e meteo del 9 ottobre 2026."""
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

VERSION = 814
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"

IMAGE_SOURCES = {
    "nba": GENERATED / "exec-83dfb98e-c5f3-4a0e-b705-9078cad7cbd5.png",
    "vonn": GENERATED / "exec-17f4e29b-df95-4110-9f90-adc150b6716c.png",
    "hurkacz": GENERATED / "exec-6bfa601d-b43a-42e1-856c-52d05c9ab0a2.png",
    "dustfall": GENERATED / "exec-b6681979-2466-4bbb-a002-7709c72b5fe5.png",
    "stick": GENERATED / "exec-7247c8f9-cac2-4abe-bd1a-f0572e1fcb2c.png",
    "reich": GENERATED / "exec-b94b9cf9-13b5-44f9-9227-d06368b1bf32.png",
    "apocalypse": GENERATED / "exec-185532e0-145f-4840-9567-e7ab7888cb53.png",
    "fiumicino": GENERATED / "exec-c1b51402-7207-4945-84f8-89e9197d0ba5.png",
    "frattamaggiore": GENERATED / "exec-bdacf8f4-c74a-404c-9efc-757b9fd73aa7.png",
    "meteo": GENERATED / "exec-ed59f5a0-0c9b-4896-a5ac-47b334c98c38.png",
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
    rows = []
    output = ROOT / "assets/images/editorial-auto"
    for width in (480, 800, 1200):
        path = output / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, round(width / ratio)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=89, method=6
        )
        rows.append({
            "w": width,
            "h": round(width / ratio),
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return rows


def make_image(article: dict) -> dict:
    record = {
        "key": f"{article['slug']}-v{VERSION}",
        "alt": article.pop("image_alt"),
        "prompt": article.pop("image_prompt"),
        "variants": make_variants(IMAGE_SOURCES[article.pop("image_source")], article["slug"]),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": article.pop("sensitive_context", False),
        "weatherMap": False,
        "reenactedEvent": False,
    }
    if article.pop("public_figure", False):
        record["syntheticLikeness"] = "public-figure"
    if record["sensitiveContext"]:
        record["portraitOnly"] = True
        record["portraitFormat"] = "neutral-isolated"
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
    if slug == "nba-china-games-2026-rockets-mavericks-macao-orari-diretta":
        for node in doc.xpath('//main//div[contains(concat(" ",normalize-space(@class)," ")," badge ")][1]'):
            node.text = "Sport"
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )


ARTICLES = [
    {
        "slug": "allerta-meteo-oggi-9-ottobre-2026-arancione-lazio-campania",
        "titolo": "Allerta meteo oggi: arancione in Lazio e Campania, gialla in 14 regioni",
        "sommario": "Il bollettino nazionale segnala temporali e rischio idrogeologico per venerdì 9 ottobre. Le zone arancioni interessano tre bacini del Lazio e l'area di Napoli.",
        "categoria": "Meteo", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["arancione", "14 regioni"],
        "dati_chiave": [
            {"valore": "2 regioni", "etichetta": "con aree in codice arancione"},
            {"valore": "14 regioni", "etichetta": "interessate dal codice giallo"},
            {"valore": "9 ottobre", "etichetta": "validità del bollettino"},
        ],
        "paragrafi": [
            "La Protezione Civile segnala per oggi, venerdì 9 ottobre 2026, criticità arancione in settori di Lazio e Campania e criticità gialla in porzioni di altre dodici regioni. Il quadro deriva dal bollettino nazionale pubblicato l'8 ottobre e riguarda soprattutto temporali, rischio idrogeologico e possibili effetti sul reticolo idraulico.",
            "Nel Lazio il livello arancione riguarda Liri, Bacini Costieri Sud e Aniene per rischio idrogeologico legato ai temporali. In Campania è arancione la zona che comprende la Piana campana, Napoli, le isole e l'area vesuviana, dove la valutazione si concentra sul rischio idrogeologico.",
            "Il codice giallo compare, con tipologie e zone differenti, in Piemonte, Lombardia, Friuli Venezia Giulia, Lazio, Campania, Toscana, Marche, Umbria, Abruzzo, Molise, Basilicata, Puglia, Calabria e Sicilia. Non significa che l'intero territorio di ogni regione sia coinvolto allo stesso modo: la mappa ufficiale distingue i singoli settori.",
            "Durante i temporali intensi possono verificarsi allagamenti rapidi, caduta di rami, difficoltà nei sottopassi e innalzamenti dei corsi d'acqua minori. La situazione può cambiare anche a breve distanza, quindi il colore regionale va letto insieme agli avvisi del Comune e della Protezione Civile locale.",
            "Chi deve spostarsi dovrebbe evitare scantinati, rive, ponti bassi e strade già interessate da accumuli d'acqua. In auto non bisogna attraversare un tratto allagato: profondità e forza della corrente non sono valutabili dal veicolo e possono aumentare in pochi minuti.",
            "Il bollettino nazionale offre una sintesi previsionale, non una cronaca in tempo reale. Per scuola, trasporti, viabilità e chiusure decide l'autorità locale competente; prima di uscire è utile controllare i canali ufficiali del proprio Comune e gli eventuali aggiornamenti regionali.",
        ],
        "fonti": [{"url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/", "nome": "Dipartimento della Protezione Civile — bollettino nazionale di criticità per il 9 ottobre 2026."}],
        "image_source": "meteo",
        "image_alt": "Illustrazione editoriale IA di un forte temporale su Roma e sul Tevere; scena meteorologica non documentaria e senza mappa.",
        "image_prompt": "Scena meteorologica fotorealistica su Roma e sul Tevere durante un forte temporale, pioggia intensa e fulmini lontani, nessuna mappa o testo.",
    },
    {
        "slug": "nba-china-games-2026-rockets-mavericks-macao-orari-diretta",
        "titolo": "NBA China Games oggi a Macao: Rockets-Mavericks, orari e diretta",
        "sommario": "Houston e Dallas giocano il 9 e l'11 ottobre alla Venetian Arena. Le due amichevoli di preseason sono trasmesse da NBA TV e League Pass.",
        "categoria": "Sport", "luogo": "Macao", "formato": "flash",
        "parole_chiave_titolo": ["NBA China Games", "Rockets-Mavericks"],
        "dati_chiave": [
            {"valore": "9 e 11 ott", "etichetta": "le due partite a Macao"},
            {"valore": "16ª edizione", "etichetta": "degli NBA China Games"},
            {"valore": "NBA TV", "etichetta": "con League Pass per la diretta"},
        ],
        "paragrafi": [
            "Gli NBA China Games 2026 portano Houston Rockets e Dallas Mavericks alla Venetian Arena di Macao per due partite di preseason. La prima è in programma oggi, venerdì 9 ottobre, alle 20 locali, le 14 in Italia; la seconda si gioca domenica 11 ottobre alle 18 locali, mezzogiorno italiano.",
            "Negli Stati Uniti gli orari indicati dalla NBA sono le 8 del mattino sulla costa orientale per gara 1 e le 6 per gara 2. La lega segnala la trasmissione su NBA TV e NBA League Pass, con disponibilità che può dipendere dal Paese e dalle condizioni dell'abbonamento.",
            "L'attenzione è rivolta anche ai volti delle due squadre: Kevin Durant guida il nuovo corso dei Rockets, mentre Dallas presenta Cooper Flagg e un gruppo costruito per valutare rotazioni e intese prima della stagione regolare. Trattandosi di preseason, minutaggi e quintetti possono cambiare fino alla palla a due.",
            "Quella di Macao è la sedicesima edizione dell'evento. Secondo la NBA, dal 2004 le squadre della lega hanno disputato trenta partite in Cina, un percorso interrotto per diversi anni e ora ripreso con una doppia sfida nello stesso impianto.",
            "Le partite fanno parte di cinque appuntamenti internazionali di preseason annunciati dalla lega. Il risultato non incide sulla classifica della regular season, ma offre agli allenatori un test contro un avversario NBA e al pubblico asiatico un evento dal vivo con roster di primo piano.",
            "Per seguire l'incontro dall'Italia conviene verificare la schermata dell'evento su League Pass poco prima dell'inizio. Eventuali restrizioni territoriali, repliche e commenti disponibili sono gestiti dal servizio ufficiale e possono differire rispetto alla programmazione statunitense di NBA TV.",
        ],
        "fonti": [{"url": "https://www.nba.com/news/2026-nba-china-games-everything-to-know", "nome": "NBA — programma, orari e informazioni ufficiali sui China Games 2026."}],
        "image_source": "nba", "public_figure": True,
        "image_alt": "Illustrazione editoriale IA di Kevin Durant e Cooper Flagg alla Venetian Arena di Macao; scena non documentaria.",
        "image_prompt": "Kevin Durant in divisa Houston e Cooper Flagg in divisa Dallas nella Venetian Arena di Macao, fotografia editoriale ultrarealistica, loghi sportivi coerenti.",
    },
    {
        "slug": "lindsey-vonn-squadra-usa-sci-alpino-2026-27-recupero",
        "titolo": "Lindsey Vonn nella squadra USA 2026-27 mentre prosegue il recupero",
        "sommario": "U.S. Ski & Snowboard inserisce Vonn nel gruppo di 49 atleti per la nuova stagione. La Coppa del Mondo parte il 24 ottobre a Sölden.",
        "categoria": "Sport", "luogo": "Stati Uniti", "formato": "flash",
        "parole_chiave_titolo": ["Lindsey Vonn", "49 atleti"],
        "dati_chiave": [
            {"valore": "49", "etichetta": "atleti nella squadra alpina USA"},
            {"valore": "24-25 ott", "etichetta": "apertura a Sölden"},
            {"valore": "1-14 feb", "etichetta": "Mondiali 2027 a Crans-Montana"},
        ],
        "paragrafi": [
            "Lindsey Vonn compare nell'elenco di 49 atleti della squadra statunitense di sci alpino per la stagione 2026-2027. U.S. Ski & Snowboard ha annunciato il gruppo il 7 ottobre, precisando che la campionessa sta proseguendo il recupero dagli infortuni riportati durante Milano Cortina.",
            "L'inserimento nella squadra indica che Vonn resta nel programma federale, ma non equivale alla conferma della partecipazione a una gara specifica. Tempi di rientro, convocazioni e carico agonistico dipenderanno dalle valutazioni mediche e tecniche comunicate più avanti dalla federazione e dall'atleta.",
            "Nel roster figurano anche Mikaela Shiffrin, Breezy Johnson, Paula Moltzan, River Radamus e Ryan Cochran-Siegle. La formazione riunisce specialisti delle prove veloci e tecniche in vista di un calendario che comprende Coppa del Mondo e campionati iridati.",
            "La stagione internazionale comincia a Sölden, in Austria, il 24 e 25 ottobre. Il programma femminile della Coppa del Mondo prevede quaranta gare in venti località; quello maschile quarantatré gare distribuite in ventuno sedi, secondo i numeri riepilogati dalla federazione statunitense.",
            "L'appuntamento centrale saranno i Mondiali di Crans-Montana, in Svizzera, dal 1° al 14 febbraio 2027. Per gli Stati Uniti la preparazione unirà quindi risultati nel circuito, gestione fisica degli atleti e selezione della squadra per le singole discipline mondiali.",
            "Per Vonn ogni aggiornamento sul ritorno in pista richiede cautela: il comunicato ufficiale conferma la presenza nel team, non un calendario personale già fissato. Le indicazioni affidabili restano quelle diffuse da U.S. Ski & Snowboard e dai canali verificati dell'atleta.",
        ],
        "fonti": [{"url": "https://www.usskiandsnowboard.org/news/2026-27-stifel-us-alpine-ski-team-announced", "nome": "U.S. Ski & Snowboard — annuncio ufficiale della squadra alpina 2026-2027."}],
        "image_source": "vonn", "public_figure": True, "sensitive_context": True,
        "image_alt": "Ritratto editoriale neutrale isolato di Lindsey Vonn in abbigliamento della squadra statunitense; somiglianza sintetica IA non documentaria.",
        "image_prompt": "Neutral editorial portrait of Lindsey Vonn, isolated on a plain studio background, composed expression and U.S. ski team clothing.",
    },
    {
        "slug": "hurkacz-19-ace-shanghai-2026-djokovic-tsitsipas",
        "titolo": "Shanghai, Hurkacz serve 19 ace: ora sfida Djokovic; avanti Tsitsipas",
        "sommario": "Il polacco supera James Duckworth 6-3 7-6(4) e trova Novak Djokovic. Stefanos Tsitsipas batte Kimmer Coppejans in due set.",
        "categoria": "Sport", "luogo": "Shanghai, Cina", "formato": "flash",
        "parole_chiave_titolo": ["19 ace", "sfida Djokovic"],
        "dati_chiave": [
            {"valore": "19 ace", "etichetta": "per Hubert Hurkacz"},
            {"valore": "6-3 7-6", "etichetta": "il risultato su Duckworth"},
            {"valore": "2 set", "etichetta": "per la vittoria di Tsitsipas"},
        ],
        "paragrafi": [
            "Hubert Hurkacz ha superato James Duckworth 6-3 7-6(4) al Masters 1000 di Shanghai, costruendo la vittoria su diciannove ace. Il polacco avanza così al turno successivo, dove lo aspetta Novak Djokovic in uno degli incroci più attesi del tabellone.",
            "Il servizio ha permesso a Hurkacz di controllare molti scambi brevi e di difendere i propri turni di battuta. Dopo il primo set chiuso con un break, la seconda partita è arrivata al tie-break, deciso dal polacco senza concedere a Duckworth la possibilità di allungare al terzo.",
            "L'abbinamento con Djokovic alza subito il livello del torneo per Hurkacz. Contro il serbo, la percentuale di prime e la qualità della risposta sulle seconde palle saranno decisive: gli ace raccontano la potenza, ma non esauriscono il lavoro necessario per gestire gli scambi più lunghi.",
            "Nella stessa giornata Stefanos Tsitsipas ha battuto il belga Kimmer Coppejans 6-3 7-5. Il greco ha evitato un terzo set e ha consolidato il proprio percorso a Shanghai, in una fase della stagione in cui ogni vittoria può pesare anche sulle posizioni finali dell'anno.",
            "Il Masters cinese si gioca sul cemento e distribuisce gli incontri su più campi. Orari e ordine di gioco vengono aggiornati quotidianamente dall'ATP: per sapere quando si disputa Hurkacz-Djokovic è necessario consultare il programma ufficiale della giornata interessata.",
            "I risultati qui riportati fotografano il turno completato l'8 ottobre. Ritiri, variazioni del programma o nuovi esiti successivi non sono inclusi automaticamente: il livescore ATP resta il riferimento per il punteggio in tempo reale e per il tabellone aggiornato.",
        ],
        "fonti": [{"url": "https://www.atptour.com/en/news/hurkacz-duckworth-shanghai-2026-thursday", "nome": "ATP Tour — risultati e cronaca ufficiale di Hurkacz e Tsitsipas a Shanghai."}],
        "image_source": "hurkacz", "public_figure": True,
        "image_alt": "Illustrazione editoriale IA di Hubert Hurkacz al servizio sul campo centrale di Shanghai; scena non documentaria.",
        "image_prompt": "Hubert Hurkacz al servizio su un campo da tennis di Shanghai, fotografia editoriale ultrarealistica, arena riconoscibile e loghi coerenti.",
    },
    {
        "slug": "dustfall-apple-tv-serie-crime-anna-torv-2027",
        "titolo": "Dustfall, Apple TV ordina la serie crime con Anna Torv",
        "sommario": "Il thriller australiano avrà sei episodi ed è tratto da The Unbelieved di Vikki Petraitis. Il debutto globale è previsto nel 2027.",
        "categoria": "Film e serie TV", "luogo": "Australia", "formato": "flash",
        "parole_chiave_titolo": ["Dustfall", "Anna Torv"],
        "dati_chiave": [
            {"valore": "6 episodi", "etichetta": "per il crime drama"},
            {"valore": "2027", "etichetta": "anno del debutto globale"},
            {"valore": "1 romanzo", "etichetta": "The Unbelieved all'origine"},
        ],
        "paragrafi": [
            "Apple TV ha ordinato Dustfall, una serie crime australiana in sei episodi con Anna Torv come protagonista e produttrice esecutiva. Il progetto è tratto dal romanzo The Unbelieved di Vikki Petraitis e sarà distribuito nel mondo nel 2027, con l'eccezione dell'Australia per accordi territoriali già esistenti.",
            "Torv interpreta una detective che arriva in una comunità rurale dopo una segnalazione e si trova davanti a un caso che mette in discussione equilibri e silenzi locali. La piattaforma presenta la storia come un thriller investigativo concentrato anche sulle conseguenze umane del mancato ascolto delle vittime.",
            "La sceneggiatura è affidata a Dianne Taylor, che figura anche tra i produttori esecutivi. Emma Freeman dirige la serie. Il formato limitato a sei puntate suggerisce un racconto compatto, ma Apple non ha ancora comunicato durata degli episodi o data precisa di uscita.",
            "The Unbelieved è un'opera narrativa ispirata al lavoro della giornalista e autrice di true crime Vikki Petraitis. L'adattamento televisivo non viene presentato come documentario: personaggi e struttura seguono il linguaggio della fiction, anche quando affrontano temi legati alla giustizia e alla credibilità delle denunce.",
            "Per Anna Torv il ruolo segna un nuovo progetto seriale australiano dopo esperienze internazionali tra thriller, fantascienza e drama. L'annuncio ufficiale non rivela ancora il resto del cast, né mostra immagini di scena o un trailer.",
            "La disponibilità australiana sarà gestita separatamente, perché BBC e ZDF Studios detengono diritti nel Paese. Per il pubblico italiano, invece, Apple indica l'arrivo su Apple TV nel 2027; il calendario definitivo verrà comunicato più vicino alla première.",
        ],
        "fonti": [{"url": "https://www.apple.com/tv-pr/news/2026/10/apple-tv-lands-gripping-crime-drama-dustfall-starring-emmy-award-nominee-anna-torv/", "nome": "Apple TV Press — annuncio ufficiale, cast creativo e distribuzione di Dustfall."}],
        "image_source": "dustfall", "public_figure": True,
        "image_alt": "Illustrazione editoriale IA di Anna Torv su un set crime tropicale australiano; scena non documentaria.",
        "image_prompt": "Anna Torv su un set televisivo crime australiano umido e tropicale, fotografia editoriale ultrarealistica, cinepresa visibile, nessuna scena di violenza.",
    },
    {
        "slug": "stick-2-trailer-apple-tv-owen-wilson-rhea-seehorn-4-novembre-2026",
        "titolo": "Stick 2, il trailer riporta Owen Wilson sul green con Rhea Seehorn",
        "sommario": "La seconda stagione della comedy Apple TV debutta il 4 novembre con due episodi. Le restanti puntate usciranno ogni mercoledì fino al 30 dicembre.",
        "categoria": "Film e serie TV", "luogo": "Stati Uniti", "formato": "flash",
        "parole_chiave_titolo": ["Stick 2", "Rhea Seehorn"],
        "dati_chiave": [
            {"valore": "10 episodi", "etichetta": "nella seconda stagione"},
            {"valore": "4 novembre", "etichetta": "debutto con due puntate"},
            {"valore": "30 dicembre", "etichetta": "finale della stagione"},
        ],
        "paragrafi": [
            "Apple TV ha pubblicato il trailer della seconda stagione di Stick, la comedy sportiva con Owen Wilson. I nuovi episodi debuttano mercoledì 4 novembre 2026: le prime due puntate saranno disponibili insieme, poi l'uscita proseguirà ogni settimana fino al finale del 30 dicembre.",
            "La stagione è composta da dieci episodi. Wilson torna nei panni di Pryce Cahill, ex golfista professionista diventato mentore, mentre Rhea Seehorn entra nel cast con un ruolo centrale. Il trailer punta sul rapporto fra competizione, seconde occasioni e legami costruiti lontano dai riflettori del tour.",
            "Jason Keller resta creatore e produttore esecutivo della serie. Il golf continua a essere il motore della storia, ma la commedia usa il campo soprattutto per raccontare persone che cercano un nuovo equilibrio tra ambizione personale, famiglia e responsabilità verso il gruppo.",
            "La distribuzione settimanale evita il rilascio completo in un solo giorno. Dopo i due episodi iniziali, gli altri otto arriveranno uno alla volta il mercoledì: il calendario porta quindi la stagione attraverso novembre e dicembre, fino alla settimana di fine anno.",
            "Apple non ha indicato nel comunicato una durata uniforme per le puntate. Anche la disponibilità di doppiaggio e sottotitoli può essere verificata nella scheda italiana della serie al momento dell'uscita, perché le opzioni linguistiche dipendono dal mercato.",
            "Stick è disponibile con un abbonamento Apple TV. Il trailer anticipa la nuova stagione, ma non sostituisce la visione degli episodi precedenti: chi non ricorda i rapporti tra i personaggi può recuperare la prima stagione prima del 4 novembre.",
        ],
        "fonti": [{"url": "https://www.apple.com/tv-pr/news/2026/10/apple-tv-debuts-un-fore-gettable-trailer-for-the-second-season-of-the-beloved-sports-comedy-stick-starring-and-executive-produced-by-owen-wilson/", "nome": "Apple TV Press — trailer, cast e calendario ufficiale della seconda stagione di Stick."}],
        "image_source": "stick", "public_figure": True,
        "image_alt": "Illustrazione editoriale IA di Owen Wilson e Rhea Seehorn su un set da golf; scena non documentaria.",
        "image_prompt": "Owen Wilson e Rhea Seehorn su un set televisivo ambientato in un campo da golf, fotografia editoriale ultrarealistica, cinepresa e troupe discrete.",
    },
    {
        "slug": "it-gets-worse-paramount-plus-leo-reich-6-novembre-2026",
        "titolo": "It Gets Worse su Paramount+ dal 6 novembre: Leo Reich crea e interpreta la serie",
        "sommario": "La nuova comedy A24 avrà sei episodi. Il comico britannico firma il progetto ed è anche protagonista e produttore esecutivo.",
        "categoria": "Film e serie TV", "luogo": "Stati Uniti", "formato": "flash",
        "parole_chiave_titolo": ["It Gets Worse", "6 novembre"],
        "dati_chiave": [
            {"valore": "6 episodi", "etichetta": "per la nuova comedy"},
            {"valore": "6 novembre", "etichetta": "première su Paramount+"},
            {"valore": "A24", "etichetta": "studio della serie"},
        ],
        "paragrafi": [
            "Paramount+ ha fissato al 6 novembre 2026 la première di It Gets Worse, nuova serie comedy creata e interpretata da Leo Reich. La prima stagione è composta da sei episodi ed è prodotta da A24, con Reich coinvolto anche come produttore esecutivo.",
            "La serie segue un giovane britannico alle prese con la vita universitaria negli Stati Uniti e con l'immagine di sé che prova a costruire davanti agli altri. Il titolo suggerisce un percorso tutt'altro che lineare, affidato all'umorismo osservativo e autobiografico che ha reso noto Reich negli spettacoli dal vivo.",
            "L'annuncio ufficiale concentra l'attenzione sul punto di vista del protagonista e sul contrasto culturale tra Regno Unito e campus americano. Paramount non presenta il progetto come un documentario sulla vita del comico: si tratta di una fiction con personaggi e situazioni costruiti per la serie.",
            "A24 entra nel progetto come studio, mentre Paramount+ cura la distribuzione annunciata. Il comunicato non specifica se tutti e sei gli episodi saranno pubblicati insieme o con cadenza settimanale, dettaglio che dovrà essere verificato sulla scheda del titolo vicino al debutto.",
            "Anche la disponibilità territoriale può variare tra i mercati serviti dalla piattaforma. La data del 6 novembre è quella indicata nell'annuncio Paramount+; catalogo italiano, doppiaggio e sottotitoli saranno confermati nell'app quando la pagina locale della serie sarà attiva.",
            "Per Leo Reich è il passaggio a una narrazione seriale dopo il lavoro nella stand-up e in televisione. Sei episodi consentono alla comedy di sviluppare una storia continua senza rinunciare a situazioni brevi, imbarazzanti e concentrate sul modo in cui il protagonista legge se stesso.",
        ],
        "fonti": [{"url": "https://www.paramountpressexpress.com/paramount-plus/shows/it-gets-worse/releases/?view=113380-paramount-sets-november-6-premiere-for-it-gets-worse-the-new-comedy-series-created-by-and-starring-leo-reich", "nome": "Paramount Press Express — data, formato e crediti ufficiali di It Gets Worse."}],
        "image_source": "reich", "public_figure": True,
        "image_alt": "Illustrazione editoriale IA di Leo Reich su un set comedy in un campus statunitense; scena non documentaria.",
        "image_prompt": "Leo Reich su un set televisivo comedy in un campus americano, fotografia editoriale ultrarealistica, troupe e cinepresa visibili.",
    },
    {
        "slug": "apocalypse-z-nuovo-mondo-trailer-prime-video-30-ottobre-2026",
        "titolo": "Apocalypse Z: Nuovo Mondo, il trailer porta i sopravvissuti alle Canarie",
        "sommario": "Il sequel debutta su Prime Video il 30 ottobre e passa prima dal Festival di Sitges. Le isole sembrano un rifugio, ma nascondono nuovi pericoli.",
        "categoria": "Film e serie TV", "luogo": "Isole Canarie, Spagna", "formato": "flash",
        "parole_chiave_titolo": ["Apocalypse Z", "Canarie"],
        "dati_chiave": [
            {"valore": "30 ottobre", "etichetta": "uscita globale su Prime Video"},
            {"valore": "10 ottobre", "etichetta": "presentazione a Sitges"},
            {"valore": "1 sequel", "etichetta": "diretto da Carles Torrens"},
        ],
        "paragrafi": [
            "Prime Video ha diffuso il trailer di Apocalypse Z: Nuovo Mondo, seguito del film spagnolo tratto dall'universo narrativo di Manel Loureiro. Il debutto globale in streaming è fissato al 30 ottobre 2026, dopo una presentazione al Festival di Sitges prevista per il 10 ottobre.",
            "La storia riprende il viaggio di Manel e dei sopravvissuti in un mondo travolto dall'epidemia. Le Isole Canarie vengono indicate come possibile ultimo rifugio, ma il trailer mostra che l'arrivo nell'arcipelago non coincide con la sicurezza e introduce minacce diverse dagli infetti.",
            "Carles Torrens dirige il sequel. Il cast comprende Francisco Ortiz, Berta Vázquez, José María Yazpik, Marta Poveda e Iria del Río, insieme ad altri interpreti annunciati da Prime Video. La produzione amplia quindi luoghi e personaggi rispetto al primo capitolo.",
            "Le ambientazioni vulcaniche e costiere delle Canarie diventano parte visibile dell'identità del film. Il contrasto tra paesaggi aperti e isolamento rafforza l'idea di un rifugio difficile da raggiungere e ancora più difficile da difendere.",
            "La presentazione a Sitges anticipa l'uscita in piattaforma di venti giorni, ma non cambia la data globale del 30 ottobre. Il film sarà incluso nel catalogo Prime Video nei territori indicati dal servizio; audio e sottotitoli disponibili vanno controllati nella scheda locale.",
            "Nuovo Mondo è un sequel diretto, quindi la visione del primo Apocalypse Z aiuta a comprendere rapporti, perdite e motivazioni del protagonista. Il trailer rivela il punto di partenza alle Canarie, ma non chiarisce l'esito della nuova traversata né la natura completa del pericolo umano.",
        ],
        "fonti": [{"url": "https://www.aboutamazon.com/news/entertainment/apocalypse-z-2-new-world-sequel-prime-video", "nome": "Amazon — trailer, cast, festival e data di uscita ufficiale di Apocalypse Z: Nuovo Mondo."}],
        "image_source": "apocalypse",
        "image_alt": "Illustrazione editoriale IA dei sopravvissuti di Apocalypse Z su una costa vulcanica delle Canarie; scena non documentaria e senza violenza grafica.",
        "image_prompt": "Set cinematografico di Apocalypse Z su una costa vulcanica delle Canarie, sopravvissuti e infetti lontani, fotografia ultrarealistica senza gore, cinepresa visibile.",
    },
    {
        "slug": "maltempo-fiumicino-alberi-caduti-viabilita-8-ottobre-2026",
        "titolo": "Maltempo a Fiumicino, alberi caduti bloccano la strada: viabilità ripristinata",
        "sommario": "Due alberi hanno ostruito via della Torre di Pagliaccetto. Il Comune segnala interventi anche in via Casale di Sant'Angelo e via Tragliata.",
        "categoria": "Cronaca", "luogo": "Fiumicino, Roma", "formato": "flash",
        "parole_chiave_titolo": ["Fiumicino", "alberi caduti"],
        "dati_chiave": [
            {"valore": "2 alberi", "etichetta": "caduti sulla carreggiata"},
            {"valore": "3 strade", "etichetta": "interessate dagli interventi"},
            {"valore": "8 ottobre", "etichetta": "giorno delle operazioni"},
        ],
        "paragrafi": [
            "Il maltempo ha causato la caduta di due alberi su via della Torre di Pagliaccetto, nel territorio di Fiumicino, bloccando la carreggiata. Il Comune ha comunicato l'intervento delle squadre incaricate, che hanno rimosso gli ostacoli e lavorato per rimettere in sicurezza la viabilità.",
            "Problemi sono stati segnalati anche in via Casale di Sant'Angelo e in via Tragliata. In queste zone le verifiche hanno riguardato rami, vegetazione e condizioni del passaggio stradale dopo pioggia e vento, con operatori e mezzi impegnati nei punti indicati.",
            "La Polizia locale ha supportato le attività sul traffico e la protezione delle aree interessate. Durante la rimozione degli alberi, la priorità è impedire l'accesso al tratto di carreggiata non sicuro e consentire agli addetti di utilizzare i mezzi senza esporre automobilisti e residenti.",
            "Il Comune ha riferito che la viabilità è stata ripristinata dopo gli interventi. Il ritorno alla circolazione non esclude controlli successivi sugli alberi vicini o nuove limitazioni temporanee, soprattutto se le condizioni meteorologiche restano instabili.",
            "Chi percorre strade alberate dopo un temporale dovrebbe ridurre la velocità e mantenere distanza da rami pendenti, recinzioni mobili e mezzi di soccorso. Una segnalazione precisa, con nome della via e punto riconoscibile, aiuta la centrale operativa a valutare la priorità.",
            "L'aggiornamento ufficiale è stato pubblicato dal Comune di Fiumicino l'8 ottobre alle 19:51. Per chiusure ancora attive o deviazioni dell'ultimo minuto, i riferimenti più affidabili restano i canali istituzionali locali e le indicazioni presenti sul posto.",
        ],
        "fonti": [{"url": "https://www.comune.fiumicino.rm.it/it/news/maltempo-interventi-per-la-messa-in-sicurezza-della-viabilita", "nome": "Comune di Fiumicino — interventi e ripristino della viabilità dopo il maltempo."}],
        "image_source": "fiumicino",
        "image_alt": "Illustrazione editoriale IA di due pini caduti su una strada bagnata nel territorio di Fiumicino; scena non documentaria.",
        "image_prompt": "Due grandi pini caduti su una strada bagnata di Fiumicino, luci dei mezzi d'emergenza, fotografia editoriale ultrarealistica senza persone ferite.",
    },
    {
        "slug": "frattamaggiore-via-don-minzoni-sprofondamento-deviazione-bus-928",
        "titolo": "Frattamaggiore, sprofonda via Don Minzoni: deviata la linea bus 928",
        "sommario": "EAV modifica temporaneamente il percorso tra Orta di Atella e Napoli. La deviazione resta attiva fino al ripristino della strada.",
        "categoria": "Cronaca", "luogo": "Frattamaggiore, Napoli", "formato": "flash",
        "parole_chiave_titolo": ["via Don Minzoni", "linea 928"],
        "dati_chiave": [
            {"valore": "Linea 928", "etichetta": "il collegamento deviato"},
            {"valore": "8 ottobre", "etichetta": "inizio della modifica"},
            {"valore": "2 direzioni", "etichetta": "percorsi alternativi indicati"},
        ],
        "paragrafi": [
            "Uno sprofondamento improvviso della sede stradale in via Don Minzoni, a Frattamaggiore, ha reso necessaria la deviazione temporanea della linea EAV 928 tra Orta di Atella e Napoli. La modifica è in vigore dall'8 ottobre 2026 e resterà valida fino al ripristino delle condizioni di sicurezza.",
            "Per i bus provenienti da Napoli, dopo il Ponte di Fratta il percorso alternativo passa per via Roma, via Vittorio Veneto, via C. Pezzullo, via Niglio e via Vittorio Emanuele III, quindi svolta in via Pirozzi per raggiungere l'ospedale.",
            "Nella direzione opposta, dopo l'ospedale i mezzi percorrono via Pirozzi, via Vittorio Emanuele III, via Capasso, Corso Durante, via Pezzullo e via Vittorio Veneto, per poi rientrare verso via Roma e il Ponte di Fratta.",
            "La deviazione comporta la sospensione pratica delle fermate presenti nel tratto non percorso e può allungare i tempi di viaggio, soprattutto nelle ore di traffico. EAV non indica nel comunicato una data certa per il ritorno all'itinerario ordinario.",
            "I passeggeri diretti alle fermate vicine a via Don Minzoni dovrebbero verificare quale punto del percorso alternativo sia più accessibile e considerare un margine aggiuntivo. Per coincidenze importanti è utile consultare gli avvisi EAV prima della partenza.",
            "Lo sprofondamento resta un evento di viabilità locale e non autorizza ad avvicinarsi alla zona transennata. Segnaletica, recinzioni e indicazioni degli operatori vanno rispettate anche quando il cedimento sembra limitato, perché la stabilità del terreno deve essere verificata dai tecnici.",
        ],
        "fonti": [{"url": "https://www.eavsrl.it/linea-928-deviazione-temporanea-di-percorso-in-frattamaggiore-via-don-minzoni-dal-8-ottobre-2026/", "nome": "EAV — percorso alternativo ufficiale della linea 928 a Frattamaggiore."}],
        "image_source": "frattamaggiore",
        "image_alt": "Illustrazione editoriale IA di un cedimento transennato in via Don Minzoni con un autobus EAV deviato; scena non documentaria.",
        "image_prompt": "Piccolo cedimento stradale transennato in via Don Minzoni a Frattamaggiore, autobus EAV sul percorso deviato, fotografia ultrarealistica senza persone in pericolo.",
    },
]


def main() -> None:
    base = datetime.now(ROME).replace(microsecond=0)
    images = []
    written = []
    for index, article in enumerate(ARTICLES):
        image = make_image(article)
        slug = site.write_article(article, image, VERSION)
        set_published(slug, base - timedelta(seconds=index))
        image["article"] = f"/notizie/{slug}.html"
        images.append(image)
        written.append(article)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    new_urls = {row["article"] for row in images}
    registry["items"] = images + [row for row in registry.get("items", []) if row.get("article") not in new_urls]
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces(
        written,
        f"/notizie/{written[0]['slug']}.html",
        VERSION,
        update_manifest=False,
    )

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION,
        "currentVersion": VERSION,
        "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": f"notizie-multicategoria-v{VERSION}",
        "date": base.date().isoformat(),
        "release_date": base.date().isoformat(),
        "updated_at": base.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
