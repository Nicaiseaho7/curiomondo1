#!/usr/bin/env python3
from pathlib import Path
from PIL import Image
from xml.etree import ElementTree as ET
import html as htmllib
import json
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
SLUGS=[
'terremoto-indonesia-100-morti-180000-evacuati-24-agosto-2026',
'ue-61-miliardi-difesa-ucraina-24-agosto-2026',
'nevada-incendio-hawk-fire-reno-evacuazioni-24-agosto-2026',
'guinea-conakry-frana-discarica-30-morti-24-agosto-2026',
'tunisia-naufragio-migranti-italia-11-morti-24-agosto-2026',
'shein-ipo-hong-kong-valutazione-27-miliardi-24-agosto-2026',
'cina-rinvia-missione-lunare-change-7-ghiaccio-24-agosto-2026',
'alibaba-collocamento-10-miliardi-ai-azioni-calo-24-agosto-2026']
IMAGES=[
'terremoto-indonesia-flores-100-morti-24-agosto-2026-ai-960.webp',
'ue-61-miliardi-difesa-ucraina-24-agosto-2026-ai-960.webp',
'nevada-hawk-fire-reno-24-agosto-2026-ai-960.webp',
'guinea-conakry-discarica-frana-24-agosto-2026-ai-960.webp',
'tunisia-naufragio-migranti-italia-24-agosto-2026-ai-960.webp',
'shein-ipo-hong-kong-24-agosto-2026-ai-960.webp',
'change-7-rinvio-luna-24-agosto-2026-ai-960.webp',
'alibaba-ai-collocamento-hong-kong-24-agosto-2026-ai-960.webp']
Q='quale-verita-su-di-te-continui-a-chiamare-confusione-perche-ammetterla-ti-obbligherebbe-a-cambiare-qualcosa'
errors=[]
def check(ok,msg):
    if not ok: errors.append(msg)

home=(ROOT/'index.html').read_text()
archive=(ROOT/'notizie/index.html').read_text()
search=(ROOT/'assets/data/search-index-v101.json').read_text()
feed=(ROOT/'feed.xml').read_text()
site=(ROOT/'sitemap.xml').read_text()
newsmap=(ROOT/'news-sitemap.xml').read_text()

for slug,img in zip(SLUGS,IMAGES):
    p=ROOT/'notizie'/f'{slug}.html'; check(p.exists(),f'HTML assente: {slug}')
    if p.exists():
        t=p.read_text(); check(f'https://curiomondo.it/notizie/{slug}.html' in t,f'canonical assente: {slug}')
        m=re.search(r'<script type="application/ld\+json">(.*?)</script>',t,re.S)
        check(bool(m),f'JSON-LD assente: {slug}')
        if m:
            try: check(json.loads(m.group(1)).get('@type')=='NewsArticle',f'JSON-LD non NewsArticle: {slug}')
            except Exception: errors.append(f'JSON-LD invalido: {slug}')
        art=re.search(r'<article class="art-body"([^>]*)>(.*?)</article>',t,re.S)
        check(bool(art),f'corpo articolo assente: {slug}')
        if art:
            body=art.group(2)
            check(len(re.findall(r'<p>',body))>=6,f'meno di 6 paragrafi: {slug}')
            check(not re.search(r'<h[23]\b',body),f'sottotitoli nel corpo: {slug}')
            plain=htmllib.unescape(re.sub(r'<[^>]+>',' ',body)); chars=len(re.sub(r'\s+',' ',plain).strip())
            exception=re.search(r'data-length-exception="([^"]{20,})"',art.group(1))
            check(5000<=chars<=7000 or bool(exception),f'corpo fuori limite 5.000–7.000 senza eccezione motivata: {slug} ({chars})')
            check('data-length-policy="5000-7000"' in art.group(1) or bool(exception),f'policy lunghezza non dichiarata: {slug}')
        check('Fonti consultate' in t and 'generata con IA' in t,f'fonti/disclosure assenti: {slug}')
        check('Perché conta davvero' not in t and 'Perché è rilevante' not in t,f'frase vietata: {slug}')
    ip=ROOT/'assets/images/optimized'/img; check(ip.exists(),f'immagine assente: {img}')
    if ip.exists():
        check(30_000 <= ip.stat().st_size <= 700_000,f'dimensione immagine non conforme: {img}')
        try:
            im=Image.open(ip); check(im.size==(960,720),f'crop/dimensioni non 4:3: {img}')
        except Exception: errors.append(f'immagine illeggibile: {img}')
    for hay,name in [(home,'home'),(archive,'archivio'),(search,'ricerca'),(feed,'feed'),(site,'sitemap'),(newsmap,'news sitemap')]:
        check(slug in hay,f'{slug} assente da {name}')

