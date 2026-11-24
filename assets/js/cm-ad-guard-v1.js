/* I banner restano in pagina. I popunder no: niente nuove schede e niente dirottamenti. */
(function () {
  "use strict";
  var pop = /theconsumersearch|journeys-finds|consumersearch\.com|popads|popcash|propellerads|onclickmax|onclkds|clickadu/i;
  function bad(url) {
    return pop.test(String(url || ""));
  }
  window.open = function () { return null; };
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
