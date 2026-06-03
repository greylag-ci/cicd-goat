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
| 1 | Insufficient flow control | 5 | 3/5 | 0/3 | 0/3 | 0/3 | 0/5 | 0/3 | 0/3 | 1/1 |
| 2 | Inadequate IAM | 6 | 4/6 | 0/3 | 0/3 | 0/3 | 0/6 | 0/3 | 0/3 | 1/2 |
| 3 | Dependency chain abuse | 19 | 13/19 | 3/10 | 3/10 | 2/10 | 2/19 | 0/10 | 0/10 | 3/3 |
| 4 | Poisoned pipeline execution | 24 | 17/24 | 10/15 | 8/15 | 4/15 | 8/23 | 6/15 | 10/15 | 2/4 |
| 5 | Insufficient PBAC | 7 | 5/7 | 3/6 | 1/6 | 0/6 | 1/7 | 0/6 | 1/6 | 1/1 |
| 6 | Insufficient credential hygiene | 10 | 8/10 | 3/4 | 1/4 | 2/4 | 0/10 | 0/4 | 1/4 | 2/2 |
| 7 | Insecure system configuration | 8 | 6/8 | 0/3 | 1/3 | 0/3 | 0/8 | 0/3 | 1/3 | 1/2 |
| 8 | Ungoverned 3rd-party services | 1 | 1/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | 0/1 | — |
| 9 | Improper artifact integrity validation | 11 | 9/11 | 3/6 | 1/6 | 0/6 | 2/11 | 0/6 | 1/6 | 2/2 |
| 10 | Insufficient logging & visibility | 2 | 1/2 | 0/1 | 0/1 | 0/1 | 0/2 | 0/1 | 0/1 | — |
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
| 🔴 critical | 11 | 9/11 | 3/9 | 3/9 | 0/9 | 0/11 | 0/9 | 3/9 | 0/1 |
| 🟠 high | 41 | 28/41 | 10/23 | 8/23 | 7/23 | 8/40 | 6/23 | 9/23 | 5/7 |
| 🟡 medium | 14 | 11/14 | 3/6 | 1/6 | 0/6 | 3/14 | 0/6 | 0/6 | 2/2 |
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
| 22 | [GCP OIDC over-broad WIF](../scenarios/22-gcp-oidc-broad-wif/README.md) | **pipeline&#x2011;check** |
| 23 | [`github-actions[bot]` branch-protection bypass](../scenarios/23-actions-bot-branch-protection-bypass/README.md) | **pipeline&#x2011;check** |
| 24 | [Third-party webhook exfiltration](../scenarios/24-third-party-webhook-exfil/README.md) | **pipeline&#x2011;check** |
| 25 | [Environment branch-pattern bypass](../scenarios/25-environment-branch-pattern-bypass/README.md) | **pipeline&#x2011;check** |
| 27 | [Secret leak in workflow logs](../scenarios/27-secret-leak-in-logs/README.md) | **pipeline&#x2011;check** |
| 28 | [Reusable workflow `${{ inputs.* }}` injection](../scenarios/28-reusable-workflow-input-injection/README.md) | **pipeline&#x2011;check** |
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

**Solo catches per scanner** — scenarios where this is the only ✅ on the row:

| Scanner | Solo catches |
| :-- | :-: |
| pipeline&#x2011;check | **21** |
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
