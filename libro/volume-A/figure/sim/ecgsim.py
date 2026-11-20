#!/usr/bin/env python3
"""
ecgsim – tracciati ECG didattici SIMULATI a 12 derivazioni, basati su un modello a dipolo.

MODELLO
-------
L'attività elettrica del cuore è rappresentata da un unico vettore cardiaco H(t) = (x, y, z) in mV:
  x = verso la sinistra del paziente, y = verso il basso (piedi), z = in avanti (anteriore).
Ogni onda è la somma di pochi «componenti»: un vettore 3D fisso moltiplicato per un profilo
temporale gaussiano (eventualmente asimmetrico). Ad esempio il QRS normale è la somma di:
  - attivazione settale   (precoce, verso destra e in avanti: q in I/aVL/V5-V6, r in V1);
  - parete libera del VS  (grande, a sinistra-in basso-indietro: R in I/II/V5-V6, S in V1-V2);
  - attivazione basale    (tardiva, in alto-dietro-a destra: piccola s in I e V6).
Ogni derivazione è la proiezione di H(t) sul proprio vettore di derivazione:
  - periferiche: triangolo di Einthoven / sistema esassiale (I = 0°, II = 60°, III = 120°);
    III, aVR, aVL, aVF sono calcolate dalle relazioni di Einthoven e Goldberger
    (III = II − I; aVR = −(I+II)/2; aVL = I − II/2; aVF = II − I/2), quindi sempre coerenti;
  - precordiali: vettori nel piano orizzontale (V1 115°, V2 95°, V3 75°, V4 55°, V5 30°,
    V6 0°, misurati da sinistra verso avanti) con un guadagno che riproduce la maggiore vicinanza
    al cuore di V2–V4.
Le patologie si ottengono modificando i componenti in modo fisiopatologicamente motivato
(es. BBD = forze terminali lente dirette a destra e in avanti; lesione = vettore di corrente di
lesione nel segmento ST diretto verso la zona lesa). I ritmi sono costruiti da un «motore» che
programma eventi atriali e ventricolari (con conduzione AV esplicita).

LIMITI DICHIARATI
-----------------
- È un modello didattico: morfologie lisce e «pulite», senza la variabilità di un ECG reale.
- Le ampiezze precordiali sono calibrate su valori di riferimento medi dell'adulto, non su un paziente.
- Fibrillazione ventricolare e torsione di punta sono modelli fenomenologici (non a dipolo
  fisiologico): vanno affiancati a tracciati reali (vedi figure/real) e validati con particolare cura.
- Non modellati (rimandati ai tracciati reali): pre-eccitazione/WPW, Brugada, Wellens, de Winter,
  pericardite, infarto del ventricolo destro (V4R), derivazioni posteriori V7–V9, ipotermia (onda J),
  effetto digitalico, artefatti reali.
Tutti i parametri sono espliciti e salvati nei metadati di ogni tracciato.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

FS = 1000  # Hz
LEADS = ["I", "II", "III", "aVR", "aVL", "aVF", "V1", "V2", "V3", "V4", "V5", "V6"]

# ------------------------------------------------------------------ vettori di derivazione
PRECORD = {  # angolo nel piano orizzontale (da sinistra verso avanti), guadagno, componente verticale
    "V1": (115, 1.05, 0.0), "V2": (95, 1.75, 0.0), "V3": (75, 1.85, 0.05),
    "V4": (55, 1.80, 0.10), "V5": (30, 1.45, 0.10), "V6": (0, 1.05, 0.10),
}


def lead_matrix():
    """Matrice 12×3: riga = vettore di derivazione (x sinistra, y basso, z avanti)."""
    I = np.array([1.0, 0.0, 0.0])
    II = np.array([math.cos(math.radians(60)), math.sin(math.radians(60)), 0.0])
    rows = {
        "I": I, "II": II, "III": II - I,
        "aVR": -(I + II) / 2, "aVL": I - II / 2, "aVF": II - I / 2,
    }
    for ld, (ang, g, yv) in PRECORD.items():
        a = math.radians(ang)
        rows[ld] = g * np.array([math.cos(a), yv, math.sin(a)])
    return np.stack([rows[ld] for ld in LEADS])


LM = lead_matrix()


def fvec(axis_deg: float, mag: float, z: float = 0.0):
    """Vettore 3D da asse nel piano frontale (convenzione esassiale: 0° = sinistra, +90° = basso),
    ampiezza della proiezione frontale (mV) e componente anteriore z (mV, + = avanti)."""
    a = math.radians(axis_deg)
    return np.array([mag * math.cos(a), mag * math.sin(a), z])


# ------------------------------------------------------------------ profili temporali
def agauss(t, c, sl, sr):
    """Gaussiana asimmetrica (sigma sinistra sl, destra sr)."""
    s = np.where(t < c, sl, sr)
    return np.exp(-0.5 * ((t - c) / s) ** 2)


def sigm(t, c, w):
    return 0.5 * (1 + np.tanh((t - c) / w))


# ------------------------------------------------------------------ morfologie
@dataclass
class Comp:
    c: float          # centro (frazione della durata dell'onda)
    s: float          # sigma (frazione), simmetrica se sr None
    v: np.ndarray     # vettore 3D (mV)
    sr: float | None = None


@dataclass
class VMorph:
    """Morfologia ventricolare: QRS (componenti), ripolarizzazione (T, ST, U)."""
    nome: str
    qrs: list
    qrs_dur: float = 0.090         # s
    t_vec: np.ndarray = field(default_factory=lambda: fvec(45, 0.30, 0.10))
    t_shape: tuple = (0.15, 0.11)  # sigma sin/dx della T come frazione del QT
    st_vec: np.ndarray | None = None   # vettore di corrente di lesione (sopra/sottoslivellamento ST)
    u_vec: np.ndarray | None = None    # onda U
    st_profilo: str = "plateau"        # 'plateau' (lesione) | 'precoce' (J che si esaurisce, de Winter)
                                       # | 'cucchiaio' (sottoslivellamento concavo, effetto digitalico)
    j_vec: np.ndarray | None = None    # onda J (di Osborn) alla fine del QRS
    qtc: float = 0.410             # s (correzione di Fridericia)
    qt_fisso: float | None = None  # se dato, ignora la frequenza


def qrs_normale(axis=55, mag=1.25, sett=0.20, base=0.40):
    """QRS normale a quattro componenti: setto, parete libera del VS (fase apicale-anteriore e fase
    laterale-posteriore: il vettore ruota in senso antiorario nel piano orizzontale), regioni basali."""
    return [
        Comp(0.17, 0.075, fvec(axis + 160, sett, 0.38)),            # setto: verso destra e in avanti
        Comp(0.40, 0.095, fvec(axis + 8, 0.62 * mag, 0.42 * mag)),  # VS apicale-anteriore
        Comp(0.56, 0.095, fvec(axis - 12, 0.62 * mag, -0.80 * mag)),  # VS laterale-posteriore
        Comp(0.80, 0.085, fvec(axis - 150, base, -0.30)),           # basali: in alto, a destra, indietro
    ]


def m_normale(axis=55, qrs_dur=0.090, qtc=0.410, t_mag=0.32, **kw):
    return VMorph("normale", qrs_normale(axis), qrs_dur, t_vec=fvec(axis - 10, t_mag, 0.12), qtc=qtc, **kw)


def m_bbd():
    """Blocco di branca destra: forze iniziali normali + forze terminali lente a destra e in avanti
    (rSR' in V1, S larga e impastata in I e V6); T discordante con il ritardo terminale in V1–V3."""
    q = qrs_normale(axis=60)
    q = [Comp(c.c * 0.62, c.s * 0.62, c.v) for c in q]  # attivazione sinistra normale nei primi ~80 ms
    q.append(Comp(0.79, 0.13, fvec(-170, 0.56, 0.45)))  # attivazione tardiva e lenta del VD
    return VMorph("BBD", q, 0.135, t_vec=fvec(40, 0.28, -0.28), qtc=0.43)


def m_bbs():
    """Blocco di branca sinistra: setto attivato da destra a sinistra (scompare la q in I/V6 e la r
    in V1 si riduce), attivazione lenta e intaccata del VS verso sinistra e indietro (R larga
    monofasica in I, aVL, V5–V6; QS/rS in V1–V3); ST-T discordanti."""
    q = [
        Comp(0.15, 0.08, fvec(10, 0.35, 0.06)),     # setto da destra a sinistra, appena anteriore
        Comp(0.42, 0.13, fvec(0, 1.00, -1.15)),     # VS: a sinistra e molto indietro
        Comp(0.70, 0.13, fvec(-15, 0.95, -0.95)),   # seconda gobba (intaccatura)
    ]
    return VMorph("BBS", q, 0.150, t_vec=fvec(170, 0.25, 0.30), st_vec=fvec(160, 0.07, 0.17), qtc=0.45)


def m_esv(sede="tratto_efflusso_VD", qtc=0.44):
    """Extrasistole/battito ventricolare: QRS largo, morfologia secondo la sede; T discordante."""
    if sede == "tratto_efflusso_VD":  # morfologia tipo BBS con asse inferiore
        q = [Comp(0.35, 0.17, fvec(85, 1.45, -0.55)), Comp(0.70, 0.15, fvec(60, 0.9, -0.85))]
        t = fvec(-100, 0.45, 0.25)
    elif sede == "VS":  # morfologia tipo BBD con asse destro
        q = [Comp(0.35, 0.17, fvec(150, 1.3, 0.85)), Comp(0.70, 0.15, fvec(170, 0.7, 0.45))]
        t = fvec(-30, 0.40, -0.35)
    else:
        raise ValueError(sede)
    return VMorph("ESV_" + sede, q, 0.150, t_vec=t, qtc=qtc)


def m_pacing_vd():
    """Stimolazione dall'apice del VD: QRS largo tipo BBS con asse superiore sinistro; T discordante."""
    q = [Comp(0.35, 0.17, fvec(-65, 1.45, -0.80)), Comp(0.70, 0.15, fvec(-40, 0.8, -0.70))]
    return VMorph("pacing_VD", q, 0.155, t_vec=fvec(115, 0.40, 0.35), qtc=0.46)


def m_scappamento_ventricolare():
    q = [Comp(0.25, 0.12, fvec(-100, 1.15, 0.60)), Comp(0.55, 0.12, fvec(-130, 0.9, 0.40)),
         Comp(0.80, 0.10, fvec(-165, 0.40, 0.20))]
    return VMorph("scappamento_ventricolare", q, 0.160, t_vec=fvec(70, 0.35, -0.30), qtc=0.47)


# onde P
P_SINUS = [Comp(0.33, 0.15, fvec(80, 0.12, 0.05)), Comp(0.66, 0.15, fvec(25, 0.10, -0.07))]  # dur 0,10 s
P_ECTOPICA_ALTA = [Comp(0.40, 0.18, fvec(20, 0.11, -0.06)), Comp(0.70, 0.15, fvec(0, 0.06, -0.04))]
P_RETROGRADA = [Comp(0.50, 0.20, fvec(-95, 0.12, 0.04))]  # negativa in II, III, aVF
P_STIMOLATA = [Comp(0.35, 0.18, fvec(75, 0.11, 0.03)), Comp(0.70, 0.17, fvec(30, 0.09, -0.05))]  # più larga


@dataclass
class Spike:
    t: float
    v: np.ndarray          # direzione e ampiezza (mV) nel piano frontale
    width: float = 0.002


# ------------------------------------------------------------------ costruttore del tracciato
class Tracciato:
    """Contenitore del segnale: si aggiungono eventi (P, QRS+T, spike, attività atriale continua)."""

    def __init__(self, durata: float, fs: int = FS, seed: int = 0):
        self.fs, self.durata = fs, durata
        self.t = np.arange(int(round(durata * fs))) / fs
        self.H = np.zeros((len(self.t), 3))
        self.rng = np.random.default_rng(seed)
        self.eventi = []   # verità di riferimento (per metadati e annotazioni)

    # --- onda P
    def add_p(self, t_on, comps=P_SINUS, dur=0.10, scale=1.0, tipo="P sinusale", ta_vec=None, ta_end=None):
        for c in comps:
            g = agauss(self.t, t_on + c.c * dur, c.s * dur, (c.sr or c.s) * dur)
            self.H += np.outer(g, c.v * scale)
        if ta_vec is not None and ta_end:  # lesione atriale: tratto PR spostato (pericardite)
            plat = sigm(self.t, t_on + dur * 0.9, 0.008) * (1 - sigm(self.t, ta_end, 0.004))
            self.H += np.outer(plat, ta_vec)
        self.eventi.append({"tipo": tipo, "t": round(t_on, 3), "durata": dur})

    # --- QRS + ripolarizzazione
    def add_qrs(self, t_on, m: VMorph, rr=1.0, tipo=None, qrs_scale=1.0, t_scale=1.0):
        D = m.qrs_dur
        for c in m.qrs:
            g = agauss(self.t, t_on + c.c * D, c.s * D, (c.sr or c.s) * D)
            self.H += np.outer(g, c.v * qrs_scale)
        qt = m.qt_fisso if m.qt_fisso else m.qtc * (max(rr, 0.25) ** (1 / 3))  # Fridericia
        qt = max(qt, D + 0.12)
        sl, sr = m.t_shape[0] * qt, m.t_shape[1] * qt
        t_end = t_on + qt
        t_peak = t_end - 2.3 * sr
        gT = agauss(self.t, t_peak, sl, sr)
        self.H += np.outer(gT, m.t_vec * t_scale)
        if m.st_vec is not None:
            j = t_on + D
            if m.st_profilo == "precoce":      # massimo al punto J, si esaurisce prima del picco della T
                plat = sigm(self.t, j - 0.005, 0.006) * np.exp(-np.clip(self.t - j, 0, None) / 0.05)
            elif m.st_profilo == "cucchiaio":  # concavità del tratto ST che si fonde con la T
                plat = agauss(self.t, j + 0.45 * (t_peak - j), 0.04, 0.07) * sigm(self.t, j - 0.005, 0.006)
            else:                              # corrente di lesione: plateau dal punto J alla fine della T
                plat = sigm(self.t, j - 0.005, 0.006) * (1 - sigm(self.t, t_end - 0.05, 0.03))
            self.H += np.outer(plat, m.st_vec)
        if m.j_vec is not None:  # onda J: gobba lenta subito dopo il QRS
            self.H += np.outer(agauss(self.t, t_on + D * 0.95, 0.012, 0.030), m.j_vec)
        if m.u_vec is not None:
            gU = agauss(self.t, t_end + 0.07, 0.04, 0.045)
            self.H += np.outer(gU, m.u_vec)
        self.eventi.append({"tipo": tipo or ("QRS " + m.nome), "t": round(t_on, 3), "qrs": D, "qt": round(qt, 3)})

    # --- spike di stimolazione
    def add_spike(self, t, v=None, tipo="spike"):
        v = fvec(-60, 2.0, 0.3) if v is None else v
        i = int(round(t * self.fs))
        w = max(1, int(0.002 * self.fs))
        if 0 <= i < len(self.t) - 3 * w:
            self.H[i:i + w] += v
            self.H[i + w:i + 3 * w] -= 0.25 * v
        self.eventi.append({"tipo": tipo, "t": round(t, 3)})

    # --- attività atriale continua (FA, flutter)
    def add_continuous(self, H):
        self.H += H

    def add_noise(self, mv=0.008, wander=0.0):
        """Rumore minimo (opzionale) per evitare un aspetto troppo «sintetico»."""
        if mv:
            n = self.rng.normal(0, mv, self.H.shape)
            k = np.ones(5) / 5
            for i in range(3):
                self.H[:, i] += np.convolve(n[:, i], k, mode="same")
        if wander:
            ph = self.rng.uniform(0, 2 * np.pi)
            self.H[:, 1] += wander * np.sin(2 * np.pi * 0.25 * self.t + ph)

    def leads(self):
        L = self.H @ LM.T
        return {ld: L[:, i] for i, ld in enumerate(LEADS)}


# ------------------------------------------------------------------ motori del ritmo
def _sinus_times(durata, hr, t0=0.25, mod=None, jitter=0.004, rng=None):
    rr0 = 60.0 / hr
    ts, t = [], t0
    while t < durata + 1.5:
        ts.append(t)
        rr = rr0 * (1 + (mod(t) if mod else 0))
        if rng is not None and jitter:
            rr *= 1 + rng.normal(0, jitter)
        t += rr
    return ts


def ritmo_condotto(durata, hr=72, pr=0.16, m: VMorph = None, p_comps=P_SINUS, p_dur=0.10,
                   mod=None, seed=0, t0=0.30, p_scale=1.0, rumore=0.0, ta_vec=None):
    """Ritmo sinusale (o atriale) condotto 1:1 con PR costante."""
    m = m or m_normale()
    tr = Tracciato(durata, seed=seed)
    ps = _sinus_times(durata, hr, t0, mod, rng=tr.rng)
    prev = None
    for tp in ps:
        tq = tp + pr
        rr = (tq - prev) if prev else 60 / hr
        tr.add_p(tp, p_comps, p_dur, scale=p_scale, ta_vec=ta_vec, ta_end=tq)
        tr.add_qrs(tq, m, rr)
        prev = tq
    tr.add_noise(rumore)
    return tr


def extrasistoli(durata, tipo="ESV", hr=72, pr=0.16, schema=(4,), accoppiamento=0.58, seed=0,
                 bigeminismo=False, m=None):
    """Ritmo sinusale con extrasistoli.
    tipo: 'ESA' (atriale), 'ESG' (giunzionale), 'ESV' (ventricolare).
    schema: indici dei battiti sinusali dopo i quali compare l'extrasistole.
    ESV: la P sinusale successiva cade nel periodo refrattario -> pausa compensatoria piena.
    ESA/ESG: il nodo del seno viene «resettato" -> pausa non compensatoria."""
    m = m or m_normale()
    tr = Tracciato(durata, seed=seed)
    rr0 = 60.0 / hr
    tp, k, prev_q, last_v = 0.30, 0, None, -9
    mv = m_esv("tratto_efflusso_VD")
    while tp < durata + 1:
        tq = tp + pr
        conducted = (tq - last_v) > 0.36  # P che cade durante l'ESV: non condotta
        tr.add_p(tp)
        if conducted:
            tr.add_qrs(tq, m, (tq - prev_q) if prev_q else rr0)
            prev_q = tq
        is_ext = (bigeminismo and conducted) or (k in schema and conducted)
        if is_ext:
            te = prev_q + accoppiamento * rr0
            if tipo == "ESV":
                tr.add_qrs(te, mv, accoppiamento * rr0, tipo="ESV")
                last_v = te
                tp += rr0
            elif tipo == "ESA":
                tpa = te - 0.17
                tr.add_p(tpa, P_ECTOPICA_ALTA, 0.09, tipo="P ectopica (ESA)")
                tr.add_qrs(te, m, accoppiamento * rr0, tipo="QRS ESA")
                prev_q = te
                tp = tpa + rr0 * 1.02  # ripristino del seno: pausa non compensatoria
            elif tipo == "ESG":
                tr.add_qrs(te, m, accoppiamento * rr0, tipo="QRS ESG")
                tr.add_p(te + 0.045, P_RETROGRADA, 0.08, tipo="P retrograda")
                prev_q = te
                tp = te + rr0 * 1.0
            k += 1
            continue
        tp += rr0
        k += 1
    return tr


def onde_f(tr, f_amp=0.075):
    """Onde f della FA: somma di oscillazioni a ≈ 5–7,5 Hz con frequenza, ampiezza e direzione
    lentamente variabili (più evidenti in V1 e nelle inferiori)."""
    rng, t = tr.rng, tr.t
    H = np.zeros((len(t), 3))
    for k in range(4):
        f0 = rng.uniform(5.0, 7.5)
        fm = f0 * (1 + 0.08 * np.sin(2 * np.pi * rng.uniform(0.1, 0.3) * t + rng.uniform(0, 6)))
        ph = 2 * np.pi * np.cumsum(fm) / tr.fs + rng.uniform(0, 2 * np.pi)
        env = 0.6 + 0.4 * np.sin(2 * np.pi * rng.uniform(0.15, 0.4) * t + rng.uniform(0, 6))
        d = fvec(rng.uniform(40, 120), 1.0, rng.uniform(0.6, 1.2))
        H += np.outer(env * np.sin(ph), d * f_amp / 2)
    return H


def fibrillazione_atriale(durata, fc_media=105, cv=0.22, seed=3, m=None, f_amp=0.075):
    """FA: onde f (≈ 6 Hz, ampiezza e frequenza variabili), nessuna P, RR irregolarmente irregolari."""
    m = m or m_normale()
    tr = Tracciato(durata, seed=seed)
    rng = tr.rng
    tr.add_continuous(onde_f(tr, f_amp))
    mean_rr = 60.0 / fc_media
    tq, prev = 0.25, None
    while tq < durata + 1:
        rr = (tq - prev) if prev else mean_rr
        tr.add_qrs(tq, m, rr, tipo="QRS (FA)")
        prev = tq
        tq += float(np.clip(rng.normal(mean_rr, cv * mean_rr), 0.36, 1.6))
    return tr


def flutter(durata, conduzione=2, f_rate=300, seed=5, m=None, f_amp=0.36, av=0.25):
    """Flutter atriale tipico (antiorario): onde F a dente di sega negative in II, III, aVF e positive
    in V1; conduzione AV fissa n:1."""
    m = m or m_normale()
    tr = Tracciato(durata, seed=seed)
    T = 60.0 / f_rate
    ph = (tr.t % T) / T
    # dente di sega: lenta discesa (75 % del ciclo) e rapida risalita (proiezione su II)
    saw = np.where(ph < 0.72, -ph / 0.72, -1 + (ph - 0.72) / 0.28)
    saw = saw - saw.mean()
    from scipy.ndimage import gaussian_filter1d
    saw = gaussian_filter1d(saw, 0.006 * tr.fs)
    d = fvec(-90, 1.0, 0.95)  # vettore superiore e anteriore -> F negative in II/III/aVF, positive in V1
    # orientiamo il segno: in II l'onda deve essere negativa con discesa lenta
    tr.add_continuous(np.outer(-saw, d * f_amp * 0.9))
    k, prev = 0, None
    tf = 0.0
    while tf < durata + 1:
        if k % conduzione == 0:
            tq = tf + av
            rr = (tq - prev) if prev else T * conduzione
            tr.add_qrs(tq, m, rr, tipo=f"QRS (flutter {conduzione}:1)")
            prev = tq
        tf += T
        k += 1
    tr.eventi.append({"tipo": "onde F", "frequenza": f_rate})
    return tr


def tsv_rientro(durata, fc=180, seed=7, m=None):
    """TSV da rientro nodale (TRNAV tipica): QRS stretti regolari, P retrograda quasi coincidente col
    QRS (pseudo-r' in V1, pseudo-S in II/III/aVF)."""
    m = m or m_normale()
    tr = Tracciato(durata, seed=seed)
    rr = 60.0 / fc
    tq = 0.20
    while tq < durata + 1:
        tr.add_qrs(tq, m, rr, tipo="QRS (TRNAV)")
        tr.add_p(tq + 0.055, P_RETROGRADA, 0.06, scale=0.9, tipo="P retrograda")
        tq += rr * (1 + tr.rng.normal(0, 0.002))
    return tr


def tachicardia_ventricolare(durata, fc=170, seed=9, sinus_hr=78, sede="tratto_efflusso_VD"):
    """TV monomorfa: QRS larghi identici, regolari; dissociazione AV (P sinusali indipendenti)."""
    tr = Tracciato(durata, seed=seed)
    mv = m_esv(sede)
    rr = 60.0 / fc
    tq = 0.20
    while tq < durata + 1:
        tr.add_qrs(tq, mv, rr, tipo="QRS (TV)")
        tq += rr
    for tp in _sinus_times(durata, sinus_hr, 0.45):
        tr.add_p(tp, scale=0.9, tipo="P dissociata")
    return tr


def torsione_di_punta(durata, fc=230, seed=11, ciclo_s=2.2):
    """Torsione di punta (modello FENOMENOLOGICO): complessi larghi a ≈ 200–250/min il cui vettore
    ruota progressivamente nel piano frontale: ampiezza e polarità «si attorcigliano» attorno alla
    linea di base. Preceduta da due battiti sinusali con QT molto lungo."""
    tr = Tracciato(durata, seed=seed)
    mlqt = m_normale(qtc=0.62)
    mlqt.t_vec = fvec(40, 0.35, 0.05)
    tr.add_p(0.10)
    tr.add_qrs(0.26, mlqt, 1.1)
    tr.add_p(1.25)
    tr.add_qrs(1.41, mlqt, 1.15)
    start = 1.41 + 0.50  # R su T dopo il secondo battito
    rr = 60.0 / fc
    tq, k = start, 0
    while tq < durata + 0.5:
        frac = (tq - start) / ciclo_s
        ang = 90 + 180 * frac                       # rotazione dell'asse
        amp = 0.55 + 1.15 * abs(math.sin(math.pi * frac))  # fusi di ampiezza
        v = fvec(ang, amp, 0.4 * math.cos(math.pi * frac))
        q = [Comp(0.5, 0.26, v)]
        m = VMorph("TdP", q, 0.16, t_vec=-0.45 * v, t_shape=(0.16, 0.14), qt_fisso=0.25)
        tr.add_qrs(tq, m, rr, tipo="complesso TdP")
        tq += rr * (1 + tr.rng.normal(0, 0.03))
        k += 1
    return tr


def fibrillazione_ventricolare(durata, grossolana=True, seed=13):
    """FV (modello FENOMENOLOGICO): oscillazioni caotiche 4–8 Hz di ampiezza e forma variabili,
    nessun QRS identificabile."""
    tr = Tracciato(durata, seed=seed)
    rng, t = tr.rng, tr.t
    amp = 0.55 if grossolana else 0.14
    H = np.zeros((len(t), 3))
    for k in range(6):
        f0 = rng.uniform(3.8, 7.5)
        fm = f0 * (1 + 0.15 * np.sin(2 * np.pi * rng.uniform(0.1, 0.5) * t + rng.uniform(0, 6)))
        ph = 2 * np.pi * np.cumsum(fm) / tr.fs + rng.uniform(0, 6)
        env = np.clip(0.5 + 0.5 * np.sin(2 * np.pi * rng.uniform(0.15, 0.6) * t + rng.uniform(0, 6)), 0.05, 1)
        d = fvec(rng.uniform(0, 360), 1.0, rng.uniform(-1, 1))
        H += np.outer(env * np.sin(ph), d * amp / 2.2)
    tr.add_continuous(H)
    tr.add_noise(0.01)
    tr.eventi.append({"tipo": "FV", "grossolana": grossolana})
    return tr


def asistolia(durata, onde_p=False, seed=15):
    tr = Tracciato(durata, seed=seed)
    if onde_p:
        for tp in _sinus_times(durata, 45, 0.5):
            tr.add_p(tp, scale=1.1)
    tr.add_noise(0.006, wander=0.03)
    return tr


def bav(durata, grado="1", hr_atriale=80, pr=0.16, seed=17, m=None, schema_mobitz2=3,
        scappamento="giunzionale"):
    """Blocchi atrioventricolari.
    grado '1'  : PR costante > 200 ms (pr)
    grado '2I' : Mobitz I (Wenckebach) 4:3 – PR progressivamente più lungo, poi P non condotta
    grado '2II': Mobitz II – PR costante, P non condotta ogni `schema_mobitz2` P (es. 3:2)
    grado '3'  : dissociazione AV completa con ritmo di scappamento (giunzionale o ventricolare)"""
    m = m or m_normale()
    tr = Tracciato(durata, seed=seed)
    ps = _sinus_times(durata, hr_atriale, 0.25, rng=tr.rng, jitter=0.002)
    prev = None
    if grado == "3":
        for tp in ps:
            tr.add_p(tp, tipo="P (non condotta)")
        if scappamento == "giunzionale":
            me, fce, t0 = m, 45, 0.55
        else:
            me, fce, t0 = m_scappamento_ventricolare(), 34, 0.80
        tq = t0
        while tq < durata + 1:
            tr.add_qrs(tq, me, 60 / fce, tipo="QRS di scappamento " + scappamento)
            tq += 60.0 / fce
        return tr
    seq_wenck = [0.20, 0.30, 0.355]
    for i, tp in enumerate(ps):
        tr.add_p(tp)
        if grado == "1":
            p = pr
        elif grado == "2I":
            j = i % 4
            if j == 3:
                tr.eventi[-1]["tipo"] = "P non condotta"
                continue
            p = seq_wenck[j]
        elif grado == "2II":
            if i % schema_mobitz2 == schema_mobitz2 - 1:
                tr.eventi[-1]["tipo"] = "P non condotta"
                continue
            p = pr
        tq = tp + p
        tr.add_qrs(tq, m, (tq - prev) if prev else 60 / hr_atriale)
        prev = tq
    return tr


def pacemaker(durata, modo="DDD", fc=70, av=0.17, seed=19):
    """Ritmi da pacemaker.
    AAI : spike atriale -> P stimolata -> conduzione AV spontanea (QRS stretto).
    VVI : spike ventricolare -> QRS largo (stimolazione apicale VD); nessuna attività atriale organizzata
          (qui: FA a bassa ampiezza, uno scenario tipico).
    DDD : spike atriale -> P, ritardo AV programmato -> spike ventricolare -> QRS largo."""
    tr = Tracciato(durata, seed=seed)
    rr = 60.0 / fc
    mn, mp = m_normale(), m_pacing_vd()
    va = fvec(-100, 2.4, 0.2)   # spike atriale (reso ben visibile a scopo didattico)
    vv = fvec(-100, 4.0, 0.3)   # spike ventricolare
    t = 0.30
    prev = None
    if modo == "VVI":
        tr.add_continuous(onde_f(tr, 0.05))
    while t < durata + 1:
        if modo == "AAI":
            tr.add_spike(t, va, "spike atriale")
            tr.add_p(t + 0.01, P_STIMOLATA, 0.11, tipo="P stimolata")
            tr.add_qrs(t + 0.20, mn, rr, tipo="QRS condotto")
        elif modo == "VVI":
            tr.add_spike(t, vv, "spike ventricolare")
            tr.add_qrs(t + 0.004, mp, rr, tipo="QRS stimolato")
        elif modo == "DDD":
            tr.add_spike(t, va, "spike atriale")
            tr.add_p(t + 0.01, P_STIMOLATA, 0.11, tipo="P stimolata")
            tr.add_spike(t + av, vv, "spike ventricolare")
            tr.add_qrs(t + av + 0.004, mp, rr, tipo="QRS stimolato")
        t += rr
    return tr


def elettroliti(durata, quadro, hr=72, seed=21):
    """Alterazioni elettrolitiche (ECG tipici, quadri didattici):
    'iperK_lieve'  : T alte, appuntite, a base stretta («a tenda»), QT normale-breve
    'iperK_grave'  : P appiattite, PR lungo, QRS largo, T alte e appuntite
    'ipoK'         : T appiattite, ST lievemente sottoslivellato, onda U evidente (QU apparente lungo)
    'iperCa'       : QT corto per accorciamento del tratto ST
    'ipoCa'        : QT lungo per allungamento del tratto ST (T di forma normale)"""
    if quadro == "iperK_lieve":
        m = m_normale(qtc=0.39, t_mag=0.85)
        m.t_shape = (0.085, 0.07)
        return ritmo_condotto(durata, hr, 0.16, m, seed=seed)
    if quadro == "iperK_grave":
        m = m_normale(qtc=0.42, t_mag=0.95)
        m.qrs_dur = 0.165
        m.qrs = [Comp(c.c, c.s * 1.25, c.v * 0.85) for c in m.qrs]
        m.t_shape = (0.10, 0.075)
        return ritmo_condotto(durata, hr, 0.24, m, p_dur=0.13, p_scale=0.35, seed=seed)
    if quadro == "ipoK":
        m = m_normale(qtc=0.41, t_mag=0.10)
        m.u_vec = fvec(50, 0.16, 0.12)
        m.st_vec = fvec(55, -0.06, -0.03)
        return ritmo_condotto(durata, hr, 0.17, m, seed=seed)
    if quadro == "iperCa":
        m = m_normale(qtc=0.33)
        return ritmo_condotto(durata, hr, 0.16, m, seed=seed)
    if quadro == "ipoCa":
        m = m_normale(qtc=0.52)
        m.t_shape = (0.115, 0.085)  # stessa larghezza assoluta della T: si allunga il tratto ST
        return ritmo_condotto(durata, hr, 0.16, m, seed=seed)
    raise ValueError(quadro)


TERRITORI = {
    # vettore di lesione (mV): punta verso la zona lesa -> ST sopraslivellato nelle derivazioni che la
    # «guardano», sottoslivellamento speculare nelle opposte
    "anteriore":  {"st": np.array([0.03, -0.07, 0.22]), "q": np.array([0.0, 0.0, -0.40]),
                   "nota": "ST↑ V1–V4 (max V2–V3); speculare lieve in II, III, aVF (DA prossimale)"},
    "inferiore":  {"st": np.array([-0.07, 0.21, -0.02]), "q": np.array([0.10, -0.40, 0.0]),
                   "nota": "ST↑ II, III, aVF con III > II (coronaria destra); speculare in I e aVL"},
    "laterale":   {"st": np.array([0.19, -0.10, -0.04]), "q": np.array([-0.40, 0.15, 0.0]),
                   "nota": "ST↑ I, aVL, V5–V6; speculare in III e aVF (circonflessa/diagonale)"},
    "inferolaterale": {"st": np.array([0.10, 0.17, -0.06]), "q": np.array([-0.25, -0.30, 0.0]),
                   "nota": "ST↑ II, III, aVF e V5–V6; speculare in aVR, V1"},
}


def stemi(durata, territorio="anteriore", hr=82, onde_q=False, seed=23):
    """STEMI acuto: corrente di lesione orientata verso il territorio + T iperacute concordanti;
    onde Q opzionali (fase evolutiva: perdita delle forze iniziali dirette verso la zona necrotica)."""
    info = TERRITORI[territorio]
    m = m_normale(qtc=0.42)
    m.st_vec = info["st"].copy()
    m.t_vec = m.t_vec + 1.1 * info["st"]
    if onde_q:
        m.qrs = m.qrs + [Comp(0.22, 0.11, info["q"])]
    return ritmo_condotto(durata, hr, 0.16, m, seed=seed)


# ------------------------------------------------------------------ quadri aggiunti (v2)
def m_wpw():
    """Pre-eccitazione ventricolare: la via accessoria attiva precocemente e LENTAMENTE una parte dei
    ventricoli (onda delta = rampa iniziale impastata che sfuma nell'R), poi l'attivazione normale;
    PR corto, QRS ≈ 0,12 s, ripolarizzazione secondaria opposta alla delta.
    Vettore della delta qui scelto in basso-a sinistra-in avanti (delta positiva in I, II, aVF, V2–V6):
    la localizzazione della via accessoria NON è rappresentata."""
    base = qrs_normale(axis=55)
    q = [Comp(0.46, 0.30, fvec(45, 0.70, 0.30), sr=0.06)]           # onda delta (rampa lenta)
    q += [Comp(0.38 + 0.62 * c.c, 0.62 * c.s, 0.85 * c.v) for c in base]
    return VMorph("WPW", q, 0.125, t_vec=fvec(-140, 0.16, -0.18), qtc=0.43)


def wpw(durata, hr=72, seed=31):
    # PR (inizio P -> inizio della delta) ≈ 0,10 s
    return ritmo_condotto(durata, hr, pr=0.095, m=m_wpw(), seed=seed)


def pericardite(durata, hr=92, seed=33):
    """Pericardite acuta (fase 1): sopraslivellamento ST diffuso a concavità superiore (vettore di lesione
    verso l'apice: ST↑ in I, II, aVF, V2–V6; ST↓ in aVR e spesso V1) e sottoslivellamento del PR
    (lesione atriale: PR↓ nelle stesse derivazioni, PR↑ in aVR); nessuna onda Q."""
    m = m_normale(qtc=0.42)
    m.st_vec = fvec(55, 0.17, 0.07)
    m.t_vec = m.t_vec + fvec(55, 0.08, 0.03)
    return ritmo_condotto(durata, hr, 0.16, m, seed=seed, ta_vec=-fvec(60, 0.055, 0.0))


def infarto_posteriore(durata, hr=80, seed=35):
    """Infarto posteriore (infero-basale) acuto visto dalle precordiali anteriori: immagine speculare
    di lesione posteriore = sottoslivellamento ST orizzontale in V1–V3 con R alte e T positive."""
    m = m_normale(qtc=0.42)
    m.st_vec = np.array([0.02, 0.02, -0.17])
    m.qrs = m.qrs + [Comp(0.45, 0.11, np.array([0.0, 0.0, 0.45]))]  # perdita delle forze posteriori
    m.t_vec = m.t_vec + np.array([0.0, 0.0, 0.18])
    return ritmo_condotto(durata, hr, 0.16, m, seed=seed)


def wellens(durata, hr=70, seed=37):
    """Pattern di Wellens tipo B (fase senza dolore): T profonde e simmetriche in V2–V3 (spesso V1–V4),
    ST isoelettrico o appena sopraslivellato, onda R conservata, nessuna onda Q."""
    m = m_normale(qtc=0.43)
    m.t_vec = fvec(35, 0.16, -0.42)
    m.t_shape = (0.12, 0.12)
    return ritmo_condotto(durata, hr, 0.16, m, seed=seed)


def de_winter(durata, hr=85, seed=39):
    """Pattern di de Winter: sottoslivellamento del punto J con tratto ST ascendente che si continua in
    T alte e simmetriche nelle precordiali (V1–V6), lieve ST↑ in aVR; nessun sopraslivellamento ST."""
    m = m_normale(qtc=0.42)
    m.st_vec = np.array([-0.05, 0.03, -0.20])
    m.st_profilo = "precoce"
    m.t_vec = fvec(40, 0.30, 0.55)
    m.t_shape = (0.11, 0.10)
    return ritmo_condotto(durata, hr, 0.16, m, seed=seed)


def ipotermia(durata, hr=44, seed=41):
    """Ipotermia: bradicardia, onda J di Osborn (gobba alla fine del QRS concordante con l'R, più evidente
    in II, aVF, V3–V6), QT lungo."""
    m = m_normale(qtc=0.49)
    m.j_vec = fvec(55, 0.30, 0.10)
    return ritmo_condotto(durata, hr, 0.20, m, seed=seed)


def digitalico(durata, hr=64, seed=43):
    """Effetto digitalico (non tossicità): sottoslivellamento ST «a cucchiaio» nelle derivazioni con R
    dominante, T appiattite, QT accorciato, PR ai limiti alti."""
    m = m_normale(qtc=0.37, t_mag=0.14)
    m.st_vec = -fvec(50, 0.13, 0.06)
    m.st_profilo = "cucchiaio"
    return ritmo_condotto(durata, hr, 0.20, m, seed=seed)


# ------------------------------------------------------------------ quadri aggiunti (v3, lacune del confronto)
P_MITRALICA = [Comp(0.28, 0.14, fvec(75, 0.10, 0.05)), Comp(0.70, 0.14, fvec(30, 0.13, -0.14))]   # dur 0,13
P_POLMONARE = [Comp(0.40, 0.17, fvec(78, 0.27, 0.10)), Comp(0.68, 0.15, fvec(40, 0.06, -0.03))]   # dur 0,10
P_MULTI = [  # morfologie di P di focolai atriali diversi (pacemaker migrante / TAM)
    P_SINUS,
    [Comp(0.45, 0.20, fvec(20, 0.09, -0.04))],                       # P bassa e piatta in II
    [Comp(0.45, 0.20, fvec(-80, 0.09, 0.03))],                       # P negativa in II (focolaio basso)
    [Comp(0.35, 0.15, fvec(95, 0.16, 0.10)), Comp(0.70, 0.12, fvec(60, 0.05, 0.0))],  # P appuntita
]


def pausa_sinusale(durata, hr=70, pausa_s=2.6, scappamento="giunzionale", seed=51):
    """Pausa/arresto sinusale: dopo il 4° battito il nodo del seno tace per `pausa_s` secondi; un battito di
    scappamento (giunzionale: QRS stretto senza P; ventricolare: QRS largo) interrompe la pausa, poi il
    ritmo sinusale riprende."""
    m = m_normale()
    tr = Tracciato(durata, seed=seed)
    rr = 60.0 / hr
    t, prev = 0.30, None
    for _ in range(4):
        tr.add_p(t)
        tr.add_qrs(t + 0.16, m, rr)
        prev = t + 0.16
        t += rr
    t_esc = prev + pausa_s
    if scappamento == "giunzionale":
        tr.add_qrs(t_esc, m, pausa_s, tipo="QRS di scappamento giunzionale")
    else:
        tr.add_qrs(t_esc, m_scappamento_ventricolare(), pausa_s, tipo="QRS di scappamento ventricolare")
    tr.eventi.append({"tipo": "pausa sinusale", "t": round(prev, 3), "durata": round(pausa_s, 2)})
    t = t_esc + 0.95 * rr
    prev = t_esc
    while t < durata + 1:
        tr.add_p(t)
        tr.add_qrs(t + 0.16, m, (t + 0.16) - prev)
        prev = t + 0.16
        t += rr
    return tr


def esa_non_condotta(durata, hr=72, bigeminismo=False, seed=53):
    """Extrasistole atriale NON condotta: P prematura che cade sulla T (nodo AV ancora refrattario), nessun QRS,
    pausa. Con bigeminismo=True: bigeminismo atriale CONDOTTO (ogni battito sinusale seguito da un'ESA)."""
    m = m_normale()
    tr = Tracciato(durata, seed=seed)
    rr = 60.0 / hr
    t, prev, k = 0.30, None, 0
    while t < durata + 1:
        tr.add_p(t)
        tq = t + 0.16
        tr.add_qrs(tq, m, (tq - prev) if prev else rr)
        prev = tq
        if bigeminismo:
            tpa = tq + 0.42 * rr
            tr.add_p(tpa, P_ECTOPICA_ALTA, 0.09, tipo="P ectopica (ESA)")
            tr.add_qrs(tpa + 0.18, m, tpa + 0.18 - prev, tipo="QRS ESA")
            prev = tpa + 0.18
            t = tpa + 1.05 * rr
        elif k in (2, 6):
            tpa = tq + 0.27  # sulla T: non condotta
            tr.add_p(tpa, P_ECTOPICA_ALTA, 0.09, tipo="P ectopica non condotta")
            t = tpa + 1.05 * rr
        else:
            t += rr
        k += 1
    return tr


def esv_complesse(durata, hr=75, quadro="multifocali", seed=55):
    """Extrasistoli ventricolari complesse su ritmo sinusale.
    'multifocali': ESV di due morfologie diverse (due focolai) · 'coppia': due ESV consecutive ·
    'R_su_T': ESV con accoppiamento molto breve che cade sull'apice della T precedente."""
    m = m_normale()
    tr = Tracciato(durata, seed=seed)
    rr = 60.0 / hr
    mA, mB = m_esv("tratto_efflusso_VD"), m_esv("VS")
    piano = {"multifocali": {2: [(0.60, mA)], 6: [(0.58, mB)]},
             "coppia": {3: [(0.58, mA), (0.95, mA)]},
             "R_su_T": {3: [(0.33, mA)]}}[quadro]
    t, prev, k, last_v = 0.30, None, 0, -9
    while t < durata + 1:
        tq = t + 0.16
        tr.add_p(t)
        if tq - last_v > 0.56:  # la P che segue l'ESV trova i ventricoli refrattari: pausa compensatoria
            tr.add_qrs(tq, m, (tq - prev) if prev else rr)
            prev = tq
            for frac, mv in piano.get(k, []):
                te = prev + frac * rr
                tr.add_qrs(te, mv, frac * rr, tipo=f"ESV ({mv.nome})")
                last_v = te
        t += rr
        k += 1
    return tr


def m_eas():
    """Blocco fascicolare anteriore sinistro: asse ≈ −60°, qR in I e aVL, rS in II, III, aVF; QRS < 0,12 s."""
    return m_normale(axis=-60, qrs_dur=0.100)


def m_eps():
    """Blocco fascicolare posteriore sinistro: asse ≈ +120°, rS in I e aVL, qR in II, III, aVF."""
    m = m_normale(axis=115, qrs_dur=0.100)
    m.t_vec = fvec(70, 0.28, 0.12)
    return m


def m_bifascicolare():
    """BBD + blocco fascicolare anteriore sinistro."""
    m = m_bbd()
    base = qrs_normale(axis=-60)
    m.qrs = [Comp(c.c * 0.62, c.s * 0.62, c.v) for c in base] + [m.qrs[-1]]
    return m


def m_ivd():
    """Ipertrofia ventricolare destra: forze dominanti a destra e in avanti (R alta in V1, S persistenti in
    V5–V6, asse destro ≈ +110°), T negative in V1–V3 (sovraccarico)."""
    q = [Comp(0.17, 0.075, fvec(-60, 0.15, 0.30)),
         Comp(0.45, 0.13, fvec(115, 1.00, 0.95)),
         Comp(0.75, 0.10, fvec(-150, 0.45, 0.10))]
    return VMorph("IVD", q, 0.100, t_vec=fvec(30, 0.20, -0.30), qtc=0.42)


def m_ivs_strain():
    """Ipertrofia ventricolare sinistra con sovraccarico: voltaggi aumentati (SV1 + RV5/V6 > 3,5 mV), QRS
    lievemente allargato, ST sottoslivellato e T asimmetriche negative in I, aVL, V5–V6."""
    m = m_normale(axis=20, qrs_dur=0.105, qtc=0.43)
    m.qrs = [Comp(c.c, c.s, c.v * (1.9 if i in (1, 2) else 1.0)) for i, c in enumerate(m.qrs)]
    m.t_vec = fvec(-170, 0.30, 0.25)
    m.t_shape = (0.12, 0.13)
    m.st_vec = fvec(-160, 0.07, 0.05)
    return m


def atriale_multifocale(durata, fc=115, seed=57, migrante=False):
    """Tachicardia atriale multifocale (fc > 100/min) o pacemaker atriale migrante (fc < 100/min):
    ≥ 3 morfologie di P diverse, PR variabili, RR irregolari; ogni P è condotta."""
    m = m_normale()
    tr = Tracciato(durata, seed=seed)
    rng = tr.rng
    base = 60.0 / (72 if migrante else fc)
    t, prev = 0.25, None
    while t < durata + 1:
        k = int(rng.integers(0, len(P_MULTI)))
        pr = float(rng.uniform(0.12, 0.20))
        tr.add_p(t, P_MULTI[k], 0.10, tipo=f"P morfologia {k + 1}")
        tq = t + pr
        tr.add_qrs(tq, m, (tq - prev) if prev else base)
        prev = tq
        t += base * float(rng.uniform(0.82, 1.18))
    return tr


def flutter_ventricolare(durata, fc=280, seed=59):
    """Flutter ventricolare: onde sinusoidali ampie e regolari ≈ 250–300/min, senza distinzione tra QRS e T."""
    tr = Tracciato(durata, seed=seed)
    f = fc / 60.0
    env = 1.0 + 0.08 * np.sin(2 * np.pi * 0.3 * tr.t)
    tr.add_continuous(np.outer(env * np.sin(2 * np.pi * f * tr.t), fvec(70, 1.1, 0.5)))
    tr.add_noise(0.01)
    tr.eventi.append({"tipo": "flutter ventricolare", "frequenza": fc})
    return tr


def ta_con_blocco(durata, fa=180, conduzione=2, seed=61):
    """Tachicardia atriale con blocco AV 2:1 (quadro tipico della tossicità digitalica): P' ectopiche
    regolari ≈ 180/min con linea isoelettrica tra loro (a differenza del flutter), una ogni due condotta."""
    m = m_normale()
    tr = Tracciato(durata, seed=seed)
    T = 60.0 / fa
    t, k, prev = 0.20, 0, None
    while t < durata + 1:
        tr.add_p(t, P_ECTOPICA_ALTA, 0.08, scale=1.3, tipo="P ectopica")
        if k % conduzione == 0:
            tq = t + 0.20
            tr.add_qrs(tq, m, (tq - prev) if prev else T * conduzione)
            prev = tq
        t += T
        k += 1
    return tr


def bav_avanzato(durata, hr_atriale=90, rapporto=3, seed=63):
    """BAV di 2° grado avanzato (es. 3:1): due o più P consecutive non condotte, PR costante nei battiti
    condotti, QRS spesso largo."""
    m = m_bbd()
    tr = Tracciato(durata, seed=seed)
    rr = 60.0 / hr_atriale
    t, k, prev = 0.30, 0, None
    while t < durata + 1:
        tr.add_p(t, tipo="P" if k % rapporto == 0 else "P non condotta")
        if k % rapporto == 0:
            tq = t + 0.18
            tr.add_qrs(tq, m, (tq - prev) if prev else rr * rapporto)
            prev = tq
        t += rr
        k += 1
    return tr


def sottoslivellamento_diffuso(durata, hr=95, seed=65):
    """Sottoslivellamento ST diffuso (I, II, aVF, V4–V6) con sopraslivellamento in aVR: ischemia
    subendocardica estesa (es. stenosi del tronco comune o multivasale) nel contesto clinico adatto."""
    m = m_normale(qtc=0.42)
    m.st_vec = fvec(-125, 0.17, -0.10)
    return ritmo_condotto(durata, hr, 0.16, m, seed=seed)


def bassi_voltaggi(durata, hr=88, seed=67):
    """Bassi voltaggi: QRS < 0,5 mV in tutte le periferiche e < 1 mV nelle precordiali (versamento
    pericardico, BPCO, obesità, mixedema, cardiopatie infiltrative)."""
    m = m_normale()
    m.qrs = [Comp(c.c, c.s, c.v * 0.33) for c in m.qrs]
    m.t_vec = m.t_vec * 0.4
    return ritmo_condotto(durata, hr, 0.16, m, p_scale=0.6, seed=seed)


def ingrandimento_atriale(durata, lato="sinistro", hr=78, seed=69):
    if lato == "sinistro":
        return ritmo_condotto(durata, hr, 0.18, p_comps=P_MITRALICA, p_dur=0.13, seed=seed)
    return ritmo_condotto(durata, hr, 0.16, p_comps=P_POLMONARE, p_dur=0.10, seed=seed)
