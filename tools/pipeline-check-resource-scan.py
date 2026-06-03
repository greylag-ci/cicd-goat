"""Run pipeline-check over each non-pipeline manifest under a tree (Tekton,
Argo, Dockerfile, Kubernetes, Helm), normalise every finding's SARIF artifact
URI to the real file path, and merge into one SARIF document on stdout
(or --output).

Why a wrapper (cf. tools/ciguard-scan-tree.py):
  * pipeline-check's discovery for these manifest types is single-manifest per
    --<type>-path, so one invocation over scenarios/ only scans one file — we
    invoke it per discovered manifest instead.
  * It attaches some findings to a SYNTHETIC URI (`resource:///tekton`,
    `kubernetes/manifests`, …) rather than the file path, which can't be
    attributed to a scenario (regen-readme.py's SCENARIO_RE keys on
    `scenario-NN-` / `scenarios/NN-` in the URI). Each invocation scans exactly
    one scenario's manifest, so we rewrite every finding's URI to that file.

Terraform and CloudFormation are intentionally NOT handled here: pipeline-check's
Terraform provider needs a `terraform show -json` plan (not raw .tf), and its
CloudFormation ruleset is thin / non-attributable. Checkov + KICS cover those
raw manifests directly in CI.

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

# provider -> pipeline-check companion path flag
FLAG = {
    "tekton":     "--tekton-path",
    "argo":       "--argo-path",
    "dockerfile": "--dockerfile-path",
    "kubernetes": "--k8s-path",
    "helm":       "--helm-path",
}
# content markers for the YAML CI-native resource types (priority order)
YAML_MARKERS = [("tekton", "tekton.dev/"), ("argo", "argoproj.io/")]
K8S_KINDS = ("Pod", "Deployment", "DaemonSet", "StatefulSet", "Job", "CronJob",
             "ReplicaSet", "ReplicationController")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", ".scanvenv"}


def discover(roots: list[str]) -> list[tuple[str, Path, Path]]:
    """Return [(provider, scan_dir, attribution_file)] for every manifest.

    scan_dir is passed to pipeline-check's path flag; attribution_file is the
    repo path findings are rewritten to (and attributed from).
    """
    out: list[tuple[str, Path, Path]] = []
    chart_dirs: set[Path] = set()

    # Pass 1: Helm charts (a directory containing Chart.yaml). Scanned via
    # --helm-path <chartdir>; findings attribute to the Chart.yaml.
    for root in roots:
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            chart = next((n for n in ("Chart.yaml", "Chart.yml") if n in fns), None)
            if chart:
                chart_dirs.add(Path(dp).resolve())
                out.append(("helm", Path(dp), Path(dp) / chart))

    def under_chart(p: Path) -> bool:
        rp = str(p.resolve())
        return any(rp.startswith(str(c)) for c in chart_dirs)

    # Pass 2: Dockerfiles + Tekton/Argo/Kubernetes YAML (skip helm internals).
    for root in roots:
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            for name in fns:
                f = Path(dp) / name
                if under_chart(f):
                    continue
                if name == "Dockerfile" or name.endswith(".Dockerfile"):
                    out.append(("dockerfile", f.parent, f))
                    continue
                if not name.endswith((".yml", ".yaml")):
                    continue
                try:
                    head = f.read_text(encoding="utf-8", errors="replace")[:4000]
                except OSError:
                    continue
                prov = next((p for p, marker in YAML_MARKERS if marker in head), None)
                if prov is None and "apiVersion:" in head and \
                        any(f"kind: {k}" in head for k in K8S_KINDS):
                    prov = "kubernetes"
                if prov:
                    out.append((prov, f.parent, f))

    seen: set[tuple[str, str]] = set()
    res: list[tuple[str, Path, Path]] = []
    for prov, scan_dir, attr in out:
        key = (prov, str(attr.resolve()))
        if key not in seen:
            seen.add(key)
            res.append((prov, scan_dir, attr))
    return sorted(res, key=lambda t: (t[0], t[2].as_posix()))


def scan_one(prov: str, scan_dir: Path, attr: Path, pc_cmd: str) -> list[dict]:
    """Run pipeline-check on one manifest; return results with URIs rewritten."""
    proc = subprocess.run(
        [pc_cmd, "--pipeline", prov, FLAG[prov], str(scan_dir), "--output", "sarif"],
        capture_output=True, text=True, encoding="utf-8", errors="replace",
        env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
    )
    # pipeline-check exits 1 when findings are present; SARIF is still on stdout.
    if not proc.stdout.strip():
        print(f"warn: no pipeline-check output for {attr} ({prov}, exit {proc.returncode})",
              file=sys.stderr)
        return []
    try:
        doc = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        print(f"warn: bad pipeline-check SARIF for {attr}: {e}", file=sys.stderr)
        return []
    uri = attr.as_posix()
    results: list[dict] = []
    for run in doc.get("runs", []):
        for rule in (run.get("tool", {}).get("driver", {}) or {}).get("rules", []) or []:
            rid = rule.get("id")
            if rid:
                scan_one._rules[rid] = rule  # type: ignore[attr-defined]
        for r in run.get("results", []) or []:
            for loc in r.get("locations", []) or []:
                loc.setdefault("physicalLocation", {}).setdefault("artifactLocation", {})["uri"] = uri
            results.append(r)
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
    print(f"pipeline-check-resource-scan: {len(manifests)} manifest(s) "
          f"({', '.join(sorted({p for p, _, _ in manifests})) or 'none'})", file=sys.stderr)
    results: list[dict] = []
    for prov, scan_dir, attr in manifests:
        results.extend(scan_one(prov, scan_dir, attr, args.pc))

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
