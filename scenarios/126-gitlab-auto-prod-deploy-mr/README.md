# Scenario 126: GitLab CI — automatic production deployment on a merge-request pipeline

**Provider:** GitLab CI · **OWASP:** CICD-SEC-1 (Insufficient Flow Control) · **Severity: critical**

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

```yaml
deploy_prod:
  environment: production
  script: [./deploy.sh]
  rules:
    - if: $CI_PIPELINE_SOURCE == 'merge_request_event'   # auto, no when: manual
```

A job reachable on a merge-request pipeline binds a production-tier
`environment:` and is **not** gated by `when: manual`. GL-004 treats any
`environment:` as sufficient gating, so it misses this; `GL-044` names the
automatic-deploy shape and raises it to CRITICAL. Review-app, `test`, and
`staging` environments don't fire — only the production tier.

## How an attacker exploits it

A merge-request pipeline runs the MR branch's code. A contributor opens an MR
that edits `deploy.sh` (or any earlier build step); the MR pipeline runs it with
the **production** environment's scoped credentials and ships the change live —
on every MR, before review or merge. On fork MRs this is untrusted code reaching
production. The GitLab analogue of [scenario 124](../124-bitbucket-prod-deploy-pr/README.md).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-044` — _automatic production deployment on a merge-request pipeline_ |
| Checkov / ciguard | — |

## Fix

Deploy to an ephemeral review-app environment on MRs; gate the production
`environment:` job behind `when: manual` **and** a protected-branch rule
(`if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH`) so it runs against merged,
reviewed code.

## References

- GitLab — Environments and deployments: https://docs.gitlab.com/ee/ci/environments/
- GitLab — `rules` and pipeline types: https://docs.gitlab.com/ee/ci/yaml/#rules
