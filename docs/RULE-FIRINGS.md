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
  [FIELD-TEST.md § ⑤](FIELD-TEST.md#-the-hygiene-baseline--a-scope-difference-not-a-coverage-one)
  for the absence-of-control rule family.
- _(none)_ = scanner emitted nothing on this workflow file.
- The **Verdict** column is the same as the [main matrix](MATRIX.md)
  cell: ✅ if every canonical-bug rule fired, ⚠️ if some, ❌ if none,
  — if not applicable.

Same source as the main matrix — auto-rebuilt from the latest
`scanner-comparison` SARIF on `main`.

---

<!-- AUTOGEN:rule-firings -->
### Scenario 01 — `pull_request_target` + fork-head checkout

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-002`**, **`GHA-044`** | ✅ |
| zizmor | **`zizmor/dangerous-triggers`** | ✅ |
| poutine | **`untrusted_checkout_exec`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | **`dangerous-checkout`** | ✅ |

### Scenario 02 — Script injection via issue title

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | **`20f14e1a-a899-4e79-9f09-b6a84cd4649b`** | ✅ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 03 — Action pinned to mutable ref

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-001`** | ✅ |
| zizmor | **`zizmor/unpinned-uses`** | ✅ |
| poutine | **`github_action_from_unverified_creator_used`** | ✅ |
| KICS | **`555ab8f9-2001-455e-a077-f2d0f41e2fb9`** | ✅ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 04 — `GITHUB_TOKEN` `write-all`

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-004`** | ✅ |
| zizmor | **`zizmor/excessive-permissions`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | **`CKV2_GHA_1`** | ✅ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 05 — Cache poisoning via PR title

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-011`**, **`GHA-052`** | ✅ |
| zizmor | **`zizmor/cache-poisoning`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 06 — Reusable workflow `secrets: inherit`

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-034`** | ✅ |
| zizmor | **`zizmor/secrets-inherit`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 07 — `workflow_run` artifact RCE

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-009`**, **`GHA-032`** | ✅ |
| zizmor | **`zizmor/dangerous-triggers`** | ✅ |
| poutine | **`known_vulnerability_in_build_component`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | **`dangerous-checkout`** | ✅ |

### Scenario 08 — Self-hosted runner on public repo

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-012`** | ✅ |
| zizmor | **`zizmor/self-hosted-runner`** | ✅ |
| poutine | **`pr_runs_on_self_hosted`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | **`runner-label`** | ✅ |

### Scenario 09 — Container image `:latest`

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-051`** | ✅ |
| zizmor | **`zizmor/unpinned-images`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 10 — AWS OIDC wildcard `sub`

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-062`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 11 — `pip install` no hashes

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-060`** | ✅ |
| zizmor | _(none)_ | — |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 12 — `persist-credentials` leak

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-037`** | ✅ |
| zizmor | **`zizmor/artipacked`** | ✅ |
| poutine | **`github_action_from_unverified_creator_used`** | ✅ |
| KICS | **`555ab8f9-2001-455e-a077-f2d0f41e2fb9`** | ✅ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 13 — `workflow_dispatch` input injection

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | **`CKV_GHA_7`** | ✅ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 14 — `$GITHUB_ENV` poisoning

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`dangerous-write`** | ✅ |

### Scenario 15 — Hardcoded secret in `env:`

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-008`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | **`487f4be7-3fd9-4506-a07a-eae252180c08`**, **`baee238e-1921-4801-9c3f-79ae1d7b2cbc`** | ✅ |
| Checkov | **`CKV_GHA_3`** | ✅ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 16 — `curl \| sh` install

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-016`** | ✅ |
| zizmor | **`zizmor/unverified-script-download`** | ✅ |
| poutine | **`unverified_script_exec`** | ✅ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 17 — ArtiPACKED — `.git/` in artifact

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-019`**, **`GHA-037`** | ✅ |
| zizmor | **`zizmor/artipacked`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | **`dangerous-artefact`** | ✅ |

### Scenario 18 — Composite action `${{ inputs.* }}` injection

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 19 — Codecov-style trusted-installer

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-016`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 20 — Dependency confusion (Birsan)

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`NPM-001`**, **`NPM-004`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 21 — Matrix expansion injection

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`TAINT-002`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 22 — GCP OIDC over-broad WIF

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-062`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 23 — `github-actions[bot]` branch-protection bypass

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-049`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 24 — Third-party webhook exfiltration

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-057`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | **`CKV_GHA_3`** | ✅ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 25 — Environment branch-pattern bypass

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-086`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 26 — GitHub App token over-scope

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-061`** | ✅ |
| zizmor | **`zizmor/github-app`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 27 — Secret leak in workflow logs

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-033`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 28 — Reusable workflow `${{ inputs.* }}` injection

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`TAINT-003`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 29 — npm lifecycle-script RCE

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`NPM-004`** | ✅ |
| zizmor | _(none)_ | ❌ |
| poutine | _(none)_ | ❌ |
| KICS | _(none)_ | ❌ |
| Checkov | _(none)_ | ❌ |
| actionlint | _(none)_ | ❌ |
| octoscan | _(none)_ | ❌ |

### Scenario 30 — Script injection via issue body

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | **`20f14e1a-a899-4e79-9f09-b6a84cd4649b`** | ✅ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 31 — Script injection via `github.head_ref`

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | **`20f14e1a-a899-4e79-9f09-b6a84cd4649b`** | ✅ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 32 — Script injection via commit message

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | **`20f14e1a-a899-4e79-9f09-b6a84cd4649b`** | ✅ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`expression-injection`** | ✅ |

### Scenario 33 — Script injection via comment body

| Scanner | Rules fired | Verdict |
| :-- | :-- | :-: |
| pipeline&#x2011;check | **`GHA-003`** | ✅ |
| zizmor | **`zizmor/template-injection`** | ✅ |
| poutine | **`injection`** | ✅ |
| KICS | **`20f14e1a-a899-4e79-9f09-b6a84cd4649b`** | ✅ |
| Checkov | **`CKV_GHA_2`** | ✅ |
| actionlint | **`expression`** | ✅ |
| octoscan | **`expression-injection`** | ✅ |
<!-- /AUTOGEN:rule-firings -->
