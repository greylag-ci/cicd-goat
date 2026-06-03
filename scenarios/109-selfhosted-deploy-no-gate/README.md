# Scenario 109: GHA — self-hosted deploy without an environment gate

**Provider:** GitHub Actions · **OWASP:** CICD-SEC-1 (Insufficient Flow Control Mechanisms) · CICD-SEC-7 · **Severity: high**

**Vulnerable file:** [`.github/workflows/scenario-109-selfhosted-deploy-no-gate.yml`](../../.github/workflows/scenario-109-selfhosted-deploy-no-gate.yml)

## The pattern

```yaml
jobs:
  deploy:
    runs-on: [self-hosted, production]
    steps:
      - run: kubectl apply -f k8s/ --context prod
```

A deploy job runs on a **self-hosted runner** — persistent org infrastructure
that holds standing production credentials (a kubeconfig, a long-lived cloud
role) and survives across jobs — with **no `environment:` gate**. The
ungated-deploy gap of scenario 108, but on infrastructure with a far larger
blast radius.

## How an attacker exploits it

A low-privilege trigger (a push, a self-merged PR) reaches persistent infra that
ships to prod with standing credentials and no human approval. Worse, because
the runner persists, an attacker who compromises it — or who lands a job on it
from an untrusted trigger — can harvest the standing credentials and deploy at
will.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GHA-014` (deploy missing environment) + `GHA-012` (self-hosted runner without ephemeral marker) — names both facets. (Newer pipeline-check also has the dedicated `GHA-112` for this combination.) |
| zizmor / poutine / KICS / Checkov / actionlint / octoscan | — (miss) |

## Fix

Bind the job to a protected `environment:` with required reviewers and a
deployment-branch policy; prefer **ephemeral** self-hosted runners
(actions-runner-controller, `--ephemeral`) so a job can't inherit state or
credentials; keep untrusted-trigger jobs off the self-hosted fleet entirely.

## References

- GitHub — self-hosted runner security & hardening with environments: https://docs.github.com/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#self-hosted-runner-security
