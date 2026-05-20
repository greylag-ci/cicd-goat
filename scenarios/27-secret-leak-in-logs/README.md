# Scenario 27: Secret leak in workflow logs

**OWASP CICD-SEC mapping:** CICD-SEC-10 (Insufficient Logging and Visibility)

**Vulnerable workflow:** [`.github/workflows/scenario-27-secret-leak-in-logs.yml`](../../.github/workflows/scenario-27-secret-leak-in-logs.yml)

## The pattern

GitHub Actions masks secret values in workflow logs — **as registered**.
Three common ways the masking fails open:

1. **`set -x` echoes the command before substitution masking applies
   uniformly.** Some shells echo the *expanded* form; depending on
   shell and quoting, the secret can land in the trace.
2. **Credentials in URL query strings.** GHA's masking matches exact
   secret values. If the secret is wrapped in a longer string that
   only *contains* it (URL-encoded, prepended with `?key=`,
   concatenated with other text), masking can miss.
3. **Derived values.** The fingerprint, the first 8 characters, the
   SHA-256, the base64 — none of those are the registered secret, so
   none of them are masked. But any of them can be enough to brute
   the rest, or to identify the secret across leaks.

Public-repo workflow logs are world-readable, indexed by search
engines, and downloadable as artifacts. Any leak here is a permanent
disclosure unless you rotate the secret immediately.

## How an attacker exploits it

Passively: trawl public repos' workflow logs for partial credentials
(prefix matches against known issuer formats — `ghp_`, `ghs_`, `xoxb-`,
`AKIA`, etc.). Even an 8-character prefix lets you fingerprint which
provider it came from and which org owns it.

Actively: if you can get a PR or comment to trigger a workflow that
leaks the secret (combine with Scenario 02), do it once and harvest.

## Expected scanner coverage

| Scanner            | Detection                                                                            |
| :----------------- | :----------------------------------------------------------------------------------- |
| **pipeline-check** | ✅ `GHA-033` (`set -x` + secret-bound env var anywhere in the body); derived-value echoes still slip past |
| zizmor             | ❌                                                                                   |
| poutine            | ❌                                                                                   |
| KICS               | ❌                                                                                   |
| Checkov            | ❌                                                                                   |
| Trivy              | ❌                                                                                   |
| Gitleaks           | ⚠️ Only if the leaked output gets committed back into the repo                      |

> CICD-SEC-10 is the hardest category to scan statically — most of the
> failure happens at runtime, in the log output. Pipeline-check
> catches the predicate patterns (`set -x`, credential-in-URL,
> derived-from-secret echoes); the rest of the field doesn't try.

## Fix

Three rules:

1. **Never `set -x` in a step that touches secrets.** If you need shell
   tracing for debugging, do it in a separate step that has the
   secrets unset.
2. **Pass credentials via header / env / stdin**, never via URL query
   string. `curl -H "Authorization: Bearer $API_KEY"` is masked
   correctly because the secret stands alone on the command line.
3. **Don't echo anything derived from a secret.** Not the fingerprint,
   not the prefix, not the SHA. If you genuinely need to compare
   secrets across runs (rare), do it inside a step and report a
   boolean.

```yaml
- env:
    API_KEY: ${{ secrets.API_KEY }}
  run: |
    curl -fsS -X POST \
      -H "Authorization: Bearer $API_KEY" \
      "https://api.example.com/deploy"
```

## References

- GitHub docs — Workflow commands, "Masking a value":
  https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#masking-a-value-in-log
- OWASP CICD-SEC-10:
  https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-10-Insufficient-Logging-and-Visibility
