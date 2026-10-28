---
name: iec61360
description: IEC 61360 Data Specification expertise for AAS ConceptDescriptions (IDTA-01003-a Part 3a v3.1.1). Covers DataSpecificationIEC61360's full element set (preferredName, shortName, definition, sourceOfDefinition, unit/unitId, valueFormat, value/valueId, valueList, levelType, dataType enum, symbol), the IRDI semanticId pattern (`0173-1#02-AAxxx#nnn`), how the spec couples to ConceptDescription categories (PROPERTY / VALUE / DOCUMENT / QUALIFIER and their AASc-3a constraints; the former AASd-050..075 were renamed to AASc or removed in 3.0), the langString wrappers (langStringPreferredNameTypeIec61360 / langStringShortNameTypeIec61360 / langStringDefinitionTypeIec61360), ECLASS Basic / Standard / Advanced catalogue tiers, IEC CDD interoperability, value-list shape (ValueReferencePair with value + valueId), and the common pitfalls of using IEC61360 in AAS. Use this skill whenever the user works with ConceptDescription, DataSpecificationIEC61360, semanticId resolution to a CD, IRDI lookups, ECLASS catalogue queries, langString wrappers in IEC61360 context, value-lists with coded values, or asks "what semanticId for my property". Trigger when the user mentions IEC 61360, IEC61360, IRDI, ECLASS, ConceptDescription, dataSpecificationIec61360, or pastes a CD definition.
---

# IEC 61360 data specification

IEC 61360 (ISO 13584-42) is the international standard for **electronic
exchange of characteristic data for components, materials, services**.
In the AAS metamodel, it's the canonical content schema for a
ConceptDescription. A `<dataSpecificationContent>` block carries
`<dataSpecificationIec61360>` with the structured IEC61360 fields.

**Source**: IDTA-01003-a Part 3a: Specification of the Asset
Administration Shell — Data Specification IEC 61360, v3.1.1 (official PDF from
industrialdigitaltwin.org, vendored at `idta-specs:pdf/`, paged text in `idta-specs:txt/`;
sha256 in `VERSION.json`). Part 3a v3.1.1 p.16: *"This specification is only valid in
combination with IDTA-01001-3-1."*

The IEC 61360 layer is what gives an AAS Property semantic
**resolvability**: "what does this idShort really mean?" → resolve its
semanticId to a ConceptDescription with an IEC61360 block, read the
preferredName / definition / unit / valueList there.

---

## 1. The element model

**Template IRI** (the `dataSpecification` ExternalReference value) — **settled by
Part 3a v3.1.1** (official PDF, `idta-specs:txt/IDTA-01003-a-3-1-1_…txt`):
- The template table (p.16) gives *"id: https://admin-shell.io/DataSpecificationTemplates/DataSpecificationIec61360/3"*
  and lists four forms as *"<<deprecated>>"*: `https://…/DataSpecificationIec61360/3/0`,
  `http://…/DataSpecificationIec61360/3/0`, `https://…/DataSpecificationIEC61360/3/0`,
  `http://…/DataSpecificationIEC61360/3/0`. Why no minor version: *"with the exception
  that the minor version was excluded because this ID is also part of the instances of
  Asset Administration Shells"*.
- **AASc-3a-050** (p.40): *"If the _DataSpecificationContent_ DataSpecificationIec61360 is
  used for an element, the value of _HasDataSpecification/dataSpecification_ shall contain
  the external reference to the IRI of the corresponding data specification template
  `https://admin-shell.io/DataSpecificationTemplates/DataSpecificationIec61360/3`."*
  The change table "V3.0.2 vs. V3.0.1" (p.67) records the switch: *"Update Now
  https://admin-shell.io/DataSpecificationTemplates/DataSpecificationIec61360/3"*; V3.0 had
  `…/DataSpecificationIec61360/3/0` (p.68/69).
