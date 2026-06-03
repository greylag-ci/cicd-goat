"""Run pipeline-check over each Tekton / Argo manifest under a tree, normalise
every finding's SARIF artifact URI to the real file path, and merge into one
SARIF document on stdout (or --output).

Why a wrapper (cf. tools/ciguard-scan-tree.py):

  * For Tekton and Argo, pipeline-check's discovery is single-manifest per
    `--tekton-path`/`--argo-path`, so a single invocation over `scenarios/`
    only scans one file. We invoke it per discovered manifest instead.
  * pipeline-check attaches some Tekton/Argo findings to a SYNTHETIC URI
    (`resource:///tekton`, `resource:///argo`) rather than the file path, so
    those findings can't be attributed to a scenario (regen-readme.py's
    SCENARIO_RE keys on `scenario-NN-` / `scenarios/NN-` in the URI). Because
    each invocation scans exactly one scenario's manifest, we rewrite every
    finding's URI to that manifest's path.

Manifests are discovered by content (the provider's `apiVersion` marker), so
the wrapper doesn't depend on file naming.

Usage:
  python tools/pipeline-check-resource-scan.py --output pc-resource.sarif scenarios
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

# provider -> (apiVersion marker substring, pipeline-check path flag)
PROVIDERS = {
    "tekton": ("tekton.dev/", "--tekton-path"),
    "argo":   ("argoproj.io/", "--argo-path"),
}
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", ".scanvenv"}


def discover(roots: list[str]) -> list[tuple[str, Path]]:
    """Return [(provider, file)] for every Tekton/Argo manifest under roots."""
    found: list[tuple[str, Path]] = []
    for root in roots:
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                if not name.endswith((".yml", ".yaml")):
                    continue
                f = Path(dirpath) / name
                try:
                    head = f.read_text(encoding="utf-8", errors="replace")[:4000]
                except OSError:
                    continue
                for prov, (marker, _flag) in PROVIDERS.items():
                    if marker in head:
                        found.append((prov, f))
                        break
    return sorted(set(found), key=lambda t: t[1].as_posix())


def scan_one(prov: str, f: Path, pc_cmd: str) -> list[dict]:
    """Run pipeline-check on one manifest; return its results with URIs rewritten."""
    flag = PROVIDERS[prov][1]
    proc = subprocess.run(
        [pc_cmd, "--pipeline", prov, flag, str(f.parent), "--output", "sarif"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
    )
    # pipeline-check exits 1 when findings are present; SARIF is still on stdout.
    if not proc.stdout.strip():
        print(f"warn: no pipeline-check output for {f} (exit {proc.returncode})",
              file=sys.stderr)
        return []
    try:
        doc = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        print(f"warn: bad pipeline-check SARIF for {f}: {e}", file=sys.stderr)
        return []
    uri = f.as_posix()
    rules: dict[str, dict] = {}
    results: list[dict] = []
    for run in doc.get("runs", []):
        for rule in (run.get("tool", {}).get("driver", {}) or {}).get("rules", []) or []:
            rid = rule.get("id")
            if rid:
                rules[rid] = rule
        for r in run.get("results", []) or []:
            for loc in r.get("locations", []) or []:
                phys = loc.setdefault("physicalLocation", {})
                phys.setdefault("artifactLocation", {})["uri"] = uri
            results.append(r)
    scan_one._rules.update(rules)  # type: ignore[attr-defined]
    return results


scan_one._rules = {}  # type: ignore[attr-defined]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("roots", nargs="*", default=["scenarios"],
                    help="directories to walk (default: scenarios)")
    ap.add_argument("--output", type=Path, help="write merged SARIF here (default: stdout)")
    ap.add_argument("--pc", default="pipeline_check",
                    help="pipeline-check console-script command (default: pipeline_check)")
    args = ap.parse_args()
    roots = args.roots or ["scenarios"]

    manifests = discover(roots)
    print(f"pipeline-check-resource-scan: {len(manifests)} Tekton/Argo manifest(s)",
          file=sys.stderr)
    results: list[dict] = []
    for prov, f in manifests:
        results.extend(scan_one(prov, f, args.pc))

    doc = {
        "version": "2.1.0",
        "$schema": "https://json.schemastore.org/sarif-2.1.0.json",
        "runs": [{
            "tool": {"driver": {"name": "pipeline_check",
                                "rules": list(scan_one._rules.values())}},  # type: ignore[attr-defined]
            "results": results,
        }],
    }
    text = json.dumps(doc, indent=2)
    if args.output:
        args.output.write_text(text, encoding="utf-8")
        print(f"wrote {args.output} ({len(results)} result(s))", file=sys.stderr)
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
