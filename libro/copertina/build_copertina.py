#!/usr/bin/env python3
"""
Copertina distesa (full wrap) KDP per «Basi di farmacologia clinica».

Tutto vettoriale (ReportLab): nessuna immagine raster, testo con font Gelasio
(OFL) incorporati in subset. Parametrico sul numero di pagine.

Uso:
    python3 build_copertina.py --pagine 128
    python3 build_copertina.py --pagine 140 --autore "Nome Cognome"
    python3 build_copertina.py --pagine 128 --carta crema

Output (nella cartella dello script):
    copertina_KDP.pdf              variante raccomandata (scura navy/oro), da caricare
    copertina_KDP_chiara.pdf       variante alternativa (avorio/navy)
    copertina_KDP_scura.pdf        copia esplicita della variante scura
    anteprime/*.png                anteprime con e senza guide
    copertina_anteprima.png        distesa con guide (variante raccomandata)
    copertina_anteprima_senza_guide.png
    prima_di_copertina.png         solo prima di copertina, al rifilo
    build_info.json                misure calcolate dell'ultima generazione
"""
from __future__ import annotations

import argparse
import json
import math
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from reportlab.lib.colors import CMYKColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

QUI = Path(__file__).resolve().parent
FONT_DIR = QUI / "fonts"
INCH = 72.0  # punti tipografici per pollice

# ---------------------------------------------------------------------------
# Specifiche KDP (vedi KDP_SPECIFICHE.md per fonti e data di consultazione)
# ---------------------------------------------------------------------------
BLEED = 0.125            # abbondanza su tutti i lati esterni (in)
TRIM_W, TRIM_H = 6.0, 9.0  # formato di rifilo (in)
SAFE = 0.125             # KDP G201953020: testo ad almeno 0,125 in dal rifilo
SAFE_PRUDENTE = 0.25     # KDP G201857950: 0,25 in dal bordo (valore più restrittivo, usato come guida)
SPINE_COEF = {           # spessore per pagina (in), interno B/N
    "bianca": 0.002252,
    "crema": 0.0025,
}
SPINE_TEXT_MIN_PAGES = 79   # KDP G201953020: "at least 79 pages" per il testo sul dorso
SPINE_TEXT_MARGIN = 0.0625  # margine minimo testo/bordi del dorso (in)
BARCODE_W, BARCODE_H = 2.0, 1.2  # area codice a barre (in)
BARCODE_OFFSET = 0.25    # distanza dell'area barcode da rifilo inferiore e dal dorso (in)

# ---------------------------------------------------------------------------
# Testi
# ---------------------------------------------------------------------------
TITOLO = ("Basi di", "farmacologia clinica")
SOTTOTITOLO = "I principali farmaci nella pratica assistenziale: dal meccanismo al letto del paziente"
ETICHETTA = "FARMACOLOGIA CLINICA PER L’ASSISTENZA"
EDIZIONE = "Prima edizione di lavoro"
QUARTA_INTRO = (
    "Un manuale essenziale per chi assiste il paziente ogni giorno. Per ciascuna "
    "classe di farmaci il testo collega il meccanismo d’azione agli effetti "
    "attesi, alle reazioni avverse e ai controlli da eseguire al letto del "
    "paziente, con un linguaggio chiaro e orientato alla pratica infermieristica."
)
QUARTA_PUNTI = (
    "13 classi di farmaci di uso quotidiano, dai beta-bloccanti ai gastroprotettori",
    "Schede rapide e checklist infermieristiche per somministrazione e monitoraggio",
    "Focus su cardiochirurgia e pronto soccorso",
)
AVVERTENZA = "Testo didattico: non sostituisce RCP, linee guida e giudizio clinico."


# ---------------------------------------------------------------------------
# Colori: definiti in esadecimale, convertiti in CMYK (default) o RGB
# ---------------------------------------------------------------------------
def hex_rgb(h: str) -> tuple[float, float, float]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def mix(a: str, b: str, t: float) -> str:
    """Miscela due colori esadecimali (t=0 -> a, t=1 -> b).
    Usata al posto della trasparenza: il PDF resta privo di alpha/blend."""
    ra, rb = hex_rgb(a), hex_rgb(b)
    return "#" + "".join(f"{round((x + (y - x) * t) * 255):02X}" for x, y in zip(ra, rb))


