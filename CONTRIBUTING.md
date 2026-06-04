# Contributing

## Add a scanner

One new job in
[`.github/workflows/scanner-comparison.yml`](.github/workflows/scanner-comparison.yml).
Three steps:

1. Install the binary (release tarball, `pip install`, `cargo install`…).
   Pin the version — the file's safety model is "everything pinned to
   an immutable artifact." Tools without a checksums file (octoscan,
   for example) get a manually-computed SHA-256.
2. Run it with SARIF output.
3. Upload via `github/codeql-action/upload-sarif` (SHA-pinned, see
   existing jobs in `scanner-comparison.yml`) under a unique
   `category:` so the Code Scanning tab can split it from the others.

Then add a column to **The full matrix** by registering the scanner in
[`tools/scenarios.yaml`](tools/scenarios.yaml) (`scanners:` list — `id`,
`sarif_tool`, `label`, and **`providers`**: the list of CI/CD providers it
can statically scan) and the next `regen-readme.py` run picks it up. The
`providers` list is what decides which per-provider leaderboard the scanner
appears in; on a scenario whose `provider` isn't in the list the scanner
auto-renders `—` (not-applicable) and is excluded from its denominator.

### Gotchas seen so far

The existing scanner jobs in
[`scanner-comparison.yml`](.github/workflows/scanner-comparison.yml)
each carry a comment explaining the integration quirks worth knowing
before adding the next scanner:

- **No native SARIF.** Some scanners (e.g. actionlint) only emit JSON
  or text. Wrap with a small converter — see
  [`tools/actionlint-to-sarif.py`](tools/actionlint-to-sarif.py) — and
  confirm the converter handles the scanner's actual key casing (the
  actionlint converter originally read PascalCase keys; actionlint
  marshals lowercase per its Go json tags).
- **Target-path semantics differ.** octoscan's `scan <dir>` does
  `WalkDir(<dir>)` looking for `<subdir>/.github/workflows/`, so you
  pass repo root (`.`), not the workflows dir. Other scanners take
  the workflows dir directly. Read each tool's `--help` rather than
  copying the previous job's invocation verbatim.
- **Third-party action wrappers are brittle.** The
  `checkmarx/kics-github-action` wrapper depended on Chainguard's
  `wolfi-base:latest` registry image, which broke our pipeline when
  upstream went down. The KICS job now invokes
  `checkmarx/kics:v2.1.20` directly via `docker run` — no wrapper.
  Prefer direct invocation when the wrapper only adds GHA-specific
  annotation formatting you don't consume.
- **SARIF schema strictness.** GitHub Code Scanning rejects SARIF
  with duplicate `taxonomies[*].taxa` entries (we hit this with KICS;
  the workaround is a `jq '… | unique'` pass before upload). Test
  the upload step end-to-end — a valid-looking SARIF file is not the
  same as one Code Scanning will accept.
- **Exit-code conventions.** Most scanners exit non-zero when they
  find issues. Default GHA shell is `bash -e`, so `script: scanner`
  alone aborts the step. Use `… > out.sarif || true` (zizmor / KICS
  pattern) or `… || [ $? -eq 1 ]` (pipeline-check pattern) — but be
  aware the `|| [ $? -eq 1 ]` form has subtle interactions with
  `set -e` on multi-line scripts that bit us on the actionlint job.
- **Basename-only SARIF URIs.** A scanner's SARIF
  `artifactLocation.uri` must contain the scanned file's path for the
  matrix to attribute the finding (`SCENARIO_RE` keys on `scenario-NN-`
  / `scenarios/NN-`). ciguard's native SARIF writes only the *basename*
  (`.gitlab-ci.yml`), so every finding would land unattributed. The fix
  is [`tools/ciguard-scan-tree.py`](tools/ciguard-scan-tree.py): it runs
  ciguard per file and rewrites each URI to the real nested path before
  merging — the ciguard analogue of `actionlint-to-sarif.py`. Check a
  new scanner's URIs before trusting its matrix column.
- **Parser strictness vs. the `if: false` gate.** ciguard's pydantic
  `Job.if` model rejects a YAML boolean `if: false` (it wants a string),
  so it can't parse this repo's gated GHA workflows at all. Rather than
  re-quote the safety gate on 38 files for one scanner, ciguard's
  `providers` list simply omits `github`. When a scanner can't read a
  provider's files *as this corpus writes them*, drop that provider from
  its `providers` rather than bending the fixtures.

## Add a scenario for another provider (GitLab, Jenkins, …)

