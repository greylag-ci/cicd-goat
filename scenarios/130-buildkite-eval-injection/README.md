# Scenario 130: Buildkite — dangerous shell idiom in a step command

**Provider:** Buildkite · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: high**

**Vulnerable pipeline:** [`.buildkite/pipeline.yml`](.buildkite/pipeline.yml)

## The pattern

```yaml
steps:
  - command:
      - eval "$BUILD_CMD"
      - sh -c $RAW_HOOK
```

A step `command:` entry uses `eval "$VAR"` / `sh -c $VAR` / backtick exec. The
idiom hands the value full shell-grammar reach regardless of whether its source
is currently trusted. The Buildkite analogue of GHA-028 / GL-026 / BB-026 /
ADO-027 / CC-027 / DR-017 — the one CI provider that previously lacked the rule.

## How an attacker exploits it

`eval` re-parses its argument as a shell command line. Buildkite build metadata
(`buildkite-agent meta-data get`), pipeline env, and PR-controlled values all
commonly flow into step variables; if any reaches `$BUILD_CMD` / `$RAW_HOOK`,
the attacker runs arbitrary commands on the agent. `eval "$(ssh-agent -s)"` and
similar literal-bootstrap forms are intentionally not flagged.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `BK-016` — _dangerous shell idiom in a Buildkite step command_ |

## Fix

Replace `eval "$VAR"` / `sh -c "$VAR"` / backtick exec with direct invocation;
pass the value as a quoted argument to a script you own that validates it:

```yaml
command:
  - ./scripts/dispatch.sh "$BUILD_CMD"
```

## References

- Buildkite — Command step: https://buildkite.com/docs/pipelines/command-step
- CWE-78 — OS command injection: https://cwe.mitre.org/data/definitions/78.html
