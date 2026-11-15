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
  let data = null;
  let saved = loadSaved();

  function loadSaved() { try { return new Set(JSON.parse(localStorage.getItem('cm-saved-concerts') || '[]')); } catch (_) { return new Set(); } }
  function persistSaved() { try { localStorage.setItem('cm-saved-concerts', JSON.stringify([...saved])); } catch (_) {} }
  function now() { return new Date(); }
  function endOfDay(date) { const copy = new Date(date); copy.setHours(23,59,59,999); return copy; }
  function normalized(text) { return String(text || '').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase(); }
  function activeEvents() { const moment = now(); return data.events.filter(event => new Date(event.end || event.start) >= moment); }
  function archivedEvents() { const moment = now(); return data.events.filter(event => new Date(event.end || event.start) < moment); }
  function ticketLabel(status) { return ({available:'Biglietti disponibili',upcoming:'Vendita prossima','sold-out':'Sold out',unknown:'Disponibilità da verificare'})[status] || 'Disponibilità da verificare'; }
  function eventState(event, archived) { if (archived) return 'Concluso'; return ({annullato:'Annullato',rinviato:'Rinviato',prevendita:'Prevendita',annunciato:'Annunciato','in-vendita':ticketLabel(event.ticketStatus)})[event.status] || ticketLabel(event.ticketStatus); }
  function dateParts(value) { const date = new Date(value); return {day:new Intl.DateTimeFormat('it-IT',{day:'2-digit',timeZone:'Europe/Rome'}).format(date), month:new Intl.DateTimeFormat('it-IT',{month:'short',timeZone:'Europe/Rome'}).format(date).replace('.','')}; }

  function eventCard(event, archived = false) {
    const date = new Date(event.start); const parts = dateParts(event.start); const isSaved = saved.has(event.id);
    const tickets = !archived && event.ticketUrl ? `<a class="ticket-link" href="${esc(event.ticketUrl)}" target="_blank" rel="noopener noreferrer sponsored">Biglietti ufficiali ↗</a>` : '';
    return `<article class="event-card" id="${esc(event.id)}" data-event-id="${esc(event.id)}">
      <time class="date-box" datetime="${esc(event.start)}"><strong>${parts.day}</strong><span>${esc(parts.month)}</span></time>
      <div class="event-main"><h3>${esc(event.artist)}</h3><p>${esc(event.tour || 'Concerto')}</p><p>${esc(fmtDate.format(date))} · ore ${esc(fmtTime.format(date))}${event.doors ? ` · porte ${esc(event.doors)}` : ''}</p></div>
      <div class="event-location"><strong>${esc(event.city)} · ${esc(event.region)}</strong><p>${esc(event.venue)}</p><a class="source-link" href="${esc(event.sourceUrl)}" target="_blank" rel="noopener noreferrer">Fonte ufficiale · verificata ${esc(fmtVerified.format(new Date(event.lastVerified)))}</a></div>
      <div class="event-actions"><span class="status ${esc(event.ticketStatus)}">${esc(eventState(event, archived))}</span>${tickets}${event.article ? `<a class="source-link" href="${esc(event.article.url)}">Leggi la notizia</a>` : ''}<div class="card-tools">${archived ? '' : `<button class="icon-button save-button" type="button" data-save="${esc(event.id)}" aria-pressed="${isSaved}" aria-label="${isSaved ? 'Rimuovi dai' : 'Salva nei'} preferiti">${isSaved ? '★ Salvato' : '☆ Salva'}</button>`}<button class="icon-button share-button" type="button" data-share="${esc(event.id)}">Condividi</button></div></div>
      ${event.note ? `<p class="event-note">${esc(event.note)}</p>` : ''}
    </article>`;
  }

  function groupMarkup(events, archived = false) {
    if (!events.length) return `<p class="empty-state">${archived ? 'L’archivio non contiene ancora concerti conclusi.' : 'Nessun concerto corrisponde ai filtri selezionati.'}</p>`;
    const groups = new Map();
    events.forEach(event => { const key = new Intl.DateTimeFormat('sv-SE',{year:'numeric',month:'2-digit',timeZone:'Europe/Rome'}).format(new Date(event.start)); if (!groups.has(key)) groups.set(key, []); groups.get(key).push(event); });
    return [...groups].map(([, items]) => `<section class="month-group"><h3 class="month-title">${esc(fmtMonth.format(new Date(items[0].start)))}</h3>${items.map(event => eventCard(event, archived)).join('')}</section>`).join('');
  }

  function selectedEvents() {
    const events = activeEvents(); const q = normalized($('#searchFilter')?.value); const period = $('#periodFilter')?.value || 'all'; const region = $('#regionFilter')?.value || 'all'; const genre = $('#genreFilter')?.value || 'all'; const ticket = $('#ticketFilter')?.value || 'all'; const onlySaved = $('#savedOnly')?.checked;
    const start = now(); let finish = null;
    if (period === '7days') finish = endOfDay(new Date(start.getFullYear(), start.getMonth(), start.getDate() + 7));
    if (period === '30days') finish = endOfDay(new Date(start.getFullYear(), start.getMonth(), start.getDate() + 30));
    if (period === 'month') finish = endOfDay(new Date(start.getFullYear(), start.getMonth() + 1, 0));
    const from = $('#dateFrom')?.value ? new Date(`${$('#dateFrom').value}T00:00:00`) : null; const to = $('#dateTo')?.value ? endOfDay(new Date(`${$('#dateTo').value}T00:00:00`)) : null;
    return events.filter(event => { const date = new Date(event.start); const haystack = normalized([event.artist,event.tour,event.city,event.region,event.venue,event.genre].join(' ')); return (!q || haystack.includes(q)) && (region === 'all' || event.region === region) && (genre === 'all' || event.genre === genre) && (ticket === 'all' || event.ticketStatus === ticket) && (!onlySaved || saved.has(event.id)) && (!finish || date <= finish) && (period !== 'custom' || ((!from || date >= from) && (!to || date <= to))); }).sort((a,b) => new Date(a.start) - new Date(b.start));
  }

  function renderFeatured() {
    const root = $('#featuredEvents'); if (!root) return; const events = activeEvents().filter(event => event.featured).slice(0,3);
    root.innerHTML = events.map(event => `<article class="featured-card"><span class="featured-date">${esc(fmtDate.format(new Date(event.start)))}</span><h3>${esc(event.artist)}</h3><p>${esc(event.city)} · ${esc(event.venue)}</p><a href="#${esc(event.id)}">Vedi la data</a></article>`).join('');
  }
  function renderRegions() {
    const root = $('#regionDirectory'); if (!root) return; const filtered = selectedEvents();
    root.innerHTML = REGIONS.map(region => { const count = filtered.filter(event => event.region === region).length; return `<button class="region-button" type="button" data-region="${esc(region)}"><span>${esc(region)}</span><span>${count}</span></button>`; }).join('');
  }
  function renderNews() {
    const section = $('#concertNewsSection'); const root = $('#concertNews'); if (!section || !root) return;
    const articles = [...new Map(data.events.filter(event => event.article).map(event => [event.article.url,event.article])).values()];
    if (!articles.length) { section.hidden = true; return; }
    root.innerHTML = articles.map(article => `<article><img src="${esc(article.image)}" alt="" loading="lazy"><div><h3>${esc(article.title)}</h3><p>${esc(article.description || '')}</p><a href="${esc(article.url)}">Leggi la notizia completa</a></div></article>`).join(''); section.hidden = false;
  }
  function renderCalendar() {
    const root = $('#concertGroups'); if (!root) return; const events = selectedEvents(); root.innerHTML = groupMarkup(events);
    $('#resultCount').textContent = `${events.length} ${events.length === 1 ? 'concerto' : 'concerti'}`;
    $('#filterSummary').textContent = events.length ? `Mostrati ${events.length} appuntamenti dal più vicino al più lontano.` : 'Prova ad ampliare i filtri.';
    renderRegions();
  }
  function fillOptions() {
    const regionSelect = $('#regionFilter'); const genreSelect = $('#genreFilter'); if (!regionSelect || !genreSelect) return;
    REGIONS.forEach(region => regionSelect.insertAdjacentHTML('beforeend', `<option value="${esc(region)}">${esc(region)}</option>`));
    [...new Set(data.events.map(event => event.genre))].sort((a,b)=>a.localeCompare(b,'it')).forEach(genre => genreSelect.insertAdjacentHTML('beforeend', `<option value="${esc(genre)}">${esc(genre)}</option>`));
  }
  function bindEvents() {
    const form = $('#concertFilters'); if (!form) return;
    form.addEventListener('input', event => { if (event.target.id === 'periodFilter') $('#customDates').hidden = event.target.value !== 'custom'; renderCalendar(); });
    form.addEventListener('reset', () => setTimeout(() => { $('#customDates').hidden = true; renderCalendar(); },0));
    document.addEventListener('click', async event => {
      const saveButton = event.target.closest('[data-save]'); if (saveButton) { const id = saveButton.dataset.save; saved.has(id) ? saved.delete(id) : saved.add(id); persistSaved(); renderCalendar(); return; }
      const shareButton = event.target.closest('[data-share]'); if (shareButton) { const url = `${location.origin}${location.pathname}#${shareButton.dataset.share}`; try { if (navigator.share) await navigator.share({title:'Concerto su CurioMondo',url}); else { await navigator.clipboard.writeText(url); shareButton.textContent='Link copiato'; } } catch (_) {} return; }
      const regionButton = event.target.closest('[data-region]'); if (regionButton) { $('#regionFilter').value = regionButton.dataset.region; renderCalendar(); $('#calendar-title').scrollIntoView({behavior:'smooth'}); }
    });
  }
  function addEventSchema(events) {
    const script = document.createElement('script'); script.type = 'application/ld+json'; script.textContent = JSON.stringify({'@context':'https://schema.org','@graph':events.slice(0,20).map(event => ({'@type':'MusicEvent','@id':`https://curiomondo.it/concerti/#${event.id}`,name:`${event.artist} – ${event.city}`,startDate:event.start,eventStatus:'https://schema.org/EventScheduled',location:{'@type':'Place',name:event.venue,address:{'@type':'PostalAddress',addressLocality:event.city,addressRegion:event.region,addressCountry:'IT'}},performer:{'@type':'MusicGroup',name:event.artist},offers:event.ticketUrl?{'@type':'Offer',url:event.ticketUrl,availability:event.ticketStatus==='sold-out'?'https://schema.org/SoldOut':'https://schema.org/InStock'}:undefined,url:`https://curiomondo.it/concerti/#${event.id}`}))}); document.head.appendChild(script);
  }
  function handleHash() { if (!location.hash) return; const target = document.getElementById(decodeURIComponent(location.hash.slice(1))); if (target) setTimeout(() => target.scrollIntoView({behavior:'smooth',block:'center'}),120); }
  async function init() {
    try { const response = await fetch(DATA_URL,{cache:'no-cache'}); if (!response.ok) throw new Error(`HTTP ${response.status}`); data = await response.json(); }
    catch (_) { const target = $('#concertGroups') || $('#archiveGroups'); if (target) target.innerHTML='<p class="empty-state">Il calendario non è disponibile in questo momento. Riprova tra poco.</p>'; return; }
    if (window.CONCERT_ARCHIVE) { const events = archivedEvents().sort((a,b)=>new Date(b.start)-new Date(a.start)); $('#archiveGroups').innerHTML = groupMarkup(events,true); return; }
    const active = activeEvents(); $('#heroCount').textContent = `${active.length} date verificate`; $('#lastVerified').textContent = `Verificato ${fmtVerified.format(new Date(data.lastVerified))}`;
    fillOptions(); renderFeatured(); renderCalendar(); renderNews(); bindEvents(); addEventSchema(active); handleHash();
  }
  document.addEventListener('DOMContentLoaded', init);
})();
