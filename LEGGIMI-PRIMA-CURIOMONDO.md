# CurioMondo — stato del pacchetto

**Versione:** v248  
**Data:** 30 agosto 2026  
**Baseline verificata:** `curiomondo-v230-29-agosto-2026-netlify.zip`

Questo ZIP contiene il sito statico completo pronto per il caricamento manuale su Netlify. Non usa un comando di build, `netlify.toml`, Netlify Functions, `package.json` o dipendenze Node. È un output statico già pronto: va caricato direttamente nella zona Deploys/drag-and-drop del sito Netlify.

## Aggiornamento editoriale v171

- Domanda del giorno del 25 agosto mantenuta: “Che cosa stai proteggendo quando preferisci avere ragione invece di capire chi hai davanti?”.
- Nuova notizia mondo: estensione delle sanzioni statunitensi all’Iran e risposta annunciata da Teheran.
- Nuova notizia Italia: Roma non parteciperà alle esercitazioni autunnali della Coalizione dei Volenterosi, pur mantenendo sostegno politico e umanitario all’Ucraina.
- Due nuove immagini editoriali WebP generate con IA, dichiarate nelle pagine e ottimizzate a 960×720.
- Aggiornati homepage, LIVE, In evidenza, archivio, ricerca, feed RSS, sitemap generale e Google News Sitemap.

## Regole operative

Il protocollo obbligatorio è in `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`; lo stato macchina è in `curiomondo-site-manifest.json` e `CURIOMONDO-RELEASE-STATE.json`.

Prima di distribuire una versione futura eseguire:

```bash
python3 tools/predeploy.py
```

Il comando deve terminare con exit code 0. La pubblicazione Netlify prevista per questo pacchetto è un caricamento statico manuale.

## Aggiornamento editoriale v189

- Quattro nuove notizie verificate: alluvione lampo Nepal–Tibet, incendio nella nursery dell’ospedale di Islamabad, accordo Meta da massimo 16,68 miliardi di dollari e morte di Dolly Parton.
- Cinque nuovi visual editoriali fotorealistici generati con IA, unici e dichiarati con la disclosure completa obbligatoria.
- Nuovo approfondimento evergreen indicizzabile sulle piene dei laghi glaciali, collegato in entrambe le direzioni alla notizia Nepal–Tibet.
- Aggiornati homepage, LIVE, Ultima ora, Ultime notizie, archivio, ricerca, Approfondimenti, feed RSS, sitemap e Google News Sitemap.
- Pacchetto statico deploy-only: nessun `netlify.toml`, `package.json`, framework o build Netlify.

## Hotfix tecnico v190

- Ripristinato il contenitore animato della barra LIVE, che ora mostra e fa scorrere correttamente le 10 notizie.
- Resi affidabili click e tap sui titoli LIVE durante l'animazione, con pausa al passaggio/focus e supporto da tastiera.
- Verificati i collegamenti interni della homepage e dell'intero pacchetto: nessuna destinazione mancante.

## Redesign Domanda del giorno v191

- La risposta del 26 agosto è ora impaginata come un editoriale premium, con veri paragrafi semantici e ritmo di lettura da rivista.
- Apertura, principio centrale e domanda da portare con sé hanno una gerarchia distinta senza modificare il significato del testo.
- Migliorati contrasto, spaziatura, resa mobile, modalità scura e invito all’eBook collegato.
- Registrata come regola permanente la tipografia editoriale premium per tutte le future risposte della Domanda del giorno.
- Aggiunta la copertina premium mancante all’eBook del 26 agosto: il libro apre ora sulla copertina e continua con le 10 pagine di lettura.
- Riparati i controlli `← Indietro` e `Avanti →`, ora collegati al lettore anche nelle pagine legacy prive dell’attributo di inizializzazione.

## Audit click e layout unificato v192

- Corretto il vero punto di rottura dei mini eBook legacy: il lettore ora riconosce sia la struttura moderna sia quella storica e collega sempre i pulsanti `← Indietro` e `Avanti →` alle pagine.
- Copertina, pagina attiva, contatore, stati disabilitati e accessibilità dei controlli sono gestiti dallo stesso lettore condiviso in tutti gli eBook.
- Biblioteca, categorie, guide, manuali, eBook e tutte le risposte della Domanda del giorno usano ora lo stesso sistema premium bianco, blu CurioMondo e navy.
- Eliminati dal lettore effetti 3D e page-flip residui: la navigazione resta esclusivamente tramite i due grandi pulsanti blu.
- Aggiornati gli asset a `v192` per evitare cache di vecchi fogli stile o script.
- Eseguiti audit su link interni, pulsanti, controlli dinamici, destinazioni e struttura del pacchetto statico Netlify.

