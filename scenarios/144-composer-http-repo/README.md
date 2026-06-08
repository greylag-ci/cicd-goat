# Scenario 144: Composer — plain-HTTP repository + `secure-http: false`

**Provider:** Composer (`composer.json`) · **OWASP:** CICD-SEC-3 (Dependency Chain Abuse) · **Severity: high**

**Vulnerable manifest:** [`composer.json`](composer.json)

## The pattern

```json
"repositories": [{ "type": "composer", "url": "http://packages.internal.example.com" }],
"config": { "secure-http": false }
```

A custom repository is declared over plain **HTTP**, and `config.secure-http` is
`false` — which disables Composer's HTTPS enforcement globally and silences the
protection that would otherwise refuse the HTTP repo.

## How an attacker exploits it

With `secure-http` off and packages fetched over HTTP, a network-MITM (or
whoever controls the repo) serves arbitrary package archives, whose install-time
scripts run on the CI runner. `secure-http: false` is the explicit override that
turns Composer's default refusal into silent acceptance.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `COMPOSER-003` — _repository declared over plain HTTP_ · `COMPOSER-010` — _`config.secure-http: false` disables HTTPS enforcement_ |

## Fix

Use `https://` for every repository and remove `secure-http: false` (leave
Composer's default HTTPS enforcement on). If you must run an internal repo,
terminate TLS with a real certificate.

## References

- Composer — Repositories: https://getcomposer.org/doc/05-repositories.md
- Composer — `secure-http` config: https://getcomposer.org/doc/06-config.md#secure-http
