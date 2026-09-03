#!/usr/bin/env python3
"""CurioMondo v263 static pre-deploy audit."""
from pathlib import Path
from collections import Counter
from lxml import html
from urllib.parse import urlparse, unquote
import argparse, json, subprocess, re
from datetime import datetime
from difflib import SequenceMatcher

ap=argparse.ArgumentParser(); ap.add_argument('--root',default='.'); args=ap.parse_args()
root=Path(args.root).resolve(); errors=[]
ads_path=root/'ads.txt'
ads_record='google.com, pub-8050187517048759, DIRECT, f08c47fec0942fa0'
if not ads_path.exists(): errors.append('ads.txt assente nella radice del sito')
elif ads_path.read_text(errors='replace').strip()!=ads_record: errors.append('ads.txt non autorizza il publisher AdSense del sito')
policy_path=root/'AI-EDITORIAL-IMAGE-PROTOCOL.md'
prompt_path=root/'automation/prompts/image-generation-contract.txt'
config_path=root/'automation/config.json'
manifest_path=root/'curiomondo-site-manifest.json'
image_registry_path=root/'assets/data/editorial-images-v210.json'
for required_path in (policy_path,prompt_path,config_path,manifest_path,root/'AGENTS.md'):
    if not required_path.exists(): errors.append(f'protocollo IA assente: {required_path.relative_to(root)}')
if prompt_path.exists():
    prompt=prompt_path.read_text(errors='replace')
    for marker in ('PUBLIC FIGURES AND SYNTHETIC LIKENESS','data-synthetic-likeness="public-figure"','data-sensitive-context="true|false"','AI-EDITORIAL-IMAGE-PROTOCOL.md','ORDINARY public-figure news','SENSITIVE public-figure news','neutral isolated portrait','buildings and logos are allowed'):
        if marker not in prompt: errors.append(f'direttiva immagini pubbliche assente nel prompt: {marker}')
if config_path.exists():
    try:
        config=json.loads(config_path.read_text())
        likeness=config.get('articles',{}).get('public_figure_synthetic_likeness',{})
        if likeness.get('allowed') is not True: errors.append('somiglianza sintetica pubblica non abilitata nella config')
        if likeness.get('policy_mode')!='context_sensitive': errors.append('modalità contestuale immagini pubbliche assente nella config')
        if likeness.get('ordinary_news',{}).get('contextual_scenes_allowed') is not True: errors.append('scene ordinarie non abilitate nella config')
        if likeness.get('ordinary_news',{}).get('relevant_logos_allowed') is not True: errors.append('loghi pertinenti non abilitati nella config')
        if likeness.get('sensitive_news',{}).get('neutral_isolated_portrait_required') is not True: errors.append('ritratto neutrale per casi sensibili assente nella config')
        if likeness.get('documentary_claim_forbidden') is not True: errors.append('divieto documentario assente nella config')
        articles_cfg=config.get('articles',{})
        if articles_cfg.get('body_min_chars')!=3000: errors.append('minimo articoli v257 non impostato a 3000 nella config')
        if articles_cfg.get('body_max_chars')!=7000: errors.append('massimo articoli v257 non impostato a 7000 nella config')
        if articles_cfg.get('length_exceptions_allowed') is not False: errors.append('eccezioni lunghezza articoli v257 non disabilitate')
        if articles_cfg.get('semantic_repetition_forbidden') is not True: errors.append('divieto ripetizioni semantiche assente nella config')
        length_policy_effective_from=articles_cfg.get('length_policy_effective_from','2026-09-01T12:00:00+02:00')
        try: length_policy_effective_dt=datetime.fromisoformat(length_policy_effective_from)
        except Exception: errors.append('timestamp efficacia policy lunghezza non valido'); length_policy_effective_dt=datetime.fromisoformat('2026-09-01T12:00:00+02:00')
    except Exception as exc: errors.append(f'automation/config.json non valido: {exc}')