class Pal:
    """Converte i colori nello spazio scelto. La conversione RGB->CMYK è quella
    semplice (con GCR completo): sufficiente per KDP, che accetta file RGB e
    CMYK e converte in stampa; i valori CMYK espliciti dei colori di marca sono
    fissati a mano per evitare derive."""

    FISSI = {  # valori CMYK scelti per i colori di marca (0-1)
        "#1F3A5F": (0.92, 0.70, 0.30, 0.25),  # navy
        "#C9A227": (0.20, 0.33, 0.95, 0.05),  # oro
        "#F6F1E4": (0.03, 0.04, 0.11, 0.00),  # avorio
    }

    def __init__(self, mode: str):
        self.mode = mode

    def __call__(self, h: str):
        h = h.upper()
        r, g, b = hex_rgb(h)
        if self.mode == "rgb":
            return Color(r, g, b)
        if h in self.FISSI:
            return CMYKColor(*self.FISSI[h])
        k = 1 - max(r, g, b)
        if k >= 0.999:
            return CMYKColor(0, 0, 0, 1)
        c, m, y = ((1 - x - k) / (1 - k) for x in (r, g, b))
        return CMYKColor(c, m, y, k)


NAVY, ORO, AVORIO = "#1F3A5F", "#C9A227", "#F6F1E4"


@dataclass
class Tema:
    nome: str
    bg_top: str
    bg_bottom: str
    titolo: str
    sottotitolo: str
    accento: str       # oro
    linee: str         # linee del motivo principale
    linee_glow: list   # aloni (colori già miscelati sul fondo)
    pattern: str       # icone di fondo a bassissimo contrasto
    testo: str
    testo_soft: str
    dorso: str


def temi() -> dict[str, Tema]:
    scuro_bg_b = "#0E1C2F"
    return {
        "scura": Tema(
            nome="scura",
            bg_top=NAVY,
            bg_bottom=scuro_bg_b,
            titolo=AVORIO,
            sottotitolo=mix(AVORIO, NAVY, 0.15),
            accento=ORO,
            linee=ORO,
            linee_glow=[mix("#1A3352", ORO, 0.12), mix("#1A3352", ORO, 0.26)],
            pattern=mix(NAVY, AVORIO, 0.075),
            testo=AVORIO,
            testo_soft=mix(AVORIO, NAVY, 0.30),
            dorso=mix(NAVY, scuro_bg_b, 0.5),
        ),
        "chiara": Tema(
            nome="chiara",
            bg_top="#FBF8F0",
            bg_bottom=AVORIO,
            titolo=NAVY,
            sottotitolo=mix(NAVY, AVORIO, 0.12),
            accento=ORO,
            linee=NAVY,
            linee_glow=[mix(AVORIO, ORO, 0.18), mix(AVORIO, ORO, 0.38)],
            pattern=mix(AVORIO, NAVY, 0.07),
            testo=NAVY,
            testo_soft=mix(NAVY, AVORIO, 0.25),
            dorso=NAVY,
        ),
    }


# ---------------------------------------------------------------------------
# Geometria
# ---------------------------------------------------------------------------
@dataclass
class Geo:
    pagine: int
    carta: str
    spine: float      # in
    W: float          # in, larghezza distesa con abbondanze
    H: float          # in
    back_x0: float    # rifilo sinistro quarta (in, dal bordo del file)
    spine_x0: float
    spine_x1: float
    front_x0: float
    front_x1: float
    trim_y0: float
    trim_y1: float
    spine_text: bool

    @classmethod
    def calcola(cls, pagine: int, carta: str) -> "Geo":
        spine = pagine * SPINE_COEF[carta]
        W = BLEED + TRIM_W + spine + TRIM_W + BLEED
        H = BLEED + TRIM_H + BLEED
        spine_x0 = BLEED + TRIM_W
        spine_x1 = spine_x0 + spine
        # testo sul dorso: regola KDP sul numero di pagine + spazio fisico minimo
        spazio = spine - 2 * SPINE_TEXT_MARGIN
        return cls(
            pagine=pagine, carta=carta, spine=spine, W=W, H=H,
            back_x0=BLEED, spine_x0=spine_x0, spine_x1=spine_x1,
            front_x0=spine_x1, front_x1=spine_x1 + TRIM_W,
            trim_y0=BLEED, trim_y1=BLEED + TRIM_H,
            spine_text=pagine >= SPINE_TEXT_MIN_PAGES and spazio >= 0.10,
        )

    def barcode_box(self) -> tuple[float, float, float, float]:
        """Area barcode (x, y, w, h) in pollici: angolo in basso a destra della
        quarta, a BARCODE_OFFSET dal rifilo inferiore e dal dorso."""
        x = self.spine_x0 - BARCODE_OFFSET - BARCODE_W
        y = self.trim_y0 + BARCODE_OFFSET
        return x, y, BARCODE_W, BARCODE_H


# ---------------------------------------------------------------------------
# Font
# ---------------------------------------------------------------------------
def registra_font():
    for nome, file in {
        "Gelasio": "Gelasio-400-normal.ttf",
        "Gelasio-Italic": "Gelasio-400-italic.ttf",
        "Gelasio-Bold": "Gelasio-700-normal.ttf",
        "Gelasio-BoldItalic": "Gelasio-700-italic.ttf",
    }.items():
        pdfmetrics.registerFont(TTFont(nome, str(FONT_DIR / file)))  # subset incorporato


