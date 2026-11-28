/* CurioMondo v536 — la home statica resta se è aggiornata; se il feed ha notizie nuove, si ricostruisce da sola. */
(() => {
  'use strict';
  const existing = document.getElementById('cm-home-editorial-v504');
  let preferStatic = false;
  if (existing && existing.dataset.static === 'ready') {
    const mixed = Array.from(existing.querySelectorAll('.cm-topic-section')).some((section) => {
      const id = section.dataset.category || '';
      return Array.from(section.querySelectorAll('.cm-topic-card, .cm-topic-lead')).some((card) => card.dataset.category && card.dataset.category !== id);
    });
    if (!mixed) {
    window.CMHomeFlowChoices?.mountCarousel(existing.querySelector('.cm-featured-carousel'));
    preferStatic = true;
    }
  }
  const A = window.CMHomepageAllocation, choices=window.CMHomeFlowChoices;
  if (!A || !choices) return;
  const $ = (selector, root = document) => root.querySelector(selector);
  const zone = (preferStatic && existing) ? existing : document.createElement('div');
  if (!preferStatic || !existing) {
    zone.id = 'cm-home-editorial-v504';
    zone.className = 'cm-home-editorial';
    zone.setAttribute('aria-live', 'polite');
  }
  const legacyFeatured = $('.featured');
  const legacyLatestTitle = $('.auto-rail-label');
  const legacyLatest = $('.auto-rail');
  if (!legacyFeatured || !legacyLatestTitle || !legacyLatest) return;
  const mobileLayout = window.matchMedia('(max-width: 760px)');
  const placeZone = () => {
    const question = $('.cm-qday');
    if (question) question.after(zone);
    else legacyFeatured.before(zone);
  };
  if (!preferStatic || !existing) placeZone();
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
    image.sizes = eager ? '(max-width: 760px) calc(100vw - 46px), (max-width: 1280px) 51vw, 625px' : '(max-width: 760px) 80vw, (max-width: 1280px) 24vw, 280px';
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
  const largeCard = (entry, label, color, primary = false, categoryId = '') => {
    const article = el('article', 'cm-topic-lead' + (primary ? ' cm-topic-lead--primary' : ''));
    if (categoryId) article.dataset.category = categoryId;
    article.style.setProperty('--cm-category-color', color);
    const visual = picture(entry, primary);
    const body = el('div', 'cm-topic-lead__body');
    const labelNode = el('span', 'cm-topic-label', label);
    const featured = label === 'In primo piano';
    if (featured) {
      labelNode.classList.add('cm-topic-label--featured');
      article.append(labelNode);
    } else {
      body.append(labelNode);
    }
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
  const featuredCarousel = ({lead:entry,selection:stories,edition,today}) => {
    const block = el('section', 'cm-featured-carousel');
    block.setAttribute('aria-label', 'Notizie in primo piano');
    const lead = el('div', 'cm-flow-lead');
    lead.append(largeCard(entry, 'In primo piano', '#B91C1C', true));
    const selection = el('div', 'cm-flow-selection');
    const viewport = el('div', 'cm-featured-carousel__viewport');
    viewport.tabIndex = 0;
    const track = el('div', 'cm-featured-carousel__track');
    const dots = el('div', 'cm-featured-carousel__dots');
    const slides = stories.map((entry, index) => {
      const slide = el('div', 'cm-featured-carousel__slide');
      slide.dataset.index = String(index);
      const card=el('a','cm-flow-pick');card.href=entry.url;card.dataset.edition=edition;
      const visual=picture(entry,false);if(visual){visual.querySelector('img').sizes='(max-width: 760px) 155px, 130px';card.append(visual);}
      const copy=el('span','cm-flow-pick-copy');copy.append(el('small','',A.categoryFor(entry)?.label||entry.section||'Notizie'),el('strong','',entry.title));card.append(copy);slide.append(card);
      const dot = el('button', 'cm-featured-carousel__dot');
      dot.type = 'button';
      dot.setAttribute('aria-label', `Vai alla notizia ${index + 1}`);
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
    controls.append(previous, dots, next);
    const heading=el('div','cm-flow-select-head');heading.append(el('h2','cm-flow-selection-title','Da leggere'));
    if(edition!==today&&slides.length){const badge=el('time','',`Edizione del ${choices.dateLabel(edition)}`);badge.dateTime=edition;heading.append(badge);}
    if(slides.length)selection.append(heading,viewport,controls);
    block.append(lead,selection);
    return block;
  };
  const smallCard = (entry, category, eager = true) => {
    const link = el('a', 'cm-topic-card');
    link.dataset.category = category.id;
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
  const ultimaOra = (entries) => {
    const block = el('section', 'cm-wire');
    block.id = 'cm-ultima-ora';
    block.setAttribute('aria-label', 'Ultima ora');
    const details = el('details', 'cm-wire__details');
    const summary = el('summary', 'cm-wire__toggle');
    const live = el('span', 'cm-flow-more', 'Mostra tutte e 10');
    const less = el('span', 'cm-flow-less', 'Mostra meno');
    summary.setAttribute('aria-controls', 'cm-flow-wire-list');
    const chevron = el('span', 'cm-wire__chevron');
    chevron.setAttribute('aria-hidden', 'true');
    summary.append(live, less, chevron);
    const list = el('ol', 'cm-wire__list');
    list.id = 'cm-flow-wire-list';
    entries.slice(0, 10).forEach((entry, index) => {
      const item = el('li');
      const link = el('a', 'cm-wire__item');
      link.href = entry.url;
      if (index === 0) link.classList.add('is-latest');
      link.append(el('span', 'cm-wire__title', entry.title));
      item.append(link);
      list.append(item);
    });
    const more = el('a', 'cm-wire__more', 'Tutte le notizie');
    more.href = '/notizie/';
    details.append(summary);
    block.append(el('h2', 'cm-flow-wire-title', 'Ultima ora'), details, list, more);
    return block;
  };
  const section = ({ category, stories }) => {
    const block = el('section', 'cm-topic-section');
    block.dataset.category = category.id;
    // Ancoraggio per la barra delle sezioni in alto: cliccando "Sport" la
    // pagina scende fin qui invece di portare via dalla home.
    block.id = 'categoria-' + category.id;
    block.style.setProperty('--cm-category-color', category.color);
    const rail = el('div', 'cm-topic-section__rail');
    rail.dataset.forCategory = category.id;
    const label=category.id==='film-tv'?'Film e serie TV':category.label;
    rail.append(el('h2', 'cm-topic-section__title', label));
    const [lead,...own] = stories;
    const content=el('div','cm-flow-category-body');
    if(lead){
      const feature=el('a','cm-topic-card cm-flow-category-feature');feature.href=lead.url;feature.dataset.category=category.id;
      const visual=picture(lead,false);
      if(visual){visual.querySelector('img').sizes='(max-width: 760px) calc(100vw - 60px), (max-width: 1344px) calc(100vw - 94px), 1250px';feature.append(visual);}
      const copy=el('div','cm-flow-category-copy'), badge=el('span','cm-topic-label meta cm-flow-visually-hidden',label);
      badge.setAttribute('aria-hidden','true');
      copy.append(badge,el('h3','cm-flow-category-headline',lead.title));feature.append(copy);content.append(feature);
    }
    if (own.length) {
      const grid = el('div', 'cm-topic-grid');
      grid.append(...own.map(entry=>{
        const link=el('a','cm-topic-card cm-flow-title-row');link.href=entry.url;link.dataset.category=category.id;
        const badge=el('span','cm-topic-label meta cm-flow-visually-hidden',label);badge.setAttribute('aria-hidden','true');
        link.append(badge,el('h3','cm-topic-card__title',entry.title));
        return link;
      }));
      content.append(grid);
    }
    rail.append(content);
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
    const fragment = document.createDocumentFragment();
    const previousWire = document.getElementById('cm-ultima-ora');
    const wireWasOpen = !!previousWire?.querySelector('details[open]');
    const wireFocused = previousWire?.contains(document.activeElement);
    const focusedHref = wireFocused ? document.activeElement.getAttribute('href') : '';
    const now=new Date();
    const edition=choices.compose(A,items,now);
    const opening=el('div','cm-flow-opening');
    opening.append(el('h2','cm-flow-opening-title','In primo piano'));
    if(edition.lead)opening.append(featuredCarousel(edition));
    const wire=ultimaOra(edition.wire);
    wire.querySelector('details').open = wireWasOpen;
    opening.append(wire);
    fragment.append(opening);
    const services = document.querySelector('template#cm-flow-services');
    if (services) fragment.append(services.content.cloneNode(true));
    edition.sections.filter(it=>it.stories.length).forEach(item=>fragment.append(section(item)));
    // Preserva la rail Curiosità e approfondimenti (max 10 card statiche, non derivate dal feed notizie)
    const curiositaKeep = document.getElementById('categoria-curiosita');
    const curiositaNode = curiositaKeep ? curiositaKeep.cloneNode(true) : null;
    // Mantiene gli slot esistenti senza creare o cambiare i banner.
    const existingAds = [];
    zone.querySelectorAll('.cm-safe-ad').forEach((ad) => {
      const anchor = ad.previousElementSibling;
      if (anchor?.classList.contains('cm-flow-opening')) existingAds.push([opening, ad]);
      else if (anchor?.id) {
        const next = [...fragment.querySelectorAll('.cm-topic-section')].find((el) => el.id === anchor.id);
        if (next) existingAds.push([next, ad]);
      }
    });
    for (const [anchor, ad] of existingAds) anchor.after(ad);
    zone.replaceChildren(fragment);
    choices.mountCarousel(zone.querySelector('.cm-featured-carousel'));
    // Elimina solo l’eventuale duplicato legacy, mai la nuova lista.
    if (previousWire?.isConnected && !zone.contains(previousWire)) previousWire.remove();
    if (wireFocused) {
      const target = [...wire.querySelectorAll('a')].find((link) => link.getAttribute('href') === focusedHref);
      (target || wire.querySelector('summary')).focus({ preventScroll: true });
    }
    if (curiositaNode) {
      const after = zone.querySelector('#categoria-politica') || zone.querySelector('#categoria-sport') || zone.lastElementChild;
      if (after && after.nextSibling) after.after(curiositaNode);
      else if (after) after.after(curiositaNode);
      else zone.appendChild(curiositaNode);
    }
    hideLegacy();
    updateRest({rest:edition.remaining});
    verifyUnique();
    const expiry = A.nextExpiry({now,featured:edition.lead});
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
  const syncIfStale = async () => {
    try {
      const response = await fetch('/assets/data/home-feed-stamp.json', { cache: 'no-store', credentials: 'same-origin' });
      if (!response.ok) return;
      const stamp = await response.json();
      const bare = (value) => String(value || '').split('?')[0].split('#')[0].replace(/\.html$/, '').replace(/\/$/, '');
      const wanted = bare(stamp && stamp.newest);
      if (!wanted.startsWith('/notizie/')) return;
      const links = document.querySelectorAll('a[href]');
      for (const link of links) {
        if (bare(link.getAttribute('href')) === wanted) return;
      }
      start();
    } catch (error) {
      console.error('CurioMondo homepage sync:', error);
    }
  };
  const scheduleSync = () => {
    const run = () => { syncIfStale(); };
    if (window.requestIdleCallback) window.requestIdleCallback(run, { timeout: 2500 });
    else window.setTimeout(run, 1500);
  };
  // La home pubblicata resta com'è. Si controlla solo un file piccolo:
  // il feed intero si scarica soltanto se manca la notizia più recente.
  if (preferStatic) scheduleSync();
  else {
    window.addEventListener('pointerdown', start, { once: true, passive: true });
    window.addEventListener('keydown', start, { once: true });
    window.addEventListener('scroll', start, { once: true, passive: true });
  }
})();


/* v532 — pulsante Torna su, visibile dopo lo scroll in homepage */
(function initBackToTop() {
  if (typeof document === 'undefined') return;
  const make = () => {
    if (document.getElementById('cm-back-to-top')) return;
    const btn = document.createElement('button');
    btn.id = 'cm-back-to-top';
    btn.className = 'cm-back-to-top';
    btn.type = 'button';
    btn.setAttribute('aria-label', 'Torna all’inizio della pagina');
    btn.title = 'Torna su';
    btn.innerHTML = '↑';
    btn.addEventListener('click', () => {
      const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
      window.scrollTo({ top: 0, behavior: reduce ? 'auto' : 'smooth' });
    });
    document.body.appendChild(btn);
    const threshold = 420;
    const onScroll = () => {
      if (window.scrollY > threshold) btn.classList.add('is-visible');
      else btn.classList.remove('is-visible');
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', make);
  else make();
})();


