# Scenario 107: GHA — org secret handed to an unpinned 3rd-party action

**Provider:** GitHub Actions · **OWASP:** CICD-SEC-8 (Ungoverned Usage of 3rd Party Services) · CICD-SEC-6 · **Severity: high**

**Vulnerable file:** [`.github/workflows/scenario-107-thirdparty-action-broad-secret.yml`](../../.github/workflows/scenario-107-thirdparty-action-broad-secret.yml)

## The pattern

```yaml
env:
  DEPLOY_API_KEY: ${{ secrets.DEPLOY_API_KEY }}   # workflow scope
jobs:
  publish:
    steps:
      - uses: acme-deploy/publish-action@v2         # unpinned 3rd-party
        with: { api-key: ${{ env.DEPLOY_API_KEY }} }
```

A workflow-scope `env:` publishes an org secret to **every job and every step**,
and that secret is handed to an unpinned, unverified third-party marketplace
action. Two ungoverned-3rd-party failures stack: the action can be re-pointed
under you at any time (mutable `@v2`), and the secret's blast radius is the
whole workflow rather than the one step that needs it.

## How an attacker exploits it

If the third-party action is compromised (maintainer takeover, mutable-tag
swap) it already has the deploy key in its process env. Even a different
compromised step — an injected `run:`, a poisoned cache, an upstream action
takeover — can read `DEPLOY_API_KEY` from its own environment, because the
workflow-scope `env:` leaks it everywhere.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GHA-072` — secret in `env:` at a wider scope than its consumer (also fires `GHA-001` for the unpinned action) |
| zizmor | `unpinned-uses` — third-party action not pinned to a digest |
| poutine | `github_action_from_unverified_creator_used` |
| KICS | unpinned-action query (`555ab8f9-…`) |
| octoscan | `repo-jacking` — unpinned action is repo-jackable |
| Checkov / actionlint | — (miss) |

> The corpus's richest 3rd-party row: pipeline-check names the over-scoped
> secret while four other scanners independently flag the unpinned/unverified
> action it's handed to.

## Fix

Scope the secret `env:` to the single step that consumes it, never workflow- or
job-level. Pin third-party actions to a full commit SHA, prefer verified
creators, and grant each integration the minimum secret and `permissions:` it
needs.

## References

- GitHub — security hardening for Actions (least privilege, pinning): https://docs.github.com/actions/security-guides/security-hardening-for-github-actions
