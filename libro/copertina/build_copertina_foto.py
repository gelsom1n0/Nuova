#!/usr/bin/env python3
"""
Copertina KDP «foto»: illustrazione fornita dall'utente (cuore anatomico,
molecole, ECG) + testo interamente vettoriale.

Prerequisito (una volta sola): python3 prepara_sfondo_foto.py
Uso:
    python3 build_copertina_foto.py --pagine 128
    python3 build_copertina_foto.py --pagine 128 --autore "Nome Cognome"

Principi:
- l'illustrazione NON viene mai deformata: scala uniforme (altezza = 9,25 in,
  ~327 dpi). È divisa in due metà: la quarta è ancorata al bordo sinistro del
  file, la prima al bordo destro. Così, al variare del numero di pagine,
  ciascun piatto resta identico rispetto al proprio rifilo; il dorso (fascia
  vettoriale della larghezza esatta) copre la giunzione;
- immagini convertite in CMYK, nessuna trasparenza nel PDF, font incorporati;
- tutto il testo è vettoriale (Gelasio, OFL), nessun testo nel raster.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from reportlab.lib.colors import Color
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas

import build_copertina as base  # geometria, specifiche KDP, colori, font, guide

QUI = Path(__file__).resolve().parent
SRC = QUI / "sorgenti_immagine"
INCH = 72.0
ORIG_W, ORIG_H = 1024, 755          # coordinate del modello originale
SPLIT = 2054                        # colonna di taglio nell'immagine 4K (centro del dorso disegnato)

# ---------------------------------------------------------------------------
# Colori (campionati dal modello)
# ---------------------------------------------------------------------------
ORO_CHIARO = "#F2E3B3"
ORO_SCURO = "#B48F52"
ORO = "#D2B878"          # etichette, filetti
AVORIO = "#ECE9E2"       # testo corrente
AVORIO_SOFT = "#BFC2C6"  # avvertenza
FORMULE = "#D3C9AA"      # formule (beige dorato tenue)
ETICH_SFERA = "#F4F1EA"
ETICH_SFERA_TENUE = "#7D8CA3"

# ---------------------------------------------------------------------------
# Testi
# ---------------------------------------------------------------------------
ETICHETTA = "FARMACOLOGIA CLINICA PER L’ASSISTENZA"
TITOLO = ("Basi di", "farmacologia clinica")
SOTTOTITOLO = ("I principali farmaci nella pratica assistenziale:",
               "dal meccanismo al letto del paziente")
EDIZIONE = "PRIMA EDIZIONE DI LAVORO"
QUARTA_INTRO = base.QUARTA_INTRO
QUARTA_PUNTI = (
    "13 classi di farmaci di uso quotidiano, dai beta-bloccanti ai gastroprotettori",
    "Schede rapide e checklist infermieristiche per somministrazione e monitoraggio",
    "Focus su cardiochirurgia e pronto soccorso",
)
AVVERTENZA = "Testo didattico: non sostituisce RCP, linee guida e giudizio clinico."
MENO = "−"
CORPO_MIN = 7.0  # KDP: corpo minimo 7 pt, vale anche per pedici e apici


def piccolo(size, k):
    return max(CORPO_MIN, size * k)


# ---------------------------------------------------------------------------
# Conversione colore immagini: stessa formula dei vettori (base.Pal)
# ---------------------------------------------------------------------------
def rgb_to_cmyk(arr: np.ndarray) -> np.ndarray:
    f = arr.astype(np.float32) / 255.0
    k = 1.0 - f.max(axis=2)
    d = np.maximum(1.0 - k, 1e-6)
    c = (1.0 - f[..., 0] - k) / d
    m = (1.0 - f[..., 1] - k) / d
    y = (1.0 - f[..., 2] - k) / d
    out = np.stack([c, m, y, k], axis=2)
    return (out.clip(0, 1) * 255 + 0.5).astype(np.uint8)


def salva_cmyk(arr_rgb: np.ndarray, path: Path, mode: str):
    if mode == "rgb":
        Image.fromarray(arr_rgb, "RGB").save(path, quality=94, subsampling=0, dpi=(327, 327))
    else:
        Image.fromarray(rgb_to_cmyk(arr_rgb), "CMYK").save(path, quality=94, dpi=(327, 327))


# ---------------------------------------------------------------------------
# Mini-impaginatore di formule (vettoriale)
# ---------------------------------------------------------------------------
class Formula:
    """Elementi: str | ('sub', s) | ('sup', s) | ('frac', [..], [..]) | ('paren', [..])"""

    def __init__(self, c, font="Gelasio", size=12.0):
        self.c, self.font, self.size = c, font, size

    def w(self, items, size) -> float:
        tot = 0.0
        for it in items:
            if isinstance(it, str):
                tot += pdfmetrics.stringWidth(it, self.font, size)
            elif it[0] in ("sub", "sup"):
                tot += pdfmetrics.stringWidth(it[1], self.font, piccolo(size, 0.68))
            elif it[0] == "frac":
                tot += max(self.w(it[1], size * 0.86), self.w(it[2], size * 0.86)) + size * 0.3
            elif it[0] == "paren":
                tot += self.w(it[1], size) + 2 * pdfmetrics.stringWidth("(", self.font, size * 1.9)
        return tot

    def draw(self, items, x, y, size=None):
        """Disegna con l'asse matematico (linea di frazione) a quota y."""
        size = size or self.size
        c = self.c
        base_y = y - size * 0.28  # baseline del testo rispetto all'asse
        for it in items:
            if isinstance(it, str):
                c.setFont(self.font, size)
                c.drawString(x, base_y, it)
                x += pdfmetrics.stringWidth(it, self.font, size)
            elif it[0] == "sub":
                c.setFont(self.font, piccolo(size, 0.68))
                c.drawString(x, base_y - size * 0.18, it[1])
                x += pdfmetrics.stringWidth(it[1], self.font, piccolo(size, 0.68))
            elif it[0] == "sup":
                c.setFont(self.font, piccolo(size, 0.68))
                c.drawString(x, base_y + size * 0.42, it[1])
                x += pdfmetrics.stringWidth(it[1], self.font, piccolo(size, 0.68))
            elif it[0] == "frac":
                fs = size * 0.86
                wn, wd = self.w(it[1], fs), self.w(it[2], fs)
                wf = max(wn, wd) + size * 0.3
                c.setLineWidth(max(0.5, size * 0.055))
                c.line(x, y, x + wf, y)
                self.draw(it[1], x + (wf - wn) / 2, y + fs * 0.62, fs)
                self.draw(it[2], x + (wf - wd) / 2, y - fs * 0.78, fs)
                x += wf
            elif it[0] == "paren":
                ps = size * 1.9
                pw = pdfmetrics.stringWidth("(", self.font, ps)
                c.setFont(self.font, ps)
                c.drawString(x, y - ps * 0.27, "(")
                x += pw
                x = self.draw(it[1], x, y, size)
                c.setFont(self.font, ps)
                c.drawString(x, y - ps * 0.27, ")")
                x += pw
        return x


