# Scenario 47: GitLab — OIDC `id_tokens` with over-broad audience / subject

**Provider:** GitLab CI/CD

**OWASP CICD-SEC mapping:** CICD-SEC-2 (Inadequate IAM) · CICD-SEC-7 (Insecure System Configuration)

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml) · trust policy: [`trust-policy.json`](trust-policy.json)

## The pattern

The pipeline mints an OIDC token with a generic, shared audience:

```yaml
id_tokens:
  AWS_ID_TOKEN:
    aud: https://gitlab.example.com
```

…and the cloud trust policy it federates into matches the token `sub` far too
loosely:

```json
"gitlab.example.com:sub": "project_path:*:ref_type:branch:ref:*"
```

Any project on any branch in the instance produces a token that satisfies both
conditions. This is the GitLab analogue of the AWS / GCP OIDC scenarios
([10](../10-oidc-aws-wildcard-sub/README.md) / [22](../22-gcp-oidc-broad-wif/README.md)):
the over-broad condition lives in the sibling `trust-policy.json`.

## How an attacker exploits it

A different project — or a fork pipeline — mints an OIDC token that still
matches the shared `aud` and the wildcard `sub`, and assumes the cloud role:
cross-tenant credential abuse. Path-based `sub` claims are also spoofable by
creating a matching namespace path.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-031` — `id_tokens:` missing audience pin or environment binding |
| ciguard | — (no OIDC rule) |
| Checkov | — |

> pipeline-check catches the **workflow-side** half (the unpinned/shared
> audience, no environment binding). The deeper wildcard-`sub` bug lives in the
> trust policy — a solo catch by pipeline-check, mirroring scenarios 10 / 22.

## Fix

Use a **unique `aud:` per service**; bind the deploy job to a GitLab
`environment:`; and tighten the trust policy's `sub` condition to an
exact-match value (no `*` glob) and require `ref_protected`. On gitlab.com you
can additionally bind to the immutable `project_id` / `namespace_id` claims;
on self-managed instances (like the `gitlab.example.com` here) those aren't
available as cloud condition keys, so the exact-match `sub` is the lever.

## References

- GitLab Docs — ID token authentication: https://docs.gitlab.com/ci/secrets/id_token_authentication/
- GitLab Docs — Configure OIDC in AWS: https://docs.gitlab.com/ci/cloud_services/aws/
