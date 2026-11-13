#!/usr/bin/env python3
"""
Motore di build per la collana "Manuale di farmacologia cardiovascolare".

Uso:   python3 libro/engine/build.py libro/volumi/01-betabloccanti
Input: <volume>/meta.json  +  <volume>/parte-NN.md (ordinati per nome)
Output: <volume>/output/<slug>.pdf

Convenzioni Markdown nei file parte-NN.md
  # Titolo della Parte            -> Parte (nuova pagina, numerazione romana automatica)
  ## Titolo del capitolo          -> Capitolo (numerazione progressiva sull'intero volume)
  ### Sezione                     -> sottotitolo non numerato
  !!! nota "Titolo"               -> riquadro giallo/oro (note e casi studio)
  !!! chiave "Punti chiave"       -> riquadro azzurro
  !!! attenzione "Titolo"         -> riquadro rosso (sicurezza)
  !!! obiettivi "In questa parte" -> riquadro introduttivo di Parte
  Il corpo del riquadro è indentato di 4 spazi.
"""
import json, re, sys, html
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

ENGINE = Path(__file__).resolve().parent
ROMAN = ["I","II","III","IV","V","VI","VII","VIII","IX","X","XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX"]

def render_md(text: str) -> str:
    md = markdown.Markdown(extensions=["tables", "admonition", "attr_list", "sane_lists", "toc", "md_in_html"],
                           extension_configs={"toc": {"permalink": False}})
    return md.convert(text)

def build(vol_dir: Path):
    meta = json.loads((vol_dir / "meta.json").read_text(encoding="utf-8"))
    parts = sorted(vol_dir.glob("parte-*.md"))
    if not parts:
        sys.exit("Nessun file parte-*.md trovato")

    body_md = "\n\n".join(p.read_text(encoding="utf-8").strip() for p in parts)
    body = render_md(body_md)

    # --- numerazione di Parti e Capitoli + raccolta voci d'indice --------------------------------
    toc, part_i, ch_i = [], 0, 0
    def h1(m):
        nonlocal part_i
        part_i += 1
        hid = f"p{part_i}"
        title = m.group(3)
        toc.append(("part", f"Parte {ROMAN[part_i-1]} — {html.unescape(re.sub('<[^>]+>','',title))}", hid, ROMAN[part_i-1]))
        first = " first" if part_i == 1 else ""
        label = re.sub('<[^>]+>','',title).replace('"','').replace("'","")
        return (f'<h1 class="part{first}" id="{hid}" style="string-set: partname \'Parte {ROMAN[part_i-1]} — {label}\'"><span class="plabel">Parte {ROMAN[part_i-1]}</span>'
                f'<span class="ptitle">{title}</span></h1>')
    def h2(m):
        nonlocal ch_i
        ch_i += 1
        hid = f"c{ch_i}"
        title = m.group(3)
        toc.append(("ch", re.sub('<[^>]+>','',title), hid, str(ch_i)))
        return f'<h2 class="chapter" id="{hid}"><span class="cnum">Capitolo {ch_i}</span>{title}</h2>'
    body = body.replace('<li>[ ] ', '<li class="check"><span class="cb"></span>')
    # un'unica passata sui titoli h1/h2, così l'indice rispetta l'ordine del documento
    def heading(m):
        return h1(m) if m.group(1) == "1" else h2(m)
    body = re.sub(r'<h([12]) id="([^"]*)">(.*?)</h\1>', heading, body)

    def make_toc(pages):
        out = ['<div class="toc">']
        for kind, label, hid, n in toc:
            pg = pages.get(hid, "")
            if kind == "part":
                out.append(f'<div class="tp"><a href="#{hid}"><span class="t">{html.escape(label)}</span><span class="pg">{pg}</span></a></div>')
            else:
                out.append(f'<div class="tc"><a href="#{hid}"><span class="n">{n}</span><span class="t">{html.escape(label)}</span><span class="pg">{pg}</span></a></div>')
        out.append('</div>')
        return "".join(out)

    front_extra = (vol_dir / "frontmatter.md")
    front_html = render_md(front_extra.read_text(encoding="utf-8")) if front_extra.exists() else ""

    cover = f"""
    <section class="cover">
      <div class="band"></div>
      <div class="series">{html.escape(meta['serie'])}</div>
      <div class="vol">Volume {html.escape(meta['volume'])}</div>
      <h1 class="title">{html.escape(meta['titolo_breve'])}</h1>
      <div class="rule"></div>
      <div class="subtitle">{html.escape(meta['sottotitolo'])}</div>
      <div class="foot">{meta['piede_copertina']}</div>
    </section>"""

    def make_doc(toc_html):
      return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
    <title>{html.escape(meta['titolo_completo'])}</title>
    <meta name="author" content="{html.escape(meta.get('autore',''))}">
    <meta name="description" content="{html.escape(meta['sottotitolo'])}">
    </head><body>
    {cover}
    <section class="front">{front_html}
      <h2 class="plain toc-title">Indice</h2>
      {toc_html}
    </section>
    <section class="main">{body}</section>
    </body></html>"""

    out_dir = vol_dir / "output"; out_dir.mkdir(exist_ok=True)
    out = out_dir / meta["file"]
    fc = FontConfiguration()  # necessario per caricare i @font-face (Gelasio)
    css = [CSS(filename=str(ENGINE / "style.css"), font_config=fc)]

    # Passo 1: render con indice vuoto per ricavare la pagina di ogni titolo
    doc1 = make_doc(make_toc({}))
    rendered = HTML(string=doc1, base_url=str(ENGINE)).render(stylesheets=css, font_config=fc)
    anchor_page = {}
    for i, page in enumerate(rendered.pages):
        for name in page.anchors:
            anchor_page.setdefault(name, i)
    first_body = anchor_page["p1"]
    pages = {k: v - first_body + 1 for k, v in anchor_page.items() if k[0] in "pc"}

    # Passo 2: render definitivo con numeri di pagina reali nell'indice
    doc = make_doc(make_toc(pages))
    (out_dir / "debug.html").write_text(doc, encoding="utf-8")
    HTML(string=doc, base_url=str(ENGINE)).write_pdf(out, font_config=fc, stylesheets=css)
    print(f"OK  {out}  | parti={part_i} capitoli={ch_i}")

if __name__ == "__main__":
    build(Path(sys.argv[1]).resolve())
