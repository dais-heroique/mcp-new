# mcp-readiness

Read-only static analyzer for MCP release readiness against the 2026-07-28 checklist. It scans a **local repository only**, reports evidence and heuristic findings, and never writes to the target repository or customer infrastructure.

> This is not a certified security audit, compliance certification, or legal advice. Findings require human validation.

## Install and usage

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -e .
mcp-readiness --demo --output demo-report
mcp-readiness /path/to/authorized/repository --i-have-authorization --output report
```

The authorization flag is required for every non-demo target and represents the operator’s confirmation that written owner consent exists. `--apply` is always rejected. Outputs are `report.md` and `report.json`.

The analyzer detects transport signals, OAuth/EMA and registration patterns, tools/resources, potentially sensitive capabilities, logging and SDK references. It does not execute customer code, contact remote hosts, validate an IdP, resolve every framework abstraction or prove runtime behavior.

## Tests

```bash
python -m pytest -q
```
