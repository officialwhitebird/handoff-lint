import os
import pytest
from handoff_lint.parser import parse_instruction_file, OperationalError

# Path helper for fixtures
FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def test_parse_valid_instruction():
    filepath = os.path.join(FIXTURES_DIR, "valid_instruction.md")
    instruction, has_fm = parse_instruction_file(filepath)
    
    assert has_fm is True
    assert instruction.goal == "Test valid structure"
    assert instruction.scope.include == ["src/"]
    assert instruction.scope.exclude == ["dist/"]
    assert instruction.verification.commands == ["pytest"]
    assert instruction.approval_required_for == ["deploy"]
    assert "Context" in instruction.sections
    assert "Acceptance Criteria" in instruction.sections

def test_parse_missing_file():
    with pytest.raises(OperationalError) as exc:
        parse_instruction_file("non_existent_file.md")
    assert "File not found" in str(exc.value)

def test_parse_missing_frontmatter():
    filepath = os.path.join(FIXTURES_DIR, "invalid_missing_frontmatter.md")
    instruction, has_fm = parse_instruction_file(filepath)
    
    assert has_fm is False
    assert instruction.goal is None
    assert "Context" in instruction.sections
    assert "Acceptance Criteria" in instruction.sections

def test_parse_malformed_yaml():
    filepath = os.path.join(FIXTURES_DIR, "malformed_yaml.md")
    with pytest.raises(OperationalError) as exc:
        parse_instruction_file(filepath)
    assert "Malformed YAML frontmatter" in str(exc.value)

def test_parse_missing_closing_fence():
    # Create a temporary file with missing closing fence
    content = "---\ngoal: test\nscope:\n  include: []"
    temp_file = os.path.join(FIXTURES_DIR, "temp_missing_close.md")
    with open(temp_file, "w", encoding="utf-8") as f:
        f.write(content)
        
    try:
        with pytest.raises(OperationalError) as exc:
            parse_instruction_file(temp_file)
        assert "Malformed frontmatter: missing closing fence" in str(exc.value)
    finally:
        if os.path.exists(temp_file):
            os.remove(temp_file)
