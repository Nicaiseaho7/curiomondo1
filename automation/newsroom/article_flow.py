"""Layout CurioMondo per le notizie. Nessun accesso alla rete."""
from __future__ import annotations
from collections import defaultdict
from functools import lru_cache
from pathlib import Path
from urllib.parse import unquote, urlsplit
from datetime import datetime, timezone
import json, re, unicodedata
from lxml import html, etree

CANONICAL_HOSTS = {'', 'curiomondo.it', 'www.curiomondo.it'}
NEWS = re.compile(r'^/notizie/([a-zA-Z0-9][a-zA-Z0-9_-]+)(?:\.html|/index\.html|/)?$')
IMAGE = re.compile(r'^/assets/images/[a-zA-Z0-9_./-]+\.(?:webp|avif|jpg|jpeg|png)$', re.I)
CSS = '/assets/css/curiomondo-article-flow-v1.css'
SCRIPT_VERSION = '1691'
EXAMPLE = 'umbria-allerta-332-vento-frane-27-novembre-2026'
EXAMPLE_BRIEF = [
    ('Venerdì', 'Rovesci soprattutto a est. Rischio idrogeologico nelle zone A, C e D.'),
    ('Da mezzanotte', 'L’allerta gialla riguarda il vento. Possibili raffiche forti sull’Appennino.')
]
EXAMPLE_BOLD = ['zone A, C e D', 'codice giallo per il rischio idrogeologico',
                'venti forti da nord', 'avvisi aggiornati del proprio Comune']
STOP = frozenset('della delle degli nello nella dalla nelle alla alle oggi domani venerdi lunedi sabato novembre ottobre settembre dicembre curiomondo notizia dopo sono prima anche questo queste degli degli'.split())

def tokens(text):
    normalized = unicodedata.normalize('NFKD', str(text or '').casefold())
    plain = ''.join(c for c in normalized if not unicodedata.combining(c))
    return {s for s in re.findall('[a-z0-9]{4,}', plain) if s not in STOP}

def key(value):
    u = urlsplit(str(value or ''))
    if u.netloc not in CANONICAL_HOSTS or u.scheme not in ('', 'https', 'http'):
        return ''
    m = NEWS.fullmatch('/' + unquote(u.path).lstrip('/'))
    return m.group(1).lower() if m and m.group(1).lower() != 'index' else ''

def image_path(value):
    u = urlsplit(str(value or ''))
    if u.netloc not in CANONICAL_HOSTS or u.scheme not in ('', 'https', 'http'):
        return ''
    p = '/' + u.path.lstrip('/')
    return p if IMAGE.fullmatch(p) and '..' not in p.split('/') else ''

class Catalog:
    def __init__(self, root, rows):
        self.root = root
        self.lookup, self.categories, self.latest = {}, defaultdict(list), []
        now = datetime.now(timezone.utc)
        for row in sorted(rows, key=lambda r: str(r.get('dateISO') or ''), reverse=True):
            slug = key(row.get('url'))
            cover = image_path(row.get('image'))
            title = ' '.join(str(row.get('title') or '').split())
            published = str(row.get('firstPublishedAt') or row.get('dateISO') or '')
            try:
                date = datetime.fromisoformat(published.replace('Z','+00:00'))
                if date.tzinfo is None or date > now:
                    continue
            except ValueError:
                continue
            if not slug or slug in self.lookup or not cover or not title:
                continue
            target = next((p for p in (root/'notizie'/f'{slug}.html', root/'notizie'/slug/'index.html') if p.is_file()), None)
            if not target or not (root/cover[1:]).is_file():
                continue
            if (root/cover[1:]).stat().st_size == 0:
                continue
            thumb = re.sub(r'-\d+w?(?=\.[^.]+$)', '-480', cover)
            if thumb == cover or not (root/thumb[1:]).is_file():
                thumb = cover
            category = ' '.join(str(row.get('section') or 'Notizie').split())
            item = dict(key=slug, url='/' + target.relative_to(root).as_posix(),
                        image=thumb, imagekey=re.sub(r'-\d+w?(?=\.[^.]+$)', '', cover),
                        title=title, titlekey=' '.join(sorted(tokens(title))),
                        category=category, terms=tokens(title + ' ' + str(row.get('excerpt') or '')))
            self.lookup[slug] = item
            self.categories[category.casefold()].append(item)
            self.latest.append(item)

    def choose(self, slug, title, category, explicit):
        seen, titles, seen_images, selected = {slug}, {' '.join(sorted(tokens(title)))}, set(), []
        current = self.lookup.get(slug)
        if current: seen_images.add(current['imagekey'])
        def add(item):
            if not item or item['key'] in seen or item['titlekey'] in titles or item['imagekey'] in seen_images:
                return
            seen.add(item['key']); titles.add(item['titlekey']); seen_images.add(item['imagekey']); selected.append(item)
        for url in explicit:
            add(self.lookup.get(key(url)))
            if len(selected) == 3: return selected
        words = tokens(title)
        name = category.casefold()
        same = self.categories.get(name, [])
        mixed = [item for cat, rows in self.categories.items() if cat != name and name in cat.split(' / ') for item in rows[:100]]
        for pool in (same[:250] + mixed, self.latest[:500]):
            for i in sorted(pool, key=lambda item: len(words & item['terms']), reverse=True):
                add(i)
                if len(selected) == 3: return selected
        for i in self.latest:
            add(i)
            if len(selected) == 3: return selected
        raise ValueError('servono tre altre notizie distinte e già pubblicate con le proprie immagini')

