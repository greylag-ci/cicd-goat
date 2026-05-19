# greylag-ci scenarios (GitHub Actions-focused extension to cicd-goat)

The upstream `cider-security-research/cicd-goat` focuses primarily on Jenkins,
GitLab, and CircleCI through full-blown Docker environments. These additional
scenarios target **GitHub Actions** specifically, covering modern attack
patterns that have appeared (or become prominent) since the upstream's last
significant update.

Each scenario lives as a runnable-but-gated workflow under
[`.github/workflows/scenario-NN-*.yml`](../.github/workflows/) so every
GHA-aware static scanner can analyze it, plus a writeup in this directory.
Every job in every scenario workflow is gated with `if: false` — the workflow
triggers (so it appears in run history) but no runner is ever assigned.

## Scenarios

| # | Scenario | CICD-SEC | Attack class |
|---|---|---|---|
| 01 | [pull_request_target with fork checkout](01-prtarget-checkout-head/README.md) | 4, 5 | Forky checkout RCE |
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

## How the comparison workflow uses these

The [`scanner-comparison.yml`](../.github/workflows/scanner-comparison.yml)
workflow runs **zizmor**, **poutine**, **checkov**, **kics**, **trivy**, and
**gitleaks** against the entire tree on every push, uploading each scanner's
SARIF output under a separate Code Scanning category. The per-scenario
"How scanners catch it" tables document the *expected* coverage; the actual
results in the Security tab let you verify (or measure gaps in) each tool.

## OWASP CICD-SEC reference

- [OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
- Upstream cicd-goat: https://github.com/cider-security-research/cicd-goat
