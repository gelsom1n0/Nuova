#!/usr/bin/env python3
"""
Build del Volume A «ABC della cardiologia clinica» – KDP 7 × 10 in, interno in bianco e nero.

Uso
  python3 libro/volume-A/engine/build_A.py <cartella-sorgenti> [--out nome.pdf] [--bozza]
  (es. la prova: python3 libro/volume-A/engine/build_A.py libro/volume-A/engine/prova)

Sorgenti (nella cartella indicata)
  meta.json                titolo, sottotitolo, edizione, file, copyright_html
  parte-00-*.md            «Parte 0»: pagine preliminari (numeri romani). Ogni '#' apre una pagina.
  parte-NN-*.md            Parti numerate: NN è il numero della Parte (01–12…)

Convenzioni Markdown (oltre al Markdown standard con tabelle)
  # Titolo                         -> «Parte NN» su pagina nuova (numero dal nome del file)
  ## Titolo                        -> sezione NN.M (numerazione automatica)
  ### Metoprololo {.pa}            -> scheda: voce principale (in grassetto) nell'indice dei farmaci
  ### Fibrillazione atriale {.ix}  -> voce principale nell'indice di aritmie e termini ECG
  [metoprololo]{.pa}               -> occorrenza nel testo indicizzata (farmaci)
  [flutter atriale]{.ix}           -> occorrenza indicizzata (aritmie/termini ECG)
  [β-bloccante]{.pa voce="Beta-bloccanti"}  -> occorrenza indicizzata sotto un'altra voce
  !!! tipo "Titolo"                -> riquadro (corpo indentato di 4 spazi). Tipi:
        nota (Nota clinica) · chiave (Regola/Mnemonico) · allarme · errore (Errore classico) ·
        autotest (righe per la risposta: '{{righe:N}}' dove servono; se assente, 3 righe in fondo) ·
        sbar (Cosa dico al medico: elenco «- S: …», «- B: …», «- A: …», «- R: …») ·
        rischio (Farmaco ad alto rischio) · focus (Cardiochirurgia e PS) · obiettivi
      Senza titolo si usa quello predefinito del tipo.
  ::: fig ID [larghezza=intera|mezza|mezza-sx|pagina] [variante=3x4] [file=percorso] [fonte="…"]
  Didascalia in Markdown (una o più righe).
  :::                              -> figura numerata «Fig. N.k»; file, tipo e fonte letti da
                                      figure/MANIFEST.csv tramite l'ID (sovrascrivibili)
  ::: ecg-esercizio ID
  Domanda…
  ---
  Soluzione…
  :::                              -> esercizio con tracciato; la soluzione va in fondo alla Parte
  [[fig:ID]]                       -> rimando «Fig. N.k»   ·   [[es:ID]] -> «Esercizio N.k»

Passaggi
  1. Markdown -> HTML per Parte, numerazioni, didascalie, indici (ancore).
  2. Primo rendering: lettura delle pagine delle ancore; galleggiamento delle figure (se una figura
     finisce in cima alla pagina lasciando un vuoto in fondo alla precedente, viene spostata dopo
     uno o più blocchi successivi della stessa sezione; massimo 3 blocchi; fino a 4 iterazioni).
  3. Rendering finale con numeri di pagina reali in indice generale e indice analitico.
  Report: <out>/build_report.json (figure usate e loro pagina/stato di validazione, spostamenti).
"""
from __future__ import annotations

import csv
import html
import json
import re
import shlex
import sys
import unicodedata
from pathlib import Path

import markdown
from weasyprint import CSS, HTML
from weasyprint.text.fonts import FontConfiguration

ENGINE = Path(__file__).resolve().parent
VOLUME = ENGINE.parent
FIGDIR = VOLUME / "figure"
GABBIA_MM = 143.5  # larghezza della gabbia di testo (5,65 in)

TITOLI_RIQUADRI = {
    "nota": "Nota clinica", "chiave": "Regola", "allarme": "Allarme", "errore": "Errore classico",
    "autotest": "Autotest", "sbar": "Cosa dico al medico", "rischio": "Farmaco ad alto rischio",
    "focus": "Focus cardiochirurgia e pronto soccorso", "obiettivi": "In questa parte",
}
SBAR = {"S": "Situazione", "B": "Background", "A": "Valutazione", "R": "Richiesta"}
ETICHETTA_TIPO = {"simulato": "Tracciato didattico simulato", "schema": "Schema originale",
                  "reale": "Tracciato reale"}


# ------------------------------------------------------------------ utilità
def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()


def sortkey(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c) and (c.isalnum() or c == " "))


def md2html(text):
    m = markdown.Markdown(extensions=["tables", "admonition", "attr_list", "sane_lists", "toc", "md_in_html"])
    return m.convert(text)


def load_manifest():
    p = FIGDIR / "MANIFEST.csv"
    if not p.exists():
        return {}
    with p.open(encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def svg_width_mm(path: Path):
    """Larghezza intrinseca di un SVG (pt o mm) in mm; None se non determinabile."""
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:2000]
    except OSError:
        return None
    m = re.search(r'<svg[^>]*\swidth="([\d.]+)(pt|mm|px|in)?"', head)
    if not m:
        return None
    v, u = float(m.group(1)), m.group(2) or "px"
    return {"pt": v * 25.4 / 72, "mm": v, "in": v * 25.4, "px": v * 25.4 / 96}[u]


# ------------------------------------------------------------------ stato della build
class Stato:
    def __init__(self, bozza=False):
        self.manifest = load_manifest()
        self.bozza = bozza
        self.toc = []          # (tipo, etichetta, ancora, numero)
        self.voci = []         # (indice 'pa'|'ix', voce, ancora, principale)
        self.figure = {}       # ID -> {"num", "anchor", "parte", "stato", "file"}
        self.esercizi = {}     # ID -> "N.k"
        self.avvisi = []
        self.n_ix = 0


# ------------------------------------------------------------------ preprocessori Markdown
FIG_RE = re.compile(r"^::: *(fig|ecg-esercizio) +(\S+)(.*?)\n(.*?)\n:::[ \t]*$", re.M | re.S)
IX_RE = re.compile(r"\[([^\]\n]+)\]\{\.(pa|ix)((?:\s+[a-z]+=\"[^\"]*\")*)\s*\}")


def opts(s):
    out = {}
    for tok in shlex.split(s or ""):
        if "=" in tok:
            k, v = tok.split("=", 1)
            out[k] = v
    return out


def figure_html(st: Stato, parte: int, fid: str, o: dict, caption_md: str, kind="fig"):
    """Costruisce l'HTML di una figura numerata, con didascalia ed etichetta di provenienza."""
    k = sum(1 for f in st.figure.values() if f["parte"] == parte) + 1
    num = f"{parte}.{k}"
    anchor = "fig-" + re.sub(r"[^A-Za-z0-9_-]", "-", fid)
    if fid in st.figure:
        anchor += f"-{k}"
    row = st.manifest.get(fid, {})
    rel = o.get("file") or row.get("file", "")
    if o.get("variante") and rel:
        rel = re.sub(r"(\.[a-z]+)$", f"_{o['variante']}\\1", rel)
    path = (FIGDIR / rel) if rel else None
    tipo = o.get("tipo") or row.get("tipo", "")
    fonte = o.get("fonte") or row.get("fonte_licenza", "")
    stato = row.get("stato_validazione", "non nel manifest")
    if not row:
        st.avvisi.append(f"Fig. {num}: ID {fid} assente da MANIFEST.csv")
    if path is None or not path.exists():
        st.avvisi.append(f"Fig. {num}: file mancante ({rel or 'nessun file'})")
    larg = o.get("larghezza", "intera")
    cls = {"intera": "", "mezza": " mezza", "mezza-sx": " mezza sinistra", "pagina": " pagina"}.get(larg, "")
    avail = GABBIA_MM * (0.48 if larg.startswith("mezza") else 1.0)
    scala_txt = ""
    w = svg_width_mm(path) if path and path.suffix == ".svg" else None
    if w and tipo in ("simulato", "reale"):
        sc = min(1.0, avail / w)
        try:
            sc *= float(row.get("scala") or 1.0)
        except ValueError:
            pass
        scala_txt = "25 mm/s, 10 mm/mV" if sc > 0.985 else f"griglia ridotta al {round(sc * 100)} % (quadretto piccolo = 0,04 s × 0,1 mV)"
    src = ETICHETTA_TIPO.get(tipo, "")
    if tipo == "reale" and fonte:
        src = f"{src} – {fonte}"
    elif tipo == "simulato":
        src = f"{src} ({fid})"
    if scala_txt:
        src = f"{src}. {scala_txt}." if src else scala_txt
    if st.bozza and stato != "validato":
        src += f" [{stato.upper()}]"
    st.figure[fid if fid not in st.figure else f"{fid}#{k}"] = {
        "num": num, "anchor": anchor, "parte": parte, "stato": stato, "file": rel, "tipo": tipo}
    cap = md2html(caption_md.strip()) if caption_md.strip() else ""
    cap = re.sub(r"^<p>(.*)</p>$", r"\1", cap.strip(), flags=re.S)
    img = f'<img src="{path.as_uri()}" alt="{html.escape(fid)}">' if path and path.exists() else \
        f'<div style="border:0.75pt dashed #000;padding:20pt">FIGURA MANCANTE: {html.escape(fid)}</div>'
    return (f'<figure class="fig{cls}" id="{anchor}" data-fig="{html.escape(fid)}">{img}'
            f'<figcaption><span class="fnum">Fig. {num}</span>{cap}'
            f'{f"<span class=fsrc>{html.escape(src)}</span>" if src else ""}</figcaption></figure>'), num


