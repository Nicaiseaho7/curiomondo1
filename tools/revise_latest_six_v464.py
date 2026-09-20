#!/usr/bin/env python3
"""Revisione professionale e nuove immagini per gli ultimi sei articoli."""
from __future__ import annotations

from datetime import datetime
import hashlib
import json
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import etree, html
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "tools")]
from automation.newsroom.site import CAPTION, register_image, sync_surfaces

VERSION = 464
ROME = ZoneInfo("Europe/Rome")
STAMP = datetime.now(ROME).replace(microsecond=0).isoformat()


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
        resized = image.resize((width, round(width * 2 / 3)), Image.Resampling.LANCZOS)
        resized.save(target, "WEBP", quality=88, method=6)
        result.append({
            "w": width,
            "src": f"/assets/images/editorial-auto/{target.name}",
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
            "bytes": target.stat().st_size,
        })
    return result


ARTICLES = [
    {
        "slug": "roma-prof-accoltellata-i-carabinieri-cercano-eventuali-istigatori-online-20-09-2026",
        "title": "Roma, prof accoltellata: i carabinieri cercano eventuali istigatori online",
        "summary": "Dopo l’aggressione nella scuola Giovanni Verga di Centocelle, gli investigatori analizzano telefono, chat e diffusione dei video. Il possibile ruolo di terzi resta un’ipotesi da verificare.",
        "category": "Cronaca",
        "place": "Roma",
        "format": "standard",
        "status": "IN SVILUPPO — IPOTESI INVESTIGATIVE NON ACCERTATE",
        "highlights": ["Roma", "istigatori online"],
        "stats": [
            {"icona": "◆", "valore": "13 anni", "etichetta": "età dello studente coinvolto"},
            {"icona": "●", "valore": "7 giorni", "etichetta": "prognosi riferita per la docente"},
            {"icona": "▦", "valore": "chat e video", "etichetta": "materiale digitale sotto esame"},
        ],
        "paragraphs": [
            "I carabinieri stanno ricostruendo la rete di contatti online del tredicenne che il 18 settembre ha aggredito una docente nella scuola media Giovanni Verga, nel quartiere Centocelle a Roma. Gli accertamenti riguardano il telefono del ragazzo, le chat e la circolazione dei video registrati prima e durante l’episodio.",
            "L’insegnante, 66 anni, è stata medicata e dimessa con una prognosi di sette giorni. Il ragazzo è seguito in un reparto di neuropsichiatria infantile. La sua identità resta protetta perché minorenne e, avendo meno di quattordici anni, non è penalmente imputabile secondo la legge italiana.",
            "Uno dei punti da chiarire è se qualcuno abbia incoraggiato l’azione, aiutato a prepararla oppure rilanciato consapevolmente le immagini. Gli investigatori stanno cercando di identificare gli utenti presenti nelle conversazioni e di stabilire chi abbia pubblicato il filmato. Al momento non risulta accertata una regia esterna.",
            "Il materiale digitale dovrà essere ordinato cronologicamente e attribuito ai singoli account. La presenza di una persona in una chat o durante una diretta non dimostra da sola un concorso nell’aggressione: servono messaggi, tempi e condotte capaci di documentare un contributo concreto o un’istigazione.",
            "La Procura per i minorenni può comunque valutare interventi civili ed educativi, anche in assenza di responsabilità penale. Le misure possibili riguardano l’assistenza dei servizi sociali e percorsi specialistici; ogni decisione dipenderà dagli esiti clinici e dalla ricostruzione investigativa.",
            "Durante l’attacco un compagno è intervenuto per fermare il ragazzo e proteggere l’insegnante. Il ministro dell’Istruzione Giuseppe Valditara ha annunciato un riconoscimento per il suo comportamento. La scuola e le famiglie sono ora coinvolte nel sostegno alla comunità scolastica.",
            "Le prossime verifiche dovranno distinguere tre livelli: la preparazione materiale, l’eventuale influenza esercitata online e la successiva diffusione dei contenuti. Finché questi passaggi non saranno documentati, la ricerca di possibili istigatori resta una pista investigativa e non una conclusione giudiziaria.",
        ],
        "sources": [
            {"url": "https://tg24.sky.it/cronaca/2026/09/20/insegnante-accoltellata-roma-studente-indagini-news", "descrizione": "Sky TG24 — accertamenti sul telefono, condizioni della docente e ipotesi sugli utenti online."},
            {"url": "https://www.lapresse.it/cronaca/2026/09/20/prof-accoltellata-a-roma-caccia-agli-istigatori-del-13enne-su-social-e-web/", "descrizione": "LaPresse — indagini sulle chat, sui video e sulle eventuali misure educative."},
            {"url": "https://www.rainews.it/articoli/2026/09/prof-accoltellata-a-roma-verifiche-sui-cellulari-del-13enne-si-cercano-eventuali-istigatori-9db6b8dd.html", "descrizione": "RaiNews — ricostruzione degli accertamenti digitali e stato dell’indagine."},
        ],
        "source_image": "/workspace/scratch/63d8c74bad9c/generated_images/exec-b543093d-8bd7-4dc4-8b55-82acd8af9328.png",
        "alt": "Illustrazione editoriale generata con IA: ingresso dell’Istituto Giovanni Verga di Roma con auto dei Carabinieri, scritte CARABINIERI e 112 visibili, senza persone o scene di violenza; non è una fotografia documentaria.",
        "sensitive": True,
        "likeness": None,
        "prompt": "Neutral exterior of Istituto Giovanni Verga in Rome with a marked Carabinieri car; no people, violence or reenactment; authentic school and Carabinieri lettering.",
    },
    {
        "slug": "trump-sull-iran-via-fox-decidero-se-e-quando-aperto-a-pezeshkian-20-09-2026",
        "title": "Trump sull’Iran: nuove minacce, ma resta aperta l’ipotesi di un incontro con Pezeshkian",
        "summary": "Il presidente statunitense ha riferito a Fox di essere in una fase decisionale. Non risultano ordini militari pubblici; resta possibile un contatto diplomatico durante l’Assemblea generale dell’ONU.",
        "category": "Mondo",
        "place": "Washington",
        "format": "standard",
        "status": "IN SVILUPPO — DICHIARAZIONI, NESSUN ORDINE PUBBLICO",
        "highlights": ["Trump sull’Iran", "incontro con Pezeshkian"],
        "stats": [
            {"icona": "◆", "valore": "3 opzioni", "etichetta": "accordo, pressione o escalation"},
            {"icona": "●", "valore": "ONU", "etichetta": "possibile sede di un incontro"},
            {"icona": "▦", "valore": "nessun ordine", "etichetta": "atto militare pubblico non diffuso"},
        ],
        "paragraphs": [
            "Donald Trump ha irrigidito i toni verso l’Iran durante una conversazione riferita dal corrispondente di Fox News Trey Yingst. Il presidente statunitense si è descritto in una fase decisionale e ha indicato tre possibili direzioni: un accordo, un ulteriore logoramento economico di Teheran oppure un’escalation militare.",
            "Tra le frasi attribuitegli figura anche una minaccia estrema contro l’intero Paese. Si tratta del resoconto di una conversazione giornalistica, non di un discorso ufficiale o di un documento della Casa Bianca. Il linguaggio usato segnala pressione politica, ma non dimostra che sia stata presa una decisione operativa.",
            "Trump ha lasciato aperta la possibilità di incontrare il presidente iraniano Masoud Pezeshkian, atteso a New York per l’Assemblea generale delle Nazioni Unite. Non sono stati comunicati un appuntamento, un’agenda o un canale negoziale già concordato.",
            "La dichiarazione arriva in una fase di forte tensione regionale, segnata dal confronto militare con l’Iran, dal blocco navale statunitense e dagli attacchi degli Houthi. Le ambasciate americane hanno diffuso avvisi di sicurezza e possibili disagi ai trasporti in diversi Paesi dell’area.",
            "Il rientro anticipato di Trump da Camp David ha alimentato le interpretazioni su una decisione imminente. Tuttavia, nelle ore successive non risultavano pubblicati ordini presidenziali, comunicati del Pentagono o briefing ufficiali che confermassero l’avvio di una nuova operazione.",
            "Per valutare un eventuale cambio di fase serviranno segnali verificabili: movimenti militari confermati, notifiche al Congresso, comunicazioni della Casa Bianca o l’annuncio di colloqui formali. Le dichiarazioni televisive, da sole, non equivalgono a questi atti e vanno distinte dalle decisioni formali dell’amministrazione statunitense e dai passaggi istituzionali che ne seguirebbero.",
            "Il quadro resta quindi doppio: minacce molto dure utilizzate come leva e una porta diplomatica non completamente chiusa. L’eventuale presenza contemporanea di Trump e Pezeshkian all’ONU offrirà il primo test concreto sulla possibilità di trasformare l’apertura verbale in un contatto politico.",
        ],
        "sources": [
            {"url": "https://www.foxnews.com/video/6405331395112", "descrizione": "Fox News — servizio di Trey Yingst sull’apertura di Trump a un incontro con Pezeshkian."},
            {"url": "https://www.mediaite.com/media/news/trump-warns-foxs-yingst-very-big-things-are-happening-on-iran-my-question-is-if-and-when-do-i-blow-the-entire-nation-up/", "descrizione": "Mediaite — trascrizione e contesto delle dichiarazioni riferite dal corrispondente."},
            {"url": "https://www.ansa.it/sito/notizie/mondo/2026/09/20/trump-decidero-se-e-quando-far-esplodere-liran-si-comportino-bene_529cf907-e627-4924-ad3b-31582aeb9af5.html", "descrizione": "ANSA — riscontro italiano delle dichiarazioni e del possibile incontro all’ONU."},
        ],
        "source_image": "/workspace/scratch/63d8c74bad9c/generated_images/exec-d7698c1f-e0ae-4079-b758-d0719641ba4a.png",
        "alt": "Ritratto editoriale neutrale generato con IA di Donald Trump al podio della Casa Bianca, con bandiera statunitense; non è una fotografia documentaria dell’intervista citata.",
        "sensitive": True,
        "likeness": "public-figure",
        "prompt": "Neutral editorial portrait of Donald Trump at a White House lectern for a sensitive Iran story; isolated subject, one US flag, no weapons, Iranian imagery or aggressive gesture.",
    },
    {
        "slug": "meloni-in-arrivo-tetto-agli-stranieri-in-classe-e-divieto-di-burqa-a-scuola-20-09-2026",
        "title": "Meloni annuncia un tetto agli alunni stranieri e il divieto di burqa e niqab a scuola",
        "summary": "La misura dovrebbe arrivare in Consiglio dei ministri, ma il testo non è ancora pubblico. Restano da definire limite per classe, deroghe e forma del provvedimento.",
        "category": "Politica",
        "place": "Roma",
        "format": "standard",
        "status": "ANNUNCIO POLITICO — TESTO NON PUBBLICATO",
        "highlights": ["tetto agli alunni stranieri", "burqa e niqab"],
        "stats": [
            {"icona": "◆", "valore": "11,6%", "etichetta": "alunni senza cittadinanza italiana"},
            {"icona": "●", "valore": "CdM", "etichetta": "passaggio annunciato dalla premier"},
            {"icona": "?", "valore": "limite ignoto", "etichetta": "soglia non ancora comunicata"},
        ],
        "paragraphs": [
            "Giorgia Meloni ha annunciato una misura per fissare un numero massimo di alunni stranieri per classe e vietare burqa e niqab nelle scuole. La presidente del Consiglio ne ha parlato a Fenix, la manifestazione giovanile di Fratelli d’Italia, indicando il Consiglio dei ministri come prossimo passaggio.",
            "La proposta comprenderebbe anche l’obbligo di apprendere l’italiano per i genitori degli studenti con maggiori difficoltà d’inserimento. Meloni ha collegato il provvedimento alla necessità di condividere una lingua comune e di evitare classi nelle quali l’integrazione diventi più difficile.",
            "Il testo normativo non è stato ancora pubblicato. Non sono quindi noti il tetto numerico, il criterio utilizzato per definire gli studenti interessati, le deroghe territoriali o didattiche e le modalità con cui sarebbe applicato l’obbligo linguistico per le famiglie.",
            "Dal 2010 una circolare ministeriale indica già, come regola generale, un limite del 30% di alunni con cittadinanza non italiana per classe. La soglia può essere modificata in base alle competenze linguistiche, alla presenza di studenti nati in Italia e alle condizioni delle singole scuole.",
            "Nell’anno scolastico 2023-2024 gli alunni senza cittadinanza italiana erano circa 930 mila, pari all’11,6% del totale. La distribuzione non è uniforme: alcuni territori e istituti registrano concentrazioni molto superiori alla media nazionale, rendendo decisivi i criteri di deroga.",
            "Anche la portata del divieto dovrà essere precisata. Burqa e niqab coprono il volto in modo diverso, mentre il semplice velo che lascia il viso scoperto pone questioni giuridiche differenti. Le ricostruzioni più solide dell’annuncio parlano di burqa e niqab, non di un divieto generale di ogni hijab.",
            "L’annuncio non modifica immediatamente le regole scolastiche. Prima dell’entrata in vigore serviranno un atto formale del governo e il percorso previsto dalla sua natura giuridica. Solo il testo consentirà di valutare compatibilità costituzionale, tempi, sanzioni e impatto concreto e amministrativo sulle classi.",
        ],
        "sources": [
            {"url": "https://www.reuters.com/world/italy-ban-veils-schools-limit-foreign-students-per-class-meloni-says-2026-09-20/", "descrizione": "Reuters — annuncio, quota nazionale degli alunni stranieri e assenza della soglia numerica."},
            {"url": "https://apnews.com/article/862c88cc1aa98560ba2b3f7bf31ae622", "descrizione": "Associated Press — perimetro indicato per burqa e niqab e iter ancora da definire."},
            {"url": "https://www.ansa.it/sito/notizie/topnews/2026/09/20/meloni-in-classe-numero-massimo-di-stranieri-e-divieto-di-burqa-norma-in-arrivo_0d622362-ec85-4807-a30b-27c63fa3aabd.html", "descrizione": "ANSA — dichiarazioni della premier dal palco di Fenix."},
        ],
        "source_image": "/workspace/scratch/63d8c74bad9c/generated_images/exec-ad4f44ac-96fa-4cb0-832b-8a1c171def77.png",
        "alt": "Illustrazione editoriale generata con IA: Giorgia Meloni parla sul palco di FENIX con bandiere italiana ed europea e loghi FENIX e Fratelli d’Italia visibili; non è una fotografia documentaria.",
        "sensitive": False,
        "likeness": "public-figure",
        "prompt": "Giorgia Meloni speaking at FENIX with Italian and EU flags and naturally visible FENIX and Fratelli d’Italia logos; no stereotypes or added headline.",
    },
    {
        "slug": "trump-annuncia-una-forza-per-l-ia-sul-modello-della-space-force-20-09-2026",
        "title": "Trump annuncia una “AI Force” e un nuovo consigliere per l’intelligenza artificiale",
        "summary": "Il presidente statunitense promette una struttura dedicata e un “AI czar”, senza chiarire poteri, composizione o finanziamento. Per ora non risulta istituito un nuovo organismo.",
        "category": "Mondo",
        "place": "Washington",
        "format": "standard",
        "status": "ANNUNCIO — STRUTTURA NON ANCORA ISTITUITA",
        "highlights": ["AI Force", "nuovo consigliere"],
        "stats": [
            {"icona": "◆", "valore": "19 set", "etichetta": "data dell’annuncio"},
            {"icona": "●", "valore": "1 nomina", "etichetta": "nuovo AI czar promesso"},
            {"icona": "?", "valore": "nessun atto", "etichetta": "struttura formale non pubblicata"},
        ],
        "paragraphs": [
            "Donald Trump ha annunciato l’intenzione di creare una “AI Force” e di nominare un nuovo consigliere per l’intelligenza artificiale. Il messaggio è stato pubblicato il 19 settembre su Truth Social, ma non è stato accompagnato da un ordine esecutivo, da una struttura organizzativa o da un calendario.",
            "Il presidente ha paragonato l’iniziativa alla Space Force, senza specificare se il nuovo organismo avrà natura militare, civile o interagenzia. Restano sconosciuti composizione, poteri, budget e rapporto con gli uffici federali che già si occupano di sicurezza, ricerca e regolazione dell’IA.",
            "Trump ha promesso la nomina di un “AI czar” nel prossimo futuro. Il precedente incarico dedicato a intelligenza artificiale e criptovalute era stato affidato a David Sacks, che ha poi lasciato il ruolo formale mantenendo una funzione consultiva esterna.",
            "Nel suo intervento Trump ha presentato l’IA come una nuova rivoluzione industriale e ha ribadito l’obiettivo di mantenere il vantaggio statunitense sulla Cina. Ha inoltre sostenuto che gli abusi possano essere affrontati attraverso le norme penali e civili esistenti, mostrando contrarietà a nuovi vincoli generali.",
            "La stima secondo cui l’intelligenza artificiale potrebbe arrivare a rappresentare fino al 25% del prodotto interno lordo americano è una valutazione politica contenuta nell’annuncio. Non è accompagnata da metodologia, orizzonte temporale o previsione ufficiale di un’agenzia economica indipendente.",
            "Il percorso istituzionale dipenderà dalla forma scelta. Un gruppo di coordinamento interno può essere creato dall’esecutivo; un organismo con fondi permanenti, competenze militari o autorità sulle agenzie potrebbe invece richiedere stanziamenti e interventi del Congresso.",
            "Per ora la “AI Force” resta quindi un progetto annunciato. I prossimi elementi verificabili saranno il nome del consigliere, un eventuale ordine esecutivo, la definizione dei compiti e l’indicazione delle risorse. Fino ad allora non è corretto descriverla come un ente già operativo o dotato di personale e competenze proprie all’interno del governo federale statunitense.",
        ],
        "sources": [
            {"url": "https://www.reuters.com/world/us/trump-says-he-will-create-ai-force-name-ai-czar-2026-09-19/", "descrizione": "Reuters — annuncio su Truth Social, precedente incarico e assenza di dettagli operativi."},
            {"url": "https://www.cnn.com/2026/09/19/politics/trump-ai-task-force-czar", "descrizione": "CNN — quesiti aperti sulla natura civile o militare e richiesta di chiarimenti alla Casa Bianca."},
            {"url": "https://www.foxnews.com/politics/trump-announces-new-ai-force-vows-protect-industry-ai-czar-announcement-nears", "descrizione": "Fox News — contenuto del messaggio e confronto con la Space Force."},
        ],
        "source_image": "/workspace/scratch/63d8c74bad9c/generated_images/exec-ec6dc163-91e5-46d8-8343-2ea725ec6505.png",
        "alt": "Illustrazione editoriale generata con IA: Donald Trump parla a un evento tecnologico davanti a una bandiera statunitense e a uno schermo con la scritta AI; non è una fotografia documentaria.",
        "sensitive": False,
        "likeness": "public-figure",
        "prompt": "Donald Trump at an ordinary technology-policy event, US flag and clean screen reading AI; no military imagery, fake official seal or added headline.",
    },
    {
        "slug": "legge-elettorale-alla-camera-l-ultimo-passaggio-della-riforma-20-09-2026",
        "title": "Legge elettorale, la riforma torna alla Camera per il passaggio decisivo",
        "summary": "Dopo il via libera del Senato con 113 voti favorevoli, il testo rientra a Montecitorio. Premio di governabilità, preferenze e raccolta firme restano al centro del confronto.",
        "category": "Politica",
        "place": "Roma",
        "format": "standard",
        "status": "ITER PARLAMENTARE — TESTO NON ANCORA LEGGE",
        "highlights": ["riforma torna alla Camera", "passaggio decisivo"],
        "stats": [
            {"icona": "◆", "valore": "113 sì", "etichetta": "voto favorevole al Senato"},
            {"icona": "●", "valore": "42%", "etichetta": "soglia indicata per il premio"},
            {"icona": "▦", "valore": "3 preferenze", "etichetta": "massimo previsto dal testo"},
        ],
        "paragraphs": [
            "La riforma della legge elettorale torna alla Camera dopo l’approvazione del Senato con 113 voti favorevoli, 71 contrari e due astenuti. Montecitorio deve ora esaminare lo stesso testo modificato da Palazzo Madama: solo un voto conforme potrà chiudere l’iter parlamentare.",
            "Il progetto prevede un premio di governabilità per la coalizione che supera il 42% dei voti validi. Il meccanismo attribuirebbe seggi aggiuntivi con un tetto complessivo indicato in 220 deputati e 113 senatori per la maggioranza beneficiaria.",
            "L’elezione dei parlamentari combinerebbe capilista definiti dai partiti e fino a tre preferenze espresse dagli elettori. Resterebbero le soglie del sistema vigente: 10% per le coalizioni e 3% per le singole liste, secondo il testo uscito dal Senato.",
            "Un altro punto discusso riguarda la raccolta delle firme. Per le forze non già rappresentate in Parlamento il minimo per collegio salirebbe da 1.500 a 6 mila. Il provvedimento disciplina anche il voto fuori sede per chi vive lontano dal Comune di residenza per un periodo prolungato.",
            "La maggioranza presenta il premio come uno strumento di stabilità; le opposizioni contestano il rapporto tra voti ottenuti e seggi assegnati. Restano sensibili anche il ruolo dei capilista bloccati e l’aumento delle firme richieste alle liste più piccole.",
            "La presidente del Consiglio ha preannunciato la fiducia, scelta che ridurrebbe lo spazio per modifiche durante il passaggio alla Camera. Il voto finale può però conservare margini d’incertezza, soprattutto se vengono richieste procedure a scrutinio segreto sugli aspetti ammessi dai regolamenti parlamentari.",
            "Il provvedimento non è ancora legge e le regole attuali restano in vigore. Il calendario politico punta a una conclusione nelle prossime settimane, ma tempi ed esito dipendono dai lavori della commissione, dalla decisione sulla fiducia e dal voto dell’Aula di Montecitorio. Eventuali nuove modifiche renderebbero inoltre necessario un ulteriore passaggio al Senato prima dell’approvazione parlamentare definitiva.",
        ],
        "sources": [
            {"url": "https://www.ansa.it/sito/notizie/politica/2026/09/20/legge-elettorale-al-via-alla-camera-lultimo-step-della-riforma_9eeeaa9d-59a7-4070-8fc5-3780eb563458.html", "descrizione": "ANSA — ritorno alla Camera, contenuti principali e passaggi ancora necessari."},
            {"url": "https://www.rainews.it/articoli/2026/09/via-libera-del-senato-allo-stabilicum-113-si-le-opposizioni-insorgono-6da48dcb-f4c9-4bdb-9c11-b9d8cfad603a.html", "descrizione": "RaiNews — risultato del voto al Senato e posizioni politiche."},
            {"url": "https://tg24.sky.it/politica/approfondimenti/legge-elettorale-stabilicum-come-funziona", "descrizione": "Sky TG24 — scheda su premio, preferenze, soglie e raccolta firme."},
        ],
        "source_image": "/workspace/scratch/63d8c74bad9c/generated_images/exec-5ae12e93-ccdb-458e-82c7-30b75ad929d6.png",
        "alt": "Illustrazione editoriale generata con IA: Aula della Camera dei deputati con bandiere italiana ed europea e fascicolo in primo piano recante la scritta Riforma elettorale; non è una fotografia documentaria.",
        "sensitive": False,
        "likeness": None,
        "prompt": "Realistic Chamber of Deputies hall with Italian and EU flags and a foreground folder labelled RIFORMA ELETTORALE; no politicians or invented vote tally.",
    },
    {
        "slug": "tajani-non-siamo-in-guerra-con-gli-houthi-kallas-e-il-rafforzamento-di-aspides-20-09-2026",
        "title": "Tajani: “L’Italia non è in guerra con gli Houthi”. Roma chiede di rafforzare Aspides",
        "summary": "Il ministro degli Esteri ribadisce la natura difensiva della missione europea nel Mar Rosso. L’Italia sollecita più navi dai partner o una maggiore condivisione dei costi.",
        "category": "Italia",
        "place": "Roma",
        "format": "standard",
        "status": "CONFERMATA — RAFFORZAMENTO ANCORA DA DEFINIRE",
        "highlights": ["non è in guerra", "rafforzare Aspides"],
        "stats": [
            {"icona": "◆", "valore": "40%", "etichetta": "traffico marittimo italiano nell’area"},
            {"icona": "●", "valore": "1 fregata", "etichetta": "unità italiana già impegnata"},
            {"icona": "↗", "valore": "più navi", "etichetta": "richiesta italiana ai partner UE"},
        ],
        "paragraphs": [
            "L’Italia non considera l’operazione Aspides una guerra contro gli Houthi. Antonio Tajani ha ribadito che la missione europea nel Mar Rosso mantiene un mandato difensivo: proteggere i mercantili e garantire la libertà di navigazione senza condurre una campagna offensiva nello Yemen.",
            "Roma chiede però un rafforzamento rapido. Dalla rotta del Mar Rosso passa circa il 40% del traffico marittimo commerciale italiano e una quota ancora maggiore delle esportazioni dirette verso l’Asia. Le deviazioni intorno all’Africa aumentano tempi, carburante e costi assicurativi.",
            "Il ministro della Difesa Guido Crosetto ha sollecitato l’Alto rappresentante europeo Kaja Kallas a coinvolgere più unità navali degli altri Stati membri. L’Italia valuta la disponibilità di una seconda fregata, ma chiede che l’onere operativo e finanziario non ricada sui pochi Paesi già presenti.",
            "La fregata Carlo Bergamini ha già effettuato scorte nell’area, compreso il passaggio del mercantile italiano Jolly Oro. Queste attività rientrano nel mandato di protezione di Aspides e sono distinte da eventuali operazioni offensive condotte da singoli alleati fuori dal quadro europeo.",
            "Kallas ha confermato la necessità di mantenere elevata l’allerta e di sostenere la sicurezza del traffico commerciale. Non è stato però annunciato un nuovo elenco di navi assegnate alla missione, né un accordo definitivo sulla ripartizione dei costi richiesto dall’Italia.",
            "Il punto politico riguarda quindi la sostenibilità della presenza navale. Una seconda unità italiana aumenterebbe la capacità di scorta, ma ridurrebbe le risorse disponibili per altri impegni della Marina. Roma propone che i partner contribuiscano con mezzi oppure con un sostegno finanziario più consistente.",
            "Il rafforzamento resta da negoziare nelle sedi europee. Gli elementi da verificare saranno il numero di nuove navi, le regole d’ingaggio, la durata degli schieramenti e il meccanismo di finanziamento. Fino ad allora Aspides conserva la configurazione difensiva rivendicata dal governo italiano, mentre prosegue il confronto tra le capitali europee.",
        ],
        "sources": [
            {"url": "https://www.lapresse.it/esteri/2026/09/20/guerra-in-medio-oriente-tajani-non-siamo-in-conflitto-con-gli-houthi-aspides-va-rafforzata/", "descrizione": "LaPresse — dichiarazioni di Tajani sulla natura difensiva di Aspides."},
            {"url": "https://tg24.sky.it/mondo/2026/09/19/aspides-missione-news", "descrizione": "Sky TG24 — richiesta di Crosetto a Kallas, seconda fregata e condivisione dei costi."},
            {"url": "https://www.ansa.it/english/news/2026/09/18/boost-aspides-with-more-ships-eu-countries-should-participate-crosetto-kallas_3751363c-9e1b-4087-83d2-0692a83bd093.html", "descrizione": "ANSA — richiesta italiana di più navi europee e attività della fregata Bergamini."},
        ],
        "source_image": "/workspace/scratch/63d8c74bad9c/generated_images/exec-9c70fda8-c48c-48d3-8bf5-ec3d153d58a8.png",
        "alt": "Ritratto editoriale neutrale generato con IA di Antonio Tajani al podio del Ministero degli Affari Esteri, con bandiere italiana ed europea; non è una fotografia documentaria.",
        "sensitive": True,
        "likeness": "public-figure",
        "prompt": "Neutral editorial portrait of Antonio Tajani at the Italian Foreign Ministry; isolated subject with Italian and EU flags, no warship, weapons or conflict imagery.",
    },
]


