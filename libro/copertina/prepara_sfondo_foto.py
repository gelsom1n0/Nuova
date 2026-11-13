#!/usr/bin/env python3
"""
Stadio A della copertina «foto» (illustrazione fornita dall'utente).

Prende l'illustrazione ingrandita (sorgenti_immagine/base_upscale_4k.png,
4096 x 3021 px = ~327 dpi su 9,25 in) e produce:

  sorgenti_immagine/sfondo_pulito.png   illustrazione senza alcun testo raster
  sorgenti_immagine/caduceo.png         caduceo ritagliato (RGBA) per il dorso
  sorgenti_immagine/maschera_testo.png  maschera usata (controllo visivo)

Il testo raster viene tolto SOLO dove c'è testo: la maschera è calcolata sui
pixel chiari/caldi del lettering dentro rettangoli definiti a mano, quindi il
cuore, le molecole, l'ECG e le sfere non vengono toccati né deformati. Tutto
il testo viene poi ricomposto in vettoriale da build_copertina_foto.py.

Non dipende dal numero di pagine: si esegue una volta sola.
"""
from pathlib import Path

import cv2
import numpy as np
from PIL import Image

QUI = Path(__file__).resolve().parent
SRC = QUI / "sorgenti_immagine"
S = 4.0  # fattore originale 1024 px -> 4096 px

# Rettangoli di testo in coordinate dell'immagine originale 1024 x 755 px:
# (x0, y0, x1, y1, tipo). "chiaro" = testo avorio/oro su fondo navy.
TESTI = [
    # "pieno": nel rettangolo c'è solo fondo + testo -> ricostruzione completa
    # "glifi": vicino a molecole -> solo lettering e sua ombra
    # quarta di copertina
    (52, 72, 474, 399, "pieno"),     # etichetta, titolo, presentazione, elenco, avvertenza (si ferma prima dello smusso del dorso)
    (472, 140, 502, 399, "chiari"),  # lettere tagliate dal dorso, su ombra e smusso: solo pixel del lettering
    (52, 430, 378, 498, "pieno"),    # formula ClCr (errata: "age", "weight", "if female")
    (71, 586, 324, 672, "pieno"),    # formula pH
    # prima di copertina
    (560, 54, 1024, 310, "pieno"),   # etichetta, titolo, divisore, sottotitolo
    (554, 318, 702, 369, "pieno"),   # formula ClCr (si ferma prima della vena cava)
    (700, 318, 736, 339, "pieno"),   # "ght": sopra il bordo del vaso (che inizia a y≈341)
    (700, 339, 717, 349, "pieno"),   # linea di frazione, fino a 2 px dal vaso
    (717, 339, 736, 342, "caldi"),   # fascia a contatto col vaso: solo pixel caldi
    (858, 324, 1012, 381, "pieno"),  # formula pH
    (566, 624, 674, 685, "pieno"),   # formula Vd
    (898, 618, 986, 627, "glifi"),   # formula Cl, parte alta (adiacente alla molecola)
    (899, 625, 986, 682, "pieno"),   # formula Cl, resto
    (403, 412, 412, 432, "pieno"),   # quarta: "I" allucinata nella sfera Na tenue
    (676, 688, 864, 724, "pieno"),   # edizione
]

# Sfere con etichetta sbagliata/allucinata dall'upscaler: (cx, cy, r) originali.
SFERE_DA_CORREGGERE = [  # (cx, cy, r, soglia sopra la mediana del vetro)
    (830, 340, 16, 14),   # "Na♪"  -> Na+
    (989, 460, 14, 14),   # "Caᵃ⁺" -> Ca2+
    (395, 422, 16, 5),    # quarta, "Na|" tenue -> Na+
    (195, 694, 18, 5),    # quarta, "Na⁺" deformato -> Na+
]

# Dorso dell'illustrazione (px dell'immagine 4K): interno piatto e smussi.
DORSO_ART = (1985, 2128)


def maschera_testo(img: np.ndarray) -> np.ndarray:
    """Pixel di testo: luminosi e non dominati dal blu (il navy e i vasi blu del
    cuore hanno B > R; il lettering avorio/oro ha R >= B)."""
    f = img.astype(np.int16)
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    lum = (r + g + b) / 3
    return ((lum > 62) & (r >= b - 12)).astype(np.uint8)


