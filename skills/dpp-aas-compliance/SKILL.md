---
name: dpp-aas-compliance
description: >-
  Map, validate and compliance-check a Digital Product Passport (DPP) realised as
  an Asset Administration Shell. Use for: ESPR / EU Digital Product Passport
  questions; CEN-CENELEC JTC 24 standards (EN 18216/18219/18220/18221/18222/18223/18239/18246);
  the IDTA DppMetadata submodel (IDTA 02099-1); deriving a JTC24-compliant DPP from
  an AAS; the Digital Battery Passport (IDTA 02035 series, the first live DPP);
  and mapping DPP data points to AAS submodels, idShorts, semanticIds, cardinalities
  and value lists. Companion to dpp-knowledge (regulatory/architecture) — this skill
  owns the AAS realisation + verified field-level mapping + compliance checklist.
---

# DPP ↔ AAS Compliance

The **regulatory/architecture** axis (ESPR articles, CIRPASS four-layer, access tiers,
data carriers) lives in [[dpp-knowledge]]. **This** skill owns the **technical realisation
in AAS** and **compliance verification**: the standards-to-submodel mapping, verified
idShorts/semanticIds, value lists, and an actionable checklist.

Four jobs this skill serves:
1. **Q&A / reference** — JTC 24 module map, IDTA deliverable catalogue + status, the AAS↔DPP relationship.
2. **Extraction / validation** — given an AASX/submodel, locate the DPP-relevant fields and check structure.
3. **Mapping** — DPP requirement → AAS submodel → idShort → semanticId → valueType → cardinality.
4. **Compliance checking** — verify a passport/file against the legal + standards requirements and flag gaps.

> **Anti-drift rule (carried from project memory):** every idShort/semanticId below is copied
> verbatim from the official IDTA specs (2025-2026 releases). When the live IDTA template
> disagrees with this file, **the live template wins** — re-verify before encoding, and
> never invent submodel IDs (e.g. there is **no** "Maintenance 02018"/"Recycling 02077" in
> the battery DPP — it uses the 02035 series only).

---

## 1. What a DPP is (one paragraph)

A DPP is a structured digital record of a product's characteristics across its lifecycle
(circularity, material composition, repairability, carbon footprint, …), mandated under the
**ESPR — Regulation (EU) 2024/1781**. Rollout: **Battery Passport mandatory Feb 2027**
(EU Battery Regulation **2023/1542**, Art. 77 + Annex XIII); the ESPR Working Plan COM(2025) 187
gives *indicative adoption* years (not application dates) of 2026 for iron & steel and 2027 for
textiles/apparel;
by **2030 almost all industrial products** are expected to be covered. The DPP is **delivered
to the market as a single JSON document** but is best **produced from a modular AAS**.

---

## 2. Standards landscape (the reference job)

### 2.1 CEN-CENELEC JTC 24 — the 8 horizontal "modules" (all :2026)

JTC 24 writes the *system* standards for the DPP. There are **8 modules**, not just 18216–18223
(memory note `project_aas_en_jtc24_compliance` listed only the 18216–18223 range — **add 18239
and 18246**). Verbatim from IDTA 02099-1 §1.2:

| EN | Module | Theme | Status (May 2026) |
|---|---|---|---|
| **EN 18219**:2026 | 1 | Unique identifiers | published |
| **EN 18220**:2026 | 2 | Data carriers & digital representation | published |
| **EN 18239**:2026 | 3 | Access-rights mgmt, info-system security, business confidentiality | **not yet released** |
| **EN 18223**:2026 | 4 | System interoperability (JSON payload) | published |
| **EN 18216**:2026 | 5 | Data processing / data exchange | published |
| **EN 18221**:2026 | 6 | Data storage, archiving, persistence | published |
| **EN 18246**:2026 | 7 | Data authentication, reliability, integrity | **not yet released** |
| **EN 18222**:2026 | 8 | APIs (lifecycle management + searchability) | published |

**OJ status (verified on EUR-Lex 2026-10-19):** Commission Implementing Decision
(EU) 2026/1736 of 14 July 2026 (OJ 15.7.2026) cites **six** of the eight: EN 18216,
18219, 18220, 18221, 18222, 18223 (:2026). **EN 18239 and EN 18246 are not cited.**
Under ESPR Art. 41(2), conforming DPPs are presumed to meet Arts. 10 and 11 only
"to the extent that those requirements are covered"; access rights (Art. 11(f))
and authentication/integrity (Art. 11(g)) need a clause-level check before relying
on the presumption. Details in [[dpp-knowledge]] §2.2 and §2.2a.

`EN 18221` (retention/archiving) is the **critical gap** for AAS-based DPPs. The metamodel has no
retention construct, but an IDTA template exists: **IDTA 02056 Data Retention Policies** v1.0
(2024-06-14) represents retention policies applied to AAS elements via semantic identifiers — "A data
retention policy defines how long data must be stored before it may be deleted", with the enforcing
requirement/law, validity timeframe and an audit log (§1.2 p.6). It does not set the legal DPP
retention period; that comes from the regulation (and enforcement is still a platform job).

