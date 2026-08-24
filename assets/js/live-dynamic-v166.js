(()=>{
 const endpoint='/.netlify/functions/live-feed';
 const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 function itemHTML(x){
   const text=`<span aria-hidden="true">✦</span> ${esc(x.title)}`;
   if(x.article_exists && x.url && /^\//.test(x.url)) return `<a class="ticker-news" href="${esc(x.url)}">${text}</a>`;
   return `<span class="ticker-news cm-live-unlinked" aria-label="Ultimissima non ancora disponibile come articolo">${text}</span>`;
 }
 function render(items){
   const root=document.getElementById('tickerMove'); if(!root||!Array.isArray(items)||!items.length)return;
   const ten=items.slice(0,10); if(ten.length<1)return;
   const html=ten.map(itemHTML).join('');
   root.innerHTML=`<div class="cm-ticker-set">${html}</div><div aria-hidden="true" class="cm-ticker-set">${html}</div>`;
 }
 async function refresh(){
   try{const r=await fetch(endpoint,{cache:'no-store'}); if(!r.ok)return; const d=await r.json(); render(d.items);}catch(e){}
 }
 if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',refresh);else refresh();
 setInterval(()=>{if(!document.hidden)refresh()},60000);
 document.addEventListener('visibilitychange',()=>{if(!document.hidden)refresh()});
})();
