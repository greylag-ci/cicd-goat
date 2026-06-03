# Scenario 95: Dockerfile — base image pinned to a mutable tag

**Provider:** Dockerfile · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-9

**Vulnerable file:** [`Dockerfile`](Dockerfile)

## The pattern

```dockerfile
FROM node:latest
```

The base image is a mutable tag, not a digest. Every rebuild pulls whatever
`node:latest` resolves to at build time.

## How an attacker exploits it

Whoever moves the tag (upstream, or an attacker who compromises the registry
namespace) gets their layers into your image on the next build — the Dockerfile
form of the mutable-image class (scenarios 09 / 46 / 58 / 64 / 73 / 78).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `DF-001` — FROM image not pinned to a sha256 digest |
| Trivy | `DS-0001` — `FROM` uses a non-specific (`latest`) tag |
| Checkov | `CKV_DOCKER_7` — base image uses a non-latest version tag |
| KICS | `Image Version Using 'latest'` (`f45ea400-…`) — mutable base tag |

## Fix

Pin the base image by digest: `FROM node@sha256:…` (optionally `node:20@sha256:…`
for readability). Rebuild via a controlled base-image bump process.

## References

- Checkov — Dockerfile policies: https://www.checkov.io/5.Policy%20Index/dockerfile.html
