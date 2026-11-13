#!/usr/bin/env python3
"""Inserisce sezioni aggiuntive alla fine dei capitoli indicati (una tantum, idempotente tramite marcatore)."""
import re, sys
from pathlib import Path
VOL = Path(__file__).resolve().parent.parent / "volumi" / "01-betabloccanti"

ADD = {}

# ------------------------------------------------------------------ PARTE I
ADD[("parte-01.md", "Introduzione ai betabloccanti")] = """
### Una breve cronologia

| Periodo | Tappa | Significato |
|---|---|---|
| 1948 | Raymond Ahlquist distingue recettori α e β | Base concettuale dell'intera classe |
| Fine anni '50 – anni '60 | Prime molecole (dicloroisoprenalina, pronetalolo), poi propranololo con James Black | Nasce la terapia antianginosa a base di blocco β |
| Anni '70 – '80 | Molecole β1-selettive (atenololo, metoprololo); studi post-infarto come BHAT | Estensione alla prevenzione secondaria |
| 1999 – 2005 | CIBIS-II, MERIT-HF, COPERNICUS, SENIORS | I betabloccanti diventano pilastro dello scompenso |
| 2002 – 2008 | LIFE, ASCOT, POISE | Ridimensionati nell'ipertensione e nella chirurgia non cardiaca |
| 2024 – 2025 | REDUCE-AMI, ABYSS, REBOOT | Riesame del ruolo dopo infarto con funzione conservata |

### Come leggere questo manuale

Ogni Parte risponde a una domanda: che cosa fa il sistema adrenergico (I), come agisce il farmaco (II), quali molecole esistono (III), per quali malattie si usa (IV), che cosa cambia in urgenza (V), quali sono i rischi (VI), che cosa fa l'infermiere (VII), come cambia nelle popolazioni speciali (VIII), che cosa fare in caso di eccesso (IX). Le ultime due Parti consolidano, con casi e strumenti pratici. La stessa architettura sarà riproposta nei volumi dedicati alle altre classi di farmaci cardiovascolari, così da rendere comparabili le classi.
"""

ADD[("parte-01.md", "Il sistema nervoso autonomo")] = """
### Il riflesso barocettivo

La pressione arteriosa è regolata minuto per minuto dal **riflesso barocettivo**. I barocettori dei seni carotidei e dell'arco aortico inviano al tronco encefalico, tramite i nervi glossofaringeo e vago, un segnale proporzionale allo stiramento parietale. Se la pressione scende, ad esempio nell'alzarsi in piedi, il tono vagale si riduce e quello simpatico aumenta: frequenza e resistenze crescono e la pressione viene ripristinata. Un betabloccante attenua la parte cardiaca di questa risposta; per questo l'**ipotensione ortostatica** e la ridotta tolleranza a ipovolemia, sepsi e disidratazione sono rischi prevedibili.

### Risposta di allarme e di riposo

L'attivazione simpatica generalizzata («combatti o fuggi») comprende tachicardia, aumento della contrattilità, vasocostrizione splancnica e cutanea, vasodilatazione muscolare, broncodilatazione, glicogenolisi e lipolisi. Il parasimpatico prevale a riposo e nel sonno. Capire che i due sistemi agiscono su organi diversi con segno opposto aiuta a prevedere gli effetti collaterali: ciò che il betabloccante toglie al simpatico lo restituisce, in apparenza, al parasimpatico.

!!! chiave "Punti chiave"
    - Il riflesso barocettivo è il meccanismo che compensa l'ortostatismo e la perdita di volume.
    - Il blocco β ne riduce la componente cardiaca: ipotensione e sincope sono rischi da ricordare.
"""

ADD[("parte-01.md", "Le catecolamine")] = """
### Catecolamine e farmaci vasoattivi: confronto dei profili recettoriali

La conoscenza dei profili recettoriali è utile per comprendere sia le urgenze sia la tossicologia dei betabloccanti.

| Sostanza | Recettori principali | Effetto emodinamico prevalente | Uso tipico |
|---|---|---|---|
| Adrenalina | α1, β1, β2 | Aumento di gittata e pressione; broncodilatazione | Anafilassi, arresto cardiaco |
| Noradrenalina | α1, β1 (β2 minimo) | Vasocostrizione e pressione | Shock vasoplegico |
| Dopamina | D1, β1, α1 (secondo la dose) | Dipende dalla dose | Impiego ridotto |
| Dobutamina | β1 > β2, modesto α1 | Aumento di contrattilità | Scompenso con basso output |
| Isoprenalina | β1, β2 | Aumento di frequenza e contrattilità; vasodilatazione | Bradicardia refrattaria in contesti selezionati |

### Perché interessa il farmaco

Poiché il blocco competitivo è superabile, dosi elevate di agonisti β possono ripristinare in parte l'effetto in caso di eccesso di betabloccante. Allo stesso tempo, un paziente in terapia può rispondere meno alla dobutamina o all'adrenalina: ne derivano le scelte di antidoti e supporti descritte nella Parte IX.
"""

ADD[("parte-01.md", "I recettori adrenergici")] = """
### Agonisti, antagonisti e agonisti inversi

Un recettore può avere un'attività basale anche in assenza di ligando. Un **agonista** la aumenta, un **antagonista neutro** si limita a occupare il sito, un **agonista inverso** la riduce. Molti betabloccanti si comportano in parte come agonisti inversi, e ciò potrebbe contribuire alla riduzione del rilascio basale di renina e dell'attività cardiaca a riposo. Alcune molecole hanno attività simpaticomimetica intrinseca (ISA), cioè sono agonisti parziali: bloccano gli stimoli forti ma attivano debolmente il recettore, con minore bradicardia a riposo.

### Segnalazione «biased»

Il recettore può attivare, oltre alla via Gs-cAMP, anche vie dipendenti dalla β-arrestina. Per alcune molecole, tra cui il carvedilolo, è stata proposta una modulazione preferenziale di queste vie come possibile contributo ai loro effetti; si tratta di un campo di ricerca e non di un criterio di scelta clinica.

!!! nota "Nota – Selettività e recettori extracardiaci"
    Il cuore umano contiene anche recettori β2 e, in misura minore, β3. Per questo i betabloccanti β1-selettivi non sono «cardiospecifici»: il termine corretto è «cardioselettivi», a indicare una preferenza relativa.
"""

