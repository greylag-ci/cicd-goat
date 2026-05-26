# The full matrix

Per-scenario verdicts for every scanner in the comparison. Auto-generated
from the latest successful
[`scanner-comparison`](../../../actions/workflows/scanner-comparison.yml)
run on `main` by [`tools/regen-readme.py`](../tools/regen-readme.py),
driven by [`tools/scenarios.yaml`](../tools/scenarios.yaml).

Rebuild locally: see [CONTRIBUTING.md → Regenerate the stats](../CONTRIBUTING.md#regenerate-the-stats).

| key | meaning                                                  |
| :-: | :------------------------------------------------------- |
| ✅  | scanner flags the **canonical bug** with a matching rule |
| ⚠️  | scanner partially catches — adjacent rule, half the antipattern, or related but distinct concern |
| ❌  | scanner misses the canonical bug                         |
| —   | not applicable to that scanner's class                   |

<!-- AUTOGEN:matrix -->
| #  | Scenario | pipeline&#x2011;check | zizmor | poutine | KICS | Checkov | actionlint | octoscan |
| :-:| :--- | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 01 | `pull_request_target` + fork-head checkout | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ |
| 02 | Script injection via issue title | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 03 | Action pinned to mutable ref | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 04 | `GITHUB_TOKEN` `write-all` | ✅ | ❌ | ❌ | ❌ | ✅ | ❌ | ❌ |
| 05 | Cache poisoning via PR title | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 06 | Reusable workflow `secrets: inherit` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 07 | `workflow_run` artifact RCE | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 08 | Self-hosted runner on public repo | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ✅ |
| 09 | Container image `:latest` | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 10 | AWS OIDC wildcard `sub` | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 11 | `pip install` no hashes | ✅ | — | ❌ | ❌ | ❌ | ❌ | ❌ |
| 12 | `persist-credentials` leak | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| 13 | `workflow_dispatch` input injection | ✅ | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ |
| 14 | `$GITHUB_ENV` poisoning | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| 15 | Hardcoded secret in `env:` | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| 16 | `curl \| sh` install | ✅ | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ |
| 17 | ArtiPACKED — `.git/` in artifact | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ✅ |
| 18 | Composite action `${{ inputs.* }}` injection | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| 19 | Codecov-style trusted-installer | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 20 | Dependency confusion (Birsan) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 21 | Matrix expansion injection | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 22 | GCP OIDC over-broad WIF | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 23 | `github-actions[bot]` branch-protection bypass | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 24 | Third-party webhook exfiltration | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 25 | Environment branch-pattern bypass | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 26 | GitHub App token over-scope | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 27 | Secret leak in workflow logs | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 28 | Reusable workflow `${{ inputs.* }}` injection | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 29 | npm lifecycle-script RCE | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| 30 | Script injection via issue body | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| 31 | Script injection via `github.head_ref` | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| 32 | Script injection via commit message | ✅ | ✅ | ✅ | ❌ | ✅ | ✅ | ✅ |
| 33 | Script injection via comment body | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
|    | **canonical bugs caught** | **31 ✅** | **16 ✅** | **12 ✅** | **6 ✅** | **8 ✅** | **6 ✅** | **10 ✅** |
<!-- /AUTOGEN:matrix -->

> [!IMPORTANT]
> The hard cases — multi-file scope (10, 22), network-egress reasoning
> (16, 19, 24), sibling-manifest analysis (11, 20, 29), and
> GitHub-settings-level configuration that doesn't appear in any file
> (23, 25, 27) — collapse to *solo catches by one scanner* on the
> current matrix. See [COVERAGE-AXES § ③](COVERAGE-AXES.md#-solo-catches)
> for the live solo-catches list, autogen'd from the same SARIF as the
> matrix above. Their primary value here is as a target for the *next*
> generation of rules across the field.

---

## Scenarios index

<!-- AUTOGEN:scenarios-index -->
| #  | Title | CICD-SEC | Severity |
| :-:| :--- | :-: | :-- |
| 01 | [`pull_request_target` + fork-head checkout](../scenarios/01-prtarget-checkout-head/README.md) | 4 · 5 | 🔴 critical |
| 02 | [Script injection via issue title](../scenarios/02-script-injection-issue-title/README.md) | 4 | 🟠 high |
| 03 | [Action pinned to mutable ref](../scenarios/03-action-mutable-ref/README.md) | 3 | 🟠 high |
| 04 | [`GITHUB_TOKEN` `write-all`](../scenarios/04-github-token-write-all/README.md) | 5 | 🟡 medium |
| 05 | [Cache poisoning via PR title](../scenarios/05-cache-poisoning-pr-controlled/README.md) | 4 · 9 | 🟠 high |
| 06 | [Reusable workflow `secrets: inherit`](../scenarios/06-reusable-secrets-inherit/README.md) | 5 · 6 | 🟡 medium |
| 07 | [`workflow_run` artifact RCE](../scenarios/07-workflow-run-artifact-rce/README.md) | 4 · 9 | 🔴 critical |
| 08 | [Self-hosted runner on public repo](../scenarios/08-self-hosted-public-fork/README.md) | 7 | 🔴 critical |
| 09 | [Container image `:latest`](../scenarios/09-container-image-latest/README.md) | 3 · 9 | 🟡 medium |
| 10 | [AWS OIDC wildcard `sub`](../scenarios/10-oidc-aws-wildcard-sub/README.md) | 2 · 7 | 🔴 critical |
| 11 | [`pip install` no hashes](../scenarios/11-pip-install-no-hashes/README.md) | 3 | 🟡 medium |
| 12 | [`persist-credentials` leak](../scenarios/12-persist-credentials-leak/README.md) | 6 · 3 | 🟠 high |
| 13 | [`workflow_dispatch` input injection](../scenarios/13-input-injection-workflow-dispatch/README.md) | 4 | 🟠 high |
| 14 | [`$GITHUB_ENV` poisoning](../scenarios/14-env-injection-pr-body/README.md) | 4 | 🟠 high |
| 15 | [Hardcoded secret in `env:`](../scenarios/15-hardcoded-secret-env/README.md) | 6 | 🟠 high |
| 16 | [`curl \| sh` install](../scenarios/16-curl-pipe-sh/README.md) | 3 | 🟡 medium |
| 17 | [ArtiPACKED — `.git/` in artifact](../scenarios/17-artipacked-git-dir/README.md) | 6 · 9 | 🔴 critical |
| 18 | [Composite action `${{ inputs.* }}` injection](../scenarios/18-composite-action-input-injection/README.md) | 4 | 🟠 high |
| 19 | [Codecov-style trusted-installer](../scenarios/19-codecov-style-installer/README.md) | 3 · 9 | 🔴 critical |
| 20 | [Dependency confusion (Birsan)](../scenarios/20-dependency-confusion/README.md) | 3 | 🔴 critical |
| 21 | [Matrix expansion injection](../scenarios/21-matrix-expansion-injection/README.md) | 4 | 🟠 high |
| 22 | [GCP OIDC over-broad WIF](../scenarios/22-gcp-oidc-broad-wif/README.md) | 2 · 7 | 🔴 critical |
| 23 | [`github-actions[bot]` branch-protection bypass](../scenarios/23-actions-bot-branch-protection-bypass/README.md) | 1 | 🟠 high |
| 24 | [Third-party webhook exfiltration](../scenarios/24-third-party-webhook-exfil/README.md) | 8 | 🟠 high |
| 25 | [Environment branch-pattern bypass](../scenarios/25-environment-branch-pattern-bypass/README.md) | 1 · 5 | 🟠 high |
| 26 | [GitHub App token over-scope](../scenarios/26-app-token-over-scope/README.md) | 5 | 🟡 medium |
| 27 | [Secret leak in workflow logs](../scenarios/27-secret-leak-in-logs/README.md) | 10 | 🟠 high |
| 28 | [Reusable workflow `${{ inputs.* }}` injection](../scenarios/28-reusable-workflow-input-injection/README.md) | 4 | 🟠 high |
| 29 | [npm lifecycle-script RCE](../scenarios/29-npm-lifecycle-script-rce/README.md) | 3 | 🔴 critical |
| 30 | [Script injection via issue body](../scenarios/30-script-injection-issue-body/README.md) | 4 | 🟠 high |
| 31 | [Script injection via `github.head_ref`](../scenarios/31-script-injection-head-ref/README.md) | 4 | 🟠 high |
| 32 | [Script injection via commit message](../scenarios/32-script-injection-commit-message/README.md) | 4 | 🟠 high |
| 33 | [Script injection via comment body](../scenarios/33-script-injection-comment-body/README.md) | 4 | 🟠 high |
<!-- /AUTOGEN:scenarios-index -->

> [!NOTE]
> **Full OWASP CICD-SEC top 10 coverage** — every category 1 through 10
> has at least one scenario. See
> [`scenarios/README.md`](../scenarios/README.md#owasp-cicd-sec-top-10--full-coverage)
> for the per-category mapping.

Each scenario has a writeup at `scenarios/NN-*/README.md` with the
exploitation walkthrough, the per-scanner coverage notes, and the fix.
