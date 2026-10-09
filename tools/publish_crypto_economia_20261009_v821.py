#!/usr/bin/env python3
"""Release v821: cinque notizie crypto e cinque notizie economiche del 9 ottobre 2026."""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from lxml import html
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site  # noqa: E402

VERSION = 821
ROME = ZoneInfo("Europe/Rome")
GENERATED = ROOT.parent / "generated_images"

IMAGE_SOURCES = {
    "stablecoin_mica": GENERATED / "exec-99782685-fce1-4c43-b1b4-45818ea07e51.png",
    "token_collateral": GENERATED / "exec-2fdacc92-385d-4a06-9120-df82762fdd49.png",
    "samsung_usdc": GENERATED / "exec-70070425-338e-430b-893f-e6ccfe5dd48d.png",
    "circle_sap": GENERATED / "exec-89fdfd05-7bc6-41c4-9c9c-7b5c4983776c.png",
    "coinbase_fraud": GENERATED / "exec-f6ed7965-33bc-4b28-b2d4-c36fbac2e935.png",
    "edilizia": GENERATED / "exec-95d73030-2cd6-4f78-bc81-ea84ec9aa066.png",
    "capitali_ue": GENERATED / "exec-9c03afe6-bc52-49ce-ab5d-1f91ea7f6083.png",
    "lista_fiscale": GENERATED / "exec-fb30f3ef-8dcd-445e-89fc-703f71a9a9c1.png",
    "materie_prime": GENERATED / "exec-57f81acc-54ed-4729-b36a-569420258b72.png",
    "difesa_ue": GENERATED / "exec-a97fe76b-bfcb-459d-b84a-6e63b2e8d725.png",
}


def make_variants(source: Path, slug: str) -> list[dict]:
    image = Image.open(source).convert("RGB")
    ratio = 16 / 9
    if image.width / image.height > ratio:
        width = round(image.height * ratio)
        left = (image.width - width) // 2
        image = image.crop((left, 0, left + width, image.height))
    else:
        height = round(image.width / ratio)
        top = (image.height - height) // 2
        image = image.crop((0, top, image.width, top + height))
    output = ROOT / "assets/images/editorial-auto"
    variants = []
    for width in (480, 800, 1200):
        path = output / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, round(width / ratio)), Image.Resampling.LANCZOS).save(
            path, "WEBP", quality=89, method=6
        )
        variants.append({
            "w": width,
            "h": round(width / ratio),
            "src": f"/assets/images/editorial-auto/{path.name}",
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "bytes": path.stat().st_size,
        })
    return variants


def make_image(article: dict) -> dict:
    return {
        "key": f"{article['slug']}-v{VERSION}",
        "alt": article.pop("image_alt"),
        "prompt": article.pop("image_prompt"),
        "variants": make_variants(IMAGE_SOURCES[article.pop("image_source")], article["slug"]),
        "disclosure": site.CAPTION,
        "generator": "OpenAI image generation",
        "aiGenerated": True,
        "documentaryPhoto": False,
        "officialArtwork": False,
        "sensitiveContext": False,
        "weatherMap": False,
        "reenactedEvent": False,
    }


def set_published(slug: str, published: datetime) -> None:
    path = ROOT / "notizie" / f"{slug}.html"
    doc = html.fromstring(path.read_text(encoding="utf-8"))
    iso = published.isoformat(timespec="seconds")
    for node in doc.xpath('//script[@type="application/ld+json"]'):
        data = json.loads(node.text or "{}")
        if data.get("@type") == "NewsArticle":
            data["datePublished"] = iso
            data["dateModified"] = iso
            node.text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    path.write_text(
        html.tostring(doc, encoding="unicode", method="html", doctype="<!doctype html>") + "\n",
        encoding="utf-8",
    )


