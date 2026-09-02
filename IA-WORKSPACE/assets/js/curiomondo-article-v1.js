try{if(localStorage.getItem('cm_theme')==='dark')document.documentElement.classList.add('cm-dark');else document.documentElement.classList.remove('cm-dark');}catch(e){}
/* CurioMondo Article Layout v1
   Comportamenti condivisi di tutte le nuove pagine notizia. */
(function(){
  "use strict";

  var currentUtterance = null;
  var body = document.body;
  var articleId = body.dataset.articleId || location.pathname.split('/').pop().replace(/\.html$/,'');

  function toast(message){
    var t=document.querySelector('.cm-inline-toast');
    if(!t){
      t=document.createElement('div');
      t.className='cm-inline-toast';
      t.setAttribute('role','status');
      document.body.appendChild(t);
    }
    t.textContent=message;
    t.classList.add('on');
    clearTimeout(t._tm);
    t._tm=setTimeout(function(){t.classList.remove('on');},2600);
  }

  function articleText(){
    var title=document.querySelector('h1');
    var parts=Array.from(document.querySelectorAll('.subtitle,.summary,.art-body p,.art-body h2,.conclusion p'));
    return (title?title.innerText+'. ':'')+parts.map(function(e){return e.innerText;}).join(' ');
  }

  window.toggleSpeak=function(){
    var b=document.getElementById('listenBtn');
    if(!b || !('speechSynthesis' in window)){toast('La lettura vocale non è disponibile su questo dispositivo.');return;}
    if(speechSynthesis.speaking&&!speechSynthesis.paused){speechSynthesis.pause();b.textContent='▶ Riprendi lettura';return;}
    if(speechSynthesis.paused){speechSynthesis.resume();b.textContent='⏸ Pausa';return;}
    speechSynthesis.cancel();
    currentUtterance=new SpeechSynthesisUtterance(articleText());
    currentUtterance.lang='it-IT';
    currentUtterance.onend=function(){b.textContent='▶ Ascolta l’articolo';b.classList.remove('playing');};
    speechSynthesis.speak(currentUtterance);
    b.textContent='⏸ Pausa';b.classList.add('playing');
  };

  window.shareArticle=async function(){
    var h1=document.querySelector('h1');
    var data={title:document.title,text:h1?h1.innerText:document.title,url:location.href};
    try{
      if(navigator.share) await navigator.share(data);
      else if(navigator.clipboard){await navigator.clipboard.writeText(location.href);toast('Link copiato');}
      else toast('Copia il link dalla barra del browser.');
    }catch(e){}
  };

  window.curioBack=function(ev){
    if(ev)ev.preventDefault();
    if(history.length>1){history.back();return false;}
    location.href='../index.html';
    return false;
  };

  function favs(){try{return JSON.parse(localStorage.getItem('cm_favs')||'[]');}catch(e){return[];}}
  function syncSave(){
    var b=document.getElementById('cmSaveBtn'); if(!b)return;
    var on=favs().indexOf(articleId)>=0;
    b.textContent=on?'★ Salvato':'★ Salva'; b.classList.toggle('saved',on); b.setAttribute('aria-pressed',on?'true':'false');
  }
  function toggleSave(){
    var ids=favs(),i=ids.indexOf(articleId);
    if(i>=0){ids.splice(i,1);toast('Rimosso dai preferiti');}
    else{ids.unshift(articleId);toast('Salvato nei preferiti');}
    localStorage.setItem('cm_favs',JSON.stringify(ids));syncSave();
  }
  function toggleTheme(){
    var on=document.documentElement.classList.toggle('cm-dark');document.body.classList.toggle('dark',on);
    localStorage.setItem('cm_theme',on?'dark':'light');
    var b=document.querySelector('.article-theme-toggle');
    if(b){b.textContent=on?'☀':'☾';b.setAttribute('aria-label',on?'Attiva modalità chiara':'Attiva modalità scura');}
  }
  function progress(){
    var d=document.documentElement,max=d.scrollHeight-innerHeight,p=max>0?scrollY/max*100:0;
    var bar=document.querySelector('.cm-reading-progress');if(bar)bar.style.width=Math.max(0,Math.min(100,p))+'%';
  }
  function validateLayout(){
    var required=['.topbar','.wrap','.badge','h1','.subtitle','.meta','.actions','figure','.summary','.editorial-data','.art-body','.conclusion','.art-sources','.site-footer-links'];
    var missing=required.filter(function(selector){return !document.querySelector(selector);});
    if(missing.length){console.error('CurioMondo article-v1: struttura incompleta. Mancano:',missing.join(', '));}
  }
  function buildChrome(){
    var p=document.createElement('i');p.className='cm-reading-progress';p.setAttribute('aria-hidden','true');document.body.prepend(p);
    var inner=document.querySelector('.topbar .inner');
    if(inner&&!inner.querySelector('.article-theme-toggle')){
      var theme=document.createElement('button');theme.type='button';theme.className='article-theme-toggle';
      theme.textContent=document.documentElement.classList.contains('cm-dark')?'☀':'☾';
      theme.setAttribute('aria-label',document.documentElement.classList.contains('cm-dark')?'Attiva modalità chiara':'Attiva modalità scura');
      theme.onclick=toggleTheme;inner.appendChild(theme);
    }
    document.querySelectorAll('.btn-back').forEach(function(b){
      b.setAttribute('href','../index.html');b.textContent='← Indietro';b.onclick=curioBack;
    });
    var actions=document.querySelector('.actions');
    if(actions&&!actions.querySelector('#cmSaveBtn')){
      var save=document.createElement('button');save.id='cmSaveBtn';save.type='button';save.setAttribute('aria-pressed','false');save.onclick=toggleSave;actions.appendChild(save);
    }
    syncSave();validateLayout();progress();
  }

  document.addEventListener('DOMContentLoaded',buildChrome);
  window.addEventListener('scroll',progress,{passive:true});
  window.addEventListener('resize',progress,{passive:true});
})();
