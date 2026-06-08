# Scenario 143: Composer — `scripts` hook pipes a remote download to a shell

**Provider:** Composer (`composer.json`) · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · **Severity: high**

**Vulnerable manifest:** [`composer.json`](composer.json)

## The pattern

```json
"config": { "allow-plugins": true },
"scripts": { "post-install-cmd": ["curl -fsSL https://setup.internal.example.com/bootstrap.sh | sh"] }
```

A `scripts` hook (`post-install-cmd`, `post-update-cmd`, …) pipes a remote
download straight into a shell, and `config.allow-plugins` is `true` so **any**
installed plugin may execute code during install. Composer runs scripts hooks
automatically on `composer install` / `update`, so this is RCE on every CI run.

## How an attacker exploits it

The `curl | sh` runs whatever the URL serves with the build's credentials — a
network-MITM or a compromised host owns the runner. Separately, `allow-plugins:
true` removes Composer's plugin-execution allowlist, so any dependency that ships
a Composer plugin also runs code at install time.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `COMPOSER-006` — _`scripts` hook pipes a remote download to a shell_ · `COMPOSER-008` — _`allow-plugins` permits any plugin to execute_ |

## Fix

Don't `curl | sh` in `scripts`; run a checked-in, reviewed script (and verify
downloads with `sha256sum -c` on the same line). Replace `allow-plugins: true`
with an explicit per-plugin allowlist (`{"vendor/plugin": true}`).

## References

- Composer — Scripts: https://getcomposer.org/doc/articles/scripts.md
- Composer — `allow-plugins`: https://getcomposer.org/doc/06-config.md#allow-plugins
