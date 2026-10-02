# Protocollo redazione corpo articolo — CurioMondo

**Stato:** obbligatorio, fail-closed  
**Data:** 22 settembre 2026  
**Prevalenza scrittura:** `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md` (v502). Questo file resta il contratto tecnico del markup pubblico. Non sostituisce il protocollo qualità, il protocollo immagini né il gate di rischio v471.

La velocità non prevale sulla qualità. Se le informazioni verificate non bastano per un articolo completo e originale: `NON PUBBLICARE`.

## Principio

Il testo pubblico segue lo standard professionale in `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md`.

Non ottimizzare il testo per «sembrare un giornale». Ottimizzarlo per essere utile al lettore.

Ogni articolo deve comunicare subito il fatto, distinguere fatti da dichiarazioni e stime, spiegare conseguenze concrete senza commenti, aggiungere informazioni rispetto al titolo, restare adulto e sobrio, e terminare quando terminano i fatti.

Nel corpo pubblico non devono mai comparire appunti interni, verifiche automatiche, elenchi di testate, timestamp di lavorazione o conversazioni tra redattori.

## Markup

- **Titolo (H1):** secondo `PROTOCOLLO-TITOLI-CTR.md` v2.1. Informativo e professionale, con un motivo concreto e veritiero per approfondire, fondato su dettagli, dati, contrasti, conseguenze, limiti o utilità documentati. Può già dare il fatto principale; domande solo motivate, nessuno schema seriale «cosa…». Test del titolo isolato su Google e della promessa mantenuta. Il sommario aggiunge dettagli, non recupera informazioni nascoste per il clic.
- **Sommario (`.subtitle`):** uno o due elementi non già nel titolo.
- **Lead:** primo paragrafo di `.art-body`. Si regge da solo.
- **Corpo:** `.art-body` con `data-editorial-protocol="4.0"` e `data-article-format` (`flash` | `standard` | `feature`). I nuovi articoli **non** dichiarano `data-length-policy="3000-7000"`.
- **Sottotitoli H2/H3:** **vietati** nelle notizie (`notizie/*.html`, flash e standard). Ammessi solo negli approfondimenti evergreen/feature se informativi. Vietati i titoletti generici.
- **Fonti:** soltanto in `.art-sources`, fuori da `.art-body`.
- **Evergreen:** blocco `.cm-evergreen-reader` sotto l’articolo, mai nel corpo della notizia.

## Lunghezza

La lunghezza dipende dalla materia verificata. Vietato allungare per quota.

Orientamento di formato, non obiettivo:

- flash: circa 100–250 parole;
- standard: circa 300–700 parole;
- approfondimento: 800+ soltanto se la materia lo richiede.

Sotto le 300 parole dopo la revisione: flash, non ripetizioni. Se manca materia anche per un flash: non pubblicare.

## Tono

Italiano professionale, naturale, preciso. Verbi diretti. Niente prima persona editoriale («abbiamo verificato», «non pubblichiamo», «restiamo sulle conferme», «riteniamo»).

## Fonti nel corpo

**VIETATO** nel corpo dell'articolo (`.art-body`), in qualsiasi forma:

- paragrafi o frasi finali del tipo `Fonte: …`, `Fonti: …`, `Fonte primaria: …`, `Fonti consultate: …`;
- elenchi di testate a fine pezzo («Fonte: ANSA, Reuters, BBC»);
- note sul fact-checking, `Conferma:`, `Letture:`, `Europe/Rome`, orari di lavorazione, «al momento della verifica», «nei testi consultati», «le testate allineano», «fonti riportate in fondo».

Le fonti con link stanno **solo** nella sezione dedicata **«Fonti consultate»** (`.art-sources`), già presente sotto l'articolo. **Non** ripetere le fonti nel testo.

Il nome di una fonte nel corpo è ammesso **solo** se indispensabile per l'attribuzione giornalistica *dentro* la frase (citazione, dato esclusivo, distinzione tra ricostruzione e atto ufficiale), es.: «secondo il bollettino Mimit…», «la FIGC ha comunicato…». Mai come riga separata `Fonte: …`.

## Divieti nel testo pubblico

Appunti redazionali, istruzioni operative, «non confondere», «chi cerca», «niente articolo», «da quelle query», contenuti fuori tema, ripetizioni dello stesso fatto o cifra.

Ogni paragrafo deve riguardare il fatto, una conseguenza, un dato necessario o un precedente pertinente. Se eliminandolo il lettore non perde nulla sulla notizia, eliminarlo.

## Fatti e incertezze

Non presentare come fatto promesse, proposte, stime, indiscrezioni. Usare «ha annunciato», «secondo il comunicato», «il testo non è ancora stato pubblicato», «la cifra è una stima».

## Controllo bloccante predeploy

`tools/predeploy.py` analizza `.art-body` degli articoli v4 e blocca il deploy se trova le espressioni vietate o frasi duplicate. I nomi delle fonti restano obbligatori in `.art-sources`.

## Sottotitoli H2/H3 nelle notizie — VIETATI (27 settembre 2026)

**Nelle pagine `notizie/*.html` (flash e standard) i sottotitoli H2/H3 nel corpo `.art-body` sono vietati.**
Il pezzo scorre solo a paragrafi (e liste solo se indispensabili per candidati/orari).
I sottotitoli H2/H3 restano ammessi **solo** negli **approfondimenti** evergreen (`approfondimenti/` o formato feature), quando orientano una guida lunga.
Non inserire mai titoletti del tipo «Il contesto», «Cosa sappiamo», «Il punto» nelle notizie.
Violazione = articolo da correggere prima del go-live.


## Vietati i commenti personali / meta della redazione nel corpo — 27 settembre 2026

Nelle **notizie** (`notizie/*.html`) è **vietato** inserire nel corpo `.art-body` frasi meta, di metodo o di «voce CurioMondo», ad esempio:
- «CurioMondo segue il caso con sobrietà…»
- «CurioMondo aggiorna solo su fatti di agenzia…»
- «CurioMondo non pubblica dettagli…»
- «Non anticipiamo sentenze…» / «Aggiorneremo solo con fonti…»
- qualsiasi chiusura in prima persona redazionale o auto-elogio del metodo

Il pezzo racconta **fatti, contesto e fonti**. Metodo, disclosure IA e firma stanno **solo** in `art-sources` / footer / pagine istituzionali (`Come lavoriamo`), non nei paragrafi della notizia.
Violazione = correggere prima del go-live.


## Immagini incidenti / morti sul lavoro — vietati rottami e scene macabre (27 settembre 2026)

Nelle hero e illustrazioni di **notizie su incidenti stradali, morti sul lavoro, cantieri, investimenti, incidenti autostradali**:
- **MAI** auto rovesciate, carcasse, lamiere contorte, vetri infranti in primo piano, sangue, corpi, barelle, scene di soccorso gore o “re-enactment” spettacolari dell’incidente.
- **Sì** a immagini sobrie di contesto: cantiere segnalato, coni e luci, tratto di strada vuoto, barriere, autostrada di notte **senza** veicolo incidentato.
- Niente targhe (anche inventate) su qualsiasi veicolo.
- Tone: documentario, rispettoso della vittima, non tabloid.

Violazione = rigenerare l’immagine e aggiornare hero/og prima del go-live. **Non deve più succedere.**
