#!/usr/bin/env python3
"""
Schemi originali del Volume A, disegnati interamente con codice (matplotlib), in bianco e nero.
Nessuna anatomia pittorica: solo diagrammi, curve calcolate e geometria delle derivazioni.

  SCH-PA-VENT    potenziale d'azione del miocita ventricolare (fasi 0–4) con correnti principali
  SCH-PA-NSA     potenziale d'azione della cellula del nodo del seno (depolarizzazione diastolica)
  SCH-WIGGERS    ciclo cardiaco (diagramma di Wiggers semplificato) con ECG simulato e toni
  SCH-CONDUZ     sistema di conduzione come diagramma a blocchi con tempi e frequenze intrinseche
  SCH-EINTH      triangolo di Einthoven e sistema esassiale
  SCH-PRECORD    posizione degli elettrodi precordiali (schema del torace con linee di repere)
  SCH-TERRIT     territori coronarici sullo schema delle 12 derivazioni

Uscite: out/<ID>.svg, out/<ID>.png (300 dpi, grigi), out/<ID>.json (metadati per il MANIFEST).
Uso: python3 genera_schemi.py
"""
import json
import math
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle, Circle, FancyArrowPatch  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "out"
sys.path.insert(0, str(HERE.parent / "sim"))
sys.path.insert(0, str(HERE.parent / "common"))

MM = 1 / 25.4
LW = 1.0       # linee principali (pt) – minimo KDP 0,75 pt
LW_THIN = 0.75
G_LIGHT = "#d9d9d9"   # 15 %
G_MID = "#a6a6a6"     # 35 %
G_DARK = "#595959"    # 65 %
matplotlib.rcParams.update({"svg.fonttype": "path", "font.family": "DejaVu Sans", "font.size": 7,
                            "axes.linewidth": LW_THIN, "xtick.major.width": LW_THIN,
                            "ytick.major.width": LW_THIN, "svg.hashsalt": "schemi-volume-A",
                            "lines.linewidth": LW, "hatch.linewidth": 0.75})