def wrap(text: str, font: str, size: float, maxw: float) -> list[str]:
    righe, cur = [], ""
    for parola in text.split():
        prova = (cur + " " + parola).strip()
        if pdfmetrics.stringWidth(prova, font, size) <= maxw:
            cur = prova
        else:
            righe.append(cur)
            cur = parola
    if cur:
        righe.append(cur)
    return righe


def spaced(c, x, y, text, font, size, tracking, align="left"):
    """Testo con spaziatura tra lettere (tracking in punti)."""
    w = pdfmetrics.stringWidth(text, font, size) + tracking * (len(text) - 1)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setCharSpace(tracking)
    t.textOut(text)
    t.setCharSpace(0)  # Tc persiste tra blocchi BT/ET: va azzerato
    c.drawText(t)
    return w


# ---------------------------------------------------------------------------
# Disegno: primitive del motivo
# ---------------------------------------------------------------------------
def esagono(c, cx, cy, r, rot=90):
    p = c.beginPath()
    for i in range(7):
        a = math.radians(rot + 60 * i)
        x, y = cx + r * math.cos(a), cy + r * math.sin(a)
        (p.moveTo if i == 0 else p.lineTo)(x, y)
    p.close()
    c.drawPath(p, stroke=1, fill=0)


def vertici(cx, cy, r, rot=90):
    return [(cx + r * math.cos(math.radians(rot + 60 * i)),
             cy + r * math.sin(math.radians(rot + 60 * i))) for i in range(6)]


def capsula(c, x, y, s, ang):
    c.saveState()
    c.translate(x, y)
    c.rotate(ang)
    c.roundRect(-s, -s * 0.38, 2 * s, s * 0.76, s * 0.38, stroke=1, fill=0)
    c.line(0, -s * 0.38, 0, s * 0.38)
    c.restoreState()


def goccia(c, x, y, s, ang):
    c.saveState()
    c.translate(x, y)
    c.rotate(ang)
    p = c.beginPath()
    p.moveTo(0, s)
    p.curveTo(s * 0.15, s * 0.55, s * 0.62, s * 0.05, s * 0.62, -s * 0.30)
    p.curveTo(s * 0.62, -s * 0.70, s * 0.30, -s * 0.95, 0, -s * 0.95)
    p.curveTo(-s * 0.30, -s * 0.95, -s * 0.62, -s * 0.70, -s * 0.62, -s * 0.30)
    p.curveTo(-s * 0.62, s * 0.05, -s * 0.15, s * 0.55, 0, s)
    p.close()
    c.drawPath(p, stroke=1, fill=0)
    c.restoreState()


def siringa(c, x, y, s, ang):
    c.saveState()
    c.translate(x, y)
    c.rotate(ang)
    c.rect(-s * 0.7, -s * 0.18, s * 1.2, s * 0.36, stroke=1, fill=0)   # cilindro
    c.line(-s * 0.7, -s * 0.32, -s * 0.7, s * 0.32)                     # alette
    c.line(-s * 0.7, 0, -s * 1.05, 0)                                   # stantuffo
    c.line(-s * 1.05, -s * 0.2, -s * 1.05, s * 0.2)
    c.line(s * 0.5, 0, s * 1.05, 0)                                     # ago
    for k in (0.1, -0.15, -0.4):
        c.line(s * k, s * 0.18, s * k, s * 0.04)                         # tacche
    c.restoreState()


def pattern_icone(c, tema, pal, geo, esclusioni):
    """Icone a bassissimo contrasto su griglia sfalsata, su tutta la distesa
    (abbondanze comprese), escluse le zone in `esclusioni` (rettangoli in pt)."""
    c.saveState()
    c.setStrokeColor(pal(tema.pattern))
    c.setLineWidth(0.6)
    passo = 0.62 * INCH
    s = 0.085 * INCH
    funzioni = (capsula, goccia, siringa)
    righe = int(geo.H * INCH / (passo * 0.866)) + 2
    colonne = int(geo.W * INCH / passo) + 2
    for r in range(righe):
        y = r * passo * 0.866 + 0.2 * INCH
        for k in range(colonne):
            x = k * passo + (passo / 2 if r % 2 else 0) + 0.15 * INCH
            if any(x0 - s * 1.6 <= x <= x1 + s * 1.6 and y0 - s * 1.6 <= y <= y1 + s * 1.6
                   for x0, y0, x1, y1 in esclusioni):
                continue
            f = funzioni[(r + 2 * k) % 3]  # alterna i tre tipi su righe e colonne
            ang = ((r * 37 + k * 53) % 8) * 22.5
            f(c, x, y, s, ang)
    c.restoreState()


