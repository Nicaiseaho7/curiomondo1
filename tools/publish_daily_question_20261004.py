#!/usr/bin/env python3
"""Pacchetto Domanda del giorno del 4 ottobre 2026.

La domanda n. 1017 e stata verificata sul PDF privato originale. Il PDF non
viene copiato nel repository. Il rilascio collega un eBook esistente conforme
e pubblica le due guide previste dalla coda canonica.
"""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from html import escape
from pathlib import Path
from zoneinfo import ZoneInfo
import hashlib
import json
import re

from lxml import etree, html

import build_v501_daily as shared
from daily_question_auto import (
    choose_question,
    render_question_page,
    update_feed,
    update_home,
    update_sitemap,
)

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-10-04"
DATE_LABEL = "4 ottobre 2026"
NUMBER = 1017
QUESTION = "Quanto della nostra identità sparirebbe in un congedo lungo?"
QUESTION_SHA256 = "72503b154373f03b5489e78bdad110c9338b28068f3c33131b9c6a183e4c80ab"
SLUG = "quanto-della-nostra-identita-sparirebbe-in-un-congedo-lungo"
QURL = f"/domanda-del-giorno/{SLUG}/"
BOOK_URL = "/biblioteca/vita-relazioni/domande-per-conoscersi/se-il-successo-non-fosse-visibile-a-nessuno-quale-obiettivo-continueresti-a-inseguire/"
BOOK_TITLE = "Il successo quando nessuno guarda"

PACKAGE = {
    "excerpt": "Una riflessione su lavoro, ruolo e appartenenza: che cosa resta di noi quando per molto tempo nessuno ci chiede di essere produttivi?",
    "answer_paragraphs": [
        "Un congedo lungo non cancellerebbe necessariamente la nostra identità, ma renderebbe visibile quanta parte di essa abbiamo affidato a un ruolo. Finché ogni giornata ha orari, compiti e persone che si aspettano qualcosa da noi, è facile confondere ciò che facciamo con ciò che siamo. Quando quella struttura si interrompe, il silenzio iniziale può sembrare una perdita anche se è soltanto uno spazio ancora senza forma.",
        "Sparirebbero alcuni segnali esterni: il titolo professionale, le urgenze, i risultati misurabili, le conversazioni nate dal lavoro. Potrebbe diminuire anche il senso di utilità, soprattutto se siamo abituati a ricevere conferme attraverso problemi risolti e responsabilità sostenute. Non significa che quel valore fosse falso. Significa che dipendeva anche da un ambiente che lo riconosceva ogni giorno.",
        "Resterebbero però qualità che il ruolo rendeva visibili senza crearle: pazienza, precisione, curiosità, capacità di ascoltare, desiderio di costruire. Un congedo può spostarle altrove. La persona organizzata in ufficio può usarle per prendersi cura di qualcuno; chi guidava un gruppo può imparare a stare in una relazione senza dirigere. L’identità non coincide con il luogo in cui una capacità viene esercitata.",
        "Il vuoto può essere più duro quando il congedo non è scelto o comporta incertezza economica, malattia o responsabilità di cura. In quei casi non basta invitare a scoprire se stessi. Servono sicurezza, tempo e relazioni che non giudichino la persona dalla sua produttività. Una pausa forzata può aprire domande importanti, ma non deve essere romanticizzata né trattata come un semplice esercizio di crescita.",
        "Forse il criterio più utile è osservare che cosa cercheremmo di ricostruire per primo. Se sentissimo il bisogno immediato di riempire ogni ora, potremmo domandarci quale paura stiamo tenendo lontana. Se invece emergessero legami, interessi e forme di presenza rimaste ai margini, il congedo mostrerebbe che l’identità era più ampia del ruolo, anche quando non avevamo tempo per accorgercene.",
        "Non tutto ciò che scompare durante una pausa merita di essere recuperato. Alcune abitudini erano soltanto adattamenti a un ritmo; altre custodivano competenze, comunità e orgoglio autentici. La domanda allora non è soltanto quanto di noi resterebbe, ma quale parte vorremmo riportare con noi al ritorno e quale potremmo finalmente lasciare andare.",
    ],
}