CLCR_BREVE = ["ClCr = ", ("frac", ["(140 " + MENO + " età) × peso"], ["72 × Cr", ("sub", "s")])]
CLCR_COMPLETA = ["ClCr = ", ("frac", ["(140 " + MENO + " età) × peso"], ["72 × Cr", ("sub", "s")]),
                 " (× 0,85 se donna)"]
PH = ["pH = pK", ("sub", "a"), " + log ", ("frac", ["[A", ("sup", MENO), "]"], ["[HA]"])]
PH_GRANDE = ["pH = pK", ("sub", "a"), " + log", ("paren", [("frac", ["[A", ("sup", MENO), "]"], ["[HA]"])])]
VD = ["V", ("sub", "d"), " = ", ("frac", ["Dose"], ["C", ("sub", "0")])]
CL = ["Cl = ", ("frac", ["U × V"], ["P"])]


# ---------------------------------------------------------------------------
# Utilità di testo
# ---------------------------------------------------------------------------
def testo_gradiente(c, pal, x, y, testo, font, size, top, bottom, align="left", tracking=0.0):
    """Testo vettoriale riempito con una sfumatura (effetto oro metallico):
    il testo diventa tracciato di ritaglio (render mode 7) e la sfumatura vi
    viene dipinta dentro. Nessuna trasparenza."""
    w = pdfmetrics.stringWidth(testo, font, size) + tracking * (len(testo) - 1)
    if align == "center":
        x -= w / 2
    c.saveState()
    t = c.beginText(x, y)
    t.setFont(font, size)
    t.setCharSpace(tracking)
    t.setTextRenderMode(7)
    t.textOut(testo)
    t.setCharSpace(0)
    c.drawText(t)
    c.linearGradient(x, y + size * 0.75, x, y - size * 0.22, (pal(top), pal(bottom)), extend=True)
    c.restoreState()
    return w


