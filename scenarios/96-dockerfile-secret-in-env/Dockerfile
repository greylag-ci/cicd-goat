# scenarios/96-dockerfile-secret-in-env
# CICD-SEC-6 (Insufficient Credential Hygiene) — Dockerfile
#
# Pattern: a credential is baked into an image layer via `ENV` (or `ARG`). It is
# readable by anyone who can pull the image and run `docker history` / inspect
# the layers — and it ships everywhere the image ships. (The token below is a
# fake hex fixture, not a real provider format.)
#
# SAFETY: static fixture nested under scenarios/; never built. Base image
# digest-pinned + USER set so the ONLY intended bug is the embedded secret.
# See README.md.

FROM node@sha256:1d3f5a7c9e2b4d6f8a0c2e4b6d8f0a1c3e5b7d9f1a3c5e7b9d0f2a4c6e8b0d2f
USER node
WORKDIR /app
COPY . .
# DANGER — credential baked into the image. Use a build secret / runtime env /
# secrets manager instead, never `ENV`/`ARG` for secrets.
ENV API_TOKEN=deadbeefcafef00dfeedfacebadc0ffee0ddf00d
CMD ["node", "server.js"]
