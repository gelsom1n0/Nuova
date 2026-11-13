# Collana «Manuale di farmacologia cardiovascolare»

- `PROMPT_MASTER.md` – prompt riutilizzabile per ogni volume.
- `engine/` – motore di impaginazione (WeasyPrint): `build.py`, `style.css`, `check_fill.py`, font Gelasio (OFL).
- `volumi/01-betabloccanti/` – Volume I: `meta.json`, `frontmatter.md`, `parte-01…11.md`, `output/*.pdf`.

Compilare: `pip install weasyprint markdown pillow numpy` poi `python3 libro/engine/build.py libro/volumi/01-betabloccanti`
Controllo pagine: `python3 libro/engine/check_fill.py libro/volumi/01-betabloccanti/output/<file>.pdf`
Nuovo volume: copiare la cartella `volumi/01-betabloccanti`, cambiare `meta.json` e sostituire i `parte-NN.md`.
