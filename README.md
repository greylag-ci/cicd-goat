> [!WARNING]
> Every workflow file in `.github/workflows/scenario-*.yml` is intentionally broken.
> Do not reuse the patterns. Do not enable Actions on a clone you forgot to read first.

```
══════════════════════════════════════════════════════════════════════════════
   cicd-goat   ·   greylag-ci                                          v1.0
   ──────────────────────────────────────────────────────────────────────
   A test range for CI/CD security scanners.
   27 vulnerable GitHub Actions workflows.  7 scanners.  1 leaderboard.
══════════════════════════════════════════════════════════════════════════════
```

[![scanner-comparison](https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml/badge.svg)](https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml)
[![License Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-3a3a3a?style=flat-square)](LICENSE)
[![CICD-SEC top 10](https://img.shields.io/badge/owasp-CICD--SEC_10%2F10-9c2b2b?style=flat-square)](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
[![scenarios 27](https://img.shields.io/badge/scenarios-27-1f6feb?style=flat-square)](scenarios/README.md)
[![scanners 7](https://img.shields.io/badge/scanners-7-1f6feb?style=flat-square)](#the-full-matrix)

---

## The thesis

> Every CI/CD scanner has blind spots. The only honest way to measure them
> is on a target where the bugs are catalogued in advance. This is that target.

Twenty-seven GitHub Actions workflows. Each one demonstrates one
real-world attack pattern, drawn from named incident disclosures
(tj-actions 2025, Codecov 2021, ArtiPACKED 2024, Birsan dependency
confusion 2021) and from the **OWASP Top 10 CI/CD Security Risks** —
all ten categories have at least one scenario. Every job is gated with
`if: false` so the workflows show up in run history but never spawn
a runner.

Six community scanners + **`pipeline-check`** (the engine behind the
[Pipeline-Check VSCode extension](https://github.com/greylag-ci/pipeline-check-vscode))
get the same input. What the data shows: every scanner has a narrow
lane. **Some scenarios nobody catches.** The matrix below is built
from actual SARIF (community scanners) and the verbatim `pipeline_check
--output json` for this branch.

> [!NOTE]
> **Scoring methodology.** A scanner gets ✅ on a scenario only if it
> emits a rule whose description names the *specific canonical bug*
> for that scenario. Hygiene findings that fire on every workflow file
> (missing SBOM, unpinned `actions/checkout@v4`, no `timeout-minutes`,
> etc.) don't count toward ✅ on a scenario whose canonical bug is
> something else — they're the same finding on every file and tell
> you nothing comparative. Pipeline-check carries a wide hygiene
> baseline that the field doesn't ship; that's a separate, real
> differentiator covered in [section ⑤](#-the-hygiene-baseline-pipeline-checks-real-edge).

---

## Field test — five cinematic scenarios

### ① The `tj-actions` tag move &nbsp;·&nbsp; scenario 03

> [!NOTE]
> **CICD-SEC-3 · Dependency Chain Abuse · CVE-2025-30066.** On March 14, 2025
> the `tj-actions/changed-files` GitHub Action was compromised; the
> injected code dumped Runner Worker memory (including secrets) into the
> workflow log. Over **23,000 repositories** ran the malicious version
> before the rollback. Pinning to a tag instead of a SHA was the whole bug.

```yaml
# .github/workflows/scenario-03-action-mutable-ref.yml
- uses: third-party-org/some-deploy-action@main       # ← branch ref
- uses: another-org/composite@master                   # ← branch ref
- uses: yet-another-org/widget-action@v1               # ← movable tag
```

| scanner            | verdict | rule that fired                                                          |
| :----------------- | :-----: | :----------------------------------------------------------------------- |
| **pipeline-check** |   ✅    | `GHA-001` — _Action not pinned to commit SHA: 4 refs (actions/checkout@v4, third-party-org/..., another-org/..., yet-another-org/...)_ |
| zizmor             |   ✅    | `unpinned-uses`                                                          |
| KICS               |   ✅    | `555ab8f9-…` — _Unpinned Actions Full Length Commit SHA_                 |
| poutine            |   ⚠️   | `github_action_from_unverified_creator_used` — adjacent (creator trust, not SHA pinning), but routes to investigation |
| Checkov            |   ❌    | —                                                                        |
| Trivy              |   ❌    | —                                                                        |
| Gitleaks           |   —     | _(secret scanner)_                                                       |

---

### ② AWS OIDC trust policy with `sub: repo:*` &nbsp;·&nbsp; scenario 10

> [!NOTE]
> **CICD-SEC-2 · Inadequate IAM.** A trust policy with a wildcard subject
> lets *any* GitHub repository assume your production role. The bug
> lives in two files (workflow + IAM trust JSON) and no single scanner
> here covers both ends.

```yaml
# .github/workflows/scenario-10-oidc-aws-wildcard-sub.yml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/example-overly-broad
```
```json
// scenarios/10-oidc-aws-wildcard-sub/trust-policy.json
"Condition": {
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:*"
  }
}
```

| scanner            | sees workflow                                         | sees trust-policy.json |
| :----------------- | :--------------------------------------------------- | :--------------------: |
| **pipeline-check** | ⚠️&nbsp;_Hygiene fires (no SBOM, no SLSA, no signing); no IAM-aware rule yet_ | ❌                     |
| zizmor             | ❌                                                    | ❌                     |
| poutine            | ❌                                                    | ❌                     |
| KICS               | ⚠️&nbsp;_Catches `aws-actions/...@v4` as unpinned_ref, not the wildcard sub_ | ❌                     |
| Checkov            | ❌                                                    | ❌                     |
| Trivy              | ❌                                                    | ❌                     |

> **This is a scanner-comparison miss.** None of the seven scanners
> currently catches the wildcard-sub bug from the workflow side; KICS
> can be made to fire on the IaC side with a different scan config
> (Terraform input, not just Actions). Honest finding; included as
> a benchmark for the hard end.

---

### ③ ArtiPACKED — `.git/` packed into an artifact &nbsp;·&nbsp; scenario 17

> [!NOTE]
> **CICD-SEC-6 · Insufficient Credential Hygiene.** Palo Alto Unit 42
> disclosed in August 2024, finding **14 cases** in production open
> source at Red Hat, Google, AWS, Canonical, Microsoft, and OWASP.
> `actions/checkout` defaults to `persist-credentials: true`, writing
> `GITHUB_TOKEN` into `.git/config`; `upload-artifact` with `path: .`
> then ships it.

```yaml
# .github/workflows/scenario-17-artipacked-git-dir.yml
- uses: actions/checkout@v4
  # persist-credentials defaults to true → token in .git/config
- uses: actions/upload-artifact@v4
  with:
    name: workspace
    path: .            # ← uploads .git/, including .git/config with the token
```

| scanner            | verdict                                                                                 |
| :----------------- | :-------------------------------------------------------------------------------------- |
| zizmor             | ✅&nbsp;`artipacked` (the rule was named after this very disclosure; catches both halves) |
| **pipeline-check** | ⚠️&nbsp;`GHA-037` catches the `persist-credentials` half; no dedicated rule yet for `upload-artifact path: .` |
| poutine            | ❌                                                                                      |
| KICS               | ❌                                                                                      |
| Checkov            | ❌                                                                                      |
| Trivy              | ❌                                                                                      |
| Gitleaks           | ❌&nbsp;_(token isn't in source — only in the artifact)_                                |

> Honest assessment: **zizmor is the only scanner here that ships a
> rule precisely for this disclosure.** Pipeline-check catches half;
> the rest miss entirely.

---

### ④ The silent default: `persist-credentials` &nbsp;·&nbsp; scenario 12

> [!NOTE]
> **CICD-SEC-6 · Insufficient Credential Hygiene.** Same root cause as #③
> without the artifact step. `actions/checkout` *defaults* to writing the
> token. Any later untrusted step in the same job can read it.

```yaml
# .github/workflows/scenario-12-persist-credentials-leak.yml
- uses: actions/checkout@v4
  # ← no persist-credentials: false; GITHUB_TOKEN now in .git/config
- uses: third-party-org/some-build-action@main
```

| scanner            | verdict | rule fired                                              |
| :----------------- | :-----: | :------------------------------------------------------ |
| **pipeline-check** |   ✅    | `GHA-037` — _actions/checkout persists `GITHUB_TOKEN` into `.git/config`_ |
| zizmor             |   ✅    | `artipacked`                                            |
| poutine            |   ⚠️   | `github_action_from_unverified_creator_used` — flags the third-party action, not the persist-credentials root cause |
| KICS               |   ⚠️   | `555ab8f9-…` — fires on `actions/checkout@v4` as unpinned, not on persist-credentials specifically |
| Checkov            |   ❌    | —                                                       |
| Trivy              |   ❌    | —                                                       |
| Gitleaks           |   —     | _(secret scanner)_                                      |

---

### ⑤ The hygiene baseline — pipeline-check's real edge

The strict per-scenario matrix shows pipeline-check leading on
canonical-bug coverage but not by a wide margin. The bigger story is
**what fires on every scenario, that no other scanner ships at all.**
Pipeline-check carries 63 GitHub Actions rules; ~20 of them are
"absence-of-control" hygiene rules that fire on any workflow lacking
the corresponding step. Verbatim findings from this branch:

```
GHA-006   Artifacts not signed (no cosign/sigstore step)
GHA-007   SBOM not produced (no CycloneDX/syft/Trivy-SBOM step)
GHA-024   No SLSA provenance attestation produced
GHA-020   No vulnerability scanning step
GHA-014   Deploy job missing environment binding
GHA-015   Job has no `timeout-minutes`, unbounded build
GHA-051   services / container image is not pinned by digest
GHA-001   Action not pinned to commit SHA — fires on actions/checkout@v4
GHA-037   actions/checkout persists GITHUB_TOKEN into .git/config
```

Hygiene findings on the deploy-style scenarios (01, 10, 17, 22) reach
**7 simultaneous real fires** each — every category SLSA Level 3 cares
about, plus the bug under test. **No other scanner in this comparison
emits SBOM, SLSA, signing, or vuln-scan absence findings at all.**

The strict matrix below scores only the canonical bug per scenario.
The hygiene-baseline edge is what makes pipeline-check the only
single-tool option if you want all of "supply-chain hygiene + CICD-SEC
attack-class coverage" from one scan.

---

## The full matrix

| key | meaning                                                  |
| :-: | :------------------------------------------------------- |
| ✅  | scanner flags the **canonical bug** with a matching rule |
| ⚠️  | scanner partially catches — adjacent rule, half the antipattern, or related but distinct concern |
| ❌  | scanner misses the canonical bug                         |
| —   | not applicable to that scanner's class                   |

Sourced from the latest [`scanner-comparison`](../../actions/workflows/scanner-comparison.yml) SARIF
(`commit 86a4c92`) for the community scanners and `python -m pipeline_check --pipeline github --output json` for pipeline-check.

| #  | Scenario                                          | pipeline&#x2011;check | zizmor | poutine | KICS | Checkov | Trivy | Gitleaks |
| :-:| :------------------------------------------------ | :-------------------: | :----: | :-----: | :--: | :-----: | :---: | :------: |
| 01 | `pull_request_target` + fork-head checkout        |          ✅          |   ✅   |   ✅    |  ❌  |   ❌   |  ❌   |    —     |
| 02 | Script injection via issue title                  |          ✅          |   ✅   |   ✅    |  ✅  |   ✅   |  ❌   |    —     |
| 03 | Action pinned to mutable ref                      |          ✅          |   ✅   |   ⚠️    |  ✅  |   ❌   |  ❌   |    —     |
| 04 | `GITHUB_TOKEN: write-all`                         |          ✅          |   ❌   |   ❌    |  ❌  |   ✅   |  ❌   |    —     |
| 05 | Cache poisoning via PR title                      |          ✅          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 06 | Reusable workflow `secrets: inherit`              |          ✅          |   ✅   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 07 | `workflow_run` artifact RCE                       |          ✅          |   ✅   |   ✅    |  ❌  |   ❌   |  ❌   |    —     |
| 08 | Self-hosted runner on public repo                 |          ✅          |   ❌   |   ✅    |  ❌  |   ❌   |  ❌   |    —     |
| 09 | Container image `:latest`                         |          ✅          |   ✅   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 10 | AWS OIDC wildcard `sub`                           |          ⚠️          |   ❌   |   ❌    |  ⚠️  |   ❌   |  ❌   |    —     |
| 11 | `pip install` no hashes                           |          ✅          |   —    |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 12 | `persist-credentials` leak                        |          ✅          |   ✅   |   ⚠️    |  ⚠️  |   ❌   |  ❌   |    —     |
| 13 | `workflow_dispatch` input injection               |          ✅          |   ✅   |   ❌    |  ❌  |   ✅   |  ❌   |    —     |
| 14 | `$GITHUB_ENV` poisoning                           |          ⚠️          |   ⚠️   |   ✅    |  ❌  |   ✅   |  ❌   |    —     |
| 15 | Hardcoded secret in `env:`                        |          ❌          |   ❌   |   ❌    |  ✅  |   ❌   |  ❌   |    ❌    |
| 16 | `curl \| sh` install                              |          ✅          |   ❌   |   ✅    |  ❌  |   ❌   |  ❌   |    —     |
| 17 | ArtiPACKED — `.git/` in artifact                  |          ⚠️          |   ✅   |   ❌    |  ❌  |   ❌   |  ❌   |    ❌    |
| 18 | Composite action `${{ inputs.* }}` injection      |          ❌          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 19 | Codecov-style trusted-installer                   |          ❌          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 20 | Dependency confusion (Birsan)                     |          ❌          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 21 | Matrix expansion injection                        |          ❌          |   ✅   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 22 | GCP OIDC over-broad WIF                           |          ❌          |   ❌   |   ❌    |  ⚠️  |   ❌   |  ❌   |    —     |
| 23 | `github-actions[bot]` branch-protection bypass    |          ❌          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 24 | Third-party webhook exfiltration                  |          ❌          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 25 | Environment branch-pattern bypass                 |          ❌          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 26 | GitHub App token over-scope                       |          ❌          |   ✅   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 27 | Secret leak in workflow logs                      |          ❌          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
|    | **canonical bugs caught**                         |   **13 ✅ · 2 ⚠️**   | **11 ✅ · 1 ⚠️** | **6 ✅ · 2 ⚠️** | **3 ✅ · 3 ⚠️** | **4 ✅** | 0 | 0 |

> [!IMPORTANT]
> Six scenarios (18, 19, 20, 23, 24, 25, 27) are **caught by no scanner
> in this comparison.** Those are the hard cases — multi-file scope,
> network-egress reasoning, GitHub-settings-level configuration that
> doesn't appear in any file. Their primary value here is as a target
> for the *next* generation of rules.

---

## Scenarios index

| #  | Title                                                                                                | CICD-SEC  | Severity     |
| :-:| :--------------------------------------------------------------------------------------------------- | :-------: | :----------- |
| 01 | [`pull_request_target` + fork-head checkout](scenarios/01-prtarget-checkout-head/README.md)          |   4 · 5   | 🔴 critical |
| 02 | [Script injection via issue title](scenarios/02-script-injection-issue-title/README.md)              |     4     | 🟠 high     |
| 03 | [Action pinned to mutable ref](scenarios/03-action-mutable-ref/README.md)                            |     3     | 🟠 high     |
| 04 | [`GITHUB_TOKEN` `write-all`](scenarios/04-github-token-write-all/README.md)                          |     5     | 🟡 medium   |
| 05 | [Cache poisoning via PR title](scenarios/05-cache-poisoning-pr-controlled/README.md)                 |   4 · 9   | 🟠 high     |
| 06 | [Reusable workflow `secrets: inherit`](scenarios/06-reusable-secrets-inherit/README.md)              |   5 · 6   | 🟡 medium   |
| 07 | [`workflow_run` artifact RCE](scenarios/07-workflow-run-artifact-rce/README.md)                      |   4 · 9   | 🔴 critical |
| 08 | [Self-hosted runner on public repo](scenarios/08-self-hosted-public-fork/README.md)                  |     7     | 🔴 critical |
| 09 | [Container image `:latest`](scenarios/09-container-image-latest/README.md)                           |   3 · 9   | 🟡 medium   |
| 10 | [AWS OIDC wildcard subject](scenarios/10-oidc-aws-wildcard-sub/README.md)                            |   2 · 7   | 🔴 critical |
| 11 | [`pip install` no hashes](scenarios/11-pip-install-no-hashes/README.md)                              |     3     | 🟡 medium   |
| 12 | [`persist-credentials` leak](scenarios/12-persist-credentials-leak/README.md)                        |   6 · 3   | 🟠 high     |
| 13 | [`workflow_dispatch` input injection](scenarios/13-input-injection-workflow-dispatch/README.md)      |     4     | 🟠 high     |
| 14 | [`$GITHUB_ENV` poisoning](scenarios/14-env-injection-pr-body/README.md)                              |     4     | 🟠 high     |
| 15 | [Hardcoded secret in `env:`](scenarios/15-hardcoded-secret-env/README.md)                            |     6     | 🟠 high     |
| 16 | [`curl \| sh` install](scenarios/16-curl-pipe-sh/README.md)                                          |     3     | 🟡 medium   |
| 17 | [ArtiPACKED — `.git/` in artifact](scenarios/17-artipacked-git-dir/README.md)                        |   6 · 9   | 🔴 critical |
| 18 | [Composite action `${{ inputs.* }}` injection](scenarios/18-composite-action-input-injection/README.md) |  4    | 🟠 high     |
| 19 | [Codecov-style trusted-installer](scenarios/19-codecov-style-installer/README.md)                    |   3 · 9   | 🔴 critical |
| 20 | [Dependency confusion (Birsan)](scenarios/20-dependency-confusion/README.md)                         |     3     | 🔴 critical |
| 21 | [Matrix expansion injection](scenarios/21-matrix-expansion-injection/README.md)                      |     4     | 🟠 high     |
| 22 | [GCP OIDC over-broad WIF](scenarios/22-gcp-oidc-broad-wif/README.md)                                 |   2 · 7   | 🔴 critical |
| 23 | [`github-actions[bot]` branch-protection bypass](scenarios/23-actions-bot-branch-protection-bypass/README.md) | 1 | 🟠 high     |
| 24 | [Third-party webhook exfiltration](scenarios/24-third-party-webhook-exfil/README.md)                 |     8     | 🟠 high     |
| 25 | [Environment branch-pattern bypass](scenarios/25-environment-branch-pattern-bypass/README.md)        |   1 · 5   | 🟠 high     |
| 26 | [GitHub App token over-scope](scenarios/26-app-token-over-scope/README.md)                           |     5     | 🟡 medium   |
| 27 | [Secret leak in workflow logs](scenarios/27-secret-leak-in-logs/README.md)                           |    10     | 🟠 high     |

> [!NOTE]
> **Full OWASP CICD-SEC top 10 coverage** — every category 1 through 10
> has at least one scenario. See [`scenarios/README.md`](scenarios/README.md#owasp-cicd-sec-top-10--full-coverage)
> for the per-category mapping.

> Each scenario has a writeup at `scenarios/NN-*/README.md` with the
> exploitation walkthrough, the per-scanner coverage notes, and the fix.

---

## How the comparison runs

```
                    push   /   pull_request
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │  .github/workflows/scanner-comparison.yml               │
    │                                                         │
    │   zizmor ▸ poutine ▸ checkov ▸ kics ▸ trivy ▸ gitleaks  │
    │                        │                                │
    │                        ▼                                │
    │              upload SARIF                               │
    │       (one Code-Scanning category per tool)             │
    └────────────────────────┬────────────────────────────────┘
                             ▼
                Code Scanning  +  Run Summary
                             │
                             ▼
                tools/comparison-report.py
                             │
                             ▼
                    comparison-report.md
```

Each scanner uploads under a unique `category:` so the
**Security → Code scanning** tab filters per tool. The
[`tools/comparison-report.py`](tools/comparison-report.py) script ingests
the downloaded SARIF artifacts and emits a per-rule × per-scenario
markdown matrix:

```bash
gh run download <run-id> --dir ./sarif-out
python tools/comparison-report.py ./sarif-out --output report.md
```

> [!NOTE]
> `pipeline-check` is currently scored from local `python -m pipeline_check --output json` runs against the scenario tree.
> A dedicated SARIF-emitting job in `scanner-comparison.yml` is the next addition — see [Contributing](#contributing).

---

## Contributing

<details>
<summary><b>Add a scanner</b></summary>

One new job in
[`scanner-comparison.yml`](.github/workflows/scanner-comparison.yml).
Three steps:

1. Install the binary (release tarball, `pip install`, `cargo install`…).
2. Run it with SARIF output.
3. Upload via `github/codeql-action/upload-sarif@v4` under a unique
   `category:` so the Code Scanning tab can split it from the others.

Then add a column to **The full matrix** with the scanner's per-scenario verdict.

</details>

<details>
<summary><b>Add a scenario</b></summary>

1. `.github/workflows/scenario-NN-<name>.yml` — vulnerable pattern in a
   real-looking workflow file, every job gated with `if: false` so the
   workflow shows up in run history but no runner is ever assigned.
2. `scenarios/NN-<name>/README.md` — pattern, exploitation walkthrough,
   expected per-scanner coverage, and the fix.
3. New row in **The full matrix** and in
   [`scenarios/README.md`](scenarios/README.md). Link it from the
   scenarios index above.

</details>

<details>
<summary><b>Disagree with a verdict?</b></summary>

Open an issue with the scenario number, the scanner, the version, and
the SARIF output you got. Verdicts in the matrix track <i>canonical-bug
coverage</i>, not raw finding count; if your scanner version fires a
rule whose description names the canonical bug for that scenario, the
cell flips.

</details>

---

## Why `pipeline-check` is in this comparison

This repo is the test range; [`pipeline-check`](https://github.com/greylag-ci/pipeline-check-vscode)
is one of the engines being tested. Its differentiators on this corpus:

- **Canonical-bug coverage**: 13 ✅ / 2 ⚠️ across 27 scenarios, leading
  the next closest scanner (zizmor) by two. The lead is real but the
  gap is narrower than a raw "finding count" comparison would suggest.
- **Hygiene baseline no one else ships**: 7+ rules per workflow file
  for the supply-chain hygiene categories (SBOM, SLSA, artifact
  signing, vuln-scan presence, environment binding, `timeout-minutes`,
  container digest pinning). Other scanners don't have these rules at
  all, not just don't fire them.
- **Provider breadth**: 23 CI/CD providers and manifest types — AWS,
  Terraform, CloudFormation, GitHub Actions, GitLab CI, Azure DevOps,
  Bitbucket Pipelines, Jenkins, CircleCI, Google Cloud Build,
  Buildkite, Drone CI, Tekton, Argo Workflows, Dockerfile, Kubernetes,
  Helm, OCI image manifests, SCM posture (GitHub / GitLab / Bitbucket),
  npm, pypi.
- **Inline VS Code experience**: gutter squiggles, hover with
  `--explain` prose, severity-graded status bar, keyboard nav,
  findings panel grouped by severity / file / rule.

The VSCode extension is at
[`greylag-ci/pipeline-check-vscode`](https://github.com/greylag-ci/pipeline-check-vscode).
The Python rule engine is at
[`dmartinochoa/pipeline-check`](https://github.com/dmartinochoa/pipeline-check).
Editor findings match `pipeline_check --output json` byte-for-byte.

---

## License & lineage

```
Apache License 2.0  ·  see LICENSE
```

This project started as a soft fork of
[`cider-security-research/cicd-goat`](https://github.com/cider-security-research/cicd-goat)
(Cider Security, later acquired by Palo Alto Networks). All upstream
content has since been removed; the project is now standalone, focused
narrowly on GitHub Actions and the scanner-comparison purpose.

We owe a conceptual debt to the original `cicd-goat` for the format of
mapping deliberate misconfigurations onto the **OWASP Top 10 CI/CD
Security Risks**. If you want to learn the Jenkins / GitLab / CircleCI
side of the same problem space, their original project is still an
excellent companion. See [`NOTICE`](NOTICE) for the full lineage.
