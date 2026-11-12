from skillguard.scanner import calculate_score, scan_skill


def test_valid_skill_has_no_findings(tmp_path):
    (tmp_path / "SKILL.md").write_text(
        "---\nname: hello-world\ndescription: A sample skill\n---\n# Hello\n",
        encoding="utf-8",
    )
    assert scan_skill(tmp_path) == []


def test_missing_skill_file_is_error(tmp_path):
    findings = scan_skill(tmp_path)
    assert findings[0].code == "SG002"
    assert findings[0].severity == "error"


def test_missing_frontmatter_fields_are_reported(tmp_path):
    (tmp_path / "SKILL.md").write_text("---\nname: demo\n---\n", encoding="utf-8")
    findings = scan_skill(tmp_path)
    assert any(f.code == "SG004" for f in findings)


def test_broken_local_link_is_reported(tmp_path):
    (tmp_path / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Demo\n---\n[Guide](missing.md)\n",
        encoding="utf-8",
    )
    findings = scan_skill(tmp_path)
    assert any(f.code == "SG013" for f in findings)


def test_risky_command_is_flagged(tmp_path):
    (tmp_path / "SKILL.md").write_text(
        "---\nname: demo\ndescription: Demo\n---\nRun `rm -rf /tmp/demo`.\n",
        encoding="utf-8",
    )
    findings = scan_skill(tmp_path)
    assert any(f.code == "SG010" for f in findings)


def test_score_is_bounded():
    assert calculate_score([]) == 100
