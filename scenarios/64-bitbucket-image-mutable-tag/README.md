# Scenario 64: Bitbucket — `image:` pinned to a mutable tag

**Provider:** Bitbucket Pipelines · **OWASP:** CICD-SEC-9 (Improper Artifact Integrity) · CICD-SEC-3

**Vulnerable pipeline:** [`bitbucket-pipelines.yml`](bitbucket-pipelines.yml)

## The pattern

```yaml
image: node:latest
```

The build `image:` is pinned to a mutable tag instead of a digest. Every step
runs inside whatever that tag currently resolves to.

## How an attacker exploits it

A tag overwrite (upstream, or via stolen registry creds) swaps in a malicious
image on the next run, with the pipeline's source and secrets exposed —
analogue of scenarios 09 / 46 / 58.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `BB-029` — `image:` not pinned by sha256 digest |
| Checkov | `CKV_BITBUCKETPIPELINES_1` — image uses a non-latest version tag |

> Both pipeline-check (`BB-029`, added in 1.9.0) and Checkov flag the mutable `image:` tag.

## Fix

Pin the image by digest: `image: node@sha256:…`.

## References

- Checkov — Bitbucket Pipelines policies: https://www.checkov.io/5.Policy%20Index/bitbucket_pipelines.html
