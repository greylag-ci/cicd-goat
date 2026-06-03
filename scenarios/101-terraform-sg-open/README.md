# Scenario 101: Terraform — security group SSH open to `0.0.0.0/0`

**Provider:** Terraform · **OWASP:** CICD-SEC-7 (Insecure System Configuration)

**Vulnerable file:** [`main.tf`](main.tf)

## The pattern

```hcl
ingress { from_port = 22; to_port = 22; protocol = "tcp"; cidr_blocks = ["0.0.0.0/0"] }
```

A security group exposing SSH (port 22) to the entire internet. Applied by a
pipeline, it puts the instance's SSH directly on the public internet.

## How an attacker exploits it

The host is immediately subject to internet-wide SSH brute-force / 0-day
exposure; one weak/leaked key or vuln = shell on the instance.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Checkov | `CKV_AWS_24` — no security group allows ingress from `0.0.0.0/0` to port 22 |
| KICS | (reconciled from CI) |
| pipeline-check | — (Terraform needs a plan JSON) |

## Fix

Restrict `cidr_blocks` to known admin CIDRs / a bastion / VPN; prefer SSM
Session Manager over open SSH; never `0.0.0.0/0` on 22 (or 3389/databases).

## References

- Checkov — Terraform/AWS policies: https://www.checkov.io/5.Policy%20Index/terraform.html
