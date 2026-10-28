---
name: aas-knowledge
description: Asset Administration Shell (AAS, IDTA V3.1) domain expertise — metamodel essentials, the statically-checkable AASd-* constraints, IDTA submodel template catalogue (Nameplate / TechnicalData / CarbonFootprint / HandoverDocumentation / ContactInformation / Battery Passport 02035 / AID 02017 / CATENA-X), Battery Passport / DPP / EU 2023/1542 compliance, validation pipeline (XSD AAS 3.1 then AASd-*), vendor canonicalisation, EPD/PCF posture, and the non-obvious pitfalls of audit-grade AAS extraction. Use this skill whenever the user works with AAS files (.aasx, AAS XML, AAS JSON), the admin-shell.io namespace, IDTA submodel templates, AASd validation, Battery Passport / Digital Product Passport / EU 2023/1542, ECLASS IRDIs (`0173-1#02-AAxxx#nnn`), `aas-test-engines`, or product-datasheet → AAS extraction. Trigger even when the user names a specific submodel or property by IRDI/idShort/semanticId without saying "AAS" explicitly.
---

# AAS knowledge

Asset Administration Shell (AAS) is the IDTA V3.1 standard for digital twins
in industrial / regulatory contexts. This skill captures the **non-obvious**
domain knowledge: the metamodel rules the XSD cannot express, the submodel
template shapes, the Battery Passport regulatory anchors, and the gotchas
that get rediscovered every time someone touches an AAS file.

If the user is working with **anything** under `admin-shell.io`, .aasx files,
IDTA submodel templates, Battery Passport / DPP, ECLASS IRDIs, or the
`aas-test-engines` conformance gate — load this content and apply it.

---

## 1. AAS 3.1 metamodel essentials

**Namespace:** `https://admin-shell.io/aas/3/1` (this skill targets 3/1; "3/0" is legacy
and triggers an upgrade pass on import). The 3.2 XSD declares
`targetNamespace="https://admin-shell.io/aas/3/2"` (schemas/3.2/AAS.xsd:2); validate each
document against the XSD of its own namespace.

**Top-level entities:**
- `<environment>` — root container, holds `assetAdministrationShells`,
  `submodels`, `conceptDescriptions`.
- `<assetAdministrationShell>` — the shell. Has `idShort`, `id` (URN),
  `assetInformation`. AssetInformation has 5 children, in XSD order:
  `assetKind` (required), `globalAssetId?`, `specificAssetIds?`,
  `assetType?` (a legitimate string field — do NOT flag it as invalid),
  `defaultThumbnail?`.
- `<submodel>` — a named bundle of related properties. Has `idShort`, `id`,
  `kind` (`Instance` | `Template`), `semanticId`, `submodelElements`.
- `<conceptDescription>` — semantic definition; carries IRDIs and IEC61360
  data specification.

**Identification:**
- `id` is a URN (`urn:foo:bar`) or URL. `idShort` is a human label.
- `idShort` pattern (3.1): `^[A-Za-z][A-Za-z0-9_-]*[A-Za-z0-9_]$`
  - starts with a letter, ends with letter / digit / underscore (never `-`)
  - allowed chars: letters, digits, underscore, hyphen; at least two characters
  - 3.0 is different: `[a-zA-Z][a-zA-Z0-9_]*` — one letter suffices, NO hyphen
    (schemas/3.0/AAS.xsd:722-727), so `X` is legal and `Motor-1` illegal in a 3/0 document
  - **case-SENSITIVE** for uniqueness checks within a container, so `Foo` and
    `foo` are two distinct siblings and not a collision

> **Two corrections made 2026-08-02, after this file contradicted reality.**
> Found by cross-checking against the `aas-validation` skill and a production
> AASd validator; in both cases this file was the outlier:
> 1. idShort uniqueness said case-INSENSITIVE. IDTA-01001 v3.2 words AASd-003
>    and AASd-022 as "unique (case-sensitive)". Implementations compare verbatim
>    and lowercase only for AASd-116, where `globalAssetId` genuinely IS a
>    case-insensitive reserved name.
> 2. AASd-107 and AASd-108 were SWAPPED in the table below. 108 is the
>    `typeValueListElement` rule, which is the one that actually bites: a list
>    of `Property` that falls back to the `SubmodelElementCollection` default
>    serialises to invalid XML.
>
> The lesson worth keeping: a constraint NUMBER in a reference table is exactly
> the kind of fact nobody re-derives once it is written down, so it has to be
> checked against the spec text or an implementation, never against memory.
- `globalAssetId` is a SIMPLE string (URN or URL), NOT a `keys` structure.
  See §8 — this is one of the most common malformations.

**`assetKind`** (`AssetInformation.assetKind`):
- `Instance` — a specific physical asset (one battery, one motor)
- `Type` — a product line / SKU (the model, not the unit)
- `Role` — a role the asset plays (3.1 adds it: `assetKind_t` = Type | Instance | Role |
  NotApplicable, schemas/3.1/AAS.xsd:960-966)
