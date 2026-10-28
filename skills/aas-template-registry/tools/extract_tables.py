# Extract every table row that carries a cardinality from the IDTA template PDFs,
# with its page number, into pdf_card_rows.json. PyMuPDF find_tables.
#
# Logical rows: in several IDTA PDFs (e.g. IDTA 02035-7 1.0.1 and 1.0.2) find_tables returns ONE physical row per
# text line, so an element row comes back as
#   ['[Prop]', 'urn:samm:io.admin-', '[Float]', '1']
#   ['', 'shell.idta.batterypass.circularity:1.0.0#renewableContent', '', '']
#   ['RenewableCo', '', None, None]
#   ['ntent', 'supplementalSemanticId: ...', None, None]
# Only the first line carries the cardinality, so keeping physical rows lost the idShort ("RenewableCo" + "ntent")
# and the end of the semanticId. A logical row starts at a line that carries a cardinality or whose first cell is a
# type marker ("[SMC]", "[Prop]", ...); the following lines of the same table are appended column by column until
# the next start. Matching (build_registry.py) removes whitespace, so "RenewableCo ntent" equals "RenewableContent".
#
# Usage: run in the PDF cache folder (reads published_pdfs.json and pdf/), or pass the cache folder and an output
# file: python3 extract_tables.py [<pdf-cache-dir> [<out.json>]]
import fitz, json, os, re, sys
BASE = sys.argv[1] if len(sys.argv) > 1 else '.'
OUT = sys.argv[2] if len(sys.argv) > 2 else os.path.join(BASE, 'pdf_card_rows.json')
pubs = json.load(open(os.path.join(BASE, 'published_pdfs.json')))
CARD = re.compile(r'^\[?\s*(0|1)\s*(\.\.|…|\.\.\.)\s*(1|\*|n|N)\s*\]?$|^\[?\s*1\s*\]?$')
TYPE = re.compile(r'^\[[A-Za-z][^\]]*\]')


def norm(s):
    s = re.sub(r'\s+', '', s).strip('[]').replace('…', '..').replace('...', '..')
    return {'0..1': '0..1', '0..*': '0..*', '0..n': '0..*', '0..N': '0..*', '1..*': '1..*', '1..n': '1..*', '1..N': '1..*', '1': '1'}.get(s)


def card_of(cells):
    for c in reversed(cells):
        if c and CARD.match(re.sub(r'\s+', '', c)):
            return norm(c)
    return None


def logical_rows(physical):
    """Group the physical lines of one table into logical element rows (see the header)."""
    out, cur = [], None
    for cells in physical:
        card = card_of(cells)
        starts = bool(cells and cells[0] and TYPE.match(cells[0]))
        if card is not None and cur is not None and cur['card'] is None and not starts:
            starts = False  # the cardinality of a row that started on a type-marker line
        elif card is not None:
            starts = True
        if starts or cur is None:
            if cur is not None:
                out.append(cur)
            cur = {'cols': [[c] if c else [] for c in cells], 'card': card}
            continue
        for i, c in enumerate(cells):
            while len(cur['cols']) <= i:
                cur['cols'].append([])
            if c:
                cur['cols'][i].append(c)
        if cur['card'] is None and card is not None:
            cur['card'] = card
    if cur is not None:
        out.append(cur)
    return [r for r in out if r['card']]


out = {}
for p in pubs:
    doc = fitz.open(os.path.join(BASE, 'pdf', p))
    rows = []
    for i, page in enumerate(doc):
        try:
            tables = page.find_tables().tables
        except Exception:
            continue
        for t in tables:
            physical = [[re.sub(r'\s+', ' ', str(c or '')).strip() for c in r] for r in t.extract()]
            for lr in logical_rows(physical):
                cells = [' '.join(col) for col in lr['cols']]
                rows.append({'page': i + 1, 'card': lr['card'], 'text': ' | '.join(cells)[:1200], 'flat': re.sub(r'\s+', '', ' '.join(cells))})
    out[p] = rows
    print(p, len(rows), file=sys.stderr, flush=True)
json.dump(out, open(OUT, 'w'))
print('done', sum(len(v) for v in out.values()))
