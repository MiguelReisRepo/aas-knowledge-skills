---
name: aas-validation
description: Asset Administration Shell (AAS) validation expertise — the canonical catalogue of all 79 AASd-* metamodel constraints (extracted verbatim from IDTA-01001 Part 1 Metamodel v3.2), the diagnostic decision tree (XSD vs AASd-* vs aas-test-engines), per-rule fix recipes, the auto-fix vs flag-for-human philosophy (production-tested over 63 repair passes), how to read aas-test-engines output, and CI/CD validation patterns (golden snapshots, per-rule fixtures, independent conformance gate). Use this skill whenever the user is debugging an AAS validation error, sees an AASd-* error code, asks "is this AAS valid", needs to fix an .aasx / AAS XML / AAS JSON, designs a validator, runs aas-test-engines, sets up CI for AAS conformance, or writes auto-repair logic for malformed AAS files. Trigger even when the user just pastes a validator error string without context, or shows an AAS file fragment asking "what's wrong with this".
---

# AAS validation

The canonical reference for validating AAS files (AAS 3.x XML / JSON /
.aasx) against the IDTA metamodel. The XSD catches **structural**
problems; the AASd-* gate catches the **semantic** rules the XSD cannot
express. A file is valid only when it clears **both** gates plus the
independent IDTA conformance check (`aas-test-engines`).

This skill complements `aas-knowledge` (which is the domain map). This one
is the **field manual**: given an error, what does it mean, how do you fix
it, and what should never be auto-fixed.

The 79 AASd constraints in §3 are extracted **verbatim from IDTA-01001
Part 1 Metamodel v3.2**. When in doubt about the exact wording or normative
context, consult the spec PDF at industrialdigitaltwin.io.

---

## 1. The validation pipeline

```
input.xml / .aasx
   │
   ▼
[0. detect revision]          Read the xmlns DECLARATION (anchored — a loose
   │                          substring also matches an id or a Property value
   │                          carrying the IRI, which routes the file to the
   │                          wrong schema). JSON has no namespace: take the
   │                          caller's request, else a $schema/$id hint, else
   │                          default — and always REPORT which was used.
   ▼
[1. pinned XSD for THAT       xmllint-wasm against the bundled 3.0 / 3.1 / 3.2
    revision]                 schema. Catches structural failures: missing
   │                          required elements, wrong types, malformed enums,
   │                          attribute-vs-element mistakes.
   ▼ structural OK?
[2. AASd-* gate, gated on     Semantic rules from IDTA-01001 §C.1. Apply ONLY
    THAT revision]            the rules that revision contains — see the
   │                          revision ledger below.
   ▼ semantic OK?
[3. IDTA aas-test-engines]    The IDTA's official reference implementation —
                              but it implements metamodel 3.0.1 ONLY. For a
                              3.0 file it is the authoritative tie-breaker.
                              For 3.1/3.2 it is judging a revision it does not
                              know, so its findings are ADVISORY: surface them,
                              never let them fail the document.
   ▼ conformance OK?
file reports valid: true
```

**Every stage judges the document by ITS OWN declared revision.** That is the
invariant the pipeline exists to protect — checking a conformant file against
the wrong revision's rules yields a false "invalid", which is worse than no
answer at all.

**Report shape:** the response shape should distinguish how far the pipeline
went. A conventional shape:

- `validation: 'structural'` — XSD passed, AASd-* not yet run (degraded mode).
- `validation: 'semantic'` — XSD + AASd-* both passed. Also the CEILING for a
  3.1/3.2 document, since the engine can only advise on those.
- `validation: 'full'` — XSD + AASd-* + aas-test-engines judging the document at
  its OWN revision, all green. Today that means AAS 3.0 only.

> **Structural = BOTH serializations.** An `.aasx` ships an `.aas.xml` AND an
> `.aas.json` of the same Environment. The XSD only checks the XML; the AAS 3.1
> **JSON schema (draft-2019-09)** is stricter on facets the XSD can't express
> (langString `text` maxLength 1023/128; MLP `value` `minItems:1`; `submodels`/
> `conceptDescriptions` `minItems:1` so an EMPTY array is INVALID — omit it). So a
> `.aas.json` can be schema-INVALID while its `.aas.xml` is XSD-valid. Report
> `structural`/`valid` only when BOTH pass. In the browser use a draft-2019-09 JS
> validator (`@cfworker/json-schema` — zero-dep; the older `ajv@6` is draft-07 only).
>
> **Provenance principle (hard bar):** EVERY emitted error/warning must cite an
> identifiable OFFICIAL source (an AASd-XXX/AASc-XXX, an XSD facet, a JSON-schema
> pointer, an IEC61360 rule, or an IDTA template requirement) — no invented rules,
> no fabricated AASd numbers. NEVER emit a rule that does not exist in the
> document's OWN revision (see the revision ledger below). A rule-registry + a CI
> guard that fails on an unregistered citation or an emitted removed-rule is the
> enforcement. And "valid" must be 100% certain — the official
> schema(s) actually RAN and passed; "couldn't run" is a distinct UNVERIFIED state,
> never shown as valid.

### ⚠️ Revision ledger — the AASd set is NOT nested across 3.0 / 3.1 / 3.2

**Gate every rule on the revision the DOCUMENT declares, in BOTH directions.**
3.1 both adds to and *removes from* 3.0. The removal direction is the dangerous
one: applying a deleted rule reports a **conformant** document as INVALID, which
is worse than not checking at all.

