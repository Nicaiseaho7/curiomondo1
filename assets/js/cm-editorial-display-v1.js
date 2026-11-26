/* CurioMondo: display consent-based, isolated, no popup format. */
(function () {
  "use strict";
  var selector = "aside[data-cm-editorial-banner]";
  var managed = new Map();
  var style = document.createElement("style");
  style.textContent =
    'aside[data-cm-editorial-banner]:not([data-cm-ad-filled="1"]){max-height:1px!important;height:1px!important;min-height:0!important;margin:0!important;padding:0!important;overflow:hidden!important;visibility:hidden!important;transition:none!important}' +
    'aside[data-cm-editorial-banner][data-cm-ad-filled="1"]{transition:none!important}' +
    'aside[data-cm-editorial-banner] iframe{max-width:100%!important}.cm-editorial-banner{display:block;box-sizing:border-box;clear:both;width:100%;text-align:center;margin:20px auto}';
  document.head.appendChild(style);

  function reportCreative(token, site) {
    let last;
    const eligible = (e) => {
      const r = e.getBoundingClientRect(), cs = getComputedStyle(e);
      if (r.width < 45 || r.height < 24 || cs.display === "none" ||
          cs.visibility === "hidden" || Number(cs.opacity) === 0) return false;
      if (e.tagName === "IMG") return e.complete && e.naturalWidth >= 45 && e.naturalHeight >= 24;
      
      if (e.tagName === "IFRAME") return e.dataset.cmChildLoaded === "1" &&
        /^https?:/i.test(e.getAttribute("src") || "");
      return false;
    };
    function signal() {
      const ready = [...document.querySelectorAll("iframe,img")].some(eligible);
      if (last === ready) return;
      last = ready;
      parent.postMessage({type:"cm-editorial-banner", token, ready}, site);
    }
    document.addEventListener("load", (e) => {
      if (e.target.tagName === "IFRAME") e.target.dataset.cmChildLoaded = "1";
      signal();
    }, true);
    document.addEventListener("loadeddata", signal, true);
    new MutationObserver(signal).observe(document.documentElement,{childList:true,subtree:true,attributes:true});
    signal();
  }

  function widthFits(state) {
    return state.slot.clientWidth >= state.minWidth;
  }

  function setFilled(state, value) {
    const flag = value ? "1" : "0";
    if (state.slot.getAttribute("data-cm-ad-filled") !== flag)
      state.slot.setAttribute("data-cm-ad-filled", flag);
  }

  function permitted() {
    const status = document.documentElement.dataset.consentMarketing;
    if (status !== undefined) return status === "granted";
    // Some article templates do not contain the consent dialog. Read, never
    // create, the same site-wide choice already made on another CurioMondo page.
    try {
      const saved = JSON.parse(localStorage.getItem("cm_consent_v2"));
      return Boolean(saved && saved.version === "2026-08-06" &&
        ["preferences","analytics","marketing","external"].every(k => typeof saved[k] === "boolean") &&
        saved.marketing === true);
    } catch (_) { return false; }
  }

  function reconcile(state) {
    if (!permitted() || !widthFits(state)) {
      setFilled(state, false);
      if (state.frame) { state.frame.remove(); state.frame = null; }
      return;
    }
    if (!state.near || state.frame) return;
    const frame = document.createElement("iframe");
    frame.setAttribute("sandbox", "allow-scripts");
    frame.setAttribute("referrerpolicy", "strict-origin-when-cross-origin");
    frame.setAttribute("title","Pubblicità");
    frame.width = state.width;
    frame.height = state.height;
    frame.style.cssText = "border:0;display:block;margin:0 auto;max-width:100%";
    state.token = crypto.randomUUID();
    state.frame = frame;
    const bridge = "<script>(" + reportCreative.toString() + ")(" +
      JSON.stringify(state.token) + "," + JSON.stringify(location.origin) + ");</scr" + "ipt>";
    frame.srcdoc = state.source.replace(/<body\b[^>]*>/i, match => match + bridge);
    state.slot.append(frame);
  }

  window.addEventListener("message", e => {
    const m = e.data;
    if (e.origin !== "null" || !m || m.type !== "cm-editorial-banner" || typeof m.ready !== "boolean") return;
    for (const state of managed.values()) {
      if (state.frame && e.source === state.frame.contentWindow && m.token === state.token) {
        setFilled(state, m.ready && permitted() && widthFits(state));
        return;
      }
    }
  });

  const io = "IntersectionObserver" in window ? new IntersectionObserver(entries => {
    for (const entry of entries) {
      const state = managed.get(entry.target);
      if (state && entry.isIntersecting) { state.near = true; reconcile(state); }
    }
  }, {rootMargin:"600px 0px"}) : null;

  function start() {
    for (const slot of document.querySelectorAll(selector)) {
      const placeholder = slot.querySelector("iframe[data-cm-ad-srcdoc]");
      if (!placeholder) continue;
      const source = placeholder.getAttribute("data-cm-ad-srcdoc");
      const width = Number(placeholder.getAttribute("width"));
      const height = Number(placeholder.getAttribute("height"));
      if (!source || !/<body\b/i.test(source) || !width || !height) continue;
      // Only the native arrangement is responsive; fixed creatives must fit.
      const minWidth = width;
      const state = {slot,source,width,height,minWidth,near:!io,frame:null};
      placeholder.remove();
      managed.set(slot,state);
      if (io) io.observe(slot);
      reconcile(state);
    }
    const all = () => managed.forEach(reconcile);
    window.addEventListener("resize", all, {passive:true});
    window.addEventListener("storage", e => {
      if (e.key === "cm_consent_v2" || e.key === null) {
        // The current tab's marker may predate a change in another tab.
        try {
          const other = JSON.parse(localStorage.getItem("cm_consent_v2"));
          if (!other || other.marketing !== true)
            document.documentElement.dataset.consentMarketing = "denied";
        } catch (_) { document.documentElement.dataset.consentMarketing = "denied"; }
        all();
      }
    });
    new MutationObserver(all).observe(document.documentElement,
      {attributes:true,attributeFilter:["data-consent-marketing"]});
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded",start);
  else start();
})();
