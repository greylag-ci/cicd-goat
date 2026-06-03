# Scenario 85: GitLab — fork MR pipeline mints a cloud OIDC token

**Provider:** GitLab CI/CD · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · CICD-SEC-2 (Inadequate IAM) · **Severity: critical**

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

The highest-impact GitLab chain — one job combines two bugs:

```yaml
rules:
  - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'   # runs fork MRs (cf. #43)
id_tokens:
  AWS_ID_TOKEN: { aud: https://gitlab.example.com }       # mints cloud OIDC (cf. #47)
script:
  - make build                                            # fork-controlled code
  - aws sts assume-role-with-web-identity --web-identity-token "$AWS_ID_TOKEN" ...
```

## How an attacker exploits it

With "run fork MRs in the parent project" enabled, a fork author's MR code runs
in the parent context, mints the OIDC token, and assumes the cloud role — a
pull request becomes **cloud-account compromise**. Combines
[scenario 43](../43-gitlab-fork-mr-secrets/README.md) (fork-MR execution) and
[scenario 47](../47-gitlab-oidc-broad-aud-sub/README.md) (over-broad OIDC).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-031` — `id_tokens:` missing audience pin / environment binding (the mintable-token half) |
| ciguard | `PIPE-004` — unprotected deploy job (the ungated fork-deploy half) |
| Checkov | — |

## Fix

Don't run fork MR pipelines in the parent with privileges; gate OIDC-minting /
deploy jobs to protected branches (`$CI_COMMIT_REF_PROTECTED == "true"`) and a
GitLab `environment:`; use a unique, tightly-bound `aud:`/`sub:` per service.

## References

- GitLab — Pipeline security: https://docs.gitlab.com/ci/pipeline_security/
- GitLab — ID token authentication: https://docs.gitlab.com/ci/secrets/id_token_authentication/