sets=re.findall(r'<div(?: aria-hidden="true")? class="cm-ticker-set">(.*?)</div>',home,re.S)
check(len(sets)==2,'LIVE deve avere due set duplicati')
for i,x in enumerate(sets): check(len(re.findall(r'class="ticker-news"',x))==10,f'LIVE set {i+1} non contiene 10 elementi')
check('data-breaking-id="terremoto_indonesia_100_morti_180000_evacuati_24_agosto_2026"' in home,'hero non impostata sul nuovo bilancio del terremoto in Indonesia')
check('Domanda del giorno · 24 agosto 2026' in home and Q in home,'domanda corrente assente dalla home')
qcard=re.search(r'<section aria-label="Domanda del giorno" class="cm-qday">(.*?)</section>',home,re.S)
check(bool(qcard) and 'Quale verità' not in qcard.group(1),'la home rivela la domanda')
check(bool(qcard) and 'class="cm-qday-card"' in qcard.group(1) and 'class="cm-qday-hint"' in qcard.group(1),'markup premium della card Domanda del giorno alterato')
check(bool(qcard) and 'cm-qday-copy' not in qcard.group(1) and 'cm-qday-cta' not in qcard.group(1),'classi non approvate nella card Domanda del giorno')
deep=re.search(r'<section aria-label="Approfondimenti collegati".*?</section>',home,re.S)
check(bool(deep) and len(re.findall(r'<a ',deep.group(0)))==3,'approfondimenti home non esattamente 3')
check('return pinned.concat(ranked).slice(0,5);' in (ROOT/'assets/js/home-original-v101.js').read_text(),'In evidenza non limitato a 5')
check('Nicaise' in home,'firma Nicaise assente')
check('home-original-v101.js?v=163' in home and 'home-original-v101.css?v=163' in home,'cache version home non aggiornata')

qp=ROOT/'domanda-del-giorno'/Q/'index.html'; ep=ROOT/'biblioteca/vita-relazioni/domande-per-conoscersi'/Q/'index.html'
check(qp.exists() and ep.exists(),'pagina domanda o mini e-book assente')
if qp.exists():
    qt=qp.read_text(); flow=re.search(r'<article class="cm-daily-flow">(.*?)</article>',qt,re.S)
    check(bool(flow),'risposta quotidiana assente')
    if flow:
        check(not re.search(r'<h[23]\b',flow.group(1)),'la risposta quotidiana contiene sottotitoli vietati')
        check(all(len(re.sub(r'<[^>]+>',' ',p))<1000 for p in re.findall(r'<p[^>]*>(.*?)</p>',flow.group(1),re.S)),'paragrafo troppo lungo nella risposta quotidiana')
    check('4 min di lettura' in qt,'tempo di lettura domanda non conforme')
if ep.exists():
    plain=re.sub(r'<[^>]+>',' ',ep.read_text()); plain=htmllib.unescape(re.sub(r'\s+',' ',plain))
    check(7000<=len(plain)<=15000,f'mini e-book fuori limite: {len(plain)} caratteri')
