#!/usr/bin/env python3
"""Pubblica sport, politica e streaming del 20 settembre 2026."""
from __future__ import annotations

import hashlib, json, re, shutil, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tools")]
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 453
DATE = "2026-09-20"
STAMP = "2026-09-20T10:05:00+02:00"

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

ARTICLES = [
    {
        "slug": "roma-inter-2-2-lautaro-doppietta-rimonta-19-settembre-2026",
        "titolo": "Roma-Inter 2-2: Lautaro firma la rimonta con una doppietta",
        "sommario": "I giallorossi chiudono il primo tempo avanti di due gol con Koné. Il capitano nerazzurro pareggia nella ripresa e lascia tre squadre a 13 punti.",
        "categoria": "Sport", "luogo": "Roma", "formato": "standard", "stato": "CONFERMATA DA PIÙ FONTI",
        "parole_chiave_titolo": ["Roma-Inter 2-2", "Lautaro"],
        "dati_chiave": [{"icona":"◆","valore":"2-2","etichetta":"risultato finale all’Olimpico"},{"icona":"●","valore":"2 gol","etichetta":"doppietta di Lautaro Martínez"},{"icona":"▦","valore":"13 punti","etichetta":"Roma, Inter e Lazio in vetta"}],
        "paragrafi": [
            "Roma e Inter hanno pareggiato 2-2 sabato 19 settembre allo Stadio Olimpico, nella quinta giornata di Serie A. I giallorossi hanno segnato due volte nel primo tempo con Manu Koné; Lautaro Martínez ha risposto con una doppietta nella ripresa, evitando la prima sconfitta stagionale dei nerazzurri.",
            "Koné ha sbloccato la partita al 6° minuto con un destro e ha raddoppiato al 37° con il sinistro. La Roma ha così sfruttato meglio l’avvio, mentre l’Inter non è riuscita a trasformare il possesso in occasioni sufficientemente pulite prima dell’intervallo.",
            "La reazione è cominciata subito dopo la ripresa. Lautaro ha accorciato al 46° e ha completato la rimonta al 79°, riportando l’Inter in parità. Il risultato ha premiato il cambio di intensità dei nerazzurri senza cancellare la qualità mostrata dalla Roma nella prima metà della gara.",
            "Il pareggio interrompe il percorso a punteggio pieno di entrambe le squadre. Roma e Inter salgono a 13 punti e restano davanti insieme alla Lazio, vincitrice per 2-0 contro il Venezia. Il Cagliari segue a quota 12 dopo l’1-0 ottenuto sul campo dell’Udinese.",
            "La classifica resta quindi molto corta: un singolo risultato nella prossima giornata può cambiare l’ordine delle prime posizioni. Il dato più utile non è soltanto l’imbattibilità, ma la capacità delle due squadre di reagire a fasi sfavorevoli senza perdere equilibrio nel finale.",
            "Per l’Inter, la doppietta conferma il peso di Lautaro nella produzione offensiva e nella gestione dei momenti decisivi. Per la Roma, il vantaggio costruito nel primo tempo mostra un’efficacia elevata, ma il secondo tempo segnala quanto sia difficile proteggere il risultato contro una squadra capace di alzare ritmo e pressione.",
            "La quinta giornata prosegue con gli altri incontri in calendario. Soltanto al termine del turno sarà possibile leggere distacchi e posizioni complete, mentre il 2-2 dell’Olimpico resta il primo passaggio a vuoto per due delle squadre partite meglio in campionato."
        ],
        "fonti": [
            {"url":"https://www.reuters.com/sports/soccer/martinez-nets-double-inter-come-back-draw-2-2-with-roma-2026-09-19/","descrizione":"Reuters — risultato, marcatori e situazione di classifica."},
            {"url":"https://www.legaseriea.it/","descrizione":"Lega Serie A — calendario e quadro ufficiale della quinta giornata."},
            {"url":"https://www.uol.com.br/esporte/ultimas-noticias/2026/09/19/transmissao-ao-vivo-de-roma-x-internazionale-pelo-italiano-veja-onde-assistir.ghtm","descrizione":"UOL Esporte — contesto della sfida tra le due squadre imbattute."}
        ],
        "correlati": [{"url":"/notizie/juventus-atalanta-guida-orario-tv-20-settembre-2026.html","titolo":"Juventus-Atalanta: orario, diretta TV e numeri della sfida"}],
        "source":"/workspace/scratch/63d8c74bad9c/generated_images/exec-1049e1cc-0e9b-49b7-a38f-e097ad762388.png",
        "alt":"Scena editoriale contestuale ordinaria generata con IA: Lautaro Martínez riconoscibile celebra in maglia nerazzurra con calciatori della Roma sullo sfondo; somiglianza sintetica, non è una fotografia documentaria.",
        "prompt":"Lautaro Martinez celebrating in Inter kit at the Olimpico, photorealistic ordinary editorial scene, no text.", "synthetic":"public-figure"
    },
    {
        "slug":"pontida-salvini-lega-unita-tensioni-interne-20-settembre-2026",
        "titolo":"Pontida, Salvini richiama la Lega all’unità mentre cresce il confronto interno",
        "sommario":"Il segretario rivendica il ruolo della base e respinge l’idea di una resa dei conti. Sullo sfondo pesano risultati elettorali e richieste dei governatori.",
        "categoria":"Politica", "luogo":"Pontida", "formato":"standard", "stato":"CONFERMATA DA PIÙ FONTI",
        "parole_chiave_titolo":["Salvini", "Lega all’unità"],
        "dati_chiave":[{"icona":"◆","valore":"1 raduno","etichetta":"assemblea annuale a Pontida"},{"icona":"●","valore":"Nord-Sud","etichetta":"unità territoriale rivendicata"},{"icona":"▦","valore":"3 livelli","etichetta":"base, dirigenti e governatori"}],
        "paragrafi":[
            "Matteo Salvini ha aperto il raduno della Lega a Pontida richiamando il partito all’unità e attribuendo alla base, più che ai singoli dirigenti, la forza del movimento. L’intervento arriva mentre nel partito prosegue il confronto su leadership, organizzazione e risultati elettorali.",
            "Dal palco dei giovani, il segretario ha sostenuto che la Lega può vincere soltanto se resta «forte, unita, libera e coraggiosa da nord a sud». Ha inoltre invitato militanti e amministratori a non esaltarsi nelle fasi favorevoli e a non abbattersi quando il consenso arretra.",
            "Il richiamo all’unità non cancella le differenze emerse nelle ultime settimane. Alcuni governatori chiedono un maggiore peso delle amministrazioni territoriali e una verifica della linea politica. Salvini respinge l’idea che l’identità del partito dipenda da una sola area geografica o da una singola corrente.",
            "La distinzione tra base e gruppi dirigenti è il passaggio politico più rilevante del discorso. Serve a rafforzare il rapporto diretto del segretario con i militanti, ma segnala anche che il confronto interno non è concluso. Le dichiarazioni dal palco non equivalgono a una modifica formale degli incarichi.",
            "Per il centrodestra la tenuta della Lega conta oltre i confini del partito. Fratelli d’Italia, Forza Italia e Noi Moderati dipendono dalla capacità della coalizione di presentarsi compatta, soprattutto mentre nuovi soggetti alla destra dell’alleanza contendono consenso e visibilità.",
            "I prossimi indicatori concreti saranno le decisioni sugli organismi interni, la linea sulle priorità di governo e il rapporto con i presidenti di Regione. Senza atti organizzativi o voti, parlare di scissione o cambio di leadership sarebbe prematuro.",
            "Pontida offre dunque una fotografia politica, non una soluzione definitiva. Salvini conserva il controllo della scena e chiede disciplina; governatori e dirigenti misureranno nelle settimane successive quanto spazio avranno nelle scelte del partito e nella strategia del centrodestra. Il banco di prova sarà trasformare l’appello pubblico in decisioni condivise."
        ],
        "fonti":[
            {"url":"https://www.ansa.it/sito/notizie/topnews/2026/09/19/salvini-a-pontida-la-lega-vince-solo-se-e-forte-e-unita-da-nord-a-sud_b66bafaf-8ecb-4359-8a70-c479d6ee26ec.html","descrizione":"ANSA — dichiarazioni di Salvini dal palco di Pontida."},
            {"url":"https://www.corriere.it/politica/26_settembre_19/salvini-a-pontida-tra-le-tensioni-conta-il-popolo-non-i-dirigenti-8c81a9b6-7ff4-4ace-bb21-4e31f3ab3xlk.shtml","descrizione":"Corriere della Sera — confronto interno e posizione dei governatori."},
            {"url":"https://www.facebook.com/salviniofficial/posts/nellintervista-di-oggi-al-corriere-della-sera-ho-parlato-di-pontida-e-delle-prio/1663447075349535/","descrizione":"Canale ufficiale di Matteo Salvini — priorità indicate alla vigilia del raduno."}
        ],
        "correlati":[{"url":"/notizie/centrodestra-supermedia-40-7-sotto-41-percento-19-settembre-2026.html","titolo":"Centrodestra al 40,7% nella Supermedia"}],
        "source":"/workspace/scratch/63d8c74bad9c/generated_images/exec-aae0c147-6676-42a2-8ff3-031933e5764f.png",
        "alt":"Scena editoriale contestuale ordinaria generata con IA: Matteo Salvini riconoscibile parla a un raduno della Lega a Pontida; somiglianza sintetica, non è una fotografia documentaria.",
        "prompt":"Matteo Salvini speaking at Pontida rally, photorealistic ordinary editorial scene, no text.", "synthetic":"public-figure"
    },
    {
        "slug":"netflix-novita-weekend-film-serie-20-settembre-2026",
        "titolo":"Netflix, film e serie del weekend: le novità del 20 settembre",
        "sommario":"Dal thriller ferroviario alle nuove produzioni internazionali: una guida essenziale ai titoli entrati nel catalogo italiano e alle differenze tra i formati.",
        "categoria":"Film e serie TV", "luogo":"Italia", "formato":"standard", "stato":"UFFICIALE",
        "parole_chiave_titolo":["Netflix", "film e serie del weekend"],
        "dati_chiave":[{"icona":"◆","valore":"20 settembre","etichetta":"data delle nuove aggiunte"},{"icona":"●","valore":"4 episodi","etichetta":"durata della miniserie My Sad Dead"},{"icona":"▦","valore":"3 formati","etichetta":"film, miniserie e serie"}],
        "paragrafi":[
            "Netflix aggiorna domenica 20 settembre il proprio catalogo con nuove proposte tra film e serie. La selezione del weekend comprende il film Stop! That! Train!, la miniserie horror My Sad Dead e altre produzioni internazionali segnalate nella guida ufficiale della piattaforma.",
            "Stop! That! Train! segue due addetti ferroviari coinvolti in una corsa fuori controllo. Il titolo punta su azione e commedia, con una durata da film che lo rende adatto a una visione unica. La disponibilità effettiva può variare in base al Paese e al profilo dell’abbonato.",
            "My Sad Dead è invece una miniserie horror di quattro episodi diretta dal regista cileno Pablo Larraín. Il formato breve consente di completare la storia senza l’impegno di una stagione lunga, ma conserva una struttura seriale e una progressione distribuita in più capitoli.",
            "Nella selezione di settembre compaiono anche Habeas Corpus, serie legale brasiliana ispirata a casi reali, e Minerva Academy, produzione italiana ambientata in un liceo militare di Napoli. I titoli appartengono a generi diversi e non vanno presentati come uscite equivalenti.",
            "La distinzione utile per scegliere riguarda soprattutto tempo e tono. Il film offre una storia conclusa in una sessione; la miniserie horror distribuisce tensione e svolte in quattro episodi; la serie legale e quella italiana richiedono una visione più continuativa.",
            "Netflix pubblica le date attraverso Tudum, ma il catalogo mostrato nell’app resta il riferimento operativo per l’Italia. Licenze, doppiaggio, classificazioni e orari di disponibilità possono produrre differenze temporanee rispetto alle guide internazionali.",
            "Prima di iniziare la visione conviene quindi controllare la scheda del titolo, la lingua disponibile e il numero di episodi nel proprio account. Le aggiunte del 20 settembre ampliano l’offerta del mese senza sostituire le uscite già arrivate nei giorni precedenti. Anche classificazione per età e presenza del download offline dipendono dalla singola scheda e dal piano utilizzato."
        ],
        "fonti":[
            {"url":"https://www.netflix.com/tudum/articles/what-to-watch-on-netflix-september-18-2026","descrizione":"Netflix Tudum — guida ufficiale alle uscite del weekend e titoli del 20 settembre."},
            {"url":"https://www.netflix.com/tudum/articles/new-on-netflix","descrizione":"Netflix Tudum — calendario ufficiale di film e serie di settembre 2026."},
            {"url":"https://www.netflix.com/tudum/articles/new-shows-on-netflix","descrizione":"Netflix Tudum — panoramica ufficiale delle nuove serie del 2026."}
        ],
        "correlati":[{"url":"/notizie/resident-evil-film-2026-cinema-zach-cregger-austin-abrams-19-settembre.html","titolo":"Resident Evil al cinema: il nuovo film di Zach Cregger"}],
        "source":"/workspace/scratch/63d8c74bad9c/generated_images/exec-76ab6e84-339b-4447-84bc-3373e878c11d.png",
        "alt":"Scena editoriale contestuale generata con IA: salotto italiano con televisore acceso su una selezione astratta di film e serie, senza poster o marchi leggibili; non è una fotografia documentaria.",
        "prompt":"Italian living room with streaming selection mood, photorealistic entertainment editorial scene, no text.", "synthetic":None
    }
]

