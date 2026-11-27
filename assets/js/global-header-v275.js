/* CurioMondo v275 — tema dell'intestazione interna unica. */
(() => {
  'use strict';
  if (navigator.serviceWorker) {
    navigator.serviceWorker.getRegistrations().then((regs) => {
      regs.forEach((reg) => { reg.unregister(); });
    }).catch(() => {});
  }
  const brandSheet='/assets/css/curiomondo-brand-unified-v1.css';
  const headers=[...document.querySelectorAll('header.cm-global-header')];
  if(headers.length&&!document.querySelector('link[href="'+brandSheet+'"]')){
    const css=document.createElement('link');
    css.rel='stylesheet';css.href=brandSheet;document.head.append(css);
  }
  for(const header of headers){
    const brand=header.querySelector('.cm-global-header__brand');
    const nav=header.querySelector('.cm-global-header__inner');
    if(!brand||!nav||header.dataset.cmBrandUnified)continue;
    const part=(name, cls='', value='')=>{
      const n=document.createElement(name);
      if(cls)n.className=cls;if(value)n.textContent=value;
      return n;
    };
    const img=part('img','cm-global-unified-logo');
    img.src='/assets/images/curiomondo-logo-circle-v715-96.webp?v=715';
    img.alt='';img.width=47;img.height=47;img.decoding='async';
    const copy=part('span','cm-global-unified-copy');
    const word=part('span','cm-global-unified-word');word.setAttribute('aria-hidden','true');
    word.append(part('b','', 'Curio'),part('i','', 'Mondo'));
    const line=part('small','cm-global-unified-tagline','Notizie, curiosità e approfondimenti dall’Italia e dal mondo');
    line.setAttribute('aria-hidden','true');copy.append(word,line);
    brand.replaceChildren(img,copy);
    brand.setAttribute('aria-label','CurioMondo, torna alla home');
    header.dataset.cmBrandUnified='v1';
  }

  const area=location.pathname.split('/').filter(Boolean)[0]?.replace(/\.html$/,'');
  if(['concerti','scadenze','approfondimenti'].includes(area)&&document.querySelector('main')){
    document.documentElement.dataset.cmPremiumLayout=area;
    const href='/assets/css/'+area+'-premium-v1.css';
    if(!document.querySelector('link[href="'+href+'"]')){
      const edition=document.createElement('link');edition.rel='stylesheet';edition.href=href;document.head.append(edition);
    }
  }

  const categoryPage=document.querySelector('main.category-shell');
  const categorySlug=location.pathname.match(/^\/categorie\/([a-z-]+)(?:\/|$)/)?.[1];
  if(categoryPage&&categorySlug){
    const css=document.createElement('link');css.rel='stylesheet';css.href='/assets/css/category-edition-v1.css';document.head.append(css);
    categoryPage.dataset.cmCategoryEdition=categorySlug;
    const first=categoryPage.querySelector('.category-list>li:first-child .category-card-copy');
    if(first){const kicker=document.createElement('span');kicker.className='category-feature-kicker';kicker.textContent='In apertura';first.prepend(kicker);}
  }

  document.querySelectorAll('.cm-global-header__brand').forEach((link) => {
    link.addEventListener('click', (event) => {
      if (event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
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
      if (event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
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
