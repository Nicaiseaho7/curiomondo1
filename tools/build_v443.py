#!/usr/bin/env python3
"""Pubblica calcio femminile, Villa Medici e Batman Day."""
from __future__ import annotations

import hashlib, json, re, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 443

def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def variants(source, key):
    image = Image.open(source).convert("RGB")
    ratio = 3 / 2
    if image.width / image.height > ratio:
        w = round(image.height * ratio); left = (image.width - w) // 2
        image = image.crop((left, 0, left + w, image.height))
    else:
        h = round(image.width / ratio); top = (image.height - h) // 2
        image = image.crop((0, top, image.width, top + h))
    out = ROOT / "assets/images/editorial-auto"; out.mkdir(parents=True, exist_ok=True)
    result = []
    for width in (480, 800, 1200):
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=86, method=6)
        result.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return result

def publish(article, image, timestamp):
    slug = write_article(article, image, VERSION)
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{timestamp}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{timestamp}"', page)
    path.write_text(page, encoding="utf-8")
    article["published"] = timestamp
    register_image(image, slug, VERSION)
    write_json(ROOT / "contenuti/notizie" / f"{slug}.json", {"slug": slug, "title": article["titolo"], "excerpt": article["sommario"], "category": article["categoria"], "published_at": timestamp, "updated_at": timestamp, "development_at": "2026-09-19", "status": article["stato"], "public_url": f"https://curiomondo.it/notizie/{slug}.html", "publication_state": "pending_deploy", "body": article["paragrafi"], "sources": article["fonti"], "image": image})
    return slug

SPORT = {
 "slug":"juventus-roma-finale-serie-a-womens-cup-19-settembre-2026",
 "titolo":"Juventus-Roma, oggi la finale della Serie A Women’s Cup",
 "sommario":"Le due squadre tornano a contendersi il trofeo dopo la finale del 2025. Le bianconere difendono il titolo nella seconda edizione del torneo.",
 "categoria":"Sport", "luogo":"Italia", "formato":"standard", "stato":"UFFICIALE",
 "parole_chiave_titolo":["Juventus-Roma","finale"],
 "dati_chiave":[{"icona":"◆","valore":"33ª","etichetta":"sfida tra Juventus e Roma in tutte le competizioni"},{"icona":"●","valore":"21","etichetta":"vittorie bianconere nei 32 precedenti"},{"icona":"↗","valore":"2ª","etichetta":"edizione della Serie A Women’s Cup"}],
 "paragrafi":[
  "Juventus Women e Roma si affrontano sabato 19 settembre nella finale della Serie A Women’s Cup. Le bianconere cercano di difendere il titolo conquistato nella prima edizione; le giallorosse tornano all’ultimo atto con l’obiettivo di ribaltare l’esito del 2025.",
  "La Juventus ha raggiunto la finale superando l’Inter 2-1 in semifinale, con reti di Eva Schatzer e Michela Cambiaghi. Il percorso conferma la solidità della squadra nelle gare a eliminazione diretta. La Roma arriva alla sfida dopo avere costruito il proprio cammino in un torneo che apre la stagione nazionale.",
  "Il confronto sarà il trentatreesimo tra i due club in tutte le competizioni. Il bilancio indicato dalla Juventus conta 21 successi bianconeri, otto romanisti e tre pareggi. Tra questi c’è l’1-1 della Supercoppa 2022, poi vinta dalla Roma ai rigori.",
  "Il precedente più vicino è proprio la finale inaugurale della Women’s Cup. Nel settembre 2025 la Juventus vinse 3-2 al termine di una partita decisa nel finale. Quel risultato offre un confronto utile, ma non misura i rapporti di forza attuali: rose, condizione e avvio stagionale sono cambiati.",
  "La Women’s Cup è la coppa di lega riservata alle squadre della Serie A femminile. La formula separa una fase iniziale e gli incontri a eliminazione diretta, creando un primo trofeo prima del pieno sviluppo del campionato. Per le finaliste rappresenta anche un test competitivo ad alta pressione.",
  "Un dato individuale accompagna la vigilia: Schatzer può andare a segno in semifinale e finale per la seconda edizione consecutiva. La statistica non costituisce una previsione, ma segnala il peso già assunto dalla centrocampista nelle partite decisive della competizione.",
  "La sfida mette quindi di fronte la detentrice del trofeo e la rivale battuta un anno fa. Il risultato assegnerà il primo titolo nazionale della stagione e offrirà una prima indicazione sul livello delle due squadre, senza sostituire il giudizio che arriverà dal campionato."],
 "fonti":[
  {"url":"https://www.juventus.com/en/news/articles/preview-juventus-women-vs-roma-serie-a-women-s-cup-final-18-09-26","descrizione":"Juventus — anteprima ufficiale della finale e precedenti."},
  {"url":"https://www.juventus.com/it/video/serie-a-women-s-cup-la-conferenza-stampa-prima-della-finale-juve-roma","descrizione":"Juventus — conferenza stampa ufficiale con Martina Lenzini e Isaac Guerrero."},
  {"url":"https://www.figc.it/it/femminile/competizioni/serie-a-women-s-cup/competizione/","descrizione":"FIGC — pagina ufficiale della Serie A Women’s Cup."}],
 "correlati":[{"url":"/notizie/serie-a-quinta-giornata-orari-tv-monza-sassuolo-roma-inter-18-settembre-2026.html","titolo":"Serie A, orari e partite della quinta giornata"}]
}

