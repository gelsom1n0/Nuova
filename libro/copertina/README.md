# Copertina KDP – «Basi di farmacologia clinica»

Copertina distesa (quarta + dorso + prima) per brossura KDP 6 × 9 in, interno B/N su carta bianca.

**File da caricare su KDP: `copertina_KDP.pdf`**, che corrisponde alla variante «foto». È costruita sull'illustrazione fornita dall'utente (cuore anatomico, molecole, ECG, sfere ioniche) con tutto il testo in vettoriale.
Le due varianti interamente vettoriali (`copertina_KDP_scura.pdf`, `copertina_KDP_chiara.pdf`) restano disponibili come alternative.

## File

| File | Contenuto |
|---|---|
| `copertina_KDP.pdf` | **file da caricare**: variante foto, CMYK, ~327 dpi, font incorporati |
| `copertina_anteprima.png` | distesa con guide: rifilo (rosso), dorso (magenta), sicurezza 0,125 in (azzurro), margine prudente 0,25 in (grigio), area barcode (arancio) |
| `copertina_anteprima_senza_guide.png` | distesa senza guide |
| `prima_di_copertina.png` | solo prima di copertina, al rifilo (utile anche per promozione) |
| `build_info.json` | misure dell'ultima generazione della variante foto |
| `prepara_sfondo_foto.py` | stadio A (una volta sola): toglie il testo raster dall'illustrazione |
| `build_copertina_foto.py` | stadio B (a ogni cambio di pagine/autore): compone il PDF |
| `sorgenti_immagine/` | illustrazione originale (1024 px), upscaling 4K, sfondo ripulito, caduceo, maschera |
| `build_copertina.py`, `copertina_KDP_scura.pdf`, `copertina_KDP_chiara.pdf`, `copertina_KDP_vettoriale.pdf`, `build_info_vettoriale.json`, `anteprime/distesa_scura*`, `anteprime/distesa_chiara*` | varianti vettoriali alternative |
| `KDP_SPECIFICHE.md`, `CHECKLIST_COPERTINA.md` | requisiti ufficiali con fonti ed esiti |

Requisiti: Python 3, `reportlab`, `numpy`, `Pillow`, `opencv-python-headless` (solo per lo stadio A), `pdftoppm` (poppler-utils) per le PNG.

## Come è stata costruita la variante foto

1. **Upscaling.** L'illustrazione originale è di 1024 × 755 px, pari a circa 82 dpi sulla copertina reale (KDP chiede almeno 300). È stata ingrandita a 4096 × 3021 px con l'upscaler di Higgsfield (`bytedance_image_upscale`, 2 crediti). Il risultato è di circa 327 dpi su 9,25 in di altezza. L'upscaler non ridisegna l'immagine: il cuore è lo stesso, solo più definito.
2. **Rimozione del testo raster** (`prepara_sfondo_foto.py`). Il testo era "cotto" nell'immagine, tagliato dal dorso in quarta e troncato a destra nel sottotitolo. Le formule contenevano errori ("age", "weight", "if female", "Ca°°"). Il testo è stato tolto solo nelle aree di testo, in due modi:
   - con un riempimento armonico e la grana del fondo, dove c'era solo sfondo;
   - con una maschera dei soli pixel del lettering, dove il testo toccava cuore e molecole.

   **Verifica oggettiva: 0 pixel del cuore modificati.** Il controllo confronta i pixel rossi e dei vasi con l'originale.
3. **Composizione** (`build_copertina_foto.py`). L'illustrazione non viene mai deformata: ha una scala unica, con l'altezza a 9,25 in.
   - È divisa in due metà: la quarta è ancorata al bordo sinistro, la prima al bordo destro. Al variare delle pagine i due piatti restano identici rispetto al proprio rifilo.
   - Il dorso è una fascia vettoriale della larghezza esatta, con la sfumatura campionata dall'illustrazione.
   - Sul dorso ci sono il titolo vettoriale e i due caducei, ridotti per rispettare il margine KDP di 0,0625 in.
   - Tutto il testo è vettoriale (Gelasio, OFL) nelle stesse posizioni del modello: titoli in oro con sfumatura, formule corrette in italiano, etichette corrette sulle sfere Na⁺ e Ca²⁺.

## Rigenerare quando cambia il numero di pagine

```bash
pdfinfo ../tomo/output/interno_KDP.pdf | grep Pages    # oggi: 132
python3 build_copertina_foto.py --pagine 132           # ricalcola dorso, larghezza, barcode
```

Lo stadio A **non** va rieseguito: non dipende dal numero di pagine. Dopo la rigenerazione:

1. confronta `build_info.json` con il Cover Calculator KDP;
2. guarda `copertina_anteprima.png`;
3. fai commit di PDF, PNG e `build_info.json`.

Esempio: con 132 pagine il dorso è 0,2973 in e la larghezza 12,5473 in; passando a 140 pagine diventerebbero 0,3153 in e 12,5653 in. **Una copertina generata per un numero di pagine diverso da quello dell'interno viene respinta da KDP.**

Con meno di ~75 pagine il dorso diventa più stretto della giunzione tra le due metà. Lo script avvisa; in quel caso va rivisto il taglio (`SPLIT`).

Opzioni: `--carta crema` (0,0025 in/pagina), `--colore rgb` solo per prove a schermo.

## Aggiungere l'autore

```bash
python3 build_copertina_foto.py --pagine 132 --autore "Nome Cognome"
```

Il nome compare in maiuscolo spaziato in basso sulla prima, sopra «Prima edizione di lavoro», e sul dorso nella metà inferiore, in avorio.

## Modificare i testi

I testi sono costanti in testa a `build_copertina_foto.py` (sezione «Testi»). Le formule sono definite come liste (`CLCR_BREVE`, `PH`, `VD`, `CL`…) e vengono impaginate dal mini-impaginatore `Formula`. Dopo modifiche lunghe ricontrolla nell'anteprima con guide che la quarta non si avvicini all'area barcode.
