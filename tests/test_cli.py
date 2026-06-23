import os
import sys
import json
import pytest
from handoff_lint.cli import main

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), "fixtures")

def run_cli(args, capsys):
    # Backup argv
    old_argv = sys.argv
    sys.argv = ["handoff-lint"] + args
    
    exit_code = 0
    try:
        main()
    except SystemExit as e:
        exit_code = e.code
    finally:
        # Restore argv
        sys.argv = old_argv
        
    captured = capsys.readouterr()
    return exit_code, captured.out, captured.err

def test_cli_valid_file(capsys):
    filepath = os.path.join(FIXTURES_DIR, "valid_instruction.md")
    exit_code, out, err = run_cli(["check", filepath], capsys)
    
    assert exit_code == 0
    assert "0 findings" in out
    assert "exit code: 0" in out
    assert err == ""

def test_cli_invalid_file(capsys):
    filepath = os.path.join(FIXTURES_DIR, "invalid_missing_frontmatter.md")
    exit_code, out, err = run_cli(["check", filepath], capsys)
    
    assert exit_code == 1
    assert "frontmatter.missing" in out
    assert "1 findings" in out
    assert "exit code: 1" in out

def test_cli_warning_only(capsys):
    filepath = os.path.join(FIXTURES_DIR, "warning_unbounded_scope.md")
    exit_code, out, err = run_cli(["check", filepath], capsys)
    
    assert exit_code == 0
    assert "scope.unbounded" in out
    assert "exit code: 0" in out

def test_cli_warning_strict(capsys):
    filepath = os.path.join(FIXTURES_DIR, "warning_unbounded_scope.md")
    exit_code, out, err = run_cli(["check", filepath, "--strict"], capsys)
    
    assert exit_code == 1
    assert "scope.unbounded" in out
    assert "exit code: 1" in out

def test_cli_malformed_yaml(capsys):
    filepath = os.path.join(FIXTURES_DIR, "malformed_yaml.md")
    exit_code, out, err = run_cli(["check", filepath], capsys)
    
    assert exit_code == 2
    assert "Operational error" in err

def test_cli_json_valid(capsys):
    filepath = os.path.join(FIXTURES_DIR, "valid_instruction.md")
    exit_code, out, err = run_cli(["check", filepath, "--json"], capsys)
    
    assert exit_code == 0
    data = json.loads(out)
    assert data["ok"] is True
    assert len(data["findings"]) == 0
    assert data["summary"]["error_count"] == 0

def test_cli_json_invalid(capsys):
    filepath = os.path.join(FIXTURES_DIR, "invalid_missing_frontmatter.md")
    exit_code, out, err = run_cli(["check", filepath, "--json"], capsys)
    
    assert exit_code == 1
    data = json.loads(out)
    assert data["ok"] is False
    assert len(data["findings"]) == 1
    assert data["findings"][0]["code"] == "frontmatter.missing"
    assert data["summary"]["error_count"] == 1

def test_cli_invalid_command(capsys):
    exit_code, out, err = run_cli(["invalid_subcommand"], capsys)
    assert exit_code == 2