def cuore_path(c, cx, cy, s):
    """Cuore stilizzato (line-art) centrato in (cx, cy), larghezza ~2s."""
    p = c.beginPath()
    p.moveTo(cx, cy - 1.05 * s)                       # punta
    p.curveTo(cx - 0.35 * s, cy - 0.62 * s, cx - 1.02 * s, cy - 0.15 * s, cx - 1.0 * s, cy + 0.38 * s)
    p.curveTo(cx - 0.98 * s, cy + 0.82 * s, cx - 0.62 * s, cy + 1.02 * s, cx - 0.42 * s, cy + 1.0 * s)
    p.curveTo(cx - 0.18 * s, cy + 0.98 * s, cx - 0.04 * s, cy + 0.82 * s, cx, cy + 0.62 * s)
    p.curveTo(cx + 0.04 * s, cy + 0.82 * s, cx + 0.18 * s, cy + 0.98 * s, cx + 0.42 * s, cy + 1.0 * s)
    p.curveTo(cx + 0.62 * s, cy + 1.02 * s, cx + 0.98 * s, cy + 0.82 * s, cx + 1.0 * s, cy + 0.38 * s)
    p.curveTo(cx + 1.02 * s, cy - 0.15 * s, cx + 0.35 * s, cy - 0.62 * s, cx, cy - 1.05 * s)
    p.close()
    return p


def tratto_con_alone(c, pal, tema, disegna, w):
    """Disegna lo stesso tracciato più volte, dal più largo e tenue al più
    sottile e pieno: simula un bagliore senza usare trasparenze."""
    c.saveState()
    c.setLineCap(1)
    c.setLineJoin(1)
    for col, k in zip(tema.linee_glow, (3.8, 2.1)):
        c.setStrokeColor(pal(col))
        c.setLineWidth(w * k)
        disegna()
    c.setStrokeColor(pal(tema.linee))
    c.setLineWidth(w)
    disegna()
    c.restoreState()


def ecg_punti(x0, x1, y, picchi):
    """Polilinea ECG: linea isoelettrica con complessi P-QRS-T centrati in `picchi`."""
    pts = [(x0, y)]
    for px, amp in picchi:
        u = amp / 10
        seg = [(-34, 0), (-28, 2.2), (-22, 0), (-12, 0), (-8, -3), (-3, 10), (2, -5.5),
               (6, 0), (16, 0), (24, 3.2), (32, 0)]
        pts += [(px + dx * u * 0.9, y + dy * u) for dx, dy in seg]
    pts.append((x1, y))
    return pts


def motivo(c, tema, pal, geo, cx, cy, s):
    """Composizione centrale: cuore + rete molecolare + ECG (sulla prima)."""
    lw = 1.15

    # --- rete molecolare: esagoni fusi agganciati al profilo del cuore ---
    r = s * 0.22
    centri = [
        (cx - 0.55 * s, cy + 0.45 * s), (cx - 0.55 * s + r * math.sqrt(3), cy + 0.45 * s),
        (cx - 0.55 * s + r * math.sqrt(3) / 2, cy + 0.45 * s - 1.5 * r),
        (cx + 0.62 * s, cy - 0.05 * s),
        (cx - 1.22 * s, cy - 0.35 * s),
        (cx + 1.25 * s, cy + 0.85 * s),
    ]

    def molecole():
        for (x, y) in centri:
            esagono(c, x, y, r)
        # legami esterni con atomi terminali
        legami = [
            (vertici(*centri[1], r)[5], (cx + 0.25 * s, cy + 1.25 * s)),
            (vertici(*centri[3], r)[5], (cx + 1.05 * s, cy + 0.3 * s)),
            ((cx + 1.05 * s, cy + 0.3 * s), vertici(*centri[5], r)[3]),
            (vertici(*centri[4], r)[1], (cx - 1.38 * s, cy + 0.35 * s)),
            (vertici(*centri[4], r)[4], (cx - 1.0 * s, cy - 0.85 * s)),
            (vertici(*centri[3], r)[3], (cx + 0.3 * s, cy - 0.45 * s)),
            (vertici(*centri[5], r)[0], (cx + 1.25 * s, cy + 1.35 * s)),
        ]
        for a, b in legami:
            c.line(*a, *b)
        # doppi legami interni (stile Kekulé) sui primi due anelli
        for (x, y) in centri[:2] + centri[3:4]:
            v = vertici(x, y, r * 0.72)
            for i in (0, 2, 4):
                c.line(*v[i], *v[i + 1])

    def atomi():
        punti = [(cx + 0.25 * s, cy + 1.25 * s), (cx + 1.05 * s, cy + 0.3 * s),
                 (cx - 1.38 * s, cy + 0.35 * s), (cx - 1.0 * s, cy - 0.85 * s),
                 (cx + 0.3 * s, cy - 0.45 * s), (cx + 1.25 * s, cy + 1.35 * s)]
        for (x, y) in punti:
            c.circle(x, y, 2.2, stroke=1, fill=1)

    # cuore (doppio contorno) con alone
    tratto_con_alone(c, pal, tema, lambda: c.drawPath(cuore_path(c, cx, cy, s), stroke=1, fill=0), lw * 1.6)
    c.saveState()
    c.setStrokeColor(pal(tema.linee))
    c.setLineWidth(0.55)
    c.drawPath(cuore_path(c, cx, cy - 0.04 * s, s * 0.9), stroke=1, fill=0)
    c.restoreState()

    tratto_con_alone(c, pal, tema, molecole, lw * 0.8)
    c.saveState()
    c.setStrokeColor(pal(tema.linee))
    c.setFillColor(pal(tema.linee))
    c.setLineWidth(0.6)
    atomi()
    c.restoreState()


