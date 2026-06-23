import os
import re
import yaml
from typing import Tuple, List
from handoff_lint.models import WorkInstruction, ScopeSpec, VerificationSpec

class OperationalError(Exception):
    """Raised for operational failures (unreadable file, malformed YAML/frontmatter)."""
    pass

def parse_instruction_file(filepath: str) -> Tuple[WorkInstruction, bool]:
    """
    Reads the target file, extracts YAML frontmatter, and parses the body sections.
    Returns a Tuple (WorkInstruction, has_frontmatter).
    Raises OperationalError for operational failures.
    """
    if not os.path.exists(filepath):
        raise OperationalError(f"File not found: {filepath}")
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        raise OperationalError(f"Error reading file: {e}")

    # Check if content starts with frontmatter fence (---)
    # Must start exactly at character 0
    has_frontmatter = content.startswith("---")
    
    yaml_data = {}
    markdown_body = content
    
    if has_frontmatter:
        # Split content on '---'
        # content.split("---", 2) splits into:
        # [0] (empty string before first '---'), [1] (YAML content), [2] (Markdown body)
        parts = content.split("---", 2)
        if len(parts) < 3:
            raise OperationalError("Malformed frontmatter: missing closing fence '---'")
        
        frontmatter_str = parts[1]
        markdown_body = parts[2]
        
        try:
            yaml_data = yaml.safe_load(frontmatter_str) or {}
        except Exception as e:
            raise OperationalError(f"Malformed YAML frontmatter: {e}")

    # Extract Markdown headings from the body
    headings = []
    # Match lines starting with 1 to 6 hash signs, optional whitespace, and heading title
    heading_pattern = re.compile(r'^#{1,6}\s+(.+?)\s*$', re.MULTILINE)
    for match in heading_pattern.finditer(markdown_body):
        headings.append(match.group(1).strip())

    if not has_frontmatter:
        return WorkInstruction(sections=headings), False

    # Extract goal
    goal = yaml_data.get("goal") if "goal" in yaml_data else None

    # Extract scope
    if "scope" in yaml_data:
        s_data = yaml_data["scope"]
        if isinstance(s_data, dict):
            include = s_data.get("include") if "include" in s_data else None
            exclude = s_data.get("exclude") if "exclude" in s_data else None
            scope_spec = ScopeSpec(include=include, exclude=exclude)
        else:
            # If scope is not a dictionary (e.g. string or list),
            # store it as-is in WorkInstruction so validator can catch the type error
            scope_spec = s_data
    else:
        scope_spec = None

    # Extract verification
    if "verification" in yaml_data:
        v_data = yaml_data["verification"]
        if isinstance(v_data, dict):
            commands = v_data.get("commands") if "commands" in v_data else None
            verification_spec = VerificationSpec(commands=commands)
        else:
            # Store raw verification data for type check in validator
            verification_spec = v_data
    else:
        verification_spec = None

    # Extract approval_required_for
    approval_required_for = yaml_data.get("approval_required_for") if "approval_required_for" in yaml_data else None

    instruction = WorkInstruction(
        goal=goal,
        scope=scope_spec,
        verification=verification_spec,
        approval_required_for=approval_required_for,
        sections=headings
    )
    
    return instruction, True
