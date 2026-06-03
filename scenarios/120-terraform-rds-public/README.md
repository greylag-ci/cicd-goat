# Scenario 120: Terraform — RDS publicly accessible + unencrypted

**Provider:** Terraform · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · CICD-SEC-2 · **Severity: high**

**Vulnerable file:** [`main.tf`](main.tf)

## The pattern

```hcl
resource "aws_db_instance" "main" {
  publicly_accessible = true
  storage_encrypted   = false
}
```

An RDS database reachable from the internet with encryption-at-rest off. A
pipeline that applies this provisions an internet-exposed database whose storage
is unprotected — the Terraform twin of CloudFormation scenario 116.

## How an attacker exploits it

Internet reachability exposes the DB to credential brute-force and engine CVEs;
unencrypted storage means a snapshot or disk-level compromise yields plaintext
data. The password is wired through a `sensitive` variable so the scanners flag
the *configuration* flaws, not a literal credential.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Trivy | reconciled from CI (RDS public-access + encryption misconfig) |
| Checkov | reconciled from CI |
| KICS | reconciled from CI |
| pipeline-check | — (its Terraform provider needs a plan JSON) |

## Fix

Set `publicly_accessible = false` and `storage_encrypted = true` (KMS CMK),
place the instance in private subnets, and reach it only via a bastion / VPN /
private endpoint.

## References

- AWS — RDS security best practices: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.Security.html
