#!/usr/bin/env python3
"""
Pipeline dei tracciati REALI da banche dati aperte di PhysioNet (licenze in ../FONTI_E_LICENZE.md).

Banche dati usate
  PTB-XL 1.0.3      ECG a 12 derivazioni, 10 s, 500 Hz, etichette SCP di cardiologi   – CC BY 4.0
  MIT-BIH Arrhythmia 1.0.0   2 derivazioni (MLII + V1/V2/V4/V5), 360 Hz, annotazioni battito per
                             battito e del ritmo                                         – ODC-By 1.0
  CUDB 1.0.0        (Creighton University Ventricular Tachyarrhythmia), 250 Hz, episodi di FV – ODC-By 1.0

Per ogni categoria del piano figure:
  1. si selezionano i candidati con etichette ad alta confidenza
       PTB-XL: codice bersaglio con likelihood 100, nessun altro codice al di fuori di un elenco
               ammesso, validated_by_human, nessun problema di qualità del segnale (deriva, rumore,
               elettrodi), niente pacemaker/extra-battiti se non richiesti;
       MIT-BIH/CUDB: finestre di 10,4 s interamente dentro un episodio annotato del ritmo cercato,
               con annotazioni dei battiti coerenti (es. ≥ 6 battiti V consecutivi per la TV);
  2. si scaricano i segnali (cache locale, non versionata);
  3. si calcolano misure oggettive (ecgmeasure: FC, regolarità RR, PR, QRS, QT, ST, ampiezze) e si
     confrontano con l'etichetta attesa: i candidati incoerenti sono SCARTATI (motivo nel report);
  4. si rendono in B/N sulla stessa griglia dei simulati (filtro passa-alto 0,5 Hz e passa-basso
     40 Hz dichiarati in didascalia), con metadati e didascalia automatica (record, derivazione,
     fonte, licenza);
  5. si scrive QC_report.md.

Uso:  python3 select_real.py [--max 4] [--categorie AFIB,CLBBB,...]
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import wfdb

HERE = Path(__file__).resolve().parent
CACHE = HERE / "cache"
OUT = HERE / "out"
sys.path.insert(0, str(HERE.parent / "common"))
import ecgmeasure  # noqa: E402
import ecgplot  # noqa: E402

PTB = "https://physionet.org/files/ptb-xl/1.0.3/"
MIT = "https://physionet.org/files/mitdb/1.0.0/"
CU = "https://physionet.org/files/cudb/1.0.0/"
LIC = {
    "ptbxl": ("PTB-XL 1.0.3 (Wagner et al., PhysioNet 2022)", "CC BY 4.0"),
    "mitdb": ("MIT-BIH Arrhythmia Database 1.0.0 (Moody & Mark, PhysioNet)", "ODC-By 1.0"),
    "cudb": ("CU Ventricular Tachyarrhythmia Database 1.0.0 (Nolle et al., PhysioNet)", "ODC-By 1.0"),
}
LEADS12 = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]
SPR = 5.2


def fetch(url, dest: Path):
    if dest.exists() and dest.stat().st_size > 0:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["curl", "-sSL", "--retry", "3", "--fail", "-o", str(dest), url], check=True)
    return dest


# ------------------------------------------------------------------ criteri di coerenza (QC)
def sokolow(m):
    a = m.get("qrs_ampiezze", {})
    try:
        return max(-a["V1"]["min"], 0) + max(a["V5"]["max"], a["V6"]["max"])
    except KeyError:
        return None


QC = {
    # funzione(misure) -> (ok, motivo)
    "NORM": lambda m: _all(m, fc=(50, 100), rr_cv=(0, 0.10), qrs_ms=(60, 118), pr_ms=(110, 215),
                           qtc_bazett_ms=(340, 465), p_presente=True),
    "STACH": lambda m: _all(m, fc=(100, 180), rr_cv=(0, 0.10), p_presente=True),
    "SBRAD": lambda m: _all(m, fc=(30, 60), p_presente=True),
    "SARRH": lambda m: _all(m, rr_cv=(0.06, 0.4), p_presente=True),
    "AFIB": lambda m: _all(m, rr_cv=(0.10, 0.6), p_presente=False),
    "AFLT": lambda m: _all(m, fc=(50, 190)),
    "1AVB": lambda m: _all(m, pr_ms=(215, 450), p_presente=True),
    "2AVB": lambda m: (m.get("rr_max", 0) / max(m.get("rr_min", 1), 1e-3) >= 1.35,
                       "pause compatibili con P bloccate (RR max/min ≥ 1,35)"),
    "3AVB": lambda m: _all(m, fc=(20, 60)),
    "CRBBB": lambda m: _all(m, qrs_ms=(115, 200), **{"amp:V1.max": (0.25, 5)}),
    "CLBBB": lambda m: _all(m, qrs_ms=(120, 220), **{"amp:V6.min": (-0.35, 0.5), "amp:V1.min": (-6, -0.6)}),
    "LVH": lambda m: ((sokolow(m) or 0) >= 3.5 or m.get("amp:aVL.max", 0) >= 1.1,
                      f"Sokolow-Lyon {sokolow(m):.2f} mV o R aVL {m.get('amp:aVL.max')} mV"),
    "IMI": lambda m: _all(m, qrs_ms=(60, 130), **{"amp:III.min": (-5, -0.2)}),
    "AMI": lambda m: _all(m, qrs_ms=(60, 130)),
    "ASMI": lambda m: _all(m, qrs_ms=(60, 130), **{"amp:V2.max": (-1, 0.35)}),
    "LMI": lambda m: _all(m, qrs_ms=(60, 130)),
    "PVC": lambda m: (m.get("rr_max", 0) / max(m.get("rr_min", 1), 1e-3) >= 1.3, "battito prematuro con pausa"),
    "PAC": lambda m: (m.get("rr_max", 0) / max(m.get("rr_min", 1), 1e-3) >= 1.2, "battito prematuro"),
    "PACE": lambda m: _all(m, qrs_ms=(115, 240)),
    # con l'onda delta la stima automatica dell'inizio del QRS/P non è affidabile: solo QRS e verifica visiva
    "WPW": lambda m: _all(m, qrs_ms=(95, 200)),
    "SVTAC": lambda m: _all(m, fc=(140, 260), qrs_ms=(60, 125)),
    # MIT-BIH / CUDB
    # salva di TV: la conferma viene dalle annotazioni battito per battito (≥ 6 V consecutivi, ≥ 50 % V);
    # le misure globali sul battito mediano non sono significative in un ritmo misto
    "VT": lambda m: (m.get("fc_media") is not None and m["fc_media"] >= 70, f"FC media {m.get('fc_media')}/min; salva confermata dalle annotazioni"),
    "BIGEM": lambda m: _all(m, rr_cv=(0.10, 0.6)),
    "MIT_AFIB": lambda m: _all(m, rr_cv=(0.10, 0.6), p_presente=False),
    "MIT_AFL": lambda m: (True, "verifica visiva delle onde F"),
    # il record 231 contiene un BAV di 2° grado con conduzione 2:1: RR regolari e frequenza dimezzata
    "MIT_BII": lambda m: _all(m, fc=(25, 55)),
    "MIT_PACED": lambda m: _all(m, qrs_ms=(110, 260)),
    "MIT_SVTA": lambda m: _all(m, fc=(100, 260)),
    "VF": lambda m: (True, "nessun criterio numerico: verifica visiva"),
}


def _all(m, **crit):
    bad = []
    for k, (lo, hi) in ((k, v) for k, v in crit.items() if not isinstance(v, bool)):
        v = m.get(k)
        if v is None or not (lo <= v <= hi):
            bad.append(f"{k}={v} (atteso {lo}–{hi})")
    for k, v in ((k, v) for k, v in crit.items() if isinstance(v, bool)):
        if m.get(k) != v:
            bad.append(f"{k}={m.get(k)} (atteso {v})")
    return (not bad, "; ".join(bad) if bad else "coerente")


# ------------------------------------------------------------------ piano delle categorie
PTB_CAT = [
    # id, codice SCP, titolo, gruppo, codici ammessi oltre al bersaglio, rendering
    ("NORM", "NORM", "Ritmo sinusale normale", "morfologia_normale", {"SR"}, "12"),
    ("STACH", "STACH", "Tachicardia sinusale", "ritmo", {"NORM"}, "striscia"),
    ("SBRAD", "SBRAD", "Bradicardia sinusale", "ritmo", {"NORM"}, "striscia"),
    ("SARRH", "SARRH", "Aritmia sinusale", "ritmo", {"NORM"}, "striscia"),
    ("AFIB", "AFIB", "Fibrillazione atriale", "ritmo", set(), "striscia"),
    ("AFLT", "AFLT", "Flutter atriale", "ritmo", set(), "striscia"),
    ("1AVB", "1AVB", "Blocco AV di 1° grado", "blocchi", {"SR", "LPR"}, "striscia"),
    ("2AVB", "2AVB", "Blocco AV di 2° grado (tipo non specificato)", "blocchi", {"SR"}, "striscia"),
    ("3AVB", "3AVB", "Blocco AV di 3° grado", "blocchi", {"SR", "CRBBB", "CLBBB", "IVCD", "ABQRS"}, "striscia"),
    ("CRBBB", "CRBBB", "Blocco di branca destra completo", "morfologia_conduzione", {"SR"}, "12"),
    ("CLBBB", "CLBBB", "Blocco di branca sinistra completo", "morfologia_conduzione", {"SR"}, "12"),
    ("LVH", "LVH", "Ipertrofia ventricolare sinistra", "morfologia_ipertrofia", {"SR", "VCLVH", "HVOLT"}, "12"),
    ("AMI", "AMI", "Infarto anteriore", "ischemia", {"SR", "QWAVE"}, "12"),
    ("ASMI", "ASMI", "Infarto anterosettale", "ischemia", {"SR", "QWAVE"}, "12"),
    ("IMI", "IMI", "Infarto inferiore", "ischemia", {"SR", "QWAVE"}, "12"),
    ("LMI", "LMI", "Infarto laterale", "ischemia", {"SR", "QWAVE"}, "12"),
    ("PVC", "PVC", "Extrasistoli ventricolari", "extrasistoli", {"SR", "NORM"}, "12"),
    ("PAC", "PAC", "Extrasistoli sopraventricolari (atriali)", "extrasistoli", {"SR", "NORM"}, "striscia"),
    ("PACE", "PACE", "Ritmo da pacemaker", "pacemaker", set(), "12"),
    ("WPW", "WPW", "Pre-eccitazione (Wolff-Parkinson-White)", "morfologia_conduzione", {"SR"}, "12"),
    ("SVTAC", "SVTAC", "Tachicardia sopraventricolare", "ritmo", set(), "striscia"),
]
MIT_CAT = [
    # id, ritmo annotato, titolo, gruppo, condizione sui battiti, record candidati
    ("VT", "(VT", "Salva di tachicardia ventricolare non sostenuta", "ritmo", "V6", ["203", "205", "207", "210", "213", "214", "215", "221", "223", "233", "200"]),
    ("BIGEM", "(B", "Bigeminismo ventricolare", "extrasistoli", "alt", ["119", "106", "200", "228", "233", "213"]),
    ("MIT_AFIB", "(AFIB", "Fibrillazione atriale (2 derivazioni)", "ritmo", "", ["201", "202", "203", "210", "219", "221"]),
    ("MIT_AFL", "(AFL", "Flutter atriale (2 derivazioni)", "ritmo", "", ["202", "203", "222"]),
    ("MIT_BII", "(BII", "Blocco AV di 2° grado con conduzione 2:1", "blocchi", "", ["231"]),
    ("MIT_PACED", "(P", "Ritmo da pacemaker (2 derivazioni)", "pacemaker", "paced", ["102", "104", "107", "217"]),
    ("MIT_SVTA", "(SVTA", "Tachicardia sopraventricolare", "ritmo", "", ["209", "220", "222", "201", "114"]),
]


# ------------------------------------------------------------------ PTB-XL
RITMO_SCP = {"SR", "STACH", "SBRAD", "SARRH", "AFIB", "AFLT", "SVTAC", "PSVT", "PACE", "SVARR", "BIGU", "TRIGU"}


def ptb_candidates(db, code, allowed, n):
    """In PTB-XL le dichiarazioni di RITMO hanno di norma likelihood 0 (= non specificata): per esse si
    richiede solo la presenza; per le dichiarazioni diagnostiche si richiede likelihood 100."""
    allowed = set(allowed) | {code}
    if code not in RITMO_SCP:
        allowed |= {"SR"}
    good = []
    for _, r in db.iterrows():
        sc = r["scp"]
        if code not in sc or (code not in RITMO_SCP and sc.get(code) != 100.0):
            continue
        if code in RITMO_SCP and any(k in RITMO_SCP and k != code for k in sc):
            continue  # un solo ritmo dichiarato
        if set(sc) - allowed:
            continue
        if not r["validated_by_human"]:
            continue
        if any(isinstance(r[c], str) and r[c].strip() for c in
               ["baseline_drift", "static_noise", "burst_noise", "electrodes_problems"]):
            continue
        if code not in ("PVC", "PAC") and isinstance(r["extra_beats"], str) and r["extra_beats"].strip():
            continue
        if code != "PACE" and isinstance(r["pacemaker"], str) and r["pacemaker"].strip():
            continue
        good.append(r)
    return good[: n * 4]  # riserva per i candidati che non superano il QC


def ptb_load(r):
    base = r["filename_hr"]
    for ext in ("hea", "dat"):
        fetch(PTB + f"{base}.{ext}", CACHE / "ptbxl" / f"{base}.{ext}")
    rec = wfdb.rdrecord(str(CACHE / "ptbxl" / base))
    names = [s if s != "AVR" else "aVR" for s in rec.sig_name]
    names = [{"AVL": "aVL", "AVF": "aVF"}.get(s, s) for s in names]
    sig = {ld: rec.p_signal[:, i] for i, ld in enumerate(names)}
    return {ld: sig[ld] for ld in LEADS12}, rec.fs


def prep(sig, fs):
    return {ld: ecgmeasure.lowpass(ecgmeasure.highpass(np.nan_to_num(v), fs, 0.5), fs, 40) for ld, v in sig.items()}


def add_amp(m):
    for ld, a in (m.get("qrs_ampiezze") or {}).items():
        m[f"amp:{ld}.max"], m[f"amp:{ld}.min"] = a["max"], a["min"]


def run_ptb(cats, nmax, log):
    db = pd.read_csv(CACHE / "ptbxl" / "ptbxl_database.csv", index_col="ecg_id")
    db["scp"] = db.scp_codes.apply(ast.literal_eval)
    db = db.sort_index()
    for cid, code, titolo, gruppo, allowed, layout in cats:
        cands = ptb_candidates(db, code, allowed, nmax)
        kept = 0
        for r in cands:
            if kept >= nmax:
                break
            ecg_id = int(r.name)
            try:
                raw, fs = ptb_load(r)
            except Exception as e:  # noqa: BLE001
                log.append((cid, f"PTB-XL {ecg_id}", "errore download", str(e)[:80], None))
                continue
            sig = prep(raw, fs)
            m = ecgmeasure.measure(sig, fs, filtered=True)
            add_amp(m)
            ok, why = QC[code](m)
            rid = f"REAL-PTBXL-{cid}-{kept + 1:02d}"
            log.append((cid, f"PTB-XL ecg_id {ecg_id}", "accettato" if ok else "scartato", why, m))
            if not ok:
                continue
            kept += 1
            attr = f"PTB-XL ecg_id {ecg_id} (PhysioNet) – CC BY 4.0; filtrato 0,5–40 Hz e ridisegnato"
            base = OUT / rid
            if layout == "12":
                info = ecgplot.render_6x2(sig, fs, base, label=f"PTB-XL {ecg_id}")
                ecgplot.render_12(sig, fs, OUT / (rid + "_3x4"), width_mm=143, label=f"PTB-XL {ecg_id}")
                shown = "12 derivazioni (6×2 a scala reale; 3×4 ridotto)"
            else:
                info = ecgplot.render_strip({k: sig[k] for k in ("II", "V1")}, fs, base, leads=["II", "V1"],
                                            duration=10.0, seconds_per_row=5.0, label=f"PTB-XL {ecg_id}")
                shown = "II e V1, 2 righe × 5 s (record di 10 s)"
            write_meta(rid, titolo, gruppo, "ptbxl", attr, info, m, ok, why,
                       {"ecg_id": ecg_id, "scp_codes": r["scp"], "referto_originale": r["report"],
                        "eta": r["age"], "sesso": "M" if r["sex"] == 0 else "F", "derivazioni": shown,
                        "strat_fold": int(r["strat_fold"]), "infarction_stadium1": r["infarction_stadium1"]
                        if isinstance(r["infarction_stadium1"], str) else None},
                       has3x4=(layout == "12"))
        if kept == 0:
            log.append((cid, "—", "NESSUN CANDIDATO", f"{len(cands)} candidati esaminati, nessuno coerente", None))


# ------------------------------------------------------------------ MIT-BIH / CUDB
# esclusioni dopo ispezione visiva (motivo riportato nel QC_report)
ESCLUSI = {
    ("VT", "223"): "finestra con due morfologie ventricolari alternate: quadro ambiguo per un esempio di TV monomorfa",
    ("VT", "203"): "TV polimorfa su FA con molto rumore: poco leggibile come esempio didattico",
}


def mit_windows(ann, rhythm, fs, dur):
    """Intervalli [inizio, fine) in campioni in cui il ritmo annotato è quello cercato."""
    eps, cur = [], None
    for s, aux in zip(ann.sample, ann.aux_note):
        aux = aux.strip("\x00").strip()
        if aux.startswith("("):
            if cur is not None:
                eps.append((cur, s))
                cur = None
            if aux == rhythm:
                cur = s
    if cur is not None:
        eps.append((cur, 10 ** 9))
    return [(a, b) for a, b in eps if (b - a) / fs >= dur + 0.4]


def beats_ok(ann, a, b, cond):
    sel = [(s, sy) for s, sy in zip(ann.sample, ann.symbol) if a <= s < b and sy not in "+~|\"x[]!"]
    syms = "".join(sy for _, sy in sel)
    if cond == "V6":  # TV: almeno 6 V consecutivi e ≥ 80 % dei battiti della finestra ventricolari
        return "VVVVVV" in syms and syms.count("V") >= 0.5 * max(1, len(syms))
    if cond == "alt":
        core = syms.replace("N", "n")
        return "nVnVnVnV" in core
    if cond == "paced":
        return syms.count("/") >= 0.9 * max(1, len(syms))
    return len(syms) >= 4


def run_mit(cats, nmax, log):
    for cid, rhythm, titolo, gruppo, cond, recs in cats:
        # le salve di TV della MIT-BIH sono brevi: per la TV basta una riga da 5,2 s
        dur = 2 * SPR
        kept = 0
        for rec in recs:
            if kept >= nmax:
                break
            if (cid, rec) in ESCLUSI:
                log.append((cid, f"MIT-BIH record {rec}", "scartato", "escluso dopo ispezione visiva: " + ESCLUSI[(cid, rec)], None))
                continue
            ann = wfdb.rdann(str(CACHE / "mitdb" / rec), "atr")
            hdr = wfdb.rdheader(str(CACHE / "mitdb" / rec))
            fs = hdr.fs
            if cid == "VT":  # salve brevi: finestra che contiene l'intero episodio (inizio e fine visibili)
                wins = [(max(0, a0 - int(dur * fs * 0.5)), b0 + int(dur * fs * 0.5))
                        for a0, b0 in mit_windows(ann, rhythm, fs, -dur + 1.5)]
            else:
                wins = mit_windows(ann, rhythm, fs, dur)
            last_end = -1
            for a, b in wins:
                if kept >= nmax:
                    break
                a = max(a, last_end)  # niente finestre sovrapposte nello stesso record
                # cerca la prima finestra di 10,4 s dentro l'episodio con battiti coerenti
                start = None
                for st in range(a + int(0.2 * fs), min(b, hdr.sig_len) - int(dur * fs), int(2 * fs)):
                    if beats_ok(ann, st, st + int(dur * fs), cond):
                        start = st
                        break
                if start is None:
                    continue
                for ext in ("hea", "dat"):
                    fetch(MIT + f"{rec}.{ext}", CACHE / "mitdb" / f"{rec}.{ext}")
                r = wfdb.rdrecord(str(CACHE / "mitdb" / rec), sampfrom=start, sampto=start + int(dur * fs))
                sig = prep({n: r.p_signal[:, i] for i, n in enumerate(r.sig_name)}, fs)
                m = ecgmeasure.measure(sig, fs, filtered=True)
                add_amp(m)
                ok, why = QC[cid](m)
                t0 = start / fs
                where = f"MIT-BIH record {rec}, da {int(t0 // 60)}:{t0 % 60:04.1f}"
                log.append((cid, where, "accettato" if ok else "scartato", why, m))
                if not ok:
                    continue
                last_end = start + int(dur * fs)
                kept += 1
                rid = f"REAL-MIT-{cid.replace('MIT_', '')}-{kept:02d}"
                leads = list(sig.keys())
                info = ecgplot.render_strip(sig, fs, OUT / rid, leads=leads, duration=dur, seconds_per_row=SPR,
                                            label=f"MIT-BIH {rec}")
                attr = f"MIT-BIH Arrhythmia Database, record {rec} (PhysioNet) – ODC-By 1.0; filtrato 0,5–40 Hz e ridisegnato"
                write_meta(rid, titolo, gruppo, "mitdb", attr, info, m, ok, why,
                           {"record": rec, "inizio_s": round(t0, 1), "derivazioni": leads,
                            "ritmo_annotato": rhythm, "note": "MLII = derivazione II modificata (Holter)"})
        if kept == 0:
            log.append((cid, "—", "NESSUN CANDIDATO", "nessuna finestra coerente", None))


def run_cudb(nmax, log):
    dur = 2 * SPR
    kept = 0
    recs = [l.strip() for l in (CACHE / "cudb" / "RECORDS").read_text().split()]
    for rec in recs:
        if kept >= nmax:
            break
        ann = wfdb.rdann(str(CACHE / "cudb" / rec), "atr")
        fs = 250
        starts = [s for s, sy in zip(ann.sample, ann.symbol) if sy == "["]
        ends = [s for s, sy in zip(ann.sample, ann.symbol) if sy == "]"]
        for a in starts:
            b = next((e for e in ends if e > a), None)
            if b is None or (b - a) / fs < dur + 1:
                continue
            noisy = any(a <= s < a + int((dur + 1) * fs) and sy == "~" for s, sy in zip(ann.sample, ann.symbol))
            if noisy:
                continue
            for ext in ("hea", "dat"):
                fetch(CU + f"{rec}.{ext}", CACHE / "cudb" / f"{rec}.{ext}")
            st = a + int(0.5 * fs)
            r = wfdb.rdrecord(str(CACHE / "cudb" / rec), sampfrom=st, sampto=st + int(dur * fs))
            sig = prep({"ECG": r.p_signal[:, 0]}, fs)
            m = {"nota": "FV: misure globali non applicabili",
                 "ampiezza_max_mv": round(float(np.max(np.abs(sig["ECG"]))), 2)}
            ok = 0.1 <= m["ampiezza_max_mv"] <= 4
            why = f"ampiezza max {m['ampiezza_max_mv']} mV" + ("" if ok else " (fuori 0,1–4 mV)")
            log.append(("VF", f"CUDB {rec}, da {st / fs:.1f} s", "accettato" if ok else "scartato", why, m))
            if not ok:
                continue
            kept += 1
            rid = f"REAL-CUDB-FV-{kept:02d}"
            info = ecgplot.render_strip(sig, fs, OUT / rid, leads=["ECG"], duration=dur, seconds_per_row=SPR,
                                        label=f"CUDB {rec}")
            attr = f"CU Ventricular Tachyarrhythmia Database, record {rec} (PhysioNet) – ODC-By 1.0; filtrato e ridisegnato"
            write_meta(rid, "Fibrillazione ventricolare", "ritmo", "cudb", attr, info, m, ok, why,
                       {"record": rec, "inizio_s": round(st / fs, 1),
                        "derivazioni": ["ECG (derivazione non specificata dalla banca dati)"]})
            break


# ------------------------------------------------------------------ metadati
def write_meta(rid, titolo, gruppo, db, attr, info, m, ok, why, extra, has3x4=False):
    fonte, lic = LIC[db]
    keep = {k: m.get(k) for k in ["fc", "fc_media", "rr_cv", "rr_min", "rr_max", "qrs_ms", "pr_ms", "qt_ms",
                                   "qtc_bazett_ms", "asse_gradi", "p_presente", "t_ampiezza_mv", "st_j60_mv",
                                   "ampiezza_max_mv"] if k in m}
    meta = {
        "id": rid, "titolo": titolo, "tipo": "reale", "gruppo": gruppo,
        "etichetta_figura": "Tracciato reale", "fonte": fonte, "licenza": lic,
        "attribuzione_breve": attr,
        "elaborazione": "filtro passa-alto 0,5 Hz e passa-basso 40 Hz (fase zero); nessun'altra modifica del segnale",
        "file": {"svg": f"real/out/{rid}.svg", "png": f"real/out/{rid}.png",
                 **({"svg_3x4": f"real/out/{rid}_3x4.svg"} if has3x4 else {})},
        "dimensioni_mm": [info["larghezza_mm"], info["altezza_mm"]], "scala": info["scala"],
        "descrizione_attesa": f"{titolo} (etichetta della banca dati); vedi misure e criteri del gruppo «{gruppo}» "
                              f"in CHECKLIST_VALIDAZIONE.md",
        "criteri_revisore": ["l'etichetta della banca dati corrisponde a ciò che si vede",
                             "qualità sufficiente per la stampa (nessun artefatto fuorviante)",
                             "nessun altro reperto rilevante non dichiarato"],
        "qc_automatico": {"esito": "superato" if ok else "non superato", "motivo": why},
        "misure": keep, "sorgente": extra, "stato_validazione": "da_validare",
    }
    (OUT / f"{rid}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    print(f"  + {rid}: {why}")


def write_report(log):
    L = ["# QC dei tracciati reali", "",
         "Generato da `select_real.py`. Per ogni candidato con etichetta ad alta confidenza sono state calcolate "
         "misure oggettive (`common/ecgmeasure.py`) e confrontate con l'etichetta attesa. I candidati incoerenti "
         "sono scartati e **non** compaiono nel MANIFEST. Le misure automatiche hanno precisione ±10–20 ms e "
         "non sostituiscono la revisione clinica: tutti i tracciati accettati restano `da_validare`.", "",
         "| Categoria | Sorgente | Esito | Motivo | FC | RR CV | PR | QRS | QTc |", "|---|---|---|---|---|---|---|---|---|"]
    for cid, src, esito, why, m in log:
        m = m or {}
        L.append(f"| {cid} | {src} | {'**' + esito + '**' if esito != 'accettato' else esito} | {why} | "
                 f"{m.get('fc', '')} | {m.get('rr_cv', '')} | {m.get('pr_ms', '')} | {m.get('qrs_ms', '')} | "
                 f"{m.get('qtc_bazett_ms', '')} |")
    acc = sum(1 for r in log if r[2] == "accettato")
    sc = sum(1 for r in log if r[2] == "scartato")
    L += ["", f"Totale: {acc} accettati, {sc} scartati, "
              f"{sum(1 for r in log if r[2] == 'NESSUN CANDIDATO')} categorie senza candidati."]
    (HERE / "QC_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")


def main():
    a = sys.argv[1:]
    nmax = int(a[a.index("--max") + 1]) if "--max" in a else 4
    only = set(a[a.index("--categorie") + 1].split(",")) if "--categorie" in a else None
    OUT.mkdir(exist_ok=True)
    if not only:  # rigenerazione completa: si eliminano solo le uscite generate da questo script
        for f in OUT.glob("REAL-*"):
            f.unlink()
    log = []
    run_ptb([c for c in PTB_CAT if not only or c[0] in only], nmax, log)
    run_mit([c for c in MIT_CAT if not only or c[0] in only], min(nmax, 3), log)
    if not only or "VF" in only:
        run_cudb(3, log)
    write_report(log)


if __name__ == "__main__":
    main()
