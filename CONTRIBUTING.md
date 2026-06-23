# Contributing to handoff-lint

Thank you for your interest in contributing to handoff-lint.

## Local Setup

This project requires Python 3.11 or higher.

1. Clone the repository locally.
2. Initialize a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install the package in editable mode along with test dependencies:
   ```bash
   python -m pip install -e .[test]
   ```

## Running Tests

We use `pytest` for running unit and integration tests. Run the test suite using:

```bash
python -m pytest
```

Ensure all tests pass and coverage requirements are met before submitting pull requests.
