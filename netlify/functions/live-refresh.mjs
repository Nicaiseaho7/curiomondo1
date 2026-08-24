import { getStore } from "@netlify/blobs";
import { readFile } from "node:fs/promises";

const decode = (s="") => s
  .replace(/<!\[CDATA\[|\]\]>/g, "")
  .replace(/&amp;/g,"&").replace(/&quot;/g,'"').replace(/&#39;|&apos;/g,"'")
  .replace(/&lt;/g,"<").replace(/&gt;/g,">")
  .replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim();

function extract(xml) {
  const out=[];
  for (const m of xml.matchAll(/<item\b[\s\S]*?<\/item>/gi)) {
    const x=m[0];
    const pick=(tag)=>{const r=x.match(new RegExp(`<${tag}[^>]*>([\\s\\S]*?)<\\/${tag}>`,'i')); return r?decode(r[1]):''};
    const title=pick('title'), link=pick('link'), pubDate=pick('pubDate');
    const src=(x.match(/<source[^>]*>([\s\S]*?)<\/source>/i)||[])[1];
    if(title) out.push({title, source:decode(src||''), external_url:link, published_at:pubDate?new Date(pubDate).toISOString():new Date().toISOString()});
  }
  return out;
}

function norm(s=''){return s.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/[^a-z0-9 ]/g,' ').replace(/\s+/g,' ').trim()}
function tokens(s){return new Set(norm(s).split(' ').filter(x=>x.length>3))}
function similar(a,b){const A=tokens(a),B=tokens(b); if(!A.size||!B.size)return 0; let i=0; for(const x of A)if(B.has(x))i++; return i/Math.max(1,Math.min(A.size,B.size));}
function cleanGoogleTitle(title){return title.replace(/\s+-\s+[^-]{2,50}$/,'').trim()}

async function cfg(){
  const u=new URL("../../automation/live-sources.json",import.meta.url);
  return JSON.parse(await readFile(u,'utf8'));
}
async function seed(){
  const u=new URL("../../automation/live-seed.json",import.meta.url);
  return JSON.parse(await readFile(u,'utf8'));
}

export default async () => {
  const c=await cfg();
  const store=getStore({name:'curiomondo-live',consistency:'strong'});
  let existing=await store.get('latest',{type:'json',consistency:'strong'}).catch(()=>null);
  if(!existing?.items?.length) existing=await seed();

  const found=[];
  for(const f of c.feeds.filter(x=>x.enabled)){
    try{
      const r=await fetch(f.url,{headers:{'user-agent':'CurioMondoLive/1.0 (+https://curiomondo.it)'}});
      if(!r.ok) continue;
      for(const x of extract(await r.text())) found.push({...x, title:cleanGoogleTitle(x.title)});
    }catch(e){console.log('feed error',f.name,String(e));}
  }

  const trusted=found.filter(x=>!x.source || c.trusted_publishers.some(p=>norm(x.source).includes(norm(p))));
  const now=Date.now();
  const recent=trusted.filter(x=>{const t=Date.parse(x.published_at);return !Number.isFinite(t)||now-t<3*60*60*1000});
  const highTerms=c.high_risk_terms.map(norm);

  const accepted=[];
  for(const x of recent.sort((a,b)=>Date.parse(b.published_at)-Date.parse(a.published_at))){
    const high=highTerms.some(k=>norm(x.title).includes(k));
    if(high){
      const corroborated=recent.some(y=>y!==x && y.source!==x.source && similar(x.title,y.title)>=0.52);
      if(!corroborated) continue;
    }
    if(accepted.some(y=>similar(x.title,y.title)>=0.68)) continue;
    accepted.push({title:x.title,url:null,published_at:x.published_at,source:x.source||'Fonte verificata',article_exists:false});
  }

  // Keep CurioMondo-linked entries where useful; new discovery items lead the ticker.
  const merged=[...accepted,...existing.items.filter(x=>x.article_exists===true)]
    .filter((x,i,a)=>a.findIndex(y=>similar(x.title,y.title)>=0.72)===i)
    .slice(0,c.max_items||10);
  const payload={updated_at:new Date().toISOString(),items:merged};
  await store.setJSON('latest',payload);
  console.log(`LIVE updated: ${merged.length} items`);
};

export const config={schedule:'*/10 * * * *'};
