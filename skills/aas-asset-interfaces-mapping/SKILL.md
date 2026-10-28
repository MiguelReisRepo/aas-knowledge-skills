---
name: aas-asset-interfaces-mapping
description: Asset Administration Shell Asset Interfaces Mapping Configuration expertise — the IDTA-02027 "Asset Interfaces Mapping Configuration" (AIMC) submodel template, v2.0 (May 2026). AIMC is the CONFIGURATION layer that wires data points to target locations: it pairs a set of Sources (inputs) with a set of Sinks (outputs), optionally via a Lua Transformation, and is operationalized at runtime by a Data Mapping Processor (DMP). Two use cases — Asset-to-AAS mapping (Sources reference the InteractionMetadata data points of an Asset Interfaces Description / AID, IDTA-02017, submodel) and AAS-to-AAS mapping (no AID). Covers the full v2.0 tree (submodel AssetInterfacesMappingConfiguration → MappingConfigurations SML → MappingConfiguration SMC{DefaultPollingInterval, Transformation Blob, Sources SML, Sinks SML} → Source SMC{Source Ref, PollingInterval, SourceId} / Sink SMC{Sink Ref, SinkId}), every verbatim admin-shell.io semanticId (submodel = .../idta/AssetInterfacesMappingConfiguration/2/0/Submodel), the ModelReference-into-AID targeting, the SourceId==SinkId one-to-one forwarding rule when no Transformation, polling-interval sync/async semantics, and the v1.0→v2.0 removal of InterfaceReference + MappingSourceSinkRelations. Use this skill whenever the user models, reviews, or validates how asset/interface data is MAPPED into AAS submodels — northbound asset→AAS onboarding, AAS→AAS KPI/OEE computation, live-data wiring, DMP configuration — builds/reviews an AIMC submodel, mentions IDTA-02027, AIMC, MappingConfiguration, Sources/Sinks, SourceId/SinkId, the aimc_main Lua transformation, the Data Mapping Processor, or the relationship between AIMC and AID (IDTA-02017). AIMC (02027) is the mapping layer ON TOP OF AID (02017) — cross-reference [[aas-submodel-templates]] and the AID template. NOTE the spec-printed version drift on the MappingConfigurations SML semanticId (uses /1/0/ while everything else uses /2/0/) — frozen verbatim and flagged below. AIMC "2.1" (catalogue folder `2/1`, on main since 2026-09-25) is a BUG-FIX re-issue of the 2.0 JSON/AASX: same PDF byte for byte, same `.../2/0/Submodel` semanticId, administration still 2.0; only the three SML item idShorts (MappingConfiguration/Source/Sink) are removed (AASd-120) and the templateId loses a space — treat it as v2.0 everywhere (see "AIMC 2.1").
metadata:
  type: reference
---

# AAS Asset Interfaces Mapping Configuration (IDTA-02027 AIMC v2.0)

The reference for **configuring how data is mapped into an AAS**: IDTA-02027
*"Asset Interfaces Mapping Configuration"* (AIMC), v2.0 (May 2026). AIMC is not a
data container — it is the **configuration** that defines a directed flow from a
set of **Sources** (input data points) to a set of **Sinks** (output locations),
optionally through a **Lua Transformation**. A runtime component, the **Data
Mapping Processor (DMP)**, reads the AIMC, connects to the referenced interfaces,
executes the transformation, and writes results to the sink locations.

AIMC is the **mapping layer that sits on top of the Asset Interfaces Description
(AID, IDTA-02017)**. AID *documents* which interfaces/data points an asset offers
(authored by the asset provider); AIMC *wires* selected AID data points to AAS
submodel elements in one direction, optionally transforming (authored by the asset
user / system integrator). AID and AIMC are separate submodels and need not be
co-located in the same AAS.

Companion to [[aas-submodel-templates]] (the template map), the **AID / IDTA-02017**
template (the interfaces AIMC references), [[aas-knowledge]] (metamodel,
ModelReference vs ExternalReference), and [[aas-validation]] (AASd-*).

## ⚠ MANDATORY FIRST STEP — read the bundled spec

Read the bundled official spec before authoring/reviewing any AIMC submodel — the
.txt always works, the PDF is authoritative (22 pages; §2.3–2.9 Tables 2–8 are the
element tables; Annex C lists the v1.0→v2.0 changes):

