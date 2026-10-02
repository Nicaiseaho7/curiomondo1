# PROTOCOLLO OBBLIGATORIO — CURIOSITÀ E APPROFONDIMENTI CURIOMONDO

**Versione:** 1.1.2  
**Data:** 29 settembre 2026  
**Stato:** obbligatorio, fail-closed  
**Ambito:** ogni nuova **curiosità** e ogni nuovo **approfondimento** (evergreen, guida di comprensione, pagina in `/approfondimenti/`) pubblicati su CurioMondo  
**File operativo:** questo documento  

**Prevalenza:** per curiosità e approfondimenti questo protocollo **prevale** sulle istruzioni generiche di lunghezza breve, sulle guide “scheda”, sulle fasce 800–1.500 delle skill obsolete e su qualsiasi abitudine a produrre testo corto o superficiale.  
Non sostituisce: gate di rischio e fonti (`PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`), immagini (`AI-EDITORIAL-IMAGE-PROTOCOL.md`), marchio e markup del sito (`AGENTS.md`), divieto di fonti nel corpo e regole HTML.

Se questo file manca o non può essere rispettato, **non pubblicare** curiosità o approfondimenti.

---

## 0. PRINCIPIO FONDAMENTALE

Quando devi creare una Curiosità o un Approfondimento per CurioMondo.it, **NON** devi produrre contenuti brevi, superficiali, generici o simili a una semplice scheda informativa.

L’obiettivo è realizzare un **vero contenuto editoriale premium**: interessante da leggere, approfondito, ben documentato, visivamente ordinato e capace di spiegare realmente l’argomento al lettore.

Una curiosità o un approfondimento deve far pensare al lettore:

> «Sono entrato per una domanda semplice, ma ho scoperto molte cose che non sapevo.»

Parti dalla domanda o dal fatto curioso e sviluppa progressivamente: spiegazione, origine, contesto, cause, funzionamento, conseguenze, esempi italiani, dati, particolarità, falsi miti, domande naturali del lettore, aspetti ancora incerti, collegamenti con altri fenomeni.

Ogni sezione deve aggiungere **informazioni reali**. Non allungare ripetendo gli stessi concetti.

**Sintesi:**

- Curiosità ≠ risposta breve.
- Approfondimento ≠ articolo allungato artificialmente.
- Standard di qualità = **quotidiano serio italiano** (chiarezza, fonti, esempi, zero filler).

Preferisci qualità, profondità e verifica alla quantità di pezzi pubblicati.

---

## 1. SELEZIONE TEMI — OLTRE I SOLI TREND IN ASCESA (v1.1)

I **Google Trends Italia 24–48 h** sono un **campanello**, non l’unico criterio.

### 1.1 Pubblica SOLO se almeno 3 su 5 sono veri

1. C’è **volume** (query in ascesa **oppure** volume stabile alto in Italia)  
2. L’intento è **capire / sapere** (non “chi ha vinto”, non streaming, non gossip)  
3. C’è un **meccanismo** da spiegare (come funziona, perché esiste, da dove nasce)  
4. Esiste almeno una **fonte primaria** (legge, Gazzetta, ministero, ISS, ISTAT, banca, ente ufficiale, paper)  
5. La guida sarà **utile tra 6 mesi** (non legata solo al titolo di ieri)

### 1.2 Fonti di tema (ordine di peso)

| Peso | Fonte | Uso |
|------|--------|-----|
| 1 | Volume **stabile** + intento “capire” | Costruire il catalogo permanente |
| 2 | Soldi / tasse / salute / burocrazia / diritti con fonte ufficiale | Fiducia e ritorno SEO |
| 3 | Google Trends Italia 24–48 h (se passa 3/5) | Scoprire temi nuovi |
| 4 | Calendario (feste, scadenze, stagioni) | Pianificazione |
| 5 | Gap sul sito o gap chiaro in italiano | Differenziazione |
| 6 | “People also ask” / ricerche correlate sotto una query | Cluster di domande da coprire |

### 1.3 Priorità tematiche di default

1. Soldi / tasse / bonus / scadenze  
2. Salute / prevenzione / trasmissione  
3. Legge / diritti / burocrazia / feste istituzionali  
4. Scienza / ambiente / fenomeni spiegabili  
5. Storia / cultura / “perché si fa così in Italia”  
6. Curiosità pure solo se c’è meccanismo + fonte

### 1.4 Scarta sempre

