/* Native Banner Adsterra sulle pagine di servizio, non in homepage. */
(() => {
  "use strict";
  if (!/^\/(scioperi|scadenze|concerti)(\/|$)/.test(location.pathname)) return;
  const id = "container-81e6446ad1091f193a3bcc8fbb538b94";
  if (document.getElementById(id)) return;
  const style = document.createElement("style");
  style.textContent = ".cm-native-banner-slot{width:min(1180px,calc(100% - 40px));margin:28px auto 12px}.cm-native-banner{max-width:100%;overflow:hidden;clear:both}.cm-native-banner iframe,.cm-native-banner img{max-width:100%;height:auto}";
  document.head.append(style);
  const slot = document.createElement("div");
  slot.className = "cm-native-banner-slot";
  const box = document.createElement("div");
  box.id = id;
  box.className = "cm-native-banner";
  slot.append(box);
  const footer = document.querySelector("footer.site-footer");
  const main = document.querySelector("main");
  if (footer) footer.before(slot);
  else if (main) main.append(slot);
  else return;
  const src = "https://bauval.org/21/81e6446ad1091f193a3bcc8fbb538b94";
  if (!document.querySelector('script[src="' + src + '"]')) {
    const script = document.createElement("script");
    script.async = true;
    script.fetchPriority = "high";
    script.setAttribute("data-cfasync", "false");
    script.src = src;
    box.before(script);
  }
})();