def save(fig, sid, titolo, descr, criteri, w_mm):
    OUT.mkdir(exist_ok=True)
    fig.savefig(OUT / f"{sid}.svg", metadata={"Date": None})
    fig.savefig(OUT / f"{sid}.png", dpi=300)
    from PIL import Image
    Image.open(OUT / f"{sid}.png").convert("L").save(OUT / f"{sid}.png", optimize=True, dpi=(300, 300))
    plt.close(fig)
    meta = {"id": sid, "titolo": titolo, "tipo": "schema", "gruppo": "schemi",
            "fonte": "Schema originale generato con codice (figure/schemi/genera_schemi.py)",
            "licenza": "Originale del volume", "file": {"svg": f"schemi/out/{sid}.svg", "png": f"schemi/out/{sid}.png"},
            "dimensioni_mm": [w_mm, None], "scala": 1.0, "descrizione_attesa": descr,
            "criteri_revisore": criteri, "stato_validazione": "da_validare"}
    (OUT / f"{sid}.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print("schema", sid)


def smoothstep(t, a, b):
    x = np.clip((t - a) / (b - a), 0, 1)
    return x * x * (3 - 2 * x)


# ------------------------------------------------------------------ potenziali d'azione
def pa_ventricolare():
    """Curva calcolata: somma di transizioni sigmoidi che riproducono le cinque fasi (valori tipici:
    riposo −90 mV, picco ≈ +30 mV, plateau ≈ 0/+10 mV, durata ≈ 300 ms)."""
    t = np.linspace(-50, 450, 2000)
    v = np.full_like(t, -90.0)
    v += 120 * smoothstep(t, 0, 2)                     # fase 0: ingresso rapido di Na+
    v -= 22 * smoothstep(t, 2, 12)                     # fase 1: ripolarizzazione precoce (Ito, K+)
    v -= 8 * smoothstep(t, 12, 200)                    # fase 2: plateau (Ca2+ in, K+ out)
    v -= 90 * smoothstep(t, 190, 320)                  # fase 3: ripolarizzazione (IKr, IKs) fino a −90 mV
    v = np.where(t < 0, -90.0, v)
    w = 140
    fig, ax = plt.subplots(figsize=(w * MM, 62 * MM))
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.17, top=0.96)
    ax.plot(t, v, color="black", lw=1.5)
    ax.axhline(0, color=G_MID, lw=LW_THIN, ls=(0, (4, 3)))
    ax.axhline(-90, color=G_MID, lw=LW_THIN, ls=(0, (4, 3)))
    ax.axvspan(0, 250, ymin=0.02, ymax=0.06, color=G_LIGHT)
    ax.text(125, -103, "periodo refrattario assoluto", ha="center", va="center", fontsize=6)
    lab = [(-30, -20, "0", "Na⁺ entra"), (25, 32, "1", "K⁺ esce (Ito)"), (110, 13, "2", "plateau: Ca²⁺ entra, K⁺ esce"),
           (265, -25, "3", "K⁺ esce"), (335, -84, "4", "riposo (−90 mV)")]
    for x, y, n, s in lab:
        ax.annotate("", xy=(x, y), xytext=(x + (14 if n != "0" else 18), y + 10),
                    arrowprops=dict(arrowstyle="-", lw=LW_THIN, color="black")) if False else None
        ax.text(x, y + 6, n, ha="center", fontsize=8, fontweight="bold",
                bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec="black", lw=LW_THIN))
        ax.text(x + 12, y + 6, s, ha="left", va="center", fontsize=6.5)
    ax.set_xlim(-50, 450)
    ax.set_ylim(-110, 50)
    ax.set_xlabel("tempo (ms)")
    ax.set_ylabel("potenziale (mV)")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "SCH-PA-VENT", "Potenziale d'azione del miocita ventricolare",
         "Fasi 0–4 del potenziale d'azione ventricolare con le correnti ioniche principali e il periodo refrattario assoluto.",
         ["riposo ≈ −90 mV", "fase 0 rapida (Na⁺)", "plateau (Ca²⁺)", "fase 3 (K⁺)", "durata ≈ 250–300 ms"], w)


def pa_nodo_seno():
    t = np.linspace(0, 1700, 3000)
    period = 800.0
    v = np.empty_like(t)
    for i, ti in enumerate(t):
        ph = (ti + 150) % period
        # fase 4: depolarizzazione diastolica lenta da −60 a −40 mV (corrente If, poi Ca2+ T)
        if ph < 520:
            v[i] = -60 + 20 * (ph / 520) ** 1.3
        elif ph < 620:   # fase 0: salita lenta (Ca2+ L), picco ≈ +10 mV
            v[i] = -40 + 50 * smoothstep(np.array(ph), 520, 610)
        else:            # fase 3: ripolarizzazione (K+)
            v[i] = 10 - 70 * smoothstep(np.array(ph), 620, 800)
    w = 140
    fig, ax = plt.subplots(figsize=(w * MM, 55 * MM))
    fig.subplots_adjust(left=0.11, right=0.98, bottom=0.19, top=0.95)
    ax.plot(t, v, color="black", lw=1.5)
    ax.axhline(-40, color=G_DARK, lw=LW_THIN, ls=(0, (4, 3)))
    ax.text(1690, -38, "soglia ≈ −40 mV", ha="right", va="bottom", fontsize=6.5)
    ax.text(200, -58, "4", fontsize=8, fontweight="bold", bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec="black", lw=LW_THIN))
    ax.text(260, -60, "depolarizzazione diastolica\n(If «funny», poi Ca²⁺)", fontsize=6.5, va="center")
    ax.text(470, 2, "0", fontsize=8, fontweight="bold", bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec="black", lw=LW_THIN))
    ax.text(520, 6, "Ca²⁺ entra (lenta)", fontsize=6.5, va="center")
    ax.text(620, -24, "3", fontsize=8, fontweight="bold", bbox=dict(boxstyle="circle,pad=0.2", fc="white", ec="black", lw=LW_THIN))
    ax.text(670, -26, "K⁺ esce", fontsize=6.5, va="center")
    ax.set_xlim(0, 1700)
    ax.set_ylim(-70, 25)
    ax.set_xlabel("tempo (ms)")
    ax.set_ylabel("potenziale (mV)")
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    save(fig, "SCH-PA-NSA", "Potenziale d'azione della cellula del nodo del seno",
         "Automatismo: fase 4 instabile che raggiunge la soglia; fase 0 lenta da calcio; nessun plateau. Frequenza dell'esempio 75/min.",
         ["potenziale diastolico massimo ≈ −60 mV", "soglia ≈ −40 mV", "fase 0 lenta", "assenza delle fasi 1–2"], w)