- So: **emit `https://admin-shell.io/DataSpecificationTemplates/DataSpecificationIec61360/3`**
  (casing `Iec61360`, no `/0`). The `/3/0` forms (either casing, http or https) are
  **deprecated, not invalid**: accept them on read and report them as deprecated, never
  as an AASc-3a-050 violation. aas-core-meta v3_0/v3_1/v3_2 still state the older
  `…/DataSpecificationIEC61360/3/0` in AASc-3a-050 (v3_0.py:5113, v3_1.py:5053-5059,
  v3_2.py:5373); Part 3a is the normative source and overrides it.

**Where the template lives: ConceptDescription by design, element allowed.**
aas-core-meta v3_1.py:5521 introduces the class as *"Content of data specification
template for concept descriptions for properties, values and value lists conformant to
IEC 61360."*, and its note says the IEC 61360 identifier is not in the template:
*"Instead the `Concept_description.ID` as inherited via `Identifiable` is used."* So
the normal home is a ConceptDescription, and the CD id is the concept id. Structurally,
though, `Submodel_element(Referable, Has_semantics, Qualifiable, Has_data_specification)`
(v3_1.py:2530) means any submodel element may carry `embeddedDataSpecifications` with
an IEC 61360 block, and that is not an error. **Normative status (settled 2026-10-28):
permitted, not recommended.** Part 1 v3.1.2 (p.40): *"Submodel elements may also have
defined data specification templates. A template might be defined to mirror some of the
attributes like preferredName and unit of a property concept definition if there is no
corresponding concept description available."* Part 3a v3.1.1 (p.16) describes the
template as *"Data specification template for concept descriptions for properties and
values conformant to IEC 61360."* So the recommended home is the ConceptDescription; an
embedded block on an element is a "may" fallback for when no CD is available, and no
source makes it mandatory or recommended in general. Some templates ask for it: IDTA-02020
p.23 (CapabilityPropertyType) lists *"hasDataSpecification: Reference to external
data definitions, e.g., unit of the property."* (verified in
`aas-capability-description/IDTA-02020_Submodel_Capability_Description.txt:1044-1045`,
page 23/44). See [[aas-capability-description]] for the unit recipe.

How the AASc-3a rules apply to an embedded block on an element:
- **AASc-3a-002** (preferredName at least in English, v3_1.py:5580) is on the
  content class itself, so it applies wherever the block sits: give `en`.
- **AASc-3a-009** (a `*_MEASURE` / `*_CURRENCY` dataType needs `unit` or `unitId`) is
  also on the content class: a `REAL_MEASURE` block on a Property needs `unit` too.
- **AASc-3a-008** (definition mandatory in English unless a value is described) is an
  invariant of `Concept_description` (v3_1.py:4262-4266, docstring :4330), not of the
  content class. A block embedded on a submodel element without `definition` does not
  violate it. Do not report it there.

`DataSpecificationIec61360` content (under
`embeddedDataSpecifications/embeddedDataSpecification/dataSpecificationContent`):

**XSD element order (DataSpecificationIec61360_t sequence) — emit in EXACTLY this order:**
`preferredName`, `shortName`, `unit`, `unitId`, `sourceOfDefinition`, `symbol`,
`dataType`, `definition`, `valueFormat`, `valueList`, `value`, `levelType`.
(`valueId` is a child of a `valueReferencePair` inside `valueList`, not a
top-level element.) The table below is descriptive (grouped by purpose), NOT
ordinal — serialize in the XSD order above or the document is schema-invalid.