@lru_cache(maxsize=3)
def _catalog(root_text, stamp):
    root = Path(root_text)
    rows = json.loads((root/'assets/data/home-feed-v210.json').read_text(encoding='utf-8'))['items']
    return Catalog(root, rows)

def load_catalog(root):
    root = root.resolve()
    return _catalog(str(root), (root/'assets/data/home-feed-v210.json').stat().st_mtime_ns)

def has(node, name):
    return name in (node.get('class') or '').split()

def block(parent, names, tag=None):
    for node in parent:
        if (not tag or node.tag == tag) and any(has(node, n) for n in names):
            return node
    return None

def text(node, value=None):
    if value is not None: node.text = value
    return node

def elem(tag, cls='', value=None, **attrs):
    if cls: attrs['class'] = cls
    return text(etree.Element(tag, **attrs), value)

def highlight(article, phrases):
    for phrase in list(dict.fromkeys(phrases))[:6]:
        if not isinstance(phrase, str) or not 3 <= len(phrase.strip()) <= 95: continue
        for p in article.xpath('./p'):
            if len(p.xpath('.//strong|.//b')) >= 2:
                continue
            fragments = [segment for segment in p.xpath('./text()') if phrase in segment]
            if not fragments:
                continue
            fragment = fragments[0]
            before, after = str(fragment).split(phrase, 1)
            strong = elem('strong', value=phrase); strong.tail = after
            if fragment.is_tail:
                owner = fragment.getparent()
                owner.tail = before
                owner.addnext(strong)
            else:
                p.text = before
                p.insert(0, strong)
            break

def continuous_prose(article):
    # Conserva testo e ancore dei vecchi titoletti fattuali, senza mostrare
    # un'etichetta in una riga isolata. I riquadri/tabelle strutturati restano intatti.
    generic = {'in sintesi','attenzione','il contesto','i fatti verificati','i prossimi passaggi',
               'cosa sappiamo','il punto','le conseguenze per l’europa'}
    for h in list(article.xpath('./h2|./h3|./h4|./h5|./h6')):
        if len(h) or not h.text or set(h.attrib) - {'id', 'class'}:
            continue
        nxt = h.getnext()
        if nxt is None or nxt.tag != 'p':
            continue
        label = h.text.strip()
        if h.get('id'):
            nxt.insert(0, etree.Element('span', id=h.get('id')))
        if label and label.casefold() not in generic and not label.casefold().startswith(('che cosa ', 'cosa cambia', 'come misurare')):
            piece = elem('strong', value=label)
            piece.tail = (' ' if label.endswith((':', '.', '!', '?')) else '. ') + (nxt.text or '')
            nxt.text = ''
            nxt.insert(1 if h.get('id') else 0, piece)
        article.remove(h)

def brief_rows(panel):
    if panel is None: return []
    items=[]
    for row in panel.xpath('./div/div'):
        values=[' '.join(' '.join(n.itertext()).split()) for n in row]
        if len(values)>=2 and values[0] and values[1]:
            items.append((values[0],values[1]))
    return items[:3]

def make_brief(rows):
    sec=elem('aside','cm-flow-brief', **{'aria-label':'In breve'})
    sec.append(elem('h2',value='In breve'))
    dl=elem('dl')
    for label, value in rows:
        cell=elem('div')
        cell.extend([elem('dt',value=label),elem('dd',value=value)])
        dl.append(cell)
    sec.append(dl)
    return sec

