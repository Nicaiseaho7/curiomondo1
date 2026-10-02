# PROTOCOLLO TITOLI — CURIOSITÀ INTELLIGENTE, VERITÀ E PROFESSIONALITÀ

**Versione:** 2.1
**Data:** 2 ottobre 2026  
**Stato:** obbligatorio, fail-closed  
**Ambito:** titolo di ogni articolo nuovo (notizia e approfondimento) e di ogni revisione di titolo richiesta. Lo stesso titolo va in H1, `<title>` (prima di ` | CurioMondo`), `og:title`, `twitter:title` se presente, `NewsArticle.headline`/`Article.headline`, card, feed e indici.
**Non riscrive** i titoli già online, se non è chiesto.

**Prevalenza.** Per la formulazione dei titoli questa versione sostituisce la v2.0, la v1.0 e ogni istruzione incompatibile, anche i riepiloghi legacy nei protocolli, manifest, prompt e skill. In particolare supera l'indicazione «curiosità facoltativa»: ogni titolo deve offrire un motivo concreto e veritiero per approfondire, con intensità proporzionata alla notizia. Restano aboliti la regola 70/30, l'obbligo di lasciare una risposta in sospeso e il divieto di titoli descrittivi. Restano obbligatori veridicità, attribuzione, sobrietà e corrispondenza tra titolo e contenuto. Il nome del file resta invariato per non rompere i riferimenti esistenti.

---

## 1. OBIETTIVO E PRIORITÀ

Scrivere titoli da testata professionale che facciano capire subito il tema e il fatto nuovo e suscitino il desiderio di approfondire. L'obiettivo è ottenere clic pertinenti e soddisfatti, anche quando il lettore vede soltanto il titolo su Google: incuriosire attraverso il valore della notizia, non attraverso mistero artificiale.

**Principio: rivelare la notizia, far percepire il valore dell'approfondimento.** Il lettore deve sapere di che cosa si parla e trovare un motivo reale per leggere dettagli, conseguenze, contesto o spiegazioni presenti nel pezzo.

- Priorità: accuratezza e grado di certezza → chiarezza → rilevanza e curiosità veritiera → naturalezza e varietà. Nessun incremento atteso di CTR giustifica un'informazione ingannevole.
- Il titolo dichiarativo, diretto e informativo è la scelta ordinaria. Può già dire il risultato, la cifra, l'orario o la decisione principale: non è un difetto.
- Ogni titolo deve offrire un motivo concreto per approfondire: una novità specifica, un contrasto significativo, una conseguenza documentata, un limite rilevante o un'utilità per il lettore. Non basta eliminare il punto interrogativo o produrre una formula burocratica corretta ma indistinta.
- Non tutti i pezzi richiedono lo stesso grado di curiosità. Nei servizi l'attrattiva può essere un orario, un requisito o un vantaggio concreto; nei temi sensibili conta capire il fatto con sobrietà. Non sono obbligatorie sorpresa, suspense o una seconda frase.
- Se manca un elemento distintivo, rileggere le fonti e il valore aggiunto del pezzo; non inventarlo, non gonfiare la notizia e non nascondere informazioni essenziali. Una notizia semplice può interessare per il fatto stesso.
- SEO e CTR sono obiettivi da valutare su dati reali, non garanzie di clic, posizionamento o presenza in Discover.

## 2. COME CREARE INTERESSE SENZA DOMANDE FORZATE

Individuare il dettaglio verificato che distingue questa notizia da un annuncio generico. Scegliere una leva adatta alla singola storia, non applicare un modello fisso:

- **Fatto o risultato:** soggetto + azione + novità verificata.
- **Conseguenza concreta:** fatto + effetto già documentato, senza ipotizzare impatti.
- **Dato o contrasto:** cifra significativa, confronto o elemento inatteso sostenuto dalle fonti. Un numero va contestualizzato, non usato come esca.
- **Limite o eccezione:** confine di una decisione, destinatari esclusi, condizione o differenza rispetto alla regola, soltanto se documentati e rilevanti.
- **Meccanismo o spiegazione:** risultato accompagnato da un processo o da una causa realmente sostenuti dal materiale. Non trasformare correlazioni o ipotesi in spiegazioni accertate.
- **Dichiarazione:** citazione breve realmente pronunciata e attribuita, solo se è il cuore della notizia.
- **Servizio:** destinatari, requisito, data o orario utili. Dare l'informazione essenziale è preferibile a nasconderla.

La curiosità intelligente nasce dalla precisione: il rapporto tra 1.200 candidature e 40 posti, un limite di tre annualità, visite disponibili fino all'una. Questi dettagli lasciano spazio a domande mentali naturali sul contesto e sulle implicazioni, senza imporre una domanda nel titolo né sottrarre la risposta essenziale.

Non tutti i titoli devono contenere una sorpresa, due punti, una citazione o una seconda frase. La varietà segue i fatti: non si ottiene ruotando meccanicamente questi schemi. Non incollare a ogni titolo «il dettaglio», «il motivo», «la svolta», «cosa cambia» o altre code intercambiabili.

