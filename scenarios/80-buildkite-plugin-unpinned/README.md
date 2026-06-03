# Scenario 80: Buildkite — plugin pinned to a mutable ref

**Provider:** Buildkite · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable pipeline:** [`.buildkite/pipeline.yml`](.buildkite/pipeline.yml)

## The pattern

```yaml
plugins:
  - docker-compose#latest:
      run: app
```

A Buildkite plugin pinned to a mutable ref (`#latest`). A plugin runs hooks in
the agent's context with the build's environment in scope.

## How an attacker exploits it

A mutable ref overwritten upstream (or an untrusted plugin) executes attacker
code with the build's secrets. Analogue of the mutable-action / mutable-pipe
class (scenarios 03 / 63).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `BK-001` — Buildkite plugin not pinned to an exact version |

## Fix

Pin plugins to an exact version (`docker-compose#v4.16.0`); vet third-party
plugins; mirror critical plugins internally.

## References

- Buildkite — Using plugins: https://buildkite.com/docs/pipelines/integrations/plugins/using
