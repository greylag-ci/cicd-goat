# Scenario 06: Reusable workflow with `secrets: inherit`

**OWASP CICD-SEC mapping:** CICD-SEC-5 (Insufficient PBAC),
CICD-SEC-6 (Insufficient Credential Hygiene)

**Vulnerable workflow:**
- Caller: [`.github/workflows/scenario-06-reusable-secrets-inherit.yml`](../../.github/workflows/scenario-06-reusable-secrets-inherit.yml)
- Reusable: [`.github/workflows/_reusable-deploy.yml`](../../.github/workflows/_reusable-deploy.yml)

## The pattern

`secrets: inherit` on a reusable-workflow call passes **every** secret the
caller can see into the callee. The callee then sees them as `${{ secrets.* }}`
exactly as if they were defined on its own repo. This is convenient — and
sometimes appropriate, e.g. when both workflows live in the same repo and
the callee is genuinely trusted.

It becomes a vulnerability when:

1. The reusable workflow operates on untrusted inputs (PR-derived refs,
   user-supplied parameters), **or**
2. The reusable workflow lives in a different repo whose maintainers'
   threat model differs from the caller's, **or**
3. The caller is triggered by `pull_request` from forks, so the reusable
   workflow processes fork code with org-wide secrets in env.

## How an attacker exploits it

Open a fork PR that modifies the build script. The vulnerable caller
invokes `_reusable-deploy.yml` with `secrets: inherit`, which then checks
out the PR head, runs `npm ci`, and the postinstall script reads
`$AWS_SECRET_ACCESS_KEY` from the environment.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `secrets-inherit` |
| poutine   | partial — flags reusable + secrets pass-through |
| checkov   | limited |
| kics      | limited |

## Fix

Pass only the secrets the callee needs, explicitly:

```yaml
jobs:
  call-deploy:
    uses: ./.github/workflows/_reusable-deploy.yml
    secrets:
      AWS_DEPLOY_ROLE: ${{ secrets.AWS_DEPLOY_ROLE }}
```

And in the reusable workflow declare them:

```yaml
on:
  workflow_call:
    secrets:
      AWS_DEPLOY_ROLE:
        required: true
```

## References

- GitHub docs — "Reusing workflows":
  https://docs.github.com/en/actions/using-workflows/reusing-workflows#using-secrets-in-reusable-workflows
