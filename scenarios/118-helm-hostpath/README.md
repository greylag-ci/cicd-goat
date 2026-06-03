# Scenario 118: Helm — hostPath mount of node root in a chart

**Provider:** Helm · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: critical**

**Vulnerable files:** [`Chart.yaml`](Chart.yaml) · [`templates/daemonset.yaml`](templates/daemonset.yaml)

## The pattern

```yaml
volumes:
  - name: host-root
    hostPath: { path: / }
```

The chart's DaemonSet mounts the node's root filesystem into the pod. Installing
it gives every pod node-level read/write — the kubelet config, the container
runtime socket, other pods' secrets. The manifest twin of scenario 98, shipped
as a packaged chart that lands on every node.

## How an attacker exploits it

`chroot /host` (or writing to the kubelet / runtime socket) from the container
gives node-level control, then cluster takeover. As a DaemonSet the blast radius
is every node in the cluster, and the bug travels with the chart.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| Trivy | `KSV-0023` — hostPath volume mounted (renders the chart) |
| pipeline-check | `K8S-014` — hostPath references a sensitive host directory |
| Checkov | — (no hostPath-specific canonical fires; general securityContext checks are noise) |
| KICS | — (Helm not in KICS's scored providers here) |

## Fix

Don't use `hostPath` (especially `/`) in chart defaults; if a host mount is
unavoidable, scope it to a read-only subPath and enforce a restricted Pod
Security Standard that denies hostPath at admission.

## References

- Kubernetes — hostPath volumes (security): https://kubernetes.io/docs/concepts/storage/volumes/#hostpath
