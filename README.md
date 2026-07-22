> [!WARNING]
> Every workflow file in `.github/workflows/scenario-*.yml` is intentionally broken.
> Do not reuse the patterns. Do not enable Actions on a clone you forgot to read first.

<!-- AUTOGEN:badges -->
[![scanner-comparison](https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml/badge.svg)](https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml)
[![License Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-3a3a3a?style=flat-square)](LICENSE)
[![CICD-SEC top 10](https://img.shields.io/badge/owasp-CICD--SEC_10%2F10-9c2b2b?style=flat-square)](https://owasp.org/www-project-top-10-ci-cd-security-risks/)
[![scenarios 149](https://img.shields.io/badge/scenarios-149-1f6feb?style=flat-square)](scenarios/README.md)
[![providers 24](https://img.shields.io/badge/providers-24-1f6feb?style=flat-square)](docs/MATRIX.md)
[![scanners 9](https://img.shields.io/badge/scanners-9-1f6feb?style=flat-square)](docs/MATRIX.md)
<!-- /AUTOGEN:badges -->

---

> Every CI/CD scanner has blind spots. The only honest way to measure them
> is on a target where the bugs are catalogued in advance. This is that target.

One hundred and forty-nine vulnerable pipelines and IaC manifests, each demonstrating
one specific attack pattern drawn from named incident disclosures (tj-actions 2025, ArtiPACKED 2024,
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

**Scenarios 39+ extend the range to ten other providers** (with a couple of
later GitHub Actions additions, e.g. 89) — the same one-bug, one-writeup model
on the platforms where most pipelines actually live: GitLab CI,
Jenkins, Azure Pipelines, CircleCI, Bitbucket Pipelines, Tekton, Argo Workflows,
Drone CI, Buildkite, and Google Cloud Build. **Scenarios 94–104 push past the
pipeline file into the Infrastructure-as-Code the pipeline deploys** — Dockerfile,
Kubernetes manifests, Terraform, CloudFormation, and Helm — the artifacts a CI/CD
scanner increasingly has to read too. **Scenarios 105–113 fill the thinnest OWASP
categories** — the governance and visibility classes scanners rarely cover:
ungoverned 3rd-party services (CICD-SEC-8), insufficient flow control
(CICD-SEC-1), and insufficient logging/visibility (CICD-SEC-10). These all ship
as static fixtures nested under `scenarios/NN-*/` (never at a provider's auto-run
path), so they're readable by scanners but inert on every platform. Only the
scanners that parse a given provider score those rows — and several are all-miss
*next-gen targets* no scanner here catches yet. See the per-provider leaderboards
below.

**Scenarios 121–131 exercise newer rule classes on the platforms already in the
range** — prompt injection and `trust_remote_code` in AI/LLM-driven workflows,
IaC-apply / production-deploy on untrusted PRs (Bitbucket, Azure, GitLab),
disabled native scanners, build-parameter and `eval` command injection, and
Cloud Build compromise indicators. **Scenarios 132–149 push past the pipeline
into the package & supply-chain layer it depends on** — dependency-confusion and
build-time-execution manifests for PyPI, Maven, NuGet, Cargo, Go modules, and
Composer, plus OCI image / SLSA-attestation integrity and the Argo CD GitOps
control plane. Those eight families are read only by `pipeline-check`, so they
appear in their own *Package & supply-chain* leaderboard band.

## Leaderboard

Which scanner catches what, **per provider** — because most scanners only read
one provider's files. A scanner scores a catch only when it fires a rule naming
a scenario's *specific intended bug*, not just any finding on the file; `—`
means it can't parse that provider at all. Auto-generated from the latest
[`scanner-comparison`](../../actions/workflows/scanner-comparison.yml) run on
`main`. [How scoring works →](docs/FIELD-TEST.md)

<!-- AUTOGEN:leaderboard -->
### At a glance — scanners × providers

Full catches per provider (`caught/total`; `—` = the scanner can't parse that provider's files), grouped into bands. Ranked by total catches across the corpus. Expand the section below for the ranked per-provider tables, or see the [full per-scenario matrix](docs/MATRIX.md).

**CI/CD pipelines**

| Scanner | GHA | GitLab | Azure | CircleCI | Bitbucket | Jenkins | Tekton | Argo | Drone | Buildkite | CloudBuild |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| pipeline&#x2011;check | 44/45 | 16/16 | 8/8 | 6/7 | 9/9 | 6/7 | 4/4 | 5/5 | 4/4 | 3/3 | 3/3 |
| Checkov | 10/45 | 0/16 | 0/8 | 1/7 | 1/9 | — | — | 2/5 | — | — | — |
| KICS | 8/45 | — | — | — | — | — | — | — | — | — | — |
| zizmor | 17/45 | — | — | — | — | — | — | — | — | — | — |
| poutine | 14/45 | — | — | — | — | — | — | — | — | — | — |
| octoscan | 13/45 | — | — | — | — | — | — | — | — | — | — |
| ciguard | — | 10/16 | — | — | — | 1/7 | — | — | — | — | — |
| actionlint | 6/45 | — | — | — | — | — | — | — | — | — | — |

**IaC / manifests**

| Scanner | Docker | K8s | TF | CFN | Helm |
| :--- | :---: | :---: | :---: | :---: | :---: |
| pipeline&#x2011;check | 3/3 | 3/3 | — | — | 3/3 |
| Checkov | 2/3 | 2/3 | 7/7 | 4/4 | 2/3 |
| KICS | 2/3 | 2/3 | 7/7 | 4/4 | — |
| Trivy | 3/3 | 3/3 | 6/7 | 3/4 | 3/3 |

**Package & supply-chain**

| Scanner | PyPI | Maven | NuGet | Cargo | Go | Composer | OCI | ArgoCD |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| pipeline&#x2011;check | 3/3 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 3/3 |

<details>
<summary><strong>Per-provider leaderboards</strong> — 24 ranked tables</summary>

#### GitHub Actions — 45 scenarios

| Scanner | Scenarios caught (of 45) |
| :--- | :--- |
| pipeline&#x2011;check | **44 ✅** |
| zizmor | **17 ✅** |
| poutine | **14 ✅** |
| octoscan | **13 ✅** |
| Checkov | **10 ✅** |
| KICS | **8 ✅** |
| actionlint | **6 ✅** |

#### GitLab CI — 16 scenarios

| Scanner | Scenarios caught (of 16) |
| :--- | :--- |
| pipeline&#x2011;check | **16 ✅** |
| ciguard | **10 ✅** |
| Checkov | **0 ✅** |

#### Azure Pipelines — 8 scenarios

| Scanner | Scenarios caught (of 8) |
| :--- | :--- |
| pipeline&#x2011;check | **8 ✅** |
| Checkov | **0 ✅** |

#### CircleCI — 7 scenarios

| Scanner | Scenarios caught (of 7) |
| :--- | :--- |
| pipeline&#x2011;check | **6 ✅** |
| Checkov | **1 ✅** |

#### Bitbucket Pipelines — 9 scenarios

| Scanner | Scenarios caught (of 9) |
| :--- | :--- |
| pipeline&#x2011;check | **9 ✅** |
| Checkov | **1 ✅** |

#### Jenkins — 7 scenarios

| Scanner | Scenarios caught (of 7) |
| :--- | :--- |
| pipeline&#x2011;check | **6 ✅** |
| ciguard | **1 ✅** |

#### Tekton — 4 scenarios

| Scanner | Scenarios caught (of 4) |
| :--- | :--- |
| pipeline&#x2011;check | **4 ✅** |

#### Argo Workflows — 5 scenarios

| Scanner | Scenarios caught (of 5) |
| :--- | :--- |
| pipeline&#x2011;check | **5 ✅** |
| Checkov | **2 ✅** |

#### Drone CI — 4 scenarios

| Scanner | Scenarios caught (of 4) |
| :--- | :--- |
| pipeline&#x2011;check | **4 ✅** |

#### Buildkite — 3 scenarios

| Scanner | Scenarios caught (of 3) |
| :--- | :--- |
| pipeline&#x2011;check | **3 ✅** |

#### Cloud Build — 3 scenarios

| Scanner | Scenarios caught (of 3) |
| :--- | :--- |
| pipeline&#x2011;check | **3 ✅** |

#### Dockerfile — 3 scenarios

| Scanner | Scenarios caught (of 3) |
| :--- | :--- |
| pipeline&#x2011;check | **3 ✅** |
| Trivy | **3 ✅** |
| KICS | **2 ✅** |
| Checkov | **2 ✅** |

#### Kubernetes — 3 scenarios

| Scanner | Scenarios caught (of 3) |
| :--- | :--- |
| pipeline&#x2011;check | **3 ✅** |
| Trivy | **3 ✅** |
| KICS | **2 ✅** |
| Checkov | **2 ✅** |

#### Terraform — 7 scenarios

| Scanner | Scenarios caught (of 7) |
| :--- | :--- |
| KICS | **7 ✅** |
| Checkov | **7 ✅** |
| Trivy | **6 ✅** |

#### CloudFormation — 4 scenarios

| Scanner | Scenarios caught (of 4) |
| :--- | :--- |
| KICS | **4 ✅** |
| Checkov | **4 ✅** |
| Trivy | **3 ✅** |

#### Helm — 3 scenarios

| Scanner | Scenarios caught (of 3) |
| :--- | :--- |
| pipeline&#x2011;check | **3 ✅** |
| Trivy | **3 ✅** |
| Checkov | **2 ✅** |

#### PyPI — 3 scenarios

| Scanner | Scenarios caught (of 3) |
| :--- | :--- |
| pipeline&#x2011;check | **3 ✅** |

#### Maven — 2 scenarios

| Scanner | Scenarios caught (of 2) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |

#### NuGet — 2 scenarios

| Scanner | Scenarios caught (of 2) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |

#### Cargo — 2 scenarios

| Scanner | Scenarios caught (of 2) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |

#### Go modules — 2 scenarios

| Scanner | Scenarios caught (of 2) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |

#### Composer — 2 scenarios

| Scanner | Scenarios caught (of 2) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |

#### OCI / SLSA — 2 scenarios

| Scanner | Scenarios caught (of 2) |
| :--- | :--- |
| pipeline&#x2011;check | **2 ✅** |

#### Argo CD — 3 scenarios

| Scanner | Scenarios caught (of 3) |
| :--- | :--- |
| pipeline&#x2011;check | **3 ✅** |

</details>
<!-- /AUTOGEN:leaderboard -->

→ **[Full per-scenario matrix](docs/MATRIX.md)**  ·
**[Coverage axes — by CICD-SEC, severity, solo catches](docs/COVERAGE-AXES.md)**  ·
**[Per-rule firing detail](docs/RULE-FIRINGS.md)**  ·
**[Walkthroughs of five hand-picked scenarios](docs/FIELD-TEST.md)**

> [!NOTE]
> **Corpus scope.** Scenarios 01–38 (and 89) are GitHub Actions; 39–93 are the
> multi-provider expansion (GitLab CI, Jenkins, Azure Pipelines, CircleCI,
> Bitbucket Pipelines, Tekton, Argo, Drone, Buildkite, Cloud Build); 94–104 are
> the IaC/manifest layer the pipeline deploys (Dockerfile, Kubernetes, Terraform,
> CloudFormation, Helm); 105–113 fill the thinnest OWASP categories (ungoverned
> 3rd-party services, flow control, logging/visibility) across GHA, GitLab, and
> Terraform; 114–120 grow the thinnest IaC formats (CloudFormation, Helm,
> Terraform); 121–131 add newer rule classes on the existing platforms (AI/LLM
> prompt injection + `trust_remote_code`, IaC-apply / prod-deploy on untrusted
> PRs, disabled scanners, `params`/`eval` injection, Cloud Build compromise
> indicators); 132–149 open the package & supply-chain layer (PyPI, Maven,
> NuGet, Cargo, Go modules, Composer, OCI/SLSA, Argo CD). Each scenario
> is scored only by the scanners that actually parse its provider — a
> GHA-only scanner (zizmor, KICS, actionlint, octoscan) shows `—`
> (not-applicable), never a miss, on a GitLab or Jenkins row it was never
> built to read; that's why the leaderboards are ranked per provider. **Trivy**
> (added as the 9th scanner) is the dedicated IaC/container misconfiguration
> tool — it renders Helm charts and parses Dockerfile/Kubernetes/Terraform/
> CloudFormation, so the IaC rows are now scored by up to four tools (Trivy +
> Checkov + KICS + pipeline-check); it doesn't read CI pipeline YAML, so it
> shows `—` on the GHA/GitLab/… rows. The eight **package & supply-chain**
> families (132–149) are read only by `pipeline-check`, so those rows are
> pipeline-check-solo and render in their own leaderboard band.

## What's in this repo

- **[Scenarios](scenarios/README.md)** — 149 vulnerable pipelines, IaC
  manifests, and package/supply-chain artifacts across 24 providers/formats
  (45 GitHub Actions + 16 GitLab CI + 8 Azure + 7 CircleCI + 9 Bitbucket +
  7 Jenkins + 4 Tekton + 5 Argo + 4 Drone + 3 Buildkite + 3 Cloud Build +
  3 Dockerfile + 3 Kubernetes + 7 Terraform + 4 CloudFormation + 3 Helm +
  3 PyPI + 2 Maven + 2 NuGet + 2 Cargo + 2 Go modules + 2 Composer +
  2 OCI/SLSA + 3 Argo CD), each with its own writeup (exploitation walkthrough,
  per-scanner coverage, the fix). Indexed by attack class and CICD-SEC category.
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
    │      ▸ actionlint ▸ octoscan ▸ ciguard ▸ trivy          │
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
CI/CD providers, manifest types, and package ecosystems beyond GitHub
Actions — twenty-three of which this range now exercises (GitLab, Azure,
CircleCI, Bitbucket, Jenkins, Tekton, Argo, Drone, Buildkite, Cloud Build;
Dockerfile, Kubernetes, Helm; and the package & supply-chain layer no other
scanner here reads at all — PyPI, Maven, NuGet, Cargo, Go modules, Composer,
OCI/SLSA attestations, and the Argo CD GitOps control plane). It also added an
AI/LLM rule pack (prompt injection into agentic CLIs, `trust_remote_code`
model-load RCE) that this range now exercises too.
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
