/* CurioMondo v210: one small, deterministic home controller. */
(() => {
  'use strict';
  const $ = (selector, root = document) => root.querySelector(selector);
  const $$ = (selector, root = document) => Array.from(root.querySelectorAll(selector));
  const CM = window.CM;
  if (!CM) return;

  const topicClass = (label) => {
    const value = normalizeTopic(label);
    if (value.includes('ultima ora')) return 'urgent';
    if (value.includes('italia')) return 'italia';
    if (value.includes('mondo')) return 'mondo';
    if (value.includes('africa')) return 'africa';
    if (/(^|\s)(ia|ai)(\s|$)|intelligenza artificiale/.test(value)) return 'ia';
    if (/sicurezza|guerra|attacco/.test(value)) return 'sicurezza';
    if (/politica|governo|giustizia/.test(value)) return 'politica';
    if (/economia|energia|finanza/.test(value)) return 'economia';
    if (/ambiente|natura/.test(value)) return 'ambiente';
    if (/clima|maltempo/.test(value)) return 'clima';
    if (/scienza|ricerca/.test(value)) return 'scienza';
    if (/tecnologia|digitale/.test(value)) return 'tecnologia';
    if (/sport|calcio/.test(value)) return 'sport';
    if (/salute|sanita/.test(value)) return 'salute';
    if (/cultura|spettacolo/.test(value)) return 'cultura';
    if (/spazio|luna|astronomia/.test(value)) return 'spazio';
    return 'default';
  };
  function normalizeTopic(value) {
    return String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('it');
  }
  function decorateCard(card) {
    if (!card || card.dataset.cmDecorated === 'true') return;
    const meta = card.querySelector('.ameta,.meta');
    if (!meta) return;
    const original = meta.textContent.trim();
    const labels = original.split(/\s*[·/]\s*/).filter(Boolean);
    meta.replaceChildren(...labels.map((label) => {
      const span = document.createElement('span');
      span.className = 'cm-topic cm-topic-' + topicClass(label);
      span.textContent = label;
      return span;
    }));
    const classes = labels.map(topicClass);
    const priority = ['italia','mondo','africa','ia','sicurezza','politica','economia','ambiente','scienza','tecnologia','sport','salute','cultura','spazio'];
    const primary = priority.find((name) => classes.includes(name)) || 'default';
    card.classList.add('cm-cat-' + primary);
    if (classes.includes('urgent')) card.classList.add('cm-breaking');
    card.dataset.cmDecorated = 'true';
  }
  const decorateCards = (root = document) => root.querySelectorAll('.auto-card,.card').forEach(decorateCard);

  function open(id) {
    const node = document.getElementById(id);
    if (node) CM.openDialog(node);
  }
  $$('[data-open-dialog]').forEach((button) => {
    button.addEventListener('click', () => open(button.dataset.openDialog));
  });
  $$('[data-close-dialog]').forEach((button) => {
    button.addEventListener('click', () => CM.closeDialog(button.closest('dialog')));
  });

  const continueBar = $('#continueBar');
  const lastRead = CM.read('cm_last_read', null);
  if (continueBar && lastRead && Number(lastRead.progress || 0) < .92 && typeof lastRead.url === 'string' && lastRead.url.startsWith('/notizie/')) {
    const link = $('#continueLink');
    link.href = lastRead.url;
    $('#continueTitle').textContent = lastRead.title || 'Riprendi l’articolo';
    const image = $('#continueImage');
    if (image && lastRead.image) {
      image.src = lastRead.image;
      image.alt = lastRead.imageAlt || '';
    } else {
      image?.closest('.continue-thumb')?.remove();
      link.classList.add('without-image');
    }
    continueBar.classList.add('on');
  }
  $('#continueClose')?.addEventListener('click', () => continueBar.classList.remove('on'));

  let searchEntries;
  let searchRequest = 0;
  const normalize = (value) => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLocaleLowerCase('it');
  async function getSearchEntries() {
    if (searchEntries) return searchEntries;
    const response = await fetch('/assets/data/search-index-v210.json?v=236', { credentials: 'same-origin' });
    if (!response.ok) throw new Error('Indice non disponibile');
    const payload = await response.json();
    searchEntries = Array.isArray(payload.items) ? payload.items : [];
    return searchEntries;
  }
  function searchResult(entry) {
    const link = document.createElement('a');
    link.href = entry.url;
    const small = document.createElement('small');
    small.textContent = entry.section || 'CurioMondo';
    const strong = document.createElement('strong');
    strong.textContent = entry.title;
    const span = document.createElement('span');
    span.textContent = entry.excerpt || '';
    link.append(small, strong, span);
    return link;
  }
  async function runSearch(raw) {
    const request = ++searchRequest;
    const query = normalize(raw.trim());
    const results = $('#homeSearchResults');
    const status = $('#homeSearchStatus');
    results.replaceChildren();
    if (query.length < 2) {
      status.textContent = 'Scrivi almeno due caratteri.';
      return;
    }
    status.textContent = 'Ricerca in corso…';
    try {
      const items = await getSearchEntries();
      if (request !== searchRequest) return;
      const terms = query.split(/\s+/).filter(Boolean);
      const matches = items.filter((entry) => {
        const haystack = normalize([entry.title, entry.excerpt, entry.section, entry.searchText].join(' '));
        return terms.every((term) => haystack.includes(term));
      }).slice(0, 20);
      status.textContent = matches.length ? matches.length + (matches.length === 1 ? ' risultato' : ' risultati') : 'Nessun risultato.';
      results.append(...matches.map(searchResult));
    } catch {
      status.textContent = 'La ricerca non è disponibile in questo momento.';
    }
  }
  const searchForm = $('#homeSearchForm');
  const searchInput = $('#homeSearchInput');
  let searchTimer;
  searchInput?.addEventListener('input', () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => runSearch(searchInput.value), 160);
  });
  searchForm?.addEventListener('submit', (event) => {
    if (!searchInput?.value.trim()) return;
    event.preventDefault();
    runSearch(searchInput.value);
  });
  $$('[data-open-search]').forEach((button) => button.addEventListener('click', () => {
    open('homeSearchDialog');
    setTimeout(() => searchInput?.focus(), 20);
  }));
  const pageQuery = new URLSearchParams(location.search).get('q');
  if (pageQuery) {
    open('homeSearchDialog');
    searchInput.value = pageQuery;
    runSearch(pageQuery);
  }

  let feedItems;
  let feedCursor = Number($('#cards')?.dataset.initialCount || 0);
  async function getFeed() {
    if (feedItems) return feedItems;
    const response = await fetch('/assets/data/home-feed-v210.json?v=236', { credentials: 'same-origin' });
    if (!response.ok) throw new Error('Feed non disponibile');
    const payload = await response.json();
    feedItems = Array.isArray(payload.items) ? payload.items : [];
    return feedItems;
  }
  function picture(entry) {
    if (!entry.image) return null;
    const pictureNode = document.createElement('picture');
    const image = document.createElement('img');
    image.src = entry.image;
    image.alt = entry.imageAlt || '';
    image.width = entry.imageWidth || 800;
    image.height = entry.imageHeight || 533;
    image.loading = 'lazy';
    image.decoding = 'async';
    if (entry.srcset) {
      image.srcset = entry.srcset;
      image.sizes = '(max-width: 600px) calc(100vw - 28px), (max-width: 850px) calc(50vw - 28px), 380px';
    }
    pictureNode.append(image);
    return pictureNode;
  }
  function feedCard(entry) {
    const link = document.createElement('a');
    link.className = 'card';
    link.href = entry.url;
    const visual = picture(entry);
    if (visual) link.append(visual);
    const body = document.createElement('div');
    body.className = 'body';
    const meta = document.createElement('div');
    meta.className = 'meta';
    meta.textContent = entry.section || 'Notizie';
    const title = document.createElement('h3');
    title.textContent = entry.title;
    const excerpt = document.createElement('p');
    excerpt.textContent = entry.excerpt || '';
    const time = document.createElement('time');
    if (entry.dateISO) time.dateTime = entry.dateISO;
    time.textContent = entry.dateLabel || '';
    body.append(meta, title, excerpt, time);
    link.append(body);
    decorateCard(link);
    return link;
  }
  async function appendFeed() {
    const button = $('#loadMoreNews');
    if (!button || button.disabled) return;
    const status = $('#loadMoreStatus');
    const idleLabel = button.textContent;
    button.disabled = true;
    button.setAttribute('aria-busy', 'true');
    button.textContent = 'Caricamento…';
    if (status) status.textContent = 'Sto caricando le prossime notizie…';
    try {
      const items = await getFeed();
      const lastRendered = Array.from($('#cards')?.querySelectorAll('.card[href]') || []).at(-1);
      if (lastRendered) {
        const lastPath = new URL(lastRendered.href, location.href).pathname;
        const lastIndex = items.findIndex((item) => new URL(item.url, location.href).pathname === lastPath);
        if (lastIndex >= 0) feedCursor = Math.max(feedCursor, lastIndex + 1);
      }
      const next = items.slice(feedCursor, feedCursor + 12);
      if (!next.length) {
        button.hidden = true;
        if (status) status.textContent = 'Hai già visualizzato tutte le notizie disponibili.';
        return;
      }
      const newCards = next.map(feedCard);
      $('#cards').append(...newCards);
      feedCursor += next.length;
      if (feedCursor >= items.length) button.hidden = true;
      if (status) status.textContent = `${next.length} nuove notizie caricate.`;
      requestAnimationFrame(() => newCards[0]?.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'start' }));
    } catch {
      CM.toast('Non riesco a caricare altri articoli.');
      if (status) status.textContent = 'Caricamento non riuscito. Riprova tra poco.';
    } finally {
      button.disabled = false;
      button.removeAttribute('aria-busy');
      button.textContent = idleLabel;
    }
  }
  $('#loadMoreNews')?.addEventListener('click', appendFeed);

  decorateCards();
  const cardsRoot = $('#cards');
  if (cardsRoot) new MutationObserver(() => decorateCards(cardsRoot)).observe(cardsRoot, { childList: true });

  const params = new URLSearchParams(location.search);
  const category = params.get('cat') || params.get('categoria');
  if (category) {
    getFeed().then((items) => {
      const selected = items.filter((entry) => normalize(entry.section).includes(normalize(category)));
      const cards = $('#cards');
      cards.replaceChildren(...selected.slice(0, 24).map(feedCard));
      feedCursor = Math.min(24, selected.length);
      $('#sectionTitle').textContent = selected.length ? 'Categoria: ' + category : 'Nessun articolo in questa categoria';
      $('#loadMoreNews').hidden = true;
      $('#categoryBanner').hidden = false;
      $('#catPageLabel').textContent = category;
    }).catch(() => CM.toast('Categoria non disponibile.'));
  }

  async function showFavorites() {
    open('favoritesDialog');
    const output = $('#favoritesList');
    output.textContent = 'Caricamento…';
    try {
      const saved = CM.read('cm_favs', []);
      const index = await getSearchEntries();
      const lookup = new Map(index.map((entry) => [entry.url, entry]));
      const entries = (Array.isArray(saved) ? saved : []).map((value) => lookup.get(value) || lookup.get('/notizie/' + value + '.html')).filter(Boolean);
      output.replaceChildren();
      if (!entries.length) {
        const empty = document.createElement('p');
        empty.textContent = 'Non hai ancora salvato articoli.';
        output.append(empty);
      } else {
        output.append(...entries.map(searchResult));
      }
    } catch {
      output.textContent = 'I preferiti non sono disponibili.';
    }
  }
  $$('[data-show-favorites]').forEach((button) => button.addEventListener('click', showFavorites));

  let quizItems;
  let currentQuiz;
  let answered = false;
  const quizKey = 'cm_quiz_seen_v210';
  const starsKey = 'cm_quiz_stars_v210';
  async function getQuiz() {
    if (quizItems) return quizItems;
    const response = await fetch('/assets/data/quiz-curiomondo.json', { credentials: 'same-origin' });
    if (!response.ok) throw new Error('Quiz non disponibile');
    const payload = await response.json();
    quizItems = Array.isArray(payload.items) ? payload.items : [];
    return quizItems;
  }
  function pickQuiz(items) {
    let seen = CM.read(quizKey, []);
    if (!Array.isArray(seen) || seen.length >= items.length) seen = [];
    const available = items.filter((item) => !seen.includes(item.id));
    const item = available[Math.floor(Math.random() * available.length)] || items[0];
    seen.push(item.id);
    CM.write(quizKey, seen);
    return item;
  }
  function revealQuiz(selected, viaReveal) {
    if (answered || !currentQuiz) return;
    answered = true;
    const buttons = $$('.cm-quiz-option', $('#quizOptions'));
    buttons.forEach((button, index) => {
      button.disabled = true;
      if (index === currentQuiz.correctIndex) button.classList.add('is-correct');
      if (selected === index && index !== currentQuiz.correctIndex) button.classList.add('is-wrong');
    });
    const correct = selected === currentQuiz.correctIndex && !viaReveal;
    if (correct) CM.write(starsKey, Number(CM.read(starsKey, 0)) + 1);
    $('#quizStars').textContent = String(CM.read(starsKey, 0));
    $('#quizResultLabel').textContent = correct ? '✓ Esatto' : (viaReveal ? 'Ecco la risposta' : 'Non proprio');
    $('#quizExplanationText').textContent = currentQuiz.explanation || '';
    $('#quizCuriosity').textContent = currentQuiz.curiosity || '';
    $('#quizExplanation').hidden = false;
    $('#quizReveal').disabled = true;
    $('#quizNext').disabled = false;
  }
  function renderQuiz(item) {
    currentQuiz = item;
    answered = false;
    $('#quizCategory').textContent = item.category || 'Cultura generale';
    $('#quizQuestion').textContent = item.question;
    $('#quizStars').textContent = String(CM.read(starsKey, 0));
    const options = $('#quizOptions');
    options.replaceChildren(...item.options.map((label, index) => {
      const button = document.createElement('button');
      button.className = 'cm-quiz-option';
      button.type = 'button';
      button.dataset.letter = String.fromCharCode(65 + index);
      button.textContent = label;
      button.addEventListener('click', () => revealQuiz(index, false));
      return button;
    }));
    $('#quizExplanation').hidden = true;
    $('#quizReveal').disabled = false;
    $('#quizNext').disabled = true;
  }
  async function nextQuiz() {
    $('#quizLoading').hidden = false;
    $('#quizMain').hidden = true;
    try {
      const items = await getQuiz();
      if (!items.length) throw new Error('Quiz vuoto');
      renderQuiz(pickQuiz(items));
      $('#quizLoading').hidden = true;
      $('#quizMain').hidden = false;
    } catch {
      $('#quizLoading').textContent = 'Quiz non disponibile.';
    }
  }
  $$('[data-open-quiz]').forEach((button) => button.addEventListener('click', () => {
    open('quizDialog');
    nextQuiz();
  }));
  $('#quizReveal')?.addEventListener('click', () => revealQuiz(null, true));
  $('#quizNext')?.addEventListener('click', nextQuiz);

  let worldFacts;
  async function showFact() {
    try {
      if (!worldFacts) {
        const response = await fetch('/assets/data/world-facts-v210.json', { credentials: 'same-origin' });
        if (!response.ok) throw new Error('Curiosità non disponibili');
        worldFacts = await response.json();
      }
      let seen = CM.read('cm_world_seen_v210', []);
      if (!Array.isArray(seen) || seen.length >= worldFacts.length) seen = [];
      const indexes = worldFacts.map((_, index) => index).filter((index) => !seen.includes(index));
      const index = indexes[Math.floor(Math.random() * indexes.length)];
      seen.push(index);
      CM.write('cm_world_seen_v210', seen);
      const count = Number(CM.read('cm_world_count_v210', 0)) + 1;
      CM.write('cm_world_count_v210', count);
      $('#worldFactCategory').textContent = worldFacts[index][0];
      $('#worldFactText').textContent = worldFacts[index][1];
      $('#worldFactCount').textContent = String(count);
      $('#worldFact').hidden = false;
      $('#worldLearnedCount').textContent = String(count);
    } catch {
      CM.toast('Curiosità non disponibile.');
    }
  }
  $('#worldCore')?.addEventListener('click', showFact);
  $('#worldFactClose')?.addEventListener('click', () => { $('#worldFact').hidden = true; });
  $('#worldLearnedCount').textContent = String(CM.read('cm_world_count_v210', 0));
  $$('[data-orbit-action]').forEach((button) => button.addEventListener('click', () => {
    const stage = button.closest('.cm-orbit-stage');
    const action = button.dataset.orbitAction;
    stage?.classList.add('is-accelerating');
    window.setTimeout(() => {
      stage?.classList.remove('is-accelerating');
      if (action === 'quiz') open('quizDialog'), nextQuiz();
      if (action === 'favs') showFavorites();
      if (action === 'about') location.assign('/pagine/chi-siamo.html');
      if (action === 'contact') location.assign('/pagine/contatti.html');
    }, 720);
  }));
})();
