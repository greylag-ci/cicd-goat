# Scenario 108: GHA — deploy job missing environment binding

**Provider:** GitHub Actions · **OWASP:** CICD-SEC-1 (Insufficient Flow Control Mechanisms) · **Severity: medium**

**Vulnerable file:** [`.github/workflows/scenario-108-deploy-no-environment.yml`](../../.github/workflows/scenario-108-deploy-no-environment.yml)

## The pattern

```yaml
on: { push: { branches: [main] } }
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - run: aws s3 sync ./dist s3://prod-site-bucket --delete
```

The deploy job has no `environment:` binding. GitHub's deployment protections —
required reviewers, deployment-branch policies, wait timers — all attach to an
**environment**. Without one, there is no gate.

## How an attacker exploits it

Any commit that reaches `main` deploys immediately: a self-merged PR, a typo'd
hotfix, or a push from a compromised contributor token ships straight to
production with no second pair of eyes. This is the canonical
insufficient-flow-control gap — code moves to prod without an approval step.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GHA-014` — deploy job missing `environment:` binding |
| zizmor / poutine / KICS / Checkov / actionlint / octoscan | reconciled from CI |

## Fix

Bind deploy jobs to a protected `environment:` (`environment: production`) and
configure required reviewers, a deployment-branch policy (exact branch/tag), and
a wait timer on that environment in repo settings.

## References

- GitHub — using environments for deployment (protection rules): https://docs.github.com/actions/deployment/targeting-different-environments/using-environments-for-deployment
