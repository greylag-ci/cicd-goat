# Scenario 86: Jenkins — builds untrusted fork PRs with credentials (PPE)

**Provider:** Jenkins · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: critical**

**Vulnerable pipeline:** [`Jenkinsfile`](Jenkinsfile)

## The pattern

A multibranch pipeline is configured to **build fork pull requests** and to
**trust them** (the GitHub/Bitbucket Branch Source "Discover PRs from forks →
Trust: *Everyone*" strategy). Because the fork's own repo content drives the
build, fork-controlled steps run with the controller's credentials:

```groovy
sh 'make build'                                    // fork-supplied Makefile
withCredentials([string(credentialsId: 'prod-deploy-token', variable: 'TOKEN')]) {
    sh './deploy.sh'                               // PR code can read $TOKEN
}
```

## How an attacker exploits it

An attacker forks, edits the build to dump `credentials()` / env, opens a PR,
and Jenkins runs it with full controller credentials — the canonical OWASP
"Poisoned Pipeline Execution". Jenkins analogue of
[scenario 01](../01-prtarget-checkout-head/README.md) (`pull_request_target`).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | — |
| ciguard | — |

> **All-miss — a next-gen target.** The enabling condition is the fork-trust
> *job/folder configuration*, which lives in Jenkins config, not in the
> Jenkinsfile — so no file-scanning tool here can see it. This is the hardest,
> highest-impact class: configuration-spread fork-PR RCE.

## Fix

Set fork-PR trust to **"Nobody"** / "Collaborators"; require manual approval
before building untrusted PRs; never expose deploy credentials to PR builds;
use throwaway agents.

## References

- OWASP CICD-SEC-4 (Poisoned Pipeline Execution): https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-04-Poisoned-Pipeline-Execution
- Jenkins — GitHub Branch Source / trust: https://plugins.jenkins.io/github-branch-source/
