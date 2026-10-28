---
name: aas-nameplate
description: Asset Administration Shell Digital Nameplate expertise — the IDTA-02006 "Digital Nameplate for Industrial Equipment" submodel template, v3.0.1 (Oct 2025). Covers the complete VERSION-PAIRING TABLE (IEC CDD primary semanticId + ECLASS supplementalSemanticId per element, with the legacy ZVEI 2/0 equivalents), the mandatory set (URIOfTheProduct, ManufacturerName, ManufacturerProductDesignation, AddressInformation, OrderCodeOfManufacturer), the Markings SML (CE marking mandatory per EU Blue Guide, MarkingName/MarkingFile), AddressInformation as SMT drop-in (renamed from ContactInformation), AssetSpecificProperties → GuidelineSpecificProperties nesting, the 2.0→3.0 MLP→Property datatype flips (HW/FW/SW versions, OrderCode), and the frozen machine map semanticid-map-3-0-1.json. Use this skill whenever the user models a nameplate or rating plate, builds/reviews/migrates a Nameplate submodel, mentions IDTA-02006, Digital Nameplate, ManufacturerName/URIOfTheProduct/YearOfConstruction, ZVEI 2/0 vs IDTA 3/0 version pairing, or CE markings. ALWAYS read the bundled official IDTA-02006 PDF first (see the mandatory step below) — this skill is a map, the PDF is the law.
---

# AAS Digital Nameplate (IDTA-02006 v3.0.1)

The canonical reference for modelling an asset's **nameplate / rating plate** as an
AAS submodel: IDTA-02006 *"Digital Nameplate for Industrial Equipment"*, version
3.0.1 (October 2025). It is the submodel a customer, market-surveillance authority
or spare-parts service actually reads to identify an asset — and the template
whose **2/0 → 3/0 version drift bites real projects**. The version-pairing table below and
the frozen `semanticid-map-3-0-1.json` next to this file exist to kill that bug
class.

Companion to [[aas-submodel-templates]] (the template map), [[aas-knowledge]]
(metamodel), [[aas-validation]] (AASd-*), and [[iec61360]] (the IRDI/CD side).

## ⚠ MANDATORY FIRST STEP — read the official spec, every time

