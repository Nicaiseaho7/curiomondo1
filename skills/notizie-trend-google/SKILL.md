---
name: notizie-trend-google
description: Use when the user wants news driven by rising Google queries in Italy and published on CurioMondo — query in ascesa, ricerche di tendenza, cosa cercano gli italiani oggi, trend del giorno, notizie dalle query Google, pubblica articolo Trends, commit GitHub da Google Trends, scrittura da quotidiano, protocollo CurioMondo. Harvest trending searches, hunt last-hour stories, write like a newspaper under the live repo protocols, then publish. Do not invent search volumes. Never skip AGENTS.md or the editorial protocols.
metadata:
  type: workflow
  version: "1.1"
  geo: IT
  site: curiomondo.it
---

# Notizie Trend Google

## Obiettivo

Un solo ciclo, in quest'ordine:

1. Estrai **ora** le query Google in ascesa in Italia (giornata / ultime ore).
2. Distingui query da notizia. Caccia il fatto fresco dietro le query più forti.
3. Decidi il formato — roundup del giorno e/o notizia singola.
4. Se il gate del sito passa, **scrivi e pubblica** sul repository GitHub. Non fermarti alla bozza in chat.

Questa skill orchestra il radar. Non inventa uno stile. La scrittura e il markup sono quelli del protocollo CurioMondo nel repository, da quotidiano, fail-closed.

## Relazione con le altre skill

- `ricerche-google-italia` — metodo e limiti dei dati Trends. Usala per raccogliere le liste. Non pubblica.
- `ultime-notizie-scoop` — verifica, fonti primarie, commit GitHub. Usala dopo aver scelto le storie. Non parte da Trends.

Se un'istruzione di questa skill collide con `AGENTS.md` o i protocolli del repo, vince il repo.

## Autorizzazione al commit

L'ordine vale come via libera al commit quando l'utente chiede trend del giorno, query in ascesa, «pubblica», «metti online», «aggiorna il sito», «scrivi la notizia e pubblicala».

Stop al commit solo se dice «solo brief», «non pubblicare», o se un gate fallisce.

Default repo, se non ne indica un altro:

- owner `Nicaiseaho7`
- repo `curiomondo1`
- branch `main`
- sito `curiomondo.it`

Usa i tool GitHub collegati. Non inventare un altro deploy.

## Ciclo operativo

### 1. Fissa il radar

Fuso `Europe/Rome`. Annota data, ora di rilevazione, geo `IT`.

Finestra default:

- query — ultime 4–24 ore (Trends «trending now» / ricerche di tendenza)
- fatti di notizia — ultime 0–6 ore, max 24h se il tema è ancora in ascesa e non è già sul sito

Leggi `references/radar-query.md` e, se serve il dettaglio metodologico, il file fonti di `ricerche-google-italia`.

### 2. Raccogli le query

Apri in quest'ordine:

1. https://trends.google.com/trending?geo=IT
2. https://trends.google.it/trending?geo=IT
3. https://trends.google.com/trends/trendingsearches/daily?geo=IT

Usa `web_search` + `browse_page` e, se la pagina è un guscio JS, `browser_tab`. Integra Google News IT solo come contesto di storie collegate, non come «più lette certificate».

Per ogni query annota:

- testo esatto della query
- categoria Trends se c'è
- soglia o breakdown se Trends lo mostra («1.000+», regione) — come bucket Trends, non come volume vero
- storie / query correlate visibili
- ora di aggiornamento della pagina

Se dopo due tentativi la lista odierna non si estrae, dillo. Non inventare una top 10. Pubblicare su reprint datati che citano Trends Italia solo se etichettati come secondari.

### 3. Pulisci e classifica

Scarta o declassa:

- evergreen senza picco (meteo generico, WhatsApp, Gmail, YouTube)
- query identiche già usate in un pezzo del sito nelle ultime 24–48h sullo stesso fatto
- nomi di persone/minori in fatti di cronaca nera senza comunicato
- query sessuali esplicite, insulti, doxxing
- query che sono solo titoli clickbait senza nucleo verificabile

Tieni e ordina le altre con il punteggio in `references/selezione-query.md`.

Due pile:

- Pile A — roundup — query reali del giorno, anche se non tutte diventano un articolo
- Pile B — caccia notizia — solo query con un fatto fresco, impatto per un lettore italiano, e materia sufficiente

### 4. Caccia il fatto (solo Pile B)

Per le prime 3–7 query di Pile B, in parallelo:

1. Cerca il nucleo — chi, cosa, dove, quando, fonte.
2. Parti da fonti primarie (comunicato, account ufficiale, atto), come nella skill scoop.
3. Verifica con la checklist scoop (confermato / in verifica / smentito / rumor).
4. Controlla il repo — stesso fatto, slug o titolo già online.

### 5. Scegli il formato

Leggi `references/formati.md`. In sintesi:

- Roundup giornaliero — se hai una lista Trends datata con almeno 5 query pulite e qualcosa da dire oltre l'elenco. Un solo roundup per giorno solare, salvo aggiornamento sostanziale.
- Notizia singola — una query, un fatto verificato. Categoria del sito secondo il fatto, non una categoria inventata «trends».
- Entrambi nello stesso ciclo se entrambi passano il gate. Non pubblicare dieci flash deboli per coprire la classifica.

Vietato:

- spacciare «in ascesa» per «le più cercate in assoluto»
- mettere volumi inventati nel titolo
- fare un articolo su una query se l'unico contenuto è «sta salendo su Google»

### 6. Gate merita il sito

Pubblica in automatico solo se tutti i punti sono veri.

Notizia singola:

- fatto confermato (primaria ufficiale o due fonti indipendenti credibili)
- fresco e non già coperto nello stesso modo dal repo
- impatto reale o domanda di ricerca chiara
- materia sufficiente per il formato del repo, senza riempitivo
- niente vittime/minori esposti, niente indagini date per certe senza comunicato, niente rumor di mercato/casting

Roundup:

- lista Trends (o reprint secondario etichettato) con data/ora e geo IT
- almeno 5 query pulite
- ogni tema del digest basato su un fatto verificato (niente meta sulle query in pagina)
- nessun volume assoluto finto
- non esiste già un roundup dello stesso giorno con lista quasi identica

Se il gate fallisce: `NON PUBBLICARE — motivo` e stop su quel pezzo. Non creare file.

### 7. Scrittura da quotidiano (obbligatoria)

Prima di una riga di titolo o corpo, leggi `references/scrittura-curiomondo.md` **e** i file del repo che elenca. Senza quella lettura, non scrivere.

Regole non negoziabili, anche se l'utente chiede velocità:

- testo da quotidiano italiano — sobrio, fattuale, piramide invertita — non da blog di trend
- protocollo 4.0 qualità + protocollo redazione corpo applicati per intero
- almeno due elementi di valore aggiunto CurioMondo; altrimenti `NON PUBBLICARE — solo riscrittura`
- flash 100–250 o standard 300–600 secondo la materia verificata; vietato allungare
- niente prima persona, niente appunti interni, niente elenco fonti nel corpo
- **Regola scrittura 5 ottobre 2026 (fail-closed):** Trends e le query restano **solo radar interno**. Nel testo pubblico (titolo, sommario, lead, corpo, insight, meta) **vietato** scrivere query, Google Trends, ricerche in ascesa, soglie o volumi: **solo i fatti** della notizia, tono da quotidiano. Il «roundup» è un digest di notizie del giorno, non un elenco di query. Nelle Fonti consultate: **nomi reali** delle testate, mai «Fonte consultata». Dettaglio: `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md` e `references/formati.md`
- clona HTML, classi, disclosure e blocco fonti da un articolo già online della stessa categoria

La velocità del ciclo Trends non prevale sulla qualità. Un pezzo «da classifica» scritto male non si pubblica.

Checklist SÌ/NO del protocollo qualità in chat dopo il commit (o al posto del commit se fallisce). Non inserirla nella pagina.

### 8. Pubblicazione

Prima di toccare file, leggi nel repo, in quest'ordine:

1. `AGENTS.md`
2. i file che `AGENTS.md` elenca come obbligatori
3. un articolo recente della stessa categoria, come stampo

Poi segui il flusso GitHub della skill scoop (`ultime-notizie-scoop/references/pubblicazione-github.md`).

Immagine hero, listing, feed, sitemap, predeploy — solo come li definisce il repo. Se manca un pezzo del gate di pubblicazione completa, non dichiarare il go-live.

Commit message:

- roundup — `notizia: trend google IT YYYY-MM-DD`
- singola — `notizia: titolo corto`

## Output in chat (dopo il commit, non al posto del commit)

Italiano, corto:

- lista Trends usata (fonte, ora, geo)
- query scartate e perché
- cosa hai pubblicato (titolo, categoria, path, commit) o `NON PUBBLICARE`
- fonte primaria e ora per ogni notizia singola
- esito della checklist qualità a 12 punti (SÌ/NO, in chat)
- se la pubblicazione è incompleta (hero, sitemap, predeploy), dillo così

Niente lezione su come funziona Trends. Niente classifica annuale se l'ordine era il giornaliero.

## Limiti

- Non inventare query né volumi.
- Non usare una top USA/mondiale al posto di Italia.
- Non sovrascrivere i protocolli del repo e non pubblicare un testo che li viola.
- Non toccare altri repository salvo ordine esplicito.
- Year in Search e ranking mensili restano di `ricerche-google-italia`, salvo pezzo annuale chiesto esplicitamente.

## File di supporto

- `references/radar-query.md` — URL, estrazione, cosa annotare
- `references/selezione-query.md` — punteggio e scarti
- `references/formati.md` — roundup vs notizia singola, tono, divieti di titolo
- `references/scrittura-curiomondo.md` — ordine di lettura dei protocolli, tono da quotidiano, checklist
