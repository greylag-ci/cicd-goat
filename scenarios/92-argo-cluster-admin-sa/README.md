# Scenario 92: Argo — cluster-admin ServiceAccount → cluster takeover

**Provider:** Argo Workflows · **OWASP:** CICD-SEC-2 (Inadequate IAM) · CICD-SEC-5 · **Severity: critical**

**Vulnerable pipeline:** [`workflow.yaml`](workflow.yaml)

## The pattern

```yaml
spec:
  serviceAccountName: cluster-admin
```

The Workflow runs as a ServiceAccount bound to cluster-admin RBAC. The
over-privilege escalation of [scenario 76](../76-argo-default-serviceaccount/README.md)
(default SA) — here the SA is deliberately all-powerful.

## How an attacker exploits it

Any step — or code injected via a separate bug — uses the automounted token to
act as **cluster-admin**: read every secret in every namespace, schedule
privileged pods on any node, create new role bindings. A single compromised
step owns the whole cluster.

> Note: the container's `securityContext` (`runAsNonRoot: true`) is irrelevant
> here — the takeover comes from the **automounted ServiceAccount token** (a
> Kubernetes API privilege), not from the container UID. Hardening the
> container doesn't reduce the SA's RBAC.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | — |
| Checkov | — |

> **All-miss — a next-gen target.** The over-privilege lives in the SA's
> RBAC (`ClusterRoleBinding`), which is *config-spread* — not in the workflow.
> No scanner here flags a workflow binding to a known over-privileged / admin
> ServiceAccount by name.

## Fix

Bind a dedicated, least-privilege ServiceAccount scoped to the target namespace
and the exact verbs the workflow needs; never use `cluster-admin` (or any
cluster-wide role) for a workflow SA; set `automountServiceAccountToken: false`
unless API access is required.

## References

- Argo — Service accounts: https://argo-workflows.readthedocs.io/en/latest/service-accounts/
- Kubernetes — Using RBAC authorization: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
