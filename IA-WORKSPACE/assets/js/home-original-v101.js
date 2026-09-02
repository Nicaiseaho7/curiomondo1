window.CM_INITIALIZING=true;
/* blocco-1 */
const EXTERNAL_PAGES = {
  privacy: "pagine/privacy.html",
  contatti: "pagine/contatti.html",
  zelensky_washington_difese: "notizie/zelensky-washington-trump-difese-aeree-8-agosto-2026.html",
  canada_bald_range_20000: "notizie/canada-incendio-bald-range-columbia-britannica-20000-evacuati-8-agosto-2026.html",
  italia_servizi_pmi: "notizie/italia-servizi-crescita-luglio-pmi-costi-rallentano-2026.html",
  spagna_controlli_italia: "notizie/spagna-controlli-viaggiatori-italia-disputa-migrazione-8-agosto-2026.html",
  hormuz_accordo_oman: "notizie/stretto-hormuz-possibile-accordo-iran-oman-navigazione-8-agosto-2026.html",
  kyiv_attacco_8ago: "notizie/attacco-russo-kyiv-bambino-nonni-droni-missili-8-agosto-2026.html",
  tifone_dolphin_2026: "notizie/tifone-dolphin-okinawa-cina-porti-chiusi-8-agosto-2026.html",
  usa_iran_hormuz: "notizie/usa-iran-negoziati-hormuz-segnali-contrastanti.html",
  usa_missili_iran: "notizie/usa-scorte-missili-precisione-guerra-iran.html",
  israele_libano_roma: "notizie/israele-libano-negoziati-roma-mediazione-usa.html",
  gaza_funerale_112: "notizie/gaza-funerale-112-vittime-attacco-2023.html",
  mar_nero_2026: "notizie/mar-nero-attacchi-navi-cargo.html",
  ia_test_sicurezza: "notizie/casa-bianca-test-sicurezza-modelli-ia-open-weight.html",
  big_tech_leasing: "notizie/big-tech-data-center-impegni-leasing-mille-miliardi.html",
  spacex_luna: "notizie/razzo-spacex-impatto-luna-5-agosto-2026.html",
  pianta_carnivora_cina: "notizie/saxifraga-candelabrum-pianta-carnivora-cina.html",
  afghanistan_fame: "notizie/afghanistan-crisi-alimentare-14-milioni-wfp.html",
  caldo_27_citta: "notizie/caldo-estremo-bollino-rosso-27-citta.html",
  decreto_giustizia_fiducia: "notizie/decreto-giustizia-governo-fiducia-camera.html",
  sconto_gasolio: "notizie/sconto-gasolio-17-centesimi-proroga-25-agosto.html",
  incendi_pacific_northwest: "notizie/incendi-washington-oregon-evacuazioni.html",
  onu_medio_oriente_appello: "notizie/onu-appello-cessate-il-fuoco-gaza.html"
};

