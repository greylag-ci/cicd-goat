# Scenario 139: Cargo — git dependency on a mutable ref + compile-time `build.rs`

**Provider:** Cargo (`Cargo.toml` + `build.rs`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: high**

**Vulnerable manifest:** [`Cargo.toml`](Cargo.toml) · [`build.rs`](build.rs)

## The pattern

```toml
[dependencies]
telemetry = { git = "https://github.com/acme-internal/telemetry", branch = "main" }
```
```rust
// build.rs
ureq::get("https://setup.internal.example.com/bootstrap").call();           // network
Command::new("sh").arg("-c").arg("curl ... | sh").status();                 // process
```

A git dependency is pinned to a **mutable** ref (a branch, no `rev`), so the
resolved commit can change under you. And the crate ships a `build.rs` that makes
network / process calls at **compile** time — `cargo build` runs `build.rs`
before the application exists. The Rust analogue of an npm install script.

## How an attacker exploits it

Whoever can push to the `telemetry` branch (or who compromises the bootstrap URL)
runs code on the CI runner the next time the project builds — no release, no
version bump required, because the ref is mutable and `build.rs` runs
automatically.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `CARGO-002` — _git dependency uses a mutable ref (no `rev`)_ · `CARGO-011` — _`build.rs` runs network or process calls at compile time_ |

## Fix

Pin git dependencies to an exact `rev = "<commit-sha>"` (and prefer a
crates.io release), and remove network/process calls from `build.rs` — do code
generation from checked-in inputs, or move it to an explicit reviewed step.

## References

- Cargo — Specifying dependencies (git `rev`): https://doc.rust-lang.org/cargo/reference/specifying-dependencies.html#specifying-dependencies-from-git-repositories
- Cargo — Build scripts (`build.rs`): https://doc.rust-lang.org/cargo/reference/build-scripts.html
