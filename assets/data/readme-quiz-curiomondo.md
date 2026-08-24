# CurioMondo / Pianeta Quiz

Il file `quiz-curiomondo.json` contiene il database statico dei quiz caricato dalla homepage tramite `fetch()`.

## Schema di ogni domanda

```json
{
  "id": "cmq-001",
  "category": "Cultura Generale",
  "difficulty": "medio",
  "type": "multiple",
  "question": "Testo della domanda",
  "options": ["A", "B", "C", "D"],
  "correctIndex": 2,
  "explanation": "Spiegazione della risposta corretta.",
  "curiosity": "Curiosità aggiuntiva.",
  "image": null
}
```

- `id` deve essere univoco e non deve cambiare dopo la pubblicazione.
- `correctIndex` parte da 0.
- `options` può contenere 2 elementi per Vero/Falso oppure 4 per scelta multipla.
- `image` può essere `null` oppure un percorso relativo, ad esempio `assets/images/quiz/esempio.jpg`.

Gli ID già visualizzati, le stelle e il numero di partite sono conservati nel `localStorage` del browser. Quando tutte le domande sono state viste, il ciclo degli ID viene azzerato automaticamente e parte una nuova orbita casuale.
