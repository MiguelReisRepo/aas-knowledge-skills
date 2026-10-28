---
name: aas-handover
description: Asset Administration Shell Handover Documentation expertise — the IDTA-02004 "Handover Documentation" submodel template, v2.0 (June 2025), based on VDI 2770 Blatt 1:2020. Covers the complete Document SMC tree (Documents SML → Document → DocumentIds/DocumentId, DocumentClassifications/DocumentClassification, DocumentVersions/DocumentVersion, DocumentedEntities), every ECLASS Release-15 semanticId verbatim, the mandatory VDI 2770 classification system (the 12 official ClassIds 01-01 Identification … 04-01 Contract documents, ClassificationSystem="VDI 2770 Blatt 1:2020"), DocumentVersion's heavy mandatory set (Language SML, Version, Title, Description, StatusValue/StatusSetDate, Organization names, DigitalFiles), the DigitalFile/PreviewFile in-package vs external-link semantics (PDF/A per ISO 19005), the 1.2→2.0 non-backward-compatible renames (DocumentVersionId→Version, Summary→Description, ValueId→DocumentIdentifier), and the frozen machine map semanticid-map-2-0.json. Use this skill whenever the user models or hands over asset documentation — manuals, certificates, CE/ATEX declarations, drawings, spare-parts lists — builds/reviews/migrates a HandoverDocumentation submodel, mentions IDTA-02004, VDI 2770, Document/DocumentVersion/DocumentClassification, DocumentId, DigitalFile/PreviewFile, File attachments in .aasx packages. ALWAYS read the bundled official IDTA-02004 PDF first (see the mandatory step below) — this skill is a map, the PDF is the law.
---

# AAS Handover Documentation (IDTA-02004 v2.0)

The canonical reference for modelling an asset's **handover documentation** —
manuals, certificates, declarations of conformity, drawings, spare-parts lists —
as an AAS submodel: IDTA-02004 *"Handover Documentation"*, version 2.0 (June
2025), built on **VDI 2770 Blatt 1:2020**. It is the submodel a machine
manufacturer hands to the operator so the documentation auto-integrates into the
customer's document-management system — and the template whose **1.2 → 2.0 drift
is common in real implementations** (see "Implementation drift" below). The frozen `semanticid-map-2-0.json` next to
this file exists to kill that bug class.

**Latest release: 2.0.1 (2025-11-03), a bug-fix of 2.0** (2.0.1 PDF p.2, Annex C
p.22): issue #196 — `ClassName`'s displayName had "en" twice (invalid); the
"Klassenname" LangString is now "de"; issue #147 — two typos in the document. The
structure and semanticIds below are unchanged, so the 2.0 tree applies to 2.0.1.

Companion to [[aas-submodel-templates]] (the template map), [[aas-knowledge]]
(metamodel), [[aas-validation]] (AASd-*), [[aasx-format]] (the OPC package side
of File attachments), and [[aas-bom]] (Entity/globalAssetId conventions shared
by the Entities list).

## ⚠ MANDATORY FIRST STEP — read the official spec, every time

