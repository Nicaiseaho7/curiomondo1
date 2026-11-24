/* Il 300x250 resta uno solo. Su scioperi e concerti non entra nella lista: lì c'è il Native Banner. */
(() => {
  "use strict";
  if (!/^\/(scioperi|scadenze|concerti)(\/|$)/.test(location.pathname)) return;
  if (/^\/(scioperi|concerti)(\/|$)/.test(location.pathname)) return;
  const pool = Array.from(document.querySelectorAll("[data-cm-date-ad]"));
  const home = document.getElementById("cm-date-ad-pool");
  if (!pool.length || !home) return;

  const roots = ["#deadlineGroups", "#archiveGroups"]
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
    const root = document.querySelector("#deadlineGroups") || document.querySelector("#archiveGroups");
    if (!root) return found;
    const groups = Array.from(root.children).filter((node) => node.matches("section.deadline-group"));
    if (groups.length >= 2) {
      for (let index = 0; index < groups.length - 1; index += 2) found.push(groups[index]);
    } else if (groups.length === 1) {
      const cards = Array.from(groups[0].querySelectorAll(".deadline-card"));
      const middle = cardAfter(cards, 0.5);
      if (middle) found.push(middle);
    }
    const native = document.querySelector("[data-cm-native-slot]");
    return unique(found).filter((node) => !native || (native.previousElementSibling !== node && node !== native));
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
  place();
  setTimeout(place, 500);
  setTimeout(place, 1500);
})();
