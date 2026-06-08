"""Run pipeline-check over each non-pipeline manifest under a tree (Tekton,
Argo, Dockerfile, Kubernetes, Helm, NuGet, OCI, Argo CD), normalise every
finding's SARIF artifact URI to the real file path, and merge into one SARIF
document on stdout (or --output).

Why a wrapper (cf. tools/ciguard-scan-tree.py):
  * pipeline-check's discovery for these manifest types is single-manifest per
    --<type>-path, so one invocation over scenarios/ only scans one file — we
    invoke it per discovered manifest instead.
  * It attaches some findings to a SYNTHETIC URI (`resource:///tekton`,
    `resource:///argocd`, `kubernetes/manifests`, …) rather than the file path,
    which can't be attributed to a scenario (regen-readme.py's SCENARIO_RE keys
    on `scenario-NN-` / `scenarios/NN-` in the URI). Each invocation scans
    exactly one scenario's manifest, so we rewrite every finding's URI to that
    file.
  * Some providers emit a path RELATIVE to the scanned dir with no `scenarios/`
    prefix (NuGet: `NN-slug/NuGet.config`), which SCENARIO_RE also won't match;
    the per-file rewrite fixes that too.
  * OCI attestation parsing (ATTEST-*) needs the whole image-layout directory
    (`index.json` + the `blobs/sha256/` tree), so we point --oci-manifest at the
    layout dir and attribute findings to its index.json / manifest.json.

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
import shlex
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
    "nuget":      "--nuget-path",
    "oci":        "--oci-manifest",
    "argocd":     "--argocd-path",
}
# content markers for the YAML CI-native resource types (priority order)
YAML_MARKERS = [("tekton", "tekton.dev/"), ("argo", "argoproj.io/")]
K8S_KINDS = ("Pod", "Deployment", "DaemonSet", "StatefulSet", "Job", "CronJob",
             "ReplicaSet", "ReplicationController")
# Argo CD resource shapes. These must be detected BEFORE the argoproj.io/ argo
# (Workflows) marker, because an AppProject / ApplicationSet also carries
# `argoproj.io/` but is an Argo CD object, not a Workflow. The argocd-cm /
# argocd-rbac-cm ConfigMaps are plain v1 ConfigMaps (no argoproj.io/ marker) and
# would otherwise be missed entirely.
ARGOCD_KIND_MARKERS = ("kind: Application", "kind: ApplicationSet", "kind: AppProject")
ARGOCD_CM_MARKERS = ("name: argocd-cm", "name: argocd-rbac-cm")
# NuGet manifest filenames (--nuget-path scans a directory containing these).
NUGET_NAMES = ("nuget.config", "packages.lock.json")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", ".scanvenv"}


def _is_oci_manifest(head: str) -> bool:
    """True when a JSON document head looks like an OCI / Docker-v2 image
    manifest or image index (has schemaVersion + an OCI/Docker media type)."""
    return '"schemaVersion"' in head and (
        "vnd.oci.image" in head or "vnd.docker.distribution" in head
    )


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

    # Pass 2: Dockerfiles + Tekton/Argo CD/Argo/Kubernetes YAML + NuGet + OCI
    # (skip helm internals).
    for root in roots:
        for dp, dns, fns in os.walk(root):
            dns[:] = [d for d in dns if d not in SKIP_DIRS]
            # Never descend into an OCI image-layout blobs/ tree: those blobs are
            # content-addressed payloads, resolved via the layout dir, not scanned.
            under_blobs = f"{os.sep}blobs{os.sep}" in (dp + os.sep)
            for name in fns:
                f = Path(dp) / name
                if under_chart(f):
                    continue
                if name == "Dockerfile" or name.endswith(".Dockerfile"):
                    out.append(("dockerfile", f.parent, f))
                    continue
                # NuGet: scan the dir holding the manifest (--nuget-path <dir>).
                if name.lower() in NUGET_NAMES or name.endswith(".csproj"):
                    out.append(("nuget", f.parent, f))
                    continue
                if name.endswith(".json") and not under_blobs:
                    try:
                        head = f.read_text(encoding="utf-8", errors="replace")[:4000]
                    except OSError:
                        continue
                    # OCI: point --oci-manifest at the layout DIR so the
                    # blobs/sha256/ tree (attestations) resolves; attribute to
                    # this manifest file.
                    if _is_oci_manifest(head):
                        out.append(("oci", f.parent, f))
                    continue
                if not name.endswith((".yml", ".yaml")):
                    continue
                try:
                    head = f.read_text(encoding="utf-8", errors="replace")[:4000]
                except OSError:
                    continue
                # Argo CD before the argoproj.io/ (Argo Workflows) marker: an
                # AppProject/ApplicationSet also carries argoproj.io/, and the
                # argocd-cm / argocd-rbac-cm ConfigMaps carry no marker at all.
                if any(m in head for m in ARGOCD_KIND_MARKERS) or \
                        any(m in head for m in ARGOCD_CM_MARKERS):
                    out.append(("argocd", f.parent, f))
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


def scan_one(prov: str, scan_dir: Path, attr: Path, pc_argv: list[str]) -> tuple[list[dict], bool]:
    """Run pipeline-check on one manifest; return (results, ok).

    `ok` is False on a HARD error (pipeline-check missing, crashed, or emitted
    unparseable/empty output) — distinct from a clean "no findings" scan, which
    returns ([], True). Callers must surface hard errors: a swallowed failure
    silently drops the scenario from the matrix and scores it as a clean miss.
    """
    try:
        proc = subprocess.run(
            [*pc_argv, "--pipeline", prov, FLAG[prov], str(scan_dir), "--output", "sarif"],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            env={**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"},
        )
    except FileNotFoundError as e:
        print(f"error: cannot run pipeline-check ({' '.join(pc_argv)}): {e}", file=sys.stderr)
        return [], False
    # pipeline-check exits 0 (no findings) or 1 (findings); SARIF is on stdout
    # either way. Any other exit code is a real failure, not a verdict.
    if proc.returncode not in (0, 1):
        print(f"error: pipeline-check exit {proc.returncode} for {attr} ({prov}): "
              f"{proc.stderr.strip()[:200]}", file=sys.stderr)
        return [], False
    if not proc.stdout.strip():
        print(f"error: empty pipeline-check output for {attr} ({prov}, exit {proc.returncode})",
              file=sys.stderr)
        return [], False
    try:
        doc = json.loads(proc.stdout)
    except json.JSONDecodeError as e:
        print(f"error: bad pipeline-check SARIF for {attr}: {e}", file=sys.stderr)
        return [], False
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
    return results, True


scan_one._rules = {}  # type: ignore[attr-defined]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("roots", nargs="*", default=["scenarios"],
                    help="directories to walk (default: scenarios)")
    ap.add_argument("--output", type=Path, help="write merged SARIF here (default: stdout)")
    ap.add_argument("--pc", default=None,
                    help="pipeline-check command, shell-style (default: "
                         "'<python> -m pipeline_check'). Use the module form, not the "
                         "console-script name, so it doesn't depend on a PATH entry point.")
    args = ap.parse_args()
    roots = args.roots or ["scenarios"]
    pc_argv = shlex.split(args.pc) if args.pc else [sys.executable, "-m", "pipeline_check"]

    manifests = discover(roots)
    print(f"pipeline-check-resource-scan: {len(manifests)} manifest(s) "
          f"({', '.join(sorted({p for p, _, _ in manifests})) or 'none'})", file=sys.stderr)
    results: list[dict] = []
    failures = 0
    for prov, scan_dir, attr in manifests:
        res, ok = scan_one(prov, scan_dir, attr, pc_argv)
        results.extend(res)
        if not ok:
            failures += 1

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
    if failures:
        print(f"error: {failures} of {len(manifests)} manifest scan(s) failed — "
              f"those scenarios would be silently dropped from the matrix",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
