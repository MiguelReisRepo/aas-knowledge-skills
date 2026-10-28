---
name: aas-capability-description
description: Asset Administration Shell capability modelling expertise — the IDTA-02020 "Capability Description" submodel template. Covers the CapabilitySet → CapabilityContainer tree, the Capability element (modelType Capability) with its CapabilityRoleQualifier (Required/Offered/NotAssigned, exactly one true), PropertySet/PropertyContainer with the CapabilityPropertyType enum (Property|Range|MultiLanguageProperty|SubmodelElementList), CapabilityRelations (CapabilityRealizedBy → the capability-to-Skill realization link, ConstraintSet with Property/TransitionConstraintContainer, ComposedOfSet → CapabilityComposedOf, GeneralizedBySet → CapabilityGeneralizedBy), ALL THREE Table-3 constraints (SM-CapabilityDescription-1/-2/-3), and the semanticId table. Use this skill whenever the user models what an asset CAN DO (drilling, tightening, transporting…), matches required vs offered capabilities (production feasibility checks), builds or reviews a CapabilityDescription submodel, mentions IDTA-02020, CapabilitySet, CapabilityContainer, capability matchmaking, skills/realization. ALWAYS read the bundled official IDTA-02020 PDF first (see the mandatory step below) — this skill is a map, the PDF is the law. NOTE: capabilities = IDTA-02020; IDTA-02007 is Software Nameplate, an unrelated template.
---

# AAS Capability Description (IDTA-02020)

The canonical reference for modelling an asset's **capabilities** — implementation-
independent specifications of functions ("drilling", "tightening", "transporting")
that a production resource OFFERS or a product/process REQUIRES. The template
behind capability matchmaking: "which of my machines can drill an 8mm hole in
aluminium?" is a query over CapabilityDescription submodels.

Companion to [[aas-submodel-templates]] (the template map), [[aas-knowledge]]
(the metamodel — `Capability` is a first-class SubmodelElement type), and
[[aas-validation]] (AASd-* constraints).

## ⚠ MANDATORY FIRST STEP — read the official spec, every time

**Before authoring, editing, reviewing, or validating ANY Capability Description
submodel, you MUST read the bundled official specification.** Memory drifts; the
PDF does not — this very skill was written after the PDF exposed real semanticId
drift in code whose own comments claimed to be canonical.

```
Read: ~/.claude/skills/aas-capability-description/IDTA-02020_Submodel_Capability_Description.txt   ← always readable
      ~/.claude/skills/aas-capability-description/IDTA-02020_Submodel_Capability_Description.pdf   ← authoritative
```
(In the aas-skills repo: `skills/aas-capability-description/…`.)

44 pages — read §2 (Submodel structure tables, pp. 17–30) in full and skim the
examples in Addendum B. If a claim here and the spec disagree, **the spec wins**
— then fix this skill.

## Structure (verified against the PDF tables, §2.2)