def ecg(c, tema, pal, geo, y, picco_front, picco_back):
    """Linea ECG che attraversa l'intera distesa (prima, dorso, quarta)."""
    x0, x1 = 0, geo.W * INCH
    pts = ecg_punti(x0, x1, y, [(picco_back, 2.4), (picco_front, 6.5)])

    def traccia():
        p = c.beginPath()
        p.moveTo(*pts[0])
        for q in pts[1:]:
            p.lineTo(*q)
        c.drawPath(p, stroke=1, fill=0)

    tratto_con_alone(c, pal, tema, traccia, 1.0)


# ---------------------------------------------------------------------------
# Disegno: pannelli
# ---------------------------------------------------------------------------
def sfondo(c, tema, pal, geo):
    W, H = geo.W * INCH, geo.H * INCH
    c.saveState()
    p = c.beginPath()
    p.rect(0, 0, W, H)
    c.clipPath(p, stroke=0, fill=0)
    # sfumatura verticale (shading PDF, nessuna trasparenza)
    c.linearGradient(0, H, 0, 0, (pal(tema.bg_top), pal(tema.bg_bottom)), extend=True)
    c.restoreState()


def prima(c, tema, pal, geo, autore):
    x0, x1 = geo.front_x0 * INCH, geo.front_x1 * INCH
    cxp = (x0 + x1) / 2
    top = geo.trim_y1 * INCH
    margine = 0.62 * INCH
    maxw = (x1 - x0) - 2 * margine

    # etichetta in alto
    c.setFillColor(pal(tema.accento))
    spaced(c, cxp, top - 0.78 * INCH, ETICHETTA, "Gelasio-Bold", 8.6, 2.1, "center")
    c.setStrokeColor(pal(tema.accento))
    c.setLineWidth(0.6)
    c.line(cxp - 0.35 * INCH, top - 0.95 * INCH, cxp + 0.35 * INCH, top - 0.95 * INCH)

    # titolo: dimensione adattata alla riga più lunga
    size = 44
    while max(pdfmetrics.stringWidth(t, "Gelasio-Bold", size) for t in TITOLO) > maxw:
        size -= 0.5
    c.setFillColor(pal(tema.titolo))
    y = top - 1.75 * INCH
    for riga in TITOLO:
        c.setFont("Gelasio-Bold", size)
        c.drawCentredString(cxp, y, riga)
        y -= size * 1.08

    # filetto oro con rombo centrale
    y -= 0.12 * INCH
    c.setStrokeColor(pal(tema.accento))
    c.setFillColor(pal(tema.accento))
    c.setLineWidth(0.8)
    c.line(cxp - 1.1 * INCH, y, cxp - 0.09 * INCH, y)
    c.line(cxp + 0.09 * INCH, y, cxp + 1.1 * INCH, y)
    d = 0.045 * INCH
    p = c.beginPath()
    p.moveTo(cxp, y + d); p.lineTo(cxp + d, y); p.lineTo(cxp, y - d); p.lineTo(cxp - d, y); p.close()
    c.drawPath(p, stroke=0, fill=1)

    # sottotitolo
    y -= 0.38 * INCH
    c.setFillColor(pal(tema.sottotitolo))
    for riga in wrap(SOTTOTITOLO, "Gelasio-Italic", 14, maxw * 0.92):
        c.setFont("Gelasio-Italic", 14)
        c.drawCentredString(cxp, y, riga)
        y -= 19
    fine_testo = y

    # autore (opzionale) e edizione in basso
    base = geo.trim_y0 * INCH
    c.setFillColor(pal(tema.testo_soft))
    spaced(c, cxp, base + 0.45 * INCH, EDIZIONE.upper(), "Gelasio", 7.4, 1.6, "center")
    if autore:
        c.setFillColor(pal(tema.titolo))
        spaced(c, cxp, base + 0.82 * INCH, autore.upper(), "Gelasio-Bold", 12, 2.2, "center")
    return fine_testo