FILM = {
 "slug":"villa-medici-film-festival-programma-19-settembre-2026",
 "titolo":"Villa Medici, il festival porta oggi cinema e arte nei giardini",
 "sommario":"La sesta edizione prosegue a Roma con concorso internazionale, incontri e proiezioni all’aperto. In cartellone quasi 40 appuntamenti fino al 20 settembre.",
 "categoria":"Film e serie TV", "luogo":"Roma", "formato":"standard", "stato":"UFFICIALE",
 "parole_chiave_titolo":["Villa Medici","cinema e arte"],
 "dati_chiave":[{"icona":"◆","valore":"40","etichetta":"proiezioni circa tra sale e giardini"},{"icona":"●","valore":"12","etichetta":"film nel concorso internazionale"},{"icona":"↗","valore":"20/9","etichetta":"giornata conclusiva del festival"}],
 "paragrafi":[
  "Il Villa Medici Film Festival prosegue sabato 19 settembre a Roma con proiezioni, incontri e appuntamenti nei giardini dell’Accademia di Francia. La sesta edizione, aperta il 16 settembre, riunisce quasi 40 proiezioni e termina domenica 20.",
  "Il programma è diviso in tre sezioni. Il concorso internazionale presenta dodici opere recenti senza separare corti, mediometraggi e lungometraggi. Focus raccoglie film d’artista, scelte dei giurati e incontri; le serate nel piazzale sono dedicate ad anteprime e classici restaurati.",
  "Tra gli appuntamenti di oggi figura An Incomplete Calendar di Sanaz Sohrabi, film costruito intorno a un disco del 1980 legato all’OPEC. At Night di Beatrice Gibson attraversa invece una Parigi notturna seguendo sei donne. Le opere sono proposte in versione originale con sottotitoli indicati nel programma.",
  "La selezione non usa la durata come criterio gerarchico. Un film di sedici minuti può concorrere accanto a un’opera di oltre un’ora. Questa scelta rende il festival diverso dai calendari organizzati per formato e permette di confrontare direttamente linguaggi documentari, sperimentali e di finzione.",
  "L’edizione 2026 è dedicata alla memoria di Lili Hinstin, programmatrice e direttrice artistica morta quest’anno. Hinstin aveva lavorato a Villa Medici dal 2005 al 2010 e aveva poi sostenuto la nascita del festival, partecipando al comitato di selezione e organizzazione.",
  "I biglietti singoli costano cinque euro. Il pass per tre proiezioni è indicato a nove euro, con tariffa ridotta per gli aventi diritto; il pass completo parte da 25 euro. Alcune aree hanno accessibilità parziale, quindi l’organizzazione invita le persone con mobilità ridotta a contattare la sede prima della visita.",
  "Il festival affianca al cinema anche una cena nei giardini legata alla proiezione L’inconnue. L’iniziativa mette in dialogo cucina popolare, paesaggio e pratiche artistiche. I posti sono limitati e la prenotazione anticipata è richiesta sul circuito indicato da Villa Medici per l’appuntamento serale."],
 "fonti":[
  {"url":"https://villamedici.it/en/programme/film-festival-2026/","descrizione":"Villa Medici — programma ufficiale, orari, opere e informazioni pratiche."},
  {"url":"https://www.culture.gouv.fr/","descrizione":"Ministero della Cultura francese — istituzione di riferimento dell’Accademia di Francia a Roma."},
  {"url":"https://www.unifrance.org/","descrizione":"Unifrance — partner istituzionale del festival e rete del cinema francese."}],
 "correlati":[{"url":"/notizie/hunger-games-alba-mietitura-trailer-italiano-19-novembre-2026.html","titolo":"Hunger Games, il trailer italiano di Alba sulla mietitura"}]
}

