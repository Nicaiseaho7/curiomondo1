(function(){
'use strict';
var runtimePromise=null;
function loadScript(src){return new Promise(function(resolve,reject){var s=document.createElement('script');s.src=src;s.defer=true;s.onload=resolve;s.onerror=reject;document.head.appendChild(s);});}
window.cmLoadFullRuntime=function(){
  if(runtimePromise)return runtimePromise;
  runtimePromise=loadScript('assets/js/curiomondo-discovery-v209.js?v=209')
    .then(function(){return loadScript('assets/js/home-original-v101.js?v=209');})
    .then(function(){document.removeEventListener('input',inputHandler);document.removeEventListener('click',clickHandler);document.removeEventListener('keydown',keyHandler);return loadScript('assets/js/curiomondo-orbit-turbo-v34.js?v=209');})
    .catch(function(e){console.error('CurioMondo runtime non disponibile',e);});
  return runtimePromise;
};
window.goHomeFeed=function(){location.href='/';};

/* Header/menu: available immediately without the large editorial runtime. */
window.openDrawer=function(){
  var d=document.getElementById('drawer'),o=document.getElementById('drawerOverlay'),b=document.getElementById('menuBtn');
  if(!d)return;d.removeAttribute('inert');d.setAttribute('aria-hidden','false');d.classList.add('open');if(o)o.classList.add('open');if(b)b.setAttribute('aria-expanded','true');document.body.style.overflow='hidden';
  window.cmLoadFullRuntime();
};
window.closeDrawer=function(){
  var d=document.getElementById('drawer'),o=document.getElementById('drawerOverlay'),b=document.getElementById('menuBtn');
  if(!d)return;d.classList.remove('open');d.setAttribute('aria-hidden','true');d.setAttribute('inert','');if(o)o.classList.remove('open');if(b)b.setAttribute('aria-expanded','false');document.body.style.overflow='';
};
window.toggleTheme=function(){
  var dark=!document.body.classList.contains('dark');document.body.classList.toggle('dark',dark);document.documentElement.classList.toggle('cm-dark',dark);try{localStorage.setItem('cm_theme',dark?'dark':'light');}catch(e){}
  var lab=document.getElementById('themeLabelDrawer');if(lab)lab.textContent=dark?'Modalità chiara':'Modalità scura';
};
try{var pref=localStorage.getItem('cm_theme')==='dark';document.body.classList.toggle('dark',pref);document.documentElement.classList.toggle('cm-dark',pref);}catch(e){}

/* Search: small on-demand index; no 280 KB homepage runtime needed. */
var searchIndex=null,searchPromise=null;
function norm(v){return(v||'').toLocaleLowerCase('it').normalize('NFD').replace(/[\u0300-\u036f]/g,'');}
function loadSearch(){if(searchIndex)return Promise.resolve(searchIndex);if(!searchPromise)searchPromise=fetch('assets/data/search-index-v101.json',{credentials:'same-origin'}).then(function(r){if(!r.ok)throw new Error('search');return r.json();}).then(function(x){searchIndex=Array.isArray(x)?x:[];return searchIndex;});return searchPromise;}
window.openSiteSearch=function(){var m=document.getElementById('siteSearchModal');if(!m)return;m.removeAttribute('inert');m.setAttribute('aria-hidden','false');m.classList.add('open');document.body.style.overflow='hidden';loadSearch();setTimeout(function(){var i=document.getElementById('siteSearchInput');if(i)i.focus();},40);};
window.closeSiteSearch=function(){var m=document.getElementById('siteSearchModal');if(!m)return;m.classList.remove('open');m.setAttribute('aria-hidden','true');m.setAttribute('inert','');document.body.style.overflow='';};
window.openSearchResult=function(u){window.closeSiteSearch();location.href=u;};
window.runSiteSearch=async function(q){var box=document.getElementById('siteSearchResults'),st=document.getElementById('siteSearchStatus');if(!box||!st)return;q=norm(String(q||'').trim());if(q.length<2){box.innerHTML='';st.textContent='Scrivi almeno due lettere.';return;}st.textContent='Ricerca in corso…';try{var idx=await loadSearch(),ws=q.split(/\s+/).filter(Boolean),r=idx.map(function(x){var t=norm(x.title),d=norm(x.desc),a=norm(x.text),score=0;ws.forEach(function(w){if(t.indexOf(w)>-1)score+=8;if(d.indexOf(w)>-1)score+=4;if(a.indexOf(w)>-1)score+=1;});return Object.assign({},x,{score:score});}).filter(function(x){return x.score>0;}).sort(function(a,b){return b.score-a.score;}).slice(0,30);st.textContent=r.length?r.length+' risultati trovati':'Nessun risultato.';box.innerHTML=r.map(function(x){return '<button type="button" data-cm-search-url="'+String(x.url||'').replace(/&/g,'&amp;').replace(/"/g,'&quot;')+'"><small>NOTIZIA</small><strong>'+String(x.title||'').replace(/</g,'&lt;')+'</strong><span>'+String(x.desc||'Apri il contenuto completo').replace(/</g,'&lt;')+'</span><b>→</b></button>';}).join('');}catch(e){st.textContent='La ricerca non è disponibile in questo momento.';}};
function inputHandler(e){if(e.target&&e.target.id==='siteSearchInput')window.runSiteSearch(e.target.value);}
function clickHandler(e){var b=e.target&&e.target.closest&&e.target.closest('[data-cm-search-url]');if(b){e.preventDefault();window.openSearchResult(b.getAttribute('data-cm-search-url'));}}
function keyHandler(e){if(e.key==='Escape')window.closeSiteSearch();}
document.addEventListener('input',inputHandler);document.addEventListener('click',clickHandler);document.addEventListener('keydown',keyHandler);

/* Lazy card backgrounds without loading the full client application. */
function lazyBackgrounds(){var nodes=[].slice.call(document.querySelectorAll('[data-cm-bg]'));function load(el){var u=el&&el.getAttribute('data-cm-bg');if(!u)return;el.style.backgroundImage='url("'+u.replace(/"/g,'%22')+'")';el.removeAttribute('data-cm-bg');}if(!('IntersectionObserver'in window)){nodes.forEach(load);return;}var io=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){load(x.target);io.unobserve(x.target);}});},{rootMargin:'180px 80px'});nodes.forEach(function(n){io.observe(n);});}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',lazyBackgrounds,{once:true});else lazyBackgrounds();

/* Cookie consent remains functional on first paint. */
(function(){var KEY='cm_consent_v2',VERSION='2026-08-06';function read(){try{return JSON.parse(localStorage.getItem(KEY)||'null');}catch(e){return null;}}function apply(v){document.documentElement.dataset.consentAnalytics=v.analytics?'granted':'denied';document.documentElement.dataset.consentMarketing=v.marketing?'granted':'denied';document.documentElement.dataset.consentExternal=v.external?'granted':'denied';document.querySelectorAll('script[type="text/plain"][data-cookiecategory]').forEach(function(s){var c=s.dataset.cookiecategory;if(v[c]&&!s.dataset.loaded){var n=document.createElement('script');[].slice.call(s.attributes).forEach(function(a){if(a.name!=='type'&&a.name!=='data-cookiecategory')n.setAttribute(a.name,a.value);});n.text=s.text;s.parentNode.insertBefore(n,s.nextSibling);s.dataset.loaded='1';}});}function close(){var m=document.getElementById('cm-consent');if(m)m.classList.remove('open');}function open(custom){var m=document.getElementById('cm-consent');if(!m)return;m.classList.add('open');var d=m.querySelector('.cmc-details'),x=m.querySelector('.cmc-close');if(custom&&d)d.classList.add('open');if(custom&&x)x.style.display='block';var v=read()||{};['preferences','analytics','marketing','external'].forEach(function(k){var e=document.getElementById('cmc-'+k);if(e)e.checked=!!v[k];});}function write(v){v.version=VERSION;v.updatedAt=new Date().toISOString();try{localStorage.setItem(KEY,JSON.stringify(v));}catch(e){}apply(v);close();}function init(){var m=document.getElementById('cm-consent');if(!m)return;var v=read();if(v)apply(v);else open(false);var a=m.querySelector('[data-cm-accept]'),r=m.querySelector('[data-cm-reject]'),c=m.querySelector('[data-cm-custom]'),save=m.querySelector('[data-cm-save]'),x=m.querySelector('.cmc-close');if(a)a.onclick=function(){write({necessary:true,preferences:true,analytics:true,marketing:true,external:true});};if(r)r.onclick=function(){write({necessary:true,preferences:false,analytics:false,marketing:false,external:false});};if(c)c.onclick=function(){m.querySelector('.cmc-details').classList.add('open');if(x)x.style.display='block';};if(save)save.onclick=function(){write({necessary:true,preferences:!!document.getElementById('cmc-preferences').checked,analytics:!!document.getElementById('cmc-analytics').checked,marketing:!!document.getElementById('cmc-marketing').checked,external:!!document.getElementById('cmc-external').checked});};if(x)x.onclick=function(){if(read())close();};document.querySelectorAll('.cm-cookie-manage,[data-cookie-settings]').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();open(true);});});window.CurioConsent={open:function(){open(true);},get:read};}if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();})();

/* Advanced interactions load only when a user actually needs them or reaches the lower interactive area. */
function requestRuntime(){window.cmLoadFullRuntime();}
var fallbackShowFavs=function(){window.cmLoadFullRuntime().then(function(){if(window.showFavs&&window.showFavs!==fallbackShowFavs)try{window.showFavs();}catch(e){}});};window.showFavs=fallbackShowFavs;
window.addEventListener('keydown',function(e){if(e.key!=='Tab')requestRuntime();},{once:true});
if('requestIdleCallback'in window){requestIdleCallback(function(){requestRuntime();},{timeout:12000});}else{setTimeout(requestRuntime,12000);}
})();