```
Read: ~/.claude/skills/aas-asset-interfaces-mapping/IDTA-02027_Submodel_Asset-Interfaces-Mapping-Configuration.txt   ← always readable
      ~/.claude/skills/aas-asset-interfaces-mapping/IDTA-02027_Submodel_Asset-Interfaces-Mapping-Configuration.pdf   ← authoritative
```

This skill was authored **verbatim** against that .txt. **The bundled spec is v2.0,
whose structure differs from v1.0** — v2.0 *removed* the `InterfaceReference`
ReferenceElement and the `MappingSourceSinkRelations`/`MappingSourceSinkRelation`
SML/SMC, and *added* `DefaultPollingInterval`, the `Transformation` Blob, and the
`Sources`/`Sinks` SMLs (Annex C). If you were briefed on InterfaceReference /
MappingSourceSinkRelation / RelationDirection, that is the **v1.0** shape — do not
model it against v2.0. Follow the tree below.

## Structure tree (verbatim, §2.3–2.9)

Submodel `AssetInterfacesMappingConfiguration` (idShort SHALL be
`AssetInterfacesMappingConfiguration`), semanticId
`https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/Submodel`.
Below, `AIMC` = `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration`.
Legend: `●` = mandatory (lower card ≥ 1). modelTypes: `[SML]` SubmodelElementList,
`[SMC]` SubmodelElementCollection, `[Prop]` Property, `[Blob]` Blob, `[Ref]`
ReferenceElement.

```
Submodel  idShort=AssetInterfacesMappingConfiguration   semanticId → AIMC/2/0/Submodel
  └─ [SML] MappingConfigurations ●            AIMC/1/0/MappingConfigurations   ⚠ printed /1/0/ — see DISCREPANCY 1
        (orderRelevant=No; semanticIdListElement=[GlobalReference, AIMC/2/0/MappingConfiguration];
         typeValueListElement=SubmodelElementCollection)
     └─ [SMC] [00] MappingConfiguration  0..*  AIMC/2/0/MappingConfiguration
          ├─ [Prop] DefaultPollingInterval  0..1   AIMC/2/0/MappingConfiguration/DefaultPollingInterval   [xs:double]
          ├─ [Blob] Transformation          0..1   AIMC/2/0/MappingConfiguration/Transformation           (Lua; contentType text/plain)
          ├─ [SML] Sources ●                1      AIMC/2/0/MappingConfiguration/Sources
          │     (orderRelevant=No; semanticIdListElement=[GlobalReference, AIMC/2/0/MappingConfiguration/Source];
          │      typeValueListElement=SubmodelElementCollection)
          │   └─ [SMC] [00] Source  1..*          AIMC/2/0/MappingConfiguration/Source
          │        ├─ [Ref]  Source ●        1     AIMC/2/0/MappingConfiguration/Source/Source          (ModelReference → SubmodelElement, incl. AID InteractionMetadata)
          │        ├─ [Prop] PollingInterval 0..1  AIMC/2/0/MappingConfiguration/Source/PollingInterval [xs:double]
          │        └─ [Prop] SourceId ●      1     AIMC/2/0/MappingConfiguration/Source/SourceId        [xs:string]
          └─ [SML] Sinks ●                  1      AIMC/2/0/MappingConfiguration/Sinks
                (orderRelevant=No; semanticIdListElement=[GlobalReference, AIMC/2/0/MappingConfiguration/Sink];
                 typeValueListElement=SubmodelElementCollection)
              └─ [SMC] [00] Sink  1..*             AIMC/2/0/MappingConfiguration/Sink
                   ├─ [Ref]  Sink ●          1     AIMC/2/0/MappingConfiguration/Sink/Sink              (ModelReference → SubmodelElement, target location)
                   └─ [Prop] SinkId ●        1     AIMC/2/0/MappingConfiguration/Sink/SinkId            [xs:string]
```

### Cardinalities (verbatim)