### 2.2 IDTA deliverable catalogue (the AAS realisation)

| Deliverable | What it is | Status |
|---|---|---|
| **IDTA 02035** series (Parts 1–7) | Digital **Battery** Passport submodels (the first live DPP) | **Available** (1.0, Feb 2026). Newest in the IDTA published folder (registry, 2026-10-28): Parts 1, 2, 3 **1.1.0** (folder `1/1`; its PDF still carries only the V1.0 version history); Part 4 **1.0.2** and Part 7 **1.0.2** (folder `1/0/2`; JSON bug fix, the folder PDF is the 1.0.1 document of May 2026); Part 5 **1.0.2** (Aug 2026, PDF version history); Part 6 **1.0.1** (May 2026) |
| Digital Battery Passport Implementation Guideline (w/ Catena-X) | step-by-step DBP-as-AAS | **Available** (Feb 2026) |
| **IDTA 02099-1** "DPP – Part 1 Metadata" | the `DppMetadata` submodel; aligns to EN 18223/18222 | **Available** (1.0, 28.05.2026); **1.0.1 (08.07.2026)** "Bugfix release. Major changes: fix full expanded example." (p.2) |
| DPP Annexes to AAS Part 1 & Part 2 | DPP-specific annexes (API mapping) | member review → public ~Jun 2026 |
| White Paper "How to achieve a DPP using AAS" | architecture/API patterns | ~Jun 2026 (not yet) |
| AAS Spec **Release 26-01** | Part 1 (Metamodel) + Part 2 (API) formally aligned to EN 18223 & 18222 | end Jun–mid Jul 2026 (not yet) |
| AAS Spec **Release 26-02** | Part 4 Security + DPP Security Annex (follows EN 18239) | follows JTC 24 security (not yet) |

### 2.3 Two normative layers — do not confuse them

- **DPP *system* interoperability** comes from **JTC 24 EN 18xxx** + **IDTA 02099-1** (the metadata).
- **Battery *field* requirements** come from **DIN DKE SPEC 99100:2025-02** (which itself derives
  from EU Battery Reg 2023/1542 Art. 77 + Annex XIII + ESPR). The 7 battery submodels implement
  **99100**, *not* the EN standards directly. (Note: 02099-1 §2.1 contains a typo "DIN DKE SPEC 91100";
  the correct number is **99100** per all 7 battery specs and the DBP guideline.)
- To compliance-check **battery field completeness** you need **DIN DKE SPEC 99100** (paid, dinmedia.de).
  Without it this skill verifies **structure** (idShorts/semanticIds/cardinalities/value-lists),
  not the full mandatory-field set.

---

## 3. The core mapping — `DppMetadata` (IDTA 02099-1) & AAS↔DPP

### 3.1 Key principle (quote the spec)

> "An AAS is **not, by itself**, the Digital Product Passport… **However, a DPP can be derived
> from an existing AAS.**" The AAS is **modular** (independent, reusable submodels); the JTC 24
> DPP is **monolithic** (one JSON). The AAS **dynamically assembles** the monolithic document by
> aggregating its registered submodels' payloads.

A compliant DPP must validate against **≥2 schemas**: (a) the generic EN 18223 schema, plus
(b) the vertical "delegated-act" schema (e.g. Battery Passport), plus (c) any horizontal-regulation schemas.

### 3.2 `DppMetadata` submodel — verbatim field table

- **idShort:** `DppMetadata` — **semanticId:** `https://admin-shell.io/idta/cds/dppMetadata/1`
- Derived from the IDTA 02006 Nameplate family. **Every DPP** carries exactly this header.
- All field semanticIds follow `https://admin-shell.io/idta/cds/<field>/1`.

| idShort | semanticId | valueType | card. | Maps to AAS | Notes |
|---|---|---|---|---|---|
| `digitalProductPassportId` | …/cds/digitalProductPassportId/1 | String | 1 | `AssetAdministrationShell/id` | similar but not necessarily equal (DPP = monolithic snapshot) |
| `uniqueProductIdentifier` | …/cds/uniqueProductIdentifier/1 | String | 1 | `AssetInformation/globalAssetId` (= Nameplate `URIOfTheProduct`) | format per **EN 18219** |
| `granularity` | …/cds/granularity/1 | String | 1 | `assetKind` (see 3.3) | Model / Item / Batch |
| `dppSchemaVersion` | …/cds/dppSchemaVersion/1 | String | 1 | — | EN 18223 defines no schema yet |
| `dppStatus` | …/cds/dppStatus/1 | String | 1 | — | e.g. "Active"; no enum in EN 18223 |
| `lastUpdate` | …/cds/lastUpdate/1 | DateTime | 1 | `AdministrativeInformation/updatedAt` | EN 18223 versions **via lastUpdate**, not explicit versioning; ISO 8601 UTC |
| `economicOperatorId` | …/cds/economicOperatorId/1 | String | 1 | — | format per **EN 18219** |
| `facilityId` | …/cds/facilityId/1 | String | 0..1 | Nameplate `UniqueFacilityIdentifier` | format per **EN 18219** |
| `contentSpecificationIds` | …/cds/contentSpecificationIds/1 | SML | 0..1 | ~ `AAS/submodels` | list of the DPP's content sets |
| ↳ `contentSpecificationId` | …/cds/contentSpecificationId/1 | String | 1..* | — | **value = the `semanticId` of each contributing Submodel Template** |

