# Scenario 46: GitLab — job `image:` pinned to a mutable tag

**Provider:** GitLab CI/CD

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-9 (Improper Artifact Integrity)

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

```yaml
build:
  image: node:latest
```

The job runs inside whatever `node:latest` resolves to at run time. A mutable
tag is not an identity — it's a pointer someone can re-aim.

## How an attacker exploits it

Whoever can move the tag (the upstream maintainer, or an attacker who
compromises the registry namespace) swaps in a malicious image; the next
pipeline run executes inside it, with the job's source and secrets exposed.
The GitLab analogue of [scenario 09](../09-container-image-latest/README.md).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-001` — Image not pinned to specific version or digest |
| ciguard | `SCA-PIN-002` — Image uses mutable tag (also `PIPE-001`) |
| Checkov | — |

## Fix

Pin the image by digest: `image: node@sha256:…`. Use a controlled internal
registry and enforce digest-pinning in policy.

## References

- GitLab Docs — Pipeline security (Docker image references): https://docs.gitlab.com/ci/pipeline_security/