ADD[("parte-01.md", "Fisiologia cardiaca essenziale")] = """
### Frequenza e diastole: un esempio numerico

A 60 bpm il ciclo dura 1000 ms, di cui circa 350 di sistole e 650 di diastole. A 120 bpm il ciclo dura 500 ms: la sistole si accorcia solo in parte (circa 280 ms) e la diastole si riduce a circa 220 ms, cioè di quasi due terzi. Poiché la perfusione coronarica del ventricolo sinistro è soprattutto diastolica, la tachicardia peggiora l'ischemia in due modi: aumenta la richiesta e riduce il tempo di irrorazione. I valori sono approssimativi e dipendono dall'individuo, ma illustrano perché rallentare il cuore è antianginoso.

### La relazione pressione-volume

Il lavoro del ventricolo sinistro si rappresenta con il ciclo pressione-volume. L'aumento di postcarico sposta il ciclo verso pressioni maggiori e riduce la gittata; l'aumento di contrattilità aumenta la pendenza della relazione telesistolica. Un betabloccante riduce la contrattilità: nel cuore sano la riserva compensa, nel cuore con funzione ridotta il margine è limitato e l'avvio richiede titolazione graduale.

!!! nota "Nota – Frequenza cardiaca come bersaglio"
    Nello scompenso cronico con ritmo sinusale, il ruolo della frequenza come fattore prognostico è documentato: è stato osservato che il beneficio dei betabloccanti si associa, in parte, alla riduzione della frequenza. Nella fibrillazione atriale questo legame è meno evidente (si veda il Capitolo 24).
"""

# ------------------------------------------------------------------ PARTE II
ADD[("parte-02.md", "Meccanismo d'azione")] = """
### Blocco competitivo e superamento con gli agonisti

Poiché l'antagonismo è competitivo e reversibile, un aumento sufficiente della concentrazione di agonista può spostare l'equilibrio: l'effetto del betabloccante è «superabile». Questo principio ha due applicazioni opposte. In **tossicologia**, dosi elevate di agonisti β o di glucagone aggirano il blocco (Parte IX). In **clinica**, un paziente in terapia può non rispondere a dosi usuali di salbutamolo o adrenalina e richiedere dosi maggiori.

### Effetti metabolici e sul sistema renina-angiotensina

Il blocco dei recettori β1 nell'apparato iuxtaglomerulare riduce la renina e quindi l'angiotensina II e l'aldosterone: un contributo all'effetto antipertensivo e alla protezione dal rimodellamento. Il blocco dei β2 epatici e muscolari riduce glicogenolisi e gluconeogenesi, e il blocco dei β3 nel tessuto adiposo riduce la lipolisi; da qui il lieve aumento di peso osservato con alcune molecole.
"""

ADD[("parte-02.md", "Classificazione dei betabloccanti")] = """
### Scegliere in base al paziente: una griglia pratica

| Situazione | Caratteristica favorevole | Molecole da considerare |
|---|---|---|
| Scompenso con FE ridotta | Evidenza di mortalità | Bisoprololo, carvedilolo, metoprololo succinato, nebivololo |
| Anziano fragile | Dosi basse, buona tollerabilità | Bisoprololo, nebivololo |
| Insufficienza renale | Eliminazione epatica o mista | Metoprololo, carvedilolo, bisoprololo (dose ridotta) |
| Epatopatia | Eliminazione renale o dosi ridotte | Bisoprololo, atenololo (con cautela) |
| Gravidanza | Dati di sicurezza | Labetalolo, metoprololo |
| BPCO con indicazione cardiologica | β1-selettività | Bisoprololo, nebivololo, metoprololo succinato |
| Ipertensione con tachicardia e tremore | Lipofilia, blocco non selettivo | Propranololo (casi selezionati) |
| Urgenza con instabilità potenziale | Brevissima emivita | Esmololo, landiololo |

!!! nota "Nota – Una classificazione utile ma imperfetta"
    Le generazioni sono una convenzione didattica: il sotalolo, ad esempio, è «di prima generazione» per il blocco β ma appartiene alla classe III per l'azione sul potassio, e il carvedilolo è «di terza generazione» ma non è selettivo. In pratica conta il profilo di ogni molecola, non l'etichetta.
"""

ADD[("parte-02.md", "Farmacodinamica clinica")] = """
### Misurare l'effetto: dall'ECG alla prova da sforzo

L'effetto di un betabloccante si osserva nella **riduzione della frequenza di riposo** e, soprattutto, nell'**attenuazione della risposta allo sforzo**: la frequenza massima raggiunta è più bassa e il prodotto frequenza-pressione sotto lo stesso carico si riduce. L'allungamento dell'intervallo PR è un segno di rallentamento della conduzione AV; un PR superiore a 200–240 ms impone attenzione. Nell'angina si valuta anche la soglia ischemica alla prova da sforzo, che con un betabloccante si sposta verso un carico maggiore.

### Variabilità interindividuale

La risposta varia con il tono simpatico di base, l'età, la funzione d'organo, il polimorfismo del CYP2D6, le interazioni, l'aderenza e la dose assunta. La stessa dose può produrre bradicardia in un paziente e solo una lieve riduzione in un altro: per questo la titolazione è individuale e si basa su parametri clinici anziché su una dose standard.

!!! chiave "Punti chiave"
    - Gli indicatori di risposta sono frequenza a riposo, risposta allo sforzo, PR e sintomi.
    - La titolazione si fa sul paziente, non sulla tabella.
"""

