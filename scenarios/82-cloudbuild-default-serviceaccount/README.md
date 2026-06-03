# Scenario 82: Cloud Build — runs as the default service account

**Provider:** Google Cloud Build · **OWASP:** CICD-SEC-2 (Inadequate IAM)

**Vulnerable pipeline:** [`cloudbuild.yaml`](cloudbuild.yaml)

## The pattern

A Cloud Build config with **no `serviceAccount:`** field, so the build runs as
the default Cloud Build service account.

## How an attacker exploits it

The default Cloud Build SA historically carries broad project roles. A
compromised build step (e.g. via a poisoned step image or an injected command)
inherits those roles and pivots across the GCP project — far more than the build
needs.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GCB-002` — Cloud Build uses the default service account |

> Cloud Build is scored by pipeline-check only in this comparison.

## Fix

Bind a dedicated, least-privilege user-managed service account
(`serviceAccount: projects/$PROJECT/serviceAccounts/ci-build@...`); grant only
the roles the build needs; pair with `options: logging: CLOUD_LOGGING_ONLY`.

## References

- Google Cloud — Configure user-specified service accounts: https://cloud.google.com/build/docs/securing-builds/configure-user-specified-service-accounts
