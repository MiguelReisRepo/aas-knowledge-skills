---
name: aas-carbon-footprint
description: Asset Administration Shell Product Carbon Footprint expertise — the IDTA-02023 "Carbon Footprint" submodel template, released v1.0 (March 2025). Covers the full PCF tree (ProductCarbonFootprints SML → ProductCarbonFootprint SMC → PcfCalculationMethods SML, PcfCO2eq, ReferenceImpactUnitForCalculation, QuantityOfMeasureForCalculation, LifeCyclePhases SML, ExplanatoryStatement File, PublicationDate/ExpirationDate, GoodsHandoverAddress), the OPTIONAL ProductOrSectorSpecificCarbonFootprints/PACT subtree (ProductOrSectorSpecificRule, ExternalPcfApi, PcfInformation), the ECLASS-15 #003 IRDIs for the core PCF properties (ABG854 method, ABG855 CO2eq, ABG856 reference unit, ABG857 quantity, ABG858 lifecycle phase), the admin-shell.io/idta/CarbonFootprint IRIs for the structural elements, the ECLASS-15 value lists with valueIds (LifeCyclePhase "A1-A3"…"D - reuse", calculation methods "ISO 14067"/"EN 15804"/"GHG Protocol"/PACT…, reference units), and the draft-0.9→1.0 reshape (TransportCarbonFootprint removed, flat props → SMLs, #001→#003 IRDIs). Use this skill whenever the user models, reviews, extracts, or validates a Product Carbon Footprint / PCF / CO2 / embodied-carbon / EPD submodel, mentions IDTA-02023, ProductCarbonFootprints, cradle-to-gate, PACT. GROUND TRUTH is the bundled official IDTA-02023 PDF (read it first) cross-checked with the published machine-readable template JSON.
metadata:
  type: reference
---

# AAS Carbon Footprint (IDTA-02023 v1.0)

The canonical reference for modelling a product's **carbon footprint** as an AAS
submodel: IDTA-02023 *"Carbon Footprint"*, **released v1.0 (March 2025)**. It
carries one or more Product Carbon Footprint (PCF) blocks — a CO2-equivalent
value plus the calculation method, reference unit, lifecycle phases covered, and
supporting evidence — so a manufacturer can hand a machine-readable footprint to
the next actor in the chain (the DPP / ESPR carbon story).

Companion to [[aas-submodel-templates]] (the template map), [[aas-knowledge]]
(metamodel), [[aas-validation]] (AASd-*), [[eclass-irdi]] (the ECLASS side of the
core PCF property IRDIs), [[aas-nameplate]] (the shared `AddressInformation`
shape reused by `GoodsHandoverAddress`), and [[dpp-aas-compliance]] (where PCF
sits in the ESPR/DPP picture).

## ⚠ MANDATORY FIRST STEP — read the official spec, every time

**Before authoring, editing, reviewing, extracting, or validating ANY Carbon
Footprint submodel, read the bundled official specification first** — it is the
ground truth. Memory drifts; the PDF does not. Read the **text** extraction
(always works; PDF rendering needs poppler, which may be absent); treat the PDF
as the authoritative binary:

```
Read: ~/.claude/skills/aas-carbon-footprint/IDTA-02023_Submodel_CarbonFootprint.txt   ← always readable
      ~/.claude/skills/aas-carbon-footprint/IDTA-02023_Submodel_CarbonFootprint.pdf   ← authoritative (30 pages)
```
(In the aas-skills repo: `skills/aas-carbon-footprint/IDTA-02023_Submodel_CarbonFootprint.{txt,pdf}`.)

A second, cross-checked ground truth is the published machine-readable
template (`github.com/admin-shell-io/submodel-templates` →
`published/Carbon Footprint/1/0`). **If the PDF and the template ever disagree,
the PDF wins** — fix this skill.

## RECONCILED against an implementation (2026-07-16)

