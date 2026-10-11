#!/usr/bin/env python3
"""Lotto mattutino 11 ottobre: scrittura in tre tempi, superfici sincronizzate una volta."""
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

VERSION = 837
base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "riyadh": ROOT.parent / "generated_images/exec-50b7aca9-4413-4c8d-a3b2-711b675c72fc.png",
    "bolzano": ROOT.parent / "generated_images/exec-c6af2ae7-050b-4315-aae6-f460be073554.png",
    "castellanza": ROOT.parent / "generated_images/exec-81029b8c-9ac8-48e6-9057-6fa31afc62d4.png",
    "oman": ROOT.parent / "generated_images/exec-d8097d2e-9e28-4691-b22e-65e50ce3611e.png",
}

ARTICLES = [
    {
        "slug": "riyadh-aeroporto-attacco-12-morti-309-feriti-11-ottobre-2026",
        "titolo": "Riad, nuovo attacco all'aeroporto: 12 morti e 309 feriti",
        "sommario": "La nuova stima ufficiale riguarda l'attacco di sabato 10 ottobre, distinto da quelli dei giorni precedenti. Operazioni sospese nello scalo King Khalid: i passeggeri devono verificare il proprio volo.",
        "categoria": "Mondo", "luogo": "Arabia Saudita", "formato": "flash",
        "parole_chiave_titolo": ["12 morti", "309 feriti"],
        "dati_chiave": [{"valore": "12", "etichetta": "morti nell'attacco di sabato"}, {"valore": "309", "etichetta": "feriti secondo l'autorità"}, {"valore": "10 ottobre", "etichetta": "data del nuovo attacco"}],
        "paragrafi": [
            "L'attacco di sabato 10 ottobre all'aeroporto internazionale King Khalid di Riad ha causato 12 morti e 309 feriti, secondo il bilancio comunicato nelle prime ore di domenica dall'Autorità saudita per l'aviazione civile. Alcune persone ferite sono in condizioni critiche. Lo scalo ha sospeso temporaneamente le operazioni per le verifiche di sicurezza.",
            "Quattro vittime sono cittadini sauditi; tra le altre figurano due persone del Bangladesh e una ciascuna di Stati Uniti, Egitto, Giordania, Siria, Palestina e Sudan, riferisce l'autorità. La valutazione dei danni materiali è ancora in corso. Il numero dei feriti è un aggiornamento ufficiale, non una stima ricavata dai voli cancellati.",
            "Si tratta di un episodio diverso dai due attacchi di giovedì 8 ottobre contro le infrastrutture aeroportuali e un aereo Saudia, di cui CurioMondo aveva riferito il bilancio di tre vittime. I due conteggi non vanno confusi né sommati come se descrivessero un unico evento.",
            "Reuters riferisce che i voli per Riad di sabato sono stati cancellati o dirottati e che gli Houthi hanno rivendicato l'azione. L'attribuzione ai ribelli resta una rivendicazione, distinta dal bilancio delle vittime comunicato dall'aviazione civile saudita. Non è stata annunciata un'ora certa di riapertura dell'aeroporto.",
            "Chi ha un viaggio da o per Riad deve controllare lo stato della singola prenotazione con la compagnia aerea prima di raggiungere l'aeroporto e seguire gli avvisi dell'operatore dello scalo. Una sospensione temporanea non consente di presumere che tutti i collegamenti riprendano insieme: riprotezioni e rimborsi dipendono dal vettore e dal titolo di viaggio.",
        ],
        "fonti": [
            {"url": "https://x.com/ksagaca/status/2109039231968383000", "nome": "Autorità generale saudita dell'aviazione civile — aggiornamento ufficiale sul bilancio del 10 ottobre."},
            {"url": "https://www.reuters.com/world/middle-east/loud-blast-heard-riyadh-airport-airlines-cancel-more-flights-2026-10-10/", "nome": "Reuters — verifica indipendente del bilancio e delle conseguenze per i voli."},
        ],
        "image_source": "riyadh", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica dell'esterno di un aeroporto a Riad all'alba; non documenta l'attacco.",
        "image_prompt": "Esterno aeroportuale saudita all'alba dopo un allarme, illustrazione editoriale non documentaria; logo circolare applicato dopo.",
    },
    {
        "slug": "bolzano-merano-treni-cancellati-bus-11-ottobre-2026",
        "titolo": "Bolzano–Merano, treni cancellati fino alle 13:30: bus sostitutivi",
        "sommario": "Dalle 7:50 di domenica 11 ottobre i treni sono sostituiti da autobus per lavori di manutenzione straordinaria. RFI avverte che le variazioni possono iniziare prima e terminare dopo la finestra del cantiere.",
        "categoria": "Italia", "luogo": "Alto Adige", "formato": "flash",
        "parole_chiave_titolo": ["Bolzano–Merano", "13:30"],
        "dati_chiave": [{"valore": "7:50", "etichetta": "inizio previsto"}, {"valore": "13:30", "etichetta": "fine lavori"}, {"valore": "bus", "etichetta": "servizio sostitutivo"}],
        "paragrafi": [
            "Domenica 11 ottobre, tra Bolzano e Merano, i treni sono cancellati e sostituiti da bus dalle 7:50 alle 13:30 per lavori di manutenzione straordinaria. È l'avviso di Rete Ferroviaria Italiana per i servizi regionali di Trenitalia e SAD, utile a chi programma uno spostamento nella mattinata.",
            "La fascia 7:50–13:30 indica l'intervento, non il limite esatto di ogni modifica al viaggio. RFI specifica che le variazioni possono cominciare prima dei lavori e proseguire dopo la loro conclusione: il numero della propria corsa va verificato nei canali di vendita delle imprese ferroviarie.",
            "Il tempo di percorrenza dei bus può cambiare con il traffico stradale. Sul mezzo sostitutivo non sono ammessi biciclette, monopattini e altri veicoli elettrici di micromobilità, né animali di grossa taglia; il cane da assistenza è sempre ammesso.",
            "L'avviso è limitato al collegamento Bolzano–Merano e non annuncia una sospensione dell'intera rete altoatesina. Prima di partire, chi ha una coincidenza dovrebbe confrontare l'orario del bus con quello del treno successivo: l'operatore non garantisce la stessa durata del tragitto su strada.",
        ],
        "fonti": [{"url": "https://www.rfi.it/it/news-e-media/infomobilita/avvisi/2026/10/11/linea-bolzano---merano---strecke-bozen---meran-.html", "nome": "RFI — avviso di modifica Bolzano–Merano in vigore l'11 ottobre."}],
        "image_source": "bolzano", "image_alt": "Illustrazione editoriale IA ultrarealistica di treno e bus in una stazione altoatesina; non è una fotografia dei lavori.",
        "image_prompt": "Treno e bus sostitutivo in Alto Adige, scena editoriale non documentaria; logo circolare applicato dopo.",
    },
    {
        "slug": "a8-castellanza-entrata-milano-chiusa-11-ottobre-2026",
        "titolo": "A8, entrata di Castellanza verso Milano chiusa fino alle 20",
        "sommario": "La chiusura continua per l'intera domenica 11 ottobre a causa dei lavori alle barriere antirumore. Autostrade per l'Italia indica Legnano come ingresso alternativo.",
        "categoria": "Italia", "luogo": "Castellanza", "formato": "flash",
        "parole_chiave_titolo": ["A8", "Castellanza"],
        "dati_chiave": [{"valore": "20:00", "etichetta": "fine programmata"}, {"valore": "Legnano", "etichetta": "ingresso alternativo"}, {"valore": "A8", "etichetta": "direzione Milano"}],
        "paragrafi": [
            "L'entrata di Castellanza sulla A8 Milano–Varese in direzione Milano resta chiusa domenica 11 ottobre fino alle 20:00. Autostrade per l'Italia ha programmato l'interruzione continuativa dalle 21 di venerdì 9 per lavori di riqualificazione delle barriere antirumore.",
            "L'alternativa indicata dal concessionario è l'ingresso allo svincolo di Legnano. La misura riguarda l'accesso di Castellanza verso Milano, non la chiusura dell'intera autostrada A8 né l'uscita dallo stesso svincolo: scegliere il percorso in base alla direzione evita una deviazione non necessaria.",
            "L'orario delle 20 è la fine prevista del cantiere nel comunicato pubblicato il 5 ottobre. Per eventuali cambiamenti durante la giornata, Autostrade segnala l'app, i pannelli a messaggio variabile e il numero di viabilità 803.111, attivo 24 ore su 24.",
        ],
        "fonti": [{"url": "https://www.autostrade.it/it/comunicazione-e-media/comunicati-stampa-viabilita/-/bulletin/view/aead02bf-76fd-476a-aab1-a5b6e5e25d37", "nome": "Autostrade per l'Italia — comunicato sulla chiusura di Castellanza del 9–11 ottobre."}],
        "image_source": "castellanza", "image_alt": "Illustrazione editoriale IA ultrarealistica di una rampa autostradale temporaneamente chiusa; non è la fotografia del cantiere reale.",
        "image_prompt": "Rampa autostradale chiusa per lavori, scena editoriale non documentaria; logo circolare applicato dopo.",
    },
    {
        "slug": "golfo-oman-usa-colpiscono-nave-ocean-molica-11-ottobre-2026",
        "titolo": "Golfo dell'Oman, gli USA fermano una nave cargo con un attacco",
        "sommario": "CENTCOM afferma di aver colpito la poppa della Ocean Molica, battente bandiera panamense, per impedirle di violare il blocco dei porti iraniani. Secondo il comando, l'equipaggio non è stato ferito.",
        "categoria": "Mondo", "luogo": "Golfo dell'Oman", "formato": "flash",
        "parole_chiave_titolo": ["Golfo dell'Oman", "nave cargo"],
        "dati_chiave": [{"valore": "10 ottobre", "etichetta": "data dell'intervento"}, {"valore": "Ocean Molica", "etichetta": "nave coinvolta"}, {"valore": "0", "etichetta": "feriti tra l'equipaggio secondo CENTCOM"}],
        "paragrafi": [
            "Un caccia statunitense ha colpito sabato 10 ottobre la poppa della nave cargo Ocean Molica nel Golfo dell'Oman, disabilitandone la propulsione. Lo riferisce il comando militare americano CENTCOM, secondo cui l'equipaggio non ha riportato ferite. La nave batte bandiera panamense ed è indicata anche con il nome Arika Sun.",
            "La versione di CENTCOM è che la nave, partita in precedenza da un porto iraniano, abbia ignorato ripetuti avvisi e tentato di violare il blocco navale statunitense dei porti dell'Iran. Reuters riporta la dichiarazione ma segnala di non aver raggiunto subito l'operatore del mercantile per una replica: non c'è in questo momento una ricostruzione indipendente completa della manovra.",
            "Il comando dice di aver usato un ordigno di precisione sulla poppa per fermare la nave senza danneggiare l'equipaggio. Non sono stati diffusi nel comunicato dettagli verificati sul carico o sulla destinazione finale; attribuirle un trasporto specifico sarebbe prematuro.",
            "Per le imbarcazioni nell'area, CENTCOM invita a seguire gli avvisi relativi al blocco, monitorare le comunicazioni ai naviganti e contattare le forze navali statunitensi sul canale radio 16 in prossimità dello Stretto di Hormuz. Si tratta delle istruzioni del comando che conduce l'operazione, non di una modifica generalizzata alle rotte commerciali annunciata da autorità italiane.",
            "L'episodio si inserisce nella tensione sulla navigazione del Golfo e sulle spedizioni da e verso i porti iraniani. Le possibili ripercussioni sui prezzi dell'energia o sui rifornimenti in Italia non sono quantificate dal comunicato: serviranno dati su traffico e mercati prima di attribuire effetti economici a questo singolo intervento.",
        ],
        "fonti": [
            {"url": "https://www.forth.news/lists/centcom/CfuUiQPmfHxXfWGGkPzeZ", "nome": "U.S. Central Command — comunicato originale sul fermo della Ocean Molica, diffuso sul canale CENTCOM."},
            {"url": "https://www.reuters.com/world/us-military-says-it-disabled-cargo-vessel-trying-run-iran-blockade-2026-10-11/", "nome": "Reuters — verifica indipendente e limite sulla replica dell'operatore."},
        ],
        "image_source": "oman", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una nave cargo nel Golfo dell'Oman; non mostra l'intervento militare reale.",
        "image_prompt": "Nave mercantile nel Golfo dell'Oman, scena editoriale non documentaria; logo circolare applicato dopo.",
    },
]


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("uso: script.py indice timestamp-ISO-Europe/Rome")
    index = int(sys.argv[1])
    published = datetime.fromisoformat(sys.argv[2])
    if published.utcoffset() != ZoneInfo("Europe/Rome").utcoffset(published):
        raise SystemExit("timestamp Europe/Rome richiesto")
    if index in (0, len(ARTICLES) - 1):
        phrases_path = ROOT / "assets/data/frasi-nome.json"
        phrases = json.loads(phrases_path.read_text(encoding="utf-8"))
        for phrase in ("Un volo si prepara anche verificando le informazioni più recenti.", "La coincidenza più importante è quella con l'informazione giusta.", "Una deviazione conosciuta in anticipo può salvare il viaggio.", "I fatti contano di più delle previsioni sulle loro conseguenze."):
            if phrase not in phrases:
                phrases.append(phrase)
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
                      "last_update": f"mattina-v{VERSION}", "date": published.date().isoformat(),
                      "release_date": published.date().isoformat(), "updated_at": published.isoformat(timespec="seconds"),
                      "status": "ready"})
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"index": index, "slug": slug, "published": published.isoformat()}, ensure_ascii=False))


if __name__ == "__main__":
    main()
