from pathlib import Path
from copy import deepcopy
from datetime import datetime
import json,re,subprocess
from lxml import html

ROOT=Path('.')
SLUG='indonesia-traghetto-virgo-transport-8-129-dispersi-13-settembre-2026'

# 1) Porta il nuovo articolo nel range standard 300-600 parole con dettagli verificati da AP/Reuters.
p=ROOT/'notizie'/f'{SLUG}.html'
s=p.read_text(encoding='utf-8')
extra=(
'<p>Associated Press riferisce che il manifesto comprendeva 213 passeggeri, 30 membri dell’equipaggio e 89 veicoli. Prima del capovolgimento era stato trasmesso un segnale di emergenza mentre nella zona si registravano onde fino a circa tre metri, un elemento che sarà valutato nell’inchiesta tecnica.</p>'
'<p>La nave, costruita in Giappone nel 1987 e acquisita più recentemente dalla compagnia PT Virgo Karya Shipping, si trovava a circa 148 chilometri da Banjarmasin nell’ultima area di ricerca indicata. Questi dati aiutano a delimitare la zona delle operazioni, ma non stabiliscono da soli la causa dell’incidente.</p>'
'<p>Le autorità stanno inoltre verificando il manifesto effettivo e la distribuzione delle persone tra passeggeri ed equipaggio. Nei grandi incidenti marittimi i numeri iniziali possono cambiare durante l’identificazione dei sopravvissuti e dei dispersi, perciò CurioMondo aggiornerà il bilancio soltanto dopo nuove conferme ufficiali o di agenzie affidabili.</p>'
)
if 'manifesto comprendeva 213 passeggeri' not in s:
    s=s.replace('</article>',extra+'</article>',1)
p.write_text(s,encoding='utf-8')

# 2) Porta l'articolo sul confine polacco oltre le 300 parole senza alterarne il senso.
p=ROOT/'notizie/russia-attacco-confine-polonia-yahodyn-dorohusk-13-settembre-2026.html'
s=p.read_text(encoding='utf-8')
add='<p>Il collegamento Kyiv–Varsavia resta una delle principali vie ferroviarie internazionali usate dai passeggeri tra l’Ucraina e la Polonia. Il danneggiamento di una carrozza evacuata mostra quindi un impatto diretto anche sulla mobilità civile transfrontaliera.</p>'
if 'mobilità civile transfrontaliera' not in s:
    s=s.replace('</article>',add+'</article>',1)
p.write_text(s,encoding='utf-8')

# 3) Allinea datePublished alla prima pubblicazione verificabile nel repository per gli articoli segnalati dall'audit.
paths=[
'carburanti-decreto-157-accise-17-settembre-2026.html',
'ricerca-cancro-italia-495-trial-europa-13-settembre-2026.html',
'positano-incendio-frana-statale-amalfitana-13-settembre-2026.html',
'dengue-italia-265-casi-24-autoctoni-8-settembre-2026.html',
'russia-attacco-confine-polonia-yahodyn-dorohusk-13-settembre-2026.html',
]
for name in paths:
    fp=ROOT/'notizie'/name
    text=fp.read_text(encoding='utf-8')
    rel=fp.as_posix()
    proc=subprocess.run(['git','log','--diff-filter=A','--follow','--format=%aI','--',rel],capture_output=True,text=True,check=True)
    stamps=[x.strip() for x in proc.stdout.splitlines() if x.strip()]
    if not stamps:
        continue
    first_added=stamps[-1]
    m=re.search(r'<script type="application/ld\+json">(.*?)</script>',text)
    if not m:
        continue
    obj=json.loads(m.group(1))
    objs=obj if isinstance(obj,list) else [obj]
    changed=False
    for item in objs:
        if isinstance(item,dict) and item.get('@type')=='NewsArticle':
            old=item.get('datePublished')
            try:
                old_dt=datetime.fromisoformat(str(old).replace('Z','+00:00'))
                add_dt=datetime.fromisoformat(first_added.replace('Z','+00:00'))
            except Exception:
                continue
            if add_dt>old_dt:
                item['datePublished']=first_added
                mod=item.get('dateModified')
                try:
                    mod_dt=datetime.fromisoformat(str(mod).replace('Z','+00:00')) if mod else add_dt
                except Exception:
                    mod_dt=add_dt
                if mod_dt<add_dt:
                    item['dateModified']=first_added
                changed=True
    if changed:
        rep=json.dumps(obj,ensure_ascii=False,separators=(',',':'))
        text=text[:m.start(1)]+rep+text[m.end(1):]
        fp.write_text(text,encoding='utf-8')

