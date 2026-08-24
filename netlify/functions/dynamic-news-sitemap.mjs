
import {getStore} from "@netlify/blobs";
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
export default async()=>{
 const store=getStore({name:"curiomondo-articles",consistency:"strong"});
 const idx=await store.get("index",{type:"json",consistency:"strong"}).catch(()=>null)||{items:[]};
 const cutoff=Date.now()-48*3600*1000;
 const rows=idx.items.filter(x=>Date.parse(x.published_at)>=cutoff).map(x=>`<url><loc>https://curiomondo.it/notizie/${esc(x.slug)}.html</loc><news:news><news:publication><news:name>CurioMondo</news:name><news:language>it</news:language></news:publication><news:publication_date>${esc(x.published_at)}</news:publication_date><news:title>${esc(x.title)}</news:title></news:news></url>`).join("");
 return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">${rows}</urlset>`,{headers:{"content-type":"application/xml; charset=utf-8","cache-control":"public,max-age=300"}});
};