def dorso(c, tema, pal, geo, autore):
    x0, x1 = geo.spine_x0 * INCH, geo.spine_x1 * INCH
    # fascia del dorso a tinta unita, estesa nelle abbondanze sopra/sotto
    c.setFillColor(pal(tema.dorso))
    c.rect(x0, 0, x1 - x0, geo.H * INCH, stroke=0, fill=1)
    if not geo.spine_text:
        return
    cx = (x0 + x1) / 2
    cy = geo.H * INCH / 2
    disponibile = (x1 - x0) - 2 * SPINE_TEXT_MARGIN * INCH
    size = min(9.5, disponibile * 0.72)  # altezza maiuscole ~0,7 em
    c.saveState()
    c.translate(cx, cy)
    c.rotate(-90)  # convenzione KDP/USA: si legge dall'alto in basso
    testo = "BASI DI FARMACOLOGIA CLINICA"
    c.setFillColor(pal(AVORIO if tema.nome == "scura" else AVORIO))
    # baseline spostata per centrare otticamente le maiuscole sullo spessore
    yb = -size * 0.35
    if autore:
        spaced(c, -0.5 * INCH, yb, testo, "Gelasio-Bold", size, 1.4, "center")
        c.setFillColor(pal(ORO))
        spaced(c, 2.9 * INCH, yb, autore.upper(), "Gelasio", size * 0.9, 1.2, "center")
    else:
        spaced(c, 0, yb, testo, "Gelasio-Bold", size, 1.6, "center")
    # piccoli rombi oro alle estremità del titolo
    c.setFillColor(pal(ORO))
    for xx in ((-3.6 * INCH,) if autore else (-3.6 * INCH, 3.6 * INCH)):
        d = min(2.6, size * 0.28)
        p = c.beginPath()
        p.moveTo(xx, d); p.lineTo(xx + d, 0); p.lineTo(xx, -d); p.lineTo(xx - d, 0); p.close()
        c.drawPath(p, stroke=0, fill=1)
    c.restoreState()


def quarta(c, tema, pal, geo):
    x0 = geo.back_x0 * INCH + 0.62 * INCH
    x1 = geo.spine_x0 * INCH - 0.62 * INCH
    maxw = x1 - x0
    y = geo.trim_y1 * INCH - 1.0 * INCH

    # titolo breve
    c.setFillColor(pal(tema.accento))
    spaced(c, x0, y, ETICHETTA, "Gelasio-Bold", 7.8, 1.8)
    y -= 0.42 * INCH
    c.setFillColor(pal(tema.titolo))
    c.setFont("Gelasio-Bold", 20)
    c.drawString(x0, y, "Basi di farmacologia clinica")
    y -= 0.42 * INCH

    # presentazione
    c.setFillColor(pal(tema.testo))
    for riga in wrap(QUARTA_INTRO, "Gelasio", 11, maxw):
        c.setFont("Gelasio", 11)
        c.drawString(x0, y, riga)
        y -= 15.5
    y -= 0.22 * INCH

    # punti elenco con marcatore a esagono
    for punto in QUARTA_PUNTI:
        righe = wrap(punto, "Gelasio", 10.5, maxw - 0.28 * INCH)
        c.saveState()
        c.setStrokeColor(pal(tema.accento))
        c.setLineWidth(0.9)
        esagono(c, x0 + 0.07 * INCH, y + 3.6, 3.6)
        c.restoreState()
        c.setFillColor(pal(tema.testo))
        for riga in righe:
            c.setFont("Gelasio", 10.5)
            c.drawString(x0 + 0.28 * INCH, y, riga)
            y -= 14.5
        y -= 6
    y -= 0.12 * INCH

    # avvertenza
    c.setStrokeColor(pal(tema.accento))
    c.setLineWidth(0.5)
    c.line(x0, y + 8, x0 + 0.6 * INCH, y + 8)
    y -= 8
    c.setFillColor(pal(tema.testo_soft))
    for riga in wrap(AVVERTENZA, "Gelasio-Italic", 9, maxw):
        c.setFont("Gelasio-Italic", 9)
        c.drawString(x0, y, riga)
        y -= 12
    return y


