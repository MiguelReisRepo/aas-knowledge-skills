---
name: aas-asset-interfaces-description
description: Asset Administration Shell Asset Interfaces Description expertise — the IDTA-02017-1-1 "Asset Interfaces Description" (AID) submodel template (v1.1, April 2026; v1.0 was Jan 2024). AID describes HOW to reach an asset's live datapoints over a specific protocol so a Data Mapping Processor (DMP) can read/subscribe them (monitoring only in 1.0/1.1 — actions/events are declared but not detailed; write/invoke is a future version). AID is grounded VERBATIM in the W3C WoT Thing Description (WoT TD 1.1): each asset interface is an SMC `Interface__00__` (semanticId `.../AssetInterfacesDescription/1/0/Interface`, the WoT Thing) carrying `title/created/modified/support`, an `EndpointMetadata` SMC (base=WoT `td#baseURI`, contentType=`hypermedia#forContentType`, a `security` SML, `securityDefinitions` SMC, optional Modbus byte/word order), an `InteractionMetadata` SMC (`properties`/`actions`/`events` = WoT `td#PropertyAffordance`/`ActionAffordance`/`EventAffordance`), and an optional `ExternalDescriptor` SMC (File refs to GSDML/TD/MTP). Each datapoint is a `{property_name}` SMC (semanticId `.../1/0/PropertyDefinition`, suppl `td#name`) with a MANDATORY `forms` SMC (`td#hasForm`) carrying `href` (`hypermedia#hasTarget`, card 1) + protocol-specific terms keyed by prefix: htv_ (HTTP `w3.org/2011/http#`), modv_ (Modbus `wot/modbus#`), mqv_ (MQTT `wot/mqtt#`), uav_ (OPC UA `opcfoundation.org/UA/WoT-Binding/`), bacv_ (BACnet `w3.org/2022/bacnet#`), iolv_ (IO-Link `.../1/1/IO-Link/`, informative). Datapoint schema = boolean|integer|number|string|array|object with json-schema terms (const/enum/default/min_max/lengthRange/itemsRange/items/properties/uriVariables/valueSemantics). Security schemes: nosec_sc/basic_sc/digest_sc/apikey_sc/bearer_sc/psk_sc/oauth2_sc/combo_sc/auto_sc/opcua_channel_sc/opcua_authentication_sc (WoT `wot/security#`). Interface SMC card 1..* (SML NOT used — multiple interfaces are sibling SMCs). Use this skill whenever the user models, reviews or validates an asset's communication/connectivity interface as an AAS submodel, mentions IDTA-02017, AID, Asset Interfaces Description, WoT Thing Description in AAS, EndpointMetadata/InteractionMetadata, forms/href, EU Data Act connectivity metadata, a Modbus/HTTP/MQTT/OPC UA/BACnet/IO-Link datapoint description, or the companion AIMC (IDTA Asset Interfaces Mapping Configuration) submodel. CRITICAL TRAP: the Submodel semanticId is version `1/1` (`https://admin-shell.io/idta/AssetInterfacesDescription/1/1/Submodel`) but every core element (Interface/EndpointMetadata/InteractionMetadata/ExternalDescriptor/PropertyDefinition/key/minMaxRange/lengthRange/itemsRange/valueSemantics/externalDescriptorName) is still PRINTED with version `1/0` in the §2 tables, even though Annex F says they were "changed to version 1.1" — see the discrepancy list; treat the printed 1/0 values as authoritative until reconciled against the official AASX. AID 1.2 (IDTA 02017 Version 1.2, version history 05.10.2026, published 2026-10-05) is now the latest: Submodel semanticId `.../AssetInterfacesDescription/1/2/Submodel`, core elements still `1/0` (the 1.2 edition removed the 1.1 Annex F claim that they moved to 1/1, settling the trap), EndpointMetadata `base` becomes OPTIONAL (0..1) and gains `protocolVersion` (td#versionInfo), IO-Link becomes a normative §2.24.6, SNMP (`.../1/2/SNMP`, §2.24.7, no forms terms) and CAN (`.../1/2/CAN`, §2.24.8, canv_ terms) are new; AID 1.1.1 is a bug-fix re-issue of the 1.1 template files under the 1.1 semanticId and the identical 1.1 PDF — read the "AID 1.2" section.
metadata:
  type: reference
---

# AAS Asset Interfaces Description (IDTA-02017-1-1 v1.1)

The reference for describing **how to connect to an asset's live interface and its
served datapoints** — the IP/endpoint, the serialization, the security, and for
each datapoint the protocol addressing (Modbus register, HTTP path + method, MQTT
topic, OPC UA nodeId, BACnet object) — as an AAS submodel: IDTA-02017-1-1 *"Asset
Interfaces Description"* (AID), v1.1 (April 2026; v1.0 was 19.01.2024). An external
**Data Mapping Processor (DMP)** parses an AID, connects to the asset, and (guided
by a companion **AIMC** — Asset Interfaces Mapping Configuration submodel, IDTA
[20]) maps the retrieved runtime data into an operational-data submodel.

**AID 1.0/1.1 is monitoring-only.** It concentrates on *properties* (readable /
subscribable datapoints). `actions` and `events` collections exist (they carry WoT
semanticIds) but their detailed content and write/invoke are deferred to a future
AID version (§1.3, §2.6).

AID is **grounded verbatim in the W3C Web of Things Thing Description (WoT TD 1.1)**
[7]. Most element semanticIds ARE the WoT TD / json-schema / hypermedia / security
vocabulary IRIs; protocol bindings reuse the official W3C/OPC-Foundation WoT binding
vocabularies. Design decision (§1.5.3): *"the most assigned semanticId in the AID is
based on the namespace term definition of WoT TD."*

Companion to [[aas-submodel-templates]] (the template map), [[aas-knowledge]]
(metamodel), [[aas-validation]] (AASd-*), [[aasx-format]] (the OPC package side of
an ExternalDescriptor File), [[aas-security]] (the auth schemes), and [[iec61360]]
(the `valueSemantics` Ref → ConceptDescription for units/meaning).

## ⚠ MANDATORY FIRST STEP — read the bundled spec

Read the bundled official spec before authoring/reviewing any AID submodel — the
.txt always works, the PDF is authoritative (92 pages; §2.3–2.27 are the element
tables, Annex B is IO-Link, Annex C is base/href, Annex E is the WoT-TD↔AID map,
Annex F is the v1.0→v1.1 change log):

```
Read: ~/.claude/skills/aas-asset-interfaces-description/IDTA-02017-1-1_Submodel_Asset-Interfaces-Description.txt   ← always readable
      ~/.claude/skills/aas-asset-interfaces-description/IDTA-02017-1-1_Submodel_Asset-Interfaces-Description.pdf   ← authoritative
AID 1.2 (106 pages, "Version 1.2"; Annex G p.103 is the 1.1→1.2 change log):
      ~/.claude/skills/aas-asset-interfaces-description/IDTA-02017-1-2_Submodel_Asset-Interfaces-Description.txt
      ~/.claude/skills/aas-asset-interfaces-description/IDTA-02017-1-2_Submodel_Asset-Interfaces-Description.pdf
```

The 1.2 PDF is the one IDTA publishes as `published/Asset Interfaces Description/1/2/IDTA
02017_Submodel_Asset Interfaces Description.pdf` (commit `981d3f8`, merged to main by PR #336,
`f379003`, 2026-10-05); its template JSON is `…/1/2/IDTA 02017_Template_Asset Interfaces
Description.json`. Local mirror with every version's PDF/text/JSON: the `idta-pdfs` alias in
`tools/sources.json`
(`pdf/`, `txt/`, `json/` + `published/<Template>/<version>/`).

This skill was extracted **verbatim** from that .txt on 2026-07-17. Where a
semanticId is printed inconsistently or a typo is visible, it is recorded below as a
`DISCREPANCY` / `VERIFY` note rather than silently "fixed". **Do not invent
semanticIds.** The definitive machine artefact is the official AASX of the template
(Annex A says the tables "do not convey all information … the definitive definitions
are given by a separate … AASX file").

## ⚠⚠ THE #1 TRAP — version `1/1` (Submodel) vs `1/0` (everything else)

- The **Submodel** semanticId is **`https://admin-shell.io/idta/AssetInterfacesDescription/1/1/Submodel`** (version `1/1`, with the `/Submodel` suffix).
- BUT **every core structural element** is PRINTED in the §2 tables with version **`1/0`**:
  `.../1/0/Interface`, `.../1/0/EndpointMetadata`, `.../1/0/InteractionMetadata`,
  `.../1/0/ExternalDescriptor`, `.../1/0/externalDescriptorName`, `.../1/0/PropertyDefinition`,
  `.../1/0/key`, `.../1/0/minMaxRange`, `.../1/0/lengthRange`, `.../1/0/itemsRange`,
  `.../1/0/valueSemantics`.
- YET **Annex F ("Changes between version 1.0 and 1.1")** explicitly lists each of
  these as *"Changed semanticId to version 1.1."* So the change log and the element
  tables **contradict each other**.
- Only the **Submodel IRI** and the **IO-Link (informative)** IRIs use `1/1`.

**Ruling for app code:** use the *printed table values* (`1/0` for core elements,
`1/1/Submodel` for the Submodel, `1/1/IO-Link/…` for IO-Link). The Annex F rows were
the error — settled below; no `1/1` core-element ids exist in any official artefact.

**SETTLED by the 1.2 edition (2026-10-05).** The 1.2 PDF's Annex F (p.102, "Changes between version
1.0 and 1.1") keeps only *"AssetInterfacesDescription Update Submodel Changed semanticId to version
1.1"*; the eleven element rows of the 1.1 edition are gone. The 1.2 tables print every core element
with `1/0` again (Interface p.15-16, EndpointMetadata p.18-19, InteractionMetadata p.18/21,
ExternalDescriptor p.22, PropertyDefinition p.22), and the 1.0, 1.1, 1.1.1 and 1.2 template JSONs all
carry `1/0` on them (CHANGE-LIST §1.2). Core elements are `1/0` in every version; only the Submodel
semanticId moves (`1/0` → `1/1` → `1/2`).

## AID 1.2 (IDTA 02017 Version 1.2) — what changed from 1.1, verbatim with pages

Cover p.1 "Version 1.2 / May 2026"; version history p.2 "05.10.2026 1.2 Release of the official
Submodel template published by IDTA." (`VERIFY-date`: cover month and history date disagree, as in
1.1.) Annex G p.103 is the change log. Everything not listed here is unchanged from 1.1 (word diff of
the two PDFs, `aid_11_vs_12_worddiff.txt`).

| # | change | 1.2 text / value | page |
|---|---|---|---|
| 1 | Submodel semanticId | `[IRI] https://admin-shell.io/idta/AssetInterfacesDescription/1/2/Submodel` | §2.3 Table 2 p.15; Annex G "Changed semanticId to version 1.2" |
| 2 | SNMP interface IRI (new) | `[IRI] (only if SNMP is used) https://admin-shell.io/idta/AssetInterfacesDescription/1/2/SNMP` | Table 2 p.16, Table 3 p.17 |
| 3 | CAN interface IRI (new) | `[IRI] (only if CAN is used) https://admin-shell.io/idta/AssetInterfacesDescription/1/2/CAN` | Table 2 p.16, Table 3 p.17 |
| 4 | IO-Link interface IRI | unchanged `…/1/1/IO-Link`, now also in Table 2 | p.16, p.17 |
| 5 | EndpointMetadata `base` | card **0..1** (1.1: 1) — Annex G: *"Make "base" optional"* | Table 4 p.19 |
| 6 | EndpointMetadata `protocolVersion` (new) | `[Property] protocolVersion [IRI] https://www.w3.org/2019/wot/td#versionInfo` *"Used by multi-versioned protocols to indicate the specific protocol version of the interface"* `[string]` 0..1 | Table 4 p.20 |
| 7 | IO-Link | normative §2.24.6 *"Elements of IO-Link from SMC forms"* (1.1: informative Annex B) — body Tables 35-39 | p.63-68 |
| 8 | `iolv_referenceToCondition` (new) | `[Ref] …/1/1/IO-Link/referenceToCondition` *"Defined the reference to a condition that must be validated on a datapoint."* 0..1 | p.65 |
| 9 | IO-Link offsets/lengths | `[NonNegativeInteger]` (1.1: `[integer]` with examples) | p.64, p.66-67 |
| 10 | IO-Link payloadMapping item IRIs | `…/IO-Link/ByteOffset`, `…/byteLength`, `…/bitOffset`, `…/bitLength` (1.1 p.76: `…/hasByteLength`, `…/hasBitOffset`, `…/hasBitLength`) | Table 37 p.66-67 |
| 11 | IO-Link SML idShort | `iolv_payloadMapping` (1.1 Table 48: `profv_payloadMapping`) | Table 36 p.66 |
| 12 | SNMP binding §2.24.7 (new) | *"Since SNMP does not require any additional information beyond what is defined in "forms", no elements necessary for SNMP binding are defined."* SNMPv1/SNMPv2c via `protocolVersion` ("SNMPv1", "SNMPv2c"); community string *"recommended to use the "identity" property of the security scheme {psk_sc}"* | p.68 |
| 13 | CAN binding §2.24.8 (new) | *"The "base" field in "EndpointMetadata" is not used."* (p.69); Table 40 p.70 `canv_offset` `…/1/2/CAN/offset` [NonNegativeInteger] 0..1 *"Must be in the range [0, 63]"*; `canv_length` `…/1/2/CAN/length` 0..1 *"[1, 64]"*; `canv_valueOffset` `…/1/2/CAN/value-offset` [Double] 0..1; `canv_enumeratedValues` [SML] `…/1/2/CAN/hasEnumeratedValues` 0..1; `canv_payloadMapping` [SML] `…/1/2/CAN/hasPayloadMapping` 0..1 *"If this is used, "canv_length", "canv_offset", "canv_valueOffset", "canv_enumeratedValues" must not be used."* | p.69-70 |
| 14 | CAN payloadMapping item | Table 41 p.71 `<no idShort>` [SMC] `…/1/2/CAN/payloadMapping` 1..*; Table 42 p.71-72 `canv_referenceToProperty` [Ref] `…/1/2/CAN/referenceToProperty` **1**, `canv_offset` [integer] **1**, `canv_length` [integer] **1**, `canv_valueOffset` [Double] 0..1, `canv_enumeratedValues` [SML] 0..1 | p.71-72 |
| 15 | CAN enumeratedValues item | Table 43 p.72 `<no idShort>` [SMC] `…/1/2/CAN/enumeratedValue` 1..*; Table 44 p.73 `canv_encodedPayload` `…/1/2/CAN/encodedPayload` integer 1, `canv_decodedPayload` `…/1/2/CAN/decodedPayload` String 1 | p.72-73 |
| 16 | base patterns (Annex B Table 57) | SNMP `snmp://{address}:{port}` (*"Default is 161 for snmpget and snmpset or 162 for snmptrap"*); CAN `can://` | p.86-87 |
| 17 | href patterns (Annex B Table 58) | SNMP `{oid}` (*"recommended using OIDs pointing to single values and not to tables"*, e.g. `1.3.6.1.2.1.1.1.0`); CAN `{identifier}` *"a 29 bit hexadecimal value … Must be in the range of [0x00000000 , 0x1fffffff]"*, e.g. `0x1f2b3a00`; IO-Link PROFINET parameters now "in decimal" | p.87-89 |
| 18 | security reference table | Table 56 is now *"Reference Element for allOf, oneOf SML"*, idShort `allOf | oneOf`; the 1.1 row giving the `security` SML the IRI `…/OPCUASecurityAuthenticationScheme` is gone (fixes 1.1 DISCREPANCY "Table 46") | p.84 |
| 19 | `opcua_channel_sc.uav_securityPolicy` | the stray `https://www.w3.org/2019/wot/security` of 1.1 p.69 is gone | Table 54 p.82 |
| 20 | number schema `type` example | `number` (1.1: `float`) | Table 10 p.28 |
| 21 | WoT registry entries (new Annex E) | SNMP binding (`snmpv:pduType` GetRequestPDU/SetRequestPDU, `snmpv:version` SNMPv1/SNMPv2c) and CAN binding for the W3C WoT registry — WoT TD terms, **not** AID submodel elements | p.96-101 |

Template JSON 1.1.1 → 1.2 (machine evidence; the PDF stays the law): 8 example interfaces
(`InterfaceTemplateForSNMP`, `InterfaceTemplateForCAN` added); Interface card OneToMany; OPC UA and
BACnet example interfaces finally carry their own protocol IRI (they carried MQTT's in 1.0-1.1.1);
`base` and EndpointMetadata `contentType` ZeroToOne, `base` xs:string; `protocolVersion` on every
interface; security-SML items (EndpointMetadata and forms) now `td#definesSecurityScheme` (1.1 JSON:
`td#hasSecurityConfiguration`; the 1.2 PDF prints no item semanticId in Table 45 — `VERIFY-securityItem`);
`htv_methodName` One; `enum` SML REMOVED from every datapoint (the PDF Tables 8-21 still list it, 0..1 —
`DISCREPANCY-enum`); nested `{property_name}` loses `observable` (matches §2.17) and its `properties`
becomes `json-schema#properties` (was `#propertyName`); `const` xs:string; lengthRange/itemsRange
xs:unsignedInt; `iolv_accessRigths` typo fixed; IO-Link item IRIs move from
`http://www.w3.org/2022/wot/iolink#…` to `…/1/1/IO-Link/…`. Qualifiers: the 1.2 JSON reverts the
1.1.1 TemplateQualifier change — all 1200 qualifiers are `kind: ConceptQualifier` again, and the
cardinality qualifier `type` is now `SMT/Cardinality` (1.1/1.1.1: `Cardinality`).

### 1.2 DISCREPANCY / VERIFY (recorded, not fixed)
- `VERIFY-ioLinkStatus`: Table 3 p.17 still says *"Note: The IO-Link IRI is informative and may be
  changed to a normative IRI value in a future version of AID"* and Table 58 p.88-89 labels IO-Link
  "(informative)", while Annex G and the README make it the normative §2.24.6.
- `DISCREPANCY-citation21`: §2.26 p.74 *"More details about UA security definitions can be found in
  [21]"* and §1.4 cites OPC UA as "[13] [21]", but the 1.2 bibliography p.105 makes [21] IETF RFC 3411
  (SNMP); in 1.1 [21] was OPC 10101.
- `DISCREPANCY-parents`: Table 39 p.68 gives the IO-Link enumeratedValue item's parent as
  "iolv_payloadMapping SML"; Table 44 p.73 gives the CAN one as "canv_payloadMapping SML". Both are the
  `*_enumeratedValues` SML.
- `DISCREPANCY-ioLinkCasing` persists in part: Table 37 p.66 `…/IO-Link/ByteOffset` (capital B) vs
  Table 35 p.64 `…/byteOffset`.
- Still present from 1.1: `EndpointMaetadata` (Table 3 p.18), `hasTarget.` trailing dot (Table 22 p.50),
  BACnet `hasValueMap` vs `hasMapEntry` (Tables 33/34 p.62).
- Stale list of tables p.6-7 (security tables listed as 35-46, body 45-56; IO-Link listed 47-51, body
  35-39; CAN Tables 40-44 missing); "Error! Bookmark not defined." p.5, "Error! Reference source not
  found." p.63/67/72; Annex G typos "Section 2.264.8", "canv_paloadMapping", "canv_enumaratedValues", and
  it lists the IO-Link terms as "New" although 1.1 had them (informative).

## AID 1.1.1 (bug-fix release, folder `1/1/1`)
README: *"It builds on version 1.1; the artifacts of 1.1 are unchanged."* The PDF in `1/1/1` is
byte-identical to 1.1's (sha1 `f19e00ec…`). Its JSON keeps `…/1/1/Submodel`; it only changes 743
qualifier kinds ConceptQualifier→TemplateQualifier, removes the idShort of the 22 SML items
(AASd-120) and two trailing spaces in OPC UA IRIs (issues #187, #207, #208, #210). For every rule,
AID 1.1.1 IS AID 1.1. (The TemplateQualifier change did not survive: the 1.2 JSON is
ConceptQualifier throughout.)

## Recognising the version
By the Submodel semanticId only, against what each edition's §2.3 Table 2 prints: 1.0 `…/1/0/Submodel`
(1.0 p.13), 1.1 `…/1/1/Submodel` (1.1 p.14), 1.2 `…/1/2/Submodel` (1.2 p.15). Never by a list of
"accepted strings", never by the catalogue folder name (1.1.1 is 1.1). EndpointMetadata `base` is
mandatory in 1.0 (p.16) and 1.1 (p.17), optional in 1.2 (p.19). Protocols by version: 1.0 Modbus/MQTT/
HTTP (Table 2 p.13); 1.1 adds OPC UA, BACnet, IO-Link (informative); 1.2 adds SNMP and CAN.

## Namespace prefixes (used throughout the tree)

| short | full base | who defines it |
|---|---|---|
| `AID` | `https://admin-shell.io/idta/AssetInterfacesDescription` | IDTA (this template) |
| `td` | `https://www.w3.org/2019/wot/td#` | W3C WoT Thing Description |
| `jsc` | `https://www.w3.org/2019/wot/json-schema#` | W3C WoT JSON Schema |
| `hym` | `https://www.w3.org/2019/wot/hypermedia#` | W3C WoT Hypermedia |
| `sec` | `https://www.w3.org/2019/wot/security#` | W3C WoT Security |
| `htv` | `https://www.w3.org/2011/http#` | W3C HTTP-in-RDF |
| `modv` | `https://www.w3.org/2019/wot/modbus#` | W3C WoT Modbus binding |
| `mqv` | `https://www.w3.org/2019/wot/mqtt#` | W3C WoT MQTT binding |
| `bacv` | `http://www.w3.org/2022/bacnet#` | W3C WoT BACnet binding |
| `uav` | `http://opcfoundation.org/UA/WoT-Binding/` | OPC Foundation (OPC 10101) |
| `iolv` | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/` | IDTA (informative) |
| `rdf` | `https://www.w3.org/1999/02/22-rdf-syntax-ns#` | W3C RDF (only `type`) |
| `dct` | `http://purl.org/dc/terms/` | Dublin Core (created/modified) |
| `schema` | `https://schema.org/` | schema.org (only `unitCode`) |

**Protocol-tag convention (§2.24):** every protocol-specific idShort is prefixed to
avoid collisions — `htv_` HTTP, `modv_` Modbus, `mqv_` MQTT, `uav_` OPC UA, `bacv_`
BACnet, `iolv_` IO-Link. Element idShorts follow the standard names in each protocol
spec.

## Structure tree (verbatim, §2.3–2.27)

Submodel `AssetInterfacesDescription` (a different idShort may be used if unique).
Legend: ● = mandatory (card 1 / 1..*). Cardinalities are the spec's "card." column.
`__00__` = a 2-digit uniqueness suffix (per Annex A). SMC = SubmodelElementCollection,
SML = SubmodelElementList, Prop = Property, Ref = ReferenceElement.

```
Submodel  idShort=AssetInterfacesDescription   semanticId → AID/1/1/Submodel
 └─[SMC] Interface__00__ ●  1..*     AID/1/0/Interface   (+ suppl = the WoT Thing td, + protocol suppl)
     ├─[Prop] title ●               td#title                         [string]
     ├─[Prop] created  0..1         dct/created                      [string]
     ├─[Prop] modified 0..1         dct/modified                     [string]
     ├─[Prop] support  0..1         td#supportContact                [string]
     ├─[SMC] EndpointMetadata  "1 or 0..1"   AID/1/0/EndpointMetadata      (§2.5)
     │    ├─[Prop] base ●            td#baseURI                      [string]  e.g. modbus+tcp://192.168.99.159:502/
     │    ├─[Prop] contentType 0..1  hym#forContentType              [string]  e.g. application/json
     │    ├─[SML]  security ●        td#hasSecurityConfiguration     → Refs into securityDefinitions
     │    ├─[Prop] modv_mostSignificantByte 0..1  modv#hasMostSignificantByte  [boolean]  (Modbus only)
     │    ├─[Prop] modv_mostSignificantWord 0..1  modv#hasMostSignificantWord  [boolean]  (Modbus only)
     │    └─[SMC]  securityDefinitions ●   td#definesSecurityScheme        (§2.26)
     │              └─[SMC] {SecurityScheme}  1..*   (nosec_sc|basic_sc|… — semanticId per scheme, §2.27)
     ├─[SMC] InteractionMetadata  "1 or 0..1"   AID/1/0/InteractionMetadata  (suppl td#InteractionAffordance) (§2.6)
     │    ├─[SMC] properties 0..1   td#PropertyAffordance            (§2.8 — the datapoints)
     │    │    └─[SMC] {property_name}  0..*   AID/1/0/PropertyDefinition (suppl td#name)   (§2.9–2.14)
     │    │         ├─[Prop] key 0..1          AID/1/0/key            [string]  (when idShort can't be the real key)
     │    │         ├─[Prop] title 0..1        td#title               [string]
     │    │         ├─[Prop] observable 0..1   td#isObservable        [boolean] (MQTT: set true)
     │    │         ├─[SMC]  forms ●  (card 1) td#hasForm             (§2.23 — addressing; ONLY at top level)
     │    │         ├─[Prop] type 0..1         rdf#type               [string]  object|array|string|number|integer|boolean|null
     │    │         ├─[Prop] const 0..1        jsc#const
     │    │         ├─[SML]  enum 0..1         jsc#enum               [list of Property<string>]
     │    │         ├─[Prop] default 0..1      jsc#default
     │    │         ├─[Prop] unit 0..1         schema/unitCode        [string]
     │    │         ├─[Range] min_max 0..1     AID/1/0/minMaxRange    (suppl jsc#minimum / jsc#maximum) integer|number
     │    │         ├─[Range] lengthRange 0..1 AID/1/0/lengthRange    (suppl jsc#minLength / jsc#maxLength) string
     │    │         ├─[SMC]  items 0..1        jsc#items              (array — schema of the element, §2.15)
     │    │         ├─[Range] itemsRange 0..1  AID/1/0/itemsRange     (suppl jsc#minItems / jsc#maxItems) array
     │    │         ├─[Ref]  valueSemantics 0..1  AID/1/0/valueSemantics  → ConceptDescription
     │    │         ├─[SMC]  properties 0..1   jsc#properties         (object → nested, §2.16)
     │    │         └─[SMC]  uriVariables 0..1 td#hasUriTemplateSchema (RFC6570, §2.15)
     │    ├─[SMC] actions 0..1      td#ActionAffordance              (declared; detail out of scope in 1.1)
     │    └─[SMC] events  0..1      td#EventAffordance               (declared; detail out of scope in 1.1)
     └─[SMC] ExternalDescriptor 0..1   AID/1/0/ExternalDescriptor    (§2.7)
          └─[File] {descriptorName} 1..*   AID/1/0/externalDescriptorName   e.g. ./sensor_device.td.jsonld, ./gsdml-v21-ed2.xml
```

`forms` is the addressing heart — it is **mandatory (card 1)** on every top-level
`{property_name}` and is extended per protocol (see the binding tables). `forms` is
**only at the top level** — nested object members carry NO `forms`.

## Core element semanticId tables (verbatim)

### Submodel `AssetInterfacesDescription` (§2.3, Table 2)
- idShort: `AssetInterfacesDescription` (*"a different idShort might be used, as long as it is unique in the Submodel"*).
- semanticId: `[IRI] https://admin-shell.io/idta/AssetInterfacesDescription/1/1/Submodel`
- Child: `Interface__00__` [SMC] card **1..\*** (at least one interface).

### `Interface__00__` (§2.4, Table 3)
- semanticId: `[IRI] https://admin-shell.io/idta/AssetInterfacesDescription/1/0/Interface`
- **supplementalSemanticId** = ALWAYS the WoT Thing `https://www.w3.org/2019/wot/td`
  PLUS one protocol IRI (the interface's protocol is indicated *by its semanticId*):

  | protocol | supplementalSemanticId (verbatim) |
  |---|---|
  | Modbus | `http://www.w3.org/2011/modbus` |
  | MQTT | `http://www.w3.org/2011/mqtt` |
  | HTTP | `http://www.w3.org/2011/http` |
  | BACnet | `http://www.w3.org/2022/bacnet` |
  | OPC UA | `http://opcfoundation.org/UA/WoT-Binding/` |
  | IO-Link (informative) | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link` |

  Note: *"The IO-Link IRI is informative and may be changed to a normative IRI value
  in a future version of AID."* For a protocol not yet covered, use only
  `ExternalDescriptor` and add an appropriate `supplementalSemanticId` to identify
  the interface's purpose.
- Children: `title` ● (`td#title`), `created` 0..1 (`dct/created`), `modified` 0..1
  (`dct/modified`), `support` 0..1 (`td#supportContact`), `EndpointMetadata`,
  `InteractionMetadata`, `ExternalDescriptor`.

### `EndpointMetadata` (§2.5, Table 4)
- semanticId: `[IRI] https://admin-shell.io/idta/AssetInterfacesDescription/1/0/EndpointMetadata`
- card in the Interface table is printed as **"1 or 0..1"** (mandatory UNLESS an
  ExternalDescriptor description file is provided — see §1.5.3 design decision).

  | SME | idShort | semanticId | valueType | card |
  |---|---|---|---|---|
  | Prop | base | `td#baseURI` (`https://www.w3.org/2019/wot/td#baseURI`) | string | 1 ● |
  | Prop | contentType | `hym#forContentType` (`https://www.w3.org/2019/wot/hypermedia#forContentType`) | string | 0..1 |
  | SML | security | `td#hasSecurityConfiguration` (`https://www.w3.org/2019/wot/td#hasSecurityConfiguration`) | — | 1 ● |
  | Prop | modv_mostSignificantByte | `https://www.w3.org/2019/wot/modbus#hasMostSignificantByte` | boolean | 0..1 |
  | Prop | modv_mostSignificantWord | `https://www.w3.org/2019/wot/modbus#hasMostSignificantWord` | boolean | 0..1 |
  | SMC | securityDefinitions | `td#definesSecurityScheme` (`https://www.w3.org/2019/wot/td#definesSecurityScheme`) | — | 1 ● |

  `contentType` here is the **global** default; a `forms`-level `contentType`
  overrides it locally. Even a no-security interface should list a `nosec_sc` entry.

### `InteractionMetadata` (§2.6, Table 5)
- semanticId: `[IRI] https://admin-shell.io/idta/AssetInterfacesDescription/1/0/InteractionMetadata`
- supplementalSemanticId: `[IRI] https://www.w3.org/2019/wot/td#InteractionAffordance`
- card printed as **"1 or 0..1"** (same rule as EndpointMetadata).

  | SME | idShort | semanticId | card |
  |---|---|---|---|
  | SMC | properties | `https://www.w3.org/2019/wot/td#PropertyAffordance` | 0..1 |
  | SMC | actions | `https://www.w3.org/2019/wot/td#ActionAffordance` | 0..1 |
  | SMC | events | `https://www.w3.org/2019/wot/td#EventAffordance` | 0..1 |

### `ExternalDescriptor` (§2.7, Table 6)
- semanticId: `[IRI] https://admin-shell.io/idta/AssetInterfacesDescription/1/0/ExternalDescriptor`
- Child `{descriptorName}` [File] card **1..\***, semanticId
  `[IRI] https://admin-shell.io/idta/AssetInterfacesDescription/1/0/externalDescriptorName`.
  Value is a File ref (in-AASX or external URL) to a Thing Description, GSDML, MTP, IODD, etc.

### `properties` (§2.8, Table 7)
- semanticId: `[IRI] https://www.w3.org/2019/wot/td#hasPropertyAffordance`
- Child `{property_name}` [SMC] card **0..\***, semanticId
  `[IRI] https://admin-shell.io/idta/AssetInterfacesDescription/1/0/PropertyDefinition`,
  supplementalSemanticId `[IRI] https://www.w3.org/2019/wot/td#name`.

## Datapoint schema — `{property_name}` (§2.9–2.14) — the field catalogue

Every top-level `{property_name}` SMC has semanticId `AID/1/0/PropertyDefinition`
(suppl `td#name`) regardless of its schema type. The **`type` Property** (`rdf#type`,
value one of `object|array|string|number|integer|boolean|null`) picks the schema.
The full field set and which schema uses which:

| SME | idShort | semanticId (verbatim) | valueType | boolean | integer | number | string | array | object |
|---|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|
| Prop | key | `https://admin-shell.io/idta/AssetInterfacesDescription/1/0/key` | string | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Prop | title | `https://www.w3.org/2019/wot/td#title` | string | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Prop | observable | `https://www.w3.org/2019/wot/td#isObservable` | boolean | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SMC | **forms ●** | `https://www.w3.org/2019/wot/td#hasForm` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Prop | type | `https://www.w3.org/1999/02/22-rdf-syntax-ns#type` | string | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Prop | const | `https://www.w3.org/2019/wot/json-schema#const` | string | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SML | enum | `https://www.w3.org/2019/wot/json-schema#enum` | list<Prop string> | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Prop | default | `https://www.w3.org/2019/wot/json-schema#default` | boolean* | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Prop | unit | `https://schema.org/unitCode` | string | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Range | min_max | `https://admin-shell.io/idta/AssetInterfacesDescription/1/0/minMaxRange` (suppl `jsc#minimum`/`jsc#maximum`) | integer\|float | ✓ | ✓ | ✓ | – | – | – |
| Range | lengthRange | `https://admin-shell.io/idta/AssetInterfacesDescription/1/0/lengthRange` (suppl `jsc#minLength`/`jsc#maxLength`) | unsignedInt | ✓ | – | – | ✓ | – | – |
| SMC | items | `https://www.w3.org/2019/wot/json-schema#items` | — | ✓ | – | – | – | ✓ | – |
| Range | itemsRange | `https://admin-shell.io/idta/AssetInterfacesDescription/1/0/itemsRange` (suppl `jsc#minItems`/`jsc#maxItems`) | unsignedInt | ✓ | – | – | – | ✓ | – |
| Ref | valueSemantics | `https://admin-shell.io/idta/AssetInterfacesDescription/1/0/valueSemantics` | Ref→CD | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| SMC | properties | `https://www.w3.org/2019/wot/json-schema#properties` | — | ✓ | – | – | – | – | ✓ |
| SMC | uriVariables | `https://www.w3.org/2019/wot/td#hasUriTemplateSchema` | — | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

*`default`'s valueType should equal the datapoint's `type` (the "boolean" cell is
just the spec's example). All rows above except `forms` are card **0..1**; `forms`
is card **1 ●**. The **Boolean table (Table 8)** is the superset — it lists every
field; integer/number/string/array/object tables list only the subset marked ✓.

- `type` value = `float` is used for the *number* schema (the `[valueType]` example
  in §2.11/§2.19 prints `float`, not `number`).
- `min_max`: when `type=number` the Range datatype must be float; when `type=integer`
  it must be integer.
- `valueSemantics` → a ReferenceElement to a ConceptDescription giving the runtime
  value's meaning/unit ([[iec61360]]).

### `uriVariables` / `items` element (§2.15, Table 14)
Both are SMCs describing a data schema. semanticId: **for `items`**
`https://www.w3.org/2019/wot/json-schema#items`; **for `uriVariables`**
`https://www.w3.org/2019/wot/td#hasUriTemplateSchema`. Fields: `type` (value may be
`anyOf` / boolean / float / integer / array / object), `const`, `enum`, `default`,
`unit`, `valueSemantics`, `uriVariables`. (No `forms`, no `key`, no `title`.)

### Nested `properties` (object schema) — §2.16–2.22
For `type=object`, the `properties` SMC (semanticId
`https://www.w3.org/2019/wot/json-schema#properties`, §2.16 Table 15) holds nested
`{property_name}` SMCs whose semanticId is **`https://www.w3.org/2019/wot/json-schema#propertyName`**
(NOT `PropertyDefinition`), card **1..\***. Each nested `{property_name}` is *almost
identical* to a top-level one **except it has NO `forms` and NO `observable`** (§2.17
note). Nested fields carry the same `AID/1/0/…` and `jsc#…` semanticIds as the
top-level catalogue above (key/title/type/const/enum/default/unit/min_max/lengthRange/
items/itemsRange/valueSemantics/properties/uriVariables per schema type).

## `forms` — the addressing SMC (§2.23, Table 22)

semanticId `https://www.w3.org/2019/wot/td#hasForm`. Common terms (all protocols):

| SME | idShort | semanticId (verbatim) | valueType | card |
|---|---|---|---|---|
| Prop | contentType | `https://www.w3.org/2019/wot/hypermedia#forContentType` | string | 0..1 |
| Prop | **href ●** | `https://www.w3.org/2019/wot/hypermedia#hasTarget` | string | **1 ●** |
| Prop | subprotocol | `https://www.w3.org/2019/wot/hypermedia#forSubProtocol` | string | 0..1 |
| SML | security | `https://www.w3.org/2019/wot/td#hasSecurityConfiguration` | — | 0..1 |

`href` (card 1, mandatory) is a full IRI or a path **relative to `base`** in
EndpointMetadata (base `http://example.com` + href `/datapoint1` →
`http://example.com/datapoint1`). Per-protocol href/base syntax is in **Annex C**:

| protocol | base pattern | href pattern (example) |
|---|---|---|
| HTTP | `http(s)://{address}:{port}/` | `properties/voltage` or full URL |
| Modbus | `modbus+tcp://{address}:{port}/{unitID}/` | `{address}?quantity={quantity}` e.g. `40089?quantity=2` |
| MQTT | `mqtt(s)://{broker address}:{port}/` | `{topic}` (wildcards `#`→`%23`; leading `/`→`.//`) |
| OPC UA | `opc.tcp://<address>:<port>[/<resourcePath>]` | `/?id=<nodeId>` (`#`→`%23`, `&`→`%26`) |
| BACnet | `bacnet://{deviceId}` | `/object-type,object-instance/property-identifier[/array-index]` e.g. `/0,1/85` |
| IO-Link (inf.) | `iolink.http://{address}` or `iolink.profinet://{address}` | REST `{base-path}/{resource-path}`; PROFINET slot/subslot query |

`subprotocol` names the exact mechanism when several exist (e.g. `longpoll`,
`websub`, `sse`). `contentType` here overrides the EndpointMetadata global.

## Protocol bindings — `forms` extensions (§2.24)

`forms` is extended in-place (no new wrapper SMC) with the protocol's terms. The
binding tables have `idShort/Class/semanticId/Parent = "-"` because they are just
extra members of the `forms` SMC.

### HTTP (§2.24.1, Tables 23–25) — prefix `htv_`
| SME | idShort | semanticId | card |
|---|---|---|---|
| Prop | htv_methodName | `https://www.w3.org/2011/http#methodName` | 1 ● |
| SML | htv_headers | `https://www.w3.org/2011/http#headers` | 0..1 |

`htv_headers` SML → `<no idShort>` [SMC] (semanticId `https://www.w3.org/2011/http#headers`,
card 1..*, idShort omitted per AASd-120) → `htv_fieldName` [Prop]
`https://www.w3.org/2011/http#fieldName` (card 1) + `htv_fieldValue` [Prop]
`https://www.w3.org/2011/http#fieldValue` (card 1). HTTP methods (Table 60):
`GET`, `PUT`, `POST`, `DELETE`, `PATCH`.

### Modbus (§2.24.2, Table 26) — prefix `modv_`
| SME | idShort | semanticId | valueType | card | value list |
|---|---|---|---|---|---|
| Prop | modv_function | `https://www.w3.org/2019/wot/modbus#hasFunction` | string | 0..1 | readCoil, readDeviceIdentification, readDiscreteInput, readHoldingRegisters, readInputRegisters, writeMultipleCoils, writeMultipleHoldingRegisters, writeSingleCoil, writeSingleHoldingRegister |
| Prop | modv_entity | `https://www.w3.org/2019/wot/modbus#hasEntity` | string | 0..1 | Coil, DiscreteInput, HoldingRegister, InputRegister |
| Prop | modv_zeroBasedAddressing | `https://www.w3.org/2019/wot/modbus#hasZeroBasedAddressingFlag` | boolean | 0..1 | |
| Prop | modv_pollingTime | `https://www.w3.org/2019/wot/modbus#hasPollingTime` | integer (ms) | 0..1 | |
| Prop | modv_timeout | `https://www.w3.org/2019/wot/modbus#hasTimeout` | integer (ms) | 0..1 | |
| Prop | modv_type | `https://www.w3.org/2019/wot/modbus#hasPayloadDataType` | string | 0..1 | xsd:float, xs:short, xs:unsignedInt, xs:string, xs:byte, xs:int, xs:boolean, xs:integer, xs:double, xs:hexbinary, xs:decimal, xs:long, xs:unsignedbyte, xs:unsignedshort, xs:unsignedint, xs:unsignedlong |
| Prop | modv_mostSignificantByte | `https://www.w3.org/2019/wot/modbus#hasMostSignificantByte` | boolean | 0..1 | (overrides EndpointMetadata global) |
| Prop | modv_mostSignificantWord | `https://www.w3.org/2019/wot/modbus#hasMostSignificantWord` | boolean | 0..1 | (overrides EndpointMetadata global) |

### MQTT (§2.24.3, Table 27) — prefix `mqv_`
| SME | idShort | semanticId | valueType | card | value list |
|---|---|---|---|---|---|
| Prop | mqv_retain | `https://www.w3.org/2019/wot/mqtt#hasRetainFlag` | boolean | 0..1 | |
| Prop | mqv_controlPacket | `https://www.w3.org/2019/wot/mqtt#ControlPacket` | string | 0..1 | subscribe, publish, unsubscribe |
| Prop | mqv_qos | `https://www.w3.org/2019/wot/mqtt#hasQoSFlag` | string | 0..1 | 0=atMostOnce (default), 1=atLeastOnce, 2=exactlyOnce |

Recommendation: set `observable=true` on any MQTT property.

### OPC UA (§2.24.4, Table 28) — prefix `uav_`
| SME | idShort | semanticId | valueType | card |
|---|---|---|---|---|
| Prop | uav_browsePath | `http://opcfoundation.org/UA/WoT-Binding/browsePath` | String | 0..1 |

(e.g. `/Root/Object/Machine1/1:Pressure`.)

### BACnet (§2.24.5, Tables 29–34) — prefix `bacv_`
| SME | idShort | semanticId | card | notes |
|---|---|---|---|---|
| Prop | bacv_useService | `http://www.w3.org/2022/bacnet#usesService` | 0..1 | ReadProperty, WriteProperty, SubscribeCOV, GetEventInfo, AcknowledgeAlarm, AddListElement, RemoveListElement |
| SMC | bacv_hasDataType | `http://www.w3.org/2022/bacnet#hasDataType` | 0..1 | + suppl = ONE BACnet datatype IRI (see below) |

`bacv_hasDataType` SMC (Table 30):
| SME | idShort | semanticId | valueType | card |
|---|---|---|---|---|
| Prop | bacv_isISO8601 | `http://www.w3.org/2022/bacnet#isIso8601` | boolean | 0..1 |
| Prop | bacv_hasBinaryRepresentation | `http://www.w3.org/2022/bacnet#hasBinaryRepresentation` | string (dotted-decimal, base64) | 0..1 |
| SMC | bacv_hasMember | `http://www.w3.org/2022/bacnet#hasMember` | — | 0..1 |
| SML | bacv_hasNamedMember | `http://www.w3.org/2022/bacnet#hasNamedMember` | — | 0..1 |
| SML | bacv_hasValueMap | `http://www.w3.org/2022/bacnet#hasValueMap` | — | 0..1 |

- `bacv_hasNamedMember` SML → `<no idShort>` [SMC] `http://www.w3.org/2022/bacnet#NamedMember`
  (card 1..*) → `bacv_hasFieldName` [Prop] `http://www.w3.org/2022/bacnet#hasfieldName`
  (card 1), `bacv_hasContextTag` [Prop] `http://www.w3.org/2022/bacnet#hasContextTag`
  (boolean, 0..1), `bacv_hasDataType` [SMC] `http://www.w3.org/2022/bacnet#hasDataType` (0..1, recursive).
- `bacv_hasValueMap` SML → `<no idShort>` [SMC] `http://www.w3.org/2022/bacnet#hasMapEntry`
  (Table 34; Table 33 prints the child as `…#hasValueMap` — see DISCREPANCY) →
  `bacv_hasLogicalVal` [Prop] `http://www.w3.org/2022/bacnet#hasLogicalVal`
  (string|integer|boolean, card 1) + `bacv_hasProtocolVal` [Prop]
  `http://www.w3.org/2022/bacnet#hasProtocolVal` (integer, card 1).
- **`bacv_hasDataType` supplementalSemanticId is one of** (all `http://www.w3.org/2022/bacnet#…`):
  `SequenceOf`, `Sequence`, `List`, `Choice`, `Date`, `Time`, `WeekNDay`, `Unsigned`,
  `Signed`, `Real`, `Double`, `Boolean`, `Enumerated`, `String`, `OctetString`,
  `BitString`, `Any`, `Null`, `ObjectIdentifier`.

### IO-Link (Annex B, Tables 47–51) — prefix `iolv_` — **INFORMATIVE**
IO-Link is bridged to REST/HTTP or PROFINET. **Not normative** — its IRIs use the
`1/1/IO-Link/` base and *"may be changed to a normative IRI value in a future
version."* forms extension terms:
| idShort | semanticId | card |
|---|---|---|
| iolv_method | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/hasMethod` | 0..1 |
| iolv_type | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/hasPayloadDataType` | 0..1 |
| iolv_accessRights | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/hasAccessRights` | 0..1 (RW/R/W, default R) |
| iolv_byteOffset | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/byteOffset` | 0..1 |
| iolv_byteLength | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/byteLength` | 0..1 |
| iolv_bitOffset | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/bitOffset` | 0..1 |
| iolv_bitLength | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/bitLength` | 0..1 |
| iolv_payloadMapping [SML] | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/hasPayloadMapping` | 0..1 |
| iolv_enumeratedValues [SML] | `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/IO-Link/hasEnumeratedValues` | 0..1 |

- `iolv_payloadMapping` SML → `<no idShort>` [SMC]
  `…/IO-Link/payloadMapping` (card 1..*) → `iolv_type` (`…/hasPayloadDataType`),
  `iolv_byteOffset` (`…/ByteOffset`), `iolv_byteLength` (`…/hasByteLength`),
  `iolv_bitOffset` (`…/hasBitOffset`), `iolv_bitLength` (`…/hasBitLength`),
  `iolv_referenceToProperty` [Ref] (`…/referenceToProperty`), `iolv_enumeratedValues`
  [SML] (`…/hasEnumeratedValues`). **Casing differs from the forms-level table** —
  see DISCREPANCY.
- `iolv_enumeratedValues` SML → `<no idShort>` [SMC] `…/IO-Link/enumeratedValue`
  (card 1..*) → `iolv_encodedPayload` [Prop] `…/encodedPayload` (integer|boolean,
  card 1) + `iolv_decodedPayload` [Prop] `…/decodedPayload` (String|integer, card 1).

## Security (§2.25–2.27)

### `security` SML (§2.25, Table 35)
- idShort `security`, semanticId `https://www.w3.org/2019/wot/td#hasSecurityConfiguration`.
- Parent: EndpointMetadata SMC **or** a `forms` SMC (global vs per-datapoint).
- Child `<no idShort>` [Ref] card **1..\*** — each Ref points to a `{SecurityScheme}`
  inside `securityDefinitions`. Even no-security → one Ref to a `nosec_sc`.

### `securityDefinitions` SMC (§2.26, Table 36)
- semanticId `https://www.w3.org/2019/wot/td#definesSecurityScheme`.
- Child `{SecurityScheme}` [SMC] card **1..\*** — idShort should mirror the scheme name.

### `{SecurityScheme}` SMC (§2.27, Table 37) — common members
- idShort ∈ `nosec_sc | basic_sc | digest_sc | bearer_sc | psk_sc | oauth2_sc | apikey_sc | auto_sc | combo_sc | opcua_channel_sc | opcua_authentication_sc`.
- Common: `proxy` [Prop] `https://www.w3.org/2019/wot/security#proxy` (anyURI, 0..1);
  `scheme` [Prop] `https://www.w3.org/2019/wot/security#SecurityScheme` (string, card 1)
  — value ∈ `nosec, basic, digest, bearer, psk, oauth2, apikey, combo, auto, uav_channelsec, uav_authentication_`.
- **The SMC's own semanticId is the scheme-specific IRI:**

| scheme (idShort) | {SecurityScheme} semanticId | extra members (all `sec#…` unless noted) |
|---|---|---|
| basic_sc | `https://www.w3.org/2019/wot/security#BasicSecurityScheme` | name, in |
| apikey_sc | `https://www.w3.org/2019/wot/security#APIKeySecurityScheme` | name, in |
| psk_sc | `https://www.w3.org/2019/wot/security#PSKSecurityScheme` | identity |
| digest_sc | `https://www.w3.org/2019/wot/security#DigestSecurityScheme` | name, in, qop (auth\|auth-int) |
| bearer_sc | `https://www.w3.org/2019/wot/security#BearerSecurityScheme` | name, in, authorization (anyURI), alg (e.g. ES256), format (jwt\|cwt\|jwe\|jws) |
| oauth2_sc | `https://www.w3.org/2019/wot/security#OAuth2SecurityScheme` | token (anyURI), refresh (anyURI), authorization (anyURI), scopes [SML], flow (card 1: code\|client) |
| combo_sc | `https://www.w3.org/2019/wot/security#ComboSecurityScheme` | EXACTLY ONE of oneOf [SML] / allOf [SML] (card 1 each) |
| opcua_channel_sc | `http://opcfoundation.org/UA/WoT-Binding/OPCUASecurityChannelScheme` | uav_securityMode (card 1), uav_securityPolicy (card 1) |
| opcua_authentication_sc | `http://opcfoundation.org/UA/WoT-Binding/OPCUASecurityAuthenticationScheme` | uav_userIdentityToken (card 1), uav_issueToken [Ref] |
| nosec_sc | *(no extension table; no explicit IRI printed — `VERIFY-nosec_sc`)* | — |
| auto_sc | *(no extension table; no explicit IRI printed — `VERIFY-auto_sc`)* | — |

Security-member IRIs (verbatim): `name` `…#name`, `in` `…#in` (header|query|body|cookie|auto),
`qop` `…#qop`, `identity` `…#identity`, `authorization` `…#authorization`, `alg`
`…#alg`, `format` `…#format`, `token` `…#token`, `refresh` `…#refresh`, `scopes`
`…#scopes`, `flow` `…#flow`, `oneOf` `…#oneOf`, `allOf` `…#allOf` (all under
`https://www.w3.org/2019/wot/security`).

OPC UA scheme values: `uav_securityMode` `http://opcfoundation.org/UA/WoT-Binding/securityMode`
∈ {None, Sign, SignAndEncrypt}; `uav_securityPolicy`
`http://opcfoundation.org/UA/WoT-Binding/securityPolicy` ∈ {None, Basic256Sha256,
Aes128_Sha256_RsaOaep, Aes256_Sha256_RsaPss; outdated: Basic256, Basic128Rsa15};
`uav_userIdentityToken` `http://opcfoundation.org/UA/WoT-Binding/userIdentityToken`
∈ {Anonymous, UserName, Certificate, IssuedToken}; `uav_issueToken`
`http://opcfoundation.org/UA/WoT-Binding/issueToken` [Ref].

### security / allOf / oneOf reference SML (§2.27.9, Table 46)
- idShort `security | allOf | oneOf`, Class SML.
- semanticId: **allOf** `https://www.w3.org/2019/wot/security#allOf`; **oneOf**
  `https://www.w3.org/2019/wot/security#oneOf`; **security** — printed as
  `http://opcfoundation.org/UA/WoT-Binding/OPCUASecurityAuthenticationScheme`
  (**almost certainly a copy-paste error**; Table 35 gives the security SML
  `td#hasSecurityConfiguration` — see DISCREPANCY).
- Child `<no idShort>` [Ref] `https://www.w3.org/2019/wot/td#definesSecurityScheme`, card 1..*.
- `combo_sc`: pick exactly one of `oneOf` (any one satisfies) / `allOf` (all must be
  satisfied). `nosec_sc`/`auto_sc` do NOT extend `{SecurityScheme}` (no extra members).

## WoT TD ↔ AID mapping (Annex E, Tables 54–62)

AID mirrors the WoT TD object graph: `@context`→semanticId/suppl; `id`→AID Submodel
id; `title/created/modified/support`→Interface Properties; `base`→EndpointMetadata;
`properties/actions/events`→InteractionMetadata SMCs; `forms`→inside each affordance;
`security`→security SML of Refs; `securityDefinitions`→securityDefinitions SMC. WoT
terms **not covered** by AID 1.1 are marked `EXTERNAL` — model them by referencing a
native TD via `ExternalDescriptor`: `titles`, `descriptions`, `links`, `profile`,
`schemaDefinitions`, `op`, and the json-schema terms `exclusiveMinimum`,
`exclusiveMaximum`, `multipleOf`, `oneOf` (schema), `readOnly`, `writeOnly`,
`format`, `required`, `pattern`, `contentEncoding`, `contentMediaType`. If a native
WoT TD exists, AID **recommends** referencing it (enables read-all-properties, Web
Linking, etc.).

## Key concepts

- **AID = "how to connect", not "the data".** It is the connectivity blueprint; the
  live values land elsewhere (an operational-data submodel), wired by the **AIMC**
  (IDTA Asset Interfaces Mapping Configuration [20]) and executed by an external
  **DMP**. AID does not itself hold runtime values (contrast [[aas-time-series]],
  which stores/links the actual series).
- **One AID → many interfaces.** Each protocol interface (or each endpoint) is its
  own `Interface__00__` SMC; the protocol is declared by the interface's
  supplementalSemanticId AND the presence of the WoT `Thing` id.
- **Properties are the datapoints.** A `{property_name}` = one readable/subscribable
  datapoint, typed by JSON-schema (`type`) and addressed by `forms.href` + the
  protocol prefix terms. `actions`/`events` are placeholders in 1.1.
- **EU Data Act driver (§1.5.1).** AID is one of the mechanisms to publish the
  connectivity/interface metadata an operator must provide for a connected product.
- **Optionality via ExternalDescriptor.** If a full external descriptor (TD, GSDML,
  MTP…) is supplied, EndpointMetadata & InteractionMetadata become optional (hence
  their "1 or 0..1" cardinality).

## Gotchas

- **Version split `1/1` vs `1/0` (see the trap at top).** Submodel = `1/1/Submodel`
  (1.2: `1/2/Submodel`); core elements are `1/0/…` in every version (settled by the 1.2
  edition and all template JSONs; the 1.1 Annex F rows were wrong). IO-Link = `1/1`.
- **`forms` is mandatory and top-level only.** Every top-level `{property_name}` MUST
  have exactly one `forms` (`td#hasForm`, card 1) with a mandatory `href`
  (`hypermedia#hasTarget`, card 1). **Nested object members carry NO `forms` and no
  `observable`** (their semanticId is `json-schema#propertyName`, not `PropertyDefinition`).
- **Two different `properties` SMCs.** InteractionMetadata's `properties` =
  `td#PropertyAffordance` (the datapoint list); an object datapoint's nested
  `properties` = `json-schema#properties`. Same idShort, different semanticId/level —
  a classic mix-up.
- **`{property_name}` vs `propertyName`.** Top-level datapoint SMC semanticId =
  `AID/1/0/PropertyDefinition` (suppl `td#name`); nested member SMC semanticId =
  `json-schema#propertyName`. Do not cross them.
- **Multiple interfaces = sibling SMCs, NOT an SML.** AID uses `Interface__00__`
  SMCs with card 1..* (numbered idShorts), not a SubmodelElementList. SML is used
  only for `security`, `enum`, `scopes`, `htv_headers`, `bacv_hasNamedMember`,
  `bacv_hasValueMap`, `iolv_payloadMapping`, `iolv_enumeratedValues`, `oneOf`/`allOf`.
- **`href` is relative to `base`.** A relative `href` resolves against
  EndpointMetadata `base`; a full IRI in `href` stands alone. Modbus href carries the
  register+quantity query, MQTT href is the topic, OPC UA href is `/?id=<nodeId>`,
  BACnet href is the object/property path. Get the per-protocol syntax from Annex C —
  do not hand-roll.
- **Security is by reference, always.** `security` (SML of Refs) selects; the actual
  scheme lives once in `securityDefinitions`. A `nosec_sc` entry is still required
  when there is no security. The `{SecurityScheme}` SMC's OWN semanticId is the
  scheme IRI (e.g. `security#BasicSecurityScheme`) — the `scheme` Property value
  (`basic`, `apikey`, …) is redundant-but-required metadata.
- **SML children have no idShort (AASd-120).** Every `<no idShort>` SMC under an SML
  (htv_headers, bacv_hasNamedMember/hasValueMap, iolv_*, security/oneOf/allOf) must
  omit its idShort under AAS V3 — the spec calls this out repeatedly.
- **`modv_mostSignificant{Byte,Word}` live in two places.** Globally in
  EndpointMetadata (applies to all datapoints) OR per-datapoint in `forms` (overrides
  the global). Same for `contentType` (EndpointMetadata global vs forms local).
- **`supplementalSemanticId` is misspelled everywhere in the spec text** as
  `supplementalSemandicId` / `supplimentalSemanticId` / `supplementalSem.Id`. The
  real AAS attribute is `supplementalSemanticIds` — don't propagate the typo into code.
- **Don't invent IRIs for `nosec_sc`/`auto_sc`.** The spec prints no explicit
  semanticId for these two schemes (they add no members). Flagged `VERIFY-nosec_sc` /
  `VERIFY-auto_sc` — check the official AASX before assigning one.

## DISCREPANCY / VERIFY list (verbatim-faithful, not "fixed")

- **`VERIFY-version` / DISCREPANCY (critical):** Submodel = `.../1/1/Submodel`; core
  elements printed `.../1/0/…` in §2.3–2.14 & §2.7; Annex F says all were "changed to
  version 1.1". Tables vs change-log conflict. Affects Interface, EndpointMetadata,
  InteractionMetadata, ExternalDescriptor, externalDescriptorName, PropertyDefinition,
  key, minMaxRange, lengthRange, itemsRange, valueSemantics. **SETTLED: `1/0`** (1.2 Annex F
  dropped the element rows; 1.0-1.2 template JSONs all carry `1/0` — see the trap at top).
- **DISCREPANCY `EndpointMaetadata`:** §2.4 (Interface table) prints the child's
  semanticId value as `…/1/0/EndpointMaetadata` (extra "ae"); §2.5's own header prints
  the correct `…/1/0/EndpointMetadata`. Use `EndpointMetadata`.
- **DISCREPANCY `[IRI]1https://…`:** the `min_max` rows (§2.9, 2.10, 2.11, 2.18) glue
  a stray `1` between `[IRI]` and the URL. The IRI is
  `https://admin-shell.io/idta/AssetInterfacesDescription/1/0/minMaxRange`.
- **DISCREPANCY `href` trailing dot:** §2.23 prints
  `https://www.w3.org/2019/wot/hypermedia#hasTarget.` with a trailing period. Correct
  IRI has no dot: `https://www.w3.org/2019/wot/hypermedia#hasTarget`.
- **DISCREPANCY Table 46 security-SML semanticId:** gives the `security` SML's id as
  `http://opcfoundation.org/UA/WoT-Binding/OPCUASecurityAuthenticationScheme`,
  contradicting Table 35 (`…td#hasSecurityConfiguration`). Table 35 is correct; Table
  46's value looks copy-pasted. `VERIFY-securitySML`.
- **DISCREPANCY BACnet valueMap child id:** Table 33 prints the `bacv_hasValueMap`
  SML's `<no idShort>` child as `http://www.w3.org/2022/bacnet#hasValueMap`, but Table
  34 (the detailed SMC) uses `http://www.w3.org/2022/bacnet#hasMapEntry`. Use
  `hasMapEntry`. `VERIFY-bacnetValueMap`.
- **DISCREPANCY BACnet IRI casing:** idShort `bacv_isISO8601` → IRI `…#isIso8601`
  (lower "so"); idShort `bacv_hasFieldName` → IRI `…#hasfieldName` (lower "f"). Record
  verbatim; casing is inconsistent with the idShorts.
- **DISCREPANCY IO-Link IRI casing (informative):** forms-level uses `…/IO-Link/byteOffset`,
  `…/byteLength`, `…/bitOffset`, `…/bitLength` (Table 47); the payloadMapping-level SMC
  uses `…/IO-Link/ByteOffset`, `…/hasByteLength`, `…/hasBitOffset`, `…/hasBitLength`
  (Table 49). Same concepts, different casing/`has` prefix. `VERIFY-ioLinkCasing`
  (whole IO-Link block is informative and may become normative later).
- **DISCREPANCY Table 48 idShort `profv_payloadMapping`:** the SML in Table 48 is
  titled `profv_payloadMapping` but its semanticId is `…/IO-Link/hasPayloadMapping`
  and Table 47 references it as `iolv_payloadMapping`. Read as `iolv_payloadMapping`.
- **DISCREPANCY MQTT mapping (Table 59):** Annex E maps `mqv:retain`→`modbus_retain`,
  `mqv:controlPacket`→`modbus_controlPacket`, `mqv:qos`→`modbus_qos` — copy-paste from
  the Modbus block. Normative §2.24.3 correctly uses `mqv_retain`/`mqv_controlPacket`/
  `mqv_qos`; use §2.24.3.
- **DISCREPANCY scheme value vs idShort:** §2.27 `scheme` value list has
  `uav_channelsec` and `uav_authentication_` (trailing underscore) while the SMC
  idShorts are `opcua_channel_sc` / `opcua_authentication_sc`. Table 57 uses
  `uav_channelsec` / `uav_authentication`. Naming is inconsistent. `VERIFY-schemeValue`.
- **DISCREPANCY `modv_type` list typo:** §2.24.2 prints a doubled comma
  `xs:unsignedInt,,xs:string`. Cosmetic.
- **DISCREPANCY class labels:** Table 35 labels `security` as "SubmodelList (SML)"
  (should be "SubmodelElementList"); Table 30 labels an SMC as "Submodel Element
  Collection". Cosmetic — the modelType is SML/SMC respectively.
- **Text typos (non-structural):** `InteractionAfordances` (Table 56, single f);
  `Idshort`, `sercurity`, `secrutiyScheme`, `observ-/subscribable`; `enpoint`;
  `Defauls`; `informativ`; `celcius`; "Error! Reference source not found." (Table 50).
  None affect semanticIds.
- **Future-dated header:** the bundled text prints "Version 1.1, April 2026" /
  "15.04.2026" (v1.0 = 19.01.2024). Recorded as-is.

## Sign-off checklist

1. Read the bundled IDTA-02017-1-1 PDF/txt (92 pages) — the tables here are a map.
2. Submodel: idShort `AssetInterfacesDescription` (or unique), semanticId
   `https://admin-shell.io/idta/AssetInterfacesDescription/1/1/Submodel` (version `1/1`,
   `/Submodel` suffix) — or `…/1/2/Submodel` for an AID 1.2 submodel. ≥1 `Interface__00__` (card 1..*).
3. Each `Interface__00__`: semanticId `.../1/0/Interface`, suppl = the WoT Thing
   `https://www.w3.org/2019/wot/td` + the protocol IRI; `title` (●), optional
   created/modified/support.
4. `EndpointMetadata` (unless a full `ExternalDescriptor` is given): `base` (● in 1.0/1.1; 0..1 in 1.2),
   optional `contentType`, `security` SML (●) referencing schemes, `securityDefinitions`
   SMC (●) with ≥1 `{SecurityScheme}` (a `nosec_sc` if no security).
5. `InteractionMetadata` → `properties` with `{property_name}` datapoints. Each
   datapoint: correct schema `type`, and a MANDATORY `forms` (● card 1) with a
   mandatory `href` (● card 1) + the correct protocol prefix terms (htv_/modv_/mqv_/
   uav_/bacv_/iolv_).
6. Nested object members use `json-schema#propertyName` and carry NO `forms`/`observable`.
7. SML children (security/enum/scopes/htv_headers/bacv_*/iolv_*/oneOf/allOf) omit
   idShort (AASd-120); `security` and `combo_sc.oneOf/allOf` hold Refs into
   `securityDefinitions`.
8. Every semanticId verbatim from the bundled spec — mind the `1/1`↔`1/0` split, the
   `EndpointMaetadata`/`hasTarget.`/`hasMapEntry` fixes, and do NOT invent IRIs for
   `nosec_sc`/`auto_sc`. Keep the DISCREPANCY notes with the frozen map.
9. Run [[aas-validation]] (XSD + AASd-*); ship a conformance fixture passing the
   official engine before claiming IDTA-02017 conformance.
```
