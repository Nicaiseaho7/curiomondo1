/* Mette i banner, tranne il native, in mezzo alle date. */
(function () {
  "use strict";
  if (!/^\/(scioperi|concerti|scadenze)(\/|$)/.test(location.pathname)) return;

  function cards() {
    return Array.from(document.querySelectorAll(
      "#nationalEvents > .event-card, #concertGroups .event-card, #deadlineGroups .deadline-card, " +
      "#archiveGroups .deadline-card, #archiveGroups .event-card, #archiveEvents > .event-card"
    ));
  }

  function slots() {
    return Array.from(document.querySelectorAll("[data-cm-ad]")).filter(function (slot) {
      return slot.getAttribute("data-cm-ad") !== "native";
    });
  }

  var placing = false;
  function place() {
    if (placing) return;
    var list = cards();
    var ads = slots();
    if (list.length < 2 || !ads.length) return;
    placing = true;
    var fracs = [0.22, 0.42, 0.62, 0.78];
    var used = {};
    var plan = ads.map(function (slot, index) {
      var frac = fracs[index] !== undefined ? fracs[index] : Math.min(0.8, 0.3 + index * 0.12);
      var at = Math.round((list.length - 1) * frac);
      at = Math.max(0, Math.min(list.length - 2, at));
      while (used[at] && at > 0) at -= 1;
      used[at] = true;
      slot.hidden = false;
      slot.removeAttribute("hidden");
      return { slot: slot, at: at };
    });
    plan.sort(function (a, b) { return b.at - a.at; });
    plan.forEach(function (item) {
      var card = list[item.at];
      if (card && item.slot.previousElementSibling !== card) card.after(item.slot);
    });
    placing = false;
  }

  var roots = ["#nationalEvents", "#archiveEvents", "#concertGroups", "#archiveGroups", "#deadlineGroups"];
  function observe() {
    roots.forEach(function (selector) {
      var root = document.querySelector(selector);
      if (!root || root.dataset.cmMidObserved) return;
      root.dataset.cmMidObserved = "1";
      new MutationObserver(function () { if (!placing) place(); }).observe(root, { childList: true, subtree: true });
    });
  }

  function start() {
    observe();
    place();
    setTimeout(place, 500);
    setTimeout(place, 1600);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", start);
  else start();
})();
