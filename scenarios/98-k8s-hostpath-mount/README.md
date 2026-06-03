# Scenario 98: Kubernetes — hostPath mount of the node root

**Provider:** Kubernetes · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: critical**

**Vulnerable file:** [`pod.yaml`](pod.yaml)

## The pattern

```yaml
volumes:
  - name: host-root
    hostPath: { path: / }
```

The Pod mounts the node's root filesystem. The container reads/writes the
node's `/` — the kubelet config, the container runtime socket, other pods'
mounted secrets. The manifest twin of the Tekton/Argo hostPath escapes
(scenarios 83 / 84).

## How an attacker exploits it

`chroot /host` (or writing to `/host/etc/...` / the kubelet) gives node-level
control: harvest other workloads' secrets, drop a static pod, take over the node
and the cluster.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `K8S-014` — hostPath references a sensitive host directory |
| Trivy | `KSV-0023` — hostPath volume mounted |
| Checkov | — (no hostPath-specific canonical fires; many securityContext checks do, as noise) |
| KICS | `Workload Mounting With Sensitive OS Directory` (`5308a7a8-…`) — hostPath of node root |

## Fix

Don't use `hostPath` (especially `/`); if a host mount is unavoidable, scope it
to a specific read-only subPath and enforce a restricted Pod Security Standard /
admission policy that denies hostPath.

## References

- Kubernetes — hostPath volumes (security): https://kubernetes.io/docs/concepts/storage/volumes/#hostpath
- Checkov — Kubernetes policies: https://www.checkov.io/5.Policy%20Index/kubernetes.html
