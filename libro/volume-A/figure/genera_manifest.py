#!/usr/bin/env python3
"""
Rigenera figure/MANIFEST.csv raccogliendo i metadati JSON di tutte le figure:
  sim/out/*.json      tracciati didattici simulati
  real/out/*.json     tracciati reali (PhysioNet), solo quelli che hanno superato il QC
  schemi/out/*.json   schemi originali
Lo stato di validazione già presente nel MANIFEST (es. 'validato', 'da_correggere') viene CONSERVATO:
il revisore lo modifica a mano nel CSV e la rigenerazione non lo sovrascrive.

Colonne: id, descrizione, tipo, file, fonte_licenza, criteri_verifica, affidabilita, scala,
         gruppo_checklist, stato_validazione, note_revisore
"""
import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLS = ["id", "descrizione", "tipo", "file", "fonte_licenza", "criteri_verifica", "affidabilita", "scala",
        "gruppo_checklist", "stato_validazione", "note_revisore"]


def main():
    old = {}
    mf = HERE / "MANIFEST.csv"
    if mf.exists():
        with mf.open(encoding="utf-8") as f:
            old = {r["id"]: r for r in csv.DictReader(f)}
    rows = []
    for sub in ("schemi", "sim", "real"):
        for p in sorted((HERE / sub / "out").glob("*.json")):
            m = json.loads(p.read_text(encoding="utf-8"))
            if m.get("escluso"):
                continue
            crit = m.get("criteri_revisore") or []
            if m.get("descrizione_attesa"):
                crit = [m["descrizione_attesa"]] + crit
            r = {
                "id": m["id"],
                "descrizione": m.get("titolo", ""),
                "tipo": m.get("tipo", ""),
                "file": m.get("file", {}).get("svg", ""),
                "fonte_licenza": m.get("attribuzione_breve") or m.get("fonte", ""),
                "criteri_verifica": " | ".join(crit),
                "affidabilita": m.get("affidabilita_modello", ""),
                "scala": m.get("scala", 1.0),
                "gruppo_checklist": m.get("gruppo", ""),
                "stato_validazione": "da_validare",
                "note_revisore": "",
            }
            if r["id"] in old:  # conserva le decisioni del revisore
                r["stato_validazione"] = old[r["id"]].get("stato_validazione") or "da_validare"
                r["note_revisore"] = old[r["id"]].get("note_revisore", "")
            rows.append(r)
    with mf.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    by = {}
    for r in rows:
        by[r["tipo"]] = by.get(r["tipo"], 0) + 1
    print(f"MANIFEST.csv: {len(rows)} figure", by)


if __name__ == "__main__":
    main()
