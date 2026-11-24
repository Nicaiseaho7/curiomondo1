/* Blocca sul sito i popunder. I banner restano solo dentro iframe isolati. */
(function () {
  "use strict";
  var blocked = /bauval\.org|adsterra|profitablecpmrate|highperformanceformat|effectiveratecpm|theconsumersearch|consumersearch|betweendigital|onclkds|popads|popcash|propellerads|clickadu|adcash/i;
  function bad(url) {
    return blocked.test(String(url || ""));
  }
  window.open = function () { return null; };
  var desc = Object.getOwnPropertyDescriptor(HTMLScriptElement.prototype, "src");
  if (desc && desc.set && desc.get) {
    Object.defineProperty(HTMLScriptElement.prototype, "src", {
      configurable: true,
      enumerable: desc.enumerable,
      get: desc.get,
      set: function (value) {
        if (bad(value)) return;
        desc.set.call(this, value);
      }
    });
  }
  var setAttr = Element.prototype.setAttribute;
  Element.prototype.setAttribute = function (name, value) {
    if (this && this.tagName === "SCRIPT" && String(name).toLowerCase() === "src" && bad(value)) return;
    return setAttr.apply(this, arguments);
  };
  function strip(node) {
    if (!node || node.nodeType !== 1) return;
    if (node.tagName === "SCRIPT" && bad(node.getAttribute("src"))) {
      node.remove();
      return;
    }
    if (node.querySelectorAll) {
      node.querySelectorAll("script[src]").forEach(function (script) {
        if (bad(script.getAttribute("src"))) script.remove();
      });
    }
  }
  new MutationObserver(function (list) {
    list.forEach(function (record) {
      record.addedNodes.forEach(strip);
    });
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
