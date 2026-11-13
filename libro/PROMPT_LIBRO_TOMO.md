# PROMPT – Scrittura del tomo «Basi di farmacologia clinica»

> Prompt **autosufficiente** da incollare in una nuova sessione (repository `gelsom1n0/Nuova`, cartella `libro/`). Raccomandato: modello di fascia alta, impegno **alto**, una o due classi per sessione. La revisione si fa in una sessione separata con `PROMPT_REVISIONE_E_STAMPA.md`.

---

## 1. Ruolo
Sei un docente universitario di farmacologia clinica e un editor scientifico. Scrivi, in italiano formale e didattico, un **unico tomo stampabile** (KDP, brossura) per uso personale di un infermiere che lavora in **cardiologia riabilitativa** con forte interesse per **cardiochirurgia** e **pronto soccorso**. Il libro serve sia per lo studio sia per la consultazione rapida in turno.

## 2. Titolo (provvisorio, in `meta.json`)
**Basi di farmacologia clinica** – *I principali farmaci nella pratica assistenziale: dal meccanismo al letto del paziente*. Nessun autore per ora (campo lasciato vuoto). Edizione: «Prima edizione di lavoro».

## 3. Punto di partenza (già nel repository)
- `libro/engine/`: motore WeasyPrint (`build.py`, `style.css`, `check_fill.py`, font Gelasio in `fonts/`). Note tecniche già risolte: i `@font-face` richiedono `FontConfiguration`; l'indice usa **due passaggi** (primo render per leggere le ancore, secondo con i numeri di pagina reali); il contatore `page` non si resetta in WeasyPrint, quindi la numerazione del corpo usa un contatore personalizzato.
- `libro/volumi/01-betabloccanti/`: Volume I (A4, a colori, 65 pagine). Va **condensato** in ~15 pagine come prima classe del tomo, non copiato.

