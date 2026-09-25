#!/usr/bin/env python3
"""Pubblica la Domanda del giorno canonica del 25 settembre 2026."""
from __future__ import annotations

from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import json

from daily_question_auto import (
    render_book_page,
    render_question_page,
    update_archive,
    update_feed,
    update_home,
    update_search,
    update_sitemap,
)


ROOT = Path(__file__).resolve().parents[1]
ROME = ZoneInfo("Europe/Rome")
VERSION = 557
DATE = "2026-09-25"
DATE_LABEL = "25 settembre 2026"
QUESTION_NUMBER = 1009
QUESTION = "Siamo stanchi del lavoro o stanchi di una vita che il lavoro sta sostituendo?"
SLUG = "siamo-stanchi-del-lavoro-o-stanchi-di-una-vita-che-il-lavoro-sta-sostituendo"
QURL = f"/domanda-del-giorno/{SLUG}/"
BOOK_URL = f"/biblioteca/vita-relazioni/domande-per-conoscersi/{SLUG}/"


PACKAGE = {
    "excerpt": "Una riflessione per distinguere la fatica del lavoro dalla stanchezza di una vita in cui riposo, relazioni e desideri ricevono soltanto il tempo avanzato.",
    "answer_paragraphs": [
        "A volte diciamo di essere stanchi del lavoro, ma non è il lavoro in sé a consumarci. Ci stanca il fatto che occupi il centro della giornata e lasci a tutto il resto soltanto i bordi: pasti affrettati, relazioni rimandate, sonno insufficiente, pensieri che continuano anche dopo aver chiuso il computer o lasciato il turno. La fatica allora non finisce con il riposo, perché riguarda la forma intera della vita.",
        "Esiste però anche una stanchezza propriamente lavorativa. Può nascere da carichi eccessivi, scarsa autonomia, turni imprevedibili, conflitti, richieste contraddittorie o mancanza di riconoscimento. In questi casi non basta organizzarsi meglio nel tempo libero. Il problema è nelle condizioni concrete e ha bisogno di limiti, confronto, tutele o cambiamenti reali, non di una colpa personale da amministrare in silenzio.",
        "La distinzione si vede osservando ciò che accade quando arriva una pausa. Se dopo alcuni giorni senza lavoro torna curiosità, energia e desiderio di incontrare gli altri, il carico professionale probabilmente pesa molto. Se invece il tempo libero appare vuoto, difficile da abitare o subito riempito da nuove prestazioni, forse il lavoro ha sostituito parti della vita che non sappiamo più come raggiungere.",
        "Il lavoro offre struttura, identità, competenza e appartenenza. Per questo può allargarsi senza incontrare resistenza: non prende soltanto ore, ma dà risposte alla domanda su chi siamo. Il rischio non è impegnarsi molto. È non avere più luoghi in cui sentirsi vivi senza essere produttivi, utili o misurabili. Quando ogni valore personale dipende dal rendimento, anche il riposo sembra un’interruzione da giustificare.",
        "Non tutti possono ridurre l’orario, cambiare impiego o rinunciare a uno stipendio. La domanda non deve diventare un privilegio travestito da consiglio. Può però aiutare a riconoscere quale parte della stanchezza richiede protezione immediata e quale segnala una vita diventata troppo stretta. A volte il primo gesto è piccolo: difendere una sera, chiedere una turnazione più chiara, togliere le notifiche, tornare a un legame trascurato.",
        "Forse siamo stanchi del lavoro quando il corpo chiede recupero; siamo stanchi di una vita sostituita dal lavoro quando, anche riposando, non ricordiamo più che cosa vorremmo fare del tempo liberato. Le due cose possono convivere. Capirlo non risolve tutto, ma cambia la domanda: non soltanto come recuperare energie per lavorare ancora, bensì quale parte della vita merita di tornare a esistere prima che avanzi del tempo.",
    ],
    "book_title": "Quando il lavoro prende il posto della vita",
    "book_deck": "Un percorso tra fatica, identità, tempo, denaro, relazioni e confini per capire che cosa ci sta esaurendo e quale spazio concreto possiamo restituire alla vita.",
    "book_pages": [
        {
            "title": "Due stanchezze che si assomigliano",
            "paragraphs": [
                "La sera può arrivare con la stessa pesantezza in situazioni molto diverse. In una, il corpo e la mente hanno sostenuto un carico intenso e chiedono riposo. Nell’altra, la giornata non è stata necessariamente eccezionale, ma lascia la sensazione di non aver vissuto nulla che appartenesse davvero a noi. Entrambe si chiamano stanchezza, eppure indicano bisogni differenti: recuperare energie oppure recuperare una direzione.",
                "La fatica da carico tende a migliorare quando il carico diminuisce. Dormire, rallentare, distribuire meglio i compiti o attraversare un periodo meno esigente restituisce capacità. La fatica da sostituzione è più ambigua. Anche una domenica libera può diventare inquieta, perché manca l’abitudine a scegliere che cosa fare senza una richiesta esterna. Il tempo c’è, ma non sembra disponibile interiormente.",
                "Le due forme possono sovrapporsi. Un lavoro pesante riduce le energie necessarie per coltivare relazioni e interessi; la perdita di questi spazi rende il lavoro ancora più centrale. Si crea un circuito: siamo troppo stanchi per vivere fuori dal lavoro e, avendo sempre meno vita fuori, chiediamo al lavoro identità, riconoscimento e senso. Ciò che ci consuma diventa anche ciò da cui dipendiamo.",
                "Per distinguere non serve un’etichetta perfetta. È più utile osservare variazioni concrete. Come cambia il sonno nei giorni liberi? Che cosa accade all’umore quando una consegna viene rinviata? Esiste ancora qualcosa che desideriamo fare, oppure pensiamo soltanto a ciò da cui vorremmo fuggire? Le risposte non formulano una diagnosi, ma mostrano dove la fatica reagisce al riposo e dove chiede una trasformazione più ampia.",
                "Questa distinzione evita due errori opposti. Il primo è trattare condizioni di lavoro dannose come un problema di organizzazione personale. Il secondo è attribuire all’impiego ogni vuoto, ignorando quanto abbiamo smesso di scegliere anche quando potremmo farlo. Guardare entrambe le possibilità permette di cercare responsabilità reali senza colpevolizzarsi e senza aspettare che un solo cambiamento risolva automaticamente tutta la vita.",
            ],
        },
        {
            "title": "Quando la giornata non finisce con il turno",
            "paragraphs": [
                "Il lavoro contemporaneo può continuare oltre il luogo e l’orario dichiarati. Una notifica apre un compito, una conversazione resta sospesa, un problema viene ripassato mentalmente durante la cena. Anche senza lavorare in modo visibile, rimaniamo disponibili. Questa disponibilità diffusa sottrae al riposo la sua qualità principale: non dover essere pronti a rispondere. Il tempo libero esiste sul calendario, ma resta occupato dall’attesa.",
                "Non tutti i lavori usano uno smartphone. Un turno fisico può proseguire nel dolore muscolare, nel sonno alterato o nella necessità di organizzare trasporti e cura familiare attorno a orari irregolari. Anche qui il confine tra lavoro e vita non coincide con il cartellino. Il costo reale comprende preparazione, spostamenti, recupero e conseguenze sul corpo. Ignorare queste ore rende la giornata apparentemente più libera di quanto sia.",
                "La mente fatica a chiudere quando i compiti restano indefiniti. Una richiesta precisa può essere completata; un ruolo in cui tutto è urgente mantiene un allarme continuo. Scrivere che cosa resta da fare e quando verrà ripreso può ridurre la necessità di ricordarlo senza sosta. Non risolve carichi impossibili, ma crea una soglia: il problema è registrato e non deve essere tenuto vivo per paura di dimenticarlo.",
                "Anche le emozioni attraversano il confine. Un conflitto con un collega, una decisione poco chiara o la paura di sbagliare possono occupare più spazio del compito stesso. Pretendere di non pensarci è spesso inutile. Può aiutare nominare l’episodio, distinguere ciò che dipende da noi e fissare il prossimo passo praticabile. Il resto non scompare, ma smette di presentarsi come un’urgenza senza forma.",
                "Chiudere la giornata non significa diventare indifferenti. Significa accettare che attenzione e responsabilità hanno bisogno di pause per restare affidabili. Un rito semplice — cambiare abiti, camminare, riordinare il tavolo, silenziare un canale — non è una soluzione universale, ma segnala al corpo che il contesto è cambiato. Il confine diventa credibile quando viene ripetuto e sostenuto anche dall’organizzazione, non soltanto dalla volontà individuale.",
            ],
        },
        {
            "title": "Il lavoro come identità e misura del valore",
            "paragraphs": [
                "Alla domanda «chi sei?» rispondiamo spesso con una professione. Non è strano: il lavoro occupa tempo, produce competenze e ci colloca in una rete sociale. Diventa rischioso quando la risposta non ha alternative. Se il ruolo cambia, se arriva un errore o se l’impiego finisce, non perdiamo soltanto reddito e routine; può vacillare il modo in cui ci riconosciamo. La stanchezza cresce perché ogni risultato sembra decidere il nostro valore complessivo.",
                "Essere utili offre una gratificazione profonda. Qualcuno ha bisogno di noi, un problema viene risolto, un compito lascia una traccia visibile. Molte parti della vita non danno conferme altrettanto nette. Curare una relazione, riposare o imparare qualcosa senza scopo produce risultati lenti e difficili da misurare. Il lavoro conquista il centro anche perché restituisce punteggi, scadenze e giudizi più chiari del resto.",
                "La produttività può diventare un linguaggio morale. Una giornata piena sembra buona; una giornata lenta richiede spiegazioni. In questa logica perfino il tempo libero viene ottimizzato: allenarsi meglio, viaggiare di più, trasformare una passione in progetto. Non è sbagliato desiderare crescita. Il problema compare quando ogni attività deve dimostrare qualcosa e non resta alcuno spazio in cui esistere senza produrre una versione migliorata di sé.",
                "Allargare l’identità non richiede disprezzare il lavoro. Significa riconoscere altri nomi con cui possiamo descriverci: amico, figlia, vicino, lettore, persona curiosa, membro di una comunità. Alcuni non sono ruoli prestigiosi e proprio per questo proteggono. Ricordano che l’appartenenza non dipende sempre da una valutazione e che una giornata può avere valore anche quando nessuno la registra in un curriculum.",
                "Un esercizio utile consiste nel completare la frase «sono una persona che…» senza citare mestiere, risultati o proprietà. All’inizio può sembrare artificiale. Le parole che emergono indicano qualità praticate, legami e interessi trascurati. Non servono a costruire un’identità alternativa perfetta, ma a distribuire il peso. Se una sola area contiene tutto il valore, ogni difficoltà in quell’area diventa una minaccia troppo grande.",
            ],
        },
        {
            "title": "Il tempo libero che non sappiamo più abitare",
            "paragraphs": [
                "Quando il tempo è stato organizzato a lungo da richieste esterne, la libertà può sembrare vuota. Il primo impulso è riempirla: commissioni, schermi, piccoli lavori, programmi così fitti da evitare la domanda su ciò che desideriamo. Non è pigrizia né incapacità. Scegliere richiede un contatto con preferenze che possono essersi indebolite, mentre eseguire una richiesta conosciuta offre una direzione immediata.",
                "Il riposo non coincide sempre con l’immobilità. Per qualcuno è sonno, per altri movimento, conversazione, silenzio o un’attività manuale. Ciò che recupera davvero riduce l’allarme e restituisce presenza; ciò che anestetizza fa passare il tempo senza necessariamente rinnovare energia. Anche l’anestesia può essere necessaria dopo una giornata dura, ma riconoscerla impedisce di aspettarsi da essa un nutrimento che non può offrire.",
                "La domanda «che cosa mi piace?» può essere troppo grande quando siamo esausti. È più accessibile chiedersi che cosa rende i prossimi venti minuti leggermente più abitabili. Una doccia senza fretta, una telefonata, una breve passeggiata o preparare qualcosa con le mani non devono diventare una nuova disciplina. Sono esperimenti che riaprono la percezione e permettono al desiderio di tornare prima in forme piccole.",
                "Anche la noia ha una funzione. Dopo un lungo periodo di stimoli e compiti, il vuoto iniziale può essere sgradevole. Se viene riempito immediatamente, non scopriamo che cosa sarebbe emerso. Restare qualche minuto senza una consegna non garantisce intuizioni profonde, ma interrompe l’automatismo della risposta. Il tempo libero comincia quando non viene usato soltanto per recuperare abbastanza da tornare produttivi.",
                "Abitare il tempo richiede continuità più che eventi eccezionali. Una vacanza può dare sollievo, ma non sostituisce piccoli spazi regolari in cui la vita non è sospesa. Difendere un’ora ricorrente, un pasto non affrettato o una sera senza disponibilità può sembrare poco. Ripetuto, quel margine diventa un luogo riconoscibile e ricorda che la vita non deve aspettare una futura stagione meno impegnativa per cominciare.",
            ],
        },
        {
            "title": "Denaro, necessità e margini reali",
            "paragraphs": [
                "Parlare di equilibrio senza considerare il denaro può diventare ingiusto. Molte persone lavorano molto perché affitto, rate, cura e spese essenziali non lasciano alternative immediate. Un consiglio che presume libertà economica trasforma un problema strutturale in una scelta individuale. Riconoscere i vincoli non significa rinunciare a ogni cambiamento; significa evitare di giudicare chi non può applicare soluzioni costruite per condizioni diverse.",
                "Anche dentro vincoli stretti esistono differenze importanti. Un turno comunicato con anticipo permette di organizzare la vita; lo stesso numero di ore deciso all’ultimo momento la rende instabile. Una pausa rispettata, un riposo settimanale prevedibile o un confine sulle reperibilità possono avere un impatto concreto senza ridurre subito il reddito. Per questo le condizioni organizzative contano quanto il conteggio delle ore.",
                "Conoscere le proprie spese non risolve salari insufficienti, ma chiarisce il margine. A volte scopriamo che una parte del sovraccarico sostiene consumi diventati automatici; altre volte emerge che non c’è quasi nulla da tagliare. Entrambe le conclusioni sono utili. La prima apre una scelta tra reddito aggiuntivo e tempo; la seconda mostra che servono tutele, negoziazione, sostegno o un cambiamento più ampio, non una migliore forza di volontà.",
                "La paura economica può restare anche quando la situazione migliora. Chi ha vissuto precarietà tende comprensibilmente ad accumulare lavoro come protezione. Chiedersi quale soglia renderebbe possibile rallentare trasforma una paura indefinita in un criterio: un fondo di emergenza, un debito ridotto, una competenza alternativa. Il numero non elimina l’incertezza, ma impedisce che «non è mai abbastanza» diventi una regola senza fine.",
                "Le scelte sul lavoro coinvolgono spesso altre persone. Ridurre ore, cambiare sede o rifiutare straordinari può spostare carichi nella famiglia o nel gruppo. La soluzione più giusta non è sempre quella individualmente più libera. Serve una conversazione trasparente su costi, benefici e distribuzione della cura. Il margine reale nasce quando il tempo viene trattato come una risorsa comune e non come ciò che resta dopo le decisioni economiche.",
            ],
        },
        {
            "title": "Relazioni che ricevono soltanto gli avanzi",
            "paragraphs": [
                "Le relazioni raramente crollano perché una persona ha avuto una settimana intensa. Si indeboliscono quando ricevono per mesi soltanto attenzione residua. Si parla mentre si risponde a un messaggio, si rimanda un incontro, si ascolta con la mente già sulla mattina successiva. Nessun singolo episodio sembra decisivo, ma il legame impara di non poter contare su una presenza intera.",
                "Il tempo condiviso non deve essere lungo per essere significativo. Ha bisogno però di una qualità riconoscibile: poter finire una frase, non essere interrotti da ogni notifica, sapere quando ci si rivedrà. La prevedibilità crea fiducia. Un appuntamento modesto ma rispettato può nutrire più di una promessa grandiosa continuamente rinviata. Proteggerlo significa accettare che qualcosa di lavorativo resti incompleto per un po’.",
                "Anche chi lavora molto ha bisogno di essere visto oltre la prestazione. Quando ogni conversazione riguarda problemi, scadenze e stanchezza, la persona finisce per coincidere con ciò che la consuma. Domandare che cosa ha attirato l’attenzione, fatto ridere o suscitato curiosità riapre altri registri. Non è un modo per negare la fatica, ma per impedirle di diventare l’unico contenuto disponibile.",
                "La cura non deve trasformarsi in un’altra lista di compiti. Se chi è esausto deve anche produrre una relazione perfetta, aumenta il carico. Può essere più onesto dire quali energie esistono e concordare una forma sostenibile di presenza. A volte significa cucinare insieme senza parlare molto; altre chiedere aiuto o rinunciare a un impegno. La vicinanza cresce quando non richiede di fingere risorse che mancano.",
                "Osservare chi riceve sempre gli avanzi rivela le priorità effettive, non quelle dichiarate. Può trattarsi del partner, dei figli, degli amici o di noi stessi. Non serve rispondere con colpa. La colpa consuma energia e spesso lascia tutto uguale. È più utile scegliere un legame e restituirgli uno spazio concreto, abbastanza piccolo da essere mantenuto e abbastanza vero da non dipendere da un futuro meno pieno.",
            ],
        },
        {
            "title": "Confini individuali e responsabilità dell’organizzazione",
            "paragraphs": [
                "I confini personali sono necessari, ma non possono compensare qualunque sistema. Se il carico supera stabilmente il tempo disponibile, dire meglio di no distribuisce soltanto l’insufficienza. Servono priorità esplicite, risorse, personale e responsabilità manageriale. Chiedere quale attività deve essere rimandata quando ne arriva una nuova rende visibile il conflitto e impedisce che ogni richiesta venga aggiunta senza togliere nulla.",
                "Un limite efficace è specifico. «Devo lavorare meno» è un’intenzione; «dopo le 19 non leggo i messaggi salvo questa emergenza definita» è una regola osservabile. Per reggere, però, deve considerare il ruolo e le conseguenze. In alcuni lavori la reperibilità è reale e va organizzata a turno, compensata e separata dalla disponibilità permanente. Il confine non nega il dovere: gli dà una forma sostenibile.",
                "Documentare carichi, orari e interruzioni aiuta a uscire dalle impressioni. Una settimana di dati può mostrare quante ore assorbono riunioni, urgenze e attività non previste. Non è necessario trasformare ogni minuto in una metrica. Basta raccogliere elementi utili a una conversazione: che cosa impedisce il lavoro principale, quali richieste si ripetono e quali decisioni mancano.",
                "La solidarietà tra colleghi conta. Un confine individuale può scaricare il lavoro su chi ha meno potere di opporsi. Per questo è utile cercare soluzioni condivise: turnazioni, criteri comuni, segnalazioni collettive e uso delle rappresentanze quando presenti. La tutela non è un gesto egoistico se mira a rendere il carico più leggibile e giusto per tutti, compresi coloro che non possono negoziare da soli.",
                "Quando l’organizzazione non cambia, resta una scelta difficile tra adattamento e uscita. Preparare un’alternativa richiede tempo, competenze e sicurezza economica; non sempre è possibile subito. Anche allora un piano graduale restituisce una parte di agency: aggiornare un curriculum, esplorare un settore, chiedere informazioni, fissare una soglia oltre la quale cercare aiuto. Non è una fuga immaginaria, ma la costruzione lenta di un margine.",
            ],
        },
        {
            "title": "Restituire alla vita un posto prima degli avanzi",
            "paragraphs": [
                "Cambiare rapporto con il lavoro non richiede necessariamente una svolta spettacolare. Le trasformazioni più solide iniziano spesso da una decisione ripetibile: una pausa davvero presa, un giorno senza posta, un incontro non sacrificato alla prima urgenza. Questi gesti non risolvono condizioni ingiuste, ma rendono visibile quale spazio intendiamo proteggere e offrono informazioni su ciò che l’ambiente permette o ostacola.",
                "Scegliere una priorità esterna al lavoro aiuta più di un generico proposito di equilibrio. Può essere il sonno, una relazione, la salute, una pratica creativa o una responsabilità di cura. Quando la priorità ha un nome, diventa possibile confrontare le decisioni. Non vincerà sempre, ma smetterà di perdere automaticamente. Il tempo non appare da solo: viene assegnato prima che tutte le richieste siano concluse.",
                "È utile distinguere recupero e costruzione. Il recupero ripara ciò che il lavoro consuma; la costruzione crea una vita che non dipende soltanto dal lavoro. Dormire e riposare sono indispensabili, ma servono anche esperienze che generino appartenenza, curiosità e memoria. Se tutto il tempo libero viene usato per tornare funzionali, la vita resta organizzata attorno alla prestazione anche quando la prestazione è sospesa.",
                "I segnali di esaurimento persistente meritano attenzione competente, soprattutto quando compaiono insonnia, ansia intensa, umore depresso, sintomi fisici o incapacità di recuperare. Chiedere aiuto medico o psicologico non trasforma un problema organizzativo in una debolezza individuale. Può proteggere la salute e fornire strumenti mentre si affrontano anche condizioni, tutele e decisioni concrete.",
                "La domanda iniziale non pretende una risposta unica. Possiamo essere stanchi del lavoro e, insieme, di una vita che gli ha ceduto troppo terreno. Il passo importante è smettere di usare ogni pausa soltanto per diventare nuovamente disponibili. Restituire alla vita un posto significa darle appuntamenti, relazioni e scelte che non attendano il completamento impossibile di tutto il resto.",
            ],
        },
    ],
}


