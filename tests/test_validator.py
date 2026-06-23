import pytest
from handoff_lint.models import WorkInstruction, ScopeSpec, VerificationSpec
from handoff_lint.validator import validate_instruction

def test_validate_valid_instruction():
    instruction = WorkInstruction(
        goal="Valid Goal",
        scope=ScopeSpec(include=["src/"], exclude=[]),
        verification=VerificationSpec(commands=["pytest"]),
        approval_required_for=["publish"],
        sections=["Context", "Acceptance Criteria"]
    )
    findings = validate_instruction(instruction, has_frontmatter=True)
    assert len(findings) == 0

def test_validate_missing_frontmatter():
    instruction = WorkInstruction(sections=["Context", "Acceptance Criteria"])
    findings = validate_instruction(instruction, has_frontmatter=False)
    
    assert len(findings) == 1
    assert findings[0].code == "frontmatter.missing"
    assert findings[0].severity == "ERROR"

def test_validate_missing_fields():
    instruction = WorkInstruction(
        goal=None,
        scope=None,
        verification=None,
        approval_required_for=None,
        sections=["Context", "Acceptance Criteria"]
    )
    findings = validate_instruction(instruction, has_frontmatter=True)
    
    codes = [f.code for f in findings]
    locations = [f.location for f in findings]
    
    assert "field.missing" in codes
    assert "goal" in locations
    assert "scope" in locations
    assert "verification" in locations
    assert "approval_required_for" in locations

def test_validate_empty_goal():
    instruction = WorkInstruction(
        goal="",
        scope=ScopeSpec(include=["src/"], exclude=[]),
        verification=VerificationSpec(commands=["pytest"]),
        approval_required_for=["publish"],
        sections=["Context", "Acceptance Criteria"]
    )
    findings = validate_instruction(instruction, has_frontmatter=True)
    assert len(findings) == 1
    assert findings[0].code == "field.empty"
    assert findings[0].location == "goal"

def test_validate_invalid_goal_type():
    instruction = WorkInstruction(
        goal=123,  # Invalid type
        scope=ScopeSpec(include=["src/"], exclude=[]),
        verification=VerificationSpec(commands=["pytest"]),
        approval_required_for=["publish"],
        sections=["Context", "Acceptance Criteria"]
    )
    findings = validate_instruction(instruction, has_frontmatter=True)
    assert len(findings) == 1
    assert findings[0].code == "field.empty"
    assert findings[0].location == "goal"

def test_validate_missing_scope_nested():
    instruction = WorkInstruction(
        goal="Goal",
        scope=ScopeSpec(include=None, exclude=None),
        verification=VerificationSpec(commands=["pytest"]),
        approval_required_for=["publish"],
        sections=["Context", "Acceptance Criteria"]
    )
    findings = validate_instruction(instruction, has_frontmatter=True)
    locations = [f.location for f in findings]
    assert "scope.include" in locations
    assert "scope.exclude" in locations

def test_validate_empty_verification_commands():
    instruction = WorkInstruction(
        goal="Goal",
        scope=ScopeSpec(include=["src/"], exclude=[]),
        verification=VerificationSpec(commands=[]),  # Empty commands
        approval_required_for=["publish"],
        sections=["Context", "Acceptance Criteria"]
    )
    findings = validate_instruction(instruction, has_frontmatter=True)
    assert len(findings) == 1
    assert findings[0].code == "field.empty"
    assert findings[0].location == "verification.commands"

def test_validate_missing_sections():
    instruction = WorkInstruction(
        goal="Goal",
        scope=ScopeSpec(include=["src/"], exclude=[]),
        verification=VerificationSpec(commands=["pytest"]),
        approval_required_for=["publish"],
        sections=[]  # Empty sections
    )
    findings = validate_instruction(instruction, has_frontmatter=True)
    codes = [f.code for f in findings]
    locations = [f.location for f in findings]
    
    assert "section.missing" in codes
    assert "Context" in locations
    assert "Acceptance Criteria" in locations

def test_validate_warning_unbounded_scope():
    instruction = WorkInstruction(
        goal="Goal",
        scope=ScopeSpec(include=[], exclude=[]),  # Empty include
        verification=VerificationSpec(commands=["pytest"]),
        approval_required_for=["publish"],
        sections=["Context", "Acceptance Criteria"]
    )
    findings = validate_instruction(instruction, has_frontmatter=True)
    assert len(findings) == 1
    assert findings[0].code == "scope.unbounded"
    assert findings[0].severity == "WARNING"
    assert findings[0].location == "scope.include"

def test_validate_warning_empty_approval():
    instruction = WorkInstruction(
        goal="Goal",
        scope=ScopeSpec(include=["src/"], exclude=[]),
        verification=VerificationSpec(commands=["pytest"]),
        approval_required_for=[],  # Empty approval list
        sections=["Context", "Acceptance Criteria"]
    )
    findings = validate_instruction(instruction, has_frontmatter=True)
    assert len(findings) == 1
    assert findings[0].code == "approval.empty"
    assert findings[0].severity == "WARNING"
    assert findings[0].location == "approval_required_for"
