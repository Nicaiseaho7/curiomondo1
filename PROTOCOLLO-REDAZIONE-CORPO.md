# Protocollo redazione corpo articolo — CurioMondo

**Stato:** obbligatorio, fail-closed  
**Data:** 18 settembre 2026  
**Prevalenza:** sul testo pubblico di ogni notizia; non sostituisce `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md` né il protocollo immagini.

La velocità non prevale sulla qualità. Se le informazioni verificate non bastano per un articolo completo e originale: `NON PUBBLICARE`.

## Principio

Non ottimizzare il testo per «sembrare un giornale». Ottimizzarlo per essere utile al lettore.

Ogni articolo deve comunicare subito il fatto, distinguere fatti da dichiarazioni e stime, spiegare conseguenze concrete senza commenti, aggiungere informazioni rispetto al titolo, restare adulto e sobrio, e terminare quando terminano i fatti.

Nel corpo pubblico non devono mai comparire appunti interni, verifiche automatiche, elenchi di testate, timestamp di lavorazione o conversazioni tra redattori.

## Struttura

- **Titolo:** informativo, senza clickbait, coerente col fatto.
- **Sommario:** uno o due elementi non già nel titolo.
- **Lead:** chi, cosa, quando, dove, perché e conseguenze immediate, quando noti. Si regge da solo.
- **Corpo:** piramide invertita. Un’idea per paragrafo, 2–4 frasi, massimo 60 parole, almeno un’informazione nuova.
- **Chiusura:** prossimo passaggio, scadenza, precedente o ciò che resta da accertare. Vietate morali, opinioni, riepiloghi del lead.

Formati: flash 100–250 parole; standard 300–600; approfondimento 800–1.500 o più solo se la materia lo richiede. Non allungare con riempitivi. Sotto le 300 parole dopo la revisione: flash, non ripetizioni.

## Tono

Italiano professionale, naturale, preciso. Verbi diretti. Niente prima persona editoriale («abbiamo verificato», «non pubblichiamo», «restiamo sulle conferme», «riteniamo»).

## Fonti nel corpo

Le fonti complete stanno solo in **Fonti consultate** (`.art-sources`), fuori da `.art-body`. L’eventuale approfondimento evergreen sta sotto l’articolo nel blocco `.cm-evergreen-reader`, mai nel corpo della notizia.

Nel corpo sono vietati elenchi di testate, note sul fact-checking, `Fonti:`, `Fonte primaria:`, `Conferma:`, `Letture:`, `Europe/Rome`, orari di lavorazione, «al momento della verifica», «nei testi consultati», «le testate allineano», «fonti riportate in fondo».

Il nome di una fonte nel corpo è ammesso solo se indispensabile: citazione, dato esclusivo, distinzione tra ricostruzione e atto ufficiale.

## Divieti nel testo pubblico

Appunti redazionali, istruzioni operative, «non confondere», «chi cerca», «niente articolo», «da quelle query», contenuti fuori tema, ripetizioni dello stesso fatto o cifra.

Ogni paragrafo deve riguardare il fatto, una conseguenza, un dato necessario o un precedente pertinente. Se eliminandolo il lettore non perde nulla sulla notizia, eliminarlo.

## Fatti e incertezze

Non presentare come fatto promesse, proposte, stime, indiscrezioni. Usare «ha annunciato», «secondo il comunicato», «il testo non è ancora stato pubblicato», «la cifra è una stima».

## Controllo bloccante predeploy

`tools/predeploy.py` analizza `.art-body` degli articoli v4 e blocca il deploy se trova le espressioni vietate o frasi duplicate. I nomi delle fonti restano obbligatori in `.art-sources`.