Read verbatim against the bundled PDF. Reconciliation flagged these
**implementation discrepancies** (a mandatory-set check should enforce them):

- **`PublicationDate` is MANDATORY** (card 1, xs:dateTime, Table 4) — seeding it
  EMPTY fails twice (mandatory + xs:dateTime lexical failure).
- **`GoodsHandoverAddress`: the two official artefacts disagree.** PDF Table 4 (p.18)
  prints card **1** (mandatory); the official 1.0 and 1.0.1 template JSON qualify it
  `SMT/Cardinality` **ZeroToOne** (1.0 JSON L470 ff.). The PDF also prints a
  `supplementalSemanticId` ×3 (`https://admin-shell.io/smt-dropin/smt-dropin-use/1/0`;
  `0112/2///61360_7#AAS002#001`; `0173-1#02-AAQ837#008`) — implementations tend to omit both.
  Emitting it satisfies both readings.
- **`LifeCyclePhases` SML id:** use `CF/LifeCyclePhases/1/0`. PDF Table 6 misprints
  it as `CF/PcfCalculationMethods/1/0` (copy-paste from Table 5).
- **`PcfApiEndpoint` valueType: the two official artefacts disagree.** PDF Table 9
  (p.22) prints `[string]`; the official 1.0 / 1.0.1 template JSON use `xs:anyURI`. Do not gate valueType on either; `xs:anyURI` follows the JSON.
- **`ArbitraryContent`:** PDF prints the idShort `ArbitratyContent` (typo) + type
  `[SME]`, card 0..n; the template corrects the spelling + models it as
  `Property[xs:string]`.

## Structure tree (v1.0, verbatim from the bundled PDF §2.2)

Submodel semanticId is an **admin-shell.io IRI, not an IRDI**:
`https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/1/0`
(idShort `CarbonFootprint`). Below, `CF` = `https://admin-shell.io/idta/CarbonFootprint`.
Legend: ● = mandatory.

```
Submodel  idShort=CarbonFootprint
          semanticId → CF/CarbonFootprint/1/0
  ├─ [SML] ProductCarbonFootprints ●1        typeValueListElement=SMC
  │        │   semanticId=CF/ProductCarbonFootprints/1/0
  │        │   semanticIdListElement=CF/ProductCarbonFootprint/1/0
  │        └─ [SMC] ProductCarbonFootprint [1..*]   ← one block per measured lifecycle scope
  │             ├─ [SML]  PcfCalculationMethods ●   of Property xs:string
  │             │          → [Prop] PcfCalculationMethod   value list, e.g. "ISO 14067"
  │             ├─ [Prop] PcfCO2eq ●                 xs:decimal   (kg CO2-eq per QuantityOfMeasure)
  │             ├─ [Prop] ReferenceImpactUnitForCalculation ●  xs:string   ("piece"|"kg"|"kWh"…)
  │             ├─ [Prop] QuantityOfMeasureForCalculation ●    xs:double   (amount of ref unit)
  │             ├─ [SML]  LifeCyclePhases ●          of Property xs:string
  │             │          → [Prop] LifeCyclePhase   value list (Table 13), e.g. "A1-A3"
  │             ├─ [File]  ExplanatoryStatement 0..1 application/pdf (EPD / study report)
  │             ├─ [Prop]  PublicationDate ●         xs:dateTime   ← MANDATORY (card 1), PDF Table 4
  │             ├─ [Prop]  ExpirationDate  0..1       xs:dateTime
  │             └─ [SMC]   GoodsHandoverAddress      = Nameplate AddressInformation shape ← PDF card 1, JSON 0..1
  │                         + supplementalSemanticId ×3 (smt-dropin-use/1/0 ; 61360_7#AAS002#001 ; 0173-1#02-AAQ837#008)
  │                         (Street, HouseNumber, ZipCode, CityTown, Country, Latitude, Longitude)
  └─ [SML] ProductOrSectorSpecificCarbonFootprints  0..1 (ZeroToOne, PACT) typeValueListElement=SMC
           └─ [SMC] ProductOrSectorSpecificCarbonFootprint  (empty by default — see PACT subtree)
```

