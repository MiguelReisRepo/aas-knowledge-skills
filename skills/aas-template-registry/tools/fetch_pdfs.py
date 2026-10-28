#!/usr/bin/env python3
"""Mirror the specification PDFs of github.com/admin-shell-io/submodel-templates.

Usage: fetch_pdfs.py <cache dir>

Writes into the cache dir:
  tree.json            the repository tree (GitHub API, main branch)
  published_pdfs.json  every PDF path under published/
  pdf/<path>           each PDF, downloaded from raw.githubusercontent.com

Already downloaded PDFs are kept. Then run extract_tables.py from the same dir.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import urllib.parse

REPO = "admin-shell-io/submodel-templates"


def main() -> None:
    cache = sys.argv[1]
    os.makedirs(cache, exist_ok=True)
    os.chdir(cache)
    subprocess.run(["curl", "-sfL", "-o", "tree.json",
                    f"https://api.github.com/repos/{REPO}/git/trees/main?recursive=1"], check=True)
    tree = json.load(open("tree.json"))
    if tree.get("truncated"):
        raise SystemExit("the GitHub tree listing is truncated; the PDF list would be incomplete")
    pdfs = sorted(x["path"] for x in tree["tree"]
                  if x["type"] == "blob" and x["path"].startswith("published/") and x["path"].lower().endswith(".pdf"))
    json.dump(pdfs, open("published_pdfs.json", "w"), indent=1)
    ok, failed = 0, []
    for p in pdfs:
        dst = os.path.join("pdf", p)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        if os.path.exists(dst) and os.path.getsize(dst) > 1000:
            ok += 1
            continue
        url = f"https://raw.githubusercontent.com/{REPO}/main/{urllib.parse.quote(p)}"
        r = subprocess.run(["curl", "-sL", "-o", dst, "-w", "%{http_code}", url], capture_output=True, text=True)
        if r.stdout.strip() == "200" and os.path.getsize(dst) > 1000:
            ok += 1
        else:
            failed.append(p)
    print(f"{len(pdfs)} PDFs listed, {ok} present, {len(failed)} failed")
    for p in failed:
        print("  failed:", p)
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
