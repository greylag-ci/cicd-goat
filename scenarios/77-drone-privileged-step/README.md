# Scenario 77: Drone — `privileged: true` step

**Provider:** Drone CI · **OWASP:** CICD-SEC-7 (Insecure System Configuration)

**Vulnerable pipeline:** [`.drone.yml`](.drone.yml)

## The pattern

```yaml
steps:
  - name: build-image
    privileged: true
```

A Drone pipeline step with `privileged: true` gets full access to the host
Docker daemon / kernel.

## How an attacker exploits it

The privileged step reaches the host Docker daemon, mounts host paths, and
escapes the container — host compromise, especially on shared runners.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `DR-002` — step runs with `privileged: true` |

> Drone is scored by pipeline-check only in this comparison.

## Fix

Avoid `privileged: true`; use a rootless image builder or a dedicated, isolated
runner for builds that need the daemon; restrict which repos may run privileged
steps.

## References

- Drone — Docker pipeline / privileged mode: https://docs.drone.io/pipeline/docker/syntax/steps/
