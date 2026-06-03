# Scenario 53: Azure — `resources: repositories` on an untrusted/mutable ref

**Provider:** Azure Pipelines · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-9

**Vulnerable pipeline:** [`azure-pipelines.yml`](azure-pipelines.yml)

## The pattern

```yaml
resources:
  repositories:
    - repository: templates
      type: github
      name: third-party/ci-templates
      ref: refs/heads/main      # mutable branch on an external repo
steps:
  - checkout: templates
  - template: deploy-steps.yml@templates
```

An external repo is checked out and its template/scripts run, pinned only to a
mutable branch.

## How an attacker exploits it

Whoever controls that branch (the upstream owner, or anyone who can push to it)
gets their code/templates executed in your pipeline with your secrets — the
Azure analogue of the mutable-ref supply-chain class
([scenario 03](../03-action-mutable-ref/README.md)).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ADO-025` — cross-repo template not pinned to commit SHA |
| Checkov | — |

## Fix

Pin `ref:` to an immutable tag/commit (`ref: refs/tags/v1`); add a repository-
resource check so the external repo requires approval; restrict template
sources to trusted, controlled repos.

## References

- Microsoft Learn — Templates for security: https://learn.microsoft.com/azure/devops/pipelines/security/templates
