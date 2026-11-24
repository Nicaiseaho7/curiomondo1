/* Un solo Native Banner per pagina. Su scioperi e concerti sta in mezzo alle date. */
(() => {
  "use strict";
  if (!/^\/(scioperi|scadenze|concerti)(\/|$)/.test(location.pathname)) return;
  const id = "container-81e6446ad1091f193a3bcc8fbb538b94";
  if (document.getElementById(id)) return;

  const style = document.createElement("style");
  style.textContent = ".cm-native-banner-slot{width:min(1180px,calc(100% - 40px));margin:22px auto;clear:both}.cm-native-banner{max-width:100%;overflow:hidden;clear:both}.cm-native-banner iframe,.cm-native-banner img{max-width:100%;height:auto}";
  document.head.append(style);

  const slot = document.createElement("div");
  slot.className = "cm-native-banner-slot";
  slot.setAttribute("data-cm-native-slot", "");
  const box = document.createElement("div");
  box.id = id;
  box.className = "cm-native-banner";
  slot.append(box);

  const src = "https://bauval.org/21/81e6446ad1091f193a3bcc8fbb538b94";
  let armed = false;
  function arm() {
    if (armed || document.querySelector('script[src="' + src + '"]')) return;
    armed = true;
    const script = document.createElement("script");
    script.async = true;
    script.fetchPriority = "high";
    script.setAttribute("data-cfasync", "false");
    script.src = src;
    box.before(script);
  }

  function middle(nodes) {
    if (!nodes || nodes.length < 2) return null;
    return nodes[Math.floor(nodes.length / 2) - 1];
  }

  function cardsIn(root, selector) {
    if (!root) return [];
    return Array.from(root.querySelectorAll(selector)).filter((node) => node.closest("[data-cm-date-ad], [data-cm-native-slot], .cm-date-ad") !== node && !node.closest(".cm-date-ad"));
  }

  function anchor() {
    const path = location.pathname;
    if (/^\/scioperi(\/|$)/.test(path)) {
      const list = document.querySelector("#nationalEvents") || document.querySelector("#archiveEvents");
      const dates = list ? Array.from(list.children).filter((node) => node.classList.contains("event-card")) : [];
      const date = middle(dates);
      if (date) return date;
      const news = Array.from(document.querySelectorAll("#strikeNews > .news-card, #strikeNews > article"));
      return middle(news);
    }
    if (/^\/concerti(\/|$)/.test(path)) {
      const root = document.querySelector("#concertGroups") || document.querySelector("#archiveGroups");
      if (!root) return null;
      const folds = Array.from(root.children).filter((node) => node.matches("details.month-fold"));
      const fold = middle(folds);
      if (fold) return fold;
      const dates = cardsIn(root, ".event-card");
      return middle(dates);
    }
    return null;
  }

  function park() {
    const footer = document.querySelector("footer.site-footer");
    const main = document.querySelector("main");
    if (footer) footer.before(slot);
    else if (main) main.append(slot);
  }

  let placing = false;
  function place() {
    if (placing) return;
    placing = true;
    const spot = anchor();
    if (spot && spot.isConnected) {
      if (slot.previousElementSibling !== spot) spot.after(slot);
      arm();
    }
    placing = false;
  }

  if (/^\/scadenze(\/|$)/.test(location.pathname)) {
    park();
    arm();
    return;
  }

  const roots = ["#nationalEvents", "#archiveEvents", "#concertGroups", "#archiveGroups", "#strikeNews"]
    .map((selector) => document.querySelector(selector))
    .filter(Boolean);
  const observer = new MutationObserver(() => place());
  roots.forEach((root) => observer.observe(root, { childList: true, subtree: true }));
  place();
  setTimeout(place, 600);
  setTimeout(() => {
    if (!slot.isConnected) {
      park();
      arm();
    }
  }, 2200);
})();