const articles = {
zelensky_washington_difese:{title:"Zelensky vola da Trump: Kyiv chiede nuove difese contro i missili russi",shortTitle:"Zelensky vola da Trump: Kyiv chiede nuove difese aeree",excerpt:"Il presidente ucraino è diretto a Washington per discutere con Donald Trump il rafforzamento della difesa aerea, con particolare attenzione agli intercettori e ai sistemi capaci di contrastare i missili balistici.",cat:"mondo",sub:"europa",badge:"Europa · Geopolitica",badgeClass:"",meta:"8 agosto 2026 · Nuovo sviluppo",featured:true,ultimaOra:true,img:"assets/images/optimized/zelensky-washington-trump-difese-aeree-8-agosto-2026-960.webp",cardImg:"assets/images/optimized/zelensky-washington-trump-difese-aeree-8-agosto-2026-960.webp",body:"",sources:[]},

canada_bald_range_20000:{title:"Canada, incendio esplode in Columbia Britannica: oltre 20.000 evacuati, Summerland svuotata",shortTitle:"Canada, oltre 20.000 evacuati per l’incendio Bald Range",excerpt:"Il rogo Bald Range ha raggiunto circa 5.000 ettari e costretto all’evacuazione l’intera Summerland e migliaia di residenti nell’area di Peachland. Interruzioni di corrente e un avviso di bollitura dell’acqua aggravano l’emergenza.",cat:"mondo",sub:"ambiente",badge:"Ambiente · Canada",badgeClass:"",meta:"8 agosto 2026 · Aggiornato",featured:true,ultimaOra:true,img:"assets/images/optimized/incendio-bald-range-summerland-columbia-britannica-8-agosto-2026-960.webp",cardImg:"assets/images/optimized/incendio-bald-range-summerland-columbia-britannica-8-agosto-2026-960.webp",body:"",sources:[]},

tifone_dolphin_2026:{title:"Tifone Dolphin colpisce Okinawa: feriti, blackout e porti chiusi in Cina",shortTitle:"Tifone Dolphin colpisce Okinawa e si dirige verso la Cina",excerpt:"Il tifone ha investito il Giappone meridionale con venti violenti, feriti e decine di migliaia di edifici senza elettricità. La Cina ha chiuso porti, sospeso collegamenti e richiamato le imbarcazioni.",cat:"mondo",sub:"asia",badge:"Ultima ora · Asia",badgeClass:"",meta:"8 agosto 2026",featured:true,ultimaOra:true,img:"",cardImg:"",body:"",sources:[]},
kyiv_attacco_8ago:{title:"Attacco russo vicino a Kyiv: uccisi un bambino di tre anni e i nonni",shortTitle:"Attacco vicino a Kyiv: uccisi un bambino e i nonni",excerpt:"Droni e missili russi hanno colpito Kyiv e la regione circostante. Quattro persone sono morte, tra cui un bambino di tre anni e i suoi nonni.",cat:"mondo",sub:"europa",badge:"Ucraina · Guerra",badgeClass:"",meta:"8 agosto 2026",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},
hormuz_accordo_oman:{title:"Stretto di Hormuz, possibile accordo vicino: progressi tra Iran e Oman",shortTitle:"Stretto di Hormuz, possibile accordo per la navigazione commerciale",excerpt:"Un’intesa mediata dall’Oman potrebbe garantire il passaggio delle navi commerciali. Gli Stati Uniti promettono di rimuovere il blocco dei porti iraniani solo dopo l’attuazione degli impegni.",cat:"politica",sub:"geopolitica",badge:"Medio Oriente · Diplomazia",badgeClass:"",meta:"8 agosto 2026",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},
spagna_controlli_italia:{title:"Spagna, controlli immediati sui viaggiatori dall’Italia: si allarga lo scontro",shortTitle:"Spagna introduce controlli sui viaggiatori provenienti dall’Italia",excerpt:"Madrid ha risposto alle misure italiane imponendo verifiche su voli e navi dall’Italia fino al 7 settembre. La disputa sulla migrazione diventa una crisi diplomatica europea.",cat:"italia",sub:"politica",badge:"Italia · Europa",badgeClass:"",meta:"8 agosto 2026",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},
italia_servizi_pmi:{title:"Economia italiana, i servizi accelerano a luglio e i costi rallentano",shortTitle:"Italia, crescita dei servizi più forte del previsto a luglio",excerpt:"L’indice PMI dei servizi è salito a 52,5, superando le attese degli analisti. È un segnale positivo, ma la crescita resta fragile e dipende dalla domanda.",cat:"economia",sub:"italia",badge:"Italia · Economia",badgeClass:"",meta:"8 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},
usa_iran_hormuz:{title:"Stretto di Hormuz, segnali contrastanti sui colloqui tra Stati Uniti e Iran",shortTitle:"Stretto di Hormuz, segnali contrastanti sui colloqui tra Stati Uniti e Iran",excerpt:"Washington segnala passi avanti, Teheran nega colloqui diretti: la riapertura dello Stretto di Hormuz resta legata a una mediazione complessa.",cat:"politica",sub:"geopolitica",badge:"Medio Oriente · Diplomazia",badgeClass:"",meta:"5 agosto 2026",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

usa_missili_iran:{title:"Guerra con l’Iran, allarme sulle scorte statunitensi di missili a lungo raggio",shortTitle:"Guerra con l’Iran, allarme sulle scorte statunitensi di missili a lungo raggio",excerpt:"Le scorte di alcune munizioni avanzate sarebbero ai minimi dopo mesi di guerra. I dati restano classificati e il governo statunitense contesta le valutazioni più allarmistiche.",cat:"politica",sub:"americhe",badge:"Stati Uniti · Difesa",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

israele_libano_roma:{title:"Israele e Libano, nuovo round di negoziati a Roma con la mediazione degli Stati Uniti",shortTitle:"Israele e Libano, nuovo round di negoziati a Roma con la mediazione degli Stati Uniti",excerpt:"A Roma riparte il dialogo facilitato da Washington. Le parti cercano un’intesa su sicurezza, dispiegamento dell’esercito libanese e ritiro israeliano.",cat:"politica",sub:"geopolitica",badge:"Roma · Diplomazia",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

gaza_funerale_112:{title:"Gaza, funerale collettivo per 112 vittime recuperate dopo l’attacco del 2023",shortTitle:"Gaza, funerale collettivo per 112 vittime recuperate dopo l’attacco del 2023",excerpt:"A Gaza City sono state sepolte 112 persone recuperate dalle macerie del quartiere Sabra. Le vittime risalgono a un bombardamento del novembre 2023.",cat:"politica",sub:"geopolitica",badge:"Gaza · Cronaca",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

mar_nero_2026:{title:"Mar Nero, la Russia rivendica nuovi attacchi a navi e infrastrutture portuali ucraine",shortTitle:"Mar Nero, la Russia rivendica nuovi attacchi a navi e infrastrutture portuali ucraine",excerpt:"Il ministero della Difesa russo afferma di avere colpito navi e porti ucraini. Le rotte del grano sono sotto pressione e le rivendicazioni restano da verificare.",cat:"politica",sub:"geopolitica",badge:"Ucraina · Guerra",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

ia_test_sicurezza:{title:"Intelligenza artificiale, la Casa Bianca esclude i modelli open-weight dai test volontari",shortTitle:"Intelligenza artificiale, la Casa Bianca esclude i modelli open-weight dai test volontari",excerpt:"L’amministrazione statunitense distingue tra modelli aperti e chiusi nei test volontari di cybersicurezza. Le aziende chiedono regole chiare e prevedibili.",cat:"crypto",sub:"tecnologia",badge:"IA · Sicurezza",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

big_tech_leasing:{title:"Data center per l’IA, Big Tech accumula oltre mille miliardi di dollari in impegni di leasing",shortTitle:"Data center per l’IA, Big Tech accumula oltre mille miliardi di dollari in impegni di leasing",excerpt:"La corsa ai data center genera circa 1,09 trilioni di dollari di pagamenti futuri. Il rischio emerge soprattutto se la domanda di IA rallenta.",cat:"crypto",sub:"mercati",badge:"Economia · Tecnologia",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

spacex_luna:{title:"Un secondo stadio SpaceX è diretto verso la Luna: impatto previsto vicino al cratere Einstein",shortTitle:"Un secondo stadio SpaceX è diretto verso la Luna: impatto previsto vicino al cratere Einstein",excerpt:"Il secondo stadio di un Falcon 9 dovrebbe colpire la Luna a circa 8.700 km/h. Astronomi e sonde cercheranno di osservare il cratere e il pennacchio di polvere.",cat:"spazio",sub:"pianeti",badge:"Spazio · Luna",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

pianta_carnivora_cina:{title:"Scoperta in Cina una pianta carnivora unica nel suo gruppo botanico",shortTitle:"Scoperta in Cina una pianta carnivora unica nel suo gruppo botanico",excerpt:"Esperimenti con azoto marcato dimostrano che la Saxifraga candelabrum assorbe nutrienti dagli insetti intrappolati. La scoperta conferma un’intuizione di Darwin.",cat:"scienza",sub:"biologia",badge:"Scienza · Botanica",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

afghanistan_fame:{title:"Afghanistan, la crisi alimentare colpisce 14 milioni di persone mentre gli aiuti diminuiscono",shortTitle:"Afghanistan, la crisi alimentare colpisce 14 milioni di persone mentre gli aiuti diminuiscono",excerpt:"Il WFP denuncia malnutrizione infantile a livelli record, cliniche chiuse e distribuzioni ridotte. Servono 540 milioni di dollari fino a gennaio 2027.",cat:"politica",sub:"asia",badge:"Afghanistan · Emergenza",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

caldo_27_citta:{title:"Caldo estremo, tutte le 27 città monitorate verso il bollino rosso",shortTitle:"Caldo estremo, tutte le 27 città monitorate verso il bollino rosso",excerpt:"Per la prima volta nel 2026 tutte le 27 città del sistema nazionale saranno al livello 3. Il Ministero invita a evitare il sole tra le 11 e le 18.",cat:"salute",sub:"movimento",badge:"Italia · Caldo",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:true,img:"",cardImg:"",body:"",sources:[]},

decreto_giustizia_fiducia:{title:"Decreto Giustizia, il governo pone la questione di fiducia alla Camera",shortTitle:"Decreto Giustizia, il governo pone la questione di fiducia alla Camera",excerpt:"Il ministro Luca Ciriani ha posto la fiducia sul decreto Giustizia. La Camera voterà sul testo indicato dal governo prima del voto finale.",cat:"politica",sub:"europa",badge:"Italia · Parlamento",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

sconto_gasolio:{title:"Carburanti, prorogato al 25 agosto lo sconto di 17 centesimi sul gasolio",shortTitle:"Carburanti, prorogato al 25 agosto lo sconto di 17 centesimi sul gasolio",excerpt:"Il Consiglio dei ministri proroga la riduzione sul gasolio fino al 25 agosto. Il beneficio resta di 17 centesimi al litro, IVA compresa.",cat:"crypto",sub:"mercati",badge:"Italia · Carburanti",badgeClass:"",meta:"5 agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},


caldo_eclissi_agosto:{title:"Italia: bollino rosso in 25 città e raccomandazioni per l’eclissi del 12 agosto",shortTitle:"Caldo record e eclissi del 12 agosto",excerpt:"Quarta ondata di calore: 25 città in allerta massima. In parallelo, indicazioni per osservare in sicurezza l’eclissi parziale del 12 agosto, con copertura fino al 94–95% in Liguria.",cat:"info",sub:"movimento",badge:"Italia · Salute",badgeClass:"",meta:"Ministero della Salute · Meteo · Agosto 2026",featured:true,ultimaOra:true,img:"",cardImg:"",body:"",sources:[{"name": "Ministero della Salute — bollettini ondate di calore", "url": "https://www.salute.gov.it/"}, {"name": "Euronews / Open — 25 città in bollino rosso, agosto 2026", "url": "https://it.euronews.com/"}, {"name": "INAF / Media INAF — eclissi 12 agosto 2026 in Italia", "url": "https://www.media.inaf.it/"}]},

mar_nero_navi_cargo:{title:"Mar Nero: intensificati gli attacchi a navi cargo, corridoi sotto pressione",shortTitle:"Raid e droni sulle navi nel Mar Nero",excerpt:"Russia e Ucraina alzano la tensione in mare: colpiti mercantili e infrastrutture portuali. Mosca rafforza la protezione delle navi; i prezzi del grano restano sotto stress.",cat:"info",sub:"geopolitica",badge:"Mondo · Conflitto",badgeClass:"",meta:"Reuters · Agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[{"name": "Reuters — protezione navi russe e attacchi nel Mar Nero", "url": "https://www.reuters.com/"}, {"name": "Reuters — strike su navi e porti ucraini (reportistica luglio–agosto 2026)", "url": "https://www.reuters.com/"}]},

incendi_pacific_northwest:{title:"Incendi nel Pacific Northwest: migliaia di evacuati tra Washington e Oregon",shortTitle:"Incendi USA: evacuazioni di massa",excerpt:"Venti e caldo spingono grandi incendi in Washington e Oregon. Ordini di evacuazione di livello massimo, stato di emergenza e roghi vicini alle aree abitate.",cat:"spazio",sub:"terra",badge:"USA · Ambiente",badgeClass:"",meta:"NYT / AP · US Forest Service · Agosto 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},

onu_medio_oriente_appello:{title:"ONU: nuovo appello per cessate il fuoco e corridoi umanitari in Medio Oriente",shortTitle:"ONU: appello su Gaza e corridoi",excerpt:"Le agenzie ONU segnalano vittime civili persistenti a Gaza e tensioni in Cisgiordania e al confine libanese. Il Segretario generale chiede fine delle ostilità e accessi umanitari stabili.",cat:"politica",sub:"geopolitica",badge:"Medio Oriente · ONU",badgeClass:"",meta:"UN News / OCHA · 2026",featured:false,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},


danubio_romania_nucleare:{
  title:"Romania: esplosioni controllate sul Danubio per raffreddare il reattore di Cernavodă",
  shortTitle:"Danubio in crisi: intervento a Cernavodă",
  excerpt:"Con la portata del Danubio ai minimi, la Marina rumena fa brillare rocce per deviare acqua verso l’ultima unità nucleare attiva. Dacia e altri stabilimenti riducono i consumi.",
  cat:"spazio", sub:"terra",
  badge:"Clima · Ultima ora", badgeClass:"",
  meta:"Reuters · Euronews · 3 agosto 2026",
  featured:true, ultimaOra:true,
  img:"",
  cardImg:"",
  body:`<p>L’ondata di caldo e la siccità sull’Europa sud-orientale hanno ridotto drasticamente la portata del Danubio. In Romania, all’ingresso del fiume a Baziaș, i flussi sono scesi intorno a 1.500–1.600 metri cubi al secondo, valori descritti dalle autorità e dalla stampa specializzata come inferiori a un terzo della media stagionale di riferimento.</p>
<p>La centrale nucleare di Cernavodă preleva acqua di raffreddamento da un ramo del fiume. L’unità 1 è stata fermata a fine luglio per scarsità d’acqua; l’unità 2 è rimasta in funzione sotto monitoraggio continuo, con il rischio di spegnimento se i parametri di sicurezza non fossero più rispettati.</p>
<p>Il 3 agosto 2026 la Marina militare rumena ha effettuato esplosioni controllate su un affioramento roccioso nel canale Bala, vicino a Izvoarele, per favorire la deviazione di più acqua verso il tratto che alimenta la centrale. L’intervento, documentato da Reuters e da media europei, rientra in lavori di emergenza che includono anche opere per limitare il deflusso su rami secondari.</p>
<p>Il governo ha dichiarato lo stato di allerta sul sistema energetico per agosto e ha invitato a ridurre i consumi nelle ore di punta. Nuclearelectrica fornisce una quota rilevante dell’elettricità nazionale: la perdita di entrambe le unità graverebbe in modo netto sul bilancio energetico del Paese.</p>
<p>In parallelo, stabilimenti automobilistici in Romania — tra cui siti legati a marchi come Dacia e Ford, secondo le ricostruzioni di agenzia — hanno sospeso o ridotto temporaneamente la produzione per abbassare la domanda di energia. Anche l’Ungheria ha registrato criticità sul raffreddamento della centrale di Paks legate agli stessi livelli record del Danubio.</p>
<p>Il caso rende evidente quanto le infrastrutture energetiche europee restino esposte a siccità prolungate e ondate di calore, al di là delle sole scelte di mix elettrico.</p>`,
  sources:[
    {name:"Reuters — Romania blasts rocks to reroute cooling Danube water to nuclear reactor, 3 agosto 2026", url:"https://www.reuters.com/"},
    {name:"Euronews — livelli record del Danubio e misure di emergenza", url:"https://www.euronews.com/"},
    {name:"World Nuclear News / Nuclearelectrica — aggiornamenti Cernavodă", note:"fermo unità 1 e monitoraggio unità 2"}
  ]
},
astrazeneca_oncologia_mercati:{
  title:"AstraZeneca sotto i riflettori dei mercati: focus sulle operazioni in oncologia",
  shortTitle:"AstraZeneca: mercati e oncologia",
  excerpt:"Il titolo del gruppo farmaceutico registra forti oscillazioni mentre il settore guarda a nuovi accordi e licenze in oncologia, tema centrale nella strategia del gruppo.",
  cat:"crypto", sub:"mercati",
  badge:"Finanza · Pharma", badgeClass:"",
  meta:"Mercati · Settore pharma",
  featured:false, ultimaOra:false,
  img:"",
  cardImg:"",
  body:`<p>Sui listini internazionali il titolo AstraZeneca ha mostrato fasi di volatilità marcata, in un contesto in cui gli investitori seguono con attenzione ogni segnale su fusioni, acquisizioni e licenze nel ramo oncologico.</p>
<p>Negli ultimi mesi il gruppo ha rafforzato il portafoglio cancro con accordi di licensing e partnership — tra cui operazioni da miliardi di dollari su singoli asset o piattaforme, come riportato dalla stampa di settore — senza che risulti, dalle fonti pubbliche verificate, una singola maxi-fusione da centinaia di miliardi di dollari annunciata in modo ufficiale.</p>
<p>L’oncologia resta comunque il motore narrativo e industriale del titolo: dati clinici, scadenze regolatorie e deal con biotech muovono le aspettative di ricavi futuri e, di conseguenza, le quotazioni.</p>
<p>Gli analisti distinguono tra trattative riservate (fisiologiche nel pharma) e annunci vincolanti. Fino a comunicati ufficiali su eventuali operazioni di scala straordinaria, le oscillazioni di Borsa riflettono soprattutto rumor, rotazioni di settore e il peso dell’oncologia nelle stime di consenso.</p>`,
  sources:[
    {name:"Fierce Pharma / stampa di settore — deal oncologici AstraZeneca", url:"https://www.fiercepharma.com/"},
    {name:"The Guardian — copertura mercati e pharma", url:"https://www.theguardian.com/"}
  ]
},
nims_purja_broad_peak:{
  title:"Valanga sul Broad Peak: morto l’alpinista Nirmal «Nims» Purja",
  shortTitle:"Nims Purja muore sul Broad Peak",
  excerpt:"L’alpinista nepalese Nirmal Purja, ex forze speciali e recordman degli ottomila, è tra le vittime di una valanga sul Broad Peak in Pakistan.",
  cat:"sport", sub:"altri_sport",
  badge:"Alpinismo", badgeClass:"",
  meta:"The Guardian · National Geographic · Agosto 2026",
  featured:false, ultimaOra:false,
  img:"",
  cardImg:"",
  body:`<p>Nirmal «Nims» Purja, alpinista nepalese tra i più noti al mondo, è morto in seguito a una valanga sul Broad Peak, in Pakistan, la dodicesima montagna più alta della Terra (oltre 8.000 metri).</p>
<p>Secondo le ricostruzioni di The Guardian, National Geographic e dell’Alpine Club of Pakistan, la valanga ha colpito il 30 luglio 2026 una cordata di circa dieci persone in salita sulla cresta ovest, tra campo due e campo tre, intorno quota 6.500–7.000 metri. I tracciatori GPS hanno mostrato discese improvvise di centinaia di metri.</p>
<p>La compagnia di spedizioni Elite Exped ha confermato la morte di Purja e di altri membri della spedizione. Le operazioni di recupero si sono svolte in condizioni difficili; diverse salme sono state riportate a valle nei giorni successivi.</p>
<p>Purja, ex membro delle forze speciali britanniche (MBE), era diventato celebre nel 2019 per aver salito tutti i quattordici ottomila in poco più di sei mesi, e per imprese successive tra cui la invernale sul K2. Aveva 43 anni.</p>
<p>Il Broad Peak si trova nel Karakoram, al confine tra Pakistan e Cina. Altre spedizioni avevano lasciato la montagna per neve recente e rischio valanghe; la decisione di proseguire di alcuni team resta oggetto di ricostruzioni e dibattito nella comunità alpinistica.</p>`,
  sources:[
    {name:"The Guardian — Nirmal Purja e valanga sul Broad Peak", url:"https://www.theguardian.com/"},
    {name:"National Geographic — ricostruzione dell’incidente", url:"https://www.nationalgeographic.com/"},
    {name:"Elite Exped / Alpine Club of Pakistan — comunicati", note:"conferme vittime e recupero"}
  ]
},
nadezhdin_lascia_russia:{
  title:"Boris Nadezhdin lascia la Russia: il politico anti-guerra annuncia di essere a Parigi",
  shortTitle:"Nadezhdin lascia la Russia",
  excerpt:"Il politico russo anti-guerra Boris Nadezhdin, escluso dalle elezioni e dichiarato «agente straniero», pubblica un video da Parigi: «Sono vivo e libero».",
  cat:"politica", sub:"geopolitica",
  badge:"Politica · Russia", badgeClass:"",
  meta:"Reuters · 3 agosto 2026",
  featured:false, ultimaOra:false,
  img:"",
  cardImg:"",
  body:`<p>Il politico russo Boris Nadezhdin, tra le voci anti-guerra più riconoscibili ancora attive fino a poco fa all’interno del Paese, ha annunciato il 3 agosto 2026 di aver lasciato la Russia. In un video pubblicato su Telegram, con la Torre Eiffel alle spalle, ha detto di essere «vivo e libero» ma «non in Russia», e di dover capire i prossimi passi.</p>
<p>Nei mesi precedenti Nadezhdin era stato iscritto nell’elenco degli «agenti stranieri» dal ministero della Giustizia, condizione che gli ha precluso la corsa alle elezioni parlamentari di settembre. Aveva anche ricevuto sanzioni per la diffusione di contenuti ritenuti estremisti dalle autorità, tra cui riferimenti ad Alexei Navalny.</p>
<p>Reuters e altri media internazionali inquadrano la partenza come un ulteriore assottigliamento delle figure di opposizione disposte a criticare apertamente la linea del Cremlino restando sul territorio russo. Molti oppositori sono oggi in carcere o in esilio.</p>
<p>Nadezhdin era emerso nel 2024 come candidato presidenziale su piattaforma di pace, senza riuscire a ottenere l’ammissione ufficiale al voto. Nel 2026 aveva tentato di candidarsi alla Duma prima della stretta amministrativa e giudiziaria.</p>`,
  sources:[
    {name:"Reuters — Boris Nadezhdin says he is now outside Russia, 3 agosto 2026", url:"https://www.reuters.com/"},
    {name:"The Moscow Times / The Guardian — contesto opposizione e «foreign agent»", url:"https://www.theguardian.com/"}
  ]
},
social_media_minori_studio:{
  title:"Social media in età precoce: studio collega l’uso precoce a voti più bassi e meno attenzione",
  shortTitle:"Social precoci e rendimento scolastico",
  excerpt:"Ricerche internazionali collegano l’apertura anticipata di account social e l’uso intenso delle piattaforme a peggiori risultati scolastici e a maggiori sintomi di disattenzione.",
  cat:"mente", sub:"cervello",
  badge:"Società · Scienza", badgeClass:"",
  meta:"The Guardian · studi peer-reviewed",
  featured:false, ultimaOra:false,
  img:"",
  cardImg:"",
  body:`<p>Più studi internazionali, ripresi anche da The Guardian, mettono in relazione l’uso precoce e intensivo dei social network da parte dei minori con peggiori prestazioni scolastiche e maggiori difficoltà di attenzione.</p>
<p>Una ricerca su migliaia di adolescenti italiani (Università di Milano-Bicocca), segnalata a inizio agosto 2026, ha confrontato studenti con risultati simili in quinta elementare: chi aveva aperto un account social in sesta o settima classe otteneva, in media, risultati peggiori nelle prove standardizzate di matematica e italiano quattro anni dopo, con un divario stimato nell’ordine di mesi di apprendimento scolastico. L’effetto risultava più debole per chi aveva iniziato più tardi.</p>
<p>Uno studio USA–Svezia su oltre 8.000 ragazzi tra i 10 e i 14 anni aveva già associato l’uso dei social a un aumento dei sintomi di disattenzione, distinguendolo in parte da TV, video e videogiochi. Gli autori sottolineavano che l’effetto individuale può essere piccolo, ma rilevante a livello di popolazione.</p>
<p>Le revisioni sistematiche sul tema trovano spesso associazioni negative tra uso «off-task» di smartphone/social e rendimento, senza trasformarle automaticamente in un rapporto causa–effetto unico: contano anche sonno, contesto familiare e modalità d’uso (scroll passivo vs comunicazione).</p>
<p>Il messaggio che emerge per famiglie e scuole non è un divieto assoluto generico, ma la cautela sull’età di ingresso e sulla quantità di tempo: prima si inizia e più intensivo è l’uso, più compaiono nelle ricerche correlazioni con attenzione e voti.</p>`,
  sources:[
    {name:"The Guardian — social media e attenzione nei minori", url:"https://www.theguardian.com/"},
    {name:"Studio Milano-Bicocca / Nature coverage — età di ingresso ai social e voti", note:"adolescenti italiani, confronto longitudinale"},
    {name:"Karolinska Institute / OHSU — social e sintomi di disattenzione", note:"coorte USA 10–14 anni"}
  ]
},


eu_ai_act_trasparenza:{
  title:"EU AI Act: scattano gli obblighi di trasparenza sui contenuti generati dall’IA",
  shortTitle:"EU AI Act: obblighi di trasparenza IA",
  excerpt:"In Europa entrano in vigore le regole di trasparenza dell’AI Act: marcature e filigrane per contenuti generati o manipolati dall’intelligenza artificiale.",
  cat:"politica", sub:"europa",
  badge:"Tecnologia · Ultima ora", badgeClass:"",
  meta:"UE · Normative · Agosto 2026",
  featured:false, ultimaOra:true,
  img:"",
  cardImg:"",
  body:`<p>Nell’Unione europea sono entrati in vigore gli obblighi di trasparenza previsti dall’EU AI Act per sviluppatori e imprese che immettono sul mercato sistemi e contenuti basati sull’intelligenza artificiale.</p>
<p>Le nuove regole riguardano in particolare i contenuti generati o manipolati dall’IA — immagini, video (inclusi deepfake), testi e audio — e richiedono marcature visibili oppure filigrane digitali leggibili dai sistemi, in modo che gli utenti possano riconoscere la natura artificiale del materiale.</p>
<p>L’obiettivo dichiarato del legislatore europeo è aumentare la chiarezza per i consumatori e ridurre i rischi di disinformazione legati a contenuti sintetici difficili da distinguere da quelli reali.</p>
<p>Gli obblighi si applicano lungo la filiera: chi sviluppa i modelli e chi li integra in prodotti o servizi deve valutare come rendere identificabile l’output generato dall’IA, nei limiti e con le modalità previsti dal regolamento.</p>
<p>Le imprese che operano nell’UE o rivolgendosi al mercato europeo sono chiamate ad adeguare processi, interfacce e documentazione. Il quadro normativo resta soggetto a orientamenti attuativi e a controlli delle autorità competenti negli Stati membri.</p>`,
  sources:[
    {name:"Cooley — analisi obblighi EU AI Act / trasparenza", url:"https://www.cooley.com/"},
    {name:"Quadro normativo UE — AI Act (trasparenza contenuti)", note:"sintesi obblighi in vigore per sviluppatori e provider"}
  ]
},
spiderman_brand_new_day:{
  title:"Spider-Man: Brand New Day, esordio da record: circa 932 milioni di dollari nel weekend di apertura",
  shortTitle:"Spider-Man da record al botteghino",
  excerpt:"Il nuovo film Spider-Man: Brand New Day incassa circa 932 milioni di dollari nel weekend d’esordio globale, tra le aperture più alte della storia del cinema.",
  cat:"cinema", sub:"cinema_novita",
  badge:"Cinema · In evidenza", badgeClass:"",
  meta:"The Guardian · Botteghino",
  featured:true, ultimaOra:false,
  img:"",
  cardImg:"",
  body:`<p>Il film Spider-Man: Brand New Day ha registrato un incasso globale di circa 932 milioni di dollari nel weekend di apertura, secondo i dati di botteghino riportati dalla stampa internazionale.</p>
<p>Si tratta di una delle debut performance più elevate mai registrate al cinema, in un mercato in cui le grandi produzioni supereroistiche restano tra i titoli capaci di mobilizzare pubblici in più continenti nello stesso fine settimana.</p>
<p>Il risultato combina vendite nei mercati nordamericani e internazionali e conferma la forza del marchio Spider-Man presso un pubblico ampio, non solo tra i fan del genere.</p>
<p>Le aperture di questa portata influenzano le strategie degli studi su sequels, finestre di uscita e campagne globali. I dati definitivi di lungo periodo dipenderanno dalle settimane successive al debutto.</p>
<p>Per il settore dell’intrattenimento, il record di Brand New Day resta comunque un segnale rilevante sulla tenuta del grande schermo per i titoli di massimo richiamo.</p>`,
  sources:[
    {name:"The Guardian — botteghino Spider-Man: Brand New Day", url:"https://www.theguardian.com/"}
  ]
},
opec_produzione_settembre:{
  title:"OPEC+: sette paesi aumentano la produzione di greggio di circa 188.000 barili al giorno da settembre",
  shortTitle:"OPEC+: più greggio da settembre",
  excerpt:"Arabia Saudita, Russia e altri cinque paesi OPEC+ concordano un aumento graduale della produzione di petrolio per circa 188.000 barili/giorno da settembre.",
  cat:"crypto", sub:"mercati",
  badge:"Energia · Mercati", badgeClass:"",
  meta:"Reuters / Anadolu Agency",
  featured:false, ultimaOra:false,
  img:"",
  cardImg:"",
  body:`<p>Sette paesi del gruppo OPEC+, tra cui Arabia Saudita e Russia, hanno concordato un aumento graduale della produzione di greggio pari a circa 188.000 barili al giorno a partire da settembre.</p>
<p>La decisione arriva in un contesto di forte volatilità sui mercati energetici, legata anche alle incertezze sulle rotte di trasporto e agli equilibri geopolitici in Medio Oriente.</p>
<p>L’obiettivo dichiarato dell’accordo è contribuire a stabilizzare i listini globali del petrolio dopo fasi di tensioni sui prezzi e sui rischi di approvvigionamento.</p>
<p>Analisti e operatori guardano ora all’effettiva implementazione dell’aumento e alla reazione di domanda e scorte nei prossimi mesi. Ogni aggiustamento OPEC+ si riflette rapidamente su Brent, WTI e aspettative di inflazione energetica.</p>
<p>I mercati finanziari restano sensibili ai comunicati del gruppo e ai dati settimanali su scorte e consumi, oltre che agli sviluppi politici nelle principali aree di produzione e transito.</p>`,
  sources:[
    {name:"Reuters — decisioni OPEC+ e mercati petroliferi", url:"https://www.reuters.com/"},
    {name:"Anadolu Agency — aumento produzione OPEC+", url:"https://www.aa.com.tr/"}
  ]
},
fifa_tensioni_diritti:{
  title:"FIFA sotto pressione: federazioni europee in tensione sui piani commerciali dei Mondiali",
  shortTitle:"FIFA: tensione con le federazioni europee",
  excerpt:"Scontro tra FIFA e diverse federazioni europee, tra cui la FA inglese, sulle proposte di ristrutturazione dei diritti commerciali legati ai tornei mondiali.",
  cat:"sport", sub:"calcio",
  badge:"Calcio · Governance", badgeClass:"",
  meta:"Al Jazeera · FIFA",
  featured:false, ultimaOra:false,
  img:"",
  cardImg:"",
  body:`<p>È emersa una tensione crescente tra la FIFA e diverse federazioni calcistiche europee riguardo alle proposte di ristrutturazione dei diritti commerciali legati ai tornei mondiali.</p>
<p>Tra i soggetti citati nel dibattito figura anche la Football Association inglese. Leghe e federazioni europee hanno sollevato riserve sulle linee commerciali avanzate dalla governance FIFA e, secondo quanto riportato, hanno ventilato azioni legali e un possibile ritiro del sostegno politico all’attuale impostazione.</p>
<p>Al centro della disputa ci sono il controllo e la distribuzione del valore generato da diritti media, sponsorizzazioni e formato degli eventi globali, temi che toccano bilanci delle federazioni e calendari del calcio europeo.</p>
<p>La FIFA difende la propria autonomia nella gestione dei competizioni internazionali; le federazioni europee chiedono maggiore coinvolgimento e tutele sugli effetti delle riforme commerciali.</p>
<p>Gli sviluppi dei prossimi mesi — negoziati, eventuali ricorsi o mediazioni — saranno decisive per capire se si arriverà a un compromesso o a un braccio di ferro prolungato nella governance del calcio mondiale.</p>`,
  sources:[
    {name:"Al Jazeera — tensioni FIFA e federazioni europee", url:"https://www.aljazeera.com/"}
  ]
},

oro_petrolio_iran:{title:"Oro in rialzo e petrolio in calo dopo lo stop di Trump agli attacchi sull’Iran",shortTitle:"Oro su, petrolio giù dopo i segnali su Iran",excerpt:"Oro in rialzo e petrolio in forte calo dopo i segnali di Trump su Iran e accordo: spot vicino ai 4.068 $/oz, focus sui dati del lavoro USA.",cat:"crypto",sub:"mercati",badge:"Mercati · Ultima ora",badgeClass:"",meta:"Reuters · 3 agosto 2026",img:"",cardImg:"",featured:false,ultimaOra:true,sources:[{"name": "Reuters — Ashitha Shivaprasad, 3 agosto 2026", "url": "https://www.reuters.com/"}, {"name": "Quotazioni oro e petrolio (mercato spot/future)", "note": "dati di seduta citati nel pezzo"}],body:""},
scienza_cervello_fase:{title:"Tra 50 e 75 anni il cervello entra in una fase biologica distinta",shortTitle:"Nuova fase del cervello dopo i 50",excerpt:"Uno studio a livello di singola cellula descrive cambiamenti immunitari e di regolazione genica tra la mezza età e l’età avanzata.",cat:"scienza",sub:"scoperte",badge:"Scienza \u00b7 Agosto 2026",badgeClass:"",meta:"Neuroscienze \u00b7 Studio",img:"",cardImg:"",featured:false,ultimaOra:false,sources:[{"name": "SciTechDaily — sintesi studio single-cell, 2 agosto 2026", "url": "https://scitechdaily.com/"}, {"name": "Letteratura peer-reviewed su invecchiamento cerebrale", "note": "riferimento al lavoro citato nelle rassegne"}],body:""},
politica_hormuz_agosto:{title:"Usa-Iran: Trump parla di stop all’attacco e di accordo su Hormuz",shortTitle:"Hormuz e tregua: cosa dicono le fonti",excerpt:"All’inizio di agosto 2026 il presidente USA lega la rinuncia a un attacco a un accordo rapido su Stretto di Hormuz e dossier nucleare iraniano.",cat:"politica",sub:"geopolitica",badge:"Mondo \u00b7 Geopolitica",badgeClass:"",meta:"Medio Oriente \u00b7 Agosto 2026",img:"",cardImg:"",featured:false,ultimaOra:false,sources:[{"name": "Sky TG24 — dirette e dichiarazioni Usa-Iran, agosto 2026", "url": "https://tg24.sky.it/"}, {"name": "Dichiarazioni pubbliche su Truth Social / canali ufficiali", "note": "come riportato dalle agenzie"}],body:""},
cinema_ted_lasso_4:{title:"Ted Lasso 4 su Apple TV+: dal 5 agosto una nuova sfida a Richmond",shortTitle:"Ted Lasso 4: data e trama",excerpt:"La quarta stagione della comedy premiata torna con Jason Sudeikis: Ted allena una squadra femminile di seconda divisione.",cat:"cinema",sub:"serie_tv",badge:"Serie TV \u00b7 Agosto 2026",badgeClass:"",meta:"Apple TV+ \u00b7 Uscite",img:"",cardImg:"",featured:false,ultimaOra:false,sources:[{"name": "Apple TV+ — programmazione agosto 2026", "url": "https://tv.apple.com/"}, {"name": "Elle / Repubblica Spettacoli — calendari serie agosto 2026", "url": "https://www.repubblica.it/"}],body:""},
crypto_btc_agosto:{title:"Bitcoin intorno ai 63.000$: Fed hawkish e maxi-furto da wallet hardware",shortTitle:"Bitcoin: prezzi e rischio wallet",excerpt:"A inizio agosto 2026 BTC oscilla vicino ai 63.000 dollari mentre il mercato digerisce toni restrittivi della Fed e un attacco da oltre 70 milioni a indirizzi Coldcard.",cat:"crypto",sub:"mercati",badge:"Crypto \u00b7 Mercati",badgeClass:"",meta:"Bitcoin \u00b7 Sicurezza",img:"",cardImg:"",featured:false,ultimaOra:false,sources:[{"name": "CoinDesk / CryptoTicker — mercati e sicurezza wallet, agosto 2026", "url": "https://www.coindesk.com/"}, {"name": "Galaxy Research — analisi incidente hardware wallet", "note": "come riportato dalla stampa di settore"}],body:""},
spazio_roman_telescopio:{title:"NASA: completato il rifornimento del telescopio Roman, lancio verso fine agosto",shortTitle:"Telescopio Roman pronto al lancio",excerpt:"Al Kennedy Space Center è terminato il carico di idrazina sul Nancy Grace Roman Space Telescope. Obiettivo di lancio: non prima del 30 agosto 2026.",cat:"spazio",sub:"astrofisica",badge:"Spazio \u00b7 NASA",badgeClass:"",meta:"Missioni \u00b7 2026",img:"",cardImg:"",featured:false,ultimaOra:false,sources:[{"name": "NASA — blog missione Nancy Grace Roman Space Telescope", "url": "https://science.nasa.gov/"}, {"name": "Kennedy Space Center — aggiornamenti rifornimento e lancio", "url": "https://www.nasa.gov/"}],body:""},
nba_lebron_sixers:{title:"LeBron James ai 76ers: la free agency 2026 cambia l’Est",shortTitle:"LeBron James firma con i 76ers",excerpt:"LeBron James si lega ai Philadelphia 76ers: contratto biennale e nuovo assetto in Eastern Conference dopo l’addio ai Lakers.",cat:"sport",sub:"nba",badge:"NBA · Ultima ora",badgeClass:"",meta:"NBA · Free agency 2026",img:"",cardImg:"",featured:true,ultimaOra:false,sources:[{"name": "NBA.com / comunicati e ricostruzioni free agency 2026", "url": "https://www.nba.com/"}, {"name": "ESPN, The Athletic — reportistica free agency", "url": "https://www.espn.com/nba/"}],body:""},
ceuta_crisi:{title:"Ceuta, migranti e confini: l’Europa discute Schengen mentre la crisi si sposta",shortTitle:"Ceuta e i confini europei",excerpt:"Dopo l’afflusso verso l’exclave spagnola, diversi paesi parlano di controlli. Cosa significa per Schengen.",cat:"politica",sub:"europa",badge:"Politica · Europa",badgeClass:"mondo",meta:"2 ago 2026 · 7 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
iran_tregua:{title:"Trump sospende gli attacchi all’Iran: in bilico un accordo e lo Stretto di Hormuz",shortTitle:"Tregua Iran e Stretto di Hormuz",excerpt:"Washington parla di parametri di un deal. Teheran smentisce. Cosa succede allo stretto più strategico del mondo.",cat:"politica",sub:"geopolitica",badge:"Politica · Geopolitica",badgeClass:"mondo",meta:"2 ago 2026 · 7 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
antartide:{title:"Hanno trovato qualcosa di impossibile sotto il ghiaccio dell’Antartide",shortTitle:"Tunnel sotto l’Antartide",excerpt:"Una rete di cavità che i modelli non prevedevano.",cat:"scienza",sub:"",badge:"Scienza · Scoperta",badgeClass:"scienza",meta:"1 ago 2026 · 7 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
funghi:{title:"I funghi comunicano sotto terra con una rete nascosta",shortTitle:"La rete segreta dei funghi",excerpt:"Sotto il suolo delle foreste esiste una rete di filamenti fungini — il micelio — che collega radici di piante diverse. Attraverso queste ife…",cat:"scienza",sub:"",badge:"Scienza · Natura",badgeClass:"scienza",meta:"30 lug 2026 · 7 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
sbadiglio:{title:"Perché sbadigliamo (e perché è contagioso)",shortTitle:"Il mistero dello sbadiglio",excerpt:"Lo sbadiglio è un comportamento quasi universale nei vertebrati. Si manifesta come inspirazione ampia, apertura prolungata della bocca e chi…",cat:"scienza",sub:"",badge:"Scienza · Comportamento",badgeClass:"scienza",meta:"29 lug 2026 · 7 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
octopodi:{title:"I polpi hanno tre cuori e un’intelligenza aliena",shortTitle:"L’intelligenza aliena dei polpi",excerpt:"Il polpo comune e altre specie di cefalopodi hanno tre cuori: due branchiali che spingono il sangue verso le branchie e uno sistemico che lo…",cat:"scienza",sub:"",badge:"Scienza · Biologia",badgeClass:"scienza",meta:"28 lug 2026 · 7 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
sonno_animali:{title:"Alcuni animali dormono con metà cervello alla volta",shortTitle:"Sonno uni-emisferico",excerpt:"Delfini, focene e alcune foche risolvono un problema apparente: dormire senza annegare. La risposta fisiologica è il sonno uniemisferico: un…",cat:"scienza",sub:"",badge:"Scienza · Sonno",badgeClass:"scienza",meta:"27 lug 2026 · 7 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
gatti:{title:"Perché i gatti ti fissano mentre dormi",shortTitle:"I gatti che ti fissano di notte",excerpt:"Chi convive con un gatto conosce la sensazione di essere osservato al buio. Non è solo impressione: i felini domestici hanno un apparato vis…",cat:"animali",sub:"",badge:"Animali · Comportamento",badgeClass:"animali",meta:"1 ago 2026 · 7 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
corvi:{title:"I corvi sono più intelligenti di molti mammiferi",shortTitle:"L’intelligenza dei corvi",excerpt:"I corvidi — corvi, cornacchie e gazze — sono al centro di decenni di studi su cognizione animale. Laboratori in Europa, Giappone e Nuova Zel…",cat:"animali",sub:"",badge:"Animali · Intelligenza",badgeClass:"animali",meta:"1 ago 2026 · 6 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
elefanti:{title:"Gli elefanti non dimenticano (e piangono i morti)",shortTitle:"La memoria degli elefanti",excerpt:"Riconoscono ossa e mostrano comportamenti simili al lutto.",cat:"animali",sub:"",badge:"Animali · Memoria",badgeClass:"animali",meta:"28 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
polpi_animali:{title:"I polpi usano gusci e noci di cocco come scudi",shortTitle:"Polpi che usano utensili",excerpt:"Nel 2009 ricercatori che lavoravano in acque indonesiane hanno documentato polpi (Amphioctopus marginatus) che raccoglievano metà di noci di…",cat:"animali",sub:"",badge:"Animali · Comportamento",badgeClass:"animali",meta:"26 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
cani:{title:"I cani capiscono le nostre emozioni meglio di quanto crediamo",shortTitle:"I cani e le emozioni umane",excerpt:"Il cane domestico ha evoluto, in migliaia di anni di convivenza con Homo sapiens, una sensibilità particolare ai segnali sociali umani. Non …",cat:"animali",sub:"",badge:"Animali · Empatia",badgeClass:"animali",meta:"25 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
cervello:{title:"Il cervello cancella i ricordi mentre dormi",shortTitle:"Il cervello che dimentica di notte",excerpt:"Durante il sonno il cervello non si spegne. Nelle fasi non-REM e REM si riorganizzano tracce di memoria: alcune si consolidano, altre si ind…",cat:"psicologia",sub:"",badge:"Psicologia · Cervello",badgeClass:"psicologia",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
tempo:{title:"Perché il tempo passa più veloce invecchiando",shortTitle:"Il tempo che accelera",excerpt:"Molte persone hanno l’impressione che gli anni scorrono più in fretta con l’età. La psicologia sperimentale ha raccolto dati su questo effet…",cat:"psicologia",sub:"",badge:"Psicologia · Percezione",badgeClass:"psicologia",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
memoria:{title:"Perché non ricordiamo i primi anni di vita",shortTitle:"L’amnesia infantile",excerpt:"La memoria umana non è un registratore fedele. È un insieme di sistemi — di lavoro, episodica, semantica, procedurale — con limiti di capaci…",cat:"psicologia",sub:"",badge:"Psicologia · Memoria",badgeClass:"psicologia",meta:"30 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
decisioni:{title:"Perché prendiamo decisioni peggiori quando siamo stanchi",shortTitle:"Fatica e cattive decisioni",excerpt:"Decidere sotto incertezza coinvolge reti cerebrali di valutazione, controllo e regolazione emotiva. La neuroeconomia e la psicologia cogniti…",cat:"psicologia",sub:"",badge:"Psicologia · Decisioni",badgeClass:"psicologia",meta:"27 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
effetto_placebo:{title:"L’effetto placebo funziona anche se sai che è un placebo",shortTitle:"Il placebo consapevole",excerpt:"L’effetto placebo è un cambiamento reale misurabile dopo un intervento senza principio attivo specifico per quella condizione, mediato da as…",cat:"psicologia",sub:"",badge:"Psicologia · Mente-corpo",badgeClass:"psicologia",meta:"24 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
btc_cosè:{title:"Cos’è Bitcoin in parole semplici (senza tecnicismi inutili)",shortTitle:"Cos’è Bitcoin spiegato semplice",excerpt:"Una moneta digitale senza banche centrali: come funziona l’idea di base.",cat:"crypto",sub:"",badge:"Crypto · Base",badgeClass:"scienza",meta:"2 ago 2026 · 6 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:"<p>Bitcoin è una moneta digitale che non dipende da una banca centrale o da un governo. Nasce nel 2009 da un’idea firmata con lo pseudonimo Satoshi Nakamoto e si basa su una rete di computer che si mettono d’accordo su chi possiede cosa, senza un unico “capo”.</p>\n<p>In pratica, invece di un registro tenuto da una banca, esiste un registro pubblico (la blockchain) aggiornato da migliaia di partecipanti. Le regole sono scritte nel software: quanti bitcoin possono esistere al massimo, come si creano di nuovi, come si trasferiscono.</p>\n<p>Chi lo sostiene sottolinea la scarsità (ne esisteranno al massimo 21 milioni), la possibilità di inviare valore a distanza senza intermediari e l’indipendenza da politiche monetarie nazionali. Chi è scettico sottolinea la volatilità del prezzo, il consumo energetico di alcune reti e i rischi di truffe o perdita delle chiavi di accesso.</p>\n<p>Capire Bitcoin non significa doverci investire. Significa capire un’idea tecnologica e sociale che ha influenzato un intero settore. Come ogni strumento finanziario, comporta rischi: non è un consiglio di investimento, è una spiegazione.</p>\n<p>Se ti avvicini all’argomento, parti dalle basi (cos’è una blockchain, cos’è un wallet, cos’è la volatilità) e diffida di promesse di guadagni facili. Le promesse facili, in questo mondo, sono quasi sempre un segnale d’allarme.</p>"},
blockchain:{title:"Cos’è una blockchain (e perché non serve solo alle crypto)",shortTitle:"Blockchain spiegata facile",excerpt:"Un registro condiviso, difficile da alterare, utile oltre le monete digitali.",cat:"crypto",sub:"",badge:"Crypto · Tecnologia",badgeClass:"scienza",meta:"2 ago 2026 · 6 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
wallet:{title:"Cos’è un wallet crypto e perché “non i tuoi seed, non i tuoi coin”",shortTitle:"Wallet e seed phrase",excerpt:"Le chiavi private sono la vera proprietà. Perderle significa perdere i fondi.",cat:"crypto",sub:"",badge:"Crypto · Sicurezza",badgeClass:"scienza",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
volatilita:{title:"Perché le criptovalute oscillano così tanto",shortTitle:"La volatilità delle crypto",excerpt:"Pochi vincoli, tanta speculazione, liquidità variabile: il prezzo si muove in fretta.",cat:"crypto",sub:"",badge:"Crypto · Mercati",badgeClass:"scienza",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
scam:{title:"Le truffe crypto più comuni (e come riconoscerle)",shortTitle:"Truffe crypto: come difendersi",excerpt:"Promesse di guadagni facili, falsi supporti e link fraudolenti.",cat:"crypto",sub:"",badge:"Crypto · Sicurezza",badgeClass:"scienza",meta:"31 lug 2026 · 6 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
gravita:{title:"Cosa succede al corpo in assenza di gravità",shortTitle:"Il corpo senza gravità",excerpt:"Muscoli, ossa, occhi e equilibrio cambiano in fretta.",cat:"spazio",sub:"",badge:"Spazio · Corpo umano",badgeClass:"spazio",meta:"31 lug 2026 · 6 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
buchi_neri:{title:"Cosa succederebbe se cadiessi in un buco nero",shortTitle:"Cadere in un buco nero",excerpt:"Spaghettificazione e orizzonte degli eventi.",cat:"spazio",sub:"",badge:"Spazio · Astrofisica",badgeClass:"spazio",meta:"28 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
marte_acqua:{title:"Su Marte c’era (e forse c’è ancora) acqua",shortTitle:"Acqua su Marte",excerpt:"Su Marte l’acqua liquida stabile in superficie è ostacolata da pressione e temperatura medie. Ciò non esclude un passato più umido né riserv…",cat:"spazio",sub:"",badge:"Spazio · Marte",badgeClass:"spazio",meta:"26 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
iss:{title:"Come si vive davvero sulla Stazione Spaziale",shortTitle:"Vita sulla ISS",excerpt:"La Stazione Spaziale Internazionale è un laboratorio in orbita bassa, frutto di cooperazione tra agenzie di Stati Uniti, Russia, Europa, Gia…",cat:"spazio",sub:"",badge:"Spazio · Vita in orbita",badgeClass:"spazio",meta:"25 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
luce_sole:{title:"La luce del Sole che vedi è “vecchia” di 8 minuti",shortTitle:"La luce del Sole e i 8 minuti",excerpt:"La luce solare regola il ritmo circadiano attraverso cellule retiniche sensibili alla melanopsina, che inviano segnali all’orologio biologic…",cat:"spazio",sub:"",badge:"Spazio · Luce",badgeClass:"spazio",meta:"23 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
luce:{title:"Non dormire mai con la luce accesa",shortTitle:"Luce accesa e sonno",excerpt:"Anche una luce debole altera melatonina e metabolismo.",cat:"salute",sub:"",badge:"Salute · Sonno",badgeClass:"salute",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
acqua:{title:"Cosa succede se bevi acqua tiepida ogni mattina",shortTitle:"Acqua tiepida al mattino",excerpt:"Il corpo adulto è costituito in larga parte da acqua, con percentuali che variano per età, sesso e composizione corporea. Liquidi intra ed e…",cat:"salute",sub:"",badge:"Salute · Abitudini",badgeClass:"salute",meta:"31 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
camminare:{title:"Camminare 10 minuti dopo i pasti cambia la glicemia",shortTitle:"Camminare dopo mangiato",excerpt:"Camminare è l’attività fisica più accessibile per gran parte della popolazione. Studi osservazionali e interventi controllati la associano a…",cat:"salute",sub:"",badge:"Salute · Movimento",badgeClass:"salute",meta:"29 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
natura:{title:"20 minuti nella natura riducono lo stress",shortTitle:"Natura e stress",excerpt:"L’esposizione a contesti naturali — parchi, boschi, coste — è associata in letteratura a riduzioni auto-riportate di stress e, in alcuni stu…",cat:"salute",sub:"",badge:"Salute · Mente",badgeClass:"salute",meta:"27 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
sonno_ore:{title:"Dormire meno di 6 ore a lungo non si recupera nel weekend",shortTitle:"Il debito di sonno",excerpt:"Per la maggior parte degli adulti, le raccomandazioni internazionali collocano il fabbisogno di sonno intorno alle 7–9 ore per notte, con ec…",cat:"salute",sub:"",badge:"Salute · Sonno",badgeClass:"salute",meta:"25 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
isola:{title:"L’isola che scompare e riappare",shortTitle:"Isole che spariscono",excerpt:"Le isole isolate sono laboratori naturali di evoluzione: popolazioni limitate, risorse finite, predatori assenti o diversi. Da qui tratti co…",cat:"mondo",sub:"",badge:"Mondo · Mistero",badgeClass:"mondo",meta:"31 lug 2026 · 6 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
oceano:{title:"Conosciamo meglio Marte dei fondali oceanici",shortTitle:"Oceano inesplorato",excerpt:"Gli oceani assorbono gran parte del calore in eccesso e una quota rilevante di anidride carbonica antropica. Conseguenze misurate includono …",cat:"mondo",sub:"",badge:"Mondo · Esplorazione",badgeClass:"mondo",meta:"29 lug 2026 · 6 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
deserto:{title:"Il Sahara non è sempre stato un deserto",shortTitle:"Quando il Sahara era verde",excerpt:"I deserti non sono ecosistemi «vuoti». Ospitano organismi con adattamenti a scarsità idrica, escursioni termiche e suoli poveri: da piante a…",cat:"mondo",sub:"",badge:"Mondo · Clima",badgeClass:"mondo",meta:"27 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
citta_sommerse:{title:"Città antiche sotto il mare",shortTitle:"Città sommerse",excerpt:"Resti archeologici sommersi — da strutture portuali a interi abitati — documentano variazioni del livello marino, sprofondamenti locali e ab…",cat:"mondo",sub:"",badge:"Mondo · Archeologia",badgeClass:"mondo",meta:"25 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
aurora:{title:"Come nasce un’aurora boreale",shortTitle:"L’aurora boreale spiegata",excerpt:"L’aurora polare nasce quando particelle cariche del vento solare, guidate dal campo magnetico terrestre, eccitano atomi dell’alta atmosfera.…",cat:"mondo",sub:"",badge:"Mondo · Fenomeni",badgeClass:"mondo",meta:"23 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
pompei:{title:"Pompei non è “congelata nel 79 d.C.” come pensiamo",shortTitle:"Il mito di Pompei",excerpt:"Pompei fu sepolta dall’eruzione del Vesuvio nel 79 d.C. Cenere e materiali piroclastici hanno conservato edifici, oggetti e impronte di corp…",cat:"storia",sub:"",badge:"Storia · Antichità",badgeClass:"storia",meta:"30 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
biblioteca_alessandria:{title:"La Biblioteca di Alessandria non bruciò in un solo giorno",shortTitle:"Il mito di Alessandria",excerpt:"La Biblioteca di Alessandria, nell’Egitto tolemaico, fu il simbolo di un progetto di raccolta del sapere del Mediterraneo antico. Le fonti a…",cat:"storia",sub:"",badge:"Storia · Sapere",badgeClass:"storia",meta:"28 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
vichinghi:{title:"I vichinghi non indossavano elmi con le corna",shortTitle:"Il mito delle corna vichinghe",excerpt:"Tra VIII e XI secolo gruppi scandinavi esplorarono, commerciarono e razziarono su un arco che va dalle isole britanniche alla Rus’, al Medit…",cat:"storia",sub:"",badge:"Storia · Medioevo",badgeClass:"storia",meta:"26 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
mummie:{title:"Le mummie egizie non erano solo per i faraoni",shortTitle:"Mummie oltre i faraoni",excerpt:"La mummificazione egizia mirava a preservare il corpo per l’oltretomba, secondo credenze religiose articolate. Tecniche variarono per epoca …",cat:"storia",sub:"",badge:"Storia · Egitto",badgeClass:"storia",meta:"24 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
strada_roma:{title:"Le strade romane esistono ancora sotto i nostri piedi",shortTitle:"Le strade romane di oggi",excerpt:"La rete stradale romana collegava città, accampamenti e porti con standard costruttivi riconoscibili: strati compattati, drenaggio, basoli i…",cat:"storia",sub:"",badge:"Storia · Roma",badgeClass:"storia",meta:"22 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
pol_geopolitica:{title:"Perché le rotte commerciali stanno ridisegnando la politica mondiale",shortTitle:"Rotte e potere globale",excerpt:"Canali, stretto e nuovi corridoi: chi controlla i passaggi controlla i prezzi.",cat:"politica",sub:"geopolitica",badge:"Politica · Geopolitica",badgeClass:"mondo",meta:"2 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
pol_europa:{title:"L’Europa cerca una linea comune su energia e difesa (ed è più difficile di quanto sembra)",shortTitle:"Europa: energia e difesa",excerpt:"Interessi nazionali diversi, un’unica agenda da costruire.",cat:"politica",sub:"europa",badge:"Politica · Europa",badgeClass:"mondo",meta:"2 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
pol_africa:{title:"L’Africa non è un pezzo unico: 54 paesi, interessi e alleanze in movimento",shortTitle:"Africa: 54 paesi, non un blocco",excerpt:"Risorse, giovani, infrastrutture e nuovi partner globali.",cat:"politica",sub:"africa",badge:"Politica · Africa",badgeClass:"mondo",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
pol_asia:{title:"Indo-Pacifico: il centro di gravità della politica del XXI secolo",shortTitle:"Indo-Pacifico al centro",excerpt:"Commercio, tecnologia e tensioni marittime sullo stesso tavolo.",cat:"politica",sub:"asia",badge:"Politica · Asia",badgeClass:"mondo",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
pol_americhe:{title:"Nord e Sud America: democrazia, economia e migrazioni sullo stesso filo",shortTitle:"Americhe: democrazia e migrazioni",excerpt:"Elezioni, disuguaglianze e flussi umani collegano l’intero continente.",cat:"politica",sub:"americhe",badge:"Politica · Americhe",badgeClass:"mondo",meta:"31 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
cin_film:{title:"Estate 2026 al cinema: blockbuster, autoriali e la lotta per il biglietto",shortTitle:"Estate 2026 al cinema",excerpt:"Cosa attira ancora le persone in sala nell’era dello streaming.",cat:"cinema",sub:"cinema_novita",badge:"Cinema · Nuovi film",badgeClass:"curiosita",meta:"2 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
cin_serie:{title:"Serie TV 2026: meno quantità, più stagioni che restano in testa",shortTitle:"Serie TV: qualità contro quantità",excerpt:"Le piattaforme stringono i budget: sopravvive chi crea dipendenza vera.",cat:"cinema",sub:"serie_tv",badge:"Cinema · Serie TV",badgeClass:"curiosita",meta:"2 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
cin_streaming:{title:"Streaming: abbonamenti, password e la guerra silenziosa dei prezzi",shortTitle:"Streaming e prezzi",excerpt:"Troppi abbonamenti, poca pazienza: le piattaforme cambiano le regole.",cat:"cinema",sub:"streaming",badge:"Cinema · Streaming",badgeClass:"curiosita",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
cin_festival:{title:"Festival e premi: perché contano ancora (anche se non vinci un Oscar)",shortTitle:"Festival e premi",excerpt:"Visibilità, carriere e film che altrimenti non vedresti mai.",cat:"cinema",sub:"festival",badge:"Cinema · Festival",badgeClass:"curiosita",meta:"31 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
sp_calcio:{title:"Calcio 2026: calendari pieni, giocatori stanchi e tifosi sempre più esigenti",shortTitle:"Calcio: calendario e fatica",excerpt:"Più partite, più soldi, più dibattito sulla salute degli atleti.",cat:"sport",sub:"calcio",badge:"Sport · Calcio",badgeClass:"scienza",meta:"2 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
sp_nba:{title:"NBA: ritmo, star e il nuovo equilibrio tra spettacolo e difesa",shortTitle:"NBA: spettacolo e difesa",excerpt:"Il basket USA resta il prodotto sportivo più «serie TV» del mondo.",cat:"sport",sub:"nba",badge:"Sport · NBA",badgeClass:"scienza",meta:"2 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
sp_tennis:{title:"Tennis: il passaggio generazionale è già in campo",shortTitle:"Tennis, nuova generazione",excerpt:"Nuovi nomi, nuovi stili, stessi Slam che decidono le leggende.",cat:"sport",sub:"tennis",badge:"Sport · Tennis",badgeClass:"scienza",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
sp_f1:{title:"Formula 1: tecnologia, regolamenti e lo spettacolo del margine minimo",shortTitle:"F1: margini e regolamenti",excerpt:"Decimi di secondo, strategie e regole che cambiano le gerarchie.",cat:"sport",sub:"f1",badge:"Sport · Formula 1",badgeClass:"scienza",meta:"1 ago 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
sp_altri:{title:"Oltre calcio e NBA: gli sport che meritano più attenzione",shortTitle:"Sport da non perdere",excerpt:"Oltre al calcio e ai grandi circuiti mediatici, decine di discipline costruiscono culture locali e percorsi olimpici: dal canottaggio alle a…",cat:"sport",sub:"altri_sport",badge:"Sport · Altri",badgeClass:"scienza",meta:"31 lug 2026 · 5 min di lettura",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
privacy:{title:"Privacy Policy",shortTitle:"Privacy",excerpt:"",cat:"info",sub:"",badge:"Info",badgeClass:"curiosita",meta:"1 ago 2026",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
contatti:{title:"Contatti",shortTitle:"Contatti",excerpt:"Contatta la redazione di CurioMondo per collaborazioni, segnalazioni o richieste informative.",cat:"info",sub:"",badge:"Info",badgeClass:"scienza",meta:"",img:"",cardImg:"",featured:false,ultimaOra:false,body:""},
};

/* ===== Controllo editoriale e metadati uniformi ===== */
const SOURCE_LIBRARY = {
  scienza:[
    {name:"Nature — ricerca e notizie scientifiche",url:"https://www.nature.com/",note:"approfondimento generale"},
    {name:"Science — rivista e aggiornamenti",url:"https://www.science.org/",note:"approfondimento generale"}
  ],
  mente:[
    {name:"Organizzazione Mondiale della Sanità",url:"https://www.who.int/",note:"salute e prevenzione"},
    {name:"Istituto Superiore di Sanità",url:"https://www.iss.it/",note:"informazioni sanitarie"}
  ],
  salute:[
    {name:"Organizzazione Mondiale della Sanità",url:"https://www.who.int/"},
    {name:"Istituto Superiore di Sanità",url:"https://www.iss.it/"}
  ],
  animali:[
    {name:"Smithsonian's National Zoo & Conservation Biology Institute",url:"https://nationalzoo.si.edu/",note:"biologia e comportamento animale"},
    {name:"Encyclopaedia Britannica — Animal",url:"https://www.britannica.com/animal/animal",note:"quadro generale"}
  ],
  spazio:[
    {name:"NASA — Science",url:"https://science.nasa.gov/"},
    {name:"ESA — European Space Agency",url:"https://www.esa.int/"}
  ],
  mondo:[
    {name:"NOAA — ambiente, oceani e atmosfera",url:"https://www.noaa.gov/"},
    {name:"UNEP — Programma ONU per l'ambiente",url:"https://www.unep.org/"}
  ],
  storia:[
    {name:"Encyclopaedia Britannica — History",url:"https://www.britannica.com/browse/History",note:"inquadramento storico"},
    {name:"Treccani — Storia",url:"https://www.treccani.it/enciclopedia/",note:"consultazione enciclopedica"}
  ],
  politica:[
    {name:"Nazioni Unite — Notizie e documenti",url:"https://www.un.org/"},
    {name:"Reuters — World",url:"https://www.reuters.com/world/",note:"aggiornamenti internazionali"}
  ],
  cinema:[
    {name:"Internet Movie Database",url:"https://www.imdb.com/",note:"schede e crediti"},
    {name:"The Academy of Motion Picture Arts and Sciences",url:"https://www.oscars.org/",note:"archivio e industria cinematografica"}
  ],
  sport:[
    {name:"Comitato Olimpico Internazionale",url:"https://olympics.com/ioc"},
    {name:"BBC Sport",url:"https://www.bbc.com/sport",note:"risultati e approfondimenti"}
  ],
  crypto:[
    {name:"Banca d'Italia — Educazione finanziaria",url:"https://economiapertutti.bancaditalia.it/"},
    {name:"CONSOB — Avvertenze per i risparmiatori",url:"https://www.consob.it/",note:"rischi e tutela"}
  ],
  biblioteca:[
    {name:"Treccani — Enciclopedia",url:"https://www.treccani.it/enciclopedia/",note:"inquadramento generale"},
    {name:"Google Scholar",url:"https://scholar.google.com/",note:"ricerca di letteratura scientifica"}
  ],
  info:[{name:"CurioMondo — redazione",note:"contenuto informativo del sito"}]
};
const IMAGE_FALLBACKS={
 scienza:"https://images.unsplash.com/photo-1532094349884-543bc11b234d?w=1400&q=82&auto=format&fm=webp",
 mente:"https://images.unsplash.com/photo-1506126613408-eca07ce68773?w=1400&q=82&auto=format&fm=webp",
 salute:"https://images.unsplash.com/photo-1505751172876-fa1923c5c528?w=1400&q=82&auto=format&fm=webp",
 animali:"https://images.unsplash.com/photo-1474511320723-9a56873867b5?w=1400&q=82&auto=format&fm=webp",
 spazio:"https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=1400&q=82&auto=format&fm=webp",
 mondo:"https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1400&q=82&auto=format&fm=webp",
 storia:"https://images.unsplash.com/photo-1461360370896-922624d12aa1?w=1400&q=82&auto=format&fm=webp",
 politica:"https://images.unsplash.com/photo-1529107386315-e1a2ed48a620?w=1400&q=82&auto=format&fm=webp",
 cinema:"https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1400&q=82&auto=format&fm=webp",
 sport:"https://images.unsplash.com/photo-1461896836934-ffe607ba8211?w=1400&q=82&auto=format&fm=webp",
 crypto:"https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=1400&q=82&auto=format&fm=webp",
 biblioteca:"https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=1400&q=82&auto=format&fm=webp"
};
function cleanArticleBody(body){
  if(!body) return "";
  let out=String(body)
    .replace(/Canali, stretto e nuovi corridoi:/g,"Canali, stretti e nuovi corridoi:")
    .replace(/\btermini, templi\b/g,"terme, templi")
    .replace(/\bdebate\b/g,"dibattito")
    .replace(/\bNorse\b/g,"norrena");
  const parts=out.match(/<p[^>]*>[\s\S]*?<\/p>|<h[2-4][^>]*>[\s\S]*?<\/h[2-4]>|<ul[^>]*>[\s\S]*?<\/ul>|<ol[^>]*>[\s\S]*?<\/ol>/gi);
  if(!parts) return out;
  const seen=new Set();
  return parts.filter(part=>{
    const key=part.replace(/<[^>]+>/g," ").replace(/\s+/g," ").trim().toLowerCase();
    if(!key || seen.has(key)) return false;
    seen.add(key); return true;
  }).join("\n");
}
function articleWordCount(body){
  return String(body||"").replace(/<[^>]*>/g," ").replace(/&[^;]+;/g," ").trim().split(/\s+/).filter(Boolean).length;
}
function articleReadLabel(body){
  const words=articleWordCount(body);
  const mins=Math.max(1,Math.ceil(words/210));
  return mins===1 ? "1 min di lettura" : mins+" min di lettura";
}
function enhanceAllArticles(){
  Object.keys(articles).forEach(id=>{
    const a=articles[id];
    if(!a.img) a.img=IMAGE_FALLBACKS[a.cat]||IMAGE_FALLBACKS.biblioteca;
    if(!a.cardImg) a.cardImg=a.img;
    if(a.excerpt) a.excerpt=a.excerpt.replace(/\s*…$/, "…");
  });
}
function ensureArticleDetail(a){
  if(!a||a._cmDetailReady)return a;
  a.body=cleanArticleBody(a.body||"");
  if(!a.sources||!a.sources.length)a.sources=(SOURCE_LIBRARY[a.cat]||SOURCE_LIBRARY.info).map(x=>Object.assign({},x));
  a.readLabel=articleReadLabel(a.body);
  a._cmDetailReady=true;
  return a;
}
enhanceAllArticles();


const taxonomy = {
  all: { label: "Tutte", cats: null, subs: [] },
  scienza: { label: "Scienze & Natura", cats: ["scienza"], subs: [
    {id:"scoperte",label:"Scoperte"},{id:"biologia",label:"Biologia"},{id:"comportamento_sci",label:"Comportamento"},{id:"natura",label:"Natura"}
  ]},
  mente: { label: "Mente & Corpo", cats: ["psicologia","salute"], subs: [
    {id:"cervello",label:"Cervello"},{id:"percezione",label:"Percezione"},{id:"sonno",label:"Sonno"},{id:"abitudini",label:"Abitudini"},{id:"movimento",label:"Movimento"}
  ]},
  animali: { label: "Animali", cats: ["animali"], subs: [
    {id:"intelligenza",label:"Intelligenza"},{id:"comportamento",label:"Comportamento"},{id:"empatia",label:"Empatia"},{id:"memoria",label:"Memoria"}
  ]},
  spazio: { label: "Spazio & Pianeta", cats: ["spazio","mondo"], subs: [
    {id:"astrofisica",label:"Astrofisica"},{id:"corpo_umano",label:"Corpo nello spazio"},{id:"pianeti",label:"Pianeti"},{id:"terra",label:"Terra & Oceani"},{id:"fenomeni",label:"Fenomeni"}
  ]},
  storia: { label: "Storia", cats: ["storia"], subs: [
    {id:"antichita",label:"Antichità"},{id:"miti",label:"Miti da sfatare"},{id:"medioevo",label:"Medioevo"},{id:"sapere",label:"Sapere antico"}
  ]},
  politica: { label: "Politica nel mondo", cats: ["politica"], subs: [
    {id:"geopolitica",label:"Geopolitica"},{id:"europa",label:"Europa"},{id:"africa",label:"Africa"},{id:"asia",label:"Asia"},{id:"americhe",label:"Americhe"}
  ]},
  cinema: { label: "Cinema & Serie", cats: ["cinema"], subs: [
    {id:"cinema_novita",label:"Nuovi film"},{id:"serie_tv",label:"Serie TV"},{id:"streaming",label:"Streaming"},{id:"festival",label:"Festival"}
  ]},
  sport: { label: "Sport", cats: ["sport"], subs: [
    {id:"calcio",label:"Calcio"},{id:"nba",label:"NBA"},{id:"tennis",label:"Tennis"},{id:"f1",label:"Formula 1"},{id:"altri_sport",label:"Altri sport"}
  ]},
  crypto: { label: "Crypto & Denaro", cats: ["crypto"], subs: [
    {id:"basi",label:"Basi"},{id:"tecnologia",label:"Tecnologia"},{id:"sicurezza",label:"Sicurezza"},{id:"mercati",label:"Mercati"}
  ]}
};


function showToast(msg) {
  const t = document.getElementById("toast");
  if (!t) return;
  t.textContent = msg;
  t.classList.add("show");
  clearTimeout(showToast._tm);
  showToast._tm = setTimeout(() => t.classList.remove("show"), 2200);
}
function setLastRead(id) {
  try { localStorage.setItem("cm_last", id); } catch(e) {}
  renderContinue();
}
function getLastRead() {
  try { return localStorage.getItem("cm_last"); } catch(e) { return null; }
}
function clearLastRead(ev) {
  if (ev) { ev.stopPropagation(); ev.preventDefault(); }
  try { localStorage.removeItem("cm_last"); } catch(e) {}
  renderContinue();
}
function renderContinue() {
  const bar = document.getElementById("continueBar");
  if (!bar) return;
  const id = getLastRead();
  if (!id || !articles[id]) {
    bar.classList.remove("on");
    return;
  }
  // hide if currently viewing that article
  const view = document.getElementById("articleView");
  if (view && view.classList.contains("open")) {
    bar.classList.remove("on");
    return;
  }
  const a = articles[id];
  document.getElementById("continueImg").style.backgroundImage = "url('" + (a.cardImg || a.img || "") + "')";
  document.getElementById("continueTitle").textContent = a.shortTitle || a.title;
  bar.classList.add("on");
  const link = document.getElementById("continueLink");
  if (link) {
    link.href = (typeof EXTERNAL_PAGES !== "undefined" && EXTERNAL_PAGES[id]) || ("#articolo=" + encodeURIComponent(id));
    link.onclick = function(e) { e.preventDefault(); openArticle(id); };
  }
  const cx = document.getElementById("continueClose");
  if (cx) cx.onclick = clearLastRead;
}

function updateArtProgress() {
  const view = document.getElementById("articleView");
  const bar = document.getElementById("artProgress");
  if (!view || !bar || !view.classList.contains("open")) return;
  const max = view.scrollHeight - view.clientHeight;
  const p = max > 0 ? (view.scrollTop / max) * 100 : 0;
  bar.style.width = Math.min(100, Math.max(0, p)) + "%";
}

let currentMain = "all";
let currentSub = "all";
const navStack = [{type:"home"}];

function stripHtml(s) {
  const d = document.createElement("div");
  d.innerHTML = s || "";
  return (d.textContent || "").replace(/\s+/g," ").trim();
}
function calcReadTime(body) {
  const w = stripHtml(body).split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.round(w / 200));
}
function favs() {
  try { return JSON.parse(localStorage.getItem("cm_favs") || "[]"); } catch(e) { return []; }
}
function saveFavs(a) { localStorage.setItem("cm_favs", JSON.stringify(a)); }
function isFav(id) { return favs().includes(id); }
function toggleFav(id) {
  let a = favs();
  if (a.includes(id)) {
    a = a.filter(x => x !== id);
    saveFavs(a);
    showToast("Rimosso dai preferiti");
  } else {
    a.push(id);
    saveFavs(a);
    showToast("Salvato nei preferiti");
  }
  renderArticle(id);
}
function toggleTheme() {
  document.body.classList.toggle("dark");
  const isDark = document.body.classList.contains("dark");
  localStorage.setItem("cm_theme", isDark ? "dark" : "light");
  const lab = document.getElementById("themeLabelDrawer");
  if (lab) lab.textContent = isDark ? "Modalità chiara" : "Modalità scura";
}
function initTheme() {
  if (localStorage.getItem("cm_theme") === "dark") {
    document.body.classList.add("dark");
    const lab = document.getElementById("themeLabelDrawer");
    if (lab) lab.textContent = "Modalità chiara";
  }
}


/* ===== Auto-scroll articoli ===== */
let autoTimer = null;
let autoPaused = false;
let autoIdx = 0;

function stopAutoRail() {
  if (autoTimer) {
    clearInterval(autoTimer);
    autoTimer = null;
  }
}
function pauseAutoRail() {
  autoPaused = true;
  stopAutoRail();
  const w = document.getElementById("autoRailWrap");
  if (w) w.classList.add("paused");
}
function resumeAutoRail() {
  // riprende solo se utente non ha toccato; dopo tocco resta in pausa finché non ricarica o torna home
}
function cmApplyLazyBackgrounds(root) {
  if (!root) return;
  const nodes = Array.from(root.querySelectorAll('[data-cm-bg]'));
  const load = el => {
    if (!el || !el.dataset.cmBg) return;
    el.style.backgroundImage = "url('" + el.dataset.cmBg.replace(/'/g, "%27") + "')";
    delete el.dataset.cmBg;
  };
  if (!("IntersectionObserver" in window)) {
    nodes.forEach(load);
    return;
  }
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      load(entry.target);
      observer.unobserve(entry.target);
    });
  }, { rootMargin: "160px 80px" });
  nodes.forEach(node => observer.observe(node));
}
function buildAutoRail() {
  if (window.CM_INITIALIZING) return;
  const rail = document.getElementById("autoRail");
  const wrap = document.getElementById("autoRailWrap");
  if (!rail || !wrap) return;
  // solo in home feed (non in pagina categoria)
  if (typeof isCategoryPage === "function" && isCategoryPage()) {
    wrap.style.display = "none";
    stopAutoRail();
    return;
  }
  wrap.style.display = "";
  const ids = Object.keys(articles).filter(k => {
    const a = articles[k];
    return a && a.cat !== "info" && a.cat !== "biblioteca";
  }).slice(0, 12);
  // priorità: featured, ultimaOra, poi altri
  ids.sort((a, b) => {
    const sa = (articles[a].featured ? 2 : 0) + (articles[a].ultimaOra ? 1 : 0);
    const sb = (articles[b].featured ? 2 : 0) + (articles[b].ultimaOra ? 1 : 0);
    return sb - sa;
  });
  rail.innerHTML = ids.map(function(id) {
    const a = articles[id];
    return '<article class="auto-card ' + (a.ultimaOra ? 'auto-breaking ' : '') + (a.featured ? 'auto-featured' : '') + '" data-id="' + id + '" onclick="openArticle(\'' + id + '\')">' +
      '<div class="athumb" data-cm-bg="' + (a.cardImg || a.img || "").replace(/&/g, "&amp;").replace(/\"/g, "&quot;") + '"></div>' +
      '<div class="abody"><div class="ameta">' + (a.badge || a.cat || "") + '</div>' +
      '<h3>' + (a.shortTitle || a.title || "") + '</h3><p>' + (a.excerpt || "") + '</p></div></article>';
  }).join("");
  cmApplyLazyBackgrounds(rail);

  autoIdx = 0;
  autoPaused = false;
  wrap.classList.remove("paused");
  startAutoRail();
  bindAutoRailTouch();
}
function startAutoRail() {
  stopAutoRail();
  if (autoPaused) return;
  const rail = document.getElementById("autoRail");
  if (!rail || !rail.children.length) return;
  autoTimer = setInterval(() => {
    if (autoPaused) return;
    const cards = rail.querySelectorAll(".auto-card");
    if (!cards.length) return;
    autoIdx = (autoIdx + 1) % cards.length;
    const el = cards[autoIdx];
    const left = el.offsetLeft - 8;
    rail.scrollTo({ left: left, behavior: "smooth" });
  }, 3200);
}
function bindAutoRailTouch() {
  const rail = document.getElementById("autoRail");
  const wrap = document.getElementById("autoRailWrap");
  if (!rail || rail._autoBound) return;
  rail._autoBound = true;
  const pause = () => pauseAutoRail();
  rail.addEventListener("touchstart", pause, { passive: true });
  rail.addEventListener("mousedown", pause);
  rail.addEventListener("wheel", pause, { passive: true });
  // anche tocco generale sulla home ferma lo scorrimento
  document.addEventListener("touchstart", function onFirstTouch(e) {
    if (!document.getElementById("articleView").classList.contains("open")) {
      pauseAutoRail();
    }
  }, { passive: true, once: false });
}

function pickFeatured() {
  const ids = Object.keys(articles).filter(k => articles[k].cat !== "info");
  // Primo piano: la notizia più recente registrata dal flusso editoriale.
  const newest = Array.isArray(window.CM_LATEST_NEWS) ? window.CM_LATEST_NEWS : [];
  let feat = newest.find(id => articles[id] && articles[id].cat !== "info");
  if (!feat) feat = ids.find(id => articles[id].ultimaOra) || ids[0];
  // In evidenza: una storia forte diversa dal primo piano.
  let late = ids.find(id => id !== feat && articles[id].featured);
  if (!late) late = ids.find(id => id !== feat && articles[id].badge && /forte rilievo|record|storica|emergenza|nuovo sviluppo/i.test(articles[id].badge + " " + (articles[id].meta || "")));
  if (!late) late = ids.find(id => id !== feat) || feat;
  return { feat, late };
}

function matches(id, main, sub) {
  const a = articles[id];
  if (!a || a.cat === "info") return false;
  if (main === "all") return a.cat !== "biblioteca";
  const tax = taxonomy[main];
  if (!tax || !tax.cats) return false;
  if (!tax.cats.includes(a.cat)) return false;
  if (sub && sub !== "all") {
    if (a.sub) return a.sub === sub;
    return true;
  }
  return true;
}


function isCategoryPage() {
  return currentMain && currentMain !== "all";
}
function updateFeedChrome() {
  const feat = document.getElementById("featured");
  const late = document.getElementById("latest");
  const banner = document.getElementById("catPageBanner");
  const cont = document.getElementById("continueBar");
  const catPage = isCategoryPage();
  if (feat) feat.style.display = catPage ? "none" : "";
  if (late) late.style.display = catPage ? "none" : "";
  if (banner) {
    if (catPage) {
      banner.classList.add("on");
      const tax = taxonomy[currentMain];
      const label = document.getElementById("catPageLabel");
      let t = tax ? tax.label : currentMain;
      if (currentSub && currentSub !== "all" && tax && tax.subs) {
        const s = tax.subs.find(x => x.id === currentSub);
        if (s) t = tax.label + " · " + s.label;
      }
      if (label) label.textContent = t;
    } else {
      banner.classList.remove("on");
    }
  }
  if (cont && catPage) cont.classList.remove("on");
  const arw = document.getElementById("autoRailWrap");
  if (arw) {
    if (catPage) { arw.style.display = "none"; stopAutoRail(); }
    else { arw.style.display = ""; }
  }
  if (cont && !catPage) renderContinue();
}
function goHomeFeed() {
  currentMain = "all";
  currentSub = "all";
  renderCats();
  renderSubs();
  renderHero();
  try { updateCards3D(); } catch(e) {}
  renderCards();
  updateFeedChrome();
  window.scrollTo(0, 0);
}

function renderCats() {
  const bar = document.getElementById("catBar");
  bar.innerHTML = Object.keys(taxonomy).filter(k => k !== "all").map(k => {
    const t = taxonomy[k];
    return `<button type="button" class="cat-pill ${k===currentMain?"active":""}" data-main="${k}">${t.label}</button>`;
  }).join("");
  bar.querySelectorAll(".cat-pill").forEach(btn => {
    btn.onclick = () => {
      currentMain = btn.dataset.main;
      currentSub = "all";
      renderCats();
      renderSubs();
      if (currentMain === "all") renderHero();
      renderCards();
      updateFeedChrome();
      window.scrollTo({ top: 0, behavior: "smooth" });
    };
  });
}
function renderSubs() {
  const bar = document.getElementById("subBar");
  const tax = taxonomy[currentMain];
  if (!tax || !tax.subs || !tax.subs.length) {
    bar.classList.remove("on");
    bar.innerHTML = "";
    return;
  }
  bar.classList.add("on");
  bar.innerHTML = `<button type="button" class="sub-pill ${currentSub==="all"?"active":""}" data-sub="all">Tutte</button>` +
    tax.subs.map(s => `<button type="button" class="sub-pill ${currentSub===s.id?"active":""}" data-sub="${s.id}">${s.label}</button>`).join("");
  bar.querySelectorAll(".sub-pill").forEach(btn => {
    btn.onclick = () => { currentSub = btn.dataset.sub; renderSubs(); renderCards(); updateFeedChrome(); };
  });
}

function renderHero() {
  if (window.CM_INITIALIZING) return;
  const picked = pickFeatured();
  const feat = picked.feat, late = picked.late;
  const f = articles[feat], l = articles[late];
  const fe = document.getElementById("featured");
  if (fe && f) {
    fe.setAttribute("data-id", feat);
    fe.setAttribute("onclick", "openArticle('" + feat + "')");
    fe.style.cursor = "pointer";
    fe.innerHTML =
      '<img class="bg" alt="" aria-hidden="true" decoding="async" fetchpriority="high" loading="eager" width="960" height="720" src="' + (f.img || f.cardImg || "") + '">' +
      '<div class="shade"></div><div class="txt">' +
      '<span class="tag">Ultima ora</span>' +
      '<h1>' + (f.title || "") + '</h1>' +
      '<p>' + (f.excerpt || "") + '</p>' +
      '<span class="cta">Leggi l\'articolo →</span></div>';
  }
  const la = document.getElementById("latest");
  if (la && l) {
    la.setAttribute("data-id", late);
    la.setAttribute("onclick", "openArticle('" + late + "')");
    la.style.cursor = "pointer";
    la.innerHTML =
      '' +
      '<div><div class="lab">Ultime notizie</div><h2>' + (l.title || "") + '</h2><p>' + (l.excerpt || "") + '</p></div>';
  }
}


function renderCards() {
  if (window.CM_INITIALIZING) return;
  const title = document.getElementById("sectionTitle");
  const tax = taxonomy[currentMain];
  if (title) {
    title.textContent = tax ? tax.label : "Ultime curiosità";
    if (currentSub !== "all" && tax && tax.subs) {
      const s = tax.subs.find(x => x.id === currentSub);
      if (s) title.textContent = tax.label + " · " + s.label;
    }
  }
  const keys = Object.keys(articles).filter(id => matches(id, currentMain, currentSub));
  const grid = document.getElementById("cards");
  if (!grid) return;
  const renderSignature = currentMain + "|" + currentSub + "|" + keys.join(",");
  if (grid.dataset.cmRenderSignature === renderSignature) return;
  grid.dataset.cmRenderSignature = renderSignature;
  if (!keys.length) {
    grid.innerHTML = '<div class="empty">' + (currentMain === 'biblioteca' ? 'Biblioteca in aggiornamento.' : 'Nessun articolo in questa sezione.') + '</div>';
    return;
  }
  grid.innerHTML = keys.map(id => {
    const a = articles[id];
    const img = (a.cardImg || a.img || "").replace(/'/g, "%27");
    const t = (a.shortTitle || a.title || "").replace(/</g, "&lt;");
    const ex = (a.excerpt || "").replace(/</g, "&lt;");
    const meta = ((a.badge || a.cat || "")).replace(/</g, "&lt;");
    const href = (typeof EXTERNAL_PAGES !== "undefined" && EXTERNAL_PAGES[id]) || ("#articolo=" + encodeURIComponent(id));
    return '<a class="card" data-id="' + id + '" href="' + href.replace(/&/g, "&amp;").replace(/\"/g, "&quot;") + '">' +
      '<div class="thumb" data-cm-bg="' + img.replace(/&/g, "&amp;").replace(/\"/g, "&quot;") + '"></div>' +
      '<div class="body"><div class="meta">' + meta + '</div><h3>' + t + '</h3><p>' + ex + '</p></div></a>';
  }).join("");
  cmApplyLazyBackgrounds(grid);
}


function relatedArticles(id, n) {
  const a = articles[id];
  if (!a) return [];
  return Object.keys(articles).filter(k => k !== id && articles[k].cat === a.cat && articles[k].cat !== "info").slice(0, n);
}

function renderArticle(id) {
  const a = ensureArticleDetail(articles[id]);
  if (!a) return;
  const rel = relatedArticles(id, 3);
  const relHtml = rel.length ? `<div class="related"><h3>Potrebbe interessarti anche</h3><div class="rel-grid">` +
    rel.map(rid => {
      const r = articles[rid];
      return `<div class="rel-card" data-id="${rid}">
        <div class="ri" style="background-image:url('${r.cardImg || r.img}')"></div>
        <div class="rh">${r.shortTitle || r.title}</div>
      </div>`;
    }).join("") + `</div></div>` : "";

  let sourcesHtml = "";
  if (a.sources && a.sources.length) {
    sourcesHtml = `<div class="art-sources"><h3>Fonti e approfondimenti</h3><ul>` +
      a.sources.map(s => {
        if (typeof s === "string") return `<li>${s}</li>`;
        const name = s.name || s.title || "Fonte";
        const url = s.url || "";
        if (url) return `<li><a href="${url}" target="_blank" rel="noopener noreferrer">${name}</a>${s.note ? " — " + s.note : ""}</li>`;
        return `<li>${name}${s.note ? " — " + s.note : ""}</li>`;
      }).join("") + `</ul></div>`;
  }

  const content = document.getElementById("articleContent");
  if (!content) return;
  content.innerHTML = `
    <span class="badge">${a.badge || a.cat || ""}</span>
    <h1>${a.title}</h1>
    <div class="art-meta">${(()=>{const clean=String(a.meta||"").replace(/(?:\s*[·|—-]\s*)?\d+\s*min(?:uti)?\s+di\s+lettura/gi,"").replace(/\s*[·|—-]\s*$/g,"").trim();return (clean?clean+" · ":"")+(a.readLabel||articleReadLabel(a.body));})()}</div>
    <div class="art-actions">
      <button type="button" class="primary" id="listenBtn" aria-pressed="false">▶ Ascolta l’articolo</button>
      <button type="button" id="shareBtn">↗ Condividi</button>
      <button type="button" id="favBtn">${isFav(id) ? "★ Salvato" : "★ Salva"}</button>
    </div>
    
    <div class="art-body">${a.body || ""}</div>
    ${sourcesHtml}<p class="art-source-note">Le fonti indicate servono a verificare o approfondire il tema. Per le notizie in evoluzione, controlla sempre data e aggiornamenti della fonte originale.</p>
    ${relHtml}`;

  const listenBtn = document.getElementById("listenBtn");
  const shareBtn = document.getElementById("shareBtn");
  const favBtn = document.getElementById("favBtn");
  if (listenBtn) listenBtn.onclick = function() { toggleListen(id); };
  if (shareBtn) shareBtn.onclick = function() { shareArticle(id); };
  if (favBtn) { favBtn.classList.toggle("saved", isFav(id)); favBtn.setAttribute("aria-pressed", isFav(id)?"true":"false"); favBtn.onclick = function() { toggleFav(id); }; }
  content.querySelectorAll(".rel-card").forEach(function(el) {
    el.onclick = function() { openArticle(el.dataset.id); };
  });
  document.title = a.title + " – CurioMondo";
}


let CM_LEGACY_BODY_CACHE=null;
let CM_LEGACY_BODY_PROMISE=null;
function cmLoadLegacyBody(id){
  if(CM_LEGACY_BODY_CACHE){const hit=CM_LEGACY_BODY_CACHE[id];if(hit&&articles[id])articles[id].body=hit.body||"";return Promise.resolve(!!hit)}
  if(!CM_LEGACY_BODY_PROMISE){CM_LEGACY_BODY_PROMISE=fetch("assets/data/legacy-article-bodies-v117.json",{cache:"force-cache"}).then(r=>r.ok?r.json():{}).catch(()=>({})).then(data=>{CM_LEGACY_BODY_CACHE=data||{};return CM_LEGACY_BODY_CACHE})}
  return CM_LEGACY_BODY_PROMISE.then(data=>{const hit=data&&data[id];if(hit&&articles[id])articles[id].body=hit.body||"";return !!hit})
}

function openArticle(id, skipPush) {
  if (typeof EXTERNAL_PAGES !== "undefined" && EXTERNAL_PAGES[id]) {
    window.location.href = EXTERNAL_PAGES[id];
    return;
  }
  if(id && articles[id] && !articles[id].body){
    cmLoadLegacyBody(id).then(function(found){if(found)openArticle(id,skipPush);});
    return;
  }
  try {
    if (!id || !articles[id]) {
      console.warn("Articolo non trovato:", id);
      return;
    }
    if (!skipPush) {
      const last = navStack[navStack.length - 1];
      if (!(last && last.type === "article" && last.id === id)) {
        navStack.push({ type: "article", id: id });
      }
    }
    renderArticle(id);
    if (typeof setLastRead === "function") setLastRead(id);
    const view = document.getElementById("articleView");
    if (!view) return;
    view.classList.add("open");
    view.style.display = "block";
    view.style.visibility = "visible";
    view.style.pointerEvents = "auto";
    view.scrollTop = 0;
    const bar = document.getElementById("artProgress");
    if (bar) bar.style.width = "0%";
    document.body.style.overflow = "hidden";
    if (typeof renderContinue === "function") renderContinue();
  } catch (err) {
    console.error("openArticle error", err);
    alert("Errore apertura articolo: " + (err && err.message ? err.message : err));
  }
}


window.openArticle = openArticle;
window.showHome = showHome;
function showHome(skipPush) {
  stopListen();
  (function(){ var v=document.getElementById("articleView"); if(v){ v.classList.remove("open"); v.style.display=""; v.style.visibility=""; v.style.pointerEvents=""; } })();
  const gv = document.getElementById("gameView");
  if (gv) gv.classList.remove("open");
  const gh = document.getElementById("gamesHub");
  if (gh) gh.classList.remove("on");
  const home = document.getElementById("home");
  if (home) home.style.display = "";
  document.body.style.overflow = "";
  document.title = "CurioMondo – Curiosità e notizie dal mondo";
  if (!skipPush) {
    navStack.length = 0;
    navStack.push({ type: "home" });
  }
  // Sempre feed iniziale: evidenza + ultima ora
  currentMain = "all";
  currentSub = "all";
  if (typeof renderCats === "function") renderCats();
  if (typeof renderSubs === "function") renderSubs();
  if (typeof renderHero === "function") renderHero();
  if (typeof renderCards === "function") renderCards();
  window.scrollTo(0, 0);
  if (typeof renderContinue === "function") renderContinue();
  if (typeof updateFeedChrome === "function") updateFeedChrome();
  setTimeout(function(){ if (typeof updateCards3D === "function") updateCards3D(); }, 50);
}

function goBack() {
  stopListen();
  if (navStack.length) navStack.pop();
  const prev = navStack[navStack.length - 1];
  if (!prev || prev.type === "home") {
    showHome(true);
    if (!navStack.length) navStack.push({ type: "home" });
  } else if (prev.type === "article") {
    openArticle(prev.id, true);
  } else {
    showHome(true);
  }
}

function showFavs() {
  closeDrawer();
  showHome(true);
  currentMain = "all";
  currentSub = "all";
  renderCats();
  renderSubs();
  const ids = favs().filter(id => articles[id]);
  document.getElementById("sectionTitle").textContent = "★ Articoli preferiti";
  const grid = document.getElementById("cards");
  if (!ids.length) {
    grid.innerHTML = `<div class="empty-rich">
      <span class="ei">★</span>
      <h3>Ancora nessun preferito</h3>
      <p>Quando trovi una storia che vuoi rileggere, tocca «Salva» dentro l’articolo. Riapparirà qui.</p>
      <button type="button" onclick="openDrawer()">Apri il menu</button>
    </div>`;
    return;
  }
  grid.innerHTML = ids.map(id => {
    const a = articles[id];
    return `<article class="card" data-id="${id}">
      <div class="thumb" style="background-image:url('${a.cardImg || a.img}')"></div>
      <div class="body"><h3>${a.shortTitle || a.title}</h3><p>${a.excerpt || ""}</p></div>
    </article>`;
  }).join("");
  grid.querySelectorAll(".card").forEach(c => c.onclick = () => openArticle(c.dataset.id));
}



let utter = null;



/* ===== 3D scroll on cards ===== */
function updateCards3D() {
  if(window.matchMedia&&window.matchMedia("(max-width: 760px)").matches)return;
  var vh = window.innerHeight || 600;
  var center = vh * 0.42;
  var nodes = document.querySelectorAll(".card, .auto-card, .rel-card, .featured, .latest");
  for (var i = 0; i < nodes.length; i++) {
    var el = nodes[i];
    // non toccare elementi fuori viewport pesantemente
    var r = el.getBoundingClientRect();
    if (r.bottom < -80 || r.top > vh + 80) {
      el.classList.remove("cm3d-near", "cm3d-mid", "cm3d-far");
      el.classList.add("cm3d-far");
      continue;
    }
    var mid = r.top + r.height * 0.5;
    var dist = Math.abs(mid - center) / vh;
    el.classList.remove("cm3d-near", "cm3d-mid", "cm3d-far");
    if (dist < 0.18) el.classList.add("cm3d-near");
    else if (dist < 0.38) el.classList.add("cm3d-mid");
    else el.classList.add("cm3d-far");
  }
}

let _3dRaf = 0;
function onScroll3D() {
  if (_3dRaf) return;
  _3dRaf = requestAnimationFrame(function () {
    _3dRaf = 0;
    updateCards3D();
  });
}

/* ===== Listen play/pause state ===== */
let listenId = null;
let isPaused = false;
function stopListen() {
  if (window.speechSynthesis) speechSynthesis.cancel();
  utter = null;
  listenId = null;
  isPaused = false;
  syncListenBtn();
}
function syncListenBtn() {
  const btn = document.getElementById("listenBtn");
  if (!btn) return;
  btn.classList.remove("playing","paused");
  if (listenId && !isPaused && window.speechSynthesis && speechSynthesis.speaking) {
    btn.textContent = "⏸ In lettura — pausa";
    btn.classList.add("playing");
    btn.setAttribute("aria-pressed","true");
    btn.setAttribute("aria-label","Metti in pausa la lettura");
  } else if (listenId && isPaused) {
    btn.textContent = "▶ Lettura in pausa — riprendi";
    btn.classList.add("paused");
    btn.setAttribute("aria-pressed","true");
    btn.setAttribute("aria-label","Riprendi la lettura");
  } else {
    btn.textContent = "▶ Ascolta l’articolo";
    btn.setAttribute("aria-pressed","false");
    btn.setAttribute("aria-label","Avvia la lettura dell’articolo");
  }
}
function toggleListen(id) {
  const a = articles[id];
  if (!a || !window.speechSynthesis) {
    showToast("Ascolto non supportato su questo dispositivo");
    return;
  }
  // same article playing -> pause
  if (listenId === id && speechSynthesis.speaking && !speechSynthesis.paused) {
    speechSynthesis.pause();
    isPaused = true;
    syncListenBtn();
    showToast("In pausa");
    return;
  }
  // paused -> resume
  if (listenId === id && isPaused) {
    speechSynthesis.resume();
    isPaused = false;
    syncListenBtn();
    return;
  }
  // start new
  speechSynthesis.cancel();
  const text = (a.title || "") + ". " + stripHtml(a.body || "");
  utter = new SpeechSynthesisUtterance(text);
  utter.lang = "it-IT";
  utter.rate = 1;
  listenId = id;
  isPaused = false;
  utter.onend = function() {
    utter = null; listenId = null; isPaused = false; syncListenBtn();
  };
  utter.onerror = function() {
    utter = null; listenId = null; isPaused = false; syncListenBtn();
  };
  speechSynthesis.speak(utter);
  syncListenBtn();
  // some browsers need delayed sync
  setTimeout(syncListenBtn, 200);
}

/* ===== Share robust ===== */


function shareArticle(id) {
  const a = articles[id];
  if (!a) return;
  let path = (window.location.pathname || "/");
  if (typeof EXTERNAL_PAGES !== "undefined" && EXTERNAL_PAGES[id]) path = "/" + EXTERNAL_PAGES[id].replace(/^\//,"");
  else path = path + "#article-" + id;
  let origin = window.location.origin || "";
  if (origin.indexOf("http://")===0) origin = "https://" + window.location.host;
  const url = origin + path;
  const title = a.title || "CurioMondo";
  const text = a.excerpt || a.title || "";

  if (navigator.share) {
    navigator.share({
      title: title,
      text: text,
      url: url
    }).then(function () {
      if (typeof showToast === "function") showToast("Condiviso");
    }).catch(function (err) {
      if (err && err.name === "AbortError") return;
      if (typeof showToast === "function") showToast("Condivisione annullata");
    });
    return;
  }

  // Desktop / browser senza share nativo: fallback minimo
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(function () {
      if (typeof showToast === "function") showToast("Link copiato: incollalo dove vuoi");
    }).catch(function () {
      prompt("Copia il link e condividilo dove preferisci:", url);
    });
  } else {
    prompt("Copia il link e condividilo dove preferisci:", url);
  }
}


function copyLink(url) {
  function ok() { showToast("Link copiato negli appunti"); }
  function fallback() {
    try {
      const ta = document.createElement("textarea");
      ta.value = url;
      ta.setAttribute("readonly", "");
      ta.style.position = "fixed";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      ok();
    } catch (e) {
      prompt("Copia questo link:", url);
    }
  }
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard.writeText(url).then(ok).catch(fallback);
  } else fallback();
}

/* ===== Games & retention ===== */
const GAMES = [
  { id:"memory", icon:"🃏", title:"Memory infinito", desc:"Il classico delle coppie, con partite sempre diverse e serie da battere.", meta:"Classico · Memoria · Replay infinito" },
  { id:"sequenza", icon:"🟦", title:"Simon: sequenza", desc:"Memorizza una sequenza sempre più lunga. Semplice da capire, difficile da mollare.", meta:"Classico · Livelli progressivi" },
  { id:"focus", icon:"🎨", title:"Stroop Challenge", desc:"Il colore dice una cosa, la parola un’altra. Quanto regge davvero la tua attenzione?", meta:"Cervello · Velocità" },
  { id:"indovinelli", icon:"💡", title:"Enigmi & indovinelli", desc:"Rompicapi brevi, logica laterale e soluzioni che sembrano ovvie solo dopo.", meta:"Enigmi · Logica" },
  { id:"anagrammi", icon:"🔤", title:"Anagrammi", desc:"Ricostruisci le parole nel minor tempo possibile e prova a migliorare la tua serie.", meta:"Parole · Rapidità" },
  { id:"trova_intruso", icon:"🧩", title:"Trova l’intruso", desc:"Quattro elementi, uno non appartiene al gruppo. Individua la regola nascosta.", meta:"Logica · Pattern" },
  { id:"cronologia", icon:"⏳", title:"Timeline", desc:"Metti eventi e scoperte nell’ordine corretto. Una sfida sorprendentemente competitiva.", meta:"Storia · Ordine" },
  { id:"stima", icon:"🎯", title:"Quanto ci vai vicino?", desc:"Stima numeri, distanze e grandezze: non serve sapere, serve ragionare.", meta:"Stima · Numeri" },
  { id:"vero_falso", icon:"⚡", title:"Vero o falso?", desc:"Fatti assurdi, miti e scienza: scegli prima che il dubbio ti freghi.", meta:"Classico · Conoscenza" },
  { id:"speed_vf", icon:"⏱️", title:"Vero o falso: Blitz", desc:"La stessa idea, ma contro il tempo. Perfetto per inseguire un nuovo record.", meta:"Speed · Record" },
  { id:"geo_flash", icon:"🌍", title:"Geo Challenge", desc:"Capitali, oceani e luoghi del mondo in round rapidi sempre rigiocabili.", meta:"Geografia · Quiz" },
  { id:"quiz_curiosita", icon:"🧠", title:"The Impossible Quiz", desc:"Curiosità, trabocchetti e domande che sembrano facili finché non devi rispondere.", meta:"Quiz · Domande variabili" }
];

const QUIZ_BANK = [
  { q: "Quanti cuori ha una piovra?", a: ["Uno", "Due", "Tre", "Quattro"], c: 2 },
  { q: "Il sole è una…", a: ["Pianeta", "Stella", "Cometa", "Satellite"], c: 1 },
  { q: "Quale animale non può regredire la lingua?", a: ["Cane", "Gatto", "Coccodrillo", "Elefante"], c: 2 },
  { q: "Quanti minuti ha un giorno terrestre?", a: ["1440", "1200", "1600", "1000"], c: 0 },
  { q: "La Grande Muraglia è visibile dalla Luna a occhio nudo?", a: ["Sì", "No", "Solo con telescopio dalla Luna", "Solo di giorno"], c: 1 },
  { q: "Il miele in condizioni ideali…", a: ["Scade in 2 anni", "Non va quasi mai a male", "Fermenta in un mese", "Si solidifica e basta"], c: 1 },
  { q: "Quante ossa ha circa un adulto?", a: ["106", "206", "306", "406"], c: 1 },
  { q: "Il diamante è una forma di…", a: ["Silicio", "Carbonio", "Ferro", "Quarzo"], c: 1 }
];
const RIDDLES = [
  { q: "Più ne prendi, più ne lasci. Cosa sono?", a: ["passi", "impronte", "passi a piedi"] },
  { q: "Ha città ma non case, ha boschi ma non alberi, ha acqua ma non pesci. Cos'è?", a: ["mappa", "carta geografica", "cartina"] },
  { q: "Cosa si rompe quando la nomini?", a: ["silenzio", "il silenzio"] },
  { q: "Volo senza ali, piango senza occhi. Cosa sono?", a: ["nuvola", "nube", "la nuvola"] }
];
const VF_BANK = [
  { t: "I pipistrelli sono ciechi.", v: false, why: "Vedono, e usano anche l'ecolocalizzazione." },
  { t: "I fulmini non colpiscono due volte lo stesso posto.", v: false, why: "Possono colpire più volte lo stesso punto." },
  { t: "L'oro è commestibile in foglia (edibile).", v: true, why: "L'oro alimentare E175 è usato in pasticceria." },
  { t: "Gli squali sono mammiferi.", v: false, why: "Sono pesci cartilaginei." },
  { t: "Il caffè può aiutare a concentrarsi in dosi moderate.", v: true, why: "La caffeina è uno stimolante lieve del sistema nervoso." }
];

function getStreak() {
  try {
    const d = JSON.parse(localStorage.getItem("cm_streak") || "{}");
    return d;
  } catch(e) { return {}; }
}
function cmLocalDateKey(date) {
  const d = date || new Date();
  return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
}
function bumpStreak() {
  const today = cmLocalDateKey(new Date());
  let d = getStreak();
  if (d.last === today) {
    renderStreak();
    return d.count || 1;
  }
  const y = new Date(); y.setDate(y.getDate() - 1);
  const ys = cmLocalDateKey(y);
  if (d.last === ys) d.count = (d.count || 0) + 1;
  else d.count = 1;
  d.last = today;
  localStorage.setItem("cm_streak", JSON.stringify(d));
  renderStreak();
  return d.count;
}
function renderStreak() {
  const el = document.getElementById("streakPill");
  if (!el) return;
  const d = getStreak();
  const n = d.count || 0;
  el.textContent = n > 0 ? ("🔥 Serie: " + n + " giorno" + (n > 1 ? "i" : "")) : "🔥 Inizia una serie giocando oggi";
}

function openGamesHub() {
  closeDrawer();
  stopListen();
  (function(){ var v=document.getElementById("articleView"); if(v){ v.classList.remove("open"); v.style.display=""; v.style.visibility=""; v.style.pointerEvents=""; } })();
  const gameView=document.getElementById("gameView");
  const home=document.getElementById("home");
  const hub=document.getElementById("gamesHub");
  const grid=document.getElementById("gamesGrid");
  if(gameView) gameView.classList.remove("open");
  /* Il vecchio hub non è presente nella UI attuale: torna alla home senza generare eccezioni. */
  if(!hub || !grid){
    if(home) home.style.display="";
    document.body.style.overflow="";
    renderContinue();
    updateCards3D();
    return;
  }
  if(home) home.style.display = "none";
  const cont = document.getElementById("continueBar");
  if (cont) cont.classList.remove("on");
  hub.classList.add("on");
  document.body.style.overflow = "";
  renderStreak();
  grid.innerHTML = GAMES.map(g => `
    <article class="game-card" data-gid="${g.id}">
      <div class="gi">${g.icon}</div>
      <h3>${g.title}</h3>
      <p>${g.desc}</p>
      <div class="gmeta">${g.meta}</div>
    </article>`).join("");
  grid.querySelectorAll(".game-card").forEach(c => {
    c.onclick = () => startGame(c.dataset.gid);
  });
  window.scrollTo(0, 0);
  document.title = "Sala Giochi – CurioMondo";
}
function closeGamesHub() {
  const hub=document.getElementById("gamesHub");
  const home=document.getElementById("home");
  if(hub) hub.classList.remove("on");
  if(home) home.style.display = "";
  document.title = "CurioMondo – Curiosità e notizie dal mondo";
  renderContinue();
  updateCards3D();
}
function closeGame() {
  const gameView=document.getElementById("gameView");
  if(gameView) gameView.classList.remove("open");
  document.body.style.overflow = "";
  openGamesHub();
}
function startGame(id) {
  bumpStreak();
  const panel = document.getElementById("gamePanel");
  document.getElementById("gameView").classList.add("open");
  document.body.style.overflow = "hidden";
  if (id === "quiz_curiosita") runQuiz(panel, null, "Quiz curiosità");
  else if (id === "quiz_spazio") runQuiz(panel, QUIZ_SPAZIO, "Quiz spazio");
  else if (id === "quiz_animali") runQuiz(panel, QUIZ_ANIMALI, "Quiz animali");
  else if (id === "quiz_storia") runQuiz(panel, QUIZ_STORIA, "Quiz storia");
  else if (id === "quiz_corpo") runQuiz(panel, QUIZ_CORPO, "Quiz corpo umano");
  else if (id === "geo_flash") runQuiz(panel, QUIZ_GEO, "Geo flash");
  else if (id === "eco_quiz") runQuiz(panel, QUIZ_ECO, "Quiz pianeta");
  else if (id === "memory" || id === "memory_emoji") runMemory(panel, id === "memory_emoji");
  else if (id === "indovinelli") runRiddles(panel);
  else if (id === "vero_falso") runVF(panel, false);
  else if (id === "speed_vf") runVF(panel, true);
  else if (id === "sequenza") runSequence(panel);
  else if (id === "anagrammi") runAnagram(panel);
  else if (id === "stima") runEstimate(panel);
  else if (id === "focus") runStroop(panel);
  else if (id === "trova_intruso") runIntruder(panel);
  else if (id === "cronologia") runTimeline(panel);
  else runQuiz(panel, null, "Quiz");
}

const QUIZ_SPAZIO = [
  { q: "Quanti pianeti ha il sistema solare?", a: ["7","8","9","10"], c: 1 },
  { q: "La ISS orbita intorno a…", a: ["Luna","Terra","Marte","Sole"], c: 1 },
  { q: "Il Sole è principalmente…", a: ["Ferro","Idrogeno ed elio","Ossigeno","Carbonio"], c: 1 },
  { q: "Un anno-luce misura…", a: ["Tempo","Distanza","Velocità","Massa"], c: 1 },
  { q: "Quale pianeta è noto per gli anelli?", a: ["Marte","Venere","Saturno","Mercurio"], c: 2 }
];
const QUIZ_ANIMALI = [
  { q: "Quanti cuori ha un polpo?", a: ["1","2","3","4"], c: 2 },
  { q: "I corvidi sono…", a: ["Rettili","Uccelli","Mammiferi","Pesci"], c: 1 },
  { q: "Il sonno uniemisferico è tipico di…", a: ["Gatti","Delfini","Serpenti","Api"], c: 1 },
  { q: "Le api comunicano risorse con…", a: ["Canto","Danza","Colore solo","Ultrasuoni"], c: 1 },
  { q: "Un gruppo di leoni si chiama…", a: ["Branco","Mandria","White","Stormo"], c: 0 }
];
const QUIZ_STORIA = [
  { q: "Pompei fu sepolta nel…", a: ["79 a.C.","79 d.C.","790 d.C.","1790"], c: 1 },
  { q: "La Biblioteca di Alessandria sorgeva in…", a: ["Grecia","Egitto","Roma","Persia"], c: 1 },
  { q: "L'Anse aux Meadows è legata ai…", a: ["Romani","Maya","Norse/Vichinghi","Fenici"], c: 2 },
  { q: "Le strade consolari sono tipiche di…", a: ["Atene","Roma antica","Cartagine","Babilonia"], c: 1 },
  { q: "Il Vesuvio domina il golfo di…", a: ["Genova","Napoli","Venezia","Trieste"], c: 1 }
];
const QUIZ_CORPO = [
  { q: "Ore di sonno consigliate per molti adulti:", a: ["4–5","7–9","10–12","3–4"], c: 1 },
  { q: "La vitamina D è legata soprattutto a…", a: ["Luce solare sulla pelle","Sale","Sonno REM","Caffeina"], c: 0 },
  { q: "L'effetto placebo riguarda…", a: ["Solo frodi","Risposte reali mediate da aspettative","Solo bambini","Solo chirurgia"], c: 1 },
  { q: "Durante il sonno la memoria…", a: ["Si spegne","Può consolidarsi","Si cancella tutta","Diventa fotografica"], c: 1 },
  { q: "Camminare regolarmente è associato a…", a: ["Nessun beneficio","Benefici su cuore e umore","Solo dimagrimento estremo","Solo sportivi"], c: 1 }
];
const QUIZ_GEO = [
  { q: "Il più grande oceano:", a: ["Atlantico","Indiano","Pacifico","Artico"], c: 2 },
  { q: "Quanti continenti si contano di solito a scuola in Italia?", a: ["5","6","7","8"], c: 2 },
  { q: "Il Nilo sfocia nel…", a: ["Mar Rosso","Mediterraneo","Golfo Persico","Atlantico"], c: 1 },
  { q: "La capitale della Francia è…", a: ["Lione","Marsiglia","Parigi","Bordeaux"], c: 2 },
  { q: "L'Everest è nella catena…", a: ["Ande","Alpi","Himalaya","Montagne Rocciose"], c: 2 }
];
const QUIZ_ECO = [
  { q: "Gli oceani assorbono una grande quota di…", a: ["Azoto solo","Calore e CO₂","Elio","Oro"], c: 1 },
  { q: "Il micelio è collegato a…", a: ["Funghi e radici","Solo alghe","Nuclei atomici","Vento solare"], c: 0 },
  { q: "L'acidificazione oceanica impatta soprattutto…", a: ["Organismi calcificanti","Vulcani","Deserti","Ghiaccio secco"], c: 0 },
  { q: "La desertificazione è…", a: ["Sinonimo di deserto naturale","Degrado di terre aride","Solo un mito","Solo glaciale"], c: 1 },
  { q: "Le aurore sono legate a…", a: ["Vento solare e campo magnetico","Solo inquinamento luminoso","Terremoti","Maree"], c: 0 }
];

function runSequence(panel) {
  const syms = ["●","■","▲","◆","★","✚"];
  let level = 1, seq = [], step = 0, showing = false;
  function nextSeq() {
    seq = [];
    for (let i = 0; i < level + 2; i++) seq.push(syms[Math.floor(Math.random()*syms.length)]);
    step = 0; showing = true;
    panel.innerHTML = `<h1>Sequenza lampo</h1><p class="gdesc">Livello ${level}: guarda e ripeti</p>
      <div class="quiz-q" id="seqShow" style="text-align:center;font-size:1.6rem;letter-spacing:.3em">${seq.join(" ")}</div>`;
    setTimeout(() => {
      showing = false;
      panel.innerHTML = `<h1>Sequenza lampo</h1><p class="gdesc">Tocca i simboli nell'ordine giusto</p>
        <div style="display:flex;flex-wrap:wrap;gap:8px;justify-content:center">` +
        syms.map(s => `<button type="button" class="quiz-opt" style="width:auto;min-width:64px;text-align:center;font-size:1.3rem" data-s="${s}">${s}</button>`).join("") +
        `</div><p id="seqMsg" style="text-align:center;margin-top:12px;color:var(--muted)"></p>`;
      panel.querySelectorAll(".quiz-opt").forEach(btn => {
        btn.onclick = () => {
          if (showing) return;
          if (btn.dataset.s === seq[step]) {
            step++;
            if (step >= seq.length) {
              level++;
              showToast("Livello " + level);
              setTimeout(nextSeq, 400);
            }
          } else {
            panel.innerHTML = `<h1>Sequenza lampo</h1><div class="game-score"><div class="big">${level}</div>
              <p style="margin:12px 0">Livello raggiunto</p>
              <button type="button" class="quiz-opt" style="text-align:center" onclick="startGame('sequenza')">Rigioca</button>
              <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
          }
        };
      });
    }, 900 + level * 200);
  }
  nextSeq();
}
function runAnagram(panel) {
  const words = [
    { w: "SCIENZA", h: "Metodo e ricerca" },
    { w: "PIANETA", h: "Corpo celeste" },
    { w: "MEMORIA", h: "Ricordi" },
    { w: "OCEANO", h: "Grande massa d'acqua" },
    { w: "CERVELLO", h: "Organo del pensiero" }
  ];
  let list = shuffle(words), i = 0, ok = 0;
  function show() {
    if (i >= list.length) {
      panel.innerHTML = `<h1>Parole mescolate</h1><div class="game-score"><div class="big">${ok}/${list.length}</div>
        <button type="button" class="quiz-opt" style="text-align:center;margin-top:12px" onclick="startGame('anagrammi')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
      return;
    }
    const item = list[i];
    const mixed = shuffle(item.w.split("")).join(" ");
    panel.innerHTML = `<h1>Parole mescolate</h1><p class="gdesc">${item.h}</p>
      <div class="quiz-q" style="letter-spacing:.15em;text-align:center">${mixed}</div>
      <input class="riddle-input" id="anaIn" placeholder="Scrivi la parola" autocomplete="off" autocapitalize="characters">
      <button type="button" class="quiz-opt" id="anaGo" style="text-align:center;background:linear-gradient(135deg,var(--teal),var(--ocean));color:#fff;border:none">Verifica</button>`;
    const go = () => {
      const v = (document.getElementById("anaIn").value || "").trim().toUpperCase();
      if (v === item.w) { ok++; i++; showToast("Esatto"); setTimeout(show, 400); }
      else showToast("Riprova");
    };
    document.getElementById("anaGo").onclick = go;
  }
  show();
}
function runEstimate(panel) {
  const items = shuffle([
    { q: "Ore in una settimana?", a: 168, tol: 0 },
    { q: "Pianeti nel sistema solare?", a: 8, tol: 0 },
    { q: "Gradi di un triangolo (somma)?", a: 180, tol: 0 },
    { q: "Minuti in 3 ore?", a: 180, tol: 0 },
    { q: "Lati di un esagono?", a: 6, tol: 0 }
  ]).slice(0, 4);
  let i = 0, ok = 0;
  function show() {
    if (i >= items.length) {
      panel.innerHTML = `<h1>Stima numerica</h1><div class="game-score"><div class="big">${ok}/${items.length}</div>
        <button type="button" class="quiz-opt" style="text-align:center;margin-top:12px" onclick="startGame('stima')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
      return;
    }
    const it = items[i];
    panel.innerHTML = `<h1>Stima numerica</h1><div class="quiz-q">${it.q}</div>
      <input class="riddle-input" id="estIn" type="number" inputmode="numeric" placeholder="Numero">
      <button type="button" class="quiz-opt" id="estGo" style="text-align:center;background:linear-gradient(135deg,var(--teal),var(--ocean));color:#fff;border:none">Conferma</button>`;
    document.getElementById("estGo").onclick = () => {
      const v = Number(document.getElementById("estIn").value);
      if (v === it.a) { ok++; showToast("Corretto"); }
      else showToast("Era " + it.a);
      i++; setTimeout(show, 500);
    };
  }
  show();
}
function runStroop(panel) {
  const colors = [{n:"ROSSO",c:"#e11d48"},{n:"BLU",c:"#2563eb"},{n:"VERDE",c:"#059669"},{n:"GIALLO",c:"#ca8a04"}];
  let i = 0, ok = 0, total = 8;
  function trial() {
    if (i >= total) {
      panel.innerHTML = `<h1>Colore vs parola</h1><div class="game-score"><div class="big">${ok}/${total}</div>
        <button type="button" class="quiz-opt" style="text-align:center;margin-top:12px" onclick="startGame('focus')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
      return;
    }
    const word = colors[Math.floor(Math.random()*colors.length)];
    let ink = colors[Math.floor(Math.random()*colors.length)];
    if (Math.random() < 0.5) ink = word;
    panel.innerHTML = `<h1>Colore vs parola</h1><p class="gdesc">Tocca il colore dell'inchiostro, non la parola</p>
      <div class="quiz-q" style="text-align:center;font-size:1.8rem;color:${ink.c}">${word.n}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">` +
      colors.map(c => `<button type="button" class="quiz-opt" style="text-align:center" data-n="${c.n}">${c.n}</button>`).join("") +
      `</div>`;
    panel.querySelectorAll(".quiz-opt").forEach(btn => {
      btn.onclick = () => {
        if (btn.dataset.n === ink.n) ok++;
        i++; trial();
      };
    });
  }
  trial();
}
function runIntruder(panel) {
  const sets = shuffle([
    { items: ["Cane","Gatto","Leone","Tavolo"], x: 3 },
    { items: ["Venere","Marte","Sole","Giove"], x: 2 },
    { items: ["Roma","Parigi","Londra","Vesuvio"], x: 3 },
    { items: ["Acqua","Ghiaccio","Vapore","Ferro"], x: 3 },
    { items: ["Occhio","Orecchio","Naso","Sedia"], x: 3 }
  ]).slice(0, 4);
  let i = 0, ok = 0;
  function show() {
    if (i >= sets.length) {
      panel.innerHTML = `<h1>Trova l'intruso</h1><div class="game-score"><div class="big">${ok}/${sets.length}</div>
        <button type="button" class="quiz-opt" style="text-align:center;margin-top:12px" onclick="startGame('trova_intruso')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
      return;
    }
    const s = sets[i];
    panel.innerHTML = `<h1>Trova l'intruso</h1><p class="gdesc">Quale non c'entra?</p>` +
      s.items.map((t, idx) => `<button type="button" class="quiz-opt" data-i="${idx}" style="text-align:center">${t}</button>`).join("");
    panel.querySelectorAll(".quiz-opt").forEach(btn => {
      btn.onclick = () => {
        if (+btn.dataset.i === s.x) { ok++; showToast("Giusto"); }
        else showToast("No: era «" + s.items[s.x] + "»");
        i++; setTimeout(show, 450);
      };
    });
  }
  show();
}
function runTimeline(panel) {
  const events = shuffle([
    { t: "Primo uomo sulla Luna", y: 1969 },
    { t: "Caduta del Muro di Berlino", y: 1989 },
    { t: "Eruzione che seppellì Pompei", y: 79 },
    { t: "Inizio WWW (anni 90)", y: 1991 }
  ]);
  // simplified: ask which came first between two
  let i = 0, ok = 0, pairs = [];
  for (let a = 0; a < events.length; a++)
    for (let b = a+1; b < events.length; b++) pairs.push([events[a], events[b]]);
  pairs = shuffle(pairs).slice(0, 4);
  function show() {
    if (i >= pairs.length) {
      panel.innerHTML = `<h1>Metti in ordine</h1><div class="game-score"><div class="big">${ok}/${pairs.length}</div>
        <button type="button" class="quiz-opt" style="text-align:center;margin-top:12px" onclick="startGame('cronologia')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
      return;
    }
    const [a,b] = pairs[i];
    panel.innerHTML = `<h1>Metti in ordine</h1><p class="gdesc">Quale evento è avvenuto prima?</p>
      <button type="button" class="quiz-opt" data-p="a" style="text-align:center">${a.t}</button>
      <button type="button" class="quiz-opt" data-p="b" style="text-align:center">${b.t}</button>`;
    panel.querySelectorAll(".quiz-opt").forEach(btn => {
      btn.onclick = () => {
        const first = a.y <= b.y ? "a" : "b";
        if (btn.dataset.p === first) { ok++; showToast("Corretto"); }
        else showToast("Non proprio");
        i++; setTimeout(show, 450);
      };
    });
  }
  show();
}


function shuffle(arr) {
  const a = arr.slice();
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    const t = a[i]; a[i] = a[j]; a[j] = t;
  }
  return a;
}

function runQuiz(panel, bank, title) {
  title = title || "Quiz";
  const qs = shuffle(bank || QUIZ_BANK).slice(0, 5);
  let i = 0, score = 0;
  function render() {
    if (i >= qs.length) {
      panel.innerHTML = `<h1>${title}</h1><div class="game-score"><div class="big">${score}/${qs.length}</div>
        <p style="margin:12px 0 18px">Quiz completato. ${score >= 4 ? "Ottima curiosità!" : score >= 2 ? "Buon inizio: riprova!" : "Riprova: ogni errore insegna."}</p>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="startGame('quiz_curiosita')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
      if (score >= 4) showToast("Quiz superato ✨");
      return;
    }
    const q = qs[i];
    panel.innerHTML = `<p style="color:var(--muted);font-size:.8rem;font-weight:700;margin-bottom:8px">Domanda ${i+1} di ${qs.length}</p>
      <div class="quiz-q">${q.q}</div>
      ${q.a.map((opt, idx) => `<button type="button" class="quiz-opt" data-i="${idx}">${opt}</button>`).join("")}`;
    panel.querySelectorAll(".quiz-opt").forEach(btn => {
      btn.onclick = () => {
        const pick = +btn.dataset.i;
        panel.querySelectorAll(".quiz-opt").forEach(b => b.disabled = true);
        if (pick === q.c) { btn.classList.add("correct"); score++; }
        else {
          btn.classList.add("wrong");
          const right = panel.querySelector('.quiz-opt[data-i="'+q.c+'"]');
          if (right) right.classList.add("correct");
        }
        i++;
        setTimeout(render, 700);
      };
    });
  }
  panel.innerHTML = `<h1>Quiz curiosità</h1><p class="gdesc">5 domande. Una sola risposta corretta.</p>`;
  const hold = panel.innerHTML;
  render = (function(inner) {
    return function() {
      if (i === 0 && !panel.querySelector(".quiz-q")) {
        /* keep title once */ 
      }
      if (i >= qs.length) {
        panel.innerHTML = `<h1>${title}</h1><div class="game-score"><div class="big">${score}/${qs.length}</div>
        <p style="margin:12px 0 18px">${score >= 4 ? "Livello curiosità: alto." : "Continua ad esplorare gli articoli e riprova."}</p>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="startGame('quiz_curiosita')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
        return;
      }
      const q = qs[i];
      panel.innerHTML = `<h1>${title}</h1>
        <p style="color:var(--muted);font-size:.8rem;font-weight:700;margin-bottom:8px">Domanda ${i+1} di ${qs.length}</p>
        <div class="quiz-q">${q.q}</div>
        ${q.a.map((opt, idx) => `<button type="button" class="quiz-opt" data-i="${idx}">${opt}</button>`).join("")}`;
      panel.querySelectorAll(".quiz-opt").forEach(btn => {
        btn.onclick = () => {
          const pick = +btn.dataset.i;
          panel.querySelectorAll(".quiz-opt").forEach(b => b.disabled = true);
          if (pick === q.c) { btn.classList.add("correct"); score++; }
          else {
            btn.classList.add("wrong");
            const right = panel.querySelector('.quiz-opt[data-i="'+q.c+'"]');
            if (right) right.classList.add("correct");
          }
          i++;
          setTimeout(render, 650);
        };
      });
    };
  })();
  render();
}

function runMemory(panel, alt) {
  const symbols = alt ? ["🌟","🍀","🎵","🔥","💧","🌙","❄️","🌈"] : ["🌍","🔬","🧠","🚀","🦁","🎧","⚡","📚"];
  let deck = shuffle(symbols.concat(symbols)).map((s, i) => ({ id: i, s, flipped: false, matched: false }));
  let open = [];
  let locks = false;
  let moves = 0;
  function paint() {
    const done = deck.every(c => c.matched);
    panel.innerHTML = `<h1>Memory simboli</h1>
      <p class="gdesc">Mosse: ${moves}${done ? " — Completato!" : ""}</p>
      <div class="memory-grid">${deck.map(c =>
        `<button type="button" class="mem-card ${c.flipped||c.matched?"flipped":""} ${c.matched?"matched":""}" data-id="${c.id}">${(c.flipped||c.matched)?c.s:""}</button>`
      ).join("")}</div>
      ${done ? `<button type="button" class="quiz-opt" style="text-align:center;margin-top:16px" onclick="startGame('memory')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button>` : ""}`;
    if (done) showToast("Memory completato");
    panel.querySelectorAll(".mem-card").forEach(btn => {
      btn.onclick = () => {
        if (locks) return;
        const card = deck[+btn.dataset.id];
        if (card.flipped || card.matched) return;
        card.flipped = true;
        open.push(card);
        if (open.length === 2) {
          moves++;
          locks = true;
          if (open[0].s === open[1].s) {
            open[0].matched = open[1].matched = true;
            open = [];
            locks = false;
            paint();
          } else {
            paint();
            setTimeout(() => {
              open.forEach(c => c.flipped = false);
              open = [];
              locks = false;
              paint();
            }, 550);
            return;
          }
        } else paint();
      };
    });
  }
  paint();
}

function runRiddles(panel) {
  const list = shuffle(RIDDLES).slice(0, 3);
  let i = 0, ok = 0;
  function show() {
    if (i >= list.length) {
      panel.innerHTML = `<h1>Indovinelli</h1><div class="game-score"><div class="big">${ok}/${list.length}</div>
        <p style="margin:12px 0 18px">Enigmi risolti.</p>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="startGame('indovinelli')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
      return;
    }
    const r = list[i];
    panel.innerHTML = `<h1>Indovinelli</h1>
      <p style="color:var(--muted);font-size:.8rem;font-weight:700">Enigma ${i+1} di ${list.length}</p>
      <div class="riddle-box">${r.q}</div>
      <input class="riddle-input" id="riddleIn" placeholder="La tua risposta..." autocomplete="off">
      <button type="button" class="quiz-opt" id="riddleGo" style="text-align:center;background:linear-gradient(135deg,var(--teal),var(--ocean));color:#fff;border:none">Verifica</button>
      <p id="riddleMsg" style="margin-top:10px;font-size:.9rem;color:var(--muted)"></p>`;
    const go = () => {
      const val = (document.getElementById("riddleIn").value || "").trim().toLowerCase();
      const good = r.a.some(x => val === x || val.includes(x));
      const msg = document.getElementById("riddleMsg");
      if (good) {
        ok++;
        msg.textContent = "Esatto!";
        msg.style.color = "var(--teal-deep)";
        i++;
        setTimeout(show, 600);
      } else {
        msg.textContent = "Non proprio. Riprova o passa…";
        msg.style.color = "var(--coral)";
      }
    };
    document.getElementById("riddleGo").onclick = go;
    document.getElementById("riddleIn").onkeydown = e => { if (e.key === "Enter") go(); };
  }
  show();
}

function runVF(panel, speed) {
  const list = shuffle(VF_BANK).slice(0, speed ? 7 : 5);
  let i = 0, score = 0;
  function show() {
    if (i >= list.length) {
      panel.innerHTML = `<h1>Vero o falso</h1><div class="game-score"><div class="big">${score}/${list.length}</div>
        <button type="button" class="quiz-opt" style="text-align:center;margin-top:16px" onclick="startGame('vero_falso')">Rigioca</button>
        <button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;
      return;
    }
    const item = list[i];
    panel.innerHTML = `<h1>Vero o falso</h1>
      <p style="color:var(--muted);font-size:.8rem;font-weight:700">${i+1} / ${list.length}</p>
      <div class="quiz-q">${item.t}</div>
      <button type="button" class="quiz-opt" data-v="1" style="text-align:center">Vero</button>
      <button type="button" class="quiz-opt" data-v="0" style="text-align:center">Falso</button>
      <p id="vfWhy" style="margin-top:12px;color:var(--muted);font-size:.9rem"></p>`;
    panel.querySelectorAll(".quiz-opt").forEach(btn => {
      btn.onclick = () => {
        const pick = btn.dataset.v === "1";
        panel.querySelectorAll(".quiz-opt").forEach(b => b.disabled = true);
        if (pick === item.v) { btn.classList.add("correct"); score++; }
        else btn.classList.add("wrong");
        document.getElementById("vfWhy").textContent = item.why;
        i++;
        setTimeout(show, speed ? 500 : 900);
      };
    });
  }
  show();
}

/* patch showHome to close games */

function openDrawer() {
  const drawer=document.getElementById("drawer");
  drawer.removeAttribute("inert");drawer.setAttribute("aria-hidden","false");drawer.classList.add("open");
  document.getElementById("drawerOverlay").classList.add("open");
  document.body.style.overflow = "hidden";
  renderDrawerNav();
  const dark = document.body.classList.contains("dark");
  const lab = document.getElementById("themeLabelDrawer");
  if (lab) lab.textContent = dark ? "Modalità chiara" : "Modalità scura";
}
function closeDrawer() {
  const drawer=document.getElementById("drawer");
  drawer.classList.remove("open");drawer.setAttribute("aria-hidden","true");drawer.setAttribute("inert","");
  document.getElementById("drawerOverlay").classList.remove("open");
  if (!document.getElementById("articleView").classList.contains("open")) {
    document.body.style.overflow = "";
  }
}
function renderDrawerNav() {
  const ul = document.getElementById("drawerNav");
  if (!ul) return;
  const keys = Object.keys(taxonomy).filter(k => k !== "all");
  ul.innerHTML = keys.map(k => {
    const t = taxonomy[k];
    const hasSubs = t.subs && t.subs.length;
    const subHtml = hasSubs
      ? `<ul class="drawer-subs" id="dsub-${k}">` +
        t.subs.map(s => `<li><a href="#" data-main="${k}" data-sub="${s.id}">${s.label}</a></li>`).join("") +
        `</ul>`
      : "";
    return `<li>
      <button type="button" class="drawer-link" data-main="${k}" data-has-subs="${hasSubs?1:0}">
        <span>${t.label}</span>${hasSubs?'<span class="chev">▼</span>':''}
      </button>
      ${subHtml}
    </li>`;
  }).join("");
  ul.querySelectorAll(".drawer-link").forEach(btn => {
    btn.onclick = () => {
      const main = btn.dataset.main;
      const has = btn.dataset.hasSubs === "1";
      if (has) {
        btn.classList.toggle("open");
        const sub = document.getElementById("dsub-" + main);
        if (sub) sub.classList.toggle("open");
      } else {
        currentMain = main; currentSub = "all";
        closeDrawer(); showHome(true);
        renderCats(); renderSubs();
        if (currentMain === "all") renderHero();
        renderCards(); updateFeedChrome();
      }
    };
  });
  ul.querySelectorAll(".drawer-subs a").forEach(a => {
    a.onclick = (e) => {
      e.preventDefault();
      currentMain = a.dataset.main;
      currentSub = a.dataset.sub;
      closeDrawer(); showHome(true);
      renderCats(); renderSubs(); renderCards(); updateFeedChrome();
    };
  });
}

/* swipe back */
(function(){
  let sx=0,sy=0,cx=0,active=false,dragging=false;
  function view(){ return document.getElementById("articleView"); }
  function open(){ return view().classList.contains("open"); }
  document.addEventListener("touchstart", e => {
    const t=e.touches[0];
    if (t.clientX>48 || !open()) return;
    active=true; dragging=false; sx=t.clientX; sy=t.clientY; cx=sx;
  }, {passive:true});
  document.addEventListener("touchmove", e => {
    if (!active) return;
    const t=e.touches[0];
    const dx=t.clientX-sx, dy=Math.abs(t.clientY-sy);
    if (!dragging) {
      if (dy>50 && dy>Math.abs(dx)) { active=false; return; }
      if (dx>10) dragging=true;
    }
    if (!dragging) return;
    if (e.cancelable) e.preventDefault();
    cx=t.clientX;
    const v=view();
    const x=Math.max(0,dx);
    v.style.transform="translateX("+x+"px)";
    v.style.opacity=String(Math.max(0.4, 1-x/window.innerWidth*0.6));
  }, {passive:false});
  document.addEventListener("touchend", () => {
    if (!active && !dragging) return;
    const v=view();
    const dx=cx-sx;
    active=false;
    if (dragging && dx>window.innerWidth*0.22) {
      v.style.transition="transform .2s ease, opacity .2s ease";
      v.style.transform="translateX(100%)";
      v.style.opacity="0";
      setTimeout(() => {
        v.style.transition=""; v.style.transform=""; v.style.opacity="";
        goBack();
      }, 200);
    } else {
      v.style.transition="transform .25s ease, opacity .25s ease";
      v.style.transform="translateX(0)"; v.style.opacity="1";
      setTimeout(() => { v.style.transition=""; v.style.transform=""; v.style.opacity=""; }, 250);
    }
    dragging=false;
  }, {passive:true});
})();

function buildTicker() {
  /* I titoli sono già presenti nell’HTML: ripara solo il contenitore senza ricreare contenuti. */
  const track = document.querySelector(".ticker-track");
  const move = document.getElementById("tickerMove") || (track && track.firstElementChild);
  if (!move) return;
  move.id = "tickerMove";
  move.classList.add("ticker-move");
}

function boot() {
  try {
    const c = document.getElementById("canonicalLink");
    if (c) c.href = location.origin + "/";
  } catch(e) {}
  document.body.style.overflow = "";
  const av = document.getElementById("articleView");
  if (av) av.classList.remove("open");
  const gv = document.getElementById("gameView");
  if (gv) gv.classList.remove("open");
  const dov = document.getElementById("drawerOverlay");
  if (dov) dov.classList.remove("open");
  const dr = document.getElementById("drawer");
  if (dr) dr.classList.remove("open");
  initTheme();
  buildTicker();
  const cmTickerPrimary=document.querySelector('#tickerMove .cm-ticker-set:not([aria-hidden])');
  if(!cmTickerPrimary || cmTickerPrimary.querySelectorAll('.ticker-news').length!==10) buildTicker();
  renderCats();
  renderSubs();
  const cmHasSsrHero=!!document.querySelector('#featured[data-breaking-id]');
  const cmHasSsrRail=document.querySelectorAll('#autoRail .auto-card').length===5;
  if(!cmHasSsrHero) renderHero();
  renderCards();
  updateFeedChrome();
  renderContinue();
  if(!cmHasSsrRail && typeof buildAutoRail === "function") buildAutoRail();
  else cmApplyLazyBackgrounds(document.getElementById('autoRail'));
  if (av) av.addEventListener("scroll", updateArtProgress, {passive:true});
  window.addEventListener("scroll", onScroll3D, {passive:true});
  setTimeout(updateCards3D, 100);
  const h = location.hash || "";
  if (h.startsWith("#article-")) {
    const id = h.slice(9);
    if (articles[id]) openArticle(id);
  }
}


/* Click delegation */

document.addEventListener("click", function(ev) {
  try {
    var t = ev.target;
    if (!t || !t.closest) return;
    if (t.closest("button, a, input, .drawer, .drawer-overlay, .art-actions, .share-sheet")) return;
    var card = t.closest(".card, .auto-card, .rel-card");
    if (card && card.getAttribute("data-id")) {
      ev.preventDefault();
      ev.stopPropagation();
      openArticle(card.getAttribute("data-id"));
      return;
    }
    var feat = t.closest("#featured");
    if (feat && feat.getAttribute("data-id")) {
      openArticle(feat.getAttribute("data-id"));
      return;
    }
    var late = t.closest("#latest");
    if (late && late.getAttribute("data-id")) {
      openArticle(late.getAttribute("data-id"));
      return;
    }
  } catch (e) { console.error(e); }
}, false);


function cmFinalBoot(){window.CM_INITIALIZING=false;boot();}
if(document.readyState === "complete") cmFinalBoot(); else document.addEventListener("DOMContentLoaded", cmFinalBoot, {once:true});

/* Regola immagini: ogni articolo deve avere img coerente col titolo (no stock food/random). */
function assertArticleImages() {
  try {
    Object.keys(articles).forEach(function(id) {
      var a = articles[id];
      if (!a || !a.img) return;
      var t = ((a.title||"") + " " + (a.excerpt||"")).toLowerCase();
      var badFood = /fries|burger|pizza|coffee-cup/i.test(a.img);
      if (badFood) console.warn("CurioMondo: immagine incoerente per", id);
    });
  } catch (e) {}
}
function cmIdle(fn){if("requestIdleCallback" in window)requestIdleCallback(fn,{timeout:1800});else setTimeout(fn,700);}
if(document.readyState==="complete")cmIdle(assertArticleImages);else window.addEventListener("load",function(){cmIdle(assertArticleImages)},{once:true});

/* SEO: alt dinamico su card */
document.addEventListener("DOMContentLoaded", function() { cmIdle(function(){
  try {
    document.querySelectorAll("img[data-alt-title], article img, .card img, .story-card img").forEach(function(img) {
      if (!img.alt || img.alt === "") {
        var t = img.getAttribute("data-alt-title") || img.closest("[data-title]")?.getAttribute("data-title") || document.title;
        if (t) img.alt = t;
      }
      if (img.src && img.src.indexOf("fm=webp") === -1 && img.src.indexOf("unsplash.com") !== -1) {
        img.src = img.src + (img.src.indexOf("?") >= 0 ? "&" : "?") + "auto=format&fm=webp";
      }
    });
  } catch (e) {}
  });
});
;

/* cm-future-engine */
(function(){
 const imgOverrides={
  usa_missili_iran:'https://images.unsplash.com/photo-1569511166187-97eb6e387e19',
  israele_libano_roma:'https://images.unsplash.com/photo-1521295121783-8a321d551ad2',
  decreto_giustizia_fiducia:'https://images.unsplash.com/photo-1552832230-c0197dd311b5',
  mar_nero_2026:'https://images.unsplash.com/photo-1530053969600-caed2596d2427',
  gaza_funerale_112:'https://images.unsplash.com/photo-1548013146-72479768bada',
  afghanistan_fame:'https://images.unsplash.com/photo-1533130061792-64b345e4a833',
  onu_medio_oriente_appello:'https://images.unsplash.com/photo-1529107386315-e1a2ed48a620',
  caldo_27_citta:'https://images.unsplash.com/photo-1504370805625-d32c54b16100'
 };
 Object.keys(imgOverrides).forEach(id=>{if(window.articles&&articles[id]){articles[id].img=imgOverrides[id]+'?w=1400&h=788&fit=crop&q=82&auto=format&fm=webp';articles[id].cardImg=imgOverrides[id]+'?w=900&h=600&fit=crop&q=80&auto=format&fm=webp';}});
 // Biblioteca: include every library article and ensure cards remain clickable.
 const oldMatches=window.matches;
 window.matches=function(id,main,sub){const a=articles[id];if(main==='biblioteca'){if(!a||a.cat!=='biblioteca')return false;return !sub||sub==='all'||!a.sub||a.sub===sub;}return oldMatches(id,main,sub)};
 // Featured reader: readable preview in-place, then explicit full article.
 window.renderHero=function(){if(window.CM_INITIALIZING)return;
  const picked=pickFeatured(),feat=picked.feat,late=picked.late,f=articles[feat],l=articles[late],fe=document.getElementById('featured');
  if(fe&&f){const preview=(f.body||'').replace(/<h[2-6][^>]*>/gi,'<p><strong>').replace(/<\/h[2-6]>/gi,'</strong></p>');fe.dataset.id=feat;fe.removeAttribute('onclick');fe.innerHTML='<img class="bg" alt="" aria-hidden="true" decoding="async" fetchpriority="high" loading="eager" width="960" height="720" src="'+(f.img||f.cardImg||'')+'"><div class="shade"></div><div class="txt"><span class="tag">Ultime notizie</span><h1>'+f.title+'</h1><div class="feature-reader" tabindex="0">'+preview+'</div><div class="feature-lock">↕ Anteprima scorrevole · il resto continua nell’articolo</div><button class="cta" type="button">Apri tutto l’articolo →</button></div>';fe.querySelector('.cta').onclick=()=>openArticle(feat);}
  const la=document.getElementById('latest');if(la&&l){la.dataset.id=late;la.onclick=()=>openArticle(late);la.innerHTML='<div><div class="lab">Ultima ora</div><h2>'+l.title+'</h2><p>'+l.excerpt+'</p></div>';}
 };
 // Keep exactly ten game families, with persistent unbounded level progression.
 if(window.GAMES&&GAMES.length>10)GAMES.splice(10);
 let currentGame='';const originalStart=window.startGame;
 function levelOf(id){return +(localStorage.getItem('cm_level_'+id)||1)}
 window.startGame=function(id){currentGame=id;originalStart(id);decorateLevel();};
 function decorateLevel(){setTimeout(()=>{const panel=document.getElementById('gamePanel');if(!panel||!currentGame)return;const h=panel.querySelector('h1');if(h&&!h.querySelector('.cm-level-badge'))h.insertAdjacentHTML('beforeend','<span class="cm-level-badge">Livello '+levelOf(currentGame)+'</span>');panel.querySelectorAll('button').forEach(b=>{if(/Rigioca/i.test(b.textContent)){b.textContent='Livello successivo →';b.onclick=function(){localStorage.setItem('cm_level_'+currentGame,levelOf(currentGame)+1);window.startGame(currentGame);};}})},50)}
 new MutationObserver(()=>decorateLevel()).observe(document.getElementById('gamePanel'),{childList:true,subtree:true});
 // Futuristic fixed-space horizontal deck; vertical wheel advances articles while pointer is on deck.
 function updateDeck(){const rail=document.getElementById('cards');if(!rail)return;const c=rail.getBoundingClientRect().left+rail.clientWidth/2;rail.querySelectorAll('.card').forEach(el=>{const r=el.getBoundingClientRect(),d=(r.left+r.width/2)-c;el.classList.toggle('cm-deck-active',Math.abs(d)<r.width*.35);el.classList.toggle('cm-deck-left',d<-r.width*.35);el.classList.toggle('cm-deck-right',d>r.width*.35);});}
 function bindDeck(){const rail=document.getElementById('cards');if(!rail||rail.dataset.deckBound)return;rail.dataset.deckBound='1';rail.addEventListener('scroll',updateDeck,{passive:true});rail.addEventListener('wheel',e=>{if(Math.abs(e.deltaY)>Math.abs(e.deltaX)){e.preventDefault();rail.scrollBy({left:e.deltaY*1.25,behavior:'smooth'});}},{passive:false});updateDeck();}
 const oldRenderCards=window.renderCards;window.renderCards=function(){if(window.CM_INITIALIZING)return;oldRenderCards();requestAnimationFrame(bindDeck);requestAnimationFrame(updateDeck)};
 
})();
;

/* cm-history-router */
(function(){
  "use strict";
  var legacyOpenArticle=window.openArticle;
  var legacyShowFavs=window.showFavs;
  var baseRenderCats=window.renderCats;
  var baseRenderSubs=window.renderSubs;
  var applyingRoute=false;

  function baseUrl(){return location.pathname+location.search;}
  function stateUrl(s){
    if(s.view==="article")return baseUrl()+"#articolo="+encodeURIComponent(s.id);
    if(s.view==="category")return baseUrl()+"#category="+encodeURIComponent(s.main)+(s.sub&&s.sub!=="all"?"&sub="+encodeURIComponent(s.sub):"");
    if(s.view==="favorites")return baseUrl()+"#preferiti";
    return baseUrl();
  }
  function parseLocation(){
    var h=(location.hash||"").replace(/^#/,"");
    if(h.indexOf("article-")===0)return {cm:true,view:"article",id:decodeURIComponent(h.slice(8)),depth:0};
    if(h.indexOf("articolo=")===0)return {cm:true,view:"article",id:decodeURIComponent(h.slice(9)),depth:0};
    if(h.indexOf("category=")===0){var q=new URLSearchParams(h);return {cm:true,view:"category",main:q.get("category")||"all",sub:q.get("sub")||"all",depth:0};}
    if(h==="preferiti")return {cm:true,view:"favorites",depth:0};
    return {cm:true,view:"home",main:"all",sub:"all",depth:0,scrollY:window.scrollY||0};
  }
  function ensureState(){
    if(history.state&&history.state.cm)return history.state;
    var s=parseLocation();history.replaceState(s,"",stateUrl(s));return s;
  }
  function saveScroll(){
    var s=ensureState(),next=Object.assign({},s);
    if(s.view==="article"){
      var v=document.getElementById("articleView");next.articleScroll=v?v.scrollTop:0;
    }else next.scrollY=window.scrollY||0;
    history.replaceState(next,"",stateUrl(next));
  }
  function closeOverlays(){
    if(typeof stopListen==="function")stopListen();
    var av=document.getElementById("articleView");if(av){av.classList.remove("open");av.style.display="";av.style.visibility="";av.style.pointerEvents="";av.style.transform="";av.style.opacity="";}
    var gv=document.getElementById("gameView");if(gv)gv.classList.remove("open");
    var gh=document.getElementById("gamesHub");if(gh)gh.classList.remove("on");
    var home=document.getElementById("home");if(home)home.style.display="";
    document.body.style.overflow="";
  }
  function displayFeed(main,sub,scrollY){
    applyingRoute=true;closeOverlays();
    currentMain=main&&taxonomy[main]?main:"all";currentSub=sub||"all";
    document.title="CurioMondo – Curiosità e notizie dal mondo";
    if(typeof renderCats==="function")renderCats();if(typeof renderSubs==="function")renderSubs();
    if(typeof renderHero==="function")renderHero();if(typeof renderCards==="function")renderCards();
    if(typeof updateFeedChrome==="function")updateFeedChrome();if(typeof renderContinue==="function")renderContinue();
    setTimeout(function(){if(typeof updateCards3D==="function")updateCards3D();window.scrollTo(0,Number(scrollY)||0);applyingRoute=false;},30);
  }
  function displayArticle(id,scroll){
    if(!articles[id])return;
    applyingRoute=true;legacyOpenArticle(id,true);
    setTimeout(function(){var v=document.getElementById("articleView");if(v)v.scrollTop=Number(scroll)||0;applyingRoute=false;},20);
  }
  function displayFavorites(){
    applyingRoute=true;legacyShowFavs();setTimeout(function(){applyingRoute=false;},20);
  }
  function applyState(s){
    if(!s||!s.cm){displayFeed("all","all",0);return;}
    if(s.view==="article"&&articles[s.id])displayArticle(s.id,s.articleScroll);
    else if(s.view==="category")displayFeed(s.main,s.sub,s.scrollY);
    else if(s.view==="favorites")displayFavorites();
    else displayFeed("all","all",s.scrollY);
  }
  function push(s){
    var old=ensureState();s.cm=true;s.depth=(Number(old.depth)||0)+1;
    history.pushState(s,"",stateUrl(s));applyState(s);
  }

  window.openArticle=function(id,skipPush){
    if(!id||!articles[id]){console.warn("Articolo non trovato:",id);return;}
    if(typeof EXTERNAL_PAGES!=="undefined"&&EXTERNAL_PAGES[id]){
      saveScroll();sessionStorage.setItem("cm_last_article_id",id);location.href=EXTERNAL_PAGES[id];return;
    }
    if(skipPush){displayArticle(id,0);return;}
    var cur=ensureState();
    if(cur.view==="article"&&cur.id===id){displayArticle(id,cur.articleScroll||0);return;}
    saveScroll();push({view:"article",id:id,articleScroll:0});
  };
  window.showHome=function(skipPush){
    if(skipPush){displayFeed(currentMain||"all",currentSub||"all",0);return;}
    var cur=ensureState();
    if(cur.view==="home"&&!document.getElementById("articleView").classList.contains("open")){window.scrollTo({top:0,behavior:"smooth"});return;}
    saveScroll();push({view:"home",main:"all",sub:"all",scrollY:0});
  };
  window.goExplicitHome=window.showHome;
  window.goBack=function(){
    if(typeof stopListen==="function")stopListen();
    var s=ensureState();
    if((Number(s.depth)||0)>0){history.back();return;}
    if(document.referrer){try{var r=new URL(document.referrer);if(r.origin===location.origin){history.back();return;}}catch(e){}}
    if(typeof showToast==="function")showToast("Non c’è una pagina precedente. Tocca CurioMondo per la home.");
  };
  window.openDedicatedCategory=function(main,sub){
    if(!taxonomy[main])return;
    if(typeof closeDrawer==="function")closeDrawer();
    var cur=ensureState(),next={view:main==="all"?"home":"category",main:main,sub:sub||"all",scrollY:0};
    if(cur.view===next.view&&cur.main===next.main&&cur.sub===next.sub){displayFeed(next.main,next.sub,0);return;}
    saveScroll();push(next);
  };
  window.showFavs=function(){
    if(typeof closeDrawer==="function")closeDrawer();
    var cur=ensureState();if(cur.view==="favorites"){displayFavorites();return;}
    saveScroll();var s={view:"favorites"};s.cm=true;s.depth=(Number(cur.depth)||0)+1;history.pushState(s,"",stateUrl(s));displayFavorites();
  };

  window.renderCats=function(){
    baseRenderCats();
    document.querySelectorAll("#catBar .cat-pill").forEach(function(btn){
      var original=btn.onclick;btn.onclick=function(ev){if(original)original.call(btn,ev);if(applyingRoute)return;var m=btn.dataset.main||"all";var cur=ensureState();saveScroll();var s={cm:true,view:m==="all"?"home":"category",main:m,sub:"all",scrollY:0,depth:(Number(cur.depth)||0)+1};history.pushState(s,"",stateUrl(s));};
    });
  };
  window.renderSubs=function(){
    baseRenderSubs();
    document.querySelectorAll("#subBar .sub-pill").forEach(function(btn){
      var original=btn.onclick;btn.onclick=function(ev){if(original)original.call(btn,ev);if(applyingRoute)return;var cur=ensureState();saveScroll();var s={cm:true,view:"category",main:currentMain,sub:btn.dataset.sub||"all",scrollY:0,depth:(Number(cur.depth)||0)+1};history.pushState(s,"",stateUrl(s));};
    });
  };

  window.addEventListener("popstate",function(ev){applyState(ev.state||parseLocation());});
  document.addEventListener("keydown",function(ev){
    var el=ev.target&&ev.target.closest?ev.target.closest(".card[role=button],.auto-card,.rel-card"):null;
    if(!el||!(ev.key==="Enter"||ev.key===" "))return;ev.preventDefault();window.openArticle(el.dataset.id);
  });
  document.addEventListener("DOMContentLoaded",function(){
    var s=ensureState();
    document.querySelectorAll(".art-top .logo").forEach(function(l){l.setAttribute("aria-label","Vai alla home di CurioMondo");});
    if(s.view!=="home")setTimeout(function(){applyState(s);},60);
  });
})();
;

/* cm-three-news-update-20260805 */
(function(){
  "use strict";
  if(typeof articles==='undefined'||typeof EXTERNAL_PAGES==='undefined')return;

  var existing={};
  Object.keys(articles).forEach(function(id){
    existing[id]=articles[id];
    if(existing[id])existing[id].ultimaOra=false;
  });

  var fresh={
    hormuz_controllo_iran:{
      title:"Stretto di Hormuz, il piano discusso con l’Oman affiderebbe all’Iran il controllo del traffico in entrata",
      shortTitle:"Hormuz: il piano affiderebbe all’Iran il traffico in entrata",
      excerpt:"Teheran chiede il controllo delle rotte in ingresso e visibilità su quelle in uscita. Restano aperti ispezioni, tariffe e garanzie per gli altri Paesi del Golfo.",
      cat:"politica",sub:"geopolitica",badge:"Medio Oriente · Geopolitica",badgeClass:"",
      meta:"5 agosto 2026 · Aggiornato alle 20:45",featured:true,ultimaOra:true,
      img:"",
      cardImg:"",
      body:"",
      sources:[]
    },
    kyiv_attacco_17_morti:{
      title:"Kyiv sotto un nuovo attacco russo: almeno 17 morti e decine di feriti",
      shortTitle:"Kyiv colpita: almeno 17 morti e 44 feriti",
      excerpt:"Missili e droni hanno colpito la capitale e la regione circostante. Zelensky denuncia la carenza di intercettori e la crescente pressione sulle difese aeree.",
      cat:"politica",sub:"geopolitica",badge:"Ucraina · Guerra",badgeClass:"",
      meta:"5 agosto 2026 · Aggiornato alle 20:45",featured:true,ultimaOra:false,
      img:"",
      cardImg:"",
      body:"",
      sources:[]
    },
    sole_immagini_inouye:{
      title:"La superficie del Sole fotografata con un dettaglio senza precedenti",
      shortTitle:"Il Sole fotografato con un dettaglio mai raggiunto",
      excerpt:"Il telescopio solare Daniel K. Inouye mostra strutture sottili e movimenti del plasma mai osservati a questa risoluzione.",
      cat:"spazio",sub:"astronomia",badge:"Spazio · Astronomia",badgeClass:"",
      meta:"5 agosto 2026 · Aggiornato alle 20:45",featured:true,ultimaOra:false,
      img:"",
      cardImg:"",
      body:"",
      sources:[]
    }
  };

  Object.keys(articles).forEach(function(id){delete articles[id]});
  Object.assign(articles,fresh,existing);
  Object.assign(EXTERNAL_PAGES,{
    hormuz_controllo_iran:"notizie/stretto-hormuz-iran-controllo-traffico-entrata.html",
    kyiv_attacco_17_morti:"notizie/kyiv-attacco-russo-17-morti-difese-aeree.html",
    sole_immagini_inouye:"notizie/sole-immagini-dettaglio-inouye-telescope.html"
  });
})();
;

/* cm-fresh-questions-v2 */
(function(){
 const EXTRA={
  "Quiz curiosità":[
   ["Quale metallo è liquido a temperatura ambiente?",["Mercurio","Alluminio","Rame","Argento"],0],
   ["Qual è l'oceano più grande?",["Atlantico","Indiano","Pacifico","Artico"],2],
   ["Che cosa misura la scala Richter?",["Vento","Terremoti","Pioggia","Pressione"],1],
   ["Quale gas assorbono soprattutto le piante?",["Ossigeno","Azoto","Anidride carbonica","Elio"],2],
   ["Quanti lati ha un dodecagono?",["10","11","12","14"],2],
   ["Quale organo filtra principalmente il sangue?",["Polmoni","Reni","Stomaco","Pelle"],1],
   ["La luce viaggia più velocemente nel…",["Vuoto","Vetro","Acqua","Legno"],0],
   ["Quale continente attraversa l'Equatore e i due tropici?",["Europa","Africa","Asia","Antartide"],1]
  ],
  "Quiz spazio":[
   ["Qual è il pianeta più caldo?",["Mercurio","Venere","Marte","Giove"],1],
   ["Come si chiama la nostra galassia?",["Andromeda","Via Lattea","Sombrero","Triangolo"],1],
   ["Quale pianeta ruota quasi sdraiato?",["Urano","Terra","Marte","Saturno"],0],
   ["Una supernova è…",["Una luna","L'esplosione di una stella","Un asteroide","Una galassia"],1],
   ["Il primo essere umano nello spazio fu…",["Armstrong","Gagarin","Aldrin","Glenn"],1]
  ],
  "Quiz animali":[
   ["Quale mammifero depone uova?",["Delfino","Ornitorinco","Koala","Lontra"],1],
   ["Qual è l'animale terrestre più veloce?",["Leone","Ghepardo","Antilope","Struzzo"],1],
   ["I polpi hanno sangue di colore…",["Rosso","Blu","Verde","Trasparente"],1],
   ["Quale animale usa l'ecolocalizzazione?",["Pipistrello","Pavone","Tartaruga","Giraffa"],0]
  ],
  "Quiz storia":[
   ["In quale secolo iniziò la Rivoluzione francese?",["XVII","XVIII","XIX","XX"],1],
   ["Chi inventò la stampa a caratteri mobili in Europa?",["Galileo","Gutenberg","Newton","Volta"],1],
   ["Costantinopoli oggi si chiama…",["Atene","Istanbul","Ankara","Smirne"],1],
   ["Il Rinascimento italiano iniziò soprattutto in…",["Toscana","Sicilia","Sardegna","Piemonte"],0]
  ],
  "Quiz corpo umano":[
   ["Qual è l'organo più esteso del corpo?",["Fegato","Pelle","Polmoni","Intestino"],1],
   ["Quante camere ha il cuore umano?",["2","3","4","5"],2],
   ["Dove si trova il femore?",["Braccio","Coscia","Cranio","Torace"],1],
   ["Quale vitamina favorisce l'assorbimento del calcio?",["A","C","D","K soltanto"],2]
  ],
  "Geo flash":[
   ["Qual è la capitale del Canada?",["Toronto","Ottawa","Vancouver","Montreal"],1],
   ["Il Danubio sfocia nel…",["Mar Nero","Baltico","Atlantico","Caspio"],0],
   ["Quale Paese ha la forma di uno stivale?",["Grecia","Italia","Croazia","Portogallo"],1],
   ["Il Kilimangiaro si trova in…",["Kenya","Tanzania","Etiopia","Marocco"],1]
  ],
  "Quiz pianeta":[
   ["Quale ecosistema immagazzina molto carbonio nel suolo?",["Torbiere","Deserti","Spiagge","Ghiacciai"],0],
   ["La barriera corallina è formata soprattutto da…",["Piante","Animali coloniali","Roccia vulcanica","Alghe soltanto"],1],
   ["Che cosa indica la biodiversità?",["Solo il numero di alberi","Varietà di vita","Temperatura media","Quantità di pioggia"],1],
   ["Quale gas è il principale responsabile antropico del riscaldamento globale?",["Elio","CO₂","Neon","Idrogeno"],1]
  ]
 };
 function qobj(x){return Array.isArray(x)?{q:x[0],a:x[1],c:x[2]}:x}
 function procedural(title){
  const out=[];
  for(let k=0;k<18;k++){
   if(title.includes('spazio')){
    let a=2+Math.floor(Math.random()*8),b=2+Math.floor(Math.random()*8),ans=a*b;
    out.push({q:`Se un segnale impiega ${a} minuti per tratta, quanti minuti servono per andata e ritorno ripetuti ${b} volte?`,a:[ans,ans+a,ans*2,Math.max(1,ans-a)].map(String),c:0});
   }else if(title.includes('corpo')){
    let bpm=55+Math.floor(Math.random()*36),min=2+Math.floor(Math.random()*5),ans=bpm*min;
    out.push({q:`A ${bpm} battiti al minuto, quanti battiti avvengono in ${min} minuti?`,a:[ans,ans+bpm,ans-min,ans*2].map(String),c:0});
   }else{
    let a=3+Math.floor(Math.random()*18),b=2+Math.floor(Math.random()*9),ans=a*b;
    out.push({q:`Quanto fa ${a} × ${b}?`,a:[ans,ans+b,ans-a,ans+1].map(String),c:0});
   }
  }
  return out;
 }
 function fresh(bank,title,count){
  let all=(bank||window.QUIZ_BANK||[]).map(qobj).concat((EXTRA[title]||[]).map(qobj),procedural(title));
  const key='cm_seen_'+title,seen=JSON.parse(localStorage.getItem(key)||'[]');
  let pool=all.filter(x=>!seen.includes(x.q));
  if(pool.length<count){localStorage.removeItem(key);pool=all.slice();}
  pool=window.shuffle?shuffle(pool):pool.sort(()=>Math.random()-.5);
  const pick=pool.slice(0,count);
  localStorage.setItem(key,JSON.stringify(seen.concat(pick.map(x=>x.q)).slice(-40)));
  return pick.map(q=>{let pairs=q.a.map((v,i)=>({v,ok:i===q.c}));pairs.sort(()=>Math.random()-.5);return {q:q.q,a:pairs.map(p=>p.v),c:pairs.findIndex(p=>p.ok)}});
 }
 window.runQuiz=function(panel,bank,title){
  title=title||'Quiz';const qs=fresh(bank,title,5);let i=0,score=0;
  function render(){
   if(i>=qs.length){panel.innerHTML=`<h1>${title}</h1><div class="game-score"><div class="big">${score}/${qs.length}</div><p style="margin:12px 0 18px">Nuovo giro disponibile: le domande cambiano a ogni partita.</p><button type="button" class="quiz-opt" style="text-align:center" id="cmReplay">Nuove domande</button><button type="button" class="quiz-opt" style="text-align:center" onclick="closeGame()">Altri giochi</button></div>`;document.getElementById('cmReplay').onclick=()=>runQuiz(panel,bank,title);return}
   const q=qs[i];panel.innerHTML=`<h1>${title}</h1><p style="color:var(--muted);font-size:.8rem;font-weight:700;margin-bottom:8px">Domanda ${i+1} di ${qs.length} · set sempre rinnovato</p><div class="quiz-q">${q.q}</div>${q.a.map((o,n)=>`<button type="button" class="quiz-opt" data-i="${n}">${o}</button>`).join('')}`;
   panel.querySelectorAll('.quiz-opt').forEach(btn=>btn.onclick=()=>{const p=+btn.dataset.i;panel.querySelectorAll('.quiz-opt').forEach(b=>b.disabled=true);if(p===q.c){btn.classList.add('correct');score++}else{btn.classList.add('wrong');const r=panel.querySelector(`.quiz-opt[data-i="${q.c}"]`);if(r)r.classList.add('correct')}i++;setTimeout(render,650)});
  }render();
 };
})();
;

/* cm-add-3-news-20260806 */
(function(){
"use strict";if(typeof articles==='undefined'||typeof EXTERNAL_PAGES==='undefined')return;
Object.keys(articles).forEach(function(id){if(articles[id])articles[id].ultimaOra=false;});
var fresh={sinopec_petrolio_russo:{title:"Sinopec accelera sul petrolio russo per compensare il calo delle forniture dal Medio Oriente",shortTitle:"Sinopec aumenta gli acquisti di petrolio russo",excerpt:"Il colosso cinese avrebbe acquistato tra 30 e 40 carichi di greggio ESPO per le consegne tra luglio e settembre, ridisegnando in poche settimane una parte dei flussi energetici asiatici.",cat:"economia",sub:"energia",badge:"Energia · Cina e Russia",badgeClass:"",meta:"6 agosto 2026 · Aggiornato alle 06:10",featured:true,ultimaOra:true,img:"",cardImg:"",body:"",sources:[]},papa_leone_sudamerica:{title:"Papa Leone XIV visiterà Uruguay, Argentina e Perù nel suo viaggio sudamericano di novembre",shortTitle:"Papa Leone XIV in Sudamerica a novembre",excerpt:"Il Pontefice sarà in Uruguay, Argentina e Perù dal 6 al 17 novembre. Il viaggio avrà un forte valore pastorale e diplomatico, con un ritorno nei luoghi della sua lunga esperienza missionaria.",cat:"politica",sub:"mondo",badge:"Vaticano · America Latina",badgeClass:"",meta:"6 agosto 2026 · Aggiornato alle 06:10",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},wall_street_iran_record:{title:"Wall Street resta vicino ai record mentre i mercati scommettono su un’intesa con l’Iran",shortTitle:"Wall Street vicino ai record sulle speranze di accordo con l’Iran",excerpt:"Il Dow Jones ha aggiornato il proprio massimo, mentre S&P 500 e Nasdaq hanno risentito della debolezza dei grandi titoli tecnologici. Energia e diplomazia restano al centro delle decisioni degli investitori.",cat:"economia",sub:"mercati",badge:"Mercati · Stati Uniti",badgeClass:"",meta:"6 agosto 2026 · Aggiornato alle 06:10",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]}};
var old={};Object.keys(articles).forEach(function(id){old[id]=articles[id];});
Object.keys(articles).forEach(function(id){delete articles[id];});Object.assign(articles,fresh,old);
Object.assign(EXTERNAL_PAGES,{sinopec_petrolio_russo:"notizie/sinopec-petrolio-russo-forniture-medio-oriente.html",papa_leone_sudamerica:"notizie/papa-leone-xiv-viaggio-uruguay-argentina-peru-novembre.html",wall_street_iran_record:"notizie/wall-street-record-speranze-accordo-iran.html"});
})();
;

/* cm-book-emotions-20260806 */
(function(){
"use strict";
if(typeof articles==="undefined")return;
var book={"title":"La bussola interiore: capire, proteggere e guidare le emozioni","shortTitle":"La bussola interiore","excerpt":"Un libro completo per comprendere che cosa sono le emozioni, riconoscere la manipolazione emotiva e imparare a rispondere con lucidità, dignità e libertà.","cat":"biblioteca","sub":"mente_emozioni","badge":"Biblioteca · Emozioni","badgeClass":"curiosita","meta":"Biblioteca · 10.015 parole · lettura lunga","img":"","cardImg":"","featured":false,"ultimaOra":false,"body":"","sources":[]};
var old={};Object.keys(articles).forEach(function(id){old[id]=articles[id];});
Object.keys(articles).forEach(function(id){delete articles[id];});
})();
;

/* cm-add-5-news-20260806-night */
(function(){
"use strict";if(typeof articles==='undefined'||typeof EXTERNAL_PAGES==='undefined')return;
Object.keys(articles).forEach(function(id){if(articles[id])articles[id].ultimaOra=false;});
var fresh={germania_drone_esplosivo_leipzig:{title:"Germania, drone con esplosivo trovato all’aeroporto cargo di Lipsia-Halle",shortTitle:"Drone con esplosivo all’aeroporto di Lipsia-Halle",excerpt:"La procura federale tedesca ha assunto l’indagine dopo il ritrovamento di un drone con un ordigno nei pressi della pista sud. L’episodio riapre il tema della protezione delle infrastrutture critiche europee.",cat:"politica",sub:"europa",badge:"Germania · Sicurezza europea",badgeClass:"",meta:"6 agosto 2026 · Aggiornato alle 22:25",featured:true,ultimaOra:true,img:"",cardImg:"",body:"",sources:[]},vaccino_mrna_influenza_mflusiva:{title:"Influenza, la FDA approva mFlusiva: il primo vaccino a mRNA contro l’influenza",shortTitle:"FDA approva il primo vaccino antinfluenzale a mRNA",excerpt:"Il vaccino di Moderna è autorizzato negli Stati Uniti per gli adulti dai 50 anni. La tecnologia a mRNA potrebbe rendere più rapida la produzione di dosi aggiornate contro i ceppi stagionali.",cat:"salute",sub:"medicina",badge:"Salute · Vaccini",badgeClass:"",meta:"6 agosto 2026 · Aggiornato alle 22:25",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},uganda_truppe_gaza:{title:"Uganda, il Parlamento approva l’invio di truppe nella forza internazionale per Gaza",shortTitle:"Uganda approva l’invio di truppe nella forza per Gaza",excerpt:"Kampala ha dato il primo assenso pubblico a una partecipazione militare alla futura forza di stabilizzazione. Restano aperte domande sul mandato, sui rischi e sull’effettiva attuazione del piano.",cat:"politica",sub:"geopolitica",badge:"Gaza · Missione internazionale",badgeClass:"",meta:"6 agosto 2026 · Aggiornato alle 22:25",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},italia_produzione_industriale_giugno:{title:"Italia, la produzione industriale scende dell’1% a giugno e delude le attese",shortTitle:"Produzione industriale italiana in calo dell’1% a giugno",excerpt:"Il dato ISTAT interrompe il recupero mensile atteso dagli analisti. I beni strumentali registrano la flessione più marcata, mentre l’energia è l’unico raggruppamento in crescita.",cat:"economia",sub:"italia",badge:"Italia · Industria",badgeClass:"",meta:"6 agosto 2026 · Aggiornato alle 22:25",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]},ponte_stretto_progettazione_esecutiva:{title:"Ponte sullo Stretto, via libera unanime alla fase di progettazione esecutiva",shortTitle:"Ponte sullo Stretto, via libera alla progettazione esecutiva",excerpt:"Il Consiglio Superiore dei Lavori Pubblici ha concluso l’esame del collegamento tra Sicilia e Calabria e autorizzato il passaggio alla fase successiva. Restano ulteriori passaggi tecnici e amministrativi.",cat:"politica",sub:"italia",badge:"Italia · Infrastrutture",badgeClass:"",meta:"6 agosto 2026 · Aggiornato alle 22:25",featured:true,ultimaOra:false,img:"",cardImg:"",body:"",sources:[]}};
var old={};Object.keys(articles).forEach(function(id){old[id]=articles[id];});
Object.keys(articles).forEach(function(id){delete articles[id];});Object.assign(articles,fresh,old);
var shown=0;Object.keys(articles).forEach(function(id){var a=articles[id];if(!a||a.cat==='biblioteca')return;a.featured=shown<10;shown++;});
Object.assign(EXTERNAL_PAGES,{germania_drone_esplosivo_leipzig:"notizie/germania-drone-esplosivo-aeroporto-lipsia-halle.html",vaccino_mrna_influenza_mflusiva:"notizie/vaccino-mrna-influenza-mflusiva-fda-adulti-50-anni.html",uganda_truppe_gaza:"notizie/uganda-approva-truppe-forza-internazionale-gaza.html",italia_produzione_industriale_giugno:"notizie/italia-produzione-industriale-giugno-2026-calo-istat.html",ponte_stretto_progettazione_esecutiva:"notizie/ponte-stretto-via-libera-progettazione-esecutiva.html"});
})();
;

/* cm-add-7-news-20260807 */
(function(){
"use strict";
if(typeof articles==='undefined'||typeof EXTERNAL_PAGES==='undefined')return;
Object.keys(articles).forEach(function(id){if(articles[id]){articles[id].ultimaOra=false;articles[id].featured=false;}});
var newest={"thailandia_sparatoria_scuola":{"title":"Thailandia, sparatoria in una scuola: uccisi un insegnante e l’aggressore, quattro feriti","shortTitle":"Thailandia, sparatoria in una scuola: due morti e quattro feriti","excerpt":"Un insegnante è morto e quattro persone sono rimaste ferite in una sparatoria in una scuola alla periferia di Bangkok. Secondo la polizia, l’aggressore era uno studente e si è tolto la vita.","cat":"politica","sub":"asia","badge":"Ultima ora · Thailandia","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 02:00","featured":true,"ultimaOra":true,"img":"","cardImg":"","body":"","sources":[]},"taiwan_ponte_strategico_esercitazioni":{"title":"Taiwan simula la chiusura di un ponte strategico per difendere l’accesso a Taipei","shortTitle":"Taiwan, esercitazioni su un ponte strategico verso Taipei","excerpt":"Le forze di Taiwan hanno provato a bloccare e difendere un ponte considerato un possibile passaggio rapido verso la capitale durante le esercitazioni militari annuali.","cat":"politica","sub":"asia","badge":"Taiwan · Difesa","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 02:00","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"usa_ordini_cittadinanza_nascita":{"title":"Stati Uniti, Trump firma nuovi ordini per limitare la cittadinanza alla nascita","shortTitle":"USA, nuovi ordini di Trump sulla cittadinanza alla nascita","excerpt":"Donald Trump ha firmato nuovi ordini esecutivi che restringono alcune categorie della cittadinanza alla nascita e mirano a vietare il cosiddetto turismo delle nascite.","cat":"politica","sub":"americhe","badge":"Stati Uniti · Immigrazione","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 02:00","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"iran_minaccia_stati_golfo":{"title":"Iran avverte gli Stati del Golfo: possibili ritorsioni se gli Stati Uniti lanceranno nuovi attacchi","shortTitle":"Iran minaccia ritorsioni nel Golfo in caso di nuovi attacchi USA","excerpt":"Teheran ha avvertito diversi Paesi del Golfo che potrebbe colpire infrastrutture energetiche e strategiche se Washington attaccasse nuovamente il territorio iraniano.","cat":"politica","sub":"geopolitica","badge":"Medio Oriente · Tensione","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 02:00","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"israele_libano_scontri_roma":{"title":"Israele e Libano, nuovi scontri mentre proseguono i negoziati a Roma","shortTitle":"Israele-Libano, violenze al confine durante i colloqui di Roma","excerpt":"Due soldati israeliani sono morti in un’esplosione nel sud del Libano. Gli attacchi di risposta israeliani hanno causato vittime e feriti, mentre a Roma continuano i colloqui mediati dagli Stati Uniti.","cat":"politica","sub":"geopolitica","badge":"Libano · Diplomazia e conflitto","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 02:00","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"italia_caldo_altri_dieci_giorni":{"title":"Italia, caldo estremo per altri dieci giorni: temporali al Nord ma tregua breve","shortTitle":"Italia, caldo intenso per altri dieci giorni e temporali al Nord","excerpt":"L’ondata di caldo dovrebbe continuare per altri dieci giorni. Al Nord sono previsti temporali localmente intensi, ma il sollievo sarà limitato e temporaneo.","cat":"salute","sub":"movimento","badge":"Italia · Meteo e salute","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 02:00","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"francesco_guccini_morto":{"title":"È morto Francesco Guccini, il “Maestrone” della canzone italiana aveva 86 anni","shortTitle":"È morto Francesco Guccini, aveva 86 anni","excerpt":"Francesco Guccini è morto a 86 anni a Pavana, circondato dai familiari. I funerali si svolgeranno in forma privata e una commemorazione è prevista a settembre.","cat":"storia","sub":"sapere","badge":"Italia · Cultura","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 02:00","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]}};
var previous={};Object.keys(articles).forEach(function(id){previous[id]=articles[id];});
Object.keys(articles).forEach(function(id){delete articles[id];});
Object.assign(articles,newest,previous);
var shown=0;Object.keys(articles).forEach(function(id){var a=articles[id];if(!a||a.cat==='info'||a.cat==='biblioteca')return;a.featured=shown<10;shown++;});
articles.thailandia_sparatoria_scuola.ultimaOra=true;
Object.assign(EXTERNAL_PAGES,{"thailandia_sparatoria_scuola":"notizie/thailandia-sparatoria-scuola-insegnante-ucciso-7-agosto-2026.html","taiwan_ponte_strategico_esercitazioni":"notizie/taiwan-esercitazioni-ponte-strategico-difesa-taipei.html","usa_ordini_cittadinanza_nascita":"notizie/usa-trump-ordini-cittadinanza-nascita.html","iran_minaccia_stati_golfo":"notizie/iran-minaccia-stati-golfo-nuovi-attacchi-usa.html","israele_libano_scontri_roma":"notizie/israele-libano-scontri-negoziati-roma.html","italia_caldo_altri_dieci_giorni":"notizie/italia-caldo-estremo-altri-dieci-giorni.html","francesco_guccini_morto":"notizie/morto-francesco-guccini-86-anni.html"});
})();
;

/* cm-2-news-crypto-calciomercato-20260807 */
(function(){
"use strict";
if(typeof articles==="undefined"||typeof EXTERNAL_PAGES==="undefined")return;
var additions={"crypto_bitcoin_ether_altcoin":{"title":"Crypto, Bitcoin ed Ether tengono meglio mentre le altcoin perdono slancio","shortTitle":"Crypto: Bitcoin ed Ether tengono, altcoin più deboli","excerpt":"Bitcoin ed Ether sovraperformano il mercato crypto più ampio mentre i trader riducono l’esposizione alle altcoin e si concentrano sugli asset principali.","cat":"crypto","sub":"mercati","badge":"Crypto · Mercati","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 02:15","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"real_madrid_diomande_2033":{"title":"Calciomercato, il Real Madrid ingaggia Yan Diomande dal Lipsia fino al 2033","shortTitle":"Calciomercato: Diomande al Real Madrid fino al 2033","excerpt":"Il Real Madrid ha ufficializzato l’arrivo dell’ala ivoriana Yan Diomande dal RB Lipsia con un contratto di sette stagioni, fino al 30 giugno 2033.","cat":"sport","sub":"calcio","badge":"Calciomercato · Real Madrid","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 02:12","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]}};
var existing={};Object.keys(articles).forEach(function(id){existing[id]=articles[id];});
Object.keys(articles).forEach(function(id){delete articles[id];});
Object.assign(articles,additions,existing);
var shown=0;Object.keys(articles).forEach(function(id){var a=articles[id];if(!a||a.cat==='info'||a.cat==='biblioteca')return;a.featured=shown<10;shown++;});
Object.assign(EXTERNAL_PAGES,{"crypto_bitcoin_ether_altcoin":"notizie/bitcoin-ether-rifugio-mercato-crypto-altcoin-deboli.html","real_madrid_diomande_2033":"notizie/real-madrid-yan-diomande-rb-lipsia-contratto-2033.html"});
})();
;

/* cm-update-7-news-20260807-evening */
(function(){
"use strict";
if(typeof articles==="undefined"||typeof EXTERNAL_PAGES==="undefined")return;
var latest={"italia_spagna_controlli_ceuta":{"title":"Italia e Spagna, scontro sui controlli alle frontiere dopo la crisi di Ceuta","shortTitle":"Italia-Spagna, scontro sui controlli dopo la crisi di Ceuta","excerpt":"Roma respinge la richiesta di Madrid di eliminare i controlli selettivi sui viaggiatori provenienti dalla Spagna. La crisi migratoria di Ceuta apre un nuovo confronto dentro l’Unione europea.","cat":"politica","sub":"europa","badge":"Italia · Europa","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 20:50","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"patto_difesa_saudi_turchia_pakistan":{"title":"Arabia Saudita, Turchia e Pakistan firmano un patto di difesa reciproca","shortTitle":"Patto di difesa tra Arabia Saudita, Turchia e Pakistan","excerpt":"L’accordo firmato alla Mecca stabilisce che un attacco contro uno dei tre Paesi sarà considerato un attacco contro tutti. Cambiano gli equilibri della sicurezza regionale.","cat":"politica","sub":"geopolitica","badge":"Ultima ora · Geopolitica","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 20:48","featured":true,"ultimaOra":true,"img":"","cardImg":"","body":"","sources":[]},"trump_ballroom_casa_bianca_stop":{"title":"Un tribunale blocca il salone da 400 milioni di dollari voluto da Trump alla Casa Bianca","shortTitle":"Stop al salone da 400 milioni voluto da Trump","excerpt":"La corte d’appello stabilisce che il progetto non può proseguire senza l’approvazione del Congresso. Trump prepara il ricorso alla Corte Suprema.","cat":"politica","sub":"americhe","badge":"Stati Uniti · Giustizia","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 20:45","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"israele_libano_forza_verifica_hezbollah":{"title":"Israele e Libano concordano una lista di Paesi per verificare il disarmo di Hezbollah","shortTitle":"Israele-Libano, lista di Paesi per verificare il disarmo di Hezbollah","excerpt":"La lista è stata discussa nei colloqui di Roma. Gli Stati Uniti dovranno scegliere i Paesi che potrebbero contribuire alla missione di verifica.","cat":"politica","sub":"geopolitica","badge":"Medio Oriente · Diplomazia","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 20:42","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"ucraina_droni_urali_wildberries":{"title":"Droni ucraini colpiscono un magazzino negli Urali, oltre 2.000 chilometri dal confine","shortTitle":"Droni ucraini raggiungono gli Urali, oltre 2.000 km dal confine","excerpt":"L’attacco ha raggiunto un centro Wildberries a Ekaterinburg. Ottocento lavoratori sono stati evacuati senza feriti.","cat":"politica","sub":"europa","badge":"Ucraina · Guerra dei droni","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 20:38","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"europa_caldo_incendi_serbia_allerta_italia":{"title":"Caldo estremo in Europa: incendi in Serbia e allerta rossa in tutte le città italiane monitorate","shortTitle":"Caldo estremo: incendi in Serbia e 27 città italiane in allerta","excerpt":"Temperature vicine ai 40 gradi alimentano gli incendi nei Balcani. In Italia tutte le 27 città monitorate sono state poste in allerta rossa.","cat":"ambiente","sub":"clima","badge":"Ambiente · Europa","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 20:34","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]},"usa_lavoro_luglio_mercati_fed":{"title":"Gli Stati Uniti perdono 23.000 posti di lavoro: i mercati riducono le attese di un rialzo dei tassi","shortTitle":"USA, persi 23.000 posti: cambiano le attese sui tassi Fed","excerpt":"Il dato di luglio è molto più debole delle previsioni. Borse e obbligazioni salgono mentre diminuisce la probabilità di un aumento dei tassi a settembre.","cat":"economia","sub":"mercati","badge":"Economia · Stati Uniti","badgeClass":"","meta":"7 agosto 2026 · Aggiornato alle 20:30","featured":true,"ultimaOra":false,"img":"","cardImg":"","body":"","sources":[]}};
var previous={};
Object.keys(articles).forEach(function(id){previous[id]=articles[id];});
Object.keys(articles).forEach(function(id){delete articles[id];});
Object.assign(articles,latest,previous);
var shown=0;
Object.keys(articles).forEach(function(id){
  var a=articles[id];
  if(!a||a.cat==="info"||a.cat==="biblioteca")return;
  a.featured=shown<10;
  shown++;
});
Object.assign(EXTERNAL_PAGES,{"italia_spagna_controlli_ceuta":"notizie/italia-spagna-scontro-controlli-frontiere-crisi-ceuta.html","patto_difesa_saudi_turchia_pakistan":"notizie/arabia-saudita-turchia-pakistan-patto-difesa-reciproca.html","trump_ballroom_casa_bianca_stop":"notizie/tribunale-blocca-salone-casa-bianca-trump-approvazione-congresso.html","israele_libano_forza_verifica_hezbollah":"notizie/israele-libano-lista-paesi-forza-verifica-disarmo-hezbollah.html","ucraina_droni_urali_wildberries":"notizie/droni-ucraini-urali-magazzino-wildberries-oltre-2000-km.html","europa_caldo_incendi_serbia_allerta_italia":"notizie/europa-caldo-incendi-serbia-italia-27-citta-allerta-rossa.html","usa_lavoro_luglio_mercati_fed":"notizie/usa-lavoro-luglio-posti-persi-mercati-fed-tassi.html"});
})();
;

/* blocco-12 */
(function(){var KEY='cm_consent_v2',VERSION='2026-08-06';function read(){try{return JSON.parse(localStorage.getItem(KEY)||'null')}catch(e){return null}}function write(v){v.version=VERSION;v.updatedAt=new Date().toISOString();localStorage.setItem(KEY,JSON.stringify(v));apply(v);close()}function apply(v){document.documentElement.dataset.consentAnalytics=v.analytics?'granted':'denied';document.documentElement.dataset.consentMarketing=v.marketing?'granted':'denied';document.documentElement.dataset.consentExternal=v.external?'granted':'denied';document.querySelectorAll('script[type="text/plain"][data-cookiecategory]').forEach(function(s){var c=s.dataset.cookiecategory;if(v[c]&&!s.dataset.loaded){var n=document.createElement('script');for(var i=0;i<s.attributes.length;i++){var a=s.attributes[i];if(a.name!=='type'&&a.name!=='data-cookiecategory')n.setAttribute(a.name,a.value)}n.text=s.text;s.parentNode.insertBefore(n,s.nextSibling);s.dataset.loaded='1'}})}function open(custom){var m=document.getElementById('cm-consent');if(!m)return;m.classList.add('open');var d=m.querySelector('.cmc-details'),x=m.querySelector('.cmc-close');if(custom){d.classList.add('open');x.style.display='block'}var v=read()||{};['preferences','analytics','marketing','external'].forEach(function(k){var e=document.getElementById('cmc-'+k);if(e)e.checked=!!v[k]})}function close(){var m=document.getElementById('cm-consent');if(m)m.classList.remove('open');}function init(){var m=document.getElementById('cm-consent');if(!m)return;var v=read();if(v)apply(v);else open(false);m.querySelector('[data-cm-accept]').onclick=function(){write({necessary:true,preferences:true,analytics:true,marketing:true,external:true})};m.querySelector('[data-cm-reject]').onclick=function(){write({necessary:true,preferences:false,analytics:false,marketing:false,external:false})};m.querySelector('[data-cm-custom]').onclick=function(){m.querySelector('.cmc-details').classList.add('open');m.querySelector('.cmc-close').style.display='block'};m.querySelector('[data-cm-save]').onclick=function(){write({necessary:true,preferences:document.getElementById('cmc-preferences').checked,analytics:document.getElementById('cmc-analytics').checked,marketing:document.getElementById('cmc-marketing').checked,external:document.getElementById('cmc-external').checked})};m.querySelector('.cmc-close').onclick=function(){if(read())close()};document.querySelectorAll('.cm-cookie-manage,[data-cookie-settings]').forEach(function(b){b.addEventListener('click',function(e){e.preventDefault();open(true)})})}window.CurioConsent={open:function(){open(true)},get:read};if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init);else init()})();
;

/* cm-theme-sync-final */
(function(){
 function apply(){var d=false;try{d=localStorage.getItem('cm_theme')==='dark'}catch(e){}document.body.classList.toggle('dark',d);document.documentElement.classList.toggle('cm-dark',d)}
 apply();window.addEventListener('pageshow',apply);document.addEventListener('visibilitychange',function(){if(!document.hidden)apply()});window.addEventListener('storage',function(e){if(e.key==='cm_theme')apply()});
 var old=window.toggleTheme;window.toggleTheme=function(){if(old)old();setTimeout(apply,0)};
})();
;

/* cm-global-search-script */
var CM_SEARCH_INDEX=[];
var CM_SEARCH_PROMISE=null;
var CM_SEARCH_LOADED=false;
function cmLoadSearchIndex(){
  if(CM_SEARCH_LOADED)return Promise.resolve(CM_SEARCH_INDEX);
  if(!CM_SEARCH_PROMISE)CM_SEARCH_PROMISE=fetch('assets/data/search-index-v101.json',{credentials:'same-origin'})
    .then(function(r){if(!r.ok)throw new Error('Indice non disponibile');return r.json()})
    .then(function(items){
      var recent=CM_SEARCH_INDEX.slice(),seen=Object.create(null),merged=[];
      recent.concat(items).forEach(function(item){if(item&&item.url&&!seen[item.url]){seen[item.url]=true;merged.push(item)}});
      CM_SEARCH_INDEX=merged;CM_SEARCH_LOADED=true;return merged;
    });
  return CM_SEARCH_PROMISE;
}
function cmNorm(v){return(v||'').toLocaleLowerCase('it').normalize('NFD').replace(/[\u0300-\u036f]/g,'')}
function openSiteSearch(){let m=document.getElementById('siteSearchModal');if(!m)return;m.removeAttribute('inert');m.setAttribute('aria-hidden','false');m.classList.add('open');document.body.style.overflow='hidden';cmLoadSearchIndex();setTimeout(()=>document.getElementById('siteSearchInput')?.focus(),60)}
function closeSiteSearch(){let m=document.getElementById('siteSearchModal');if(!m)return;m.classList.remove('open');m.setAttribute('aria-hidden','true');m.setAttribute('inert','');document.body.style.overflow=''}
function openSearchResult(u){closeSiteSearch();location.href=u}
async function runSiteSearch(q){let box=document.getElementById('siteSearchResults'),st=document.getElementById('siteSearchStatus');q=cmNorm(q.trim());if(q.length<2){box.innerHTML='';st.textContent='Scrivi almeno due lettere.';return}st.textContent='Ricerca in corso…';try{let index=await cmLoadSearchIndex(),ws=q.split(/\s+/).filter(Boolean),r=index.map(x=>{let t=cmNorm(x.title),d=cmNorm(x.desc),a=cmNorm(x.text),score=0;ws.forEach(w=>{if(t.includes(w))score+=8;if(d.includes(w))score+=4;if(a.includes(w))score++});return{...x,score}}).filter(x=>x.score).sort((a,b)=>b.score-a.score).slice(0,30);st.textContent=r.length?r.length+' risultati trovati':'Nessun risultato.';box.innerHTML=r.map(x=>`<button type="button" onclick='openSearchResult(${JSON.stringify(x.url)})'><small>NOTIZIA</small><strong>${x.title}</strong><span>${x.desc||'Apri il contenuto completo'}</span><b>→</b></button>`).join('')}catch(e){st.textContent='La ricerca non è disponibile in questo momento.'}}
document.addEventListener('input',e=>{if(e.target?.id==='siteSearchInput')runSiteSearch(e.target.value)});
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeSiteSearch()});
function openLibraryFromTool(){location.href='biblioteca/'}
function openRandomArticle(){let ids=Object.keys(articles).filter(id=>articles[id]?.cat!=='biblioteca');if(ids.length)openArticle(ids[Math.floor(Math.random()*ids.length)])}
;

/* cm-menu-aria-fix */
document.addEventListener("DOMContentLoaded",function(){var b=document.getElementById("menuBtn"),d=document.getElementById("drawer");if(!b||!d)return;var sync=function(){b.setAttribute("aria-expanded",d.classList.contains("open")?"true":"false")};new MutationObserver(sync).observe(d,{attributes:true,attributeFilter:["class"]});sync();});
;

/* cm-v24-stable-controller */
(function(){
'use strict';
const current={
  etna_catania_chiuso_13_agosto_2026:{title:'Etna, aeroporto di Catania chiuso fino alle 16 del 13 agosto: circa 700 voli saltati',shortTitle:'Etna: Catania chiuso fino alle 16 del 13 agosto',excerpt:'La cenere vulcanica mantiene chiuso Fontanarossa fino alle 16 di giovedì 13 agosto. Tra l’8 e l’11 agosto sono saltati circa 700 voli e oltre 250 collegamenti sono stati riprogrammati.',cat:'italia',sub:'ambiente',badge:'Italia · Sicilia · Ultima ora',meta:'12 agosto 2026 · Nuovo sviluppo',featured:true,ultimaOra:true,img:'assets/images/optimized/etna-cenere-catania-voli-10-agosto-2026-960.webp',cardImg:'assets/images/optimized/etna-cenere-catania-voli-10-agosto-2026-960.webp'},
  ucraina_novorossiysk_stop_petroliere_usa_2026:{title:'Ucraina, stop mirato agli attacchi alle petroliere a Novorossiysk dopo la richiesta degli USA',shortTitle:'Ucraina, stop mirato alle petroliere a Novorossiysk',excerpt:'Secondo il Financial Times, citato da Reuters, Kyiv avrebbe sospeso alcuni attacchi contro petroliere e infrastrutture collegate a Novorossiysk dopo una richiesta statunitense.',cat:'mondo',sub:'geopolitica',badge:'Ucraina · USA · Mar Nero',meta:'12 agosto 2026 · Nuovo sviluppo',featured:true,ultimaOra:true,img:'assets/images/optimized/novorossiysk-petroliere-ucraina-droni-12-agosto-2026-960.webp',cardImg:'assets/images/optimized/novorossiysk-petroliere-ucraina-droni-12-agosto-2026-960.webp'},
  ronaldo_georgina_matrimonio_2026:{title:'Cristiano Ronaldo e Georgina Rodríguez si sono sposati: nozze private a Cascais',shortTitle:'Cristiano Ronaldo e Georgina: nozze private a Cascais',excerpt:'Cristiano Ronaldo e Georgina Rodríguez hanno celebrato un matrimonio civile privato a Cascais, in Portogallo, dopo circa dieci anni di relazione.',cat:'sport',sub:'calcio',badge:'Sport · Personaggi · Portogallo',meta:'12 agosto 2026 · Nuovo sviluppo',featured:true,ultimaOra:true,img:'assets/images/optimized/cristiano-ronaldo-georgina-matrimonio-cascais-11-agosto-2026-960.webp',cardImg:'assets/images/optimized/cristiano-ronaldo-georgina-matrimonio-cascais-11-agosto-2026-960.webp'},
  ucraina_zaporizhzhia_missili_11agosto_2026:{title:'Nuova ondata di missili russi sull’Ucraina: 6 morti a Zaporizhzhia, attaccata anche Kyiv',shortTitle:'Missili russi sull’Ucraina: 6 morti a Zaporizhzhia',excerpt:'Nuova offensiva notturna su più città ucraine. L’ultimo bilancio disponibile indica sei morti e 19 feriti a Zaporizhzhia; incendi segnalati anche a Kyiv.',cat:'mondo',sub:'geopolitica',badge:'Ucraina · Guerra · Attacco notturno',meta:'11 agosto 2026 · Nuovo sviluppo',featured:true,ultimaOra:true,img:'assets/images/optimized/ucraina-zaporizhzhia-attacco-russo-11-agosto-2026-960.webp',cardImg:'assets/images/optimized/ucraina-zaporizhzhia-attacco-russo-11-agosto-2026-960.webp'},
  eclissi_totale_sole_europa_2026:{title:'Eclissi totale di Sole il 12 agosto: la Spagna tra i luoghi migliori d’Europa',shortTitle:'Eclissi totale di Sole: domani il grande spettacolo',excerpt:'La fascia di totalità attraverserà Groenlandia, Islanda, Portogallo e Spagna. In Italia l’eclissi sarà parziale: filtri solari certificati indispensabili.',cat:'scienza',sub:'astronomia',badge:'Spazio · Astronomia · Europa',meta:'11 agosto 2026 · Domani',featured:true,ultimaOra:true,img:'assets/images/optimized/eclissi-totale-sole-europa-spagna-12-agosto-2026-960.webp',cardImg:'assets/images/optimized/eclissi-totale-sole-europa-spagna-12-agosto-2026-960.webp'},
  etna_sicilia_cenere_catania_2026:{title:'Etna, nuova fase esplosiva e nube di cenere: sospesi i voli in arrivo a Catania',shortTitle:'Etna, nube di cenere: sospesi i voli in arrivo a Catania',excerpt:'L’attività esplosiva dal cratere Voragine si intensifica. La nube di cenere ha imposto la sospensione temporanea dei voli in arrivo all’aeroporto di Catania.',cat:'italia',sub:'ambiente',badge:'Italia · Sicilia · Etna',meta:'10 agosto 2026 · Nuovo sviluppo',featured:true,ultimaOra:true,img:'assets/images/optimized/etna-cenere-catania-voli-10-agosto-2026-960.webp',cardImg:'assets/images/optimized/etna-cenere-catania-voli-10-agosto-2026-960.webp'},
  infantino_confederazioni_fifa_2026:{title:'UEFA, CONCACAF e AFC contro Infantino: «fiducia tradita» sul progetto Mondiali',shortTitle:'UEFA, CONCACAF e AFC contro Infantino: scontro ai vertici FIFA',excerpt:'Tre confederazioni continentali accusano il presidente FIFA di inganno e di una fondamentale violazione della fiducia sul progetto, poi abbandonato, di aprire a investitori privati i diritti commerciali dei Mondiali.',cat:'sport',sub:'calcio',badge:'Calcio mondiale · FIFA',meta:'10 agosto 2026 · Nuovo sviluppo',featured:true,ultimaOra:true,img:'assets/images/optimized/uefa-concacaf-afc-infantino-10-agosto-2026-960.webp',cardImg:'assets/images/optimized/uefa-concacaf-afc-infantino-10-agosto-2026-960.webp'},
  colombia_terremoto_7_4_2026:{title:'Terremoto in Colombia, oltre 250 morti e migliaia di dispersi: continua la corsa contro il tempo',shortTitle:'Colombia, oltre 250 morti e migliaia di dispersi',excerpt:'Reuters riporta almeno 254 morti dopo il sisma di magnitudo 7,4. Associated Press riferisce fino a 4.000 dispersi nei conteggi civili mentre proseguono i soccorsi.',cat:'mondo',sub:'americhe',badge:'Colombia · Terremoto · America Latina',meta:'12 agosto 2026 · Aggiornamento importante',featured:true,ultimaOra:true,img:'assets/images/optimized/colombia-terremoto-132-morti-11-agosto-2026-960.webp',cardImg:'assets/images/optimized/colombia-terremoto-132-morti-11-agosto-2026-960.webp'},
  meloni_frederiksen_migrazione_2026:{title:'Meloni e Frederiksen: no all’immigrazione incontrollata verso l’Europa',shortTitle:'Meloni e Frederiksen: no all’immigrazione incontrollata',excerpt:'Le premier di Italia e Danimarca chiedono centri di rimpatrio in Paesi terzi e nuove soluzioni esterne all’UE per frenare i flussi irregolari.',cat:'italia',sub:'politica',badge:'Italia · Europa · Migrazione',meta:'10 agosto 2026 · Nuovo sviluppo',featured:true,ultimaOra:false,img:'assets/images/optimized/meloni-frederiksen-immigrazione-10-agosto-2026-ai-960.webp',cardImg:'assets/images/optimized/meloni-frederiksen-immigrazione-10-agosto-2026-ai-960.webp'},
  netanyahu_piano_usa_gaza_2026:{title:'Netanyahu boccia il piano USA per Gaza: nessun ritiro finché Hamas non sarà disarmato',shortTitle:'Netanyahu boccia il piano USA per Gaza',excerpt:'Il premier israeliano lega qualsiasi ritiro da Gaza a un disarmo reale e completo di Hamas. Resta aperto il disaccordo sulla sequenza del piano.',cat:'politica',sub:'geopolitica',badge:'Medio Oriente · Geopolitica',meta:'10 agosto 2026 · Nuovo sviluppo',featured:true,ultimaOra:false,img:'assets/images/optimized/netanyahu-piano-usa-gaza-10-agosto-2026-ai-960.webp',cardImg:'assets/images/optimized/netanyahu-piano-usa-gaza-10-agosto-2026-ai-960.webp'},
  joe_biden_salute_2026:{title:'Joe Biden, il tumore si è diffuso oltre le ossa: peggiorano le condizioni dell’ex presidente USA',shortTitle:'Joe Biden, il tumore si è diffuso oltre le ossa',excerpt:'Hunter Biden ha riferito che il tumore alla prostata dell’ex presidente si è diffuso oltre le ossa ed è diventato molto doloroso.',cat:'mondo',sub:'americhe',badge:'Stati Uniti · Salute',meta:'8 agosto 2026 · Nuovo sviluppo',featured:true,ultimaOra:false,img:'assets/images/optimized/joe-biden-tumore-progressione-8-agosto-2026-ai-960.webp',cardImg:'assets/images/optimized/joe-biden-tumore-progressione-8-agosto-2026-ai-960.webp'},
  codice_strada_17_anni_2026:{title:'Codice della Strada, patente a 17 anni e superamento a destra: le proposte del MIT',shortTitle:'Patente a 17 anni e superamento a destra: le ipotesi del MIT',excerpt:'Il MIT ha avviato il confronto su una nuova revisione del Codice della Strada. Le misure sono proposte allo studio, non norme già in vigore.',cat:'italia',sub:'politica',badge:'Italia · Politica e normative',meta:'9 agosto 2026 · Proposte allo studio',featured:true,ultimaOra:false,img:'assets/images/optimized/codice-strada-patente-17-anni-sorpasso-destra-ai-960.webp',cardImg:'assets/images/optimized/codice-strada-patente-17-anni-sorpasso-destra-ai-960.webp'},
  tetris_ricordi_intrusivi_trauma:{title:'Tetris dopo un trauma può ridurre i ricordi intrusivi? Cosa mostrano gli studi',shortTitle:'Tetris e trauma: cosa mostrano gli studi',excerpt:'Una procedura strutturata che include un compito visuo-spaziale con Tetris ha ridotto i ricordi intrusivi in alcuni piccoli studi. Non equivale a una cura fai-da-te del PTSD.',cat:'psicologia',sub:'cervello',badge:'Mente & Corpo · Psicologia',meta:'9 agosto 2026 · Ricerca',featured:true,ultimaOra:false,img:'assets/images/optimized/tetris-trauma-ricordi-intrusivi-ai-960.webp',cardImg:'assets/images/optimized/tetris-trauma-ricordi-intrusivi-ai-960.webp'},
  thailand_scuola_stretta_armi:{title:'Strage nella scuola in Thailandia, il governo prepara una nuova stretta sulle armi',shortTitle:'Thailandia, nuova stretta sulle armi dopo la strage',excerpt:'Dopo la strage alla Debsirin Nonthaburi School, il governo ha annunciato l’intenzione di intervenire sulla regolamentazione delle armi.',cat:'mondo',sub:'asia',badge:'Asia · Società',meta:'8 agosto 2026 · Sviluppo importante',featured:true,ultimaOra:false,img:'assets/images/optimized/thailandia-debsirin-nonthaburi-school-armi-8-agosto-2026-960.webp',cardImg:'assets/images/optimized/thailandia-debsirin-nonthaburi-school-armi-8-agosto-2026-960.webp'}
};
const pages={
 etna_catania_chiuso_13_agosto_2026:'notizie/etna-catania-chiuso-13-agosto-700-voli-12-agosto-2026.html',
 ucraina_novorossiysk_stop_petroliere_usa_2026:'notizie/ucraina-stop-attacchi-petroliere-novorossiysk-richiesta-usa-12-agosto-2026.html',
 ronaldo_georgina_matrimonio_2026:'notizie/cristiano-ronaldo-georgina-matrimonio-cascais-11-agosto-2026.html',
 ucraina_zaporizhzhia_missili_11agosto_2026:'notizie/ucraina-zaporizhzhia-nuova-ondata-missili-russi-11-agosto-2026.html',
 eclissi_totale_sole_europa_2026:'notizie/eclissi-totale-sole-europa-spagna-12-agosto-2026.html',
 etna_sicilia_cenere_catania_2026:'notizie/etna-nuova-fase-esplosiva-cenere-voli-catania-10-agosto-2026.html',
 infantino_confederazioni_fifa_2026:'notizie/uefa-concacaf-afc-infantino-scontro-fifa-10-agosto-2026.html',
 colombia_terremoto_7_4_2026:'notizie/colombia-terremoto-7-4-decine-morti-edifici-crollati-10-agosto-2026.html',
 meloni_frederiksen_migrazione_2026:'notizie/meloni-frederiksen-immigrazione-incontrollata-centri-rimpatrio-10-agosto-2026.html',
 netanyahu_piano_usa_gaza_2026:'notizie/netanyahu-boccia-piano-usa-gaza-disarmo-hamas-10-agosto-2026.html',
 joe_biden_salute_2026:'notizie/joe-biden-tumore-progressione-oltre-ossa-8-agosto-2026.html',
 codice_strada_17_anni_2026:'notizie/codice-strada-patente-17-anni-superamento-destra-proposte-mit-2026.html',
 tetris_ricordi_intrusivi_trauma:'notizie/tetris-trauma-ricordi-intrusivi-flashback-studi.html',
 thailand_scuola_stretta_armi:'notizie/thailandia-strage-scuola-governo-stretta-armi-8-agosto-2026.html'
};
const priority=['etna_catania_chiuso_13_agosto_2026','colombia_terremoto_7_4_2026','ucraina_novorossiysk_stop_petroliere_usa_2026','ronaldo_georgina_matrimonio_2026','ucraina_zaporizhzhia_missili_11agosto_2026','eclissi_totale_sole_europa_2026','etna_sicilia_cenere_catania_2026','infantino_confederazioni_fifa_2026','meloni_frederiksen_migrazione_2026','netanyahu_piano_usa_gaza_2026','joe_biden_salute_2026','codice_strada_17_anni_2026','tetris_ricordi_intrusivi_trauma','thailand_scuola_stretta_armi','zelensky_washington_difese','canada_bald_range_20000','kyiv_attacco_8ago','tifone_dolphin_2026'];
const editorialFeatured=[
 'trump_riduce_esercitazioni_usa_corea_sud_apertura_pyongyang_17agosto_2026',
 'furto_antonello_da_messina_museo_messina_16agosto_2026',
 'incendio_belgio_3000_ettari_germania_16agosto_2026',
 'uragano_lala_hawaii_big_island_16agosto_2026',
 'simona_quadarella_oro_400_stile_libero_tripletta_parigi_16agosto_2026'
];
const editorialScores={
 trump_riduce_esercitazioni_usa_corea_sud_apertura_pyongyang_17agosto_2026:9.4,
 furto_antonello_da_messina_museo_messina_16agosto_2026:9.5,
 incendio_belgio_3000_ettari_germania_16agosto_2026:9.2,
 uragano_lala_hawaii_big_island_16agosto_2026:9.1,
 simona_quadarella_oro_400_stile_libero_tripletta_parigi_16agosto_2026:9.0
};
/* v195: registro cronologico unico per le notizie della homepage. */
const CM_MONTH_INDEX={gennaio:0,febbraio:1,marzo:2,aprile:3,maggio:4,giugno:5,luglio:6,agosto:7,settembre:8,ottobre:9,novembre:10,dicembre:11};
function cmStoryTimestamp(id){
 const a=(typeof articles!=='undefined'&&articles[id])?articles[id]:{},meta=String(a.meta||'').toLocaleLowerCase('it');
 const m=meta.match(/\b(\d{1,2})\s+(gennaio|febbraio|marzo|aprile|maggio|giugno|luglio|agosto|settembre|ottobre|novembre|dicembre)\s+(20\d{2})(?:\D{0,8}(\d{1,2}):(\d{2}))?/i);
 if(!m)return 0;
 return new Date(Number(m[3]),CM_MONTH_INDEX[m[2]],Number(m[1]),Number(m[4]||0),Number(m[5]||0),0,0).getTime();
}
function cmNormalizeLatestNews(){
 const source=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS:[];
 const unique=[];
 const seenUrls=Object.create(null);
 source.forEach(function(id){
  if(!id||unique.indexOf(id)!==-1)return;
  const url=(typeof EXTERNAL_PAGES!=='undefined'&&EXTERNAL_PAGES[id])||'';
  if(url&&seenUrls[url])return;
  if(url)seenUrls[url]=1;
  unique.push(id);
 });
 const originalOrder=new Map(unique.map(function(id,i){return [id,i];}));
 unique.sort(function(a,b){
  const ta=cmStoryTimestamp(a),tb=cmStoryTimestamp(b);
  if(ta&&tb&&ta!==tb)return tb-ta;
  if(ta&&!tb)return -1;
  if(!ta&&tb)return 1;
  return originalOrder.get(a)-originalOrder.get(b);
 });
 window.CM_LATEST_NEWS=unique.slice(0,10);
 return window.CM_LATEST_NEWS;
}
function cmRegisterLatestNews(id){
 const latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
 window.CM_LATEST_NEWS=[id].concat(latest.filter(function(key){return key!==id;}));
 return cmNormalizeLatestNews();
}
/* v195: registra le notizie esterne prima del primo rendering della homepage. */
(function cmHydratePendingNewsBeforeRender(){
 const queue=Array.isArray(window.CM_PENDING_DISCOVERY)?window.CM_PENDING_DISCOVERY:[];
 if(!queue.length||typeof articles==='undefined'||typeof EXTERNAL_PAGES==='undefined'||typeof CM_SEARCH_INDEX==='undefined')return;
 queue.forEach(function(entry){
  if(!entry||!entry.id||!entry.url||!entry.item)return;
  const id=entry.id,url=entry.url;
  articles[id]=entry.item;
  EXTERNAL_PAGES[id]=url;
  if(!entry.evergreen){
   const latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
   cmRegisterLatestNews(id);
  }
  if(entry.searchItem){
   for(let i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url)CM_SEARCH_INDEX.splice(i,1);}
   CM_SEARCH_INDEX.unshift(entry.searchItem);
  }
 });
 window.CM_PENDING_DISCOVERY=[];
})();
function currentPriority(){
 const newest=cmNormalizeLatestNews();
 return Array.from(new Set(newest.concat(priority)));
}
function isEditorialStory(id){
 return !!(articles[id]&&articles[id].cat!=='info'&&articles[id].cat!=='biblioteca');
}
function storyDateKey(id){
 const a=articles[id]||{},meta=String(a.meta||'');
 const m=meta.match(/\b(\d{1,2}\s+[a-zàèéìòù]+\s+20\d{2})\b/i);
 return m?m[1].toLocaleLowerCase('it'):'';
}
function newestEditorialBatch(){
 const newest=(Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS:[]).filter(isEditorialStory);
 if(!newest.length)return [];
 const firstDate=storyDateKey(newest[0]);
 if(!firstDate)return newest.slice(0,2);
 const sameDay=[];
 for(const id of newest){
  if(storyDateKey(id)!==firstDate)break;
  sameDay.push(id);
 }
 return sameDay.length?sameDay:newest.slice(0,2);
}
function latestStoryId(){
 const batch=newestEditorialBatch();
 if(batch.length){
  return batch.map((id,index)=>({id,score:editorialScore(id,index)}))
   .sort((a,b)=>b.score-a.score||batch.indexOf(a.id)-batch.indexOf(b.id))[0].id;
 }
 return currentPriority().find(isEditorialStory)||Object.keys(articles).find(isEditorialStory);
}
function editorialScore(id,recencyIndex){
 const a=articles[id]||{},text=[a.title,a.badge,a.meta].join(' ').toLocaleLowerCase('it');
 let score=Math.max(Number(a.editorialPriority)||0,editorialScores[id]||0);
 if(/forte rilievo|record|storica|emergenza|vittim|guerra|terremoto|uragano|incendio/.test(text))score+=.35;
 if(/guida|come funziona|spiegat/.test(text))score-=1.5;
 score+=Math.max(0,10-recencyIndex)*.025;
 return score;
}
function evidenzaIds(){
 const newest=(Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS:[]).filter(isEditorialStory);
 if(newest.length>=5)return newest.slice(0,5);
 const main=latestStoryId(),latest=currentPriority(),batch=newestEditorialBatch();
 const pinned=batch.filter(id=>id!==main&&isEditorialStory(id)).slice(0,5);
 const pool=Array.from(new Set(editorialFeatured.concat(latest,Object.keys(articles))));
 const ranked=pool.filter(id=>id!==main&&!pinned.includes(id)&&isEditorialStory(id))
  .map(id=>({id,score:editorialScore(id,latest.indexOf(id)<0?99:latest.indexOf(id))}))
  .sort((a,b)=>b.score-a.score||pool.indexOf(a.id)-pool.indexOf(b.id)).map(item=>item.id);
 return pinned.concat(ranked).slice(0,5);
}
function esc(v){return String(v||'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
let installSignature='';
function install(){
 if(typeof articles==='undefined')return false;
 const nextInstallSignature=currentPriority().join('|');
 if(installSignature===nextInstallSignature)return true;
 Object.entries(current).forEach(([id,data])=>{articles[id]=Object.assign({},articles[id]||{},data)});
 if(typeof EXTERNAL_PAGES!=='undefined')Object.assign(EXTERNAL_PAGES,pages);
 // Correct known recent image metadata.
 if(articles.zelensky_washington_difese){articles.zelensky_washington_difese.img='assets/images/optimized/zelensky-washington-trump-difese-aeree-8-agosto-2026-960.webp';articles.zelensky_washington_difese.cardImg=articles.zelensky_washington_difese.img;}
 if(articles.canada_bald_range_20000){articles.canada_bald_range_20000.img='assets/images/optimized/incendio-bald-range-summerland-columbia-britannica-8-agosto-2026-960.webp';articles.canada_bald_range_20000.cardImg=articles.canada_bald_range_20000.img;}
 const activePriority=currentPriority(),main=latestStoryId(),featured=evidenzaIds();
 Object.keys(articles).forEach(id=>{const a=articles[id];if(a&&a.cat!=='info'&&a.cat!=='biblioteca'){a.ultimaOra=(id===main);a.featured=featured.includes(id);}});
 const ordered={};activePriority.forEach(id=>{if(articles[id])ordered[id]=articles[id]});Object.keys(articles).forEach(id=>{if(!ordered[id])ordered[id]=articles[id]});Object.keys(articles).forEach(id=>delete articles[id]);Object.assign(articles,ordered);
 installSignature=nextInstallSignature;
 return true;
}
function openId(id){if(typeof openArticle==='function')openArticle(id);else if(window.EXTERNAL_PAGES&&EXTERNAL_PAGES[id])location.href=EXTERNAL_PAGES[id];}
function cmLoadRailImages(rail){
 const nodes=Array.from(rail.querySelectorAll('[data-cm-bg]'));
 const load=el=>{if(!el||!el.dataset.cmBg)return;el.style.backgroundImage='url("'+el.dataset.cmBg.replace(/"/g,'%22')+'")';delete el.dataset.cmBg};
 const start=()=>{if(!('IntersectionObserver'in window)){nodes.forEach(load);return}const observer=new IntersectionObserver(entries=>{entries.forEach(entry=>{if(!entry.isIntersecting)return;load(entry.target);observer.unobserve(entry.target)})},{root:rail,rootMargin:'0px 24px',threshold:.01});nodes.forEach(node=>observer.observe(node))};
 const hero=document.querySelector('#featured img.bg');
 if(hero&&!hero.complete){hero.addEventListener('load',()=>{if('requestIdleCallback'in window)requestIdleCallback(start,{timeout:900});else setTimeout(start,100)},{once:true})}
 else if('requestIdleCallback'in window)requestIdleCallback(start,{timeout:900});else setTimeout(start,100);
}
function renderBreaking(){
 if(!install())return;
 const id=latestStoryId(),a=articles[id],fe=document.getElementById('featured');if(!a||!fe)return;
 const img=a.img||a.cardImg||'';
 const changed=fe.dataset.breakingId!==id;
 fe.className='featured cm-breaking-single';fe.dataset.breakingId=id;fe.removeAttribute('onclick');fe.setAttribute('aria-label','Ultima ora: '+a.title);
 if(changed||!fe.querySelector('.bg'))fe.innerHTML='<img class="bg" alt="" aria-hidden="true" decoding="async" fetchpriority="high" loading="eager" width="960" height="720"><div class="shade"></div><div class="txt"><span class="tag">Ultima ora</span><div class="breaking-meta">'+esc(a.badge)+(a.meta?' · '+esc(a.meta):'')+'</div><h1>'+esc(a.title)+'</h1><div class="breaking-reader"><p>'+esc(a.excerpt)+'</p></div><button class="cta" type="button">Leggi la notizia →</button></div>';
 const bg=fe.querySelector('.bg');if(bg&&img){if(bg.tagName==='IMG'){if(bg.getAttribute('src')!==img)bg.setAttribute('src',img)}else bg.style.setProperty('background-image','url("'+img.replace(/"/g,'%22')+'")','important')}
 const cta=fe.querySelector('.cta');if(cta&&!cta.dataset.cmBound){cta.dataset.cmBound='1';cta.addEventListener('click',e=>{e.stopPropagation();openId(fe.dataset.breakingId)})}
 if(!fe.dataset.cmBound){fe.dataset.cmBound='1';fe.addEventListener('click',e=>{if(!e.target.closest('button'))openId(fe.dataset.breakingId)})}
 const late=document.getElementById('latest');if(late)late.style.display='none';
}
function renderRail(){
 if(!install())return;
 const rail=document.getElementById('autoRail'),wrap=document.getElementById('autoRailWrap');if(!rail||!wrap)return;
 const ids=evidenzaIds();
 const railSignature=ids.join(',');
 if(rail.dataset.cmRailSignature!==railSignature){
  rail.innerHTML=ids.map(id=>{const a=articles[id],img=a.cardImg||a.img||'',has=!!img,href=(typeof EXTERNAL_PAGES!=='undefined'&&EXTERNAL_PAGES[id])||('#articolo='+encodeURIComponent(id));return '<a class="auto-card '+(has?'has-image':'')+'" data-id="'+esc(id)+'" href="'+esc(href)+'"><div class="athumb"'+(has?' data-cm-bg="'+esc(img)+'"':'')+'></div><div class="abody"><div class="ameta">'+esc(a.badge||a.cat||'')+'</div><h3>'+esc(a.shortTitle||a.title||'')+'</h3><p>'+esc(a.excerpt||'')+'</p></div></a>';}).join('');
  rail.dataset.cmRailSignature=railSignature;
 }
 cmLoadRailImages(rail);
 wrap.style.display='';
}
function markOrbit(){const cards=document.getElementById('cards');if(!cards)return;const main=(typeof currentMain!=='undefined'?currentMain:'all');cards.classList.toggle('cm-news-orbit',main==='all');}
const originalRenderCards=window.renderCards;
if(typeof originalRenderCards==='function')window.renderCards=function(){const r=originalRenderCards.apply(this,arguments);markOrbit();return r;};
window.buildAutoRail=renderRail;window.renderHero=renderBreaking;window.renderUltimaOra=renderBreaking;
function refresh(){install();renderRail();renderBreaking();markOrbit();}
/* Initial rendering is performed once by boot() after all discovery data has registered. */
window.addEventListener('pageshow',function(e){if(e.persisted)refresh();});
})();
;

/* cm-v26-sticky-orbit-js */
(function(){
  function makeFloatingHeader(){
    if(document.getElementById('cmFloatingHeader')) return;
    var original=document.querySelector('.header');
    if(!original) return;
    var bar=document.createElement('div');
    bar.id='cmFloatingHeader';bar.className='cm-floating-header';
    bar.innerHTML='<div class="cm-floating-inner"><a href="#" class="cm-floating-brand" aria-label="CurioMondo home"><img src="curiomondo-logo-96.webp" alt=""><strong>Curio<span>Mondo</span></strong></a><div class="cm-floating-actions"><button type="button" aria-label="Cerca nel sito" class="cm-float-search"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m21 21-4.4-4.4m2.4-5.1a7.5 7.5 0 1 1-15 0 7.5 7.5 0 0 1 15 0Z" fill="none" stroke="currentColor" stroke-linecap="round" stroke-width="2.1"/></svg></button><button type="button" aria-label="Apri menu" class="cm-float-menu">☰</button></div></div>';
    document.body.appendChild(bar);
    bar.querySelector('.cm-floating-brand').addEventListener('click',function(e){e.preventDefault();if(typeof goHomeFeed==='function')goHomeFeed()});
    bar.querySelector('.cm-float-search').addEventListener('click',function(){if(typeof openSiteSearch==='function')openSiteSearch()});
    bar.querySelector('.cm-float-menu').addEventListener('click',function(){if(typeof openDrawer==='function')openDrawer()});
    var searchStrip=document.getElementById('siteSearchStrip');
    var threshold=0;
    function measure(){
      var r=(searchStrip||original).getBoundingClientRect();
      threshold=window.scrollY+r.bottom;
    }
    function sync(){
      var showSearchHeader=searchStrip
        ? searchStrip.getBoundingClientRect().bottom<=0
        : window.scrollY>threshold;
      bar.classList.toggle('is-visible',showSearchHeader);
    }
    measure();sync();
    window.addEventListener('scroll',sync,{passive:true});
    window.addEventListener('resize',function(){measure();sync()},{passive:true});
    window.addEventListener('pageshow',function(){measure();sync()});
  }
  function orbitDepth(){
    var stage=document.getElementById('cmOrbitStage');if(!stage||window.matchMedia('(prefers-reduced-motion: reduce)').matches)return;
    stage.addEventListener('pointermove',function(e){if(e.pointerType==='touch')return;var r=stage.getBoundingClientRect();var x=(e.clientX-r.left)/r.width-.5;var y=(e.clientY-r.top)/r.height-.5;stage.style.transform='rotateY('+(x*5).toFixed(2)+'deg) rotateX('+(-y*4).toFixed(2)+'deg)'});
    stage.addEventListener('pointerleave',function(){stage.style.transform=''});
  }
  function initOptionalChrome(){makeFloatingHeader();orbitDepth()}
  if(window.scrollY>20)setTimeout(initOptionalChrome,0);else window.addEventListener('scroll',initOptionalChrome,{passive:true,once:true})
})();
;

/* cm-v27-quiz-orbit-js */
(function(){
  'use strict';
  const DATA_URL='assets/data/quiz-curiomondo.json';
  const LS_SEEN='cm_quiz_seen_v1', LS_STARS='cm_quiz_stars_v1', LS_PLAYED='cm_quiz_played_v1';
  const fallback=[
    {id:'fallback-1',category:'Cultura Generale',question:'Qual è la capitale dell’Australia?',options:['Sydney','Melbourne','Canberra','Perth'],correctIndex:2,explanation:'La capitale federale dell’Australia è Canberra.',curiosity:'Fu scelta anche per evitare la rivalità tra Sydney e Melbourne.'},
    {id:'fallback-2',category:'Indovinello Intelligente',question:'Più ne togli, più diventa grande. Che cos’è?',options:['Un buco','Una montagna','Una candela','Un’ombra'],correctIndex:0,explanation:'È un buco: togliendo materiale, il buco diventa più grande.',curiosity:'È un classico indovinello basato sull’inversione del significato di “togliere”.'},
    {id:'fallback-3',category:'Scienza & Natura',question:'Quale gas costituisce la maggior parte dell’atmosfera terrestre?',options:['Ossigeno','Azoto','Anidride carbonica','Argon'],correctIndex:1,explanation:'L’azoto costituisce circa il 78% dell’atmosfera terrestre.',curiosity:'L’ossigeno rappresenta circa il 21%.'},
    {id:'fallback-4',category:'Spazio',question:'Quanto impiega circa la luce del Sole a raggiungere la Terra?',options:['8 secondi','8 minuti','80 minuti','8 ore'],correctIndex:1,explanation:'La luce impiega circa 8 minuti e 20 secondi.',curiosity:'La distanza media Terra-Sole è circa 150 milioni di chilometri.'}
  ];
  let db=[], current=null, answered=false, previousFocus=null, opening=false;
  const $=id=>document.getElementById(id);
  const safeJSON=(key,fallbackValue)=>{try{const v=localStorage.getItem(key);return v?JSON.parse(v):fallbackValue}catch(e){return fallbackValue}};
  const saveJSON=(key,v)=>{try{localStorage.setItem(key,JSON.stringify(v))}catch(e){}};
  const getStars=()=>{try{return Math.max(0,parseInt(localStorage.getItem(LS_STARS)||'0',10)||0)}catch(e){return 0}};
  const setStars=n=>{try{localStorage.setItem(LS_STARS,String(n))}catch(e){};const el=$("cmQuizStars");if(el)el.textContent=String(n)};
  const getPlayed=()=>{try{return Math.max(0,parseInt(localStorage.getItem(LS_PLAYED)||'0',10)||0)}catch(e){return 0}};
  const setPlayed=n=>{try{localStorage.setItem(LS_PLAYED,String(n))}catch(e){}};
  const shuffle=a=>{const x=a.slice();for(let i=x.length-1;i>0;i--){const j=Math.floor(Math.random()*(i+1));[x[i],x[j]]=[x[j],x[i]]}return x};

  async function loadDB(){
    if(db.length)return db;
    try{
      const r=await fetch(DATA_URL,{cache:'no-store'});
      if(!r.ok)throw new Error('HTTP '+r.status);
      const d=await r.json();
      const list=Array.isArray(d)?d:(Array.isArray(d.items)?d.items:[]);
      db=list.filter(q=>q&&q.id&&q.question&&Array.isArray(q.options)&&q.options.length>=2&&Number.isInteger(q.correctIndex)&&q.correctIndex>=0&&q.correctIndex<q.options.length);
      if(!db.length)throw new Error('Dataset vuoto');
    }catch(e){db=fallback.slice()}
    return db;
  }

  function pickQuestion(){
    let seen=safeJSON(LS_SEEN,[]);if(!Array.isArray(seen))seen=[];
    const valid=new Set(db.map(q=>q.id));seen=seen.filter(id=>valid.has(id));
    let available=db.filter(q=>!seen.includes(q.id));
    let reset=false;
    if(!available.length){seen=[];available=db.slice();reset=true}
    const q=shuffle(available)[0];
    seen.push(q.id);saveJSON(LS_SEEN,seen);
    return {q,seenCount:seen.length,reset};
  }

  function animateCard(){const d=$("cmQuizDialog");if(!d)return;d.classList.remove('is-changing');void d.offsetWidth;d.classList.add('is-changing')}
  function renderQuestion(){
    if(!db.length)return;
    const picked=pickQuestion();current=picked.q;answered=false;animateCard();
    $("cmQuizCategory").textContent=current.category||'CurioMondo';
    $("cmQuizQuestion").textContent=current.question;
    $("cmQuizStars").textContent=String(getStars());
    const prog=$("cmQuizProgress");if(prog)prog.style.width=Math.max(2,Math.min(100,(picked.seenCount/db.length)*100))+'%';
    $("cmQuizCounter").textContent=(picked.reset?'Nuova orbita · ':'')+'Domanda '+picked.seenCount+' di '+db.length;
    const iw=$("cmQuizImageWrap"),im=$("cmQuizImage");
    if(current.image){im.src=current.image;im.alt=current.imageAlt||'Immagine collegata alla domanda';iw.classList.add('is-visible')}else{im.removeAttribute('src');im.alt='';iw.classList.remove('is-visible')}
    const options=$("cmQuizOptions");options.innerHTML='';
    current.options.forEach((txt,i)=>{
      const b=document.createElement('button');b.type='button';b.className='cm-quiz-option';b.dataset.letter=String.fromCharCode(65+i);b.textContent=txt;b.addEventListener('click',()=>answer(i,b));options.appendChild(b)
    });
    $("cmQuizExplanation").classList.remove('is-visible');$("cmQuizExplanationText").textContent='';$("cmQuizCuriosity").textContent='';
    $("cmQuizReveal").disabled=false;$("cmQuizNext").disabled=true;
  }

  function finish(selectedIndex,viaReveal){
    if(answered||!current)return;answered=true;setPlayed(getPlayed()+1);
    const btns=[...$("cmQuizOptions").querySelectorAll('.cm-quiz-option')];
    btns.forEach((b,i)=>{b.disabled=true;if(i===current.correctIndex)b.classList.add('is-correct')});
    if(selectedIndex!==null&&selectedIndex!==current.correctIndex&&btns[selectedIndex])btns[selectedIndex].classList.add('is-wrong');
    const correct=selectedIndex===current.correctIndex&&!viaReveal;
    if(correct)setStars(getStars()+1);
    $("cmQuizResultLabel").textContent=correct?'✓ Esatto · stella guadagnata':(viaReveal?'✦ Ecco la risposta':'Non proprio · ecco perché');
    $("cmQuizExplanationText").textContent=current.explanation||'';
    $("cmQuizCuriosity").textContent=current.curiosity||'';
    $("cmQuizExplanation").classList.add('is-visible');$("cmQuizReveal").disabled=true;$("cmQuizNext").disabled=false;
    setTimeout(()=>$("cmQuizNext").focus({preventScroll:true}),correct?420:260)
  }
  function answer(i){finish(i,false)}

  async function open(){
    if(opening)return;opening=true;previousFocus=document.activeElement;
    const modal=$("cmQuizModal");if(!modal){opening=false;return}
    modal.removeAttribute('inert');modal.classList.add('is-open');modal.setAttribute('aria-hidden','false');document.body.classList.add('cm-quiz-open');
    $("cmQuizLoading").hidden=false;$("cmQuizMain").hidden=true;
    await loadDB();
    $("cmQuizLoading").hidden=true;$("cmQuizMain").hidden=false;renderQuestion();opening=false;
    setTimeout(()=>$("cmQuizClose").focus({preventScroll:true}),50)
  }
  function close(){const modal=$("cmQuizModal");if(!modal)return;modal.classList.remove('is-open');modal.setAttribute('aria-hidden','true');modal.setAttribute('inert','');document.body.classList.remove('cm-quiz-open');if(previousFocus&&previousFocus.focus)previousFocus.focus({preventScroll:true})}
  function next(){if(!answered)return;renderQuestion();const d=$("cmQuizDialog");if(d)d.scrollTo({top:0,behavior:'smooth'})}

  window.openCurioQuiz=open;window.closeCurioQuiz=close;
  function init(){
    const modal=$("cmQuizModal");if(!modal)return;
    $("cmQuizClose").addEventListener('click',close);$("cmQuizReveal").addEventListener('click',()=>finish(null,true));$("cmQuizNext").addEventListener('click',next);
    modal.addEventListener('click',e=>{if(e.target===modal)close()});
    document.addEventListener('keydown',e=>{if(!modal.classList.contains('is-open'))return;if(e.key==='Escape')close();if(e.key==='Enter'&&answered&&document.activeElement!==$("cmQuizClose"))next()});
    // Precarica in modo asincrono quando l'utente si avvicina alla sezione Orbita.
    const hub=document.getElementById('usefulHub');
    if('IntersectionObserver'in window&&hub){const io=new IntersectionObserver(es=>{if(es.some(x=>x.isIntersecting)){loadDB();io.disconnect()}},{rootMargin:'350px'});io.observe(hub)}
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
;

/* cm-v30-earth-universe-js */
(function(){
  'use strict';
  var FACTS=[["GEOGRAFIA", "L’Oceano Pacifico è più grande di tutte le terre emerse del pianeta messe insieme."], ["TERRA", "Circa il 71% della superficie terrestre è coperto da acqua."], ["SPAZIO", "La Terra viaggia intorno al Sole a circa 30 chilometri al secondo."], ["OCEANI", "La maggior parte dell’attività vulcanica terrestre avviene sotto gli oceani."], ["GEOGRAFIA", "L’Antartide è il deserto più grande della Terra: un deserto è definito dalla scarsità di precipitazioni, non dal caldo."], ["NATURA", "Le foreste dell’Amazzonia attraversano nove Paesi e territori del Sud America."], ["ANIMALI", "I polpi hanno tre cuori e sangue ricco di rame, che appare bluastro."], ["LINGUE", "Nel mondo esistono migliaia di lingue vive; molte sono parlate da comunità molto piccole."], ["OCEANI", "Il punto più profondo conosciuto degli oceani si trova nella Fossa delle Marianne."], ["TERRA", "Il nucleo interno della Terra è solido, nonostante temperature paragonabili a quelle della superficie del Sole, grazie all’enorme pressione."], ["GEOGRAFIA", "La Russia si estende su undici fusi orari."], ["NATURA", "Un fulmine può riscaldare l’aria circostante a temperature superiori a quelle della superficie del Sole per un istante."], ["ANIMALI", "Le api comunicano la posizione delle fonti di cibo anche attraverso una particolare “danza” nell’alveare."], ["SPAZIO", "La Luna si allontana lentamente dalla Terra di pochi centimetri ogni anno."], ["OCEANI", "Più dell’80% dell’oceano non è stato ancora mappato e osservato in modo dettagliato."], ["GEOGRAFIA", "Il Lago Baikal contiene circa un quinto dell’acqua dolce superficiale non congelata del pianeta."], ["TERRA", "La durata del giorno terrestre non è perfettamente costante: varia leggermente per effetto di atmosfera, oceani e interazioni con la Luna."], ["ANIMALI", "Le balene blu sono gli animali più grandi conosciuti ad aver vissuto sulla Terra."], ["NATURA", "I funghi sono evolutivamente più vicini agli animali che alle piante."], ["GEOGRAFIA", "L’Africa è attraversata sia dall’Equatore sia dal meridiano di Greenwich."], ["STORIA", "L’Università di Bologna, fondata nell’XI secolo, è tradizionalmente considerata la più antica università del mondo occidentale ancora in attività."], ["ITALIA", "L’Italia ospita il maggior numero di siti iscritti nella Lista del Patrimonio Mondiale UNESCO tra i Paesi del mondo."], ["ANIMALI", "I corvi sono capaci di risolvere problemi complessi e di usare strumenti."], ["NATURA", "Alcuni alberi possono comunicare indirettamente attraverso reti sotterranee di funghi associate alle loro radici."], ["TERRA", "Il campo magnetico terrestre aiuta a deviare molte particelle cariche provenienti dal Sole."], ["GEOGRAFIA", "Il Sahara non è sempre stato un deserto: in passato ha attraversato periodi molto più verdi e umidi."], ["OCEANI", "Le correnti oceaniche trasportano enormi quantità di calore e contribuiscono a regolare il clima mondiale."], ["ANIMALI", "Gli elefanti possono comunicare anche con suoni a frequenze così basse da viaggiare per chilometri."], ["SPAZIO", "Se il Sole fosse una sfera di circa un metro di diametro, la Terra avrebbe dimensioni paragonabili a una piccola biglia e orbiterebbe a oltre cento metri di distanza."], ["TERRA", "Le placche tettoniche si muovono in genere di pochi centimetri all’anno, velocità simili alla crescita delle unghie."], ["LINGUE", "La Papua Nuova Guinea è uno dei Paesi con la maggiore diversità linguistica del pianeta."], ["ANIMALI", "I delfini usano fischi distintivi che possono funzionare in modo simile a “nomi” individuali."], ["NATURA", "Le mangrovie proteggono molte coste attenuando onde ed erosione e ospitano ecosistemi estremamente ricchi."], ["GEOGRAFIA", "Il monte Everest continua a cambiare altezza su scala geologica perché la placca indiana spinge contro quella eurasiatica."], ["OCEANI", "Il plancton marino svolge un ruolo enorme nel ciclo globale del carbonio e nella produzione di ossigeno."], ["TERRA", "L’atmosfera terrestre è composta soprattutto da azoto, mentre l’ossigeno rappresenta circa un quinto del totale."], ["ANIMALI", "Alcune tartarughe marine possono percepire il campo magnetico terrestre e usarlo come una sorta di mappa durante le migrazioni."], ["NATURA", "I bambù appartenenti ad alcune specie possono crescere decine di centimetri in un solo giorno in condizioni favorevoli."], ["GEOGRAFIA", "Il Nilo e l’Amazzonia si contendono il primato di fiume più lungo a seconda dei metodi usati per definirne sorgente e lunghezza."], ["SPAZIO", "Le aurore polari nascono quando particelle provenienti dal Sole interagiscono con l’atmosfera e il campo magnetico terrestre."], ["ANIMALI", "I tardigradi possono sopravvivere a condizioni estreme entrando in uno stato di attività metabolica quasi sospesa."], ["TERRA", "I continenti non sono immobili: tra milioni di anni la mappa del mondo sarà molto diversa da quella attuale."], ["STORIA", "Le prime città conosciute nacquero migliaia di anni fa in diverse regioni, tra cui la Mesopotamia."], ["NATURA", "Una singola barriera corallina può ospitare migliaia di specie e funzionare come una vera città biologica."], ["GEOGRAFIA", "Il Mar Morto si trova a centinaia di metri sotto il livello medio del mare ed è uno dei punti emersi più bassi della Terra."], ["ANIMALI", "I pinguini vivono nell’emisfero australe; in natura non convivono con gli orsi polari, che vivono nell’Artico."], ["TERRA", "La gravità non è identica in ogni punto del pianeta: varia leggermente con altitudine, latitudine e distribuzione delle masse."], ["NATURA", "Le sequoie giganti possono vivere per migliaia di anni."], ["GEOGRAFIA", "Esistono isole all’interno di laghi che si trovano a loro volta su isole: la geografia può creare strutture “annidate”."], ["OCEANI", "Le montagne sottomarine sono numerosissime e molte non emergono mai dalla superficie."], ["ANIMALI", "Le lontre marine spesso usano pietre come strumenti per aprire conchiglie e altri gusci duri."], ["TERRA", "La Terra non è una sfera perfetta: è leggermente schiacciata ai poli e più larga all’equatore."], ["NATURA", "La fotosintesi ha trasformato profondamente l’atmosfera terrestre nel corso della storia del pianeta."], ["GEOGRAFIA", "Indonesia e Filippine sono composte da migliaia di isole."], ["ANIMALI", "Gli squali esistono da molto prima dei dinosauri."], ["SPAZIO", "La luce del Sole impiega poco più di otto minuti per raggiungere la Terra."], ["TERRA", "Ogni giorno minuscole quantità di materiale extraterrestre entrano nell’atmosfera terrestre sotto forma di polvere cosmica."], ["NATURA", "Alcuni semi possono restare dormienti per anni e germinare solo quando le condizioni diventano favorevoli."], ["OCEANI", "Le maree sono influenzate soprattutto dalla gravità della Luna, con un contributo importante anche del Sole."], ["ANIMALI", "Le formiche formano società con divisione dei compiti, comunicazione chimica e strategie collettive molto complesse."]];
  var KEY_SEEN='cm_world_curiosities_seen_v1';
  var KEY_COUNT='cm_world_curiosities_count_v1';
  function $(id){return document.getElementById(id)}
  function getSeen(){try{var x=JSON.parse(localStorage.getItem(KEY_SEEN)||'[]');return Array.isArray(x)?x:[]}catch(e){return []}}
  function setSeen(x){try{localStorage.setItem(KEY_SEEN,JSON.stringify(x))}catch(e){}}
  function getCount(){try{return parseInt(localStorage.getItem(KEY_COUNT)||'0',10)||0}catch(e){return 0}}
  function setCount(n){try{localStorage.setItem(KEY_COUNT,String(n))}catch(e){}var el=$('cmEarthLearnedCount');if(el)el.textContent=String(n)}
  function pickFact(){
    var seen=getSeen();
    if(seen.length>=FACTS.length){seen=[];setSeen(seen)}
    var candidates=[];for(var i=0;i<FACTS.length;i++)if(seen.indexOf(i)<0)candidates.push(i);
    var idx=candidates[Math.floor(Math.random()*candidates.length)];
    seen.push(idx);setSeen(seen);
    var count=getCount()+1;setCount(count);
    return {category:FACTS[idx][0],text:FACTS[idx][1],count:count};
  }
  function showFact(){
    var box=$('cmWorldCuriosity');if(!box)return;
    var f=pickFact();
    $('cmWorldCuriosityCategory').textContent=f.category;
    $('cmWorldCuriosityText').textContent=f.text;
    $('cmWorldCuriosityCount').textContent=String(f.count);
    box.classList.remove('is-visible');box.removeAttribute('inert');box.setAttribute('aria-hidden','false');
    requestAnimationFrame(function(){requestAnimationFrame(function(){box.classList.add('is-visible')})});
    var core=$('cmEarthCore');if(core){core.classList.remove('is-learning');void core.offsetWidth;core.classList.add('is-learning')}
  }
  function boost(callback){
    var stage=$('cmOrbitStage');if(!stage){if(callback)callback();return}
    stage.classList.remove('is-hyper');void stage.offsetWidth;stage.classList.add('is-hyper');
    window.setTimeout(function(){stage.classList.remove('is-hyper');if(callback)callback()},720);
  }
  function action(name){
    if(name==='quiz')return function(){if(typeof openCurioQuiz==='function')openCurioQuiz()};
    if(name==='favs')return function(){if(typeof showFavs==='function')showFavs()};
    if(name==='about')return function(){window.location.href='pagine/chi-siamo.html'};
    if(name==='contact')return function(){window.location.href='pagine/contatti.html'};
    return function(){};
  }
  function init(){
    var core=$('cmEarthCore');if(core)core.addEventListener('click',showFact);
    var close=$('cmWorldCuriosityClose');if(close)close.addEventListener('click',function(){var b=$('cmWorldCuriosity');b.classList.remove('is-visible');b.setAttribute('aria-hidden','true');b.setAttribute('inert','')});
    document.querySelectorAll('[data-orbit-action]').forEach(function(btn){btn.addEventListener('click',function(){var fn=action(btn.getAttribute('data-orbit-action'));boost(fn)})});
    var boostBtn=$('cmEarthBoostBtn');if(boostBtn&&!window.cmV32TurboInstalled)boostBtn.addEventListener('click',function(){boost()});
    setCount(getCount());
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
;

/* cm-discovery-meloni-consensi-giovani-under-35-13-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="meloni_consensi_giovani_13_agosto_2026", url="notizie/meloni-consensi-giovani-under-35-13-agosto-2026.html", item={"title":"Meloni perde terreno tra i giovani: governo al 25% di approvazione tra gli under 35","shortTitle":"Meloni perde terreno tra i giovani: governo al 25% di approvazione tra gli under 35","excerpt":"Secondo dati YouTrend riportati da Reuters, la coalizione di governo è sotto il 30% tra gli under 35, mentre l’opposizione sfiora il 50%. Le politiche economiche e di sicurezza sono al centro del malcontento.","cat":"italia","sub":"politica","badge":"Italia · Politica · Sondaggi","badgeClass":"","meta":"13 agosto 2026 · Nuovo sviluppo","featured":true,"ultimaOra":true,"img":"assets/images/optimized/meloni-consensi-giovani-13-agosto-2026-960.webp","cardImg":"assets/images/optimized/meloni-consensi-giovani-13-agosto-2026-960.webp","body":"","sources":[]}, searchItem={"title":"Meloni perde terreno tra i giovani: governo al 25% di approvazione tra gli under 35","desc":"Secondo dati YouTrend riportati da Reuters, la coalizione di governo è sotto il 30% tra gli under 35, mentre l’opposizione sfiora il 50%. Le politiche economiche e di sicurezza sono al centro del malcontento.","text":"","url":"notizie/meloni-consensi-giovani-under-35-13-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-discovery-putin-iturup-giappone-isole-contese-13-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="putin_iturup_giappone_isole_contese_13_agosto_2026", url="notizie/putin-iturup-giappone-isole-contese-13-agosto-2026.html", item={"title":"Putin visita Iturup, il Giappone protesta: tensione sulle isole contese","shortTitle":"Putin visita Iturup, il Giappone protesta: tensione sulle isole contese","excerpt":"Il presidente russo ha visitato Iturup, chiamata Etorofu in Giappone, una delle isole controllate da Mosca e rivendicate da Tokyo. La premier Sanae Takaichi definisce la visita inaccettabile.","cat":"mondo","sub":"geopolitica","badge":"Mondo · Giappone · Russia","badgeClass":"","meta":"13 agosto 2026 · Ultima ora","featured":true,"ultimaOra":true,"img":"assets/images/optimized/putin-iturup-isole-contese-13-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/putin-iturup-isole-contese-13-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Putin visita Iturup, il Giappone protesta: tensione sulle isole contese","desc":"Il presidente russo ha visitato Iturup, chiamata Etorofu in Giappone, una delle isole controllate da Mosca e rivendicate da Tokyo. La premier Sanae Takaichi definisce la visita inaccettabile.","text":"","url":"notizie/putin-iturup-giappone-isole-contese-13-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-discovery-microsoft-riduce-presenza-cina-ai-azure-13-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="microsoft_cina_ai_azure_13_agosto_2026", url="notizie/microsoft-riduce-presenza-cina-ai-azure-13-agosto-2026.html", item={"title":"Microsoft riduce la presenza in Cina, ma l’AI la convince a restare","shortTitle":"Microsoft riduce la presenza in Cina, ma l’AI la convince a restare","excerpt":"Almeno 15 filiali e joint venture chiuse negli ultimi cinque anni. Le tensioni tra USA e Cina spingono Microsoft a ridurre le attività, ma Azure e l’AI per le imprese cinesi globali mantengono aperta una parte del business.","cat":"tecnologia","sub":"cina","badge":"Tecnologia · AI · Cina","badgeClass":"","meta":"13 agosto 2026 · Ultima ora","featured":true,"ultimaOra":true,"img":"assets/images/optimized/microsoft-cina-ai-13-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/microsoft-cina-ai-13-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Microsoft riduce la presenza in Cina, ma l’AI la convince a restare","desc":"Almeno 15 filiali e joint venture chiuse negli ultimi cinque anni. Le tensioni tra USA e Cina spingono Microsoft a ridurre le attività, ma Azure e l’AI per le imprese cinesi globali mantengono aperta una parte del business.","text":"","url":"notizie/microsoft-riduce-presenza-cina-ai-azure-13-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-discovery-colleferro-esplosione-fabbrica-munizioni-13-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="colleferro_esplosione_munizioni_13_agosto_2026";
  var url="notizie/colleferro-esplosione-fabbrica-munizioni-13-agosto-2026.html";
  var title="Esplosione in una fabbrica di munizioni a Colleferro: incendio nel reparto polveri, nessun ferito";
  var excerpt="Un incendio seguito da una forte esplosione ha colpito lo stabilimento KNDS Ammo Italy, ex Simmel Difesa. Nelle prime verifiche non risultano feriti né dispersi.";
  var item={
    title:title,
    shortTitle:title,
    excerpt:excerpt,
    cat:"italia",
    sub:"cronaca",
    badge:"Italia · Lazio · Cronaca",
    badgeClass:"",
    meta:"13 agosto 2026 · Ultima ora",
    featured:true,
    ultimaOra:true,
    img:"assets/images/optimized/colleferro-esplosione-fabbrica-munizioni-13-agosto-2026-ai-960.webp",
    cardImg:"assets/images/optimized/colleferro-esplosione-fabbrica-munizioni-13-agosto-2026-ai-960.webp",
    body:"",
    sources:[]
  };
  var searchItem={
    title:title,
    desc:excerpt,
    text:"Esplosione Colleferro KNDS Ammo Italy 13 agosto 2026 incendio reparto polveri ex Simmel Difesa fabbrica munizioni Roma Vigili del Fuoco nessun ferito nessun disperso Italia Lazio cronaca. Un incendio seguito da una forte esplosione ha colpito lo stabilimento KNDS Ammo Italy di Colleferro, in provincia di Roma. Le prime ricostruzioni indicano il reparto di pressatura delle polveri. Vigili del Fuoco, Carabinieri e investigatori sono sul posto per la messa in sicurezza e per accertare le cause dell’incidente.",
    url:url
  };
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  function refreshTicker(){
    var move=document.getElementById("tickerMove");
    if(!move)return;
    var seen={};
    var items=[{title:title,url:url}];
    move.querySelectorAll(".cm-ticker-set:not([aria-hidden]) .ticker-news").forEach(function(link){
      var href=link.getAttribute("href");
      var label=(link.textContent||"").replace(/^\s*✦\s*/,"").trim();
      if(href&&label)items.push({title:label,url:href});
    });
    items=items.filter(function(entry){
      if(seen[entry.url])return false;
      seen[entry.url]=true;
      return true;
    }).slice(0,10);
    function renderSet(hidden){
      return '<div class="cm-ticker-set"'+(hidden?' aria-hidden="true"':'')+'>'+items.map(function(entry){
        return '<a class="ticker-news" href="'+entry.url+'"><span aria-hidden="true">✦</span> '+entry.title+'</a>';
      }).join('')+'</div>';
    }
    move.innerHTML=renderSet(false)+renderSet(true);
  }

})();
;

/* cm-discovery-sara-curtis-record-mondo-50-dorso-parigi-13-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="sara_curtis_record_mondo_50_dorso_13_agosto_2026";
  var url="notizie/sara-curtis-oro-record-mondo-50-dorso-parigi-13-agosto-2026.html";
  var title="Sara Curtis nella storia: oro e nuovo record del mondo nei 50 dorso";
  var excerpt="Agli Europei di Parigi l’azzurra vince l’oro nei 50 dorso in 26”56, nuovo record mondiale. Ventiquattro ore prima aveva già nuotato in 26”63 in semifinale.";
  var item={
    title:title,
    shortTitle:title,
    excerpt:excerpt,
    cat:"sport",
    sub:"nuoto",
    badge:"Sport · Nuoto · Record mondiale",
    badgeClass:"",
    meta:"13 agosto 2026 · Ultima ora",
    featured:true,
    ultimaOra:true,
    img:"assets/images/optimized/sara-curtis-record-mondo-50-dorso-parigi-13-agosto-2026-ai-960.webp",
    cardImg:"assets/images/optimized/sara-curtis-record-mondo-50-dorso-parigi-13-agosto-2026-ai-960.webp",
    body:"",
    sources:[]
  };
  var searchItem={
    title:title,
    desc:excerpt,
    text:"Sara Curtis oro record mondiale 50 dorso 26.56 Parigi Europei nuoto 13 agosto 2026 Italia Kaylee McKeown. Sara Curtis, 19 anni, ha conquistato l’oro europeo nei 50 metri dorso con 26”56, migliorando il record del mondo che aveva già ottenuto in semifinale con 26”63. Il precedente primato era di Kaylee McKeown.",
    url:url
  };
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  function refreshTicker(){
    var move=document.getElementById("tickerMove");
    if(!move)return;
    var seen={};
    var items=[{title:title,url:url}];
    move.querySelectorAll(".cm-ticker-set:not([aria-hidden]) .ticker-news").forEach(function(link){
      var href=link.getAttribute("href");
      var label=(link.textContent||"").replace(/^\s*✦\s*/,"").trim();
      if(href&&label)items.push({title:label,url:href});
    });
    items=items.filter(function(entry){
      if(seen[entry.url])return false;
      seen[entry.url]=true;
      return true;
    }).slice(0,10);
    function renderSet(hidden){
      return '<div class="cm-ticker-set"'+(hidden?' aria-hidden="true"':'')+'>'+items.map(function(entry){
        return '<a class="ticker-news" href="'+entry.url+'"><span aria-hidden="true">✦</span> '+entry.title+'</a>';
      }).join('')+'</div>';
    }
    move.innerHTML=renderSet(false)+renderSet(true);
  }

})();
;

/* cm-discovery-infantino-nuova-zelanda-ritira-sostegno-fifa-14-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="infantino_nuova_zelanda_ritira_sostegno_fifa_14_agosto_2026";
  var url="notizie/infantino-nuova-zelanda-ritira-sostegno-fifa-14-agosto-2026.html";
  var title="Infantino sempre più sotto pressione: anche la Nuova Zelanda ritira il sostegno al presidente FIFA";
  var excerpt="New Zealand Football ritira il sostegno alla rielezione di Gianni Infantino e chiede una revisione indipendente del piano FIFA, poi ritirato, sui diritti commerciali.";
  var item={
    title:title,
    shortTitle:title,
    excerpt:excerpt,
    cat:"sport",
    sub:"calcio",
    badge:"Sport · Calcio · FIFA",
    badgeClass:"",
    meta:"14 agosto 2026 · Nuovo sviluppo",
    featured:true,
    ultimaOra:true,
    img:"assets/images/optimized/infantino-nuova-zelanda-ritira-sostegno-fifa-14-agosto-2026-ai-960.webp",
    cardImg:"assets/images/optimized/infantino-nuova-zelanda-ritira-sostegno-fifa-14-agosto-2026-ai-960.webp",
    body:"",
    sources:[]
  };
  var searchItem={
    title:title,
    desc:excerpt,
    text:"Infantino Nuova Zelanda ritira sostegno FIFA 14 agosto 2026 elezione presidente FIFA diritti commerciali Mondiali UEFA AFC CONCACAF. New Zealand Football ha ritirato il sostegno a Gianni Infantino e chiede una revisione indipendente del piano che avrebbe ceduto il 20% dei diritti commerciali delle competizioni FIFA per circa 4,2 miliardi di dollari.",
    url:url
  };
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  function refreshTicker(){
    var move=document.getElementById("tickerMove");
    if(!move)return;
    var seen={};
    var items=[{title:title,url:url}];
    move.querySelectorAll(".cm-ticker-set:not([aria-hidden]) .ticker-news").forEach(function(link){
      var href=link.getAttribute("href");
      var label=(link.textContent||"").replace(/^\s*✦\s*/,"").trim();
      if(href&&label)items.push({title:label,url:href});
    });
    items=items.filter(function(entry){
      if(seen[entry.url])return false;
      seen[entry.url]=true;
      return true;
    }).slice(0,10);
    function renderSet(hidden){
      return '<div class="cm-ticker-set"'+(hidden?' aria-hidden="true"':'')+'>'+items.map(function(entry){
        return '<a class="ticker-news" href="'+entry.url+'"><span aria-hidden="true">✦</span> '+entry.title+'</a>';
      }).join('')+'</div>';
    }
    move.innerHTML=renderSet(false)+renderSet(true);
  }

})();
;

/* cm-evergreen-registry-v1 */
(function(){
  "use strict";
  var catalog=Array.isArray(window.CM_EVERGREEN_CATALOG)?window.CM_EVERGREEN_CATALOG:[];
  window.CM_EVERGREEN_CATALOG=catalog;
  function render(){
    var grid=document.getElementById("cmEvergreenGrid");
    if(!grid)return;
    grid.innerHTML="";
    if(!catalog.length){
      var empty=document.createElement("p");
      empty.className="cm-evergreen-empty";
      empty.textContent="Stiamo preparando nuovi approfondimenti collegati alle notizie.";
      grid.appendChild(empty);
      return;
    }
    catalog.slice().reverse().forEach(function(item){
      var card=document.createElement("a"), tag=document.createElement("small"), heading=document.createElement("h3"), text=document.createElement("p"), action=document.createElement("b");
      card.className="cm-evergreen-card";
      card.href=item.url;
      tag.textContent=item.topic||"Approfondimento";
      heading.textContent=item.title;
      text.textContent=item.description||item.question||"Una guida per andare oltre la notizia.";
      action.textContent="Leggi l’approfondimento →";
      card.append(tag,heading,text,action);
      grid.appendChild(card);
    });
  }
  window.CM_registerEvergreen=function(item){
    if(!item||!item.id||!item.url||!item.title)return;
    var index=catalog.findIndex(function(entry){return entry.id===item.id;});
    if(index===-1)catalog.push(item);else catalog[index]=item;
    render();
  };
  window.CM_renderEvergreens=render;
  if(document.getElementById("cmEvergreenGrid")){if(document.readyState==="complete")render();else document.addEventListener("DOMContentLoaded",render,{once:true});}
})();
;

/* cm-discovery-evergreen-elezione-presidente-fifa */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="come_si_elegge_presidente_fifa_voti_mandato_regole";
  var url="notizie/come-si-elegge-presidente-fifa-voti-mandato-regole.html";
  var title="Come si elegge il presidente FIFA? Voti, mandato e regole spiegati";
  var excerpt="Chi vota, quanti voti servono e perché le confederazioni non controllano automaticamente il risultato dell’elezione FIFA.";
  articles[id]={
    title:title,
    shortTitle:title,
    excerpt:excerpt,
    cat:"sport",
    sub:"calcio",
    badge:"Sport · Calcio · Guida FIFA",
    badgeClass:"",
    meta:"Guida evergreen · Aggiornato 14 agosto 2026",
    featured:false,
    ultimaOra:false,
    img:"assets/images/optimized/come-si-elegge-presidente-fifa-voti-mandato-regole-ai-960.webp",
    cardImg:"assets/images/optimized/come-si-elegge-presidente-fifa-voti-mandato-regole-ai-960.webp",
    body:"",
    sources:[]
  };
  EXTERNAL_PAGES[id]=url;
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen({
    id:id,
    url:url,
    title:title,
    topic:"Sport · FIFA",
    question:"Chi elegge davvero il presidente FIFA e quanti voti servono?",
    description:"Voti, mandato e regole: la guida per capire che cosa succede alle elezioni FIFA."
  });
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift({title:title,desc:excerpt,text:"come si elegge presidente FIFA quanti voti servono mandato FIFA Congresso FIFA federazioni voto FIFA 211 federazioni un voto a testa maggioranza semplice due terzi",url:url});
})();
;

/* cm-v73-live-stability-js */
(function(){
  'use strict';

  function initLiveStability(){
    var tickerMove=document.getElementById('tickerMove');
    if(tickerMove){
      var primarySet=tickerMove.querySelector('.cm-ticker-set:not([aria-hidden])');
      tickerMove.querySelectorAll('.cm-ticker-set[aria-hidden="true"]').forEach(function(set){
        set.querySelectorAll('a,button,input,select,textarea,[tabindex]').forEach(function(control){
          control.setAttribute('tabindex','-1');
        });
      });

      function syncTickerSpeed(){
        if(!primarySet)return;
        if(window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches){
          tickerMove.style.setProperty('--cm-live-ticker-duration','160s');
          return;
        }
        var width=Math.ceil(primarySet.getBoundingClientRect().width);
        if(!width)return;
        var seconds=Math.max(64,Math.min(130,Math.round(width/115)));
        tickerMove.style.setProperty('--cm-live-ticker-duration',seconds+'s');
      }
      syncTickerSpeed();
      if(document.fonts&&document.fonts.ready)document.fonts.ready.then(syncTickerSpeed);
      window.addEventListener('resize',syncTickerSpeed,{passive:true});
    }

    var floating=document.getElementById('cmFloatingHeader');
    var searchStrip=document.getElementById('siteSearchStrip');
    if(!floating||!searchStrip)return;
    var controls=floating.querySelectorAll('button,a');
    function syncSearchHeader(){
      var showSearch=searchStrip.getBoundingClientRect().bottom<=0;
      floating.classList.toggle('is-visible',showSearch);
      floating.setAttribute('aria-hidden',showSearch?'false':'true');
      controls.forEach(function(control){
        if(showSearch)control.removeAttribute('tabindex');
        else control.setAttribute('tabindex','-1');
      });
    }
    syncSearchHeader();
    window.addEventListener('scroll',syncSearchHeader,{passive:true});
    window.addEventListener('resize',syncSearchHeader,{passive:true});
    window.addEventListener('pageshow',syncSearchHeader);
  }

  if(document.readyState==='complete')initLiveStability();else document.addEventListener('DOMContentLoaded',initLiveStability,{once:true});
})();
;

/* cm-evergreen-come-funzionano-robotaxi-sicurezza-regole-europa */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="come_funziona_robotaxi_sicurezza_regole_europa", url="notizie/come-funzionano-robotaxi-sicurezza-regole-europa.html", item={"title":"Come funzionano i robotaxi? Sono sicuri e quali regole devono rispettare in Europa?","shortTitle":"Come funzionano i robotaxi? Sono sicuri e quali regole devono rispettare in Europa?","excerpt":"Un robotaxi non è un’auto che può guidare ovunque e comunque: usa sensori, mappe e limiti precisi. Ecco cosa cambia per passeggeri, città e sicurezza stradale.","cat":"tecnologia","sub":"mobilità autonoma","badge":"Tecnologia / Mobilità autonoma","badgeClass":"","meta":"Guida aggiornata il 14 agosto 2026","featured":false,"ultimaOra":false,"img":"assets/images/optimized/come-funzionano-robotaxi-sicurezza-europa-ai-960.webp","cardImg":"assets/images/optimized/come-funzionano-robotaxi-sicurezza-europa-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Come funzionano i robotaxi? Sono sicuri e quali regole devono rispettare in Europa?","desc":"Un robotaxi non è un’auto che può guidare ovunque e comunque: usa sensori, mappe e limiti precisi. Ecco cosa cambia per passeggeri, città e sicurezza stradale.","text":"","url":"notizie/come-funzionano-robotaxi-sicurezza-regole-europa.html"}, hubItem={"id":"come_funziona_robotaxi_sicurezza_regole_europa","url":"notizie/come-funzionano-robotaxi-sicurezza-regole-europa.html","title":"Come funzionano i robotaxi? Sono sicuri e quali regole devono rispettare in Europa?","topic":"Tecnologia / Mobilità autonoma","question":"","description":"Un robotaxi non è un’auto che può guidare ovunque e comunque: usa sensori, mappe e limiti precisi. Ecco cosa cambia per passeggeri, città e sicurezza stradale."};
  articles[id]=item;
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen(hubItem);
})();
;

/* cm-discovery-uber-pony-ai-robotaxi-europa-14-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="uber_pony_ai_robotaxi_europa_14_agosto_2026", url="notizie/uber-pony-ai-robotaxi-europa-14-agosto-2026.html", item={"title":"Uber e Pony.ai puntano a oltre 2.000 robotaxi in Europa: l’espansione passa da Zagabria","shortTitle":"Uber e Pony.ai puntano a oltre 2.000 robotaxi in Europa: l’espansione passa da Zagabria","excerpt":"Pony.ai e Uber annunciano un piano per portare oltre 2.000 robotaxi in Europa. Dopo Zagabria, il progetto dovrebbe estendersi a quattro città europee che non sono state ancora indicate.","cat":"mondo","sub":"mobilità autonoma","badge":"Nuovo sviluppo","badgeClass":"","meta":"14 agosto 2026 · Nuovo sviluppo","featured":true,"ultimaOra":true,"img":"assets/images/optimized/uber-pony-ai-robotaxi-europa-14-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/uber-pony-ai-robotaxi-europa-14-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Uber e Pony.ai puntano a oltre 2.000 robotaxi in Europa: l’espansione passa da Zagabria","desc":"Pony.ai e Uber annunciano un piano per portare oltre 2.000 robotaxi in Europa. Dopo Zagabria, il progetto dovrebbe estendersi a quattro città europee che non sono state ancora indicate.","text":"","url":"notizie/uber-pony-ai-robotaxi-europa-14-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-discovery-debito-pubblico-italiano-record-3200-miliardi-14-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="debito_pubblico_italiano_record_3200_miliardi_14_agosto_2026", url="notizie/debito-pubblico-italiano-record-3200-miliardi-14-agosto-2026.html", item={"title":"Debito pubblico italiano, nuovo record storico: superati i 3.200 miliardi di euro","shortTitle":"Debito pubblico italiano, nuovo record storico: superati i 3.200 miliardi di euro","excerpt":"A giugno il debito delle amministrazioni pubbliche è salito a 3.203,5 miliardi di euro, secondo i dati della Banca d’Italia.","cat":"italia","sub":"economia e finanza","badge":"ITALIA · ECONOMIA","badgeClass":"","meta":"14 agosto 2026 · Economia","featured":true,"ultimaOra":true,"img":"../assets/images/optimized/debito-pubblico-italiano-14-agosto-2026-ai-960.webp","cardImg":"../assets/images/optimized/debito-pubblico-italiano-14-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Debito pubblico italiano, nuovo record storico: superati i 3.200 miliardi di euro","desc":"A giugno il debito delle amministrazioni pubbliche è salito a 3.203,5 miliardi di euro, secondo i dati della Banca d’Italia.","text":"","url":"notizie/debito-pubblico-italiano-record-3200-miliardi-14-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-discovery-terremoto-indonesia-7-7-maumere-20-morti-15-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="terremoto_indonesia_7_7_maumere_20_morti_15_agosto_2026", url="notizie/terremoto-indonesia-7-7-maumere-20-morti-15-agosto-2026.html", item={"title":"Terremoto 7,7 in Indonesia, il bilancio sale a 47 morti: oltre 150 case distrutte","shortTitle":"Terremoto 7,7 in Indonesia, il bilancio sale a 47 morti: oltre 150 case distrutte","excerpt":"Il nuovo bilancio Reuters parla di almeno 47 morti. Oltre 150 abitazioni sono state distrutte o gravemente danneggiate; i soccorsi restano difficili vicino a Nagekeo.","cat":"mondo","sub":"terremoti e asia","badge":"MONDO · TERREMOTI","badgeClass":"","meta":"15 agosto 2026 · Aggiornamento grave","featured":true,"ultimaOra":true,"img":"../assets/images/optimized/terremoto-indonesia-maumere-15-agosto-2026-ai-960.webp","cardImg":"../assets/images/optimized/terremoto-indonesia-maumere-15-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Terremoto 7,7 in Indonesia, il bilancio sale a 47 morti: oltre 150 case distrutte","desc":"Il nuovo bilancio Reuters parla di almeno 47 morti. Oltre 150 abitazioni sono state distrutte o gravemente danneggiate; i soccorsi restano difficili vicino a Nagekeo.","text":"","url":"notizie/terremoto-indonesia-7-7-maumere-20-morti-15-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-evergreen-perche-aumenta-debito-pubblico-italiano-cosa-cambia */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="perche_aumenta_debito_pubblico_italiano_cosa_cambia", url="notizie/perche-aumenta-debito-pubblico-italiano-cosa-cambia.html", item={"title":"Perché aumenta il debito pubblico italiano e cosa cambia per famiglie e imprese?","shortTitle":"Perché aumenta il debito pubblico italiano e cosa cambia per famiglie e imprese?","excerpt":"Dal significato dei 3.200 miliardi agli interessi, ai BTP e al rapporto debito-PIL: una guida per capire il debito pubblico senza tecnicismi inutili.","cat":"italia","sub":"economia e finanza","badge":"APPROFONDIMENTO · ECONOMIA","badgeClass":"","meta":"14 agosto 2026 · Approfondimento","featured":false,"ultimaOra":false,"img":"../assets/images/optimized/debito-pubblico-italiano-14-agosto-2026-ai-960.webp","cardImg":"../assets/images/optimized/debito-pubblico-italiano-14-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Perché aumenta il debito pubblico italiano e cosa cambia per famiglie e imprese?","desc":"Dal significato dei 3.200 miliardi agli interessi, ai BTP e al rapporto debito-PIL: una guida per capire il debito pubblico senza tecnicismi inutili.","text":"","url":"notizie/perche-aumenta-debito-pubblico-italiano-cosa-cambia.html"}, hubItem={"id":"perche_aumenta_debito_pubblico_italiano_cosa_cambia","url":"notizie/perche-aumenta-debito-pubblico-italiano-cosa-cambia.html","title":"Perché aumenta il debito pubblico italiano e cosa cambia per famiglie e imprese?","topic":"APPROFONDIMENTO · ECONOMIA","question":"","description":"Dal significato dei 3.200 miliardi agli interessi, ai BTP e al rapporto debito-PIL: una guida per capire il debito pubblico senza tecnicismi inutili."};
  articles[id]=item;
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen(hubItem);
})();
;

/* cm-evergreen-perche-indonesia-terremoti-frequenti-allerta-tsunami */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="perche_indonesia_terremoti_frequenti_allerta_tsunami", url="notizie/perche-indonesia-terremoti-frequenti-allerta-tsunami.html", item={"title":"Perché in Indonesia i terremoti sono così frequenti e quando può arrivare uno tsunami?","shortTitle":"Perché in Indonesia i terremoti sono così frequenti e quando può arrivare uno tsunami?","excerpt":"La guida per capire la Cintura di Fuoco, le allerte tsunami e le prime decisioni che possono salvare vite dopo una forte scossa.","cat":"mondo","sub":"terremoti e asia","badge":"APPROFONDIMENTO · TERREMOTI","badgeClass":"","meta":"15 agosto 2026 · Approfondimento","featured":false,"ultimaOra":false,"img":"../assets/images/optimized/terremoto-indonesia-maumere-15-agosto-2026-ai-960.webp","cardImg":"../assets/images/optimized/terremoto-indonesia-maumere-15-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Perché in Indonesia i terremoti sono così frequenti e quando può arrivare uno tsunami?","desc":"La guida per capire la Cintura di Fuoco, le allerte tsunami e le prime decisioni che possono salvare vite dopo una forte scossa.","text":"","url":"notizie/perche-indonesia-terremoti-frequenti-allerta-tsunami.html"}, hubItem={"id":"perche_indonesia_terremoti_frequenti_allerta_tsunami","url":"notizie/perche-indonesia-terremoti-frequenti-allerta-tsunami.html","title":"Perché in Indonesia i terremoti sono così frequenti e quando può arrivare uno tsunami?","topic":"APPROFONDIMENTO · TERREMOTI","question":"","description":"La guida per capire la Cintura di Fuoco, le allerte tsunami e le prime decisioni che possono salvare vite dopo una forte scossa."};
  articles[id]=item;
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen(hubItem);
})();
;

/* cm-discovery-ferran-torres-psg-trasferimento-barcellona-15-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="ferran_torres_psg_barcellona_15agosto_2026", url="notizie/ferran-torres-psg-trasferimento-barcellona-15-agosto-2026.html", item={"title":"Ferran Torres lascia il Barcellona: ufficiale il trasferimento al PSG fino al 2031","shortTitle":"Ferran Torres lascia il Barcellona: ufficiale il trasferimento al PSG fino al 2031","excerpt":"Il Paris Saint-Germain ha annunciato l’arrivo di Ferran Torres dal Barcellona. L’attaccante spagnolo ha firmato fino al 2031; secondo i media l’operazione vale circa 50 milioni di euro.","cat":"sport","sub":"calciomercato","badge":"Sport · Calciomercato","badgeClass":"","meta":"15 agosto 2026 · Calciomercato","featured":true,"ultimaOra":true,"img":"assets/images/optimized/ferran-torres-psg-calciomercato-15-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/ferran-torres-psg-calciomercato-15-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Ferran Torres lascia il Barcellona: ufficiale il trasferimento al PSG fino al 2031","desc":"Il Paris Saint-Germain ha annunciato l’arrivo di Ferran Torres dal Barcellona. L’attaccante spagnolo ha firmato fino al 2031; secondo i media l’operazione vale circa 50 milioni di euro.","text":"","url":"notizie/ferran-torres-psg-trasferimento-barcellona-15-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-evergreen-quando-trasferimento-calciomercato-ufficiale */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="quando_trasferimento_calciomercato_ufficiale", url="notizie/quando-trasferimento-calciomercato-ufficiale.html", item={"title":"Quando un trasferimento nel calciomercato è davvero ufficiale? Visite mediche, contratto e comunicati spiegati","shortTitle":"Quando un trasferimento nel calciomercato è davvero ufficiale? Visite mediche, contratto e comunicati spiegati","excerpt":"Una trattativa non diventa ufficiale al primo tweet: ecco cosa cambiano accordo, visite mediche, firma, registrazione e comunicato del club.","cat":"sport","sub":"calciomercato","badge":"Sport · Calciomercato","badgeClass":"","meta":"Guida aggiornata il 15 agosto 2026","featured":false,"ultimaOra":false,"img":"assets/images/optimized/ferran-torres-psg-calciomercato-15-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/ferran-torres-psg-calciomercato-15-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Quando un trasferimento nel calciomercato è davvero ufficiale? Visite mediche, contratto e comunicati spiegati","desc":"Una trattativa non diventa ufficiale al primo tweet: ecco cosa cambiano accordo, visite mediche, firma, registrazione e comunicato del club.","text":"","url":"notizie/quando-trasferimento-calciomercato-ufficiale.html"}, hubItem={"id":"quando_trasferimento_calciomercato_ufficiale","url":"notizie/quando-trasferimento-calciomercato-ufficiale.html","title":"Quando un trasferimento nel calciomercato è davvero ufficiale? Visite mediche, contratto e comunicati spiegati","topic":"Sport · Calciomercato","question":"","description":"Una trattativa non diventa ufficiale al primo tweet: ecco cosa cambiano accordo, visite mediche, firma, registrazione e comunicato del club."};
  articles[id]=item;
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen(hubItem);
})();
;

/* cm-discovery-uragano-lala-hawaii-big-island-blackout-alluvioni-16-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="uragano_lala_hawaii_big_island_16agosto_2026", url="notizie/uragano-lala-hawaii-big-island-blackout-alluvioni-16-agosto-2026.html", item={"title":"Uragano Lala sfiora la Big Island senza toccare terra: blackout, alluvioni e una vittima","shortTitle":"Uragano Lala sfiora la Big Island senza toccare terra: blackout, alluvioni e una vittima","excerpt":"Lala ha costeggiato la Big Island senza un impatto diretto, ma ha portato piogge torrenziali, raffiche violente, alluvioni e blackout a decine di migliaia di utenze.","cat":"mondo","sub":"usa","badge":"Ultima ora · Hawaii · Uragano","badgeClass":"","meta":"16 agosto 2026 · Ultimo aggiornamento","featured":true,"ultimaOra":true,"img":"assets/images/optimized/uragano-lala-hawaii-big-island-16-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/uragano-lala-hawaii-big-island-16-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Uragano Lala sfiora la Big Island senza toccare terra: blackout, alluvioni e una vittima","desc":"Lala ha costeggiato la Big Island senza un impatto diretto, ma ha portato piogge torrenziali, raffiche violente, alluvioni e blackout a decine di migliaia di utenze.","text":"","url":"notizie/uragano-lala-hawaii-big-island-blackout-alluvioni-16-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-evergreen-perche-uragani-colpiscono-raramente-hawaii */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="perche_uragani_colpiscono_raramente_hawaii", url="notizie/perche-uragani-colpiscono-raramente-hawaii.html", item={"title":"Perché gli uragani colpiscono raramente le Hawaii e quando diventano pericolosi?","shortTitle":"Perché gli uragani colpiscono raramente le Hawaii e quando diventano pericolosi?","excerpt":"Le Hawaii si trovano nel Pacifico tropicale, ma gli impatti diretti restano rari. Ecco come rotte, acqua, vento e montagne cambiano il rischio.","cat":"mondo","sub":"usa","badge":"Meteo · Hawaii · Come funziona","badgeClass":"","meta":"Guida aggiornata il 16 agosto 2026","featured":false,"ultimaOra":false,"img":"assets/images/optimized/uragano-lala-hawaii-big-island-16-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/uragano-lala-hawaii-big-island-16-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Perché gli uragani colpiscono raramente le Hawaii e quando diventano pericolosi?","desc":"Le Hawaii si trovano nel Pacifico tropicale, ma gli impatti diretti restano rari. Ecco come rotte, acqua, vento e montagne cambiano il rischio.","text":"","url":"notizie/perche-uragani-colpiscono-raramente-hawaii.html"}, hubItem={"id":"perche_uragani_colpiscono_raramente_hawaii","url":"notizie/perche-uragani-colpiscono-raramente-hawaii.html","title":"Perché gli uragani colpiscono raramente le Hawaii e quando diventano pericolosi?","topic":"Meteo · Hawaii · Come funziona","question":"","description":"Le Hawaii si trovano nel Pacifico tropicale, ma gli impatti diretti restano rari. Ecco come rotte, acqua, vento e montagne cambiano il rischio."};
  articles[id]=item;
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen(hubItem);
})();
;

/* cm-discovery-incendio-belgio-3000-ettari-germania-16-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="incendio_belgio_3000_ettari_germania_16agosto_2026", url="notizie/incendio-belgio-3000-ettari-germania-16-agosto-2026.html", item={"title":"Belgio, l’incendio più grande mai registrato raggiunge 3.000 ettari e avanza verso la Germania","shortTitle":"Belgio, l’incendio più grande mai registrato raggiunge 3.000 ettari e avanza verso la Germania","excerpt":"L’incendio nelle Hautes Fagnes ha bruciato circa 3.000 ettari. Il fronte si muove verso il confine tedesco mentre prosegue una vasta operazione internazionale.","cat":"mondo","sub":"incendi","badge":"Aggiornamento · Belgio · Incendio record","badgeClass":"","meta":"16 agosto 2026 · Aggiornamento importante","featured":true,"ultimaOra":true,"img":"assets/images/optimized/incendio-belgio-high-fens-16-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/incendio-belgio-high-fens-16-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Belgio, l’incendio più grande mai registrato raggiunge 3.000 ettari e avanza verso la Germania","desc":"L’incendio nelle Hautes Fagnes ha bruciato circa 3.000 ettari. Il fronte si muove verso il confine tedesco mentre prosegue una vasta operazione internazionale.","text":"","url":"notizie/incendio-belgio-3000-ettari-germania-16-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-evergreen-perche-incendi-torbiere-difficili-spegnere */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="perche_incendi_torbiere_difficili_spegnere", url="notizie/perche-incendi-torbiere-difficili-spegnere.html", item={"title":"Perché gli incendi nelle torbiere sono così difficili da spegnere e possono ripartire?","shortTitle":"Perché gli incendi nelle torbiere sono così difficili da spegnere e possono ripartire?","excerpt":"La torba può bruciare lentamente sotto terra, sfuggire ai controlli e riaccendere le fiamme in superficie. Ecco che cosa accade e come si interviene.","cat":"mondo","sub":"incendi","badge":"Ambiente · Incendi · Come funziona","badgeClass":"","meta":"Guida aggiornata il 16 agosto 2026","featured":false,"ultimaOra":false,"img":"assets/images/optimized/incendio-belgio-high-fens-16-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/incendio-belgio-high-fens-16-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Perché gli incendi nelle torbiere sono così difficili da spegnere e possono ripartire?","desc":"La torba può bruciare lentamente sotto terra, sfuggire ai controlli e riaccendere le fiamme in superficie. Ecco che cosa accade e come si interviene.","text":"","url":"notizie/perche-incendi-torbiere-difficili-spegnere.html"}, hubItem={"id":"perche_incendi_torbiere_difficili_spegnere","url":"notizie/perche-incendi-torbiere-difficili-spegnere.html","title":"Perché gli incendi nelle torbiere sono così difficili da spegnere e possono ripartire?","topic":"Ambiente · Incendi · Come funziona","question":"","description":"La torba può bruciare lentamente sotto terra, sfuggire ai controlli e riaccendere le fiamme in superficie. Ecco che cosa accade e come si interviene."};
  articles[id]=item;
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen(hubItem);
})();
;

/* cm-discovery-furto-antonello-da-messina-museo-messina-16-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="furto_antonello_da_messina_museo_messina_16agosto_2026", url="notizie/furto-antonello-da-messina-museo-messina-16-agosto-2026.html", item={"title":"Colpo al Museo di Messina: rubate quattro opere di Antonello da Messina","shortTitle":"Colpo al Museo di Messina: rubate quattro opere di Antonello da Messina","excerpt":"Tre tavole del Polittico di San Gregorio e una tavoletta bifronte attribuite ad Antonello da Messina sono state rubate al Museo Regionale. Indagini in corso.","cat":"italia","sub":"cronaca","badge":"Nuovo sviluppo · Messina · Furto d’arte","badgeClass":"","meta":"16 agosto 2026 · Nuovo sviluppo rilevante","featured":true,"ultimaOra":true,"img":"assets/images/optimized/furto-antonello-da-messina-museo-16-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/furto-antonello-da-messina-museo-16-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Colpo al Museo di Messina: rubate quattro opere di Antonello da Messina","desc":"Tre tavole del Polittico di San Gregorio e una tavoletta bifronte attribuite ad Antonello da Messina sono state rubate al Museo Regionale. Indagini in corso.","text":"","url":"notizie/furto-antonello-da-messina-museo-messina-16-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-evergreen-come-si-rintracciano-recuperano-opere-arte-rubate */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="come_si_rintracciano_recuperano_opere_arte_rubate", url="notizie/come-si-rintracciano-recuperano-opere-arte-rubate.html", item={"title":"Come si rintracciano e si recuperano le opere d’arte rubate?","shortTitle":"Come si rintracciano e si recuperano le opere d’arte rubate?","excerpt":"Dalla denuncia alle banche dati internazionali: ecco come fotografie, inventari, controlli doganali e verifiche sul mercato aiutano a recuperare i beni culturali.","cat":"italia","sub":"patrimonio","badge":"Cultura · Sicurezza · Come funziona","badgeClass":"","meta":"Guida aggiornata il 16 agosto 2026","featured":false,"ultimaOra":false,"img":"assets/images/optimized/furto-antonello-da-messina-museo-16-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/furto-antonello-da-messina-museo-16-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Come si rintracciano e si recuperano le opere d’arte rubate?","desc":"Dalla denuncia alle banche dati internazionali: ecco come fotografie, inventari, controlli doganali e verifiche sul mercato aiutano a recuperare i beni culturali.","text":"","url":"notizie/come-si-rintracciano-recuperano-opere-arte-rubate.html"}, hubItem={"id":"come_si_rintracciano_recuperano_opere_arte_rubate","url":"notizie/come-si-rintracciano-recuperano-opere-arte-rubate.html","title":"Come si rintracciano e si recuperano le opere d’arte rubate?","topic":"Cultura · Sicurezza · Come funziona","question":"","description":"Dalla denuncia alle banche dati internazionali: ecco come fotografie, inventari, controlli doganali e verifiche sul mercato aiutano a recuperare i beni culturali."};
  articles[id]=item;
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen(hubItem);
})();
;

/* cm-discovery-simona-quadarella-oro-400-stile-libero-tripletta-parigi-16-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="simona_quadarella_oro_400_stile_libero_tripletta_parigi_16agosto_2026", url="notizie/simona-quadarella-oro-400-stile-libero-tripletta-parigi-16-agosto-2026.html", item={"title":"Simona Quadarella regina d’Europa: oro nei 400 stile libero e terza tripletta storica","shortTitle":"Simona Quadarella regina d’Europa: oro nei 400 stile libero e terza tripletta storica","excerpt":"La romana vince i 400 stile libero in 4’01”34, record dei Campionati, e completa a Parigi la terza tripletta europea della carriera dopo 800 e 1.500.","cat":"sport","sub":"europei","badge":"Sport · Nuoto · Impresa storica","badgeClass":"","meta":"16 agosto 2026 · Impresa storica","featured":true,"ultimaOra":true,"img":"assets/images/optimized/simona-quadarella-oro-400-stile-parigi-16-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/simona-quadarella-oro-400-stile-parigi-16-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Simona Quadarella regina d’Europa: oro nei 400 stile libero e terza tripletta storica","desc":"La romana vince i 400 stile libero in 4’01”34, record dei Campionati, e completa a Parigi la terza tripletta europea della carriera dopo 800 e 1.500.","text":"","url":"notizie/simona-quadarella-oro-400-stile-libero-tripletta-parigi-16-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-evergreen-perche-400-800-1500-stile-libero-strategie-diverse */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="perche_400_800_1500_stile_libero_strategie_diverse", url="notizie/perche-400-800-1500-stile-libero-strategie-diverse.html", item={"title":"Perché 400, 800 e 1.500 stile libero richiedono strategie così diverse?","shortTitle":"Perché 400, 800 e 1.500 stile libero richiedono strategie così diverse?","excerpt":"Dal ritmo iniziale allo sprint finale: come cambiano distribuzione dello sforzo, tecnica e decisioni tattiche nelle tre gare del mezzofondo in piscina.","cat":"sport","sub":"tecnica","badge":"Sport · Nuoto · Come funziona","badgeClass":"","meta":"Guida aggiornata il 16 agosto 2026","featured":false,"ultimaOra":false,"img":"assets/images/optimized/simona-quadarella-oro-400-stile-parigi-16-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/simona-quadarella-oro-400-stile-parigi-16-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Perché 400, 800 e 1.500 stile libero richiedono strategie così diverse?","desc":"Dal ritmo iniziale allo sprint finale: come cambiano distribuzione dello sforzo, tecnica e decisioni tattiche nelle tre gare del mezzofondo in piscina.","text":"","url":"notizie/perche-400-800-1500-stile-libero-strategie-diverse.html"}, hubItem={"id":"perche_400_800_1500_stile_libero_strategie_diverse","url":"notizie/perche-400-800-1500-stile-libero-strategie-diverse.html","title":"Perché 400, 800 e 1.500 stile libero richiedono strategie così diverse?","topic":"Sport · Nuoto · Come funziona","question":"","description":"Dal ritmo iniziale allo sprint finale: come cambiano distribuzione dello sforzo, tecnica e decisioni tattiche nelle tre gare del mezzofondo in piscina."};
  articles[id]=item;
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen(hubItem);
})();
;

/* cm-discovery-trump-riduce-esercitazioni-usa-corea-sud-apertura-pyongyang-17-agosto-2026 */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="trump_riduce_esercitazioni_usa_corea_sud_apertura_pyongyang_17agosto_2026", url="notizie/trump-riduce-esercitazioni-usa-corea-sud-apertura-pyongyang-17-agosto-2026.html", item={"title":"Trump ordina di ridurre le esercitazioni militari con la Corea del Sud: apertura a Pyongyang","shortTitle":"Trump ordina di ridurre le esercitazioni militari con la Corea del Sud: apertura a Pyongyang","excerpt":"Il presidente USA chiede al Pentagono di ridimensionare sostanzialmente le Ulchi Freedom Shield, iniziate il 17 agosto. Un segnale politico verso Kim Jong Un mentre resta alta la tensione al confine coreano.","cat":"mondo","sub":"coree","badge":"Nuovo sviluppo · USA · Penisola coreana","badgeClass":"","meta":"17 agosto 2026 · Nuovo sviluppo di forte rilievo","featured":true,"ultimaOra":true,"img":"assets/images/optimized/trump-riduce-esercitazioni-usa-corea-sud-17-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/trump-riduce-esercitazioni-usa-corea-sud-17-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Trump ordina di ridurre le esercitazioni militari con la Corea del Sud: apertura a Pyongyang","desc":"Il presidente USA chiede al Pentagono di ridimensionare sostanzialmente le Ulchi Freedom Shield, iniziate il 17 agosto. Un segnale politico verso Kim Jong Un mentre resta alta la tensione al confine coreano.","text":"","url":"notizie/trump-riduce-esercitazioni-usa-corea-sud-apertura-pyongyang-17-agosto-2026.html"};
  articles[id]=item;
  var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
  cmRegisterLatestNews(id);
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
})();
;

/* cm-evergreen-cosa-sono-esercitazioni-militari-congiunte-usa-corea-sud */
(function(){
  "use strict";
  if(typeof articles === "undefined" || typeof EXTERNAL_PAGES === "undefined" || typeof CM_SEARCH_INDEX === "undefined") return;
  var id="cosa_sono_esercitazioni_militari_congiunte_usa_corea_sud", url="notizie/cosa-sono-esercitazioni-militari-congiunte-usa-corea-sud.html", item={"title":"Che cosa sono le esercitazioni militari congiunte USA-Corea del Sud?","shortTitle":"Che cosa sono le esercitazioni militari congiunte USA-Corea del Sud?","excerpt":"Dalle simulazioni al coordinamento sul campo: come funzionano Freedom Shield e Ulchi Freedom Shield, perché contano per l’alleanza e perché Pyongyang le considera ostili.","cat":"mondo","sub":"coree","badge":"Geopolitica · Coree · Come funziona","badgeClass":"","meta":"Guida aggiornata il 17 agosto 2026","featured":false,"ultimaOra":false,"img":"assets/images/optimized/trump-riduce-esercitazioni-usa-corea-sud-17-agosto-2026-ai-960.webp","cardImg":"assets/images/optimized/trump-riduce-esercitazioni-usa-corea-sud-17-agosto-2026-ai-960.webp","body":"","sources":[]}, searchItem={"title":"Che cosa sono le esercitazioni militari congiunte USA-Corea del Sud?","desc":"Dalle simulazioni al coordinamento sul campo: come funzionano Freedom Shield e Ulchi Freedom Shield, perché contano per l’alleanza e perché Pyongyang le considera ostili.","text":"","url":"notizie/cosa-sono-esercitazioni-militari-congiunte-usa-corea-sud.html"}, hubItem={"id":"cosa_sono_esercitazioni_militari_congiunte_usa_corea_sud","url":"notizie/cosa-sono-esercitazioni-militari-congiunte-usa-corea-sud.html","title":"Che cosa sono le esercitazioni militari congiunte USA-Corea del Sud?","topic":"Geopolitica · Coree · Come funziona","question":"","description":"Dalle simulazioni al coordinamento sul campo: come funzionano Freedom Shield e Ulchi Freedom Shield, perché contano per l’alleanza e perché Pyongyang le considera ostili."};
  articles[id]=item;
  EXTERNAL_PAGES[id]=url;
  for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url) CM_SEARCH_INDEX.splice(i,1);}
  CM_SEARCH_INDEX.unshift(searchItem);
  if(typeof window.CM_registerEvergreen === "function") window.CM_registerEvergreen(hubItem);
})();
;

/* cm-v116-pending-discovery: registra i nuovi contenuti una sola volta prima del boot. */
(function(){
  var queue=Array.isArray(window.CM_PENDING_DISCOVERY)?window.CM_PENDING_DISCOVERY:[];
  if(!queue.length||typeof articles==='undefined'||typeof EXTERNAL_PAGES==='undefined'||typeof CM_SEARCH_INDEX==='undefined')return;
  queue.forEach(function(entry){
    if(!entry||!entry.id||!entry.url||!entry.item)return;
    var id=entry.id,url=entry.url;
    articles[id]=entry.item;
    EXTERNAL_PAGES[id]=url;
    if(!entry.evergreen){
      var latest=Array.isArray(window.CM_LATEST_NEWS)?window.CM_LATEST_NEWS.slice():[];
      cmRegisterLatestNews(id);
    }
    if(entry.searchItem){
      for(var i=CM_SEARCH_INDEX.length-1;i>=0;i--){if(CM_SEARCH_INDEX[i]&&CM_SEARCH_INDEX[i].url===url)CM_SEARCH_INDEX.splice(i,1);}
      CM_SEARCH_INDEX.unshift(entry.searchItem);
    }
    if(entry.evergreen&&entry.hubItem&&typeof window.CM_registerEvergreen==='function')window.CM_registerEvergreen(entry.hubItem);
  });
  window.CM_PENDING_DISCOVERY=[];
})();

/* Controllo prestazionale senza effetti visivi. */
(function(){
  var universe=document.getElementById('usefulHub');
  if(universe&&'IntersectionObserver'in window){
    var io=new IntersectionObserver(function(entries){
      entries.forEach(function(entry){universe.classList.toggle('cm-perf-paused',!entry.isIntersecting)});
    },{rootMargin:'160px'});
    io.observe(universe);
  }
})();