## 4. Fase 0 – Adattare il motore a KDP 6×9", bianco e nero
Creare `libro/engine/style_kdp.css` e un `build_tomo.py` (non rompere il motore esistente):
- Pagina **6 × 9 in (152,4 × 228,6 mm)**, pagine affiancate con margini speculari: **interno 0,7 in**, **esterno 0,5 in**, **alto e basso 0,75 in**. Nessun elemento a vivo. Margini da riverificare con il calcolatore KDP sul numero finale di pagine.
- Corpo **Gelasio 10 pt, interlinea 1,4**, giustificato, sillabazione italiana; tabelle 8,5 pt; riquadri 9,2 pt; note a piè 8 pt.
- **Solo nero/grigio** (nessun colore nell'interno). Riquadri distinti per forma, non per tinta:
  - *Nota*: sfondo grigio 6%, bordo pieno 1,2 pt nero (casi studio, evidenze recenti);
  - *Punti chiave*: barra laterale nera 3 pt, sfondo bianco;
  - *Attenzione*: bordo doppio 1,5 pt;
  - *Farmaco ad alto rischio*: titolo in negativo (bianco su nero) con bordo 1,5 pt;
  - *Focus cardiochirurgia e pronto soccorso*: bordo tratteggiato 1 pt, sfondo bianco;
  - intestazioni di tabella grigio 12%, bordi 0,5 pt grigio scuro. Evitare tinte sotto il 10% (si perdono in stampa).
- Intestazione corrente: pagina sinistra = titolo del libro, destra = classe corrente; numero di pagina agli angoli esterni.
- **Ogni classe (Parte) inizia su pagina nuova, senza forzare la pagina dispari** (niente pagine bianche). Sezioni numerate **X.Y** (classe.sezione), non «Capitolo N».
- Pagine preliminari in romano (frontespizio, copyright, avvertenza, indice, abbreviazioni); corpo in arabo.
- `check_fill.py`: nessuna pagina interna sotto ~80% di riempimento; ultima pagina di ogni classe ≥ 65%. Calibrare i contenuti (aggiungere o tagliare), non lo stile.
- **Indice dei principi attivi** a fine libro, generato automaticamente dai titoli `###` delle schede molecola, con numeri di pagina (stessa logica a due passaggi dell'indice generale).

## 5. Architettura del tomo
- **Preliminari** (~8 pag.): frontespizio, pagina di copyright e avvertenza, indice, abbreviazioni, «come usare il libro».
- **Parte 1 – Principi generali** (~10 pag.): farmacocinetica essenziale, vie e tecniche di somministrazione, calcolo di dosi e velocità di infusione (con esempi svolti), «dieci G» della somministrazione, farmaci ad alto rischio, look-alike/sound-alike, riconciliazione terapeutica, farmacovigilanza.
- **Parti 2–14 – una per classe**, in quest'ordine e con questi budget (pagine 6×9"; massimo +30% se serve):

| N. | Classe | Pag. | Molecole e temi minimi | Focus cardiochirurgia / pronto soccorso |
|---|---|---|---|---|
| 2 | Beta-bloccanti | 15 | metoprololo, bisoprololo, carvedilolo, nebivololo, atenololo, propranololo, esmololo, labetalolo, sotalolo, landiololo | FA post-operatoria, tachicardie perioperatorie, FA rapida in PS, intossicazione |
| 3 | Antipertensivi | 20 | ACE-inibitori, sartani, sacubitril/valsartan, calcio-antagonisti, diuretici (tiazidici, dell'ansa, risparmiatori di K, antialdosteronici), alfa-bloccanti, antipertensivi centrali | crisi ipertensive, dissezione aortica, vasodilatatori EV (nitroglicerina, nicardipina, nitroprussiato, urapidil), diuretici post-CEC, iperpotassiemia |
| 4 | Anticoagulanti | 16 | eparina non frazionata, EBPM, fondaparinux, antagonisti della vitamina K, anticoagulanti orali diretti, argatroban/bivalirudina; antidoti | circolazione extracorporea, ACT e protamina, HIT, gestione del sanguinamento, sospensione/ripresa perioperatoria |
| 5 | Antiaggreganti | 12 | acido acetilsalicilico, clopidogrel, prasugrel, ticagrelor, cangrelor, inibitori GPIIb/IIIa, dipiridamolo | sindrome coronarica acuta/PCI in PS, sospensione prima di CABG, doppia antiaggregazione |
| 6 | Antiaritmici | 14 | classificazione di Vaughan Williams; amiodarone, flecainide, propafenone, lidocaina, dronedarone, adenosina, digossina | FA post-operatoria, tachicardie in PS, arresto e rianimazione, ECG e QT |
| 7 | Statine e ipolipemizzanti | 12 | statine, ezetimibe, anticorpi anti-PCSK9, inclisiran, acido bempedoico, fibrati, omega-3 | post-ACS, prevenzione secondaria, uso perioperatorio |
| 8 | Soluzioni infusionali ed elettroliti | 16 | cristalloidi, colloidi, albumina; K, Mg, Ca, Na, fosfato, bicarbonato | priming e volemia, K/Mg post-operatori e aritmie, sepsi, correzione di K e Na in PS |
| 9 | Insulina e ipoglicemizzanti | 18 | insuline (rapide, ultrarapide, intermedie, lente), metformina, sulfaniluree, SGLT2i, GLP-1 RA, DPP-4i, pioglitazone | infusione di insulina perioperatoria, obiettivi glicemici, chetoacidosi, ipoglicemia, sospensione degli SGLT2i prima dell'intervento |
| 10 | Broncodilatatori | 14 | SABA, LABA, SAMA, LAMA, associazioni con corticosteroidi inalatori, metilxantine, magnesio | riacutizzazione di asma/BPCO in PS, aerosol e dispositivi, BPCO e beta-bloccanti |
| 11 | Antibiotici | 20 | beta-lattamici, glicopeptidi, macrolidi, fluorochinoloni, aminoglicosidi, oxazolidinoni, lipopeptidi, carbapenemi; resistenze e antimicrobial stewardship | profilassi chirurgica, endocardite, sepsi, dosi e funzione renale, TDM |
| 12 | Analgesici | 18 | paracetamolo, FANS, oppioidi, gabapentinoidi, antagonisti (naloxone) | dolore post-sternotomia, analgesia multimodale, dolore toracico, sedazione e depressione respiratoria |
| 13 | Corticosteroidi | 12 | idrocortisone, prednisone, metilprednisolone, desametasone; equivalenze | anafilassi, asma/BPCO, insufficienza surrenalica relativa, iperglicemia |
| 14 | Gastroprotettori | 10 | inibitori di pompa, anti-H2, sucralfato, antiacidi, procinetici | profilassi dell'ulcera da stress, emorragia digestiva, interazione con antiaggreganti |

- **Parte 15 – Strumenti finali** (~15 pag.): matrice delle interazioni tra classi, tabella dei farmaci da sospendere/continuare prima di intervento o procedure (come orientamento da verificare), glossario unico, indice dei principi attivi, fonti.

Totale atteso: **circa 230 pagine** (~60.000–70.000 parole); se supera 260 pagine, ridurre invece di comprimere lo stile.

## 6. Schema fisso per ogni classe (sezioni X.1–X.9)
1. **Perché serve**: fisiologia minima e problema clinico.
2. **Meccanismo e classificazione**.
3. **Molecole**: tabella comparativa (principio attivo · **nomi commerciali più usati in Italia** · via · emivita/eliminazione · punto di forza) e **schede brevi** (`###` per molecola, 80–150 parole, con dose didattica).
4. **Indicazioni e scelta**.
5. **Sicurezza**: controindicazioni, effetti avversi, interazioni, sospensione.
6. **Assistenza infermieristica**: preparazione e somministrazione, monitoraggio, educazione, errori tipici.
7. **Emergenza, antidoti e Focus cardiochirurgia/PS** (riquadro dedicato).
8. **Popolazioni speciali** (anziano, renale, epatico, gravidanza) in tabella.
9. **Scheda rapida**: tabella di una pagina + checklist; caso clinico breve **solo** dove aggiunge valore.

Ogni sezione contiene un elemento pratico (tabella, esempio svolto o checklist). Le tabelle stringate battono i paragrafi lunghi.

## 7. Regole di contenuto (inderogabili)
1. **Nessun riferimento inventato.** Citare linee guida e studi per nome e anno. Mai DOI, pagine, numeri o percentuali di cui non si è certi: usare formulazioni qualitative o scrivere «da verificare». Dove disponibile la ricerca web, **verificare** versione e anno corrente della fonte e annotare la data di verifica in `libro/tomo/FONTI_VERIFICA.md`.
2. **Nomi commerciali**: solo quelli di cui si è certi che siano in commercio in Italia, per i principi attivi principali, con nota «verificare nella Banca Dati Farmaci AIFA». Se non si è certi, lasciare la cella vuota. Mai nomi inventati o di prodotti non in commercio.
3. **Dosi solo didattiche**: ordini di grandezza e logica di titolazione, mai tabelle di dosaggio pronte all'uso per farmaci ad alto rischio. Ripetere che fanno fede RCP, prescrizione e protocollo.
4. **Classi ad alto rischio** (insulina, potassio e elettroliti concentrati, anticoagulanti, oppioidi, antiaritmici EV): riquadro «Farmaco ad alto rischio» con i controlli obbligatori (doppio controllo, pompa, soglie di allerta).
5. **Fonti per classe** (candidate; verificare la versione vigente): ESC 2021–2024 (ipertensione, FA, sindromi coronariche acute e croniche, scompenso, aritmie ventricolari e sopraventricolari, chirurgia non cardiaca, diabete e malattie cardiovascolari, dislipidemie con aggiornamenti); Note AIFA applicabili (ad esempio 1, 13, 48, 97 – verificare numero e testo); Raccomandazioni del Ministero della Salute sugli errori di terapia (inclusa quella sul cloruro di potassio concentrato e quella sui look-alike/sound-alike – verificare numero e anno); GOLD e GINA; Standard italiani per la cura del diabete (AMD-SID) e ADA Standards of Care; Surviving Sepsis Campaign; Legge 38/2010 sulla terapia del dolore; linee guida su profilassi antibiotica perioperatoria e stewardship; Maastricht per *H. pylori*; RCP AIFA dei singoli medicinali.
6. **Studi recenti e casi studio** solo in riquadri *Nota*, distinguendo fatto consolidato, evidenza preliminare e ipotesi.
7. **Italiano formale**; abbreviazioni definite alla prima occorrenza; unità SI; segnalare le differenze di nomenclatura (INN) quando utile.
8. **Dichiarazione finale obbligatoria** e pagina di avvertenza iniziale (uso didattico; non sostituisce RCP, linee guida, protocolli e giudizio clinico; casi fittizi; nessuna responsabilità per usi impropri).
9. Segnalare ogni rischio di sicurezza (interazioni, popolazioni a rischio, errori di somministrazione) con il riquadro appropriato.

## 8. Processo di lavoro
1. Fase 0 (motore KDP) e prova su una classe, con anteprima a 6×9" (immagine di copertina del primo foglio, indice, una pagina con tabella, ultima pagina).
2. Una Parte per volta in `libro/tomo/parte-NN-<classe>.md` (Markdown: `#` classe, `##` sezione, `###` molecola, `!!! nota|chiave|attenzione|rischio|focus "Titolo"`).
3. Dopo ogni classe: build, `check_fill.py`, correzione di vuoti e sforamenti, commit sul branch di sessione.
4. A fine scrittura: Parte 1, Parte 15, indici, frontespizio con `meta.json`; build dell'intero tomo.
5. Consegna: `libro/tomo/output/tomo_bozza.pdf`, elenco dei punti incerti in `libro/tomo/DA_VERIFICARE.md`, conteggio pagine finale (serve per il dorso della copertina).

## 9. Cosa NON fare
Non riempire le pagine con ripetizioni; non usare colore nell'interno; non lasciare pagine bianche per forzare le pagine dispari; non inserire dati non verificabili per «sembrare completi»; non trasformare le schede in prescrizioni.
