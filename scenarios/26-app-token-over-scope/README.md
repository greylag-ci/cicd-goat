# Scenario 26: GitHub App token minted with no `permissions:` filter

**OWASP CICD-SEC mapping:** CICD-SEC-5 (Insufficient Pipeline-Based Access Controls)

**Vulnerable workflow:** [`.github/workflows/scenario-26-app-token-over-scope.yml`](../../.github/workflows/scenario-26-app-token-over-scope.yml)

## The pattern

Two trends collide:

1. The community is migrating from long-lived PATs to **GitHub Apps**
   minting short-lived installation tokens via
   `actions/create-github-app-token`. Good.
2. The App's installation permissions are usually granted broadly
   ("contents: write, packages: write, actions: write, pull-requests:
   write, ...") because configuring granular per-install permissions
   is tedious and most installers click through.

The token-minting action *can* request a `permissions:` subset at mint
time. When it doesn't, the token inherits **every** permission the App
has on the org. A workflow that needs only `contents: write` (to push
a release tag) ends up with a token that can also write packages,
actions, and deployments. If that workflow has any other vuln —
script injection, unsafe action, unsafe checkout — the blast radius is
"everything the App can do."

## How an attacker exploits it

The exploit isn't this step alone; it's combining over-broad token
minting with any vector that gives an attacker control inside the
workflow:

- Combine with [Scenario 02 (script injection)](../02-script-injection-issue-title/README.md):
  attacker controls a shell step, exfiltrates the token, uses it
  against any scope the App holds.
- Combine with [Scenario 03 (mutable action ref)](../03-action-mutable-ref/README.md):
  upstream-compromise of an unpinned action runs with the broad token.
- Combine with [Scenario 12 (persist-credentials)](../12-persist-credentials-leak/README.md):
  the token from `app-token` ends up in `.git/config` and any later
  step reads it.

## Expected scanner coverage

| Scanner            | Detection                                                                   |
| :----------------- | :-------------------------------------------------------------------------- |
| **pipeline-check** | ✅ Flags `create-github-app-token` without `permissions:` filter            |
| zizmor             | ⚠️ Limited — flags App-token use but not the missing scope filter          |
| poutine            | ❌                                                                          |
| KICS               | ❌                                                                          |
| Checkov            | ❌                                                                          |
| Trivy              | ❌                                                                          |
| Gitleaks           | —                                                                           |

## Fix

Always pass a `permissions:` filter at token-mint time:

```yaml
- id: app-token
  uses: actions/create-github-app-token@v1
  with:
    app-id: ${{ secrets.RELEASE_APP_ID }}
    private-key: ${{ secrets.RELEASE_APP_KEY }}
    owner: ${{ github.repository_owner }}
    permissions: >-
      {"contents":"write"}
```

The minted token will have *only* the requested scopes, even if the
App's install grants more. For workflows that legitimately need more,
list them explicitly so a future reader knows exactly why each scope
is there.

## References

- `actions/create-github-app-token` docs:
  https://github.com/actions/create-github-app-token
- GitHub docs — Authenticating with a GitHub App in a workflow:
  https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app
