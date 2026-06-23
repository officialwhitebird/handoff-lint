# Case Study: Building handoff-lint — Structural Linting for Coding Agent Work Instructions

## Project Overview
- **Project Name**: handoff-lint
- **Role**: Portfolio Project
- **Purpose**: Catch structural omissions in agent instructions before sending work to an AI agent.

## The Problem
AI coding agents are highly sensitive to the structure and boundaries of their instructions. When writing handoff files or task descriptions manually, authors often leave out critical metadata:
- Defining the precise goal of the instruction.
- Setting explicit scope boundaries (which directories to modify and which to exclude).
- Establishing explicit verification steps (commands to test the outcome).
- Declaring clear approval boundaries for high-risk operations (e.g. file deletion or publishing).

When these elements are missing, coding agents might guess, modify unrelated files, or run destructive operations without approval, resulting in wasted cycles and manual rework.

## The Solution
To address this workflow friction, `handoff-lint` was built as a lightweight, local-first linting tool. Instead of relying on slow or non-deterministic large language models (LLMs) to grade text quality, `handoff-lint` applies simple, deterministic structural rules to instruction files written in Markdown with a YAML frontmatter.

### Core Design Principles
- **Read-Only**: The linter reads instruction files without modifying them.
- **Deterministic**: The check is fast, predictable, and runs offline on the developer's local machine.
- **Strict Boundary Control**: Unbounded scopes (empty include list) and empty approval declarations trigger warnings that can be elevated to errors via command flags.

## What Was Built
We implemented a self-contained, single-purpose Python tool with the following layout:
- **Models**: Simple dataclasses mapping frontmatter properties (goal, scope, verification, approval) and findings.
- **Parser**: Extracted the YAML frontmatter section and markdown headings (specifically checking for Context and Acceptance Criteria).
- **Validator**: Evaluated the parsed instruction and returned structured error or warning findings.
- **CLI**: Provided a `check` command supporting optional `--json` schemas and `--strict` warnings.

## Verification Evidence
The tool was tested against 23 deterministic test cases covering edge cases, missing fields, empty fields, malformed frontmatter syntax, and command line options.
```bash
python -m pytest
```
All tests pass cleanly. 

The CLI provides standard output formats and structured JSON outputs to integrate with local hooks or local verification scripts.

## Boundaries and Non-Goals
The tool is strictly limited to structural syntax validation:
- It does not check if the paths declared in the scope actually exist on the disk.
- It does not run the verification commands.
- It does not provide subjective language quality grading or automatic fixes.

## Garage and Factory Alignment
This project is built under the officialwhitebird garage, which aims to convert recurring AI orchestration frictions into small, single-purpose, reproducible tools. Verifying instruction structure is intended to catch structural omissions in handoff instructions locally before agent invocation, supporting more consistent, explicitly-bounded handoffs.
