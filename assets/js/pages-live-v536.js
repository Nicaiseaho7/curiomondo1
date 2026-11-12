/* Aggiorna archivio e categorie dal feed, senza rifare a mano l'HTML. */
(() => {
  'use strict';
  const cats = [
    { id: 'sport', aliases: ['sport', 'calcio', 'basket', 'tennis', 'motogp'] },
    { id: 'politica', aliases: ['politica', 'governo', 'parlamento', 'elezioni'] },
    { id: 'film-tv', aliases: ['film e serie tv', 'film', 'cinema', 'serie tv', 'streaming'] },
    { id: 'meteo', aliases: ['meteo', 'previsioni', 'maltempo'] },
    { id: 'cronaca', aliases: ['cronaca', 'giustizia', 'sicurezza'] },
    { id: 'tecnologia', aliases: ['tecnologia', 'digitale', 'intelligenza artificiale'] },
    { id: 'economia', aliases: ['economia', 'finanza', 'lavoro'] },
    { id: 'scienza', aliases: ['scienza', 'ricerca', 'spazio', 'salute'] },
    { id: 'ambiente', aliases: ['ambiente', 'clima', 'natura'] },
    { id: 'cultura', aliases: ['cultura', 'spettacolo'] },
    { id: 'italia', aliases: ['italia'] },
    { id: 'mondo', aliases: ['mondo'] }
  ];
  const norm = (value) => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const categoryId = (section) => {
    const text = norm(section);
    const parts = text.split(/\s*[\/.·]\s*/);
    const found = cats.find((cat) => cat.id === text || parts.includes(cat.id) || cat.aliases.some((alias) => parts.includes(alias) || text.includes(alias)));
    return found ? found.id : '';
  };
  const esc = (value) => String(value || '').replace(/[&<>"']/g, (ch) => ({ '&': '&', '<': '<', '>': '>', '"': '"', "'": '&#39;' }[ch]));
  const thumb = (image) => String(image || '').replace(/-800\.webp$/, '-480.webp');

  const list = document.querySelector('.category-list');
  const archive = !list && location.pathname.replace(/\/$/, '') === '/notizie'
    ? document.querySelector('main ul')
    : null;
  if (!list && !archive) return;

  const page = location.pathname.replace(/\/$/, '').split('/').pop();
  const pageId = page === 'film-serie-tv' ? 'film-tv' : page;

  fetch('/assets/data/home-feed-v210.json', { cache: 'no-store', credentials: 'same-origin' })
    .then((response) => response.ok ? response.json() : null)
    .then((payload) => {
      const items = (payload && payload.items || []).filter((entry) => entry && entry.url && entry.title);
      items.sort((a, b) => String(b.dateISO || '').localeCompare(String(a.dateISO || '')));
      if (list) {
        const have = new Set(Array.from(list.querySelectorAll('a[href]')).map((link) => link.getAttribute('href')));
        const fresh = items.filter((entry) => categoryId(entry.section) === pageId && !have.has(entry.url));
        fresh.slice().reverse().forEach((entry) => {
          const li = document.createElement('li');
          li.innerHTML = '<a href="' + esc(entry.url) + '"><span class="category-card-thumb"><img src="' + esc(thumb(entry.image)) + '" alt="" width="112" height="75" loading="lazy" decoding="async"></span><span class="category-card-copy"><small>' + esc(entry.section || '') + '</small><strong>' + esc(entry.title) + '</strong><span>' + esc(entry.excerpt || '') + '</span></span><span class="category-card-arrow" aria-hidden="true">→</span></a>';
          list.insertBefore(li, list.firstChild);
        });
        const count = document.querySelector('.category-hero-copy strong');
        if (count && fresh.length) {
          const current = Number((count.textContent.match(/\d+/) || ['0'])[0]);
          count.textContent = (current + fresh.length) + ' articoli';
        }
        return;
      }
      const have = new Set(Array.from(archive.querySelectorAll('a[href]')).map((link) => link.getAttribute('href')));
      items.filter((entry) => entry.url.startsWith('/notizie/') && !have.has(entry.url)).slice().reverse().forEach((entry) => {
        const li = document.createElement('li');
        li.innerHTML = '<a href="' + esc(entry.url) + '"><strong>' + esc(entry.title) + '</strong><span>' + esc(String(entry.dateISO || '').slice(0, 10)) + '</span></a>';
        archive.insertBefore(li, archive.firstChild);
      });
    })
    .catch(() => {});
})();
