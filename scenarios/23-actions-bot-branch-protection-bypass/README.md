# Scenario 23: Branch protection bypass via `github-actions[bot]`

**OWASP CICD-SEC mapping:** CICD-SEC-1 (Insufficient Flow Control Mechanisms)

**Vulnerable workflow:** [`.github/workflows/scenario-23-actions-bot-branch-protection-bypass.yml`](../../.github/workflows/scenario-23-actions-bot-branch-protection-bypass.yml)

## The pattern

Teams set up branch protection on `main`: required reviewers, required
status checks, no direct pushes. They also want auto-formatting,
auto-versioning, or "release please"-style automation to keep the
branch tidy. The tension resolves in repo settings → Branches →
**"Allow specified actors to bypass required pull requests"**, with
`github-actions[bot]` (or a dedicated `release-bot` PAT) on the
allowlist.

Now any workflow that runs as that actor can push directly to `main`:

- The auto-format workflow runs on a schedule. Good.
- The auto-format workflow runs on a `workflow_dispatch` anyone can
  trigger via the API. Less good.
- The auto-format workflow has a script injection vuln (Scenario 02)
  or unsafe checkout (Scenario 01). Now any external actor who can
  trigger the workflow has write-to-main.

The bypass-list isn't the bug — it's the *amplifier*. Combined with
any other single-step weakness, the impact upgrades from "the runner
gets owned" to "the protected branch gets owned."

## How an attacker exploits it

The exploit is whichever upstream vuln gets you arbitrary code in this
workflow's context. Once there:

```bash
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git remote set-url origin "https://x-access-token:${GITHUB_TOKEN}@github.com/${GITHUB_REPOSITORY}.git"
echo "# pwned" >> README.md
git add README.md
git commit -m "chore: housekeeping"
git push origin HEAD:main          # ← bypasses all the protection
```

## Expected scanner coverage

| Scanner            | Detection                                                                   |
| :----------------- | :-------------------------------------------------------------------------- |
| **pipeline-check** | ✅ Flags `contents: write` + `git push` to main + missing branch-policy doc |
| zizmor             | ⚠️ Catches the `contents: write` + token interaction                       |
| poutine            | ❌ (the bypass is a GitHub setting, not in the YAML)                        |
| KICS               | ❌                                                                          |
| Checkov            | ❌                                                                          |

> The bypass *configuration* lives in GitHub repo settings, not in any
> file in the repo — but the workflow that *uses* the bypass is visible
> to scanners. Pipeline-check's CICD-SEC-1 rule chain flags the
> push-to-protected-branch pattern; the field doesn't have an equivalent
> rule yet.

## Fix

Two complementary mitigations:

1. **Remove `github-actions[bot]` from the branch-protection bypass
   list.** Run the bot's commits through a PR like any other change.
   "Auto-format" workflows that open a PR for review are a tiny
   ergonomic cost relative to a writable `main`.
2. **Scope the workflow to the bare minimum.** If you *must* push back
   to the repo, make it a dedicated workflow that does only that, runs
   only on a tightly-scoped trigger, has `permissions: contents: write`
   and *nothing else*, and never checks out untrusted input.

## References

- GitHub docs — Branch protection rules:
  https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
- OWASP CICD-SEC-1:
  https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms
