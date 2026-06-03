# Scenario 96: Dockerfile — hardcoded secret in `ENV`

**Provider:** Dockerfile · **OWASP:** CICD-SEC-6 (Insufficient Credential Hygiene)

**Vulnerable file:** [`Dockerfile`](Dockerfile)

## The pattern

```dockerfile
ENV API_TOKEN=deadbeefcafef00dfeedfacebadc0ffee0ddf00d
```

The credential is baked into an image layer. Anyone who can pull the image reads
it via `docker history` / layer inspection, and it ships everywhere the image
goes. (The token is a fake hex fixture.)

## How an attacker exploits it

Pull the published image, run `docker history --no-trunc` (or extract the layer
tar), and recover the token. `ARG` is no better — it's recorded in history too.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `DF-006` — ENV/ARG carries a credential-shaped literal |
| Checkov | — (its dockerfile framework has no secret-in-ENV check) |
| KICS | — (fires only `Healthcheck Instruction Missing` noise; no secret-in-ENV Dockerfile query in this version) |

> Solo catch — only pipeline-check (`DF-006`) names the baked-in credential.
> Checkov and KICS both parse the Dockerfile but neither carries a
> secret-in-`ENV` query, so this is an all-but-one miss.

## Fix

Never put secrets in `ENV`/`ARG`. Use BuildKit build secrets
(`RUN --mount=type=secret`), inject at runtime via the orchestrator's secret
store, or pull from a secrets manager.

## References

- Docker — Build secrets: https://docs.docker.com/build/building/secrets/
