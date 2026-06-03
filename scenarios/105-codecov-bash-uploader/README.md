# Scenario 105: GHA — Codecov-style remote uploader piped to a shell

**Provider:** GitHub Actions · **OWASP:** CICD-SEC-8 (Ungoverned Usage of 3rd Party Services) · CICD-SEC-3 · **Severity: high**

**Vulnerable file:** [`.github/workflows/scenario-105-codecov-bash-uploader.yml`](../../.github/workflows/scenario-105-codecov-bash-uploader.yml)

## The pattern

```yaml
run: curl -s https://codecov.io/bash | bash
```

The pipeline trusts a third-party service by piping a remote script straight
into a shell. Whatever that endpoint serves at run time executes in the runner
with the job's full environment — every secret, token, and cloud credential.

## How an attacker exploits it

This is the exact shape of the **Codecov 2021** breach: attackers modified the
bash uploader upstream and it quietly exfiltrated CI environment variables from
thousands of pipelines for months. A SHA-256 check or GPG signature wouldn't
have helped — the malicious uploader was signed by Codecov's own (compromised)
release pipeline. Anyone who controls the endpoint, the CDN, or DNS gets RCE in
your runner.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GHA-016` — remote script piped to a shell interpreter (curl-pipe / Codecov shape) |
| poutine | `unverified_script_exec` — remote script executed unverified |
| zizmor / KICS / Checkov / actionlint / octoscan | — (miss) |

## Fix

Download the uploader to a file, verify it against an **upstream-attested
provenance** reference (`slsa-verifier`, `gh attestation verify`,
`cosign verify-attestation`) or a pinned release digest — not just any
signature — then execute. Better, vendor the script into the repo and review
changes through PR.

## References

- Codecov 2021 bash-uploader compromise: https://about.codecov.io/security-update/
- SLSA provenance verification: https://slsa.dev/
