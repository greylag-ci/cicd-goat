# scenarios/95-dockerfile-unpinned-base
# CICD-SEC-3 (Dependency Chain Abuse) · CICD-SEC-9 (Improper Artifact Integrity)
#
# Pattern: the base image is pinned to a MUTABLE tag (`node:latest`) rather than
# a digest. Every rebuild pulls whatever that tag currently resolves to, so
# whoever moves the tag (upstream, or an attacker who compromises the registry
# namespace) gets their layers into your image. The Dockerfile equivalent of
# the mutable-image scenarios (09 / 46 / 58 / 64 / 73 / 78).
#
# SAFETY: static fixture nested under scenarios/; never built. USER set so the
# ONLY intended bug is the unpinned base image. See README.md.

# DANGER — mutable tag. The fix is a digest pin: node@sha256:<...>.
FROM node:latest
USER node
WORKDIR /app
COPY . .
CMD ["node", "server.js"]