# ------------------------------------------------------------------ Wiggers
def wiggers():
    import ecgsim
    T = 0.8
    t = np.linspace(0, T, 2000)
    # tempi (s) del ciclo a 75/min, valori indicativi da manuale di fisiologia
    t_qrs, t_mv_close, t_av_open, t_av_close, t_mv_open = 0.0, 0.05, 0.10, 0.37, 0.45
    # pressione ventricolare sinistra: tratti raccordati in modo continuo
    lv = np.empty_like(t)
    for i, ti in enumerate(t):
        if ti < t_mv_close:
            lv[i] = 10 + 2 * smoothstep(np.array(ti), 0.0, t_mv_close)
        elif ti < t_av_open:
            lv[i] = 12 + 68 * smoothstep(np.array(ti), t_mv_close, t_av_open)
        elif ti < t_av_close:
            x = (ti - t_av_open) / (t_av_close - t_av_open)
            lv[i] = 80 + 38 * math.sin(math.pi * x) + 15 * x
        elif ti < t_mv_open:
            lv[i] = 95 - 89 * smoothstep(np.array(ti), t_av_close, t_mv_open)
        else:
            lv[i] = 6 + 2 * smoothstep(np.array(ti), t_mv_open, 0.70) + 3 * math.exp(-((ti - 0.74) / 0.025) ** 2) \
                + 1 * smoothstep(np.array(ti), 0.70, 0.80)
    # aorta: segue il VS in eiezione; incisura dicrota alla chiusura; poi decadimento fino a 80 mmHg
    dec = lambda dt: 80 + 14 * (math.exp(-dt / 0.3) - math.exp(-0.53 / 0.3)) / (1 - math.exp(-0.53 / 0.3))
    ao = np.empty_like(t)
    for i, ti in enumerate(t):
        if t_av_open <= ti < t_av_close:
            ao[i] = max(80.0, lv[i] - 2 * smoothstep(np.array(ti), t_av_open, t_av_open + 0.03))
        elif ti >= t_av_close:
            ao[i] = dec(ti - t_av_close) - 5 * math.exp(-((ti - t_av_close - 0.012) / 0.007) ** 2)
        else:
            ao[i] = dec(ti + T - t_av_close)
    # atrio sinistro (onde a, c, v)
    la = 6 + 4 * np.exp(-((t - 0.72) / 0.03) ** 2) + 2 * np.exp(-((t - 0.07) / 0.02) ** 2) + \
        6 * smoothstep(t, 0.15, t_mv_open) - 6 * smoothstep(t, t_mv_open, 0.55)
    # volume ventricolare
    vol = 120 - 70 * smoothstep(t, t_av_open, t_av_close) + 45 * smoothstep(t, t_mv_open, 0.62) + \
        25 * smoothstep(t, 0.68, 0.78) * (t > 0.6)
    vol = np.where(t < t_av_open, 120.0, vol)
    # ECG simulato (derivazione II), allineato: QRS al tempo 0 -> spostiamo di 0,03 s
    tr = ecgsim.ritmo_condotto(2.0, hr=75, pr=0.16)
    L = tr.leads()["II"]
    q0 = [e["t"] for e in tr.eventi if e["tipo"].startswith("QRS")][1]
    ecg_t = np.arange(len(L)) / 1000 - q0 - 0.035  # il QRS precede la salita della pressione
    m = (ecg_t >= -0.05) & (ecg_t <= T)
    w = 140
    fig, axs = plt.subplots(3, 1, figsize=(w * MM, 125 * MM), sharex=True,
                            gridspec_kw={"height_ratios": [3, 1.3, 1.0]})
    fig.subplots_adjust(left=0.12, right=0.97, bottom=0.08, top=0.97, hspace=0.12)
    a = axs[0]
    a.plot(t, ao, color="black", lw=1.5, label="aorta")
    a.plot(t, lv, color="black", lw=1.5, ls=(0, (6, 2)), label="ventricolo sinistro")
    a.plot(t, la, color=G_DARK, lw=1.25, label="atrio sinistro")
    a.set_ylabel("pressione (mmHg)")
    a.set_ylim(0, 135)
    a.legend(loc="upper right", fontsize=6, frameon=False)
    for x, s in [(t_mv_close, "chiusura\nmitrale"), (t_av_open, "apertura\naortica"),
                 (t_av_close, "chiusura\naortica"), (t_mv_open, "apertura\nmitrale")]:
        for ax_ in axs:
            ax_.axvline(x, color=G_MID, lw=LW_THIN, ls=(0, (2, 2)))
        a.text(x, 128, s, ha="center", va="top", fontsize=5.5)
    a.axvspan(t_mv_close, t_av_open, color=G_LIGHT, lw=0)
    a.axvspan(t_av_close, t_mv_open, color=G_LIGHT, lw=0)
    a.text((t_mv_close + t_av_open) / 2, 45, "contrazione\nisovolumetrica", rotation=90, ha="center", va="center", fontsize=5.5)
    a.text((t_av_close + t_mv_open) / 2, 45, "rilasciamento\nisovolumetrico", rotation=90, ha="center", va="center", fontsize=5.5)
    a.text(0.24, 20, "eiezione", ha="center", fontsize=6.5)
    a.text(0.62, 20, "riempimento", ha="center", fontsize=6.5)
    b = axs[1]
    b.plot(t, vol, color="black", lw=1.5)
    b.set_ylabel("volume VS\n(mL)")
    b.set_ylim(35, 135)
    c = axs[2]
    c.plot(ecg_t[m], L[m], color="black", lw=1.25)
    c.set_ylabel("ECG (II)")
    c.set_yticks([])
    for x, s in [(0.02, "S1"), (t_av_close + 0.01, "S2")]:
        c.text(x, -0.55, s, ha="center", fontsize=7, fontweight="bold")
    c.set_ylim(-0.8, 1.4)
    c.set_xlabel("tempo (s) – ciclo a 75/min")
    for ax_ in axs:
        for sp in ("top", "right"):
            ax_.spines[sp].set_visible(False)
    c.set_xlim(-0.05, T)
    save(fig, "SCH-WIGGERS", "Ciclo cardiaco (diagramma di Wiggers semplificato)",
         "Pressioni in aorta, ventricolo e atrio sinistri, volume ventricolare, ECG e toni cardiaci in un ciclo a 75/min; fasi isovolumetriche evidenziate.",
         ["sequenza delle valvole", "valori indicativi (Ao 120/80, VS 120/8, AS 5–12 mmHg)", "S1 alla chiusura delle AV, S2 alla chiusura delle semilunari",
          "QRS precede la salita della pressione ventricolare"], w)


