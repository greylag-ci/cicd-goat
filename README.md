# cicd-goat (greylag-ci)

A deliberately-vulnerable GitHub Actions playground built for one purpose:
**comparing what different CI/CD security scanners find when pointed at
the same known-vulnerable target.**

Every scanner ships with a different rule set, a different default
sensitivity, and a different blind spot. The only honest way to compare
them is on a target where the bugs are catalogued in advance. This repo
is that target.

## What's in here

- **18 scenario workflows** at [`.github/workflows/scenario-NN-*.yml`](.github/workflows),
  each demonstrating one canonical GitHub Actions vulnerability. Every
  job is gated with `if: false` — the workflow shows up in run history,
  but no runner is ever assigned, so the scenarios serve only as
  static-analysis fodder.
- **Per-scenario writeups** at [`scenarios/`](scenarios/) covering the
  OWASP CICD-SEC mapping, exploitation walkthrough, expected per-scanner
  coverage, and the fix.
- **A scanner-comparison workflow** at
  [`.github/workflows/scanner-comparison.yml`](.github/workflows/scanner-comparison.yml)
  that runs six scanners on every push and uploads each result as a
  separate Code Scanning category.
- **A comparison report tool** at [`tools/comparison-report.py`](tools/comparison-report.py)
  that ingests the SARIF artifacts from a workflow run and produces a
  markdown matrix of which scanner flagged which scenario.

## Quickstart

1. Browse [`scenarios/`](scenarios/) to see the catalogued vulnerabilities.
2. Open the [Actions tab](../../actions/workflows/scanner-comparison.yml)
   and pick the latest `scanner-comparison` run. The job summary lists
   per-scanner finding counts.
3. Open the [Security → Code scanning](../../security/code-scanning) tab
   and filter by **Tool**. Each scanner uploads under its own category
   (`zizmor`, `poutine`, `checkov`, `kics`, `Trivy`, `Gitleaks`).
4. To produce a side-by-side comparison markdown, download the SARIF
   artifacts from a run and run:
   ```
   python tools/comparison-report.py <path-to-artifacts-dir>
   ```

## Scenarios

| #  | Scenario | CICD-SEC | Attack class |
|---:|---|---|---|
| 01 | [pull_request_target with fork-head checkout](scenarios/01-prtarget-checkout-head/README.md) | 4, 5 | Forky checkout RCE |
| 02 | [Script injection via issue title](scenarios/02-script-injection-issue-title/README.md) | 4 | Expression injection |
| 03 | [Action pinned to mutable ref](scenarios/03-action-mutable-ref/README.md) | 3 | Supply chain (tag move) |
| 04 | [GITHUB_TOKEN `write-all`](scenarios/04-github-token-write-all/README.md) | 5 | Excessive permissions |
| 05 | [Cache poisoning via PR title](scenarios/05-cache-poisoning-pr-controlled/README.md) | 4, 9 | Cross-job cache abuse |
| 06 | [Reusable workflow `secrets: inherit`](scenarios/06-reusable-secrets-inherit/README.md) | 5, 6 | Privilege passthrough |
| 07 | [workflow_run artifact RCE](scenarios/07-workflow-run-artifact-rce/README.md) | 4, 9 | Trigger context confusion |
| 08 | [Self-hosted runner on public repo](scenarios/08-self-hosted-public-fork/README.md) | 7 | Runner persistence |
| 09 | [Container image `:latest`](scenarios/09-container-image-latest/README.md) | 3, 9 | Mutable base image |
| 10 | [AWS OIDC wildcard subject](scenarios/10-oidc-aws-wildcard-sub/README.md) | 2, 7 | Federation misconfig |
| 11 | [pip install no hashes](scenarios/11-pip-install-no-hashes/README.md) | 3 | Dependency hijack |
| 12 | [checkout `persist-credentials` leak](scenarios/12-persist-credentials-leak/README.md) | 6, 3 | Token in `.git/config` |
| 13 | [workflow_dispatch input injection](scenarios/13-input-injection-workflow-dispatch/README.md) | 4 | Operator-trigger injection |
| 14 | [`$GITHUB_ENV` poisoning](scenarios/14-env-injection-pr-body/README.md) | 4 | Env-file injection |
| 15 | [Hardcoded secret in `env:`](scenarios/15-hardcoded-secret-env/README.md) | 6 | Secret in source |
| 16 | [`curl \| sh` toolcache poisoning](scenarios/16-curl-pipe-sh/README.md) | 3 | TOFU install script |
| 17 | [`upload-artifact` includes `.git/`](scenarios/17-artipacked-git-dir/README.md) | 6, 9 | Artifact-packed token |
| 18 | [Composite action `${{ inputs.* }}` injection](scenarios/18-composite-action-input-injection/README.md) | 4 | Composite expansion |

## Scanners under comparison

| Scanner   | Focus                              | Repo |
|-----------|------------------------------------|------|
| zizmor    | GHA static analysis (Rust)         | https://github.com/woodruffw/zizmor |
| poutine   | Pipeline supply-chain (Go)         | https://github.com/boostsecurityio/poutine |
| Checkov   | IaC + GHA (Python)                 | https://github.com/bridgecrewio/checkov |
| KICS      | IaC + GHA (Go)                     | https://github.com/Checkmarx/kics |
| Trivy     | Config / IaC / container (Go)      | https://github.com/aquasecurity/trivy |
| Gitleaks  | Secrets in source + history        | https://github.com/gitleaks/gitleaks |

Adding a scanner is a single job in
[`scanner-comparison.yml`](.github/workflows/scanner-comparison.yml):
install the binary, emit SARIF, upload under a unique `category:`.

## How to add a scenario

1. Drop a new `.github/workflows/scenario-NN-<name>.yml` with the
   vulnerable pattern, **every job gated with `if: false`** so the
   workflow never actually runs.
2. Add `scenarios/NN-<name>/README.md` covering: the pattern, real-world
   exploitation, expected per-scanner coverage, and the fix.
3. Add a row to the table above and the table in
   [`scenarios/README.md`](scenarios/README.md).

## License

Apache License 2.0 — see [`LICENSE`](LICENSE). Acknowledgements and
project lineage in [`NOTICE`](NOTICE).
