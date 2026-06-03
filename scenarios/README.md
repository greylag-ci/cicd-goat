# Scenarios

Eighty-two deliberately-vulnerable pipelines, each demonstrating one canonical
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
pipelines live: **GitLab CI** (39, 41–48), **Jenkins** (40, 67–70),
**Azure Pipelines** (49–54), **CircleCI** (55–60), **Bitbucket Pipelines**
(61–66), **Tekton** (71–73), **Argo Workflows** (74–76), **Drone CI** (77–78),
**Buildkite** (79–80), and **Google Cloud Build** (81–82). Only the scanners
that actually parse a given provider's files score those rows; the rest render
`—` (not-applicable), and several rows are all-miss **next-gen targets** —
canonical bugs (Azure/CircleCI injection, persist-credentials, the Mandiant
secret-to-artifact leak, `skip-ssl-verify`, Jenkins `input`-without-submitter)
that no scanner here catches yet. See the per-provider leaderboards in the
[README](../README.md) and the sectioned [matrix](../docs/MATRIX.md).

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
| 49 | [Azure — macro `$(...)` injection into Bash@3](49-azure-macro-injection/README.md) | 4 | **Azure** — runtime macro injection |
| 50 | [Azure — `${{ parameters }}` template injection](50-azure-template-parameter-injection/README.md) | 4 | **Azure** — compile-time template injection |
| 51 | [Azure — `checkout persistCredentials: true`](51-azure-persist-credentials/README.md) | 6 | **Azure** — token in `.git/config` |
| 52 | [Azure — `addSpnToEnvironment` SP exposure](52-azure-spn-to-environment/README.md) | 2, 6 | **Azure** — SP secret to env |
| 53 | [Azure — `resources` untrusted/mutable ref](53-azure-resources-untrusted-repo/README.md) | 3, 9 | **Azure** — external repo on mutable ref |
| 54 | [Azure — self-hosted pool for untrusted builds](54-azure-self-hosted-untrusted/README.md) | 7 | **Azure** — runner persistence |
| 55 | [CircleCI — orb pinned to `@volatile`](55-circleci-orb-volatile/README.md) | 3 | **CircleCI** — supply chain (orb version) |
| 56 | [CircleCI — `run:` injection via `<< pipeline.* >>`](56-circleci-run-injection/README.md) | 4 | **CircleCI** — pipeline-value injection |
| 57 | [CircleCI — `machine: true` privileged executor](57-circleci-machine-privileged/README.md) | 7 | **CircleCI** — privileged executor |
| 58 | [CircleCI — docker image mutable tag](58-circleci-image-mutable-tag/README.md) | 3, 9 | **CircleCI** — mutable base image |
| 59 | [CircleCI — hardcoded secret in `environment:`](59-circleci-secret-in-environment/README.md) | 6 | **CircleCI** — secret in source |
| 60 | [CircleCI — uncertified third-party orb](60-circleci-uncertified-orb/README.md) | 3 | **CircleCI** — supply chain (publisher) |
| 61 | [Bitbucket — secret dumped to `artifacts:`](61-bitbucket-secret-to-artifact/README.md) | 6, 10 | **Bitbucket** — Mandiant masking bypass |
| 62 | [Bitbucket — `$BITBUCKET_*` script injection](62-bitbucket-var-injection/README.md) | 4 | **Bitbucket** — SCM-metadata injection |
| 63 | [Bitbucket — `pipe:` mutable tag](63-bitbucket-pipe-mutable-tag/README.md) | 3 | **Bitbucket** — supply chain (pipe) |
| 64 | [Bitbucket — `image:` mutable tag](64-bitbucket-image-mutable-tag/README.md) | 3, 9 | **Bitbucket** — mutable base image |
| 65 | [Bitbucket — `clone: skip-ssl-verify: true`](65-bitbucket-clone-skip-ssl-verify/README.md) | 7 | **Bitbucket** — TLS verification off |
| 66 | [Bitbucket — custom-pipeline variable injection](66-bitbucket-custom-pipeline-injection/README.md) | 4, 1 | **Bitbucket** — user-input injection |
| 67 | [Jenkins — `@Grab` sandbox bypass (CVE-2019-1003000)](67-jenkins-grab-sandbox-bypass/README.md) | 4 | **Jenkins** — compile-time sandbox escape |
| 68 | [Jenkins — `input` without `submitter`](68-jenkins-input-no-submitter/README.md) | 1, 5 | **Jenkins** — approval-gate bypass |
| 69 | [Jenkins — shared library on mutable `@master`](69-jenkins-library-mutable-ref/README.md) | 3 | **Jenkins** — mutable library ref |
| 70 | [Jenkins — `agent any` controller exposure](70-jenkins-agent-any/README.md) | 7, 5 | **Jenkins** — runner isolation |
| 71 | [Tekton — `$(params.*)` step-script injection](71-tekton-param-injection/README.md) | 4 | **Tekton** — param injection |
| 72 | [Tekton — privileged / root step](72-tekton-privileged-step/README.md) | 7 | **Tekton** — privileged step |
| 73 | [Tekton — step image not pinned](73-tekton-image-unpinned/README.md) | 3, 9 | **Tekton** — mutable image |
| 74 | [Argo — `{{inputs.parameters}}` injection](74-argo-param-injection/README.md) | 4 | **Argo** — param injection |
| 75 | [Argo — privileged / root container](75-argo-privileged-container/README.md) | 7 | **Argo** — privileged container |
| 76 | [Argo — default ServiceAccount + automount](76-argo-default-serviceaccount/README.md) | 2 | **Argo** — over-broad SA |
| 77 | [Drone — `privileged: true` step](77-drone-privileged-step/README.md) | 7 | **Drone** — privileged step |
| 78 | [Drone — step image mutable tag](78-drone-image-unpinned/README.md) | 3, 9 | **Drone** — mutable image |
| 79 | [Buildkite — `$BUILDKITE_*` command injection](79-buildkite-var-injection/README.md) | 4 | **Buildkite** — var injection |
| 80 | [Buildkite — plugin on a mutable ref](80-buildkite-plugin-unpinned/README.md) | 3 | **Buildkite** — supply chain (plugin) |
| 81 | [Cloud Build — step image not pinned](81-cloudbuild-image-unpinned/README.md) | 3, 9 | **Cloud Build** — mutable image |
| 82 | [Cloud Build — default service account](82-cloudbuild-default-serviceaccount/README.md) | 2 | **Cloud Build** — over-broad SA |

