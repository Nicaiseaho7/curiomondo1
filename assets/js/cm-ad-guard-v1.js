/* I banner restano in pagina. I popunder no: niente nuove schede e niente dirottamenti. */
(function () {
  "use strict";
  var pop = /theconsumersearch|journeys-finds|consumersearch\.com|popads|popcash|propellerads|onclickmax|onclkds|clickadu/i;
  function bad(url) {
    return pop.test(String(url || ""));
  }
  var origOpen = window.open;
  window.open = function (url) {
    var target = String(url || "");
    if (!target || target === "about:blank" || bad(target)) return null;
    try { return origOpen.apply(window, arguments); }
    catch (e) { return null; }
  };
  var origClick = HTMLElement.prototype.click;
  HTMLElement.prototype.click = function () {
    if (this && this.tagName === "A" && bad(this.getAttribute("href") || this.href)) return;
    return origClick.apply(this, arguments);
  };
  document.addEventListener("click", function (event) {
    var link = event.target && event.target.closest ? event.target.closest("a") : null;
    if (link && bad(link.getAttribute("href") || link.href)) {
      event.preventDefault();
      event.stopPropagation();
    }
  }, true);
  new MutationObserver(function (list) {
    list.forEach(function (record) {
      record.addedNodes.forEach(function (node) {
        if (!node || node.nodeType !== 1) return;
        var src = node.getAttribute && (node.getAttribute("src") || node.getAttribute("href") || "");
        var code = node.tagName === "SCRIPT" ? node.textContent || "" : "";
        if (bad(src) || /theconsumersearch|journeys-finds/i.test(code)) node.remove();
      });
    });
  }).observe(document.documentElement, { childList: true, subtree: true });
})();

/* Niente buchi bianchi: il riquadro prende spazio solo se l'annuncio è arrivato. */
(function () {
  "use strict";
  var css = document.createElement("style");
  css.textContent = [
    'aside[data-cm-ad="exo"],aside[data-cm-ad="exo2"]{display:block!important;text-align:center;clear:both;width:100%;margin:0!important;min-height:0!important;padding:0!important;line-height:0;}',
    'aside[data-cm-ad="exo"] ins,aside[data-cm-ad="exo2"] ins{display:inline-block!important;line-height:normal;vertical-align:top;max-width:100%;}',
    'aside[data-cm-ad="exo"].cm-ad-live,aside[data-cm-ad="exo2"].cm-ad-live{margin:28px auto!important;line-height:normal;}',
    '#cm-adcash-slot{margin:0!important;min-height:0!important;padding:0!important;}',
    '#cm-adcash-slot.cm-ad-live{margin:28px auto!important;}'
  ].join("");
  document.head.appendChild(css);

  function filled(el) {
    var box = el.querySelector("iframe, img, video, canvas, object");
    if (box) {
      var r = box.getBoundingClientRect();
      if (r.height > 24 && r.width > 40) return true;
    }
    return el.scrollHeight > 48;
  }
  function tick() {
    var nodes = document.querySelectorAll('aside[data-cm-ad="exo"], #cm-adcash-slot');
    for (var i = 0; i < nodes.length; i++) nodes[i].classList.toggle("cm-ad-live", filled(nodes[i]));
  }
  var n = 0;
  var timer = setInterval(function () {
    tick();
    if (++n > 24) clearInterval(timer);
  }, 500);
  new MutationObserver(tick).observe(document.documentElement, { childList: true, subtree: true });
})();

/* Banner display Adcash, una volta, prima del banner ExoClick e lontano dal Native. */
(function () {
  "use strict";
  if (window.__cmAdcash) return;
  window.__cmAdcash = true;
  var ZONE = "12487982";

  function isAd(el) {
    if (!el || el.nodeType !== 1) return false;
    if (el.id === "cm-adcash-slot") return true;
    if (el.getAttribute && el.getAttribute("data-cm-ad")) return true;
    if (el.matches && el.matches(".cm-safe-ad, .cm-inline-ad, .cm-home-ad")) return true;
    if (el.querySelector && el.querySelector("[data-cm-ad='native']")) return true;
    return false;
  }

  function spot() {
    var article = document.querySelector("article.art-body");
    if (article) {
      var ps = article.querySelectorAll(":scope > p");
      if (ps.length >= 4) {
        var i = Math.min(ps.length - 3, Math.max(1, Math.round(ps.length * 0.38)));
        var node = ps[i];
        if (isAd(node.previousElementSibling) || isAd(node.nextElementSibling)) {
          if (i > 1) node = ps[i - 1];
          else if (i + 1 < ps.length - 1) node = ps[i + 1];
        }
        return { parent: article, before: node.nextSibling };
      }
    }
    var film = document.getElementById("categoria-film-tv");
    if (film && film.parentNode) return { parent: film.parentNode, before: film };
    var main = document.querySelector("main");
    if (!main) return null;
    var kids = [];
    for (var c = main.firstElementChild; c; c = c.nextElementSibling) {
      if (c.tagName !== "SCRIPT" && c.tagName !== "STYLE" && c.tagName !== "NAV") kids.push(c);
    }
    if (!kids.length) return { parent: main, before: null };
    var idx = Math.max(0, Math.floor(kids.length * 0.35));
    var guard = 0;
    while (guard < 8 && idx > 0 && (isAd(kids[idx]) || isAd(kids[idx - 1]))) {
      idx -= 1;
      guard += 1;
    }
    return { parent: main, before: kids[idx] };
  }

  function place() {
    if (document.getElementById("cm-adcash-slot")) return;
    if (!window.aclib || typeof aclib.runBanner !== "function") return;
    var where = spot();
    if (!where) return;
    var slot = document.createElement("div");
    slot.id = "cm-adcash-slot";
    slot.setAttribute("data-cm-ad", "adcash");
    slot.setAttribute("aria-label", "Pubblicita");
    slot.style.cssText = "display:block;text-align:center;clear:both;width:100%;max-width:100%;margin:0;min-height:0;";
    where.parent.insertBefore(slot, where.before || null);
    var inline = document.createElement("script");
    inline.text = "aclib.runBanner({zoneId:'" + ZONE + "'});";
    slot.appendChild(inline);
  }

  function arm() {
    var lib = document.getElementById("aclib");
    if (!lib) {
      lib = document.createElement("script");
      lib.id = "aclib";
      lib.src = "https://acscdn.com/script/aclib.js";
      lib.async = true;
      lib.onload = place;
      document.head.appendChild(lib);
      return;
    }
    if (window.aclib) place();
    else lib.addEventListener("load", place);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", arm);
  else arm();
})();
