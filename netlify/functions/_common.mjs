
export const esc=(s="")=>String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
export const norm=(s="")=>String(s).toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g,"").replace(/[^a-z0-9 ]/g," ").replace(/\s+/g," ").trim();
export const tok=(s="")=>new Set(norm(s).split(" ").filter(x=>x.length>3));
export function similarity(a,b){const A=tok(a),B=tok(b);if(!A.size||!B.size)return 0;let n=0;for(const x of A)if(B.has(x))n++;return n/Math.max(1,Math.min(A.size,B.size))}
export function slugify(s=""){return norm(s).split(" ").slice(0,15).join("-").replace(/-+/g,"-").slice(0,110).replace(/^-|-$/g,"")}
export function extractOutput(r){if(r.output_text)return r.output_text;let a=[];for(const o of r.output||[])for(const c of o.content||[])if(c.text)a.push(c.text);return a.join("")}
export function stripFence(s=""){return s.replace(/^```(?:json)?\s*/i,"").replace(/\s*```$/,"").trim()}
export function paragraphs(body=""){return String(body).split(/\n{2,}/).map(x=>x.trim()).filter(Boolean)}
