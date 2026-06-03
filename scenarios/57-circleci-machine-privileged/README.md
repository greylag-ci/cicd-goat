# Scenario 57: CircleCI — `machine: true` privileged executor

**Provider:** CircleCI · **OWASP:** CICD-SEC-7 (Insecure System Configuration)

**Vulnerable pipeline:** [`.circleci/config.yml`](.circleci/config.yml)

## The pattern

```yaml
jobs:
  build:
    machine: true
```

The `machine` executor gives a full VM with root and direct Docker daemon
access, where the `docker` executor (which restricts daemon control for
isolation) would suffice.

## How an attacker exploits it

Combined with any injection, `machine: true` escalates from in-container to
host-level — container escape, Docker daemon abuse, host-path mounts — the
CircleCI analogue of scenario 08's runner-trust problem.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `CC-029` — machine executor image not pinned (fires on `machine: true`) |
| Checkov | — |

## Fix

Prefer the `docker` executor; use `setup_remote_docker` for image builds rather
than `machine`; never run untrusted code with `machine: true`.

## References

- CircleCI — Using Docker / executors: https://circleci.com/docs/guides/execution-managed/using-docker/
