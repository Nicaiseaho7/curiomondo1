#!/usr/bin/env python3
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]
src=(ROOT/'tools/build_v308.py').read_text(encoding='utf-8')
repls={
"VERSION=308":"VERSION=313","DATE='2026-09-08'":"DATE='2026-09-10'","DATE_LABEL='8 settembre 2026'":"DATE_LABEL='10 settembre 2026'",
"OLD='cosa-faremmo-se-il-tempo-tornasse-indietro-di-dieci-anni-sapendo-cio-che-sappiamo-ora'":"OLD='quando-la-prudenza-smette-di-proteggerci-e-comincia-a-trattenerci'",
"SLUG='quale-parte-della-tua-vita-stai-vivendo-in-attesa-di-sentirti-finalmente-pronto'":"SLUG='cosa-faremmo-oggi-se-il-coraggio-arrivasse-prima-del-tempo'",
"QUESTION='Quale parte della tua vita stai vivendo in attesa di sentirti finalmente pronto?'":"QUESTION='Cosa faremmo oggi se il coraggio arrivasse prima del tempo?'",
"DECK='Una riflessione sulla differenza tra prepararsi davvero e usare la preparazione per rimandare ciò che conta.'":"DECK='Dal PDF Mille e più domande per pensare, una riflessione sul coraggio che non cancella la paura ma le impedisce di scegliere al posto nostro.'",
"BOOK_TITLE='La soglia che continuiamo a preparare'":"BOOK_TITLE='Il coraggio prima del momento perfetto'",
"BOOK_DECK='Un eBook su attesa, paura e piccoli inizi: come capire quando essere prudenti e quando la prudenza è diventata rinvio.'":"BOOK_DECK='Un eBook su paura, prudenza e piccoli inizi: come agire con misura quando la certezza non arriva.'",
"Domanda del giorno dell’8 settembre 2026":"Domanda del giorno del 10 settembre 2026",
"if strong: strong[0].text='08'":"if strong: strong[0].text='10'"
}
for a,b in repls.items(): src=src.replace(a,b)
paras='''QUESTION_PARAGRAPHS=[
"A volte immaginiamo il coraggio come qualcosa che arriva al momento giusto: una forza improvvisa che mette ordine nei dubbi e rende semplice ciò che fino a ieri sembrava impossibile. Ma il tempo raramente ci consegna una certezza completa. Ci offre una giornata normale, qualche informazione incompleta e la possibilità di scegliere anche mentre una parte di noi vorrebbe restare ferma.",
"Se il coraggio arrivasse prima del tempo, forse non cambieremmo tutta la nostra vita. Potremmo fare quella telefonata rimandata, mostrare un lavoro ancora imperfetto, dire una verità con rispetto o chiedere aiuto senza aspettare di essere esausti. Il gesto coraggioso non sarebbe necessariamente grande: sarebbe preciso, riconoscibile e abbastanza piccolo da non trasformare l’audacia in incoscienza.",
"Il coraggio non elimina la prudenza. Le dà un confine. Ci chiede che cosa stiamo davvero proteggendo, quali conseguenze possiamo sostenere e quale rischio esiste soltanto nella paura del giudizio. Quando salute, denaro o altre persone sono coinvolti, prepararsi resta necessario. Quando invece continuiamo a spostare la soglia dopo ogni nuova risposta, l’attesa può essere diventata una forma elegante di rinuncia.",
"Molte sicurezze nascono dopo il primo passo. Una conversazione ci insegna più di dieci dialoghi immaginati; una prova limitata mostra difficoltà che la teoria non vede; un no reale può fare meno male di mesi trascorsi ad anticiparlo. Agire non garantisce il risultato, ma restituisce informazioni che il pensiero da solo non può produrre.",
"Forse oggi il coraggio potrebbe arrivare prima non come un’emozione, ma come una regola gentile: scegliere un gesto reversibile, fissare un limite e accettare che la paura venga con noi. Il presente non deve diventare perfetto per essere abitabile.",
"Quale gesto compiresti oggi se non dovessi prima dimostrare a te stesso di non avere paura?"
]

BOOK_PAGES='''
src=re.sub(r'QUESTION_PARAGRAPHS=\[.*?\]\n\nBOOK_PAGES=',paras,src,flags=re.S)
exec(compile(src,str(ROOT/'tools/build_v313_question.py'),'exec'),{'__file__':str(ROOT/'tools/build_v313_question.py'),'__name__':'__main__'})
