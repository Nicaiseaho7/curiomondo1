#!/usr/bin/env python3
"""Pubblica il flash sull'accoltellamento a Milano del 20 settembre 2026."""
from __future__ import annotations
import hashlib, json, re, shutil, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tools")]
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 454
DATE = "2026-09-20"
STAMP = "2026-09-20T10:35:00+02:00"

def write_json(path, data):
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def variants(source, key):
    image = Image.open(source).convert("RGB")
    ratio = 1.5
    if image.width / image.height > ratio:
        width = round(image.height * ratio); left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio); top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    folder = ROOT / "assets/images/editorial-auto"
    result = []
    for width in (480, 800, 1200):
        target = folder / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(target, "WEBP", quality=86, method=6)
        result.append({"w": width, "src": f"/assets/images/editorial-auto/{target.name}", "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "bytes": target.stat().st_size})
    return result

ARTICLE = {
    "slug": "milano-lite-strada-25enne-accoltellato-gola-20-settembre-2026",
    "titolo": "Milano, 25enne accoltellato alla gola dopo una lite in strada",
    "sommario": "Il giovane è stato ricoverato in gravi condizioni al San Raffaele. I carabinieri cercano l’uomo che si è allontanato dopo l’aggressione.",
    "categoria": "Cronaca", "luogo": "Milano", "formato": "flash", "stato": "IN SVILUPPO",
    "parole_chiave_titolo": ["25enne accoltellato", "lite in strada"],
    "dati_chiave": [
        {"icona":"◆","valore":"25 anni","etichetta":"età del giovane ferito"},
        {"icona":"●","valore":"1 ricovero","etichetta":"trasporto al San Raffaele"},
        {"icona":"▦","valore":"In corso","etichetta":"ricerche dell’aggressore"}
    ],
    "paragrafi": [
        "Un uomo di 25 anni è stato ricoverato in gravi condizioni all’ospedale San Raffaele di Milano dopo essere stato ferito alla gola con un’arma da taglio nella notte tra sabato 19 e domenica 20 settembre. Sul posto sono intervenuti i carabinieri e il personale sanitario del 118.",
        "Secondo la prima ricostruzione raccolta dai militari attraverso alcuni testimoni, il giovane avrebbe litigato in strada con un altro uomo. Al culmine della discussione, quest’ultimo lo avrebbe colpito e si sarebbe poi allontanato prima dell’arrivo dei soccorsi.",
        "I carabinieri stanno cercando di identificare e rintracciare l’aggressore. Non sono stati resi noti il punto esatto della città in cui è avvenuto l’episodio, il motivo della lite né eventuali elementi recuperati dagli investigatori.",
        "La ricostruzione resta preliminare. Anche le indicazioni sulle origini delle persone coinvolte derivano dalle prime testimonianze e non costituiscono un’identificazione definitiva. Ulteriori aggiornamenti dipenderanno dalle condizioni del ferito e dagli accertamenti in corso."
    ],
    "fonti": [
        {"url":"https://www.ansa.it/lombardia/notizie/2026/09/20/lite-in-strada-25enne-accoltellato-alla-gola-a-milano_45a8c458-d5fc-4041-915d-ec4b2974380f.html","descrizione":"ANSA Lombardia — ricovero, prima ricostruzione dei carabinieri e ricerche dell’aggressore."},
        {"url":"https://www.ansa.it/lombardia/","descrizione":"ANSA Lombardia, Ultima Ora — orario di pubblicazione e classificazione della notizia; non è una conferma indipendente."}
    ],
    "correlati": [
        {"url":"/notizie/allerta-gialla-sei-regioni-temporali-19-settembre-2026.html","titolo":"Allerta gialla su sei regioni del Centro-Sud"}
    ]
}

def main():
    words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in ARTICLE["paragrafi"])
    if not 100 <= words <= 250: raise SystemExit(f"word gate: {words}")
    source = Path("/workspace/scratch/63d8c74bad9c/generated_images/exec-64e66a70-d70f-4e52-9cfd-3c79439ed6aa.png")
    local = ROOT / "generated_images" / "v454-0.png"; shutil.copy2(source, local)
    key = f"{ARTICLE['slug']}-v{VERSION}"
    image = {"key":key,"aiGenerated":True,"documentaryPhoto":False,"generator":"ChatGPT/OpenAI image generation","variants":variants(local,key),"alt":"Scena editoriale neutrale generata con IA: pattuglia dei carabinieri e ambulanza in una strada di Milano di notte, senza persone ferite né ricostruzione dell’aggressione; non è una fotografia documentaria.","disclosure":CAPTION,"sensitiveContext":True,"reenactedEvent":False,"syntheticLikeness":None,"prompt":"Neutral sensitive-context Milan emergency response scene, no victim, injury, blood, weapon, attacker or readable text."}
    slug = write_article(ARTICLE, image, VERSION); ARTICLE["published"] = STAMP; register_image(image, slug, VERSION)
    write_json(Path("contenuti/notizie") / f"{slug}.json", {"slug":slug,"title":ARTICLE["titolo"],"excerpt":ARTICLE["sommario"],"category":ARTICLE["categoria"],"published_at":STAMP,"updated_at":STAMP,"development_at":DATE,"status":ARTICLE["stato"],"public_url":f"https://curiomondo.it/notizie/{slug}.html","publication_state":"pending_deploy","body":ARTICLE["paragrafi"],"sources":ARTICLE["fonti"],"image":image})
    sync_surfaces([ARTICLE], "", VERSION)
    mp=ROOT/"curiomondo-site-manifest.json"; manifest=json.loads(mp.read_text(encoding="utf-8")); manifest["site"].update({"current_site_version":VERSION,"site_version":VERSION}); manifest.update({"site_version":VERSION,"version":f"v{VERSION}","release_version":f"v{VERSION}"}); manifest["last_release"]={"version":VERSION,"date":DATE,"type":"breaking-news","news_added":[slug],"news_updated":[],"change":"Flash in sviluppo sull’accoltellamento di un 25enne a Milano","image_policy_applied":"new-openai-sensitive-context-editorial-image"}; write_json(Path("curiomondo-site-manifest.json"),manifest)
    for name in ("RELEASE-STATE.json","CURIOMONDO-RELEASE-STATE.json"):
        p=ROOT/name; state=json.loads(p.read_text(encoding="utf-8")); state.update({"currentVersion":VERSION,"site_version":VERSION,"version":str(VERSION),"date":DATE,"release_date":DATE,"last_update":"breaking-news-v454","articleCount":int(state.get("articleCount",0))+1,"generatedEditorialImages":int(state.get("generatedEditorialImages",0))+1}); write_json(Path(name),state)
    write_json(Path("automation/logs/editoriale-20260920T103500-Europe-Rome.json"),{"run_at":STAMP,"processed":[{"title":ARTICLE["titolo"],"decision":"publish-in-development","source_count":2,"independent_confirmations":0}]})
    print(json.dumps({"added":[slug],"words":words},ensure_ascii=False))

if __name__ == "__main__": main()
