#!/usr/bin/env python3
from __future__ import annotations
from datetime import datetime
from email.utils import format_datetime
from html import escape
from pathlib import Path
import json
from lxml import etree, html

ROOT=Path(__file__).resolve().parents[1]
VERSION=246
DATE='2026-08-30'
DISCLOSURE='Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.'
TEMPLATE=ROOT/'notizie/rai-rimuove-sigfrido-ranucci-conduzione-report-29-agosto-2026.html'

NEPAL={
 'slug':'nepal-tibet-alluvioni-oltre-350-morti-1300-dispersi-27-agosto-2026',
 'title':'Catastrofe Nepal-Tibet, almeno 750 morti e oltre 3.000 dispersi: 261 stranieri risultano scomparsi in Tibet',
 'excerpt':'Il bilancio sale a 750 vittime e 3.044 dispersi tra Nepal e Tibet. In Tibet risultano scomparsi 261 stranieri di 23 Paesi, mentre nuove piogge e una seconda diga naturale complicano i soccorsi.',
 'section':'Ultima ora · Mondo / Asia / Ambiente',
 'category_meta':'Mondo / Asia / Ambiente',
 'published':'2026-08-27T16:55:00+02:00','updated':'2026-08-30T05:45:00+02:00','display':'27 agosto 2026 · aggiornato il 30 agosto alle 05:45',
 'image_base':'/assets/images/editorial-v246/nepal-tibet-750-morti-30-agosto-2026-ai',
 'image_alt':'Illustrazione editoriale IA di una valle himalayana devastata da una piena e da colate di detriti tra Nepal e Tibet',
 'insight':[('750','vittime confermate tra Nepal e Tibet'),('3.044','persone ancora disperse'),('261','stranieri dispersi in Tibet, da 23 Paesi')],
 'body':[
  'Il bilancio della catastrofe che ha investito il confine himalayano tra Nepal e Tibet compie un nuovo, drammatico salto. Le autorità nepalesi hanno comunicato domenica 30 agosto che i morti nel Paese sono saliti a 734, con 2.498 persone ancora disperse e 7.514 tratte in salvo. Sul versante tibetano le autorità cinesi hanno confermato 16 vittime e 546 dispersi. Sommando i due registri ufficiali, il bilancio minimo raggiunge quindi 750 morti e 3.044 persone di cui non si hanno ancora notizie.',
  'L’aumento è sostanziale rispetto agli aggiornamenti precedenti e non dipende da una semplice revisione statistica. Le squadre stanno raggiungendo aree rimaste isolate per giorni, mentre i registri di Nepal e Cina vengono aggiornati separatamente. In una calamità transfrontaliera di questa scala i numeri possono cambiare rapidamente: persone inizialmente registrate come disperse vengono ritrovate, nuovi corpi vengono identificati e intere comunità possono restare fuori dalle comunicazioni per molte ore. Per questo CurioMondo mantiene data e ora accanto a ogni bilancio.',
  'C’è anche un elemento internazionale nuovo. La Cina ha diffuso per la prima volta una ripartizione per nazionalità di 261 cittadini stranieri dispersi sul versante tibetano, provenienti da 23 Paesi. Tra loro figurano 104 nepalesi, 49 indiani, 33 lettoni, 18 statunitensi e 15 britannici. Pechino e Kathmandu stanno lavorando insieme per confrontare gli elenchi, identificare le persone mancanti e ridurre il rischio di doppi conteggi tra chi attraversava la frontiera, pellegrini, lavoratori e viaggiatori.',
  'Il nuovo elenco non risolve automaticamente tutte le segnalazioni nazionali emerse nei giorni scorsi. Nel precedente aggiornamento italiano, ANSA aveva indicato tra i dispersi Luca Barachini e la moglie Patrizia Marziale. Il dispaccio Reuters del 30 agosto non fornisce un nuovo stato specifico per la coppia; per correttezza CurioMondo non trasforma quindi l’assenza di un aggiornamento in una conferma positiva o negativa. In emergenze di questo tipo, il dato sulla nazionalità e quello sulla singola persona possono arrivare da registri diversi e in momenti differenti.',
  'La situazione sul terreno resta instabile. Nuove piogge hanno fatto salire il livello del fiume Trishuli e residenti e soccorritori sono stati invitati a spostarsi verso zone più alte. Il lago formatosi a monte dopo la frana legata al collasso glaciale si era in gran parte svuotato entro sabato sera, riducendo uno dei rischi immediati. Ma i droni hanno individuato un’altra frana circa 2,8 chilometri più a valle: il materiale ha creato una nuova diga naturale e un nuovo bacino d’acqua, costringendo le autorità ad allontanare parte delle squadre dalla zona di frontiera.',
  'Una cosa utile da sapere: una diga naturale formata da frana non funziona come una diga progettata. Rocce, fango, ghiaccio e tronchi possono bloccare un corso d’acqua senza avere sfioratori o strutture capaci di regolare la pressione. Se il livello cresce rapidamente, l’acqua può erodere il materiale e aprire un varco improvviso, generando una nuova piena a valle. È il motivo per cui droni, radar e misurazioni idrologiche sono diventati parte integrante delle operazioni di soccorso, non un’attività separata dalla ricerca dei dispersi.',
  'In Nepal l’attenzione si sta concentrando anche sui tunnel degli impianti idroelettrici. Centinaia di persone potrebbero essere rimaste intrappolate in sistemi sotterranei investiti da acqua, fango e detriti. Questo tipo di ricerca richiede competenze diverse da quelle usate per un edificio crollato: occorre valutare ventilazione, stabilità, accessi, presenza d’acqua e possibilità di ulteriori cedimenti. Kathmandu ha spiegato di non avere bisogno di un soccorso internazionale generalizzato, ma di assistenza tecnica mirata per tunnel, analisi del DNA, conservazione delle salme e identificazione forense.',
  'La cooperazione regionale si sta quindi spostando dalla prima risposta alla fase più complessa. Esperti indiani e cinesi sono sul terreno per contribuire alla riapertura dei tunnel e alle operazioni specialistiche. La Cina ha mobilitato oltre 2.100 soccorritori e stanziato almeno 220 milioni di yuan per gli interventi, oltre a fornire al Nepal dati satellitari e idrologici, materiali d’emergenza e specialisti. Le autorità dei due Paesi hanno definito l’evento una delle più gravi catastrofi transfrontaliere affrontate negli ultimi anni.',
  'Il disastro è stato innescato dal collasso di una massa glaciale e rocciosa nell’Himalaya, che ha scaricato ghiaccio, roccia, fango e detriti nei sistemi fluviali. La Cina ha collegato l’instabilità glaciale agli effetti di lungo periodo del riscaldamento globale. L’attribuzione scientifica di un singolo collasso resta un processo complesso, ma il contesto è chiaro: l’aumento delle temperature modifica ghiacciai, permafrost e laghi d’alta quota, creando combinazioni di rischio che possono propagarsi per decine di chilometri lungo valli molto ripide.',
  'Secondo la Croce Rossa, più di 90.000 persone potrebbero essere state interessate direttamente o indirettamente dalla catastrofe. Il danno non riguarda soltanto le vittime e gli sfollati: ponti, strade, centrali idroelettriche, reti elettriche e collegamenti commerciali sono stati distrutti o interrotti. In Nepal la ricostruzione è già stimata nell’ordine di diversi miliardi di dollari, una quota enorme per l’economia nazionale. Ripristinare le infrastrutture di montagna richiederà inoltre tempi lunghi perché molti cantieri dipendono da strade che devono essere ricostruite prima ancora di poter trasportare mezzi e materiali.',
  'Il dato più importante, però, resta umano. Con 3.044 persone ancora disperse, il bilancio delle vittime potrebbe cambiare ancora in entrambe le direzioni: alcuni nomi saranno cancellati dagli elenchi quando le persone verranno ritrovate, altri casi potranno trasformarsi in decessi confermati. Le prossime ore dipenderanno dal meteo, dalla stabilità delle nuove dighe naturali e dall’accesso ai tunnel e alle comunità isolate. Il minimo verificato al 30 agosto è di 750 morti; qualsiasi cifra successiva dovrà essere letta insieme alla fonte e all’orario di aggiornamento.',
  'CurioMondo aggiorna questo stesso articolo senza creare un duplicato, perché si tratta dello sviluppo della medesima catastrofe. Il salto del bilancio, la prima ripartizione dei 261 stranieri dispersi in Tibet e la comparsa di un nuovo bacino formato da frana cambiano materialmente il quadro rispetto al controllo precedente. L’emergenza non è più soltanto una grande operazione di ricerca: è diventata una crisi transfrontaliera di soccorso, identificazione, sicurezza idrogeologica e ricostruzione destinata a proseguire a lungo.'
 ],
 'sources':[
  ('https://www.reuters.com/world/china/china-identifies-countries-261-foreigners-missing-himalayan-mudslide-2026-08-30/','Reuters — bilancio di 750 morti e 3.044 dispersi, nazionalità dei 261 stranieri e nuova diga naturale'),
  ('https://apnews.com/article/nepal-china-flood-galchhi-warning-afec20e612514ca3598c65b29f485303','Associated Press — 734 morti e 2.498 dispersi in Nepal, 16 morti e 546 dispersi in Tibet e nuove allerte per le piene'),
  ('https://www.reuters.com/world/china/nepal-needs-help-technical-areas-not-search-rescue-foreign-minister-says-2026-08-29/','Reuters — assistenza tecnica richiesta dal Nepal, tunnel idroelettrici e quadro della ricostruzione'),
  ('https://www.ansa.it/sito/notizie/topnews/2026/08/29/tra-i-dispersi-in-nepal-gli-italiani-luca-barachini-e-la-moglie-patrizia-marziale_bc902ce6-fcf9-41c3-b449-f3bf7700ee71.html','ANSA — precedente segnalazione dei due cittadini italiani dispersi')
 ],
 'related':[
  ('/notizie/nepal-alluvione-ricostruzione-5-miliardi-29-agosto-2026.html','Mondo · Economia','Nepal, ricostruzione fino a 5 miliardi: l’alluvione vale quasi un decimo dell’economia'),
  ('/notizie/come-funzionano-piene-laghi-glaciali-glof-himalaya.html','Approfondimento · Clima','Come funzionano le piene da laghi glaciali e perché l’Himalaya è vulnerabile'),
  ('/notizie/terremoto-indonesia-100-morti-180000-evacuati-24-agosto-2026.html','Mondo · Asia','Indonesia, terremoto e maxi evacuazioni: il quadro dell’emergenza')
 ],
 'source_note':'Testo originale CurioMondo. Bilancio verificato su Reuters e Associated Press; ultimo aggiornamento editoriale: 30 agosto 2026, ore 05:45 italiane.'
}

