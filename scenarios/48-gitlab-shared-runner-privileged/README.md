# Scenario 48: GitLab — untagged shared-runner job + privileged Docker-in-Docker

**Provider:** GitLab CI/CD

**OWASP CICD-SEC mapping:** CICD-SEC-7 (Insecure System Configuration) · CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

A build job carries **no `tags:`** (so it lands on any shared/untagged runner)
and brings up a privileged `docker:dind` service with TLS disabled on the
daemon socket:

```yaml
build-image:
  services:
    - name: docker:27-dind@sha256:…
      command: ["--host=tcp://0.0.0.0:2375"]
  variables:
    DOCKER_TLS_CERTDIR: ""          # no TLS on the daemon socket
    DOCKER_HOST: "tcp://docker:2375"
  script:
    - docker build -t app .
```

On a shared runner, a privileged dind with an unauthenticated daemon socket can
reach the host Docker daemon and the workspaces/credentials of other tenants'
jobs — container escape and cross-tenant compromise.

## How an attacker exploits it

A job from a low-trust pipeline scheduled onto the same shared runner talks to
the exposed, unauthenticated Docker daemon, escapes its container, and harvests
other jobs' state and credentials.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| ciguard | `RUN-002` — Privileged Docker-in-Docker (also flags shared-runner use) |
| pipeline-check | `GL-039` — Docker-in-Docker service exposes an unauthenticated daemon |
| Checkov | — |

> ciguard (`RUN-002`) names the privileged-dind / shared-runner combination. pipeline-check 1.9.0 now joins it from a different angle: `GL-039` flags the insecure dind daemon (TLS disabled on the exposed Docker socket), the exploitable core. It does not separately flag the untagged-shared-runner facet.

## Fix

Tag-pin privileged jobs to dedicated, ephemeral runners; disable `run_untagged`
on sensitive runners; keep TLS on the dind daemon (`DOCKER_TLS_CERTDIR=/certs`)
and never expose `tcp://0.0.0.0:2375`. Avoid privileged builds on shared
infrastructure entirely where possible.

## References

- GitLab Docs — Configure runners: https://docs.gitlab.com/ci/runners/configure_runners/
- GitLab Docs — Use Docker to build Docker images: https://docs.gitlab.com/ci/docker/using_docker_build/
