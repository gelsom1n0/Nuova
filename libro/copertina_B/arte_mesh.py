#!/usr/bin/env python3
"""
Rendering procedurale di oggetti "digitali" low-poly (opera originale):
qui la pillola del Volume B, con lo stesso motore del cuore del Volume A.

Pipeline:
  maglia 3D (pillola_mesh.py) -> rotazione + proiezione prospettica ->
  facce frontali con ombreggiatura tenue (volume) + spigoli (frontali brillanti,
  posteriori in trasparenza "olografica") + nodi luminosi + particelle che si
  staccano dalla superficie e si dissolvono -> bagliore gaussiano a più scale ->
  mappatura tonale azzurro -> bianco freddo -> fondo nero con dithering.
In più: granuli di principio attivo dentro il guscio, molecole esagonali tra
le particelle, reticolo esagonale in cui la compressa si "trasforma".

Tutto è calcolato in un canale di intensità I (lineare, additivo), poi colorato:
  rgb = 1 - exp(-I * K)   con K = (0.55, 2.6, 4.2)
che dà blu petrolio (#1A6991) alle basse intensità, azzurro tecnologico
(#3DBAE0) ai valori medi e un bianco-ciano ai picchi.

Il disegno avviene in super-campionamento 2x (antialias per media d'area).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import cv2
import numpy as np

QUI = Path(__file__).resolve().parent
K_COLORE = np.array([0.55, 2.6, 4.2], np.float32)    # R, G, B
FONDO = 5 / 255.0                                     # #050505


@dataclass
class Stile:
    nome: str = "A"
    forma: str = "capsula"
    n_facce: int = 1800
    rotazioni: tuple = (("y", -28.0), ("z", 35.0), ("x", 10.0))
    spigoli_fronte: float = 0.62     # intensità spigoli frontali
    spigoli_retro: float = 0.11      # spigoli posteriori (effetto trasparenza)
    facce: float = 0.055              # riempimento delle facce frontali
    nodi: float = 1.0
    frazione_nodi_luce: float = 0.10  # nodi con alone
    particelle: int = 2200
    dissolvenza: float = 0.32        # 0 = maglia intatta, 1 = molto frammentata
    direzione_dissolvenza: tuple = (1.0, 0.18)   # verso destra (schermo, y in alto)
    glow: tuple = (0.55, 0.45, 0.34)
    seme: int = 7
    granuli: int = 0                  # punti interni (principio attivo)
    getto: float = 0.0                # granuli che escono dalla zona centrale (capsula aperta)
    molecole: int = 0                 # piccole molecole esagonali tra le particelle
    reticolo: float = 0.0             # reticolo esagonale nella zona dissolta (compressa)


# ---------------------------------------------------------------------------
def _rot(ax, deg):
    a = np.radians(deg)
    c, s = np.cos(a), np.sin(a)
    return {"x": np.array([[1, 0, 0], [0, c, -s], [0, s, c]]),
            "y": np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]),
            "z": np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])}[ax]


def carica_mesh(forma: str, n_facce: int):
    f = QUI / "sorgenti" / f"{forma}_{n_facce}.npz"
    if not f.exists():
        from pillola_mesh import genera_mesh
        V, F = genera_mesh(forma, n_facce)
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
    R = np.eye(3)
    for ax, deg in s.rotazioni:
        R = _rot(ax, deg) @ R
    W = V @ R.T
    c = (W.min(0) + W.max(0)) / 2
    W = W - c
    h = max(np.ptp(W[:, 0]), np.ptp(W[:, 1]))        # ingombro massimo = 1
    W = W / h
    cam = 3.2                                  # distanza della camera (in altezze)
    f = cam / (cam - W[:, 2])
    P = W[:, :2] * f[:, None]
    return P, W[:, 2], R


def _proietta_con(punti, R, V):
    """Proietta punti 3D con la stessa camera usata per la maglia V."""
    W = V @ R.T
    c = (W.min(0) + W.max(0)) / 2
    h = max(np.ptp(W[:, 0]), np.ptp(W[:, 1]))
    Wp = (punti @ R.T - c) / h
    Wv = (W - c) / h
    cam = 3.2
    f = cam / (cam - Wp[:, 2])
    zc = Wp[:, 2] - np.median(Wv[:, 2])          # >0: metà anteriore
    return Wp[:, :2] * f[:, None], zc


def render_oggetto(px_w: int, px_h: int, centro: tuple, altezza_px: float, s: Stile,
                   maschera_vuoto=None) -> np.ndarray:
    """Intensità lineare (float32, px_h x px_w) dell'oggetto centrato in `centro`
    (pixel, origine in alto a sinistra); `altezza_px` = ingombro massimo."""
    rng = np.random.default_rng(s.seme)
    V, F = carica_mesh(s.forma, s.n_facce)
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
    p_min, p_ptp = proj.min(), np.ptp(proj)
    proj = (proj - p_min) / p_ptp
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

    def sdiss_in(pt):                                   # dissoluzione in un punto schermo qualsiasi
        if s.dissolvenza <= 0:
            return np.zeros(len(pt))
        pr = (pt @ d - p_min) / p_ptp
        return smoothstep(1.0 - s.dissolvenza, 1.02, pr)

    # ---- granuli di principio attivo visibili attraverso il guscio ----
    if s.granuli:
        from pillola_mesh import dentro
        G = dentro(s.forma, s.granuli, seme=s.seme)
        Pg, zg = _proietta_con(G, R, V)
        sg = sdiss_in(Pg)
        # escono dove il guscio si dissolve, o dalla zona aperta (getto)
        spinta = sg ** 1.2 * rng.exponential(0.16, len(G))
        if s.getto:
            spinta += s.getto * np.exp(-(G[:, 0] / 0.45) ** 2) * rng.exponential(0.16, len(G))
        dirg = d[None, :] + rng.normal(0, 0.45, (len(G), 2))
        dirg /= np.linalg.norm(dirg, axis=1, keepdims=True)
        Pg = Pg + dirg * spinta[:, None]
        Xg, Yg = cx + Pg[:, 0] * scala, cy - Pg[:, 1] * scala
        lg = (0.40 + 0.35 * (zg > 0)) * rng.uniform(0.6, 1.25, len(G)) * np.clip(1.25 - spinta * 2.5, 0.3, 1)
        rg = rng.choice([1.0, 1.4, 1.8, 2.4], len(G)) * sp * 1.1
        for x, y, l, r in zip(Xg, Yg, lg, rg):
            if 0 <= x < W2 and 0 <= y < H2:
                cv2.circle(I, (int(x * 4), int(y * 4)), max(2, int(r * 4)), float(l), -1, cv2.LINE_8, 2)

    # ---- reticolo esagonale nella zona dissolta (la compressa diventa struttura) ----
    if s.reticolo:
        passo = 0.042 * scala
        sil = np.zeros((H2 // 4, W2 // 4), np.uint8)       # silhouette a 1/4 per la distanza
        for f in F:
            cv2.fillConvexPoly(sil, np.round(Q[f] / 4).astype(np.int32), 1)
        dist_out = cv2.distanceTransform(1 - sil, cv2.DIST_L2, 3) * 4 / scala
        xs0, xs1 = Q[:, 0].min() - 0.1 * scala, Q[:, 0].max() + 0.45 * scala
        ys0, ys1 = Q[:, 1].min() - 0.35 * scala, Q[:, 1].max() + 0.1 * scala
        nodi_h = {}
        for j, yy in enumerate(np.arange(ys0, ys1, passo * 0.866)):
            for i, xx in enumerate(np.arange(xs0, xs1, passo)):
                x = xx + (passo / 2 if j % 2 else 0)
                if not (0 <= x < W2 and 0 <= yy < H2):
                    continue
                pn = np.array([[(x - cx) / scala, (cy - yy) / scala]])
                sd = sdiss_in(pn)[0]
                do = dist_out[int(yy) // 4, int(x) // 4]
                w = s.reticolo * sd * np.exp(-do / 0.13) * rng.uniform(0.6, 1.2)
                if w > 0.08 and rng.random() < 0.15 + w:
                    nodi_h[(i, j)] = (x, yy, w)
        for (i, j), (x, y, w) in nodi_h.items():
            vic = [(i + 1, j), (i + (j % 2), j + 1), (i - 1 + (j % 2), j + 1)]   # vicini in griglia sfalsata
            for v in vic:
                if v in nodi_h and rng.random() < 0.8:
                    x2, y2, w2 = nodi_h[v]
                    cv2.line(I, (int(x * 4), int(y * 4)), (int(x2 * 4), int(y2 * 4)),
                             float(0.5 * min(w, w2)), sp, cv2.LINE_8, 2)
            cv2.circle(I, (int(x * 4), int(y * 4)), int(sp * 1.4 * 4), float(0.9 * w), -1, cv2.LINE_8, 2)

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

    # ---- piccole molecole esagonali che si allontanano ----
    if s.molecole:
        cand = np.where(sdiss > 0.3)[0] if s.dissolvenza > 0 else np.arange(len(P))
        if s.getto:
            cand = np.arange(len(P))
        for _ in range(s.molecole):
            if s.getto:                                   # dalla fessura tra le due metà
                base = np.array([0.0, 0.0]) + rng.normal(0, 0.05, 2)
                dist = rng.exponential(0.16) + 0.06
            else:
                base = P[rng.choice(cand)]
                dist = rng.exponential(0.09) + 0.02
            dirm = d + rng.normal(0, 0.5, 2)
            dirm /= np.linalg.norm(dirm)
            c0 = base + dirm * dist
            X0, Y0 = cx + c0[0] * scala, cy - c0[1] * scala
            r = rng.uniform(0.010, 0.022) * scala
            ang = rng.uniform(0, np.pi / 3)
            lum = float(np.clip(0.95 - dist * 2.2, 0.2, 0.9) * rng.uniform(0.6, 1.1))
            vert = np.array([[X0 + r * np.cos(ang + k * np.pi / 3), Y0 + r * np.sin(ang + k * np.pi / 3)] for k in range(6)])
            cv2.polylines(I, [np.round(vert * 4).astype(np.int32)], True, lum, sp, cv2.LINE_8, 2)
            for vx, vy in vert:
                cv2.circle(I, (int(vx * 4), int(vy * 4)), int(sp * 1.2 * 4), lum * 1.1, -1, cv2.LINE_8, 2)
            if rng.random() < 0.6:                       # catena laterale
                k = rng.integers(0, 6)
                a1 = vert[k]
                dv = (vert[k] - np.array([X0, Y0])) / r
                a2 = a1 + dv * r * 0.9
                a3 = a2 + np.array([np.cos(ang + k * np.pi / 3 + 0.5), np.sin(ang + k * np.pi / 3 + 0.5)]) * r * 0.9
                cv2.polylines(I, [np.round(np.array([a1, a2, a3]) * 4).astype(np.int32)], False, lum * 0.9, sp, cv2.LINE_8, 2)
                cv2.circle(I, (int(a3[0] * 4), int(a3[1] * 4)), int(sp * 1.4 * 4), lum, -1, cv2.LINE_8, 2)

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


# ---------------------------------------------------------------------------
# Tracciati "farmacologici" (al posto dell'ECG del Volume A)
# Coordinate in pollici, y verso il basso. Ritornano polilinee (array Nx2).
# ---------------------------------------------------------------------------
def curva_pk(x0, x1, y, dosi, intervallo, amp, ka=7.0, ke=0.9, passo=0.004):
    """Concentrazione plasmatica con dosi ripetute per via orale (modello a un
    compartimento, Bateman): picchi e valli che salgono fino allo stato
    stazionario. `dosi` = ascissa della prima dose; una dose ogni `intervallo`
    pollici. Normalizzata in modo che il picco allo stato stazionario = amp."""
    xs = np.arange(x0, x1 + passo, passo)
    c = np.zeros_like(xs)
    t0 = dosi
    while t0 < x1:
        t = np.clip(xs - t0, 0, None)
        c += np.where(xs > t0, np.exp(-ke * t) - np.exp(-ka * t), 0)
        t0 += intervallo
    # picco teorico allo stato stazionario
    tt = np.linspace(0, intervallo, 400)
    acc = 1 / (1 - np.exp(-ke * intervallo)), 1 / (1 - np.exp(-ka * intervallo))
    css = (np.exp(-ke * tt) * acc[0] - np.exp(-ka * tt) * acc[1]).max()
    return np.stack([xs, y - amp * c / css], axis=1), css


def catena_molecolare(x0, x1, y, passo_legame=0.16, ogni=7, seme=4):
    """Scheletro molecolare: zig-zag di legami a 120° con anelli esagonali
    inseriti ogni `ogni` legami. Ritorna (polilinea della catena, lista di
    esagoni [6x2], nodi [Nx2])."""
    rng = np.random.default_rng(seme)
    h = passo_legame * np.sin(np.radians(30))
    dx = passo_legame * np.cos(np.radians(30))
    pts, anelli = [], []
    x, k, su = x0, 0, True
    while x < x1:
        pts.append((x, y + (-h / 2 if su else h / 2)))
        if k % ogni == ogni - 1 and x + 3 * dx < x1:
            # anello appeso al vertice corrente, dalla parte opposta alla catena
            cxr, cyr = x, y + (-h / 2 - passo_legame) if su else y + (h / 2 + passo_legame)
            r = passo_legame
            anelli.append(np.array([[cxr + r * np.cos(np.radians(90 + 60 * i)),
                                     cyr + r * np.sin(np.radians(90 + 60 * i))] for i in range(6)]))
        x += dx
        su = not su
        k += 1
    pts = np.array(pts)
    nodi = np.concatenate([pts] + anelli) if anelli else pts
    return pts, anelli, nodi


def curva_dose_risposta(x0, x1, y_basso, y_alto, x50, pendenza=2.2, passo=0.004, n_punti=9):
    """Curva sigmoide dose-risposta (equazione di Hill su asse logaritmico),
    più punti sperimentali sparsi lungo la curva."""
    xs = np.arange(x0, x1 + passo, passo)
    e = 1 / (1 + np.exp(-pendenza * (xs - x50)))
    curva = np.stack([xs, y_basso + (y_alto - y_basso) * e], axis=1)
    px = np.linspace(x50 - 2.2, x50 + 2.2, n_punti)
    pe = 1 / (1 + np.exp(-pendenza * (px - x50)))
    rng = np.random.default_rng(9)
    punti = np.stack([px, y_basso + (y_alto - y_basso) * pe + rng.normal(0, 0.03, n_punti)], axis=1)
    return curva, punti