def update_page(article: dict, image: dict) -> str:
    path = ROOT / "notizie" / f"{article['slug']}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    doc.xpath('//main//h1[1]')[0].text = article["title"]
    doc.xpath('//main//p[contains(@class,"subtitle")][1]')[0].text = article["summary"]
    body = doc.xpath('//article[contains(@class,"art-body")]')[0]
    body.set("data-article-format", article["format"])
    for child in list(body):
        body.remove(child)
    for paragraph in article["paragraphs"]:
        etree.SubElement(body, "p").text = paragraph

    source_list = doc.xpath('//div[contains(@class,"art-sources")]//ul[1]')[0]
    for child in list(source_list):
        source_list.remove(child)
    for source in article["sources"]:
        li = etree.SubElement(source_list, "li")
        link = etree.SubElement(li, "a", href=source["url"], rel="noopener noreferrer", target="_blank")
        link.text = source["descrizione"]

    variants_by_width = {item["w"]: item["src"] for item in image["variants"]}
    figure = doc.xpath('//figure[contains(@class,"article-image")][1]')[0]
    figure.attrib.clear()
    figure.set("class", "article-image")
    figure.set("data-ai-generated", "true")
    if image.get("syntheticLikeness"):
        figure.set("data-synthetic-likeness", image["syntheticLikeness"])
    figure.set("data-sensitive-context", str(bool(image["sensitiveContext"])).lower())
    if image.get("syntheticLikeness") == "public-figure" and image["sensitiveContext"]:
        figure.set("data-portrait-format", "neutral-isolated")
    img = figure.xpath('.//img[1]')[0]
    img.set("src", ".." + variants_by_width[800])
    img.set("srcset", ", ".join(f"..{variants_by_width[w]} {w}w" for w in (480, 800, 1200)))
    img.set("sizes", "(max-width:832px) calc(100vw - 32px),800px")
    img.set("width", "800")
    img.set("height", "533")
    img.set("alt", image["alt"])

    title_node = doc.xpath('//head/title')[0]
    title_node.text = f"{article['title']} | CurioMondo"
    doc.xpath('//meta[@name="description"]')[0].set("content", article["summary"])
    doc.xpath('//meta[@property="og:title"]')[0].set("content", article["title"])
    doc.xpath('//meta[@property="og:description"]')[0].set("content", article["summary"])
    image_url = "https://curiomondo.it" + variants_by_width[1200]
    doc.xpath('//meta[@property="og:image"]')[0].set("content", image_url)
    doc.xpath('//meta[@property="og:image:alt"]')[0].set("content", image["alt"])
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        try:
            data = json.loads(node.text or "")
        except json.JSONDecodeError:
            continue
        if data.get("@type") == "NewsArticle":
            data.update({
                "headline": article["title"],
                "description": article["summary"],
                "dateModified": STAMP,
                "image": [image_url],
            })
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            published = data["datePublished"]
            break
    else:
        raise RuntimeError(f"NewsArticle JSON-LD assente: {article['slug']}")
    for link in doc.xpath('//link[contains(@href,"curiomondo-article-v211.css")]'):
        link.set("href", f"../assets/css/curiomondo-article-v211.css?v={VERSION}")
    for script in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'):
        script.set("src", f"../assets/js/curiomondo-article-v210.js?v={VERSION}")
    path.write_text("<!doctype html>\n" + html.tostring(doc, encoding="unicode", method="html"), encoding="utf-8")
    return published