`contentSpecificationIds` SML rule: `orderRelevant=No, typeValueListElement=Property, valueTypeListElement=xs:string`.
Recommendation: use each contributing submodel's **semanticId** as the content id; if a product is
under several regulations, add all of them (one DPP, not one-per-regulation); always reference the
**newest** version of a submodel present in the AAS.

### 3.3 `granularity` → `assetKind` enum

| EN 18223 granularity | semanticId | AAS AssetKind | supplementalSemanticId |
|---|---|---|---|
| Model | …/cds/model/1 | Type | …/aas/3/2/AssetKind/Type |
| Item | …/cds/item/1 | Instance | …/aas/3/2/AssetKind/Instance |
| Batch | …/cds/batch/1 | Batch | …/aas/3/2/AssetKind/Batch |

(`Role` / `NotApplicable` AssetKinds have **no** ESPR equivalent.)

### 3.4 Serialization mapping (EN 18222/18223 ↔ AAS)

| EN 18223 format | AAS serialization | Mandatory? |
|---|---|---|
| **compressed** | **Value-Only** | yes (default) |
| expanded / full | Normal | optional |

The **DppMetadata** payload itself maps to **Value-Only** (one correct serialization, since it is part
of the overall schema). DPP API operations (EN 18222: ReadDPPById, ReadDPPByProductId, CreateDPP,
UpdateDPPById via JSON Merge Patch RFC 7396, DeleteDPPById, ReadDataElement…) map to AAS Part-2
service operations + discovery via the AAS Discovery Service (see the DPP API Annex; full mapping in
`/tmp/dpp_api_annex.txt`).

---

## 4. The Digital **Battery** Passport — reference implementation (IDTA 02035)

The DBP is the **only live DPP** and the template for every future product group. It is **7 submodels**
(plus `DppMetadata`). Field requirements come from **DIN DKE SPEC 99100**.

### 4.1 Composition table

| Part | idShort / submodel | semanticId | Derived from | Granularity |
|---|---|---|---|---|
| **1** Digital Nameplate | `BatteryNameplate` | `https://admin-shell.io/idta/digitalbatterypassport/nameplate/1/0/Nameplate` | 02006 Digital Nameplate v3 | **Item**, static |
| **2** Handover Documentation | `HandoverDocumentation` | `0173-1#01-AHF578#003` | 02004 Handover Doc v2 (VDI 2770) | model |
| **3** Product Carbon Footprint | `CarbonFootprint` | `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/1/0` | 02023 Carbon Footprint v1 (subset) | **Model per plant** (uses `facilityId`) |
| **4** Technical Data | `TechnicalData` | `https://admin-shell.io/idta/digitalbatterypassport/TechnicalData/1/0` | 02003 Generic Technical Data v2 (instance) | model |
| **5** Product Condition | `ProductCondition` | `urn:samm:io.admin-shell.idta.batterypass.product_condition:1.0.2#ProductCondition` (1.0.2; 1.0.0 and 1.0.1 used `…:1.0.0#ProductCondition`, and 1.0.2 moves every element semanticId to the `:1.0.2#` namespace too) | BatteryPass project | **Item**, **dynamic** |
| **6** Material Composition | `MaterialComposition` | `urn:samm:io.admin-shell.idta.batterypass.material_composition:1.0.0#MaterialComposition` | BatteryPass project | model |
| **7** Circularity | `Circularity` | `urn:samm:io.admin-shell.idta.batterypass.circularity:1.0.0#Circularity` | BatteryPass project | model |

> A new DPP (new `digitalProductPassportId`) must be issued when `LifeCycleStage`/`batteryStatus`
> changes (remanufactured/repurposed/re-used) and the battery is re-placed on the market.

### 4.2 Per-submodel essentials, value lists & gotchas

