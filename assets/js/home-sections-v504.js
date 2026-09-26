/* CurioMondo v529 — la home nuova è già nel HTML. Nessun salto dopo il caricamento. */
(() => {
  'use strict';
  const existing = document.getElementById('cm-home-editorial-v504');
  if (existing && existing.dataset.static === 'ready') {
    const viewport = existing.querySelector('.cm-featured-carousel__viewport');
    const slides = Array.from(existing.querySelectorAll('.cm-featured-carousel__slide'));
    const dots = Array.from(existing.querySelectorAll('.cm-featured-carousel__dot'));
    const arrows = existing.querySelectorAll('.cm-featured-carousel__arrow');
    if (viewport && slides.length) {
      const currentIndex = () => Math.max(0, Math.min(slides.length - 1, Math.round(viewport.scrollLeft / Math.max(1, viewport.clientWidth))));
      const update = () => dots.forEach((dot, index) => {
        const active = index === currentIndex();
        dot.classList.toggle('is-active', active);
        dot.setAttribute('aria-current', active ? 'true' : 'false');
      });
      const go = (delta) => viewport.scrollTo({ left: ((currentIndex() + delta + slides.length) % slides.length) * viewport.clientWidth, behavior: 'smooth' });
      if (arrows[0]) arrows[0].addEventListener('click', () => go(-1));
      if (arrows[1]) arrows[1].addEventListener('click', () => go(1));
      dots.forEach((dot, index) => dot.addEventListener('click', () => slides[index].scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' })));
      viewport.addEventListener('scroll', update, { passive: true });
    }
    return;
  }
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
  const mobileLayout = window.matchMedia('(max-width: 760px)');
  const placeZone = () => {
    const question = $('.cm-qday');
    if (mobileLayout.matches && question) question.after(zone);
    else legacyFeatured.before(zone);
  };
  placeZone();
  const hideLegacy = () => [legacyFeatured, legacyLatestTitle, legacyLatest].forEach((node) => {
    node.hidden = true;
    node.setAttribute('aria-hidden', 'true');
  });

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
    image.dataset.cmPersistentImage = 'true';
    if (eager) image.fetchPriority = 'high';
    let retries = 0;
    image.addEventListener('load', () => {
      wrap.classList.remove('cm-image-frame--error');
      image.classList.add('cm-image-loaded');
    });
    image.addEventListener('error', () => {
      if (retries++ === 0) {
        image.removeAttribute('srcset');
        image.removeAttribute('sizes');
        const separator = entry.image.includes('?') ? '&' : '?';
        image.src = entry.image + separator + 'cm_img_retry=1';
        return;
      }
      wrap.classList.add('cm-image-frame--error');
    });
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
    const visual = picture(entry, true);
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
  const featuredCarousel = (entries) => {
    const block = el('section', 'cm-featured-carousel');
    block.setAttribute('aria-label', 'Notizie in primo piano');
    const viewport = el('div', 'cm-featured-carousel__viewport');
    viewport.tabIndex = 0;
    const track = el('div', 'cm-featured-carousel__track');
    const dots = el('div', 'cm-featured-carousel__dots');
    const slides = entries.map((entry, index) => {
      const slide = el('div', 'cm-featured-carousel__slide');
      slide.dataset.index = String(index);
      slide.append(largeCard(entry, 'In primo piano', '#B91C1C', index === 0));
      const dot = el('button', 'cm-featured-carousel__dot');
      dot.type = 'button';
      dot.setAttribute('aria-label', `Vai alla notizia ${index + 1}`);
      dot.addEventListener('click', () => slide.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' }));
      dots.append(dot);
      return slide;
    });
    track.append(...slides);
    viewport.append(track);
    const controls = el('div', 'cm-featured-carousel__controls');
    const previous = el('button', 'cm-featured-carousel__arrow', '←');
    const next = el('button', 'cm-featured-carousel__arrow', '→');
    previous.type = next.type = 'button';
    previous.setAttribute('aria-label', 'Notizia precedente');
    next.setAttribute('aria-label', 'Notizia successiva');
    const currentIndex = () => Math.max(0, Math.min(slides.length - 1, Math.round(viewport.scrollLeft / Math.max(1, viewport.clientWidth))));
    const update = () => Array.from(dots.children).forEach((dot, index) => {
      const active = index === currentIndex();
      dot.classList.toggle('is-active', active);
      dot.setAttribute('aria-current', active ? 'true' : 'false');
    });
    const go = (delta) => viewport.scrollTo({ left: (currentIndex() + delta + slides.length) % slides.length * viewport.clientWidth, behavior: 'smooth' });
    previous.addEventListener('click', () => go(-1));
    next.addEventListener('click', () => go(1));
    viewport.addEventListener('scroll', update, { passive: true });
    viewport.addEventListener('keydown', (event) => {
      if (event.key === 'ArrowLeft') { event.preventDefault(); go(-1); }
      if (event.key === 'ArrowRight') { event.preventDefault(); go(1); }
    });
    controls.append(previous, dots, next);
    block.append(viewport, controls);
    requestAnimationFrame(update);
    return block;
  };
  const smallCard = (entry, category, eager = true) => {
    const link = el('a', 'cm-topic-card');
    link.href = entry.url;
    link.style.setProperty('--cm-category-color', category.color);
    const body = el('div', 'cm-topic-card__body');
    body.append(el('span', 'cm-topic-label', category.label));
    body.append(el('h3', 'cm-topic-card__title', entry.title));
    const visual = picture(entry, eager);
    if (visual) body.append(visual);
    body.append(time(entry));
    link.append(body);
    return link;
  };
  const hourLabel = (entry) => {
    const date = A.firstPublished(entry);
    if (!date) return '';
    const zone = A.CONFIG.timeZone;
    if (A.zonedDay(date, zone) === A.zonedDay(new Date(), zone)) {
      const parts = new Intl.DateTimeFormat('it-IT', { timeZone: zone, hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).formatToParts(date);
      const pick = (type) => parts.find((part) => part.type === type)?.value || '';
      return pick('hour') + ':' + pick('minute');
    }
    return new Intl.DateTimeFormat('it-IT', { timeZone: zone, day: 'numeric', month: 'short' }).format(date).replace('.', '');
  };
  const ultimaOra = (entries) => {
    const block = el('section', 'cm-wire');
    block.id = 'cm-ultima-ora';
    block.setAttribute('aria-label', 'Ultima ora');
    const details = el('details', 'cm-wire__details');
    const summary = el('summary', 'cm-wire__toggle');
    const kicker = el('span', 'cm-wire__kicker');
    const dot = el('span', 'cm-wire__dot');
    dot.setAttribute('aria-hidden', 'true');
    kicker.append(dot, el('span', '', 'Ultima ora'));
    const peek = el('span', 'cm-wire__peek', entries[0] ? entries[0].title : '');
    const chevron = el('span', 'cm-wire__chevron');
    chevron.setAttribute('aria-hidden', 'true');
    summary.append(kicker, peek, chevron);
    const panel = el('div', 'cm-wire__panel');
    const list = el('ol', 'cm-wire__list');
    entries.slice(0, 10).forEach((entry) => {
      const item = el('li');
      const link = el('a', 'cm-wire__item');
      link.href = entry.url;
      const stamp = el('time', 'cm-wire__time', hourLabel(entry));
      stamp.dateTime = entry.firstPublishedAt || entry.dateISO || '';
      link.append(stamp, el('span', 'cm-wire__title', entry.title));
      item.append(link);
      list.append(item);
    });
    const more = el('a', 'cm-wire__more', 'Tutte le notizie');
    more.href = '/notizie/';
    panel.append(list, more);
    details.append(summary, panel);
    block.append(details);
    return block;
  };
  const section = ({ category, lead, cards }) => {
    const block = el('section', 'cm-topic-section');
    block.dataset.category = category.id;
    // Ancoraggio per la barra delle sezioni in alto: cliccando "Sport" la
    // pagina scende fin qui invece di portare via dalla home.
    block.id = 'categoria-' + category.id;
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
      const card = smallCard(entry, category, false);
      card.classList.add('card');
      return card;
    }));
    cards.dataset.initialCount = String(Math.min(limit, allocation.rest.length));
    const loadMore = $('#loadMoreNews');
    if (loadMore) loadMore.hidden = true;
  }
  function verifyUnique() {
    const keys = Array.from(document.querySelectorAll('#cm-home-editorial-v504 a[href^="/notizie/"], #cards a[href^="/notizie/"]'))
      .filter((link) => !link.closest('#cm-ultima-ora'))
      .map((link) => A.canonicalKey({ url: link.getAttribute('href') })).filter(Boolean);
    if (keys.length !== new Set(keys).size) throw new Error('Homepage CurioMondo: identificativi duplicati');
    zone.dataset.cardCount = String(keys.length);
    zone.dataset.uniqueCardCount = String(new Set(keys).size);
  }
  async function render() {
    const current = ++generation;
    clearTimeout(timer);
    const [response, configResponse] = await Promise.all([
      fetch('/assets/data/home-feed-v210.json', { credentials: 'same-origin' }),
      fetch('/assets/data/homepage-config-v504.json', { credentials: 'same-origin' })
    ]);
    if (!response.ok || !configResponse.ok) throw new Error('Feed homepage non disponibile');
    const [payload, editorialConfig] = await Promise.all([response.json(), configResponse.json()]);
    const overrides = editorialConfig && editorialConfig.articles || {};
    const items = (Array.isArray(payload.items) ? payload.items : []).map((entry) => ({ ...entry, ...(overrides[entry.url] || {}) }));
    if (current !== generation) return;
    const allocation = A.allocate(items, {
      now: new Date(),
      latestCapacity: mobileLayout.matches ? 0 : A.CONFIG.latestCapacity,
      smallCardsPerCategory: 11
    });
    const fragment = document.createDocumentFragment();
    if (allocation.featuredItems && allocation.featuredItems.length) fragment.append(featuredCarousel(allocation.featuredItems));
    const previousWire = document.getElementById('cm-ultima-ora');
    if (previousWire) previousWire.remove();
    const ranked = items.slice().sort((a, b) => {
      const left = A.firstPublished(b);
      const right = A.firstPublished(a);
      return (left ? left.getTime() : 0) - (right ? right.getTime() : 0);
    });
    fragment.append(ultimaOra(ranked));
    allocation.sections.forEach((item) => fragment.append(section(item)));
    zone.replaceChildren(fragment);
    hideLegacy();
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
  mobileLayout.addEventListener?.('change', () => {
    placeZone();
    if (zone.dataset.started) refresh();
  });
  const start = () => {
    if (zone.dataset.started) return;
    zone.dataset.started = '1';
    refresh();
  };
  window.addEventListener('pointerdown', start, { once: true, passive: true });
  window.addEventListener('keydown', start, { once: true });
  window.addEventListener('scroll', start, { once: true, passive: true });
})();
