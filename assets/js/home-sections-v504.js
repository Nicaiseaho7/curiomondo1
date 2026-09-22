/* CurioMondo v510 — stable image frames for every category card. */
(() => {
  'use strict';
  const A = window.CMHomepageAllocation;
  if (!A) return;
  const $ = (selector, root = document) => root.querySelector(selector);
  const zone = document.createElement('div');
  zone.id = 'cm-home-editorial-v504';
  zone.className = 'cm-home-editorial';
  zone.setAttribute('aria-live', 'polite');
  const legacyFeatured = $('.featured');
  const legacyLatestTitle = $('.auto-rail-label');
  const legacyLatest = $('.auto-rail');
  if (!legacyFeatured || !legacyLatestTitle || !legacyLatest) return;
  legacyFeatured.before(zone);
  [legacyFeatured, legacyLatestTitle, legacyLatest].forEach((node) => { node.hidden = true; node.setAttribute('aria-hidden', 'true'); });

  let timer = 0;
  let generation = 0;
  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const formatDate = (entry) => {
    const date = A.firstPublished(entry);
    if (!date) return '';
    return new Intl.DateTimeFormat('it-IT', { timeZone: A.CONFIG.timeZone, day: 'numeric', month: 'long', year: 'numeric', hour: '2-digit', minute: '2-digit' }).format(date);
  };
  const picture = (entry, eager = false) => {
    if (!entry.image) return null;
    const wrap = el('picture');
    const image = el('img');
    image.src = entry.image;
    if (entry.srcset) image.srcset = entry.srcset;
    image.sizes = '(max-width: 600px) calc(100vw - 28px), (max-width: 900px) calc(50vw - 32px), 380px';
    image.alt = entry.imageAlt || '';
    image.width = entry.imageWidth || 800;
    image.height = entry.imageHeight || 533;
    image.loading = eager ? 'eager' : 'lazy';
    image.decoding = 'async';
    if (eager) image.fetchPriority = 'high';
    image.addEventListener('error', () => {
      wrap.classList.add('cm-image-frame--error');
      image.setAttribute('aria-hidden', 'true');
    }, { once: true });
    wrap.append(image);
    return wrap;
  };
  const time = (entry) => {
    const node = el('time', '', formatDate(entry));
    node.dateTime = entry.firstPublishedAt || entry.dateISO || '';
    return node;
  };
  const largeCard = (entry, label, color, primary = false) => {
    const article = el('article', 'cm-topic-lead' + (primary ? ' cm-topic-lead--primary' : ''));
    article.style.setProperty('--cm-category-color', color);
    const visual = picture(entry, primary);
    const body = el('div', 'cm-topic-lead__body');
    body.append(el('span', 'cm-topic-label', label));
    const title = el(primary ? 'h1' : 'h3', 'cm-topic-lead__title', entry.title);
    body.append(title);
    if (entry.excerpt) body.append(el('p', 'cm-topic-lead__summary', entry.excerpt));
    const footer = el('div', 'cm-topic-lead__footer');
    const link = el('a', 'cm-topic-lead__cta', 'Leggi l’articolo →');
    link.href = entry.url;
    footer.append(link, time(entry));
    body.append(footer);
    article.append(body);
    if (visual) article.append(visual);
    return article;
  };
  const smallCard = (entry, category) => {
    const link = el('a', 'cm-topic-card');
    link.href = entry.url;
    link.style.setProperty('--cm-category-color', category.color);
    const body = el('div', 'cm-topic-card__body');
    body.append(el('span', 'cm-topic-label', category.label));
    body.append(el('h3', 'cm-topic-card__title', entry.title));
    const visual = picture(entry);
    if (visual) body.append(visual);
    body.append(time(entry));
    link.append(body);
    return link;
  };
  const latestCard = (entry) => {
    const category = A.categoryFor(entry) || { label: String(entry.section || 'Notizie').split('/').pop().trim(), color: '#475569' };
    return smallCard(entry, category);
  };
  const section = ({ category, lead, cards }) => {
    const block = el('section', 'cm-topic-section');
    block.dataset.category = category.id;
    block.style.setProperty('--cm-category-color', category.color);
    if (lead) block.append(largeCard(lead, category.label, category.color));
    const rail = el('div', 'cm-topic-section__rail');
    rail.dataset.forCategory = category.id;
    rail.append(el('h2', 'cm-topic-section__title', category.label));
    if (cards.length) {
      const grid = el('div', 'cm-topic-grid');
      grid.append(...cards.map((entry) => smallCard(entry, category)));
      rail.append(grid);
    }
    if (category.archive) {
      const archive = el('a', 'cm-topic-archive', category.id === 'meteo' ? 'Tutte le notizie Meteo →' : `Tutte le notizie di ${category.label} →`);
      archive.href = category.archive;
      rail.append(archive);
    }
    block.append(rail);
    return block;
  };
  function updateRest(allocation) {
    const cards = $('#cards');
    if (!cards) return;
    const limit = Number(cards.dataset.initialCount || 41);
    cards.replaceChildren(...allocation.rest.slice(0, limit).map((entry) => {
      const category = A.categoryFor(entry) || { label: String(entry.section || 'Notizie').split('/').pop().trim(), color: '#475569' };
      const card = smallCard(entry, category);
      card.classList.add('card');
      return card;
    }));
    cards.dataset.initialCount = String(Math.min(limit, allocation.rest.length));
    const loadMore = $('#loadMoreNews');
    if (loadMore) loadMore.hidden = true;
  }
  function verifyUnique() {
    const keys = Array.from(document.querySelectorAll('#cm-home-editorial-v504 a[href^="/notizie/"], #cards a[href^="/notizie/"]'))
      .map((link) => A.canonicalKey({ url: link.getAttribute('href') })).filter(Boolean);
    if (keys.length !== new Set(keys).size) throw new Error('Homepage CurioMondo: identificativi duplicati');
    zone.dataset.cardCount = String(keys.length);
    zone.dataset.uniqueCardCount = String(new Set(keys).size);
  }
  async function render() {
    const current = ++generation;
    clearTimeout(timer);
    const nonce = Date.now();
    const [response, configResponse] = await Promise.all([
      fetch('/assets/data/home-feed-v210.json?homepage=v504&t=' + nonce, { credentials: 'same-origin', cache: 'no-store' }),
      fetch('/assets/data/homepage-config-v504.json?t=' + nonce, { credentials: 'same-origin', cache: 'no-store' })
    ]);
    if (!response.ok || !configResponse.ok) throw new Error('Feed homepage non disponibile');
    const [payload, editorialConfig] = await Promise.all([response.json(), configResponse.json()]);
    const overrides = editorialConfig && editorialConfig.articles || {};
    const items = (Array.isArray(payload.items) ? payload.items : []).map((entry) => ({ ...entry, ...(overrides[entry.url] || {}) }));
    if (current !== generation) return;
    const allocation = A.allocate(items, { now: new Date() });
    const fragment = document.createDocumentFragment();
    if (allocation.featured) fragment.append(largeCard(allocation.featured, 'In primo piano', '#B91C1C', true));
    const latestSection = el('section', 'cm-latest-section');
    latestSection.append(el('h2', 'cm-latest-title', 'Ultime notizie'));
    const latestGrid = el('div', 'cm-latest-grid');
    latestGrid.append(...allocation.latest.map(latestCard));
    latestSection.append(latestGrid);
    fragment.append(latestSection);
    allocation.sections.forEach((item) => fragment.append(section(item)));
    zone.replaceChildren(fragment);
    updateRest(allocation);
    verifyUnique();
    const expiry = A.nextExpiry(allocation);
    if (expiry) timer = window.setTimeout(refresh, Math.max(50, expiry.getTime() - Date.now() + 25));
  }
  const refresh = () => render().catch((error) => {
    zone.dataset.state = 'feed-error';
    zone.dataset.error = String(error && error.message || error).slice(0, 180);
    console.error('CurioMondo homepage v504:', error);
  });
  refresh();
})();