if manifest_path.exists():
    try:
        manifest=json.loads(manifest_path.read_text())
        likeness=manifest.get('images',{}).get('public_figure_synthetic_likeness_policy',{})
        if likeness.get('allowed') is not True: errors.append('protocollo personaggi pubblici non abilitato nel manifest')
        if likeness.get('policy_mode')!='context_sensitive': errors.append('modalità contestuale immagini pubbliche assente nel manifest')
        if likeness.get('ordinary_news',{}).get('contextual_scenes_allowed') is not True: errors.append('scene ordinarie non abilitate nel manifest')
        if likeness.get('ordinary_news',{}).get('relevant_logos_allowed') is not True: errors.append('loghi pertinenti non abilitati nel manifest')
        if likeness.get('sensitive_news',{}).get('neutral_isolated_portrait_required') is not True: errors.append('ritratto neutrale per casi sensibili assente nel manifest')
        if likeness.get('must_never_be_presented_as_documentary_evidence') is not True: errors.append('divieto di prova documentaria assente nel manifest')
        body_policy=manifest.get('news',{}).get('article_body_characters',{})
        if body_policy.get('mandatory_min')!=3000 or body_policy.get('mandatory_max')!=7000: errors.append('policy manifest articoli non impostata a 3000–7000')
        if body_policy.get('exceptions_allowed') is not False: errors.append('manifest consente eccezioni di lunghezza non ammesse')
        if body_policy.get('semantic_repetition_forbidden') is not True: errors.append('manifest non vieta le ripetizioni semantiche')
    except Exception as exc: errors.append(f'curiomondo-site-manifest.json non valido: {exc}')
if image_registry_path.exists():
    try:
        image_registry=json.loads(image_registry_path.read_text())
        for item in image_registry.get('items',[]):
            if item.get('syntheticLikeness')=='public-figure':
                if item.get('sensitiveContext') not in (True,False):
                    errors.append(f"classificazione sensibilità assente: {item.get('article','senza articolo')}")
                if item.get('sensitiveContext') is True:
                    if item.get('portraitOnly') is not True or item.get('portraitFormat')!='neutral-isolated' or item.get('reenactedEvent') is not False:
                        errors.append(f"registro sensibile non conforme al ritratto neutrale: {item.get('article','senza articolo')}")
                    if 'neutral editorial portrait' not in item.get('prompt','').lower():
                        errors.append(f"prompt sensibile non neutrale: {item.get('article','senza articolo')}")
    except Exception as exc: errors.append(f'assets/data/editorial-images-v210.json non valido: {exc}')
html_files=[p for p in root.rglob('*.html') if 'IA-WORKSPACE' not in p.relative_to(root).parts]
for p in html_files:
    try: d=html.fromstring(p.read_text(errors='replace'))
    except Exception as exc: errors.append(f'HTML non valido {p.relative_to(root)}: {exc}'); continue
    ids=d.xpath('//*[@id]/@id')
    if len(ids)!=len(set(ids)): errors.append(f'ID duplicati: {p.relative_to(root)}')
    if d.xpath('//footer//*[contains(concat(" ",normalize-space(@class)," ")," cm-nicaise-signature ")]'): errors.append(f'firma Nicaise nel footer: {p.relative_to(root)}')
    for img in d.xpath('//img'):
        if img.get('alt') is None: errors.append(f'alt assente: {p.relative_to(root)}')
    for url in d.xpath('//@src|//@href'):
        if not url or url.startswith(('#','http://','https://','mailto:','tel:','data:','javascript:')): continue
        url=url.split('?')[0].split('#')[0]
        if not url: continue
        target=root/url.lstrip('/') if url.startswith('/') else p.parent/url
        if url.endswith('/'): target=target/'index.html'
        if not target.exists(): errors.append(f'riferimento rotto {p.relative_to(root)} → {url}')

news=[p for p in (root/'notizie').glob('*.html') if p.name!='index.html']
refs=[]

STOPWORDS={
    'anche','ancora','avere','aveva','avevano','come','con','contro','dalla','dalle','dello','della','delle','degli','dopo','dove','essere','fino','fra','gli','hanno','il','alla','alle','allo','che','chi','dei','del','dell','dell’','dell\'','dentro','due','era','erano','ha','in','la','le','lo','ma','mentre','nel','nella','nelle','nello','non','per','piu','più','quella','quello','questa','questo','sono','sua','sue','sul','sulla','sulle','tra','una','uno','un','nel','nei','nelle','agli','ai','al','all','alla','alle','allo','e','ed','o','ad','da','di','si','è'
}
def norm_text(value):
    value=(value or '').casefold().replace('’',"'")
    value=re.sub(r'[^0-9a-zà-öø-ÿ%€$]+',' ',value,flags=re.I)
    return re.sub(r'\s+',' ',value).strip()
