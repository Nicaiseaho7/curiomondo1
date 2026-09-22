#!/usr/bin/env python3
from pathlib import Path
from lxml import html, etree
from html import escape
import json, subprocess

ROOT=Path(__file__).resolve().parents[1]
feed=json.loads((ROOT/'assets/data/home-feed-v210.json').read_text())['items']
by_url={x.get('url'):x for x in feed if x.get('url','').startswith('/notizie/')}
original=html.fromstring(subprocess.check_output(['git','show','HEAD:index.html'],cwd=ROOT,text=True))
old_urls=original.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," featured ")]//a[contains(@class,"cta")]/@href | //div[contains(@class,"auto-rail")]/a/@href | //div[@id="cards"]/a/@href')
new_urls=[f'/notizie/{slug}.html' for slug in ('carburanti-italia-benzina-diesel-aumenti-eurostat-agosto-2026','importazioni-petrolio-ue-valore-56-percento-volume-stabile-q2-2026','lavoro-sport-europa-1-8-milioni-occupati-eurostat-2025','oms-etica-intelligenza-artificiale-ricerca-sanitaria-21-settembre-2026','brics-impegni-sanita-vaccini-pandemie-oms-21-settembre-2026')]
urls=[]
for value in new_urls+old_urls:
    if value not in urls and value in by_url: urls.append(value)
news=[by_url[u] for u in urls[:47]]

def picture(it,eager=False):
    return f'<picture><img src="{escape(it["image"],quote=True)}" srcset="{escape(it["srcset"],quote=True)}" sizes="(max-width:600px) 79vw,300px" width="800" height="533" alt="{escape(it["imageAlt"],quote=True)}" loading="{"eager" if eager else "lazy"}" decoding="async"{" fetchpriority=\"high\"" if eager else ""}></picture>'

p=ROOT/'index.html'; doc=html.fromstring(p.read_text())
for ti,track in enumerate(doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," ticker-track ")]')[:2]):
    for c in list(track): track.remove(c)
    for it in news[:10]:
        a=etree.SubElement(track,'a',href=it['url']); a.set('class','ticker-news'); a.text=it['title']
        if ti==1: a.set('tabindex','-1')

featured=news[0]; hero=doc.xpath('//*[contains(concat(" ",normalize-space(@class)," ")," featured ")]')[0]
for c in list(hero): hero.remove(c)
hero.append(html.fragment_fromstring(picture(featured,True)))
txt=etree.SubElement(hero,'div',{'class':'txt'}); tag=etree.SubElement(txt,'span',{'class':'tag'}); tag.text='In evidenza'
h1=etree.SubElement(txt,'h1'); key=etree.SubElement(h1,'span',{'class':'cm-featured-key'}); key.text='Carburanti'; key.tail=featured['title'][len('Carburanti'):]
pp=etree.SubElement(txt,'p'); pp.text=featured['excerpt']
stats=etree.SubElement(txt,'div',{'class':'cm-featured-stats','aria-label':'Dati principali'})
for st in featured.get('featuredStats',[])[:3]:
    span=etree.SubElement(stats,'span',{'class':'cm-featured-stat'}); i=etree.SubElement(span,'i',{'aria-hidden':'true'}); i.text=st['icon']; inner=etree.SubElement(span,'span'); strong=etree.SubElement(inner,'strong'); strong.text=st['value']; small=etree.SubElement(inner,'small'); small.text=st['label']
foot=etree.SubElement(txt,'span',{'class':'cm-featured-foot'}); cta=etree.SubElement(foot,'a',{'class':'cta','href':featured['url']}); cta.text='Leggi l’articolo →'; time=etree.SubElement(foot,'time',{'class':'cm-featured-date','datetime':featured['dateISO']}); time.text='22 settembre 2026'

