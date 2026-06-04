# Scenario 51: Azure — `checkout` with `persistCredentials: true`

**Provider:** Azure Pipelines · **OWASP:** CICD-SEC-6 (Insufficient Credential Hygiene)

**Vulnerable pipeline:** [`azure-pipelines.yml`](azure-pipelines.yml)

## The pattern

```yaml
- checkout: self
  persistCredentials: true
```

`persistCredentials: true` leaves the `System.AccessToken` / repo OAuth token in
`.git/config` as an `AUTHORIZATION` header after fetch (the default is false).

## How an attacker exploits it

A later step — or attacker-controlled PR code — reads `.git/config`,
base64-decodes the auth header, and reuses the token to push or reach other
repos. The Azure equivalent of the ArtiPACKED / persist-credentials leak
(scenarios [12](../12-persist-credentials-leak/README.md) /
[17](../17-artipacked-git-dir/README.md)).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ADO-032` — `persistCredentials` leaves the pipeline token in `.git/config` |
| Checkov | — |

> pipeline-check 1.9.0 added `ADO-032`, which flags `checkout persistCredentials: true`.

## Fix

Don't set `persistCredentials: true` unless a step truly needs to push; if so,
scrub `.git/config` afterward and never upload the workspace as an artifact.
Prefer short-lived / OIDC auth.

## References

- Microsoft Learn — `steps.checkout`: https://learn.microsoft.com/azure/devops/pipelines/yaml-schema/steps-checkout
- Synacktiv — CI/CD secrets extraction: https://www.synacktiv.com/en/publications/cicd-secrets-extraction-tips-and-tricks
