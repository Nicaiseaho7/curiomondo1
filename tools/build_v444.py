#!/usr/bin/env python3
"""Guide Juventus-Atalanta, Milan-Lecce e riforma elettorale."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.build_v443 import variants, publish, write_json
from automation.newsroom.site import CAPTION, sync_surfaces

VERSION = 444

JUVE = {
 "slug":"juventus-atalanta-guida-orario-tv-20-settembre-2026",
 "titolo":"Juventus-Atalanta: orario, diretta TV e numeri della sfida",
 "sommario":"La partita si gioca domenica alle 18 a Torino e sarà trasmessa da DAZN, Sky e NOW. I bianconeri arrivano dal largo successo europeo sul NEC.",
 "categoria":"Sport","luogo":"Torino","formato":"standard","stato":"UFFICIALE",
 "parole_chiave_titolo":["Juventus-Atalanta","orario"],
 "dati_chiave":[{"icona":"◆","valore":"20/9","etichetta":"domenica, calcio d’inizio alle 18"},{"icona":"●","valore":"3","etichetta":"piattaforme: DAZN, Sky e NOW"},{"icona":"↗","valore":"5ª","etichetta":"giornata della Serie A 2026-27"}],
 "paragrafi":[
  "Juventus e Atalanta si affrontano domenica 20 settembre alle 18 a Torino per la quinta giornata di Serie A. La partita sarà disponibile in diretta su DAZN e sui canali Sky abilitati, con streaming tramite NOW e Sky Go. Orari e piattaforme possono richiedere un abbonamento attivo.",
  "La Juventus arriva dalla vittoria per 5-0 contro il NEC nella prima giornata di Europa League. Il risultato europeo ha dato continuità offensiva, ma riduce il tempo di recupero prima del campionato. La gestione delle energie sarà quindi uno dei dati da osservare nelle scelte iniziali e nei cambi.",
  "L’Atalanta si presenta dopo un avvio di campionato irregolare e cerca punti in una trasferta tradizionalmente impegnativa. La squadra bergamasca ha avuto una settimana più lineare per preparare la gara. Questo vantaggio di calendario non garantisce il risultato, ma può incidere su intensità e pressione.",
  "Il confronto tattico oppone due squadre che cercano spesso di recuperare il pallone in avanti. La Juventus dovrà evitare perdite centrali durante la costruzione; l’Atalanta dovrà limitare gli spazi alle spalle della prima pressione. Le transizioni possono diventare decisive più del possesso complessivo.",
  "I precedenti segnalati dal club bianconero aiutano a leggere la tradizione della sfida, ma non sostituiscono la forma attuale. Per il pubblico, il dato pratico è semplice: calcio d’inizio alle 18, collegamento sulle piattaforme autorizzate e formazioni ufficiali disponibili circa un’ora prima della gara.",
  "Chi segue la partita in streaming dovrebbe verificare in anticipo aggiornamento dell’app, dispositivo registrato e qualità della connessione. Le probabili formazioni pubblicate alla vigilia restano indicazioni giornalistiche: soltanto le distinte diffuse dalle squadre e dalla Lega confermano titolari e panchine.",
  "La gara chiude il pomeriggio domenicale prima del posticipo Milan-Lecce. Per la Juventus è il passaggio dalla competizione europea al campionato; per l’Atalanta è un test sulla capacità di reagire fuori casa. Il risultato inciderà sulla classifica dopo le prime cinque giornate."],
 "fonti":[
  {"url":"https://www.juventus.com/it/news/articoli/serie-a-juventus-atalanta-i-precedenti-della-sfida","descrizione":"Juventus — precedenti ufficiali della sfida."},
  {"url":"https://www.legaseriea.it/","descrizione":"Lega Serie A — calendario ufficiale della quinta giornata."},
  {"url":"https://www.dazn.com/it-IT/competition/Competition:1r097lpxe0xn03ihb7wi98kao","descrizione":"DAZN — programmazione della Serie A in Italia."},
  {"url":"https://sport.sky.it/calcio/serie-a","descrizione":"Sky Sport — programmazione e copertura della Serie A."}],
 "correlati":[{"url":"/notizie/serie-a-quinta-giornata-orari-tv-monza-sassuolo-roma-inter-18-settembre-2026.html","titolo":"Serie A, calendario e dirette della quinta giornata"}]
}

MILAN = {
 "slug":"milan-lecce-guida-orario-tv-san-siro-20-settembre-2026",
 "titolo":"Milan-Lecce: orario, diretta TV e precedenti del posticipo",
 "sommario":"Il match chiude domenica la quinta giornata alle 20.45 a San Siro. Diretta esclusiva su DAZN; il Milan torna in casa dopo due trasferte.",
 "categoria":"Sport","luogo":"Milano","formato":"standard","stato":"CONFERMATA DA PIÙ FONTI",
 "parole_chiave_titolo":["Milan-Lecce","streaming"],
 "dati_chiave":[{"icona":"◆","valore":"20:45","etichetta":"calcio d’inizio domenica a San Siro"},{"icona":"●","valore":"49°","etichetta":"precedente tra le squadre in campionato"},{"icona":"↗","valore":"DAZN","etichetta":"diretta esclusiva in Italia"}],
 "paragrafi":[
  "Milan-Lecce si gioca domenica 20 settembre alle 20.45 allo stadio San Siro. Il posticipo della quinta giornata sarà trasmesso in diretta esclusiva da DAZN, tramite app e dispositivi compatibili. Non è prevista la diretta integrale sui normali canali Sky Sport.",
  "Per il Milan è il ritorno davanti al proprio pubblico dopo due gare esterne. Il club ha indicato l’appuntamento come quarantanovesimo confronto di campionato tra le squadre. Il bilancio storico comprende 31 vittorie rossonere, 15 pareggi e due successi del Lecce.",
  "I precedenti descrivono la distanza accumulata nel tempo, non il valore della singola partita. Il Lecce può ridurre gli spazi con un blocco compatto e cercare uscite rapide; il Milan dovrà trasformare il possesso in occasioni senza scoprirsi quando perde il pallone.",
  "La posizione di chi crea gioco tra le linee sarà centrale. Se il Lecce difende stretto, il Milan dovrà allargare il campo e attaccare l’area con più uomini. Se i salentini superano la prima pressione, possono trovare spazio contro una difesa in movimento.",
  "Le probabili formazioni della vigilia possono cambiare per condizioni fisiche, rotazioni e scelte tecniche. Le uniche indicazioni definitive arriveranno con le distinte ufficiali, normalmente diffuse circa un’ora prima del calcio d’inizio. Conviene quindi controllare i canali dei club nel tardo pomeriggio.",
  "Per guardare la partita servono un abbonamento DAZN attivo e un dispositivo collegato. Chi usa una smart TV dovrebbe aprire l’app prima del match e verificare eventuali aggiornamenti. Smartphone, tablet, computer e console compatibili offrono alternative in caso di problemi sul televisore.",
  "Milan-Lecce conclude il programma della domenica dopo Juventus-Atalanta. Per i rossoneri è un passaggio importante per consolidare la posizione nelle prime giornate; per il Lecce è un test di organizzazione contro una squadra costruita per occupare la parte alta della classifica e controllare il gioco senza rinunciare alle ripartenze."],
 "fonti":[
  {"url":"https://www.acmilan.com/it/news/articoli/ticketing/2026-08-17/milan-lecce-san-siro-vi-aspetta","descrizione":"AC Milan — data, orario e precedenti ufficiali."},
  {"url":"https://www.legaseriea.it/","descrizione":"Lega Serie A — calendario ufficiale della quinta giornata."},
  {"url":"https://www.dazn.com/it-IT/competition/Competition:1r097lpxe0xn03ihb7wi98kao","descrizione":"DAZN — programmazione ufficiale della Serie A."},
  {"url":"https://www.eurosport.it/calcio/serie-a/2026-2027/milan-lecce-probabili-formazioni-statistiche-quando-e-dove-vederla_sto23338082/story.shtml","descrizione":"Eurosport — conferma indipendente di orario e trasmissione."}],
 "correlati":[{"url":"/notizie/serie-a-quinta-giornata-orari-tv-monza-sassuolo-roma-inter-18-settembre-2026.html","titolo":"Serie A, calendario e dirette della quinta giornata"}]
}

POLITICA = {
 "slug":"riforma-legge-elettorale-42-percento-camera-19-settembre-2026",
 "titolo":"Legge elettorale: premio al 42%, il testo torna alla Camera",
 "sommario":"Il Senato ha modificato la riforma e l’ha approvata con 113 voti favorevoli. Per diventare legge serve ora un nuovo via libera di Montecitorio.",
 "categoria":"Politica","luogo":"Roma","formato":"standard","stato":"CONFERMATA DA PIÙ FONTI",
 "parole_chiave_titolo":["Legge elettorale","42%"],
 "dati_chiave":[{"icona":"◆","valore":"42%","etichetta":"soglia prevista per il premio"},{"icona":"●","valore":"70+35","etichetta":"seggi aggiuntivi a Camera e Senato"},{"icona":"↗","valore":"113-71","etichetta":"esito del voto a Palazzo Madama"}],
 "paragrafi":[
  "La riforma della legge elettorale torna alla Camera dopo l’approvazione con modifiche da parte del Senato. Palazzo Madama ha votato il testo con 113 sì e 71 no. Il provvedimento non è ancora legge: Montecitorio deve approvare la stessa versione senza ulteriori cambiamenti.",
  "Il nuovo sistema elimina i collegi uninominali e imposta l’elezione su base proporzionale. La lista o coalizione che raggiunge almeno il 42 per cento dei voti ottiene un premio di governabilità: 70 seggi aggiuntivi alla Camera e 35 al Senato, entro i limiti massimi previsti.",
  "Il tetto indicato è di 220 deputati e 113 senatori per la forza o coalizione beneficiaria. Se nessuno raggiunge la soglia, il premio non scatta e i seggi vengono distribuiti proporzionalmente. Il meccanismo cerca quindi di conciliare rappresentanza e possibilità di una maggioranza parlamentare stabile.",
  "Tra le modifiche introdotte al Senato figura il sistema delle preferenze. Le coalizioni devono inoltre indicare prima del voto il candidato alla Presidenza del Consiglio. Questa indicazione ha valore politico, mentre la nomina del presidente del Consiglio resta costituzionalmente affidata al Presidente della Repubblica.",
  "Il passaggio alla Camera è necessario perché ogni modifica approvata da un ramo del Parlamento deve essere accettata dall’altro nello stesso testo. Se Montecitorio introducesse nuove correzioni, il provvedimento tornerebbe ancora al Senato. Soltanto l’approvazione identica conclude l’iter parlamentare.",
  "La maggioranza presenta il premio come strumento di stabilità. Le opposizioni contestano soglia, tempi e possibile vantaggio per le coalizioni più forti. Queste valutazioni restano posizioni politiche distinte dai dati normativi: la verifica decisiva riguarda il testo approvato e gli atti parlamentari.",
  "Per gli elettori non cambia ancora nulla. Fino all’approvazione definitiva, alla promulgazione e all’entrata in vigore resta applicabile la legge esistente. I prossimi passaggi da seguire sono la calendarizzazione alla Camera, eventuali emendamenti e il voto finale sul testo trasmesso dal Senato."],
 "fonti":[
  {"url":"https://www.senato.it/lavori/assemblea/comunicato-di-seduta?num=453","descrizione":"Senato della Repubblica — comunicato ufficiale con contenuto e soglia del premio."},
  {"url":"https://temi.camera.it/leg19/provvedimento/disposizioni-in-materia-di-elezioni-della-camera-dei-deputati-e-del-senato-della-repubblica.html","descrizione":"Camera dei deputati — dossier e iter della riforma elettorale."},
  {"url":"https://www.reuters.com/world/italian-senate-clears-melonis-electoral-reform-amid-opposition-resistance-2026-09-15/","descrizione":"Reuters — conferma indipendente del voto e del ritorno alla Camera."},
  {"url":"https://www.rainews.it/maratona/2026/09/legge-elettorale-senato-camera-opposizione-maggioranza-elezioni-coalizioni-costituzionalita-2a1018f4-0cc2-468e-a8fa-b681fc6dc1fe.html","descrizione":"RaiNews — dettagli su preferenze, premio e limiti di seggi."}],
 "correlati":[{"url":"/notizie/bollo-auto-governo-esenzione-14-5-milioni-veicoli-16-settembre-2026.html","titolo":"Bollo auto, il testo ufficiale dell’esenzione 2027"}]
}

def main():
    articles=[JUVE,MILAN,POLITICA]
    files=["juventus-atalanta-v444.png","milan-lecce-v444.png","legge-elettorale-v444.png"]
    alts=["Scena editoriale contestuale generata con IA: calciatori in bianconero e nerazzurro si preparano a Juventus-Atalanta; non è una fotografia documentaria.","Scena editoriale contestuale generata con IA: calciatori in rossonero e giallorosso si preparano a Milan-Lecce; non è una fotografia documentaria.","Scena editoriale contestuale generata con IA: documenti parlamentari nell’aula italiana durante l’iter della legge elettorale; non è una fotografia documentaria."]
    prompts=["Juventus-Atalanta, riscaldamento prepartita a Torino, fotografia editoriale senza testo.","Milan-Lecce, preparazione al posticipo a San Siro, fotografia editoriale senza testo.","Iter della riforma elettorale nel Parlamento italiano, fotografia editoriale istituzionale senza testo."]
    stamps=["2026-09-19T10:10:00+02:00","2026-09-19T10:12:00+02:00","2026-09-19T10:14:00+02:00"]
    slugs=[]
    for article,filename,alt,prompt,stamp in zip(articles,files,alts,prompts,stamps):
        image={"key":f"{article['slug']}-v{VERSION}","aiGenerated":True,"documentaryPhoto":False,"generator":"ChatGPT/OpenAI image generation","variants":variants(ROOT/"generated_images"/filename,f"{article['slug']}-v{VERSION}"),"alt":alt,"disclosure":CAPTION,"sensitiveContext":False,"reenactedEvent":False,"prompt":prompt}
        slugs.append(publish(article,image,stamp))
    sync_surfaces(articles,"",VERSION)
    mp=ROOT/"curiomondo-site-manifest.json"; manifest=json.loads(mp.read_text(encoding="utf-8")); manifest["site"].update({"current_site_version":VERSION,"site_version":VERSION}); manifest.update({"site_version":VERSION,"version":f"v{VERSION}","release_version":f"v{VERSION}"}); manifest["last_release"]={"version":VERSION,"date":"2026-09-19","type":"content-release","news_added":slugs,"news_updated":[],"change":"Guide Juventus-Atalanta e Milan-Lecce, riforma elettorale","image_policy_applied":"new-openai-contextual-editorial-images"}; write_json(mp,manifest)
    for name in ("RELEASE-STATE.json","CURIOMONDO-RELEASE-STATE.json"):
        p=ROOT/name
        if p.exists():
            s=json.loads(p.read_text(encoding="utf-8")); s.update({"currentVersion":VERSION,"site_version":VERSION,"version":str(VERSION),"date":"2026-09-19","release_date":"2026-09-19","articleCount":int(s.get("articleCount",0))+3,"generatedEditorialImages":int(s.get("generatedEditorialImages",0))+3,"last_update":"news-v444"}); write_json(p,s)
    write_json(ROOT/"automation/logs/editoriale-20260919T101400-Europe-Rome.json",{"run_at":"2026-09-19T10:14:00+02:00","processed":[{"title":a["titolo"],"decision":"publish","public_url":f"https://curiomondo.it/notizie/{s}.html"} for a,s in zip(articles,slugs)]})

if __name__=="__main__": main()