def preprocess(text: str, st: Stato, parte: int, soluzioni: list):
    """Sostituisce blocchi figura/esercizio e marcature di indice con HTML grezzo."""
    es_k = [0]

    def blk(m):
        kind, fid, rest, body = m.group(1), m.group(2), m.group(3), m.group(4)
        o = opts(rest)
        if kind == "fig":
            h, _ = figure_html(st, parte, fid, o, body)
            return "\n\n" + h + "\n\n"
        es_k[0] += 1
        n = f"{parte}.{es_k[0]}"
        eid = o.get("id", f"es-{parte}-{es_k[0]}")
        st.esercizi[eid] = n
        st.esercizi.setdefault(fid, n)
        dom, _, sol = body.partition("\n---\n")
        h, fnum = figure_html(st, parte, fid, o, f"Esercizio {n}.", kind="es")
        soluzioni.append((n, sol.strip(), eid))
        return (f'\n\n<div class="ecg-esercizio" id="{eid}" markdown="1">\n'
                f'<div class="es-titolo">Esercizio ECG {n}</div>\n\n{h}\n\n{dom.strip()}\n\n'
                f'<div class="es-rimando">Soluzione a fine Parte {parte}</div>\n</div>\n\n')

    text = FIG_RE.sub(blk, text)

    def ix(m):
        st.n_ix += 1
        aid = f"ix{st.n_ix}"
        o = opts(m.group(3))
        voce = o.get("voce", m.group(1))
        st.voci.append((m.group(2), voce, aid, False))
        return f'<span class="{m.group(2)}" id="{aid}">{m.group(1)}</span>'

    text = IX_RE.sub(ix, text)
    return text


