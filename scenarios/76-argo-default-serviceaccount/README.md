# Scenario 76: Argo — default ServiceAccount + token automount

**Provider:** Argo Workflows · **OWASP:** CICD-SEC-2 (Inadequate IAM)

**Vulnerable pipeline:** [`workflow.yaml`](workflow.yaml)

## The pattern

A Workflow with **no `serviceAccountName`** (so it uses the namespace **default**
ServiceAccount), whose token is automounted into the pod.

## How an attacker exploits it

The default SA often carries broader Kubernetes RBAC than the workflow needs. A
compromised step uses the automounted token to call the K8s API as default —
reading secrets, creating pods, or escalating within the namespace.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ARGO-003` — Argo workflow uses the default ServiceAccount |
| Checkov | `CKV_ARGO_1` — Workflow pods are not using the default ServiceAccount |

> Caught by both — a clean two-scanner agreement on Argo.

## Fix

Bind a dedicated least-privilege `serviceAccountName`; set
`automountServiceAccountToken: false` unless the workflow truly needs API
access; scope the SA's RBAC to exactly what the workflow requires.

## References

- Checkov — Argo Workflows policies: https://www.checkov.io/5.Policy%20Index/argo_workflows.html
- Argo — Service accounts: https://argo-workflows.readthedocs.io/en/latest/service-accounts/
