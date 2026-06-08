# Scenario 142: Go modules — non-canonical host (bare IP / `host:port`) coordinate

**Provider:** Go modules (`go.mod`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: high**

**Vulnerable manifest:** [`go.mod`](go.mod)

## The pattern

```go
require 10.0.0.42/team/util v1.0.0
replace example.com/x => git.internal.example.com:8443/mirror/x v1.0.0
```

A module coordinate uses a **non-canonical host** — a bare IPv4 literal, or an
explicit `host:port`. Canonical Go module paths resolve a real hostname (no
scheme, no port). A bare IP pins the fetch to one box with no DNS / TLS-name
binding (trivially spoofable on a shared network), and a custom port usually
means a self-hosted proxy that sits outside the public module-proxy + checksum
database guarantees. The Go analogue of the PyPI insecure-host rules.

## How an attacker exploits it

A peer on the runner's network answers for `10.0.0.42` and serves a backdoored
module. With no TLS name binding and no canonical proxy, the checksum database
never sees the real bytes, so `go mod verify` can't catch the swap.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GOMOD-012` — _require / replace targets an insecure or non-canonical host_ |

> The cross-module `replace` here also trips `GOMOD-003`, and the absent `go.sum`
> trips `GOMOD-001`; the non-canonical host (`GOMOD-012`) is the canonical bug.

## Fix

Point every module coordinate at a canonical hostname. If a dependency lives on
an internal host, front it with a TLS-terminating canonical name (not a raw IP /
port), and keep `GOINSECURE` scoped narrowly rather than disabling sum
verification.

## References

- Go — Module paths: https://go.dev/ref/mod#module-path
- Go — `GOINSECURE` / module proxy: https://go.dev/ref/mod#environment-variables
