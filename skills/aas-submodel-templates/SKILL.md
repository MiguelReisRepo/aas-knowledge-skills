---
name: aas-submodel-templates
description: The backbone map of IDTA Submodel Templates — which template solves which job, the IDTA numbering (02002 Contact Information, 02003 Technical Data, 02004 Handover Documentation, 02006 Digital Nameplate, 02008 Time Series, 02011 Hierarchical Structures/BoM, 02014 Functional Safety, 02017 Asset Interfaces Description, 02018 Maintenance Instructions, 02020 Capability Description, 02023 Carbon Footprint, 02035 Digital Battery Passport, 02056 Data Retention Policies, 02099 Digital Product Passport), where the official PDFs live, and the authoring discipline that applies to EVERY template (read the official PDF first; version-pair the submodel semanticId with its elements; satisfy the mandatory-cardinality set). Use this skill when the user asks which submodel template to use for a job, mentions an IDTA-02xxx number, wants an overview of published templates, starts modelling a NEW submodel type that has no dedicated skill yet, or asks how templates relate to each other (Nameplate vs DBP Part 1, Technical Data vs DBP Part 4, BoM vs DPP). Dedicated deep skills exist for some templates (aas-bom for 02011; dpp-aas-compliance for 02099/02035/02023) — route there when the work is inside one of those.
---

# IDTA Submodel Templates — the backbone map

One AAS = one shell + N submodels, and each submodel SHOULD instantiate a
published IDTA Submodel Template so consumers can interpret it by semanticId
instead of by out-of-band agreement. This skill is the MAP: what exists, what
each is for, and the discipline that keeps an instance conformant.

## Routing — dedicated skills first

| Working on | Go to |
|---|---|
| BoM / component hierarchy / IDTA-02011 | **[[aas-bom]]** (bundles the official PDF — mandatory read) |
| DPP / battery passport / ESPR mapping (02099, 02035, 02023) | **[[dpp-aas-compliance]]** + [[dpp-knowledge]] |
| Metamodel types, References, Entities | [[aas-knowledge]] |
| AASd-*/AASc-* constraints, engine failures | [[aas-validation]] |
| Is element X of template Y mandatory? JSON vs PDF cardinality | **[[aas-template-registry]]** |

For any template WITHOUT a dedicated skill, this skill + the official PDF is
the path. Never author from memory of a template.

## ⚠ The universal rule — the official PDF decides, every time

Before authoring, editing, reviewing, or signing off ANY template instance:

1. **Dedicated skill exists** → invoke it; read its bundled PDF (its rule).
2. **No dedicated skill** → get the official PDF and read the data-model
   section + examples in full:
