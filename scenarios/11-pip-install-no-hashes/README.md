# Scenario 11: `pip install` of unpinned, unhashed deps

**OWASP CICD-SEC mapping:** CICD-SEC-3 (Dependency Chain Abuse)

**Vulnerable workflow:** [`.github/workflows/scenario-11-pip-install-no-hashes.yml`](../../.github/workflows/scenario-11-pip-install-no-hashes.yml)

**Requirements file:** [`requirements.txt`](requirements.txt)

## The pattern

`pip install -r requirements.txt` resolves dependencies at install time.
Without:

- Version pins (`requests==2.31.0`, not `requests>=2.0`),
- Transitive pinning (a lock file like `requirements.lock` from `pip-compile`),
- `--require-hashes` to bind each install to a known artifact hash,

the CI runner happily pulls whatever PyPI currently serves under each
package name. Any compromise of PyPI, account takeover of a maintainer, or
typosquat (`reqeusts`, `python-requests` vs `requests`) lands directly on
the runner with the workflow's privileges.

## How an attacker exploits it

- **Typosquat:** publish `python-requestz` and wait for someone to add it.
- **Maintainer compromise:** push a malicious patch release of an existing
  unpinned dep; every downstream `pip install` on next CI run executes it.
- **Dependency confusion:** if the package isn't on PyPI yet and the org's
  internal mirror is misconfigured, register the name on PyPI first.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | ❌ miss — parses the workflow but has no pip-hash rule |
| poutine   | partial |
| checkov   | "Ensure pip install uses --require-hashes" |
| kics      | "Pip install without hash verification" |
| (bonus)   | OSV-Scanner, Snyk, Dependabot — outside this comparison |

## Fix

Generate a hashed lock file (`pip-compile --generate-hashes`) and install
with `--require-hashes`:

```yaml
- run: pip install --require-hashes -r requirements.lock
```

## References

- pip docs — "Hash-checking mode":
  https://pip.pypa.io/en/stable/topics/secure-installs/
- PyPA — "pip-tools": https://github.com/jazzband/pip-tools
