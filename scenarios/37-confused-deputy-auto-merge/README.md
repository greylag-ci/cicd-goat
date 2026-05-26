# Scenario 37: confused-deputy auto-approve / auto-merge gated by `github.actor`

**OWASP CICD-SEC mapping:** CICD-SEC-1 (Insufficient Flow Control Mechanisms)

**Vulnerable workflow:** [`.github/workflows/scenario-37-confused-deputy-auto-merge.yml`](../../.github/workflows/scenario-37-confused-deputy-auto-merge.yml)

## The pattern

An automation workflow auto-approves and auto-merges PRs gated only
by a `github.actor == '<bot>[bot]'` check:

```yaml
jobs:
  auto-approve:
    if: github.actor == 'dependabot[bot]'   # the only gate
    ...
```

The intent is "Dependabot PRs are trusted, merge them without
review." The actual semantic is "any PR whose triggering actor IS
dependabot[bot] gets auto-merged." Synacktiv
([writeup](https://www.synacktiv.com/publications/github-actions-exploitation-dependabot))
demonstrated that an attacker can bridge a Dependabot-authored
commit from their own fork into a PR against the main repo so the
triggering actor satisfies the check.

The same shape applies to **any bot-identity allowlist**: renovate,
github-actions, or a CI app installed on the repo. Each one is a
confused-deputy vector — the workflow trusts an identity it can't
prove originated where it expects.

## How an attacker exploits it

The Synacktiv walkthrough on spring-projects/spring-security has
the canonical exploit chain. Compressed:

1. Attacker has a fork of the target repo.
2. Attacker installs Dependabot on their fork.
3. Attacker waits for / triggers Dependabot to push a commit to the
   fork. The fork now has a commit authored by `dependabot[bot]`
   that the attacker controls (because they control the dependency
   that Dependabot updated).
4. Attacker opens a PR from the fork branch onto the main repo.
   The PR's "triggering actor" on the `pull_request_target` event
   is `dependabot[bot]` — the GitHub Actor of the commit's author.
5. The main repo's `auto-approve` workflow fires, the `if:` check
   passes, the PR is auto-approved and auto-merged, bypassing
   required-reviewer rules.

The merged commit contains attacker code; the repo's `GITHUB_TOKEN`
just merged it under the bot's signature.

## Expected scanner coverage

| Scanner | Detection |
|---|---|
| poutine | `confused_deputy_auto_merge` — the rule was written precisely for this pattern |
| others | ❌ — no other scanner here flags bot-identity allowlists as a confused-deputy vector |

This scenario is the only one in the corpus that exercises poutine's
`confused_deputy_auto_merge` rule, and the second CICD-SEC-1 row
alongside #23 (`actions[bot]` branch-protection bypass).

## Fix

Don't gate sensitive actions on `github.actor` alone. Authenticate
the *commit*, not the *triggering actor*:

```yaml
jobs:
  auto-approve:
    if: github.event.pull_request.user.login == 'dependabot[bot]'
    runs-on: ubuntu-latest
    steps:
      - uses: dependabot/fetch-metadata@v2     # cryptographically vetted commit lookup
        id: meta
      - if: steps.meta.outputs.update-type == 'version-update:semver-patch'
        run: gh pr review --approve "$PR_URL"
```

`dependabot/fetch-metadata` uses the Dependabot API to confirm the
PR was actually authored by Dependabot's GitHub App installation on
the target repo — not just that the triggering actor's *login*
happens to match.

## References

- Synacktiv — "GitHub Actions exploitation: Dependabot":
  https://www.synacktiv.com/publications/github-actions-exploitation-dependabot
- poutine — `confused_deputy_auto_merge` rule:
  https://boostsecurityio.github.io/poutine/rules/
