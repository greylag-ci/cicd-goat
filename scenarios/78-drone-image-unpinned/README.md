# Scenario 78: Drone — step `image:` mutable tag

**Provider:** Drone CI · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-9

**Vulnerable pipeline:** [`.drone.yml`](.drone.yml)

## The pattern

```yaml
steps:
  - name: test
    image: node:20
```

A Drone step `image:` pinned to a mutable tag instead of a digest.

## How an attacker exploits it

Whoever moves the tag serves attacker-controlled image content on the next run,
with the step's environment and secrets exposed. Analogue of scenarios
09 / 46 / 58 / 73.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `DR-001` — step image not pinned to a digest |

## Fix

Pin step images by digest (`image: node@sha256:…`).

## References

- Drone — Docker pipeline steps: https://docs.drone.io/pipeline/docker/syntax/steps/