**Before authoring, editing, reviewing, migrating, or validating ANY Handover
Documentation submodel, you MUST read the bundled official specification** — it
is the ground truth. Memory (yours or this skill's) drifts; the PDF does not.
This very skill was written after the 2.0 PDF exposed real drift in app code
that claims IDTA-02004 conformance.

Read it with the Read tool. The skill bundles TWO copies — read the **text**
extraction (always works; PDF rendering needs poppler which may be absent), and
treat the **PDF** as the authoritative binary:

```
Read: ~/.claude/skills/aas-handover/IDTA-02004-2-0_Submodel_Handover-Documentation.txt   ← always readable
      ~/.claude/skills/aas-handover/IDTA-02004-2-0_Submodel_Handover-Documentation.pdf   ← authoritative (needs poppler)
```
(In the aas-skills repo: `skills/aas-handover/IDTA-02004-2-0_Submodel_Handover-Documentation.{txt,pdf}`.)

It is 31 pages — read Chapter 2 in full (§2.1 approach + file rules, §2.3 the
VDI 2770 class table, §2.4–2.9 the element tables 2–14) and Annex C (the
non-backward-compatible 1.2→2.0 change list). If a claim in this skill and the
spec ever disagree, **the spec wins** — and fix this skill AND the JSON map.

## THE CENTERPIECE — the Document tree (2.0 verbatim, §2.4–2.9)

**The submodel semanticId is an ECLASS IRDI, not an IRI:**
`0173-1#01-AHF578#003` (idShort `HandoverDocumentation`). All element IRDIs are
**ECLASS Release 15** — v2.0 re-keyed EVERY IRDI vs 1.2 (Annex C change #2,
non-backward compatible). Never mix 1.2 ids/idShorts into a 2.0 submodel.

Legend: ● = mandatory. Every ECLASS IRDI below pairs with a printed
supplementalSemanticId at `https://api.eclass-cdp.com/<IRDI with '#'→'-'>`
(e.g. `0173-1#02-ABI501#003` → `https://api.eclass-cdp.com/0173-1-02-ABI501-003`)
— full verbatim strings in `semanticid-map-2-0.json`; exceptions are flagged.

### Structure tree

```
Submodel  idShort=HandoverDocumentation
          semanticId → 0173-1#01-AHF578#003          ← IRDI, NOT an admin-shell.io IRI
  ├─ [SML] Documents ●1                orderRelevant=No, typeValueListElement=SMC,
  │        │                           semanticIdListElement=[GlobalReference,
  │        │                             0173-1#02-ABI500#003/0173-1#01-AHF579#003]
  │        └─ [SMC] Document  [1..*]   ← one per VDI 2770 "Document"
  │             ├─ [SML] DocumentIds ●1
  │             │    └─ [SMC] DocumentId  [1..* — JSON OneToMany; PDF prints no row]
  │             │         ├─ [Prop] DocumentDomainId ●   xs:string
  │             │         ├─ [Prop] DocumentIdentifier ● xs:string   (was ValueId in 1.2)
  │             │         └─ [Prop] DocumentIsPrimary    xs:boolean  0..1
  │             ├─ [SML] DocumentClassifications ●1
  │             │    └─ [SMC] DocumentClassification  [1..* — JSON OneToMany; VDI entry mandatory]
  │             │         ├─ [Prop] ClassId ●              xs:string  (e.g. "03-02")
  │             │         ├─ [MLP]  ClassName ●            EN mandatory
  │             │         └─ [Prop] ClassificationSystem ● xs:string  ("VDI 2770 Blatt 1:2020")
  │             ├─ [SML] DocumentVersions ●1
  │             │    └─ [SMC] DocumentVersion  [1..* — JSON OneToMany; PDF prints no row]
  │             │         ├─ [SML]  Language ●   → [Prop] <ISO 639 code as VALUE>  1..*
  │             │         ├─ [Prop] Version ●    xs:string   (was DocumentVersionId in 1.2)
  │             │         ├─ [MLP]  Title ●  /  Subtitle 0..1
  │             │         ├─ [MLP]  Description ●            (was Summary in 1.2)
  │             │         ├─ [MLP]  KeyWords  0..1
  │             │         ├─ [Prop] StatusSetDate ● xs:date  /  StatusValue ● ("InReview"|"Released")
  │             │         ├─ [Prop] OrganizationShortName ●  /  OrganizationOfficialName ●
  │             │         ├─ [SML]  RefersToEntities / BasedOnReferences / TranslationOfEntities
  │             │         │          0..1 each  → [Ref] child  1..*
  │             │         ├─ [SML]  DigitalFiles ●  → [File] DigitalFile  1..*
  │             │         └─ [File] PreviewFile  0..1   ← DIRECT child, NOT inside DigitalFiles
  │             └─ [SML] DocumentedEntities  0..1  → [Ref] DocumentedEntity  1..*
  └─ [SML] Entities  0..1               orderRelevant=No, typeValueListElement=Entity
       └─ [Ent] Entity  [1..*]          ← supplier parts; co-managed recommended for simple cases
```

### Submodel root (Table 2)

| idShort | Type | Card | semanticId (verbatim) |
|---|---|---|---|
| **Documents** | SML | ●1 | `0173-1#02-ABI500#003` |
| Entities | SML | 0..1 | `https://admin-shell.io/vdi/2770/1/0/EntitiesForDocumentation` |

`Documents` details (Table 3): `orderRelevant=No`,
`semanticIdListElement=[GlobalReference, 0173-1#02-ABI500#003/0173-1#01-AHF579#003]`,
`typeValueListElement=SubmodelElementCollection`.
`Entities` details (Table 4): `orderRelevant=No`, `typeValueListElement=Entity`;
child `[Ent] Entity` 1..* → `https://admin-shell.io/vdi/2770/1/0/EntityForDocumentation`.

### `Document` SMC (Tables 3, 5)

semanticId `0173-1#02-ABI500#003/0173-1#01-AHF579#003`, card **1..***.
Supplementals (verbatim, incl. a printed `~0` infix — see gotchas):
`0173-1#02-ABI500#003~0/0173-1#01-AHF579#003`,
`https://api.eclass-cdp.com/0173-1-02-ABI500-003/0173-1-01-AHF579-003`.

| idShort | Type | Card | semanticId (verbatim) |
|---|---|---|---|
| **DocumentIds** | SML | ●1 | `0173-1#02-ABI501#003` |
| **DocumentClassifications** | SML | ●1 | `0173-1#02-ABI502#003` |
| **DocumentVersions** | SML | ●1 | `0173-1#02-ABI503#003` |
| DocumentedEntities | SML | 0..1 | `https://admin-shell.io/vdi/2770/1/0/Document/DocumentedEntities` |

### `DocumentId` SMC (Table 6) — `0173-1#02-ABI501#003/0173-1#01-AHF580#003`

| idShort | Type [valueType] | Card | semanticId (verbatim) |
|---|---|---|---|
| **DocumentDomainId** | Prop [xs:string] | ●1 | `0173-1#02-ABH994#003` |
| **DocumentIdentifier** | Prop [xs:string] | ●1 | `0173-1#02-AAO099#004` |
| DocumentIsPrimary | Prop [xs:boolean] | 0..1 | `0173-1#02-ABH995#003` |

DocumentId = simplified VDI 2770 tuple (domain ID + document ID); IDs are unique
*within a domain*, not globally. When ≥2 DocumentIds exist, flag the preferred
one with `DocumentIsPrimary=true`.

### `DocumentClassification` SMC (Table 7) — `0173-1#02-ABI502#003/0173-1#01-AHF581#003`

| idShort | Type [valueType] | Card | semanticId (verbatim) |
|---|---|---|---|
| **ClassId** | Prop [xs:string] | ●1 | `0173-1#02-ABH996#003` |
| **ClassName** | MLP (EN mandatory) | ●1 | `0173-1#02-ABJ219#002` |
| **ClassificationSystem** | Prop [xs:string] | ●1 | `0173-1#02-ABH997#003` |

### THE VDI 2770 classification system (Table 1, §2.3) — MANDATORY

`ClassificationSystem` = **exactly** `"VDI 2770 Blatt 1:2020"`. Every Document
MUST carry at least one classification in this system (additional systems may
be added on top). The 12 official classes, verbatim:

| ClassId | ClassName (EN) | ClassName (DE) | Class semanticId |
|---|---|---|---|
| 01-01 | Identification | Identifikation | `0173-1#07-ABU484#003` |
| 02-01 | Technical specification | Technische Spezifikation | `0173-1#07-ABU485#003` |
| 02-02 | Drawings, plans | Zeichnungen, Pläne | `0173-1#07-ABU486#003` |
| 02-03 | Assemblies | Bauteile | `0173-1#07-ABU487#003` |
| 02-04 | Certificates, declarations | Zeugnisse, Zertifikate, Bescheinigungen | `0173-1#07-ABU488#003` |
| 03-01 | Commissioning, de-commissioning | Montage, Demontage | `0173-1#07-ABU489#003` |
| 03-02 | Operation | Bedienung | `0173-1#07-ABU490#003` |
| 03-03 | General safety | Allgemeine Sicherheit | `0173-1#07-ABU491#003` |
| 03-04 | Inspection, maintenance, testing | Inspektion, Wartung, Prüfung | `0173-1#07-ABU492#003` |
| 03-05 | Repair | Instandsetzung | `0173-1#07-ABU493#003` |
| 03-06 | Spare parts | Ersatzteile | `0173-1#07-ABU494#003` |
| 04-01 | Contract documents | Vertragsunterlagen | `0173-1#07-ABU495#003` |

An operating manual is **03-02 Operation** (NOT 03-04, which is
inspection/maintenance/testing — implementations get this pair wrong).
Secondary system (Annex E): `ClassificationSystem="IEC 61355-1:2008"`, ClassId =
two-letter upper-case code (full printed selection in the JSON map's
`classifications.iec61355_2008`; e.g. `DC` Instructions and manuals). Annex B:
the "Intelligent Information for Use" submodel specializes exactly the 03-xx
classes.

### `DocumentVersion` SMC (Table 8) — `0173-1#02-ABI503#003/0173-1#01-AHF582#003`

| idShort | Type [valueType] | Card | semanticId (verbatim) |
|---|---|---|---|
| **Language** | SML (of Prop) | ●1 | `0173-1#02-AAN468#008` |
| **Version** | Prop [xs:string] | ●1 | `0173-1#02-AAP003#005` |
| **Title** | MLP | ●1 | `0173-1#02-ABG940#003` |
| Subtitle | MLP | 0..1 | `0173-1#02-ABH998#003` |
| **Description** | MLP | ●1 | `0173-1#02-AAN466#004` |
| KeyWords | MLP | 0..1 | `0173-1#02-ABH999#003` |
| **StatusSetDate** | Prop [xs:date] | ●1 | `0173-1#02-ABI000#003` |
| **StatusValue** | Prop [xs:string] | ●1 | `0173-1#02-ABI001#003` |
| **OrganizationShortName** | Prop [xs:string] | ●1 | `https://api.eclass-cdp.com/0173-1-02-ABI002-003` ¹ |
| **OrganizationOfficialName** | Prop [xs:string] | ●1 | `0173-1#02-ABI004#003` |
| RefersToEntities | SML (of Ref) | 0..1 | `0173-1#02-ABK288#002` |
| BasedOnReferences | SML (of Ref) | 0..1 | `0173-1#02-ABK289#002` |
| TranslationOfEntities | SML (of Ref) | 0..1 | `0173-1#02-ABK290#002` |
| **DigitalFiles** | SML (of File) | ●1 | `0173-1#02-ABK126#002` |
| PreviewFile | File | 0..1 | `0173-1#02-ABK127#002` |

¹ **Printing anomaly, verified in the PDF binary**: OrganizationShortName's row
prints ONLY the eclass-cdp URL — no ECLASS IRDI, no supplemental. Every sibling
prints IRDI + cdp pair. The official template JSON agrees with the print: the
semanticId is the eclass-cdp URL only, with no IRDI and no supplementalSemanticId,
and its ConceptDescription id is that same URL (2.0 and 2.0.1 JSON L1514, L3654; 2.0.2 JSON L1557, L3712).
Emit the URL; do not substitute the pattern IRDI `0173-1#02-ABI002#003`. (The JSON
map records the same settlement since 2026-10-28.)

**Multi-language handling (§2.1 — the data-loss hotspot):**
- Document exists in multiple languages → **different `Document` SMCs**.
- One file contains multiple languages → **ONE `DocumentVersion`** with multiple
  entries in its `Language` SML.
- Multiple versions of the same document → multiple `DocumentVersion` SMCs.
- `Language` SML (Table 9): `orderRelevant=No`, `typeValueListElement=Property`;
  each child Prop [xs:string] carries the **ISO 639 code as its VALUE** (the
  printed idShort "en" is a placeholder — SML children carry no idShort under
  metamodel 3.0), cardinality **1..*** (at least one language).
- MLPs (Title/Subtitle/Description/KeyWords/ClassName): VDI 2770's
  TranslateableString is mapped onto MultiLanguageProperty (Annex D §6); EN is
  explicitly mandatory for ClassName. Never overwrite an MLP's langString set
  when adding a language — merge.

**Relationship SMLs** (Tables 10–12): each 0..1, `orderRelevant=No`,
`typeValueListElement=ReferenceElement`, child Ref 1..* with the SAME semanticId
as the list. `RefersTo*` = loose relationship; `BasedOn*` / `TranslationOf*` =
strong. References may span multiple AAS — then **the AssetId shall be used as
first key** (§2.2).

**DocumentedEntities / Entities** (Tables 4, 14, §2.2): asset association is
implicit via the AAS↔asset relation. Supplier parts inside a complex asset are
marked as `Entity` elements in the `Entities` SML (creation of the Entity
element is **required** when parts are marked); recommendation for simple cases
is **co-managed**; self-managed Entities point to the part's own AAS via
`globalAssetId` (AASd-14 — see [[aas-bom]]). A Document that documents such a
part (not the asset itself) carries a `DocumentedEntities` list of
ReferenceElements → those Entity elements. Entity elements may contain
SubmodelElements but **no self-standing Submodels** (spec footnote 3).

## FILE / ATTACHMENT semantics (feeds package tests)

What the spec actually says (§2.1 + Table 13 + Annex D), and what it implies for
a `.aasx` package (cross-reference [[aasx-format]] for the OPC mechanics):

1. **Every `DocumentVersion` SHALL contain at least one `DigitalFile`** — an AAS
   `File` element inside the `DigitalFiles` SML (`typeValueListElement=File`).
   "MIME-Type, file name and file contents given by the file SubmodelElement."
2. **PDF/A is the required format** per VDI 2770: ISO 19005-1/-2/-3 = PDF/A-1,
   PDF/A-2, PDF/A-3 ("PDF/A files are required"). Long-term access is the point
   (Annex D). Expected `contentType`: `application/pdf`.
3. **In-package vs external — BOTH are allowed.** The spec: "The 'DigitalFile'
   … can also be provided in the Submodel via a link, which is technically
   supported by the file element of an AAS." So:
   - **In-package** (the handover-grade default): `File.value` = a relative
     path to a **supplementary part inside the .aasx** (e.g.
     `/aasx/HandoverDocumentation/manual.pdf`). Package contract per
     IDTA-01005: the part must exist in the ZIP, be declared in
     `[Content_Types].xml`, and be targeted by an `aas-suppl` relationship
     (`http://admin-shell.io/aasx/relationships/aas-suppl`).
   - **External**: `File.value` = an absolute URL. BUT the legal-requirements
     caveat applies verbatim: "the legal requirements (e.g. Machinenrichtlinie
     [Machinery Directive 2006/42/EC]) for the 'DigitalFile' according to ISO
     19005 and the document/information provided by a link **should be
     identical**." A link is a convenience, not a substitute for the PDF/A
     content — for a handover that must survive the operator's IT intake,
     embed the file.
