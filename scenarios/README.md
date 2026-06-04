# Scenarios

One hundred and twenty deliberately-vulnerable pipelines and IaC manifests, each
demonstrating one canonical attack pattern from the modern threat landscape.
**Scenarios 01–38 (and 89) are GitHub Actions** workflows; scenarios 30–33 are
**variants** of scenario 02
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
pipelines live: **GitLab CI** (39, 41–48, 85), **Jenkins** (40, 67–70, 86),
**Azure Pipelines** (49–54), **CircleCI** (55–60, 87), **Bitbucket Pipelines**
(61–66, 88), **Tekton** (71–73, 83), **Argo Workflows** (74–76, 84),
**Drone CI** (77–78), **Buildkite** (79–80), and **Google Cloud Build** (81–82).
Only the scanners that actually parse a given provider's files score those rows;
the rest render `—` (not-applicable). A few rows are still all-miss **next-gen
targets** — canonical bugs (the CircleCI uncertified-orb namespace, Jenkins
`input`-without-submitter, and the configuration-spread fork-trust PPE) that no
scanner here catches yet. pipeline-check 1.9.0 closed several earlier gaps in
this band (Azure/CircleCI injection, persist-credentials, the Mandiant
secret-to-artifact leak, `skip-ssl-verify`).
**Scenarios 83–93 add critical examples**: container/cluster escape (hostPath →
node takeover, Tekton/Argo 83/84; host Docker socket, Drone 93), fork-PR RCE /
secret-theft (the "pwn request" class, GitLab/Jenkins/CircleCI/Bitbucket 85–88),
**IaC plan/apply RCE** (`terraform apply` on untrusted PR/MR — GHA 89, GitLab 91),
an untrusted external template on a self-hosted agent (Azure 90), and K8s RBAC
takeover (Argo cluster-admin SA 92).

**Scenarios 94–104 extend coverage to IaC / manifest types** — the artifacts
pipelines build and deploy: **Dockerfile** (94–96), **Kubernetes** (97–99),
**Terraform** (100–102), **CloudFormation** (103), and **Helm** (104). These are
the corpus's richest multi-scanner rows: Checkov + KICS (the IaC specialists)
score them alongside pipeline-check's Dockerfile/Kubernetes/Helm rules.

**Scenarios 105–113 fill the thinnest OWASP categories** — the governance and
visibility classes scanners rarely cover: **CICD-SEC-8** ungoverned 3rd-party
services (Codecov-style remote uploader 105, GitLab remote `include:` 106, an
org secret handed to an unpinned 3rd-party action 107), **CICD-SEC-1**
insufficient flow control (deploy with no `environment:` gate 108, self-hosted
ungated deploy 109, GitLab manual job that silently `allow_failure`s 110), and
**CICD-SEC-10** insufficient logging/visibility (Terraform CloudTrail-off 111
and no-flow-logs 112, GitLab `CI_DEBUG_TRACE` secret-to-log leak 113, caught by
pipeline-check `GL-038` as of 1.9.0).

**Scenarios 114–120 grow the thinnest IaC formats** alongside a 9th scanner,
**Trivy** (the dedicated IaC/container misconfiguration scanner — it renders
Helm charts and parses Dockerfile/Kubernetes/Terraform/CloudFormation): more
**CloudFormation** (SG-open 114, IAM admin 115, RDS unencrypted+public 116),
**Helm** (weak securityContext 117, hostPath 118), and **Terraform** (S3
unencrypted 119, RDS public+unencrypted 120). These IaC rows are now scored by
**four** tools — Trivy + Checkov + KICS + pipeline-check — the corpus's richest
cross-scanner comparison.