def main():
    img = np.asarray(Image.open(SRC / "base_upscale_4k.png").convert("RGB")).copy()
    H, W = img.shape[:2]
    testo = maschera_testo(img)
    mask = np.zeros((H, W), np.uint8)

    pieno = np.zeros((H, W), np.uint8)
    lum_all = img.astype(np.int16).mean(axis=2)
    for x0, y0, x1, y1, tipo in TESTI:
        X0, Y0, X1, Y1 = (int(round(v * S)) for v in (x0, y0, x1, y1))
        if tipo == "pieno":
            pieno[Y0:Y1, X0:X1] = 1
            continue
        # glifi chiari + ombra scura del lettering (più scura del fondo locale)
        zona = lum_all[Y0:Y1, X0:X1]
        fondo = cv2.medianBlur(zona.clip(0, 255).astype(np.uint8), 31).astype(np.int16)
        chiari = testo[Y0:Y1, X0:X1].astype(bool)
        if tipo == "chiari":
            # soglia relativa al fondo locale: prende anche l'antialias più tenue
            z = img[Y0:Y1, X0:X1].astype(np.int16)
            rel = (zona > fondo + 9) & (z[..., 0] >= z[..., 2] - 25)
            vicino = cv2.dilate((chiari | rel).astype(np.uint8), np.ones((21, 21), np.uint8)).astype(bool)
            ombra = (zona < fondo - 4) & vicino
            mask[Y0:Y1, X0:X1] |= cv2.dilate((chiari | rel | ombra).astype(np.uint8), np.ones((9, 9), np.uint8))
            continue
        if tipo == "caldi":
            # accanto al cuore: solo lettering beige (R nettamente > B), niente ombre,
            # così i riflessi lavanda del vaso non entrano nella maschera
            z = img[Y0:Y1, X0:X1].astype(np.int16)
            calde = (z[..., 0] - z[..., 2] > 10) & (zona > 70)
            mask[Y0:Y1, X0:X1] |= cv2.dilate(calde.astype(np.uint8), np.ones((5, 5), np.uint8))
            continue
        ombre = (zona < fondo - 3) & cv2.dilate(chiari.astype(np.uint8), np.ones((21, 21), np.uint8)).astype(bool)
        mask[Y0:Y1, X0:X1] |= (chiari | ombre).astype(np.uint8)

    # sfere: solo i glifi (più chiari del vetro) dentro il 72 % del raggio
    f = img.astype(np.int16).mean(axis=2)
    yy, xx = np.mgrid[0:H, 0:W]
    for cx, cy, r, delta in SFERE_DA_CORREGGERE:
        CX, CY, R = cx * S, cy * S, r * S
        y0, y1, x0, x1 = int(CY - R), int(CY + R), int(CX - R), int(CX + R)
        disco = ((xx[y0:y1, x0:x1] - CX) ** 2 + (yy[y0:y1, x0:x1] - CY) ** 2) < (0.72 * R) ** 2
        zona = f[y0:y1, x0:x1]
        soglia = np.median(zona[disco]) + delta
        mask[y0:y1, x0:x1] |= (disco & (zona > soglia)).astype(np.uint8)

    # dilatazione: copre l'antialias e l'alone del lettering
    mask = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11)))

    # --- dorso dell'illustrazione: testo e caduceo via, interno a tinta piatta ---
    a0, a1 = DORSO_ART
    # caduceo (in alto e in basso) estratto prima di ripulire
    cad = estrai_caduceo(img, 250, 440)
    Image.fromarray(cad, "RGBA").save(SRC / "caduceo.png")
    # colore di riga del dorso: mediana dell'interno piatto, esclusi i pixel chiari
    interno = img[:, 2012:2100].astype(np.float32)
    navy = (interno[..., 2] - interno[..., 0]) > 30  # esclude oro/avorio del lettering e del caduceo
    righe = np.zeros((H, 3), np.float32)
    for y in range(H):
        sel = interno[y][navy[y]]
        righe[y] = np.median(sel, axis=0) if len(sel) > 8 else righe[y - 1]
    righe = cv2.GaussianBlur(righe.reshape(H, 1, 3), (1, 121), 0).reshape(H, 3)
    np.save(SRC / "colore_dorso_righe.npy", righe)
    img[:, 2004:2110] = righe[:, None, :].astype(np.uint8)
    # residui di caduceo/testo sugli smussi del dorso
    sm = np.zeros((H, W), np.uint8)
    sm[:, a0:a1] = testo[:, a0:a1]
    sm[:, 2004:2110] = 0
    sm = cv2.dilate(sm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
    mask |= sm

    # residui del caduceo sugli smussi: tutto ciò che è "dorato" vicino al dorso
    for cy0, cy1 in ((240, 450), (2560, 2800)):
        z = img[cy0:cy1, 1950:2160].astype(np.int16)
        oro = ((z[..., 0] - z[..., 2]) > -8) & (z.mean(axis=2) > 28)
        mask[cy0:cy1, 1950:2160] |= cv2.dilate(oro.astype(np.uint8), np.ones((9, 9), np.uint8))

    # le aree "piene" entrano nella maschera già qui: così l'inpainting delle
    # zone vicine non preleva pixel del vecchio testo
    out = cv2.inpaint(img, (mask | pieno) * 255, 7, cv2.INPAINT_TELEA)
    out = riempi_pieni(out, pieno)
    # banda d'ombra e smusso del dorso lato quarta (x 472-502, y 140-399): l'ombra
    # originale varia solo in orizzontale, quindi ogni colonna viene ricostruita
    # interpolando in verticale tra le righe intatte sopra e sotto il testo
    xa, xb, ya, yb = 472 * 4, 502 * 4, 140 * 4, 399 * 4
    sopra = out[ya - 40:ya - 4, xa:xb].astype(np.float32).mean(axis=0)
    sotto = out[yb + 4:yb + 40, xa:xb].astype(np.float32).mean(axis=0)
    t = np.linspace(0, 1, yb - ya, dtype=np.float32)[:, None, None]
    rumore = np.random.default_rng(5).normal(0, 2.0, (yb - ya, xb - xa, 1)).astype(np.float32)
    out[ya:yb, xa:xb] = (sopra * (1 - t) + sotto * t + rumore).clip(0, 255).astype(np.uint8)

    # ombra residua di "ght" a contatto con la vena cava: copia del fondo già
    # pulito (riga sopra), solo sui pixel scuri; il vaso (chiaro) resta intatto
    y0, y1, x0, x1 = 334 * 4, 344 * 4, 714 * 4, 740 * 4
    zona = out[y0:y1, x0:x1].astype(np.int16).mean(axis=2)
    fonte = out[y0 - 12:y0 - 8, x0:x1].astype(np.float32).mean(axis=0)  # fondo pulito poco sopra
    sel = zona < 90
    blocco = out[y0:y1, x0:x1].astype(np.float32)
    rumore = np.random.default_rng(3).normal(0, 2.2, blocco.shape[:2])[..., None]
    blocco[sel] = (np.broadcast_to(fonte, blocco.shape) + rumore)[sel]
    out[y0:y1, x0:x1] = blocco.astype(np.uint8)
    mask |= pieno
    Image.fromarray(out).save(SRC / "sfondo_pulito.png", optimize=True)
    Image.fromarray(mask * 255).save(SRC / "maschera_testo.png", optimize=True)
    print("maschera:", round(mask.mean() * 100, 2), "% dei pixel; output", out.shape)


def riempi_pieni(img: np.ndarray, pieno: np.ndarray) -> np.ndarray:
    """Ricostruisce i rettangoli 'pieni' con un riempimento armonico (soluzione
    dell'equazione di Laplace con i bordi come condizione): il risultato è la
    sfumatura più liscia compatibile con il fondo circostante, senza macchie.
    Calcolo a 1/8 di risoluzione, ingrandimento bicubico, poi grana uguale a
    quella del fondo, così le zone ricostruite non risultano 'lisce'."""
    H, W = pieno.shape
    k = 8
    small = cv2.resize(img, (W // k, H // k), interpolation=cv2.INTER_AREA).astype(np.float32)
    ms = cv2.resize(pieno, (W // k, H // k), interpolation=cv2.INTER_NEAREST)
    ms = cv2.dilate(ms, np.ones((3, 3), np.uint8)).astype(bool)
    # oggetti chiari (atomi, sfere) a ridosso del bordo: non devono fare da
    # condizione al contorno, altrimenti "illuminano" il riempimento. Entrano nel
    # calcolo come incognite; nell'immagine finale restano comunque originali,
    # perché la fusione avviene solo dentro i rettangoli "pieni".
    chiari = cv2.cvtColor(small.astype(np.uint8), cv2.COLOR_RGB2GRAY) > 70
    vicini = cv2.dilate(ms.astype(np.uint8), np.ones((9, 9), np.uint8)).astype(bool)
    ms = ms | (chiari & vicini)
    f = cv2.inpaint(small.astype(np.uint8), ms.astype(np.uint8) * 255, 5, cv2.INPAINT_TELEA).astype(np.float32)
    kern = np.array([[0, .25, 0], [.25, 0, .25], [0, .25, 0]], np.float32)
    for _ in range(4000):  # Jacobi: converge alla soluzione armonica
        f[ms] = cv2.filter2D(f, -1, kern, borderType=cv2.BORDER_REPLICATE)[ms]
    up = cv2.resize(f, (W, H), interpolation=cv2.INTER_CUBIC)
    up = cv2.GaussianBlur(up, (0, 0), 4)
    hf = img.astype(np.float32) - cv2.GaussianBlur(img.astype(np.float32), (0, 0), 3)
    sigma = float(np.std(hf[(pieno == 0) & (img.mean(axis=2) < 50)]))
    rng = np.random.default_rng(7)
    grana = cv2.GaussianBlur(rng.normal(0, sigma, (H, W)).astype(np.float32), (0, 0), 0.8) * 1.4
    out = img.astype(np.float32)
    m = cv2.GaussianBlur(pieno.astype(np.float32), (0, 0), 3)[..., None]
    out = out * (1 - m) + (up + grana[..., None]) * m
    return out.clip(0, 255).astype(np.uint8)


def estrai_caduceo(img: np.ndarray, y0: int, y1: int) -> np.ndarray:
    """Ritaglia il caduceo dorato dal dorso originale e ne ricava un canale
    alfa dalla 'doratura' (R - B), così da poterlo ricomporre su un fondo
    piatto senza alone del vecchio sfondo."""
    crop = img[y0:y1, 1970:2140].astype(np.int16)
    oro = np.clip((crop[..., 0] - crop[..., 2] - 8) * 6, 0, 255).astype(np.uint8)
    ys, xs = np.where(oro > 40)
    yb0, yb1, xb0, xb1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    rgba = np.dstack([crop[..., :3].clip(0, 255).astype(np.uint8), oro])[yb0:yb1, xb0:xb1]
    return rgba


if __name__ == "__main__":
    main()
