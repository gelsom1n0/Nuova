#!/usr/bin/env python3
"""
Verifiche di stampa del PDF del Volume A (adattato da libro/engine/check_fill.py).

Uso:  python3 verifica_A.py <pdf> [--sorgenti <cartella>]
Controlli
  1. formato: tutte le pagine 504 × 720 pt (7 × 10 in)
  2. font: tutti incorporati (pdffonts); elenco dei font usati
  3. colore: nessun pixel cromatico (rendering RGB a 60 dpi, tolleranza 6/255)
  4. grigi: nessuna tinta più chiara del 10 % nei CSS e negli SVG delle figure usate (statico)
  5. riempimento: nessuna pagina interna di una Parte sotto l'80 %; ultima pagina di Parte ≥ 65 %
     (le pagine con una figura a tutta pagina o l'inizio di Parte sono escluse dal controllo interno)
Esce con codice 1 se un controllo bloccante (1–4) fallisce; il riempimento è un avviso da correggere
calibrando i contenuti (aggiungere o tagliare testo, spostare figure), non lo stile.
"""
import glob
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

ENGINE = Path(__file__).resolve().parent
SOGLIA_INTERNA, SOGLIA_FINE_PARTE = 0.80, 0.65
TINTA_MIN = 0xE6  # 10 % di nero


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, check=True).stdout


def grays_in(text):
    """Colori esadecimali grigi (r=g=b) e non grigi trovati in un testo CSS/SVG."""
    out = []
    for m in re.finditer(r"#([0-9a-fA-F]{6})\b", text):
        h = m.group(1)
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
        out.append((h, r, g, b))
    return out


def main():
    a = sys.argv[1:]
    pdf = a[0]
    err, warn = [], []
    # 1. formato
    info = run(["pdfinfo", "-l", "9999", pdf])
    sizes = set(re.findall(r"Page\s+\d+ size:\s+([\d.]+ x [\d.]+) pts", info))
    npages = int(re.search(r"Pages:\s+(\d+)", info).group(1))
    if sizes != {"504 x 720"}:
        err.append(f"formato pagine non uniforme o diverso da 504 x 720 pt: {sizes}")
    # 2. font
    fonts = run(["pdffonts", pdf]).splitlines()[2:]
    names = []
    for ln in fonts:
        parts = ln.split()
        emb = parts[-5] if len(parts) >= 6 else "?"
        names.append(parts[0])
        if emb != "yes":
            err.append(f"font non incorporato: {ln}")
    # 3–5. raster
    d = tempfile.mkdtemp()
    subprocess.run(["pdftoppm", "-r", "60", "-png", pdf, d + "/pg"], check=True)
    fs = sorted(glob.glob(d + "/pg-*.png"))
    fills, colored = {}, []
    for i, f in enumerate(fs, 1):
        rgb = np.asarray(Image.open(f).convert("RGB")).astype(int)
        chroma = np.max(rgb, axis=2) - np.min(rgb, axis=2)
        if (chroma > 6).sum() > 3:
            colored.append(i)
        g = rgb.mean(axis=2)
        h = g.shape[0]
        top, bot = int(h * 0.075), int(h * 0.925)  # area di testo (margini alto/basso 0,75 in su 10 in)
        rows = np.where((g[top:bot] < 200).sum(axis=1) > 0)[0]
        fills[i] = (rows.max() + 1) / (bot - top) if len(rows) else 0.0
    if colored:
        err.append(f"pagine con colore: {colored}")
    # 4. grigi nei CSS e negli SVG (statico)
    light = set()
    srcs = [ENGINE / "style_A.css"]
    dbg = Path(pdf).parent / "debug.html"
    if dbg.exists():
        srcs += [Path(re.sub(r"^file://", "", u)) for u in re.findall(r'src="(file://[^"]+\.svg)"', dbg.read_text(encoding="utf-8"))]
    for p in srcs:
        try:
            t = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for h, r, g, b in grays_in(t):
            if not (r == g == b):
                err.append(f"colore non grigio #{h} in {p.name}")
            elif TINTA_MIN < r < 0xFF:
                light.add(f"#{h} ({p.name})")
    if light:
        err.append(f"grigi più chiari del 10 %: {sorted(light)[:10]}")
    # 5. riempimento per Parte
    starts = []
    for p in range(1, npages + 1):
        t = run(["pdftotext", "-f", str(p), "-l", str(p), "-layout", pdf, "-"])
        if re.search(r"^\s*PARTE\s+(\d+)\s*$", t, re.M):
            starts.append(p)
        if re.search(r"^\s*Indice analitico\s*$", t, re.M) and p > (starts[0] if starts else 0) and "idx" not in locals():
            idx = p
    ends = [s - 1 for s in starts[1:]] + [locals().get("idx", npages + 1) - 1]
    report = {"pagine": npages, "font": names, "parti": []}
    for k, (s, e) in enumerate(zip(starts, ends)):
        interne = [(i, round(fills[i] * 100)) for i in range(s, e) if fills[i] < SOGLIA_INTERNA]
        last = fills[e]
        report["parti"].append({"pagine": [s, e], "ultima_pagina_%": round(last * 100), "interne_sotto_80": interne})
        line = f"Parte con inizio a p.{s}: p.{s}-{e} ({e - s + 1} pag.); ultima pagina al {last * 100:.0f}%"
        if last < SOGLIA_FINE_PARTE:
            warn.append(line + f" (< {SOGLIA_FINE_PARTE * 100:.0f}%)")
        if interne:
            warn.append(f"  pagine interne sotto l'80%: {interne}")
        print(line)
    print("pagine:", npages, "| formato:", sizes, "| font:", ", ".join(names))
    for w in warn:
        print("AVVISO:", w)
    for e_ in err:
        print("ERRORE:", e_)
    report.update({"errori": err, "avvisi": warn})
    (Path(pdf).parent / "verifica_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print("ESITO:", "OK" if not err else "ERRORI BLOCCANTI")
    sys.exit(1 if err else 0)


if __name__ == "__main__":
    main()