ADD[("parte-02.md", "Farmacocinetica")] = """
### Farmacogenetica del CYP2D6

L'enzima CYP2D6 presenta un marcato polimorfismo: una quota della popolazione europea, indicativamente tra il 5% e il 10%, è costituita da **metabolizzatori lenti**, nei quali farmaci come metoprololo, carvedilolo e nebivololo raggiungono concentrazioni più alte; all'estremo opposto vi sono i metabolizzatori ultra-rapidi, con livelli più bassi. Nella pratica la genotipizzazione non è di routine: si osserva la **risposta clinica** (frequenza, pressione, sintomi) e si presta attenzione a farmaci che inibiscono l'enzima, come fluoxetina, paroxetina, bupropione e chinidina.

### Formulazioni a rilascio immediato e prolungato

Le formulazioni a rilascio prolungato riducono i picchi plasmatici e migliorano l'aderenza con monosomministrazione. La differenza non è solo di comodità: nello scompenso l'evidenza di mortalità riguarda il **succinato**, non il tartrato. Compresse a rilascio modificato non vanno frantumate; se prevista, la divisione segue la linea di frattura.

### Funzione d'organo e accumulo

In caso di insufficienza renale i farmaci idrofili si accumulano; nell'epatopatia aumenta la biodisponibilità di quelli ad elevato metabolismo di primo passaggio (propranololo, labetalolo, metoprololo, carvedilolo). Con età avanzata e bassa massa muscolare, il rischio di sovraesposizione cresce anche con funzione renale apparentemente normale perché la creatinina sottostima il deficit.

!!! nota "Nota – Quanto tempo ci vuole per lo stato stazionario"
    Una regola didattica: lo stato stazionario si raggiunge in circa 4–5 emivite. Con emivita di 12 ore, come per bisoprololo, si arriva in 2–3 giorni; con eliminazione renale ridotta i tempi si allungano. È uno dei motivi per cui la titolazione si fa a intervalli di giorni o settimane e non di ore.
"""

# ------------------------------------------------------------------ PARTE III
ADD[("parte-03.md", "Metoprololo")] = """
### Posizione rispetto alle altre molecole

Il metoprololo è la molecola più versatile del gruppo: dispone di formulazione endovenosa, orale a rilascio immediato e prolungato, ha prove di mortalità nello scompenso (succinato) e dati dopo infarto. Limiti sono la variabilità farmacocinetica da CYP2D6 e la lipofilia. Nella pratica, la scelta tra tartrato e succinato non è una questione di preferenza, ma di indicazione e di formulazione disponibile.
"""
ADD[("parte-03.md", "Bisoprololo")] = """
### Confronto pratico

Rispetto al metoprololo, il bisoprololo offre una cinetica più prevedibile e minore dipendenza dal CYP2D6; rispetto al carvedilolo ha meno effetti vasodilatatori e minore rischio di ipotensione ortostatica, ma non ha l'effetto antiossidante e α-bloccante. Nei pazienti con BPCO è tra le scelte più usate per la maggiore selettività.

!!! nota "Nota – Titolazione nell'ambulatorio dello scompenso"
    Nei programmi strutturati l'intervallo tra i rialzi di dose è spesso di due settimane o più, con controllo clinico prima di ogni aumento. L'obiettivo non è raggiungere la dose massima a ogni costo, ma la dose più alta tollerata dal singolo paziente.
"""
ADD[("parte-03.md", "Carvedilolo")] = """
### Quando preferirlo

Il carvedilolo è attraente quando coesistono scompenso e ipertensione, per l'effetto vasodilatatore. È meno adatto nel paziente con ipotensione basale, ortostatismo marcato, asma o BPCO significativa. Nel cirrotico con varici è un'opzione per la riduzione della pressione portale. Ricordare che la sospensione va graduale e che la dose target è più alta nei pazienti di peso maggiore.

### Educazione

Il paziente va avvisato che le vertigini all'avvio sono frequenti e di solito transitorie; assumere il farmaco con il cibo e alzarsi lentamente riduce il problema.
"""
ADD[("parte-03.md", "Nebivololo")] = """
### Posizione nella pratica

Il nebivololo è una scelta ragionevole in pazienti ipertesi anziani, con diabete o disfunzione erettile preoccupanti, o con scompenso a partire dai 70 anni. Nei metabolizzatori lenti del CYP2D6 l'emivita è molto più lunga: il rischio di bradicardia è maggiore. Alcune formulazioni associano il nebivololo a un diuretico o a un inibitore del sistema renina-angiotensina in compressa unica, utile per l'aderenza.
"""
ADD[("parte-03.md", "Atenololo")] = """
### Un caso di deprescrizione ragionata

In un paziente iperteso in terapia da anni con atenololo senza altre indicazioni, un'opzione di gestione è la sostituzione con una classe di prima linea, con riduzione graduale per prevenire il rebound. Se coesistono angina o aritmie, si può passare a una molecola β1-selettiva con migliori prove (per esempio bisoprololo o nebivololo), valutando funzione renale e frequenza.
"""
ADD[("parte-03.md", "Propranololo")] = """
### Confronto con le molecole cardioselettive

Il blocco β2 rende il propranololo meno adatto a pazienti con asma, BPCO, diabete con ipoglicemie e arteriopatia periferica; la lipofilia comporta effetti centrali. Resta insostituibile dove serve un'azione non selettiva (ipertensione portale, tireotossicosi, tremore, emangioma infantile, alcune canalopatie).

!!! nota "Nota – Propranololo e performance"
    La riduzione del tremore e dell'ansia somatica spiega l'uso improprio del propranololo in ambito sportivo e di performance: per alcune discipline è sostanza proibita in competizione. È un esempio di come una molecola «datata» abbia effetti non cardiaci di grande rilevanza.
"""
ADD[("parte-03.md", "Esmololo")] = """
### Confronto con landiololo e metoprololo EV

Il landiololo ha emivita ancora più breve e selettività maggiore; il metoprololo endovenoso ha durata più lunga e minore titolabilità. L'esmololo si colloca in una posizione intermedia, con ampia disponibilità e lunga esperienza. In situazioni di instabilità potenziale, la brevità d'azione è una garanzia di sicurezza: se compare ipotensione, la riduzione o l'interruzione dell'infusione ne determina la risoluzione nell'arco di pochi minuti.
"""
ADD[("parte-03.md", "Labetalolo")] = """
### Scelte in ostetricia

Nelle emergenze ipertensive in gravidanza il labetalolo è considerato un farmaco di prima linea insieme a nifedipina a rilascio immediato e idralazina; le scelte e le dosi sono stabilite dai protocolli ostetrici locali. Il bambino esposto nelle ultime ore di gravidanza va monitorato per bradicardia e ipoglicemia.
"""
ADD[("parte-03.md", "Altri betabloccanti")] = """
### Come orientarsi

Le molecole di questa sezione hanno un valore soprattutto storico o di nicchia. Possono presentarsi nell'anamnesi del paziente (ad esempio nadololo per canalopatie, timololo per glaucoma) e vanno riconosciute come betabloccanti a tutti gli effetti, con le stesse precauzioni e interazioni delle altre molecole.
"""
ADD[("parte-03.md", "Sotalolo")] = """
### Protocollo infermieristico di inizio terapia

All'avvio in ambiente monitorato: ECG basale con misura del QTc; potassio e magnesio nel range; creatinina; frequenza e pressione; registrazione ECG dopo ogni dose o secondo protocollo, con sospensione e allerta se il QTc supera le soglie indicate dal prescrittore o compaiono extrasistoli ventricolari ravvicinate. Preparare defibrillatore e magnesio solfato.
"""

