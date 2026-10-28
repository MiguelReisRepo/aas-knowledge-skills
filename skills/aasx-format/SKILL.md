---
name: aasx-format
description: AASX package file format expertise (IDTA-01005 Part 5 v3.1) — the AASX is an OPC (Open Packaging Conventions, same family as .docx/.xlsx/.pptx) ZIP container holding the AAS environment XML/JSON plus supplementary files, thumbnail, and relationships. This skill covers the package structure ([Content_Types].xml, _rels/.rels, aasx-origin, per-part relationships), the content types (package MIME type `application/asset-administration-shell-package` in Part 5 v3.1, replaced by the IANA-registered `application/aas+zip` in v3.2; ECMA-376 types such as `text/xml` / `application/json` for the parts), the relationship type IRIs (`http://admin-shell.io/aasx/relationships/aasx-origin`, `aas-spec`, `aas-suppl`; the thumbnail uses the OPC `metadata/thumbnail` type), how to add/extract a supplementary file, how a `File` submodel element references a part by path, MIME-type sniffing rules, package-signing and editor round-trip pitfalls. Use this skill whenever the user is reading or writing .aasx files, integrating with an AASX File Server, debugging "this AASX won't open in AASX Package Explorer", packaging supplementary PDFs / images into an AAS, or implementing a serializer / parser for AASX. Trigger when the user mentions OPC, .aasx, AASX Package Explorer, package-explorer, aasx-origin, or pastes a ZIP listing of an AASX.
---

# AASX package format

The AASX is the canonical **bundle** format for AAS content. It packages
the AAS environment (XML or JSON), supplementary files (PDFs, images,
test reports), and a thumbnail in a single ZIP, with explicit
**relationships** declaring which part is which.

**Source**: IDTA-01005 Part 5: Specification of the Asset Administration
Shell — Package File Format (AASX), v3.1 (release 25-01) and v3.2, official PDFs
from industrialdigitaltwin.org, vendored at `idta-specs:pdf/` with paged text in
`idta-specs:txt/` (sha256 in `VERSION.json`). The only normative change in v3.2 is
the package MIME type (§3 below).

The format is built on **OPC (Open Packaging Conventions)**, the same
ECMA-376 / ISO/IEC 29500-2 family that underlies .docx, .xlsx, .pptx, and
.3mf. If you know how a .docx is structured, the AASX is the same shape
with different content types.

---

## 1. The package structure

An .aasx is a ZIP with this canonical layout:

```
my-asset.aasx (ZIP)
├── [Content_Types].xml          ← MIME type declarations for every part
├── _rels/
│   └── .rels                    ← package-level relationships (entry points)
├── aasx/
│   ├── aasx-origin              ← empty part; marks this ZIP as an AASX
│   ├── _rels/
│   │   └── aasx-origin.rels     ← what the origin points at (the AAS content)
│   ├── data.aas.xml             ← the AAS environment (XML or JSON)
│   │                              filename is conventional; relationships
│   │                              identify it
│   └── _rels/
│       └── data.aas.xml.rels    ← relationships FROM the AAS to supplementary
│                                  files (so File elements resolve)
├── aasx/files/                  ← supplementary files referenced by AAS
│   ├── datasheet.pdf            ← (filename is conventional; references
│   │                              by File element point at /aasx/files/...)
│   └── installation.pdf
└── thumbnail.png                ← optional package thumbnail (top-level)
```

Three core conventions to internalise:

1. **`[Content_Types].xml`** declares the MIME type for every part (file)
   in the package by extension or by exact path. Without an entry here,
   readers don't know how to interpret a part.
2. **`_rels/.rels`** is the entry-point manifest. It points at the
   `aasx-origin` part with the well-known relationship type.
3. **`aasx-origin`** is a (typically empty) part whose presence + its
   `_rels/aasx-origin.rels` file together say "this ZIP is an AASX, and
   the actual AAS content is at <PATH>".

---

## 2. The relationship-type IRIs

Three relationship types travel through the package, used in the `.rels`
XML to link parts together.

**The namespace (corrected 2026-09-19; this skill said the opposite until then).**
IDTA-01005 Part 5 v3.1 (`admin-shell-io/aas-specs-aasx`, tag `v3.1.0`, `aasx.adoc`),
literal: *"The following relationship path is deprecated:
`http://www.admin-shell.io/aasx/relationships`"*, and in the namespace table
`<rel_aas>` = `http://admin-shell.io/aasx/relationships` "and (<<Deprecated>>)
`http://www.admin-shell.io/aasx/relationships`". Its changelog: *"support both
relationship paths: http://admin-shell.io/aasx/relationships (as specified and
recommended) and (deprecated) http://www.admin-shell.io/aasx/relationships"*.
So: **write the non-www form; read both.** aas-test-engines 1.0.3 agrees (its
`TYPE_AASX_*` are non-www; the www ones sit in `DEPRECATED_TYPES` and each raises
a WARNING), and Eclipse BaSyx 2.1.0 finds the `aas-spec` part only under the
non-www IRI: with the www form it opened every one of our 103 template packages
as EMPTY.

