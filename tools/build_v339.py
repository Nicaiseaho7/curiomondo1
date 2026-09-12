#!/usr/bin/env python3
from pathlib import Path
from html import escape
import hashlib, json, runpy

ROOT = Path(__file__).resolve().parents[1]
VERSION = 339
CAPTION = "Illustrazione editoriale CurioMondo generata con IA per rappresentare questa notizia; non è una fotografia documentaria."
ARTICLES = [
{
"slug":"ucraina-attacchi-sei-morti-decine-feriti-12-settembre-2026",
"title":"Ucraina, attacchi in più regioni: almeno sei morti e decine di feriti",
"excerpt":"Missili e droni colpiscono abitazioni e infrastrutture da Žytomyr a Zaporižžja. I bilanci locali restano provvisori e le rivendicazioni militari delle parti non sono verificabili in modo indipendente.",
"published":"2026-09-12T22:15:00+02:00","category":"Mondo / Ucraina / Guerra","place":"Kyiv","key":"ucraina-attacchi-regioni-ai-openai-v339",
"alt":"Scena editoriale sensibile generata con IA di edifici danneggiati in una città ucraina con soccorritori al lavoro, senza vittime visibili",
"sensitive":True,
"body":[
"Almeno sei civili sono morti e decine sono rimasti feriti sabato 12 settembre in una serie di attacchi russi contro diverse regioni dell’Ucraina. Le autorità locali hanno segnalato vittime a Zvjahel, Zaporižžja e Kryvyj Rih, oltre a gravi danni nell’area di Odessa. Il bilancio è provvisorio e può cambiare con il proseguire delle ricerche.",
"Nella regione di Žytomyr, il governatore Vitaliy Bunechko ha riferito che un attacco ha colpito un negozio a Zvjahel, uccidendo due persone. Sono stati segnalati danni anche a due distributori e a un’impresa con investimenti esteri. A Zaporižžja, secondo il governatore Ivan Fedorov, due persone sono morte e undici sono rimaste ferite.",
"A Kryvyj Rih le autorità municipali hanno comunicato altri due decessi dopo attacchi con droni e missili. Nell’area di Odessa il governatore Oleh Kiper ha indicato decine di feriti, tra cui un neonato, e due dispersi. Associated Press ha riportato un bilancio nazionale più alto includendo ulteriori vittime locali; la differenza mostra che i conteggi non erano ancora consolidati.",
"Mosca ha dichiarato di avere colpito impianti industriali e navi cargo utilizzate a fini militari. Kyiv ha invece annunciato un attacco contro uno stabilimento di gomma sintetica a Togliatti, in Russia. Reuters non ha potuto verificare autonomamente le rivendicazioni delle due parti: vengono quindi riportate come dichiarazioni, non come fatti accertati.",
"Il dato utile per leggere l’evoluzione è la distribuzione geografica degli attacchi. Le segnalazioni coinvolgono aree del nord, del centro, del sud e dell’est, indicando un’operazione estesa e non un singolo episodio locale. Questo aumenta la pressione sui sistemi di difesa aerea e sui soccorsi, chiamati a intervenire contemporaneamente in territori lontani.",
"I bilanci di guerra raccolti nelle prime ore hanno limiti precisi. Possono sovrapporre comunicazioni emesse in momenti diversi, includere dispersi ritrovati successivamente o cambiare dopo l’accesso dei soccorritori agli edifici. CurioMondo aggiornerà questa pagina solo con variazioni sostanziali attribuite ad autorità identificabili o a più fonti indipendenti.",
"Restano distinti il danno civile verificabile e gli obiettivi militari rivendicati. Fotografie geolocalizzate, immagini satellitari e accesso indipendente potrebbero chiarire alcuni episodi, ma al momento non consentono una ricostruzione completa. Le informazioni confermate riguardano soprattutto vittime, feriti e danni comunicati dalle amministrazioni regionali ucraine."
],
"sources":[
["https://www.reuters.com/world/europe/russian-attacks-kill-six-injure-dozens-ukraine-moscow-says-it-hits-ships-plants-2026-09-12/","Reuters — 12 settembre 2026 — bilanci regionali, danni e rivendicazioni delle parti"],
["https://apnews.com/article/839f5b0fc5217afc4cb34e15b01b6eff","Associated Press — 12 settembre 2026 — vittime, feriti e quadro degli attacchi"],
["https://t.me/s/V_Zelenskiy_official?before=5443","Presidenza dell’Ucraina — 12 settembre 2026 — elenco delle regioni interessate e risposta della difesa aerea"],
["https://www.rte.ie/news/2026/0912/1591278-ukraine/","RTÉ — 12 settembre 2026 — conferma indipendente dei bilanci locali"]]
},
{
"slug":"corea-nord-missili-balistici-wonsan-12-settembre-2026",
"title":"Corea del Nord, lanciati più missili balistici a corto raggio da Wonsan",
"excerpt":"Seul rileva più lanci verso il Mar Orientale dopo l’esercitazione trilaterale con Stati Uniti e Giappone. I vettori avrebbero percorso circa 250 chilometri.",
"published":"2026-09-12T22:05:00+02:00","category":"Mondo / Asia / Sicurezza","place":"Seul","key":"corea-nord-missili-wonsan-ai-openai-v339",
"alt":"Scena editoriale contestuale ordinaria generata con IA di lanci missilistici lontani dalla costa di Wonsan verso il mare, senza persone visibili",
"sensitive":False,
"body":[
"La Corea del Nord ha lanciato più missili balistici a corto raggio dalla zona costiera di Wonsan verso il Mar Orientale sabato 12 settembre. Lo Stato maggiore congiunto sudcoreano ha rilevato i lanci intorno alle 5:20 locali. Secondo Seul, i vettori hanno percorso circa 250 chilometri prima di cadere in mare.",
"Le forze sudcoreane hanno rafforzato la sorveglianza e dichiarato di condividere i dati con Stati Uniti e Giappone. Il Comando Indo-Pacifico statunitense ha affermato che l’episodio non ha rappresentato una minaccia immediata per il territorio americano o per gli alleati. La valutazione tecnica completa non è stata resa pubblica.",
"I lanci sono avvenuti il giorno dopo la conclusione di Freedom Edge, esercitazione di cinque giorni condotta da Corea del Sud, Stati Uniti e Giappone in acque internazionali. Pyongyang considera queste attività una provocazione e aveva annunciato contromisure. Questo collegamento temporale non dimostra però da solo la motivazione operativa dei test.",
"La distanza indicata aiuta a classificare l’episodio, ma non rivela automaticamente precisione, carico o capacità effettiva del sistema. Traiettoria, quota, velocità e punto di caduta sono necessari per un confronto tecnico più solido. Le autorità sudcoreane non hanno diffuso tutti questi dati nel primo comunicato.",
"La zona di partenza offre un altro elemento di contesto. Wonsan si trova sulla costa orientale nordcoreana e viene utilizzata con frequenza per attività missilistiche dirette verso il mare. Un lancio da quell’area riduce il rischio immediato per centri abitati stranieri, ma consente comunque ai Paesi vicini di raccogliere dati sul comportamento dei vettori.",
"È il primo lancio nordcoreano di questo tipo in circa tre settimane, secondo Associated Press e Reuters. La frequenza dei test è un indicatore della pressione militare nella penisola, ma ogni episodio va separato dalle dichiarazioni politiche e dalle stime sull’arsenale nucleare, che richiedono informazioni differenti.",
"Per valutare i prossimi sviluppi conteranno eventuali nuovi lanci, le analisi di Seul e Tokyo e una comunicazione ufficiale nordcoreana sul tipo di missile. CurioMondo non attribuisce al test obiettivi non dichiarati e non presenta come certa una risposta militare futura."
],
"sources":[
["https://en.yna.co.kr/view/AEN20260912000352315","Yonhap — 12 settembre 2026 — comunicato dello Stato maggiore congiunto sudcoreano, orario e area dei lanci"],
["https://apnews.com/article/ccf51bb9cd9abfda6c0b0f36c4b639e1","Associated Press — 12 settembre 2026 — distanza, contesto dell’esercitazione e valutazione statunitense"],
["https://www.reuters.com/world/asia-pacific/north-korea-launches-unidentified-projectile-toward-east-sea-yonhap-reports-2026-09-11/","Reuters — 12 settembre 2026 — conferma indipendente dei lanci e della condivisione dati"],
["https://www.pacom.mil/Media/News/","U.S. Indo-Pacific Command — comunicazioni ufficiali sulla sicurezza regionale"]]
},
{
"slug":"brics-dichiarazione-new-delhi-medio-oriente-12-settembre-2026",
"title":"BRICS, dichiarazione comune sul Medio Oriente: appello alla massima moderazione",
"excerpt":"Iran ed Emirati Arabi Uniti sostengono il testo approvato a New Delhi. Il documento chiede protezione dei civili, sovranità degli Stati e sicurezza dei flussi commerciali ed energetici.",
"published":"2026-09-12T21:55:00+02:00","category":"Mondo / Politica / Diplomazia","place":"New Delhi","key":"brics-new-delhi-dichiarazione-ai-openai-v339",
"alt":"Scena editoriale contestuale ordinaria generata con IA di una sala del vertice BRICS a New Delhi con delegazioni e bandiere, senza incontri specifici ricostruiti",
"sensitive":False,
"body":[
"I leader dei BRICS riuniti a New Delhi hanno approvato sabato 12 settembre una dichiarazione comune che chiede massima moderazione nel conflitto mediorientale. Il testo è stato sostenuto anche da Iran ed Emirati Arabi Uniti, divisi dalla guerra regionale. Il documento invoca protezione dei civili, rispetto della sovranità e tutela dei flussi commerciali, energetici e marittimi.",
"L’intesa ha rilievo diplomatico perché Teheran e Abu Dhabi hanno accettato una formulazione condivisa durante una fase di forte tensione. A margine del vertice, il presidente iraniano Masoud Pezeshkian ha incontrato il principe ereditario di Abu Dhabi, Sheikh Khaled bin Mohamed bin Zayed. Gli uffici emiratini hanno riferito un confronto su riduzione delle tensioni e stabilità regionale.",
"La dichiarazione non introduce un cessate il fuoco né un meccanismo di applicazione. È una posizione politica costruita per consenso tra Paesi con interessi diversi. La sua efficacia dipenderà da negoziati successivi, decisioni nazionali e coinvolgimento degli attori militari che non appartengono al gruppo.",
"Il vertice riunisce undici membri e rappresenta oltre il 40% della popolazione mondiale. Questa quota descrive il peso demografico, non un’identità politica uniforme. Il gruppo comprende economie, alleanze e sistemi istituzionali differenti; ottenere un testo comune è quindi un segnale di coordinamento, ma non prova una strategia estera unica.",
"Il documento affronta anche riforma delle istituzioni multilaterali, commercio, energia e sviluppo. I membri chiedono più rappresentanza per i Paesi emergenti nelle strutture globali e sostengono catene di approvvigionamento resilienti. Sul clima riconoscono che i combustibili fossili manterranno un ruolo, accompagnando l’impegno a ridurre le emissioni secondo condizioni nazionali differenti.",
"L’India ospitante punta a trasformare il consenso del gruppo in risultati concreti. Il passaggio verificabile sarà osservare se alle dichiarazioni seguiranno iniziative diplomatiche, accordi economici o proposte formali nelle organizzazioni internazionali. Senza questi atti, il valore del testo resta soprattutto politico e simbolico.",
"La Cina assumerà la presidenza dei BRICS nel 2027 e ospiterà il diciannovesimo vertice. Il cambio di presidenza offrirà il primo banco di prova sulla continuità degli impegni presi a New Delhi e sulla capacità del gruppo di mantenere una posizione comune durante l’evoluzione della crisi."
],
"sources":[
["https://ebs.publicnow.com/view/322C608779C3EE82D80D8869B7D797096FDC352E","Ufficio del Primo ministro dell’India — 12 settembre 2026 — testo integrale della Dichiarazione di New Delhi"],
["https://www.reuters.com/business/aerospace-defense/brics-agrees-joint-declaration-before-new-delhi-summit-sources-say-2026-09-12/","Reuters — 12 settembre 2026 — consenso tra Iran ed Emirati e incontri diplomatici"],
["https://www.reuters.com/world/china/chinas-xi-urges-brics-take-peacemaking-role-middle-east-war-2026-09-12/","Reuters — 12 settembre 2026 — intervento di Xi Jinping e presidenza cinese 2027"],
["https://indianexpress.com/article/business/brics-summit-new-delhi-declaration-fossil-fuels-energy-transition-critical-minerals-10875456/","Indian Express — 12 settembre 2026 — capitolo energia e transizione della dichiarazione"]]
}
]

