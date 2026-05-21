# Scenario 14: `$GITHUB_ENV` poisoning via PR body

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-14-env-injection-pr-body.yml`](../../.github/workflows/scenario-14-env-injection-pr-body.yml)

## The pattern

The runner reads `$GITHUB_ENV` after every step finishes and adds each
`KEY=VALUE` line to the workflow's environment for all *later* steps.
Writing untrusted text to that file lets the attacker append additional
env entries — they don't just set the variable you wanted, they can
also set `LD_PRELOAD`, `PATH`, `NODE_OPTIONS`, `PYTHONSTARTUP`, etc.

```bash
# This step:
echo "PR_BODY=${{ github.event.pull_request.body }}" >> "$GITHUB_ENV"

# If the PR body is:
#   benign first line
#   LD_PRELOAD=/tmp/payload.so
# ...then GITHUB_ENV now contains both PR_BODY and LD_PRELOAD.
```

Subsequent steps that exec native binaries (npm, node, python) inherit
the poisoned env and load attacker code.

## How an attacker exploits it

Open a PR whose body is:

```
benign first line
NODE_OPTIONS=--require ./malicious.js
```

The "Later step that trusts the env" runs `node -e ...`, Node reads
`NODE_OPTIONS`, evaluates the `--require` path against the checked-out
working dir (which contains attacker code from the fork), payload runs.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `template-injection` + heuristic for `$GITHUB_ENV` writes |
| poutine   | `github_env_injection` |
| checkov   | partial |
| kics      | "GitHub Env Injection" rule |

## Fix

Use the **heredoc-protected** form, or serialize to JSON and let a later
step read it back deliberately:

```yaml
- env:
    PR_BODY: ${{ github.event.pull_request.body }}
  run: |
    {
      echo 'PR_BODY<<EOF_GITHUB_ENV'
      printf '%s\n' "$PR_BODY"
      echo 'EOF_GITHUB_ENV'
    } >> "$GITHUB_ENV"
```

The heredoc form treats the entire body as one value regardless of
newlines, and `EOF_GITHUB_ENV` is unique enough that an attacker can't
trivially close it from inside the body.

## References

- GitHub Security Lab — "Keeping your GitHub Actions and workflows secure
  Part 4: GITHUB_ENV":
  https://github.blog/security/vulnerability-research/keeping-your-github-actions-and-workflows-secure-part-4-preventing-environment-injection/
