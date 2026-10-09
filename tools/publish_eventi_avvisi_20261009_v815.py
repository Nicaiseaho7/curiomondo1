#!/usr/bin/env python3
"""Release v815: partite, concerti, biglietti e avvisi di servizio."""
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

VERSION = 815
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"

IMAGE_SOURCES = {
    "greta": GENERATED / "exec-badb81b5-fec0-4a9a-b69d-634e75fde607.png",
    "raf": GENERATED / "exec-7e031a23-b4d9-46e0-a9e6-61d36ed91b65.png",
    "pooh": GENERATED / "exec-3c000eef-dd77-45c0-89ad-6fbb58b9472b.png",
    "mengoni": GENERATED / "exec-c67b446c-9339-401f-91c2-f2e0216c7476.png",
    "inter": GENERATED / "exec-878c4053-da32-4d97-bd42-26f8a7a97201.png",
    "derby": GENERATED / "exec-17ef6602-9a46-43db-9723-7b11efab347c.png",
    "olimpia": GENERATED / "exec-2cb0df58-505c-4f40-8e9e-a3ac7a547079.png",
    "atm": GENERATED / "exec-a2902c6c-df6b-461a-9539-147f3008fef3.png",
    "start": GENERATED / "exec-c576f983-54a3-41c5-a82e-d3f189900144.png",
    "rfi": GENERATED / "exec-93d71f65-c0e1-423f-afba-2d55bd963167.png",
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
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )


