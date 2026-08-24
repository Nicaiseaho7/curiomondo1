
import {getStore} from "@netlify/blobs";
import {readFile} from "node:fs/promises";
import {extractOutput,stripFence,slugify,similarity} from "./_common.mjs";

const OPENAI="https://api.openai.com/v1/responses";
const allowedLicenses=["cc0","public domain","cc by","cc by-sa"];

async function load(path){return readFile(new URL(path,import.meta.url),"utf8")}
async function openai(payload){
  const key=process.env.OPENAI_API_KEY;
  if(!key) throw new Error("OPENAI_API_KEY missing");
  const r=await fetch(OPENAI,{method:"POST",headers:{"content-type":"application/json","authorization":`Bearer ${key}`},body:JSON.stringify(payload)});
  const t=await r.text(); if(!r.ok) throw new Error(`OpenAI ${r.status}: ${t.slice(0,800)}`); return JSON.parse(t);
}
async function commonsImage(q){
  if(!q) return null;
  const u=new URL("https://commons.wikimedia.org/w/api.php");
  u.search=new URLSearchParams({action:"query",format:"json",origin:"*",generator:"search",gsrsearch:q,gsrnamespace:"6",gsrlimit:"8",prop:"imageinfo",iiprop:"url|extmetadata",iiurlwidth:"1200"}).toString();
  try{
    const r=await fetch(u,{headers:{"user-agent":"CurioMondo/1.0 (https://curiomondo.it)"}});
    const j=await r.json();
    for(const p of Object.values(j.query?.pages||{})){
      const ii=p.imageinfo?.[0], em=ii?.extmetadata||{};
      const lic=(em.LicenseShortName?.value||"").toLowerCase();
      if(!allowedLicenses.some(x=>lic===x||lic.startsWith(x+" "))) continue;
      const url=ii.thumburl||ii.url; if(!url) continue;
      return {url,source_page:`https://commons.wikimedia.org/wiki/${encodeURIComponent(p.title.replace(/ /g,"_"))}`,license:em.LicenseShortName?.value||"",author:(em.Artist?.value||"").replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim(),credit:(em.Credit?.value||"").replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim()};
    }
  }catch(e){console.log("commons",String(e))}
  return null;
}

export default async()=>{
  const started=new Date().toISOString();
  if(String(process.env.CURIOMONDO_AUTO_PUBLISH||"").toLowerCase()!=="true"){
    console.log("AUTO EDITOR dry-run: CURIOMONDO_AUTO_PUBLISH != true"); return;
  }
  const protocol=await load("../../CURIO-MONDO-PROTOCOLLO-MAESTRO.md");
  const staticIndex=JSON.parse(await load("../../automation/static-article-index.json"));
  const store=getStore({name:"curiomondo-articles",consistency:"strong"});
  const idx=await store.get("index",{type:"json",consistency:"strong"}).catch(()=>null)||{items:[]};
  const existing=[...staticIndex,...idx.items].map(x=>({title:x.title,slug:x.slug}));

  const prompt=`Sei la redazione automatica di CurioMondo. Oggi è ${started}.
Applica RIGIDAMENTE il protocollo allegato. Esegui una scansione web delle notizie delle ultime ore, con priorità Reuters, AP, AFP, Bloomberg, ANSA, Adnkronos, AGI e fonti istituzionali. Cerca sia Italia sia mondo e categorie diverse.
Seleziona al massimo 4 storie realmente nuove, significative e pubblicabili. Non devi riempire una quota.
Per geopolitica/guerre non trattare come fatto un'affermazione di una sola parte. Escludi gossip, rumor, dichiarazioni senza conseguenze, duplicati e aggiornamenti minori.
Confronta con l'elenco degli articoli già presenti. Se è solo un aggiornamento di una storia esistente, pubblica una nuova pagina soltanto se lo sviluppo è sostanziale; se manca la storia-base, costruisci l'articolo partendo dalla storia-base e incorpora lo sviluppo.
Per ogni storia approvata scrivi un articolo italiano fluido, senza H2/H3 di default, normalmente 5000-7000 caratteri di BODY. Non inventare nulla.
Restituisci SOLO JSON:
{"articles":[{"publish":true,"title":"","short_title":"","slug":"","description":"","category":"","sub_category":"","badge":"","priority":0,"ultima_ora":false,"keywords":[""],"body_paragraphs":[""],"sources":[{"name":"","url":"","claim":""}],"image_query":""}]}
Le sources devono contenere URL reali emersi dalla ricerca. image_query deve essere una query concreta in inglese per Wikimedia Commons, non il nome di un fotografo.

ARTICOLI ESISTENTI:
${JSON.stringify(existing.slice(-450))}

PROTOCOLLO:
${protocol.slice(0,24000)}`;

  const res=await openai({model:process.env.CURIOMONDO_OPENAI_MODEL||"gpt-5.6-sol",tools:[{type:"web_search"}],input:prompt});
  let data; try{data=JSON.parse(stripFence(extractOutput(res)))}catch(e){throw new Error("Invalid editorial JSON")}
  const approved=[];
  for(const a of data.articles||[]){
    if(!a.publish||!a.title||!Array.isArray(a.body_paragraphs)||!Array.isArray(a.sources)) continue;
    const body=a.body_paragraphs.join("\n\n").trim();
    const chars=body.length;
    if(chars<4200||chars>7600){console.log("blocked length",a.title,chars);continue}
    if(a.sources.length<1||a.sources.some(s=>!/^https?:\/\//.test(s.url||""))){console.log("blocked sources",a.title);continue}
    if(existing.some(x=>similarity(x.title,a.title)>=0.72)){console.log("blocked duplicate",a.title);continue}
    let slug=slugify(a.slug||a.title); if(!slug) continue;
    if(await store.get(`article:${slug}`,{type:"json",consistency:"strong"}).catch(()=>null)) continue;
    const image=await commonsImage(a.image_query);
    const now=new Date().toISOString();
    const article={...a,slug,body,body_paragraphs:a.body_paragraphs,character_count:chars,image,published_at:now,modified_at:now,auto_published:true};
    await store.setJSON(`article:${slug}`,article);
    approved.push({slug,title:a.title,short_title:a.short_title||a.title,description:a.description||"",category:a.category||"Mondo",sub_category:a.sub_category||"",badge:a.badge||a.category||"Notizie",priority:Number(a.priority||0),ultima_ora:Boolean(a.ultima_ora),image,published_at:now,url:`/notizie/${slug}.html`});
    existing.push({title:a.title,slug});
  }
  if(approved.length){
    const next={updated_at:new Date().toISOString(),items:[...approved,...idx.items].filter((x,i,a)=>a.findIndex(y=>y.slug===x.slug)===i).slice(0,300)};
    await store.setJSON("index",next);
    const live=getStore({name:"curiomondo-live",consistency:"strong"});
    const lf=await live.get("latest",{type:"json",consistency:"strong"}).catch(()=>null);
    if(lf?.items){
      for(const li of lf.items) for(const a of approved) if(similarity(li.title,a.title)>=0.48){li.article_exists=true;li.url=a.url}
      await live.setJSON("latest",{...lf,updated_at:new Date().toISOString()});
    }
  }
  console.log(JSON.stringify({started,approved:approved.map(x=>x.title)}));
};
export const config={schedule:"*/30 * * * *"};
