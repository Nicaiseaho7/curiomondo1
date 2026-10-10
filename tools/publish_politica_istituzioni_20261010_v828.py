#!/usr/bin/env python3
"""Release v828: politica e istituzioni italiane ed europee."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import publish_notte_mattina_20261010_v827 as base
from automation.newsroom import site

ROME = ZoneInfo("Europe/Rome")
VERSION = 828

base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "ngs": ROOT.parent / "generated_images/exec-54554a52-deed-48de-83e3-3ce474e31ca0.png",
    "risarcimenti": ROOT.parent / "generated_images/exec-3ca0c63b-3857-4361-81a3-f184fabdd699.png",
    "rinnovabili": ROOT.parent / "generated_images/exec-7b376034-58ce-4705-a30c-75a9b5d8aa13.png",
    "decreto181": ROOT.parent / "generated_images/exec-fabf817f-eeba-48fb-85be-003bd7263368.png",
    "sanzioni": ROOT.parent / "generated_images/exec-aeccf8a6-683f-4d62-8a75-6a4d74f6e3ca.png",
    "terzosettore": ROOT.parent / "generated_images/exec-087d7890-6553-4c4c-9a8e-eca1904d2d9b.png",
    "strade": ROOT.parent / "generated_images/exec-f068a7a3-a0aa-4508-b870-727c89ccd7a0.png",
    "rusecco": ROOT.parent / "generated_images/exec-591e1d7f-907a-49ff-a0e9-dcabda5601a6.png",
    "clima": ROOT.parent / "generated_images/exec-6e386bee-c22c-449c-b007-55fdbfc9d5ce.png",
    "recovery": ROOT.parent / "generated_images/exec-823149ea-6955-48ba-bf68-e947b633fb3d.png",
}

ARTICLES = [
    {
        "slug": "test-ngs-tumore-ovaio-un-milione-regioni-decreto-2026",
        "titolo": "Tumore ovarico, un milione alle Regioni per potenziare i test genomici",
        "sommario": "Il decreto del Ministero della Salute ripartisce le risorse per i test NGS destinati alle pazienti con carcinoma sieroso di alto grado in stadio avanzato.",
        "categoria": "Salute", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["tumore ovarico", "test genomici NGS"],
        "dati_chiave": [{"valore": "1 milione", "etichetta": "risorse da ripartire"}, {"valore": "40 giorni", "etichetta": "termine per i programmi regionali"}, {"valore": "NGS", "etichetta": "tecnologia di profilazione"}],
        "paragrafi": [
            "È stato pubblicato in Gazzetta Ufficiale il decreto che stabilisce come distribuire un milione di euro tra le Regioni per potenziare i test di profilazione genomica NGS nel tumore ovarico.",
            "La misura riguarda in particolare le pazienti con carcinoma sieroso di alto grado dell'ovaio in stadio avanzato. I test multigenici possono aiutare i centri clinici a individuare alterazioni molecolari utili per scegliere terapie mirate già autorizzate.",
            "Il riparto viene calcolato sulla stima delle pazienti eleggibili, usando popolazione femminile residente, incidenza della patologia e disponibilità complessiva del fondo. Le quote precise per ciascun territorio sono contenute nell'allegato al decreto.",
            "Entro quaranta giorni dalla pubblicazione, le Regioni devono presentare al Ministero un programma sull'impiego delle risorse. Il finanziamento serve a rafforzare capacità organizzativa e diagnostica, non introduce automaticamente una nuova prestazione separata dai percorsi clinici.",
            "Il Ministero chiarisce che l'obiettivo è rendere più uniforme l'accesso ai test sul territorio nazionale, per donne residenti e non residenti quando esiste l'indicazione clinica.",
            "Per le pazienti non cambia il criterio medico: l'esame resta deciso dai centri specialistici in base alla diagnosi. Il provvedimento interviene invece sulle risorse regionali necessarie per eseguirlo.",
        ],
        "fonti": [{"url": "https://www.gazzettaufficiale.it/atto/serie_generale/caricaDettaglioAtto/originario?atto.codiceRedazionale=26A05282&atto.dataPubblicazioneGazzetta=2026-10-09&elenco30giorni=false", "nome": "Gazzetta Ufficiale — decreto del Ministero della Salute su criteri e riparto del fondo NGS."}],
        "image_source": "ngs", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di mediche in un laboratorio italiano di profilazione genomica; non è una fotografia documentaria.",
        "image_prompt": "Laboratorio italiano di oncologia molecolare con mediche che esaminano dati genomici; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "risarcimenti-lesioni-gravi-tabelle-nazionali-aggiornate-aprile-2026",
        "titolo": "Risarcimenti per lesioni gravi, aggiornate le tabelle nazionali",
        "sommario": "Il Mimit adegua dal mese di aprile i valori per i danni non patrimoniali da incidenti stradali e responsabilità sanitaria alla variazione Istat del 2,6%.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["risarcimenti", "lesioni gravi"],
        "dati_chiave": [{"valore": "+2,6%", "etichetta": "variazione Istat di riferimento"}, {"valore": "aprile 2026", "etichetta": "decorrenza dell'aggiornamento"}, {"valore": "10-100", "etichetta": "punti di invalidità della tabella"}],
        "paragrafi": [
            "Il Ministero delle Imprese e del Made in Italy ha aggiornato le tabelle nazionali usate per quantificare il danno non patrimoniale nelle lesioni gravi.",
            "La revisione si applica dal mese di aprile 2026 e riguarda la tabella unica nazionale per invalidità comprese tra dieci e cento punti, con valori che variano anche in base all'età della persona danneggiata.",
            "Il decreto interessa i risarcimenti dovuti per sinistri causati dalla circolazione di veicoli e natanti e, attraverso la disciplina collegata, i casi di responsabilità sanitaria cui si applicano gli stessi criteri.",
            "L'adeguamento prende come riferimento l'indice Istat dei prezzi al consumo per le famiglie di operai e impiegati, aumentato del 2,6% tra aprile 2025 e aprile 2026. Il calcolo considera inoltre le tavole di mortalità e il tasso legale dell'1,60%.",
            "La pubblicazione non significa che ogni risarcimento salga automaticamente della stessa cifra finale. L'importo concreto dipende da percentuale di invalidità, età, durata dell'inabilità temporanea e valutazione del singolo caso.",
            "Per pratiche già aperte conviene verificare con assicurazione o professionista quale versione della tabella debba essere applicata, considerando la data del danno e gli atti della procedura.",
        ],
        "fonti": [{"url": "https://www.gazzettaufficiale.it/atto/serie_generale/caricaDettaglioAtto/originario?atto.codiceRedazionale=26A05220&atto.dataPubblicazioneGazzetta=2026-10-09&elenco30giorni=false", "nome": "Gazzetta Ufficiale — decreto Mimit del 28 settembre 2026 sulle tabelle risarcitorie."}],
        "image_source": "risarcimenti",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una consulenza su un risarcimento per lesioni; scena non documentaria.",
        "image_prompt": "Consulenza legale e assicurativa in Italia su risarcimenti per lesioni gravi; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "rinnovabili-decreto-regole-procedure-competitive-contingenti-2026",
        "titolo": "Rinnovabili, aggiornate le regole per le procedure competitive",
        "sommario": "Il Mase pubblica il decreto direttoriale 93 con modalità, contingenti di potenza e coefficienti territoriali per gli impianti vicini alla competitività di mercato.",
        "categoria": "Ambiente", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["rinnovabili", "procedure competitive"],
        "dati_chiave": [{"valore": "n. 93", "etichetta": "decreto direttoriale"}, {"valore": "2 ottobre", "etichetta": "data di adozione"}, {"valore": "9 ottobre", "etichetta": "pubblicazione in Gazzetta"}],
        "paragrafi": [
            "Il Ministero dell'Ambiente e della Sicurezza energetica ha pubblicato il decreto direttoriale numero 93 del 2 ottobre, che aggiorna le regole operative delle procedure competitive per nuovi impianti da fonti rinnovabili.",
            "Il provvedimento disciplina come presentare e valutare le manifestazioni di interesse e le successive richieste di partecipazione. Approva inoltre i contingenti di potenza e i coefficienti locazionali usati nelle procedure.",
            "Il meccanismo è rivolto alle tecnologie rinnovabili con costi di generazione vicini alla competitività di mercato. L'obiettivo è assegnare il sostegno attraverso procedure concorrenziali, entro quantità di potenza definite.",
            "Per gli operatori la novità concreta è documentale e procedurale: prima di candidare un progetto occorre utilizzare le regole aggiornate e controllare il contingente applicabile alla tecnologia e all'area interessata.",
            "La pubblicazione in Gazzetta del 9 ottobre rende disponibile il riferimento ufficiale, mentre il testo integrale e gli allegati sono ospitati sul sito del Mase.",
            "Il decreto non autorizza da solo nuovi impianti e non sostituisce i permessi ambientali e territoriali. Stabilisce invece il quadro per competere nell'accesso al meccanismo di sostegno.",
        ],
        "fonti": [{"url": "https://www.gazzettaufficiale.it/atto/serie_generale/caricaDettaglioAtto/originario?atto.codiceRedazionale=26A05291&atto.dataPubblicazioneGazzetta=2026-10-09&elenco30giorni=false", "nome": "Gazzetta Ufficiale — comunicato Mase sul decreto direttoriale 93 del 2026."}],
        "image_source": "rinnovabili",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di tecnici davanti a impianti solari ed eolici in Italia; scena non documentaria.",
        "image_prompt": "Tecnici esaminano impianti solari ed eolici in un paesaggio italiano; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "decreto-181-comunicazioni-ue-alimenti-rumore-radio-vigore-24-ottobre",
        "titolo": "Comunicazioni tecniche UE, il decreto 181 entra in vigore il 24 ottobre",
        "sommario": "Il provvedimento italiano recepisce la direttiva europea che semplifica alcuni obblighi nei settori degli alimenti irradiati e delle macchine rumorose all'aperto.",
        "categoria": "Politica", "luogo": "Roma", "formato": "flash",
        "parole_chiave_titolo": ["decreto 181", "obblighi di comunicazione UE"],
        "dati_chiave": [{"valore": "24 ottobre", "etichetta": "entrata in vigore"}, {"valore": "4 settori", "etichetta": "ambiti della direttiva UE"}, {"valore": "0", "etichetta": "nuovi oneri pubblici previsti"}],
        "paragrafi": [
            "Il decreto legislativo numero 181 del 2026 è stato pubblicato in Gazzetta Ufficiale e entrerà in vigore il 24 ottobre. Recependo la direttiva UE 2024/2839, elimina alcuni obblighi di comunicazione divenuti superflui.",
            "Gli ambiti richiamati dalla direttiva sono alimenti e ingredienti trattati con radiazioni ionizzanti, emissioni acustiche delle macchine usate all'aperto, diritti dei pazienti e apparecchiature radio.",
            "Nel testo italiano l'intervento operativo abroga una comunicazione prevista dalla disciplina sugli alimenti irradiati e due disposizioni collegate alle informazioni sulle macchine e attrezzature rumorose.",
            "Restano in vigore le regole sostanziali di sicurezza e le sanzioni per prodotti senza dichiarazione di conformità, marcatura CE o indicazione corretta della potenza sonora. I controlli continuano a spettare alle autorità competenti.",
            "Per imprese e amministrazioni l'effetto principale è una riduzione di adempimenti informativi duplicati. Per i consumatori non cambiano né gli obblighi essenziali di etichettatura né le tutele sanitarie e di conformità.",
            "La clausola finanziaria stabilisce che l'attuazione avvenga con le risorse già disponibili e senza nuovi o maggiori costi per la finanza pubblica.",
        ],
        "fonti": [{"url": "https://www.gazzettaufficiale.it/atto/serie_generale/caricaDettaglioAtto/originario?atto.codiceRedazionale=26G00196&atto.dataPubblicazioneGazzetta=2026-10-09&elenco30giorni=false", "nome": "Gazzetta Ufficiale — decreto legislativo 25 settembre 2026 n. 181."}],
        "image_source": "decreto181",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una riunione tecnica su alimenti, rumore, sanità e radio; scena non documentaria.",
        "image_prompt": "Riunione istituzionale italiana su norme tecniche europee, con strumenti dei settori coinvolti; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "ue-sanzioni-attivita-ibride-russia-proroga-9-ottobre-2027",
        "titolo": "Attività ibride russe, l'UE proroga le sanzioni fino a ottobre 2027",
        "sommario": "Il Consiglio mantiene congelamento dei beni, divieto di finanziamento e restrizioni di viaggio per 80 persone e 20 entità accusate di azioni destabilizzanti.",
        "categoria": "Politica", "luogo": "Bruxelles", "formato": "flash",
        "parole_chiave_titolo": ["sanzioni UE", "attività ibride russe"],
        "dati_chiave": [{"valore": "9 ottobre 2027", "etichetta": "nuova scadenza"}, {"valore": "80", "etichetta": "persone designate"}, {"valore": "20", "etichetta": "entità designate"}],
        "paragrafi": [
            "Il Consiglio dell'Unione europea ha prorogato di un anno, fino al 9 ottobre 2027, il regime di misure restrittive contro le attività ibride attribuite alla Russia.",
            "Il quadro sanzionatorio riguarda al momento 80 persone e 20 entità. Per i soggetti inseriti nell'elenco sono previsti congelamento dei beni e divieto per cittadini e imprese dell'UE di mettere a disposizione fondi o risorse economiche.",
            "Alle persone designate si applica anche il divieto di ingresso o transito nel territorio dell'Unione. La proroga non aggiunge automaticamente nuovi nomi: prolunga la validità delle misure già decise.",
            "Il regime è stato creato per colpire campagne di manipolazione dell'informazione, interferenze, operazioni informatiche e altre azioni considerate destabilizzanti contro Stati membri, partner e istituzioni europee.",
            "Per banche e imprese italiane la conseguenza pratica è la prosecuzione degli obblighi di controllo su controparti, pagamenti e beni riconducibili ai soggetti elencati.",
            "Le designazioni possono essere riesaminate e contestate secondo le procedure europee. La decisione politica del Consiglio deve essere letta insieme agli atti giuridici pubblicati nella Gazzetta ufficiale dell'UE.",
        ],
        "fonti": [{"url": "https://www.consilium.europa.eu/en/press/press-releases/2026/10/08/russia-s-hybrid-activities-council-prolongs-restrictive-measures-until-october-2027/", "nome": "Consiglio dell'UE — proroga del regime sulle attività ibride russe."}],
        "image_source": "sanzioni", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un centro europeo di sicurezza informatica; scena non documentaria.",
        "image_prompt": "Centro UE di sicurezza informatica monitora minacce ibride e disinformazione; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "veneto-1694-milioni-65-progetti-terzo-settore-2026",
        "titolo": "Veneto, quasi 1,7 milioni finanziano 65 progetti del Terzo Settore",
        "sommario": "La Giunta scorre la graduatoria dell'avviso 2025: risorse a volontariato, associazioni di promozione sociale e fondazioni per interventi regionali.",
        "categoria": "Politica", "luogo": "Veneto", "formato": "flash",
        "parole_chiave_titolo": ["Veneto", "Terzo Settore"],
        "dati_chiave": [{"valore": "1.694.059 euro", "etichetta": "risorse 2026"}, {"valore": "65", "etichetta": "progetti sostenuti"}, {"valore": "168", "etichetta": "domande ricevute"}],
        "paragrafi": [
            "La Giunta regionale del Veneto ha approvato l'impiego di 1.694.059 euro per finanziare progetti di rilevanza regionale promossi dagli enti del Terzo Settore.",
            "Le risorse arrivano dal Ministero del Lavoro nell'ambito dell'accordo di programma 2025-2027. La Regione utilizzerà l'annualità 2026 per scorrere la graduatoria dell'avviso pubblico pubblicato l'anno scorso.",
            "Saranno sostenuti 63 ulteriori progetti: cinque presentati da fondazioni e 58 da organizzazioni di volontariato o associazioni di promozione sociale. Il provvedimento completa inoltre due contributi che erano stati assegnati solo in parte.",
            "In totale l'avviso aveva ricevuto 168 domande e l'istruttoria ne aveva dichiarate ammissibili 155. Con le risorse del 2025 erano già stati finanziati 52 progetti per circa 1,43 milioni di euro.",
            "Per gli enti interessati non si apre un nuovo bando: il finanziamento riguarda progetti già valutati e collocati in graduatoria. Le strutture beneficiarie dovranno rispettare tempi, attività e rendicontazione previsti dall'avviso.",
            "Gli interventi possono riguardare bisogni sociali, inclusione e servizi di prossimità. I singoli importi e destinatari saranno quelli indicati negli atti applicativi della graduatoria.",
        ],
        "fonti": [{"url": "https://www.regione.veneto.it/article-detail?articleId=14423304", "nome": "Regione Veneto — delibera e dati sui progetti del Terzo Settore."}],
        "image_source": "terzosettore",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di volontari e cittadini in un centro comunitario veneto; scena non documentaria.",
        "image_prompt": "Volontari e cittadini lavorano a progetti sociali in Veneto; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "veneto-mutuo-50-milioni-strade-ponti-sicurezza-2026",
        "titolo": "Veneto, via libera a un mutuo fino a 50 milioni per strade e ponti",
        "sommario": "La Giunta avvia la gara per finanziare manutenzione e sicurezza della rete regionale: 18 milioni alle opere d'arte e 15 milioni ai tratti critici.",
        "categoria": "Politica", "luogo": "Veneto", "formato": "flash",
        "parole_chiave_titolo": ["Veneto", "strade e ponti"],
        "dati_chiave": [{"valore": "50 milioni", "etichetta": "importo massimo"}, {"valore": "20 anni", "etichetta": "durata del mutuo"}, {"valore": "31 dicembre 2028", "etichetta": "termine di utilizzo"}],
        "paragrafi": [
            "La Giunta del Veneto ha autorizzato l'avvio delle procedure per un mutuo fino a 50 milioni di euro destinato alla manutenzione e alla sicurezza della rete viaria regionale.",
            "Il programma assegna 18 milioni a ponti e opere d'arte e 15 milioni all'adeguamento dei tratti considerati più critici. Altri sette milioni sono riservati alla regionale 104 Monselice-Mare.",
            "Quattro milioni andranno alla viabilità bellunese, tre alla messa in sicurezza di versanti e scarpate, due alla regionale 450 di Affi e un milione alla mitigazione acustica.",
            "Il finanziamento avrà durata massima di vent'anni, tasso fisso e rate costanti. La Regione potrà utilizzare le somme in una o più tranche entro il 31 dicembre 2028 e ridurre l'importo se i lavori richiederanno meno risorse.",
            "L'istituto finanziatore sarà scelto con gara telematica sulla base dello spread più basso. Se le condizioni di mercato non saranno migliori, la Regione potrà rivolgersi a Cassa Depositi e Prestiti.",
            "Il via libera non coincide con l'apertura simultanea di tutti i cantieri. Le opere saranno realizzate da Veneto Strade secondo progettazione, affidamenti e cronoprogrammi specifici.",
        ],
        "fonti": [{"url": "https://www.regione.veneto.it/article-detail?articleId=14423245", "nome": "Regione Veneto — decisione sul mutuo e ripartizione degli interventi viari."}],
        "image_source": "strade",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di tecnici che ispezionano un ponte stradale nelle Dolomiti; scena non documentaria.",
        "image_prompt": "Tecnici regionali ispezionano un ponte e un versante stradale in Veneto; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "ru-secco-san-vito-cadore-cinque-milioni-sicurezza-idrogeologica",
        "titolo": "San Vito di Cadore, oltre 5 milioni per mettere in sicurezza il Ru Secco",
        "sommario": "La Regione Veneto finanzia briglie, adeguamenti idraulici e manutenzione nel bacino ai piedi dell'Antelao, interessato in passato da colate detritiche.",
        "categoria": "Politica", "luogo": "San Vito di Cadore", "formato": "flash",
        "parole_chiave_titolo": ["Ru Secco", "sicurezza idrogeologica"],
        "dati_chiave": [{"valore": "oltre 5 milioni", "etichetta": "investimento complessivo"}, {"valore": "551.000 euro", "etichetta": "manutenzione straordinaria"}, {"valore": "5", "etichetta": "interventi su opere esistenti"}],
        "paragrafi": [
            "La Regione Veneto ha fatto il punto su oltre cinque milioni di euro di interventi per la sicurezza idrogeologica del bacino del Ru Secco, a San Vito di Cadore.",
            "La parte principale, pari a 4.444.473 euro, è stata finanziata dopo la tempesta Vaia e con il piano triennale dei lavori pubblici. Si aggiungono 551 mila euro per la manutenzione straordinaria di opere idraulico-forestali esistenti.",
            "I lavori comprendono briglie capaci di trattenere il materiale, un bacino di invaso, un nuovo canale lungo 75 metri e interventi vicino all'attraversamento della statale 51 di Alemagna.",
            "Cinque opere costruite tra gli anni Sessanta e Ottanta sono state consolidate o adeguate. Una briglia aveva richiesto un ripristino anche dopo gli eventi del novembre 2024.",
            "Il Ru Secco scende da un bacino ripido ai piedi dell'Antelao e può trasportare grandi quantità di detriti. Per questo le strutture di contenimento servono a proteggere abitato e viabilità, non soltanto a regolare il corso d'acqua.",
            "La Regione segnala cantieri programmati e manutenzioni già finanziate; non si tratta di un'allerta in corso. Eventuali avvisi per residenti e viabilità restano di competenza delle autorità locali e della Protezione civile.",
        ],
        "fonti": [{"url": "https://www.regione.veneto.it/article-detail?articleId=14420266", "nome": "Regione Veneto — quadro finanziario e tecnico degli interventi sul Ru Secco."}],
        "image_source": "rusecco",
        "image_alt": "Illustrazione editoriale IA ultrarealistica delle opere idrauliche sul Ru Secco nelle Dolomiti; scena non documentaria.",
        "image_prompt": "Opere di contenimento e tecnici sul Ru Secco a San Vito di Cadore; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "ecofin-finanza-climatica-300-miliardi-anno-2035-cop31",
        "titolo": "Clima, l'UE conferma l'obiettivo globale di 300 miliardi l'anno entro il 2035",
        "sommario": "I ministri delle Finanze approvano le conclusioni per la COP31 e chiedono ai Paesi con capacità economica di aumentare i contributi destinati alle economie in via di sviluppo.",
        "categoria": "Politica", "luogo": "Bruxelles", "formato": "flash",
        "parole_chiave_titolo": ["finanza climatica", "300 miliardi"],
        "dati_chiave": [{"valore": "300 miliardi $", "etichetta": "obiettivo annuo globale"}, {"valore": "2035", "etichetta": "orizzonte dell'impegno"}, {"valore": "9-20 novembre", "etichetta": "date della COP31"}],
        "paragrafi": [
            "Il Consiglio Ecofin ha approvato la posizione dell'Unione europea sulla finanza climatica in vista della COP31, in programma ad Antalya dal 9 al 20 novembre.",
            "I ministri hanno riaffermato l'impegno a contribuire all'obiettivo collettivo globale di mobilitare 300 miliardi di dollari ogni anno entro il 2035 per i Paesi in via di sviluppo.",
            "Le conclusioni chiedono a tutti gli Stati con capacità finanziaria di aumentare lo sforzo. L'UE sottolinea di essere, insieme ai suoi Paesi membri, il maggiore contributore alla finanza climatica internazionale.",
            "L'importo di 300 miliardi non è un nuovo fondo europeo già stanziato integralmente. È un obiettivo collettivo internazionale che può comprendere risorse pubbliche, strumenti multilaterali e capitale privato mobilitato.",
            "Per l'Italia le decisioni operative passeranno attraverso bilancio nazionale, fondi europei e accordi internazionali. Le conclusioni del Consiglio definiscono la posizione negoziale, ma non sostituiscono gli atti di spesa.",
            "Il dossier sarà discusso alla COP31 insieme a mitigazione, adattamento e perdite climatiche. Gli impegni concreti dei singoli Paesi dovranno essere verificati dopo la conferenza.",
        ],
        "fonti": [{"url": "https://www.consilium.europa.eu/en/meetings/ecofin/2026/10/09/", "nome": "Consiglio dell'UE — risultati Ecofin del 9 ottobre 2026 sulla finanza climatica."}],
        "image_source": "clima",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una riunione dei ministri finanziari europei sul clima; scena non documentaria.",
        "image_prompt": "Ministri finanziari UE discutono di finanza climatica a Bruxelles; logo CurioMondo circolare applicato in post-produzione.",
    },
    {
        "slug": "recovery-facility-fase-finale-440-miliardi-pagamenti-dicembre-2026",
        "titolo": "Recovery europeo alla fase finale: erogati circa 440 miliardi",
        "sommario": "L'Ecofin fa il punto sul dispositivo post-pandemia: obiettivi nazionali completati entro agosto e ultimi pagamenti della Commissione entro dicembre 2026.",
        "categoria": "Politica", "luogo": "Bruxelles", "formato": "flash",
        "parole_chiave_titolo": ["Recovery europeo", "440 miliardi"],
        "dati_chiave": [{"valore": "circa 440 miliardi", "etichetta": "risorse erogate finora"}, {"valore": "agosto 2026", "etichetta": "termine per traguardi e obiettivi"}, {"valore": "dicembre 2026", "etichetta": "termine per i pagamenti"}],
        "paragrafi": [
            "Il dispositivo europeo per la ripresa e la resilienza è entrato nella fase conclusiva. Al Consiglio Ecofin del 9 ottobre i ministri hanno fatto il punto su attuazione e pagamenti.",
            "Secondo il Consiglio, sono stati erogati finora circa 440 miliardi di euro agli Stati membri. Il fondo ha sostenuto riforme e investimenti nazionali nati dopo la pandemia, compreso il PNRR italiano.",
            "I Paesi dovevano completare traguardi e obiettivi previsti dai piani entro la fine di agosto 2026. La Commissione ha invece tempo fino alla fine di dicembre per effettuare gli ultimi versamenti dopo le verifiche.",
            "La scadenza non garantisce automaticamente il pagamento di ogni somma richiesta. Ogni rata dipende dalla valutazione della Commissione sull'effettivo raggiungimento degli impegni concordati.",
            "Per l'Italia questa fase concentra l'attenzione sulla documentazione finale, sui controlli e sulla chiusura amministrativa degli interventi. Eventuali importi specifici devono essere distinti dal totale europeo comunicato dall'Ecofin.",
            "Dopo dicembre continueranno rendicontazione, audit e gestione delle opere finanziate. A chiudersi è la finestra dei pagamenti del dispositivo, non necessariamente tutti i cantieri collegati.",
        ],
        "fonti": [{"url": "https://www.consilium.europa.eu/en/meetings/ecofin/2026/10/09/", "nome": "Consiglio dell'UE — stato di attuazione del Recovery and Resilience Facility."}],
        "image_source": "recovery",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di funzionari europei che verificano progetti del Recovery; scena non documentaria.",
        "image_prompt": "Funzionari UE esaminano progetti ferroviari, digitali ed energetici finanziati dal Recovery; logo CurioMondo circolare applicato in post-produzione.",
    },
]


def append_name_phrases() -> None:
    path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        "Una cura più precisa comincia da strumenti accessibili in ogni territorio.",
        "Una regola chiara rende più leggibile anche il momento più difficile.",
        "La transizione energetica diventa reale quando procedure e responsabilità sono definite.",
        "Semplificare un adempimento ha senso soltanto se le tutele restano intatte.",
        "La sicurezza comune dipende anche dalla capacità di riconoscere le minacce invisibili.",
        "Il volontariato trasforma risorse limitate in legami che durano.",
        "Prendersi cura di una strada significa proteggere ogni viaggio quotidiano.",
        "La prevenzione migliore lavora prima che la montagna mostri la sua forza.",
        "Gli impegni sul clima contano quando diventano risorse verificabili.",
        "Un grande piano si misura non solo dai fondi, ma dai risultati che lascia.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    append_name_phrases()
    base_time = datetime.now(ROME).replace(microsecond=0)
    minute_offsets = (0, 8, 19, 33, 48, 65, 82, 100, 117, 135)
    images, written = [], []
    for article, minutes in zip(ARTICLES, minute_offsets):
        image = base.make_image(article)
        slug = site.write_article(article, image, VERSION)
        published = base_time - timedelta(minutes=minutes)
        base.set_published(slug, published)
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
        "site_version": VERSION, "currentVersion": VERSION, "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": f"politica-istituzioni-v{VERSION}", "date": base_time.date().isoformat(),
        "release_date": base_time.date().isoformat(), "updated_at": base_time.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base_time.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
