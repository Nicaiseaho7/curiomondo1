/* Scrive nel HTML la home che prima compariva solo dopo il feed.
   Così il primo disegno è già la versione nuova. */
const fs = require('fs');
const path = require('path');
const root = path.resolve(__dirname, '..');
const api = require(path.join(root, 'assets/js/home-allocation-v504.js'));

const esc = (value) => String(value || '')
  .replace(/&/g, '&')
  .replace(/</g, '<')
  .replace(/>/g, '>')
  .replace(/"/g, '"');

const formatDate = (entry) => {
  const date = api.firstPublished(entry);
  if (!date) return '';
  return new Intl.DateTimeFormat('it-IT', {
    timeZone: api.CONFIG.timeZone,
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  }).format(date);
};

const hourLabel = (entry) => {
  const date = api.firstPublished(entry);
  if (!date) return '';
  const zone = api.CONFIG.timeZone;
  const now = new Date();
  if (api.zonedDay(date, zone) === api.zonedDay(now, zone)) {
    const parts = new Intl.DateTimeFormat('it-IT', {
      timeZone: zone, hour: '2-digit', minute: '2-digit', hourCycle: 'h23'
    }).formatToParts(date);
    const pick = (type) => parts.find((part) => part.type === type)?.value || '';
    return pick('hour') + ':' + pick('minute');
  }
  return new Intl.DateTimeFormat('it-IT', { timeZone: zone, day: 'numeric', month: 'short' })
    .format(date).replace('.', '');
};

const picture = (entry, eager) => {
  if (!entry.image) return '';
  const extra = eager
    ? ' loading="eager" decoding="async" fetchpriority="high"'
    : ' loading="lazy" decoding="async"';
  return `<picture><img src="${esc(entry.image)}"${entry.srcset ? ` srcset="${esc(entry.srcset)}"` : ''} sizes="(max-width: 600px) calc(100vw - 28px), (max-width: 900px) calc(50vw - 32px), 380px" alt="${esc(entry.imageAlt)}" width="${entry.imageWidth || 800}" height="${entry.imageHeight || 533}"${extra}></picture>`;
};

const time = (entry) => {
  const raw = entry.firstPublishedAt || entry.dateISO || '';
  return `<time datetime="${esc(raw)}">${esc(formatDate(entry))}</time>`;
};

const largeCard = (entry, label, color, primary, categoryId) => {
  const cls = 'cm-topic-lead' + (primary ? ' cm-topic-lead--primary' : '');
  const title = primary ? 'h1' : 'h3';
  const categoryAttr = categoryId ? ` data-category="${esc(categoryId)}"` : '';
  return `<article class="${cls}"${categoryAttr} style="--cm-category-color:${esc(color)}"><div class="cm-topic-lead__body"><span class="cm-topic-label">${esc(label)}</span><${title} class="cm-topic-lead__title">${esc(entry.title)}</${title}>${entry.excerpt ? `<p class="cm-topic-lead__summary">${esc(entry.excerpt)}</p>` : ''}<div class="cm-topic-lead__footer"><a class="cm-topic-lead__cta" href="${esc(entry.url)}">Leggi l’articolo →</a>${time(entry)}</div></div>${picture(entry, primary)}</article>`;
};

const carousel = (entries) => {
  const slides = entries.map((entry, index) => (
    `<div class="cm-featured-carousel__slide" data-index="${index}">${largeCard(entry, 'In primo piano', '#B91C1C', index === 0)}</div>`
  )).join('');
  const dots = entries.map((_, index) => (
    `<button class="cm-featured-carousel__dot${index === 0 ? ' is-active' : ''}" type="button" aria-label="Vai alla notizia ${index + 1}"${index === 0 ? ' aria-current="true"' : ''}></button>`
  )).join('');
  return `<section class="cm-featured-carousel" aria-label="Notizie in primo piano"><div class="cm-featured-carousel__viewport" tabindex="0"><div class="cm-featured-carousel__track">${slides}</div></div><div class="cm-featured-carousel__controls"><button class="cm-featured-carousel__arrow" type="button" aria-label="Notizia precedente">←</button><div class="cm-featured-carousel__dots">${dots}</div><button class="cm-featured-carousel__arrow" type="button" aria-label="Notizia successiva">→</button></div></section>`;
};

const ultimaOra = (entries) => {
  const items = entries.slice(0, 10).map((entry) => {
    const raw = entry.firstPublishedAt || entry.dateISO || '';
    return `<li><a class="cm-wire__item" href="${esc(entry.url)}"><time class="cm-wire__time" datetime="${esc(raw)}">${esc(hourLabel(entry))}</time><span class="cm-wire__title">${esc(entry.title)}</span></a></li>`;
  }).join('');
  return `<section class="cm-wire" id="cm-ultima-ora" aria-label="Ultima ora"><details class="cm-wire__details"><summary class="cm-wire__toggle"><span class="cm-wire__kicker"><span class="cm-wire__dot" aria-hidden="true"></span><span>Ultima ora</span></span><span class="cm-wire__chevron" aria-hidden="true"></span></summary></details><ol class="cm-wire__list">${items}</ol><a class="cm-wire__more" href="/notizie/">Tutte le notizie</a></section>`;
};

const section = ({ category, lead, cards }) => {
  const label = category.id === 'film-tv' ? 'Film e serie TV' : category.label;
  const belongs = (entry) => api.categoryFor(entry)?.id === category.id;
  if (!belongs(lead)) return '';
  const own = cards.filter(belongs);
  if (!own.length) return '';
  const small = own.map((entry) => (
    `<a class="cm-topic-card" data-category="${esc(category.id)}" href="${esc(entry.url)}" style="--cm-category-color:${esc(category.color)}"><div class="cm-topic-card__body"><span class="cm-topic-label meta">${esc(label)}</span><h3 class="cm-topic-card__title">${esc(entry.title)}</h3>${picture(entry, false)}${time(entry)}</div></a>`
  )).join('');
  const archive = category.archive
    ? `<a class="cm-topic-archive" href="${esc(category.archive)}">${esc(category.id === 'meteo' ? 'Tutte le notizie Meteo →' : `Tutte le notizie di ${label} →`)}</a>`
    : '';
  return `<section class="cm-topic-section" data-category="${esc(category.id)}" id="categoria-${esc(category.id)}" style="--cm-category-color:${esc(category.color)}">${largeCard(lead, label, category.color, false, category.id)}<div class="cm-topic-section__rail" data-for-category="${esc(category.id)}"><h2 class="cm-topic-section__title">${esc(label)}</h2><div class="cm-topic-grid">${small}</div>${archive}</div></section>`;
};

const text = (value) => String(value || '')
  .replace(/&/g, '&')
  .replace(/</g, '<')
  .replace(/>/g, '>')
  .replace(/"/g, '"');

const curiositaRail = () => {
  const indexPath = path.join(root, 'approfondimenti/index.html');
  if (!fs.existsSync(indexPath)) return '';
  const source = fs.readFileSync(indexPath, 'utf8');
  const found = [];
  const pattern = /<a class="card"[^>]*href="([^"]+)"[^>]*>[\s\S]*?<h2>([^<]+)<\/h2><p>([^<]*)<\/p>/g;
  const blocked = ['cinema', 'film', 'serie tv', 'serie televis', 'streaming', 'netflix', 'apple tv', 'prime video', 'disney+', 'nba', 'basket', 'raptors', 'clippers'];
  let match;
  while ((match = pattern.exec(source)) && found.length < 10) {
    const href = match[1].replace('../', '/');
    const title = match[2].replace(/\s+/g, ' ').trim();
    const excerpt = match[3].replace(/\s+/g, ' ').trim();
    const signal = (href + ' ' + title).toLocaleLowerCase('it');
    if (blocked.some((term) => signal.includes(term))) continue;
    const file = path.join(root, href.replace(/^\//, ''));
    if (!fs.existsSync(file)) continue;
    const page = fs.readFileSync(file, 'utf8');
    const image = (page.match(/property="og:image" content="([^"]+)"/) || page.match(/<img[^>]+src="(\/assets\/images\/[^"]+)"/) || [])[1];
    if (!image) continue;
    const src = image.replace(/^https?:\/\/[^/]+/, '');
    const sized = src.match(/^(.*)-1200\.webp$/);
    const srcset = sized
      ? [480, 800, 1200].filter((width) => fs.existsSync(path.join(root, sized[1].replace(/^\//, '') + '-' + width + '.webp')))
        .map((width) => `${sized[1]}-${width}.webp ${width}w`).join(', ')
      : '';
    found.push({ href, title, excerpt, src, srcset });
  }
  if (!found.length) return '';
  const cards = found.map((entry) => (
    `<a class="cm-topic-card" data-category="curiosita" href="${text(entry.href)}" style="--cm-category-color:#6333bd"><div class="cm-topic-card__body"><span class="cm-topic-label meta">Curiosità e approfondimenti</span><h3 class="cm-topic-card__title">${text(entry.title)}</h3><picture><img src="${text(entry.src)}"${entry.srcset ? ` srcset="${text(entry.srcset)}"` : ''} sizes="(max-width: 600px) 82vw, 320px" alt="${text(entry.title)}" width="800" height="533" loading="lazy" decoding="async"></picture><p class="cm-curiosita-card__excerpt">${text(entry.excerpt)}</p></div></a>`
  )).join('');
  return `<section class="cm-topic-section cm-curiosita-rail" data-category="curiosita" id="categoria-curiosita" style="--cm-category-color:#6333bd"><div class="cm-topic-section__rail" data-for-category="curiosita"><h2 class="cm-topic-section__title">Curiosità e approfondimenti</h2><div class="cm-topic-grid">${cards}</div><a class="cm-topic-archive" href="/approfondimenti/">Tutte le curiosità e gli approfondimenti →</a></div></section>`;
};

const feed = JSON.parse(fs.readFileSync(path.join(root, 'assets/data/home-feed-v210.json'), 'utf8'));
const config = JSON.parse(fs.readFileSync(path.join(root, 'assets/data/homepage-config-v504.json'), 'utf8'));
const overrides = config.articles || {};
const items = (feed.items || []).map((entry) => ({ ...entry, ...(overrides[entry.url] || {}) }));
const allocation = api.allocate(items, { now: new Date(), latestCapacity: 0, smallCardsPerCategory: 11 });
const ranked = items.slice().sort((a, b) => {
  const left = api.firstPublished(b);
  const right = api.firstPublished(a);
  return (left ? left.getTime() : 0) - (right ? right.getTime() : 0);
});
const sectionsHtml = allocation.sections.map(section).join('');
const curiosita = curiositaRail();
const orderedSections = sectionsHtml.includes('id="categoria-politica"')
  ? sectionsHtml.replace(/(<section class="cm-topic-section" data-category="politica"[\s\S]*?<\/section>)/, '$1' + curiosita)
  : sectionsHtml + curiosita;
const html = `<div class="cm-home-editorial" id="cm-home-editorial-v504" data-static="ready">${carousel(allocation.featuredItems)}${ultimaOra(ranked)}${orderedSections}</div>`;

const homePath = path.join(root, 'index.html');
let home = fs.readFileSync(homePath, 'utf8');
const block = `<!-- cm-home-editorial:start -->${html}<!-- cm-home-editorial:end -->`;
if (home.includes('<!-- cm-home-editorial:start -->')) {
  home = home.replace(/<!-- cm-home-editorial:start -->[\s\S]*?<!-- cm-home-editorial:end -->/, block);
} else {
  const mark = '<article class="featured">';
  if (!home.includes(mark)) throw new Error('card in evidenza non trovata');
  home = home.replace(mark, block + mark);
}
const hero = allocation.featuredItems[0];
const placed = home.match(/<!-- cm-home-editorial:start -->[\s\S]*?<!-- cm-home-editorial:end -->/);
if (placed) {
  home = home.replace(placed[0], '');
  const qday = home.match(/<section class="cm-qday"[\s\S]*?<\/section>/);
  if (!qday) throw new Error('domanda del giorno non trovata');
  home = home.replace(qday[0], qday[0] + placed[0]);
}
if (hero && hero.image) {
  home = home.replace(
    /<link rel="preload" as="image" href="[^"]*" imagesrcset="[^"]*" imagesizes="[^"]*" fetchpriority="high">/,
    `<link rel="preload" as="image" href="${hero.image}" imagesrcset="${hero.srcset || ''}" imagesizes="(max-width: 600px) calc(100vw - 28px), 380px" fetchpriority="high">`
  );
}
let wireCount = 0;
home = home.replace(/<section class="cm-wire" id="cm-ultima-ora"/g, (match) => {
  wireCount += 1;
  return wireCount === 1
    ? match
    : '<section class="cm-wire cm-wire--legacy" id="cm-ultima-ora-legacy"';
});
const tickerItems = ranked.filter((entry) => entry.url && entry.title).slice(0, 10);
const tickerLink = (entry, hidden) => `<a class="ticker-news" href="${esc(entry.url)}"${hidden ? ' tabindex="-1"' : ''}>${esc(entry.title)}</a>`;
const tickerNav = `<nav aria-label="Ultime notizie in diretta" class="ticker-track">${tickerItems.map((entry) => tickerLink(entry, false)).join('')}</nav>`;
const tickerCopy = `<div aria-hidden="true" class="ticker-track" inert="">${tickerItems.map((entry) => tickerLink(entry, true)).join('')}</div>`;
if (!home.includes('class="ticker-track"')) throw new Error('ticker assente');
home = home.replace(/<nav aria-label="Ultime notizie in diretta" class="ticker-track">[\s\S]*?<\/nav>/, tickerNav);
home = home.replace(/<div aria-hidden="true" class="ticker-track" inert="">[\s\S]*?<\/div>/, tickerCopy);
fs.writeFileSync(homePath, home);
console.log('home-editorial', hero && hero.title, allocation.sections.length);
