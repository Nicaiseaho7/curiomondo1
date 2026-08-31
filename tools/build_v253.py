#!/usr/bin/env python3
"""Publish the Cyprus and Libya stories, update Nepal-Tibet, and prepare CurioMondo v253."""
from __future__ import annotations

from datetime import datetime
from email.utils import format_datetime
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re

from PIL import Image
from lxml import etree, html


ROOT = Path(__file__).resolve().parents[1]
VERSION = 253
DATE_LABEL = "2026-08-30"
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
IMAGE_DIR = "/assets/images/editorial-v253"
GENERATED = ROOT.parent / "generated-v253"

CYPRUS = {
    "slug": "cipro-naufragio-traghetto-filojet-morti-dispersi-30-agosto-2026",
    "title": "FILOJET capovolto al largo di Cipro: 7 morti, 23 dispersi e 237 persone salvate",
    "excerpt": "Il nuovo bilancio del naufragio conta 7 vittime e 23 persone ancora disperse. I soccorritori hanno recuperato vive 237 persone sulle 267 registrate a bordo.",
    "category": "Ultima ora · Mondo / Cipro / Cronaca",
    "published": "2026-08-30T16:05:00+02:00",
    "updated": "2026-08-30T16:05:00+02:00",
    "image_key": "cipro-filojet-naufragio-30-agosto-2026-ai-v253",
    "source_image": GENERATED / "cipro-filojet-naufragio-editorial.png",
    "image_alt": "Illustrazione editoriale IA del traghetto FILOJET capovolto al largo di Cipro con mezzi di soccorso in avvicinamento, senza persone o vittime visibili",
    "sensitive": True,
    "prompt": "Use case: photorealistic-natural. Respectful ultra-realistic aerial editorial illustration of a capsized passenger ferry off Cyprus, distant rescue vessels and calm Mediterranean sea, no people in the water, no bodies, no trauma, no readable vessel name, no text, no watermark, no documentary claim.",
    "insights": [("7", "le vittime confermate"), ("23", "le persone ancora disperse"), ("237", "le persone recuperate vive")],
    "body": [
        "Il bilancio del naufragio del FILOJET al largo della parte settentrionale di Cipro è salito ad almeno 7 morti, mentre 23 persone risultano ancora disperse. Secondo l’ultimo conteggio riferito da Reuters, 237 persone sono state recuperate vive. I registri di bordo indicavano 259 passeggeri e otto membri dell’equipaggio: 267 persone in tutto.",
        "Il traghetto era partito da Kyrenia, chiamata Girne dalle autorità turco-cipriote, ed era diretto verso la costa meridionale della Turchia. Le prime informazioni collocano il capovolgimento a poche miglia nautiche dalla partenza. Le autorità non hanno ancora comunicato una causa definitiva: finché non saranno esaminati scafo, dati di navigazione, condizioni del carico e testimonianze, sarebbe scorretto attribuire il disastro a un singolo fattore.",
        "Il conto più recente è internamente coerente: 237 sopravvissuti, 23 dispersi e 7 vittime corrispondono alle 267 persone registrate a bordo. Associated Press, in un aggiornamento precedente, aveva indicato 24 dispersi; in operazioni ancora aperte una persona può essere riclassificata quando gli elenchi dei passeggeri vengono confrontati con ospedali, centri di accoglienza e squadre di soccorso. CurioMondo adotta quindi il dato Reuters più recente, specificandone l’orario editoriale.",
        "Le ricerche proseguono in mare e all’interno dell’imbarcazione. Quando un traghetto si capovolge, alcuni ambienti possono conservare sacche d’aria ma diventano difficili da raggiungere: porte, corridoi e scale cambiano orientamento, mentre carburante, detriti e instabilità dello scafo aumentano il rischio per i sommozzatori. Per questo la verifica di eventuali persone intrappolate richiede squadre specializzate e non può essere sostituita da una semplice ricognizione in superficie.",
        "Alla risposta partecipano mezzi navali, elicotteri e unità costiere dell’area. La posizione politica dell’isola rende necessario distinguere la geografia dal riconoscimento internazionale: Kyrenia si trova nella parte settentrionale controllata dai turco-ciprioti, riconosciuta come Stato soltanto dalla Turchia, mentre la Repubblica di Cipro è riconosciuta internazionalmente e controlla il sud. Questa distinzione non modifica il dato umano, ma aiuta a capire perché i comunicati possano arrivare da autorità differenti.",
        "Il termine “salvate” indica che le persone sono state recuperate vive, non necessariamente che tutte siano già state dimesse o identificate definitivamente. Alcune possono essere state trasportate in strutture sanitarie o registrate inizialmente senza documenti. Il passaggio decisivo sarà la riconciliazione nominativa: ogni nome nell’elenco d’imbarco dovrà corrispondere a una persona localizzata, a un ricovero, a una vittima identificata o a una segnalazione ancora aperta.",
        "Le prossime informazioni utili riguarderanno l’esito delle ispezioni nello scafo, l’identificazione delle vittime e l’apertura dell’indagine tecnica. Il bilancio può ancora cambiare, ma l’aumento a 7 morti e la definizione di 23 dispersi rendono questo aggiornamento sostanziale. CurioMondo manterrà questa pagina come riferimento unico, evitando di separare i conteggi precedenti in articoli duplicati.",
    ],
    "related": [
        ("/notizie/nepal-tibet-alluvioni-oltre-350-morti-1300-dispersi-27-agosto-2026.html", "Mondo · Asia / Ambiente", "Nepal–Tibet, una nuova frana costringe i soccorritori a evacuare"),
        ("/notizie/terremoto-indonesia-100-morti-180000-evacuati-24-agosto-2026.html", "Mondo · Asia", "Indonesia, terremoto e maxi evacuazioni: il quadro dell’emergenza"),
        ("/notizie/come-funzionano-piene-laghi-glaciali-glof-himalaya.html", "Approfondimento · Rischi naturali", "Come le dighe naturali possono generare piene improvvise"),
    ],
    "sources": [
        ("https://www.reuters.com/world/europe/boat-with-around-270-people-capsizes-off-north-cyprus-media-says-2026-08-30/", "Reuters — ultimo bilancio, persone a bordo e operazioni di soccorso"),
        ("https://apnews.com/article/e7753be49f345d1b1f1579013b241e9e", "Associated Press — bilancio, rotta del traghetto e precedente conteggio dei dispersi"),
    ],
}

