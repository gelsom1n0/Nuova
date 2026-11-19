#!/usr/bin/env python3
"""
ecgplot – rendering in bianco e nero di tracciati ECG su carta millimetrata standard.

Usato sia dai tracciati simulati (figure/sim) sia da quelli reali (figure/real), così che
tutte le figure del volume abbiano la stessa griglia:
  * 25 mm/s e 10 mm/mV (valori standard; modificabili solo esplicitamente);
  * quadretti piccoli 1 mm (0,04 s × 0,1 mV) e grandi 5 mm (0,20 s × 0,5 mV);
  * impulso di calibrazione 1 mV × 0,2 s all'inizio di ogni riga;
  * solo nero e grigi (tinta minima 10 %: il grigio più chiaro usato è il 22 %);
  * tutte le linee ≥ 0,75 pt (raccomandazione KDP per l'interno in B/N).

Le dimensioni fisiche del file (SVG/PDF) corrispondono alla scala dichiarata: con scala 1,0
un quadretto piccolo misura davvero 1 mm sulla pagina stampata. Il testo è convertito in tracciati
(svg.fonttype = 'path'), quindi i file non richiedono font installati in fase di impaginazione.

Layout disponibili
  render_strip(...)  : una o più derivazioni, ciascuna su una o più righe (striscia del ritmo)
  render_12(...)     : 12 derivazioni nel formato 3×4 (2,5 s per colonna) + striscia di ritmo
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.collections import LineCollection  # noqa: E402

# ---------------------------------------------------------------- costanti grafiche
MM_PER_S = 25.0          # velocità carta standard
MM_PER_MV = 10.0         # guadagno standard
GRID_MINOR = "#c7c7c7"   # 22 % di nero (≥ 10 %, minimo KDP per i grigi)
GRID_MAJOR = "#7a7a7a"   # 52 % di nero
GRID_DOT = "#8c8c8c"     # punti dei quadretti piccoli a scala ridotta
TRACE = "#000000"
LW_MINOR_PT = 0.75       # spessori in punti tipografici: KDP raccomanda linee ≥ 0,75 pt
LW_MAJOR_PT = 1.00       # (gli spessori non si riducono con la scala della figura)
LW_TRACE_PT = 1.25
CAL_W_S = 0.20           # larghezza impulso di calibrazione
CAL_MARGIN_S = 0.40      # spazio a sinistra riservato alla calibrazione
MM = 1 / 25.4            # mm -> pollici

matplotlib.rcParams.update({
    "svg.fonttype": "path",        # testo convertito in curve: nessun font da incorporare
    "pdf.fonttype": 42,
    "font.family": "DejaVu Sans",
    "font.size": 6.5,
    "svg.hashsalt": "ecg-volume-A",  # SVG deterministici (diff puliti in git)
    "path.simplify": True,          # unisce i segmenti quasi collineari (errore < 0,02 mm)
    "path.simplify_threshold": 0.05,
})


def _grid(ax, x0_mm, x1_mm, y0_mm, y1_mm, scale=1.0):
    """Disegna la griglia millimetrata (1 mm e 5 mm) nel rettangolo dato.

    A scala ridotta (< 0,75: tipicamente l'ECG a 12 derivazioni nella gabbia di testo) le righe
    da 1 mm, con spessore minimo 0,75 pt, coprirebbero metà della carta: i quadretti piccoli
    diventano allora punti agli incroci, i quadretti grandi restano linee.
    """
    minor, major = [], []
    if scale < 0.75:
        xs = [i for i in range(int(math.floor(x0_mm)), int(math.ceil(x1_mm)) + 1)]
        ys = [j for j in range(int(math.floor(y0_mm)), int(math.ceil(y1_mm)) + 1)]
        # punti come linee verticali tratteggiate (un tratto quasi nullo con estremità tonde = un punto
        # ogni 1 mm): pochi oggetti nel file vettoriale invece di migliaia di marcatori
        step_pt = 72 / 25.4 * scale  # 1 mm in punti alla scala della figura
        dots = [[(i, y0_mm), (i, y1_mm)] for i in xs if i % 5]
        ax.add_collection(LineCollection(dots, colors=GRID_DOT, linewidths=LW_MINOR_PT, capstyle="round",
                                         linestyles=[(0, (0.001, step_pt / LW_MINOR_PT))], zorder=1))
        for i in xs:
            if i % 5 == 0:
                major.append([(i, y0_mm), (i, y1_mm)])
        for j in ys:
            if j % 5 == 0:
                major.append([(x0_mm, j), (x1_mm, j)])
        ax.add_collection(LineCollection(major, colors=GRID_MAJOR, linewidths=LW_MINOR_PT, zorder=2))
        return
    for i in range(int(math.floor(x0_mm)), int(math.ceil(x1_mm)) + 1):
        (major if i % 5 == 0 else minor).append([(i, y0_mm), (i, y1_mm)])
    for j in range(int(math.floor(y0_mm)), int(math.ceil(y1_mm)) + 1):
        (major if j % 5 == 0 else minor).append([(x0_mm, j), (x1_mm, j)])
    ax.add_collection(LineCollection(minor, colors=GRID_MINOR, linewidths=LW_MINOR_PT, zorder=1))
    ax.add_collection(LineCollection(major, colors=GRID_MAJOR, linewidths=LW_MAJOR_PT, zorder=2))


def _calibration(ax, x_mm, base_mm, gain=MM_PER_MV):
    """Impulso di calibrazione 1 mV × 0,2 s (gradino rettangolare)."""
    w = CAL_W_S * MM_PER_S
    xs = [x_mm, x_mm + 2, x_mm + 2, x_mm + 2 + w, x_mm + 2 + w, x_mm + 4 + w]
    ys = [base_mm, base_mm, base_mm + gain, base_mm + gain, base_mm, base_mm]
    ax.plot(xs, ys, color=TRACE, lw=LW_TRACE_PT, solid_joinstyle="miter", zorder=4)


def _robust(s):
    """Segnale senza gli spike di stimolazione (≤ 3 ms): l'altezza della riga dipende dalle onde,
    non dagli spike, che vengono poi tagliati al bordo della riga."""
    from scipy.signal import medfilt
    s = np.asarray(s, float)
    return medfilt(s, 9) if len(s) > 9 else s


def _row_extent(segments, pad_mv=0.25):
    """Restituisce (min, max) in mV di un insieme di segmenti, arrotondati al quadretto grande."""
    lo = min(float(np.nanmin(_robust(s))) for s in segments)
    hi = max(float(np.nanmax(_robust(s))) for s in segments)
    lo = min(lo - pad_mv, -0.5)
    hi = max(hi + pad_mv, 1.2)          # spazio per l'impulso di calibrazione (1 mV)
    lo = math.floor(lo * 2) / 2          # multipli di 0,5 mV = 5 mm
    hi = math.ceil(hi * 2) / 2
    return lo, hi


def _finish(fig, out_base: Path, formats, dpi):
    out_base = Path(out_base)
    out_base.parent.mkdir(parents=True, exist_ok=True)
    written = []
    for fmt in formats:
        p = out_base.with_suffix("." + fmt)
        kw = {"dpi": dpi} if fmt == "png" else {}
        if fmt == "svg":
            kw["metadata"] = {"Date": None}
        if fmt == "pdf":
            kw["metadata"] = {"CreationDate": None, "ModDate": None}
        fig.savefig(p, format=fmt, facecolor="white", **kw)
        if fmt == "png":  # scala di grigi a 8 bit: più leggero e garantito senza colore
            from PIL import Image
            Image.open(p).convert("L").save(p, optimize=True, dpi=(dpi, dpi))
        written.append(str(p))
    plt.close(fig)
    return written


def _new_fig(w_mm, h_mm, scale):
    fig = plt.figure(figsize=(w_mm * scale * MM, h_mm * scale * MM))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w_mm)
    ax.set_ylim(0, h_mm)
    ax.set_axis_off()
    return fig, ax


def _draw_annotations(ax, annotations, x_of_t, base_mm, t0, t1):
    """Annotazioni didattiche: etichette sopra il tracciato e parentesi per gli intervalli.

    annotations: lista di dict
      {"t": 1.23, "testo": "P"}                     -> etichetta centrata in t (s)
      {"t": 1.10, "t2": 1.30, "testo": "PR 0,20 s"} -> parentesi orizzontale tra t e t2
      opzionale "y": quota in mV (default 1,6 mV sopra la linea di base)
    """
    for a in annotations or []:
        t = a["t"]
        if t < t0 or t > t1:
            continue
        y = base_mm + a.get("y", 1.6) * MM_PER_MV
        if "t2" in a:
            xa, xb = x_of_t(t), x_of_t(min(a["t2"], t1))
            ax.plot([xa, xa, xb, xb], [y - 1.2, y, y, y - 1.2], color=TRACE, lw=0.75, zorder=5)
            ax.text((xa + xb) / 2, y + 0.6, a["testo"], ha="center", va="bottom", fontsize=6, zorder=6,
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.4))
        else:
            ax.text(x_of_t(t), y, a["testo"], ha="center", va="bottom", fontsize=6.5, zorder=6,
                    fontweight="bold", bbox=dict(facecolor="white", edgecolor="none", pad=0.4))


def render_strip(signals: dict, fs: float, out_base, leads=None, t_start=0.0, duration=None,
                 seconds_per_row=None, scale=1.0, label=None, annotations=None,
                 formats=("svg", "png"), dpi=300, show_speed=True):
    """Striscia del ritmo: per ogni derivazione richiesta, una o più righe consecutive.

    signals          dict derivazione -> array in mV (stessa frequenza di campionamento fs)
    leads            derivazioni da mostrare (default: tutte, nell'ordine del dict)
    duration         durata totale mostrata (s); seconds_per_row la spezza su più righe
    scale            1,0 = scala reale (1 mm = 1 mm); <1 riduce tutto in proporzione
    label            testo piccolo in basso a destra (es. ID figura)
    annotations      vedi _draw_annotations (applicate alla prima derivazione)
    Ritorna: dict con file scritti e dimensioni fisiche (mm).
    """
    leads = leads or list(signals.keys())
    n = len(next(iter(signals.values())))
    total = n / fs - t_start
    duration = min(duration or total, total)
    spr = seconds_per_row or duration
    nrows_per_lead = int(math.ceil(duration / spr - 1e-9))

    rows = []  # (lead, t0, t1)
    for ld in leads:
        for k in range(nrows_per_lead):
            t0 = t_start + k * spr
            rows.append((ld, t0, min(t0 + spr, t_start + duration)))

    segs = {}
    for ld, t0, t1 in rows:
        i0, i1 = int(round(t0 * fs)), int(round(t1 * fs))
        segs[(ld, t0)] = np.asarray(signals[ld][i0:i1], float)
    # altezza riga uniforme (stessa per tutte le righe: confronto visivo onesto)
    lo, hi = _row_extent(list(segs.values()))
    row_h = (hi - lo) * MM_PER_MV
    w_mm = (CAL_MARGIN_S + spr) * MM_PER_S
    foot = 4.0 if (show_speed or label) else 0.0
    h_mm = row_h * len(rows) + foot
    w_mm = math.ceil(w_mm / 5) * 5
    h_mm = math.ceil(h_mm / 5) * 5
    fig, ax = _new_fig(w_mm, h_mm, scale)
    _grid(ax, 0, w_mm, 0, h_mm, scale)

    for r, (ld, t0, t1) in enumerate(rows):
        top = h_mm - r * row_h
        base = top - hi * MM_PER_MV
        _calibration(ax, 1.0, base)
        y = np.clip(segs[(ld, t0)], lo - 0.05, hi - 0.1)  # spike tagliati al bordo della riga
        x = CAL_MARGIN_S * MM_PER_S + np.arange(len(y)) / fs * MM_PER_S
        ax.plot(x, base + y * MM_PER_MV, color=TRACE, lw=LW_TRACE_PT, solid_joinstyle="round",
                solid_capstyle="round", zorder=4)
        ax.text(CAL_MARGIN_S * MM_PER_S + 1.0, top - 2.6, ld, fontsize=7, fontweight="bold", va="center",
                ha="left", zorder=6, bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
        if r == 0 and annotations:
            _draw_annotations(ax, annotations, lambda t: CAL_MARGIN_S * MM_PER_S + (t - t0) * MM_PER_S,
                              base, t0, t1)
    _footer(ax, w_mm, label, show_speed)
    files = _finish(fig, out_base, formats, dpi)
    return {"file": files, "larghezza_mm": w_mm * scale, "altezza_mm": h_mm * scale, "scala": scale,
            "secondi_per_riga": spr, "righe": len(rows)}


def _footer(ax, w_mm, label, show_speed):
    txt = []
    if show_speed:
        txt.append("25 mm/s · 10 mm/mV")
    if label:
        txt.append(label)
    if txt:
        ax.text(w_mm - 1.0, 1.0, "   ".join(txt), fontsize=5.5, ha="right", va="bottom", zorder=6,
                color="#000000", bbox=dict(facecolor="white", edgecolor="none", pad=0.5))


LAYOUT_12 = [["I", "aVR", "V1", "V4"], ["II", "aVL", "V2", "V5"], ["III", "aVF", "V3", "V6"]]


def render_12(signals: dict, fs: float, out_base, t_start=0.0, rhythm_lead="II", col_s=2.5,
              scale=None, width_mm=None, label=None, formats=("svg", "png"), dpi=300, row_mv=None,
              show_speed=True):
    """ECG a 12 derivazioni, formato 3×4 (2,5 s per colonna) + striscia di ritmo da 10 s.

    La larghezza naturale è (0,4 + 4×2,5) s × 25 mm/s = 260 mm: per stare nella gabbia del
    volume (143 mm) serve scala ≈ 0,55, oppure una figura ruotata a piena pagina (scala ≈ 0,8).
    Se width_mm è dato, la scala viene calcolata di conseguenza.
    """
    total_s = CAL_MARGIN_S + 4 * col_s
    w_mm = total_s * MM_PER_S
    if width_mm and not scale:
        scale = width_mm / w_mm
    scale = scale or 1.0
    # altezza di riga: dall'ampiezza effettiva (minimo 25 mm = 2,5 mV)
    rows = LAYOUT_12 + ([[rhythm_lead]] if rhythm_lead else [])
    extents = []
    for r, row in enumerate(rows):
        segs = []
        for c, ld in enumerate(row):
            dur = 4 * col_s if len(row) == 1 else col_s
            t0 = t_start + (0 if len(row) == 1 else c * col_s)
            i0, i1 = int(round(t0 * fs)), int(round((t0 + dur) * fs))
            segs.append(np.asarray(signals[ld][i0:i1], float))
        extents.append(_row_extent(segs, pad_mv=0.15))
    if row_mv:
        extents = [(-row_mv / 2 + 0.25, row_mv / 2 + 0.25) for _ in extents]
    heights = [(hi - lo) * MM_PER_MV for lo, hi in extents]
    foot = 4.0
    h_mm = math.ceil((sum(heights) + foot) / 5) * 5
    fig, ax = _new_fig(w_mm, h_mm, scale)
    _grid(ax, 0, w_mm, 0, h_mm, scale)
    top = h_mm
    for r, row in enumerate(rows):
        lo, hi = extents[r]
        base = top - hi * MM_PER_MV
        _calibration(ax, 1.0, base)
        for c, ld in enumerate(row):
            if len(row) == 1:
                t0, dur, x0 = t_start, 4 * col_s, CAL_MARGIN_S * MM_PER_S
            else:
                t0, dur, x0 = t_start + c * col_s, col_s, (CAL_MARGIN_S + c * col_s) * MM_PER_S
            i0, i1 = int(round(t0 * fs)), int(round((t0 + dur) * fs))
            y = np.asarray(signals[ld][i0:i1], float)
            y = np.clip(y, lo - 0.05, hi - 0.1)
            x = x0 + np.arange(len(y)) / fs * MM_PER_S
            ax.plot(x, base + y * MM_PER_MV, color=TRACE, lw=LW_TRACE_PT, solid_joinstyle="round", zorder=4)
            if c > 0 and len(row) > 1:  # piccolo marcatore di cambio derivazione
                ax.plot([x0, x0], [base + 3, base + 6], color=TRACE, lw=LW_TRACE_PT, zorder=4)
            ax.text(x0 + 1.2, top - 2.6, ld, fontsize=7, fontweight="bold", va="center", ha="left", zorder=6,
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
        top -= heights[r]
    _footer(ax, w_mm, label, show_speed)
    files = _finish(fig, out_base, formats, dpi)
    return {"file": files, "larghezza_mm": round(w_mm * scale, 1), "altezza_mm": round(h_mm * scale, 1),
            "scala": round(scale, 3), "formato": "3x4 + ritmo" if rhythm_lead else "3x4"}


LAYOUT_6x2 = [["I", "V1"], ["II", "V2"], ["III", "V3"], ["aVR", "V4"], ["aVL", "V5"], ["aVF", "V6"]]


def render_6x2(signals: dict, fs: float, out_base, t_start=0.0, col_s=2.6, scale=1.0, label=None,
               formats=("svg", "png"), dpi=300, show_speed=True):
    """ECG a 12 derivazioni in formato 6×2 (periferiche a sinistra, precordiali a destra; colonne
    consecutive di col_s secondi). Con col_s = 2,6 s la larghezza è 140 mm: entra a SCALA REALE
    nella gabbia di testo del volume (143,5 mm)."""
    w_mm = math.ceil((CAL_MARGIN_S + 2 * col_s) * MM_PER_S / 5) * 5
    extents = []
    for row in LAYOUT_6x2:
        segs = []
        for c, ld in enumerate(row):
            t0 = t_start + c * col_s
            segs.append(np.asarray(signals[ld][int(round(t0 * fs)):int(round((t0 + col_s) * fs))], float))
        extents.append(_row_extent(segs, pad_mv=0.15))
    heights = [(hi - lo) * MM_PER_MV for lo, hi in extents]
    h_mm = math.ceil((sum(heights) + 4.0) / 5) * 5
    fig, ax = _new_fig(w_mm, h_mm, scale)
    _grid(ax, 0, w_mm, 0, h_mm, scale)
    top = h_mm
    for r, row in enumerate(LAYOUT_6x2):
        lo, hi = extents[r]
        base = top - hi * MM_PER_MV
        _calibration(ax, 1.0, base)
        for c, ld in enumerate(row):
            t0 = t_start + c * col_s
            x0 = (CAL_MARGIN_S + c * col_s) * MM_PER_S
            y = np.asarray(signals[ld][int(round(t0 * fs)):int(round((t0 + col_s) * fs))], float)
            y = np.clip(y, lo - 0.05, hi - 0.1)
            x = x0 + np.arange(len(y)) / fs * MM_PER_S
            ax.plot(x, base + y * MM_PER_MV, color=TRACE, lw=LW_TRACE_PT, solid_joinstyle="round", zorder=4)
            if c > 0:
                ax.plot([x0, x0], [base + 3, base + 6], color=TRACE, lw=LW_TRACE_PT, zorder=4)
            ax.text(x0 + 1.2, top - 2.6, ld, fontsize=7, fontweight="bold", va="center", ha="left", zorder=6,
                    bbox=dict(facecolor="white", edgecolor="none", pad=0.6))
        top -= heights[r]
    _footer(ax, w_mm, label, show_speed)
    files = _finish(fig, out_base, formats, dpi)
    return {"file": files, "larghezza_mm": round(w_mm * scale, 1), "altezza_mm": round(h_mm * scale, 1),
            "scala": scale, "formato": "6x2"}
