# Asset e origine – copertina «ABC della farmacologia clinica»

## Elenco degli asset

| Asset | Origine | Note |
|---|---|---|
| Capsula, capsula aperta e compressa a maglia low-poly | Procedurale, originale. `pillola_mesh.py`: campi di distanza impliciti (capsula in due pezzi con gradino di giunzione, gusci aperti con spessore, compressa biconvessa con linea di frattura), superficie estratta con marching cubes e decimata con decimazione quadrica (`fast-simplification`). Maglie in `sorgenti/capsula_1800.npz`, `capsula_aperta_2400.npz`, `compressa_1500.npz` | Nessuno strumento di generazione di immagini; nessuna impronta, marchio o colore di farmaci reali |
| Rendering (spigoli, nodi, bagliore, particelle, granuli di principio attivo, molecole esagonali, reticolo esagonale, mappatura tonale azzurra) | Procedurale, originale. `arte_mesh.py` (NumPy, OpenCV) | Rendering proprio, non un modello di immagini |
| Tracciati (curva di concentrazione plasmatica, catena molecolare, sigmoide dose-risposta), rete low-poly del retro, polvere luminosa, alone del titolo | Procedurali (`arte_mesh.py`, `build_copertina_B.py`; SciPy, OpenCV, Pillow) | Alone del titolo calcolato dal font |
| Icona a capsula del dorso | Vettoriale, disegnata nel codice | |
| Font | Montserrat (SIL Open Font License), `fonts/` con `OFL.txt` | Incorporati nel PDF come subset |
| Testi (titolo, sottotitolo, quarta, avvertenza) | Scritti per il libro; costanti in `build_copertina_B.py` | Sottotitolo e quarta sono testi di lavoro, da confermare con l'autore |
| Immagini stock, illustrazioni o elementi di terzi | Nessuno | |
| Copertine esistenti | Non copiate né tracciate | Layout condiviso solo con il volume A, dello stesso progetto |

I raster nella cache (`sorgenti/cache/`) e quelli incorporati nel PDF derivano interamente dal codice sopra.

## Serve dichiarare la copertina come contenuto generato da IA?

Definizioni KDP (pagina G, sintesi in `../copertina_A/KDP_SPECIFICHE.md`):
- **AI-generated**: contenuto (testo, immagini, traduzioni) creato da uno strumento di IA, «even if you applied substantial edits afterwards». Da dichiarare.
- **AI-assisted**: contenuto creato dall'autore e migliorato con IA (modifica, revisione, controllo errori). Non da dichiarare.

Caso concreto: l'immagine non è prodotta da uno strumento di generazione di immagini. È arte procedurale, risultato dell'esecuzione di algoritmi geometrici e di rendering deterministici. Il codice che la produce è stato però scritto con un assistente di programmazione basato su IA. Le due letture sono entrambe difendibili:
- *Non dichiarare*: l'IA ha assistito la scrittura di un programma; l'immagine non è stata generata da un modello di immagini, quindi sarebbe "AI-assisted".
- *Dichiarare*: il contenuto visivo finale è stato in sostanza ideato e realizzato tramite IA, anche se in modo indiretto (codice).

È un giudizio che spetta all'autore: la definizione KDP non copre esplicitamente questo caso. Nel dubbio, dichiarare è la scelta conservativa. L'autore resta in ogni caso responsabile della conformità alle linee guida. Vale la stessa decisione presa per il volume A (`../copertina_A/ASSET_E_IA.md`), per coerenza tra i due volumi.

## Nota sulle altre copertine

La copertina separata di «Basi di farmacologia clinica» (`../copertina/`) usa invece un'illustrazione generata con IA, fornita dall'utente e ingrandita con Higgsfield. Se quella copertina viene pubblicata, va dichiarata come contenuto generato da IA. Questa copertina B non ne riusa alcun elemento grafico; del libro «Basi» è riusato solo il sottotitolo (testo di lavoro).
