# mcp-readiness

Read-only static analyzer for MCP production readiness against the 2026-07-28 checklist. It scans a **local repository only**, reports evidence and heuristic findings, and never writes to the target repository or customer infrastructure.

> This is not a certified security audit, compliance certification, or legal advice. Findings require human validation.

## Install and usage

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
mcp-readiness --demo --output demo-report
mcp-readiness /path/to/authorized/repository --i-have-authorization --output report
```

The authorization flag is required for every non-demo target and represents the operator’s confirmation that written owner consent exists. `--apply` is always rejected. Outputs include `report.md`, `report.json`, `badge.svg` and `guided-fixes.md`.

Use `--fail-under 55` in CI to block a release below the chosen threshold. The workflow template at `../.github/mcp-readiness.yml.example` runs tests, produces the score and uploads the artifacts.

## Fix workflow

The CLI supports a safe review workflow:

```bash
mcp-readiness --demo --output demo-report --preview-fixes --test-command "python -m pytest -q"
```

This produces `fixes.patch`, `fix-preview.md`, `pr-body.md` and `fix-manifest.json`. Tests run on a temporary copy. The source repository is never edited. `--create-pr` is intentionally rejected; a human must inspect the diff, adapt the remediation, run the repository checks and create or approve the pull request through the normal Git workflow.

The analyzer detects transport signals, OAuth/EMA and registration patterns, tools/resources, potentially sensitive capabilities, logging and SDK references. It does not contact remote hosts, validate an IdP, resolve every framework abstraction or prove runtime behavior.

## Tests

```bash
python -m pytest -q
```
