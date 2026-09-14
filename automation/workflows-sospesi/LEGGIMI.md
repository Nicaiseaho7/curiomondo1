# Automazioni sospese

Qui dentro stanno i workflow che avevano bisogno di una chiave OpenAI
(`OPENAI_API_KEY`) o della coda privata delle domande
(`CURIOMONDO_DAILY_QUESTIONS_JSON`). Sono stati spostati fuori da
`.github/workflows/` il 14 settembre 2026, quando il sito e tornato alla
pubblicazione manuale: GitHub legge soltanto quella cartella, quindi da qui non
partono e non falliscono piu.

Non e stato cancellato niente. Per riattivarne uno basta rimetterlo al suo posto:

    git mv automation/workflows-sospesi/<nome>.yml .github/workflows/

e ricreare il segreto che gli serve. Il codice della redazione automatica
(`automation/newsroom/`) resta dov'era: senza chiave non chiama nulla.

## Cosa resta attivo

- `bozze/` piu `tools/pubblica_articolo.py`: pubblicazione manuale, nessuna
  chiave richiesta.
- `sito-pubblico.yml`: controlla che le pagine rispondano sul dominio.
- `newsroom-tests.yml` e gli altri controlli: non toccano servizi a pagamento.