## Aggiornamento editoriale v172

- Nuovo approfondimento: Coalizione dei Volenterosi e scopo delle esercitazioni.
- Nuovo approfondimento: funzionamento e controlli del voto postale negli Stati Uniti.
- Nuova regola permanente: ogni concetto non immediato nelle notizie deve avere una guida autonoma, chiara e collegata in entrambe le direzioni.


## v176 — Biblioteca, eBook e immagini editoriali
Palette definitiva Biblioteca/eBook: premium bianco + blu CurioMondo; eliminato il bianco-verde come identità dominante. Tutte le pagine Biblioteca caricano gli asset v176. Regola immagini rafforzata: ogni nuova notizia e ogni aggiornamento deve avere un visual completamente nuovo; vietati riuso, crop, resize, filtri o rinomina di asset già pubblicati. Il predeploy controlla l'unicità degli hero e blocca duplicati binari. Restano: risposta Domanda del giorno 1.000–3.000 caratteri, eBook 15.000–30.000 caratteri con sfoglio 3D realistico, 2 guide premium quotidiane da 3.000–15.000 caratteri e categorizzazione obbligatoria.

## v177 — correzione obbligatoria fotorealismo hero
Sostituiti gli hero del 25 agosto (Verona/Cerea, Andora, Salvini/manovra e SAFE) con visual fotorealistici nuovi. Rafforzato il protocollo: flat/vector/silhouette/pittogrammi/infografiche/mockup/collage sono errori bloccanti per gli hero delle notizie. Gli asset hanno nomi nuovi per evitare cache delle immagini precedenti.


## Prompt immagini IA obbligatorio
Prima di creare o aggiornare qualunque articolo, leggere `automation/prompts/image-generation-contract.txt`. È il contratto canonico e machine-readable per la generazione delle immagini editoriali e la disclosure IA.

## Protocollo personaggi pubblici e somiglianza sintetica v234
Prima di generare immagini con persone pubbliche, leggere anche `AI-EDITORIAL-IMAGE-PROTOCOL.md`. CurioMondo autorizza persone pubbliche riconoscibili, viventi o decedute, in immagini ultrarealistiche direttamente pertinenti alla notizia. Nelle notizie ordinarie sono ammessi posti, luoghi, ambientazioni e loghi coerenti. Soltanto per incidenti, morte, salute, violenza, tragedie, lutto, sofferenza e altre situazioni sensibili è obbligatorio un ritratto neutrale isolato, senza rappresentare il momento doloroso. Le immagini restano illustrazioni editoriali IA dichiarate e non documentarie.


## Disclosure immagini IA
Le immagini editoriali devono restare pulite, senza testo sovrapposto. La dicitura “Immagine illustrativa generata con IA” o “Creato da IA” va sempre inserita subito sotto la foto come figcaption HTML visibile.

### Regola disclosure immagini e approfondimenti
- Sotto ogni immagine IA articolo usare esattamente: `Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.`
- `Una cosa utile da sapere` è un inserto interno consigliato/obbligatorio quando utile, ma sulla maggior parte delle notizie va inoltre creato o collegato un approfondimento evergreen indicizzabile.
- Tutte le pagine editoriali pubbliche devono essere indicizzabili.
- Biblioteca/eBook: niente page-flip o swipe; navigazione soltanto con grandi controlli blu `Indietro` e `Avanti` sotto la pagina.

## v248 — nuova lunghezza articoli e divieto assoluto di ripetizioni
- Dal 30 agosto 2026, ore 10:04 (Europe/Rome), ogni nuovo articolo e ogni aggiornamento sostanziale deve avere **2.000–4.500 caratteri nel corpo `.art-body`**.
- Nessuna eccezione di lunghezza: se non ci sono abbastanza informazioni verificate per 2.000 caratteri senza diluire il testo, non si pubblica un articolo autonomo.
- Ogni fatto e concetto può comparire una sola volta, anche se riscritto con parole diverse. Ogni paragrafo deve aggiungere informazione nuova.
- Vietati riepiloghi finali ridondanti, parafrasi del lead, ripetizioni di cifre già spiegate e frasi di riempimento.
- Il predeploy v248 applica il controllo di lunghezza ai contenuti soggetti alla nuova regola e intercetta duplicazioni testuali evidenti.
