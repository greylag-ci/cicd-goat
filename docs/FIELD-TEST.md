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

| scanner            | sees workflow                                         | sees trust-policy.json |
| :----------------- | :--------------------------------------------------- | :--------------------: |
| **pipeline-check** | ❌&nbsp;_Hygiene fires (no SBOM/SLSA/signing/vuln-scan); no IAM-aware rule yet_ | ❌                     |
| zizmor             | ❌                                                    | ❌                     |
| poutine            | ❌                                                    | ❌                     |
| KICS               | ❌&nbsp;_Catches `aws-actions/...@v4` as unpinned action; misses the wildcard sub_ | ❌                     |
| Checkov            | ❌                                                    | ❌                     |

> **This is a comparison-wide miss.** Both halves of the canonical bug
> — the workflow's `role-to-assume` ARN reference and the IAM trust
> policy's wildcard `sub` — go uncaught by every scanner in this run.
> Pipeline-check fires the supply-chain hygiene rules on the workflow
> (no SBOM / SLSA / signing) and KICS fires its unpinned-actions rule,
> but neither lands on the actual OIDC misconfig. Honest benchmark for
> the hard end; the kind of scenario the *next* generation of cross-
> scope rules needs to learn.

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

| scanner            | verdict                                                                                 |
| :----------------- | :-------------------------------------------------------------------------------------- |
| zizmor             | ✅&nbsp;`artipacked` (the rule was named after this very disclosure; catches both halves) |
| **pipeline-check** | ⚠️&nbsp;`GHA-037` catches the `persist-credentials` half; no dedicated rule yet for `upload-artifact path: .` |
| poutine            | ❌                                                                                      |
| KICS               | ❌                                                                                      |
| Checkov            | ❌                                                                                      |

> Honest assessment: **zizmor is the only scanner here that ships a
> rule precisely for this disclosure.** Pipeline-check catches half;
> the rest miss entirely.

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

---

## ⑤ The hygiene baseline — a scope difference, not a coverage one

The strict per-scenario matrix shows pipeline-check leading on
canonical-bug coverage by one scenario over zizmor — close enough that
the more interesting comparison isn't the leaderboard. It's that
pipeline-check ships an **absence-of-control** rule family that the
other six scanners don't carry at all: rules that fire when a workflow
*lacks* an expected step (SBOM, SLSA, signing, vuln-scan, etc.).
Pipeline-check 1.1.0 carries **65 rules** across the `GHA-*`,
`TAINT-*`, and `AC-*` (attack-chain) families. Verbatim rule list
from the latest run:

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
