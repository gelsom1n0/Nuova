# Checklist copertina KDP – «ABC della cardiologia clinica» (variante A)

File verificato: `copertina_KDP.pdf` (290 pagine, carta bianca, 7 x 10 in, B/N interno). Fonti KDP (lettere A-G) e date di consultazione in `KDP_SPECIFICHE.md` (19 novembre 2026): A = Create a Paperback Cover (G201953020), B = Paperback Submission Guidelines (G201857950), C = Barcodes (G5HDYGP4BXLX4RUW), D = Print Options (G201834180), E = Trim Size, Bleed, Margins (GVBQ3CMEQW3W2VL6), F = Printing Cost (G201834340), G = Content Guidelines/AI (G200672390).

| # | Voce | Requisito (fonte) | Valore nel file | Esito |
|---|---|---|---|---|
| 1 | Dimensioni distesa | Bleed + retro + dorso + fronte + bleed (A); altezza = bleed + rifilo + bleed | 1073,02 x 738 pt = 14,9031 x 10,25 in (378,54 x 260,35 mm); 0,125 + 7 + 0,6531 + 7 + 0,125 | ✅ |
| 2 | Dorso | pagine x 0,002252 in, B/N carta bianca (A, B) | 290 x 0,002252 = 0,65308 in (16,59 mm) | ✅ |
| 3 | Abbondanza (bleed) | 0,125 in (3,2 mm) su tutti i lati (A, B, E) | 0,125 in; fondo e raster ancorati ai bordi esterni, estesi fino al vivo | ✅ |
| 4 | Zona di sicurezza 0,125 in | testo ad almeno 0,125 in dentro il rifilo (A) | Misurato sul PDF (pdfplumber, tutti i caratteri): testo dei piatti a ≥ 0,424 in da rifilo e piega; testo del dorso a ≥ 0,185 in dai bordi del dorso | ✅ |
| 5 | Zona prudente 0,25 in | contenuti importanti ad almeno 0,25 in dal bordo (B) | Tutti i testi >= 0,25 in (misurato: ≥ 0,424 in dal rifilo e dalla piega sui piatti). Solo la linea ECG e le particelle arrivano al vivo, di proposito | ✅ |
| 6 | Testo sul dorso | solo con >= 79 pagine (A; B «more than 79») | 290 pagine: testo presente, max 17 pt | ✅ |
| 7 | Margine testo-dorso | >= 0,0625 in (1,6 mm) per lato (A) | Spessore utile 0,5281 in (13,4 mm); testo misurato a ≥ 0,185 in dai bordi del dorso | ✅ |
| 8 | Variazione sulle pieghe | 0,0625 in per lato (A) | Progettata con tolleranza 0,0625 in; dorso vettoriale in nero pieno che sormonta di 1 pt i raster, nessuno spigolo netto sul dorso | ✅ |
| 9 | Area codice a barre | consigliata 2 x 1,2 in, >= 0,25 in da dorso e rifilo; nessuna immagine o testo nell'area, altrimenti rifiuto (C, A) | x 4,875-6,875 in, y 0,375-1,575 in dal basso: vuota (nessuna grafica, zero caratteri nell'area, verificato); 0,25 in da dorso e rifilo. KDP applica il barcode sul fondo nero: verificare nell'anteprima KDP | ✅ |
| 10 | Font incorporati | incorporare tutti i font (A) | 8 font Montserrat (SemiBold, Black, Bold, Light, Regular, Medium, Italic, Light Italic): TrueType, subset incorporati | ✅ |
| 11 | Corpo minimo | 7 pt (A); B non indica minimo per la copertina | Minimo 7,13 pt (misurato sul PDF; pedici e apici delle formule non scendono sotto il minimo) | ✅ |
| 12 | Risoluzione immagini | >= 300 DPI, 100 % (A, B) | 2 raster 2850 x 4100 px a 400 ppi, uno per piatto | ✅ |
| 13 | Spazio colore | CMYK; niente spot; evitare profili e spazi misti (A) | Raster CMYK JPEG; nessun operatore RGB, nessuno spot, nessun profilo ICC, nessuno shading | ✅ |
| 14 | Trasparenze | appiattire (A, B) | Nessun ExtGState/SMask: le sfumature dell'ECG sono segmenti di colore pieno; gli aloni luminosi sono nel raster; le formule di sfondo sono grigio pieno #595959 (bianco al 35 %), non trasparenza | ✅ |
| 15 | Crop marks, guide, template | da rimuovere (A, B) | Assenti: il PDF di stampa è costruito con `con_guide=False`; le guide esistono solo nelle anteprime `*_guide.png` | ✅ |
| 16 | Dimensione file | max 650 MB, consigliati <= 40 MB (A, B) | circa 8,7 MB | ✅ |
| 17 | Cifratura | PDF non protetto (A, B) | Non cifrato | ✅ |
| 18 | Aree nere estese | KDP non dà alcun valore (nessuna regola su rich black o TAC) | Scelta di progetto: nero ricco C40 M30 Y30 K100 (TAC 200 %), identico nel raster e nel dorso vettoriale; TAC massimo del raster 259 % (tetto 260 %). Rischio: il fuori registro può creare aloni sul testo bianco piccolo "in negativo" su nero ricco; il testo più piccolo (formule di sfondo, pedici) arriva a 7,13 pt, ma è grigio #595959 su nero. Opzione `--nero solo-k` (K100) disponibile | ⚠️ |
| 19 | Originalità | nessuna copia di copertine esistenti | Grafica e layout originali; la copertina di riferimento non è stata copiata (vedi `ASSET_E_IA.md`) | ✅ |
| 20 | Dichiarazione IA | G: dichiarare i contenuti «AI-generated» | Arte procedurale scritta in codice: decisione dell'autore, vedi `ASSET_E_IA.md` | ⚠️ |
| 21 | Correttezza scientifica delle annotazioni | Le etichette devono corrispondere al tipo di tracciato | Sigle P, Q, R, S, T sul primo complesso, ciascuna sulla propria deflessione (P e T onde positive lente, Q negativa prima di R, R picco, S negativa dopo R). Formule coerenti: FC = 60/RR; QTc = QT/√RR (Bazett); PAM = PAD + (PAS − PAD)/3; GC = FC · GS; FE = (VTD − VTS)/VTD; RVS = (PAM − PVC)/GC; E_K = 61,5 · log([K⁺]e/[K⁺]i) (Nernst a 37 °C, mV). Revisione finale da parte dell'autore consigliata | ⚠️ |

