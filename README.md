# SkillGuard

Static quality, structure, and security checks for AI Agent Skills.

> Early MVP. Findings are heuristics, not proof that a Skill is safe or malicious.

## Features

- Check for a `SKILL.md` file and basic YAML frontmatter fields.
- Check basic skill-name formatting.
- Check referenced local Markdown files.
- Flag selected risky shell commands and credential-like literals.
- Print terminal reports or export JSON.
- Run tests through GitHub Actions.

## Requirements

Python 3.10 or newer. SkillGuard does not need an AI API key.

## Install

From the repository root:

```bash
python -m pip install .
```

## Usage

Scan the example skill:

```bash
skillguard examples/sample-skill
```

Print a JSON report:

```bash
skillguard examples/sample-skill --json
```

Show available options:

```bash
skillguard --help
```

## Security

SkillGuard performs static inspection only. It never executes scripts from scanned Skills.
A clean report is not a security guarantee. Findings may be false positives or false negatives;
manually review results and use proper isolation for untrusted code.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Add tests for new rules.

## License

MIT.
