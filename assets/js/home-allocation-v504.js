/* CurioMondo v519 — three-item featured carousel with category handoff. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.CMHomepageAllocation = api;
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';

  const CONFIG = Object.freeze({
    timeZone: 'Europe/Rome',
    promotionHours: 3,
    featuredCapacity: 3,
    latestCapacity: 5,
    smallCardsPerCategory: 11,
    categories: Object.freeze([
      { id: 'sport', label: 'Sport', color: '#1565C0', archive: '/categorie/sport/', aliases: ['sport', 'calcio', 'basket', 'tennis', 'motogp'] },
      { id: 'politica', label: 'Politica', color: '#B91C1C', archive: '/categorie/politica/', aliases: ['politica', 'governo', 'parlamento', 'elezioni'] },
      { id: 'film-tv', label: 'Film e Serie TV', color: '#6D28D9', archive: '/categorie/cultura/', aliases: ['film e serie tv', 'film', 'cinema', 'serie tv', 'streaming'] },
      { id: 'meteo', label: 'Meteo', color: '#047857', archive: '/categorie/meteo/', aliases: ['meteo', 'previsioni', 'maltempo'] },
      { id: 'cronaca', label: 'Cronaca', color: '#9A3412', archive: '/categorie/cronaca/', aliases: ['cronaca', 'giustizia', 'sicurezza'] },
      { id: 'tecnologia', label: 'Tecnologia', color: '#0E7490', archive: '/categorie/tecnologia/', aliases: ['tecnologia', 'digitale', 'intelligenza artificiale'] },
      { id: 'economia', label: 'Economia', color: '#854D0E', archive: '/categorie/economia/', aliases: ['economia', 'finanza', 'lavoro'] },
      { id: 'scienza', label: 'Scienza', color: '#4338CA', archive: '/categorie/scienza/', aliases: ['scienza', 'ricerca', 'spazio'] },
      { id: 'ambiente', label: 'Ambiente', color: '#3F6212', archive: '/categorie/ambiente/', aliases: ['ambiente', 'clima', 'natura'] },
      { id: 'cultura', label: 'Cultura', color: '#9D174D', archive: '/categorie/cultura/', aliases: ['cultura', 'spettacolo'] },
      { id: 'italia', label: 'Italia', color: '#0F766E', archive: '/categorie/italia/', aliases: ['italia'] },
      { id: 'mondo', label: 'Mondo', color: '#475569', archive: '/categorie/mondo/', aliases: ['mondo'] }
    ])
  });

  const normalize = (value) => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('it');
  const canonicalKey = (entry) => {
    if (entry && entry.id) return 'id:' + String(entry.id).trim().toLowerCase();
    try {
      const url = new URL(String(entry && entry.url || ''), 'https://curiomondo.it');
      return 'url:' + url.pathname.replace(/\/{2,}/g, '/').replace(/\/$/, '') + url.search;
    } catch { return ''; }
  };
  const zonedDay = (date, timeZone = CONFIG.timeZone) => {
    if (!(date instanceof Date) || Number.isNaN(date.getTime())) return '';
    const parts = new Intl.DateTimeFormat('en-CA', { timeZone, year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(date);
    const get = (type) => parts.find((part) => part.type === type)?.value || '';
    return `${get('year')}-${get('month')}-${get('day')}`;
  };
  const firstPublished = (entry) => {
    const raw = entry && (entry.firstPublishedAt || entry.dateISO);
    const date = new Date(raw || '');
    return Number.isNaN(date.getTime()) ? null : date;
  };
  const isPromotable = (entry, now = new Date()) => {
    const published = firstPublished(entry);
    if (!published || published > now) return false;
    return zonedDay(published) === zonedDay(now) && now.getTime() - published.getTime() < CONFIG.promotionHours * 3600000;
  };
  const importance = (entry) => Number(entry && entry.homepagePriority) || 0;
  const isImportant = (entry) => importance(entry) > 0;
  const categoryFor = (entry) => {
    const explicit = normalize(entry && entry.primaryCategory);
    if (explicit) {
      const match = CONFIG.categories.find((category) => category.id === explicit || normalize(category.label) === explicit);
      if (match) return match;
    }
    const section = normalize(entry && entry.section);
    return CONFIG.categories.find((category) => category.aliases.some((alias) => section.split(/\s*[\/.·]\s*/).includes(normalize(alias))))
      || CONFIG.categories.find((category) => category.aliases.some((alias) => section.includes(normalize(alias))))
      || null;
  };
  const prepare = (items, now) => {
    const unique = new Map();
    (Array.isArray(items) ? items : []).forEach((entry) => {
      const key = canonicalKey(entry);
      const published = firstPublished(entry);
      if (!key || !published || published > now || entry.draft === true || entry.published === false) return;
      if (!unique.has(key)) unique.set(key, { ...entry, _key: key, _published: published });
    });
    return Array.from(unique.values()).sort((a, b) => b._published - a._published || a._key.localeCompare(b._key));
  };
  function allocate(items, options = {}) {
    const now = options.now instanceof Date ? options.now : new Date(options.now || Date.now());
    const featuredCapacity = Number.isInteger(options.featuredCapacity) ? options.featuredCapacity : CONFIG.featuredCapacity;
    const latestCapacity = Number.isInteger(options.latestCapacity) ? options.latestCapacity : CONFIG.latestCapacity;
    const smallCapacity = Number.isInteger(options.smallCardsPerCategory) ? options.smallCardsPerCategory : CONFIG.smallCardsPerCategory;
    const available = prepare(items, now);
    const used = new Set();
    const take = (entry) => { if (entry) used.add(entry._key); return entry || null; };
    const remaining = () => available.filter((entry) => !used.has(entry._key));

    // The three newest published entries belong exclusively to the main carousel.
    // When a fourth entry arrives, the displaced one becomes available to its category.
    const featuredItems = remaining().slice(0, featuredCapacity).map(take);
    const featured = featuredItems[0] || null;
    const sections = [];
    CONFIG.categories.forEach((category) => {
      const pool = remaining().filter((entry) => categoryFor(entry)?.id === category.id);
      const leadCandidate = pool[0];
      const cardCandidates = pool.slice(1, smallCapacity);
      if (!leadCandidate || !cardCandidates.length) return;
      const lead = take(leadCandidate);
      const cards = cardCandidates.map(take);
      sections.push({ category, lead, cards });
    });
    // Desktop may still show the legacy latest strip, but only with entries not already
    // reserved by the featured carousel or a category.
    const latest = remaining().slice(0, latestCapacity).map(take);
    return { featured, featuredItems, latest, sections, rest: remaining(), used, now };
  }
  function nextExpiry(allocation) {
    const leads = (allocation && allocation.featuredItems || [allocation && allocation.featured]).concat((allocation && allocation.sections || []).map((section) => section.lead)).filter(Boolean);
    if (!leads.length) return null;
    const now = allocation.now instanceof Date ? allocation.now : new Date();
    const today = zonedDay(now);
    let low = now.getTime();
    let high = low + 27 * 3600000;
    while (high - low > 1) {
      const middle = Math.floor((low + high) / 2);
      if (zonedDay(new Date(middle)) === today) low = middle;
      else high = middle;
    }
    const futureExpiries = leads
      .map((entry) => firstPublished(entry).getTime() + CONFIG.promotionHours * 3600000)
      .filter((timestamp) => timestamp > now.getTime());
    return new Date(Math.min(high, ...futureExpiries));
  }
  return { CONFIG, allocate, canonicalKey, categoryFor, firstPublished, importance, isPromotable, nextExpiry, zonedDay };
}));