```
Submodel  idShort=CapabilityDescription        (idShort free)
          semanticId → https://admin-shell.io/idta/SubmodelTemplate/CapabilityDescription/1/0
└─ [SMC] CapabilitySet  [1..*]                 .../CapabilityDescription/CapabilitySet/1/0
   └─ [SMC] CapabilityContainer  [1..*]        .../CapabilityDescription/CapabilityContainer/1/0
        ├─ [Cap] Capability  [1]               .../CapabilityDescription/Capability/1/0
        │     supplementalSemanticId → the EXTERNAL capability definition
        │     (e.g. an ontology IRI for "drilling") — this is the matchmaking key
        │     └─ CapabilityRoleQualifier (Qualifier, kind=ValueQualifier):
        │        Required | Offered | NotAssigned  (xs:boolean, EXACTLY ONE true;
        │        default NotAssigned)             .../CapabilityRoleQualifier/<Role>/1/0
        ├─ [MLP] CapabilityComment  [0..1]     .../CapabilityDescription/CapabilityComment/1/0
        ├─ [SMC] PropertySet  [0..*]           .../CapabilityDescription/PropertySet/1/0
        │   └─ [SMC] PropertyContainer [1..*]  .../CapabilityDescription/PropertyContainer/1/0
        │        ├─ CapabilityPropertyType — EXACTLY ONE of
        │        │    Property | Range | MultiLanguageProperty | SubmodelElementList
        │        │    semanticId .../CapabilityPropertyType/<Type>/1/0
        │        ├─ [Rel] SameProperty [0..*]  .../CapabilityDescription/SameProperty/1/0
        │        │    (this property ↔ the identical property in another Submodel)
        │        └─ [MLP] PropertyComment      .../CapabilityDescription/PropertyComment/1/0
        └─ [SMC] CapabilityRelations  [0..1]   .../CapabilityDescription/CapabilityRelations/1/0
             ├─ [Rel] CapabilityRealizedBy [0..*]  .../CapabilityDescription/CapabilityRealizedBy/1/0
             │    first = the Capability element; second = a SKILL implementation
             │    (e.g. an Operation / program outside this template) — the
             │    capability→skill realization link
             ├─ [SMC] ConstraintSet             .../CapabilityDescription/ConstraintSet/1/0
             │    holds PropertyConstraintContainer AND/OR
             │    TransitionConstraintContainer, side by side (§2.2.2.3).
             │    (PropertyConstraintType / PropertyConditionalType /
             │     TransitionConditionalType / ConstraintPropertyRelations /
             │     ConstraintHasProperty / TransitionConstrainedBy — PDF §2.2.2)
             ├─ [SMC] ComposedOfSet   → [SMC] ComposedOfContainer
             │                            → [Rel] CapabilityComposedOf   (decomposition)
             └─ [SMC] GeneralizedBySet → [Rel] CapabilityGeneralizedBy   (taxonomy)
```

Key semantics (verify in the PDF):
- **idShorts are free** on nearly every element ("IdShort can be chosen freely") —
  conformance lives in the **semanticIds**, not the names. A container named
  `CapabilityName` with the `CapabilityContainer/1/0` semanticId is conformant;
  one with NO semanticId is not addressable as 02020.
- **Role**: exactly ONE of Required/Offered/NotAssigned true per Capability.
  Offered = a resource provides it; Required = a product/process needs it —
  matchmaking joins Required against Offered via the Capability's
  supplementalSemanticId (the shared external definition).
- **Table 3 (§1.7) lists THREE constraints, not one.** All three are template
  rules that no AASd-* checker, XSD or JSON schema will ever catch. The official
  AASX does not enforce them either: "The restricitons are not explicitly modelled
  in the Submodel template contained in the AASX package [...] Nevertheless, the
  restrictions apply" (IDTA-02020 v1.0 §1.7 p.15) — check them in your own code:
  - **SM-CapabilityDescription-1** (extends AASd-109): a property list whose
    `typeValueListElement` ∈ {Property, Range, MultiLanguageProperty,
    SubmodelElementList} MUST set `valueTypeListElement`, and every first-level
    child must match it.
  - **SM-CapabilityDescription-2**: a `ConstraintSet` MUST contain at least one
    `PropertyConstraintContainer` or `TransitionConstraintContainer`. An empty
    ConstraintSet is a violation — and a very easy one to ship, because "create
    the container, fill it later" is the natural authoring order.
  - **SM-CapabilityDescription-3**: the `PropertyConstraintType` instance must
    match the selected `ConstraintType` (§2).
    ⚠️ **Spec-vs-template dispute (recorded 2026-09-14).** The PDF's
    PropertyConstraintContainer table (p.33) lists PropertyConstraintType,
    PropertyConditionalType and ConstraintPropertyRelations, and NO
    `ConstraintType`, although SM-3 refers to it. The official template JSON
    DOES declare it: a Property `ConstraintType`, semanticId
    `https://admin-shell.io/idta/CapabilityDescription/ConstraintType/1/0`,
    `SMT/Cardinality One`, `FormChoices`
    `OperationConstraint;OCLConstraint;BasicConstraint;CustomConstraint`, placed
    after the four instances. Emit it (template followed) with the value naming
    the instantiated member, and check SM-3 against it. A real supplier
    package carries one too, with a SPACE inside its IRI
    (`…/CapabilityDescription/ ConstraintType/1/0`): read it, never emit that form.
  - **ConstraintHasProperty.first targets the constraint ELEMENT, not its
    container.** p.32: "Relates the PropertyConstraint as first element to a
    Property from a PropertyContainer as second element". The template's own
    reference has 7 keys ending at `Property:BasicConstraint`, and every
    real supplier package version does the same. Ending it at the
    PropertyConstraintContainer (6 keys) also
    resolves, so a
    "references resolve" check cannot tell them apart: compare the last key's
    TYPE with the instance's modelType.
