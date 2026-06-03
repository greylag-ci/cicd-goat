# The full matrix

Per-scenario verdicts for every scanner in the comparison. Auto-generated
from the latest successful
[`scanner-comparison`](../../../actions/workflows/scanner-comparison.yml)
run on `main` by [`tools/regen-readme.py`](../tools/regen-readme.py),
driven by [`tools/scenarios.yaml`](../tools/scenarios.yaml).

Rebuild locally: see [CONTRIBUTING.md → Regenerate the stats](../CONTRIBUTING.md#regenerate-the-stats).

| key | meaning                                                  |
| :-: | :------------------------------------------------------- |
| ✅  | scanner flags the **canonical bug** with a matching rule |
| ⚠️  | scanner partially catches — adjacent rule, half the antipattern, or related but distinct concern |
| ❌  | scanner misses the canonical bug                         |
| —   | not applicable to that scanner's class                   |

<!-- AUTOGEN:matrix -->
### GitHub Actions

| #  | Scenario | pipeline&#x2011;check | zizmor | poutine | KICS | Checkov | actionlint | octoscan |
| :-:| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 01 | `pull_request_target` + fork-head checkout | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| 02 | Script injection via issue title | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 03 | Action pinned to mutable ref | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 04 | `GITHUB_TOKEN` `write-all` | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| 05 | Cache poisoning via PR title | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 06 | Reusable workflow `secrets: inherit` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 07 | `workflow_run` artifact RCE | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 08 | Self-hosted runner on public repo | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| 09 | Container image `:latest` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 10 | AWS OIDC wildcard `sub` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 11 | `pip install` no hashes | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 12 | `persist-credentials` leak | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 13 | `workflow_dispatch` input injection | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| 14 | `$GITHUB_ENV` poisoning | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| 15 | Hardcoded secret in `env:` | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| 16 | `curl \| sh` install | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 17 | ArtiPACKED — `.git/` in artifact | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| 18 | Composite action `${{ inputs.* }}` injection | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| 19 | Codecov-style trusted-installer | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 20 | Dependency confusion (Birsan) | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 21 | Matrix expansion injection | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| 22 | GCP OIDC over-broad WIF | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| 23 | `github-actions[bot]` branch-protection bypass | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 24 | Third-party webhook exfiltration | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 25 | Environment branch-pattern bypass | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 26 | GitHub App token over-scope | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 27 | Secret leak in workflow logs | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 28 | Reusable workflow `${{ inputs.* }}` injection | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 29 | npm lifecycle-script RCE | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 30 | Script injection via issue body | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 31 | Script injection via `github.head_ref` | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| 32 | Script injection via commit message | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| 33 | Script injection via comment body | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 34 | `ACTIONS_ALLOW_UNSECURE_COMMANDS` re-enabled | ❌ | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ |
| 35 | `cosign verify` without identity binding | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 36 | Environment secret read without consumer binding | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 37 | Confused-deputy auto-merge via bot-identity gate | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 38 | Recursive submodule checkout from PR | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 89 | GHA: `terraform apply` on untrusted PR (IaC RCE) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 105 | GHA: Codecov-style remote uploader piped to shell | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 107 | GHA: org secret handed to unpinned 3rd-party action | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ |
| 108 | GHA: deploy job missing environment binding | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 109 | GHA: self-hosted deploy without environment gate | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
|    | **canonical bugs caught** | **37 ✅** | **17 ✅** | **14 ✅** | **8 ✅** | **10 ✅** | **6 ✅** | **13 ✅** |

### GitLab CI

| #  | Scenario | pipeline&#x2011;check | Checkov | ciguard |
| :-:| :--- | :-: | :-: | :-: |
| 39 | GitLab CI: script injection via `$CI_*` / MR vars | ✅ | ❌ | ❌ |
| 41 | GitLab: `CI_JOB_TOKEN` cross-project access | ❌ | ❌ | ✅ |
| 42 | GitLab: untrusted `include:` (remote / mutable ref) | ✅ | ❌ | ✅ |
| 43 | GitLab: secret job on fork merge-request pipeline | ✅ | ❌ | ✅ |
| 44 | GitLab: hardcoded secret in `variables:` | ✅ | ❌ | ✅ |
| 45 | GitLab: `curl \| sh` in `before_script` | ✅ | ❌ | ✅ |
| 46 | GitLab: job `image:` mutable tag | ✅ | ❌ | ✅ |
| 47 | GitLab: OIDC `id_tokens` over-broad aud/sub | ✅ | ❌ | ❌ |
| 48 | GitLab: untagged shared-runner + privileged dind | ❌ | ❌ | ✅ |
| 85 | GitLab: fork MR pipeline mints cloud OIDC token | ✅ | ❌ | ✅ |
| 91 | GitLab: `terraform apply` in a merge-request pipeline | ✅ | ❌ | ❌ |
| 106 | GitLab: `include: remote:` unpinned 3rd-party template | ✅ | ❌ | ✅ |
| 110 | GitLab: manual deploy defaults to allow_failure | ✅ | ❌ | ✅ |
| 113 | GitLab: `CI_DEBUG_TRACE` leaks secrets to job log | ❌ | ❌ | ❌ |
|    | **canonical bugs caught** | **11 ✅** | **0 ✅** | **10 ✅** |

### Azure Pipelines

| #  | Scenario | pipeline&#x2011;check | Checkov |
| :-:| :--- | :-: | :-: |
| 49 | Azure: macro `$(...)` injection into Bash@3 | ❌ | ❌ |
| 50 | Azure: `${{ parameters }}` template injection | ❌ | ❌ |
| 51 | Azure: `checkout persistCredentials: true` | ❌ | ❌ |
| 52 | Azure: `addSpnToEnvironment` SP-secret exposure | ✅ | ❌ |
| 53 | Azure: `resources: repositories` untrusted ref | ✅ | ❌ |
| 54 | Azure: self-hosted pool for untrusted builds | ✅ | ❌ |
| 90 | Azure: untrusted `resources` template on self-hosted agent | ✅ | ❌ |
|    | **canonical bugs caught** | **4 ✅** | **0 ✅** |

### CircleCI

| #  | Scenario | pipeline&#x2011;check | Checkov |
| :-:| :--- | :-: | :-: |
| 55 | CircleCI: orb pinned to `@volatile` | ✅ | ❌ |
| 56 | CircleCI: `run:` injection via `<< pipeline.* >>` | ❌ | ❌ |
| 57 | CircleCI: `machine: true` privileged executor | ✅ | ❌ |
| 58 | CircleCI: docker image mutable tag | ✅ | ✅ |
| 59 | CircleCI: hardcoded secret in `environment:` | ✅ | ❌ |
| 60 | CircleCI: uncertified third-party orb | ❌ | ❌ |
| 87 | CircleCI: secrets passed to forked PRs | ✅ | ❌ |
|    | **canonical bugs caught** | **5 ✅** | **1 ✅** |

### Bitbucket Pipelines

| #  | Scenario | pipeline&#x2011;check | Checkov |
| :-:| :--- | :-: | :-: |
| 61 | Bitbucket: secret dumped to `artifacts:` (Mandiant) | ❌ | ❌ |
| 62 | Bitbucket: `$BITBUCKET_*` script injection | ✅ | ❌ |
| 63 | Bitbucket: `pipe:` mutable tag | ✅ | ❌ |
| 64 | Bitbucket: `image:` mutable tag | ❌ | ✅ |
| 65 | Bitbucket: `clone: skip-ssl-verify: true` | ❌ | ❌ |
| 66 | Bitbucket: custom-pipeline variable injection | ❌ | ❌ |
| 88 | Bitbucket: fork PR pipeline exposes secrets | ✅ | ❌ |
|    | **canonical bugs caught** | **3 ✅** | **1 ✅** |

### Jenkins

| #  | Scenario | pipeline&#x2011;check | ciguard |
| :-:| :--- | :-: | :-: |
| 40 | Jenkins: `sh` string-interpolation injection | ✅ | ❌ |
| 67 | Jenkins: `@Grab` sandbox-bypass (CVE-2019-1003000) | ✅ | ❌ |
| 68 | Jenkins: `input` step without `submitter` | ❌ | ❌ |
| 69 | Jenkins: shared library on a mutable `@master` ref | ✅ | ❌ |
| 70 | Jenkins: `agent any` (controller exposure) | ✅ | ✅ |
| 86 | Jenkins: builds untrusted fork PRs with creds (PPE) | ❌ | ❌ |
|    | **canonical bugs caught** | **4 ✅** | **1 ✅** |

### Tekton

| #  | Scenario | pipeline&#x2011;check |
| :-:| :--- | :-: |
| 71 | Tekton: `$(params.*)` injected into step script | ❌ |
| 72 | Tekton: privileged / root step | ✅ |
| 73 | Tekton: step `image:` not pinned to a digest | ✅ |
| 83 | Tekton: privileged step + hostPath node escape | ✅ |
|    | **canonical bugs caught** | **3 ✅** |

### Argo Workflows

| #  | Scenario | pipeline&#x2011;check | Checkov |
| :-:| :--- | :-: | :-: |
| 74 | Argo: `{{inputs.parameters}}` injected into args | ✅ | ❌ |
| 75 | Argo: privileged / root container | ✅ | ✅ |
| 76 | Argo: default ServiceAccount + token automount | ✅ | ✅ |
| 84 | Argo: hostPath mount → node filesystem escape | ✅ | ❌ |
| 92 | Argo: cluster-admin ServiceAccount → cluster takeover | ❌ | ❌ |
|    | **canonical bugs caught** | **4 ✅** | **2 ✅** |

### Drone CI

| #  | Scenario | pipeline&#x2011;check |
| :-:| :--- | :-: |
| 77 | Drone: `privileged: true` step | ✅ |
| 78 | Drone: step `image:` mutable tag | ✅ |
| 93 | Drone: privileged step mounts host Docker socket | ✅ |
|    | **canonical bugs caught** | **3 ✅** |

### Buildkite

| #  | Scenario | pipeline&#x2011;check |
| :-:| :--- | :-: |
| 79 | Buildkite: `$BUILDKITE_*` command injection | ✅ |
| 80 | Buildkite: plugin pinned to a mutable ref | ✅ |
|    | **canonical bugs caught** | **2 ✅** |

### Cloud Build

| #  | Scenario | pipeline&#x2011;check |
| :-:| :--- | :-: |
| 81 | Cloud Build: step image not pinned by digest | ✅ |
| 82 | Cloud Build: runs as default service account | ✅ |
|    | **canonical bugs caught** | **2 ✅** |

### Dockerfile

| #  | Scenario | pipeline&#x2011;check | KICS | Checkov |
| :-:| :--- | :-: | :-: | :-: |
| 94 | Dockerfile: container runs as root (no USER) | ✅ | ✅ | ✅ |
| 95 | Dockerfile: base image unpinned (`:latest`) | ✅ | ✅ | ✅ |
| 96 | Dockerfile: hardcoded secret in `ENV` | ✅ | ❌ | ❌ |
|    | **canonical bugs caught** | **3 ✅** | **2 ✅** | **2 ✅** |

### Kubernetes

| #  | Scenario | pipeline&#x2011;check | KICS | Checkov |
| :-:| :--- | :-: | :-: | :-: |
| 97 | Kubernetes: privileged container | ✅ | ❌ | ✅ |
| 98 | Kubernetes: hostPath mount of node root | ✅ | ✅ | ❌ |
| 99 | Kubernetes: root + allowPrivilegeEscalation | ✅ | ✅ | ✅ |
|    | **canonical bugs caught** | **3 ✅** | **2 ✅** | **2 ✅** |

### Terraform

| #  | Scenario | KICS | Checkov |
| :-:| :--- | :-: | :-: |
| 100 | Terraform: IAM policy `*:*` (full admin) | ✅ | ✅ |
| 101 | Terraform: security group SSH open to 0.0.0.0/0 | ✅ | ✅ |
| 102 | Terraform: S3 bucket public-access-block disabled | ✅ | ✅ |
| 111 | Terraform: CloudTrail logging disabled / single-region | ✅ | ✅ |
| 112 | Terraform: VPC flow logs + S3 access logging off | ✅ | ✅ |
|    | **canonical bugs caught** | **5 ✅** | **5 ✅** |

### CloudFormation

| #  | Scenario | KICS | Checkov |
| :-:| :--- | :-: | :-: |
| 103 | CloudFormation: S3 bucket public read+write | ✅ | ✅ |
|    | **canonical bugs caught** | **1 ✅** | **1 ✅** |

### Helm

| #  | Scenario | pipeline&#x2011;check | Checkov |
| :-:| :--- | :-: | :-: |
| 104 | Helm: privileged container in chart template | ✅ | ✅ |
|    | **canonical bugs caught** | **1 ✅** | **1 ✅** |
<!-- /AUTOGEN:matrix -->

> [!IMPORTANT]
> The hard cases — multi-file scope (10, 22), network-egress reasoning
> (16, 19, 24), sibling-manifest analysis (11, 20, 29), and
> GitHub-settings-level configuration that doesn't appear in any file
> (23, 25, 27) — collapse to *solo catches by one scanner* on the
> current matrix. See [COVERAGE-AXES § ③](COVERAGE-AXES.md#-solo-catches)
> for the live solo-catches list, autogen'd from the same SARIF as the
> matrix above. Their primary value here is as a target for the *next*
> generation of rules across the field.

---

## Scenarios index

<!-- AUTOGEN:scenarios-index -->
| #  | Title | Provider | CICD-SEC | Severity |
| :-:| :--- | :-- | :-: | :-- |
| 01 | [`pull_request_target` + fork-head checkout](../scenarios/01-prtarget-checkout-head/README.md) | GitHub Actions | 4 · 5 | 🔴 critical |
| 02 | [Script injection via issue title](../scenarios/02-script-injection-issue-title/README.md) | GitHub Actions | 4 | 🟠 high |
| 03 | [Action pinned to mutable ref](../scenarios/03-action-mutable-ref/README.md) | GitHub Actions | 3 | 🟠 high |
| 04 | [`GITHUB_TOKEN` `write-all`](../scenarios/04-github-token-write-all/README.md) | GitHub Actions | 5 | 🟡 medium |
| 05 | [Cache poisoning via PR title](../scenarios/05-cache-poisoning-pr-controlled/README.md) | GitHub Actions | 4 · 9 | 🟠 high |
| 06 | [Reusable workflow `secrets: inherit`](../scenarios/06-reusable-secrets-inherit/README.md) | GitHub Actions | 5 · 6 | 🟡 medium |
| 07 | [`workflow_run` artifact RCE](../scenarios/07-workflow-run-artifact-rce/README.md) | GitHub Actions | 4 · 9 | 🔴 critical |
| 08 | [Self-hosted runner on public repo](../scenarios/08-self-hosted-public-fork/README.md) | GitHub Actions | 7 | 🔴 critical |
| 09 | [Container image `:latest`](../scenarios/09-container-image-latest/README.md) | GitHub Actions | 3 · 9 | 🟡 medium |
| 10 | [AWS OIDC wildcard `sub`](../scenarios/10-oidc-aws-wildcard-sub/README.md) | GitHub Actions | 2 · 7 | 🔴 critical |
| 11 | [`pip install` no hashes](../scenarios/11-pip-install-no-hashes/README.md) | GitHub Actions | 3 | 🟡 medium |
| 12 | [`persist-credentials` leak](../scenarios/12-persist-credentials-leak/README.md) | GitHub Actions | 6 · 3 | 🟠 high |
| 13 | [`workflow_dispatch` input injection](../scenarios/13-input-injection-workflow-dispatch/README.md) | GitHub Actions | 4 | 🟠 high |
| 14 | [`$GITHUB_ENV` poisoning](../scenarios/14-env-injection-pr-body/README.md) | GitHub Actions | 4 | 🟠 high |
| 15 | [Hardcoded secret in `env:`](../scenarios/15-hardcoded-secret-env/README.md) | GitHub Actions | 6 | 🟠 high |
| 16 | [`curl \| sh` install](../scenarios/16-curl-pipe-sh/README.md) | GitHub Actions | 3 | 🟡 medium |
| 17 | [ArtiPACKED — `.git/` in artifact](../scenarios/17-artipacked-git-dir/README.md) | GitHub Actions | 6 · 9 | 🔴 critical |
| 18 | [Composite action `${{ inputs.* }}` injection](../scenarios/18-composite-action-input-injection/README.md) | GitHub Actions | 4 | 🟠 high |
| 19 | [Codecov-style trusted-installer](../scenarios/19-codecov-style-installer/README.md) | GitHub Actions | 3 · 9 | 🔴 critical |
| 20 | [Dependency confusion (Birsan)](../scenarios/20-dependency-confusion/README.md) | GitHub Actions | 3 | 🔴 critical |
| 21 | [Matrix expansion injection](../scenarios/21-matrix-expansion-injection/README.md) | GitHub Actions | 4 | 🟠 high |
| 22 | [GCP OIDC over-broad WIF](../scenarios/22-gcp-oidc-broad-wif/README.md) | GitHub Actions | 2 · 7 | 🔴 critical |
| 23 | [`github-actions[bot]` branch-protection bypass](../scenarios/23-actions-bot-branch-protection-bypass/README.md) | GitHub Actions | 1 | 🟠 high |
| 24 | [Third-party webhook exfiltration](../scenarios/24-third-party-webhook-exfil/README.md) | GitHub Actions | 8 | 🟠 high |
| 25 | [Environment branch-pattern bypass](../scenarios/25-environment-branch-pattern-bypass/README.md) | GitHub Actions | 1 · 5 | 🟠 high |
| 26 | [GitHub App token over-scope](../scenarios/26-app-token-over-scope/README.md) | GitHub Actions | 5 | 🟡 medium |
| 27 | [Secret leak in workflow logs](../scenarios/27-secret-leak-in-logs/README.md) | GitHub Actions | 10 | 🟠 high |
| 28 | [Reusable workflow `${{ inputs.* }}` injection](../scenarios/28-reusable-workflow-input-injection/README.md) | GitHub Actions | 4 | 🟠 high |
| 29 | [npm lifecycle-script RCE](../scenarios/29-npm-lifecycle-script-rce/README.md) | GitHub Actions | 3 | 🔴 critical |
| 30 | [Script injection via issue body](../scenarios/30-script-injection-issue-body/README.md) | GitHub Actions | 4 | 🟠 high |
| 31 | [Script injection via `github.head_ref`](../scenarios/31-script-injection-head-ref/README.md) | GitHub Actions | 4 | 🟠 high |
| 32 | [Script injection via commit message](../scenarios/32-script-injection-commit-message/README.md) | GitHub Actions | 4 | 🟠 high |
| 33 | [Script injection via comment body](../scenarios/33-script-injection-comment-body/README.md) | GitHub Actions | 4 | 🟠 high |
| 34 | [`ACTIONS_ALLOW_UNSECURE_COMMANDS` re-enabled](../scenarios/34-actions-allow-unsecure-commands/README.md) | GitHub Actions | 4 | 🟠 high |
| 35 | [`cosign verify` without identity binding](../scenarios/35-cosign-verify-no-identity-binding/README.md) | GitHub Actions | 3 · 9 | 🟠 high |
| 36 | [Environment secret read without consumer binding](../scenarios/36-environment-secret-no-binding/README.md) | GitHub Actions | 5 · 2 | 🟠 high |
| 37 | [Confused-deputy auto-merge via bot-identity gate](../scenarios/37-confused-deputy-auto-merge/README.md) | GitHub Actions | 1 | 🟠 high |
| 38 | [Recursive submodule checkout from PR](../scenarios/38-submodule-trust-from-pr/README.md) | GitHub Actions | 3 · 4 | 🟠 high |
| 39 | [GitLab CI: script injection via `$CI_*` / MR vars](../scenarios/39-gitlab-ci-script-injection/README.md) | GitLab CI | 4 | 🟠 high |
| 40 | [Jenkins: `sh` string-interpolation injection](../scenarios/40-jenkins-shell-injection/README.md) | Jenkins | 4 | 🟠 high |
| 41 | [GitLab: `CI_JOB_TOKEN` cross-project access](../scenarios/41-gitlab-ci-job-token-cross-project/README.md) | GitLab CI | 2 · 5 | 🟠 high |
| 42 | [GitLab: untrusted `include:` (remote / mutable ref)](../scenarios/42-gitlab-include-remote-untrusted/README.md) | GitLab CI | 3 · 9 | 🟠 high |
| 43 | [GitLab: secret job on fork merge-request pipeline](../scenarios/43-gitlab-fork-mr-secrets/README.md) | GitLab CI | 1 · 6 | 🟠 high |
| 44 | [GitLab: hardcoded secret in `variables:`](../scenarios/44-gitlab-secret-in-variables/README.md) | GitLab CI | 6 | 🟠 high |
| 45 | [GitLab: `curl \| sh` in `before_script`](../scenarios/45-gitlab-curl-pipe-sh/README.md) | GitLab CI | 3 · 4 | 🟡 medium |
| 46 | [GitLab: job `image:` mutable tag](../scenarios/46-gitlab-image-latest/README.md) | GitLab CI | 3 · 9 | 🟡 medium |
| 47 | [GitLab: OIDC `id_tokens` over-broad aud/sub](../scenarios/47-gitlab-oidc-broad-aud-sub/README.md) | GitLab CI | 2 · 7 | 🔴 critical |
| 48 | [GitLab: untagged shared-runner + privileged dind](../scenarios/48-gitlab-shared-runner-privileged/README.md) | GitLab CI | 7 · 4 | 🟠 high |
| 49 | [Azure: macro `$(...)` injection into Bash@3](../scenarios/49-azure-macro-injection/README.md) | Azure Pipelines | 4 | 🟠 high |
| 50 | [Azure: `${{ parameters }}` template injection](../scenarios/50-azure-template-parameter-injection/README.md) | Azure Pipelines | 4 | 🟠 high |
| 51 | [Azure: `checkout persistCredentials: true`](../scenarios/51-azure-persist-credentials/README.md) | Azure Pipelines | 6 | 🟠 high |
| 52 | [Azure: `addSpnToEnvironment` SP-secret exposure](../scenarios/52-azure-spn-to-environment/README.md) | Azure Pipelines | 2 · 6 | 🟠 high |
| 53 | [Azure: `resources: repositories` untrusted ref](../scenarios/53-azure-resources-untrusted-repo/README.md) | Azure Pipelines | 3 · 9 | 🟠 high |
| 54 | [Azure: self-hosted pool for untrusted builds](../scenarios/54-azure-self-hosted-untrusted/README.md) | Azure Pipelines | 7 | 🔴 critical |
| 55 | [CircleCI: orb pinned to `@volatile`](../scenarios/55-circleci-orb-volatile/README.md) | CircleCI | 3 | 🟠 high |
| 56 | [CircleCI: `run:` injection via `<< pipeline.* >>`](../scenarios/56-circleci-run-injection/README.md) | CircleCI | 4 | 🟠 high |
| 57 | [CircleCI: `machine: true` privileged executor](../scenarios/57-circleci-machine-privileged/README.md) | CircleCI | 7 | 🟡 medium |
| 58 | [CircleCI: docker image mutable tag](../scenarios/58-circleci-image-mutable-tag/README.md) | CircleCI | 3 · 9 | 🟡 medium |
| 59 | [CircleCI: hardcoded secret in `environment:`](../scenarios/59-circleci-secret-in-environment/README.md) | CircleCI | 6 | 🟠 high |
| 60 | [CircleCI: uncertified third-party orb](../scenarios/60-circleci-uncertified-orb/README.md) | CircleCI | 3 | 🟡 medium |
| 61 | [Bitbucket: secret dumped to `artifacts:` (Mandiant)](../scenarios/61-bitbucket-secret-to-artifact/README.md) | Bitbucket Pipelines | 6 · 10 | 🟠 high |
| 62 | [Bitbucket: `$BITBUCKET_*` script injection](../scenarios/62-bitbucket-var-injection/README.md) | Bitbucket Pipelines | 4 | 🟠 high |
| 63 | [Bitbucket: `pipe:` mutable tag](../scenarios/63-bitbucket-pipe-mutable-tag/README.md) | Bitbucket Pipelines | 3 | 🟡 medium |
| 64 | [Bitbucket: `image:` mutable tag](../scenarios/64-bitbucket-image-mutable-tag/README.md) | Bitbucket Pipelines | 3 · 9 | 🟡 medium |
| 65 | [Bitbucket: `clone: skip-ssl-verify: true`](../scenarios/65-bitbucket-clone-skip-ssl-verify/README.md) | Bitbucket Pipelines | 7 | 🟡 medium |
| 66 | [Bitbucket: custom-pipeline variable injection](../scenarios/66-bitbucket-custom-pipeline-injection/README.md) | Bitbucket Pipelines | 4 · 1 | 🟠 high |
| 67 | [Jenkins: `@Grab` sandbox-bypass (CVE-2019-1003000)](../scenarios/67-jenkins-grab-sandbox-bypass/README.md) | Jenkins | 4 | 🔴 critical |
| 68 | [Jenkins: `input` step without `submitter`](../scenarios/68-jenkins-input-no-submitter/README.md) | Jenkins | 1 · 5 | 🟠 high |
| 69 | [Jenkins: shared library on a mutable `@master` ref](../scenarios/69-jenkins-library-mutable-ref/README.md) | Jenkins | 3 | 🟠 high |
| 70 | [Jenkins: `agent any` (controller exposure)](../scenarios/70-jenkins-agent-any/README.md) | Jenkins | 7 · 5 | 🟠 high |
| 71 | [Tekton: `$(params.*)` injected into step script](../scenarios/71-tekton-param-injection/README.md) | Tekton | 4 | 🟠 high |
| 72 | [Tekton: privileged / root step](../scenarios/72-tekton-privileged-step/README.md) | Tekton | 7 | 🟠 high |
| 73 | [Tekton: step `image:` not pinned to a digest](../scenarios/73-tekton-image-unpinned/README.md) | Tekton | 3 · 9 | 🟡 medium |
| 74 | [Argo: `{{inputs.parameters}}` injected into args](../scenarios/74-argo-param-injection/README.md) | Argo Workflows | 4 | 🟠 high |
| 75 | [Argo: privileged / root container](../scenarios/75-argo-privileged-container/README.md) | Argo Workflows | 7 | 🟠 high |
| 76 | [Argo: default ServiceAccount + token automount](../scenarios/76-argo-default-serviceaccount/README.md) | Argo Workflows | 2 | 🟡 medium |
| 77 | [Drone: `privileged: true` step](../scenarios/77-drone-privileged-step/README.md) | Drone CI | 7 | 🟠 high |
| 78 | [Drone: step `image:` mutable tag](../scenarios/78-drone-image-unpinned/README.md) | Drone CI | 3 · 9 | 🟡 medium |
| 79 | [Buildkite: `$BUILDKITE_*` command injection](../scenarios/79-buildkite-var-injection/README.md) | Buildkite | 4 | 🟠 high |
| 80 | [Buildkite: plugin pinned to a mutable ref](../scenarios/80-buildkite-plugin-unpinned/README.md) | Buildkite | 3 | 🟡 medium |
| 81 | [Cloud Build: step image not pinned by digest](../scenarios/81-cloudbuild-image-unpinned/README.md) | Cloud Build | 3 · 9 | 🟡 medium |
| 82 | [Cloud Build: runs as default service account](../scenarios/82-cloudbuild-default-serviceaccount/README.md) | Cloud Build | 2 | 🟡 medium |
| 83 | [Tekton: privileged step + hostPath node escape](../scenarios/83-tekton-hostpath-escape/README.md) | Tekton | 7 | 🔴 critical |
| 84 | [Argo: hostPath mount → node filesystem escape](../scenarios/84-argo-hostpath-escape/README.md) | Argo Workflows | 7 | 🔴 critical |
| 85 | [GitLab: fork MR pipeline mints cloud OIDC token](../scenarios/85-gitlab-fork-pipeline-oidc/README.md) | GitLab CI | 4 · 2 | 🔴 critical |
| 86 | [Jenkins: builds untrusted fork PRs with creds (PPE)](../scenarios/86-jenkins-untrusted-pr-build/README.md) | Jenkins | 4 | 🔴 critical |
| 87 | [CircleCI: secrets passed to forked PRs](../scenarios/87-circleci-forked-pr-secrets/README.md) | CircleCI | 6 · 4 | 🔴 critical |
| 88 | [Bitbucket: fork PR pipeline exposes secrets](../scenarios/88-bitbucket-forked-pr-secrets/README.md) | Bitbucket Pipelines | 6 · 4 | 🔴 critical |
| 89 | [GHA: `terraform apply` on untrusted PR (IaC RCE)](../scenarios/89-iac-apply-untrusted/README.md) | GitHub Actions | 4 | 🔴 critical |
| 90 | [Azure: untrusted `resources` template on self-hosted agent](../scenarios/90-azure-untrusted-template-selfhosted/README.md) | Azure Pipelines | 3 · 7 | 🔴 critical |
| 91 | [GitLab: `terraform apply` in a merge-request pipeline](../scenarios/91-gitlab-iac-apply-mr/README.md) | GitLab CI | 4 | 🔴 critical |
| 92 | [Argo: cluster-admin ServiceAccount → cluster takeover](../scenarios/92-argo-cluster-admin-sa/README.md) | Argo Workflows | 2 · 5 | 🔴 critical |
| 93 | [Drone: privileged step mounts host Docker socket](../scenarios/93-drone-host-socket/README.md) | Drone CI | 7 | 🔴 critical |
| 94 | [Dockerfile: container runs as root (no USER)](../scenarios/94-dockerfile-root-user/README.md) | Dockerfile | 7 | 🟠 high |
| 95 | [Dockerfile: base image unpinned (`:latest`)](../scenarios/95-dockerfile-unpinned-base/README.md) | Dockerfile | 3 · 9 | 🟡 medium |
| 96 | [Dockerfile: hardcoded secret in `ENV`](../scenarios/96-dockerfile-secret-in-env/README.md) | Dockerfile | 6 | 🟠 high |
| 97 | [Kubernetes: privileged container](../scenarios/97-k8s-privileged-container/README.md) | Kubernetes | 7 | 🔴 critical |
| 98 | [Kubernetes: hostPath mount of node root](../scenarios/98-k8s-hostpath-mount/README.md) | Kubernetes | 7 | 🔴 critical |
| 99 | [Kubernetes: root + allowPrivilegeEscalation](../scenarios/99-k8s-allow-priv-escalation/README.md) | Kubernetes | 7 | 🟠 high |
| 100 | [Terraform: IAM policy `*:*` (full admin)](../scenarios/100-terraform-iam-admin/README.md) | Terraform | 2 | 🔴 critical |
| 101 | [Terraform: security group SSH open to 0.0.0.0/0](../scenarios/101-terraform-sg-open/README.md) | Terraform | 7 | 🟠 high |
| 102 | [Terraform: S3 bucket public-access-block disabled](../scenarios/102-terraform-s3-public/README.md) | Terraform | 7 · 6 | 🟠 high |
| 103 | [CloudFormation: S3 bucket public read+write](../scenarios/103-cloudformation-s3-public/README.md) | CloudFormation | 7 · 6 | 🟠 high |
| 104 | [Helm: privileged container in chart template](../scenarios/104-helm-privileged-pod/README.md) | Helm | 7 | 🔴 critical |
| 105 | [GHA: Codecov-style remote uploader piped to shell](../scenarios/105-codecov-bash-uploader/README.md) | GitHub Actions | 8 · 3 | 🟠 high |
| 106 | [GitLab: `include: remote:` unpinned 3rd-party template](../scenarios/106-gitlab-include-remote/README.md) | GitLab CI | 8 · 3 | 🟠 high |
| 107 | [GHA: org secret handed to unpinned 3rd-party action](../scenarios/107-thirdparty-action-broad-secret/README.md) | GitHub Actions | 8 · 6 | 🟠 high |
| 108 | [GHA: deploy job missing environment binding](../scenarios/108-deploy-no-environment/README.md) | GitHub Actions | 1 | 🟡 medium |
| 109 | [GHA: self-hosted deploy without environment gate](../scenarios/109-selfhosted-deploy-no-gate/README.md) | GitHub Actions | 1 · 7 | 🟠 high |
| 110 | [GitLab: manual deploy defaults to allow_failure](../scenarios/110-gitlab-manual-allow-failure/README.md) | GitLab CI | 1 | 🟡 medium |
| 111 | [Terraform: CloudTrail logging disabled / single-region](../scenarios/111-terraform-cloudtrail-disabled/README.md) | Terraform | 10 | 🟠 high |
| 112 | [Terraform: VPC flow logs + S3 access logging off](../scenarios/112-terraform-no-flow-logs/README.md) | Terraform | 10 | 🟡 medium |
| 113 | [GitLab: `CI_DEBUG_TRACE` leaks secrets to job log](../scenarios/113-gitlab-debug-trace/README.md) | GitLab CI | 10 · 6 | 🟡 medium |
<!-- /AUTOGEN:scenarios-index -->

> [!NOTE]
> **Full OWASP CICD-SEC top 10 coverage** — every category 1 through 10
> has at least one scenario. See
> [`scenarios/README.md`](../scenarios/README.md#owasp-cicd-sec-top-10--full-coverage)
> for the per-category mapping.

Each scenario has a writeup at `scenarios/NN-*/README.md` with the
exploitation walkthrough, the per-scanner coverage notes, and the fix.
