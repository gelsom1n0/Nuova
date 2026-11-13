# Checklist copertina KDP

Riferita a `copertina_KDP.pdf`: variante «foto», **132 pagine (`libro/tomo/output/interno_KDP.pdf`, versione definitiva della revisione), carta bianca, interno B/N, nessun autore** (vedi `build_info.json`).
Le fonti dei requisiti sono in `KDP_SPECIFICHE.md`. Verifiche eseguite con `pdfinfo`, `pdffonts`, `pdfimages`, `pypdf`, ispezione visiva delle anteprime e confronto pixel per pixel con l'illustrazione originale.

| # | Voce | Requisito | Valore nel file | Esito |
|---|---|---|---|---|
| 1 | Dimensioni distesa | 0,125 + 6 + dorso + 6 + 0,125 × 9,25 in | **12,5473 × 9,25 in** (903,403 × 666 pt; 318,70 × 234,95 mm) | ✅ conforme alla formula — ⚠️ da confrontare con il calcolatore KDP da browser |
| 2 | Dorso e formula | pagine × 0,002252 in (B/N, carta bianca) | 132 × 0,002252 = **0,2973 in** (7,55 mm) | ✅ — ⚠️ va rigenerata se l'interno cambia ancora |
| 3 | Abbondanze | 0,125 in su alto, basso, lati esterni | l'illustrazione copre l'intera pagina PDF | ✅ |
| 4 | Zona di sicurezza | testo ≥ 0,125 in (A) / ≥ 0,25 in (B) dal rifilo | testo prima/quarta ≥ 0,45 in dal rifilo; formula pH e Cl limitate in automatico | ✅ |
| 5 | Testo sul dorso | ≥ 79 pagine; ≥ 0,0625 in dai bordi del dorso | 132 pagine; corpo 10 pt in 0,172 in utili; caducei larghi 0,17 in | ✅ |
| 6 | Verso del testo sul dorso | dall'alto verso il basso | ruotato −90° | ✅ |
| 7 | Tolleranza piega 0,0625 in | nessun testo a cavallo delle pieghe | testo e caducei centrati nel dorso; fondo continuo ai lati | ✅ |
| 8 | Area barcode libera | 2 × 1,2 in, ≥ 0,25 in da dorso e rifilo, niente testo/immagini sopra | x 3,875–5,875 in, y 0,375–1,575 in: solo fondo navy, nessun testo né oggetto; la formula pH termina ≥ 0,3 in prima | ✅ |
| 9 | Font incorporati | tutti | Gelasio Regular/Italic/Bold (TrueType, subset) | ✅ |
| 10 | Corpo minimo | ≥ 7 pt | minimo **7,0 pt**: pedici e apici di formule ed etichette sono forzati a ≥ 7 pt (`CORPO_MIN`); verificato con pdfplumber su tutti i caratteri | ✅ |
| 11 | Risoluzione | immagini ≥ 300 DPI | illustrazione **327 ppi** (4096 × 3021 px su 12,54 × 9,25 in); caducei 325 ppi | ✅ |
| 12 | Spazio colore | CMYK, niente spot, niente profili | immagini JPEG **DeviceCMYK**; vettori e sfumature DeviceCMYK; nessun RGB, nessun ICC | ✅ |
| 13 | Trasparenze / livelli | appiattiti | nessun ExtGState/SMask/OCG; l'oro dei titoli è una sfumatura ritagliata sul testo (non è trasparenza) | ✅ |
| 14 | Segni di taglio / guide | assenti | guide solo nelle PNG di anteprima | ✅ |
| 15 | Dimensione file | ≤ 650 MB (consigliato ≤ 40 MB) | **~8,2 MB** | ✅ |
| 16 | Protezione | nessuna cifratura | `Encrypted: no` | ✅ |
| 17 | Integrità dell'illustrazione | cuore e oggetti non deformati | scala uniforme, nessuna deformazione; **0 pixel del cuore modificati** rispetto all'upscaling | ✅ |
| 18 | Correttezza dei contenuti | niente errori visibili | formule corrette in italiano (Cockcroft-Gault con «× 0,85 se donna», Henderson-Hasselbalch, Vd = Dose/C₀, Cl = U × V / P); etichette Na⁺ e Ca²⁺ corrette | ✅ |
| 19 | Contenuti vietati | nessun marchio, ente, volto, sangue, nome di autore inventato | nessuno; campo autore vuoto | ✅ |

## Controlli da fare al momento del caricamento

- [x] Numero di pagine dell'interno definitivo: **132** (`pdfinfo libro/tomo/output/interno_KDP.pdf`); copertina rigenerata con `--pagine 132`. Ripetere se l'interno cambia.
- [ ] Confronto di `build_info.json` con il **Cover Calculator** KDP.
- [ ] Nel previewer KDP: barcode nell'area libera, nessun avviso su testo fuori dalla zona sicura o sul dorso.
- [ ] **Dichiarazione sui contenuti generati con IA**: nel flusso di pubblicazione KDP chiede se testi o immagini sono generati con IA. L'illustrazione di copertina lo è, quindi va dichiarata.
- [ ] Cartoncino: **opaco** consigliato (navy scuro e cuore lucido rendono meglio senza riflessi).
