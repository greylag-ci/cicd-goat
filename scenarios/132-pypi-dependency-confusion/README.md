# Scenario 132: PyPI — dependency confusion via `--extra-index-url`

**Provider:** PyPI (`requirements.txt`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: high**

**Vulnerable manifest:** [`requirements.txt`](requirements.txt)

## The pattern

```
--extra-index-url https://pypi.internal.example.com/simple
internal-billing>=1.0
acme-auth-helpers>=2.3
```

`--extra-index-url` adds a *second* index alongside public PyPI. pip queries
**all** configured indexes and installs the highest version found on *any* of
them. There's no hashing (`--hash` / `--require-hashes`), so whatever pip
resolves is installed unverified.

## How an attacker exploits it

This is Birsan dependency confusion (2021): an attacker publishes
`internal-billing 99.0.0` to **public** PyPI. Because public PyPI now offers a
higher version than the private index, pip installs the attacker's package — and
its `setup.py` / build backend runs on the CI runner. The private package name
leaked (in this file) is all the attacker needs.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `PYPI-005` — _declares `--extra-index-url` (dependency-confusion surface)_ · `PYPI-002` — _missing hash pinning_ |

> pipeline-check is the only scanner in this comparison that parses Python
> dependency manifests — this whole family is pipeline-check-solo.

## Fix

Use a single index you control that proxies/pins PyPI (`--index-url`, not
`--extra-index-url`), enable `--require-hashes` with pinned `--hash` lines, and
claim your internal package names on public PyPI to block the shadow.

## References

- Alex Birsan — Dependency Confusion (2021): https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610
- pip — Secure installs / hash-checking mode: https://pip.pypa.io/en/stable/topics/secure-installs/
