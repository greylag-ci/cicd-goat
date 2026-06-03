"""Safety invariant 2: non-GitHub-Actions pipeline files must never sit at a
provider's canonical auto-run path.

Why: GitHub Actions only ever runs `.github/workflows/*`, so a `.gitlab-ci.yml`,
`Jenkinsfile`, `.circleci/config.yml`, `bitbucket-pipelines.yml`, etc. committed
to *this* GitHub repo is inert — no runner will ever pick it up. The real risk
is a clone that gets **mirrored to another platform** (GitLab, Bitbucket,
CircleCI, Drone, …), where a file sitting at that platform's canonical path
(repo root, `.circleci/`, `.buildkite/`, …) is auto-discovered and executed.

We neutralise that by keeping every non-GHA provider pipeline file **nested
under `scenarios/NN-<slug>/`**. None of these providers auto-discover pipeline
files in arbitrary subdirectories — they only run the one at their canonical
location — so a nested copy is a static fixture that scanners can read but no
platform will ever run. This script fails closed if any recognised non-GHA
pipeline file appears anywhere outside `scenarios/`.

GitHub Actions scenario workflows are the deliberate exception: they live in
`.github/workflows/scenario-*.yml` (GHA scanners need them there) and their
safety comes from the `if: false` gate enforced by check-scenarios-gated.py,
not from this check.

Wired into .github/workflows/safety-check.yml, which runs from the base tree on
every PR via pull_request_target so a PR can't disable it. The script only
walks the filesystem and inspects names/paths — it never executes anything.
"""
from __future__ import annotations

import os
import sys
import pathlib

# Non-GHA pipeline files keyed by the basename a platform auto-runs.
CANONICAL_BASENAMES = {
    ".gitlab-ci.yml":          "GitLab CI",
    ".gitlab-ci.yaml":         "GitLab CI",
    "bitbucket-pipelines.yml": "Bitbucket Pipelines",
    "azure-pipelines.yml":     "Azure Pipelines",
    "azure-pipelines.yaml":    "Azure Pipelines",
    "Jenkinsfile":             "Jenkins",
    ".drone.yml":              "Drone CI",
    ".drone.yaml":             "Drone CI",
    "cloudbuild.yaml":         "Cloud Build",
    "cloudbuild.yml":          "Cloud Build",
}
# Providers whose canonical file lives in a fixed subdirectory rather than at a
# fixed basename — matched on the relative posix path suffix.
CANONICAL_PATH_SUFFIXES = {
    ".circleci/config.yml":   "CircleCI",
    ".circleci/config.yaml":  "CircleCI",
    ".buildkite/pipeline.yml": "Buildkite",
    ".buildkite/pipeline.yaml": "Buildkite",
}

# Directories never worth descending into.
SKIP_DIRS = {".git", ".github", "node_modules", ".venv", "venv"}

NESTED_PREFIX = "scenarios/"


def find_violations(root: pathlib.Path) -> list[str]:
    """Return a list of error strings; empty list = tree is safe."""
    violations: list[str] = []
    root = root.resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        # prune skip dirs in-place
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            abs = pathlib.Path(dirpath) / name
            rel = abs.relative_to(root).as_posix()
            provider = CANONICAL_BASENAMES.get(name)
            if provider is None:
                for suffix, prov in CANONICAL_PATH_SUFFIXES.items():
                    if rel == suffix or rel.endswith("/" + suffix):
                        provider = prov
                        break
            if provider is None:
                continue
            if not rel.startswith(NESTED_PREFIX):
                violations.append(
                    f"{rel}: {provider} pipeline file at a canonical auto-run "
                    f"path. Move it under scenarios/NN-<slug>/ so no mirrored "
                    f"platform can auto-run it."
                )
    return violations


def main() -> int:
    # Optional positional arg = repo root to scan (the safety-check workflow
    # points this at the sandboxed PR-head checkout). Defaults to CWD.
    root = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] else pathlib.Path(".")
    if not root.is_dir():
        print(f"error: {root} does not exist", file=sys.stderr)
        return 2

    violations = find_violations(root)
    if violations:
        print("SAFETY INVARIANT BROKEN — non-GHA pipeline file(s) outside scenarios/:",
              file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        return 1

    print(f"OK: no non-GHA pipeline files at a canonical auto-run path under {root}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
