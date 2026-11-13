# Collana «Manuale di farmacologia cardiovascolare»

- `PROMPT_LIBRO_TOMO.md` – prompt per scrivere il tomo «Basi di farmacologia clinica» (13 classi, KDP 6×9", B/N).
- `PROMPT_REVISIONE_E_STAMPA.md` – revisione indipendente, interno KDP e montaggio copertina.
- `PROMPT_COPERTINA.md` – prompt per generare la grafica di copertina.
- `PROMPT_MASTER.md` – (superato) prompt del Volume I singolo, A4.
- `engine/` – motore di impaginazione (WeasyPrint): `build.py`, `style.css`, `check_fill.py`, font Gelasio (OFL).
- `volumi/01-betabloccanti/` – Volume I: `meta.json`, `frontmatter.md`, `parte-01…11.md`, `output/*.pdf`.

Compilare: `pip install weasyprint markdown pillow numpy` poi `python3 libro/engine/build.py libro/volumi/01-betabloccanti`
Controllo pagine: `python3 libro/engine/check_fill.py libro/volumi/01-betabloccanti/output/<file>.pdf`
Nuovo volume: copiare la cartella `volumi/01-betabloccanti`, cambiare `meta.json` e sostituire i `parte-NN.md`.
