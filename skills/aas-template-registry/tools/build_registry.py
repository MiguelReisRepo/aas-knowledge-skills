#!/usr/bin/env python3
"""Build the IDTA submodel template registry.

For every template version the editor catalogue offers, record each element's
cardinality as the template JSON declares it and as the specification PDF's
tables declare it, and derive the EFFECTIVE cardinality:

  - JSON and PDF agree                        -> that value            (agree)
  - they disagree, PDF row matched with high  -> the less strict of    (divergent)
    confidence                                   the two
  - JSON has a cardinality, PDF not verifiable -> the JSON value         (unverified / json-only)
  - JSON has none, PDF row high confidence     -> the PDF value          (pdf-only)

Why the less strict one (project decision, 2026-09-17): IDTA publishes both artefacts as
official and states no precedence between them (checked in all 76 PDFs and the
repository README). A requirement only blocks a user when both official sources
make it; the divergence itself is reported.

Inputs (all local, nothing fetched here):
  --catalogue  the editor's catalogue dump (list of {idShort, version, name, path, sha, jsonData})
  --pdf-rows   pdf_card_rows.json from extract_tables.py (per PDF: page, card, flat row text)
  --pdfs       published_pdfs.json (paths of the PDFs in the IDTA repository)
Output: registry/ next to this tools/ folder.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "registry")

NORM = {"one": "1", "zerotoone": "0..1", "zerotomany": "0..*", "onetomany": "1..*"}
BOUNDS = {"1": (1, 1), "0..1": (0, 1), "0..*": (0, math.inf), "1..*": (1, math.inf)}
FROM_BOUNDS = {v: k for k, v in BOUNDS.items()}


def loosest(a: str, b: str) -> str:
    (amin, amax), (bmin, bmax) = BOUNDS[a], BOUNDS[b]
    return FROM_BOUNDS[(min(amin, bmin), max(amax, bmax))]


def json_cardinality(el: dict) -> tuple[str | None, str | None]:
    for q in el.get("qualifiers") or []:
        if str(q.get("type", "")).lower() in ("cardinality", "smt/cardinality", "multiplicity"):
            return NORM.get(str(q.get("value", "")).lower()), q.get("kind")
    return None, None


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")


def pdf_for(template_path: str, pdfs: list[str]) -> tuple[str | None, str]:
    """The PDF in the template's version folder, else the nearest ancestor folder's."""
    d = os.path.dirname(template_path)
    same = True
    while d.startswith("published/") and d != "published":
        c = sorted(p for p in pdfs if os.path.dirname(p) == d)
        if c:
            return c[0], ("same folder" if same else "ancestor folder (bug-fix release without its own PDF)")
        d = os.path.dirname(d)
        same = False
    return None, "none"


def walk(elements, path, out, in_list=False):
    for i, el in enumerate(elements or []):
        if not isinstance(el, dict):
            continue
        label = el.get("idShort") or f"[{i}]"
        p = f"{path} > {label}" if path else label
        sid = ((el.get("semanticId") or {}).get("keys") or [{}])[0].get("value", "")
        card, kind = json_cardinality(el)
        out.append({
            "path": p, "idShort": el.get("idShort") or "", "modelType": el.get("modelType"),
            "semanticId": sid, "json": card, "jsonQualifierKind": kind, "listChild": in_list,
        })
        mt = str(el.get("modelType", "")).lower()
        if isinstance(el.get("value"), list) and mt in ("submodelelementcollection", "submodelelementlist"):
            walk(el["value"], p, out, mt == "submodelelementlist")
        if isinstance(el.get("statements"), list):
            walk(el["statements"], p, out)
        if isinstance(el.get("annotations"), list):
            walk(el["annotations"], p, out)


def match_pdf(el: dict, rows: list[dict], sid_counts: Counter) -> dict:
    sid = re.sub(r"\s+", "", el["semanticId"] or "")
    if len(sid) <= 12:
        return {"confidence": "none"}
    by_sid = [r for r in rows if sid in r["flat"]]
    if not by_sid:
        return {"confidence": "none"}
    ids = re.sub(r"\s+", "", el["idShort"] or "")
    # The idShort must EQUAL a cell (type prefix like "[SML]" and footnote digits
    # removed), not merely occur in the row: "htv_header" occurs in the row of its
    # parent "htv_headers" and matched the parent's cardinality.
    # extract_tables.py joins the lines of a wrapped cell ("RenewableCo" + "ntent"); whitespace is removed here.
    # A wrapped idShort can also lose one inner character to the next column ("SeparateColl" + "ction"): a cell
    # equal to the idShort minus one inner character counts too (idShorts of 8+ characters, same semanticId row
    # only, and only when no row of that semanticId carries the exact idShort).
    by_both = [r for r in by_sid if ids and any(cell_name(c) == ids for c in r["text"].split(" | "))] or \
        [r for r in by_sid if ids and any(is_name(c, ids) for c in r["text"].split(" | "))]
    shared = sid_counts[el["semanticId"]] > 1
    for rows_, level in ((by_both, "high"), (by_sid, "medium")):
        if not rows_:
            continue
        cards = sorted({r["card"] for r in rows_})
        pages = sorted({r["page"] for r in rows_})
        if len(cards) == 1 and not (shared and level == "medium"):
            out = {"confidence": level, "card": cards[0], "pages": pages}
            if level == "high":
                out["row"] = row_cells(rows_[0], ids, sid)
            return out
        return {"confidence": "low", "cards": cards, "pages": pages}
    return {"confidence": "none"}


def cell_name(c: str) -> str:
    """A table cell as an idShort: type marker ("[SML]") and footnote digits removed, whitespace removed."""
    return re.sub(r"\s+", "", re.sub(r"^\[[^\]]*\]\s*\d*", "", c.strip()))


def is_name(cell: str, ids: str) -> bool:
    n = cell_name(cell)
    # inner deletions only: a missing first or last character is a different idShort ("PcfCalculationMethod" is
    # the child of "PcfCalculationMethods"), not a wrap loss
    return n == ids or (len(ids) >= 8 and len(n) == len(ids) - 1 and any(ids[:i] + ids[i + 1:] == n for i in range(1, len(ids) - 1)))


def row_cells(row: dict, ids: str, sid: str) -> dict:
    """The matched table row, for a citation: PDF page, the type marker, the idShort cell (wrapped lines joined), the
    semanticId and the card. cell."""
    cell = next((c for c in row["text"].split(" | ") if is_name(c, ids)), "")
    m = re.match(r"^(\[[^\]]*\])", cell.strip())
    return {"page": row["page"], "type": m.group(1) if m else None, "idShort": cell_name(cell), "semanticId": sid, "card": row["card"]}


ANNEX_A = [  # literal sentences of Annex A ("Explanations on used table formats") worth citing, whitespace-normalised
    re.compile(r"The table heads abbreviate .cardinality. with .card.\."),
    re.compile(r"[^.]*the definitive definitions are (?:given by|provided in) a separate file in (?:the )?form of an AASX file of the Submodel template and its elements\."),
    re.compile(r"The cardinality is defined with [^.]*?optional to many entries"),
]
_annex: dict = {}


def annex_a(pdf_path: str | None) -> list[dict]:
    """Annex A sentences of one PDF with their PDF page (1-based), read with PyMuPDF; [] when the PDF or PyMuPDF is
    not available (the registry then simply carries no Annex A quotes)."""
    if not pdf_path or not os.path.exists(pdf_path):
        return []
    if pdf_path in _annex:
        return _annex[pdf_path]
    out = []
    try:
        import fitz  # PyMuPDF
        doc = fitz.open(pdf_path)
        for i, page in enumerate(doc):
            text = re.sub(r"\s+", " ", page.get_text())
            for rx in ANNEX_A:
                for m in rx.finditer(text):
                    q = m.group(0).strip()
                    if not any(o["quote"] == q for o in out):
                        out.append({"page": i + 1, "quote": q})
    except Exception:  # noqa: BLE001
        out = []
    _annex[pdf_path] = out
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--catalogue", required=True)
    ap.add_argument("--pdf-rows", required=True)
    ap.add_argument("--pdfs", required=True)
    ap.add_argument("--pdf-dir", required=True, help="local mirror of the PDFs, for their sha256")
    args = ap.parse_args()

    catalogue = json.load(open(args.catalogue))
    rows_by_pdf = json.load(open(args.pdf_rows))
    pdfs = json.load(open(args.pdfs))
    os.makedirs(OUT, exist_ok=True)

    index, divergences, totals = [], [], Counter()
    for t in catalogue:
        pdf, relation = pdf_for(t["path"], pdfs)
        rows = rows_by_pdf.get(pdf, []) if pdf else []
        pdf_sha = None
        if pdf and os.path.exists(os.path.join(args.pdf_dir, pdf)):
            pdf_sha = hashlib.sha256(open(os.path.join(args.pdf_dir, pdf), "rb").read()).hexdigest()
        subs = t["jsonData"].get("submodels") or [t["jsonData"]]
        sm = subs[0]
        elements = []
        walk(sm.get("submodelElements"), "", elements)
        sid_counts = Counter(e["semanticId"] for e in elements if e["semanticId"])
        for e in elements:
            m = match_pdf(e, rows, sid_counts)
            e["pdf"] = m
            pdf_card = m.get("card") if m["confidence"] in ("high", "medium") else None
            if e["json"] and pdf_card:
                if e["json"] == pdf_card:
                    e["status"], e["effective"] = "agree", e["json"]
                elif m["confidence"] == "high":
                    e["status"], e["effective"] = "divergent", loosest(e["json"], pdf_card)
                else:
                    e["status"], e["effective"] = "unverified", e["json"]
            elif e["json"]:
                e["status"], e["effective"] = ("unverified" if m["confidence"] != "none" else "json-only"), e["json"]
            elif pdf_card and m["confidence"] == "high":
                e["status"], e["effective"] = "pdf-only", pdf_card
            else:
                e["status"], e["effective"] = "none", None
            totals[e["status"]] += 1
            if e["status"] == "divergent":
                divergences.append({
                    "template": t["idShort"], "version": t["version"], "path": e["path"],
                    "semanticId": e["semanticId"], "json": e["json"], "pdf": pdf_card,
                    "pages": m.get("pages"), "effective": e["effective"],
                })
        key = f"{slug(t['idShort'])}/{t['version']}"
        record = {
            "template": t["idShort"], "version": t["version"],
            "submodelIdShort": sm.get("idShort"),
            "submodelSemanticId": ((sm.get("semanticId") or {}).get("keys") or [{}])[0].get("value"),
            "json": {"path": t["path"], "gitBlob": t["sha"]},
            "pdf": {"path": pdf, "relation": relation, "sha256": pdf_sha,
                    "annexA": annex_a(os.path.join(args.pdf_dir, pdf) if pdf else None)},
            "counts": dict(Counter(e["status"] for e in elements)),
            "elements": elements,
        }
        os.makedirs(os.path.join(OUT, slug(t["idShort"])), exist_ok=True)
        with open(os.path.join(OUT, f"{key}.json"), "w") as f:
            json.dump(record, f, indent=1, ensure_ascii=False)
        write_card(record, os.path.join(OUT, f"{key}.md"))
        index.append({"template": t["idShort"], "version": t["version"], "file": f"{key}.json",
                      "card": f"{key}.md", "submodelSemanticId": record["submodelSemanticId"],
                      "pdf": pdf, "counts": record["counts"]})

    with open(os.path.join(OUT, "index.json"), "w") as f:
        json.dump(index, f, indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, "divergences.json"), "w") as f:
        json.dump(divergences, f, indent=1, ensure_ascii=False)
    write_divergences(divergences, totals, os.path.join(OUT, "DIVERGENCES.md"))
    print(f"templates {len(index)}; element statuses {dict(totals)}; divergent {len(divergences)}")


def cell(s) -> str:
    return str(s if s is not None else "").replace("|", "\\|")


def write_card(r: dict, path: str) -> None:
    lines = [
        f"# {r['template']} {r['version']}",
        "",
        f"- Submodel: `{r['submodelIdShort']}`, semanticId `{r['submodelSemanticId']}`",
        f"- Template JSON: `{r['json']['path']}` (git blob `{r['json']['gitBlob']}`)",
        f"- Specification PDF: `{r['pdf']['path']}` ({r['pdf']['relation']})",
        f"- Element statuses: {r['counts']}",
        "",
        "Effective cardinality: JSON and PDF agree, or the less strict of the two when they diverge (see the registry SKILL.md).",
        "",
        "| path | type | semanticId | JSON | PDF (page) | effective | status |",
        "|---|---|---|---|---|---|---|",
    ]
    for e in r["elements"]:
        m = e["pdf"]
        pdf = ""
        if m.get("card"):
            pdf = f"{m['card']} (p.{','.join(map(str, m['pages']))}, {m['confidence']})"
        elif m.get("cards"):
            pdf = f"ambiguous {m['cards']} (p.{','.join(map(str, m['pages']))})"
        lines.append(f"| {cell(e['path'])} | {cell(e['modelType'])} | {cell(e['semanticId'])} | {cell(e['json'])} | {cell(pdf)} | {cell(e['effective'])} | {e['status']} |")
    open(path, "w").write("\n".join(lines) + "\n")


def write_divergences(divs: list[dict], totals: Counter, path: str) -> None:
    lines = [
        "# JSON versus PDF divergences",
        "",
        "Generated by `tools/build_registry.py`. Every row is an element whose template JSON cardinality differs from the cardinality in its specification PDF table, where the table row was matched by semanticId AND idShort. The effective cardinality is the less strict of the two. Each one is a candidate issue for github.com/admin-shell-io/submodel-templates.",
        "",
        f"Element statuses over the whole catalogue: {dict(totals)}",
        "",
        "| template | version | path | JSON | PDF | pages | effective |",
        "|---|---|---|---|---|---|---|",
    ]
    for d in divs:
        lines.append(f"| {cell(d['template'])} | {d['version']} | {cell(d['path'])} | {d['json']} | {d['pdf']} | {','.join(map(str, d['pages'] or []))} | {d['effective']} |")
    open(path, "w").write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
