/* Mantiene un solo Native Banner e lo colloca fra le schede, senza duplicati. */
(function () {
  "use strict";

  if (!/^\/(scioperi|concerti|scadenze)(\/|$)/.test(location.pathname)) return;

  var CONTAINER_ID = "container-81e6446ad1091f193a3bcc8fbb538b94";
  var SOURCE = "https://bauval.org/21/81e6446ad1091f193a3bcc8fbb538b94";

  function existingSlot() {
    var nodes = Array.from(document.querySelectorAll('[data-cm-ad="native"], [data-cm-native-slot]'));
    var slot = nodes.shift();
    nodes.forEach(function (extra) { extra.remove(); });
    return slot || null;
  }

  function createSlot() {
    var slot = document.createElement("aside");
    slot.className = "cm-safe-ad cm-native-banner-slot";
    slot.setAttribute("data-cm-ad", "native");
    slot.setAttribute("data-cm-native-slot", "");
    slot.setAttribute("aria-label", "Pubblicita");
    var box = document.createElement("div");
    box.id = CONTAINER_ID;
    box.className = "cm-native-banner";
    slot.appendChild(box);
    return slot;
  }

  var slot = existingSlot() || createSlot();
  slot.setAttribute("data-cm-native-slot", "");

  function arm() {
    if (slot.dataset.cmArmed === "true") return;
    if (slot.querySelector("iframe")) {
      slot.dataset.cmArmed = "true";
      return;
    }
    var box = slot.querySelector("#" + CONTAINER_ID);
    if (!box) {
      box = document.createElement("div");
      box.id = CONTAINER_ID;
      box.className = "cm-native-banner";
      slot.appendChild(box);
    }
    if (!document.querySelector('script[src="' + SOURCE + '"]')) {
      var script = document.createElement("script");
      script.async = true;
      script.src = SOURCE;
      script.setAttribute("data-cfasync", "false");
      box.before(script);
    }
    slot.dataset.cmArmed = "true";
  }

  function candidates() {
    if (/^\/scioperi(\/|$)/.test(location.pathname)) {
      return Array.from(document.querySelectorAll("#nationalEvents > .event-card, #archiveEvents > .event-card"));
    }
    if (/^\/concerti(\/|$)/.test(location.pathname)) {
      return Array.from(document.querySelectorAll("#concertGroups .event-card, #archiveGroups .event-card"));
    }
    return Array.from(document.querySelectorAll("#deadlineGroups .deadline-card, #archiveGroups .deadline-card"));
  }

  var placing = false;
  function place() {
    if (placing) return;
    placing = true;
    var list = candidates();
    if (list.length >= 2) {
      var anchor = list[Math.max(0, Math.round(list.length * 0.46) - 1)];
      if (slot.previousElementSibling !== anchor) anchor.after(slot);
      arm();
    } else {
      var footer = document.querySelector("footer.site-footer");
      var main = document.querySelector("main");
      if (!slot.isConnected) {
        if (footer) footer.before(slot);
        else if (main) main.appendChild(slot);
      }
      arm();
    }
    placing = false;
  }

  var roots = ["#nationalEvents", "#archiveEvents", "#concertGroups", "#archiveGroups", "#deadlineGroups"]
    .map(function (selector) { return document.querySelector(selector); })
    .filter(Boolean);
  var observer = new MutationObserver(function () { if (!placing) place(); });
  roots.forEach(function (root) { observer.observe(root, { childList: true, subtree: true }); });
  place();
  setTimeout(place, 500);
  setTimeout(place, 1600);
})();