- The **skill** (executable implementation) is OUTSIDE this template —
  `CapabilityRealizedBy` points at it (second attribute). Capability =
  what; Skill = how.

## Conformance gotchas

- **The submodel semanticId is `…/idta/SubmodelTemplate/CapabilityDescription/1/0`**
  — note the `SubmodelTemplate/` segment and the trailing `/1/0`.
  ⚠️ **The spec itself is the trap here.** §1.6.8 explains what an IRI looks like
  using `https://admin-shell.io/idta/CapabilityDescription/1/0/Submodel` as its
  worked example — prose about IRI anatomy, in a section about naming, nowhere
  near the attribute tables. It reads exactly like a declaration, and at least
  one production implementation shipped precisely that value before
  a spec re-read caught it. The normative value lives in the §2.2 Submodel
  attribute table. Recognise the §1.6.8 form on READ so those documents open and
  can be repaired; never EMIT it.
- Every structural SMC needs its 02020 semanticId — a semanticId-less container
  breaks matchmaking even though it renders fine in a viewer.
- `Capability` is its own **modelType** (`[Cap]`) — not a Property. The XML tag
  is `<capability>`; it has NO value payload (its meaning lives in the
  qualifiers + siblings).
- **The CapabilityPropertyType enum IRIs sit OUTSIDE `/CapabilityDescription/`.**
  The abstract type is `…/idta/CapabilityDescription/CapabilityPropertyType/1/0`,
  but its four values are `…/idta/CapabilityPropertyType/{Property,Range,
  MultiLanguageProperty,SubmodelElementList}/1/0` — no `CapabilityDescription`
  segment. Deliberate in the spec (§2.2.1), and easy to "correct" into a wrong
  value when transcribing by pattern rather than by reading.
- **`PropertyRealizedBy` is named but not modelled.** §1.8.2 lists it among the
  in-between-Submodel relationships alongside `CapabilityRealizedBy` and
  `SameProperty`, but — unlike those two — it has NO attribute table anywhere in
  the document and no semanticId. Do not invent one.
- Exactly-one-role: emitting all three qualifiers with two `true` (or none)
  violates the template even though AASd-* checkers won't flag it.
- The external capability definition goes in **supplementalSemanticId** of the
  Capability element; the element's own semanticId stays
  `.../CapabilityDescription/Capability/1/0`.

## Legacy capability shapes and the rebuild recipe (measured 2026-10-28)

A real capability submodel authored in 2025 by a supplier raised 43 template warnings in a current editor, all from five
legacy shapes. None is an AASd violation; each one makes the submodel unreadable to a
02020 consumer.

| legacy shape | why a 02020 reader rejects it | conformant form |
|---|---|---|
| submodel semanticId `https://admin-shell.io/idta/CapabilityDescription/1/0/Submodel` | it is the §1.6.8 naming example, not the §2.2 declaration (see "Conformance gotchas") | `https://admin-shell.io/idta/SubmodelTemplate/CapabilityDescription/1/0` |
| typed element semanticId `…/CapabilityPropertyEnumType/…` | IDTA-02020 defines no `CapabilityPropertyEnumType`; the enum is `CapabilityPropertyType` (p.22-23) | `https://admin-shell.io/idta/CapabilityPropertyType/{Property,Range,MultiLanguageProperty,SubmodelElementList}/1/0` |
| one PropertyContainer holding several properties (e.g. a `BuildVolumeContainer` with Height, Length, Width) | the PropertyContainer instantiates exactly ONE CapabilityPropertyType (p.22-23: "Exactly one of the SubmodelElements below must be instanciated") | one container per value (`BuildVolumeHeightContainer`, …), same idShorts and values |
| `CapabilityRelations/ConstraintSet` present but empty | SM-CapabilityDescription-2: a ConstraintSet holds at least one Property- or TransitionConstraintContainer | omit it (CapabilityRelations is 0..1) until there is a constraint |
| the unit put in the property's semanticId, as a ModelReference to a ConceptDescription that is not in the package (`…/ids/cd/meter`) | the ModelReference itself is VALID (see [[aas-validation]], settled non-violations), but it takes the semanticId slot, so the element no longer carries a CapabilityPropertyType IRI and its container counts 0 typed elements (that is where most of the 25 cardinality warnings came from, single-property containers included) | semanticId = the CapabilityPropertyType IRI; the unit as an embedded IEC 61360 block (below) |

