# Scenario 115: CloudFormation — IAM managed policy `*:*` (full admin)

**Provider:** CloudFormation · **OWASP:** CICD-SEC-2 (Inadequate IAM) · **Severity: critical**

**Vulnerable file:** [`template.yaml`](template.yaml)

## The pattern

```yaml
PolicyDocument:
  Statement:
    - { Effect: Allow, Action: '*', Resource: '*' }
```

A managed IAM policy granting every action on every resource. A pipeline that
creates and attaches this to a role or user turns any compromise into full
cloud-account takeover — the CloudFormation twin of the Terraform IAM scenario
(100).

## How an attacker exploits it

Anything using this policy can read every secret, modify every resource, create
backdoor principals, and disable logging — total account compromise.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Checkov | `CKV_AWS_109` — IAM policy allows permissions management without constraints (the `*` action) |
| KICS | `IAM policy allows for data exfiltration` (`022f8938-…`) |
| Trivy | — (its CFN ruleset doesn't flag the `*:*` wildcard here — honest miss, mirrors Terraform 100) |
| pipeline-check | — (CloudFormation ruleset thin / non-attributable) |

## Fix

Scope `Action` and `Resource` to least privilege; never `"*":"*"`. Use
permission boundaries and access analyzers.

## References

- AWS — IAM least-privilege guidance: https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html
