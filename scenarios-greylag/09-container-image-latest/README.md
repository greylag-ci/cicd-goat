# Scenario 09: Container image pinned to `:latest`

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse),
CICD-SEC-9 (Improper Artifact Integrity Validation)

**Vulnerable workflow:** [`.github/workflows/scenario-09-container-image-latest.yml`](../../.github/workflows/scenario-09-container-image-latest.yml)

## The pattern

`container:` (and `services:`) blocks in a job can pull arbitrary OCI
images. If the reference uses a mutable tag (`:latest`, or any tag the
registry side can move), the image you actually run can change between
jobs. The classic supply-chain pattern: an attacker compromises the
upstream image, pushes a malicious build to `:latest`, and every consumer
runs it on next pull.

## How an attacker exploits it

1. Compromise the source image (typosquat, account compromise of the
   maintainer, credential leak in their own CI...).
2. Push a tampered build to `:latest`.
3. Wait for downstream CI to pull. The image runs with whatever the
   job container layer permits — including `GITHUB_TOKEN` and secrets
   available to the job.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | partial — current rule set focuses on action refs more than container refs |
| poutine   | partial |
| checkov   | "Ensure image is pinned to a digest" |
| kics      | "Image Tagged Latest" |
| trivy     | "Image should not be tagged with 'latest'" |
| gitleaks  | n/a |

## Fix

Pin to a digest:

```yaml
container:
  image: ubuntu@sha256:1234abcd...  # digest is immutable
```

Or at least to a specific build tag:

```yaml
container:
  image: ubuntu:24.04
```

## References

- Docker docs — "Why pinning images to digests":
  https://docs.docker.com/engine/security/trust/content_trust/
