# Scenario 99: Kubernetes — root container + `allowPrivilegeEscalation`

**Provider:** Kubernetes · **OWASP:** CICD-SEC-7 (Insecure System Configuration)

**Vulnerable file:** [`pod.yaml`](pod.yaml)

## The pattern

```yaml
securityContext:
  runAsUser: 0
  allowPrivilegeEscalation: true
```

The container runs as root and permits privilege escalation — a process can
gain more privileges than its parent (setuid binaries, file capabilities),
which eases container breakout. The hardening baseline (`runAsNonRoot`,
`allowPrivilegeEscalation: false`, drop `ALL` caps, seccomp) is absent.

## How an attacker exploits it

A foothold in the container leverages a setuid/capability path to escalate, then
combines with any kernel/runtime bug to break out — far easier than from a
locked-down, non-root, no-escalation container.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `K8S-035` — container `runAsUser` is 0 (root) |
| Checkov | `CKV_K8S_20` — containers should not run with `allowPrivilegeEscalation` |
| KICS | `Privilege Escalation Allowed` (`5572cc5e-…`) — `allowPrivilegeEscalation` not false |

## Fix

Set `runAsNonRoot: true`, a non-zero `runAsUser`, `allowPrivilegeEscalation:
false`, drop `ALL` capabilities, and a seccomp profile; enforce the restricted
Pod Security Standard.

## References

- Kubernetes — Pod Security Standards (restricted): https://kubernetes.io/docs/concepts/security/pod-security-standards/
