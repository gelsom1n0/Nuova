# Copertina KDP – «Basi di farmacologia clinica»

Copertina distesa (quarta + dorso + prima) per brossura KDP 6 × 9 in, interno B/N su carta bianca.
Tutto vettoriale, generato da `build_copertina.py` (ReportLab), font Gelasio (OFL) incorporati, colori CMYK.

## File

| File | Contenuto |
|---|---|
| `copertina_KDP.pdf` | **file da caricare** (variante raccomandata: scura navy/oro) |
| `copertina_KDP_scura.pdf` / `copertina_KDP_chiara.pdf` | le due varianti |
| `copertina_anteprima.png` | distesa con guide: rifilo (rosso), dorso (magenta), sicurezza 0,125 in (azzurro), margine prudente 0,25 in (grigio), area barcode (arancio) |
| `copertina_anteprima_senza_guide.png` | distesa senza guide |
| `prima_di_copertina.png` | solo prima di copertina, al rifilo (utile anche come immagine promozionale) |
| `anteprime/` | anteprime di entrambe le varianti |
| `build_info.json` | misure dell'ultima generazione |
| `fonts/` | Gelasio in TTF (convertito dai WOFF2 di `libro/engine/fonts/`) + licenza OFL |
| `KDP_SPECIFICHE.md`, `CHECKLIST_COPERTINA.md` | requisiti ufficiali con fonti ed esiti |

Requisiti: Python 3, `reportlab`, `pdftoppm` (poppler-utils) per le PNG.

## Rigenerare quando cambia il numero di pagine

```bash
pdfinfo ../tomo/output/tomo_bozza.pdf | grep Pages     # leggi il numero definitivo
python3 build_copertina.py --pagine 136                # ricalcola dorso e larghezza
```

Lo script ricalcola dorso (`pagine × 0,002252 in`), larghezza totale, posizione di prima/dorso, area barcode, e decide da solo se scrivere il testo sul dorso (≥ 79 pagine). Poi:

1. controlla le misure in `build_info.json` contro il Cover Calculator KDP;
2. guarda `copertina_anteprima.png`;
3. fai commit di PDF, PNG e `build_info.json`.

Esempio: 128 → 136 pagine fa passare il dorso da 0,2883 a 0,3063 in e la larghezza da 12,5383 a 12,5563 in. **Una copertina generata per un numero di pagine diverso da quello dell'interno viene respinta da KDP** (o stampata con il dorso fuori posto).

Opzioni utili:

- `--carta crema` se si sceglie carta crema (0,0025 in/pagina);
- `--raccomandata chiara` per far diventare `copertina_KDP.pdf` la variante chiara;
- `--colore rgb` solo per prove a schermo (KDP chiede CMYK).

## Aggiungere l'autore

```bash
python3 build_copertina.py --pagine 128 --autore "Nome Cognome"
```

Il nome compare in maiuscolo spaziato sulla prima (sopra «Prima edizione di lavoro»), sul dorso (in oro, nella metà inferiore, se il dorso ha testo) e nei metadati del PDF. Per più autori: `--autore "Nome Cognome, Nome Cognome"`.

## Modificare i testi

Titolo, sottotitolo, etichetta, testo di quarta, punti elenco e avvertenza sono costanti in testa a `build_copertina.py` (sezione «Testi»). Il titolo si adatta in automatico alla larghezza disponibile; il testo di quarta va a capo da solo. Dopo modifiche lunghe ricontrolla che la quarta non scenda verso l'area barcode (nell'anteprima con guide).