4. **Multiple DigitalFiles = same content, different MIME types.** "If multiple
   'DigitalFiles' with different MIME-Types are used, **each of them is assumed
   to represent the 'DocumentVersion' in total and must contain equal
   content**." A DocumentVersion's files are NOT chapters/fragments — never
   split one document across DigitalFile entries.
5. **`PreviewFile`** (0..1, direct child of DocumentVersion, NOT inside
   DigitalFiles): "a preview image of the Document Version, e.g. first page, in
   a commonly used image format and low resolution" → `image/png`/`image/jpeg`.
6. **VDI 2770's own container format (XML+ZIP) is NOT used** — "This format is,
   however, not relevant for the Submodel template defined" (Annex D). The
   .aasx package + File elements replace it.

**Package-test assertions this section licenses** (for every File element in a
HandoverDocumentation submodel — DigitalFile and PreviewFile):
- `value` is non-empty (an empty File in a mandatory DigitalFiles slot is a
  broken handover);
- relative `value` → the part EXISTS in the .aasx ZIP, has a
  `[Content_Types].xml` entry, and is reachable via an `aas-suppl`
  relationship;
- absolute `value` → it is a well-formed absolute IRI;
- `contentType` is a valid MIME type and matches the referenced bytes
  (sniff-check); DigitalFile defaults to `application/pdf` (PDF/A) — non-PDF is
  spec-legal only as an equal-content alternative representation;
