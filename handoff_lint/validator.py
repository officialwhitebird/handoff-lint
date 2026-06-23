from typing import List
from handoff_lint.models import WorkInstruction, Finding, ScopeSpec, VerificationSpec

def validate_instruction(instruction: WorkInstruction, has_frontmatter: bool) -> List[Finding]:
    """
    Validates the WorkInstruction and returns a list of Findings in deterministic order.
    """
    findings = []
    
    # 1. Rule frontmatter.missing
    if not has_frontmatter:
        findings.append(Finding(
            severity="ERROR",
            code="frontmatter.missing",
            location="frontmatter",
            message="The file does not start with a valid YAML frontmatter fence (---)."
        ))
        return findings  # Short-circuit as required by the spec

    # 2. Rule field.missing & field.empty validations

    # goal
    if instruction.goal is None:
        findings.append(Finding(
            severity="ERROR",
            code="field.missing",
            location="goal",
            message="Add goal to the frontmatter."
        ))
    elif not isinstance(instruction.goal, str):
        findings.append(Finding(
            severity="ERROR",
            code="field.empty",
            location="goal",
            message="goal must be a string."
        ))
    elif not instruction.goal.strip():
        findings.append(Finding(
            severity="ERROR",
            code="field.empty",
            location="goal",
            message="goal cannot be empty."
        ))

    # scope
    if instruction.scope is None:
        findings.append(Finding(
            severity="ERROR",
            code="field.missing",
            location="scope",
            message="Add scope to the frontmatter."
        ))
    elif not isinstance(instruction.scope, ScopeSpec):
        findings.append(Finding(
            severity="ERROR",
            code="field.empty",
            location="scope",
            message="scope must be a mapping."
        ))
    else:
        # scope.include
        if instruction.scope.include is None:
            findings.append(Finding(
                severity="ERROR",
                code="field.missing",
                location="scope.include",
                message="Add scope.include to the frontmatter."
            ))
        elif not isinstance(instruction.scope.include, list):
            findings.append(Finding(
                severity="ERROR",
                code="field.empty",
                location="scope.include",
                message="scope.include must be a list."
            ))

        # scope.exclude
        if instruction.scope.exclude is None:
            findings.append(Finding(
                severity="ERROR",
                code="field.missing",
                location="scope.exclude",
                message="Add scope.exclude to the frontmatter."
            ))
        elif not isinstance(instruction.scope.exclude, list):
            findings.append(Finding(
                severity="ERROR",
                code="field.empty",
                location="scope.exclude",
                message="scope.exclude must be a list."
            ))

    # verification
    if instruction.verification is None:
        # Note: The JSON example maps this exact case to location="verification" and message="Add verification.commands with at least one command."
        findings.append(Finding(
            severity="ERROR",
            code="field.missing",
            location="verification",
            message="Add verification.commands with at least one command."
        ))
    elif not isinstance(instruction.verification, VerificationSpec):
        findings.append(Finding(
            severity="ERROR",
            code="field.empty",
            location="verification",
            message="verification must be a mapping."
        ))
    else:
        # verification.commands
        if instruction.verification.commands is None:
            findings.append(Finding(
                severity="ERROR",
                code="field.missing",
                location="verification.commands",
                message="Add verification.commands with at least one command."
            ))
        elif not isinstance(instruction.verification.commands, list):
            findings.append(Finding(
                severity="ERROR",
                code="field.empty",
                location="verification.commands",
                message="verification.commands must be a list."
            ))
        elif len(instruction.verification.commands) == 0:
            findings.append(Finding(
                severity="ERROR",
                code="field.empty",
                location="verification.commands",
                message="Add verification.commands with at least one command."
            ))

    # approval_required_for
    if instruction.approval_required_for is None:
        findings.append(Finding(
            severity="ERROR",
            code="field.missing",
            location="approval_required_for",
            message="Add at least one approval-triggering action."
        ))
    elif not isinstance(instruction.approval_required_for, list):
        findings.append(Finding(
            severity="ERROR",
            code="field.empty",
            location="approval_required_for",
            message="approval_required_for must be a list."
        ))

    # Required body headings
    if "Context" not in instruction.sections:
        findings.append(Finding(
            severity="ERROR",
            code="section.missing",
            location="Context",
            message="Required heading 'Context' is missing from the body."
        ))
        
    if "Acceptance Criteria" not in instruction.sections:
        findings.append(Finding(
            severity="ERROR",
            code="section.missing",
            location="Acceptance Criteria",
            message="Required heading 'Acceptance Criteria' is missing from the body."
        ))

    # Warnings (only when keys exist and are of valid types)
    if (instruction.scope is not None and 
        isinstance(instruction.scope, ScopeSpec) and 
        isinstance(instruction.scope.include, list) and 
        len(instruction.scope.include) == 0):
        findings.append(Finding(
            severity="WARNING",
            code="scope.unbounded",
            location="scope.include",
            message="scope.include contains zero entries. Execution scope is unbounded."
        ))
        
    if (instruction.approval_required_for is not None and 
        isinstance(instruction.approval_required_for, list) and 
        len(instruction.approval_required_for) == 0):
        findings.append(Finding(
            severity="WARNING",
            code="approval.empty",
            location="approval_required_for",
            message="approval_required_for list is empty."
        ))
        
    return findings