HOUSE={
 'slug':'affitto-genitori-separati-fondo-60-milioni-30-agosto-2026',
 'title':'Affitto dimezzato per i genitori separati: pronta la norma da 60 milioni, contributi fino a 6.000 euro l’anno',
 'excerpt':'Il MIT dichiara pronta la norma per il sostegno abitativo: 50% dell’affitto fino a 6.000 euro l’anno, reddito IRPEF entro 35.000 euro e prima platea stimata in almeno 5.000 beneficiari.',
 'section':'Italia · Economia / Casa / Famiglie','category_meta':'Italia / Economia / Casa / Famiglie',
 'published':'2026-08-30T00:19:00+02:00','updated':'2026-08-30T00:19:00+02:00','display':'30 agosto 2026 · 00:19',
 'image_base':'/assets/images/editorial-v246/affitto-genitori-separati-30-agosto-2026-ai',
 'image_alt':'Illustrazione editoriale IA di una chiave di casa davanti a un edificio residenziale italiano, simbolo del sostegno all’affitto',
 'insight':[('60 mln €','risorse previste nel triennio'),('6.000 €','contributo massimo annuo'),('35.000 €','limite di reddito IRPEF indicato')],
 'body':[
  'Il fondo per il sostegno abitativo destinato ai genitori separati o divorziati entra in una fase più concreta. Il Ministero delle Infrastrutture e dei Trasporti ha comunicato il 29 agosto che la norma è pronta e che al Ministero dell’Economia è stata inviata una nota per sbloccare le risorse. L’obiettivo dichiarato è far partire il contributo quanto prima, con una prima platea stimata in almeno 5.000 beneficiari già nei prossimi mesi. Il passaggio è rilevante perché trasforma un fondo previsto dalla legge di Bilancio in una misura con criteri operativi molto più definiti.',
  'Le risorse complessive ammontano a 60 milioni di euro nel triennio. Il meccanismo indicato dal MIT prevede il pagamento del 50% delle spese di affitto dell’abitazione, fino a un massimo di 6.000 euro l’anno. In termini teorici il tetto corrisponde a 500 euro al mese per dodici mesi, ma l’importo effettivo dipenderà dal canone e dalle condizioni fissate nel provvedimento attuativo. Non significa quindi che ogni beneficiario riceverà automaticamente 6.000 euro: quello è il limite massimo previsto.',
  'I possibili beneficiari sono genitori separati o divorziati con almeno un figlio a carico, non assegnatari dell’abitazione familiare e in regola con i versamenti di mantenimento. Il reddito annuo dovrà essere entro 35.000 euro. Il MIT specifica inoltre che per questa misura non verrà utilizzato l’ISEE come parametro, ma il reddito ai fini IRPEF. È una scelta che modifica in modo importante la platea potenziale, perché ISEE e reddito IRPEF non misurano la stessa cosa e non sono intercambiabili.',
  'Una cosa utile da sapere: l’ISEE prova a fotografare la situazione economica complessiva del nucleo familiare combinando redditi, patrimoni e composizione della famiglia; il reddito IRPEF parte invece dai redditi fiscalmente rilevanti del contribuente. Due persone con lo stesso reddito possono quindi avere ISEE diversi, per esempio per patrimonio, numero di componenti o altre caratteristiche del nucleo. La scelta del parametro IRPEF rende il requisito più immediato da verificare, ma non equivale a una valutazione completa della ricchezza familiare.',
  'Ci sono poi altri paletti. Per ottenere il sostegno sarà necessario avere un contratto d’affitto regolare e non possedere altri immobili nel raggio di 50 chilometri dalla precedente abitazione familiare. Il contributo non potrà essere cumulato con altri sussidi per l’affitto. La domanda, secondo le indicazioni diffuse dal ministero, sarà presentabile online. Una volta sbloccate le risorse, la priorità dovrebbe andare alle regioni con un numero maggiore di genitori separati o divorziati e con una più forte emergenza abitativa.',
  'Il punto decisivo è che la misura non è ancora materialmente erogabile. Il MIT ha dichiarato pronta la norma, ma serve il via libera del Ministero dell’Economia allo sblocco dei fondi. Fino a quel momento non esiste una finestra di domanda effettivamente aperta e non avrebbe senso presentare richieste a siti o intermediari non ufficiali. Quando partirà la procedura, dovranno essere pubblicate istruzioni definitive su documenti, piattaforma, tempistiche, graduatorie e modalità di pagamento.',
  'La novità del 29-30 agosto va distinta dall’annuncio del 13 agosto. In quella data il MIT aveva comunicato di avere già avviato interlocuzioni con il MEF per rendere operativo il fondo entro il 2026. Allora erano noti lo stanziamento di 20 milioni l’anno per tre anni e l’obiettivo generale di sostenere i genitori non assegnatari della casa familiare. Il nuovo passaggio aggiunge requisiti molto più precisi: soglia di 35.000 euro, parametro IRPEF, distanza di 50 chilometri, non cumulabilità con altri aiuti e domanda online.',
  'Il problema a cui il fondo prova a rispondere è specifico. Dopo una separazione, l’abitazione familiare può essere assegnata al genitore con cui vivono prevalentemente i figli, mentre l’altro deve continuare a contribuire al mantenimento e contemporaneamente sostenere il costo di una nuova casa. Nelle città con canoni elevati questa doppia pressione può assorbire una quota molto grande del reddito disponibile. La misura non interviene sulle regole di assegnazione della casa o sugli assegni di mantenimento: agisce soltanto sul costo dell’alloggio del genitore che deve trovare una nuova sistemazione.',
  'Anche il limite geografico dei 50 chilometri ha una logica pratica: evitare che il contributo vada a chi dispone già di un’altra abitazione sufficientemente vicina alla precedente casa familiare. Ma la formulazione definitiva sarà importante per capire quali immobili verranno considerati, come saranno trattate quote di proprietà, case non abitabili o immobili occupati da altri familiari. Sono dettagli tecnici che possono cambiare concretamente l’accesso alla misura e che dovranno essere letti nel testo ufficiale.',
  'Sul piano finanziario, 60 milioni in tre anni significano una dotazione media di 20 milioni l’anno. Se tutti ricevessero il massimo teorico di 6.000 euro, 20 milioni coprirebbero poco più di 3.300 contributi pieni in un anno; nella pratica gli importi potrebbero essere inferiori e la distribuzione dipenderà dalle regole definitive. La stima ministeriale di almeno 5.000 beneficiari nei prossimi mesi va quindi letta come una previsione di platea iniziale, non come una garanzia individuale di accesso.',
  'Per chi potrebbe rientrare nei requisiti, il passaggio utile adesso è conservare e verificare la documentazione: contratto di locazione registrato, dati fiscali, situazione relativa al mantenimento e titolarità di eventuali immobili. Non serve invece affidarsi a moduli non ufficiali o anticipare pagamenti a soggetti che promettono di “prenotare” il bonus. Il canale corretto sarà quello indicato dalle amministrazioni quando il MEF avrà sbloccato le risorse e il provvedimento sarà operativo.',
  'La misura merita quindi attenzione, ma con una distinzione netta tra norma pronta e contributo già disponibile. Il salto rispetto a metà agosto è reale: il disegno è molto più dettagliato e il MIT ha formalizzato la richiesta di sblocco dei fondi. Il prossimo sviluppo sostanziale sarà l’ok del MEF e l’apertura effettiva della procedura. Solo allora si potrà sapere con certezza quando partiranno le domande, come verranno ordinate e quanti beneficiari riusciranno a ricevere il sostegno nel primo ciclo.'
 ],
 'sources':[
  ('https://www.mit.gov.it/comunicazione/news/genitori-separati-il-mit-norma-per-sostegno-abitativo-pronta-breve-con-ok-del','MIT — norma pronta, 60 milioni, requisiti, 50% dell’affitto e richiesta al MEF di sbloccare i fondi'),
  ('https://www.adnkronos.com/economia/affitto-dimezzato-fondo-genitori-separati_tdgtoIKElk5cXzPjJ14ML','Adnkronos — rilancio del 30 agosto con platea, requisiti e modalità previste'),
  ('https://www.ansa.it/sito/notizie/economia/2026/08/13/salvini-accelera-per-contributo-genitori-separati-entro-2026_5eac5d56-c3c6-4ffe-8dce-83722e1422a4.html','ANSA — precedente annuncio del 13 agosto e quadro originario del fondo')
 ],
 'related':[
  ('/notizie/italia-sconto-diesel-5-settembre-sostegni-reddito-27-agosto-2026.html','Italia · Economia','Diesel, sconto fino al 5 settembre e sostegni legati al reddito'),
  ('/notizie/italia-servizi-crescita-luglio-pmi-costi-rallentano-2026.html','Italia · Economia','Servizi italiani: crescita, PMI e costi sotto osservazione'),
  ('/notizie/ponte-stretto-via-libera-progettazione-esecutiva.html','Italia · Infrastrutture','Ponte sullo Stretto, il passaggio alla progettazione esecutiva')
 ],
 'source_note':'Testo originale CurioMondo. La misura non è ancora erogabile: l’avvio dipende dallo sblocco delle risorse da parte del MEF.'
}

