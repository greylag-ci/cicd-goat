# Scenario 42: GitLab — untrusted `include:` (remote / mutable ref)

**Provider:** GitLab CI/CD

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-9 (Improper Artifact Integrity)

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

`include:` merges external pipeline configuration that runs with the **full
privileges** of your pipeline. Two unsafe forms:

```yaml
include:
  - remote: 'https://templates.example.com/ci/build.yml'   # unpinned, unverifiable
  - project: 'platform/ci-templates'
    ref: main                                              # mutable branch, not a SHA
    file: '/deploy.yml'
```

A `remote:` include is fetched over the network and **cannot be pinned or
verified** by GitLab. A `project:` include on a mutable `ref:` (a branch or a
moved tag) lets whoever can push to that ref inject jobs into your pipeline.

## How an attacker exploits it

Whoever controls the remote host, or can push to `platform/ci-templates@main`,
adds a job/`script:` that exfiltrates your pipeline's secrets on your next run.
This is the GitLab analogue of the tj-actions mutable-ref class
([scenario 03](../03-action-mutable-ref/README.md)) and the March-2026 CI
supply-chain incidents GitLab analysed.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-005` — `include:` pulls remote / project without pinned ref |
| ciguard | `PIPE-002` — Unsafe remote include (also `SC-002` for the unpinned project include) |
| Checkov | — |

## Fix

Avoid `remote:` includes — vendor the file into your repo and include the local
copy. For `project:`/component includes, pin to a **commit SHA** (or a protected
tag), never a branch.

## References

- GitLab Docs — Pipeline security (Includes): https://docs.gitlab.com/ci/pipeline_security/
- "Pipeline security lessons from March supply chain incidents": https://about.gitlab.com/blog/
