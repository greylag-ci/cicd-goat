# scenarios/94-dockerfile-root-user
# CICD-SEC-7 (Insecure System Configuration) — Dockerfile
#
# Pattern: the image declares no USER, so every process (and anything an
# attacker runs via an app/RCE bug) runs as root inside the container — and
# root-in-container is one `--privileged`/kernel-bug step from the host. The
# image this pipeline builds and ships is the artifact at risk.
#
# SAFETY: static fixture nested under scenarios/; never built. Base image is
# digest-pinned so the ONLY intended bug is the missing USER. See README.md.

FROM node@sha256:1d3f5a7c9e2b4d6f8a0c2e4b6d8f0a1c3e5b7d9f1a3c5e7b9d0f2a4c6e8b0d2f
WORKDIR /app
COPY . .
RUN npm ci --omit=dev
# DANGER — no `USER` directive; the container runs as root. Add e.g. `USER node`.
CMD ["node", "server.js"]
