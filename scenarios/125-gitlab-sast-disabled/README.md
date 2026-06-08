# Scenario 125: GitLab CI — native security scanner explicitly disabled

**Provider:** GitLab CI · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: medium**

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

```yaml
variables:
  SAST_DISABLED: "true"
  SECRET_DETECTION_DISABLED: "true"
  DEPENDENCY_SCANNING_DISABLED: "true"
```

A `*_DISABLED` CI/CD variable for a GitLab-managed scanner (SAST, Secret
Detection, Dependency Scanning, Container Scanning, DAST) is set to a truthy
value at the top level or on a job. The included scanner templates become inert,
silently dropping the finding stream the rest of the supply-chain controls
assume exists.

## How an attacker exploits it

This is a control-erosion bug, not a direct RCE: with secret detection and
dependency scanning off, a committed credential or a known-vulnerable dependency
now ships with no pipeline gate to catch it. The variable form makes it easy to
hide — pipeline-check reads both the plain scalar and the typed
`{value:, description:}` form, and (unlike a hidden *project* variable) the
in-file declaration is at least visible in code review.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-043` — _GitLab native security scanner explicitly disabled_ |
| Checkov / ciguard | — |

## Fix

Remove the `*_DISABLED: "true"` variable so the managed scanner runs again, or
scope the opt-out narrowly with `rules:` instead of disabling it pipeline-wide.
If a scanner is noisy, tune it (`SAST_EXCLUDED_PATHS`, ruleset overrides) rather
than switching it off.

## References

- GitLab — Application security (managed scanners): https://docs.gitlab.com/ee/user/application_security/
- GitLab — SAST analyzer settings: https://docs.gitlab.com/ee/user/application_security/sast/#available-cicd-variables
