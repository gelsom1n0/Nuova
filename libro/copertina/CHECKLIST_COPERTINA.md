# Checklist copertina KDP

Riferita alla generazione corrente: **128 pagine, carta bianca, interno B/N, nessun autore** (`build_info.json`).
Fonti dei requisiti: `KDP_SPECIFICHE.md`. Verifiche eseguite con `pdfinfo`, `pdffonts`, `pypdf` e ispezione visiva delle anteprime.

| # | Voce | Requisito | Valore nel file | Esito |
|---|---|---|---|---|
| 1 | Dimensioni distesa | 0,125 + 6 + dorso + 6 + 0,125 × 9,25 in | **12,5383 × 9,25 in** (902,754 × 666 pt; 318,47 × 234,95 mm) | ✅ conforme alla formula — ⚠️ da confrontare col calcolatore KDP da browser (non leggibile in automatico) |
| 2 | Dorso e formula | pagine × 0,002252 in (B/N, carta bianca) | 128 × 0,002252 = **0,2883 in** (7,32 mm) | ✅ — ⚠️ **provvisorio**: dipende dal numero di pagine finale |
| 3 | Abbondanze | 0,125 in su alto, basso, lati esterni | sfondo, sfumatura e pattern coprono l'intera pagina PDF | ✅ |
| 4 | Zona di sicurezza | testo ≥ 0,125 in (A) / contenuti ≥ 0,25 in (B) dal rifilo | testo prima/quarta ≥ 0,45 in dal rifilo; motivo centrale ben dentro | ✅ |
| 5 | Testo sul dorso | ≥ 79 pagine; ≥ 0,0625 in dai bordi del dorso | 128 pagine; corpo 9,5 pt (maiuscole ≈ 6,7 pt) in 0,163 in utili | ✅ |
| 6 | Verso del testo sul dorso | convenzione KDP/USA: dall'alto verso il basso | ruotato −90° | ✅ |
| 7 | Tolleranza piega 0,0625 in | nessun testo a cavallo delle pieghe | nessun testo entro 0,0625 in dalle linee del dorso; fondo continuo | ✅ |
| 8 | Area barcode libera | 2 × 1,2 in, ≥ 0,25 in da dorso e rifilo, niente testo/immagini | area a x 3,875–5,875 in, y 0,375–1,575 in: nessun testo, nessuna icona (margine extra 0,12 in) | ✅ — solo fondo a tinta/sfumato, su cui KDP stampa il riquadro bianco |
| 9 | Font incorporati | tutti incorporati | Gelasio Regular/Italic/Bold (TrueType, subset) — nessun font non incorporato (`pdffonts`) | ✅ |
| 10 | Corpo minimo | ≥ 7 pt | minimo 7,4 pt («PRIMA EDIZIONE DI LAVORO») | ✅ |
| 11 | Risoluzione | immagini ≥ 300 DPI | nessuna immagine raster: grafica e testo vettoriali | ✅ |
| 12 | Spazio colore | CMYK, niente spot, niente profili, un solo spazio | solo operatori `k/K` + sfumatura `/DeviceCMYK`; nessun RGB, nessun ICC | ✅ |
| 13 | Trasparenze / livelli | appiattiti | nessun ExtGState, nessuna SMask, nessun OCG; l'«alone» è simulato con tratti pieni | ✅ |
| 14 | Segni di taglio / guide | assenti | guide presenti solo nelle PNG di anteprima | ✅ |
| 15 | Dimensione file | ≤ 650 MB (consigliato ≤ 40 MB) | ~47 KB | ✅ |
| 16 | Protezione | nessuna cifratura | `Encrypted: no` | ✅ |
| 17 | Copertura inchiostro | (buona pratica di stampa, non requisito KDP esplicito) | navy CMYK 92/70/30/25 = TAC 217 %; fondo scuro inferiore più carico ma < 300 % | ✅ buona pratica |
| 18 | Contenuti vietati | nessun marchio, ente, volto, sangue, croce rossa, nome di autore inventato | nessuno; campo autore vuoto | ✅ |
| 19 | Nome file | niente caratteri speciali | `copertina_KDP.pdf` | ✅ |

## Controlli da fare al momento del caricamento

- [ ] Numero di pagine **definitivo** del PDF interno (`pdfinfo libro/tomo/output/<file>.pdf`) e rigenerazione con `--pagine N`.
- [ ] Confronto delle misure in `build_info.json` con il **Cover Calculator** KDP (6 × 9, B/N, carta bianca, N pagine).
- [ ] Nel previewer KDP: barcode posizionato nell'area libera, nessun avviso su testo fuori dalla zona sicura o sul dorso.
- [ ] Scelta del cartoncino: **opaco** consigliato per la variante scura (riduce impronte e riflessi sul navy).
