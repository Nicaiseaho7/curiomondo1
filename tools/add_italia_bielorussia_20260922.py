#!/usr/bin/env python3
"""Completa il pacchetto editoriale del 22 settembre con la biglietteria FIGC."""
import json
from pathlib import Path

from lxml import html

from publish_requested_20260922 import ROOT, VERSION, CAPTION, variants, site

SLUG = "italia-bielorussia-femminile-biglietti-firenze-13-ottobre-2026-22-09-2026"
URL = f"/notizie/{SLUG}.html"
IMAGE = {
    "key": f"{SLUG}-v{VERSION}",
    "alt": "Illustrazione IA di tifosi diretti allo stadio Franchi di Firenze; non è una fotografia della partita.",
    "variants": variants(SLUG, "exec-b1052508-0cb7-46eb-ad78-1657f070ae0f.png"),
    "disclosure": CAPTION,
    "generator": "OpenAI image tool",
    "sensitiveContext": False,
}
ARTICLE = {
    "slug": SLUG,
    "titolo": "Italia-Bielorussia femminile, biglietti in vendita per Firenze",
    "sommario": "Il ritorno dei playoff mondiali si gioca al Franchi il 13 ottobre alle 18:15. Maratona a 5 euro, ridotto a 1 euro per gli aventi diritto.",
    "categoria": "Sport",
    "luogo": "Firenze",
    "formato": "flash",
    "paragrafi": [
        "Sono in vendita dal 22 settembre i biglietti per Italia-Bielorussia femminile, gara di ritorno del primo turno dei playoff per il Mondiale. Si giocherà martedì 13 ottobre allo stadio Artemio Franchi di Firenze, con inizio alle 18:15. La FIGC indica come canali di acquisto il portale ticketing.figc.it e i punti vendita autorizzati Vivaticket.",
        "Il settore Maratona costa 5 euro; il biglietto ridotto per chi ne ha diritto costa 1 euro. Sono previste riduzioni per Under 20, Over 65, studenti universitari iscritti all’anno accademico in corso e abbonati della Fiorentina. Il prezzo agevolato richiede la verifica dei requisiti indicati dalla federazione, e non si applica indistintamente a ogni acquisto.",
        "Per la Poltronissima il biglietto intero costa 14 euro e il ridotto 10 euro. La Tribuna d’Onore con accesso all’esperienza Casa Azzurre costa 30 euro. Per gli universitari l’acquisto del ridotto è previsto nei punti vendita abilitati, presentando la documentazione richiesta dalla FIGC.",
        "La partita di Firenze segue l’andata in programma il 9 ottobre a Tbilisi, in Georgia. Il doppio confronto è il primo turno dei playoff mondiali. Chi intende assistere al ritorno può controllare disponibilità dei posti e condizioni delle riduzioni sul circuito ufficiale prima di acquistare."
    ],
    "fonti": [
        {"url": "https://www.figc.it/it/nazionali/news/nazionale-femminile-play-off-mondiali-in-vendita-i-biglietti-per-la-gara-di-firenze-con-la-bielorussia-amua4jcs", "descrizione": "FIGC — annuncio di biglietteria, prezzi e riduzioni, 22 settembre 2026, ore 10:25."},
        {"url": "https://ticketing.figc.it/", "descrizione": "FIGC — circuito ufficiale per l’acquisto dei biglietti."}
    ],
    "dati_chiave": [
        {"valore": "13 ottobre", "etichetta": "gara a Firenze", "icona": "◆"},
        {"valore": "18:15", "etichetta": "calcio d’inizio", "icona": "◆"},
        {"valore": "5 €", "etichetta": "Maratona intero", "icona": "◆"}
    ],
    "parole_chiave_titolo": ["Italia-Bielorussia"],
}

def main():
    assert not (ROOT / "notizie" / f"{SLUG}.html").exists()
    assert site.write_article(ARTICLE, IMAGE, VERSION) == SLUG
    registry = ROOT / "assets/data/editorial-images-v210.json"
    data = json.loads(registry.read_text())
    data["items"].insert(0, {**IMAGE, "article": URL})
    registry.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    cfg = ROOT / "assets/data/homepage-config-v504.json"
    config = json.loads(cfg.read_text())
    doc = html.parse(str(ROOT / "notizie" / f"{SLUG}.html"))
    published = json.loads(doc.xpath('//script[@type="application/ld+json"]')[0].text)["datePublished"]
    config["articles"][URL] = {"firstPublishedAt": published, "homepagePriority": 78, "primaryCategory": "sport"}
    cfg.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n")
    site.sync_surfaces([ARTICLE], URL, VERSION)
    manifest = ROOT / "curiomondo-site-manifest.json"
    state = json.loads(manifest.read_text())
    state["last_release"]["news_added"].append(SLUG)
    state["last_release"]["change"] = "Sei notizie verificate e due aggiornamenti, inclusa la biglietteria FIGC"
    manifest.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text())
        if "articleCount" in state: state["articleCount"] += 1
        if "generatedEditorialImages" in state: state["generatedEditorialImages"] += 1
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n")
    print(URL)

if __name__ == "__main__": main()
