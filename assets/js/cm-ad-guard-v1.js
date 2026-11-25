/* Blocca i popunder, conserva i banner e impedisce gli spazi pubblicitari vuoti. */
(function () {
  "use strict";
  var pop = /sectrav|theconsumersearch|journeys-finds|consumersearch\.com|popads|popcash|propellerads|onclickmax|onclkds|clickadu|popunder/i;

  window.open = function () { return null; };

  function killRedirects(node) {
    if (!node || node.nodeType !== 1) return;
    var src = node.getAttribute && (node.getAttribute("src") || "");
    if (/magsrv\.com|ad-provider\.js|bauval\.org|acscdn\.com/i.test(src)) node.remove();
    if (node.tagName === "SCRIPT" && /atOptions|aclib\.runBanner|runVideoSlider/.test(node.textContent || "")) node.remove();
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
    '.cm-safe-ad,[data-cm-ad]{box-sizing:border-box;clear:both;width:100%;max-width:100%;margin:22px auto!important;padding:0!important;overflow:visible;line-height:normal;text-align:center}',
    '[data-cm-ad="banner320"]{min-height:50px}',
    '[data-cm-ad="banner468"]{min-height:60px}',
    '[data-cm-ad="box300"]{min-height:250px}',
    '[data-cm-ad="adcash"]{min-height:120px}',
    '[data-cm-ad="native"],[data-cm-native-slot]{min-height:250px}',
    '.cm-safe-ad iframe,.cm-safe-ad img,.cm-safe-ad video,.cm-safe-ad canvas,.cm-safe-ad object{max-width:100%!important;margin-left:auto;margin-right:auto}'
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

/* v18: isolated inline banners. Templates are inert until marketing is allowed. */
(function () {
  "use strict";
  const selector = '[data-cm-inline="1"]';
  const states = new Map();
  const style = document.createElement("style");
  style.textContent =
    '[data-cm-inline="disabled"]{display:none!important}' +
    '[data-cm-inline="1"]{display:block!important;width:100%!important;max-width:100%!important;box-sizing:border-box!important;clear:both!important;overflow:hidden!important;text-align:center!important;padding:0!important;transition:none!important}' +
    '[data-cm-inline="1"]:not([data-cm-inline-ready="1"]){height:1px!important;max-height:1px!important;min-height:0!important;margin:0!important;visibility:hidden!important}' +
    '[data-cm-inline="1"][data-cm-inline-ready="1"]{height:auto!important;max-height:none!important;min-height:0!important;margin:22px auto!important;visibility:visible!important}' +
    '[data-cm-inline="1"]>iframe{display:block!important;max-width:100%!important;margin:0 auto!important;border:0!important}';
  document.head.append(style);

  function report(token, parentOrigin) {
    const loaded = new WeakSet();
    let previous;
    function scan() {
      const ready = Array.from(document.querySelectorAll("iframe,img,video,canvas")).some(node => {
        const r = node.getBoundingClientRect(), s = getComputedStyle(node);
        if (r.width < 120 || r.height < 24 || s.display === "none" || s.visibility === "hidden" || Number(s.opacity) === 0) return false;
        if (node.tagName === "IMG") return node.complete && node.naturalWidth >= 120 && node.naturalHeight >= 24;
        if (node.tagName === "VIDEO") return node.readyState >= 2;
        if (node.tagName === "CANVAS") return false;
        return loaded.has(node) && (/^https?:\/\//i.test(node.getAttribute("src") || "") ||
          /^\/\//.test(node.getAttribute("src") || ""));
      });
      if (previous !== ready) {
        previous = ready;
        parent.postMessage({type:"cm-inline-banner-v18",token,ready},parentOrigin);
      }
    }
    document.addEventListener("load", e => { if (e.target.tagName === "IFRAME") loaded.add(e.target); scan(); }, true);
    document.addEventListener("error", e => { loaded.delete(e.target); scan(); }, true);
    document.addEventListener("loadeddata",scan,true);
    window.addEventListener("resize", scan);
    new MutationObserver(scan).observe(document.documentElement,{subtree:true,childList:true,attributes:true});
    scan();
  }

  function permitted() {
    const marker = document.documentElement.dataset.consentMarketing;
    if (marker !== undefined) return marker === "granted";
    try {
      const data = JSON.parse(localStorage.getItem("cm_consent_v2"));
      return !!(data && data.version === "2026-08-06" &&
        ["preferences","analytics","marketing","external"].every(k => typeof data[k] === "boolean") &&
        data.marketing === true);
    } catch (_) { return false; }
  }
  function fit(s) { return s.slot.clientWidth >= s.minimum; }
  function show(s, ready) {
    s.slot.dataset.cmInlineReady = ready ? "1" : "0";
    if (s.frame) s.frame.setAttribute("aria-hidden", ready ? "false" : "true");
  }
  function mount(s) {
    if (!permitted() || !fit(s)) {
      if (s.frame) { s.frame.remove(); s.frame=null; }
      if (s.slot.dataset.cmInlineReady !== "0") show(s,false);
      return;
    }
    if (!s.near || s.frame || !window.crypto || !crypto.getRandomValues) return;
    const f=document.createElement("iframe");
    const bytes=crypto.getRandomValues(new Uint32Array(4));
    s.token=Array.from(bytes,x=>x.toString(16).padStart(8,"0")).join("");
    f.setAttribute("sandbox","allow-scripts");
    f.setAttribute("referrerpolicy","strict-origin-when-cross-origin");
    f.setAttribute("title","Pubblicità");
    f.setAttribute("aria-hidden","true");
    f.width=s.width;
    f.height=s.height;
    const hook="<script>("+report.toString()+")("+JSON.stringify(s.token)+","+JSON.stringify(location.origin)+");</scr"+"ipt>";
    f.srcdoc=s.src.replace(/<body\b[^>]*>/i,tag=>tag+hook);
    s.frame=f;
    s.slot.append(f);
  }

  const io="IntersectionObserver" in window ? new IntersectionObserver(entries=>{
    for (const e of entries) {
      const s=states.get(e.target);
      if(s && e.isIntersecting){s.near=true;mount(s);}
    }
  }, {rootMargin:"550px 0px"}) : null;
  const ro="ResizeObserver" in window ? new ResizeObserver(entries=>{
    for(const e of entries){const s=states.get(e.target);if(s)mount(s);}
  }) : null;
  window.addEventListener("message",e=>{
    const m=e.data;
    if(e.origin!=="null" || !m || m.type!=="cm-inline-banner-v18" || typeof m.ready!=="boolean")return;
    for(const s of states.values())if(s.frame && e.source===s.frame.contentWindow && m.token===s.token) {
      show(s,m.ready && permitted() && fit(s));break;
    }
  });
  function start() {
    for(const slot of document.querySelectorAll(selector)) {
      const source=slot.querySelector("template[data-cm-inline-source]");
      if(!source)continue;
      const src=source.getAttribute("data-cm-html");
      const width=Number(slot.dataset.cmInlineWidth),height=Number(slot.dataset.cmInlineHeight);
      if(!src || !/<body\b/i.test(src) || ![300,320,336,360,468].includes(width) || ![50,60,250,300,420].includes(height))continue;
      const s={slot,src,width,height,minimum:slot.dataset.cmAd==="native"?280:width,frame:null,near:!io};
      states.set(slot,s);
      if(io)io.observe(slot);
      if(ro)ro.observe(slot);
      mount(s);
    }
    const all=()=>states.forEach(mount);
    window.addEventListener("resize",all,{passive:true});
    window.addEventListener("storage",e=>{
      if(e.key!=="cm_consent_v2"&&e.key!==null)return;
      try {
        const x=JSON.parse(localStorage.getItem("cm_consent_v2"));
        if (!x || x.marketing!==true) document.documentElement.dataset.consentMarketing="denied";
      } catch (_) { document.documentElement.dataset.consentMarketing="denied"; }
      all();
    });
    window.addEventListener("pageshow",all);
    new MutationObserver(all).observe(document.documentElement,{attributes:true,attributeFilter:["data-consent-marketing"]});
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",start);
  else start();
})();
