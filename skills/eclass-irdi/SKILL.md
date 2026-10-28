---
name: eclass-irdi
description: ECLASS / IEC CDD IRDI grammar and IDTA conventions — the transversal reference card for every semanticId that starts with digits instead of https. Covers IRDI anatomy per ISO/IEC 11179-6 / ISO 29002-5 (RAI#DI#VI, the 01/02/05/07 code-type prefixes, the `#00Z` version suffix), the IEC CDD slash form (0112/2///61360_4#…), how to tell IRDI from IRI, the IDTA primary-vs-supplemental pairing conventions (IEC CDD primary + ECLASS supplemental vs ECLASS-as-primary), version-suffix drift between template revisions, ECLASS Release re-keying (all DIs change, not just versions), printed-PDF anomalies (the '~0' infix, cdp-URL-only rows), the eclass-cdp '#'→'-' URL convention, the URL-encoding trap (# → %23), where to verify an IRDI (cdp.eclass-cdp.com / cdd.iec.ch), the frozen-map discipline, and the ECLASS licensing boundary. Use this skill whenever the user works with an IRDI, mentions ECLASS or IEC CDD, pastes a 0173-1#… or 0112/2///61360… identifier, asks "is this semanticId an IRDI or an IRI", wires ConceptDescription dictionary entries, debugs a supplementalSemanticId, migrates a template across ECLASS Releases (re-keying), or writes IRDI validation or IRDI catalogue code. This skill carries NO bundled PDF and NO frozen map — its ground truth is ISO 11179-6/29002-5 grammar, the verbatim evidence frozen in the sibling skills' maps (aas-nameplate, aas-handover), and the live registries. It deliberately does NOT reproduce ECLASS dictionary content (licensed).
---

# ECLASS / IEC CDD IRDI — grammar, conventions, pitfalls

The transversal reference for **IRDIs** (International Registration Data
Identifiers) as they appear in AAS/IDTA work: what the string means, how IDTA
templates deploy them, and the bug classes they breed. Unlike the per-template
skills, there is **no bundled PDF and no frozen map here** — nothing to freeze.
Ground truth is (a) ISO/IEC 11179-6 / ISO 29002-5 grammar, (b) verbatim
evidence already frozen in [[aas-nameplate]] `semanticid-map-3-0-1.json` and
[[aas-handover]] `semanticid-map-2-0.json`, (c) the live registries
(cdp.eclass-cdp.com, cdd.iec.ch). **This skill must never grow a copy of the
ECLASS dictionary** — grammar and conventions only (see Licensing).

Companion to [[iec61360]] (the ConceptDescription/data-spec side),
[[aas-nameplate]] / [[aas-handover]] (the two frozen evidence bases),
[[aas-submodel-templates]] (which template uses which id style), and
[[aas-knowledge]].

## 1. IRDI anatomy — `RAI#DI#VI`

An IRDI is three `#`-separated parts (ISO/IEC 11179-6; resolution per ISO
29002-5): **Registration Authority Identifier # Data Identifier # Version**.
The AAS spec bases the IRDI scheme on "ISO29002-5, ISO IEC 6523 and ISO IEC
11179-6" (IDTA-01001 v3.0 PDF p.29, §4.3.3).

```
0173-1#02-AAO677#002
└─┬──┘ └───┬───┘ └┬─┘
  RAI      DI     VI
```

- **RAI** `0173-1` — ICD `0173` (ISO 6523 code for ECLASS) + organization part
  `1`. Every ECLASS IRDI starts `0173-1`.
- **DI** `02-AAO677` — a 2-digit **code-type prefix** + `-` + the **6-char
  data identifier** (uppercase letters/digits). The prefix tells you WHAT is
  identified:
  | prefix | identifies | example (verbatim from the frozen maps) |
  |---|---|---|
  | `01-` | classification class | `0173-1#01-AHF578#003` (HandoverDocumentation submodel) |
  | `02-` | property | `0173-1#02-AAO677#004` (ManufacturerName) |
  | `05-` | unit | (units of measure — see [[iec61360]] unitId) |
  | `07-` | value / enumeration entry | `0173-1#07-ABU490#003` (VDI 2770 class "03-02 Operation"); CE marking value `0173-1#07-DAA603#004` |
- **VI** `#002` — 3-digit version suffix. **The same DI with a different VI is
  a different revision of the same concept** — and templates DO bump it (see
  version-suffix drift below).

**IEC CDD form** (ICD `0112`, slash-separated RAI):
`0112/2///61360_4#AAA000#001` — `0112` = IEC, `/2` = CDD, `///` empty
sub-fields, then the source database (`61360_4`, `61987`, `61360_7` in the
Nameplate map) before the usual `#DI#VI`. Real examples:
`0112/2///61987#ABA565#009` (ManufacturerName primary),
`0112/2///61360_7#AAS006#001` (Markings SML primary).

**ECLASS pair form** — IDTA prints SMC/SML semanticIds as a property-IRDI +
class-IRDI joined by `/`:
`0173-1#02-ABI500#003/0173-1#01-AHF579#003` (Document SMC). And sometimes the
class IRDI ALONE: `0173-1#01-AHD205#004` (GuidelineSpecificProperties__00__ —
deliberately different from its containing SML's pair). The pair is ONE
semanticId string; do not split it into two keys.

**IRDI vs IRI — the 2-second test:** starts with `https://` or `urn:` → IRI.
Starts with digits and contains `#` → IRDI (`/` inside digits = IEC CDD slash
form, still not an IRI — no scheme). Both are legal `GlobalReference` values;
neither is "wrong" per se — which one is REQUIRED depends on the template (§2).

**URL-encoding trap:** `#` is the URI fragment delimiter. An IRDI pasted raw
into a query param silently truncates at the first `#` — always encode
(`#`→`%23`): `?semanticId=0173-1%2302-AAO677%23002`. ECLASS CDP deep links
avoid the problem by substitution: the printed supplementals use
`https://api.eclass-cdp.com/<IRDI with '#'→'-'>`, e.g. `0173-1#02-ABI501#003`
→ `https://api.eclass-cdp.com/0173-1-02-ABI501-003`. That `-` form is a URL
convention, NOT an alternative IRDI spelling — never store it as the IRDI.

## 2. THE IDTA CONVENTIONS (the load-bearing part)

### Primary vs supplemental — two patterns, check the PDF's two-row layout

- **Newer templates (Nameplate 3.0.1 pattern):** IEC CDD IRDI is the PRIMARY
  semanticId, ECLASS IRDI is the SUPPLEMENTAL. Verbatim:
  ManufacturerName primary `0112/2///61987#ABA565#009`, supplemental
  `0173-1#02-AAO677#004`; URIOfTheProduct primary `0112/2///61987#ABN590#002`,
  supplemental `0173-1#02-ABH173#003`.
- **Older/other templates (Handover 2.0 pattern):** ECLASS IRDI IS the
  primary — the submodel semanticId itself is `0173-1#01-AHF578#003`, and the
  printed supplemental is the eclass-cdp URL
  (`https://api.eclass-cdp.com/0173-1-02-ABI500-003` for Documents).
- **The trap:** a single ECLASS IRDI in a template table is often the
  SUPPLEMENTAL when an IEC CDD primary exists — the PDF prints them as two
  rows per element. A parser/template that emits the ECLASS IRDI as the
  primary of a Nameplate-3.0 element has flipped the pair. Exceptions exist WITHIN one template: Nameplate 3.0.1's
  AssetSpecificProperties has NO IEC CDD primary — the ECLASS pair IS the
  primary. Per-element, not per-template — read the row.

### Version-suffix drift (same DI, bumped #00Z)

Template revisions bump the VI while the DI stays put:
`0173-1#02-AAO677#002` (Nameplate 2.0) → `#004` (3.0.1);
`0173-1#02-AAM985#002` → `#004`. **Real bug:** FirmwareVersion — a production
parser carried `0173-1#02-AAM985#003` while the 3.0.1 template says `#004`
(the parser lagged the template; 3.0.1 bug fix #123 territory). A VI mismatch
is silent: nothing crashes, cross-document matching just stops working.

**Why it breaks matching — Part 1's matching strategies** (IDTA-01001 v3.0 PDF
p.34, §4.4.1). The DEFAULT is exact matching: "two semantic IDs need to be
string-identical", so `…AAO677#002` and `…AAO677#003` do NOT match. Only
"intelligent matching" that ignores versioning treats them as equal, which is
safe for ECLASS because "ECLASS rules ensure that the semantics is always
backward compatible for new versions; a new IRDI would be created for breaking
changes". Cross-dictionary equivalences need explicit mapping data: Part 1's
own IEC CDD ↔ ECLASS example (`0112/2///61360_4#AAE530` ↔
`0173-1#02-AAI048#004`, battery nominal capacity) "does not represent an
existing semantic mapping; it is only a candidate" — never rely on it.

### Release re-keying (ALL DIs change — not versions)

ECLASS Releases can re-key EVERY IRDI of a template revision. Handover
v2.0 moved to **ECLASS Release 15, non-backward compatible with 1.2 (Annex C
change #2)** — every DI changed, not just VIs: 1.2-era
`0173-1#02-AAY813#001` (Language) / `0173-1#02-AAY814#001` (DocumentVersionId)
vs 2.0 `0173-1#02-AAN468#008` (Language) / `0173-1#02-AAP003#005` (Version).
**Never assume an old IRDI is "the same concept, older version"** — a
different DI is a different dictionary entry; bumping the VI of an old DI
fabricates an identifier. Migration = re-key every element from the new PDF.

### Printing anomalies in official PDFs — copy VERBATIM + warn, never "fix"

Frozen, binary-verified examples from the sibling maps:
- **The `~0` infix** — Handover's Document supplemental prints
  `0173-1#02-ABI500#003~0/0173-1#01-AHF579#003` (PDF p.10, verified in the
  binary). Not valid IRDI grammar; copied verbatim into the map with a
  warning.
- **cdp-URL-only row** — OrganizationShortName prints ONLY
  `https://api.eclass-cdp.com/0173-1-02-ABI002-003` — no IRDI at all (every
  sibling prints both). The pattern-expected IRDI `0173-1#02-ABI002#003` is
  recorded as a GUESS pending the official AASX, not as fact.
- **Line-break hyphen loss** — Nameplate prints `0173-1#02AAM985#004`
  (hyphen eaten at a line break); normalized WITH a note in the map.
- **Duplicate-concept smell** — SoftwareVersion's supplemental prints
  IDENTICAL to FirmwareVersion's (`AAM985#004`; expected lineage `AAM737`).
  Copied verbatim + flagged VERIFY.

The rule: the map records what the PDF PRINTS. Anomalies get a `warnings`
entry and a VERIFY flag against the official template AASX — hand-"fixing" an
anomaly invents an identifier that exists nowhere.

## 3. Verification workflow

**Where to check an IRDI** (do not trust memory — including this skill's):
- **ECLASS:** public search at `https://cdp.eclass-cdp.com` (ECLASS
  ContentDevelopmentPlatform); the per-IRDI deep link is the `#`→`-` form
  under `api.eclass-cdp.com` (§1). Note WHICH Release you are reading.
- **IEC CDD:** `https://cdd.iec.ch` (free browsing of IEC 61360-4/61987/…
  databases).
- **The template itself:** the LIVE official IDTA PDF + its published AASX —
  for template work these outrank both registries, because the template
  fixes the exact VI (and carries the anomalies).

**Frozen-map discipline** (how the sibling skills kill this bug class): skill
extracts every semanticId VERBATIM from the official IDTA PDF → frozen JSON
map next to the SKILL.md → copied byte-identical into the application → **no
hand-typed IRIs/IRDIs anywhere in code**. Every anomaly is a `warnings` entry,
every unprintable value a `VERIFY-IN-PDF` marker. A new template skill that
hand-types its table has already failed.

**Guardrails worth copying:**
- A consistency test that no field emits an IRDI conflicting with the template.
- **The template being right does NOT save the parser.** When a template
  module and an extraction parser emit independently, both must be verified
  (the FirmwareVersion `#003` vs `#004` lag lived exactly in that gap; a
  flat-handover block was seen emitting wrong-CONCEPT IRDIs:
  Title→`0173-1#02-AAU731#003` = Nameplate ManufacturerProductFamily).
- Curation policy for any IRDI catalogue: only verifiable entries; when
  uncertain leave the IRDI OFF — "a missing IRDI is a known gap; a wrong IRDI
  corrupts every downstream consumer".

## 4. KNOWN NOTES — IRDI validator pitfalls

What a naive IRDI validator gets wrong (each one seen in a real implementation):
- **The IEC CDD slash form** (`0112/2///61360_4#AAA000#001`) contains `/`; a
  validator that treats anything with `/` as "not an IRDI" leaves the form used
  by every Nameplate-3.0 PRIMARY unvalidated. Give it its own pattern.
- **The ECLASS pair form** (`0173-1#02-ABI219#003/0173-1#01-AHD205#004`, printed
  as ONE semanticId for SMCs/SMLs) fails a single-IRDI pattern for the same reason;
  validate both halves.
- **Parser and pattern must agree** on the DI length (ECLASS DIs are 6 chars; a
  pattern allowing 4..8 and a parser requiring 6 disagree).
- **Name the parts as ISO 11179 does**: in `0173-1#02-AAM985#004` the RAI is
  `0173-1`, the DI is `02-AAM985` (code-type prefix included), the VI is `004`.
- **Casing and paste damage**: ECLASS prints uppercase DIs; repair or reject
  `%23` for `#`, PDF hyphen loss and the `~0` anomaly instead of passing them.

## 5. Licensing — the boundary

**ECLASS dictionary content is licensed.** The line these skills hold:
- ✔ Carrying IRDI strings that appear VERBATIM in public IDTA template PDFs,
  citing the template as source (that is what the frozen maps do — their
  `source` field names the PDF and tables).
- ✔ Naming grammar, code-type prefixes, Release mechanics, and where to look
  things up.
- ✘ Bundling, scraping, or reproducing the ECLASS dictionary itself —
  preferredNames/definitions/units en masse, class trees, or "the ECLASS
  properties for class X" dumps. A lookup NEED is answered with a CDP/CDD
  pointer, not a copy. (Same policy for any curated IRDI catalogue: small, curated,
  per-entry citations — not a mirrored dictionary.)

## 6. Sign-off checklist (before shipping anything IRDI-touching)

1. **IRDI or IRI?** Scheme prefix → IRI; digits+`#` → IRDI; `0112/2///` →
   IEC CDD IRDI (don't let a `/` fool a validator — see KNOWN NOTES).
2. **Primary or supplemental?** Checked the template PDF's two-row layout for
   THIS element — not assumed from the template's general pattern?
3. **Which ECLASS Release?** Same-DI-different-VI = revision; different DI =
   re-keyed Release or different concept. No fabricated "older versions".
4. **VI matches the LIVE template PDF?** (FirmwareVersion `#003`-vs-`#004`
   class of lag.)
5. **Parser AND template both updated?** (bug class #16 — verify both
   emitters + `parser-irdi-consistency` green.)
6. **Anomalies copied verbatim with a warning**, VERIFY-flagged against the
   official AASX — nothing hand-"fixed"?
7. **Pair form kept as ONE string**; cdp `-` URL never stored as the IRDI;
   `#` encoded as `%23` in any query param.
8. **No ECLASS dictionary content** copied beyond what the cited IDTA PDF
   prints.
