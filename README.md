# AAS and DPP knowledge skills for Claude Code

Eighteen domain-knowledge skills for working with the **Asset Administration
Shell (AAS, IDTA V3.x)** and the **EU Digital Product Passport (DPP)**. Each skill
is a folder with a `SKILL.md` that Claude Code loads when a task matches its
description. Several skills bundle the official IDTA specification PDF they are
based on, and every skill ships a set of evaluation questions whose answers are
tied to literal quotes in official sources.

## The skills

| Skill | What it covers |
|---|---|
| `aas-knowledge` | AAS 3.1 metamodel essentials, the statically checkable AASd-* constraints, the IDTA submodel template catalogue, Battery Passport / DPP anchors, the validation pipeline, extraction pitfalls. |
| `aas-validation` | The 79 AASd-* constraints (IDTA-01001 Part 1), the revision ledger (rules removed in 3.1, added in 3.2), the XSD → AASd-* → aas-test-engines decision tree, fix recipes, auto-fix versus flag, CI patterns, DPP value-list checks. |
| `iec61360` | DataSpecificationIEC61360 (IDTA-01003-a Part 3a): element set, `dataType` enum, levelType, value lists, ConceptDescription authoring. |
| `aasx-format` | The AASX package (IDTA-01005 Part 5, OPC/ZIP): content types, relationship IRIs, origin and supplementary parts, File element paths, writer defects. |
| `aas-security` | IDTA-01004 Part 4 Access Rule Model versus production authentication and signing (OAuth, mTLS, JWS, JCS), with the regulatory access tiers. |
| `eclass-irdi` | ECLASS / IEC CDD IRDI grammar, primary versus supplemental semanticIds, version-suffix drift, ECLASS licensing boundary. |
| `aas-submodel-templates` | Map of the IDTA submodel templates: which template solves which job, current versions, cross-template pitfalls. |
| `aas-template-registry` | Per-element cardinality registry of 155 published template versions: template JSON versus specification PDF, the effective value and its evidence, prose rules with literal quotes. |
| `aas-nameplate` | IDTA-02006 Digital Nameplate 3.0.1: version-pairing table (IEC CDD primary + ECLASS supplemental), mandatory set, Markings, AddressInformation. Bundles the PDF. |
| `aas-handover` | IDTA-02004 Handover Documentation 2.0 (VDI 2770): Document tree, classification system, DigitalFile semantics, 1.2 → 2.0 migration. Bundles the PDF. |
| `aas-bom` | IDTA-02011 Hierarchical Structures (Bill of Materials): ArcheTypes, Entity tree, HasPart / IsPartOf references, multi-AAS linking. Bundles the PDF. |
| `aas-time-series` | IDTA-02008 Time Series Data 1.1: Metadata / Record schema, internal, linked and external segments. Bundles the PDF. |
| `aas-carbon-footprint` | IDTA-02023 Carbon Footprint 1.0: PCF tree, life-cycle phases, PACT subtree, JSON-versus-PDF disagreements. Bundles the PDF. |
| `aas-asset-interfaces-description` | IDTA-02017 Asset Interfaces Description (AID) 1.0 / 1.1 / 1.2, grounded in the W3C WoT Thing Description and its protocol bindings. Bundles the PDFs. |
| `aas-asset-interfaces-mapping` | IDTA-02027 Asset Interfaces Mapping Configuration (AIMC) 2.0, with the v1.0 differences. Bundles the PDF. |
| `aas-capability-description` | IDTA-02020 Capability Description: capability tree, role qualifier, constraints, realization by skills. Bundles the PDF. |
| `dpp-knowledge` | DPP regulation and architecture: ESPR (2024/1781), Battery Regulation (2023/1542), CIRPASS, access tiers, data carriers, registry. Bundles the EUR-Lex texts. |
| `dpp-aas-compliance` | Realising a DPP as an AAS: CEN/CENELEC JTC 24, IDTA 02099 DppMetadata, the IDTA 02035 Battery Passport series, field-level mapping and a compliance checklist. |

## Install

Symlink every skill into your user-level Claude Code skills folder:

```bash
./install.sh                      # -> ~/.claude/skills
./install.sh /path/to/project/.claude/skills   # or into one project
```

`install.sh` creates symlinks, so a `git pull` updates the skills in place. It never
overwrites a real (non-symlink) folder of the same name. To install a single skill,
copy or symlink its folder from `skills/` into `~/.claude/skills/`.

## Evals

Every skill has `evals/evals.json` (8 to 15 questions) and `VERSION.json` (version,
last verification date, pinned sources). Each question carries a citation: the
document, revision, file, page or line locator, and a **literal quote** that must
occur there.

```bash
python3 tools/run-evals.py selftest              # structural self-test of all evals
python3 tools/run-evals.py selftest --skill aas-bom
python3 tools/run-evals.py grade answers.json    # grade answers {item id: answer text}
```

`selftest` first proves it can fail (a fixture with planted defects must trigger every
check), then verifies every citation: the cited file exists and the quote occurs at the
cited page or lines. It needs Python 3.9+ and `pypdf` (only for citations into a PDF).

Most citations point at files in this repository (`skills/…`, `vendor/…`). Some point at
official sources that are not redistributed here, through the aliases in
`tools/sources.json`:

- `idta-pdfs:` a local mirror of
  [admin-shell-io/submodel-templates](https://github.com/admin-shell-io/submodel-templates)
  (`pdf/`, `json/`, and `txt/` with the per-page text of each PDF);
- `idta-specs:` a folder with the IDTA-01001 Part 1 Metamodel v3.0 PDF.

Point an alias at your copy with `AAS_SOURCES_IDTA_PDFS=/path` or
`AAS_SOURCES_IDTA_SPECS=/path`. Without them, run
`python3 tools/run-evals.py selftest --skip-missing-sources`: those citations are counted
and reported as skipped, never as passed.

`UPDATE-WATCH.md` lists, per skill, the upstream sources to watch and what to re-check
when one of them changes.

## Source and citation discipline

These skills are maps; the official documents are the law.

- **Primary sources only.** Facts come from the IDTA specifications and submodel
  templates (PDF and template JSON), the official XSD and JSON schemas, aas-core-meta,
  and EU legal texts on EUR-Lex. A secondary source never settles a question.
- **Verbatim, never from memory.** semanticIds, idShorts, enumeration literals and
  cardinalities are transcribed from the source. Where a printed value is ambiguous the
  skill says `VERIFY-IN-PDF` instead of guessing.
- **Read the bundled PDF first.** A template skill that bundles its specification asks
  the model to read it before answering; if the skill and the PDF disagree, the PDF wins
  and the skill is wrong.
- **Revision-aware.** A constraint is cited only for the metamodel revision that
  contains it: a rule removed in 3.1 or introduced in 3.2 is never applied to a document
  of another revision.
- **The burden of proof is on INVALID.** A verdict of "invalid" names the concrete
  normative rule (XSD facet, JSON-schema keyword, AASd/AASc constraint, template
  requirement) and its source.
- **Evidence versus decision.** Where the official sources disagree (for example a
  template JSON and its PDF), the skill states both with their locations and labels any
  resolution as a project decision, not as the IDTA rule.

## Licence

- Skill text and documentation (every `SKILL.md`, references, evals and notes): [CC BY 4.0](LICENSE-CC-BY-4.0).
  Reuse is free, including commercially, with attribution.
- Scripts, tools and tests: [MIT](LICENSE).
- Third-party material bundled here (IDTA specifications and schemas, aas-core-meta, EUR-Lex
  texts) keeps its own licence; see `NOTICE.md`.
