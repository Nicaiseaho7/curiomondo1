/* Shared by the static renderer and the browser when a newer feed arrives. */
((root,factory)=>{const api=factory();if(typeof module==='object'&&module.exports)module.exports=api;else root.CMHomeFlowChoices=api})(typeof globalThis==='undefined'?this:globalThis,()=>{
  'use strict';
  const key=(A,e)=>A.canonicalKey(e).replace(/(?:\/index)?\.html(?=[?$]|$)/,'');
  function compose(A,items,now,preferred){
    const entries=new Map();
    for(const e of items){
      const date=A.firstPublished(e), k=key(A,e);
      if(!k||!date||date>now||e.draft===true||e.published===false||!e.title||!e.url)continue;
      if(!entries.has(k))entries.set(k,e);
    }
    const ordered=[...entries.values()].sort((a,b)=>A.firstPublished(b)-A.firstPublished(a));
    const stamp=new Intl.DateTimeFormat('sv-SE',{year:'numeric',month:'2-digit',day:'2-digit',timeZone:'Europe/Rome'});
    const today=stamp.format(now);
    const day=e=>stamp.format(A.firstPublished(e));
    const category=e=>A.categoryFor(e)?.id||'';
    const lead=preferred&&entries.get(key(A,preferred)) || ordered.find(e=>day(e)===today&&e.image)||ordered.find(e=>e.image)||ordered[0];
    const heroKey=lead&&key(A,lead);
    const groups=new Map();
    for(const e of ordered){
      if(key(A,e)===heroKey||!e.image)continue;
      const d=day(e);if(!groups.has(d))groups.set(d,[]);groups.get(d).push(e);
    }
    // Se l'edizione del nuovo giorno non ha ancora cinque pezzi illustrati,
    // mantieni l'ultima selezione completa, con la sua data indicata in pagina.
    const edition=groups.get(today)?.length>=5 ? today : [...groups].find(([,pool])=>pool.length>=5)?.[0]||today;
    const ranked=(groups.get(edition)||[]).map((e,i)=>{
      const t=String(e.title||'');
      const priority=Math.max(0,Math.min(30,A.importance(e)));
      const impact=/\b(allerta|scioper\w*|manovra|elezioni|corte|sentenza|treni|prezz\w*|terremot\w*)\b/i.test(t)?14:0;
      const country=/\b(italia|italian[oi]|ue|europa|nazionale)\b/i.test(t)?6:0;
      const c=category(e);
      const nationalSport=c==='sport'&&/\b(serie a|champions|juventus|inter|milan|napoli|nazionale|mondiali|ferrari|sinner|motogp)\b/i.test(t)?14:0;
      const limited=/\b(nhl.*(richiama|rockford|assegn)|variazione da [\d.]+ euro|riqualificare la strada)\b/i.test(t)?19:0;
      const action=/\b(ritir\w* dal mercato|richiamo alimentare|taglio dei tassi|bollette|scadenza|fasce garantite)\b/i.test(t)?13:0;
      return {e,score:priority*2+impact+country+nationalSport+action-limited+(e.updated===true?4:0)+Math.max(0,13-i/10)};
    }).sort((a,b)=>b.score-a.score);
    const selection=[], seen=new Set(lead?[heroKey]:[]), categories=new Set();
    const add=e=>{const k=key(A,e);if(seen.has(k))return;seen.add(k);selection.push(e)};
    for(const {e} of ranked){const c=category(e);if(!c||categories.has(c))continue;add(e);categories.add(c);if(selection.length===5)break;}
    for(const {e} of ranked){if(selection.length===5)break;add(e);}
    const wire=[];
    for(const e of ordered){const k=key(A,e);if(seen.has(k))continue;seen.add(k);wire.push(e);if(wire.length===10)break;}
    const sections=A.CONFIG.categories.map(category=>{
      const stories=[];
      const pool=ordered.filter(e=>A.categoryFor(e)?.id===category.id&&!seen.has(key(A,e)));
      const lead=pool.find(e=>e.image)||pool[0];
      if(lead){stories.push(lead);seen.add(key(A,lead));}
      for(const e of pool){if(seen.has(key(A,e)))continue;seen.add(key(A,e));stories.push(e);if(stories.length===6)break;}
      return {category,stories};
    });
    return {lead,selection,edition,today,wire,sections,remaining:ordered.filter(e=>!seen.has(key(A,e)))};
  }
  const dateLabel=day=>new Intl.DateTimeFormat('it-IT',{day:'numeric',month:'long',timeZone:'Europe/Rome'}).format(new Date(day+'T12:00:00Z'));
  function mountCarousel(block){
    const viewport=block?.querySelector('.cm-featured-carousel__viewport');
    if(!viewport||viewport.dataset.flowMounted)return;
    const slides=[...viewport.querySelectorAll('.cm-featured-carousel__slide')];
    const controls=block.querySelector('.cm-featured-carousel__controls');
    if(!slides.length||!controls)return;
    viewport.dataset.flowMounted='true';
    const dots=[...controls.querySelectorAll('.cm-featured-carousel__dot')];
    const arrows=[...controls.querySelectorAll('.cm-featured-carousel__arrow')];
    const positions=()=>slides.map(slide=>slide.offsetLeft-slides[0].offsetLeft);
    const max=()=>Math.max(0,viewport.scrollWidth-viewport.clientWidth);
    const idx=()=>viewport.scrollLeft>=max()-3&&max()>3 ? slides.length-1 : positions().reduce((best,x,i,all)=>Math.abs(x-viewport.scrollLeft)<Math.abs(all[best]-viewport.scrollLeft)?i:best,0);
    const go=i=>viewport.scrollTo({left:Math.min(max(),positions()[Math.max(0,Math.min(i,slides.length-1))]),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
    const update=()=>{
      const index=idx();dots.forEach((dot,i)=>{dot.classList.toggle('is-active',i===index);dot.setAttribute('aria-current',String(i===index));});
      if(arrows[0])arrows[0].disabled=viewport.scrollLeft<=3;
      if(arrows[1])arrows[1].disabled=viewport.scrollLeft>=max()-3;
    };
    const nudge=delta=>viewport.scrollBy({left:delta*(positions()[1]||viewport.clientWidth),behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'instant':'smooth'});
    arrows[0]?.addEventListener('click',()=>nudge(-1));
    arrows[1]?.addEventListener('click',()=>nudge(1));
    dots.forEach((dot,i)=>dot.addEventListener('click',()=>go(i)));
    viewport.addEventListener('keydown',e=>{if(!['ArrowLeft','ArrowRight'].includes(e.key)||e.target!==viewport)return;e.preventDefault();nudge(e.key==='ArrowLeft'?-1:1);});
    viewport.addEventListener('scroll',update,{passive:true});
    if(typeof ResizeObserver!=='undefined')new ResizeObserver(update).observe(viewport);
    update();
  }
  return {compose,dateLabel,mountCarousel};
});
