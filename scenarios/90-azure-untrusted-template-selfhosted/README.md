# Scenario 90: Azure — untrusted `resources` template on a self-hosted agent

**Provider:** Azure Pipelines · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-7 · **Severity: critical**

**Vulnerable pipeline:** [`azure-pipelines.yml`](azure-pipelines.yml)

## The pattern

The worst-case combination of [scenario 53](../53-azure-resources-untrusted-repo/README.md)
and [scenario 54](../54-azure-self-hosted-untrusted/README.md):

```yaml
resources:
  repositories:
    - repository: templates
      type: github
      name: third-party/ci-templates
      ref: refs/heads/main        # untrusted external repo, mutable ref
pool:
  name: 'Self-Hosted-Linux'       # persistent self-hosted agent
steps:
  - checkout: templates
  - template: build-and-deploy.yml@templates
```

## How an attacker exploits it

Whoever controls `third-party/ci-templates@main` ships a template whose steps
run on the **persistent** self-hosted agent. Because the agent state survives
between jobs, the compromise persists — it plants a backdoor that steals
subsequent pipelines' source and secrets. Supply-chain RCE *with a foothold*.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ADO-025` — cross-repo template not pinned to a commit SHA (also `ADO-013` self-hosted) |
| Checkov | — |

## Fix

Pin external repository resources to an immutable tag/commit and require
approval on the resource; build untrusted/external code only on ephemeral,
reimaged agents (Microsoft-hosted or one-time scale-set), never persistent
self-hosted ones.

## References

- Microsoft Learn — Templates for security: https://learn.microsoft.com/azure/devops/pipelines/security/templates
- Microsoft DevOps Blog — Let's Hack a Pipeline: Shared Infrastructure: https://devblogs.microsoft.com/devops/pipeline-shared-infrastructure/
