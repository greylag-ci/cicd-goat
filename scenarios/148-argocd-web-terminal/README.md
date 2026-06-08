# Scenario 148: Argo CD — web terminal enabled (`exec.enabled`)

**Provider:** Argo CD (`argocd-cm`) · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: critical**

**Vulnerable manifest:** [`argocd-cm.yaml`](argocd-cm.yaml)

## The pattern

```yaml
# argocd-cm
exec.enabled: "true"
```

`argocd-cm` enables the **web terminal**. The Argo CD UI then offers an
interactive shell *into* the running workload pods of any Application a user can
reach.

## How an attacker exploits it

A UI session becomes pod `exec` on the target cluster — a powerful
lateral-movement and data-access primitive. Combined with broad RBAC (see
[scenario 147](../147-argocd-rbac-anonymous/README.md)) it's a direct path from
an Argo CD login to a shell inside production workloads, reading their mounted
secrets and service-account tokens.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ARGOCD-014` — _web terminal enabled via `exec.enabled`_ |

## Fix

Leave the web terminal disabled (`exec.enabled: "false"`, the default). If a
break-glass terminal is genuinely needed, restrict the `exec` RBAC verb to a
narrow, audited role and require strong authentication.

## References

- Argo CD — Web-based terminal: https://argo-cd.readthedocs.io/en/stable/operator-manual/web_based_terminal/
- Argo CD — RBAC (`exec` resource): https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/