# ------------------------------------------------------------------ PARTE IV
ADD[("parte-04.md", "Ipertensione arteriosa")] = """
### Quando il betabloccante è ragionevole: fenotipi

| Fenotipo | Perché |
|---|---|
| Ipertensione con angina | Doppio beneficio: pressione e sintomi |
| Ipertensione dopo infarto con FE ridotta | Indicazione prognostica |
| Ipertensione con scompenso a FE ridotta | Pilastro del trattamento |
| Ipertensione con FA e frequenza elevata | Controllo della frequenza |
| Gravidanza o programmazione di gravidanza | Labetalolo, metoprololo |
| Sindromi aortiche (Marfan) | Riduzione dello stress parietale |

### Scelta della molecola

Quando si decide di usare un betabloccante nell'ipertensione, le linee guida e i pareri di esperti convergono verso molecole con profilo vasodilatatore o β1-selettivo (nebivololo, bisoprololo, carvedilolo) rispetto all'atenololo. Le dosi tipiche sono basse e l'effetto massimo si ottiene entro 2–4 settimane.
"""
ADD[("parte-04.md", "Angina e sindromi coronariche croniche")] = """
### Esempio di scelta terapeutica

Un uomo di 62 anni con angina da sforzo stabile, frequenza di 82 bpm e pressione 138/82 mmHg: un betabloccante cardioselettivo a basse dosi riduce angina e frequenza; se persiste, si aggiunge amlodipina (diidropiridinico). Evitare l'aggiunta di verapamil o diltiazem. Se c'è bradicardia a 52 bpm con angina residua, la strategia può passare ad altre classi anti-anginose (ivabradina, ranolazina, nitrati a lunga durata) secondo le indicazioni.

!!! nota "Nota – Beta-blocker e prognosi nelle CCS"
    A differenza dello scompenso, nelle sindromi coronariche croniche senza infarto recente né disfunzione ventricolare l'evidenza è di riduzione dei sintomi, non di riduzione della mortalità. Il razionale della terapia è dunque soprattutto sintomatico.
"""
ADD[("parte-04.md", "Infarto miocardico acuto")] = """
### Tre epoche della terapia betabloccante

| Epoca | Contesto | Messaggio dominante |
|---|---|---|
| Prima della riperfusione (anni '70–'80) | Infarto non riperfuso | Riduzione di mortalità e reinfarto (BHAT, ISIS-1) |
| Era della riperfusione (anni '90–2000) | Angioplastica, trombolisi, antiaggreganti | Dubbio sul beneficio; rischio di shock con EV precoce (COMMIT) |
| Era contemporanea (dal 2024) | Riperfusione, statine, ACE-inibitori, antiaggreganti | Nessun beneficio chiaro con FE conservata (REDUCE-AMI, REBOOT) |

### Come orientarsi nella pratica

Il betabloccante post-infarto è raccomandato con FE ridotta, aritmie ventricolari, angina residua o ipertensione; in assenza di queste condizioni la durata e l'indicazione vanno discusse. La durata ottimale della terapia in assenza di disfunzione ventricolare non è definita.
"""
ADD[("parte-04.md", "Scompenso cardiaco")] = """
### Dosi target dagli studi

| Molecola | Dose target (didattica) | Studio |
|---|---|---|
| Bisoprololo | 10 mg/die | CIBIS-II |
| Metoprololo succinato | 200 mg/die | MERIT-HF |
| Carvedilolo | 25 mg × 2 (50 mg × 2 se peso > 85 kg) | US Carvedilol, COPERNICUS |
| Nebivololo | 10 mg/die | SENIORS |

### Intolleranza e sospensione

L'intolleranza è meno frequente di quanto temuto se si procede gradualmente: la maggior parte dei pazienti raggiunge dosi significative. In caso di ipotensione si rivede la terapia concomitante (diuretici, vasodilatatori), si spostano gli orari di somministrazione; in caso di bradicardia si valuta con ECG e si sospendono farmaci inutili che rallentano il cuore; si considera un pacemaker se necessario per proseguire la terapia.

### Scompenso acuto in paziente già in terapia

Nello scompenso acuto, i pazienti che già assumono betabloccanti dovrebbero in genere **proseguirli**, riducendo la dose in caso di ipoperfusione o bradicardia, e sospenderli solo in presenza di shock o ipotensione grave. L'interruzione sistematica è associata a peggiori esiti.
"""
ADD[("parte-04.md", "Fibrillazione atriale")] = """
### Come si sceglie il farmaco di controllo della frequenza

| Contesto | Scelta tipica |
|---|---|
| FE > 40%, nessuna BPCO grave | Betabloccante o diltiazem/verapamil |
| FE ≤ 40% | Betabloccante, digossina o combinazione |
| BPCO | Betabloccante β1-selettivo o calcio-antagonista |
| Ipertiroidismo | Propranololo |
| Instabilità, scompenso acuto | Amiodarone, cardioversione |
| Fibrillazione post-operatoria | Betabloccante, secondo condizioni |

L'intero percorso AF-CARE comprende, oltre al controllo di frequenza o ritmo, la gestione delle comorbilità, l'anticoagulazione secondo il rischio e la rivalutazione periodica.
"""
ADD[("parte-04.md", "Altre aritmie")] = """
### Quadro riassuntivo

| Aritmia o condizione | Ruolo del betabloccante |
|---|---|
| Tachicardia sinusale inappropriata | Prima scelta farmacologica |
| TSV da rientro (AVNRT/AVRT) | Opzione dopo manovre vagali e adenosina |
| Extrasistoli ventricolari sintomatiche | Prima linea farmacologica |
| QT lungo (LQT1, LQT2) | Nadololo, propranololo |
| CPVT | Nadololo, propranololo (± flecainide) |
| Cardiopatia ischemica con TV | Prevenzione con betabloccante |
| Tempesta aritmica | Betabloccante con sedazione |
| Cardiomiopatia ipertrofica ostruttiva | Prima linea per sintomi |

!!! nota "Nota – Brugada e betabloccanti"
    Nella sindrome di Brugada i betabloccanti non sono raccomandati e vanno usati con cautela, perché possono interferire con il quadro elettrico: la presenza di una canalopatia va sempre segnalata prima di iniziare la terapia.
"""