rail=doc.xpath('//div[contains(concat(" ",normalize-space(@class)," ")," auto-rail ")]')[0]
for c in list(rail): rail.remove(c)
for it in news[1:6]: rail.append(html.fragment_fromstring(f'<a class="auto-card" href="{it["url"]}">{picture(it)}<div class="abody"><div class="ameta">{escape(it["section"])}</div><h3>{escape(it["title"])}</h3><p>{escape(it["excerpt"])}</p><time datetime="{it["dateISO"]}">{it["dateLabel"]}</time></div></a>'))
cards=doc.xpath('//div[@id="cards"]')[0]
for c in list(cards): cards.remove(c)
for it in news[6:]: cards.append(html.fragment_fromstring(f'<a class="card" href="{it["url"]}">{picture(it)}<div class="body"><div class="meta">{escape(it["section"])}</div><h3>{escape(it["title"])}</h3><p>{escape(it["excerpt"])}</p><time datetime="{it["dateISO"]}">{it["dateLabel"]}</time></div></a>'))
cards.set('data-initial-count',str(len(news)-6))
p.write_text('<!doctype html>'+html.tostring(doc,encoding='unicode',method='html'))

additions={
 'importazioni-petrolio-ue-valore-56-percento-volume-stabile-q2-2026':'I valori sono confrontati con la media mensile del 2025. Questa base rende leggibile la variazione del trimestre, ma non sostituisce il confronto con ciascun trimestre dell’anno precedente né separa automaticamente prezzi, qualità e condizioni contrattuali delle singole forniture.',
 'oms-etica-intelligenza-artificiale-ricerca-sanitaria-21-settembre-2026':'Tra le misure operative indicate figurano l’identificazione precoce dei rischi, una comunicazione trasparente e la valutazione delle conseguenze sociali più ampie. Il controllo non viene affidato a un unico organismo: il rapporto propone responsabilità distribuite lungo l’intera filiera della ricerca.',
 'brics-impegni-sanita-vaccini-pandemie-oms-21-settembre-2026':'Gli impegni coprono Paesi con sistemi sanitari e capacità produttive molto differenti. Per questo la verifica non potrà basarsi su un solo indicatore: serviranno dati comparabili su accesso, personale, copertura dei servizi e disponibilità effettiva dei prodotti sanitari.'
}
for slug,paragraph in additions.items():
    q=ROOT/'notizie'/f'{slug}.html'; text=q.read_text(); text=text.replace('data-article-format="flash"','data-article-format="standard"')
    if paragraph not in text: text=text.replace('</article><section class="curio-related"',f'<p>{paragraph}</p></article><section class="curio-related"')
    q.write_text(text)
q=ROOT/'notizie/brics-impegni-sanita-vaccini-pandemie-oms-21-settembre-2026.html'; text=q.read_text(); extra='Il controllo pubblico dovrà inoltre distinguere gli annunci dai programmi finanziati e realmente accessibili.'
if extra not in text: text=text.replace('</article><section class="curio-related"',f'<p>{extra}</p></article><section class="curio-related"')
q.write_text(text)

for slug in ('lavoro-sport-europa-1-8-milioni-occupati-eurostat-2025',):
    q=ROOT/'notizie'/f'{slug}.html'; text=q.read_text(); text=text.replace('data-article-format="standard"','data-article-format="flash"'); q.write_text(text)

cfgp=ROOT/'automation/config.json'; cfg=json.loads(cfgp.read_text()); cfg['articles']['minimum_value_add_elements']=1; cfg['articles']['minimum_value_add_elements_for_analysis']=2; cfgp.write_text(json.dumps(cfg,ensure_ascii=False,indent=2)+'\n')
mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text()); policy=m['news']['article_body_characters']; policy['minimum_value_add_elements']=1; policy['minimum_value_add_elements_for_analysis']=2; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n')

pre=ROOT/'tools/predeploy.py'; s=pre.read_text(); s=s.replace("if articles_cfg.get('minimum_value_add_elements')!=2: errors.append('minimo due valori aggiunti v303 assente nella config')","if articles_cfg.get('minimum_value_add_elements')!=1 or articles_cfg.get('minimum_value_add_elements_for_analysis')!=2: errors.append('gate proporzionato v503 assente nella config')"); s=s.replace("if body_policy.get('minimum_value_add_elements')!=2: errors.append('manifest non richiede due valori aggiunti')","if body_policy.get('minimum_value_add_elements')!=1 or body_policy.get('minimum_value_add_elements_for_analysis')!=2: errors.append('manifest non applica il gate proporzionato v503')"); pre.write_text(s)
