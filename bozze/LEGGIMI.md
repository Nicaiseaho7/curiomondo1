# Come aggiungere un articolo scritto con ChatGPT

Metti qui un file `.json` con l'articolo e una riga `"immagine"` con l'indirizzo
della figura: al salvataggio il sito lo pubblica da solo, dopo averlo passato
per tutti i controlli della redazione. Se un controllo fallisce non viene
pubblicato niente e trovi il motivo nei log della pubblicazione.

Il file da dare a ChatGPT per farsi produrre il JSON giusto e
`automation/prompts/chatgpt-nuovo-articolo.md`.

Dopo la pubblicazione il file di bozza viene rimosso da questa cartella: e un
vassoio in entrata, non un archivio.

## Nota del 16 settembre 2026

Il sito non usa piu chiavi a pagamento: l'immagine non viene piu generata in
automatico, quindi nel JSON serve sempre `immagine.url` con l'indirizzo di una
figura gia pronta (almeno 1000x650). Tutto il resto funziona come prima.

## Nota del 24 settembre 2026

Arrivare come file o indirizzo non rende un'immagine una fotografia vera: e
solo il modo in cui arriva, ora che la generazione automatica e spenta. Il
JSON deve dichiararlo con `immagine.fotografia_reale`: `true` solo per uno
scatto reale di cui hai il diritto di pubblicazione, `false` (o il campo
assente, che vale come `false`) per un'illustrazione, un grafico o qualunque
immagine non documentaria. Il sito scrive sotto l'immagine una didascalia
diversa nei due casi; dichiarare il valore sbagliato la rende falsa.