### Core PCF property semanticIds (verbatim — ECLASS Release 15 #003 IRDIs)

| idShort | Type [valueType] | semanticId (verbatim) |
|---|---|---|
| **PcfCalculationMethod** | Prop [xs:string] | `0173-1#02-ABG854#003` |
| **PcfCO2eq** | Prop [xs:decimal] | `0173-1#02-ABG855#003` |
| **ReferenceImpactUnitForCalculation** | Prop [xs:string] | `0173-1#02-ABG856#003` |
| **QuantityOfMeasureForCalculation** | Prop [xs:double] | `0173-1#02-ABG857#003` |
| **LifeCyclePhase** | Prop [xs:string] | `0173-1#02-ABG858#003` |

The wrapping SMLs carry a semanticId (IRI) AND a `semanticIdListElement` = the
IRDI of their child: `PcfCalculationMethods` → `semanticIdListElement 0173-1#02-ABG854#003`;
`LifeCyclePhases` → `0173-1#02-ABG858#003`. The child Properties repeat that IRDI.

### Structural / IRI semanticIds (verbatim)

| Element | semanticId |
|---|---|
| Submodel `CarbonFootprint` | `CF/CarbonFootprint/1/0` |
| `ProductCarbonFootprints` (SML) | `CF/ProductCarbonFootprints/1/0` |
| `ProductCarbonFootprint` (SMC) | `CF/ProductCarbonFootprint/1/0` |
| `PcfCalculationMethods` (SML) | `CF/PcfCalculationMethods/1/0` |
| `LifeCyclePhases` (SML) | `CF/LifeCyclePhases/1/0` |
| `ExplanatoryStatement` (File) | `CF/ExplanatoryStatement/1/0` |
| `PublicationDate` / `ExpirationDate` | `CF/PublicationDate/1/0` · `CF/ExpirationDate/1/0` |
| `GoodsHandoverAddress` (SMC) | `https://admin-shell.io/zvei/nameplate/1/0/ContactInformations/AddressInformation` |
| `ProductOrSectorSpecificCarbonFootprints` (SML) | `CF/ProductOrSectorSpecificCarbonFootprints/1/0` |

### The OPTIONAL PACT subtree (`ProductOrSectorSpecificCarbonFootprint` SMC)

Seeded EMPTY (cardinality ZeroToOne) so it never forces content. Clone this shape
into it when a product-category / sector rule applies (idShorts + IRIs verbatim
from the published 1.0 JSON):

- **ProductOrSectorSpecificRule** (SMC, `CF/ProductOrSectorSpecificRule/1/0`):
  `PcfRuleOperator`, `PcfRuleName`, `PcfRuleVersion` (Prop xs:string) +
  **`PcfRuleOnlineReference` is a File** (`application/pdf`), NOT a Property
  xs:anyURI — the published template models the rule reference as a File.
- **ExternalPcfApi** (SMC, `CF/ExternalPcfApi/1/0`): `PcfApiEndpoint`
  (Prop **xs:anyURI**), `PcfApiQuery` (Prop xs:string) — a live PCF API to query.
- **PcfInformation** (SMC, `CF/PcfInformation/1/0`): `ArbitraryContent`
  (Prop xs:string) whose semanticId is the **cross-template**
  `https://admin-shell.io/SMT/General/Arbitrary` — NOT under the CarbonFootprint
  namespace. Easy to get wrong.

## Value lists (§2.5-2.7, Tables 11-13, ECLASS 15) — emit the printed value strings

Three Properties take values from ECLASS 15 value lists; each value has a valueId.
"Further values with corresponding semanticIds can be added." (notes under each table).

