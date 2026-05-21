# Scenario 07: `workflow_run` consumes and executes a fork-PR artifact

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution),
CICD-SEC-9 (Improper Artifact Integrity Validation)

**Vulnerable workflow:** [`.github/workflows/scenario-07-workflow-run-artifact-rce.yml`](../../.github/workflows/scenario-07-workflow-run-artifact-rce.yml)

## The pattern

`workflow_run` triggers in the **base repository's context** (with secrets,
elevated `GITHUB_TOKEN`) when another workflow completes — *including* runs
of the upstream workflow triggered by fork PRs. The original intent is
"post-process the build result with privileges the build itself didn't have."

The footgun: the post-processing job often downloads an artifact uploaded
by the upstream run. That artifact was produced by *fork* code. Treating
it as data is safe; treating it as code is RCE.

## How an attacker exploits it

1. Open a fork PR that modifies the `build` workflow to upload a malicious
   `run.sh` as the `build-output` artifact. (Or, in the more subtle case,
   modifies a *real* artifact like a compiled binary to do extra work on
   first run.)
2. `workflow_run` fires after the PR's build completes.
3. The handler downloads `build-output`, marks it executable, and runs it.
4. `run.sh` reads `${{ secrets.* }}` from the env and exfiltrates.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `artipacked` / `dangerous-triggers` |
| poutine   | `workflow_run_third_party_artifact` |
| checkov   | partial |
| kics      | partial |

## Fix

- Treat artifacts from fork-PR builds as **untrusted data**, never as code.
- If you must run something, run it inside an unprivileged sub-job that
  does not have access to secrets.
- Validate artifact provenance via `${{ github.event.workflow_run.head_repository.fork }}`
  and bail out for fork-origin runs.

## References

- GitHub Security Lab — "Keeping your GitHub Actions and workflows secure
  Part 2: Untrusted input":
  https://securitylab.github.com/research/github-actions-untrusted-input/
- Adnan Khan — "ActionsInTheMirror" research on workflow_run abuse:
  https://www.legitsecurity.com/blog/github-actions-that-open-the-door-to-cicd-pipeline-attacks