def transform(page, catalog, *, fallback_url='', bold=()):
    doc = html.document_fromstring(page, parser=html.HTMLParser(encoding='utf-8'))
    body = doc.find('body')
    main = (doc.xpath('//main[contains(concat(" ",normalize-space(@class)," ")," wrap ")][.//article[contains(concat(" ",normalize-space(@class)," ")," art-body ")]]') or [None])[0]
    canonical = (doc.xpath('//link[@rel="canonical"]/@href') or [fallback_url])[0]
    slug = key(canonical)
    if body is None or main is None or not slug:
        return page, False
    if has(body, 'cm-news-flow-article'):
        section = block(main, ('curio-related','cm-related'))
        if section is not None:
            links=section.xpath('.//a[.//img and .//strong]/@href')
            keys=[key(x) for x in links]
            if len(links)==3 and all(keys) and len(set(keys))==3 and slug not in keys:
                return page, False
        raise ValueError(f'{slug}: anteprima già migrata ma tre correlate valide assenti')
    h1=next((n for n in main if n.tag=='h1'), None)
    article=block(main, ('art-body',),'article')
    photo=block(main, ('article-image',),'figure')
    if h1 is None or article is None or photo is None:
        raise ValueError(f'{slug}: struttura articolo non riconosciuta')
    title = ' '.join(''.join(h1.itertext()).split())
    badge=block(main, ('badge',))
    category=' '.join(''.join(badge.itertext()).split()) if badge is not None else 'Notizie'
    old=block(main, ('curio-related','cm-related'))
    explicit=old.xpath('.//a/@href') if old is not None else []
    selected=catalog.choose(slug,title,category,explicit)
    # Conserva i riferimenti esistenti, il titolo dell'articolo, i parametri degli annunci e lo schema.
    stylesheet=etree.Element('link',rel='stylesheet',href=CSS)
    doc.find('head').append(stylesheet)
    classes=(body.get('class') or '').split()+['cm-news-flow-article']
    body.set('class',' '.join(classes))
    for script in doc.xpath('//script[contains(@src,"curiomondo-article-v210.js")]'):
        script.set('src',re.sub(r'\?.*$', '', script.get('src'))+'?v='+SCRIPT_VERSION)
    brand=doc.xpath('//a[contains(concat(" ",normalize-space(@class)," ")," cm-global-header__brand ")]/span')
    if brand and brand[0].text=='Curio':
        brand[0].text=None
        brand[0].insert(0,elem('b','cm-flow-curio','Curio'))
    bar=elem('div','cm-flow-progress',**{'aria-hidden':'true'})
    bar.append(elem('span','cm-reading-progress'))
    if not doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," cm-reading-progress ")]'):
        body.insert(0,bar)
    actions=block(main, ('actions',))
    at=block(main, ('meta',))
    author=block(main, ('cm-article-byline',))
    if actions is not None and at is not None and author is not None and at.getnext() is author and author.getnext() is actions:
        meta=elem('div','cm-flow-meta-row')
        attribution=elem('div','cm-flow-attribution')
        logo=etree.Element('img',src='/assets/images/curiomondo-logo-circle-v715-96.webp?v=715',
                            alt='',width='36',height='36')
        texts=elem('div')
        main.insert(main.index(at),meta)
        texts.append(author);texts.append(at)
        attribution.extend([logo,texts]);meta.extend([attribution,actions])
    photo_next=photo.getnext()
    panel=photo_next if photo_next is not None and any(has(photo_next,n) for n in ('cm-insight','cm-data-cube')) else None
    rows=EXAMPLE_BRIEF if slug==EXAMPLE else brief_rows(panel)
    if rows:
        media=elem('div','cm-flow-media')
        main.insert(main.index(photo),media)
        media.extend([photo,make_brief(rows)])
        if panel is not None and panel.getparent() is main and not panel.xpath('.//a|.//iframe|.//script'):
            main.remove(panel)
    continuous_prose(article)
    highlight(article,EXAMPLE_BOLD if slug==EXAMPLE else bold)
    section=elem('section','curio-related',**{'data-cm-flow-static':'true','aria-label':'Altre notizie'})
    section.append(elem('h2',value='Altre notizie'))
    grid=elem('div','curio-related-grid')
    for item in selected:
        link=elem('a',href=item['url'])
        thumb=elem('span','curio-related-thumb')
        thumb.append(etree.Element('img',src=item['image'],alt='',width='400',height='225',loading='lazy',decoding='async'))
        copy=elem('span','curio-related-copy')
        copy.extend([elem('small',value=item['category']),elem('strong',value=item['title'])])
        link.extend([thumb,copy]);grid.append(link)
    section.append(grid)
    if old is not None: main.replace(old,section)
    else: main.append(section)
    return html.tostring(doc, encoding='unicode',method='html',doctype='<!doctype html>'), True
