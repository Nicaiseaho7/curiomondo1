# Redazione automatica CurioMondo

Sistema di monitoraggio, verifica e pubblicazione delle notizie. Sostituisce
progressivamente la pubblicazione manuale (un workflow YAML scritto a mano per
ogni articolo) con una pipeline autonoma.

## Principio di fondo

**Monitorare costa poco, scrivere costa molto.** Le due cose sono separate:

```
watcher (ogni ~5 min, gratuito)
   └─ nessun candidato nuovo → si ferma qui, zero costi
   └─ candidato nuovo → worker editoriale (a pagamento, raro)
```

E soprattutto: **tanti controlli ≠ tanti deploy**. Lo stato del watcher vive sul
branch `automation-state`, che Netlify non pubblica. Un controllo ogni cinque
minuti non consuma neanche un build.

## Stato di avanzamento

| Fase | Contenuto | Stato |
|---|---|---|
| 1 | Watcher, fonti, deduplicazione, filtri, stato persistente | ✅ completata |
| 2 | Verifica editoriale e stesura articolo (OpenAI) | da fare |
| 3 | Immagine editoriale fotorealistica (OpenAI) | da fare |
| 4 | Coda di pubblicazione e deploy a lotti | da fare |
| 5 | Verifica post-deploy sul sito pubblico e recupero automatico | da fare |

## Componenti della Fase 1

| File | Ruolo |
|---|---|
| `sources.json` | Registro delle fonti: istituzionali, agenzie, scienza, economia, sport |
| `sources.py` | Lettura RSS/Atom con cache condizionale (`ETag`), timeout e ritentativi |
| `normalize.py` | Ripulisce URL e titoli, produce le impronte per la deduplicazione |
| `filters.py` | Filtri economici: cosa non merita nemmeno una chiamata al modello |
| `state.py` | Stato persistente: ciclo di vita di ogni candidato |
| `watcher.py` | Il ciclo di sorveglianza |
| `health.py` | Verifica quali fonti rispondono davvero |
| `observability.py` | Log strutturati, con oscuramento automatico dei segreti |

### Le due velocità

- **Controllo rapido** (`*/5`): fonti prioritarie e ultima ora.
- **Scansione ampia** (`17,47` di ogni ora): tutto il registro, incluse
  istituzionali, scientifiche ed economiche.

### Come viene evitato un doppione

Tre reti sovrapposte, dalla più economica alla più accurata:

1. **URL identico** — l'indirizzo viene ripulito da parametri di tracciamento,
   `www` e schema, quindi lo stesso link non viene mai valutato due volte.
2. **Impronta del titolo** — raggruppa i casi facili.
3. **Somiglianza fra parole chiave** — riconosce lo stesso fatto raccontato con
   parole diverse ("Terremoto di magnitudo 6.2 colpisce la costa del Giappone"
   e "Giappone, terremoto magnitudo 6.2 sulla costa" sono la stessa notizia).

In più ogni candidato viene confrontato con gli articoli **già online**: se
CurioMondo ha già raccontato quel fatto, si scarta.

## Una nota onesta sulla frequenza

GitHub esegue i cron *al meglio possibile*: sotto carico può ritardarli. Il
minimo consentito è 5 minuti, ma la consegna non è garantita al minuto. In
pratica: spesso 5 minuti, a volte 10-15.

Il repository è **pubblico**, quindi i minuti di GitHub Actions sono gratuiti e
illimitati: la frequenza non ha costi.

Se in futuro servisse una puntualità rigorosa, la via più semplice è un servizio
esterno di cron che invochi `workflow_dispatch` via API. Non serve oggi.

## Credenziali da configurare

Nessuna per la Fase 1: il watcher usa solo feed pubblici.

Dalla Fase 2 servirà **`OPENAI_API_KEY`**, da inserire in
**GitHub → Settings → Secrets and variables → Actions → New repository secret**.
La chiave viene letta esclusivamente dall'ambiente, non compare mai nel
repository né nei log (`observability.py` la oscura anche se finisse per errore
dentro un messaggio), e un controllo in CI blocca qualunque credenziale committata.

## Verifica

```bash
python3 -m pytest automation/newsroom/tests -q      # logica, senza rete
python3 -m automation.newsroom.health               # quali fonti rispondono
python3 -m automation.newsroom.watcher --state .state --cadence fast
```

Il watcher è progettato per non fallire mai in modo rumoroso: se tutte le fonti
sono irraggiungibili registra l'errore per ciascuna, non produce candidati e
termina con successo. Una fonte rotta non deve tingere di rosso la CI né
fermare le altre.
