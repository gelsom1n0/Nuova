#!/usr/bin/env python3
"""Misura il riempimento delle pagine e segnala vuoti a fine Parte. Uso: check_fill.py <pdf>"""
import sys, subprocess, re, glob, os, tempfile
from PIL import Image
import numpy as np
pdf = sys.argv[1]
d = tempfile.mkdtemp()
subprocess.run(["pdftoppm","-r","40","-png",pdf,d+"/pg"],check=True)
fs = sorted(glob.glob(d+"/pg-*.png"))
fills = {}
for i,f in enumerate(fs,1):
    a = np.array(Image.open(f).convert("L")); h = a.shape[0]
    top, bot = int(h*0.085), int(h*0.915)
    rows = np.where((a[top:bot] < 200).sum(axis=1) > 0)[0]
    fills[i] = (rows.max()+1)/(bot-top) if len(rows) else 0
starts = []
for p in range(1,len(fs)+1):
    t = subprocess.run(["pdftotext","-f",str(p),"-l",str(p),"-layout",pdf,"-"],capture_output=True,text=True).stdout
    if re.search(r"^\s*PARTE (\d+|[IVX]+)\s*$", t, re.M): starts.append(p)
ends = [s-1 for s in starts[1:]] + [len(fs)]
print("pagine totali:", len(fs))
for k,(s,e) in enumerate(zip(starts,ends),1):
    print(f"Parte {k:>2}: p.{s}-{e} ({e-s+1} pag.)  ultima pagina riempita al {fills[e]*100:.0f}%")
print("pagine interne <80%:", [(i,round(v*100)) for i,v in fills.items() if v<0.8 and i>4 and i not in ends])
