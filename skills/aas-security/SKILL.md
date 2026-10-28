---
name: aas-security
description: Asset Administration Shell security expertise. TWO distinct topics that must be kept separate. (1) IDTA-01004 Part 4 (v3.0.2, current v3.1) defines an ABAC-based Access Rule Model (DEFATTRIBUTES / DEFACLS / DEFOBJECTS / DEFFORMULAS / AccessPermissionRule, serialised in BNF or JSON Schema) consuming signed JWT bearer access tokens (RFC 7519); it leaves the authentication flow open (OAuth 2.0 / OIDC named as usable examples) and does not specify a data-bound signing format (v3.1 points to the IDTA-01002 v3.2 /$signed JWS endpoints). (2) Production auth patterns for AAS REST APIs (OAuth 2.0 / OIDC Bearer, mTLS, API keys, JWS/XMLDSig signing of content) are IETF/W3C standards adopted by AAS deployments, not specified by IDTA-01004. Use this skill when the user designs the auth layer for an AAS deployment, integrates with Keycloak / Azure AD / Okta, debugs 401/403, asks "how do I expose this submodel only to authorised partners", signs an AASX, or maps ESPR/DPP access categories onto AAS. Trigger on: IDTA-01004, AAS auth, AAS ABAC / RBAC, Access Rule Model, DEFATTRIBUTES/DEFACLS/DEFOBJECTS/DEFFORMULAS, AASX signing, mTLS for AAS, AccessControl / the removed AAS security attribute, DPP tier integration.
---

# AAS security

**Verify at source before writing anything technical about IDTA-01004.** The official PDFs
of v3.0.2 and v3.1 (current, July 2026) are vendored at `idta-specs:pdf/IDTA-01004-3-0-2_…pdf`
and `idta-specs:pdf/IDTA-01004-3-1_…pdf` with paged text in `idta-specs:txt/` (sha256 in
`VERSION.json`); the HTML is at `industrialdigitaltwin.io/aas-specifications/IDTA-01004/`. This skill was rewritten
on 2026-07-10 after the previous version conflated IDTA-01004 with production auth
patterns. If you're about to publish a claim about IDTA-01004, WebFetch the spec section
first and cite it inline.

Two distinct topics travel under "AAS security". Keep them separate:

1. **IDTA-01004 Part 4 (Security)** — the AAS-native Access Rule Model (ABAC-based).
2. **Production auth for the AAS REST API** — IETF/W3C standards deployments actually use.

Conflating the two is how "IDTA-01004 defines OAuth / mTLS / RBAC" gets published as a
claim. It doesn't.

---

## 1. What IDTA-01004 actually defines (v3.0.2 and v3.1)

The AAS Access Rule Model is an **Attribute Based Access Control (ABAC)** model. Direct
quote from the "Explanation of the Access Rule Model BNF → General" section of the spec
(v3.0.2 p.40, v3.1 p.55):

> "The AAS Access Rule Model uses Attribute Based Access Control (ABAC), i.e. Attributes
> are used in access rules. By ABAC also Role Based Access Control (RBAC) can be
> implemented by defining role attributes."

### Vocabulary (normative primitives)

- **Attributes**, three flavours:
  - `CLAIM` — from an external Identity Provider's access token
  - `GLOBAL` — request context (time, IP, other environmental facts)
  - `REFERENCE` — drawn from the AAS content itself
- **DEFATTRIBUTES** — named groups of attributes for reuse
- **DEFACLS** — named ACLs binding attribute expressions to rights: `CREATE`, `READ`,
  `UPDATE`, `DELETE`, `EXECUTE`, `VIEW`, `ALL`
- **DEFOBJECTS** — named groups of protected objects: `ROUTE`, `IDENTIFIABLE`,
  `REFERABLE`, `FRAGMENT`, `DESCRIPTOR`
- **DEFFORMULAS** — named boolean expressions that gate rule activation
- **AccessPermissionRule** — composes an ACL, an Object group, and (optionally) a Formula
  into a single normative rule

Verified in the v3.1 BNF (p.48): *`<Right> ::= "CREATE" | "READ" | "UPDATE" | "DELETE" |
"EXECUTE" | "VIEW" | "ALL"`*; object kinds `"ROUTE"`, `"IDENTIFIABLE"` (`$aas` | `$sm` |
`$cd`), `"REFERABLE"` (`$sme`), `"FRAGMENT"`, `"DESCRIPTOR"` (`$aasdesc` | `$smdesc`);
attributes `"CLAIM"`, `"GLOBAL"`, `"REFERENCE"`. The same grammar is shared with the
IDTA-01002 Query Language.

