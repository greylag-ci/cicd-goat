# Coverage axes

The leaderboard answers _"how many canonical bugs does each scanner
catch?"_ — one strong number, but it hides three other comparisons.

This page slices the same per-scenario verdicts three more ways:

1. **By OWASP CICD-SEC category** — which of the 10 risk categories
   does each scanner have *any* catch in?
2. **By severity** — does a scanner that does well on highs also do
   well on criticals, or is its coverage skewed?
3. **Solo catches** — for which scenarios is a given scanner the
   *only* one that catches the canonical bug?

All three tables are auto-generated from
[`tools/scenarios.yaml`](../tools/scenarios.yaml) +
[`scanner-comparison`](../../../actions/workflows/scanner-comparison.yml)
SARIF by [`tools/regen-readme.py`](../tools/regen-readme.py). Same
scoring rule as the [main matrix](MATRIX.md): a cell increments only
when the scanner emits a rule whose description names the canonical
bug for that scenario.

---

## ① Coverage by OWASP CICD-SEC category

Each scenario is mapped to one or more
[CICD-SEC categories](https://owasp.org/www-project-top-10-ci-cd-security-risks/).
The cell is `caught / total` — how many scenarios in that category
the scanner gets ✅ on, out of how many scenarios fall in the category
overall (a scenario in two categories counts once in each row).

<!-- AUTOGEN:cicd-sec-coverage -->
| # | Category | Scenarios | pipeline&#x2011;check | zizmor | poutine | KICS | Checkov | actionlint | octoscan | ciguard |
| :-: | :-- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 1 | Insufficient flow control | 9 | 6/9 | 0/5 | 0/5 | 0/5 | 0/8 | 0/5 | 0/5 | 2/3 |
| 2 | Inadequate IAM | 11 | 7/10 | 0/3 | 0/3 | 1/4 | 3/10 | 0/3 | 0/3 | 2/3 |
| 3 | Dependency chain abuse | 28 | 24/28 | 3/11 | 4/11 | 3/12 | 3/23 | 0/11 | 0/11 | 4/5 |
| 4 | Poisoned pipeline execution | 34 | 24/34 | 10/16 | 8/16 | 4/16 | 8/29 | 6/16 | 10/16 | 3/8 |
| 5 | Insufficient PBAC | 10 | 6/10 | 3/6 | 1/6 | 0/6 | 1/8 | 0/6 | 1/6 | 2/3 |
| 6 | Insufficient credential hygiene | 17 | 12/15 | 4/5 | 2/5 | 5/8 | 2/17 | 0/5 | 2/5 | 2/3 |
| 7 | Insecure system configuration | 25 | 20/22 | 0/4 | 1/4 | 6/11 | 9/20 | 0/4 | 1/4 | 2/3 |
| 8 | Ungoverned 3rd-party services | 4 | 4/4 | 1/3 | 2/3 | 1/3 | 0/4 | 0/3 | 1/3 | 1/1 |
| 9 | Improper artifact integrity validation | 15 | 13/15 | 3/6 | 1/6 | 1/7 | 3/12 | 0/6 | 1/6 | 2/2 |
| 10 | Insufficient logging & visibility | 5 | 1/3 | 0/1 | 0/1 | 2/3 | 2/5 | 0/1 | 0/1 | 0/1 |
<!-- /AUTOGEN:cicd-sec-coverage -->

> Read this table for **shape**, not absolute leaderboard position.
> A scanner that's `0/N` across multiple categories is blind to
> entire classes of bug, even if its overall ✅ count looks fine.
> A `1/1` on a small category is less informative than `3/5` on a
> larger one.

---

## ② Coverage by severity

Same `caught / total` shape, this time grouped by the severity we
assign to each scenario in
[`scenarios.yaml`](../tools/scenarios.yaml).

<!-- AUTOGEN:severity-coverage -->
| Severity | Scenarios | pipeline&#x2011;check | zizmor | poutine | KICS | Checkov | actionlint | octoscan | ciguard |
| :-- | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 🔴 critical | 27 | 23/26 | 3/10 | 3/10 | 2/13 | 4/23 | 0/10 | 3/10 | 1/5 |
| 🟠 high | 61 | 42/57 | 11/26 | 10/26 | 14/33 | 15/53 | 6/26 | 10/26 | 7/11 |
| 🟡 medium | 25 | 20/24 | 3/7 | 1/7 | 2/9 | 6/20 | 0/7 | 0/7 | 3/4 |
<!-- /AUTOGEN:severity-coverage -->

> If a scanner's critical-row fraction is meaningfully lower than its
> high-row fraction, that's worth examining: the criticals on this
> corpus are mostly the multi-file / configuration-spread bugs
> (scenarios 1, 7, 8, 10, 17, 19, 20, 22, 29) — exactly where single-
> file YAML pattern matching runs out of road.

---

## ③ Solo catches

Scenarios where exactly one scanner emits the canonical-bug rule.
Adding the scanner to your stack is the only way to cover these
scenarios from the field tested here.

<!-- AUTOGEN:unique-catches -->
| #  | Scenario | Solo catcher |
| :-: | :-- | :-- |
| 05 | [Cache poisoning via PR title](../scenarios/05-cache-poisoning-pr-controlled/README.md) | **pipeline&#x2011;check** |
| 10 | [AWS OIDC wildcard `sub`](../scenarios/10-oidc-aws-wildcard-sub/README.md) | **pipeline&#x2011;check** |
| 11 | [`pip install` no hashes](../scenarios/11-pip-install-no-hashes/README.md) | **pipeline&#x2011;check** |
| 19 | [Codecov-style trusted-installer](../scenarios/19-codecov-style-installer/README.md) | **pipeline&#x2011;check** |
| 20 | [Dependency confusion (Birsan)](../scenarios/20-dependency-confusion/README.md) | **pipeline&#x2011;check** |
| 23 | [`github-actions[bot]` branch-protection bypass](../scenarios/23-actions-bot-branch-protection-bypass/README.md) | **pipeline&#x2011;check** |
| 24 | [Third-party webhook exfiltration](../scenarios/24-third-party-webhook-exfil/README.md) | **pipeline&#x2011;check** |
| 25 | [Environment branch-pattern bypass](../scenarios/25-environment-branch-pattern-bypass/README.md) | **pipeline&#x2011;check** |
| 27 | [Secret leak in workflow logs](../scenarios/27-secret-leak-in-logs/README.md) | **pipeline&#x2011;check** |
| 28 | [Reusable workflow `${{ inputs.* }}` injection](../scenarios/28-reusable-workflow-input-injection/README.md) | **pipeline&#x2011;check** |
| 29 | [npm lifecycle-script RCE](../scenarios/29-npm-lifecycle-script-rce/README.md) | **pipeline&#x2011;check** |
| 39 | [GitLab CI: script injection via `$CI_*` / MR vars](../scenarios/39-gitlab-ci-script-injection/README.md) | **pipeline&#x2011;check** |
| 40 | [Jenkins: `sh` string-interpolation injection](../scenarios/40-jenkins-shell-injection/README.md) | **pipeline&#x2011;check** |
| 41 | [GitLab: `CI_JOB_TOKEN` cross-project access](../scenarios/41-gitlab-ci-job-token-cross-project/README.md) | **ciguard** |
| 47 | [GitLab: OIDC `id_tokens` over-broad aud/sub](../scenarios/47-gitlab-oidc-broad-aud-sub/README.md) | **pipeline&#x2011;check** |
| 48 | [GitLab: untagged shared-runner + privileged dind](../scenarios/48-gitlab-shared-runner-privileged/README.md) | **ciguard** |
| 52 | [Azure: `addSpnToEnvironment` SP-secret exposure](../scenarios/52-azure-spn-to-environment/README.md) | **pipeline&#x2011;check** |
| 53 | [Azure: `resources: repositories` untrusted ref](../scenarios/53-azure-resources-untrusted-repo/README.md) | **pipeline&#x2011;check** |
| 54 | [Azure: self-hosted pool for untrusted builds](../scenarios/54-azure-self-hosted-untrusted/README.md) | **pipeline&#x2011;check** |
| 55 | [CircleCI: orb pinned to `@volatile`](../scenarios/55-circleci-orb-volatile/README.md) | **pipeline&#x2011;check** |
| 57 | [CircleCI: `machine: true` privileged executor](../scenarios/57-circleci-machine-privileged/README.md) | **pipeline&#x2011;check** |
| 59 | [CircleCI: hardcoded secret in `environment:`](../scenarios/59-circleci-secret-in-environment/README.md) | **pipeline&#x2011;check** |
| 62 | [Bitbucket: `$BITBUCKET_*` script injection](../scenarios/62-bitbucket-var-injection/README.md) | **pipeline&#x2011;check** |
| 63 | [Bitbucket: `pipe:` mutable tag](../scenarios/63-bitbucket-pipe-mutable-tag/README.md) | **pipeline&#x2011;check** |
| 64 | [Bitbucket: `image:` mutable tag](../scenarios/64-bitbucket-image-mutable-tag/README.md) | **Checkov** |
| 67 | [Jenkins: `@Grab` sandbox-bypass (CVE-2019-1003000)](../scenarios/67-jenkins-grab-sandbox-bypass/README.md) | **pipeline&#x2011;check** |
| 69 | [Jenkins: shared library on a mutable `@master` ref](../scenarios/69-jenkins-library-mutable-ref/README.md) | **pipeline&#x2011;check** |
| 72 | [Tekton: privileged / root step](../scenarios/72-tekton-privileged-step/README.md) | **pipeline&#x2011;check** |
| 73 | [Tekton: step `image:` not pinned to a digest](../scenarios/73-tekton-image-unpinned/README.md) | **pipeline&#x2011;check** |
| 74 | [Argo: `{{inputs.parameters}}` injected into args](../scenarios/74-argo-param-injection/README.md) | **pipeline&#x2011;check** |
| 77 | [Drone: `privileged: true` step](../scenarios/77-drone-privileged-step/README.md) | **pipeline&#x2011;check** |
| 78 | [Drone: step `image:` mutable tag](../scenarios/78-drone-image-unpinned/README.md) | **pipeline&#x2011;check** |
| 79 | [Buildkite: `$BUILDKITE_*` command injection](../scenarios/79-buildkite-var-injection/README.md) | **pipeline&#x2011;check** |
| 80 | [Buildkite: plugin pinned to a mutable ref](../scenarios/80-buildkite-plugin-unpinned/README.md) | **pipeline&#x2011;check** |
| 81 | [Cloud Build: step image not pinned by digest](../scenarios/81-cloudbuild-image-unpinned/README.md) | **pipeline&#x2011;check** |
| 82 | [Cloud Build: runs as default service account](../scenarios/82-cloudbuild-default-serviceaccount/README.md) | **pipeline&#x2011;check** |
| 83 | [Tekton: privileged step + hostPath node escape](../scenarios/83-tekton-hostpath-escape/README.md) | **pipeline&#x2011;check** |
| 84 | [Argo: hostPath mount → node filesystem escape](../scenarios/84-argo-hostpath-escape/README.md) | **pipeline&#x2011;check** |
| 87 | [CircleCI: secrets passed to forked PRs](../scenarios/87-circleci-forked-pr-secrets/README.md) | **pipeline&#x2011;check** |
| 88 | [Bitbucket: fork PR pipeline exposes secrets](../scenarios/88-bitbucket-forked-pr-secrets/README.md) | **pipeline&#x2011;check** |
| 90 | [Azure: untrusted `resources` template on self-hosted agent](../scenarios/90-azure-untrusted-template-selfhosted/README.md) | **pipeline&#x2011;check** |
| 91 | [GitLab: `terraform apply` in a merge-request pipeline](../scenarios/91-gitlab-iac-apply-mr/README.md) | **pipeline&#x2011;check** |
| 93 | [Drone: privileged step mounts host Docker socket](../scenarios/93-drone-host-socket/README.md) | **pipeline&#x2011;check** |
| 96 | [Dockerfile: hardcoded secret in `ENV`](../scenarios/96-dockerfile-secret-in-env/README.md) | **pipeline&#x2011;check** |
| 108 | [GHA: deploy job missing environment binding](../scenarios/108-deploy-no-environment/README.md) | **pipeline&#x2011;check** |
| 109 | [GHA: self-hosted deploy without environment gate](../scenarios/109-selfhosted-deploy-no-gate/README.md) | **pipeline&#x2011;check** |

**Solo catches per scanner** — scenarios where this is the only ✅ on the row:

| Scanner | Solo catches |
| :-- | :-: |
| pipeline&#x2011;check | **43** |
| ciguard | **2** |
| Checkov | **1** |
| zizmor | **0** |
| poutine | **0** |
| KICS | **0** |
| actionlint | **0** |
| octoscan | **0** |
<!-- /AUTOGEN:unique-catches -->

> Solo-catch count is a different signal from leaderboard rank. A
> scanner can sit mid-leaderboard and still be the only line of
> defense for a handful of bugs none of the others see — that's worth
> knowing before you pick the scanner with the highest total ✅ and
> drop the rest.

---

## What this view does *not* measure

- **Finding noise.** A scanner can score the same canonical-catch
  count as another while emitting 10× more findings. The leaderboard
  is silent on this; so is this page. See
  [`tools/comparison-report.py`](../tools/comparison-report.py) for a
  total-findings-per-rule breakdown from a single SARIF dir.
- **Severity assigned by the scanner.** All severities on this page
  come from `scenarios.yaml` — *our* judgment of how bad the bug is,
  not the scanner's `level: error/warning/note` choice. Two scanners
  catching the same canonical bug can rate it differently; that's a
  fairness-of-display question, not a coverage question.
- **Absence-of-control rules.** Pipeline-check's hygiene baseline
  (SBOM / SLSA / signing / vuln-scan / `timeout-minutes` /
  digest-pinning) fires on every workflow regardless of canonical
  bug, so it doesn't show up here. See
  [FIELD-TEST.md § ⑤](FIELD-TEST.md#-the-hygiene-baseline--a-scope-difference-layered-on-top-of-a-coverage-one).
