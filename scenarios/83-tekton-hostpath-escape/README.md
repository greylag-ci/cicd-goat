# Scenario 83: Tekton — privileged step + hostPath node escape

**Provider:** Tekton · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: critical**

**Vulnerable pipeline:** [`pipeline.yaml`](pipeline.yaml)

## The pattern

```yaml
volumes:
  - name: host-root
    hostPath: { path: / }
steps:
  - securityContext: { privileged: true }
    volumeMounts: [{ name: host-root, mountPath: /host }]
```

The Task mounts the **node's root filesystem** into the step and runs it
privileged. The step can now read and write everything on the node.

## How an attacker exploits it

`chroot /host` gives a root shell on the node: read every other tenant's pod
secrets, steal the kubelet credentials / `admin.conf`, drop a static pod, and
own the cluster. This is the container-escape escalation of the privileged-step
bug ([scenario 72](../72-tekton-privileged-step/README.md)).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `TKN-004` — Tekton Task mounts hostPath or shares host namespaces |

> Tekton is scored by pipeline-check only in this comparison. (`TKN-002`
> privileged also fires; `TKN-004` names the canonical escape.)

## Fix

Never mount `hostPath` (especially `/`) into a build step; never run privileged.
Use a rootless builder, enforce a restricted PodSecurity standard / admission
policy that blocks hostPath + privileged, and isolate build namespaces.

## References

- Tekton — Tasks / securityContext: https://tekton.dev/docs/pipelines/tasks/
- Kubernetes — Pod Security Standards (restricted): https://kubernetes.io/docs/concepts/security/pod-security-standards/
