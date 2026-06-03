# Scenario 112: Terraform — VPC flow logs + S3 access logging off

**Provider:** Terraform · **OWASP:** CICD-SEC-10 (Insufficient Logging & Visibility) · **Severity: medium**

**Vulnerable file:** [`main.tf`](main.tf)

## The pattern

```hcl
resource "aws_vpc" "main"   { cidr_block = "10.0.0.0/16" }   # no aws_flow_log
resource "aws_s3_bucket" "data" { bucket = "app-data-bucket" } # no logging
```

A VPC with no flow logs and an S3 bucket with no access logging. Network traffic
leaves no record, and reads/writes to the bucket aren't logged. A pipeline that
applies this provisions infrastructure that is, by construction, unobservable.

## How an attacker exploits it

Lateral movement, data staging, and exfiltration through this VPC and bucket
produce no telemetry — there's nothing for detection or incident response to
query after the fact. The gap isn't a direct exploit so much as the absence of
the evidence needed to notice or investigate one.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Checkov | `CKV_AWS_18` — S3 bucket access logging (also fires `CKV2_AWS_11` VPC flow-log graph check) |
| KICS | `VPC FlowLogs Disabled` (`f83121ea-…`) + `S3 Bucket Logging Disabled` (`f861041c-…`) |
| Trivy | `AWS-0178` — VPC Flow Logs not enabled |
| pipeline-check | — (its Terraform provider needs a plan JSON) |

## Fix

Attach an `aws_flow_log` to every VPC (to CloudWatch Logs or S3) and configure
`aws_s3_bucket_logging` (or the `logging {}` block) on buckets; centralize logs
and set retention so they survive an incident.

## References

- Checkov — Terraform/AWS policies: https://www.checkov.io/5.Policy%20Index/terraform.html
- AWS — VPC Flow Logs: https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html