**Part 1 — `BatteryNameplate`** (semanticId root `…/digitalbatterypassport/nameplate/1/0/`)
- `URIOfTheProduct` (IRDI `0112/2///61987#ABN590#002`) ⇒ **`AssetInformation/globalAssetId`** = `DppMetadata.uniqueProductIdentifier`. This is the DPP identity anchor.
- Mandatory beyond base 02006: `SerialNumber`, `DateOfManufacture`, `UniqueFacilityIdentifier`, `Markings`, `LifeCycleStage`, `ManufacturerIdentifier`, `EUDeclarationOfConformity`, `ResultsOfTestReportsProvingCompliance`.
- `AddressInformation` is an **SMC drop-in** (semanticId `https://admin-shell.io/zvei/nameplate/1/0/ContactInformations/AddressInformation`) used by Nameplate & PCF; mandatory subset per the Nameplate spec: `Street`, `Zipcode`, `CityTown`, `NationalCode`. ⚠ **Correction:** the SMC form is defined in the **Nameplate (IDTA-02006) ContactInformation context** (which *references* IDTA-02002) — **IDTA-02002 v1.0 itself has flat address Properties inside `ContactInformation`, no `AddressInformation` SMC**. Don't cite 02002 as the SMC source.
- **`LifeCycleStage`** value list (`0173-1#02-ABL841#001`, `batteryStatus`): `original` (`0173-1#07-ACC020#001`), `repurposed`, `re-used`, `remanufactured`, `waste`.

**Part 2 — `HandoverDocumentation`** (VDI 2770; the **document store** of the whole DBP)
- All PDFs/files referenced by Parts 1/3/5/7 live **here**. Other submodels carry a **`DocumentIdentifier`** which must **match** a `DocumentId` in Handover Doc to resolve the file. (Validation: every `DocumentIdentifier` referenced elsewhere must exist here.)
- VDI 2770 `DocumentClassification` mapped to DIN DKE SPEC 99100: `02-04` Certificates/declarations (EU DoC, test reports, PCF study, due-diligence); `03-01` Commissioning/decommissioning (dismantling); `03-03` General safety (safety measures); `03-02` Operation (waste-prevention, separate-collection, end-of-life info); `03-04` Inspection/maintenance/testing (accidents).
- Structure: `Documents` (SML) → `Document` (SMC) → `DocumentClassifications` / `DocumentIds` / `DocumentVersions`. A `DocumentVersion` needs ≥1 `DigitalFile` (PDF/A per VDI 2770).

**Part 3 — `CarbonFootprint`** (subset of 02023)
- `ProductCarbonFootprints` (SML) → `ProductCarbonFootprint` (SMC) with: `PcfCO2eq` (`0173-1#02-ABG855#003`, decimal), `ReferenceImpactUnitForCalculation` (`…ABG856#003`), `QuantityOfMeasureForCalculation` (`…ABG857#003`), `PcfCalculationMethods` (SML), `LifeCyclePhases` (SML), `PerformanceClass`, `WebLinkToPublicCarbonFootprintStudy` (→ Handover `DocumentIdentifier`).
- **`PcfCalculationMethod`** — ECLASS `0173-1#09-AAO115#003` gives a **recommended** coded list (EN 15804, GHG Protocol, IEC TS 63058, ISO 14040/14044, **ISO 14067**, PEP Ecopassport, PACT v1/2/3, Catena-X v1/2/3, BS PAS 2050, IEC 63372…) **but the IDTA SAMM model types it as free-text `xs:string` (IRDI `0173-1#02-ABG854#003`), NOT a closed enum** — treat the list as recommended, not enforceable. Catena-X likewise has no single calc-method enum (uses `crossSectoralStandards` list + IPCC characterization-factors enum).
- **`LifeCyclePhase`** value list (ECLASS `0173-1#09-AAO113#003`, IDTA 02023 Table 13): the values are **labelled
  strings** with a valueId, e.g. `A1 - raw material supply (and upstream production)` (`0173-1#07-ABU208#003`),
  `A3 - production`, `A4 - transport to final destination`, `C3 - recycling, waste treatment`; only the ranges are
  bare codes (`A1-A3` `0173-1#07-ABZ789#003`, `A4-A5`, `B1-B7`, `C1-C4`, `C2-C4`). IDTA 02035-3 1.1.0 (PDF p.9)
  names exactly those labels for batteries ("based on DIN DKE SPEC 99100"). The SAMM `LifeCyclePhaseEnum` (§8.3)
  uses bare codes (`A1`, `A3`); a checker must accept the Table 13 label (compare the code before " - ", or the
  valueId), never reject "A3 - production". (Model must contain at least one **total** PCF entry covering all phases.)

**Part 4 — `TechnicalData`** (instance of 02003; semanticIds `urn:samm:io.admin-shell.idta.batterypass.technical_data:1.0.0#…`)
- `GeneralInformation` (manufacturer, `BatteryCategory`, `WarrantyPeriod`, `BatteryMass`) + `TechnicalPropertyAreas` (SMC, **not** SML in this instance): `CapacityEnergyVoltage`, `RoundTripEnergyEfficiency`, `Resistance`, `PowerCapability`, `Temperature`, `Lifetime`.
- **`BatteryCategory`** value list: `lmt`, `ev`, `industrial`, `stationary`.

