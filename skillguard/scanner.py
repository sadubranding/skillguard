"""Static, heuristic checks for AI agent skill folders."""

from __future__ import annotations

import re
from pathlib import Path

from .models import Finding

REQUIRED_FRONTMATTER = ("name", "description")
NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
LINK_PATTERN = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
RISK_PATTERNS = (
    (re.compile(r"\brm\s+-rf\b", re.IGNORECASE), "Potentially destructive command: rm -rf"),
    (re.compile(r"\bsudo\b", re.IGNORECASE), "Privileged command detected: sudo"),
    (re.compile(r"\bcurl\b.+\|\s*(?:sh|bash)\b", re.IGNORECASE), "Remote script piped to a shell"),
    (re.compile(r"\bwget\b.+\|\s*(?:sh|bash)\b", re.IGNORECASE), "Remote script piped to a shell"),
)
SECRET_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{12,}"
)


def _parse_frontmatter(text: str) -> tuple[dict[str, str], bool]:
    """Parse a deliberately small YAML frontmatter subset without dependencies."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, False

    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end is None:
        return {}, False

    metadata: dict[str, str] = {}
    for line in lines[1:end]:
        if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip("'\"")
    return metadata, True


def scan_skill(skill_dir: str | Path) -> list[Finding]:
    """Scan one skill directory and return findings.

    This is a heuristic quality check, not a security audit.
    """
    root = Path(skill_dir)
    findings: list[Finding] = []
    skill_file = root / "SKILL.md"

    if not root.exists() or not root.is_dir():
        return [Finding("SG001", "error", "Skill directory does not exist.", str(root))]
    if not skill_file.is_file():
        return [Finding("SG002", "error", "Missing required SKILL.md file.", "SKILL.md")]

    content = skill_file.read_text(encoding="utf-8", errors="replace")
    metadata, has_frontmatter = _parse_frontmatter(content)

    if not has_frontmatter:
        findings.append(Finding(
            "SG003", "error", "Missing or invalid YAML frontmatter.", "SKILL.md", 1
        ))
    else:
        for key in REQUIRED_FRONTMATTER:
            if not metadata.get(key):
                findings.append(Finding(
                    "SG004", "error", f"Missing required frontmatter field: {key}.",
                    "SKILL.md", 2
                ))
        name = metadata.get("name", "")
        if name and not NAME_PATTERN.fullmatch(name):
            findings.append(Finding(
                "SG005", "warning",
                "Skill name should use lowercase letters, numbers, and hyphens only.",
                "SKILL.md", 2
            ))

    for line_number, line in enumerate(content.splitlines(), start=1):
        for pattern, message in RISK_PATTERNS:
            if pattern.search(line):
                findings.append(Finding(
                    "SG010", "warning", message, "SKILL.md", line_number
                ))
        if SECRET_PATTERN.search(line):
            findings.append(Finding(
                "SG011", "warning",
                "Possible hard-coded credential; verify and remove real secrets.",
                "SKILL.md", line_number
            ))

    markdown_files = list(root.rglob("*.md"))
    for md_file in markdown_files:
        text = md_file.read_text(encoding="utf-8", errors="replace")
        for line_number, line in enumerate(text.splitlines(), start=1):
            for target in LINK_PATTERN.findall(line):
                if target.startswith(("http://", "https://", "mailto:", "#")):
                    continue
                local_target = target.split("#", 1)[0]
                if not local_target:
                    continue
                resolved = (md_file.parent / local_target).resolve()
                try:
                    resolved.relative_to(root.resolve())
                except ValueError:
                    findings.append(Finding(
                        "SG012", "warning",
                        "Markdown link points outside the skill directory.",
                        str(md_file.relative_to(root)), line_number
                    ))
                    continue
                if not resolved.exists():
                    findings.append(Finding(
                        "SG013", "warning", f"Broken local Markdown link: {target}",
                        str(md_file.relative_to(root)), line_number
                    ))

    return findings


def calculate_score(findings: list[Finding]) -> int:
    """Return a simple 0-100 score based on finding severity."""
    penalty = sum(20 if f.severity == "error" else 8 for f in findings)
    return max(0, 100 - penalty)