GUIDES = [
    {
        "topic": "Come resettare telefono",
        "slug": "come-resettare-telefono-android-iphone",
        "title": "Come resettare un telefono Android o iPhone senza perdere dati",
        "deck": "Backup, account, eSIM e controlli finali: la procedura sicura per inizializzare lo smartphone e prepararlo al riuso o alla vendita.",
        "sections": [
            ("Capire quale reset serve davvero", [
                "Riavviare, ripristinare le impostazioni e inizializzare il telefono sono operazioni diverse. Un riavvio spegne e riaccende il sistema senza cancellare i dati. Il ripristino di rete o delle sole impostazioni può risolvere problemi specifici mantenendo foto e documenti. Il ripristino di fabbrica, invece, elimina app, account e contenuti locali: va usato quando il dispositivo deve essere ceduto, quando si vuole ricominciare da zero o quando l’assistenza ufficiale lo indica dopo tentativi meno invasivi.",
                "Prima di scegliere l’opzione più drastica, annota il problema e prova gli aggiornamenti, il riavvio e la rimozione dell’app che causa l’errore. Se il telefono appartiene a un’azienda o a una scuola, non inizializzarlo senza autorizzazione: potrebbe essere gestito da remoto. Se lo stai vendendo, il reset è necessario ma non basta da solo; devi anche verificare che gli account e i blocchi di attivazione siano stati rimossi correttamente.",
            ]),
            ("Preparare backup e credenziali", [
                "Controlla che foto, contatti, messaggi e file importanti esistano davvero fuori dal telefono. Apri alcuni elementi dal cloud o da un computer: vedere un’icona di sincronizzazione non prova che il caricamento sia finito. Per le chat usa la funzione di backup prevista dall’app; per autenticazione a due fattori, password manager e app bancarie verifica la procedura di trasferimento prima di cancellare il dispositivo. Conserva i codici di recupero in un luogo sicuro e separato.",
                "Su Android devi conoscere l’Account Google già configurato, la relativa password e il codice di sblocco. Google avverte che, dopo una modifica recente della password, può essere necessario attendere 24 ore prima del ripristino. Su iPhone verifica Apple Account, codice del dispositivo e backup iCloud o computer. Se è abbinato un Apple Watch, annulla l’abbinamento. Carica il telefono, collegalo a una rete affidabile e non iniziare se potresti aver bisogno urgente del dispositivo durante la procedura.",
            ]),
            ("Resettare Android dalle Impostazioni", [
                "I nomi cambiano tra produttori, ma il percorso parte in genere da Impostazioni e conduce a Sistema, Gestione generale o Informazioni sul telefono, quindi a Opzioni di ripristino o Ripristina dati di fabbrica. Leggi l’elenco dei contenuti che saranno eliminati, controlla l’account indicato e conferma con PIN o password. Google consiglia almeno il 70 per cento di batteria e ricorda che l’operazione può richiedere fino a un’ora. Per il modello preciso, usa la guida del produttore.",
                "Se il telefono non si avvia, le combinazioni di tasti e la modalità di recupero variano molto. Non seguire video riferiti a un modello diverso e non installare firmware casuali: potresti bloccare il dispositivo o perdere protezioni di sicurezza. Dopo il reset, la protezione di ripristino può chiedere l’Account Google usato in precedenza. Prima di vendere il telefono, completa la schermata iniziale solo quanto basta per verificare che non richieda le tue credenziali, poi lascialo alla pagina di benvenuto.",
            ]),
            ("Inizializzare iPhone e gestire la eSIM", [
                "Su iPhone apri Impostazioni, Generali, Trasferisci o inizializza iPhone e scegli Inizializza contenuto e impostazioni. Il riepilogo mostra ciò che verrà rimosso; conferma con il codice e, quando richiesto, con la password dell’Apple Account. Apple permette di scegliere se conservare o eliminare la eSIM. Se stai preparando il telefono per la vendita o il passaggio a un’altra persona, elimina la eSIM; se devi soltanto ripristinare il tuo iPhone e continuare a usarlo, valuta di conservarla secondo le indicazioni dell’operatore.",
                "Attendi la schermata di benvenuto senza forzare il riavvio. Se hai dimenticato il codice o l’iPhone è disabilitato, usa le procedure ufficiali di recupero da Mac o PC; il ripristino cancella i contenuti e non aggira il Blocco attivazione. Chi acquista il dispositivo deve poterlo configurare senza il tuo Apple Account. Controlla anche che l’iPhone non compaia più tra i dispositivi affidabili solo dopo aver verificato che il backup e il trasferimento siano completi.",
            ]),
            ("Controllo finale prima di cedere il telefono", [
                "Rimuovi SIM fisica, scheda di memoria e accessori. Da un altro dispositivo verifica che i dati importanti siano disponibili, poi accendi lo smartphone resettato: deve mostrare la configurazione iniziale e non fotografie, notifiche o account personali. Non inviare mai a un acquirente password o codici per superare un blocco; se compare ancora una richiesta legata al tuo account, risolvi il collegamento tramite l’assistenza ufficiale prima della consegna.",
                "Conserva ricevuta, numero seriale e prova di cancellazione finché il passaggio non è concluso. Per un telefono danneggiato che non consente il reset, usa le funzioni ufficiali di localizzazione e cancellazione remota quando applicabili, ma ricorda che l’ordine verrà eseguito soltanto quando il dispositivo torna online. Se contiene dati sensibili e non può essere avviato, affidati al produttore o a un centro autorizzato invece di consegnarlo a servizi non verificati.",
            ]),
        ],
        "sources": [
            ("Google: ripristinare le impostazioni di fabbrica di Android", "https://support.google.com/android/answer/6088915?hl=it"),
            ("Apple: inizializzare iPhone e gestire la eSIM", "https://support.apple.com/it-it/108931"),
        ],
    },
    {
        "topic": "Come trasferire dati da Android a iPhone (e viceversa)",
        "slug": "come-trasferire-dati-android-iphone-e-viceversa",
        "title": "Come trasferire dati da Android a iPhone e viceversa",
        "deck": "Cavo, Wi-Fi, account e verifiche: come spostare contatti, foto, messaggi e WhatsApp senza cancellare il vecchio telefono troppo presto.",
        "sections": [
            ("Preparare i due telefoni", [
                "Aggiorna entrambi i dispositivi, caricali e collegali all’alimentazione. Controlla lo spazio occupato sul vecchio telefono e quello disponibile sul nuovo, includendo eventuale scheda microSD. Esegui comunque un backup separato: la migrazione copia molti contenuti, ma non sostituisce una copia di sicurezza. Tieni a portata di mano password degli account, PIN, credenziali del gestore telefonico e codici di recupero per le app con autenticazione a due fattori.",
                "La procedura più completa avviene durante la prima configurazione del nuovo telefono. Se hai già terminato la configurazione, alcune funzioni ufficiali richiedono di inizializzarlo e ricominciare; in alternativa dovrai spostare manualmente categorie diverse. Prima di procedere aggiorna WhatsApp e le altre app importanti, verifica che i contatti siano sincronizzati e decidi quando trasferire SIM o eSIM. Non cancellare il vecchio telefono finché non hai controllato tutto sul nuovo.",
            ]),
            ("Da Android a iPhone con Passa a iOS", [
                "Durante la configurazione dell’iPhone scegli Trasferisci app e dati, poi Da Android. Sul vecchio telefono apri l’app ufficiale Passa a iOS, accetta le autorizzazioni necessarie e inserisci il codice mostrato dall’iPhone. I dispositivi creano una connessione temporanea; lasciali vicini, alimentati e senza usare altre app fino al termine indicato sull’iPhone. Quando possibile, un collegamento USB-C diretto può rendere il trasferimento più rapido e stabile.",
                "Apple indica che possono passare contatti, cronologia messaggi, SMS, foto e video della fotocamera, album, file, calendari, account email, cronologia chiamate, Memo Vocali e contenuti WhatsApp supportati. Alcune app gratuite vengono abbinate se esistono anche su App Store, ma devi comunque scaricarle e accedere di nuovo. Musica, libri e PDF possono richiedere un passaggio manuale. Se lo spazio termina, inizializza l’iPhone e ripeti dopo aver ridotto i contenuti o scelto un modello adeguato.",
            ]),
            ("Da iPhone ad Android", [
                "Accendi il nuovo Android e, quando chiede di copiare i dati, scegli iPhone o iPad. Segui il codice QR oppure collega i dispositivi con il cavo indicato. Accedi all’Account Google e seleziona le categorie da copiare. Google consiglia di lasciare i telefoni collegati fino alla fine, anche mentre viene proposta la migrazione della eSIM. Il percorso può cambiare sui dispositivi Samsung, Pixel e di altri produttori: usa l’assistente integrato e l’app ufficiale suggerita durante la configurazione.",
                "Prima di togliere la SIM disattiva iMessage e FaceTime sul vecchio iPhone, così gli SMS non continueranno a essere indirizzati ai servizi Apple. Controlla i contenuti conservati soltanto in iCloud: foto e video possono essere trasferiti con gli strumenti previsti da Apple e Google oppure scaricati e caricati manualmente. Le app acquistate su iOS non diventano automaticamente acquistate su Android; cerca la versione equivalente nel Play Store e verifica gli abbonamenti separatamente.",
            ]),
            ("WhatsApp, autenticazione e dati che non seguono", [
                "Usa il flusso WhatsApp proposto durante la configurazione, con lo stesso numero telefonico e i dispositivi compatibili. Un backup iCloud non si ripristina direttamente su Android e un backup Google Drive non si apre direttamente su iPhone: la migrazione ufficiale crea il ponte tra le piattaforme. Non affidare la cronologia a programmi sconosciuti che chiedono accesso completo a chat, backup o credenziali. Se la procedura fallisce, consulta prima l’assistenza di WhatsApp e dei produttori.",
                "App bancarie, identità digitale, token aziendali, carte di pagamento e autenticazione a due fattori spesso richiedono una nuova attivazione. Trasferisci gli account dell’app di autenticazione con la funzione ufficiale oppure salva i codici di recupero. Scarica biglietti, certificati e documenti che non possono essere riscaricati facilmente. Per le app di salute e dispositivi indossabili verifica esportazione e compatibilità: alcuni dati restano legati all’ecosistema o al produttore.",
            ]),
            ("Verificare prima di cancellare il vecchio dispositivo", [
                "Apri sul nuovo telefono contatti, calendario, foto recenti e vecchie, video, file scaricati, messaggi e registrazioni. Fai una chiamata, invia un SMS e prova la rete dati. Accedi alle app essenziali e controlla che notifiche, codici e abbonamenti funzionino. Confronta il numero approssimativo di foto e la presenza di album o cartelle importanti; una miniatura visibile non garantisce che il file sia disponibile offline.",
                "Usa per alcuni giorni il nuovo dispositivo mantenendo il vecchio spento ma non inizializzato. Quando sei sicuro, esegui il backup finale, rimuovi gli account e applica la procedura di reset corretta. Conservare il vecchio telefono per poco tempo è più prudente che scoprire dopo la cancellazione che una nota, una chat o un codice esisteva soltanto lì. La migrazione è conclusa quando sai ritrovare i contenuti, non quando la barra raggiunge il cento per cento.",
            ]),
        ],
        "sources": [
            ("Apple: passare da Android a iPhone", "https://support.apple.com/it-it/118670"),
            ("Google: passare a un nuovo dispositivo Android", "https://support.google.com/android/answer/6193424?hl=it"),
        ],
    },
]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def dump(path: Path, value: object) -> None:
    write(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def guide_html(guide: dict) -> str:
    body = "".join(
        f"<h2>{escape(title)}</h2>" + "".join(f"<p>{escape(p)}</p>" for p in paragraphs)
        for title, paragraphs in guide["sections"]
    )
    sources = " · ".join(
        f'<a href="{escape(url, quote=True)}" rel="noopener">{escape(label)}</a>'
        for label, url in guide["sources"]
    )
    canonical = f'https://curiomondo.it/biblioteca/tecnologia-ai/smartphone-computer/{guide["slug"]}/'
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(guide["title"])} | Biblioteca CurioMondo</title><meta name="description" content="{escape(guide["deck"], quote=True)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=526"><link rel="stylesheet" href="/assets/css/global-header-v275.css?v=633"><script defer src="/assets/js/global-header-v275.js"></script><script defer src="/assets/js/ga4-v714.js"></script><style>.cm-guide{{max-width:920px;margin:28px auto 64px;padding:clamp(24px,5vw,48px);background:#fff;border:1px solid #d7e6f6;border-radius:28px;box-shadow:0 20px 60px rgba(10,55,105,.1)}}.cm-guide h1{{font-size:clamp(2rem,5vw,3.5rem);line-height:1.08;color:#092f57}}.cm-guide h2{{margin-top:2.3rem;color:#1266c3}}.cm-guide p{{font:1.08rem/1.78 Georgia,serif;color:#213a53}}.art-sources{{margin-top:2.5rem;padding:18px 20px;border-radius:18px;background:#edf5ff}}html.cm-dark .cm-guide{{background:#0c2038}}html.cm-dark .cm-guide p{{color:#e8f1fb}}</style></head><body><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main><article class="cm-guide"><p class="cb-kicker">Guida pratica · {DATE_LABEL}</p><h1>{escape(guide["title"])}</h1><p><strong>{escape(guide["deck"])}</strong></p>{body}<aside class="art-sources" aria-label="Fonti consultate"><p><strong>Fonti consultate</strong></p><p>{sources}</p></aside></article></main><footer class="cb-footer"><div class="cb-shell">© 2026 CurioMondo</div></footer></body></html>'''


def guide_index() -> str:
    cards = "".join(
        f'<a class="cb-subcard" href="/biblioteca/tecnologia-ai/smartphone-computer/{g["slug"]}/"><span class="cb-kicker">{DATE_LABEL} · Guida</span><h2>{escape(g["title"])}</h2><p>{escape(g["deck"])}</p><b>Leggi la guida →</b></a>'
        for g in GUIDES
    )
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Guide Smartphone e Computer | CurioMondo</title><meta name="description" content="Guide pratiche CurioMondo per smartphone, computer, trasferimenti, backup e sicurezza digitale."><meta name="robots" content="index,follow"><link rel="canonical" href="https://curiomondo.it/biblioteca/tecnologia-ai/smartphone-computer/"><link rel="stylesheet" href="/assets/css/biblioteca-v1.css?v=526"><link rel="stylesheet" href="/assets/css/global-header-v275.css?v=633"><script defer src="/assets/js/global-header-v275.js"></script><script defer src="/assets/js/ga4-v714.js"></script></head><body><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main><section class="cb-hero"><div class="cb-shell cb-hero-copy"><span class="cb-kicker">Biblioteca</span><h1>Smartphone e computer</h1><p>Procedure chiare per proteggere dati, account e dispositivi.</p></div></section><div class="cb-shell"><section class="cb-subgrid">{cards}</section></div></main><footer class="cb-footer"><div class="cb-shell">© 2026 CurioMondo</div></footer></body></html>'''


def add_feed_entries(entries: list[tuple[str, str, str]], stamp: datetime) -> None:
    path = ROOT / "feed.xml"
    tree = etree.parse(str(path))
    channel = tree.getroot().find("channel")
    assert channel is not None
    full_urls = {f"https://curiomondo.it{url}" for _, url, _ in entries}
    for item in list(channel.findall("item")):
        if item.findtext("link") in full_urls:
            channel.remove(item)
    insert_at = next((i for i, child in enumerate(channel) if child.tag == "item"), len(channel))
    for title, url, description in entries:
        node = etree.Element("item")
        full = f"https://curiomondo.it{url}"
        for tag, value in (("title", title), ("link", full), ("guid", full), ("pubDate", format_datetime(stamp)), ("description", description)):
            child = etree.SubElement(node, tag)
            child.text = value
        channel.insert(insert_at, node)
        insert_at += 1
    tree.write(str(path), encoding="utf-8", xml_declaration=True, pretty_print=True)


def main() -> None:
    now = datetime.now(ZoneInfo("Europe/Rome"))
    if now.date().isoformat() != DATE:
        raise SystemExit("Data Europe/Rome diversa da quella del pacchetto")
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    daily = manifest["daily_state"]
    if daily.get("last_question_date", "") >= DATE:
        print(json.dumps({"status": "noop", "date": DATE}, ensure_ascii=False))
        return

    queue_path = ROOT / "automation/state/daily-questions.json"
    questions = json.loads(queue_path.read_text(encoding="utf-8"))
    row = next(item for item in questions if item.get("number") == NUMBER)
    row["question"] = QUESTION
    row["source_verification"] = {
        "document": "Mille_e_piu_domande_per_pensare.pdf",
        "number": NUMBER,
        "page": 45,
        "verified_on": DATE,
        "question_sha256": QUESTION_SHA256,
    }
    if hashlib.sha256(row["question"].encode("utf-8")).hexdigest() != QUESTION_SHA256:
        raise SystemExit("Impronta della domanda non coerente con la verifica PDF")
    dump(queue_path, questions)
    chosen = choose_question(manifest)
    if chosen["number"] != NUMBER or chosen["question"] != QUESTION:
        raise SystemExit("La domanda selezionata non coincide con la voce PDF verificata")

    answer_chars = len(" ".join(PACKAGE["answer_paragraphs"]))
    if not 1000 <= answer_chars <= 3000:
        raise SystemExit(f"Risposta fuori standard: {answer_chars}")
    guide_lengths = {g["slug"]: len(" ".join(p for _, ps in g["sections"] for p in ps)) for g in GUIDES}
    if any(not 3000 <= n <= 15000 for n in guide_lengths.values()):
        raise SystemExit(f"Guide fuori standard: {guide_lengths}")

    book_path = ROOT / BOOK_URL.strip("/") / "index.html"
    book_text = book_path.read_text(encoding="utf-8")
    book = html.fromstring(book_text)
    stage = book.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " cm-book-stage ")]')[0]
    book_words = len(re.findall(r"\S+", " ".join(stage.xpath(".//p//text()"))))
    book_chapters = len(book.xpath('//*[@data-book-page]'))
    if not 22000 <= book_words <= 32000 or not 8 <= book_chapters <= 12:
        raise SystemExit(f"eBook collegato fuori standard: {book_words} parole, {book_chapters} capitoli")

    state_versions = [int(manifest.get("site_version", 0)), int(manifest["site"].get("current_site_version", 0))]
    for p in (ROOT / "assets/data/search-index-v210.json", ROOT / "RELEASE-STATE.json", ROOT / "CURIOMONDO-RELEASE-STATE.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        state_versions.extend(int(data.get(k, 0)) for k in ("version", "site_version", "currentVersion") if str(data.get(k, "")).isdigit())
    version = max(state_versions) + 1
    shared.VERSION = version
    shared.DATE = DATE
    shared.DATE_LABEL = DATE_LABEL

    page = render_question_page(QUESTION, PACKAGE, SLUG, DATE, DATE_LABEL, BOOK_URL)
    page = page.replace("biblioteca-v1.css?v=346", "biblioteca-v1.css?v=526")
    page = page.replace("<small>Continua la riflessione</small>", "<small>eBook su identità, lavoro e riconoscimento</small>")
    page = page.replace("<strong>Leggi l'eBook collegato</strong>", f"<strong>{escape(BOOK_TITLE)}</strong>")
    stamp = now.isoformat(timespec="seconds")
    schema = {"@context": "https://schema.org", "@type": "Article", "headline": QUESTION, "description": PACKAGE["excerpt"], "mainEntityOfPage": "https://curiomondo.it" + QURL, "datePublished": stamp, "dateModified": stamp, "author": {"@type": "Organization", "name": "CurioMondo"}, "publisher": {"@type": "Organization", "name": "CurioMondo"}, "inLanguage": "it-IT", "relatedLink": "https://curiomondo.it" + BOOK_URL}
    meta = '<meta property="og:type" content="article"><meta property="og:title" content="' + escape(QUESTION, quote=True) + '"><meta property="og:description" content="' + escape(PACKAGE["excerpt"], quote=True) + '"><meta property="og:url" content="https://curiomondo.it' + QURL + '"><script type="application/ld+json">' + json.dumps(schema, ensure_ascii=False) + '</script><script defer src="/assets/js/ga4-v714.js"></script>'
    page = page.replace("</head>", meta + "</head>")
    write(ROOT / QURL.strip("/") / "index.html", page)
    update_home(SLUG, now, DATE_LABEL)

    question_card = f'<a class="cb-subcard" href="{QURL}"><span class="cb-kicker">{DATE_LABEL} · Domanda del giorno</span><h2>{escape(QUESTION)}</h2><p>{escape(PACKAGE["excerpt"])}</p><b>Leggi →</b></a>'
    for path, cls in (("domanda-del-giorno/index.html", "cb-qday-grid"), ("biblioteca/index.html", "cb-qday-grid"), ("biblioteca/vita-relazioni/domande-per-conoscersi/index.html", "cb-subgrid")):
        shared.prepend_card(ROOT / path, cls, question_card, QURL)

    backlink = f'<a class="cm-book-back" href="{QURL}">Domanda del {DATE_LABEL}: {escape(QUESTION)}</a>'
    if QURL not in book_text:
        book_text = book_text.replace("</article></main>", backlink + "</article></main>", 1)
        write(book_path, book_text)

    guide_root = ROOT / "biblioteca/tecnologia-ai/smartphone-computer"
    write(guide_root / "index.html", guide_index())
    for guide in GUIDES:
        write(guide_root / guide["slug"] / "index.html", guide_html(guide))

    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text(encoding="utf-8"))
    items = search.get("items", [])
    urls = {QURL, *[f'/biblioteca/tecnologia-ai/smartphone-computer/{g["slug"]}/' for g in GUIDES]}
    items = [item for item in items if item.get("url") not in urls]
    additions = [{"title": QUESTION, "excerpt": PACKAGE["excerpt"], "url": QURL, "section": "Domanda del giorno"}]
    additions.extend({"title": g["title"], "excerpt": g["deck"], "url": f'/biblioteca/tecnologia-ai/smartphone-computer/{g["slug"]}/', "section": "Biblioteca / Tecnologia e informatica"} for g in GUIDES)
    search["items"] = additions + items
    search["version"] = version
    dump(search_path, search)

    update_sitemap(DATE, QURL, BOOK_URL)
    shared.add_sitemap_url("/biblioteca/tecnologia-ai/smartphone-computer/")
    for guide in GUIDES:
        shared.add_sitemap_url(f'/biblioteca/tecnologia-ai/smartphone-computer/{guide["slug"]}/')
    update_feed(now, QUESTION, PACKAGE, QURL)
    add_feed_entries([(g["title"], f'/biblioteca/tecnologia-ai/smartphone-computer/{g["slug"]}/', g["deck"]) for g in GUIDES], now)

    guide_queue_path = ROOT / "automation/state/guide-topics.json"
    guide_queue = json.loads(guide_queue_path.read_text(encoding="utf-8"))
    technology = next(c for c in guide_queue["categories"] if c["category"] == "Tecnologia e informatica")
    for guide in GUIDES:
        if guide["topic"] not in technology["remaining_topics"]:
            raise SystemExit(f"Tema guida non disponibile: {guide['topic']}")
        technology["remaining_topics"].remove(guide["topic"])
        technology["published_from_queue"].append(guide["topic"])
    guide_queue["version"] = int(guide_queue.get("version", 0)) + 1
    dump(guide_queue_path, guide_queue)

    manifest["site"].update({"current_site_version": version, "site_version": version})
    manifest.update({"site_version": version, "version": f"v{version}", "release_version": f"v{version}"})
    daily.setdefault("used_question_source_numbers", []).append(NUMBER)
    daily.update({"current_question_source_number": NUMBER, "last_question_date": DATE, "last_question_slug": SLUG, "last_question_ebook_url": BOOK_URL, "last_daily_package_date": DATE, "last_daily_guides": [g["slug"] for g in GUIDES], "current_question_source_verification": chosen["source_verification"], "question_queue_rule": "La coda è una cache: ogni voce deve essere verificata sul PDF privato originale prima della pubblicazione."})
    manifest["last_release"] = {"version": version, "date": DATE, "type": "daily-editorial-package", "daily_question_added": SLUG, "ebook_linked": BOOK_URL, "ebook_created": False, "guides_added": [g["slug"] for g in GUIDES], "news_added": [], "news_updated": [], "change": "Domanda n. 1017 verificata sul PDF originale, eBook conforme collegato e due guide Biblioteca pubblicate dalla coda canonica."}
    dump(manifest_path, manifest)

    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({"currentVersion": version, "site_version": version, "version": str(version), "date": DATE, "release_date": DATE, "last_daily_question_date": DATE, "last_update": f"daily-package-v{version}"})
        dump(path, state)

    write(ROOT / f"RELEASE-NOTES-v{version}.md", f'''# CurioMondo v{version} — {DATE_LABEL}\n\n- Pubblicata la Domanda del giorno n. {NUMBER}, verificata sul PDF privato originale: “{QUESTION}”.\n- Corretta la voce n. {NUMBER} nella cache e registrata la verifica di pagina 45 con SHA-256 UTF-8.\n- Collegato l’eBook esistente “{BOOK_TITLE}” ({book_chapters} capitoli, {book_words} parole), con collegamento reciproco.\n- Pubblicate due guide dalla coda canonica: reset sicuro del telefono e trasferimento dati Android/iPhone.\n- Aggiornati homepage, archivi, Biblioteca, ricerca, feed, sitemap, manifest e stati di rilascio.\n- Nessuna notizia o automazione modificata.\n''')
    print(json.dumps({"status": "prepared", "version": version, "date": DATE, "question_number": NUMBER, "answer_characters": answer_chars, "linked_book_words": book_words, "linked_book_chapters": book_chapters, "guide_characters": guide_lengths}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
