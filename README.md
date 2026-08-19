# MCP Production Readiness

**MCP Production Readiness** is the GitHub Actions / Snyk-style validation layer for MCP servers: repository scan, weighted score, release gate, badge, guided fixes and a foundation for history and monitoring.

## Product flow

```text
GitHub repository → MCP Readiness Score → findings → guided fixes → CI gate → badge → monitoring
```

The current V1 is deliberately safe and local-first. It scans code in read-only mode, requires explicit owner authorization outside the demo, generates `report.md`, `report.json`, `badge.svg` and `guided-fixes.md`, and never applies changes or opens pull requests automatically. Guided fixes are review-ready suggestions; a human must inspect, test and approve any future PR.

## Quick start

```bash
cd mcp-readiness
python -m pip install -e .
mcp-readiness --demo --output demo-report
```

Use `--fail-under 55` in CI to block a release below the chosen threshold. The included workflow at `.github/workflows/mcp-readiness.yml` runs tests, produces the score and uploads the artifacts.

> The score is a heuristic alignment signal, not a security certification, certified audit, legal advice, or guarantee of compliance.

## Repository map

| Path | Purpose |
|---|---|
| [`mcp-readiness/`](mcp-readiness/) | Python analyzer, score model, examples, tests and report artifacts |
| [`.github/mcp-readiness.yml.example`](.github/mcp-readiness.yml.example) | Workflow CI à placer dans `.github/workflows/` avec la permission GitHub workflows |
| [`business/`](business/) | Offer, landing page, outreach, demo and legal review notes |
| [`RESEARCH_NOTES.md`](RESEARCH_NOTES.md) | MCP/EMA research basis |
| [`NEXT_STEPS.md`](NEXT_STEPS.md) | Product validation and commercial next steps |

## Product validation thesis

The commercial hypothesis is not “a scanner that produces a report.” It is a repeatable **pre-publication validation standard** for MCP servers. The next validation step is to interview and pilot with 10–20 people or companies that actively build MCP servers, testing willingness to pay for a bounded readiness review before expanding into hosted history, GitHub integration, monitoring, organization rules, SSO and private deployment.
