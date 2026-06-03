# Scenario 93: Drone — privileged step mounts the host Docker socket

**Provider:** Drone CI · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: critical**

**Vulnerable pipeline:** [`.drone.yml`](.drone.yml)

## The pattern

```yaml
steps:
  - privileged: true
    volumes: [{ name: dockersock, path: /var/run/docker.sock }]
volumes:
  - name: dockersock
    host: { path: /var/run/docker.sock }
```

The step is privileged **and** the node's Docker daemon socket is mounted in.
The host-escape escalation of [scenario 77](../77-drone-privileged-step/README.md).

## How an attacker exploits it

With the host daemon in reach, the step runs
`docker run -v /:/host … chroot /host` — a root shell on the node. It reads
other repos' secrets, the runner's config, and takes over the host. (Drone
honours `privileged` + host volumes only for **trusted** repos, so a trusted
repo — or an attacker who gets one trusted — is the enabling condition.)

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `DR-007` — step mounts a sensitive host path (also `DR-002` privileged) |

> Drone is scored by pipeline-check only in this comparison.

## Fix

Never mount `/var/run/docker.sock` (or other host paths) into a step; never run
privileged. Use a rootless image builder, or a dedicated, isolated/ephemeral
runner; don't mark repos trusted unless absolutely required.

## References

- Drone — Docker pipeline volumes / privileged: https://docs.drone.io/pipeline/docker/syntax/volumes/host/
