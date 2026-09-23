#!/usr/bin/env python3
"""Pubblica le quattro notizie selezionate dall'editore il 23 settembre 2026."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 528
GEN = ROOT.parent / "generated_images"

ARTICLES = [
    {
        "slug": "lazio-15-risorse-genetiche-anagrafe-biodiversita-22-settembre-2026",
        "titolo": "Biodiversità, 15 risorse genetiche del Lazio entrano nell’Anagrafe nazionale",
        "sommario": "Il decreto del Ministero dell’Agricoltura riguarda risorse locali a rischio di erosione genetica. L’iscrizione riconosce il loro interesse agricolo e alimentare.",
        "categoria": "Ambiente", "luogo": "Lazio", "formato": "flash",
        "parole_chiave_titolo": ["15 risorse genetiche", "Lazio"],
        "dati_chiave": [{"valore":"15","etichetta":"risorse genetiche locali"},{"valore":"22 settembre","etichetta":"data del decreto"},{"valore":"Lazio","etichetta":"regione interessata"}],
        "paragrafi": [
            "Quindici risorse genetiche locali del Lazio a rischio di erosione genetica sono state iscritte nell’Anagrafe nazionale della biodiversità di interesse agricolo e alimentare. L’atto è contenuto nel decreto ministeriale numero 493412 del 22 settembre 2026.",
            "L’iscrizione certifica l’interesse delle risorse per il patrimonio agricolo e alimentare italiano e le inserisce nel sistema nazionale di tutela. Il decreto non equivale però, da solo, a un finanziamento automatico né garantisce che le varietà siano già diffuse nelle coltivazioni commerciali.",
            "Il rischio di erosione genetica riguarda la progressiva perdita di varietà e popolazioni locali, spesso sostituite da un numero ristretto di colture uniformi. Conservare questo materiale mantiene disponibili caratteristiche che possono risultare utili per ricerca, adattamento climatico e produzioni territoriali.",
            "Il passaggio successivo è l’attuazione delle misure di conservazione previste dal sistema nazionale e regionale. L’elenco ufficiale allegato al decreto resta il riferimento per identificare con precisione tutte le quindici risorse riconosciute."
        ],
        "fonti": [{"url":"https://www.masaf.gov.it/flex/cm/pages/ServeBLOB.php/L/IT/IDPagina/25178","descrizione":"MASAF — decreto n. 493412 del 22 settembre 2026 e iscrizione delle quindici risorse genetiche locali."}],
        "image": "exec-ab0e0fe8-1ec7-482b-833b-7de23ba626d3.png",
        "alt": "Illustrazione editoriale IA di una banca dei semi del Lazio con campioni agricoli locali catalogati; scena non documentaria.",
        "primary": "ambiente", "priority": 91,
    },
    {
        "slug": "istat-matrice-pendolarismo-studenti-comuni-censimento-2021",
        "titolo": "Istat pubblica la matrice degli spostamenti degli studenti tra i comuni",
        "sommario": "Il dataset ricostruisce i tragitti abituali per studio dentro lo stesso comune e tra comuni diversi. I dati si riferiscono al Censimento 2021.",
        "categoria": "Italia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Istat", "spostamenti degli studenti"],
        "dati_chiave": [{"valore":"2021","etichetta":"censimento di riferimento"},{"valore":"3 giorni","etichetta":"frequenza minima settimanale"},{"valore":"23 settembre","etichetta":"ultimo aggiornamento"}],
        "paragrafi": [
            "L’Istat ha pubblicato la matrice origine-destinazione degli spostamenti abituali per motivi di studio, aggiornata il 23 settembre. Il file misura quante persone si muovono all’interno dello stesso comune o tra comuni differenti sulla base del Censimento permanente 2021.",
            "La popolazione considerata comprende residenti in famiglia o in convivenza che raggiungono il luogo abituale di studio almeno tre giorni alla settimana e rientrano quotidianamente nell’alloggio di residenza. Il riferimento temporale dei dati è il 31 dicembre 2021.",
            "La matrice consente analisi territoriali su mobilità scolastica, relazioni tra comuni e domanda potenziale di trasporto. Non descrive però tutti gli spostamenti occasionali e non rappresenta automaticamente la situazione del 2026, perché fotografa l’edizione censuaria indicata.",
            "Istat accompagna il dataset con una nota metodologica sulle fonti impiegate e sul processo di stima. Per confrontare singoli territori è quindi necessario considerare insieme valori, periodo di riferimento e criteri usati per costruire la base statistica."
        ],
        "fonti": [{"url":"https://www.istat.it/notizia/matrice-di-pendolarismo-per-studio/","descrizione":"Istat — dataset, periodo di riferimento, popolazione osservata e nota metodologica."}],
        "image": "exec-2d206de9-a5a7-49a1-ad11-91e19a1b9dde.png",
        "alt": "Illustrazione editoriale IA di studenti pendolari in un nodo ferroviario e autobus italiano; scena non documentaria.",
        "primary": "italia", "priority": 90,
    },
    {
        "slug": "unity-euro-cup-2026-coverciano-sorteggio-22-squadre",
        "titolo": "Unity EURO Cup 2026 a Coverciano: record di 22 squadre",
        "sommario": "Il torneo UEFA e UNHCR sarà ospitato per la prima volta dall’Italia il 15 ottobre. Il sorteggio è in programma il 23 settembre.",
        "categoria": "Sport", "luogo": "Coverciano", "formato": "flash",
        "parole_chiave_titolo": ["Unity EURO Cup", "22 squadre"],
        "dati_chiave": [{"valore":"22","etichetta":"squadre partecipanti"},{"valore":"400","etichetta":"atleti e membri degli staff"},{"valore":"15 ottobre","etichetta":"data del torneo"}],
        "paragrafi": [
            "La quinta Unity EURO Cup si giocherà il 15 ottobre 2026 a Coverciano e sarà ospitata per la prima volta dall’Italia. La competizione promossa dalla UEFA con UNHCR raggiunge il record di 22 squadre e circa 400 partecipanti tra atleti e componenti degli staff.",
            "Ventuno rappresentative provengono da federazioni calcistiche europee; la ventiduesima rappresenta l’Unione europea. Le squadre riuniscono rifugiati e membri delle comunità locali, con un formato costruito attorno a inclusione e partecipazione attraverso il calcio.",
            "Il sorteggio è previsto il 23 settembre al Centro Tecnico Federale, con inizio della cerimonia alle 14:30 e diretta su Vivo Azzurro TV dalle 14:45. Gli abbinamenti saranno definitivi soltanto al termine dell’evento.",
            "L’Italia parteciperà con il Refugee Team Italy, selezionato attraverso il percorso organizzato a giugno a Coverciano con calciatori rifugiati di 13 nazionalità. Dal 2025 la Unity EURO Cup è una competizione ufficiale UEFA."
        ],
        "fonti": [{"url":"https://www.figc.it/it/federazione/news/unity-euro-cup-2026-il-23-settembre-a-coverciano-il-sorteggio-della-quinta-edizione-fwukhfop","descrizione":"FIGC — squadre, partecipanti, orari del sorteggio e data della competizione."}],
        "image": "exec-df353b7f-c067-4977-92dd-73a5c2a715f6.png",
        "alt": "Illustrazione editoriale IA del sorteggio della Unity EURO Cup nel centro tecnico di Coverciano; scena non documentaria.",
        "primary": "sport", "priority": 89,
    },
    {
        "slug": "antonio-costa-onu-piano-pace-gaza-due-stati-23-settembre-2026",
        "titolo": "Gaza, Costa all’ONU chiede l’attuazione della roadmap per la pace",
        "sommario": "Il presidente del Consiglio europeo indica ritiro israeliano, disarmo di Hamas, forza internazionale e amministrazione palestinese tra i passaggi necessari.",
        "categoria": "Mondo", "luogo": "New York", "formato": "flash",
        "parole_chiave_titolo": ["Costa", "roadmap per la pace"],
        "dati_chiave": [{"valore":"22 settembre","etichetta":"data dell’intervento"},{"valore":"2 Stati","etichetta":"soluzione sostenuta dall’UE"},{"valore":"2 milioni","etichetta":"persone richiamate nel discorso"}],
        "paragrafi": [
            "Il presidente del Consiglio europeo António Costa ha chiesto a New York la piena attuazione della roadmap internazionale per Gaza. L’intervento è stato pronunciato il 22 settembre durante una riunione ad alto livello a margine dell’Assemblea generale delle Nazioni Unite; il testo è stato pubblicato il 23 settembre.",
            "Costa ha indicato quattro passaggi: disarmo di Hamas, ritiro di Israele, dispiegamento di una forza internazionale di stabilizzazione e ingresso a Gaza di un comitato nazionale incaricato dell’amministrazione. Si tratta della posizione espressa dal presidente del Consiglio europeo, non dell’annuncio di un nuovo accordo raggiunto durante la riunione.",
            "Nel discorso, Costa ha sostenuto che l’accesso degli aiuti resta insufficiente e ha richiamato la condizione di circa due milioni di persone esposte a un altro inverno tra tende e macerie. Il dato e la valutazione sono attribuiti all’intervento istituzionale dell’Unione europea.",
            "Per la Cisgiordania, compresa Gerusalemme Est, Costa ha denunciato gli ostacoli quotidiani alla soluzione dei due Stati. Ha ribadito la posizione europea a favore di Israele e di uno Stato palestinese indipendente, democratico, contiguo, sovrano e sostenibile, capaci di vivere fianco a fianco in sicurezza e con reciproco riconoscimento.",
            "La riunione è stata co-organizzata da Francia, Regno Unito e Canada nel quadro della settimana di alto livello dell’ONU. Il governo britannico aveva confermato la partecipazione al vertice dedicato alla soluzione dei due Stati; l’attuazione concreta dei passaggi citati dipenderà dalle decisioni dei soggetti coinvolti e dagli organismi internazionali competenti."
        ],
        "fonti": [
            {"url":"https://www.consilium.europa.eu/it/press/press-releases/2026/09/23/remarks-by-president-antonio-costa-at-the-high-level-international-meeting-on-the-two-state-solution-and-the-comprehensive-peace-plan-for-gaza/","descrizione":"Consiglio europeo — testo integrale dell’intervento di António Costa e passaggi della roadmap."},
            {"url":"https://www.gov.uk/government/news/prime-minister-drives-global-work-on-artificial-intelligence-at-unga-as-uk-and-us-make-history-with-firing-from-undersea-drone","descrizione":"Governo britannico — conferma della riunione ad alto livello sulla soluzione dei due Stati durante l’Assemblea generale ONU."}
        ],
        "image": "exec-8008bf9b-8b6a-45cb-81c7-7408f29f3115.png",
        "alt": "Illustrazione editoriale IA neutrale di una sala diplomatica ONU con bandiere europea, ONU, israeliana e palestinese; scena non documentaria.",
        "primary": "mondo", "priority": 87, "sensitive": True,
    },
]


def make_image(a):
    src = GEN / a["image"]
    im = Image.open(src).convert("RGB")
    w, h = im.size
    target = 1.5
    if w / h > target:
        nw = round(h * target); im = im.crop(((w-nw)//2, 0, (w-nw)//2+nw, h))
    else:
        nh = round(w / target); im = im.crop((0, (h-nh)//2, w, (h-nh)//2+nh))
    variants = []
    for width in (480, 800, 1200):
        p = ROOT / "assets/images/editorial-auto" / f'{a["slug"]}-v{VERSION}-{width}.webp'
        im.resize((width, round(width / target)), Image.Resampling.LANCZOS).save(p, "WEBP", quality=87, method=6)
        variants.append({"w":width,"src":f"/assets/images/editorial-auto/{p.name}","sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size})
    return {"key":f'{a["slug"]}-v{VERSION}',"alt":a["alt"],"variants":variants,"disclosure":site.CAPTION,"generator":"OpenAI image tool","sensitiveContext":bool(a.get("sensitive"))}


def main():
    for a in ARTICLES:
        image = make_image(a)
        site.write_article(a, image, VERSION)
        site.register_image(image, a["slug"], VERSION)
    site.sync_surfaces(ARTICLES, f'/notizie/{ARTICLES[0]["slug"]}.html', VERSION)
    cfgp = ROOT / "assets/data/homepage-config-v504.json"
    cfg = json.loads(cfgp.read_text()); cfg["version"] = VERSION
    for a in ARTICLES:
        cfg["articles"][f'/notizie/{a["slug"]}.html'] = {"firstPublishedAt":a["published"],"homepagePriority":a["priority"],"primaryCategory":a["primary"]}
    cfgp.write_text(json.dumps(cfg, ensure_ascii=False, indent=2)+"\n")
    mp = ROOT / "curiomondo-site-manifest.json"; m = json.loads(mp.read_text())
    m["site"]["current_site_version"] = VERSION; m["site"]["site_version"] = VERSION
    m["site_version"] = VERSION; m["version"] = f"v{VERSION}"; m["release_version"] = f"v{VERSION}"
    m["last_release"] = {"version":VERSION,"date":"2026-09-23","type":"environment-data-sport-world","news_added":[a["slug"] for a in ARTICLES],"news_updated":[],"change":"Quattro nuove notizie selezionate dall’editore"}
    mp.write_text(json.dumps(m, ensure_ascii=False, indent=2)+"\n")
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        p=ROOT/name; d=json.loads(p.read_text()); d.update(site_version=VERSION,version=str(VERSION),currentVersion=VERSION,last_update="selected-all-v528"); p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({"added":[a["slug"] for a in ARTICLES]},ensure_ascii=False))


if __name__ == "__main__":
    main()
