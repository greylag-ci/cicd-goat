> [!WARNING]
> Every workflow file in `.github/workflows/scenario-*.yml` is intentionally broken.
> Do not reuse the patterns. Do not enable Actions on a clone you forgot to read first.

<!-- AUTOGEN:badges -->
[![scanner-comparison](https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml/badge.svg)](https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml)
[![License Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-3a3a3a?style=flat-square)](LICENSE)
[![CICD-SEC top 10](https://img.shields.io/badge/owasp-CICD--SEC_10%2F10-9c2b2b?style=flat-square)](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
[![scenarios 82](https://img.shields.io/badge/scenarios-82-1f6feb?style=flat-square)](scenarios/README.md)
[![providers 11](https://img.shields.io/badge/providers-11-1f6feb?style=flat-square)](docs/MATRIX.md)
[![scanners 8](https://img.shields.io/badge/scanners-8-1f6feb?style=flat-square)](docs/MATRIX.md)
<!-- /AUTOGEN:badges -->

---

> Every CI/CD scanner has blind spots. The only honest way to measure them
> is on a target where the bugs are catalogued in advance. This is that target.

Eighty-two vulnerable pipelines, each demonstrating one specific attack pattern
drawn from named incident disclosures (tj-actions 2025, ArtiPACKED 2024,
Codecov 2021, Birsan dependency confusion 2021,
event-stream/ua-parser-js/node-ipc/Shai-Hulud npm lifecycle abuse,
Project Zero bug 2070, Synacktiv Dependabot exploitation) and the
**OWASP Top 10 CI/CD Security Risks** — all ten categories covered.
Scenarios 01–38 are GitHub Actions: 30–33 are variants of scenario 02 that
probe scanner untrusted-input list completeness across four `github.event.*`
contexts; 34–38 broaden the GHA corpus with unsecure-commands revival,
signed-but-not-bound `cosign verify`, cross-job environment-secret leak,
confused-deputy auto-merge, and recursive submodule checkout from PR. Every
GHA job is gated with `if: false` so the workflows show up in run history but
never spawn a runner.

**Scenarios 39+ extend the range to ten other providers** — the same one-bug,
one-writeup model on the platforms where most pipelines actually live: GitLab CI,
Jenkins, Azure Pipelines, CircleCI, Bitbucket Pipelines, Tekton, Argo Workflows,
Drone CI, Buildkite, and Google Cloud Build. These ship as static fixtures
nested under `scenarios/NN-*/` (never at a provider's auto-run path), so they're
readable by scanners but inert on every platform. Only the scanners that parse a
given provider score those rows — and several are all-miss *next-gen targets* no
scanner here catches yet. See the per-provider leaderboards below.

## Leaderboard

How many scenarios each scanner catches, **ranked separately per provider** —
because most scanners only read one provider's files. A scanner scores ✅ on a
scenario only when it fires a rule that names that scenario's *specific
intended bug* — not just any finding on the file; it doesn't appear in a
provider's table at all if it can't parse that provider. Auto-generated from
the latest [`scanner-comparison`](../../actions/workflows/scanner-comparison.yml)
run on `main`. [How scoring works →](docs/FIELD-TEST.md)

<!-- AUTOGEN:leaderboard -->
### GitHub Actions — 38 scenarios

| Scanner | Scenarios caught (of 38) |
| :--- | :--- |
| pipeline&#x2011;check | **31 ✅** |
| zizmor | **16 ✅** |
| poutine | **12 ✅** |
| octoscan | **12 ✅** |
| Checkov | **9 ✅** |
| KICS | **7 ✅** |
| actionlint | **6 ✅** |

### GitLab CI — 9 scenarios

| Scanner | Scenarios caught (of 9) |
| :--- | :--- |
| pipeline&#x2011;check | **7 ✅** |
| ciguard | **7 ✅** |
| Checkov | **0 ✅** |

### Azure Pipelines — 6 scenarios

| Scanner | Scenarios caught (of 6) |
| :--- | :--- |
| pipeline&#x2011;check | **3 ✅** |
| Checkov | **0 ✅** |

### CircleCI — 6 scenarios

| Scanner | Scenarios caught (of 6) |
| :--- | :--- |
| pipeline&#x2011;check | **4 ✅** |
| Checkov | **1 ✅** |

### Bitbucket Pipelines — 6 scenarios

| Scanner | Scenarios caught (of 6) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |
| Checkov | **1 ✅** |

### Jenkins — 5 scenarios

| Scanner | Scenarios caught (of 5) |
| :--- | :--- |
| pipeline&#x2011;check | **4 ✅** |
| ciguard | **1 ✅** |

### Tekton — 3 scenarios

| Scanner | Scenarios caught (of 3) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |

### Argo Workflows — 3 scenarios

| Scanner | Scenarios caught (of 3) |
| :--- | :--- |
| pipeline&#x2011;check | **3 ✅** |
| Checkov | **2 ✅** |

### Drone CI — 2 scenarios

| Scanner | Scenarios caught (of 2) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |

### Buildkite — 2 scenarios

| Scanner | Scenarios caught (of 2) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |

### Cloud Build — 2 scenarios

| Scanner | Scenarios caught (of 2) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |
<!-- /AUTOGEN:leaderboard -->

→ **[Full per-scenario matrix](docs/MATRIX.md)**  ·
**[Coverage axes — by CICD-SEC, severity, solo catches](docs/COVERAGE-AXES.md)**  ·
**[Per-rule firing detail](docs/RULE-FIRINGS.md)**  ·
**[Walkthroughs of five hand-picked scenarios](docs/FIELD-TEST.md)**

> [!NOTE]
> **Corpus scope.** Scenarios 01–38 are GitHub Actions; 39+ are the
> multi-provider expansion (GitLab CI, Jenkins, Azure Pipelines, CircleCI,
> Bitbucket Pipelines, Tekton, Argo, Drone, Buildkite, Cloud Build). Each scenario
> is scored only by the scanners that actually parse its provider — a
> GHA-only scanner (zizmor, KICS, actionlint, octoscan) shows `—`
> (not-applicable), never a miss, on a GitLab or Jenkins row it was never
> built to read; that's why the leaderboards are ranked per provider. Scanners
> whose primary design target is something else entirely (container scanning,
> source-tree secret detection) still aren't included here — they'd score 0
> on a corpus they were never built for.

## What's in this repo

- **[Scenarios](scenarios/README.md)** — 82 vulnerable pipelines across 11
  providers (38 GitHub Actions + 9 GitLab CI + 6 Azure + 6 CircleCI +
  6 Bitbucket + 5 Jenkins + 3 Tekton + 3 Argo + 2 Drone + 2 Buildkite +
  2 Cloud Build), each with its own writeup
  (exploitation walkthrough, per-scanner coverage, the fix). Indexed by
  attack class and CICD-SEC category.
- **[Full matrix](docs/MATRIX.md)** — per-(scenario × scanner) verdict
  table, auto-rebuilt from real SARIF.
- **[Coverage axes](docs/COVERAGE-AXES.md)** — same verdicts sliced
  three different ways: by OWASP CICD-SEC category, by severity, and
  by solo catches (scenarios only one scanner sees).
- **[Per-rule firing detail](docs/RULE-FIRINGS.md)** — for each
  (scenario × scanner) pair, every rule the scanner actually emitted
  on that workflow. Canonical-bug rules **bolded**; everything else
  is noise or adjacent.
- **[Field test](docs/FIELD-TEST.md)** — five hand-picked scenarios
  with rule-by-rule commentary, including a section on rules that fire
  for *missing* security controls (SBOM, signing, etc.).
- **[Safety posture](SAFETY.md)** — how fork PRs and Actions
  permissions are hardened so this can't be turned into someone's runner.
- **[Contributing](CONTRIBUTING.md)** — add a scanner, add a scenario,
  regenerate the stats.

## How the comparison runs

```
                    push   /   pull_request
                              │
                              ▼
    ┌─────────────────────────────────────────────────────────┐
    │  .github/workflows/scanner-comparison.yml               │
    │                                                         │
    │   pipeline-check ▸ zizmor ▸ poutine ▸ kics ▸ checkov    │
    │      ▸ actionlint ▸ octoscan ▸ ciguard                  │
    │                        │                                │
    │                        ▼                                │
    │              upload SARIF                               │
    │       (one Code-Scanning category per tool)             │
    └────────────────────────┬────────────────────────────────┘
                             ▼
                Code Scanning  +  Run Summary
                             │
                             ▼
                tools/regen-readme.py  (reads SARIF)
                             │
                             ▼
                README leaderboard  +  docs/MATRIX.md
```

A weekly job — [`.github/workflows/regen-readme.yml`](.github/workflows/regen-readme.yml) —
pulls the latest SARIF, re-runs the leaderboard + matrix, and opens a PR
if anything moved. See
[CONTRIBUTING.md → Regenerate the stats](CONTRIBUTING.md#regenerate-the-stats).

## Why `pipeline-check` is in this comparison

This repo is the test range; [`pipeline-check`](https://github.com/greylag-ci/pipeline-check-vscode)
is one of the engines being tested. What it does differently on this
corpus (narrow but real): leads the leaderboard ahead of the next-best
scanner (zizmor); ships a rule family that fires when a workflow is
*missing* a security control (SBOM, SLSA, artifact signing, vuln-scan,
`environment:` binding, `timeout-minutes`, container digest pinning)
— no other scanner here carries those rules at all; and covers many more
CI/CD providers and manifest types beyond GitHub Actions — eleven of which
this range now exercises (GitLab, Azure, CircleCI, Bitbucket, Jenkins, Tekton,
Argo, Drone, Buildkite, Cloud Build).
Inline VS Code experience via the
[Pipeline-Check extension](https://github.com/greylag-ci/pipeline-check-vscode);
the Python rule engine lives at
[`dmartinochoa/pipeline-check`](https://github.com/dmartinochoa/pipeline-check).

## License & lineage

Apache 2.0 — see [LICENSE](LICENSE). Soft fork of
[`cider-security-research/cicd-goat`](https://github.com/cider-security-research/cicd-goat);
all upstream content has since been removed, the project is now
standalone — originally focused on GitHub Actions, now expanding across
CI/CD providers. See [NOTICE](NOTICE) for the full lineage.