def guide(c, geo, includi_barcode=True):
    """Sovrimpressione per l'anteprima: rifilo, sicurezza, dorso, barcode."""
    I = INCH
    c.saveState()
    c.setLineWidth(0.8)
    # rifilo (bordo esterno del libro finito)
    c.setStrokeColor(Color(1, 0, 0))
    c.rect(geo.back_x0 * I, geo.trim_y0 * I, (geo.front_x1 - geo.back_x0) * I, TRIM_H * I, stroke=1, fill=0)
    # linee del dorso
    c.setStrokeColor(Color(1, 0, 1))
    c.line(geo.spine_x0 * I, 0, geo.spine_x0 * I, geo.H * I)
    c.line(geo.spine_x1 * I, 0, geo.spine_x1 * I, geo.H * I)
    # zona di sicurezza dei pannelli
    c.setStrokeColor(Color(0, 0.75, 1))
    c.setDash(4, 3)
    for xa, xb in ((geo.back_x0 + SAFE, geo.spine_x0 - SAFE), (geo.front_x0 + SAFE, geo.front_x1 - SAFE)):
        c.rect(xa * I, (geo.trim_y0 + SAFE) * I, (xb - xa) * I, (TRIM_H - 2 * SAFE) * I, stroke=1, fill=0)
    if geo.spine_text:
        c.rect((geo.spine_x0 + SPINE_TEXT_MARGIN) * I, (geo.trim_y0 + SAFE) * I,
               (geo.spine - 2 * SPINE_TEXT_MARGIN) * I, (TRIM_H - 2 * SAFE) * I, stroke=1, fill=0)
    # margine prudente 0,25 in (G201857950)
    c.setStrokeColor(Color(0.55, 0.55, 0.55))
    c.setDash(1, 3)
    for xa, xb in ((geo.back_x0 + SAFE_PRUDENTE, geo.spine_x0 - SAFE_PRUDENTE),
                   (geo.front_x0 + SAFE_PRUDENTE, geo.front_x1 - SAFE_PRUDENTE)):
        c.rect(xa * I, (geo.trim_y0 + SAFE_PRUDENTE) * I, (xb - xa) * I,
               (TRIM_H - 2 * SAFE_PRUDENTE) * I, stroke=1, fill=0)
    c.setDash()
    # area barcode
    if includi_barcode:
        bx, by, bw, bh = geo.barcode_box()
        c.setFillColor(Color(1, 1, 1))
        c.setStrokeColor(Color(1, 0.55, 0))
        c.setLineWidth(1.2)
        c.rect(bx * I, by * I, bw * I, bh * I, stroke=1, fill=1)
        c.setFillColor(Color(1, 0.45, 0))
        c.setFont("Gelasio-Bold", 8)
        c.drawCentredString((bx + bw / 2) * I, (by + bh / 2) * I + 2, "AREA CODICE A BARRE")
        c.setFont("Gelasio", 7)
        c.drawCentredString((bx + bw / 2) * I, (by + bh / 2) * I - 9, "2 × 1,2 in – lasciare libera")
    # etichette
    c.setFillColor(Color(1, 0, 0))
    c.setFont("Gelasio", 7)
    c.drawString(geo.back_x0 * I + 3, geo.trim_y1 * I + 2, "rifilo")
    c.setFillColor(Color(0, 0.6, 0.9))
    c.drawString((geo.back_x0 + SAFE) * I + 3, (geo.trim_y1 - SAFE) * I - 9, "zona di sicurezza 0,125 in")
    c.restoreState()


# ---------------------------------------------------------------------------
# Costruzione
# ---------------------------------------------------------------------------
def costruisci(out: Path, tema: Tema, geo: Geo, mode: str, autore: str, con_guide=False):
    pal = Pal(mode)
    I = INCH
    c = canvas.Canvas(str(out), pagesize=(geo.W * I, geo.H * I), pageCompression=1,
                      initialFontName="Gelasio")  # evita Helvetica non incorporato
    c.setTitle("Basi di farmacologia clinica – copertina")
    c.setSubject(f"Copertina KDP 6x9 in, {geo.pagine} pagine, carta {geo.carta}, dorso {geo.spine:.4f} in")
    c.setCreator("build_copertina.py (ReportLab)")
    if autore:
        c.setAuthor(autore)

    sfondo(c, tema, pal, geo)

    # zone escluse dal pattern di icone: barcode (+margine) e testo quarta/titolo
    bx, by, bw, bh = geo.barcode_box()
    esclusioni = [((bx - 0.12) * I, (by - 0.12) * I, (bx + bw + 0.12) * I, (by + bh + 0.12) * I)]
    fx0, fx1 = geo.front_x0 * I, geo.front_x1 * I
    esclusioni.append((fx0 + 0.35 * I, (geo.trim_y1 - 4.25) * I, fx1 - 0.35 * I, (geo.trim_y1 - 0.45) * I))
    esclusioni.append(((geo.back_x0 + 0.4) * I, (geo.trim_y1 - 5.6) * I, (geo.spine_x0 - 0.4) * I, (geo.trim_y1 - 0.6) * I))
    esclusioni.append((geo.spine_x0 * I, 0, geo.spine_x1 * I, geo.H * I))
    # fascia inferiore della prima: autore ed edizione
    esclusioni.append((fx0 + 0.9 * I, (geo.trim_y0 + 0.25) * I, fx1 - 0.9 * I, (geo.trim_y0 + 1.1) * I))
    # interno del motivo centrale (cuore): niente icone sotto le linee principali
    cxm, cym, sm = (geo.front_x0 + TRIM_W / 2) * I, (geo.trim_y0 + 2.95) * I, 1.05 * I
    esclusioni.append((cxm - 1.05 * sm, cym - 1.1 * sm, cxm + 1.05 * sm, cym + 1.05 * sm))
    pattern_icone(c, tema, pal, geo, esclusioni)

    # ECG lungo l'intera distesa, nel terzo inferiore
    y_ecg = (geo.trim_y0 + 2.35) * I
    cx_front = (geo.front_x0 + TRIM_W / 2) * I
    ecg(c, tema, pal, geo, y_ecg, cx_front, (geo.back_x0 + 1.25) * I)

    dorso(c, tema, pal, geo, autore)

    # motivo principale sulla prima (metà inferiore)
    motivo(c, tema, pal, geo, cx_front, (geo.trim_y0 + 2.95) * I, 1.05 * I)

    prima(c, tema, pal, geo, autore)
    quarta(c, tema, pal, geo)

    if con_guide:
        guide(c, geo)
    c.showPage()
    c.save()


