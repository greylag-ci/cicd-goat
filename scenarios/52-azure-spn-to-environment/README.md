# Scenario 52: Azure — `addSpnToEnvironment` service-principal exposure

**Provider:** Azure Pipelines · **OWASP:** CICD-SEC-2 (Inadequate IAM) · CICD-SEC-6

**Vulnerable pipeline:** [`azure-pipelines.yml`](azure-pipelines.yml)

## The pattern

```yaml
- task: AzureCLI@2
  inputs:
    azureSubscription: 'SP-CICD-Owner'
    addSpnToEnvironment: true
```

`addSpnToEnvironment: true` dumps the service connection's service-principal
client id/secret/tenant into the job environment — and the connection here is
an over-scoped (Owner) SP, with no environment/branch gate on the job.

## How an attacker exploits it

Any step (or injected code) reads `$servicePrincipalKey` and authenticates to
Azure ARM directly, pivoting beyond the pipeline with the SP's full rights.
Documented by Synacktiv's CI/CD secrets-extraction research.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ADO-029` — service-connection job without environment or branch gate |
| Checkov | — |

> pipeline-check flags the **ungated service-connection job** (the core risky
> construct that `addSpnToEnvironment` makes worse); it doesn't name the
> `addSpnToEnvironment` flag specifically.

## Fix

Avoid `addSpnToEnvironment` unless required; use Workload Identity Federation
(OIDC) service connections instead of SP secrets; scope the SP to the minimum
resource group/role; gate the connection behind environment approvals & checks.

## References

- Synacktiv — CI/CD secrets extraction: https://www.synacktiv.com/en/publications/cicd-secrets-extraction-tips-and-tricks
- Microsoft Learn — Secure Azure Pipelines: https://learn.microsoft.com/azure/devops/pipelines/security/overview
