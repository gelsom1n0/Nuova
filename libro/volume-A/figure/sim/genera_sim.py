#!/usr/bin/env python3
"""
Genera tutti i tracciati simulati del catalogo (catalogo_sim.py):
  out/<ID>.svg  (vettoriale, per l'impaginazione)     out/<ID>.png  (300 dpi, anteprima/alternativa)
  out/<ID>.json (metadati: parametri, descrizione attesa, criteri, misure, esito dei controlli)
  QC_sim.md     (riepilogo dei controlli automatici)
Per gli ECG a 12 derivazioni: <ID>.svg = formato 6×2 a scala reale; <ID>_3x4.svg = formato 3×4 al 55 %.

Uso:  python3 genera_sim.py [ID ...]      (senza argomenti rigenera tutto)
"""
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "common"))
import ecgsim  # noqa: E402
import ecgplot  # noqa: E402
import ecgmeasure  # noqa: E402
from catalogo_sim import CATALOGO  # noqa: E402

OUT = HERE / "out"
SPR = 5.2  # secondi per riga: (0,4 + 5,2) s × 25 mm/s = 140 mm, entra a scala reale nella gabbia (143,5 mm)

MORPH = {"bbd": ecgsim.m_bbd, "bbs": ecgsim.m_bbs}
MOD = {"resp": lambda t: 0.13 * math.sin(2 * math.pi * t / 4.6)}


def build(entry):
    fname, kw = entry["gen"]
    kw = dict(kw)
    if isinstance(kw.get("m"), str):
        kw["m"] = MORPH[kw["m"]]()
    if isinstance(kw.get("mod"), str):
        kw["mod"] = MOD[kw["mod"]]
    return getattr(ecgsim, fname)(**kw)


def extra_metrics(tr, L, meas):
    fs = tr.fs
    ii = ecgmeasure.lowpass(ecgmeasure.highpass(L["II"], fs, 0.5), fs, 40)
    meas["ampiezza_max_mv"] = round(float(np.max(np.abs(ii[int(0.5 * fs):-int(0.5 * fs)]))), 3)
    n_p = sum(1 for e in tr.eventi if e["tipo"].startswith("P") and e["t"] < tr.durata - 0.1)
    n_q = meas.get("n_qrs") or 0
    meas["n_p_eventi"] = n_p
    meas["rapporto_p_qrs"] = round(n_p / n_q, 2) if n_q else None
    for ld, a in (meas.get("qrs_ampiezze") or {}).items():
        meas[f"amp:{ld}.max"] = a["max"]
        meas[f"amp:{ld}.min"] = a["min"]


def main(ids):
    OUT.mkdir(exist_ok=True)
    rows = []
    for e in CATALOGO:
        if ids and e["id"] not in ids:
            continue
        tr = build(e)
        L = tr.leads()
        meas = ecgmeasure.measure(L, tr.fs)
        extra_metrics(tr, L, meas)
        ok, res = ecgmeasure.check(meas, e["auto"])
        base = OUT / e["id"]
        if e["layout"] == "12":
            info = ecgplot.render_6x2(L, tr.fs, base, label=e["id"])
            info_3x4 = ecgplot.render_12(L, tr.fs, OUT / (e["id"] + "_3x4"), width_mm=143, label=e["id"])
            leads_shown = ecgsim.LEADS
        else:
            info = ecgplot.render_strip(L, tr.fs, base, leads=e["derivazioni"], duration=2 * SPR,
                                        seconds_per_row=SPR, label=e["id"])
            info_3x4 = None
            leads_shown = e["derivazioni"]
        fname, kw = e["gen"]
        keep = {k: meas[k] for k in ["fc", "fc_media", "rr_cv", "rmssd_ms", "n_qrs", "qrs_ms", "pr_ms", "qt_ms",
                                      "qtc_bazett_ms", "qtc_fridericia_ms", "asse_gradi", "p_presente",
                                      "p_ampiezza_mv", "t_ampiezza_mv", "u_ampiezza_mv", "ampiezza_max_mv",
                                      "rapporto_p_qrs", "st_j60_mv"] if k in meas}
        meta = {
            "id": e["id"], "titolo": e["titolo"], "tipo": "simulato", "gruppo": e["gruppo"],
            "etichetta_figura": "Tracciato didattico simulato",
            "fonte": "Generato con codice per questo volume (figure/sim/ecgsim.py, modello a dipolo)",
            "licenza": "Originale del volume",
            "modello": {"funzione": fname, "parametri": kw, "fs_hz": tr.fs},
            "layout": "12 derivazioni 6x2 (scala reale) + 3x4 (55 %)" if e["layout"] == "12" else
                      f"striscia {', '.join(leads_shown)} – {info['righe']} righe × {SPR} s",
            "carta": "25 mm/s, 10 mm/mV",
            "file": {"svg": f"sim/out/{e['id']}.svg", "png": f"sim/out/{e['id']}.png",
                     **({"svg_3x4": f"sim/out/{e['id']}_3x4.svg"} if info_3x4 else {})},
            "dimensioni_mm": [info["larghezza_mm"], info["altezza_mm"]], "scala": info["scala"],
            "descrizione_attesa": e["attesa"],
            "criteri_automatici": [{"criterio": c, "misura": m if not isinstance(m, dict) else None, "ok": bool(g)}
                                   for c, m, g in res],
            "esito_controllo_automatico": "superato" if ok else "NON superato",
            "criteri_revisore": e["revisore"], "affidabilita_modello": e["affidabilita"],
            "nota": e.get("nota", ""), "misure": keep,
            "eventi": tr.eventi[:60],
            "stato_validazione": "da_validare",
        }
        (OUT / f"{e['id']}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1, default=float),
                                             encoding="utf-8")
        rows.append((e, ok, res, keep))
        print(f"{e['id']:<12} {'OK ' if ok else 'KO '} " + "; ".join(f"{c}={m}" for c, m, g in res if not g))
    if not ids:
        write_qc(rows)


def write_qc(rows):
    L = ["# Controllo automatico dei tracciati simulati", "",
         "Generato da `genera_sim.py`. Le misure sono calcolate da `common/ecgmeasure.py` sul segnale simulato, "
         "come se fosse un tracciato sconosciuto (QRS rilevati, battito mediano, metodo della tangente per il QT). "
         "Precisione attesa ±10–20 ms. Il controllo automatico **non sostituisce** la revisione clinica "
         "(stato di tutti i tracciati: `da_validare`).", "",
         "| ID | Titolo | Affidabilità | FC | RR CV | PR ms | QRS ms | QTc ms | P | Esito | Criteri falliti |",
         "|---|---|---|---|---|---|---|---|---|---|---|"]
    for e, ok, res, m in rows:
        failed = "; ".join(f"{c} = {v}" for c, v, g in res if not g) or "—"
        L.append(f"| {e['id']} | {e['titolo']} | {e['affidabilita']} | {m.get('fc')} | {m.get('rr_cv')} | "
                 f"{m.get('pr_ms')} | {m.get('qrs_ms')} | {m.get('qtc_bazett_ms')} | "
                 f"{'sì' if m.get('p_presente') else 'no'} | {'superato' if ok else '**NON superato**'} | {failed} |")
    L += ["", "Note: per FV, torsione di punta e alcune extrasistoli le misure globali (FC, QRS mediano) non sono "
          "significative e non sono usate come criterio; la verifica è affidata al revisore."]
    (HERE / "QC_sim.md").write_text("\n".join(L) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(set(sys.argv[1:]))
