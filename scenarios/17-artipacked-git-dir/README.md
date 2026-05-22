# Scenario 17: `upload-artifact` includes `.git/` (ArtiPACKED)

**OWASP CICD-SEC mapping:** CICD-SEC-6 (Insufficient Credential Hygiene),
CICD-SEC-9 (Improper Artifact Integrity Validation)

**Vulnerable workflow:** [`.github/workflows/scenario-17-artipacked-git-dir.yml`](../../.github/workflows/scenario-17-artipacked-git-dir.yml)

## The pattern

Two things combine into a leak:

1. `actions/checkout` defaults `persist-credentials: true`, writing
   `GITHUB_TOKEN` into `.git/config` as an `extraheader`. (Same root
   cause as [Scenario 12](../12-persist-credentials-leak/README.md).)
2. `actions/upload-artifact` with `path: .` happily uploads every file
   in the workspace, including `.git/config`.

Anyone with read access to the workflow run (which is *everyone* on
public repos) can download the artifact, extract `.git/config`, and pull
out the token. Palo Alto Unit 42 named this "ArtiPACKED" and documented
it across hundreds of public repos.

## How an attacker exploits it

```bash
gh run download <run-id> -n workspace
strings workspace/.git/config | grep AUTHORIZATION
# AUTHORIZATION: basic <base64(x-access-token:ghs_xxx)>
echo "<base64-value>" | base64 -d
# x-access-token:ghs_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

The token's scope is whatever the workflow's `permissions:` block
granted — `write-all` ([Scenario 04](../04-github-token-write-all/README.md))
means full repo takeover.

## Expected scanner coverage

| Scanner        | Detection |
|----------------|-----------|
| pipeline-check | `GHA-037` (persist-credentials default fires for the token-in-`.git/config` half) + `GHA-019` (`.git/config` leaked through the uploaded artifact) + `GHA-066` (the `path: .` workspace-wildcard upload half, shipped in v1.4.0) |
| zizmor         | `artipacked` (named after the original Unit 42 disclosure; catches both halves in one fire) |
| poutine        | `artifact_with_git_dir` |
| checkov        | partial |
| kics           | partial |

## Fix

Pick one (or all three):

- Set `persist-credentials: false` on checkout — the token never lands
  in `.git/config`.
- Set `upload-artifact`'s `path:` to a specific output directory, not `.`.
- Add `.git` to an explicit `exclude:` list on the artifact upload.

```yaml
- uses: actions/checkout@v4
  with:
    persist-credentials: false
- run: make build && mv dist /tmp/upload
- uses: actions/upload-artifact@v4
  with:
    name: workspace
    path: /tmp/upload
```

## References

- Palo Alto Unit 42 — "ArtiPACKED: Hacking Giants Through a Race
  Condition in GitHub Actions Artifacts":
  https://unit42.paloaltonetworks.com/artipacked-github-actions-vulnerability/
- zizmor — `artipacked` audit: https://docs.zizmor.sh/audits/#artipacked
