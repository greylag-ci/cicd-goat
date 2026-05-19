# Scenarios

Twenty-seven deliberately-vulnerable GitHub Actions workflows, each
demonstrating one canonical attack pattern from the modern threat
landscape. Every scenario lives as a runnable-but-gated workflow at
[`.github/workflows/scenario-NN-*.yml`](../.github/workflows/) so every
GHA-aware static scanner can analyze it, plus a writeup here.

Every job in every scenario workflow is gated with `if: false` — the
workflow triggers on the documented events (so it appears in run history),
but no runner is ever assigned.

| #  | Scenario | CICD-SEC | Attack class |
|---:|---|---|---|
| 01 | [pull_request_target with fork-head checkout](01-prtarget-checkout-head/README.md) | 4, 5 | Forky checkout RCE |
| 02 | [Script injection via issue title](02-script-injection-issue-title/README.md) | 4 | Expression injection |
| 03 | [Action pinned to mutable ref](03-action-mutable-ref/README.md) | 3 | Supply chain (tag move) |
| 04 | [GITHUB_TOKEN `write-all`](04-github-token-write-all/README.md) | 5 | Excessive permissions |
| 05 | [Cache poisoning via PR title](05-cache-poisoning-pr-controlled/README.md) | 4, 9 | Cross-job cache abuse |
| 06 | [Reusable workflow `secrets: inherit`](06-reusable-secrets-inherit/README.md) | 5, 6 | Privilege passthrough |
| 07 | [workflow_run artifact RCE](07-workflow-run-artifact-rce/README.md) | 4, 9 | Trigger context confusion |
| 08 | [Self-hosted runner on public repo](08-self-hosted-public-fork/README.md) | 7 | Runner persistence |
| 09 | [Container image `:latest`](09-container-image-latest/README.md) | 3, 9 | Mutable base image |
| 10 | [AWS OIDC wildcard subject](10-oidc-aws-wildcard-sub/README.md) | 2, 7 | Federation misconfig |
| 11 | [pip install no hashes](11-pip-install-no-hashes/README.md) | 3 | Dependency hijack |
| 12 | [checkout `persist-credentials` leak](12-persist-credentials-leak/README.md) | 6, 3 | Token in `.git/config` |
| 13 | [workflow_dispatch input injection](13-input-injection-workflow-dispatch/README.md) | 4 | Operator-trigger injection |
| 14 | [`$GITHUB_ENV` poisoning](14-env-injection-pr-body/README.md) | 4 | Env-file injection |
| 15 | [Hardcoded secret in `env:`](15-hardcoded-secret-env/README.md) | 6 | Secret in source |
| 16 | [`curl \| sh` toolcache poisoning](16-curl-pipe-sh/README.md) | 3 | TOFU install script |
| 17 | [`upload-artifact` includes `.git/`](17-artipacked-git-dir/README.md) | 6, 9 | Artifact-packed token |
| 18 | [Composite action `${{ inputs.* }}` injection](18-composite-action-input-injection/README.md) | 4 | Composite expansion |
| 19 | [Codecov-style trusted-installer compromise](19-codecov-style-installer/README.md) | 3, 9 | Signed-but-malicious supply chain |
| 20 | [Dependency confusion (Birsan attack)](20-dependency-confusion/README.md) | 3 | Internal package name hijack |
| 21 | [Matrix expansion injection](21-matrix-expansion-injection/README.md) | 4 | Matrix-mediated taint flow |
| 22 | [GCP OIDC over-broad workload identity](22-gcp-oidc-broad-wif/README.md) | 2, 7 | Federation misconfig |
| 23 | [Branch-protection bypass via `github-actions[bot]`](23-actions-bot-branch-protection-bypass/README.md) | 1 | Bypass allowlist amplifier |
| 24 | [Third-party webhook exfiltration](24-third-party-webhook-exfil/README.md) | 8 | Egress to ungoverned service |
| 25 | [Environment branch-pattern bypass](25-environment-branch-pattern-bypass/README.md) | 1, 5 | Glob-pattern bypass |
| 26 | [GitHub App token over-scope](26-app-token-over-scope/README.md) | 5 | Token minted without `permissions:` |
| 27 | [Secret leak in workflow logs](27-secret-leak-in-logs/README.md) | 10 | `set -x` + URL-embedded + derived values |

## OWASP CICD-SEC top 10 — full coverage

| Risk | Coverage | Scenarios |
|:---|:---|:---|
| CICD-SEC-1: Insufficient Flow Control Mechanisms              | ✅ | 23, 25 |
| CICD-SEC-2: Inadequate Identity and Access Management         | ✅ | 10, 22 |
| CICD-SEC-3: Dependency Chain Abuse                            | ✅ | 3, 9, 11, 12, 16, 19, 20 |
| CICD-SEC-4: Poisoned Pipeline Execution                       | ✅ | 1, 2, 5, 7, 13, 14, 18, 21 |
| CICD-SEC-5: Insufficient Pipeline-Based Access Controls       | ✅ | 1, 4, 6, 25, 26 |
| CICD-SEC-6: Insufficient Credential Hygiene                   | ✅ | 6, 12, 15, 17 |
| CICD-SEC-7: Insecure System Configuration                     | ✅ | 8, 10, 22 |
| CICD-SEC-8: Ungoverned Usage of Third-Party Services          | ✅ | 24 |
| CICD-SEC-9: Improper Artifact Integrity Validation            | ✅ | 5, 7, 9, 16, 17, 19 |
| CICD-SEC-10: Insufficient Logging and Visibility              | ✅ | 27 |

Every risk in the top 10 has at least one scenario. See the
[OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
for the canonical definitions.
