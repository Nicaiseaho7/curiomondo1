#!/usr/bin/env python3
"""Release v829: economia utile e sport del 10 ottobre 2026."""
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
VERSION = 829

base.VERSION = VERSION
base.IMAGE_SOURCES = {
    "aspettative": ROOT.parent / "generated_images/exec-9db433f2-830a-491e-8a96-a5948ace4b18.png",
    "imprese": ROOT.parent / "generated_images/exec-4e6f80ca-6b62-45b1-93e5-15cf8cb6af15.png",
    "asili": ROOT.parent / "generated_images/exec-5d64ea5d-0114-49ae-9dda-b9fc14d56402.png",
    "consob": ROOT.parent / "generated_images/exec-25d1173b-1f08-4802-a8ec-83b8f80dfa29.png",
    "inflazione": ROOT.parent / "generated_images/exec-3714a787-dc69-4204-b81c-7ba64277dd85.png",
    "motogp": ROOT.parent / "generated_images/exec-d0ab2f1f-7106-48c9-9476-1aca6dfcaaf1.png",
    "f1": ROOT.parent / "generated_images/exec-6b582980-731b-4b99-83a2-de43f867378d.png",
    "tennis": ROOT.parent / "generated_images/exec-a60f5294-0daf-4edb-a52e-65c244dce83e.png",
    "azzurre": ROOT.parent / "generated_images/exec-c82ef89e-e290-48ca-a255-17506863a1bb.png",
    "gravel": ROOT.parent / "generated_images/exec-df2b5f77-864d-41ec-9235-df0a2e64058e.png",
}

ARTICLES = [
    {
        "slug": "imprese-italiane-quarto-trimestre-costi-materie-prime-10-10-2026",
        "titolo": "Imprese italiane, quarto trimestre ancora difficile: pesano le materie prime",
        "sommario": "L'indagine della Banca d'Italia rileva attese ancora sfavorevoli, ma una domanda complessivamente positiva. Le aziende prevedono nuovi rincari dei listini.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["imprese italiane", "materie prime"],
        "dati_chiave": [{"valore": "25 ago-18 set", "etichetta": "periodo dell'indagine"}, {"valore": "50+", "etichetta": "addetti delle imprese coinvolte"}, {"valore": "4° trimestre", "etichetta": "orizzonte ancora sfavorevole"}],
        "paragrafi": [
            "Le imprese italiane affrontano l'ultimo trimestre del 2026 con un quadro ancora difficile. La nuova indagine della Banca d'Italia segnala che il giudizio sulle condizioni generali resta negativo, pur essendosi attenuato rispetto alla rilevazione precedente.",
            "Il sondaggio è stato condotto tra il 25 agosto e il 18 settembre tra aziende dell'industria e dei servizi con almeno 50 addetti. Le risposte fotografano quindi aspettative aziendali, non una previsione ufficiale del prodotto interno lordo.",
            "La domanda complessiva viene valutata in modo positivo grazie soprattutto alla componente estera, mentre quella interna appare più debole. Le tensioni internazionali incidono soprattutto sui costi degli input e meno sugli ordini.",
            "Per il quarto trimestre le attese operative restano sfavorevoli. Le imprese prevedono comunque una crescita dell'occupazione, anche se leggermente più lenta, e mantengono programmi di investimento nel complesso espansivi.",
            "Il punto più sensibile per famiglie e consumatori riguarda i prezzi. Molte aziende si aspettano di aumentare i propri listini, indicando tra le cause principali l'aumento delle materie prime e degli altri costi di produzione.",
            "Il quadro non implica rincari identici in ogni settore. Mostra però che la pressione a monte della filiera resta elevata e può trasferirsi gradualmente sui prezzi finali, con effetti diversi secondo concorrenza e domanda.",
        ],
        "fonti": [{"url": "https://www.bancaditalia.it/media/notizia/indagine-sulle-aspettative-di-inflazione-e-crescita-3-trimestre-2026/", "nome": "Banca d'Italia — indagine sulle aspettative di inflazione e crescita del terzo trimestre 2026."}],
        "image_source": "aspettative",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di imprenditori italiani che esaminano costi e ordini; scena non documentaria.",
        "image_prompt": "Imprenditori italiani in una piccola fabbrica analizzano ordini, materie prime e costi; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "imprese-straniere-italia-677mila-saldo-positivo-2026",
        "titolo": "Imprese straniere in Italia, saldo positivo di oltre 16 mila in sei mesi",
        "sommario": "Unioncamere conta 677.188 attività guidate da persone nate all'estero a fine giugno. Rappresentano il 12% del tessuto imprenditoriale nazionale.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["imprese straniere", "saldo positivo"],
        "dati_chiave": [{"valore": "677.188", "etichetta": "imprese registrate"}, {"valore": "+16.097", "etichetta": "saldo del semestre"}, {"valore": "12%", "etichetta": "quota sul totale"}],
        "paragrafi": [
            "Le imprese guidate da persone nate all'estero continuano a crescere in Italia. Al 30 giugno 2026 Unioncamere ne registra 677.188, pari al 12% di tutte le attività presenti nel Paese.",
            "Nel primo semestre sono nate 37.140 imprese e ne sono cessate 21.043, al netto delle cancellazioni d'ufficio. Il saldo è quindi positivo per 16.097 unità.",
            "Il 79% delle attività fa capo a imprenditori provenienti da Paesi esterni all'Unione europea. Il dato comprende imprese individuali e società, con una presenza importante nel commercio, nelle costruzioni e nei servizi.",
            "La crescita non riguarda soltanto iniziative appena avviate. Alla fine del 2025 circa il 35% delle imprese straniere aveva superato i dieci anni di attività, un segnale di progressivo consolidamento.",
            "I numeri sono utili anche per leggere lavoro e consumi: più imprese significano occupazione, contributi e domanda di servizi professionali, ma non dicono da soli quanto siano produttive o solide finanziariamente.",
            "Unioncamere usa la nazionalità di nascita delle persone con cariche o quote di controllo per classificare le attività. Per confronti territoriali e settoriali va quindi considerata la definizione statistica adottata.",
        ],
        "fonti": [{"url": "https://unioncamere.gov.it/comunicazione-istituzionale-il-sistema-camerale/comunicati-stampa/imprese-straniere-italia-al-30-giugno-sono-677mila", "nome": "Unioncamere — dati Movimprese sulle attività a guida straniera al 30 giugno 2026."}],
        "image_source": "imprese",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di titolari di piccole imprese in una via commerciale italiana; scena non documentaria.",
        "image_prompt": "Titolari di diverse origini davanti a piccole attività in una via commerciale italiana riconoscibile; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "inps-mappa-asili-nido-servizi-famiglie-portale-2026",
        "titolo": "Asili nido, l'INPS attiva la mappa nazionale delle strutture autorizzate",
        "sommario": "Nel Portale della famiglia è disponibile un servizio per localizzare nidi e strutture educative da zero a tre anni. L'accesso richiede identità digitale.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["asili nido", "mappa INPS"],
        "dati_chiave": [{"valore": "0-3 anni", "etichetta": "fascia dei servizi educativi"}, {"valore": "4", "etichetta": "sistemi di accesso digitale"}, {"valore": "9 ottobre", "etichetta": "annuncio INPS"}],
        "paragrafi": [
            "L'INPS ha aggiunto al Portale della famiglia una mappa nazionale per cercare asili nido e altre strutture educative autorizzate destinate ai bambini da zero a tre anni.",
            "Il servizio permette di individuare le strutture presenti sul territorio e consultarne le informazioni disponibili. La banca dati sarà aggiornata progressivamente, quindi una struttura autorizzata potrebbe non comparire subito.",
            "Nel portale sono state raccolte anche le mappe dei centri per le famiglie e le informazioni su alcuni bandi di welfare rivolti agli iscritti a specifiche gestioni creditizie e sociali pubbliche.",
            "La sezione statistica riunisce inoltre dati su assegno unico, bonus nido, bonus nuovi nati e bonus mamme. Non sostituisce però la domanda per ottenere le singole prestazioni.",
            "Per entrare nell'area personale servono SPID di livello 2, Carta d'identità elettronica di livello 3, Carta nazionale dei servizi oppure un'identità eIDAS riconosciuta.",
            "La mappa può aiutare le famiglie a orientarsi, ma disponibilità dei posti, rette e graduatorie restano gestite dai Comuni o dalle singole strutture. Prima dell'iscrizione occorre quindi verificare direttamente requisiti e scadenze.",
        ],
        "fonti": [{"url": "https://www.inps.it/it/it/inps-comunica/notizie/dettaglio-news-page.news.2026.10.portale-della-famiglia-disponibili-nuove-funzionalit.html", "nome": "INPS — nuove funzionalità del Portale della famiglia e accesso alla mappa degli asili."}],
        "image_source": "asili",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di genitori che consultano la mappa degli asili nido; scena non documentaria.",
        "image_prompt": "Genitori italiani consultano su tablet una mappa di asili nido davanti a una struttura educativa; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "consob-oscura-quattro-siti-finanziari-1838-ottobre-2026",
        "titolo": "Consob oscura altri quattro siti finanziari abusivi: totale a 1.838",
        "sommario": "L'Autorità ordina ai provider italiani di bloccare nuove piattaforme non autorizzate. Attenzione a offerte su trading, investimenti e criptoattività.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Consob", "siti finanziari abusivi"],
        "dati_chiave": [{"valore": "4", "etichetta": "nuovi siti oscurati"}, {"valore": "1.838", "etichetta": "totale da luglio 2019"}, {"valore": "2019", "etichetta": "avvio del potere di blocco"}],
        "paragrafi": [
            "Consob ha ordinato l'oscuramento di altri quattro siti che offrivano servizi finanziari senza la necessaria autorizzazione. I provider italiani devono impedirne l'accesso dalla rete nazionale.",
            "Con l'ultimo intervento sale a 1.838 il numero complessivo dei siti bloccati da luglio 2019, quando l'Autorità ha ottenuto il potere di disporre l'inibizione delle piattaforme abusive.",
            "Il blocco tecnico può richiedere alcuni giorni e non garantisce il recupero del denaro già trasferito. I gestori possono inoltre cambiare dominio o ripresentarsi con nomi simili.",
            "Prima di inviare fondi per trading, valute, contratti derivati o criptoattività è utile controllare che l'intermediario compaia negli albi ufficiali e che il dominio sia davvero quello dichiarato.",
            "Rendimenti garantiti, pressioni a versare subito e richieste di altri pagamenti per sbloccare un prelievo sono segnali di rischio. Anche una piattaforma curata graficamente può essere priva di autorizzazione.",
            "Chi teme una frode dovrebbe interrompere nuovi versamenti, conservare chat e ricevute, contattare rapidamente banca o gestore della carta e presentare una segnalazione alle autorità competenti.",
        ],
        "fonti": [{"url": "https://www.consob.it/web/consob/w/occhio-alle-truffe-abusivismo-finanziario-consob-oscura-4-siti-internet%C2%A0?p_l_back_url=%2Fweb%2Fconsob%2Fsearch&p_l_back_url_title=Search", "nome": "Consob — provvedimento del 9 ottobre 2026 sull'oscuramento di quattro siti abusivi."}],
        "image_source": "consob", "image_sensitive": True,
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un controllo su piattaforme finanziarie online; scena non documentaria.",
        "image_prompt": "Analista italiana di sicurezza finanziaria controlla siti di trading sospetti su schermi senza marchi; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "inflazione-settembre-2026-4-2-energia-carrello-spesa",
        "titolo": "Inflazione al 4,2% a settembre: energia e spese frequenti accelerano",
        "sommario": "La stima Istat indica un deciso aumento dei prezzi rispetto ad agosto. Il carrello della spesa sale meno dell'indice generale, mentre pesa soprattutto l'energia.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["inflazione", "4,2%"],
        "dati_chiave": [{"valore": "+4,2%", "etichetta": "variazione annua NIC"}, {"valore": "+0,7%", "etichetta": "variazione mensile"}, {"valore": "+5,3%", "etichetta": "acquisti frequenti"}],
        "paragrafi": [
            "L'inflazione italiana è salita al 4,2% su base annua a settembre, secondo la stima preliminare dell'Istat. Ad agosto il tasso era al 3,3%, mentre rispetto al mese precedente i prezzi aumentano dello 0,7%.",
            "La spinta principale arriva dall'energia: i prezzi dei beni regolamentati crescono del 25,9% su base annua e quelli non regolamentati del 22,2%. Accelerano anche gli alimentari freschi, al 5,5%.",
            "L'inflazione di fondo, calcolata senza energia e alimentari freschi, sale dall'1,5% all'1,7%. Questo indica che l'aumento più forte resta concentrato nelle componenti volatili.",
            "Per le famiglie conta soprattutto la frequenza delle spese. I prodotti acquistati più spesso registrano un aumento annuo del 5,3%, mentre il cosiddetto carrello della spesa cresce dell'1,7%.",
            "L'indice armonizzato europeo IPCA è stimato al 4,1%. L'inflazione acquisita per l'intero 2026, cioè quella che si avrebbe con prezzi fermi fino a dicembre, è pari al 3,1%.",
            "I dati sono provvisori e potranno essere rivisti con la pubblicazione definitiva. Per mutui, stipendi e pensioni non determinano da soli un adeguamento immediato, ma influenzano potere d'acquisto, tassi e future rivalutazioni.",
        ],
        "fonti": [{"url": "https://www.istat.it/comunicato-stampa/prezzi-al-consumo-dati-provvisori-settembre-2026/", "nome": "Istat — stima preliminare dei prezzi al consumo di settembre 2026."}],
        "image_source": "inflazione",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una famiglia italiana che controlla prezzi e bollette; scena non documentaria.",
        "image_prompt": "Famiglia italiana confronta scontrino, spesa alimentare e bolletta energetica in cucina; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "marc-marquez-vince-sprint-mandalika-leader-mondiale-10-10-2026",
        "titolo": "Márquez vince la Sprint di Mandalika e torna leader per quattro punti",
        "sommario": "Il pilota Ducati approfitta di una gara movimentata e precede Ogura e Di Giannantonio. Martín chiude quarto; domenica il GP alle 9 italiane.",
        "categoria": "Sport", "luogo": "Mandalika", "formato": "flash",
        "parole_chiave_titolo": ["Márquez", "Sprint Mandalika"],
        "dati_chiave": [{"valore": "1°", "etichetta": "Marc Márquez"}, {"valore": "+4", "etichetta": "vantaggio mondiale su Martín"}, {"valore": "09:00", "etichetta": "GP di domenica in Italia"}],
        "paragrafi": [
            "Marc Márquez ha vinto la Sprint del Gran Premio d'Indonesia a Mandalika e ha ripreso la testa del Mondiale MotoGP. Il pilota Ducati ora precede Jorge Martín di quattro punti.",
            "Ai Ogura ha chiuso secondo e Fabio Di Giannantonio terzo. Martín, dopo essere stato al comando, è scivolato indietro e ha terminato al quarto posto limitando i danni in classifica.",
            "La gara è cambiata già alla prima curva, dove Raúl Fernández e Marco Bezzecchi sono caduti. Entrambi sono stati indicati in condizioni fisiche rassicuranti dopo l'incidente.",
            "Il risultato della Sprint assegna punti ma non modifica la griglia della gara lunga. La sfida principale del Gran Premio resta in programma domenica 11 ottobre alle 9:00, ora italiana.",
            "In Italia l'evento è disponibile attraverso i servizi indicati dal promotore e dagli operatori titolari dei diritti; il VideoPass ufficiale MotoGP trasmette le sessioni in streaming per gli abbonati.",
            "Con un margine di soli quattro punti, la gara di domenica può cambiare di nuovo il leader del campionato. Strategia gomme, temperatura e gestione della prima curva saranno decisive.",
        ],
        "fonti": [{"url": "https://www.motogp.com/en/news/2026/10/10/marc-marquez-wins-dramatic-mandalika-sprint-martin-loses-the-lead-after-rollercoaster-ride-to-fourth/1174849", "nome": "MotoGP — resoconto ufficiale e classifica della Sprint di Mandalika."}],
        "image_source": "motogp", "image_likeness": "Marc Márquez", "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di Marc Márquez in pista a Mandalika; non è una fotografia della Sprint.",
        "image_prompt": "Marc Márquez in tuta Ducati festeggia dopo una gara a Mandalika, ritratto ultrarealistico e non documentario; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "verstappen-vince-sprint-singapore-pioggia-qualifiche-10-10-2026",
        "titolo": "Verstappen vince la Sprint bagnata di Singapore: Hamilton secondo",
        "sommario": "Partenza rinviata per il temporale e gara caotica a Marina Bay. Leclerc completa il podio; le qualifiche del GP sono previste alle 15 italiane.",
        "categoria": "Sport", "luogo": "Singapore", "formato": "flash",
        "parole_chiave_titolo": ["Verstappen", "Sprint Singapore"],
        "dati_chiave": [{"valore": "1°", "etichetta": "Max Verstappen"}, {"valore": "2°", "etichetta": "Lewis Hamilton"}, {"valore": "15:00", "etichetta": "qualifiche in Italia"}],
        "paragrafi": [
            "Max Verstappen ha vinto la Sprint del Gran Premio di Singapore dopo una partenza ritardata di oltre mezz'ora dalla pioggia intensa. Lewis Hamilton ha chiuso secondo e Charles Leclerc terzo.",
            "George Russell era riuscito a superare Verstappen al via, ma ha perso il controllo della Mercedes sul fondo bagnato ed è finito contro le barriere. Il pilota Red Bull ha così ripreso il comando.",
            "La gara corta è stata segnata da numerosi ritiri e interventi della safety car. Nel finale anche le due McLaren di Lando Norris e Oscar Piastri sono entrate in contatto.",
            "Il programma prosegue oggi con le qualifiche del Gran Premio alle 15:00 italiane. La gara è fissata per domenica 11 ottobre alle 14:00.",
            "Sky trasmette il fine settimana in diretta su Sky Sport F1, Sky Sport Uno e Sky Sport 4K, oltre allo streaming su NOW. Eventuali variazioni dovute al meteo saranno comunicate dagli organizzatori.",
            "Il risultato della Sprint assegna punti separati e non determina la griglia della gara domenicale. Le qualifiche restano quindi decisive per stabilire l'ordine di partenza del Gran Premio.",
        ],
        "fonti": [{"url": "https://www.formula1.com/en/racing/2026/singapore", "nome": "Formula 1 — programma ufficiale, aggiornamenti e risultati del GP di Singapore."}, {"url": "https://sport.sky.it/formula-1/2026/10/09/f1-orari-gp-singapore-2026-marina-bay", "nome": "Sky Sport — orari italiani e canali televisivi del fine settimana."}],
        "image_source": "f1", "image_likeness": "Max Verstappen", "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di Max Verstappen nella Sprint bagnata di Singapore; non è una fotografia dell'evento.",
        "image_prompt": "Max Verstappen guida sul circuito cittadino bagnato di Singapore, ritratto ultrarealistico e scena non documentaria; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "arnaldi-eliminato-fritz-darderi-tsitsipas-shanghai-10-10-2026",
        "titolo": "Shanghai, Arnaldi eliminato da Fritz: Darderi sfida Tsitsipas",
        "sommario": "Il ligure perde 7-5, 6-4 e accusa un fastidio alla spalla destra. L'altro azzurro è nel quarto match del programma su Sky Sport Tennis.",
        "categoria": "Sport", "luogo": "Shanghai", "formato": "flash",
        "parole_chiave_titolo": ["Arnaldi", "Darderi-Tsitsipas"],
        "dati_chiave": [{"valore": "7-5, 6-4", "etichetta": "risultato Arnaldi-Fritz"}, {"valore": "2 ore", "etichetta": "durata approssimativa"}, {"valore": "canale 203", "etichetta": "Sky Sport Tennis"}],
        "paragrafi": [
            "Matteo Arnaldi è stato eliminato al secondo turno del Masters 1000 di Shanghai da Taylor Fritz. Lo statunitense ha vinto 7-5, 6-4 in poco meno di due ore.",
            "Il primo set è rimasto in equilibrio fino all'undicesimo gioco, quando Fritz ha ottenuto il break decisivo. Nel secondo Arnaldi ha recuperato uno svantaggio iniziale, ma non è riuscito a mantenere il ritmo.",
            "L'azzurro ha accusato un fastidio alla spalla destra dopo una breve interruzione per la pioggia. Il problema ha ridotto la fluidità del dritto nella parte finale dell'incontro.",
            "Il programma italiano continua con Luciano Darderi contro Stefanos Tsitsipas. La partita è il quarto incontro sul Grandstand 2 dopo l'avvio della sessione alle 6:00 italiane, quindi l'orario effettivo dipende dalla durata dei match precedenti.",
            "La sfida di Darderi è trasmessa su Sky Sport Tennis, canale 203, e in streaming su NOW. Le piattaforme Sky Sport Plus ed Extra Match permettono di seguire anche i campi aggiuntivi.",
            "Nel programma odierno figura anche Carlos Alcaraz contro Juan Manuel Cerundolo alle 12:00 italiane su Sky Sport Arena. Gli orari possono slittare per pioggia o incontri più lunghi del previsto.",
        ],
        "fonti": [{"url": "https://sport.sky.it/tennis/2026/10/10/arnaldi-fritz-atp-shanghai-2026-risultato", "nome": "Sky Sport — risultato e cronaca di Arnaldi-Fritz."}, {"url": "https://sport.sky.it/tennis/2026/10/10/atp-shanghai-2026-partite-oggi-10-ottobre", "nome": "Sky Sport — programma, orari e copertura televisiva del 10 ottobre."}],
        "image_source": "tennis", "image_likeness": "Matteo Arnaldi e Luciano Darderi", "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica di Matteo Arnaldi e Luciano Darderi sui campi di Shanghai; non è una foto dei match.",
        "image_prompt": "Matteo Arnaldi e Luciano Darderi su campi da tennis professionali a Shanghai, ritratti ultrarealistici e non documentari; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "italia-bielorussia-femminile-2-0-playoff-mondiali-ritorno-firenze",
        "titolo": "Italia femminile, 2-0 alla Bielorussia: ritorno martedì al Franchi",
        "sommario": "Piemonte e Polli firmano il successo nell'andata dei play-off mondiali. La seconda sfida si gioca a Firenze con biglietti in vendita su Vivaticket.",
        "categoria": "Sport", "luogo": "Tbilisi", "formato": "flash",
        "parole_chiave_titolo": ["Italia femminile", "2-0 Bielorussia"],
        "dati_chiave": [{"valore": "2-0", "etichetta": "risultato dell'andata"}, {"valore": "68'", "etichetta": "gol di Piemonte"}, {"valore": "13 ottobre", "etichetta": "ritorno a Firenze"}],
        "paragrafi": [
            "L'Italia femminile ha battuto 2-0 la Bielorussia a Tbilisi nell'andata del primo turno dei play-off per il Mondiale 2027. Le reti sono arrivate nella ripresa con Martina Piemonte ed Elisa Polli.",
            "Piemonte ha sbloccato la partita al 68° minuto dopo un primo tempo dominato dalle Azzurre ma senza gol. Polli ha firmato il raddoppio nel recupero, trovando la sua prima rete con la Nazionale maggiore.",
            "Il ritorno è in programma martedì 13 ottobre allo stadio Artemio Franchi di Firenze. L'Italia parte con due reti di vantaggio, ma il passaggio del turno sarà deciso dal risultato complessivo delle due gare.",
            "I biglietti sono in vendita attraverso il portale ticketing della FIGC e le agenzie Vivaticket. Sono previste riduzioni per Under 20, Over 65, studenti universitari e abbonati della Fiorentina.",
            "Elisa Bartoli non fa parte del gruppo per un lieve problema muscolare; il commissario tecnico Andrea Soncin aveva convocato al suo posto Michela Giordano, già impegnata nel raduno dell'Under 23.",
            "Superando la Bielorussia, le Azzurre affronterebbero nel secondo e decisivo spareggio la vincente tra Finlandia e Serbia. Soltanto quel confronto assegnerebbe il posto al Mondiale in Brasile.",
        ],
        "fonti": [{"url": "https://www.figc.it/it", "nome": "FIGC — risultato ufficiale, programma del ritorno e informazioni sui biglietti."}, {"url": "https://www.rainews.it/maratona/2026/10/calcio-mondiali-donne-playoff-italia-bielorussia-andata-ritorno-diretta-su-rainewsit-aggiornamenti-news-live-video-0521f09f-1b6b-469b-b9c4-f9306052d27e.html", "nome": "RaiNews — cronaca, marcatrici e scenario dei play-off."}],
        "image_source": "azzurre", "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica delle Azzurre dopo la vittoria sulla Bielorussia; non è una fotografia della partita.",
        "image_prompt": "Calciatrici della Nazionale italiana festeggiano in campo dopo una vittoria, scena ultrarealistica non documentaria; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
    {
        "slug": "mondiali-gravel-nannup-2026-programma-percorsi-italiani",
        "titolo": "Mondiali gravel a Nannup: donne oggi, uomini domenica su percorsi durissimi",
        "sommario": "Prima edizione iridata fuori dall'Europa, con oltre l'80% di sterrato. Le élite affrontano 125,6 e 144 chilometri sulle salite dell'Australia occidentale.",
        "categoria": "Sport", "luogo": "Nannup", "formato": "flash",
        "parole_chiave_titolo": ["Mondiali gravel", "Nannup"],
        "dati_chiave": [{"valore": "125,6 km", "etichetta": "gara élite donne"}, {"valore": "144 km", "etichetta": "gara élite uomini"}, {"valore": "oltre 80%", "etichetta": "tracciato sterrato"}],
        "paragrafi": [
            "I Mondiali UCI gravel si disputano questo fine settimana a Nannup, nell'Australia occidentale. È la prima edizione della rassegna organizzata fuori dall'Europa.",
            "La gara élite femminile è in programma oggi su 125,6 chilometri con 3.179 metri di dislivello. Domenica tocca agli uomini, chiamati ad affrontare 144 chilometri e 3.713 metri di salita.",
            "Oltre l'80% di ogni percorso è su sterrato. Dopo una prima sezione asfaltata di nove chilometri, si susseguono strade larghe, salite da uno a tre chilometri e brevi tratti utili per rifornirsi e ricompattarsi.",
            "La parte più dura è concentrata anche nel finale: tutti i percorsi terminano con un anello meridionale di 24,5 chilometri e l'ultima vetta arriva a soli 3,5 chilometri dall'arrivo.",
            "Il programma completo, le liste di partenza e i risultati ufficiali sono pubblicati nell'hub UCI della manifestazione. Per l'Italia, l'orario locale australiano richiede di controllare con attenzione il fuso prima di seguire gli aggiornamenti in diretta.",
            "La competizione usa parte del tracciato della SEVEN Gravel Race, prova già inserita nelle World Series. Il fondo selettivo e il dislivello rendono il Mondiale più vicino a una classica di montagna che a una gara pianeggiante su ghiaia.",
        ],
        "fonti": [{"url": "https://www.uci.org/race-hub/2026-uci-gravel-world-championships/1qcmx5mDsNfbA3Hf1X2noi", "nome": "UCI — hub ufficiale dei Mondiali gravel 2026."}, {"url": "https://gravelchampswesternaustralia.com/courses/", "nome": "Organizzazione Nannup 2026 — distanze, dislivelli e caratteristiche dei percorsi."}],
        "image_source": "gravel", "image_reenacted": True,
        "image_alt": "Ricostruzione editoriale IA ultrarealistica della gara femminile dei Mondiali gravel a Nannup; non è una fotografia dell'evento.",
        "image_prompt": "Ciclista élite donna su percorso gravel tra foreste e colline di Nannup in Australia occidentale, scena ultrarealistica non documentaria; logo CurioMondo perfettamente circolare applicato in post-produzione.",
    },
]


def append_name_phrases() -> None:
    path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        "Dietro ogni previsione economica ci sono decisioni quotidiane molto concrete.",
        "Un'impresa che mette radici racconta una parte del futuro del Paese.",
        "Orientarsi tra i servizi è il primo passo per renderli davvero accessibili.",
        "Prima di investire, la verifica più preziosa è quella che evita una truffa.",
        "Il costo della vita si capisce soprattutto nelle spese che tornano ogni settimana.",
        "Quattro punti bastano a trasformare ogni curva in una scelta decisiva.",
        "Sotto la pioggia, vincere significa leggere il limite prima degli altri.",
        "Una partita può finire, ma il modo di reagire prepara già la prossima.",
        "Due gol di vantaggio contano soltanto se la concentrazione dura fino al ritorno.",
        "Quando la strada sale senza tregua, il coraggio deve trovare il proprio ritmo.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    append_name_phrases()
    base_time = datetime.now(ROME).replace(microsecond=0)
    minute_offsets = (0, 7, 19, 34, 49, 65, 83, 101, 118, 136)
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
        "last_update": f"economia-sport-v{VERSION}", "date": base_time.date().isoformat(),
        "release_date": base_time.date().isoformat(), "updated_at": base_time.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base_time.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