def content_tokens(value):
    return {w for w in re.findall(r"[0-9a-zà-öø-ÿ%€$']+",norm_text(value),flags=re.I) if len(w)>=4 and w not in STOPWORDS}
def near_duplicate(a,b):
    na,nb=norm_text(a),norm_text(b)
    if len(na)<70 or len(nb)<70: return False
    if na==nb: return True
    seq=SequenceMatcher(None,na,nb).ratio()
    ta,tb=content_tokens(na),content_tokens(nb)
    if min(len(ta),len(tb))<6: return seq>=0.92
    containment=len(ta & tb)/min(len(ta),len(tb))
    jaccard=len(ta & tb)/max(1,len(ta | tb))
    return seq>=0.90 or (seq>=0.72 and containment>=0.84 and jaccard>=0.62)
def article_policy_active(doc):
    robots=' '.join(doc.xpath('//meta[@name="robots"]/@content')).lower()
    if 'noindex' in robots: return False
    bodies=doc.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')
    if bodies and bodies[0].get('data-length-policy')=='3000-7000': return True
    for raw in doc.xpath('//script[@type="application/ld+json"]/text()'):
        try: obj=json.loads(raw)
        except Exception: continue
        objs=obj if isinstance(obj,list) else [obj]
        for item in objs:
            if not isinstance(item,dict): continue
            typ=item.get('@type')
            if typ!='NewsArticle' and not (isinstance(typ,list) and 'NewsArticle' in typ): continue
            stamp=item.get('dateModified') or item.get('datePublished')
            if not stamp: continue
            try:
                dt=datetime.fromisoformat(str(stamp).replace('Z','+00:00'))
                if dt.tzinfo is None: continue
                if dt>=length_policy_effective_dt: return True
            except Exception: pass
    return False
caption='Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria.'
for p in news:
    d=html.fromstring(p.read_text(errors='replace'))
    if not d.xpath('//main[contains(@class,"wrap")]'): errors.append(f'main non vincolato: {p.name}')
    bodies=d.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]')
    if not bodies: errors.append(f'testo articolo assente: {p.name}')
    elif article_policy_active(d):
        body=bodies[0]
        if body.get('data-length-policy')!='3000-7000': errors.append(f'policy lunghezza v257 non dichiarata nel markup: {p.name}')
        body_text=re.sub(r'\s+',' ',' '.join(body.itertext())).strip()
        body_chars=len(body_text)
        if body_chars<3000: errors.append(f'articolo v257 sotto 3000 caratteri: {p.name} ({body_chars})')
        if body_chars>7000: errors.append(f'articolo v257 sopra 7000 caratteri: {p.name} ({body_chars})')
        paras=[re.sub(r'\s+',' ',' '.join(x.itertext())).strip() for x in body.xpath('.//p')]
        paras=[x for x in paras if x]
        sentences=[]
        for para in paras:
            sentences.extend([x.strip() for x in re.split(r'(?<=[.!?])\s+',para) if len(x.strip())>=45])
        norm_sent=[norm_text(x) for x in sentences]
        dup_exact=[x for x,c in Counter(norm_sent).items() if x and c>1]
        if dup_exact: errors.append(f'frasi duplicate nell’articolo v248: {p.name}')
        found_near=False
        for i in range(len(sentences)):
            for j in range(i+1,len(sentences)):
                if near_duplicate(sentences[i],sentences[j]):
                    errors.append(f'possibile ripetizione/parafrasi ridondante nell’articolo v248: {p.name} (frasi {i+1}/{j+1})')
                    found_near=True; break
            if found_near: break
        if not found_near:
            found_para=False
            for i in range(len(paras)):
                for j in range(i+1,len(paras)):
                    if len(paras[i])>=120 and len(paras[j])>=120 and SequenceMatcher(None,norm_text(paras[i]),norm_text(paras[j])).ratio()>=0.82:
                        errors.append(f'paragrafi ridondanti nell’articolo v248: {p.name} ({i+1}/{j+1})')
                        found_para=True; break
                if found_para: break
    figures=d.xpath('//main/figure[1]')
    if figures:
        refs += figures[0].xpath('.//img/@src')
        if ' '.join(figures[0].xpath('.//figcaption//text()')).strip()!=caption: errors.append(f'didascalia IA errata: {p.name}')
        if figures[0].get('data-synthetic-likeness')=='public-figure':
            sensitive=figures[0].get('data-sensitive-context')
            if sensitive not in ('true','false'): errors.append(f'classificazione sensibilità figura assente: {p.name}')
            if sensitive=='true':
                if figures[0].get('data-portrait-format')!='neutral-isolated': errors.append(f'formato ritratto sensibile non dichiarato: {p.name}')
                alt=' '.join(figures[0].xpath('.//img/@alt')).lower()
                if 'ritratto editoriale neutrale' not in alt: errors.append(f'alt sensibile non descrive ritratto neutrale: {p.name}')
    robots=' '.join(d.xpath('//meta[@name="robots"]/@content')).lower()
    if 'noindex' not in robots and len(d.xpath('//div[contains(@class,"art-sources")]//a[@href]'))<2:
        errors.append(f'meno di due fonti nell’articolo indicizzabile: {p.name}')
    if 'noindex' in robots and d.xpath('//script[contains(@src,"pagead2.googlesyndication.com")]'):
        errors.append(f'pubblicità presente in articolo noindex: {p.name}')
    def related_key(value):
        value=unquote(urlparse(value or '').path).rstrip('/')
        if value.endswith('/index.html'): value=value[:-11]
        if value.endswith('.html'): value=value[:-5]
        return value
    canonical=d.xpath('//link[@rel="canonical"]/@href')
    current_key=related_key(canonical[0] if canonical else f'/notizie/{p.name}')
    current_title=' '.join(d.xpath('//main[contains(@class,"wrap")]//h1[1]//text()')).strip().casefold()
    for link in d.xpath('//section[contains(@class,"curio-related") or contains(@class,"cm-related")]//a[@href]'):
        linked_title=' '.join(link.xpath('.//strong//text()')).strip().casefold()
        if related_key(link.get('href'))==current_key or (current_title and linked_title==current_title):
            errors.append(f'articolo autoreferenziale in Potrebbe interessarti: {p.name}')
    scripts=d.xpath('//script[contains(@src,"curiomondo-article-v210.js")]/@src')
    if scripts and not any(re.search(r'[?&]v=\d+(?:&|$)', value) for value in scripts):
        errors.append(f'cache correlati senza versione numerica: {p.name}')