**Part 5 — `ProductCondition`** (dynamic, **item-level**)
- Every dynamic datapoint is a pair `{value, LastUpdate}` (`LastUpdate` = `xs:dateTime`, `lastUpdate` IRDI `0173-1#02-ABG740#003`). Members: `EnergyThroughput`, `CapacityThroughput`, `NumberOfFullCycles`, `StateOfCertifiedEnergy`, `RemainingEnergy`, `RemainingCapacity`, `NegativeEvents`, `InformationOnAccidents`, `TemperatureInformation`, `RemainingPowerCapability`, `EvolutionOfSelfDischarge`, `CurrentSelfDischargingRate`, `RemainingRoundTripEnergyEfficiency`, `StateOfCharge`.

**Part 6 — `MaterialComposition`** (model)
- `BatteryChemistry` (`ShortName` e.g. "NMC", `ClearName`), `BatteryMaterials` (SML of `BatteryMaterial`: `BatteryMaterialIdentifier` = **CAS number** `0173-1#02-ABH034#003`, `IsCriticalRawMaterial` boolean, `BatteryMaterialMass`), `HazardousSubstances` (SML).
- **`HazardousSubstanceClass`** value list (CLP): `AcuteToxicity`, `SkinCorrosionOrIrritation`, `EyeDamageOrIrritation`, … (`HazardousSubstanceIdentifier` = CAS).

**Part 7 — `Circularity`** (model; semanticIds `urn:samm:io.admin-shell.idta.batterypass.circularity:1.0.0#…`)
- `DismantlingAndRemovalInformation`, `SparePartSources` (supplier name/address/email/components), `RecycledContentInformation`, `SafetyMeasures` (`SafetyInstructions` + `ExtinguishingAgents`), `EndOfLifeInformation` (`WastePrevention`/`SeparateCollection`/`InformationOnCollection`), `RenewableContent` (`0173-1#02-ABL867#001`).
- **`RecycledContent.RecycledMaterial`** value list: `Cobalt`, `Nickel`, `Lithium`, `Lead`. Shares `PreConsumerShare`/`PostConsumerShare` (xs:float).
- **`ExtinguishingAgent`** — ⚠ **free-text `xs:string`, NOT an enforced enum** in the TTL (`samm-c:List` of strings). The "A/B/C/D/K" classes (EUBR Annex VI Part A(9)) are only a prose hint — do **not** validate as a closed list.

### 4.3 Live-data onboarding (optional, ties to EU Data Act)
If the AAS must pull live machine values into DPP submodels, the **AID** (Asset Interface Description)
+ **AIMC** (Asset Interfaces Mapping Configuration, **IDTA 02027 v2.0**) + a **Data Mapping Processor**
define source→sink mappings (Lua transformations, Modbus/HTTP/MQTT/OPC UA/BACnet). 02027 explicitly
names DPP + EU Data Act as drivers.

---

## 5. Compliance checklist (the "checking" job)

**A. DPP-level (every DPP, via `DppMetadata` + EN 18223):**
- [ ] `DppMetadata` submodel present with semanticId `…/cds/dppMetadata/1`.
- [ ] All 7 mandatory header fields set (of 9; `facilityId` and `contentSpecificationIds` are 0..1, 02099-1 §3.1 p.14-18); `facilityId` present if granularity/footprint requires it.
- [ ] `uniqueProductIdentifier` == `AssetInformation/globalAssetId` == Nameplate `URIOfTheProduct`; format per EN 18219.
- [ ] `granularity` value ↔ `assetKind` consistent (Model↔Type, Item↔Instance, Batch↔Batch).
- [ ] `contentSpecificationIds` lists the **semanticId of every contributing submodel**, newest version.
- [ ] `lastUpdate` is ISO-8601 UTC; updates bump it (no explicit versioning expected by EN 18223).
- [ ] DPP serialises to **compressed/Value-Only**; validates against generic EN 18223 schema **and** the vertical schema.
- [ ] Identifiers/data carriers per EN 18219 (Module 1) & EN 18220 (Module 2); access control planned per EN 18239 (Module 3, pending); retention per EN 18221 (Module 6) — **flag: AAS-native gap**.

