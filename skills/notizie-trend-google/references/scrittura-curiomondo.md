# Scrittura — legge del repository

Prima di comporre titolo, sommario o corpo, leggi **nel repo** e applica per intero, in quest'ordine:

1. `AGENTS.md`
2. `PROTOCOLLO-SCOPERTA-NOTIZIE.md`
3. `AI-EDITORIAL-IMAGE-PROTOCOL.md`
4. `automation/prompts/image-generation-contract.txt`
5. `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md` (protocollo 4.0)
6. `PROTOCOLLO-REDAZIONE-CORPO.md`
7. `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`
8. `curiomondo-site-manifest.json`
9. un articolo recente della stessa categoria, come stampo HTML

Se un file manca o una regola non si può rispettare: `NON PUBBLICARE`. Non inventare uno stile «giornalistico» parallelo. Il giornale vero, su questo sito, è già definito da quei file.

Questa pagina è solo un promemoria operativo. Se diverge dal repo, vince il repo.

## Prima di scrivere (interno, non finisce nella pagina)

Cinque righe private:

1. nucleo del fatto in una frase
2. fonte primaria + ora
3. due elementi di valore aggiunto CurioMondo (dato spiegato, limite del dato, confronto, scheda pratica, link evergreen, aggiornamento sostanziale)
4. formato — flash 100–250 / standard 300–600 / approfondimento solo se la materia lo richiede
5. cosa il titolo non dirà e il lettore deve comunque sapere

Senza i punti 2 e 3: non aprire il file.

## Testo pubblico — struttura

- Titolo informativo, senza clickbait, coerente con H1 e URL.
- Sommario: uno o due elementi assenti dal titolo.
- Lead: 5 W e conseguenza immediata. Si regge da solo. Niente «Google Trends» al posto del fatto.
- Corpo: piramide invertita. Un'idea per paragrafo, 2–4 frasi, massimo 60 parole, almeno un'informazione nuova.
- Frasi lineari, soggetto + verbo + complemento, obiettivo 20–25 parole.
- Chiusura: prossimo passaggio, scadenza, precedente o ciò che resta da accertare. Vietate morali, opinioni, riepilogo del lead.

## Tono da quotidiano

Italiano standard, adulto, sobrio, preciso. Verbi diretti al presente o al passato prossimo.

Vietato nel corpo pubblico (`.art-body`):

- prima persona editoriale — abbiamo verificato, non pubblichiamo, riteniamo, restiamo sulle conferme
- appunti interni — chi cerca, da quelle query, niente articolo, al momento della verifica, Europe/Rome, timestamp di lavorazione
- elenchi di testate, `Fonti:`, `Fonte primaria:`, `Conferma:`, `Letture:`
- clickbait, enfasi, aggettivi vuoti, `ovviamente`, `attualmente`, `fondamentalmente` se non aggiungono un fatto
- spiegazioni di parole difficili, sigle o glossari dentro la notizia
- scene, emozioni, cause o citazioni inventate
- volumi di ricerca inventati o «la query più digitata d'Italia»
- **qualsiasi menzione pubblica di query, Google Trends, ricerche in ascesa, soglie (100K+, 5K+), geo IT, trending now** — vietato in titolo, sommario, lead, corpo, insight e meta (regola 5 ottobre 2026)
- il placeholder «Fonte consultata» al posto del nome reale della testata

Le fonti complete stanno solo in `.art-sources`. Nel corpo il nome di una fonte compare solo se indispensabile (citazione, dato esclusivo, atto ufficiale vs ricostruzione).

`tools/predeploy.py` blocca il deploy se trova espressioni vietate o paragrafi duplicati. Scrivi già pulito.

## Valore aggiunto

Ogni pezzo, anche il roundup, deve offrire almeno due elementi originali CurioMondo. Una parafrasi di ANSA o un elenco di query senza fatto non è un articolo. Esito: `NON PUBBLICARE — solo riscrittura`.

## Checklist pre-pubblicazione (in chat, non in pagina)

Compila SÌ/NO. Un solo NO blocca il commit:

1. il lead sta in piedi da solo
2. almeno due elementi di valore aggiunto
3. non è la parafrasi di una sola agenzia
4. niente glossario, niente morale
5. ogni cifra ha una fonte
6. niente fatti inventati o cause speculative
7. titolo, URL e contenuto coincidono
8. firma, fonti, data e disclosure IA presenti se richiesti dal repo
9. il lettore apprende qualcosa che il titolo non contiene
10. il testo non è intercambiabile con un sito-clone
11. lingua, nomi e toponimi corretti
12. il pezzo termina quando terminano i fatti

Domanda finale del protocollo qualità: un lettore arrivato diretto su CurioMondo, senza Google, considererebbe questa pagina completa, affidabile e utile? Se non è un sì chiaro, non pubblicare.


## Regola ferrea Trends → testo pubblico (5 ottobre 2026)

Trends = radar interno. Il pezzo = solo fatti di notizia da quotidiano.

Prima del commit, greppare il file HTML per: `query`, `Trends`, `ascesa`, `soglia`, `100K`, `ricerche in ascesa`, `Fonte consultata`.  
Se compare in senso meta o come placeholder fonti: **NON PUBBLICARE** finché non è corretto.

Vincolo repo: `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md` § «Notizie da Google Trends».
