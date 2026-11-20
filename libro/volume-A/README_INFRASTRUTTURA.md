# Volume A «ABC della cardiologia clinica» – infrastruttura di impaginazione e figure

Strumenti per scrivere, impaginare e illustrare il Volume A (KDP, brossura 7 × 10 in, interno B/N su
carta bianca, ≈ 300 pagine). **Qui non ci sono capitoli**: c'è il motore, il generatore di tracciati
simulati, la pipeline dei tracciati reali, gli schemi e gli strumenti di validazione.

```
libro/volume-A/
├── INDICE_PROPOSTO.md            struttura del libro (approvazione dell'autore)
├── README_INFRASTRUTTURA.md      questo file
├── engine/                       motore 7 × 10 in
│   ├── build_A.py                Markdown → PDF (WeasyPrint), due passaggi, indici, figure
│   ├── style_A.css               pagina, tipografia, riquadri B/N, figure
│   ├── verifica_A.py             controlli di stampa (formato, font, colore, grigi, riempimento)
│   ├── fonts/                    Gelasio (OFL) + DejaVu Sans per i simboli, con licenze
│   └── prova/                    capitolo di prova (sorgenti + output/prova_7x10.pdf)
└── figure/
    ├── MANIFEST.csv              elenco unico delle figure (id, tipo, file, fonte/licenza, criteri, stato)
    ├── genera_manifest.py        rigenera il MANIFEST conservando le decisioni del revisore
    ├── FONTI_E_LICENZE.md        licenze verificate e testi di attribuzione
    ├── CHECKLIST_VALIDAZIONE.md  criteri per la revisione clinica indipendente
    ├── common/ecgplot.py         griglia ECG standard (B/N, 25 mm/s, 10 mm/mV) – usata da sim e real
    ├── common/ecgmeasure.py      misure oggettive (FC, RR, PR, QRS, QT, ST, asse) per il QC
    ├── sim/                      tracciati didattici simulati (modello a dipolo)
    ├── real/                     tracciati reali PhysioNet (PTB-XL, MIT-BIH, CUDB) con QC
    └── schemi/                   schemi originali disegnati con codice
```

## 1. Requisiti

```bash
pip install weasyprint markdown wfdb matplotlib scipy numpy pandas pillow fonttools pyphen
# strumenti di sistema: poppler-utils (pdfinfo, pdffonts, pdftoppm, pdftotext), curl
```
Versioni usate nella sessione di costruzione: WeasyPrint 70.0, wfdb 4.3.1, matplotlib 3.11, scipy 1.18.

## 2. Compilare il libro

```bash
python3 libro/volume-A/engine/build_A.py <cartella-sorgenti> [--out nome.pdf] [--bozza]
python3 libro/volume-A/engine/verifica_A.py <cartella-sorgenti>/output/<file>.pdf
```
Prova già pronta: `python3 libro/volume-A/engine/build_A.py libro/volume-A/engine/prova`.

La cartella dei sorgenti (es. `libro/volume-A/testo/`, da creare per i capitoli veri) contiene:
- `meta.json` – `titolo`, `sottotitolo`, `edizione`, `file`, `copyright_html` (vedi `engine/prova/meta.json`);
- `parte-00-*.md` – **Parte 0**, pagine preliminari in numeri romani (ogni `#` apre una pagina);
- `parte-NN-*.md` – Parti 1–12: **il numero viene dal nome del file**.

Uscite in `<sorgenti>/output/`: il PDF, `debug.html` (HTML finale, utile per capire un problema di
layout), `build_report.json` (pagina di ogni figura, stato di validazione, spostamenti, avvisi),
`verifica_report.json`. `--bozza` stampa in didascalia lo stato delle figure non validate.

### Pagina e tipografia (in `style_A.css`)
- 7 × 10 in = 504 × 720 pt; margini speculari: interno 0,8 in, esterno 0,55 in, alto/basso 0,75 in;
  gabbia 5,65 × 8,5 in (143,5 × 215,9 mm).
- **Minimi KDP verificati il 19/11/2026** (help topic GVBQ3CMEQW3W2VL6): interno 0,375 in (24–150 pp.),
  0,5 in (151–300), **0,625 in (301–500)**, 0,75 in (501–700), 0,875 in (701–828); esterno/alto/basso
  ≥ 0,25 in senza abbondanza. Con 0,8 in il margine interno è valido fino a 700 pagine: superare le 300
  pagine non richiede modifiche. 7 × 10 in è un formato «large trim» (costo di stampa diverso), B/N su
  carta bianca fino a 828 pagine.
- Raccomandazioni KDP (Paperback Submission Guidelines G201857950): **grigi ≥ 10 %**, **linee ≥ 0,75 pt**,
  corpo minimo 7 pt, immagini ≥ 300 dpi. Tutto il CSS e le figure le rispettano.
- Gelasio 10,3 pt, interlinea 1,4, giustificato con sillabazione italiana (`lang="it"`, Pyphen);
  tabelle 8,6 pt; riquadri 9,4 pt; numeri di pagina agli angoli esterni; intestazione corrente
  sinistra = titolo, destra = Parte; ogni Parte su pagina nuova (senza forzare la dispari).

### Convenzioni Markdown
| Sintassi | Risultato |
|---|---|
| `# Titolo` | «Parte NN» su pagina nuova |
| `## Titolo` | sezione NN.M numerata, nell'indice generale |
| `### Metoprololo {.pa}` / `### Flutter atriale {.ix}` | voce **principale** (pagina in grassetto) nell'indice analitico |
| `[metoprololo]{.pa}` | occorrenza indicizzata tra i **farmaci** |
| `[flutter atriale]{.ix}` | occorrenza indicizzata tra **aritmie, quadri ECG e termini** |
| `[β-bloccante]{.pa voce="Beta-bloccanti"}` | occorrenza registrata sotto un'altra voce |
| `!!! nota "Titolo"` + corpo indentato di 4 spazi | riquadro (titolo predefinito se omesso) |
| `::: fig ID [larghezza=intera\|mezza\|mezza-sx\|pagina] [variante=3x4]` … `:::` | figura numerata «Fig. N.k» con didascalia |
| `::: ecg-esercizio ID` domanda `---` soluzione `:::` | esercizio; la soluzione va in fondo alla Parte |
| `[[fig:ID]]`, `[[es:ID]]` | rimandi «Fig. N.k», «Esercizio N.k» |
| `- [ ] voce` | casella di controllo |

Tipi di riquadro (distinti per **forma**, non per colore): `nota` (Nota clinica: fondo grigio 10 %,
bordo pieno) · `chiave` (Regola/Mnemonico: barra nera laterale) · `allarme` (bordo doppio) · `errore`
(Errore classico: bordo tratteggiato) · `autotest` (righe per la risposta: `{{righe:N}}` dove servono,
altrimenti 3 in fondo) · `sbar` (Cosa dico al medico: elenco `- S: …`, `- B: …`, `- A: …`, `- R: …` →
tabella a due colonne) · `rischio` (Farmaco ad alto rischio: titolo in negativo) · `focus`
(Cardiochirurgia e PS: filetti spessi sopra e sotto) · `obiettivi`.

La **Nota clinica** segue sempre il modello dell'indice: *Situazione · Cosa si vede · Cosa si fa ·
Il farmaco, in due righe · Occhio infermieristico* (in grassetto a inizio frase).

### Come lavora il motore
1. Ogni Parte è convertita separatamente (numerazione di sezioni, figure ed esercizi per Parte).
2. Primo rendering con numeri di pagina fittizi «000» (stessa larghezza dei reali, così l'indice non
   sposta il corpo); lettura delle pagine delle ancore.
3. **Galleggiamento delle figure** (WeasyPrint non ha i float di pagina): se una figura o un esercizio
   finisce in cima a una pagina lasciando la precedente sotto l'82 %, viene spostato dopo 1–3 blocchi
   successivi della stessa sezione (mai oltre un titolo `#`/`##`); se una figura a mezza colonna si
   spezza tra due pagine, viene anticipata di un blocco. Fino a 6 iterazioni; gli spostamenti sono nel
   report.
4. Rendering finale con i numeri reali in indice generale e indice analitico (farmaci; aritmie e termini).

### Didascalie automatiche
Il motore legge `figure/MANIFEST.csv` tramite l'ID: file, tipo e fonte. Aggiunge l'etichetta
«Tracciato didattico simulato (ID)», «Tracciato reale – fonte – licenza» o «Schema originale» e, per i
tracciati, «25 mm/s, 10 mm/mV» se la figura è a scala reale oppure «griglia ridotta al X %».

### Verifica di stampa (`verifica_A.py`)
Bloccanti: formato 504 × 720 pt su tutte le pagine; tutti i font incorporati; nessun pixel colorato;
nessun grigio più chiaro del 10 % nel CSS e negli SVG usati. Avvisi: pagina interna di Parte < 80 %,
ultima pagina di Parte < 65 %. **Il riempimento si corregge sul contenuto** (aggiungere/togliere testo,
cambiare `larghezza` o posizione di una figura), non sullo stile.

## 3. Aggiungere una figura
1. Generarla (simulato: voce in `sim/catalogo_sim.py`; reale: categoria in `real/select_real.py`;
   schema: funzione in `schemi/genera_schemi.py`; figura esterna: SVG in una cartella di `figure/` più
   un JSON accanto con gli stessi campi dei generati, `tipo` e `licenza` compresi).
2. `python3 libro/volume-A/figure/genera_manifest.py` (conserva `stato_validazione` e `note_revisore`).
3. Nel testo: `::: fig ID` + didascalia + `:::`.
4. Farla validare (`CHECKLIST_VALIDAZIONE.md`) e segnare `validato` nel MANIFEST.

