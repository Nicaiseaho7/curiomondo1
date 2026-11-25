/* Blocca i popunder, conserva i banner e impedisce gli spazi pubblicitari vuoti. */
(function () {
  "use strict";
  var pop = /sectrav|theconsumersearch|journeys-finds|consumersearch\.com|popads|popcash|propellerads|onclickmax|onclkds|clickadu|popunder/i;

  window.open = function () { return null; };

  function killRedirects(node) {
    if (!node || node.nodeType !== 1) return;
    var src = node.getAttribute && (node.getAttribute("src") || "");
    if (/magsrv\.com|ad-provider\.js|bauval\.org|acscdn\.com/i.test(src)) node.remove();
  }

  var origClick = HTMLElement.prototype.click;
  HTMLElement.prototype.click = function () {
    if (this && this.tagName === "A") {
      var href = this.getAttribute("href") || "";
      var blank = (this.getAttribute("target") || "") === "_blank";
      if (blank || pop.test(href)) return;
    }
    return origClick.apply(this, arguments);
  };

  function disarm(node) {
    if (!node || node.nodeType !== 1) return;
    if (node.tagName === "IFRAME") {
      var sandbox = node.getAttribute("sandbox") || "";
      if (/allow-popups|allow-top-navigation/.test(sandbox)) node.setAttribute("sandbox", "allow-scripts");
    }
    if (node.tagName !== "SCRIPT") return;
    var src = node.getAttribute("src") || "";
    var code = node.textContent || "";
    if (pop.test(src) || /theconsumersearch|journeys-finds|sectrav|runVideoSlider|12488470/.test(code)) node.remove();
  }

  new MutationObserver(function (list) {
    list.forEach(function (record) {
      record.addedNodes.forEach(function (node) {
        disarm(node);
        killRedirects(node);
        if (node.querySelectorAll) node.querySelectorAll("iframe,script").forEach(function (child) {
          disarm(child);
          killRedirects(child);
        });
      });
    });
  }).observe(document.documentElement, { childList: true, subtree: true });
  document.querySelectorAll("iframe,script").forEach(function (node) {
    disarm(node);
    killRedirects(node);
  });
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
