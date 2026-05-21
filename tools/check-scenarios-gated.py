"""Safety invariant: every job in every scenario-*.yml (and every
companion _reusable-*.yml) must have a top-level `if: false`.

Why: scenarios are deliberately vulnerable. The only thing that keeps
the patterns from actually executing is the job-level `if: false`.
If any scenario job lacks this gate, the bug it demonstrates could
actually fire on push / pull_request / pull_request_target / etc.

This script is also wired into .github/workflows/safety-check.yml,
which runs on every PR and fails closed if the invariant is broken.
"""
from __future__ import annotations

import sys
import pathlib
import yaml

DEFAULT_WORKFLOWS = pathlib.Path(".github/workflows")
SCENARIO_GLOB = "scenario-*.yml"
REUSABLE_GLOB = "_reusable-*.yml"


def check_file(path: pathlib.Path) -> list[str]:
    """Return list of error strings; empty list = file OK."""
    errors: list[str] = []
    text = path.read_text(encoding="utf-8")
    try:
        doc = yaml.safe_load(text)
    except yaml.YAMLError as e:
        return [f"{path}: invalid YAML: {e}"]

    if not isinstance(doc, dict):
        return [f"{path}: top-level is not a mapping"]

    jobs = doc.get("jobs", {})
    if not isinstance(jobs, dict) or not jobs:
        return [f"{path}: no `jobs:` block"]

    for job_id, job in jobs.items():
        if not isinstance(job, dict):
            errors.append(f"{path}: job `{job_id}` is not a mapping")
            continue
        if job.get("if") is not False and job.get("if") != "false":
            errors.append(
                f"{path}: job `{job_id}` is missing `if: false` "
                f"(got `if: {job.get('if')!r}`)"
            )
    return errors


def main() -> int:
    # Optional positional arg lets the safety-check workflow point the
    # script at a sandboxed copy of the PR head's workflows dir while
    # the script itself remains a trusted, base-checked-out file.
    if len(sys.argv) > 1 and sys.argv[1]:
        workflows = pathlib.Path(sys.argv[1])
    else:
        workflows = DEFAULT_WORKFLOWS

    if not workflows.is_dir():
        print(f"error: {workflows} does not exist", file=sys.stderr)
        return 2

    files = sorted(workflows.glob(SCENARIO_GLOB)) + sorted(workflows.glob(REUSABLE_GLOB))

    if not files:
        print(f"error: no scenario files under {workflows}", file=sys.stderr)
        return 2

    all_errors: list[str] = []
    for f in files:
        all_errors.extend(check_file(f))

    if all_errors:
        print("SAFETY INVARIANT BROKEN:", file=sys.stderr)
        for e in all_errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print(f"OK: every job in {len(files)} scenario file(s) is gated `if: false`.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
