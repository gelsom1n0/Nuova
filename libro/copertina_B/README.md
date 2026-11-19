# Copertina KDP – «ABC della farmacologia clinica» (volume B)

Copertina per brossura KDP, 7 x 10 in, interno B/N su carta bianca, 290 pagine (provvisorie). Grafica originale procedurale, testo vettoriale Montserrat, CMYK, nessuna trasparenza. È la gemella del volume A (`../copertina_A/`): stessa griglia, stessa tipografia, stesso nero ricco C40 M30 Y30 K100, così i due volumi si leggono come serie. Cambiano soggetto (pillola al posto del cuore), colore d'accento (azzurro #1EA7FF, CMYK 78/18/0/0, al posto del rosso) e tracciato (motivo farmacologico al posto dell'ECG). Specifiche KDP: stesse del volume A, vedi `../copertina_A/KDP_SPECIFICHE.md` (stesso formato di rifilo).

## File

| File | Contenuto |
|---|---|
| `copertina_KDP.pdf` | PDF da caricare su KDP (variante A, CMYK) |
| `copertina_KDP_variante_B.pdf`, `copertina_KDP_variante_C.pdf` | Altre due varianti, stesso formato |
| `copertina_anteprima.png` | Anteprima della distesa con guide (rifilo, bleed, zone di sicurezza 0,125 e 0,25 in, dorso, area barcode) |
| `copertina_anteprima_senza_guide.png`, `prima_di_copertina.png` | Distesa pulita e solo la prima, variante A |
| `anteprime/` | `distesa_{A,B,C}.png`, `distesa_{A,B,C}_guide.png`, `prima_{A,B,C}.png` |
| `build_copertina_B.py` | Generatore (layout, testi, PDF, anteprime) |
| `arte_mesh.py`, `pillola_mesh.py` | Rendering procedurale e geometrie 3D (capsula, capsula aperta, compressa) |
| `build_info.json` | Parametri dell'ultimo build (pagine, dorso, dimensioni, area barcode, ecc.) |
| `PROMPT_COPERTINA_B.md` | Brief eseguito per questa copertina |
| `CHECKLIST_COPERTINA.md` | Verifica del file rispetto ai requisiti, e passi per il caricamento |
| `ASSET_E_IA.md` | Origine degli asset e questione della dichiarazione IA |
| `fonts/` | Montserrat (OFL) |
| `sorgenti/` | Maglie (`capsula_1800.npz`, `capsula_aperta_2400.npz`, `compressa_1500.npz`); `sorgenti/cache/` = raster dei piatti (ignorata da git) |

## Le tre varianti

- **A, capsula che si dematerializza + curva farmacocinetica (consigliata)**: capsula in due pezzi, inclinata in diagonale, che si dissolve in alto a destra in particelle, granuli di principio attivo e piccole molecole esagonali. Il tracciato è una curva di concentrazione plasmatica con dosi ripetute fino allo stato stazionario e finestra terapeutica tratteggiata: è l'equivalente farmacologico dell'ECG del volume A. Anteprima: `anteprime/prima_A.png`.
- **B, capsula aperta + catena molecolare**: le due metà separate, con un flusso di granuli e molecole tra l'una e l'altra; il tracciato è una catena molecolare (legami a zig-zag con anelli esagonali). Anteprima: `anteprime/prima_B.png`.
- **C, compressa + curva dose-risposta**: compressa rotonda con linea di frattura, vista a 3/4, il cui bordo diventa un reticolo esagonale; il tracciato è una sigmoide dose-risposta con punti sperimentali. Anteprima: `anteprime/prima_C.png`.

Motivo della raccomandazione di A: l'oggetto (capsula) e la dissoluzione sono riconoscibili anche in miniatura, e la curva a picchi e valli si legge subito come farmacocinetica e richiama l'ECG del volume A, rafforzando la serie.

## Dati del file (variante A, 290 pagine)

Distesa 1073,02 x 738 pt = 14,9031 x 10,25 in; dorso 0,6531 in; 2 raster CMYK 2850 x 4100 px a 400 ppi; file circa 7,6 MB (B: 8,1 MB; C: 7,8 MB). Dettaglio e verifiche in `CHECKLIST_COPERTINA.md`.

## Rigenerare con un nuovo numero di pagine

```
python3 build_copertina_B.py --pagine N [--variante A|B|C] [--tutte] [--autore "Nome Cognome"]
```

I due piatti raster sono ancorati ai bordi esterni del file: cambiando le pagine cambia solo il dorso, che è vettoriale. La cache dei raster in `sorgenti/cache/` viene quindi riutilizzata (rigenerazione in pochi secondi). La cache è ignorata da git (`.gitignore` locale) e si ricostruisce da sola se manca. Il build aggiorna anche `build_info.json` e le anteprime.

### Opzioni

| Opzione | Significato |
|---|---|
| `--pagine N` | Numero di pagine (default 290) |
| `--autore "Nome Cognome"` | Nome dell'autore (campo parametrico, oggi vuoto) |
| `--variante A\|B\|C` | Variante del PDF principale `copertina_KDP.pdf` (default A) |
| `--tutte` | Genera anche le altre varianti (`copertina_KDP_variante_X.pdf` + anteprime) |
| `--trim LxA` | Formato di rifilo in pollici (default `7x10`) |
| `--carta bianca\|crema` | Coefficiente del dorso (0,002252 o 0,0025 in per pagina) |
| `--nero ricco\|solo-k` | Nero di fondo: ricco C40 M30 Y30 K100 (default) oppure solo K100 |
| `--colore cmyk\|rgb` | Spazio colore del PDF (default CMYK; RGB solo per prove) |
| `--rigenera-arte` | Ignora la cache e ricalcola i raster |
| `--dpi-anteprima N` | Risoluzione delle anteprime PNG (default 150) |

## Modificare i testi

Le costanti in cima a `build_copertina_B.py`: `KICKER`, `TITOLO_GRANDE`, `TITOLO_RIGA`, `SOTTOTITOLO`, `QUARTA_INTRO`, `QUARTA_PUNTI`, `AVVERTENZA`. Il testo è vettoriale, quindi cambiarlo non richiede di rigenerare l'arte (i raster contengono solo aloni luminosi). Il testo del dorso è nel blocco "DORSO" di `costruisci()`.

**Testi di lavoro**: sottotitolo (riusato da «Basi di farmacologia clinica») e testi di quarta (principi di farmacocinetica e farmacodinamica, vie di somministrazione e interazioni; antibiotici, analgesici e oppioidi, insuline, broncodilatatori, corticosteroidi e gastroprotettori; schede rapide e checklist infermieristiche) sono provvisori e vanno confermati dall'autore sul contenuto finale del volume B.

## Coerenza con il volume A

Le due copertine condividono griglia, margini, posizione di kicker, «ABC», titolo, filetto, sottotitolo, quarta, avvertenza e dorso (testo dall'alto al basso, «ABC» in colore d'accento, resto in bianco, piccola icona d'accento: qui una capsula). Variano solo soggetto, accento e tracciato. Le modifiche alla griglia o alla tipografia vanno fatte in entrambi gli script per non perdere l'effetto serie.

## Requisiti

python3, reportlab, numpy, opencv-python-headless, Pillow, scipy, scikit-image, fast-simplification; `pdftoppm` (poppler-utils) per le anteprime.

## Nota sulle anteprime

Le anteprime PNG sono renderizzate da un build RGB: i visualizzatori PDF mostrano il nero ricco CMYK come un grigio-bruno che in stampa non c'è. Il PDF da caricare su KDP è invece in CMYK, quindi i colori possono differire dall'anteprima.
