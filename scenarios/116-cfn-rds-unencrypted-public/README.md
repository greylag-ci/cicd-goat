# Scenario 116: CloudFormation — RDS unencrypted + publicly accessible

**Provider:** CloudFormation · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · CICD-SEC-2 · **Severity: high**

**Vulnerable file:** [`template.yaml`](template.yaml)

## The pattern

```yaml
StorageEncrypted: false
PubliclyAccessible: true
```

An RDS database with encryption-at-rest disabled and public accessibility on. A
pipeline that deploys this stack provisions an internet-reachable database whose
storage is unprotected.

## How an attacker exploits it

The database is reachable from the internet (brute-force / exposed credentials /
CVE) and, because storage isn't encrypted, a snapshot or disk-level compromise
yields plaintext data. Two independent exposure surfaces on one resource.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Trivy | reconciled from CI (RDS encryption + public-access misconfig) |
| Checkov | reconciled from CI |
| KICS | reconciled from CI |
| pipeline-check | — (CloudFormation ruleset thin / non-attributable) |

## Fix

Set `StorageEncrypted: true` (KMS CMK), `PubliclyAccessible: false`, place the
instance in private subnets, and reach it only through a bastion / VPN / private
endpoint.

## References

- AWS — RDS security best practices: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_BestPractices.Security.html
