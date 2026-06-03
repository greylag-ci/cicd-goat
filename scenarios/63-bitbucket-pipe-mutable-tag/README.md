# Scenario 63: Bitbucket — `pipe:` pinned to a mutable tag

**Provider:** Bitbucket Pipelines · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable pipeline:** [`bitbucket-pipelines.yml`](bitbucket-pipelines.yml)

## The pattern

```yaml
- pipe: atlassian/aws-s3-deploy:latest
  variables: { ... }
```

A Bitbucket Pipe is a Docker container that runs with your pipeline's
variables/secrets passed in as inputs. Pinning it to a mutable tag (`:latest`)
means an upstream tag overwrite changes the code that receives your secrets.

## How an attacker exploits it

A mutable tag overwritten upstream (or a non-vetted third-party pipe) executes
attacker code with your secured variables in scope — analogue of the
mutable-action-ref / third-party-exfil class (scenarios 03 / 24).

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `BB-001` — `pipe:` action not pinned to exact version |
| Checkov | — |

## Fix

Pin pipes by digest (`pipe: ...@sha256:...`) or at minimum an exact immutable
version; prefer Atlassian-authored pipes; review third-party pipe source.

## References

- Atlassian — Use pipes in Bitbucket Pipelines: https://support.atlassian.com/bitbucket-cloud/docs/use-pipes-in-bitbucket-pipelines/
