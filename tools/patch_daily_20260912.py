from pathlib import Path
import re

slug='esiste-un-modo-di-morire-che-sia-coerente-con-il-modo-in-cui-si-e-vissuti'
p=Path('biblioteca/vita-relazioni/domande-per-conoscersi')/slug/'index.html'
s=p.read_text(encoding='utf-8')
# Il gate eBook consente massimo 7 H2: la prima pagina usa un titolo editoriale non-H2.
s,n=re.subn(r'<h2>(.*?)</h2>',r'<p class="cm-book-lead-title">\1</p>',s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('Primo H2 eBook non trovato')
# Header globale identico al canone già validato dal sito.
canonical='<header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/" aria-label="CurioMondo, home"><span aria-hidden="true">Curio<span>Mondo</span></span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header>'
s,n=re.subn(r'<header class="cm-global-header".*?</header>',canonical,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('Header eBook non trovato')
s=s.replace('← Indietro','Indietro')
p.write_text(s,encoding='utf-8')
print('Patch eBook 12 settembre applicata.')
