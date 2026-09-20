#!/usr/bin/env python3
"""Aggiornamento notizie del 20 settembre 2026."""
from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tools")]
from automation.newsroom.site import CAPTION, register_image, sync_surfaces, write_article

VERSION = 449
DATE = "2026-09-20"
STAMP = "2026-09-20T07:08:00+02:00"


def write_json(path: Path, data: object) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def variants(source: Path, key: str) -> list[dict[str, object]]:
    image = Image.open(source).convert("RGB")
    ratio = 1.5
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    folder = ROOT / "assets/images/editorial-auto"
    result = []
    for width in (480, 800, 1200):
        target = folder / f"{key}-{width}.webp"
        image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS).save(
            target, "WEBP", quality=86, method=6
        )
        result.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{target.name}",
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "bytes": target.stat().st_size,
        })
    return result


ARTICLES = [
    {
        "slug": "australia-albanese-tim-cook-sicurezza-social-minori-20-settembre-2026",
        "titolo": "Australia, Albanese incontra Tim Cook sulle tutele social per i minori",
        "sommario": "Il premier australiano ha discusso con il presidente esecutivo di Apple controlli sui contenuti, sicurezza online e intelligenza artificiale durante una visita a Cupertino.",
        "categoria": "Tecnologia",
        "luogo": "Cupertino",
        "formato": "standard",
        "stato": "CONFERMATA DA PIÙ FONTI",
        "parole_chiave_titolo": ["Albanese", "tutele social per i minori"],
        "dati_chiave": [
            {"icona": "◆", "valore": "16 anni", "etichetta": "soglia australiana per l’accesso ai social"},
            {"icona": "●", "valore": "1 incontro", "etichetta": "confronto a Cupertino tra governo e Apple"},
            {"icona": "▦", "valore": "3 livelli", "etichetta": "aziende, governi e regole internazionali"},
        ],
        "paragrafi": [
            "Il primo ministro australiano Anthony Albanese ha incontrato domenica 20 settembre il presidente esecutivo di Apple Tim Cook nel campus dell’azienda a Cupertino. Il colloquio ha riguardato sicurezza online dei minori, controllo dei contenuti suggeriti dalle piattaforme e regole per l’intelligenza artificiale.",
            "Albanese ha riferito che Cook considera l’approccio australiano un riferimento internazionale. La valutazione è stata resa pubblica dal premier e non equivale a un nuovo annuncio commerciale di Apple. L’incontro inserisce però le scelte di Canberra nel confronto globale sulla responsabilità delle grandi piattaforme.",
            "L’Australia vieta l’accesso ai social media ai minori di 16 anni e sta lavorando a ulteriori obblighi per ridurre i danni online. Tra le proposte discusse nel Paese c’è la possibilità di rinunciare ai sistemi che selezionano automaticamente i contenuti in base al comportamento dell’utente.",
            "Il governo sostiene che la protezione non possa dipendere soltanto dalle famiglie. Piattaforme e produttori di dispositivi dovrebbero offrire strumenti comprensibili, verificabili e adatti all’età. I critici chiedono invece prove più robuste sull’efficacia dei divieti e garanzie contro controlli invasivi dell’identità.",
            "Il colloquio ha toccato anche l’intelligenza artificiale. Albanese ha indicato tre piani di intervento: protezioni integrate dalle aziende, regole nazionali e accordi internazionali. La visita negli Stati Uniti precede i suoi impegni a New York, dove la governance dell’IA sarà tra i temi del confronto multilaterale.",
            "Resta aperta anche la questione del diritto d’autore. Il premier ha ribadito che creatori ed editori devono mantenere controllo e remunerazione quando le loro opere vengono usate nei sistemi di IA. Non è stato annunciato un accordo con Apple su licenze, compensi o nuovi prodotti.",
            "Per gli utenti, l’elemento concreto da osservare sarà l’evoluzione degli strumenti di controllo: limiti per età, impostazioni dei suggerimenti e informazioni più chiare sulle scelte automatiche. Il confronto politico non modifica oggi le funzioni degli iPhone in Italia, ma può influenzare standard adottati in altri mercati.",
        ],
        "fonti": [
            {"url": "https://www.reuters.com/business/retail-consumer/apples-tim-cook-sees-australias-social-media-curbs-world-leading-pm-says-2026-09-20/", "descrizione": "Reuters — incontro a Cupertino, dichiarazioni di Albanese e temi di sicurezza online."},
            {"url": "https://www.theguardian.com/media/2026/sep/19/australia-global-leader-online-safety-big-tech-ai-social-media", "descrizione": "The Guardian Australia — quadro delle regole australiane, controlli algoritmici e obiezioni sull’efficacia."},
            {"url": "https://www.news.com.au/technology/anthony-albanese-to-discuss-international-protocols-on-ai-in-us-visit/news-story/6edb84899104c061cf46f1a49fa436fd", "descrizione": "News.com.au — agenda statunitense del premier e proposta di regole internazionali sull’IA."},
            {"url": "https://www.theaustralian.com.au/nation/anthony-albanese-dismisses-indigenous-child-protection-crisis-as-a-problem-for-the-states/news-story/45487c841c68dbd195404e3efa17bebc", "descrizione": "The Australian — visita ad Apple e posizioni del governo su copyright e dovere di cura digitale."},
        ],
        "correlati": [
            {"url": "/notizie/come-funziona-coppa-privacy-minori-online.html", "titolo": "Come funziona la tutela della privacy dei minori online"}
        ],
        "source": "/workspace/scratch/d825bbf302f0/generated_images/exec-a44d371a-8d00-4bfa-99ae-140e1a01f7a7.png",
        "alt": "Scena editoriale contestuale generata con IA: Anthony Albanese e Tim Cook riconoscibili durante un confronto professionale in un campus tecnologico; somiglianze sintetiche, non è una fotografia documentaria.",
        "prompt": "Anthony Albanese and Tim Cook in a calm professional discussion at an Apple campus, photorealistic ordinary editorial scene, no text or fabricated handshake.",
        "synthetic": "public-figure",
        "update": False,
    },
    {
        "slug": "russia-elezioni-duma-voto-kamchatka-18-settembre-2026",
        "titolo": "Russia, ultimo giorno di voto per la Duma: risultati attesi in serata",
        "sommario": "Si chiude il primo voto parlamentare dall’invasione dell’Ucraina. Russia Unita è favorita in una competizione senza una lista federale apertamente contraria alla guerra.",
        "categoria": "Mondo",
        "luogo": "Mosca",
        "formato": "standard",
        "stato": "CONFERMATA DA PIÙ FONTI",
        "parole_chiave_titolo": ["ultimo giorno di voto", "Duma"],
        "dati_chiave": [
            {"icona": "◆", "valore": "450", "etichetta": "seggi della camera bassa in palio"},
            {"icona": "●", "valore": "3 giorni", "etichetta": "voto dal 18 al 20 settembre"},
            {"icona": "▦", "valore": "32,58%", "etichetta": "affluenza comunicata sabato pomeriggio"},
        ],
        "paragrafi": [
            "La Russia affronta domenica 20 settembre l’ultima giornata delle elezioni per rinnovare i 450 seggi della Duma di Stato. I primi risultati preliminari sono attesi in serata, dopo la chiusura delle urne distribuite su undici fusi orari.",
            "È il primo voto parlamentare dall’invasione su larga scala dell’Ucraina nel 2022. Russia Unita, il partito che sostiene Vladimir Putin, parte favorita per conservare la maggioranza. La competizione si svolge in un sistema che ha escluso gran parte dell’opposizione contraria alla guerra.",
            "Yabloko non partecipa con una lista federale dopo una decisione della Corte suprema, anche se alcuni suoi candidati corrono nei collegi individuali. Dirigenti e attivisti hanno segnalato pressioni sugli osservatori. Associated Press ha riportato l’arresto di un rappresentante del partito in un seggio di San Pietroburgo.",
            "Secondo i dati diffusi dalle autorità russe e riportati da Reuters, sabato pomeriggio aveva votato il 32,58 per cento degli aventi diritto. Il dato non consente ancora di stimare l’affluenza finale e include modalità di voto elettronico disponibili in diverse regioni.",
            "Mosca ha dichiarato di aver respinto attacchi informatici contro i sistemi elettorali e le reti di comunicazione. Le autorità hanno attribuito i tentativi all’Ucraina senza rendere pubbliche prove verificabili. Per questo l’origine degli episodi resta una rivendicazione russa, non un fatto accertato in modo indipendente.",
            "Il voto è organizzato anche nei territori ucraini occupati e annessi unilateralmente dalla Russia. Kiev e l’Unione europea considerano illegittima questa estensione e non riconosceranno i risultati prodotti in quelle aree. La Russia sostiene invece che i residenti con documenti russi abbiano diritto a partecipare.",
            "Manca inoltre una missione di osservazione dell’OSCE, il principale organismo europeo specializzato nel monitoraggio elettorale. Le autorità russe indicano centinaia di migliaia di osservatori nazionali e più di mille ospiti internazionali, ma l’assenza dell’OSCE limita un controllo esterno comparabile con altre consultazioni.",
            "La lettura politica comincerà solo quando saranno disponibili risultati per liste e collegi, affluenza finale e distribuzione territoriale. Fino ad allora è corretto descrivere Russia Unita come favorita, non come vincitrice. Eventuali contestazioni dovranno essere valutate sulla base di documenti e riscontri specifici.",
        ],
        "fonti": [
            {"url": "https://www.reuters.com/world/europe/russian-election-cast-test-support-ukraine-war-enters-final-day-2026-09-20/", "descrizione": "Reuters — giornata finale, quadro politico e calendario dei primi risultati."},
            {"url": "https://www.reuters.com/world/europe/russia-reports-online-attacks-electoral-system-second-day-parliamentary-vote-2026-09-19/", "descrizione": "Reuters — affluenza comunicata sabato e rivendicazioni russe sugli attacchi informatici."},
            {"url": "https://apnews.com/article/31a304d3156d9a066ff8001cf1338d7e", "descrizione": "Associated Press — osservatori, arresto segnalato da Yabloko e assenza della missione OSCE."},
            {"url": "https://www.theguardian.com/world/2026/sep/20/ukraine-war-briefing-kyiv-denounces-russias-inclusion-of-annexed-regions-in-parliamentary-elections", "descrizione": "The Guardian — contestazione ucraina ed europea del voto nei territori occupati."},
            {"url": "https://mirb.cikrf.ru/", "descrizione": "Commissione elettorale centrale russa — portale ufficiale del voto all’estero e informazioni elettorali."},
        ],
        "correlati": [
            {"url": "/notizie/usa-camera-sanzioni-russia-dazi-100-percento-16-settembre-2026.html", "titolo": "Camera Usa, via libera a sanzioni e dazi al 100% sulla Russia"},
            {"url": "/notizie/ue-33-miliardi-ucraina-missili-droni-17-settembre-2026.html", "titolo": "Ue, altri 3,3 miliardi all’Ucraina per missili e droni"},
        ],
        "source": "/workspace/scratch/d825bbf302f0/generated_images/exec-8025ab65-b4fd-41b3-8e68-d57fe5c86ff0.png",
        "alt": "Scena editoriale contestuale generata con IA: elettori in un seggio russo depositano schede in un’urna trasparente; non è una fotografia documentaria.",
        "prompt": "Final day of Russia State Duma election in a Moscow polling station, voters and transparent ballot box, photorealistic ordinary editorial scene, no text.",
        "synthetic": None,
        "update": True,
    },
]


