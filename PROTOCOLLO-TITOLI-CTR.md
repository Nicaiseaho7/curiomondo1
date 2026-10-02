# PROTOCOLLO TITOLI PROFESSIONALI — CHIAREZZA, INTERESSE E VARIETÀ

**Versione:** 2.0
**Data:** 2 ottobre 2026  
**Stato:** obbligatorio, fail-closed  
**Ambito:** titolo di ogni articolo nuovo (notizia e approfondimento) e di ogni revisione di titolo richiesta. Lo stesso titolo va in H1, `<title>` (prima di ` | CurioMondo`), `og:title`, `twitter:title` se presente, `NewsArticle.headline`/`Article.headline`, card, feed e indici.
**Non riscrive** i titoli già online, se non è chiesto.

**Prevalenza.** Per la formulazione dei titoli questa versione sostituisce la v1.0 e ogni istruzione incompatibile, anche i riepiloghi legacy nei prompt e nelle skill. Sono aboliti la regola 70/30, l'obbligo di lasciare una risposta in sospeso e il divieto di titoli descrittivi o da agenzia. Restano obbligatori veridicità, attribuzione, sobrietà e corrispondenza tra titolo e contenuto. Il nome del file resta invariato per non rompere i riferimenti esistenti.

---

## 1. OBIETTIVO E PRIORITÀ

Scrivere titoli da testata professionale: il lettore deve capire subito il tema e il fatto nuovo. L'interesse nasce dalla notizia, non da una domanda aggiunta per ottenere il clic.

- Priorità: accuratezza → chiarezza → rilevanza → naturalezza e varietà → interesse.
- Il titolo dichiarativo, diretto e informativo è la scelta ordinaria. Può già dire il risultato, la cifra, l'orario o la decisione principale: non è un difetto.
- La curiosità è facoltativa, non richiesta per ogni articolo. Se i fatti non offrono un elemento interessante, non inventare un gancio.
- SEO e CTR sono obiettivi da valutare su dati reali, non garanzie di clic, posizionamento o presenza in Discover.

## 2. COME CREARE INTERESSE SENZA DOMANDE FORZATE

Scegliere la forma adatta alla singola storia, non applicare un modello fisso:

- **Fatto o risultato:** soggetto + azione + novità verificata.
- **Conseguenza concreta:** fatto + effetto già documentato, senza ipotizzare impatti.
- **Dato o contrasto:** cifra significativa, confronto o elemento inatteso sostenuto dalle fonti. Un numero va contestualizzato, non usato come esca.
- **Dichiarazione:** citazione breve realmente pronunciata e attribuita, solo se è il cuore della notizia.
- **Servizio:** destinatari, requisito, data o orario utili. Dare l'informazione essenziale è preferibile a nasconderla.

Non tutti i titoli devono contenere una sorpresa, due punti, una citazione o una seconda frase. La varietà segue i fatti: non si ottiene ruotando meccanicamente questi schemi.

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
- Se tutti i titoli del lotto cercano il clic con una domanda o una suspense, il lotto va revisionato. Nessuna quota obbligatoria di titoli curiosi e nessuna rotazione automatica di sinonimi.

## 5. INFORMAZIONE, SOBRIETÀ E PROMESSA

- Non nascondere il fatto decisivo o un'informazione essenziale di servizio solo per far aprire l'articolo. Il titolo non deve contenere ogni dettaglio, ma deve essere autonomo e non fuorviante.
- Il sommario e il lead completano il titolo con dettagli, limiti e contesto, senza ripeterlo né ritardare la risposta.
- Dichiarazioni, accuse, stime e possibilità restano attribuite come tali anche nel titolo. Una domanda non rende lecita un'insinuazione non verificata.
- Per salute, guerra, giustizia, vittime e sicurezza privilegiare sempre chiarezza e sobrietà, non suspense o allarmismo.
- Vietati clickbait falso, promesse vaghe, enfasi gratuita e formule come «non crederai», «il segreto», «nessuno lo sa», «ecco cosa…» usate come esca. Restano i divieti sensazionalistici di `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md`.

## 6. SEO E LUNGHEZZA SENZA RIGIDITÀ

- Mettere tema e keyword principale vicino all'inizio, preferibilmente nei primi 35–40 caratteri, quando l'italiano resta naturale.
- **55–70 caratteri** è un orientamento, non una soglia minima o un obbligo. Un titolo più breve e completo è valido; uno più lungo è ammesso se serve a precisione o attribuzione.
- Non aggiungere «cosa…», una domanda o parole inutili per raggiungere una misura. Non tagliare un'attribuzione necessaria per accorciarlo.
- Niente keyword stuffing. Il suffisso ` | CurioMondo` non entra nel conteggio. Il numero di caratteri non garantisce l'assenza di tagli su tutti i dispositivi.

## 7. WORKFLOW E CONTROLLO FINALE

1. Identificare fatto nuovo, soggetto, elemento distintivo e grado di certezza.
2. Preparare internamente fino a tre alternative quando utile; almeno una deve essere dichiarativa e informativa. Non creare varianti solo cambiando «cosa» con «quali».
3. Scegliere per precisione, leggibilità e specificità, non per quantità di mistero. Se la versione diretta funziona meglio, pubblicare quella.
4. Confrontare gli ultimi 10 titoli e il lotto corrente secondo §4.
5. Verificare che titolo, sommario e testo coincidano nei fatti e nel grado di certezza; sincronizzare tutte le superfici indicate nell'ambito.

Checklist bloccante: fatto comprensibile; testo a sostegno; nessun dettaglio nascosto in modo fuorviante; domanda realmente giustificata se presente; nessuno schema seriale; lingua naturale; metadati coerenti. La valutazione di stile è editoriale: un semplice conteggio di `?` o della parola «cosa» non basta.

## 8. ESEMPI DI STILE

Esempi illustrativi, da usare soltanto se tutti i fatti indicati sono verificati:

- Evitare la formula generica «Corporate MBA, cosa c'era in palio»; preferire «CDP-Luiss, 1.200 candidature per 40 posti nel Corporate MBA».
- «Sciopero ferroviario, stop dalle 11 alle 14» è un titolo valido se ambito e orari sono confermati: non va trasformato in «quali treni si fermano» solo per creare suspense.
- «La missione rientra dopo sei mesi in orbita» crea interesse attraverso il fatto, senza domanda né coda artificiale.
- «Come funziona il voto per gli italiani all'estero» è ammissibile per una guida che spiega davvero la procedura, non come modello per tutte le notizie.

## MODIFICHE DELLA VERSIONE 2.0

Curiosità facoltativa; titoli diretti ammessi e ordinari; abolita la regola 70/30; domande solo motivate, comprese quelle indirette; confronto con gli ultimi 10 titoli e il lotto; forme scelte sui fatti; lunghezza indicativa; accuratezza e servizio prima del clic. Nessuna modifica retroattiva automatica agli articoli pubblicati.
