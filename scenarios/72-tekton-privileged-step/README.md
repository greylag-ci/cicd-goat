# Scenario 72: Tekton — privileged / root step

**Provider:** Tekton · **OWASP:** CICD-SEC-7 (Insecure System Configuration)

**Vulnerable pipeline:** [`pipeline.yaml`](pipeline.yaml)

## The pattern

```yaml
steps:
  - name: build
    securityContext:
      privileged: true
      runAsUser: 0
```

A Tekton step runs privileged and as root. A privileged step shares the node
kernel and can reach the host, the container runtime, and other workloads.

## How an attacker exploits it

On a shared cluster, the privileged step escapes its container to the node —
host compromise and cross-tenant access to other pipelines' workspaces and
credentials.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `TKN-002` — Tekton step runs privileged or as root |

## Fix

Use a rootless image builder (kaniko / buildkit-rootless); set
`runAsNonRoot: true`, a non-zero `runAsUser`, and drop all capabilities; never
set `privileged: true` on a build step.

## References

- Tekton — Security: https://tekton.dev/docs/pipelines/tasks/#specifying-securitycontext
