# Scenario 149: Argo CD — plaintext repository credentials + any-source AppProject

**Provider:** Argo CD (`argocd-cm` + `AppProject`) · **OWASP:** CICD-SEC-6 (Insufficient Credential Hygiene) · CICD-SEC-5 · **Severity: critical**

**Vulnerable manifest:** [`argocd.yaml`](argocd.yaml)

## The pattern

```yaml
# argocd-cm
repositories: |
  - url: https://git.internal.example.com/acme/deploy
    username: ci-bot
    password: <literal token>
---
kind: AppProject
spec:
  sourceRepos: ['*']
```

`argocd-cm` stores a repository credential as a **literal password** (instead of
the documented `passwordSecret` indirection), and the `AppProject` permits **any**
source repository (`sourceRepos: ['*']`).

## How an attacker exploits it

The plaintext token is committed in cluster config (and anything that can read
the ConfigMap — or the Git repo it lives in — gets it). The wide-open
`sourceRepos: ['*']` lets an Application sync from a repo the platform team never
vetted, so an attacker who can create/edit an Application points it at their own
manifests and deploys arbitrary workloads.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ARGOCD-005` — _repository entry stores plaintext credentials_ · `ARGOCD-001` — _AppProject permits any source repository_ |

> The wide-open destinations here also trip `ARGOCD-002`; the plaintext
> credential (`ARGOCD-005`) and any-source project (`ARGOCD-001`) are the
> canonical bugs.

## Fix

Reference credentials via `passwordSecret` / `sshPrivateKeySecret` (a Kubernetes
Secret, not a literal), and scope each `AppProject`'s `sourceRepos` /
`destinations` to the specific repos, clusters, and namespaces it needs.

## References

- Argo CD — Private repositories / credential secrets: https://argo-cd.readthedocs.io/en/stable/operator-manual/declarative-setup/#repositories
- Argo CD — Projects (`sourceRepos`): https://argo-cd.readthedocs.io/en/stable/user-guide/projects/