ENERGY={
 'slug':'bollette-imprese-870-milioni-confesercenti-29-agosto-2026',
 'title':'Bollette, stangata da 870 milioni sulle imprese italiane: per alberghi e ristoranti aumenti vicini al 50%',
 'excerpt':'Confesercenti stima 870 milioni di maggiori costi energetici tra giugno e agosto: 700 milioni per l’elettricità e 170 per il gas, con rincari vicini al 50% per alberghi e ristoranti.',
 'section':'Italia · Economia / Energia / Imprese','category_meta':'Italia / Economia / Energia / Imprese',
 'published':'2026-08-29T11:17:00+02:00','updated':'2026-08-29T11:17:00+02:00','display':'29 agosto 2026 · 11:17',
 'image_base':'/assets/images/editorial-v246/bollette-imprese-870-milioni-30-agosto-2026-ai',
 'image_alt':'Illustrazione editoriale IA di una lampadina accesa davanti a un grafico in crescita, simbolo dei costi energetici delle imprese',
 'insight':[('870 mln €','maggiori costi energetici stimati'),('700 mln €','attribuiti all’elettricità'),('+48,5%','aumento indicativo per un albergo medio')],
 'body':[
  'L’estate 2026 presenta alle imprese italiane del commercio, della ristorazione e dell’accoglienza un conto energetico molto più pesante. Confesercenti, in collaborazione con il Gruppo Innova, stima in circa 870 milioni di euro l’aumento della spesa per le forniture di luce e gas tra giugno e agosto rispetto allo stesso periodo del 2025. Circa 700 milioni deriverebbero dall’elettricità e altri 170 milioni dal gas. La stima fotografa soprattutto i settori che durante l’estate devono mantenere accesi climatizzazione, refrigerazione, cucine e servizi per molte ore al giorno.',
  'Gli aumenti medi indicati dall’associazione superano il 40% per diverse categorie e arrivano vicino al 50% per ristoranti e alberghi. In alcuni casi singole imprese avrebbero registrato bollette quasi raddoppiate, con punte vicine al 90%. Il dato non significa che ogni attività italiana abbia subito lo stesso rincaro: contratti, consumi, potenza impegnata, località e profilo orario possono produrre risultati molto diversi. Ma la dimensione complessiva stimata mostra un problema nazionale di competitività, non una serie di episodi isolati.',
  'Per un albergo medio da 45 camere, le elaborazioni diffuse da Confesercenti indicano una spesa elettrica estiva che passa da circa 8.250 a 12.250 euro, un aumento del 48,5%. Per un ristorante il confronto è da circa 2.100 a 3.100 euro, pari al 47,6%, mentre per un bar si passa da circa 1.250 a 1.800 euro, circa il 44% in più. Anche i negozi registrano aumenti superiori al 40%. Sono esempi costruiti su profili medi e servono a rendere visibile l’ordine di grandezza del fenomeno.',
  'A spingere la spesa verso l’alto sono due forze che si sommano. La prima è il consumo: temperature eccezionalmente elevate hanno aumentato l’uso di condizionatori e sistemi di refrigerazione. La seconda è il prezzo dell’energia elettrica all’ingrosso. Tra giugno e agosto il PUN, il riferimento storico del mercato elettrico italiano, è aumentato di oltre il 30% rispetto allo stesso periodo del 2025 secondo i dati richiamati da Confesercenti. Più chilowattora consumati a un costo di mercato più alto producono un effetto moltiplicativo sulla bolletta.',
  'Una cosa utile da sapere: il prezzo all’ingrosso non coincide con il totale che un’impresa trova in fattura. La bolletta comprende energia, costi di rete, componenti di sistema, imposte e condizioni del contratto sottoscritto. Tuttavia il prezzo all’ingrosso influenza direttamente o indirettamente molte offerte, soprattutto quelle indicizzate. Per questo un aumento del mercato può trasferirsi con tempi e intensità differenti sulle singole aziende, mentre chi ha fissato il prezzo in precedenza può essere temporaneamente più protetto.',
  'Confesercenti segnala inoltre un problema di orario. Alberghi, ristoranti, bar e pubblici esercizi concentrano una parte importante dell’attività nelle ore serali, proprio quando durante l’estate si sono verificati picchi di prezzo particolarmente elevati. Un ristorante non può semplicemente spegnere frigoriferi, cucine o climatizzazione quando l’energia costa di più: il profilo operativo limita la capacità di spostare i consumi. Questo rende il settore più esposto rispetto ad attività che possono programmare parte della produzione in fasce meno costose.',
  'Il presidente di Confesercenti Nico Gronchi chiede interventi sugli oneri di sistema e sulla fiscalità per ridurre il rischio di nuovi rincari. L’associazione teme infatti che una parte dei maggiori costi venga trasferita sui prezzi finali. Non è un passaggio automatico: un’impresa può assorbire parte della spesa riducendo i margini, cercare efficienza o rinegoziare i contratti. Ma se l’aumento persiste, la pressione sui listini cresce, soprattutto nei settori con margini ridotti e costi energetici difficili da comprimere.',
  'La questione tocca direttamente il turismo, uno dei comparti più sensibili al rapporto tra prezzi e domanda. Alberghi e ristoranti devono competere con destinazioni estere e contemporaneamente sostenere costi che non dipendono soltanto dal numero di clienti. Una camera vuota continua a richiedere una struttura illuminata e climatizzata; una cucina deve mantenere la catena del freddo anche fuori dagli orari di servizio. Se l’energia assorbe una quota crescente dei ricavi, investimenti, assunzioni e manutenzione possono essere rinviati.',
  'Il confronto con il gas aggiunge un secondo livello di rischio. Dei 870 milioni stimati, circa 170 milioni riguardano il gas, ma l’attenzione delle imprese è già rivolta ai mesi più freddi, quando i consumi termici aumentano. L’Italia resta esposta alle oscillazioni internazionali dell’energia e nel 2026 le tensioni geopolitiche hanno già inciso su forniture, trasporti e prezzi. La recente interruzione di ulteriori carichi di GNL destinati a Edison mostra quanto la sicurezza degli approvvigionamenti e il costo finale possano restare collegati anche quando vengono trovati volumi alternativi.',
  'Per le imprese il dato utile non è soltanto la percentuale di aumento, ma la struttura del proprio contratto. Un prezzo fisso, un’offerta indicizzata, la durata residua, le fasce orarie e la potenza impegnata possono cambiare molto l’esposizione ai movimenti del mercato. Anche interventi relativamente semplici — manutenzione degli impianti, regolazione della climatizzazione, gestione delle celle frigorifere, illuminazione efficiente e controllo dei picchi — possono ridurre i consumi, ma non cancellano un aumento generalizzato del prezzo della materia energia.',
  'La stima da 870 milioni va quindi letta come un indicatore della pressione che l’energia esercita sul tessuto delle piccole e medie imprese. Non è una voce di spesa astratta: entra nei conti di hotel, ristoranti, bar e negozi proprio nel periodo in cui molte attività realizzano una parte decisiva del fatturato annuale. Se il rincaro dovesse proseguire verso l’autunno e l’inverno, il problema potrebbe spostarsi dalla stagione turistica alla tenuta dei margini e ai prezzi pagati dalle famiglie.',
  'Il prossimo dato da osservare sarà l’evoluzione dei prezzi all’ingrosso e del gas insieme alle eventuali decisioni del governo su fiscalità e oneri. Per ora il numero verificato è quello diffuso da Confesercenti e ripreso da ANSA e AGI: 870 milioni di euro di maggiori costi stimati tra giugno e agosto 2026 rispetto allo stesso periodo dell’anno precedente. È abbastanza per trasformare il caro-energia da tema settoriale a questione economica nazionale, soprattutto per commercio, ristorazione e accoglienza.'
 ],
 'sources':[
  ('https://www.confesercenti.it/blog/bollette-confesercenti-giugno-agosto-stangata/','Confesercenti — stima originaria dei 870 milioni, cause dei rincari e impatto sui diversi settori'),
  ('https://www.ansa.it/sito/notizie/economia/pmi/2026/08/29/confesercenti-con-bollette-stangata-da-870-milioni-su-imprese-e-turismo_13af97a3-8b77-4695-b58a-f2ede7b572ac.html','ANSA — 870 milioni di maggiori costi, 700 milioni elettricità e 170 milioni gas'),
  ('https://www.agi.it/economia/news/2026-08-29/confesercenti-stangata-bollette-38763530/','AGI — riscontro sul rincaro delle bollette per commercio, ristorazione e turismo')
 ],
 'related':[
  ('/notizie/qatarenergy-stop-gas-edison-italia-novembre-29-agosto-2026.html','Italia · Energia','Gas, QatarEnergy ferma altre cinque consegne a Edison fino a novembre'),
  ('/notizie/italia-sconto-diesel-5-settembre-sostegni-reddito-27-agosto-2026.html','Italia · Economia','Diesel, lo sconto resta fino al 5 settembre'),
  ('/notizie/iran-economia-guerra-sanzioni-commercio-29-agosto-2026.html','Mondo · Economia','Iran, guerra e sanzioni pesano sul commercio e sull’energia')
 ],
 'source_note':'Testo originale CurioMondo. I valori sono stime Confesercenti elaborate con Gruppo Innova e riprese da ANSA e AGI.'
}

