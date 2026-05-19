# Scenario 16: `curl | sh` toolcache poisoning

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse),
CICD-SEC-9 (Improper Artifact Integrity Validation)

**Vulnerable workflow:** [`.github/workflows/scenario-16-curl-pipe-sh.yml`](../../.github/workflows/scenario-16-curl-pipe-sh.yml)

## The pattern

`curl https://... | sh` (and variants: `wget -qO- | bash`,
`iwr -useb ... | iex`) downloads an install script and executes it
immediately with no integrity check. The runner trusts:

- That the URL still points to the same domain (DNS, registrar).
- That the host still serves the same bytes (account, build pipeline).
- That TLS terminates where you think it does (no MITM).
- That the upstream's own CI hasn't been compromised.

All four of these have been the *initial vector* of real CI/CD breaches
in the last few years. The fix isn't "trust the upstream more" — it's
"don't run unverified bytes."

## How an attacker exploits it

Several paths:

1. **Domain hijack:** the registrar expires, attacker re-registers, takes
   over the install URL. Happens to dead OSS projects, then "lives on"
   as a watering-hole.
2. **Maintainer account compromise:** attacker pushes an updated install
   script that does the original install *plus* whatever they want.
3. **CDN cache poisoning:** less common but documented for static install
   hosts on shared CDNs.
4. **Just a bad commit:** the maintainer's own runner gets compromised
   and force-updates the published script.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `unverified-script-download` (recent rule) |
| poutine   | `curl_pipe_shell` |
| checkov   | partial |
| kics      | "Untrusted Shell Script Execution" |
| trivy     | partial — config rules cover some patterns |
| gitleaks  | n/a |

## Fix

Pin to a known SHA-256 of the script and verify before executing:

```yaml
- run: |
    set -euo pipefail
    SCRIPT_SHA256="abc123...deadbeef"
    curl -sSL https://install.some-tool.example/v1.2.3.sh -o install.sh
    echo "${SCRIPT_SHA256}  install.sh" | sha256sum -c
    sh install.sh
```

Better: use the upstream's published GitHub Action (if any), pinned to
a commit SHA per [Scenario 03](../03-action-mutable-ref/README.md). Or
install from a package manager whose own integrity model you accept
(`apt`, `pip --require-hashes`, signed releases).

## References

- "curl | bash is malware":
  https://www.idontplaydarts.com/2016/04/detecting-curl-pipe-bash-server-side/
- GitHub docs — "Security hardening, never download external scripts
  without verification":
  https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
