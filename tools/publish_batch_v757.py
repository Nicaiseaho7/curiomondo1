#!/usr/bin/env python3
"""Batch v757: F1 Bahrain/Antonelli, Schlein PD direzione, Maschi Veri 2 Netflix."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

VERSION = 757

IMAGES_SRC = {
    "f1-gp-bahrain-sepang-verstappen-pole-antonelli-terzo-4-ottobre-2026": ROOT / "generated_images/f1-antonelli-v757.jpg",
    "schlein-direzione-pd-avete-fallito-andate-a-casa-meloni-conte-2-ottobre-2026": ROOT / "generated_images/schlein-v757.jpg",
    "maschi-veri-2-netflix-7-ottobre-2026-cast-trama": ROOT / "generated_images/maschi-veri-v757.jpg",
}

ARTICLES = [
  {
    "slug": "f1-gp-bahrain-sepang-verstappen-pole-antonelli-terzo-4-ottobre-2026",
    "titolo": "F1 a Sepang: Verstappen in pole, Antonelli parte terzo da leader del Mondiale",
    "sommario": "Hamilton in prima fila con la Ferrari. La gara del Bahrain Grand Prix in Malesia è in programma domenica 4 ottobre alle 9 italiane.",
    "categoria": "Sport",
    "luogo": "Sepang, Malesia",
    "formato": "standard",
    "parole_chiave_titolo": ["Verstappen pole", "Antonelli terzo"],
    "dati_chiave": [
      {"valore": "1:35.130", "etichetta": "tempo pole Verstappen"},
      {"valore": "P3", "etichetta": "partenza di Antonelli"},
      {"valore": "09:00", "etichetta": "ora gara Italia"},
    ],
    "paragrafi": [
      "Max Verstappen ha conquistato la pole position del Bahrain Grand Prix 2026, disputato a Sepang in Malesia, con il tempo di 1:35.130. Lewis Hamilton ha chiuso secondo con la Ferrari a 0,298 secondi; dietro di loro Isack Hadjar, poi Kimi Antonelli con la Mercedes.",
      "Hadjar ha ricevuto una penalità di cinque posizioni per il settimo motore termico, quindi Antonelli — leader del Mondiale — partirà terzo e Charles Leclerc quarto. George Russell, compagno di Antonelli, è rimasto ottavo in qualifica.",
      "La gara di oggi, domenica 4 ottobre, è in programma alle 9:00 italiane sul circuito di Sepang, utilizzato in sostituzione degli appuntamenti del Medio Oriente annullati. È la prima volta che la Formula 1 torna a Sepang dal 2017.",
      "Antonelli ha definito la gara «stretta» e ha detto di puntare al miglior risultato possibile, anche una vittoria se le condizioni lo permetteranno. Il degrado gomme e la gestione delle temperature saranno, secondo il pilota italiano, i fattori decisivi.",
      "Verstappen ha ottenuto la prima pole della stagione e la quarantanovesima in carriera. Hamilton ha riportato la Ferrari in prima fila, mentre McLaren ha messo Norris e Piastri in quinta e sesta posizione di griglia.",
      "Il duello in classifica vede Antonelli davanti, con Russell tra i rivali più vicini. La partenza dalla seconda fila offre all’italiano la possibilità di attaccare Verstappen e Hamilton già nelle prime curve di Sepang.",
    ],
    "fonti": [
      {"url": "https://www.formula1.com/en/results/2026/races/1308/bahrain/qualifying", "descrizione": "Formula1.com — classifica ufficiale qualifiche Bahrain GP 2026 a Sepang"},
      {"url": "https://www.fia.com/system/files/decision-document/2026_bahrain_grand_prix_in_malaysia_-_final_qualifying_classification.pdf", "descrizione": "FIA — documento stewards final qualifying classification"},
      {"url": "https://www.grandprix.com/races/bahrain-gp-2026-qualifying-report.html", "descrizione": "Grandprix.com — report qualifiche e penalità motore Hadjar"},
    ],
  },
  {
    "slug": "schlein-direzione-pd-avete-fallito-andate-a-casa-meloni-conte-2-ottobre-2026",
    "titolo": "Schlein a Meloni: «Avete fallito, andate a casa». A Conte: «Uno non vale uno»",
    "sommario": "Alla direzione Pd la segretaria attacca il governo e rivendica il ruolo di primo partito nel campo progressista. Meloni replica sui social: «Dieci falsità».",
    "categoria": "Politica",
    "luogo": "Roma",
    "formato": "standard",
    "parole_chiave_titolo": ["Schlein", "andate a casa"],
    "dati_chiave": [
      {"valore": "2 ott", "etichetta": "direzione Pd"},
      {"valore": "10", "etichetta": "criticità elencate a Meloni"},
      {"valore": "unanimità", "etichetta": "relazione approvata (minoranza astenuta)"},
    ],
    "paragrafi": [
      "Elly Schlein, alla direzione nazionale del Pd del 2 ottobre 2026, ha attaccato frontalmente il governo Meloni: «Prendete atto che avete fallito e andate a casa. Prima si vota e meglio è per l’Italia». La relazione della segretaria è stata approvata all’unanimità, con l’astensione della minoranza riformista che non ha partecipato al voto.",
      "Schlein ha rivolto un messaggio anche a Giuseppe Conte e al Movimento 5 Stelle: l’alleanza progressista sarà inclusiva, ma «non è che uno vale uno». Ha rivendicato che il Pd è il primo partito della coalizione e ha i numeri più alti del campo.",
      "Alla premier, che le aveva chiesto di indicare «una cosa vera», la segretaria ha risposto elencando dieci criticità su inflazione, salari, pressione fiscale, industria ed energia. Ha anche contestato la fiducia sulla legge elettorale e il ruolo di chi, in Aula, monitorava i voti dei franchi tiratori.",
      "Giorgia Meloni ha replicato sui social: «Elly Schlein risponde oggi a una domanda che le ho fatto quasi due settimane fa. Con questi ritmi ce la vedo bene a risolvere i problemi degli italiani», aggiungendo che le dieci contestazioni sono «falsità».",
      "Conte ha ribadito che nel campo progressista le primarie restano lo strumento per scegliere la leadership e che non spetta a Meloni decidere chi guida l’opposizione. Il botta e risposta accelera il confronto sul programma comune e sulle regole di alleanza in vista di un possibile voto anticipato.",
      "Sul piano istituzionale resta aperto il passaggio finale della legge elettorale alla Camera, previsto nella prima settimana di ottobre. Schlein ha collegato l’urgenza del voto alla valutazione politica sul bilancio di quattro anni di governo, senza anticipare date che non dipendono dal solo Pd.",
    ],
    "fonti": [
      {"url": "https://www.adnkronos.com/politica/direzione-pd-discorso-schlein-oggi_61JP6MgdrXhfGq8gEziteO", "descrizione": "Adnkronos — discorso Schlein in direzione Pd e citazioni complete"},
      {"url": "https://www.italpress.com/schlein-a-meloni-avete-fallito-andate-a-casa-prima-si-vota-meglio-e-per-italia/", "descrizione": "Italpress — «andate a casa» e replica di Meloni sui social"},
      {"url": "https://roma.corriere.it/notizie/cronaca/26_ottobre_02/direzione-pd-la-relazione-della-segretaria-elly-schlein-il-governo-ha-fallito-con-tempo-e-numeri-a-disposizione-non-ha-fatto-30079cc5-aed5-4cfb-b10c-1dad239c6xlk.shtml", "descrizione": "Corriere di Roma — direzione Pd, «uno non vale uno» e risposta Meloni"},
    ],
  },
  {
    "slug": "maschi-veri-2-netflix-7-ottobre-2026-cast-trama",
    "titolo": "Maschi Veri 2 su Netflix dal 7 ottobre: coppie ribaltate e cinque new entry",
    "sommario": "Tornano Lastrico, Martari, Montanari e Sermonti. Tra le novità del cast Carolina Crescentini, Silvia D’Amico, Alessio Boni, Giancarlo Commare e Ilenia Pastorelli.",
    "categoria": "Spettacolo",
    "luogo": "Italia",
    "formato": "standard",
    "parole_chiave_titolo": ["Maschi Veri 2", "7 ottobre"],
    "dati_chiave": [
      {"valore": "7 ott", "etichetta": "uscita Netflix"},
      {"valore": "4", "etichetta": "protagonisti confermati"},
      {"valore": "5", "etichetta": "new entry nel cast"},
    ],
    "paragrafi": [
      "Maschi Veri 2 arriva su Netflix mercoledì 7 ottobre 2026 con tutti gli episodi della seconda stagione. La comedy italiana prodotta da Groenlandia riparte dal punto in cui si era chiusa la prima stagione: le quattro coppie si ritrovano in una situazione capovolta e non possono più nascondersi dietro la scusa di non aver capito i cambiamenti nei rapporti tra uomini e donne.",
      "Tornano Maurizio Lastrico, Matteo Martari, Francesco Montanari e Pietro Sermonti nei ruoli di Massimo, Luigi, Mattia e Riccardo. Il trailer anticipa nuovi lavori e vecchie fiamme come elementi che complicano ulteriormente le relazioni già in bilico.",
      "Nel cast entrano cinque new entry: Carolina Crescentini (Simona), Silvia D’Amico (Paola), Alessio Boni (Giordano), Giancarlo Commare (Augusto) e Ilenia Pastorelli (Tecla). Netflix non ha ancora svelato in dettaglio come ciascuno si intrecci con i quattro protagonisti.",
      "La serie è il remake italiano di Machos Alfa, comedy spagnola che ha superato le quattro stagioni. La prima stagione italiana era online dal 21 maggio 2025 ed è ancora disponibile in catalogo per chi vuole recuperarla prima del 7 ottobre.",
      "L’uscita coincide con un ottobre ricco di novità streaming, ma resta un appuntamento specifico per il pubblico della comedy di relazione made in Italy. Per vederla serve un abbonamento Netflix attivo; non sono previsti costi aggiuntivi rispetto al piano scelto.",
      "Il tono resta quello della prima stagione: commedia di equivoci, con spazi di romanticismo e di riflessione sui ruoli di genere. La data del 7 ottobre è stata comunicata dalla piattaforma insieme al trailer ufficiale a fine estate 2026.",
    ],
    "fonti": [
      {"url": "https://www.ilmattino.it/spettacoli/televisione/maschi_veri_2_netflix_trama_coppie_novita_cast-9801682.html", "descrizione": "Il Mattino — trama, cast e new entry di Maschi Veri 2"},
      {"url": "https://jumptheshark.it/netflix/maschi-veri-2-dal-7-ottobre-su-netflix-cast-e-trama/", "descrizione": "Jump the Shark — data di uscita Netflix e trailer"},
      {"url": "https://www.napolike.it/televisione/2026/09/maschi-veri-2-netflix-7-ottobre-344841", "descrizione": "NapoliLike — conferma 7 ottobre e recupero prima stagione"},
    ],
  },
]

ALTS = {
  ARTICLES[0]["slug"]: "Illustrazione editoriale IA di Kimi Antonelli in tuta Mercedes AMG Petronas al circuito di Sepang; scena non documentaria.",
  ARTICLES[1]["slug"]: "Illustrazione editoriale IA di Elly Schlein durante un intervento politico; scena non documentaria.",
  ARTICLES[2]["slug"]: "Illustrazione editoriale IA del cast di Maschi Veri in un salotto moderno; scena non documentaria.",
}


def make_image(slug: str) -> dict:
    im = Image.open(IMAGES_SRC[slug]).convert("RGB")
    w, h = im.size
    target = 1.5
    if w / h > target:
        nw = round(h * target)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = round(w / target)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    out = []
    for width in (480, 800, 1200):
        p = ROOT / "assets/images/editorial-auto" / f"{slug}-v{VERSION}-{width}.webp"
        im.resize((width, round(width / target)), Image.Resampling.LANCZOS).save(
            p, "WEBP", quality=87, method=6
        )
        out.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{p.name}",
            "sha256": hashlib.sha256(p.read_bytes()).hexdigest(),
            "bytes": p.stat().st_size,
        })
    return {
        "key": f"{slug}-v{VERSION}",
        "alt": ALTS[slug],
        "variants": out,
        "disclosure": site.CAPTION,
        "generator": "Grok Imagine",
        "aiGenerated": True,
        "syntheticLikeness": "public-figure",
        "sensitiveContext": False,
    }


def main() -> None:
    written = []
    for art in ARTICLES:
        img = make_image(art["slug"])
        slug = site.write_article(art, img, VERSION)
        site.register_image(img, slug, VERSION)
        written.append(art)
        print("OK", slug)

    featured = f"/notizie/{written[0]['slug']}.html"
    site.sync_surfaces(written, featured, VERSION)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state["site_version"] = VERSION
    state["currentVersion"] = VERSION
    state["version"] = str(VERSION)
    state["articleCount"] = int(state.get("articleCount", 0)) + len(written)
    state["generatedEditorialImages"] = int(state.get("generatedEditorialImages", 0)) + len(written)
    state["last_update"] = f"notizie-batch-v{VERSION}"
    state["date"] = "2026-10-04"
    state["release_date"] = "2026-10-04"
    state["status"] = "ready"
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # Force chronological dateISO for new articles matching feed order
    # (predeploy requires featured/rail/cards chronological)
    import time
    from datetime import datetime, timedelta
    from zoneinfo import ZoneInfo
    ROME = ZoneInfo("Europe/Rome")
    base = datetime.now(ROME).replace(microsecond=0)
    # stagger: newest first article 0
    feed_path = ROOT / "assets/data/home-feed-v210.json"
    feed = json.loads(feed_path.read_text(encoding="utf-8"))
    for i, art in enumerate(written):
        dt = (base - timedelta(minutes=i)).isoformat()
        url = f"/notizie/{art['slug']}.html"
        for item in feed["items"]:
            if item.get("url") == url:
                item["dateISO"] = dt
                item["dateLabel"] = dt[:10]
                item["excerpt"] = art["sommario"]
                item["featuredStats"] = [
                    {"icon": "•", "value": d["valore"], "label": d["etichetta"]}
                    for d in art["dati_chiave"][:3]
                ]
                item["featuredHighlights"] = art["parole_chiave_titolo"][:2]
        # align article time tags
        path = ROOT / "notizie" / f"{art['slug']}.html"
        html = path.read_text(encoding="utf-8")
        # replace datePublished/dateModified in JSON-LD if present
        import re
        html2 = re.sub(
            r'"datePublished":"[^"]+"',
            f'"datePublished":"{dt}"',
            html,
            count=1,
        )
        html2 = re.sub(
            r'"dateModified":"[^"]+"',
            f'"dateModified":"{dt}"',
            html2,
            count=1,
        )
        path.write_text(html2, encoding="utf-8")
        print("date sync", art["slug"], dt)

    feed_path.write_text(json.dumps(feed, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    # re-render home from feed
    import subprocess
    r = subprocess.run(
        ["node", "tools/render_home_editorial.js"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    print("render_home", r.returncode, r.stdout[-500:] if r.stdout else r.stderr[-500:])

    print("DONE v", VERSION, "articles", len(written))


if __name__ == "__main__":
    main()
