# Scenario 100: Terraform — IAM policy `*:*` (full admin)

**Provider:** Terraform · **OWASP:** CICD-SEC-2 (Inadequate IAM) · **Severity: critical**

**Vulnerable file:** [`main.tf`](main.tf)

## The pattern

```hcl
policy = jsonencode({ Statement = [{ Effect = "Allow", Action = "*", Resource = "*" }] })
```

An IAM policy granting every action on every resource. When a pipeline applies
this and attaches it to a build/deploy role (or a workload), any compromise
becomes full cloud-account compromise.

## How an attacker exploits it

A foothold on anything using this policy can read every secret, modify every
resource, create backdoor users/roles, and disable logging — total account
takeover.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Checkov | `CKV_AWS_62` — IAM policy grants full `*-*` administrative privileges (also fires `CKV_AWS_355/63`) |
| KICS | `IAM Policies With Full Privileges` (`2f37c4a3-…`) |
| Trivy | — (its ruleset doesn't flag the IAM `*:*` wildcard here — honest miss) |
| pipeline-check | — (its Terraform provider needs a `terraform show -json` plan, not raw `.tf`) |

## Fix

Scope `Action` and `Resource` to the minimum the principal needs (least
privilege); never `"*":"*"`. Use permission boundaries and access analyzers.

## References

- Checkov — Terraform/AWS policies: https://www.checkov.io/5.Policy%20Index/terraform.html
- AWS — IAM least-privilege guidance: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
