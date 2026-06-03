# Scenario 60: CircleCI — uncertified third-party orb

**Provider:** CircleCI · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable pipeline:** [`.circleci/config.yml`](.circleci/config.yml)

## The pattern

```yaml
orbs:
  deploy-tool: random-vendor/deploy-tool@1.2.3
```

An orb from an **uncertified** (non-`circleci/*`) namespace. Only `circleci/*`
orbs are CircleCI-certified; a third-party orb is arbitrary remote config that
runs inline in your pipeline with your context secrets in scope. Distinct from
scenario 55 (a *volatile version* of a certified orb) — here the orb is pinned
to an exact version, but the **publisher itself is untrusted**.

## How an attacker exploits it

A compromised or malicious third-party publisher ships an orb that exfiltrates
the context secrets passed to its jobs/commands.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | — (pins to exact semver, so the orb-pinning rule correctly stays silent; no untrusted-publisher rule) |
| Checkov | — |

> **All-miss — a next-gen target.** Detecting an *uncertified orb namespace*
> (publisher trust, as opposed to version mutability) is a candidate rule no
> scanner here carries.

## Fix

Restrict orbs to the `circleci/*` namespace and a vetted internal allowlist;
require admin opt-in for uncertified orbs (Org Settings → Security); review
third-party orb source before use.

## References

- CircleCI — Security & supply chain (orb certification): https://circleci.com/docs/security-supply-chain/
