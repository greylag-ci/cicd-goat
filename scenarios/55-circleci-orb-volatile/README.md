# Scenario 55: CircleCI — orb pinned to `@volatile`

**Provider:** CircleCI · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable pipeline:** [`.circleci/config.yml`](.circleci/config.yml)

## The pattern

```yaml
orbs:
  aws-cli: circleci/aws-cli@volatile
```

An orb is a remote package of config (commands/jobs/executors) that executes
inline in your pipeline. `@volatile` resolves to "latest, even across breaking
major bumps" — CircleCI explicitly recommends against it.

## How an attacker exploits it

An upstream push (malicious or compromised) runs in your build on the next
trigger, with your context secrets in scope — the exact analogue of the
tj-actions tag-move class ([scenario 03](../03-action-mutable-ref/README.md)).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `CC-001` — orb not pinned to exact semver |
| Checkov | — |

## Fix

Pin orbs to an exact published version (`circleci/aws-cli@3.2.1`); require
admins to opt into uncertified orbs; bump pins with Renovate.

## References

- CircleCI — Security & supply chain: https://circleci.com/docs/security-supply-chain/
- CircleCI — Orbs best practices: https://circleci.com/docs/orbs-best-practices/