# ------------------------------------------------------------------ PARTE V
ADD[("parte-05.md", "Il betabloccante in pronto soccorso")] = """
### Tachicardie da non rallentare

| Causa della tachicardia | Perché non rallentare | Azione prioritaria |
|---|---|---|
| Emorragia, ipovolemia | Compenso della gittata | Volume, controllo del sanguinamento |
| Sepsi | Compenso emodinamico | Antibiotici, fluidi, source control |
| Embolia polmonare massiva | Compenso del ventricolo destro | Reperfusione |
| Anemia severa | Compenso del trasporto di O2 | Trasfusione |
| Ipossia | Risposta fisiologica | Ossigeno, ventilazione |
| Dolore, febbre, ansia | Risposta fisiologica | Trattare la causa |
| Tireotossicosi, feocromocitoma | Causa specifica | Approccio dedicato |

### Il ruolo del triage

Al triage l'infermiere può riconoscere i segnali d'allarme per i quali una frequenza elevata non va trattata ma segnalata: ipotensione, alterazione dello stato di coscienza, pallore e sudorazione, dispnea, dolore toracico. Un ECG precoce e una scala di early warning (NEWS2) orientano l'urgenza.
"""
ADD[("parte-05.md", "Somministrazione endovenosa")] = """
### Preparazione e compatibilità

- Esmololo: siringhe o flaconi pronti all'uso; verificare concentrazione e velocità; non miscelare con soluzioni di bicarbonato.
- Metoprololo: soluzione pronta, non diluire a meno che previsto; somministrare lentamente.
- Labetalolo: possibile diluizione secondo scheda; evitare compatibilità con soluzioni alcaline.
- Landiololo: ricostituzione e diluizione secondo RCP; infusione con pompa.

### Una sequenza di sicurezza

1. Verificare indicazione e controindicazioni; eseguire ECG.
2. Posizionare monitor; accesso venoso sicuro.
3. Registrare i valori basali.
4. Somministrare la prima dose lentamente.
5. Rivalutare a intervalli stabiliti; fermarsi se frequenza, pressione o conduzione superano le soglie.
6. Documentare e passare le consegne, specificando dose cumulativa.

!!! attenzione "Attenzione"
    Il rischio di accumulo si manifesta con dosi ripetute nell'arco di pochi minuti: la dose cumulativa va sempre annotata e comunicata al passaggio di consegne.
"""
ADD[("parte-05.md", "Emodinamica complessa")] = """
### Scenari e azioni in sintesi

| Scenario | Betabloccante? | Considerazioni |
|---|---|---|
| Shock cardiogeno | No | Sospendere, supportare |
| Scompenso acuto congesto | Non avviare; proseguire se già in terapia | Ridurre la dose solo se ipoperfusione |
| Shock settico con tachicardia persistente | Non routinario | Dati preliminari con esmololo |
| Dissezione aortica | Sì, prima misura | Esmololo o labetalolo |
| Crisi tireotossica | Sì (propranololo) | Con terapia antitiroidea |
| Feocromocitoma | Solo dopo blocco α | Rischio di crisi |
| Intossicazione da cocaina | Evitare i puri | Benzodiazepine, vasodilatatori |
| Embolia polmonare massiva | No | Reperfusione |

### Il paziente già in terapia che arriva in urgenza

Il betabloccante cronico può mascherare la tachicardia dello shock (l'ipovolemia può non produrre la tachicardia attesa) e rende meno efficace l'adrenalina. Una frequenza «normale» in un paziente trattato con ipotensione e segni di ipoperfusione è un campanello d'allarme.
"""