## OWASP CICD-SEC top 10 — full coverage

| Risk | Coverage | Scenarios |
|:---|:---|:---|
| CICD-SEC-1: Insufficient Flow Control Mechanisms              | ✅ | 23, 25, 37, 43, 66, 68 |
| CICD-SEC-2: Inadequate Identity and Access Management         | ✅ | 10, 22, 36, 41, 47, 52, 76, 82 |
| CICD-SEC-3: Dependency Chain Abuse                            | ✅ | 3, 9, 11, 12, 16, 19, 20, 29, 35, 38, 42, 45, 46, 53, 55, 58, 60, 63, 64, 69, 73, 78, 80, 81 |
| CICD-SEC-4: Poisoned Pipeline Execution                       | ✅ | 1, 2, 5, 7, 13, 14, 18, 21, 28, 30, 31, 32, 33, 34, 38, 39, 40, 45, 48, 49, 50, 56, 62, 66, 67, 71, 74, 79 |
| CICD-SEC-5: Insufficient Pipeline-Based Access Controls       | ✅ | 1, 4, 6, 25, 26, 36, 41, 68, 70 |
| CICD-SEC-6: Insufficient Credential Hygiene                   | ✅ | 6, 12, 15, 17, 43, 44, 51, 52, 59, 61 |
| CICD-SEC-7: Insecure System Configuration                     | ✅ | 8, 10, 22, 47, 48, 54, 57, 65, 70, 72, 75, 77 |
| CICD-SEC-8: Ungoverned Usage of Third-Party Services          | ✅ | 24 |
| CICD-SEC-9: Improper Artifact Integrity Validation            | ✅ | 5, 7, 9, 17, 19, 35, 42, 46, 53, 58, 64, 73, 78, 81 |
| CICD-SEC-10: Insufficient Logging and Visibility              | ✅ | 27, 61 |

Every risk in the top 10 has at least one scenario. See the
[OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
for the canonical definitions.
