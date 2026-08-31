/* Biblioteca CurioMondo v210: throttled reader progress and race-safe search. */
(() => {
  'use strict';
  const CM = window.CM;
  document.querySelectorAll('[data-cb-theme]').forEach((button) => {
    button.setAttribute('data-theme-toggle', '');
  });
  if (!CM) return;
  const reader = document.querySelector('[data-cb-reader]');
  if (!reader) return;
  const BOOKMARK_KEY = 'cm_biblioteca_resume_v1';
  const PENDING_KEY = 'cm_biblioteca_pending_resume_v1';
  const progress = document.querySelector('.cb-progress');
  const book = reader.dataset.book || '';
  const chapterUrl = reader.dataset.chapterUrl || location.pathname;
  const chapterLabel = reader.dataset.chapterLabel || 'questa sezione';
  const tocLinks = Array.from(document.querySelectorAll('[data-cb-toc] a[href]'));
  const sections = Array.from(document.querySelectorAll('.cb-chapter h2, .cb-chapter h3'));
  const normalizePath = (value) => (value || '/').replace(/\/+$/, '') || '/';
  let sectionOffsets = [];
  let framePending = false;
  let lastSave = 0;

  reader.querySelectorAll('.cb-chapter img').forEach((image) => {
    image.loading = 'lazy';
    image.decoding = 'async';
    if (!image.width || !image.height) {
      image.style.aspectRatio = image.style.aspectRatio || '3 / 2';
    }
  });
  reader.querySelectorAll('.cb-chapter iframe').forEach((frame) => { frame.loading = 'lazy'; });
  reader.querySelectorAll('.cb-chapter table').forEach((table) => table.classList.add('cb-lazy-table'));

  function readBookmarks() {
    const stored = CM.read(BOOKMARK_KEY, {});
    return stored && stored.book ? { [stored.book]: stored } : (stored || {});
  }
  function saveBookmark(top) {
    if (!book) return;
    const bookmarks = readBookmarks();
    bookmarks[book] = {
      book,
      url: chapterUrl,
      label: chapterLabel,
      top: Math.max(0, Math.round(top)),
      updated: Date.now(),
    };
    CM.write(BOOKMARK_KEY, bookmarks);
  }
  function measureSections() {
    sectionOffsets = sections.map((heading) => ({
      id: heading.id,
      top: heading.getBoundingClientRect().top + scrollY,
    })).filter((entry) => entry.id);
  }
  function refresh() {
    framePending = false;
    const maximum = document.documentElement.scrollHeight - innerHeight;
    const percentage = maximum > 0 ? Math.max(0, Math.min(100, scrollY / maximum * 100)) : 0;
    if (progress) progress.style.width = percentage + '%';
    const threshold = scrollY + innerHeight * .38;
    let active = '';
    for (const entry of sectionOffsets) {
      if (entry.top > threshold) break;
      active = entry.id;
    }
    tocLinks.forEach((link) => {
      const href = link.getAttribute('href') || '';
      link.classList.toggle('active', Boolean(active) && (href === '#' + active || href.endsWith('#' + active)));
    });
    const now = Date.now();
    if (now - lastSave > 4000) {
      saveBookmark(scrollY);
      lastSave = now;
    }
  }
  function schedule() {
    if (framePending) return;
    framePending = true;
    requestAnimationFrame(refresh);
  }
  measureSections();
  refresh();
  addEventListener('scroll', schedule, { passive: true });
  addEventListener('resize', () => { measureSections(); schedule(); }, { passive: true });
  addEventListener('pagehide', () => saveBookmark(scrollY));

  const saved = readBookmarks()[book];
  let pending = null;
  try { pending = JSON.parse(sessionStorage.getItem(PENDING_KEY) || 'null'); } catch {}
  if (pending && pending.book === book && normalizePath(pending.url) === normalizePath(chapterUrl)) {
    try { sessionStorage.removeItem(PENDING_KEY); } catch {}
    setTimeout(() => scrollTo({ top: pending.top || 0, behavior: 'auto' }), 0);
  } else {
    pending = null;
  }
  if (saved && saved.top > 64 && !pending) {
    const notice = document.querySelector('[data-cb-resume]');
    if (notice) {
      notice.hidden = false;
      const text = notice.querySelector('[data-cb-resume-text]');
      if (text) text.textContent = 'Vuoi riprendere da ' + (saved.label || 'dove ti eri fermato') + '?';
      notice.querySelector('button')?.addEventListener('click', () => {
        if (normalizePath(saved.url) === normalizePath(chapterUrl)) {
          scrollTo({ top: saved.top || 0, behavior: 'smooth' });
        } else {
          try { sessionStorage.setItem(PENDING_KEY, JSON.stringify(saved)); } catch {}
          location.href = (saved.url || chapterUrl) + '#riprendi';
        }
        notice.hidden = true;
      });
    }
  }

  document.querySelectorAll('[data-cb-toc-toggle]').forEach((button) => {
    button.addEventListener('click', () => {
      const expanded = reader.classList.toggle('toc-open');
      button.setAttribute('aria-expanded', String(expanded));
    });
  });

  const resultBox = document.querySelector('[data-cb-toc-results]');
  const indexUrl = reader.dataset.cbSearchIndex;
  let searchEntries;
  let searchToken = 0;
  function makeResult(entry) {
    const link = document.createElement('a');
    link.className = 'cb-search-result';
    link.href = entry.href;
    const title = document.createElement('strong');
    title.textContent = entry.title || 'Risultato nel manuale';
    const excerpt = document.createElement('span');
    const value = entry.text || '';
    excerpt.textContent = value.length > 130 ? value.slice(0, 130).trim() + '…' : value;
    link.append(title, excerpt);
    return link;
  }
  async function searchBook(query) {
    if (!resultBox) return;
    const token = ++searchToken;
    resultBox.replaceChildren();
    if (!query || !indexUrl) return;
    try {
      if (!searchEntries) {
        const response = await fetch(indexUrl, { credentials: 'same-origin' });
        if (!response.ok) throw new Error('Indice non disponibile');
        const payload = await response.json();
        searchEntries = Array.isArray(payload.entries) ? payload.entries : [];
      }
      if (token !== searchToken) return;
      const matches = searchEntries.filter((entry) => ((entry.title || '') + ' ' + (entry.text || '')).toLocaleLowerCase('it').includes(query)).slice(0, 8);
      if (!matches.length) {
        const empty = document.createElement('p');
        empty.textContent = 'Nessun risultato nel manuale.';
        resultBox.append(empty);
      } else {
        const label = document.createElement('p');
        label.textContent = 'Risultati nel libro';
        resultBox.append(label, ...matches.map(makeResult));
      }
    } catch {
      if (token === searchToken) resultBox.textContent = 'La ricerca completa non è disponibile in questo momento.';
    }
  }
  let timer;
  document.querySelectorAll('[data-cb-toc-search]').forEach((input) => {
    input.addEventListener('input', () => {
      const query = input.value.trim().toLocaleLowerCase('it');
      tocLinks.forEach((link) => {
        link.hidden = Boolean(query) && !link.textContent.toLocaleLowerCase('it').includes(query);
      });
      clearTimeout(timer);
      timer = setTimeout(() => searchBook(query), 140);
    });
  });
})();

(() => {
  'use strict';
  const escapeHTML = (value) => String(value || '').replace(/[&<>'"]/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
  })[character]);
  window.CurioBiblioteca = {
    widget({ href, title, description }) {
      return '<aside class="cb-widget"><small>Approfondisci in Biblioteca</small><h3>' +
        escapeHTML(title) + '</h3><p>' + escapeHTML(description) + '</p><a href="' +
        escapeHTML(href || '/biblioteca/') + '">Apri il manuale →</a></aside>';
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