# ------------------------------------------------------------------ sistema di conduzione
def conduzione():
    w = 140
    fig, ax = plt.subplots(figsize=(w * MM, 95 * MM))
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 95)
    ax.axis("off")

    def box(x, y, bw, bh, title, sub, fill="white"):
        ax.add_patch(FancyBboxPatch((x, y), bw, bh, boxstyle="round,pad=0.6,rounding_size=1.5",
                                    fc=fill, ec="black", lw=LW))
        ax.text(x + bw / 2, y + bh * 0.64, title, ha="center", va="center", fontsize=7, fontweight="bold")
        ax.text(x + bw / 2, y + bh * 0.28, sub, ha="center", va="center", fontsize=5.8)

    def arr(x1, y1, x2, y2):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=7, lw=LW, color="black"))

    box(45, 80, 50, 11, "Nodo del seno", "pacemaker: 60–100/min", G_LIGHT)
    box(45, 63, 50, 10, "Atri (vie internodali)", "onda P ≈ 0,08–0,10 s")
    box(45, 46, 50, 10, "Nodo atrioventricolare", "ritardo → segmento PR; 40–60/min", G_LIGHT)
    box(45, 30, 50, 9, "Fascio di His", "giunzione: 40–60/min")
    box(10, 14, 45, 9, "Branca destra", "")
    box(85, 14, 45, 9, "Branca sinistra", "fascicolo anteriore e posteriore")
    box(30, 1, 80, 8, "Fibre di Purkinje → miocardio ventricolare", "QRS < 0,12 s; scappamento 20–40/min", G_LIGHT)
    arr(70, 80, 70, 73.6)
    arr(70, 63, 70, 56.6)
    arr(70, 46, 70, 39.6)
    arr(60, 30, 40, 23.6)
    arr(80, 30, 100, 23.6)
    arr(32, 14, 55, 9.6)
    arr(108, 14, 85, 9.6)
    # scala dei tempi a destra
    ax.text(118, 85, "P", fontsize=8, fontweight="bold", ha="center")
    ax.text(118, 51, "PR", fontsize=8, fontweight="bold", ha="center")
    ax.text(14, 5, "QRS", fontsize=8, fontweight="bold", ha="center")
    ax.text(2, 92, "Frequenze intrinseche: più si scende, più lento è il pacemaker di riserva.", fontsize=6)
    save(fig, "SCH-CONDUZ", "Sistema di conduzione (schema a blocchi)",
         "Sequenza di attivazione dal nodo del seno alle fibre di Purkinje, con onde/intervalli corrispondenti e frequenze dei pacemaker di riserva.",
         ["frequenze intrinseche (seno 60–100, giunzione 40–60, ventricoli 20–40)", "corrispondenza P / PR / QRS"], w)


