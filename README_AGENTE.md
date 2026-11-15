# Sezione “Scioperi” — pacchetto per CurioMondo.it

Pacchetto locale pronto per l’integrazione nella repository `Nicaiseaho7/curiomondo1`. Non è stato pubblicato nulla e non sono stati modificati file online.

## Contenuto

- `scioperi/index.html`: calendario principale all’indirizzo `/scioperi/`.
- `scioperi/archivio/index.html`: archivio degli eventi conclusi.
- `assets/data/scioperi.json`: unico archivio strutturato di eventi e notizie collegate.
- `assets/js/scioperi-v1.js`: filtri, ricerca, tendine, conteggi, collegamenti diretti e separazione automatica dello storico.
- `assets/css/scioperi-v1.css`: grafica responsive e accessibile.
- `tools/install-scioperi.py`: inserimento idempotente nel menu e nello sitemap.
- `tests/test_scioperi.py`: controlli sui dati, sugli URL e sulle funzioni richieste.

## Installazione consigliata

1. Verificare che la repository sia aggiornata e che il branch sia quello corretto.
2. Estrarre il contenuto dello ZIP nella radice della repository, mantenendo le cartelle.
3. Eseguire prima una simulazione:

   ```bash
   python3 tools/install-scioperi.py --root . --dry-run
   ```

4. Integrare la voce “Scioperi” nel menu e i due URL nello sitemap:

   ```bash
   python3 tools/install-scioperi.py --root .
   ```

5. Eseguire i controlli:

   ```bash
   node --check assets/js/scioperi-v1.js
   python3 tests/test_scioperi.py
   python3 tools/predeploy.py
   ```

6. Controllare il diff prima del commit. Non rinominare né rimuovere URL esistenti. Seguire la regola CurioMondo: un lotto, un commit, un push.

## Come aggiungere uno sciopero

Modificare soltanto `assets/data/scioperi.json` e aggiungere un oggetto nell’array `events`. Non modificare il layout.

Campi obbligatori:

```json
{
  "id": "mit-AAAA-MM-GG-identificativo-stabile",
  "title": "Titolo descrittivo dell’evento",
  "startDate": "AAAA-MM-GG",
  "endDate": "AAAA-MM-GG",
  "startsAt": "AAAA-MM-GGT00:00:00+01:00",
  "endsAt": "AAAA-MM-GGT23:59:00+01:00",
  "scheduleText": "Orario o durata comunicati ufficialmente",
  "sector": "tpl",
  "sectorLabel": "Trasporto pubblico locale",
  "territory": "Territorio coinvolto",
  "services": "Azienda, ente o servizio interessato",
  "organizations": "Organizzazioni proclamanti oppure Non comunicato",
  "status": "proclamato",
  "guarantees": "Fasce ufficiali oppure Non comunicato",
  "national": false,
  "regions": ["lazio"],
  "verifiedAt": "AAAA-MM-GGT00:00:00+01:00",
  "source": {
    "label": "Nome della fonte ufficiale",
    "url": "https://indirizzo-ufficiale.example/"
  },
  "article": null
}
```

Usare solo questi valori per `sector`: `treni`, `aerei`, `tpl`, `marittimo`, `scuola`, `sanita`, `pa`, `altri`.

Usare solo questi valori per `status`: `proclamato`, `confermato`, `modificato`, `rinviato`, `revocato`.

## Come aggiornare, rinviare o revocare

- Trovare l’evento tramite `id` e non cambiarlo: è l’identificativo stabile usato per evitare duplicati.
- Aggiornare soltanto i campi cambiati dalla fonte.
- Impostare `status` su `modificato`, `rinviato` o `revocato`.
- Aggiornare sempre `verifiedAt` con data, ora e offset del fuso Europe/Rome.
- Se cambia data, aggiornare insieme `startDate`, `endDate`, `startsAt`, `endsAt` e `scheduleText`.
- Non cancellare un evento revocato futuro: la pagina deve renderne evidente la revoca. Dopo la data di fine passerà nello storico.

## Come associare più regioni

Inserire una sola volta l’evento e aggiungere gli slug nell’array `regions`, per esempio:

```json
"regions": ["lombardia", "piemonte", "liguria"]
```

Per un vero sciopero nazionale impostare `national: true` e inserire tutte le 20 regioni. L’evento comparirà nella sezione nazionale e nelle regioni coinvolte, ma resterà un solo record con un solo `id`.

## Come collegare una notizia CurioMondo

Sostituire `"article": null` nell’evento con:

```json
"article": {
  "url": "/notizie/slug-articolo.html",
  "title": "Titolo esatto della notizia",
  "summary": "Breve descrizione editoriale.",
  "image": "/assets/images/percorso-immagine-800.webp",
  "imageAlt": "Descrizione informativa dell’immagine"
}
```

Inserire inoltre una sola scheda dello stesso articolo nell’array principale `articles`, con il campo `publishedAt`, per mostrarlo nella sezione “Ultime notizie sugli scioperi”. Nell’articolo aggiungere un link diretto alla regione, ad esempio `/scioperi/#lombardia`, oppure all’evento con `/scioperi/#ID-EVENTO`.

## Archivio automatico

La separazione avviene in fase di visualizzazione: quando `endsAt` è precedente all’ora corrente, l’evento non appare più nel calendario principale e viene mostrato in `/scioperi/archivio/`. Non servono copie né spostamenti manuali e non si generano duplicati.

## Regole editoriali sui dati

- Usare soltanto fonti istituzionali, calendari ufficiali o comunicazioni ufficiali degli enti coinvolti.
- Non trasformare “proclamato” in “confermato” senza una comunicazione ufficiale esplicita.
- Non presentare uno sciopero come disservizio avvenuto: l’adesione effettiva è un dato distinto.
- Se un’informazione manca, scrivere `Non comunicato`.
- Aggiornare l’intestazione `meta.lastVerified` e `meta.verificationLabel` soltanto dopo una verifica effettiva di tutti gli eventi correnti.
- Prima di aggiungere un record, cercare un evento con stessa data, servizio e organizzazioni per evitare duplicati.

## Dati iniziali inclusi

Il file contiene 10 eventi riscontrati nel calendario ufficiale MIT: 6 futuri al momento della verifica e 4 già conclusi utili a testare l’archivio. Tutti gli stati iniziali sono prudentemente indicati come “proclamato”; dove disponibili, le fasce o i servizi garantiti sono attribuiti alla fonte ufficiale.

Ultima verifica effettiva del pacchetto: **15 novembre 2026 alle ore 09:42, Europe/Rome**.
