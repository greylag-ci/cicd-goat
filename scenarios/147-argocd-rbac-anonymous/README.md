# Scenario 147: Argo CD — wildcard RBAC policy + anonymous access

**Provider:** Argo CD (`argocd-rbac-cm` / `argocd-cm`) · **OWASP:** CICD-SEC-2 (Inadequate IAM) · CICD-SEC-5 · **Severity: critical**

**Vulnerable manifest:** [`argocd-cm.yaml`](argocd-cm.yaml)

## The pattern

```yaml
# argocd-rbac-cm
policy.csv: |
  p, role:dev, *, *, *, allow
  g, alice, role:admin
---
# argocd-cm
users.anonymous.enabled: "true"
```

The RBAC policy grants **wildcard** authority (a role with `*, *, *, allow`, and
a subject bound to `role:admin`), while `argocd-cm` enables **anonymous** access.

## How an attacker exploits it

With anonymous access on, an unauthenticated user reaches the API; with the
wildcard policy, the role they land on can sync, delete, or repoint **any**
Application on **any** cluster Argo CD manages — including pointing an app at an
attacker repo to deploy arbitrary workloads. Argo CD is a cluster-admin-adjacent
control plane, so this is effectively unauthenticated multi-cluster compromise.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ARGOCD-004` — _RBAC policy grants wildcard authority_ · `ARGOCD-009` — _anonymous access enabled_ |

> pipeline-check is the only scanner in this comparison that parses Argo CD
> resources.

## Fix

Disable anonymous access (`users.anonymous.enabled: "false"`); replace wildcard
RBAC with least-privilege roles scoped to specific projects/actions; never bind
broad subjects to `role:admin`.

## References

- Argo CD — RBAC configuration: https://argo-cd.readthedocs.io/en/stable/operator-manual/rbac/
- Argo CD — User management / anonymous access: https://argo-cd.readthedocs.io/en/stable/operator-manual/user-management/
