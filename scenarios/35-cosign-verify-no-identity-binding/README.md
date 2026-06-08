# Scenario 35: `cosign verify` without identity binding (signed-but-not-bound)

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse),
CICD-SEC-9 (Improper Artifact Integrity Validation)

**Vulnerable workflow:** [`.github/workflows/scenario-35-cosign-verify-no-identity-binding.yml`](../../.github/workflows/scenario-35-cosign-verify-no-identity-binding.yml)

## The pattern

`cosign verify` in keyless Sigstore mode checks two things:

1. The signature is cryptographically valid for the blob/image.
2. The certificate chains to the Sigstore root.

**It does *not* check who the signer was unless you tell it to.**
Without `--certificate-identity` / `--certificate-identity-regexp`
and `--certificate-oidc-issuer`, the verify command will happily
accept a signature minted by anyone who could run a workflow on
github.com (i.e. anyone) — including the attacker who replaced the
artifact on the CDN.

A passing `cosign verify` *without identity binding* is closer to a
checksum than a trust assertion: it proves the bytes weren't
corrupted in transit, not that they came from someone you trust.

## How an attacker exploits it

1. Compromise the CDN, S3 bucket, or release host that serves
   `installer`, `installer.sig`, and `installer.crt`.
2. Build a malicious `installer` binary.
3. Sign it with cosign keyless from a workflow on the attacker's
   GitHub account — produces a valid `.sig` and `.crt` pair signed
   by the Sigstore root, just with a different signer identity.
4. Replace all three files at the CDN.
5. The next CI run fetches the malicious bundle, `cosign verify-blob`
   accepts it (signature valid, cert valid, no identity pin), and
   `./installer` runs the attacker's code with the workflow's
   permissions.

## Expected scanner coverage

| Scanner | Detection |
|---|---|
| pipeline-check | `GHA-100` — _`cosign verify` without certificate identity binding_ |
| others | ❌ — no other scanner here distinguishes "verify with identity pin" from "verify without identity pin" |

pipeline-check is **solo** on this one. The check is exactly the static-YAML
signature the older writeup anticipated: the `cosign verify` line either carries
`--certificate-identity*` **and** `--certificate-oidc-issuer` or it doesn't.
A formerly "hard case" (alongside #10 / #22 / #19) that a single scanner now
covers.

## Fix

Pin the signer identity to the workflow that legitimately produces
the artifact, and the OIDC issuer to the GitHub Actions OIDC provider:

```yaml
- run: |
    cosign verify-blob \
      --certificate-identity-regexp '^https://github\.com/your-org/your-build-repo/\.github/workflows/release\.yml@.*$' \
      --certificate-oidc-issuer 'https://token.actions.githubusercontent.com' \
      --signature installer.sig \
      --certificate installer.crt \
      installer
```

Now an attacker can no longer mint a passing signature from their own
GitHub account — the verifier requires the cert subject to match the
specific workflow file in the specific repo.

## References

- Sigstore docs — "Verifying signatures":
  https://docs.sigstore.dev/cosign/verifying/verify/#keyless-verification-of-signed-blob
- Sigstore policy-controller — identity-binding documentation:
  https://docs.sigstore.dev/policy-controller/overview/
