# Scenario 43: GitLab — secret job on a fork merge-request pipeline

**Provider:** GitLab CI/CD

**OWASP CICD-SEC mapping:** CICD-SEC-1 (Insufficient Flow Control) · CICD-SEC-6 (Insufficient Credential Hygiene)

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

A secret-bearing deploy job is gated to run on merge-request pipelines:

```yaml
deploy-on-mr:
  rules:
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  script:
    - curl -H "Authorization: Bearer $DEPLOY_TOKEN" https://deploy.example.com/release
```

GitLab can be configured to **run fork merge-request pipelines in the parent
project**. When it is, the fork's MR code executes in the *parent* context —
with the parent's protected variables (`$DEPLOY_TOKEN`) in scope, and no human
gate before the privileged step. This is the GitLab analogue of GitHub's
`pull_request_target` fork RCE ([scenario 01](../01-prtarget-checkout-head/README.md)).

## How an attacker exploits it

An attacker forks the project, opens an MR whose pipeline reaches the
secret-bearing job, and exfiltrates `$DEPLOY_TOKEN` (or runs arbitrary build
steps with it in scope) — no maintainer privileges required.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-004` — deploy job lacks manual approval / environment gate |
| ciguard | `PIPE-004` — Unprotected deploy job |
| Checkov | — |

> Both scanners catch the *missing gate* that is the core of the exposure;
> neither models the fork-in-parent setting (which lives in project settings).

## Fix

Don't run fork MR code in the parent with secrets. Gate secret-bearing jobs to
the parent project and protected branches
(`$CI_PROJECT_PATH == "trusted/repo"`, `$CI_COMMIT_REF_PROTECTED == "true"`),
and require `when: manual` review before any privileged job.

## References

- GitLab Docs — Merge request pipelines: https://docs.gitlab.com/ci/pipelines/merge_request_pipelines/
- GitLab Docs — Pipeline security: https://docs.gitlab.com/ci/pipeline_security/