**Before authoring, editing, reviewing, migrating, or validating ANY Digital
Nameplate submodel, you MUST read the bundled official specification** — it is
the ground truth. Memory (yours or this skill's) drifts; the PDF does not. This
very skill was written after the 3.0.1 PDF exposed real drift in app code whose
own comments claimed to be verbatim.

Read it with the Read tool. The skill bundles TWO copies — read the **text**
extraction (always works; PDF rendering needs poppler which may be absent), and
treat the **PDF** as the authoritative binary:

```
Read: ~/.claude/skills/aas-nameplate/IDTA-02006-3-0-1_Submodel_Digital-Nameplate.txt   ← always readable
      ~/.claude/skills/aas-nameplate/IDTA-02006-3-0-1_Submodel_Digital-Nameplate.pdf   ← authoritative (needs poppler)
```
(In the aas-skills repo: `skills/aas-nameplate/IDTA-02006-3-0-1_Submodel_Digital-Nameplate.{txt,pdf}`.)

It is 22 pages — read Chapter 3 (the element tables, §3.1–3.5) and Annex B (the
2.0→3.0 change list + 3.0.1 bug fixes) in full. If a claim in this skill and the
spec ever disagree, **the spec wins** — and fix this skill AND the JSON map.

## THE CENTERPIECE — version-pairing table (3.0.1 verbatim, §3.1–3.5)

**The pairing rule:** the submodel semanticId
`https://admin-shell.io/idta/nameplate/3/0/Nameplate` (unchanged by 3.0.1 —
verified against the PDF, there is NO `/3/0/1/` or `/3/1/` IRI) pairs with the
**IEC CDD primary + ECLASS supplemental** element set below. The old
`https://admin-shell.io/zvei/nameplate/2/0/Nameplate` pairs with the pure-ECLASS
2/0 set (last column). **Never mix the two sets** — a 3/0 submodel IRI over 2/0
element ids (or vice versa) is silent data loss for every 02006-aware consumer.

Legend: ● = mandatory. `2/0 legacy` is sourced from IDTA 02006-2-0 (NOT in the
bundled 3.0.1 PDF) — informative for migration; `VERIFY-2/0` = confirm against
the 2.0 PDF before coding against it.

### Submodel root (`Nameplate`, §3.1)

| idShort | Type [valueType] | Card | 3.0.1 primary (IEC CDD) | 3.0.1 supplemental (ECLASS) | 2/0 legacy |
|---|---|---|---|---|---|
| **URIOfTheProduct** | Prop [xs:anyURI] | ●1 | `0112/2///61987#ABN590#002` | `0173-1#02-ABH173#003` | `0173-1#02-AAY811#001` (was String) |
| **ManufacturerName** | MLP | ●1 | `0112/2///61987#ABA565#009` | `0173-1#02-AAO677#004` | `0173-1#02-AAO677#002` |
| **ManufacturerProductDesignation** | MLP | ●1 | `0112/2///61987#ABA567#009` | `0173-1#02-AAW338#003` | `0173-1#02-AAW338#001` |
| **AddressInformation** | SMC | ●1 | `https://admin-shell.io/zvei/nameplate/1/0/ContactInformations/AddressInformation` | `https://admin-shell.io/smt-dropin/smt-dropin-use/1/0`, `0112/2///61360_7#AAS002#001`, `0173-1#02-AAQ837#008/0173-1#01-ADR448#008` | `…/zvei/nameplate/1/0/ContactInformations/ContactInformation` (idShort was `ContactInformation`) |
| ManufacturerProductRoot | MLP | 0..1 | `0112/2///61360_7#AAS011#001` | `0173-1#02-AAU732#003` | `0173-1#02-AAU732#001` |
| ManufacturerProductFamily | MLP | 0..1 | `0112/2///61987#ABP464#002` | `0173-1#02-AAU731#003` | `0173-1#02-AAU731#001` |
| ManufacturerProductType | Prop [xs:string] | 0..1 | `0112/2///61987#ABA300#008` | `0173-1#02-AAO057#004` | `0173-1#02-AAO057#002` (was MLP) |
| **OrderCodeOfManufacturer** | Prop [xs:string] | ●1 | `0112/2///61987#ABA950#008` | `0173-1#02-AAO227#004` | `0173-1#02-AAO227#002` (was MLP, 0..1) |
| ProductArticleNumberOfManufacturer | Prop [xs:string] | 0..1 | `0112/2///61987#ABA581#007` | `0173-1#02-AAO676#005` | `0173-1#02-AAO676#003` (was MLP) |
| SerialNumber | Prop [xs:string] | 0..1 | `0112/2///61987#ABA951#009` | `0173-1#02-AAM556#004` | `0173-1#02-AAM556#002` |
| YearOfConstruction | Prop [xs:string] | 0..1 | `0112/2///61987#ABP000#002` | `0173-1#02-AAP906#003` | `0173-1#02-AAP906#001` (was ●1) |
| DateOfManufacture | Prop [xs:date] | 0..1 | `0112/2///61987#ABB757#007` | `0173-1#02-AAR972#004` | `0173-1#02-AAR972#002` |
| HardwareVersion | Prop [xs:string] | 0..1 | `0112/2///61987#ABA926#008` | `0173-1#02-AAN270#004` | `0173-1#02-AAN270#002` (was MLP) |
| FirmwareVersion | Prop [xs:string] | 0..1 | `0112/2///61987#ABA302#006` | `0173-1#02-AAM985#004` ¹ | `0173-1#02-AAM985#002` (was MLP) |
| SoftwareVersion | Prop [xs:string] | 0..1 | `0112/2///61987#ABA601#008` | `0173-1#02-AAM737#004` ² | `0173-1#02-AAM737#002` (was MLP) |
| CountryOfOrigin | Prop [xs:string] | 0..1 | `0112/2///61987#ABP462#001` | `0173-1#02-AAO259#007` | `0173-1#02-AAO259#004` |
| UniqueFacilityIdentifier | Prop [xs:string] | 0..1 | `https://admin-shell.io/idta/nameplate/3/0/UniqueFacilityIdentifier` | — | — (NEW in 3.0, ESPR anticipation) |
| CompanyLogo | File | 0..1 | `0112/2///61987#ABP463#001` | `0173-1#02-ABI776#002` | `…/zvei/nameplate/2/0/Nameplate/CompanyLogo` |
| Markings | SML | 0..1 ³ | `0112/2///61360_7#AAS006#001` | `0173-1#02-ABI563#003/0173-1#01-AHF849#003` | VERIFY-2/0 (was an SMC) |
| AssetSpecificProperties | SMC | 0..1 | `0173-1#02-ABI218#003/0173-1#01-AGZ672#004` (ECLASS pair — no IEC CDD primary) | — | VERIFY-2/0 |

¹ FirmwareVersion supplemental prints as `0173-1#02AAM985#004` in the PDF (hyphen
lost at a line break) — normalized here; this exact IRDI is the subject of 3.0.1
bug fix **#123 "Potentially erroneous ECLASS IRDI for FirmwareVersion"**.
² SoftwareVersion supplemental: the official 3.0.1 template JSON has
**`0173-1#02-AAM737#004`** (JSON L717; FirmwareVersion has `AAM985#004` at L674).
The 3.0.1 PDF prints `AAM985#004` for both (p.10) — a print error (ECLASS `AAM985`
is "firmware version", `AAM737` "software version"). Use `AAM737#004`. The frozen
`semanticid-map-3-0-1.json` carries `AAM737#004` from the JSON (corrected
2026-10-28; the entry's note records the deliberate deviation from the PDF print).
³ Template-optional, but the CE marking is **mandatory per the EU Blue Guide** —
a real product placed on the EU market needs the Markings SML with a CE entry.

### `Markings` SML → `Markings__00__` SMC (§3.3)

SML element details: `orderRelevant=No`, `typeValueListElement=SubmodelElementCollection`
(the invalid typeValueListElement was 3.0.1 bug fix **#155**).

| idShort | Type [valueType] | Card | 3.0.1 primary (IEC CDD) | 3.0.1 supplemental (ECLASS) | 2/0 legacy |
|---|---|---|---|---|---|
| **Markings__00__** | SMC | ●1..* | `0112/2///61360_7#AAS009#001` | `0173-1#02-ABI564#003/0173-1#01-AHF850#003` | VERIFY-2/0 (was `Marking`) |
| **MarkingName** | Prop [xs:string] | ●1 | `0112/2///61987#ABA231#009` | `0173-1#02-ABI190#003` | VERIFY-2/0 |
| DesignationOfCertificateOrApproval | Prop [xs:string] | 0..1 | `0112/2///61987#ABH783#003` | `0173-1#02-ABI975#002` | VERIFY-2/0 |
| IssueDate | Prop [xs:date] | 0..1 | `0112/2///61987#ABO097#001` | `0173-1#02-ABL774#001` | VERIFY-2/0 |
| ExpiryDate | Prop [xs:date] | 0..1 | `0112/2///61987#ABH830#002` | `0173-1#02-ABL775#001` | VERIFY-2/0 |
| **MarkingFile** | File | ●1 | `0112/2///61987#ABO100#002` | `0173-1#02-ABI191#003` | VERIFY-2/0 |
| MarkingAdditionalText | Prop [xs:string] | 0..* | `0112/2///61987#ABB146#007` | `0173-1#02-ABI192#003` | VERIFY-2/0 |

`MarkingName` value convention (§3.3): prefer a **valueId** IRDI from the IEC
CDD/ECLASS enumeration — CE = `0112/2///61987#ABO409#003` or
`0173-1#07-DAA603#004`; plain string text in `value` is the fallback. ECLASS
booleans like "CE-qualification present" (`0173-1#02-BAF053#008`) should NOT be
used — use the matching enumeration value instead.

### `AssetSpecificProperties` SMC (§3.4) and `GuidelineSpecificProperties` (§3.5)

| idShort | Type [valueType] | Card | 3.0.1 semanticId | 2/0 legacy |
|---|---|---|---|---|
| ArbitraryProperty | Prop [xs:string] | 0..* | `https://admin-shell.io/SMT/General/ArbitraryProp` | — (new arbitrary-slot convention) |
| ArbitraryMLP | MLP | 0..* | `https://admin-shell.io/SMT/General/ArbitraryMLP` | — |
| ArbitraryFile | File | 0..* | `https://admin-shell.io/SMT/General/ArbitraryFile` | — |
| GuidelineSpecificProperties | SML | 0..1 | `0173-1#02-ABI219#003/0173-1#01-AHD205#004` | VERIFY-2/0 |
| **GuidelineSpecificProperties__00__** | SMC | ●1..* | `0173-1#01-AHD205#004` (class IRDI ONLY — differs from the SML's pair) | VERIFY-2/0 |
| **GuidelineForConformityDeclaration** | Prop [xs:string] | ●1 | `0173-1#02-AAO856#002` | `0173-1#02-AAO856#002` (unchanged) |

The Arbitrary* slots repeat inside each `GuidelineSpecificProperties__00__`
(same General IRIs); idShorts of arbitrary elements are free, `displayName`
recommended. One `GuidelineSpecificProperties__00__` SMC **per standard/
directive**, its `GuidelineForConformityDeclaration` naming the stipulation.

## Structure tree (verified against §2.2 + §3)

```
Submodel  idShort=Nameplate
          semanticId ExternalRef → https://admin-shell.io/idta/nameplate/3/0/Nameplate   ← UNCHANGED in 3.0.1
  ├─ [Prop] URIOfTheProduct ●          … 16 more data elements (table above)
  ├─ [SMC]  AddressInformation ●       ← SMT drop-in "Address Information" (IDTA 02002 family);
  │           MLP Street ● / Zipcode ● / CityTown ● / NationalCode ●
  │           (mandatory per §3.2 of the DOCUMENT only — the drop-in defines all
  │            address props optional, and the four are NOT in the template AASX;
  │            their semanticIds come from the drop-in, not printed in 02006)
  ├─ [File] CompanyLogo
  ├─ [SML]  Markings                   orderRelevant=No, typeValueListElement=SMC
  │    └─ [SMC] Markings__00__  [1..*]
  │         ├─ MarkingName ●  /  MarkingFile ●
  │         └─ DesignationOfCertificateOrApproval / IssueDate / ExpiryDate / MarkingAdditionalText
  └─ [SMC]  AssetSpecificProperties
       ├─ Arbitrary{Property|MLP|File}  [0..*]
       └─ [SML] GuidelineSpecificProperties        ← NESTED HERE, not a submodel-root child
            └─ [SMC] GuidelineSpecificProperties__00__  [1..*]
                 ├─ GuidelineForConformityDeclaration ●
                 └─ Arbitrary{Property|File|MLP}  [0..*]
```

Naming history: 2.0's `ContactInformation` SMC **was renamed to
`AddressInformation`** in 3.0 and re-based on the SMT drop-in "Address
Information" — but its primary semanticId intentionally KEEPS the
`zvei/nameplate/1/0/ContactInformations/…` namespace. A `zvei/1/0` IRI inside a
`idta/3/0` submodel is CORRECT here; do not "fix" it.

## Conformance gotchas (the ones that bite)

- **Version pairing rule** — the submodel IRI version MUST match the element
  semanticId set (see centerpiece table). The typical drift incident is exactly this: 3/0 submodel IRI with stale 2/0 element ids (or 2.0-era
  idShorts). When migrating, re-key EVERY element, not just the submodel.
- **2.0→3.0 type flips** — OrderCodeOfManufacturer, ManufacturerProductType,
  ProductArticleNumberOfManufacturer, HardwareVersion, FirmwareVersion,
  SoftwareVersion: **MLP (langString) in 2.0 → Property (xs:string) in 3.0**;
  URIOfTheProduct: String → **xs:anyURI**. A migration that only swaps
  semanticIds but keeps MLP modelTypes is non-conformant. Fields that STAY MLP:
  ManufacturerName, ManufacturerProductDesignation, ManufacturerProductRoot,
  ManufacturerProductFamily (recommendation: max 1 language string, since the
  values are language-independent).
- **Cardinality flips** — YearOfConstruction ●→0..1; OrderCodeOfManufacturer
  0..1→●. A 2.0-shaped "mandatory fields" checklist is wrong on both in 3.0.
- **Engine only actively template-checks ZVEI 2/0, skips 3/0** — aas-test-engines'
  nameplate template check recognizes the 2/0 IRI; a 3/0 nameplate gets NO
  template-cardinality check and "passes" vacuously. Passing the engine ≠ 3.0
  conformance — enforce the mandatory set yourself from
  `semanticid-map-3-0-1.json`.
- **Empty-mandatory vs missing-mandatory** — a template-aware checker flags a
  MISSING mandatory element (cardinality). A PRESENT-but-empty element usually
  passes cardinality but can fail value/lexical checks instead (empty string is
  not a valid `xs:date`/`xs:anyURI`), and an empty MLP langString set trips
  metamodel constraints. Wizard rule: never emit empty optional elements; never
  emit typed props (date/anyURI) with `value=""`.
- **XSD element order** — the AAS XSD fixes child order (semanticId →
  supplementalSemanticIds → qualifiers → … ; valueType before value; SML
  attributes orderRelevant/typeValueListElement before value). Emit through the
  serializer and gate with an XSD run — never hand-order.
- **SML children and idShort (AASd-120)** — under metamodel **3.0**, direct
  children of an SML must NOT carry an idShort; the official 3.0.1 AASX uses
  idShorts inside `Markings` for readability and the PDF's *Known issues* says
  the file **"will be valid as of metamodel V3.1"**. So `Markings__00__` with an
  idShort = fine on AAS 3.1, AASd-120 violation on 3.0. Know which metamodel you
  serialize.
- **`Markings__00__` / `GuidelineSpecificProperties__00__`** — the `__00__`
  suffix is the decimal-digit uniquifier convention (Annex A); any unique idShort
  is allowed.
- **AddressInformation supplementalSemanticIds** — the 3.0.1 table lists THREE:
  the smt-dropin-use marker, the IEC CDD `61360_7#AAS002#001`, and the ECLASS
  pair `0173-1#02-AAQ837#008/0173-1#01-ADR448#008`. Emitting only the primary is
  incomplete.
- **3.0.1 is a bug-fix release, same IRIs** — fixes: #155 invalid
  typeValueListElement for Markings, #131 empty idShort, #123 FirmwareVersion
  ECLASS IRDI, #116 faulty `administration.templateId` format. The submodel IRI
  and the IEC CDD primaries did NOT change. (Cosmetic: the imprint's version
  history prints the 3.0.1 date as "2025-14-10".)

## Implementation drift to check for (found in a production template, 2026-07-13)

1. **FirmwareVersion supplemental** — a stale `0173-1#02-AAM985#003`; 3.0.1 PDF
   says `…#004` (bug fix #123 territory).
2. **SoftwareVersion supplemental** — `0173-1#02-AAM737#004` is right: it
   matches the official 3.0.1 JSON (the PDF's `AAM985#004` is the print error,
   footnote ²). No change needed.
3. **GuidelineSpecificProperties placement** — putting the SML at the SUBMODEL
   ROOT is wrong; the spec nests it INSIDE `AssetSpecificProperties`. Structural drift.
4. **Missing optional root elements** — ManufacturerProductRoot,
   ManufacturerProductType, ProductArticleNumberOfManufacturer, CompanyLogo are
   absent from the template (silent-data-loss risk for wizard mapping).
5. **Missing supplementalSemanticIds** — AddressInformation (all three),
   Markings SML, Markings__00__, MarkingName, MarkingFile need theirs too.
6. **Markings__00__ missing optional children** — DesignationOfCertificateOrApproval,
   IssueDate, ExpiryDate, MarkingAdditionalText.
7. **Markings SML `orderRelevant=No` not set**; AssetSpecificProperties has no
   Arbitrary* slots (minor, 0..*).
8. **AddressInformation children** (Street `0173-1#02-AAO128#002`, Zipcode
   `…AAO129#002`, CityTown `…AAO132#002`, NationalCode `…AAO134#002`) are not
   defined in the 02006 PDF at all — verify them against the SMT drop-in
   "Address Information" / IDTA 02002 before treating them as conformant.
9. **Company / Phone / Email / Fax are NOT Nameplate elements — never add them to
   AddressInformation** (the #1 silent moat-breaker). The Nameplate's `AddressInformation` drop-in is ADDRESS-ONLY —
   §3.2 (line ~474): "The following SubmodelElements shall be specified within SMC
   AddressInformation: Street, Zipcode, CityTown, NationalCode". §3.2 note (line
   ~469): "SMC AddressInformation is part of SMC ContactInformation of SMT
   ContactInformations [11]" — i.e. the company-contact fields live in the
   **SEPARATE IDTA-02002 `ContactInformations` submodel**, whose `ContactInformation`
   SMC holds `Company` (MLP, `0173-1#02-AAW001#001`, "name of the company") + the
   nested SMCs `Phone` (→ `TelephoneNumber` `0173-1#02-AAO136#002`), `Fax`, `Email`
   (→ `EmailAddress` `0173-1#02-AAO198#002`). The Nameplate's only company-identity
   elements are top-level `ManufacturerName` (MLP, the manufacturer, NOT
   NameOfSupplier/AAW001) and `CompanyLogo` (File). Putting `Company`/AAW001 as a
   flat child inside the untyped address-only `AddressInformation` SMC violates no
   XSD and no AASd-* rule, so it **PASSES the structural conformance gate SILENTLY**
   while being semantically wrong. To model contact identity, build the standalone
   IDTA-02002 `ContactInformations` submodel; never extend the Nameplate. (Verified
   against IDTA-02006-3-0 §3.1/§3.2 + IDTA-02002-1-0 §3.1-3.5.)

The frozen machine map for the conformance core is
`skills/aas-nameplate/semanticid-map-3-0-1.json` (same directory) — extracted
verbatim from the PDF tables; entries flagged `VERIFY-IN-PDF` / notes mark the
two extraction ambiguities (FirmwareVersion hyphen, SoftwareVersion duplicate — the
latter resolved by the official JSON to `AAM737#004`, footnote ²; the map entry is stale).

**Migration 2/0 → 3/0 must be BOUNDED**: build the 3/0 representation as a NEW
submodel object (never mutate in place), PRESERVE the 2/0 source untouched, and
show the user a VISIBLE field diff (re-keyed semanticIds, MLP→Prop type flips,
renamed ContactInformation→AddressInformation, moved/new/dropped fields) before
committing. No silent rewrites.

## Sign-off checklist (only after reading the PDF)

1. Read the bundled IDTA-02006-3-0-1 PDF/txt — done?
2. Submodel semanticId = `https://admin-shell.io/idta/nameplate/3/0/Nameplate`
   (ExternalReference/GlobalReference; NOT the zvei/2/0 IRI, NOT a made-up /3/0/1/).
3. All five root mandatories present: URIOfTheProduct, ManufacturerName,
   ManufacturerProductDesignation, AddressInformation, OrderCodeOfManufacturer.
4. Every element's primary + supplemental semanticId matches the centerpiece
   table / `semanticid-map-3-0-1.json` — no 2/0 stragglers, no mixed sets.
5. Types right: HW/FW/SW versions, OrderCode, ProductType, ArticleNumber are
   Properties (xs:string) not MLPs; URIOfTheProduct is xs:anyURI;
   DateOfManufacture/IssueDate/ExpiryDate are xs:date.
6. AddressInformation carries Street/Zipcode/CityTown/NationalCode (§3.2) and
   its three supplementalSemanticIds.
7. Markings: SML with typeValueListElement=SubmodelElementCollection; each
   marking SMC has MarkingName + MarkingFile; CE modelled via valueId enum where
   possible; idShort-in-SML decision matches the target metamodel (3.0 vs 3.1).
8. GuidelineSpecificProperties nested under AssetSpecificProperties, one SMC per
   guideline with GuidelineForConformityDeclaration.
9. Run [[aas-validation]] (XSD + AASd-*) AND self-check the 3/0 mandatory set —
   remember the engine only template-checks 2/0.

---

## `URIOfTheProduct` case: only scheme and host are case-insensitive

**RFC 3986 §6.2.2.1 makes only *scheme* and *host* case-insensitive — path, query
and fragment are case-SENSITIVE.** Lower-casing the whole value on save can turn a
resolvable product URL into a 404, and `URIOfTheProduct` is the Nameplate's
identity-bearing field (mandatory, `xs:anyURI`). If a tool normalises it, the
minimal-damage form is scheme+host only, leaving the path untouched; a round-trip
test must then compare against the normalised expectation.