for url,count in Counter(refs).items():
    if count>1: errors.append(f'immagine articolo duplicata ({count}): {url}')

home=html.fromstring((root/'index.html').read_text(errors='replace'))
if home.xpath('//footer//*[contains(concat(" ",normalize-space(@class)," ")," cm-nicaise-signature ")]'): errors.append('firma Nicaise ancora presente nel footer home')
for selector,label in [('//div[contains(@class,"auto-rail")]//img/@src','Ultime notizie'),('//div[@id="cards"]//img/@src','Tutte le notizie')]:
    section_refs=home.xpath(selector)
    if len(section_refs)!=len(set(section_refs)): errors.append(f'immagini duplicate in {label}')
if len(home.xpath('//nav[contains(@class,"ticker-track")][1]/a'))!=10: errors.append('LIVE non contiene 10 notizie')
if len(home.xpath('//div[contains(@class,"auto-rail")]/a'))!=5: errors.append('Ultime notizie non contiene 5 articoli')
if len(home.xpath('//div[contains(@class,"auto-rail")]/a/h3 | //div[contains(@class,"auto-rail")]/a//h3'))!=5: errors.append('titoli mancanti nelle card Ultime notizie')
if len(home.xpath('//div[contains(@class,"auto-rail")]/a//p[normalize-space()]'))!=5: errors.append('spiegazioni iniziali mancanti nelle card Ultime notizie')
if len(home.xpath('//div[@id="cards"]/a//h3[normalize-space()]'))<12: errors.append('titoli mancanti nelle card Tutte le notizie')
if len(home.xpath('//div[@id="cards"]/a//p[normalize-space()]'))<12: errors.append('spiegazioni iniziali mancanti nelle card Tutte le notizie')
if len(home.xpath('//a[contains(@class,"featured")]'))!=1: errors.append('apertura principale non unica')
if len(home.xpath('//section[contains(@class,"cm-home-deep-links")]//a'))!=3: errors.append('approfondimenti home non sono 3')
if 'home-original-v101' in (root/'index.html').read_text(): errors.append('runtime home legacy ancora attivo')
if not (root/'llms.txt').exists(): errors.append('llms.txt assente')
else:
    llms=(root/'llms.txt').read_text(errors='replace')
    if not re.search(r'(?m)^#\s+\S',llms): errors.append('llms.txt senza H1 Markdown')
    if not re.search(r'\[[^\]]+\]\(https://[^)]+\)',llms): errors.append('llms.txt senza link Markdown')

