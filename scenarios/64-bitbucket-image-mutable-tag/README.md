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
| pipeline-check | — (no Bitbucket image-tag rule fires) |
| Checkov | `CKV_BITBUCKETPIPELINES_1` — image uses a non-latest version tag |

> **Checkov solo catch.** pipeline-check flags Bitbucket `pipe:` pinning
> (scenario 63) but not the top-level `image:` tag — so Checkov is the only
> scanner that covers this row.

## Fix

Pin the image by digest: `image: node@sha256:…`.

## References

- Checkov — Bitbucket Pipelines policies: https://www.checkov.io/5.Policy%20Index/bitbucket_pipelines.html