### Serialisation (both normative)

- **BNF grammar** (validated against BNF Playground)
- **JSON Schema** (with pattern validation)

Both representations express identical logic.

### What IDTA-01004 fixes about tokens, and what it leaves open

- **Access tokens: signed JWT bearer tokens.** v3.1 p.46 (same text v3.0.2 p.32): *"AAS
  Security uses signed JWT (JSON Web Token) bearer tokens as Access Tokens, as they are
  defined in RFC 7519."* (This skill said "JWT is not specified in IDTA-01004" until
  2026-10-28; that was wrong.)
- **Authentication flow: open.** v3.1 p.26 (v3.0.2 p.27): *"AAS Security supports any
  authentication flow which provides signed JSON Web Tokens. Even other formats for Access
  Tokens might be used."* and *"Authentication flows like OAUTH 2.0 or OIDC can be used."*
  OAuth 2.0 Client Credentials and OpenID Connect appear as example flows, not as
  requirements. mTLS and X.509 client auth are not specified.
- **Content signing: not native.** v3.1 p.124: *"This document does not specify a native way
  to protect AAS elements with data-bound protection mechanisms such as digital
  signatures."* It points to the API instead: *"…using the /$signed endpoint (IDTA 01002
  [2])"*, and p.126: *"Signing of Identifiables is defined in the REST API specification. …
  Currently plain JWS (JSON Web Signature) is used for signing, which MAY be extended to
  additional formats e.g. JAdES"*. v3.0.2 p.9 only says *"Signatures will be defined in a
  later version of this document."* So: JWS signing of shells / submodels / concept
  descriptions is IDTA-01002 v3.2 (`/$signed`, RS256, embedded payload, `x5c`; IDTA-01002 v3.2 p.77), not IDTA-01004; XMLDSig / XAdES / detached signatures remain deployment
  choices.

### Relationship to the AAS metamodel