- Risultati sportivi, streaming, gossip, meteo del giorno  
- Notizie già coperte senza nuovo angolo evergreen  
- Query senza oggetto durevole (“oggi cosa succede”, “chi è uscito”)  
- Temi senza fonte verificabile  
- Spike senza meccanismo da spiegare


### 1.6 Volume di ciclo (v1.1.1)

| Contesto | Massimo per ciclo |
|----------|-------------------|
| **Trends / curiosità in tendenza** (`approfondimenti-da-trend`) | **10** guide |
| Evergreen sotto notizie del giorno (`approfondimenti-evergreen`) | 3 guide (o quanto già previsto dalla skill, senza superare 10) |
| Homepage rail «Curiosità e approfondimenti» | **10** card in evidenza (sempre le più recenti) |
| Indice `/approfondimenti/` | Tutte le guide pubblicate (nessun tetto di 3) |

Non pubblicare 10 pezzi deboli: il tetto è un massimo, non una quota. Ogni pezzo deve passare i 3/5 criteri e la soglia di lunghezza.

### 1.5 Deduplica

Se esiste già una guida CurioMondo equivalente → **collegare**, non duplicare.  
Stesso argomento con angolo autonomo e sostanziale → nuovo pezzo ammessibile.

---

## 2. DIFFERENZA TRA «CURIOSITÀ» E «APPROFONDIMENTO»

### 2.1 Curiosità

Parte da una domanda o un fenomeno sorprendente (scienza, storia, natura, tecnologia, cultura).  
La risposta arriva **subito** nei primi paragrafi, poi diventa un **viaggio** nell’argomento.  
Non è una scheda di 150 parole.

### 2.2 Approfondimento

Tratta un argomento importante in modo **sistematico e completo**.  
Risponde progressivamente a: che cos’è, come funziona, perché esiste, come si è arrivati qui, dati, conseguenze, aspetti meno noti, controversie, cosa sappiamo / cosa no.  
Permette a chi parte da zero di capire **senza banalizzare**.

---

## 3. LUNGHEZZA OBBLIGATORIA (v1.1 — prevale sulle skill 800–1500)

**Conta solo il corpo** (`.art-body` / testo della guida). Non contare menu, sidebar, footer, titoli di sistema.

| Tipo | Parole obbligatorie | Quando |
|------|---------------------|--------|
| Guida / curiosità standard | **2.000 – 3.500** | Tema chiaro, un meccanismo principale |
| Guida premium | **3.500 – 5.000+** | Fisco, salute, legge, storia istituzionale, temi multi-layer |
| Minimo assoluto | **1.800** | Se non si arriva a 1.800 con **sostanza verificata** → **NON PUBBLICARE** |

- **Non** riempire per raggiungere la fascia.  
- **Non** comprimere un tema da 4.000 parole in 900.  
- Se manca materia → non pubblicare (mai filler).  
- Questa sezione **prevale** sulle fasce 800–1.500 scritte in skill o template obsoleti.

---

## 4. RICERCA PRIMA DELLA SCRITTURA

Ordine di privilegio:

1. fonti primarie  
2. istituzioni / enti pubblici  
3. università e paper  
4. organizzazioni internazionali  
5. documentazione ufficiale  
6. testate autorevoli solo se necessarie  

Ogni numero, data, articolo di legge o affermazione forte deve essere **verificabile**.  
Se le fonti non concordano: **spiega l’incertezza**, non scegli a caso.  
Ipotesi ≠ fatti.

---

## 5. STRUTTURA EDITORIALE OBBLIGATORIA

```
1. H1 chiaro e specifico: anche dichiarativo; domanda solo se descrive il reale intento della guida
2. Lead 120–180 parole — risposta in pillola + perché conta
3. Indice (opzionale se >3.000 parole)
4. Corpo H2/H3:
   - definizione precisa
   - origine / perché esiste
   - come funziona (passo-passo)
   - esempi concreti italiani (numeri, scaglioni, casi, date)
   - cosa cambia per il cittadino / cosa sapere in pratica
   - limiti, eccezioni, miti da sfatare
   - contesto più ampio (se utile)
5. FAQ 4–8 (da People also ask / correlate reali)
6. Box «In sintesi» 5–8 bullet
7. «Fonti consultate» (.art-sources) — mai «Fonte:» nel corpo
```

### Titolo
Interessante ma **preciso**. Segue `PROTOCOLLO-TITOLI-CTR.md` v2.0: la curiosità nasce dal tema e dai fatti, non da una domanda obbligatoria. Anche il titolo dichiarativo è valido. «Che cos'è», «come» e «perché» sono ammessi quando esprimono un reale intento di comprensione, non come schema seriale. Tema vicino all'inizio e 55–70 caratteri sono orientamenti; niente 70/30, informazioni nascoste per il clic o promesse non mantenute. Per i titoli prevale il protocollo dedicato.

