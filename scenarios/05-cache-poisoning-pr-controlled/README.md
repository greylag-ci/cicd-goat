# Scenario 05: Cache poisoning via attacker-controlled key

**OWASP CICD-SEC mapping:** CICD-SEC-4 (Poisoned Pipeline Execution),
CICD-SEC-9 (Improper Artifact Integrity Validation)

**Vulnerable workflow:** [`.github/workflows/scenario-05-cache-poisoning-pr-controlled.yml`](../../.github/workflows/scenario-05-cache-poisoning-pr-controlled.yml)

## The pattern

`actions/cache` keys are namespaced by repository, but **not** by branch or
trigger. A cache saved by a PR build can be restored by a main-branch build
later, as long as the *key* matches. If any part of the key derives from
attacker-controllable PR metadata (`pull_request.title`, `head_ref`,
`pull_request.body`), the attacker can:

1. Open a PR that builds and saves a cache under a key colliding with the
   main branch's key.
2. Wait for the next main-branch run to restore that cache.
3. The poisoned `node_modules` / `~/.cache/pip` runs on main with whatever
   privileges main has.

## How an attacker exploits it

Given the vulnerable key `deps-${{ runner.os }}-${{ github.event.pull_request.title }}`:

1. Predict the next main-branch cache key value (e.g. when main next runs
   without a PR, the title context is empty → key becomes `deps-Linux-`).
2. Open a fork PR whose title evaluates the cache key to the same string.
3. The PR build saves a malicious `node_modules` (e.g. with a tampered
   `node_modules/.bin/jest` that exfiltrates secrets on invocation).
4. Next main run restores that cache, runs `jest`, secrets exfiltrate.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `cache-poisoning` |
| poutine   | `cache_poisoning` |
| checkov   | partial (cache + untrusted input rule may flag) |
| kics      | limited |

## Fix

- Never include attacker-controllable input in a cache key.
- Use `github.sha` or hashes of lockfiles (`hashFiles('**/package-lock.json')`).
- Consider not restoring caches at all on `pull_request` from forks.
- Scope `restore-keys:` carefully — a too-broad prefix re-introduces the
  same risk.

```yaml
- uses: actions/cache@v4
  with:
    path: |
      node_modules
      ~/.npm
    key: deps-${{ runner.os }}-${{ hashFiles('**/package-lock.json') }}
```

## References

- GitHub docs — "Caching dependencies to speed up workflows":
  https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows
- Adnan Khan — "GitHub Actions Cache Poisoning":
  https://adnanthekhan.com/2024/05/06/the-monsters-in-your-build-cache/
