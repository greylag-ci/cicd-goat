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
| trivy     | partial — its secret rules apply |
| gitleaks  | **Yes — primary scanner for this pattern** |

This is the scenario where a secret-scanner (Gitleaks) and an
expression-scanner (zizmor) overlap. Compare their findings: does
either flag *both* `LEGACY_API_TOKEN` and `DB_PASSWORD`? Does either
flag the password-shaped string at all, or only the hex one?

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