# ------------------------------------------------------------------ Einthoven ed esassiale
def einthoven():
    w = 140
    fig, (a, b) = plt.subplots(1, 2, figsize=(w * MM, 72 * MM))
    fig.subplots_adjust(left=0.02, right=0.98, bottom=0.03, top=0.92, wspace=0.08)
    # triangolo: braccio destro (RA) in alto a sinistra, braccio sinistro (LA) in alto a destra, gamba (LL) in basso
    RA, LA, LL = np.array([-1, 0.6]), np.array([1, 0.6]), np.array([0, -1.13])
    a.add_patch(Polygon([RA, LA, LL], closed=True, fill=False, lw=1.5, ec="black"))
    for p, s in [(RA, "braccio\ndestro (−)"), (LA, "braccio\nsinistro"), (LL, "gamba\nsinistra (+)")]:
        a.add_patch(Circle(p, 0.06, fc="black"))
    a.text(-1.08, 0.75, "RA", ha="center", fontsize=8, fontweight="bold")
    a.text(1.08, 0.75, "LA", ha="center", fontsize=8, fontweight="bold")
    a.text(0, -1.33, "LL", ha="center", fontsize=8, fontweight="bold")
    a.text(0, 0.72, "I:  RA (−) → LA (+)", ha="center", fontsize=6.5)
    a.text(-0.95, -0.45, "II:\nRA (−) →\nLL (+)", ha="center", fontsize=6.5)
    a.text(0.95, -0.45, "III:\nLA (−) →\nLL (+)", ha="center", fontsize=6.5)
    a.text(0, -0.05, "II = I + III", ha="center", fontsize=7.5, fontweight="bold")
    a.set_xlim(-1.4, 1.4)
    a.set_ylim(-1.5, 1.05)
    a.set_aspect("equal")
    a.axis("off")
    a.set_title("Triangolo di Einthoven", fontsize=8, fontweight="bold")
    # sistema esassiale: 0° a destra (sinistra del paziente), +90° in basso
    leads = [("I", 0), ("II", 60), ("III", 120), ("aVR", -150), ("aVL", -30), ("aVF", 90)]
    b.add_patch(Circle((0, 0), 1.0, fill=False, lw=LW_THIN, ec=G_MID))
    for name, ang in leads:
        r = math.radians(ang)
        dx, dy = math.cos(r), -math.sin(r)
        b.plot([-dx, dx], [-dy, dy], color=G_DARK, lw=LW_THIN, ls=(0, (3, 2)))
        b.annotate("", xy=(dx, dy), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=1.2, color="black",
                                                                     mutation_scale=8))
        b.text(1.2 * dx, 1.2 * dy, f"{name}\n{'+' if ang > 0 else ''}{ang}°", ha="center", va="center", fontsize=6.5)
    # quadrante normale
    th = np.radians(np.linspace(-30, 90, 60))
    b.fill(np.r_[0, 0.55 * np.cos(th)], np.r_[0, -0.55 * np.sin(th)], color=G_LIGHT, lw=0)
    b.text(0.3, -0.2, "asse\nnormale\n−30°/+90°", ha="center", va="center", fontsize=5.8)
    b.text(-1.3, 0.0, "±180°", ha="center", va="center", fontsize=6.5)
    b.set_xlim(-1.5, 1.5)
    b.set_ylim(-1.45, 1.45)
    b.set_aspect("equal")
    b.axis("off")
    b.set_title("Sistema esassiale (piano frontale)", fontsize=8, fontweight="bold")
    save(fig, "SCH-EINTH", "Triangolo di Einthoven e sistema esassiale",
         "Derivazioni bipolari I, II, III sul triangolo di Einthoven (II = I + III) e sistema esassiale con le sei derivazioni periferiche e l'intervallo dell'asse normale.",
         ["polarità delle derivazioni", "angoli: I 0°, II +60°, III +120°, aVF +90°, aVL −30°, aVR −150°", "asse normale −30°/+90°"], w)


