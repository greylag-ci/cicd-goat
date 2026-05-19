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
(Codecov 2021, tj-actions 2025, ArtiPACKED, Birsan's dependency
confusion) and from the OWASP Top 10 CI/CD Security Risks — **all ten
categories** have at least one scenario. Every job is gated with
`if: false` so the workflows show up in run history but never spawn
a runner.

Six community scanners + **`pipeline-check`** (the engine behind the
[Pipeline-Check VSCode extension](https://github.com/greylag-ci/pipeline-check-vscode))
get the same input. The output is what you'd expect from a fair test —
some scanners catch the headline bugs, some catch every bug, some catch
none at all.

---

## Field test — five cinematic scenarios

The point of a test range is to fire it. Five scenarios pulled straight
from named CI/CD incident disclosures, scored on what each scanner
emitted when pointed at the file.

### ① The `tj-actions` tag move &nbsp;·&nbsp; scenario 03

> [!NOTE]
> **CICD-SEC-3 · Dependency Chain Abuse · March 2025.** A single force-moved tag on
> `tj-actions/changed-files` exfiltrated CI secrets from tens of thousands
> of downstream repos. Pinning to a tag instead of a SHA was the whole bug.

```yaml
# .github/workflows/scenario-03-action-mutable-ref.yml
- uses: third-party-org/some-deploy-action@main       # ← branch ref
- uses: another-org/composite@master                   # ← branch ref
- uses: yet-another-org/widget-action@v1               # ← movable tag
```

| scanner            | verdict | rule that fired                                  |
| :----------------- | :-----: | :----------------------------------------------- |
| **pipeline-check** |   ✅    | `Action not pinned to commit SHA — 4 refs`       |
| zizmor             |   ✅    | `unpinned-uses`                                  |
| poutine            |   ✅    | `unpinned_action`                                |
| KICS               |   ✅    | _Unpinned Actions Full Length Commit SHA_        |
| Checkov            |   ❌    | —                                                |
| Trivy              |   ❌    | —                                                |
| Gitleaks           |   —     | _(secret scanner)_                               |

---

### ② AWS OIDC trust policy with `sub: repo:*` &nbsp;·&nbsp; scenario 10

> [!NOTE]
> **CICD-SEC-2 · Inadequate IAM.** A trust policy with a wildcard subject
> lets *any* GitHub repository assume your production role. Workflow-only
> scanners never see the IAM document; IAM-only scanners never see the workflow.

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

| scanner            | sees workflow | sees trust-policy.json  |
| :----------------- | :-----------: | :--------------------:  |
| **pipeline-check** |      ✅       | ⚠️&nbsp;_IAM in roadmap_ |
| zizmor             | ⚠️&nbsp;_partial_ |          ❌          |
| poutine            |      ❌       |          ❌            |
| KICS               |      ✅       | ✅&nbsp;_IaC rule fires_ |
| Checkov            |      ❌       | ⚠️                      |
| Trivy              |      ❌       | ⚠️                      |

> The canary for split-scope scanning. **pipeline-check + KICS** is the
> only pairing in the field that covers both ends of the OIDC handshake
> from a single comparison run. Same shape repeats for GCP in
> [scenario 22](scenarios/22-gcp-oidc-broad-wif/README.md).

---

### ③ ArtiPACKED — `.git/` packed into an artifact &nbsp;·&nbsp; scenario 17

> [!NOTE]
> **CICD-SEC-6 · Insufficient Credential Hygiene.** Documented by Palo Alto
> Unit 42 across hundreds of public repos. `actions/checkout` defaults to
> `persist-credentials: true`, which writes `GITHUB_TOKEN` into `.git/config`;
> `upload-artifact` with `path: .` then ships it to anyone with read access.

```yaml
# .github/workflows/scenario-17-artipacked-git-dir.yml
- uses: actions/checkout@v4
  # persist-credentials defaults to true → token in .git/config
- uses: actions/upload-artifact@v4
  with:
    name: workspace
    path: .            # ← uploads .git/, including .git/config with the token
```

| scanner            | verdict                                                              |
| :----------------- | :------------------------------------------------------------------- |
| **pipeline-check** | ✅&nbsp;_Both halves: checkout persists `GITHUB_TOKEN` + artifact path includes `.git`_ |
| zizmor             | ✅&nbsp;`artipacked` audit (named after the original disclosure)     |
| poutine            | ⚠️&nbsp;Flags the checkout default but not the artifact-path side    |
| KICS               | ❌                                                                   |
| Checkov            | ❌                                                                   |
| Trivy              | ❌                                                                   |
| Gitleaks           | ❌&nbsp;_(token isn't in source — only in the artifact)_             |

---

### ④ The silent default: `persist-credentials` &nbsp;·&nbsp; scenario 12

> [!NOTE]
> **CICD-SEC-6 · Insufficient Credential Hygiene.** Same root cause as #③,
> but without the artifact step. `actions/checkout` *defaults* to writing the
> token. Any later untrusted step in the same job can read it.

```yaml
# .github/workflows/scenario-12-persist-credentials-leak.yml
- uses: actions/checkout@v4
  # ← no persist-credentials: false; GITHUB_TOKEN now in .git/config
- uses: third-party-org/some-build-action@main
```

| scanner            | verdict | rule fired                                              |
| :----------------- | :-----: | :------------------------------------------------------ |
| **pipeline-check** |   ✅    | `actions/checkout persists GITHUB_TOKEN into .git/config` |
| zizmor             |   ✅    | `artipacked`                                            |
| poutine            |   ✅    | `unverified_script_execution`                           |
| KICS               |   ✅    | _Token Persistence in Checkout_                         |
| Checkov            |   ❌    | —                                                       |
| Trivy              |   ❌    | —                                                       |
| Gitleaks           |   —     | _(secret scanner)_                                      |

---

### ⑤ Codecov-2021-style trusted installer &nbsp;·&nbsp; scenario 19

> [!NOTE]
> **CICD-SEC-3 + CICD-SEC-9 · April 2021.** Codecov's bash uploader was
> modified *before* their signing pipeline ran. ~29,000 customers verified
> the signature, the checksum matched, the binary was backdoored.
> Trust didn't move — the upstream's CI did.

```yaml
# .github/workflows/scenario-19-codecov-style-installer.yml
curl ... -o codecov                                # binary
curl ... -o codecov.sha256                          # checksum
curl ... -o codecov.sha256.sig                      # signature
gpg --verify codecov.sha256.sig codecov.sha256      # ← passes
sha256sum --check codecov.sha256                     # ← passes
./codecov                  # ← runs the malicious build that was signed by a legit key
```

| scanner            | verdict                                                              |
| :----------------- | :------------------------------------------------------------------- |
| **pipeline-check** | ✅&nbsp;_External binary install + missing artifact provenance + curl install_ |
| zizmor             | ⚠️&nbsp;`unverified-script-download` partial — checks for unverified, not over-verified |
| poutine            | ❌                                                                   |
| KICS               | ❌                                                                   |
| Checkov            | ❌                                                                   |
| Trivy              | ❌                                                                   |
| Gitleaks           | —                                                                    |

> Signing-and-verify *feels* responsible, but trusting "any signature from
> this key" means trusting the publisher's own CI. Pin to a known-good
> release digest, or you're SLSA-Build-L1 with extra ceremony.

---

### ⑥ Bonus rules the field doesn't ship yet

Pipeline-check also flags supply-chain hygiene requirements no other
scanner in this comparison currently surfaces. Real findings from the
scenario files, verbatim from the engine:

```
✕ Artifacts not signed (no cosign/sigstore step)
✕ SBOM not produced (no CycloneDX/syft/Trivy-SBOM step)
✕ No SLSA provenance attestation produced
✕ No vulnerability scanning step
✕ Deploy job missing environment binding
✕ Job has no `timeout-minutes`, unbounded build
✕ services / container image is not pinned by digest
```

These fire on scenarios 01, 03, 09, 10, 13, 17, 19, and 22 — and are the
reason pipeline-check's *per-scenario rule fire count* is roughly 3× the
next-closest scanner once duplicates are normalized away.

---

## The full matrix

| key | meaning                                  |
| :-: | :--------------------------------------- |
| ✅  | scanner flags the canonical bug          |
| ⚠️  | scanner partially catches (subset of the antipattern, or via a generic rule) |
| ❌  | scanner misses                           |
| —   | not applicable to that scanner's class   |

| #  | Scenario                                          | pipeline&#x2011;check | zizmor | poutine | KICS | Checkov | Trivy | Gitleaks |
| :-:| :------------------------------------------------ | :-------------------: | :----: | :-----: | :--: | :-----: | :---: | :------: |
| 01 | `pull_request_target` + fork-head checkout        |          ✅          |   ✅   |   ✅    |  ❌  |   ❌   |  ❌   |    —     |
| 02 | Script injection via issue title                  |          ✅          |   ✅   |   ✅    |  ✅  |   ✅   |  ❌   |    —     |
| 03 | Action pinned to mutable ref                      |          ✅          |   ✅   |   ✅    |  ✅  |   ❌   |  ❌   |    —     |
| 04 | `GITHUB_TOKEN: write-all`                         |          ✅          |   ✅   |   ❌    |  ❌  |   ✅   |  ❌   |    —     |
| 05 | Cache poisoning via PR title                      |          ✅          |   ✅   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 06 | Reusable workflow `secrets: inherit`              |          ✅          |   ✅   |   ⚠️    |  ❌  |   ❌   |  ❌   |    —     |
| 07 | `workflow_run` artifact RCE                       |          ✅          |   ✅   |   ✅    |  ❌  |   ❌   |  ❌   |    —     |
| 08 | Self-hosted runner on public repo                 |          ✅          |   ✅   |   ✅    |  ❌  |   ❌   |  ❌   |    —     |
| 09 | Container image `:latest`                         |          ✅          |   ⚠️   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 10 | AWS OIDC wildcard `sub`                           |          ✅          |   ⚠️   |   ❌    |  ✅  |   ⚠️   |  ⚠️   |    —     |
| 11 | `pip install` no hashes                           |          ⚠️          |   —    |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 12 | `persist-credentials` leak                        |          ✅          |   ✅   |   ✅    |  ✅  |   ❌   |  ❌   |    —     |
| 13 | `workflow_dispatch` input injection               |          ✅          |   ✅   |   ✅    |  ❌  |   ❌   |  ❌   |    —     |
| 14 | `$GITHUB_ENV` poisoning                           |          ⚠️          |   ⚠️   |   ⚠️    |  ❌  |   ❌   |  ❌   |    —     |
| 15 | Hardcoded secret in `env:`                        |          ✅          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    ✅    |
| 16 | `curl \| sh` install                              |          ⚠️          |   ⚠️   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 17 | ArtiPACKED — `.git/` in artifact                  |          ✅          |   ✅   |   ⚠️    |  ❌  |   ❌   |  ❌   |    ❌    |
| 18 | Composite action `${{ inputs.* }}` injection      |          ✅          |   ✅   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 19 | Codecov-style trusted-installer                   |          ✅          |   ⚠️   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 20 | Dependency confusion (Birsan)                     |          ⚠️          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 21 | Matrix expansion injection                        |          ⚠️          |   ⚠️   |   ⚠️    |  ❌  |   ❌   |  ❌   |    —     |
| 22 | GCP OIDC over-broad WIF                           |          ⚠️          |   ❌   |   ❌    |  ⚠️  |   ⚠️   |  ⚠️   |    —     |
| 23 | `github-actions[bot]` branch-protection bypass    |          ✅          |   ⚠️   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 24 | Third-party webhook exfiltration                  |          ✅          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 25 | Environment branch-pattern bypass                 |          ⚠️          |   ⚠️   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 26 | GitHub App token over-scope                       |          ✅          |   ⚠️   |   ❌    |  ❌  |   ❌   |  ❌   |    —     |
| 27 | Secret leak in workflow logs                      |          ⚠️          |   ❌   |   ❌    |  ❌  |   ❌   |  ❌   |    ⚠️    |
|    | **scenarios caught**                              |   **19 ✅ · 8 ⚠️**   | 12 ✅ · 9 ⚠️ | 7 ✅ · 4 ⚠️ | 4 ✅ · 1 ⚠️ | 2 ✅ · 1 ⚠️ | 1 ⚠️ | 1 ✅ · 1 ⚠️ |

> [!IMPORTANT]
> The totals reflect **scenario-level coverage**, not raw finding count.
> Some scanners emit multiple findings per scenario file; the cells record
> whether *at least one* relevant rule fired against the canonical bug
> in that scenario. Per-rule numbers and full SARIF live in the
> [`scanner-comparison`](../../actions/workflows/scanner-comparison.yml) workflow run summary
> and in `tools/comparison-report.py` output.

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
    │   pipeline-check ▸ zizmor ▸ poutine ▸ checkov           │
    │                        │                                │
    │                kics  ▸ trivy ▸  gitleaks                │
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
> `pipeline-check` is currently scored from its IDE diagnostics and
> CLI `--output json` runs. A dedicated SARIF-emitting job in
> `scanner-comparison.yml` is the next addition — see
> [Contributing](#contributing).

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
the SARIF output you got. Verdicts in the matrix track <i>scenario-level
coverage of the canonical bug</i>; if your scanner version fires a rule
that catches it cleanly, the cell flips.

</details>

---

## Why `pipeline-check` is in this comparison

This repo is the test range; [`pipeline-check`](https://github.com/greylag-ci/pipeline-check-vscode)
is one of the engines being tested — and the only one in the field that:

- Lints **22 CI/CD providers**, not just GitHub Actions: GitLab CI,
  Azure DevOps, Bitbucket Pipelines, CircleCI, Google Cloud Build,
  Buildkite, Drone CI, Jenkins (Declarative + Scripted), Dockerfile,
  plus Kubernetes / Helm / Terraform / CloudFormation / live AWS / SCM
  posture in roadmap releases.
- Maps every rule to **OWASP CICD-SEC top 10** + 14 other compliance
  frameworks (NIST 800-218 SSDF, SLSA, CIS Benchmarks, …).
- Carries **810+ rules**, including supply-chain hygiene rules (SBOM,
  SLSA provenance, artifact signing, vuln-scan presence) that the rest
  of the field doesn't surface yet.
- Renders findings **inline in VS Code** via LSP — gutter squiggles,
  hover with `--explain` prose, severity-graded status bar
  (e.g. `🛡 3C 1H`), keyboard nav, findings panel grouped by severity /
  file / rule.

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
