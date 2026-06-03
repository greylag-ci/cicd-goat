# Scenario 97: Kubernetes — privileged container

**Provider:** Kubernetes · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: critical**

**Vulnerable file:** [`deployment.yaml`](deployment.yaml)

## The pattern

```yaml
securityContext:
  privileged: true
```

A privileged container shares the node's kernel, devices, and capabilities — it
can mount host disks, load kernel modules, and access other containers. This is
the manifest a CI/CD pipeline applies to the cluster.

## How an attacker exploits it

Code in (or injected into) the privileged container escapes to the node: reads
every pod's mounted secrets, talks to the container runtime, and takes over the
node — and from there, often the cluster.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `K8S-005` — container `securityContext.privileged: true` |
| Trivy | `KSV-0017` — privileged container |
| Checkov | `CKV_K8S_16` — container should not be privileged |
| KICS | — (honest miss: its `Container Is Privileged` query fires on the Helm Deployment in scenario 104 but **not** on this plain `Deployment` in the tested KICS version) |

> A real coverage gap worth recording: pipeline-check and Checkov both flag
> the privileged container, but KICS's privileged-container query doesn't fire
> on this `kind: Deployment` (it does fire on the identically-structured Helm
> chart in 104) — a scanner quirk this corpus surfaces precisely because the
> bug is catalogued in advance.

## Fix

Never set `privileged: true`. Set `runAsNonRoot: true`, drop `ALL` capabilities,
`allowPrivilegeEscalation: false`, a read-only root FS, and a seccomp profile;
enforce a restricted Pod Security Standard at admission.

## References

- Checkov — Kubernetes policies: https://www.checkov.io/5.Policy%20Index/kubernetes.html
- Kubernetes — Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
