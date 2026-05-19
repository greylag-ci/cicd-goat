# Safety model

> **The whole point of this repository is that the patterns inside it
> are dangerous to copy.** Every workflow file under
> [`.github/workflows/scenario-*.yml`](.github/workflows) and
> [`_reusable-deploy.yml`](.github/workflows/_reusable-deploy.yml)
> demonstrates a real CI/CD attack pattern. The patterns must be
> visible to static scanners (that's the comparison target) but they
> must **never execute on a runner.**

This document describes how that invariant is enforced.

## Invariant 1 — `if: false` on every scenario job

Every job in every `scenarios/.../*.yml` workflow has a top-level
`if: false`. GitHub Actions evaluates this expression **before runner
assignment**: the workflow appears in run history (so the static-analysis
purpose is preserved) but no runner is ever provisioned and no `run:`
step is ever executed.

The check is automated:

- [`tools/check-scenarios-gated.py`](tools/check-scenarios-gated.py)
  parses every scenario YAML and fails closed if any job is missing
  `if: false`.
- [`.github/workflows/safety-check.yml`](.github/workflows/safety-check.yml)
  runs that script on every push and PR. Branch-protection should
  require the `safety-check / scenarios-are-gated` check before
  merging.

## Invariant 2 — only three workflows execute, with documented permissions

The repo has exactly **three** workflow files whose jobs are not gated:

- [`scanner-comparison.yml`](.github/workflows/scanner-comparison.yml)
  — runs the seven scanners against the static tree.
  Permissions: `contents: read`, `security-events: write` (for SARIF
  upload). Read-only checkout (`persist-credentials: false`).
- [`safety-check.yml`](.github/workflows/safety-check.yml)
  — verifies invariant 1. Permissions: `contents: read`. Read-only
  checkout.
- [`regen-readme.yml`](.github/workflows/regen-readme.yml)
  — auto-regenerates the README stats from `tools/scenarios.yaml` +
  the latest scanner-comparison SARIF. Permissions: `contents: write`
  and `pull-requests: write` — **the broadest token in the repo.**
  This workflow needs write access because it pushes a new branch
  and opens a PR. The expanded permissions are justified because:
  - It triggers only on `workflow_dispatch` and weekly `schedule`,
    never on a fork PR or any attacker-controllable event.
  - It never pushes to `main` directly; it always opens a PR for
    human review.
  - Branch protection on `main` requires the `safety-check /
    scenarios-are-gated` check, so even a malicious commit landing
    via this PR path can't break invariant 1 without first failing
    the safety check.

All three workflows:

- Pin every action — including the official `actions/*` and
  `github/codeql-action/*` — to a **full 40-character commit SHA**,
  not a tag. The pin is the entire defence against the
  [`tj-actions/changed-files` 2025 compromise pattern](scenarios/03-action-mutable-ref/README.md)
  in our own scanner.
- Set `timeout-minutes:` on every job.
- The two read-only workflows set `actions/checkout` to
  `persist-credentials: false` (see
  [scenario 12](scenarios/12-persist-credentials-leak/README.md)).
  `regen-readme.yml` deliberately keeps the default
  `persist-credentials: true` because the job's last step pushes
  back via the auto-issued `GITHUB_TOKEN`; this is the *only* place
  in the repo where the persist-credentials default is on, and it is
  scoped to a single, manually-triggered workflow.

## Invariant 3 — every external binary is integrity-verified

The only binary fetched by `scanner-comparison.yml` outside of pinned
actions is `gitleaks`, downloaded from its GitHub release. The
download is verified against an inline SHA-256 before the binary is
made executable:

```yaml
env:
  GL_VERSION: 8.21.2
  GL_SHA256: 5bc41815076e6ed6ef8fbecc9d9b75bcae31f39029ceb55da08086315316e3ba
run: |
  set -euo pipefail
  curl -fsSL -o gitleaks.tgz ".../gitleaks_${GL_VERSION}_linux_x64.tar.gz"
  echo "${GL_SHA256}  gitleaks.tgz" | sha256sum -c -
  tar -xzf gitleaks.tgz gitleaks
  chmod +x gitleaks
```

The integrity check is the difference between the
[Scenario 19 / Codecov-2021](scenarios/19-codecov-style-installer/README.md)
failure mode and a safe install.

## Invariant 4 — auxiliary fixtures fail closed on accidental install

A few scenarios ship companion files (`package.json`, `requirements.txt`,
`.tf`, JSON) so static IaC scanners can find the bug outside the
workflow YAML:

- [`scenarios/20-dependency-confusion/package.json`](scenarios/20-dependency-confusion/package.json)
  references an internal-style scope that doesn't exist on public
  npm — but anyone could register it. A root-level `preinstall`
  script aborts `npm install` with a loud message **before** any
  dependency is fetched, so the dependency-confusion attack can't
  land on a developer who accidentally `cd`'d into the fixture
  directory.
- [`scenarios/11-pip-install-no-hashes/requirements.txt`](scenarios/11-pip-install-no-hashes/requirements.txt)
  lists real, public PyPI packages with unpinned floors. A
  `pip install -r` from that directory would install real (not
  malicious) versions, but accumulating that habit is exactly what
  the scenario warns against. The file is loudly commented as a
  vulnerable fixture and is only referenced from the scenario's
  workflow, which is `if: false`-gated.
- [`scenarios/22-gcp-oidc-broad-wif/workload-identity-pool.tf`](scenarios/22-gcp-oidc-broad-wif/workload-identity-pool.tf)
  and [`scenarios/10-oidc-aws-wildcard-sub/trust-policy.json`](scenarios/10-oidc-aws-wildcard-sub/trust-policy.json)
  are static IaC documents. They have no execution surface unless
  someone deliberately `terraform apply`s or AWS-CLI-attaches them.

## Threat model

What this repo is designed to be safe against:

- **A reader who clones the repo and runs `git push` / `gh pr create`
  from their own copy.** Every scenario workflow triggers, all jobs
  skip due to `if: false`, nothing executes.
- **A fork PR to this repo.** Workflows from the PR are loaded by
  GitHub but jobs are skipped (workflow body's `if: false` is evaluated
  in the base context). `scanner-comparison.yml` runs on the PR but
  with a read-only `GITHUB_TOKEN` and no secrets, so a malicious PR
  can at worst run a scanner against its own changes.
- **A scheduled run.** Same as above — only `scanner-comparison.yml`
  and `safety-check.yml` execute; both have minimum permissions.
- **An upstream compromise of a third-party action used by
  `scanner-comparison.yml`.** All third-party actions are pinned to
  commit SHAs; a malicious tag-move on
  `bridgecrewio/checkov-action`, `boostsecurityio/poutine-action`,
  `checkmarx/kics-github-action`, or `aquasecurity/trivy-action` does
  not affect this repo until a maintainer deliberately updates the
  pin.

What this repo is **not** designed to be safe against:

- A maintainer who removes `if: false` from a scenario and merges it.
  `safety-check.yml` will fail closed on the PR — but it's only as
  strong as branch protection. If branch protection is bypassed, the
  invariant breaks. Treat `safety-check / scenarios-are-gated` as a
  required check.
- A `terraform apply` or `aws iam create-role` of a fixture file.
  Those tools are explicitly out of scope: running them is a
  deliberate maintainer action, not an accidental side effect.

## Reporting a safety issue

If you find a way to make any scenario actually execute on a runner,
or if any of the invariants above is broken in this branch, open a
private security advisory rather than a public issue. The lineage and
contact path are documented in [`NOTICE`](NOTICE).