| Relationship type IRI | Used at | Points to |
|---|---|---|
| `http://admin-shell.io/aasx/relationships/aasx-origin` | package level (`_rels/.rels`) | the `aasx-origin` part |
| `http://admin-shell.io/aasx/relationships/aas-spec` | origin level (`_rels/aasx-origin.rels`) | the AAS content part (XML or JSON) |
| `http://admin-shell.io/aasx/relationships/aas-suppl` | AAS-content level (`_rels/data.aas.xml.rels`) | supplementary files referenced by `File` submodel elements |
| `http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail` | package level | the thumbnail image |

Each relationship in a `.rels` XML looks like:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="r1"
                Type="http://admin-shell.io/aasx/relationships/aas-spec"
                Target="/aasx/data.aas.xml"/>
</Relationships>
```

- `Id` is local to the .rels file (a stable identifier within the
  package, often "r1", "r2", "rId1", etc.).
- `Type` is the relationship IRI from the table above.
- `Target` is the path to the related part, relative to the .rels file's
  parent (use a leading `/` for absolute-to-package).

---

## 3. `[Content_Types].xml`

Declares which MIME type each part of the package has. Two declaration
forms:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <!-- Default: by extension -->
  <Default Extension="rels"
           ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"
           ContentType="text/xml"/>
  <Default Extension="pdf"
           ContentType="application/pdf"/>
  <Default Extension="png"
           ContentType="image/png"/>

  <!-- Override: by specific part path -->
  <Override PartName="/aasx/aasx-origin"
            ContentType="text/plain"/>
  <Override PartName="/aasx/data.aas.xml"
            ContentType="text/xml"/>
</Types>
```

