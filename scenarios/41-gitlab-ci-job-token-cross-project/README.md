# Scenario 41: GitLab — `CI_JOB_TOKEN` cross-project access

**Provider:** GitLab CI/CD

**OWASP CICD-SEC mapping:** CICD-SEC-2 (Inadequate IAM) · CICD-SEC-5 (Insufficient PBAC)

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

Every GitLab job is handed a `$CI_JOB_TOKEN`, scoped to the running pipeline.
Jobs use it to clone repos, pull packages, and call the API of **other**
projects:

```yaml
- git clone https://gitlab-ci-token:${CI_JOB_TOKEN}@gitlab.example.com/platform/internal-libs.git
- curl --header "JOB-TOKEN: $CI_JOB_TOKEN" https://gitlab.example.com/api/v4/projects/4242/packages
```

Whether that cross-project access is *allowed* is controlled by the **target**
project's inbound job-token allowlist (Settings → CI/CD → Job token
permissions). When that allowlist is disabled ("allow access from all
projects" — the common state on older instances), **any** project that can run
a pipeline can mint a token and reach the target.

## How an attacker exploits it

An attacker who can run a pipeline in *any* low-trust project (a fork, a
sandbox repo) mints its `CI_JOB_TOKEN` and uses it to read source, pull private
packages, or trigger pipelines in the victim project — because the victim
accepts job tokens from all projects. GitLab issue
[#243703](https://gitlab.com/gitlab-org/gitlab/-/issues/243703) is the
canonical disclosure; **CVE-2024-8641** escalated a leaked job token into a
full user session token.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| ciguard | `IAM-002` — Unrestricted `CI_JOB_TOKEN` usage |
| pipeline-check | — (no job-token-scope rule fires on this shape) |
| Checkov | — (fires only an adjacent `CKV_GITLABCI_1` "curl with CI var", not the token-scope bug) |

> A solo catch by ciguard. Reconciled against real `scanner-comparison` SARIF.

## Fix

Keep the inbound job-token allowlist **enabled** (default since GitLab 18) and
list only the specific projects/groups that legitimately need access. Prefer
fine-grained job-token permissions, or a dedicated deploy token / OIDC for
cross-project access rather than the broad `CI_JOB_TOKEN`.

## References

- GitLab Docs — CI/CD job token: https://docs.gitlab.com/ci/jobs/ci_job_token/
- GitLab issue #243703: https://gitlab.com/gitlab-org/gitlab/-/issues/243703
- CVE-2024-8641 (job token → session token)
