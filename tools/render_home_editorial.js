/* Scrive nel HTML la home che prima compariva solo dopo il feed.
   Così il primo disegno è già la versione nuova. */
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');
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

const LCP_SIZES = '(max-width: 700px) 250px, (max-width: 900px) calc(50vw - 32px), 380px';

const picture = (entry, eager) => {
  if (!entry.image) return '';
  const parts = String(entry.srcset || '').split(',').map((part) => part.trim()).filter(Boolean);
  const small = parts.find((part) => /\s480w$/.test(part));
  const src = eager && small ? small.split(/\s+/)[0] : entry.image;
  const extra = eager
    ? ' loading="eager" decoding="sync" fetchpriority="high"'
    : ' loading="lazy" decoding="async"';
  return `<picture><img src="${esc(src)}"${entry.srcset ? ` srcset="${esc(entry.srcset)}"` : ''} sizes="${LCP_SIZES}" alt="${esc(entry.imageAlt)}" width="${entry.imageWidth || 800}" height="${entry.imageHeight || 533}"${extra}></picture>`;
};

const updateFlag = (entry) => entry.updated
  ? '<span class="cm-update-flag">aggiornamento</span>'
  : '';

const time = (entry) => {
  const raw = entry.firstPublishedAt || entry.dateISO || '';
  return `<time datetime="${esc(raw)}">${esc(formatDate(entry))}</time>`;
};

