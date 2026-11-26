/* Blocca i popup. I banner restano visibili in pagina. */
(function () {
  "use strict";

  function badUrl(value) {
    var url = String(value || "");
    if (!url) return false;
    if (/sectrav|theconsumersearch|journeys-finds|consumersearch\.com|popads|popcash|propellerads|onclickmax|onclkds|clickadu|popunder/i.test(url)) return true;
    if (/magsrv\.com|ad-provider/i.test(url)) return true;
    if (/bauval\.org\/14\//i.test(url)) return true;
    if (/acscdn\.com/i.test(url) && !/aclib\.js/i.test(url)) return true;
    if (/12488470|runVideoSlider/i.test(url)) return true;
    return false;
  }

  function badCode(code) {
    return /runVideoSlider|12488470|magsrv\.com|ad-provider|sectrav|theconsumersearch|popunder/i.test(code || "");
  }

  function blockOpen() { return null; }
  try {
    Object.defineProperty(window, "open", { configurable: false, writable: false, value: blockOpen });
  } catch (error) {
    window.open = blockOpen;
  }

  /* I banner Adsterra usano document.write. Su iPhone quel comando non disegna:
     il risultato viene inserito subito dopo lo script, dentro il riquadro. */
  document.write = function () {
    var html = Array.prototype.slice.call(arguments).join("");
    var current = document.currentScript;
    var holder = document.createElement("div");
    holder.innerHTML = html;
    var nodes = Array.prototype.slice.call(holder.childNodes);
    var anchor = current && current.parentNode ? current : null;
    nodes.forEach(function (node) {
      var next = node;
      if (node.tagName === "SCRIPT") {
        next = document.createElement("script");
        if (node.src) next.src = node.src;
        else next.text = node.textContent || "";
        next.setAttribute("data-cfasync", "false");
      }
      if (anchor) anchor.parentNode.insertBefore(next, anchor.nextSibling);
      else document.body.appendChild(next);
      anchor = next;
    });
  };
  document.writeln = function () {
    document.write(Array.prototype.slice.call(arguments).join("") + "\n");
  };

  function kill(node) {
    if (!node || node.nodeType !== 1) return;
    var src = node.getAttribute ? (node.getAttribute("src") || "") : "";
    var code = node.textContent || "";
    if (node.tagName === "SCRIPT" && (badUrl(src) || badCode(code))) {
      node.remove();
      return;
    }
    if (node.tagName === "IFRAME") {
      var sandbox = node.getAttribute("sandbox") || "";
      if (/allow-popups|allow-top-navigation/.test(sandbox)) node.setAttribute("sandbox", "allow-scripts");
      if (badUrl(src) || badUrl(node.getAttribute("srcdoc") || "")) node.remove();
    }
  }

  new MutationObserver(function (list) {
    list.forEach(function (record) {
      record.addedNodes.forEach(function (node) {
        kill(node);
        if (node.querySelectorAll) node.querySelectorAll("script,iframe").forEach(kill);
      });
    });
  }).observe(document.documentElement, { childList: true, subtree: true });

  document.addEventListener("click", function (event) {
    var link = event.target && event.target.closest ? event.target.closest("a") : null;
    if (!link) return;
    if (badUrl(link.getAttribute("href") || "")) {
      event.preventDefault();
      event.stopPropagation();
    }
  }, true);

  if (window.navigation && navigation.addEventListener) {
    navigation.addEventListener("navigate", function (event) {
      var url = event.destination && event.destination.url;
      if (badUrl(url)) event.preventDefault();
    });
  }
})();

(function () {
  "use strict";
  var css = document.createElement("style");
  css.textContent = [
    '.cm-safe-ad,[data-cm-ad]{box-sizing:border-box;clear:both;width:100%;max-width:100%;margin:22px auto!important;padding:0!important;overflow:visible;line-height:normal;text-align:center}',
    '[data-cm-ad="banner320"]{min-height:50px}',
    '[data-cm-ad="banner468"]{min-height:60px}',
    '[data-cm-ad="box300"]{min-height:250px}',
    '[data-cm-ad="adcash"]{min-height:90px}',
    '[data-cm-ad="native"],[data-cm-native-slot]{min-height:250px}',
    '.cm-safe-ad iframe,.cm-safe-ad img,.cm-safe-ad video,.cm-safe-ad canvas,.cm-safe-ad object{max-width:100%!important;margin-left:auto;margin-right:auto}'
  ].join("");
  document.head.appendChild(css);
})();

(function () {
  "use strict";
  if (/^\/(scioperi|concerti|scadenze)(\/|$)/.test(location.pathname)) return;

  function place() {
    var slots = Array.from(document.querySelectorAll('[data-cm-ad="native"]'));
    var slot = slots.shift();
    if (!slot) return;
    slots.forEach(function (extra) { extra.remove(); });
    var footer = document.querySelector("footer");
    if (footer && footer.parentNode) footer.parentNode.insertBefore(slot, footer);
    else (document.querySelector("main") || document.body).appendChild(slot);
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", place);
  else place();
})();