# ------------------------------------------------------------------ elettrodi precordiali
def precordiali():
    w = 100
    fig, ax = plt.subplots(figsize=(w * MM, 95 * MM))
    fig.subplots_adjust(0.02, 0.02, 0.98, 0.98)
    ax.set_xlim(-60, 60)
    ax.set_ylim(-62, 52)
    ax.set_aspect("equal")
    ax.axis("off")
    # profilo schematico del torace (contorno geometrico, non anatomico)
    th = np.linspace(0, 2 * math.pi, 200)
    ax.plot(48 * np.cos(th), 8 + 52 * np.sin(th) * (np.sin(th) < 0) + 40 * np.sin(th) * (np.sin(th) >= 0),
            color=G_DARK, lw=LW)
    # sterno
    ax.add_patch(Rectangle((-4, -30), 8, 72, fc=G_LIGHT, ec="black", lw=LW_THIN))
    ax.text(0, 44.5, "sterno", ha="center", fontsize=6)
    # spazi intercostali (II–VI) come linee orizzontali numerate
    ys = {2: 30, 3: 19, 4: 8, 5: -4, 6: -16}
    for k, y in ys.items():
        ax.plot([-44, -5], [y, y], color=G_MID, lw=LW_THIN)
        ax.plot([5, 46], [y, y], color=G_MID, lw=LW_THIN)
        ax.text(-50, y, f"{k}° sic", ha="right", va="center", fontsize=5.5)
    # linee di repere verticali
    for x, s in [(-24, "emiclaveare\ndx"), (22, "emiclaveare\nsx"), (34, "ascellare\nanteriore"), (45, "ascellare\nmedia")]:
        ax.plot([x, x], [-40, 40], color="black", lw=LW_THIN, ls=(0, (3, 2)))
        ax.text(x + 1.2, -38, s.replace("\n", " "), ha="left", va="bottom", fontsize=5.2, rotation=90)
    pos = {"V1": (-7, 8), "V2": (7, 8), "V3": (14.5, 2), "V4": (22, -4), "V5": (34, -4), "V6": (45, -4)}
    for k, (x, y) in pos.items():
        ax.add_patch(Circle((x, y), 2.6, fc="black"))
        ax.text(x, y + 4.2, k, ha="center", fontsize=7, fontweight="bold")
    ax.text(-58, -58, "V1: 4° spazio a destra dello sterno · V2: 4° spazio a sinistra · V4: 5° spazio, emiclaveare\n"
                      "V3: a metà tra V2 e V4 · V5: ascellare anteriore, livello di V4 · V6: ascellare media, livello di V4",
            fontsize=5.5, ha="left", va="bottom")
    save(fig, "SCH-PRECORD", "Posizione degli elettrodi precordiali",
         "Schema geometrico del torace con spazi intercostali e linee di repere; posizione di V1–V6.",
         ["V1–V2 al 4° spazio intercostale ai lati dello sterno", "V4 al 5° spazio sull'emiclaveare", "V5–V6 allo stesso livello orizzontale di V4"], w)


