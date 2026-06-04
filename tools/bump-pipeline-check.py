"""Bump the pinned `pipeline-check` version + wheel hash in
.github/workflows/scanner-comparison.yml to a newer PyPI release.

This automates the *mechanical* half of a pipeline-check bump: the pin line
and the `# Pinned to X.Y.Z` comment. It deliberately does NOT touch
tools/scenarios.yaml `expected:` lists, the per-scenario READMEs, or the
grounding comments — deciding whether a new rule is the *canonical* catch
for a scenario is editorial judgment and stays a human review (the
`regen-readme.py --verify` drift report is the worklist for it).

Flow once a bump lands: scanner-comparison.yml runs the scanners against the
new version, regen-readme.yml regenerates the leaderboard + matrix from the
fresh SARIF, and its drift step flags scenarios whose `expected` rules now
fire (or newly-firing rules on `expected: []` rows) for the human pass.

Usage:
  python tools/bump-pipeline-check.py --check          # report only; exit 10 if a newer release exists
  python tools/bump-pipeline-check.py                  # rewrite the pin to the latest PyPI release
  python tools/bump-pipeline-check.py --version 1.9.0  # rewrite to a specific version

Exit codes: 0 = up to date / rewritten, 10 = newer available (--check only),
2 = error (network, no wheel, pin line not found).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "scanner-comparison.yml"
PYPI = "https://pypi.org/pypi/pipeline-check"

# The pinned requirement line inside the `--require-hashes` heredoc, e.g.
#   pipeline-check==1.9.0 --hash=sha256:59e5...f040
# Anchored on `pipeline-check==`, so sibling scanner pins are never matched.
PIN_RE = re.compile(
    r"(pipeline-check==)(\d+\.\d+\.\d+)(\s+--hash=sha256:)([0-9a-f]{64})"
)


def _version_key(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v.split("."))


def _get_json(url: str) -> dict:
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:  # noqa: S310 (pypi, https)
        return json.load(resp)


def latest_version() -> str:
    return _get_json(f"{PYPI}/json")["info"]["version"]


def wheel_sha256(version: str) -> str:
    data = _get_json(f"{PYPI}/{version}/json")
    for f in data.get("urls", []):
        if f.get("packagetype") == "bdist_wheel":
            return f["digests"]["sha256"]
    raise RuntimeError(f"no bdist_wheel for pipeline-check {version} on PyPI")


def current_pin() -> tuple[str, str]:
    """Return (version, sha256) of the pin currently in the workflow."""
    text = WORKFLOW.read_text(encoding="utf-8")
    m = PIN_RE.search(text)
    if not m:
        raise RuntimeError(f"pin line not found in {WORKFLOW}")
    return m.group(2), m.group(4)


def rewrite(version: str, sha: str, cur_ver: str) -> bool:
    """Rewrite the pin + comment to (version, sha). Returns True if the file changed.

    Reads/writes bytes so the file's existing newline style is preserved.
    """
    raw = WORKFLOW.read_bytes()
    text = raw.decode("utf-8")
    new = PIN_RE.sub(lambda m: f"{m.group(1)}{version}{m.group(3)}{sha}", text)
    # Update only the pipeline-check "# Pinned to <cur_ver>" comment. Anchoring
    # on the current pipeline-check version (not a bare \d+\.\d+\.\d+) keeps the
    # sibling scanner pins (octoscan, ciguard, … on different versions)
    # untouched; count=1 guards a freak same-version collision.
    comment_re = re.compile(r"(#\s*Pinned to\s+)" + re.escape(cur_ver) + r"\b")
    new = comment_re.sub(lambda m: f"{m.group(1)}{version}", new, count=1)
    if new == text:
        return False
    WORKFLOW.write_bytes(new.encode("utf-8"))
    return True


def _emit_output(**kv: str) -> None:
    """Write key=value pairs to $GITHUB_OUTPUT when running under Actions."""
    out = os.environ.get("GITHUB_OUTPUT")
    if not out:
        return
    with open(out, "a", encoding="utf-8") as fh:
        for k, v in kv.items():
            fh.write(f"{k}={v}\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--version", help="target version (default: latest on PyPI)")
    ap.add_argument(
        "--check", action="store_true",
        help="report only; exit 10 if a newer release exists, 0 if up to date",
    )
    args = ap.parse_args()

    try:
        cur_ver, cur_sha = current_pin()
        target = args.version or latest_version()
    except (urllib.error.URLError, RuntimeError, KeyError, TimeoutError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    newer = _version_key(target) > _version_key(cur_ver)
    print(f"pinned: {cur_ver}    latest: {target}    "
          f"{'NEWER AVAILABLE' if newer else 'up to date'}")
    _emit_output(current=cur_ver, latest=target)

    if args.check:
        _emit_output(changed="false")
        return 10 if newer else 0

    if not newer and not args.version:
        _emit_output(changed="false")
        return 0
    if target == cur_ver:
        print("target equals current pin; nothing to do.")
        _emit_output(changed="false")
        return 0

    try:
        sha = wheel_sha256(target)
    except (urllib.error.URLError, RuntimeError, KeyError, TimeoutError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    if not rewrite(target, sha, cur_ver):
        print("pin already matches target; no change written.", file=sys.stderr)
        _emit_output(changed="false")
        return 0

    print(f"bumped pipeline-check {cur_ver} -> {target}\n  sha256: {sha}")
    _emit_output(changed="true", current=cur_ver, latest=target, sha256=sha)
    return 0


if __name__ == "__main__":
    sys.exit(main())
