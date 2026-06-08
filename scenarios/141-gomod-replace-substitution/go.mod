// scenarios/141-gomod-replace-substitution
// CICD-SEC-3 (Dependency Chain Abuse) — Go modules / go.mod
//
// Pattern: a `replace` directive substitutes a DIFFERENT module path for an
// upstream one (orig != new), silently redirecting an import to attacker-chosen
// code, AND there is no sibling go.sum, so module integrity is never verified.
// A same-module version-pin replace would be an auditable override; a
// cross-module swap is a supply-chain substitution.
//
// SAFETY: static fixture nested under scenarios/. `go build` is never invoked on
// this tree; pipeline-check parses go.mod statically. See README.md.

module example.com/acme/service

go 1.22

require (
	github.com/sirupsen/logrus v1.9.3
	github.com/acme/auth v1.4.0
)

// DANGER — cross-module substitution: imports of github.com/acme/auth now
// resolve to a fork at a different module path the operator must vet.
replace github.com/acme/auth => github.com/acme-mirror/auth v1.4.0-patched