LIBYA = {
    "slug": "libia-accordo-fazioni-elezioni-entro-24-mesi-30-agosto-2026",
    "title": "Libia, le istituzioni rivali firmano una road map: elezioni nazionali entro 24 mesi",
    "excerpt": "L’intesa raggiunta nei colloqui guidati dall’ONU prevede elezioni presidenziali e legislative, un’autorità esecutiva unica e istituzioni nazionali unificate.",
    "category": "Mondo · Africa / Libia / Politica",
    "published": "2026-08-30T15:55:00+02:00",
    "updated": "2026-08-30T15:55:00+02:00",
    "image_key": "libia-accordo-elezioni-30-agosto-2026-ai-v253",
    "source_image": GENERATED / "libia-accordo-elezioni-editorial.png",
    "image_alt": "Illustrazione editoriale IA di una sala di colloqui a Tripoli con bandiere libiche e la città sullo sfondo, senza rappresentare una firma documentaria",
    "sensitive": False,
    "prompt": "Use case: photorealistic-natural. Sober ultra-realistic editorial illustration of a political negotiation room in Tripoli with Libyan flags and skyline, no named public figures, no handshake, no signing, no readable documents, no UN logo, no text, no watermark, no documentary claim.",
    "insights": [("24 mesi", "il limite indicato per le elezioni"), ("2", "le consultazioni previste: presidenziali e legislative"), ("1 mese", "il tempo indicato per il quadro operativo")],
    "body": [
        "I rappresentanti delle principali istituzioni politiche rivali della Libia hanno firmato a Tripoli una road map che punta a elezioni nazionali entro un massimo di 24 mesi. L’intesa è maturata nei colloqui guidati dalle Nazioni Unite e comprende sia il voto presidenziale sia quello legislativo. È un impegno politico formale, non ancora la convocazione delle urne.",
        "Al tavolo hanno partecipato esponenti del Governo di unità nazionale, dell’Alto Consiglio di Stato, della Camera dei rappresentanti e dell’Esercito nazionale libico. Il testo indica come obiettivi un’unica autorità esecutiva e istituzioni nazionali unificate. Entro un mese dovrebbe essere definito il quadro operativo: calendario, passaggi legislativi, responsabilità e meccanismi necessari a trasformare la dichiarazione in atti verificabili.",
        "La distinzione è importante. Una road map stabilisce una direzione e delle scadenze, ma non risolve automaticamente i conflitti sulle regole elettorali, sui requisiti dei candidati o sulla sicurezza dei seggi. Reuters sottolinea che saranno necessari interventi sulla legge elettorale e sugli organismi incaricati del voto. Senza questi passaggi, la finestra dei 24 mesi resterebbe un obiettivo politico privo di un percorso esecutivo completo.",
        "Il precedente del dicembre 2021 spiega la cautela. Quelle elezioni, presentate come il passaggio capace di riunificare il Paese, furono rinviate all’ultimo momento per dispute sulle regole e sull’ammissibilità di candidati controversi. Non esisteva un accordo condiviso su chi potesse concorrere, su quale istituzione avesse l’ultima parola e su come gestire eventuali contestazioni. Il voto non venne semplicemente posticipato di qualche settimana: il processo si bloccò.",
        "Da allora la Libia è rimasta divisa fra strutture con basi territoriali e militari differenti. A Tripoli opera il Governo di unità nazionale; nell’est la Camera dei rappresentanti è sostenuta dal campo legato a Khalifa Haftar e all’Esercito nazionale libico. Anche petrolio, bilancio pubblico, milizie e controllo delle istituzioni economiche entrano nella trattativa, perché un’elezione credibile richiede che chi perde riconosca il risultato e rinunci a usare la forza per modificarlo.",
        "L’intesa del 30 agosto è quindi rilevante perché riunisce attori che raramente condividono lo stesso percorso e fissa una scadenza misurabile. Non garantisce però che la Libia avrà davvero un governo unico entro due anni. I segnali da osservare sono concreti: approvazione delle norme, accordo sull’esecutivo transitorio, indipendenza della commissione elettorale, sicurezza nazionale e accesso uniforme al voto.",
        "Per ricostruire le origini della divisione, il ruolo delle istituzioni dell’est e dell’ovest e le ragioni del fallimento del 2021, CurioMondo ha preparato l’approfondimento <a href=\"/notizie/perche-libia-divisa-chi-governa-elezioni-2021-fallite.html\">Perché la Libia è ancora divisa e che cosa bloccò le elezioni del 2021</a>. La nuova road map va letta dentro quella storia: è un tentativo di spezzare lo stallo, non la sua conclusione.",
    ],
    "related": [
        ("/notizie/perche-libia-divisa-chi-governa-elezioni-2021-fallite.html", "Approfondimento · Libia", "Perché la Libia è ancora divisa e che cosa bloccò il voto del 2021"),
        ("/notizie/niger-attacco-aeroporto-presidenza-niamey-29-agosto-2026.html", "Mondo · Africa / Sicurezza", "Niger, attacco all’aeroporto e alla presidenza di Niamey"),
        ("/notizie/come-funzionano-trasferimenti-richiedenti-asilo-europa.html", "Approfondimento · Migrazioni", "Come funzionano i trasferimenti dei richiedenti asilo in Europa"),
    ],
    "sources": [
        ("https://www.reuters.com/world/africa/libya-rivals-agree-roadmap-elections-within-24-months-un-led-talks-2026-08-30/", "Reuters — accordo di Tripoli, soggetti coinvolti e scadenza dei 24 mesi"),
        ("https://www.reuters.com/world/middle-east/libyan-leaders-agree-form-new-unified-government-2024-03-10/", "Reuters — precedente processo per un governo unificato e fallimento del voto del 2021"),
        ("https://www.reuters.com/world/libyan-rivals-agree-work-with-un-end-political-deadlock-2024-12-19/", "Reuters — istituzioni rivali e precedenti tentativi ONU contro lo stallo politico"),
    ],
}

