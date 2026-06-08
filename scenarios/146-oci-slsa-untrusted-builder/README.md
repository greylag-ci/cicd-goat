# Scenario 146: OCI — SLSA provenance attests an untrusted builder + unbound subject

**Provider:** OCI image-index + in-toto attestation · **OWASP:** CICD-SEC-9 (Improper Artifact Integrity Validation) · **Severity: high**

**Vulnerable manifest:** [`index.json`](index.json) (+ `blobs/sha256/…` in-toto Statement)

## The pattern

This is an OCI **image-layout** directory: `index.json` references a runtime
manifest plus a BuildKit attestation manifest, whose in-toto SLSA provenance
Statement lives under `blobs/sha256/`:

```json
"predicate": { "runDetails": { "builder": { "id": "https://self-hosted.internal.example.com/agents/runner-7" } } },
"subject": [ { "name": "acme/app", "digest": {} } ]
```

Two failures: (1) the SLSA provenance attests a **self-hosted builder identity**
the SLSA contract cannot vouch for; (2) the Statement `subject` carries **no
digest**, so the attestation binds to no actual image bytes.

## How an attacker exploits it

A compromised self-hosted runner can produce a perfectly-formed, signature-valid
attestation for a *tampered* image — so a present, valid-looking attestation
isn't the same as a trustworthy one. And an empty subject digest means the
Statement attests "something" without binding to the image's content, so it can
be replayed against substituted bytes.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ATTEST-001` — _SLSA provenance attests an untrusted builder identity_ · `ATTEST-005` — _in-toto Statement subject is missing or unpinned_ |

> pipeline-check parses the in-toto Statement out of the image-layout `blobs/`
> tree — `OCI-002` (attestation present) passing is *not* the same as a
> trustworthy attestation, which is what these `ATTEST-*` rules check.

## Fix

Produce SLSA provenance from a hosted, isolated builder (SLSA Build L3), and bind
the Statement `subject` to the image's real digest. Verify the builder identity
against an allowlist before promoting an image.

## References

- SLSA — Provenance & build levels: https://slsa.dev/spec/v1.0/provenance
- in-toto — Attestation framework / Statement: https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md
