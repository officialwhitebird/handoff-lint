# Distribution Copy: handoff-lint v0.1.0

This document contains pre-written distribution materials for handoff-lint v0.1.0. All copy avoids unproven performance claims or demand assertions.

## 1. GitHub Repository Description
"A local, offline CLI tool to verify the structure, metadata, and sections of agent work instruction files before execution."

## 2. README Tagline Alternative
"Check structural discipline in your agent instructions: goals, scopes, approval boundaries, and verification commands."

## 3. X (Twitter) Post Drafts (3 variants)

### Variant A: Problem & Solution focus
"AI coding agents work best when given clear scope boundaries and verification steps. But manually writing instructions often leads to missing metadata.
handoff-lint is an experimental, offline CLI tool to check your instruction structure locally before sending them to an agent."

### Variant B: Technical detail focus
"Just built handoff-lint: a tiny Python CLI that statically parses instruction files (Markdown with YAML frontmatter). 
It checks for goal, scope boundaries, verification commands, and Context/Acceptance headings. Purely local, offline, and read-only.
GitHub Actions CI configured."

### Variant C: Portfolio context focus
"Part of the officialwhitebird garage projects: handoff-lint v0.1.0 is a local linter designed to check structural discipline in agent handoff instructions.
Deterministically warns about unbounded scopes or empty approval steps."

## 4. Release Announcement Draft
"We are pleased to introduce handoff-lint v0.1.0, an experimental local-first CLI tool to validate the structure of agent work instructions.

AI coding agents are highly sensitive to scope boundaries and verification commands. Missing metadata often translates directly into failed attempts or unintended modifications. 

handoff-lint addresses this friction by evaluating Markdown instruction files starting with a YAML frontmatter fence. It checks for:
- Required metadata: goal, scope, verification commands, and approval steps.
- Body headings: Context and Acceptance Criteria.
- Potential risks: warns against unbounded scopes (empty include list) or empty approval declarations.

The linter runs locally and does not contact any external servers, collect telemetry, or modify files. It is an experimental prototype intended for local workflow inspection."

## 5. Short Video Script Outline (Under 1 minute)
- **Visual**: Terminal screen showing a markdown file.
- **Audio/Voiceover**: "AI coding agents are powerful, but they work best with structured instructions. Vague goals, unbounded scopes, or missing verification steps can make a task harder to review."
- **Visual**: Cursor runs `handoff-lint check invalid.md` in terminal. Errors show up for missing verification and approval.
- **Audio/Voiceover**: "handoff-lint catches these structural omissions locally on your machine before you send the task to an agent."
- **Visual**: Show YAML file edits (adding fields), then rerun linter. It passes cleanly.
- **Audio/Voiceover**: "Catch structural omissions before execution, set explicit boundaries, and keep review points visible. handoff-lint is local, offline, and read-only."