**No AAS or Submodel in the 3.x metamodel carries an `AccessControl` / `security`
attribute.** IDTA-01001 v3.0: "REMOVED: Security attribute removed from Asset
Administration Shell, Access Control remains part of the specification" (PDF p.152);
Table 19 (p.171): `AssetAdministrationShell/security` Removed — "the Asset Administration
Shell and its elements are referenced from Security", not the other way round.
aas-core-meta v3.0, v3.1 and v3.2 contain no AccessControl class at all. Access rules live
outside the AAS content (IDTA-01004's Access Rule Model, or the server), and point AT
shells / submodels / elements.

What the V3.0 security-part change log (Part 1 Annex, PDF pp.181-182, 204, 209) also records:
- PDP / PEP / PIP removed: "not part of information model but of server infrastructure
  hosting the Asset Administration Shells"; Certificate, BlobCertificate and
  Security/certificate removed for the same reason (Table 25, p.181).
- `AccessPermissionRule` no longer inherits from Referable nor Qualifiable (its new
  `constraint` attribute substitutes for the qualifiers); `Formula` is now abstract and
  used only in the security part, no longer in Qualifiables; `Formula/dependsOn` removed.
- Security constraints renamed from `AASd-` to `AASs-` (p.204): AASd-010/011 became
  AASs-010 (the property referenced in Permission/permission shall have category
  "CONSTANT") and AASs-011; AASs-009 was removed "since class PolicyAdministrationPoint
  was removed" (Table 27, p.182).
- `PermissionKind` literals are capitalised since V2.0: `Allow`, `Deny`, `NotApplicable`,
  `Undefined` (Table 46, p.209).

Enforcement therefore happens in the server / API gateway using tokens. Label that as
deployment practice, not as "IDTA-01004 says".

---

## 2. Production auth for AAS REST APIs (beyond IDTA-01004)

IDTA-01004 fixes only the token form (signed JWT bearer, §1). Everything else in this
section (claim names, scopes, mTLS, API keys) is IETF/W3C or vendor practice, not
IDTA-normative. Label it that way when writing about it.

### 2.1 OAuth 2.0 / OpenID Connect (Bearer tokens)

The default choice for human-facing and most B2B flows.

```
Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...
```

Token claims the AAS server typically inspects (become `CLAIM` attributes in an IDTA-01004
rule if you're using the Access Rule Model):

- `iss` — trusted issuer (Keycloak, Azure AD, custom OP)
- `aud` — must match this AAS service's audience
- `sub` — subject identifier
- `scope` — space-separated permissions (e.g., `aas:read submodel:write`)
- `roles` / `groups` — role claims (custom, depends on IdP)
- `org` / `tenant` — multi-tenant key

Production convention (not IDTA-normative):
- Scope tokens like `aas:read`, `aas:write`, `submodel:read`, `submodel:write`,
  `submodel:invoke`, `aas:admin`.
- Role-to-scope mapping happens at the IdP.
- The API gateway enforces; the AAS server is policy-aware but not policy-defining.

### 2.2 mTLS (mutual TLS)

Default for service-to-service in critical / regulated flows (Catena-X, regulator-side
DPP access).

- Each peer presents an X.509 certificate during TLS handshake.
- The server identifies the client by the certificate's Subject / SubjectAlternativeName.
- A CA chain (often a federation CA, like Catena-X's IATP) validates the certificate.
- Role / permission mapping uses CN, OU, or a custom certificate attribute; these become
  `CLAIM` attributes when composed with the Access Rule Model.

Pros: no token lifetime to manage. Cons: certificate lifecycle management is heavier.

### 2.3 API keys

Not in the IDTA spec, but common in commercial AAS Repository deployments.

- Pragmatic for pre-OAuth onboarding, per-user isolation, easy revocation.
- API keys SHOULD travel as `Authorization: Bearer <key>` over HTTPS, matching the
  OAuth wire shape so consumers don't change for the OAuth migration.

---

## 3. Authorisation patterns at the AAS API level

Production convention for scope-to-endpoint mapping (not IDTA-normative):

| Operation | Required scope (typical) | Notes |
|---|---|---|
| `GET /shells` | `aas:read` | List, paginated |
| `GET /shells/{id}` | `aas:read` | Get one shell |
| `POST /shells` | `aas:write` | Create |
| `PUT /shells/{id}` | `aas:write` | Update / replace |
| `DELETE /shells/{id}` | `aas:admin` | Admin-only (typical) |
| `GET /shells/{id}/submodels/{sid}` | `submodel:read` | Get submodel via shell |
| `POST /shells/{id}/submodels/{sid}/submodel-elements/{path}/invoke` | `submodel:invoke` | Execute Operation |
| `GET /shell-descriptors` | `registry:read` | Registry list |
| `POST /shell-descriptors` | `registry:write` | Register a shell |

**Per-resource decisions.** The Access Rule Model in IDTA-01004 allows per-shell,
per-submodel, per-element rules via `DEFOBJECTS` groups. Most production deployments
simplify to per-shell or per-tenant, plus a public/authenticated split at the API
gateway.

---

## 4. AAS content signing (not IDTA-01004; API-level JWS is IDTA-01002 v3.2)

IDTA-01004 specifies no native data-bound signature (v3.1 p.124, §1). The only IDTA-defined
signature is the IDTA-01002 v3.2 `/$signed` JWS (RS256, embedded JSON payload, `x5c`).
Everything below is deployment practice composed from IETF/W3C standards.

### 4.1 AASX signing (XMLDSig + XAdES)

For `.aasx` packages: standard OPC / OOXML signing.

- `_xmlsignatures/` directory holds signature parts.
- OPC relationship `digital-signatures/origin` points at the signature.

Tools: OOXML signing libraries (DocuSign API, OpenSSL + Apache POI,
`System.Security.Cryptography.Xml`).

### 4.2 AAS JSON signing (JWS / JAdES)

For JSON serialisations: detached or attached JWS. Sign a canonicalised JSON payload.

Recommended:
- Canonicalisation: **JCS (RFC 8785)** for deterministic ordering.
- Signing algorithm: **ES256** (ECDSA P-256) or **PS256** (RSA-PSS).
- JWS Compact or JWS JSON serialisation depending on consumer.

### 4.3 Per-element signing (granular)

For sensitive submodels (e.g., a Battery Passport's PCF) sign JUST that submodel
(canonicalise + sign the sub-tree). Lets a verifier check the PCF independent of the
rest of the AAS.

### 4.4 Key management

- **Certificates**: X.509 issued by a recognised CA (sectoral CA like Catena-X IATP, or
  a commercial CA).
- **Key rotation**: include a `kid` in the signature so consumers validate against a
  key from the rotation set.
- **Revocation**: OCSP or CRL distribution points. For offline regulator inspection,
  embed the CRL in the AASX package.

---

## 5. Federation between Registry and Repository

In a federated AAS deployment (Catena-X, DPP), the resolver chain from IDTA-01002 goes:

```
Consumer ──→ Discovery  ──→ Asset-ID → AAS-ID
        ──→ Registry   ──→ AAS-ID → Repository endpoint
        ──→ Repository ──→ AAS content
```

Auth flow:

1. Consumer obtains a token from the trusted IdP.
2. Consumer presents token to Registry → gets descriptor.
3. Consumer presents the same token (or a delegated token) to Repository → gets the
   shell.

Two production federation patterns:

- **Single IdP** (simpler): Discovery, Registry and Repository trust the same issuer.
  The token works for all three.
- **IdP federation** (Catena-X): each Repository may trust a different IdP; tokens are
  exchanged through a trust framework (e.g., IATP).

IDTA-01004 is mechanism-flexible on this. Single IdP is fine for closed deployments;
federation only when crossing organisation boundaries.

---

## 6. CORS, CSP, and other web-platform concerns

Not in the AAS spec. Production essentials:

- **CORS**: AAS REST APIs serving browser-based consumers need CORS headers. Allow only
  expected origins; never `*` for write endpoints.
- **CSP**: serve a Content-Security-Policy for any HTML viewer.
- **Rate limiting**: per-token limits.
- **Audit logging**: every authenticated write should log
  `(timestamp, subject, resource, operation, outcome)`. Required for ESPR / Battery
  Regulation audit trails.

---

## 7. Common attack surfaces

- **Unauthenticated `/description`**: by convention this endpoint is open. Don't put
  behind auth; breaks discovery.
- **Authenticated but unauthorised**: a valid token doesn't imply permission. 401
  (no / bad token) is not 403 (token valid, permission insufficient). Keep them
  separate.
- **IDOR (Insecure Direct Object Reference)**: if `/shells/{id}` doesn't check tenant
  ownership, any authenticated user reads everyone's shells. Scope every query by
  tenant from the token.
- **Tenant isolation**: cross-tenant access should return **404 (not 403)** to avoid
  enumeration. Pin this contract with tenant-isolation property tests.
- **Replay of signed AASX**: a signed AAS from yesterday could be re-presented today.
  Use nonce or timestamp in the signing payload for time-sensitive flows.
- **JWT algorithm confusion**: explicitly pin `alg=RS256` or `ES256`; never accept
  `alg=none`.
- **Long-lived API keys**: rotate. Document the rotation policy for consumers.
- **CORS on write endpoints**: never `*`. Restrict to known partner origins.

---

## 8. Integration with the DPP access model

The 4-tier CIRPASS reference (`Public / Verified / Regulator / Recycler` — see
`dpp-knowledge` §5) is a **stakeholder-category taxonomy** used as reference
architecture. It is not the same as any specific regulation's mandated access model.

**Battery Regulation (EU 2023/1542)** collapses those into three categories, distributed
across Annex XIII Points 1, 2, 3, 4 (Point 2 is shared):
- Public (Point 1)
- Persons with legitimate interest (Points 2 and 4) — the Regulation does not list
  them: Art. 77(9) requires the Commission to adopt implementing acts by 18 August 2026
  specifying who counts and what they may access (EUR-Lex CELEX_32023R1542, Art. 77(9))
- Notified bodies + market surveillance + European Commission (Points 2 and 3)

Textile Passport (in the ESPR delegated-act pipeline) will define its own stakeholder
structure over the same reference architecture.

The mapping to IDTA-01004 rules (production pattern, not IDTA-normative):

| CIRPASS tier | Typical auth mechanism | Sample IDTA-01004 rule |
|---|---|---|
| Public | Anonymous over HTTPS | Rule matching `CLAIM.role=anonymous` on public submodels |
| Verified | OAuth Bearer (operator-issued) | Rule matching `CLAIM.role=operator` on full shell |
| Regulator | mTLS (regulator CA) | Rule matching `CLAIM.iss=eu-regulator-ca` on all submodels |
| Recycler / EoL | OAuth Bearer (registry-issued at take-back) | Rule matching `CLAIM.role=recycler` on recycler-specific submodels |

The token claims become IDTA-01004 `CLAIM` attributes; the rules gate submodels by
attribute. The AAS server enforces at the API gateway (production pattern); the 3.x
metamodel has no AccessControl element on the shell to carry these rules.

---

## 9. Pitfalls and non-obvious rules

- **The spec is mechanism-agnostic on authentication.** Don't cite IDTA-01004 to
  justify a specific auth protocol.
- **RBAC is a special case of ABAC in IDTA-01004.** Implement RBAC by defining role
  attributes.
- **IDTA-01004 fixes the token form, not the protocol.** Signed JWT bearer access tokens
  (RFC 7519, v3.1 p.46); any authentication flow that yields one (v3.1 p.26). No native
  content signing (v3.1 p.124); API JWS is IDTA-01002 v3.2 `/$signed`.
- **There is no AccessControl / security attribute on a 3.x AAS** (removed in V3.0,
  IDTA-01001 v3.0 PDF p.152); enforcement happens in the server / API gateway.
- **401 vs 403 distinction matters.** 401 = no / bad auth. 403 = auth OK but rule
  denies.
- **Cross-tenant 404 vs 403.** When a request is well-authenticated but the resource
  belongs to another tenant, return 404 (not 403) to avoid leaking existence.
- **JWS canonicalisation matters.** Use JCS (RFC 8785) so equivalent JSON produces
  identical signatures.
- **API keys are NOT in the IDTA spec.** Use them for pragmatism; plan the OAuth
  migration.
- **mTLS certificates need lifecycle management.** Auto-renew, monitor expiry, rotate
  on compromise.
- **Auth claims should travel as scopes, not raw roles.** Map roles to scopes at the
  IdP; the AAS service consumes scopes. Decouples IdP role taxonomy from AAS
  permission taxonomy.
- **Don't inline secrets in AAS content.** A Property with value `API_KEY=sk-...` gets
  persisted forever. Use Reference to a secrets manager URL.

---

## 10. Authoritative references

- **IDTA-01004 Part 4 v3.1** (current) and **v3.0.2**, official PDFs vendored at
  `idta-specs:pdf/` (industrialdigitaltwin.org content hub); HTML:
  https://industrialdigitaltwin.io/aas-specifications/IDTA-01004/v3.0.2/
  - Access Rule Model normative section:
    https://industrialdigitaltwin.io/aas-specifications/IDTA-01004/v3.0.2/access-rule-model.html
- **OAuth 2.0** — RFC 6749 (base), OIDC Core (identity). Production auth, NOT in
  IDTA-01004.
- **OAuth 2.0 + mTLS** — RFC 8705 (client auth via mTLS). Production auth, NOT in
  IDTA-01004.
- **JWS** — RFC 7515. Not in IDTA-01004; IDTA-01002 v3.2 uses it for `/$signed`
  (RS256 only, embedded payload). Detached or ES256 JWS is deployment practice.
- **JCS (canonical JSON)** — RFC 8785. Production signing prerequisite.
- **Eclipse FA³ST** — `github.com/FraunhoferIOSB/FAAAST-Service`, Java reference impl
  with Keycloak integration.

---

## Behavioural notes for Claude using this skill

- **When asked "what does IDTA-01004 define"**, always answer: an ABAC-based Access
  Rule Model with `DEFATTRIBUTES` / `DEFACLS` / `DEFOBJECTS` / `DEFFORMULAS` /
  `AccessPermissionRule` primitives, serialised in BNF or JSON Schema. Authentication
  is out of scope.
- **When asked "how do I secure my AAS API"**, separate: (1) what IDTA-01004 defines
  (rules), (2) what auth mechanism to use (OAuth, mTLS, API keys — production choices,
  NOT IDTA-normative), (3) what signing format to use (JWS, XMLDSig — production
  choices).
- **Never claim IDTA-01004 defines OAuth, mTLS, X.509, JWT, or signing formats.** That
  was a known error in the pre-2026-07-10 version of this skill.
- **For DPP integration**, map to the CIRPASS reference tiers (Public / Verified /
  Regulator / Recycler) and note that specific regulations (Battery, Textile) may
  collapse or extend that model. Do not present the 4-tier as "what the Battery
  Regulation defines".
- **For tenant isolation**, insist on 404 (not 403) for cross-tenant access.
- **Verify at source before writing anything technical about IDTA-01004.** WebFetch
  the spec section and cite it inline.
