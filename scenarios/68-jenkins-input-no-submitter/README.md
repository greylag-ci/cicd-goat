# Scenario 68: Jenkins — `input` step without `submitter`

**Provider:** Jenkins · **OWASP:** CICD-SEC-1 (Insufficient Flow Control) · CICD-SEC-5

**Vulnerable pipeline:** [`Jenkinsfile`](Jenkinsfile)

## The pattern

```groovy
input message: 'Deploy to production?'
sh './deploy.sh --env prod'
```

The Pipeline `input` step defaults to allowing **any** authenticated user to
approve when no `submitter:` is set. A "manual approval before prod" gate that
omits `submitter:` therefore enforces no real separation of duties.

## How an attacker exploits it

Any logged-in user (not just the intended approvers) approves the gate, and the
privileged deploy proceeds — defeating the control. Analogue of scenario 37
(confused-deputy auto-merge / approval-gate weakness).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | — |
| ciguard | — |

> **All-miss — a next-gen target.** An `input` step lacking a `submitter:`
> field is a clean static signature that no scanner here flags yet.

## Fix

Always set `submitter:` to a specific user/group
(`input message: '…', submitter: 'release-managers'`); combine with credential
scoping so approval actually gates the privileged action.

## References

- Jenkins — Pipeline `input` step: https://www.jenkins.io/doc/pipeline/steps/pipeline-input-step/
