# Scenario 81: Cloud Build — step image not pinned by digest

**Provider:** Google Cloud Build · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-9

**Vulnerable pipeline:** [`cloudbuild.yaml`](cloudbuild.yaml)

## The pattern

```yaml
steps:
  - name: 'gcr.io/cloud-builders/docker:latest'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/app', '.']
```

A Cloud Build step `name:` (the step's builder image) pinned to a mutable tag
rather than a digest.

## How an attacker exploits it

Whoever moves the tag (or compromises the builder image) controls the step's
execution environment on the next build. Analogue of scenarios
09 / 46 / 58 / 73 / 78.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GCB-001` — Cloud Build step image not pinned by digest |

> Cloud Build is scored by pipeline-check only in this comparison.

## Fix

Pin builder images by digest (`gcr.io/cloud-builders/docker@sha256:…`); prefer
images from a controlled registry.

## References

- Google Cloud — Build configuration overview: https://cloud.google.com/build/docs/build-config-file-schema
