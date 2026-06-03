# Scenario 67: Jenkins — `@Grab` sandbox bypass (CVE-2019-1003000)

**Provider:** Jenkins · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`Jenkinsfile`](Jenkinsfile)

## The pattern

```groovy
@Grab(group = 'org.buildobjects', module = 'jproc', version = '2.8.2')
import org.buildobjects.process.ProcBuilder
```

`@Grab` is an AST-transforming annotation applied during **compilation** —
before the Groovy sandbox's runtime checks. A user who can control a Jenkinsfile
(or a sandboxed shared library) uses it to fetch and execute arbitrary Java on
the controller, bypassing the sandbox entirely.

## How an attacker exploits it

This is the **CVE-2019-1003000 / -1003001 / -1003002** (SECURITY-1266) class.
Public PoCs `@Grab` `org.buildobjects:jproc` and use it to run shell commands on
the controller — full RCE — before any pipeline step executes.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `JF-019` — Groovy sandbox escape pattern detected |
| ciguard | — |

## Fix

Patch Script Security ≥ 1.50 / Pipeline Groovy ≥ 2.61.1 / Declarative ≥ 1.3.4.1;
restrict who can edit Jenkinsfiles and sandboxed libraries; disallow `@Grab`
(and other AST-transform annotations) in untrusted code.

## References

- adamyordan — CVE-2019-1003000 Jenkins RCE PoC: https://github.com/adamyordan/cve-2019-1003000-jenkins-rce-poc
- Jenkins security advisory SECURITY-1266
