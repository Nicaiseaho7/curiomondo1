/* CurioMondo v275 — tema dell'intestazione interna unica. */
(() => {
  'use strict';

  const brandStyle=document.createElement("style");
  brandStyle.id="cm-brand-visibility";
  brandStyle.textContent=`
    .cm-global-header__inner{min-height:82px}
    .cm-global-header__brand,
    .cm-global-header__brand span[aria-hidden]{
      color:#10233c!important;
      -webkit-text-fill-color:#10233c!important;
      font-weight:900!important;
      font-size:clamp(2.05rem,8.8vw,2.9rem)!important;
      letter-spacing:-.05em!important;
      line-height:.9!important;
      text-shadow:none!important;
    }
    .cm-global-header__brand span span{
      color:#1d4ed8!important;
      -webkit-text-fill-color:#1d4ed8!important;
      text-shadow:none!important;
    }
    html.cm-dark .cm-global-header__brand,
    html.cm-dark .cm-global-header__brand span[aria-hidden],
    html.dark .cm-global-header__brand,
    html.dark .cm-global-header__brand span[aria-hidden]{
      color:#fff!important;
      -webkit-text-fill-color:#fff!important;
    }
    html.cm-dark .cm-global-header__brand span span,
    html.dark .cm-global-header__brand span span{
      color:#8eb6ff!important;
      -webkit-text-fill-color:#8eb6ff!important;
    }
    @media(max-width:600px){
      .cm-global-header__inner{min-height:74px}
      .cm-global-header__brand{font-size:clamp(1.95rem,8.2vw,2.25rem)!important}
    }
  `;
  document.head.appendChild(brandStyle);
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
