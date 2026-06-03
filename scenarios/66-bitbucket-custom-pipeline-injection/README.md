# Scenario 66: Bitbucket — custom-pipeline variable injection

**Provider:** Bitbucket Pipelines · **OWASP:** CICD-SEC-4 (PPE) · CICD-SEC-1 (Insufficient Flow Control)

**Vulnerable pipeline:** [`bitbucket-pipelines.yml`](bitbucket-pipelines.yml)

## The pattern

```yaml
pipelines:
  custom:
    deploy:
      - variables:
          - name: TARGET
      - step:
          script:
            - ./deploy.sh --target $TARGET
```

A `custom:` pipeline declares a user-provided variable that is then used
**unquoted** in a privileged `script:` step, and the pipeline is triggerable
(UI/API) by users who shouldn't reach that step.

## How an attacker exploits it

A user with trigger rights supplies a `TARGET` value with shell metacharacters
(or an unauthorized deploy target), achieving injection or unauthorized deploy
— analogue of scenario 13 (workflow_dispatch input injection).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | — (its `BB-002` injection rule keys on `$BITBUCKET_*` contexts, not custom-pipeline user vars) |
| Checkov | — |

> **All-miss — a next-gen target.** Injection through a *custom-pipeline
> user-provided variable* (vs. a built-in `$BITBUCKET_*` context, scenario 62)
> is not covered.

## Fix

Validate/allow-list custom-pipeline variable values; quote all expansions
(`"$TARGET"`); restrict who can trigger privileged custom pipelines.

## References

- Atlassian — Custom pipelines / user-provided variables: https://support.atlassian.com/bitbucket-cloud/docs/configure-bitbucket-pipelinesyml/
