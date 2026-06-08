# Scenario 133: PyPI — plain-HTTP primary index + TLS verification disabled

**Provider:** PyPI (`requirements.txt`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: high**

**Vulnerable manifest:** [`requirements.txt`](requirements.txt)

## The pattern

```
--index-url http://mirror.internal.example.com/simple
--trusted-host mirror.internal.example.com
```

`--index-url` repoints pip's **primary** index to a non-PyPI host over plain
HTTP — every dependency resolves from that mirror with no TLS. `--trusted-host`
then suppresses pip's own "insecure transport" warning, removing the last
guardrail.

## How an attacker exploits it

With packages fetched over HTTP and TLS verification off, anyone in a
network-MITM position (or whoever controls the mirror) serves arbitrary package
content, whose `setup.py` / build backend executes on the CI runner. The
`--trusted-host` line guarantees pip won't even warn.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `PYPI-003` — _HTTP index or disables TLS verification_ · `PYPI-011` — _disables TLS via `--trusted-host`_ |

## Fix

Use `https://` for every index, drop `--trusted-host`, and pin a CA you trust.
If you must run an internal mirror, terminate TLS on it with a real certificate
and enable `--require-hashes`.

## References

- pip — `--index-url` / `--trusted-host`: https://pip.pypa.io/en/stable/cli/pip_install/#cmdoption-i
- pip — Secure installs: https://pip.pypa.io/en/stable/topics/secure-installs/
