# Scenario 69: Jenkins — shared library on a mutable `@master` ref

**Provider:** Jenkins · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable pipeline:** [`Jenkinsfile`](Jenkinsfile)

## The pattern

```groovy
@Library('platform-shared-lib@master') _
```

A shared library loaded on a **mutable branch ref** (`@master`). Whoever can
push to that library repo's `master` executes code in every consuming pipeline
on its next run. (A *trusted*, folder-global library runs outside the Groovy
sandbox — controller RCE.)

## How an attacker exploits it

An attacker with push access to the library repo (or who compromises it) lands
a malicious change on `master`; it runs in every pipeline that loads the library
`@master`. Jenkins analogue of the mutable-action-ref / reusable-workflow-trust
class (scenarios 03 / 28).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `JF-001` — shared library not pinned to a tag or commit |
| ciguard | — |

## Fix

Pin the library to an immutable tag or commit SHA
(`@Library('platform-shared-lib@v1.4.2')`); restrict write access to
trusted-library repos; prefer folder-level (sandboxed) libraries for
less-trusted code.

## References

- Jenkins — Extending with Shared Libraries: https://www.jenkins.io/doc/book/pipeline/shared-libraries/