| Element | Type | Cardinality | Purpose |
|---|---|---|---|
| `preferredName` | langStringPreferredNameTypeIec61360 | 1..n | The human-readable canonical name in each supported language; AASc-3a-002: shall be provided at least in English (aas-core-meta v3_1.py:5580-5581) |
| `shortName` | langStringShortNameTypeIec61360 | 0..n | Display-friendly short form (often domain abbreviation) |
| `definition` | langStringDefinitionTypeIec61360 | 0..n | Full prose definition in each language |
| `sourceOfDefinition` | string | 0..1 | Citation to the originating standard / publication |
| `unit` | string | 0..1 | Unit symbol (e.g. "kg", "°C", "m/s") |
| `unitId` | Reference | 0..1 | Reference to a unit ConceptDescription (the preferred form for unambiguity) |
| `valueFormat` | string | 0..1 | Format hint for the value (e.g. "##.##") |
| `value` | string | 0..1 | When the CD itself encodes a discrete VALUE (categories VALUE + DOCUMENT) |
| `valueId` | Reference | 0..1 | Reference to a coded value when the CD encodes a VALUE |
| `valueList` | collection of ValueReferencePair | 0..1 | Permitted values + their coded refs (when applicable) |
| `levelType` | set of {Min, Max, Nom, Typ} | 0..1 | Which level-type values the CD provides (used by Range / measurements) |
| `dataType` | DataTypeIec61360 (enum below) | 0..1 (AAS 3.1 XSD `minOccurs="0"`; corrected 2026-10-02 from 1..1) | The data type of the value the CD describes |
| `symbol` | string | 0..1 | Domain symbol (e.g. "ρ" for density) |

The element set is fixed by the spec — vendor extensions don't go here
(use `Extension` on the parent Referable instead).

**Emitting ConceptDescriptions: enriched, not idShort-fallback.**
A good serializer resolves each element's semanticId — and, when the
primary is an IEC-CDD / SAMM id, its `supplementalSemanticIds` — to a
**registered ECLASS / IDTA ConceptDescription** and fills the emitted CD with
the REAL `preferredName` / `definition` / `unit` / `dataType`, looking up a rich
ECLASS dataset first and a curated IRDI catalogue second. Only
when nothing resolves does it fall back to the element's own metadata + the
idShort. Element-supplied `preferredName` / `definition` still win over the
registry (an explicit value is never overwritten); it never fabricates a
preferredName for an unknown IRDI. This handles the IDTA pattern (Nameplate
3.0, Battery Passport) where the ECLASS IRDI rides as a supplemental.

---

## 2. The `dataType` enum (DataTypeIec61360)

The values the CD's `dataType` can take. Distinct from XSD's `xs:*`
types (Property.valueType) — they describe IEC61360 semantic categories,
not XML primitive types.

| Value | Maps to (typical xs:) | Used for |
|---|---|---|
| `STRING` | xs:string | Free text |
| `STRING_TRANSLATABLE` | langString | Text needing translations |
| `INTEGER_MEASURE` | xs:int / xs:integer | Counted integers (count, number-of) |
| `INTEGER_COUNT` | xs:int | Pure count |
| `INTEGER_CURRENCY` | xs:int (in cents) | Monetary integer values |
| `REAL_MEASURE` | xs:double | Real-valued measurement |
| `REAL_COUNT` | xs:double | Real count (e.g., fraction) |
| `REAL_CURRENCY` | xs:double | Monetary real |
| `BOOLEAN` | xs:boolean | True/false |
| `RATIONAL` | xs:string (formatted) | Rational number (a/b) |
| `RATIONAL_MEASURE` | xs:string | Rational with unit |
| `TIME` | xs:time | Time of day |
| `TIMESTAMP` | xs:dateTime | Date + time |
| `DATE` | xs:date | Calendar date |
| `FILE` | (binary) | File-typed value |
| `BLOB` | (binary) | Inline binary |
| `HTML` | xs:string (HTML payload) | Rich-text |
| `IRDI` | xs:string (IRDI form) | Identifier dictionary entry |
| `IRI` | xs:anyURI | URI; also covers URLs — there is no `URL` literal (3.1 XSD `dataTypeIec61360_t`; aas-core-meta v3_1.py:5140-5147) |

### dataType allowed per ConceptDescription category (AASc-3a-004/005/006)

The CD `category` constrains which `dataType` values are legal:

| category | allowed `dataType` |
|---|---|
| **PROPERTY / VALUE** | DATE, STRING, STRING_TRANSLATABLE, INTEGER_* (MEASURE/COUNT/CURRENCY), REAL_* (MEASURE/COUNT/CURRENCY), BOOLEAN, RATIONAL, RATIONAL_MEASURE, TIME, TIMESTAMP |
| **REFERENCE** | STRING, IRI, IRDI |
| **DOCUMENT** | FILE, BLOB, HTML |