STORIES=[NEPAL,HOUSE,ENERGY]
NEW=[HOUSE,ENERGY]

def dump(path,obj,compact=False):
 path.parent.mkdir(parents=True,exist_ok=True)
 path.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':') if compact else None,indent=None if compact else 2)+'\n',encoding='utf-8')

def write(path,text):
 path.parent.mkdir(parents=True,exist_ok=True); path.write_text(text,encoding='utf-8')

def url(story): return f"/notizie/{story['slug']}.html"
def canonical(story): return 'https://curiomondo.it'+url(story)
def image(story,w=800): return f"{story['image_base']}-{w}.webp"
def srcset(story): return f"{image(story,480)} 480w, {image(story,800)} 800w, {image(story,1200)} 1200w"
def date_label(story): return story['updated'][:10]

def entry(story):
 return {'title':story['title'],'excerpt':story['excerpt'],'url':url(story),'section':story['section'],'dateISO':story['updated'],'dateLabel':date_label(story),'image':image(story,800),'imageAlt':story['image_alt'],'imageWidth':800,'imageHeight':533,'srcset':srcset(story)}

def set_meta(doc, attr, key, value):
 n=doc.xpath(f'//meta[@{attr}="{key}"]')
 if n: n[0].set('content',value)

def set_article(story, new=False):
 path=ROOT/f"notizie/{story['slug']}.html"
 if new:
  doc=html.fromstring(TEMPLATE.read_text(encoding='utf-8'))
 else:
  doc=html.fromstring(path.read_text(encoding='utf-8'))
 doc.xpath('//title')[0].text=story['title']+' | CurioMondo'
 set_meta(doc,'name','description',story['excerpt']); set_meta(doc,'property','og:title',story['title']); set_meta(doc,'property','og:description',story['excerpt']); set_meta(doc,'property','og:url',canonical(story)); set_meta(doc,'property','og:image','https://curiomondo.it'+image(story,1200)); set_meta(doc,'property','og:image:alt',story['image_alt'])
 can=doc.xpath('//link[@rel="canonical"]')[0]; can.set('href',canonical(story))
 schema_node=doc.xpath('//script[@type="application/ld+json"]')[0]
 schema={'@context':'https://schema.org','@type':'NewsArticle','headline':story['title'],'description':story['excerpt'],'datePublished':story['published'],'dateModified':story['updated'],'mainEntityOfPage':canonical(story),'inLanguage':'it-IT','author':{'@type':'Organization','name':'Redazione CurioMondo'},'publisher':{'@type':'Organization','name':'CurioMondo','logo':{'@type':'ImageObject','url':'https://curiomondo.it/curiomondo-logo-512.png'}},'image':['https://curiomondo.it'+image(story,1200)]}
 schema_node.text=json.dumps(schema,ensure_ascii=False,separators=(',',':'))
 doc.xpath('//body')[0].set('data-article-id',story['slug'])
 doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," badge ")]')[0].text=story['section']
 doc.xpath('//h1')[0].text=story['title']
 doc.xpath('//p[contains(concat(" ",normalize-space(@class)," ")," subtitle ")]')[0].text=story['excerpt']
 meta=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," meta ")]')[0]
 for c in list(meta): meta.remove(c)
 meta.text=f"{story['display']} · {story['category_meta']} · "; sp=etree.SubElement(meta,'span',id='readTime'); sp.text='5 min di lettura'
 # figure
 fig=doc.xpath('//figure[contains(concat(" ",normalize-space(@class)," ")," article-image ")]')[0]
 fig.attrib.clear(); fig.set('class','article-image'); fig.set('data-ai-generated','true')
 pic=fig.xpath('./picture')[0]; img=pic.xpath('.//img')[0]
 img.set('src','..'+image(story,800)); img.set('srcset','..'+srcset(story).replace(', ', ', ../').replace('/assets','/assets',1))
 # fix relative srcset robustly
 img.set('srcset',f"..{image(story,480)} 480w, ..{image(story,800)} 800w, ..{image(story,1200)} 1200w")
 img.set('alt',story['image_alt']); img.set('width','800'); img.set('height','533'); img.set('loading','eager'); img.set('fetchpriority','high'); img.set('decoding','async'); img.set('sizes','(max-width:832px) calc(100vw - 32px),800px')
 cap=fig.xpath('./figcaption')[0] if fig.xpath('./figcaption') else etree.SubElement(fig,'figcaption'); cap.text=DISCLOSURE
 # editorial data
 ed=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," editorial-data ")]')[0]
 for c in list(ed): ed.remove(c)
 d1=etree.SubElement(ed,'div'); st=etree.SubElement(d1,'strong'); st.text='Keyword principale:'; st.tail=' '+story['title'].split(':')[0]
 d2=etree.SubElement(ed,'div'); st=etree.SubElement(d2,'strong'); st.text='URL SEO:'; st.tail=' '+url(story)
 # insight
 ins=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cm-insight ")]')[0]
 newi=html.fragment_fromstring('<section class="cm-insight"><span class="cm-kicker">Il punto in tre dati</span><div class="cm-insight-grid"></div></section>')
 grid=newi.xpath('.//div')[0]
 for b,small in story['insight']:
  d=etree.SubElement(grid,'div'); be=etree.SubElement(d,'b'); be.text=b; sm=etree.SubElement(d,'small'); sm.text=small
 ins.getparent().replace(ins,newi)
 # body
 art=doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')[0]
 art.attrib.clear(); art.set('class','art-body'); art.set('data-length-policy','5000-7000')
 for c in list(art): art.remove(c)
 for ptxt in story['body']:
  p=etree.SubElement(art,'p'); p.text=ptxt
 # related
 sources=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," art-sources ")]')[0]
 old=doc.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," curio-related ")]')
 rh='<section class="curio-related" aria-labelledby="curio-related-title"><h2 id="curio-related-title">Potrebbe interessarti anche…</h2><div class="curio-related-grid">'
 for u,cat,t in story['related']: rh+=f'<a href="{u}"><span>{escape(cat)}</span><strong>{escape(t)}</strong></a>'
 rh+='</div></section>'; rel=html.fragment_fromstring(rh)
 if old: old[0].getparent().replace(old[0],rel)
 else: sources.addprevious(rel)
 # sources
 ul=sources.xpath('./ul')[0]
 for c in list(ul): ul.remove(c)
 for u,label in story['sources']:
  li=etree.SubElement(ul,'li'); a=etree.SubElement(li,'a',href=u,rel='noopener noreferrer',target='_blank'); a.text=label
 sm=sources.xpath('.//small');
 if sm: sm[0].text=story['source_note']
 for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'): link.set('href','../assets/css/curiomondo-article-v211.css?v=246')
 for sc in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'): sc.set('src','../assets/js/curiomondo-article-v210.js?v=246')
 write(path,'<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'))
 dump(ROOT/f"contenuti/notizie/{story['slug']}.json",{'slug':story['slug'],'title':story['title'],'excerpt':story['excerpt'],'category':story['section'],'published_at':story['published'],'updated_at':story['updated'],'body':story['body'],'related':[u for u,_,_ in story['related']],'sources':[{'url':u,'label':l} for u,l in story['sources']],'image':{'key':Path(story['image_base']).name,'alt':story['image_alt'],'ai_generated':True,'documentary_photo':False,'disclosure':DISCLOSURE}})

