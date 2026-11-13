#!/usr/bin/env python3
"""
Build del tomo «Basi di farmacologia clinica» (KDP 6x9", bianco e nero).

Uso:  python3 libro/engine/build_tomo.py libro/tomo [--out nome.pdf]
Input: <tomo>/meta.json, <tomo>/frontmatter.md, <tomo>/parte-NN-*.md (ordine alfabetico)
Convenzioni Markdown:
  # Titolo Parte           -> Parte N (nuova pagina); N = ordine dei file
  ## Titolo sezione        -> sezione N.M
  ### Molecola {.pa}       -> scheda molecola: finisce nell'indice dei principi attivi
  !!! nota|chiave|attenzione|rischio|focus "Titolo"  (corpo indentato di 4 spazi)
  - [ ] voce               -> checklist con casella
"""
import json, re, sys, html, unicodedata
from pathlib import Path
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

ENGINE = Path(__file__).resolve().parent

def md2html(text):
    m = markdown.Markdown(extensions=["tables", "admonition", "attr_list", "sane_lists", "toc", "md_in_html"])
    return m.convert(text)

def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()

def sortkey(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))

def build(tomo: Path, outname=None):
    meta = json.loads((tomo / "meta.json").read_text(encoding="utf-8"))
    parts = sorted(tomo.glob("parte-*.md"))
    if not parts:
        sys.exit("Nessun file parte-*.md")
    body = md2html("\n\n".join(p.read_text(encoding="utf-8").strip() for p in parts))
    body = body.replace('<li>[ ] ', '<li class="check"><span class="cb"></span>')

    toc, pa, st = [], [], {"part": 0, "sec": 0}
    def head(m):
        lvl, hid, title = m.group(1), m.group(2), m.group(3)
        if lvl == "1":
            st["part"] += 1; st["sec"] = 0
            n = st["part"]; pid = f"p{n}"
            toc.append(("part", plain(title), pid, str(n)))
            label = re.sub(r"[\"']", "", plain(title))
            return (f'<h1 class="part" id="{pid}" style="string-set: partname \'Parte {n} — {label}\'">'
                    f'<span class="plabel">Parte {n}</span><span class="ptitle">{title}</span></h1>')
        st["sec"] += 1
        num = f'{st["part"]}.{st["sec"]}'; sid = f"s{st['part']}_{st['sec']}"
        toc.append(("sec", plain(title), sid, num))
        return f'<h2 class="sezione" id="{sid}"><span class="snum">{num}</span>{title}</h2>'
    body = re.sub(r'<h([12]) id="([^"]*)">(.*?)</h\1>', head, body)

    def h3(m):
        attrs, title = m.group(1), m.group(2)
        if 'class="pa"' in attrs:
            idm = re.search(r'id="([^"]*)"', attrs)
            if idm: pa.append((plain(title), idm.group(1)))
        return m.group(0)
    re.sub(r'<h3([^>]*)>(.*?)</h3>', h3, body)

    front_md = tomo / "frontmatter.md"
    front = md2html(front_md.read_text(encoding="utf-8")) if front_md.exists() else ""

    def make_toc(pg):
        out = ['<div class="toc">']
        for kind, label, hid, n in toc:
            p = pg.get(hid, "")
            if kind == "part":
                out.append(f'<div class="tp"><a href="#{hid}"><span class="t">Parte {n} — {html.escape(label)}</span><span class="pg">{p}</span></a></div>')
            else:
                out.append(f'<div class="tc"><a href="#{hid}"><span class="n">{n}</span><span class="t">{html.escape(label)}</span><span class="pg">{p}</span></a></div>')
        out.append("</div>")
        return "".join(out)

    def make_index(pg):
        if not pa: return ""
        out = ['<h1 class="plain-index" id="indice-pa">Indice dei principi attivi</h1><div class="pa-index">']
        cur = ""
        for name, hid in sorted(pa, key=lambda x: sortkey(x[0])):
            L = sortkey(name)[:1].upper()
            if L != cur:
                out.append(f'<div class="let">{L}</div>'); cur = L
            out.append(f'<div><a href="#{hid}"><span class="t">{html.escape(name)}</span><span class="pg">{pg.get(hid, "")}</span></a></div>')
        out.append("</div>")
        return "".join(out)

    def make_doc(pg):
        return f"""<!doctype html><html lang="it"><head><meta charset="utf-8">
<title>{html.escape(meta['titolo'])}</title>
<meta name="description" content="{html.escape(meta['sottotitolo'])}">
</head><body>
<section class="titlepage"><div class="rule"></div>
<h1 class="title">{html.escape(meta['titolo'])}</h1>
<div class="subtitle">{html.escape(meta['sottotitolo'])}</div>
<div class="edition">{html.escape(meta['edizione'])}</div></section>
<section class="titlepage"><div class="copyright">{meta['copyright_html']}</div></section>
<section class="front">{front}
<h2 class="plain">Indice</h2>{make_toc(pg)}</section>
<section class="main">{body}{make_index(pg)}</section>
</body></html>"""

    out_dir = tomo / "output"; out_dir.mkdir(exist_ok=True)
    out = out_dir / (outname or meta["file"])
    fc = FontConfiguration()
    css = [CSS(filename=str(ENGINE / "style_kdp.css"), font_config=fc)]

    rendered = HTML(string=make_doc({}), base_url=str(ENGINE)).render(stylesheets=css, font_config=fc)
    anchor = {}
    for i, page in enumerate(rendered.pages):
        for name in page.anchors:
            anchor.setdefault(name, i)
    first = anchor["p1"]
    pg = {k: v - first + 1 for k, v in anchor.items()}
    doc = make_doc(pg)
    (out_dir / "debug.html").write_text(doc, encoding="utf-8")
    HTML(string=doc, base_url=str(ENGINE)).write_pdf(out, font_config=fc, stylesheets=css)
    print(f"OK {out} | parti={st['part']} voci_indice_pa={len(pa)} | pagine preliminari={first}")

if __name__ == "__main__":
    a = sys.argv[1:]
    out = a[a.index("--out") + 1] if "--out" in a else None
    build(Path(a[0]).resolve(), out)
