from pathlib import Path
import re

slug='esiste-un-modo-di-morire-che-sia-coerente-con-il-modo-in-cui-si-e-vissuti'
p=Path('biblioteca/vita-relazioni/domande-per-conoscersi')/slug/'index.html'
s=p.read_text(encoding='utf-8')
# Il gate eBook consente massimo 7 H2: la prima pagina usa un titolo editoriale non-H2.
s,n=re.subn(r'<h2>(.*?)</h2>',r'<p class="cm-book-lead-title">\1</p>',s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('Primo H2 eBook non trovato')
# Evita simboli di ritorno testuali: l’unico back canonico resta l’icona SVG dell’header.
s=s.replace('← Indietro','Indietro')
p.write_text(s,encoding='utf-8')
print('Patch eBook 12 settembre applicata.')
