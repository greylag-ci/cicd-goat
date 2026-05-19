#!/usr/bin/env python3
"""Aggregate SARIF outputs into a markdown comparison matrix.

Usage:
  python tools/comparison-report.py <sarif-dir> [--output report.md]

<sarif-dir> is the directory created by `actions/download-artifact@v4`
in the comparison-summary job — one subdirectory per scanner, each
containing one or more *.sarif files. The script walks the tree, counts
rule IDs per scanner, and emits a markdown report:

  - per-scanner total findings
  - per-rule counts per scanner
  - which scenarios (matched by file path under .github/workflows/) were
    flagged by which scanner

Pure stdlib; runs anywhere Python 3.9+ runs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SCENARIO_RE = re.compile(r"scenario-(\d+)-[a-z0-9-]+\.yml$")


def load_sarif(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def iter_results(sarif: dict):
    for run in sarif.get("runs", []) or []:
        tool = (run.get("tool", {}).get("driver", {}) or {}).get("name") or "unknown"
        for result in run.get("results", []) or []:
            yield tool, result


def result_locations(result: dict) -> list[str]:
    paths = []
    for loc in result.get("locations", []) or []:
        uri = (
            (loc.get("physicalLocation", {}) or {})
            .get("artifactLocation", {})
            .get("uri")
        )
        if uri:
            paths.append(uri)
    return paths


def scenario_of(path: str) -> str | None:
    m = SCENARIO_RE.search(path)
    return m.group(0) if m else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("sarif_dir", type=Path)
    ap.add_argument("--output", "-o", type=Path, default=Path("comparison-report.md"))
    args = ap.parse_args()

    if not args.sarif_dir.is_dir():
        print(f"error: {args.sarif_dir} is not a directory", file=sys.stderr)
        return 2

    sarif_files = sorted(args.sarif_dir.rglob("*.sarif"))
    if not sarif_files:
        print(f"error: no *.sarif files under {args.sarif_dir}", file=sys.stderr)
        return 2

    per_scanner_total: Counter[str] = Counter()
    per_scanner_rule: dict[str, Counter[str]] = defaultdict(Counter)
    per_scanner_scenarios: dict[str, set[str]] = defaultdict(set)

    for f in sarif_files:
        try:
            sarif = load_sarif(f)
        except (OSError, json.JSONDecodeError) as e:
            print(f"warn: cannot parse {f}: {e}", file=sys.stderr)
            continue
        for tool, result in iter_results(sarif):
            per_scanner_total[tool] += 1
            rule = result.get("ruleId") or "(no-ruleId)"
            per_scanner_rule[tool][rule] += 1
            for path in result_locations(result):
                scn = scenario_of(path)
                if scn:
                    per_scanner_scenarios[tool].add(scn)

    scanners = sorted(per_scanner_total)
    all_scenarios = sorted(
        {s for ss in per_scanner_scenarios.values() for s in ss}
    )

    lines: list[str] = []
    lines.append("# Scanner comparison report")
    lines.append("")
    lines.append(f"Source: `{args.sarif_dir}`")
    lines.append("")

    lines.append("## Total findings per scanner")
    lines.append("")
    lines.append("| Scanner | Total |")
    lines.append("|---|---:|")
    for s in scanners:
        lines.append(f"| {s} | {per_scanner_total[s]} |")
    lines.append("")

    lines.append("## Scenario coverage matrix")
    lines.append("")
    lines.append("Did each scanner flag at least one finding in each scenario file?")
    lines.append("")
    header = "| Scenario | " + " | ".join(scanners) + " |"
    divider = "|---|" + "---|" * len(scanners)
    lines.append(header)
    lines.append(divider)
    for scn in all_scenarios:
        cells = [
            "OK" if scn in per_scanner_scenarios[s] else "."
            for s in scanners
        ]
        lines.append(f"| `{scn}` | " + " | ".join(cells) + " |")
    lines.append("")

    lines.append("## Top rules per scanner")
    lines.append("")
    for s in scanners:
        lines.append(f"### {s}")
        lines.append("")
        lines.append("| Rule | Count |")
        lines.append("|---|---:|")
        for rule, n in per_scanner_rule[s].most_common(20):
            lines.append(f"| `{rule}` | {n} |")
        lines.append("")

    args.output.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {args.output} ({len(lines)} lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
