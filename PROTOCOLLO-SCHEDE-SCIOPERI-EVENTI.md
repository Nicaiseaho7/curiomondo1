# Schede scioperi, concerti ed eventi

Ordine del proprietario, 15 novembre 2026. Non scade. Vale per ogni notizia nuova e per ogni aggiornamento, prima di dichiarare la pubblicazione conclusa.

Una notizia su uno sciopero, un concerto o un evento non è pubblicata finché non è anche nella scheda giusta.

## Dove

- Sciopero, proclamato, revocato o aggiornato: `assets/data/scioperi.json` e la pagina `/scioperi/`.
- Concerto, spettacolo, festival, mostra o altro evento in Italia, a pagamento o gratuito: `assets/data/concerti.json` e la pagina `/concerti/`.

## Cosa fare, nello stesso ciclo della notizia

1. Leggere titolo, sommario e corpo. Se non parla di sciopero, concerto o evento, il protocollo non si applica.
2. Cercare la scheda già presente. Per uno sciopero contano soggetto, giorno e territorio. Per un concerto o un evento contano artista o nome, giorno e città.
3. Se la scheda c’è, non se ne crea una seconda. Si aggiunge il link della notizia.
4. Se la scheda non c’è, si crea subito con i soli fatti verificati nell’articolo e nelle fonti. I campi non noti restano `Non comunicato` o `null`. Non si inventano orari, prezzi, biglietterie o fasce garantite.
5. Il link della notizia sta nel campo `article` della scheda. Per gli scioperi la stessa notizia entra anche nell’elenco `articles`.

## Campi minimi di una scheda nuova

Sciopero: `id`, titolo, date, settore, territorio, stato (`proclamato`, `revocato` o quello detto dalla fonte), fonte, `article` con `url`, `title`, `summary` e immagine della notizia.

Concerto o evento: `id`, artista o nome, data di inizio, città, luogo se noto, stato dei biglietti se noto, `article` con `url`, `title`, `description` e `image`.

## Non si fa

- Non si lascia la notizia solo in homepage e in archivio.
- Non si duplica una scheda già esistente.
- Non si crea una scheda senza una data verificata.
- Non si riscrivono in blocco le schede vecchie solo per questa regola. Si applica a ogni notizia nuova e a ogni notizia che si sta aggiornando.