### Lead
Entra subito nel tema. Vietato: «Fin dall’alba dei tempi…», «In un mondo sempre più…».

### Corpo
H2/H3 ammessi e utili (vietati solo nelle notizie flash/standard).  
Sezioni sostanziose, non micro-titoletti vuoti.

### Chiusura
Non ripetere il lead. Lascia concetto chiave, conseguenza o domanda ancora aperta.

---

## 6. SCRITTURA

Tono: **quotidiano serio** (professionale, divulgativo, chiaro, coinvolgente).

- NON enciclopedia fredda  
- NON tema scolastico  
- NON post social  
- NON frasi contorte per sembrare esperti  

Spiega il complesso con parole semplici **senza impoverire**.  
Almeno **un esempio numerico o caso concreto italiano** per guida.  
Almeno **una fonte primaria** citata in modo narrativo nel testo.  
Restano i divieti di meta-commenti redazionali, prima persona di redazione e elenchi «Fonte:» nel corpo.

---

## 7. VIETATO IL FILLER

Vietati: ripetizioni, paragrafi generici, intro lunghissime, conclusioni che solo riassumono, elenchi di riempimento, motivazionali, ovvietà, sezioni da 2–3 frasi senza sostanza, clickbait, sensazionalismo, dati non verificati.

Se eliminando un paragrafo non si perde informazione utile, quel paragrafo **non serve**.

---

## 8. ELEMENTI VISIVI (opzionali, solo se utili)

| Elemento | Uso |
|----------|-----|
| In breve | 3–5 punti iniziali |
| Il dato | numero chiave |
| Lo sapevi? | fatto documentato e sorprendente |
| Attenzione | equivoco comune |
| Cosa sappiamo davvero | fatti vs ipotesi |
| Timeline | storia / norme nel tempo |
| Tabelle | confronti |

Clona classi e stampi **già presenti** sul sito. Non inventare CSS.

---

## 9. IMMAGINI

- Hero **3:2**, qualità alta, pertinente, alt descrittivo  
- Varianti webp 480 / 800 / 1200 secondo pipeline repo  
- Illustrazione IA = disclosure, mai falsa prova documentaria  
- Rispettare `AI-EDITORIAL-IMAGE-PROTOCOL.md` e `automation/prompts/image-generation-contract.txt`

---

## 10. SEO SENZA ROVINARE IL TESTO

Keyword e correlate **naturali**. Titolo SEO, meta description, slug chiaro, link interni.  
Qualità editoriale **prima** della densità keyword. Niente keyword stuffing.

Slug consigliati: `che-cose-…`, `perche-…`, `come-funziona-…` (corti, italiani, senza data salvo necessità).

---

## 11. ORIGINALITÀ

Sintesi di **più fonti**, non riscrittura di una sola pagina.  
Valore CurioMondo = organizzazione, spiegazione, esempi IT, falsi miti, FAQ utili.  
Obiettivo: una delle pagine **più utili in italiano** su quell’argomento.

---

## 12. FONTI

Sezione finale **«Fonti consultate»** (`.art-sources`).  
Mai inventare studi, URL, date, istituzioni.  
Mai «Fonte:» nel corpo.

---

## 13. WORKFLOW DI PUBBLICAZIONE (obbligatorio)

1. Seleziona fino a **10 temi** da Trends (o fino a 10 in un ciclo misto Trends + altri criteri §1); se non c’è materia valida, meno — mai filler  
2. Verifica fonti primarie  
3. Scrivi la guida intera (**2.000–5.000+** parole di corpo)  
4. Hero 3:2 + webp  
5. File `approfondimenti/<slug>.html` (stampo vivo del sito)  
6. Stesso commit:  
   - card in cima a `approfondimenti/index.html`  
   - homepage rail «Curiosità e approfondimenti» (max **10** card in evidenza = le 10 più recenti; le altre restano in `/approfondimenti/` e in index)  
   - blocco `.cm-evergreen-reader` sotto ogni notizia padre, se esiste  
   - `search-index` / sitemap / `_redirects` / manifest secondo pipeline  
7. Gate: `python3 tools/repository_integrity_gate.py` e `python3 tools/predeploy.py` → exit 0  
8. Push `main` (`Nicaiseaho7/curiomondo1`)  
9. Verifica live HTTP 200 (pagina + hero). Solo allora → **PUBBLICATO**