# 4) Ricostruisce Ultime notizie e Tutte le notizie dalla cronologia reale dei NewsArticle indicizzabili.
def cls_xpath(name):
    return f'contains(concat(" ",normalize-space(@class)," ")," {name} ")'

def meta_for(url):
    name=url.rsplit('/',1)[-1]
    fp=ROOT/'notizie'/name
    d=html.fromstring(fp.read_text(errors='replace'))
    title=' '.join(d.xpath('//main[contains(@class,"wrap")]//h1[1]//text()')).strip()
    desc=' '.join(d.xpath('//main[contains(@class,"wrap")]//p[contains(@class,"subtitle")][1]//text()')).strip()
    badge=' '.join(d.xpath('//main[contains(@class,"wrap")]//*[contains(@class,"badge")][1]//text()')).strip()
    img=d.xpath('//main//figure[1]//img[1]')
    src=img[0].get('src','') if img else ''
    if src.startswith('../'): src='/'+src[3:]
    srcset=img[0].get('srcset','') if img else ''
    if srcset:
        parts=[]
        for piece in srcset.split(','):
            piece=piece.strip()
            if not piece: continue
            bits=piece.split()
            if bits and bits[0].startswith('../'): bits[0]='/'+bits[0][3:]
            parts.append(' '.join(bits))
        srcset=', '.join(parts)
    alt=img[0].get('alt','') if img else title
    return {'title':title,'desc':desc,'badge':badge,'src':src,'srcset':srcset,'alt':alt}

def dates():
    out={}
    for fp in (ROOT/'notizie').glob('*.html'):
        if fp.name=='index.html': continue
        d=html.fromstring(fp.read_text(errors='replace'))
        robots=' '.join(d.xpath('//meta[@name="robots"]/@content')).lower()
        if 'noindex' in robots or not d.xpath('//main//figure[1]//img/@src'): continue
        for raw in d.xpath('//script[@type="application/ld+json"]/text()'):
            try: obj=json.loads(raw)
            except Exception: continue
            arr=obj if isinstance(obj,list) else [obj]
            for item in arr:
                if isinstance(item,dict) and item.get('@type')=='NewsArticle' and item.get('datePublished'):
                    stamp=str(item['datePublished'])
                    if len(stamp)<=10: stamp+='T00:00:00+02:00'
                    try: out['/notizie/'+fp.name]=datetime.fromisoformat(stamp.replace('Z','+00:00'))
                    except Exception: pass
                    break
            if '/notizie/'+fp.name in out: break
    return out

idx=ROOT/'index.html'
doc=html.fromstring(idx.read_text(errors='replace'))
rail=doc.xpath(f'//div[{cls_xpath("auto-rail")}]')[0]
cards=doc.xpath('//div[@id="cards"]')[0]
rail_templates=rail.xpath('./a')
card_templates=cards.xpath('./a')
if not rail_templates or not card_templates:
    raise SystemExit('Template homepage mancanti')
rail_t=deepcopy(rail_templates[0]); card_t=deepcopy(card_templates[0])
featured=doc.xpath(f'//*[{cls_xpath("featured")}]//a[contains(@class,"cta")]/@href')
featured=featured[0] if featured else None
all_dates=dates()
chron=[u for u,_ in sorted(all_dates.items(),key=lambda kv:(kv[1],kv[0]),reverse=True) if u!=featured]
need=len(rail_templates)+len(card_templates)
chron=chron[:need]

def build(tpl,url):
    node=deepcopy(tpl)
    node.set('href',url)
    m=meta_for(url)
    hs=node.xpath('.//h3')
    if hs: hs[0].text=m['title']
    ps=node.xpath('.//p')
    if ps: ps[0].text=m['desc']
    small=node.xpath('.//small')
    if small and m['badge']: small[0].text=m['badge']
    imgs=node.xpath('.//img')
    if imgs:
        imgs[0].set('src',m['src']); imgs[0].set('alt',m['alt'])
        if m['srcset']: imgs[0].set('srcset',m['srcset'])
    for source in node.xpath('.//source'):
        if m['srcset']: source.set('srcset',m['srcset'])
    return node

for child in list(rail): rail.remove(child)
for url in chron[:len(rail_templates)]: rail.append(build(rail_t,url))
for child in list(cards): cards.remove(child)
for url in chron[len(rail_templates):]: cards.append(build(card_t,url))
serialized='<!doctype html>'+html.tostring(doc,encoding='unicode',method='html')
idx.write_text(serialized,encoding='utf-8')