def main() -> None:
    answer_len = len(" ".join(PACKAGE["answer_paragraphs"]))
    book_len = len(" ".join(p for page in PACKAGE["book_pages"] for p in page["paragraphs"]))
    if not 1000 <= answer_len <= 3000:
        raise SystemExit(f"risposta fuori soglia: {answer_len}")
    if not 15000 <= book_len <= 30000:
        raise SystemExit(f"ebook fuori soglia: {book_len}")

    dt = datetime(2026, 9, 25, 5, 30, tzinfo=ROME)
    qpath = ROOT / "domanda-del-giorno" / SLUG / "index.html"
    bpath = ROOT / "biblioteca/vita-relazioni/domande-per-conoscersi" / SLUG / "index.html"
    qpath.parent.mkdir(parents=True, exist_ok=True)
    bpath.parent.mkdir(parents=True, exist_ok=True)
    qpath.write_text(render_question_page(QUESTION, PACKAGE, SLUG, DATE, DATE_LABEL, BOOK_URL), encoding="utf-8")
    bpath.write_text(render_book_page(QURL, BOOK_URL, PACKAGE), encoding="utf-8")

    update_home(SLUG, dt, DATE_LABEL)
    update_archive(QUESTION, PACKAGE, SLUG, DATE_LABEL)
    update_search(QUESTION, PACKAGE, QURL, BOOK_URL)
    update_sitemap(DATE, QURL, BOOK_URL)
    update_feed(dt, QUESTION, PACKAGE, QURL)

    manifest_path = ROOT / "curiomondo-site-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    daily = manifest.setdefault("daily_state", {})
    daily.update({
        "current_question_source_number": QUESTION_NUMBER,
        "last_question_date": DATE,
        "last_question_slug": SLUG,
    })
    used = daily.setdefault("used_question_source_numbers", [])
    if QUESTION_NUMBER not in used:
        used.append(QUESTION_NUMBER)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    for name in ("RELEASE-STATE.json", "CURIOMONDO-RELEASE-STATE.json"):
        path = ROOT / name
        state = json.loads(path.read_text(encoding="utf-8"))
        state["last_daily_question_date"] = DATE
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(json.dumps({"status": "ok", "question": QUESTION_NUMBER, "answer": answer_len, "ebook": book_len}, ensure_ascii=False))


if __name__ == "__main__":
    main()
