---
name: aas-bom
description: Asset Administration Shell Bill-of-Materials / component hierarchy expertise — the IDTA-02011 "Hierarchical Structures enabling Bills of Material" submodel template. Covers the three ArcheTypes (OneDown / OneUp / Full and when each applies), the EntryNode/Node Entity tree, the HasPart / IsPartOf / SameAs RelationshipElements, BulkCount, SelfManaged vs Co-Managed Entities, the globalAssetId join between a parent's BoM and a child's own AAS, resolution via AAS Basic Discovery, the first/second Reference conventions (ExternalReference→globalAssetId vs ModelReference→Entity), and the conformance gotchas (AASd-14, semanticId formats, distinct AAS-id vs asset-id). Use this skill whenever the user models a bill of materials, links assets as parent/child or "part of", builds or reviews a HierarchicalStructures submodel, mentions IDTA-02011, OneDown/OneUp/Full, HasPart/IsPartOf, EntryNode, BulkCount, a component tree, or asks how to relate multiple AAS/.aasx files (e.g. machine → motor → sensor). ALWAYS read the bundled official IDTA-02011 PDF first (see the mandatory step below) — this skill is a map, the PDF is the law.
---

# AAS Bill of Materials (IDTA-02011 Hierarchical Structures)

The canonical reference for modelling an asset's **component hierarchy** as an
AAS submodel: IDTA-02011 *"Hierarchical Structures enabling Bills of Material"*.
It is the submodel a recall, a material-disclosure query, or a DPP component-
traceability walk actually traverses.

This skill complements `aas-knowledge` (the domain map) and `aas-validation` (the
AASd-* constraints). This one is the **BoM field manual**.

## ⚠ MANDATORY FIRST STEP — read the official spec, every time