def adatta(testi, font, size, maxw, tracking=0.0):
    while max(pdfmetrics.stringWidth(t, font, size) + tracking * (len(t) - 1) for t in testi) > maxw:
        size -= 0.25
    return size


# ---------------------------------------------------------------------------
# Costruzione
# ---------------------------------------------------------------------------
def prepara_immagini(tmp: Path, geo, mode: str):
    full = np.asarray(Image.open(SRC / "sfondo_pulito.png").convert("RGB"))
    H, W = full.shape[:2]
    ppi = H / geo.H
    back = full[:, :SPLIT]
    front = full[:, SPLIT:]
    salva_cmyk(back, tmp / "quarta.jpg", mode)
    salva_cmyk(front, tmp / "prima.jpg", mode)
    return ppi, back.shape[1] / ppi, front.shape[1] / ppi


def caduceo_patch(tmp: Path, colore_rgb, larghezza_px: int, mode: str, nome: str):
    """Caduceo ricomposto su un fondo pieno del colore del dorso (niente alfa nel PDF)."""
    cad = Image.open(SRC / "caduceo.png").convert("RGBA")
    h = round(cad.height * larghezza_px / cad.width)
    cad = cad.resize((larghezza_px, h), Image.LANCZOS)
    fondo = Image.new("RGBA", cad.size, tuple(int(v) for v in colore_rgb) + (255,))
    fondo.alpha_composite(cad)
    arr = np.asarray(fondo.convert("RGB"))
    p = tmp / f"{nome}.jpg"
    salva_cmyk(arr, p, mode)
    return p, larghezza_px, h


