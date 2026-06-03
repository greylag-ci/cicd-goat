# Scenario 114: CloudFormation — security group SSH open to `0.0.0.0/0`

**Provider:** CloudFormation · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: high**

**Vulnerable file:** [`template.yaml`](template.yaml)

## The pattern

```yaml
SecurityGroupIngress:
  - { IpProtocol: tcp, FromPort: 22, ToPort: 22, CidrIp: 0.0.0.0/0 }
```

A security group exposes SSH to the entire internet. A pipeline that deploys
this stack puts the instance's SSH directly on the public internet — the
CloudFormation twin of the Terraform SG scenario (101).

## How an attacker exploits it

The host is immediately subject to internet-wide SSH brute-force and 0-day
exposure; one weak/leaked key or vuln is a shell on the instance.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Trivy | `AWS-0107` — security group ingress from public internet |
| Checkov | `CKV_AWS_24` — no SG ingress from 0.0.0.0/0 to port 22 |
| KICS | `Security Group With Unrestricted Access To SSH` (`6e856af2-…`) |
| pipeline-check | — (CloudFormation ruleset thin / non-attributable) |

## Fix

Restrict `CidrIp` to known admin CIDRs / a bastion / VPN; prefer SSM Session
Manager over open SSH; never `0.0.0.0/0` on 22 (or 3389/databases).

## References

- AWS — security group best practices: https://docs.aws.amazon.com/vpc/latest/userguide/vpc-security-groups.html