See the per-provider leaderboards in the [README](../README.md) and the
sectioned [matrix](../docs/MATRIX.md).

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
| 83 | [Tekton — privileged + hostPath node escape](83-tekton-hostpath-escape/README.md) | 7 | **Tekton** 🔴 — container/node escape |
| 84 | [Argo — hostPath node filesystem escape](84-argo-hostpath-escape/README.md) | 7 | **Argo** 🔴 — container/node escape |
| 85 | [GitLab — fork MR pipeline mints cloud OIDC token](85-gitlab-fork-pipeline-oidc/README.md) | 4, 2 | **GitLab** 🔴 — fork RCE → cloud creds |
| 86 | [Jenkins — builds untrusted fork PRs with creds](86-jenkins-untrusted-pr-build/README.md) | 4 | **Jenkins** 🔴 — PPE (config-spread) |
| 87 | [CircleCI — secrets passed to forked PRs](87-circleci-forked-pr-secrets/README.md) | 6, 4 | **CircleCI** 🔴 — pwn-request secret theft |
| 88 | [Bitbucket — fork PR pipeline exposes secrets](88-bitbucket-forked-pr-secrets/README.md) | 6, 4 | **Bitbucket** 🔴 — pwn-request secret theft |
| 89 | [GHA — `terraform apply` on untrusted PR](89-iac-apply-untrusted/README.md) | 4 | **GitHub Actions** 🔴 — IaC plan/apply RCE |
| 90 | [Azure — untrusted template on self-hosted agent](90-azure-untrusted-template-selfhosted/README.md) | 3, 7 | **Azure** 🔴 — supply-chain RCE + foothold |
| 91 | [GitLab — `terraform apply` in MR pipeline](91-gitlab-iac-apply-mr/README.md) | 4 | **GitLab** 🔴 — IaC plan/apply RCE |
| 92 | [Argo — cluster-admin ServiceAccount](92-argo-cluster-admin-sa/README.md) | 2, 5 | **Argo** 🔴 — K8s RBAC cluster takeover |
| 93 | [Drone — privileged step mounts host Docker socket](93-drone-host-socket/README.md) | 7 | **Drone** 🔴 — host-socket escape |
| 94 | [Dockerfile — container runs as root (no USER)](94-dockerfile-root-user/README.md) | 7 | **Dockerfile** — root container |
| 95 | [Dockerfile — base image unpinned (`:latest`)](95-dockerfile-unpinned-base/README.md) | 3, 9 | **Dockerfile** — mutable base image |
| 96 | [Dockerfile — hardcoded secret in `ENV`](96-dockerfile-secret-in-env/README.md) | 6 | **Dockerfile** — secret in image layer |
| 97 | [Kubernetes — privileged container](97-k8s-privileged-container/README.md) | 7 | **Kubernetes** 🔴 — privileged pod |
| 98 | [Kubernetes — hostPath mount of node root](98-k8s-hostpath-mount/README.md) | 7 | **Kubernetes** 🔴 — node escape |
| 99 | [Kubernetes — root + allowPrivilegeEscalation](99-k8s-allow-priv-escalation/README.md) | 7 | **Kubernetes** — weak pod securityContext |
| 100 | [Terraform — IAM policy `*:*` (full admin)](100-terraform-iam-admin/README.md) | 2 | **Terraform** 🔴 — admin IAM policy |
| 101 | [Terraform — security group SSH open to world](101-terraform-sg-open/README.md) | 7 | **Terraform** — 0.0.0.0/0 ingress |
| 102 | [Terraform — S3 public-access-block disabled](102-terraform-s3-public/README.md) | 7, 6 | **Terraform** — public bucket |
| 103 | [CloudFormation — S3 bucket public read+write](103-cloudformation-s3-public/README.md) | 7, 6 | **CloudFormation** — public bucket |
| 104 | [Helm — privileged container in chart template](104-helm-privileged-pod/README.md) | 7 | **Helm** 🔴 — privileged pod in chart |
| 105 | [GHA — Codecov-style remote uploader piped to shell](105-codecov-bash-uploader/README.md) | 8, 3 | **GitHub Actions** — ungoverned 3rd-party (Codecov 2021) |
| 106 | [GitLab — `include: remote:` unpinned template](106-gitlab-include-remote/README.md) | 8, 3 | **GitLab** — ungoverned 3rd-party include |
| 107 | [GHA — org secret handed to unpinned 3rd-party action](107-thirdparty-action-broad-secret/README.md) | 8, 6 | **GitHub Actions** — over-scoped 3rd-party secret |
| 108 | [GHA — deploy job missing environment binding](108-deploy-no-environment/README.md) | 1 | **GitHub Actions** — ungated deploy |
| 109 | [GHA — self-hosted deploy without environment gate](109-selfhosted-deploy-no-gate/README.md) | 1, 7 | **GitHub Actions** 🔴 — ungated self-hosted deploy |
| 110 | [GitLab — manual deploy defaults to `allow_failure`](110-gitlab-manual-allow-failure/README.md) | 1 | **GitLab** — fake approval gate |
| 111 | [Terraform — CloudTrail logging disabled / single-region](111-terraform-cloudtrail-disabled/README.md) | 10 | **Terraform** — blind audit trail |
| 112 | [Terraform — VPC flow logs + S3 access logging off](112-terraform-no-flow-logs/README.md) | 10 | **Terraform** — unobservable infra |
| 113 | [GitLab — `CI_DEBUG_TRACE` leaks secrets to job log](113-gitlab-debug-trace/README.md) | 10, 6 | **GitLab** — secrets in the audit log |
| 114 | [CloudFormation — security group SSH open to world](114-cfn-sg-open/README.md) | 7 | **CloudFormation** — 0.0.0.0/0 ingress |
| 115 | [CloudFormation — IAM managed policy `*:*`](115-cfn-iam-admin/README.md) | 2 | **CloudFormation** 🔴 — admin IAM policy |
| 116 | [CloudFormation — RDS unencrypted + public](116-cfn-rds-unencrypted-public/README.md) | 7, 2 | **CloudFormation** — exposed/unencrypted DB |
| 117 | [Helm — container runs as root + privilege escalation](117-helm-weak-securitycontext/README.md) | 7 | **Helm** — weak pod securityContext |
| 118 | [Helm — hostPath mount of node root in chart](118-helm-hostpath/README.md) | 7 | **Helm** 🔴 — node escape in chart |
| 119 | [Terraform — S3 bucket unencrypted + unversioned](119-terraform-s3-unencrypted/README.md) | 7 | **Terraform** — unencrypted bucket |
| 120 | [Terraform — RDS publicly accessible + unencrypted](120-terraform-rds-public/README.md) | 7, 2 | **Terraform** — exposed/unencrypted DB |

