/* Sposta i riquadri 300x250, già eseguiti nel markup, in mezzo alle date. */
(() => {
  "use strict";
  if (!/^\/(scioperi|scadenze|concerti)(\/|$)/.test(location.pathname)) return;
  const pool = Array.from(document.querySelectorAll("[data-cm-date-ad]"));
  const home = document.getElementById("cm-date-ad-pool");
  if (!pool.length || !home) return;

  const roots = ["#nationalEvents", "#archiveEvents", "#concertGroups", "#deadlineGroups", "#archiveGroups", "#regionsAccordion"]
    .map((selector) => document.querySelector(selector))
    .filter(Boolean);

  let placing = false;

  function unique(nodes) {
    return nodes.filter((node, index) => node && nodes.indexOf(node) === index);
  }

  function cardAfter(cards, fraction) {
    if (cards.length < 3) return null;
    const index = Math.min(cards.length - 2, Math.max(0, Math.round(cards.length * fraction) - 1));
    return cards[index];
  }

  function anchors() {
    const found = [];
    const national = document.querySelector("#nationalEvents");
    const archiveEvents = document.querySelector("#archiveEvents");
    [national, archiveEvents].forEach((list) => {
      if (!list) return;
      const cards = Array.from(list.children).filter((node) => node.classList.contains("event-card"));
      const middle = cardAfter(cards, 0.5);
      if (middle) found.push(middle);
      if (cards.length >= 8) {
        const early = cardAfter(cards, 0.33);
        if (early) found.push(early);
      }
    });

    ["#concertGroups", "#deadlineGroups", "#archiveGroups"].forEach((selector) => {
      const root = document.querySelector(selector);
      if (!root) return;
      const groups = Array.from(root.children).filter((node) => node.matches("details.month-fold, section.deadline-group"));
      if (groups.length >= 2) {
        for (let index = 0; index < groups.length - 1; index += 2) found.push(groups[index]);
        return;
      }
      if (groups.length === 1) {
        const cards = Array.from(groups[0].querySelectorAll(".event-card, .deadline-card"));
        const middle = cardAfter(cards, 0.5);
        if (middle) found.push(middle);
      }
    });

    document.querySelectorAll("#regionsAccordion .region-panel").forEach((panel) => {
      if (panel.hidden) return;
      const cards = Array.from(panel.querySelectorAll(".event-card"));
      const middle = cardAfter(cards, 0.5);
      if (middle) found.push(middle);
    });

    return unique(found);
  }

  function place() {
    if (placing) return;
    placing = true;
    const spots = anchors();
    pool.forEach((slot, index) => {
      const spot = spots[index];
      if (spot && spot.isConnected) {
        if (slot.previousElementSibling !== spot) spot.after(slot);
      } else if (slot.parentElement !== home) {
        home.append(slot);
      }
    });
    placing = false;
  }

  const observer = new MutationObserver(() => {
    if (!placing) place();
  });
  roots.forEach((root) => observer.observe(root, { childList: true, subtree: true }));
  document.addEventListener("click", (event) => {
    if (event.target.closest(".region-toggle, .regions-fold, .month-fold")) {
      setTimeout(place, 60);
    }
  });
  place();
  setTimeout(place, 500);
  setTimeout(place, 1500);
})();
