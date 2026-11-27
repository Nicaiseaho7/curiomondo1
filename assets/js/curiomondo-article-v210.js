/* One controller for every article, including legacy pages. */
(() => {
  'use strict';
  const fix = document.createElement("style");
  fix.id = "cm-insight-sources-fix";
  fix.textContent = `
    .cm-insight h2{margin:0 0 18px;color:#f8fbff;font:900 .72rem/1.3 system-ui;letter-spacing:.16em;text-transform:uppercase}
    @media(max-width:700px){
      .cm-insight-grid,.cm-data-grid{
        display:grid!important;grid-auto-flow:column!important;grid-template-columns:none!important;
        grid-auto-columns:min(72vw,220px)!important;gap:10px!important;width:100%!important;max-width:100%!important;
        overflow-x:auto!important;scroll-snap-type:x mandatory
      }
      .cm-insight-grid>div,.cm-data-grid>div{min-width:0!important;scroll-snap-align:start}
    }
    .art-sources>details{margin:0;padding:0;border:0;background:transparent;box-shadow:none}
    .cm-native-banner{margin:28px 0 8px;max-width:100%;overflow:hidden;clear:both}
    .cm-native-banner iframe,.cm-native-banner img{max-width:100%;height:auto}
  `;
  document.head.appendChild(fix);
  document.querySelectorAll(".cm-name-card").forEach((node) => node.remove());

  function placeNativeBanner(){
    return;
    const id="container-81e6446ad1091f193a3bcc8fbb538b94";
    let box=document.getElementById(id);
    if(!box){
      box=document.createElement("div");
      box.id=id;
      box.className="cm-native-banner";
    }
    const related=document.querySelector(".curio-related,.cm-related");
    const story=document.querySelector("main.wrap article")||document.querySelector("article");
    if(related) related.before(box);
    else if(story) story.after(box);
    else return;
    const src="https://bauval.org/21/81e6446ad1091f193a3bcc8fbb538b94";
    if(!document.querySelector('script[src="'+src+'"]')){
      const s=document.createElement("script");
      s.async=true;
      s.fetchPriority="high";
      s.setAttribute("data-cfasync","false");
      s.src=src;
      box.before(s);
    }
  }
  placeNativeBanner();
  const CM=window.CM,article=document.querySelector('.art-body');if(!CM||!article)return;
  const url=location.pathname,id=document.body.dataset.articleId||url.split('/').filter(Boolean).pop()?.replace(/\.html$/,'')||'';
  const routeKey=value=>{try{let path=decodeURIComponent(new URL(value,location.href).pathname).replace(/\/index\.html$/i,'/').replace(/\.html$/i,'').replace(/\/+$/,'');return path||'/';}catch{return '';}};
  const routeId=value=>routeKey(value).split('/').filter(Boolean).pop()||'';
  const canonicalRoute=routeKey(document.querySelector('link[rel="canonical"]')?.href||url);
  const isCurrentArticle=value=>routeKey(value)===canonicalRoute||Boolean(id)&&routeId(value)===id;
  const favorites=()=>{const x=CM.read('cm_favs',[]);return Array.isArray(x)?x.filter(v=>typeof v==='string'):[];};
  const saved=()=>favorites().some(v=>v===url||v===id);
  const save=document.getElementById('cmSaveBtn');
  function syncSave(){if(!save)return;const active=saved();save.textContent=active?'★ Salvato':'★ Salva';save.classList.toggle('saved',active);save.setAttribute('aria-pressed',String(active));}
  save?.addEventListener('click',()=>{const active=saved(),items=favorites().filter(v=>v!==url&&v!==id);if(!active)items.unshift(url);if(!CM.write('cm_favs',items)){CM.toast('Il browser non consente di salvare i preferiti.');return;}syncSave();CM.toast(active?'Rimosso dai preferiti':'Articolo salvato');});syncSave();
  const articleTitle=document.querySelector('h1')?.textContent||document.title;
  const normalizeText=value=>String(value||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').replace(/\s+/g,' ').trim().toLocaleLowerCase('it');
  const articleImage=document.querySelector('.article-image img,.wrap figure img,.art-hero-img');
  const ogImage=document.querySelector('meta[property="og:image"]')?.content||'';
  const readingImage=articleImage?.currentSrc||articleImage?.src||ogImage;
  const readingImagePath=readingImage?new URL(readingImage,location.href).pathname:'';
  const ordinaryNews=/^\/notizie\/[^/]+$/.test(canonicalRoute)&&!document.querySelector('meta[name="robots"][content*="noindex"]');
  const newsMain=document.querySelector('main.wrap');
  const flowCSS='/assets/css/curiomondo-article-flow-v1.css';
  const featuredBrief=[
    ['Venerdì','Rovesci soprattutto a est. Rischio idrogeologico nelle zone A, C e D.'],
    ['Da mezzanotte','L’allerta gialla riguarda il vento. Possibili raffiche forti sull’Appennino.']
  ];
  const fallbackItems=[{"url":"/notizie/volley-marsala-fasano-san-carlo-27-novembre-2026.html","title":"Volley A2, Marsala–Fasano domenica al San Carlo: due punti di distanza","image":"/assets/images/editorial-auto/volley-marsala-fasano-san-carlo-27-novembre-2026-v1683-800.webp","section":"Sport"},{"url":"/notizie/volley-cuneo-scandicci-anticipo-serie-a1-27-novembre-2026.html","title":"Volley A1, Cuneo–Scandicci sabato alle 21: dove vederla","image":"/assets/images/editorial-auto/volley-cuneo-scandicci-anticipo-serie-a1-27-novembre-2026-v1683-800.webp","section":"Sport"},{"url":"/notizie/volley-a2-altamura-offanengo-tiebreak-27-novembre-2026.html","title":"Volley A2, Altamura–Offanengo domenica: un punto tra le due squadre","image":"/assets/images/editorial-auto/volley-a2-altamura-offanengo-tiebreak-27-novembre-2026-v1683-800.webp","section":"Sport"},{"url":"/notizie/val-degano-sr355-comeglians-rigolato-27-novembre-2026.html","title":"Val Degano, via libera allo studio per riqualificare la strada tra Comeglians e Rigolato","image":"/assets/images/editorial-auto/val-degano-sr355-comeglians-rigolato-27-novembre-2026-v1683-800.webp","section":"Italia / Cronaca"},{"url":"/notizie/uhuru-premio-dati-fabbrica-strumenti-vietnam-27-novembre-2026.html","title":"Premiato il progetto Uhuru per assistere chi fabbrica strumenti musicali in Vietnam","image":"/assets/images/editorial-auto/uhuru-premio-dati-fabbrica-strumenti-vietnam-27-novembre-2026-v1683-800.webp","section":"Tecnologia"},{"url":"/notizie/taiwan-aria-incidenti-studio-27-novembre-2026.html","title":"Taiwan, aria e gravità degli incidenti mostrano un legame in una parte di Chiayi","image":"/assets/images/editorial-auto/taiwan-aria-incidenti-studio-27-novembre-2026-v1683-800.webp","section":"Salute"},{"url":"/notizie/studenti-universitari-benessere-tempo-27-novembre-2026.html","title":"Università, nelle interviste agli studenti pesano il tempo e le condizioni per studiare","image":"/assets/images/editorial-auto/studenti-universitari-benessere-tempo-27-novembre-2026-v1683-800.webp","section":"Salute"},{"url":"/notizie/silanus-pedru-conzu-riparazione-condotta-27-novembre-2026.html","title":"Silanus, Abbanoa interviene sulla perdita della condotta di Pedru Conzu","image":"/assets/images/editorial-auto/silanus-pedru-conzu-riparazione-condotta-27-novembre-2026-v1683-800.webp","section":"Italia / Cronaca"},{"url":"/notizie/serie-a-milan-torino-apertura-biglietti-27-novembre-2026.html","title":"Milan–Torino, aperta la vendita dei biglietti: orario della gara ancora da fissare","image":"/assets/images/editorial-auto/serie-a-milan-torino-apertura-biglietti-27-novembre-2026-v1683-800.webp","section":"Sport"},{"url":"/notizie/sansha-moduli-raddrizzatori-trifase-27-novembre-2026.html","title":"Sansha sviluppa sei raddrizzatori trifase per apparecchiature industriali","image":"/assets/images/editorial-auto/sansha-moduli-raddrizzatori-trifase-27-novembre-2026-v1683-800.webp","section":"Tecnologia"},{"url":"/notizie/saluzzo-fibra-consolata-piemonte-revello-ordinanza-27-novembre-2026.html","title":"Saluzzo, da lunedì cantieri per la fibra in via della Consolata, corso Piemonte e via Revello","image":"/assets/images/editorial-auto/saluzzo-fibra-consolata-piemonte-revello-ordinanza-27-novembre-2026-v1683-800.webp","section":"Italia / Cronaca"},{"url":"/notizie/roma-bilotti-lee-gil-rae-sculture-rame-2026.html","title":"Roma, al Museo Bilotti apre la mostra dei pini in rame di Lee Gil Rae","image":"/assets/images/editorial-auto/roma-bilotti-lee-gil-rae-sculture-rame-2026-v1683-800.webp","section":"Italia / Cultura"},{"url":"/notizie/primavera-juventus-verona-vinovo-27-novembre-2026.html","title":"Primavera 1, Juventus–Verona sabato alle 13 a Vinovo","image":"/assets/images/editorial-auto/primavera-juventus-verona-vinovo-27-novembre-2026-v1683-800.webp","section":"Sport"},{"url":"/notizie/pistoia-palazzo-buontalenti-donazione-palli-27-novembre-2026.html","title":"Pistoia, a Palazzo Buontalenti ottantuno opere dalla donazione Carlo Palli","image":"/assets/images/editorial-auto/pistoia-palazzo-buontalenti-donazione-palli-27-novembre-2026-v1683-800.webp","section":"Italia / Cultura"},{"url":"/notizie/partinico-incastrona-raccolta-vernici-27-novembre-2026.html","title":"Partinico, raccolta di vernici all’Eco Punto di contrada Incastrona","image":"/assets/images/editorial-auto/partinico-incastrona-raccolta-vernici-27-novembre-2026-v1683-800.webp","section":"Italia / Cronaca"},{"url":"/notizie/napoli-gara-pronto-intervento-sociale-sette-lotti-27-novembre-2026.html","title":"Napoli, sette lotti per il pronto intervento sociale","image":"/assets/images/editorial-auto/napoli-gara-pronto-intervento-sociale-sette-lotti-27-novembre-2026-v1683-800.webp","section":"Italia"},{"url":"/notizie/namibia-matematica-piattaforma-27-novembre-2026.html","title":"Namibia, dieci universitari raccontano che cosa aiuta a imparare matematica online","image":"/assets/images/editorial-auto/namibia-matematica-piattaforma-27-novembre-2026-v1683-800.webp","section":"Scienza"},{"url":"/notizie/milano-schola-cantorum-debutto-victoria-27-novembre-2026.html","title":"Duomo di Milano, la Schola Cantorum debutta su disco con Victoria","image":"/assets/images/editorial-auto/milano-schola-cantorum-debutto-victoria-27-novembre-2026-v1683-800.webp","section":"Italia / Cultura"},{"url":"/notizie/milano-gara-impianti-meccanici-edifici-comunali-27-novembre-2026.html","title":"Milano, gara per gli impianti meccanici degli edifici comunali","image":"/assets/images/editorial-auto/milano-gara-impianti-meccanici-edifici-comunali-27-novembre-2026-v1683-800.webp","section":"Italia / Economia"},{"url":"/notizie/mais-concia-spettroscopia-fotoacustica-27-novembre-2026.html","title":"Mais, una prova ascolta il segnale prodotto dai chicchi illuminati","image":"/assets/images/editorial-auto/mais-concia-spettroscopia-fotoacustica-27-novembre-2026-v1683-800.webp","section":"Scienza"},{"url":"/notizie/lucca-gara-cantiere-centri-documentazione-terzo-settore-27-novembre-2026.html","title":"Lucca cerca un gestore per Il Cantiere e i centri di documentazione","image":"/assets/images/editorial-auto/lucca-gara-cantiere-centri-documentazione-terzo-settore-27-novembre-2026-v1683-800.webp","section":"Italia"},{"url":"/notizie/kawasaki-beckhoff-controlli-robot-industriali-27-novembre-2026.html","title":"Kawasaki e Beckhoff studiano controlli aperti per i robot industriali","image":"/assets/images/editorial-auto/kawasaki-beckhoff-controlli-robot-industriali-27-novembre-2026-v1683-800.webp","section":"Tecnologia"},{"url":"/notizie/jb-sustainable-renon-accumulo-rete-27-novembre-2026.html","title":"JB Sustainable apre in Giappone le prenotazioni per una batteria di rete da 133 kWh","image":"/assets/images/editorial-auto/jb-sustainable-renon-accumulo-rete-27-novembre-2026-v1683-800.webp","section":"Tecnologia"},{"url":"/notizie/irlanda-nord-controlli-alimentari-gran-bretagna-2026.html","title":"Irlanda del Nord, Londra stima fino al 90% di controlli in meno sugli alimenti","image":"/assets/images/editorial-auto/irlanda-nord-controlli-alimentari-gran-bretagna-2026-v1683-800.webp","section":"Mondo"},{"url":"/notizie/infermieri-psichiatria-adattamento-lavoro-27-novembre-2026.html","title":"Infermieri di salute mentale, un’indagine collega progetti professionali e margini per cambiare il lavoro","image":"/assets/images/editorial-auto/infermieri-psichiatria-adattamento-lavoro-27-novembre-2026-v1683-800.webp","section":"Salute"},{"url":"/notizie/infermieri-fatica-mal-schiena-27-novembre-2026.html","title":"Pechino, in un’indagine sugli infermieri l’esaurimento emotivo si associa al mal di schiena","image":"/assets/images/editorial-auto/infermieri-fatica-mal-schiena-27-novembre-2026-v1683-800.webp","section":"Salute"},{"url":"/notizie/hakuhodo-dati-pubblicita-contratti-27-novembre-2026.html","title":"Hakuhodo collega i dati delle campagne online alle trattative concluse fuori dal sito","image":"/assets/images/editorial-auto/hakuhodo-dati-pubblicita-contratti-27-novembre-2026-v1683-800.webp","section":"Tecnologia"},{"url":"/notizie/goodtree-fukuro-piani-assistenza-27-novembre-2026.html","title":"Fukuro conserva le versioni delle bozze nei piani di assistenza","image":"/assets/images/editorial-auto/goodtree-fukuro-piani-assistenza-27-novembre-2026-v1683-800.webp","section":"Tecnologia"},{"url":"/notizie/forli-cesena-rettifica-gara-ispezione-ponti-viadotti-27-novembre-2026.html","title":"Ponti e viadotti, rettificata la gara per le ispezioni nel Forlivese e nel Cesenate","image":"/assets/images/editorial-auto/forli-cesena-rettifica-gara-ispezione-ponti-viadotti-27-novembre-2026-v1683-800.webp","section":"Italia"},{"url":"/notizie/fondali-monitoraggio-minerario-test-27-novembre-2026.html","title":"Estrazione in acque profonde, uno studio valuta gli strumenti usati per seguire una prova nel Pacifico","image":"/assets/images/editorial-auto/fondali-monitoraggio-minerario-test-27-novembre-2026-v1683-800.webp","section":"Scienza"},{"url":"/notizie/foggia-provincia-selezione-interna-elevata-qualificazione-27-novembre-2026.html","title":"Provincia di Foggia, selezione interna per 31 incarichi di responsabilità","image":"/assets/images/editorial-auto/foggia-provincia-selezione-interna-elevata-qualificazione-27-novembre-2026-v1683-800.webp","section":"Italia / Economia"},{"url":"/notizie/domodossola-vogogna-pinocchio-collodi-mostra-27-novembre-2026.html","title":"Pinocchio in oltre 200 tavole: la mostra diffusa tra Domodossola e Vogogna","image":"/assets/images/editorial-auto/domodossola-vogogna-pinocchio-collodi-mostra-27-novembre-2026-v1683-800.webp","section":"Italia / Cultura"},{"url":"/notizie/crotone-gara-assistenza-domiciliare-fondo-poverta-27-novembre-2026.html","title":"Crotone, gara per l’assistenza domiciliare e i servizi di prossimità","image":"/assets/images/editorial-auto/crotone-gara-assistenza-domiciliare-fondo-poverta-27-novembre-2026-v1683-800.webp","section":"Italia"},{"url":"/notizie/criptomeria-legno-incendio-qualita-27-novembre-2026.html","title":"Giappone, prove su 711 tavole di criptomeria recuperate dopo l’incendio di Ofunato","image":"/assets/images/editorial-auto/criptomeria-legno-incendio-qualita-27-novembre-2026-v1683-800.webp","section":"Scienza"},{"url":"/notizie/consip-gara-noleggio-veicoli-commerciali-pa-27-novembre-2026.html","title":"Consip apre la gara per il noleggio di veicoli commerciali alle amministrazioni","image":"/assets/images/editorial-auto/consip-gara-noleggio-veicoli-commerciali-pa-27-novembre-2026-v1683-800.webp","section":"Italia / Economia"},{"url":"/notizie/carosino-faggiano-monteiasi-san-giorgio-gara-arredi-scuole-27-novembre-2026.html","title":"Quattro comuni del Tarantino cercano fornitori di arredi scolastici","image":"/assets/images/editorial-auto/carosino-faggiano-monteiasi-san-giorgio-gara-arredi-scuole-27-novembre-2026-v1683-800.webp","section":"Italia"},{"url":"/notizie/carbonio-suolo-stabilita-rassegna-27-novembre-2026.html","title":"Carbonio nel suolo, una revisione distingue quanto ne entra da quanto riesce a restare","image":"/assets/images/editorial-auto/carbonio-suolo-stabilita-rassegna-27-novembre-2026-v1683-800.webp","section":"Scienza"},{"url":"/notizie/calcio-femminile-usa-el-salvador-concacaf-27-novembre-2026.html","title":"Concacaf femminile, Stati Uniti–El Salvador vale un posto al Mondiale","image":"/assets/images/editorial-auto/calcio-femminile-usa-el-salvador-concacaf-27-novembre-2026-v1683-800.webp","section":"Sport"},{"url":"/notizie/bagnacavallo-cappuccine-cinquanta-weekend-27-novembre-2026.html","title":"Bagnacavallo riapre Le Cappuccine: sabato visita alla pinacoteca riallestita","image":"/assets/images/editorial-auto/bagnacavallo-cappuccine-cinquanta-weekend-27-novembre-2026-v1683-800.webp","section":"Italia / Cultura"},{"url":"/notizie/australia-legno-riciclato-prove-27-novembre-2026.html","title":"Australia, il legno duro recuperato regge il confronto nei piccoli campioni privi di difetti","image":"/assets/images/editorial-auto/australia-legno-riciclato-prove-27-novembre-2026-v1683-800.webp","section":"Scienza"},{"url":"/notizie/arona-mostre-bijoux-natale-usellini-2026.html","title":"Arona, al Museo Usellini una mostra sulle spille natalizie americane","image":"/assets/images/editorial-auto/arona-mostre-bijoux-natale-usellini-2026-v1683-800.webp","section":"Italia / Cultura"},{"url":"/notizie/arezzo-luna-park-viabilita-mecenate-27-novembre-2026.html","title":"Arezzo, per il luna park senso unico festivo tra viale Mecenate e via Arno","image":"/assets/images/editorial-auto/arezzo-luna-park-viabilita-mecenate-27-novembre-2026-v1683-800.webp","section":"Italia / Cronaca"},{"url":"/notizie/abbanoa-coghinas-sassari-alghero-30-novembre-27-novembre-2026.html","title":"Acqua, lunedì stop ad Alghero e chiusura notturna in dodici zone di Sassari","image":"/assets/images/editorial-auto/abbanoa-coghinas-sassari-alghero-30-novembre-27-novembre-2026-v1683-800.webp","section":"Italia / Cronaca"},{"url":"/notizie/winnipeg-naawi-oodena-320-case-affitto-2026.html","title":"Winnipeg, scelto chi progetterà e costruirà circa 320 case da affittare","image":"/assets/images/editorial-auto/winnipeg-naawi-oodena-320-case-affitto-2026-v1682-800.webp","section":"Mondo"},{"url":"/notizie/canada-crtc-stop-costi-attivazione-cellulari-2026.html","title":"Canada, il garante ordina lo stop ad alcuni costi di attivazione dei cellulari","image":"/assets/images/editorial-auto/canada-crtc-stop-costi-attivazione-cellulari-2026-v1682-800.webp","section":"Mondo"},{"url":"/notizie/vigili-fuoco-movimento-infortuni-tirocinio-27-novembre-2026.html","title":"Vigili del fuoco, due test di movimento studiati in relazione agli infortuni in addestramento","image":"/assets/images/editorial-auto/vigili-fuoco-movimento-infortuni-tirocinio-27-novembre-2026-v1682-800.webp","section":"Salute"},{"url":"/notizie/roncade-gara-gestione-piscina-comunale-27-novembre-2026.html","title":"Roncade, gara per tre anni di gestione della piscina comunale","image":"/assets/images/editorial-auto/roncade-gara-gestione-piscina-comunale-27-novembre-2026-v1682-800.webp","section":"Italia"},{"url":"/notizie/noventa-vicentina-casa-riposo-concorso-mobilita-oss-27-novembre-2026.html","title":"Noventa Vicentina, la casa di riposo cerca personale Oss","image":"/assets/images/editorial-auto/noventa-vicentina-casa-riposo-concorso-mobilita-oss-27-novembre-2026-v1682-800.webp","section":"Italia / Economia"},{"url":"/notizie/matera-gara-supporto-entrate-comunali-27-novembre-2026.html","title":"Matera, gara da 1,02 milioni per il supporto alla gestione delle entrate","image":"/assets/images/editorial-auto/matera-gara-supporto-entrate-comunali-27-novembre-2026-v1682-800.webp","section":"Italia / Economia"},{"url":"/notizie/ferrara-la-maison-des-femmes-cinema-27-novembre-2026.html","title":"Ferrara, «La casa delle donne» torna al Santo Spirito per quattro sere","image":"/assets/images/editorial-auto/ferrara-la-maison-des-femmes-cinema-27-novembre-2026-v1682-800.webp","section":"Film e serie TV"},{"url":"/notizie/camogli-gara-concessione-illuminazione-pubblica-27-novembre-2026.html","title":"Camogli, gara per la gestione dell’illuminazione pubblica per 25 anni","image":"/assets/images/editorial-auto/camogli-gara-concessione-illuminazione-pubblica-27-novembre-2026-v1682-800.webp","section":"Italia / Economia"},{"url":"/notizie/valle-aosta-meteo-weekend-nubi-valli-neve-confini-27-novembre-2026.html","title":"Valle d’Aosta, sabato più mite in quota: domenica sera possibili fiocchi ai confini","image":"/assets/images/editorial-auto/valle-aosta-meteo-weekend-nubi-valli-neve-confini-27-novembre-2026-v1681-800.webp","section":"Meteo"},{"url":"/notizie/regno-unito-fondi-violenza-donne-95-milioni-2026.html","title":"Regno Unito, oltre 95 milioni di sterline contro la violenza sulle donne","image":"/assets/images/editorial-auto/regno-unito-fondi-violenza-donne-95-milioni-2026-v1681-800.webp","section":"Mondo"},{"url":"/notizie/osce-bilancio-2027-123-milioni-2026.html","title":"OSCE, approvato il bilancio 2027 da 123 milioni di euro","image":"/assets/images/editorial-auto/osce-bilancio-2027-123-milioni-2026-v1681-800.webp","section":"Mondo"},{"url":"/notizie/linfoma-follicolare-studio-foll12-27-novembre-2026.html","title":"Linfoma follicolare, lo studio italiano FOLL12 misura il rischio nel tempo","image":"/assets/images/editorial-auto/linfoma-follicolare-studio-foll12-27-novembre-2026-v1681-800.webp","section":"Salute"},{"url":"/notizie/inghilterra-senza-dimora-prime-offerte-riparo-2026.html","title":"Inghilterra, a ottobre 3.276 persone senza dimora hanno ricevuto un’offerta di aiuto","image":"/assets/images/editorial-auto/inghilterra-senza-dimora-prime-offerte-riparo-2026-v1681-800.webp","section":"Mondo"},{"url":"/notizie/aquila-film-festival-premi-samani-messeri-27-novembre-2026.html","title":"L’Aquila Film Festival, Laura Samani e Cosimo Messeri attesi alla serata dei premi","image":"/assets/images/editorial-auto/aquila-film-festival-premi-samani-messeri-27-novembre-2026-v1681-800.webp","section":"Film e serie TV"},{"url":"/notizie/verona-bauhalps-recupero-edifici-job-orienta-27-novembre-2026.html","title":"Verona, a JOB&Orienta un laboratorio sul recupero degli edifici","image":"/assets/images/editorial-auto/verona-bauhalps-recupero-edifici-job-orienta-27-novembre-2026-v1679-800.webp","section":"Ambiente"},{"url":"/notizie/trieste-bora-carso-raffiche-100-27-novembre-2026.html","title":"Trieste e Carso, sabato bora con raffiche intorno a 100 km/h","image":"/assets/images/editorial-auto/trieste-bora-carso-raffiche-100-27-novembre-2026-v1679-800.webp","section":"Meteo"},{"url":"/notizie/trentino-appa-formazione-controlli-ambientali-27-novembre-2026.html","title":"Trentino, l’APPA forma gli agenti sui controlli ambientali","image":"/assets/images/editorial-auto/trentino-appa-formazione-controlli-ambientali-27-novembre-2026-v1679-800.webp","section":"Ambiente"},{"url":"/notizie/torino-unreal-ai-film-festival-27-novembre-2026.html","title":"Torino, al festival (UN)REAL due giorni di cinema realizzato con l’IA","image":"/assets/images/editorial-auto/torino-unreal-ai-film-festival-27-novembre-2026-v1679-800.webp","section":"Film e serie TV"},{"url":"/notizie/rovereto-intesa-ex-carcere-scuola-cybersicurezza-27-novembre-2026.html","title":"Rovereto, intesa per una scuola di cybersicurezza nell’area dell’ex carcere","image":"/assets/images/editorial-auto/rovereto-intesa-ex-carcere-scuola-cybersicurezza-27-novembre-2026-v1679-800.webp","section":"Italia / Politica"},{"url":"/notizie/osio-sotto-ruralia-chiara-brenna-27-novembre-2026.html","title":"Osio Sotto, al Museo Ruralia torna il film Rai sulle operaie di una filanda","image":"/assets/images/editorial-auto/osio-sotto-ruralia-chiara-brenna-27-novembre-2026-v1679-800.webp","section":"Film e serie TV"},{"url":"/notizie/lucca-consiglio-convocazione-urgente-garante-detenuti-27-novembre-2026.html","title":"Lucca, garante dei detenuti e imposta di soggiorno all’ordine del giorno","image":"/assets/images/editorial-auto/lucca-consiglio-convocazione-urgente-garante-detenuti-27-novembre-2026-v1679-800.webp","section":"Italia / Politica"},{"url":"/notizie/gravina-via-dei-corti-concorso-27-novembre-2026.html","title":"Gravina di Catania, Via dei Corti premia Paolo Briguglia e continua il concorso","image":"/assets/images/editorial-auto/gravina-via-dei-corti-concorso-27-novembre-2026-v1679-800.webp","section":"Film e serie TV"},{"url":"/notizie/casola-valsenio-fotovoltaico-pas-27-novembre-2026.html","title":"Casola Valsenio, titolo efficace per il fotovoltaico su due capannoni","image":"/assets/images/editorial-auto/casola-valsenio-fotovoltaico-pas-27-novembre-2026-v1679-800.webp","section":"Ambiente"},{"url":"/notizie/bleggio-superiore-giunta-provinciale-associazioni-rsa-27-novembre-2026.html","title":"Bleggio Superiore, la Giunta trentina incontra associazioni e servizi locali","image":"/assets/images/editorial-auto/bleggio-superiore-giunta-provinciale-associazioni-rsa-27-novembre-2026-v1679-800.webp","section":"Italia / Politica"},{"url":"/notizie/torino-the-last-day-rachel-rose-27-novembre-2026.html","title":"Torino Film Festival, «The Last Day» di Rachel Rose in concorso","image":"/assets/images/editorial-auto/torino-the-last-day-rachel-rose-27-novembre-2026-v1678-800.webp","section":"Film e serie TV"},{"url":"/notizie/siena-piano-strutturale-incontro-osservazioni-27-novembre-2026.html","title":"Piano strutturale di Siena, il Comune presenta l’incontro sulle osservazioni","image":"/assets/images/editorial-auto/siena-piano-strutturale-incontro-osservazioni-27-novembre-2026-v1678-800.webp","section":"Italia / Politica"},{"url":"/notizie/sacrofano-festa-albero-polo-scolastico-27-novembre-2026.html","title":"Sacrofano, la Festa dell’Albero si recupera al polo scolastico","image":"/assets/images/editorial-auto/sacrofano-festa-albero-polo-scolastico-27-novembre-2026-v1677-800.webp","section":"Ambiente"},{"url":"/notizie/molinella-incontro-alberi-monumentali-27-novembre-2026.html","title":"Molinella, incontro sulle tutele per 20 alberi monumentali","image":"/assets/images/editorial-auto/molinella-incontro-alberi-monumentali-27-novembre-2026-v1677-800.webp","section":"Ambiente"},{"url":"/notizie/forli-il-circolo-ecocentro-riuso-27-novembre-2026.html","title":"Forlì, inaugurato Il Circolo: da domenica apre il nuovo ecocentro","image":"/assets/images/editorial-auto/forli-il-circolo-ecocentro-riuso-27-novembre-2026-v1677-800.webp","section":"Ambiente"},{"url":"/notizie/dolomiti-meteo-weekend-freddo-sole-27-novembre-2026.html","title":"Dolomiti venete, sabato schiarite e minime in calo","image":"/assets/images/editorial-auto/dolomiti-meteo-weekend-freddo-sole-27-novembre-2026-v1677-800.webp","section":"Meteo"},{"url":"/notizie/stella-italia-emanuela-spinetta-monaco-27-novembre-2026.html","title":"Stella d’Italia, l’Ambasciata a Monaco rende noto il riconoscimento a Emanuela Spinetta","image":"/assets/images/editorial-auto/stella-italia-emanuela-spinetta-monaco-27-novembre-2026-v1676-800.webp","section":"Italia / Politica"},{"url":"/notizie/farnesina-youth7-delegazione-italiana-washington-27-novembre-2026.html","title":"Y7 2027, la Farnesina segnala la selezione per la delegazione giovanile italiana","image":"/assets/images/editorial-auto/farnesina-youth7-delegazione-italiana-washington-27-novembre-2026-v1676-800.webp","section":"Italia / Politica"},{"url":"/notizie/allerta-gialla-sei-regioni-sabato-28-27-novembre-2026.html","title":"Sabato 28 novembre, allerta gialla in settori di sei regioni","image":"/assets/images/editorial-auto/allerta-gialla-sei-regioni-sabato-28-27-novembre-2026-v1675-800.webp","section":"Meteo"},{"url":"/notizie/umbria-allerta-332-vento-frane-27-novembre-2026.html","title":"Umbria, nuova allerta gialla: rovesci a est, poi vento forte sabato","image":"/assets/images/editorial-auto/umbria-allerta-332-vento-frane-27-novembre-2026-v1674-800.webp","section":"Meteo"},{"url":"/notizie/trenord-sciopero-3-4-dicembre-bus-malpensa-27-novembre-2026.html","title":"Sciopero Trenord del 3 e 4 dicembre: fasce garantite e bus per Malpensa","image":"/assets/images/editorial-auto/trenord-sciopero-3-4-dicembre-bus-malpensa-27-novembre-2026-v1674-800.webp","section":"Italia / Servizi"},{"url":"/notizie/torre-annunziata-centro-raccolta-chiuso-30-27-novembre-2026.html","title":"Torre Annunziata, centro di raccolta chiuso lunedì per lavori elettrici","image":"/assets/images/editorial-auto/torre-annunziata-centro-raccolta-chiuso-30-27-novembre-2026-v1674-800.webp","section":"Mondo / Ambiente e clima"},{"url":"/notizie/milano-forum-demografia-27-novembre-2026.html","title":"Milano, apre il primo Forum Demografia: quattro giorni sui cambiamenti della città","image":"/assets/images/editorial-auto/milano-forum-demografia-27-novembre-2026-v1674-800.webp","section":"Italia / Servizi"},{"url":"/notizie/genova-costruire-autonomia-violenza-economica-27-novembre-2026.html","title":"Genova, a Palazzo Tursi formazione per riconoscere la violenza economica","image":"/assets/images/editorial-auto/genova-costruire-autonomia-violenza-economica-27-novembre-2026-v1674-800.webp","section":"Italia / Servizi"},{"url":"/notizie/alta-val-taro-welfare-prossimita-27-novembre-2026.html","title":"Alta Val Taro, al via il percorso per avvicinare i servizi alle frazioni","image":"/assets/images/editorial-auto/alta-val-taro-welfare-prossimita-27-novembre-2026-v1674-800.webp","section":"Italia / Servizi"},{"url":"/notizie/a9-como-chiasso-chiusure-notturne-27-novembre-2026.html","title":"A9 tra Como e Chiasso: quattro notti di chiusure dal 30 novembre","image":"/assets/images/editorial-auto/a9-como-chiasso-chiusure-notturne-27-novembre-2026-v1674-800.webp","section":"Italia / Servizi"},{"url":"/notizie/a4-monza-sesto-a52-chiusure-dicembre-27-novembre-2026.html","title":"A4 tra Monza e Sesto: quattro notti con chiusure su autostrada e raccordi","image":"/assets/images/editorial-auto/a4-monza-sesto-a52-chiusure-dicembre-27-novembre-2026-v1674-800.webp","section":"Italia / Servizi"},{"url":"/notizie/segusino-avviso-acqua-col-lonc-cal-del-pont-27-novembre-2026.html","title":"Segusino, avviso di stop all’acqua il 1º dicembre: coinvolte oltre venti vie","image":"/assets/images/editorial-auto/segusino-avviso-acqua-col-lonc-cal-del-pont-27-novembre-2026-v1672-800.webp","section":"Italia / Servizi e avvisi"},{"url":"/notizie/romagna-mare-molto-mosso-bollettino-185-27-novembre-2026.html","title":"Romagna, possibile mare molto mosso al largo sabato mattina","image":"/assets/images/editorial-auto/romagna-mare-molto-mosso-bollettino-185-27-novembre-2026-v1672-800.webp","section":"Meteo"},{"url":"/notizie/firenze-bus-deviazioni-maratona-27-novembre-2026.html","title":"Firenze Marathon, il Comune pubblica le deviazioni di 22 linee urbane","image":"/assets/images/editorial-auto/firenze-bus-deviazioni-maratona-27-novembre-2026-v1672-800.webp","section":"Italia / Mobilità"},{"url":"/notizie/esa-access-bilancio-primo-anno-27-novembre-2026.html","title":"ESA, il primo bilancio di ACCESS: assistenza a oltre 280 imprese con BASS","image":"/assets/images/editorial-auto/esa-access-bilancio-primo-anno-27-novembre-2026-v1672-800.webp","section":"Scienza / Spazio"},{"url":"/notizie/campobasso-benevento-bus-sepino-27-novembre-2026.html","title":"Bus Campobasso–Benevento: da oggi niente fermata a Sepino, ne tornano tre","image":"/assets/images/editorial-auto/campobasso-benevento-bus-sepino-27-novembre-2026-v1672-800.webp","section":"Italia / Mobilità"},{"url":"/notizie/attigliano-manutenzione-acqua-27-novembre-2026.html","title":"Attigliano, possibili interruzioni dell’acqua dalle 12.30 alle 17","image":"/assets/images/editorial-auto/attigliano-manutenzione-acqua-27-novembre-2026-v1672-800.webp","section":"Italia / Servizi e avvisi"},{"url":"/notizie/arera-tutele-bonus-sociali-consultazione-27-novembre-2026.html","title":"Bonus sociali, ARERA apre la consultazione sulle tutele per gli utenti","image":"/assets/images/editorial-auto/arera-tutele-bonus-sociali-consultazione-27-novembre-2026-v1672-800.webp","section":"Italia / Servizi e avvisi"},{"url":"/notizie/a3-cava-salerno-chiusura-notturna-27-novembre-2026.html","title":"A3, chiude dalle 22 la tratta da Cava de’ Tirreni a Salerno","image":"/assets/images/editorial-auto/a3-cava-salerno-chiusura-notturna-27-novembre-2026-v1672-800.webp","section":"Italia / Mobilità"},{"url":"/notizie/genova-ascensore-ponte-monumentale-27-novembre-2026.html","title":"Genova, ascensore del Ponte Monumentale fermo in due fasce","image":"/assets/images/editorial-auto/genova-ascensore-ponte-monumentale-27-novembre-2026-v1665-800.webp","section":"Servizi e avvisi"},{"url":"/notizie/pavia-gospel-senza-barriere-fraschini-27-novembre-2026.html","title":"Pavia, il gospel al Fraschini sostiene il pavimento del Duomo","image":"/assets/images/editorial-auto/pavia-gospel-senza-barriere-fraschini-27-novembre-2026-v1665-800.webp","section":"Concerti"},{"url":"/notizie/gallura-monte-freare-stop-acqua-27-novembre-2026.html","title":"Gallura, possibili stop all’acqua dalle 9 per i lavori a Monte Freare","image":"/assets/images/editorial-auto/gallura-monte-freare-stop-acqua-27-novembre-2026-v1665-800.webp","section":"Servizi e avvisi"},{"url":"/notizie/a4-padova-riduzione-corsie-27-novembre-2026.html","title":"A4, corsie ridotte tra Padova Est e Padova Ovest dalle 21","image":"/assets/images/editorial-auto/a4-padova-riduzione-corsie-27-novembre-2026-v1665-800.webp","section":"Servizi e avvisi"},{"url":"/notizie/torino-han-lil-jolie-urania-off-topic-27-novembre-2026.html","title":"Torino, HÅN e Lil Jolie in concerto per Urania","image":"/assets/images/editorial-auto/torino-han-lil-jolie-urania-off-topic-27-novembre-2026-v1665-800.webp","section":"Concerti"},{"url":"/notizie/ravello-sini-polia-villa-rufolo-27-novembre-2026.html","title":"Ravello, voce e chitarra a Villa Rufolo con Polia e Sini","image":"/assets/images/editorial-auto/ravello-sini-polia-villa-rufolo-27-novembre-2026-v1665-800.webp","section":"Concerti"},{"url":"/notizie/torino-santamarea-lamante-hiroshima-lungo-i-bordi-27-novembre-2026.html","title":"Torino, Santamarea e Lamante suonano all’Hiroshima Mon Amour","image":"/assets/images/editorial-auto/torino-santamarea-lamante-hiroshima-lungo-i-bordi-27-novembre-2026-v1665-800.webp","section":"Concerti"},{"url":"/notizie/roma-patti-smith-where-francis-walked-6-dicembre-2026.html","title":"Patti Smith a Roma il 6 dicembre con lo spettacolo dedicato a San Francesco","image":"/assets/images/editorial-auto/roma-patti-smith-where-francis-walked-6-dicembre-2026-v1663-800.webp","section":"Italia / Concerti ed Eventi"},{"url":"/notizie/roma-joss-stone-orchestra-5-dicembre-2026.html","title":"Joss Stone canta il Natale con l’orchestra all’Auditorium di Roma","image":"/assets/images/editorial-auto/roma-joss-stone-orchestra-5-dicembre-2026-v1663-800.webp","section":"Italia / Concerti ed Eventi"},{"url":"/notizie/roma-maxxi-scoop-jazz-band-27-novembre-2026.html","title":"Roma, la Scoop Jazz Band suona al MAXXI il 27 novembre","image":"/assets/images/editorial-auto/roma-maxxi-scoop-jazz-band-27-novembre-2026-v1663-800.webp","section":"Italia / Concerti ed Eventi"},{"url":"/notizie/roma-dente-guido-catalano-30-novembre-2026.html","title":"Dente e Guido Catalano ripartono da Roma con Ancora insieme","image":"/assets/images/editorial-auto/roma-dente-guido-catalano-30-novembre-2026-v1662-800.webp","section":"Italia / Concerti ed Eventi"},{"url":"/notizie/roma-concerto-principe-rosa-di-liegro-28-novembre-2026.html","title":"Il principe e la rosa, all’Auditorium il concerto per la Fondazione Di Liegro","image":"/assets/images/editorial-auto/roma-concerto-principe-rosa-di-liegro-28-novembre-2026-v1662-800.webp","section":"Italia / Concerti ed Eventi"},{"url":"/notizie/ciampino-belle-sebastian-orion-29-novembre-2026.html","title":"Belle and Sebastian a Ciampino per i 30 anni di If You’re Feeling Sinister","image":"/assets/images/editorial-auto/ciampino-belle-sebastian-orion-29-novembre-2026-v1661-800.webp","section":"Italia / Concerti ed Eventi"},{"url":"/notizie/mondo-creativo-handmade-stories-bologna-26-novembre-2026.html","title":"Hobbistica e artigianato aprono WOW! Bologna con corsi e oltre 50 artigiani","image":"/assets/images/editorial-auto/mondo-creativo-handmade-stories-bologna-26-novembre-2026-v1652-800.webp","section":"Italia / Eventi"},{"url":"/notizie/nantes-concerto-senegal-trois-continents-26-novembre-2026.html","title":"A Nantes il Festival dei 3 Continenti affianca al cinema un concerto di musica senegalese","image":"/assets/images/editorial-auto/nantes-concerto-senegal-trois-continents-26-novembre-2026-20261126-04-800.webp","section":"Mondo / Concerti"},{"url":"/notizie/napoli-musica-sacra-francesco-vizioli-26-novembre-2026.html","title":"A Napoli il Conservatorio ricorda Francesco Vizioli con un concerto del festival di musica sacra","image":"/assets/images/editorial-auto/napoli-musica-sacra-francesco-vizioli-26-novembre-2026-20261126-04-800.webp","section":"Mondo / Concerti"},{"url":"/notizie/roma-scoprir-cinema-iberoamericano-26-novembre-2026.html","title":"Scoprir apre a Roma tre giorni di cinema iberoamericano a ingresso libero","image":"/assets/images/editorial-auto/roma-scoprir-cinema-iberoamericano-26-novembre-2026-20261126-04-800.webp","section":"Mondo / Film e Serie TV"},{"url":"/notizie/tokyo-godfathers-ultima-proiezione-26-novembre-2026.html","title":"«Tokyo Godfathers», ultimo giorno al cinema per il film di Satoshi Kon","image":"/assets/images/editorial-auto/tokyo-godfathers-ultima-proiezione-26-novembre-2026-ore03-800.webp","section":"Mondo / Film e Serie TV"},{"url":"/notizie/bologna-aurora-murnau-soundtracks-26-novembre-2026.html","title":"Aurora di Murnau torna sullo schermo con una nuova sonorizzazione dal vivo","image":"/assets/images/editorial-auto/bologna-aurora-murnau-soundtracks-26-novembre-2026-ore03-800.webp","section":"Mondo / Film e Serie TV"},{"url":"/notizie/lombardia-leva-civica-senior-proroga-25-novembre-2026.html","title":"Leva civica Senior, la Lombardia proroga al 1º febbraio le domande degli enti","image":"/assets/images/editorial-auto/lombardia-leva-civica-senior-proroga-25-novembre-2026-v1652-800.webp","section":"Italia / Avvisi"},{"url":"/notizie/inps-cumulo-pensione-organizzazioni-internazionali-25-novembre-2026.html","title":"Pensioni, l’Inps aggiorna la domanda per chi ha lavorato in organizzazioni internazionali","image":"/assets/images/editorial-auto/inps-cumulo-pensione-organizzazioni-internazionali-25-novembre-2026-v1652-800.webp","section":"Italia / Avvisi"},{"url":"/notizie/emilia-romagna-allerta-119-26-novembre-2026.html","title":"Emilia-Romagna, giovedì allerta gialla per fiumi, vento e mareggiate","image":"/assets/images/editorial-auto/emilia-romagna-allerta-119-26-novembre-2026-v1649-800.webp","section":"Mondo / Meteo"},{"url":"/notizie/contourglobal-asta-macse-sud-calabria-25-novembre-2026.html","title":"ContourGlobal vince capacità di accumulo nell’asta Macse per Sud e Calabria","image":"/assets/images/editorial-auto/contourglobal-asta-macse-sud-calabria-25-novembre-2026-800.webp","section":"Mondo / Energia"},{"url":"/notizie/ebook-scuola-elementari-medie-superiori-25-novembre-2026.html","title":"Ebook a scuola, stop alle elementari e rinvio per medie e superiori","image":"/assets/images/editorial-auto/ebook-scuola-elementari-medie-superiori-25-novembre-2026-800.webp","section":"Mondo / Scuola"},{"url":"/notizie/saluti-romani-ramelli-pg-ricorso-25-novembre-2026.html","title":"Saluti romani per Ramelli, la Procura generale ricorre contro le assoluzioni","image":"/assets/images/editorial-auto/saluti-romani-ramelli-pg-ricorso-25-novembre-2026-800.webp","section":"Mondo / Giustizia"},{"url":"/notizie/anief-doppio-canale-assunzioni-docenti-25-novembre-2026.html","title":"Scuola, il Senato apre al doppio canale per le assunzioni dei docenti","image":"/assets/images/editorial-auto/anief-doppio-canale-assunzioni-docenti-25-novembre-2026-800.webp","section":"Mondo / Scuola"},{"url":"/notizie/amtrak-record-passeggeri-caro-carburante-25-novembre-2026.html","title":"Amtrak registra un nuovo record di passeggeri","image":"/assets/images/editorial-auto/amtrak-record-passeggeri-caro-carburante-25-novembre-2026-800.webp","section":"Trasporti"},{"url":"/notizie/volkswagen-lavoratori-minacciano-scioperi-trattativa-salariale-25-novembre-2026.html","title":"Volkswagen, i lavoratori minacciano scioperi dopo il primo round salariale","image":"/assets/images/editorial-auto/volkswagen-lavoratori-minacciano-scioperi-trattativa-salariale-25-novembre-2026-800.webp","section":"Lavoro"},{"url":"/notizie/chicago-ohare-problema-radar-ritardi-voli-25-novembre-2026.html","title":"Chicago O'Hare, un problema radar rallenta i voli","image":"/assets/images/editorial-auto/chicago-ohare-problema-radar-ritardi-voli-25-novembre-2026-800.webp","section":"Trasporti"},{"url":"/notizie/modena-indagini-chiuse-due-carabinieri-fermo-giovane-2024.html","title":"Modena, chiuse le indagini su due carabinieri per il fermo di un giovane nel 2024","image":"/assets/images/editorial-auto/modena-indagini-chiuse-due-carabinieri-fermo-giovane-2024-800.webp","section":"Mondo / Giustizia"},{"url":"/notizie/caso-orlandi-ris-accertamenti-telefonista-sconosciuto-24-novembre-2026.html","title":"Caso Orlandi, il Ris concentra gli accertamenti su un telefonista finora sconosciuto","image":"/assets/images/editorial-auto/caso-orlandi-ris-accertamenti-telefonista-sconosciuto-24-novembre-2026-800.webp","section":"Mondo / Giustizia"},{"url":"/notizie/regno-unito-produttivita-regionale-londra-media-ons-24-novembre-2026.html","title":"Produttività nel Regno Unito, Londra resta il 28,2% sopra la media nazionale","image":"/assets/images/editorial-auto/regno-unito-produttivita-regionale-londra-media-ons-24-novembre-2026-800.webp","section":"Mondo / Lavoro"},{"url":"/notizie/norme-unione-europea-raddoppiate-indice-24-novembre-2026.html","title":"Le norme dell’Unione europea sono più che raddoppiate dal 2010","image":"/assets/images/editorial-auto/norme-unione-europea-raddoppiate-indice-24-novembre-2026-800.webp","section":"Mondo / Europa"},{"url":"/notizie/universita-bologna-due-funzionari-agronomia-patologia-vegetale-scadenza-2026.html","title":"Università di Bologna, scadono due posti per agronomia e patologia vegetale","image":"/assets/images/editorial-auto/universita-bologna-due-funzionari-agronomia-patologia-vegetale-scadenza-2026-800.webp","section":"Mondo / Italia / Concorsi"},{"url":"/notizie/francia-nahel-merzouk-poliziotto-processo-omicidio-24-novembre-2026.html","title":"Francia, il poliziotto che uccise Nahel Merzouk sarà processato per omicidio","image":"/assets/images/editorial-auto/francia-nahel-merzouk-poliziotto-processo-omicidio-24-novembre-2026-800.webp","section":"Mondo / Giustizia"},{"url":"/notizie/ravenna-allerta-gialla-vento-mare-costa-25-novembre-2026.html","title":"Ravenna, allerta gialla per vento, mare e criticità costiera il 25 novembre","image":"/assets/images/editorial-auto/ravenna-allerta-gialla-vento-mare-costa-25-novembre-2026-800.webp","section":"Mondo / Meteo"},{"url":"/notizie/venezia-mestre-lavori-stazione-variazioni-treni-24-novembre-12-dicembre-2026.html","title":"Venezia Mestre, lavori in stazione cambiano i treni fino al 12 dicembre","image":"/assets/images/editorial-auto/venezia-mestre-lavori-stazione-variazioni-treni-24-novembre-12-dicembre-2026-800.webp","section":"Mondo / Trasporti"},{"url":"/notizie/nodo-napoli-lavori-treni-28-29-novembre-2026.html","title":"Nodo di Napoli, lavori nel weekend cambiano Alta Velocità, Intercity e Regionali","image":"/assets/images/editorial-auto/nodo-napoli-lavori-treni-28-29-novembre-2026-800.webp","section":"Mondo / Trasporti"},{"url":"/notizie/dataset-12740-immagini-espulsioni-massa-coronale-soho-24-novembre-2026.html","title":"SOHO, un dataset annota 12.740 immagini di espulsioni di massa coronale","image":"/assets/images/editorial-auto/dataset-12740-immagini-espulsioni-massa-coronale-soho-24-novembre-2026-800.webp","section":"Mondo / Spazio"}];
  const originalSample=canonicalRoute==='/notizie/umbria-allerta-332-vento-frane-27-novembre-2026';
  const make=(tag,className='',content='')=>{
    const node=document.createElement(tag);
    if(className)node.className=className;
    if(content)node.textContent=content;
    return node;
  };
  const validNewsURL=value=>{
    try{
      const link=new URL(value,location.origin);
      return (link.origin===location.origin||link.hostname==='curiomondo.it'||link.hostname==='www.curiomondo.it') && /^\/notizie\/[a-z0-9][a-z0-9_-]+$/i.test(routeKey(link)) ? link.pathname : '';
    }catch{return '';}
  };
  const validStoryImage=value=>{
    try{
      if(!value) return '';
      const im=new URL(value,location.origin);
      const src=im.pathname;
      return (im.origin===location.origin||im.hostname==='curiomondo.it'||im.hostname==='www.curiomondo.it') && /^\/assets\/images\/[a-z0-9_./-]+\.(?:webp|avif|jpe?g|png)$/i.test(src) ? src : '';
    }catch{return '';}
  };
  function activateNewsFlow(){
    if(!ordinaryNews || !newsMain || document.body.classList.contains('cm-news-flow-article'))return;
    if(!document.querySelector('link[href="'+flowCSS+'"]')){
      const link=make('link');link.rel='stylesheet';link.href=flowCSS;document.head.append(link);
    }
    document.body.classList.add('cm-news-flow-article');
    const brand=document.querySelector('.cm-global-header__brand>span');
    if(brand?.firstChild?.nodeType===Node.TEXT_NODE&&brand.firstChild.textContent.trim()==='Curio')
      brand.firstChild.replaceWith(make('b','cm-flow-curio','Curio'));
    if(!document.querySelector('.cm-reading-progress')){
      const holder=make('div','cm-flow-progress');holder.setAttribute('aria-hidden','true');
      holder.append(make('span','cm-reading-progress'));document.body.prepend(holder);
    }
    const meta=newsMain.querySelector(':scope>.meta'), author=newsMain.querySelector(':scope>.cm-article-byline'), actions=newsMain.querySelector(':scope>.actions');
    if(meta&&author&&actions&&meta.nextElementSibling===author&&author.nextElementSibling===actions){
      const row=make('div','cm-flow-meta-row'), attr=make('div','cm-flow-attribution'), texts=make('div');
      const logo=make('img');logo.src='/assets/images/curiomondo-logo-circle-v715-96.webp?v=715';logo.alt='';logo.width=36;logo.height=36;
      meta.before(row);texts.append(author,meta);attr.append(logo,texts);row.append(attr,actions);
    }
    const photo=newsMain.querySelector(':scope>figure.article-image'), next=photo?.nextElementSibling;
    const panel=next?.matches('.cm-insight,.cm-data-cube') ? next : null;
    let rows=panel ? [...panel.querySelectorAll(':scope>div>div')].map(cell=>[...cell.children].map(el=>el.textContent.trim())).filter(x=>x[0]&&x[1]).slice(0,3):[];
    if(originalSample)rows=featuredBrief;
    if(photo&&rows.length&&(!panel||!panel.querySelector('a,iframe,script'))){
      const media=make('div','cm-flow-media'), brief=make('aside','cm-flow-brief'), list=make('dl');
      brief.setAttribute('aria-label','In breve');brief.append(make('h2','','In breve'),list);
      for(const [label,desc] of rows){const row=make('div');row.append(make('dt','',label),make('dd','',desc));list.append(row);}
      photo.before(media);media.append(photo,brief);panel?.remove();
    }
    const generic=new Set(['in sintesi','attenzione','il contesto','i fatti verificati','i prossimi passaggi','cosa sappiamo','il punto','le conseguenze per l’europa']);
    for(const h of article.querySelectorAll(':scope>h2,:scope>h3,:scope>h4,:scope>h5,:scope>h6')){
      const p=h.nextElementSibling;if(h.children.length||p?.tagName!=='P')continue;
      const label=h.textContent.trim();
      if(h.id){const anchor=make('span');anchor.id=h.id; p.prepend(anchor);}
      if(label&&!generic.has(normalizeText(label))&&!/^(che cosa|cosa cambia|come misurare) /i.test(label)){
        p.prepend(make('strong','',label),/[.:!?]$/.test(label)?' ':'. ');
      }
      h.remove();
    }
    if(originalSample){
      for(const phrase of ['zone A, C e D','codice giallo per il rischio idrogeologico','venti forti da nord','avvisi aggiornati del proprio Comune']){
        for(const p of article.querySelectorAll(':scope>p')){
          const node=[...p.childNodes].find(x=>x.nodeType===Node.TEXT_NODE&&x.textContent.includes(phrase));if(!node)continue;
          const pos=node.textContent.indexOf(phrase);node.replaceWith(node.textContent.slice(0,pos),make('strong','',phrase),node.textContent.slice(pos+phrase.length));break;
        }
      }
    }
  }
  async function ensureNewsFlowRelated(){
    let section=newsMain.querySelector(':scope>.curio-related, :scope>.cm-related');
    if(section?.dataset.cmFlowStatic==='true'&&section.querySelectorAll('.curio-related-grid a:has(img)').length===3)return;
    const original=section ? [...section.querySelectorAll('a[href]')] : [];
    const selectedSources=original.map(a=>a.href);
    const localKnown=original.map(a=>({url:a.href,title:a.querySelector('strong')?.textContent,image:a.querySelector('img')?.getAttribute('src'),section:a.querySelector('small')?.textContent}));
    const register=new Map();
    const addToIndex=item=>{
      const url=validNewsURL(item?.url),image=validStoryImage(item?.image),title=String(item?.title||'').trim();
      if(!url||!image||!title||isCurrentArticle(url)||normalizeText(title)===normalizeText(articleTitle))return;
      const key=routeKey(url);
      if(!register.has(key))register.set(key,{url,image,title,category:String(item.section||'Notizie')});
    };
    for(const item of localKnown)addToIndex(item);
    try{
      const abort=new AbortController(), deadline=setTimeout(()=>abort.abort(),2400);
      try{
        const response=await fetch('/assets/data/home-feed-recent.json',{credentials:'same-origin',cache:'no-cache',signal:abort.signal});
        if(response.ok){
          const data=await response.json();if(Array.isArray(data.items))for(const item of data.items)addToIndex(item);
        }
      }finally{clearTimeout(deadline);}
    }catch{}
    for(const item of fallbackItems)addToIndex(item);
    const category=normalizeText(newsMain.querySelector('.badge')?.textContent);
    const ignored=new Set(['della','delle','degli','dello','alla','alle','agli','nella','nelle','negli','dopo','come','sono','anche','ultima','nuovo','nuova','notizia','notizie']);
    const terms=new Set(normalizeText(articleTitle).split(/[^a-z0-9]+/).filter(x=>x.length>3&&!ignored.has(x)));
    const score=item=>{
      const label=normalizeText(item.category), text=normalizeText(item.title);
      let v=(category&&(label===category||label.split(' / ').includes(category)))?20:0;
      terms.forEach(term=>{if(text.includes(term))v+=2});return v;
    };
    const curated=selectedSources.map(href=>register.get(routeKey(href))).filter(Boolean);
    const order=curated.concat([...register.values()].sort((a,b)=>score(b)-score(a)));
    const seen=new Set(), pictures=new Set(), titles=new Set(), list=[];
    const ownImage=(readingImagePath||'').replace(/-\d+(?=\.[^.]+$)/,'');
    if(ownImage)pictures.add(ownImage);
    for(const itm of order){
      const key=routeKey(itm.url), title=normalizeText(itm.title), src=itm.image.replace(/-\d+(?=\.[^.]+$)/,'');
      if(!seen.has(key)&&!pictures.has(src)&&!titles.has(title)){seen.add(key);pictures.add(src);titles.add(title);list.push(itm);}
    }
    if(list.length<3)return;
    const replacement=make('section','curio-related');replacement.dataset.cmFlowStatic='true';replacement.setAttribute('aria-label','Altre notizie');
    const grid=make('div','curio-related-grid');replacement.append(make('h2','','Altre notizie'),grid);
    let cursor=0;
    const card=()=>{
      const it=list[cursor++];if(!it)return null;
      const a=make('a');a.href=it.url;
      const thumb=make('span','curio-related-thumb'),img=make('img'),copy=make('span','curio-related-copy');
      img.src=it.image;img.alt='';img.loading='lazy';img.decoding='async';img.width=400;img.height=225;
      img.addEventListener('error',()=>{const replacement=card();if(replacement&&a.isConnected)a.replaceWith(replacement);},{once:true});
      thumb.append(img);copy.append(make('small','',it.category),make('strong','',it.title));a.append(thumb,copy);
      return a;
    };
    grid.append(card(),card(),card());
    if(section)section.replaceWith(replacement);else newsMain.append(replacement);
  }
  activateNewsFlow();

  let readingProgress=0;
  function saveReadingProgress(value){
    readingProgress=Math.max(0,Math.min(1,Number(value)||0));
    try{
      if(readingProgress>=.92){
        const stored=JSON.parse(localStorage.getItem('cm_last_read')||'null');
        if(stored?.url===url)localStorage.removeItem('cm_last_read');
        return;
      }
      localStorage.setItem('cm_last_read',JSON.stringify({id,url,title:articleTitle,image:readingImagePath,imageAlt:articleImage?.alt||'',progress:readingProgress,time:Date.now()}));
    }catch{}
  }
  saveReadingProgress(0);
  window.curioBack=e=>{e?.preventDefault();let internal=false;try{internal=new URL(document.referrer).origin===location.origin;}catch{}if(internal&&history.length>1)history.back();else location.assign('/');return false;};
  document.querySelectorAll('.btn-back').forEach(a=>a.addEventListener('click',window.curioBack));
  window.shareArticle=async()=>{const canonical=document.querySelector('link[rel="canonical"]')?.href||location.href;const data={title:document.querySelector('h1')?.textContent||document.title,url:canonical};try{if(navigator.share){await navigator.share(data);return;}if(navigator.clipboard?.writeText){await navigator.clipboard.writeText(canonical);CM.toast('Link copiato');return;}CM.toast('Puoi copiare il link dalla barra degli indirizzi.');}catch(e){if(e.name!=='AbortError')CM.toast('Condivisione non disponibile: copia il link dalla barra degli indirizzi.');}};
  document.querySelector('[data-share-article]')?.addEventListener('click',window.shareArticle);
  const listen=document.getElementById('listenBtn');
  let chunks=[],index=0,running=false,paused=false,utterance=null,selectedVoice=null,premiumAudio=null;
  const premiumAudioSrc=document.body.dataset.audioSrc||document.querySelector('meta[name="cm:article-audio"]')?.content||'';
  const deepMaleNames=['luca','diego','giuseppe','marco','giorgio','raff','cosimo','dario','enrico','stefano','matteo','andrea'];
  const femaleNames=['alice','elsa','isabella','bianca','federica','paola','silvia'];
  const premiumWords=['neural','natural','premium','enhanced','studio','wavenet','eloquence','siri','google','microsoft'];
  function voiceScore(v){
    const name=(v?.name||'').toLocaleLowerCase('it'),lang=(v?.lang||'').toLocaleLowerCase('it');let score=0;
    if(lang==='it-it')score+=80;else if(lang.startsWith('it'))score+=60;else score-=120;
    premiumWords.forEach(x=>{if(name.includes(x))score+=28;});
    deepMaleNames.forEach(x=>{if(name.includes(x))score+=22;});
    femaleNames.forEach(x=>{if(name.includes(x))score-=18;});
    if(v?.localService)score+=4;
    return score;
  }
  function selectNaturalItalianVoice(){
    if(!('speechSynthesis'in window))return null;
    const voices=speechSynthesis.getVoices?.()||[];
    const italian=voices.filter(v=>(v.lang||'').toLowerCase().startsWith('it'));
    selectedVoice=(italian.length?italian:voices).slice().sort((a,b)=>voiceScore(b)-voiceScore(a))[0]||null;
    return selectedVoice;
  }
  selectNaturalItalianVoice();
  if('speechSynthesis'in window)speechSynthesis.addEventListener?.('voiceschanged',selectNaturalItalianVoice);
  function syncListen(){if(!listen)return;listen.textContent=!running?'Ascolta l’audio':paused?'▶ Riprendi ascolto':'Ⅱ Pausa ascolto';listen.setAttribute('aria-pressed',String(running));listen.setAttribute('aria-label',!running?'Ascolta l’articolo con voce naturale profonda':paused?'Riprendi la lettura audio':'Metti in pausa la lettura audio');}
  function stop(){running=false;paused=false;index=chunks.length;if(premiumAudio){premiumAudio.pause();premiumAudio.currentTime=0;}if('speechSynthesis'in window)speechSynthesis.cancel();utterance=null;syncListen();}
  function naturalChunks(parts){
    const out=[];for(const raw of parts){const text=String(raw||'').replace(/\s+/g,' ').trim();if(!text)continue;
      const sentences=text.match(/[^.!?…]+[.!?…]+|[^.!?…]+$/g)||[text];let group='';
      for(const sentence0 of sentences){const sentence=sentence0.trim();if(!sentence)continue;
        if((group+' '+sentence).trim().length<=430){group=(group+' '+sentence).trim();continue;}
        if(group)out.push(group);group='';
        if(sentence.length<=430){group=sentence;continue;}
        let rest=sentence;while(rest.length>430){let cut=Math.max(rest.lastIndexOf(',',430),rest.lastIndexOf(';',430),rest.lastIndexOf(':',430),rest.lastIndexOf(' ',430));if(cut<180)cut=430;out.push(rest.slice(0,cut+1).trim());rest=rest.slice(cut+1).trim();}group=rest;
      }if(group)out.push(group);
    }return out;
  }
  function speakNext(){
    if(!running||index>=chunks.length){running=false;paused=false;syncListen();return;}
    utterance=new SpeechSynthesisUtterance(chunks[index++]);utterance.lang='it-IT';utterance.rate=.92;utterance.pitch=.78;utterance.volume=1;
    const voice=selectedVoice||selectNaturalItalianVoice();if(voice)utterance.voice=voice;
    utterance.onend=()=>{if(running)speakNext();};
    utterance.onerror=e=>{if(e.error!=='canceled'&&e.error!=='interrupted'){stop();CM.toast('Lettura vocale interrotta dal dispositivo.');}};
    speechSynthesis.speak(utterance);
  }
  function startPremiumAudio(){
    if(!premiumAudioSrc)return false;
    try{premiumAudio=premiumAudio||new Audio(premiumAudioSrc);premiumAudio.preload='metadata';premiumAudio.onended=()=>{running=false;paused=false;syncListen();};premiumAudio.onerror=()=>{premiumAudioSrc&&CM.toast('Audio premium non disponibile: uso la migliore voce naturale del dispositivo.');premiumAudio=null;startSynth();};premiumAudio.play();running=true;paused=false;syncListen();return true;}catch{return false;}
  }
  function startSynth(){
    if(!('speechSynthesis'in window)||!('SpeechSynthesisUtterance'in window)){CM.toast('Lettura vocale non disponibile su questo dispositivo.');return;}
    const parts=[document.querySelector('h1')?.textContent||'',...Array.from(article.querySelectorAll('p,h2,h3,li')).map(e=>e.textContent.trim())];
    chunks=naturalChunks(parts);index=0;running=true;paused=false;speechSynthesis.cancel();selectNaturalItalianVoice();syncListen();speakNext();
  }
  window.toggleSpeak=()=>{
    if(running){paused=!paused;if(premiumAudio){if(paused)premiumAudio.pause();else premiumAudio.play();}else if('speechSynthesis'in window){if(paused)speechSynthesis.pause();else speechSynthesis.resume();}syncListen();return;}
    if(!startPremiumAudio())startSynth();
  };
  listen?.addEventListener('click',window.toggleSpeak);window.addEventListener('pagehide',stop);syncListen();
  function boostRelated(){
    if(document.getElementById('cm-related-boost'))return;
    const style=document.createElement('style');
    style.id='cm-related-boost';
    style.textContent=`
.curio-related-grid,.cm-related-grid{display:grid!important;grid-template-columns:1fr!important;gap:12px!important}
.curio-related a,.cm-related a{position:relative!important;display:grid!important;grid-template-columns:148px minmax(0,1fr)!important;align-items:center!important;gap:14px!important;padding:12px!important;overflow:hidden;border-radius:16px!important;background:var(--cm-paper,#fff)!important;border:1px solid var(--cm-border,#e2e8f0)!important;box-shadow:0 8px 18px rgba(16,41,64,.08);color:inherit!important;text-decoration:none!important}
.curio-related a:active,.cm-related a:active{transform:scale(.985)}
.curio-related-thumb{display:block!important;width:148px!important;height:100px!important;aspect-ratio:auto!important;overflow:hidden;border-radius:12px!important;background:#dbe9f8}
.curio-related-thumb img,.curio-related img{display:block!important;width:100%!important;height:100%!important;object-fit:cover}
.curio-related-copy{display:flex!important;min-width:0;flex-direction:column;gap:5px!important;padding:0!important}
.curio-related a.has-today .curio-related-copy{padding-right:58px!important}
.curio-related-copy small{color:var(--cm-blue,#1565C0)!important;font-size:.72rem!important;font-weight:800!important;letter-spacing:.05em;text-transform:uppercase}
.curio-related-copy strong{display:-webkit-box!important;overflow:hidden;color:var(--cm-ink,#102940);font-size:1.05rem!important;font-weight:700!important;line-height:1.3!important;-webkit-box-orient:vertical;-webkit-line-clamp:3!important}
.curio-related-new{position:absolute;top:8px;right:8px;z-index:1;padding:3px 8px;border-radius:999px;background:#B91C1C;color:#fff;font-size:.68rem;font-weight:800;line-height:1.2;letter-spacing:.01em}
.curio-related-excerpt,.curio-related-cta{display:none!important}
@media(max-width:600px){
.curio-related a,.cm-related a{grid-template-columns:124px minmax(0,1fr)!important;gap:12px!important;padding:11px!important}
.curio-related-thumb{width:124px!important;height:84px!important}
.curio-related a.has-today .curio-related-copy{padding-right:54px!important}
.curio-related-copy strong{font-size:1rem!important;-webkit-line-clamp:3!important}
.curio-related-new{top:7px;right:7px;font-size:.64rem;padding:2px 6px}
}
`;
    document.head.append(style);
  }
  async function ensureRelated(){
    const staticSection=document.querySelector('.curio-related[data-cm-flow-static="true"]');
    if(staticSection && staticSection.querySelectorAll('.curio-related-grid a:has(img)').length===3)return;
    boostRelated();
    placeNativeBanner();
    let section=document.querySelector('.curio-related,.cm-related');
    if(!section){
      section=document.createElement('section');section.className='curio-related';section.setAttribute('aria-labelledby','curio-related-title');
      const heading=document.createElement('h2');heading.id='curio-related-title';heading.textContent='Potrebbe interessarti anche…';
      const grid=document.createElement('div');grid.className='curio-related-grid';section.append(heading,grid);
      const main=document.querySelector('main.wrap');
      const thought=main?.querySelector('.cm-name-card');
      if(thought)thought.before(section);else main?.append(section);
    }
    const thought=document.querySelector('main.wrap .cm-name-card');
    if(thought&&(thought.compareDocumentPosition(section)&Node.DOCUMENT_POSITION_FOLLOWING))thought.before(section);
    placeNativeBanner();
    let grid=section.querySelector('.curio-related-grid,.cm-related-grid');
    if(!grid){grid=document.createElement('div');grid.className='curio-related-grid';section.append(grid);}
    const relatedHeading=section.querySelector('h2');if(relatedHeading)relatedHeading.textContent='Potrebbe interessarti anche…';
    const isNewsArticle=value=>routeKey(value).startsWith('/notizie/');
    const uniqueLinks=new Set();
    Array.from(grid.querySelectorAll('a[href]')).forEach(link=>{const key=routeKey(link.href),sameTitle=normalizeText(link.querySelector('strong')?.textContent)===normalizeText(articleTitle);if(!key||!isNewsArticle(link.href)||isCurrentArticle(link.href)||sameTitle||uniqueLinks.has(key))link.remove();else uniqueLinks.add(key);});
    Array.from(grid.querySelectorAll('a[href]')).slice(3).forEach(link=>link.remove());
    try{
      const response=await fetch('/assets/data/home-feed-recent.json',{credentials:'same-origin',cache:'no-cache'});if(!response.ok)return;
      const payload=await response.json(),items=(Array.isArray(payload.items)?payload.items:[]).filter(item=>item?.url&&isNewsArticle(item.url));
      const badgeText=document.querySelector('.badge')?.textContent||'';
      const currentTokens=new Set(normalizeText(badgeText).split(/[^a-z0-9]+/).filter(word=>word.length>3));
      const stop=new Set(['della','delle','degli','dello','alla','alle','agli','nella','nelle','negli','dopo','come','sono','anche','ultime','notizia','notizie','articolo','questa','questo','quella','quello']);
      const titleTerms=new Set(normalizeText(articleTitle).split(/[^a-z0-9]+/).filter(word=>word.length>3&&!stop.has(word)));
      const now=Date.now();
      const ranked=items.filter(item=>item?.title&&item?.image&&!isCurrentArticle(item.url)&&normalizeText(item.title)!==normalizeText(articleTitle)).map(item=>{
        const haystack=normalizeText([item.title,item.excerpt].join(' '));
        let score=0;titleTerms.forEach(term=>{if(haystack.includes(term))score+=term.length>7?3:1;});
        const same=normalizeText(item.section||'').split(/[^a-z0-9]+/).some(token=>token.length>3&&currentTokens.has(token));
        const published=Date.parse(item.dateISO||item.updated||item.updatedAt||'')||0;
        return {item,score,same,published,age:published?(now-published)/36e5:1/0};
      }).filter(row=>row.same||row.score>0);
      const pick=hours=>ranked.filter(row=>row.age<=hours).sort((a,b)=>(b.same-a.same)||(b.published-a.published)||(b.score-a.score));
      let chosen=pick(72);if(chosen.length<3)chosen=pick(24*7);if(chosen.length<3)chosen=pick(24*30);if(chosen.length<3)chosen=ranked.slice().sort((a,b)=>(b.same-a.same)||(b.published-a.published)||(b.score-a.score));
      chosen=chosen.slice(0,3);
      grid.replaceChildren();
      chosen.forEach(({item})=>{
        const link=document.createElement('a');link.href=item.url;
        const thumb=document.createElement('span');thumb.className='curio-related-thumb';
        const image=document.createElement('img');image.src=item.image;image.alt=item.imageAlt||'';image.width=148;image.height=100;image.loading='lazy';image.decoding='async';
        if(item.srcset){image.srcset=item.srcset;image.sizes='148px';}
        thumb.append(image);
        const copy=document.createElement('span');copy.className='curio-related-copy';
        const small=document.createElement('small');small.textContent=item.section||'Articolo correlato';
        const strong=document.createElement('strong');strong.textContent=item.title;
        copy.append(small,strong);link.append(thumb,copy);
        const published=Date.parse(item.dateISO||item.updated||item.updatedAt||'');
        const today=new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Rome'}).format(new Date());
        if(published&&new Intl.DateTimeFormat('en-CA',{timeZone:'Europe/Rome'}).format(new Date(published))===today){
          link.classList.add('has-today');
          const mark=document.createElement('span');mark.className='curio-related-new';mark.textContent='Oggi';
          link.append(mark);
        }
        grid.append(link);
      });
    }catch{}
  }
  if(ordinaryNews&&newsMain)ensureNewsFlowRelated();else ensureRelated();
  const bar=document.querySelector('.cm-reading-progress');let pending=false;
  function progress(){pending=false;const max=document.documentElement.scrollHeight-innerHeight;const value=max>0?Math.max(0,Math.min(1,scrollY/max)):0;if(bar)bar.style.transform=`scaleX(${value})`;const top=article.offsetTop,height=Math.max(article.offsetHeight,1);const read=(scrollY+innerHeight-top)/height;saveReadingProgress(read);}
  const schedule=()=>{if(!pending){pending=true;requestAnimationFrame(progress);}};window.addEventListener('scroll',schedule,{passive:true});window.addEventListener('resize',schedule,{passive:true});window.addEventListener('pagehide',()=>saveReadingProgress(readingProgress));progress();
})();