## OWASP CICD-SEC top 10 — full coverage

| Risk | Coverage | Scenarios |
|:---|:---|:---|
| CICD-SEC-1: Insufficient Flow Control Mechanisms              | ✅ | 23, 25, 37, 43, 66, 68, 108, 109, 110 |
| CICD-SEC-2: Inadequate Identity and Access Management         | ✅ | 10, 22, 36, 41, 47, 52, 76, 82, 85, 92, 100, 115, 116, 120 |
| CICD-SEC-3: Dependency Chain Abuse                            | ✅ | 3, 9, 11, 12, 16, 19, 20, 29, 35, 38, 42, 45, 46, 53, 55, 58, 60, 63, 64, 69, 73, 78, 80, 81, 90, 95, 105, 106 |
| CICD-SEC-4: Poisoned Pipeline Execution                       | ✅ | 1, 2, 5, 7, 13, 14, 18, 21, 28, 30, 31, 32, 33, 34, 38, 39, 40, 45, 48, 49, 50, 56, 62, 66, 67, 71, 74, 79, 85, 86, 87, 88, 89, 91 |
| CICD-SEC-5: Insufficient Pipeline-Based Access Controls       | ✅ | 1, 4, 6, 25, 26, 36, 41, 68, 70, 92 |
| CICD-SEC-6: Insufficient Credential Hygiene                   | ✅ | 6, 12, 15, 17, 43, 44, 51, 52, 59, 61, 87, 88, 96, 102, 103, 107, 113 |
| CICD-SEC-7: Insecure System Configuration                     | ✅ | 8, 10, 22, 47, 48, 54, 57, 65, 70, 72, 75, 77, 83, 84, 90, 93, 94, 97, 98, 99, 101, 102, 103, 104, 109, 114, 116, 117, 118, 119, 120 |
| CICD-SEC-8: Ungoverned Usage of Third-Party Services          | ✅ | 24, 105, 106, 107 |
| CICD-SEC-9: Improper Artifact Integrity Validation            | ✅ | 5, 7, 9, 17, 19, 35, 42, 46, 53, 58, 64, 73, 78, 81, 95 |
| CICD-SEC-10: Insufficient Logging and Visibility              | ✅ | 27, 61, 111, 112, 113 |

Every risk in the top 10 has at least one scenario. See the
[OWASP Top 10 CI/CD Security Risks](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
for the canonical definitions.
