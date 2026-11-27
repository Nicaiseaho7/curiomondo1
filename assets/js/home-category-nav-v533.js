/* La barra delle categorie resta sempre dentro la home. */
(()=>{
  const nav=document.querySelector('.cm-flow-nav');
  if(!nav)return;
  const active=()=>{
    const hash=location.hash;
    nav.querySelectorAll('a').forEach(a=>{
      const matched=hash ? a.getAttribute('href')===hash : a.getAttribute('href')==='/';
      if(matched)a.setAttribute('aria-current','location');else a.removeAttribute('aria-current');
    });
  };
  nav.addEventListener('click',e=>{
    const a=e.target.closest('a[href^="#categoria-"]');
    if(!a||e.button!==0||e.ctrlKey||e.metaKey||e.shiftKey||e.altKey)return;
    const target=document.getElementById(a.hash.slice(1));if(!target)return;
    e.preventDefault();
    if(location.hash!==a.hash)history.pushState(null,'',a.hash);
    target.scrollIntoView({block:'start',behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
    const heading=target.querySelector('h2');if(heading){heading.tabIndex=-1;heading.focus({preventScroll:true});}
    active();
  });
  addEventListener('hashchange',active);active();
})();
