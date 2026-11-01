/* CurioMondo v275 — tema dell'intestazione interna unica. */
(() => {
  'use strict';
  const restore = document.createElement("style");
  restore.id = "cm-inner-brand-restore";
  restore.textContent = `
    .cm-global-header__brand,
    .cm-global-header__brand span[aria-hidden]{
      color:#fff!important;
      -webkit-text-fill-color:#fff!important;
      font-weight:700!important;
      font-size:clamp(1.85rem,6.6vw,2.28rem)!important;
      letter-spacing:-.03em!important;
      line-height:.92!important;
      text-shadow:0 1px 0 #031020,0 2px 6px rgba(3,16,32,.55)!important;
    }
    .cm-global-header__brand span span{
      color:#245fd6!important;
      -webkit-text-fill-color:#245fd6!important;
    }
    @media(max-width:600px){
      .cm-global-header__brand{font-size:clamp(1.58rem,7.2vw,1.82rem)!important}
    }
  `;
  document.head.appendChild(restore);

  document.querySelectorAll('.cm-global-header__brand').forEach((link) => {
    link.addEventListener('click', (event) => {
      event.preventDefault();
      event.stopPropagation();
      try {
        sessionStorage.removeItem('cm_menu_return');
        sessionStorage.setItem('cm_skip_menu', '1');
      } catch {}
      if (location.pathname === '/' || location.pathname === '/index.html') {
        location.reload();
        return;
      }
      location.assign('/');
    });
  });
  document.querySelectorAll('.cm-global-header__back').forEach((link) => {
    link.addEventListener('click', (event) => {
      let same = false;
      try { same = new URL(document.referrer).origin === location.origin; } catch {}
      if (same && history.length > 1) {
        event.preventDefault();
        history.back();
      }
    });
  });
  const button=document.querySelector('[data-cm-global-theme]');
  if(!button)return;
  const root=document.documentElement;
  const icon=button.querySelector('[aria-hidden="true"]');
  const read=()=>{try{return localStorage.getItem('cm_theme')==='dark';}catch{return root.classList.contains('cm-dark')||root.classList.contains('dark');}};
  const apply=dark=>{
    root.classList.toggle('cm-dark',dark);
    root.classList.toggle('dark',dark);
    document.body?.classList.toggle('dark',dark);
    button.setAttribute('aria-pressed',String(dark));
    button.setAttribute('aria-label',dark?'Attiva modalità chiara':'Attiva modalità scura');
    if(icon)icon.textContent=dark?'☀':'☾';
  };
  apply(read());
  button.addEventListener('click',()=>{
    const dark=!root.classList.contains('cm-dark');
    try{localStorage.setItem('cm_theme',dark?'dark':'light');}catch{}
    apply(dark);
  });
  window.addEventListener('storage',event=>{if(event.key==='cm_theme')apply(read());});
})();
