"""Run ciguard over every pipeline file it understands under the given roots,
normalise each finding's SARIF artifact URI to the file's real repo-relative
path, and merge everything into one SARIF document on stdout (or --output).

Why a wrapper (the ciguard analogue of tools/actionlint-to-sarif.py):

  * ciguard's native SARIF (`ciguard scan --format sarif`) is single-file and
    sets `artifactLocation.uri` to just the BASENAME (e.g. `.gitlab-ci.yml`),
    taken from `report.pipeline_name`. The cicd-goat matrix attributes a
    finding to a scenario by matching `scenario-NN-` / `scenarios/NN-` in the
    SARIF URI (tools/regen-readme.py SCENARIO_RE). A bare basename has no
    scenario number, so we rewrite the URI to the scanned file's path.
  * `ciguard scan-repo` discovers files recursively but only emits a JSON
    summary (no SARIF). So we do our own discovery + per-file SARIF + merge.

Usage:
  python tools/ciguard-scan-tree.py \
      --ciguard ciguard --output ciguard.sarif \
      .github/workflows scenarios
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# Pipeline files ciguard can scan in this corpus: GitLab CI and Jenkins
# declarative pipelines, all nested under scenarios/. (ciguard also has a
# GitHub Actions ruleset, but its pydantic Job.if model rejects the
# `if: false` boolean every GHA scenario here carries, so we don't point it
# at .github/workflows — see scenarios.yaml. The GHA_DIR detection below
# stays for completeness if a caller explicitly passes that root.)
GHA_DIR = ".github/workflows"
GITLAB_BASENAMES = {".gitlab-ci.yml", ".gitlab-ci.yaml"}
JENKINS_BASENAMES = {"Jenkinsfile"}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", ".scanvenv"}
DEFAULT_ROOTS = ["scenarios"]


def discover(roots: list[str]) -> list[Path]:
    found: list[Path] = []
    for root in roots:
        rp = Path(root)
        if not rp.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(rp):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            posix_dir = Path(dirpath).as_posix()
            for name in filenames:
                f = Path(dirpath) / name
                if name in GITLAB_BASENAMES or name in JENKINS_BASENAMES:
                    found.append(f)
                elif GHA_DIR in posix_dir and name.endswith((".yml", ".yaml")):
                    found.append(f)
    # stable, de-duplicated
    return sorted(set(found), key=lambda p: p.as_posix())


def scan_one(ciguard: str, f: Path) -> dict | None:
    """Run ciguard on one file; return its SARIF doc, or None on failure."""
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out.sarif"
        # Force UTF-8 in the child: ciguard prints box-drawing chars to stdout
        # and would crash a cp1252 pipe on Windows. No-op on Linux CI.
        env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
        proc = subprocess.run(
            [ciguard, "scan", "--input", str(f),
             "--format", "sarif", "--output", str(out), "--offline"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env=env,
        )
        # ciguard exits non-zero when findings cross --fail-on; that's fine —
        # we only care whether it produced a SARIF file.
        if not out.exists():
            print(f"warn: ciguard produced no SARIF for {f} "
                  f"(exit {proc.returncode})", file=sys.stderr)
            return None
        try:
            return json.loads(out.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"warn: bad ciguard SARIF for {f}: {e}", file=sys.stderr)
            return None


def merge(ciguard: str, files: list[Path]) -> dict:
    rules: dict[str, dict] = {}
    results: list[dict] = []
    for f in files:
        uri = f.as_posix()
        doc = scan_one(ciguard, f)
        if not doc:
            continue
        for run in doc.get("runs", []):
            for rule in (run.get("tool", {}).get("driver", {}) or {}).get("rules", []) or []:
                rid = rule.get("id")
                if rid and rid not in rules:
                    rules[rid] = rule
            for r in run.get("results", []) or []:
                # Rewrite every location URI to the real repo-relative path so
                # SCENARIO_RE can attribute the finding to its scenario.
                for loc in r.get("locations", []) or []:
                    phys = loc.setdefault("physicalLocation", {})
                    phys.setdefault("artifactLocation", {})["uri"] = uri
                results.append(r)
    return {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {
                "name": "ciguard",
                "rules": list(rules.values()),
            }},
            "results": results,
        }],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("roots", nargs="*", default=DEFAULT_ROOTS,
                    help="directories to walk (default: scenarios)")
    ap.add_argument("--ciguard", default="ciguard", help="ciguard executable")
    ap.add_argument("--output", type=Path, help="write merged SARIF here (default: stdout)")
    args = ap.parse_args()

    roots = args.roots or DEFAULT_ROOTS
    files = discover(roots)
    print(f"ciguard-scan-tree: {len(files)} pipeline file(s) under {roots}", file=sys.stderr)
    doc = merge(args.ciguard, files)
    text = json.dumps(doc, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output} ({len(doc['runs'][0]['results'])} result(s))", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
