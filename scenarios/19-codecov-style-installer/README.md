# Scenario 19: Codecov-style trusted-installer compromise

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse),
CICD-SEC-9 (Improper Artifact Integrity Validation)

**Vulnerable workflow:** [`.github/workflows/scenario-19-codecov-style-installer.yml`](../../.github/workflows/scenario-19-codecov-style-installer.yml)

## The pattern

This is the cousin of [Scenario 16 (`curl | sh`)](../16-curl-pipe-sh/README.md) —
but with all the *responsible* mitigations bolted on:

```bash
curl ... -o tool
curl ... -o tool.sha256
curl ... -o tool.sha256.sig
gpg --verify tool.sha256.sig tool.sha256
sha256sum --check tool.sha256
chmod +x tool && ./tool
```

This looks like the textbook fix. It fails open against the **Codecov
2021 incident**: the attacker compromised Codecov's own build pipeline
and modified the bash uploader *before* the publisher's signing system
ran. The signature was valid. The SHA-256 matched. The binary was
malicious. ~29,000 customers ran the modified uploader for ~2 months;
the payload was env-var exfiltration.

The corrupted-supply-chain failure modes the signing-and-checksumming
flow doesn't catch:

- Publisher's CI runner is owned, malicious bytes get signed by the
  legitimate signing path (Codecov 2021, SolarWinds 2020).
- Publisher's signing key is hot in CI (i.e. usable by any CI job),
  attacker triggers signing of an arbitrary payload.
- Publisher rotates the signing key under duress; you don't notice.

## How an attacker exploits it

You don't break the crypto. You compromise the upstream's CI or
account, push a malicious patch that goes through their own pipeline,
let it be signed normally, and wait. Every downstream consumer who
trusts "any signature from this key" executes the payload.

## Expected scanner coverage

| Scanner            | Detection                                                                     |
| :----------------- | :---------------------------------------------------------------------------- |
| **pipeline-check** | ❌ `GHA-016` / `GHA-018` don't currently fire on this signed-and-checksummed install path; over-verified supply-chain compromise needs a dedicated rule |
| zizmor             | ⚠️ `unverified-script-download` partial — checks for unverified, not over-verified |
| poutine            | ❌                                                                            |
| KICS               | ❌                                                                            |
| Checkov            | ❌                                                                            |
| Trivy              | ❌                                                                            |
| Gitleaks           | —                                                                             |

## Fix

Pin the installer to a **known-good release digest**, not "any signature
from this key":

```yaml
- run: |
    EXPECTED_SHA="e8b1f...known-good"
    curl -fLso codecov "https://uploader.coverage-provider.example/v0.7.4/linux/codecov"
    echo "${EXPECTED_SHA}  codecov" | sha256sum -c
    chmod +x codecov
```

Even better: install via your package manager's signed-release flow
*with a frozen lockfile*, or via an OCI image you've previously
mirrored and pinned by digest. Whatever you do, the trust root has to
be a value you control, not "the maintainer's signature on this build."

## References

- HashiCorp's write-up of Codecov 2021:
  https://discuss.hashicorp.com/t/hcsec-2021-12-codecov-security-event-and-hashicorp-gpg-key-exposure/23512
- SLSA framework — provenance + immutable references:
  https://slsa.dev/
