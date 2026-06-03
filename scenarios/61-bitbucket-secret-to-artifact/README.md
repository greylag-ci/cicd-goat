# Scenario 61: Bitbucket — secret dumped to `artifacts:` (Mandiant pattern)

**Provider:** Bitbucket Pipelines · **OWASP:** CICD-SEC-6 · CICD-SEC-10 (masking bypass)

**Vulnerable pipeline:** [`bitbucket-pipelines.yml`](bitbucket-pipelines.yml)

## The pattern

```yaml
- step:
    script:
      - printenv > vars.txt
    artifacts:
      - vars.txt
```

Bitbucket masks **secured** variables only in log **output** — masking does not
apply to files written to artifacts. Dumping the environment to a file and
capturing it as an artifact exfiltrates secured variables in the clear.

## How an attacker exploits it

Mandiant documented real AWS keys (stored as "secured" Bitbucket variables)
dumped to a `.txt` artifact during "troubleshooting", then downloaded and used
by attackers. The "secured" flag gave false confidence.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | — |
| Checkov | — |

> **All-miss — a next-gen target.** The `env`-dump → `artifacts:` masking
> bypass is a clean static signature (env/printenv redirect to a file that an
> `artifacts:` clause then captures) that no scanner here flags yet.

## Fix

Never `printenv`/`env`-dump in pipelines; audit every `artifacts:` entry; pull
secrets at runtime from a real secrets manager rather than storing them as
Bitbucket variables.

## References

- Mandiant / Google Cloud — Holes in Your Bitbucket: https://cloud.google.com/blog/topics/threat-intelligence/bitbucket-pipeline-leaking-secrets
