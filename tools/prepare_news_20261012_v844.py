#!/usr/bin/env python3
"""Prepara il lotto v844; nessuna operazione remota o lettura del manifest."""
import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo
from PIL import Image, ImageOps
from lxml import html

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from automation.newsroom import site
from tools.publish_notte_mattina_20261010_v827 import set_published
from tools.publish_finale_20261010_v836 import correct_visible_date
VERSION=844
PHRASES=(
    "Puoi spegnere le notifiche mentre ti riposi.",
    "Se sei stanco, chiedi di rimandare l'appuntamento.",
    "Puoi farti accompagnare quando non vuoi andare da solo.",
    "Se hai freddo, concediti una coperta in più.",
    "Puoi correggere una scelta senza giustificarti con tutti.",
    "Oggi puoi lasciare una faccenda a domani.",
    "Prima di uscire, prenditi il tempo di mangiare.",
    "Puoi dire che hai bisogno di silenzio.",
    "Se non senti bene, chiedi di ripetere.",
    "Puoi tenere per te una cosa che non vuoi raccontare.",
)
GUIDES={
    "agcom":("phishing-smishing-vishing-come-riconoscere-truffe", "Phishing, smishing e vishing: riconoscere le truffe digitali", "I segnali da controllare prima di fidarsi di un messaggio o di una chiamata."),
    "russia":("come-funzionano-sanzioni-unione-europea", "Come funzionano le sanzioni dell'Unione europea", "Gli strumenti europei, i destinatari e i limiti delle misure restrittive."),
}

def set_times(rows):
    release=datetime.now(ZoneInfo("Europe/Rome")).replace(microsecond=0)
    offsets=(0,5,11,18,26,35,45,56,68,81)
    for a,minutes in zip(rows,offsets):
        stamp=release-timedelta(minutes=minutes)
        set_published(a["slug"],stamp)
        correct_visible_date(a["slug"],stamp,a["luogo"])
    return release

def main():
    rows=json.loads((ROOT/"tools/news_batch_20261012_v844.json").read_text())
    source_map=json.loads((ROOT/"tools/news_images_20261012_v844.json").read_text())
    if sys.argv[1:]==["--refresh-times"]:
        release=set_times(rows)
        site.sync_surfaces(rows,"/notizie/"+rows[0]["slug"]+".html",VERSION,update_manifest=False)
        print(release.isoformat());return
    for a in rows:
        if (ROOT/"notizie"/(a["slug"]+".html")).exists():
            raise SystemExit("Articolo già presente: "+a["slug"])
    p=ROOT/"assets/data/frasi-nome.json";phrases=json.loads(p.read_text())
    phrases.extend(x for x in PHRASES if x not in phrases)
    p.write_text(json.dumps(phrases,ensure_ascii=False,indent=2)+"\n")
    images=[]
    for a in rows:
        key=a["image_key"]
        source=ROOT.parent/"generated_images"/source_map[key]
        im=ImageOps.fit(Image.open(source).convert("RGB"),(1600,900),method=Image.Resampling.LANCZOS)
        variants=[]
        for w in (480,800,1200):
            h=round(w*9/16)
            path=ROOT/"assets/images/editorial-auto"/f"{a['slug']}-v{VERSION}-{w}.webp"
            im.resize((w,h),Image.Resampling.LANCZOS).save(path,"WEBP",quality=89,method=6)
            variants.append({"w":w,"h":h,"src":"/assets/images/editorial-auto/"+path.name,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"bytes":path.stat().st_size})
        image={"id":a["slug"],"article":"/notizie/"+a["slug"]+".html","alt":a["image_alt"],"prompt":source_map.get(key+"_prompt",a["titolo"]+"; illustrazione editoriale non documentaria."),"variants":variants,"disclosure":site.CAPTION,"generator":"OpenAI image generation","aiGenerated":True,"documentaryPhoto":False,"officialArtwork":False,"sensitiveContext":key in ("russia","libano"),"weatherMap":False,"reenactedEvent":False,"logoApplied":False}
        if a.get("likeness"):
            image.update({"syntheticLikeness":"public-figure","publicFigureName":a["likeness"]})
        slug=site.write_article(a,image,VERSION)
        images.append(image)
        if key in GUIDES:
            guide,title,summary=GUIDES[key]
            if not (ROOT/"approfondimenti"/(guide+".html")).exists():raise RuntimeError("Guida mancante")
            path=ROOT/"notizie"/(slug+".html");doc=html.fromstring(path.read_text())
            body=doc.xpath('//article[contains(@class,"art-body")]')[0]
            block=html.fragment_fromstring('<aside class="cm-evergreen-reader"><p>Approfondimento</p><h2>'+title+'</h2><p>'+summary+'</p><a href="/approfondimenti/'+guide+'.html">Leggi l’approfondimento →</a></aside>')
            body.addnext(block)
            path.write_text(html.tostring(doc,encoding="unicode",method="html",doctype="<!doctype html>")+"\n")
    release=set_times(rows)
    p=ROOT/"assets/data/editorial-images-v210.json";registry=json.loads(p.read_text())
    registry["items"]=images+registry["items"];registry["version"]=VERSION
    p.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+"\n")
    site.sync_surfaces(rows,images[0]["article"],VERSION,update_manifest=False)
    p=ROOT/"CURIOMONDO-RELEASE-STATE.json";state=json.loads(p.read_text())
    state.update({"site_version":VERSION,"currentVersion":VERSION,"version":str(VERSION),"articleCount":int(state["articleCount"])+len(rows),"generatedEditorialImages":int(state["generatedEditorialImages"])+len(rows),"last_update":"ultime-notizie-v844","date":release.date().isoformat(),"release_date":release.date().isoformat(),"updated_at":release.isoformat(),"status":"ready"})
    p.write_text(json.dumps(state,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"version":VERSION,"new_articles":len(rows),"slugs":[a["slug"] for a in rows]},ensure_ascii=False))

if __name__=="__main__":main()