**The AAS XML part is `text/xml` (or `application/xml`).** Part 5 v3.1 names one
MIME type, for the PACKAGE: *"MIME-type for the AASX format:
application/asset-administration-shell-package"* (p.15, footnoted *"The current
MIME-type is provisory and needs to be requested officially."*). **Part 5 v3.2
changes it:** *"MIME-type for the AASX format: application/aas+zip"* (p.14, footnote
*"This MIME-type is registered at IANA"*); changelog: *"the provisory MIME-Type
application/asset-administration-shell-package was substituted with the newly
registered IANA MIME-Type application/aas+zip (#41)"* (p.22). Write `application/aas+zip`
when targeting v3.2; accept both when reading. For the
parts it asks only for *"appropriate ECMA-376 Content Types (MIME type)"*.
`application/asset-administration-shell-package+xml` on the XML part is defined
nowhere (this skill called it "critical" until 2026-09-19); BaSyx 2.1.0 refuses a part it cannot classify and accepts `text/xml`,
`application/xml`, `text/json`, `application/json`. The third-party packages in a
real-world fixture set use `text/xml`.

For an AAS JSON variant, the override would be `application/json` (or
`text/json`) on `/aasx/data.aas.json` — no AAS-specific part type is defined
for JSON either.

---

## 4. Reading an AASX (the recipe)

To extract content programmatically:

1. **Open the ZIP**. Use a streaming ZIP reader if the package is large
   (some battery passport packages with multi-megapixel images run to
   100+ MB).
2. **Read `[Content_Types].xml`**. Build a map: part path → content type.
3. **Read `_rels/.rels`**. Find the relationship of type `aasx-origin`;
   note its target (`/aasx/aasx-origin`).
4. **Read `<target>/_rels/<target-name>.rels`** (i.e.
   `/aasx/_rels/aasx-origin.rels`). Find relationship of type
   `aas-spec`; note its target (e.g. `/aasx/data.aas.xml`).
5. **Read the AAS content**. Parse based on the content type
   (XML for `text/xml` / `application/xml`, JSON for `application/json` /
   `text/json`; fall back to the part's extension).
6. **Optionally read the AAS-content `.rels`** for supplementary file
   resolution. Each `aas-suppl` relationship's target is a `File`
   submodel element's `value` (resolution: the File's `value` is a path
   that matches a `Target` in this .rels).

In Python with `python-docx`'s underlying `zipfile` + `lxml`:

```python
import zipfile
from lxml import etree

NS = {'r': 'http://schemas.openxmlformats.org/package/2006/relationships'}

with zipfile.ZipFile('my.aasx') as z:
    # 1. content types
    ct = etree.fromstring(z.read('[Content_Types].xml'))

    # A reader accepts BOTH namespaces (Part 5 v3.1: the www one is deprecated, not gone).
    AAS_RELS = ('http://admin-shell.io/aasx/relationships/',
                'http://www.admin-shell.io/aasx/relationships/')
    def target(rels, name):
        for rel in rels.xpath('//r:Relationship', namespaces=NS):
            if rel.get('Type') in (ns + name for ns in AAS_RELS):
                return rel.get('Target').lstrip('/')
        raise ValueError(f'no {name} relationship')

    # 2. package rels → origin
    pkg_rels = etree.fromstring(z.read('_rels/.rels'))
    origin = target(pkg_rels, 'aasx-origin')

    # 3. origin rels → aas-spec
    origin_rels_path = f'aasx/_rels/{origin.rsplit("/", 1)[1]}.rels'
    origin_rels = etree.fromstring(z.read(origin_rels_path))
    aas_path = target(origin_rels, 'aas-spec')

    # 4. AAS content
    aas_xml = z.read(aas_path)
```

In Node with `jszip`:

```javascript
import JSZip from 'jszip';

const zip = await JSZip.loadAsync(buffer);
const pkgRels = await zip.file('_rels/.rels').async('text');
// XML-parse pkgRels, find aasx-origin Target
// ...
const aasXml = await zip.file('aasx/data.aas.xml').async('text');
```

---

## 5. Writing an AASX (the recipe)

To create a valid AASX:

1. Serialise your AAS environment to XML (or JSON).
2. Decide where supplementary files go (typically `/aasx/files/...`).
3. Build the package skeleton:
   - `[Content_Types].xml` with defaults + overrides for AAS content.
   - `_rels/.rels` pointing at `aasx-origin`.
   - `aasx/aasx-origin` (Part 5 v3.1 p.17: *"an empty file or a plain text file containing the text \"Intentionally empty\""*).
   - `aasx/_rels/aasx-origin.rels` pointing at the AAS content.
   - `aasx/data.aas.xml` (your serialised content).
   - For each supplementary file: write to `/aasx/files/...` AND add an
     `aas-suppl` relationship in `aasx/_rels/data.aas.xml.rels`.
4. ZIP it with `Deflate` compression. Avoid `Store` (uncompressed) — some
   tools accept it but the format expects compression for non-trivial
   payloads.

**Critical**: file paths inside `File` submodel elements MUST match the
relationship targets. If `File.value = "/aasx/files/datasheet.pdf"`,
there must be both:
- a ZIP entry at `aasx/files/datasheet.pdf`
- an `aas-suppl` relationship with `Target="/aasx/files/datasheet.pdf"`

Mismatch = the file element points at nothing, the package "opens" but
the supplementary file is invisible.

---

## 6. File submodel element resolution

`File` elements bind path references in the AAS to ZIP entries. A `Blob`
does NOT: "in contrast to the file property the file content is stored
directly as value" (aas-core-meta v3_1.py:3218-3221). The semantics:

```xml
<file>
  <idShort>Datasheet</idShort>
  <value>/aasx/files/datasheet.pdf</value>
  <contentType>application/pdf</contentType>
</file>
```

- `value` is "a URI that can represent an absolute or relative path"
  (IDTA-01001 v3.0 PDF p.72). For a file inside the package use a path
  relative to the package root; an absolute path (e.g. an `https://` URL) is
  for a file that exists independently of the AAS (same page). In 3.1 it is a
  `Path_type`: 1-2048 characters conformant to a URI per RFC 2396
  (aas-core-meta v3_1.py:1389-1392). Never a filesystem path.
- `contentType` is the file's MIME: a valid media type per RFC 2046
  (`type/subtype`, e.g. `application/pdf`; a bare `pdf` is not conformant),
  max 100 characters in V3.0 and 128 in V3.1 (aas-core-meta v3_0.py:1378-1381,
  v3_1.py:1362-1369). **Optional in 3.1** (schemas/3.1/AAS.xsd:412
  `minOccurs="0"`), mandatory in 3.0. When set, keep it consistent with the
  `[Content_Types].xml` declaration; a mismatch makes some tools reject or
  misrender the package.
- An `aas-suppl` relationship in `aasx/_rels/data.aas.xml.rels` MUST
  exist with this Target. Part 5 v3.1 (p.18): *"The source of any aasx-suppl
  relationship must be the file containing the AAS structure/specification. If the
  information is available in several formats, the relationships need to be defined
  for each of the files."* Only relative references are package parts: *"Only a
  relative URI reference shall be interpreted as a reference to a supplementary file
  within the AASX package."* Blobs are never package parts (*"blobs as defined via
  submodel Element Blob are not stored as supplemental files within the package"*).

When a `File` element points at an **external URL** (`http://...` or
`https://...`), the value is the URL; no ZIP entry exists; no `aas-suppl`
relationship is needed. contentType follows the same rule as above
(optional in 3.1, mandatory in 3.0).

---

## 7. Thumbnail

A thumbnail is a single image at the PACKAGE level (not inside `/aasx/`).
Convention: `/thumbnail.png` or `/thumbnail.jpg`.

Declared in `_rels/.rels`:

```xml
<Relationship Id="rThumb"
              Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/thumbnail"
              Target="/thumbnail.png"/>
```

Inside the AAS, `AssetInformation/defaultThumbnail` is a `Resource`: only
`path` is required, its `contentType` is optional (schemas/3.1/aas.json:1305-1308).

Plus an entry in `[Content_Types].xml`:
```xml
<Default Extension="png" ContentType="image/png"/>
```

Editors (AASX Package Explorer) display this
thumbnail when listing packages, so users can recognise an asset
visually.

---

## 8. Server-side delivery (AASX File Server API)

When serving an AASX over HTTP (per the IDTA-01002 AASX File Server API):

- Response `Content-Type`:
  `application/aas+zip` (Part 5 v3.2, IANA-registered) or
  `application/asset-administration-shell-package` (Part 5 v3.1, provisory);
  a ZIP is not XML, so never `+xml`
- Response `Content-Disposition`: `attachment;
  filename="<asset-name>.aasx"` so browsers download rather than render.
- Binary body. Chunked transfer encoding for large packages.
- For multi-MB packages: support range requests (`Accept-Ranges: bytes`)
  so consumers can resume.

A common mistake: serving with `Content-Type: application/zip`. Tools
will accept it (because the bytes ARE a ZIP) but the content type
mismatch breaks downstream MIME-driven flows (e.g., a webhook that
should fan-out only when an actual AASX is delivered).

---

## 9. Editor round-trip pitfalls

When extracting → modifying → re-packaging:

- **Preserve `Id` attributes on relationships.** Some readers cache
  relationship IDs; changing them on every save breaks idempotency.
- **Preserve part-path casing.** OPC says paths are case-sensitive;
  Windows ZIP tools sometimes silently lowercase. AASX Package Explorer
  treats `/aasx/Data.aas.xml` and `/aasx/data.aas.xml` as different.
- **Strip BOMs from XML parts.** `[Content_Types].xml` with a BOM at the
  start is technically allowed but some parsers (especially older
  python-docx variants used by tooling vendors) trip on it.
- **Don't rewrite `[Content_Types].xml` in non-canonical order.** Some
  validators check default-then-override ordering; reordering can
  produce a valid-but-rejected package.
- **Re-emit relationships in the same XML namespace.** Mix-ups happen
  when copying `<Relationships>` between packages with different
  XML default namespaces.
- **Keep the `aasx-origin` file content identical** (typically empty or
  exactly one bytea pattern from the canonical example). Some tools
  validate by hashing this part as a "magic number".

---

## 10. Validation + tools

- **AASX Package Explorer** (Microsoft Windows desktop app), reference
  implementation: `github.com/admin-shell-io/aasx-package-explorer`.
  THE tool for visual inspection of a package.
- **aas-test-engines `check_aasx`**:
  `aas_test_engines check_aasx your.aasx --version 3.1` runs the IDTA
  conformance gate on the package (both the AAS metamodel inside AND
  the OPC structure outside).
- **A real writer defect to check for** (seen in a production editor): the
  origin's relationship part written as `_rels/aasx-original.rels` at package
  root (canon is `aasx/_rels/aasx-origin.rels`). Two things that look wrong but
  are not: non-www relationship `Type` IRIs (`http://admin-shell.io/...`) are in
  fact the RECOMMENDED form (Part 5 v3.1 deprecates the www one; this note had it
  backwards until 2026-09-19), and no `Override` for the XML part is fine as long
  as the `Default` for `xml` is `text/xml`. Use §1–§3 of this skill as canon
  for what a correct chain looks like.
- **OPC validation**: any OOXML toolchain that validates package
  structure (OpenXML SDK, `python-docx` internals, `epubcheck` for
  comparison) — the OPC layer is reusable.

---

## 11. Pitfalls and non-obvious rules

- **The relationship Target is a path, not a URI.** `Target="/aasx/foo"`
  is a package-relative path; don't add `file://` or any scheme.
- **`[Content_Types].xml`'s `<Default Extension="...">` is GREEDY.** A
  default for `xml` matches both `data.aas.xml` AND `aasx-origin.rels`'s
  `.xml` if you forget — always override for the AAS content.
- **The empty `aasx-origin` file MUST exist** even though it has no
  body. Some tools check its presence; some hash it. Don't omit.
- **Supplementary file paths in `File.value` use `/` as separator on ALL
  platforms.** A backslash is not a URI character, so a `\` path fails 3.1's
  RFC 2396 `Path_type` (aas-core-meta v3_1.py:1389-1392) besides breaking
  portability.
- **Compress all parts** with `Deflate`. Uncompressed-stored parts are
  legal but some readers (especially older Java OOXML libraries) crash
  on them.
- **A signed AASX has additional parts** (`_xmlsignatures/`,
  `_rels/.rels` extended). If you re-pack a signed AASX without
  re-signing, the signature breaks silently.
- **Package size limits vary by consumer.** Mobile AAS viewer apps cap
  at 50 MB; some servers at 100 MB. Battery passport packages with full
  EPD PDFs often hit these. Test against your target consumer's limits
  before deploying.
- **Thumbnails are optional but EXPECTED.** A package without one
  renders as a generic icon in editors. For consumer-facing DPP, embed
  a real product image.
- **One AAS is never split across parts.** Since V3.0 "no splitting of an Asset
  Administration Shell allowed any longer (i.e. relationship type aas-spec-split
  removed)" (IDTA-01001 v3.0 PDF p.199).
- **Multi-shell AASX (more than one AAS in one package) is supported.**
  The single `data.aas.xml` declares multiple `<assetAdministrationShell>`
  entries under `<environment>`. Don't split into multiple .aasx files
  unless the consumer flow needs that.
- **Prefer a `File` over a large `Blob`.** A `File` points at a supplementary
  part; a `Blob` carries the content itself, base64 inside the AAS
  (aas-core-meta v3_1.py:3218-3221). Large inlined blobs inflate the XML and
  strain streaming parsers.

---

## 12. Authoritative references

- **IDTA-01005 Part 5 v3.1 / v3.2** (the AASX format spec): official PDFs on
  industrialdigitaltwin.org (content hub, AAS specifications), vendored at
  `idta-specs:pdf/IDTA_01005-25-01_…pdf` (v3.1) and `idta-specs:pdf/IDTA-01005-3-2_…pdf` (v3.2)
- **OPC base spec (ECMA-376 / ISO/IEC 29500-2):**
  the underlying packaging convention. Reading this gives you 80% of the
  AASX format for free — AAS just adds specific content types and
  relationship IRIs on top.
- **AASX Package Explorer** (reference editor + viewer):
  [github.com/admin-shell-io/aasx-package-explorer](https://github.com/admin-shell-io/aasx-package-explorer)
- **aas-test-engines**: `pip install aas-test-engines` then
  `aas_test_engines check_aasx your.aasx --version 3.1`.

---

## Behavioural notes for Claude using this skill

- When the user reports "AASX won't open", **lead with the package
  structure checklist** (§1 + §3 + §4): does `[Content_Types].xml`
  declare a usable MIME (`text/xml`, `application/json`…) for the AAS part? Does `_rels/.rels` point at
  `aasx-origin`? Does the origin's `.rels` point at the AAS content?
  90% of "broken AASX" issues are one of these three.
- For "add a supplementary file" questions, **always do both steps**:
  the ZIP entry AND the `aas-suppl` relationship. Skipping the
  relationship is the most common mistake.
- When asked "what content type for the AAS part": `text/xml` (or
  `application/xml`) for the XML part and `application/json` (or `text/json`)
  for the JSON part. Part 5 names a MIME type only for the PACKAGE
  (`application/asset-administration-shell-package`); see §3 above. (Corrected
  2026-10-02: this note still prescribed `...-package+xml` for the XML part.)
- For File element resolution, **match path exactly** — case-sensitive,
  forward slashes, leading `/`. Spell out the rules to the user; tools
  fail silently here.
- When the user is implementing a packager, **build to §1–§3 of this
  skill as the canonical OPC chain**, plus AASX Package Explorer as the
  reference visual validator. Do NOT cite an existing writer as a worked
  example without checking it against §1–§3 first (the wrong origin-rels
  path in §10 is a real-world defect; a writer can also get the chain right and
  still use the deprecated www relationship Type IRIs or put the package media
  type on a part).
- For signed-AASX questions, the X.509 signature layer is OPC-standard.
  Refer to OPC's `digital-signatures` part. Don't reinvent.
