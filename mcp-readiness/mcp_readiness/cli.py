from __future__ import annotations

import argparse
import sys
from pathlib import Path
from .analyzer import analyze, write_reports
from .fixflow import create_preview

DISCLAIMER = "This is not a certified security audit or legal advice. Findings are heuristic checklist alignment signals."

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="mcp-readiness", description="Read-only MCP production-readiness analyzer")
    p.add_argument("path", nargs="?", help="Local repository path")
    p.add_argument("--output", default="mcp-readiness-report")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--i-have-authorization", action="store_true", help="Confirm written owner consent")
    p.add_argument("--apply", action="store_true", help="Reserved and always rejected")
    p.add_argument("--fail-under", type=int, default=None, help="Exit 1 when score is below this threshold")
    p.add_argument("--preview-fixes", action="store_true", help="Generate a review-only diff and PR body")
    p.add_argument("--test-command", default=None, help="Run a test command on a temporary candidate copy")
    p.add_argument("--create-pr", action="store_true", help="Always rejected; PR creation requires a separate human-approved workflow")
    args = p.parse_args(argv)
    if args.apply:
        print("Refusing --apply: this release is read-only and never modifies customer infrastructure.", file=sys.stderr); return 2
    if args.create_pr:
        print("Refusing automatic PR creation: inspect the preview, approve the diff and create the PR through the repository workflow.", file=sys.stderr); return 2
    if args.demo: target = Path(__file__).parent.parent / "examples" / "clean-server"
    elif args.path: target = Path(args.path).expanduser()
    else: p.error("provide a local path or use --demo")
    if not target.is_dir(): print(f"Target is not a local directory: {target}", file=sys.stderr); return 2
    if not args.demo and not args.i_have_authorization:
        print("Refusing to scan: provide --i-have-authorization after obtaining written owner consent.", file=sys.stderr); return 2
    data = analyze(target); output = Path(args.output); write_reports(data, output)
    if args.preview_fixes or args.test_command:
        manifest = create_preview(data, target, output, args.test_command)
        print(f"Fix preview: {manifest['output']} ({manifest['test']['status']})")
    score = data["score"]
    print(f"Analyzed: {target}\nScore: {score['score']}/100\nGate: {score['gate']}\nReports: {output.resolve()}\n{DISCLAIMER}")
    if args.fail_under is not None and score["score"] < args.fail_under: return 1
    return 0

if __name__ == "__main__": raise SystemExit(main())
