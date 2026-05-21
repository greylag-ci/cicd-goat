> [!WARNING]
> Every workflow file in `.github/workflows/scenario-*.yml` is intentionally broken.
> Do not reuse the patterns. Do not enable Actions on a clone you forgot to read first.

```
══════════════════════════════════════════════════════════════════════════════
   cicd-goat   ·   greylag-ci                                          v1.0
   ──────────────────────────────────────────────────────────────────────
   A test range for CI/CD security scanners.
   29 vulnerable GitHub Actions workflows.  5 scanners.  1 leaderboard.
══════════════════════════════════════════════════════════════════════════════
```

<!-- AUTOGEN:badges -->
[![scanner-comparison](https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml/badge.svg)](https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml)
[![License Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-3a3a3a?style=flat-square)](LICENSE)
[![CICD-SEC top 10](https://img.shields.io/badge/owasp-CICD--SEC_10%2F10-9c2b2b?style=flat-square)](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
[![scenarios 29](https://img.shields.io/badge/scenarios-29-1f6feb?style=flat-square)](scenarios/README.md)
[![scanners 5](https://img.shields.io/badge/scanners-5-1f6feb?style=flat-square)](docs/MATRIX.md)
<!-- /AUTOGEN:badges -->

---

> Every CI/CD scanner has blind spots. The only honest way to measure them
> is on a target where the bugs are catalogued in advance. This is that target.

Twenty-nine GitHub Actions workflows, each demonstrating one specific
attack pattern drawn from named incident disclosures (tj-actions 2025,
ArtiPACKED 2024, Codecov 2021, Birsan dependency confusion 2021,
event-stream/ua-parser-js/node-ipc/Shai-Hulud npm lifecycle abuse) and
the **OWASP Top 10 CI/CD Security Risks** — all ten categories covered.
Every job is gated with `if: false` so the workflows show up in run
history but never spawn a runner.

## Leaderboard

How many of the 29 scenarios each scanner catches. A scanner scores ✅ on
a scenario only when it fires a rule that names that scenario's *specific
intended bug* — not just any finding on the workflow file. Auto-generated
from the latest [`scanner-comparison`](../../actions/workflows/scanner-comparison.yml)
run on `main`. [How scoring works →](docs/FIELD-TEST.md)

<!-- AUTOGEN:leaderboard -->
| Scanner | Scenarios caught (of 29) |
| :--- | :--- |
| **pipeline&#x2011;check** | **15 ✅** · 1 ⚠️ |
| zizmor | **13 ✅** |
| poutine | **8 ✅** |
| KICS | **4 ✅** |
| Checkov | **4 ✅** |
<!-- /AUTOGEN:leaderboard -->

→ **[Full per-scenario matrix](docs/MATRIX.md)**  ·
**[Walkthroughs of five hand-picked scenarios](docs/FIELD-TEST.md)**

> [!NOTE]
> **Corpus scope.** All 29 scenarios are GitHub Actions workflows. Scanners
> whose primary design target is something else (container scanning,
> source-tree secret detection) aren't included here — they'd score 0/27
> on a corpus they were never built for. Trivy belongs in a container/IaC
> bench; Gitleaks in a source-secrets bench.

## What's in this repo

- **[Scenarios](scenarios/README.md)** — 27 vulnerable workflows, each
  with its own writeup (exploitation walkthrough, per-scanner coverage,
  the fix). Indexed by attack class and CICD-SEC category.
- **[Full matrix](docs/MATRIX.md)** — per-(scenario × scanner) verdict
  table, auto-rebuilt from real SARIF.
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
    │   pipeline-check ▸ zizmor ▸ poutine                     │
    │      ▸ kics ▸ checkov                                   │
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
corpus (narrow but real): catches one more scenario than the next-best
scanner (zizmor); ships a rule family that fires when a workflow is
*missing* a security control (SBOM, SLSA, artifact signing, vuln-scan,
`environment:` binding, `timeout-minutes`, container digest pinning)
— no other scanner here carries those rules at all; covers 22 CI/CD
providers and manifest types beyond GitHub Actions.
Inline VS Code experience via the
[Pipeline-Check extension](https://github.com/greylag-ci/pipeline-check-vscode);
the Python rule engine lives at
[`dmartinochoa/pipeline-check`](https://github.com/dmartinochoa/pipeline-check).

## License & lineage

Apache 2.0 — see [LICENSE](LICENSE). Soft fork of
[`cider-security-research/cicd-goat`](https://github.com/cider-security-research/cicd-goat);
all upstream content has since been removed, the project is now
standalone and focused on GitHub Actions. See [NOTICE](NOTICE) for the
full lineage.
