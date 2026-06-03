# Scenario 119: Terraform — S3 bucket unencrypted + unversioned

**Provider:** Terraform · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: high**

**Vulnerable file:** [`main.tf`](main.tf)

## The pattern

```hcl
resource "aws_s3_bucket" "artifacts" {
  bucket = "build-artifacts-bucket"
}
```

The bucket has no server-side encryption configuration and no versioning. A
pipeline that applies this stores build artifacts unencrypted at rest, with no
way to recover an object after it's overwritten or deleted.

## How an attacker exploits it

Disk-level or snapshot access yields plaintext data (no encryption), and an
attacker who can write to the bucket can overwrite artifacts irreversibly (no
versioning) — useful for supply-chain tampering with no rollback.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Trivy | reconciled from CI (S3 encryption / versioning misconfig) |
| Checkov | reconciled from CI |
| KICS | reconciled from CI |
| pipeline-check | — (its Terraform provider needs a plan JSON) |

## Fix

Add `aws_s3_bucket_server_side_encryption_configuration` (SSE-KMS) and
`aws_s3_bucket_versioning` (Enabled) for the bucket; enable access logging and
a lifecycle/Object-Lock policy where artifacts must be immutable.

## References

- AWS — S3 security best practices: https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html
