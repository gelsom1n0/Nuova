# Dalla cellula al tracciato: elettrofisiologia

!!! obiettivi "In questa parte"
    Come una cellula cardiaca si carica e si scarica, quali ioni attraversano la membrana in ciascuna fase e quali farmaci agiscono su quei passaggi; perché alcune cellule battono da sole e altre no; che cosa sono l'automatismo, la conduzione, la refrattarietà, il rientro e l'attività triggerata. Nella seconda metà: come l'attività elettrica di milioni di cellule diventa un vettore, come le derivazioni lo «guardano» da angolazioni diverse, come si legge la carta e che cosa rappresenta ogni onda e ogni intervallo, con i valori normali dell'adulto. Fonti dei valori: raccomandazioni AHA/ACC/HRS per la standardizzazione e l'interpretazione dell'ECG (parte I, 2007; parti III–IV, 2009). Lo schema riassuntivo e gli 8 esercizi sono in fondo alla Parte.

## Il potenziale di riposo e il potenziale d'azione

### La membrana come una batteria

Ogni cellula del cuore è separata dall'ambiente esterno da una membrana che si comporta come una piccola batteria: all'interno la carica è negativa rispetto all'esterno. Questa differenza di carica, misurata in millivolt (mV), si chiama **[potenziale di membrana]{.ix}**. Nasce da due fatti. Il primo è che gli ioni non sono distribuiti in modo uguale: il potassio (K⁺) è molto concentrato dentro la cellula, il sodio (Na⁺) e il calcio (Ca²⁺) fuori. Il secondo è che la membrana, a riposo, lascia passare quasi soltanto il potassio, attraverso canali sempre aperti.

Il potassio tende quindi a uscire, spinto dalla differenza di concentrazione; ogni ione che esce porta fuori una carica positiva e lascia l'interno un po' più negativo. Si arriva a un equilibrio quando la negatività interna, che trattiene il potassio, bilancia la spinta della concentrazione. Nel miocita ventricolare questo equilibrio corrisponde a circa −90 mV: è il **[potenziale di riposo]{.ix}**. La differenza di concentrazione è mantenuta da una pompa, la **[pompa sodio-potassio]{.ix}** (Na⁺/K⁺-ATPasi), che consuma energia (ATP) e scambia tre ioni sodio portati fuori con due ioni potassio portati dentro.

| Ione | Dentro la cellula (mmol/L, indicativo) | Fuori, nel plasma (mmol/L) | Che cosa fa nel cuore |
|---|---|---|---|
| Potassio (K⁺) | ≈ 140–150 | 3,5–5,0 | determina il potenziale di riposo; ripolarizza (fase 3) |
| Sodio (Na⁺) | ≈ 10–15 | 135–145 | depolarizzazione rapida di atri, ventricoli e Purkinje (fase 0) |
| Calcio (Ca²⁺) | ≈ 0,0001 (libero) | ≈ 1,1–1,3 (ionizzato) | plateau (fase 2), contrazione; fase 0 del nodo del seno e del nodo atrioventricolare (AV) |

!!! chiave "Regola – Il potassio comanda il riposo"
    Il potenziale di riposo dipende soprattutto dal **rapporto tra potassio dentro e fuori** la cellula. Per questo variazioni piccole del potassio plasmatico (pochi decimi di mmol/L) cambiano l'eccitabilità del cuore e il tracciato: il potassio è l'elettrolita che l'infermiere di cardiologia controlla più spesso.

### Il potenziale d'azione del miocita contrattile

Quando una cellula vicina si attiva, una piccola corrente porta la membrana dal riposo verso un valore meno negativo. Se si raggiunge la **soglia** (circa −70 mV nel miocita ventricolare), si aprono di colpo i canali del sodio e parte il **[potenziale d'azione]{.ix}**, una sequenza stereotipata di variazioni del voltaggio che dura circa 250–300 ms e si descrive in cinque fasi, numerate da 0 a 4.

::: fig SCH-PA-VENT
Potenziale d'azione del miocita ventricolare. Si osservino la salita quasi verticale della **fase 0** (ingresso di sodio), il breve picco della **fase 1**, il lungo **plateau** della fase 2 (ingresso di calcio bilanciato dall'uscita di potassio), la discesa della **fase 3** (uscita di potassio) e il ritorno al riposo di −90 mV (**fase 4**). La barra in basso indica il periodo refrattario assoluto, durante il quale la cellula non risponde a nessuno stimolo.
:::

- **Fase 0 – depolarizzazione rapida.** I canali rapidi del sodio si aprono per circa un millisecondo; il sodio entra in massa e il potenziale sale fino a +20/+30 mV. La velocità di questa salita decide la velocità con cui l'impulso si propaga da una cellula all'altra.
- **Fase 1 – ripolarizzazione precoce.** I canali del sodio si chiudono (si *inattivano*) e una breve corrente di potassio in uscita (corrente transitoria, Ito) riporta il potenziale verso zero.
- **Fase 2 – plateau.** Si aprono i canali del calcio di tipo L: il calcio che entra mantiene la membrana intorno a 0 mV mentre il potassio comincia a uscire. È la fase che rende il potenziale d'azione cardiaco lungo e che accoppia l'evento elettrico alla contrazione: il calcio entrato libera altro calcio dalle riserve interne della cellula e attiva le proteine contrattili.
- **Fase 3 – ripolarizzazione.** I canali del calcio si chiudono e prevalgono le correnti di potassio in uscita (le più importanti si chiamano IKr e IKs); il potenziale ritorna a −90 mV.
- **Fase 4 – riposo.** La membrana resta stabile grazie ai canali del potassio sempre aperti (IK1); la pompa sodio-potassio e lo scambiatore sodio-calcio ristabiliscono le concentrazioni.

Il miocita contrattile, a riposo, **non si attiva da solo**: la sua fase 4 è piatta e aspetta lo stimolo che arriva dalle cellule vicine. Le cellule degli atri hanno un potenziale d'azione simile ma più breve; le fibre di Purkinje lo hanno più lungo e con una fase 4 lievemente instabile, che spiega la loro capacità di fare da pacemaker di riserva.

### Il potenziale d'azione della cellula pacemaker

Le cellule del **[nodo del seno]{.ix}** (nodo senoatriale) e del **nodo AV** funzionano in modo diverso. Hanno pochissimi canali del potassio che stabilizzano il riposo (IK1), per cui il loro potenziale più negativo è soltanto −60 mV circa; inoltre i canali rapidi del sodio, a quel voltaggio, sono in gran parte inattivi. Ne derivano due caratteristiche.

::: fig SCH-PA-NSA
Potenziale d'azione della cellula del nodo del seno. Manca un vero riposo: durante la **fase 4** il potenziale sale lentamente da circa −60 mV fino alla soglia di circa −40 mV (depolarizzazione diastolica spontanea, sostenuta dalla corrente «funny» If e poi dal calcio); la **fase 0** è lenta perché è dovuta al calcio; non ci sono le fasi 1 e 2; la **fase 3** è dovuta all'uscita di potassio. Ogni ciclo genera un battito: nell'esempio 75/min.
:::

La prima è la **[depolarizzazione diastolica spontanea]{.ix}**: in fase 4 la membrana non resta ferma, ma sale lentamente fino alla soglia. All'inizio della salita c'è una corrente in entrata di sodio, chiamata **corrente «funny» (If)**, che ha la particolarità di attivarsi quando la cellula è più negativa; nella seconda parte contribuiscono canali del calcio. Raggiunta la soglia, parte da sola un nuovo potenziale d'azione: questo è l'**automatismo**. La seconda caratteristica è che la fase 0 è sostenuta dal **calcio** (canali di tipo L), non dal sodio: la salita è lenta e la conduzione da cellula a cellula è lenta. Nel nodo AV questa lentezza è utile, perché crea il ritardo tra la contrazione degli atri e quella dei ventricoli.

La pendenza della fase 4 decide la frequenza cardiaca. Il simpatico, attraverso i recettori beta-1, aumenta la corrente If e quella del calcio: la fase 4 diventa più ripida, la soglia si raggiunge prima, il cuore accelera. Il vago (acetilcolina) apre canali del potassio che rendono la cellula più negativa e riduce la corrente If: la fase 4 si appiattisce e il cuore rallenta. I farmaci che rallentano il seno agiscono qui: i beta-bloccanti tolgono lo stimolo simpatico, l'**[ivabradina]{.pa}** blocca direttamente la corrente If e riduce la frequenza senza ridurre la forza di contrazione.

