
import {getStore} from "@netlify/blobs";
const esc=s=>String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;");
export default async()=>{
 const store=getStore({name:"curiomondo-articles",consistency:"strong"});
 const idx=await store.get("index",{type:"json",consistency:"strong"}).catch(()=>null)||{items:[]};
 const rows=idx.items.map(x=>`<url><loc>https://curiomondo.it/notizie/${esc(x.slug)}.html</loc><lastmod>${esc(x.published_at||new Date().toISOString())}</lastmod></url>`).join("");
 return new Response(`<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">${rows}</urlset>`,{headers:{"content-type":"application/xml; charset=utf-8","cache-control":"public,max-age=300"}});
};
