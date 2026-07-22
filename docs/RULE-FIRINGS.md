# Per-rule firing detail

For every (scenario × scanner) pair, the rules that each scanner
actually fired on that scenario's workflow file — not just the
canonical-bug rule. Use this view when:

- Investigating *why* a verdict came out the way it did
- Spotting hygiene rules a scanner fires on every workflow (so you can
  filter them when reading SARIF directly)
- Cross-checking [`scenarios.yaml`](../tools/scenarios.yaml)
  `expected:` claims against what the scanner is doing today — the
  `--verify` mode of [`regen-readme.py`](../tools/regen-readme.py)
  catches drift programmatically; this page is the eyeball view.

## How to read it

For each scenario, one row per scanner:

- **`bold rule ID`** = the canonical-bug rule for this scenario per
  `scenarios.yaml`. Multiple bold IDs in one cell means the scanner
  ships several rules that all name the same canonical bug.
- `non-bold rule ID` = a rule that fired but isn't the canonical-bug
  rule for this scenario. Could be: a relevant adjacent finding, a
  hygiene rule that fires on every workflow, or a false positive on
  the scenario's anti-pattern. Cross-reference with
  [FIELD-TEST.md § ⑤](FIELD-TEST.md#-the-hygiene-baseline--a-scope-difference-layered-on-top-of-a-coverage-one)
  for the absence-of-control rule family.
- _(none)_ = scanner emitted nothing on this workflow file.
- The **Verdict** column is the same as the [main matrix](MATRIX.md)
  cell: ✅ if every canonical-bug rule fired, ⚠️ if some, ❌ if none,
  — if not applicable.

Same source as the main matrix — auto-rebuilt from the latest
`scanner-comparison` SARIF on `main`.

---

<!-- AUTOGEN:rule-firings -->
### Scenario 01 — `pull_request_target` + fork-head checkout (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, **`GHA-002`**, `GHA-004`, `GHA-015`, `GHA-037`, **`GHA-044`**, `GHA-059` | ✅ |
| zizmor | **`zizmor/dangerous-triggers`**, `zizmor/unpinned-uses` | ✅ |
| poutine | **`untrusted_checkout_exec`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | **`dangerous-checkout`** | ✅ |

### Scenario 02 — Script injection via issue title (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`**, `GHA-004`, `GHA-015` | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | **`20f14e1a-a899-4e79-9f09-b6a84cd4649b`** | ✅ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`**, `if-cond` | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 03 — Action pinned to mutable ref (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `AC-018`, **`GHA-001`**, `GHA-014`, `GHA-015`, `GHA-037`, `GHA-098` | ✅ |
| zizmor | `zizmor/artipacked`, **`zizmor/unpinned-uses`** | ✅ |
| poutine | **`github_action_from_unverified_creator_used`** | ✅ |
| KICS | **`555ab8f9-2001-455e-a077-f2d0f41e2fb9`** | ✅ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 04 — `GITHUB_TOKEN` `write-all` (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, **`GHA-004`**, `GHA-015`, `GHA-037`, `GHA-059`, `GHA-069`, `GHA-108` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | **`CKV2_GHA_1`** | ✅ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 05 — Cache poisoning via PR title (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, **`GHA-011`**, `GHA-015`, `GHA-037`, **`GHA-052`**, `GHA-059` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 06 — Reusable workflow `secrets: inherit` (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GHA-014`, **`GHA-034`**, `GHA-098` | ✅ |
| zizmor | **`zizmor/secrets-inherit`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | `local-action` | ❌ |

### Scenario 07 — `workflow_run` artifact RCE (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-004`, **`GHA-009`**, `GHA-015`, **`GHA-032`** | ✅ |
| zizmor | **`zizmor/dangerous-triggers`**, `zizmor/unpinned-uses` | ✅ |
| poutine | **`known_vulnerability_in_build_component`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 08 — Self-hosted runner on public repo (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, **`GHA-012`**, `GHA-015`, `GHA-037`, `GHA-059`, `GHA-105` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | **`pr_runs_on_self_hosted`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | **`runner-label`** | ✅ |

### Scenario 09 — Container image `:latest` (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, **`GHA-051`** | ✅ |
| zizmor | `zizmor/artipacked`, **`zizmor/unpinned-images`**, `zizmor/unpinned-uses` | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 10 — AWS OIDC wildcard `sub` (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GHA-001`, `GHA-006`, `GHA-007`, `GHA-015`, `GHA-020`, `GHA-024`, `GHA-037`, **`GHA-062`**, `GHA-098`, `GHA-108` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | `555ab8f9-2001-455e-a077-f2d0f41e2fb9` | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 11 — `pip install` no hashes (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, **`GHA-060`**, `PYPI-001`, `PYPI-002` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 12 — `persist-credentials` leak (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-004`, `GHA-015`, **`GHA-037`** | ✅ |
| zizmor | **`zizmor/artipacked`**, `zizmor/unpinned-uses` | ✅ |
| poutine | **`github_action_from_unverified_creator_used`** | ✅ |
| KICS | **`555ab8f9-2001-455e-a077-f2d0f41e2fb9`** | ✅ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 13 — `workflow_dispatch` input injection (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-002`, `AC-005`, `AC-018`, `GHA-001`, **`GHA-003`**, `GHA-014`, `GHA-015`, `GHA-023`, `GHA-037`, `GHA-070`, `GHA-098` | ✅ |
| zizmor | `zizmor/artipacked`, **`zizmor/template-injection`**, `zizmor/unpinned-uses` | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | **`CKV_GHA_7`** | ✅ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 14 — `$GITHUB_ENV` poisoning (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, **`GHA-003`**, `GHA-015`, `GHA-037` | ✅ |
| zizmor | `zizmor/artipacked`, **`zizmor/template-injection`**, `zizmor/unpinned-uses` | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`**, `if-cond` | ✅ |
| octoscan | **`dangerous-write`**, `expression-injection` | ✅ |

### Scenario 15 — Hardcoded secret in `env:` (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, **`GHA-008`**, `GHA-015`, `GHA-037` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | **`487f4be7-3fd9-4506-a07a-eae252180c08`**, **`baee238e-1921-4801-9c3f-79ae1d7b2cbc`** | ✅ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 16 — `curl \| sh` install (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, **`GHA-016`**, `GHA-037` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | **`unverified_script_exec`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 17 — ArtiPACKED — `.git/` in artifact (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GHA-001`, `GHA-006`, `GHA-007`, `GHA-015`, **`GHA-019`**, `GHA-020`, `GHA-024`, **`GHA-037`**, `GHA-066` | ✅ |
| zizmor | **`zizmor/artipacked`**, `zizmor/unpinned-uses` | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | **`dangerous-artefact`** | ✅ |

### Scenario 18 — Composite action `${{ inputs.* }}` injection (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, **`GHA-003`**, `GHA-004`, `GHA-013`, `GHA-015`, `GHA-037` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/template-injection`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | **`expression-injection`**, `local-action` | ✅ |

### Scenario 19 — Codecov-style trusted-installer (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, **`GHA-016`**, `GHA-037` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 20 — Dependency confusion (Birsan) (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, `GHA-059`, **`NPM-001`**, **`NPM-004`** | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 21 — Matrix expansion injection (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, **`TAINT-002`** | ✅ |
| zizmor | `zizmor/artipacked`, **`zizmor/template-injection`**, `zizmor/unpinned-uses` | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | **`dangerous-write`** | ✅ |

### Scenario 22 — GCP OIDC over-broad WIF (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GHA-001`, `GHA-006`, `GHA-007`, `GHA-015`, `GHA-020`, `GHA-024`, `GHA-037`, **`GHA-062`**, `GHA-098`, `GHA-108` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | `555ab8f9-2001-455e-a077-f2d0f41e2fb9` | ❌ |
| Checkov | **`CKV_GCP_125`** | ✅ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 23 — `github-actions[bot]` branch-protection bypass (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-021`, `GHA-037`, **`GHA-049`**, `GHA-059` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 24 — Third-party webhook exfiltration (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, **`GHA-057`** | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 25 — Environment branch-pattern bypass (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, `GHA-069`, **`GHA-086`**, `GHA-098`, `GHA-108` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 26 — GitHub App token over-scope (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `AC-018`, `GHA-001`, `GHA-014`, `GHA-015`, `GHA-037`, **`GHA-061`**, `GHA-098` | ✅ |
| zizmor | `zizmor/artipacked`, **`zizmor/github-app`**, `zizmor/unpinned-uses` | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | `expression-injection` | ❌ |

### Scenario 27 — Secret leak in workflow logs (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `AC-018`, `GHA-001`, `GHA-014`, `GHA-015`, **`GHA-033`**, `GHA-037`, `GHA-098` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 28 — Reusable workflow `${{ inputs.* }}` injection (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`TAINT-003`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | `local-action` | ❌ |

### Scenario 29 — npm lifecycle-script RCE (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-021`, `GHA-037`, `GHA-059`, `NPM-001`, **`NPM-004`** | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 30 — Script injection via issue body (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`**, `GHA-004`, `GHA-015` | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | **`20f14e1a-a899-4e79-9f09-b6a84cd4649b`** | ✅ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`**, `if-cond` | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 31 — Script injection via `github.head_ref` (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`**, `GHA-015` | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`**, `if-cond` | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 32 — Script injection via commit message (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`**, `GHA-015` | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`**, `if-cond` | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 33 — Script injection via comment body (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`**, `GHA-004`, `GHA-013`, `GHA-015` | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | **`20f14e1a-a899-4e79-9f09-b6a84cd4649b`** | ✅ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`**, `if-cond` | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 34 — `ACTIONS_ALLOW_UNSECURE_COMMANDS` re-enabled (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, **`GHA-038`** | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/insecure-commands`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | **`60fd272d-15f4-4d8f-afe4-77d9c6cc0453`** | ✅ |
| Checkov | **`CKV_GHA_1`** | ✅ |
| actionlint | `deprecated-commands`, `if-cond` | ❌ |
| octoscan | **`unsecure-commands`** | ✅ |

### Scenario 35 — `cosign verify` without identity binding (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `AC-018`, `AC-032`, `GHA-001`, `GHA-014`, `GHA-015`, `GHA-037`, `GHA-098`, **`GHA-100`** | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | `555ab8f9-2001-455e-a077-f2d0f41e2fb9` | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 36 — Environment secret read without consumer binding (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `AC-033`, `GHA-014`, `GHA-015`, `GHA-019`, `GHA-033`, `GHA-057`, `GHA-098`, `GHA-108`, **`TAINT-009`** | ✅ |
| zizmor | `zizmor/template-injection` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | `dangerous-write`, `expression-injection` | ❌ |

### Scenario 37 — Confused-deputy auto-merge via bot-identity gate (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-004`, `GHA-015` | ❌ |
| zizmor | `zizmor/dangerous-triggers`, `zizmor/template-injection` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 38 — Recursive submodule checkout from PR (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-034`, `GHA-001`, `GHA-015`, `GHA-037`, `GHA-059`, `GHA-060`, **`GHA-102`** | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 39 — GitLab CI: script injection via `$CI_*` / MR vars (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GL-002`**, `GL-015` | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, `SC-003` | ❌ |

### Scenario 40 — Jenkins: `sh` string-interpolation injection (Jenkins)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`JF-002`**, `JF-003`, `JF-011`, `JF-014`, `JF-015`, `JF-028`, `JF-036` | ✅ |
| ciguard | _(none)_ | ❌ |

### Scenario 41 — GitLab: `CI_JOB_TOKEN` cross-project access (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GL-015`, **`GL-040`** | ✅ |
| Checkov | `CKV_GITLABCI_1` | ❌ |
| ciguard | `ART-003`, **`IAM-002`**, `SC-003` | ✅ |

### Scenario 42 — GitLab: untrusted `include:` (remote / mutable ref) (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GL-005`**, `GL-015` | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, **`PIPE-002`**, `SC-002`, `SC-003` | ✅ |

### Scenario 43 — GitLab: secret job on fork merge-request pipeline (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, **`GL-004`**, `GL-015` | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, **`PIPE-004`**, `RUN-003`, `SC-003` | ✅ |

### Scenario 44 — GitLab: hardcoded secret in `variables:` (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, **`GL-003`**, `GL-004`, `GL-008`, `GL-015` | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, **`IAM-001`**, `IAM-003`, `PIPE-004`, `RUN-003`, `SC-003` | ✅ |

### Scenario 45 — GitLab: `curl \| sh` in `before_script` (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GL-015`, **`GL-016`** | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, `PIPE-003`, **`SC-001`**, `SC-003` | ✅ |

### Scenario 46 — GitLab: job `image:` mutable tag (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GL-001`**, `GL-009`, `GL-015`, `GL-034` | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, `PIPE-001`, `SC-003`, **`SCA-PIN-002`** | ✅ |

### Scenario 47 — GitLab: OIDC `id_tokens` over-broad aud/sub (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GL-004`, `GL-015`, **`GL-031`** | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, `PIPE-004`, `RUN-003`, `SC-003` | ❌ |

### Scenario 48 — GitLab: untagged shared-runner + privileged dind (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GL-004`, `GL-006`, `GL-007`, `GL-015`, `GL-019`, `GL-024`, **`GL-039`** | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, **`RUN-002`**, `SC-003` | ✅ |

### Scenario 49 — Azure: macro `$(...)` injection into Bash@3 (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `ADO-001`, **`ADO-002`**, `ADO-015` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 50 — Azure: `${{ parameters }}` template injection (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`ADO-002`**, `ADO-015` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 51 — Azure: `checkout persistCredentials: true` (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `ADO-015`, **`ADO-032`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 52 — Azure: `addSpnToEnvironment` SP-secret exposure (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `ADO-001`, `ADO-015`, **`ADO-029`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 53 — Azure: `resources: repositories` untrusted ref (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `ADO-015`, **`ADO-025`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 54 — Azure: self-hosted pool for untrusted builds (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`ADO-013`**, `ADO-015` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 55 — CircleCI: orb pinned to `@volatile` (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`CC-001`**, `CC-014`, `CC-015` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 56 — CircleCI: `run:` injection via `<< pipeline.* >>` (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`CC-002`**, `CC-014`, `CC-015` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 57 — CircleCI: `machine: true` privileged executor (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `CC-006`, `CC-007`, `CC-014`, `CC-015`, `CC-020`, `CC-024`, **`CC-029`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 58 — CircleCI: docker image mutable tag (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`CC-003`**, `CC-014`, `CC-015` | ✅ |
| Checkov | **`CKV_CIRCLECIPIPELINES_1`** | ✅ |

### Scenario 59 — CircleCI: hardcoded secret in `environment:` (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, **`CC-004`**, `CC-008`, `CC-009`, `CC-013`, `CC-014`, `CC-015` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 60 — CircleCI: uncertified third-party orb (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `CC-009`, `CC-013` | ❌ |
| Checkov | _(none)_ | ❌ |

### Scenario 61 — Bitbucket: secret dumped to `artifacts:` (Mandiant) (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `BB-005`, **`BB-032`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 62 — Bitbucket: `$BITBUCKET_*` script injection (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`BB-002`**, `BB-005` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 63 — Bitbucket: `pipe:` mutable tag (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, **`BB-001`**, `BB-004`, `BB-005`, `BB-006`, `BB-007`, `BB-009`, `BB-015`, `BB-024` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 64 — Bitbucket: `image:` mutable tag (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `BB-005`, **`BB-029`**, `BB-030` | ✅ |
| Checkov | **`CKV_BITBUCKETPIPELINES_1`** | ✅ |

### Scenario 65 — Bitbucket: `clone: skip-ssl-verify: true` (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `BB-005`, **`BB-023`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 66 — Bitbucket: custom-pipeline variable injection (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, **`BB-002`**, `BB-004`, `BB-005` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 67 — Jenkins: `@Grab` sandbox-bypass (CVE-2019-1003000) (Jenkins)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `JF-011`, `JF-014`, `JF-015`, **`JF-019`** | ✅ |
| ciguard | _(none)_ | ❌ |

### Scenario 68 — Jenkins: `input` step without `submitter` (Jenkins)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `JF-011`, `JF-014`, `JF-015`, **`JF-024`**, `JF-028` | ✅ |
| ciguard | _(none)_ | ❌ |

### Scenario 69 — Jenkins: shared library on a mutable `@master` ref (Jenkins)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`JF-001`**, `JF-011`, `JF-014`, `JF-015` | ✅ |
| ciguard | _(none)_ | ❌ |

### Scenario 70 — Jenkins: `agent any` (controller exposure) (Jenkins)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`JF-003`**, `JF-011`, `JF-014`, `JF-015` | ✅ |
| ciguard | **`JKN-RUN-001`** | ✅ |

### Scenario 71 — Tekton: `$(params.*)` injected into step script (Tekton)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-023`, `TKN-002`, **`TKN-003`**, `TKN-012` | ✅ |

### Scenario 72 — Tekton: privileged / root step (Tekton)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`TKN-002`**, `TKN-012` | ✅ |

### Scenario 73 — Tekton: step `image:` not pinned to a digest (Tekton)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`TKN-001`**, `TKN-002`, `TKN-012` | ✅ |

### Scenario 74 — Argo: `{{inputs.parameters}}` injected into args (Argo Workflows)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`ARGO-005`**, `ARGO-007`, `ARGO-012` | ✅ |
| Checkov | `CKV_ARGO_2` | ❌ |

### Scenario 75 — Argo: privileged / root container (Argo Workflows)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`ARGO-002`**, `ARGO-007`, `ARGO-012` | ✅ |
| Checkov | **`CKV_ARGO_2`** | ✅ |

### Scenario 76 — Argo: default ServiceAccount + token automount (Argo Workflows)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`ARGO-003`**, `ARGO-007`, `ARGO-009`, `ARGO-010`, `ARGO-011`, `ARGO-012`, `ARGO-013` | ✅ |
| Checkov | **`CKV_ARGO_1`**, `CKV_ARGO_2` | ✅ |

### Scenario 77 — Drone: `privileged: true` step (Drone CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`DR-002`**, `DR-013`, `DR-019`, `DR-020`, `DR-021`, `DR-022` | ✅ |

### Scenario 78 — Drone: step `image:` mutable tag (Drone CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`DR-001`**, `DR-013`, `DR-022` | ✅ |

### Scenario 79 — Buildkite: `$BUILDKITE_*` command injection (Buildkite)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`BK-003`**, `BK-006`, `BK-012` | ✅ |

### Scenario 80 — Buildkite: plugin pinned to a mutable ref (Buildkite)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`BK-001`**, `BK-006`, `BK-012` | ✅ |

### Scenario 81 — Cloud Build: step image not pinned by digest (Cloud Build)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GCB-001`**, `GCB-002`, `GCB-005`, `GCB-008`, `GCB-017`, `GCB-021`, `GCB-025` | ✅ |

### Scenario 82 — Cloud Build: runs as default service account (Cloud Build)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GCB-002`**, `GCB-005`, `GCB-008`, `GCB-021`, `GCB-025` | ✅ |

### Scenario 83 — Tekton: privileged step + hostPath node escape (Tekton)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `TKN-002`, **`TKN-004`**, `TKN-012` | ✅ |

### Scenario 84 — Argo: hostPath mount → node filesystem escape (Argo Workflows)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`ARGO-004`**, `ARGO-007`, `ARGO-012` | ✅ |
| Checkov | `CKV_ARGO_2` | ❌ |

### Scenario 85 — GitLab: fork MR pipeline mints cloud OIDC token (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GL-004`, `GL-015`, **`GL-031`** | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, **`PIPE-004`**, `RUN-003`, `SC-003` | ✅ |

### Scenario 86 — Jenkins: builds untrusted fork PRs with creds (PPE) (Jenkins)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `JF-011`, `JF-014`, `JF-015`, `JF-028` | ❌ |
| ciguard | _(none)_ | ❌ |

### Scenario 87 — CircleCI: secrets passed to forked PRs (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `CC-009`, `CC-013`, `CC-014`, `CC-015`, **`CC-030`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 88 — Bitbucket: fork PR pipeline exposes secrets (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, **`BB-004`**, `BB-005` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 89 — GHA: `terraform apply` on untrusted PR (IaC RCE) (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GHA-006`, `GHA-007`, `GHA-014`, `GHA-015`, `GHA-020`, `GHA-024`, `GHA-037`, `GHA-069`, `GHA-098`, `GHA-108`, **`GHA-117`** | ✅ |
| zizmor | `zizmor/artipacked` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 90 — Azure: untrusted `resources` template on self-hosted agent (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `ADO-013`, `ADO-015`, **`ADO-025`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 91 — GitLab: `terraform apply` in a merge-request pipeline (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, **`GL-004`**, `GL-006`, `GL-007`, `GL-015`, `GL-019`, `GL-024`, `GL-041` | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, `SC-003` | ❌ |

### Scenario 92 — Argo: cluster-admin ServiceAccount → cluster takeover (Argo Workflows)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `ARGO-007`, `ARGO-009`, `ARGO-010`, `ARGO-011`, `ARGO-012`, `ARGO-013`, **`ARGO-016`** | ✅ |
| Checkov | `CKV_ARGO_2` | ❌ |

### Scenario 93 — Drone: privileged step mounts host Docker socket (Drone CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `DR-002`, **`DR-007`**, `DR-013`, `DR-022` | ✅ |

### Scenario 94 — Dockerfile: container runs as root (no USER) (Dockerfile)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`DF-002`**, `DF-007`, `DF-016`, `DF-024` | ✅ |
| KICS | `b03a748a-542d-44f4-bb86-9199ab4fd2d5`, **`fd54f200-402c-4333-a5a4-36ef6709af2f`** | ✅ |
| Checkov | `CKV_DOCKER_2`, **`CKV_DOCKER_3`** | ✅ |
| Trivy | **`DS-0002`**, `DS-0026` | ✅ |

### Scenario 95 — Dockerfile: base image unpinned (`:latest`) (Dockerfile)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`DF-001`**, `DF-007`, `DF-016` | ✅ |
| KICS | `b03a748a-542d-44f4-bb86-9199ab4fd2d5`, **`f45ea400-6bbe-4501-9fc7-1c3d75c32067`** | ✅ |
| Checkov | `CKV_DOCKER_2`, **`CKV_DOCKER_7`** | ✅ |
| Trivy | **`DS-0001`**, `DS-0026` | ✅ |

### Scenario 96 — Dockerfile: hardcoded secret in `ENV` (Dockerfile)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`DF-006`**, `DF-007`, `DF-016` | ✅ |
| KICS | `b03a748a-542d-44f4-bb86-9199ab4fd2d5` | ❌ |
| Checkov | `CKV_DOCKER_2` | ❌ |
| Trivy | `DS-0026`, **`DS-0031`** | ✅ |

### Scenario 97 — Kubernetes: privileged container (Kubernetes)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`K8S-005`**, `K8S-006`, `K8S-007`, `K8S-008`, `K8S-009`, `K8S-010`, `K8S-011`, `K8S-012`, `K8S-015`, `K8S-016`, `K8S-019`, `K8S-024`, `K8S-032`, `K8S-033` | ✅ |
| KICS | `02323c00-cdc3-4fdc-a310-4f2b3e7a1660`, `229588ef-8fde-40c8-8756-f4f2b5825ded`, `268ca686-7fb7-4ae9-b129-955a2a89064e`, `48471392-d4d0-47c0-b135-cdec95eb3eef`, `48a5beba-e4c0-4584-a2aa-e6894e4cf424`, `4a20ebac-1060-4c81-95d1-1f7f620e983b`, `4ac0e2b7-d2d2-4af7-8799-e8de6721ccda`, `5572cc5e-1e4c-4113-92a6-7a8a3bd25e6d`, `611ab018-c4aa-4ba2-b0f6-a448337509a6`, `8b36775e-183d-4d46-b0f7-96a6f34a723f`, `a659f3b5-9bf0-438a-bd9a-7d3a6427f1e3`, `a9c2f49d-0671-4fc9-9ece-f4e261e128d0`, `ade74944-a674-4e00-859e-c6eab5bde441`, `b14d1bc4-a208-45db-92f0-e21f8e2588e9`, `ca469dd4-c736-448f-8ac1-30a642705e0a`, `cf34805e-3872-4c08-bf92-6ff7bb0cfadb`, `dbbc6705-d541-43b0-b166-dd4be8208b54`, `f377b83e-bd07-4f48-a591-60c82b14a78b` | ❌ |
| Checkov | `CKV2_K8S_6`, `CKV_K8S_10`, `CKV_K8S_11`, `CKV_K8S_12`, `CKV_K8S_13`, **`CKV_K8S_16`**, `CKV_K8S_20`, `CKV_K8S_21`, `CKV_K8S_22`, `CKV_K8S_23`, `CKV_K8S_28`, `CKV_K8S_29`, `CKV_K8S_31`, `CKV_K8S_37`, `CKV_K8S_38`, `CKV_K8S_40`, `CKV_K8S_8`, `CKV_K8S_9` | ✅ |
| Trivy | `KSV-0001`, `KSV-0003`, `KSV-0004`, `KSV-0011`, `KSV-0012`, `KSV-0014`, `KSV-0015`, `KSV-0016`, **`KSV-0017`**, `KSV-0018`, `KSV-0020`, `KSV-0021`, `KSV-0030`, `KSV-0104`, `KSV-0106`, `KSV-0110`, `KSV-0118` | ✅ |

### Scenario 98 — Kubernetes: hostPath mount of node root (Kubernetes)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `K8S-006`, `K8S-007`, `K8S-008`, `K8S-009`, `K8S-010`, `K8S-011`, `K8S-012`, `K8S-013`, **`K8S-014`**, `K8S-015`, `K8S-016`, `K8S-019`, `K8S-024`, `K8S-032`, `K8S-033` | ✅ |
| KICS | `02323c00-cdc3-4fdc-a310-4f2b3e7a1660`, `229588ef-8fde-40c8-8756-f4f2b5825ded`, `268ca686-7fb7-4ae9-b129-955a2a89064e`, `48471392-d4d0-47c0-b135-cdec95eb3eef`, `48a5beba-e4c0-4584-a2aa-e6894e4cf424`, `4a20ebac-1060-4c81-95d1-1f7f620e983b`, `4ac0e2b7-d2d2-4af7-8799-e8de6721ccda`, **`5308a7a8-06f8-45ac-bf10-791fe21de46e`**, `5572cc5e-1e4c-4113-92a6-7a8a3bd25e6d`, `591ade62-d6b0-4580-b1ae-209f80ba1cd9`, `611ab018-c4aa-4ba2-b0f6-a448337509a6`, `8b36775e-183d-4d46-b0f7-96a6f34a723f`, `a659f3b5-9bf0-438a-bd9a-7d3a6427f1e3`, `a97a340a-0063-418e-b3a1-3028941d0995`, `a9c2f49d-0671-4fc9-9ece-f4e261e128d0`, `aa8f7a35-9923-4cad-bd61-a19b7f6aac91`, `ade74944-a674-4e00-859e-c6eab5bde441`, `b14d1bc4-a208-45db-92f0-e21f8e2588e9`, `ca469dd4-c736-448f-8ac1-30a642705e0a`, `cf34805e-3872-4c08-bf92-6ff7bb0cfadb`, `dbbc6705-d541-43b0-b166-dd4be8208b54`, `f377b83e-bd07-4f48-a591-60c82b14a78b` | ✅ |
| Checkov | `CKV2_K8S_6`, `CKV_K8S_10`, `CKV_K8S_11`, `CKV_K8S_12`, `CKV_K8S_13`, `CKV_K8S_20`, `CKV_K8S_21`, `CKV_K8S_22`, `CKV_K8S_23`, `CKV_K8S_28`, `CKV_K8S_29`, `CKV_K8S_30`, `CKV_K8S_31`, `CKV_K8S_37`, `CKV_K8S_38`, `CKV_K8S_40`, `CKV_K8S_8`, `CKV_K8S_9` | ❌ |
| Trivy | `KSV-0001`, `KSV-0003`, `KSV-0004`, `KSV-0011`, `KSV-0012`, `KSV-0014`, `KSV-0015`, `KSV-0016`, `KSV-0018`, `KSV-0020`, `KSV-0021`, **`KSV-0023`**, `KSV-0030`, `KSV-0104`, `KSV-0106`, `KSV-0110`, `KSV-0118`, `KSV-0121` | ✅ |

### Scenario 99 — Kubernetes: root + allowPrivilegeEscalation (Kubernetes)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `K8S-006`, `K8S-007`, `K8S-008`, `K8S-009`, `K8S-010`, `K8S-011`, `K8S-012`, `K8S-015`, `K8S-016`, `K8S-019`, `K8S-024`, `K8S-032`, `K8S-033`, **`K8S-035`** | ✅ |
| KICS | `02323c00-cdc3-4fdc-a310-4f2b3e7a1660`, `229588ef-8fde-40c8-8756-f4f2b5825ded`, `268ca686-7fb7-4ae9-b129-955a2a89064e`, `48471392-d4d0-47c0-b135-cdec95eb3eef`, `48a5beba-e4c0-4584-a2aa-e6894e4cf424`, `4a20ebac-1060-4c81-95d1-1f7f620e983b`, `4ac0e2b7-d2d2-4af7-8799-e8de6721ccda`, **`5572cc5e-1e4c-4113-92a6-7a8a3bd25e6d`**, `591ade62-d6b0-4580-b1ae-209f80ba1cd9`, `611ab018-c4aa-4ba2-b0f6-a448337509a6`, `8b36775e-183d-4d46-b0f7-96a6f34a723f`, `a659f3b5-9bf0-438a-bd9a-7d3a6427f1e3`, `a97a340a-0063-418e-b3a1-3028941d0995`, `a9c2f49d-0671-4fc9-9ece-f4e261e128d0`, `ade74944-a674-4e00-859e-c6eab5bde441`, `b14d1bc4-a208-45db-92f0-e21f8e2588e9`, `ca469dd4-c736-448f-8ac1-30a642705e0a`, `cf34805e-3872-4c08-bf92-6ff7bb0cfadb`, `dbbc6705-d541-43b0-b166-dd4be8208b54`, `f377b83e-bd07-4f48-a591-60c82b14a78b` | ✅ |
| Checkov | `CKV2_K8S_6`, `CKV_K8S_10`, `CKV_K8S_11`, `CKV_K8S_12`, `CKV_K8S_13`, **`CKV_K8S_20`**, `CKV_K8S_21`, `CKV_K8S_22`, `CKV_K8S_23`, `CKV_K8S_28`, `CKV_K8S_29`, `CKV_K8S_31`, `CKV_K8S_37`, `CKV_K8S_38`, `CKV_K8S_40`, `CKV_K8S_8`, `CKV_K8S_9` | ✅ |
| Trivy | **`KSV-0001`**, `KSV-0003`, `KSV-0004`, `KSV-0011`, `KSV-0012`, `KSV-0014`, `KSV-0015`, `KSV-0016`, `KSV-0018`, `KSV-0020`, `KSV-0021`, `KSV-0030`, `KSV-0104`, `KSV-0105`, `KSV-0106`, `KSV-0110`, `KSV-0118` | ✅ |

### Scenario 100 — Terraform: IAM policy `*:*` (full admin) (Terraform)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | `0ca1017d-3b80-423e-bb9c-6cd5898d34bd`, **`2f37c4a3-58b9-4afe-8a87-d7f1d2286f84`**, `575a2155-6af1-4026-b1af-d5bc8fe2a904`, `ba2ed23b-52d3-45ca-be25-f6c358d45abd`, `e38a8e0a-b88b-4902-b3fe-b0fcb17d5c10`, `e592a0c5-5bdb-414c-9066-5dba7cdea370` | ✅ |
| Checkov | `CKV2_AWS_40`, `CKV_AWS_286`, `CKV_AWS_287`, `CKV_AWS_288`, `CKV_AWS_289`, `CKV_AWS_290`, `CKV_AWS_355`, **`CKV_AWS_62`**, `CKV_AWS_63` | ✅ |
| Trivy | _(none)_ | ❌ |

### Scenario 101 — Terraform: security group SSH open to 0.0.0.0/0 (Terraform)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | `381c3f2a-ef6f-4eff-99f7-b169cda3422c`, `4728cd65-a20c-49da-8b31-9c08b423e4db`, `4849211b-ac39-479e-ae78-5694d506cb24`, **`65905cec-d691-4320-b320-2000436cb696`**, `cb3f5ed6-0d18-40de-a93d-b3538db31e8c`, `e38a8e0a-b88b-4902-b3fe-b0fcb17d5c10`, `e592a0c5-5bdb-414c-9066-5dba7cdea370` | ✅ |
| Checkov | `CKV2_AWS_5`, `CKV_AWS_23`, **`CKV_AWS_24`** | ✅ |
| Trivy | `AWS-0099`, **`AWS-0107`** | ✅ |

### Scenario 102 — Terraform: S3 bucket public-access-block disabled (Terraform)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | `1a4bc881-9f69-4d44-8c9a-d37d08f54c50`, `4fa66806-0dd9-4f8d-9480-3174d39c7c91`, `568a4d22-3517-44a6-a7ad-6a7eed88722c`, **`d0cc8694-fcad-43ff-ac86-32331d7e867f`**, `e38a8e0a-b88b-4902-b3fe-b0fcb17d5c10`, `e592a0c5-5bdb-414c-9066-5dba7cdea370`, `f861041c-8c9f-4156-acfc-5e6e524f5884` | ✅ |
| Checkov | `CKV2_AWS_6`, `CKV2_AWS_61`, `CKV2_AWS_62`, `CKV_AWS_144`, `CKV_AWS_145`, `CKV_AWS_18`, `CKV_AWS_21`, **`CKV_AWS_53`**, `CKV_AWS_54`, `CKV_AWS_55`, `CKV_AWS_56` | ✅ |
| Trivy | **`AWS-0086`**, `AWS-0087`, `AWS-0089`, `AWS-0090`, `AWS-0091`, `AWS-0093`, `AWS-0132` | ✅ |

### Scenario 103 — CloudFormation: S3 bucket public read+write (CloudFormation)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | `350cd468-0e2c-44ef-9d22-cfb73a62523c`, `37fa8188-738b-42c8-bf82-6334ea567738`, `38c64e76-c71e-4d92-a337-60174d1de1c9`, `4552b71f-0a2a-4bc4-92dd-ed7ec1b4674c`, **`48f100d9-f499-4c6d-b2b8-deafe47ffb26`**, `6c8d51af-218d-4bfb-94a9-94eabaa0703a`, `860ba89b-b8de-4e72-af54-d6aee4138a69`, `8d29754a-2a18-460d-a1ba-9509f8d359da`, `a227ec01-f97a-4084-91a4-47b350c1db54`, `b2e8752c-3497-4255-98d2-e4ae5b46bbf5` | ✅ |
| Checkov | `CKV_AWS_18`, **`CKV_AWS_20`**, `CKV_AWS_21`, `CKV_AWS_53`, `CKV_AWS_54`, `CKV_AWS_55`, `CKV_AWS_56`, **`CKV_AWS_57`** | ✅ |
| Trivy | **`AWS-0086`**, `AWS-0087`, `AWS-0089`, `AWS-0090`, `AWS-0091`, `AWS-0092`, `AWS-0093`, `AWS-0094`, `AWS-0132` | ✅ |

### Scenario 104 — Helm: privileged container in chart template (Helm)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `HELM-005`, `HELM-006`, **`K8S-005`**, `K8S-006`, `K8S-007`, `K8S-008`, `K8S-009`, `K8S-010`, `K8S-011`, `K8S-012`, `K8S-015`, `K8S-016`, `K8S-019`, `K8S-024`, `K8S-032`, `K8S-033` | ✅ |
| Checkov | `CKV2_K8S_6`, `CKV_K8S_10`, `CKV_K8S_11`, `CKV_K8S_12`, `CKV_K8S_13`, **`CKV_K8S_16`**, `CKV_K8S_20`, `CKV_K8S_21`, `CKV_K8S_22`, `CKV_K8S_23`, `CKV_K8S_28`, `CKV_K8S_29`, `CKV_K8S_31`, `CKV_K8S_37`, `CKV_K8S_38`, `CKV_K8S_40`, `CKV_K8S_8`, `CKV_K8S_9` | ✅ |
| Trivy | `KSV-0001`, `KSV-0003`, `KSV-0004`, `KSV-0011`, `KSV-0012`, `KSV-0014`, `KSV-0015`, `KSV-0016`, **`KSV-0017`**, `KSV-0018`, `KSV-0020`, `KSV-0021`, `KSV-0030`, `KSV-0104`, `KSV-0106`, `KSV-0110`, `KSV-0118` | ✅ |

### Scenario 105 — GHA: Codecov-style remote uploader piped to shell (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-004`, `GHA-015`, **`GHA-016`**, `GHA-037` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/excessive-permissions` | ❌ |
| poutine | **`unverified_script_exec`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | `CKV2_GHA_1` | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 106 — GitLab: `include: remote:` unpinned 3rd-party template (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GL-005`**, `GL-015` | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, **`PIPE-002`**, `SC-003` | ✅ |

### Scenario 107 — GHA: org secret handed to unpinned 3rd-party action (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `AC-018`, `GHA-001`, `GHA-004`, `GHA-014`, `GHA-015`, `GHA-037`, **`GHA-072`**, `GHA-098` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/excessive-permissions`, **`zizmor/unpinned-uses`** | ✅ |
| poutine | **`github_action_from_unverified_creator_used`** | ✅ |
| KICS | **`555ab8f9-2001-455e-a077-f2d0f41e2fb9`** | ✅ |
| Checkov | `CKV2_GHA_1` | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | `expression-injection`, **`repo-jacking`** | ✅ |

### Scenario 108 — GHA: deploy job missing environment binding (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GHA-004`, `GHA-006`, `GHA-007`, **`GHA-014`**, `GHA-015`, `GHA-020`, `GHA-024`, `GHA-037`, `GHA-098` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/excessive-permissions` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | `CKV2_GHA_1` | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 109 — GHA: self-hosted deploy without environment gate (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GHA-004`, `GHA-006`, `GHA-007`, `GHA-012`, `GHA-014`, `GHA-015`, `GHA-020`, `GHA-024`, `GHA-037`, `GHA-098`, **`GHA-112`** | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/excessive-permissions` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | `CKV2_GHA_1` | ❌ |
| actionlint | `if-cond`, `runner-label` | ❌ |
| octoscan | `runner-label` | ❌ |

### Scenario 110 — GitLab: manual deploy defaults to allow_failure (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GL-015`, **`GL-029`** | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, `DEP-002`, **`PIPE-004`**, `RUN-003`, `SC-003` | ✅ |

### Scenario 111 — Terraform: CloudTrail logging disabled / single-region (Terraform)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | `17b30f8f-8dfb-4597-adf6-57600b6cf25e`, `482b7d26-0bdb-4b5f-bf6f-545826c0a3dd`, **`4bb76f17-3d63-4529-bdca-2b454529d774`**, `52ffcfa6-6c70-4ea6-8376-d828d3961669`, `5d9e3164-9265-470c-9a10-57ae454ac0c7`, `8173d5eb-96b5-4aa6-a71b-ecfa153c123d`, `e38a8e0a-b88b-4902-b3fe-b0fcb17d5c10`, `e592a0c5-5bdb-414c-9066-5dba7cdea370` | ✅ |
| Checkov | `CKV2_AWS_10`, `CKV_AWS_251`, `CKV_AWS_252`, `CKV_AWS_35`, `CKV_AWS_36`, **`CKV_AWS_67`** | ✅ |
| Trivy | **`AWS-0014`**, `AWS-0015`, `AWS-0016`, `AWS-0162` | ✅ |

### Scenario 112 — Terraform: VPC flow logs + S3 access logging off (Terraform)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | `568a4d22-3517-44a6-a7ad-6a7eed88722c`, `e38a8e0a-b88b-4902-b3fe-b0fcb17d5c10`, `e592a0c5-5bdb-414c-9066-5dba7cdea370`, **`f83121ea-03da-434f-9277-9cd247ab3047`**, **`f861041c-8c9f-4156-acfc-5e6e524f5884`**, `fd632aaf-b8a1-424d-a4d1-0de22fd3247a` | ✅ |
| Checkov | `CKV2_AWS_11`, `CKV2_AWS_12`, `CKV2_AWS_6`, `CKV2_AWS_61`, `CKV2_AWS_62`, `CKV_AWS_144`, `CKV_AWS_145`, **`CKV_AWS_18`**, `CKV_AWS_21` | ✅ |
| Trivy | `AWS-0086`, `AWS-0087`, `AWS-0089`, `AWS-0090`, `AWS-0091`, `AWS-0093`, `AWS-0094`, `AWS-0132`, **`AWS-0178`** | ✅ |

### Scenario 113 — GitLab: `CI_DEBUG_TRACE` leaks secrets to job log (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GL-015`, **`GL-038`** | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, `SC-003` | ❌ |

### Scenario 114 — CloudFormation: security group SSH open to 0.0.0.0/0 (CloudFormation)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | `0104165b-02d5-426f-abc9-91fb48189899`, `4a1e6b34-1008-4e61-a5f2-1f7c276f8d14`, `5e6c9c68-8a82-408e-8749-ddad78cbb9c5`, **`6e856af2-62d7-4ba2-adc1-73b62cef9cc1`**, `8d29754a-2a18-460d-a1ba-9509f8d359da`, `cdbb0467-2957-4a77-9992-7b55b29df7b7` | ✅ |
| Checkov | `CKV_AWS_23`, **`CKV_AWS_24`** | ✅ |
| Trivy | **`AWS-0107`**, `AWS-0124` | ✅ |

### Scenario 115 — CloudFormation: IAM managed policy `*:*` (full admin) (CloudFormation)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | **`022f8938-4b17-420c-aca3-f917f290f322`**, `8d29754a-2a18-460d-a1ba-9509f8d359da` | ✅ |
| Checkov | `CKV_AWS_107`, `CKV_AWS_108`, **`CKV_AWS_109`**, `CKV_AWS_110`, `CKV_AWS_111` | ✅ |
| Trivy | _(none)_ | ❌ |

### Scenario 116 — CloudFormation: RDS unencrypted + publicly accessible (CloudFormation)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | `2b1d4935-9acf-48a7-8466-10d18bf51a69`, `2c161e58-cb52-454f-abea-6470c37b5e6e`, **`5beacce3-4020-4a3d-9e1d-a36f953df630`**, `8d29754a-2a18-460d-a1ba-9509f8d359da`, `9c30655c-f9a1-4296-b365-53c0bba80c76`, `9fcd0a0a-9b6f-4670-a215-d94e6bf3f184`, **`de38e1d5-54cb-4111-a868-6f7722695007`**, `e649a218-d099-4550-86a4-1231e1fcb60d`, `f0104061-8bfc-4b45-8a7d-630eb502f281`, `ffee2785-c347-451e-89f3-11aeb08e5c84` | ✅ |
| Checkov | `CKV_AWS_118`, `CKV_AWS_157`, **`CKV_AWS_16`**, `CKV_AWS_161`, **`CKV_AWS_17`** | ✅ |
| Trivy | `AWS-0077`, **`AWS-0080`**, `AWS-0133`, `AWS-0176`, `AWS-0177`, `AWS-0180` | ✅ |

### Scenario 117 — Helm: container runs as root + privilege escalation (Helm)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `HELM-005`, `HELM-006`, **`K8S-006`**, **`K8S-007`**, `K8S-008`, `K8S-009`, `K8S-010`, `K8S-011`, `K8S-012`, `K8S-015`, `K8S-016`, `K8S-019`, `K8S-024`, `K8S-032`, `K8S-033` | ✅ |
| Checkov | `CKV2_K8S_6`, `CKV_K8S_10`, `CKV_K8S_11`, `CKV_K8S_12`, `CKV_K8S_13`, **`CKV_K8S_20`**, `CKV_K8S_21`, `CKV_K8S_22`, `CKV_K8S_23`, `CKV_K8S_28`, `CKV_K8S_29`, `CKV_K8S_31`, `CKV_K8S_37`, `CKV_K8S_38`, `CKV_K8S_40`, `CKV_K8S_8`, `CKV_K8S_9` | ✅ |
| Trivy | **`KSV-0001`**, `KSV-0003`, `KSV-0004`, `KSV-0011`, `KSV-0012`, `KSV-0014`, `KSV-0015`, `KSV-0016`, `KSV-0018`, `KSV-0020`, `KSV-0021`, `KSV-0030`, `KSV-0104`, `KSV-0106`, `KSV-0110`, `KSV-0118` | ✅ |

### Scenario 118 — Helm: hostPath mount of node root in chart (Helm)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `HELM-005`, `HELM-006`, `K8S-006`, `K8S-007`, `K8S-008`, `K8S-009`, `K8S-010`, `K8S-011`, `K8S-012`, `K8S-013`, **`K8S-014`**, `K8S-015`, `K8S-016`, `K8S-019`, `K8S-024`, `K8S-032`, `K8S-033` | ✅ |
| Checkov | `CKV2_K8S_6`, `CKV_K8S_10`, `CKV_K8S_11`, `CKV_K8S_12`, `CKV_K8S_13`, `CKV_K8S_20`, `CKV_K8S_21`, `CKV_K8S_22`, `CKV_K8S_23`, `CKV_K8S_28`, `CKV_K8S_29`, `CKV_K8S_30`, `CKV_K8S_31`, `CKV_K8S_37`, `CKV_K8S_38`, `CKV_K8S_40`, `CKV_K8S_8`, `CKV_K8S_9` | ❌ |
| Trivy | `KSV-0001`, `KSV-0003`, `KSV-0004`, `KSV-0011`, `KSV-0012`, `KSV-0014`, `KSV-0015`, `KSV-0016`, `KSV-0018`, `KSV-0020`, `KSV-0021`, **`KSV-0023`**, `KSV-0030`, `KSV-0104`, `KSV-0106`, `KSV-0110`, `KSV-0118`, `KSV-0121` | ✅ |

### Scenario 119 — Terraform: S3 bucket unencrypted + unversioned (Terraform)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | **`568a4d22-3517-44a6-a7ad-6a7eed88722c`**, `e38a8e0a-b88b-4902-b3fe-b0fcb17d5c10`, `e592a0c5-5bdb-414c-9066-5dba7cdea370`, `f861041c-8c9f-4156-acfc-5e6e524f5884` | ✅ |
| Checkov | `CKV2_AWS_6`, `CKV2_AWS_61`, `CKV2_AWS_62`, `CKV_AWS_144`, **`CKV_AWS_145`**, `CKV_AWS_18`, `CKV_AWS_21` | ✅ |
| Trivy | `AWS-0086`, `AWS-0087`, `AWS-0089`, `AWS-0090`, `AWS-0091`, `AWS-0093`, `AWS-0094`, **`AWS-0132`** | ✅ |

### Scenario 120 — Terraform: RDS publicly accessible + unencrypted (Terraform)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| KICS | **`08bd0760-8752-44e1-9779-7bb369b2b4e4`**, `1dc73fb4-5b51-430c-8c5f-25dcf9090b02`, `2a153952-2544-4687-bcc9-cc8fea814a9b`, **`35113e6f-2c6b-414d-beec-7a9482d3b2d1`**, `6d3dead4-c6b2-4db7-81bd-3a83eae8f255`, `88fd05e0-ac0e-43d2-ba6d-fc0ba60ae1a6`, `8d7f7b8c-6c7c-40f8-baa6-62006c6c7b56`, `e38a8e0a-b88b-4902-b3fe-b0fcb17d5c10`, `e592a0c5-5bdb-414c-9066-5dba7cdea370` | ✅ |
| Checkov | `CKV2_AWS_30`, `CKV2_AWS_60`, `CKV_AWS_118`, `CKV_AWS_129`, `CKV_AWS_157`, **`CKV_AWS_16`**, `CKV_AWS_161`, **`CKV_AWS_17`**, `CKV_AWS_226`, `CKV_AWS_293`, `CKV_AWS_353` | ✅ |
| Trivy | `AWS-0077`, **`AWS-0080`**, `AWS-0133`, `AWS-0176`, `AWS-0177`, `AWS-0180` | ✅ |

### Scenario 121 — GHA: untrusted context -> agentic AI CLI (prompt injection) (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-035`, `GHA-003`, `GHA-004`, `GHA-013`, `GHA-015`, `GHA-037`, `GHA-103`, `GHA-106`, **`GHA-119`** | ✅ |
| zizmor | `zizmor/artipacked` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 122 — GHA: ML model `trust_remote_code=True` (code execution) (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-015`, `GHA-021`, `GHA-037`, `GHA-060`, **`GHA-120`**, `GHA-121` | ✅ |
| zizmor | `zizmor/artipacked` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 123 — Bitbucket: `terraform apply` on a pull-request pipeline (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `BB-004`, `BB-005`, `BB-006`, `BB-007`, `BB-015`, `BB-024`, `BB-028`, **`BB-033`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 124 — Bitbucket: production deploy on a pull-request pipeline (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `BB-005`, **`BB-034`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 125 — GitLab: native security scanner explicitly disabled (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `GL-004`, `GL-015`, **`GL-043`** | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, `IAM-003`, `PIPE-004`, `RUN-003`, `SC-003` | ❌ |

### Scenario 126 — GitLab: auto production deploy on a merge-request pipeline (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GL-015`, **`GL-044`** | ✅ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, `DEP-001`, `DEP-003`, `RUN-003`, `SC-003` | ❌ |

### Scenario 127 — Azure: IaC apply on a PR-validated pipeline (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `ADO-004`, `ADO-006`, `ADO-007`, `ADO-015`, `ADO-020`, `ADO-024`, **`ADO-033`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 128 — Jenkins: shell step interpolates `params.*` (injection) (Jenkins)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `JF-003`, `JF-006`, `JF-007`, `JF-011`, `JF-015`, `JF-020`, `JF-028`, **`JF-036`** | ✅ |
| ciguard | `JKN-RUN-001` | ❌ |

### Scenario 129 — Drone: dangerous shell idiom (`eval`/`sh -c`) in command (Drone CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `DR-013`, **`DR-017`**, `DR-022` | ✅ |

### Scenario 130 — Buildkite: dangerous shell idiom (`eval`/`sh -c`) in command (Buildkite)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `BK-006`, `BK-012`, **`BK-016`** | ✅ |

### Scenario 131 — Cloud Build: config has indicators of malicious activity (Cloud Build)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GCB-001`, `GCB-002`, `GCB-005`, `GCB-008`, `GCB-021`, `GCB-025`, **`GCB-027`** | ✅ |

### Scenario 132 — PyPI: dependency confusion via `--extra-index-url` (PyPI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `PYPI-001`, **`PYPI-002`**, **`PYPI-005`** | ✅ |

### Scenario 133 — PyPI: plain-HTTP index + TLS verification disabled (PyPI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `PYPI-002`, **`PYPI-003`**, **`PYPI-011`** | ✅ |

### Scenario 134 — PyPI: floating `build-system.requires` + HTTP source (PyPI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`PYPI-012`**, **`PYPI-014`** | ✅ |

### Scenario 135 — Maven: plain-HTTP repository + mutable `SNAPSHOT` (Maven)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`MVN-002`**, **`MVN-003`**, `MVN-005` | ✅ |

### Scenario 136 — Maven: build plugin bound to lifecycle (build-time RCE) (Maven)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`MVN-015`** | ✅ |

### Scenario 137 — NuGet: plain-HTTP feed + private feed without `<clear/>` (NuGet)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`NUGET-004`**, `NUGET-012`, **`NUGET-016`** | ✅ |

### Scenario 138 — NuGet: multiple sources without `packageSourceMapping` (NuGet)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`NUGET-007`**, `NUGET-012`, `NUGET-017` | ✅ |

### Scenario 139 — Cargo: git dep on a mutable ref + compile-time `build.rs` (Cargo)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `CARGO-001`, **`CARGO-002`**, `CARGO-003`, `CARGO-010`, **`CARGO-011`**, `CARGO-014` | ✅ |

### Scenario 140 — Cargo: alternate registry + `.cargo/config.toml` override (Cargo)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `CARGO-001`, `CARGO-003`, **`CARGO-005`**, `CARGO-010`, **`CARGO-012`**, `CARGO-014` | ✅ |

### Scenario 141 — Go modules: `replace` substitution + missing `go.sum` (Go modules)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GOMOD-001`**, **`GOMOD-003`** | ✅ |

### Scenario 142 — Go modules: non-canonical host (bare IP / host:port) (Go modules)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GOMOD-001`, `GOMOD-003`, **`GOMOD-012`** | ✅ |

### Scenario 143 — Composer: `scripts` hook pipes a remote download to a shell (Composer)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `COMPOSER-001`, `COMPOSER-002`, **`COMPOSER-006`**, **`COMPOSER-008`** | ✅ |

### Scenario 144 — Composer: plain-HTTP repository + `secure-http: false` (Composer)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `COMPOSER-001`, `COMPOSER-002`, **`COMPOSER-003`**, **`COMPOSER-010`**, `COMPOSER-011` | ✅ |

### Scenario 145 — OCI: foreign-layer URL + legacy `schemaVersion 1` (OCI / SLSA)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `OCI-001`, `OCI-002`, `OCI-003`, **`OCI-004`**, `OCI-005`, **`OCI-007`**, `OCI-009` | ✅ |

### Scenario 146 — OCI: SLSA provenance attests untrusted builder + unbound subject (OCI / SLSA)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`ATTEST-001`**, `ATTEST-002`, `ATTEST-004`, **`ATTEST-005`**, `OCI-001`, `OCI-003`, `OCI-005`, `OCI-009` | ✅ |

### Scenario 147 — Argo CD: wildcard RBAC policy + anonymous access (Argo CD)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-030`, **`ARGOCD-004`**, **`ARGOCD-009`** | ✅ |

### Scenario 148 — Argo CD: web terminal enabled (`exec.enabled`) (Argo CD)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`ARGOCD-014`** | ✅ |

### Scenario 149 — Argo CD: plaintext repo credentials + any-source AppProject (Argo CD)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`ARGOCD-001`**, `ARGOCD-002`, **`ARGOCD-005`** | ✅ |
<!-- /AUTOGEN:rule-firings -->