def update_data():
 hp=ROOT/'assets/data/home-feed-v210.json'; h=json.loads(hp.read_text(encoding='utf-8')); h['version']=VERSION
 urls={url(s) for s in STORIES}; items=[x for x in h['items'] if x.get('url') not in urls]; items.extend(entry(s) for s in STORIES); items.sort(key=lambda x:str(x.get('dateISO','')),reverse=True); h['items']=items; dump(hp,h,True)
 sp=ROOT/'assets/data/search-index-v210.json'; s=json.loads(sp.read_text(encoding='utf-8')); s['version']=VERSION
 si=[x for x in s['items'] if x.get('url') not in urls]
 for st in reversed(STORIES): si.insert(0,{k:entry(st)[k] for k in ('title','excerpt','url','section')})
 s['items']=si; dump(sp,s,True)
 lp=ROOT/'automation/live-seed.json'; live=json.loads(lp.read_text(encoding='utf-8')); live['updated_at']='2026-08-30T06:53:00+00:00'; news=[x for x in items if x.get('url','').startswith('/notizie/')]; live['items']=[{'title':x['title'],'url':x['url'],'published_at':x['dateISO'],'source':'CurioMondo','article_exists':True} for x in news[:10]]; dump(lp,live)

def picture(item,eager=False,hero=False):
 loading='eager' if eager else 'lazy'; fp=' fetchpriority="high"' if eager else ''
 sizes='(max-width:600px) 79vw,300px'
 return f'<picture><img alt="{escape(item["imageAlt"],quote=True)}" decoding="async" loading="{loading}" height="533" sizes="{sizes}" src="{item["image"]}" srcset="{item["srcset"]}" width="800"{fp}></picture>'

def update_home():
 p=ROOT/'index.html'; doc=html.fromstring(p.read_text(encoding='utf-8')); items=json.loads((ROOT/'assets/data/home-feed-v210.json').read_text(encoding='utf-8'))['items']; news=[x for x in items if x.get('url','').startswith('/notizie/')]
 # ticker exact 10
 for ti,track in enumerate(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')[:2]):
  for c in list(track): track.remove(c)
  for it in news[:10]:
   a=etree.SubElement(track,'a',href=it['url']); a.set('class','ticker-news'); a.text=it['title'];
   if ti==1: a.set('tabindex','-1')
 # hero = Nepal
 hero=doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]; st=entry(NEPAL); hero.set('href',st['url'])
 for c in list(hero): hero.remove(c)
 hero.append(html.fragment_fromstring(picture(st,True)))
 txt=etree.SubElement(hero,'div'); txt.set('class','txt'); tag=etree.SubElement(txt,'span'); tag.set('class','tag'); tag.text='Ultima ora'; h1=etree.SubElement(txt,'h1'); h1.text=st['title']; pp=etree.SubElement(txt,'p'); pp.text=st['excerpt']; cta=etree.SubElement(txt,'span'); cta.set('class','cta'); cta.text='Leggi l’articolo →'
 # 5 today
 rail=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
 for c in list(rail): rail.remove(c)
 for it in news[:5]:
  rail.append(html.fragment_fromstring(f'<a class="auto-card" href="{it["url"]}">{picture(it)}<div class="abody"><div class="ameta">{escape(it["section"])}</div><h3>{escape(it["title"])}</h3><p>{escape(it["excerpt"])}</p><time datetime="{it["dateISO"]}">{it["dateLabel"]}</time></div></a>'))
 cards=doc.xpath('//div[@id="cards"]')[0]
 for c in list(cards): cards.remove(c)
 for it in news[5:23]:
  cards.append(html.fragment_fromstring(f'<a class="card" href="{it["url"]}">{picture(it)}<div class="body"><div class="meta">{escape(it["section"])}</div><h3>{escape(it["title"])}</h3><p>{escape(it["excerpt"])}</p><time datetime="{it["dateISO"]}">{it["dateLabel"]}</time></div></a>'))
 for sc in doc.xpath('//script[contains(@src,"home-v210.js")]'): sc.set('src','/assets/js/home-v210.js?v=246')
 write(p,'<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'))

