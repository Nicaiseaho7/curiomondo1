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

- **Titolo (H1):** informativo, senza clickbait, coerente col fatto.
- **Sommario (`.subtitle`):** uno o due elementi non già nel titolo.
- **Lead:** primo paragrafo di `.art-body`. Si regge da solo.
- **Corpo:** `.art-body` con `data-editorial-protocol="4.0"` e `data-article-format` (`flash` | `standard` | `feature`). I nuovi articoli **non** dichiarano `data-length-policy="3000-7000"`.
- **Sottotitoli H2/H3:** ammessi in `.art-body` solo se informativi e utili alla lettura. Vietati i titoletti generici. Obbligatori negli approfondimenti `feature` quando aiutano a orientarsi.
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

Nel corpo sono vietati elenchi di testate, note sul fact-checking, `Fonti:`, `Fonte primaria:`, `Conferma:`, `Letture:`, `Europe/Rome`, orari di lavorazione, «al momento della verifica», «nei testi consultati», «le testate allineano», «fonti riportate in fondo».

Il nome di una fonte nel corpo è ammesso solo se indispensabile: citazione, dato esclusivo, distinzione tra ricostruzione e atto ufficiale.

## Divieti nel testo pubblico

Appunti redazionali, istruzioni operative, «non confondere», «chi cerca», «niente articolo», «da quelle query», contenuti fuori tema, ripetizioni dello stesso fatto o cifra.

Ogni paragrafo deve riguardare il fatto, una conseguenza, un dato necessario o un precedente pertinente. Se eliminandolo il lettore non perde nulla sulla notizia, eliminarlo.

## Fatti e incertezze

Non presentare come fatto promesse, proposte, stime, indiscrezioni. Usare «ha annunciato», «secondo il comunicato», «il testo non è ancora stato pubblicato», «la cifra è una stima».

## Controllo bloccante predeploy

`tools/predeploy.py` analizza `.art-body` degli articoli v4 e blocca il deploy se trova le espressioni vietate o frasi duplicate. I nomi delle fonti restano obbligatori in `.art-sources`.