## 3. DOMANDE: ECCEZIONE MOTIVATA

- Non trasformare una notizia con un fatto già noto in una domanda. Una domanda non sostituisce il risultato o la decisione.
- Usare un titolo interrogativo soltanto quando la domanda è davvero il tema di una guida, di un approfondimento o di una questione ancora aperta trattata nel testo. Anche allora valutare prima una forma dichiarativa.
- Le domande non devono essere la forma dominante del flusso di notizie né una scorciatoia per creare curiosità.
- Il controllo riguarda anche le interrogative indirette senza `?`: «cosa cambia», «cosa succede», «cosa rischia», «cosa indicano i dati», «quali sono…». Togliere il punto interrogativo non risolve la ripetizione.
- «Come», «perché» e «che cos'è» restano legittimi quando descrivono un reale intento di comprensione; non sono formule da aggiungere a ogni articolo.

## 4. ANTI-RIPETIZIONE EDITORIALE

Prima di approvare un titolo, confrontarlo con gli ultimi **10 titoli di notizie** pubblicati e con gli altri titoli del lotto in preparazione.

- Usare i titoli reali, non gli slug: `assets/data/home-feed-v210.json`, ordinato per `dateISO` decrescente, oppure H1/`headline` con la data di pubblicazione.
- Non approvare una sequenza costruita sullo stesso attacco o sulla stessa coda generica («cosa…», «ecco…», «il dettaglio che…»). Riformulare il nuovo titolo attorno al fatto specifico.
- Non sostituire «cosa cambia» con «quali effetti» soltanto per mascherare lo stesso schema interrogativo.
- Evitare serie tutte costruite come `tema: domanda`, `tema: cosa…` o `tema: ecco…`. I due punti sono ammessi, non obbligatori.
- Ripetere il nome di una persona, un luogo o una keyword pertinente è lecito: non alterare il fatto per ottenere varietà artificiale.
- Se tutti i titoli del lotto cercano il clic con una domanda o una suspense, il lotto va revisionato. Lo stesso vale per titoli generici che cambiano soltanto il soggetto. Il motivo per approfondire va individuato in ogni pezzo, senza quote di sorprese, numeri o citazioni e senza rotazioni automatiche di sinonimi.

## 5. INFORMAZIONE, SOBRIETÀ E PROMESSA

- Non nascondere il fatto decisivo o un'informazione essenziale di servizio solo per far aprire l'articolo. Il titolo non deve contenere ogni dettaglio, ma deve essere autonomo e non fuorviante.
- Il sommario e il lead completano il titolo con dettagli, limiti e contesto, senza ripeterlo né ritardare la risposta.
- Dichiarazioni, accuse, stime e possibilità restano attribuite come tali anche nel titolo. Una domanda non rende lecita un'insinuazione non verificata.
- Per salute, guerra, giustizia, vittime e sicurezza privilegiare sempre chiarezza e sobrietà, non suspense o allarmismo.
- Vietati clickbait falso, promesse vaghe, enfasi gratuita e formule come «non crederai», «il segreto», «nessuno lo sa», «ecco cosa…» usate come esca. Restano i divieti sensazionalistici di `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md`.
- Vietato il clickbait formalmente vero ma fuorviante: cifre senza il contesto necessario, dettagli marginali presentati come notizia principale, insinuazioni, superlativi non dimostrati o una precisazione nel corpo che smentisce l'impressione del titolo.
- La promessa implicita deve essere mantenuta: se il titolo richiama conseguenze, ragioni, condizioni o una spiegazione, il corpo deve offrirle realmente. Non promettere ciò che le fonti non consentono di sapere.

## 6. SEO E LUNGHEZZA SENZA RIGIDITÀ

- Mettere tema e keyword principale vicino all'inizio, preferibilmente nei primi 35–40 caratteri, quando l'italiano resta naturale.
- **55–70 caratteri** è un orientamento, non una soglia minima o un obbligo. Un titolo più breve e completo è valido; uno più lungo è ammesso se serve a precisione o attribuzione.
- Non aggiungere «cosa…», una domanda o parole inutili per raggiungere una misura. Non tagliare un'attribuzione necessaria per accorciarlo.
- Niente keyword stuffing. Il suffisso ` | CurioMondo` non entra nel conteggio. Il numero di caratteri non garantisce l'assenza di tagli su tutti i dispositivi.
- **Test Google:** rileggere il titolo isolato, senza sommario o immagine. Deve chiarire tema e fatto e far percepire perché questa pagina merita di essere aperta. L'inizio deve restare comprensibile e fedele anche se il risultato è troncato; non relegare in coda una negazione o un'attribuzione indispensabile.
- Il titolo deve corrispondere all'intento reale del lettore e al contenuto della pagina. Non aggiungere keyword o promesse per intercettare ricerche estranee.
- Google determina automaticamente il titolo mostrato e può usare `<title>`, H1, `og:title` e altri segnali. La coerenza delle superfici è necessaria, ma non garantisce il testo visualizzato o l'aumento dei clic. Riferimento tecnico: [Google Search Central — title links](https://developers.google.com/search/docs/appearance/title-link).