# ------------------------------------------------------------------ PARTE VI
ADD[("parte-06.md", "Controindicazioni")] = """
### Valutazione del rischio prima dell'avvio

Prima di prescrivere un betabloccante conviene rispondere a una lista di domande: la frequenza basale è superiore a 55–60 bpm? Il PR è nei limiti? C'è un blocco AV? La pressione sistolica è sufficiente? Esiste storia di asma o broncospasmo? Il paziente è diabetico con ipoglicemie? Assume verapamil, diltiazem, digossina, amiodarone? C'è un'arteriopatia o Raynaud? È in gravidanza? La funzione renale ed epatica è adeguata? Una risposta affermativa non esclude di per sé la terapia, ma ne orienta molecola, dose e monitoraggio.

### Situazioni in cui si procede con cautela

Anziani fragili, ipotensione di base, scompenso recente, diabete insulino-trattato, malattia polmonare ostruttiva, arteriopatia, sindromi depressive importanti, insufficienza renale o epatica: l'avvio avviene a dosi basse e con controllo ravvicinato.
"""
ADD[("parte-06.md", "Effetti avversi")] = """
### Frequenza e gestione degli effetti più comuni

| Effetto | Frequenza (qualitativa) | Gestione |
|---|---|---|
| Astenia, affaticamento | Frequente, spesso transitoria | Rassicurare; verificare bradicardia e ipotensione |
| Bradicardia | Frequente, dose-dipendente | ECG; ridurre dose; rivedere interazioni |
| Ipotensione ortostatica | Frequente con molecole vasodilatatrici | Alzarsi lentamente; adeguare dose e orario |
| Estremità fredde | Frequente | Rassicurare; valutare arteriopatia |
| Disturbi del sonno | Con molecole lipofile | Dose serale ridotta; cambiare molecola |
| Broncospasmo | Raro ma importante | Sospendere; broncodilatatori |
| Peggioramento dello scompenso | All'avvio, nei rialzi | Ottimizzare diuretico; ridurre dose |
| Mascheramento ipoglicemia | In diabetici | Educazione; automonitoraggio |

### Quando segnalare e quando ridurre

Un effetto avverso lieve non giustifica la sospensione immediata, mentre sintomi di allarme (sincope, blocco AV nuovo, broncospasmo, scompenso ingravescente) richiedono rivalutazione medica tempestiva. Va sempre privilegiata la riduzione della dose rispetto all'interruzione quando la terapia ha un'indicazione prognostica.
"""
ADD[("parte-06.md", "Interazioni farmacologiche")] = """
### Come verificare un'interazione

Procedere per tre passaggi: identificare il meccanismo (farmacodinamico o farmacocinetico), valutare la gravità e la reversibilità, decidere se evitare, ridurre dose o monitorare. Per i betabloccanti i meccanismi dominanti sono la somma di effetti rallentanti sul nodo AV e l'inibizione del CYP2D6. Gli strumenti di riferimento sono l'RCP del farmaco, la banca dati AIFA e il servizio di farmacia ospedaliera.

!!! chiave "Punti chiave"
    - Betabloccante + verapamil/diltiazem: evitare (specialmente EV).
    - Betabloccante + clonidina: sospendere prima il betabloccante, poi la clonidina.
    - Betabloccante + inibitori CYP2D6: ridurre dose e monitorare.
    - In anafilassi: adrenalina meno efficace; considerare glucagone.
"""
ADD[("parte-06.md", "Rebound e sospensione")] = """
### Dove il rebound è più pericoloso

Il rischio maggiore si ha nei pazienti con cardiopatia ischemica, ipertensione severa o aritmie, e in chi assume dosi elevate di molecole a breve emivita (propranololo, metoprololo tartrato). Per le molecole a lunga emivita il fenomeno può comparire più tardi e in forma attenuata. È più probabile quando la sospensione avviene per dimenticanza, mancata disponibilità del farmaco, digiuno prima di un intervento o dimissione senza istruzioni.

### Prevenire il rebound nel quotidiano

- Controllare la scorta di farmaco e la prescrizione prima di dimissioni e festività.
- Inserire nelle consegne e nella lettera di dimissione l'indicazione «non sospendere».
- Nel perioperatorio, proseguire la terapia anche il giorno dell'intervento.
- Segnalare al medico qualsiasi dose saltata ripetutamente.
"""

