# Scenario 129: Drone CI — dangerous shell idiom in a step command

**Provider:** Drone CI · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: high**

**Vulnerable pipeline:** [`.drone.yml`](.drone.yml)

## The pattern

```yaml
steps:
  - name: build
    commands:
      - eval "$BUILD_CMD"
      - sh -c $RAW_HOOK
```

A step `commands:` entry uses `eval "$VAR"` / `sh -c $VAR` / backtick exec.
These idioms hand the value **full shell-grammar reach** regardless of whether
its source is currently trusted — so the moment any attacker-influenced value
flows into `$BUILD_CMD` / `$RAW_HOOK`, it's command execution. Completes the
dangerous-shell-idiom family across providers (GHA-028 / GL-026 / BB-026 /
ADO-027 / CC-027 / BK-016).

## How an attacker exploits it

`eval` re-parses its argument as a full shell command line. If `$BUILD_CMD` is
ever set from build metadata, a Drone substitution variable, a secret, or a file
the build fetched, an attacker who influences that value runs arbitrary commands
on the runner. `eval "$(ssh-agent -s)"` and similar literal-bootstrap forms are
intentionally **not** flagged — only the variable-reach shape.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `DR-017` — _dangerous shell idiom in a Drone step command_ |

## Fix

Replace `eval "$VAR"` / `sh -c "$VAR"` / backtick exec with direct command
invocation; pass the value as a quoted argument to a script you own that
validates it against an allow-list:

```yaml
commands:
  - ./scripts/dispatch.sh "$BUILD_CMD"
```

## References

- Drone — Pipeline steps: https://docs.drone.io/pipeline/docker/syntax/steps/
- CWE-78 — OS command injection: https://cwe.mitre.org/data/definitions/78.html