def article(a):
    canonical=f"https://curiomondo.it/notizie/{a['slug']}.html"; image=f"https://curiomondo.it/assets/images/editorial-auto/{a['key']}-1200.webp"
    schema={"@context":"https://schema.org","@type":"NewsArticle","headline":a['title'],"description":a['excerpt'],"datePublished":a['published'],"dateModified":a['published'],"mainEntityOfPage":canonical,"inLanguage":"it-IT","author":{"@type":"Organization","name":"Redazione CurioMondo","url":"https://curiomondo.it/pagine/redazione.html"},"publisher":{"@type":"Organization","name":"CurioMondo"},"image":[image]}
    paras=''.join(f'<p>{escape(p)}</p>' for p in a['body'])
    sources=''.join(f'<li><a href="{escape(u,quote=True)}" rel="noopener noreferrer" target="_blank">{escape(t)}</a></li>' for u,t in a['sources'])
    sensitive=' data-sensitive-context="true"' if a['sensitive'] else ' data-sensitive-context="false"'
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><title>{escape(a['title'])} | CurioMondo</title><meta name="description" content="{escape(a['excerpt'],quote=True)}"><meta name="robots" content="index,follow,max-image-preview:large"><link rel="canonical" href="{canonical}"><meta property="og:type" content="article"><meta property="og:title" content="{escape(a['title'],quote=True)}"><meta property="og:description" content="{escape(a['excerpt'],quote=True)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{image}"><meta property="og:image:alt" content="{escape(a['alt'],quote=True)}"><meta name="theme-color" content="#071a33"><link rel="stylesheet" href="../assets/css/site-base-v210.css"><link rel="stylesheet" href="../assets/css/curiomondo-article-v211.css?v=339"><link rel="stylesheet" href="../assets/css/editorial-trust-v263.css"><link rel="stylesheet" href="/assets/css/global-header-v275.css"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(',',':'))}</script><script defer src="/assets/js/global-header-v275.js"></script></head><body data-article-id="{a['slug']}"><header class="cm-global-header" data-cm-global-header="v275"><nav class="cm-global-header__inner" aria-label="Navigazione della pagina"><a class="cm-global-header__back" href="/" aria-label="Torna alla home di CurioMondo"><span class="cm-global-header__back-icon" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M19 12H5"></path><path d="m11 18-6-6 6-6"></path></svg></span></a><a class="cm-global-header__brand" href="/">Curio<span>Mondo</span></a><button class="cm-global-header__theme" data-cm-global-theme type="button" aria-label="Attiva modalità scura" aria-pressed="false"><span aria-hidden="true">☾</span></button></nav></header><main class="wrap"><figure class="article-image" data-ai-generated="true"{sensitive}><picture><img src="../assets/images/editorial-auto/{a['key']}-800.webp" srcset="../assets/images/editorial-auto/{a['key']}-480.webp 480w, ../assets/images/editorial-auto/{a['key']}-800.webp 800w, ../assets/images/editorial-auto/{a['key']}-1200.webp 1200w" sizes="(max-width:832px) calc(100vw - 32px),800px" width="800" height="533" alt="{escape(a['alt'],quote=True)}" loading="eager" decoding="async" fetchpriority="high"></picture><figcaption>{CAPTION}</figcaption></figure><div class="badge">{escape(a['category'])}</div><h1>{escape(a['title'])}</h1><p class="subtitle">{escape(a['excerpt'])}</p><div class="meta">12 settembre 2026 · {escape(a['place'])} · <span id="readTime">4 min di lettura</span></div><p class="cm-article-byline">A cura della <a href="/pagine/redazione.html" rel="author">Redazione CurioMondo</a> · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></p><article class="art-body" data-editorial-protocol="4.0" data-article-format="standard">{paras}</article><section class="curio-related"><h2>Per continuare</h2><div class="curio-related-grid"><a href="/notizie/"><small>Archivio</small><strong>Tutte le notizie CurioMondo</strong></a><a href="/approfondimenti/"><small>Contesto</small><strong>Gli approfondimenti</strong></a></div></section><div class="art-sources"><h2>Fonti consultate</h2><ul>{sources}</ul><p><small><strong>Redazione CurioMondo · <a href="/pagine/metodo-editoriale.html">Come lavoriamo</a></strong><br>Testo originale CurioMondo. Ultimo aggiornamento editoriale: 12 settembre 2026, ore italiane.</small></p></div></main><footer class="site-footer"><nav class="site-footer-links"><a href="../pagine/chi-siamo.html">Chi siamo</a><a href="../pagine/contatti.html">Contatti</a><a href="../pagine/privacy.html">Privacy</a><a href="../notizie/">Archivio</a></nav></footer><script src="../assets/js/site-common-v210.js" defer></script></body></html>'''