const largeCard = (entry, label, color, primary, categoryId) => {
  const cls = 'cm-topic-lead' + (primary ? ' cm-topic-lead--primary' : '');
  const title = primary ? 'h1' : 'h3';
  const categoryAttr = categoryId ? ` data-category="${esc(categoryId)}"` : '';
  const featured = label === 'In primo piano';
  const labelMarkup = `<span class="cm-topic-label${featured ? ' cm-topic-label--featured' : ''}">${esc(label)}</span>`;
  return `<article class="${cls}"${categoryAttr} style="--cm-category-color:${esc(color)}">${featured ? labelMarkup : ''}<div class="cm-topic-lead__body">${featured ? '' : labelMarkup}${updateFlag(entry)}<${title} class="cm-topic-lead__title">${esc(entry.title)}</${title}>${entry.excerpt ? `<p class="cm-topic-lead__summary">${esc(entry.excerpt)}</p>` : ''}<div class="cm-topic-lead__footer"><a class="cm-topic-lead__cta" href="${esc(entry.url)}">Leggi l’articolo →</a>${time(entry)}</div></div>${picture(entry, primary)}</article>`;
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
    return `<li><a class="cm-wire__item" href="${esc(entry.url)}"><time class="cm-wire__time" datetime="${esc(raw)}">${esc(hourLabel(entry))}</time><span class="cm-wire__title">${updateFlag(entry)}${esc(entry.title)}</span></a></li>`;
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
    `<a class="cm-topic-card" data-category="${esc(category.id)}" href="${esc(entry.url)}" style="--cm-category-color:${esc(category.color)}"><div class="cm-topic-card__body"><span class="cm-topic-label meta">${esc(label)}</span>${updateFlag(entry)}<h3 class="cm-topic-card__title">${esc(entry.title)}</h3>${picture(entry, false)}${time(entry)}</div></a>`
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

const readRepoFile = (relativePath) => {
  const file = path.join(root, relativePath);
  if (fs.existsSync(file)) return fs.readFileSync(file, 'utf8');
  try {
    return execFileSync('git', ['show', `HEAD:${relativePath}`], { cwd: root, encoding: 'utf8', maxBuffer: 8_000_000 });
  } catch {
    return '';
  }
};

const curiositaRail = () => {
  const source = readRepoFile('approfondimenti/index.html');
  if (!source) return '';
  const found = [];
  const pattern = /<a class="card"[^>]*href="([^"]+)"[^>]*>[\s\S]*?<h2>([^<]+)<\/h2><p>([^<]*)<\/p>/g;
  const blocked = ['cinema', 'film', 'serie tv', 'serie televis', 'streaming', 'netflix', 'apple tv', 'prime video', 'disney+', 'nba', 'basket', 'raptors', 'clippers'];
  let match;
  let order = 0;
  while ((match = pattern.exec(source))) {
    const href = match[1].replace('../', '/');
    const title = match[2].replace(/\s+/g, ' ').trim();
    const excerpt = match[3].replace(/\s+/g, ' ').trim();
    const signal = (href + ' ' + title).toLocaleLowerCase('it');
    if (blocked.some((term) => signal.includes(term))) continue;
    const page = readRepoFile(href.replace(/^\//, ''));
    if (!page) continue;
    const image = (page.match(/property="og:image" content="([^"]+)"/) || page.match(/<img[^>]+src="(\/assets\/images\/[^"]+)"/) || [])[1];
    if (!image) continue;
    const src = image.replace(/^https?:\/\/[^/]+/, '');
    const sized = src.match(/^(.*)-1200\.webp$/);
    const srcset = sized
      ? [480, 800, 1200].filter((width) => fs.existsSync(path.join(root, sized[1].replace(/^\//, '') + '-' + width + '.webp')))
        .map((width) => `${sized[1]}-${width}.webp ${width}w`).join(', ')
      : '';
    const published = (page.match(/"datePublished"\s*:\s*"([^"]+)"/) || [])[1];
    const publishedAt = Date.parse(published || '');
    found.push({ href, title, excerpt, src, srcset, publishedAt: Number.isFinite(publishedAt) ? publishedAt : 0, order: order++ });
  }
  if (!found.length) return '';
  // Protocollo curiosità v1.1.2: fino a 10 guide più recenti in homepage rail.
  // A parità di orario resta davanti l'ultima inserita nell'indice.
  const cards = found.sort((a, b) => b.publishedAt - a.publishedAt || b.order - a.order).slice(0, 10).map((entry) => (
    `<a class="cm-topic-card" data-category="curiosita" href="${text(entry.href)}" style="--cm-category-color:#6333bd"><div class="cm-topic-card__body"><span class="cm-topic-label meta">Curiosità e approfondimenti</span><h3 class="cm-topic-card__title">${text(entry.title)}</h3><picture><img src="${text(entry.src)}"${entry.srcset ? ` srcset="${text(entry.srcset)}"` : ''} sizes="(max-width: 600px) 82vw, 320px" alt="${text(entry.title)}" width="800" height="533" loading="lazy" decoding="async"></picture><p class="cm-curiosita-card__excerpt">${text(entry.excerpt)}</p></div></a>`
  )).join('');
  return `<section class="cm-topic-section cm-curiosita-rail" data-category="curiosita" id="categoria-curiosita" data-cm-rail-max="10" style="--cm-category-color:#6333bd"><div class="cm-topic-section__rail" data-for-category="curiosita"><h2 class="cm-topic-section__title">Curiosità e approfondimenti</h2><div class="cm-topic-grid" aria-label="Carosello curiosità e approfondimenti">${cards}</div><a class="cm-topic-archive" href="/approfondimenti/">Tutti gli approfondimenti →</a></div></section>`;
};

const feed = JSON.parse(fs.readFileSync(path.join(root, 'assets/data/home-feed-v210.json'), 'utf8'));
const config = JSON.parse(fs.readFileSync(path.join(root, 'assets/data/homepage-config-v504.json'), 'utf8'));
const overrides = config.articles || {};
const CLUB = new Set('milan inter juventus napoli roma lazio atalanta fiorentina torino bologna genoa cagliari udinese monza lecce verona venezia parma como frosinone sassuolo cremonese empoli virtus olimpia besiktas zalgiris olympiacos panathinaikos barcellona barcelona'.split(' '));
const NAZIONALI = new Set('italia francia spagna belgio germania portogallo inghilterra turchia bielorussia'.split(' '));
const piatto = (value) => String(value || '').toLocaleLowerCase('it')
  .replace(/[àá]/g, 'a').replace(/[èé]/g, 'e').replace(/[ìí]/g, 'i').replace(/[òó]/g, 'o').replace(/[ùú]/g, 'u')
  .replace(/ş/g, 's').replace(/ğ/g, 'g').replace(/ı/g, 'i').replace(/ç/g, 'c').replace(/ö/g, 'o').replace(/ü/g, 'u');
const nomeSquadra = (token) => (token === 'juve' ? 'juventus' : token);
const partiteDi = (title) => {
  const n = piatto(title);
  const trovate = new Set();
  const trasporto = /\b(treni|linea|stazione|binari|circolazione|ferrovia|cassino)\b/.test(n);
  if (!trasporto) {
    const fixture = /([a-z]{3,})\s*[-–]\s*([a-z]{3,})/g;
    let match;
    while ((match = fixture.exec(n))) {
      const a = nomeSquadra(match[1]);
      const b = nomeSquadra(match[2]);
      if (a === b) continue;
      const donne = /\b(women|femminile|donne)\b/.test(n) ? '|donne' : '';
      const coppia = [a, b].sort().join('|') + donne;
      if (CLUB.has(a) && CLUB.has(b)) trovate.add(coppia);
      else if (NAZIONALI.has(a) && NAZIONALI.has(b) && /\b(nazionale|azzurr\w*|calcio|nations|san siro|biglietti|stadio)\b/.test(n)) trovate.add(coppia);
    }
    const clubs = [...CLUB].sort((a, b) => b.length - a.length).join('|');
    const legato = new RegExp(`\\b(${clubs})\\b.{0,80}?\\b(?:contro|dal|dalla|batte|sconfigge|supera|ospita|riceve)\\b.{0,40}?\\b(${clubs})\\b`, 'g');
    while ((match = legato.exec(n))) {
      const a = nomeSquadra(match[1]);
      const b = nomeSquadra(match[2]);
      if (a !== b) trovate.add([a, b].sort().join('|') + (/\b(women|femminile|donne)\b/.test(n) ? '|donne' : ''));
    }
  }
  if (/\bderby\b/.test(n) && !/\b(nba|dallas|basket|sole)\b/.test(n) && (/\bserie\b/.test(n) || /\b(milan|inter)\b/.test(n))) trovate.add('inter|milan' + (/\b(women|femminile|donne)\b/.test(n) ? '|donne' : ''));
  if (/\bnazionale\b/.test(n) && n.includes('francia')) trovate.add('francia|italia' + (/\b(women|femminile|donne)\b/.test(n) ? '|donne' : ''));
  if (/\bnazionale\b/.test(n) && n.includes('belgio')) trovate.add('belgio|italia' + (/\b(women|femminile|donne)\b/.test(n) ? '|donne' : ''));
  if (/\b(formula\s*1|\bf1\b)/.test(n)) {
    const piste = ['messico', 'austin', 'singapore', 'monza', 'baku', 'bahrain', 'sepang', 'suzuka', 'silverstone', 'imola', 'miami', 'qatar', 'ungheria', 'canada', 'australia', 'giappone', 'spa'];
    const place = piste.map((pista) => [n.indexOf(pista), pista]).filter(([index]) => index >= 0).sort((a, b) => a[0] - b[0])[0];
    if (place) trovate.add('gp|f1|' + place[1]);
  }
  if (n.includes('motogp')) {
    const piste = [['sepang', 'malesia'], ['malesia', 'malesia'], ['malaysia', 'malesia'], ['phillip', 'australia'], ['australia', 'australia'], ['mandalika', 'indonesia'], ['indonesia', 'indonesia'], ['motegi', 'giappone'], ['giappone', 'giappone'], ['spielberg', 'austria'], ['austria', 'austria']];
    const place = piste.map(([token, canon]) => [n.indexOf(token), canon]).filter(([index]) => index >= 0).sort((a, b) => a[0] - b[0])[0];
    if (place) trovate.add('gp|motogp|' + place[1]);
  }
  if (n.includes('errani') && n.includes('paolini')) {
    const tornei = ['tokyo', 'wuhan', 'pechino', 'parigi', 'wimbledon', 'finals'];
    const torneo = tornei.find((nome) => n.includes(nome));
    if (torneo) trovate.add('tennis|errani|paolini|' + torneo);
  }
  if (n.includes('cretti')) trovate.add('atleta|cretti');
  return trovate;
};
const eRisultato = (title) => {
  const n = piatto(title);
  const match = n.match(/\b(\d{1,3})\s*[-–]\s*(\d{1,3})\b/);
  if (!match) return false;
  const dopo = n.slice(match.index + match[0].length, match.index + match[0].length + 24);
  if (/gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre/.test(dopo)) return false;
  return Number(match[1]) <= 150 && Number(match[2]) <= 150;
};
const vociDistinte = (voci) => {
  const viste = new Set();
  const scelte = [];
  voci.forEach((item) => {
    const chiavi = partiteDi(item.title);
    if (!chiavi.size) { scelte.push(item); return; }
    if (eRisultato(item.title)) { scelte.push(item); chiavi.forEach((k) => viste.add(k)); return; }
    if ([...chiavi].some((k) => viste.has(k))) return;
    scelte.push(item);
    chiavi.forEach((k) => viste.add(k));
  });
  return scelte;
};
const items = vociDistinte((feed.items || []).map((entry) => ({ ...entry, ...(overrides[entry.url] || {}) })));
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
// Il gate editoriale richiede che il carosello parta sempre dalle tre
// pubblicazioni più recenti, senza che gli override di allocazione possano
// lasciare in testa articoli precedenti.
const newestFeatured = ranked.slice(0, 3);
const html = `<div class="cm-home-editorial" id="cm-home-editorial-v504" data-static="ready">${carousel(newestFeatured)}${ultimaOra(ranked)}${orderedSections}</div>`;

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
const hero = newestFeatured[0];
const placed = home.match(/<!-- cm-home-editorial:start -->[\s\S]*?<!-- cm-home-editorial:end -->/);
if (placed) {
  home = home.replace(placed[0], '');
  const qday = home.match(/<section class="cm-qday"[\s\S]*?<\/section>/);
  if (!qday) throw new Error('domanda del giorno non trovata');
  home = home.replace(qday[0], qday[0] + placed[0]);
}
if (hero && hero.image) {
  const parts = String(hero.srcset || '').split(',').map((part) => part.trim()).filter(Boolean);
  const small = parts.find((part) => /\s480w$/.test(part));
  const href = small ? small.split(/\s+/)[0] : hero.image;
  const preload = `<link rel="preload" as="image" href="${href}" imagesrcset="${hero.srcset || ''}" imagesizes="${LCP_SIZES}" fetchpriority="high">`;
  if (/<link rel="preload" as="image"[^>]*>/.test(home)) {
    let seen = false;
    home = home.replace(/<link rel="preload" as="image"[^>]*>/g, (tag) => {
      if (seen) return '';
      seen = true;
      return preload;
    });
  } else {
    home = home.replace('</head>', preload + '</head>');
  }
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
const UPDATE_FLAG_CSS = '<style id="cm-update-flag-css">.cm-update-flag{position:absolute;top:14px;right:14px;z-index:4;display:inline-flex;align-items:center;width:max-content;margin:0;padding:5px 10px;border-radius:999px;background:#B91C1C;color:#fff;font-size:.68rem;font-weight:800;letter-spacing:.09em;line-height:1;text-transform:uppercase;box-shadow:0 8px 18px rgba(120,15,15,.28)}.cm-topic-lead,.cm-topic-card,.cm-wire__item{position:relative}.cm-topic-lead .cm-update-flag{top:22px;right:28px}.cm-featured-carousel .cm-update-flag{top:24px;right:34px}.cm-wire__title:has(.cm-update-flag){display:block;padding-right:132px}.cm-wire__item .cm-update-flag{top:12px;right:8px}@media(max-width:700px){.cm-update-flag{top:10px;right:10px;font-size:.62rem;padding:4px 8px}.cm-topic-lead .cm-update-flag,.cm-featured-carousel .cm-update-flag{top:16px;right:16px}.cm-wire__title:has(.cm-update-flag){padding-right:112px}}</style>';
if (home.includes('id="cm-update-flag-css"')) {
  home = home.replace(/<style id="cm-update-flag-css">[\s\S]*?<\/style>/, UPDATE_FLAG_CSS);
} else {
  home = home.replace('</head>', UPDATE_FLAG_CSS + '</head>');
}
fs.writeFileSync(homePath, home);
console.log('home-editorial', hero && hero.title, allocation.sections.length);
