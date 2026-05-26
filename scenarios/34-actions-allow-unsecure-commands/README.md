# Scenario 34: `ACTIONS_ALLOW_UNSECURE_COMMANDS` re-enabled

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-34-actions-allow-unsecure-commands.yml`](../../.github/workflows/scenario-34-actions-allow-unsecure-commands.yml)

## The pattern

Before October 2020, GitHub Actions allowed steps to issue *workflow
commands* over stdout — lines like `::set-env name=X::value` mutated
the runner's environment for every subsequent step, and `::add-path::`
prepended directories to PATH. Project Zero
[bug 2070](https://bugs.chromium.org/p/project-zero/issues/detail?id=2070)
showed this was trivially abusable: any step that echoed
attacker-controlled text could redirect PATH or inject environment
variables, gaining persistent control over the rest of the job.

GitHub disabled the commands by default and added the
`ACTIONS_ALLOW_UNSECURE_COMMANDS=true` env switch as an escape hatch
"only for legacy scripts you can't otherwise upgrade." Setting it to
`true` resurrects the entire vulnerability class.

## How an attacker exploits it

Any step in this workflow that emits a line matching `::set-env name=X::Y`
or `::add-path::Y` becomes a primitive for the attacker who supplied
`Y` (a fetched manifest, an issue body parsed earlier in the job, a
crafted commit message, a `cat manifest.txt` that included
attacker-controlled bytes). With `ACTIONS_ALLOW_UNSECURE_COMMANDS=true`,
the line is interpreted; later steps run inside the poisoned env.

The most dangerous payload is PATH prepending — once `/tmp/evil` is
first in PATH, every `make`, `git`, `curl`, `gh` call that follows
runs the attacker's binary instead of the real one.

## Expected scanner coverage

| Scanner | Detection |
|---|---|
| KICS | `60fd272d-…` — _Unsecured Commands_ (fires when `ACTIONS_ALLOW_UNSECURE_COMMANDS=true` is present in `env:`) |
| Checkov | `CKV_GHA_1` — _Ensure ACTIONS_ALLOW_UNSECURE_COMMANDS isn't true_ |
| octoscan | `unsecure-commands` — same pattern |
| others | ❌ — no rule for this specific anti-pattern at present |

This scenario is the only one in the corpus that exercises KICS's
`unsecured_commands`, Checkov's `CKV_GHA_1`, and octoscan's
`unsecure-commands` rules.

## Fix

Remove the env line entirely:

```yaml
# DELETE THIS:
env:
  ACTIONS_ALLOW_UNSECURE_COMMANDS: 'true'
```

Then port any scripts that depended on `::set-env` to write to
`$GITHUB_ENV` instead, and any `::add-path::` to write to
`$GITHUB_PATH`. The file-based interface doesn't share the stdout-
parsing attack surface.

## References

- Project Zero bug 2070 — "GitHub Actions runner allows env-var injection":
  https://bugs.chromium.org/p/project-zero/issues/detail?id=2070
- GitHub docs — "Workflow commands for GitHub Actions" (security guidance):
  https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions
