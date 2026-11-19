#!/usr/bin/env python3
"""
Geometria del cuore anatomico (originale, procedurale).

Il cuore è un campo di distanza implicito: unione morbida (smooth-min) di
ellissoidi (ventricoli, atri, auricola) e tubi lungo curve (aorta con arco e
tronchi sovra-aortici, tronco polmonare con biforcazione, vene cave, vene
polmonari). La superficie si estrae con marching cubes e si decima a una
maglia low-poly irregolare (decimazione quadrica).

Coordinate: vista anteriore. x verso destra dell'osservatore (= sinistra del
paziente), y in alto, z verso l'osservatore. Unità ~ centimetri.

Uso come modulo: genera_mesh(n_facce) -> (V, F).
Uso da riga di comando: salva sorgenti/cuore_<n>.npz per ispezione.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

QUI = Path(__file__).resolve().parent


# ---------------------------------------------------------------------------
# Primitive di distanza (vettorizzate su array (..., 3))
# ---------------------------------------------------------------------------
def rot(ax: str, deg: float) -> np.ndarray:
    a = np.radians(deg)
    c, s = np.cos(a), np.sin(a)
    if ax == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if ax == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def ellissoide(p, c, r, R=np.eye(3)):
    """Distanza approssimata da un ellissoide di centro c, semiassi r, orientato da R."""
    q = (p - np.asarray(c)) @ R  # coordinate locali
    r = np.asarray(r, float)
    k0 = np.linalg.norm(q / r, axis=-1)
    k1 = np.linalg.norm(q / (r * r), axis=-1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9)


def ventricoli(p, c, r, R, rastremazione):
    """Massa ventricolare: ellissoide rastremato verso l'apice (asse y locale
    negativo), così la punta è più stretta della base."""
    q = (p - np.asarray(c)) @ R
    t = np.clip(-q[..., 1] / r[1], -1, 1)          # 1 all'apice, -1 alla base
    scala = 1.0 - rastremazione * np.clip(t, 0, 1) ** 1.6
    q2 = q.copy()
    q2[..., 0] = q[..., 0] / scala
    q2[..., 2] = q[..., 2] / scala
    r = np.asarray(r, float)
    k0 = np.linalg.norm(q2 / r, axis=-1)
    k1 = np.linalg.norm(q2 / (r * r), axis=-1)
    return k0 * (k0 - 1.0) / np.maximum(k1, 1e-9) * scala


def _decasteljau(P, n):
    t = np.linspace(0, 1, n)
    out = []
    for tt in t:
        Q = P.copy()
        while len(Q) > 1:
            Q = Q[:-1] * (1 - tt) + Q[1:] * tt
        out.append(Q[0])
    return np.array(out)


def tubo(p, curva, r0, r1=None):
    """Distanza da un tubo lungo una polilinea, con raggio che varia da r0 a r1."""
    r1 = r0 if r1 is None else r1
    best = np.full(p.shape[:-1], np.inf)
    n = len(curva) - 1
    for i in range(n):
        a, b = curva[i], curva[i + 1]
        ab = b - a
        L2 = float(ab @ ab)
        t = np.clip(((p - a) @ ab) / L2, 0, 1)
        d = np.linalg.norm(p - (a + t[..., None] * ab), axis=-1)
        rr = r0 + (r1 - r0) * (i + t) / n
        best = np.minimum(best, d - rr)
    return best


def smin(a, b, k):
    h = np.clip(0.5 + 0.5 * (b - a) / k, 0, 1)
    return b * (1 - h) + a * h - k * h * (1 - h)


# ---------------------------------------------------------------------------
# Anatomia
# ---------------------------------------------------------------------------
def campo(p: np.ndarray) -> np.ndarray:
    # ventricoli: asse lungo inclinato, apice in basso a destra (sinistra del paziente)
    Rv = rot("z", 36) @ rot("x", -12)
    d = ventricoli(p, (0.45, -0.75, 0.05), (1.8, 2.55, 1.5), Rv, 0.72)
    # rilievo del ventricolo destro (anteriore, verso sinistra dell'osservatore)
    d = smin(d, ellissoide(p, (-0.45, -0.35, 0.55), (1.25, 1.55, 0.95), rot("z", 25)), 0.45)
    # atrio destro (a sinistra dell'osservatore) e auricola destra
    d = smin(d, ellissoide(p, (-1.55, 0.75, 0.05), (0.95, 1.1, 0.95), rot("z", -10)), 0.4)
    d = smin(d, ellissoide(p, (-1.05, 1.55, 0.55), (0.55, 0.38, 0.4), rot("z", 25)), 0.25)
    # atrio sinistro (posteriore) e auricola sinistra (lobo che sporge a destra)
    d = smin(d, ellissoide(p, (0.75, 1.0, -0.85), (1.15, 0.75, 0.85)), 0.4)
    d = smin(d, ellissoide(p, (1.75, 1.0, 0.25), (0.55, 0.32, 0.42), rot("z", -25)), 0.25)

    # aorta ascendente, arco e discendente
    aorta = _decasteljau(np.array([
        (0.05, 0.55, 0.25), (0.0, 2.4, 0.45), (0.15, 3.55, 0.1),
        (1.05, 3.85, -0.6), (1.55, 3.1, -1.05), (1.5, 1.6, -1.25)]), 48)
    d = smin(d, tubo(p, aorta, 0.62, 0.5), 0.3)
    # tronchi sovra-aortici
    for a, b in [((0.25, 3.45, 0.05), (0.05, 4.45, 0.15)),
                 ((0.75, 3.7, -0.3), (0.85, 4.55, -0.3)),
                 ((1.2, 3.55, -0.65), (1.5, 4.35, -0.75))]:
        d = smin(d, tubo(p, _decasteljau(np.array([a, (np.add(a, b) / 2) + (0.05, 0.1, 0), b]), 10), 0.24, 0.2), 0.12)

    # tronco polmonare (anteriore, a destra dell'aorta) e biforcazione
    pol = _decasteljau(np.array([(0.55, 0.55, 0.95), (0.85, 1.6, 1.05), (1.0, 2.45, 0.55)]), 20)
    d = smin(d, tubo(p, pol, 0.55, 0.5), 0.3)
    sx = _decasteljau(np.array([(1.0, 2.45, 0.55), (1.55, 2.75, 0.15), (2.1, 2.5, -0.35)]), 16)
    d = smin(d, tubo(p, sx, 0.4, 0.3), 0.15)
    dx = _decasteljau(np.array([(0.95, 2.4, 0.45), (0.3, 2.3, -0.6), (-0.9, 2.2, -0.8)]), 16)
    d = smin(d, tubo(p, dx, 0.38, 0.3), 0.15)

    # vena cava superiore (a sinistra) e inferiore (stub in basso)
    vcs = _decasteljau(np.array([(-1.45, 1.0, -0.1), (-1.4, 2.3, -0.1), (-1.3, 3.45, -0.15)]), 18)
    d = smin(d, tubo(p, vcs, 0.5, 0.46), 0.35)
    vci = _decasteljau(np.array([(-1.45, -0.2, -0.45), (-1.5, -1.0, -0.6), (-1.5, -1.6, -0.65)]), 10)
    d = smin(d, tubo(p, vci, 0.45, 0.42), 0.25)

    # vene polmonari sull'atrio sinistro
    for a, b in [((1.4, 1.3, -1.1), (2.05, 1.5, -1.4)), ((1.4, 0.75, -1.15), (2.0, 0.6, -1.5)),
                 ((0.1, 1.3, -1.15), (-0.5, 1.5, -1.5))]:
        d = smin(d, tubo(p, np.array([a, b]), 0.24, 0.2), 0.15)
    return d


# ---------------------------------------------------------------------------
# Estrazione e decimazione
# ---------------------------------------------------------------------------
def genera_mesh(n_facce: int = 2200, passo: float = 0.06, seme: int = 3):
    from skimage.measure import marching_cubes
    import fast_simplification

    lo, hi = np.array([-3.4, -3.9, -2.6]), np.array([3.6, 5.3, 2.4])
    xs = [np.arange(lo[i], hi[i] + passo, passo) for i in range(3)]
    X, Y, Z = np.meshgrid(*xs, indexing="ij")
    P = np.stack([X, Y, Z], axis=-1)
    vol = np.empty(P.shape[:3], np.float32)
    for i in range(P.shape[0]):           # a fette per contenere la memoria
        vol[i] = campo(P[i])
    V, F, _, _ = marching_cubes(vol, 0.0, spacing=(passo,) * 3)
    V = V + lo
    # piccola irregolarità prima della decimazione: maglia meno "da griglia"
    rng = np.random.default_rng(seme)
    V = V + rng.normal(0, passo * 0.15, V.shape)
    ratio = 1.0 - n_facce / len(F)
    Vd, Fd = fast_simplification.simplify(V.astype(np.float32), F.astype(np.int32), target_reduction=ratio)
    return Vd.astype(np.float64), Fd.astype(np.int64)


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 2200
    V, F = genera_mesh(n)
    out = QUI / "sorgenti" / f"cuore_{n}.npz"
    np.savez_compressed(out, V=V, F=F)
    print(out, V.shape, F.shape, V.min(0).round(2), V.max(0).round(2))
