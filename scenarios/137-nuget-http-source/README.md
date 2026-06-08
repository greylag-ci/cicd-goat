# Scenario 137: NuGet — plain-HTTP feed + private feed without `<clear/>`

**Provider:** NuGet (`NuGet.config`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: high**

**Vulnerable manifest:** [`NuGet.config`](NuGet.config)

## The pattern

```xml
<packageSources>
  <!-- no <clear/> first: the implicit public nuget.org source stays active -->
  <add key="internal" value="http://nuget.internal.example.com/v3/index.json" />
</packageSources>
```

The private feed is added over plain HTTP (no TLS), and there's no `<clear/>`
before it — so the public nuget.org gallery is still active alongside it. With no
`<packageSourceMapping>`, restore pulls each package from whichever source offers
it.

## How an attacker exploits it

Two failure modes at once: (1) the HTTP feed is MITM-able; (2) because the public
gallery is still active and unmapped, an attacker publishing a same-named package
to nuget.org can shadow a private one (NuGet dependency confusion). Either way
the attacker's package restores and its MSBuild logic can run at build time.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `NUGET-004` — _HTTP-only NuGet package source_ · `NUGET-016` — _private feed without `<clear/>` inherits the public gallery_ |

## Fix

`<clear/>` first, use `https://` feeds only, and add `<packageSourceMapping>` so
each package id/prefix is pinned to exactly one source.

## References

- Microsoft — Package source mapping: https://learn.microsoft.com/en-us/nuget/consume-packages/package-source-mapping
- Microsoft — `NuGet.config` reference: https://learn.microsoft.com/en-us/nuget/reference/nuget-config-file
