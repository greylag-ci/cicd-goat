// scenarios/142-gomod-insecure-host
// CICD-SEC-3 (Dependency Chain Abuse) — Go modules / go.mod
//
// Pattern: a module coordinate uses a non-canonical host — a bare IPv4 literal,
// or an explicit host:port. Canonical Go module paths resolve a real hostname
// (no scheme, no port); a bare IP pins the fetch to one box with no DNS/TLS-name
// binding (spoofable on a shared network) and a custom port usually means a
// self-hosted proxy outside the public module-proxy + checksum-database
// guarantees. The Go analogue of the PyPI insecure-host rules.
//
// SAFETY: static fixture nested under scenarios/. `go build` is never invoked on
// this tree; pipeline-check parses go.mod statically. See README.md.

module example.com/acme/app

go 1.22

require (
	// DANGER (1) — bare-IP host: no DNS / TLS-name binding, trivially spoofable.
	10.0.0.42/team/util v1.0.0
	github.com/sirupsen/logrus v1.9.3
)

// DANGER (2) — replace target on a custom host:port (self-hosted proxy smell).
replace example.com/x => git.internal.example.com:8443/mirror/x v1.0.0
