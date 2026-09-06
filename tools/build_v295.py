from pathlib import Path
from lxml import html, etree
import json

ROOT=Path(__file__).resolve().parents[1]
VERSION=295
OLD='chi-siamo-nei-cinque-minuti-prima-di-addormentarci-quando-cadono-le-maschere-utili'
NEW='cosa-faremmo-se-il-tempo-tornasse-indietro-di-dieci-anni-sapendo-cio-che-sappiamo-ora'
OLD_Q=f'/domanda-del-giorno/{OLD}/'
OLD_B=f'/biblioteca/vita-relazioni/domande-per-conoscersi/{OLD}/'
NEW_Q=f'/domanda-del-giorno/{NEW}/'
NEW_B=f'/biblioteca/vita-relazioni/domande-per-conoscersi/{NEW}/'

for rel in (f'domanda-del-giorno/{NEW}/index.html',f'biblioteca/vita-relazioni/domande-per-conoscersi/{NEW}/index.html'):
    p=ROOT/rel
    s=p.read_text(encoding='utf-8').replace('6 settembre 2026','7 settembre 2026').replace('2026-09-06','2026-09-07')
    p.write_text(s,encoding='utf-8')

p=ROOT/'index.html'; s=p.read_text(encoding='utf-8')
s=s.replace('Scopri la Domanda del giorno del 6 settembre 2026','Scopri la Domanda del giorno del 7 settembre 2026')
s=s.replace('<time class="cm-qday-date" datetime="2026-09-06"><strong>06</strong><span>SET · 2026</span></time>','<time class="cm-qday-date" datetime="2026-09-07"><strong>07</strong><span>SET · 2026</span></time>')
s=s.replace('home-bundle-v291.css?v=294','home-bundle-v291.css?v=295')
p.write_text(s,encoding='utf-8')

p=ROOT/'domanda-del-giorno/index.html'; d=html.fromstring(p.read_text(encoding='utf-8')); grid=d.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cb-subgrid ")]')[0]
first=grid.xpath('./a')[0]; first.xpath('.//span')[0].text='7 settembre 2026'
old_card=html.fragment_fromstring(f'<a class="cb-subcard" href="{OLD_Q}"><span class="cb-kicker">6 settembre 2026</span><h2>Chi siamo nei cinque minuti prima di addormentarci, quando cadono le maschere utili?</h2><p>Una riflessione su ciò che resta di noi quando i ruoli della giornata si allentano, prima del sonno.</p><b>Leggi →</b></a>')
for a in grid.xpath(f'./a[@href="{OLD_Q}"]'): grid.remove(a)
grid.insert(1,old_card); p.write_text('<!doctype html>'+html.tostring(d,encoding='unicode',method='html'),encoding='utf-8')

p=ROOT/'biblioteca/vita-relazioni/domande-per-conoscersi/index.html'; d=html.fromstring(p.read_text(encoding='utf-8')); grid=d.xpath('//section[contains(concat(" ",normalize-space(@class)," ")," cb-subgrid ")]')[0]
first=grid.xpath('./a')[0]; first.xpath('.//span')[0].text='7 settembre 2026 · eBook'
old_card=html.fragment_fromstring(f'<a class="cb-subcard" href="{OLD_B}"><span class="cb-kicker">6 settembre 2026 · eBook</span><h2>La voce che resta quando le maschere si tolgono</h2><p>Maschere utili, autenticità e pensieri notturni: come distinguere un bisogno reale dal rumore della stanchezza.</p><b>Sfoglia →</b></a>')
for a in grid.xpath(f'./a[@href="{OLD_B}"]'): grid.remove(a)
grid.insert(1,old_card); p.write_text('<!doctype html>'+html.tostring(d,encoding='unicode',method='html'),encoding='utf-8')

