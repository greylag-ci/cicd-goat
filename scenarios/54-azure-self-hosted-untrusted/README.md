# Scenario 54: Azure — self-hosted pool building untrusted PRs

**Provider:** Azure Pipelines · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · CICD-SEC-4

**Vulnerable pipeline:** [`azure-pipelines.yml`](azure-pipelines.yml)

## The pattern

```yaml
pr:
  branches: { include: ['*'] }   # builds every PR, including forks
pool:
  name: 'Self-Hosted-Linux'      # persistent self-hosted agent
```

A persistent self-hosted agent runs untrusted (fork/public) PR code. The agent
state survives between jobs.

## How an attacker exploits it

Untrusted job code installs a backdoor / filesystem watcher / poisoned compiler
that persists and steals the *next* pipeline's source and secrets — the Azure
analogue of the self-hosted-runner-on-public-repo bug
([scenario 08](../08-self-hosted-public-fork/README.md)). Documented in
Microsoft's "Let's Hack a Pipeline: Shared Infrastructure".

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ADO-013` — self-hosted pool without explicit ephemeral marker |
| Checkov | — |

## Fix

Use Microsoft-hosted or one-time scale-set (ephemeral, reimaged) agents for
untrusted builds; never build public/fork code on persistent self-hosted
agents; network-isolate and reset self-hosted agents between jobs.

## References

- Microsoft DevOps Blog — Let's Hack a Pipeline: Shared Infrastructure: https://devblogs.microsoft.com/devops/pipeline-shared-infrastructure/
- CyberArk — A Security Analysis of Azure DevOps Job Execution: https://www.cyberark.com/resources/threat-research-blog/a-security-analysis-of-azure-devops-job-execution