def update_archive():
 p=ROOT/'notizie/index.html'; doc=html.fromstring(p.read_text(encoding='utf-8')); ul=doc.xpath('//main//ul')[0]; urls={url(s) for s in STORIES}
 for li in list(ul):
  a=li.xpath('./a')
  if a and a[0].get('href') in urls: ul.remove(li)
 # Use home-feed news order for archive entries, preserving old unknown items afterwards.
 top=[NEPAL,HOUSE]
 # energy position by update time: after Cremona and before Di Battista? We'll rebuild all known story positions via sort of current li + new/update metadata.
 existing=[]
 for li in list(ul):
  a=li.xpath('./a');
  if not a: continue
  href=a[0].get('href'); strong=a[0].xpath('./strong'); span=a[0].xpath('./span'); existing.append((href,strong[0].text_content() if strong else a[0].text_content(),span[0].text_content() if span else ''))
 # prepend/update based on home news order, then keep rest unique
 feed=json.loads((ROOT/'assets/data/home-feed-v210.json').read_text(encoding='utf-8'))['items']; order=[x for x in feed if x.get('url','').startswith('/notizie/')]
 byhref={h:(t,d) for h,t,d in existing}
 for st in NEW: byhref[url(st)]=(st['title'],date_label(st))
 byhref[url(NEPAL)]=(NEPAL['title'],date_label(NEPAL))
 for c in list(ul): ul.remove(c)
 seen=set()
 for it in order:
  href=it['url']
  if href in byhref and href not in seen:
   t,d=byhref[href]; li=html.fragment_fromstring(f'<li><a href="{href}"><strong>{escape(t)}</strong><span>{escape(d)}</span></a></li>'); ul.append(li); seen.add(href)
 for href,t,d in existing:
  if href not in seen:
   li=html.fragment_fromstring(f'<li><a href="{href}"><strong>{escape(t)}</strong><span>{escape(d)}</span></a></li>'); ul.append(li); seen.add(href)
 doc.xpath('//main/p')[0].text=f"{len(ul.xpath('./li'))} articoli, ordinati per data."
 write(p,'<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'))

def update_feed():
 p=ROOT/'feed.xml'; parser=etree.XMLParser(remove_blank_text=False); tree=etree.parse(str(p),parser); ch=tree.getroot().find('channel'); urls={canonical(s) for s in STORIES}
 for it in list(ch.findall('item')):
  if it.findtext('link') in urls: ch.remove(it)
 for st in STORIES:
  it=etree.Element('item')
  for n,v in [('title',st['title']),('link',canonical(st)),('guid',canonical(st)),('pubDate',format_datetime(datetime.fromisoformat(st['updated']))),('description',st['excerpt'])]: etree.SubElement(it,n).text=v
  ch.append(it)
 # sort item elements by pubDate descending, leave non-item channel children in place by moving items after metadata block
 items=list(ch.findall('item'))
 from email.utils import parsedate_to_datetime
 
 def dtkey(x):
  v=x.findtext('pubDate')
  try: return parsedate_to_datetime(v) if v else datetime(1970,1,1).astimezone()
  except Exception: return datetime(1970,1,1).astimezone()
 items.sort(key=dtkey,reverse=True)
 for it in list(ch.findall('item')): ch.remove(it)
 for it in items: ch.append(it)
 p.write_bytes(etree.tostring(tree,encoding='utf-8',xml_declaration=True,pretty_print=True))

