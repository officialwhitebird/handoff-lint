# handoff-lint

A local tool to check coding-agent work instructions before execution.

## Status

Experimental. This project is a prototype designed for local verification of instruction structure. It is not currently validated for broad production use.

## What Problem It Solves

Coding agents work best when given clear, structured context, strict scopes, and explicit verification steps. However, writing these instructions manually often leads to missing metadata, unbounded execution scopes, or forgotten approval triggers. 

handoff-lint helps instruction authors catch these mechanical structural omissions locally on their own machines before sending the work to an agent.

## What It Checks

handoff-lint checks work instruction files written in Markdown with a YAML frontmatter fence. It verifies:
- Presence and syntax of the YAML frontmatter.
- Required frontmatter fields: goal, scope (include/exclude), verification, and approval_required_for.
- Non-empty values in those fields.
- Required Markdown headings in the body: Context, Acceptance Criteria.
- Potential risks like unbounded scopes or empty approval triggers (as warnings).

It does not check writing quality, clarity, or completeness of the prose, and it does not use a large language model (LLM).

## Input Format

handoff-lint accepts exactly one input format: a Markdown file starting with a YAML frontmatter block, followed by the Markdown body.

Example structure:
```markdown
---
goal: Describe the requested outcome
scope:
  include:
    - src/example.py
  exclude:
    - deployment
verification:
  commands:
    - python -m pytest
approval_required_for:
  - publish
  - delete
---

## Context
Provide necessary context here.

## Acceptance Criteria
Provide acceptance criteria here.
```

## 30-Second Quick Start

Run the tool against your instruction Markdown file:

handoff-lint check instruction.md

## Example: Invalid Instruction

Suppose you have an instruction file named invalid.md with missing verification and approval fields:

```markdown
---
goal: Refactor helper functions
scope:
  include:
    - src/helper.py
  exclude: []
---

## Context
Refactor the old helper modules.

## Acceptance Criteria
- All tests pass.
```

Running the check command:

```text
$ handoff-lint check invalid.md
ERROR field.missing at verification: Add verification.commands with at least one command.
ERROR field.missing at approval_required_for: Add at least one approval-triggering action.

2 findings
exit code: 1
```

## Example: Corrected Instruction

After adding the missing fields:

```markdown
---
goal: Refactor helper functions
scope:
  include:
    - src/helper.py
  exclude: []
verification:
  commands:
    - python -m pytest
approval_required_for:
  - publish
  - delete
---

## Context
Refactor the old helper modules.

## Acceptance Criteria
- All tests pass.
```

Running the check command again:

```text
$ handoff-lint check corrected.md

0 findings
exit code: 0
```

## CLI Reference

handoff-lint check <path-to-file>

Options:
```text
--json: Output the results in JSON format.
--strict: Elevate warning-level findings to blocking errors (exits with code 1 if warnings are present).
```

## Finding Codes

The tool produces deterministic findings with the following codes:

- ERROR frontmatter.missing: The file does not start with a valid YAML frontmatter fence (---).
- ERROR field.missing: A required field or nested key is missing from the frontmatter.
- ERROR field.empty: A required field exists but has an empty string (specifically for goal), empty list (specifically for verification.commands), or empty mapping. Empty scope.include and approval_required_for lists do not trigger field.empty.
- ERROR section.missing: A required Markdown heading (Context or Acceptance Criteria) is missing from the body.
- WARNING scope.unbounded: The scope.include field contains zero entries.
- WARNING approval.empty: The approval_required_for field is defined but contains zero entries.

## Exit Codes

The tool returns the following exit codes:
- 0: Success. No blocking findings (warnings do not block unless --strict is set).
- 1: Validation failed. One or more ERROR findings were detected, or WARNING findings were detected under --strict.
- 2: Operational failure. The command was invalid, the file was unreadable, or the YAML frontmatter was malformed (YAML syntax error).

## JSON Output

When running with the --json option:

```text
$ handoff-lint check invalid.md --json
```

```json
{
  "ok": false,
  "findings": [
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
    "error_count": 2,
    "warning_count": 0
  }
}
```

## Read-Only and Privacy

handoff-lint is a local-first command-line tool.
- It operates completely read-only and never modifies the target file.
- It does not require internet access or contact external servers.
- It does not collect telemetry, usage metrics, or send code snippets anywhere.

## Scope and Limitations

- Only validates the structure and presence of fields.
- Does not check if the paths in scope actually exist.
- Does not run the verification commands during linting.
- No semantic prose checking or quality grading.

## Development

Prerequisites: Python 3.11 or higher.

To install dependencies and run tests:

```bash
python -m pip install -e .
python -m pytest
```

## License

This project is licensed under the MIT License.
