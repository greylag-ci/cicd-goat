# Field test — five cinematic scenarios

Five scenarios that show where the scanners agree, where they disagree,
and where they all fall over. Picked for didactic value, not to flatter
any one tool. The full per-scenario table is in [MATRIX.md](MATRIX.md).

> [!NOTE]
> **Scoring methodology.** A scanner gets ✅ on a scenario only if it
> emits a rule whose description names the *specific canonical bug*
> for that scenario. Hygiene findings that fire on every workflow file
> (missing SBOM, unpinned `actions/checkout@v4`, no `timeout-minutes`,
> etc.) don't count toward ✅ on a scenario whose canonical bug is
> something else — they're the same finding on every file and tell
> you nothing comparative. Pipeline-check carries a wide hygiene
> baseline that the field doesn't ship; that's a separate, real
> differentiator covered in [§ ⑤](#-the-hygiene-baseline--a-scope-difference-not-a-coverage-one).

---

## ① The `tj-actions` tag move &nbsp;·&nbsp; scenario 03

> [!NOTE]
> **CICD-SEC-3 · Dependency Chain Abuse · CVE-2025-30066.** On March 14, 2025
> the `tj-actions/changed-files` GitHub Action was compromised; the
> injected code dumped Runner Worker memory (including secrets) into the
> workflow log. Over **23,000 repositories** ran the malicious version
> before the rollback. Pinning to a tag instead of a SHA was the whole bug.

```yaml
# .github/workflows/scenario-03-action-mutable-ref.yml
- uses: third-party-org/some-deploy-action@main       # ← branch ref
- uses: another-org/composite@master                   # ← branch ref
- uses: yet-another-org/widget-action@v1               # ← movable tag
```

| scanner            | verdict | rule that fired                                                          |
| :----------------- | :-----: | :----------------------------------------------------------------------- |
| **pipeline-check** |   ✅    | `GHA-001` — _Action not pinned to commit SHA: 4 refs (actions/checkout@v4, third-party-org/..., another-org/..., yet-another-org/...)_ |
| zizmor             |   ✅    | `unpinned-uses`                                                          |
| KICS               |   ✅    | `555ab8f9-…` — _Unpinned Actions Full Length Commit SHA_                 |
| poutine            |   ✅    | `github_action_from_unverified_creator_used` — routes through creator trust, not SHA pinning, but still flags the action for review |
| Checkov            |   ❌    | —                                                                        |
| actionlint         |   ❌    | — _generalist linter; no unpinned-action rule_                           |
| octoscan           |   ❌    | — _`dangerous-action` targets untrusted-artifact misuse, not mutable refs; `repo-jacking` only fires when the referenced org doesn't exist_ |

---

## ② AWS OIDC trust policy with `sub: repo:*` &nbsp;·&nbsp; scenario 10

> [!NOTE]
> **CICD-SEC-2 · Inadequate IAM.** A trust policy with a wildcard subject
> lets *any* GitHub repository assume your production role. The bug
> lives in two files (workflow + IAM trust JSON) and no single scanner
> here covers both ends.

```yaml
# .github/workflows/scenario-10-oidc-aws-wildcard-sub.yml
- uses: aws-actions/configure-aws-credentials@v4
  with:
    role-to-assume: arn:aws:iam::123456789012:role/example-overly-broad
```
```json
// scenarios/10-oidc-aws-wildcard-sub/trust-policy.json
"Condition": {
  "StringLike": {
    "token.actions.githubusercontent.com:sub": "repo:*"
  }
}
```

| scanner            | sees workflow                                                                  | sees trust-policy.json |
| :----------------- | :----------------------------------------------------------------------------- | :--------------------: |
| **pipeline-check** | ✅&nbsp;`GHA-062` walks the workflow's repo for `*trust-polic*.json`, parses the trust policy directly, and flags `StringLike :sub` values that match more than one repo | (caught via the workflow lane) |
| zizmor             | ❌                                                                              | ❌                     |
| poutine            | ❌                                                                              | ❌                     |
| KICS               | ❌&nbsp;_Catches `aws-actions/...@v4` as unpinned action; misses the wildcard sub_ | ❌                     |
| Checkov            | ❌                                                                              | ❌                     |
| actionlint         | ❌                                                                              | ❌                     |
| octoscan           | ❌&nbsp;_no rule walks sibling JSON / Terraform; `debug-oidc-action` only notes that the step uses OIDC_ | ❌                     |

> **Pipeline-check is the only scanner here that crosses scopes for
> this scenario.** GHA-062 was added in the v1.3 cycle precisely for
> cicd-goat scenarios 10 and 22: instead of asking the workflow file
> alone (where the bug isn't visible), the rule walks the repo for
> sibling `trust-policy*.json` and Terraform / Pulumi WIF declarations
> and flags broad `:sub` claims directly. The other six scanners stay
> on the workflow side, so the actual misconfig — `"repo:*"` in the
> trust policy JSON — slips past them. The OIDC-step half (KICS's
> unpinned-actions noise) is a false anchor, not the canonical bug.

---

## ③ ArtiPACKED — `.git/` packed into an artifact &nbsp;·&nbsp; scenario 17

> [!NOTE]
> **CICD-SEC-6 · Insufficient Credential Hygiene.** Palo Alto Unit 42
> disclosed in August 2024, finding **14 cases** in production open
> source at Red Hat, Google, AWS, Canonical, Microsoft, and OWASP.
> `actions/checkout` defaults to `persist-credentials: true`, writing
> `GITHUB_TOKEN` into `.git/config`; `upload-artifact` with `path: .`
> then ships it.

```yaml
# .github/workflows/scenario-17-artipacked-git-dir.yml
- uses: actions/checkout@v4
  # persist-credentials defaults to true → token in .git/config
- uses: actions/upload-artifact@v4
  with:
    name: workspace
    path: .            # ← uploads .git/, including .git/config with the token
```

| scanner            | verdict                                                                                                                |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------- |
| **pipeline-check** | ✅&nbsp;`GHA-037` catches the `persist-credentials` half; `GHA-019` catches the `.git/config` leak through the artifact; `GHA-066` (v1.4.0) catches the `upload-artifact path: .` workspace-wildcard half |
| zizmor             | ✅&nbsp;`artipacked` (the rule was named after this disclosure; catches both halves in one fire)                           |
| poutine            | ❌                                                                                                                     |
| KICS               | ❌                                                                                                                     |
| Checkov            | ❌                                                                                                                     |
| actionlint         | ❌                                                                                                                     |
| octoscan           | ✅&nbsp;`dangerous-artefact` — _rule is literally "workflow that upload artefacts containing sensitive files"_           |

> Three scanners ship rules precisely for this disclosure. **Zizmor**
> catches both halves with one named rule (`artipacked`).
> **Pipeline-check** catches both halves with three rules across two
> concerns: the persist-credentials default (`GHA-037`), the
> credential-bearing artifact (`GHA-019`), and the workspace-wildcard
> upload (`GHA-066`, shipped in v1.4.0 from the zizmor parity sweep).
> **Octoscan**'s `dangerous-artefact` flags the upload step shipping
> sensitive files but doesn't separately attribute the
> persist-credentials default. The other four scanners miss entirely.

---

## ④ The silent default: `persist-credentials` &nbsp;·&nbsp; scenario 12

> [!NOTE]
> **CICD-SEC-6 · Insufficient Credential Hygiene.** Same root cause as #③
> without the artifact step. `actions/checkout` *defaults* to writing the
> token. Any later untrusted step in the same job can read it.

```yaml
# .github/workflows/scenario-12-persist-credentials-leak.yml
- uses: actions/checkout@v4
  # ← no persist-credentials: false; GITHUB_TOKEN now in .git/config
- uses: third-party-org/some-build-action@main
```

| scanner            | verdict | rule fired                                              |
| :----------------- | :-----: | :------------------------------------------------------ |
| **pipeline-check** |   ✅    | `GHA-037` — _actions/checkout persists `GITHUB_TOKEN` into `.git/config`_ |
| zizmor             |   ✅    | `artipacked`                                            |
| poutine            |   ⚠️   | `github_action_from_unverified_creator_used` — flags the third-party action, not the persist-credentials root cause |
| KICS               |   ⚠️   | `555ab8f9-…` — fires on `actions/checkout@v4` as unpinned, not on persist-credentials specifically |
| Checkov            |   ❌    | —                                                       |
| actionlint         |   ❌    | —                                                       |
| octoscan           |   ❌    | — _`dangerous-checkout` only fires on the privileged-trigger shape (workflow_run / pull_request_target), not on the default persist-credentials behavior of a regular checkout_ |

---

## ⑤ The hygiene baseline — a scope difference layered on top of a coverage one

The strict per-scenario matrix shows pipeline-check leading the field,
so the leaderboard *is* part of the story now — but it's still not the
whole story. Pipeline-check also ships an **absence-of-control** rule
family that the other six scanners in this comparison don't carry at
all: rules that fire when a
workflow *lacks* an expected step (SBOM, SLSA, signing, vuln-scan,
etc.). Pipeline-check 1.4.0 carries **78 rules** across the `GHA-*`,
`TAINT-*`, and `AC-*` (attack-chain) families. The hygiene subset
fires on every workflow file regardless of canonical bug; the verbatim
list from the latest run:

```
GHA-006   Artifacts not signed (no cosign/sigstore step)
GHA-007   SBOM not produced (no CycloneDX/syft/Trivy-SBOM step)
GHA-024   No SLSA provenance attestation produced
GHA-020   No vulnerability scanning step
GHA-014   Deploy job missing environment binding
GHA-015   Job has no `timeout-minutes`, unbounded build
GHA-051   services / container image is not pinned by digest
GHA-001   Action not pinned to commit SHA — fires on actions/checkout@v4
GHA-037   actions/checkout persists GITHUB_TOKEN into .git/config
```

The four supply-chain hygiene rules (`GHA-006`/`007`/`020`/`024`) fire
together on **scenarios 10, 17, and 22** — the deploy-style workflows
whose targets look like production releases — bringing their total
real-fire count to **8 rules each.** No other scanner in this
comparison emits any of those four rules at all.

The strict matrix below scores only the canonical bug per scenario.
The hygiene-baseline rules are a separate axis: whether you want a
scanner that emits them is a scope call, not a coverage one — most
teams already get them from a dedicated SBOM/provenance tool. We
include them here because they're a real differentiator on this
corpus, not because every scanner *should* ship them.