def render_png(pdf: Path, png: Path, dpi: int, crop_in=None, geo=None):
    """Rasterizza con pdftoppm; crop_in = (x, y_top, w, h) in pollici."""
    args = ["pdftoppm", "-png", "-r", str(dpi), "-singlefile"]
    if crop_in:
        x, y, w, h = crop_in
        args += ["-x", str(round(x * dpi)), "-y", str(round(y * dpi)),
                 "-W", str(round(w * dpi)), "-H", str(round(h * dpi))]
    args += [str(pdf), str(png.with_suffix(""))]
    subprocess.run(args, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pagine", type=int, required=True, help="numero di pagine dell'interno (pari)")
    ap.add_argument("--carta", choices=sorted(SPINE_COEF), default="bianca")
    ap.add_argument("--autore", default="", help="nome dell'autore (vuoto = nessun autore)")
    ap.add_argument("--colore", choices=("cmyk", "rgb"), default="cmyk",
                    help="spazio colore dei vettori (default CMYK)")
    ap.add_argument("--raccomandata", choices=("scura", "chiara"), default="scura")
    ap.add_argument("--dpi-anteprima", type=int, default=150)
    a = ap.parse_args()

    if a.pagine < 24:
        ap.error("KDP richiede almeno 24 pagine per la brossura")
    if a.pagine % 2:
        print("Attenzione: numero di pagine dispari; KDP conta le pagine a coppie.")

    registra_font()
    geo = Geo.calcola(a.pagine, a.carta)
    tutti = temi()
    anteprime = QUI / "anteprime"
    anteprime.mkdir(exist_ok=True)

    for nome, tema in tutti.items():
        pdf = QUI / f"copertina_KDP_{nome}.pdf"
        costruisci(pdf, tema, geo, a.colore, a.autore)
        guide_pdf = anteprime / f"_guide_{nome}.pdf"
        costruisci(guide_pdf, tema, geo, "rgb", a.autore, con_guide=True)
        render_png(pdf, anteprime / f"distesa_{nome}.png", a.dpi_anteprima)
        render_png(guide_pdf, anteprime / f"distesa_{nome}_guide.png", a.dpi_anteprima)
        render_png(pdf, anteprime / f"prima_{nome}.png", a.dpi_anteprima,
                   crop_in=(geo.front_x0, BLEED, TRIM_W, TRIM_H))
        guide_pdf.unlink()

    r = a.raccomandata
    shutil.copy(QUI / f"copertina_KDP_{r}.pdf", QUI / "copertina_KDP.pdf")
    shutil.copy(anteprime / f"distesa_{r}_guide.png", QUI / "copertina_anteprima.png")
    shutil.copy(anteprime / f"distesa_{r}.png", QUI / "copertina_anteprima_senza_guide.png")
    shutil.copy(anteprime / f"prima_{r}.png", QUI / "prima_di_copertina.png")

    info = {
        "pagine": geo.pagine,
        "carta": geo.carta,
        "coefficiente_dorso_in": SPINE_COEF[geo.carta],
        "dorso_in": round(geo.spine, 4),
        "dorso_mm": round(geo.spine * 25.4, 2),
        "larghezza_in": round(geo.W, 4),
        "altezza_in": round(geo.H, 4),
        "larghezza_mm": round(geo.W * 25.4, 2),
        "altezza_mm": round(geo.H * 25.4, 2),
        "larghezza_pt": round(geo.W * INCH, 3),
        "altezza_pt": round(geo.H * INCH, 3),
        "testo_sul_dorso": geo.spine_text,
        "area_barcode_in": dict(zip(("x", "y_dal_basso", "w", "h"), (round(v, 4) for v in geo.barcode_box()))),
        "spazio_colore": a.colore.upper(),
        "autore": a.autore or None,
        "variante_raccomandata": r,
    }
    (QUI / "build_info.json").write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
