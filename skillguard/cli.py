"""Command-line interface for SkillGuard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .scanner import calculate_score, scan_skill


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="skillguard",
        description="Check the structure and common risks of an AI agent skill.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    parser.add_argument("skill_dir", nargs="?", default=".", help="Path to a skill folder")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    skill_path = Path(args.skill_dir)
    findings = scan_skill(skill_path)
    score = calculate_score(findings)

    if args.json:
        print(json.dumps({
            "skill": skill_path.name,
            "score": score,
            "findings": [finding.to_dict() for finding in findings],
        }, indent=2))
    else:
        print(f"SkillGuard report: {skill_path}")
        print(f"Quality score: {score}/100")
        if not findings:
            print("No issues found by the current checks.")
        for finding in findings:
            location = f":{finding.line}" if finding.line else ""
            print(
                f"[{finding.severity.upper()}] {finding.code} "
                f"{finding.file}{location} — {finding.message}"
            )
        print("\nNote: heuristic checks only; this is not a security audit.")

    return 1 if any(f.severity == "error" for f in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