# ------------------------------------------------------------------ postprocessori HTML
def post_admonitions(h: str):
    def fix(tipo, inner):
        # titolo predefinito se l'autore non l'ha dato (Python-Markdown usa il tipo capitalizzato)
        inner = re.sub(r'<p class="admonition-title">' + re.escape(tipo.capitalize()) + r"</p>",
                       f'<p class="admonition-title">{TITOLI_RIQUADRI.get(tipo, tipo.capitalize())}</p>', inner, count=1)
        if tipo == "autotest":
            if "{{righe" in inner:
                inner = re.sub(r"\{\{righe:(\d+)\}\}",
                               lambda m: '<div class="righe">' + '<div class="riga"></div>' * int(m.group(1)) + "</div>", inner)
            else:
                inner += '<div class="righe">' + '<div class="riga"></div>' * 3 + "</div>"
        if tipo == "sbar":
            items = re.findall(r"<li>\s*(?:<p>)?\s*([SBAR])\s*:\s*(.*?)(?:</p>)?\s*</li>", inner, re.S)
            if items:
                rows = "".join(f'<tr><td class="sbar-k"><span class="lettera">{k}</span>{SBAR[k]}</td><td>{v}</td></tr>'
                               for k, v in items)
                inner = re.sub(r"<ul>.*?</ul>", f'<table class="sbar-t">{rows}</table>', inner, count=1, flags=re.S)
        return f'<div class="admonition {tipo}">{inner}</div>'

    # ricerca bilanciata della chiusura di ogni <div class="admonition …"> (il corpo può contenere div)
    out, pos = [], 0
    for m in re.finditer(r'<div class="admonition ([a-z]+)">', h):
        if m.start() < pos:
            continue
        depth, end = 0, None
        for t in re.finditer(r"<(/?)div\b[^>]*>", h[m.start():]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                end = m.start() + t.end()
                break
        if end is None:
            continue
        inner = h[m.end():end - len("</div>")]
        out.append(h[pos:m.start()])
        out.append(fix(m.group(1), inner))
        pos = end
    out.append(h[pos:])
    return "".join(out)


def number_headings(h: str, st: Stato, parte: int, front: bool):
    sec = [0]

    def head(m):
        lvl, title = m.group(1), m.group(3)
        if front:
            if lvl == "1":
                aid = f"pre{len(st.toc)}"
                st.toc.append(("front", plain(title), aid, ""))
                return f'<h1 class="prelim" id="{aid}">{title}</h1>'
            return f'<h2 class="prelim-sec">{title}</h2>'
        if lvl == "1":
            pid = f"p{parte}"
            st.toc.append(("part", plain(title), pid, str(parte)))
            label = re.sub(r"[\"'\\]", "", plain(title))
            return (f'<h1 class="part" id="{pid}" style="string-set: partname \'Parte {parte} — {label}\'">'
                    f'<span class="plabel">Parte {parte}</span><span class="ptitle">{title}</span></h1>')
        sec[0] += 1
        num = f"{parte}.{sec[0]}"
        sid = f"s{parte}_{sec[0]}"
        st.toc.append(("sec", plain(title), sid, num))
        return f'<h2 class="sezione" id="{sid}"><span class="snum">{num}</span>{title}</h2>'

    h = re.sub(r'<h([12]) id="([^"]*)">(.*?)</h\1>', head, h)

    def h3(m):
        attrs, title = m.group(1), m.group(2)
        for kind in ("pa", "ix"):
            if re.search(rf'class="[^"]*\b{kind}\b', attrs):
                idm = re.search(r'id="([^"]*)"', attrs)
                if idm:
                    st.voci.append((kind, plain(title), idm.group(1), True))
        return m.group(0)

    re.sub(r"<h3([^>]*)>(.*?)</h3>", h3, h)
    return h


def soluzioni_html(sol, parte):
    if not sol:
        return ""
    out = [f'<div class="soluzioni"><h2>Soluzioni degli esercizi ECG – Parte {parte}</h2>']
    for n, txt, eid in sol:
        body = re.sub(r"^<p>(.*)</p>$", r"\1", md2html(txt).strip(), flags=re.S)
        out.append(f'<div class="sol"><b>Esercizio {n}.</b>{body}</div>')
    out.append("</div>")
    return "".join(out)


def crossrefs(h: str, st: Stato):
    def r(m):
        kind, ref = m.group(1), m.group(2)
        if kind == "fig":
            f = st.figure.get(ref)
            if not f:
                st.avvisi.append(f"rimando a figura inesistente: {ref}")
                return f"Fig. ??"
            return f'<a href="#{f["anchor"]}">Fig. {f["num"]}</a>'
        n = st.esercizi.get(ref)
        if not n:
            st.avvisi.append(f"rimando a esercizio inesistente: {ref}")
        return f"Esercizio {n or '??'}"
    return re.sub(r"\[\[(fig|es):([^\]]+)\]\]", r, h)


# ------------------------------------------------------------------ blocchi di primo livello
VOID = {"img", "br", "hr", "meta", "input", "col", "source", "wbr"}
TAG_RE = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*?)(/?)>")