| Element | modelType | card. | valueType |
|---|---|---|---|
| MappingConfigurations | SML | 1 (mandatory) | — |
| MappingConfiguration | SMC | 0..* | — |
| DefaultPollingInterval | Prop | 0..1 | xs:double |
| Transformation | Blob | 0..1 | — (0 bytes example) |
| Sources | SML | 1 (mandatory) | — |
| Source | SMC | 1..* | — |
| Source (Source→Source) | Ref | 1 (mandatory) | — |
| PollingInterval | Prop | 0..1 | xs:double |
| SourceId | Prop | 1 (mandatory) | xs:string |
| Sinks | SML | 1 (mandatory) | — |
| Sink | SMC | 1..* | — |
| Sink (Sink→Sink) | Ref | 1 (mandatory) | — |
| SinkId | Prop | 1 (mandatory) | xs:string |

## Verbatim semanticIds (14 distinct — the frozen source)

Freeze these EXACTLY. `AIMC` = `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration`.

| # | idShort | modelType | semanticId (verbatim) |
|---|---|---|---|
| 1 | AssetInterfacesMappingConfiguration | Submodel | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/Submodel` |
| 2 | MappingConfigurations | SML | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/1/0/MappingConfigurations` ⚠ `/1/0/` (DISCREPANCY 1) |
| 3 | MappingConfiguration | SMC | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration` |
| 4 | DefaultPollingInterval | Prop | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/DefaultPollingInterval` |
| 5 | Transformation | Blob | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Transformation` |
| 6 | Sources | SML | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Sources` |
| 7 | Source | SMC | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Source` |
| 8 | Source (→Source Ref) | Ref | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Source/Source` |
| 9 | PollingInterval | Prop | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Source/PollingInterval` |
| 10 | SourceId | Prop | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Source/SourceId` |
| 11 | Sinks | SML | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Sinks` |
| 12 | Sink | SMC | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Sink` |
| 13 | Sink (→Sink Ref) | Ref | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Sink/Sink` |
| 14 | SinkId | Prop | `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/2/0/MappingConfiguration/Sink/SinkId` |

Note the SML `semanticIdListElement` values (used to type the list items) reuse the
child SMC ids: `Sources` list → id #7 (`.../Source`), `Sinks` list → id #12
(`.../Sink`), `MappingConfigurations` list → id #3 (`.../2/0/MappingConfiguration`).
The spec defines **no** IEC61360/IRDI ConceptDescription ids — all semanticIds are
admin-shell.io path IRIs. Every id above is legibly printed in the .txt, so there
are **no `VERIFY-<idShort>` (missing-id) flags** — only the discrepancies below.

## Key concepts

### Two use cases (§1.2)
1. **Asset-to-AAS mapping** — together with the **AID (IDTA-02017)**, AIMC specifies
   how data from an asset (or asset-related service) is mapped to target locations in
   an AAS. AIMC is the configuration submodel for **northbound** asset→AAS
   communication (e.g. into a monitoring/logging/OperationalData submodel).
2. **AAS-to-AAS mapping** — AIMC maps between locations within/across AASs **without
   the AID** (e.g. compute one KPI value from several existing elements). Typical for
   deriving higher-level signals (OEE per ISO 22400-2, "machine is running", …).

In both cases a mapping = a relationship between a set of **sources** (input) and a
set of **sinks** (output), with an optional transformation in between. AIMC + AID
help meet EU Digital Product Passport / EU Data Act obligations by exposing
machine data via the AAS in standardized machine-readable form.

### Data Mapping Processor (DMP) (§1.3)
The **runtime** that operationalizes AIMC: establishes/maintains the data flows,
uses the referenced AIDs to connect to asset interfaces, executes optional
transformations, and writes results to the configured sink locations. Typically run
by the AAS platform/service provider or an adjacent integration service. Its
implementation is out of scope; AIMC only *configures* it. For **synchronous**
protocols (e.g. HTTP/REST) the DMP polls per the polling interval; for
**asynchronous** protocols (e.g. MQTT) inputs arrive as updates. Any input change
re-evaluates the MappingConfiguration and propagates the result(s) to the sinks.

### Transformation (Lua) (§1.4)
- Optional `Transformation` **Blob** on each MappingConfiguration; `contentType` =
  `"text/plain"`; holds a **Lua** script that MUST contain the entrypoint
  `function aimc_main(sources)`.
- The DMP passes all `Sources` inputs into `aimc_main` via the `sources` table,
  keyed by each **SourceId**. The function returns a table assigning an output value
  to each **SinkId**.
- **No Transformation → 1:1 forwarding**: the number of Sources and Sinks **shall be
  equal**, each source maps to exactly one sink, and the pairing is established by
  **matching `SourceId == SinkId`**.
- In v2.0 Lua transformations **shall be stateless** (no persisted global state
  across executions). Annex B gives the rationale for Lua and a sandboxed Python/lupa
  prototype (memory + CPU-time caps, module whitelist).

### Source / Sink references (§2.2, §2.7, §2.9)
- Each `Source` SMC = a `Source` **ReferenceElement** (the data point) + optional
  `PollingInterval` + mandatory `SourceId`.
- Each `Sink` SMC = a `Sink` **ReferenceElement** (the target location) + mandatory
  `SinkId`.
- Both `Source/Source` and `Sink/Sink` are **`ModelReference`** type pointing to the
  actual `SubmodelElement` of interest. A source can be **any SubmodelElement,
  including those in the `InteractionMetadata` of an AID submodel** (fetching live
  asset data). A sink can be any addressable submodel element (e.g. a Property in a
  monitoring submodel). Because they are ModelReferences, sources and sinks **may
  live in external AASs** — they need not be in the same AAS as the AIMC.

### Polling intervals (§2.5, §2.7)
`DefaultPollingInterval` (MappingConfiguration-level) and `PollingInterval`
(Source-level) are seconds (`xs:double`). Must be **> 0 for synchronous protocols
that need polling (e.g. HTTP)**; **ignored for asynchronous protocols (e.g. MQTT)**.
A local `PollingInterval` **overwrites** the `DefaultPollingInterval` for that
source. Per §1.3, for synchronous sources **at least one** polling interval (Default
or local) **must** be defined.

### Relationship to AID (IDTA-02017)
AIMC 2.0 adapts to **AID 1.1** protocols: **Modbus, HTTP, MQTT, OPC UA, BACnet**.
In v2.0 there is **no explicit `InterfaceReference`** — it was removed because the
related AID submodel **can be inferred from each `Source` ReferenceElement's target**
(which points into the AID's InteractionMetadata). New AID versions may trigger new
AIMC versions.

## Gotchas

- **This is v2.0, not v1.0.** v2.0 **removed** `InterfaceReference` (Ref) and the
  `MappingSourceSinkRelations` SML / `MappingSourceSinkRelation` SMC, and **added**
  `DefaultPollingInterval`, the `Transformation` Blob, and the `Sources`/`Sinks`
  SMLs (Annex C). Do NOT model InterfaceReference / MappingSourceSinkRelation /
  RelationDirection against v2.0 — the AID link is now implicit via each Source Ref.
- **Source/Sink refs are `ModelReference`, not `ExternalReference`.** §2.2 is
  explicit: "reference element of the type ModelReference that points to the
  SubmodelElement". The `[GlobalReference, …]` you see in the element tables is the
  **semanticIdListElement** (how the SML types its items) — that is unrelated to the
  Source/Sink reference kind. Do not confuse the two.
- **Direction is fixed: Source = input (read), Sink = output (write).** Data flows
  Source → (optional Transform) → Sink. There is no RelationDirection element in
  v2.0; the direction is structural (Sources vs Sinks lists).
- **`SourceId`/`SinkId` are locally unique only.** Unique **within the parent
  MappingConfiguration's** Sources / Sinks list respectively — **not globally**.
  They must be non-empty.
- **No-Transformation contract.** Without a `Transformation` Blob you get only 1:1
  forwarding: `#Sources == #Sinks` and pairs are matched by **`SourceId == SinkId`**.
  With a Transformation, N sources → M sinks is allowed and the Lua return table maps
  each SinkId to its computed value.
