# Scenario 103: CloudFormation — S3 bucket public read+write

**Provider:** CloudFormation · **OWASP:** CICD-SEC-7 · CICD-SEC-6

**Vulnerable file:** [`template.yaml`](template.yaml)

## The pattern

```yaml
ArtifactsBucket:
  Type: AWS::S3::Bucket
  Properties:
    AccessControl: PublicReadWrite
```

A CloudFormation template that creates an S3 bucket with a world-readable **and**
world-writable ACL. A pipeline that deploys this stack exposes the bucket's
contents and lets anyone overwrite them.

## How an attacker exploits it

Anyone on the internet lists/reads the bucket (data exposure) and writes to it
(tamper with artifacts/state consumed by later deploys → supply-chain poisoning).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Checkov | `CKV_AWS_20` (public READ) + `CKV_AWS_57` (public WRITE) — both fire on the `PublicReadWrite` ACL |
| KICS | `S3 Bucket Allows Public ACL` (`48f100d9-…`) |
| Trivy | `AWS-0086` — S3 bucket should block public ACLs |
| pipeline-check | — (its CloudFormation ruleset is thin / non-attributable) |

> Two-scanner agreement: Checkov's CloudFormation framework and KICS both parse
> the template and flag the public ACL directly — no AWS account or deploy
> needed.

## Fix

Use `AccessControl: Private` (or omit it) and add a
`PublicAccessBlockConfiguration` with all four guards enabled; grant access via
scoped bucket policies / IAM only.

## References

- KICS — CloudFormation queries: https://docs.kics.io/latest/queries/cloudformation-queries/
- AWS — S3 Block Public Access: https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html