def costruisci(out: Path, geo, mode: str, autore: str, con_guide: bool, tmp: Path):
    pal = base.Pal(mode)
    I = INCH
    Wpt, Hpt = geo.W * I, geo.H * I
    c = canvas.Canvas(str(out), pagesize=(Wpt, Hpt), pageCompression=1, initialFontName="Gelasio")
    c.setTitle("Basi di farmacologia clinica – copertina")
    if autore:
        c.setAuthor(autore)

    ppi, w_back, w_front = prepara_immagini(tmp, geo, mode)
    # quarta ancorata a sinistra, prima ancorata a destra; stessa scala, nessuna deformazione
    c.drawImage(str(tmp / "quarta.jpg"), 0, 0, w_back * I, Hpt)
    c.drawImage(str(tmp / "prima.jpg"), Wpt - w_front * I, 0, w_front * I, Hpt)

    # conversione coordinate del modello (1024 x 755) -> punti PDF
    k = geo.H / ORIG_H  # pollici per pixel del modello

    def bx(px):  # quarta
        return px * k * I

    def fx(px):  # prima (ancorata a destra)
        return Wpt - (ORIG_W - px) * k * I

    def yy(py):  # dall'alto
        return Hpt - py * k * I

    # --- dorso: fascia vettoriale con la sfumatura verticale campionata ---
    righe = np.load(SRC / "colore_dorso_righe.npy")
    n = len(righe)
    stops = np.linspace(0, n - 1, 24).astype(int)
    colori = ["#%02X%02X%02X" % tuple(int(round(v)) for v in righe[i]) for i in stops]
    x0, x1 = geo.spine_x0 * I, geo.spine_x1 * I
    c.saveState()
    p = c.beginPath()
    p.rect(x0, 0, x1 - x0, Hpt)
    c.clipPath(p, stroke=0, fill=0)
    c.linearGradient(0, Hpt, 0, 0, [pal(h) for h in colori], positions=list(np.linspace(0, 1, len(colori))), extend=True)
    c.restoreState()

    cx = (x0 + x1) / 2
    y_cad_top, y_cad_bot = yy(84), yy(642)
    if geo.spine_text:
        # caducei (ridotti per stare nel dorso con il margine KDP di 0,0625 in)
        larg_in = min(0.17, geo.spine - 2 * base.SPINE_TEXT_MARGIN)
        larg_px = round(larg_in * 327)
        for nome, ycen_pt in (("cad_alto", y_cad_top), ("cad_basso", y_cad_bot)):
            riga = int(np.clip((Hpt - ycen_pt) / Hpt * n, 0, n - 1))
            patch, wpx, hpx = caduceo_patch(tmp, righe[riga], larg_px, mode, nome)
            wpt, hpt = larg_in * I, larg_in * I * hpx / wpx
            c.drawImage(str(patch), cx - wpt / 2, ycen_pt - hpt / 2, wpt, hpt)
        # titolo sul dorso, letto dall'alto in basso (convenzione KDP)
        disponibile = (x1 - x0) - 2 * base.SPINE_TEXT_MARGIN * I
        size = min(10.0, disponibile * 0.72)
        c.saveState()
        c.translate(cx, (y_cad_top + y_cad_bot) / 2)
        c.rotate(-90)
        c.setFillColor(pal("#E6D6A6"))
        if autore:
            base.spaced(c, -0.45 * I, -size * 0.35, "BASI DI FARMACOLOGIA CLINICA", "Gelasio-Bold", size, 1.3, "center")
            c.setFillColor(pal(AVORIO))
            base.spaced(c, 2.55 * I, -size * 0.35, autore.upper(), "Gelasio", size * 0.85, 1.0, "center")
        else:
            base.spaced(c, 0, -size * 0.35, "BASI DI FARMACOLOGIA CLINICA", "Gelasio-Bold", size, 1.5, "center")
        c.restoreState()

    # --- PRIMA DI COPERTINA ---------------------------------------------------
    fc = (geo.front_x0 + base.TRIM_W / 2) * I
    maxw = 5.0 * I  # larghezza utile del titolo (margini ≥ 0,5 in dal rifilo)
    # etichetta
    c.setFillColor(pal(ORO))
    s = adatta([ETICHETTA], "Gelasio-Bold", 10, 3.95 * I, 2.0)
    base.spaced(c, fc, yy(80), ETICHETTA, "Gelasio-Bold", s, 2.0, "center")
    c.setStrokeColor(pal(ORO))
    c.setLineWidth(0.6)
    c.line(fc - 0.36 * I, yy(88.5), fc + 0.36 * I, yy(88.5))
    # titolo in oro metallico
    st = adatta(TITOLO, "Gelasio-Bold", 46, maxw)
    testo_gradiente(c, pal, fc, yy(160), TITOLO[0], "Gelasio-Bold", st, ORO_CHIARO, ORO_SCURO, "center")
    testo_gradiente(c, pal, fc, yy(197), TITOLO[1], "Gelasio-Bold", st, ORO_CHIARO, ORO_SCURO, "center")
    # divisore con rombo
    yd = yy(242.5)
    c.setStrokeColor(pal(ORO))
    c.setFillColor(pal(ORO))
    c.setLineWidth(0.7)
    c.line(fc - 1.02 * I, yd, fc - 0.09 * I, yd)
    c.line(fc + 0.09 * I, yd, fc + 1.02 * I, yd)
    d = 0.045 * I
    p = c.beginPath()
    p.moveTo(fc, yd + d); p.lineTo(fc + d, yd); p.lineTo(fc, yd - d); p.lineTo(fc - d, yd); p.close()
    c.drawPath(p, stroke=0, fill=1)
    # sottotitolo
    ss = adatta(SOTTOTITOLO, "Gelasio-Italic", 16, maxw)
    c.setFillColor(pal(AVORIO))
    c.setFont("Gelasio-Italic", ss)
    c.drawCentredString(fc, yy(276), SOTTOTITOLO[0])
    c.drawCentredString(fc, yy(297), SOTTOTITOLO[1])

    # formule (correzione di quelle del modello: niente "age/weight/if female")
    c.setFillColor(pal(FORMULE))
    c.setStrokeColor(pal(FORMULE))
    F = Formula(c, "Gelasio", 10.5)
    F.draw(CLCR_BREVE, fx(566), yy(346))
    wph = F.w(PH, 11)
    F.draw(PH, min(fx(1000), Wpt - (0.125 + 0.45) * I) - wph, yy(352), 11)
    F.draw(VD, fx(578), yy(652), 14)
    wcl = F.w(CL, 14)
    F.draw(CL, min(fx(976), Wpt - (0.125 + 0.5) * I) - wcl, yy(650), 14)

    # etichette corrette sulle sfere (glifi raster allucinati rimossi)
    def etichetta_sfera(x, y, simbolo, apice, size, colore):
        c.setFillColor(pal(colore))
        w1 = pdfmetrics.stringWidth(simbolo, "Gelasio", size)
        w2 = pdfmetrics.stringWidth(apice, "Gelasio", piccolo(size, 0.6))
        x0s = x - (w1 + w2) / 2
        c.setFont("Gelasio", size)
        c.drawString(x0s, y - size * 0.33, simbolo)
        c.setFont("Gelasio", piccolo(size, 0.6))
        c.drawString(x0s + w1, y + size * 0.12, apice)

    etichetta_sfera(fx(830), yy(340), "Na", "+", 11.5, ETICH_SFERA)
    etichetta_sfera(fx(989), yy(460), "Ca", "2+", 8.6, ETICH_SFERA)

    # edizione
    # con autore: nome nella fascia bassa (sotto le sfere, y ≥ 680) ed edizione sotto
    c.setFillColor(pal("#CBBF9F"))
    base.spaced(c, fc, yy(721 if autore else 710), EDIZIONE, "Gelasio-Bold", 7.4, 1.9, "center")
    if autore:
        c.setFillColor(pal(AVORIO))
        base.spaced(c, fc, yy(704), autore.upper(), "Gelasio-Bold", 11, 2.2, "center")

    # --- QUARTA DI COPERTINA -------------------------------------------------
    lx = bx(60)
    maxq = geo.spine_x0 * I - 0.55 * I - lx
    c.setFillColor(pal(ORO))
    base.spaced(c, lx, yy(93), ETICHETTA, "Gelasio-Bold", 8.4, 1.7)
    sq = adatta(["Basi di farmacologia clinica"], "Gelasio-Bold", 25, maxq * 0.95)
    testo_gradiente(c, pal, lx, yy(129), "Basi di farmacologia clinica", "Gelasio-Bold", sq, ORO_CHIARO, ORO_SCURO)

    y = yy(162)
    c.setFillColor(pal(AVORIO))
    for riga in base.wrap(QUARTA_INTRO, "Gelasio", 11.6, maxq):
        c.setFont("Gelasio", 11.6)
        c.drawString(lx, y, riga)
        y -= 16.2
    y -= 0.2 * I
    for punto in QUARTA_PUNTI:
        c.setStrokeColor(pal(AVORIO))
        c.setLineWidth(0.9)
        c.circle(lx + 0.07 * I, y + 3.9, 3.3, stroke=1, fill=0)
        for riga in base.wrap(punto, "Gelasio", 11, maxq - 0.3 * I):
            c.setFillColor(pal(AVORIO))
            c.setFont("Gelasio", 11)
            c.drawString(lx + 0.3 * I, y, riga)
            y -= 15
        y -= 6
    y -= 0.08 * I
    c.setStrokeColor(pal(ORO))
    c.setLineWidth(0.6)
    c.line(lx, y + 6, lx + 0.65 * I, y + 6)
    y -= 12
    c.setFillColor(pal(AVORIO_SOFT))
    c.setFont("Gelasio-Italic", 10)
    c.drawString(lx, y, AVVERTENZA)
    fine_testo_quarta = y

    # formule della quarta
    c.setFillColor(pal(FORMULE))
    c.setStrokeColor(pal(FORMULE))
    Fq = Formula(c, "Gelasio", 14)
    Fq.draw(CLCR_COMPLETA, lx, yy(465), 14)
    # pH: deve terminare prima dell'area barcode (x 3,875 in) con margine
    bxb, byb, bwb, bhb = geo.barcode_box()
    sp = 21
    while Fq.w(PH_GRANDE, sp) > (bxb - 0.3) * I - bx(75):
        sp -= 0.5
    Fq.draw(PH_GRANDE, bx(75), yy(628), sp)

    # etichette delle due sfere tenui della quarta
    etichetta_sfera(bx(395), yy(422), "Na", "+", 10.5, ETICH_SFERA_TENUE)
    etichetta_sfera(bx(195), yy(694), "Na", "+", 11.5, ETICH_SFERA_TENUE)

    if con_guide:
        base.guide(c, geo)
    c.showPage()
    c.save()
    return fine_testo_quarta