- **`aimc_main(sources)` is mandatory in any Transformation Blob**; contentType
  `text/plain`; stateless in v2.0. If a SinkId is not a valid Lua identifier, use the
  `["Sink Id1"]` bracket form in the return table (see §1.4 example).
- **Version drift on the `MappingConfigurations` SML id** (DISCREPANCY 1) — the SML's
  OWN semanticId is printed `.../AssetInterfacesMappingConfiguration/1/0/MappingConfigurations`
  (with `/1/0/`) while its `semanticIdListElement` and every other node use `/2/0/`.
  Freeze it verbatim as `/1/0/` (that is what the official AASX most likely carries),
  but a detector should tolerate BOTH `/1/0/` and `/2/0/` for this one node.
- **List-item idShorts / the `[00]` prefix.** The UML tags list items `[00]`
  (Annex A: an idShort suffix of decimal digits to keep it unique). These SMCs live
  inside SubmodelElementLists (`MappingConfigurations`, `Sources`, `Sinks`), so under
  metamodel v3 they are addressed by index and item idShorts are not required — know
  your target metamodel when serializing/validating (cf. AASd-108/AASd-120).
- **AID and AIMC can be hosted separately** and are authored by different parties
  (AID: asset provider; AIMC: asset user/integrator). Don't assume co-location.