**Before authoring, editing, reviewing, or validating ANY Hierarchical Structures
/ BoM submodel, you MUST read the bundled official specification** — it is the
ground truth. Memory (yours or this skill's) drifts; the PDF does not. Maximum
compliance means the normative document decides, not a summary.

Read it with the Read tool. The skill bundles TWO copies — read the **text**
extraction (always works; PDF rendering needs poppler which may be absent), and
treat the **PDF** as the authoritative binary:

```
Read: ~/.claude/skills/aas-bom/IDTA-02011-1-0_HierarchicalStructures.txt   ← always readable
      ~/.claude/skills/aas-bom/IDTA-02011-1-0_HierarchicalStructures.pdf   ← authoritative (needs poppler)
```
(In the aas-skills repo: `skills/aas-bom/IDTA-02011-1-0_HierarchicalStructures.{txt,pdf}`.)

It is 21 pages — read the data-model section (Entities, ArcheTypes, the three
relationships) and the examples in full. Do not proceed to author or sign off on
a BoM until you have. If a claim in this skill and the spec ever disagree, **the
spec wins** — and fix this skill.

The quick reference below exists to orient you and to name the gotchas; it is
NOT a substitute for the PDF.

## The three ArcheTypes — pick by whether sub-assets have their own AAS

The `ArcheType` Property (`xs:string`) at the submodel root declares the modelling
style. Verify the exact semantics against the PDF; the decision rule:

- **OneDown** — each asset in the tree has **its own AAS**, and that AAS carries a
  submodel expressing the *one-level-down* view (its direct children). Integration
  is by adding the subsystem into a top-level system via `HasPart`. **This is the
  right choice for "3 separate .aasx files, one per asset" (machine → motor →
  sensor)**: the machine's AAS lists the motor; the motor's AAS lists the sensor;
  the sensor is a leaf (no BoM submodel needed). Child nodes are **SelfManaged**
  Entities (they have their own AAS, identified by `globalAssetId`).
- **OneUp** — the *installation location* view (a child pointing **up** to its
  parent via `IsPartOf`). Lets an asset state where it is installed without needing
  external AAS. Complementary to OneDown.
- **Full** — the **entire** hierarchy (including sub-assets) in a **single**
  submodel. Used when sub-assets are **Co-Managed** Entities that do **not** have
  their own AAS. Also allows a version status to be kept centrally.

**SelfManagedEntity vs CoManagedEntity** is the hinge: a SelfManaged child HAS its
own AAS (→ `globalAssetId`, OneDown/OneUp across files); a Co-Managed child does
NOT (→ modelled inline in a Full hierarchy). AASd-14: a **SelfManagedEntity MUST
carry `globalAssetId` (or `specificAssetIds`)** — verify in the PDF + aas-validation.

## Structure (verify every semanticId + shape against the PDF)

```
Submodel  idShort=HierarchicalStructures
          semanticId ExternalRef → https://admin-shell.io/idta/HierarchicalStructures/1/1/Submodel  (rev 1-1 — see §semanticId)
  ├─ Property  ArcheType  xs:string = "OneDown" | "OneUp" | "Full"   (.../ArcheType/1/0)
  └─ Entity    EntryNode   entityType=SelfManagedEntity   globalAssetId = <THIS asset>   (.../EntryNode/1/0)
       │        ↑ NORMATIVE: the EntryNode MUST be a SelfManagedEntity carrying the
       │          globalAssetId of the asset this AAS administers — never CoManaged, never empty.
       ├─ Entity  <NodeA>  entityType=SelfManagedEntity   globalAssetId = <child A>   (.../Node/1/0)  ← JOIN key (AASd-14)
       ├─ Entity  <NodeB>  entityType=SelfManagedEntity   globalAssetId = <child B>   (.../Node/1/0)  ← SIBLING = same level
       ├─ RelationshipElement  HasPart_A   (.../HasPart/1/0)   first→EntryNode   second→EntryNode/NodeA
       └─ RelationshipElement  HasPart_B   (.../HasPart/1/0)   first→EntryNode   second→EntryNode/NodeB
          (only for kind=Type bulk parts, NOT instance children:)
          Property  BulkCount  xs:unsignedLong = <quantity>   (.../BulkCount/1/0)
```

Relationships (confirm direction + reference form in the PDF):
- **HasPart** — *first has-part second* → `first` = the whole (parent), `second` =
  the part (child).
- **IsPartOf** — the inverse → `first` = the part, `second` = the whole.
- **SameAs** — asserts two nodes are the same asset.
- Use **only ONE** relationship type across the whole submodel (HasPart **XOR**
  IsPartOf, never both). OneDown → HasPart.

### Multiple children at the same level (one parent → N parts)
A `RelationshipElement` is **binary** (one `first` + one `second`) — it CANNOT
express "parent has two parts". For a parent with N children:
- Nest **N sibling `Node` Entities** directly in `EntryNode.statements` (Table 4:
  `Node [1..*]`) — they are the children *at the same level*.
- Create **N `HasPart`** RelationshipElements, one per child, each with
  `second` → that child Node (also `EntryNode.statements` elements, HasPart `[0..*]`).
- **AASd-022**: all siblings in `EntryNode.statements` share ONE namespace, so the
  N Nodes **and** the N HasParts need **distinct idShorts** — you cannot name both
  relationships `HasPart`. Use `HasPart_<Child>` (semanticId stays the same
  `.../HasPart/1/0` on all — it types "HasPart", it is NOT unique).

### BulkCount — omit it for instance children
`BulkCount` (`.../BulkCount/1/0`, `xs:unsignedLong`) is **[0..1] and only valid on a
Node whose asset is `AssetKind=Type`** (spec §1.5.1.5: "with BulkCount only a
reference to an asset with kind type is allowed", e.g. "10× M4×30 type screw").
Every OneDown child that has its own AAS is a **SelfManaged instance** → **omit
BulkCount** (putting it on an instance Node is a semantic violation). (Note the
type is `xs:unsignedLong`, not `xs:long`.)

## The join is `globalAssetId`, resolved by Discovery

The link between a parent's BoM and a child's **own AAS** is the child's
`globalAssetId`: the child `Node` Entity's `globalAssetId` MUST equal the child
AAS's `assetInformation.globalAssetId`. A consumer resolves it to the child's AAS
via **AAS Basic Discovery** — `GET /lookup/shells?assetIds={globalAssetId}` →
child AAS id → fetch from a repository. You do NOT embed the child's AAS-id in the
parent; the `globalAssetId` is the durable, cross-AAS link.

## `first` / `second` References — NORMATIVE: reference the EntryNode/Node

`RelationshipElement.first/second` are **References** (not values). The spec is
explicit (IDTA-02011 §"Scope of the Submodel" + the HasPart/IsPartOf/SameAs rows):

> *"The relationships must contain an EntryNode or Node as first and second
> attribute. The relationships shall only reference EntryNodes or Nodes in the
> same Submodel."*

So `first`/`second` MUST be **`ModelReference`s that point at the EntryNode / Node
Entity ELEMENTS** in this submodel — NOT `ExternalReference → globalAssetId`.
- `HasPart` (inside a Node): `first` = ModelReference → the EntryNode (parent);
  `second` = ModelReference → this Node (the part). (The Node "shall be created
  using this Node as Second attribute".)
- `IsPartOf` (OneUp): the inverse.
- `HasPart` and `IsPartOf` never leave the submodel ("shall only reference EntryNodes or
  Nodes in the same Submodel", IDTA-02011 v1.0 Table 5 p.17-18). Only **`SameAs`** may
  cross: its `first` is an EntryNode/Node, its `second` "may contain an Entity element in
  a different Submodel, including Submodels of a different specification" (Table 5 p.17)
  — still an Entity element reference, not a bare globalAssetId.
- Distributed hierarchies (several submodels): only **Full and OneDown** may be mixed;
  "The "OneUp" archetype cannot be used in a mixed (only Full and OneDown) form with the
  other two forms" (§1.5.1.5 p.11).

A ModelReference to a nested Node walks the tree by keys:
```
first  → keys: [{Submodel, <smId>}, {Entity, EntryNode}]
second → keys: [{Submodel, <smId>}, {Entity, EntryNode}, {Entity, <NodeIdShort>}]
```

The child's **`globalAssetId` still lives on the Node Entity** (`SelfManagedEntity`,
AASd-14) — that is the asset join a consumer resolves via Discovery. The
*relationship* references the Node *element*; the *asset link* is the Node's
globalAssetId. Do not conflate them. `ExternalReference → GlobalReference →
globalAssetId` in first/second is a **conformance violation** (it fails the
"shall only reference EntryNodes or Nodes" rule) even though a viewer that reads
the Node's globalAssetId still renders.

## Recipe: one AAS that carries several assets (several nameplates in one AAS)

Case: a cell, kit or machine is ONE AAS, but its components (robot, positioner,
torch…) are separate physical assets with their own nameplate data, and they get NO
AAS of their own. That is the Co-Managed case, so use **Full** (§1.5.1.3 of
IDTA-02011 v1.0, `.txt` lines 225-229: Co-Managed Entities "typically do not have an
Asset Administration Shell").

```
Submodel HierarchicalStructures   semanticId ExternalReference[GlobalReference …/HierarchicalStructures/1/1/Submodel]
  ├─ Property ArcheType = "Full"
  └─ Entity EntryNode  SelfManagedEntity  globalAssetId = assetInformation.globalAssetId of THIS AAS
       ├─ Entity <Child>  CoManagedEntity  (no globalAssetId, no specificAssetIds)
       ├─ RelationshipElement HasPart_<Child>
       │     first  = ModelReference [{Submodel, <smId>}, {Entity, EntryNode}]
       │     second = ModelReference [{Submodel, <smId>}, {Entity, EntryNode}, {Entity, <Child>}]
       └─ … one Node + one HasPart_<Child> per component (AASd-022: distinct idShorts)
```

- **EntryNode** MUST be a Self-managed Entity "reflecting the Assets administrated in
  the Asset Administration Shell this Submodel is part of" (Table 4, `.txt` lines
  ~556-560, p.15), so its `globalAssetId` MUST equal the AAS's
  `assetInformation.globalAssetId`.
- **Child Nodes** are `CoManagedEntity` (Table 4: "The Entity Node can be a co-managed
  or self-managed entity", `.txt` ~571-572). Leave `globalAssetId` out: metamodel 3.0
  forbids it on a co-managed entity ("They are not existing otherwise",
  `aas-core-meta-v3_0.py:3490-3494`); 3.1 dropped the sentence
  (`aas-core-meta-v3_1.py:3437-3440`), so it is allowed there but not needed.
- **HasPart_<Child>** sits at EntryNode level (Table 4 `HasPart 0..*`, `.txt`
  ~620-636, p.16: "shall only reference EntryNodes or Nodes in the same Submodel";
  Node row: "HasPart shall be created using this Node as Second attribute",
  `.txt` ~576-578).
- **No standard link from a Node to "its" Nameplate submodel.** IDTA-02011 v1.0 has
  no occurrence of "Nameplate" and defines only HasPart / IsPartOf / SameAs. SameAs
  must point at an Entity ("may contain an Entity element in a different Submodel",
  Table 5 `.txt` ~710-713, p.17), so a SameAs to a Nameplate submodel is not
  conformant. Several Nameplate submodels in one AAS are related to the Nodes only by
  naming/convention (e.g. matching idShorts); say so, do not invent a reference.

### Pitfalls of the official template (measured 2026-10-28)

Measured in the template JSON itself (`Hierarchical Structures enabling Bills of
Material/1/1/2/IDTA 02011-1-1-2_Template_HSEBoM_forAASMetamodelV3.1.json` in the IDTA
submodel-templates repository) and on a submodel built from it in an editor.
- The EntryNode's `globalAssetId` is pre-filled with the semanticId IRI
  `https://admin-shell.io/idta/HierarchicalStructures/EntryNode/1/0`. It passes
  AASd-014 (it is set), but it names a concept, not the asset. Replace it with the
  AAS's `assetInformation.globalAssetId`.
- The template's first-level `Node` is a copy of the EntryNode: same placeholder
  `globalAssetId`, `SelfManagedEntity`, and the EntryNode description "Base entry
  point for the Entity tree in this Submodel, this must be a Self-managed Entity…".
  Every Node cloned from it inherits that text.
  Replace or remove the description; switch to CoManaged and drop the globalAssetId.
- The 1.1.2 V3.1 template's submodel semanticId is
  `ModelReference[Submodel …/1/1/Submodel]`. Valid (IDTA-01001 v3.1.2 p.197 removed
  the recommendation to use external references for semanticId), but base 1.1 uses
  `ExternalReference[GlobalReference]` and the key names a Submodel id that is not in
  the file; `ExternalReference` is the safer form for instances (see
  aas-template-registry, "semanticId reference form").

## Conformance gotchas (the ones that bite)

- **AASd-14** — a `SelfManagedEntity` MUST have `globalAssetId` or
  `specificAssetIds`. Every child Node in a OneDown BoM is SelfManaged → must
  carry `globalAssetId`. Metamodel 3.0 adds "They are not existing otherwise", so a
  `CoManagedEntity` must NOT carry them (aas-core-meta v3_0.py:3490-3494); 3.1 dropped
  that sentence, so a co-managed Node may carry them (v3_1.py:3437-3440).
- **AASd-022** — sibling `idShort`s unique within a collection. Dedup child Node
  idShorts (suffix repeats).
- **semanticId format + version** — elements: `https://admin-shell.io/idta/HierarchicalStructures/<Name>/1/0`
  (EntryNode, Node, ArcheType, HasPart, IsPartOf, SameAs, BulkCount). The **submodel**
  semanticId is version-dependent and must NOT be mixed with the elements: the bundled
  PDF is **rev 1-0** → submodel `.../HierarchicalStructures/1/0/Submodel`; **rev 1-1**
  (the "v1.1.x" template) bumped only the submodel to `.../1/1/Submodel` while the
  **element** semanticIds stayed at `/1/0`. Pick the pair for your target template
  version; do not emit `/1/1` elements. Verify casing/version against the PDF.
- **AAS-id ≠ asset-id** — the shell `id` and `assetInformation.globalAssetId` are
  DIFFERENT identifiers and should be distinct URIs (e.g. `…/aas/…` vs `…/asset/…`).
  Do not ship a `urn:extracted:…` synthetic placeholder as a real product asset id;
  give each asset a proper, stable URI.
- **XML Entity element order** (AAS 3.1 XSD): `statements` → `entityType` →
  `globalAssetId`. Emitting them out of order fails the XSD.
- **Reciprocal is optional** — in OneDown, the parent declares its parts; the child
  does NOT need an `IsPartOf` back-reference. Only add the OneUp reciprocal when you
  want the installation-location view.

## Adding a component = one edit on the PARENT's AAS

Linking a child into a parent's BoM is a change to the **parent** model only:
create the HierarchicalStructures submodel (if absent), add the child `Node`
(globalAssetId = child), the `HasPart` (parent → child), and a `BulkCount` only if the
child is a Type asset (see "BulkCount" above; never on a SelfManaged instance). It
does NOT write to the child's `.aasx`. A multi-level chain (machine → motor →
sensor) is built one level at a time, each on that parent's own AAS.

## Implementation notes (lessons from a production editor)

- Keep the BoM generators PURE (add part, set quantity, remove part, list parts,
  new HierarchicalStructures): deep-clone the input, never mutate live UI state.
  An editor tree may nest Entity children under `children`; the serializer maps
  them to native `statements`.
- Resolve `globalAssetId → model` on the owner side; a PUBLIC resolver must only
  link public children and show the rest as "external".
- Emit `HasPart` / `IsPartOf` `first`/`second` as `ModelReference → EntryNode/Node`
  (key path `[Submodel, EntryNode, <Node>]`); the child's `globalAssetId` lives on the
  Node Entity, NOT inside the relationship. Regression-test that the globalAssetId
  string does NOT appear anywhere in the relationship.
- LEGACY DATA authored with `ExternalReference → globalAssetId` in `first`/`second`
  must be re-emitted to become conformant; the Node's `globalAssetId` is unaffected.

## Sign-off checklist (only after reading the PDF)

1. Read `skills/aas-bom/IDTA-02011-1-0_HierarchicalStructures.pdf` — done?
2. ArcheType matches the topology (OneDown for per-asset AAS files).
3. Every child Node is a SelfManagedEntity WITH a `globalAssetId` (AASd-14).
4. Each child's `globalAssetId` EXACTLY equals that child AAS's
   `assetInformation.globalAssetId` (the join resolves via Discovery).
5. semanticIds match the spec (submodel `/1/1/Submodel`; elements `/<Name>/1/0`).
6. `HasPart` direction + `first`/`second` reference form match the PDF examples.
7. AAS-id and asset-id are distinct proper URIs (no `urn:extracted:` placeholders).
8. Run it through `aas-validation` (AASd-* + XSD + aas-test-engines).