**`PcfCalculationMethod`** — list `0173-1#09-AAO115#003` (Table 11, p.25):
`EN 15804` ABU223#003 · `GHG Protocol` ABU221#003 · `IEC TS 63058` ABU222#003 ·
`IEC 63366` ACA792#002 · `ISO 14040, ISO 14044` ABV505#003 · **`ISO 14067` ABU218#003** ·
`PEP Ecopassport` ABU220#003 · `PACT v1.0.1` ACC004#001 · `PACT v2.0.0` ACC003#001 ·
`PACT v3.0.0` ACC012#001 · `TFS v2` ACC005#001 · `TFS v3` ACC010#001 · `Catena-X v1`
ACC007#001 · `Catena-X v2` ACC006#001 · `Catena-X v3` ACC011#001 · `BS PAS 2050`
ACC008#001 · `IEC 63372` ACC019#001 (all valueIds `0173-1#07-…`). The value is the bare
standard name ("ISO 14067", not "ISO 14067:2018"); there is no PEF entry. "For values not
given in the table, use SMC „ProductOrSectorSpecificRule“" (PcfCalculationMethod row, p.19).

**`ReferenceImpactUnitForCalculation`** — list `0173-1#09-AAO323#003` (Table 12, p.25-26):
`g` ABZ596#003 · `kg` ABZ597#003 · `t` ABZ598#003 · `ml` ABZ599#003 · `l` ABZ600#003 ·
`cbm` ABZ601#003 · `qm` ABZ602#003 · **`piece` ABZ603#003** · `kWh` ACB997#001.

**`LifeCyclePhase`** — list `0173-1#09-AAO113#003` (Table 13, p.26). Values are labelled
EN 15804-style module strings, plus combined ranges; cradle-to-gate = **`A1-A3`
ABZ789#003**:
`A1 - raw material supply (and upstream production)` ABU208#003 · `A2 - cradle-to-gate
transport to factory` ABU209#003 · `A3 - production` ABU210#003 · `A4 - transport to final
destination` ABU211#003 · `A4-A5` ACC013#001 · `A5 - Installation` ACC016#001 ·
`B1 - usage phase` ABU212#003 · `B1-B7` ACC014#001 · `B2 - maintenance` ABV498#003 ·
`B3 - repair` ABV497#003 · `B4 - Replacement` ACC017#001 · `B5 - update/upgrade,
refurbishing` ABV499#003 · `B6 - usage energy consumption` ABV500#003 · `B7 - usage water
consumption` ABV501#003 · `C1 - reassembly` ABV502#003 · `C1-C4` ACC015#001 · `C2 -
transport to recycler` ABU213#003 · `C2-C4` ACC018#001 · `C3 - recycling, waste treatment`
ABV503#003 · `C4 - landfill` ABV504#003 · `D - reuse` ABU214#003.

**Codes vs labels (do not mix them up).** The Table 13 *value* is the whole label string
(`A3 - production`); only the combined ranges (`A1-A3`, `A4-A5`, `B1-B7`, `C1-C4`, `C2-C4`) are bare
codes. The battery passport part IDTA 02035-3 1.1.0 uses the same labels: "The string value in the
value list is based on DIN DKE SPEC 99100: "A1 - raw material supply (and upstream production)" …
"A3 - production" … "A4 - transport to final destination" … "C3 - recycling, waste treatment""
(LifeCyclePhases row, PDF p.9). The SAMM enumeration `…carbon_footprint:1.0.0#LifeCyclePhaseEnum`
(see [[dpp-aas-compliance]] §8.3) lists bare codes (`A1`, `A3`). So: write the Table 13 label plus its
valueId; when validating, accept a label whose code before " - " is in the code list (or match the
valueId), and never flag `A3 - production` as "not in the list".

## Conformance gotchas (the ones that bite)

