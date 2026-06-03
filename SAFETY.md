# Safety model

> **The whole point of this repository is that the patterns inside it
> are dangerous to copy.** Every workflow file under
> [`.github/workflows/scenario-*.yml`](.github/workflows) and
> [`_reusable-deploy.yml`](.github/workflows/_reusable-deploy.yml), plus
> the nested non-GHA pipeline fixtures under
> [`scenarios/NN-*/`](scenarios) (`.gitlab-ci.yml`, `Jenkinsfile`, …),
> demonstrates a real CI/CD attack pattern. The patterns must be
> visible to static scanners (that's the comparison target) but they
> must **never execute on a runner** — on this platform or any other a
> clone might be mirrored to.

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
  `if: false`. It accepts an optional positional path so a trusted,
  base-checked-out copy of the script can be pointed at a sandboxed
  copy of the PR head's workflows dir.
- [`.github/workflows/safety-check.yml`](.github/workflows/safety-check.yml)
  runs that script on every push, workflow_dispatch, and **fork or
  branch PR via `pull_request_target`**. The `pull_request_target`
  trigger uses the workflow file from `main`, not the PR head, so a
  PR cannot disable or modify the check by editing the safety-check
  workflow itself. The PR head is checked out into `./pr-head/` with
  `persist-credentials: false` and the script (from base) only parses
  YAML there — nothing from the PR is ever executed.
- Branch protection on `main` **must** require the
  `scenarios-are-gated` check before merging. Without that required
  check, the safety gate is advisory: a PR could land with `if: false`
  removed even though the check failed.

## Invariant 1b — non-GHA provider files are nested, never at a canonical path

The multi-provider scenarios (39+) ship pipeline files for platforms other
than GitHub Actions — `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/config.yml`,
`bitbucket-pipelines.yml`, and so on. GitHub Actions never runs these (it only
runs `.github/workflows/*`), so they are inert **here**. The residual risk is
a clone that gets **mirrored to that other platform**, where a file sitting at
the platform's canonical auto-run path (the repository root, `.circleci/`,
`.buildkite/`, …) would be auto-discovered and executed.

The invariant that neutralises this: **every non-GHA pipeline file lives nested
under `scenarios/NN-<slug>/`, never at a canonical auto-run path.** None of
these platforms auto-discover a pipeline file in an arbitrary subdirectory —
each runs only the one at its fixed location — so a nested copy is a static
fixture that scanners can read but no platform will ever run. As defense in
depth, providers that support an always-skip gate also carry one (e.g. GitLab
`workflow: rules: - when: never`), the cross-platform analogue of `if: false`.

The check is automated:

- [`tools/check-provider-files-safe.py`](tools/check-provider-files-safe.py)
  walks the tree and fails closed if any recognised non-GHA pipeline file
  appears outside `scenarios/`.
- [`.github/workflows/safety-check.yml`](.github/workflows/safety-check.yml)
  runs it alongside the `if: false` gate on every push and **fork/branch PR
  via `pull_request_target`** (from the base tree, so a PR can't disable it).
  As with invariant 1, the script only walks the filesystem and inspects
  names/paths — nothing from the PR is executed.

## Invariant 2 — only three workflows execute, with documented permissions

The repo has exactly **three** workflow files whose jobs are not gated:

- [`scanner-comparison.yml`](.github/workflows/scanner-comparison.yml)
  — runs the eight scanners against the static tree.
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

`scanner-comparison.yml` does not download any binaries outside of
pinned actions. `pipeline-check` is installed via `pip install
--require-hashes` against an inline SHA-256 of the wheel from PyPI;
every other scanner runs through a SHA-pinned official action. If a
future scanner addition needs a raw binary download, it must be
verified against an inline SHA-256 — the difference between the
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
- **A fork PR to this repo.** This case has two halves, because
  GitHub resolves the workflow file differently per trigger:
  - For `pull_request_target` (scenario 01 and `safety-check.yml`)
    the workflow body is taken from `main`. The PR cannot remove
    `if: false` or disable the safety gate by editing the file. ✓
  - For `pull_request` (scenarios 03-06, 08, 11-12, 14, 16, 19-21,
    24, plus `scanner-comparison.yml`) the workflow body is taken
    from the **PR head**. A malicious PR could in principle remove
    `if: false` from a scenario, and that scenario would then
    execute on the PR run. Blast radius is bounded by GitHub's
    fork-PR rules — the `GITHUB_TOKEN` is read-only and **no
    secrets are available to fork PRs** — so the worst case is
    arbitrary read-only code on a throwaway runner with no
    credentials. The merge itself is blocked by `safety-check`
    (which runs from base via `pull_request_target` and therefore
    *cannot* be disabled by the PR) plus the required-check branch
    protection on `main`.
- **A scheduled run.** Only `scanner-comparison.yml`,
  `safety-check.yml`, and `regen-readme.yml` execute on schedule;
  all three have minimum permissions and operate on the base tree.
- **An upstream compromise of a third-party action used by
  `scanner-comparison.yml`.** All third-party actions are pinned to
  commit SHAs; a malicious tag-move on
  `bridgecrewio/checkov-action`, `boostsecurityio/poutine-action`, or
  `checkmarx/kics-github-action` does not affect this repo until a
  maintainer deliberately updates the pin.

What this repo is **not** designed to be safe against:

- A maintainer who removes `if: false` from a scenario and merges it.
  `safety-check.yml` will fail closed on the PR — but it's only as
  strong as branch protection. The `scenarios-are-gated` check **must**
  be a required status check on `main`, and `enforce_admins` should be
  on. Without those, the invariant is advisory.
- A `terraform apply` or `aws iam create-role` of a fixture file.
  Those tools are explicitly out of scope: running them is a
  deliberate maintainer action, not an accidental side effect.

## Required GitHub settings

The code-side invariants above assume two repo-level settings are
configured. The static gates lose most of their value without them:

1. **Branch protection on `main`** with `scenarios-are-gated` listed
   as a required status check. The `safety-check` workflow only
   blocks a merge if this check is required; otherwise it's a green
   advisory that can be ignored.
2. **Settings → Actions → General → "Fork pull request workflows from
   outside collaborators"** set to **"Require approval for all
   outside collaborators"**. The default for public repos is "first-
   time contributors", which lets a returning fork contributor's PR
   auto-run the workflows in their PR head — bounded but unnecessary
   attack surface for a deliberately-vulnerable repo.

## Reporting a safety issue

If you find a way to make any scenario actually execute on a runner,
or if any of the invariants above is broken in this branch, open a
private security advisory rather than a public issue. The lineage and
contact path are documented in [`NOTICE`](NOTICE).
