# Scenario 113: GitLab — `CI_DEBUG_TRACE` leaks secrets to the job log

**Provider:** GitLab CI · **OWASP:** CICD-SEC-10 (Insufficient Logging & Visibility) · CICD-SEC-6 · **Severity: medium**

**Vulnerable file:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

```yaml
variables:
  CI_DEBUG_TRACE: "true"
```

`CI_DEBUG_TRACE` turns on full shell-trace logging for every job. GitLab's job
log masking is best-effort string matching; debug trace dumps the entire
**expanded** environment — including masked CI/CD variables and protected
secrets — into the job log. A logging/visibility control inverted into a
secret-exfiltration channel: the audit log itself becomes the leak.

## How an attacker exploits it

Anyone with Reporter access (or the job-trace API, or a cached/forwarded log)
reads the unmasked secrets straight out of the trace — cloud keys, registry
tokens, deploy credentials. No code execution needed; the secrets are sitting in
the logs by design.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-038` — `CI_DEBUG_TRACE` / debug logging dumps secrets to the job log |
| ciguard | — |
| Checkov | — |

> pipeline-check 1.9.0 added `GL-038`, which flags `CI_DEBUG_TRACE` debug logging.

## Fix

Never set `CI_DEBUG_TRACE` in committed CI config; if a maintainer needs it to
debug, enable it transiently on a protected branch and rotate every exposed
secret afterward. Treat job logs as a sink that must never receive secrets.

## References

- GitLab — debug logging & the `CI_DEBUG_TRACE` security warning: https://docs.gitlab.com/ee/ci/variables/index.html#enable-debug-logging
