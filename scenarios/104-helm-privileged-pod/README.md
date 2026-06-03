# Scenario 104: Helm — privileged container in a chart template

**Provider:** Helm · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: critical**

**Vulnerable files:** [`Chart.yaml`](Chart.yaml) · [`templates/deployment.yaml`](templates/deployment.yaml)

## The pattern

The chart's Deployment template ships a `privileged: true` container. Anyone who
installs the chart gets a privileged pod — node-level access wherever the
release lands. Same impact as scenario 97, but delivered as a packaged chart.

## How an attacker exploits it

A consumer `helm install`s the chart (often from a registry, transitively as a
dependency); the privileged pod escapes to the node. The chart is a supply-chain
vector: the bug travels with the package.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | — (its `HELM-*` rules check Chart.yaml *metadata*, not rendered template security) |
| Checkov | — (its Helm framework needs the `helm` binary to render the chart; absent here) |
| KICS | — (no Helm rendering) |

> **All-miss — a next-gen target.** The privileged container is inside a Helm
> *template* (with `{{ }}` interpolation), invisible to scanners that don't
> `helm template` the chart first. It's a real, shippable bug that the file-level
> scanners here don't render-and-inspect.

## Fix

Render charts in CI (`helm template | <k8s scanner>`) so pod-security checks run
against the output; don't ship `privileged: true` in chart defaults; gate
installs behind a restricted Pod Security Standard at admission.

## References

- Checkov — scanning Helm charts: https://www.checkov.io/7.Scan%20Examples/Helm.html
- Helm — Chart template guide: https://helm.sh/docs/chart_template_guide/
