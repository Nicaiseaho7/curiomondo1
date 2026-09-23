#!/usr/bin/env python3
"""Pubblica le notizie richieste dall'editore il 23 settembre 2026."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from automation.newsroom import site

GENERATED = ROOT.parent / "generated_images"
VERSION = 522

STORIES = [
    dict(slug="inail-2025-1189-morti-lavoratori-malattie-professionali", titolo="INAIL, nel 2025 denunciate 1.189 morti tra i lavoratori", sommario="Le denunce mortali complessive scendono a 1.198. Le malattie professionali salgono a 98.312, l’11,3% in più del 2024.", categoria="Lavoro", luogo="Roma", formato="flash", image="exec-f0f42712-cfe9-4eb5-ad29-61fc3a77c3ef.png", alt="Illustrazione editoriale IA della sede INAIL con casco da lavoro e documenti statistici; scena non documentaria.", stats=[("1.189", "denunce mortali tra lavoratori"), ("9", "denunce mortali tra studenti"), ("+11,3%", "malattie professionali")], priority=96, primary="italia", body=[
        "Nel 2025 l’INAIL ha ricevuto 1.198 denunce di infortunio con esito mortale: 1.189 riguardano lavoratori e nove studenti. Il totale è inferiore del 3,3% alle 1.239 denunce del 2024. I numeri descrivono segnalazioni all’Istituto e non coincidono automaticamente con casi già riconosciuti o indennizzati.",
        "Le denunce complessive di infortunio sono state circa 600 mila, in aumento dell’1,2% su base annua. Quelle relative ai lavoratori hanno superato quota 519 mila, mentre per gli studenti sono state circa 81 mila. La diminuzione delle segnalazioni mortali si accompagna quindi a una crescita del totale degli eventi denunciati.",
        "La relazione annuale registra 98.312 denunce di malattia professionale, contro 88.338 nel 2024: l’incremento è dell’11,3%. L’INAIL collega il dato anche a una maggiore emersione delle patologie legate al lavoro; l’aumento delle denunce non misura da solo quanti casi saranno riconosciuti al termine dell’istruttoria.",
        "Il documento è stato presentato il 22 settembre alla Camera dei deputati. Il confronto annuale permette di distinguere tre piani diversi: frequenza degli infortuni denunciati, gravità degli eventi mortali e crescita delle segnalazioni di malattia professionale."
    ], sources=[("https://www.inail.it/portale/it/inail-comunica/news/notizia.2026.09.la-relazione-annuale-inail-presentata-alla-camera-nel-2025-in-calo-gli-infortuni-mortali-denunciati-aumenta-l-emersione-delle-malattie-professionali.html", "INAIL — relazione annuale 2025, denunce di infortunio e malattie professionali, 22 settembre 2026."), ("https://www.rainews.it/video/2026/09/inail-rapporto-2025-muoiono-3-persone-al-giorno-sul-lavoro-aumentano-denunce-incidenti-88a0f653-d2e1-4474-9d92-f233e410ea6b.html", "RaiNews — riscontro indipendente sui principali dati della relazione INAIL.")]),
    dict(slug="incendiamoeba-cascadensis-record-eucarioti-63-gradi", titolo="Un’ameba si riproduce a 63 °C: nuovo record tra gli eucarioti", sommario="Incendiamoeba cascadensis è stata isolata nelle sorgenti calde della California. Lo studio sostenuto dalla NASA è pubblicato su Cell.", categoria="Scienza", luogo="California", formato="flash", image="exec-4dde547d-6ca5-40f4-8355-1163effcc2bf.png", alt="Illustrazione editoriale IA di Incendiamoeba cascadensis osservata in laboratorio vicino a una sorgente calda; scena non documentaria.", stats=[("63 °C", "divisione cellulare osservata"), ("64 °C", "attività ancora rilevata"), ("Cell", "rivista dello studio")], priority=94, primary="scienza", body=[
        "Una nuova ameba isolata nelle sorgenti calde del Lassen Volcanic National Park, in California, riesce a dividersi a 63 °C. Il risultato stabilisce il limite più alto finora documentato per la riproduzione di un eucariote, cioè un organismo le cui cellule possiedono un nucleo.",
        "I ricercatori hanno chiamato la specie Incendiamoeba cascadensis. In laboratorio l’organismo è rimasto attivo fino a 64 °C, muovendosi e cercando cibo, ma la divisione cellulare si è fermata oltre i 63 °C. Il record riguarda quindi la riproduzione, non una sopravvivenza indefinita a temperature superiori.",
        "Lo studio, sostenuto dalla NASA e pubblicato su Cell, ha analizzato anche il genoma dell’ameba. Il gruppo ha osservato un arricchimento di geni collegati alla stabilità del genoma, al controllo delle proteine e alla percezione dell’ambiente esterno, elementi che possono contribuire alla tolleranza termica.",
        "Batteri e archei possono vivere a temperature ancora più elevate, ma appartengono a gruppi cellulari differenti. Il risultato amplia il confine sperimentale conosciuto per la vita eucariotica senza dimostrare che tutti gli organismi complessi possano adattarsi allo stesso modo."
    ], sources=[("https://ciencia.nasa.gov/ciencias-terrestres/investigacion-financiada-por-la-nasa-descubre-vida-compleja-que-desafia-un-calor-record/", "NASA Science — presentazione della ricerca e temperature osservate, 22 settembre 2026."), ("https://pubmed.ncbi.nlm.nih.gov/41394606/", "PubMed/Cell — studio sulla nuova soglia termica degli eucarioti."), ("https://www.reuters.com/business/environment/tenacious-hot-springs-amoeba-sets-heat-tolerance-record-2026-09-22/", "Reuters — conferma indipendente e contesto scientifico.")]),
    dict(slug="nasa-spacex-crew-13-lancio-1-ottobre-2026", titolo="NASA e SpaceX preparano Crew-13: lancio previsto dal 1° ottobre", sommario="La prima opportunità è fissata alle 17:10 italiane da Cape Canaveral, subordinatamente ai controlli finali di preparazione.", categoria="Scienza", luogo="Cape Canaveral", formato="flash", image="exec-9cbfdec5-6f19-44b6-82bb-b085faecee30.png", alt="Illustrazione editoriale IA di Falcon 9 e Crew Dragon sulla rampa a Cape Canaveral durante i preparativi di Crew-13; scena non documentaria.", stats=[("1 ottobre", "prima opportunità di lancio"), ("17:10", "orario italiano previsto"), ("4", "componenti dell’equipaggio")], priority=90, primary="scienza", body=[
        "NASA e SpaceX puntano a giovedì 1° ottobre per il lancio della missione Crew-13 verso la Stazione spaziale internazionale. La prima opportunità è indicata alle 15:10 UTC, le 17:10 in Italia, da Cape Canaveral. La data resta subordinata alle verifiche di preparazione e al coordinamento delle operazioni in orbita.",
        "La missione utilizzerà una capsula Crew Dragon su un Falcon 9. L’equipaggio annunciato comprende la comandante NASA Jessica Watkins, il pilota Luke Delaney, l’astronauta canadese Joshua Kutryk e il cosmonauta Roscosmos Sergey Teteryatnikov. Sono previsti una permanenza di lunga durata e attività scientifiche a bordo della stazione.",
        "La formula “prima opportunità” è importante: nei lanci spaziali la finestra può cambiare per meteo, controlli tecnici o esigenze della ISS. NASA e SpaceX avevano spostato la missione all’inizio di ottobre per completare le attività precedenti al decollo e le revisioni di prontezza.",
        "Il prossimo passaggio operativo sarà la conferma dopo i controlli finali. Orario e giorno vanno quindi considerati programmati, non definitivi, fino al via libera delle squadre di missione."
    ], sources=[("https://www.nasa.gov/blogs/spacestation/2026/08/29/nasa-spacex-adjust-crew-13-launch-date/", "NASA — aggiornamento ufficiale sulla finestra di lancio di Crew-13."), ("https://nextspaceflight.com/launches/details/6973/", "Next Spaceflight — equipaggio, data e profilo della missione."), ("https://www.rocketlaunch.live/launch/crew-13", "RocketLaunch.Live — riscontro sull’orario della prima opportunità.")]),
    dict(slug="giornate-europee-patrimonio-26-27-settembre-2026", titolo="Giornate del Patrimonio, aperture speciali il 26 e 27 settembre", sommario="Musei e luoghi della cultura organizzano visite ed eventi. Sabato sera, nei musei statali aderenti, ingresso simbolico a un euro.", categoria="Cultura", luogo="Italia", formato="flash", image="exec-08dd5ebb-5c62-4758-a193-86c0c1e16348.png", alt="Illustrazione editoriale IA di un museo statale italiano durante un’apertura serale delle Giornate Europee del Patrimonio; scena non documentaria.", stats=[("26–27 set.", "giornate dell’iniziativa"), ("1 €", "ingresso serale simbolico"), ("2 giorni", "eventi in tutta Italia")], priority=86, primary="cultura", body=[
        "Sabato 26 e domenica 27 settembre tornano in Italia le Giornate Europee del Patrimonio. Musei, parchi archeologici, archivi e altri luoghi della cultura propongono aperture straordinarie, visite guidate e iniziative organizzate dagli istituti aderenti.",
        "La sera di sabato 26 i musei statali partecipanti prevedono aperture speciali con ingresso al prezzo simbolico di un euro, escluse le gratuità stabilite dalla legge. La tariffa non vale automaticamente in ogni luogo: orari, prenotazioni e disponibilità dipendono dal programma del singolo istituto.",
        "L’edizione 2026 è coordinata in Italia dal Ministero della Cultura nell’ambito dell’iniziativa promossa dal Consiglio d’Europa e dalla Commissione europea. Partecipano anche luoghi pubblici e privati, enti e associazioni del territorio con eventi dedicati alla conoscenza e alla tutela del patrimonio.",
        "Prima della visita è utile controllare la scheda dell’evento prescelto sul portale ministeriale. Alcune aperture prevedono prenotazione obbligatoria, capienza limitata o fasce orarie diverse dal normale servizio."
    ], sources=[("https://cultura.gov.it/giornate-europee-del-patrimonio-2026", "Ministero della Cultura — programma nazionale delle Giornate Europee del Patrimonio 2026."), ("https://musei.cultura.gov.it/notizie/notifiche/tornano-le-giornate-europee-del-patrimonio-gep-2026", "Direzione generale Musei — date, aperture serali e ingresso a un euro.")]),
    dict(slug="pio-sebastiano-esposito-insieme-nazionale-fratelli-italia", titolo="Pio e Sebastiano Esposito insieme in Nazionale", sommario="I due attaccanti raccontano il raduno condiviso. Potrebbero diventare la quarta coppia di fratelli schierata insieme nell’Italia maggiore.", categoria="Sport", luogo="Coverciano", formato="flash", image="exec-99174516-2639-4611-9036-3d158159772f.png", alt="Illustrazione editoriale IA contestuale di Francesco Pio e Sebastiano Esposito al centro tecnico di Coverciano; scena non documentaria.", stats=[("2", "fratelli convocati insieme"), ("4ª coppia", "possibile primato storico"), ("2022", "esordio azzurro di Salvatore")], priority=89, primary="sport", public=True, body=[
        "Francesco Pio e Sebastiano Esposito condividono il raduno della Nazionale maggiore a Coverciano. Nell’intervista pubblicata dalla FIGC il 22 settembre, i due attaccanti hanno descritto come un’emozione ulteriore la possibilità di vivere insieme una convocazione azzurra.",
        "Se venissero utilizzati contemporaneamente, diventerebbero la quarta coppia di fratelli schierata nella stessa partita dell’Italia. La possibilità non equivale però a una presenza già registrata: dipenderà dalle scelte del commissario tecnico nelle prossime gare.",
        "La famiglia Esposito ha già un precedente in Nazionale. Salvatore, il maggiore dei tre fratelli, ha esordito con l’Italia nel giugno 2022. Un’eventuale presenza di Sebastiano renderebbe inoltre gli Esposito la prima famiglia italiana con tre fratelli impiegati nella selezione maggiore.",
        "Pio arriva al raduno dopo due reti segnate con l’Inter in avvio di stagione; Sebastiano, passato al Sassuolo, ha realizzato il suo primo gol nel successo sulla Juventus. I dati di club forniscono il contesto tecnico della convocazione, senza anticipare le gerarchie della Nazionale."
    ], sources=[("https://www.figc.it/it/nazionali/news/pio-e-sebastiano-ecco-i-nuovi-fratelli-ditalia-stare-qui-insieme-e-unemozione-ancora-piu-bella-v1k6u7rc", "FIGC — intervista a Pio e Sebastiano Esposito, 22 settembre 2026."), ("https://sport.sky.it/calcio/nazionale/2026/09/22/italia-pio-sebastiano-esposito-nazionale-intervista", "Sky Sport — conferma indipendente sul raduno e sulle prossime gare.")]),
    dict(slug="roma-barcellona-femminile-biglietti-30-settembre-2026", titolo="Roma–Barcellona femminile, biglietti in vendita", sommario="La partita di Champions League si gioca il 30 settembre alle 18:45 al Tre Fontane. Tagliandi digitali e riduzioni per gli under 16.", categoria="Sport", luogo="Roma", formato="flash", image="exec-6697bd9d-4d73-4066-aa9b-fcc7bcf87830.png", alt="Illustrazione editoriale IA del Tre Fontane al tramonto per Roma-Barcellona femminile; scena non documentaria.", stats=[("30 settembre", "data della partita"), ("18:45", "calcio d’inizio"), ("15–20 €", "prezzi interi indicati")], priority=82, primary="sport", body=[
        "Sono in vendita i biglietti per Roma-Barcellona della UEFA Women’s Champions League, in programma mercoledì 30 settembre alle 18:45 allo stadio Tre Fontane. La società giallorossa ha aperto la vendita alle 12 del 22 settembre attraverso i propri canali ufficiali.",
        "Gli interi indicati dal club costano 15 o 20 euro a seconda del settore. Sono previste riduzioni per gli under 16. La disponibilità e le condizioni definitive vanno verificate nel sistema di biglietteria, perché alcuni settori possono esaurirsi prima della partita.",
        "Per gli acquisti online il titolo di accesso è digitale: il club segnala che non viene inviato un PDF separato. Il biglietto resta disponibile nel profilo utilizzato per l’acquisto, elemento da controllare prima di raggiungere l’impianto.",
        "La gara è il secondo turno della fase campionato. La Roma ospita il Barcellona campione in carica e quattro volte vincitore della competizione: il dato spiega il rilievo dell’appuntamento, ma non modifica le normali regole di accesso e capienza del Tre Fontane."
    ], sources=[("https://www.asroma.com/it/notizie/75970/roma-barcelona-biglietti-in-vendita-dal-22-settembre", "AS Roma — vendita, data, orario e informazioni sui biglietti."), ("https://www.fcbarcelona.com/en/football/womens-football/schedule", "FC Barcelona — calendario ufficiale della squadra femminile.")]),
    dict(slug="docufilm-80-anni-fipav-rai-2-23-settembre-2026", titolo="Il docufilm sugli 80 anni della FIPAV arriva su Rai 2", sommario="“80 Years – FIPAV Anniversary” va in onda il 23 settembre in seconda serata, dopo Italia–Finlandia agli Europei.", categoria="Film e serie TV", luogo="Televisione", formato="flash", image="exec-82731dc3-de97-4dff-83f3-ef57f5f2379f.png", alt="Illustrazione editoriale IA di uno studio televisivo dedicato al docufilm sugli 80 anni della FIPAV; scena non documentaria.", stats=[("23 settembre", "messa in onda"), ("Rai 2", "canale annunciato"), ("80 anni", "storia della Federazione")], priority=70, primary="film-serie-tv", body=[
        "“80 Years – FIPAV Anniversary”, il docufilm dedicato agli ottant’anni della Federazione Italiana Pallavolo, va in onda mercoledì 23 settembre in seconda serata su Rai 2. La trasmissione è prevista dopo il quarto di finale europeo Italia-Finlandia, con inizio della partita alle 21:05.",
        "Il film ricostruisce la storia federale attraverso immagini d’archivio e testimonianze di protagonisti della pallavolo italiana. La collocazione dopo la gara lega la programmazione televisiva all’attualità sportiva della Nazionale maschile impegnata negli Europei.",
        "La FIPAV aveva presentato il progetto fra le iniziative per l’anniversario, dopo una serie di produzioni dedicate alle Nazionali, agli arbitri, al Club Italia e al percorso olimpico della squadra femminile. Il nuovo lavoro concentra invece il racconto sull’intero arco degli ottant’anni.",
        "L’orario preciso di inizio dipende dalla durata della partita e dal palinsesto successivo. Chi vuole seguirlo deve quindi considerare la seconda serata come una finestra, non come un minuto di avvio fisso."
    ], sources=[("https://www.federvolley.it/comunicato-stampa-del-16-settembre3", "FIPAV — presentazione ufficiale del docufilm e progetto per l’ottantesimo anniversario."), ("https://www.volleynews.it/80-years-fipav-anniversary-su-rai2-il-docufilm-che-celebra-gli-80-anni-della-federazione/", "Volley News — annuncio della messa in onda su Rai 2, 22 settembre 2026.")]),
    dict(slug="meta-petal-cavo-transatlantico-petabit-francia-usa-2029", titolo="Meta annuncia Petal, cavo transatlantico da un petabit", sommario="Il sistema collegherà Francia e Stati Uniti per circa 7.000 chilometri. L’entrata in servizio è prevista nel 2029.", categoria="Tecnologia", luogo="Oceano Atlantico", formato="flash", image="exec-67b03759-514d-4211-a161-6823ea8dc86d.png", alt="Illustrazione editoriale IA di una nave posacavi e del cavo sottomarino Petal di Meta nell’Atlantico; scena non documentaria.", stats=[("1 Pbit/s", "capacità annunciata"), ("7.000 km", "lunghezza prevista"), ("2029", "entrata in servizio attesa")], priority=88, primary="tecnologia", body=[
        "Meta ha annunciato Petal, un nuovo cavo sottomarino che collegherà la Francia agli Stati Uniti lungo un percorso di circa 7.000 chilometri. L’azienda prevede una capacità di un petabit al secondo e l’entrata in servizio nel 2029. Si tratta di obiettivi progettuali, non di prestazioni già disponibili.",
        "Secondo Meta, Petal sarà il primo sistema a portare capacità dell’ordine del petabit su una distanza transoceanica. Un petabit al secondo equivale a mille terabit al secondo. L’azienda sostiene che il cavo raddoppierà la capacità dei sistemi transatlantici più avanzati senza un aumento proporzionale di energia e infrastruttura fisica.",
        "Il progetto userà fibre multicore e sarà realizzato con NEC e Sumitomo Electric Industries. Orange collaborerà per l’approdo sulla costa atlantica francese. Questi partner coprono rispettivamente sistema sottomarino, fibra e collegamento a terra.",
        "Meta ricorda che i cavi sottomarini trasportano la quasi totalità del traffico intercontinentale. La capacità nominale di Petal non corrisponderà necessariamente alla velocità percepita da un singolo utente: distribuzione, reti terrestri e congestione restano fattori distinti."
    ], sources=[("https://about.fb.com/news/2026/09/announcing-petal-meta-petabit-transoceanic-cable/", "Meta — annuncio ufficiale di Petal, capacità, rotta, partner e data prevista."), ("https://engineering.fb.com/", "Meta Engineering — contesto tecnico sulle infrastrutture di rete dell’azienda.")]),
    dict(slug="eurovolley-2026-francia-polonia-semifinali-3-0", titolo="EuroVolley, Francia e Polonia conquistano le semifinali", sommario="Romania e Germania battute 3–0 nei quarti di Sofia. La fase finale prosegue il 25 settembre a Milano.", categoria="Sport", luogo="Sofia", formato="flash", image="exec-2c001656-3bae-413a-a73e-c43991537201.png", alt="Illustrazione editoriale IA contestuale con giocatori reali di Francia e Polonia dopo i quarti di EuroVolley 2026; scena non documentaria.", stats=[("3–0", "Francia-Romania"), ("3–0", "Polonia-Germania"), ("25 settembre", "semifinali a Milano")], priority=84, primary="sport", public=True, body=[
        "Francia e Polonia sono le prime semifinaliste degli Europei maschili di pallavolo 2026. Nei quarti giocati il 22 settembre a Sofia, i francesi hanno battuto la Romania 3-0; la Polonia ha superato la Germania con lo stesso risultato.",
        "La Francia ha chiuso i set 25-16, 25-19 e 25-19. La squadra di Andrea Giani ha prodotto cinque ace senza subirne e ha terminato la partita in un’ora e 14 minuti. In semifinale affronterà la vincente di Italia-Finlandia, in programma il 23 settembre alle 21:05.",
        "La Polonia ha battuto la Germania 25-23, 25-17 e 25-17. Wilfredo León ha realizzato 17 punti e Bartłomiej Bołądź 13; l’efficienza offensiva polacca indicata dalla CEV è stata del 61%. Per i campioni in carica è la quarta semifinale europea consecutiva.",
        "Le semifinali si giocano il 25 settembre a Milano. La Polonia attende la vincente dell’altro quarto tra Belgio e Slovenia, mentre Francia e possibile avversaria italiana sono collocate nell’altra parte del tabellone."
    ], sources=[("https://www.cev.eu/articles/volleyball/first-into-the-final-four-france-and-poland-stamp-a-ticket-to-italy/", "CEV — risultati, parziali e statistiche dei quarti di finale."), ("https://www.federvolley.it/comunicato-stampa-del-20-settembre-2026", "FIPAV — calendario ufficiale della fase a eliminazione diretta."), ("https://sport.sky.it/volley/tabellone-europei-volley-maschile-2026", "Sky Sport — riscontro su tabellone e orari delle semifinali.")]),
    dict(slug="btp-green-2038-collocati-otto-miliardi-rendimento", titolo="BTP Green 2038, collocati otto miliardi di euro", sommario="Il nuovo titolo ha cedola annua del 4,40% e rendimento lordo all’emissione del 4,492%. Scadenza fissata al 30 ottobre 2038.", categoria="Economia", luogo="Roma", formato="flash", image="exec-0724be8f-c370-4e0f-9230-f52d55ba98db.png", alt="Illustrazione editoriale IA del Ministero dell’Economia con documenti finanziari verdi relativi al BTP Green; scena non documentaria.", stats=[("8 mld €", "importo collocato"), ("4,40%", "cedola annua"), ("4,492%", "rendimento lordo iniziale")], priority=91, primary="economia", body=[
        "Il Ministero dell’Economia e delle Finanze ha collocato otto miliardi di euro del nuovo BTP Green con scadenza 30 ottobre 2038. Il titolo ha godimento dal 29 settembre 2026 e una cedola annua del 4,40%, pagata in due rate semestrali.",
        "Il prezzo di emissione è stato fissato a 99,591. A quel prezzo il rendimento lordo annuo all’emissione è pari al 4,492%. Cedola e rendimento non sono la stessa misura: la prima determina i pagamenti periodici sul valore nominale, il secondo considera anche il prezzo pagato e il rimborso a scadenza.",
        "L’etichetta Green indica che le risorse raccolte sono destinate al finanziamento di spese statali con obiettivi ambientali secondo il quadro definito dal Tesoro. Non significa che il titolo sia privo di rischio di mercato: il suo prezzo può salire o scendere prima della scadenza in funzione dei tassi e della domanda.",
        "Il dato del 4,492% fotografa le condizioni del collocamento iniziale e non garantisce lo stesso rendimento a chi acquisterà successivamente sul mercato. Tassazione, commissioni e prezzo effettivo incidono sul risultato netto del singolo investitore."
    ], sources=[("https://www.borsaitaliana.it/borsa/notizie/radiocor/prima-pagina/dettaglio/tesoro-btp-green-emesso-per-8-miliardi-rendimento-fissato-al-4492-nRC_22092026_1558_480181047.html", "Borsa Italiana/Radiocor — importo, scadenza, prezzo e rendimento del collocamento."), ("https://videoembed.ansa.it/sito/notizie/economia/2026/09/22/mef-emessi-8-miliardi-di-euro-del-nuovo-btp-green_cc73f15e-1cc9-498c-a573-e3fa41f365f9.html", "ANSA — conferma indipendente delle condizioni comunicate dal MEF."), ("https://www.dt.mef.gov.it/it/debito_pubblico/titoli_di_stato/quali_sono_titoli/btp_green/", "Dipartimento del Tesoro — quadro ufficiale dei BTP Green.")]),
]


def variants(slug: str, filename: str) -> list[dict]:
    image = Image.open(GENERATED / filename).convert("RGB")
    target = 1.5
    w, h = image.size
    if w / h > target:
        nw = round(h * target); left = (w - nw) // 2; image = image.crop((left, 0, left + nw, h))
    else:
        nh = round(w / target); top = (h - nh) // 2; image = image.crop((0, top, w, top + nh))
    out = []
    directory = ROOT / "assets/images/editorial-auto"
    for width in (480, 800, 1200):
        path = directory / f"{slug}-v{VERSION}-{width}.webp"
        image.resize((width, round(width / 1.5)), Image.Resampling.LANCZOS).save(path, "WEBP", quality=86, method=6)
        out.append({"w": width, "src": f"/assets/images/editorial-auto/{path.name}", "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "bytes": path.stat().st_size})
    return out


def main() -> None:
    registry_path = ROOT / "assets/data/editorial-images-v210.json"
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    cfg_path = ROOT / "assets/data/homepage-config-v504.json"
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    for a in STORIES:
        image = {"alt": a["alt"], "variants": variants(a["slug"], a["image"]), "disclosure": site.CAPTION, "generator": "OpenAI image tool", "sensitiveContext": False, "key": f"{a['slug']}-v{VERSION}"}
        if a.get("public"):
            image["syntheticLikeness"] = "public-figure"
        article = {"slug": a["slug"], "titolo": a["titolo"], "sommario": a["sommario"], "categoria": a["categoria"], "luogo": a["luogo"], "formato": a["formato"], "paragrafi": a["body"], "fonti": [{"url": u, "descrizione": d} for u, d in a["sources"]], "dati_chiave": [{"valore": v, "etichetta": t, "icona": "◆"} for v, t in a["stats"]], "parole_chiave_titolo": []}
        site.write_article(article, image, VERSION)
        a.update(article)
        registry["items"].insert(0, {**image, "article": f"/notizie/{a['slug']}.html"})
        cfg["articles"][f"/notizie/{a['slug']}.html"] = {"firstPublishedAt": a["published"], "homepagePriority": a["priority"], "primaryCategory": a["primary"]}
    registry["version"] = VERSION
    registry_path.write_text(json.dumps(registry, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cfg["version"] = VERSION
    cfg_path.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    site.sync_surfaces(STORIES, "", VERSION)
    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["site_version"] = VERSION; manifest["version"] = manifest["release_version"] = f"v{VERSION}"
    manifest["last_release"] = {"version": VERSION, "date": "2026-09-23", "type": "editorial-news-cycle", "news_added": [a["slug"] for a in STORIES], "news_updated": [], "change": "Dieci notizie verificate richieste dall’editore; evitato duplicato Under 21 già presente"}
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for name in ("CURIOMONDO-RELEASE-STATE.json", "RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state.update(site_version=VERSION, version=str(VERSION), currentVersion=VERSION, release_date="2026-09-23", last_update="notizie-richieste-23-settembre-v522")
        if "articleCount" in state: state["articleCount"] += len(STORIES)
        if "generatedEditorialImages" in state: state["generatedEditorialImages"] += len(STORIES)
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"added": [a["slug"] for a in STORIES]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
