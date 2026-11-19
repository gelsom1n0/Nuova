#!/usr/bin/env python3
"""
Geometrie 3D (originali, procedurali) per la copertina del Volume B.

- capsula: capsula rigida in due pezzi (corpo + cappuccio leggermente più
  largo, con il gradino della giunzione), asse lungo x;
- capsula_aperta: le due metà separate, come gusci aperti (spessore visibile);
- compressa: compressa rotonda biconvessa con linea di frattura.

Ogni forma è un campo di distanza; la superficie si estrae con marching cubes e
si decima a maglia low-poly (decimazione quadrica), come per il cuore del
Volume A. Le funzioni `dentro_*` campionano punti interni (granuli di principio
attivo visibili attraverso la maglia).
"""
from __future__ import annotations

import numpy as np

R_CORPO, R_CAPP = 0.62, 0.66        # raggi corpo e cappuccio
L_CORPO, L_CAPP = 1.25, 1.05        # semilunghezze cilindriche (dal centro)


def _capsula_sdf(p, a, b, r):
    """Distanza da un segmento a-b con raggio r (capsula)."""
    ab = b - a
    t = np.clip(((p - a) @ ab) / (ab @ ab), 0, 1)
    return np.linalg.norm(p - (a + t[..., None] * ab), axis=-1) - r


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


def campo_capsula(p):
    # corpo: da x=-L_CORPO-? fino a x=+0.35 (sovrapposto al cappuccio)
    corpo = _capsula_sdf(p, np.array([-L_CORPO, 0, 0.0]), np.array([0.35, 0, 0.0]), R_CORPO)
    capp = _capsula_sdf(p, np.array([-0.15, 0, 0.0]), np.array([L_CAPP, 0, 0.0]), R_CAPP)
    # il cappuccio copre il corpo: unione netta (il gradino resta visibile)
    return np.minimum(corpo, capp)


def campo_capsula_aperta(p, apertura=1.15, spessore=0.05):
    """Due gusci aperti, separati lungo x di `apertura`."""
    q1 = p.copy()
    q1[..., 0] += apertura / 2
    corpo = np.abs(_capsula_sdf(q1, np.array([-L_CORPO, 0, 0.0]), np.array([0.0, 0, 0.0]), R_CORPO)) - spessore
    corpo = np.maximum(corpo, q1[..., 0] - 0.0)          # taglio: aperto verso +x
    q2 = p.copy()
    q2[..., 0] -= apertura / 2
    capp = np.abs(_capsula_sdf(q2, np.array([0.0, 0, 0.0]), np.array([L_CAPP, 0, 0.0]), R_CAPP)) - spessore
    capp = np.maximum(capp, -q2[..., 0])                 # aperto verso -x
    return np.minimum(corpo, capp)


def campo_compressa(p, r=1.0, h=0.20, R=2.6, raccordo=0.08):
    """Compressa biconvessa: intersezione di cilindro e due sfere, con
    linea di frattura sulla faccia superiore (asse y = spessore)."""
    x, y, z = p[..., 0], p[..., 1], p[..., 2]
    cil = np.sqrt(x * x + z * z) - r
    s1 = np.sqrt(x * x + (y + (R - h - 0.12)) ** 2 + z * z) - R
    s2 = np.sqrt(x * x + (y - (R - h - 0.12)) ** 2 + z * z) - R
    d = np.maximum(np.maximum(s1, s2), cil)
    # raccordo morbido del bordo
    d = d - raccordo * 0.3
    # linea di frattura: scanalatura a V lungo z sulla faccia superiore
    sol = np.maximum(np.abs(x) - (0.035 + 0.25 * np.clip(y - 0.1, 0, None)), -(y - 0.12))
    return np.maximum(d, -sol)


CAMPI = {
    "capsula": (campo_capsula, (-2.1, -1.0, -1.0), (2.0, 1.0, 1.0)),
    "capsula_aperta": (campo_capsula_aperta, (-2.65, -1.0, -1.0), (2.55, 1.0, 1.0)),
    "compressa": (campo_compressa, (-1.2, -0.6, -1.2), (1.2, 0.6, 1.2)),
}


def genera_mesh(forma: str, n_facce: int, passo: float = 0.03, seme: int = 3):
    from skimage.measure import marching_cubes
    import fast_simplification

    f, lo, hi = CAMPI[forma]
    lo, hi = np.array(lo), np.array(hi)
    xs = [np.arange(lo[i], hi[i] + passo, passo) for i in range(3)]
    X, Y, Z = np.meshgrid(*xs, indexing="ij")
    P = np.stack([X, Y, Z], axis=-1)
    vol = np.empty(P.shape[:3], np.float32)
    for i in range(P.shape[0]):
        vol[i] = f(P[i])
    V, F, _, _ = marching_cubes(vol, 0.0, spacing=(passo,) * 3)
    V = V + lo
    rng = np.random.default_rng(seme)
    V = V + rng.normal(0, passo * 0.15, V.shape)
    Vd, Fd = fast_simplification.simplify(V.astype(np.float32), F.astype(np.int32),
                                          target_reduction=1.0 - n_facce / len(F))
    return Vd.astype(np.float64), Fd.astype(np.int64)


def dentro(forma: str, n: int, seme: int = 5, margine: float = 0.08):
    """Punti casuali all'interno della forma (granuli)."""
    f, lo, hi = CAMPI[forma]
    if forma == "capsula_aperta":
        # granuli nella zona tra le due metà e dentro i gusci
        f = lambda p: np.minimum(_capsula_sdf(p, np.array([-1.9, 0, 0.0]), np.array([1.6, 0, 0.0]), 0.55), 9)
    rng = np.random.default_rng(seme)
    out = []
    while sum(len(o) for o in out) < n:
        p = rng.uniform(lo, hi, (n * 4, 3))
        out.append(p[f(p) < -margine])
    return np.concatenate(out)[:n]
