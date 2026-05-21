# Scenario 15: Hardcoded secret in `env:`

**OWASP CICD-SEC mapping:** CICD-SEC-6 (Insufficient Credential Hygiene)

**Vulnerable workflow:** [`.github/workflows/scenario-15-hardcoded-secret-env.yml`](../../.github/workflows/scenario-15-hardcoded-secret-env.yml)

## The pattern

A credential pasted into the workflow source is visible to:

- Anyone who can read the repository (it's `git show HEAD:.github/...`).
- Anyone who can read a *historic* commit of the repository — `git
  rewrite` and `git push --force` don't fully scrub history if anyone
  cloned in between.
- Anyone who can read a cached workflow log (logs scrub `secrets.*` but
  not values pasted as literals into `env:`).
- Anyone who greps GitHub for tokens of that shape.

The fake token in this scenario (`deadbeef...`) matches a 40-char hex
pattern — the same shape as a classic GitHub PAT.

## How an attacker exploits it

`grep -E '[0-9a-f]{40}' .github/workflows/*.yml` — or just open the file
in the GitHub web UI. No exploitation needed; you're handing it over.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `hardcoded-credentials` (when value matches a known token shape) |
| poutine   | `secrets_in_workflow` |
| checkov   | partial — focuses on AWS/Azure key shapes |
| kics      | "Hardcoded Secret in Workflow" |

Note that "hardcoded secret in YAML" is fundamentally a *secret
scanner's* problem class — Gitleaks / TruffleHog / detect-secrets are
the right primary tools and they belong in a source-secrets bench,
not in this CI/CD-workflow corpus. The scanners listed above catch
this scenario as a side effect (KICS has an explicit workflow-secrets
rule; zizmor and pipeline-check pattern-match known token shapes).

## Fix

Move the value to repo / org / environment secrets and read it via
`${{ secrets.NAME }}`:

```yaml
env:
  LEGACY_API_TOKEN: ${{ secrets.LEGACY_API_TOKEN }}
```

Even better: kill long-lived tokens entirely, switch to OIDC + short-lived
credentials ([Scenario 10](../10-oidc-aws-wildcard-sub/README.md)
shows how to do that *correctly*).

## References

- GitHub docs — "Using secrets in GitHub Actions":
  https://docs.github.com/en/actions/security-guides/encrypted-secrets
