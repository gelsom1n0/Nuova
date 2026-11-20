# Asset e origine – copertina «ABC della cardiologia clinica»

## Elenco degli asset

| Asset | Origine | Note |
|---|---|---|
| Cuore anatomico a maglia low-poly | Procedurale, originale. `cuore_mesh.py`: campo di distanza implicito (smooth-min di ellissoidi e tubi per ventricoli, atri, aorta, tronco polmonare, vene), superficie estratta con marching cubes, decimata con decimazione quadrica (`fast-simplification`). Maglie salvate in `sorgenti/cuore_*.npz` | Nessuno strumento di generazione di immagini |
| Rendering del cuore (spigoli, nodi, particelle, bagliore, mappatura tonale) | Procedurale, originale. `arte_cuore.py` (NumPy, OpenCV) | Rendering proprio, non un modello di immagini |
| Rete low-poly dell'angolo del retro, ECG, polvere luminosa, alone del titolo | Procedurali (`build_copertina_A.py`, SciPy Delaunay, OpenCV, Pillow) | Alone del titolo calcolato dal font |
| Font | Montserrat (SIL Open Font License), `fonts/` con `OFL.txt` | Incorporati nel PDF come subset |
| Montserrat Light Italic (`fonts/Montserrat-LightItalic.ttf`) | Istanza statica wght 300 generata con fontTools dal font variabile ufficiale OFL `google/fonts`, `ofl/montserrat/Montserrat-Italic[wght].ttf` (stesso file del Volume B). Nessun font di terzi non OFL | Usato per sigle ECG e formule di sfondo |
| Sigle delle onde ECG e formule di sfondo | Testo vettoriale scritto per il libro (`onde_ecg`, `FORMULE_PRIMA`, `FORMULE_QUARTA`); formule standard di fisiologia, nessuna fonte di terzi | Contenuto scientifico da rivedere a cura dell'autore |
| Testi (titolo, sottotitolo, quarta, avvertenza) | Scritti per il libro; costanti in `build_copertina_A.py` | |
| Immagini stock, illustrazioni o elementi di terzi | Nessuno | |
| Copertina di riferimento | Non copiata né tracciata | Layout e grafica sono originali |

I raster nella cache (`sorgenti/cache/`) e quelli incorporati nel PDF derivano interamente dal codice sopra.

## Serve dichiarare la copertina come contenuto generato da IA?

Definizioni KDP (pagina G, sintesi in `KDP_SPECIFICHE.md`):
- **AI-generated**: contenuto (testo, immagini, traduzioni) creato da uno strumento di IA, «even if you applied substantial edits afterwards». Da dichiarare.
- **AI-assisted**: contenuto creato dall'autore e migliorato con IA (modifica, revisione, controllo errori). Non da dichiarare.

Caso concreto: l'immagine non è prodotta da uno strumento di generazione di immagini. È arte procedurale, risultato dell'esecuzione di algoritmi geometrici e di rendering deterministici. Il codice che la produce è stato però scritto con un assistente di programmazione basato su IA. Le due letture sono entrambe difendibili:
- *Non dichiarare*: l'IA ha assistito la scrittura di un programma; l'immagine non è stata generata da un modello di immagini, quindi sarebbe "AI-assisted".
- *Dichiarare*: il contenuto visivo finale è stato in sostanza ideato e realizzato tramite IA, anche se in modo indiretto (codice).

È un giudizio che spetta all'autore: la definizione KDP non copre esplicitamente questo caso. Nel dubbio, dichiarare è la scelta conservativa. L'autore resta in ogni caso responsabile della conformità alle linee guida.

## Nota sull'altra copertina (`../copertina/`)

La copertina separata di «Basi di farmacologia clinica» (in `../copertina/`) usa invece un'illustrazione generata con IA, fornita dall'utente e ingrandita con Higgsfield. Se quella copertina viene pubblicata, va dichiarata come contenuto generato da IA.