Pick the `dataType` from the CD's category, not from the property's wire type.
(Tooling caveat: aas-test-engines 1.0.3 has a known false positive on
AASc-3a-004/005/006 — it compares the DataTypeIec61360 enum against a string
set and fires on any CD carrying a `category`. Don't trust that engine version
for these three rules; validate against the XSD.)

**Mapping rule**: Property.valueType (xs:*) is the WIRE type for the
value; CD.dataType is the SEMANTIC category. They must be compatible
(e.g., Property.valueType=xs:double pairs with CD.dataType=REAL_MEASURE,
not BOOLEAN).

---

## 3. langString wrappers (specific to IEC61360 in 3.x)

IEC61360 multilingual content uses dedicated wrapper types, distinct
from `langStringNameType` (used by displayName) and `langStringTextType`
(used by description):

```xml
<preferredName>
  <langStringPreferredNameTypeIec61360>
    <language>en</language>
    <text>Manufacturer name</text>
  </langStringPreferredNameTypeIec61360>
  <langStringPreferredNameTypeIec61360>
    <language>de</language>
    <text>Herstellername</text>
  </langStringPreferredNameTypeIec61360>
</preferredName>

<shortName>
  <langStringShortNameTypeIec61360>
    <language>en</language>
    <text>Manuf.</text>
  </langStringShortNameTypeIec61360>
</shortName>

<definition>
  <langStringDefinitionTypeIec61360>
    <language>en</language>
    <text>The legal entity manufacturing the product.</text>
  </langStringDefinitionTypeIec61360>
</definition>
```

**Critical**: don't reuse the regular `langStringNameType` wrapper inside
DataSpecificationIEC61360. The 3.1 XSD rejects it: `preferredName` admits only
`langStringPreferredNameTypeIec61360` children (schemas/3.1/AAS.xsd:215-218), and
likewise for the shortName / definition wrappers.

Length constraints (aas-core-meta v3_1.py:5398-5440; each text min 1 char):
- `preferredName` text: max **255 chars** per language; advised to keep it to **35**
- `shortName` text: max **18 chars** per language (intentionally short)
- `definition` text: max **1023 chars** per language (NOT unbounded)

---

## 4. ConceptDescription categories + IEC61360 coupling

The `ConceptDescription.category` (an attribute of `Referable`, inherited)
declares what kind of semantic entity the CD describes. The AAS-3.x
allowed values are:

`VALUE`, `PROPERTY`, `REFERENCE`, `DOCUMENT`, `CAPABILITY`,
`RELATIONSHIP`, `COLLECTION`, `FUNCTION`, `EVENT`, `ENTITY`,
`APPLICATION_CLASS`, `QUALIFIER`, `VIEW` (deprecated).

The element → CD-category coupling below is a **recommendation, not a 3.x
constraint**. IDTA-01001 v3.0 Annex H, Table 30 (PDF pp.189-192) marks the
former AASd-052a…069 "Removed | removed, still recommended; would be renamed to
AASc if still needed", AASd-064 removed with Views and AASd-075 removed; only
AASd-070…074 survive, renamed to AASc-004…008 (today's AASc-3a-004…008, the
dataType-per-category rules in §2). Never report a mismatch as a violation.