BATMAN = {
 "slug":"batman-day-2026-italia-two-worlds-19-settembre-2026",
 "titolo":"Batman Day 2026: in Italia debutta “Batman of Two Worlds”",
 "sommario":"DC celebra oggi il personaggio con un albo speciale e iniziative nelle fumetterie. L’uscita mette a confronto due versioni del Cavaliere Oscuro.",
 "categoria":"Curiosità", "luogo":"Italia", "formato":"standard", "stato":"UFFICIALE",
 "parole_chiave_titolo":["Batman Day 2026","Batman of Two Worlds"],
 "dati_chiave":[{"icona":"◆","valore":"2","etichetta":"versioni di Batman nello stesso albo"},{"icona":"●","valore":"5","etichetta":"nuove edizioni cartonate annunciate"},{"icona":"↗","valore":"89","etichetta":"anni dal debutto editoriale del personaggio"}],
 "paragrafi":[
  "DC celebra sabato 19 settembre il Batman Day 2026 con il debutto mondiale di Batman of Two Worlds. L’albo speciale accosta una storia del Batman dell’universo principale a una dell’Absolute Universe. In Italia l’uscita è sostenuta da Panini Comics e dalle fumetterie aderenti.",
  "La prima storia è firmata dallo sceneggiatore Matt Fraction e dal disegnatore Javi Fernández. La seconda riunisce Scott Snyder e Nick Derington. Entrambe partono dal tema del furto, ma osservano come due Bruce Wayne diversi definiscono giustizia e risposta al crimine.",
  "Il confronto funziona perché l’Absolute Batman è costruito senza la fortuna, la villa e le risorse tradizionalmente associate al personaggio. L’albo non mette semplicemente due costumi sulla stessa copertina: usa lo stesso problema narrativo per mostrare quanto ambiente e mezzi cambino il metodo dell’eroe.",
  "DC ha annunciato anche quattro maschere di carta distribuite nei negozi partecipanti e cinque nuove edizioni cartonate. Tra queste figurano Batman ’89, Batman: H2SH Volume One e una versione deluxe di The Dark Knight Returns. Disponibilità e iniziative possono cambiare da una fumetteria all’altra.",
  "Per il mercato italiano è prevista la pubblicazione in contemporanea di Batman: H2SH Volume One. DC segnala inoltre materiali promozionali, spille e un incontro con il disegnatore Corrado Roi a Milano. Per conoscere sedi e quantità disponibili occorre verificare direttamente con il rivenditore.",
  "La ricorrenza cade ogni anno a settembre, ma non corrisponde alla data del debutto di Batman. Il personaggio apparve nel 1939 su Detective Comics n. 27. Il Batman Day è quindi una celebrazione editoriale moderna, usata per coordinare uscite, letture e attività locali.",
  "La piattaforma digitale DC propone anche una selezione di fumetti leggibili gratuitamente, con limiti territoriali e di account. Il programma 2026 mostra così le due funzioni della giornata: richiamare i lettori storici nelle fumetterie e offrire un punto d’ingresso a chi conosce Batman soprattutto attraverso cinema e videogiochi."],
 "fonti":[
  {"url":"https://www.dc.com/blog/2026-09-02/batman-day-2026","descrizione":"DC — comunicato ufficiale sul Batman Day 2026 e sulle iniziative italiane."},
  {"url":"https://www.dc.com/blog/2026-09-18/which-batman-fan-are-you-a-batman-day-2026-reading-guide","descrizione":"DC — guida ufficiale alle uscite pubblicata alla vigilia."},
  {"url":"https://www.dc.com/news","descrizione":"DC — newsroom ufficiale e aggiornamenti sul programma."}],
 "correlati":[{"url":"/notizie/spider-man-brand-new-day-record-box-office-nord-america-17-settembre-2026.html","titolo":"Spider-Man: Brand New Day, record al box office"}]
}