**Rebuild recipe** (applied to 6 capabilities, 31 typed elements; every container,
idShort, element type, valueType, value, min and max came out unchanged):
1. Set the submodel semanticId to the §2.2 value.
2. One PropertyContainer per value; give each typed element its CapabilityPropertyType
   IRI. ENUM lists: `typeValueListElement=Property` plus `valueTypeListElement`
   (SM-CapabilityDescription-1 / AASd-109).
3. Drop an empty ConstraintSet instead of shipping it.
4. Units: do not recreate the dangling CD references. Put an embedded
   `DataSpecificationIec61360` on the typed element, as p.23 provides for
   CapabilityPropertyType (*"hasDataSpecification: Reference to external data
   definitions, e.g., unit of the property."*, page 23/44), with `preferredName` (en),
   `unit` (e.g. `m`, `mm`, `m/min`, `kg/h`, `kg`) and `dataType` `REAL_MEASURE`. That
   satisfies AASc-3a-002 and AASc-3a-009; AASc-3a-008 (definition) binds
   ConceptDescriptions only. See [[iec61360]] for the template IRI question.
5. Leave `supplementalSemanticId` alone and mint no new CD ids. Re-read after save and
   compare every value field with the source.

## Implementation notes (lessons from production editors)

- Match a 02020 submodel on semanticId ONLY, never idShort, and read both the
  JSON `keys:[…]` and an xml2js `keys:{key:…}` shape.
- Do NOT feed 02020 to a mandatory-set engine that pairs a mandatory child with
  its parent BY idShort: this template says idShorts are free, so a conformant
  `CapabilitySet` named `MachiningCapabilities` would simply not be found, and the
  engine would report a clean bill of health on a document it never inspected.
- The role Qualifier is a `ValueQualifier`: an export step that strips
  TemplateQualifiers from instances must filter on `kind`, not drop every
  qualifier. `supplementalSemanticId` (the matchmaking key) must reach both the
  XML and the JSON part, and `<capability>` carries no value payload.
- This template is made of relationships: build every ModelReference from the
  submodel's effective id, which a template-created submodel may only receive at
  serialization time.
- An empty PropertySet or CapabilitySet should be emitted as authored and
  reported, never silently dropped.

## Sign-off checklist (only after reading the PDF)

1. Read the bundled IDTA-02020 PDF — done?
2. Submodel semanticId = `…/idta/SubmodelTemplate/CapabilityDescription/1/0`.
3. Tree = CapabilitySet[1..*] → CapabilityContainer[1..*] → Capability[1] —
   every container with its 02020 semanticId (idShorts free).
4. Capability: modelType `Capability`, external definition in
   supplementalSemanticId, exactly ONE role qualifier true.
5. PropertyContainer: exactly one CapabilityPropertyType element; lists satisfy
   SM-CapabilityDescription-1 (valueTypeListElement set + children match); any
   ConstraintSet satisfies SM-CapabilityDescription-2 (at least one Property- or
   TransitionConstraintContainer) and SM-CapabilityDescription-3.
6. Realization: CapabilityRealizedBy first=Capability, second=the skill.
7. Run [[aas-validation]] (AASd-* + XSD) AND check the 02020 semanticIds —
   generic validators pass a submodel that 02020 consumers cannot read.

### `SubmodelElement` is not `SubmodelElementList` (matters for SM-CapabilityDescription-1)

SM-CapabilityDescription-1 widens AASd-109 to `typeValueListElement` ∈ {Property, Range,
MultiLanguageProperty, SubmodelElementList}. Real supplier packages declare
**`SubmodelElement`**, the abstract base, on some lists (13 of 29 in one package): that value is in
NEITHER set, so neither AASd-109 nor SM-1 applies to them, and `aas-core3.1` 1.0.0 confirms the shape
verifies with 0 errors. A checker that raises a blocking AASd-109 error on them is wrong. When a checker
fires on a list, read the DECLARED value literally before deciding which rule, if any, it breaks.
