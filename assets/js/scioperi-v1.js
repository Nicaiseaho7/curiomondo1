(() => {
  'use strict';

  const DATA_URL = '/assets/data/scioperi.json';
  const page = document.documentElement.dataset.page || 'current';
  const state = { data: null, current: [], filtered: [], openRegions: new Set() };
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
          <h3>${escapeHtml(event.title)}</h3>
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
    target.innerHTML = events.length ? events.map(event => eventCard(event, 'national')).join('') : empty('Nessuno sciopero nazionale corrisponde ai filtri selezionati.');
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
      $('.region-next', item).textContent = filtered.length ? `Prossimo: ${shortDate(filtered[0])}` : 'Prossimo: non disponibile';
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
    if (summary) summary.textContent = `${plural(state.filtered.length)} corrispondenti. I conteggi regionali includono gli scioperi nazionali pertinenti.`;
  }

  function bindFilters() {
    const form = $('#strikeFilters');
    if (!form) return;
    const period = $('#periodFilter');
    const custom = $('#customDates');
    const updateCustom = () => { custom.hidden = period.value !== 'custom'; };
    form.addEventListener('input', () => { updateCustom(); applyFilters(); });
    form.addEventListener('change', () => { updateCustom(); applyFilters(); });
    form.addEventListener('reset', () => setTimeout(() => { updateCustom(); applyFilters(); }, 0));
    updateCustom();
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
    const hash = decodeURIComponent(location.hash.replace(/^#/, ''));
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
      setRegionOpen(event.regions[0], true, false);
    }
    const card = document.querySelector(`[data-event-id="${CSS.escape(hash)}"]`);
    const fold = card?.querySelector('details');
    if (fold) fold.open = true;
    card?.scrollIntoView({block:'center'});
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
      if (verified) verified.textContent = state.data.meta.verificationLabel || verifiedDate(state.data.meta.lastVerified);
      state.current = sorted(state.data.events.filter(event => !isFinished(event)));
      state.filtered = [...state.current];
      buildRegions();
      bindFilters();
      applyFilters();
      renderNews();
      openFromHash();
      window.addEventListener('hashchange', openFromHash);
    } catch (error) {
      console.error('Impossibile caricare il calendario scioperi:', error);
      ['#nationalEvents','#regionsAccordion','#archiveEvents','#strikeNews'].forEach(selector => {
        const target = $(selector); if (target) target.innerHTML = empty('Il calendario non è disponibile in questo momento. Riprova più tardi.');
      });
    }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init, {once:true});
  else init();
})();