NEPAL = {
    "slug": "nepal-tibet-alluvioni-oltre-350-morti-1300-dispersi-27-agosto-2026",
    "title": "Nepal–Tibet, una nuova frana ferma i soccorritori: oltre 800 morti e 3.000 dispersi",
    "excerpt": "Una nuova frana vicino al lago-barriera ha costretto le squadre a ripiegare. In Nepal cresce il Bhotekoshi mentre il bilancio supera 800 morti e 3.000 dispersi.",
    "category": "Ultima ora · Mondo / Asia / Ambiente",
    "published": "2026-08-27T16:55:00+02:00",
    "updated": "2026-08-30T15:40:00+02:00",
    "image_key": "nepal-tibet-nuova-frana-30-agosto-2026-ai-v253",
    "source_image": GENERATED / "nepal-tibet-nuova-frana-editorial.png",
    "image_alt": "Illustrazione editoriale IA di una nuova frana in una valle tra Nepal e Tibet, con lago-barriera e soccorritori già in posizione sicura",
    "sensitive": True,
    "prompt": "Use case: photorealistic-natural. Respectful ultra-realistic Himalayan valley after a new landslide, barrier lake and muddy river, tiny rescue teams already on safe high ground, no victims, no bodies, no active impact, no text, no watermark, no documentary claim.",
    "insights": [("800+", "le vittime indicate nel quadro AP"), ("3.000+", "le persone ancora disperse"), ("2,8 km", "la distanza della nuova frana dal lago-barriera")],
    "body": [
        "Una nuova frana in Tibet ha costretto le autorità a evacuare anche i soccorritori impegnati nell’area della catastrofe tra Nepal e Cina. Il distacco è stato rilevato circa 2,8 chilometri a valle del lago-barriera formatosi dopo il primo evento. Le squadre vicine al valico di Gyirong sono state spostate verso terreno più alto e stabile, perché un secondo cedimento potrebbe alterare improvvisamente il corso dell’acqua e dei detriti.",
        "Un lago-barriera nasce quando una frana o una massa di ghiaccio blocca una valle e trattiene il fiume. Non è una diga progettata: rocce, fango e tronchi non hanno sfioratori né strutture capaci di regolare la pressione. Se il livello sale, l’acqua può erodere il materiale, aprire un varco e produrre una nuova piena a valle. L’evacuazione dei soccorritori è quindi una misura preventiva legata a un rischio reale, non l’annuncio che un secondo collasso sia già avvenuto.",
        "Sul versante nepalese sono stati diramati nuovi avvisi mentre cresce il livello del Bhotekoshi, uno dei corsi d’acqua che attraversano le valli colpite. Pioggia, sedimenti e sbarramenti naturali rendono difficile prevedere dove si concentrerà l’onda di piena. Le comunità a valle devono ricevere avvisi rapidi, ma le comunicazioni restano danneggiate e numerose strade sono ancora interrotte.",
        "Associated Press indica ora almeno 800 morti e oltre 3.000 dispersi tra Nepal e Tibet. Il totale supera il precedente bilancio di 750 vittime perché le squadre hanno raggiunto nuove aree e i registri dei due Paesi continuano a essere riconciliati. In una crisi transfrontaliera, la cifra può cambiare quando persone isolate vengono localizzate, nuovi corpi sono identificati o segnalazioni riferite alla stessa persona vengono eliminate.",
        "Reuters descrive intanto un’operazione sempre più specializzata per raggiungere centinaia di persone che potrebbero essere rimaste nei tunnel degli impianti idroelettrici. Entrare in spazi sotterranei allagati richiede verifiche su ventilazione, stabilità, pressione dell’acqua e accessi alternativi. L’instabilità della valle impone inoltre di fermare le ricerche ogni volta che sensori, droni o osservatori rilevano nuovi movimenti del terreno.",
        "La priorità immediata non è soltanto trovare i dispersi, ma evitare che le squadre di soccorso diventino a loro volta vittime. Per questo autorità nepalesi e cinesi stanno combinando immagini satellitari, monitoraggio dei fiumi e controlli sul campo. Il meteo può ridurre la visibilità dei droni e accelerare l’erosione delle dighe naturali, mentre ogni nuova frana modifica le mappe di accesso preparate poche ore prima.",
        "Per capire il meccanismo fisico dietro queste piene, si può leggere l’approfondimento CurioMondo <a href=\"/notizie/come-funzionano-piene-laghi-glaciali-glof-himalaya.html\">Che cosa sono le piene dei laghi glaciali e perché possono travolgere intere valli?</a>. Il caso attuale combina più rischi: ghiaccio instabile, frane, laghi temporanei, fiumi molto ripidi e infrastrutture costruite in corridoi stretti.",
        "Le prossime verifiche dovranno chiarire se la nuova frana continua a muoversi, quanto rapidamente cresce il Bhotekoshi e quando le squadre potranno rientrare in sicurezza. CurioMondo aggiorna questa stessa pagina perché si tratta dello sviluppo della medesima catastrofe: il nuovo pericolo modifica le operazioni, ma non giustifica un articolo duplicato.",
    ],
    "related": [
        ("/notizie/come-funzionano-piene-laghi-glaciali-glof-himalaya.html", "Approfondimento · Clima", "Come funzionano le piene da laghi glaciali e perché l’Himalaya è vulnerabile"),
        ("/notizie/nepal-alluvione-ricostruzione-5-miliardi-29-agosto-2026.html", "Mondo · Economia", "Nepal, ricostruzione fino a 5 miliardi dopo la catastrofe"),
        ("/notizie/cipro-naufragio-traghetto-filojet-morti-dispersi-30-agosto-2026.html", "Mondo · Cipro / Cronaca", "Cipro, naufragio del FILOJET: 7 morti e 23 dispersi"),
    ],
    "sources": [
        ("https://apnews.com/article/ad4f11f22f7e8e80e17d7557c396e966", "Associated Press — nuovo bilancio, frane e allerta per ulteriori inondazioni"),
        ("https://www.reuters.com/world/china/nepal-steps-up-rescue-effort-reach-hundreds-trapped-tunnels-2026-08-30/", "Reuters — operazioni nei tunnel, dispersi e difficoltà dei soccorsi"),
        ("https://www.reuters.com/world/china/china-identifies-countries-261-foreigners-missing-himalayan-mudslide-2026-08-30/", "Reuters — precedente bilancio coordinato e nuova diga naturale")
    ],
}

