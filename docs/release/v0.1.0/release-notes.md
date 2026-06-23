# Release Notes: handoff-lint v0.1.0

Initial experimental release candidate.

`handoff-lint` is a local-first CLI tool for checking the structure of coding-agent work instruction files before execution. It validates Markdown files with YAML frontmatter and reports deterministic findings for missing fields, missing required sections, unbounded scopes, and empty approval triggers.

## What is included

- `handoff-lint check <path-to-file>` CLI command
- Markdown + YAML frontmatter parser
- Deterministic validation rules
- Human-readable output
- `--json` machine-readable output
- `--strict` mode for warning-only failures
- 23 pytest cases
- GitHub Actions workflow file
- MIT license

## Verified locally

```bash
python -m pytest -q
```

Observed result:

```text
23 passed
```

Representative behavior:

- valid instruction fixture exits `0`
- missing required fields exits `1`
- warning-only fixture exits `0`, or `1` with `--strict`
- malformed YAML exits `2`

## Boundaries

- Experimental prototype
- Not validated for broad production use
- Does not use an LLM
- Does not modify files
- Does not contact external services
- Does not collect telemetry
- Does not execute verification commands
- Does not perform semantic prose grading

## Publication status

Published as `v0.1.0`.
