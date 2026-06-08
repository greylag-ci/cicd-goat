# Scenario 140: Cargo — alternate registry + `.cargo/config.toml` source override

**Provider:** Cargo (`Cargo.toml` + `.cargo/config.toml`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: high**

**Vulnerable manifest:** [`Cargo.toml`](Cargo.toml) · [`.cargo/config.toml`](.cargo/config.toml)

## The pattern

```toml
# Cargo.toml
acme-secrets = { version = "1.2", registry = "internal" }
```
```toml
# .cargo/config.toml
[source.crates-io]
replace-with = "internal"
[source.internal]
registry = "sparse+http://crates.internal.example.com/index/"
[build]
rustflags = ["-C", "link-arg=..."]
```

A dependency is sourced from an **alternate registry**, and `.cargo/config.toml`
**replaces the crates.io source** with that registry and injects build flags.
Cargo now resolves *every* dependency — even ones that look like crates.io — from
the attacker-influenceable index, over plain HTTP.

## How an attacker exploits it

The `source.crates-io` replacement silently redirects all crate lookups to the
internal index; whoever controls it serves arbitrary crate content (whose
`build.rs` runs at compile time). The injected `rustflags` apply to every build.
A developer reading only `Cargo.toml` wouldn't see the redirect — it's in
`.cargo/config.toml`.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `CARGO-005` — _dependency sourced from an alternate registry_ · `CARGO-012` — _`.cargo/config.toml` overrides the registry source or injects build flags_ |

## Fix

Resolve from crates.io (or a single, TLS-terminated, trusted mirror); avoid
`source.*.replace-with` redirects; review any `.cargo/config.toml` `rustflags`;
commit a `Cargo.lock` and gate with `cargo-deny` / `cargo-vet`.

## References

- Cargo — Source replacement: https://doc.rust-lang.org/cargo/reference/source-replacement.html
- Cargo — Registries / alternate registries: https://doc.rust-lang.org/cargo/reference/registries.html
