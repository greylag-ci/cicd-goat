# Scenario 141: Go modules — `replace` module substitution + missing `go.sum`

**Provider:** Go modules (`go.mod`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: high**

**Vulnerable manifest:** [`go.mod`](go.mod)

## The pattern

```go
require github.com/acme/auth v1.4.0
replace github.com/acme/auth => github.com/acme-mirror/auth v1.4.0-patched
```

A `replace` directive substitutes a **different** module path for an upstream one
(`orig != new`), silently redirecting every import of `github.com/acme/auth` to
attacker-choosable code at `github.com/acme-mirror/auth`. And there is no sibling
`go.sum`, so module integrity is never verified. A *same-module* version-pin
replace would be an auditable override; a cross-module swap is a supply-chain
substitution.

## How an attacker exploits it

Whoever controls `github.com/acme-mirror/auth` controls what the build compiles
in place of the real `acme/auth` — and with no `go.sum`, `go mod verify` can't
catch a swap. The redirect is one line that's easy to miss in review.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GOMOD-003` — _`replace` substitutes a different module_ · `GOMOD-001` — _`go.mod` present without sibling `go.sum`_ |

## Fix

Remove cross-module `replace` directives (fold patches upstream, or vendor a
fork you maintain with a documented rotation policy), and always commit `go.sum`
so the checksum database verifies every module.

## References

- Go — `replace` directive: https://go.dev/ref/mod#go-mod-file-replace
- Go — Module authentication (`go.sum`, checksum DB): https://go.dev/ref/mod#authenticating
