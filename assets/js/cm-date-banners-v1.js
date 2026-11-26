/* Sposta il banner Adcash fra le date. Non carica video né popup. */
(function () {
  "use strict";
  if (!/^\/(scioperi|concerti|scadenze)(\/|$)/.test(location.pathname)) return;

  function cards() {
    return Array.from(document.querySelectorAll(
      "#nationalEvents > .event-card, #concertGroups .event-card, #deadlineGroups .deadline-card, " +
      "#archiveGroups .deadline-card, #archiveGroups .event-card, #archiveEvents > .event-card"
    )).filter(function (node) {
      return !node.closest("[data-cm-date-ad], [data-cm-native-slot], .cm-date-ad");
    });
  }

  function place() {
    var list = cards();
    if (list.length < 2) return;
    var slot = document.querySelector('[data-cm-ad="adcash"]');
    if (!slot) return;
    slot.hidden = false;
    slot.removeAttribute("hidden");
    var at = Math.min(list.length - 1, Math.max(0, Math.round(list.length * 0.5) - 1));
    var card = list[at];
    if (card && slot.previousElementSibling !== card) card.after(slot);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", place);
  else place();
})();
