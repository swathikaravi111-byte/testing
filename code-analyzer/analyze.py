#!/usr/bin/env python3
"""CLI entry point for the intelligent code analysis system.

Usage:
    python analyze.py <source_root> [--out DIR]
"""

import argparse
import sys

from analyzer.report import run


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Multi-language code analysis system")
    parser.add_argument("root", help="Source tree to analyze")
    parser.add_argument("--out", default="docs/generated", help="Output directory for reports")
    args = parser.parse_args(argv)

    result = run(args.root, args.out)
    project = result["project"]
    if project.file_errors:
        print(f"warning: {project.file_errors} files failed to parse", file=sys.stderr)
    print(f"done. reports in {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
