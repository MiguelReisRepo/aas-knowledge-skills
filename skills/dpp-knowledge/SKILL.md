---
name: dpp-knowledge
description: Digital Product Passport (DPP) regulatory + architecture expertise — EU ESPR (Regulation 2024/1781) framework, the delegated-act roadmap per product category (batteries, textiles, electronics, construction, furniture, tires, detergents), DPP architecture (unique identifier, data carrier QR/RFID/NFC, repository / registry / resolver chain, access tiers public/regulator/recycler), CIRPASS reference architecture, stakeholder roles + permissions, lifecycle phases, data exchange formats (AAS / JSON-LD / GS1 EPCIS / GS1 Digital Link), integration with AAS Battery Passport (IDTA-02035), and the non-obvious pitfalls of multi-stakeholder DPP deployments. Use this skill whenever the user works with ESPR, Digital Product Passport, DPP, product passport, EU 2024/1781, CIRPASS, delegated acts for ecodesign, GS1 Digital Link, EPCIS, product carbon footprint at the DPP level, recyclability disclosure, market-surveillance DPP access, customs DPP verification, or any architecture decision touching "what goes in the passport, who can read it, where does it live". Also covers the EIGHT harmonised EN 182xx standards (EN 18216/18219/18220/18221/18222/18223 cited in the OJ, plus the unpublished EN 18239/18246) and what each does and does NOT require, and the LIVE EU DPP Registry as documented in the Commission's operator guide (EU Login, sealed-declaration enrolment, online-form vs file-upload submission, Model/Batch/Item granularity, the UPI-must-resolve rule). Trigger even when the user names a category (battery / textile / appliance / EV) without saying "DPP" explicitly, and whenever they mention an EN 182xx number, the EU DPP Registry, UPI resolution, or DPP registration/enrolment.
---

# DPP knowledge

The Digital Product Passport (DPP) is the EU's umbrella mechanism for
per-product traceability, sustainability disclosure, and recyclability,
mandated under the Ecodesign for Sustainable Products Regulation (ESPR,
Regulation 2024/1781). Unlike a static spec sheet, a DPP is a **digital
artefact, with a unique identifier, that travels with the product through
its entire lifecycle** and exposes different facets to different audiences
(consumer, regulator, recycler, customs).

This skill captures the **regulatory framework + architecture patterns**.
It complements `aas-knowledge` — AAS is one of the official **carrier
formats** for DPP content; DPP is the **business + legal** layer that
says what must be in the carrier and who can read it.

If the user is working with **ESPR / Regulation 2024/1781**, the Battery
Regulation §77 DPP, CIRPASS architecture, a category-specific delegated
act (textiles, electronics, etc.), GS1 Digital Link, product UIDs, or
multi-stakeholder access control over product data — load this content.

---

## 1. Regulatory framework

### ESPR — Regulation (EU) 2024/1781

The umbrella regulation that establishes the DPP as a horizontal
instrument across product categories. Replaces the 2009 Ecodesign
Directive.

- **In force**: 18 July 2024 (entered into force 20 days after publication)
- **DPP becomes effective**: per category, via **delegated acts**. No
  category-blanket effective date — each product family gets its own
  timeline + scope.
> **Article map, verified against the EUR-Lex text on 2026-10-19.** An earlier
> version of this list put the registry in Art. 10, called Art. 14 "market
> surveillance access" and gave "10 years" as a retention default. All three
> were wrong. Use this table; quote the article text, not this summary.

| Article | What it actually says |
|---|---|
| **2(28)** | DPP = "a set of data specific to a product that includes the information specified in the applicable delegated act adopted pursuant to Article 4 and that is accessible via electronic means through a data carrier" |
| **2(30)** | unique product identifier = "a unique string of characters for the identification of a product that also enables a web link to the digital product passport" |
| **9** | The DPP. (1) products only on the market if a DPP is available; "The data in the digital product passport shall be accurate, complete and up to date." (2) delegated acts specify, per product group: data (Annex III), data carriers, model/batch/item level, access before purchase, **who may access which data (f)**, **who may create or update which data (g)**, update arrangements (h), and **(i) the availability period, "at least the expected lifetime of a specific product"**. (3) aims include "improve the traceability of products along the value chain". |
| **10** | Essential requirements: persistent unique product identifier via a data carrier; open, interoperable, machine-readable, no vendor lock-in; no customer personal data without consent; (4) **a back-up copy through a DPP service provider**. |
| **11** | Technical design and operation: (b) free of charge, easy access per access rights for a long list of actors; (c) stored by the operator or DPP service providers; (d) new DPP linked to the original; **(e) available "including after an insolvency, a liquidation or a cessation of activity"**; (f) write rights restricted; (g) authentication, reliability, integrity; (h) security, privacy, fraud. Service providers may not sell or reuse data beyond the service. |
| **12** | Unique operator and facility identifiers (heading not re-verified). |
| **13** | **The registry**: by 19 July 2026, stores at least the unique identifiers (and battery identifiers of Reg. 2023/1542 Art. 77(3)); (5) the registration identifier "shall not be deemed to be proof of compliance". |
| **14** | Web portal for data in the DPP. |
| **15** | Customs controls relating to the DPP. |
| **22** | SMEs: digital tools and guidelines with delegated acts, one-stop shops in Member States, possible financial and technical support. |
| **41** | Presumption of conformity; **(2) DPPs conforming to cited harmonised standards are presumed to meet Arts. 10 and 11 "to the extent that those requirements are covered"**. |
| **42** | Common specifications by implementing act, an "exceptional fall-back" only when the standardisation request failed. |

There is **no** retention period in the ESPR itself: Art. 9(2)(i) leaves it to
each delegated act, with "at least the expected lifetime" as the floor.

### Category-specific anchors

DPP technical content lives in **delegated acts** under Article 4 of ESPR
(and, for batteries, in the pre-existing Battery Regulation).

| Category | Anchor | DPP mandatory from |
|---|---|---|
| **LMT, industrial (>2 kWh) and EV batteries** (the 2 kWh threshold is for industrial only) | Regulation (EU) 2023/1542 Art. 77(1) + Annex XIII | **18 Feb 2027** |
| **Textiles** (clothing + footwear) | ESPR delegated act, draft 2025 | ~2027 |
| **Furniture** | ESPR delegated act, planned 2026 draft | ~2028 |
| **Construction products** (cement, steel) | ESPR delegated act, overlapping CPR rev. | ~2028 |
| **Iron + steel** | ESPR delegated act, draft 2025 | ~2027 |
| **Tires** | ESPR delegated act, draft 2026 | ~2028 |
| **Detergents** | ESPR delegated act, planned | TBD |
| **Electronics** (broad) | ESPR + RoHS + WEEE alignment, planned | TBD |

**Working priority list** (Commission's first wave of delegated acts,
published April 2025, COM(2025) 187, stored in `sources/eur-lex/`): textiles, iron+steel, aluminium, furniture, tires.
Its year column is headed "Indicative timeline for adoption": the years (iron and steel 2026; textiles, tyres,
aluminium, repairability 2027; furniture 2028; mattresses, EEE recycled content/recyclability 2029) are planned
adoption years of the delegated acts, not dates from which obligations apply. The "~" dates in the table above are
older approximations.

**Battery passport, Reg. (EU) 2023/1542 Art. 77 (OJ text):** (1) from 18 February 2027 "each LMT battery,
each industrial battery with a capacity greater than 2 kWh and each electric vehicle battery". (2) access:
point 1 of Annex XIII public; points 2 and 3 (test reports) "only to notified bodies, market surveillance
authorities and the Commission"; points 2 and 4 to persons with a legitimate interest (not point 3).
(3) accessed "through the QR code referred to in Article 13(6)" linking to a unique identifier the
operator attributes; QR code and identifier comply with ISO/IEC 15459-1 to -6 "or their equivalent".
(7) after preparation for re-use/repurposing or remanufacturing the operator placing it on the market takes
over, and the battery gets "a new battery passport linked to the battery passport or passports of the
original battery". (8) "A battery passport shall cease to exist after the battery has been recycled."
Batteries are NOT in this wave because Article 77 of 2023/1542 already
covers them.

### Adjacent regulation that the DPP plugs into

The DPP is the **mechanism**, but the content obligations are often set
elsewhere:

- **CSRD** (Corporate Sustainability Reporting Directive) — entity-level
  ESG disclosures. DPP is product-level; not the same, but PCF figures
  in CSRD reports come from product DPPs.
- **CBAM** (Carbon Border Adjustment Mechanism) — customs use DPP carbon
  data to compute CBAM levies on imports.
- **CRMA** (Critical Raw Materials Act, 2024/1252) — declares the 17
  strategic + 34 critical raw materials. DPPs must declare CRM
  mass-fraction + recycled content.
- **CPR** (Construction Products Regulation revision) — for cement,
  steel, etc., uses the DPP as the disclosure channel.
- **PEFCR** (Product Environmental Footprint Category Rules) — per-
  category PCF calculation methodology; the DPP carries the PEFCR result.

---

## 2. DPP architecture

The official EU reference architecture comes from the **CIRPASS** projects
(CIRPASS-1 2022-2023, CIRPASS-2 2024-2026 led by the Joint Research Centre).
Four-layer model:

```
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 4 · Applications                                          │
│ Consumer apps, retailer portals, recycler tools, customs systems│
└─────────────────────────────────────────────────────────────────┘
              ▲ access tiers + role-based ACL
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 3 · DPP data repositories                                 │
│ Decentralised: economic operator hosts its own; AAS / JSON-LD / │
│ EPCIS payloads served via HTTPS.                                │
└─────────────────────────────────────────────────────────────────┘
              ▲ resolves UID → repository URL
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 2 · EU product passport registry (Article 13)             │
│ Centralised pointer: UID → economic operator's repository URL.  │
│ Commission-operated, free, machine-readable.                    │
└─────────────────────────────────────────────────────────────────┘
              ▲ scan / NFC tap / search
┌─────────────────────────────────────────────────────────────────┐
│ LAYER 1 · Data carriers (per-unit)                              │
│ QR (most common), GS1 DataMatrix, RFID, NFC. Encodes the UID    │
│ as a GS1 Digital Link URL or URN.                               │
└─────────────────────────────────────────────────────────────────┘
```