check(Q in (ROOT/'domanda-del-giorno/index.html').read_text(),'domanda assente dall’archivio')
check(Q in (ROOT/'biblioteca/vita-relazioni/domande-per-conoscersi/index.html').read_text(),'mini e-book assente dalla categoria')
for f in ['feed.xml','sitemap.xml','news-sitemap.xml']:
    try: ET.parse(ROOT/f)
    except Exception as e: errors.append(f'{f} non valido: {e}')
manifest=json.loads((ROOT/'curiomondo-site-manifest.json').read_text())
check(manifest['daily_state']['last_question_date']=='2026-08-24','manifest domanda non aggiornato')
state=json.loads((ROOT/'CURIOMONDO-RELEASE-STATE.json').read_text())
check(state['site_version'] in (161,162,163,164),'versione candidate/finale inattesa')
release_date=state.get('release_date','')
for page in (ROOT/'notizie').glob('*.html'):
    text=page.read_text()
    schema=re.search(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)
    if not schema: continue
    try: data=json.loads(schema.group(1))
    except Exception: continue
    if data.get('@type')!='NewsArticle' or not str(data.get('datePublished','')).startswith(release_date): continue
    art=re.search(r'<article class="art-body"([^>]*)>(.*?)</article>',text,re.S)
    check(bool(art),f'articolo del ciclo senza corpo: {page.name}')
    if not art: continue
    body=art.group(2); plain=htmllib.unescape(re.sub(r'<[^>]+>',' ',body)); chars=len(re.sub(r'\s+',' ',plain).strip())
    exception=re.search(r'data-length-exception="([^"]{20,})"',art.group(1))
    check(5000<=chars<=7000 or bool(exception),f'articolo del ciclo fuori limite senza eccezione: {page.name} ({chars})')
    check(not re.search(r'<h[23]\b',body),f'articolo del ciclo con sottotitoli nel corpo: {page.name}')

for page in ROOT.rglob('*.html'):
    check(not re.search(r'una\s+domanda[.!]?\s+nessuna\s+risposta\s+automatica',page.read_text(),re.I),f'frase vietata Domanda del giorno: {page.relative_to(ROOT)}')
book_root=ROOT/'biblioteca/vita-relazioni/domande-per-conoscersi'
for page in book_root.glob('*/index.html'):
    text=page.read_text(); page_count=len(re.findall(r'\bdata-book-page\b',text)); h2_count=len(re.findall(r'<h2\b',text,re.I))
    check(4<=page_count<=6,f'mini e-book non sfogliabile o numero pagine errato: {page.parent.name} ({page_count})')
    check(h2_count<=4,f'troppi sottotitoli nel mini e-book: {page.parent.name} ({h2_count})')
    check('data-book-prev' in text and 'data-book-next' in text and 'data-book-count' in text,f'controlli libro assenti: {page.parent.name}')
    check('biblioteca-book-reader-v1.css' in text and 'biblioteca-book-reader-v1.js' in text,f'asset lettore libro assenti: {page.parent.name}')
    article=re.search(r'<article class="cm-book-shell">(.*?)</article>',text,re.S)
    if article:
        plain=htmllib.unescape(re.sub(r'<[^>]+>',' ',article.group(1))); chars=len(re.sub(r'\s+',' ',plain).strip())
        check(7000<=chars<=15000,f'mini e-book fuori limite: {page.parent.name} ({chars})')
check((ROOT/'assets/css/biblioteca-book-reader-v1.css').exists(),'CSS lettore libro assente')
check((ROOT/'assets/js/biblioteca-book-reader-v1.js').exists(),'JS lettore libro assente')

if errors:
    print('PREDEPLOY FAIL')
    for e in errors: print('-',e)
    sys.exit(1)
print('PREDEPLOY OK — 8 articoli, 8 immagini, home, LIVE, domanda, archivi, feed e sitemap verificati')