Larghezze: le strisce del ritmo sono 140 mm (2 righe × 5,2 s a scala reale); gli ECG a 12 derivazioni
`<ID>.svg` sono 6×2 a **scala reale** (140 mm × ≈ 170–200 mm: quasi una pagina) e `<ID>_3x4.svg`
(`variante=3x4`) sono 3×4 ridotti al 55 % (≈ 90 mm di altezza, con i quadretti piccoli resi a punti).

## 4. Tracciati simulati (`figure/sim/`)
```bash
python3 libro/volume-A/figure/sim/genera_sim.py [ID ...]
```
- `ecgsim.py`: **modello a dipolo** – un vettore cardiaco 3D somma di componenti gaussiane (setto,
  parete libera del VS in due fasi, regioni basali; P a due componenti atriali; T asimmetrica; U;
  corrente di lesione nel tratto ST), proiettato sulle 12 derivazioni (Einthoven/Goldberger per le
  periferiche, quindi III = II − I sempre esatta; vettori orizzontali con guadagno per V1–V6).
  Motore del ritmo con eventi atriali e ventricolari e conduzione AV esplicita. Parametri espliciti:
  frequenza, PR, durata QRS, QTc (Fridericia), asse, ampiezze, vettori.
- `catalogo_sim.py`: 46 tracciati (39 iniziali + 7 aggiunti il 20/11/2026: WPW, pericardite, infarto
  posteriore, Wellens tipo B, de Winter, ipotermia con onda J, effetto digitalico) con descrizione attesa, criteri automatici, criteri per il revisore,
  affidabilità del modello.
- Uscite: `out/<ID>.svg|png|json` e `QC_sim.md` (misure automatiche sul segnale: **39/39 superano** i
  criteri). Ogni JSON contiene parametri, misure ed eventi (tempi di P, QRS, spike).
- **Non modellati** (rimandati ai reali): Brugada (alterazione limitata a V1–V2 che un dipolo unico non
  riproduce senza falsare le altre derivazioni), infarto del VD (richiede V4R), derivazioni posteriori
  V7–V9, artefatti. Nella WPW la sede della via accessoria non è rappresentata e la misura automatica del
  PR non è affidabile. FV e torsione di punta sono modelli **fenomenologici** (affidabilità
  «schematica»): usare preferibilmente i reali.

## 5. Tracciati reali (`figure/real/`)
```bash
python3 libro/volume-A/figure/real/select_real.py [--max 4] [--categorie AFIB,CLBBB,...]
```
- PhysioNet si raggiunge con `curl -L` (redirect verso `physionet-open.s3.amazonaws.com`). I dati
  scaricati vanno in `real/cache/` (**non versionata**, ≈ 40 MB, rigenerabile).
- Selezione: PTB-XL – codice diagnostico con likelihood 100 (per i codici di **ritmo**, che in PTB-XL
  hanno likelihood 0 = «non specificata», basta la presenza e l'unicità del ritmo), nessun codice fuori
  da un elenco ammesso, `validated_by_human`, nessun problema di segnale; MIT-BIH/CUDB – finestre dentro
  episodi annotati con battiti coerenti (es. salve di TV: ≥ 6 V consecutivi).
- **QC**: misure oggettive confrontate con l'etichetta; incoerenti scartati; esclusioni manuali motivate
  (`ESCLUSI`). Report: `QC_report.md`.
- Rendering con lo stesso `ecgplot` dei simulati, filtro 0,5–40 Hz dichiarato in didascalia.
- Licenze e attribuzioni: `figure/FONTI_E_LICENZE.md`.

## 6. Schemi (`figure/schemi/`)
`python3 libro/volume-A/figure/schemi/genera_schemi.py` – potenziale d'azione ventricolare e del nodo
del seno, Wiggers semplificato (con ECG simulato), sistema di conduzione a blocchi, Einthoven ed
esassiale, elettrodi precordiali, territori coronarici sulle 12 derivazioni.

## 7. Flusso consigliato per le sessioni di scrittura
1. Scrivere una Parte in `testo/parte-NN-*.md` citando le figure per ID (cercarle in `MANIFEST.csv`).
2. `build_A.py` → `verifica_A.py` → correggere vuoti e sforamenti sul contenuto.
3. Controllare `build_report.json`: figure mancanti, rimandi rotti, figure da validare.
4. Commit sul branch condiviso (`git pull --rebase` prima del push).

## 8. Limiti noti
- Gli ECG a 12 derivazioni a scala reale occupano quasi una pagina: la pagina che li precede resta
  spesso al 65–75 % (nella prova: pp. 15 e 17). Rimedi: usare `variante=3x4`, spostare il testo, o
  dedicare loro pagine di esercizi.
- Le misure automatiche sono grossolane (±10–20 ms) e falliscono con onda delta (WPW), ritmi misti e FV:
  per questi il QC è solo visivo.
- PTB-XL non distingue Mobitz I/II (`2AVB`) e le etichette di infarto non indicano la fase acuta.
- Il primo commit del simulatore conteneva SVG non ottimizzati (≈ 56 MB nella storia git); i file attuali
  sono ≈ 11 MB (simulati) + ≈ 35 MB (reali).
