# Brief – KDP cover for Volume B «ABC della farmacologia clinica»

*(Improved and translated from the author's Italian request of 2026-11-19. This is the prompt executed for this cover.)*

## Goal
Design the full-wrap paperback cover (back + spine + front) for Volume B of the two-volume series, as the visual twin of Volume A «ABC della cardiologia clinica» (`libro/copertina_A/`). Same grid, typography system, black background and "digital medicine" mood, so the two books read instantly as a series on the shelf and as Amazon thumbnails, while the subject and the accent colour clearly mark the difference: heart/red/ECG → pill/technological light blue/pharmacology.

## Book data
- Title: **ABC della farmacologia clinica**. Working subtitle (editable constant): «I principali farmaci nella pratica assistenziale: dal meccanismo al letto del paziente». No author yet: keep the parametric slot.
- Trim **7 × 10 in**, B/W interior, white paper; page count not final (default 290, `--pagine N`). Reuse the KDP values already verified for Volume A (`libro/copertina_A/KDP_SPECIFICHE.md`, same trim): bleed 0.125 in, spine = pages × 0.002252 in, spine text from 79 pages with ≥ 0.0625 in margins, 2 × 1.2 in barcode area clear at ≥ 0.25 in from spine and trim, CMYK, fonts embedded, no transparency, images ≥ 300 dpi.
- Content to reflect on the back (Volume B holds the drug classes not covered in Volume A): general principles (pharmacokinetics, pharmacodynamics, administration routes, interactions); the everyday classes (antibiotics, analgesics and opioids, insulins and oral hypoglycaemics, bronchodilators, corticosteroids, gastroprotective agents); quick reference cards and nursing checklists. No clinical promises. Disclaimer: «Testo didattico: non sostituisce RCP, linee guida e giudizio clinico».

## Visual direction
- **Hero object:** a large 3D pill rendered as the same glowing low-poly wireframe as the heart of Volume A (triangulated mesh, luminous nodes, faint X-ray back edges), **dematerialising**: one end breaks into particles, small triangular shards and tiny hexagonal molecules, as if the drug were being released and absorbed. Granules of active substance visible inside the shell through the mesh.
- **Colour:** technological light blue on pure black (#050505). Mesh and glow from deep azure (#0A4C8C) to cyan (#1EA7FF – #3CC8FF), hot spots near white. Accent colour for «ABC», rules and bullets: azure #1EA7FF. Text white #FFFFFF and grey #B9B9B9.
- **Replacing the ECG line:** a thin glowing line that "speaks pharmacology", crossing the wrap horizontally like the ECG did on Volume A.
- **Typography identical to Volume A:** kicker line in small spaced caps with coloured dots, giant «ABC» (Montserrat Black) in the accent colour with a soft glow, «della farmacologia clinica» in bold white, short accent rule, light subtitle. Spine: «ABC» in accent colour + «DELLA FARMACOLOGIA CLINICA» in white, read top-to-bottom, with a small vector capsule icon as the accent.
- Do not copy any existing cover, logo, brand or pill imprint (no real drug, no brand colours of real medicines).

## Three options to choose from
1. **A – Dissolving capsule + pharmacokinetic curve.** Two-piece capsule, tilted diagonally, dissolving towards the upper right into particles and molecules; the line is a plasma-concentration curve with repeated doses reaching steady state (peaks and troughs) – the pharmacology equivalent of the ECG.
2. **B – Open capsule releasing molecules + molecular chain.** The two halves pulled apart; between them a stream of granules and small hexagonal molecules; the line is a molecular backbone (bonds with hexagonal rings and atom nodes).
3. **C – Round tablet into a molecular lattice + dose–response curve.** A scored round tablet seen in 3/4 view, its edge dissolving into a hexagonal lattice; the line is a sigmoid dose–response curve with data points.

Recommend one, with reasons.

## Technical rules
- Artwork procedural in Python (no AI image generator, no stock), rendered at 400 dpi, CMYK with the same rich black as Volume A (C40 M30 Y30 K100, TAC ≤ 260 %), dithering against banding. All text vector, never inside raster.
- Parametric build script (`--pagine`, `--trim`, `--autore`, `--variante`, `--tutte`), raster cache git-ignored (never commit it).
- Work only in `libro/copertina_B/`; do not touch `libro/copertina/`, `libro/copertina_A/` or the manuscript folders. Commit and push on the session branch, no pull request.
- Deliverables: `copertina_KDP.pdf` (recommended option) + the two alternative PDFs, previews with and without guides, front-cover PNGs of the three options, `build_info.json`, README, checklist, asset/AI list.
- Final answer to the author in Italian.