def split_blocks(h: str):
    """Divide l'HTML in blocchi di primo livello (paragrafi, tabelle, riquadri, figure…)."""
    blocks, depth, start, pos = [], 0, None, 0
    for m in TAG_RE.finditer(h):
        close, tag, selfclose = m.group(1), m.group(2).lower(), m.group(4)
        if tag in VOID or selfclose:
            if depth == 0:
                blocks.append(h[m.start():m.end()])
            continue
        if not close:
            if depth == 0:
                start = m.start()
            depth += 1
        else:
            depth -= 1
            if depth == 0 and start is not None:
                blocks.append(h[start:m.end()])
                start = None
    return blocks


def tag_blocks(blocks, base):
    out = []
    for i, b in enumerate(blocks):
        out.append(re.sub(r"^<([a-zA-Z0-9]+)", lambda m: f'<{m.group(1)} data-b="{base + i}"', b, count=1))
    return out


# ------------------------------------------------------------------ indici
def make_toc(st: Stato, pg: dict):
    out = ['<div class="toc">']
    for kind, label, hid, n in st.toc:
        p = pg.get(hid, "")
        if kind == "front":
            out.append(f'<div class="tc"><a href="#{hid}"><span class="n"></span><span class="t">{html.escape(label)}</span><span class="pg">{p}</span></a></div>')
        elif kind == "part":
            out.append(f'<div class="tp"><a href="#{hid}"><span class="t">Parte {n} — {html.escape(label)}</span><span class="pg">{p}</span></a></div>')
        else:
            out.append(f'<div class="tc"><a href="#{hid}"><span class="n">{n}</span><span class="t">{html.escape(label)}</span><span class="pg">{p}</span></a></div>')
    if any(k in ("pa", "ix") for k, *_ in st.voci):
        out.append(f'<div class="tp"><a href="#indice-analitico"><span class="t">Indice analitico</span><span class="pg">{pg.get("indice-analitico", "")}</span></a></div>')
    out.append("</div>")
    return "".join(out)


def make_index(st: Stato, pg: dict):
    if not st.voci:
        return ""
    out = ['<h1 class="indice" id="indice-analitico" style="string-set: partname \'Indice analitico\'">Indice analitico</h1>',
           '<div class="ix-index">']
    for kind, titolo in (("pa", "Farmaci"), ("ix", "Aritmie, quadri ECG e termini")):
        voci = {}
        for k, voce, aid, princ in st.voci:
            if k != kind:
                continue
            key = voce.strip()
            key = key[0].upper() + key[1:]
            voci.setdefault(key, {})
            p = pg.get(aid)
            if p is not None:
                voci[key][p] = voci[key].get(p, False) or princ
        if not voci:
            continue
        out.append(f"<h2>{titolo}</h2>")
        cur = ""
        for voce in sorted(voci, key=sortkey):
            L = sortkey(voce)[:1].upper()
            if L != cur:
                out.append(f'<div class="let">{L}</div>')
                cur = L
            pages = ", ".join((f"<b>{p}</b>" if pr else str(p)) for p, pr in sorted(voci[voce].items()))
            out.append(f'<div class="voce"><span class="t">{html.escape(voce)}</span><span class="pgs">{pages}</span></div>')
    out.append("</div>")
    return "".join(out)