- **`Transformation` is a Blob, not a File.** It is embedded inline (example size
  "0 bytes"), not an .aasx supplementary part.

## AIMC 2.1 (bug-fix release, folder `published/Asset Interfaces Mapping Configuration/2/1`)

On main via PR #332 (merged 2026-09-25; added in commit `5bf65db` "bug fixes for 22 reported
issues: new patch folders", 2026-09-22). README, verbatim: *"This folder contains a bug-fix release of
the submodel template artifacts. It was produced from version 2 and contains only corrections to the
machine-readable artifacts (JSON and AASX). The specification PDF, where present, is carried over
unchanged."* Issues fixed: #187, #207, #208, #210 (generic template-quality issues, none AIMC-specific).

What actually differs from 2.0 (JSON diff of both files, `IDTA 02027_Template_AIMC.json` and
`…_without_examplevalues.json`):
- `administration.templateId` `https://admin-shell.io/IDTA 02027-2-0` → `https://admin-shell.io/IDTA02027-2-0`
  (space removed; it still says 2-0);
- the three SubmodelElementList items `MappingConfiguration` (in `MappingConfigurations`), `Source`
  (in `Sources`) and `Sink` (in `Sinks`) lose their idShort (AASd-120: an SML item has none).

Nothing else: Submodel semanticId stays `…/AssetInterfacesMappingConfiguration/2/0/Submodel`,
`MappingConfigurations` keeps `…/1/0/MappingConfigurations` (DISCREPANCY 1), administration stays `version: "2"`,
`revision: "0"` (2/1 JSON L50-53), every cardinality and semanticId is unchanged, and the PDF is the 2.0 PDF (sha1
`85e1654c…` in both folders). **An AIMC "2.1" submodel cannot be told from 2.0 by semanticId, version or
structure** — only by the absent item idShorts, which a v2.0 instance may also omit. Readers must find
list items by semanticId or position, never by idShort.
"2.1.0" exists only as the catalogue folder name.

### Which 2.0 PDF? (`VERIFY-pdfEdition`)
The PDF bundled with this skill is the May 2026 original (blob `d2b6c31`, commit `d9822f7`). IDTA
re-uploaded it on 2026-07-21 (commit `290e242` "AIMC SMT pdf updated", blob `9dc7972`); that July
edition is what folders `2/0` and `2/1` carry today (local copy: `idta-pdfs:pdf/published/Asset
Interfaces Mapping Configuration/2/1/`). Word diff: every semanticId and
cardinality identical; the July cover prints *"Version 1.0 / May 2026"* (its version history p.2 says
"21.05.2026 2.0"); 21 pages instead of 22; the table-header "Explanation:" cells are empty, and the element
descriptions are drawn but missing from the text layer, so quote descriptions from the May edition
bundled here and confirm them visually in the July PDF.

## AIMC v1.0 (IDTA-02027-1-0): what its tables require

The v1.0 PDF and its text are outside this skill, in the official repository mirror (`idta-pdfs` alias):
`idta-pdfs:pdf/published/Asset Interfaces Mapping Configuration/1/0/IDTA 02027-1-0_Submodel_AssetInterfacesMappingConfiguration.pdf`
(the `.txt` sits under `idta-pdfs:txt/...` at the same path). v1.0 tree, verbatim cardinalities:

| table | element | card. |
|---|---|---|
| 2 | `MappingConfigurations` [SML], `.../1/0/MappingConfigurations` | 1 |
| 3 | `{Configuration #00}` [SMC], `.../1/0/MappingConfiguration` | 0..* |
| 4 | `InterfaceReference` [Ref], `.../1/0/InterfaceReference` | 1 |
| 4 | `MappingSourceSinkRelations` [SML], `.../1/0/MappingSourceSinkRelations` | 1 |
| 5 | `{Relation #00}` [Rel], `.../1/0/MappingSourceSinkRelation` | 0..* |

