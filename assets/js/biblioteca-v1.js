(function () {
  const BOOKMARK_KEY = 'cm_biblioteca_resume_v1';
  const PENDING_KEY = 'cm_biblioteca_pending_resume_v1';
  const reader = document.querySelector('[data-cb-reader]');

  function updateTheme() {
    try {
      document.documentElement.classList.toggle('cm-dark', localStorage.getItem('cm_theme') === 'dark');
    } catch (error) {}
  }

  updateTheme();
  window.addEventListener('storage', updateTheme);
  document.querySelectorAll('[data-cb-theme]').forEach((button) => {
    button.addEventListener('click', () => {
      const dark = !document.documentElement.classList.contains('cm-dark');
      document.documentElement.classList.toggle('cm-dark', dark);
      try {
        localStorage.setItem('cm_theme', dark ? 'dark' : 'light');
      } catch (error) {}
    });
  });

  if (!reader) return;

  const progress = document.querySelector('.cb-progress');
  const book = reader.dataset.book || '';
  const chapterUrl = reader.dataset.chapterUrl || window.location.pathname;
  const chapterLabel = reader.dataset.chapterLabel || 'questa sezione';
  const tocLinks = Array.from(document.querySelectorAll('[data-cb-toc] a[href]'));
  const sections = Array.from(document.querySelectorAll('.cb-chapter h2, .cb-chapter h3'));

  reader.querySelectorAll('.cb-chapter img').forEach((image) => {
    image.loading = 'lazy';
    image.decoding = 'async';
  });
  reader.querySelectorAll('.cb-chapter iframe').forEach((frame) => {
    frame.loading = 'lazy';
  });
  reader.querySelectorAll('.cb-chapter table').forEach((table) => {
    table.classList.add('cb-lazy-table');
  });

  function normalPath(path) {
    return (path || '/').replace(/\/+$/, '') || '/';
  }

  function readBookmarks() {
    try {
      const stored = JSON.parse(localStorage.getItem(BOOKMARK_KEY) || '{}');
      // Compatibilità con il primo formato, che conteneva un solo segnalibro.
      return stored && stored.book ? { [stored.book]: stored } : stored || {};
    } catch (error) {
      return {};
    }
  }

  function saveBookmark(top) {
    if (!book) return;
    try {
      const bookmarks = readBookmarks();
      bookmarks[book] = {
        book,
        url: chapterUrl,
        label: chapterLabel,
        top: Math.max(0, Math.round(top)),
        updated: Date.now(),
      };
      localStorage.setItem(BOOKMARK_KEY, JSON.stringify(bookmarks));
    } catch (error) {}
  }

  function refresh(save) {
    const documentElement = document.documentElement;
    const maximum = documentElement.scrollHeight - window.innerHeight;
    const percentage = maximum > 0 ? Math.max(0, Math.min(100, (window.scrollY / maximum) * 100)) : 0;
    if (progress) progress.style.width = percentage + '%';
    if (save) saveBookmark(window.scrollY);

    let active = '';
    sections.forEach((heading) => {
      if (heading.getBoundingClientRect().top < window.innerHeight * 0.38) active = heading.id;
    });
    tocLinks.forEach((link) => {
      const hash = '#' + active;
      const href = link.getAttribute('href') || '';
      link.classList.toggle('active', Boolean(active) && (href === hash || href.endsWith(hash)));
    });
  }

  const saved = readBookmarks()[book];
  let pending = null;
  try {
    pending = JSON.parse(sessionStorage.getItem(PENDING_KEY) || 'null');
    if (pending && pending.book === book && normalPath(pending.url) === normalPath(chapterUrl)) {
      sessionStorage.removeItem(PENDING_KEY);
      window.setTimeout(() => window.scrollTo({ top: pending.top || 0, behavior: 'auto' }), 0);
    }
  } catch (error) {}

  if (saved && saved.book === book && saved.top > 64 && !pending) {
    const notice = document.querySelector('[data-cb-resume]');
    if (notice) {
      notice.hidden = false;
      const text = notice.querySelector('[data-cb-resume-text]');
      if (text) text.textContent = 'Vuoi riprendere da ' + (saved.label || 'dove ti eri fermato') + '?';
      const button = notice.querySelector('button');
      if (button) {
        button.addEventListener('click', () => {
          if (normalPath(saved.url) === normalPath(chapterUrl)) {
            window.scrollTo({ top: saved.top || 0, behavior: 'smooth' });
          } else {
            try {
              sessionStorage.setItem(PENDING_KEY, JSON.stringify(saved));
            } catch (error) {}
            window.location.href = (saved.url || chapterUrl) + '#riprendi';
          }
          notice.hidden = true;
        });
      }
    }
  }

  window.addEventListener('scroll', () => refresh(true), { passive: true });
  window.addEventListener('pagehide', () => saveBookmark(window.scrollY));
  refresh(false);

  document.querySelectorAll('[data-cb-toc-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      const open = reader.classList.toggle('toc-open');
      button.setAttribute('aria-expanded', String(open));
    });
  });

  const resultBox = document.querySelector('[data-cb-toc-results]');
  const indexUrl = reader.dataset.cbSearchIndex;
  let searchEntries = null;

  function makeResult(entry) {
    const link = document.createElement('a');
    link.className = 'cb-search-result';
    link.href = entry.href || '#';
    const title = document.createElement('strong');
    title.textContent = entry.title || 'Risultato nel manuale';
    const excerpt = document.createElement('span');
    const text = entry.text || '';
    excerpt.textContent = text.length > 130 ? text.slice(0, 130).trim() + '…' : text;
    link.append(title, excerpt);
    return link;
  }

  async function searchEntireBook(query) {
    if (!resultBox) return;
    resultBox.replaceChildren();
    if (!query || !indexUrl) return;
    try {
      if (!searchEntries) {
        const response = await fetch(indexUrl, { credentials: 'same-origin' });
        if (!response.ok) throw new Error('Indice non disponibile');
        const payload = await response.json();
        searchEntries = Array.isArray(payload.entries) ? payload.entries : [];
      }
      const matches = searchEntries.filter((entry) => {
        const haystack = ((entry.title || '') + ' ' + (entry.text || '')).toLocaleLowerCase('it');
        return haystack.includes(query);
      }).slice(0, 8);
      if (!matches.length) {
        const empty = document.createElement('p');
        empty.textContent = 'Nessun risultato nel manuale.';
        resultBox.append(empty);
        return;
      }
      const label = document.createElement('p');
      label.textContent = 'Risultati nel libro';
      resultBox.append(label, ...matches.map(makeResult));
    } catch (error) {
      const unavailable = document.createElement('p');
      unavailable.textContent = 'La ricerca completa non è disponibile in questo momento.';
      resultBox.append(unavailable);
    }
  }

  document.querySelectorAll('[data-cb-toc-search]').forEach((input) => {
    input.addEventListener('input', () => {
      const query = input.value.trim().toLocaleLowerCase('it');
      tocLinks.forEach((link) => {
        link.style.display = !query || link.textContent.toLocaleLowerCase('it').includes(query) ? '' : 'none';
      });
      searchEntireBook(query);
    });
  });
})();

(function () {
  const escapeHTML = (value) => String(value || '').replace(/[&<>'"]/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  })[character]);

  window.CurioBiblioteca = {
    widget({ href, title, description }) {
      return '<aside class="cb-widget"><small>Approfondisci in Biblioteca</small><h3>'
        + escapeHTML(title) + '</h3><p>' + escapeHTML(description) + '</p><a href="'
        + escapeHTML(href || '/biblioteca/') + '">Apri il manuale →</a></aside>';
    },
    mountWidgets() {
      document.querySelectorAll('[data-biblioteca-widget]').forEach((element) => {
        element.innerHTML = this.widget({
          href: element.dataset.href || '/biblioteca/',
          title: element.dataset.title || 'Approfondimento in arrivo',
          description: element.dataset.description || 'Consulta la Biblioteca CurioMondo.',
        });
      });
    },
  };
  window.CurioBiblioteca.mountWidgets();
})();