# ------------------------------------------------------------------ layout: galleggiamento figure
def layout_info(doc):
    """Per ogni blocco data-b: (pagina, y_top, y_bottom) del primo frammento; riempimento pagine."""
    info, fill = {}, {}
    for pi, page in enumerate(doc.pages):
        pb = page._page_box
        top, h = pb.content_box_y(), pb.height
        bottom = top
        seen = set()
        for b in pb.descendants():
            el = getattr(b, "element", None)
            if el is None:
                continue
            k = el.get("data-b")
            if k is None or (k, pi) in seen:
                continue
            seen.add((k, pi))
            y0, y1 = b.position_y, b.position_y + b.margin_height()
            bottom = max(bottom, y1)
            k = int(k)
            if k not in info:
                fig = el.get("data-fig") or ("esercizio" if "ecg-esercizio" in (el.get("class") or "") else None)
                info[k] = {"page": pi, "y0": y0, "y1": y1, "tag": el.tag, "fig": fig}
            else:
                info[k].setdefault("pages", set()).add(pi)
        fill[pi] = (bottom - top) / h if h else 0
        for k in list(info):
            pass
    return info, fill


def float_figures(blocks, doc, moved_log, max_shift=3, soglia=0.82):
    """Sposta in avanti le figure che, finite in cima alla pagina, lasciano un vuoto nella precedente."""
    info, fill = layout_info(doc)
    by_page = {}
    for k, v in info.items():
        by_page.setdefault(v["page"], []).append(k)
    changed = False
    idx = {int(re.search(r'data-b="(\d+)"', b).group(1)): i for i, b in enumerate(blocks) if 'data-b="' in b[:80]}
    # figure spezzate tra due pagine (succede ai float «mezza»): si anticipano di un blocco
    for k, v in sorted(info.items()):
        if v["fig"] and v.get("pages") and k in idx and idx[k] > 0:
            i = idx[k]
            if re.match(r"<h[12]", blocks[i - 1]):
                continue
            blocks[i - 1], blocks[i] = blocks[i], blocks[i - 1]
            moved_log.append({"figura": v["fig"], "pagina_prima": v["page"] + 1, "blocchi_saltati": -1,
                              "motivo": "figura spezzata tra due pagine"})
            return True
    for k, v in sorted(info.items()):
        if not v["fig"] or "pagina" in blocks[idx[k]][:120]:
            continue
        p = v["page"]
        if p == 0 or min(by_page.get(p, [k])) != k or fill.get(p - 1, 1) >= soglia:
            continue
        i = idx[k]
        prev = blocks[i - 1] if i > 0 else ""
        if re.match(r"<h1", prev) or 'class="soluzioni"' in prev:
            continue
        gap = (1 - fill[p - 1])
        # quanti blocchi successivi spostare prima della figura (non oltre un titolo h1/h2)
        n, acc = 0, 0.0
        for j in range(i + 1, min(len(blocks), i + 1 + max_shift)):
            if re.match(r"<h[12]", blocks[j]) or 'class="soluzioni"' in blocks[j][:80]:
                break
            kb = int(re.search(r'data-b="(\d+)"', blocks[j]).group(1))
            hb = info.get(kb)
            if not hb:
                break
            frac = (hb["y1"] - hb["y0"]) / 648.0  # altezza della gabbia: 9 in = 648 pt circa
            splittable = re.match(r"<(p|ul|ol)\b", blocks[j]) is not None
            if acc + frac <= gap or (n == 0 and splittable):
                n += 1
                acc += frac
                if acc >= gap:
                    break
            else:
                break
        if n:
            fig = blocks.pop(i)
            blocks.insert(i + n, fig)
            moved_log.append({"figura": v["fig"], "pagina_prima": p + 1, "blocchi_saltati": n})
            changed = True
            break  # un solo spostamento per passaggio: il layout cambia a valle
    return changed


# ------------------------------------------------------------------ build
def build(src: Path, outname=None, bozza=False):
    meta = json.loads((src / "meta.json").read_text(encoding="utf-8"))
    st = Stato(bozza)
    files = sorted(src.glob("parte-*.md"))
    if not files:
        sys.exit("Nessun file parte-*.md in " + str(src))
    front_html, body_parts = "", []
    for f in files:
        n = int(re.match(r"parte-(\d+)", f.name).group(1))
        sol = []
        txt = preprocess(f.read_text(encoding="utf-8"), st, n, sol)
        h = md2html(txt)
        h = h.replace("<li>[ ] ", '<li class="check"><span class="cb"></span>')
        h = post_admonitions(h)
        h = number_headings(h, st, n, front=(n == 0))
        if n == 0:
            front_html += h
        else:
            body_parts.append(h + soluzioni_html(sol, n))
    body = crossrefs("".join(body_parts), st)
    front_html = crossrefs(front_html, st)
    blocks = tag_blocks(split_blocks(body), 0)

    fc = FontConfiguration()
    css = [CSS(filename=str(ENGINE / "style_A.css"), font_config=fc)]

    def make_doc(pg):
        return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>{html.escape(meta['titolo'])}</title>
