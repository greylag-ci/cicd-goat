# Scenario 106: GitLab — `include: remote:` unpinned 3rd-party template

**Provider:** GitLab CI · **OWASP:** CICD-SEC-8 (Ungoverned Usage of 3rd Party Services) · CICD-SEC-3 · **Severity: high**

**Vulnerable file:** [`.gitlab-ci.yml`](.gitlab-ci.yml)

## The pattern

```yaml
include:
  - remote: 'https://templates.example.com/ci/build.yml'
```

The pipeline pulls its job definitions from a third-party URL with no pinned
ref. There's no integrity control on what that external host returns — it
defines what runs in your pipeline, with your CI credentials, on every run.

## How an attacker exploits it

Whoever controls the remote host (or poisons DNS / the CDN, or compromises the
template repo) injects jobs that run with the project's `CI_JOB_TOKEN` and any
variables in scope — exfiltrating secrets or tampering with artifacts. The org
has delegated pipeline definition to a service it doesn't govern or version.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GL-005` — `include:` pulls remote/project config without a pinned ref |
| ciguard | `PIPE-002` — UnsafeRemoteInclude |
| Checkov | — (GitLab ruleset has no remote-include check) |

## Fix

Pin includes to an immutable ref — a commit SHA or signed tag
(`include: { project: 'group/templates', ref: 'v1.2.3', file: '/build.yml' }`),
never a bare `remote:` URL or a branch ref. Vendor critical templates in-repo
and review updates through MR.

## References

- GitLab — `include` keyword & ref pinning: https://docs.gitlab.com/ee/ci/yaml/#include
