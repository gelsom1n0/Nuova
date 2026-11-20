#!/usr/bin/env python3
"""
ecgmeasure – misure oggettive e grossolane su un ECG (simulato o reale) per il controllo di coerenza.

Non è un algoritmo diagnostico: serve a scartare record palesemente incoerenti con l'etichetta
(es. «bradicardia» con frequenza 95/min, «BAV 1°» con PR 160 ms) e a verificare che i tracciati
simulati rispettino i parametri dichiarati. Precisione attesa: ±10–20 ms sugli intervalli.

Metodo
  1. rilevazione dei QRS (wfdb.processing.XQRS se disponibile, altrimenti un rivelatore
     tipo Pan-Tompkins sull'energia della derivata di tutte le derivazioni);
  2. statistiche RR: frequenza (mediana), coefficiente di variazione, RMSSD, rapporto max/min;
  3. battito mediano per derivazione (finestra −400/+600 ms, solo battiti con RR simili);
  4. QRS: inizio/fine sulla «velocità spaziale» (somma |dV/dt| sulle derivazioni);
  5. P: deflessione più ampia nella finestra 300–40 ms prima del QRS; assente se < 0,05 mV;
  6. QT: fine della T con il metodo della tangente sulla derivazione con T più ampia;
  7. ST: livello a J+60 ms rispetto alla linea isoelettrica PR, per derivazione;
  8. asse: arcotangente delle aree nette del QRS in I e aVF.
"""
from __future__ import annotations

import math
import numpy as np
from scipy.signal import butter, filtfilt

LIMB = ["I", "II", "III", "aVR", "aVL", "aVF"]


def _bp(x, fs, lo, hi, order=2):
    b, a = butter(order, [lo / (fs / 2), min(hi / (fs / 2), 0.99)], btype="band")
    return filtfilt(b, a, x)


def highpass(x, fs, fc=0.5):
    """Rimozione della deriva della linea di base (filtro a fase zero)."""
    b, a = butter(2, fc / (fs / 2), btype="high")
    # padding lungo (fino a 3 s, con riflessione) per evitare i transitori ai bordi dei record di 10 s
    return filtfilt(b, a, x, padtype="even", padlen=min(len(x) - 1, int(3 * fs)))


def lowpass(x, fs, fc=40.0):
    b, a = butter(3, fc / (fs / 2), btype="low")
    return filtfilt(b, a, x, padtype="even", padlen=min(len(x) - 1, int(1 * fs)))


def detect_qrs(sig: dict, fs: float, use_xqrs=True):
    """Restituisce gli indici dei picchi QRS (campioni)."""
    leads = list(sig.keys())
    # energia combinata della derivata, banda 5–25 Hz
    e = np.zeros(len(sig[leads[0]]))
    for ld in leads:
        e += np.abs(np.gradient(_bp(np.asarray(sig[ld], float), fs, 5, 25)))
    w = max(1, int(0.08 * fs))
    env = np.convolve(e, np.ones(w) / w, mode="same")
    thr = 0.35 * np.percentile(env, 99)
    refr = int(0.22 * fs)
    peaks, i, n = [], 0, len(env)
    above = env > thr
    while i < n:
        if above[i]:
            j = i
            while j < n and above[j]:
                j += 1
            k = i + int(np.argmax(env[i:j]))
            if not peaks or k - peaks[-1] > refr:
                peaks.append(k)
            elif env[k] > env[peaks[-1]]:
                peaks[-1] = k
            i = j
        else:
            i += 1
    # rifinitura: picco della derivazione con ampiezza QRS maggiore (II se presente)
    ref = "II" if "II" in sig else leads[0]
    x = _bp(np.asarray(sig[ref], float), fs, 1, 40)
    out = []
    for k in peaks:
        a, b = max(0, k - int(0.06 * fs)), min(len(x), k + int(0.06 * fs))
        out.append(a + int(np.argmax(np.abs(x[a:b]))))
    return np.array(sorted(set(out)), int)


def rr_stats(peaks, fs):
    if len(peaks) < 3:
        return {"n_qrs": int(len(peaks)), "fc": None, "rr_cv": None}
    rr = np.diff(peaks) / fs
    d = np.diff(rr)
    return {
        "n_qrs": int(len(peaks)),
        "fc": round(60.0 / float(np.median(rr)), 1),
        "fc_media": round(60.0 / float(np.mean(rr)), 1),
        "rr_min": round(float(rr.min()), 3),
        "rr_max": round(float(rr.max()), 3),
        "rr_cv": round(float(np.std(rr) / np.mean(rr)), 3),
        "rmssd_ms": round(float(np.sqrt(np.mean(d ** 2)) * 1000), 1) if len(d) else None,
        "rr": [round(float(v), 3) for v in rr],
    }


