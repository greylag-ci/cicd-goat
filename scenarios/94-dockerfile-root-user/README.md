# Scenario 94: Dockerfile — container runs as root (no `USER`)

**Provider:** Dockerfile · **OWASP:** CICD-SEC-7 (Insecure System Configuration)

**Vulnerable file:** [`Dockerfile`](Dockerfile)

## The pattern

The image declares no `USER`, so every process runs as **root** inside the
container. Root-in-container plus any `--privileged`/kernel/escape bug is one
step from the host — and this is the image the pipeline builds and ships.

## How an attacker exploits it

An app/RCE bug in the running container executes as root, easing breakout and
host/orchestrator compromise; mounted secrets and the container runtime are in
reach.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `DF-002` — container runs as root (missing/root USER) |
| Checkov | `CKV_DOCKER_3` — a non-root user has been created |
| KICS | (reconciled from CI — KICS has a "container runs as root" query) |

> Dockerfile is scored by three scanners here — a richer comparison than the
> single-scorer pipeline rows.

## Fix

Add a non-root `USER` (e.g. `RUN adduser --system app && USER app`); set a
read-only root filesystem and drop capabilities at runtime.

## References

- Checkov — Dockerfile policies: https://www.checkov.io/5.Policy%20Index/dockerfile.html
- Docker — Dockerfile best practices (USER): https://docs.docker.com/build/building/best-practices/
