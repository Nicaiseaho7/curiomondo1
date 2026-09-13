#!/usr/bin/env bash
# Un ciclo completo della redazione automatica, dal controllo delle fonti alla
# pubblicazione verificata.
#
# Vive in uno script e non dentro il workflow perche viene eseguito da due
# innesti diversi — il ciclo singolo e la staffetta notturna — e due copie della
# stessa procedura prima o poi divergono. Qui la procedura e una sola.
#
# Variabili attese:
#   REPO_URL   indirizzo con credenziali per i push
#   CADENZA    "fast" (fonti prioritarie) oppure "deep" (scansione ampia)
#   MASSIMO    quante bozze al massimo per ciclo
#
# Non pubblica mai senza il gate: se un controllo critico fallisce, il lotto
# viene ritirato e il sito resta come prima.
set -uo pipefail

CADENZA="${CADENZA:-fast}"
MASSIMO="${MASSIMO:-2}"
STATO="${STATO:-.state}"

annota() { printf '%s · %s\n' "$(date -u +%H:%M:%S)" "$1"; }

salva_stato() {
  # Lo stato vive su un ramo separato: scriverlo su main significherebbe un
  # deploy Netlify a ogni ciclo, anche quando non si pubblica niente.
  ( cd "$STATO" || exit 0
    git add -A
    git diff --cached --quiet && exit 0
    git commit --quiet -m "redazione $CADENZA: $(date -u +%Y-%m-%dT%H:%MZ)"
    for tentativo in 1 2 3; do
      git push --quiet "$REPO_URL" automation-state && exit 0
      git pull --quiet --rebase "$REPO_URL" automation-state || true
      sleep $((tentativo * 3))
    done
    echo "stato non salvato dopo tre tentativi" ) || true
}

# Il sito potrebbe essere cambiato sotto di noi: un altro ciclo, o una mano
# umana. Meglio ripartire dall'ultimo stato pubblicato.
git pull --rebase --quiet "$REPO_URL" main || annota "riallineamento a main non riuscito, proseguo"

annota "controllo delle fonti ($CADENZA)"
python3 -m automation.newsroom.watcher \
  --state "$STATO" --cadence "$CADENZA" --articles notizie > /tmp/riepilogo.json || {
    annota "watcher in errore: salto il ciclo"; exit 1; }
python3 -c "import json;d=json.load(open('/tmp/riepilogo.json'));print('  nuovi candidati:',d['nuovi_candidati'])"

annota "verifica dei deploy precedenti sul dominio pubblico"
python3 -m automation.newsroom.verify --state "$STATO" || annota "verifica non riuscita, proseguo"

annota "verifica editoriale e stesura"
python3 -m automation.newsroom.worker \
  --state "$STATO" --max "$MASSIMO" --articles notizie > /tmp/editor.json || annota "worker in errore"
python3 -c "import json;d=json.load(open('/tmp/editor.json'));print('  bozze:',d.get('bozze',0),'| speso oggi:',d.get('speso_oggi_usd',0),'USD')" 2>/dev/null || true

annota "immagini e sincronizzazione del sito"
if ! CURIOMONDO_AUTO_PUBLISH=true python3 -m automation.newsroom.publisher \
      --state "$STATO" --max "$MASSIMO" > /tmp/publish.json; then
  annota "renderer in errore: ritiro il lotto"
  python3 -m automation.newsroom.publisher --state "$STATO" --rollback || true
  salva_stato; exit 1
fi
cat /tmp/publish.json
ARTICOLI=$(python3 -c "import json;print(json.load(open('/tmp/publish.json')).get('articoli',0))")

if [ "$ARTICOLI" = "0" ]; then
  annota "nessun articolo pronto: nessun deploy"
  salva_stato
  exit 0
fi

annota "gate completo prima del deploy"
if ! python3 tools/predeploy.py; then
  annota "GATE FALLITO: non pubblico e ritiro il lotto"
  python3 -m automation.newsroom.publisher --state "$STATO" --rollback || true
  salva_stato
  exit 1
fi

annota "pubblico il lotto ($ARTICOLI articoli)"
git add notizie assets/data assets/images/editorial-auto categorie index.html \
        feed.xml sitemap.xml news-sitemap.xml curiomondo-site-manifest.json
if git diff --cached --quiet; then
  annota "il renderer dichiarava articoli pronti ma il sito non e cambiato"
  python3 -m automation.newsroom.publisher --state "$STATO" --rollback || true
  salva_stato
  exit 1
fi
git commit --quiet -m "Redazione automatica: pubblica lotto $(date -u +%Y-%m-%dT%H:%MZ)"

PUBBLICATO=""
for tentativo in 1 2 3; do
  if git push --quiet "$REPO_URL" HEAD:main; then
    PUBBLICATO=$(git rev-parse HEAD); break
  fi
  annota "push non riuscito (tentativo $tentativo): riallineo e rivalido"
  git pull --rebase --quiet "$REPO_URL" main || true
  python3 tools/predeploy.py >/dev/null || { annota "gate rosso dopo il riallineo"; break; }
done

if [ -n "$PUBBLICATO" ]; then
  annota "pubblicato in $PUBBLICATO"
  python3 -m automation.newsroom.publisher --state "$STATO" --confirm --commit "$PUBBLICATO" || true
else
  annota "pubblicazione non riuscita: ritiro il lotto"
  git reset --hard --quiet "$(git rev-parse HEAD~1)" || true
  python3 -m automation.newsroom.publisher --state "$STATO" --rollback || true
  salva_stato
  exit 1
fi

salva_stato
annota "ciclo concluso"