def update_sitemaps():
 sns='http://www.sitemaps.org/schemas/sitemap/0.9'; nns='http://www.google.com/schemas/sitemap-news/0.9'; parser=etree.XMLParser(remove_blank_text=False)
 sp=ROOT/'sitemap.xml'; stree=etree.parse(str(sp),parser); root=stree.getroot()
 for story in STORIES:
  can=canonical(story); nodes=stree.xpath('//s:url[s:loc=$loc]',namespaces={'s':sns},loc=can)
  if nodes: node=nodes[0]
  else:
   node=etree.Element(f'{{{sns}}}url'); etree.SubElement(node,f'{{{sns}}}loc').text=can; root.append(node)
  lm=node.find(f'{{{sns}}}lastmod');
  if lm is None: lm=etree.SubElement(node,f'{{{sns}}}lastmod')
  lm.text=story['updated'][:10]
 sp.write_bytes(etree.tostring(stree,encoding='utf-8',xml_declaration=True,pretty_print=True))
 np=ROOT/'news-sitemap.xml'; ntree=etree.parse(str(np),parser); nroot=ntree.getroot()
 for story in STORIES:
  can=canonical(story); nodes=ntree.xpath('//s:url[s:loc=$loc]',namespaces={'s':sns},loc=can)
  if nodes: node=nodes[0]
  else:
   node=etree.Element(f'{{{sns}}}url'); etree.SubElement(node,f'{{{sns}}}loc').text=can; news=etree.SubElement(node,f'{{{nns}}}news'); pub=etree.SubElement(news,f'{{{nns}}}publication'); etree.SubElement(pub,f'{{{nns}}}name').text='CurioMondo'; etree.SubElement(pub,f'{{{nns}}}language').text='it'; etree.SubElement(news,f'{{{nns}}}publication_date').text=story['published']; etree.SubElement(news,f'{{{nns}}}title').text=story['title']; nroot.insert(0,node)
  title=node.find(f'.//{{{nns}}}title'); pub=node.find(f'.//{{{nns}}}publication_date')
  if title is not None: title.text=story['title']
  if pub is not None: pub.text=story['published']
 np.write_bytes(etree.tostring(ntree,encoding='utf-8',xml_declaration=True,pretty_print=True))

def update_release():
 for fn in ['RELEASE-STATE.json','CURIOMONDO-RELEASE-STATE.json']:
  p=ROOT/fn
  if not p.exists(): continue
  d=json.loads(p.read_text(encoding='utf-8'))
  if fn=='RELEASE-STATE.json': d.update({'currentVersion':VERSION,'baselineVersion':245,'status':'ready','date':DATE,'site_version':VERSION,'version':str(VERSION),'baseline_version':245,'baseline':'curiomondo-v245-domanda-del-giorno-30-agosto-2026-netlify.zip','last_update':'nepal-750-house-energy-v246','release_date':DATE,'articleCount':d.get('articleCount',191)+2,'generatedEditorialImages':d.get('generatedEditorialImages',71)+3})
  else: d.update({'site_version':VERSION,'baseline_version':245,'version':str(VERSION),'date':DATE,'baseline':'curiomondo-v245-domanda-del-giorno-30-agosto-2026-netlify.zip','last_update':'nepal-750-house-energy-v246','performance_pass':'Tre visual WebP responsive; LIVE 10, Notizie di oggi 5, nessun build Netlify.'})
  dump(p,d)
 mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text(encoding='utf-8')); m['site']['current_site_version']=VERSION; m['site_version']=VERSION; m['version']='v246'; m['release_version']='v246'; m['last_release_date']=DATE; m['last_release']={'version':VERSION,'date':DATE,'baseline_version':245,'news_added':[HOUSE['slug'],ENERGY['slug']],'news_updated':[NEPAL['slug']],'daily_question_preserved':'quanto-di-te-stai-rendendo-piu-piccolo-per-non-mettere-a-disagio-gli-altri','library_guides_preserved':['come-scaricare-video-youtube','come-fare-backup-whatsapp-foto-pc'],'image_policy_applied':'three-new-ai-editorial-visuals-v246'}; dump(mp,m)
 notes=f'''# CurioMondo v246 — 30 agosto 2026\n\n- Aggiornato senza duplicati l’articolo Nepal–Tibet: almeno 750 morti e 3.044 dispersi; aggiunta la prima ripartizione dei 261 stranieri dispersi in Tibet e il nuovo rischio da frana/diga naturale.\n- Aggiunto l’articolo sul fondo affitti per genitori separati: 60 milioni in tre anni, copertura del 50% fino a 6.000 euro annui, reddito IRPEF entro 35.000 euro e avvio subordinato allo sblocco MEF.\n- Aggiunto l’articolo sulle bollette delle imprese: stima Confesercenti da 870 milioni tra giugno e agosto, con impatto vicino al 50% su alberghi e ristoranti.\n- Generati tre nuovi visual editoriali IA dedicati, senza testo nei pixel, con disclosure obbligatoria nelle pagine articolo.\n- Nepal–Tibet promosso a Ultima Ora; aggiornati LIVE, Notizie di oggi, Altre notizie, archivio, ricerca, feed RSS, sitemap e News Sitemap.\n- Preservati Domanda del giorno ed eBook/guide della v245.\n'''; write(ROOT/'RELEASE-NOTES-v246.md',notes)

def qa():
 out={}
 for st in STORIES:
  p=ROOT/f"notizie/{st['slug']}.html"; doc=html.fromstring(p.read_text(encoding='utf-8')); body=sum(len(x) for x in st['body']); out[st['slug']]={'body_chars':body,'body_ok':5000<=body<=7000,'h1':doc.xpath('//h1')[0].text_content()==st['title'],'sources':len(doc.xpath('//div[contains(@class,"art-sources")]//li')),'related':len(doc.xpath('//section[contains(@class,"curio-related")]//a')),'image_exists':(ROOT/image(st,800).lstrip('/')).exists(),'disclosure':DISCLOSURE in p.read_text(encoding='utf-8')}
 home=html.fromstring((ROOT/'index.html').read_text(encoding='utf-8')); tracks=home.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]'); rail=home.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0].xpath('./a'); cards=home.xpath('//div[@id="cards"]')[0].xpath('./a'); hero=home.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
 out['home']={'live':len(tracks[0].xpath('./a')),'today':len(rail),'other':len(cards),'hero_nepal':hero.get('href')==url(NEPAL),'unique_today_other':len({a.get('href') for a in rail+cards})==len(rail+cards)}
 bad=[]
 for k,v in out.items():
  if k=='home':
   if v!={'live':10,'today':5,'other':18,'hero_nepal':True,'unique_today_other':True}: bad.append((k,v))
  else:
   if not v['body_ok'] or not v['h1'] or v['sources']<3 or v['related']!=3 or not v['image_exists'] or not v['disclosure']: bad.append((k,v))
 if bad: raise RuntimeError(bad)
 return out

def main():
 set_article(NEPAL,False); set_article(HOUSE,True); set_article(ENERGY,True); update_data(); update_home(); update_archive(); update_feed(); update_sitemaps(); update_release(); print(json.dumps({'version':VERSION,'checks':qa()},ensure_ascii=False,indent=2))
if __name__=='__main__': main()