def main():
    added=[]
    for i, article in enumerate(ARTICLES):
        words=sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in article["paragrafi"])
        if not 300 <= words <= 600: raise SystemExit(f"word gate {article['slug']}: {words}")
        local=ROOT / "generated_images" / f"v{VERSION}-{i}.png"
        shutil.copy2(Path(article["source"]), local)
        key=f"{article['slug']}-v{VERSION}"
        image={"key":key,"aiGenerated":True,"documentaryPhoto":False,"generator":"ChatGPT/OpenAI image generation","variants":variants(local,key),"alt":article["alt"],"disclosure":CAPTION,"sensitiveContext":False,"reenactedEvent":False,"syntheticLikeness":article["synthetic"],"prompt":article["prompt"]}
        slug=write_article(article,image,VERSION)
        article["published"]=STAMP
        register_image(image,slug,VERSION); added.append(slug)
        write_json(Path("contenuti/notizie") / f"{slug}.json", {"slug":slug,"title":article["titolo"],"excerpt":article["sommario"],"category":article["categoria"],"published_at":STAMP,"updated_at":STAMP,"development_at":DATE,"status":article["stato"],"public_url":f"https://curiomondo.it/notizie/{slug}.html","publication_state":"pending_deploy","body":article["paragrafi"],"sources":article["fonti"],"image":image})
    sync_surfaces(ARTICLES,"",VERSION)
    mp=ROOT/"curiomondo-site-manifest.json"; manifest=json.loads(mp.read_text(encoding="utf-8")); manifest["site"].update({"current_site_version":VERSION,"site_version":VERSION}); manifest.update({"site_version":VERSION,"version":f"v{VERSION}","release_version":f"v{VERSION}"}); manifest["last_release"]={"version":VERSION,"date":DATE,"type":"news-update","news_added":added,"news_updated":[],"change":"Nuove notizie su Roma-Inter, Pontida e uscite streaming","image_policy_applied":"new-openai-contextual-editorial-images"}; write_json(Path("curiomondo-site-manifest.json"),manifest)
    for name in ("RELEASE-STATE.json","CURIOMONDO-RELEASE-STATE.json"):
        p=ROOT/name; state=json.loads(p.read_text(encoding="utf-8")); state.update({"currentVersion":VERSION,"site_version":VERSION,"version":str(VERSION),"date":DATE,"release_date":DATE,"last_update":"news-update-v453","articleCount":int(state.get("articleCount",0))+3,"generatedEditorialImages":int(state.get("generatedEditorialImages",0))+3}); write_json(Path(name),state)
    write_json(Path("automation/logs/editoriale-20260920T100500-Europe-Rome.json"),{"run_at":STAMP,"processed":[{"title":a["titolo"],"decision":"publish"} for a in ARTICLES]})
    print(json.dumps({"added":added},ensure_ascii=False))

if __name__ == "__main__": main()
