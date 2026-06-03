# Scenario 88: Bitbucket — fork PR pipeline exposes secrets

**Provider:** Bitbucket Pipelines · **OWASP:** CICD-SEC-6 (Insufficient Credential Hygiene) · CICD-SEC-4 · **Severity: critical**

**Vulnerable pipeline:** [`bitbucket-pipelines.yml`](bitbucket-pipelines.yml)

## The pattern

A `pull-requests:` pipeline runs fork-PR code with account/repository variables
in scope, and the repo enables pipelines for forked repositories:

```yaml
pipelines:
  pull-requests:
    '**':
      - step:
          script:
            - ./build.sh                                  # fork-controlled
            - curl -H "Authorization: Bearer $DEPLOY_TOKEN" https://deploy.example.com/release
```

## How an attacker exploits it

The fork's PR edits the pipeline to exfiltrate the in-scope variables (or
defeats secured-var masking by writing them to an artifact,
[scenario 61](../61-bitbucket-secret-to-artifact/README.md)). Bitbucket
withholds *secured* vars from fork PRs by default, so the bug bites when the var
is unsecured or fork-pipeline runs are enabled with secrets in reach. Bitbucket
analogue of [scenario 01](../01-prtarget-checkout-head/README.md).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `BB-004` — deploy step missing a `deployment:` environment gate |
| Checkov | — |

> `BB-004` flags the missing environment gate — the control that would stop a
> fork-PR-triggered step from running with deploy secrets. The fork-pipeline
> account toggle itself is config-spread (not in the file).

## Fix

Mark all sensitive variables **secured**; don't enable pipelines on forked
repos for repos holding deploy secrets; gate privileged steps behind a
`deployment:` environment with restricted access; don't run privileged steps on
`pull-requests:`.

## References

- Atlassian — Variables and secrets (secured vars / fork PRs): https://support.atlassian.com/bitbucket-cloud/docs/variables-and-secrets/
- Mandiant — Holes in Your Bitbucket: https://cloud.google.com/blog/topics/threat-intelligence/bitbucket-pipeline-leaking-secrets