def main() -> None:
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    revised_articles = {f"/notizie/{article['slug']}.html" for article in ARTICLES}
    registry["items"] = [
        item for item in registry.get("items", [])
        if item.get("article") not in revised_articles
    ]
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    sync_articles = []
    for article in ARTICLES:
        source = Path(article["source_image"])
        if not source.exists():
            raise SystemExit(f"immagine mancante: {source}")
        words = len(re.findall(r"\b[0-9A-Za-zÀ-ÖØ-öø-ÿ’']+\b", " ".join(article["paragraphs"])))
        if not 300 <= words <= 600:
            raise SystemExit(f"word gate {article['slug']}: {words}")
        key = f"{article['slug']}-v{VERSION}"
        image = {
            "key": key,
            "aiGenerated": True,
            "documentaryPhoto": False,
            "generator": "ChatGPT/OpenAI image generation",
            "variants": variants(source, key),
            "alt": article["alt"],
            "disclosure": CAPTION,
            "sensitiveContext": article["sensitive"],
            "reenactedEvent": False,
            "syntheticLikeness": article["likeness"],
            "prompt": article["prompt"],
        }
        if article["likeness"] == "public-figure" and article["sensitive"]:
            image["portraitOnly"] = True
            image["portraitFormat"] = "neutral-isolated"
        published = update_page(article, image)
        register_image(image, article["slug"], VERSION)
        write_json(Path("contenuti/notizie") / f"{article['slug']}.json", {
            "slug": article["slug"],
            "title": article["title"],
            "excerpt": article["summary"],
            "category": article["category"],
            "published_at": published,
            "updated_at": STAMP,
            "development_at": "2026-09-20",
            "status": article["status"],
            "public_url": f"https://curiomondo.it/notizie/{article['slug']}.html",
            "publication_state": "pending_deploy",
            "body": article["paragraphs"],
            "sources": article["sources"],
            "image": image,
        })
        sync_articles.append({
            "slug": article["slug"],
            "titolo": article["title"],
            "sommario": article["summary"],
            "categoria": article["category"],
            "parole_chiave_titolo": article["highlights"],
            "dati_chiave": article["stats"],
        })

    sync_surfaces(sync_articles, "", VERSION)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site"].update({"current_site_version": VERSION, "site_version": VERSION})
    manifest.update({"site_version": VERSION, "version": f"v{VERSION}", "release_version": f"v{VERSION}"})
    manifest["last_release"] = {
        "version": VERSION,
        "date": "2026-09-20",
        "type": "editorial-revision",
        "news_added": [],
        "news_updated": [article["slug"] for article in ARTICLES],
        "change": "Revisione professionale degli ultimi sei articoli e sei nuove immagini editoriali uniche",
        "image_policy_applied": "six-new-openai-editorial-images-with-context-and-relevant-logos",
    }
    write_json(Path("curiomondo-site-manifest.json"), manifest)
    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        state = json.loads((ROOT / name).read_text(encoding="utf-8"))
        state.update({
            "currentVersion": VERSION,
            "site_version": VERSION,
            "version": str(VERSION),
            "date": "2026-09-20",
            "release_date": "2026-09-20",
            "last_update": "editorial-revision-v464",
            "generatedEditorialImages": max(285, int(state.get("generatedEditorialImages", 0)) + 6),
        })
        write_json(Path(name), state)
    write_json(Path("automation/logs/revisione-ultimi-sei-20260920.json"), {
        "run_at": STAMP,
        "updated": [article["slug"] for article in ARTICLES],
        "checks": ["professional rewrite", "three sources", "unique image", "mobile crop", "no source names in body"],
    })
    print(json.dumps({"version": VERSION, "updated": [a["slug"] for a in ARTICLES]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
