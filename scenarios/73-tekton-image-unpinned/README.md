# Scenario 73: Tekton — step `image:` not pinned to a digest

**Provider:** Tekton · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-9

**Vulnerable pipeline:** [`pipeline.yaml`](pipeline.yaml)

## The pattern

```yaml
steps:
  - name: test
    image: node:20
```

A Tekton step image pinned to a mutable tag instead of a digest. The step runs
inside whatever the tag resolves to at run time.

## How an attacker exploits it

Whoever moves the tag (upstream maintainer, or an attacker who compromises the
registry namespace) swaps in a malicious image; the next run executes inside it.
Tekton analogue of scenarios 09 / 46 / 58 / 64 / 78.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `TKN-001` — Tekton step image not pinned to a digest |

## Fix

Pin step images by digest (`image: node@sha256:…`); use an admission policy
that rejects mutable image references.

## References

- Tekton — Tasks (steps / image): https://tekton.dev/docs/pipelines/tasks/
