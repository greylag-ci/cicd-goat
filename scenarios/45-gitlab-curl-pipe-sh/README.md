# Scenario 45: GitLab — `curl | sh` in `before_script`

**Provider:** GitLab CI/CD

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

A job fetches a remote installer and pipes it straight into a shell:

```yaml
before_script:
  - curl -sSL https://get.example.com/install.sh | sh
```

There is no pinning, no checksum, no signature. Whatever the host serves runs
with the runner's privileges and the job's secrets in scope.

## How an attacker exploits it

The upstream host — or anyone who can move a tag, poison a CDN cache, or MITM
the connection — serves a malicious script that executes on the runner. This is
the same mechanism as the Codecov bash-uploader compromise
([scenarios 16](../16-curl-pipe-sh/README.md) / [19](../19-codecov-style-installer/README.md)).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-016` — Remote script piped to shell interpreter |
| ciguard | `SC-001` — External script execution (also `PIPE-003`) |
| Checkov | — (its `CKV_GITLABCI_1` keys on curl carrying a CI variable, not on the pipe-to-shell shape) |

## Fix

Vendor the installer or a pinned release artifact; verify a known
checksum/signature before executing; never pipe network output directly into a
shell.

## References

- GitLab Docs — Pipeline security: https://docs.gitlab.com/ci/pipeline_security/