EVERGREEN = {
    "slug": "perche-libia-divisa-chi-governa-elezioni-2021-fallite",
    "title": "Perché la Libia è ancora divisa e che cosa bloccò le elezioni del 2021",
    "excerpt": "Dalla caduta di Gheddafi alle istituzioni rivali dell’est e dell’ovest: una guida per capire chi governa, il ruolo delle forze armate e perché il voto del 2021 fallì.",
    "category": "Approfondimento · Geopolitica / Libia",
    "published": "2026-08-30T15:50:00+02:00",
    "updated": "2026-08-30T15:50:00+02:00",
    "body": [
        "Per capire perché ogni accordo elettorale libico viene accolto insieme con speranza e prudenza bisogna partire dal 2011. La caduta di Muammar Gheddafi eliminò il centro autoritario che aveva controllato il Paese per decenni, ma non produsse istituzioni nazionali abbastanza forti da integrare le molte forze armate nate durante la rivolta. Milizie locali, città e coalizioni politiche conservarono armi, territori e capacità di veto.",
        "Nel 2014 la crisi si trasformò in una divisione stabile. A ovest si consolidarono autorità con base a Tripoli; a est la Camera dei rappresentanti si stabilì nell’area di Bengasi e Tobruk, sostenuta dal campo militare di Khalifa Haftar e dall’Esercito nazionale libico. Le etichette “est” e “ovest” semplificano una realtà più frammentata, perché dentro ciascun campo esistono città, milizie e interessi non sempre allineati.",
        "Oggi a Tripoli opera il Governo di unità nazionale, nato da un processo sostenuto dalle Nazioni Unite. La Camera dei rappresentanti continua però a rivendicare legittimità nell’est e ha appoggiato strutture esecutive alternative. L’Alto Consiglio di Stato, con base occidentale, partecipa ai negoziati sulle leggi e sulle nomine. Nessuno di questi organi controlla da solo tutto il territorio, tutte le forze armate e tutte le entrate pubbliche.",
        "Il petrolio rende la divisione più delicata. I giacimenti, i terminali e la Banca centrale collegano zone controllate da attori diversi; bloccare produzione o esportazioni può diventare uno strumento di pressione. Anche se la National Oil Corporation e altre istituzioni economiche cercano di mantenere un carattere nazionale, le dispute su bilancio e distribuzione delle entrate influenzano ogni accordo politico.",
        "Le elezioni del dicembre 2021 avrebbero dovuto creare una presidenza e un Parlamento riconosciuti in tutto il Paese. Il voto fallì perché le regole non erano state concordate in modo definitivo. Restavano contestati i requisiti dei candidati, la possibilità per figure militari o titolari di cariche pubbliche di concorrere, i poteri della futura presidenza e l’autorità competente a decidere sui ricorsi.",
        "Il problema non era soltanto giuridico. Alcuni candidati rappresentavano centri di potere capaci di contestare un risultato sfavorevole, mentre mancavano garanzie condivise sulla sicurezza dei seggi e sul trasferimento pacifico dell’autorità. Senza una catena di comando unificata e senza una corte o commissione accettata da tutti, anche una regola scritta poteva essere interpretata in modi opposti.",
        "Per questo l’espressione “un’unica autorità esecutiva” è centrale negli accordi più recenti. Significa tentare di sostituire governi concorrenti con un esecutivo incaricato di portare il Paese al voto, amministrare il bilancio e coordinare le istituzioni. Ma la formula funziona soltanto se vengono definiti mandato, durata, meccanismo di nomina e limiti: altrimenti la fase transitoria può diventare un nuovo terreno di scontro.",
        "La road map firmata il 30 agosto 2026 prova a trasformare questi nodi in un calendario di 24 mesi. L’articolo collegato <a href=\"/notizie/libia-accordo-fazioni-elezioni-entro-24-mesi-30-agosto-2026.html\">Libia, le istituzioni rivali firmano una road map</a> segue l’attuazione dell’intesa. I segnali decisivi saranno una legge elettorale condivisa, una commissione indipendente, accordi di sicurezza e l’impegno verificabile dei principali attori a riconoscere il risultato.",
    ],
    "sources": [
        ("https://www.reuters.com/world/africa/how-libya-reached-its-dangerous-political-impasse-2023-08-15/", "Reuters — origine della divisione politica e istituzionale dal 2014"),
        ("https://www.reuters.com/world/middle-east/libyan-leaders-agree-form-new-unified-government-2024-03-10/", "Reuters — istituzioni rivali e fallimento delle elezioni del 2021"),
        ("https://www.reuters.com/world/libyan-rivals-agree-work-with-un-end-political-deadlock-2024-12-19/", "Reuters — struttura del negoziato ONU e persistenza dello stallo")
    ],
}


def url(story: dict) -> str:
    return f"/notizie/{story['slug']}.html"


def canonical(story: dict) -> str:
    return f"https://curiomondo.it{url(story)}"