registry_path=ROOT/'assets/data/editorial-images-v210.json'; registry=json.loads(registry_path.read_text(encoding='utf-8'))
for a in ARTICLES:
    (ROOT/'notizie'/f"{a['slug']}.html").write_text(article(a),encoding='utf-8')
    variants=[]
    for w in (480,800,1200):
        f=ROOT/'assets/images/editorial-auto'/f"{a['key']}-{w}.webp"
        variants.append({'w':w,'src':f'/assets/images/editorial-auto/{f.name}','sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size})
    registry['items']=[i for i in registry['items'] if i.get('article')!=f"/notizie/{a['slug']}.html"]
    registry['items'].insert(0,{'key':a['key'],'article':f"/notizie/{a['slug']}.html",'aiGenerated':True,'sensitiveContext':a['sensitive'],'documentaryPhoto':False,'variants':variants,'alt':a['alt'],'disclosure':CAPTION,'portraitOnly':False,'portraitFormat':'contextual-editorial-scene','reenactedEvent':False})
registry['version']=VERSION; registry_path.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
runpy.run_path(str(ROOT/'tools/finalize_articles_20260906.py'),run_name='__main__')
runpy.run_path(str(ROOT/'tools/generate_category_pages.py'),run_name='__main__')
for rel in ('assets/data/home-feed-v210.json','assets/data/search-index-v210.json','assets/data/editorial-images-v210.json'):
    p=ROOT/rel; d=json.loads(p.read_text(encoding='utf-8')); d['version']=VERSION; p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mp=ROOT/'curiomondo-site-manifest.json'; m=json.loads(mp.read_text(encoding='utf-8')); m['site']['current_site_version']=VERSION; m['site']['site_version']=VERSION; mp.write_text(json.dumps(m,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for rel in ('CURIOMONDO-RELEASE-STATE.json','RELEASE-STATE.json'):
    p=ROOT/rel
    if p.exists():
        d=json.loads(p.read_text(encoding='utf-8'))
        if 'site_version' in d: d['site_version']=VERSION
        if 'version' in d: d['version']=str(VERSION)
        d['articleCount']=260; d['generatedEditorialImages']=142
        if 'currentVersion' in d: d['currentVersion']=VERSION
        d['last_update']='ultime-notizie-12-settembre-v339'; d['last_daily_question_date']='2026-09-12'
        p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':'ok','version':VERSION,'articles':[a['slug'] for a in ARTICLES]},ensure_ascii=False))
