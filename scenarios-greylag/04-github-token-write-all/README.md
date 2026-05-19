# Scenario 04: GITHUB_TOKEN with `permissions: write-all`

**OWASP CICD-SEC mapping:** CICD-SEC-5 (Insufficient Pipeline-Based Access Controls)

**Vulnerable workflow:** [`.github/workflows/scenario-04-github-token-write-all.yml`](../../.github/workflows/scenario-04-github-token-write-all.yml)

## The pattern

Every workflow run gets an automatically-issued `GITHUB_TOKEN`. The scopes
that token carries are controlled by the workflow's `permissions:` block.
`permissions: write-all` (or omitting `permissions:` entirely on repos that
default to permissive) hands the token write access to **every** scope:
contents, packages, deployments, pages, issues, pull-requests, statuses, ...

On its own this is just "violation of least privilege." Combined with any
*other* vulnerability — script injection (Scenario 02), unpinned action
(Scenario 03), unsafe checkout (Scenario 01) — it converts a small breach
into full repo takeover.

## How an attacker exploits it

The token itself is harmless; the impact appears when something else lets
an attacker run *with* the token. With write-all the attacker can:

- Push code to any branch (including default), enabling self-perpetuating
  workflows.
- Publish packages.
- Create deployments to GitHub Pages or environments without protection.
- Edit issues/PRs to look like maintainer comments.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `excessive-permissions` |
| poutine   | `excessive_permissions` |
| checkov   | `CKV_GHA_4` (top-level write permissions) |
| kics      | "Token Permissions Not Read-Only" |
| trivy     | "Job permissions are not minimal" |
| gitleaks  | n/a |

## Fix

Set `permissions: read-all` at the workflow top (or `permissions: {}` to
deny all by default), then grant the minimum each job actually needs:

```yaml
permissions: read-all

jobs:
  release:
    permissions:
      contents: write   # to tag the release
      packages: write   # to publish
    ...
```

## References

- GitHub docs — "Permissions for the GITHUB_TOKEN":
  https://docs.github.com/en/actions/security-guides/automatic-token-authentication
