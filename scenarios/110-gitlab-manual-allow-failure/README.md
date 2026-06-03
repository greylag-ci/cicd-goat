# Scenario 110: GitLab — manual deploy defaults to `allow_failure`

**Provider:** GitLab CI · **OWASP:** CICD-SEC-1 (Insufficient Flow Control Mechanisms) · **Severity: medium**

**Vulnerable file:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

```yaml
deploy-prod:
  stage: deploy
  when: manual          # looks like an approval gate...
  script: [./deploy.sh production]
```

A `when: manual` production deploy job looks like an approval gate in the UI.
But manual jobs default to **`allow_failure: true`**, so the pipeline reports
success — and downstream jobs proceed — whether or not anyone ever clicks the
button. The gate enforces nothing.

## How an attacker exploits it

The team believes prod deploys require a manual approval; in practice the
pipeline passes green with the job never run, and any later stage that depends
on "pipeline success" runs as though it were approved. More subtly, the visible
"gate" creates false assurance — there is no real flow-control checkpoint
between merge and production.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-029` — manual deploy job defaults to `allow_failure: true` |
| ciguard | reconciled from CI |
| Checkov | reconciled from CI (thin GitLab ruleset) |

## Fix

Set `allow_failure: false` on manual gate jobs so the pipeline can't pass
without them, and enforce approval out-of-band: protected environments with
required approvers, or merge-request approval rules — not a manual job alone.

## References

- GitLab — `allow_failure` and manual jobs: https://docs.gitlab.com/ee/ci/yaml/#allow_failure
