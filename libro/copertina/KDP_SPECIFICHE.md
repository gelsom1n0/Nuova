# Specifiche KDP per la copertina in brossura

Consultazione: **13 novembre 2026**, pagine Help ufficiali su `kdp.amazon.com` (versione `en_US`).
Le citazioni sono brevi estratti testuali; il resto è parafrasato.

## Pagine fonte

| Sigla | Pagina | URL |
|---|---|---|
| **A** | Create a Paperback Cover | https://kdp.amazon.com/en_US/help/topic/G201953020 |
| **B** | Paperback Submission Guidelines | https://kdp.amazon.com/en_US/help/topic/G201857950 |
| **C** | Barcodes | https://kdp.amazon.com/en_US/help/topic/G5HDYGP4BXLX4RUW |
| **D** | Print Options (carta, formati) | https://kdp.amazon.com/en_US/help/topic/G201834180 |
| **E** | Set Trim Size, Bleed, and Margins (interno) | https://kdp.amazon.com/en_US/help/topic/GVBQ3CMEQW3W2VL6 |
| **F** | Cover Calculator | https://kdp.amazon.com/en_US/cover-calculator |

> **F non utilizzabile:** il calcolatore ha risposto con «A system error occurred» e non ha restituito né le misure né il template scaricabile. Le misure sono state calcolate con le formule ufficiali di A/B. **Prima del caricamento conviene confrontarle con il calcolatore aperto da browser** (vedi checklist).

## Valori

| Voce | Valore ufficiale | Fonte | Valore usato nel progetto |
|---|---|---|---|
| Larghezza distesa | «Bleed + Back Cover Width + Spine Width + Front Cover Width + Bleed» | A, B | 0,125 + 6 + dorso + 6 + 0,125 in |
| Altezza distesa | «Bleed + Trim Height + Bleed» | A, B | 0,125 + 9 + 0,125 = **9,25 in** |
| Abbondanza (bleed) | 0,125 in (3,2 mm) su alto, basso e lati esterni; «required on all sides» | A, B | 0,125 in; lo sfondo copre tutta la distesa |
| Dorso, B/N carta bianca | pagine × **0,002252 in** (0,0572 mm) | A, B | **coefficiente confermato** (default) |
| Dorso, B/N carta crema | pagine × 0,0025 in (0,0635 mm) | A, B | opzione `--carta crema` |
| Dorso, colore standard / premium | 0,002252 / 0,002347 in (B riporta solo 0,002347) | A, B | non pertinente (interno B/N) |
| Testo sul dorso: pagine minime | «at least 79 pages» (in un altro passo «more than 79»; Cover Creator: 80) | A | soglia 79 nello script; con 128 pagine nessuna ambiguità |
| Margine testo/bordi del dorso | almeno 0,0625 in (1,6 mm) | A, B | 0,0625 in per lato |
| Tolleranza di piega | 0,0625 in per lato delle linee del dorso | A, B | nessun testo entro 0,0625 in dalle pieghe |
| Spostamento del dorso accettato | «up to 0.0125"» (il valore in mm, 3,2 mm, fa pensare a 0,125 in: incongruenza nella pagina) | A | colori del dorso poco contrastati rispetto ai piatti nella variante scura |
| Zona di sicurezza (testo) | almeno 0,125 in dentro il rifilo | A | guida a 0,125 in |
| Zona di sicurezza (contenuti da non rifilare) | almeno 0,25 in dal bordo esterno | B | **adottato il valore più restrittivo**: tutto il testo è ad almeno 0,45 in dal rifilo |
| Cornici | se usate, almeno 0,25 in dentro il rifilo; sconsigliate | A | nessuna cornice |
| Barcode: dimensione | suggerita 2 × 1,2 in (50,8 × 30,5 mm); minima 1,4 × 0,8 in | C | area riservata 2 × 1,2 in |
| Barcode: posizione | almeno 0,25 in dal dorso e dal rifilo; angolo in basso (a destra per i libri sinistra→destra, implicito: la pagina cita esplicitamente solo il caso destra→sinistra) | C, A | x = 3,875 in, y = 0,375 in dal bordo inferiore del file (= 0,25 in dal rifilo e dal dorso) |
| Barcode: altro | nero 100 %, fondo bianco pieno; se non lo si fornisce lo aggiunge KDP; «Covers with images or text in the barcode location will be rejected» | C | area lasciata **senza testo né icone**; nessun barcode inserito (lo aggiunge KDP) |
| Formato file | un solo PDF con quarta, dorso e prima | A | PDF a pagina singola |
| Dimensione file | max 650 MB; consigliati ≤ 40 MB | A, B | ~47 KB |
| Risoluzione immagini | minimo 300 DPI (massimo consigliato 600 DPI) | A, B | nessuna immagine raster: tutto vettoriale |
| Spazio colore | «Images should be in CMYK color»; sconsigliato mischiare spazi colore; sconsigliati i profili colore incorporati | A | **solo DeviceCMYK**, nessun profilo ICC |
| Colori spot | non ammessi | A | nessuno |
| Font | incorporare tutti i font; corpo minimo **7 pt** | B | Gelasio incorporato (subset TrueType); corpo minimo usato 7,4 pt |
| Trasparenze / livelli | «Flatten all transparencies»; livelli appiattiti | A, B | nessuna trasparenza (nessun ExtGState/SMask), nessun livello OCG |
| Segni di taglio ecc. | rimuovere crop/trim marks, barre colore, testo del template, segnalibri, commenti, annotazioni | A, B | assenti nel PDF di stampa (le guide esistono solo nelle PNG di anteprima) |
| Sicurezza file | niente PDF protetti/cifrati | B | non cifrato |
| Nome file | niente emoji o caratteri speciali | B | `copertina_KDP.pdf` |
| Cartoncino copertina | 80 lb (220 g/m²) bianco, lucido o opaco | D | scelta in fase di caricamento (consigliato **opaco** per la variante scura) |
| Pagine ammesse (B/N, 6×9) | 24–828 | D | minimo 24 controllato dallo script |

## Note sulle discrepanze nelle pagine KDP

1. **Soglia testo sul dorso** 79 vs «più di 79» vs 80 (Cover Creator): irrilevante con 128 pagine; diventa rilevante solo se l'interno scendesse a 79–80 pagine.
2. **Zona di sicurezza** 0,125 in (A) vs 0,25 in (B): applicato 0,25 in come limite operativo.
3. **Calcolatore** non raggiungibile in modo automatico: verificare a mano le misure finali (vedi checklist, voce 1).
