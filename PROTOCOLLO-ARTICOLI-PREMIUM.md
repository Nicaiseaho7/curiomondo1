# CurioMondo — Protocollo articoli premium

**Versione:** 1.0  
**Data:** 4 ottobre 2026  
**Stato:** obbligatorio per ogni nuovo articolo e per ogni revisione sostanziale richiesta  
**Ambito:** notizie, aggiornamenti, analisi e articoli premium in `/notizie/`  

Questo protocollo porta negli articoli di attualità lo stesso livello di cura già richiesto agli approfondimenti, senza trasformare ogni notizia in una guida e senza imporre una struttura ripetitiva.

## 1. Promessa editoriale

Un articolo CurioMondo deve aiutare il lettore a capire:

- che cosa è successo;
- che cosa è confermato e da chi;
- che cosa significa concretamente;
- quale sviluppo è ragionevole seguire.

La velocità conta, ma non sostituisce verifica, utilità e chiarezza. La lunghezza, da sola, non rende premium un articolo.

## 2. Prevalenza e compatibilità

Questo file integra, senza sostituirli, i protocolli di scrittura, titoli, scoperta, rischio, qualità, corpo, immagini e pubblicazione tecnica.

- Il gate di rischio v471 determina quante conferme servono.
- `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md` governa la qualità della prosa.
- `PROTOCOLLO-TITOLI-CTR.md` governa i titoli.
- `PROTOCOLLO-REDAZIONE-CORPO.md` governa markup, fonti fuori dal corpo e divieti H2/H3 nelle notizie.
- `AI-EDITORIAL-IMAGE-PROTOCOL.md` e il contratto immagini governano generazione, trasparenza e sicurezza dei visual.

In caso di conflitto sulle fasce di lunghezza o sulla struttura editoriale delle notizie nuove, prevale questo protocollo. Restano prevalenti tutte le regole più restrittive su accuratezza, sicurezza, privacy, immagini sensibili, fonti e integrità tecnica.

## 3. Selezione: non coprire tutto

Prima di scrivere, verificare che la storia abbia almeno una domanda reale del lettore e almeno una possibilità concreta di valore originale. Sono segnali positivi:

- esiste una fonte primaria o ufficiale pertinente;
- la conseguenza pratica non è evidente dal lancio iniziale;
- dati, documenti o dichiarazioni possono essere confrontati;
- il tema ha interesse durevole o si collega a un approfondimento utile;
- l'evento può richiedere aggiornamenti sostanziali;
- CurioMondo può chiarire un punto che altri articoli lasciano ambiguo.

Non pubblicare in serie contenuti generici, intercambiabili o ottenuti con semplice riscrittura. La quantità non deve produrre pagine prive di apporto editoriale.

## 4. Formati proporzionati

Le fasce sono orientative e non sono obiettivi SEO né minimi da riempire:

| Formato | Orientamento | Uso |
|---|---:|---|
| Flash verificato | circa 250–450 parole | Un fatto circoscritto, con conferma e conseguenza essenziale |
| Notizia completa | circa 700–1.200 parole | Fatto, riscontri, contesto e impatto concreto |
| Articolo premium | circa 1.200–2.200 parole | Più documenti, confronto, analisi originale o conseguenze articolate |
| Evento in evoluzione | lunghezza variabile | Pagina aggiornata quando emergono fatti sostanziali |

Un contenuto può essere più corto o più lungo quando la materia lo richiede. Vietati riempitivo, ripetizioni, definizioni ovvie e conclusioni che ricapitolano quanto già detto.

## 5. Flusso a due velocità

Per una notizia urgente:

1. pubblicare una prima versione breve ma verificata, con ciò che è certo e ciò che manca;
2. arricchire la stessa pagina con documenti, conferme, contesto e conseguenze quando arrivano nuove informazioni affidabili.

Non aprire un nuovo URL per ogni dettaglio dello stesso evento. Creare un nuovo articolo soltanto quando cambia davvero l'angolazione, il pubblico, la conseguenza o l'utilità.

## 6. Contributo originale

Ogni articolo importante deve offrire almeno un contributo che non sia la semplice parafrasi delle fonti. Per un articolo dichiarato premium il contributo originale è obbligatorio e sostanziale. Esempi:

