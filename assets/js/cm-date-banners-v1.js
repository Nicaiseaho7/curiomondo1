/* Mette i banner che non sono Adsterra in mezzo alle date, una volta sola. */
(function () {
  "use strict";
  if (!/^\/(scioperi|concerti|scadenze)(\/|$)/.test(location.pathname)) return;

  var units = [
    {
      key: "exo2",
      selector: '[data-cm-ad="exo2"]',
      html: '<aside class="cm-safe-ad" data-cm-ad="exo2" aria-label="Pubblicita" style="display:block;text-align:center;clear:both;width:100%;margin:28px auto;min-height:0;"><script async type="application/javascript" src="https://a.magsrv.com/ad-provider.js"><\/script><ins class="eas6a97888e17" data-zoneid="6106094"></ins><script>(AdProvider = window.AdProvider || []).push({"serve": {}});<\/script></aside>'
    },
    {
      key: "exo",
      selector: '[data-cm-ad="exo"]',
      html: '<aside class="cm-safe-ad" data-cm-ad="exo" aria-label="Pubblicita" style="display:block;text-align:center;clear:both;width:100%;margin:28px auto;min-height:0;"><script async type="application/javascript" src="https://a.magsrv.com/ad-provider.js"><\/script><ins class="eas6a97888e10" data-zoneid="6106062"></ins><script>(AdProvider = window.AdProvider || []).push({"serve": {}});<\/script></aside>'
    },
    {
      key: "adcash",
      selector: "#cm-adcash-slot",
      html: '<aside class="cm-safe-ad" id="cm-adcash-slot" data-cm-ad="adcash" aria-label="Pubblicita" style="display:block;text-align:center;clear:both;width:100%;margin:28px auto;min-height:0;"><script type="text/javascript">aclib.runBanner({zoneId:"12487982"});<\/script></aside>'
    }
  ];

  function cards() {
    return Array.from(document.querySelectorAll(
      "#nationalEvents > .event-card, #concertGroups .event-card, #deadlineGroups .deadline-card, #archiveGroups .deadline-card, #archiveGroups .event-card, #archiveEvents > .event-card"
    ));
  }

  function ensure(unit) {
    var nodes = Array.from(document.querySelectorAll(unit.selector));
    var slot = nodes[0];
    if (!slot) {
      var wrap = document.createElement("div");
      wrap.innerHTML = unit.html;
      slot = wrap.firstElementChild;
    }
    nodes.slice(1).forEach(function (extra) { extra.remove(); });
    return slot;
  }

  var placing = false;
  function place() {
    if (placing) return;
    var list = cards();
    if (list.length < 2) return;
    placing = true;
    var fractions = [0.34, 0.55, 0.76];
    units.forEach(function (unit, index) {
      var slot = ensure(unit);
      var at = Math.min(list.length - 1, Math.max(0, Math.round(list.length * fractions[index]) - 1));
      var card = list[at];
      if (card && slot && slot.previousElementSibling !== card) card.after(slot);
    });
    if (window.AdProvider) {
      try { (AdProvider = window.AdProvider || []).push({ serve: {} }); } catch (e) {}
    }
    placing = false;
  }

  var roots = ["#nationalEvents", "#concertGroups", "#deadlineGroups", "#archiveGroups", "#archiveEvents"]
    .map(function (selector) { return document.querySelector(selector); })
    .filter(Boolean);
  var observer = new MutationObserver(function () {
    if (!placing) place();
  });
  roots.forEach(function (root) {
    observer.observe(root, { childList: true, subtree: true });
  });
  place();
  setTimeout(place, 600);
  setTimeout(place, 1800);
})();
