# Scenario 03: Third-party action pinned to a mutable ref

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable workflow:** [`.github/workflows/scenario-03-action-mutable-ref.yml`](../../.github/workflows/scenario-03-action-mutable-ref.yml)

## The pattern

`uses: org/action@<ref>` resolves the ref *at job start*. If `<ref>` is a
branch (`@main`, `@master`) or a tag the upstream can move (`@v1`), an
upstream compromise — or a deliberate malicious tag-move — runs in your CI
the next time it triggers.

## Real-world incident: tj-actions/changed-files (CVE-2025-30066)

In March 2025 an attacker gained write access to the `tj-actions/changed-files`
repo and force-moved every published tag (`v1`, `v35`, `v44`, ...) to point
at a malicious commit that exfiltrated CI secrets via the runner's process
memory. Tens of thousands of repos that pinned by tag executed the malicious
code on the next workflow run. Repos that pinned to a commit SHA were
unaffected — the SHA is immutable.

## How an attacker exploits it

1. Compromise the action upstream (phishing a maintainer, exploiting a
   misconfigured workflow on the action's repo, etc.) — or *be* the maintainer.
2. Push a new commit that does whatever you want (dump env, write to
   `~/.gitconfig`, etc.).
3. Move every release tag to that commit (`git tag -f v1`, `git push -f --tags`).
4. Wait. Every downstream pinning by tag executes your code on next CI run.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `unpinned-uses` |
| poutine   | `unpinned_action` |
| checkov   | `CKV_GHA_3` family |
| kics      | "Unpinned Actions Full Length Commit SHA" |
| trivy     | "Pin actions to full-length commit SHA" |
| gitleaks  | n/a |

## Fix

Pin every third-party action to a **full 40-char commit SHA**:

```yaml
- uses: third-party-org/some-deploy-action@1a2b3c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b  # v1.2.3
```

For first-party actions (`actions/*`, `github/*`) the policy can be relaxed
to tag-pinning if you trust GitHub's tag-protection.

## References

- StepSecurity write-up of tj-actions/changed-files compromise:
  https://www.stepsecurity.io/blog/harden-runner-detection-tj-actions-changed-files-action-is-compromised
- GitHub docs — "Using third-party actions":
  https://docs.github.com/en/actions/security-guides/security-hardening-for-github-actions#using-third-party-actions