## 7. WORKFLOW E CONTROLLO FINALE

1. Identificare fatto nuovo, soggetto, elemento distintivo, pubblico interessato e grado di certezza.
2. Esplicitare internamente il **motivo per approfondire** in una frase e individuare il passaggio del corpo e la fonte che lo sostengono. Questa nota è di lavorazione, non va nel testo pubblico né nei metadati.
3. Quando la materia lo consente, confrontare due o tre alternative realmente diverse; almeno una deve essere dichiarativa e informativa. Non creare varianti solo cambiando «cosa» con «quali».
4. Scegliere il titolo più preciso e interessante per ciò che promette realmente il pezzo, non il più misterioso. Applicare il test Google e il test della promessa mantenuta.
5. Confrontare gli ultimi 10 titoli e il lotto corrente secondo §4.
6. Verificare che titolo, sommario e testo coincidano nei fatti e nel grado di certezza; sincronizzare tutte le superfici indicate nell'ambito.

Checklist bloccante:

- Il fatto si capisce anche leggendo il titolo da solo?
- Si percepisce un motivo concreto per approfondire, specifico di questa notizia?
- Ogni cifra, confronto, conseguenza e implicazione del titolo è sostenuto dal corpo e dalle fonti?
- L'articolo mantiene la promessa e aggiunge valore rispetto al titolo?
- Non sono nascosti fatti essenziali, limiti o attribuzioni per ottenere il clic?
- La domanda, se presente, è realmente giustificata e non seriale?
- Il titolo evita formule intercambiabili, ripetizioni, enfasi e italiano artificiale?
- H1, metadati, card, feed e indici sono coerenti?

Se manca il motivo per approfondire, rivedere l'angolazione sui fatti disponibili, non aggiungere una domanda o una coda vaga. La valutazione di curiosità e veridicità è editoriale: un conteggio di `?`, della parola «cosa», di cifre o di caratteri non misura la qualità di un titolo.

## 8. ESEMPI DI STILE

Esempi illustrativi: ogni formulazione è utilizzabile soltanto se tutti i fatti e gli ambiti indicati sono verificati nel pezzo.

| Titolo generico | Curiosità professionale e verificabile | Motivo per approfondire |
| --- | --- | --- |
| CDP, conclusa la terza edizione del Corporate MBA | CDP-Luiss, 1.200 candidature per 40 posti nel Corporate MBA | Rapporto significativo tra domanda e accessi al master, non posti di lavoro |
| Tennis and Friends, al via la manifestazione | Tennis and Friends, visite gratuite fino all'una sabato 3 ottobre | Opportunità concreta e orario distintivo |
| La Cassazione interviene sui mutui insoluti | Mutui insoluti, privilegio sugli interessi limitato a tre annualità | Confine preciso della prelazione, senza promettere cancellazioni del debito |
| Ustica, nuovi sviluppi nelle indagini | Ustica, il gip restituisce gli atti alla Procura: indagini avanti | Passaggio giudiziario reale e prosecuzione dell'indagine |

«Sciopero ferroviario, stop dalle 11 alle 14» resta valido se ambito e orari sono confermati: l'utilità è già un motivo per leggere i dettagli. «Come funziona il voto per gli italiani all'estero» è ammissibile per una guida che spiega davvero la procedura, non come modello per tutte le notizie.

## 9. MISURARE SENZA INSEGUIRE IL CLICKBAIT

Quando sono disponibili dati autorizzati, valutare impressioni, clic e CTR per pagina e query, tenendo conto di posizione, dispositivo, periodo e domanda di ricerca. Non attribuire automaticamente un cambiamento di CTR al titolo e non promettere percentuali di miglioramento senza prove. Non sacrificare accuratezza o soddisfazione del lettore per ottenere clic vuoti.

La curiosità non deve dipendere dall'omissione di informazioni cruciali, dall'esagerazione o dal richiamo morboso. Riferimento tecnico: [Google Search Central — Discover e clickbait](https://developers.google.com/search/docs/appearance/google-discover).

## MODIFICHE DELLA VERSIONE 2.1

Ogni titolo deve offrire un motivo veritiero per approfondire, non essere soltanto corretto; interesse attraverso dettagli distintivi, dati, contrasti, conseguenze, limiti, meccanismi o utilità documentati; intensità proporzionata; test del titolo isolato su Google e della promessa mantenuta; nota interna di riscontro nelle fonti; confronto di alternative quando utile; controllo anche del clickbait formalmente vero ma ingannevole. Restano domande solo motivate, divieto di schemi seriali, nessun 70/30, lunghezza indicativa e nessuna riscrittura retroattiva automatica.