def render_png(pdf: Path, png: Path, dpi: int, crop_in=None):
    args = ["pdftoppm", "-png", "-r", str(dpi), "-singlefile"]
    if crop_in:
        x, y, w, h = crop_in
        args += ["-x", str(round(x * dpi)), "-y", str(round(y * dpi)),
                 "-W", str(round(w * dpi)), "-H", str(round(h * dpi))]
    args += [str(pdf), str(png.with_suffix(""))]
    subprocess.run(args, check=True)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pagine", type=int, required=True)
    ap.add_argument("--carta", choices=sorted(base.SPINE_COEF), default="bianca")
    ap.add_argument("--autore", default="")
    ap.add_argument("--colore", choices=("cmyk", "rgb"), default="cmyk")
    ap.add_argument("--dpi-anteprima", type=int, default=150)
    a = ap.parse_args()
    if a.pagine < 24:
        ap.error("KDP richiede almeno 24 pagine")

    base.registra_font()
    geo = base.Geo.calcola(a.pagine, a.carta)
    if geo.spine * 327 < (SPLIT - 2000) * 2:
        print("Attenzione: dorso molto sottile; la giunzione delle due metà potrebbe vedersi.")

    ant = QUI / "anteprime"
    ant.mkdir(exist_ok=True)
    pdf = QUI / "copertina_KDP.pdf"  # file da caricare su KDP
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        costruisci(pdf, geo, a.colore, a.autore, False, tmp)
        g = tmp / "guide.pdf"
        costruisci(g, geo, "rgb", a.autore, True, tmp)
        render_png(g, ant / "distesa_foto_guide.png", a.dpi_anteprima)
    render_png(pdf, ant / "distesa_foto.png", a.dpi_anteprima)
    render_png(pdf, ant / "prima_foto.png", a.dpi_anteprima, crop_in=(geo.front_x0, base.BLEED, base.TRIM_W, base.TRIM_H))

    # anteprime principali
    shutil.copy(ant / "distesa_foto_guide.png", QUI / "copertina_anteprima.png")
    shutil.copy(ant / "distesa_foto.png", QUI / "copertina_anteprima_senza_guide.png")
    shutil.copy(ant / "prima_foto.png", QUI / "prima_di_copertina.png")

    info = {
        "variante": "foto (illustrazione dell'utente)",
        "pagine": geo.pagine, "carta": geo.carta,
        "coefficiente_dorso_in": base.SPINE_COEF[geo.carta],
        "dorso_in": round(geo.spine, 4), "dorso_mm": round(geo.spine * 25.4, 2),
        "larghezza_in": round(geo.W, 4), "altezza_in": round(geo.H, 4),
        "larghezza_mm": round(geo.W * 25.4, 2), "altezza_mm": round(geo.H * 25.4, 2),
        "testo_sul_dorso": geo.spine_text,
        "area_barcode_in": dict(zip(("x", "y_dal_basso", "w", "h"), (round(v, 4) for v in geo.barcode_box()))),
        "risoluzione_immagine_dpi": round(3021 / geo.H, 1),
        "spazio_colore": a.colore.upper(), "autore": a.autore or None,
    }
    (QUI / "build_info.json").write_text(json.dumps(info, indent=2, ensure_ascii=False) + "\n")
    print(json.dumps(info, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
