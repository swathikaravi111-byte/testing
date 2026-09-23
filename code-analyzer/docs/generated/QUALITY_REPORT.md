# Code Quality Report

_Generated 2026-09-23T11:32:19+00:00_

## Smell Summary

| Smell | Occurrences | Severity |
|---|---|---|
| High Cyclomatic Complexity | 11 | high |
| TODO/FIXME Left In Code | 6 | low |
| Very Long Line | 5 | low |
| Long Function | 4 | medium |
| Deep Nesting | 3 | medium |
| Magic Numbers | 3 | low |
| Print Debugging | 2 | low |
| Possible Code Duplication | 2 | high |
| Too Many Parameters | 1 | medium |

**Total findings**: 37

## Findings Detail

- **[LOW] Print Debugging** — `main` (`analyze.py:14`) — debug print statement left in production code
- **[MEDIUM] Deep Nesting** — `generate_api_docs` (`analyzer/docs.py:8`) — nesting depth = 5
- **[HIGH] High Cyclomatic Complexity** — `_example` (`analyzer/docs.py:109`) — cyclomatic complexity = 11
- **[HIGH] High Cyclomatic Complexity** — `nesting_depth` (`analyzer/metrics.py:26`) — cyclomatic complexity = 13
- **[HIGH] High Cyclomatic Complexity** — `strip_comments_and_strings` (`analyzer/metrics.py:69`) — cyclomatic complexity = 13
- **[MEDIUM] Deep Nesting** — `strip_comments_and_strings` (`analyzer/metrics.py:69`) — nesting depth = 5
- **[LOW] TODO/FIXME Left In Code** — `find_todos` (`analyzer/metrics.py:148`) — TODO|FIXME|HACK|XXX|BUG)\b[^\n]*", source, re.IGNORECASE
- **[MEDIUM] Long Function** — `_parse_python` (`analyzer/parsers.py:70`) — 86 lines of code
- **[HIGH] High Cyclomatic Complexity** — `_parse_python` (`analyzer/parsers.py:70`) — cyclomatic complexity = 14
- **[HIGH] High Cyclomatic Complexity** — `_py_params` (`analyzer/parsers.py:187`) — cyclomatic complexity = 14
- **[MEDIUM] Deep Nesting** — `_py_params` (`analyzer/parsers.py:187`) — nesting depth = 5
- **[MEDIUM] Long Function** — `_parse_java` (`analyzer/parsers.py:257`) — 79 lines of code
- **[HIGH] High Cyclomatic Complexity** — `_parse_java` (`analyzer/parsers.py:257`) — cyclomatic complexity = 13
- **[MEDIUM] Long Function** — `_parse_typescript` (`analyzer/parsers.py:359`) — 95 lines of code
- **[HIGH] High Cyclomatic Complexity** — `_parse_typescript` (`analyzer/parsers.py:359`) — cyclomatic complexity = 19
- **[HIGH] Possible Code Duplication** — `owning_class` (`analyzer/parsers.py:380`) — Body identical to owning_class (code-analyzer/analyzer/parsers.py:280) [hash d76272db35ea343b]
- **[MEDIUM] Long Function** — `_parse_cpp` (`analyzer/parsers.py:470`) — 77 lines of code
- **[HIGH] High Cyclomatic Complexity** — `_parse_cpp` (`analyzer/parsers.py:470`) — cyclomatic complexity = 15
- **[LOW] Very Long Line** — `_parse_cpp` (`analyzer/parsers.py:470`) — longest line = 134 chars
- **[HIGH] Possible Code Duplication** — `owning_class` (`analyzer/parsers.py:484`) — Body identical to owning_class (code-analyzer/analyzer/parsers.py:280) [hash d76272db35ea343b]
- **[HIGH] High Cyclomatic Complexity** — `_java_ts_params` (`analyzer/parsers.py:568`) — cyclomatic complexity = 13
- **[MEDIUM] Too Many Parameters** — `_build_function` (`analyzer/parsers.py:614`) — 15 parameters
- **[HIGH] High Cyclomatic Complexity** — `_braces_end` (`analyzer/parsers.py:657`) — cyclomatic complexity = 12
- **[LOW] TODO/FIXME Left In Code** — `Refactoring.recipe_title` (`analyzer/refactoring.py:48`) — todo": "Resolve Outstanding TODOs",
- **[LOW] Very Long Line** — `Refactoring._long_function` (`analyzer/refactoring.py:91`) — longest line = 127 chars
- **[LOW] Magic Numbers** — `Refactoring._long_function` (`analyzer/refactoring.py:91`) — unexplained literals: 1500
- **[LOW] Very Long Line** — `Refactoring._high_complexity` (`analyzer/refactoring.py:193`) — longest line = 146 chars
- **[LOW] Magic Numbers** — `Refactoring._duplicate` (`analyzer/refactoring.py:216`) — unexplained literals: 800
- **[LOW] Very Long Line** — `Refactoring._long_line` (`analyzer/refactoring.py:285`) — longest line = 167 chars
- **[LOW] TODO/FIXME Left In Code** — `Refactoring._print_debug` (`analyzer/refactoring.py:297`) — bug(f: SmellFinding, fn: Function) -> Refactoring:; bug prints leak into production output and lack severity/levels.",
- **[LOW] TODO/FIXME Left In Code** — `Refactoring._todo` (`analyzer/refactoring.py:309`) — todo(f: SmellFinding, fn: Function) -> Refactoring:; TODO/FIXME markers indicate unfinished work or known debt.",
- **[LOW] Very Long Line** — `_refactoring_doc` (`analyzer/report.py:79`) — longest line = 143 chars
- **[LOW] Print Debugging** — `_summary_line` (`analyzer/report.py:98`) — debug print statement left in production code
- **[HIGH] High Cyclomatic Complexity** — `SmellFinding._function_smells` (`analyzer/smells.py:60`) — cyclomatic complexity = 12
- **[LOW] TODO/FIXME Left In Code** — `SmellFinding._function_smells` (`analyzer/smells.py:60`) — bug print statement left in production code", "low"); todo", "; ".join(t[:80] for t in fn.todos[:3]), "low")
- **[LOW] TODO/FIXME Left In Code** — `TestSmells.test_smells_detected` (`tests/test_analyzer.py:153`) — todo", ids)
- **[LOW] Magic Numbers** — `TestEndToEnd.test_full_run_generates_docs` (`tests/test_analyzer.py:214`) — unexplained literals: 100

## Complexity Hotspots

| Function | File | CX | LOC | Nesting |
|---|---|---|---|---|
| `_parse_typescript` | `analyzer/parsers.py` | 19 | 95 | 4 |
| `_parse_python` | `analyzer/parsers.py` | 14 | 86 | 4 |
| `_parse_cpp` | `analyzer/parsers.py` | 15 | 77 | 4 |
| `_parse_java` | `analyzer/parsers.py` | 13 | 79 | 4 |
| `_py_params` | `analyzer/parsers.py` | 14 | 52 | 5 |
| `nesting_depth` | `analyzer/metrics.py` | 13 | 43 | 4 |
| `strip_comments_and_strings` | `analyzer/metrics.py` | 13 | 42 | 5 |
| `_java_ts_params` | `analyzer/parsers.py` | 13 | 46 | 3 |
| `SmellFinding._function_smells` | `analyzer/smells.py` | 12 | 48 | 2 |
| `_braces_end` | `analyzer/parsers.py` | 12 | 31 | 4 |