**B. Battery-specific (DIN DKE SPEC 99100):**
- [ ] All 7 IDTA 02035 submodels present with the exact semanticIds in §4.1.
- [ ] Granularity per submodel matches §4.1 (Nameplate/Condition = item; PCF = model-per-plant; rest = model).
- [ ] Every `DocumentIdentifier` (in Parts 1/3/5/7) resolves to a `DocumentId` in Part 2 Handover Doc.
- [ ] **Enforceable enums** validated as closed lists (§8.3): `LifeCycleStage` (IDTA lowercase/hyphenated form), `BatteryCategory`, `HazardousSubstanceClass`, `RecycledMaterial`, `LifeCyclePhase`. **Recommended-not-enforced** (free-text in the model): `ExtinguishingAgent`, `PcfCalculationMethod` — flag unknown values as advisory, not as errors.
- [ ] Critical-raw-material flag, CAS identifiers, hazardous-substance concentrations present where mandated.
- [ ] PCF has ≥1 total entry (all phases) + per-phase entries; `PerformanceClass` set per Art. 7 timing.
- [ ] Dynamic Product-Condition datapoints each carry `LastUpdate`.
- [ ] New `digitalProductPassportId` on lifecycle-stage change (remanufactured/repurposed/re-used).

**C. Structural / AAS hygiene (delegate detail to [[aas-validation]] & [[iec61360]]):**
- [ ] SML attributes set (`orderRelevant`, `typeValueListElement`, `valueTypeListElement`, `semanticIdListElement`).
- [ ] `valueType` correct per IEC 61360 / ECLASS data type (table §6.2).
- [ ] `File` elements have `contentType` + resolvable path; `Blob` base64 + contentType.
- [ ] semanticIds match the **current** IDTA template (re-verify; mapping-drift guard).

---

## 6. Mapping / extraction cheat-sheet

### 6.1 "Where does requirement X live?"
- Product identity / manufacturer / DoC / markings → **Part 1 Nameplate**
- Any document/PDF (safety, dismantling, due-diligence, test reports) → **Part 2 Handover Doc** (referenced by `DocumentIdentifier`)
- CO₂ footprint, performance class → **Part 3 PCF**
- Capacity/voltage/resistance/lifetime/power → **Part 4 Technical Data**
- State-of-health, cycles, accidents, live condition → **Part 5 Product Condition**
- Chemistry, materials, CRMs, hazardous substances → **Part 6 Material Composition**
- Dismantling, spare parts, recycled content, EoL, extinguishing → **Part 7 Circularity**
- The 9 DPP header fields (7 mandatory) → **`DppMetadata` (02099-1)**

### 6.2 IEC 61360 / ECLASS data type → AAS `valueType` (feeds [[iec61360]])
From the IDTA "How to transport ECLASS in the AAS" guide (2024-10):

| ECLASS data type | AAS element / valueType |
|---|---|
| REAL_MEASURE / REAL_COUNT / REAL_CURRENCY | `Property` `xs:float` (or `xs:double`); MEASURE adds `unit`+`unitId` |
| INTEGER_COUNT / INTEGER_MEASURE / INTEGER_CURRENCY | `Property` `xs:integer` |
| RATIONAL / RATIONAL_MEASURE | `Property` `xs:string` |
| BOOLEAN | `Property` `xs:boolean` (+ `valueId` for the enumerated literal) |
| STRING (direct, not translatable) | `Property` `xs:string` |
| STRING (indirect = value list) / STRING_TRANSLATABLE | `MultiLanguageProperty` (+ `valueId` from the list) |
| DATE / TIME / TIMESTAMP | `Property` `xs:date` / `xs:time` / `xs:dateTime` |
| URI | `MultiLanguageProperty`, ConceptDescription dataType `STRING` |
| FILE | `File` (`value`=path, `contentType`) |
| BLOB | `Blob` (base64 `value`, `contentType`) |

- **Identifiers:** dual notation — IRI `https://api.eclass-cdp.com/0173-1-02-AAC895-008` **or** IRDI `0173-1#02-AAC895#008`. Primary semanticId on IDTA `cds/…` concepts; ECLASS/IEC-CDD added as **`supplementalSemanticId`** (or `IsCaseOf` in newer specs).
- **Multiple values** of one property ⇒ wrap in an **SML** (a `Property` carries one value).
- ECLASS Advanced: **Aspect** → SM or SMC; **Block** → SMC; **Cardinality** → SML+SMC; **Polymorphism** → SMC (URI-path notation `…#003~0` for repeated blocks).

---

## 7. Sources & status (auditability)

All field-level data above is transcribed from the official IDTA PDFs (primary source), access date 2026-06-26:
IDTA **02099-1** v1.0 (28.05.2026; 1.0.1 of 08.07.2026 since published) · IDTA **02035-1…7** v1.0 (18.02.2026; later bug-fix releases, see §2.2) · DBP Implementation Guideline
v1.0 (19.02.2026) · IDTA **02006** v3.0.1 · **02004** v2.0 · **02003** v2.0 · **02023** v1.0 · **02027** v2.0 ·
"How to transport ECLASS in the AAS" v1.0 (2024-10) · IDTA 2-pager "AAS is ready for the EU DPP" (May 2026).
**Obtained 2026-06-26 (free, verified — see §8):** EUR-Lex **2023/1542** (Annex XIII, Art. 77, Art. 7, Annex VI A) & **2024/1781** (Chapter III, Arts. 9–15) verbatim; **Battery Pass Content Guidance / Longlist v1.2** (free DIN-99100 substitute, 93 attributes); IDTA + BatteryPass + Catena-X **SAMM/TTL** models; **CIRPASS D3.2** architecture; **ESPR Working Plan 2025-2030** (COM(2025) 187).
Still paid, and only needed for **formal clause-level conformance** (not for capability): **EN 18xxx** — note EN 18223 defines **no JSON schema yet**, so its marginal value now is low; **DIN DKE SPEC 99100** — field completeness is now covered by the free Longlist.