ARTICLES = [
    {
        "slug": "greta-van-fleet-milano-16-maggio-2027-biglietti",
        "titolo": "Greta Van Fleet a Milano nel 2027: biglietti in vendita oggi",
        "sommario": "L'unica data italiana del tour è il 16 maggio all'Unipol Forum. La vendita generale parte il 9 ottobre alle 10 con prezzi nominali fissi.",
        "categoria": "Cultura", "luogo": "Milano", "formato": "flash",
        "parole_chiave_titolo": ["Greta Van Fleet", "biglietti"],
        "dati_chiave": [
            {"valore": "16 maggio", "etichetta": "concerto all'Unipol Forum"},
            {"valore": "ore 10", "etichetta": "apertura vendita generale"},
            {"valore": "1 data", "etichetta": "unico appuntamento italiano"},
        ],
        "paragrafi": [
            "I Greta Van Fleet tornano in Italia domenica 16 maggio 2027 con un'unica data all'Unipol Forum di Milano. La vendita generale dei biglietti parte oggi, venerdì 9 ottobre 2026, alle 10 sui circuiti indicati dalla pagina ufficiale Live Nation.",
            "Il concerto fa parte di un tour di 59 date. Le prevendite dedicate all'artista e agli iscritti My Live Nation si sono svolte il 7 e l'8 ottobre; dalla mattina del 9 ottobre l'acquisto è aperto al pubblico, fino a disponibilità dei posti.",
            "Live Nation precisa che per questo tour viene adottato un sistema di prezzi nominali fissi, ai quali si aggiungono le commissioni applicabili, e che non è previsto il programma Platinum. La disponibilità può cambiare rapidamente mentre gli utenti completano gli ordini.",
            "Per ridurre il rischio di annunci falsi o biglietti non validi conviene partire dai collegamenti presenti sulla pagina dell'organizzatore. Prima del pagamento vanno controllati settore, quantità, prezzo complessivo e condizioni del circuito scelto.",
            "L'Unipol Forum si trova ad Assago, nell'area metropolitana di Milano. Indicazioni su apertura porte, trasporti, eventuali limiti agli oggetti ammessi e orario di inizio saranno aggiornate dai canali ufficiali più vicino alla data.",
        ],
        "fonti": [{"url": "https://www.livenation.it/greta-van-fleet-milano", "nome": "Live Nation Italia — data, luogo e modalità ufficiali di vendita."}],
        "image_source": "greta", "public_figure": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica dei Greta Van Fleet sul palco dell'Unipol Forum di Milano; scena non documentaria.",
        "image_prompt": "Greta Van Fleet performing at the recognizable Unipol Forum in Milan, ultra-realistic editorial concert illustration, accurate public figures, authentic stage branding, no text overlay.",
    },
    {
        "slug": "raf-napoli-rinviato-14-ottobre-2027-biglietti-rimborsi",
        "titolo": "Raf, Napoli rinviata al 14 ottobre 2027: biglietti validi",
        "sommario": "Il concerto previsto il 9 ottobre 2026 al Palapartenope cambia data. I titoli restano validi; richieste di rimborso entro il 30 ottobre.",
        "categoria": "Cultura", "luogo": "Napoli", "formato": "flash",
        "parole_chiave_titolo": ["Raf", "14 ottobre 2027"],
        "dati_chiave": [
            {"valore": "14 ottobre 2027", "etichetta": "nuova data a Napoli"},
            {"valore": "ore 21", "etichetta": "inizio al Palapartenope"},
            {"valore": "30 ottobre", "etichetta": "termine per i rimborsi"},
        ],
        "paragrafi": [
            "Il concerto di Raf previsto oggi, 9 ottobre 2026, al Palapartenope di Napoli è rinviato a giovedì 14 ottobre 2027 alle 21. L'organizzatore Friends & Partners conferma che i biglietti già acquistati restano validi per la nuova data.",
            "Cambiano anche gli altri appuntamenti del tour nei palasport: Milano passa dal 12 ottobre 2026 al 2 ottobre 2027, mentre Roma viene riprogrammata dal 17 ottobre 2026 al 9 ottobre 2027. I possessori dei titoli non devono effettuare una nuova prenotazione se intendono partecipare.",
            "Chi non può essere presente può richiedere il rimborso entro le 23:59 del 30 ottobre 2026. La procedura deve essere avviata attraverso il circuito usato per l'acquisto, seguendo le istruzioni pubblicate da TicketOne o Ticketmaster.",
            "Per i biglietti comprati in un punto vendita fisico possono essere previste modalità diverse rispetto agli ordini online. È utile conservare titolo di accesso, ricevuta e conferma dell'ordine fino alla conclusione della pratica.",
            "La scadenza del 30 ottobre è l'informazione più importante per chi sceglie il rimborso. Richieste inviate dopo il termine potrebbero non essere accettate; eventuali aggiornamenti devono essere controllati sulla pagina ufficiale del tour.",
        ],
        "fonti": [{"url": "https://www.friendsandpartners.it/in-tour/raf-infinito-palasport-2027", "nome": "Friends & Partners — nuovo calendario, validità dei biglietti e rimborsi."}],
        "image_source": "raf", "public_figure": True,
        "image_alt": "Ritratto editoriale neutrale di Raf su sfondo scuro; somiglianza sintetica IA non documentaria.",
        "image_prompt": "neutral editorial portrait of Raf, isolated on a plain dark studio background, composed expression, no event reenactment, ultra-realistic editorial illustration.",
    },
    {
        "slug": "pooh-60-tour-torino-10-11-ottobre-2026-biglietti",
        "titolo": "Pooh 60, il tour parte da Torino: due concerti il 10 e 11 ottobre",
        "sommario": "L'Inalpi Arena apre il calendario nei palasport. Seguono Roma, Milano, Eboli e Bari; i canali ufficiali indicano ancora l'accesso ai biglietti.",
        "categoria": "Cultura", "luogo": "Torino", "formato": "flash",
        "parole_chiave_titolo": ["Pooh 60", "Torino"],
        "dati_chiave": [
            {"valore": "10-11 ottobre", "etichetta": "le due date di Torino"},
            {"valore": "ore 21", "etichetta": "inizio dei concerti"},
            {"valore": "5 città", "etichetta": "nel calendario dei palasport"},
        ],
        "paragrafi": [
            "Il tour Pooh 60 - La nostra storia parte dall'Inalpi Arena di Torino con due concerti sabato 10 e domenica 11 ottobre 2026, entrambi alle 21. La pagina ufficiale di Friends & Partners collega ai circuiti autorizzati per verificare i posti ancora disponibili.",
            "Dopo Torino il calendario prosegue a Roma il 15 e 16 ottobre e a Milano il 18 e 19 ottobre. Sono poi previste due serate a Eboli, il 27 e 28 ottobre, e due a Bari, il 30 e 31 ottobre.",
            "La doppia data torinese apre quindi una sequenza concentrata di appuntamenti nei palasport. Chi ha già acquistato deve controllare che sul titolo siano corretti giorno, città e settore, soprattutto dove sono previste due serate consecutive nello stesso impianto.",
            "Per gli acquisti dell'ultimo momento è prudente usare esclusivamente i collegamenti pubblicati dall'organizzatore. Prezzi, settori e disponibilità vengono mostrati dal circuito di biglietteria al momento dell'ordine e possono cambiare con l'esaurimento dei posti.",
            "Orari di apertura porte, accessi e regole sugli oggetti ammessi dipendono dall'arena. Prima di partire conviene consultare anche le comunicazioni dell'Inalpi Arena e predisporre sul telefono o su carta il titolo richiesto all'ingresso.",
        ],
        "fonti": [{"url": "https://www.friendsandpartners.it/in-tour/pooh60-la-nostra-storia-palasport", "nome": "Friends & Partners — calendario ufficiale e collegamenti alla biglietteria."}],
        "image_source": "pooh", "public_figure": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica dei Pooh sul palco dell'Inalpi Arena di Torino; scena non documentaria.",
        "image_prompt": "The real members of Pooh performing at Turin Inalpi Arena, ultra-realistic editorial concert illustration, recognizable venue, authentic band branding, no text overlay.",
    },
    {
        "slug": "marco-mengoni-allo-sbagliato-milano-biglietti-regole-2026",
        "titolo": "Mengoni, Allo Sbagliato a Milano: biglietti nominali e telefoni vietati",
        "sommario": "Il nuovo club al Teatro Principe ospita 26 serate dal 5 novembre al 19 dicembre. Massimo due titoli per account e ritiro con documento.",
        "categoria": "Cultura", "luogo": "Milano", "formato": "flash",
        "parole_chiave_titolo": ["Allo Sbagliato", "telefoni vietati"],
        "dati_chiave": [
            {"valore": "26 serate", "etichetta": "dal 5 novembre al 19 dicembre"},
            {"valore": "500 posti", "etichetta": "capienza indicata"},
            {"valore": "2 biglietti", "etichetta": "massimo per account"},
        ],
        "paragrafi": [
            "Marco Mengoni apre Allo Sbagliato, un club temporaneo al Teatro Principe di Milano, in viale Bligny 52. Il programma comprende 26 serate dal 5 novembre al 19 dicembre 2026, con concerti dell'artista e appuntamenti affidati a ospiti e comici.",
            "Lo spazio ha una capienza indicata di 500 persone. Per le date di Mengoni ogni account può acquistare al massimo due biglietti e soltanto per una delle 26 serate; uno dei titoli è destinato all'intestatario dell'account e l'altro all'eventuale accompagnatore.",
            "I biglietti vanno ritirati il giorno dello spettacolo a partire dalle 18:30 mostrando un documento originale valido. L'organizzatore presenta l'esperienza come phone-free: i telefoni non potranno essere usati durante l'evento secondo le modalità comunicate all'ingresso.",
            "La vendita passa dai circuiti Ticketmaster e TicketOne collegati dalla pagina ufficiale. È importante leggere le condizioni prima di pagare, perché limiti per account, identificazione e ritiro rendono rischioso acquistare da inserzioni non autorizzate.",
            "Il calendario completo distingue le serate di Mengoni da quelle con altri protagonisti. Prima dell'acquisto bisogna quindi controllare data, nome dell'evento e quantità, senza dare per scontato che ogni appuntamento preveda lo stesso spettacolo.",
        ],
        "fonti": [{"url": "https://www.livenation.it/allosbagliato", "nome": "Live Nation Italia — calendario, capienza e condizioni ufficiali di accesso."}],
        "image_source": "mengoni", "public_figure": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di Marco Mengoni sul palco del Teatro Principe di Milano; scena non documentaria.",
        "image_prompt": "Marco Mengoni performing inside the recognizable Teatro Principe in Milan, ultra-realistic editorial concert illustration, accurate public figure, authentic venue details, no text overlay.",
    },
    {
        "slug": "inter-parma-10-ottobre-2026-biglietti-san-siro-accessi",
        "titolo": "Inter-Parma sabato a San Siro: biglietti, orario e cambio nome",
        "sommario": "La partita si gioca il 10 ottobre alle 16. Disponibili titoli BASE, PLUS e Hospitality; per il BASE il cambio utilizzatore è a pagamento.",
        "categoria": "Sport", "luogo": "Milano", "formato": "flash",
        "parole_chiave_titolo": ["Inter-Parma", "cambio nome"],
        "dati_chiave": [
            {"valore": "10 ottobre", "etichetta": "partita al Meazza"},
            {"valore": "ore 16", "etichetta": "calcio d'inizio"},
            {"valore": "3 formule", "etichetta": "BASE, PLUS e Hospitality"},
        ],
        "paragrafi": [
            "Inter-Parma si gioca sabato 10 ottobre 2026 alle 16 allo stadio Giuseppe Meazza di Milano. La pagina ufficiale dell'Inter mostra l'accesso all'acquisto e distingue tre formule: BASE, PLUS e Hospitality.",
            "Il biglietto BASE consente un solo cambio utilizzatore a pagamento: 20 euro per il primo anello, 15 per il secondo e 10 per il terzo. La formula PLUS include invece un cambio; anche l'Hospitality comprende un cambio e aggiunge area dedicata, accoglienza e catering.",
            "Il club avverte che il cambio utilizzatore può comunque essere soggetto a limitazioni decise dalla società o dall'autorità di pubblica sicurezza. Chi compra per un'altra persona deve controllare le condizioni aggiornate prima di concludere l'ordine.",
            "Gli abbonati FULL e PLUS e i soci Inter Club PLUS possono acquistare fino a quattro biglietti aggiuntivi a prezzo riservato. Per i soci Inter Club devono risultare attivi nella stagione in corso sia l'acquirente sia l'intestatario.",
            "Sono cambiati alcuni ingressi e percorsi nell'area dello stadio. Prima della partenza è utile aprire l'avviso dedicato del club, verificare il varco sul biglietto e considerare tempo extra per i controlli e per l'afflusso del sabato pomeriggio.",
        ],
        "fonti": [{"url": "https://www.inter.it/it/biglietti", "nome": "FC Internazionale Milano — orario, formule di biglietto e condizioni di accesso."}],
        "image_source": "inter",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di Inter-Parma allo stadio Giuseppe Meazza; scena sportiva non documentaria.",
        "image_prompt": "Inter versus Parma at the recognizable San Siro stadium, ultra-realistic editorial sports illustration, authentic club kits and logos, no invented players, no text overlay.",
    },
    {
        "slug": "milan-inter-31-ottobre-2026-biglietti-derby-san-siro",
        "titolo": "Milan-Inter del 31 ottobre: derby alle 20:45, biglietti in vendita",
        "sommario": "La vendita libera è aperta fino a esaurimento. Il Milan avverte che non sarà consentito il cambio nominativo sui titoli acquistati.",
        "categoria": "Sport", "luogo": "Milano", "formato": "flash",
        "parole_chiave_titolo": ["Milan-Inter", "20:45"],
        "dati_chiave": [
            {"valore": "31 ottobre", "etichetta": "data del derby"},
            {"valore": "ore 20:45", "etichetta": "calcio d'inizio"},
            {"valore": "49 euro", "etichetta": "prezzo indicato per il settore ospiti"},
        ],
        "paragrafi": [
            "Milan-Inter è in programma sabato 31 ottobre 2026 alle 20:45 allo stadio Giuseppe Meazza. Il portale ufficiale del Milan indica che i biglietti sono in vendita e che la fase libera prosegue fino a esaurimento dei posti disponibili.",
            "La vendita generale è iniziata il 30 settembre alle 15. La pagina mostra prezzi diversi per settore e disponibilità; per il secondo anello verde, destinato agli ospiti, è indicato un prezzo di 49 euro, salvo variazioni e commissioni mostrate durante l'acquisto.",
            "Il club specifica che sui biglietti del derby non sarà consentito il cambio nominativo. Nome dell'intestatario, dati inseriti e documento da portare allo stadio devono quindi essere controllati con attenzione prima del pagamento.",
            "La disponibilità visualizzata può cambiare mentre altri utenti completano l'ordine. Per evitare truffe è consigliabile usare il portale di biglietteria collegato dal sito del Milan e non affidarsi a immagini del biglietto o annunci privi di verifica.",
            "Per una partita con grande affluenza conviene raggiungere lo stadio con anticipo e controllare settore e varco. Eventuali prescrizioni dell'autorità, modifiche agli accessi o informazioni per i tifosi ospiti saranno pubblicate dai club e dagli enti competenti.",
        ],
        "fonti": [{"url": "https://booking.acmilan.com/serie-a/milan-inter/", "nome": "AC Milan — vendita ufficiale, prezzi e condizioni nominali del derby."}],
        "image_source": "derby",
        "image_alt": "Illustrazione editoriale IA ultrarealistica del derby Milan-Inter allo stadio Giuseppe Meazza; scena non documentaria.",
        "image_prompt": "Milan versus Inter derby at the recognizable San Siro stadium, ultra-realistic editorial sports illustration, authentic club kits and logos, no invented players, no text overlay.",
    },
    {
        "slug": "olimpia-milano-treviso-11-ottobre-2026-biglietti-inclusione",
        "titolo": "Olimpia Milano-Treviso domenica: partita alle 16 e iniziativa inclusiva",
        "sommario": "Il Forum ospita la gara dell'11 ottobre. Dalle 14:30 attività gratuita aperta a tutti con una sfida di tiri liberi insieme a Special Olympics.",
        "categoria": "Sport", "luogo": "Assago, Milano", "formato": "flash",
        "parole_chiave_titolo": ["Olimpia Milano-Treviso", "iniziativa inclusiva"],
        "dati_chiave": [
            {"valore": "11 ottobre", "etichetta": "gara all'Unipol Forum"},
            {"valore": "ore 16", "etichetta": "inizio della partita"},
            {"valore": "14:30-15:30", "etichetta": "attività gratuita all'esterno"},
        ],
        "paragrafi": [
            "Olimpia Milano-Treviso si gioca domenica 11 ottobre 2026 alle 16 all'Unipol Forum di Assago. Il sito ufficiale dell'Olimpia collega alla biglietteria per verificare settori e disponibilità della gara.",
            "Prima della partita, dalle 14:30 alle 15:30, l'area esterna dell'impianto ospita un'attività gratuita e aperta a tutti insieme a Special Olympics. L'iniziativa propone una sfida di tiri liberi legata a un progetto di inclusione attraverso lo sport.",
            "Ogni tiro realizzato simboleggia un chilometro del percorso ideale verso i Giochi Mondiali Estivi Special Olympics di Santiago 2027. L'obiettivo complessivo comunicato dall'Olimpia è di 11.936 chilometri, la distanza indicativa tra Italia e Cile.",
            "L'attività esterna non sostituisce il biglietto necessario per assistere alla partita. Chi vuole partecipare a entrambe le iniziative deve calcolare il tempo richiesto per il successivo accesso, i controlli e il raggiungimento del proprio settore.",
            "Per l'acquisto è preferibile usare il collegamento ufficiale del club. Informazioni su parcheggi, trasporto pubblico, apertura dei cancelli ed eventuali variazioni vengono aggiornate dall'Olimpia e dall'Unipol Forum nei rispettivi canali.",
        ],
        "fonti": [{"url": "https://www.olimpiamilano.com/olimpia-club-parte-la-stagione-2026-27-copy-copy-copy-2/", "nome": "Pallacanestro Olimpia Milano — partita, biglietti e programma dell'iniziativa inclusiva."}],
        "image_source": "olimpia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di Olimpia Milano-Treviso all'Unipol Forum; scena sportiva non documentaria.",
        "image_prompt": "Olimpia Milano versus Treviso basketball at the recognizable Unipol Forum, ultra-realistic editorial sports illustration, authentic club uniforms and logos, inclusive fan activity outside, no text overlay.",
    },
    {
        "slug": "sciopero-atm-milano-9-ottobre-2026-fasce-orarie",
        "titolo": "Sciopero ATM oggi a Milano: le fasce in cui metro e bus non sono garantiti",
        "sommario": "Venerdì 9 ottobre il servizio può fermarsi dalle 8:45 alle 15 e dalle 18 a fine servizio. Orari diversi per la funicolare Como-Brunate.",
        "categoria": "Cronaca", "luogo": "Milano", "formato": "flash",
        "parole_chiave_titolo": ["Sciopero ATM", "fasce"],
        "dati_chiave": [
            {"valore": "8:45-15", "etichetta": "prima fascia non garantita"},
            {"valore": "dalle 18", "etichetta": "seconda fascia fino a fine servizio"},
            {"valore": "9 ottobre", "etichetta": "giornata dello sciopero"},
        ],
        "paragrafi": [
            "Lo sciopero proclamato da AL Cobas e Confial può modificare oggi, venerdì 9 ottobre 2026, il servizio ATM a Milano. Metropolitana, tram e autobus non sono garantiti dalle 8:45 alle 15 e dalle 18 fino al termine del servizio.",
            "Al di fuori di queste finestre ATM prevede le fasce garantite, ma affollamento e ripresa progressiva possono produrre attese o modifiche. Prima di partire è utile controllare lo stato delle linee nell'app e sui canali ufficiali dell'azienda.",
            "Per la funicolare Como-Brunate valgono orari diversi: il servizio non è garantito dalle 8:30 alle 16:30 e dalle 19:30 fino alla chiusura. Chi deve raggiungere una coincidenza dovrebbe prevedere un percorso alternativo.",
            "La durata effettiva delle interruzioni dipende dall'adesione del personale. Una linea può funzionare in parte o terminare le corse prima dell'inizio della fascia, per consentire ai mezzi e ai treni di rientrare secondo le procedure operative.",
            "Per appuntamenti non rinviabili conviene anticipare lo spostamento o valutare treni suburbani e servizi di altri operatori, verificandone però separatamente la regolarità. Le indicazioni in stazione e alle fermate prevalgono sulle pianificazioni fatte in precedenza.",
        ],
        "fonti": [{"url": "https://www.atm.it/it/ViaggiaConNoi/InfoTraffico/Pagine/Sciopero9ottobre.aspx", "nome": "ATM Milano — fasce ufficiali dello sciopero del 9 ottobre."}],
        "image_source": "atm",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una stazione della metropolitana di Milano durante lo sciopero; scena non documentaria.",
        "image_prompt": "Recognizable Milan metro station during a transport strike, stationary ATM train and calm passengers, ultra-realistic editorial illustration, authentic ATM branding, no text overlay.",
    },
    {
        "slug": "sciopero-start-romagna-9-ottobre-2026-fasce-garantite",
        "titolo": "Sciopero bus in Romagna oggi: fasce garantite diverse nelle tre province",
        "sommario": "Lo stop Start Romagna dura 24 ore e interessa Forlì-Cesena, Ravenna e Rimini. Restano protette due finestre di servizio per ciascun bacino.",
        "categoria": "Cronaca", "luogo": "Romagna", "formato": "flash",
        "parole_chiave_titolo": ["Sciopero bus", "fasce garantite"],
        "dati_chiave": [
            {"valore": "24 ore", "etichetta": "durata dello sciopero"},
            {"valore": "3 bacini", "etichetta": "Forlì-Cesena, Ravenna e Rimini"},
            {"valore": "2 fasce", "etichetta": "garantite in ogni territorio"},
        ],
        "paragrafi": [
            "Lo sciopero aziendale Start Romagna di oggi, venerdì 9 ottobre 2026, dura dalle 00:00 alle 24:00 e interessa il personale dei bacini di Forlì-Cesena, Ravenna e Rimini. Fuori dalle fasce protette le corse possono subire variazioni o sospensioni.",
            "A Forlì-Cesena il servizio è garantito dalle 5:30 alle 8:30 e dalle 13 alle 16. Nel bacino di Ravenna le finestre sono 5:30-8:30 e 12-15; comprendono anche il traghetto tra Porto Corsini e Marina di Ravenna.",
            "Nel territorio di Rimini le fasce garantite sono invece dalle 6 alle 9 e dalle 13 alle 16. Gli orari non coincidono quindi in tutte le province: il passeggero deve fare riferimento al bacino in cui si svolge la corsa.",
            "Lo sciopero è stato proclamato da FILT CGIL, FIT CISL, UILTRASPORTI, FAISA CISAL, USB Lavoro Privato e UGL Autoferro. Start Romagna collega la protesta ai temi della sicurezza del personale e degli utenti a bordo.",
            "L'adesione non è prevedibile con certezza per ogni linea. Prima di raggiungere la fermata è utile consultare gli aggiornamenti Start, il servizio clienti o i canali territoriali, soprattutto per coincidenze ferroviarie, visite e appuntamenti con orario fisso.",
        ],
        "fonti": [{"url": "https://www.startromagna.it/news/sciopero-9-ottobre-2026/", "nome": "Start Romagna — durata, territori e fasce di garanzia dello sciopero."}],
        "image_source": "start",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di autobus Start Romagna fermi in deposito durante lo sciopero; scena non documentaria.",
        "image_prompt": "Start Romagna buses stationary in a recognizable Romagna depot during a strike, ultra-realistic editorial illustration, authentic company branding, calm scene, no text overlay.",
    },
    {
        "slug": "lavori-ferrovia-ravenna-rimini-9-26-ottobre-2026-treni-bus",
        "titolo": "Lavori tra Ravenna e Rimini fino al 26 ottobre: treni cancellati e bus",
        "sommario": "RFI avvia la manutenzione programmata sulla linea. Coinvolti Frecciarossa, regionali e collegamenti sostitutivi in più fine settimana.",
        "categoria": "Cronaca", "luogo": "Emilia-Romagna", "formato": "flash",
        "parole_chiave_titolo": ["Ravenna e Rimini", "treni cancellati"],
        "dati_chiave": [
            {"valore": "9-26 ottobre", "etichetta": "periodo dei lavori"},
            {"valore": "2 Frecciarossa", "etichetta": "con tratte cancellate"},
            {"valore": "2 weekend", "etichetta": "con interruzioni notturne"},
        ],
        "paragrafi": [
            "I lavori di manutenzione programmata sulla linea Ravenna-Rimini modificano i treni dal 9 al 26 ottobre 2026. L'avviso RFI riguarda servizi ad alta velocità, regionali e autobus sostitutivi, con conseguenze anche per collegamenti provenienti da altre regioni.",
            "Il Frecciarossa 8852 Roma-Ravenna è cancellato tra Rimini e Ravenna il 9, 10, 11, 16, 17 e 18 ottobre. Il Frecciarossa 8851 Ravenna-Roma non circola tra Ravenna e Rimini il 10, 11, 12, 17, 18 e 19 ottobre.",
            "Tra le 23 di venerdì 9 e le 5:30 di lunedì 12 ottobre, e di nuovo dalle 23 del 16 alle 5:30 del 19, sono previste interruzioni e modifiche ai regionali con servizi bus sostitutivi su alcune tratte. I tempi su strada possono aumentare per traffico e fermate.",
            "Dal 19 al 26 ottobre cambiano inoltre orari e percorsi di diversi regionali sulle direttrici Bologna-Ravenna-Rimini-Pesaro e collegate. RFI segnala che i sistemi di vendita sono aggiornati: la ricerca della singola soluzione mostra il programma previsto per quel giorno.",
            "Chi viaggia con coincidenze dovrebbe ricontrollare numero del treno, stazione di partenza e tratta coperta dal bus. Sui mezzi sostitutivi possono valere regole diverse per biciclette e animali; le informazioni della compagnia che emette il biglietto restano il riferimento operativo.",
        ],
        "fonti": [{"url": "https://www.rfi.it/it/news-e-media/infomobilita/avvisi/2026/10/9/roma---ravenna-milano--suzzara---ferrara---bologna---ravenna---r.html", "nome": "Rete Ferroviaria Italiana — calendario dei lavori e modifiche ai collegamenti."}],
        "image_source": "rfi",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di lavori ferroviari sulla linea Ravenna-Rimini con treno fermo; scena non documentaria.",
        "image_prompt": "Rail maintenance on the Ravenna-Rimini line with a stopped Italian train and recognizable Adriatic landscape, ultra-realistic editorial illustration, authentic railway branding, no text overlay.",
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

    site.sync_surfaces(written, f"/notizie/{written[0]['slug']}.html", VERSION, update_manifest=False)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION,
        "currentVersion": VERSION,
        "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": f"eventi-biglietti-avvisi-v{VERSION}",
        "date": base.date().isoformat(),
        "release_date": base.date().isoformat(),
        "updated_at": base.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
