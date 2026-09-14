#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, re
from pathlib import Path
from PIL import Image
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

ROOT=Path(__file__).resolve().parents[1]
VERSION=353
SLUG="svezia-centrosinistra-avanti-elezioni-14-settembre-2026"
PUBLISHED="2026-09-14T16:42:00+02:00"
IMAGE_KEY=f"{SLUG}-ai-openai-v{VERSION}"
SOURCE_IMAGE=ROOT/"assets"/"images"/"editorial-source"/f"{SLUG}.png"

ARTICLE={
 "slug":SLUG,
 "titolo":"Svezia, centrosinistra avanti di tre seggi nelle elezioni: risultato ancora provvisorio",
 "sommario":"Il blocco guidato dalla socialdemocratica Magdalena Andersson ottiene 176 seggi contro 173 secondo il conteggio preliminare. Restano da scrutinare voti che possono incidere sull’equilibrio finale.",
 "categoria":"Mondo / Politica",
 "luogo":"Svezia",
 "formato":"standard",
 "parole_chiave_titolo":["centrosinistra avanti","risultato ancora provvisorio"],
 "dati_chiave":[
  {"icona":"◆","valore":"176","etichetta":"seggi al centrosinistra"},
  {"icona":"●","valore":"173","etichetta":"seggi al blocco di destra"},
  {"icona":"↔","valore":"3","etichetta":"seggi di differenza"},
 ],
 "paragrafi":[
  "Il centrosinistra svedese guidato dalla leader socialdemocratica Magdalena Andersson è avanti nelle elezioni parlamentari del 13 settembre. Il conteggio preliminare assegna al blocco 176 seggi, contro 173 alla coalizione di destra del primo ministro uscente Ulf Kristersson. Il margine resta però troppo stretto per considerare definitivo il risultato.",
  "I dati provvisori arrivano dall’Autorità elettorale svedese dopo lo scrutinio della grande maggioranza dei distretti. Devono ancora essere completati i controlli e conteggiati alcuni voti, compresi quelli espressi dall’estero. L’ente prevede di certificare il risultato finale nel fine settimana successivo al voto.",
  "La differenza di tre seggi consegnerebbe al blocco di Andersson la maggioranza minima nel Riksdag, composto da 349 membri. Non equivale tuttavia alla nascita automatica di un governo: la leader socialdemocratica dovrà ottenere sostegno parlamentare tra forze con posizioni diverse su tasse, welfare e ruolo della sinistra.",
  "Il voto segna anche una battuta d’arresto per i Democratici Svedesi. Secondo i risultati preliminari riportati da Reuters, il partito perde seggi rispetto alla precedente legislatura. È la prima flessione elettorale nazionale dopo anni di crescita, ma la formazione conserva un peso rilevante nel blocco di destra.",
  "L’eventuale cambio di maggioranza non implica una rapida inversione delle politiche migratorie. Durante la campagna anche il centrosinistra ha mantenuto una linea più restrittiva rispetto alla tradizione svedese, in un dibattito dominato da criminalità, integrazione e pressione sui servizi pubblici.",
  "Il confronto con il 2022 invita alla cautela. Quattro anni fa le prime proiezioni indicarono un vantaggio per Andersson, poi superato nel conteggio definitivo dalla coalizione di Kristersson. Per questo i leader hanno evitato di proclamare una vittoria prima della certificazione ufficiale.",
  "Il dato centrale, al momento, è quindi un vantaggio parlamentare minimo e non ancora consolidato. Eventuali spostamenti di pochi seggi possono cambiare sia il blocco più numeroso sia le trattative necessarie per eleggere il primo ministro e formare il prossimo governo.",
 ],
 "fonti":[
  {"url":"https://www.val.se/english/election-results/elections-to-the-riksdag-and-regional-and-municipal-councils/election-results-2026","descrizione":"Autorità elettorale svedese — calendario del conteggio, risultati preliminari e tempi previsti per la proclamazione definitiva."},
  {"url":"https://www.reuters.com/world/europe/swedish-centre-left-opposition-pole-position-take-power-after-tight-election-2026-09-14/","descrizione":"Reuters — ripartizione provvisoria 176-173, quadro politico e confronto con le elezioni del 2022."},
  {"url":"https://www.svt.se/nyheter/inrikes","descrizione":"SVT Nyheter — copertura nazionale del voto, conteggio e reazioni dei principali partiti svedesi."},
 ],
}

def save_image_variants():
 image=Image.open(SOURCE_IMAGE).convert("RGB")
 ratio=3/2
 if image.width/image.height>ratio:
  width=round(image.height*ratio); left=(image.width-width)//2; image=image.crop((left,0,left+width,image.height))
 else:
  height=round(image.width/ratio); top=(image.height-height)//2; image=image.crop((0,top,image.width,top+height))
 out=ROOT/"assets"/"images"/"editorial-auto"; out.mkdir(parents=True,exist_ok=True)
 variants=[]
 for width in (480,800,1200):
  path=out/f"{IMAGE_KEY}-{width}.webp"
  image.resize((width,round(width*2/3)),Image.Resampling.LANCZOS).save(path,"WEBP",quality=88,method=6)
  variants.append({"w":width,"src":f"/assets/images/editorial-auto/{path.name}","sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size})
 return variants

def main():
 image={"key":IMAGE_KEY,"aiGenerated":True,"documentaryPhoto":False,"variants":save_image_variants(),"alt":"Scena editoriale ordinaria ultrarealistica del Parlamento svedese a Stoccolma dopo le elezioni, con bandiere nazionali e giornalisti in lontananza.","disclosure":CAPTION,"sensitiveContext":False}
 slug=write_article(ARTICLE,image,VERSION)
 p=ROOT/"notizie"/f"{slug}.html"; page=p.read_text(encoding="utf-8")
 page=re.sub(r'"datePublished":"[^"]+"',f'"datePublished":"{PUBLISHED}"',page)
 page=re.sub(r'"dateModified":"[^"]+"',f'"dateModified":"{PUBLISHED}"',page)
 p.write_text(page,encoding="utf-8")
 ARTICLE["published"]=PUBLISHED
 register_image(image,slug,VERSION)
 sync_surfaces([ARTICLE],f"/notizie/{slug}.html",VERSION)
 for name in ("RELEASE-STATE.json","CURIOMONDO-RELEASE-STATE.json"):
  q=ROOT/name
  if q.exists():
   state=json.loads(q.read_text(encoding="utf-8"))
   if "version" in state: state["version"]=VERSION
   q.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
 print(json.dumps({"status":"ok","version":VERSION,"slug":slug},ensure_ascii=False))
if __name__=="__main__": main()
