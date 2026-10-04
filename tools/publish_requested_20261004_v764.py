#!/usr/bin/env python3
"""Pubblica quattro notizie richieste e aggiorna il GP di F1 già online."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 764
ROME = ZoneInfo("Europe/Rome")
F1_SLUG = "f1-gp-bahrain-sepang-verstappen-pole-antonelli-terzo-4-ottobre-2026"

IMAGE_SPECS = {
    F1_SLUG: {
        "path": ROOT / "generated_images/f1-verstappen-sepang-v764.jpg",
        "alt": "Illustrazione editoriale IA di Max Verstappen in pista sotto la pioggia a Sepang; scena non documentaria.",
        "prompt": "Max Verstappen wins a rain-hit Formula 1 race at Sepang, driving through spray on wet asphalt; premium photorealistic editorial sports image, wide 16:9, no readable sponsors, logos, text or watermark.",
        "public": True,
        "sensitive": False,
    },
    "mattarella-assisi-san-francesco-festa-nazionale-4-ottobre-2026": {
        "path": ROOT / "generated_images/mattarella-assisi-v764.jpg",
        "alt": "Illustrazione editoriale IA di Sergio Mattarella ad Assisi con frati francescani e rappresentanti istituzionali; scena non documentaria.",
        "prompt": "Italian President Sergio Mattarella arriving in Assisi for Saint Francis national celebrations with Franciscan friars and institutional representatives; premium photorealistic editorial image, wide 16:9, no text or watermark.",
        "public": True,
        "sensitive": False,
    },
    "caivano-operaio-morto-indagini-capannone-4-ottobre-2026": {
        "path": ROOT / "generated_images/caivano-operaio-v764.jpg",
        "alt": "Illustrazione editoriale IA di un capannone e di una strada isolata nell'area napoletana, senza persone; nessuna ricostruzione dell'incidente.",
        "prompt": "Sober context for an investigated fatal workplace accident in Caivano: empty warehouse roof under maintenance, ladder, waterproofing rolls and isolated access road; no people or reenactment, wide 16:9.",
        "public": False,
        "sensitive": True,
    },
    "san-paolo-pallone-gigante-disintegrato-cielo-4-ottobre-2026": {
        "path": ROOT / "generated_images/san-paolo-pallone-v764.jpg",
        "alt": "Illustrazione editoriale IA di un enorme pallone artigianale senza passeggeri che si disintegra sopra San Paolo; scena non documentaria.",
        "prompt": "Gigantic unmanned paper balloon disintegrating high above the outskirts of Sao Paulo, fragments and smoke visible at a safe distance; factual premium editorial image, wide 16:9, no people, text or watermark.",
        "public": False,
        "sensitive": False,
    },
    "vieste-padre-figlio-caduta-matrimonio-3-ottobre-2026": {
        "path": ROOT / "generated_images/vieste-padre-figlio-v764.jpg",
        "alt": "Illustrazione editoriale IA di una terrazza per ricevimenti a Vieste con un'area messa in sicurezza, senza persone; nessuna ricostruzione della caduta.",
        "prompt": "Sober context for father and child injured at a Vieste wedding venue: empty terrace with secured skylight area and distant Adriatic coast; no people, accident reenactment, text or watermark, wide 16:9.",
        "public": False,
        "sensitive": True,
    },
}

F1 = {
    "slug": F1_SLUG,
    "titolo": "Verstappen vince a Sepang sotto la pioggia, Antonelli secondo",
    "sommario": "Il leader del Mondiale scatta dalla terza posizione e guida al via, ma Verstappen riprende la testa dopo la safety car. Hamilton completa il podio; Russell si ritira nel finale.",
    "categoria": "Sport",
    "luogo": "Sepang, Malesia",
    "formato": "standard",
    "parole_chiave_titolo": ["Verstappen", "Antonelli secondo"],
    "dati_chiave": [
        {"icona": "◆", "valore": "1°", "etichetta": "Verstappen al traguardo"},
        {"icona": "▲", "valore": "2°", "etichetta": "Antonelli consolida il primato"},
        {"icona": "●", "valore": ">90 min", "etichetta": "ritardo per la pioggia"},
    ],
    "paragrafi": [
        "Max Verstappen ha vinto il Bahrain Grand Prix disputato domenica 4 ottobre sul circuito malese di Sepang. Il pilota Red Bull ha ottenuto il primo successo della stagione davanti a Kimi Antonelli, leader del Mondiale, e a Lewis Hamilton su Ferrari.",
        "La corsa è partita con oltre novanta minuti di ritardo per la pioggia e le condizioni della pista. Prima del via alcune monoposto sono state richiamate nella corsia box; l'attesa ha trasformato la gestione dell'acqua e delle gomme nel primo passaggio decisivo della gara.",
        "Antonelli ha avuto lo spunto migliore quando il semaforo si è spento. Partito terzo, ha preso la testa, mentre George Russell è salito dal settimo al secondo posto e Verstappen, che scattava dalla pole, è scivolato in terza posizione.",
        "Il vantaggio Mercedes non è durato. Alla ripartenza del tredicesimo giro, dopo una fase di safety car, Verstappen ha superato Antonelli e si è ripreso la leadership, secondo la ricostruzione pubblicata dalla Formula 1.",
        "Da quel momento l'olandese ha controllato il ritmo fino alla bandiera a scacchi. Antonelli ha difeso la seconda posizione e ha limitato l'effetto della vittoria di Verstappen sulla classifica piloti, aggiungendo un altro podio alla sua stagione.",
        "Hamilton ha chiuso terzo dopo essere partito dalla prima fila. Charles Leclerc è arrivato quarto con l'altra Ferrari, mentre Russell, che occupava la terza posizione, si è ritirato a cinque giri dalla fine per un sospetto problema alla power unit.",
        "Il ritiro di Russell ha un peso superiore al singolo risultato. Il britannico era il rivale più vicino di Antonelli nella corsa al titolo: il secondo posto del pilota italiano, unito allo zero del compagno, aumenta il margine del leader senza che serva una vittoria.",
        "La sequenza spiega anche perché il risultato non coincide con la fotografia della partenza. Mercedes ha occupato le prime due posizioni nei primi metri, ma il riavvio dopo la safety car ha restituito a Verstappen l'occasione di sfruttare la velocità mostrata in qualifica.",
        "Il nome ufficiale dell'evento resta Bahrain Grand Prix, benché la gara si sia corsa in Malesia. Sepang ha ospitato l'appuntamento dopo la modifica del calendario e ha riportato la Formula 1 sul tracciato per la prima volta dal 2017.",
        "L'articolo pubblicato in mattinata sulle qualifiche è stato aggiornato con il risultato finale, senza aprire una seconda pagina sullo stesso Gran Premio. La data di pubblicazione originaria resta invariata; l'ordine d'arrivo sostituisce le informazioni ormai superate sulla griglia.",
    ],
    "fonti": [
        {"url": "https://www.reuters.com/sports/formula1/verstappen-wins-rain-delayed-bahrain-grand-prix-malaysia-2026-10-04/", "descrizione": "Reuters — risultato, ritardo per la pioggia e ritiro di Russell"},
        {"url": "https://www.formula1.com/en/racing/2026/bahrain", "descrizione": "Formula 1 — pagina ufficiale del Bahrain Grand Prix in Malaysia"},
        {"url": "https://www.formula1.com/en/video/2026-bahrain-grand-prix-antonelli-and-russell-give-mercedes-a-1-2-lead-on-the-race-start.1878108841209792429", "descrizione": "Formula 1 — partenza con Antonelli e Russell davanti"},
        {"url": "https://www.formula1.com/en/video/2026-bahrain-grand-prix-verstappen-retakes-the-lead-on-the-safety-car-restart.1878110027701100715", "descrizione": "Formula 1 — sorpasso di Verstappen alla ripartenza"},
    ],
}

NEW_ARTICLES = [
    {
        "slug": "caivano-operaio-morto-indagini-capannone-4-ottobre-2026",
        "titolo": "Caivano, operaio muore dopo il ricovero: indagini sul capannone",
        "sommario": "Salvatore Calignano, 61 anni, era stato trovato con gravi traumi in una strada isolata. L'autopsia e gli accertamenti dei carabinieri dovranno stabilire dove sia avvenuta la caduta.",
        "categoria": "Cronaca",
        "luogo": "Caivano",
        "formato": "standard",
        "parole_chiave_titolo": ["Caivano", "capannone"],
        "dati_chiave": [
            {"icona": "◆", "valore": "61 anni", "etichetta": "età della vittima"},
            {"icona": "▲", "valore": "118", "etichetta": "soccorso in strada"},
            {"icona": "●", "valore": "autopsia", "etichetta": "disposta dalla Procura"},
        ],
        "paragrafi": [
            "Salvatore Calignano, operaio edile di 61 anni residente a Orta di Atella, è morto all'Ospedale del Mare di Napoli dopo il ricovero per un grave politrauma. Era stato soccorso venerdì in via Fossa del Lupo, una zona isolata di Caivano, dopo una chiamata al 118.",
            "La Procura di Napoli Nord indaga sull'ipotesi di un incidente sul lavoro. I carabinieri devono ancora ricostruire il luogo esatto della caduta, chi abbia chiesto l'intervento dei sanitari e come l'uomo sia arrivato nel punto in cui è stato trovato.",
            "Prima di perdere conoscenza, Calignano avrebbe riferito ai soccorritori di essere caduto da una scala. Questa dichiarazione orienta gli accertamenti, ma non prova da sola né il luogo dell'incidente né la successione degli eventi precedenti al ritrovamento.",
            "La moglie ha raccontato al proprio legale che il marito le aveva telefonato intorno alle 13 dicendo di trovarsi sul tetto di un capannone. Secondo il suo racconto, stava posando una guaina isolante e lavorava senza un contratto regolare.",
            "Nel complesso indicato dalla donna è stata trovata l'automobile della famiglia. La presenza del veicolo costituisce un elemento verificabile, ma la dinamica resta sottoposta alle indagini e non consente ancora di attribuire responsabilità a persone o imprese.",
            "La frase della moglie sull'eventuale abbandono in strada esprime un sospetto, non una conclusione investigativa. Non è stato accertato chi abbia spostato l'operaio, se sia stato spostato, né se qualcuno abbia omesso di prestare soccorso.",
            "La Procura ha disposto l'autopsia e il sequestro del telefono della vittima. L'esame medico-legale potrà chiarire la compatibilità delle lesioni con una caduta; i dati del cellulare e la chiamata al 118 possono aiutare a ricostruire tempi, contatti e spostamenti.",
            "RaiNews e altre cronache locali avevano riferito già il giorno precedente del ritrovamento in stato di incoscienza e delle lesioni multiple. L'aggiornamento decisivo è la morte in ospedale e l'emersione dell'ipotesi del lavoro sul tetto, ancora da verificare in sede giudiziaria.",
            "Il caso comprende quindi tre livelli distinti: il decesso e il soccorso in strada sono accertati; la caduta da una scala è una dichiarazione attribuita alla vittima; il lavoro irregolare e l'eventuale abbandono derivano dal racconto della famiglia e richiedono riscontri.",
        ],
        "fonti": [
            {"url": "https://www.ansa.it/sito/notizie/cronaca/2026/10/04/operaio-edile-morto-in-ospedale-stava-lavorando-in-nero-su-tetto-capannone_e247d139-6bcb-4859-8475-8ac5bfd697de.html", "descrizione": "ANSA — morte, testimonianza della moglie e atti disposti dalla Procura"},
            {"url": "https://www.rainews.it/tgr/campania/articoli/2026/10/caivano-61-enne-trovato-incosciente-in-strada-e-grave--f8a74b34-3c05-40fa-80c9-fc6c5f6b001d.html", "descrizione": "RaiNews TGR Campania — primo ritrovamento e condizioni dell'operaio"},
            {"url": "https://napoli.repubblica.it/cronaca/2026/10/03/news/operaio_trovato_in_strada_in_fin_di_vita_muore_in_ospedale_ipotesi_incidente_sul_lavoro-425624388/amp/", "descrizione": "la Repubblica Napoli — soccorso, decesso e ipotesi d'infortunio"},
        ],
    },
    {
        "slug": "san-paolo-pallone-gigante-disintegrato-cielo-4-ottobre-2026",
        "titolo": "San Paolo, pallone gigante si disintegra sopra la città",
        "sommario": "Il video mostra la struttura perdere pezzi ad alta quota. Le prime ricostruzioni parlano di un balão clandestino alto oltre 50 metri e carico di fuochi d'artificio.",
        "categoria": "Mondo",
        "luogo": "San Paolo",
        "formato": "standard",
        "parole_chiave_titolo": ["San Paolo", "pallone gigante"],
        "dati_chiave": [
            {"icona": "◆", "valore": ">50 m", "etichetta": "altezza riferita"},
            {"icona": "▲", "valore": "9.605/98", "etichetta": "legge ambientale brasiliana"},
            {"icona": "●", "valore": "senza guida", "etichetta": "struttura non pilotata"},
        ],
        "paragrafi": [
            "Un enorme pallone artigianale senza passeggeri si è disintegrato in volo sopra San Paolo, in Brasile. Un video diffuso domenica 4 ottobre mostra l'involucro perdere rapidamente consistenza, mentre frammenti e fumo si disperdono nel cielo della metropoli.",
            "Le immagini non mostrano una mongolfiera turistica con cesta e pilota. Si tratta del fenomeno brasiliano dei balões: grandi strutture di carta lanciate clandestinamente e trasportate dal vento senza un sistema di guida o una zona di atterraggio controllata.",
            "Una ricostruzione pubblicata da iLMeteo attribuisce al pallone un'altezza superiore a 50 metri e la presenza di fuochi d'artificio. Questi dettagli non sono visibili integralmente nel filmato e vanno letti come informazioni riferite, non come misure ricavate dal video.",
            "La sequenza diventa pericolosa quando la struttura si rompe. Ogni frammento acceso può cadere su tetti, aree verdi, linee elettriche o strade; inoltre il percorso dipende dalle correnti e non può essere corretto da terra dopo il lancio.",
            "La pratica è vietata in Brasile dalla legge sui reati ambientali 9.605 del 1998, richiamata anche nei resoconti dell'episodio. Il divieto riguarda fabbricazione, vendita, trasporto e lancio di palloni capaci di provocare incendi nelle foreste, nelle aree urbane o in altri insediamenti.",
            "Il dato più importante che il video non permette di stabilire è il punto di caduta. Al momento delle fonti consultate non risultavano informazioni precise su eventuali danni, feriti o interventi dei vigili del fuoco collegati a questo specifico episodio.",
            "L'assenza di tali informazioni non equivale alla conferma che non vi siano state conseguenze. Significa soltanto che il filmato documenta la disintegrazione in aria, mentre il seguito della traiettoria e l'impatto dei detriti richiedono comunicazioni delle autorità locali.",
            "La scala del pallone spiega perché immagini simili attirino attenzione, ma non deve confondere la natura dell'evento. Non è un incidente dell'aviazione commerciale né l'esplosione di un mezzo con persone a bordo: è il cedimento di una struttura illegale non pilotata sopra un'area densamente abitata.",
        ],
        "fonti": [
            {"url": "https://www.ansa.it/sito/videogallery/mondo/2026/10/04/un-gigantesco-pallone-aerostatico-si-disintegra-nel-cielo-di-san-paolo_57e3c1f3-5a33-4417-9887-c22b80065fb3.html", "descrizione": "ANSA Video — immagini della disintegrazione nel cielo di San Paolo"},
            {"url": "https://www.ilmeteo.it/notizie/il-fenomeno-dei-baloes-in-brasile-limpatto-dei-lanci-clandestini-sulla-sicurezza-delle-metropoli-video-153002", "descrizione": "iLMeteo — dimensioni riferite, fuochi d'artificio e contesto dei balões"},
        ],
    },
    {
        "slug": "mattarella-assisi-san-francesco-festa-nazionale-4-ottobre-2026",
        "titolo": "Mattarella ad Assisi: San Francesco torna festa nazionale",
        "sommario": "Il capo dello Stato partecipa alle celebrazioni dell'ottavo centenario. Il 4 ottobre è di nuovo un giorno festivo nazionale, per la prima volta dopo la legge del 2025.",
        "categoria": "Politica",
        "luogo": "Assisi",
        "formato": "standard",
        "parole_chiave_titolo": ["Mattarella", "festa nazionale"],
        "dati_chiave": [
            {"icona": "◆", "valore": "4 ott", "etichetta": "festa nazionale ripristinata"},
            {"icona": "▲", "valore": "800 anni", "etichetta": "dalla morte di Francesco"},
            {"icona": "●", "valore": "2026", "etichetta": "prima ricorrenza festiva"},
        ],
        "paragrafi": [
            "Il presidente della Repubblica Sergio Mattarella è arrivato ad Assisi domenica 4 ottobre per le celebrazioni di San Francesco, patrono d'Italia. La ricorrenza torna quest'anno a essere una festa nazionale con effetti sul calendario civile e sul lavoro.",
            "Ad accogliere il capo dello Stato c'erano il sottosegretario Alfredo Mantovano, la presidente dell'Umbria Stefania Proietti, il sindaco di Assisi Valter Stoppini e il custode del Sacro Convento, fra Marco Moroni. La cerimonia cade nell'ottavo centenario della morte del santo.",
            "Il programma prevede la celebrazione eucaristica nella Basilica superiore e l'accensione della Lampada votiva dei Comuni d'Italia. Per la prima volta il gesto è affidato alla città di Assisi in rappresentanza dell'intero popolo italiano, anziché a una sola regione.",
            "Dopo la celebrazione Mattarella rivolge un messaggio al Paese dalla Loggia del Sacro Convento. La presenza dei presidenti di Regione, dei sindaci dei capoluoghi e degli ambasciatori amplia la giornata oltre la tradizionale delegazione territoriale.",
            "La novità pratica riguarda lo status del 4 ottobre. La legge 151 del 2025 ha inserito la festa di San Francesco tra i giorni festivi nazionali, con l'osservanza dell'orario festivo nei luoghi di lavoro e gli effetti previsti per gli atti giuridici.",
            "La data era già riconosciuta come solennità civile dedicata alla pace, alla fraternità e al dialogo tra culture e religioni. Il passaggio del 2025 non ha creato da zero la ricorrenza: le ha restituito il rango di giorno festivo nazionale a partire dal 2026.",
            "Mattarella promulgò la legge l'8 ottobre 2025, accompagnandola con una lettera ai presidenti delle Camere. Il Quirinale segnalò allora alcuni aspetti tecnici, ma confermò gli effetti generali del nuovo giorno festivo.",
            "Il calendario delle celebrazioni collega il significato civile a quello religioso. Il 3 ottobre è stato dedicato al Transito di Francesco e al pellegrinaggio notturno; il 4 riunisce la messa, la Lampada votiva e i messaggi istituzionali.",
            "Assisi diventa così il centro della prima applicazione concreta della legge. L'evento non è soltanto una visita presidenziale: coincide con la riapertura di una festività nazionale e con una rappresentanza estesa delle istituzioni italiane.",
        ],
        "fonti": [
            {"url": "https://www.ansa.it/sito/notizie/politica/2026/10/04/il-presidente-mattarella-ad-assisi-per-le-celebrazioni-di-san-francesco_166af3b4-37e5-401f-ad90-eebef5c84503.html", "descrizione": "ANSA — arrivo di Mattarella e autorità presenti"},
            {"url": "https://basilica.sanfrancesco.org/notizie/celebrazioni-per-la-festa-di-san-francesco-dassisi-3-e-4-ottobre-2026", "descrizione": "Sacro Convento — programma ufficiale delle celebrazioni"},
            {"url": "https://www.quirinale.it/it/comunicato/presidente-mattarella-ha-promulgato-legge-per-istituzione-festa-nazionale-san-francesco-d-assisi-ha-inviato-lettera-presidenti-camere", "descrizione": "Quirinale — promulgazione e contenuto della legge sulla festa nazionale"},
            {"url": "https://presidenza.governo.it/USRI/confessioni/IniziativeLegislative/Tabella_XIX-legislatura_20260116.pdf", "descrizione": "Presidenza del Consiglio — iter e numero della legge 151/2025"},
        ],
    },
    {
        "slug": "vieste-padre-figlio-caduta-matrimonio-3-ottobre-2026",
        "titolo": "Vieste, padre e figlio cadono durante un matrimonio: grave il 40enne",
        "sommario": "Il bambino di 10 anni avrebbe ceduto su un lucernario; il padre è precipitato tentando di raggiungerlo. L'area è stata sequestrata e la Procura di Foggia coordina gli accertamenti.",
        "categoria": "Cronaca",
        "luogo": "Vieste",
        "formato": "standard",
        "parole_chiave_titolo": ["Vieste", "grave il 40enne"],
        "dati_chiave": [
            {"icona": "◆", "valore": "10 anni", "etichetta": "età del bambino"},
            {"icona": "▲", "valore": "4-5 m", "etichetta": "caduta riferita"},
            {"icona": "●", "valore": "2", "etichetta": "trasporti in elisoccorso"},
        ],
        "paragrafi": [
            "Un uomo di 40 anni e il figlio di 10 sono rimasti feriti venerdì 3 ottobre durante una festa di matrimonio in una sala ricevimenti a Vieste, nel Foggiano. Il padre è ricoverato in prognosi riservata; il bambino ha riportato la frattura di un arto inferiore.",
            "Secondo la prima ricostruzione, il bambino stava giocando con alcuni coetanei su un terrazzino quando sarebbe precipitato per circa quattro o cinque metri nella struttura sottostante. Il punto esatto e la tenuta del lucernario sono oggetto degli accertamenti.",
            "Il padre è accorso per raggiungere il figlio ed è caduto a sua volta all'interno del vano. RaiNews riferisce che l'uomo ha riportato un grave trauma cranico; le sue condizioni sono considerate molto serie.",
            "Entrambi sono stati trasferiti con l'elisoccorso in strutture sanitarie. Il bambino non risulta in pericolo di vita, mentre per il quarantenne i medici hanno mantenuto la prognosi riservata.",
            "La festa di nozze è stata interrotta. I carabinieri hanno sequestrato l'area e stanno verificando la dinamica sotto il coordinamento della Procura di Foggia, secondo quanto riportato dalla TGR Puglia.",
            "Il sequestro serve a conservare lo stato dei luoghi e a permettere rilievi sulla protezione dell'apertura, sui materiali e sull'accessibilità del terrazzino. Non equivale all'individuazione di una responsabilità penale né dimostra, da solo, una violazione delle regole di sicurezza.",
            "Le fonti concordano sull'ordine delle due cadute e sulle condizioni generali dei feriti. Restano invece da stabilire la causa del primo cedimento, l'eventuale presenza di barriere adeguate e chi avesse la gestione dell'area in quel momento.",
            "Per tutelare il minore non sono stati diffusi nomi o altri dettagli personali. La notizia riguarda la dinamica dell'incidente e gli accertamenti sulla sicurezza del luogo, non l'identità della famiglia o degli sposi.",
            "L'elemento decisivo sarà l'esito dei rilievi. Fino ad allora è corretto descrivere la caduta come una ricostruzione iniziale e distinguere i dati sanitari comunicati dalle ipotesi sulle cause.",
        ],
        "fonti": [
            {"url": "https://www.ansa.it/puglia/notizie/2026/10/03/padre-e-figlio-cadono-dal-terrazzo-durante-la-festa-di-nozze-grave-40enne_c629138e-676d-45b5-ad21-c311789a9363.html", "descrizione": "ANSA — caduta, trasporti in elisoccorso e condizioni dei feriti"},
            {"url": "https://www.rainews.it/amp/tgr/puglia/articoli/2026/10/vieste-padre-ferito-matrimonio-3385ffd3-914c-4fad-8680-2923711bd770.html", "descrizione": "RaiNews TGR Puglia — prima dinamica, trauma cranico e sequestro dell'area"},
            {"url": "https://tg24.sky.it/cronaca/2026/10/04/vieste-incidente-festa-di-nozze", "descrizione": "Sky TG24 — conferma indipendente dell'incidente e degli accertamenti"},
        ],
    },
]


def make_image(slug: str) -> dict:
    spec = IMAGE_SPECS[slug]
    im = Image.open(spec["path"]).convert("RGB")
    ratio = 16 / 9
    w, h = im.size
    if w / h > ratio:
        new_w = round(h * ratio)
        left = (w - new_w) // 2
        im = im.crop((left, 0, left + new_w, h))
    else:
        new_h = round(w / ratio)
        top = (h - new_h) // 2
        im = im.crop((0, top, w, top + new_h))
    variants = []
    for width in (480, 800, 1200):
        height = round(width * 9 / 16)
        out = ROOT / "assets/images/editorial-auto" / f"{slug}-v{VERSION}-{width}.webp"
        im.resize((width, height), Image.Resampling.LANCZOS).save(out, "WEBP", quality=88, method=6)
        variants.append({
            "w": width,
            "h": height,
            "src": f"/assets/images/editorial-auto/{out.name}",
            "sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
            "bytes": out.stat().st_size,
        })
    image = {
        "key": f"{slug}-v{VERSION}",
        "alt": spec["alt"],
        "prompt": spec["prompt"],
        "variants": variants,
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "sensitiveContext": spec["sensitive"],
        "reenactedEvent": False,
    }
    if spec["public"]:
        image["syntheticLikeness"] = "public-figure"
    return image


def set_schema_times(path: Path, published: str, modified: str | None = None) -> None:
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', page, count=1)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{modified or published}"', page, count=1)
    path.write_text(page, encoding="utf-8")


def update_f1(image: dict, modified: str) -> None:
    path = ROOT / "notizie" / f"{F1_SLUG}.html"
    old_page = path.read_text(encoding="utf-8")
    old_doc = html.fromstring(old_page)
    old_schema = json.loads(old_doc.xpath('//script[@type="application/ld+json"]')[0].text)
    published = old_schema["datePublished"]
    old_note = old_doc.xpath('//aside[contains(@class,"cm-name-card")]')
    old_note_html = html.tostring(old_note[0], encoding="unicode") if old_note else ""

    backup = path.with_suffix(".html.v764-backup")
    path.rename(backup)
    try:
        slug, page = site.render_article(F1, image, VERSION)
        page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', page, count=1)
        page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{modified}"', page, count=1)
        if old_note_html:
            page = re.sub(r'<aside class="cm-name-card".*?</aside>', old_note_html, page, count=1)
        path.write_text(page, encoding="utf-8")
        if slug != F1_SLUG:
            raise RuntimeError("slug F1 modificato durante l'aggiornamento")
    except Exception:
        path.unlink(missing_ok=True)
        backup.rename(path)
        raise
    backup.unlink()


def replace_feed_summaries(articles: list[dict]) -> None:
    by_url = {f"/notizie/{a['slug']}.html": a for a in articles}
    for rel in ("assets/data/home-feed-v210.json", "assets/data/search-index-v210.json"):
        path = ROOT / rel
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in data.get("items", []):
            article = by_url.get(item.get("url"))
            if article:
                item["excerpt"] = article["sommario"]
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    now = datetime.now(ROME).replace(microsecond=0)
    images = {slug: make_image(slug) for slug in IMAGE_SPECS}
    written = []
    for index, article in enumerate(NEW_ARTICLES):
        image = images[article["slug"]]
        slug = site.write_article(article, image, VERSION)
        site.register_image(image, slug, VERSION)
        published = (now - timedelta(minutes=index)).isoformat()
        set_schema_times(ROOT / "notizie" / f"{slug}.html", published)
        written.append(article)
        print("created", slug, published)

    update_f1(images[F1_SLUG], now.isoformat())
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    f1_url = f"/notizie/{F1_SLUG}.html"
    registry["items"] = [row for row in registry.get("items", []) if row.get("article") != f1_url]
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.register_image(images[F1_SLUG], F1_SLUG, VERSION)
    print("updated", F1_SLUG)

    all_articles = written + [F1]
    site.sync_surfaces(all_articles, f"/notizie/{written[0]['slug']}.html", VERSION)
    replace_feed_summaries(all_articles)
    site.sync_surfaces(all_articles, f"/notizie/{written[0]['slug']}.html", VERSION)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION,
        "currentVersion": VERSION,
        "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": "requested-news-batch-v764",
        "date": "2026-10-04",
        "release_date": "2026-10-04",
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    (ROOT / "RELEASE-NOTES-v764.md").write_text(
        "# CurioMondo v764 — notizie richieste del 4 ottobre 2026\n\n"
        "- Quattro nuovi articoli verificati: Caivano, pallone su San Paolo, Mattarella ad Assisi e incidente di Vieste.\n"
        "- Aggiornata la pagina F1 già esistente con il risultato del GP di Sepang, senza duplicati e conservando datePublished.\n"
        "- Cinque nuove hero editoriali IA in formato panoramico 16:9, con visual non ricostruttivi per le notizie sensibili.\n"
        "- Sincronizzate homepage, archivio, categorie, ricerca, feed e sitemap.\n",
        encoding="utf-8",
    )
    print("DONE", VERSION, "new", len(written), "updated", 1)


if __name__ == "__main__":
    main()