def median_beats(sig, fs, peaks, pre=0.40, post=0.60, rr_tol=0.20):
    """Battito mediano per derivazione. Si usano i battiti con RR precedente vicino alla mediana
    (esclude extrasistoli e pause, che altrimenti deformerebbero il mediano)."""
    a, b = int(pre * fs), int(post * fs)
    rr = np.diff(peaks)
    med = np.median(rr) if len(rr) else None
    sel = []
    for i, k in enumerate(peaks):
        if k - a < 0 or k + b >= len(next(iter(sig.values()))):
            continue
        if med is not None and i > 0 and abs(rr[i - 1] - med) > rr_tol * med:
            continue
        if med is not None and i < len(rr) and abs(rr[i] - med) > rr_tol * med * 2.5:
            continue
        sel.append(k)
    if not sel:
        sel = [k for k in peaks if k - a >= 0 and k + b < len(next(iter(sig.values())))]
    tpl = {ld: np.median(np.stack([np.asarray(x)[k - a:k + b] for k in sel]), axis=0) for ld, x in sig.items()}
    return tpl, len(sel), a


def measure(sig: dict, fs: float, filtered=False):
    """Misure globali. sig: dict derivazione -> mV. Restituisce un dict serializzabile in JSON."""
    s = {ld: np.asarray(v, float) for ld, v in sig.items()}
    if not filtered:
        s = {ld: lowpass(highpass(v, fs, 0.5), fs, 40) for ld, v in s.items()}
    peaks = detect_qrs(s, fs)
    out = rr_stats(peaks, fs)
    out["picchi_s"] = [round(float(k) / fs, 3) for k in peaks]
    if len(peaks) < 3:
        out["nota"] = "troppo pochi QRS per le misure morfologiche"
        return out
    rr_med = float(np.median(np.diff(peaks))) / fs
    post = min(0.62, max(0.30, 0.80 * rr_med))
    pre = min(0.40, max(0.34, 0.60 * rr_med))
    tpl, nsel, z = median_beats(s, fs, peaks, pre=pre, post=post)
    out["battiti_mediano"] = nsel
    leads = list(tpl.keys())
    n = len(tpl[leads[0]])
    t = (np.arange(n) - z) / fs  # s, 0 = picco R

    # --- QRS onset/offset sulla velocità spaziale
    vel = sum(np.abs(np.gradient(tpl[ld])) for ld in leads) * fs  # mV/s
    lo_win = (t > -0.16) & (t < 0.18)
    vmax = vel[lo_win].max()
    base_v = np.percentile(vel[(t > -pre + 0.02) & (t < -0.10)], 50) if (t < -0.10).sum() > 5 else 0
    thr = base_v + 0.06 * (vmax - base_v)
    iz = z
    on = iz
    while on > 0 and t[on] > -0.14 and (vel[on] > thr or vel[max(0, on - max(1, int(0.008 * fs))):on].max() > thr):
        on -= 1
    off = iz
    while off < n - 1 and t[off] < 0.16 and (vel[off] > thr or vel[off:off + max(1, int(0.010 * fs))].max() > thr):
        off += 1
    qrs = (off - on) / fs
    out["qrs_ms"] = round(qrs * 1000)

    # --- linea isoelettrica: valore medio subito prima dell'inizio del QRS (segmento PR)
    i_iso = slice(max(0, on - int(0.030 * fs)), max(1, on - int(0.010 * fs)))
    iso = {ld: float(np.mean(tpl[ld][i_iso])) for ld in leads}

    # --- onda P
    pw0, pw1 = max(1, on - int(0.30 * fs)), on - int(0.035 * fs)
    p_amp, p_lead, p_peak = 0.0, None, None
    if pw1 > pw0 + 10:
        # P = gobba della magnitudine spaziale PIÙ VICINA al QRS (non la più ampia: in tachicardia la
        # gobba più ampia della finestra è spesso la T del battito precedente)
        from scipy.signal import find_peaks
        magp = np.sqrt(sum((tpl[ld][pw0:pw1] - iso[ld]) ** 2 for ld in leads))
        pk, _ = find_peaks(np.r_[0, magp, 0], prominence=0.03)
        pk = pk - 1
        pk = pk[(pk >= 0) & (pk < len(magp))]
        if len(pk):
            k = pw0 + int(pk[-1])
            p_peak = k
            p_lead = max(leads, key=lambda ld: abs(tpl[ld][k] - iso[ld]))
            p_amp = abs(tpl[p_lead][k] - iso[p_lead])
    # coerenza battito per battito: la P deve essere sincrona col QRS (esclude FA/dissociazione)
    p_sync = None
    if p_lead and p_amp >= 0.05:
        x = s[p_lead]
        rel = p_peak - z
        vals = []
        for k in peaks:
            j = k + rel
            if j - int(0.02 * fs) > 0 and j + int(0.02 * fs) < len(x):
                vals.append(x[j] - np.mean(x[k + (on - z) - int(0.03 * fs): k + (on - z) - int(0.01 * fs)]))
        if vals:
            v = np.array(vals)
            p_sync = round(float(np.mean(np.sign(v) == np.sign(np.median(v)))), 2)
    out["p_ampiezza_mv"] = round(p_amp, 3)
    out["p_derivazione"] = p_lead
    out["p_sincrona_frazione"] = p_sync
    out["p_presente"] = bool(p_amp >= 0.05 and (p_sync is None or p_sync >= 0.8))
    if out["p_presente"]:
        # inizio della P sulla magnitudine spaziale (robusto alle P bifasiche, es. V1)
        mag = np.sqrt(sum((tpl[ld] - iso[ld]) ** 2 for ld in leads))
        a0 = max(0, pw0 - int(0.08 * fs))
        kp = p_peak
        lvl = 0.12 * mag[kp]
        k = kp
        while k > a0 and mag[k] > lvl and not (mag[k - 1] > mag[k] and mag[k] < 0.5 * mag[kp]):
            k -= 1  # ci si ferma anche al primo minimo locale (P fusa con la T precedente)
        out["pr_ms"] = round((on - k) / fs * 1000)
    else:
        out["pr_ms"] = None

    # --- onda T e QT (metodo della tangente)
    cand = [ld for ld in ["II", "V2", "V3", "V4", "V5", "I", "V6"] if ld in tpl] or leads
    t0, t1 = off + int(0.06 * fs), min(n - 2, z + int(min(post, 0.66 * rr_med + 0.02) * fs) - 2)
    best = None
    for ld in cand:
        seg = tpl[ld][t0:t1] - iso[ld]
        if len(seg) < 10:
            continue
        k = int(np.argmax(np.abs(seg)))
        if best is None or abs(seg[k]) > best[1]:
            best = (ld, abs(seg[k]), t0 + k)
    if best:
        ld, amp, kp = best
        x = tpl[ld] - iso[ld]
        sign = np.sign(x[kp])
        d = np.gradient(x) * fs
        a, b = kp, min(n - 1, kp + int(0.20 * fs))
        km = a + int(np.argmin(sign * d[a:b])) if b > a + 2 else kp
        slope = d[km]
        tend = km - x[km] / slope * fs if slope != 0 else km
        tend = int(min(max(tend, kp), n - 1))
        qt = (tend - on) / fs
        out["t_derivazione"] = ld
        out["t_ampiezza_mv"] = round(float(x[kp]), 3)
        out["qt_ms"] = round(qt * 1000)
        out["qtc_bazett_ms"] = round(qt / math.sqrt(rr_med) * 1000)
        out["qtc_fridericia_ms"] = round(qt / rr_med ** (1 / 3) * 1000)
        # onda U: seconda gobba concordante dopo la T (se la «T» trovata è in realtà la U, la vera T
        # è la gobba precedente: è l'errore classico di lettura del QU nell'ipopotassiemia)
        from scipy.signal import find_peaks
        seg = x[t0:t1] * sign
        pk, pr_ = find_peaks(seg, prominence=0.02, distance=int(0.08 * fs))
        u = 0.0
        if len(pk) >= 2:
            u = float(seg[pk[-1]])
        else:
            u0, u1 = tend + int(0.04 * fs), min(n - 1, tend + int(0.22 * fs))
            if u1 > u0 + 5:
                u = float(max(0.0, (x[u0:u1] * sign).max()))
        out["u_ampiezza_mv"] = round(u, 3)
        out["gobbe_st_t"] = int(len(pk))

    # --- ST a J+60 ms e ampiezze per derivazione
    j60 = min(n - 1, off + int(0.06 * fs))
    out["st_j60_mv"] = {ld: round(float(tpl[ld][j60] - iso[ld]), 3) for ld in leads}
    out["qrs_ampiezze"] = {}
    for ld in leads:
        q = tpl[ld][on:off + 1] - iso[ld]
        out["qrs_ampiezze"][ld] = {"max": round(float(q.max()), 2), "min": round(float(q.min()), 2)}
    # --- asse elettrico (aree nette del QRS)
    if "I" in tpl and "aVF" in tpl:
        a1 = float(np.sum(tpl["I"][on:off + 1] - iso["I"]))
        af = float(np.sum(tpl["aVF"][on:off + 1] - iso["aVF"]))
        out["asse_gradi"] = round(math.degrees(math.atan2(af, a1)))
    return out


def check(meas: dict, crit: dict):
    """Confronta le misure con i criteri attesi. crit: chiave -> [min, max] oppure valore booleano.
    Chiavi speciali: 'st_su' / 'st_giu': {derivazione: soglia_mV}. Restituisce (ok, lista_esiti)."""
    res, ok = [], True
    for k, v in crit.items():
        if k in ("st_su", "st_giu"):
            for ld, thr in v.items():
                m = meas.get("st_j60_mv", {}).get(ld)
                good = m is not None and (m >= thr if k == "st_su" else m <= -thr)
                res.append((f"ST {ld} {'≥' if k == 'st_su' else '≤ −'}{thr}", m, good))
                ok &= good
            continue
        m = meas.get(k)
        if isinstance(v, bool):
            good = (m == v)
        elif isinstance(v, (list, tuple)) and len(v) == 2:
            good = m is not None and v[0] <= m <= v[1]
        else:
            good = (m == v)
        res.append((k, m, good))
        ok &= bool(good)
    return ok, res