The decoupling matters: the registry holds POINTERS, not data. Economic
operators keep control of their own data and only publish the URL. The
registry is the trusted resolver; the operator is the source of truth.

### 2.1 The EU DPP Registry as it ACTUALLY works (not as planned)

Sourced from the Commission's own **DPP Registry User Guide for Economic
Operators, DG GROW Digital Solutions** (v1.01 of 2026-07-28; re-verified against
**v1.03, last published 2026-09-16, 63 pages**, downloaded from
single-market-economy.ec.europa.eu on 2026-10-12).

> **v1.03 headline: registration of battery passports is NOT yet possible.**
> Verbatim: "Successful registration of DPPs for batteries is not currently
> available, as the semantic catalogue for this product group has not yet been
> defined. Currently, it is not possible to successfully register DPPs."
> Batteries are "the first product group for which DPP registration will be
> available". Re-check the latest guide before saying otherwise.
Layer 2 above is no longer a plan — it is an operating system with a test
environment, and the operational detail changes what an implementer must build.

**Getting in is a legal-identity process, not a signup.**
1. **EU Login** account (the Commission's SSO) — a prerequisite, not optional.
2. An **organisation application**, as Legal Person or Natural Person.
3. Verification by **sealed declaration**: you request a PDF that *the
   Commission seals*, the **legal representative signs or seals it**, you upload
   the signed document and submit. Then it is reviewed and can be **rejected
   with an error report**. v1.03 detail: the signature must be a **QES or QSeal
   from a Qualified Trust Service Provider**, embedded as **PAdES Baseline
   B/T/LT/LTA**. "A qualified certificate installed as a software file (e.g.
   .p12 /.pfx) ... produces only an advanced signature (AdES/QC), which will be
   rejected." Adobe's default signing format can also be rejected (must be
   PAdES/CAdES-equivalent). Other formats "shall not be accepted".

   Consequence for product planning: onboarding an economic operator to the real
   registry has a human, days-long legal step in the middle. Any UX that implies
   "register your passport in one click" is wrong about the registry.

**Registering a DPP.** Two submission methods, and note which one is missing:
- **Online form** — a single DPP.
- **File upload** — a single DPP *or a batch*.
- There is **no machine-to-machine API described in the user guide**. If you
  need one, do not assume it exists; verify before designing against it.

**What the registry stores (v1.03, verbatim):** "The DPP Registry does not
store the full DPP data. Instead, it records a subset of information necessary
to identify and access the DPP, such as unique product identifiers and the
location where the passport is hosted." The registration record binds the UPI to
a **Unique Registration Identifier** issued by the registry; ESPR Art. 13(5):
that identifier "shall not be deemed to be proof of compliance". The UPI is "a
mandatory value conforming to a URL format compliant with JTC 24 standards. Max
length is 2000 chars." No subscription fee is expected. A separate **test
environment** exists, with its own EU Login, whose data may be cleaned.

**The UPI requirement is the load-bearing one.** The guide states the Unique
Product Identifier "needs to resolve to where you have hosted the DPP Data in
question". The registry stores a *pointer*; resolution is the operator's
obligation. A passport whose identifier does not resolve is not registrable in
any meaningful sense.

**Granularity is a closed set: `Model`, `Batch`, `Item`.** And the guide is
explicit that **only Item is currently available and pre-selected**, "as it is
the agreed and defined level for the Batteries product group". So the enum has
three values but the live system accepts one, for one product group. Build the
three; expect to exercise one.

### 2.2 The EN 182xx harmonised family — EIGHT standards, not six

