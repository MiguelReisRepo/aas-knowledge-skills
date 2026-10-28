---
name: aas-template-registry
description: Per-template registry of the published IDTA submodel templates (155 template versions, built 2026-10-06) — for every element, its cardinality as the template JSON declares it, as the specification PDF table declares it (with page), the EFFECTIVE cardinality, and prose rules from the PDFs with literal quotes. Use it whenever a question depends on whether an element of an IDTA template is mandatory or optional (a "required but empty" finding, a test oracle, a sweep, a flow's expected findings, filling a template for a test), when the JSON and the PDF disagree, when a template has several JSON files per version, or when the registry must be rebuilt after the template catalogue changes. Compose with aas-submodel-templates (which template for which job) and the per-template deep skills.
---

# IDTA template registry

One question this answers without opening a PDF: **is this element of this
template mandatory, and on what evidence?**

```
registry/index.json                     one row per template version (file, card, PDF, status counts)
registry/<Template>/<version>.json      every element: path, type, semanticId, JSON card, PDF match, effective, status
registry/<Template>/<version>.md        the same as a readable table
registry/divergences.json + DIVERGENCES.md   the 227 elements where JSON and PDF disagree (194 before the 2026-10-28 extraction fix; 127 in the 103 versions of 2026-09-17)
prose-rules.json                        requirements stated in PDF prose, not in any table
tools/                                  fetch_pdfs.py, extract_tables.py, build_registry.py
```

## Lookup procedure

1. Find the template version in `registry/index.json` by `template` (the catalogue
   title, e.g. `Contact Information`) and `version`. Several JSON files per version
   exist upstream (Template, Sample, `_forAASMetamodelV3.1`, `without_examplevalues`);
   the registry uses one per version, chosen by a fixed preference (see "Which JSON" below),
   named in the card's `Template JSON` line with its git blob.
2. Open the card (`.md`) or the record (`.json`) and find the element by `path`
   (`Parent > Child`, list children by idShort, or `[i]` when they have none).
3. Use `effective`. Read `status` before trusting it:

| status | meaning | effective |
|---|---|---|
| `agree` | JSON and PDF table give the same cardinality | that value |
| `divergent` | they disagree; the PDF row matched by semanticId AND an exact idShort cell | the less strict of the two |
| `unverified` | a PDF row matched only by semanticId, or ambiguously (several cardinalities) | the JSON value |
| `json-only` | no PDF row found for the element | the JSON value |
| `pdf-only` | the JSON has no cardinality qualifier; the PDF row matched with high confidence | the PDF value (informative, see limits) |
| `none` | neither source gives one | none |

4. Then check `prose-rules.json` for the template: some requirements exist only in
   PDF prose (e.g. the four mandatory address MLPs of the Digital Nameplate).

## The effective rule: literal evidence versus our decision

**Literal (IDTA):**
- Both artefacts are official. Repository README: *"The published folder contains
  Submodel Templates that are officially released and registered by IDTA."* The
  folder holds the JSON and the PDF side by side; the README states no precedence.
- The PDFs do. Annex A ("Explanations on used table formats", 1. General) of almost
  every template (77 of the 79 PDF texts on disk; not 02007-1-0, 02012-1-0) says the
  tables *"do not convey all information on Submodels and SubmodelElements. For this
  purpose, the definitive definitions are given by a separate file in form of an AASX
  file of the Submodel template and its elements."* (e.g. IDTA 02010-1-0 p.19). The
  sentence names the template AASX; the JSON beside it in the folder is not mentioned.
- What a cardinality means. IDTA 02010-1-0, p.19: *"The cardinality is defined with
  0…1: optional; 1: mandatory 1 entry; 1…n: mandatory 1 to many entries; 0…n:
  optional to many entries"*. It counts occurrences of the element within its
  parent. It does not say a value must be filled in.

**Our decision, not IDTA's:**
- When JSON and PDF diverge, the less strict applies (min of the minimums, max of
  the maximums). Annex A instead names the template AASX as definitive; this rule is ours. A requirement blocks a user only when both official sources make
  it. Each divergence is kept as a candidate IDTA issue.
- Only `divergent` rows with high confidence change a consuming editor's behaviour.
  `unverified` and `json-only` keep the JSON value; `pdf-only` is informative.
- An unused optional part requires nothing (option 1): if an element's effective
  cardinality starts with `0` and it holds no value anywhere inside, nothing inside
  it is required.
- A mandatory element must also carry a value (team rule `template-value-required`). That is ours, not the cardinality's.

Never present an effective value as "the IDTA rule". Say which source it came from.

## Verified JSON-vs-PDF divergences (read in the official files, not the registry)

Divergence runs both ways — sometimes the JSON is stricter, sometimes the PDF. Examples
(JSON = `idta-pdfs/json/published/<Template>/<version>/…json`, PDF = the txt extract):

| Template / element | JSON | PDF table |
|---|---|---|
| AID 1.1 `EndpointMetadata/contentType` | `Cardinality` **One** (L322-349) | **0..1** (Table 4, p.17) |
| AID 1.1 forms `htv_methodName` | **ZeroToOne** (L4441-4468) | **1** (Table 23, p.50) |
| AID 1.1 `oauth2_sc/flow` | **ZeroToOne** (every example interface) | **1** (Table 42, p.67) |
| AID 1.1 forms `bacv_useService` | **One** (L23075-23102) | **0..1** (p.56) |
| Carbon Footprint 1.0 / 1.0.1 `GoodsHandoverAddress` | `SMT/Cardinality` **ZeroToOne** (1.0 JSON L470 ff.) | **1** (Table 4, p.18) |
| Service Request Notification 1.0 Entity `RelatedAsset` | `Cardinality` **One** (L378) | **1..*** (Table 3, p.13) |

AID 1.2 resolves all four AID rows in favour of the PDF: its JSON has `contentType`
ZeroToOne (L264-285), `htv_methodName` One, `flow` One, `bacv_useService` ZeroToOne, with
qualifier type `SMT/Cardinality` (1.1: `Cardinality`). Record each divergence against its
exact template version and JSON file.

## Prose rules (`prose-rules.json`)

Each entry has `templates`, `pdf`, `page`, a literal `quote` and the `effect` we
derive from it. Current entries:
- `02006-3.2-address`: Digital Nameplate 3.0.x, AddressInformation gets Street,
  Zipcode, CityTown, NationalCode (p.11).
- `02035-1-3.2-address`: Battery Passport Part 1 Digital Nameplate, the same four;
  Email and AddressOfAdditionalLink are "if available", so optional (p.12).
- `02010-2.1-contact-information`: Service Request Notification takes its
  ContactInformation content from IDTA 02002 (p.9).
- `02002-table3-isCaseOf`: SMC ContactInformation is ECLASS `0173-1#02-AAQ837`
  (p.11), which is how an empty ContactInformation SMC in another template is recognised.

Add an entry only with a literal quote and a page. An inference goes in `effect`,
labelled as ours.

## Which JSON

The official repository can hold several files for one template version. The
registry prefers, in order: not a Sample/Example/GenericForm, the
`_forAASMetamodelV3.1` variant, not `without_examplevalues`. Inside ONE version folder
the V3.1 variant is JSON-identical to its base file in 37 of the 38 pairs; Production
Calendar 1.0 differs (measured 2026-10-28 over `idta-pdfs/json/published`, canonical
`json.dumps(sort_keys=True)` comparison). Across versions there is no such identity, and
the submodel semanticId FORM can change: `Hierarchical Structures enabling Bills of
Material/1/1/IDTA 02011-1-1_Template_HSEBoM.json` writes
`ExternalReference[GlobalReference …/HierarchicalStructures/1/1/Submodel]`, while
`…/1/1/2/IDTA 02011-1-1-2_Template_HSEBoM_forAASMetamodelV3.1.json` (and both 1.1.1
files) write `ModelReference[Submodel …/HierarchicalStructures/1/1/Submodel]`. So a
newer patch, or the variant the picker prefers, is not interchangeable with an older
base file on reference form.

### semanticId reference form

Many IDTA template JSONs ship the SUBMODEL semanticId as a `ModelReference` with one
`Submodel` key whose value is the concept IRI/IRDI (e.g. Technical Data 2.0.1
`0173-1#01-AHX837#002`, Production Calendar 1.0, AIMC 1.0.x, HSEBoM 1.1.1/1.1.2). It
occurs in base files too, not only in V3.1 variants: 103 of the 188 submodels in the
local `idta-pdfs/json/published` mirror (all files, Samples included; measured
2026-10-28). Over the pinned catalogue (155 template versions) it is 85 versions, 94
submodels (the MTP files carry four each).
- It is VALID. No AASd constraint requires a semanticId to resolve; AASd-121..128/137
  constrain key structure only (see aas-validation, settled non-violations).
- Since 3.1 no form is recommended for a semanticId. IDTA-01001 v3.1.2 change notes
  (p.197, "Changes V3.1 vs. V3.0.2"): "REMOVED: remove recommendation to use external references for semanticId (#376) and related attributes like valueId, semanticIdListElement and isCaseOf". aas-core-meta v3.1 still carries the
  older note in `Has_semantics.semantic_ID` (`aas-core-meta-v3_1.py:1476`, also :1486):
  "It is recommended to use a global reference."; the PDF is the normative text. For a
  submodel of kind Instance the PDF only says (p.157) "Typically, the semanticId is an
  external reference to an external standard defining the semantics of the submodel."
- A tool may normalise it to `ExternalReference[GlobalReference <same value>]`. Do not
  report it as an error, and do not convert a ModelReference whose key is a
  ConceptDescription, one with several keys, or one that names another submodel of
  the environment.

## Regenerate (after the template catalogue or the PDFs change)

```bash
# 1. PDFs (cache outside any repo; ~111 PDFs)
python3 tools/fetch_pdfs.py <pdf-cache-dir>
cd <pdf-cache-dir> && python3 <skill>/tools/extract_tables.py   # writes pdf_card_rows.json (PyMuPDF find_tables)
# 2. registry (catalogue = JSON list of {idShort, version, name, path, sha, jsonData}
#    for the template JSON files of the official repository)
cd <skill> && python3 tools/build_registry.py \
  --catalogue <catalogue.json> \
  --pdf-rows <pdf-cache-dir>/pdf_card_rows.json \
  --pdfs <pdf-cache-dir>/published_pdfs.json \
  --pdf-dir <pdf-cache-dir>/pdf
```
`pdf_card_rows.json` comes from `extract_tables.py`, which
reads `published_pdfs.json` and `pdf/` from the working directory.

## Limits (say them when you use the registry)

- **Table extraction is heuristic.** A row is matched by semanticId (whitespace
  removed, longer than 12 chars) and an idShort cell equal to the element's idShort
  after stripping a `[SML]`-style prefix and footnote digits. `extract_tables.py`
  rebuilds logical rows: where PyMuPDF returns one physical row per text line (IDTA
  02035-7 and others), the lines up to the next type marker or cardinality are joined
  per column, so an idShort wrapped over lines ("RenewableCo" + "ntent") or a
  semanticId wrapped mid-word still matches. A wrapped idShort that lost one inner
  character to the next column ("SeparateColl" + "ction") matches only when no row
  of that semanticId has the exact idShort. Rows split across pages, merged cells or
  idShorts written differently in the PDF still fall to `unverified` or `json-only`.
- **Citations.** A `high` match stores the row (`pdf.row`: PDF page, type marker,
  idShort, semanticId, card.) and each record stores the literal Annex A sentences of
  its PDF with their PDF page (`pdf.annexA`: "The table heads abbreviate 'cardinality'
  with 'card'.", the "definitive definitions ... AASX file" sentence, and the
  cardinality notation where the PDF defines it), so a finding can cite the template's
  own specification instead of another template's convention.
- **`unverified` (817) and `json-only` (2215) are not confirmed by a PDF.** They use
  the JSON value. Do not call them "checked against the PDF".
- **`pdf-only` (113) is informative.** Do not add a requirement the JSON
  does not carry.
- **Bug-fix releases without their own PDF** use the nearest ancestor folder's PDF;
  the card says so (`ancestor folder`).
- **Presence is not checked here.** Cardinality says how many occurrences may exist;
  an absent mandatory element is a separate presence check, not this registry's.
- Status totals at build time (2026-09-17, 103 versions): agree 4861, json-only 2078,
  unverified 821, divergent 127, none 115, pdf-only 68.
- Rebuilt 2026-10-06 (155 versions, 111 PDFs): agree 7877, json-only 4168, unverified
  1598, divergent 194, none 191, pdf-only 97.
- Rebuilt 2026-10-28 with the logical-row extraction (same 155 versions, 111 PDFs, 7255
  card rows): agree 10578 (+2701), json-only 2215 (-1953), unverified 817 (-781),
  divergent 227 (+33), none 175 (-16), pdf-only 113 (+16). No element moved away from
  `agree` or `divergent`; 29 effective cardinalities changed (all to the less strict
  value of a newly found divergence). Example: Digital Battery Passport / Circularity
  1.0.2 went from 37 json-only to 31 agree, 5 unverified, 1 json-only. The old tools on
  the old rows reproduce the 2026-10-06 registry byte for byte; the new tools on the
  old rows give the same counts (the fuzzy idShort rule changes nothing there).

## Who uses it

- `aas-validation`: whether a "required but empty" finding is backed by both sources.
- Test oracles: expected findings per template, and what to fill to reach a valid document.
