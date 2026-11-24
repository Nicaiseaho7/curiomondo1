/* Distribuisce i banner fra le date e avvia sempre gli script creati a runtime. */
(function () {
  "use strict";

  if (!/^\/(scioperi|concerti|scadenze)(\/|$)/.test(location.pathname)) return;

  var EXO_PROVIDER = "https://a.magsrv.com/ad-provider.js";
  var units = [
    { key: "exo2", selector: '[data-cm-ad="exo2"]', zone: "6106094", className: "eas6a97888e17", fraction: 0.34 },
    { key: "exo", selector: '[data-cm-ad="exo"]', zone: "6106062", className: "eas6a97888e10", fraction: 0.58 },
    { key: "adcash", selector: "#cm-adcash-slot", zone: "12487982", fraction: 0.80 }
  ];

  function cards() {
    return Array.from(document.querySelectorAll(
      "#nationalEvents > .event-card, #concertGroups .event-card, #deadlineGroups .deadline-card, " +
      "#archiveGroups .deadline-card, #archiveGroups .event-card, #archiveEvents > .event-card"
    )).filter(function (node) {
      return !node.closest("[data-cm-date-ad], [data-cm-native-slot], .cm-date-ad");
    });
  }

  function makeSlot(unit) {
    var slot = document.createElement("aside");
    slot.className = "cm-safe-ad cm-date-ad";
    slot.setAttribute("data-cm-ad", unit.key);
    slot.setAttribute("data-cm-date-ad", unit.key);
    slot.setAttribute("aria-label", "Pubblicita");
    if (unit.key === "adcash") slot.id = "cm-adcash-slot";
    return slot;
  }

  function ensure(unit) {
    var nodes = Array.from(document.querySelectorAll(unit.selector));
    var slot = nodes.shift() || makeSlot(unit);
    nodes.forEach(function (extra) { extra.remove(); });
    slot.classList.add("cm-date-ad");
    slot.setAttribute("data-cm-date-ad", unit.key);
    return slot;
  }

  function loadScriptOnce(id, src, ready) {
    var script = document.getElementById(id);
    if (script) {
      if (script.dataset.cmLoaded === "true") ready();
      else script.addEventListener("load", ready, { once: true });
      return;
    }
    script = document.createElement("script");
    script.id = id;
    script.async = true;
    script.src = src;
    script.setAttribute("data-cfasync", "false");
    script.addEventListener("load", function () {
      script.dataset.cmLoaded = "true";
      ready();
    }, { once: true });
    document.head.appendChild(script);
  }

  function armExo(slot, unit) {
    if (slot.dataset.cmArmed === "true") return;
    slot.dataset.cmArmed = "true";
    var ins = slot.querySelector("ins[data-zoneid]");
    if (!ins) {
      ins = document.createElement("ins");
      ins.className = unit.className;
      ins.setAttribute("data-zoneid", unit.zone);
      slot.appendChild(ins);
    }
    function serve() {
      try {
        window.AdProvider = window.AdProvider || [];
        window.AdProvider.push({ serve: {} });
      } catch (error) {
        slot.dataset.cmAdError = "provider";
      }
    }
    if (window.AdProvider) serve();
    else loadScriptOnce("cm-exo-provider", EXO_PROVIDER, serve);
  }

  function armAdcash(slot, unit) {
    if (slot.dataset.cmArmed === "true") return;
    slot.dataset.cmArmed = "true";
    function serve() {
      try {
        if (window.aclib && typeof window.aclib.runBanner === "function") {
          window.aclib.runBanner({ zoneId: unit.zone });
        }
      } catch (error) {
        slot.dataset.cmAdError = "provider";
      }
    }
    if (window.aclib && typeof window.aclib.runBanner === "function") serve();
    else loadScriptOnce("aclib", "https://acscdn.com/script/aclib.js", serve);
  }

  function arm(slot, unit) {
    if (unit.key === "adcash") armAdcash(slot, unit);
    else armExo(slot, unit);
  }

  var placing = false;
  function place() {
    if (placing) return;
    var list = cards();
    if (list.length < 2) return;
    placing = true;
    units.forEach(function (unit) {
      var slot = ensure(unit);
      var at = Math.min(list.length - 1, Math.max(0, Math.round(list.length * unit.fraction) - 1));
      var card = list[at];
      if (card && slot.previousElementSibling !== card) card.after(slot);
      arm(slot, unit);
    });
    placing = false;
  }

  var roots = ["#nationalEvents", "#concertGroups", "#deadlineGroups", "#archiveGroups", "#archiveEvents"]
    .map(function (selector) { return document.querySelector(selector); })
    .filter(Boolean);
  var observer = new MutationObserver(function () {
    if (!placing) place();
  });
  roots.forEach(function (root) { observer.observe(root, { childList: true, subtree: true }); });
  place();
  setTimeout(place, 500);
  setTimeout(place, 1600);
})();
