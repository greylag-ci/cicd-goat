# Scenario 127: Azure Pipelines — IaC apply on a PR-validated pipeline (IaC RCE)

**Provider:** Azure Pipelines · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: critical**

**Vulnerable pipeline:** [`azure-pipelines.yml`](azure-pipelines.yml)

## The pattern

```yaml
trigger: [main]
pr: [main]                    # PR validation: runs the PR branch's scripts
steps:
  - script: |
      terraform init
      terraform apply -auto-approve
```

The pipeline opts into PR validation (`pr:` set to a real branch list) and a
`script:` step runs an IaC apply. A `pr:`-validated pipeline runs the PR
branch's YAML and scripts, so the apply executes untrusted IaC. A pipeline with
no `pr:` key (or `pr: none`) would be out of scope.

## How an attacker exploits it

A contributor opens a PR whose `.tf` adds an `external` data source or a
`local-exec` provisioner; `terraform apply` runs it on the agent with whatever
cloud credentials (often a federated service connection) the apply uses, before
the change is reviewed or merged. The Azure DevOps analogue of GHA
[scenario 89](../89-iac-apply-untrusted/README.md), GitLab
[91](../91-gitlab-iac-apply-mr/README.md), and Bitbucket
[123](../123-bitbucket-iac-apply-pr/README.md).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ADO-033` — _IaC apply on a PR-validated pipeline_ |
| Checkov | — |

## Fix

On PR validation run a read-only `plan`; move the `apply` onto the default-branch
(`trigger:`) leg, in a `deployment:` job gated by a protected `environment:`, so
it runs against merged, reviewed code.

## References

- Microsoft — Build validation / PR triggers: https://learn.microsoft.com/en-us/azure/devops/pipelines/repos/github#pr-triggers
- Microsoft — Environments & approvals: https://learn.microsoft.com/en-us/azure/devops/pipelines/process/environments
