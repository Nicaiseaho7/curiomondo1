(() => {
  'use strict';

  const DATA_URL = '/assets/data/scioperi.json';
  const page = document.documentElement.dataset.page || 'current';
  const state = { data: null, current: [], filtered: [], openRegions: new Set(), resettingForLink: false };
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const fallback = (value) => value === null || value === undefined || value === '' ? 'Non comunicato' : String(value);
  const escapeHtml = (value) => fallback(value).replace(/[&<>'"]/g, char => ({'&':'&','<':'<','>':'>',"'":'&#39;','"':'"'}[char]));
  const safeUrl = (value) => {
    if (typeof value !== 'string') return '#';
    if (value.startsWith('/')) return value;
    try { const url = new URL(value); return /^https?:$/.test(url.protocol) ? url.href : '#'; } catch (_) { return '#'; }
  };
  const titleCase = (value) => fallback(value).charAt(0).toUpperCase() + fallback(value).slice(1);
  const plural = (count, one = 'evento', many = 'eventi') => `${count} ${count === 1 ? one : many}`;

  function romeToday() {
    const parts = new Intl.DateTimeFormat('en-CA', {timeZone:'Europe/Rome', year:'numeric', month:'2-digit', day:'2-digit'}).formatToParts(new Date());
    const value = Object.fromEntries(parts.map(part => [part.type, part.value]));
    return `${value.year}-${value.month}-${value.day}`;
  }

  function addDays(dateString, amount) {
    const date = new Date(`${dateString}T12:00:00Z`);
    date.setUTCDate(date.getUTCDate() + amount);
    return date.toISOString().slice(0, 10);
  }

  function monthEnd(dateString) {
    const [year, month] = dateString.split('-').map(Number);
    return new Date(Date.UTC(year, month, 0, 12)).toISOString().slice(0, 10);
  }

  function isFinished(event) {
    const end = new Date(event.endsAt || `${event.endDate}T23:59:59+01:00`);
    return Number.isFinite(end.getTime()) && end < new Date();
  }

  function sorted(events, direction = 'asc') {
    return [...events].sort((a, b) => {
      const diff = new Date(a.startsAt).getTime() - new Date(b.startsAt).getTime();
      return direction === 'desc' ? -diff : diff;
    });
  }

  function dateParts(event) {
    const date = new Date(event.startsAt);
    const weekday = new Intl.DateTimeFormat('it-IT', {timeZone:'Europe/Rome', weekday:'short'}).format(date).replace('.', '');
    const day = new Intl.DateTimeFormat('it-IT', {timeZone:'Europe/Rome', day:'2-digit'}).format(date);
    const month = new Intl.DateTimeFormat('it-IT', {timeZone:'Europe/Rome', month:'short'}).format(date).replace('.', '');
    return {weekday, day, month};
  }

  function longDate(event) {
    const start = new Date(event.startsAt);
    const end = new Date(event.endsAt);
    const format = new Intl.DateTimeFormat('it-IT', {timeZone:'Europe/Rome', weekday:'long', day:'numeric', month:'long', year:'numeric'});
    if (event.startDate === event.endDate) return format.format(start);
    return `${format.format(start)} – ${format.format(end)}`;
  }

  function shortDate(event) {
    return new Intl.DateTimeFormat('it-IT', {timeZone:'Europe/Rome', day:'numeric', month:'short'}).format(new Date(event.startsAt)).replace('.', '');
  }

  function verifiedDate(value) {
    if (!value) return 'Non comunicato';
    return new Intl.DateTimeFormat('it-IT', {timeZone:'Europe/Rome', day:'numeric', month:'long', year:'numeric', hour:'2-digit', minute:'2-digit'}).format(new Date(value));
  }

  function articleBlock(article) {
    if (!article || !article.url) return '';
    const image = article.image ? `<img src="${escapeHtml(safeUrl(article.image))}" alt="${escapeHtml(article.imageAlt || article.title || '')}" width="296" height="184" loading="lazy" decoding="async">` : '';
    return `<a class="article-preview" href="${escapeHtml(safeUrl(article.url))}"><span class="sector-label">Notizia</span>${image}<strong>${escapeHtml(article.title)}</strong><span>${escapeHtml(article.summary)}</span></a>`;
  }

  function eventCard(event, context = 'list') {
    const d = dateParts(event);
    return `<article class="event-card" data-status="${escapeHtml(event.status)}" data-event-id="${escapeHtml(event.id)}" data-context="${escapeHtml(context)}">
      <details class="event-fold">
        <summary>
          <time class="event-date" datetime="${escapeHtml(event.startsAt)}"><span class="weekday">${escapeHtml(d.weekday)}</span><strong>${escapeHtml(d.day)}</strong><span class="month">${escapeHtml(d.month)}</span></time>
          ${page === 'current' ? `<span class="event-heading"><span class="event-title">${escapeHtml(event.title)}</span><span class="event-preview">${escapeHtml(event.sectorLabel)} · ${escapeHtml(event.territory)}<br>${escapeHtml(event.scheduleText)}</span></span>` : `<h3>${escapeHtml(event.title)}</h3>`}
          <span class="status-badge" data-status="${escapeHtml(event.status)}">${escapeHtml(titleCase(event.status))}</span>
          <span class="fold-chevron" aria-hidden="true"></span>
        </summary>
        <div class="event-body">
          <p class="event-essentials"><span>${escapeHtml(longDate(event))}</span><span>${escapeHtml(event.scheduleText)}</span><span>${escapeHtml(event.territory)}</span><span>${escapeHtml(event.sectorLabel)}</span></p>
          <dl class="event-details">
            <div><dt>Azienda, ente o servizio</dt><dd>${escapeHtml(event.services)}</dd></div>
            <div><dt>Organizzazioni proclamanti</dt><dd>${escapeHtml(event.organizations)}</dd></div>
            <div><dt>Fasce e servizi garantiti</dt><dd>${escapeHtml(event.guarantees)}</dd></div>
            <div><dt>Ultima verifica</dt><dd>${escapeHtml(verifiedDate(event.verifiedAt))} · Europe/Rome</dd></div>
          </dl>
          ${event.source?.url ? `<p class="event-source"><a href="${escapeHtml(safeUrl(event.source.url))}">Fonte ufficiale: ${escapeHtml(event.source.label)}</a></p>` : ''}
          ${articleBlock(event.article)}
        </div>
      </details>
    </article>`;
  }

  function empty(message) { return `<p class="empty-state">${escapeHtml(message)}</p>`; }

  function renderNational() {
    const target = $('#nationalEvents');
    if (!target) return;
    const events = sorted(state.filtered.filter(event => event.national));
    target.innerHTML = events.length ? events.map(event => eventCard(event, 'national')).join('') : empty(state.current.some(event => event.national) ? 'Nessuno sciopero nazionale corrisponde ai filtri. Prova a cambiare periodo, settore o stato.' : 'Al momento non risultano scioperi nazionali in calendario.');
    $('#nationalCount').textContent = plural(events.length);
  }

  function regionShell(region) {
    return `<section class="region-item" id="${escapeHtml(region.slug)}" data-region="${escapeHtml(region.slug)}">
      <h3>
        <button class="region-toggle" type="button" aria-expanded="false" aria-controls="panel-${escapeHtml(region.slug)}">
          <span class="region-title">${escapeHtml(region.name)}</span>
          <span class="region-meta"><span class="region-count">0 scioperi</span><span class="region-next">Prossimo: non disponibile</span></span>
          <span class="fold-chevron" aria-hidden="true"></span>
        </button>
      </h3>
      <div class="region-panel" id="panel-${escapeHtml(region.slug)}" hidden></div>
    </section>`;
  }

  function buildRegions() {
    const root = $('#regionsAccordion');
    if (!root) return;
    root.innerHTML = state.data.regions.map(regionShell).join('');
    $$('.region-toggle', root).forEach(button => button.addEventListener('click', () => {
      const item = button.closest('.region-item');
      const slug = item.dataset.region;
      const open = button.getAttribute('aria-expanded') !== 'true';
      setRegionOpen(slug, open, true);
    }));
    const search = $('#regionSearch');
    if (search) search.addEventListener('input', filterRegionList);
    const jump = $('#regionJump');
    if (jump) {
      state.data.regions.forEach(region => jump.add(new Option(region.name, region.slug)));
      $('#regionQuick').hidden = false;
      jump.addEventListener('change', () => {
        if (!jump.value) return;
        if (search) search.value = '';
        filterRegionList();
        $('#regionsFold').open = true;
        setRegionOpen(jump.value, true, true);
        $('.region-toggle', document.getElementById(jump.value)).focus({preventScroll:true});
        document.getElementById(jump.value).scrollIntoView({block:'start'});
      });
    }
  }

  function filterRegionList() {
    const query = ($('#regionSearch')?.value || '').trim().toLocaleLowerCase('it-IT');
    let visible = 0;
    state.data.regions.forEach(region => {
      const item = document.getElementById(region.slug);
      if (!item) return;
      const match = !query || region.name.toLocaleLowerCase('it-IT').includes(query);
      item.hidden = !match;
      if (match) visible += 1;
    });
    const emptyState = $('#regionSearchEmpty');
    if (emptyState) emptyState.hidden = visible !== 0;
  }

  function setRegionOpen(slug, open, updateLocation = false) {
    const item = document.getElementById(slug);
    if (!item) return;
    const button = $('.region-toggle', item);
    const panel = $('.region-panel', item);
    button.setAttribute('aria-expanded', String(open));
    panel.hidden = !open;
    if (open) state.openRegions.add(slug); else state.openRegions.delete(slug);
    if (open && updateLocation) history.replaceState(null, '', `#${slug}`);
  }

  function renderRegions() {
    state.data.regions.forEach(region => {
      const item = document.getElementById(region.slug);
      if (!item) return;
      const allRegionEvents = state.current.filter(event => event.regions.includes(region.slug));
      const filtered = sorted(state.filtered.filter(event => event.regions.includes(region.slug)));
      $('.region-count', item).textContent = plural(filtered.length, 'sciopero', 'scioperi');
      $('.region-next', item).textContent = filtered.length ? `Prossimo: ${shortDate(filtered[0])}` : 'Nessuna data nei risultati';
      const panel = $('.region-panel', item);
      if (filtered.length) panel.innerHTML = `<div class="events-list">${filtered.map(event => eventCard(event, `region-${region.slug}`)).join('')}</div>`;
      else if (!allRegionEvents.length) panel.innerHTML = empty('Al momento non risultano scioperi programmati per questa regione.');
      else panel.innerHTML = empty('Nessuno sciopero corrisponde ai filtri selezionati.');
    });
  }

  function filterEvents(events) {
    const period = $('#periodFilter')?.value || 'all';
    const sector = $('#sectorFilter')?.value || 'all';
    const status = $('#statusFilter')?.value || 'all';
    const query = ($('#searchFilter')?.value || '').trim().toLocaleLowerCase('it-IT');
    const today = romeToday();
    let from = null, to = null;
    if (period === 'today') from = to = today;
    if (period === '7days') { from = today; to = addDays(today, 6); }
    if (period === 'month') { from = `${today.slice(0, 7)}-01`; to = monthEnd(today); }
    if (period === 'custom') { from = $('#dateFrom')?.value || null; to = $('#dateTo')?.value || null; }
    return events.filter(event => {
      if (sector !== 'all' && event.sector !== sector) return false;
      if (status !== 'all' && event.status !== status) return false;
      if (from && event.endDate < from) return false;
      if (to && event.startDate > to) return false;
      if (query) {
        const haystack = [event.title,event.sectorLabel,event.territory,event.services,event.organizations,event.status].join(' ').toLocaleLowerCase('it-IT');
        if (!haystack.includes(query)) return false;
      }
      return true;
    });
  }

  function applyFilters() {
    state.filtered = filterEvents(state.current);
    renderNational();
    renderRegions();
    const summary = $('#filterSummary');
    if (summary) summary.textContent = state.filtered.length
      ? `${plural(state.filtered.length, 'sciopero', 'scioperi')} nel calendario. I conteggi per regione includono gli eventi nazionali pertinenti.`
      : (state.current.length ? 'Nessuno sciopero corrisponde a questi filtri. Cambia la ricerca o azzera i filtri.' : 'Al momento non risultano scioperi in calendario. Consulta l’archivio per gli eventi conclusi.');
    const chosen = $('#periodFilter').value;
    const day = chosen === 'today' ? romeToday() : (chosen === 'custom' && $('#dateFrom').value === $('#dateTo').value ? $('#dateFrom').value : '');
    $$('#strikeDates button').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.day === day)));
  }

  function bindFilters() {
    const form = $('#strikeFilters');
    if (!form) return;
    const period = $('#periodFilter');
    const custom = $('#customDates');
    const updateCustom = () => { custom.hidden = period.value !== 'custom'; };
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('input', () => { updateCustom(); applyFilters(); });
    form.addEventListener('change', () => { updateCustom(); applyFilters(); });
    form.addEventListener('reset', () => {
      if (!state.resettingForLink) setTimeout(() => { updateCustom(); applyFilters(); }, 0);
    });
    updateCustom();
  }

  function renderSpotlight() {
    const target = $('#nextStrikes');
    if (!target) return;
    const today = romeToday();
    const fmt = new Intl.DateTimeFormat('it-IT', { weekday:'long', day:'numeric', month:'long', timeZone:'Europe/Rome' });
    const label = $('#strikeToday');
    label.dateTime = today;
    label.textContent = fmt.format(new Date(`${today}T12:00:00Z`));
    label.hidden = false;
    target.addEventListener('click', click => {
      const link = click.target.closest('a');
      if (link && link.hash === location.hash) {
        click.preventDefault();
        openFromHash();
      }
    });
    const events = state.current.filter(event => !['revocato','rinviato'].includes(event.status));
    target.innerHTML = events.length ? events.slice(0, 3).map(event => {
      const d = dateParts(event);
      const isToday = event.startDate <= today && event.endDate >= today;
      return `<article class="strike-next-card">
        <div class="strike-next-top"><time datetime="${escapeHtml(event.startsAt)}"><strong>${escapeHtml(isToday ? 'Oggi' : d.weekday)}</strong>${isToday ? '' : ' ' + escapeHtml(d.day + ' ' + d.month)}</time><span class="status-badge" data-status="${escapeHtml(event.status)}">${escapeHtml(titleCase(event.status))}</span></div>
        <h3><a href="#${escapeHtml(encodeURIComponent(event.id))}">${escapeHtml(event.title)}</a></h3>
        <p>${escapeHtml(event.sectorLabel)} · ${escapeHtml(event.territory)}</p>
        <p class="strike-next-hours">${escapeHtml(event.scheduleText)}</p>
      </article>`;
    }).join('') : empty('Al momento non risultano scioperi in evidenza. Verifica il calendario o consulta l’archivio.');
  }

  function renderDates() {
    const rail = $('#strikeDates');
    if (!rail) return;
    const today = romeToday();
    const weekdays = new Intl.DateTimeFormat('it-IT', { weekday:'short', timeZone:'Europe/Rome' });
    const dates = new Intl.DateTimeFormat('it-IT', { day:'numeric', month:'short', timeZone:'Europe/Rome' });
    rail.innerHTML = Array.from({length:7}, (_, index) => {
      const date = addDays(today, index);
      const moment = new Date(`${date}T12:00:00Z`);
      const count = state.current.filter(event => event.startDate <= date && event.endDate >= date).length;
      const name = index ? weekdays.format(moment) : 'Oggi';
      return `<button type="button" data-day="${date}" aria-pressed="false" aria-label="${escapeHtml(name + ' ' + dates.format(moment) + ': ' + plural(count))}"><span>${escapeHtml(name)}</span><strong>${escapeHtml(dates.format(moment))}</strong><small>${plural(count, 'evento', 'eventi')}</small></button>`;
    }).join('');
    rail.hidden = false;
    rail.addEventListener('click', event => {
      const button = event.target.closest('button[data-day]');
      if (!button) return;
      const active = button.getAttribute('aria-pressed') === 'true';
      $('#periodFilter').value = active ? 'all' : 'custom';
      $('#dateFrom').value = $('#dateTo').value = active ? '' : button.dataset.day;
      $('#customDates').hidden = active;
      applyFilters();
    });
  }

  function renderNews() {
    const target = $('#strikeNews');
    if (!target) return;
    const section = target.closest('section');
    const articles = [...(state.data.articles || [])].sort((a,b) => new Date(b.publishedAt) - new Date(a.publishedAt));
    if (!articles.length) {
      target.innerHTML = '';
      if (section) section.hidden = true;
      return;
    }
    if (section) section.hidden = false;
    target.innerHTML = articles.map(article => `<article class="news-card"><a href="${escapeHtml(safeUrl(article.url))}">${article.image ? `<img src="${escapeHtml(safeUrl(article.image))}" alt="${escapeHtml(article.imageAlt || '')}" width="640" height="360" loading="lazy" decoding="async">` : ''}<div><time datetime="${escapeHtml(article.publishedAt)}">${escapeHtml(verifiedDate(article.publishedAt))}</time><h3>${escapeHtml(article.title)}</h3><p>${escapeHtml(article.summary)}</p></div></a></article>`).join('');
  }

  function openFromHash() {
    let hash;
    try { hash = decodeURIComponent(location.hash.replace(/^#/, '')); } catch (_) { return; }
    if (!hash) return;
    const regionsFold = document.getElementById('regionsFold');
    if (state.data.regions.some(region => region.slug === hash)) {
      if (regionsFold) regionsFold.open = true;
      const search = $('#regionSearch');
      if (search) search.value = '';
      filterRegionList();
      setRegionOpen(hash, true, false);
      document.getElementById(hash)?.scrollIntoView({block:'start'});
      return;
    }
    const event = state.data.events.find(item => item.id === hash);
    if (!event) return;
    if (!event.national && event.regions[0]) {
      if (regionsFold) regionsFold.open = true;
      if ($('#regionSearch')) $('#regionSearch').value = '';
      filterRegionList();
      setRegionOpen(event.regions[0], true, false);
    }
    if (!state.filtered.some(item => item.id === hash) && state.current.some(item => item.id === hash)) {
      state.resettingForLink = true;
      $('#strikeFilters')?.reset();
      state.resettingForLink = false;
      $('#customDates').hidden = true;
      applyFilters();
    }
    const card = document.querySelector(`[data-event-id="${CSS.escape(hash)}"]`);
    const fold = card?.querySelector('details');
    if (fold) fold.open = true;
    card?.scrollIntoView({block:'center'});
    if (card && document.activeElement?.closest('#nextStrikes')) fold?.querySelector('summary')?.focus({preventScroll:true});
  }

  function renderArchive() {
    const events = sorted(state.data.events.filter(isFinished), 'desc');
    const target = $('#archiveEvents');
    if (!target) return;
    target.innerHTML = events.length ? events.map(event => eventCard(event, 'archive')).join('') : empty('L’archivio non contiene ancora eventi conclusi.');
    $('#archiveCount').textContent = plural(events.length);
  }

  async function init() {
    try {
      const response = await fetch(DATA_URL, {headers:{'Accept':'application/json'}});
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      state.data = await response.json();
      if (!Array.isArray(state.data.regions) || !Array.isArray(state.data.events)) throw new Error('Formato dati non valido');
      if (page === 'archive') { renderArchive(); return; }
      const verified = $('#lastVerified');
      if (verified) verified.textContent = state.data.meta?.verificationLabel || verifiedDate(state.data.meta?.lastVerified);
      state.current = sorted(state.data.events.filter(event => !isFinished(event)));
      state.filtered = [...state.current];
      renderSpotlight();
      renderDates();
      buildRegions();
      bindFilters();
      applyFilters();
      renderNews();
      openFromHash();
      window.addEventListener('hashchange', openFromHash);
    } catch (error) {
      console.error('Impossibile caricare il calendario scioperi:', error);
      if ($('#lastVerified')) $('#lastVerified').textContent = 'Non disponibile';
      if ($('#nationalCount')) $('#nationalCount').textContent = 'Non disponibile';
      ['#nextStrikes','#nationalEvents','#regionsAccordion','#archiveEvents','#strikeNews'].forEach(selector => {
        const target = $(selector); if (target) target.innerHTML = empty('Il calendario non è disponibile in questo momento. Riprova più tardi.');
      });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true});
  else init();
})();
