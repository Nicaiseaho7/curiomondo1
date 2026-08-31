(function(){
  'use strict';

  var reader=document.querySelector('[data-book-reader]')||document.querySelector('.cm-book-shell');
  if(!reader)return;

  var shell=reader.closest('.cm-book-shell')||reader;
  var stage=reader.querySelector('.cm-book-stage')||reader;
  var prev=shell.querySelector('[data-book-prev]')||document.querySelector('[data-book-prev]');
  var next=shell.querySelector('[data-book-next]')||document.querySelector('[data-book-next]');
  if(!prev||!next)return;
  if(shell.getAttribute('data-book-bound')==='true')return;

  reader.setAttribute('data-book-reader','');
  shell.setAttribute('data-book-bound','true');

  function addCover(){
    if(stage.querySelector('.cm-book-cover'))return;
    var first=stage.querySelector('.cm-book-page');
    if(!first)return;
    var originalTitle=first.querySelector('h1');
    var originalLead=first.querySelector('p');
    var originalMeta=first.querySelector('.cm-book-kicker,.cm-book-meta');
    var title=originalTitle?originalTitle.textContent.trim():document.title.split('|')[0].trim();
    var lead=originalLead?originalLead.textContent.trim():'';
    var meta=originalMeta?originalMeta.textContent.trim():'eBook CurioMondo';
    var cover=document.createElement('section');
    cover.className='cm-book-page cm-book-cover';
    cover.setAttribute('data-book-page','');
    cover.setAttribute('aria-label','Copertina eBook: '+title);
    cover.innerHTML=
      '<div class="cm-cover-orbit" aria-hidden="true"><i></i><i></i><i></i></div>'+ 
      '<div class="cm-cover-content">'+
        '<span class="cm-cover-series">Biblioteca CurioMondo</span>'+ 
        '<span class="cm-book-meta"></span>'+ 
        '<h1></h1>'+ 
        '<p class="cm-book-lead"></p>'+ 
        '<div class="cm-cover-rule"></div>'+ 
        '<div class="cm-cover-footer"><strong>CurioMondo</strong><span>Biblioteca · guida premium</span></div>'+ 
      '</div>'+ 
      '<span class="cm-book-page-number">Copertina</span>';
    cover.querySelector('h1').textContent=title;
    cover.querySelector('.cm-book-lead').textContent=lead;
    cover.querySelector('.cm-book-meta').textContent=meta;
    stage.insertBefore(cover,first);
  }

  addCover();

  var pages=Array.prototype.slice.call(stage.querySelectorAll('.cm-book-page'));
  if(!pages.length)return;
  var index=0;
  var animating=false;
  var reduceMotion=true;
  var hashMatch=location.hash.match(/^#pagina-(\d+)$/);
  if(hashMatch)index=Math.max(0,Math.min(pages.length-1,Number(hashMatch[1])-1));

  prev.textContent='← Indietro';
  next.textContent='Avanti →';

  pages.forEach(function(page,i){
    var number=page.querySelector('.cm-book-page-number');
    if(!number){
      number=document.createElement('span');
      number.className='cm-book-page-number';
      page.appendChild(number);
    }
    number.textContent=(i===0?'Copertina · ':'')+(i+1)+' / '+pages.length;
  });

  function updateControls(shouldScroll){
    prev.disabled=index===0;
    next.disabled=index===pages.length-1;
    prev.setAttribute('aria-label','Indietro: pagina precedente');
    next.setAttribute('aria-label','Avanti: pagina successiva');
    var count=shell.querySelector('[data-book-count]')||document.querySelector('[data-book-count]');
    if(count)count.textContent='Pagina '+(index+1)+' di '+pages.length;
    try{history.replaceState(null,'','#pagina-'+(index+1))}catch(e){}
    if(shouldScroll)stage.scrollIntoView({behavior:reduceMotion?'auto':'smooth',block:'start'});
  }

  function renderInitial(){
    pages.forEach(function(page,i){
      var active=i===index;
      page.classList.toggle('is-active',active);
      page.setAttribute('aria-hidden',active?'false':'true');
    });
    updateControls(false);
  }

  function goTo(target,shouldScroll){
    if(animating||target<0||target>=pages.length||target===index)return;
    var from=index;
    var direction=target>from?1:-1;
    var outgoing=pages[from];
    var incoming=pages[target];
    index=target;
    incoming.setAttribute('aria-hidden','false');
    outgoing.setAttribute('aria-hidden','true');
    if(reduceMotion){
      outgoing.classList.remove('is-active');
      incoming.classList.add('is-active');
      updateControls(shouldScroll);
      return;
    }
    animating=true;
    outgoing.classList.add('is-leaving',direction>0?'cm-turn-out-forward':'cm-turn-out-back');
    incoming.classList.add('is-active',direction>0?'cm-turn-in-forward':'cm-turn-in-back');
    updateControls(shouldScroll);
    window.setTimeout(function(){
      outgoing.classList.remove('is-active','is-leaving','cm-turn-out-forward','cm-turn-out-back');
      incoming.classList.remove('cm-turn-in-forward','cm-turn-in-back');
      animating=false;
    },460);
  }

  prev.addEventListener('click',function(event){
    event.preventDefault();
    goTo(index-1,true);
  });

  next.addEventListener('click',function(event){
    event.preventDefault();
    goTo(index+1,true);
  });

  renderInitial();
})();