for p in (root/'assets/js').glob('*-v210.js'):
    r=subprocess.run(['node','--check',str(p)],capture_output=True,text=True)
    if r.returncode: errors.append(f'JavaScript non valido: {p.name}')
zeros=[p for p in root.rglob('*') if p.is_file() and p.suffix.lower() in {'.webp','.avif','.png','.jpg','.jpeg'} and p.stat().st_size==0 and 'IA-WORKSPACE' not in p.relative_to(root).parts]
if zeros: errors.append(f'{len(zeros)} file immagine vuoti')

# Daily editorial cycle v263: mystery card, reflection, ebook and two queued guides.
daily_slug='siamo-responsabili-anche-delle-conseguenze-che-non-potevamo-prevedere'
daily_path=root/'domanda-del-giorno'/daily_slug/'index.html'
book_path=root/'biblioteca/vita-relazioni/domande-per-conoscersi'/daily_slug/'index.html'
guide_paths=[
    root/'biblioteca/tecnologia-ai/smartphone-computer/come-recuperare-password-gmail-facebook-instagram-wifi/index.html',
    root/'biblioteca/tecnologia-ai/smartphone-computer/come-installare-app-android-iphone/index.html',
]
qday=home.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cm-qday ")]')
if len(qday)!=1: errors.append('card Domanda del giorno v255 assente o duplicata')
elif not qday[0].xpath('.//a[contains(concat(" ",normalize-space(@class)," ")," cm-qday-link ")]//*[contains(concat(" ",normalize-space(@class)," ")," cm-qday-card ")]//*[contains(concat(" ",normalize-space(@class)," ")," cm-qday-hint ")]'):
    errors.append('struttura mystery card v255 incompleta')
if daily_path.exists():
    daily=html.fromstring(daily_path.read_text(errors='replace'))
    if daily.xpath('//h2|//h3'): errors.append('Domanda del giorno v255 contiene H2/H3 vietati')
    answer=' '.join(daily.xpath('//article[contains(concat(" ",normalize-space(@class)," ")," q-flow ")]/p[not(contains(@class,"q-sign"))]//text()'))
    if not 1000<=len(re.sub(r'\s+',' ',answer).strip())<=3000: errors.append('risposta Domanda del giorno v255 fuori 1000–3000 caratteri')
else: errors.append('pagina Domanda del giorno v255 assente')
if book_path.exists():
    book=html.fromstring(book_path.read_text(errors='replace'))
    pages=book.xpath('//*[@data-book-page]')
    book_text=re.sub(r'\s+',' ',' '.join(book.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," cm-book-stage ")]//p//text()'))).strip()
    if not 8<=len(pages)<=14: errors.append('eBook v255 fuori 8–14 pagine')
    if not 15000<=len(book_text)<=30000: errors.append(f'eBook v255 fuori 15000–30000 caratteri ({len(book_text)})')
    if len(book.xpath('//h2'))>7: errors.append('eBook v255 supera 7 H2')
    if len(book.xpath('//button[@data-book-prev]'))!=1 or len(book.xpath('//button[@data-book-next]'))!=1: errors.append('controlli eBook v255 non conformi')
else: errors.append('eBook v255 assente')
for guide_path in guide_paths:
    if not guide_path.exists(): errors.append(f'guida giornaliera v255 assente: {guide_path.parent.name}'); continue
    guide=html.fromstring(guide_path.read_text(errors='replace'))
    visible=re.sub(r'\s+',' ',' '.join(guide.xpath('//main//article//text()'))).strip()
    if not 3000<=len(visible)<=15000: errors.append(f'guida v255 fuori 3000–15000 caratteri: {guide_path.parent.name} ({len(visible)})')
report={'version':263,'html':len(html_files),'articles':len(news),'articleImages':len(refs),'errors':errors}
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(1 if errors else 0)
