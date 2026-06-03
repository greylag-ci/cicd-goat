# Scenario 44: GitLab — hardcoded secret in `variables:`

**Provider:** GitLab CI/CD

**OWASP CICD-SEC mapping:** CICD-SEC-6 (Insufficient Credential Hygiene)

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

A credential is pasted straight into the pipeline's `variables:` block:

```yaml
variables:
  LEGACY_API_TOKEN: "deadbeefcafef00dfeedfacebadc0ffee0ddf00d"
  DB_PASSWORD: "P@ssw0rd-do-not-actually-do-this"
```

It's now visible to anyone who can read the repo, anyone who can read a job
log, and anyone who greps a runner for tokens of that shape — and it lives in
git history forever. The GitLab analogue of
[scenario 15](../15-hardcoded-secret-env/README.md). (The token here is a fake
40-char hex fixture, matching generic secret-scanner patterns but no real
provider's format.)

## How an attacker exploits it

Read access to the repo (or to one cached log line) hands over the credential
directly. No pipeline execution is even required.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-003` — Variables contain literal secret values |
| ciguard | `IAM-001` — Hardcoded secret in variable (also `IAM-003`) |
| Checkov | — |

## Fix

Never commit secrets in `variables:`. Store them as **Protected + Masked** (or
Hidden) CI/CD variables restricted to protected branches, or — better — pull
them at runtime from Vault / an external secret manager via `secrets:`.

## References

- GitLab Docs — CI/CD variables (protect / mask / hide): https://docs.gitlab.com/ci/variables/
- GitLab Docs — Pipeline security: https://docs.gitlab.com/ci/pipeline_security/
