#!/usr/bin/env python3
"""Pubblica le notizie verificate su Premier League e cinema del 19 settembre."""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))

from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article
from build_v446 import stamp, variants

VERSION = 447

ARTICLES = [
    {
        "slug": "tottenham-aston-villa-2-3-prima-vittoria-emery-19-settembre-2026",
        "titolo": "Tottenham-Aston Villa 2-3: prima vittoria per Emery",
        "sommario": "Manzambi, Jackson e Buendía firmano il primo successo dei Villans in Premier League. La rimonta finale degli Spurs si ferma a un gol dal pareggio.",
        "categoria": "Sport internazionale", "luogo": "Londra", "formato": "standard", "stato": "UFFICIALE",
        "parole_chiave_titolo": ["Tottenham-Aston Villa", "2-3"],
        "dati_chiave": [
            {"icona": "◆", "valore": "2-3", "etichetta": "risultato finale a Londra"},
            {"icona": "●", "valore": "3", "etichetta": "marcatori diversi per il Villa"},
            {"icona": "▦", "valore": "1ª", "etichetta": "vittoria stagionale in Premier"},
        ],
        "paragrafi": [
            "L’Aston Villa ha battuto il Tottenham 3-2 a Londra sabato 19 settembre, conquistando la prima vittoria della stagione in Premier League. Johan Manzambi, Nicolas Jackson ed Emiliano Buendía hanno portato gli ospiti sul 3-0; Conor Gallagher e Jan Paul van Hecke hanno riaperto la partita nel finale senza completare la rimonta.",
            "La squadra di Unai Emery ha sbloccato il risultato nel recupero del primo tempo con Manzambi. Il centrocampista ha concluso un’azione che ha premiato l’organizzazione degli ospiti dopo una frazione equilibrata. Per il Tottenham è stato il primo colpo di una serata già delicata per classifica e fiducia.",
            "Jackson ha raddoppiato al 67° minuto, trasformando la superiorità del Villa in un vantaggio più solido. Dodici minuti dopo Buendía ha segnato il terzo gol. Sullo 0-3, la partita sembrava chiusa e i Villans avevano il controllo sia degli spazi sia del ritmo.",
            "Gli Spurs hanno però reagito negli ultimi minuti. Gallagher ha accorciato le distanze e Van Hecke ha segnato di testa il 2-3, aumentando la pressione fino al recupero. Un precedente gol di Mohammed Kudus era stato annullato, episodio che ha contribuito alla sensazione di una gara rimasta aperta fino alla fine.",
            "Il dato più importante per Emery è il risultato: dopo quattro giornate senza successi, il Villa sale a quattro punti e interrompe l’avvio negativo. I tre marcatori differenti indicano anche una distribuzione offensiva più ampia, utile in una fase della stagione nella quale la squadra stava producendo meno di quanto atteso.",
            "Per il Tottenham il problema è opposto. La squadra resta con due punti in cinque partite e ancora senza vittorie, nella zona bassa della classifica. I due gol finali mostrano capacità di reazione, ma non cancellano le difficoltà difensive e il ritardo con cui gli Spurs hanno cambiato l’inerzia dell’incontro.",
            "La lettura della gara va quindi oltre il 3-2. Il Villa ha costruito il successo prima e dopo l’intervallo, poi ha rischiato di disperderlo quando ha abbassato il baricentro. Il Tottenham ha trovato energia tardi: un segnale utile, ma insufficiente per evitare un’altra sconfitta casalinga.",
        ],
        "fonti": [
            {"url": "https://www.reuters.com/sports/soccer/wrapup-soccer-manzambi-jackson-buendia-fire-villa-first-win-spurs-misery-deepens-2026-09-19/", "descrizione": "Reuters, 19 settembre — cronaca, marcatori e contesto di classifica."},
            {"url": "https://www.theguardian.com/football/live/2026/sep/19/tottenham-v-aston-villa-premier-league-live", "descrizione": "The Guardian, 19 settembre — diretta e sviluppo della partita."},
            {"url": "https://www.espn.co.uk/football/story/_/id/49978180/tottenham-aston-villa-live-premier-league-latest-updates-commentary-score-result", "descrizione": "ESPN, 19 settembre — risultato e resoconto dell’incontro."},
        ],
        "correlati": [
            {"url": "/notizie/eurovolley-italia-polonia-3-1-finale-turchia-5-settembre-2026.html", "titolo": "Eurovolley, Italia in finale dopo il 3-1 alla Polonia"},
            {"url": "/notizie/italia-turchia-finale-europei-volley-femminile-3-2-6-settembre-2026.html", "titolo": "Italia-Turchia, finale degli Europei di volley"},
            {"url": "/notizie/formula-1-calendario-2027-dieci-sprint-monaco-monza.html", "titolo": "Formula 1, il calendario Sprint 2027"},
        ],
        "stamp": "2026-09-19T22:42:00+02:00", "source": "tottenham-aston-villa-v447.png",
        "source_path": "/workspace/scratch/d825bbf302f0/generated_images/exec-058d20cf-94ba-4b62-b0e9-59466cb02c9a.png",
        "alt": "Illustrazione editoriale generata con IA: Unai Emery a bordo campo dopo Tottenham-Aston Villa; non è una fotografia documentaria.",
        "prompt": "Photorealistic editorial depiction of Unai Emery on a London stadium touchline after an Aston Villa match, no logos, text or watermark.",
    },
    {
        "slug": "resident-evil-film-2026-cinema-zach-cregger-austin-abrams-19-settembre",
        "titolo": "Resident Evil al cinema: il nuovo film di Zach Cregger",
        "sommario": "Il regista di Barbarian e Weapons porta nelle sale una storia originale ambientata nell’universo Capcom, con Austin Abrams nei panni di un corriere travolto dall’epidemia.",
        "categoria": "Film e serie TV", "luogo": "Italia", "formato": "standard", "stato": "UFFICIALE",
        "parole_chiave_titolo": ["Resident Evil", "Zach Cregger"],
        "dati_chiave": [
            {"icona": "◆", "valore": "17 settembre", "etichetta": "uscita nelle sale italiane"},
            {"icona": "●", "valore": "Austin Abrams", "etichetta": "protagonista nel ruolo di Bryan"},
            {"icona": "▦", "valore": "Raccoon City", "etichetta": "scenario dell’epidemia"},
        ],
        "paragrafi": [
            "Resident Evil, il nuovo film scritto e diretto da Zach Cregger, è arrivato nelle sale italiane il 17 settembre ed è il principale debutto horror del fine settimana. Austin Abrams interpreta Bryan, un corriere che durante una consegna notturna finisce nel pieno dell’epidemia di Raccoon City.",
            "Il film non ripropone la trama di uno specifico videogioco e non mette al centro i personaggi storici Leon Kennedy, Claire Redfield o Jill Valentine. Cregger costruisce invece una vicenda originale nello stesso universo, scegliendo un protagonista comune e inesperto. La sua vulnerabilità sostituisce l’approccio da eroe d’azione delle precedenti saghe cinematografiche.",
            "La storia parte durante una tempesta di neve. Bryan accetta un’ultima consegna tra due ospedali e, dopo un incidente sulla strada, entra in contatto con l’inizio del disastro. Il percorso diventa una fuga tra creature, edifici isolati e ostacoli pensati con la logica progressiva di un videogioco survival horror.",
            "I riferimenti ai giochi non passano soltanto dall’ambientazione. Secondo Entertainment Weekly, la regia utilizza inquadrature in prima persona e sopra la spalla, munizioni limitate, chiavi, oggetti curativi e rompicapi ambientali. Sono elementi riconoscibili per i fan, integrati però in una narrazione autonoma e accessibile anche ai nuovi spettatori.",
            "Abrams porta nel film un protagonista impacciato, ironico e spesso spaventato. È una scelta che permette a Cregger di alternare tensione e comicità, come già accadeva in Barbarian e Weapons. Il contrasto tra panico quotidiano e minacce sovrannaturali distingue questa versione dai precedenti adattamenti live action.",
            "La distribuzione italiana lo presenta come un’uscita esclusivamente cinematografica: al 19 settembre non è stata annunciata una data ufficiale per lo streaming. Indicazioni non confermate su piattaforme o finestre digitali vanno quindi considerate previsioni, non informazioni definitive.",
            "Per chi conosce la serie, il punto d’interesse è il modo in cui il film recupera la sensazione di giocare senza copiare una campagna esistente. Per gli altri, la proposta è un horror d’azione autonomo, costruito attorno alla regia di Cregger e alla performance di Abrams più che alla continuità dei capitoli precedenti.",
        ],
        "fonti": [
            {"url": "https://www.youtube.com/watch?v=w_k72lFKSkc", "descrizione": "Trailer ufficiale italiano — uscita nelle sale dal 17 settembre e crediti principali."},
            {"url": "https://ew.com/resident-evil-easter-eggs-video-game-references-12126582", "descrizione": "Entertainment Weekly, 19 settembre — riferimenti ai videogiochi e scelte di regia."},
            {"url": "https://www.theguardian.com/film/2026/sep/16/resident-evil-reboot-movie-review", "descrizione": "The Guardian — trama, interpretazione di Austin Abrams e impostazione del film."},
            {"url": "https://www.youtube.com/watch?v=KGlapnJFacE", "descrizione": "Sony Pictures Entertainment — clip ufficiale e crediti del film."},
        ],
        "correlati": [
            {"url": "/notizie/cinema-uscite-italia-14-20-settembre-2026.html", "titolo": "Cinema, le uscite italiane della settimana"},
            {"url": "/notizie/batman-day-2026-italia-two-worlds-19-settembre-2026.html", "titolo": "Batman Day 2026, gli eventi in Italia"},
            {"url": "/notizie/villa-medici-film-festival-programma-19-settembre-2026.html", "titolo": "Villa Medici Film Festival, il programma"},
        ],
        "stamp": "2026-09-19T22:40:00+02:00", "source": "resident-evil-zach-cregger-v447.png",
        "source_path": "/workspace/scratch/d825bbf302f0/generated_images/exec-87b034b6-31ab-423d-b175-0af2e1f60e38.png",
        "alt": "Illustrazione editoriale generata con IA: Zach Cregger in una sala di proiezione cinematografica; non è una fotografia documentaria.",
        "prompt": "Photorealistic editorial portrait of Zach Cregger in a cinema projection room, moody non-graphic horror atmosphere, no text or watermark.",
    },
]