Un pezzo solo in chat **non** è pubblicato.

---

## 14. CHECKLIST PRE-PUBBLICAZIONE

- [ ] Almeno 3/5 criteri di selezione  
- [ ] Corpo ≥ 1.800 parole (target 2.000–5.000+) **senza filler**  
- [ ] Risposta alla domanda principale nei primi paragrafi  
- [ ] Almeno un esempio / dato italiano concreto  
- [ ] Almeno una fonte primaria  
- [ ] H2 che rispondono a domande vere  
- [ ] FAQ non ripetono solo il lead  
- [ ] Box In sintesi  
- [ ] Fonti solo in `.art-sources`  
- [ ] Hero 3:2 e gate immagini  
- [ ] Index + homepage rail + (se serve) evergreen-reader  
- [ ] predeploy exit 0 + URL live 200  
- [ ] Non sembra una risposta chatbot allungata

Se sembra una scheda corta o un testo generico → **NON È PRONTA**.

---

## 15. COSA SCARTARE SUBITO

`NON PUBBLICARE` se:

- corpo sotto 1.800 parole di sostanza  
- scheda superficiale senza viaggio nell’argomento  
- manca ricerca primaria quando l’oggetto lo richiede  
- allungamento solo con ripetizioni  
- dati/URL/studi inventati  
- violazione gate immagini o rischio  
- guida equivalente già online (collegare invece)

---

## 16. PROMPT CORTO DA INCOLLARE A OGNI CICLO

```
Esegui il PROTOCOLLO-CURIOSITA-E-APPROFONDIMENTI.md v1.1 (CurioMondo).

1) Seleziona fino a **10 temi** da Trends IT 24-48h (e/o volume stabile + gap sito) che passano almeno 3/5 criteri §1. Massimo 10 per ciclo; meno se manca materia.
2) Per ciascun tema: guida evergreen 2000–5000+ parole di corpo, italiano da quotidiano, H2 meccanismi + esempi IT + fonti primarie + FAQ + box In sintesi. Minimo assoluto 1800; sotto soglia o senza sostanza → non pubblicare.
3) Hero 3:2 protocollo immagini; pubblica in approfondimenti/, aggiorna index, homepage rail (max 10 card), evergreen-reader sotto padri, search-index, sitemap, redirects.
4) Gate predeploy exit 0; commit+push main Nicaiseaho7/curiomondo1; verifica URL live 200.
5) Scarta gossip/sport result/meteo/streaming. Niente filler. Repo protocolli vincono su skill obsolete 800–1500.
```

---

## 17. RIFERIMENTI INCROCIATI

Lettura obbligatoria:

1. `AGENTS.md`  
2. **`PROTOCOLLO-CURIOSITA-E-APPROFONDIMENTI.md`** (questo file — **prevale** per curiosità/approfondimenti)  
3. `PROTOCOLLO-SCRITTURA-PROFESSIONALE.md`  
4. `PROTOCOLLO-QUALITA-EDITORIALE-ADSENSE.md`  
5. `AI-EDITORIAL-IMAGE-PROTOCOL.md`  
6. `automation/prompts/image-generation-contract.txt`  
7. `PROTOCOLLO-REDAZIONE-CORPO.md`  
8. `CURIO-MONDO-PROTOCOLLO-MAESTRO.md`  
9. uno stampo vivo di approfondimento già online  

Skill collegate (devono deferire a questo file):

- `skills/approfondimenti-evergreen/SKILL.md`  
- skill server `approfondimenti-da-trend` / `approfondimenti-evergreen`  
- trigger Trends → guide permanenti (non notizie)

---

**Fine protocollo v1.1.1 — 29 settembre 2026.**  
**Changelog v1.1:** criteri di selezione oltre i soli trend; fasce 2.000–5.000+ parole; minimo 1.800; priorità tematiche; prompt corto; homepage rail max 3 in evidenza; **fino a 10 guide da Trends per ciclo** (v1.1.1); prevalenza sulle skill 800–1.500.

**Changelog v1.1.1 (29 settembre 2026):** massimo guide da Trends / curiosità in tendenza per ciclo portato da 3 a **10**. L’index `/approfondimenti/` e la pubblicazione accettano fino a 10 pezzi.

**Changelog v1.1.2 (29 settembre 2026):** rail homepage «Curiosità e approfondimenti» portata da max 3 a **max 10** card in evidenza (le più recenti).
