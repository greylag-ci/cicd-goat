# Scenario 36: environment secret read in one job, consumed in another with no `environment:` binding

**OWASP CICD-SEC mapping:** CICD-SEC-5 (Insufficient Pipeline-Based
Access Controls), CICD-SEC-2 (Inadequate Identity and Access
Management)

**Vulnerable workflow:** [`.github/workflows/scenario-36-environment-secret-no-binding.yml`](../../.github/workflows/scenario-36-environment-secret-no-binding.yml)

## The pattern

GitHub's *environment protection rules* (required reviewers, wait
timer, deployment-branches-rule, custom protection rules) are
attached to jobs that bind `environment:`. The protection fires
once, when that job starts.

A common misuse: read the env-protected secret in a job that has
`environment: production`, then ship the secret value to a sibling
job through `needs.<job>.outputs.*`. The sibling job has no
`environment:` binding of its own, so none of `production`'s
protection rules apply to whatever it does with the secret —
deployment branches, wait timers, custom Slack-approval webhooks,
all bypassed.

The "minting" job got reviewed. The job that does the *actual*
production-touching work didn't.

## How an attacker exploits it

The exploitation here is **policy bypass by an insider**, not by an
external attacker:

1. Maintainer A submits a PR that modifies the `deploy` job's
   request body — say, redirecting traffic to a different region
   or changing the deployment payload.
2. The PR triggers the workflow. The `mint` job pauses, required
   reviewer (also maintainer A or a colleague) sees a familiar
   "production deploy" job awaiting approval and clicks approve —
   because the reviewer was *trained* that approving `production`
   means approving the deploy.
3. The reviewer's approval gates ONLY the secret mint. The actual
   deploy step runs with no further review, deploying whatever PR A
   put in.

The same shape lets an attacker who has gained limited write access
to the repo escalate: they can ship arbitrary `deploy` steps that
the env-protected secret reaches, provided they can get the `mint`
job approved once.

## Expected scanner coverage

| Scanner | Detection |
|---|---|
| _all 7_ | ❌ — no scanner here ships a rule that pairs "secret read inside `environment:`" with "secret consumed in a job without `environment:`" |

This scenario joins the "hard cases" group (#10 / #22 / #25 / #35) —
the bug spans two jobs and requires cross-job dataflow that the
field's current YAML pattern matchers don't carry. The right next-
generation rule would be a small taint trace: secret → step output
→ job output → `needs.<>.outputs.*` consumer; if the consumer's job
has no `environment:`, flag.

## Fix

Bind `environment: production` on the job that actually consumes the
secret — not just the one that reads it:

```yaml
deploy:
  needs: mint
  environment: production    # ← required-reviewer gate fires here too
  runs-on: ubuntu-latest
  steps:
    - run: |
        curl -X POST https://api.example.com/deploy \
          -H "Authorization: Bearer ${{ needs.mint.outputs.deploy_token }}"
```

Better: don't pass the secret through outputs at all. Move the deploy
shell into the same job as the secret read, or use OIDC to mint a
short-lived deploy credential per-job from the cloud IAM side.

## References

- GitHub docs — "Using environments for deployment":
  https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
- GitHub docs — "Environment protection rules":
  https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment#environment-protection-rules
