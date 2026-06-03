# Scenario 102: Terraform — S3 public-access-block disabled

**Provider:** Terraform · **OWASP:** CICD-SEC-7 · CICD-SEC-6

**Vulnerable file:** [`main.tf`](main.tf)

## The pattern

```hcl
resource "aws_s3_bucket_public_access_block" "data" {
  block_public_acls = false; block_public_policy = false
  ignore_public_acls = false; restrict_public_buckets = false
}
```

All four account/bucket public-access guards are disabled, so a bucket ACL or
policy can make the bucket world-readable/writable. A pipeline that applies this
(for build artifacts, state, or logs) can expose them publicly.

## How an attacker exploits it

With the guards off, a permissive ACL/policy (set here or later) exposes the
bucket; attackers read sensitive artifacts/state or overwrite objects to poison
downstream deploys.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Checkov | `CKV_AWS_53` — S3 bucket block-public-ACLs enabled (and `_54/_55/_56` for the other guards) |
| KICS | `S3 Bucket Allows Public ACL` (`d0cc8694-…`) — public-access-block guards off |
| pipeline-check | — (Terraform needs a plan JSON) |

## Fix

Set all four to `true`; keep the bucket private; use bucket policies + IAM for
controlled access; enable encryption, versioning, and access logging.

## References

- Checkov — Terraform/AWS policies: https://www.checkov.io/5.Policy%20Index/terraform.html
- AWS — S3 Block Public Access: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