| Rule | 3.0 | 3.1 | 3.2 | Normative change note |
|---|:--:|:--:|:--:|---|
| **AASd-013** | ✗ | ✗ | ✗ | Removed in **V2.0.1** — predates all of 3.x. Open-bounds Range is valid. |
| **AASd-027** | ✗ | ✗ | ✗ | Removed in **V3.0**; folded into the `NameType` datatype (schema enforces 128 chars). |
| **AASd-090** | ✓ | ✗ | ✗ | «REMOVED: remove AASd-090: category is deprecated (#514)» |
| **AASd-120** | ✓ | ✗ | ✗ | «REMOVED: remove AASd-120: idShort also allowed for elements within a SubmodelElementList (#432)» |
| **AASd-137** | ✗ | ✗ | ✓ | «NEW: Constraint AASd-137 for References (#592)» |
| **AASd-138** | ✗ | ✗ | ✓ | «NEW: Constraint AASd-138 for SubmodelElementList for OperationVariable (#462)» |

> **Provenance — verified 2026-08-28 against the official PDFs, page-cited.** This
> table is the burden-of-proof evidence; cite it verbatim when someone's validator
> disputes a verdict.
>
> | Document | sha256 | Finding |
> |---|---|---|
> | [Part 1 v3.1.1](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.1.1/part-1-metamodel.pdf) · 264 pp | `d4cfafe29e82b92c5e5570f53ccf81a2d07234e4cd35c815f7d8d03dbc0fb3ff` | `AASd-138`: **0 occurrences**. Change notes: «REMOVED: remove AASd-120 (#432)», «REMOVED: remove AASd-090 (#514)», plus change-table rows `AASd-090 \| Removed`, `AASd-120 \| Removed`. Highest AASd present: 136. |
> | [Part 1 v3.2](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.2/part-1-metamodel.pdf) · 290 pp | `a8a5c16c4477932867bbe66d7e165da4edcc7e611b79c0cfa2b3dcb4558e1737` | **p.218** change table: `AASd-138 \| New`. **p.215**: «NEW: Constraint AASd-137 for References (#592) · NEW: Constraint AASd-138 … (#462)» under *"Changes V3.2 vs. V3.1.2"*. Normative text pp. 61 and 209. Highest AASd present: 138. |
> | Part 1 v3.1.2 (industrialdigitaltwin.org PDF, vendored `idta-specs:pdf/IDTA-01001-3-1-2_…pdf`) · 267 pp | `63e0e15cd22121367e2687cef02cd233e4b033537aa4ae4f8b05937b8539b9d1` | **p.196** under *"Changes V3.1 vs. V3.0.2"*: «REMOVED: remove AASd-120: idShort also allowed for elements within a SubmodelElementList (#432)», «REMOVED: remove AASd-090: category is deprecated (#514)»; change table p.199 `AASd-090 Removed`, p.200 `AASd-120 Removed`. 79 distinct AASd numbers, highest 136, no 137/138. |
> | Part 1 v3.2 (industrialdigitaltwin.org PDF, vendored `idta-specs:pdf/IDTA-01001-3-2_…pdf`; bytes differ from the .io file above) · 290 pp | `882e2e30788e788a6a52cf07fbae0398f0769738db6bcf2cf5126d7a99701615` | Same 090/120 removal notes; AASd-137 and AASd-138 present; 81 distinct AASd numbers. |
> | Part 1 v3.0 (bundled) | `8ba8171554defdb9b81a112f9ce6f86ae4447529e854290272d8b8241e175f0e` | Neither `AASd-137` nor `AASd-138` appears; no 090/120 removal rows — both live in 3.0. |
>
> **This ledger has now outranked production code twice.** A constraint gate asserted
> in its own header that "3.0 ≡ 3.1 … nothing has ever been removed" and therefore
> emitted `AASd-090` and `AASd-120` against every 3.1 document — two deleted rules
> reporting conformant files invalid. When code and this table disagree, **re-derive
> from the PDFs; do not assume the code encodes the check it claims.**

**3.1 also RELAXED cardinalities** — mandatory in 3.0, optional from 3.1. A 3.0-era
checker rejects a conformant 3.1 file that omits any of these:
- `File/contentType`, `Blob/contentType` (#412)
- `RelationshipElement/first`, `/second` — and so `AnnotatedRelationshipElement` (#412)
- `Entity/entityType`, which also relaxes **AASd-014** (#287)

**AASd-002 keeps its id but changed its PATTERN**: 3.0 is `[a-zA-Z][a-zA-Z0-9_]*`
(1 char legal, no hyphen); 3.1+ is `[a-zA-Z][a-zA-Z0-9_-]*[a-zA-Z0-9_]+` (min 2
chars, mid-string hyphen legal). The bundled XSDs agree — so the same idShort is
legal in 3.0 and illegal in 3.1.

> **Tooling caveat — aas-test-engines is a 3.0-only oracle.** `aas-test-engines`
> 1.0.3 implements metamodel **3.0.1 only**; to check a 3.1/3.2 file you must
> namespace-downgrade it, which makes the engine apply 3.0's rules — it will
> report AASd-090/AASd-120 and the relaxed-cardinality fields on a perfectly
> conformant 3.1 file. **Treat its verdict as authoritative only for 3.0**; for
> 3.1+ demote its findings to advisory and drop any that cite a rule the
> document's revision does not contain.

> **Method note for verifying any of this**: read the *change notes* of the
> official Part 1 PDF, and trust ONLY an explicit `Removed` / `REMOVED` row.
> Absence of a constraint from extracted body text is NOT evidence of removal —
> PDF text extractors mangle the constraint boxes and tables (this wrongly
> suggested AASd-135/136 were absent when they are live).

> **Packaged gate (CLI + GitHub Action).** The XSD + AASd-* + auto-fix pipeline
> is exposed standalone as `aas-gate` (`docs/AAS_GATE_CLI.md`,
> `.github/actions/aas-gate`), framework-free (`runAasGate`) so any AAS project can gate CI without the web app:
> `aas-gate <files> [--fix] [--json] [--fail-on=both]` — exit 1 on failure. It
> enforces the same XSD-first short-circuit and degrades to AASd-*-only
> (`stage: 'structural'`) when xmllint-wasm can't initialise.

> **⚠️ STAGE 3 IS NOT OPTIONAL, AND IT IS RUNNABLE (measured 2026-08-24).**
> An editor's export cleared the official 3.1 XSD, cleared the official
> JSON schema, and cleared our own AASd gate with **0 errors and 0 warnings** —
> and `aas-test-engines` 1.0.3 then reported it NON-CONFORMANT:
> `AASd-121 violated: first key must be one of GloballyIdentifiables` and
> `AASd-123 violated: first key must be one of AasIdentifiables`, both on the
> AID's `security` ReferenceElement. The violation was real (the exporter had
> dropped an empty-valued leading `Submodel` key, promoting a
> `SubmodelElementCollection` to first position). **Two green schema gates are
> not a conformance verdict.**
> Run it on the shipped JSON — `file.check_json_data(doc, version="3.0")`. The
> 3/1-vs-3/0 limitation below is about the XML ROOT NAMESPACE; JSON has none, so
> the JSON path runs meaningfully against 3/1 documents, and AASd-121/123 are
> identical in 3.0 and 3.1.
> Corollary: **our gate emitting AASd-123 does not mean it SEES every
> violation.** It did not walk this one (a ReferenceElement nested inside
> SMC/SML template data). Treat "our gate is clean" as necessary, never
> sufficient.

> **Tooling caveats — `aas-test-engines` is NOT an unconditional tie-breaker.**
> Validate against the XSD **matching the document's own namespace** (3/0, 3/1 or
> 3/2), from a PINNED bundled copy — never the moving `master` branch, which now
> serves 3.2 and rejects every conformant 3.0/3.1 file with `No matching global
> declaration`.
> `aas-test-engines` ≤ 1.0.3 only supports **3/0** and rejects a 3/1 file at
> the root (`invalid namespace`). For 3/1+ files, validate with **xmllint against
> the pinned XSD of that revision** — don't rely on aas-test-engines alone. That
> version also has a **known false positive on AASc-3a-004/005/006** (it compares
> the DataTypeIec61360 enum against a string set, so it fires on any CD carrying
> a `category`). When the engine and the XSD disagree on namespace or on
> AASc-3a-004/005/006, the XSD wins.

**Never report `valid: true` after only XSD.** A structurally-valid file can
still violate AASd-022 (idShort uniqueness), AASd-119 (kind alignment),
AASd-131 (AssetInformation), and many others without the XSD catching it.

---

## 1b. The verdict is LAW — deterministic, not opinion

"Is this AAS valid?" must give the **same answer every time**, decided ONLY by
normative sources. It is never "valid today, invalid tomorrow" because a person
or another tool asserted so.

**The verdict function.**
- `VALID`   — the official schema(s) for the file's version **actually ran and
  passed** (XSD for the XML; the draft-2019-09 JSON schema for the JSON — BOTH for
  an `.aasx`) AND no **normative** AASd/AASc MUST fired.
- `INVALID` — at least one diagnostic cites a **specific normative source that
  fired** (see below).
- `UNVERIFIED` — a required schema could NOT be run (asset outage, unbundled
  version, or a tie-breaker that doesn't support the version). NEVER shown as valid.

**A finding is a VIOLATION only if it cites a normative source that fired:** an
**XSD facet**, a **JSON-schema keyword**, a numbered **AASd-XXX / AASc-XXX**, or an
**aas-test-engines** failure. No such citation ⇒ it is **NOT a violation** — an
advisory/data-quality note at most.

**Two kinds of non-AASd code — do NOT collapse them (corrected 2026-08-31).** This
paragraph used to say every internal code is "WARNING-only, never ERROR", listing
`value-type` and `range-order` among them. That is **wrong in practice and
dangerous**: both are emitted as BLOCKING errors in the production wizard, and
reading the old wording literally leads to *demoting a real constraint*, which is
a false-VALID — the exact failure this section exists to prevent.

| kind | what it is | severity | examples |
|---|---|---|---|
| **app-normative** | a requirement the METAMODEL really imposes that simply carries no AASd number | **ERROR** | `APP-PROPERTY-VALUE-TYPE`, `value-type` (Range), `range-order`, `APP-EXPORT-DROP` |
| **internal** | an app HEURISTIC no norm requires | **WARNING only** | `reference-resolution`, `lang-string`, `template-conformance`, `template-migration`, `relationship-endpoints` (since 2026-09-14), `iec61360-language-repeated` |

Only the second kind is warning-only. The first is a MUST wearing a slug instead
of a number, and must never be demoted just because it has no AASd id.

⚠️ **Before calling the serialization schema "laxer than the metamodel", check
the metamodel REVISION.** This skill used to cite RelationshipElement `first`/
`second` as the example: "the 3.1 XSD gives them `minOccurs=0` while the metamodel
keeps 1..1". That was the **3.0** metamodel, and it contradicted the relaxation
list above (#412). Corrected 2026-09-14 with three primary sources:
- **aas-core-meta** (the machine-readable metamodel the official schemas are
  generated from): v3.0 `first: "Reference"`, v3.1 `first: Optional["Reference"]`.
- **Official XSDs:** 3.0 `<xs:element name="first" type="reference_t"/>` (required);
  3.1 and 3.2 `minOccurs="0" maxOccurs="1"`. BasicEventElement `observed`/
  `direction`/`state` stay required in all three, so the change is deliberate.
- **Official 3.1 JSON schema:** neither is in `required`.

So for a 3/1 document a relationship without endpoints is **legal**, and an
exporter that drops it loses data. An app-normative rule
follows the metamodel of the revision the document declares, never an older one.

**Burden of proof is on INVALID.** To overturn a verdict where the official
schemas + the AASd gate passed, you MUST name the specific normative rule.
- **Another tool's red-X is NOT a normative source.** Another editor's "6
  errors", a vendor validator, a linter — map each claim to a concrete XSD facet /
  JSON-schema keyword / AASd / AASc / aas-test-engines failure. If none exists, it
  is **their false-positive**, and our VALID stands.
- **A human's assertion is NOT a normative source either.** When challenged, RUN
  the gate against the norm (xmllint vs the official XSD; jsonschema vs the official
  JSON schema; grep the metamodel for the constraint) and report the verdict the
  evidence gives — even if it contradicts the challenger. Do not "agree" to end a
  disagreement; adjudicate it.

**Settled non-violations (case law — do NOT re-litigate).** Provably-non-normative
patterns, with the proof, so the answer is fixed:

| Pattern | Verdict | Proof + code behaviour |
|---|---|---|
| **langString duplicate-language** in a langStringSet (`description` / `displayName` / MLP `value`) — e.g. `description` with 3× `en` | **VALID** — **never an ERROR** | Official XSD (`langStringTextType` is `maxOccurs="unbounded"`, **no `xs:unique`**; our bundled XSD is byte-identical to `aas-specs-metamodel@v3.1.2`) VALIDATES a 3×`en` `description`; official JSON schema → 0 errors; **no** AASd/AASc on language uniqueness (AASd-012 = MLP value/valueId meaning, unrelated); aas-test-engines can't run 3/1. Code (`validateLangStringUniqueness`): a **`description` is NOT flagged at all** (free-form multi-note annotation — the IDTA Nameplate `Arbitrary*` placeholders ship 3× `en` notes, spec-allowed); a **`displayName` / MLP `value`** with a repeated language gets an **advisory WARNING** (genuine ambiguity) — never an error. A tool labelling any of these "XML_SCHEMA violation" is a false-positive on its side. |
| **`semanticId` / `supplementalSemanticId` pointing OUTSIDE the package** — e.g. DppMetadata's `semanticId` = ModelReference→`admin-shell.io/idta/cds/dppMetadata/1` (a submodel-key concept not in the .aasx) | **VALID** — **not even a warning** | A `semanticId` is a HasSemantics reference to a SEMANTIC DEFINITION (concept / CD / submodel template) — **external by design.** **No AAS constraint requires it to resolve in-package:** the reference constraints AASd-121..128/137 are key-CHAIN STRUCTURE only, and AASd-118 is "supplementalSemanticId ⇒ a main semanticId is present" (presence, not resolution). The IDTA templates themselves ship external concept semanticIds. Our internal `reference-resolution` heuristic (a "deliberately-internal non-AASd code") must therefore **exclude semanticId/supplementalSemanticId** — flagging them "dangling reference" was a false-positive. The check stays for genuine element-VALUE linkages (`valueId`/ReferenceElement/Relationship). |
| **`semanticId` / `supplementalSemanticId` given as a `ModelReference`** instead of an `ExternalReference` — e.g. the submodel semanticId as one key of type `Submodel` (how 85 of the 155 pinned IDTA template versions ship it, see aas-template-registry "semanticId reference form"), or a key of type `ConceptDescription` | **VALID** — **no error and no warning** | aas-core-meta v3.1 `Has_semantics` (`aas-core-meta-v3_1.py:1476` for `semantic_ID`, same note at `:1486` for `supplemental_semantic_IDs`): *"It is recommended to use a global reference."* That note is stale: IDTA-01001 v3.1.2 (p.197) lists "REMOVED: remove recommendation to use external references for semanticId (#376) and related attributes like valueId, semanticIdListElement and isCaseOf". Even under 3.0 it was a recommendation (note), not an invariant: no AASd constrains the reference TYPE of a semanticId. AASd-121..128/137 check only the key chain of whatever reference is given (for a ModelReference: first key an AasIdentifiable, AASd-123), and AASd-118 only requires a main semanticId when supplemental ones exist. **Trap:** do not call it an error, and do not raise a warning that reads like one; on 2026-10-28 it was mis-reported as an error and had to be withdrawn. At most a tool may offer to normalise a single-`Submodel`-key reference to `ExternalReference[GlobalReference <same value>]`; a `ConceptDescription` key, a multi-key chain, or one naming another submodel of the environment is left as is. |

| **`AASd-138` fired on a 3/1 document** — e.g. "a SubmodelElementList in a Template submodel must have exactly one element (found 0)", reported ×9 by a partner's validator on a conformant 3.1 `.aasx` | **VALID** — the rule does not exist in 3.1 | `AASd-138` is **NEW in 3.2**: official v3.2 PDF **p.218** change table `AASd-138 \| New`, **p.215** «NEW: Constraint AASd-138 … (#462)» under *"Changes V3.2 vs. V3.1.2"*; the v3.1.1 PDF has **0 occurrences** (shas in the provenance block above). A document declaring `admin-shell.io/aas/3/1` is judged by 3.1's set — applying a 3.2 rule to it is the SAME class of false-invalid as the settled `AASd-013` case. **Corollary worth knowing before anyone builds an "auto-fix":** of the 12 official IDTA templates checked, only **IDTA-02017 (Asset Interfaces Description)** violates AASd-138 — 39 SMLs with 0 elements (`security`, `enum`, `scopes`, `oneOf`/`allOf`, `htv_headers`, `iolv_payloadMapping`…). Every other official template already carries exactly one exemplar child. So the official AID template is itself not 3.2-clean: an auto-fix inserting placeholder children would be "correcting" IDTA's own template, and fabricating a value that ships in a downloaded `.aasx` is forbidden. Report and guide; never fill. |

| **A SubmodelElementList child that SHIPS but loses its `idShort`** — e.g. `Marking001` inside the IDTA Nameplate's `Markings` SML | **was not a drop; the underlying strip is now FIXED** | An exporter that strips the idShort of every DIRECT SML child emits the element while discarding its name, so any check that looks for it BY NAME in the output concludes it vanished. A drop-detector built that way accused `Marking001` — an element of the stock Nameplate template — and, being blocking, made a plain Nameplate impossible to publish (caught live 2026-08-31). The strip itself cited **AASd-120, which was REMOVED in 3.1** (#432): a 3.1 list child may legally carry an idShort, so the strip was enforcing a foreign rule AND losing the template's own names. **Check which behaviour an exporter has before writing a name-based diff:** if it strips, skip direct SML children; if it keeps, do not — and if it strips while emitting 3/1, that is the bug to fix, not to work around. Downstream symptom worth recognising: after an export→import round-trip the AIMC target column shows `[0]` instead of `Marking001`, because no name survived. |

Add a row here (with its proof) each time a "is X valid?" question is settled
against the norms, so it is never flip-flopped again.

---

## 2. Diagnostic decision tree

When the user pastes a validator error or says "this file won't import",
walk through this tree before guessing:

```
Q: Does the file parse as XML / JSON?
├── No  → encoding / BOM / malformed root element.
│        Look at: file declaration line, first 32 bytes for BOM,
│        namespace declaration on root <environment>.
└── Yes
    ├── Q: XSD valid?
    │   ├── No  → STRUCTURAL failure (not AASd).
    │   │        Most common in production:
    │   │        - wrong namespace (3.0 vs 3.1/3.2)
    │   │        - missing required attributes (idShort, id on Identifiable)
    │   │        - wrong child ordering inside complexType
    │   │        - File without contentType (3.0 only; optional from 3.1, see #412 above)
    │   │        - empty langString text
    │   │        - reference key written as XML attributes instead of children
    │   │        - <value>abc</value> with valueType=xs:int
    │   └── Yes
    │       ├── Q: AASd-* gate clean?
    │       │   ├── No  → SEMANTIC failure. See §3 table for the rule;
    │       │   │        most-encountered: AASd-002, AASd-012, AASd-014,
    │       │   │        AASd-020, AASd-022, AASd-119, AASd-121, AASd-131.
    │       │   │        FIRST check the rule exists in the doc's revision
    │       │   │        (see the revision ledger).
    │       │   │        Each row has the failure pattern + fix recipe.
    │       │   └── Yes
    │       │       └── Q: aas-test-engines clean?
    │       │           ├── No  → CONFORMANCE failure (not pure metamodel).
    │       │           │        Most common: submodel's semanticId doesn't
    │       │           │        match the claimed IDTA template (e.g. you
    │       │           │        labelled a SMC "Nameplate" but the
    │       │           │        semanticId resolves to TechnicalData), or
    │       │           │        a template-required element is missing.
    │       │           └── Yes → file is valid.
```

**Order matters.** The first failure can mask later ones (e.g., XSD fails
on missing `<id>`, you never get to the AASd-022 idShort uniqueness check
that would also have failed). Always rerun the full pipeline after each
fix, never trust a single-stage green light.

---

## 3. The canonical AASd-* constraint catalogue

> **Provenance audit, 2026-09-15 (read this before trusting any row).** Every row
> below was cross-checked against the primary sources available locally:
> IDTA-01001-3-0 (body and Annex H "Metamodel Changes"), aas-core-meta
> v3.0/v3.1/v3.2 (`:constraint` declarations) and the official 3.1 schemas. The
> **Source** column gives the literal location. Rows that Annex H marks
> Removed or Renamed before V3.0 was published are now marked so, whatever the
> earlier status said; 34 rows were affected, including AASd-001, 003, 008, 023,
> 026, 051, 053 to 063, 065 to 069, 070 to 075, 092, 093 and 100. The claim below
> that this table is "extracted from v3.2" could not be verified when written: the
> v3.1.2 and v3.2 PDFs were not on disk, and aas-core-meta v3.2 declares none of the
> rows marked removed. Both PDFs are vendored since 2026-10-28 (`idta-specs:`); the
> row-by-row re-check of those 34 rows against them is still open.
> Rule: a constraint number is cited only with its literal source; an inference
> is never presented as the norm.

**Source: IDTA-01001 Part 1 Metamodel v3.2** (`industrialdigitaltwin.io`).
This table is the complete enumeration extracted from the spec.

Status legend:
- **prod** — emitted by the reference production constraint gate this table was
  checked against.
- **static** — statically checkable from the file alone but not yet emitted
  by the gate.
- **context** — needs external resolution (registry / cross-reference) to verify.
- **legacy** — pre-3.x AccessControl / Permission rules, kept for back-compat.
- **deprecated** — referenced in the spec but marked Removed; do not check.

> ✅ **The gate's spec IDs are now the spec's IDs — match by the AASd
> number directly.** A correction pass in the reference gate
> fixed the earlier mislabelling (the file's header doc comment carries the
> corrected mapping verbatim). The gate's code list carries these **27 AASd codes**:
> 002, 005, 013, 014, 020, 021, 022, 077, 090, 107, 108, 109, 116, 117,
> 118, 119, 120, 122, 123, 124, 125, 127, 128, 131, 134, 137, 138 — but per the
> revision ledger above it may emit 090 and 120 ONLY on a 3.0 document, 138 ONLY on
> 3.2, and 013 NEVER (removed in V2.0.1; any emission is a bug) — each
> under its CORRECT spec ID (e.g. AASd-131 = AssetInformation has a
> globalAssetId/specificAssetId; AASd-014 = SelfManagedEntity has one;
> AASd-020 = **Qualifier**/value ↔ Qualifier/valueType consistency (REFORMULATED
> from Property in v3.1 — verified vs IDTA-01001-3-1-2; Property value/valueType is
> NOT a numbered AASd in 3.1.x, so cite it internally, e.g. `APP-PROPERTY-VALUE-TYPE`,
> never `AASd-020`); AASd-021 = at most one
> Qualifier per type). It also emits `AASc-3a-010` (IEC61360 value and valueList
> mutually exclusive; until 2026-09-14 it mislabelled a repeated language with this
> id, now `iec61360-language-repeated`) plus four deliberately-internal non-AASd codes:
> `value-type` (value parses against valueType — NOT spec AASd-090),
> `lang-string` (description langString cardinality — NOT spec AASd-012),
> `range-order` (numeric Range min ≤ max), and `reference-resolution`
> (submodel ModelReferences resolve in-environment). The old "map by
> message text, IDs are wrong" warning, and the previously-emitted codes
> AASd-012 and AASd-114, no longer apply.

### 3.1 Identification, naming, uniqueness

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-001** | Referable | `idShort` is mandatory on every Referable that is not an Identifiable. | **removed**: do not check (was `static`) | IDTA-01001-3-0 Annex H p.158: Removed (V3.0 vs. V2.0.1) |
| **AASd-002** | Referable.idShort | `idShort` consists of at least two characters and only of letters, digits, hyphen, underscore; starts with a letter; does not end with a hyphen: `^[a-zA-Z][a-zA-Z0-9_-]*[a-zA-Z0-9_]+$`. | prod | aas-core-meta v3.1 `:1426` |
| **AASd-003** | Referable.idShort | `idShort` of Referables within the same name space is unique (case-sensitive). | **removed**: do not check (was `static`) | IDTA-01001-3-0 Annex H p.158: Removed (V3.0 vs. V2.0.1) |
| **AASd-022** | Referable.idShort | `idShort` of non-identifiable Referables within the same name space is unique (case-sensitive). | prod | aas-core-meta v3.1 `:1644` |
| **AASd-027** | Referable.idShort | ⚠️ **REMOVED in V3.0** — exists in NO 3.x revision. Verbatim from the change notes ("Changes V3.0 vs. V3.0RC02"): «AASd-027 \| Removed \| Not needed any longer since Type of idShort was changed to NameType and NameType has a maximum length of 128 characters». The 128-char ceiling is REAL but is carried by the `NameType` datatype, so the **XSD/JSON schema already enforces it** — if you also check it in a constraint gate, cite an internal code (e.g. `idshort-length`), never AASd-027. | removed | IDTA-01001-3-0 Annex H p.167: Removed (V3.0 vs. V3.0RC02) |
| **AASd-077** | Extension.name | The name of an Extension within `HasExtensions` is unique. | prod | aas-core-meta v3.1 `:1523` |
| **AASd-100** | string | An attribute with data type "string" must not be empty (where required). | **removed**: do not check (was `static`) | IDTA-01001-3-0 Annex H p.167: Removed (V3.0 vs. V3.0RC02) |
| **AASd-117** | Referable.idShort | `idShort` of a non-identifiable Referable that is NOT a direct child of a SubmodelElementList shall be specified (literal: "not being a direct child of a Submodel_element_list"; i.e. idShort is mandatory for every Referable except Identifiables and the direct children of a SubmodelElementList; corrected 2026-10-02, the earlier paraphrase said "not equal to SubmodelElementList"). | prod | aas-core-meta v3.1 `:1432` |
| **AASd-120** | SubmodelElementList children | `idShort` of submodel elements being a direct child of a SubmodelElementList must NOT be specified (the index identifies them). ⚠️ **AAS 3.0 ONLY — REMOVED in 3.1.** Verbatim ("Changes V3.1 vs. V3.0.2"): «• REMOVED: remove AASd-120: idShort also allowed for elements within a SubmodelElementList (#432)». A 3.1+ list child MAY carry an idShort; flagging it there is a **false invalid**. | 3.0 only | IDTA-01001-3-0 p.105; removal: IDTA-01001-3-1-2 p.196 + p.200; aas-core-meta v3.0 `:2755`; absent from v3.1 |
| **AASd-130** | string | An attribute with data type "string" is restricted to the characters defined by XML Schema 1.0: `^[\x09\x0A\x0D\x20-퟿-�0000-FFFF]*$`. | prod | aas-core-meta v3.1 `:1230` |
| **AASd-134** | Operation | The `idShort` of all `inputVariable/value`, `outputVariable/value`, and `inoutputVariable/value` is unique. | prod | aas-core-meta v3.1 `:3893` |
| **AASd-135** | AdministrativeInformation.version | `version` has a length of at most 4 characters. | prod; **number unverified for 3.1** | not in aas-core-meta 3.0-3.2; IDTA-01001-3-0 Annex H p.161: New (V3.0 vs. V2.0.1) |
| **AASd-136** | AdministrativeInformation.revision | `revision` has a length of at most 4 characters. | prod; **number unverified for 3.1** | not in aas-core-meta 3.0-3.2; IDTA-01001-3-0 Annex H p.161: New (V3.0 vs. V2.0.1) |

### 3.2 HasKind / Template / Instance

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-008** | OperationVariable.value | The submodel element value of an operation variable is of `kind=Template`. | **removed**: do not check (was `static`) | IDTA-01001-3-0 Annex H p.159: Removed (V3.0 vs. V2.0.1) |
| **AASd-119** | Qualifiable.qualifier | If any `Qualifier/kind` value equals `TemplateQualifier` and the qualified element inherits from HasKind, the qualified element is of `kind=Template`. | prod | aas-core-meta v3.1 `:1919` |
| **AASd-129** | SubmodelElement.qualifier | If any `Qualifier/kind` equals `TemplateQualifier` (inherited via Qualifiable), the submodel element is part of a Submodel of `kind=Template`. | static | aas-core-meta v3.1 `:2537` |
| **AASd-138** | SubmodelElementList | A SubmodelElementList within a Submodel of `kind=Template` or as part of an OperationVariable has exactly one element. | prod | aas-core-meta v3.2 `:2998`; not in v3.1 |

### 3.3 AdministrativeInformation

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-005** | AdministrativeInformation | If `version` is not specified, `revision` is also not specified. A revision requires a version. | prod | aas-core-meta v3.1 `:1841` |

### 3.4 Property / Range / MultiLanguageProperty

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-006** | Qualifier | If both `value` and `valueId` are present, the value is identical to the value of the referenced coded value in `valueId`. | static | aas-core-meta v3.1 `:1992` |
| **AASd-007** | Property | If both `Property/value` and `Property/valueId` are present, `value` is identical to the referenced coded value in `valueId`. | static | aas-core-meta v3.1 `:2958` |
| **AASd-012** | MultiLanguageProperty | If both `value` and `valueId` are present, the meaning is the same for each string in a specific language as the referenced `valueId`. (A langString's non-empty `text` is NOT this constraint: it comes from the schemas' minLength 1; corrected 2026-10-02.) | static | aas-core-meta v3.1 `:3037` |
| **AASd-013** | Range | ⚠️ **REMOVED in V2.0.1 — exists in NO 3.x revision.** Verbatim ("Changes V2.0.1 vs. V2.0", carried in the v3.0, v3.1 AND v3.2 PDFs): «AASd-013 \| Removed \| Constraint AASd-013: In case of a range with kind=Instance either the min or the max value or both need to be defined.» Open-bounds Ranges are VALID in 3.0, 3.1 and 3.2 — do NOT enforce or even warn, on any revision. | removed | not in aas-core-meta 3.0-3.2; IDTA-01001-3-0 Annex H p.204: Removed (V2.0.1 vs. V2.0) |
| **AASd-020** | Qualifier | `Qualifier/value` is consistent with the data type defined in `Qualifier/valueType`. ⚠️ **REFORMULATED from Property in v3.1** (verified vs the PRIMARY source **IDTA-01001-3-1-2 Part 1** §C: the active definition reads «The value of Qualifier/value shall be consistent with the data type as defined in Qualifier/valueType»; the "Property/value" wording survives ONLY in superseded changelogs). Property value↔valueType is NOT a numbered AASd in 3.1.x → cite it internally (e.g. `APP-PROPERTY-VALUE-TYPE`), never as AASd-020. | prod | aas-core-meta v3.1 `:1999` |
| **AASd-021** | Qualifiable | Every qualifiable has at most one Qualifier with the same `Qualifier/type`. | prod | aas-core-meta v3.1 `:1935` |

### 3.5 Entity / AssetInformation

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-014** | Entity | Either `globalAssetId` or `specificAssetId` of an Entity must be set if `Entity/entityType` is set to `SelfManagedEntity`. Otherwise they do not exist. | prod | aas-core-meta v3.1 `:3437` |
| **AASd-023** | AssetInformation | `AssetInformation/globalAssetId` is either a reference to an Asset object or a global reference. | **removed**: do not check (was `static`) | IDTA-01001-3-0 Annex H p.175: Removed (V3.0RC02 vs. V2.0.1) |
| **AASd-116** | SpecificAssetId.name | `globalAssetId` (case-insensitive) is a reserved key for `SpecificAssetId/name` with the semantics defined at `https://admin-shell.io/aas/3/x/AssetInformation/globalAssetId`. | prod | aas-core-meta v3.1 `:2206` |
| **AASd-131** | AssetInformation | `globalAssetId` or at least one `specificAssetId` is defined for AssetInformation. | prod | aas-core-meta v3.1 `:2227` |
| **AASd-133** | SpecificAssetId | `externalSubjectId` is a global reference (Reference/type = GlobalReference). | prod | aas-core-meta v3.1 `:2366` |

### 3.6 References (the largest category — get these right or imports fail)

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-080** | Key (legacy 3.0) | In case `Key/type == GlobalReference`, `idType` must not be a local identifier. | deprecated | IDTA-01001-3-0 Annex H p.191: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-081** | Key (legacy 3.0) | In case `Key/type == AssetAdministrationShell`, identifier constraints apply. | deprecated | IDTA-01001-3-0 Annex H p.191: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-121** | Reference | For References, the value of `Key/type` of the FIRST key of `Reference/keys` is one of GloballyIdentifiables (AssetAdministrationShell, ConceptDescription, GlobalReference, Submodel). | static | aas-core-meta v3.1 `:4530` |
| **AASd-122** | ExternalReference | For external references (`Reference/type=ExternalReference`), the FIRST key's `Key/type` is one of GenericGloballyIdentifiables (GlobalReference). | prod | aas-core-meta v3.1 `:4535` |
| **AASd-123** | ModelReference | For model references (`Reference/type=ModelReference`), the FIRST key's `Key/type` is one of AasIdentifiables. | prod | aas-core-meta v3.1 `:4542` |
| **AASd-124** | ExternalReference | For external references, the LAST key of `Reference/keys` is either one of GenericGloballyIdentifiables or one of GenericFragmentKeys. | prod | aas-core-meta v3.1 `:4549` |
| **AASd-125** | ModelReference | For model references with >1 key, the `Key/type` of each non-first key is one of FragmentKeys. | prod | aas-core-meta v3.1 `:4557` |
| **AASd-126** | ModelReference | For model references with >1 key, the LAST key's `Key/type` may be a GenericFragmentKey, OR no key in the chain has a GenericFragmentKey value. | static | aas-core-meta v3.1 `:4569` |
| **AASd-127** | ModelReference | For model references, a key with `Key/type=FragmentReference` must be preceded by a key with `Key/type=File` or `Blob`. Other AAS fragments do not support fragments. | prod | aas-core-meta v3.1 `:4578` |
| **AASd-128** | ModelReference | For model references, the `Key/value` of a Key preceded by a Key with `Key/type=SubmodelElementList` is an integer index into the list. | prod | aas-core-meta v3.1 `:4594` |
| **AASd-137** | ExternalReference | For external references, the `Key/type` of ANY key in the Reference is NOT one of AasReferables (cannot point at AAS-internal elements from an external reference). | prod | aas-core-meta v3.2 `:4829`; not in v3.1 |

### 3.7 SubmodelElementList (homogeneous list constraints)

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-107** | SubmodelElementList | If a first-level child has a `semanticId`, it is identical to `SubmodelElementList/semanticIdListElement`. | prod | aas-core-meta v3.1 `:2727` |
| **AASd-108** | SubmodelElementList | All first-level children have the same submodel element type as `SubmodelElementList/typeValueListElement`. | prod | aas-core-meta v3.1 `:2744` |
| **AASd-109** | SubmodelElementList | If `typeValueListElement` is `Property` or `Range`, `valueTypeListElement` is set and all children share that value type. **Guarded by the DECLARATION only — see §4** | prod | aas-core-meta v3.1 `:2749` |
| **AASd-114** | SubmodelElementList | If two first-level children have a `semanticId`, they are identical. | prod | aas-core-meta v3.1 `:2733` |
| **AASd-115** | SubmodelElementList | If a child does not specify a `semanticId`, its value is assumed identical to `semanticIdListElement`. | static | aas-core-meta v3.1 `:2738` |

### 3.8 SubmodelElementCollection (heterogeneous bag constraints)

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-026** | SubmodelElementCollection | If `allowDuplicates==false` then the collection does not contain several elements with the same semantics (same `semanticId`). | **removed**: do not check (was `static`) | IDTA-01001-3-0 Annex H p.188: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-092** | SubmodelElementCollection | If `allowDuplicates==false` and the semanticId references a ConceptDescription, that CD's category is `ENTITY`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.191: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-093** | SubmodelElementCollection | If `allowDuplicates==true` and the semanticId references a ConceptDescription, that CD's category is `COLLECTION`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.191: Removed (V3.0RC02 vs. V3.0RC01) |

### 3.9 ConceptDescription / IEC 61360 (categories + semanticId consistency)

These need ConceptDescription resolution to verify (context-dependent).
All sourced verbatim from IDTA-01001 v3.2.

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-050** | ConceptDescription | If DataSpecificationIEC61360 is used, `hasDataSpecification/dataSpecification` contains the global reference to `http://admin-shell.io/DataSpecificationTemplates/DataSpecificationIEC61360/2/0`. | context; **number unverified for 3.1** | not in aas-core-meta 3.0-3.2; IDTA-01001-3-0 Annex H p.188: Update (V3.0RC02 vs. V3.0RC01) |
| **AASd-051** | ConceptDescription | A ConceptDescription has one of: VALUE, PROPERTY, REFERENCE, DOCUMENT, CAPABILITY, RELATIONSHIP, COLLECTION, FUNCTION, EVENT, ENTITY, APPLICATION_CLASS, QUALIFIER, VIEW. Default: PROPERTY. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.168: Removed (V3.0 vs. V3.0RC02) |
| **AASd-053** | Range | If `semanticId` references a CD, the CD's category is `PROPERTY`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.188: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-054** | ReferenceElement | If `semanticId` references a CD, the CD's category is `REFERENCE`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.189: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-055** | RelationshipElement | If `semanticId` references a CD, the CD's category is `RELATIONSHIP`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.189: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-056** | Entity | If `semanticId` references a CD, the CD's category is `ENTITY`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.189: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-057** | File / Blob | `semanticId` references only a CD with category `DOCUMENT`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.189: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-058** | Capability | `semanticId` references only a CD with category `CAPABILITY`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.189: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-059** | SubmodelElementCollection | If `semanticId` references a CD, the CD's category is `COLLECTION` or `ENTITY`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.189: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-060** | Operation | If `semanticId` references a CD, the CD's category is `FUNCTION`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.189: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-061** | Event | If `semanticId` references a CD, the CD's category is `EVENT`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.189: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-062** | Property | If `semanticId` references a CD, the CD's category is `APPLICATION_CLASS`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.189: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-063** | Qualifier | If `semanticId` references a CD, the CD's category is `QUALIFIER`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.190: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-064** | View (deprecated 3.x) | If `semanticId` references a CD, the CD's category is `VIEW`. | deprecated | IDTA-01001-3-0 Annex H p.190: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-065** | Property/MLP + VALUE | If the CD's category is VALUE, the property `value`/`valueId` is identical to `DataSpecificationIEC61360/value`/`valueId`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.190: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-066** | Property/MLP + PROPERTY+valueList | If the CD's category is PROPERTY and a valueList is defined, the property's value matches one of the `valueReferencePair` entries. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.190: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-067** | MultiLanguageProperty | If `semanticId` references a CD, `DataSpecificationIEC61360/dataType` is `STRING_TRANSLATABLE`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.190: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-068** | Range | If `semanticId` references a CD, `DataSpecificationIEC61360/dataType` is a numerical one (`REAL_*` or `RATIONAL_*`). | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.190: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-069** | Range | If `semanticId` references a CD, `DataSpecificationIEC61360/levelType` is identical to the set `{Min, Max}`. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.190: Removed (V3.0RC02 vs. V3.0RC01) |
| **AASd-070** | CD category=PROPERTY | Specific IEC61360 conformance requirements apply. See spec §C.1 for detail. | **renamed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.190: Renamed (V3.0RC02 vs. V3.0RC01) |
| **AASd-071** | CD category=VALUE | Specific IEC61360 conformance requirements apply. See spec §C.1 for detail. | **renamed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.190: Renamed (V3.0RC02 vs. V3.0RC01) |
| **AASd-072** | CD category=DOCUMENT | Specific IEC61360 conformance requirements apply. See spec §C.1 for detail. | **renamed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.190: Renamed (V3.0RC02 vs. V3.0RC01) |
| **AASd-073** | CD category=QUALIFIER | Specific IEC61360 conformance requirements apply. See spec §C.1 for detail. | **renamed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.191: Renamed (V3.0RC02 vs. V3.0RC01) |
| **AASd-074** | CD all categories | Generic IEC61360 conformance requirements apply. See spec §C.1 for detail. | **renamed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.191: Renamed (V3.0RC02 vs. V3.0RC01) |
| **AASd-075** | CD using DataSpec | Generic data-spec conformance requirements apply. See spec §C.1 for detail. | **removed**: do not check (was `context`) | IDTA-01001-3-0 Annex H p.191: Removed (V3.0RC02 vs. V3.0RC01) |

### 3.9a IEC 61360 data-spec CONTENT constraints (AASc-3a-*) — verified 2026-08-06

§3.9 covers the AASd-* *category* rules. The **content** of a
`DataSpecificationIec61360` has its own family, **AASc-3a-***, which
`aas-test-engines check_aasx_file` DOES enforce (empirically confirmed while
generating ConceptDescriptions for a real DPP — a naive generator trips both):

| ID | Observed rule | Practical authoring rule |
|---|---|---|
| **AASc-3a-008** | A `DataSpecificationIec61360` with **no `definition`** (or none in English) is flagged invalid (`"definition is missing"`). **Exception in the rule text (IDTA-01003-a p.39): a CD that describes a value, i.e. whose `value` is set, needs no definition**; the engine skips those too. | Emit the IEC61360 block ONLY where you have a real definition; otherwise a **bare** ConceptDescription (`id` + optional `displayName`, no data-spec) is valid + honest. **Never fabricate a definition** to satisfy the rule. |
| **AASc-3a-010** | `value` and `valueList` both set (`"value and value_list cannot be set simultaneously"`). Both empty is legal. | A CD describes either a single value or a value list, never both. NOT a language rule. |
| **AASc-3a-009** | If `dataType` is a **measure/currency** type (`REAL_MEASURE`, `INTEGER_MEASURE`, `RATIONAL_MEASURE`, `*_CURRENCY`), a `unit`/`unitId` is **mandatory** (`"neither unit nor unit_id is set"`). | With no unit in the source, do NOT assert a measure `dataType`. Emit `dataType` only for unit-free types (STRING, IRI, BOOLEAN, DATE, TIMESTAMP, `*_COUNT`), else omit it. **Never invent a unit.** |
| **AASc-3a-002** | Verbatim (aas-core-meta v3.1 `:5580`, docstring of `preferred_name`): ":attr:`preferred_name` shall be provided at least in English." | Every IEC 61360 block carries an English `preferredName`. Do not translate a German one by guesswork; report it. |

**The dataSpecification reference IRI (the #1 papercut) — settled by Part 3a v3.1.1.**
AASc-3a-050 in the official Part 3a v3.1.1 PDF (p.40; `idta-specs:txt/IDTA-01003-a-3-1-1_…txt`):
*"…shall contain the external reference to the IRI of the corresponding data specification
template `https://admin-shell.io/DataSpecificationTemplates/DataSpecificationIec61360/3`."* Its
template table (p.16) marks `…/DataSpecificationIec61360/3/0` and `…/DataSpecificationIEC61360/3/0`
(http and https) as *"<<deprecated>>"*; the switch happened in V3.0.2 (change table p.67). aas-core-meta
still carries the older `…/DataSpecificationIEC61360/3/0` (v3_0.py:5113, v3_1.py:5053-5059,
v3_2.py:5373), which is why the engine and the formalisation disagree. Verdict: **emit `/3`**; a
`/3/0` reference is **deprecated, not invalid** (report as a warning, never as an AASc-3a-050
error). Whether an embedded IEC 61360 block may sit on a submodel element: yes, as a "may"
fallback (Part 1 v3.1.2 p.40: *"Submodel elements may also have defined data specification
templates. A template might be defined to mirror some of the attributes like preferredName and
unit of a property concept definition if there is no corresponding concept description
available."*); see [[iec61360]]. Only the legacy
`…/DataSpecificationIEC61360/2/0` in the AASd-050 row above is the 2.0 form.

### 3.10 Submodel + supplemental semantic ID

| ID | Class | Constraint | Status | Source (audited 2026-09-15) |
|---|---|---|---|---|
| **AASd-090** | DataElement | For DataElements, `category` shall be one of CONSTANT, PARAMETER, VARIABLE (default VARIABLE). ⚠️ **AAS 3.0 ONLY — introduced in V3.0, REMOVED in 3.1.** Verbatim ("Changes V3.1 vs. V3.0.2"): «• REMOVED: remove AASd-090: category is deprecated (#514)». Enforce it on a 3.0 document; on 3.1+ the enum is gone (`category` is deprecated) and flagging it is a **false invalid**. | 3.0 only | IDTA-01001-3-0 p.69; removal: IDTA-01001-3-1-2 p.196 + p.199; aas-core-meta v3.0 `:2951`; absent from v3.1 |
| **AASd-118** | HasSemantics | If `supplementalSemanticId` is defined, a main `semanticId` is also defined. | prod | aas-core-meta v3.1 `:1463` |

**AASd-118 presence: a semanticId whose keys are all blank is NOT a semanticId**. Clearing an editor's Semantic ID field can leave
`{keys:[{value:""}]}`; a validator that counts `keys.length > 0` as "has a semanticId" stays clean,
while serializers that drop the blank key ship `supplementalSemanticIds` with NO
`semanticId`, a package that breaks AASd-118. Judge presence by what ships: at least one key, in any
of the three key shapes, whose value is not blank; clearing the field should delete the `semanticId`.

- The official 3.1 XSD (bundled `AAS_3_1.xsd`) has **no `xs:whiteSpace` facet** anywhere. Its string
  restrictions are `xs:string` with **`minLength 1`** (plus maxLength). `xs:string` preserves
  whitespace (XML Schema Part 2), so `"   "` (length 3) satisfies minLength 1, and `" X"` and `"X"`
  are two different values. No facet asks a reader to trim.
- Measured with `xmllint --schema AAS_3_1.xsd`, one field at a time set to `"   "` in an otherwise
  valid environment:

  | result | fields |
  |---|---|
  | **accepted** | Submodel `id`, Property `value`, langString `text`, Reference Key `value`, Extension `name` |
  | rejected by an **enumeration** | Property `valueType`, Key `type`, Submodel `kind` (a padded `" Template"` too) |
  | rejected by a **pattern** | `idShort`, langString `language`, File `value`, File `contentType`, administration `version` |

- The same two facets, read from the XSD, cover the other enumerated types (`dataTypeIec61360_t`,
  `assetKind_t`, `entityType_t`, `direction_t`, `stateOfEvent_t`, `qualifierKind_t`,
  `referenceTypes_t`, `aasSubmodelElements_t` for `typeValueListElement`) and the other patterned
  fields (administration `revision`, BasicEventElement `lastUpdate` / `minInterval` / `maxInterval`,
  EventPayload `timeStamp`, Blob and Resource `contentType`, Resource `path`).
- Why it bites: an editor whose two serializers apply separate per-field whitespace rules can ship
  one package with a valid part and an invalid one (e.g. a qualifier `valueType` of `"   "` shipped as
  `<valueType>   </valueType>` in the XML part, which fails the XSD enumeration, and as `xs:string` in
  the JSON part).

### langString per-language uniqueness — the DEFINITIVE rule (verified 2026-07-22)

**The question**: is a langString set (a `description` / `displayName` /
IEC61360 field) that repeats the SAME language more than once — e.g. a
`description` with three `en` entries — valid?

**The absolute answer depends ENTIRELY on WHERE the langString sits. Do not
apply one blanket rule.**

| langString location | Same-language repeated is… | Normative basis |
|---|---|---|
| Element **`description`** (`langStringTextType`) | **VALID** — not a violation | XSD `maxOccurs="unbounded"`, no uniqueness; no AASd/AASc constraint |
| Element **`displayName`** (`langStringNameType`) | **VALID** — not a violation | same as above |
| MLP **`value`** (`langStringTextType`) | **VALID** — not a violation | same as above |
| **IEC61360** ConceptDescription fields — `preferredName` / `shortName` / `definition` | **VALID** — not a numbered violation; a data-quality WARNING | no AASc number (see the correction below); suggested internal code `iec61360-language-repeated` |

**Grounding (triple-checked on the `OAS_Mixer_test1.aasx` case, 2026-07-22):**
1. **Official XSD** (`public/aas-3.1.xsd`, `xmllint --schema`): a `description`
   with 3 `en` entries → **validates, 0 errors**. `langStringTextType` is
   `minOccurs="1" maxOccurs="unbounded"` with **no** uniqueness key.
2. **Official JSON schema** (Draft 2019-09): **0 errors**.
3. **Metamodel catalogue** (IDTA-01001-3-1-2): no numbered per-language
   uniqueness constraint. **AASd-012 is about MultiLanguageProperty value ↔ valueId
   having the same meaning, NOT uniqueness** (aas-core-meta v3_1.py:3037-3040).
4. **CORRECTED 2026-09-14: AASc-3a-010 is NOT a uniqueness rule.** Its text, in
   IDTA-01003-a v3.0 p.22 (renumbered for Part 3a in the p.64 change log): "If
   DataSpecificationIec61360/value is not empty, DataSpecificationIec61360/valueList
   shall be empty, and vice versa." `aas-test-engines` 1.0.3 implements exactly
   that ("value and value_list cannot be set simultaneously") and has no language
   uniqueness check at all. This skill previously cited AASc-3a-010 for a repeated
   IEC61360 language.
5. **aas-core-meta v3.1** carries unnumbered invariants "… must specify unique
   languages" on EVERY langString set (displayName, description, MLP value,
   IEC61360 preferredName/shortName/definition). The helper is decorated
   `@verification @implementation_specific`: an SDK verification, not a numbered
   constraint and not a schema facet. An aas-core based verifier WILL flag a
   repeated language anywhere, which is why a data-quality warning is worth
   emitting, and why it must never be reported as INVALID.
   An internal `lang-string` code for a plain `description` must be
   explicitly filed **"NOT spec"** (see §3 intro, the "deliberately-internal
   non-AASd codes").

**Therefore — the correct validator behaviour (apply IDENTICALLY in every
validator):**

- A repeated language in `description` / `displayName` / MLP `value` is **NOT a
  schema violation and NOT an AASd/AASc violation.** At most surface a
  **non-blocking, informational data-quality WARNING** ("a reader picks one
  entry arbitrarily; consider merging") — with a **non-schema** code. **Never**
  categorise it `XML_SCHEMA`, never say "doesn't conform to the AAS 3.1 schema",
  never let it block export/"Validation failed".
- A repeated language in an **IEC61360 ConceptDescription field** → the same:
  a data-quality WARNING with a non-numbered code. It is NOT AASc-3a-010.
- **AASc-3a-010 proper** (value and valueList both set) IS normative: report it.

**Anti-drift / reconciliation invariant**: a file that PASSES the official XSD
must never be reported by any surface of the same product as an `XML_SCHEMA`
error. If the list badge says VALID and the editor says "6 XSD ERRORS" for the
same file, the editor is wrong — the two validation surfaces MUST agree (this is
the divergent-validation-contract bug class). The honesty bar applies to
validators too: only call something a schema violation when the official schema
actually rejects it.

### AASd-013 — Range bounds — ⛔ DO NOT IMPLEMENT

**This rule was REMOVED in metamodel V2.0.1 and exists in no 3.x revision.** A
`<range>` with both `<min>` and `<max>` empty is **VALID** in 3.0, 3.1 and 3.2 —
which is exactly what you want for an extracted range where the datasheet gave
only one bound, or neither.

Do not enforce it, do not warn on it, and do not "auto-fix" by deleting the
Range: that silently destroys user data to satisfy a rule the specification does
not have. If you find AASd-013 in a validator, it is a bug producing false
"invalid" verdicts on conformant files.

What IS still checkable on a Range: that `min`/`max` parse against `valueType`
(cite `value-type`), and that a numeric `min` is not greater than `max` (cite
`range-order` — an internal code, **not** AASd-013).

### AASd-014 — Entity globalAssetId or specificAssetId

**Pattern**: an Entity with `entityType=SelfManagedEntity` and no
`globalAssetId`/`specificAssetId` set.

**Fix recipe**:
- If you can derive a globalAssetId from context (e.g., the entity is a
  sub-component of a known asset), insert it.
- Otherwise change `entityType` to `CoManagedEntity` (which doesn't
  require an asset id), OR remove the Entity element.

### Property value ↔ valueType conformance (internal `APP-PROPERTY-VALUE-TYPE`, NOT AASd-020)

> ⚠️ In v3.1.x **AASd-020 is the Qualifier constraint** (Qualifier/value ↔
> Qualifier/valueType — see the catalogue row). A **Property** value/valueType
> mismatch is the SAME typing principle but has NO numbered AASd in 3.1.x, so cite
> it internally (`APP-PROPERTY-VALUE-TYPE`), never as AASd-020. The Qualifier
> variant IS cited `AASd-020`. The fix recipe below applies to both.

**Pattern**: `<value>abc</value>` with `valueType=xs:int` (the string
doesn't parse as int).

**Typical failure**: extraction guessed the valueType wrong, or the
datasheet had a value like "10 kg" with units inlined.

**Fix recipe (auto when safe)**:
1. Try to parse the value as the declared type. If it parses: keep.
2. If not: infer the actual type from the value content (number → xs:int /
   xs:double; ISO date → xs:date; URL → xs:anyURI; etc.) and replace
   `valueType`.
3. If the value has trailing units (`"10 kg"` → `xs:int`), strip the unit
   to a separate `unit` field if the parent element supports one.

**Common confusion**: `xs:integer` ≠ `xs:int`. `xs:integer` is unbounded,
`xs:int` is 32-bit signed. The XSD catches this as type-conformance fail,
not AASd.

### AASd-119 / AASd-129 — TemplateQualifier kind alignment

**Pattern**: a SubmodelElement has a Qualifier with `kind=TemplateQualifier`
but the containing Submodel has `kind=Instance` (or vice versa).

**Typical failure**: importing a vendor template into an instance flow
without rebadging the kind.

**Fix recipe**:
- If the file was MEANT to be a template (i.e. it's the definition of a
  product family, not a unit): set `Submodel/kind=Template`.
- If MEANT to be an instance (a specific product unit): remove the
  TemplateQualifier-kind qualifiers.

This is a semantic choice — do NOT auto-fix without user confirmation.

#### The `kind` split is what decides whether a qualifier SHIPS (measured 2026-09-01)

"Template qualifiers are stripped from instances" is **half true**, and the half
that is wrong will mislead a design decision. Counted over the 61 catalogue
templates, on the **7401** `SMT/Cardinality` qualifiers:

| `kind` | count | at export from an Instance |
|---|---:|---|
| `TemplateQualifier` | 3583 (48%) | **stripped** |
| `ConceptQualifier` | 2290 (31%) | **ships** |
| *(absent)* | 1528 (21%) | **ships** |

So **52% of cardinality qualifiers survive into the instance**. Key any rule on
the qualifier's own `kind`/provenance, never on "it is a cardinality qualifier".
(The blanket version has been asserted before and had to be corrected the same
day — the measurement is cheap, do it before asserting.)

Measured `SMT/Cardinality` values across the same corpus: `One` 2398 ·
`ZeroToOne` 4081 · `ZeroToMany` 691 · `OneToMany` 211, **plus 13 IDTA typos and
7 off-list values**. A closed dropdown over the four legal values is therefore
right for AUTHORING, but a reader must tolerate the 20 malformed ones rather
than reject the template.

#### Ground truth: which catalogue templates ship IDTA-authored defects

Measured on the newest version of each of the 61 templates (2026-08-31 → 09-01):

- **DEXPI** — 48 × AASd-121 (ModelReference first key not a GloballyIdentifiable).
- **MaintenanceInstructions** — 1 × AASd-022 (duplicate idShort in one container).
- **AASc-3a-008** — **0 occurrences**. An earlier claim of "112" was counted over
  *all* versions including superseded ones; on current versions it is zero.
- Everything else is clean.

Two templates out of 61 means a defect report against a stock template is
*usually* our bug, not IDTA's — check this list before blaming the source.

### AASd-121 / AASd-122 / AASd-123 — Reference shape

**Pattern**: a Reference's first Key has the wrong type for the reference
class.

```xml
<!-- WRONG: ExternalReference with first key=Submodel -->
<reference>
  <type>ExternalReference</type>
  <keys>
    <key><type>Submodel</type><value>urn:foo</value></key>
  </keys>
</reference>

<!-- RIGHT: ExternalReference with first key=GlobalReference -->
<reference>
  <type>ExternalReference</type>
  <keys>
    <key><type>GlobalReference</type><value>urn:foo</value></key>
  </keys>
</reference>
```

**Fix recipe (auto when intent is clear)**:
- If `type=ExternalReference`: first key's type → `GlobalReference`.
- If `type=ModelReference`: first key's type → one of
  `AssetAdministrationShell`, `Submodel`, `ConceptDescription`,
  `Identifiable`.

### AASd-131 — AssetInformation needs an asset id

**Pattern**: `<assetInformation>` block without `<globalAssetId>` or
`<specificAssetId>`.

**Fix recipe (auto)**:
- Derive `globalAssetId` from the AAS's `id` URN if no other source.
- Specifically for Battery Passport: pull from the serial number;
  pattern `urn:battery:<manufacturer>:<serial>`.

### AASd-107 / AASd-108 / AASd-109 — SubmodelElementList consistency

**Pattern**: SML with mixed child types or mixed semanticIds.

**Fix recipe**:
- If the SML was misclassified (the elements are heterogeneous), convert
  to SMC.
- If genuinely homogeneous but the consistency declaration is missing,
  set `typeValueListElement` from the first child's type, then validate
  all children.

#### ⚠️ AASd-107 applies ONLY when `semanticIdListElement` is DECLARED (settled 2026-09-01)

Verbatim: *"If a first level child element in a SubmodelElementList has a
semanticId **it shall be identical to** SubmodelElementList/semanticIdListElement."*
The comparison target is **0..1**. When the list declares nothing there is
nothing to be identical to, so **the rule does not fire** — children carrying a
semanticId under an undeclared list are CONFORMANT. This is how aas-core
implements it (`if semantic_id_list_element is not None: …`) (the AASd-107
branch only runs when the list declares one; the no-declaration branch falls through to
**AASd-114**, "any two children that both carry a semanticId must agree").

Do **not** invent the inverse rule ("children have one, the list doesn't →
AASd-107"). It flags conformant IDTA templates: the published **Handover
Documentation 2.0.1** ships `DocumentVersion/Language` as an SML whose child
carries `0173-1#02-AAN468#008` with **no** `semanticIdListElement` — verified
live 2026-09-01. A UI hint written that way made the inspector warn while
Validate passed on the same document: two verdicts for one file, which is the
failure §1b exists to prevent. If a hint and the gate disagree, the **gate** is
the verdict and the hint is the bug.

#### ⚠️ AASd-109 is guarded by the DECLARATION, never by the children's type (settled 2026-09-18)

Verbatim (aas-core-meta v3.1, the `Submodel_element_list` invariant and the class docstring's
`:constraint AASd-109:`): *"If type value list element is equal to Property or Range value type
list element shall be set and all first level child elements shall have the value type as
specified in value type list element."* The guard is `type_value_list_element == Property or
Range`. A list that DECLARES `SubmodelElement` and holds Property children is therefore outside
the rule, however tempting the children look — and it does not violate AASd-108 either, because
`submodel_element_is_of_type(element, SubmodelElement)` is satisfied by any submodel element.

Adjudicated with the reference implementation, `aas-core3.1` 1.0.0 (PyPI), `verification.verify`:

| document | verdict |
|---|---|
| `typeValueListElement=SubmodelElement`, Property children, no `valueTypeListElement` | **0 errors** |
| `typeValueListElement=Property`, no `valueTypeListElement` | 1 error, AASd-109 |
| `typeValueListElement=Property`, `valueTypeListElement=xs:string` | 0 errors |

A validator that ORs the declaration with the children's runtime type gives imported vendor lists
of the first shape a BLOCKING AASd-109 error. Same failure mode as the AASd-107 inverse
above: an invented guard that flags conformant documents. When a tool and this table disagree,
check the invariant's guard before the prose.

### AASd-134 — Operation variable idShort uniqueness

**Pattern**: an Operation has two `inputVariable`s with the same
`idShort` (or in/out collision).

**Fix recipe (auto)**:
- Suffix duplicates with the variable role: `Voltage_in`, `Voltage_out`.

---

## 5. The auto-fix vs flag philosophy

Production rule: **only
auto-fix what is syntactically determined by the spec and semantically
neutral**.

| Category | Auto-fix? | Why |
|---|---|---|
| Namespace upgrade (3/0 → 3/1) | YES | Mechanical, lossless. |
| idShort sanitisation within the pattern | YES | Deterministic, reversible. |
| Empty container removal (qualifiers, statements, extensions) | YES | The empty container is invalid by itself. |
| langString missing language → "en" | YES | Better-default; user can override. |
| langString empty text → placeholder | YES | The placeholder is recognisably "needs review". |
| `<key>` attributes → child elements | YES | Wire-format error, not intent error. |
| `globalAssetId` keys-shape → simple string | YES | The keys structure was never valid; we're recovering intent. |
| Range with one bound (set the other) | NO | Guessing a value invents data. |
| Property empty value (fill placeholder) | DEPENDS | Placeholder OK for `value`; never for compliance-bearing fields like `PCFCO2eq`. |
| valueType mismatch (re-type the field) | NO | Could lose information; surface to user. |
| Instance vs Template kind decision | NO | Semantic choice the user made. |
| Inventing semanticId / IRDI | NEVER | Hallucinated IRDIs corrupt the audit trail. |
| Inserting EPD / PCF numbers | NEVER | Verified-only is the compliance discipline. |

The right framing: a fix is auto-safe when **a domain expert reviewing
the diff would say "yes, that's what they meant"**. Otherwise it's a
guess, and the right move is to flag.

---

## 6. Reading aas-test-engines output

The IDTA's `aas-test-engines` runs both metamodel constraints AND IDTA
submodel template conformance. Its output is structured JSON per test
case:

```json
{
  "test_case": "constraint_AASd_002",
  "level": "error",
  "path": "AssetAdministrationShells[0].submodels[0].submodelElements[3]",
  "message": "idShort 'Manufacturer-Name-' violates pattern (ends with hyphen)",
  "context": { "expected": "regex match", "actual": "Manufacturer-Name-" }
}
```

Reading patterns:
- **`level`**: `error` blocks pass, `warning` is informative, `info` is
  context.
- **`path`**: model path (not XML path). Translate to XML coordinates
  using your serialiser when surfacing to the user.
- **`test_case`**: maps 1:1 with constraints in §3 OR with template-
  specific checks (e.g., `nameplate_v3_required_elements`).

**The two failure flavours:**
1. **Constraint failures** — one of the AASd-* rules in §3. Map to the
   table for the fix.
2. **Template instance failures** — the file claims to be a Nameplate
   submodel (semanticId resolves to the IDTA Nameplate IRI) but is
   missing required elements per the IDTA-02006 template. Fix is
   submodel-specific (see `aas-knowledge` §3 for the IDTA template
   catalogue).

**⚠️ API gotcha — the file entry points differ on constraints (verified 2026-08-06):**
`check_json_file` / `check_json_data` run **schema/parse ONLY and SKIP the AASd-*/AASc-***
layer — they emit a quiet `"Skipped checking of constraints"` and will call a
constraint-VIOLATING document "valid". `check_aasx_file` / `check_aasx_data` run the
**FULL** check (schema + constraints). To get a constraint verdict on a bare `.json`,
package it into an `.aasx` and use `check_aasx_file`, or call `check_constraints(obj, …)`
yourself on the parsed object. **Reporting a JSON "valid" off `check_json_file` alone is a
false pass — it was never constraint-checked** (this is how an open-bounds-Range /
missing-`valueTypeListElement` file slips through a JSON-only gate).

**If aas-test-engines and your local validator disagree:** aas-test-engines
is authoritative. Either:
- Your local validator has a bug → fix the validator.
- Your test case is a corner the spec genuinely didn't address → file
  an issue against IDTA, document the divergence, do not auto-fix.

---

## 7. Validation in CI/CD

Patterns proven in production CI:

### Per-rule fixtures

For every rule in §3 you implement: a pair of fixture files in your
test corpus.

```
test-fixtures/aasd/
├── aasd-002-violates.xml   (file that fails AASd-002)
├── aasd-002-passes.xml     (the same fixture corrected)
├── aasd-119-violates.xml
├── aasd-119-passes.xml
…
```

Tests assert:
- `validate(violates)` → `valid: false`, errors include the rule ID.
- `validate(passes)` → `valid: true`.
- `fix(violates)` → output equals `passes` (golden snapshot).

### Golden AASX round-trip

Every released AASX template gets a snapshot test:

```
1. Load template.aasx
2. Extract -> parse -> re-export -> repackage as roundtrip.aasx
3. Compare roundtrip.aasx ↔ template.aasx (canonical XML diff)
4. Diff is empty OR documented in a CHANGES.md
```

Drift here means the serialiser has a regression. Block the PR.

### Independent conformance gate

Run `aas-test-engines` on every PR over a fixture set (12-30 files
covering each IDTA submodel template). The job fails the build on any
error-level finding. Run it on a cron too (monthly) over a wider corpus
so spec evolution surfaces.

### Performance budget

The full pipeline (XSD + AASd + IDTA engine + IDTA-02035 template check)
should run < 500ms for a typical Battery Passport file (~50 KB).
> 2s = something is regressing.

---

## 8. Pitfalls and non-obvious rules

- **A cardinality counts occurrences, not values.** IDTA 02010-1-0 p.19: *"0…1:
  optional; 1: mandatory 1 entry; 1…n: mandatory 1 to many entries; 0…n: optional
  to many entries"*. "Required but empty" (a mandatory element with no value) is a
  team/product rule, not an IDTA one. Say so.
- **JSON and PDF can disagree on a cardinality** (127 elements over 103 template
  versions as of 2026-09-17; see `aas-template-registry` for current counts). Both are official and IDTA states no precedence.
  Applying the less strict of the two is a product decision, not an IDTA rule. Look the element up in
  `aas-template-registry` before calling an empty element a violation.
- **An unused optional part requires nothing inside it** (a product decision, not an IDTA rule):
  a child's cardinality applies within an instance of its parent, and an optional
  parent the user never filled has no instance. The same holds for an unused item of a
  SubmodelElementList (a template's exemplar item). Apply it to EVERY producer of a
  "required" finding.
- **Template defects are inherited, not the user's.** Some published templates
  ship AASd violations (DEXPI 48 × AASd-121). Report them as inherited
  ("Schema valid, normative violations found"), never as blocking errors of the
  user; a violation the user introduces still blocks.
- **Non-BMP characters and JSON-schema validators.** A validator compiling patterns
  with the JavaScript `u` flag rejects emoji and other characters above U+FFFF with
  the official surrogate-pair XML string pattern. aas-core-meta (AASd-130) defines
  the allowed set by code point, so the rejection is a false positive: rewrite the
  pattern to `\u{10000}-\u{10FFFF}` rather than accepting the finding.

- **Order matters.** Always run XSD first, then AASd, then IDTA engine.
  An earlier-stage failure masks later ones.
- **Don't report `valid: true` after one stage.** Use the tri-state
  `structural | semantic | full` from §1 so the consumer knows how far
  you got.
- **Auto-fix then re-validate.** It is shockingly common to fix one
  rule and break another (e.g., empty-container removal makes the parent
  fail because the container was the only required child). Re-run the
  full pipeline post-fix.
- **Two validators is one validator.** Diverging local + IDTA outputs is
  not a "consensus" — IDTA wins. Treat your local as a fast pre-check.
- **A constraint's wording in v3.x may differ from v2.x.** Some renames
  + clarifications happened (e.g., AASd-118 was added in 3.x). Always
  cite the spec version when reporting.
- **The XSD doesn't validate semantics.** It is wholly possible to have
  an XSD-valid AAS that fails 8 AASd rules. Don't ship a public API
  that returns `valid` after only XSD.
- **`xs:integer` vs `xs:int`.** Common confusion. `xs:integer` is
  unbounded; `xs:int` is 32-bit signed. Different rules apply.
- **`<File>` content-type must be a real MIME.** `application/pdf`, not
  `pdf` or `application/x-pdf`. Goes through xs:string but
  documentation-rule checks the MIME against `^[-\w.]+/[-\w.+]+$`.
- **TemplateQualifier rules cascade.** AASd-119 + AASd-129 + AASd-138
  all enforce different facets of the Template/Instance dichotomy. Get
  one right, the others usually fall into place; ignore one, the others
  fail too.
- **Reference chain rules are 7-deep.** AASd-121 through AASd-128 cover
  reference key chains. The fix is almost always "what did they mean"
  rather than "syntactic transform". Don't blindly rewrite.
- **Removed constraints don't go away in tooling.** Old validators emit
  AASd-052 / AASd-076 / AASd-101 etc. Update your tooling, do NOT add
  fixes for these to your repair logic.
- **Auto-repair is a content liability.** If your `/v1/fix` mutates a
  Property value to an arbitrary placeholder ("—"), the user's exported
  AAS now contains a fact they didn't intend. Tag every auto-edit with
  `tier: low` + a `repair_provenance` note so audit reviewers can spot
  generated content.

---

## 9. Authoritative references

- **IDTA-01001 Part 1 Metamodel v3.2 (THE SOURCE FOR §3):**
  [industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.2/](https://industrialdigitaltwin.io/aas-specifications/IDTA-01001/v3.2/)
  — §C.1 contains the canonical constraint catalogue. Cite this PDF +
  exact section in any disagreement.
- **`aas-test-engines`** (the IDTA reference implementation):
  [github.com/admin-shell-io/aas-test-engines](https://github.com/admin-shell-io/aas-test-engines)
  — install via `pip install aas-test-engines`. Run with
  `aas_test_engines check_aasx your.aasx`.
- **IDTA-01005 Package File Format (AASX)** v3.1: for understanding the
  .aasx ZIP structure (OPC package format, content-types, relationships).
- **IDTA index page** (all parts + submodel templates):
  [industrialdigitaltwin.io/aas-specifications/index/home/index.html](https://industrialdigitaltwin.io/aas-specifications/index/home/index.html)

---

## 10. DPP / Battery-passport value-list & cardinality validation (regulatory layer)

Beyond the metamodel (AASd-*) gate, a DPP / battery file must satisfy **regulatory**
value-list, cardinality and completeness rules. These are **NOT** in IDTA-01001 —
they come from the IDTA / BatteryPass **SAMM models** + EU **2023/1542 Annex XIII**.
Implement as a **separate gate** and
report distinctly from AASd-* — a value-list miss is a *regulatory* finding, not a
metamodel violation. Source: SAMM TTLs (`admin-shell-io/smt-semantic-models`,
`batterypass/BatteryPassDataModel`), verified 2026-06-26. Legal field list + full
URNs: [[dpp-aas-compliance]] §8.

### 10.1 Enforceable enums (validate as CLOSED lists — unknown value = error)

| Field | Closed value set | Source URN |
|---|---|---|
| `granularity` (DppMetadata) | `Model` `Batch` `Item` | `…idta.dpp.dpp_metadata:1.0.0#GranularityEnum` |
| battery `status` / lifecycle | `original` `repurposed` `re-used` `remanufactured` `waste` | `…batterypass.digital_nameplate:1.0.0#BatteryStatusEnumeration` |
| `batteryCategory` | `lmt` `ev` `industrial` `stationary` | `…batterypass.technical_data:1.0.1#BatteryCategoryEnum` |
| `hazardousSubstanceClass` | `AcuteToxicity` `SkinCorrosionOrIrritation` `EyeDamageOrIrritation` | `…batterypass.material_composition:1.0.1#HazardousSubstanceClassEnum` |
| `recycledMaterial` | `Cobalt` `Nickel` `Lithium` `Lead` | `…batterypass.circularity:1.0.0#RecycledMaterial` (⚠ source TTL lists each twice → dedupe) |
| carbon-footprint `lifeCyclePhase` | EN-15978 codes `A1`,`A1-A3`,`A2`,`A3`,`A4`,`A4-A5`,`A5`,`B1…B7`,`C1…C4`,`D` | `…idta.carbon_footprint:1.0.0#LifeCyclePhaseEnum` |

### 10.2 ⚠ NOT enums — do NOT validate as closed lists (would be a false positive)

- **`ExtinguishingAgent`** — free-text `xs:string` (`samm-c:List`). The "A/B/C/D/K" classes are prose, not a model enum.
- **`PcfCalculationMethod`** (IDTA `carbon_footprint`) — free-text `xs:string` (IRDI `0173-1#02-ABG854#003`). ECLASS `0173-1#09-AAO115#003` gives a *recommended* list → treat unknown values as **advisory**, not errors.
- **Casing trap:** the BatteryPass consortium repo (`io.BatteryPass.*`) uses `Original/Repurposed/Reused/Remanufactured/Waste` (capitalised, no hyphen) while IDTA uses the lowercase/hyphenated form in 10.1. Validate IDTA-conformant files against the **IDTA** literals — don't reject `re-used` as invalid.

### 10.3 Cardinality / datatype rules (DppMetadata + battery)

- **DppMetadata:** `facilityId` + `contentSpecificationIds` are **optional**; the other 7 (`digitalProductPassportId`, `uniqueProductIdentifier`, `granularity`, `dppSchemaVersion`, `dppStatus`, `lastUpdate`, `economicOperatorId`) are **mandatory** — flag any missing. `lastUpdate` → `xs:dateTime` (the Property value must be consistent with its valueType — an unnumbered invariant, aas-core-meta v3_1.py:2950; AASd-020 is the Qualifier rule, v3_1.py:1979-1987).
- **MaterialComposition:** `hazardousSubstanceName` + `hazardousSubstanceIdentifier` mandatory; CAS number must match `^\d{2,7}-\d{2}-\d{1}$`; concentration `xs:double`.
- **Circularity** recycled-content shares: `xs:float`, range **0–100** (a `preConsumerShare`/`postConsumerShare` outside 0–100 is a regulatory error — reuse the `range-order` machinery).
- **ProductCondition** mandatory leaves: `numberOfFullCycles`, `informationOnAccidents`, `temperatureInformation`, `stateOfCharge`.

### 10.4 Field-completeness gate (per battery category)

Completeness is **category-sensitive** — validate the present mandatory set against the
battery category (`lmt`/`ev`/`industrial`/`stationary`) using the **Battery Pass Longlist
v1.2** (free DIN-99100 substitute; 93 attributes with mandatory/voluntary flags per
category + access tier + Annex XIII ref). E.g. *remaining capacity / power capability /
round-trip efficiency* are mandatory for **LMT & Stationary** but voluntary for **EV &
Industrial**; *capacity threshold for exhaustion* is **EV-only**; *test reports* are
authorities-tier (see [[dpp-knowledge]] §5 for the role→tier mapping).
Report a missing-mandatory as a `regulatory-completeness` finding
(distinct from `value-type` / AASd-*). Full attribute set + legal field list:
[[dpp-aas-compliance]] §8.1–8.2.

---

## Behavioural notes for Claude using this skill

- When the user pastes a validator error, **lead with the AASd rule ID
  if present** and look it up in §3. Quote the constraint verbatim
  before proposing a fix.
- When the user asks "is this AAS valid?", **walk the §2 decision tree**
  in your response. Don't jump to a single-stage answer.
- For fix recipes, **prefer §4's auto-fix decisions** over guessing. A
  fix that violates the §5 philosophy (silently inserts data the user
  didn't have) is worse than reporting the failure.
- When a rule has `status=context` in §3, **flag that you can't fully
  verify it from the file alone** — it needs ConceptDescription /
  registry resolution. Don't pretend to check what you cannot.
- When the user is implementing a validator from scratch, **start from
  the `prod`-tagged rules in §3** (the 22-ish most common). Adding more
  later is straightforward; getting the foundation wrong is not.
- Cite the spec version (IDTA-01001 v3.2) when the wording matters.
  Constraints have been renumbered + clarified across versions.
- For the legacy / removed entries: **do NOT generate fix logic** for
  AASd-010, AASd-011, AASd-015, AASd-025, AASd-064 (View), AASd-080,
  AASd-081 in current systems. They are present for vintage-spec
  recognition only.

## The mirror blind spot: a rule INTRODUCED later is as wrong as a removed one (2026-09-07)

The removed-rule case (AASd-013/090/120) was already settled law here. Its mirror
was not, and it shipped: **AASd-138 — new in 3.2 — was enforced as a BLOCKING
error against 3/1 output**, so a conformant document was reported INVALID and the
user's Download was locked. `AASd-137` was doing the same as a warning. The
existing provenance guard could not see it: it only asked "is this rule
REMOVED?", never "does this rule EXIST YET in the revision we emit?".

**The rule, generalised:** a conformance claim is valid only *for a revision*.
Judge every citation against the revision the exporter actually writes — not
against "the spec". Both directions are false-invalids:

| Failure | Example | Guard |
|---|---|---|
| Rule REMOVED, still enforced | AASd-013 / 090 / 120 | removed-set check |
| Rule NOT YET INTRODUCED, enforced | AASd-137 / 138 (3.2-only) | `introducedIn` vs emitted namespace |
| Rule dead but its BEHAVIOUR survives | `delete element.idShort` "per AASd-120" | funnel property tests |

**Implementation pattern:** an emitted-namespace constant (e.g. 3/1) + a
rule→introduced-in map + a `ruleAppliesToEmittedVersion()` check; each rule
records the first revision carrying it. The detection code is GATED, never
deleted, so bumping the exporter turns the rule back on in the same commit.

**Behaviour, not just messages.** The third defect of that day carried no string
at all: `moveElementByPath` deleted an SML child's idShort when it was dragged
into a list, citing removed AASd-120 — silent data loss, invisible to any
message-based guard. Test the FUNNELS (add / move / duplicate / import / export)
for the property the dead rule used to impose, not the wording.

**Watch for a shadowed registry key.** `AASd-137` was registered twice in the
same object literal; the second entry won and silently discarded the first's
metadata. TypeScript says nothing. Assert key uniqueness in the guard.

Test batteries that encode all of the above: a runtime probe with a document that
deliberately trips every version-scoped rule + static citation scan + registry
integrity + funnel behaviour + a comment-voice detector, and a rule-version gate test.
