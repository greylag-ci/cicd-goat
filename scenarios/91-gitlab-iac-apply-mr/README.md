# Scenario 91: GitLab — `terraform apply` in a merge-request pipeline (IaC RCE)

**Provider:** GitLab CI/CD · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: critical**

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

```yaml
rules:
  - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
script:
  - terraform init
  - terraform apply -auto-approve     # MR-controlled IaC
```

Terraform executes code at plan/apply time (`external` data sources,
`local-exec`/custom provisioners, arbitrary providers), so running `apply` on
merge-request-controlled `.tf` is arbitrary code execution on the runner — the
GitLab twin of [scenario 89](../89-iac-apply-untrusted/README.md).

## How an attacker exploits it

An MR adds an `external` data source (or `local-exec` provisioner) whose program
exfiltrates the job's secrets / cloud credentials; `terraform apply` runs it on
the runner. With fork MRs runnable in the parent (scenario 43), a fork author
gets this directly.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-004` — deploy job lacks manual approval / environment gate (the ungated-MR-deploy half) |
| Checkov | — |
| ciguard | — |

> `GL-004` flags the missing gate on an MR-triggered privileged job; the
> *apply-on-untrusted-input RCE* specifics are a next-gen target no scanner here
> models yet.

## Fix

Run `plan` only on MRs, in a job with **no** cloud credentials and `external`/
`local-exec` disabled; gate `apply` to protected branches with manual approval;
vendor + pin providers/modules.

## References

- GitLab — Pipeline security: https://docs.gitlab.com/ci/pipeline_security/
- HashiCorp — Terraform `external` data source: https://registry.terraform.io/providers/hashicorp/external/latest/docs/data-sources/external
