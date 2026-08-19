from __future__ import annotations

import argparse
import sys
from pathlib import Path
from .analyzer import analyze, write_reports

DISCLAIMER = "This is not a certified security audit or legal advice. Findings are heuristic checklist alignment signals."

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="mcp-readiness", description="Read-only MCP release-readiness analyzer")
    p.add_argument("path", nargs="?", help="Local repository path")
    p.add_argument("--output", default="mcp-readiness-report")
    p.add_argument("--demo", action="store_true")
    p.add_argument("--i-have-authorization", action="store_true", help="Confirm written owner consent")
    p.add_argument("--apply", action="store_true", help="Reserved and always rejected")
    args = p.parse_args(argv)
    if args.apply:
        print("Refusing --apply: this release is read-only and never modifies customer infrastructure.", file=sys.stderr); return 2
    if args.demo: target = Path(__file__).parent.parent / "examples" / "clean-server"
    elif args.path: target = Path(args.path).expanduser()
    else: p.error("provide a local path or use --demo")
    if not target.is_dir(): print(f"Target is not a local directory: {target}", file=sys.stderr); return 2
    if not args.demo and not args.i_have_authorization:
        print("Refusing to scan: provide --i-have-authorization after obtaining written owner consent.", file=sys.stderr); return 2
    data = analyze(target); write_reports(data, Path(args.output))
    print(f"Analyzed: {target}\nReports: {Path(args.output).resolve() / 'report.md'} and report.json\n{DISCLAIMER}")
    return 0

if __name__ == "__main__": raise SystemExit(main())
