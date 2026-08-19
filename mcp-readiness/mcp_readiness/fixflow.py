from __future__ import annotations

import difflib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def _proposal(data: dict) -> str:
    lines = ["# Proposed MCP Readiness Remediation", "", "> Review-only proposal. This file is generated in a temporary candidate workspace; it never edits the source repository.", ""]
    for finding in data.get("findings", []):
        if finding["status"] == "OK":
            continue
        lines += [f"## {finding['dimension']}: {finding['title']}", "", f"- Status: {finding['status']}", f"- Evidence: {', '.join(finding['evidence']) or 'none detected'}", f"- Suggested change: {finding['remediation']}", ""]
    lines += ["## Human review checklist", "", "1. Inspect the proposed change and adapt it to the repository architecture.", "2. Add or update tests before applying any source change.", "3. Run the project’s normal test and security checks.", "4. Review the final diff and approve creation of a pull request."]
    return "\n".join(lines) + "\n"


def create_preview(data: dict, repo: Path, output: Path, test_command: str | None = None) -> dict:
    repo = repo.resolve(); output.mkdir(parents=True, exist_ok=True)
    before = repo / ".mcp-readiness-proposed-remediation.md"
    proposal = _proposal(data)
    with tempfile.TemporaryDirectory(prefix="mcp-readiness-") as temp:
        candidate = Path(temp) / repo.name
        shutil.copytree(repo, candidate, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "*.egg-info"))
        proposed = candidate / ".mcp-readiness-proposed-remediation.md"
        proposed.write_text(proposal, encoding="utf-8")
        diff = difflib.unified_diff([], proposal.splitlines(keepends=True), fromfile="/dev/null", tofile=str(before), lineterm="")
        (output / "fixes.patch").write_text("".join(diff), encoding="utf-8")
        test_result = {"status": "not_run", "command": test_command}
        if test_command:
            run = subprocess.run(test_command, cwd=candidate, shell=True, text=True, capture_output=True, timeout=120)
            test_result = {"status": "passed" if run.returncode == 0 else "failed", "command": test_command, "returncode": run.returncode, "stdout": run.stdout[-4000:], "stderr": run.stderr[-4000:]}
    (output / "fix-preview.md").write_text(proposal, encoding="utf-8")
    pr_body = "# MCP Readiness remediation PR\n\nThis PR was prepared from a human-reviewed readiness report.\n\n## Scope\n\n" + "\n".join(f"- {f['dimension']}: {f['title']} ({f['status']})" for f in data.get("findings", []) if f["status"] != "OK") + "\n\n## Required checks\n\n- [ ] Inspect `fixes.patch` and adapt source changes.\n- [ ] Run repository tests.\n- [ ] Confirm security and legal review where applicable.\n- [ ] Approve PR creation manually.\n"
    (output / "pr-body.md").write_text(pr_body, encoding="utf-8")
    manifest = {"mode": "preview-only", "source": str(repo), "output": str(output), "test": test_result, "pr_creation": "not_performed_without_explicit_human_approval"}
    (output / "fix-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