# ------------------------------------------------------------------ territori coronarici
def territori():
    w = 140
    fig, ax = plt.subplots(figsize=(w * MM, 70 * MM))
    fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
    ax.set_xlim(0, 140)
    ax.set_ylim(0, 70)
    ax.axis("off")
    grid = [["I", "aVR", "V1", "V4"], ["II", "aVL", "V2", "V5"], ["III", "aVF", "V3", "V6"]]
    terr = {"I": "lat", "aVL": "lat", "V5": "lat", "V6": "lat", "II": "inf", "III": "inf", "aVF": "inf",
            "V1": "sett", "V2": "sett", "V3": "ant", "V4": "ant", "aVR": None}
    style = {"lat": dict(fc="white", hatch="////"), "inf": dict(fc=G_MID, hatch=None),
             "sett": dict(fc=G_LIGHT, hatch=None), "ant": dict(fc="white", hatch="....")}
    cw, ch = 32, 15
    for r, row in enumerate(grid):
        for c, ld in enumerate(row):
            x, y = 3 + c * (cw + 2), 53 - r * (ch + 2)
            t = terr[ld]
            st = style.get(t, dict(fc="white", hatch=None))
            ax.add_patch(Rectangle((x, y), cw, ch, lw=LW, ec="black", **st))
            ax.text(x + cw / 2, y + ch / 2, ld, ha="center", va="center", fontsize=10, fontweight="bold",
                    bbox=dict(fc="white", ec="none", pad=1.2))
    leg = [("inf", "Inferiore – II, III, aVF – coronaria destra (o circonflessa)"),
           ("sett", "Settale – V1, V2 – discendente anteriore"),
           ("ant", "Anteriore – V3, V4 – discendente anteriore"),
           ("lat", "Laterale – I, aVL, V5, V6 – circonflessa / diagonale")]
    for i, (k, s) in enumerate(leg):
        x, y = 3 + (i % 2) * 70, 9 - (i // 2) * 7.5
        ax.add_patch(Rectangle((x, y), 7, 5, lw=LW_THIN, ec="black", **style[k]))
        ax.text(x + 9, y + 2.5, s, va="center", fontsize=6)
    save(fig, "SCH-TERRIT", "Territori coronarici sullo schema delle 12 derivazioni",
         "Le 12 derivazioni nella disposizione 3×4 raggruppate per territorio (inferiore, settale, anteriore, laterale) con l'arteria più spesso coinvolta; aVR esclusa.",
         ["raggruppamento delle derivazioni contigue", "arterie indicate come «più spesso», non in modo assoluto", "aVR non assegnata"], w)


if __name__ == "__main__":
    pa_ventricolare()
    pa_nodo_seno()
    wiggers()
    conduzione()
    einthoven()
    precordiali()
    territori()