- confronto tra documenti ufficiali o versioni differenti;
- timeline verificata;
- tabella di dati selezionati e spiegati;
- calcolo originale riproducibile;
- ricostruzione geografica o procedurale;
- conseguenza concreta per persone, territori, imprese o istituzioni;
- precedente pertinente, spiegato senza analogie forzate;
- distinzione documentata tra dichiarato, confermato e ancora incerto;
- collegamento a un approfondimento evergreen realmente utile.

Il contributo deve essere visibile nel testo e sostenuto dalle fonti; non basta dichiararlo negli appunti redazionali.

## 7. Livelli di certezza

Durante la ricerca classificare ogni informazione rilevante come:

- confermata da documento o fonte primaria;
- dichiarata da una parte interessata;
- confermata in modo indipendente;
- ricostruzione plausibile ma non definitiva;
- non ancora verificata;
- smentita, corretta o superata.

Nel testo pubblico usare attribuzioni naturali e precise. Non trasformare dichiarazioni, indiscrezioni, proposte o stime in fatti. Le etichette interne non vanno riversate meccanicamente nel corpo.

## 8. Composizione libera, non seriale

**Non esiste una sequenza obbligatoria di sezioni.** È vietato imporre a tutti i pezzi una struttura riconoscibile e ripetitiva del tipo «che cosa è successo / cosa sappiamo / perché conta / cosa succede ora».

La storia determina ordine, ritmo e profondità. Il lead deve comunque dare subito il fatto principale; il resto segue la logica più utile al lettore. Nelle notizie restano vietati H2/H3 e titoletti seriali secondo `PROTOCOLLO-REDAZIONE-CORPO.md`.

Timeline, tabelle, documenti, box o altri moduli sono facoltativi: usarli solo quando rendono un'informazione più comprensibile. Non devono diventare una gabbia grafica o un riempitivo.

## 9. Titolo, sommario e apertura

- Il titolo contiene il soggetto, il fatto nuovo e, quando utile, la conseguenza o il dettaglio distintivo.
- L'attribuzione entra nel titolo quando è necessaria per non presentare come certo ciò che è soltanto dichiarato.
- Il sommario aggiunge uno o due elementi informativi; non ripete il titolo.
- Il lead si regge da solo, risponde alle domande essenziali note e non trattiene informazioni per creare suspense.
- Vietati clickbait, vaghezza artificiale, formule seriali e promessa più ampia del contenuto.

## 10. Aggiornamenti e freschezza reale

- Conservare sempre la `datePublished` originaria.
- Modificare `dateModified` soltanto per aggiornamenti sostanziali, non per refusi o ritocchi cosmetici.
- Non cambiare la data per simulare freschezza.
- Se utile, mostrare con misura uno stato chiaro: `In aggiornamento`, `Aggiornato alle`, `Notizia conclusa`, `Analisi` o `Verifica completata`.
- Per eventi complessi usare un registro degli aggiornamenti soltanto quando aiuta il lettore a capire che cosa è cambiato; non aggiungerlo a ogni pagina.
- Correggere gli errori in modo trasparente e distinguere una correzione da un normale ampliamento.

Tutti gli orari editoriali sono in `Europe/Rome` e devono essere esatti.

## 11. Fiducia, firma e fonti

Ogni articolo deve mostrare una firma reale o una firma redazionale esplicita, con collegamento alla pagina autore o al metodo editoriale quando disponibile. Non inventare autori, qualifiche o competenze.

Le fonti devono essere pertinenti, accessibili e raggruppate nella sezione `.art-sources`, fuori da `.art-body`, distinguendo quando utile:

- documenti e fonti primarie;
- comunicati o dichiarazioni delle parti;
- conferme indipendenti;
- materiali di contesto.

Nel corpo si attribuisce la fonte solo quando è giornalisticamente necessario. Restano vietati elenchi `Fonte:` nel testo e commenti autocelebrativi sul metodo CurioMondo.

La pagina `Come lavoriamo` deve spiegare metodo, correzioni, uso dell'IA e responsabilità editoriale. L'eventuale assistenza IA non sostituisce verifica, controllo umano/editoriale e responsabilità sul testo pubblicato.