def write(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def dump(path: Path, value: object, compact: bool = False) -> None:
    text = json.dumps(value, ensure_ascii=False, indent=None if compact else 2,
                      separators=(",", ":") if compact else None)
    write(path, text + ("" if compact else "\n"))


def make_images(stories: list[dict]) -> dict[str, list[dict]]:
    target_dir = ROOT / IMAGE_DIR.lstrip("/")
    target_dir.mkdir(parents=True, exist_ok=True)
    result: dict[str, list[dict]] = {}
    for story in stories:
        source_path = story["source_image"]
        if not source_path.exists():
            raise SystemExit(f"Missing generated image: {source_path}")
        variants = []
        with Image.open(source_path) as image:
            source = image.convert("RGB")
            for width in (480, 800, 1200):
                height = round(width * 2 / 3)
                target = target_dir / f"{story['image_key']}-{width}.webp"
                source.resize((width, height), Image.Resampling.LANCZOS).save(target, "WEBP", quality=88, method=6)
                variants.append({"w": width, "src": f"{IMAGE_DIR}/{story['image_key']}-{width}.webp",
                                 "sha256": sha256(target.read_bytes()).hexdigest(), "bytes": target.stat().st_size})
        result[story["slug"]] = variants
    return result


def feed_entry(story: dict) -> dict:
    return {
        "title": story["title"], "excerpt": story["excerpt"], "url": url(story), "section": story["category"],
        "dateISO": story["updated"], "dateLabel": DATE_LABEL,
        "image": f"{IMAGE_DIR}/{story['image_key']}-800.webp", "imageAlt": story["image_alt"],
        "imageWidth": 800, "imageHeight": 533,
        "srcset": ", ".join(f"{IMAGE_DIR}/{story['image_key']}-{w}.webp {w}w" for w in (480, 800, 1200)),
    }


def article_html(story: dict, *, published_label: str = "30 agosto 2026") -> str:
    story_url = url(story)
    story_canonical = canonical(story)
    schema = {
        "@context": "https://schema.org", "@type": "NewsArticle", "headline": story["title"],
        "description": story["excerpt"], "datePublished": story["published"], "dateModified": story["updated"],
        "mainEntityOfPage": story_canonical, "inLanguage": "it-IT",
        "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo", "logo": {"@type": "ImageObject", "url": "https://curiomondo.it/curiomondo-logo-512.png"}},
        "image": [f"https://curiomondo.it{IMAGE_DIR}/{story['image_key']}-1200.webp"],
        "creditText": "Illustrazione editoriale CurioMondo generata con IA; non fotografia documentaria.",
    }
    body = "".join(f"<p>{p}</p>" for p in story["body"])
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>' for u, label in story["sources"])
    related = "".join(f'<a href="{u}"><small>{escape(section)}</small><strong>{escape(title)}</strong></a>' for u, section, title in story["related"])
    insights = "".join(f"<div><b>{escape(a)}</b><small>{escape(b)}</small></div>" for a, b in story["insights"])
    modified_dt = datetime.fromisoformat(story["updated"])
    time_label = modified_dt.strftime("%H:%M")
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(story['title'])} | CurioMondo</title><meta name="description" content="{escape(story['excerpt'], quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{story_canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(story['title'], quote=True)}"><meta property="og:description" content="{escape(story['excerpt'], quote=True)}"><meta property="og:url" content="{story_canonical}"><meta property="og:image" content="https://curiomondo.it{IMAGE_DIR}/{story['image_key']}-1200.webp"><meta property="og:image:alt" content="{escape(story['image_alt'], quote=True)}"><meta name="theme-color" content="#071a33"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=253"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script><script type="text/plain" data-cookiecategory="marketing" async crossorigin="anonymous" src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-8050187517048759"></script></head><body data-article-id="{story['slug']}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="topbar"><div class="inner"><a class="btn-back" href="../index.html">← Indietro</a><a class="logo" href="../index.html"><img class="cm-brand-logo" src="../curiomondo-logo-96.webp" width="36" height="36" alt=""><span class="cm-wordmark">Curio<span>Mondo</span></span></a><button class="article-theme-toggle" data-theme-toggle type="button" aria-label="Cambia tema">☾</button></div></header><main class="wrap"><div class="badge">{escape(story['category'])}</div><h1>{escape(story['title'])}</h1><p class="subtitle">{escape(story['excerpt'])}</p><div class="meta">{published_label} · aggiornato alle {time_label} · {escape(story['category'].replace('Ultima ora · ', ''))} · <span id="readTime">4 min di lettura</span></div><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><figure class="article-image" data-ai-generated="true" data-sensitive-context="{'true' if story['sensitive'] else 'false'}"><picture><img src="../assets/images/editorial-v253/{story['image_key']}-800.webp" srcset="../assets/images/editorial-v253/{story['image_key']}-480.webp 480w, ../assets/images/editorial-v253/{story['image_key']}-800.webp 800w, ../assets/images/editorial-v253/{story['image_key']}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(story['image_alt'], quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><div class="editorial-data"><div><strong>Keyword principale:</strong> {escape(story['title'])}</div><div><strong>URL SEO:</strong> {story_url}</div></div><section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid">{insights}</div></section><article class="art-body" data-length-policy="2000-4500">{body}</article>{'<section aria-labelledby="cm-evergreen-question" class="cm-evergreen-reader"><small>Approfondimento collegato</small><h2 id="cm-evergreen-question">Perché la Libia è ancora divisa e che cosa bloccò le elezioni del 2021?</h2><a href="/notizie/perche-libia-divisa-chi-governa-elezioni-2021-fallite.html">Leggi l’approfondimento →</a></section>' if story is LIBYA else ''}<section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 30 agosto 2026, ore {time_label} italiane.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a><button class="cm-cookie-manage" type="button">Gestisci cookie</button></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=253" defer></script></body></html>'''


def evergreen_html() -> str:
    e = EVERGREEN
    c = canonical(e)
    schema = {
        "@context": "https://schema.org", "@type": "Article", "headline": e["title"], "description": e["excerpt"],
        "datePublished": e["published"], "dateModified": e["updated"], "mainEntityOfPage": c, "inLanguage": "it-IT",
        "author": {"@type": "Organization", "name": "Redazione CurioMondo"},
        "publisher": {"@type": "Organization", "name": "CurioMondo", "logo": {"@type": "ImageObject", "url": "https://curiomondo.it/curiomondo-logo-512.png"}},
    }
    body = "".join(f"<p>{p}</p>" for p in e["body"])
    sources = "".join(f'<li><a href="{u}" rel="noopener noreferrer" target="_blank">{escape(label)}</a></li>' for u, label in e["sources"])
    related = '<a href="/notizie/libia-accordo-fazioni-elezioni-entro-24-mesi-30-agosto-2026.html"><small>Mondo · Libia / Politica</small><strong>La road map firmata a Tripoli: elezioni entro 24 mesi</strong></a><a href="/notizie/niger-attacco-aeroporto-presidenza-niamey-29-agosto-2026.html"><small>Mondo · Africa / Sicurezza</small><strong>Niger, attacco all’aeroporto e alla presidenza</strong></a><a href="/notizie/come-funzionano-trasferimenti-richiedenti-asilo-europa.html"><small>Approfondimento · Migrazioni</small><strong>Come funzionano i trasferimenti dei richiedenti asilo in Europa</strong></a>'
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(e['title'])} | CurioMondo</title><meta name="description" content="{escape(e['excerpt'], quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{c}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(e['title'], quote=True)}"><meta property="og:description" content="{escape(e['excerpt'], quote=True)}"><meta property="og:url" content="{c}"><meta name="theme-color" content="#071a33"><link rel="icon" href="/favicon.ico"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=253"><script type="application/ld+json">{json.dumps(schema, ensure_ascii=False, separators=(',', ':'))}</script></head><body data-article-id="{e['slug']}"><div class="cm-reading-progress" aria-hidden="true"></div><header class="topbar"><div class="inner"><a class="btn-back" href="../approfondimenti/">← Approfondimenti</a><a class="logo" href="../index.html"><img class="cm-brand-logo" src="../curiomondo-logo-96.webp" width="36" height="36" alt=""><span class="cm-wordmark">Curio<span>Mondo</span></span></a><button class="article-theme-toggle" data-theme-toggle type="button" aria-label="Cambia tema">☾</button></div></header><main class="wrap"><div class="badge">{escape(e['category'])}</div><h1>{escape(e['title'])}</h1><p class="subtitle">{escape(e['excerpt'])}</p><div class="meta">30 agosto 2026 · Geopolitica / Libia · <span id="readTime">4 min di lettura</span></div><div class="actions"><button class="primary" id="listenBtn" type="button">▶ Ascolta l’audio</button><button type="button" data-share-article>↗ Condividi</button><button id="cmSaveBtn" type="button">★ Salva</button></div><div class="editorial-data"><div><strong>Domanda guida:</strong> chi governa la Libia e perché il voto del 2021 fallì?</div><div><strong>URL SEO:</strong> {url(e)}</div></div><article class="art-body" data-length-policy="2000-4500">{body}</article><section aria-labelledby="cm-news-link" class="cm-evergreen-reader"><small>Notizia collegata</small><h2 id="cm-news-link">Libia, firmata una road map per elezioni nazionali entro 24 mesi</h2><a href="/notizie/libia-accordo-fazioni-elezioni-entro-24-mesi-30-agosto-2026.html">Leggi l’aggiornamento →</a></section><section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">{related}</div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small>Approfondimento originale CurioMondo, aggiornato il 30 agosto 2026.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links" aria-label="Informazioni"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../pagine/cookie.html">Cookie</a><a href="../notizie/">Archivio</a><button class="cm-cookie-manage" type="button">Gestisci cookie</button></nav></footer><script src="../assets/js/site-common-v210.js" defer></script><script src="../assets/js/curiomondo-article-v210.js?v=253" defer></script></body></html>'''


def story_json(story: dict) -> dict:
    return {
        "slug": story["slug"], "title": story["title"], "excerpt": story["excerpt"], "category": story["category"],
        "published_at": story["published"], "updated_at": story["updated"], "body": story["body"],
        "related": [u for u, _, _ in story["related"]],
        "sources": [{"url": u, "label": label} for u, label in story["sources"]],
        "image": {"key": story["image_key"], "alt": story["image_alt"], "ai_generated": True,
                  "sensitive_context": story["sensitive"], "documentary_photo": False, "disclosure": CAPTION},
    }


def update_data(variants: dict[str, list[dict]]) -> list[dict]:
    news_stories = [CYPRUS, LIBYA, NEPAL]
    home_path = ROOT / "assets/data/home-feed-v210.json"
    home = json.loads(home_path.read_text(encoding="utf-8"))
    replaced = {url(x) for x in news_stories}
    home["version"] = VERSION
    home["items"] = [x for x in home["items"] if x.get("url") not in replaced] + [feed_entry(x) for x in news_stories]
    home["items"].sort(key=lambda x: x.get("dateISO", ""), reverse=True)
    dump(home_path, home, compact=True)

    search_path = ROOT / "assets/data/search-index-v210.json"
    search = json.loads(search_path.read_text(encoding="utf-8"))
    all_stories = [CYPRUS, LIBYA, NEPAL, EVERGREEN]
    replaced_all = {url(x) for x in all_stories}
    search["version"] = VERSION
    search["items"] = [x for x in search["items"] if x.get("url") not in replaced_all]
    search["items"] = [{"title": x["title"], "excerpt": x["excerpt"], "url": url(x), "section": x["category"]} for x in all_stories] + search["items"]
    dump(search_path, search, compact=True)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["version"] = VERSION
    new_items = []
    for story in news_stories:
        new_items.append({
            "key": story["image_key"], "article": url(story), "aiGenerated": True,
            "sensitiveContext": story["sensitive"], "documentaryPhoto": False, "prompt": story["prompt"],
            "variants": variants[story["slug"]], "alt": story["image_alt"], "disclosure": CAPTION,
            "portraitOnly": False, "portraitFormat": "contextual-editorial-scene", "reenactedEvent": False,
        })
    old_items = []
    for item in registry.get("items", []):
        if item.get("article") in replaced:
            if item.get("article") == url(NEPAL):
                item = dict(item)
                item["active"] = False
                item["supersededBy"] = NEPAL["image_key"]
                old_items.append(item)
            continue
        old_items.append(item)
    registry["items"] = new_items + old_items
    dump(registry_path, registry)
    return home["items"]


def picture(item: dict, eager: bool = False) -> str:
    loading = "eager" if eager else "lazy"
    priority = ' fetchpriority="high"' if eager else ""
    return (f'<picture><img alt="{escape(item.get("imageAlt", ""), quote=True)}" decoding="async" '
            f'loading="{loading}" height="533" sizes="(max-width:600px) 79vw,300px" '
            f'src="{escape(item.get("image", ""), quote=True)}" srcset="{escape(item.get("srcset", ""), quote=True)}" '
            f'width="800"{priority}></picture>')


def update_home(items: list[dict]) -> None:
    news = [x for x in items if x.get("url", "").startswith("/notizie/")]
    path = ROOT / "index.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    for track_index, track in enumerate(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')[:2]):
        for child in list(track): track.remove(child)
        for item in news[:10]:
            link = etree.SubElement(track, "a", href=item["url"], **{"class": "ticker-news"})
            if track_index == 1: link.set("tabindex", "-1")
            link.text = item["title"]

    hero_item = feed_entry(CYPRUS)
    old_featured = doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
    new_featured = html.fragment_fromstring(
        f'<a class="featured" href="{hero_item["url"]}">{picture(hero_item, eager=True)}<div class="txt">'
        f'<span class="tag">Ultima ora</span><h1>{escape(hero_item["title"])}</h1><p>{escape(hero_item["excerpt"])}</p>'
        f'<span class="cta">Leggi l’articolo →</span></div></a>')
    old_featured.getparent().replace(old_featured, new_featured)

    labels = doc.xpath('//h2[contains(concat(" ",normalize-space(@class)," ")," auto-rail-label ")]')
    if labels: labels[0].text = "Altre notizie"
    rail_items = [x for x in news if x.get("url") != hero_item["url"]][:5]
    rail = doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
    for child in list(rail): rail.remove(child)
    for item in rail_items:
        rail.append(html.fragment_fromstring(
            f'<a class="auto-card" href="{item["url"]}">{picture(item)}<div class="abody">'
            f'<div class="ameta">{escape(item["section"])}</div><h3>{escape(item["title"])}</h3>'
            f'<p>{escape(item["excerpt"])}</p><time datetime="{item["dateISO"]}">{item["dateLabel"]}</time></div></a>'))

    cards = doc.xpath('//div[@id="cards"]')[0]
    for child in list(cards): cards.remove(child)
    used = {hero_item["url"], *(x["url"] for x in rail_items)}
    for item in [x for x in news if x.get("url") not in used][:18]:
        cards.append(html.fragment_fromstring(
            f'<a class="card" href="{item["url"]}">{picture(item)}<div class="body">'
            f'<div class="meta">{escape(item["section"])}</div><h3>{escape(item["title"])}</h3>'
            f'<p>{escape(item["excerpt"])}</p><time datetime="{item["dateISO"]}">{item["dateLabel"]}</time></div></a>'))

    deep = doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cm-home-deep-links ")]//div')[0]
    for child in list(deep): deep.remove(child)
    for href, label in [
        (url(EVERGREEN), "Perché la Libia è ancora divisa"),
        ("/notizie/come-funzionano-piene-laghi-glaciali-glof-himalaya.html", "Come nascono le piene dei laghi glaciali"),
        ("/notizie/voto-postale-usa-come-funziona-regole-controlli.html", "Come funziona il voto postale negli Stati Uniti"),
    ]:
        a = etree.SubElement(deep, "a", href=href); a.text = label
    for script in doc.xpath('//script[contains(@src,"home-v210.js")]'):
        script.set("src", re.sub(r"[?&]v=\d+", "?v=253", script.get("src") or ""))
    write(path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))