def append_name_phrases() -> None:
    path = ROOT / "assets/data/frasi-nome.json"
    phrases = json.loads(path.read_text(encoding="utf-8"))
    additions = [
        "Puoi capire una novità senza doverla inseguire.",
        "Proteggere i tuoi risparmi parte dalle domande giuste.",
        "La tecnologia è utile quando sai anche dove sono i limiti.",
        "Una scelta digitale può restare semplice e consapevole.",
        "Controllare i dati ti aiuta a distinguere risultati e promesse.",
        "Una casa nuova comincia sempre da un progetto ben letto.",
        "Anche le regole lontane possono cambiare le occasioni vicine.",
        "Capire una lista è più importante che fermarsi al suo nome.",
        "Le risorse contano davvero quando diventano progetti concreti.",
        "Le decisioni pubbliche meritano attenzione anche dopo il titolo.",
    ]
    for phrase in additions:
        if phrase not in phrases:
            phrases.append(phrase)
    path.write_text(json.dumps(phrases, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


ARTICLES = [
    {
        "slug": "esma-collaterali-tokenizzati-consultazione-15-gennaio-2027",
        "titolo": "ESMA apre ai collaterali tokenizzati: consultazione fino al 15 gennaio",
        "sommario": "L'autorità europea chiede al mercato quando obbligazioni e altri asset digitalizzati possano essere usati in sicurezza dalle controparti centrali.",
        "categoria": "Economia", "luogo": "Unione europea", "formato": "flash",
        "parole_chiave_titolo": ["Collaterali tokenizzati", "15 gennaio"],
        "dati_chiave": [
            {"valore": "15 gennaio 2027", "etichetta": "termine per le risposte"},
            {"valore": "1° trimestre 2027", "etichetta": "valutazione ESMA"},
            {"valore": "CCP", "etichetta": "controparti centrali coinvolte"},
        ],
        "paragrafi": [
            "ESMA ha aperto il 9 ottobre una consultazione sull'uso di collaterali tokenizzati da parte delle controparti centrali europee. Banche, infrastrutture di mercato e altri soggetti interessati possono inviare contributi entro il 15 gennaio 2027.",
            "L'analisi riguarda sia versioni digitali di attività conservate nei sistemi tradizionali, spesso definite digital twin, sia asset emessi direttamente su registri distribuiti. Sono compresi i modelli ibridi e l'interazione con denaro tokenizzato e strumenti di regolamento.",
            "Il punto centrale è verificare che trasferimento, custodia, segregazione e conversione in liquidità funzionino anche in caso di insolvenza di un partecipante. ESMA vuole inoltre capire se la tokenizzazione modifichi il profilo di rischio di garanzie già ammesse.",
            "La consultazione non autorizza automaticamente nuovi prodotti e non modifica oggi le regole per gli investitori. L'autorità esaminerà le risposte nel primo trimestre 2027 e deciderà poi se proporre interventi regolamentari o di convergenza della vigilanza.",
        ],
        "fonti": [{"url": "https://www.esma.europa.eu/press-news/esma-news/esma-seeks-evidence-use-tokenised-collateral-central-clearing", "nome": "ESMA — consultazione sui collaterali tokenizzati nelle controparti centrali."}],
        "image_source": "token_collateral",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di obbligazioni e oro trasformati in garanzie digitali davanti a un'infrastruttura finanziaria europea; scena non documentaria.",
        "image_prompt": "Collaterali tradizionali trasformati in token digitali presso una clearing house europea, illustrazione editoriale ultrarealistica senza testo.",
    },
    {
        "slug": "stablecoin-non-conformi-mica-esma-stop-servizi-tre-mesi-2026",
        "titolo": "Stablecoin non conformi a MiCA: ESMA chiede lo stop ai servizi",
        "sommario": "La vigilanza europea include trading, custodia, trasferimenti e consulenza. Le esposizioni già esistenti dovrebbero essere risolte entro tre mesi.",
        "categoria": "Economia", "luogo": "Unione europea", "formato": "flash",
        "parole_chiave_titolo": ["Stablecoin", "MiCA"],
        "dati_chiave": [
            {"valore": "3 mesi", "etichetta": "termine massimo indicato"},
            {"valore": "tutti i servizi", "etichetta": "dal trading alla custodia"},
            {"valore": "MiCA", "etichetta": "quadro europeo applicato"},
        ],
        "paragrafi": [
            "ESMA ha chiarito che i fornitori di servizi crypto autorizzati in base a MiCA dovrebbero interrompere nell'Unione europea i servizi collegati a stablecoin non conformi. L'opinione riguarda token collegati ad attività e token di moneta elettronica.",
            "L'indicazione copre piattaforme di negoziazione, cambio, esecuzione e trasmissione di ordini, collocamento, consulenza, trasferimenti, custodia e gestione di portafogli. Le autorità nazionali sono invitate a impedire anche l'introduzione di nuove esposizioni.",
            "Per le posizioni già esistenti, ESMA chiede una soluzione il prima possibile e comunque entro tre mesi dalla pubblicazione dell'8 ottobre. Nel periodo transitorio dovrebbero restare soltanto attività necessarie a liquidazione, conversione, prelievo, trasferimento o custodia.",
            "L'opinione non identifica nel comunicato un elenco universale di token vietati. Gli utenti devono quindi verificare con il proprio intermediario la conformità dello specifico asset e le modalità disponibili, evitando decisioni affrettate basate soltanto sul nome commerciale della stablecoin.",
        ],
        "fonti": [{"url": "https://www.esma.europa.eu/press-news/esma-news/esma-sets-out-supervisory-expectations-services-related-unauthorised", "nome": "ESMA — aspettative di vigilanza sulle stablecoin non conformi a MiCA."}],
        "image_source": "stablecoin_mica",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una stablecoin fermata da una barriera di conformità europea; scena non documentaria.",
        "image_prompt": "Stablecoin davanti a una barriera di conformità con bandiere UE in una sala di vigilanza, illustrazione editoriale ultrarealistica.",
    },
    {
        "slug": "samsung-wallet-usdc-coinbase-stati-uniti-ottobre-2026",
        "titolo": "Samsung Wallet integra USDC negli USA con la custodia di Coinbase",
        "sommario": "Il lancio parte nell'ultima settimana di ottobre per il mercato statunitense. USDC sarà la stablecoin in dollari predefinita nel portafoglio.",
        "categoria": "Tecnologia", "luogo": "Stati Uniti", "formato": "flash",
        "parole_chiave_titolo": ["Samsung Wallet", "USDC"],
        "dati_chiave": [
            {"valore": "ultima settimana", "etichetta": "avvio previsto a ottobre"},
            {"valore": "USA", "etichetta": "mercato iniziale"},
            {"valore": "Coinbase Prime", "etichetta": "custodia delle disponibilità"},
        ],
        "paragrafi": [
            "Coinbase e Samsung hanno annunciato l'integrazione di USDC in Samsung Wallet, con avvio previsto nell'ultima settimana di ottobre 2026 negli Stati Uniti. La stablecoin comparirà come opzione in dollari predefinita quando un utente idoneo ricarica il saldo digitale.",
            "Le disponibilità saranno custodite attraverso Coinbase Prime Vault, in collaborazione con Bastion, indicato come fornitore autorizzato di infrastruttura e custodia. L'annuncio estende la partnership già avviata tra le due società per Samsung Pay e Coinbase One.",
            "Coinbase ricorda che USDC è progettato per essere riscattabile uno a uno in dollari e supportato da contanti e titoli di Stato statunitensi a breve termine. Questa descrizione non elimina però i rischi operativi, normativi e di controparte propri degli asset digitali.",
            "Il lancio comunicato riguarda gli Stati Uniti, non automaticamente gli utenti italiani o europei. Disponibilità, funzioni di trasferimento, costi e tutele devono essere verificati nelle condizioni locali prima di usare il servizio.",
        ],
        "fonti": [{"url": "https://www.coinbase.com/en-nl/blog/coinbase-and-samsung-bring-usdc-to-samsung-wallet", "nome": "Coinbase — annuncio dell'integrazione di USDC in Samsung Wallet."}],
        "image_source": "samsung_usdc",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di uno smartphone Samsung Wallet con simbolo USDC e custodia Coinbase; scena non documentaria.",
        "image_prompt": "Smartphone Samsung Wallet con USDC e richiamo visivo a Coinbase in una scena urbana statunitense, immagine editoriale ultrarealistica.",
    },
    {
        "slug": "circle-tereina-usdc-eurc-pagamenti-sap-ottobre-2026",
        "titolo": "USDC ed EURC entrano nei flussi SAP con Circle e Tereina",
        "sommario": "La partnership punta a integrare pagamenti in stablecoin nelle applicazioni aziendali. I primi programmi pilota arriveranno nei prossimi mesi.",
        "categoria": "Economia", "luogo": "Mondo", "formato": "flash",
        "parole_chiave_titolo": ["USDC ed EURC", "SAP"],
        "dati_chiave": [
            {"valore": "2 stablecoin", "etichetta": "USDC ed EURC"},
            {"valore": "SAP Cloud ERP", "etichetta": "ambiente di partenza"},
            {"valore": "prossimi mesi", "etichetta": "avvio dei programmi pilota"},
        ],
        "paragrafi": [
            "Circle e Tereina, società sostenuta da SAP, hanno annunciato l'integrazione di USDC ed EURC nell'infrastruttura di pagamento di Tereina, partendo da SAP Cloud ERP. L'obiettivo è consentire alle imprese idonee di inviare e ricevere stablecoin senza cambiare le applicazioni usate per tesoreria e contabilità.",
            "USDC è indicata come opzione preferita per i flussi denominati in dollari, mentre EURC è destinata alle operazioni in euro. L'integrazione sarà resa disponibile ai clienti SAP attraverso SAP Pay, ma non equivale a un'attivazione immediata per tutte le aziende.",
            "Nei prossimi mesi le due società prevedono programmi con clienti, formazione per specialisti di tesoreria e pagamenti e collaborazione con altri partner dell'ecosistema. Costi, paesi ammessi e requisiti saranno definiti nelle singole implementazioni.",
            "Circle avverte che gli asset digitali restano soggetti a volatilità e a un quadro normativo in evoluzione e non sono normalmente coperti dalle garanzie sui depositi. Per le imprese italiane l'uso effettivo dovrà rispettare regole contabili, fiscali e antiriciclaggio applicabili.",
        ],
        "fonti": [{"url": "https://www.circle.com/pressroom/tereina-an-sap-backed-company-and-circle-bring-usdc-and-eurc-into-enterprise-workflows-starting-with-the-sap-ecosystem-behind-84-of-global-commerce", "nome": "Circle — partnership con Tereina per pagamenti USDC ed EURC nei flussi SAP."}],
        "image_source": "circle_sap",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di pagamenti aziendali in dollari ed euro collegati a flussi logistici globali; scena non documentaria.",
        "image_prompt": "Pagamenti USDC ed EURC integrati in flussi aziendali e logistici globali, professionisti con volti visibili, immagine ultrarealistica.",
    },
    {
        "slug": "coinbase-ia-antifrode-onramp-qwen-latenza-test-2026",
        "titolo": "Coinbase addestra un'IA antifrode: -55% di latenza nei test",
        "sommario": "Il modello Qwen3.5-9B specializzato ha superato il riferimento interno su quattro metriche. I risultati sono aziendali e riguardano il sistema Onramp.",
        "categoria": "Tecnologia", "luogo": "Mondo", "formato": "flash",
        "parole_chiave_titolo": ["IA antifrode", "Coinbase"],
        "dati_chiave": [
            {"valore": "-55%", "etichetta": "latenza mediana dichiarata"},
            {"valore": "+9,6%", "etichetta": "miglioramento F1 nel benchmark"},
            {"valore": "9 miliardi", "etichetta": "parametri del modello Qwen"},
        ],
        "paragrafi": [
            "Coinbase ha presentato un modello aperto specializzato per individuare frodi nel servizio Onramp, che permette di acquistare crypto dentro applicazioni partner. Il sistema parte da Qwen3.5-9B ed è stato addestrato sui dati proprietari dell'azienda con ricompense legate agli esiti noti delle transazioni.",
            "Nel benchmark interno il modello avrebbe superato Opus 4.5 su quattro metriche di rilevamento, con un F1 più alto del 9,6%. In produzione, la latenza mediana dichiarata è scesa da 1,515 a 0,683 secondi, pari a una riduzione del 55%.",
            "La società precisa che il modello produce una classificazione del rischio, mentre regole e software esterni trasformano il risultato in una decisione. L'IA non sostituisce quindi l'intero sistema antifrode e continua a richiedere monitoraggio, aggiornamenti e procedure di ritorno alla versione precedente.",
            "I risultati provengono da Coinbase e non da una valutazione indipendente. Sono utili come caso tecnico, ma non dimostrano che ogni frode venga bloccata né che le prestazioni siano replicabili su altre piattaforme o categorie di pagamento.",
        ],
        "fonti": [{"url": "https://www.coinbase.com/blog/landing/engineering", "nome": "Coinbase Engineering — serie tecnica sul modello antifrode per Onramp."}],
        "image_source": "coinbase_fraud",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un'analista davanti a un sistema antifrode per transazioni crypto, con volto visibile; scena non documentaria.",
        "image_prompt": "Analista di sicurezza davanti a un sistema IA che individua percorsi crypto sospetti, volto visibile, immagine editoriale ultrarealistica.",
    },
    {
        "slug": "permessi-costruire-abitazioni-crescita-secondo-trimestre-2026-istat",
        "titolo": "Permessi di costruire, abitazioni +3,8% nel secondo trimestre",
        "sommario": "Istat stima 13.246 nuove abitazioni autorizzate. Crescono anche superficie residenziale e comparto non residenziale, ma non è ancora recuperato il calo precedente.",
        "categoria": "Economia", "luogo": "Italia", "formato": "flash",
        "parole_chiave_titolo": ["Permessi di costruire", "+3,8%"],
        "dati_chiave": [
            {"valore": "+3,8%", "etichetta": "abitazioni sul trimestre precedente"},
            {"valore": "13.246", "etichetta": "abitazioni stimate"},
            {"valore": "+2,0%", "etichetta": "superficie non residenziale"},
        ],
        "paragrafi": [
            "Nel secondo trimestre 2026 il numero di abitazioni autorizzate in Italia è cresciuto del 3,8% rispetto ai tre mesi precedenti, al netto della stagionalità. La superficie utile abitabile è aumentata dell'1,4%, secondo i dati pubblicati da Istat il 9 ottobre.",
            "La stima è di 13.246 abitazioni in nuovi fabbricati residenziali e di poco meno di 1,15 milioni di metri quadrati di superficie utile. L'edilizia non residenziale supera 2,59 milioni di metri quadrati, con una crescita congiunturale del 2%.",
            "Nel confronto con il secondo trimestre 2025, il numero di abitazioni aumenta dell'8%, la superficie residenziale del 7,3% e quella non residenziale del 5,1%.",
            "Istat sottolinea però che il rimbalzo del residenziale non basta ancora a recuperare il calo registrato nel primo trimestre. I dati misurano autorizzazioni e non equivalgono automaticamente a cantieri già aperti o abitazioni consegnate.",
        ],
        "fonti": [{"url": "https://www.istat.it/comunicato-stampa/permessi-di-costruire-ii-trimestre-2026/", "nome": "Istat — permessi di costruire del secondo trimestre 2026."}],
        "image_source": "edilizia",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di nuove abitazioni e un cantiere ordinato a Firenze; scena non documentaria.",
        "image_prompt": "Nuove abitazioni e cantiere residenziale italiano con Firenze sullo sfondo, immagine editoriale ultrarealistica.",
    },
    {
        "slug": "mercati-capitali-ue-accordo-consiglio-vigilanza-esma-9-ottobre-2026",
        "titolo": "Mercati dei capitali UE, accordo del Consiglio sulla nuova vigilanza",
        "sommario": "La posizione negoziale trasferirebbe a ESMA il controllo degli operatori transfrontalieri più rilevanti. Ora serve il confronto con il Parlamento.",
        "categoria": "Economia", "luogo": "Lussemburgo", "formato": "flash",
        "parole_chiave_titolo": ["Mercati dei capitali UE", "ESMA"],
        "dati_chiave": [
            {"valore": "9 ottobre", "etichetta": "accordo del Consiglio"},
            {"valore": "ESMA", "etichetta": "vigilanza europea rafforzata"},
            {"valore": "negoziato", "etichetta": "passaggio ancora necessario"},
        ],
        "paragrafi": [
            "Il Consiglio dell'Unione europea ha concordato gli elementi principali della propria posizione sul pacchetto per integrazione e vigilanza dei mercati. L'obiettivo è ridurre gli ostacoli alle attività transfrontaliere e facilitare il finanziamento delle imprese europee.",
            "La proposta trasferirebbe a ESMA la vigilanza sulle sedi di negoziazione transfrontaliere più importanti e su alcune infrastrutture post-trading, come depositari centrali e controparti centrali di maggiore rilievo.",
            "Il pacchetto mira anche a ridurre frammentazione normativa e costi di conformità per gli operatori presenti in più paesi. Per cittadini e imprese gli effetti dipenderanno però dai testi finali e dall'applicazione concreta delle nuove regole.",
            "Quello del Consiglio è un mandato negoziale, non una legge già applicabile. Il passaggio successivo è il confronto con il Parlamento europeo; soltanto dopo un accordo e l'adozione formale saranno definite entrata in vigore e scadenze operative.",
        ],
        "fonti": [{"url": "https://www.consilium.europa.eu/en/press/press-releases/2026/10/09/savings-and-investments-union-council-agrees-key-elements-of-crucial-measures-to-deepen-eu-capital-markets/", "nome": "Consiglio dell'UE — posizione sul pacchetto per mercati e vigilanza."}],
        "image_source": "capitali_ue",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una riunione europea collegata a una rete dei mercati dei capitali; scena non documentaria.",
        "image_prompt": "Riunione istituzionale UE con rete dei mercati dei capitali e bandiere europee, immagine editoriale ultrarealistica.",
    },
    {
        "slug": "lista-fiscale-ue-panama-vietnam-rimossi-otto-giurisdizioni-2026",
        "titolo": "Lista fiscale UE, fuori Panama e Vietnam: restano otto giurisdizioni",
        "sommario": "Il Consiglio sposta i due paesi nell'allegato dedicato agli impegni in corso. La prossima revisione della lista è prevista a febbraio 2027.",
        "categoria": "Economia", "luogo": "Unione europea", "formato": "flash",
        "parole_chiave_titolo": ["Lista fiscale UE", "Panama e Vietnam"],
        "dati_chiave": [
            {"valore": "8", "etichetta": "giurisdizioni ancora elencate"},
            {"valore": "2 paesi", "etichetta": "Panama e Vietnam rimossi"},
            {"valore": "febbraio 2027", "etichetta": "prossima revisione"},
        ],
        "paragrafi": [
            "Il Consiglio dell'Unione europea ha rimosso Panama e Vietnam dalla lista delle giurisdizioni non cooperative a fini fiscali. Entrambi passano nell'allegato che registra impegni e verifiche ancora in corso.",
            "Panama era nell'elenco dal febbraio 2020 e ha riformato il regime di esenzione dei redditi di fonte estera considerato dannoso. Il paese sarà sottoposto a una nuova revisione del Global Forum dell'OCSE sullo scambio di informazioni fiscali.",
            "Il Vietnam, inserito nel febbraio 2026, ha varato riforme dopo una valutazione negativa sullo scambio di informazioni su richiesta. Anche in questo caso è prevista una nuova verifica prima di una valutazione definitiva.",
            "Restano nella lista Samoa americane, Anguilla, Guam, Palau, Russia, Turks e Caicos, Isole Vergini americane e Vanuatu. La rimozione non equivale a una certificazione generale dei sistemi fiscali: riguarda esclusivamente i criteri e gli impegni esaminati in questo processo UE.",
        ],
        "fonti": [{"url": "https://www.consilium.europa.eu/en/press/press-releases/2026/10/09/taxation-council-updates-the-eu-list-of-non-cooperative-jurisdictions-for-tax-purposes/", "nome": "Consiglio dell'UE — aggiornamento della lista fiscale del 9 ottobre 2026."}],
        "image_source": "lista_fiscale",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di un tavolo del Consiglio UE con Panama e Vietnam evidenziati su una mappa; scena non documentaria.",
        "image_prompt": "Tavolo istituzionale UE con mappa mondiale e Panama e Vietnam evidenziati in modo neutrale, immagine ultrarealistica.",
    },
    {
        "slug": "materie-prime-critiche-ue-46-progetti-strategici-21-miliardi-2026",
        "titolo": "Materie prime critiche, l'UE seleziona 46 nuovi progetti",
        "sommario": "Le iniziative coprono sedici paesi e richiedono circa 21,1 miliardi. Lo status strategico accelera permessi e accesso ai finanziatori, ma non garantisce fondi.",
        "categoria": "Economia", "luogo": "Unione europea", "formato": "flash",
        "parole_chiave_titolo": ["Materie prime critiche", "46 progetti"],
        "dati_chiave": [
            {"valore": "46", "etichetta": "nuovi progetti strategici"},
            {"valore": "16 paesi", "etichetta": "presenza nell'Unione"},
            {"valore": "21,1 miliardi", "etichetta": "capitale stimato necessario"},
        ],
        "paragrafi": [
            "La Commissione europea ha selezionato 46 nuovi progetti strategici per estrazione, lavorazione, riciclo e sostituzione delle materie prime critiche. Le iniziative sono distribuite in sedici paesi dell'Unione e portano a 106 il totale dei progetti designati nel quadro del regolamento europeo.",
            "I progetti coprono quindici delle diciassette materie considerate strategiche, tra cui rame, litio, nichel, cobalto, grafite, terre rare, magnesio e tungsteno. L'investimento complessivo necessario è stimato in circa 21,1 miliardi di euro.",
            "Lo status consente procedure autorizzative più rapide e facilita il contatto con fondi europei, banche e investitori. Non assegna però automaticamente finanziamenti pubblici e non significa che tutti i cantieri partiranno nei tempi ipotizzati.",
            "L'obiettivo del Critical Raw Materials Act è arrivare entro il 2030 a estrarre nell'UE il 10% del fabbisogno annuale, lavorarne il 40% e riciclarne il 25%. I risultati dipenderanno da autorizzazioni, sostenibilità economica, consenso territoriale e disponibilità dei capitali.",
        ],
        "fonti": [
            {"url": "https://ec.europa.eu/commission/presscorner/detail/en/ip_26_2113", "nome": "Commissione europea — selezione dei 46 nuovi progetti strategici."},
            {"url": "https://www.reuters.com/business/aerospace-defense/european-commission-picks-46-new-strategic-critical-mineral-projects-2026-10-09/", "nome": "Reuters — investimenti richiesti, paesi e limiti dello status strategico."},
        ],
        "image_source": "materie_prime",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di impianti europei per lavorazione e riciclo di materie prime critiche; scena non documentaria.",
        "image_prompt": "Impianti europei per litio, rame, terre rare e riciclo collegati in una filiera UE, immagine editoriale ultrarealistica.",
    },
    {
        "slug": "difesa-europea-norme-appalti-investimenti-via-libera-consiglio-2026",
        "titolo": "Difesa europea, via libera finale alle norme per accelerare appalti",
        "sommario": "Il Consiglio adotta il pacchetto Omnibus V: meno ritardi per autorizzazioni, acquisti e cooperazione industriale. Seguiranno pubblicazione ed entrata in vigore.",
        "categoria": "Mondo", "luogo": "Unione europea", "formato": "flash",
        "parole_chiave_titolo": ["Difesa europea", "Appalti"],
        "dati_chiave": [
            {"valore": "Omnibus V", "etichetta": "nome del pacchetto"},
            {"valore": "via libera finale", "etichetta": "decisione del Consiglio"},
            {"valore": "9 ottobre", "etichetta": "data dell'adozione"},
        ],
        "paragrafi": [
            "Il Consiglio dell'Unione europea ha dato il via libera finale al pacchetto di norme che semplifica appalti, investimenti e cooperazione per la sicurezza e la difesa. L'insieme degli atti è noto come Omnibus V.",
            "Le modifiche puntano a ridurre ritardi amministrativi nelle procedure di acquisto, nelle autorizzazioni, negli obblighi di rendicontazione e nei trasferimenti transfrontalieri di prodotti legati alla difesa.",
            "Il pacchetto comprende un regolamento sulla preparazione alla difesa e sulle condizioni per l'industria, oltre ad adeguamenti di altri atti europei. L'obiettivo dichiarato è rendere più rapida la capacità di investimento e coordinamento tra paesi e imprese.",
            "Il via libera del Consiglio conclude la fase politica, ma l'applicazione non è immediata. I testi devono essere pubblicati nella Gazzetta ufficiale dell'Unione europea e le singole disposizioni seguiranno le rispettive date di entrata in vigore.",
        ],
        "fonti": [{"url": "https://www.consilium.europa.eu/it/press/press-releases/2026/10/09/simplification-council-gives-final-green-light-to-new-laws-boosting-defence-industry-and-readiness/", "nome": "Consiglio dell'UE — adozione finale del pacchetto Omnibus V sulla difesa."}],
        "image_source": "difesa_ue",
        "image_alt": "Illustrazione editoriale IA ultrarealistica di una struttura logistica europea per la difesa con mezzi non armati e bandiere UE; scena non documentaria.",
        "image_prompt": "Struttura logistica e industriale europea per la difesa con mezzi non armati e bandiere UE, immagine neutrale ultrarealistica.",
    },
]


def main() -> None:
    append_name_phrases()
    base = datetime.now(ROME).replace(microsecond=0)
    minute_offsets = (0, 7, 16, 27, 39, 51, 64, 78, 92, 108)
    images = []
    written = []
    for article, minutes in zip(ARTICLES, minute_offsets):
        image = make_image(article)
        slug = site.write_article(article, image, VERSION)
        published = base - timedelta(minutes=minutes)
        set_published(slug, published)
        article["published"] = published.isoformat(timespec="seconds")
        image["article"] = f"/notizie/{slug}.html"
        images.append(image)
        written.append(article)

    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    new_urls = {row["article"] for row in images}
    registry["items"] = images + [row for row in registry.get("items", []) if row.get("article") not in new_urls]
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    site.sync_surfaces(written, f"/notizie/{written[0]['slug']}.html", VERSION, update_manifest=False)

    state_path = ROOT / "CURIOMONDO-RELEASE-STATE.json"
    state = json.loads(state_path.read_text(encoding="utf-8"))
    state.update({
        "site_version": VERSION,
        "currentVersion": VERSION,
        "version": str(VERSION),
        "articleCount": int(state.get("articleCount", 0)) + len(written),
        "generatedEditorialImages": int(state.get("generatedEditorialImages", 0)) + len(images),
        "last_update": f"crypto-economia-v{VERSION}",
        "date": base.date().isoformat(),
        "release_date": base.date().isoformat(),
        "updated_at": base.isoformat(timespec="seconds"),
        "status": "ready",
    })
    state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"version": VERSION, "published": base.isoformat(), "articles": [a["slug"] for a in written]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
