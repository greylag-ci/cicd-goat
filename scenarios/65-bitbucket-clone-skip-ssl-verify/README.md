# Scenario 65: Bitbucket — `clone: skip-ssl-verify: true`

**Provider:** Bitbucket Pipelines · **OWASP:** CICD-SEC-7 (Insecure System Configuration)

**Vulnerable pipeline:** [`bitbucket-pipelines.yml`](bitbucket-pipelines.yml)

## The pattern

```yaml
clone:
  skip-ssl-verify: true
```

Disables TLS certificate verification on the repository clone.

## How an attacker exploits it

A man-in-the-middle on the clone path serves malicious source into the build,
which then runs with the pipeline's privileges and secrets.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | — |
| Checkov | — |

> **All-miss — a next-gen target.** `clone: { skip-ssl-verify: true }` is a
> clean single-key static signature that no scanner here flags yet.

## Fix

Never set `skip-ssl-verify: true`. Leave TLS verification on; if a self-signed
internal host is involved, install its CA into the build image instead.

## References

- Atlassian — Git clone behavior: https://support.atlassian.com/bitbucket-cloud/docs/git-clone-behavior/
