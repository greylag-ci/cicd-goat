"""Regenerate README + MATRIX stats from tools/scenarios.yaml + scanner SARIF.

Two modes:

  regen (default):
    Reads tools/scenarios.yaml, downloads/loads SARIF for each scanner,
    computes per-(scenario, scanner) verdicts based on whether each
    `expected` rule actually fired, and rewrites the AUTOGEN sections in:
      - README.md         : badges, leaderboard (compact totals)
      - docs/MATRIX.md    : full matrix, scenarios index

  verify (--verify):
    Same parse but doesn't write the README.  Exits non-zero if any
    scanner that scenarios.yaml claims catches a scenario (`expected`
    list non-empty) emitted *none* of those rules in the latest SARIF.
    Wired into a CI workflow so the matrix can't silently drift.

Usage:
  # download latest SARIF from main + regen:
  python tools/regen-readme.py --from-latest-run

  # use a local SARIF dir (gh run download ./sarif):
  python tools/regen-readme.py --sarif-dir ./sarif

  # CI:
  python tools/regen-readme.py --verify --sarif-dir ./sarif
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
MATRIX_DOC = ROOT / "docs" / "MATRIX.md"
COVERAGE_AXES_DOC = ROOT / "docs" / "COVERAGE-AXES.md"
RULE_FIRINGS_DOC = ROOT / "docs" / "RULE-FIRINGS.md"
DATA = ROOT / "tools" / "scenarios.yaml"

VERDICT_FULL = "✅"        # ✅
VERDICT_PARTIAL = "⚠️"  # ⚠️
VERDICT_MISS = "❌"        # ❌
VERDICT_NA = "—"          # —

SEVERITY_LABELS = {
    "critical": "\U0001f534 critical",  # 🔴
    "high":     "\U0001f7e0 high",       # 🟠
    "medium":   "\U0001f7e1 medium",     # 🟡
    "low":      "\U0001f535 low",        # 🔵
}

# Provider a scenario targets when its `provider:` key is omitted — the
# original 38 scenarios predate the multi-provider expansion and are all
# GitHub Actions.
DEFAULT_PROVIDER = "github"

# Display names + canonical render order for the per-provider sections.
# Only providers that actually appear in scenarios.yaml are rendered, but
# they always come out in this order so the GitHub Actions corpus leads.
PROVIDER_LABELS = {
    "github":     "GitHub Actions",
    "gitlab":     "GitLab CI",
    "azure":      "Azure Pipelines",
    "circleci":   "CircleCI",
    "bitbucket":  "Bitbucket Pipelines",
    "jenkins":    "Jenkins",
    "tekton":     "Tekton",
    "argo":       "Argo Workflows",
    "drone":      "Drone CI",
    "buildkite":  "Buildkite",
    "cloudbuild": "Cloud Build",
    # IaC / manifest types (the artifacts pipelines build and deploy)
    "dockerfile":     "Dockerfile",
    "kubernetes":     "Kubernetes",
    "terraform":      "Terraform",
    "cloudformation": "CloudFormation",
    "helm":           "Helm",
}
PROVIDER_ORDER = list(PROVIDER_LABELS)


def scenario_provider(scn: dict) -> str:
    return scn.get("provider", DEFAULT_PROVIDER)


def scanner_supports(scanner: dict, provider: str) -> bool:
    """True if `scanner` can statically scan `provider`'s pipeline files.

    A scanner with no `providers:` key is treated as universal (applies to
    every provider) for backward compatibility; in practice every scanner
    in scenarios.yaml declares one.
    """
    provs = scanner.get("providers")
    if provs is None:
        return True
    return provider in provs


def applicable(scn: dict, scanner: dict) -> bool:
    return scanner_supports(scanner, scenario_provider(scn))


def providers_in_use(data: dict) -> list[str]:
    """Providers that appear in scenarios.yaml, in canonical render order."""
    seen = {scenario_provider(s) for s in data["scenarios"]}
    extra = sorted(seen - set(PROVIDER_ORDER))  # unknown providers, if any
    return [p for p in PROVIDER_ORDER if p in seen] + extra


def provider_label(provider: str) -> str:
    return PROVIDER_LABELS.get(provider, provider)


def scenarios_for(data: dict, provider: str) -> list[dict]:
    return [s for s in data["scenarios"] if scenario_provider(s) == provider]


def scanners_for(data: dict, provider: str) -> list[dict]:
    return [s for s in data["scanners"] if scanner_supports(s, provider)]

# Matches either the canonical workflow filename (`scenario-NN-...yml`)
# or a sibling file inside the scenario's writeup dir
# (`scenarios/NN-.../action/action.yml`, `scenarios/NN-.../trust-policy.json`,
# etc.). The latter form lets a scanner that walks composite-action /
# trust-policy / package.json siblings attribute its finding to the
# scenario whose dir contains them. Without the second alternative,
# scenarios 18 / 20 / 28's cross-file sinks silently disappear from
# the matrix.
SCENARIO_RE = re.compile(r"(?:scenario-|scenarios/)(\d+)-")
REPO_DEFAULT = "greylag-ci/cicd-goat"
WORKFLOW_DEFAULT = "scanner-comparison.yml"


def load_data() -> dict:
    return yaml.safe_load(DATA.read_text(encoding="utf-8"))


def parse_sarif_dir(sarif_dir: Path) -> dict[str, dict[int, set[str]]]:
    """Return {tool_name: {scenario_id: set(rule_ids_fired_on_that_scenario)}}."""
    out: dict[str, dict[int, set[str]]] = {}
    files = list(sarif_dir.rglob("*.sarif"))
    if not files:
        print(f"warning: no *.sarif under {sarif_dir}", file=sys.stderr)
    for f in files:
        try:
            doc = json.loads(f.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"warn: {f}: {e}", file=sys.stderr)
            continue
        for run in doc.get("runs", []) or []:
            tool = (run.get("tool", {}).get("driver", {}) or {}).get("name", "unknown")
            d = out.setdefault(tool, {})
            for r in run.get("results", []) or []:
                rid = r.get("ruleId") or ""
                for loc in r.get("locations", []) or []:
                    # Each hop can be JSON `null` (not just missing) for malformed
                    # SARIF — chain `or {}` everywhere so AttributeError doesn't
                    # abort the whole regen on one bad scanner output.
                    phys = loc.get("physicalLocation") or {}
                    art = phys.get("artifactLocation") or {}
                    uri = art.get("uri") or ""
                    m = SCENARIO_RE.search(uri)
                    if m:
                        d.setdefault(int(m.group(1)), set()).add(rid)
    return out


def download_latest_run_sarif(repo: str, workflow: str, dest: Path) -> None:
    """Find the latest successful run of `workflow` on main and download artifacts."""
    cmd = [
        "gh", "run", "list",
        "--repo", repo,
        "--workflow", workflow,
        "--branch", "main",
        "--status", "success",
        "--limit", "1",
        "--json", "databaseId",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    runs = json.loads(res.stdout)
    if not runs:
        raise SystemExit(f"error: no successful runs of {workflow} on main")
    run_id = runs[0]["databaseId"]
    print(f"downloading SARIF from run {run_id} -> {dest}", file=sys.stderr)
    subprocess.run(
        ["gh", "run", "download", str(run_id), "--repo", repo, "--dir", str(dest)],
        check=True,
    )


def verdict(scenario: dict, scanner: dict, sarif_data: dict) -> str:
    # Structural na: the scanner can't read this provider's files at all,
    # so it's not-applicable rather than a miss.  Resolved before looking
    # at `expected:` so authors don't have to spell out `na` for every
    # GHA-only scanner on every non-GHA row.
    if not applicable(scenario, scanner):
        return VERDICT_NA
    # Use .get() on both hops in case a malformed scenario row omits
    # `expected:` entirely — KeyError here would abort the whole regen.
    expected = scenario.get("expected", {}).get(scanner["id"])
    if expected == "na":
        return VERDICT_NA
    if not isinstance(expected, list):
        return VERDICT_MISS
    if not expected:
        return VERDICT_MISS
    fired = sarif_data.get(scanner["sarif_tool"], {}).get(scenario["id"], set())
    matches = sum(1 for r in expected if r in fired)
    if matches == len(expected):
        return VERDICT_FULL
    if matches > 0:
        return VERDICT_PARTIAL
    return VERDICT_MISS


def compute_totals(
    data: dict, sarif_data: dict, scenarios: list[dict] | None = None
) -> dict[str, dict[str, int]]:
    """Per-scanner verdict counts across `scenarios` (default: all)."""
    if scenarios is None:
        scenarios = data["scenarios"]
    totals: dict[str, dict[str, int]] = {}
    for s in data["scanners"]:
        t = {VERDICT_FULL: 0, VERDICT_PARTIAL: 0, VERDICT_MISS: 0, VERDICT_NA: 0}
        for scn in scenarios:
            t[verdict(scn, s, sarif_data)] += 1
        totals[s["id"]] = t
    return totals


def _leaderboard_cell(t: dict[str, int]) -> str:
    cell = f"**{t[VERDICT_FULL]} {VERDICT_FULL}**"
    if t[VERDICT_PARTIAL]:
        cell += f" · {t[VERDICT_PARTIAL]} {VERDICT_PARTIAL}"
    return cell


def render_leaderboard(data: dict, sarif_data: dict) -> str:
    """Per-provider leaderboards for the README landing page.

    One ranked table per provider in use, listing only the scanners that
    can scan that provider (so GHA-only scanners don't show up under
    GitLab / Jenkins / …).  Within each table, sorted by full-catch count
    desc, then partials desc; stable on ties via scanners.yaml order.
    The denominator is the number of scenarios for that provider.
    """
    out: list[str] = []
    for prov in providers_in_use(data):
        scns = scenarios_for(data, prov)
        scanners = scanners_for(data, prov)
        totals = compute_totals(data, sarif_data, scns)
        order = sorted(
            scanners,
            key=lambda s: (-totals[s["id"]][VERDICT_FULL], -totals[s["id"]][VERDICT_PARTIAL]),
        )
        n = len(scns)
        out.append(f"### {provider_label(prov)} — {n} scenario{'s' if n != 1 else ''}")
        out.append("")
        out.append(f"| Scanner | Scenarios caught (of {n}) |")
        out.append("| :--- | :--- |")
        for s in order:
            out.append(f"| {s['label']} | {_leaderboard_cell(totals[s['id']])} |")
        out.append("")
    return "\n".join(out).rstrip()


def render_matrix(data: dict, sarif_data: dict) -> str:
    """Full verdict matrix, sectioned by provider.

    Each provider gets its own table whose columns are only the scanners
    that scan that provider — keeping non-applicable "—" columns out of
    the table rather than filling them with em-dashes.
    """
    out: list[str] = []
    for prov in providers_in_use(data):
        scns = scenarios_for(data, prov)
        scanners = scanners_for(data, prov)
        totals = compute_totals(data, sarif_data, scns)
        out.append(f"### {provider_label(prov)}")
        out.append("")
        out.append("| #  | Scenario | " + " | ".join(s["label"] for s in scanners) + " |")
        out.append("| :-:| :--- | " + " | ".join(":-:" for _ in scanners) + " |")
        for scn in scns:
            cells = [verdict(scn, s, sarif_data) for s in scanners]
            out.append(f"| {scn['id']:02d} | {scn['title']} | " + " | ".join(cells) + " |")
        parts = [_leaderboard_cell(totals[s["id"]]) for s in scanners]
        out.append("|    | **canonical bugs caught** | " + " | ".join(parts) + " |")
        out.append("")
    return "\n".join(out).rstrip()


def render_scenarios_index(data: dict) -> str:
    rows: list[str] = []
    rows.append("| #  | Title | Provider | CICD-SEC | Severity |")
    rows.append("| :-:| :--- | :-- | :-: | :-- |")
    for scn in data["scenarios"]:
        cs = " · ".join(str(x) for x in scn["cicd_sec"])
        sev = SEVERITY_LABELS.get(scn["severity"], scn["severity"])
        prov = provider_label(scenario_provider(scn))
        # docs/MATRIX.md lives one level below repo root, so links go up.
        link = f"../scenarios/{scn['slug']}/README.md"
        rows.append(f"| {scn['id']:02d} | [{scn['title']}]({link}) | {prov} | {cs} | {sev} |")
    return "\n".join(rows)


# CICD-SEC category titles (from OWASP project; one-line summary each).
CICD_SEC_TITLES = {
    1:  "Insufficient flow control",
    2:  "Inadequate IAM",
    3:  "Dependency chain abuse",
    4:  "Poisoned pipeline execution",
    5:  "Insufficient PBAC",
    6:  "Insufficient credential hygiene",
    7:  "Insecure system configuration",
    8:  "Ungoverned 3rd-party services",
    9:  "Improper artifact integrity validation",
    10: "Insufficient logging & visibility",
}


def _catches(scn: dict, scanner: dict, sarif_data: dict) -> bool:
    """True if scanner gets ✅ on this scenario."""
    return verdict(scn, scanner, sarif_data) == VERDICT_FULL


def _coverage_cell(scns: list[dict], scanner: dict, sarif_data: dict) -> str:
    """`caught / applicable` for a scanner over a scenario bucket.

    The denominator counts only scenarios whose provider this scanner can
    scan, so a GHA-only scanner shows e.g. `0/3` (or `—` when none of the
    bucket's scenarios are GHA) instead of being scored against GitLab /
    Jenkins rows it was never built to read.
    """
    appl = [sc for sc in scns if applicable(sc, scanner)]
    if not appl:
        return VERDICT_NA
    caught = sum(1 for sc in appl if _catches(sc, scanner, sarif_data))
    return f"{caught}/{len(appl)}"


def render_cicd_sec_coverage(data: dict, sarif_data: dict) -> str:
    """One row per CICD-SEC category 1..10; cells show catches/total."""
    scanners = data["scanners"]
    # Bucket scenarios by category (a scenario can appear in multiple buckets).
    by_cat: dict[int, list[dict]] = {c: [] for c in range(1, 11)}
    for scn in data["scenarios"]:
        for c in scn["cicd_sec"]:
            by_cat.setdefault(c, []).append(scn)
    rows: list[str] = []
    rows.append("| # | Category | Scenarios | " + " | ".join(s["label"] for s in scanners) + " |")
    rows.append("| :-: | :-- | :-: | " + " | ".join(":-:" for _ in scanners) + " |")
    for c in range(1, 11):
        scns = by_cat.get(c, [])
        n = len(scns)
        if n == 0:
            cells = [VERDICT_NA for _ in scanners]
        else:
            cells = [_coverage_cell(scns, s, sarif_data) for s in scanners]
        rows.append(
            f"| {c} | {CICD_SEC_TITLES.get(c, '')} | {n if n else '—'} | "
            + " | ".join(cells) + " |"
        )
    return "\n".join(rows)


def render_severity_coverage(data: dict, sarif_data: dict) -> str:
    """One row per severity tier; cells show catches/total at that tier."""
    scanners = data["scanners"]
    order = ["critical", "high", "medium", "low"]
    by_sev: dict[str, list[dict]] = {sev: [] for sev in order}
    for scn in data["scenarios"]:
        by_sev.setdefault(scn["severity"], []).append(scn)
    rows: list[str] = []
    rows.append("| Severity | Scenarios | " + " | ".join(s["label"] for s in scanners) + " |")
    rows.append("| :-- | :-: | " + " | ".join(":-:" for _ in scanners) + " |")
    for sev in order:
        scns = by_sev.get(sev, [])
        n = len(scns)
        if n == 0:
            continue
        label = SEVERITY_LABELS.get(sev, sev)
        cells = [_coverage_cell(scns, s, sarif_data) for s in scanners]
        rows.append(f"| {label} | {n} | " + " | ".join(cells) + " |")
    return "\n".join(rows)


def render_rule_firings(data: dict, sarif_data: dict) -> str:
    """For each scenario, render every rule each scanner fired.

    Annotates rules that are on the scenario's `expected:` canonical-bug
    list with **bold**, so noise/off-target firings are visually distinct
    from canonical-bug matches.
    """
    out: list[str] = []
    for scn in data["scenarios"]:
        prov = scenario_provider(scn)
        # Only scanners that can read this provider's files — the rest
        # would be a row of "(none) / —" noise on every non-GHA scenario.
        scanners = scanners_for(data, prov)
        out.append(f"### Scenario {scn['id']:02d} — {scn['title']} ({provider_label(prov)})")
        out.append("")
        out.append("| Scanner | Rules fired | Verdict |")
        out.append("| :-- | :-- | :-: |")
        for s in scanners:
            fired = sorted(
                sarif_data.get(s["sarif_tool"], {}).get(scn["id"], set())
            )
            expected = scn.get("expected", {}).get(s["id"])
            expected_set: set[str] = (
                set(expected) if isinstance(expected, list) else set()
            )
            if fired:
                rules_text = ", ".join(
                    (f"**`{r}`**" if r in expected_set else f"`{r}`")
                    for r in fired
                )
            else:
                rules_text = "_(none)_"
            v = verdict(scn, s, sarif_data)
            out.append(f"| {s['label']} | {rules_text} | {v} |")
        out.append("")
    return "\n".join(out).rstrip()


def render_unique_catches(data: dict, sarif_data: dict) -> str:
    """Scenarios where exactly one scanner catches the canonical bug."""
    scanners = data["scanners"]
    label = {s["id"]: s["label"] for s in scanners}
    unique_count: dict[str, int] = {s["id"]: 0 for s in scanners}
    table_rows: list[str] = []
    table_rows.append("| #  | Scenario | Solo catcher |")
    table_rows.append("| :-: | :-- | :-- |")
    for scn in data["scenarios"]:
        catchers = [s for s in scanners if _catches(scn, s, sarif_data)]
        if len(catchers) != 1:
            continue
        sid = catchers[0]["id"]
        unique_count[sid] += 1
        link = f"../scenarios/{scn['slug']}/README.md"
        table_rows.append(
            f"| {scn['id']:02d} | [{scn['title']}]({link}) | **{label[sid]}** |"
        )
    # Trailing summary table.
    summary: list[str] = []
    summary.append("")
    summary.append("**Solo catches per scanner** — scenarios where this is the only ✅ on the row:")
    summary.append("")
    summary.append("| Scanner | Solo catches |")
    summary.append("| :-- | :-: |")
    # Sort by count desc, stable on scanners.yaml order.
    order = sorted(
        [s["id"] for s in scanners],
        key=lambda sid: -unique_count[sid],
    )
    for sid in order:
        summary.append(f"| {label[sid]} | **{unique_count[sid]}** |")
    return "\n".join(table_rows + summary)


def render_badge_line(data: dict) -> str:
    n_scn = len(data["scenarios"])
    n_scan = len(data["scanners"])
    n_prov = len(providers_in_use(data))
    badges = [
        "[![scanner-comparison](https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml/badge.svg)]"
        "(https://github.com/greylag-ci/cicd-goat/actions/workflows/scanner-comparison.yml)",
        "[![License Apache 2.0](https://img.shields.io/badge/license-Apache_2.0-3a3a3a?style=flat-square)](LICENSE)",
        "[![CICD-SEC top 10](https://img.shields.io/badge/owasp-CICD--SEC_10%2F10-9c2b2b?style=flat-square)]"
        "(https://owasp.org/www-project-top-10-ci-cd-security-risks/)",
        f"[![scenarios {n_scn}](https://img.shields.io/badge/scenarios-{n_scn}-1f6feb?style=flat-square)](scenarios/README.md)",
        f"[![providers {n_prov}](https://img.shields.io/badge/providers-{n_prov}-1f6feb?style=flat-square)](docs/MATRIX.md)",
        f"[![scanners {n_scan}](https://img.shields.io/badge/scanners-{n_scan}-1f6feb?style=flat-square)](docs/MATRIX.md)",
    ]
    return "\n".join(badges)


def patch_markers(path: Path, content: str, sections: dict[str, str]) -> str:
    """Rewrite every <!-- AUTOGEN:<marker> --> block in `content`.

    `sections` maps marker name -> replacement text.  Missing a marker in
    the file is fatal — keeps us from silently dropping a section after a
    rename.
    """
    for marker, replacement in sections.items():
        pattern = re.compile(
            rf"(<!-- AUTOGEN:{re.escape(marker)} -->\n).*?(\n<!-- /AUTOGEN:{re.escape(marker)} -->)",
            re.DOTALL,
        )
        content, n = pattern.subn(
            lambda _m, r=replacement: _m.group(1) + r + _m.group(2),
            content,
        )
        if n == 0:
            raise SystemExit(f"error: marker AUTOGEN:{marker} not found in {path}")
    return content


def verify(data: dict, sarif_data: dict) -> int:
    """Check every (scenario, scanner) where expected is non-empty: at least one rule fired."""
    drifts: list[str] = []
    for scn in data["scenarios"]:
        for s in data["scanners"]:
            if not applicable(scn, s):
                continue
            expected = scn.get("expected", {}).get(s["id"])
            if not isinstance(expected, list) or not expected:
                continue
            fired = sarif_data.get(s["sarif_tool"], {}).get(scn["id"], set())
            if not any(r in fired for r in expected):
                drifts.append(
                    f"  scenario {scn['id']:02d} ({scn['title']!r}): "
                    f"'{s['id']}' was expected to fire one of {expected} "
                    f"but none did. SARIF for this scenario contains: {sorted(fired) or '(empty)'}"
                )
    if drifts:
        print(
            f"\nDRIFT DETECTED ({len(drifts)} mismatch(es) between scenarios.yaml and SARIF):",
            file=sys.stderr,
        )
        for d in drifts:
            print(d, file=sys.stderr)
        print(
            "\nResolve by either (a) updating scenarios.yaml to reflect the scanner's "
            "current behavior, or (b) restoring the rule on the scanner side.\n",
            file=sys.stderr,
        )
        return 1
    print(
        f"verify OK: every non-empty `expected` rule list in scenarios.yaml "
        f"has at least one rule firing in the latest SARIF."
    )
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Regenerate README stats from scenarios.yaml + scanner SARIF.",
    )
    src = ap.add_mutually_exclusive_group()
    src.add_argument("--sarif-dir", type=Path,
                     help="Directory containing scanner SARIF subdirs (gh run download output).")
    src.add_argument("--from-latest-run", action="store_true",
                     help="Fetch SARIF from the latest successful scanner-comparison run on main via gh.")
    ap.add_argument("--repo", default=REPO_DEFAULT)
    ap.add_argument("--workflow", default=WORKFLOW_DEFAULT)
    ap.add_argument("--verify", action="store_true",
                    help="Don't write the README; check that scenarios.yaml claims still match SARIF.")
    ap.add_argument("--allow-empty-sarif", action="store_true",
                    help="Don't abort the regen when SARIF parsing yields no tools "
                         "(default: refuse, since the output would mark every verdict ❌).")
    args = ap.parse_args()

    data = load_data()

    sarif_data: dict[str, dict[int, set[str]]] = {}
    if args.from_latest_run:
        with tempfile.TemporaryDirectory(prefix="cicd-goat-sarif-") as tmp:
            download_latest_run_sarif(args.repo, args.workflow, Path(tmp))
            sarif_data = parse_sarif_dir(Path(tmp))
    elif args.sarif_dir:
        if not args.sarif_dir.is_dir():
            print(f"error: --sarif-dir {args.sarif_dir} not found", file=sys.stderr)
            return 2
        sarif_data = parse_sarif_dir(args.sarif_dir)
    else:
        print(
            "error: provide --sarif-dir PATH or --from-latest-run "
            "(SARIF is required to derive verdicts)",
            file=sys.stderr,
        )
        return 2

    if args.verify:
        return verify(data, sarif_data)

    # Guard: rewriting the AUTOGEN sections against zero SARIF would flip
    # every verdict to ❌ and silently corrupt README.md + docs/MATRIX.md.
    # Caught in CI by `if: hashFiles('sarif/**/*.sarif') != ''`; this is
    # the local-run guard.
    #
    # Two empty shapes catch the matrix:
    #   (a) no tools at all — sarif_data == {} (e.g. SARIF dir empty)
    #   (b) tools present but every per-scenario map empty — e.g. every
    #       finding URI failed SCENARIO_RE. Without this second check the
    #       guard passes and every verdict silently flips to ❌.
    parsed_findings = sum(len(v) for v in sarif_data.values())
    if (not sarif_data or parsed_findings == 0) and not args.allow_empty_sarif:
        print(
            "error: parsed SARIF contains zero tools — refusing to rewrite "
            "AUTOGEN sections (would mark every verdict ❌). "
            "Check --sarif-dir path, or pass --allow-empty-sarif to override.",
            file=sys.stderr,
        )
        return 2

    sections_by_file: dict[Path, dict[str, str]] = {
        README: {
            "badges":      render_badge_line(data),
            "leaderboard": render_leaderboard(data, sarif_data),
        },
        MATRIX_DOC: {
            "matrix":           render_matrix(data, sarif_data),
            "scenarios-index":  render_scenarios_index(data),
        },
        COVERAGE_AXES_DOC: {
            "cicd-sec-coverage": render_cicd_sec_coverage(data, sarif_data),
            "severity-coverage": render_severity_coverage(data, sarif_data),
            "unique-catches":    render_unique_catches(data, sarif_data),
        },
        RULE_FIRINGS_DOC: {
            "rule-firings": render_rule_firings(data, sarif_data),
        },
    }
    for path, sections in sections_by_file.items():
        if not path.exists():
            print(f"warn: {path} missing — skipping (run from a checked-out repo)", file=sys.stderr)
            continue
        new = patch_markers(path, path.read_text(encoding="utf-8"), sections)
        path.write_text(new, encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        print(f"regenerated {rel} ({path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
