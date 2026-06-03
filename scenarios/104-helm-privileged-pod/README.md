# Scenario 104: Helm — privileged container in a chart template

**Provider:** Helm · **OWASP:** CICD-SEC-7 (Insecure System Configuration) · **Severity: critical**

**Vulnerable files:** [`Chart.yaml`](Chart.yaml) · [`templates/deployment.yaml`](templates/deployment.yaml)

## The pattern

The chart's Deployment template ships a `privileged: true` container. Anyone who
installs the chart gets a privileged pod — node-level access wherever the
release lands. Same impact as scenario 97, but delivered as a packaged chart.
The `securityContext` block is **literal** in the template (only the pod name
and labels use `{{ .Release.Name }}` interpolation), so a scanner that parses
the template YAML as Kubernetes finds the bug without rendering the chart.

## How an attacker exploits it

A consumer `helm install`s the chart (often from a registry, transitively as a
dependency); the privileged pod escapes to the node. The chart is a supply-chain
vector: the bug travels with the package.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `K8S-005` — flags the literal `privileged: true` in the chart template (its `HELM-*` rules also fire on Chart.yaml metadata, but K8S-005 names this bug) |
| Checkov | `CKV_K8S_16` — its Kubernetes framework parses the template and flags the privileged container |
| KICS | — (Helm isn't in KICS's scored providers here, so the row is not-applicable) |

> Because the dangerous field is static (not behind `{{ }}`), the file-level
> Kubernetes parsers in pipeline-check and Checkov catch it directly — no
> `helm template` render required. A bug placed *inside* an interpolated value
> would be the genuine next-gen case; this one is shippable and statically
> visible.

## Fix

Don't ship `privileged: true` in chart defaults; render charts in CI
(`helm template | <k8s scanner>`) so pod-security checks also run against
fully-rendered output; gate installs behind a restricted Pod Security Standard
at admission.

## References

- Checkov — scanning Helm charts: https://www.checkov.io/7.Scan%20Examples/Helm.html
- Helm — Chart template guide: https://helm.sh/docs/chart_template_guide/
