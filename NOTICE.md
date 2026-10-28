# Third-party material

This repository bundles third-party files under their own licences. The licence of each
item below was verified on 2026-10-27 against the upstream licence file at the pinned
commit or tag (or, for EUR-Lex, against the EUR-Lex legal notice). Each bundled file is
byte-identical (sha256) to the upstream file named, unless the entry says otherwise.
The original content of this repository is licensed separately: skill text and documentation
under CC BY 4.0 (`LICENSE-CC-BY-4.0`), scripts and other code under MIT (`LICENSE`).

| Material | Licence | Upstream | Verification |
|---|---|---|---|
| aas-core-meta (formalised AAS metamodel, Python meta-model files) | [MIT](https://github.com/eclipse-aascw/aas-core-meta/blob/main/LICENSE) | https://github.com/aas-core-works/aas-core-meta (now eclipse-aascw/aas-core-meta) | Each file is byte-identical (sha256) to the upstream file at the pinned commit; LICENSE at each pinned commit reads 'MIT License, Copyright (c) 2024 aas-core-meta AUTHORS'. |
| Official AAS XML and JSON schemas (IDTA-01001 Part 1 serialisations) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://github.com/admin-shell-io/aas-specs-metamodel | Each file is byte-identical (sha256) to schemas/xml/AAS.xsd or schemas/json/aas.json at the pinned tag; LICENSE.txt at each tag is 'Attribution 4.0 International' (CC BY 4.0) and the README states 'This work is licensed under a Creative Commons Attribution 4.0 International License'. |
| IDTA Submodel Template specifications (PDF) | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | https://github.com/admin-shell-io/submodel-templates | Each PDF is byte-identical (sha256 / git blob) to the file at the pinned path and commit of the official repository; LICENSE.txt of that repository (at f3790038b6c9 and d9822f7) is 'Attribution 4.0 International' (CC BY 4.0) and its README carries the CC BY 4.0 badge. |
| Material derived from the IDTA Submodel Templates (adaptations) | [CC BY 4.0 (adapted material)](https://creativecommons.org/licenses/by/4.0/) | https://github.com/admin-shell-io/submodel-templates | Derived from the CC BY 4.0 templates above (same repository licence). |
| EU legal texts from EUR-Lex (Regulation (EU) 2023/1542, Regulation (EU) 2024/1781, corrigenda, Regulation (EU) 2025/1561, COM(2025) 187) | [EU reuse policy (Commission Decision 2011/833/EU); consolidated texts and EUR-Lex editorial content CC BY 4.0](https://eur-lex.europa.eu/content/legal-notice/legal-notice.html) | https://eur-lex.europa.eu | EUR-Lex legal notice, 'Copyright notice' section, read 2026-10-27: 'The Commission's document reuse policy is based on Decision 2011/833/EU. Unless otherwise specified, you can re-use the legal documents published in EUR-Lex for commercial or non-commercial purposes.' and 'The copyright for the editorial content of this website, the summaries of EU legislation and the consolidated texts, which is owned by the EU, is licensed under the Creative Commons Attribution 4.0 International licence.' Each file's sha256 is checked against sources/eur-lex/manifest.json. |

## aas-core-meta (formalised AAS metamodel, Python meta-model files)

- Copyright: Copyright (c) 2024 aas-core-meta AUTHORS
- Licence: MIT (https://github.com/eclipse-aascw/aas-core-meta/blob/main/LICENSE)
- Upstream: https://github.com/aas-core-works/aas-core-meta (now eclipse-aascw/aas-core-meta)
- Changes: Renamed on disk (aas-core-meta-v3_x.py); content unchanged.
- Full licence text: `vendor/aas-core-meta/LICENSE`

| File in this repository | Upstream file | sha256 |
|---|---|---|
| `vendor/aas-core-meta/aas-core-meta-v3_0.py` | aas_core_meta/v3.py @ 11b116c5231d24dade11330ef127307f99a0e671 | `2ef62ab51feee191…` |
| `vendor/aas-core-meta/aas-core-meta-v3_1.py` | aas_core_meta/v3_1.py @ 02040d200af0cb3bad1fa9c9555d7fb640bb8667 | `d60dbaca77e3decc…` |
| `vendor/aas-core-meta/aas-core-meta-v3_2.py` | aas_core_meta/v3_2.py @ 54e5cb1e547fbf466c9d07c6eac7f921479a1fde | `92692f843c96b0de…` |

## Official AAS XML and JSON schemas (IDTA-01001 Part 1 serialisations)

- Copyright: Industrial Digital Twin Association (IDTA)
- Licence: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
- Upstream: https://github.com/admin-shell-io/aas-specs-metamodel
- Changes: None (copied under vendor/schemas/<revision>/).

| File in this repository | Upstream file | sha256 |
|---|---|---|
| `vendor/schemas/3.0/AAS.xsd` | schemas/xml/AAS.xsd @ tag IDTA-01001-3-0-1_schemasV3.0.9 | `40eb128b16846f97…` |
| `vendor/schemas/3.0/aas.json` | schemas/json/aas.json @ tag IDTA-01001-3-0-1_schemasV3.0.9 | `eb566d47316c9909…` |
| `vendor/schemas/3.1/AAS.xsd` | schemas/xml/AAS.xsd @ tag v3.1.2 | `9270966e703a7305…` |
| `vendor/schemas/3.1/aas.json` | schemas/json/aas.json @ tag v3.1.2 | `9a8a005e303634f5…` |
| `vendor/schemas/3.2/AAS.xsd` | schemas/xml/AAS.xsd @ tag v3.2.0 | `c04279e2660632f3…` |
| `vendor/schemas/3.2/aas.json` | schemas/json/aas.json @ tag v3.2.0 | `ffc64ab21d812d2c…` |

## IDTA Submodel Template specifications (PDF)

- Copyright: Industrial Digital Twin Association (IDTA)
- Licence: CC BY 4.0 (https://creativecommons.org/licenses/by/4.0/)
- Upstream: https://github.com/admin-shell-io/submodel-templates
- Changes: Renamed (spaces to hyphens); content unchanged.

| File in this repository | Upstream file | sha256 |
|---|---|---|
| `skills/aas-asset-interfaces-description/IDTA-02017-1-1_Submodel_Asset-Interfaces-Description.pdf` | published/Asset Interfaces Description/1/1/ @ f3790038b6c9 | `0eb2a417e537934e…` |
| `skills/aas-asset-interfaces-description/IDTA-02017-1-2_Submodel_Asset-Interfaces-Description.pdf` | published/Asset Interfaces Description/1/2/ @ f3790038b6c9 | `b624d085537d3ab2…` |
| `skills/aas-asset-interfaces-mapping/IDTA-02027_Submodel_Asset-Interfaces-Mapping-Configuration.pdf` | published/Asset Interfaces Mapping Configuration/2/0/ @ d9822f792b33 (May 2026 edition) | `02a631205cb08411…` |
| `skills/aas-bom/IDTA-02011-1-0_HierarchicalStructures.pdf` | deprecated/Hierarchical Structures enabling Bills of Material/1/0/ @ f3790038b6c9 | `95a9c8e63f445f9f…` |
| `skills/aas-capability-description/IDTA-02020_Submodel_Capability_Description.pdf` | published/Capability Description/1/0/ @ f3790038b6c9 | `0d306f79465639dd…` |
| `skills/aas-carbon-footprint/IDTA-02023_Submodel_CarbonFootprint.pdf` | published/Carbon Footprint/1/0/ @ f3790038b6c9 | `acccc2b7d72cfc91…` |
| `skills/aas-handover/IDTA-02004-2-0_Submodel_Handover-Documentation.pdf` | published/Handover Documentation/2/0/ @ f3790038b6c9 | `772a94bca7974e03…` |
| `skills/aas-nameplate/IDTA-02006-3-0-1_Submodel_Digital-Nameplate.pdf` | published/Digital nameplate/3/0/1/ @ f3790038b6c9 | `0c1d21e7743a4143…` |
| `skills/aas-time-series/IDTA-02008-1-1_Submodel_TimeSeriesData.pdf` | published/Time Series Data/1/1/ @ f3790038b6c9 | `461890af1fc72d99…` |

## Material derived from the IDTA Submodel Templates (adaptations)

- Copyright: Industrial Digital Twin Association (IDTA); adaptations by the authors of this repository
- Licence: CC BY 4.0 (adapted material) (https://creativecommons.org/licenses/by/4.0/)
- Upstream: https://github.com/admin-shell-io/submodel-templates
- Changes: Text layers extracted from the PDFs per page (skills/*/IDTA-*.txt); semanticIds and cardinalities transcribed from the template tables and JSON (skills/aas-nameplate/semanticid-map-3-0-1.json, skills/aas-handover/semanticid-map-2-0.json, skills/aas-template-registry/registry/**, skills/aas-template-registry/prose-rules.json); literal quotes in SKILL.md files.

Covers: `skills/*/IDTA-*.txt`, `skills/aas-nameplate/semanticid-map-3-0-1.json`, `skills/aas-handover/semanticid-map-2-0.json`, `skills/aas-template-registry/registry/`, `skills/aas-template-registry/prose-rules.json`

## EU legal texts from EUR-Lex (Regulation (EU) 2023/1542, Regulation (EU) 2024/1781, corrigenda, Regulation (EU) 2025/1561, COM(2025) 187)

- Copyright: © European Union, 1998-2026
- Licence: EU reuse policy (Commission Decision 2011/833/EU); consolidated texts and EUR-Lex editorial content CC BY 4.0 (https://eur-lex.europa.eu/content/legal-notice/legal-notice.html)
- Upstream: https://eur-lex.europa.eu
- Changes: Saved as rendered HTML pages (no edits). Only the Official Journal versions are authentic (EUR-Lex legal notice).

| File | CELEX | Document |
|---|---|---|
| `CELEX_32023R1542.html` | 32023R1542 | Regulation (EU) 2023/1542 of 12 July 2023 concerning batteries and waste batteries (Batteries Regulation), OJ L 191, 28.7.2023, pp. 1-117 |
| `CELEX_02023R1542-20260813.html` | 02023R1542-20260813 | Batteries Regulation, consolidated version of 13.08.2026 |
| `CELEX_32023R1542R05.html` | 32023R1542R(05) | Corrigendum to Regulation (EU) 2023/1542, OJ L 2024/90243, 17.4.2024 (Art. 1(6), Art. 92) |
| `CELEX_32023R1542R11.html` | 32023R1542R(11) | Corrigendum to Regulation (EU) 2023/1542, OJ L 2025/90794, 8.10.2025 (Art. 32(4)) |
| `CELEX_32023R1542R13.html` | 32023R1542R(13) | Corrigendum to Regulation (EU) 2023/1542, OJ L 2026/90285, 10.4.2026 (Annex XIII point 1(q): Article 13(4) and (5)) |
| `CELEX_32025R1561.html` | 32025R1561 | Regulation (EU) 2025/1561 of 18 July 2025 amending Regulation (EU) 2023/1542 as regards battery due diligence (Art. 48(1): 18 August 2027; Art. 48(5): 26 July 2026) |
| `CELEX_32024R1781.html` | 32024R1781 | Regulation (EU) 2024/1781 of 13 June 2024 establishing a framework for the setting of ecodesign requirements for sustainable products (ESPR), OJ L, 2024/1781, 28.6.2024 |
| `CELEX_32024R1781R01.html` | 32024R1781R(01) | Corrigendum to Regulation (EU) 2024/1781, OJ L 2024/90493, 7.8.2024 (Articles 77 and 78, incl. the new Art. 77(10) of Regulation (EU) 2023/1542) |
| `CELEX_32024R1781R02.html` | 32024R1781R(02) | Corrigendum to Regulation (EU) 2024/1781, OJ L 2025/90356, 28.4.2025 (Art. 10(1)(d), 20, 41(4), 65(3), 69(5)) |
| `CELEX_52025DC0187.html` | 52025DC0187 | Communication COM(2025) 187 final of 16.4.2025, Ecodesign for Sustainable Products and Energy Labelling Working Plan 2025-2030 |
| `ALL_32023R1542.html` | 32023R1542 | EUR-Lex 'ALL' page of Regulation (EU) 2023/1542: consolidated versions, corrections, modifications and completing acts |
| `ALL_32024R1781.html` | 32024R1781 | EUR-Lex 'ALL' page of Regulation (EU) 2024/1781 |

## Cited but not redistributed

The evals also cite official files that are not included here; `tools/sources.json` maps
their aliases to a local copy.

- `idta-specs:` IDTA-01001 Part 1 Metamodel v3.0 (PDF) (https://industrialdigitaltwin.org/en/content-hub/aasspecifications) — cited by evals; not redistributed here
- `idta-pdfs:` Mirror of github.com/admin-shell-io/submodel-templates (pdf/, txt/ per-page extractions, json/) (https://github.com/admin-shell-io/submodel-templates) — cited by evals; not redistributed here