Cited in the OJ via **Commission Implementing Decision (EU) 2026/1736 of
14 July 2026 (OJ L, 15.7.2026; ELI http://data.europa.eu/eli/dec_impl/2026/1736/oj)**,
verified on EUR-Lex 2026-10-19: **EN 18216 (data exchange protocols), 18219
(unique identifiers), 18220 (data carriers), 18221 (data storage, archiving and
persistence), 18222 (APIs for lifecycle management and searchability), 18223
(system interoperability)**, all :2026. Request: Implementing Decision
C(2024) 5423 (31 July 2024), amended by C(2025) 8024 (28 November 2025).
Presumption runs from the publication date. Legal effect: **ESPR Art. 41(2)**,
DPPs conforming to them "shall be presumed to be in conformity with the
requirements set out in Articles 10 and 11 to the extent that those requirements
are covered". So: presumption, not proof; only as wide as the clauses actually
cover; a reference can be restricted or withdrawn after a formal objection
(Reg. 1025/2012 Art. 11); fall-back = common specifications (ESPR Art. 42).
**Do not infer coverage from titles**: no title names access rights or
authentication/integrity (Art. 11(f)(g)), but security provisions may sit inside
18216/18222; check clauses before claiming the presumption for those. Two more belong to the family and are **not yet
published**: **EN 18239** and **EN 18246**. Saying "the six harmonised
standards" is a common error; the family is eight and two are pending.

Facts worth carrying, each of which contradicts a plausible assumption:
- **EN 18216 clause 5 (normative): JSON *and* HTML are BOTH mandatory.** Serving
  only JSON is not conformant. Clause 4 sets **HTTP/2 as the minimum version**
  and **TLS 1.2 as the minimum** — those are compliance claims, so measure them
  rather than assuming the host provides them.
- **EN 18221 specifies no retention period at all**, while **EN 18219 marks
  Article 10(4) as Not Applicable**. So no harmonised standard currently gives
  presumption of conformity on the backup obligation. Treat retention as open
  ground, not as solved by citing a standard.
- **EN 18223's common information model does not reference the Asset
  Administration Shell normatively anywhere** (its clause 2 lists only
  ISO 8601-1, EN 18219 and EN 18221). Its `DigitalProductPassport` root class
  nonetheless maps field-for-field onto IDTA-02099-1 DppMetadata:
  `digitalProductPassportId`, `uniqueProductIdentifier`, `granularity`,
  `dppSchemaVersion`, `dppStatus`, `lastUpdate`, `economicOperatorId`,
  `facilityId`, `contentSpecificationIds`.

**Identifier length — the rule is CONDITIONAL, and a blanket cap is a bug.**
prEN 18219, quoted verbatim in GS1's balloting comments: *"For identifiers
conforming to ISO/IEC 15459-4: The identity for individual products and product
packages shall not contain more than 50 characters."* It applies to 15459-4
identities only; 15459-3 has its own rules for syntax, structure, length and
character set. Enforcing 50 characters on every identifier would wrongly reject
a GS1 Digital Link URL or a URN.

### 2.2a Standardisation framework behind the EN 182xx (verified 2026-10-19)

- **Regulation (EU) No 1025/2012**, Art. 2(1): a standard is "a technical
  specification, adopted by a recognised standardisation body, for repeated or
  continuous application, with which compliance is not compulsory"; (c) a
  harmonised standard is "a European standard adopted on the basis of a request
  made by the Commission for the application of Union harmonisation legislation".
  Art. 10(6): reference published in the OJ "without delay" when the standard
  satisfies the request. Art. 11: a Member State or the European Parliament can
  object; the Commission may publish, not publish or publish with restriction, and
  maintain, restrict or withdraw a reference.
- **Regulation (EU) 2022/2480** amended Art. 10: decisions on standards requested
  by the Commission are taken only by representatives of national standardisation
  bodies of EU/EEA states (applies since 9 July 2023).
- **Presumption comes from the sector law, not from 1025/2012**: for DPPs it is
  ESPR Art. 41(2); fall-back common specifications ESPR Art. 42 (also give
  presumption, recital 81).
- European standardisation organisations: CEN, CENELEC, ETSI (Annex I of
  1025/2012). National bodies (Portugal: IPQ) run the mirror committees through
  which engineers can take part.
- **Who must ensure the DPP and its back-up (verified on EUR-Lex 2026-10-26):** both the
  manufacturer (ESPR Art. 27(1)(c)) and the importer (Art. 29(2)(c)) must ensure, before placing on
  the market, that "a digital product passport is available ... including a back-up copy of the
  **most up-to-date version** ... stored by a digital product passport service provider in
  accordance with Article 10(4)". Importer = established in the Union, places a third-country
  product on the market (Art. 2(44)). Both put their contact details on the public part of the DPP
  (Arts. 27(6), 29(3)). Art. 11(e) survival is tied to "the economic operator responsible for the
  creation" of the DPP. The Regulation does not say how a passport is handed over when an importer
  fails or is replaced: a contract/architecture question (keep the DPP and its service-provider
  account under the manufacturer's control, importer with update rights).
- **Accreditation closes the trust chain** (standard → conformity assessment →
  certification → accreditation): **Regulation (EC) No 765/2008**, Art. 4(1) "Each
  Member State shall appoint a single national accreditation body"; Art. 2(11)
  defines it as the sole body in a Member State performing accreditation with
  authority derived from the State (Portugal: IPAC). A DPP claim backed by a
  certificate is only as strong as the accreditation of the body that issued it.
- **How a standard is decided (ISO/IEC Directives, verified 2026-10-20):** a new
  work item needs a 2/3 majority of the voting P-members **and** at least 4
  P-members (committees with ≤16 P-members) or 5 (≥17) committing experts.
  Ballot votes are approve / disapprove (with reasons) / abstain. Systematic
  review: an IS at least every **5 years** (TS every 3) → confirm, revise or
  withdraw. So an EN 182xx edition is not frozen: plan for revisions.
- **ITU is the odd one out of the WSC trio (ISO, IEC, ITU):** 193 Member States
  hold the vote; companies and universities join as Sector Members / Academia
  without a vote; its standards are called **ITU-T Recommendations**.

### 2.2b DPP vs traceability (verified 2026-10-19)

A DPP describes **what a product is** (ESPR Art. 2(28), "a set of data specific
to a product"); traceability records **what happened to it**. **GS1 EPCIS 2.0**
(ratified June 2022): "enables disparate applications to create and share
visibility event data"; event dimensions What, When, Where, Why, How; event types
ObjectEvent, AggregationEvent, TransactionEvent, TransformationEvent,
AssociationEvent. They meet (ESPR Art. 9(3)(c): DPP requirements shall "improve
the traceability of products along the value chain"; Battery Reg Annex XIII 1(d)
responsible sourcing from the due diligence report), but **link, don't merge**.
One shared identifier is not enough once materials are aggregated or transformed:
keep an explicit mapping from the passport identifier to item, lot and event
identifiers. Evidence for a claim like recycled content is more than events
(material accounting, independent verification).

### 2.2c UN Transparency Protocol, UNTP (verified on untp.unece.org 2026-10-19)

- UN/CEFACT (UNECE). "In July 2025, The UN/CEFACT Plenary Member States adopted
  Recommendation No. 49: Transparency at Scale – Fostering Sustainable Value
  Chains"; UNTP is "the practical application of Recommendation 49".
  "UNTP is a protocol, not a platform."
- Components: Digital Product Passport ("issued by the shipper of goods"),
  Digital Facility Record, Digital Traceability Event, Conformity Credential
  ("issued by conformity assessment bodies"), Identity Resolver, Digital Identity
  Anchor, Digital Corporate Record, Verifiable Credentials Profile (W3C VC + DID),
  Decentralised Access Control.
- **Relationship to the EU DPP (verbatim):** "The UNTP DPP does not conflict with
  national regulations such as the EU DPP. In fact, it can usefully be
  conceptualised as the upstream B2B feedstock that provides the data and evidence
  needed for the issuing of high quality national level product passports."
- Status: DPP spec **0.8.0**, "suitable for pre-production pilot
  implementations", 1.0 expected. Voluntary; gives no presumption under the ESPR.
- Principle: "implementing a sustainable practice once and then re-using it to
  satisfy multiple overlapping criteria". Reuse of evidence, not equivalence of
  legal regimes: an operator still verifies issuer, status and scope before
  mapping a supplier credential into an EU passport field.

### 2.3 What there is NO source for — do not build on these

Recorded because an unsourced detail repeated confidently is how bad
implementations get shipped, and this exact failure has happened twice.

- **The EN 18222 API route shapes.** Names circulate — `v1/dpps/{dppId}`,
  `dppsByProductId`, `dppsByIdAndDate`, `registerDPP`,
  `elements/{elementIdPath}`, a `compressed`/`full` depth flag. A sweep of a
  17-document EU/CEN/CIRPASS/GS1 corpus found **zero** occurrences of any of
  them. They may well be right; they are simply not sourced. Do not implement
  them as "EN 18222 conformance" without the normative text, and do not let a
  conformance statement claim that standard on their basis.

### Unique Identifier (UID)

A DPP UID must be:
- **Globally unique** for the unit (one battery, one garment)
- **Persistent** through the product's lifetime
- **Resolvable** to a URL via the registry

Common encodings (the operator picks one, the registry is format-agnostic):
- **GS1 Digital Link** (recommended for retail): `https://id.gs1.org/01/<GTIN>/21/<serial>`
- **URN** (recommended for industrial): `urn:operator:product:<serial>`
- **DID** (Decentralised Identifier, blockchain-leaning): `did:web:operator.com:dpp:<serial>`

GS1 Digital Link wins for consumer products because it doubles as a
human-readable URL when scanned. URN wins for industrial use where the
identifier feeds AAS `id` fields directly.

### Data carrier

QR code is the consumer default. For industrial / harsh environments,
RFID (EPC HF or UHF) and NFC are alternatives. ESPR Article 9 is
agnostic between them but the CIRPASS recommendation is:

- **Consumer goods**: QR code, printed on the product or label.
- **Industrial / EV batteries**: RFID UHF (read at distance, survives
  high temp / vibration).
- **Premium / connected goods**: NFC (tap-to-read with a phone).
- **Tiny components** (chips, small parts): aggregate carrier on the
  packaging, individual UIDs encoded within.

### Access tiers

A DPP exposes different facets per audience. CIRPASS defines four tiers:

| Tier | Audience | Examples |
|---|---|---|
| **Public** | Consumer, anyone with the URL | Brand, model, materials breakdown, recycling instructions, energy label |
| **Verified** | Authenticated economic operator | Full PCF with calculation method + auditor, full BoM |
| **Regulator** | Market-surveillance authorities | Compliance certificates, test reports, conformity assessment bodies |
| **Recycler / EoL** | End-of-life operators (post-take-back) | Disassembly instructions, hazardous substance locations, repair history |

The access mechanism is typically an HTTPS query with a header carrying
a tier-encoded token. CIRPASS leaves the auth method open (OAuth 2.0 with
DCR / mTLS / DID-based VC are all valid); each delegated act may tighten.

---

## 3. Data exchange formats

A DPP repository can serve content in any machine-readable format. The
ESPR Article 10(1)(d) requires all DPP data to be "based on open standards, developed with an
interoperable format" (machine-readable, structured, searchable, no vendor lock-in).
The four production options:

### AAS (Asset Administration Shell, IDTA V3.1)

The industrial-by-default carrier. Best when the product is already
modelled as an industrial digital twin upstream (manufacturing MES,
PLM). Battery Passport's IDTA-02035 template is the canonical example.

- Pros: rich submodel templates, integrates with IDTA tooling, AASX
  package format bundles everything (XML + JSON + files).
- Cons: verbose for consumer-grade content, slower indexing than JSON-LD.
- When to use: industrial batteries, machinery, electronics, components.

See `aas-knowledge` skill for the metamodel + submodel templates.

### JSON-LD (Linked Data)

The web-native carrier. Best when the DPP integrates with broader linked-
data graphs (schema.org, GS1 Web Vocabulary, sustainability ontologies).

- Pros: indexable by search engines, lightweight, plays well with REST APIs.
- Cons: less rich than AAS for industrial metadata; schema fragmentation
  across category groups (GS1 vs ECLASS vs schema.org).
- When to use: consumer goods, textiles, furniture.

### GS1 EPCIS 2.0

The supply-chain event carrier. Best for tracking events along the chain
(commissioned, shipped, received, returned, recycled).

- Pros: native to retail / pharma supply chain; integrates with GS1
  Digital Link UIDs.
- Cons: not a "passport" in the snapshot sense — it's an event log.
- When to use: as a complement to AAS / JSON-LD, NOT a substitute.
  Carry the lifecycle events in EPCIS; carry the static spec in AAS.

### GS1 Digital Link

Strictly the URL encoding (not a data format), but worth listing because
the resolver chain (Layer 2 → Layer 3 in §2) often uses Digital Link
resolution: a UID encoded as a URL that, when fetched, content-negotiates
the format the client wants (AAS XML / JSON-LD / HTML for the consumer).

---

## 4. Integration patterns

### AAS Battery Passport (the gold standard)

For batteries, the IDTA-02035 submodel template fits inside an AAS shell
and serialises to AASX. The EU 2023/1542 + DPP integration:

```
Battery (physical)
   │
   ▼ data carrier: QR (or RFID UHF for industrial)
   ▼ UID: urn:operator:battery:<serial>
   │
   ▼ resolver: EU registry → https://operator.com/dpp/<serial>
   │
   ▼ HTTPS GET with Accept: application/x-aasx
   │
operator.com/dpp/<serial>.aasx
  ├── /aasx/asset-administration-shell.xml
  ├── /aasx/submodels/Nameplate.xml
  ├── /aasx/submodels/<DBP Part 1…7>.xml     ← IDTA-02035 series: 7 submodel templates (02099-1 p.6)
  ├── /aasx/submodels/CarbonFootprint.xml    ← IDTA-02023, PCF
  ├── /aasx/submodels/HandoverDocumentation.xml  ← test reports, certs
  └── /aasx/files/                            ← embedded PDFs (EPD, conformity)
```

Access tier enforcement happens at the HTTP layer: the same UID returns
a stripped public AAS to anonymous callers and the full AAS (including
DueDiligence, SupplyChain, full BoM) to authenticated authorities.

### JSON-LD textile DPP

For textiles, the draft delegated act leans JSON-LD over schema.org +
GS1 Web Vocabulary. A typical resolver returns:

```jsonld
{
  "@context": ["https://schema.org", "https://gs1.org/voc/"],
  "@type": "Product",
  "gtin": "07391212345670",
  "serialNumber": "PXT-2026-01-0001",
  "manufacturer": "...",
  "materialComposition": [{ "material": "organic-cotton", "weightPct": 75 }, ...],
  "originCountry": "PT",
  "careInstructions": "https://operator.com/care/PXT-2026",
  "recyclability": { "score": "B", "process": "mechanical" },
  "dueDiligence": "https://operator.com/dd/PXT-2026.pdf"
}
```

Same access-tier model: anonymous → public sub-tree; authenticated →
full graph.

### Hybrid (AAS + EPCIS for events)

For complex industrial products with multi-stage supply chains: serve
the static spec as AAS, the per-event lifecycle log as EPCIS 2.0.
Resolver decides by `Accept` or query param:

```
GET /dpp/<UID>             Accept: application/x-aasx  → AAS bundle
GET /dpp/<UID>/events      Accept: application/json    → EPCIS 2.0 events
```

---

## 5. Stakeholder roles + permissions

Designing the access matrix is half the architecture work. The common
roles and their typical tier-mapping:

| Role | Tier read | Typical credential | Permission grant |
|---|---|---|---|
| **End consumer** | Public | none (scan QR) | Always-on, anonymous |
| **Retailer / distributor** | Public + Verified | API key, optional B2B contract | At sale time |
| **Service / repairer** | Public + Verified + Recycler | Authenticated repair operator credential | Tier rises with role registration |
| **Recycler / EoL operator** | Public + Recycler | Member of EU recycler registry, mTLS | Granted at take-back event |
| **Market surveillance** | All tiers | EU-issued credentials, regulator-side certs | Per the product group's delegated act (ESPR Art. 9(2)(f), Art. 11(b)); for batteries Art. 77(2) + Annex XIII |
| **Customs** | All tiers + CBAM data | EU customs system integration | At import declaration time |
| **Manufacturer / brand** | All tiers (write) | Operator's identity, signed by Notified Body | Always, for own products |

**Common mistake**: assuming roles imply tiers 1:1. A repairer may need
read on the recycler tier to access disassembly instructions WITHOUT
being granted regulator-tier access (which would expose competitor's
supply chain). Design the tier-to-role matrix explicitly; don't conflate.

**A collapsed 3-tier implementation (common mapping).** The table above is
the DOMAIN role vocabulary (CIRPASS/ESPR). An implementation can collapse it into
a 3-tier model per JRC145830: `public | professional | authority`. Mapping:
Verified/business → `professional`; Recycler/repairer → `professional`; Market
surveillance / customs / regulator → `authority`.

---

## 6. Lifecycle phases

A DPP isn't a snapshot — it's versioned. ESPR Art. 9(1) requires the data to be
"accurate, complete and up to date"; who may update what is set per product group
(Art. 9(2)(g)(h), Art. 11(f)). The typical phase model:

- **As-designed** (pre-production) — declared specs, planned PCF.
- **As-manufactured** (factory exit) — measured serial, batch QC results,
  realised PCF (often differs from planned by 5-15%).
- **In-use** (post-sale) — service history, repairs, software updates,
  in-field measurements (industrial only).
- **End-of-life** (take-back) — disassembly notes, recycled-content
  destinations.
- **Repurposed / remanufactured** (second life, batteries especially) —
  new UID linked to the old via a "derived from" relationship; old
  passport stays accessible.

Versioning anti-pattern: mutating the DPP in place. CIRPASS specifies
**append-only**: each phase emits a new versioned snapshot, the old
snapshots remain accessible (for the retention period of the delegated act, at least the expected
product lifetime: ESPR Art. 9(2)(i)).

---

## 7. Pitfalls and non-obvious rules

Items that bite in real deployments. Keep these in mind even when not
asked.

- **A DPP is NOT a complete LCA.** It carries SUMMARY indicators (PCF,
  recycled content), not the underlying inventory. Don't try to render
  the whole supply chain in one passport — it explodes the payload and
  the access matrix.
- **The registry holds POINTERS, not data.** Operators are the source
  of truth. If the registry goes down, well-architected operator
  endpoints still serve their own DPPs by UID lookup.
- **Public ≠ marketing-grade.** The consumer-facing tier should be
  truthful and complete on what's required; resist the urge to leave
  out unflattering numbers (recycled content < 5%, PCF higher than the
  category average). Market-surveillance reads BOTH tiers and catches
  inconsistencies.
- **Don't confuse UID, PID, and Article number.**
  - UID = unique per UNIT (one specific battery, one garment).
  - PID (product identifier) = the model / family (GTIN, MPN).
  - Article number = internal SKU; not regulatory.
  A DPP needs a UID, references its PID, and may carry the article number.
- **GS1 Digital Link URLs decay if the resolver is misconfigured.**
  Use `id.gs1.org` for portability; only use the operator's own domain
  if you commit to that domain for the whole retention period (at least the expected
  product lifetime, ESPR Art. 9(2)(i)).
- **JSON-LD context-pinning matters.** Don't reference `https://schema.org`
  without a version; the schema evolves and old fields can vanish.
  Pin to dated snapshots (`https://schema.org/version/26.0/`) for archival
  DPPs.
- **AAS + JSON-LD content negotiation needs proper `Accept` parsing.**
  Common bug: serving AAS XML when the client asked for JSON-LD because
  the resolver did a substring match on `application/`. Use full media-
  type matching.
- **Access-tier rotation requires think-ahead.** If a consumer's
  one-time token lets them read public + service-history, what happens
  when they sell the product to someone else? The token MUST be unit-
  scoped, not person-scoped.
- **CIRPASS is the architecture reference; the delegated acts are the
  obligation.** Don't quote CIRPASS as a regulation. Quote the
  category-specific delegated act for the legal anchor.
- **Don't overload the QR code.** The QR encodes a URL, not the DPP
  content. Putting PCF or BoM into the QR payload (because "it works
  offline") breaks the access-tier model entirely.
- **Battery Passport = DPP applied to batteries.** The IDTA-02035
  submodel is the carrier shape; EU 2023/1542 Article 77 is the legal
  trigger. Don't conflate the IDTA template version with the regulation
  effective date.
- **For industrial products, AAS is the right carrier.** Don't reinvent
  AAS in JSON-LD just because JSON looks lighter. The IDTA template
  catalogue + `aas-test-engines` conformance gate save weeks of
  validator work.

---

## 8. Authoritative references

When in doubt, consult these in this order:

- **ESPR text** (Regulation 2024/1781):
  [EUR-Lex 32024R1781](https://eur-lex.europa.eu/eli/reg/2024/1781/oj)
  — the umbrella regulation, Articles 9-14 for DPP mechanics.
- **EU DPP Registry — LIVE, with published operator documentation.** Corrected
  2026-08-02: this entry used to say "Commission JRC, in pilot 2025, watch the
  pages", which is stale twice over. It is run by **DG GROW Digital Solutions**,
  not JRC, and the **DPP Registry User Guide for Economic Operators (v1.01
  2026-07-28; v1.03 2026-09-16, 63 pages, the latest read)** documents enrolment, the sealed-declaration
  verification, both submission methods and the granularity levels. There is
  also a **test environment**, reachable from the Registry's Help Center. See
  §2.1 above for what it means for implementers.

- **Stored primary legal texts (in this repo, retrieved 2026-10-27)**: `sources/eur-lex/` holds the EUR-Lex
  English HTML of Regulation (EU) 2023/1542 (OJ text, consolidated version of 13.08.2026, the corrigenda that
  apply to English, amending Regulation (EU) 2025/1561), Regulation (EU) 2024/1781 (OJ text + corrigenda) and the
  ESPR Working Plan COM(2025) 187, each with CELEX number, URL, retrieval date and SHA-256 in `manifest.json`.
  Quote from these files only. Facts
  settled there that earlier summaries got wrong or left open: Annex XIII point 1(q) reads "Article 13(4) and (5)"
  since the corrigendum of 10.4.2026 (OJ L 2026/90285); battery due diligence applies from 18 August 2027
  (Regulation (EU) 2025/1561); Art. 77(10) (added by ESPR Art. 78) obliges the operator to upload the battery's
  unique identifier to the ESPR registry; Art. 78(e) keeps the battery passport available after the operator
  ceases activity and Art. 78(g) requires data authentication, reliability and integrity; the Working Plan's
  years are an "Indicative timeline for adoption" of delegated acts, not application dates.
- **Primary-source reading list** (public documents, not bundled: fetch EUR-Lex via a
  browser, since EUR-Lex blocks curl; the registry guide is a direct PDF download
  from single-market-economy.ec.europa.eu).
  - M604 standardisation mandate, CWA 18186 guidelines
    for creating a DPP, CEN DPP webinar (2026-06-25).
  - **EC DPP Registry operator guide v1.01** (the one above),
    EC DPP FAQ, JRC145830 data-requirements methodology.
  - CIRPASS D3.2 system architecture v1.9, D3.3 identification
    schemes v1.3, standardisation-gaps analysis v1.2, **CIRPASS2 AAS↔RDF
    interoperability**, CIRPASS2 D4.1 reference architecture v1.1.
  - **GS1's balloting comments on prEN 18219, 59 pages**, which
    quote the draft normative text verbatim and are the closest thing to the
    standard itself in this list; GS1 provisional DPP application standard;
    GS1 standards enabling DPP v2.2.
  - CIRPASS D2.1 textile attributes, CWA 18291 (TRICK textile
    data collection), Trace4Value textile data protocol (97 attributes).
  - **Not in the list:** the EN 182xx normative texts themselves. The GS1
    comments are commentary on a draft, not the published standard.
- **CIRPASS reference architecture**:
  [cirpass2.eu](https://cirpass2.eu) — the technical deliverables. The
  layered architecture in §2 comes from CIRPASS-2 D2.1.
- **Battery Regulation** (EU 2023/1542):
  [EUR-Lex 32023R1542](https://eur-lex.europa.eu/eli/reg/2023/1542/oj)
  — Article 77 (DPP mandate) + Annex XIII (data fields). See
  `aas-knowledge` skill for the IDTA-02035 template detail.
- **GS1 Digital Link**:
  [gs1.org/standards/gs1-digital-link](https://www.gs1.org/standards/gs1-digital-link)
  — the URL encoding spec.
- **GS1 EPCIS 2.0**:
  [ref.gs1.org/standards/epcis](https://ref.gs1.org/standards/epcis/)
  — the events spec; JSON-LD binding.
- **Working delegated-act drafts**: the Commission's ecodesign workstream
  publishes drafts; check the DG GROW pages and the JRC's ecodesign
  team.
- **CSRD / ESRS** (for the CSRD ↔ DPP overlap):
  [efrag.org](https://www.efrag.org) — the European Financial Reporting
  Advisory Group standards (ESRS) include E1 (Climate change) which
  pulls PCF data from DPPs.
- **CBAM**:
  [taxation-customs.ec.europa.eu](https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism_en)
  — for the customs ↔ DPP carbon-data exchange.

---

## Behavioural notes for Claude using this skill

- When the user is designing a DPP, **start from the legal anchor** (the
  delegated act / Article 77 / etc.), not from the data format. Wrong
  framing here cascades into wrong scope.
- When the question is "what format should we use?", **default to AAS
  for industrial / batteries / machinery; JSON-LD for textiles / furniture
  / consumer**. Mixed when lifecycle events matter (add EPCIS 2.0).
- When asked about access control, **lead with the four-tier model**
  (public / verified / regulator / recycler) and ask which roles the
  user has identified before recommending tokens or auth flows.
- For **Battery Passport** specifically, defer to `aas-knowledge` §4
  for the IDTA-02035 series (7 submodel templates) — this skill covers the DPP architecture
  context; that skill covers the IDTA-02035 detail. The two compose.
- Don't recommend storing DPP data on a blockchain unless the user has
  a specific reason (and even then, push back: ESPR doesn't require it
  and registries / repositories aren't immutability problems).
- For multi-stakeholder questions, **explicitly enumerate the roles**
  before designing the matrix. The role-to-tier mapping is the choice
  that locks in compliance posture.
- When in doubt about a category's timeline, **don't invent a date**;
  point to the JRC ecodesign workstream as the source.
