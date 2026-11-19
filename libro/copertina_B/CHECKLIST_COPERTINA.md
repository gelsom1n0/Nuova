# Checklist copertina KDP – «ABC della farmacologia clinica» (variante A)

File verificato: `copertina_KDP.pdf` (290 pagine, carta bianca, 7 x 10 in, B/N interno). Le fonti KDP (lettere A-G) e le date di consultazione sono in `../copertina_A/KDP_SPECIFICHE.md` (stesso formato di rifilo, stesse regole; 19 novembre 2026): A = Create a Paperback Cover, B = Paperback Submission Guidelines, C = Barcodes, D = Print Options, E = Trim Size, Bleed, Margins, F = Printing Cost, G = Content Guidelines/AI. Le tre varianti (`copertina_KDP.pdf` = A, `_variante_B.pdf`, `_variante_C.pdf`) hanno le stesse dimensioni e gli stessi parametri.

| # | Voce | Requisito (fonte) | Valore nel file | Esito |
|---|---|---|---|---|
| 1 | Dimensioni distesa | Bleed + retro + dorso + fronte + bleed (A); altezza = bleed + rifilo + bleed | 1073,02 x 738 pt = 14,9031 x 10,25 in; 0,125 + 7 + 0,6531 + 7 + 0,125 | ✅ |
| 2 | Dorso | pagine x 0,002252 in, B/N carta bianca (A, B) | 290 x 0,002252 = 0,6531 in (16,59 mm) | ✅ |
| 3 | Abbondanza (bleed) | 0,125 in su tutti i lati (A, B, E) | 0,125 in; fondo e raster ancorati ai bordi esterni, estesi fino al vivo | ✅ |
| 4 | Zona di sicurezza 0,125 in | testo ad almeno 0,125 in dentro il rifilo (A) | Misurato sul PDF (pdfplumber, tutti i caratteri, tutte e 3 le varianti): testo dei piatti a ≥ 0,62 in da rifilo e piega | ✅ |
| 5 | Zona prudente 0,25 in | contenuti importanti ad almeno 0,25 in dal bordo (B) | Testi a ≥ 0,62 in dal bordo (misurato); solo il tracciato e le particelle arrivano al vivo, di proposito | ✅ |
| 6 | Testo sul dorso | solo con >= 79 pagine (A, B) | 290 pagine: testo presente («ABC» azzurro + «DELLA FARMACOLOGIA CLINICA» bianco) con piccola icona a capsula | ✅ |
| 7 | Margine testo-dorso | >= 0,0625 in per lato (A) | Spessore 0,6531 in; testo del dorso misurato a ≥ 0,185 in dai bordi del dorso | ✅ |
| 8 | Variazione sulle pieghe | 0,0625 in per lato (A) | Dorso vettoriale in nero pieno che sormonta di 1 pt i raster; nessuno spigolo netto in corrispondenza delle pieghe | ✅ |
| 9 | Area codice a barre | 2 x 1,2 in, >= 0,25 in da dorso e rifilo; nessuna immagine o testo nell'area (C, A) | x 4,875-6,875 in, y 0,375-1,575 in dal basso: libera. Nella variante A la linea farmacocinetica attraversa la quarta 0,33 in sopra l'area barcode | ✅ |
| 10 | Font incorporati | tutti i font incorporati (A) | Montserrat SemiBold, Black, Bold, Light, Regular, Medium, Italic: TrueType, subset incorporati | ✅ |
| 11 | Corpo minimo | 7 pt (A) | Minimo 8,5 pt | ✅ |
| 12 | Risoluzione immagini | >= 300 DPI, 100 % (A, B) | 2 raster CMYK JPEG 2850 x 4100 px a 400 ppi, uno per piatto | ✅ |
| 13 | Spazio colore | CMYK; niente spot né profili misti (A) | Nessun operatore RGB, nessuno spot, nessun profilo ICC | ✅ |
| 14 | Trasparenze | appiattire (A, B) | Nessun ExtGState: nessuna trasparenza; gli aloni luminosi sono nel raster | ✅ |
| 15 | Crop marks, guide, template | da rimuovere (A, B) | Assenti dal PDF di stampa; le guide esistono solo nelle anteprime `*_guide.png` | ✅ |
| 16 | Dimensione file | max 650 MB, consigliati <= 40 MB (A, B) | 7,6 MB (A), 8,1 MB (B), 7,8 MB (C) | ✅ |
| 17 | Cifratura | PDF non protetto (A, B) | Non cifrato | ✅ |
| 18 | Aree nere estese | KDP non dà alcun valore (nessuna regola su rich black o TAC) | Scelta di progetto: nero ricco C40 M30 Y30 K100 (TAC 200 %), identico nel raster e nel dorso vettoriale; TAC massimo del raster 211 %. Opzione `--nero solo-k` (K100) disponibile. Rischio residuo: fuori registro su testo bianco piccolo in negativo (minimo 8,5 pt) | ⚠️ |
| 19 | Originalità | nessuna copia di copertine, marchi o impronte di farmaci reali | Grafica e layout originali; nessun farmaco, marchio o colore di medicinali reali | ✅ |
| 20 | Dichiarazione IA | G: dichiarare i contenuti «AI-generated» | Arte procedurale scritta in codice: decisione dell'autore, vedi `ASSET_E_IA.md` | ⚠️ |

Le righe 18 e 20 sono ⚠️ perché dipendono da una scelta dell'autore, non perché il file sia fuori specifica.

## Da fare al caricamento

1. **Confermare sottotitolo e testi di quarta**: sono testi di lavoro (sottotitolo riusato da «Basi di farmacologia clinica»; elenco di principi PK/PD, vie e interazioni, classi di farmaci, schede rapide e checklist). Verificarli sul contenuto finale del volume B (classi effettivamente trattate, in particolare insuline e altri ipoglicemizzanti), correggere le costanti in `build_copertina_B.py` e rigenerare.
2. **Numero di pagine finale**: il 290 è provvisorio. Rigenerare con `python3 build_copertina_B.py --pagine N` (vedi `README.md`) e caricare il nuovo PDF. KDP arrotonda per eccesso a pari se necessario (B).
3. **Autore**: se va indicato, rigenerare con `--autore "Nome Cognome"`; oggi lo slot è vuoto.
4. **Cover Calculator**: confrontare larghezza, altezza e dorso con https://kdp.amazon.com/en_US/cover-calculator in un browser (non verificabile automaticamente). Atteso per 290 pagine: 14,903 x 10,25 in, dorso 0,653 in.
5. **Anteprima KDP (previewer)**: controllare che il barcode cada sul retro senza coprire grafica o testo (nella variante A la linea farmacocinetica passa 0,33 in sopra l'area), che il testo del dorso sia centrato e che nulla sia tagliato.
6. **Dichiarazione IA**: rispondere alla domanda di KDP secondo la decisione presa (vedi `ASSET_E_IA.md`).
7. **Scelta della variante**: A è consigliata; se si preferisce B o C, rigenerare con `--variante B|C` o caricare il PDF `copertina_KDP_variante_X.pdf` già pronto.
8. **Carta e finitura** (suggerimento, a scelta dell'autore): KDP indica che la finitura lucida rende i neri più scuri e la grafica più incisiva (D), utile per un fondo quasi interamente nero con grafica azzurra luminosa; l'opaco è più sobrio e riflette meno. Nessuna delle due è prescritta.
9. **Costo di stampa**: 7 x 10 in è «large trim», con costo per pagina più alto; controllare le tabelle nella pagina F (vedi `../copertina_A/KDP_SPECIFICHE.md`).