def update_archives(items: list[dict]) -> None:
    news = [x for x in items if x.get("url", "").startswith("/notizie/")]
    archive_path = ROOT / "notizie/index.html"
    doc = html.fromstring(archive_path.read_text(encoding="utf-8"))
    ul = doc.xpath("//main//ul")[0]
    for child in list(ul): ul.remove(child)
    archive_items = news.copy()
    evergreen_entry = {"title": EVERGREEN["title"], "url": url(EVERGREEN), "dateLabel": DATE_LABEL, "dateISO": EVERGREEN["updated"]}
    archive_items.append(evergreen_entry)
    archive_items.sort(key=lambda x: x.get("dateISO", ""), reverse=True)
    for item in archive_items:
        li = etree.SubElement(ul, "li"); link = etree.SubElement(li, "a", href=item["url"])
        strong = etree.SubElement(link, "strong"); strong.text = item["title"]
        span = etree.SubElement(link, "span"); span.text = item["dateLabel"]
    paragraphs = doc.xpath("//main/p")
    if paragraphs: paragraphs[0].text = f"{len(archive_items)} articoli, ordinati per data."
    write(archive_path, "<!doctype html>" + html.tostring(doc, encoding="unicode", method="html"))

    deep_path = ROOT / "approfondimenti/index.html"
    deep_doc = html.fromstring(deep_path.read_text(encoding="utf-8"))
    grid = deep_doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," grid ")]')[0]
    for old in grid.xpath(f'./a[@data-cm-evergreen-slug="{EVERGREEN["slug"]}"]'): grid.remove(old)
    card = html.fragment_fromstring(f'<a class="card" href="../notizie/{EVERGREEN["slug"]}.html" data-cm-evergreen-slug="{EVERGREEN["slug"]}"><span class="tag">{escape(EVERGREEN["category"])}</span><div><h2>{escape(EVERGREEN["title"])}</h2><p>{escape(EVERGREEN["excerpt"])}</p></div><b>Leggi l’approfondimento →</b></a>')
    grid.insert(0, card)
    write(deep_path, "<!doctype html>" + html.tostring(deep_doc, encoding="unicode", method="html"))

    live_path = ROOT / "automation/live-seed.json"
    live = json.loads(live_path.read_text(encoding="utf-8"))
    live["updated_at"] = "2026-08-30T14:05:00+00:00"
    live["items"] = [{"title": x["title"], "url": x["url"], "published_at": x["dateISO"],
                      "source": "CurioMondo", "article_exists": True} for x in news[:10]]
    dump(live_path, live)