# ------------------------------------------------------------------ PARTE VII
ADD[("parte-07.md", "Somministrazione")] = """
### Scheda di somministrazione per molecola (orale)

| Molecola | Frequenza tipica | Rapporto con il cibo | Attenzioni |
|---|---|---|---|
| Bisoprololo | 1 volta/die, mattino | Indifferente | Divisibile se previsto |
| Metoprololo succinato | 1 volta/die | Indifferente | Non frantumare |
| Metoprololo tartrato | 2 volte/die | Indifferente | Rilascio immediato |
| Carvedilolo | 2 volte/die | Con il cibo | Ortostatismo all'avvio |
| Nebivololo | 1 volta/die | Indifferente | Metabolizzatori lenti |
| Atenololo | 1 volta/die | Indifferente | Renale |
| Propranololo | 2–3 volte/die | Indifferente | Non selettivo |

### Pazienti con difficoltà di deglutizione

Alcune formulazioni possono essere divise o sciolte; altre no. Prima di frantumare o aprire una compressa, verificare sulla scheda tecnica o con il farmacista se la formulazione lo consente; non frantumare mai quelle a rilascio prolungato. Nel paziente a digiuno o con sondino, chiedere indicazioni sulla forma alternativa, senza sospendere la terapia di propria iniziativa.
"""
ADD[("parte-07.md", "Monitoraggio")] = """
### Cartella e documentazione

Annotare per ogni somministrazione: orario, valori di frequenza e pressione, eventuali sintomi, motivo di eventuale mancata somministrazione e persona informata. Nei reparti con scale di early warning, integrare i valori nel punteggio. Un andamento in discesa della frequenza o della pressione tra due controlli, anche se entro i limiti, merita segnalazione.

### Passaggio delle consegne: lista minima

- Molecola, dose, orario dell'ultima somministrazione.
- Frequenza e pressione ultima e trend.
- Eventuali dosi non somministrate e motivo.
- Interazioni attive e soglie concordate.
- Sintomi da sorvegliare.
"""
ADD[("parte-07.md", "Complicanze")] = """
### Sequenza di risposta alla bradicardia sintomatica (schema didattico)

1. Posizionare il paziente supino, sollevare gli arti inferiori se ipoteso.
2. Misurare frequenza e pressione, ottenere ECG, saturimetria.
3. Avvisare il medico e preparare accesso venoso e carrello d'emergenza.
4. Preparare atropina e, su indicazione, glucagone, calcio, catecolamine e stimolazione.
5. Sospendere il farmaco in corso; registrare dose e orario.
6. Monitorare in modo continuo fino a stabilizzazione.

!!! attenzione "Attenzione"
    L'atropina può essere poco efficace nella bradicardia da betabloccante; non ritardare il ricorso ad altre misure se non c'è risposta.
"""
ADD[("parte-07.md", "Educazione del paziente")] = """
### Perché i pazienti smettono: cause di non aderenza

| Causa | Strategia educativa |
|---|---|
| Si sente bene e pensa che il farmaco non serva | Spiegare la funzione protettiva |
| Effetti avversi attribuiti al farmaco (stanchezza, freddo) | Dire che sono comuni e spesso transitori; proporre soluzioni |
| Timore per la funzione sessuale | Parlarne apertamente; riferire al medico |
| Politerapia complessa | Semplificare gli orari; usare blister o organizer |
| Costi o scorte esaurite | Pianificare le ricette; coinvolgere il medico di famiglia |
| Convinzioni errate («è un farmaco solo per la pressione») | Chiarire l'indicazione specifica |

### Strumenti utili

Diario di polso e pressione, scheda con i segni d'allarme, organizer settimanale, promemoria sul telefono, numero da contattare. Nei pazienti anziani o con deficit cognitivo, il coinvolgimento del caregiver è essenziale.
"""

# ------------------------------------------------------------------ PARTE VIII
ADD[("parte-08.md", "Anziani e fragilità")] = """
### Un esempio pratico

Una donna di 82 anni, con scompenso a FE 35% e pressione 105/62 mmHg, inizia bisoprololo 1,25 mg. Dopo 2 settimane riferisce stanchezza e due episodi di capogiro al risveglio. Si misura la pressione in ortostatismo (92/54 mmHg): si sposta l'assunzione di un diuretico, si insiste sull'alzarsi lentamente e si mantiene la dose per un'ulteriore settimana prima di riprendere la titolazione. Il ragionamento è graduale: un singolo sintomo non porta alla sospensione.
"""
ADD[("parte-08.md", "Gravidanza e allattamento")] = """
### Tabella pratica

| Farmaco | Gravidanza | Allattamento |
|---|---|---|
| Labetalolo | Preferito (oral e EV) | Generalmente accettabile |
| Metoprololo | Opzione preferita | Generalmente accettabile |
| Propranololo | Uso possibile, brevi periodi | Generalmente accettabile |
| Atenololo | Da evitare | Meno adatto (accumulo nel latte) |
| Bisoprololo | Dati più limitati | Dati limitati; valutare |
| Sotalolo | Casi specifici | Meno adatto |
"""
ADD[("parte-08.md", "Pediatria")] = """
### Comunicazione con i genitori

Nell'uso pediatrico, specie con il propranololo per l'emangioma, la collaborazione dei genitori è essenziale: devono sapere come somministrare il farmaco dopo il pasto, che cosa fare se il bambino vomita o non mangia, quali segni indicano ipoglicemia o broncospasmo, e quando contattare il medico. Una scheda scritta con orari e numeri utili riduce gli errori.
"""
ADD[("parte-08.md", "Insufficienza renale")] = """
### Un promemoria operativo

Nel paziente con insufficienza renale cronica, prima di avviare o continuare un betabloccante verificare: stadio della malattia, eliminazione del farmaco, dose rispetto alla clearance, rischio di ipotensione intradialitica, interazioni con farmaci che alterano la potassiemia. In caso di dubbio chiedere il parere del nefrologo e del farmacista clinico.
"""
ADD[("parte-08.md", "Epatopatia e ipertensione portale")] = """
### Cautele pratiche

Nel cirrotico, l'uso dei betabloccanti richiede sorveglianza di pressione arteriosa, frequenza e funzione renale; l'ipotensione severa e l'insufficienza renale acuta sono motivi per sospendere o ridurre. Non vanno associati con leggerezza a farmaci che peggiorano l'emodinamica renale (FANS, ACE-inibitori in ascite). Il paziente va educato a segnalare vertigini, riduzione della diuresi e sanguinamenti.
"""
ADD[("parte-08.md", "Malattie respiratorie")] = """
### Tabella di orientamento

| Condizione | Betabloccante | Note |
|---|---|---|
| Asma | Generalmente evitato | Specie non selettivi |
| BPCO con indicazione cardiologica | β1-selettivo a basse dosi | Monitorare sintomi |
| Respiro sibilante da scompenso (asma cardiaco) | Non è asma | Tratta lo scompenso |
| Collirio con timololo | Può provocare broncospasmo | Chiedere sempre |
"""
ADD[("parte-08.md", "Diabete, endocrinopatie e altre comorbilità")] = """
### Sintesi per condizione

| Condizione | Orientamento |
|---|---|
| Diabete | Non controindicato; educare sul mascheramento; molecole metabolicamente neutre |
| Ipertiroidismo | Propranololo per sintomi e crisi |
| Arteriopatia lieve-moderata | Non controindicato |
| Ischemia critica, Raynaud | Evitare, specie non selettivi |
| Depressione | Nessun nesso causale solido; monitorare |
| Atleta agonista | Verificare elenco WADA; esenzione terapeutica |
"""

