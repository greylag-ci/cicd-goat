# Scenario 134: PyPI — floating `build-system.requires` + plain-HTTP source

**Provider:** PyPI (`pyproject.toml`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: medium**

**Vulnerable manifest:** [`pyproject.toml`](pyproject.toml)

## The pattern

```toml
[build-system]
requires = ["setuptools>=61", "wheel", "cython"]   # unpinned; run at build time

[[tool.pdm.source]]
url = "http://pkgs.internal.example.com/simple"     # plain HTTP
verify_ssl = false
```

`[build-system].requires` lists the packages pip installs **and imports** to
build the project (the PEP 517 backend) — they execute code at build time.
Floating versions there mean a yanked-and-republished or newly-compromised build
dependency runs in CI on the next build. A custom package source over plain HTTP
compounds the exposure.

## How an attacker exploits it

A compromised release of any unpinned build requirement (e.g. `cython`) executes
during `pip install` / `python -m build`, before the project's own code runs.
The HTTP source means even the resolution step is MITM-able.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `PYPI-012` — _`[build-system].requires` uses floating versions_ · `PYPI-014` — _custom package source uses plain HTTP_ |

## Fix

Pin every `build-system.requires` entry to an exact version (or a hash-locked
constraints file), and use `https://` for any custom source with TLS
verification on.

## References

- PEP 517 — build-system requirements: https://peps.python.org/pep-0517/
- Python Packaging — `pyproject.toml` build system: https://packaging.python.org/en/latest/specifications/pyproject-toml/