## 12. Layout editoriale premium

L'identità CurioMondo resta blu, bianca, pulita e leggibile. Questo protocollo non autorizza varianti locali incoerenti né un ridisegno improvvisato dei template.

### Sopra la piega

Quando il template lo supporta, l'ordine visivo raccomandato è:

- categoria compatta;
- titolo;
- sommario di massimo due righe su desktop quando la sintesi lo consente;
- autore, pubblicazione e ultimo aggiornamento sostanziale;
- hero editoriale;
- riga compatta `Ascolta`, `Salva`, `Condividi` se le funzioni sono realmente disponibili.

Nessun annuncio tra titolo e sommario, né prima della risposta essenziale promessa dal titolo.

### Corpo di lettura

- Colonna principale indicativa: 700–740 px su desktop.
- Corpo tipografico indicativo: 18–20 px su desktop, con interlinea generosa e lunghezza di riga controllata.
- Niente sidebar permanente che comprima la lettura; un modulo contestuale laterale è ammesso solo se offre utilità reale e scompare correttamente su mobile.
- Paragrafi brevi ma non telegrafici; una sola idea informativa per paragrafo.
- Evitare sequenze di box, badge o callout che frammentano il racconto.

### Moduli facoltativi

Sono ammessi, solo se sostenuti dalla storia e dal template esistente:

- dato o documento chiave;
- timeline;
- tabella comparativa;
- mappa o calcolo;
- elementi confermati e ancora da verificare;
- conseguenza concreta o cambiamento operativo;
- aggiornamenti cronologici.

Nessun modulo è obbligatorio. Nelle notizie non deve introdurre H2/H3 vietati né etichette generiche come «Perché conta davvero».

### Correlati

Mostrare al massimo tre collegamenti realmente pertinenti: di norma un approfondimento evergreen, un precedente necessario e uno sviluppo successivo. Non usare correlati generici per aumentare artificialmente le pagine viste.

## 13. Immagini e formati

Per le nuove notizie, l'hero predefinita è panoramica **16:9**, larga almeno **1.200 px**, originale e dedicata. Deve funzionare anche nei ritagli mobile e card senza perdere il soggetto.

Per approfondimenti e guide evergreen resta preferibile il formato **3:2**, salvo esigenza editoriale diversa.

Quando la pipeline lo consente, produrre o dichiarare varianti ad alta risoluzione in 16:9, 4:3 e 1:1 per dati strutturati e distribuzione, mantenendo lo stesso soggetto e senza creare crop ingannevoli. Non duplicare asset soltanto rinominandoli.

Restano obbligatori `og:image`, hero e immagine nei dati strutturati coerenti, alt text descrittivo, disclosure IA, controllo visivo, soggetto pertinente e tutte le regole di sicurezza del protocollo immagini.

## 14. Pubblicità e stabilità della pagina

- Il primo annuncio può comparire soltanto dopo un blocco informativo completo.
- Non interrompere tabelle, timeline, documenti, citazioni o box essenziali.
- Riservare in anticipo le dimensioni degli spazi pubblicitari per evitare salti di layout.
- Gli annunci non devono coprire testo, controlli, fonti o navigazione e non devono provocare clic accidentali.
- Vietati interstitial aggressivi e accumuli pubblicitari sopra la piega.

## 15. Mobile e accessibilità

- Titolo, metadati e hero devono restare compatti e leggibili su schermi piccoli.
- Pulsanti e link devono avere aree di tocco sufficienti e focus visibile.
- Le tabelle possono scorrere orizzontalmente, con un segnale visivo chiaro; non devono uscire dalla pagina.
- Nessuna barra fissa deve coprire il testo o i controlli.
- Contrasto, semantica HTML, ordine di lettura, alt text e modalità scura sono requisiti, non rifiniture.
- Rispettare `prefers-reduced-motion`; evitare animazioni decorative.

## 16. Prestazioni e dati strutturati

Obiettivi al 75° percentile, su mobile e desktop:

- LCP non superiore a 2,5 secondi;
- INP inferiore a 200 millisecondi;
- CLS inferiore a 0,1.

