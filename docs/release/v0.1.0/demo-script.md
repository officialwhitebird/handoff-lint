# Terminal Demo Script: handoff-lint v0.1.0

This script guides you through demonstrating the core capabilities of `handoff-lint` locally.

## 1. Setup and Installation
First, install the package locally in editable mode from the repository root:
```bash
python -m pip install -e .
```

## 2. Running Validation on a Missing/Invalid Frontmatter File
Check an instruction file that completely lacks the YAML frontmatter:
```bash
handoff-lint check tests/fixtures/invalid_missing_frontmatter.md
```
*Expected Output:*
```text
ERROR frontmatter.missing at frontmatter: The file does not start with a valid YAML frontmatter fence (---).

1 findings
exit code: 1
```

## 3. Running Validation on a File with Missing Metadata Fields
Check an instruction file with YAML frontmatter that is missing required keys:
```bash
handoff-lint check tests/fixtures/invalid_missing_fields.md
```
*Expected Output:*
```text
ERROR field.missing at scope: Add scope to the frontmatter.
ERROR field.missing at verification: Add verification.commands with at least one command.
ERROR field.missing at approval_required_for: Add at least one approval-triggering action.

3 findings
exit code: 1
```

## 4. Running Validation on a Correct/Valid File
Check a fully compliant instruction file:
```bash
handoff-lint check tests/fixtures/valid_instruction.md
```
*Expected Output:*
```text
0 findings
exit code: 0
```

## 5. Outputting Validation Findings in JSON Format
Generate machine-readable validation findings for integration into local hooks:
```bash
handoff-lint check tests/fixtures/invalid_missing_fields.md --json
```
*Expected Output:*
```json
{
  "ok": false,
  "findings": [
    {
      "severity": "ERROR",
      "code": "field.missing",
      "location": "scope",
      "message": "Add scope to the frontmatter."
    },
    {
      "severity": "ERROR",
      "code": "field.missing",
      "location": "verification",
      "message": "Add verification.commands with at least one command."
    },
    {
      "severity": "ERROR",
      "code": "field.missing",
      "location": "approval_required_for",
      "message": "Add at least one approval-triggering action."
    }
  ],
  "summary": {
    "error_count": 3,
    "warning_count": 0
  }
}
```

## 6. Testing Unbounded Scopes and Warnings under Strict Mode
Check a file with an empty include scope list. By default, this emits a warning but passes (exit code 0):
```bash
handoff-lint check tests/fixtures/warning_unbounded_scope.md
```
*Expected Output:*
```text
WARNING scope.unbounded at scope.include: scope.include contains zero entries. Execution scope is unbounded.

1 findings
exit code: 0
```

Rerun the check using the `--strict` option to elevate warnings to blocking errors:
```bash
handoff-lint check tests/fixtures/warning_unbounded_scope.md --strict
```
*Expected Output:*
```text
WARNING scope.unbounded at scope.include: scope.include contains zero entries. Execution scope is unbounded.

1 findings
exit code: 1
```
