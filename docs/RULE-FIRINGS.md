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
| pipeline&#x2011;check | `GHA-001`, **`GHA-004`**, `GHA-015`, `GHA-037`, `GHA-059`, `GHA-069` | ✅ |
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
| pipeline&#x2011;check | `GHA-001`, **`GHA-012`**, `GHA-015`, `GHA-037`, `GHA-059` | ✅ |
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
| pipeline&#x2011;check | `AC-005`, `GHA-001`, `GHA-006`, `GHA-007`, `GHA-015`, `GHA-020`, `GHA-024`, `GHA-037`, **`GHA-062`**, `GHA-098` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | `555ab8f9-2001-455e-a077-f2d0f41e2fb9` | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 11 — `pip install` no hashes (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, **`GHA-060`** | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | — |
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
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, `GHA-059` | ❌ |
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
| pipeline&#x2011;check | `AC-005`, `GHA-001`, `GHA-006`, `GHA-007`, `GHA-015`, `GHA-020`, `GHA-024`, `GHA-037`, **`GHA-062`**, `GHA-098` | ✅ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | `555ab8f9-2001-455e-a077-f2d0f41e2fb9` | ❌ |
| Checkov | `CKV_GCP_125` | ❌ |
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
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, `GHA-069`, **`GHA-086`**, `GHA-098` | ✅ |
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
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-021`, `GHA-037`, `GHA-059` | ❌ |
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
| pipeline&#x2011;check | `GHA-001`, `GHA-015`, `GHA-037`, `GHA-038` | ❌ |
| zizmor | `zizmor/artipacked`, `zizmor/insecure-commands`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | **`60fd272d-15f4-4d8f-afe4-77d9c6cc0453`** | ✅ |
| Checkov | **`CKV_GHA_1`** | ✅ |
| actionlint | `deprecated-commands`, `if-cond` | ❌ |
| octoscan | **`unsecure-commands`** | ✅ |

### Scenario 35 — `cosign verify` without identity binding (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `AC-018`, `AC-032`, `GHA-001`, `GHA-014`, `GHA-015`, `GHA-037`, `GHA-098`, `GHA-100` | ❌ |
| zizmor | `zizmor/artipacked`, `zizmor/unpinned-uses` | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | `555ab8f9-2001-455e-a077-f2d0f41e2fb9` | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | `if-cond` | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 36 — Environment secret read without consumer binding (GitHub Actions)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `AC-033`, `GHA-014`, `GHA-015`, `GHA-019`, `GHA-033`, `GHA-057`, `GHA-098`, `TAINT-009` | ❌ |
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
| pipeline&#x2011;check | `AC-034`, `GHA-001`, `GHA-015`, `GHA-037`, `GHA-059`, `GHA-060`, `GHA-102` | ❌ |
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
| pipeline&#x2011;check | **`JF-002`**, `JF-003`, `JF-011`, `JF-014`, `JF-015`, `JF-016`, `JF-028` | ✅ |
| ciguard | _(none)_ | ❌ |

### Scenario 41 — GitLab: `CI_JOB_TOKEN` cross-project access (GitLab CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `GL-015` | ❌ |
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
| pipeline&#x2011;check | `AC-005`, `GL-004`, `GL-006`, `GL-007`, `GL-015`, `GL-019`, `GL-024` | ❌ |
| Checkov | _(none)_ | ❌ |
| ciguard | `ART-003`, **`RUN-002`**, `SC-003` | ✅ |

### Scenario 49 — Azure: macro `$(...)` injection into Bash@3 (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `ADO-001`, `ADO-015` | ❌ |
| Checkov | _(none)_ | ❌ |

### Scenario 50 — Azure: `${{ parameters }}` template injection (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `ADO-015` | ❌ |
| Checkov | _(none)_ | ❌ |

### Scenario 51 — Azure: `checkout persistCredentials: true` (Azure Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `ADO-015` | ❌ |
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
| pipeline&#x2011;check | **`CC-001`**, `CC-011`, `CC-014`, `CC-015` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 56 — CircleCI: `run:` injection via `<< pipeline.* >>` (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `CC-011`, `CC-014`, `CC-015` | ❌ |
| Checkov | _(none)_ | ❌ |

### Scenario 57 — CircleCI: `machine: true` privileged executor (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `CC-006`, `CC-007`, `CC-011`, `CC-014`, `CC-015`, `CC-020`, `CC-024`, **`CC-029`** | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 58 — CircleCI: docker image mutable tag (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`CC-003`**, `CC-011`, `CC-014`, `CC-015` | ✅ |
| Checkov | **`CKV_CIRCLECIPIPELINES_1`** | ✅ |

### Scenario 59 — CircleCI: hardcoded secret in `environment:` (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, **`CC-004`**, `CC-008`, `CC-009`, `CC-011`, `CC-013`, `CC-014`, `CC-015` | ✅ |
| Checkov | _(none)_ | ❌ |

### Scenario 60 — CircleCI: uncertified third-party orb (CircleCI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `CC-009`, `CC-011`, `CC-013`, `CC-015` | ❌ |
| Checkov | _(none)_ | ❌ |

### Scenario 61 — Bitbucket: secret dumped to `artifacts:` (Mandiant) (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `BB-005` | ❌ |
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
| pipeline&#x2011;check | `BB-005`, `BB-030` | ❌ |
| Checkov | **`CKV_BITBUCKETPIPELINES_1`** | ✅ |

### Scenario 65 — Bitbucket: `clone: skip-ssl-verify: true` (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `BB-005` | ❌ |
| Checkov | _(none)_ | ❌ |

### Scenario 66 — Bitbucket: custom-pipeline variable injection (Bitbucket Pipelines)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `AC-005`, `BB-004`, `BB-005` | ❌ |
| Checkov | _(none)_ | ❌ |

### Scenario 67 — Jenkins: `@Grab` sandbox-bypass (CVE-2019-1003000) (Jenkins)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `JF-011`, `JF-014`, `JF-015`, **`JF-019`** | ✅ |
| ciguard | _(none)_ | ❌ |

### Scenario 68 — Jenkins: `input` step without `submitter` (Jenkins)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | `JF-011`, `JF-014`, `JF-015`, `JF-024`, `JF-028` | ❌ |
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
| pipeline&#x2011;check | `TKN-002`, `TKN-012` | ❌ |

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
| pipeline&#x2011;check | **`DR-002`** | ✅ |

### Scenario 78 — Drone: step `image:` mutable tag (Drone CI)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`DR-001`** | ✅ |

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
<!-- /AUTOGEN:rule-firings -->