| Caratteristica | Miocita contrattile (atri, ventricoli) | Cellula pacemaker (nodo del seno, nodo AV) |
|---|---|---|
| Potenziale più negativo | ≈ −90 mV, stabile | ≈ −60 mV, instabile |
| Fase 4 | piatta: attende lo stimolo | sale da sola: automatismo |
| Fase 0 | rapida, da sodio | lenta, da calcio |
| Plateau (fase 2) | presente e lungo | assente |
| Velocità di conduzione | alta | bassa (nodo AV ≈ 0,05 m/s) |
| Farmaci che la modificano di più | bloccanti del sodio (classe I) e del potassio (classe III) | beta-bloccanti, calcio-antagonisti non diidropiridinici, ivabradina, digossina, adenosina |

!!! autotest "Autotest"
    **1.** Perché una cellula del nodo del seno può attivarsi da sola e un miocita ventricolare no?

    {{righe:2}}

    **2.** Quale ione sostiene la fase 0 nel nodo AV? Che cosa significa per la velocità di conduzione?

    {{righe:2}}

## I canali ionici e i farmaci che li bloccano

### Tre ioni, tre famiglie di canali

I **[canali ionici]{.ix}** sono proteine della membrana che formano un poro selettivo per un solo ione e che si aprono e si chiudono in risposta al voltaggio. Per capire l'ECG e i farmaci antiaritmici bastano tre famiglie.

I **canali del sodio** rapidi si aprono all'inizio della fase 0 e si inattivano dopo circa un millisecondo; restano inattivi finché la cellula non si è ripolarizzata. Sono il motore della conduzione rapida in atri, ventricoli e sistema di His-Purkinje. Se si bloccano, la fase 0 si appiattisce, l'impulso viaggia più lentamente e il **QRS si allarga**. Un effetto simile si osserva quando la cellula è meno negativa a riposo, come nell'iperpotassiemia: una parte dei canali del sodio resta inattiva e la conduzione rallenta.

I **canali del calcio** di tipo L si aprono più lentamente e restano aperti più a lungo: sostengono il plateau nei miociti e la fase 0 nelle cellule nodali. Se si bloccano, nel nodo del seno la frequenza scende, nel nodo AV la conduzione rallenta (il **PR si allunga**) e nei miociti la contrazione si riduce.

I **canali del potassio** sono numerosi: alcuni stabilizzano il riposo (IK1), altri ripolarizzano la cellula in fase 3 (IKr, IKs). La corrente IKr passa attraverso un canale codificato dal gene *hERG*: è il bersaglio involontario di moltissimi farmaci, anche non cardiologici, che per questo allungano la ripolarizzazione e il **QT**. Se si bloccano i canali della fase 3, il potenziale d'azione si allunga, il periodo refrattario aumenta e il QT si prolunga.

!!! chiave "Regola – Ione, onda, farmaco"
    **Sodio → QRS** (velocità di conduzione nei ventricoli) → antiaritmici di classe I.
    **Calcio → PR e frequenza** (nodo AV e nodo del seno) → calcio-antagonisti non diidropiridinici (classe IV); i beta-bloccanti (classe II) agiscono sugli stessi tessuti per via indiretta.
    **Potassio → QT e onda T** (ripolarizzazione) → classe III; e tutti i farmaci che bloccano hERG.

### La classificazione di Vaughan Williams collegata all'ECG

