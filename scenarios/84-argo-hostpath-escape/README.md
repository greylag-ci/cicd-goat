# Scenario 84: Argo — hostPath mount → node filesystem escape

**Provider:** Argo Workflows · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: critical**

**Vulnerable pipeline:** [`workflow.yaml`](workflow.yaml)

## The pattern

```yaml
volumes:
  - name: host-root
    hostPath: { path: / }
templates:
  - container:
      volumeMounts: [{ name: host-root, mountPath: /host }]
```

The Workflow mounts the **node's root filesystem** into the template container.

## How an attacker exploits it

`chroot /host` reaches the node: read other workloads' mounted secrets, modify
the kubelet, drop a static pod, take over the node and the cluster. Escalation
of the privileged-container bug ([scenario 75](../75-argo-privileged-container/README.md)).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ARGO-004` — Argo workflow mounts hostPath or shares host namespaces |
| Checkov | — (`CKV_ARGO_*` cover default-SA / non-root, not hostPath) |

## Fix

Never mount `hostPath` into a workflow pod; enforce a restricted PodSecurity
standard / OPA-Gatekeeper / Kyverno policy that denies hostPath + host
namespaces; isolate the workflow namespace.

## References

- Argo — Workflow pod security context: https://argo-workflows.readthedocs.io/en/latest/workflow-pod-security-context/
- Kubernetes — Pod Security Standards: https://kubernetes.io/docs/concepts/security/pod-security-standards/
