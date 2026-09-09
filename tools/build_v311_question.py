#!/usr/bin/env python3
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'tools/build_v308.py').read_text(encoding='utf-8')
repls={
"VERSION=308":"VERSION=311",
"DATE='2026-09-08'":"DATE='2026-09-09'",
"DATE_LABEL='8 settembre 2026'":"DATE_LABEL='9 settembre 2026'",
"OLD='cosa-faremmo-se-il-tempo-tornasse-indietro-di-dieci-anni-sapendo-cio-che-sappiamo-ora'":"OLD='quale-parte-della-tua-vita-stai-vivendo-in-attesa-di-sentirti-finalmente-pronto'",
"SLUG='quale-parte-della-tua-vita-stai-vivendo-in-attesa-di-sentirti-finalmente-pronto'":"SLUG='quando-la-prudenza-smette-di-proteggerci-e-comincia-a-trattenerci'",
"QUESTION='Quale parte della tua vita stai vivendo in attesa di sentirti finalmente pronto?'":"QUESTION='Quando la prudenza smette di proteggerci e comincia a trattenerci?'",
"DECK='Una riflessione sulla differenza tra prepararsi davvero e usare la preparazione per rimandare ciò che conta.'":"DECK='Una riflessione sul confine sottile tra proteggere ciò che conta e lasciare che la paura decida al posto nostro.'",
"BOOK_TITLE='La soglia che continuiamo a preparare'":"BOOK_TITLE='La soglia della prudenza'",
"BOOK_DECK='Un eBook su attesa, paura e piccoli inizi: come capire quando essere prudenti e quando la prudenza è diventata rinvio.'":"BOOK_DECK='Un eBook per distinguere il rischio reale dal timore di esporsi e progettare passi piccoli, responsabili e verificabili.'",
"Domanda del giorno dell’8 settembre 2026":"Domanda del giorno del 9 settembre 2026",
"node.set('datetime',DATE); strong=node.xpath('./strong'); span=node.xpath('./span')\n if strong: strong[0].text='08'":"node.set('datetime',DATE); strong=node.xpath('./strong'); span=node.xpath('./span')\n if strong: strong[0].text='09'"
}
for a,b in repls.items(): src=src.replace(a,b)
paras='''QUESTION_PARAGRAPHS=[
"La prudenza ha una voce rassicurante. Ci invita a non correre, a controllare i rischi, a non consegnare una scelta importante all’impulso. È una capacità preziosa, soprattutto quando sono coinvolti salute, denaro, lavoro o altre persone. Ma proprio perché sembra sempre ragionevole, può diventare il nome più elegante che diamo alla paura quando non vogliamo ammettere che stiamo rimandando.",
"La differenza non sta nella quantità di tempo che aspettiamo. Sta in ciò che l’attesa produce. Se raccogliamo un’informazione necessaria, mettiamo da parte risorse, chiediamo un parere competente o costruiamo una condizione di sicurezza, la prudenza modifica davvero il futuro. Se ripetiamo le stesse valutazioni e ogni risposta crea una nuova condizione, l’attesa non ci sta preparando: ci sta evitando l’esperienza di essere incerti.",
"Possiamo riconoscere il confine chiedendoci quale fatto preciso ci farebbe procedere. Una data, una cifra, un consenso, una competenza verificabile sono criteri concreti. Se invece la risposta è soltanto sentirsi finalmente sicuri, il traguardo rischia di spostarsi ogni volta che ci avviciniamo. Molte forme di sicurezza arrivano dopo una piccola prova, non prima.",
"Questo non obbliga a compiere salti enormi. La prudenza sana può progettare un gesto limitato e reversibile: una conversazione esplorativa, un’ora dedicata al progetto, una richiesta inviata, un preventivo, una prova con confini chiari. Il passo non serve a dimostrare coraggio. Serve a ottenere un dato che il pensiero, da solo, non può offrirci.",
"Forse la prudenza smette di proteggerci quando non sa più dire che cosa protegge, fino a quando e a quale prezzo. In quel punto può essere utile darle un compito nuovo: non impedirci di muoverci, ma aiutarci a scegliere la misura del movimento.",
"Quale rischio concreto stai evitando, e quale parte dell’attesa serve invece soltanto a non sentirti vulnerabile?"
]

BOOK_PAGES='''
src=re.sub(r'QUESTION_PARAGRAPHS=\[.*?\]\n\nBOOK_PAGES=',paras,src,flags=re.S)
code=compile(src,str(ROOT/'tools/build_v311_question.py'),'exec')
exec(code,{'__file__':str(ROOT/'tools/build_v311_question.py'),'__name__':'__main__'})
