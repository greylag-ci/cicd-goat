# Scenario 138: NuGet — multiple sources without `packageSourceMapping`

**Provider:** NuGet (`NuGet.config`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: high**

**Vulnerable manifest:** [`NuGet.config`](NuGet.config)

## The pattern

```xml
<packageSources>
  <clear />
  <add key="nuget.org" value="https://api.nuget.org/v3/index.json" />
  <add key="internal"  value="https://nuget.internal.example.com/v3/index.json" />
</packageSources>
<!-- no <packageSourceMapping> -->
```

Two package sources are configured with **no `<packageSourceMapping>`**. Without
mapping, NuGet restore resolves each package id from whichever source offers the
highest version.

## How an attacker exploits it

An attacker publishes a package with the same id as a private one to the public
gallery at a higher version. NuGet restore prefers it (NuGet dependency
confusion), pulls the attacker's package, and its build-time MSBuild
targets/props can execute during restore/build. Both feeds here are HTTPS — the
bug is purely the missing source mapping.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `NUGET-007` — _multiple NuGet sources without `packageSourceMapping`_ |

## Fix

Add `<packageSourceMapping>` pinning each package id (or org prefix, e.g.
`Acme.*`) to exactly one source, so a public-gallery package can never satisfy a
private id.

## References

- Microsoft — Package source mapping: https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping
- Microsoft — Security best practices (dependency confusion): https://learn.microsoft.com/en-us/nuget/concepts/security-best-practices
