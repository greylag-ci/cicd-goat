# Scenario 25: Environment branch-pattern bypass

**OWASP CICD-SEC mapping:** CICD-SEC-1 (Insufficient Flow Control Mechanisms),
CICD-SEC-5 (Insufficient PBAC)

**Vulnerable workflow:** [`.github/workflows/scenario-25-environment-branch-pattern-bypass.yml`](../../.github/workflows/scenario-25-environment-branch-pattern-bypass.yml)

## The pattern

GitHub Environments give you per-environment required reviewers, wait
timers, deployment secrets, and a "Deployment branches and tags" rule
that restricts which refs can deploy to that environment. The rule
accepts **glob patterns**:

- `main` — exact match, safe.
- `main*` — matches `main`, `main-foo`, `main-attacker-fork`. Bypass.
- `release/*` — matches `release/v1`, `release/v2`, but also
  `release/anything-i-want`. Bypass if any actor can push under
  `release/`.

Combined with a workflow trigger that also uses a glob
(`branches: ['main*']`), anyone with push access (which on some
configurations includes outside collaborators) can create
`main-anything`, push code, and the production environment's gates
fire on the wrong ref.

Worse: required-reviewer gates fire at deployment time, but the
reviewer sees only "Deploy to production from branch main-evil?" —
which is exactly what they're being asked to approve. The malicious
code in the branch isn't auto-displayed in the approval dialog.

## How an attacker exploits it

1. Get push access to the repo (collaborator, member of a team with
   write, etc.) — *or* compromise a single contributor's PAT.
2. `git checkout -b main-config-update` and push your payload.
3. The workflow's `on: push: branches: ['main*']` fires.
4. The deploy job's `environment: production` is gated on the branch
   pattern `main*`, which `main-config-update` matches.
5. If there's a required reviewer, they see a generic "approve
   production deploy" prompt and (statistically often enough) click
   through. The payload runs in production with the environment's
   secrets.

## Expected scanner coverage

| Scanner            | Detection                                                                          |
| :----------------- | :--------------------------------------------------------------------------------- |
| **pipeline-check** | ⚠️ Flags glob trigger + missing exact-branch pin in environment ref-pattern rule |
| zizmor             | ⚠️ `dangerous-triggers` partial — catches the wildcard branch trigger             |
| poutine            | ❌                                                                                 |
| KICS               | ❌                                                                                 |
| Checkov            | ❌                                                                                 |
| Trivy              | ❌                                                                                 |
| Gitleaks           | —                                                                                  |

> Like Scenarios 10 and 22, this is partially out-of-band: the
> deployment-branches rule lives in GitHub repo settings, not in any
> file. Scanners can warn about the workflow side (wildcard trigger,
> missing pinned environment reviewer) but can't see the matching
> setting in repo config.

## Fix

Two changes, both required:

1. **Workflow trigger.** Pin to exact branches:
   ```yaml
   on:
     push:
       branches: [main]
   ```
2. **Environment "Deployment branches and tags" rule.** Choose
   *"Selected branches and tags"* and add `main` exactly. Avoid the
   "Branch name pattern" mode unless you've audited the pattern.

For high-blast-radius environments, also require deployment from a
**protected tag** rather than a branch — tags are immutable in a way
branches aren't.

## References

- GitHub docs — Using environments for deployment:
  https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
- OWASP CICD-SEC-1:
  https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms
