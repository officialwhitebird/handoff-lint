# Publish Prep: handoff-lint v0.1.0

This document is the final local checklist before owner-approved publication.

Publication is not performed by this document. GitHub repository creation, push, release, and external posting remain owner-gated actions.

## Recommended GitHub repository settings

- Repository name: `handoff-lint`
- Visibility: public, if owner approves publication
- Description:

```text
A local, offline CLI tool to verify the structure, metadata, and sections of agent work instruction files before execution.
```

- Suggested topics:

```text
ai-agents
cli
developer-tools
linting
markdown
python
yaml
local-first
agent-tools
workflow
```

## Release tag

```text
v0.1.0
```

## Release title

```text
handoff-lint v0.1.0
```

## Release notes source

Use:

```text
docs/release/v0.1.0/release-notes.md
```

## Pre-publish local checks

Run from the repository root:

```bash
python -m pytest -q
handoff-lint check tests\fixtures\invalid_missing_fields.md
handoff-lint check tests\fixtures\valid_instruction.md
handoff-lint check tests\fixtures\warning_unbounded_scope.md --strict
handoff-lint check tests\fixtures\malformed_yaml.md
handoff-lint check tests\fixtures\invalid_missing_fields.md --json
```

Expected results:

- pytest passes
- invalid missing fields exits `1`
- valid fixture exits `0`
- strict warning fixture exits `1`
- malformed YAML exits `2`
- JSON command exits `1` and prints a valid JSON validation payload

## Public claim guardrails

Allowed:

- experimental
- local-first
- offline
- read-only
- no telemetry
- deterministic structural checks
- Markdown + YAML frontmatter validation
- JSON output
- strict warning handling

Avoid:

- demand validation claims
- adoption claims
- production-ready claims
- time-savings claims
- productivity magnitude claims
- enterprise readiness claims
- claims that imply semantic prose understanding

## Recommended next owner action

If the owner approves publication:

1. Create the GitHub repository under `officialwhitebird/handoff-lint`.
2. Initialize git locally if needed.
3. Commit the current repository state.
4. Add the GitHub remote.
5. Push the default branch.
6. Create tag `v0.1.0`.
7. Create the GitHub release using `docs/release/v0.1.0/release-notes.md`.
8. Add repository description and topics.
9. Only after repository page review, use the prepared distribution copy.

## Current recommendation

Ready for owner approval to publish.

