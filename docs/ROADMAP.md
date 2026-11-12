# SkillGuard Roadmap

## v0.1.0 — Initial MVP
- [x] Scan a skill folder for `SKILL.md`
- [x] Check basic frontmatter fields
- [x] Check skill-name formatting
- [x] Detect broken local Markdown links
- [x] Flag selected risky command patterns
- [x] Export JSON reports
- [x] Run tests in GitHub Actions

## Planned
- [ ] More complete YAML parsing
- [ ] SARIF output for code-scanning integrations
- [ ] Configurable rules and severity levels
- [ ] Compatibility profiles for popular agent-skill formats
- [ ] HTML report
- [ ] Additional tests and security-focused review

SkillGuard is a heuristic checker. Findings can be false positives or false negatives;
it must not be treated as a security audit.
