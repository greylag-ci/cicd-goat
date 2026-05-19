# Scenario 10: AWS OIDC trust policy with wildcard subject

**OWASP CICD-SEC mapping:** CICD-SEC-2 (Inadequate Identity and Access Management),
CICD-SEC-7 (Insecure System Configuration)

**Vulnerable workflow:** [`.github/workflows/scenario-10-oidc-aws-wildcard-sub.yml`](../../.github/workflows/scenario-10-oidc-aws-wildcard-sub.yml)

**IAM trust policy:** [`trust-policy.json`](trust-policy.json)

## The pattern

GitHub Actions OIDC lets workflows assume cloud roles without long-lived
credentials. The IAM trust policy on the AWS side decides *which* GitHub
workflows can assume the role, via a `Condition` on the OIDC `sub` claim.

The `sub` claim is structured as `repo:<owner>/<repo>:ref:refs/heads/<branch>`
(or `:environment:<env>`, etc.). Conditions like:

```json
"StringLike": {
  "token.actions.githubusercontent.com:sub": "repo:*"
}
```

match **every** GitHub repository everywhere — any random repo on github.com
can mint a token and assume this role.

Slightly less wrong but still broken:

- `"repo:greylag-ci/*"` — every repo in the org, including future ones,
  including any repo a member can create.
- `"repo:greylag-ci/cicd-goat:*"` — any branch, any environment. A fork PR
  workflow can still assume the role.

## How an attacker exploits it

Open a PR (or create their own repo) whose workflow uses
`aws-actions/configure-aws-credentials` with the target role ARN. The
returned credentials let them act as the production-deploy principal.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | n/a (zizmor doesn't scan IAM JSON) |
| poutine   | partial |
| checkov   | `CKV_AWS_*` family for IAM trust policy wildcards |
| kics      | "IAM role trust policy allows all principals" / wildcard SUB conditions |
| trivy     | partial (covers some IAM trust patterns) |
| gitleaks  | n/a |

The `aws-actions/configure-aws-credentials` step itself is fine; the bug
is in the trust policy. Scanners that look only at workflows will miss
this — IaC scanners (checkov, kics, trivy) on `trust-policy.json` are
where this should land.

## Fix

Anchor the `sub` to the exact `repo:org/repo` and the exact ref or
environment:

```json
"StringEquals": {
  "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
  "token.actions.githubusercontent.com:sub":
    "repo:greylag-ci/cicd-goat:environment:production"
}
```

## References

- GitHub docs — "Configuring OpenID Connect in Amazon Web Services":
  https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
- AWS — "Using OIDC web identity federation":
  https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html
