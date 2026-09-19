#!/usr/bin/env python3
"""Pubblica due schede di servizio verificate: casa 2027 e trasporti Puglia."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 446


def variants(source: Path, key: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 3 / 2
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    out = ROOT / "assets/images/editorial-auto"
    out.mkdir(parents=True, exist_ok=True)
    result = []
    for width in (480, 800, 1200):
        path = out / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=86, method=6)
        result.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return result


ARTICLES = [
    {
        "slug": "bonus-ristrutturazioni-2027-aliquote-36-30-cosa-cambia-19-settembre-2026",
        "titolo": "Bonus ristrutturazioni 2027: aliquote al 36% e 30% senza proroga",
        "sommario": "La normativa vigente riduce dal 2027 la detrazione per l’abitazione principale e per gli altri immobili. La legge di Bilancio può ancora modificare lo scenario.",
        "categoria": "Economia", "luogo": "Italia", "formato": "standard", "stato": "UFFICIALE",
        "parole_chiave_titolo": ["Bonus ristrutturazioni", "2027"],
        "dati_chiave": [
            {"icona": "◆", "valore": "36%", "etichetta": "aliquota 2027 per l’abitazione principale"},
            {"icona": "●", "valore": "30%", "etichetta": "aliquota 2027 negli altri casi"},
            {"icona": "▦", "valore": "10 anni", "etichetta": "ripartizione ordinaria della detrazione"},
        ],
        "paragrafi": [
            "Dal 1° gennaio 2027 il bonus ristrutturazioni scenderà, a legislazione invariata, al 36 per cento per l’abitazione principale e al 30 per cento negli altri casi. Il passaggio interessa le spese sostenute nel 2027. Una proroga nella prossima legge di Bilancio potrebbe cambiare le aliquote, ma oggi non è ancora approvata.",
            "La misura più favorevole riguarda i proprietari o i titolari di un diritto reale che destinano l’immobile ad abitazione principale. La casa deve essere il luogo di residenza e dimora abituale del contribuente. La condizione può essere soddisfatta anche al termine dei lavori, nei casi ammessi dalle regole fiscali.",
            "Per seconde case, immobili locati e spese sostenute da inquilini o comodatari, l’aliquota prevista per il 2027 è invece del 30 per cento. La differenza non dipende dal tipo di pagamento, ma dalla posizione del beneficiario e dall’uso dell’immobile. La detrazione resta ripartita in dieci quote annuali di pari importo.",
            "Il tetto di spesa del bonus ristrutturazioni resta un elemento distinto dall’aliquota. Prima di firmare un contratto occorre verificare l’anno del pagamento, la tipologia di intervento e il soggetto che sosterrà la spesa. Anticipare una fattura senza che il lavoro e la documentazione siano coerenti può creare problemi in caso di controllo.",
            "Il pagamento deve essere tracciabile secondo le modalità previste per l’agevolazione. Il bonifico dedicato riporta causale normativa, codice fiscale di chi detrae e partita IVA o codice fiscale del destinatario. Vanno conservati fatture, ricevute, eventuali titoli edilizi e la documentazione richiesta per lo specifico intervento.",
            "Il bonus mobili non va confuso con la detrazione per i lavori. La sua eventuale disponibilità nel 2027 richiede una proroga specifica e non discende automaticamente dal bonus ristrutturazioni. Chi programma acquisti di arredi o grandi elettrodomestici non dovrebbe quindi considerarne certa la detrazione per il prossimo anno.",
            "La differenza pratica è rilevante: su 40.000 euro di spesa ammessa, il 36 per cento equivale a 14.400 euro complessivi, mentre il 30 per cento vale 12.000 euro. Sono importi teorici da distribuire in dieci anni e utilizzabili nei limiti dell’IRPEF dovuta dal contribuente.",
            "Il quadro definitivo arriverà con la legge di Bilancio 2027 e con gli eventuali chiarimenti dell’Agenzia delle Entrate. Fino all’approvazione, le aliquote del 36 e del 30 per cento sono la base normativa vigente, non una previsione certa dell’esito politico della manovra.",
        ],
        "fonti": [
            {"url": "https://www.agenziaentrate.gov.it/portale/schede/agevolazioni/detrristredil36/schinfodetrristredil36", "descrizione": "Agenzia delle Entrate — scheda ufficiale sulle detrazioni per ristrutturazioni edilizie."},
            {"url": "https://www.normattiva.it/uri-res/N2Ls?urn:nir:stato:legge:2024-12-30;207", "descrizione": "Normattiva — legge 30 dicembre 2024, n. 207, disciplina delle aliquote pluriennali."},
            {"url": "https://www.corriere.it/economia/casa/26_settembre_19/bonus-ristrutturazioni-sulla-prima-casa-al-36-bonus-mobili-a-rischio-cosa-cambia-dal-2027-2c6baa66-3c24-4bb0-847d-255cbcaf9xlk.shtml", "descrizione": "Corriere della Sera, 19 settembre — confronto tra aliquote vigenti e possibili decisioni della manovra 2027."},
        ],
        "correlati": [
            {"url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html", "titolo": "Bollo auto, il testo ufficiale dell’esenzione 2027"},
            {"url": "/notizie/tari-dichiarazione-90-giorni-decreto-147-imu-sanzioni-18-settembre-2026.html", "titolo": "TARI, dichiarazione entro 90 giorni: le nuove regole"},
            {"url": "/notizie/italia-banche-contributo-manovra-2027-proposta-lega-8-settembre-2026.html", "titolo": "Manovra 2027, il confronto sul contributo delle banche"},
        ],
        "stamp": "2026-09-19T22:18:00+02:00", "source": "bonus-ristrutturazioni-v446.png",
        "alt": "Scena editoriale contestuale generata con IA: professionisti valutano progetti in un appartamento italiano in ristrutturazione; non è una fotografia documentaria.",
        "prompt": "Photorealistic Italian apartment renovation with craftsperson, plans and realistic tools, natural daylight, no text or watermark.",
    },
    {
        "slug": "bonus-trasporti-puglia-studenti-2026-2027-domanda-requisiti",
        "titolo": "Bonus trasporti Puglia 2026/27: sconto del 50% per studenti pendolari",
        "sommario": "Domande online fino al 25 ottobre per abbonamenti mensili da ottobre a maggio. ISEE massimo di 13.000 euro, più alto per le famiglie numerose.",
        "categoria": "Italia", "luogo": "Puglia", "formato": "standard", "stato": "UFFICIALE",
        "parole_chiave_titolo": ["Bonus trasporti", "50%"],
        "dati_chiave": [
            {"icona": "◆", "valore": "50%", "etichetta": "sconto sull’abbonamento mensile"},
            {"icona": "●", "valore": "13.000 €", "etichetta": "soglia ISEE ordinaria"},
            {"icona": "▦", "valore": "25 ottobre", "etichetta": "chiusura della domanda online"},
        ],
        "paragrafi": [
            "La Regione Puglia ha aperto il bonus trasporti 2026/27 per gli studenti pendolari residenti nel territorio regionale. L’agevolazione riduce del 50 per cento il prezzo degli abbonamenti mensili interurbani. La domanda si presenta online entro le 12 del 25 ottobre 2026 sul portale Studio in Puglia.",
            "Possono partecipare gli iscritti alle scuole secondarie di secondo grado, agli ITS Academy, alle università e alle istituzioni AFAM con sede in Puglia. È richiesta la residenza regionale e un’attestazione ISEE o ISEEU valida. Per i minorenni presenta l’istanza chi esercita la responsabilità genitoriale o la tutela.",
            "La soglia economica ordinaria è di 13.000 euro. Sale a 15.748,78 euro per i nuclei con almeno tre figli. Il sistema acquisisce l’attestazione dalla banca dati INPS, quindi il documento deve risultare disponibile prima dell’invio della richiesta.",
            "Lo sconto copre gli abbonamenti mensili da ottobre 2026 a maggio 2027, per otto mesi. Il valore totale riconosciuto a ciascun beneficiario deve restare sotto 1.000 euro ed è soggetto alle risorse disponibili. L’agevolazione è personale e non può essere ceduta.",
            "Chi invia la domanda entro le 12 del 25 settembre può ottenere lo sconto a partire da ottobre. Le istanze trasmesse dopo quel termine, ma entro il 25 ottobre, producono effetti da novembre. La Regione precisa che non è un click day: l’ordine di invio non attribuisce priorità.",
            "Per accedere servono SPID, Carta d’identità elettronica oppure CNS. Durante la compilazione si indicano studente, istituto frequentato e azienda di trasporto scelta. Dopo la trasmissione il richiedente riceve una ricevuta con il codice pratica, da conservare per seguire l’esito.",
            "In caso di ammissione, il codice bonus arriva via e-mail ed è utilizzabile online o nelle biglietterie dell’operatore selezionato. Sono compresi i servizi interurbani regionali, provinciali e della Città metropolitana. Le modalità d’acquisto cambiano in base al gestore e vanno controllate nella sezione dedicata.",
            "Un ISEE con omissioni o difformità può essere accolto solo provvisoriamente. La regolarizzazione deve avvenire entro dieci giorni dalla chiusura della piattaforma. Una domanda compilata ma non trasmessa entro la scadenza non produce alcun diritto al beneficio.",
        ],
        "fonti": [
            {"url": "https://www.studioinpuglia.regione.puglia.it/studenti-pendolari", "descrizione": "Regione Puglia, portale Studio in Puglia — requisiti, scadenze, procedura e modalità di utilizzo."},
            {"url": "https://www.studioinpuglia.regione.puglia.it/studenti-pendolari#avviso", "descrizione": "Allegato A alla determinazione dirigenziale n. 195 dell’11 settembre 2026 — avviso pubblico ufficiale."},
            {"url": "https://www.regione.puglia.it/", "descrizione": "Regione Puglia — amministrazione titolare dell’agevolazione approvata con D.G.R. n. 1211 del 10 settembre 2026."},
        ],
        "correlati": [
            {"url": "/notizie/tari-dichiarazione-90-giorni-decreto-147-imu-sanzioni-18-settembre-2026.html", "titolo": "TARI, dichiarazione entro 90 giorni: le nuove regole"},
            {"url": "/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html", "titolo": "Bollo auto, il testo ufficiale dell’esenzione 2027"},
            {"url": "/notizie/aumento-ticket-sanitari-21-settembre-2026-tariffario-visite.html", "titolo": "Ticket sanitari, dal 21 settembre il nuovo tariffario"},
        ],
        "stamp": "2026-09-19T22:16:00+02:00", "source": "bonus-trasporti-puglia-v446.png",
        "alt": "Scena editoriale contestuale generata con IA: studenti pendolari salgono su un autobus urbano in Puglia; non è una fotografia documentaria.",
        "prompt": "Photorealistic student commuters boarding a regional bus in southern Italy, morning light, no readable text or watermark.",
    },
]


def stamp(slug: str, iso: str) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    page = path.read_text(encoding="utf-8")
    page = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{iso}"', page)
    page = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{iso}"', page)
    path.write_text(page, encoding="utf-8")


def main() -> None:
    sources = {
        "bonus-ristrutturazioni-v446.png": ROOT.parent / "generated_images/exec-bc0b13df-9ea8-425d-ad55-f6ed5b9c8fe0.png",
        "bonus-trasporti-puglia-v446.png": ROOT.parent / "generated_images/exec-76dfe113-1178-4651-aa51-444c4c583b9b.png",
    }
    generated = ROOT / "generated_images"
    generated.mkdir(exist_ok=True)
    published = []
    for article in ARTICLES:
        words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in article["paragrafi"])
        if not 300 <= words <= 600 or any(len(p.split()) > 60 for p in article["paragrafi"]):
            raise SystemExit(f"gate corpo fallito: {article['slug']} ({words} parole)")
        src = sources[article["source"]]
        if not src.exists():
            raise SystemExit(f"immagine assente: {src}")
        local = generated / article["source"]
        shutil.copy2(src, local)
        key = f"{article['slug']}-v{VERSION}"
        image = {"key": key, "aiGenerated": True, "documentaryPhoto": False, "generator": "ChatGPT/OpenAI image generation", "variants": variants(local, key), "alt": article["alt"], "disclosure": CAPTION, "sensitiveContext": False, "reenactedEvent": False, "syntheticLikeness": None, "prompt": article["prompt"]}
        slug = write_article(article, image, VERSION)
        stamp(slug, article["stamp"])
        article["published"] = article["stamp"]
        register_image(image, slug, VERSION)
        published.append(slug)
        payload = {"slug": slug, "title": article["titolo"], "excerpt": article["sommario"], "category": article["categoria"], "published_at": article["stamp"], "updated_at": article["stamp"], "development_at": "2026-09-19", "status": article["stato"], "public_url": f"https://curiomondo.it/notizie/{slug}.html", "publication_state": "pending_deploy", "body": article["paragrafi"], "sources": article["fonti"], "image": image}
        out = ROOT / "contenuti/notizie" / f"{slug}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(slug, words, "parole")
    sync_surfaces(ARTICLES, "", VERSION)
    mp = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(mp.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {"version": VERSION, "date": "2026-09-19", "type": "content-release", "news_added": published, "news_updated": [], "change": "Bonus ristrutturazioni 2027 e bonus trasporti Puglia", "image_policy_applied": "new-openai-contextual-editorial-images"}
    mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        if path.exists():
            state = json.loads(path.read_text(encoding="utf-8"))
            state.update({"currentVersion": VERSION, "site_version": VERSION, "version": str(VERSION), "date": "2026-09-19", "release_date": "2026-09-19", "articleCount": int(state.get("articleCount", 0)) + 2, "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 2, "last_update": "news-v446"})
            path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    log = ROOT / "automation/logs/editoriale-20260919T221800-Europe-Rome.json"
    log.write_text(json.dumps({"run_at": "2026-09-19T22:18:00+02:00", "processed": [{"title": a["titolo"], "decision": "publish", "public_url": f"https://curiomondo.it/notizie/{a['slug']}.html"} for a in ARTICLES], "rejected_keywords": {"freddo": "nessuno sviluppo odierno verificato", "Sigfrido Ranucci": "nessuno sviluppo sostanziale rispetto all’articolo esistente", "Roberta Bruzzone": "nessuna notizia di rilevanza sufficiente"}}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