- **Everything is wrapped in SMLs in 1.0.** `ProductCarbonFootprints`,
  `PcfCalculationMethods`, `LifeCyclePhases` are SubmodelElementLists. The
  draft-0.9 flat `PcfCalculationMethod`/`PcfLifeCyclePhase` Properties at the PCF
  root are structurally non-conformant in 1.0. A product may carry **many** PCF
  blocks — one per lifecycle scope — hence the mandatory `ProductCarbonFootprints`
  wrapper (cardinality One).
- **SML-of-Property → AASd-108.** `PcfCalculationMethods` and `LifeCyclePhases`
  are SMLs whose children are **Property** (not SMC). Any element mapper that
  drops `typeValueListElement` / `valueTypeListElement` makes the serializer
  default the list to SMC → invalid XML.
  Carry `typeValueListElement=Property`, `valueTypeListElement=xs:string`.
- **Mixed IRDI + IRI semanticIds.** Core measured properties use **ECLASS R15
  IRDIs** (`0173-1#02-ABG85x#003`); every structural element uses
  **admin-shell.io IRIs** (`CF/…/1/0`). Don't "normalise" one family into the
  other.
- **`PcfRuleOnlineReference` is a File, not a URI Property.** And
  `PcfApiEndpoint` is `xs:anyURI` in the official JSON (PDF Table 9 prints `[string]`). Two adjacent "reference"-looking fields,
  two different model types — copy from the template, don't guess.
- **`ArbitraryContent` uses a foreign semanticId** (`…/SMT/General/Arbitrary`),
  not a CarbonFootprint IRI.
- **`GoodsHandoverAddress` reuses the Nameplate `AddressInformation` shape** and
  its semanticId — it marks where the "gate" is for cradle-to-gate scope. Keep it
  consistent with [[aas-nameplate]].
- **valueTypes matter:** `PcfCO2eq` is `xs:decimal`, `QuantityOfMeasureForCalculation`
  is `xs:double`, `PublicationDate`/`ExpirationDate` are `xs:dateTime` (never emit
  `value=""` for a populated date — lexical failure).
- **draft-0.9 → 1.0 reshape:** the draft `TransportCarbonFootprint` SMC was
  REMOVED; #001-suffixed IRDIs became #003. A submodel with `TransportCarbonFootprint`
  or #001 IRDIs is pre-release, not 1.0.

- Extraction: any AI parser that emits PCF must use the IRDIs above verbatim (the
  parser's live output drifts even when the template is right).

## Sign-off checklist

1. Read the bundled official IDTA-02023 PDF/txt AND the official template JSON.
2. Submodel: idShort `CarbonFootprint`, semanticId `CF/CarbonFootprint/1/0` (IRI).
3. `ProductCarbonFootprints` SML present (cardinality One), `typeValueListElement=SMC`,
   `semanticIdListElement=CF/ProductCarbonFootprint/1/0`; ≥1 `ProductCarbonFootprint`.
4. Each PCF: `PcfCalculationMethods` (≥1 method), `PcfCO2eq` (xs:decimal),
   `ReferenceImpactUnitForCalculation`, `QuantityOfMeasureForCalculation` (xs:double),
   `LifeCyclePhases` (≥1 Table 13 value) — all present, non-empty.
5. Core property semanticIds = the ECLASS R15 IRDIs verbatim (ABG854/855/856/857/858);
   structural elements = the `CF/…/1/0` IRIs; no #001 stragglers, no draft
   `TransportCarbonFootprint`.
6. SML-of-Property elements carry `typeValueListElement=Property` +
   `valueTypeListElement` (no AASd-108).
7. Dates are `xs:dateTime`; `PcfRuleOnlineReference` is a File; `PcfApiEndpoint`
   is xs:anyURI (JSON; PDF `[string]`); `ArbitraryContent` uses the `/SMT/General/Arbitrary` semanticId.
8. Run [[aas-validation]] (XSD + AASd-*) AND self-check the mandatory set against
   this map — don't assume the engine template-checks IDTA-02023.
