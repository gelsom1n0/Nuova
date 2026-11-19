#!/usr/bin/env python3
"""
Copertina KDP (brossura) del Volume B: «ABC della farmacologia clinica».
Gemella della copertina del Volume A (stessa griglia, stessa tipografia, stesso
nero): cambia il soggetto (pillola al posto del cuore), il colore d'accento
(azzurro tecnologico al posto del rosso) e il tracciato (motivi farmacologici
al posto dell'ECG).

Uso:
    python3 build_copertina_B.py --pagine 290
    python3 build_copertina_B.py --pagine 290 --tutte
    python3 build_copertina_B.py --pagine 296 --autore "Nome Cognome" --variante A

Varianti:
    A  capsula che si dematerializza + curva di concentrazione plasmatica (dosi ripetute)
    B  capsula aperta che rilascia molecole + catena molecolare
    C  compressa che diventa reticolo esagonale + curva dose-risposta

Principi:
- illustrazione originale procedurale (arte_mesh.py + pillola_mesh.py): nessuna
  immagine generata con IA, nessun asset di terzi;
- testo SEMPRE vettoriale (Montserrat, OFL, incorporato); nel raster ci sono solo
  gli aloni luminosi (bagliore della pillola, del tracciato e del titolo);
- quarta e prima sono raster separati ancorati ai bordi esterni del file: al
  variare del numero di pagine cambia solo il dorso (vettoriale), la grafica dei
  piatti resta identica rispetto al proprio rifilo. I raster si mettono in cache
  per variante e formato, quindi il ricalcolo per un nuovo numero di pagine è
  immediato;
- CMYK ovunque; nero di fondo "ricco" (C40 M30 Y30 K100) per le grandi aree
  scure; nessuna trasparenza nel PDF.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.colors import CMYKColor, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

import arte_mesh as arte

QUI = Path(__file__).resolve().parent
FONT_DIR = QUI / "fonts"
CACHE = QUI / "sorgenti" / "cache"
I = 72.0                     # punti per pollice
DPI_ARTE = 400               # risoluzione dei raster (KDP: minimo 300)

# ---------------------------------------------------------------------------
# Specifiche KDP (fonti e date in KDP_SPECIFICHE.md)
# ---------------------------------------------------------------------------
BLEED = 0.125
SPINE_COEF = {"bianca": 0.002252, "crema": 0.0025}
SPINE_TEXT_MIN_PAGES = 79
SPINE_TEXT_MARGIN = 0.0625
SAFE = 0.125
SAFE_PRUDENTE = 0.25
BARCODE_W, BARCODE_H, BARCODE_OFF = 2.0, 1.2, 0.25
CORPO_MIN = 7.0

# ---------------------------------------------------------------------------
# Testi
# ---------------------------------------------------------------------------
KICKER = ("MECCANISMI", "FARMACI", "ASSISTENZA")
TITOLO_GRANDE = "ABC"
TITOLO_RIGA = "della farmacologia clinica"
# sottotitolo di lavoro (da confermare con l'autore)
SOTTOTITOLO = ("I principali farmaci nella pratica assistenziale:", "dal meccanismo al letto del paziente")
QUARTA_INTRO = (
    "Un percorso essenziale nella farmacologia clinica, pensato per infermieri e "
    "studenti delle professioni sanitarie. Per ogni classe di farmaci il testo "
    "collega il meccanismo d\u2019azione agli effetti attesi, alle reazioni avverse "
    "e ai controlli da eseguire, con un linguaggio chiaro e orientato alla pratica "
    "al letto del paziente."
)
QUARTA_PUNTI = (
    "Principi di farmacocinetica e farmacodinamica, vie di somministrazione e interazioni",
    "Antibiotici, analgesici e oppioidi, insuline, broncodilatatori, corticosteroidi e gastroprotettori",
    "Schede rapide e checklist infermieristiche per somministrazione e monitoraggio",
)
AVVERTENZA = "Testo didattico: non sostituisce RCP, linee guida e giudizio clinico."

# ---------------------------------------------------------------------------
# Colori (esadecimali per l'anteprima RGB; CMYK fissati a mano per la stampa)
# ---------------------------------------------------------------------------
ACCENTO = "#1EA7FF"          # azzurro tecnologico
ACCENTO_GLOW = "#3CC8FF"
TRACCIATO = "#5CCBF2"        # linea nitida del tracciato (prima)
TRACCIATO_Q = "#3F9FCC"      # tracciato in quarta (più tenue)
FINESTRA = "#2C6F8F"         # finestra terapeutica tratteggiata
BIANCO = "#FFFFFF"
GRIGIO = "#B9B9B9"
NERO = "#050505"
CMYK_FISSI = {
    ACCENTO: (0.78, 0.18, 0.0, 0.0),
    ACCENTO_GLOW: (0.68, 0.05, 0.0, 0.0),
    BIANCO: (0.0, 0.0, 0.0, 0.0),
    GRIGIO: (0.0, 0.0, 0.0, 0.30),
    NERO: (0.40, 0.30, 0.30, 1.0),       # nero ricco, TAC 200 %
}
TAC_MAX = 2.6                            # copertura totale massima nel raster


def hex_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


class Pal:
    def __init__(self, mode, nero="ricco"):
        self.mode, self.nero = mode, nero

    def __call__(self, h):
        h = h.upper()
        if self.mode == "rgb":
            return Color(*hex_rgb(h))
        if h == NERO and self.nero == "solo-k":
            return CMYKColor(0, 0, 0, 1)
        if h in CMYK_FISSI:
            return CMYKColor(*CMYK_FISSI[h])
        r, g, b = hex_rgb(h)
        k = 1 - max(r, g, b)
        if k > 0.999:
            return CMYKColor(0, 0, 0, 1)
        return CMYKColor(*((1 - x - k) / (1 - k) for x in (r, g, b)), k)


def rgb_a_cmyk(rgb: np.ndarray, nero="ricco") -> np.ndarray:
    """RGB float (0..1) -> CMYK uint8. Conversione semplice con GCR completo; le
    zone quasi nere diventano nero ricco pieno (stesso valore del dorso
    vettoriale, così non si vede la giunzione), con transizione morbida."""
    k = 1.0 - rgb.max(axis=2)
    d = np.maximum(1.0 - k, 1e-6)
    c = (1.0 - rgb[..., 0] - k) / d
    m = (1.0 - rgb[..., 1] - k) / d
    y = (1.0 - rgb[..., 2] - k) / d
    cmyk = np.stack([c, m, y, k], axis=2)
    if nero == "ricco":
        t = np.clip((k - 0.90) / 0.07, 0, 1)[..., None]       # 1 sul fondo, 0 nelle luci
        sotto = np.array(CMYK_FISSI[NERO][:3])
        cmyk[..., :3] = np.maximum(cmyk[..., :3], t * sotto)
        cmyk[..., 3:] = cmyk[..., 3:] + (1 - cmyk[..., 3:]) * t
        tot = cmyk.sum(axis=2, keepdims=True)
        eccesso = np.clip(tot - TAC_MAX, 0, None)
        cmy = cmyk[..., :3]
        cmyk[..., :3] = cmy - eccesso * cmy / np.maximum(cmy.sum(axis=2, keepdims=True), 1e-6)
    else:
        t = (k > 0.97)[..., None]
        cmyk = np.where(t, np.array([0, 0, 0, 1.0]), cmyk)
    return (np.clip(cmyk, 0, 1) * 255 + 0.5).astype(np.uint8)


# ---------------------------------------------------------------------------
# Font
# ---------------------------------------------------------------------------
PESI = ("Light", "Regular", "Medium", "SemiBold", "Bold", "ExtraBold", "Black", "Italic")


def registra_font():
    for p in PESI:
        pdfmetrics.registerFont(TTFont(f"Montserrat-{p}", str(FONT_DIR / f"Montserrat-{p}.ttf")))


def larghezza(t, font, size, tracking=0.0):
    return pdfmetrics.stringWidth(t, font, size) + tracking * max(len(t) - 1, 0)


def wrap(text, font, size, maxw):
    righe, cur = [], ""
    for w in text.split():
        prova = (cur + " " + w).strip()
        if larghezza(prova, font, size) <= maxw:
            cur = prova
        else:
            righe.append(cur)
            cur = w
    return righe + ([cur] if cur else [])


def testo(c, x, y, t, font, size, tracking=0.0, align="left"):
    w = larghezza(t, font, size, tracking)
    if align == "center":
        x -= w / 2
    elif align == "right":
        x -= w
    o = c.beginText(x, y)
    o.setFont(font, size)
    o.setCharSpace(tracking)
    o.textOut(t)
    o.setCharSpace(0)
    c.drawText(o)
    return w


# ---------------------------------------------------------------------------
# Geometria
# ---------------------------------------------------------------------------
@dataclass
class Geo:
    trim_w: float
    trim_h: float
    pagine: int
    carta: str

    @property
    def spine(self):
        return self.pagine * SPINE_COEF[self.carta]

    @property
    def W(self):
        return 2 * BLEED + 2 * self.trim_w + self.spine

    @property
    def H(self):
        return 2 * BLEED + self.trim_h

    @property
    def panel_w(self):                  # larghezza di ciascun pannello raster (bleed + piatto)
        return BLEED + self.trim_w

    @property
    def spine_x0(self):
        return BLEED + self.trim_w

    @property
    def spine_x1(self):
        return self.spine_x0 + self.spine

    @property
    def spine_text(self):
        return self.pagine >= SPINE_TEXT_MIN_PAGES and self.spine - 2 * SPINE_TEXT_MARGIN >= 0.12

    def barcode(self):
        """(x, y_dal_basso, w, h) in pollici nelle coordinate del file."""
        return (self.spine_x0 - BARCODE_OFF - BARCODE_W, BLEED + BARCODE_OFF, BARCODE_W, BARCODE_H)


# ---------------------------------------------------------------------------
# Impaginato della prima (condiviso tra vettoriale e alone raster)
# Coordinate in pollici dal rifilo sinistro/alto della PRIMA.
# ---------------------------------------------------------------------------
@dataclass
class LayoutPrima:
    margine: float
    y_kicker: float
    abc_size: float
    y_abc: float
    riga_size: float
    y_riga: float
    y_filetto: float
    sotto_size: float
    y_sotto: tuple
    cuore_c: tuple
    cuore_h: float
    y_ecg: float


def layout_prima(trim_w, trim_h) -> LayoutPrima:
    m = 0.68
    maxw = trim_w - 2 * m
    riga = 40.0
    while larghezza(TITOLO_RIGA, "Montserrat-Bold", riga) > maxw * I:
        riga -= 0.25
    abc = riga * 4.1
    s = 15.0
    while max(larghezza(t, "Montserrat-Light", s) for t in SOTTOTITOLO) > maxw * I:
        s -= 0.25
    k = trim_h / 10.0                              # scala verticale per altri formati
    return LayoutPrima(
        margine=m, y_kicker=0.80 * k, abc_size=abc, y_abc=0.80 * k + 0.20 + abc * 0.72 / I,
        riga_size=riga, y_riga=0.80 * k + 0.20 + abc * 0.72 / I + riga * 1.15 / I + 0.04,
        y_filetto=0, sotto_size=s, y_sotto=(0, 0),
        cuore_c=(trim_w * 0.49, trim_h * 0.672), cuore_h=trim_h * 0.53, y_ecg=trim_h * 0.742,
    )._completa()


def _completa(self: LayoutPrima):
    self.y_filetto = self.y_riga + 0.24
    self.y_sotto = (self.y_filetto + 0.36, self.y_filetto + 0.36 + self.sotto_size * 1.32 / I)
    return self


LayoutPrima._completa = _completa


# ---------------------------------------------------------------------------
# Arte raster: prima e quarta (in cache per variante/formato)
# ---------------------------------------------------------------------------
# variante -> (stile del rendering, centro dell'oggetto in pollici dal rifilo
# sinistro/alto della prima, ingombro massimo in pollici, tracciato)
STILI = {
    "A": (arte.Stile(nome="A", forma="capsula", n_facce=1800, dissolvenza=0.50,
                     direzione_dissolvenza=(1.0, 0.62), granuli=1400, molecole=34,
                     particelle=3200, seme=7), (3.30, 6.05), 4.7, "pk"),
    "B": (arte.Stile(nome="B", forma="capsula_aperta", n_facce=2400, dissolvenza=0.0,
                     direzione_dissolvenza=(0.25, 1.0), granuli=1500, getto=1.6, molecole=36,
                     particelle=900, seme=11), (3.45, 6.85), 5.3, "catena"),
    "C": (arte.Stile(nome="C", forma="compressa", n_facce=1500,
                     rotazioni=(("x", 38.0), ("z", -20.0)), dissolvenza=0.48,
                     direzione_dissolvenza=(1.0, 0.35), reticolo=1.0, molecole=14,
                     particelle=1800, seme=5), (3.0, 6.95), 4.5, "sigmoide"),
}


def _glow_titolo(px_w, px_h, L: LayoutPrima, dpi):
    """Alone azzurro dietro «ABC»: il testo nitido è vettoriale, qui solo la luce."""
    img = Image.new("F", (px_w, px_h), 0.0)
    f = ImageFont.truetype(str(FONT_DIR / "Montserrat-Black.ttf"), int(round(L.abc_size / I * dpi)))
    d = ImageDraw.Draw(img)
    x = (L.margine) * dpi                       # rifilo sinistro della prima = x 0 del pannello
    y = (BLEED + L.y_abc) * dpi
    d.text((x, y), TITOLO_GRANDE, font=f, fill=1.0, anchor="ls")
    a = np.asarray(img, np.float32)
    g = cv2.GaussianBlur(a, (0, 0), 0.05 * dpi) * 0.07 + cv2.GaussianBlur(a, (0, 0), 0.30 * dpi) * 0.10
    return g


def _ecg_raster(px_w, px_h, pts_in, dpi, intensita, dissolvi=None):
    e = np.zeros((px_h * 2, px_w * 2), np.float32)
    q = np.round(pts_in * dpi * 2 * 4).astype(np.int32)
    cv2.polylines(e, [q], False, 1.0, max(2, int(0.006 * dpi * 2)), cv2.LINE_8, 2)
    e = cv2.resize(e, (px_w, px_h), interpolation=cv2.INTER_AREA)
    if dissolvi is not None:
        e *= dissolvi
    return e * intensita


def motivo(variante, lato, trim_w, L: LayoutPrima):
    """Tracciato farmacologico (pollici; y dall'alto del file).
    lato = "prima": x dalla piega del dorso; "quarta": x dal bordo sinistro.
    Ritorna dict: linee [(Nx2, chiusa)], punti [(x, y, r)], tratteggi [Nx2],
    y_base (quota della linea dove attraversa il dorso)."""
    tipo = STILI[variante][3]
    x1 = BLEED + trim_w + 0.02
    out = {"linee": [], "punti": [], "tratteggi": []}
    if tipo == "pk":
        # sotto la capsula ma sopra l'area barcode della quarta (che inizia a
        # BLEED + trim_h - 0.25 - 1.2 dall'alto): margine di 0,3 in
        yb = BLEED + L.y_ecg + 0.80
        out["y_base"] = yb
        if lato == "prima":
            pts, _ = arte.curva_pk(0.0, x1, yb, dosi=0.55, intervallo=1.15, amp=0.85)
            out["linee"].append((pts, False))
            # finestra terapeutica: valle e picco allo stato stazionario
            coda = pts[pts[:, 0] > trim_w - 2.4]
            for yy in (coda[:, 1].max() + 0.06, coda[:, 1].min() - 0.06):
                out["tratteggi"].append(np.array([[0.35, yy], [trim_w - 0.35, yy]]))
        else:
            out["linee"].append((np.array([[0.0, yb], [x1, yb]]), False))
    elif tipo == "catena":
        yb = BLEED + L.y_ecg + 0.10
        out["y_base"] = yb
        x0 = 0.04 if lato == "prima" else 0.0
        pts, anelli, nodi = arte.catena_molecolare(x0, x1 - 0.04, yb, seme=4 if lato == "prima" else 8)
        if lato == "quarta":
            pts = np.vstack([pts, [[x1, yb]]])
        else:
            pts = np.vstack([[[0.0, yb]], pts])
        out["linee"].append((pts, False))
        out["linee"] += [(a_, True) for a_ in anelli]
        out["punti"] = [(x, y, 0.018) for x, y in nodi]
    else:  # sigmoide
        yb = BLEED + L.y_ecg + 0.45
        out["y_base"] = yb
        if lato == "prima":
            curva, punti = arte.curva_dose_risposta(0.0, x1, yb, BLEED + L.y_ecg - 0.9, x50=3.9, pendenza=2.0)
            out["linee"].append((curva, False))
            out["punti"] = [(x, y, 0.032) for x, y in punti]
        else:
            out["linee"].append((np.array([[0.0, yb], [x1, yb]]), False))
    return out


def _polvere(px_w, px_h, dpi, n, rng, esclusioni_px):
    I_ = np.zeros((px_h, px_w), np.float32)
    xs, ys = rng.uniform(0, px_w, n), rng.uniform(0, px_h, n)
    for x, y in zip(xs, ys):
        if any(x0 <= x <= x1 and y0 <= y <= y1 for x0, y0, x1, y1 in esclusioni_px):
            continue
        r = rng.choice([1, 1, 2]) * dpi / 400
        cv2.circle(I_, (int(x * 4), int(y * 4)), max(3, int(r * 4)), float(rng.uniform(0.05, 0.3)), -1, cv2.LINE_AA, 2)
    return I_


def _rete_quarta(px_w, px_h, dpi, rng, zona_in, esclusioni_px):
    """Frammento di rete low-poly 2D che si dissolve (angolo basso-sinistro della quarta)."""
    from scipy.spatial import Delaunay
    x0, y0, x1, y1 = (v * dpi for v in zona_in)
    # griglia triangolare con jitter (triangoli regolari, aspetto "low-poly"),
    # tenuta solo dove il peso (vicinanza all'angolo) supera una soglia rumorosa
    passo = 0.30 * dpi
    pts = []
    for j, yy in enumerate(np.arange(y0 - passo, y1 + passo, passo * 0.866)):
        for xx in np.arange(x0 - passo, x1 + passo, passo):
            pts.append((xx + (passo / 2 if j % 2 else 0), yy))
    P = np.array(pts) + rng.normal(0, passo * 0.22, (len(pts), 2))
    ang0 = np.array([x0, y1])
    dn = np.linalg.norm(P - ang0, axis=1) / np.hypot(x1 - x0, y1 - y0)
    P = P[dn + rng.normal(0, 0.12, len(P)) < 0.85]
    T = Delaunay(P)
    I_ = np.zeros((px_h * 2, px_w * 2), np.float32)
    ang = np.array([x0, y1])
    dmax = np.hypot(x1 - x0, y1 - y0)
    def peso(p):
        return np.clip(1 - np.linalg.norm(p - ang) / dmax, 0, 1) ** 1.5
    lati = set()
    for s in T.simplices:
        for i in range(3):
            a, b = sorted((s[i], s[(i + 1) % 3]))
            lati.add((a, b))
    for a, b in lati:
        pa, pb = P[a], P[b]
        if np.linalg.norm(pa - pb) > 0.5 * dpi:
            continue
        w = (peso(pa) + peso(pb)) / 2
        if rng.random() > 0.25 + w * 1.8:
            continue
        cv2.line(I_, tuple((pa * 2 * 4).astype(int)), tuple((pb * 2 * 4).astype(int)),
                 float(0.75 * w), max(2, int(dpi / 160)), cv2.LINE_8, 2)
    for p in P:
        w = peso(p)
        cv2.circle(I_, tuple((p * 2 * 4).astype(int)), int(dpi / 110 * 4 * (0.6 + w)), float(1.1 * w), -1, cv2.LINE_8, 2)
    I_ = cv2.resize(I_, (px_w, px_h), interpolation=cv2.INTER_AREA)
    for ex0, ey0, ex1, ey1 in esclusioni_px:
        I_[int(max(ey0, 0)):int(ey1), int(max(ex0, 0)):int(ex1)] = 0
    return I_


def arte_pannelli(trim_w, trim_h, variante, dpi=DPI_ARTE, forza=False):
    """Ritorna (rgb_quarta, rgb_prima) float32; usa la cache se presente."""
    CACHE.mkdir(parents=True, exist_ok=True)
    chiave = f"{variante}_{trim_w:g}x{trim_h:g}_{dpi}"
    fq, fp = CACHE / f"quarta_{chiave}.png", CACHE / f"prima_{chiave}.png"
    if fq.exists() and fp.exists() and not forza:
        lettura = lambda f: cv2.imread(str(f), cv2.IMREAD_UNCHANGED)[..., ::-1].astype(np.float32) / 65535
        return lettura(fq), lettura(fp)

    s, centro, ingombro, _ = STILI[variante]
    L = layout_prima(trim_w, trim_h)
    pw, ph = int(round((BLEED + trim_w) * dpi)), int(round((BLEED * 2 + trim_h) * dpi))
    rng = np.random.default_rng(s.seme + 100)

    # ---- PRIMA (pannello: x=0 alla piega del dorso, rifilo destro a trim_w, poi bleed) ----
    cx, cy = centro[0] * dpi, (BLEED + centro[1]) * dpi
    # le particelle che salgono si spengono prima della zona del titolo
    y_lib = (BLEED + L.y_sotto[1] + 0.15) * dpi
    rampa = np.clip((np.arange(ph) - y_lib) / (0.55 * dpi), 0, 1)[:, None] ** 1.5
    Ip = arte.render_oggetto(pw, ph, (cx, cy), ingombro * dpi, s, maschera_vuoto=rampa)
    mp = motivo(variante, "prima", trim_w, L)
    for pts, chiusa in mp["linee"]:
        Ip += _ecg_raster(pw, ph, np.vstack([pts, pts[:1]]) if chiusa else pts, dpi, 0.75)
    Ip += _glow_titolo(pw, ph, L, dpi)
    zona_titolo = (0, 0, pw, (BLEED + L.y_sotto[1] + 0.15) * dpi)
    Ip += _polvere(pw, ph, dpi, 340, rng, [zona_titolo])
    Ip = arte.bagliore(Ip, dpi, s.glow)

    # ---- QUARTA (pannello: x=0 al bordo sinistro del file, piega del dorso a destra) ----
    Iq = np.zeros((ph, pw), np.float32)
    bx = (BLEED + trim_w - BARCODE_OFF - BARCODE_W) * dpi
    by1 = (BLEED + trim_h - BARCODE_OFF) * dpi
    by0 = by1 - BARCODE_H * dpi
    barcode_px = (bx - 0.2 * dpi, by0 - 0.2 * dpi, bx + (BARCODE_W + 0.2) * dpi, by1 + 0.2 * dpi)
    testo_px = (0, 0, pw, (BLEED + L.y_ecg - 0.55) * dpi)
    sfuma = np.clip(np.linspace(-0.25, 1.4, pw) / 1.0, 0, 1)[None, :] ** 1.2     # tracciato che svanisce a sinistra
    mq = motivo(variante, "quarta", trim_w, L)
    for pts, chiusa in mq["linee"]:
        Iq += _ecg_raster(pw, ph, np.vstack([pts, pts[:1]]) if chiusa else pts, dpi, 0.55, sfuma)
    Iq += _rete_quarta(pw, ph, dpi, rng, (0.0, BLEED + L.y_ecg + 0.15, 3.4, BLEED * 2 + trim_h),
                       [barcode_px])
    Iq += _polvere(pw, ph, dpi, 220, rng, [testo_px, barcode_px])
    Iq = arte.bagliore(Iq, dpi, s.glow)
    # area barcode rigorosamente vuota
    x0, y0, x1, y1 = (int(v) for v in barcode_px)
    Iq[max(y0, 0):y1, max(x0, 0):x1] = 0

    rp, rq = arte.colora(Ip, seme=1), arte.colora(Iq, seme=2)
    for f, im in ((fq, rq), (fp, rp)):
        cv2.imwrite(str(f), (im[..., ::-1] * 65535).astype(np.uint16))
    return rq, rp


# ---------------------------------------------------------------------------
# PDF
# ---------------------------------------------------------------------------
def salva_raster(rgb, path: Path, mode, nero):
    if mode == "rgb":
        Image.fromarray((rgb * 255 + 0.5).astype(np.uint8), "RGB").save(path, quality=95, dpi=(DPI_ARTE,) * 2)
    else:
        Image.fromarray(rgb_a_cmyk(rgb, nero), "CMYK").save(path, quality=95, dpi=(DPI_ARTE,) * 2)


def ecg_vettoriale(c, pal, pts, ox, H_in, colore, larg, sfuma_da=None, sfuma_a=None):
    """Linea ECG nitida, disegnata a segmenti: dove serve sfuma verso il nero
    variando il colore dei segmenti (nessuna trasparenza)."""
    rc, gc, bc = hex_rgb(colore)
    rn, gn, bn = hex_rgb(NERO)
    c.setLineWidth(larg)
    c.setLineCap(1)
    c.setLineJoin(1)
    passo = 6
    for i in range(0, len(pts) - 1, passo):
        seg = pts[i:i + passo + 1]
        x = seg[:, 0].mean()
        t = 1.0
        if sfuma_da is not None:
            t = float(np.clip((x - sfuma_da) / (sfuma_a - sfuma_da), 0, 1)) ** 1.3
        col = "#%02X%02X%02X" % tuple(int(round((n + (v - n) * t) * 255)) for v, n in ((rc, rn), (gc, gn), (bc, bn)))
        c.setStrokeColor(pal(col) if t < 1 else pal(colore))
        p = c.beginPath()
        p.moveTo((ox + seg[0, 0]) * I, (H_in - seg[0, 1]) * I)
        for q in seg[1:]:
            p.lineTo((ox + q[0]) * I, (H_in - q[1]) * I)
        c.drawPath(p, stroke=1, fill=0)


def _punti_vettoriali(c, pal, punti, ox, H_in, colore, sfuma=None):
    """Nodi (atomi / punti sperimentali): cerchietti pieni."""
    rc, rn = np.array(hex_rgb(colore)), np.array(hex_rgb(NERO))
    for x, y, r in punti:
        t = 1.0
        if sfuma:
            t = float(np.clip((x - sfuma[0]) / (sfuma[1] - sfuma[0]), 0, 1)) ** 1.3
        col = "#%02X%02X%02X" % tuple(int(round(v * 255)) for v in rn + (rc - rn) * t)
        c.setFillColor(pal(colore) if t >= 1 else pal(col))
        c.circle((ox + x) * I, (H_in - y) * I, r * I, stroke=0, fill=1)


def costruisci(out: Path, geo: Geo, variante, mode, nero, autore, con_guide, tmp: Path):
    pal = Pal(mode, nero)
    L = layout_prima(geo.trim_w, geo.trim_h)
    rq, rp = arte_pannelli(geo.trim_w, geo.trim_h, variante)
    salva_raster(rq, tmp / "quarta.jpg", mode, nero)
    salva_raster(rp, tmp / "prima.jpg", mode, nero)

    Wp, Hp = geo.W * I, geo.H * I
    c = canvas.Canvas(str(out), pagesize=(Wp, Hp), pageCompression=1, initialFontName="Montserrat-Regular")
    c.setTitle("ABC della farmacologia clinica \u2013 copertina")
    if autore:
        c.setAuthor(autore)

    # raster dei piatti ancorati ai bordi esterni
    c.drawImage(str(tmp / "quarta.jpg"), 0, 0, geo.panel_w * I, Hp)
    c.drawImage(str(tmp / "prima.jpg"), geo.spine_x1 * I, 0, geo.panel_w * I, Hp)
    # dorso: nero ricco pieno (sormonta di 1 pt i raster per non lasciare filo)
    c.setFillColor(pal(NERO))
    c.rect(geo.spine_x0 * I - 0.5, 0, geo.spine * I + 1, Hp, stroke=0, fill=1)

    H_in = geo.H
    # tracciato farmacologico: quarta (sfuma a sinistra), dorso, prima
    mq = motivo(variante, "quarta", geo.trim_w, L)
    mp = motivo(variante, "prima", geo.trim_w, L)
    for pts, chiusa in mq["linee"]:
        ecg_vettoriale(c, pal, np.vstack([pts, pts[:1]]) if chiusa else pts, 0.0, H_in, TRACCIATO_Q, 0.6,
                       sfuma_da=0.4, sfuma_a=2.6)
    _punti_vettoriali(c, pal, mq["punti"], 0.0, H_in, TRACCIATO_Q, sfuma=(0.4, 2.6))
    yd = mp["y_base"]
    c.setStrokeColor(pal(TRACCIATO_Q))
    c.setLineWidth(0.6)
    c.line(geo.spine_x0 * I - 1, (H_in - yd) * I, geo.spine_x1 * I + 1, (H_in - yd) * I)
    c.setStrokeColor(pal(FINESTRA))
    c.setLineWidth(0.5)
    c.setDash(3, 3)
    for t in mp["tratteggi"]:
        c.line((geo.spine_x1 + t[0, 0]) * I, (H_in - t[0, 1]) * I, (geo.spine_x1 + t[1, 0]) * I, (H_in - t[1, 1]) * I)
    c.setDash()
    for pts, chiusa in mp["linee"]:
        ecg_vettoriale(c, pal, np.vstack([pts, pts[:1]]) if chiusa else pts, geo.spine_x1, H_in, TRACCIATO, 0.85)
    _punti_vettoriali(c, pal, mp["punti"], geo.spine_x1, H_in, TRACCIATO)

    # ------------------------------ PRIMA ------------------------------
    x0 = geo.spine_x1                         # rifilo sinistro della prima
    top = BLEED                               # rifilo superiore (dall'alto)
    def Y(y):                                 # pollici dall'alto del rifilo -> punti PDF
        return (H_in - (top + y)) * I
    m = L.margine
    # occhiello: FISIOLOGIA · ECG · FARMACI
    kx = (x0 + m) * I
    for i, parola in enumerate(KICKER):
        c.setFillColor(pal(GRIGIO))
        kx += testo(c, kx, Y(L.y_kicker), parola, "Montserrat-SemiBold", 9.5, 2.6)
        if i < len(KICKER) - 1:
            c.setFillColor(pal(ACCENTO))
            kx += 7
            c.circle(kx + 2, Y(L.y_kicker) + 3.4, 1.7, stroke=0, fill=1)
            kx += 11
    # «ABC» grande, azzurro
    c.setFillColor(pal(ACCENTO))
    testo(c, (x0 + m) * I - L.abc_size * 0.035, Y(L.y_abc), TITOLO_GRANDE, "Montserrat-Black", L.abc_size, -1.0)
    # «della farmacologia clinica», bianco
    c.setFillColor(pal(BIANCO))
    testo(c, (x0 + m) * I, Y(L.y_riga), TITOLO_RIGA, "Montserrat-Bold", L.riga_size, -0.2)
    # filetto azzurro
    c.setFillColor(pal(ACCENTO))
    c.rect((x0 + m) * I, Y(L.y_filetto) - 1.1, 0.62 * I, 2.2, stroke=0, fill=1)
    # sottotitolo
    for t, y in zip(SOTTOTITOLO, L.y_sotto):
        c.setFillColor(pal(BIANCO if t is SOTTOTITOLO[0] else GRIGIO))
        testo(c, (x0 + m) * I, Y(y), t, "Montserrat-Light", L.sotto_size)
    # autore (facoltativo), in basso a sinistra
    if autore:
        c.setFillColor(pal(BIANCO))
        testo(c, (x0 + m) * I, Y(geo.trim_h - 0.62), autore.upper(), "Montserrat-SemiBold", 11.5, 2.4)

    # ------------------------------ DORSO ------------------------------
    if geo.spine_text:
        cx = (geo.spine_x0 + geo.spine_x1) / 2 * I
        utile = (geo.spine - 2 * SPINE_TEXT_MARGIN) * I
        size = min(17.0, utile / 0.95)                     # maiuscole Montserrat ~0,70 em
        c.saveState()
        c.translate(cx, Hp / 2 + 0.55 * I)
        c.rotate(-90)                                      # dall'alto verso il basso
        parti = [("ABC", "Montserrat-Black", ACCENTO), ("  DELLA FARMACOLOGIA CLINICA", "Montserrat-Bold", BIANCO)]
        tr = 1.2
        tot = sum(larghezza(t, f, size, tr) for t, f, _ in parti)
        x = -tot / 2
        yb = -size * 0.35
        for t, f, col in parti:
            c.setFillColor(pal(col))
            x += testo(c, x, yb, t, f, size, tr) + tr
        c.restoreState()
        # accento: piccola capsula bicolore (metà piena, metà contorno)
        wcap = min(0.36, geo.spine - 2 * SPINE_TEXT_MARGIN - 0.04) * I
        hcap = wcap * 0.42
        ycap = (H_in - BLEED - 0.75) * I
        c.saveState()
        p = c.beginPath()
        p.roundRect(cx - wcap / 2, ycap - hcap / 2, wcap, hcap, hcap / 2)
        c.clipPath(p, stroke=0, fill=0)
        c.setFillColor(pal(ACCENTO))
        c.rect(cx - wcap / 2, ycap - hcap / 2, wcap / 2, hcap, stroke=0, fill=1)
        c.restoreState()
        c.setStrokeColor(pal(ACCENTO))
        c.setLineWidth(0.9)
        c.roundRect(cx - wcap / 2, ycap - hcap / 2, wcap, hcap, hcap / 2, stroke=1, fill=0)
        if autore:
            c.saveState()
            c.translate(cx, BLEED * I + 1.55 * I)
            c.rotate(-90)
            c.setFillColor(pal(GRIGIO))
            testo(c, 0, -size * 0.3, autore.upper(), "Montserrat-SemiBold", size * 0.62, 1.2, "center")
            c.restoreState()

    # ------------------------------ QUARTA ------------------------------
    qx = BLEED + 0.68
    maxq = geo.trim_w - 0.68 - 0.68
    def Yq(y):
        return (H_in - (BLEED + y)) * I
    y = 0.95
    c.setFillColor(pal(ACCENTO))
    w = testo(c, qx * I, Yq(y), "ABC ", "Montserrat-Black", 24)
    c.setFillColor(pal(BIANCO))
    testo(c, qx * I + w, Yq(y), TITOLO_RIGA, "Montserrat-Bold", 24, -0.1)
    y += 0.30
    c.setFillColor(pal(GRIGIO))
    testo(c, qx * I, Yq(y), " · ".join(KICKER), "Montserrat-SemiBold", 8.5, 2.2)
    y += 0.55
    c.setFillColor(pal(BIANCO))
    for r in wrap(QUARTA_INTRO, "Montserrat-Regular", 11.0, maxq * I):
        testo(c, qx * I, Yq(y), r, "Montserrat-Regular", 11.0)
        y += 17.5 / I
    y += 0.25
    for punto in QUARTA_PUNTI:
        c.setFillColor(pal(ACCENTO))
        c.rect(qx * I, Yq(y) + 2.2, 7.5, 2.2, stroke=0, fill=1)
        c.setFillColor(pal(BIANCO))
        for r in wrap(punto, "Montserrat-Medium", 10.5, (maxq - 0.3) * I):
            testo(c, (qx + 0.3) * I, Yq(y), r, "Montserrat-Medium", 10.5)
            y += 15.5 / I
        y += 0.11
    y += 0.18
    c.setFillColor(pal(GRIGIO))
    testo(c, qx * I, Yq(y), AVVERTENZA, "Montserrat-Italic", 9.0)
    fine_quarta = y

    if con_guide:
        guide(c, geo)
    c.showPage()
    c.save()
    return fine_quarta, L


def guide(c, geo: Geo):
    c.saveState()
    c.setLineWidth(0.8)
    c.setStrokeColor(Color(1, 0.15, 0.15))
    c.rect(BLEED * I, BLEED * I, (geo.W - 2 * BLEED) * I, geo.trim_h * I, stroke=1, fill=0)
    c.setStrokeColor(Color(1, 0, 1))
    for x in (geo.spine_x0, geo.spine_x1):
        c.line(x * I, 0, x * I, geo.H * I)
    c.setDash(4, 3)
    c.setStrokeColor(Color(0, 0.8, 1))
    for xa, xb in ((BLEED + SAFE, geo.spine_x0 - SAFE), (geo.spine_x1 + SAFE, geo.W - BLEED - SAFE)):
        c.rect(xa * I, (BLEED + SAFE) * I, (xb - xa) * I, (geo.trim_h - 2 * SAFE) * I, stroke=1, fill=0)
    c.setStrokeColor(Color(0.6, 0.6, 0.6))
    c.setDash(1, 3)
    for xa, xb in ((BLEED + SAFE_PRUDENTE, geo.spine_x0 - SAFE_PRUDENTE),
                   (geo.spine_x1 + SAFE_PRUDENTE, geo.W - BLEED - SAFE_PRUDENTE)):
        c.rect(xa * I, (BLEED + SAFE_PRUDENTE) * I, (xb - xa) * I, (geo.trim_h - 2 * SAFE_PRUDENTE) * I, stroke=1, fill=0)
    if geo.spine_text:
        c.setStrokeColor(Color(0, 0.8, 1))
        c.setDash(4, 3)
        c.rect((geo.spine_x0 + SPINE_TEXT_MARGIN) * I, (BLEED + SAFE) * I,
               (geo.spine - 2 * SPINE_TEXT_MARGIN) * I, (geo.trim_h - 2 * SAFE) * I, stroke=1, fill=0)
    c.setDash()
    bx, by, bw, bh = geo.barcode()
    c.setFillColor(Color(1, 1, 1))
    c.setStrokeColor(Color(1, 0.55, 0))
    c.setLineWidth(1.2)
    c.rect(bx * I, by * I, bw * I, bh * I, stroke=1, fill=1)
    c.setFillColor(Color(1, 0.45, 0))
    testo(c, (bx + bw / 2) * I, (by + bh / 2) * I + 2, "AREA CODICE A BARRE", "Montserrat-Bold", 8, 0, "center")
    testo(c, (bx + bw / 2) * I, (by + bh / 2) * I - 9, "2 × 1,2 in – lasciare libera", "Montserrat-Regular", 7, 0, "center")
    c.restoreState()


def render_png(pdf, png, dpi, crop=None):
    args = ["pdftoppm", "-png", "-r", str(dpi), "-singlefile"]
    if crop:
        x, y, w, h = crop
        args += ["-x", str(round(x * dpi)), "-y", str(round(y * dpi)), "-W", str(round(w * dpi)), "-H", str(round(h * dpi))]
    subprocess.run(args + [str(pdf), str(Path(png).with_suffix(""))], check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pagine", type=int, default=290)
    ap.add_argument("--trim", default="7x10", help="formato di rifilo in pollici, es. 7x10")
    ap.add_argument("--carta", choices=sorted(SPINE_COEF), default="bianca")
    ap.add_argument("--autore", default="")
    ap.add_argument("--variante", choices=sorted(STILI), default="A")
    ap.add_argument("--tutte", action="store_true", help="genera anche le altre varianti (PDF + anteprime)")
    ap.add_argument("--colore", choices=("cmyk", "rgb"), default="cmyk")
    ap.add_argument("--nero", choices=("ricco", "solo-k"), default="ricco")
    ap.add_argument("--rigenera-arte", action="store_true", help="ignora la cache dei raster")
    ap.add_argument("--dpi-anteprima", type=int, default=150)
    a = ap.parse_args()
    tw, th = (float(v) for v in a.trim.lower().split("x"))
    if a.pagine < 24:
        ap.error("KDP: minimo 24 pagine")
    registra_font()
    geo = Geo(tw, th, a.pagine, a.carta)
    ant = QUI / "anteprime"
    ant.mkdir(exist_ok=True)

    varianti = sorted(STILI) if a.tutte else [a.variante]
    for v in varianti:
        if a.rigenera_arte:
            arte_pannelli(tw, th, v, forza=True)
        nome = "copertina_KDP.pdf" if v == a.variante else f"copertina_KDP_variante_{v}.pdf"
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            costruisci(QUI / nome, geo, v, a.colore, a.nero, a.autore, False, tmp)
            # anteprime dalla versione RGB: i visualizzatori convertono il nero
            # ricco CMYK in un grigio-bruno che in stampa non c'è
            g = tmp / "guide.pdf"
            costruisci(g, geo, v, "rgb", a.nero, a.autore, True, tmp)
            render_png(g, ant / f"distesa_{v}_guide.png", a.dpi_anteprima)
            r = tmp / "rgb.pdf"
            costruisci(r, geo, v, "rgb", a.nero, a.autore, False, tmp)
            render_png(r, ant / f"distesa_{v}.png", a.dpi_anteprima)
            render_png(r, ant / f"prima_{v}.png", a.dpi_anteprima, (geo.spine_x1, BLEED, tw, th))

    v = a.variante
    shutil.copy(ant / f"distesa_{v}_guide.png", QUI / "copertina_anteprima.png")
    shutil.copy(ant / f"distesa_{v}.png", QUI / "copertina_anteprima_senza_guide.png")
    shutil.copy(ant / f"prima_{v}.png", QUI / "prima_di_copertina.png")
    info = {
        "titolo": "ABC della farmacologia clinica", "variante": v,
        "trim_in": [tw, th], "pagine": a.pagine, "carta": a.carta,
        "coefficiente_dorso_in": SPINE_COEF[a.carta],
        "dorso_in": round(geo.spine, 4), "dorso_mm": round(geo.spine * 25.4, 2),
        "larghezza_in": round(geo.W, 4), "altezza_in": round(geo.H, 4),
        "larghezza_mm": round(geo.W * 25.4, 2), "altezza_mm": round(geo.H * 25.4, 2),
        "testo_sul_dorso": geo.spine_text,
        "area_barcode_in": dict(zip(("x", "y_dal_basso", "w", "h"), (round(t, 4) for t in geo.barcode()))),
        "dpi_raster": DPI_ARTE, "spazio_colore": a.colore.upper(), "nero": a.nero,
        "autore": a.autore or None,
    }
    (QUI / "build_info.json").write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
