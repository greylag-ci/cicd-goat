"""Convert actionlint JSON output to SARIF v2.1.0.

actionlint has no native SARIF emitter. Its `-format '{{json .}}'` flag
prints every finding as a JSON array of {Message, Filepath, Line,
Column, Kind, Snippet}; this script wraps that array as a single SARIF
run consumable by `github/codeql-action/upload-sarif` and by
`tools/regen-readme.py`.

The actionlint `Kind` is preserved verbatim as the SARIF `ruleId` so
`scenarios.yaml`'s `expected:` lists can reference the upstream rule
names (`expression`, `shellcheck`, `credentials`, ...).

Usage:
    actionlint -format '{{json .}}' .github/workflows/ \
        | python tools/actionlint-to-sarif.py > actionlint.sarif
"""
from __future__ import annotations

import json
import sys

SARIF_SCHEMA = (
    "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/"
    "Schemata/sarif-schema-2.1.0.json"
)


def to_sarif(findings: list[dict]) -> dict:
    rule_ids = sorted({f.get("Kind") or "actionlint" for f in findings})
    return {
        "$schema": SARIF_SCHEMA,
        "version": "2.1.0",
        "runs": [
            {
                "tool": {
                    "driver": {
                        "name": "actionlint",
                        "informationUri": "https://github.com/rhysd/actionlint",
                        "rules": [
                            {
                                "id": rid,
                                "helpUri": f"https://github.com/rhysd/actionlint/blob/main/docs/checks.md#{rid}",
                            }
                            for rid in rule_ids
                        ],
                    }
                },
                "results": [
                    {
                        "ruleId": f.get("Kind") or "actionlint",
                        "level": "warning",
                        "message": {"text": f.get("Message") or ""},
                        "locations": [
                            {
                                "physicalLocation": {
                                    "artifactLocation": {
                                        "uri": f.get("Filepath") or "",
                                        "uriBaseId": "%SRCROOT%",
                                    },
                                    "region": {
                                        "startLine": f.get("Line") or 1,
                                        "startColumn": f.get("Column") or 1,
                                    },
                                }
                            }
                        ],
                    }
                    for f in findings
                ],
            }
        ],
    }


def main() -> int:
    raw = sys.stdin.read().strip()
    findings = json.loads(raw) if raw else []
    if not isinstance(findings, list):
        print(
            "error: expected a JSON array of findings on stdin",
            file=sys.stderr,
        )
        return 2
    json.dump(to_sarif(findings), sys.stdout, indent=2)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
