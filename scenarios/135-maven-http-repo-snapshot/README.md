# Scenario 135: Maven — plain-HTTP repository + mutable `SNAPSHOT` dependency

**Provider:** Maven (`pom.xml`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: medium**

**Vulnerable manifest:** [`pom.xml`](pom.xml)

## The pattern

```xml
<repository><url>http://nexus.internal.example.com/...</url></repository>
...
<dependency>
  <version>2.4.0-SNAPSHOT</version>     <!-- mutable -->
</dependency>
```

A `<repository>` is declared over plain HTTP (no TLS), and a dependency is pinned
to a `-SNAPSHOT` version. Maven resolves SNAPSHOTs to the *latest* timestamped
build on each run, so the artifact changes under you — and an HTTP repo has no
transport integrity.

## How an attacker exploits it

A network-MITM (or whoever controls the Nexus) serves an arbitrary JAR for the
SNAPSHOT coordinate; the build links and executes it. Because SNAPSHOT is
mutable, the swap doesn't even require touching the repo's release artifacts.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `MVN-003` — _plaintext-HTTP Maven repository_ · `MVN-002` — _mutable `SNAPSHOT` version_ |

## Fix

Use `https://` for every `<repository>`, pin dependencies to released
(non-SNAPSHOT) versions, and enable strict checksum gating
(`<checksumPolicy>fail</checksumPolicy>`).

## References

- Apache Maven — Repository / mirror security: https://maven.apache.org/guides/mini/guide-mirror-settings.html
- Apache Maven — SNAPSHOT versions: https://maven.apache.org/guides/getting-started/index.html#what-is-a-snapshot-version
