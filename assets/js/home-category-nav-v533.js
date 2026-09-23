/* CurioMondo v533 — la barra delle sezioni scorre nella home invece di uscirne.
 *
 * I collegamenti restano puntati alle pagine categoria: senza JavaScript, o
 * quando una sezione non e presente nella home di oggi, il lettore ci arriva
 * comunque. Quando invece la sezione c'e, il clic la porta sotto gli occhi.
 */
(() => {
  'use strict';
  // La home chiama "film-tv" cio che nell'archivio e "film-serie-tv".
  const ALIAS = { 'film-serie-tv': 'film-tv' };
  const idDa = (href) => {
    const m = String(href || '').match(/\/categorie\/([^/]+)\//);
    if (!m) return '';
    return 'categoria-' + (ALIAS[m[1]] || m[1]);
  };

  const vaiA = (sezione) => {
    sezione.scrollIntoView({ behavior: 'smooth', block: 'start' });
    // L'indirizzo cambia senza far saltare la pagina: cosi il "torna indietro"
    // del telefono riporta dove si era.
    history.replaceState(null, '', '#' + sezione.id);
    const titolo = sezione.querySelector('.cm-topic-section__title');
    if (titolo) {
      titolo.setAttribute('tabindex', '-1');
      titolo.focus({ preventScroll: true });
    }
  };

  // Le sezioni nascono da JavaScript: al primo clic possono non esserci ancora.
  const attendi = (id, quando, scadenza = 1500) => {
    const partenza = Date.now();
    const prova = () => {
      const sezione = document.getElementById(id);
      if (sezione) return quando(sezione);
      if (Date.now() - partenza < scadenza) requestAnimationFrame(prova);
      else quando(null);
    };
    prova();
  };

  document.addEventListener('click', (evento) => {
    const collegamento = evento.target.closest('.cm-edition-nav a[href*="/categorie/"]');
    if (!collegamento || evento.metaKey || evento.ctrlKey || evento.shiftKey || evento.button !== 0) return;
    const id = idDa(collegamento.getAttribute('href'));
    if (!id) return;
    const subito = document.getElementById(id);
    if (subito) { evento.preventDefault(); vaiA(subito); return; }
    // Sezione non ancora costruita: si trattiene il clic e si aspetta un attimo.
    evento.preventDefault();
    attendi(id, (sezione) => {
      if (sezione) vaiA(sezione);
      else window.location.href = collegamento.getAttribute('href');
    });
  });

  // Arrivo con l'ancora gia nell'indirizzo (link condiviso, ricarica).
  if (location.hash.startsWith('#categoria-')) {
    attendi(location.hash.slice(1), (sezione) => { if (sezione) vaiA(sezione); });
  }
})();