- PreviewFile, when present, is an image MIME type.

## Conformance gotchas (the ones that bite)

- **Everything is wrapped in SMLs in 2.0.** `Documents`, `DocumentIds`,
  `DocumentClassifications`, `DocumentVersions`, `Language`, `DigitalFiles`,
  the three relationship lists, `DocumentedEntities`, `Entities` — ALL
  SubmodelElementLists. A 1.2-era flat shape (`Document01` SMC at the submodel
  root, `DigitalFile01` loose in the version) is structurally non-conformant.
- **The mandatory chain is heavy.** Submodel → `Documents`[1] → `Document`[1..*]
  → `DocumentIds`[1] + `DocumentClassifications`[1] + `DocumentVersions`[1];
  each DocumentId: `DocumentDomainId` + `DocumentIdentifier`; each
  Classification: all three fields; each DocumentVersion: **NINE** mandatories
  (Language, Version, Title, Description, StatusSetDate, StatusValue,
  OrganizationShortName, OrganizationOfficialName, DigitalFiles). A "minimal"
  handover is not small — plan the wizard UI accordingly.
- **1.2 → 2.0 renames are non-backward compatible** (Annex C):
  `DocumentVersionId`→`Version`, `Summary`→`Description`,
  `ValueId`→`DocumentIdentifier` — each with a NEW semanticId — and **ALL**
  ECLASS IRDIs re-keyed to Release 15. Migrating = re-keying every element, not
  just the submodel id.
