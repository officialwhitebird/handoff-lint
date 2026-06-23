# Release Evidence: handoff-lint v0.1.0

This document contains local validation and build evidence for handoff-lint v0.1.0 prior to publication approval.

## 1. Package Identification
- **Package Name**: handoff-lint
- **Target Version**: 0.1.0
- **License**: MIT
- **Dependencies**: Python >=3.11, PyYAML >=6.0.1 (sole external runtime dependency)

## 2. Installation and Build Verification
The package can be installed locally in editable mode from the repository root:
```bash
python -m pip install -e .
```
This successfully registers the console script `handoff-lint`.

## 3. Test Suite Results
All unit and integration tests must pass cleanly. 
- **Command**: `python -m pytest`
- **Output (Observed)**: 23 passed in 0.10s
- **Coverage**: Covers models, frontmatter parsing, validator rules, strict mode warning behavior, malformed YAML handling, and JSON schema output structure.

## 4. CLI Exit-code Verification
The CLI tool `handoff-lint check <path-to-file>` exhibits deterministic behavior:

| Command | Case Description | Target Fixture Path | Expected Exit Code |
| --- | --- | --- | --- |
| `handoff-lint check <file>` | Valid instruction format | `tests/fixtures/valid_instruction.md` | 0 |
| `handoff-lint check <file>` | Missing YAML frontmatter block | `tests/fixtures/invalid_missing_frontmatter.md` | 1 |
| `handoff-lint check <file>` | Missing required frontmatter fields | `tests/fixtures/invalid_missing_fields.md` | 1 |
| `handoff-lint check <file>` | Missing required body sections | `tests/fixtures/invalid_missing_sections.md` | 1 |
| `handoff-lint check <file>` | Unbounded scope (empty include list) | `tests/fixtures/warning_unbounded_scope.md` | 0 |
| `handoff-lint check <file> --strict` | Unbounded scope (under strict flag) | `tests/fixtures/warning_unbounded_scope.md` | 1 |
| `handoff-lint check <file>` | Malformed/Invalid YAML frontmatter | `tests/fixtures/malformed_yaml.md` | 2 |

## 5. JSON Output Schema Validation
When running with the `--json` option, the CLI outputs a valid JSON object matching the specification.
Example stdout for `handoff-lint check tests/fixtures/invalid_missing_fields.md --json`:
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

## 6. Privacy & Security Boundary Audit
- **Read-Only**: The CLI tool functions purely as a linter. It opens target files exclusively in read mode (`open(..., 'r')`) and does not perform write, delete, or modify actions on the workspace.
- **Local-Only**: No external API endpoints or network sockets are contacted. Runtime modules use only Python standard libraries and PyYAML.
- **No Telemetry**: The package contains no background processes, metric collectors, or crash reporting telemetry.

## 7. Known Limitations
- The tool validates syntax and structural field presence only.
- It does not check if target filepaths mentioned in the scope actually exist in the workspace.
- It does not execute or verify the success of verification commands.
- No semantic language analysis or subjective prose grading is performed.

## 8. Publication Status
- **Status**: Not published. External publication is pending owner approval.
