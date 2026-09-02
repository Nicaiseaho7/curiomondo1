/* One controller for every article, including legacy pages. */
(() => {
  'use strict';
  const CM=window.CM,article=document.querySelector('.art-body');if(!CM||!article)return;
  const url=location.pathname,id=document.body.dataset.articleId||url.split('/').filter(Boolean).pop()?.replace(/\.html$/,'')||'';
  const routeKey=value=>{try{let path=decodeURIComponent(new URL(value,location.href).pathname).replace(/\/index\.html$/i,'/').replace(/\.html$/i,'').replace(/\/+$/,'');return path||'/';}catch{return '';}};
  const routeId=value=>routeKey(value).split('/').filter(Boolean).pop()||'';
  const canonicalRoute=routeKey(document.querySelector('link[rel="canonical"]')?.href||url);
  const isCurrentArticle=value=>routeKey(value)===canonicalRoute||Boolean(id)&&routeId(value)===id;
  const favorites=()=>{const x=CM.read('cm_favs',[]);return Array.isArray(x)?x.filter(v=>typeof v==='string'):[];};
  const saved=()=>favorites().some(v=>v===url||v===id);
  const save=document.getElementById('cmSaveBtn');
  function syncSave(){if(!save)return;const active=saved();save.textContent=active?'★ Salvato':'★ Salva';save.classList.toggle('saved',active);save.setAttribute('aria-pressed',String(active));}
  save?.addEventListener('click',()=>{const active=saved(),items=favorites().filter(v=>v!==url&&v!==id);if(!active)items.unshift(url);if(!CM.write('cm_favs',items)){CM.toast('Il browser non consente di salvare i preferiti.');return;}syncSave();CM.toast(active?'Rimosso dai preferiti':'Articolo salvato');});syncSave();
  const articleTitle=document.querySelector('h1')?.textContent||document.title;
  const normalizeText=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/\s+/g,' ').trim().toLocaleLowerCase('it');
  const articleImage=document.querySelector('.article-image img,.wrap figure img,.art-hero-img');
  const ogImage=document.querySelector('meta[property="og:image"]')?.content||'';
  const readingImage=articleImage?.currentSrc||articleImage?.src||ogImage;
  const readingImagePath=readingImage?new URL(readingImage,location.href).pathname:'';
  let readingProgress=0;
  function saveReadingProgress(value){
    readingProgress=Math.max(0,Math.min(1,Number(value)||0));
    try{
      if(readingProgress>=.92){
        const stored=JSON.parse(localStorage.getItem('cm_last_read')||'null');
        if(stored?.url===url)localStorage.removeItem('cm_last_read');
        return;
      }
      localStorage.setItem('cm_last_read',JSON.stringify({id,url,title:articleTitle,image:readingImagePath,imageAlt:articleImage?.alt||'',progress:readingProgress,time:Date.now()}));
    }catch{}
  }
  saveReadingProgress(0);
  window.curioBack=e=>{e?.preventDefault();let internal=false;try{internal=new URL(document.referrer).origin===location.origin;}catch{}if(internal&&history.length>1)history.back();else location.assign('/');return false;};
  document.querySelectorAll('.btn-back').forEach(a=>a.addEventListener('click',window.curioBack));
  window.shareArticle=async()=>{const canonical=document.querySelector('link[rel="canonical"]')?.href||location.href;const data={title:document.querySelector('h1')?.textContent||document.title,url:canonical};try{if(navigator.share){await navigator.share(data);return;}if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(canonical);CM.toast('Link copiato');return;}CM.toast('Puoi copiare il link dalla barra degli indirizzi.');}catch(e){if(e.name!=='AbortError')CM.toast('Condivisione non disponibile: copia il link dalla barra degli indirizzi.');}};
  document.querySelector('[data-share-article]')?.addEventListener('click',window.shareArticle);
  const listen=document.getElementById('listenBtn');
  let chunks=[],index=0,running=false,paused=false,utterance=null,selectedVoice=null,premiumAudio=null;
  const premiumAudioSrc=document.body.dataset.audioSrc||document.querySelector('meta[name="cm:article-audio"]')?.content||'';
  const deepMaleNames=['luca','diego','giuseppe','marco','giorgio','raff','cosimo','dario','enrico','stefano','matteo','andrea'];
  const femaleNames=['alice','elsa','isabella','bianca','federica','paola','silvia'];
  const premiumWords=['neural','natural','premium','enhanced','studio','wavenet','eloquence','siri','google','microsoft'];
  function voiceScore(v){
    const name=(v?.name||'').toLocaleLowerCase('it'),lang=(v?.lang||'').toLocaleLowerCase('it');let score=0;
    if(lang==='it-it')score+=80;else if(lang.startsWith('it'))score+=60;else score-=120;
    premiumWords.forEach(x=>{if(name.includes(x))score+=28;});
    deepMaleNames.forEach(x=>{if(name.includes(x))score+=22;});
    femaleNames.forEach(x=>{if(name.includes(x))score-=18;});
    if(v?.localService)score+=4;
    return score;
  }
  function selectNaturalItalianVoice(){
    if(!('speechSynthesis'in window))return null;
    const voices=speechSynthesis.getVoices?.()||[];
    const italian=voices.filter(v=>(v.lang||'').toLowerCase().startsWith('it'));
    selectedVoice=(italian.length?italian:voices).slice().sort((a,b)=>voiceScore(b)-voiceScore(a))[0]||null;
    return selectedVoice;
  }
  selectNaturalItalianVoice();
  if('speechSynthesis'in window)speechSynthesis.addEventListener?.('voiceschanged',selectNaturalItalianVoice);
  function syncListen(){if(!listen)return;listen.textContent=!running?'Ascolta l’audio':paused?'▶ Riprendi ascolto':'Ⅱ Pausa ascolto';listen.setAttribute('aria-pressed',String(running));listen.setAttribute('aria-label',!running?'Ascolta l’articolo con voce naturale profonda':paused?'Riprendi la lettura audio':'Metti in pausa la lettura audio');}
  function stop(){running=false;paused=false;index=chunks.length;if(premiumAudio){premiumAudio.pause();premiumAudio.currentTime=0;}if('speechSynthesis'in window)speechSynthesis.cancel();utterance=null;syncListen();}
  function naturalChunks(parts){
    const out=[];for(const raw of parts){const text=String(raw||'').replace(/\s+/g,' ').trim();if(!text)continue;
      const sentences=text.match(/[^.!?…]+[.!?…]+|[^.!?…]+$/g)||[text];let group='';
      for(const sentence0 of sentences){const sentence=sentence0.trim();if(!sentence)continue;
        if((group+' '+sentence).trim().length<=430){group=(group+' '+sentence).trim();continue;}
        if(group)out.push(group);group='';
        if(sentence.length<=430){group=sentence;continue;}
        let rest=sentence;while(rest.length>430){let cut=Math.max(rest.lastIndexOf(',',430),rest.lastIndexOf(';',430),rest.lastIndexOf(':',430),rest.lastIndexOf(' ',430));if(cut<180)cut=430;out.push(rest.slice(0,cut+1).trim());rest=rest.slice(cut+1).trim();}group=rest;
      }if(group)out.push(group);
    }return out;
  }
  function speakNext(){
    if(!running||index>=chunks.length){running=false;paused=false;syncListen();return;}
    utterance=new SpeechSynthesisUtterance(chunks[index++]);utterance.lang='it-IT';utterance.rate=.92;utterance.pitch=.78;utterance.volume=1;
    const voice=selectedVoice||selectNaturalItalianVoice();if(voice)utterance.voice=voice;
    utterance.onend=()=>{if(running)speakNext();};
    utterance.onerror=e=>{if(e.error!=='canceled'&&e.error!=='interrupted'){stop();CM.toast('Lettura vocale interrotta dal dispositivo.');}};
    speechSynthesis.speak(utterance);
  }
  function startPremiumAudio(){
    if(!premiumAudioSrc)return false;
    try{premiumAudio=premiumAudio||new Audio(premiumAudioSrc);premiumAudio.preload='metadata';premiumAudio.onended=()=>{running=false;paused=false;syncListen();};premiumAudio.onerror=()=>{premiumAudioSrc&&CM.toast('Audio premium non disponibile: uso la migliore voce naturale del dispositivo.');premiumAudio=null;startSynth();};premiumAudio.play();running=true;paused=false;syncListen();return true;}catch{return false;}
  }
  function startSynth(){
    if(!('speechSynthesis'in window)||!('SpeechSynthesisUtterance'in window)){CM.toast('Lettura vocale non disponibile su questo dispositivo.');return;}
    const parts=[document.querySelector('h1')?.textContent||'',...Array.from(article.querySelectorAll('p,h2,h3,li')).map(e=>e.textContent.trim())];
    chunks=naturalChunks(parts);index=0;running=true;paused=false;speechSynthesis.cancel();selectNaturalItalianVoice();syncListen();speakNext();
  }
  window.toggleSpeak=()=>{
    if(running){paused=!paused;if(premiumAudio){if(paused)premiumAudio.pause();else premiumAudio.play();}else if('speechSynthesis'in window){if(paused)speechSynthesis.pause();else speechSynthesis.resume();}syncListen();return;}
    if(!startPremiumAudio())startSynth();
  };
  listen?.addEventListener('click',window.toggleSpeak);window.addEventListener('pagehide',stop);syncListen();
  async function ensureRelated(){
    let section=document.querySelector('.curio-related,.cm-related');
    if(!section){
      section=document.createElement('section');section.className='curio-related';section.setAttribute('aria-labelledby','curio-related-title');
      const heading=document.createElement('h2');heading.id='curio-related-title';heading.textContent='Potrebbe interessarti anche…';
      const grid=document.createElement('div');grid.className='curio-related-grid';section.append(heading,grid);
      document.querySelector('main.wrap')?.append(section);
    }
    let grid=section.querySelector('.curio-related-grid,.cm-related-grid');
    if(!grid){grid=document.createElement('div');grid.className='curio-related-grid';section.append(grid);}
    const uniqueLinks=new Set();
    Array.from(grid.querySelectorAll('a[href]')).forEach(link=>{const key=routeKey(link.href),sameTitle=normalizeText(link.querySelector('strong')?.textContent)===normalizeText(articleTitle);if(!key||isCurrentArticle(link.href)||sameTitle||uniqueLinks.has(key))link.remove();else uniqueLinks.add(key);});
    Array.from(grid.querySelectorAll('a[href]')).slice(3).forEach(link=>link.remove());
    const existing=new Set(Array.from(grid.querySelectorAll('a[href]')).map(a=>routeKey(a.href)).filter(Boolean));
    existing.add(canonicalRoute);
    try{
      const response=await fetch('/assets/data/home-feed-v210.json?v=236',{credentials:'same-origin'});if(!response.ok)return;
      const payload=await response.json(),items=Array.isArray(payload.items)?payload.items:[];
      const mediaByUrl=new Map(items.filter(item=>item?.url).map(item=>[routeKey(item.url),item]));
      Array.from(grid.querySelectorAll('a[href]')).forEach(link=>{const path=routeKey(link.href);if(!mediaByUrl.get(path)?.image)link.remove();});
      const context=normalizeText([articleTitle,document.querySelector('.badge')?.textContent,document.querySelector('.meta')?.textContent].join(' '));
      const stop=new Set(['della','delle','degli','dello','alla','alle','agli','nella','nelle','negli','dopo','come','sono','anche','ultime','notizia','notizie','articolo']);
      const terms=new Set(context.split(/[^a-z0-9]+/).filter(word=>word.length>3&&!stop.has(word)));
      const ranked=items.filter(item=>item?.url&&item?.title&&item?.image&&!isCurrentArticle(item.url)&&normalizeText(item.title)!==normalizeText(articleTitle)&&!existing.has(routeKey(item.url))).map(item=>{
        const haystack=normalizeText([item.title,item.excerpt,item.section].join(' '));let score=0;terms.forEach(term=>{if(haystack.includes(term))score+=term.length>7?3:1;});
        const currentSection=normalizeText(document.querySelector('.badge')?.textContent||document.querySelector('.meta')?.textContent||'');
        if(currentSection&&normalizeText(item.section).split(/[^a-z]+/).some(token=>token.length>4&&currentSection.includes(token)))score+=4;
        return {item,score};
      }).sort((a,b)=>b.score-a.score);
      for(const {item} of ranked){
        if(grid.querySelectorAll('a[href]').length>=3)break;
        const path=routeKey(item.url);if(!path||isCurrentArticle(item.url)||existing.has(path))continue;existing.add(path);
        const link=document.createElement('a');link.href=item.url;
        const small=document.createElement('small');small.textContent=item.section||'Articolo correlato';
        const strong=document.createElement('strong');strong.textContent=item.title;
        link.append(small,strong);grid.append(link);
      }
      Array.from(grid.querySelectorAll('a[href]')).forEach(link=>{
        const path=routeKey(link.href),item=mediaByUrl.get(path);
        let copy=link.querySelector('.curio-related-copy');
        if(!copy){
          copy=document.createElement('span');copy.className='curio-related-copy';
          Array.from(link.children).filter(child=>child.matches('small,strong')).forEach(child=>copy.append(child));
          link.append(copy);
        }
        if(!item?.image){link.classList.add('without-image');return;}
        link.classList.remove('without-image');
        if(link.querySelector('.curio-related-thumb'))return;
        const thumb=document.createElement('span');thumb.className='curio-related-thumb';
        const image=document.createElement('img');image.src=item.image;image.alt=item.imageAlt||'';image.width=112;image.height=76;image.loading='lazy';image.decoding='async';
        if(item.srcset){image.srcset=item.srcset;image.sizes='(max-width:600px) 88px,112px';}
        thumb.append(image);link.prepend(thumb);
      });
    }catch{}
  }
  ensureRelated();
  const bar=document.querySelector('.cm-reading-progress');let pending=false;
  function progress(){pending=false;const max=document.documentElement.scrollHeight-innerHeight;const value=max>0?Math.max(0,Math.min(1,scrollY/max)):0;if(bar)bar.style.transform=`scaleX(${value})`;const top=article.offsetTop,height=Math.max(article.offsetHeight,1);const read=(scrollY+innerHeight-top)/height;saveReadingProgress(read);}
  const schedule=()=>{if(!pending){pending=true;requestAnimationFrame(progress);}};window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule,{passive:true});window.addEventListener('pagehide',()=>saveReadingProgress(readingProgress));progress();
})();
