(() => {
  'use strict';
  const DATA_URL = '/assets/data/concerti.json';
  const REGIONS = ['Abruzzo','Basilicata','Calabria','Campania','Emilia-Romagna','Friuli-Venezia Giulia','Lazio','Liguria','Lombardia','Marche','Molise','Piemonte','Puglia','Sardegna','Sicilia','Toscana','Trentino-Alto Adige','Umbria','Valle d’Aosta','Veneto'];
  const $ = (selector, root = document) => root.querySelector(selector);
  const esc = value => String(value ?? '').replace(/[&<>'"]/g, char => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[char]));
  const fmtDate = new Intl.DateTimeFormat('it-IT', {weekday:'long', day:'numeric', month:'long', year:'numeric', timeZone:'Europe/Rome'});
  const fmtMonth = new Intl.DateTimeFormat('it-IT', {month:'long', year:'numeric', timeZone:'Europe/Rome'});
  const fmtVerified = new Intl.DateTimeFormat('it-IT', {day:'numeric', month:'long', year:'numeric', hour:'2-digit', minute:'2-digit', timeZone:'Europe/Rome'});
  const fmtTime = new Intl.DateTimeFormat('it-IT', {hour:'2-digit', minute:'2-digit', timeZone:'Europe/Rome'});
  const ARTICLES = {
    'gazzelle-milano-2027-04-03': {url:'/notizie/gazzelle-palasport-2027-nuove-date-milano-roma-biglietti.html', title:'Gazzelle amplia il tour 2027: nuove date a Milano e Roma', description:'Il calendario nei palasport sale a dodici appuntamenti.', image:'/assets/images/editorial-auto/gazzelle-palasport-2027-nuove-date-milano-roma-biglietti-v1372-1200.webp'},
    'gazzelle-torino-2027-04-06': {url:'/notizie/gazzelle-palasport-2027-nuove-date-milano-roma-biglietti.html', title:'Gazzelle amplia il tour 2027: nuove date a Milano e Roma', description:'Il calendario nei palasport sale a dodici appuntamenti.', image:'/assets/images/editorial-auto/gazzelle-palasport-2027-nuove-date-milano-roma-biglietti-v1372-1200.webp'},
    'gazzelle-roma-2027-04-10': {url:'/notizie/gazzelle-palasport-2027-nuove-date-milano-roma-biglietti.html', title:'Gazzelle amplia il tour 2027: nuove date a Milano e Roma', description:'Il calendario nei palasport sale a dodici appuntamenti.', image:'/assets/images/editorial-auto/gazzelle-palasport-2027-nuove-date-milano-roma-biglietti-v1372-1200.webp'},
    'tananai-verona-2027-05-21': {url:'/notizie/tananai-live-tour-2027-date-arena-palazzetti-biglietti.html', title:'Tananai torna dal vivo nel 2027: Arena di Verona e sette palasport in autunno', description:'Il calendario parte il 21 maggio e riprende l’8 ottobre ad Ancona.', image:'/assets/images/editorial-auto/tananai-live-tour-2027-date-arena-palazzetti-biglietti-v1457-1200.webp'},
    'u2-milano-2027-07-05': {url:'/notizie/u2-milano-san-siro-5-6-luglio-2027-biglietti-vendita.html', title:'U2 a San Siro nel 2027: vendita generale il 6 novembre per due date', description:'Il tour mondiale farà tappa a Milano il 5 e 6 luglio.', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'u2-milano-2027-07-06': {url:'/notizie/u2-milano-san-siro-5-6-luglio-2027-biglietti-vendita.html', title:'U2 a San Siro nel 2027: vendita generale il 6 novembre per due date', description:'Il tour mondiale farà tappa a Milano il 5 e 6 luglio.', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'u2-milano-2027-07-09': {url:'/notizie/u2-terza-data-san-siro-9-luglio-2027-biglietti.html', title:'U2, aperta la vendita per la terza data a San Siro', description:'Il nuovo concerto è in programma venerdì 9 luglio 2027 alle 19:30.', image:'/assets/images/editorial-auto/stefano-nazzi-e-francesca-crescentini-a-casa-spotify-per-scrivere-per-la-voce-2026-v20261117c-1200.webp'},
    'stray-kids-milano-2027-07-31': {url:'/notizie/stray-kids-san-siro-31-luglio-2027-prevendite.html', title:'Stray Kids a San Siro nel 2027: registrazione alla prevendita entro il 15 novembre', description:'Il RUN IT World Tour arriva a Milano il 31 luglio.', image:'/assets/images/editorial-auto/mara-sattei-tour-live-2026-cancellato-rimborsi-10-dicembre-v1476-1200.webp'},
    'aiello-napoli-2026-11-16': {url:'/notizie/aiello-dovevi-portarci-me-tour-2026-bologna-roma-napoli-milano.html', title:'Aiello nei club, da Bologna a Milano: tutte le tappe rimaste del tour di novembre', description:'Le tappe rimaste del Dovevi portarci me Tour.', image:'/assets/images/editorial-auto/aiello-dovevi-portarci-me-tour-2026-bologna-roma-napoli-milano-v1384-1200.webp'},
    'aiello-milano-2026-11-19': {url:'/notizie/aiello-dovevi-portarci-me-tour-2026-bologna-roma-napoli-milano.html', title:'Aiello nei club, da Bologna a Milano: tutte le tappe rimaste del tour di novembre', description:'Le tappe rimaste del Dovevi portarci me Tour.', image:'/assets/images/editorial-auto/aiello-dovevi-portarci-me-tour-2026-bologna-roma-napoli-milano-v1384-1200.webp'},
    'michielin-ancona-2026-11-15': {url:'/notizie/francesca-michielin-live-teatri-2026-trento-date-biglietti.html', title:'Francesca Michielin parte da Trento: il calendario completo del tour nei teatri', description:'Il percorso autunnale nei teatri, con orari e città.', image:'/assets/images/editorial-auto/francesca-michielin-live-teatri-2026-trento-date-biglietti-v1384-1200.webp'},
    'michielin-firenze-2026-11-16': {url:'/notizie/francesca-michielin-live-teatri-2026-trento-date-biglietti.html', title:'Francesca Michielin parte da Trento: il calendario completo del tour nei teatri', description:'Il percorso autunnale nei teatri, con orari e città.', image:'/assets/images/editorial-auto/francesca-michielin-live-teatri-2026-trento-date-biglietti-v1384-1200.webp'},
    'michielin-bari-2026-11-20': {url:'/notizie/francesca-michielin-live-teatri-2026-trento-date-biglietti.html', title:'Francesca Michielin parte da Trento: il calendario completo del tour nei teatri', description:'Il percorso autunnale nei teatri, con orari e città.', image:'/assets/images/editorial-auto/francesca-michielin-live-teatri-2026-trento-date-biglietti-v1384-1200.webp'},
    'michielin-bologna-2026-11-22': {url:'/notizie/francesca-michielin-live-teatri-2026-trento-date-biglietti.html', title:'Francesca Michielin parte da Trento: il calendario completo del tour nei teatri', description:'Il percorso autunnale nei teatri, con orari e città.', image:'/assets/images/editorial-auto/francesca-michielin-live-teatri-2026-trento-date-biglietti-v1384-1200.webp'},
    'michielin-trieste-2026-11-23': {url:'/notizie/francesca-michielin-live-teatri-2026-trento-date-biglietti.html', title:'Francesca Michielin parte da Trento: il calendario completo del tour nei teatri', description:'Il percorso autunnale nei teatri, con orari e città.', image:'/assets/images/editorial-auto/francesca-michielin-live-teatri-2026-trento-date-biglietti-v1384-1200.webp'},
    'michielin-padova-2026-11-25': {url:'/notizie/francesca-michielin-live-teatri-2026-trento-date-biglietti.html', title:'Francesca Michielin parte da Trento: il calendario completo del tour nei teatri', description:'Il percorso autunnale nei teatri, con orari e città.', image:'/assets/images/editorial-auto/francesca-michielin-live-teatri-2026-trento-date-biglietti-v1384-1200.webp'},
    'michielin-roma-2026-11-28': {url:'/notizie/francesca-michielin-live-teatri-2026-trento-date-biglietti.html', title:'Francesca Michielin parte da Trento: il calendario completo del tour nei teatri', description:'Il percorso autunnale nei teatri, con orari e città.', image:'/assets/images/editorial-auto/francesca-michielin-live-teatri-2026-trento-date-biglietti-v1384-1200.webp'},
    'michielin-milano-2026-12-01': {url:'/notizie/francesca-michielin-live-teatri-2026-trento-date-biglietti.html', title:'Francesca Michielin parte da Trento: il calendario completo del tour nei teatri', description:'Il percorso autunnale nei teatri, con orari e città.', image:'/assets/images/editorial-auto/francesca-michielin-live-teatri-2026-trento-date-biglietti-v1384-1200.webp'},
    'michielin-napoli-2026-12-03': {url:'/notizie/francesca-michielin-live-teatri-2026-trento-date-biglietti.html', title:'Francesca Michielin parte da Trento: il calendario completo del tour nei teatri', description:'Il percorso autunnale nei teatri, con orari e città.', image:'/assets/images/editorial-auto/francesca-michielin-live-teatri-2026-trento-date-biglietti-v1384-1200.webp'},
    'angele-milano-2027-05-13': {url:'/notizie/angele-milano-fabrique-instinct-tour-data-prevendite-biglietti-2027.html', title:'Angèle al Fabrique di Milano: unica data italiana dell’Instinct Tour', description:'La cantautrice belga al Fabrique il 13 maggio 2027.', image:'/assets/images/editorial-auto/nuzzo-di-biase-milano-spettacolo-rinviato-23-novembre-rimborsi-v1476-1200.webp'},
    'yendry-segrate-2027-02-06': {url:'/notizie/yendry-circolo-magnolia-segrate-como-agua-tour-biglietti-2027.html', title:'YEИDRY al Circolo Magnolia: data italiana del Como Agua Tour', description:'Sabato 6 febbraio 2027 al Circolo Magnolia di Segrate.', image:'/assets/images/editorial-auto/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026-v1423-1200.webp'},
    'jesse-welles-milano-2027-02-02': {url:'/notizie/jesse-welles-milano-2-febbraio-2027-biglietti.html', title:'Jesse Welles apre il tour europeo a Milano', description:'Il 2 febbraio 2027 ai Magazzini Generali.', image:'/assets/images/editorial-auto/jesse-welles-milano-2-febbraio-2027-biglietti-v1372-1200.webp'},
    'artie-5ive-genova-2027-10-05': {url:'/notizie/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti.html', title:'Artie 5ive nei palasport nel 2027: cinque date per il Vittoria Tour', description:'Cinque date a ottobre, tutte alle 21.', image:'/assets/images/editorial-auto/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti-v1457-1200.webp'},
    'artie-5ive-assago-2027-10-11': {url:'/notizie/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti.html', title:'Artie 5ive nei palasport nel 2027: cinque date per il Vittoria Tour', description:'Cinque date a ottobre, tutte alle 21.', image:'/assets/images/editorial-auto/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti-v1457-1200.webp'},
    'artie-5ive-bologna-2027-10-17': {url:'/notizie/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti.html', title:'Artie 5ive nei palasport nel 2027: cinque date per il Vittoria Tour', description:'Cinque date a ottobre, tutte alle 21.', image:'/assets/images/editorial-auto/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti-v1457-1200.webp'},
    'artie-5ive-roma-2027-10-22': {url:'/notizie/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti.html', title:'Artie 5ive nei palasport nel 2027: cinque date per il Vittoria Tour', description:'Cinque date a ottobre, tutte alle 21.', image:'/assets/images/editorial-auto/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti-v1457-1200.webp'},
    'artie-5ive-napoli-2027-10-26': {url:'/notizie/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti.html', title:'Artie 5ive nei palasport nel 2027: cinque date per il Vittoria Tour', description:'Cinque date a ottobre, tutte alle 21.', image:'/assets/images/editorial-auto/artie-5ive-vittoria-tour-palazzetti-2027-date-biglietti-v1457-1200.webp'},
    'bravi-padova-2027-01-22': {url:'/notizie/michele-bravi-tour-rinviato-dicembre-gennaio-2026-2027.html', title:'Michele Bravi rinvia il tour: le nuove date e i rimborsi', description:'La tappa di Padova è recuperata il 22 gennaio alle 21:15.', image:'/assets/images/editorial-auto/mara-sattei-tour-live-2026-cancellato-rimborsi-10-dicembre-v1476-1200.webp'},
    'subsonica-genova-2027-03-08': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-roma-2027-03-11': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-piacenza-2027-03-13': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-bologna-2027-03-16': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-varese-2027-03-19': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-napoli-2027-03-22': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-avellino-2027-03-23': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-bergamo-2027-03-25': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-venezia-2027-03-26': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-trieste-2027-03-27': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-milano-2027-03-30': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'subsonica-torino-2027-03-31': {url:'/notizie/subsonica-teatri-2027-date-biglietti-prevendite.html', title:'Subsonica a teatro nel 2027: dodici date e vendita generale dal 13 novembre', description:'', image:'/assets/images/editorial-auto/subsonica-teatri-2027-date-biglietti-prevendite-v1457-1200.webp'},
    'memoria-roma-2026-11-15': {url:'/notizie/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026.html', title:'Memoria di ragazza debutta al Teatro Valle: undici repliche fino al 22 novembre', description:'', image:'/assets/images/editorial-auto/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026-v1423-1200.webp'},
    'memoria-roma-2026-11-17': {url:'/notizie/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026.html', title:'Memoria di ragazza debutta al Teatro Valle: undici repliche fino al 22 novembre', description:'', image:'/assets/images/editorial-auto/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026-v1423-1200.webp'},
    'memoria-roma-2026-11-18': {url:'/notizie/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026.html', title:'Memoria di ragazza debutta al Teatro Valle: undici repliche fino al 22 novembre', description:'', image:'/assets/images/editorial-auto/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026-v1423-1200.webp'},
    'memoria-roma-2026-11-19': {url:'/notizie/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026.html', title:'Memoria di ragazza debutta al Teatro Valle: undici repliche fino al 22 novembre', description:'', image:'/assets/images/editorial-auto/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026-v1423-1200.webp'},
    'memoria-roma-2026-11-20': {url:'/notizie/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026.html', title:'Memoria di ragazza debutta al Teatro Valle: undici repliche fino al 22 novembre', description:'', image:'/assets/images/editorial-auto/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026-v1423-1200.webp'},
    'memoria-roma-2026-11-21': {url:'/notizie/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026.html', title:'Memoria di ragazza debutta al Teatro Valle: undici repliche fino al 22 novembre', description:'', image:'/assets/images/editorial-auto/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026-v1423-1200.webp'},
    'memoria-roma-2026-11-22': {url:'/notizie/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026.html', title:'Memoria di ragazza debutta al Teatro Valle: undici repliche fino al 22 novembre', description:'', image:'/assets/images/editorial-auto/roma-memoria-di-ragazza-teatro-valle-10-22-novembre-2026-v1423-1200.webp'},
    'orientamenti-genova-2026-11-17': {url:'/notizie/festival-orientamenti-genova-17-20-novembre-2026-programma.html', title:'Festival Orientamenti a Genova, 200 appuntamenti dal 17 al 20 novembre', description:'', image:'/assets/images/editorial-auto/festival-orientamenti-genova-17-20-novembre-2026-programma-v1423-1200.webp'},
    'nuzzo-dibiase-milano-2026-11-23': {url:'/notizie/nuzzo-di-biase-milano-spettacolo-rinviato-23-novembre-rimborsi.html', title:'Nuzzo e Di Biase rinviano lo spettacolo di Milano al 23 novembre: biglietti validi', description:'', image:'/assets/images/editorial-auto/nuzzo-di-biase-milano-spettacolo-rinviato-23-novembre-rimborsi-v1476-1200.webp'},
    'wonderland-brescia-2026-11-16': {url:'/notizie/brescia-wonderland-festival-programma-biglietti-novembre-2026.html', title:'Wonderland Festival a Brescia: spettacoli, proiezioni e musica fino al 29 novembre', description:'', image:'/assets/images/editorial-auto/brescia-wonderland-festival-programma-biglietti-novembre-2026-v1400-1200.webp'},
    'its-alessano-2026-11-23': {url:'/notizie/puglia-vision-its-orientamento-alessano-23-novembre-2026.html', title:'ITS Puglia Vision, il 23 novembre orientamento gratuito ad Alessano', description:'', image:'/assets/images/editorial-auto/puglia-vision-its-orientamento-alessano-23-novembre-2026-v1447-1200.webp'},
    'tff-torino-2026-11-24': {url:'/notizie/torino-film-festival-2026-programma-biglietti-carnet-abbonamenti.html', title:'Torino Film Festival 2026, programma presentato: biglietti online e riduzioni dal 17 novembre', description:'', image:'/assets/images/editorial-auto/torino-film-festival-2026-programma-biglietti-carnet-abbonamenti-v1383-1200.webp'},
    'guindani-genova-2026-11-15': {url:'/notizie/genova-mostra-libro-stefano-guindani-palazzo-ducale-2026.html', title:'Genova negli scatti di Stefano Guindani, mostra a Palazzo Ducale fino all’8 dicembre', description:'', image:'/assets/images/editorial-auto/genova-mostra-libro-stefano-guindani-palazzo-ducale-2026-v1423-1200.webp'},
    'sguardi-sassuolo-2026-11-15': {url:'/notizie/sguardi-sul-paesaggio-palazzo-ducale-sassuolo-7-22-novembre-2026.html', title:'Sguardi sul paesaggio arriva a Sassuolo: 60 fotografie e ingresso gratuito fino al 22 novembre', description:'', image:'/assets/images/editorial-auto/sguardi-sul-paesaggio-palazzo-ducale-sassuolo-7-22-novembre-2026-v1384-1200.webp'},
  };
  function story(event) {
    const raw = event.article || ARTICLES[event.id] || null;
    if (!raw) return null;
    if (typeof raw === 'string') return {url: raw, title: event.artist || 'Notizia', description: event.tour || '', image: ''};
    return raw.url ? raw : null;
  }
  let data = null;
  let saved = loadSaved();

  function loadSaved() { try { return new Set(JSON.parse(localStorage.getItem('cm-saved-concerts') || '[]')); } catch (_) { return new Set(); } }
  function persistSaved() { try { localStorage.setItem('cm-saved-concerts', JSON.stringify([...saved])); } catch (_) {} }
  function now() { return new Date(); }
  function endOfDay(date) { const copy = new Date(date); copy.setHours(23,59,59,999); return copy; }
  function normalized(text) { return String(text || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase(); }
  function activeEvents() { const moment = now(); return data.events.filter(event => new Date(event.end || event.start) >= moment); }
  function archivedEvents() { const moment = now(); return data.events.filter(event => new Date(event.end || event.start) < moment); }
  function ticketLabel(status) { return ({available:'Biglietti disponibili',upcoming:'Vendita prossima','sold-out':'Sold out',free:'Ingresso gratuito',unknown:'Da verificare'})[status] || 'Da verificare'; }
  function eventState(event, archived) { if (archived) return 'Concluso'; return ({annullato:'Annullato',rinviato:'Rinviato',prevendita:'Prevendita',annunciato:'Annunciato','in-vendita':ticketLabel(event.ticketStatus)})[event.status] || ticketLabel(event.ticketStatus); }
  function dateParts(value) { const date = new Date(value); return {day:new Intl.DateTimeFormat('it-IT',{day:'2-digit',timeZone:'Europe/Rome'}).format(date), month:new Intl.DateTimeFormat('it-IT',{month:'short',timeZone:'Europe/Rome'}).format(date).replace('.','')}; }

  function eventCard(event, archived = false, copy = false) {
    const date = new Date(event.start); const parts = dateParts(event.start); const isSaved = saved.has(event.id);
    const storyLink = story(event);
    const travel = event.transport || event.comeArrivare;
    const linkRel = event.ticketStatus === 'free' ? 'noopener noreferrer' : 'noopener noreferrer sponsored';
    const linkLabel = event.ticketStatus === 'free' ? 'Scheda ufficiale' : 'Biglietti ufficiali ↗';
    const tickets = !archived && event.ticketUrl ? `<a class="ticket-link" href="${esc(event.ticketUrl)}" target="_blank" rel="${linkRel}">${linkLabel}</a>` : '';
    const showTime = event.showTime !== false;
    const until = event.end ? `Fino al ${fmtDate.format(new Date(event.end))}` : '';
    return `<article class="event-card"${copy ? '' : ` id="${esc(event.id)}"`} data-event-id="${esc(event.id)}">
      <time class="date-box" datetime="${esc(event.start)}"><strong>${parts.day}</strong><span>${esc(parts.month)}</span></time>
      <div class="event-main"><h3>${esc(event.artist)}</h3><p>${esc(event.tour || 'Evento')}</p><p>${esc(fmtDate.format(date))}${showTime ? ` · ore ${esc(fmtTime.format(date))}` : ''}${event.doors ? ` · porte ${esc(event.doors)}` : ''}${until ? ` · ${esc(until)}` : ''}</p></div>
      <div class="event-location"><strong>${esc(event.city)}</strong><p>${esc(event.venue)} · ${esc(event.region)}</p>${travel ? `<p class="event-travel">Come arrivare: ${esc(travel)}</p>` : ''}</div>
      <div class="event-actions"><span class="status ${esc(event.ticketStatus)}">${esc(eventState(event, archived))}</span>${tickets}${storyLink && storyLink.url ? `<a class="news-link" href="${esc(storyLink.url)}">Leggi la notizia</a>` : ''}<div class="card-tools">${archived ? '' : `<button class="icon-button save-button" type="button" data-save="${esc(event.id)}" aria-pressed="${isSaved}" aria-label="${isSaved ? 'Rimuovi dai' : 'Salva nei'} preferiti">${isSaved ? '★ Salvato' : '☆ Salva'}</button>`}<button class="icon-button share-button" type="button" data-share="${esc(event.id)}">Condividi</button></div></div>
      ${event.note ? `<p class="event-note">${esc(event.note)}</p>` : ''}
    </article>`;
  }

  function groupMarkup(events, archived = false) {
    if (!events.length) return `<p class="empty-state">${archived ? 'L’archivio non contiene ancora appuntamenti conclusi.' : 'Nessun appuntamento corrisponde ai filtri.'}</p>`;
    if (archived) {
      const groups = new Map();
      events.forEach(event => { const key = new Intl.DateTimeFormat('sv-SE',{year:'numeric',month:'2-digit',timeZone:'Europe/Rome'}).format(new Date(event.start)); if (!groups.has(key)) groups.set(key, []); groups.get(key).push(event); });
      return [...groups].map(([, items]) => {
        const label = fmtMonth.format(new Date(items[0].start));
        const title = label.charAt(0).toUpperCase() + label.slice(1);
        const count = `${items.length} ${items.length === 1 ? 'appuntamento' : 'appuntamenti'}`;
        return `<details class="month-fold"><summary><span>${esc(title)}</span><small>${esc(count)}</small></summary><div class="month-body">${items.map(event => eventCard(event, archived)).join('')}</div></details>`;
      }).join('');
    }
    const groups = new Map();
    events.forEach(event => { if (!groups.has(event.city)) groups.set(event.city, []); groups.get(event.city).push(event); });
    return [...groups.entries()].sort((a, b) => b[1].length - a[1].length || a[0].localeCompare(b[0], 'it')).map(([city, items]) => {
      items.sort((a, b) => new Date(a.start) - new Date(b.start));
      const count = `${items.length} ${items.length === 1 ? 'appuntamento' : 'appuntamenti'}`;
      return `<details class="month-fold"><summary><span>${esc(city)}</span><small>${esc(count)}</small></summary><div class="month-body">${items.map(event => eventCard(event, archived)).join('')}</div></details>`;
    }).join('');
  }

  function selectedEvents() {
    const events = activeEvents(); const q = normalized($('#searchFilter')?.value); const period = $('#periodFilter')?.value || 'all'; const city = $('#cityFilter')?.value || 'all'; const genre = $('#genreFilter')?.value || 'all'; const ticket = $('#ticketFilter')?.value || 'all'; const onlySaved = $('#savedOnly')?.checked;
    const start = now(); let finish = null;
    if (period === '7days') finish = endOfDay(new Date(start.getFullYear(), start.getMonth(), start.getDate() + 7));
    if (period === '30days') finish = endOfDay(new Date(start.getFullYear(), start.getMonth(), start.getDate() + 30));
    if (period === 'month') finish = endOfDay(new Date(start.getFullYear(), start.getMonth() + 1, 0));
    const from = $('#dateFrom')?.value ? new Date(`${$('#dateFrom').value}T00:00:00`) : null; const to = $('#dateTo')?.value ? endOfDay(new Date(`${$('#dateTo').value}T00:00:00`)) : null;
    return events.filter(event => { const date = new Date(event.start); const haystack = normalized([event.artist,event.tour,event.city,event.region,event.venue,event.genre].join(' ')); return (!q || haystack.includes(q)) && (city === 'all' || event.city === city) && (genre === 'all' || event.genre === genre) && (ticket === 'all' || event.ticketStatus === ticket) && (!onlySaved || saved.has(event.id)) && (!finish || date <= finish) && (period !== 'custom' || ((!from || date >= from) && (!to || date <= to))); }).sort((a,b) => new Date(a.start) - new Date(b.start));
  }

  function renderFeatured() {
    const root = $('#featuredEvents'); if (!root) return;
    const events = activeEvents().sort((a,b) => new Date(a.start) - new Date(b.start)).slice(0,3);
    root.innerHTML = events.map(event => {
      const date = new Date(event.start);
      return `<article class="featured-card"><time datetime="${esc(event.start)}">${esc(fmtDate.format(date))}</time><h3>${esc(event.artist)}</h3><p>${esc(event.tour || 'Concerto')}</p><p class="featured-place">${esc(event.city)} · ${esc(event.venue)}</p><a href="#${esc(event.id)}">Vedi la data</a></article>`;
    }).join('');
  }
  function renderRegions() {
    const root = $('#regionDirectory'); if (!root) return;
    const query = normalized($('#regionSearch')?.value);
    const chosen = root.dataset.region || '';
    const source = activeEvents();
    root.innerHTML = REGIONS.filter(region => !query || normalized(region).includes(query)).map(region => {
      const count = source.filter(event => event.region === region).length;
      return `<button class="region-button${region === chosen ? ' is-active' : ''}" type="button" data-region="${esc(region)}" ${count ? '' : 'disabled'}><span>${esc(region)}</span><span>${count}</span></button>`;
    }).join('') || '<p class="empty-state">Nessuna regione con questo nome.</p>';
    const panel = $('#regionEvents');
    if (!panel) return;
    if (!chosen) { panel.innerHTML = ''; return; }
    const events = source.filter(event => event.region === chosen).sort((a,b) => new Date(a.start) - new Date(b.start));
    panel.innerHTML = events.length ? events.map(event => eventCard(event, false, true)).join('') : '<p class="empty-state">Nessun concerto in questa regione.</p>';
  }
  function renderNews() {
    const section = $('#concertNewsSection'); const root = $('#concertNews'); if (!section || !root) return;
    const articles = [...new Map(data.events.map(event => story(event)).filter(Boolean).map(article => [article.url, article])).values()];
    if (!articles.length) { section.hidden = true; return; }
    root.innerHTML = articles.map(article => `<article>${article.image ? `<img src="${esc(article.image)}" alt="" loading="lazy">` : ''}<div><h3>${esc(article.title)}</h3><p>${esc(article.description || '')}</p><a href="${esc(article.url)}">Leggi la notizia completa</a></div></article>`).join(''); section.hidden = false;
  }
  function renderCalendar() {
    const root = $('#concertGroups'); if (!root) return; const events = selectedEvents(); root.innerHTML = groupMarkup(events);
    $('#resultCount').textContent = `${events.length} ${events.length === 1 ? 'appuntamento' : 'appuntamenti'}`;
  }
  function fillOptions() {
    const citySelect = $('#cityFilter'); const genreSelect = $('#genreFilter'); if (!citySelect || !genreSelect) return;
    [...new Set(data.events.map(event => event.city))].sort((a,b)=>a.localeCompare(b,'it')).forEach(city => citySelect.insertAdjacentHTML('beforeend', `<option value="${esc(city)}">${esc(city)}</option>`));
    [...new Set(data.events.map(event => event.genre))].sort((a,b)=>a.localeCompare(b,'it')).forEach(genre => genreSelect.insertAdjacentHTML('beforeend', `<option value="${esc(genre)}">${esc(genre)}</option>`));
  }
  function bindEvents() {
    const form = $('#concertFilters'); if (!form) return;
    form.addEventListener('input', event => { if (event.target.id === 'periodFilter') $('#customDates').hidden = event.target.value !== 'custom'; renderCalendar(); });
    form.addEventListener('reset', () => setTimeout(() => { $('#customDates').hidden = true; renderCalendar(); },0));
    $('#regionSearch')?.addEventListener('input', renderRegions);
    document.addEventListener('click', async event => {
      const saveButton = event.target.closest('[data-save]'); if (saveButton) { event.preventDefault(); event.stopPropagation(); const id = saveButton.dataset.save; saved.has(id) ? saved.delete(id) : saved.add(id); persistSaved(); const pressed = saved.has(id); document.querySelectorAll(`[data-save="${CSS.escape(id)}"]`).forEach(button => { button.setAttribute('aria-pressed', String(pressed)); button.textContent = pressed ? '★ Salvato' : '☆ Salva'; button.setAttribute('aria-label', pressed ? 'Rimuovi dai preferiti' : 'Salva nei preferiti'); }); if ($('#savedOnly')?.checked) renderCalendar(); return; }
      const shareButton = event.target.closest('[data-share]'); if (shareButton) { const url = `${location.origin}${location.pathname}#${shareButton.dataset.share}`; try { if (navigator.share) await navigator.share({title:'Concerto su CurioMondo',url}); else { await navigator.clipboard.writeText(url); shareButton.textContent='Link copiato'; } } catch (_) {} return; }
      const regionButton = event.target.closest('[data-region]'); if (regionButton && !regionButton.disabled) { const root = $('#regionDirectory'); root.dataset.region = root.dataset.region === regionButton.dataset.region ? '' : regionButton.dataset.region; renderRegions(); }
      const dateLink = event.target.closest('.featured-card a'); if (dateLink) { const id = (dateLink.getAttribute('href') || '').slice(1); setTimeout(() => openFold(document.getElementById(id)), 40); }
    });
  }
  function eventDescription(event) {
    const place = [event.venue, event.city].filter(Boolean).join(', ');
    const story = event.article && event.article.description;
    if (story) return place ? `${story} Luogo: ${place}.` : story;
    return [event.artist, event.tour || 'Evento', place].filter(Boolean).join(', ');
  }
  function eventOffer(event) {
    if (event.ticketStatus !== 'free' || !event.ticketUrl) return undefined;
    const validFrom = String(event.lastVerified || event.start || '').slice(0, 10);
    return {'@type':'Offer', url:event.ticketUrl, price:'0', priceCurrency:'EUR', validFrom, availability:'https://schema.org/InStock'};
  }
  function addEventSchema(events) {
    const graph = events.slice(0, 20).map(event => {
      const page = `https://curiomondo.it/concerti/#${event.id}`;
      const item = {
        '@type': event.kind === 'evento' ? 'Event' : 'MusicEvent',
        '@id': page,
        name: `${event.artist} – ${event.city}`,
        description: eventDescription(event),
        startDate: event.start,
        eventStatus: 'https://schema.org/EventScheduled',
        eventAttendanceMode: 'https://schema.org/OfflineEventAttendanceMode',
        url: page,
        location: {'@type':'Place', name:event.venue, address:{'@type':'PostalAddress', addressLocality:event.city, addressRegion:event.region, addressCountry:'IT'}},
        organizer: {'@type':'Organization', name:event.artist, url:event.sourceUrl || page},
        performer: {'@type': event.kind === 'evento' ? 'Organization' : 'MusicGroup', name:event.artist}
      };
      if (event.end) item.endDate = event.end;
      const offer = eventOffer(event);
      if (offer) item.offers = offer;
      return item;
    });
    const script = document.createElement('script');
    script.type = 'application/ld+json';
    script.textContent = JSON.stringify({'@context':'https://schema.org', '@graph':graph});
    document.head.appendChild(script);
  }
  function openFold(target) { let node = target; while (node) { if (node.tagName === 'DETAILS') node.open = true; node = node.parentElement; } }
  function handleHash() { if (!location.hash) return; const target = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (target) { openFold(target); setTimeout(() => target.scrollIntoView({behavior:'smooth',block:'center'}),120); } }
  async function init() {
    try { const response = await fetch(DATA_URL,{cache:'no-cache'}); if (!response.ok) throw new Error(`HTTP ${response.status}`); data = await response.json(); }
    catch (_) { const target = $('#concertGroups') || $('#archiveGroups'); if (target) target.innerHTML='<p class="empty-state">Il calendario non è disponibile in questo momento. Riprova tra poco.</p>'; return; }
    if (window.CONCERT_ARCHIVE) { const events = archivedEvents().sort((a,b)=>new Date(b.start)-new Date(a.start)); $('#archiveGroups').innerHTML = groupMarkup(events,true); return; }
    const active = activeEvents(); $('#heroCount').textContent = `${active.length} date in calendario`; $('#lastVerified').textContent = `Verificato ${fmtVerified.format(new Date(data.lastVerified))}`;
    fillOptions(); renderCalendar(); renderNews(); bindEvents(); addEventSchema(active); handleHash();
  }
  document.addEventListener('DOMContentLoaded', init);
})();
