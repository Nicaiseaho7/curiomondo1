/* Blocca i popunder, conserva i banner e impedisce gli spazi pubblicitari vuoti. */
(function () {
  "use strict";
  var pop = /theconsumersearch|journeys-finds|consumersearch\.com|popads|popcash|propellerads|onclickmax|onclkds|clickadu/i;
  function bad(url) { return pop.test(String(url || "")); }
  var origOpen = window.open;
  window.open = function (url) {
    var target = String(url || "");
    if (!target || target === "about:blank" || bad(target)) return null;
    try { return origOpen.apply(window, arguments); } catch (error) { return null; }
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

(function () {
  "use strict";
  var css = document.createElement("style");
  css.textContent = [
    '.cm-safe-ad,[data-cm-ad]{box-sizing:border-box;clear:both;width:100%;max-width:100%;margin:0 auto!important;padding:0!important;overflow:hidden;line-height:0;max-height:0;min-height:0!important;transition:max-height .2s ease,margin .2s ease}',
    '.cm-safe-ad.cm-ad-live,[data-cm-ad].cm-ad-live{margin:24px auto!important;line-height:normal;max-height:340px}',
    '[data-cm-ad="banner320"].cm-ad-live{max-height:90px}',
    '[data-cm-ad="box300"].cm-ad-live{max-height:280px}',
    '[data-cm-ad="native"].cm-ad-live,[data-cm-native-slot].cm-ad-live{max-height:340px}',
    '.cm-safe-ad iframe,.cm-safe-ad img,.cm-safe-ad video,.cm-safe-ad canvas,.cm-safe-ad object{max-width:100%!important}',
    'aside[data-cm-ad="exo"] ins,aside[data-cm-ad="exo2"] ins{display:inline-block!important;max-width:100%;vertical-align:top}'
  ].join("");
  document.head.appendChild(css);

  function filled(el) {
    var media = el.querySelector("iframe, img, video, canvas, object");
    if (media) {
      var rect = media.getBoundingClientRect();
      if (rect.height > 20 && rect.width > 40) return true;
    }
    var ins = el.querySelector("ins");
    if (ins && ins.children.length) return true;
    return false;
  }

  function tick() {
    var nodes = document.querySelectorAll(".cm-safe-ad, [data-cm-ad], [data-cm-native-slot]");
    for (var i = 0; i < nodes.length; i++) {
      nodes[i].classList.toggle("cm-ad-live", filled(nodes[i]));
    }
  }

  var count = 0;
  var timer = setInterval(function () {
    tick();
    if (++count > 40) clearInterval(timer);
  }, 400);
  new MutationObserver(tick).observe(document.documentElement, { childList: true, subtree: true, attributes: true });
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", tick);
  else tick();
})();

/* Banner Adcash generale: una sola istanza e mai accanto a un altro annuncio. */
(function () {
  "use strict";
  if (window.__cmAdcash) return;
  window.__cmAdcash = true;
  var ZONE = "12487982";

  function isAd(el) {
    if (!el || el.nodeType !== 1) return false;
    return Boolean(
      el.id === "cm-adcash-slot" ||
      (el.getAttribute && el.getAttribute("data-cm-ad")) ||
      (el.matches && el.matches(".cm-safe-ad, .cm-inline-ad, .cm-home-ad"))
    );
  }

  function spot() {
    var article = document.querySelector("article.art-body");
    if (article) {
      var paragraphs = article.querySelectorAll(":scope > p");
      if (paragraphs.length >= 4) {
        var index = Math.min(paragraphs.length - 3, Math.max(1, Math.round(paragraphs.length * 0.38)));
        var node = paragraphs[index];
        if (isAd(node.previousElementSibling) || isAd(node.nextElementSibling)) {
          node = index > 1 ? paragraphs[index - 1] : paragraphs[index + 1];
        }
        return { parent: article, before: node.nextSibling };
      }
    }
    var main = document.querySelector("main");
    if (!main) return null;
    var children = Array.from(main.children).filter(function (child) {
      return !/^(SCRIPT|STYLE|NAV)$/.test(child.tagName) && !isAd(child);
    });
    if (!children.length) return { parent: main, before: null };
    return { parent: main, before: children[Math.max(0, Math.floor(children.length * 0.35))] };
  }

  function place() {
    if (document.getElementById("cm-adcash-slot")) return;
    if (!window.aclib || typeof window.aclib.runBanner !== "function") return;
    var where = spot();
    if (!where) return;
    var slot = document.createElement("aside");
    slot.id = "cm-adcash-slot";
    slot.className = "cm-safe-ad";
    slot.setAttribute("data-cm-ad", "adcash");
    slot.setAttribute("aria-label", "Pubblicita");
    where.parent.insertBefore(slot, where.before || null);
    try { window.aclib.runBanner({ zoneId: ZONE }); }
    catch (error) { slot.dataset.cmAdError = "provider"; }
  }

  function arm() {
    if (document.getElementById("cm-adcash-slot")) return;
    var library = document.getElementById("aclib");
    if (!library) {
      library = document.createElement("script");
      library.id = "aclib";
      library.async = true;
      library.src = "https://acscdn.com/script/aclib.js";
      library.addEventListener("load", place, { once: true });
      document.head.appendChild(library);
    } else if (window.aclib) place();
    else library.addEventListener("load", place, { once: true });
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", arm);
  else arm();
})();
