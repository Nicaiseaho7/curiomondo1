#!/usr/bin/env python3
"""Cinque novità internazionali, spaziali e di servizio dell'11 ottobre."""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publish_finale_20261010_v836 as prior
from tools import publish_notte_mattina_20261010_v827 as base
from automation.newsroom import site

VERSION = 841
base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "zelensky": ROOT.parent / "generated_images/exec-e71f23a8-56e6-4208-bd09-77ce1a0d67cf.png",
    "iride": ROOT.parent / "generated_images/exec-d3686749-216e-4681-af20-f480eddf1104.png",
    "frana": ROOT.parent / "generated_images/exec-4352b0c1-7c05-4b17-b0a6-fcf0452c1e64.png",
    "sciopero": ROOT.parent / "generated_images/exec-bbc9ba84-2a7d-4e6c-be86-606ce9fe0ec0.png",
    "allerta": ROOT.parent / "generated_images/exec-e8cbf6c9-4daa-4fe5-a0d8-055a17563778.png",
}

ARTICLES = [
    {
        "slug": "zelensky-elezioni-ucraina-tregua-60-giorni-11-ottobre-2026",
        "titolo": "Zelensky: elezioni in Ucraina con 60 giorni di tregua totale",
        "sommario": "Il presidente ucraino pone la condizione in un'intervista ad ABC. Non è stato annunciato un cessate il fuoco concordato con Mosca.",
        "categoria": "Mondo", "luogo": "Kyiv", "formato": "flash",
        "parole_chiave_titolo": ["Zelensky", "60 giorni"],
        "dati_chiave": [{"valore": "60 giorni", "etichetta": "tregua richiesta"}, {"valore": "11 ottobre", "etichetta": "intervista"}, {"valore": "condizione", "etichetta": "non accordo"}],
        "paragrafi": [
            "Volodymyr Zelenskyy ha detto domenica 11 ottobre che l'Ucraina potrebbe organizzare elezioni se la Russia rispettasse un cessate il fuoco totale di 60 giorni. Il presidente ucraino ha formulato la condizione durante un'intervista al programma This Week di ABC News, dopo le critiche del presidente statunitense Donald Trump alla sua leadership.",
            "Zelenskyy ha ribadito che la scelta del presidente spetta agli ucraini. Nel testo integrale dell'intervista, la proposta riguarda due mesi senza combattimenti per consentire l'organizzazione del voto: non è l'annuncio di una data elettorale né di un'intesa già sottoscritta da Kyiv e Mosca.",
            "Il presidente ha collegato la questione anche agli attacchi contro le infrastrutture energetiche. Ha sostenuto che l'Ucraina sarebbe pronta a interrompere i propri attacchi alle raffinerie russe se la Russia smettesse di colpire il sistema energetico ucraino. Si tratta di una posizione condizionata, non della prova che gli attacchi siano cessati.",
            "La distinzione conta per l'Europa, che continua a discutere sostegno e sanzioni nel quadro della guerra: una dichiarazione unilaterale non modifica automaticamente le misure in vigore né garantisce un'interruzione dei combattimenti. Serviranno eventuali accordi e verifiche successive.",
        ],
        "fonti": [{"url": "https://abcnews.com/amp/Politics/week-transcript-10-11-26-ukrainian-president-volodymyr/story?id=137165082", "nome": "ABC News — trascrizione integrale dell'intervista a Zelenskyy, 11 ottobre 2026."}, {"url": "https://www.reuters.com/world/europe/ukraines-zelenskiy-tells-abc-he-will-organize-elections-if-russia-agrees-60-day-2026-10-11/", "nome": "Reuters — verifica indipendente della condizione sui 60 giorni di tregua."}],
        "image_source": "zelensky", "image_likeness": "Volodymyr Zelenskyy",
        "image_alt": "Ritratto editoriale sintetico di Volodymyr Zelenskyy con bandiera ucraina; non è una fotografia dell'intervista ad ABC.",
        "image_prompt": "Ritratto ultrarealistico sintetico di Zelenskyy in ambiente istituzionale, non documentario; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "iride-eaglet-ii-prime-immagini-gibilterra-italia-ottobre-2026",
        "titolo": "IRIDE, prime immagini Eaglet II da Gibilterra: test per il monitoraggio",
        "sommario": "ESA mostra gli scatti ricevuti dal centro di controllo OHB Italia a Roma. La costellazione è nella fase di verifica prima dell'entrata in servizio.",
        "categoria": "Tecnologia", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["IRIDE", "Gibilterra"],
        "dati_chiave": [{"valore": "16", "etichetta": "satelliti Eaglet II"}, {"valore": "9 ottobre", "etichetta": "pubblicazione ESA"}, {"valore": "Roma", "etichetta": "centro di controllo"}],
        "paragrafi": [
            "I satelliti Eaglet II del programma italiano IRIDE hanno trasmesso le prime immagini della Terra, fra cui una veduta dello Stretto di Gibilterra pubblicata dall'Agenzia spaziale europea il 9 ottobre. I dati sono stati ricevuti dal centro di controllo di OHB Italia a Roma durante la fase iniziale di verifica in orbita.",
            "Nella scena descritta da ESA sono visibili la rocca, l'area urbana, il porto, l'aeroporto e le navi. I risultati dimostrano che piattaforma e strumento ottico hanno iniziato a funzionare; non equivalgono ancora all'annuncio di un servizio operativo per tutti gli utenti.",
            "La costellazione Eaglet II conta 16 satelliti progettati e sviluppati da OHB Italia. Ciascuno porta un sensore multispettrale e un sistema di identificazione automatica per applicazioni di osservazione e sorveglianza marittima. Gli ultimi otto erano stati lanciati all'inizio di ottobre.",
            "IRIDE è un'infrastruttura nazionale di osservazione della Terra di proprietà dell'Agenzia spaziale italiana, sviluppata con ESA e finanziata nel quadro del PNRR e del piano complementare. Le applicazioni prospettate riguardano istituzioni e servizi pubblici, ma l'entrata in servizio segue ancora le verifiche delle prestazioni.",
        ],
        "fonti": [{"url": "https://www.esa.int/ESA_Multimedia/Images/2026/10/Gibraltar_imaged_by_IRIDE_Eaglet_II", "nome": "ESA — prime immagini Eaglet II e stato della fase di verifica, 9 ottobre 2026."}],
        "image_source": "iride",
        "image_alt": "Visualizzazione IA di un piccolo satellite sopra lo Stretto di Gibilterra; non è una ripresa reale né un modello tecnico esatto di Eaglet II.",
        "image_prompt": "Satellite sintetico IRIDE sopra Gibilterra, visualizzazione non documentaria; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "frana-treni-nocera-salerno-via-cava-bus-11-ottobre-2026",
        "titolo": "Frana sulla Nocera–Salerno via Cava: treni sospesi, bus attivi",
        "sommario": "RFI conferma lo stop dalle 5:30 e la sospensione ancora nell'aggiornamento delle 13. Verificare il proprio collegamento prima di partire.",
        "categoria": "Trasporti", "luogo": "Salerno", "formato": "flash",
        "parole_chiave_titolo": ["Nocera–Salerno", "bus"],
        "dati_chiave": [{"valore": "5:30", "etichetta": "inizio dello stop"}, {"valore": "13:00", "etichetta": "ultimo bollettino RFI"}, {"valore": "bus", "etichetta": "corse attivate"}],
        "paragrafi": [
            "La circolazione ferroviaria tra Nocera Inferiore e Salerno via Cava de' Tirreni è sospesa dalle 5:30 di domenica 11 ottobre per un movimento franoso. Nell'ultimo aggiornamento pubblicato da RFI alle 13, lo stop era ancora in vigore e i tecnici erano al lavoro.",
            "RFI ha attivato corse con autobus e sta riprogrammando l'offerta ferroviaria. Il comunicato non indica un orario di riapertura: i tempi di viaggio e i collegamenti disponibili vanno verificati per il singolo treno sui monitor di stazione e sui canali dell'impresa ferroviaria.",
            "La sospensione riguarda il percorso via Cava, non tutte le linee fra Napoli e Salerno. Chi attraversa la zona dovrebbe controllare se il proprio convoglio è cancellato, limitato o deviato prima di raggiungere la stazione.",
            "L'avviso di oggi è distinto dai lavori programmati nel fine settimana su altri tratti dell'area napoletana. RFI non attribuisce alla frana un incidente ferroviario con passeggeri coinvolti.",
        ],
        "fonti": [{"url": "https://www.rfi.it/it/news-e-media/infomobilita/aggiornamenti/2026/10/11/linea-nocera-inferiore---salerno-via-cava--dalle-ore-05-30-circo.html", "nome": "RFI — aggiornamento sulla sospensione via Cava e corse bus, 11 ottobre 2026."}],
        "image_source": "frana", "image_sensitive": True, "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA di una linea ferroviaria vicino a un pendio franoso; non documenta il tratto reale né un incidente a un treno.",
        "image_prompt": "Linea ferroviaria sintetica interrotta da frana in Campania, nessun treno coinvolto; logo circolare in post-produzione.",
    },
    {
        "slug": "sciopero-treni-toscana-14-ottobre-2026-fs-italo-orari",
        "titolo": "Sciopero treni in Toscana il 14 ottobre: possibili disagi 9:01–17",
        "sommario": "RFI segnala l'agitazione del personale del Gruppo FS e Italo. Possibili variazioni anche prima e dopo la fascia indicata.",
        "categoria": "Trasporti", "luogo": "Toscana", "formato": "flash",
        "parole_chiave_titolo": ["Sciopero treni", "14 ottobre"],
        "dati_chiave": [{"valore": "14 ottobre", "etichetta": "giorno dello sciopero"}, {"valore": "9:01–17:00", "etichetta": "fascia indicata"}, {"valore": "FS e Italo", "etichetta": "personale coinvolto"}],
        "paragrafi": [
            "Mercoledì 14 ottobre i treni possono subire ritardi o variazioni per uno sciopero del personale della Toscana del Gruppo FS Italiane e di Italo, dalle 9:01 alle 17. L'avviso è pubblicato da RFI per i servizi regionali, a lunga percorrenza e ad alta velocità.",
            "La proclamazione riguarda personale della regione Toscana, ma l'impatto può interessare anche chi attraversa la regione con un treno di altra provenienza o destinazione. L'elenco di regioni nell'avviso RFI non significa che tutto il personale ferroviario italiano scioperi.",
            "RFI avverte che le modifiche possono verificarsi anche prima dell'inizio e dopo la conclusione della fascia. Le indicazioni sui servizi garantiti vanno cercate sui canali delle singole imprese ferroviarie o presso assistenza e biglietterie: l'avviso generale non fornisce una lista valida per ogni treno.",
            "Chi viaggia il 14 ottobre dovrebbe verificare il numero del treno prima di partire e ricontrollarlo il giorno stesso. Lo sciopero è futuro: non sono disponibili dati sull'adesione effettiva o cancellazioni certe per tutti i collegamenti.",
        ],
        "fonti": [{"url": "https://www.rfi.it/it/news-e-media/infomobilita/avvisi/2026/10/14/sciopero-del-personale-del-gruppo-fs-italiane-e-di-italo-regione.html", "nome": "RFI — avviso sciopero ferroviario del 14 ottobre 2026."}],
        "image_source": "sciopero",
        "image_alt": "Illustrazione editoriale IA di un treno in una stazione fiorentina evocativa; non è una fotografia dello sciopero del 14 ottobre.",
        "image_prompt": "Treno in stazione fiorentina evocativa, visual non documentario dello sciopero; logo CurioMondo circolare in post-produzione.",
    },
    {
        "slug": "allerta-gialla-12-ottobre-2026-calabria-abruzzo-sicilia",
        "titolo": "Allerta gialla il 12 ottobre: rischio idraulico sulla costa tirrenica calabrese",
        "sommario": "Il bollettino nazionale segnala anche temporali e rischio idrogeologico in zone di Abruzzo, Campania, Sicilia e Toscana. Le allerte sono territoriali, non regionali uniformi.",
        "categoria": "Meteo", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Allerta gialla", "Calabria"],
        "dati_chiave": [{"valore": "12 ottobre", "etichetta": "giorno dell'allerta"}, {"valore": "gialla", "etichetta": "livello segnalato"}, {"valore": "14:17", "etichetta": "bollettino odierno"}],
        "paragrafi": [
            "Per lunedì 12 ottobre la Protezione Civile segnala allerta gialla per rischio idraulico sui quattro versanti tirrenici della Calabria, dal settore settentrionale a quello meridionale. Il bollettino nazionale è stato emesso domenica alle 14:17 e si riferisce a zone di allerta, non all'intera regione senza distinzioni.",
            "Nelle stesse aree calabresi è indicata anche allerta gialla per temporali e rischio idrogeologico. Per temporali e rischio idrogeologico il livello giallo riguarda inoltre i bacini Tordino-Vomano e Pescara in Abruzzo e alcune zone della Sicilia nord-orientale e tirrenica.",
            "Il rischio idrogeologico giallo è segnalato anche in zone della Campania, fra area di Napoli, Piana del Sele, Alto Cilento e Penisola sorrentina-amalfitana. In Toscana, le zone di Serchio-Costa, Arno-Costa, Etruria-Costa Nord, Serchio-Lucca e Versilia risultano in allerta gialla per temporali e rischio idrogeologico.",
            "L'allerta indica una previsione di criticità, non che in ogni località si verificheranno allagamenti o frane. Chi deve spostarsi domani dovrebbe consultare la mappa ufficiale per il proprio comune e gli aggiornamenti della Regione, evitando sottopassi o corsi d'acqua se si sviluppano condizioni pericolose.",
        ],
        "fonti": [{"url": "https://mappe.protezionecivile.gov.it/it/mappe-rischi/bollettino-di-criticita/index.html", "nome": "Dipartimento della Protezione Civile — bollettino di criticità dell'11 ottobre 2026, ore 14:17."}],
        "image_source": "allerta",
        "image_alt": "Illustrazione editoriale IA della costa tirrenica calabrese sotto cielo nuvoloso; non è una fotografia di fenomeni già osservati.",
        "image_prompt": "Paesaggio tirrenico calabrese in condizioni nuvolose illustrative, senza fenomeni estremi osservati; logo CurioMondo circolare in post-produzione.",
    },
]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("uso: script.py indice timestamp-ISO-Europe/Rome")
    index = int(sys.argv[1]); published = datetime.fromisoformat(sys.argv[2])
    if published.utcoffset() != ZoneInfo("Europe/Rome").utcoffset(published):
        raise SystemExit("timestamp Europe/Rome richiesto")
    if index == 0:
        phrases_path = ROOT / "assets/data/frasi-nome.json"
        phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
        for phrase in (
            "Puoi aspettare fatti concreti prima di prendere posizione.",
            "Una scoperta nuova merita anche pazienza nelle verifiche.",
            "Prima di partire, controlla il tuo collegamento aggiornato.",
            "Organizza il viaggio con un margine per gli imprevisti.",
            "Segui gli avvisi locali e proteggi i tuoi spostamenti.",
        ):
            if phrase not in phrases: phrases.append(phrase)
        phrases_path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    article = ARTICLES[index]
    image = base.make_image(article)
    slug = site.write_article(article, image, VERSION)
    base.set_published(slug, published)
    prior.correct_visible_date(slug, published, article["luogo"])
    image["article"] = f"/notizie/{slug}.html"
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    registry["items"] = [image] + registry.get("items", [])
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if index == len(ARTICLES) - 1:
        site.sync_surfaces(ARTICLES, f"/notizie/{slug}.html", VERSION, update_manifest=False)
        state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
        state = json.loads(state_path.read_text(encoding="utf-8"))
        state.update({"site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
                      "articleCount": int(state.get("articleCount", 0)) + len(ARTICLES),
                      "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(ARTICLES),
                      "last_update": f"mondo-servizi-v{VERSION}", "date": published.date().isoformat(),
                      "release_date": published.date().isoformat(), "updated_at": published.isoformat(timespec="seconds"),
                      "status": "ready"})
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"index": index, "slug": slug, "published": published.isoformat()}, ensure_ascii=False))


if __name__ == "__main__": main()
