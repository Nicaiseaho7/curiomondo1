
import {getStore} from "@netlify/blobs";
export default async()=>{
 const store=getStore({name:"curiomondo-articles",consistency:"strong"});
 const idx=await store.get("index",{type:"json",consistency:"strong"}).catch(()=>null)||{updated_at:null,items:[]};
 return new Response(JSON.stringify(idx),{headers:{"content-type":"application/json; charset=utf-8","cache-control":"public,max-age=60"}});
};