<meta name="description" content="{html.escape(meta.get('sottotitolo', ''))}">
</head><body>
<section class="titlepage"><div class="rule"></div>
<h1 class="title">{html.escape(meta['titolo'])}</h1>
<div class="subtitle">{html.escape(meta.get('sottotitolo', ''))}</div>
<div class="edition">{html.escape(meta.get('edizione', ''))}</div></section>
<section class="titlepage"><div class="copyright">{meta.get('copyright_html', '')}</div></section>
<section class="front"><h2 class="plain">Indice</h2>{make_toc(st, pg)}{front_html}</section>
<section class="main">{''.join(blocks)}{make_index(st, pg)}</section>
</body></html>"""

    def render(pg):
        return HTML(string=make_doc(pg), base_url=str(ENGINE)).render(stylesheets=css, font_config=fc)

    class Segnaposto(dict):  # primo passaggio: numeri fittizi della stessa larghezza dei reali
        def get(self, k, d=None):
            return "000"

    moved = []
    doc = render(Segnaposto())
    for _ in range(6):
        if not float_figures(blocks, doc, moved):
            break
        doc = render(Segnaposto())
    anchor = {}
    for i, page in enumerate(doc.pages):
        for name in page.anchors:
            anchor.setdefault(name, i)
    first_key = min((k for k in anchor if re.fullmatch(r"p\d+", k)), key=lambda k: anchor[k], default=None)
    first = anchor[first_key] if first_key else 0
    pg = {}
    for k, v in anchor.items():
        pg[k] = (v - first + 1) if v >= first else roman(v + 1)
    doc = render(pg)
    # ricontrollo: i numeri di pagina non devono essere cambiati con l'indice compilato
    anchor2 = {}
    for i, page in enumerate(doc.pages):
        for name in page.anchors:
            anchor2.setdefault(name, i)
    if first_key and anchor2.get(first_key) != first:
        st.avvisi.append(f"l'indice compilato ha spostato l'inizio del corpo ({first} -> {anchor2.get(first_key)}): rieseguire la build")
    out_dir = src / "output"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / (outname or meta.get("file", "volumeA.pdf"))
    doc.write_pdf(out)
    (out_dir / "debug.html").write_text(make_doc(pg), encoding="utf-8")
    figpages = {}
    for fid, f in st.figure.items():
        figpages[fid] = {**f, "pagina": pg.get(f["anchor"])}
    report = {"pdf": str(out), "pagine_totali": len(doc.pages), "pagine_preliminari": first,
              "parti": [t[3] for t in st.toc if t[0] == "part"], "figure": figpages,
              "figure_da_validare": sorted(k for k, v in st.figure.items() if v["stato"] != "validato"),
              "spostamenti_figure": moved, "voci_indice": len(st.voci), "avvisi": st.avvisi}
    (out_dir / "build_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK {out} | pagine={len(doc.pages)} (preliminari {first}) | figure={len(st.figure)} "
          f"(da validare {len(report['figure_da_validare'])}) | spostamenti={len(moved)} | voci indice={len(st.voci)}")
    for a in st.avvisi:
        print("AVVISO:", a)
    return report


def roman(n):
    vals = [(1000, "m"), (900, "cm"), (500, "d"), (400, "cd"), (100, "c"), (90, "xc"), (50, "l"), (40, "xl"),
            (10, "x"), (9, "ix"), (5, "v"), (4, "iv"), (1, "i")]
    s = ""
    for v, r in vals:
        while n >= v:
            s += r
            n -= v
    return s


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    out = a[a.index("--out") + 1] if "--out" in a else None
    build(Path(a[0]).resolve(), out, bozza="--bozza" in a)
