# Scenario 22: GCP Workload Identity Federation with broad attribute condition

**OWASP CICD-SEC mapping:** CICD-SEC-2 (Inadequate IAM),
CICD-SEC-7 (Insecure System Configuration)

**Vulnerable workflow:** [`.github/workflows/scenario-22-gcp-oidc-broad-wif.yml`](../../.github/workflows/scenario-22-gcp-oidc-broad-wif.yml)

**Vulnerable Terraform:** [`workload-identity-pool.tf`](workload-identity-pool.tf)

## The pattern

The GCP analogue of [Scenario 10 (AWS OIDC wildcard sub)](../10-oidc-aws-wildcard-sub/README.md).
GCP Workload Identity Federation lets a GitHub Actions OIDC token map
to a service-account impersonation. The mapping is controlled by an
**attribute condition** CEL expression on the workload identity pool
provider:

```hcl
attribute_condition = "attribute.repository.startsWith('greylag-ci/')"
```

Reads as "anything in the greylag-ci org" — which sounds fine until
you remember that:

- Any org member can create a new repo under `greylag-ci/`.
- Any branch / tag / environment / actor inside any of those repos
  passes the condition.
- Future repos you don't know about yet also pass.

The right condition pins to the exact repo:branch (or repo:environment)
that needs to deploy. Anything wider is an over-grant.

## How an attacker exploits it

Two real attack vectors:

1. **Insider / compromised org member.** Create a new public repo
   under `greylag-ci/`, drop a workflow that uses
   `google-github-actions/auth@v2` with the target provider URL, and
   the workflow can impersonate the production service account.
2. **Lost branch.** A long-dead branch on a long-forgotten repo in the
   org still passes the condition. If anyone can push to that branch
   (loose branch protection, or admin override), they get prod.

## Expected scanner coverage

| Scanner            | Detection                                                            |
| :----------------- | :------------------------------------------------------------------- |
| **pipeline-check** | ⚠️ IAM/WIF rule in roadmap                                          |
| zizmor             | ❌ workflow-only                                                     |
| poutine            | ❌                                                                   |
| KICS               | ⚠️ IaC rule fires on the `.tf` if scanned, not on the workflow      |
| Checkov            | ⚠️ Similar — IaC side only                                          |
| Trivy              | ⚠️ Similar                                                          |
| Gitleaks           | —                                                                    |

> Like Scenario 10, this is a **split-scope** finding: workflow scanners
> see the auth step but not the WIF attribute condition; IaC scanners
> see the WIF but not the workflow. Catching both requires either a
> multi-scanner deployment or a unified scanner that crosses scopes.

## Fix

Pin the attribute condition to the exact `repo:owner/repo:ref:...`:

```hcl
attribute_condition = <<EOT
  assertion.repository == 'greylag-ci/cicd-goat'
  && assertion.environment == 'production'
EOT
```

And on the GitHub side, gate the workflow on a protected environment
that requires reviewers and pins deployment branches to exact names
(see [Scenario 25](../25-environment-branch-pattern-bypass/README.md)
for the trap to avoid there).

## References

- GitHub docs — Configuring OpenID Connect in Google Cloud Platform:
  https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-google-cloud-platform
- GCP — Best practices for using Workload Identity Federation:
  https://cloud.google.com/iam/docs/best-practices-for-using-and-managing-workload-identity-federation
