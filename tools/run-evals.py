#!/usr/bin/env python3
"""Eval runner for the aas-skills knowledge skills.

Two commands:

  run-evals.py selftest [--skill NAME ...] [--skip-missing-sources]
      Structural self-test of every skills/*/evals/evals.json (and VERSION.json):
        - every item has a citation with document, revision, file and a literal quote
        - ids are unique across ALL skills and carry the skill prefix
        - must_include is non-empty
        - the cited file exists (repo-relative path, or "<alias>:<path>" resolved via tools/sources.json)
        - the quote really occurs in the cited file, at the cited page (PDF / paged .txt) or line range
        - 8..15 items per skill, VERSION.json present with semver + last_verified + sources
      It first proves it can fail: a broken fixture (tools/fixtures/broken/) must trigger every check.
      --skip-missing-sources counts (and does not verify) citations into an off-repo alias whose
      directory does not exist on this machine; the summary says how many were skipped.

  run-evals.py grade ANSWERS.json [--skill NAME ...] [--out RESULT.json]
      ANSWERS.json maps item id -> answer text. Each item passes when every must_include entry occurs
      (case-insensitive, whitespace-normalised; an entry may be a list of alternatives, any one suffices)
      and no must_not_include entry occurs. Prints a pass table per skill and the failing items.

Exit code 0 only when everything passes. Python 3.9+, stdlib only; pypdf is needed only for citations
that point at a .pdf file.
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SKILLS = REPO / "skills"
SOURCES_MAP = Path(__file__).resolve().parent / "sources.json"
FIXTURES = Path(__file__).resolve().parent / "fixtures"
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
PAGE_MARK = re.compile(r"^\s*=+\s*page\s+(\d+)(?:\s*/\s*\d+)?\s*=+\s*$", re.I | re.M)
MIN_ITEMS, MAX_ITEMS = 8, 15

_pdf_cache: dict[str, list[str]] = {}
# --skip-missing-sources: citations into an alias whose directory is absent on this machine are counted
# as skipped instead of failing (for a checkout without the off-repo mirrors). Never the default.
SKIP_MISSING_SOURCES = False
_skipped: list[str] = []
_text_cache: dict[str, str] = {}


# ---------------------------------------------------------------- helpers
def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def squash(s: str) -> str:
    """Remove all whitespace: tolerates PDF extraction artefacts such as 'S P E C' or broken lines."""
    return re.sub(r"\s+", "", s).lower()


def norm_quote_chars(s: str) -> str:
    table = {"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-",
             " ": " ", "‐": "-", "‑": "-", "ﬁ": "fi", "ﬂ": "fl"}
    for a, b in table.items():
        s = s.replace(a, b)
    return s


def contains(haystack: str, needle: str) -> bool:
    h, n = norm_quote_chars(haystack), norm_quote_chars(needle)
    return norm(n) in norm(h) or squash(n) in squash(h)


def load_sources_map() -> dict[str, str]:
    m = {}
    if SOURCES_MAP.exists():
        m = json.loads(SOURCES_MAP.read_text())
        m = {k: v for k, v in m.items() if not k.startswith("_")}
    for k in list(m):
        env = os.environ.get("AAS_SOURCES_" + re.sub(r"[^A-Z0-9]", "_", k.upper()))
        if env:
            m[k] = env
    return m


def resolve(file_ref: str, smap: dict[str, str]) -> Path | None:
    if not isinstance(file_ref, str) or not file_ref:
        return None
    m = re.match(r"^([a-z0-9-]+):(?!//)(.+)$", file_ref)
    if m and m.group(1) in smap:
        return Path(os.path.expanduser(smap[m.group(1)])) / m.group(2)
    if m:
        return None  # unknown alias
    return REPO / file_ref


def file_text(p: Path) -> str:
    key = str(p)
    if key not in _text_cache:
        raw = p.read_text(errors="replace")
        if p.suffix.lower() in (".html", ".htm", ".xhtml"):
            raw = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw, flags=re.S | re.I)
            raw = html.unescape(re.sub(r"<[^>]+>", " ", raw))
        _text_cache[key] = raw
    return _text_cache[key]


def pdf_pages(p: Path) -> list[str]:
    key = str(p)
    if key not in _pdf_cache:
        try:
            import pypdf  # type: ignore
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("pypdf is required to verify citations that point at a PDF") from e
        import logging
        logging.getLogger("pypdf").setLevel(logging.ERROR)
        reader = pypdf.PdfReader(str(p))
        pages = []
        for pg in reader.pages:
            try:
                pages.append(pg.extract_text() or "")
            except Exception:  # noqa: BLE001
                pages.append("")
        _pdf_cache[key] = pages
    return _pdf_cache[key]


def paged_txt(p: Path) -> dict[int, str] | None:
    text = file_text(p)
    marks = list(PAGE_MARK.finditer(text))
    if not marks:
        return None
    out = {}
    for i, mk in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        out[int(mk.group(1))] = text[mk.end():end]
    return out


def alias_root_missing(file_ref: str, smap: dict[str, str]) -> bool:
    m = re.match(r"^([a-z0-9-]+):(?!//)(.+)$", file_ref or "")
    return bool(m and m.group(1) in smap and not Path(os.path.expanduser(smap[m.group(1)])).is_dir())


def verify_quote(cit: dict, smap: dict[str, str]) -> str | None:
    """Return None when the quote is found where the citation says, else an error message."""
    p = resolve(cit.get("file", ""), smap)
    if p is None:
        return f"citation file alias not resolvable: {cit.get('file')!r} (see tools/sources.json)"
    if not p.exists():
        return f"citation file does not exist: {p}"
    quote = cit.get("quote", "")
    page = cit.get("page")
    lines = cit.get("lines")
    if p.suffix.lower() == ".pdf":
        pages = pdf_pages(p)
        if page is None:
            hay = "\n".join(pages)
        else:
            if not isinstance(page, int) or not 1 <= page <= len(pages):
                return f"page {page!r} out of range 1..{len(pages)} in {p.name}"
            hay = pages[page - 1] + "\n" + (pages[page] if page < len(pages) else "")
        return None if contains(hay, quote) else f"quote not found in {p.name}" + (f" page {page}" if page else "")
    text = file_text(p)
    if page is not None:
        pages = paged_txt(p)
        if pages is None:
            return f"citation gives page {page} but {p.name} has no page markers (cite the PDF instead)"
        if page not in pages:
            return f"page {page} not in {p.name}"
        hay = pages[page] + "\n" + pages.get(page + 1, "")
        return None if contains(hay, quote) else f"quote not found in {p.name} page {page}"
    if lines:
        m = re.match(r"^(\d+)(?:-(\d+))?$", str(lines))
        if not m:
            return f"bad lines spec {lines!r}"
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        all_lines = text.splitlines()
        if not 1 <= a <= b <= len(all_lines):
            return f"lines {lines} out of range 1..{len(all_lines)} in {p.name}"
        hay = "\n".join(all_lines[a - 1:b])
        return None if contains(hay, quote) else f"quote not found in {p.name} lines {lines}"
    return None if contains(text, quote) else f"quote not found in {p.name}"


# ---------------------------------------------------------------- loading
def skill_dirs(only: list[str] | None, root: Path = SKILLS) -> list[Path]:
    dirs = sorted(d for d in root.iterdir() if (d / "evals" / "evals.json").exists())
    if only:
        dirs = [d for d in dirs if d.name in only]
        missing = set(only) - {d.name for d in dirs}
        if missing:
            sys.exit(f"no evals/evals.json for: {', '.join(sorted(missing))}")
    return dirs


def load_items(d: Path) -> tuple[dict, list[dict]]:
    data = json.loads((d / "evals" / "evals.json").read_text())
    return data, data.get("items", [])


# ---------------------------------------------------------------- self-test
def check_skill(d: Path, smap: dict[str, str], seen: dict[str, str]) -> list[str]:
    errs: list[str] = []
    name = d.name
    try:
        data, items = load_items(d)
    except json.JSONDecodeError as e:
        return [f"{name}: evals.json is not valid JSON: {e}"]
    if data.get("skill") != name:
        errs.append(f"{name}: evals.json 'skill' is {data.get('skill')!r}")
    if not MIN_ITEMS <= len(items) <= MAX_ITEMS:
        errs.append(f"{name}: {len(items)} items (expected {MIN_ITEMS}..{MAX_ITEMS})")
    for it in items:
        iid = it.get("id") or "<no id>"
        tag = f"{name}/{iid}"
        if not it.get("id"):
            errs.append(f"{tag}: missing id")
        elif iid in seen:
            errs.append(f"{tag}: duplicate id (also in {seen[iid]})")
        else:
            seen[iid] = name
        if it.get("id") and not str(iid).startswith(name + "-"):
            errs.append(f"{tag}: id must start with '{name}-'")
        for k in ("question", "expected_answer"):
            if not str(it.get(k, "")).strip():
                errs.append(f"{tag}: empty {k}")
        mi = it.get("must_include")
        if not isinstance(mi, list) or not mi or any(
            (isinstance(x, list) and (not x or any(not str(y).strip() for y in x))) or
            (not isinstance(x, list) and not str(x).strip()) for x in mi):
            errs.append(f"{tag}: must_include empty or has an empty entry")
        mn = it.get("must_not_include", [])
        if not isinstance(mn, list) or any(not str(x).strip() for x in mn):
            errs.append(f"{tag}: must_not_include must be a list of non-empty strings")
        cit = it.get("citation")
        if not isinstance(cit, dict) or not cit:
            errs.append(f"{tag}: no citation")
            continue
        for k in ("document", "revision", "file", "quote"):
            if not str(cit.get(k, "")).strip():
                errs.append(f"{tag}: citation.{k} missing")
        if not (cit.get("section") or cit.get("page") or cit.get("lines")):
            errs.append(f"{tag}: citation needs a section, page or lines locator")
        if cit.get("file") and cit.get("quote"):
            e = None
            if SKIP_MISSING_SOURCES and alias_root_missing(cit.get("file", ""), smap):
                _skipped.append(f"{tag}: {cit.get('file')}")
            else:
                try:
                    e = verify_quote(cit, smap)
                except RuntimeError as ex:
                    e = str(ex)
            if e:
                errs.append(f"{tag}: {e}")
        # the expected answer itself must satisfy its own grading strings
        exp = str(it.get("expected_answer", ""))
        if isinstance(mi, list) and mi and exp:
            bad = grade_one(exp, it)
            if bad:
                errs.append(f"{tag}: expected_answer fails its own grading ({bad})")
    vf = d / "VERSION.json"
    if not vf.exists():
        errs.append(f"{name}: VERSION.json missing")
    else:
        try:
            v = json.loads(vf.read_text())
            if not SEMVER.match(str(v.get("version", ""))):
                errs.append(f"{name}: VERSION.json version not semver")
            if not DATE.match(str(v.get("last_verified", ""))):
                errs.append(f"{name}: VERSION.json last_verified not YYYY-MM-DD")
            srcs = v.get("sources")
            if not isinstance(srcs, list) or not srcs or any(
                    not s.get("document") or not s.get("revision") for s in srcs):
                errs.append(f"{name}: VERSION.json sources must list document + revision")
        except json.JSONDecodeError as e:
            errs.append(f"{name}: VERSION.json invalid JSON: {e}")
    return errs


def selftest(only: list[str] | None) -> int:
    smap = load_sources_map()
    # 1) prove the checks bite: every planted defect in the broken fixture must be reported
    broken_root = FIXTURES / "broken"
    expected = json.loads((FIXTURES / "broken-expected.json").read_text())
    seen: dict[str, str] = {}
    fx_errs: list[str] = []
    for d in skill_dirs(None, broken_root):
        fx_errs += check_skill(d, smap, seen)
    must = expected["must_detect"]
    missed = [pat for pat in must if not any(re.search(pat, e) for e in fx_errs)]
    false_pos = [e for e in fx_errs for pat in expected["must_not_flag"] if re.search(pat, e)]
    print(f"negative control: {len(must) - len(missed)}/{len(must)} planted defects detected, "
          f"{len(false_pos)} false positive(s) on the clean control item")
    for pat in missed:
        print(f"  NOT DETECTED: {pat}")
    for e in false_pos:
        print(f"  FALSE POSITIVE: {e}")
    missed += false_pos
    # 2) the real skills
    seen = {}
    total, all_errs = 0, []
    print(f"\n{'skill':38} {'items':>5}  status")
    for d in skill_dirs(only):
        _, items = load_items(d)
        errs = check_skill(d, smap, seen)
        total += len(items)
        all_errs += errs
        print(f"{d.name:38} {len(items):5}  {'OK' if not errs else f'{len(errs)} error(s)'}")
    print(f"{'TOTAL':38} {total:5}")
    for e in all_errs:
        print("  ERROR", e)
    if total == 0:
        all_errs.append("no eval items found: a self-test over nothing is not a pass")
        print("  ERROR", all_errs[-1])
    if _skipped:
        print(f"\n{len(_skipped)} citation(s) SKIPPED: their source alias is not available on this machine "
              "(--skip-missing-sources); they were not verified")
    ok = not missed and not all_errs
    print("\nSELF-TEST", ("PASS" + (" (with skipped citations)" if _skipped else "")) if ok else "FAIL")
    return 0 if ok else 1


# ---------------------------------------------------------------- grading
def grade_one(answer: str, it: dict) -> str | None:
    missing = []
    for entry in it.get("must_include", []):
        alts = entry if isinstance(entry, list) else [entry]
        if not any(contains(answer, str(a)) for a in alts):
            missing.append("|".join(map(str, alts)))
    forbidden = [x for x in it.get("must_not_include", []) if contains(answer, str(x))]
    parts = []
    if missing:
        parts.append("missing: " + "; ".join(missing))
    if forbidden:
        parts.append("forbidden: " + "; ".join(forbidden))
    return " / ".join(parts) or None


def grade(answers_path: str, only: list[str] | None, out: str | None) -> int:
    answers = json.loads(Path(answers_path).read_text())
    rows, fails, result = [], [], {}
    for d in skill_dirs(only):
        _, items = load_items(d)
        p = 0
        for it in items:
            a = answers.get(it["id"])
            why = "no answer" if not a or not str(a).strip() else grade_one(str(a), it)
            result[it["id"]] = {"pass": why is None, "why": why}
            if why is None:
                p += 1
            else:
                fails.append((it["id"], why))
        rows.append((d.name, p, len(items)))
    print(f"{'skill':38} {'pass':>9}")
    tp = tn = 0
    for name, p, n in rows:
        tp, tn = tp + p, tn + n
        print(f"{name:38} {p:4}/{n:<4}")
    print(f"{'TOTAL':38} {tp:4}/{tn:<4}")
    if fails:
        print("\nFAILING ITEMS")
        for iid, why in fails:
            print(f"  {iid}: {why}")
    if out:
        Path(out).write_text(json.dumps(result, indent=1))
    return 0 if not fails else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("selftest")
    s.add_argument("--skill", nargs="*")
    s.add_argument("--skip-missing-sources", action="store_true",
                   help="skip (and count) citations whose off-repo alias directory does not exist")
    g = sub.add_parser("grade")
    g.add_argument("answers")
    g.add_argument("--skill", nargs="*")
    g.add_argument("--out")
    a = ap.parse_args()
    if a.cmd == "selftest":
        global SKIP_MISSING_SOURCES
        SKIP_MISSING_SOURCES = a.skip_missing_sources
        return selftest(a.skill)
    return grade(a.answers, a.skill, a.out)


if __name__ == "__main__":
    sys.exit(main())
