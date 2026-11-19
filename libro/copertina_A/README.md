# Copertina KDP – «ABC della cardiologia clinica» (volume A)

Copertina per brossura KDP, 7 x 10 in, interno B/N su carta bianca, 290 pagine (provvisorie). Grafica originale procedurale, testo vettoriale Montserrat, CMYK, nessuna trasparenza.

## File

| File | Contenuto |
|---|---|
| `copertina_KDP.pdf` | PDF da caricare su KDP (variante A, CMYK) |
| `copertina_KDP_variante_B.pdf`, `copertina_KDP_variante_C.pdf` | Altre due varianti, stesso formato |
| `copertina_anteprima.png` | Anteprima della distesa con guide (rifilo, bleed, zone di sicurezza 0,125 e 0,25 in, dorso, area barcode) |
| `copertina_anteprima_senza_guide.png`, `prima_di_copertina.png` | Distesa pulita e solo la prima, variante A |
| `anteprime/` | `distesa_{A,B,C}.png`, `distesa_{A,B,C}_guide.png`, `prima_{A,B,C}.png` |
| `build_copertina_A.py` | Generatore (layout, testi, PDF, anteprime) |
| `arte_cuore.py`, `cuore_mesh.py` | Rendering e geometria procedurale del cuore |
| `build_info.json` | Parametri dell'ultimo build (pagine, dorso, dimensioni, area barcode, ecc.) |
| `KDP_SPECIFICHE.md` | Specifiche KDP con fonti |
| `CHECKLIST_COPERTINA.md` | Verifica del file rispetto ai requisiti, e passi per il caricamento |
| `ASSET_E_IA.md` | Origine degli asset e questione della dichiarazione IA |
| `fonts/` | Montserrat (OFL) |
| `sorgenti/` | Maglie del cuore (`cuore_*.npz`); `sorgenti/cache/` = raster dei piatti (ignorata da git) |

## Le tre varianti

- **A, bilanciata (consigliata)**: anatomia del cuore intatta, dissolvenza solo sul lato destro. Anteprima: `anteprime/prima_A.png`.
- **B, frammentata**: triangoli più grandi (1500 facce), dissolvenza più forte, più particelle. Anteprima: `anteprime/prima_B.png`.
- **C, maglia fitta**: 4000 facce, poca dissolvenza. Anteprima: `anteprime/prima_C.png`.

## Rigenerare con un nuovo numero di pagine

```
python3 build_copertina_A.py --pagine N
```

I due piatti raster sono ancorati ai bordi esterni del file: cambiando le pagine cambia solo il dorso, che è vettoriale. La cache dei raster in `sorgenti/cache/` viene quindi riutilizzata (rigenerazione in pochi secondi). La cache è ignorata da git e si ricostruisce da sola se manca (circa 1 minuto per variante). Il build aggiorna anche `build_info.json` e le anteprime.

### Opzioni

| Opzione | Significato |
|---|---|
| `--pagine N` | Numero di pagine (default 290, minimo 24) |
| `--autore "Nome Cognome"` | Nome dell'autore: sulla prima in basso a sinistra, sul dorso nella parte bassa (solo se il dorso ha testo) |
| `--variante A\|B\|C` | Variante del PDF principale `copertina_KDP.pdf` (default A) |
| `--tutte` | Genera anche le altre varianti (`copertina_KDP_variante_X.pdf` + anteprime) |
| `--trim LxA` | Formato di rifilo in pollici (default `7x10`) |
| `--carta bianca\|crema` | Coefficiente del dorso (0,002252 o 0,0025 in per pagina) |
| `--nero ricco\|solo-k` | Nero di fondo: ricco C40 M30 Y30 K100 (default) oppure solo K100 |
| `--colore cmyk\|rgb` | Spazio colore del PDF (default CMYK; RGB solo per prove) |
| `--rigenera-arte` | Ignora la cache e ricalcola i raster |
| `--dpi-anteprima N` | Risoluzione delle anteprime PNG (default 150) |

## Modificare i testi

Le costanti in cima a `build_copertina_A.py`: `KICKER`, `TITOLO_GRANDE`, `TITOLO_RIGA`, `SOTTOTITOLO`, `QUARTA_INTRO`, `QUARTA_PUNTI`, `AVVERTENZA`. Il testo è vettoriale, quindi cambiarlo non richiede di rigenerare l'arte (i raster contengono solo aloni luminosi). Il testo del dorso è nel blocco "DORSO" di `costruisci()`.

## Requisiti

python3, reportlab, numpy, opencv-python-headless, Pillow, scipy, scikit-image, fast-simplification; `pdftoppm` (poppler-utils) per le anteprime.

## Nota sulle anteprime

Le anteprime PNG sono renderizzate da un build RGB: i visualizzatori PDF mostrano il nero ricco CMYK come un grigio-bruno che in stampa non c'è. Il PDF da caricare su KDP è invece in CMYK. Per questo le anteprime possono differire nei colori dal PDF aperto in un visualizzatore.