def update_xml() -> None:
    stories = [CYPRUS, LIBYA, NEPAL, EVERGREEN]
    feed_path = ROOT / "feed.xml"
    tree = etree.parse(str(feed_path)); channel = tree.getroot().find("channel")
    assert channel is not None
    targets = {canonical(x) for x in stories}
    for old in list(channel.findall("item")):
        if old.findtext("link") in targets: channel.remove(old)
    insertion = next((i for i, child in enumerate(channel) if child.tag == "item"), len(channel))
    for story in stories:
        node = etree.Element("item")
        for tag, value in (("title", story["title"]), ("link", canonical(story)), ("guid", canonical(story)),
                           ("pubDate", format_datetime(datetime.fromisoformat(story["updated"]))), ("description", story["excerpt"])):
            child = etree.SubElement(node, tag); child.text = value
        channel.insert(insertion, node); insertion += 1
    tree.write(str(feed_path), encoding="utf-8", xml_declaration=True, pretty_print=True)

    ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
    site_path = ROOT / "sitemap.xml"
    tree = etree.parse(str(site_path)); root = tree.getroot()
    existing = {x.text for x in root.xpath('//*[local-name()="loc"]')}
    for story in stories:
        if canonical(story) in existing: continue
        u = etree.SubElement(root, f"{{{ns}}}url")
        loc = etree.SubElement(u, f"{{{ns}}}loc"); loc.text = canonical(story)
        lastmod = etree.SubElement(u, f"{{{ns}}}lastmod"); lastmod.text = DATE_LABEL
    tree.write(str(site_path), encoding="utf-8", xml_declaration=True, pretty_print=True)

    news_path = ROOT / "news-sitemap.xml"
    tree = etree.parse(str(news_path)); root = tree.getroot()
    targets = {canonical(x) for x in [CYPRUS, LIBYA, NEPAL]}
    for node in list(root):
        locs = node.xpath('./*[local-name()="loc"]/text()')
        if locs and locs[0] in targets: root.remove(node)
    nns = "http://www.google.com/schemas/sitemap-news/0.9"
    for story in [CYPRUS, LIBYA, NEPAL]:
        u = etree.SubElement(root, f"{{{ns}}}url")
        loc = etree.SubElement(u, f"{{{ns}}}loc"); loc.text = canonical(story)
        news = etree.SubElement(u, f"{{{nns}}}news")
        publication = etree.SubElement(news, f"{{{nns}}}publication")
        name = etree.SubElement(publication, f"{{{nns}}}name"); name.text = "CurioMondo"
        language = etree.SubElement(publication, f"{{{nns}}}language"); language.text = "it"
        date = etree.SubElement(news, f"{{{nns}}}publication_date"); date.text = story["published"]
        title = etree.SubElement(news, f"{{{nns}}}title"); title.text = story["title"]
    tree.write(str(news_path), encoding="utf-8", xml_declaration=True, pretty_print=True)


