(function(){
  'use strict';
  var reader=document.querySelector('[data-book-reader]');
  if(!reader)return;
  var pages=Array.prototype.slice.call(reader.querySelectorAll('.cm-book-page'));
  var prev=document.querySelector('[data-book-prev]');
  var next=document.querySelector('[data-book-next]');
  var count=document.querySelector('[data-book-count]');
  var index=0,touchX=null;
  var hashMatch=location.hash.match(/^#pagina-(\d+)$/);
  if(hashMatch)index=Math.max(0,Math.min(pages.length-1,Number(hashMatch[1])-1));
  function show(n,scroll){
    index=Math.max(0,Math.min(pages.length-1,n));
    pages.forEach(function(page,i){var active=i===index;page.classList.toggle('is-active',active);page.setAttribute('aria-hidden',active?'false':'true');});
    prev.disabled=index===0;next.disabled=index===pages.length-1;
    prev.setAttribute('aria-label','Vai alla pagina precedente');next.setAttribute('aria-label','Vai alla pagina successiva');
    count.textContent='Pagina '+(index+1)+' di '+pages.length;
    history.replaceState(null,'','#pagina-'+(index+1));
    if(scroll)reader.scrollIntoView({behavior:'smooth',block:'start'});
  }
  prev.addEventListener('click',function(){show(index-1,true)});
  next.addEventListener('click',function(){show(index+1,true)});
  document.addEventListener('keydown',function(e){if(/INPUT|TEXTAREA|SELECT/.test(document.activeElement.tagName))return;if(e.key==='ArrowLeft')show(index-1,true);if(e.key==='ArrowRight')show(index+1,true)});
  reader.addEventListener('touchstart',function(e){touchX=e.changedTouches[0].clientX},{passive:true});
  reader.addEventListener('touchend',function(e){if(touchX===null)return;var d=e.changedTouches[0].clientX-touchX;if(Math.abs(d)>55)show(index+(d<0?1:-1),true);touchX=null},{passive:true});
  show(index,false);
})();
