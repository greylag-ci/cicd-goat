# Scenario 75: Argo — privileged / root container

**Provider:** Argo Workflows · **OWASP:** CICD-SEC-7 (Insecure System Configuration)

**Vulnerable pipeline:** [`workflow.yaml`](workflow.yaml)

## The pattern

```yaml
container:
  securityContext:
    privileged: true
    runAsUser: 0
```

An Argo template container runs privileged and as root. A privileged pod shares
the node kernel and can reach the host and other workloads.

## How an attacker exploits it

On a shared cluster, the privileged container escapes to the node — host
compromise and cross-tenant access. Analogue of scenario 72 (Tekton) /
57 (CircleCI `machine`).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ARGO-002` — Argo template container runs privileged or as root |
| Checkov | `CKV_ARGO_2` — Workflow pods run as non-root user |

> Caught by both — a clean two-scanner agreement on Argo.

## Fix

Set `runAsNonRoot: true` and a non-zero `runAsUser`; never `privileged: true`;
drop all capabilities; use a rootless builder for image builds.

## References

- Checkov — Argo Workflows policies: https://www.checkov.io/5.Policy%20Index/argo_workflows.html
- Argo — Workflow pod security: https://argo-workflows.readthedocs.io/en/latest/workflow-pod-security-context/