def update_release() -> None:
    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        data = json.loads(path.read_text(encoding="utf-8"))
        data.update({"currentVersion": VERSION, "site_version": VERSION, "version": str(VERSION),
                     "baselineVersion": 252, "baseline_version": 252,
                     "baseline": "curiomondo-v252-30-agosto-2026-motogp-marquez-netlify.zip",
                     "date": DATE_LABEL, "release_date": DATE_LABEL,
                     "articleCount": 200, "generatedEditorialImages": 80,
                     "last_update": "cipro-libia-nepal-v253",
                     "designRestored": "Cipro e Libia pubblicati; Nepal aggiornato; evergreen Libia aggiunto; home, LIVE e indici riallineati."})
        dump(path, data)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"]["current_site_version"] = VERSION
    manifest["site_version"] = VERSION
    manifest["version"] = "v253"
    manifest["release_version"] = "v253"
    manifest["last_release_date"] = DATE_LABEL
    manifest["last_release"] = {"version": VERSION, "date": DATE_LABEL, "baseline_version": 252,
                                "news_added": [CYPRUS["slug"], LIBYA["slug"]],
                                "news_updated": [NEPAL["slug"]], "evergreen_added": [EVERGREEN["slug"]],
                                "daily_question_preserved": manifest["daily_state"]["last_question_slug"],
                                "image_policy_applied": "sensitive-disaster-context-no-visible-victims-v253"}
    dump(manifest_path, manifest)
    write(ROOT / "RELEASE-NOTES-v253.md", f'''# CurioMondo v253 — 30 agosto 2026

- Pubblicato “{CYPRUS['title']}” come unica pagina canonica, assorbendo i conteggi precedenti.
- Pubblicato “{LIBYA['title']}”.
- Aggiornato l’articolo Nepal–Tibet senza creare duplicati.
- Aggiunto l’approfondimento evergreen “{EVERGREEN['title']}” con collegamento bidirezionale alla notizia.
- Create tre nuove immagini editoriali IA, tutte non documentarie; nei due contesti sensibili non sono raffigurate vittime.
- Aggiornati apertura, LIVE, Altre notizie, archivio, ricerca, feed RSS, sitemap e news sitemap.
''')
    predeploy_path = ROOT / "tools/predeploy.py"
    text = predeploy_path.read_text(encoding="utf-8")
    text = text.replace('"""CurioMondo v252 static pre-deploy audit."""', '"""CurioMondo v253 static pre-deploy audit."""')
    text = text.replace("report={'version':252", "report={'version':253")
    write(predeploy_path, text)


def main() -> None:
    for story in (CYPRUS, LIBYA, NEPAL):
        chars = len(re.sub(r"<[^>]+>", "", " ".join(story["body"])))
        if not 2000 <= chars <= 4500: raise SystemExit(f"Body length invalid for {story['slug']}: {chars}")
    evergreen_chars = len(re.sub(r"<[^>]+>", "", " ".join(EVERGREEN["body"])))
    if not 2000 <= evergreen_chars <= 4500: raise SystemExit(f"Evergreen body length invalid: {evergreen_chars}")
    variants = make_images([CYPRUS, LIBYA, NEPAL])
    for story in (CYPRUS, LIBYA):
        write(ROOT / f"notizie/{story['slug']}.html", article_html(story))
        dump(ROOT / f"contenuti/notizie/{story['slug']}.json", story_json(story))
    write(ROOT / f"notizie/{NEPAL['slug']}.html", article_html(NEPAL, published_label="27 agosto 2026"))
    dump(ROOT / f"contenuti/notizie/{NEPAL['slug']}.json", story_json(NEPAL))
    write(ROOT / f"notizie/{EVERGREEN['slug']}.html", evergreen_html())
    dump(ROOT / f"contenuti/notizie/{EVERGREEN['slug']}.json", {
        "slug": EVERGREEN["slug"], "title": EVERGREEN["title"], "excerpt": EVERGREEN["excerpt"],
        "category": EVERGREEN["category"], "published_at": EVERGREEN["published"], "updated_at": EVERGREEN["updated"],
        "body": EVERGREEN["body"], "related": [url(LIBYA)],
        "sources": [{"url": u, "label": label} for u, label in EVERGREEN["sources"]],
    })
    items = update_data(variants)
    update_home(items)
    update_archives(items)
    update_xml()
    update_release()
    print(json.dumps({"version": VERSION, "added": [CYPRUS["slug"], LIBYA["slug"], EVERGREEN["slug"]],
                      "updated": [NEPAL["slug"]], "bodyCharacters": {
                          CYPRUS["slug"]: len(" ".join(CYPRUS["body"])), LIBYA["slug"]: len(" ".join(LIBYA["body"])),
                          NEPAL["slug"]: len(" ".join(NEPAL["body"])), EVERGREEN["slug"]: evergreen_chars}},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
