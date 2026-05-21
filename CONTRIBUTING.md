# Contributing

## Add a scanner

One new job in
[`.github/workflows/scanner-comparison.yml`](.github/workflows/scanner-comparison.yml).
Three steps:

1. Install the binary (release tarball, `pip install`, `cargo install`…).
2. Run it with SARIF output.
3. Upload via `github/codeql-action/upload-sarif` (SHA-pinned, see
   existing jobs in `scanner-comparison.yml`) under a unique
   `category:` so the Code Scanning tab can split it from the others.

Then add a column to **The full matrix** by registering the scanner in
[`tools/scenarios.yaml`](tools/scenarios.yaml) (`scanners:` list — `id`,
`sarif_tool`, `label`) and the next `regen-readme.py` run picks it up.

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