The template registry (`aas-template-registry`, 1.0.0 and 1.0.1) has JSON and PDF in agreement on the three
card-1 rows. Table 5 only DESCRIBES first (the source) and second (the sink); it has no "shall", and
AAS 3.1 makes `RelationshipElement.first/second` optional (AAS_3_1.xsd `relationshipElement_t`
minOccurs="0"; AAS 3.0 had them mandatory). No v1.0 table says a reference shall resolve.

## Discrepancy / VERIFY list

- **DISCREPANCY 1 — version drift on `MappingConfigurations` semanticId.** Printed
  as `https://admin-shell.io/idta/AssetInterfacesMappingConfiguration/1/0/MappingConfigurations`
  in BOTH Table 2 (child row) and Table 3 (the element's own definition), i.e.
  consistently `/1/0/`, whereas the submodel and all other nodes use `/2/0/`, and
  this same SML's `semanticIdListElement` points at `/2/0/MappingConfiguration`.
  Likely a spec typo (intended `/2/0/`). **Frozen verbatim as `/1/0/`; flag for the
  reader; a validator should accept `/1/0/` OR `/2/0/` for this node only.**
- **DISCREPANCY 2 — brief-vs-spec structure mismatch (v1.0 vs v2.0).** Any brief
  describing `InterfaceReference`, `MappingSourceSinkRelations`,
  `MappingSourceSinkRelation`, or `RelationDirection` reflects **AIMC v1.0**. The
  bundled ground-truth spec is **v2.0**, which removed all of them (Annex C). This
  skill follows v2.0. If a v1.0 instance must be read, note those elements existed
  then but are absent from the v2.0 semanticId set above.
- **No missing-id VERIFY flags.** All 14 semanticIds are legibly printed in the .txt;
  none were invented. (Had any been illegible, it would appear here as
  `VERIFY-<idShort>`.)
- **VERIFY (metamodel `type` of semanticId keys).** Per Annex A the tables give only
  idType+value; the reference `type` ("GlobalReference" for semanticIds; ModelReference
  for the Source/Sink refs) must be set per the metamodel [6]. Confirm against the
  official AASX when generating code.
- **VERIFY (idShort suffix policy).** Whether the official AASX names list items
  `MappingConfiguration`, `Source`, `Sink` bare or with a numeric suffix (`_00_`)
  depends on the serializer/metamodel version — check the reference AASX before
  freezing item idShorts.

## Sign-off checklist

1. Read the bundled IDTA-02027 .txt/.pdf (v2.0). Confirm you are on v2.0, not v1.0.
2. Submodel: idShort `AssetInterfacesMappingConfiguration`, semanticId
   `AIMC/2/0/Submodel`.
3. `MappingConfigurations` SML present (● card 1); freeze its id verbatim as
   `AIMC/1/0/MappingConfigurations` (DISCREPANCY 1) but tolerate `/2/0/` on read.
4. Each `MappingConfiguration` (0..*) carries `Sources` (●) and `Sinks` (●) SMLs;
   `DefaultPollingInterval` (xs:double, 0..1) and `Transformation` (Blob, 0..1)
   optional.
5. Each `Source` (1..*): `Source` **ModelReference** (●) + optional `PollingInterval`
   (xs:double) + `SourceId` (xs:string, ●, locally unique). Each `Sink` (1..*):
   `Sink` **ModelReference** (●) + `SinkId` (xs:string, ●, locally unique).
6. If **no `Transformation`**: `#Sources == #Sinks` and every pair matched by
   `SourceId == SinkId`. If a `Transformation` Blob exists: contentType `text/plain`,
   contains `function aimc_main(sources)`, stateless.
7. For synchronous sources, at least one of `DefaultPollingInterval` /
   `PollingInterval` is set and > 0; ignored for asynchronous (MQTT).
8. Sources referencing an asset point into the **AID (IDTA-02017)**
   InteractionMetadata via the Source ModelReference (AID link is implicit — no
   InterfaceReference in v2.0). AID and AIMC may be hosted separately.
9. Every semanticId verbatim from the table above (14 distinct); no invented ids.
10. Run [[aas-validation]] (XSD + AASd-*); ship a conformance fixture passing the
    official engine before claiming IDTA-02027 conformance.
