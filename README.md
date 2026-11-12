# SkillGuard

Static quality, structure, and security checks for Agent Skills.

> Early MVP. Findings are heuristics, not proof that a Skill is safe or malicious.

## Features
- Parse `SKILL.md` YAML frontmatter.
- Check required metadata and basic naming conventions.
- Check referenced local Markdown files.
- Flag selected risky shell commands and credential-like literals.
- Print terminal reports or export JSON.
- Run tests through GitHub Actions.

## Install
Requires Python 3.10+. No AI API key or network connection is needed to scan local folders.

```bash
python -m pip install .
skillguard scan examples/sample-skill
skillguard scan examples/sample-skill --format json --output report.json
```

## Security
SkillGuard performs static inspection only. It never executes scripts from scanned Skills. A clean report is not a security guarantee; manually review findings and use proper isolation for untrusted code.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Add tests for new rules.

## License
MIT.