## 8. Verified ground truth (free primary sources — fetched 2026-06-26)

### 8.1 Legal field list — Battery Reg (EU) 2023/1542, Annex XIII (verbatim — the ground truth)
**§1 Public (battery model):** (a) Annex VI Part A info; (b) material composition / chemistry / hazardous substances / CRMs; (c) carbon footprint (Art. 7(1),(2)); (d) responsible sourcing per due-diligence report (Art. 52(3)); (e) recycled content (Art. 8(1)); (f) renewable content share; (g) rated capacity (Ah); (h) min/nominal/max voltage (+temp ranges); (i) original power capability (W) + limits; (j) expected lifetime in cycles + reference test; (k) capacity threshold for exhaustion (**EV only**); (l) non-use temperature range (reference test); (m) commercial warranty period (calendar life); (n) initial round-trip efficiency + at 50% cycle-life; (o) internal cell & pack resistance; (p) c-rate of cycle-life test; (q) marking (Art. 13(4) and (5), per corrigendum OJ L 2026/90285 of 10.4.2026; the OJ text said 13(3) and (4)); (r) EU DoC (Art. 18); (s) waste-battery prevention/management (Art. 74(1) a–f).
**§2 Legitimate-interest + Commission:** (a) detailed composition (cathode/anode/electrolyte); (b) part numbers + spare-part sources; (c) dismantling info (exploded diagrams, disassembly sequences, fasteners, tools, warnings, cell layout); (d) safety measures.
**§3 Notified bodies / market surveillance / Commission:** test reports proving compliance.
**§4 Individual battery, legitimate-interest:** (a) performance & durability values (Art. 10(1)) at placing + on status change; (b) state of health (Art. 14); (c) status = original/repurposed/re-used/remanufactured/waste; (d) usage data (cycles, negative events/accidents, operating conditions incl. temperature, state of charge).
Art. 77: applies **18 Feb 2027**; per-battery QR (Art. 13(6)) → unique identifier conforming to **ISO/IEC 15459 series**; three access tiers (public / legit-interest / authorities); **new passport on re-use/repurpose/remanufacture, linked to original (77(7)); passport ceases after recycling (77(8))**; legit-interest persons defined by implementing act due **18 Aug 2026 (77(9))**.
(A collapsed 3-tier lattice `public|professional|authority` maps legit-interest → `professional`, authorities → `authority`; see the implementation-mapping note in [[dpp-knowledge]] §5.)

