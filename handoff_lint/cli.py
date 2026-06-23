import sys
import json
import argparse
from handoff_lint.parser import parse_instruction_file, OperationalError
from handoff_lint.validator import validate_instruction

def main():
    parser = argparse.ArgumentParser(description="Lints agent work instructions.")
    subparsers = parser.add_subparsers(dest="command")
    
    check_parser = subparsers.add_parser("check")
    check_parser.add_argument("file", help="Path to work instruction file")
    check_parser.add_argument("--json", action="store_true", help="Output in JSON format")
    check_parser.add_argument("--strict", action="store_true", help="Elevate warnings to errors")
    
    args = parser.parse_args()
    
    if args.command != "check":
        parser.print_help()
        sys.exit(2)
        
    try:
        instruction, has_frontmatter = parse_instruction_file(args.file)
    except OperationalError as e:
        # For exit code 2, we print the operational error to stderr and exit.
        print(f"Operational error: {e}", file=sys.stderr)
        sys.exit(2)
    except Exception as e:
        print(f"Operational error: {e}", file=sys.stderr)
        sys.exit(2)
        
    findings = validate_instruction(instruction, has_frontmatter)
    
    error_count = sum(1 for f in findings if f.severity == "ERROR")
    warning_count = sum(1 for f in findings if f.severity == "WARNING")
    
    # Validation fails if errors exist, or if warnings exist under --strict
    is_blocked = error_count > 0 or (args.strict and warning_count > 0)
    
    if args.json:
        output_data = {
            "ok": not is_blocked,
            "findings": [
                {
                    "severity": f.severity,
                    "code": f.code,
                    "location": f.location,
                    "message": f.message
                }
                for f in findings
            ],
            "summary": {
                "error_count": error_count,
                "warning_count": warning_count
            }
        }
        print(json.dumps(output_data, indent=2))
    else:
        for f in findings:
            print(f"{f.severity} {f.code} at {f.location}: {f.message}")
        print()
        print(f"{len(findings)} findings")
        print(f"exit code: {1 if is_blocked else 0}")
        
    if is_blocked:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
