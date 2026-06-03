# Scenario 59: CircleCI — hardcoded secret in `environment:`

**Provider:** CircleCI · **OWASP:** CICD-SEC-6 (Insufficient Credential Hygiene)

**Vulnerable pipeline:** [`.circleci/config.yml`](.circleci/config.yml)

## The pattern

```yaml
jobs:
  deploy:
    environment:
      LEGACY_API_TOKEN: "deadbeefcafef00dfeedfacebadc0ffee0ddf00d"
```

A credential hardcoded into a job's `environment:` block in the committed
config — readable by anyone with repo or build-log access, and persisted in git
history. (The token is a fake hex fixture, no real provider format.)

## How an attacker exploits it

Read access to the repo hands over the credential directly. The 2023 CircleCI
breach is the cautionary tale for long-lived secrets stored in the provider at
all.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `CC-004` — secret-like environment variable not managed via context |
| Checkov | — |

## Fix

Never hardcode secrets in `config.yml`. Use CircleCI **Contexts** / project env
vars with team restrictions, and prefer OIDC short-lived credentials over
long-lived keys.

## References

- CircleCI — Jan 4 2023 incident report: https://circleci.com/blog/jan-4-2023-incident-report/
- CircleCI — Contexts: https://circleci.com/docs/contexts/