Same as a GHA scenario, with three differences driven by the safety model
([SAFETY.md invariant 1b](SAFETY.md#invariant-1b--non-gha-provider-files-are-nested-never-at-a-canonical-path)):

1. **Put the pipeline file *inside* the scenario dir**, at the provider's
   conventional name but nested — e.g. `scenarios/NN-<slug>/.gitlab-ci.yml`,
   `scenarios/NN-<slug>/Jenkinsfile`, `scenarios/NN-<slug>/.circleci/config.yml`.
   Never at the repo root / `.circleci/` / etc.; `check-provider-files-safe.py`
   fails the build if you do. Add a provider-appropriate always-skip gate
   where one exists (GitLab `workflow: rules: - when: never`) plus a loud
   header comment.
2. **Set `provider:`** on the scenarios.yaml row (e.g. `provider: gitlab`),
   and only fill `expected:` for scanners whose `providers` list includes
   that provider — the rest resolve to `—` automatically.
3. **Reconcile rule IDs against real SARIF.** Author your best guess, then
   after the first `scanner-comparison` run inspect
   [`docs/RULE-FIRINGS.md`](docs/RULE-FIRINGS.md) and run
   `regen-readme.py --verify` to confirm the rules you claimed actually fire.

## Add a scenario

1. `.github/workflows/scenario-NN-<name>.yml` — vulnerable pattern in a
   real-looking workflow file, every job gated with `if: false` so the
   workflow shows up in run history but no runner is ever assigned.
2. `scenarios/NN-<name>/README.md` — pattern, exploitation walkthrough,
   expected per-scanner coverage, and the fix.
3. Add a new entry to [`tools/scenarios.yaml`](tools/scenarios.yaml) —
   this is the source of truth. Include the `id`, `slug`, `title`,
   `cicd_sec` categories, `severity`, and an `expected` list per
   scanner (a list of rule IDs each scanner *should* fire, or `[]` if
   none are expected, or `na` if not applicable to that scanner's
   class). See the schema comment at the top of the file.
4. Run `python tools/regen-readme.py --sarif-dir ./sarif` locally to
   re-render the README leaderboard, the docs/MATRIX.md matrix, the
   scenarios index, and the badges between the `<!-- AUTOGEN:* -->`
   markers. Then `python tools/regen-readme.py --verify --sarif-dir
   ./sarif` to confirm scenarios.yaml's `expected` rules actually fire
   in SARIF.
5. The [`scenarios/README.md`](scenarios/README.md) per-category index
   is hand-maintained — add a row there if your new scenario covers a
   CICD-SEC category not yet represented.

## Disagree with a verdict?

Open an issue with the scenario number, the scanner, the version, and
the SARIF output you got. Verdicts in the matrix track *canonical-bug
coverage*, not raw finding count; if your scanner version fires a
rule whose description names the canonical bug for that scenario, the
cell flips.

## Regenerate the stats

The leaderboard (`README.md`), full matrix + scenarios-index
(`docs/MATRIX.md`), and badges (`README.md`) are auto-generated between
`<!-- AUTOGEN:* -->` markers. Source of truth is
[`tools/scenarios.yaml`](tools/scenarios.yaml) (one entry per scenario,
with the rule IDs each scanner is expected to fire on the canonical
bug).

To rebuild locally:

```bash
# pull SARIF from the most recent successful scanner-comparison run
mkdir -p sarif
run_id=$(gh run list --workflow scanner-comparison.yml \
    --branch main --status success --limit 1 \
    --json databaseId --jq '.[0].databaseId')
gh run download "$run_id" --dir sarif

# rewrite the marked sections in README.md + docs/MATRIX.md
pip install PyYAML
python tools/regen-readme.py --sarif-dir sarif

# (optional) verify scenarios.yaml against SARIF — non-zero on drift
python tools/regen-readme.py --verify --sarif-dir sarif
```

Or skip the manual `gh run download` and let the script fetch SARIF
itself from the latest successful run on `main`:

```bash
python tools/regen-readme.py --from-latest-run
```

CI does this automatically:
[`.github/workflows/regen-readme.yml`](.github/workflows/regen-readme.yml)
runs weekly (`cron: '23 7 * * 1'`) and on `workflow_dispatch`, and
opens a PR titled _"auto: regen README stats"_ whenever the regenerated
files differ from `main`.

## Bump the pinned `pipeline-check`

`scanner-comparison.yml` pins `pipeline-check` to an exact version + wheel
sha256. [`tools/bump-pipeline-check.py`](tools/bump-pipeline-check.py)
rewrites that pin (and only that pin) from PyPI:

```bash
python tools/bump-pipeline-check.py --check       # report; exit 10 if newer
python tools/bump-pipeline-check.py               # rewrite to the latest release
python tools/bump-pipeline-check.py --version X.Y.Z
```

CI runs it automatically:
[`.github/workflows/bump-pipeline-check.yml`](.github/workflows/bump-pipeline-check.yml)
polls PyPI weekly (also `workflow_dispatch`, or a `pipeline-check-release`
`repository_dispatch` fired by the upstream release) and opens a
`chore/bump-pipeline-check-X.Y.Z` PR when a newer release exists.

The script touches the pin only. It does **not** change `scenarios.yaml`
`expected:` lists, the grounding comments, or the per-scenario READMEs —
deciding whether a newly-firing rule is the canonical catch for a scenario
is a human call. After the pin merges, `scanner-comparison` + `regen-readme`
refresh the docs and the `--verify` drift report flags the scenarios worth
reclassifying.