def main() -> None:
    generated = ROOT / "generated_images"
    generated.mkdir(exist_ok=True)
    published = []
    for article in ARTICLES:
        words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in article["paragrafi"])
        if not 300 <= words <= 600 or any(len(p.split()) > 60 for p in article["paragrafi"]):
            raise SystemExit(f"gate corpo fallito: {article['slug']} ({words} parole)")
        src = Path(article["source_path"])
        if not src.exists():
            raise SystemExit(f"immagine assente: {src}")
        local = generated / article["source"]
        shutil.copy2(src, local)
        key = f"{article['slug']}-v{VERSION}"
        image = {
            "key": key, "aiGenerated": True, "documentaryPhoto": False,
            "generator": "ChatGPT/OpenAI image generation", "variants": variants(local, key),
            "alt": article["alt"], "disclosure": CAPTION, "sensitiveContext": False,
            "reenactedEvent": False, "syntheticLikeness": "public-figure", "prompt": article["prompt"],
        }
        slug = write_article(article, image, VERSION)
        stamp(slug, article["stamp"])
        article["published"] = article["stamp"]
        register_image(image, slug, VERSION)
        published.append(slug)
        payload = {
            "slug": slug, "title": article["titolo"], "excerpt": article["sommario"],
            "category": article["categoria"], "published_at": article["stamp"],
            "updated_at": article["stamp"], "development_at": "2026-09-19",
            "status": article["stato"], "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy", "body": article["paragrafi"],
            "sources": article["fonti"], "image": image,
        }
        out = ROOT / "contenuti/notizie" / f"{slug}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(slug, words, "parole")

    sync_surfaces(ARTICLES, "", VERSION)
    mp = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION, "date": "2026-09-19", "type": "content-release",
        "news_added": published, "news_updated": [],
        "change": "Tottenham-Aston Villa e Resident Evil di Zach Cregger",
        "image_policy_applied": "new-openai-public-figure-editorial-images",
    }
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        if path.exists():
            state = json.loads(path.read_text(encoding="utf-8"))
            state.update({
                "currentVersion": VERSION, "site_version": VERSION, "version": str(VERSION),
                "date": "2026-09-19", "release_date": "2026-09-19",
                "articleCount": int(state.get("articleCount", 0)) + 2,
                "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 2,
                "last_update": "news-v447",
            })
            path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log = ROOT / "automation/logs/editoriale-20260919T224200-Europe-Rome.json"
    log.write_text(json.dumps({
        "run_at": "2026-09-19T22:42:00+02:00",
        "processed": [{"title": a["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{a['slug']}.html"} for a in ARTICLES],
        "scope": ["sport", "cinema", "film e serie TV", "personaggi famosi"],
        "rejected": ["Nessuna notizia seriale autonoma aggiunta: mancava uno sviluppo del giorno con conferme equivalenti."],
    }, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
