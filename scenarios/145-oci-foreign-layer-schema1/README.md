# Scenario 145: OCI — foreign-layer URL + legacy `schemaVersion 1`

**Provider:** OCI image manifest · **OWASP:** CICD-SEC-9 (Improper Artifact Integrity Validation) · **Severity: high**

**Vulnerable manifest:** [`manifest.json`](manifest.json)

## The pattern

```json
"schemaVersion": 1,
"layers": [{ "urls": ["http://layers.internal.example.com/blobs/sha256:1111"] }]
```

A layer carries a `urls:` field (a **foreign layer**), so the blob is fetched
from an arbitrary URL the manifest declares — not the registry the image was
pulled from. And `schemaVersion 1` is the legacy Docker manifest format with no
content-addressable config, so there is no digest binding the image to its bytes.

## How an attacker exploits it

The URL owner serves client-specific content (server-side cloaking) or takes the
endpoint offline to break pulls; the foreign-layer fetch leaves the registry's
trust boundary. `schemaVersion 1` removes the content-addressing that would
otherwise detect tampering. Together the image's integrity is unverifiable.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `OCI-004` — _layer references an arbitrary URL (foreign layer)_ · `OCI-007` — _legacy `schemaVersion 1` (no content addressing)_ |

> pipeline-check is the only scanner in this comparison that parses OCI image
> manifests / image indexes.

## Fix

Build images as OCI / Docker v2 (`schemaVersion 2`) with content-addressable
config and layer digests; don't use foreign-layer `urls:` — push all blobs to the
registry the image is served from.

## References

- OCI — Image Manifest Specification: https://github.com/opencontainers/image-spec/blob/main/manifest.md
- OCI — Image Index / content addressing: https://github.com/opencontainers/image-spec/blob/main/image-index.md
