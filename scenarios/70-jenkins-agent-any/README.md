# Scenario 70: Jenkins — `agent any` (controller exposure)

**Provider:** Jenkins · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · CICD-SEC-5

**Vulnerable pipeline:** [`Jenkinsfile`](Jenkinsfile)

## The pattern

```groovy
pipeline {
  agent any
  ...
}
```

`agent any` lets the build schedule onto any node — including the controller /
built-in node — with no executor isolation.

## How an attacker exploits it

Building untrusted PR code on `any` agent (especially the controller) gives
attacker code access to the controller filesystem, `init.groovy.d`, the
credential store, and other jobs' workspaces — full compromise. Jenkins
analogue of scenario 08 (self-hosted runner on a public repo).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `JF-003` — pipeline uses `agent any` (no executor isolation) |
| ciguard | `JKN-RUN-001` — unconstrained top-level agent |

> Caught by both Jenkins-aware scanners — a clean two-scanner agreement.

## Fix

Use dedicated, ephemeral agents (labels / clouds) for builds; never build
untrusted code on the controller; set the built-in node executor count to 0.

## References

- Jenkins — Pipeline syntax (agent): https://www.jenkins.io/doc/book/pipeline/syntax/
