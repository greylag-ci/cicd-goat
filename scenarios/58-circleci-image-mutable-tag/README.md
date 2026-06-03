# Scenario 58: CircleCI — docker image pinned to a mutable tag

**Provider:** CircleCI · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-9

**Vulnerable pipeline:** [`.circleci/config.yml`](.circleci/config.yml)

## The pattern

```yaml
docker:
  - image: cimg/node:latest
```

A `docker:` executor image pinned to a mutable tag instead of a digest. The
next build pulls whatever the tag resolves to; CircleCI docs warn a mutable tag
may even return a stale cached image.

## How an attacker exploits it

Whoever overwrites the tag (an accidental push, or stolen registry creds)
serves attacker-controlled image content with no integrity check — analogue of
scenarios [09](../09-container-image-latest/README.md) / 46.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `CC-003` — docker image not pinned by digest |
| Checkov | `CKV_CIRCLECIPIPELINES_1` — image uses a non-latest version tag |

> Caught by both — one of the cleaner two-scanner agreements on the non-GHA
> corpus.

## Fix

Pin the image by digest: `image: cimg/node@sha256:…`.

## References

- CircleCI — Remote Docker image support policy: https://circleci.com/docs/guides/execution-managed/remote-docker-images-support-policy/