# ------------------------------------------------------------------ PARTE IX
ADD[("parte-09.md", "Quadro clinico dell'intossicazione")] = """
### Differenze tra molecole nell'overdose

| Molecola | Caratteristica tossicologica | Segni particolari |
|---|---|---|
| Propranololo | Lipofilo, stabilizzazione di membrana | Convulsioni, coma, QRS largo, shock precoce |
| Sotalolo | Blocco dei canali del potassio | QT lungo, torsione di punta |
| Metoprololo, carvedilolo | Lipofili | Bradicardia, ipotensione; carvedilolo con vasodilatazione |
| Atenololo, nadololo | Idrofili, accumulo renale | Bradicardia, dializzabili |
| Labetalolo | Blocco α e β | Ipotensione marcata |

### Segni che orientano

Il «triplo segnale» di bradicardia, ipotensione e ipoglicemia, in un paziente con anamnesi di betabloccante, è altamente suggestivo. La glicemia va controllata subito, soprattutto nei bambini.
"""
ADD[("parte-09.md", "Gestione dell'intossicazione")] = """
### Il ruolo dell'infermiere

L'infermiere raccoglie e documenta l'anamnesi (che farmaco, quanto, quando, formulazione), prepara e controlla i farmaci ad alto rischio, assicura accessi venosi (almeno due), monitoraggio continuo, controllo glicemico e dei potassio, gestione dell'insulina ad alte dosi (con doppio controllo), osservazione di segni neurologici, prevenzione di aspirazione. In caso di intossicazione volontaria è fondamentale anche la sorveglianza della sicurezza del paziente e il coinvolgimento dei servizi di salute mentale.

### Prevenzione

Educare i pazienti a conservare i farmaci in modo sicuro, usare organizer settimanali, non assumere dosi doppie, e a segnalare terapie con interazioni; ai familiari di bambini, a conservare i farmaci fuori dalla portata. Ridurre gli errori in ospedale con riconoscimento look-alike/sound-alike, doppio controllo e prescrizione elettronica.

!!! chiave "Punti chiave"
    - Triade di allarme: bradicardia, ipotensione, ipoglicemia.
    - Antidoti principali: glucagone, calcio, insulina ad alte dosi, catecolamine.
    - Contatto immediato con il Centro Antiveleni.
"""

# ------------------------------------------------------------------ PARTE X
ADD[("parte-10.md", "Caso 3 – Fibrillazione atriale rapida in un paziente con BPCO")] = """
### Autovalutazione rapida

!!! nota "Nota – Dieci domande a risposta breve"
    1. Quali sono le quattro molecole con evidenza di mortalità nello scompenso?
    2. Perché non si inizia un betabloccante in uno scompenso congesto?
    3. Perché il verapamil EV con un betabloccante EV è pericoloso?
    4. Qual è la prima misura nella dissezione aortica acuta, nel contesto farmacologico?
    5. Perché il feocromocitoma richiede il blocco α prima del betabloccante?
    6. Come si gestisce la sospensione programmata di un betabloccante?
    7. Quali sono i segni che l'infermiere non deve ignorare prima della dose?
    8. Quali antidoti si usano nell'intossicazione grave?
    9. Perché l'atenololo è meno favorevole come antipertensivo?
    10. Come cambia la scelta in un paziente asmatico rispetto a uno con BPCO?

    **Risposte sintetiche.** 1) Bisoprololo, carvedilolo, metoprololo succinato, nebivololo. 2) Per il rischio di peggioramento emodinamico. 3) Rischio di asistolia e shock. 4) Betabloccante EV (esmololo o labetalolo). 5) Per evitare crisi ipertensive da stimolo α non contrastato. 6) Riduzione graduale con monitoraggio. 7) Frequenza, pressione, ECG, sintomi nuovi. 8) Glucagone, calcio, insulina ad alte dosi, catecolamine. 9) LIFE e ASCOT-BPLA. 10) Asma: evitare; BPCO: β1-selettivo a basse dosi se c'è indicazione.
"""

# ------------------------------------------------------------------ PARTE XI
ADD[("parte-11.md", "Tabelle riepilogative")] = """
### Mini-algoritmo di scelta (didattico)

| Domanda | Se sì | Se no |
|---|---|---|
| Shock, bradicardia grave, blocco AV non protetto, broncospasmo attivo? | Non somministrare; avvisare | Prosegui |
| Scompenso acuto con congestione o ipoperfusione? | Non avviare; se già in terapia, valutare riduzione | Prosegui |
| HFrEF stabile? | Bisoprololo, carvedilolo, metoprololo succinato, nebivololo | Prosegui |
| Angina o aritmia che richiede controllo? | β1-selettivo; evitare verapamil/diltiazem in associazione | Valutare altre classi |
| Ipertensione senza altre indicazioni? | Non è prima linea | Prima linea: ACE-i/sartano, CCB, tiazidico |
| Gravidanza? | Labetalolo o metoprololo | Scelta ordinaria |
"""

def main():
    n = 0
    files = {}
    for (fname, key), text in ADD.items():
        p = VOL / fname
        t = files.get(fname) or p.read_text(encoding="utf-8")
        marker = f"<!-- exp1:{key} -->"
        if marker in t:
            files[fname] = t; continue
        # trova la sezione "## <key...>" e il successivo "\n## " o fine file
        m = re.search(r"^## " + re.escape(key) + r"[^\n]*$", t, flags=re.M)
        if not m:
            print("NON TROVATO:", fname, key); continue
        nxt = re.search(r"^## ", t[m.end():], flags=re.M)
        pos = m.end() + nxt.start() if nxt else len(t)
        t = t[:pos].rstrip("\n") + "\n\n" + marker + "\n" + text.strip("\n") + "\n\n" + t[pos:]
        files[fname] = t; n += 1
    for f, t in files.items():
        (VOL / f).write_text(t, encoding="utf-8")
    print("sezioni aggiunte:", n)

if __name__ == "__main__":
    main()
