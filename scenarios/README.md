# Scenarios

Forty-eight deliberately-vulnerable pipelines, each demonstrating one canonical
attack pattern from the modern threat landscape. **Scenarios 01–38 are
GitHub Actions** workflows; scenarios 30–33 are **variants** of scenario 02
that probe each scanner's untrusted-input list across four different
`github.event.*` contexts (issue body, head_ref, commit message, comment
body) — they share scenario 02's `expected:` rules so a scanner that scopes
its rule narrower than its competitors surfaces as drift on the matrix.
Scenarios 34–38 broaden the GHA corpus: a Project-Zero-bug-2070
`ACTIONS_ALLOW_UNSECURE_COMMANDS` revival, a signed-but-not-bound
`cosign verify`, a cross-job environment-secret leak, a confused-deputy
auto-merge (Synacktiv's Dependabot exploit), and a recursive submodule
checkout from a PR.

**Scenarios 39+ are the multi-provider expansion** — the same one-bug,
one-writeup model applied to the *other* CI/CD platforms where most real
pipelines live. Scenario 40 is a Jenkins pilot; **39 + 41–48 are the GitLab CI
set** (script/`include`/`CI_JOB_TOKEN`/OIDC/runner/secret-hygiene patterns).
Only the scanners that actually parse a given provider's files score those
rows; the rest render `—` (not-applicable). See the per-provider leaderboards
in the [README](../README.md) and the sectioned [matrix](../docs/MATRIX.md).

**Safety — two placement rules keep every pattern inert:**

- GitHub Actions scenarios live at
  [`.github/workflows/scenario-NN-*.yml`](../.github/workflows/) and every
  job is gated with `if: false` — the workflow triggers on its documented
  events (so it appears in run history) but no runner is ever assigned.
- Non-GHA provider files (`.gitlab-ci.yml`, `Jenkinsfile`, …) live
  **nested under `scenarios/NN-<slug>/`**, never at a provider's canonical
  auto-run path. GitHub never runs them, and no other platform
  auto-discovers a nested pipeline file, so they're static fixtures a
  scanner can read but nothing will execute (enforced by
  [`tools/check-provider-files-safe.py`](../tools/check-provider-files-safe.py)).

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
| 28 | [Reusable workflow `${{ inputs.* }}` injection](28-reusable-workflow-input-injection/README.md) | 4 | Cross-`workflow_call` taint |
| 29 | [npm lifecycle-script RCE](29-npm-lifecycle-script-rce/README.md) | 3 | `npm install` runs `preinstall` / `postinstall` |
| 30 | [Script injection via issue body](30-script-injection-issue-body/README.md) | 4 | Variant of 02 — `.body` instead of `.title` |
| 31 | [Script injection via `github.head_ref`](31-script-injection-head-ref/README.md) | 4 | Variant of 02 — PR branch name |
| 32 | [Script injection via commit message](32-script-injection-commit-message/README.md) | 4 | Variant of 02 — `head_commit.message` |
| 33 | [Script injection via comment body](33-script-injection-comment-body/README.md) | 4 | Variant of 02 — `comment.body` on `issue_comment` |
| 34 | [`ACTIONS_ALLOW_UNSECURE_COMMANDS` re-enabled](34-actions-allow-unsecure-commands/README.md) | 4 | Project Zero 2070 — `::set-env` / `::add-path` revival |
| 35 | [`cosign verify` without identity binding](35-cosign-verify-no-identity-binding/README.md) | 3, 9 | Signed-but-not-bound — keyless verify without identity pin |
| 36 | [Environment secret read without consumer binding](36-environment-secret-no-binding/README.md) | 5, 2 | Cross-job leak via `needs.<>.outputs.*` |
| 37 | [Confused-deputy auto-merge via bot-identity gate](37-confused-deputy-auto-merge/README.md) | 1 | Synacktiv Dependabot exploit shape |
| 38 | [Recursive submodule checkout from PR](38-submodule-trust-from-pr/README.md) | 3, 4 | `submodules: recursive` trusts attacker `.gitmodules` |
| 39 | [GitLab CI — script injection via `$CI_*`](39-gitlab-ci-script-injection/README.md) | 4 | **GitLab** — untrusted MR/commit var in `script:` |
| 40 | [Jenkins — `sh` string-interpolation injection](40-jenkins-shell-injection/README.md) | 4 | **Jenkins** — untrusted value in double-quoted GString |
| 41 | [GitLab — `CI_JOB_TOKEN` cross-project access](41-gitlab-ci-job-token-cross-project/README.md) | 2, 5 | **GitLab** — job token used across projects |
| 42 | [GitLab — untrusted `include:`](42-gitlab-include-remote-untrusted/README.md) | 3, 9 | **GitLab** — remote / mutable-ref include |
| 43 | [GitLab — secret job on fork MR pipeline](43-gitlab-fork-mr-secrets/README.md) | 1, 6 | **GitLab** — `merge_request_event` + secret |
| 44 | [GitLab — hardcoded secret in `variables:`](44-gitlab-secret-in-variables/README.md) | 6 | **GitLab** — credential in source |
| 45 | [GitLab — `curl \| sh` in `before_script`](45-gitlab-curl-pipe-sh/README.md) | 3, 4 | **GitLab** — TOFU install script |
| 46 | [GitLab — job `image:` mutable tag](46-gitlab-image-latest/README.md) | 3, 9 | **GitLab** — mutable base image |
| 47 | [GitLab — OIDC `id_tokens` over-broad aud/sub](47-gitlab-oidc-broad-aud-sub/README.md) | 2, 7 | **GitLab** — federation misconfig |
| 48 | [GitLab — untagged shared-runner + privileged dind](48-gitlab-shared-runner-privileged/README.md) | 7, 4 | **GitLab** — runner isolation |

## OWASP CICD-SEC top 10 — full coverage

| Risk | Coverage | Scenarios |
|:---|:---|:---|
| CICD-SEC-1: Insufficient Flow Control Mechanisms              | ✅ | 23, 25, 37, 43 |
| CICD-SEC-2: Inadequate Identity and Access Management         | ✅ | 10, 22, 36, 41, 47 |
| CICD-SEC-3: Dependency Chain Abuse                            | ✅ | 3, 9, 11, 12, 16, 19, 20, 29, 35, 38, 42, 45, 46 |
| CICD-SEC-4: Poisoned Pipeline Execution                       | ✅ | 1, 2, 5, 7, 13, 14, 18, 21, 28, 30, 31, 32, 33, 34, 38, 39, 40, 45, 48 |
| CICD-SEC-5: Insufficient Pipeline-Based Access Controls       | ✅ | 1, 4, 6, 25, 26, 36, 41 |
| CICD-SEC-6: Insufficient Credential Hygiene                   | ✅ | 6, 12, 15, 17, 43, 44 |
| CICD-SEC-7: Insecure System Configuration                     | ✅ | 8, 10, 22, 47, 48 |
| CICD-SEC-8: Ungoverned Usage of Third-Party Services          | ✅ | 24 |
| CICD-SEC-9: Improper Artifact Integrity Validation            | ✅ | 5, 7, 9, 17, 19, 35, 42, 46 |
| CICD-SEC-10: Insufficient Logging and Visibility              | ✅ | 27 |

Every risk in the top 10 has at least one scenario. See the
[OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
for the canonical definitions.