La classificazione degli antiaritmici più usata nella pratica è quella di **[Vaughan Williams]{.ix voce="Classificazione di Vaughan Williams"}**, che raggruppa i farmaci secondo il bersaglio principale. È semplice ma imperfetta: molti farmaci hanno più azioni (l'amiodarone le ha tutte e quattro) e alcuni farmaci importanti, come l'adenosina e la digossina, restano fuori dalle quattro classi. Nel 2018 ne è stata proposta una versione aggiornata e ampliata (Lei e collaboratori, *Circulation* 2018), che aggiunge, tra l'altro, una classe 0 per la corrente If e classi per i recettori dell'adenosina e muscarinici; nel 2025 il documento di consenso EHRA/ESC *Practical Compendium of Antiarrhythmic Drugs* l'ha adottata. Nella pratica di reparto il riferimento resta comunque alle quattro classi storiche, che bastano a collegare il farmaco al suo segno sul tracciato. La tabella che segue unisce, per ogni classe, il bersaglio, il segno che lascia sul tracciato e le molecole; il dettaglio clinico dei farmaci (indicazioni, dosi, sicurezza) è nella Parte 8.

| Bersaglio (ione o recettore) | Che cosa cambia sul tracciato | Classe e farmaci |
|---|---|---|
| Canali del Na⁺, blocco intermedio; anche K⁺ | QRS più largo e **QT più lungo** | Ia: [disopiramide]{.pa} (uso oggi limitato; la procainamide non è autorizzata in Italia) |
| Canali del Na⁺, blocco breve (rapida dissociazione), più marcato nel tessuto ischemico | poco evidente; QT invariato o lievemente più corto | Ib: [lidocaina]{.pa} |
| Canali del Na⁺, blocco marcato e lento a dissociarsi | **QRS largo**, più evidente a frequenza alta; PR lievemente più lungo | Ic: [flecainide]{.pa}, [propafenone]{.pa} |
| Recettori beta-1 (riducono l'effetto del simpatico su If e Ca²⁺) | frequenza cardiaca (FC) più bassa, **PR più lungo** | II: beta-bloccanti ([metoprololo]{.pa}, [bisoprololo]{.pa}, [esmololo]{.pa}) |
| Canali del K⁺ della fase 3 (IKr) | **QT lungo**, T più larghe, a volte onda U | III: [amiodarone]{.pa}, [sotalolo]{.pa}, [dronedarone]{.pa}, [ibutilide]{.pa} |
| Canali del Ca²⁺ di tipo L nei nodi | FC più bassa, **PR più lungo**, blocco AV | IV: [verapamil]{.pa}, [diltiazem]{.pa} |
| Corrente If del nodo del seno | solo FC più bassa | classe 0 nella classificazione del 2018: [ivabradina]{.pa} |
| Recettori A1 dell'adenosina (aprono canali del K⁺ nel nodo AV) | pausa o blocco AV di pochi secondi | [adenosina]{.pa} |
| Pompa Na⁺/K⁺-ATPasi e tono vagale | ST «a cucchiaio», PR più lungo, FC più bassa | [digossina]{.pa} |

Due conseguenze pratiche derivano direttamente dalla tabella. La prima: un farmaco che blocca il sodio si sorveglia misurando il **QRS**, un farmaco che blocca il potassio misurando il **QT**, un farmaco che agisce sui nodi misurando **frequenza e PR**. La seconda: gli effetti si sommano. Un beta-bloccante con un calcio-antagonista non diidropiridinico, o con l'amiodarone, può rallentare troppo il nodo del seno e il nodo AV; due farmaci che bloccano hERG, anche se uno è un antibiotico o un antiemetico, allungano il QT più di ciascuno da solo.

### Gli elettroliti modificano gli stessi bersagli

Gli elettroliti agiscono sugli stessi canali dei farmaci e lasciano segni simili. L'**[iperpotassiemia]{.ix}** rende meno negativo il riposo: parte dei canali del sodio si inattiva, la conduzione rallenta (P appiattite, QRS largo) e la ripolarizzazione accelera (T alte e appuntite). L'**[ipopotassiemia]{.ix}** riduce le correnti di potassio della fase 3: la ripolarizzazione si allunga e compare l'onda U. Il calcio regola la durata del plateau: l'**[ipocalcemia]{.ix}** allunga il tratto ST, l'ipercalcemia lo accorcia. La carenza di magnesio favorisce le aritmie ventricolari e rende difficile correggere l'ipopotassiemia (Parte 9).

!!! nota "QT che si allunga dopo l'inizio del sotalolo"
    **Situazione.** Paziente con fibrillazione atriale parossistica, in reparto per l'avvio della terapia con sotalolo; al terzo giorno l'ECG di controllo mostra un QT più lungo del basale.
    **Cosa si vede.** Ritmo sinusale a 58/min, QT misurato 0,52 s, QT corretto per la frequenza (QTc) ≈ 0,51 s con Bazett (basale 0,43 s); T larghe, a tratti con una gobba terminale.
    **Cosa si fa.** Il QTc oltre 500 ms e l'aumento di oltre 60 ms rispetto al basale sono soglie di rischio di torsione di punta: si informa subito il medico prima della dose successiva, che spetta a lui confermare, ridurre o sospendere; si controllano potassio, magnesio e funzione renale.
    **Il farmaco, in due righe.** Il [sotalolo]{.pa} è un beta-bloccante con un'azione di classe III: blocca i canali del potassio della ripolarizzazione e allunga il potenziale d'azione; per questo previene le recidive di aritmia ma allunga il QT, tanto di più quanto più la frequenza è bassa e la funzione renale ridotta.
    **Occhio infermieristico.** Misurare il QT sempre nella stessa derivazione e con lo stesso metodo di correzione; controllare la lista dei farmaci in corso alla ricerca di altri farmaci che allungano il QT; documentare l'ora dell'ECG rispetto alla dose.

## Automatismo, conduzione, periodo refrattario; rientro e attività triggerata

### Automatismo e gerarchia dei pacemaker

Molte cellule del cuore possiedono automatismo, ma con frequenze diverse. Il nodo del seno è il più rapido (60–100/min a riposo); le cellule della giunzione AV, cioè della zona di passaggio tra nodo AV e fascio di His, scaricano spontaneamente a 40–60/min; le fibre di Purkinje dei ventricoli a 20–40/min. In condizioni normali comanda il più veloce: ogni impulso sinusale arriva ai pacemaker più lenti prima che questi raggiungano la soglia e li «scarica» in anticipo. Il fenomeno si chiama **[soppressione da overdrive]{.ix}**: un pacemaker veloce mantiene silenziosi quelli più lenti.

::: fig SCH-CONDUZ
Sistema di conduzione a blocchi. Dall'alto: nodo del seno (pacemaker principale, 60–100/min), atri (onda P), nodo atrioventricolare (ritardo che forma il segmento PR), fascio di His e branche, fibre di Purkinje e miocardio ventricolare (QRS). Accanto a ciascun livello è indicata la frequenza del pacemaker di riserva: più si scende, più il ritmo di scappamento è lento.
:::

Se il nodo del seno rallenta o tace, oppure se l'impulso viene bloccato lungo la via, il primo pacemaker di riserva che raggiunge la soglia prende il comando: è un **[battito di scappamento]{.ix}** (o un ritmo di scappamento, se continua). Lo scappamento è un meccanismo di protezione, non un'aritmia da sopprimere: dice che il comando superiore è venuto a mancare. Un QRS stretto indica uno scappamento giunzionale, che usa ancora il sistema di conduzione dei ventricoli; un QRS largo indica uno scappamento ventricolare, più lento e meno affidabile.

L'automatismo può anche diventare eccessivo. L'**automatismo aumentato** è quello di cellule che già lo possiedono e che accelerano per effetto delle catecolamine, della febbre o di farmaci simpaticomimetici. L'**automatismo anomalo** compare in cellule che normalmente non lo hanno, come i miociti ischemici o danneggiati, che a riposo sono meno negativi e possono scaricare spontaneamente: è uno dei meccanismi delle aritmie nella fase acuta dell'infarto e nel postoperatorio.

!!! errore "Errore classico – Sopprimere lo scappamento"
    Un ritmo lento a QRS largo, senza onde P, in un paziente con bradicardia sinusale o con blocco AV, non è una «tachicardia ventricolare lenta» da trattare con un antiaritmico: è spesso l'ultimo pacemaker che tiene in vita il paziente. Un farmaco che lo sopprime, come la lidocaina, può causare asistolia. Si chiama il medico e si prepara la stimolazione secondo protocollo.

### Conduzione

L'impulso passa da una cellula all'altra attraverso le **giunzioni comunicanti** (gap junction), canali che uniscono direttamente l'interno di cellule vicine. La velocità dipende dalla rapidità della fase 0, dal numero di giunzioni e dalla geometria delle fibre. Nell'adulto l'ordine di grandezza è di circa 1 m/s nel miocardio atriale (onda P), 0,02–0,05 m/s nel nodo AV (quasi tutto il segmento PR), 2–4 m/s nel sistema di His-Purkinje, che non ha un'onda propria, e 0,3–1 m/s nel miocardio ventricolare (QRS); sono valori indicativi dei testi di fisiologia. Il nodo AV, lento e calcio-dipendente, è l'unico passaggio elettrico normale tra atri e ventricoli e funziona da filtro: quando gli atri scaricano a 300–600/min, come nel flutter e nella fibrillazione atriale, il nodo ne lascia passare solo una parte e protegge i ventricoli.

### Il periodo refrattario

Dopo la fase 0 i canali del sodio restano inattivi finché la cellula non si è ripolarizzata a sufficienza. In questo intervallo la cellula non risponde: è il **[periodo refrattario]{.ix}** assoluto, che va dalla fase 0 fino a circa metà della fase 3 (−50/−60 mV). Segue il periodo refrattario **relativo**: alcuni canali sono di nuovo disponibili e uno stimolo più forte del normale produce un potenziale d'azione, ma con fase 0 più lenta e conduzione più lenta. Nel tessuto calcio-dipendente del nodo AV la refrattarietà dura più a lungo della ripolarizzazione: più gli impulsi sono ravvicinati, più il nodo li conduce lentamente. È la **conduzione decrementale**, alla base del filtro del nodo AV e del blocco di Wenckebach.

Il periodo refrattario protegge il cuore: impedisce che un muscolo si contragga in modo continuo (tetano) e che l'impulso torni indietro verso cellule appena attivate. Sull'ECG il periodo refrattario assoluto dei ventricoli corrisponde, in modo approssimativo, al tratto dal QRS fino al primo tratto dell'onda T; il periodo relativo alla parte discendente della T. Intorno all'apice della T, quando alcune cellule sono già eccitabili e altre no, si trova il **[periodo vulnerabile]{.ix}**: uno stimolo che cade lì, come un'extrasistole molto precoce (fenomeno **[R su T]{.ix}**) o uno shock non sincronizzato, può innescare una tachicardia o una fibrillazione ventricolare. Per questo la cardioversione elettrica si esegue in modalità **sincronizzata**, che rilascia lo shock sul QRS ed evita la T.

<!-- FIG-RICHIESTA: SCH-PA-ECG | Correlazione tra potenziale d'azione ventricolare ed ECG, con i periodi refrattari. Due pannelli allineati sullo stesso asse dei tempi (0–450 ms): in alto il potenziale d'azione ventricolare (−90 → +20 mV, fasi 0–4 numerate); in basso un battito ECG (P, QRS, ST, T). Linee verticali tratteggiate: fase 0 ↔ QRS; plateau (fase 2) ↔ tratto ST; fase 3 ↔ onda T; fine della fase 3 ↔ fine della T. Sotto, tre barre orizzontali: «periodo refrattario assoluto» (dal QRS al primo terzo della T), «periodo refrattario relativo» (parte discendente della T), «periodo vulnerabile» (fascia stretta intorno all'apice della T, campitura a tratteggio). Didascalia: «Ogni fase del potenziale d'azione ha la sua traccia sull'ECG; uno stimolo nel periodo vulnerabile può innescare aritmie ventricolari». -->

### Le tre vie delle aritmie

Ogni tachiaritmia nasce da uno di tre meccanismi, o dalla loro combinazione: **automatismo** alterato (descritto sopra), **attività triggerata** e **rientro**. Conoscere il meccanismo aiuta a capire perché un farmaco funziona in un'aritmia e ne peggiora un'altra.

#### Attività triggerata

Si parla di **[attività triggerata]{.ix}** («innescata») quando un potenziale d'azione genera, durante o subito dopo la ripolarizzazione, piccole oscillazioni del potenziale, le **post-depolarizzazioni**; se una di esse raggiunge la soglia, nasce un nuovo battito, che può a sua volta innescarne altri.

Le **post-depolarizzazioni precoci** (EAD, dall'inglese *early afterdepolarizations*) compaiono durante la fase 2 o 3, quando la ripolarizzazione è troppo lunga: i canali del calcio hanno il tempo di riaprirsi e la membrana risale prima di essere tornata a riposo. Le favorisce tutto ciò che allunga il QT: farmaci che bloccano hERG, ipopotassiemia, ipomagnesiemia, bradicardia e pause lunghe, sindromi del QT lungo congenito. L'aritmia tipica è la **[torsione di punta]{.ix}**, che spesso parte dopo una pausa (sequenza breve-lunga-breve) ed è illustrata nella Parte 4. Si spiega così perché la si tratta con il magnesio, accelerando la frequenza (stimolazione o, secondo protocollo, isoprenalina) e correggendo il potassio, e non con farmaci che allungano ancora il QT.

Le **post-depolarizzazioni tardive** (DAD, *delayed afterdepolarizations*) compaiono in fase 4, dopo la ripolarizzazione completa, quando la cellula è sovraccarica di calcio: il calcio liberato in modo disordinato dalle riserve interne attiva lo scambiatore sodio-calcio, che porta dentro cariche positive. Le favoriscono l'**intossicazione digitalica**, le catecolamine elevate, l'ischemia e la riperfusione. Sono il meccanismo di alcune extrasistoli ventricolari, dei ritmi giunzionali accelerati e della tachicardia ventricolare bidirezionale da digossina.

<!-- FIG-RICHIESTA: SCH-POSTDEP | Post-depolarizzazioni precoci e tardive. Due pannelli affiancati con potenziale d'azione ventricolare (asse mV −90/+30, asse ms). A sinistra «EAD»: potenziale d'azione con plateau allungato; sulla fase 2–3 una gobba verso l'alto (tratteggiata la versione sottosoglia, continua quella che raggiunge la soglia e genera un nuovo potenziale d'azione); etichette: «ripolarizzazione lunga: QT lungo, ipoK, ipoMg, bradicardia, farmaci che bloccano hERG». A destra «DAD»: potenziale d'azione normale; dopo il ritorno a −90 mV, in fase 4, una piccola oscillazione (tratteggiata sottosoglia, continua sopra soglia con nuovo battito); etichette: «sovraccarico di calcio: digossina, catecolamine, ischemia-riperfusione». Linea orizzontale tratteggiata della soglia in entrambi. -->

#### Rientro

Il **[rientro]{.ix}** è il meccanismo più frequente delle tachicardie regolari. Un impulso, invece di estinguersi dopo aver attivato il cuore, trova una via per tornare a eccitare il tessuto da cui è partito e continua a girare in un circuito. Perché ciò accada servono tre condizioni:

1. **due vie** che collegano due punti del cuore, con proprietà diverse (una conduce più in fretta ma ha un periodo refrattario lungo, l'altra conduce più lentamente ma recupera prima);
2. un **blocco unidirezionale**: un impulso precoce, di solito un'extrasistole, trova la via veloce ancora refrattaria e scende soltanto per quella lenta;
3. una **conduzione abbastanza lenta** da permettere alla via veloce di recuperare: quando l'impulso arriva in fondo alla via lenta, la via veloce è di nuovo eccitabile e l'impulso la risale all'indietro, chiudendo il cerchio.

<!-- FIG-RICHIESTA: SCH-RIENTRO | Circuito di rientro in tre riquadri numerati. Schema: un fascio che si divide in due vie parallele, «via A (rapida, refrattarietà lunga)» e «via B (lenta, refrattarietà breve)», che si riuniscono in un tessuto comune in basso. Riquadro 1, battito normale: l'impulso scende in entrambe le vie (frecce piene), i fronti si incontrano e si annullano in basso. Riquadro 2, extrasistole precoce: la via A è ancora refrattaria (barra di blocco ⊥ in nero), l'impulso scende solo nella via B (freccia piena). Riquadro 3, rientro: l'impulso arriva in fondo alla via B, trova la via A di nuovo eccitabile e la risale all'indietro (freccia tratteggiata), quindi rientra nella via B: circuito chiuso (freccia circolare). Didascalia: «Due vie, blocco unidirezionale, conduzione lenta». Solo bianco, nero e un grigio ≥ 10 %. -->

Il rientro spiega molte aritmie che si incontrano nelle Parti successive: la **tachicardia da rientro nodale**, in cui le due vie sono dentro il nodo AV; la **tachicardia da rientro atrioventricolare**, in cui una via è il nodo AV e l'altra una via accessoria (sindrome di Wolff-Parkinson-White); il **[flutter atriale]{.ix}** tipico, che gira intorno alla valvola tricuspide; la **tachicardia ventricolare** che gira intorno o attraverso una cicatrice di infarto. Si capisce anche come si interrompe un rientro: rendendo refrattario un tratto del circuito. Lo fanno l'adenosina e le manovre vagali sul nodo AV (per un istante il nodo non conduce), i farmaci di classe III che allungano il periodo refrattario, la cardioversione elettrica che depolarizza tutto il circuito insieme e l'ablazione transcatetere, che lo interrompe in modo definitivo.

I farmaci di classe I rallentano la conduzione; in un circuito di rientro questo può interrompere l'aritmia, ma può anche, al contrario, renderla più facile, perché una conduzione più lenta lascia più tempo alla via veloce per recuperare. È uno dei motivi per cui i bloccanti del sodio di classe Ic si evitano nei pazienti con cicatrice da infarto: lo studio CAST (*Cardiac Arrhythmia Suppression Trial*, *N Engl J Med* 1989 e 1991) mostrò un aumento della mortalità con flecainide ed encainide dopo infarto, nonostante la riduzione delle extrasistoli.

| Meccanismo | Che cosa succede | Esempi | Che cosa lo favorisce | Su che cosa agisce la terapia |
|---|---|---|---|---|
| Automatismo aumentato o anomalo | un focolaio scarica troppo spesso | tachicardia sinusale, tachicardia atriale focale, ritmo idioventricolare accelerato | catecolamine, febbre, ischemia | causa scatenante; beta-bloccanti |
| Attività triggerata (EAD) | oscillazioni durante una ripolarizzazione lunga | torsione di punta | QT lungo, ipoK, ipoMg, bradicardia, farmaci | magnesio, aumento della frequenza, sospensione dei farmaci |
| Attività triggerata (DAD) | oscillazioni dopo la ripolarizzazione, sovraccarico di Ca²⁺ | aritmie da digossina, alcune extrasistoli ventricolari | digossina, catecolamine, riperfusione | sospensione della digossina, correzione di K e Mg |
| Rientro | l'impulso gira in un circuito | tachicardie sopraventricolari da rientro, flutter, tachicardia ventricolare da cicatrice | due vie, blocco unidirezionale, conduzione lenta | adenosina, manovre vagali, classe III, cardioversione, ablazione |

!!! focus
    Dopo cardiochirurgia sono presenti contemporaneamente quasi tutti i fattori che favoriscono i tre meccanismi: catecolamine endogene ed esogene (inotropi), infiammazione e pericardite, ischemia e riperfusione dopo la cardioplegia, dilatazione degli atri, perdite di potassio e magnesio con i diuretici. Per questo gli obiettivi abituali del reparto (K ≥ 4,0 mmol/L e Mg ≥ 2,0 mg/dL) non sono un dettaglio di laboratorio ma una misura antiaritmica: riducono l'automatismo anomalo e le post-depolarizzazioni. Ogni nuova extrasistolia frequente nel postoperatorio si segnala insieme all'ultimo valore degli elettroliti.

!!! allarme "Extrasistoli ventricolari precoci con QT lungo"
    Un'extrasistole che cade sulla T (R su T), coppie o salve di battiti ventricolari, in un paziente con QTc > 500 ms, ipopotassiemia o ischemia, possono precedere una torsione di punta o una fibrillazione ventricolare. Monitor continuo con allarmi attivi, defibrillatore vicino e funzionante, accesso venoso pervio; avvisare subito il medico riferendo QTc, ultimi elettroliti e farmaci che allungano il QT; registrare un ECG a 12 derivazioni. Non spetta all'infermiere iniziare un antiaritmico senza prescrizione o protocollo.

## Come nasce l'ECG: dipolo, vettore e derivazioni

### Dal fronte d'onda al dipolo

A riposo la superficie esterna di ogni cellula è positiva. Quando un'area si depolarizza, la sua superficie esterna diventa negativa; tra la zona già attivata (negativa) e quella ancora a riposo (positiva) si forma un **[dipolo]{.ix}**, una coppia di cariche opposte che avanza insieme al fronte di attivazione. Un elettrodo posto sulla pelle «vede» questo dipolo e lo registra secondo una regola semplice, che vale per tutto l'ECG:

- se il fronte di depolarizzazione **si avvicina** all'elettrodo positivo, la deflessione è **positiva** (verso l'alto);
- se **si allontana**, la deflessione è **negativa** (verso il basso);
- se corre **perpendicolare** alla linea della derivazione, la deflessione è piccola o **isodifasica** (una parte positiva e una negativa di uguale ampiezza);
- quando nessun fronte è in movimento (cellule tutte a riposo o tutte attivate) il tracciato resta sulla **linea isoelettrica**.

<!-- FIG-RICHIESTA: SCH-DIPOLO | Fronte d'onda ed elettrodo: la regola della polarità. Una striscia rettangolare di tessuto (lunga, orizzontale) attivata da sinistra a destra: la parte già depolarizzata a sinistra con segni «−» sulla superficie, la parte a riposo a destra con segni «+»; una freccia spessa indica il verso del fronte. Tre elettrodi positivi (cerchi con «+») con il rispettivo tracciato accanto: elettrodo a destra (il fronte si avvicina) → deflessione positiva; elettrodo a sinistra (il fronte si allontana) → deflessione negativa; elettrodo sopra la metà della striscia (fronte perpendicolare) → deflessione isodifasica piccola. Didascalia: «Verso l'elettrodo positivo: onda positiva; via dall'elettrodo: negativa; perpendicolare: isodifasica». -->

La ripolarizzazione è il fenomeno opposto: un fronte di ripolarizzazione che si avvicina all'elettrodo produce una deflessione negativa. Nei ventricoli, però, la ripolarizzazione procede in senso contrario alla depolarizzazione: l'attivazione va dall'endocardio all'epicardio, mentre le cellule epicardiche, che hanno un potenziale d'azione più breve, si ripolarizzano per prime. Le due inversioni si annullano e il risultato è che, in un cuore normale, **l'onda T ha in genere lo stesso segno del QRS** nella stessa derivazione. Una T opposta al QRS in derivazioni in cui di solito è concorde è un segnale da interpretare (Parti 5 e 6).

### Il vettore cardiaco

In ogni istante milioni di cellule si attivano in direzioni diverse. La somma dei loro dipoli si rappresenta con un **[vettore]{.ix}**, una freccia che ha una direzione (dove va l'attivazione), un verso e una lunghezza proporzionale alla massa di tessuto coinvolta. Il vettore cambia istante per istante: prima va dagli atri verso il basso e a sinistra (onda P), poi attraversa il setto da sinistra a destra (prima piccola parte del QRS), quindi segue la massa del ventricolo sinistro verso sinistra, in basso e indietro (grande parte del QRS), infine si porta verso le regioni basali. La media di tutti i vettori del QRS è l'**[asse elettrico]{.ix}** del cuore, che nell'adulto normale si dirige in basso e a sinistra, tra −30° e +90° nel piano frontale. Poiché il ventricolo sinistro ha una massa molto maggiore del destro, l'attivazione del sinistro domina il tracciato: è il motivo per cui un'ipertrofia sinistra aumenta i voltaggi e un blocco di branca sinistra cambia tutta la forma del QRS.

Una derivazione è una linea immaginaria con un polo positivo e uno negativo. L'ampiezza dell'onda registrata dipende dall'angolo fra il vettore e la derivazione: è massima quando sono paralleli, nulla quando sono perpendicolari. Le derivazioni sono, in altre parole, **punti di vista diversi sullo stesso fenomeno**.

### Le derivazioni periferiche e il triangolo di Einthoven

L'ECG standard usa quattro elettrodi sugli arti: braccio destro (RA, *right arm*), braccio sinistro (LA), gamba sinistra (LL) e gamba destra (RL), che fa da elettrodo di riferimento (terra) e non entra nelle derivazioni. Con i primi tre si costruiscono sei derivazioni che esplorano il **[piano frontale]{.ix}**.

Le tre **derivazioni bipolari** di Einthoven misurano la differenza di potenziale fra due arti:

- **I**: braccio sinistro (+) rispetto al braccio destro (−); guarda il cuore da sinistra, a 0°;
- **II**: gamba sinistra (+) rispetto al braccio destro (−); guarda dal basso a sinistra, a +60°;
- **III**: gamba sinistra (+) rispetto al braccio sinistro (−); guarda dal basso a destra, a +120°.

Le tre derivazioni formano il **[triangolo di Einthoven]{.ix}**, con il cuore al centro ([[fig:SCH-EINTH]]). Poiché i tre lati sono collegati, in ogni istante vale la relazione **II = I + III** (legge di Einthoven): l'onda in II è la somma di quelle in I e in III. La regola serve anche come controllo di qualità: se non torna, gli elettrodi sono stati scambiati o uno di essi non fa contatto.

Le tre **derivazioni aumentate** (aVR, aVL, aVF, dette di Goldberger) confrontano un arto con la media degli altri due e guardano il cuore dal braccio destro (aVR, −150°), dal braccio sinistro (aVL, −30°) e dal basso (aVF, +90°). Sovrapponendo le sei derivazioni nel loro centro si ottiene il **[sistema esassiale]{.ix}**, una «rosa» di sei linee a 30° l'una dall'altra, che è lo strumento per calcolare l'asse elettrico (Parte 3).

Le derivazioni periferiche si raggruppano secondo la parete del cuore che guardano: **inferiori** II, III e aVF; **laterali alte** I e aVL. La derivazione **aVR** guarda il cuore dall'alto e da destra, cioè dalla parte opposta al vettore principale: in un ECG normale P, QRS e T sono negativi in aVR. Una aVR positiva in un adulto con ritmo sinusale fa sospettare per prima cosa un'inversione degli elettrodi delle braccia.

!!! errore "Errore classico – Elettrodi delle braccia invertiti"
    Se si scambiano l'elettrodo del braccio destro e quello del sinistro, la derivazione I si capovolge (P e QRS negativi), II e III si scambiano tra loro, aVR e aVL si scambiano: il tracciato simula un asse destro o una destrocardia. Prima di segnalare un «asse destro nuovo», si controllano la posizione degli elettrodi e le precordiali, che non cambiano. Gli errori di posizionamento sono trattati nella Parte 3.

::: fig SCH-EINTH
A sinistra il triangolo di Einthoven: i tre elettrodi degli arti (RA braccio destro, LA braccio sinistro, LL gamba sinistra) e le tre derivazioni bipolari con la loro polarità; al centro la legge II = I + III. A destra il sistema esassiale del piano frontale: ogni derivazione è disegnata con il suo angolo (I 0°, II +60°, aVF +90°, III +120°, aVL −30°, aVR −150°); in grigio l'intervallo dell'asse normale, da −30° a +90°.
:::

### Le derivazioni precordiali e il piano orizzontale

Le sei **[derivazioni precordiali]{.ix}** (V1–V6) sono unipolari: ciascuna confronta un elettrodo esplorante sul torace con un riferimento ottenuto collegando i tre elettrodi degli arti (terminale centrale di Wilson). Esplorano il **[piano orizzontale]{.ix}**, come se il torace fosse sezionato all'altezza del cuore e guardato dall'alto: V1 e V2 si trovano davanti al ventricolo destro e al setto, V3 e V4 davanti alla parete anteriore e alla punta, V5 e V6 sul lato sinistro, davanti alla parete laterale.

::: fig SCH-PRECORD
Posizione degli elettrodi precordiali. V1 e V2 al 4° spazio intercostale, rispettivamente a destra e a sinistra dello sterno; V4 al 5° spazio sulla linea emiclaveare sinistra; V3 a metà tra V2 e V4; V5 sull'ascellare anteriore e V6 sull'ascellare media, allo stesso livello orizzontale di V4. Lo spazio intercostale si conta partendo dall'angolo di Louis, dove si articola la 2ª costa.
:::

Nelle precordiali la depolarizzazione dei ventricoli produce una sequenza caratteristica, la **progressione dell'onda R**. In V1 il QRS è prevalentemente negativo (piccola r iniziale dovuta al setto, poi onda S profonda perché la massa del ventricolo sinistro si allontana); procedendo verso sinistra l'onda R cresce e l'onda S si riduce, fino a V5–V6, dove il QRS è prevalentemente positivo e preceduto da una piccola q settale. La derivazione in cui R ed S hanno ampiezza simile è la **zona di transizione**, di solito in V3 o V4.

<!-- FIG-RICHIESTA: SCH-PIANO-ORIZZ | Le derivazioni precordiali nel piano orizzontale. Sezione trasversale schematica del torace vista dall'alto (convenzione radiologica dichiarata in didascalia: paziente visto dai piedi, sinistra del paziente a destra della figura), con sterno in avanti, colonna dietro, ventricolo destro anteriore e ventricolo sinistro posteriore-sinistro. Sei frecce dal centro del cuore verso gli elettrodi V1–V6 disposti sul profilo anteriore-laterale sinistro del torace. Accanto a ogni elettrodo un QRS schematico che mostra la progressione: V1 rS, V2 rS, V3 RS, V4 Rs, V5 qR, V6 qR. Etichette dei gruppi: «settali V1–V2», «anteriori V3–V4», «laterali V5–V6». -->

| Gruppo | Derivazioni | Che cosa guardano |
|---|---|---|
| Inferiori | II, III, aVF | parete inferiore (diaframmatica) del ventricolo sinistro |
| Laterali alte | I, aVL | parete laterale alta |
| Settali | V1, V2 | setto interventricolare (e ventricolo destro) |
| Anteriori | V3, V4 | parete anteriore e punta |
| Laterali basse | V5, V6 | parete laterale |
| Opposta | aVR | cavità del cuore, dall'alto e da destra |

Per le pareti che le dodici derivazioni non vedono si aggiungono le **precordiali destre** (V3R, V4R, speculari a V3 e V4) e le **posteriori** V7–V9, sulla linea orizzontale di V6 verso la schiena (Parte 6).

::: fig REAL-PTBXL-NORM-03 variante=3x4
ECG a 12 derivazioni normale (tracciato reale, ritmo sinusale secondo la banca dati). Si osservino i complessi negativi in aVR; le derivazioni inferiori (II, III, aVF) e I con QRS positivo; il QRS prevalentemente negativo in V1–V2 e la R che cresce fino a diventare dominante in V4–V6; le T positive in I, II e V3–V6.
:::

!!! nota "Nota storica"
    La prima registrazione dell'attività elettrica del cuore umano dalla superficie del corpo si deve ad Augustus Waller (1887), con un elettrometro capillare. Willem Einthoven, con il galvanometro a corda messo a punto all'inizio del Novecento, ottenne tracciati di qualità clinica, introdusse le tre derivazioni bipolari e i nomi P, Q, R, S, T, ancora in uso; nel 1924 ricevette il premio Nobel per la medicina. Frank Wilson descrisse negli anni Trenta il terminale centrale che consente le derivazioni unipolari e precordiali, ed Emanuel Goldberger nel 1942 le derivazioni aumentate: da allora l'ECG standard ha dodici derivazioni.

## La carta ECG: velocità, ampiezza, calibrazione

### Quadretti piccoli e grandi

L'elettrocardiografo registra su una carta millimetrata, reale o disegnata sullo schermo, divisa in **quadretti piccoli** di 1 mm per lato, raggruppati in **quadretti grandi** di 5 mm, delimitati da una linea più spessa. In orizzontale si misura il tempo, in verticale il voltaggio. Lo standard internazionale prevede una velocità di **25 mm/s** e un guadagno di **10 mm/mV** (raccomandazioni AHA/ACC/HRS, parte I, 2007).

| Misura | Quadretto piccolo (1 mm) | Quadretto grande (5 mm) | Altri riferimenti |
|---|---|---|---|
| Tempo (orizzontale, 25 mm/s) | 0,04 s | 0,20 s | 5 quadretti grandi = 1 s; 30 quadretti grandi = 6 s |
| Ampiezza (verticale, 10 mm/mV) | 0,1 mV | 0,5 mV | 10 mm = 1 mV (rettangolo di calibrazione) |

Da queste equivalenze discendono i metodi rapidi per la frequenza: con un ritmo regolare si divide 300 per il numero di quadretti grandi tra due onde R, oppure 1500 per il numero di quadretti piccoli; con un ritmo irregolare si contano i QRS in 6 secondi e si moltiplica per 10. I metodi e i loro limiti sono descritti nella Parte 3.

<!-- FIG-RICHIESTA: SCH-CARTA | La carta ECG ingrandita. Un tratto di griglia di 4 × 3 quadretti grandi (20 × 15 mm) disegnata in scala 2:1, con quadretti piccoli in grigio chiaro (≥ 10 %) e linee dei quadretti grandi più spesse. Quote: in orizzontale «1 mm = 0,04 s» su un quadretto piccolo e «5 mm = 0,20 s» su un quadretto grande; in verticale «1 mm = 0,1 mV» e «5 mm = 0,5 mV». A sinistra un rettangolo di calibrazione alto 10 mm e largo 5 mm (0,20 s) con la quota «10 mm = 1 mV». Sotto, nota: «velocità 25 mm/s, guadagno 10 mm/mV». A destra, tre piccoli rettangoli di calibrazione affiancati con didascalia: «standard (10 mm)», «metà (5 mm/mV)», «doppio (20 mm/mV)». -->

### La calibrazione

All'inizio di ogni riga, o di ogni gruppo di derivazioni, l'apparecchio stampa l'**[impulso di calibrazione]{.ix}**: un rettangolo che corrisponde a 1 mV. Con il guadagno standard è alto 10 mm (due quadretti grandi). Se l'operatore o l'apparecchio hanno dimezzato il guadagno (5 mm/mV), per esempio per contenere QRS molto ampi, il rettangolo è alto 5 mm e tutte le ampiezze vanno raddoppiate; con guadagno doppio (20 mm/mV) il rettangolo è alto 20 mm e le ampiezze vanno dimezzate. Alcuni apparecchi usano guadagni diversi per periferiche e precordiali, e lo segnalano con un rettangolo «a gradino». Analogamente, se la velocità è stata portata a 50 mm/s, ogni quadretto piccolo vale 0,02 s: onde e intervalli appaiono larghi il doppio e la frequenza sembra la metà.

::: fig SIM-RS-02
Striscia del ritmo in derivazione II con carta standard. Il rettangolo di calibrazione all'inizio di ogni riga è alto 10 mm (1 mV). Si possono misurare: intervallo RR di circa 21 quadretti piccoli (0,83 s, frequenza ≈ 72/min); PR di 4 quadretti piccoli (0,16 s); QRS di poco più di 2 quadretti piccoli (< 0,12 s).
:::

!!! errore "Errore classico – Ampiezze lette senza guardare la calibrazione"
    Un QRS «basso» in un tracciato registrato a 5 mm/mV può far pensare a bassi voltaggi; un QRS «altissimo» a 20 mm/mV può far pensare a un'ipertrofia. Prima di commentare un'ampiezza si guarda il rettangolo di calibrazione; prima di commentare una durata si guarda la velocità stampata sul tracciato.

### I filtri: tracciato diagnostico e monitor

Il segnale del cuore è debole e si mescola a quello dei muscoli, della rete elettrica e del respiro; gli apparecchi lo ripuliscono con filtri. Per l'ECG diagnostico le raccomandazioni AHA del 2007 indicano un filtro passa-alto di 0,05 Hz (0,67 Hz con i filtri digitali a fase lineare) e un passa-basso di almeno 150 Hz nell'adulto: in questo modo il tratto ST e le onde rapide sono riprodotti fedelmente. In **modalità monitor** molti apparecchi usano filtri più stretti (per esempio 0,5–40 Hz) che rendono il tracciato più pulito ma possono **deformare il tratto ST**, creando o nascondendo sopra- e sottoslivellamenti. I tracciati reali di questo libro sono filtrati 0,5–40 Hz, come dichiarato in didascalia.

!!! chiave "Regola – Il monitor non sostituisce l'ECG a 12 derivazioni"
    Il monitor serve a sorvegliare il **ritmo**; l'analisi del tratto ST e delle ampiezze si fa sull'ECG a 12 derivazioni in modalità diagnostica. Se sul monitor compare un'alterazione del tratto ST, la si documenta con un ECG completo.

## Le onde e gli intervalli: che cosa rappresenta ciascuno

### Un battito, dall'inizio alla fine

Il battito cardiaco normale disegna sul tracciato una sequenza fissa. Le **onde** sono deflessioni dalla linea isoelettrica; i **segmenti** sono tratti di linea compresi fra due onde; gli **intervalli** comprendono almeno un'onda più un segmento. La linea isoelettrica di riferimento è il tratto TP (fra la fine della T e l'inizio della P successiva) o, quando la frequenza è alta e il tratto TP scompare, il segmento PR.

<!-- FIG-RICHIESTA: SCH-ONDE | Anatomia di un battito ECG. Un singolo battito ingrandito in derivazione II (scala 2:1, griglia leggera ≥ 10 %), con onda P, complesso QRS (q, R, s etichettate), segmento ST, onda T e piccola onda U. Graffe o quote orizzontali sotto il tracciato: «intervallo PR» (inizio P → inizio QRS), «segmento PR» (fine P → inizio QRS), «QRS», «segmento ST» (punto J → inizio T), «intervallo QT» (inizio QRS → fine T), «intervallo RR» verso il QRS successivo appena accennato. Punto J indicato con una freccia. Linea isoelettrica tratteggiata (tratto TP). Accanto a ogni elemento l'evento: «depolarizzazione atriale», «ritardo nel nodo AV», «depolarizzazione ventricolare», «plateau», «ripolarizzazione ventricolare». -->

### L'onda P

L'**[onda P]{.ix}** è la depolarizzazione degli atri. Inizia dalla parte alta dell'atrio destro, vicino al nodo del seno, e si estende all'atrio sinistro: la prima metà della P è soprattutto destra, la seconda soprattutto sinistra. Il vettore va in basso e a sinistra, per cui la P sinusale è **positiva in I, II e aVF e negativa in aVR**; in V1 può essere bifasica (prima positiva, poi negativa). Nell'adulto dura meno di 0,12 s ed è alta meno di 0,25 mV (2,5 mm) in II: oltre questi limiti si pensa a un ingrandimento atriale (Parte 5). La ripolarizzazione degli atri produce un'onda piccola e opposta alla P (onda Ta), di solito nascosta nel QRS.

Una P di forma diversa, negativa in II o assente indica che il ritmo non nasce dal nodo del seno: per esempio da un focolaio atriale basso o dalla giunzione, con una P retrograda che può comparire prima, dentro o dopo il QRS.

### L'intervallo PR

L'**[intervallo PR]{.ix}** va dall'inizio della P all'inizio del QRS (che sia una q o una R) e misura il tempo che l'impulso impiega a passare dagli atri ai ventricoli: depolarizzazione atriale, ritardo nel nodo AV, conduzione nel fascio di His e nelle branche. Il **segmento PR**, dalla fine della P all'inizio del QRS, corrisponde soprattutto al ritardo nel nodo AV. Il valore normale nell'adulto è **0,12–0,20 s** (3–5 quadretti piccoli); si accorcia un po' con la frequenza alta e si allunga con l'età.

Un PR **lungo** (> 0,20 s) indica una conduzione rallentata, quasi sempre nel nodo AV: tono vagale elevato, farmaci che agiscono sul nodo (beta-bloccanti, verapamil e diltiazem, digossina, amiodarone), malattia del sistema di conduzione, edema e manipolazione chirurgica dopo interventi sulle valvole. Un PR **corto** (< 0,12 s) indica che l'impulso arriva ai ventricoli scavalcando il ritardo nodale (via accessoria, come nella pre-eccitazione) o che il ritmo nasce vicino alla giunzione.

### Il complesso QRS

Il **[complesso QRS]{.ix}** è la depolarizzazione dei ventricoli. Per convenzione la prima onda negativa è la **q**, la prima onda positiva è la **R**, l'onda negativa che segue una R è la **S**; una seconda onda positiva si indica con **R'**. Le lettere maiuscole indicano le onde ampie, le minuscole quelle piccole; un complesso interamente negativo si chiama **QS**. La piccola q iniziale in I, aVL e V5–V6 (q settale) e la piccola r in V1 sono l'impronta dell'attivazione del setto da sinistra verso destra.

La **durata** del QRS si misura dall'inizio della prima onda alla fine dell'ultima, nella derivazione in cui è più largo. Nell'adulto è normalmente **inferiore a 0,12 s** (di solito 0,07–0,10 s). Secondo le raccomandazioni AHA/ACC/HRS del 2009, un QRS di 0,11–0,119 s indica un ritardo di conduzione incompleto o aspecifico, mentre un QRS **≥ 0,12 s** è compatibile con un blocco di branca completo o con un'attivazione che non usa il sistema di conduzione (battito ventricolare, stimolazione da pacemaker, pre-eccitazione) o con un rallentamento diffuso (iperpotassiemia, farmaci di classe I). L'**ampiezza** varia molto con l'età, la corporatura e la derivazione; i criteri di voltaggio per l'ipertrofia e per i bassi voltaggi sono nelle Parti 5 e 6.

### Il punto J e il segmento ST

Il **[punto J]{.ix}** è il punto in cui il QRS finisce e inizia il segmento ST. Il **[segmento ST]{.ix}** va dal punto J all'inizio dell'onda T e corrisponde al **plateau** (fase 2) del potenziale d'azione ventricolare: tutte le cellule ventricolari sono depolarizzate e non c'è differenza di potenziale importante fra loro, per cui il segmento è normalmente **isoelettrico**, cioè allo stesso livello del tratto TP o del segmento PR. Piccoli spostamenti possono essere normali, soprattutto in V2–V3 nei giovani maschi; i criteri di sopraslivellamento e sottoslivellamento significativi, che variano per età, sesso e derivazione secondo la quarta definizione universale di infarto (2018), sono nella Parte 6. Il livello del segmento ST si misura al punto J rispetto alla linea isoelettrica.

### L'onda T

L'**[onda T]{.ix}** è la ripolarizzazione dei ventricoli (fase 3). È più larga e più lenta del QRS, leggermente asimmetrica (sale più lentamente di quanto scenda) e, come si è visto, ha di solito lo stesso segno del QRS: **positiva in I, II e V3–V6, negativa in aVR**; può essere negativa o variabile in III, aVL e V1 senza significato patologico. È l'onda più sensibile del tracciato: cambia con l'ischemia, gli elettroliti, i farmaci, la frequenza, il tono autonomo e perfino la posizione del corpo; per questo una T alterata è un reperto aspecifico, da interpretare nel contesto clinico.

### L'onda U

L'**[onda U]{.ix}** è una piccola onda che a volte segue la T, con lo stesso segno, ed è più visibile in V2–V3 e a frequenza bassa. La sua origine è ancora discussa (ripolarizzazione tardiva di alcune cellule o effetti meccanici del rilasciamento ventricolare). Normalmente è molto più bassa della T. Una U **ampia**, che raggiunge o supera la T, fa pensare all'ipopotassiemia o a farmaci che allungano la ripolarizzazione; una U **negativa** in derivazioni in cui la T è positiva è rara e può accompagnare ischemia o ipertensione grave.

### L'intervallo QT e il QT corretto

L'**[intervallo QT]{.ix}** va dall'inizio del QRS alla fine dell'onda T e comprende l'intera attività elettrica dei ventricoli: depolarizzazione e ripolarizzazione. Corrisponde, in pratica, alla durata media del potenziale d'azione ventricolare. Si misura nella derivazione in cui è più lungo e la fine della T è ben visibile (spesso II o V5), **escludendo l'onda U** quando è separata dalla T. Il QT si accorcia quando la frequenza aumenta e si allunga quando diminuisce: per confrontare misure fatte a frequenze diverse si usa il **[QT corretto]{.ix}** (QTc), cioè il QT riportato a una frequenza di 60/min.

La formula più diffusa è quella di **Bazett**: QTc = QT / √RR, con QT e RR in secondi. È semplice ma sovrastima il QTc a frequenze alte e lo sottostima a frequenze basse. La formula di **Fridericia** (QTc = QT / ∛RR) è più affidabile in tachicardia e in bradicardia. Le raccomandazioni AHA/ACC/HRS del 2009 suggeriscono le formule lineari, meno dipendenti dalla frequenza, e ricordano che il QT si allunga anche quando il QRS è largo (blocchi di branca, stimolazione), per cui in questi casi il QT va interpretato con cautela. Nel reparto conta soprattutto che il QT di uno stesso paziente sia misurato sempre allo stesso modo, nella stessa derivazione e con la stessa formula.

| QTc | Significato | Fonte |
|---|---|---|
| ≥ 450 ms nell'uomo, ≥ 460 ms nella donna | prolungato | AHA/ACC/HRS 2009 (parte IV) |
| ≤ 390 ms | corto | AHA/ACC/HRS 2009 (parte IV) |
| > 500 ms, oppure aumento ≥ 60 ms rispetto al basale | rischio elevato di torsione di punta: si segnala subito | soglie di sorveglianza usate in tutto il libro |

*Per l'uomo il documento AHA/ACC/HRS usa sia «450 ms o più» sia «oltre 450 ms»: la differenza non ha peso pratico, purché il reparto adotti un'unica soglia.*

*Esempio svolto.* Frequenza 75/min: RR = 60/75 = 0,80 s. QT misurato 0,40 s (10 quadretti piccoli). Bazett: 0,40 / √0,80 = 0,40 / 0,894 ≈ **0,447 s** (447 ms). Fridericia: 0,40 / ∛0,80 = 0,40 / 0,928 ≈ **0,431 s**. Le due formule danno valori diversi: per questo si annota quale si è usata.

!!! allarme "QTc oltre 500 ms o aumentato di 60 ms"
    È la soglia oltre la quale il rischio di torsione di punta aumenta in modo netto. L'infermiere: ripete la misura su un ECG a 12 derivazioni; controlla e riferisce potassio, magnesio e calcio; verifica nella terapia i farmaci che allungano il QT (antiaritmici di classe III e Ia, macrolidi, fluorochinoloni, antipsicotici, ondansetron, metadone e altri); avvisa il medico **prima** della dose successiva di un farmaco che allunga il QT; mantiene il monitor continuo e il defibrillatore disponibile. La decisione di sospendere o modificare la terapia spetta al medico.

## Ripasso ed esercizi

### Schema riassuntivo: onda → evento → intervallo → valore normale

| Onda o tratto | Evento elettrico | Fase o sede | Ione e farmaci che la modificano | Intervallo di riferimento | Valore normale (adulto) |
|---|---|---|---|---|---|
| P | depolarizzazione degli atri | miocardio atriale | Na⁺ (classe I) | durata della P | < 0,12 s; < 0,25 mV in II |
| Segmento PR | ritardo nel nodo AV | nodo AV, His | Ca²⁺ (classe IV), beta (classe II), digossina, adenosina | PR | 0,12–0,20 s |
| QRS | depolarizzazione dei ventricoli | His-Purkinje, ventricoli (fase 0) | Na⁺ (classe I, soprattutto Ic); K⁺ alto | durata del QRS | < 0,12 s |
| Punto J e ST | plateau | ventricoli (fase 2) | Ca²⁺ (ipo- e ipercalcemia) | livello dell'ST al punto J | isoelettrico |
| T | ripolarizzazione dei ventricoli | ventricoli (fase 3) | K⁺ (classe III, farmaci anti-hERG, ipo- e iperpotassiemia) | QT / QTc | QTc < 450 ms (uomo), < 460 ms (donna) |
| U | ripolarizzazione tardiva (discussa) | ventricoli | K⁺ basso, farmaci | – | piccola, concorde con la T |
| RR | ciclo cardiaco (FC = 60 / RR in s) | nodo del seno (fase 4) | If (ivabradina), beta, Ca²⁺ | RR, FC | 60–100/min (RR 0,60–1,00 s) |

!!! chiave "Regola – Le misure da sapere a memoria"
    **25 mm/s**: 1 quadretto piccolo = 0,04 s, 1 grande = 0,20 s. **10 mm/mV**: 1 quadretto piccolo = 0,1 mV. **PR 0,12–0,20 s** (3–5 quadretti piccoli). **QRS < 0,12 s** (meno di 3 quadretti piccoli). **QTc**: prolungato da 450 ms (uomo) e 460 ms (donna); **> 500 ms o + 60 ms: si avvisa**.

!!! autotest "Autotest di fine Parte"
    **1.** Quale fase del potenziale d'azione ventricolare corrisponde al segmento ST e quale ione la sostiene?

    {{righe:2}}

    **2.** Un paziente in terapia con flecainide ha un QRS passato da 0,09 a 0,13 s. Quale canale è responsabile e perché il dato va segnalato?

    {{righe:2}}

    **3.** Nella derivazione II il QRS è positivo, in aVR è negativo. Che cosa dice questo sulla direzione del vettore?

    {{righe:2}}

    **4.** Un tracciato ha il rettangolo di calibrazione alto 5 mm. Un'onda R alta 12 mm quanti millivolt misura?

    {{righe:2}}

    **5.** Una paziente ha QT 0,44 s con RR 0,64 s (frequenza ≈ 94/min). Calcola il QTc con la formula di Bazett: è nei limiti? Che cosa fai?

    {{righe:2}}

### Esercizi ECG

Gli otto tracciati che seguono si leggono con gli strumenti di questa Parte: carta, derivazioni, onde e intervalli, meccanismi. Non è ancora richiesta una diagnosi completa del ritmo, che si imparerà nelle Parti 3 e 4. Le soluzioni sono in fondo alla Parte.

::: ecg-esercizio SIM-RS-03
Misura l'intervallo RR e calcola la frequenza con il metodo dei 1500. Ogni QRS è preceduto da una P? Quanto dura il PR? Il QT, rispetto all'RR, ti sembra corto o lungo, e che cosa serve per giudicarlo?
---
**Ritmo regolare a 125/min con onde P prima di ogni QRS.** RR di 12 quadretti piccoli (0,48 s): 1500/12 = 125/min. Ogni QRS è preceduto da una P positiva in II, molto vicina alla T precedente; PR costante di circa 0,14 s; QRS stretto. Il QT è più breve che a 72/min perché la ripolarizzazione si accorcia con la frequenza: per giudicarlo serve il QTc, meglio con Fridericia (Bazett lo sovrastima a frequenza alta). Il quadro è una tachicardia sinusale (Parte 4).
:::

::: ecg-esercizio SIM-LV-01 variante=3x4
Guarda il rettangolo di calibrazione: la taratura è standard? Poi misura l'ampiezza del QRS nelle derivazioni periferiche e nelle precordiali. Che cosa noti?
---
**Bassi voltaggi con calibrazione standard.** Il rettangolo di calibrazione è alto quanto due quadretti grandi della griglia, cioè 1 mV con guadagno standard (10 mm/mV): le ampiezze sono quindi reali e non dovute a una taratura dimezzata. Il QRS è inferiore a 0,5 mV (5 mm) in tutte le derivazioni periferiche e inferiore a 1 mV (10 mm) nelle precordiali. Le cause sono discusse nella Parte 6. La griglia è ridotta (vedi didascalia): le ampiezze si leggono contando i quadretti.
:::

::: ecg-esercizio SIM-RS-01 variante=3x4
Per le derivazioni I, II, aVR, V1 e V6 indica il segno (positivo o negativo) di P, QRS e T. Perché in aVR tutto è negativo? In quale precordiale avviene la transizione?
---
**ECG normale a 12 derivazioni.** In I e II: P, QRS e T positivi. In aVR: P, QRS e T negativi, perché il vettore medio, diretto in basso e a sinistra (circa +50°), si allontana dal braccio destro (aVR guarda da −150°, quasi esattamente dalla parte opposta). In V1: P piccola, QRS di tipo rS (piccola r settale e S profonda); in V6: QRS di tipo qR con q settale piccola e T positiva. La transizione avviene tra V3 e V4. ST isoelettrico ovunque.
:::

::: ecg-esercizio SIM-BAV-01
Misura il PR in più battiti. È costante? Ogni P è seguita da un QRS? In quale struttura si trova, con ogni probabilità, il ritardo, e quali farmaci possono causarlo?
---
**PR lungo e costante (0,30 s, 7–8 quadretti piccoli) con conduzione 1:1**: ogni P è seguita da un QRS stretto. È un blocco AV di 1° grado (Parte 5). Il ritardo si trova quasi sempre nel nodo AV, dove la conduzione dipende dai canali del calcio. Lo possono causare o accentuare beta-bloccanti, verapamil e diltiazem, digossina, amiodarone, il tono vagale e, dopo cardiochirurgia valvolare, l'edema vicino al sistema di conduzione. Si documenta il valore, lo si confronta con i tracciati precedenti e lo si segnala insieme alla terapia in corso.
:::

::: ecg-esercizio SIM-EL-05
Misura il QT e l'RR. Il QT è lungo? Quale parte del QT è allungata: il tratto ST o l'onda T? A quale fase del potenziale d'azione e a quale ione ti fa pensare?
---
**QT lungo per allungamento del tratto ST** (QTc ≈ 0,52 s): l'onda T ha forma e durata normali ma è «spinta» lontano dal QRS da un segmento ST lungo e piatto. Il segmento ST corrisponde al plateau (fase 2), sostenuto dal calcio: è il quadro tipico dell'ipocalcemia (Parte 9). Un QTc oltre 500 ms si segnala subito, con calcio ionizzato, magnesio, potassio e farmaci in corso.
:::

::: ecg-esercizio SIM-EL-03 variante=3x4
Osserva le derivazioni V2–V3. Che cosa segue l'onda T? Come misureresti il QT in questo tracciato? Quale elettrolita controlleresti?
---
**Onda U evidente**, più ampia della T in V2–V3, con T appiattite e lieve sottoslivellamento del tratto ST: il quadro tipico dell'ipopotassiemia. Il QT si misura fino alla fine della T, escludendo la U; se T e U si fondono, la misura comprende la U e sovrastima il QT: va annotato. Si controllano potassio e magnesio, che spesso si abbassano insieme.
:::

::: ecg-esercizio SIM-EX-09
Dove cade il battito anticipato a QRS largo rispetto alla T del battito precedente? Dopo questo battito compare un'onda P: perché non è seguita da un QRS? Confronta la pausa che segue con due intervalli RR normali.
---
**Extrasistole ventricolare con fenomeno R su T.** Il battito largo e bizzarro cade sull'apice della T del battito precedente, cioè nel periodo vulnerabile della ripolarizzazione: in un cuore ischemico, con QT lungo o elettroliti alterati, può innescare tachicardia o fibrillazione ventricolare. La P sinusale che segue arriva puntuale ma trova il nodo AV e i ventricoli ancora refrattari, per cui non viene condotta. La pausa è compensatoria piena: l'intervallo che comprende l'extrasistole è uguale a due RR sinusali, perché il nodo del seno non è stato disturbato.
:::

::: ecg-esercizio SIM-PAU-02
Il tracciato prosegue dalla prima alla seconda riga. Che cosa succede dopo il quarto battito? Da dove nasce il battito largo che interrompe la pausa e perché il suo QRS è largo?
---
**Pausa sinusale di circa 3 s interrotta da un battito di scappamento ventricolare**, poi ripresa del ritmo sinusale. Il nodo del seno tace e nemmeno la giunzione prende il comando; scarica allora un pacemaker ventricolare di riserva (20–40/min). Il QRS è largo perché l'impulso nasce nel ventricolo e si propaga da cellula a cellula senza usare il sistema di conduzione. Lo scappamento è un battito di salvataggio: non va soppresso con antiaritmici. Pause di questa durata si segnalano subito, con i sintomi del paziente (Parte 4).
:::

<!-- ABBR: ATP = adenosina trifosfato -->
<!-- ABBR: DAD = post-depolarizzazioni tardive (delayed afterdepolarizations) -->
<!-- ABBR: EAD = post-depolarizzazioni precoci (early afterdepolarizations) -->
<!-- ABBR: hERG = gene del canale del potassio della corrente IKr (human ether-à-go-go related gene) -->
<!-- ABBR: If = corrente «funny» delle cellule pacemaker -->
<!-- ABBR: IKr, IKs, IK1, Ito = correnti del potassio (rapida, lenta, rettificatrice entrante, transitoria in uscita) -->
<!-- ABBR: LA, LL, RA, RL = elettrodi di braccio sinistro, gamba sinistra, braccio destro, gamba destra -->
<!-- ABBR: QTc = QT corretto per la frequenza -->