- `NotApplicable` — abstract / placeholder
- Battery Passport requires `Instance` (it's about a SPECIFIC battery shipped to a customer).

**`modelType`** (the discriminator on every `submodelElement`):
- `Property` — single typed value (value + valueType)
- `MultiLanguageProperty` — langString array (each with `language` + `text`)
- `Range` — `min` + `max` + `valueType` (`min <= max` required)
- `SubmodelElementCollection` (SMC) — heterogeneous bag of children
- `SubmodelElementList` (SML) — homogeneous list (typeValueListElement)
- `File` — `value` (path) + `contentType` (MIME). Both optional in 3.1 (#412); `contentType` was required in 3.0.
- `Blob` — `value` (base64) + `contentType`. `contentType` optional in 3.1 (#412), required in 3.0.
- `ReferenceElement` — single `<value>` with `<type>` + `<keys>` shape
- `RelationshipElement` — `first` + `second` references. Both OPTIONAL in 3.1 (#412; aas-core-meta v3.1 `Optional["Reference"]`), required in 3.0. An exporter that drops a 3.1 relationship without them loses data.
- `AnnotatedRelationshipElement` — relationship + annotations
- `Operation` — `inputVariables` + `outputVariables` + `inoutputVariables`
- `Capability` — abstract action declaration
- `Entity` — `entityType` (`CoManagedEntity` | `SelfManagedEntity`) + globalAssetId
- `BasicEventElement` — `observed` reference + `direction` + `state` + `messageTopic`

**`valueType`** (Property + Range) — mandatory, cardinality 1 on Property (IDTA-01001 v3.0
PDF p.75); set it even for plain text (`xs:string`):

These MUST be the lowercase `xs:` names from XSD. **`xs:integer` is different
from `xs:int`** (xs:integer is unbounded; xs:int is 32-bit signed). Common:
- `xs:string`
- `xs:boolean`
- `xs:int` / `xs:long` / `xs:short` / `xs:byte`
- `xs:integer` / `xs:positiveInteger` / `xs:nonNegativeInteger` / `xs:negativeInteger`
- `xs:decimal` / `xs:float` / `xs:double`
- `xs:date` / `xs:dateTime` / `xs:time` / `xs:duration`
- `xs:gYear` / `xs:gYearMonth` / `xs:gMonth` / `xs:gDay`
- `xs:anyURI`
- `xs:hexBinary` / `xs:base64Binary`

**`langString*` shapes** (every multilingual field has a specific wrapper):
- `langStringNameType` — used by `displayName`
- `langStringTextType` — used by `description`
- `langStringPreferredNameTypeIec61360` — IEC61360 conceptDescription preferred name
- `langStringShortNameTypeIec61360` — IEC61360 short name
- `langStringDefinitionTypeIec61360` — IEC61360 definition

Each has the same shape: `<language>` (BCP 47 like `en`, `de`, `pt-PT`) +
`<text>`. **Both required and non-empty.** An empty langString is invalid.

**Reference shape** (`semanticId`, `dataSpecification`, etc.):
```xml
<reference>
  <type>ExternalReference</type>    <!-- or ModelReference -->
  <keys>
    <key>
      <type>GlobalReference</type>  <!-- or Submodel / Property / etc. -->
      <value>https://admin-shell.io/idta/nameplate/3/0/Nameplate</value>
    </key>
  </keys>
</reference>
```

Type can be `ExternalReference` (to anything outside) or `ModelReference`
(to elements inside this environment). Key types: `GlobalReference`,
`Submodel`, `SubmodelElementCollection`, `Property`, `MultiLanguageProperty`,
`Range`, `File`, `Blob`, `ReferenceElement`, `RelationshipElement`,
`Capability`, `Operation`, `BasicEventElement`, `Entity`, `Identifiable`,
`Referable`, `FragmentReference`, `AnnotatedRelationshipElement`,
`AssetAdministrationShell`, `ConceptDescription`, `EventElement`.

**IEC 61360 on a submodel element is allowed.** The usual home of a DataSpecificationIec61360
block is the ConceptDescription, but IDTA-01001 v3.1.2 (p.40) states: *"Submodel elements may
also have defined data specification templates. A template might be defined to mirror some of
the attributes like preferredName and unit of a property concept definition if there is no
corresponding concept description available."* So an embedded block on an element is a permitted
fallback, never an error by itself (details: [[iec61360]]).

### Reading AAS 2.0 XML: where IEC 61360 sits on a ConceptDescription (measured 2026-10-02)

A reader that only knows the 3.x shape finds NO IEC 61360 content on a 2.0 ConceptDescription. 3.1
wraps it as `<embeddedDataSpecifications><embeddedDataSpecification><dataSpecification>…
<dataSpecificationContent><dataSpecificationIec61360>` (one namespace, `<language>`/`<text>` langStrings).
Real AAS 2.0 packages (root `<aas:aasenv>`, namespace `http://www.admin-shell.io/aas/2/0`) look like this
(`RobotArm_sample.aasx`, trimmed):

```xml
<aas:conceptDescription>
  <aas:idShort>ManufacturerLogo</aas:idShort>
  <aas:identification idType="IRI">https://admin-shell.io/sandbox/SG2/TechnicalData/ManufacturerLogo/1/1</aas:identification>
  <aas:embeddedDataSpecification>                    <!-- SINGLE, directly under the CD: no plural wrapper -->
    <aas:dataSpecificationContent>
      <aas:dataSpecificationIEC61360>                <!-- aas namespace, "IEC" in capitals -->
        <IEC:preferredName>                          <!-- fields in xmlns:IEC="http://www.admin-shell.io/IEC61360/2/0" -->
          <IEC:langString lang="de">Herstellerlogo-Datei</IEC:langString>   <!-- language is an ATTRIBUTE -->
          <IEC:langString lang="en">File with manufactuer logo</IEC:langString>
        </IEC:preferredName>
        <IEC:unit />
        <IEC:dataType>STRING</IEC:dataType>
        <IEC:definition>…</IEC:definition>
      </aas:dataSpecificationIEC61360>
    </aas:dataSpecificationContent>
    <aas:dataSpecification>
      <aas:keys>
        <aas:key type="GlobalReference" local="false" idType="IRI">http://admin-shell.io/DataSpecificationTemplates/DataSpecificationIEC61360/2/0</aas:key>
      </aas:keys>
    </aas:dataSpecification>
  </aas:embeddedDataSpecification>
</aas:conceptDescription>
```

- The id is `<aas:identification idType="…">` (IRI, IRDI, Custom and IdShort all occur), not `<id>`.
- Key type, `local` and `idType` are ATTRIBUTES of `<aas:key>`; the 2.0 data-specification IRI is
  `http://admin-shell.io/DataSpecificationTemplates/DataSpecificationIEC61360/2/0` (3.x: aas-core-meta AASc-3a-050 gives
  `https://admin-shell.io/DataSpecificationTemplates/DataSpecificationIEC61360/3/0`; some tooling
  expects `…/DataSpecificationIec61360/3` — see [[iec61360]] §1).
- In these files the content comes BEFORE the reference, and some UR5e CDs carry content without a
  reference. `lang` values are not normalised (`de`, `DE`, `en`, `EN`, even `Default` and `EN?`).
- Prevalence: of 25 AAS 2.0 sample packages examined (22 distinct documents), 21 carry no
  ConceptDescription at all; the 4 that do (`Assembly_line_WithUR5Cobot.aasx`,
  `RobotArm_sample.aasx`, two byte-identical `UR5eCoBot_POLIMI LAB4.0_V2*.aasx`) all use this single
  `embeddedDataSpecification` shape, never a plural wrapper. Verified read-only (unzip of the
  `.aas.xml` part).

---

## 2. AASd-* metamodel constraints (XSD-uncatchable rules)

The official AAS 3.1 XSD validates **structure and types**. The **semantic
constraints** below come from the metamodel narrative and must be checked
separately. A file is valid only when it clears BOTH gates.

A production constraint gate typically implements a ~22-rule subset of these.

The most-checked constraints (ordered by where they typically fail):

> **Corrected 2026-09-14.** This table had drifted from the specification: it
> listed AASd-013 (removed in V2.0.1), AASd-090 and AASd-120 (removed in 3.1) as
> live rules, and gave AASd-014, 020, 026, 114, 117, 122, 124 and 125 meanings
> they do not have. The rows below are taken from [[aas-validation]], whose
> constraint catalogue is checked against the IDTA-01001 PDFs. **When this table
> and aas-validation disagree, aas-validation wins.**

| Rule | Topic | One-liner |
|---|---|---|
| AASd-002 | idShort pattern | At least two characters, letters/digits/hyphen/underscore, starts with a letter, does not end with a hyphen (3.1: `^[a-zA-Z][a-zA-Z0-9_-]*[a-zA-Z0-9_]+$`; 3.0 XSD: `[a-zA-Z][a-zA-Z0-9_]*`, one character allowed, no hyphen). |
| AASd-005 | version/revision | A `revision` requires a `version`. |
| AASd-012 | MLP value/valueId | If both `value` and `valueId` are present, each language string means what `valueId` references. (Not a uniqueness rule.) |
| AASd-014 | SelfManagedEntity | A SelfManagedEntity has a `globalAssetId` or a `specificAssetId`; relaxed in 3.1 together with `entityType` (#287). |
| AASd-020 | Qualifier value | 3.1: `Qualifier/value` is consistent with `Qualifier/valueType`. (Property value vs valueType is NOT a numbered constraint in 3.1.) |
| AASd-021 | Qualifier type | At most one Qualifier per `type` on a Qualifiable. |
| AASd-022 | idShort uniqueness | idShort of non-identifiable Referables is unique within its namespace, case-sensitive. |
| AASd-077 | Extension uniqueness | Extension `name` is unique within its `HasExtensions`. |
| AASd-107 | SML semanticIdListElement | A first-level child's `semanticId`, if set, equals `semanticIdListElement`. |
| AASd-108 | SML typeValueListElement | All first-level children have the type in `typeValueListElement`. |
| AASd-109 | SML valueTypeListElement | For Property/Range lists, `valueTypeListElement` is set and all children share it. |
| AASd-114 | SML semanticIds agree | If two first-level children have a `semanticId`, they are identical. |
| AASd-117 | idShort required | idShort of non-identifiable Referables not being a direct child of a SubmodelElementList shall be specified (IDTA-01001 v3.0 PDF p.106; "Bugfix" row p.168). |
| AASd-119 | kind alignment | A TemplateQualifier on a HasKind element implies `kind=Template`. |
| AASd-121 | Reference first key | The FIRST key of any Reference is a GloballyIdentifiable (AssetAdministrationShell, ConceptDescription, GlobalReference, Submodel). |
| AASd-122 | ExternalReference first key | The first key of an ExternalReference is a GenericGloballyIdentifiable (GlobalReference). |
| AASd-124 | ExternalReference last key | The last key of an ExternalReference is a GenericGloballyIdentifiable or a GenericFragmentKey. |
| AASd-125 | ModelReference keys | In a ModelReference with more than one key, every non-first key is a FragmentKey. |
| AASd-131 | AssetInformation id | `globalAssetId` or at least one `specificAssetId`. |

**Removed, never emit against 3.1:** AASd-013 (Range bounds, removed in V2.0.1),
AASd-026 (SMC allowDuplicates; removed when SMC was split and `allowDuplicates` dropped —
IDTA-01001 v3.0 PDF p.189),
AASd-090 (category, removed in 3.1, #514), AASd-120 (idShort on SML children,
removed in 3.1, #432). **Introduced later, never emit against 3.1:** AASd-137 and
AASd-138 (3.2).

**On the validator's output:** human-friendly messages cite the rule ID
(e.g., "AASd-119: kind 'Instance' incompatible with TemplateQualifier
present"). Treat that as the diagnostic anchor; the model path is the
location, the rule ID is the cause.

---

## 3. IDTA submodel template catalogue

The IDTA publishes versioned submodel templates with canonical semanticIds.
A submodel claiming a template MUST have its `semanticId` resolve to the
canonical IRI, and its element `idShort`s match the template's element
list (modulo strict optionality).

### Nameplate (IDTA-02006-3-0-1, v3.0.1)

semanticId: `https://admin-shell.io/idta/nameplate/3/0/Nameplate`. The 3.0
template re-keyed the IRI (it does NOT inherit the legacy
`zvei/nameplate/2/0/Nameplate` — a 3.0 consumer won't recognise the old
value). 3.0 re-keys the core properties to an **IEC-CDD primary** semanticId
(`0112/2///61987#...`) and carries the legacy ECLASS IRDI as a
`supplementalSemanticId`.

Key elements (primary = IEC-CDD; ECLASS shown as the supplemental IRDI):
- `URIOfTheProduct` (Property, `xs:anyURI`) — `0112/2///61987#ABN590#002` (suppl. `0173-1#02-ABH173#003`)
- `ManufacturerName` (MultiLanguageProperty) — `0112/2///61987#ABA565#009` (suppl. `0173-1#02-AAO677#004`)
- `ManufacturerProductDesignation` (MultiLanguageProperty) — `0112/2///61987#ABA567#009` (suppl. `0173-1#02-AAW338#003`)
- `OrderCodeOfManufacturer` (Property, `xs:string`) — **NOW MANDATORY in 3.0** — `0112/2///61987#ABA950#008`
- `ManufacturerProductFamily` (MultiLanguageProperty) — `0112/2///61987#ABP464#002` (suppl. `0173-1#02-AAU731#003`)
- `SerialNumber` (Property, `xs:string`) — `0112/2///61987#ABA951#009` (suppl. `0173-1#02-AAM556#004`)
- `YearOfConstruction` (Property, `xs:string`) — `0112/2///61987#ABP000#002` — **optional [0..1] since 3.0** (was [1] in 2.0; IDTA-02006-3-0-1 p.20, Annex B)
- `DateOfManufacture` (Property, `xs:date`) — `0112/2///61987#ABB757#007`
- `HardwareVersion` (Property, `xs:string`) — `0112/2///61987#ABA926#008`
- `FirmwareVersion` (Property, `xs:string`) — `0112/2///61987#ABA302#006`
- `SoftwareVersion` (Property, `xs:string`) — `0112/2///61987#ABA601#008`
- `CountryOfOrigin` (Property, `xs:string`, ISO 3166-1 alpha-2)
- `AddressInformation` (SMC, semanticId `https://admin-shell.io/zvei/nameplate/1/0/ContactInformations/AddressInformation`) — the address block used by Nameplate (mandatory Street/Zipcode/CityTown/NationalCode). ⚠ The SMC form is defined in the **Nameplate (02006) ContactInformation context** (which *references* IDTA-02002); **IDTA-02002 v1.0 itself has flat address Properties inside `ContactInformation`, no `AddressInformation` SMC** — don't cite 02002 as the SMC source.
- `UniqueFacilityIdentifier` (Property, `xs:string`) — ESPR / EU facility id
- `Markings` (SML of marking SMCs) — CE, RoHS, certification stamps
- `AssetSpecificProperties` (SMC) / `GuidelineSpecificProperties` (SML) — extensions

### TechnicalData (IDTA 02003, current 2.0.1)

semanticId (2.0 / 2.0.1): `0173-1#01-AHX837#002` (IDTA-02003-2-0-1 p.7, Table 1); the template
submodel's `id` is `https://admin-shell.io/idta/SubmodelTemplate/TechnicalData/2/0`. The
`https://admin-shell.io/ZVEI/TechnicalData/Submodel/1/2` IRI is the legacy 1.2 semanticId.

Top-level SMCs in the 2.0.1 template JSON: `GeneralInformation` (ManufacturerName, article
number, order code, ProductImage), `ProductClassifications` (ECLASS, IEC CDD, custom),
`TechnicalPropertyAreas` (the datasheet values),
`FurtherInformation`, `SpecificDescriptions`.

### CarbonFootprint (IDTA-02023-1-0, released v1.0 March 2025)

semanticId: `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/1/0`
(the v1.0 IRI; the draft `.../CarbonFootprint/0/9/...` shape is gone).

v1.0 reshaped the draft-0.9 layout:
- **`TransportCarbonFootprint` (TCF) was REMOVED in 1.0.** Don't emit it.
- PCF entries are now wrapped in the mandatory SML `ProductCarbonFootprints`
  (cardinality One) → child SMC `ProductCarbonFootprint`, so a product can
  carry MANY PCF blocks (one per lifecycle phase measured).
- The flat draft Properties became SMLs: `PcfCalculationMethods` and
  `LifeCyclePhases` (each a list of single-value Properties).
- idShorts are now `Pcf*` (mixed case), not the draft `PCF*`:
  - `PcfCalculationMethod` (e.g., "ISO 14067:2018", "EN 15804+A2:2019") — IRDI `0173-1#02-ABG854#003`
  - `PcfCO2eq` (Property, `xs:decimal`) — the headline number — IRDI `0173-1#02-ABG855#003`
  - `ReferenceImpactUnitForCalculation` (Property, `xs:string`) — IRDI `0173-1#02-ABG856#003`
  - `QuantityOfMeasureForCalculation` (Property, `xs:double`) — IRDI `0173-1#02-ABG857#003`
  - `LifeCyclePhase` (Property, `xs:string`, EN 15804+A2 phase codes) — IRDI `0173-1#02-ABG858#003`
  - `ExplanatoryStatement` (File — EPD / study report), `PublicationDate` /
    `ExpirationDate` (Property, `xs:dateTime`), `GoodsHandoverAddress` (SMC)
- v1.0 also adds the OPTIONAL `ProductOrSectorSpecificCarbonFootprints` SML
  (ZeroToOne) — the PACT / sector-rules subtree. Left empty by default.

### HandoverDocumentation (IDTA 02004-2-0-1, VDI 2770)

Current published version is **IDTA 02004-2-0-1** (`published/Handover
Documentation/2/0/1/` upstream). **1.2 is DEPRECATED** (moved to `deprecated/`)
— don't target it for new work.

submodel semanticId (2.0.x): ECLASS IRDI `0173-1#01-AHF578#003` (IDTA-02004-2-0-1 p.9,
Table 2). `https://admin-shell.io/idta/SubmodelTemplate/HandoverDocumentation/2/0` is the
template submodel's `id`, not its semanticId (2.0.1 template JSON) — a detector must match the
IRDI. Legacy: `.../idta/HandoverDocumentation/1/2`
or the VDI profile `https://admin-shell.io/vdi/2770/1/0/Documentation`.

Document-centric: a list of `Document` SMCs each with `DocumentVersion`,
`DocumentClassifications`, and a `File` pointing at the PDF.

**1.2 → 2.0.1 idShort renames (verified 2026-06-11 against both live
templates):** leaf renames `ValueId`→`DocumentIdentifier`,
`IsPrimary`→`DocumentIsPrimary`, `DocumentVersionId`→`Version`,
`SubTitle`→`Subtitle`, `Summary`→`Description`,
`OrganizationName`→`OrganizationShortName`; and the reference/entity slots
became PLURAL `SubmodelElementList`s: `RefersTo`→`RefersToEntities`,
`BasedOn`→`BasedOnReferences`, `TranslationOf`→`TranslationOfEntities`,
`DocumentedEntity`→`DocumentedEntities`, `Entity`→`Entities`. Mapping a 2.0.x
template by the old singular idShorts silently misses every field.

### ContactInformation (IDTA 02002-1-0)

semanticId: `https://admin-shell.io/zvei/nameplate/1/0/ContactInformations`

Hierarchical: `RoleOfContactPerson`, `NationalCode` (ISO 3166-1 alpha-2 —
e.g., "DE" not "Germany"), `Language`, `TimeZone`, `CityTown`, `Company`,
`Department`, `Phone`, `Fax`, `Email`, `Street`, `Zipcode`, `POBox`,
`AddressOfAdditionalLink`.

### Battery Passport (IDTA-02035 v1.0, EU 2023/1542)

See §4 for full treatment. The spec is **SEVEN separate submodels**, not one
monolith (Part 1 Nameplate, Part 2 Handover Documentation, Part 3 Product
Carbon Footprint, Part 4 Technical Data, Part 5 Product Condition, Part 6
Material Composition, Part 7 Circularity). The old fictional
`.../SubmodelTemplates/BatteryPassport/1/0` base does NOT exist — the real
published submodel-level semanticIds differ per part, e.g.:
- Part 1 → `https://admin-shell.io/idta/digitalbatterypassport/nameplate/1/0/Nameplate`
- Part 3 → `https://admin-shell.io/idta/CarbonFootprint/CarbonFootprint/1/0`
- Part 4 → `https://admin-shell.io/idta/digitalbatterypassport/TechnicalData/1/0`
- Parts 5-7 → SAMM aspect URNs (`urn:samm:io.admin-shell.idta.batterypass.<aspect>:1.0.0#<Aspect>`),
  e.g. Part 5 → `urn:samm:io.admin-shell.idta.batterypass.product_condition:1.0.0#ProductCondition`
  (IDTA-02035-5 p.11)
- Part 2 → IRDI `0173-1#01-AHF578#003`

Leaf properties carry an ECLASS IRDI (`0173-1#02-ABLxxx#nnn`) as the PRIMARY
semanticId with the SAMM aspect-model URN as `supplementalSemanticId`.

### DppMetadata (IDTA-02099-1, v1.0 28.05.2026 — the EN 18223 DPP header)

semanticId: `https://admin-shell.io/idta/cds/dppMetadata/1`; fields under
`…/cds/<field>/1`. The AAS-native realisation of the EN 18223 DPP metadata
header — add it to any DPP-bearing AAS so a monolithic DPP can be derived from
the modular AAS. 9 fields: `digitalProductPassportId`, `uniqueProductIdentifier`
(→ `globalAssetId`), `granularity` (→ `assetKind`; `Model`/`Batch`/`Item` ↔
Type/Batch/Instance), `dppSchemaVersion`, `dppStatus`, `lastUpdate` (→
`AdministrativeInformation/updatedAt`), `economicOperatorId` — all **mandatory**;
`facilityId` + `contentSpecificationIds` (list of contributing submodel
semanticIds) **optional**. An AAS is NOT itself a DPP — the DPP is *derived* from
it. Full DPP↔AAS compliance axis (mapping, value-lists, legal field list):
[[dpp-aas-compliance]].

### CATENA-X submodels (automotive supply chain)

- **SerialPart** (`https://catenax.io/.../SerialPart/1.0.0`) — twin per
  vehicle / part instance; key fields `partInstanceId`, `manufacturingDate`,
  `localIdentifiers[]`.
- **PCF** (`https://catenax.io/.../ProductCarbonFootprint/6.0.0`) — Catena-X
  flavour of carbon footprint, more granular than IDTA CarbonFootprint;
  required for OEM disclosure.
- **Traceability** (`https://catenax.io/.../Traceability/.../1.0.0`) —
  upstream/downstream relationships; the BoM (bill of materials) lattice.

### AID (IDTA 02017) — Asset Interface Description

For runtime data binding. Declares HTTP / MQTT / OPC-UA endpoints as
`Interface` SMCs, each with `Endpoints` and `Mappings` from a property in
the AAS to a datapoint on the wire. A separate poller / worker reads the
AID and projects live values into the AAS instance.

---

## 4. Battery Passport (EU 2023/1542 + IDTA-02035)

**Regulatory anchors:**
- **Regulation (EU) 2023/1542** ("Battery Regulation"), in force since
  Aug 2023. The DPP (Digital Product Passport) obligation lives in
  **Article 77**, technical content in **Articles 7-8 + Annex VI + Annex XIII**.
- **Article 77(1)**: from **18 February 2027** each LMT battery, each industrial
  battery >2 kWh and each EV battery placed on the market or put into service
  shall have a battery passport. Carbon-footprint disclosures (Article 7) have
  their own dates.
- **Article 8**: recycled-content declarations from Aug 2028.
- **Retention / availability** (the archival driver) — ⚠ **corrected:** there is
  **no "7-year" figure** in the texts (Battery Reg Art. 9 is about *performance &
  durability*, not retention). The real basis is **ESPR (2024/1781) Art. 9(2)(i)**
  — DPP available **for at least the expected product lifetime** — + **Art. 11(e)**
  — survives operator insolvency / liquidation / cessation — and **Battery Reg
  Art. 77(7)/(8)** — new passport on status change linked to original, **ceases
  after recycling**.
  Verified verbatim: [[dpp-aas-compliance]] §8.4.
- Not listed in Art. 77(1): portable batteries, SLI batteries and industrial
  batteries ≤2 kWh. LMT batteries ARE covered.

**The 35 required properties**, grouped:

1. **General identification (8)**
   - GTIN-13 / batch-instance ID
   - Manufacturer name + EU operator
   - Model + commercial name
   - Place + date of manufacture
   - Battery category (portable / LMT / industrial / EV / SLI)
   - Battery weight (kg)
   - Battery status — ⚠ IDTA enum is **lowercase/hyphenated** `original` | `repurposed` | `re-used` | `remanufactured` | `waste` (the BatteryPass consortium repo uses the capitalised `Original/Reused/…` form; use the **IDTA** form for conformance — see [[aas-validation]] §10.2)
   - Date of placing on market

2. **Performance and durability (10)** — Annex IV
   - Rated capacity (Ah) + nominal voltage (V)
   - Energy density (Wh/kg, Wh/L)
   - Rated power (W) / max continuous discharge
   - Internal resistance (mΩ)
   - Round-trip efficiency (%)
   - Cycle life @ rated DoD + reference test conditions
   - Calendar life (years)
   - Operating temperature range (°C)
   - Self-discharge rate (%/month)
   - State of Health (SoH) / State of Charge (SoC) thresholds

3. **Composition (9)**
   - Cathode chemistry (`LFP` | `NMC811` | `NMC622` | `NCA` | …)
   - Anode chemistry (`Graphite` | `Silicon-graphite` | …)
   - Electrolyte composition
   - Critical raw materials mass fractions: Cobalt / Lithium / Nickel /
     Natural graphite
   - Hazardous substances (REACH SVHC list, Annex XVII)
   - Recycled content per CRM (mass %, Annex II)

4. **Compliance + safety (5)**
   - CE conformity, declaration URL
   - UN 38.3 (transport safety) — pass/fail + report
   - IP rating (IP54 / IP67 / IP67/IP6K9K)
   - Hazard symbols (GHS pictograms)
   - WEEE / battery-mark (separate collection symbol, UN 3480, UN 3481)

5. **Supply chain due diligence (3)** — Article 49 / Annex X
   - Due-diligence policy URL + auditor
   - Risk-management policy URL
   - Verification of the four critical raw materials (Co, Li, Ni, NG)

**Distinction:** Article 7 (carbon footprint) is mandatory for
**industrial >2 kWh and EV** batteries from earlier dates than the full
DPP (Article 77). Portable and LMT batteries are excluded from §7 but
must comply with §8 (recycled content) on the later schedule.

**Common compliance gotchas:**
- `PCFCO2eq` MUST cite the calculation method (`ISO 14067:2018` /
  `EN 15804+A2` / `PEFCR Batteries`). A number without a method is
  rejected by independent auditors.
- Recycled-content figures need the chain-of-custody method (mass balance
  vs physical segregation). Default to leaving the field empty unless you
  have the document.
- `BatteryCategory` — ⚠ **corrected:** the machine-readable IDTA/BatteryPass SAMM
  enum is `lmt` / `ev` / `industrial` / `stationary` (lowercase; verified TTL
  `…batterypass.technical_data:1.0.1#BatteryCategoryEnum`). This differs from the
  EU 2023/1542 Art. 3 *legal* vocabulary (portable / LMT / industrial / EV / SLI /
  stationary). Validate DPP files against the **model enum**, not the legal prose
  list; misspellings fail conformance.

---

## 5. Validation pipeline order

**ALWAYS XSD first, THEN AASd-*.** The XSD catches structural problems
(missing required children, wrong nesting, malformed types) that would
make the AASd checks crash or produce misleading errors. AASd-* assumes
a structurally-valid tree.

```
input.xml
   │
   ▼
[1. AAS 3.1 XSD]      xmllint-wasm against admin-shell.io/aas/3/1.xsd
   │                  Catches: wrong namespace, missing required elements,
   │                  wrong types, malformed enums.
   ▼ structural OK?
[2. AASd-* gate]      Your semantic constraint gate.
   │                  Catches: the ~22 rules in §2 (idShort uniqueness,
   │                  ranges, references, lists, qualifiers, …).
   ▼ semantic OK?
[3. (optional) IDTA aas-test-engines]
                      The authoritative reference: the IDTA's own conformance
                      gate, run in CI. If our gate + IDTA disagree, IDTA wins
                      (we have a bug). 6 submodel families pass IDTA today:
                      Nameplate, TechnicalData, CarbonFootprint,
                      HandoverDocumentation, CATENA-X SerialPart, Battery
                      Passport.
```

A file reports `valid: true` only after stage 2 (and ideally 3). For
production responses: `validation: 'structural'` means XSD-only (use
when AASd is degraded); `validation: 'full'` means both passed.

**On error formatting:** the validator returns one row per error with
`{ severity, code (AASd-XXX or xs:type), message, path }`. The `path` is
the XML node location (e.g., `submodels[0].submodelElements[3].value`).
Render it as expandable cards, not a JSON dump — that's the centerpiece
UX of any AAS UI.

---

## 6. Vendor canonicalisation (POST-extraction lift)

After the LLM extracts a draft AAS from a datasheet, run a deterministic
**vendor canonicalizer** that lifts values to vendor-canonical form. This
is what gets you from 70% accuracy to 100% on known vendors.

**Principles:**
- **Run AFTER the LLM, not in the prompt.** Canonicalisation is
  deterministic substitution; mixing it into the prompt wastes tokens
  and trades determinism for LLM whim.
- **Match on brand-distinct keyword stems**, never generic vocabulary.
  The classic bug: "STEPS" matched a Xiaomi scooter listing into the
  Shimano BT-E80 e-bike template (Shimano's brand stem is "STEPS").
  Vendor templates SHOULD use multi-word stems ("Shimano STEPS",
  "BT-E80xx") and brand-only marketing names should be avoided.
- **`appliesTo: 'type' | 'instance' | 'both'`** — declares whether the
  template applies to a product family ID (e.g., "BYD Battery-Box
  Premium HVS") or a specific unit (which would have serial-number-
  level details). `'both'` is rare and risks over-application.

A vendor template carries:
- `id`, `idShort`, brand keywords (the matchers)
- For each field: canonical value (`ManufacturerName: "BYD Company Limited"`,
  not just "BYD"), insertion policy (`onlyIfEmpty` | `override`), and
  source citation (where in the vendor's published spec sheet).

---

## 7. EPD / PCF posture: verified-only

Battery datasheets rarely include `PCFCO2eq` because PCF lives in a
**separate EN 15804 / ISO 14067 document** (the EPD) and Article 7's
mandate is recent.

**The rule: verified-only.** Only PCF numbers from a publicly auditable
EPD document go into the registry. An "industry-typical" guess tagged
`epdSourced: true, tier: high` is **WORSE than an empty slot** — it
corrupts the audit trail that gets submitted to the regulator.

**Slot vacancy is the correct compliance signal.** A blank PCFCO2eq tells
the auditor "we don't have this verified; ask the supplier for the EPD"
— which is the correct outcome. A guessed number tells the auditor
"verified at tier:high" — which is fraud.

Apply this discipline to ALL audit-grade fields, not just PCF.

---

## 8. Pitfalls and non-obvious rules

Stuff that's bitten people in production. Reorder these in the prompt
when they're directly applicable.

- **"Empty over invented."** For audit-grade extraction, prefer absent
  to hallucinated. The auditor reads a missing field as "needs followup";
  reads a wrong field as a regulatory liability.
- **idShort sanitisation order matters.** Strip non-matching chars first;
  prepend "X" if it doesn't start with a letter; trim trailing hyphens;
  collapse double underscores. Apply ONCE on insert, not on every read.
- **`File.contentType`, when present, must be a real MIME** (it is optional in 3.1, required in 3.0). Common
  malformations: `application/x-pdf`, `pdf`, `.pdf`. Use
  `application/pdf`, `image/jpeg`, `image/png`, `text/csv`, etc.
- **`xs:integer` ≠ `xs:int`.** `xs:integer` is unbounded; `xs:int` is
  32-bit signed. The XSD validator catches this; LLM extractions often
  guess one when the other is correct.
- **Every `langString*` element needs BOTH `<language>` AND non-empty
  `<text>`.** An empty langString is silently invalid: the XML parses, but the
  schemas' `minLength 1` on `text` rejects it. (Not AASd-012, which is about an MLP's
  `value` matching its `valueId`, aas-core-meta v3.1 `:3037`; corrected 2026-10-02.)
- **ConceptDescription needs a `<definition>` block under the IEC61360
  wrapper.** Bare IRDI references without a `dataSpecificationIec61360`
  definition fail downstream IRDI resolvers.
- **References use the `<keys><key><type>X</type><value>...</value></key></keys>`
  shape.** Attributes on `<key>` (`<key type="GlobalReference" value="..."/>`)
  is a common malformation; the validator rewrites it.
- **`globalAssetId` is a simple string**, not a keys structure. This
  malformation accounts for ~10% of "why isn't my AASX importing"
  questions.
- **Multi-source consensus voting and multi-model ensemble are DIFFERENT
  mechanisms.** Multi-source = several distinct documents voted by
  authority weight. Multi-model = several LLMs voting on the same
  document, with an arbiter. They compose (multi-model per source, then
  multi-source over results), they don't substitute.
- **Battery Passport needs `assetKind: Instance`.** It's about a SPECIFIC
  battery shipped to a customer (with a serial number), not about the
  product family. Using `Type` is a common conformance-fail.
- **In a multi-key production env, use a canonical "decide single vs
  ensemble" entry point**, not direct LLM calls from
  routes. Single keeps single behaviour; multi auto-enables ensemble.
- **`jsdom` must stay pinned to 24.x in Vercel-style serverless Node.**
  jsdom 27+ depends on the ESM-only `@exodus/bytes`; serverless Node
  rejects `require(ESM)` with `ERR_REQUIRE_ESM` and the route 500s.

---

## 9. Authoritative references

When in doubt, consult these in this order:

- **IDTA submodel templates:**
  [industrialdigitaltwin.org → Submodels](https://industrialdigitaltwin.org/en/content-hub/submodels)
  — versioned PDFs + reference JSONs. The IRIs of canonical semanticIds
  live here.
- **AAS 3.1 metamodel + XSD:**
  [admin-shell.io](https://admin-shell.io) — the XSD, the metamodel
  specification, the AASd-* rule list.
- **Conformance gate:**
  [`aas-test-engines` on GitHub](https://github.com/admin-shell-io/aas-test-engines)
  — the IDTA's reference implementation. If your output fails this, it
  fails for everyone.
- **EU Battery Regulation:**
  Regulation (EU) 2023/1542, full text on
  [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2023/1542/oj).
  Art. 7 (carbon footprint), Art. 77 (battery passport, applies 18 Feb 2027),
  Annex VI Part A (labelling), **Annex XIII** (the verbatim DPP field list).
- **EU ESPR (the DPP framework regulation):**
  Regulation (EU) 2024/1781, [EUR-Lex](https://eur-lex.europa.eu/eli/reg/2024/1781/oj).
  Chapter III, Arts. 9–15 (DPP, requirements, identifiers, registry by 19 Jul 2026,
  web portal, customs). Working Plan 2025-2030 = COM(2025) 187.
- **CATENA-X standards:**
  [catena-x.net / standards library](https://catena-x.net/en/standard-library)
  — CX-* documents for SerialPart, PCF, Traceability, DPP.
- **ECLASS IRDIs:** [eclass.eu](https://www.eclass.eu) — Basic catalogue
  (free) and Standard (paid).
- **VDI 2770:** for HandoverDocumentation document-classification codes
  (manufacturer info, operating manual, declaration of conformity, etc.).
- **IEC 61360:** for ConceptDescription content (preferredName, definition,
  unit, valueFormat). Live in `dataSpecificationIec61360`.

---

## Behavioural notes for Claude using this skill

- When the user shows you an AAS file with a problem, **lead with the
  AASd-* rule ID** if one applies. The rule ID is the diagnostic anchor;
  it lets the user google the spec.
- When generating AAS, **always include semanticIds on submodels** from
  §3, even when the user didn't ask. A nameless submodel is a smell.
- When in doubt about a field's `valueType` or `idShort`, **cite the
  AASd rule** (e.g., "valueType takes the xs:* names; xs:integer is
  different from xs:int — which do you have?"). Don't silently guess.
- For Battery Passport work, **map every property to the EU 2023/1542
  category** in §4 in your explanations. The regulatory anchor is the
  trust signal.
- **Do not invent IRDIs.** If you don't have a curated IRDI, leave
  `semanticId` empty rather than hallucinate one.
- When the user is extracting from a datasheet, **prefer empty over
  invented** (§8). Audit trails are the product.
- When asked "is this valid?", **run both stages mentally** (XSD shape +
  AASd-* semantics) and report each. A pass on one is not a pass.