- **Submodel semanticId is an IRDI** (`0173-1#01-AHF578#003`), unlike most
  templates' admin-shell.io IRIs. Detectors that match handover submodels by
  `https://admin-shell.io/vdi/2770/...` or `.../zvei/handover/...` prefixes are
  matching v1.x-era lineages, not 2.0.
- **VDI 2770 classification is mandatory** — at least one DocumentClassification
  with `ClassificationSystem="VDI 2770 Blatt 1:2020"` (exact string), a ClassId
  from the 12-class table, and the matching ClassName (EN mandatory). Pairing
  ClassId with the wrong ClassName (e.g. 03-04 + "Operating Manual") is
  semantic corruption even if it validates structurally.
- **StatusValue enumeration** — "the following two values should be used":
  `InReview`, `Released`. Anything else defeats interop with VDI 2770 intakes.
  `StatusSetDate` is `xs:date` — never emit `value=""` (lexical failure).
- **AASd-120** — under metamodel 3.0, direct SML children carry NO idShort. The
  spec's printed idShorts (`Document`, `DocumentId`, `en`, `DigitalFile`, …) are
  table readability; the template AASX is migrated to metamodel V3.01 (Annex C
  change #4). Same trap class as the Nameplate `Markings__00__` case — know
  which metamodel you serialize (3.0 strips, 3.1 tolerates).
- **AASd-107 / semanticIdListElement** — `Documents` declares
  `semanticIdListElement=[GlobalReference, 0173-1#02-ABI500#003/0173-1#01-AHF579#003]`;
  every child Document's semanticId must match it.
- **The `~0` supplemental** — Document's first supplementalSemanticId prints as
  `0173-1#02-ABI500#003~0/0173-1#01-AHF579#003` in the PDF (binary-verified).
  The official 2.0/2.0.1/2.0.2 template JSONs carry the same `~0` infix (also on
  DocumentId/DocumentClassification/DocumentVersion: `…ABI501#003~0/…`,
  `…ABI502#003~0/…`, `…ABI503#003~0/…`). Copy verbatim.
- **Language ≠ a property of the file** — it lives on the DocumentVersion (the
  Language SML), and drives the split rule: multi-language FILE → one version,
  many Language entries; per-language DOCUMENTS → separate Document SMCs.
- **DocumentedEntity vs the asset** — only use `DocumentedEntities` when the
  document is about a dependent Entity (supplier part), never for the AAS's own
  asset (that association is implicit). Self-managed Entities need
  `globalAssetId` (AASd-14); cross-AAS references put the AssetId as first key.
- **Cardinalities NOT printed in the PDF** — the card of `DocumentId` /
  `DocumentClassification` / `DocumentVersion` inside their SMLs has no printed
  row. The official template JSON (2.0 and 2.0.1) settles it: each item carries
  `SMT/Cardinality` = `OneToMany` (1..*), like `Document` itself (2.0 JSON L165,
  L282, L603, L917). The JSON map records `1..*` from these qualifiers since
  2026-10-28. The three SMLs have `typeValueListElement=SubmodelElementCollection`
  and no `orderRelevant` attribute in any 2.0.x JSON (metamodel default applies).

## Implementation drift (what 1.2-shaped implementations get wrong)

Seen in a production editor before its 2.0 migration; check each one:
- Submodel semanticId still the v1.x IRI `https://admin-shell.io/vdi/2770/1/0/Documentation`
  (or the ZVEI draft `https://admin-shell.io/zvei/handover/1/0/HandoverDocumentation`);
  2.0 is the IRDI `0173-1#01-AHF578#003`. The official 1.2 template JSON already used
  the IRDI `0173-1#01-AHF578#001` (ModelReference, key type Submodel; submodel id
  `https://admin-shell.io/IDTA02004-1-2`), so a vdi/2770 IRI is pre-1.2 / non-template.
- Flat 1.2 structure: `Document01` SMC at the root (no `Documents` SML),
  `DocumentClassification` / `DocumentVersion01` as direct children (no
  `DocumentClassifications` / `DocumentVersions` SMLs), and NO `DocumentIds` /
  `DocumentId` at all (mandatory in 2.0).
- `Language` as a single Property (2.0: SML 1..*); old idShorts
  `DocumentVersionId` / `Summary` (2.0: `Version` / `Description`); the other
  DocumentVersion mandatories missing (StatusSetDate, StatusValue,
  OrganizationShortName, OrganizationOfficialName, the DigitalFiles wrapper).
- `ClassificationSystem='VDI2770:2018'` (spec: `VDI 2770 Blatt 1:2020`) and ClassId
  `03-04` labelled "Operating Manual" (03-04 = Inspection/maintenance/testing; a
  manual is 03-02).
- Wrong-concept IRDIs in extraction paths: Title→`0173-1#02-AAU731#003` (= Nameplate
  ManufacturerProductFamily), Summary→`0173-1#02-AAU732#001`,
  Language→`0173-1#02-AAY813#001`, DocumentVersionId→`0173-1#02-AAY814#001`
  (v1.x-era codes). 2.0 verbatim: Title `0173-1#02-ABG940#003`, Description
  `0173-1#02-AAN466#004`, Language `0173-1#02-AAN468#008`, Version
  `0173-1#02-AAP003#005`.
- Multilingual-field data loss: a langString with a missing/blank language
  dropped on load, per-instance values overwriting (instead of merging into) the
  langString map, empty langString arrays omitted on serialize. Title / Subtitle /
  Description / KeyWords / ClassName are MLPs and Language becomes an SML, so a
  2.0 migration touches exactly these paths.
- A multi-source import that does not embed EVERY source PDF as a File element.

**Migration 1.2 → 2.0 must be BOUNDED**: build the 2.0 representation as a NEW
submodel object (never mutate in place), PRESERVE the 1.2 source untouched, and
show the user a VISIBLE field diff (re-keyed semanticIds, renamed
DocumentVersionId→Version / Summary→Description / ValueId→DocumentIdentifier,
SML wrappers added, Language Prop→SML, new mandatory fields) before committing.
No silent rewrites.

## Sign-off checklist (only after reading the PDF)

1. Read the bundled IDTA-02004-2-0 PDF/txt — done?
2. Submodel: idShort `HandoverDocumentation`, semanticId
   `0173-1#01-AHF578#003` (IRDI — not a vdi/2770 or zvei/handover IRI).
3. Structure: `Documents` SML → `Document` SMC(s) → `DocumentIds` +
   `DocumentClassifications` + `DocumentVersions` SMLs — no flat 1.2 shapes;
   SML attributes (orderRelevant=No, typeValueListElement,
   Documents' semanticIdListElement) set.
4. Every element's semanticId matches `semanticid-map-2-0.json` verbatim
   (ECLASS Release 15) — no 1.2 stragglers, no wrong-concept IRDIs.
5. Each Document: ≥1 DocumentId (DomainId + Identifier; IsPrimary when
   multiple) and ≥1 VDI 2770 classification —
   `ClassificationSystem="VDI 2770 Blatt 1:2020"`, ClassId from the 12-class
   table, ClassName (EN) matching the ClassId.
6. Each DocumentVersion: all NINE mandatories present and non-empty; StatusValue
   ∈ {InReview, Released}; StatusSetDate a real xs:date; Language SML with ≥1
   ISO 639 code as VALUE.
7. Files: ≥1 DigitalFile per DocumentVersion; in-package files exist as .aasx
   supplementary parts (Content_Types + aas-suppl rel) with truthful
   contentType; external links are absolute IRIs whose content matches the
   PDF/A; multiple DigitalFiles = equal content only; PreviewFile is an image.
8. Multi-language split rule honored (languages-in-one-file vs
   per-language Documents); MLP langString sets merged, never overwritten.
9. Entities/DocumentedEntities: Entity elements created for marked supplier
   parts (co-managed default; self-managed ⇒ globalAssetId per AASd-14);
   DocumentedEntity references only for part-scoped documents.
10. idShort-in-SML decision matches the target metamodel (3.0 strips per
    AASd-120; the official AASX targets V3.01).
11. Run [[aas-validation]] (XSD + AASd-*) AND self-check the mandatory chain
    from `semanticid-map-2-0.json` — don't assume the engine template-checks
    02004 v2.0.