### 8.2 Field-completeness checklist source (free DIN-99100 substitute)
**Battery Pass Consortium — Data Attribute Longlist v1.2 (Jan 2025)** = **93 attributes** across 7 clusters (Identifiers & product data · Symbols/labels/conformity · Carbon footprint · Supply-chain due diligence · Materials & composition · Circularity & resource efficiency · Performance & durability). Each row carries **mandatory(x)/voluntary(o) per category (EV/LMT/Industrial/Stationary)** + **access tier** + **Annex XIII ref** + **DIN DKE SPEC 99100 chapter** — it mirrors the paid 99100 attribute set → use it as the **per-category completeness gate**. Category-sensitivity is real: e.g. *remaining capacity / remaining power capability / remaining round-trip efficiency* are **mandatory for LMT & Stationary but voluntary for EV & Industrial**; *capacity threshold for exhaustion* is **EV-only**; *test reports* (#18) are authorities-tier. Full 93-row table: re-fetch `thebatterypass.eu/assets/images/content-guidance/pdf/2023_Battery_Passport_Data_Attributes.xlsx` (sheet `Data attribute longlist_v1.2`). (Stamped "Superseded by DIN-DKE-SPEC 99100" but aligned to it.)

### 8.3 Machine-readable models (exact enums/cardinalities — re-verify against these TTLs)
- `urn:samm:io.admin-shell.idta.dpp.dpp_metadata:1.0.0#` — DppMetadata; `facilityId` + `contentSpecificationIds` **optional**, the other 7 fields **mandatory**; `GranularityEnum` = `Model`/`Batch`/`Item`.
- `…idta.batterypass.digital_nameplate:1.0.0#BatteryStatusEnumeration` = `original` / `repurposed` / `re-used` / `remanufactured` / `waste` (IRDIs `0173-1#07-ACC020…024#001`).
- `…idta.batterypass.technical_data:1.0.1#BatteryCategoryEnum` = `lmt` / `ev` / `industrial` / `stationary`.
- `…idta.batterypass.material_composition:1.0.1#HazardousSubstanceClassEnum` = `AcuteToxicity` / `SkinCorrosionOrIrritation` / `EyeDamageOrIrritation`; CAS-number regex `^\d{2,7}-\d{2}-\d{1}$`; concentration `xs:double`.
- `…idta.batterypass.circularity:1.0.0#RecycledMaterial` = `Cobalt`/`Nickel`/`Lithium`/`Lead` (⚠ the source TTL lists each literal **twice** — dedupe to 4); shares `xs:float` % range 0–100.
- `…idta.carbon_footprint:1.0.0#LifeCyclePhaseEnum` = EN-15978 codes `A1`, `A1-A3`, `A2`, `A3`, `A4`, `A4-A5`, `A5`, `B1…B7`, `C1…C4`, `D`.
- Catena-X PCF: `urn:samm:io.catenax.pcf:9.0.0#` (PACT v3 aligned).
- ⚠ **NOT enums** (free-text `xs:string`): `ExtinguishingAgent`, `PcfCalculationMethod` (IDTA model). ⚠ **Casing divergence:** the BatteryPass consortium repo (`io.BatteryPass.*`) uses `Original/Repurposed/Reused/Remanufactured/Waste` — for **IDTA-conformant** DPPs use the **IDTA lowercase/hyphenated** form above. Two distinct lifecycle vocabularies coexist (IDTA generic `A1…D` vs BatteryPass 4-phase `RawMaterialExtraction/MainProduction/Distribution/Recycling`) — don't conflate. Source-name typos to transcribe literally if matching: `:HazardousSubstanceClassChrateristicEnum`, `:Documenttype` (BatteryPass repo).

### 8.4 ESPR retention/availability — grounded on FREE legal text (closes the EN 18221 gap)
Retention no longer needs the paid EN 18221: **ESPR Art. 9(2)(i)** — DPP must remain available **for at least the expected product lifetime**; **Art. 11(e)** — remains available **even after insolvency, liquidation or cessation** of the responsible operator; **Art. 11(c)/(d)** — stored by the operator or a DPP service provider, and a new DPP must be **linked to the original**; **Battery Reg Art. 77(7)/(8)** — new passport on status change linked to original, **ceases after recycling**. (Cross-ref `project_aas_en_jtc24_compliance` items F2/F5: duration is now groundable here without buying EN 18221.)

### 8.5 ESPR DPP system (Chapter III, Arts. 9–15) + roadmap
DPP essential requirements (Art. 10): connected via **data carrier** to a **persistent unique product identifier**; open-standard, interoperable, machine-readable, structured, searchable, **no vendor lock-in**; **no customer personal data without consent (GDPR)**; access-controlled per product-group delegated act. **Unique product / operator / facility identifiers** (Art. 12). **DPP registry** by **19 Jul 2026** (Art. 13 — stores UIDs + commodity code + battery UIDs per 2023/1542 Art. 77(3)). **Public web portal** to search/compare (Art. 14). **Customs** verify the registration identifier vs the registry (Art. 15). **ESPR Working Plan 2025-2030** (COM(2025) 187, 16.4.2025): textiles **2027**, tyres **2027**, furniture **2028**, mattresses **2029**, iron & steel **2026**, aluminium **2027**, repairability (horizontal) **2027**, EEE recycled-content/recyclability **2029**; mid-term review 2028.

### 8.6 CIRPASS architecture (free reference, cross-sector)
CIRPASS-2 **D3.2 DPP System Architecture v1.9** (cirpassproject.eu): Product UID (IEC 61406 / GS1 Digital Link) · **EU-Registry** ("resolver of resolvers", CSW-CERTEX customs link) · Data Carrier · **Resolver** (REO + Default EU) · **PDP (Policy Decision Point)** · **Decentralised DPP Data Repositories validated with SHACL** (regulators translate delegated acts → SHACL shapes; XSD only for syntax) · **Archives** (survive REO outage/insolvency) · plus a **DID / Verifiable-Credentials** variant. Role-based access flows: consumer / recycler / repairer / remanufacturer / authorities (customs + market surveillance). (Cross-sector attribute lists live in CIRPASS WP2 — D2.1/D2.3/roadmaps — not yet fetched.)

## Cross-links
- [[dpp-knowledge]] — ESPR regulatory framework, CIRPASS four-layer, access tiers, data carriers (regulatory axis).
- [[aas-knowledge]] — AAS metamodel, base submodel templates, AASX structure.
- [[iec61360]] — ConceptDescription / IEC 61360 data-spec content; **upgrade target** with §6.2 table.
- [[aas-validation]] — generic SML/valueType/cardinality validation; **upgrade target** with §4.2 value lists.
- [[aasx-format]] — File/Blob/MLP serialisation specifics.
