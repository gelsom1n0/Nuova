#!/usr/bin/env python3
"""
Rendering procedurale del cuore "digitale" low-poly (opera originale).

Pipeline:
  maglia 3D (cuore_mesh.py) -> rotazione + proiezione prospettica ->
  facce frontali con ombreggiatura tenue (volume) + spigoli (frontali brillanti,
  posteriori in trasparenza "olografica") + nodi luminosi + particelle che si
  staccano dalla superficie e si dissolvono -> bagliore gaussiano a più scale ->
  mappatura tonale rosso -> bianco caldo -> fondo nero con dithering.

Tutto è calcolato in un canale di intensità I (lineare, additivo), poi colorato:
  rgb = 1 - exp(-I * K)   con K = (2.4, 0.22, 0.36)
che dà cremisi (#C8102E circa) alle basse intensità e un bianco-rosa ai picchi,
come una luce rossa satura che "brucia" al centro.

Il disegno avviene in super-campionamento 2x (antialias per media d'area).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import cv2
import numpy as np

QUI = Path(__file__).resolve().parent
K_COLORE = np.array([2.3, 0.13, 0.30], np.float32)   # R, G, B
FONDO = 5 / 255.0                                     # #050505


@dataclass
class Stile:
    nome: str = "A"
    n_facce: int = 2600
    rot_y: float = -18.0
    rot_x: float = 6.0
    spigoli_fronte: float = 0.62     # intensità spigoli frontali
    spigoli_retro: float = 0.11      # spigoli posteriori (effetto trasparenza)
    facce: float = 0.055              # riempimento delle facce frontali
    nodi: float = 1.0
    frazione_nodi_luce: float = 0.10  # nodi con alone
    particelle: int = 2200
    dissolvenza: float = 0.32        # 0 = maglia intatta, 1 = molto frammentata
    direzione_dissolvenza: tuple = (1.0, 0.18)   # verso destra (schermo, y in alto)
    glow: tuple = (0.55, 0.45, 0.34)
    coronarie: float = 1.05  # pesi alone a tre scale
    seme: int = 7


# ---------------------------------------------------------------------------
def _rot(ax, deg):
    a = np.radians(deg)
    c, s = np.cos(a), np.sin(a)
    return {"x": np.array([[1, 0, 0], [0, c, -s], [0, s, c]]),
            "y": np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]),
            "z": np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[ax]


def carica_mesh(n_facce: int):
    f = QUI / "sorgenti" / f"cuore_{n_facce}.npz"
    if not f.exists():
        from cuore_mesh import genera_mesh
        V, F = genera_mesh(n_facce)
        np.savez_compressed(f, V=V, F=F)
    d = np.load(f)
    return d["V"], d["F"]


def spigoli(F):
    E = np.sort(np.concatenate([F[:, [0, 1]], F[:, [1, 2]], F[:, [2, 0]]]), axis=1)
    E, inv = np.unique(E, axis=0, return_inverse=True)
    # facce adiacenti a ogni spigolo (per sapere se è sul contorno/frontale)
    nf = len(F)
    facce_di = [[] for _ in range(len(E))]
    for k, e in enumerate(inv.ravel()):
        facce_di[e].append(k % nf)
    return E, facce_di


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def proietta(V, s: Stile):
    """Ruota e proietta in prospettiva. Ritorna coordinate schermo normalizzate
    (x a destra, y in alto, unità ~ altezza del cuore = 1), profondità z (verso
    l'osservatore positiva) e matrice di rotazione."""
    R = _rot("x", s.rot_x) @ _rot("y", s.rot_y)
    W = V @ R.T
    c = (W.min(0) + W.max(0)) / 2
    W = W - c
    h = np.ptp(W[:, 1])
    W = W / h
    cam = 3.2                                  # distanza della camera (in altezze)
    f = cam / (cam - W[:, 2])
    P = W[:, :2] * f[:, None]
    return P, W[:, 2], R


def _proietta_con(punti, R, V):
    """Proietta punti 3D con la stessa camera usata per la maglia V."""
    W = V @ R.T
    c = (W.min(0) + W.max(0)) / 2
    h = np.ptp(W[:, 1])
    Wp = (punti @ R.T - c) / h
    Wv = (W - c) / h
    cam = 3.2
    f = cam / (cam - Wp[:, 2])
    zc = Wp[:, 2] - np.median(Wv[:, 2])          # >0: metà anteriore
    return Wp[:, :2] * f[:, None], zc


def render_cuore(px_w: int, px_h: int, centro: tuple, altezza_px: float, s: Stile,
                 maschera_vuoto=None) -> np.ndarray:
    """Intensità lineare (float32, px_h x px_w) del cuore centrato in `centro`
    (pixel, origine in alto a sinistra) e alto `altezza_px`."""
    rng = np.random.default_rng(s.seme)
    V, F = carica_mesh(s.n_facce)
    P, z, R = proietta(V, s)

    # normali (nello spazio ruotato) per facce e vertici
    Vr = (V @ R.T)
    n_f = np.cross(Vr[F[:, 1]] - Vr[F[:, 0]], Vr[F[:, 2]] - Vr[F[:, 0]])
    n_f /= np.linalg.norm(n_f, axis=1, keepdims=True) + 1e-12
    n_v = np.zeros_like(Vr)
    for i in range(3):
        np.add.at(n_v, F[:, i], n_f)
    n_v /= np.linalg.norm(n_v, axis=1, keepdims=True) + 1e-12
    # verso della normale: marching cubes può dare normali entranti -> orienta verso l'esterno
    centro3 = Vr.mean(0)
    if np.mean(np.sum((Vr - centro3) * n_v, axis=1)) < 0:
        n_f, n_v = -n_f, -n_v
    frontale_f = n_f[:, 2] > 0.0

    # ---- dissoluzione: campo scalare sullo schermo + rumore ----
    d = np.array(s.direzione_dissolvenza, float)
    d /= np.linalg.norm(d)
    proj = P @ d
    proj = (proj - proj.min()) / np.ptp(proj)
    rumore = rng.normal(0, 0.06, len(P))
    sdiss = smoothstep(1.0 - s.dissolvenza, 1.02, proj + rumore) if s.dissolvenza > 0 else np.zeros(len(P))
    # spostamento dei vertici dissolti: verso l'esterno e lungo la direzione
    sposta = (n_v[:, :2] * 0.5 + d * 0.8) * (sdiss ** 2.0)[:, None] * rng.uniform(0.01, 0.07, (len(P), 1))
    P = P + sposta

    # ---- da coordinate normalizzate a pixel (super-campionamento 2x) ----
    SS = 2
    W2, H2 = px_w * SS, px_h * SS
    scala = altezza_px * SS
    cx, cy = centro[0] * SS, centro[1] * SS
    Q = np.empty_like(P)
    Q[:, 0] = cx + P[:, 0] * scala
    Q[:, 1] = cy - P[:, 1] * scala
    zn = (z - z.min()) / np.ptp(z)                       # 0 dietro, 1 davanti

    I = np.zeros((H2, W2), np.float32)

    # ---- facce frontali: volume con luce dall'alto-sinistra ----
    luce = np.array([-0.45, 0.6, 0.66])
    luce /= np.linalg.norm(luce)
    lamb = np.clip(n_f @ luce, 0, 1)
    strato = np.zeros_like(I)
    ordine = np.argsort(z[F].mean(1))                     # dal fondo al davanti
    for k in ordine:
        if not frontale_f[k]:
            continue
        sd = sdiss[F[k]].mean()
        val = s.facce * (0.25 + 0.75 * lamb[k]) * (0.55 + 0.45 * zn[F[k]].mean()) * (1 - sd)
        if val <= 0.002:
            continue
        cv2.fillConvexPoly(strato, np.round(Q[F[k]] * 4).astype(np.int32), float(val), cv2.LINE_8, 2)
    I += strato

    # ---- spigoli ----
    E, facce_di = spigoli(F)
    fronte_e = np.array([any(frontale_f[f] for f in fs) for fs in facce_di])
    sil = np.array([len(fs) == 2 and frontale_f[fs[0]] != frontale_f[fs[1]] for fs in facce_di])
    sd_e = sdiss[E].mean(1)
    tenuto = rng.random(len(E)) > (sd_e ** 1.3) * 0.95   # gli spigoli dissolti spariscono
    zi = zn[E].mean(1)
    # luce "olografica": bordo (fresnel) più acceso del centro, più un po' di lambert
    nz = np.abs(n_v[E, 2]).mean(1)
    rim = (1 - nz) ** 1.4
    lam_e = np.clip(n_v[E] @ luce, 0, 1).mean(1)
    val_e = np.where(fronte_e, s.spigoli_fronte * (0.30 + 0.35 * lam_e + 0.75 * rim) * (0.6 + 0.4 * zi),
                     s.spigoli_retro * (0.6 + 0.4 * zi))
    val_e = np.where(sil, s.spigoli_fronte * 1.15, val_e)   # contorno più deciso
    val_e = val_e * (1 - 0.65 * sd_e) * rng.uniform(0.8, 1.15, len(E))
    sp = max(1, int(round(scala * 0.00105)))            # spessore linea (px a 2x)
    strato = np.zeros_like(I)
    for k in np.argsort(val_e):
        if not tenuto[k]:
            continue
        a, b = Q[E[k, 0]], Q[E[k, 1]]
        cv2.line(strato, (int(a[0] * 4), int(a[1] * 4)), (int(b[0] * 4), int(b[1] * 4)),
                 float(val_e[k]), sp, cv2.LINE_8, 2)
    I += strato

    # ---- coronarie (segno anatomico): tratti più luminosi sulla superficie ----
    if s.coronarie:
        from cuore_mesh import coronarie
        cor = coronarie()
        for nome, c3 in cor.items():
            Pc, zc = _proietta_con(c3, R, V)
            Qc = np.stack([cx + Pc[:, 0] * scala, cy - Pc[:, 1] * scala], 1)
            spess = sp * (2 if nome in ("IVA", "CX", "CDx") else 1)
            for i in range(len(Qc) - 1):
                if zc[i] < 0:                      # tratti sul retro: non visibili
                    continue
                k = s.coronarie * (1.0 - 0.45 * i / len(Qc))
                cv2.line(I, (int(Qc[i, 0] * 4), int(Qc[i, 1] * 4)), (int(Qc[i + 1, 0] * 4), int(Qc[i + 1, 1] * 4)),
                         float(k), spess, cv2.LINE_8, 2)

    # ---- nodi ----
    fronte_v = n_v[:, 2] > -0.05
    for i in range(len(Q)):
        if not fronte_v[i] and rng.random() > 0.25:
            continue
        x, y = Q[i]
        if not (0 <= x < W2 and 0 <= y < H2):
            continue
        v = s.nodi * (0.5 + 0.5 * zn[i]) * (1 - 0.5 * sdiss[i]) * (1.0 if fronte_v[i] else 0.3)
        r = sp * (1.1 + 0.9 * zn[i])
        cv2.circle(I, (int(x * 4), int(y * 4)), int(r * 4), float(v), -1, cv2.LINE_8, 2)
    # nodi "accesi": splat gaussiani additivi
    luce_i = np.where(fronte_v & (rng.random(len(Q)) < s.frazione_nodi_luce))[0]
    splat = np.zeros_like(I)
    for i in luce_i:
        x, y = Q[i]
        if 0 <= x < W2 and 0 <= y < H2:
            splat[int(y), int(x)] += 2.5 + 3.5 * rng.random()
    I += cv2.GaussianBlur(splat, (0, 0), sp * 2.2) * (sp * 2.2) ** 2 * 0.9

    # ---- particelle: si staccano dalla superficie e si disperdono ----
    if s.particelle:
        idx = rng.integers(0, len(Vr), s.particelle)
        # più particelle dove la maglia si dissolve
        peso = 0.25 + 1.75 * sdiss[idx]
        tieni = rng.random(len(idx)) < peso / peso.max()
        idx = idx[tieni]
        dist = rng.exponential(0.035, len(idx)) + sdiss[idx] * rng.exponential(0.12, len(idx))
        dirp = n_v[idx, :2] + d * (0.4 + sdiss[idx])[:, None] + rng.normal(0, 0.35, (len(idx), 2))
        dirp /= np.linalg.norm(dirp, axis=1, keepdims=True) + 1e-9
        pp = P[idx] + dirp * dist[:, None]
        X = cx + pp[:, 0] * scala
        Y = cy - pp[:, 1] * scala
        lum = np.clip(1.15 - dist * 5.0, 0.12, 1.0) * rng.uniform(0.35, 1.1, len(idx))
        dim = rng.choice([1, 1, 1, 2, 2, 3], len(idx)) * sp * 0.75
        for x, y, l, r in zip(X, Y, lum, dim):
            if 0 <= x < W2 and 0 <= y < H2:
                cv2.circle(I, (int(x * 4), int(y * 4)), max(2, int(r * 4)), float(l), -1, cv2.LINE_8, 2)
        # qualche frammento triangolare staccato
        n_fr = int(22 * s.dissolvenza)
        cand = np.where(sdiss[F].mean(1) > 0.35)[0]
        for k in rng.choice(cand, min(n_fr, len(cand)), replace=False) if len(cand) else []:
            t = Q[F[k]].mean(0)
            off = (np.array([d[0], -d[1]]) * rng.uniform(0.03, 0.12) + rng.normal(0, 0.03, 2)) * scala
            tri = (Q[F[k]] - t) * rng.uniform(0.25, 0.55) + t + off
            cv2.polylines(I, [np.round(tri * 4).astype(np.int32)], True, float(rng.uniform(0.3, 0.8)), sp, cv2.LINE_8, 2)

    # ---- ritorno a risoluzione finale (antialias) ----
    I = cv2.resize(I, (px_w, px_h), interpolation=cv2.INTER_AREA)
    if maschera_vuoto is not None:
        I *= maschera_vuoto
    return I


def bagliore(I: np.ndarray, px_per_in: float, pesi=(0.55, 0.42, 0.30)) -> np.ndarray:
    """Alone a tre scale (circa 0,02 / 0,08 / 0,3 in). Le scale ampie si
    calcolano su un'immagine ridotta per velocità."""
    out = I.copy()
    for peso, sig_in in zip(pesi, (0.02, 0.08, 0.30)):
        sig = sig_in * px_per_in
        f = max(1, int(sig / 6))
        small = cv2.resize(I, (I.shape[1] // f, I.shape[0] // f), interpolation=cv2.INTER_AREA)
        g = cv2.GaussianBlur(small, (0, 0), sig / f)
        out += peso * cv2.resize(g, (I.shape[1], I.shape[0]), interpolation=cv2.INTER_LINEAR)
    return out


def colora(I: np.ndarray, seme=11) -> np.ndarray:
    """Intensità -> RGB float (0..1) su fondo #050505, con dithering contro il banding."""
    rgb = 1.0 - np.exp(-I[..., None] * K_COLORE)
    rgb = FONDO + (1 - FONDO) * rgb
    rng = np.random.default_rng(seme)
    # dithering triangolare di ±1 livello (1/255): rompe le fasce nei gradienti scuri
    rgb += (rng.random(I.shape, np.float32) - rng.random(I.shape, np.float32))[..., None] / 255.0
    return np.clip(rgb, 0, 1)


def ecg_punti(x0, x1, y, complessi, amp, passo=0.004):
    """Polilinea ECG (coordinate in pollici, y verso il basso): linea isoelettrica
    con complessi P-QRS-T centrati nelle ascisse `complessi` (ognuno con il
    proprio fattore di ampiezza). Forme d'onda con curve morbide per P e T."""
    xs = np.arange(x0, x1 + passo, passo)
    ys = np.zeros_like(xs)
    for xc, k in complessi:
        a = amp * k
        u = (xs - xc)
        ys += -0.12 * a * np.exp(-((u + 0.30) / 0.045) ** 2)          # onda P
        ys += 0.10 * a * np.exp(-((u + 0.035) / 0.012) ** 2)           # Q
        ys += -1.00 * a * np.exp(-((u - 0.0) / 0.016) ** 2)            # R
        ys += 0.28 * a * np.exp(-((u - 0.035) / 0.013) ** 2)           # S
        ys += -0.22 * a * np.exp(-((u - 0.30) / 0.07) ** 2)            # onda T
    return np.stack([xs, y + ys], axis=1)