def main():
    articles = [SPORT, FILM, BATMAN]
    files = ["womens-cup-v443.png", "villa-medici-v443.png", "batman-day-v443.png"]
    prompts = ["Finale italiana di calcio femminile, squadre in bianconero e rosso prima del calcio d’inizio, fotografia editoriale, senza testo.", "Festival cinematografico contemporaneo nei giardini di Villa Medici al tramonto, fotografia editoriale, senza testo.", "Fumetteria italiana con proiezione luminosa a forma di pipistrello per una celebrazione dei fumetti, fotografia editoriale, senza testo."]
    alts = ["Scena editoriale contestuale generata con IA: due squadre di calcio femminile in bianconero e rosso si preparano alla finale; non è una fotografia documentaria.", "Scena editoriale contestuale generata con IA: proiezione cinematografica nei giardini di Villa Medici a Roma; non è una fotografia documentaria.", "Scena editoriale contestuale generata con IA: fumetteria con simbolo luminoso a forma di pipistrello per il Batman Day; non è una fotografia documentaria."]
    timestamps = ["2026-09-19T09:57:00+02:00", "2026-09-19T09:59:00+02:00", "2026-09-19T10:01:00+02:00"]
    slugs = []
    for article, filename, prompt, alt, stamp in zip(articles, files, prompts, alts, timestamps):
        image = {"key":f"{article['slug']}-v{VERSION}", "aiGenerated":True, "documentaryPhoto":False, "generator":"ChatGPT/OpenAI image generation", "variants":variants(ROOT / "generated_images" / filename, f"{article['slug']}-v{VERSION}"), "alt":alt, "disclosure":CAPTION, "sensitiveContext":False, "reenactedEvent":False, "prompt":prompt}
        slugs.append(publish(article, image, stamp))
    sync_surfaces(articles, "", VERSION)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version":VERSION,"site_version":VERSION})
    manifest.update({"site_version":VERSION,"version":f"v{VERSION}","release_version":f"v{VERSION}"})
    manifest["last_release"] = {"version":VERSION,"date":"2026-09-19","type":"content-release","news_added":slugs,"news_updated":[],"change":"Calcio femminile, Villa Medici e Batman Day","image_policy_applied":"new-openai-contextual-editorial-images"}
    write_json(manifest_path, manifest)
    for filename in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / filename
        if path.exists():
            state = json.loads(path.read_text(encoding="utf-8")); state.update({"currentVersion":VERSION,"site_version":VERSION,"version":str(VERSION),"date":"2026-09-19","release_date":"2026-09-19","articleCount":int(state.get("articleCount",0))+3,"generatedEditorialImages":int(state.get("generatedEditorialImages",0))+3,"last_update":"news-v443"}); write_json(path,state)
    write_json(ROOT / "automation/logs/editoriale-20260919T100100-Europe-Rome.json", {"run_at":"2026-09-19T10:01:00+02:00","skill":"editoriale-fonti-primarie","processed":[{"title":a["titolo"],"decision":"publish","public_url":f"https://curiomondo.it/notizie/{s}.html"} for a,s in zip(articles,slugs)]})

if __name__ == "__main__": main()
