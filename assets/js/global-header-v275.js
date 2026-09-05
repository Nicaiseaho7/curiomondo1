/* CurioMondo v275 — tema dell'intestazione interna unica. */
(() => {
  'use strict';
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