Le righe 18 e 20 sono ⚠️ perché dipendono da una scelta dell'autore; la 21 perché richiede la conferma scientifica dell'autore. Nessuna indica un file fuori specifica.

## Da fare al caricamento

1. **Numero di pagine finale**: il 290 è provvisorio. Con il valore definitivo rigenerare (`python3 build_copertina_A.py --pagine N`, vedi `README.md`) e caricare il nuovo PDF. KDP arrotonda per eccesso a pari se necessario (B).
2. **Cover Calculator**: confrontare larghezza, altezza e dorso con https://kdp.amazon.com/en_US/cover-calculator in un browser (non verificabile automaticamente). Atteso per 290 pagine: 14,903 x 10,25 in, dorso 0,653 in.
3. **Anteprima KDP (previewer)**: controllare in KDP che il barcode cada sul retro senza coprire grafica o testo, che il testo del dorso sia centrato e che nulla sia tagliato.
4. **Dichiarazione IA**: rispondere alla domanda di KDP in fase di pubblicazione secondo la decisione presa (vedi `ASSET_E_IA.md`).
5. **Carta e finitura** (solo suggerimento, a scelta dell'autore): KDP indica che la finitura lucida «makes black covers darker and artwork more striking» (D), utile per un fondo quasi interamente nero con grafica rossa luminosa. L'opaco è più sobrio e riflette meno, ma può rendere meno profondo il nero; segni e graffi sui fondi scuri possono essere più visibili sul nero lucido. Nessuna delle due è prescritta da KDP.
6. **Costo di stampa**: 7 x 10 in è «large trim» (oltre 6,12 in di larghezza o 9 in di altezza), con costo per pagina più alto (nero, 110-828 pagine su Amazon.com: 0,017 USD/pag. contro 0,012 USD/pag.); controllare le tabelle complete nella pagina F. Bleed e finitura della copertina non cambiano il costo.