p=ROOT/'assets/data/search-index-v210.json'; data=json.loads(p.read_text(encoding='utf-8'))
old_items=[
 {'title':'Chi siamo nei cinque minuti prima di addormentarci, quando cadono le maschere utili?','excerpt':'Una riflessione su ciò che resta di noi quando i ruoli della giornata si allentano, prima del sonno.','url':OLD_Q,'section':'Domanda del giorno'},
 {'title':'La voce che resta quando le maschere si tolgono','excerpt':'Maschere utili, autenticità e pensieri notturni: come distinguere un bisogno reale dal rumore della stanchezza.','url':OLD_B,'section':'Biblioteca · Vita e relazioni'}]
data['items']=[x for x in data['items'] if x.get('url') not in {OLD_Q,OLD_B}]
data['items'][2:2]=old_items
data['version']=VERSION
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for rel in ('assets/data/home-feed-v210.json','assets/data/editorial-images-v210.json'):
    p=ROOT/rel; data=json.loads(p.read_text(encoding='utf-8')); data['version']=VERSION; p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

p=ROOT/'sitemap.xml'; tree=etree.parse(str(p)); ns='http://www.sitemaps.org/schemas/sitemap/0.9'
root=tree.getroot(); existing={x.text for x in root.findall(f'{{{ns}}}url/{{{ns}}}loc')}
for url,lastmod in [(f'https://curiomondo.it{OLD_Q}','2026-09-06'),(f'https://curiomondo.it{OLD_B}','2026-09-06')]:
    if url not in existing:
        node=etree.Element(f'{{{ns}}}url'); etree.SubElement(node,f'{{{ns}}}loc').text=url; etree.SubElement(node,f'{{{ns}}}lastmod').text=lastmod; root.insert(1,node)
for node in root.findall(f'{{{ns}}}url'):
    loc=node.find(f'{{{ns}}}loc')
    if loc is not None and loc.text in {f'https://curiomondo.it{NEW_Q}',f'https://curiomondo.it{NEW_B}'}:
        lm=node.find(f'{{{ns}}}lastmod')
        if lm is None: lm=etree.SubElement(node,f'{{{ns}}}lastmod')
        lm.text='2026-09-07'
tree.write(str(p),encoding='utf-8',xml_declaration=True,pretty_print=True)

p=ROOT/'notizie/laquila-monumenti-lego-maurizio-lampis-collemaggio-6-settembre-2026.html'; s=p.read_text(encoding='utf-8').replace(NEW_Q,OLD_Q).replace('Cosa faremmo tornando indietro di dieci anni?','Chi siamo quando cadono le maschere utili?'); p.write_text(s,encoding='utf-8')

p=ROOT/'curiomondo-site-manifest.json'; m=json.loads(p.read_text(encoding='utf-8')); m['site']['current_site_version']=VERSION; m['site']['site_version']=VERSION; m['daily_state']['last_question_date']='2026-09-07'; m['daily_state']['timezone']='Europe/Rome'; m['daily_state']['date_source']='current_datetime_in_Europe_Rome_never_UTC'; p.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

p=ROOT/'CURIO-MONDO-PROTOCOLLO-MAESTRO.md'; s=p.read_text(encoding='utf-8')
tick=chr(96)
needle='Prima di creare una nuova versione, confronta la data corrente con '+tick+'daily_state.last_question_date'+tick+' nel manifest.'
addition='\n\nLa data corrente deve essere calcolata **sempre nel fuso '+tick+'Europe/Rome'+tick+'**, compreso il passaggio all’ora legale. Non usare UTC, il fuso del server o una data fissata manualmente. Dopo la mezzanotte italiana la nuova data deve propagarsi automaticamente a homepage, pagina dedicata, eBook, archivi, ricerca, sitemap e '+tick+'daily_state.last_question_date'+tick+'.'
if addition.strip() not in s: s=s.replace(needle,needle+addition)
p.write_text(s,encoding='utf-8')

print(json.dumps({'status':'ok','version':VERSION,'date':'2026-09-07','timezone':'Europe/Rome'},ensure_ascii=False))
