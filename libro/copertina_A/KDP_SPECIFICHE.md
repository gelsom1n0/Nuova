# Specifiche KDP per la copertina 7 x 10 in (B/N, carta bianca)

Consultazione: **19 novembre 2026**, pagine Help ufficiali `kdp.amazon.com` (en_US), lette con web fetch. Dove la pagina non dice nulla è scritto esplicitamente.

Pagine fonte: A = https://kdp.amazon.com/en_US/help/topic/G201953020 (Create a Paperback Cover) · B = https://kdp.amazon.com/en_US/help/topic/G201857950 (Paperback Submission Guidelines) · C = https://kdp.amazon.com/en_US/help/topic/G5HDYGP4BXLX4RUW (Barcodes) · D = https://kdp.amazon.com/en_US/help/topic/G201834180 (Print Options) · E = https://kdp.amazon.com/en_US/help/topic/GVBQ3CMEQW3W2VL6 (Trim Size, Bleed, Margins) · F = https://kdp.amazon.com/en_US/help/topic/G201834340 (Paperback Printing Cost) · G = https://kdp.amazon.com/en_US/help/topic/G200672390 (Content Guidelines, AI)

## Formato 7 x 10 in
| Voce | Valore | Fonte |
|---|---|---|
| 7" x 10" supportato in brossura | Sì, elencato tra i "Large Trim Sizes" (tabella US) | E |
| Pagine, nero su carta bianca | 24–828 (7x10 segue l'intervallo "most sizes") | E |
| Carta crema / groundwood | 24–776 / 24–812 | E |
| Pagine pari | arrotondate per eccesso a pari se necessario | B |
| "Large trim" | Sì: «more than 6.12 inches (155.5 mm) in width or more than 9 inches (228.6 mm) in height» | D, E, F |
| Conseguenze | Costi di stampa diversi: formula «Fixed cost + (page count * per page cost)»; nero 110–828 pag. su Amazon.com: 0,012 USD/pag. (regular) vs 0,017 USD/pag. (large). Le tabelle complete di costo fisso non sono state estratte: controllare la pagina F. Su carta e distribuzione per il large trim le pagine lette non dicono nulla di specifico. Bleed e finitura copertina non cambiano il costo (F). | F |

## Copertina
| Voce | Valore | Fonte |
|---|---|---|
| Abbondanza | 0,125 in (3,2 mm) su alto, basso e lati esterni; «required on all sides» | A, B, E |
| Larghezza | Bleed + larghezza retro + dorso + larghezza fronte + Bleed | A |
| Altezza | Bleed + altezza rifilo + Bleed = 10,25 in (260,35 mm) | A |
| Dorso B/N carta bianca | pagine × 0,002252 in (0,0572 mm) | A, B |
| Dorso B/N carta crema | pagine × 0,0025 in (0,0635 mm) | A |
| Dorso colore premium / standard | 0,002347 / 0,002252 in | A |
| Testo sul dorso | almeno 79 pagine (80 con Cover Creator/Studio); B: «more than 79» | A, B |
| Margine testo-bordo dorso | almeno 0,0625 in (1,6 mm) | A |
| Variazione sulle pieghe | 0,0625 in (1,6 mm) per lato | A |
| Spostamento dorso accettato | la pagina scrive «up to 0.0125" (3.2mm)»: valori incoerenti (0,0125 in = 0,32 mm). Da non usare come riferimento; progettare con 0,0625 in di tolleranza. Spigoli netti sul dorso sconsigliati | A |
| Zona di sicurezza | testo ad almeno 0,125 in (3,2 mm) dentro il rifilo, fuori dal dorso (A); contenuti da non perdere ad almeno 0,25 in (6,4 mm) dal bordo esterno (B) | A, B |
| Barcode | consigliato 2 × 1,2 in (50,8 × 30,5 mm); minimo 1,4 × 0,8 in (35,56 × 20,3 mm); almeno 0,25 in (6,3 mm) da dorso e rifilo; 100 % nero (non CMYK/RGB né registro), fondo bianco pieno, dritto; «Covers with images or text in the barcode location will be rejected»; se non fornito lo mette KDP sul retro | C, A |
| File | un solo PDF retro+dorso+fronte; max 650 MB (consigliati ≤ 40 MB) | A, B |
| Immagini | min 300 DPI (max consigliato 600), dimensione 100 %, CMYK, appiattite | A, B |
| Colori | niente spot (convertire in CMYK); evitare profili colore e spazi misti | A |
| Font | incorporare tutti i font. Corpo minimo 7 pt: A lo indica per la copertina; B dice che per la copertina non è indicato un minimo (il 7 pt vale per l'interno). Usare ≥ 7 pt per prudenza | A, B |
| Trasparenze | appiattire tutte le trasparenze | A, B |
| Da rimuovere | crop/trim marks, barre colore, testo del template, segnalibri, commenti; PDF non protetti/cifrati | A, B |
| Linee/grigi | (B, interno) riempimenti grigi min 10 %, linee min 0,75 pt; non riferito alla copertina | B |
| Finitura | cartoncino 80 lb (220 g/m²) bianco, lucido o opaco; «Glossy finish ... makes black covers darker and artwork more striking» | D |

## Aree nere / inchiostro totale / rich black
**KDP non indica un valore.** Né A né B né D danno indicazioni su aree nere estese, rich black, copertura totale di inchiostro (TAC) o limiti di inchiostro per la copertina. L'unico riferimento tangente: contrasto testo/sfondo (A: «If the colors are too similar, the text might blend into the background») e la nota D sulla finitura lucida che scurisce i neri. A tratta la variazione di colore come dovuta a fattori ambientali e meccanici. Pagine di troubleshooting specifiche non trovate nelle fonti lette. Le scelte (es. nero CMYK 0/0/0/100 oppure rich black) sono quindi decisioni di progetto non supportate da una regola KDP.

## Dichiarazione contenuti AI (G)
- **AI-generated** (da dichiarare in fase di pubblicazione o di modifica): uso di uno strumento AI per creare il contenuto vero e proprio (testo, immagini, traduzioni), «even if you applied substantial edits afterwards».
- **AI-assisted** (non da dichiarare): contenuto creato dall'autore e migliorato con AI (modifica, revisione, controllo errori, brainstorming se poi crea lui testo/immagini).
- In entrambi i casi l'autore è responsabile della conformità alle linee guida. Un'immagine di copertina generata da AI ricade quindi in "AI-generated".

## Calcolo per 290 pagine, carta bianca, trim 7 x 10 in
- Dorso: 290 × 0,002252 = **0,65308 in = 16,59 mm**
- Distesa: 0,125 + 7 + 0,65308 + 7 + 0,125 = **14,90308 in = 378,54 mm** di larghezza; altezza 10,25 in = 260,35 mm.

- Con carta crema: dorso 0,725 in (18,42 mm), larghezza 14,975 in.
- Il numero di pagine è provvisorio: ricalcolare con il valore finale e confrontare con il Cover Calculator (https://kdp.amazon.com/en_US/cover-calculator, non verificabile automaticamente).
- Testo sul dorso consentito (290 > 79). Spessore utile per il testo: 16,59 − 2 × 1,6 mm = 13,4 mm.
