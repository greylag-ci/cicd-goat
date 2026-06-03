# Scenario 111: Terraform — CloudTrail logging disabled / single-region

**Provider:** Terraform · **OWASP:** CICD-SEC-10 (Insufficient Logging & Visibility) · **Severity: high**

**Vulnerable file:** [`main.tf`](main.tf)

## The pattern

```hcl
resource "aws_cloudtrail" "main" {
  enable_logging                = false
  is_multi_region_trail         = false
  include_global_service_events = false
  enable_log_file_validation    = false
}
```

The account's API-activity audit trail is effectively blind: logging is turned
off, it's single-region, global-service events are excluded, and log-file
validation (tamper detection) is disabled. A pipeline that applies this leaves
the account with no reliable record of who did what.

## How an attacker exploits it

With CloudTrail off or partial, an intruder operates without an audit trail —
creating backdoor IAM, exfiltrating data, or pivoting between regions that
aren't logged — and the org can't detect or reconstruct the activity.
Insufficient logging is what turns a contained incident into an undetected one.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Checkov | `CKV_AWS_67` — CloudTrail enabled in all regions (also fires `CKV_AWS_35/36` log-validation) |
| KICS | `CloudTrail Logging Disabled` (`4bb76f17-…`) — also flags multi-region/validation off |
| pipeline-check | — (its Terraform provider needs a plan JSON) |

## Fix

Set `enable_logging = true`, `is_multi_region_trail = true`,
`include_global_service_events = true`, and `enable_log_file_validation = true`;
ship trail logs to a dedicated, access-restricted account and alert on
`StopLogging` / `DeleteTrail`.

## References

- Checkov — Terraform/AWS policies: https://www.checkov.io/5.Policy%20Index/terraform.html
- AWS — CloudTrail best practices: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/best-practices-security.html
