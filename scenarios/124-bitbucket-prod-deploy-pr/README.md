# Scenario 124: Bitbucket — production deployment on a pull-request pipeline

**Provider:** Bitbucket Pipelines · **OWASP:** CICD-SEC-1 (Insufficient Flow Control) · **Severity: critical**

**Vulnerable pipeline:** [`bitbucket-pipelines.yml`](bitbucket-pipelines.yml)

## The pattern

```yaml
pipelines:
  pull-requests:
    '**':
      - step:
          deployment: production     # production tier on a PR pipeline
          script:
            - ./deploy.sh
```

A step under `pull-requests:` is bound to a production-tier `deployment:`
environment. The PR branch's code ships to production before it is reviewed or
merged, and the production deployment's scoped variables are exposed to
PR-controlled steps. Per-PR preview, `test`, and `staging` environments are
fine — only the production tier on a pull-request pipeline is the bug.

## How an attacker exploits it

A contributor opens a PR that edits `deploy.sh` (or any earlier build step). The
PR pipeline runs it with the **production** deployment's credentials and ships
the change live before any reviewer or merge gate. On a repo that allows
fork-PR pipelines, the attacker doesn't even need write access. The deploy-time
sibling of [scenario 123](../123-bitbucket-iac-apply-pr/README.md).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `BB-034` — _production deployment on a pull-request pipeline_ |
| Checkov | — |

## Fix

On pull requests, deploy only to an ephemeral preview or `test` environment.
Move the production `deployment:` into the `branches:` section for your default
branch (or a manual `custom:` pipeline) so it runs against merged, reviewed code
with the environment's required reviewers enforced.

## References

- Atlassian — Deployments & environments: https://support.atlassian.com/bitbucket-cloud/docs/set-up-and-monitor-deployments/
- Atlassian — Pull-request pipelines: https://support.atlassian.com/bitbucket-cloud/docs/pipeline-triggers/
