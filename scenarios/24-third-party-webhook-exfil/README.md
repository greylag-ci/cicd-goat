# Scenario 24: Third-party webhook exfiltration

**OWASP CICD-SEC mapping:** CICD-SEC-8 (Ungoverned Usage of Third-Party Services)

**Vulnerable workflow:** [`.github/workflows/scenario-24-third-party-webhook-exfil.yml`](../../.github/workflows/scenario-24-third-party-webhook-exfil.yml)

## The pattern

CI workflows accumulate "lightweight integrations" — POST a build
status to Slack, fire a webhook to a tracker, ping a chatops bot. The
egress is small per call but the trust model is enormous: every one of
those endpoints is a place CI sends data, and CI runs with environment
variables, repo metadata, and (sometimes) secrets.

The failure modes:

- **Lapsed domain.** The third-party service domain expires; an
  attacker re-registers it; every downstream POST now lands on attacker
  infrastructure.
- **Third-party breach.** The service itself gets owned; historical
  telemetry leaks. (See the Sourcegraph 2023, Circle 2023, etc.
  incident timelines.)
- **Payload over-share.** Someone added `env | base64` to a
  "diagnostic" version of the payload years ago; nobody removed it.

## How an attacker exploits it

1. Find a workflow that POSTs to a public-DNS domain you can take over.
   `whois build-tracker.third-party.example` — registration expires in 14 days.
2. Wait, register, point the A record at your host.
3. Receive every downstream's env dump indefinitely. Until someone
   notices the build-tracker dashboard isn't being updated.

## Expected scanner coverage

| Scanner            | Detection                                                              |
| :----------------- | :--------------------------------------------------------------------- |
| **pipeline-check** | ✅ Flags external HTTP POST + env-in-payload heuristic                |
| zizmor             | ❌                                                                     |
| poutine            | ❌                                                                     |
| KICS               | ❌                                                                     |
| Checkov            | ❌                                                                     |

> Until pipeline-check shipped the CICD-SEC-8 rule chain, this whole
> category was uncovered. The community tools all focus on the
> *workflow* layer — what runs where — and don't reason about the
> *network egress* surface, which is the natural home of CICD-SEC-8.

## Fix

Three controls, layered:

1. **Egress allowlist.** GitHub-hosted runners don't have a built-in
   one, but for self-hosted runners you can enforce one. For
   GitHub-hosted, pin your webhook URLs to ones you control (your own
   relay), not to third-party domains directly.
2. **Minimal payload.** Send the bare metadata the receiver needs
   (`sha`, `status`, `url`) and nothing else. Never `env`. Never
   `secrets`. Never logs.
3. **Bounded blast radius.** Use a dedicated low-scope token for the
   POST step, not the workflow's main `GITHUB_TOKEN`. Mark third-party
   integrations as "ungoverned" in your SDLC docs so the next person
   to add one thinks twice.

```yaml
- name: Notify external tracker (minimal payload)
  run: |
    jq -nc --arg repo "$GITHUB_REPOSITORY" \
           --arg sha  "$GITHUB_SHA" \
           --arg url  "${{ github.event.head_commit.url }}" \
           '{repo:$repo, sha:$sha, url:$url}' \
      | curl -fsS -X POST --data @- \
          -H "Content-Type: application/json" \
          "https://relay.your-domain.example/build-events"
```

## References

- OWASP CICD-SEC-8:
  https://owasp.org/www-project-top-10-ci-cd-security-risks/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services
- StepSecurity — "Egress firewall for GitHub Actions":
  https://www.stepsecurity.io/blog/introducing-stepsecurity-harden-runner
