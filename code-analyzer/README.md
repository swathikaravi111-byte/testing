# Intelligent Code Analysis System

Multi-language static analysis engine that scans Java, Python, TypeScript, and C++
source trees and produces four generated reports:

| Report | Contents |
|---|---|
| `API_REFERENCE.md` | Extracted function signatures, parameter tables, return/throws info, per-function usage examples |
| `ARCHITECTURE.md` | Project statistics, Mermaid module dependency graph, class diagram, per-module structure listing |
| `QUALITY_REPORT.md` | Smell summary, detailed findings with severity, complexity hotspots |
| `REFACTORING.md` | Refactoring suggestions with before/after code samples |

## Usage

```bash
python analyze.py <source_root> [--out OUTPUT_DIR]
# e.g.
python analyze.py sample-project --out docs/generated
```

Stdlib only — no third-party dependencies.

## What it detects

- **Complexity metrics**: McCabe cyclomatic complexity, LOC, nesting depth, parameter count
- **Code smells**: long functions, high complexity, deep nesting, too many parameters,
  duplicated code (normalized body hashing), magic numbers, empty catch blocks,
  print-debugging, TODO/FIXME markers
- **Structure**: classes/interfaces/records with inheritance and implementation
  relationships, imports, docstring/Javadoc extraction

## Layout

```
analyzer/           analysis library
  models.py         data models (Function, ClassInfo, FileAnalysis, ...)
  parsers.py        regex-based parsers for Java / Python / TypeScript / C++
  metrics.py        complexity, line counting, comment/string stripping
  smells.py         smell detection rules + duplication hashing
  refactoring.py    refactoring recipes with before/after samples
  docs.py           API documentation generator
  architecture.py   Mermaid diagrams and architecture report
  report.py         orchestrator
analyze.py           CLI entry point
tests/               unit + end-to-end tests
```

## Notes

- Parsers are regex-based and tolerant; they never crash on a single bad file
  (errors are counted in `ProjectAnalysis.file_errors`).
- The scanner excludes `node_modules`, `venv`, `build`, `dist`, `.git`, etc.

## Tests

```bash
cd code-analyzer && python -m unittest discover -s tests
```