def main() -> None:
    added, updated = [], []
    for index, article in enumerate(ARTICLES):
        words = sum(len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ'’]+\b", p)) for p in article["paragrafi"])
        if not 300 <= words <= 600:
            raise SystemExit(f"word gate {article['slug']}: {words}")
        source = Path(article["source"])
        local = ROOT / "generated_images" / f"v449-{index}.png"
        shutil.copy2(source, local)
        key = f"{article['slug']}-v{VERSION}"
        image = {
            "key": key,
            "aiGenerated": True,
            "documentaryPhoto": False,
            "generator": "ChatGPT/OpenAI image generation",
            "variants": variants(local, key),
            "alt": article["alt"],
            "disclosure": CAPTION,
            "sensitiveContext": False,
            "reenactedEvent": False,
            "syntheticLikeness": article["synthetic"],
            "prompt": article["prompt"],
        }
        target = ROOT / "notizie" / f"{article['slug']}.html"
        if article["update"]:
            target.unlink()
        slug = write_article(article, image, VERSION)
        html = target.read_text(encoding="utf-8")
        published = "2026-09-18T05:40:00+02:00" if article["update"] else STAMP
        html = re.sub(r'"datePublished":"[^"]+"', f'"datePublished":"{published}"', html)
        html = re.sub(r'"dateModified":"[^"]+"', f'"dateModified":"{STAMP}"', html)
        if article["update"]:
            html = html.replace("20 settembre 2026 · Mosca", "18 settembre 2026 · aggiornato il 20 settembre alle 07:08 · Mosca")
        target.write_text(html, encoding="utf-8")
        article["published"] = STAMP
        register_image(image, slug, VERSION)
        (updated if article["update"] else added).append(slug)
        write_json(Path("contenuti/notizie") / f"{slug}.json", {
            "slug": slug,
            "title": article["titolo"],
            "excerpt": article["sommario"],
            "category": article["categoria"],
            "published_at": published,
            "updated_at": STAMP,
            "development_at": DATE,
            "status": article["stato"],
            "public_url": f"https://curiomondo.it/notizie/{slug}.html",
            "publication_state": "pending_deploy",
            "body": article["paragrafi"],
            "sources": article["fonti"],
            "image": image,
        })

    sync_surfaces(ARTICLES, "", VERSION)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": DATE,
        "type": "news-update",
        "news_added": added,
        "news_updated": updated,
        "change": "Nuovo articolo su sicurezza online e aggiornamento delle elezioni russe",
        "image_policy_applied": "new-openai-contextual-editorial-images",
    }
    write_json(Path("curiomondo-site-manifest.json"), manifest)
    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": DATE,
            "release_date": DATE,
            "last_update": "news-update-v449",
            "articleCount": int(state.get("articleCount", 0)) + 1,
            "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + 2,
        })
        write_json(Path(name), state)
    write_json(Path("automation/logs/editoriale-20260920T070800-Europe-Rome.json"), {
        "run_at": STAMP,
        "processed": [
            {"title": article["titolo"], "decision": "update" if article["update"] else "publish"}
            for article in ARTICLES
        ],
    })
    print(json.dumps({"added": added, "updated": updated}, ensure_ascii=False))


if __name__ == "__main__":
    main()
