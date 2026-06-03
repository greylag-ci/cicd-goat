# Scenario 117: Helm — container runs as root + privilege escalation

**Provider:** Helm · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: high**

**Vulnerable files:** [`Chart.yaml`](Chart.yaml) · [`templates/deployment.yaml`](templates/deployment.yaml)

## The pattern

```yaml
securityContext:
  runAsNonRoot: false
  allowPrivilegeEscalation: true
```

The chart ships a container that runs as root and permits privilege escalation,
with no capability drop. The hardening baseline (`runAsNonRoot`,
`allowPrivilegeEscalation: false`, drop `ALL`, seccomp) is absent. The
`securityContext` is literal in the template, so it's detectable without
rendering chart values.

## How an attacker exploits it

A foothold in the container escalates via setuid/file-capability paths, then
combines with any kernel/runtime bug to break out — far easier than from a
locked-down, non-root container. The bug travels with the chart wherever it's
installed.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Trivy | `KSV-0001` — process can elevate its own privileges (renders the chart) |
| pipeline-check | `K8S-006` (allowPrivilegeEscalation not false) + `K8S-007` (runAsNonRoot not true) |
| Checkov | `CKV_K8S_20` — containers should not run with allowPrivilegeEscalation |
| KICS | — (Helm not in KICS's scored providers here) |

## Fix

Set `runAsNonRoot: true`, a non-zero `runAsUser`, `allowPrivilegeEscalation:
false`, drop `ALL` capabilities, and a seccomp profile in the chart defaults;
enforce the restricted Pod Security Standard at admission.

## References

- Kubernetes — Pod Security Standards (restricted): https://kubernetes.io/docs/concepts/security/pod-security-standards/