Ogni notizia deve usare dati strutturati `NewsArticle` coerenti con la pagina, includendo almeno headline concisa, autore, `datePublished`, `dateModified` reale, publisher e immagini pertinenti. La News Sitemap include soltanto le notizie ammissibili degli ultimi due giorni; la sitemap generale conserva gli URL editoriali indicizzabili.

Usare `max-image-preview:large` e metadati social coerenti quando già previsti dal template. Non introdurre script, font o librerie decorative che peggiorino la pagina senza un beneficio editoriale misurabile.

## 17. Cose da evitare

- gradienti usati ovunque;
- badge per ogni informazione;
- caroselli dentro l'articolo;
- animazioni decorative;
- più box consecutivi;
- gerarchie di titoli incoerenti;
- immagini generiche o piene di testo;
- date modificate per sembrare recenti;
- citazioni o numeri senza attribuzione;
- contenuti seriali che cambiano solo nomi e dettagli.

## 18. Punteggio premium su 100

Applicare questa griglia agli articoli esplicitamente classificati come `premium` o `feature`:

| Area | Punti |
|---|---:|
| Accuratezza e qualità delle fonti | 25 |
| Informazione o elaborazione originale | 20 |
| Chiarezza e qualità della scrittura | 15 |
| Contesto e conseguenze | 15 |
| Titolo e immagine | 10 |
| Fiducia e trasparenza | 10 |
| Qualità tecnica e page experience | 5 |
| **Totale** | **100** |

Soglia premium: **85/100**. Accuratezza, legalità, sicurezza, attribuzione e trasparenza sono requisiti bloccanti e non possono essere compensate da punti ottenuti altrove.

Flash e notizie ordinarie non devono raggiungere artificialmente 85/100: devono superare i gate proporzionati v471/v503 e rispettare tutti i requisiti bloccanti.

## 19. Misurazione editoriale

Per i primi dieci articoli prodotti con questo standard registrare, quando disponibili:

- CTR da homepage, ricerca e Discover;
- tempo di lettura attivo e profondità di scorrimento;
- ritorni sulla stessa pagina dopo un aggiornamento;
- accessi agli approfondimenti collegati;
- impression, clic e query in Search Console;
- errori, correzioni e tempi di pubblicazione.

Dopo i primi dieci articoli riesaminare formati, moduli e soglia premium. Non abbassare accuratezza o trasparenza per migliorare una metrica.

## 20. Checklist prima della pubblicazione

- [ ] Il titolo mantiene integralmente la promessa?
- [ ] Il fatto principale è chiaro nel lead?
- [ ] Ogni affermazione sensibile ha il livello di conferma richiesto?
- [ ] È evidente almeno un contributo originale per i pezzi importanti?
- [ ] La composizione è scelta per questa storia e non copiata da uno schema fisso?
- [ ] Non ci sono ripetizioni, riempitivo o conclusioni-riepilogo?
- [ ] `datePublished` e `dateModified` descrivono la storia reale della pagina?
- [ ] Firma, fonti, correzioni e uso dell'IA sono trasparenti?
- [ ] Hero, metadati e dati strutturati sono coerenti?
- [ ] Layout, annunci, mobile, accessibilità e Core Web Vitals sono protetti?
- [ ] Correlati ed evergreen sono pochi e realmente utili?
- [ ] I gate di integrità, AdSense e predeploy passano senza errori?

## 21. Riferimenti tecnici primari

- Google Search Central, contenuti utili e affidabili: <https://developers.google.com/search/docs/fundamentals/creating-helpful-content>
- Google Search Central, contenuti idonei a Discover: <https://developers.google.com/search/docs/appearance/google-discover>
- Google Search Central, norme antispam e abuso di contenuti su larga scala: <https://developers.google.com/search/docs/essentials/spam-policies>
- Google Search Central, dati strutturati Article/NewsArticle: <https://developers.google.com/search/docs/appearance/structured-data/article>
- Google Search Central, News Sitemap: <https://developers.google.com/search/docs/crawling-indexing/sitemaps/news-sitemap>
- web.dev, Core Web Vitals: <https://web.dev/articles/vitals>