| Submodel element | Recommended CD category (if semanticId references a CD) |
|---|---|
| Property | VALUE or PROPERTY (former AASd-052a; RC01's AASd-062 said APPLICATION_CLASS) |
| MultiLanguageProperty | PROPERTY (former AASd-052b) |
| Range | PROPERTY |
| ReferenceElement | REFERENCE |
| RelationshipElement / AnnotatedRelationshipElement | RELATIONSHIP |
| Entity | ENTITY |
| File / Blob | DOCUMENT |
| Capability | CAPABILITY |
| Operation | FUNCTION |
| Event | EVENT |
| SubmodelElementCollection | COLLECTION or ENTITY |
| Qualifier | QUALIFIER |

When the CD is used to encode a SPECIFIC value (rare; typical for
fixed-enum dictionaries), `category=VALUE` and the IEC61360 block has
`value` set.

---

## 5. valueList + ValueReferencePair (coded value lists)

For Property elements with a fixed enumeration (e.g., "color" with
allowed: Red, Green, Blue), the CD encodes the enum via `valueList`:

```xml
<dataSpecificationIec61360>
  <preferredName>...</preferredName>
  <dataType>STRING</dataType>
  <valueList>
    <valueReferencePairs>
      <valueReferencePair>
        <value>RED</value>
        <valueId>
          <type>ExternalReference</type>
          <keys><key><type>GlobalReference</type><value>urn:vendor:color:red</value></key></keys>
        </valueId>
      </valueReferencePair>
      <valueReferencePair>
        <value>GREEN</value>
        <valueId>
          <type>ExternalReference</type>
          <keys><key><type>GlobalReference</type><value>urn:vendor:color:green</value></key></keys>
        </valueId>
      </valueReferencePair>
      <!-- ... -->
    </valueReferencePairs>
  </valueList>
</dataSpecificationIec61360>
```

Each `ValueReferencePair` has:
- `value`: the canonical value string (the wire representation)
- `valueId`: an external Reference to the coded-dictionary entry (the
  semantic anchor)

**AASd-006 / AASd-007 / AASd-012** (from `aas-validation` §3.4): when
both `value` and `valueId` are present on a Property / Qualifier /
MultiLanguageProperty, the value MUST be identical to (i.e. the meaning
matches) the referenced coded value. Use this to enforce enum
discipline.

---

## 6. levelType (for measurements with min/max/nom/typ)

When a CD describes a Range or a measurement with multiple "levels"
(e.g., temperature with Min, Nom, Max), `levelType` declares which
levels the CD provides:

```xml
<levelType>
  <min>true</min>
  <nom>false</nom>
  <typ>false</typ>
  <max>true</max>
</levelType>
```

In 3.1 the four flags are an XSD **sequence in the order min, nom, typ, max**, each `xs:boolean`
and each mandatory once `levelType` is present (`AAS_3_1.xsd`, group `levelType`). Corrected
2026-10-02: this example used to list min, max, nom, typ, which the XSD rejects.

For Range elements, Part 3a v3.0 Table 1 ("IEC61360 Data Specification Template for Properties and
Ranges", p.34) lists `levelType` "Min = true, Max = true" in the Range column. This is template
guidance, not a numbered constraint: the former **AASd-069** ("If the semanticId of a Range references a
ConceptDescription then DataSpecificationIEC61360/levelType shall be identical to the set {Min, Max}.")
is marked "Removed | removed, still recommended; would be renamed to AASc if still needed" in
IDTA-01001-3-0 Annex H, Changes V3.0RC02 vs. V3.0RC01, p.190, and no AASc-3a constraint replaces it
(Part 3a v3.0 constraint list; aas-core-meta v3.0, v3.1 and v3.2 declare neither AASd-069 nor a
successor). Never cite AASd-069 against a 3.x file; report a deviation as a recommendation. For other
elements, `levelType` is informational.

### The flags arrive as TEXT from a parser: read them as xs:boolean (L-1, 2026-10-01)

XML-to-object parsers commonly hand every imported levelType flag over as a string (`"false"`,
`"true"`), and so does an xml2js read of the package's own XML (bare string, one-item array, or
`{_: text, $: attributes}` when the element carries an attribute). A serializer that coerces with
`!!x` turns `"false"` into `true`: the `.aas.json` part then ships min/nom/typ/max ALL true on
every import with a levelType, while the `.aas.xml` part keeps the document's flags.

Rule: read each flag the way xs:boolean does, true only for `true`, `1`, `"true"` or `"1"` (after
trimming), everything else false, and use ONE reader for both serializations. No IDTA template in the 103-template catalogue examined
carries a levelType, so only vendor packages reach this path: test it with one.

---

## 7. IRDI semanticId pattern

IRDI = International Registration Data Identifier. Pattern:
`<RAI>#<CI>#<ID>` where:
- RAI = Registration Authority Identifier (e.g., `0173-1` for ECLASS)
- CI = Class Identifier (e.g., `02` for Basic catalogue)
- ID = `AAxxx#nnn` (the class + version)

Examples from ECLASS:
- `0173-1#02-AAO677#002` — Manufacturer name (Basic, version 002)
- `0173-1#02-AAW338#001` — Manufacturer product designation
- `0173-1#02-AAY811#001` — URI of the product

In an AAS reference:
```xml
<semanticId>
  <type>ExternalReference</type>
  <keys>
    <key><type>GlobalReference</type><value>0173-1#02-AAO677#002</value></key>
  </keys>
</semanticId>
```

The `<value>` is the literal IRDI; resolution to a CD happens via the
ConceptDescriptionRepository.

---

### 7.1 isCaseOf and supplementalSemanticId (multi-dictionary anchoring)

A ConceptDescription (and any HasSemantics element) can carry MORE than one
semantic anchor — this is how DPP / battery content keeps an ECLASS IRDI, an
IEC-CDD id and a SAMM aspect URN all pointing at the same concept:

- **`semanticId`** — the PRIMARY anchor (one Reference). For 3.0 Nameplate the
  primary is IEC-CDD (`0112/2///61987#…`); for battery leaves it is the ECLASS
  IRDI (`0173-1#02-ABL…#nnn`).
- **`supplementalSemanticId`** (0..n, on any HasSemantics element) — additional
  anchors for the SAME element, e.g. the **SAMM aspect-model URN**
  (`urn:samm:io.admin-shell.idta.batterypass.<aspect>:1.0.x#<Prop>`) riding
  alongside the ECLASS primary. **AASd-118:** a `supplementalSemanticId` requires
  a primary `semanticId` to be present.
- **`ConceptDescription.isCaseOf`** (0..n) — a Reference from the CD to a
  BROADER / source concept it is a "case of" (the IDTA-02099-1 DppMetadata
  fields use `isCaseOf` external refs to their EN 18223 source concepts). It
  links CDs across dictionaries without changing the element's own `semanticId`.

**Mapping a SAMM model to AAS:** a SAMM `samm-c:Enumeration` (e.g. battery
`status`, `batteryCategory`, `hazardousSubstanceClass`) becomes a Property with
`valueType=xs:string` and a CD whose IEC61360 `valueList` carries each literal as
a `ValueReferencePair`. The SAMM `samm:dataType` (xsd:*) maps directly to the
Property `valueType` (xsd:float→`xs:float`, xsd:dateTime→`xs:dateTime`,
xsd:unsignedInt→`xs:unsignedInt`, xsd:double→`xs:double`). ⚠ **Not every SAMM
Characteristic is an enum** — battery `ExtinguishingAgent` and IDTA
`PcfCalculationMethod` are free-text `xs:string`, so do NOT emit a closed
`valueList` for them (see [[aas-validation]] §10.2).

---

## 8. ECLASS catalogue tiers

ECLASS (the dominant IEC61360-aligned catalogue) ships in three tiers:

| Tier | Free? | Use case | Catalogue size |
|---|---|---|---|
| ECLASS Basic | Yes, public | Industrial automation (most-used in DPP and Battery Passport) | ~3000 properties |
| ECLASS Standard | Paid licence | Wider industrial coverage | ~50000 properties |
| ECLASS Advanced | Paid licence | Full domain coverage | ~200000 properties |

For most DPP use cases, **Basic is sufficient**. The Basic
IRDIs cover Nameplate elements (manufacturer, product code, country of
origin) and the common Battery Passport mandatory fields.

When an IRDI doesn't exist in Basic but is needed: either
1. Upgrade to Standard / Advanced if the catalogue has it.
2. Use IEC CDD (Common Data Dictionary) as alternative source.
3. Define a custom URN under your organisation's namespace and document
   the mapping.

DO NOT invent IRDIs in the ECLASS namespace (`0173-1#02-`). They look
real but resolve to nothing, corrupting downstream tooling.

---

## 9. Interoperability with IEC CDD

IEC Common Data Dictionary (`http://cdd.iec.ch`) is the IEC-maintained
counterpart to ECLASS, with stronger coverage in:
- Electric components (per IEC 61987)
- Wind energy systems
- Smart manufacturing

IRDI form is similar: `<RAI>#<CI>#<ID>` but RAI for IEC CDD is
`0112` family (e.g., `0112/2///62683`).

The AAS metamodel treats both equivalently — both are valid `keys[].value`
on a `GlobalReference`-typed Key.

---

## 10. Pitfalls and non-obvious rules

- **Don't reuse the wrong langString wrapper.** Inside
  `DataSpecificationIEC61360`, use `langStringPreferredNameTypeIec61360`,
  `langStringShortNameTypeIec61360`, `langStringDefinitionTypeIec61360`.
  Reusing `langStringNameType` (the Referable.displayName wrapper) is a
  common copy-paste bug.
- **shortName is capped at 18 characters per language.** This is
  intentional — IEC61360 reserves it for UI-tight forms. Don't try to
  cram a description in there.
- **`dataType` (IEC61360 enum) ≠ `valueType` (xs:* enum).** The CD's
  dataType is the semantic category; the Property's valueType is the XML
  type. They must be compatible but they're not interchangeable.
- **`value` on a CD only makes sense for category=VALUE or =DOCUMENT.**
  For PROPERTY / APPLICATION_CLASS the value lives on the Property, not
  on the CD.
- **`valueList` shape (`valueReferencePairs/valueReferencePair`) is
  nested.** Common malformation: a flat list of `valueReferencePair`
  without the wrapper. AASd-validators reject this.
- **An IRDI in a `<value>` of a Key is NOT a URI.** Don't add `urn:` or
  any scheme — the IRDI form IS the identifier. Schemes appear only for
  URN-based identifiers (e.g., `urn:vendor:custom-property`).
- **Don't invent ECLASS IRDIs.** The 0173-1#02 namespace is owned by
  ECLASS Standard authority; inventing IRDIs there corrupts catalogues.
  Use your own URN namespace if no real IRDI exists.
- **A MultiLanguageProperty's CD should use `dataType=STRING_TRANSLATABLE`,
  a Range's CD an `INTEGER_*` or `REAL_*` dataType. This is a recommendation,
  not a numbered constraint in any 3.x revision.** The old rules are gone:
  IDTA-01001-3-0 Annex H (Changes V3.0RC02 vs. V3.0RC01, p.190) marks both
  "Removed | removed, still recommended; would be renamed to AASc if still
  needed", quoting the former text: "Constraint AASd-067: If the semanticId of
  a MultiLanguageProperty references a ConceptDescription then
  DataSpecificationIEC61360/dataType shall be STRING_TRANSLATABLE." and
  "Constraint AASd-068: If the semanticId of a Range submodel element
  references a ConceptDescription then DataSpecificationIEC61360/dataType
  shall be a numerical one, i.e. REAL_* or RATIONAL_*." No AASc constraint
  took their place: Part 3a v3.0 (IDTA-01003-a-3-0) numbers only AASc-3a-002
  to -010 and -050, and aas-core-meta v3.0, v3.1 and v3.2 declare neither
  AASd-067/068 nor a successor. What remains is Part 3a v3.0 Table 1
  ("IEC61360 Data Specification Template for Properties and Ranges", p.34):
  the MultiLanguageProperty column lists `STRING_TRANSLATABLE`, the Range
  column `INTEGER_* or REAL_*`, and Annex E (Changes V3.0 vs. Part 1 V2.0.1,
  p.61) records "CHANGE: no IEC 61360 data type RATIONAL_* allowed any longer
  for RANGE; instead, INTEGER_* is used". So: never cite AASd-067/068 as a
  violation of a 3.x file; a mismatch is a data-quality recommendation citing
  Table 1, and `RATIONAL_*` on a Range CD contradicts the 3.0 table (the old
  AASd-068 allowed it). Common mistake: `STRING` for an MLP (`STRING` is for
  single-language strings). Corrected 2026-10-27; this note used to present
  AASd-067/068 as live rules and to recommend RATIONAL_* for Ranges.
- **AASc-3a-010 is "value and valueList are mutually exclusive", NOT language
  uniqueness** (corrected 2026-09-14). IDTA-01003-a v3.0 p.22: "If
  DataSpecificationIec61360/value is not empty, DataSpecificationIec61360/valueList
  shall be empty, and vice versa" (both empty is legal). `aas-test-engines` 1.0.3
  enforces exactly that. This skill used to say AASc-3a-010 limits each language
  to one entry in preferredName/shortName/definition; no numbered constraint says
  that, in Part 3a or anywhere else. A repeated language is a data-quality problem
  (a reader picks one entry arbitrarily, and in practice the second entry is a
  translation left with the first one's tag). aas-core-meta v3.1 flags it through
  an unnumbered, implementation-specific verification invariant that applies to
  every langString set, `description` and `displayName` included. Report it as a
  non-blocking warning, never as INVALID. Do NOT attribute it to AASd-012 either
  (AASd-012 is MLP value/valueId semantic equivalence). See "langString
  per-language uniqueness — the DEFINITIVE rule" in [[aas-validation]].
- **AASc-3a-008 has an exception written into the rule:** a ConceptDescription
  that describes a value (its `value` is set) needs no `definition`
  (IDTA-01003-a p.39). A checker that ignores it reports every value CD.
- **AASc-3a-009: a measure or currency dataType needs a unit.** If `dataType` is
  INTEGER_MEASURE, REAL_MEASURE, RATIONAL_MEASURE, INTEGER_CURRENCY or
  REAL_CURRENCY, `unit` or `unitId` shall be defined (aas-core-meta
  v3_1.py:5385-5392, 5502-5508). A REAL_MEASURE CD with neither is invalid.
- **`sourceOfDefinition` is plain text, not a Reference.** Common
  malformation: putting a `<keys>...</keys>` block in there. Use the
  reference shape only when the spec field is typed as Reference.

---

## 11. Authoritative references

- **IDTA-01003-a Part 3a v3.1.1** (the IEC61360 data spec):
  [industrialdigitaltwin.io/aas-specifications/IDTA-01003-a/v3.1.1/](https://industrialdigitaltwin.io/aas-specifications/IDTA-01003-a/v3.1.1/)
- **IEC 61360-1 / ISO 13584-42** (the underlying ISO/IEC standards) —
  paid access via IEC and ISO. The IDTA spec adapts these for AAS use.
- **ECLASS catalogue** (public Basic, paid Standard/Advanced):
  [eclass.eu](https://www.eclass.eu) — Basic JSON dumps are downloadable
  from the public site.
- **IEC CDD**:
  [cdd.iec.ch](http://cdd.iec.ch) — public lookup tool for IEC IRDIs.

---

## Behavioural notes for Claude using this skill

- When the user asks "what semanticId for X", **first check the curated
  ECLASS Basic catalogue**.
  Only invent a URN if no IRDI exists.
- When building a ConceptDescription, **always include both
  `preferredName` AND `definition`** in at least English. Tools degrade
  gracefully with only preferredName but auditors expect definition.
- For Range elements, **set an `INTEGER_*` or `REAL_*` dataType** in the CD
  (Part 3a v3.0 Table 1; AASd-068 was removed and its RATIONAL_* option dropped).
- For MultiLanguageProperty, **set `dataType=STRING_TRANSLATABLE`** in the CD
  (Part 3a v3.0 Table 1; recommendation, AASd-067 was removed). The most-skipped detail.
- When a Property has a coded enum, **define `valueList` in the CD** and
  reference each coded value via `valueId` on the Property.
- For the langString wrappers, **use the IEC61360-specific types**
  inside DataSpecificationIEC61360. Mixing wrapper types is the most
  common XSD-validation failure in IEC61360 content.
- For IRDI references, **cite the catalogue source** (ECLASS Basic /
  Standard / Advanced / IEC CDD) so the user can audit.
- Don't invent ECLASS IRDIs even when convenient. Use a vendor URN
  (`urn:vendor:property:foo`) when no real IRDI exists; the audit trail
  stays clean.
