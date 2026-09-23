"""Code smell and anti-pattern detection rules."""

import re
from dataclasses import dataclass

from .metrics import strip_comments_and_strings
from .models import Function, ProjectAnalysis

THRESHOLDS = {
    "long_function": 60,
    "complex_function": 10,
    "deep_nesting": 4,
    "many_params": 5,
    "long_line": 120,
}

SMELL_INFO = {
    "long-function": ("Long Function", "Function exceeds 60 LOC — split into smaller units."),
    "high-complexity": ("High Cyclomatic Complexity", "Too many decision points; refactor conditionals."),
    "deep-nesting": ("Deep Nesting", "Nesting > 3 levels; use guard clauses / early returns."),
    "too-many-parameters": ("Too Many Parameters", ">= 5 params; introduce a parameter object."),
    "long-line": ("Very Long Line", "Line > 120 chars hurts readability."),
    "duplicate-code": ("Possible Code Duplication", "Identical body hash found in multiple functions."),
    "magic-number": ("Magic Numbers", "Unexplained numeric literals in logic."),
    "empty-catch": ("Empty Catch Block", "Exceptions are silently swallowed."),
    "long-parameter-list-callsite": ("God Function", "Function does too much (size + complexity + params)."),
    "print-debugging": ("Print Debugging", "print/console.log/System.out in non-test code."),
    "todo": ("TODO/FIXME Left In Code", "Unresolved work marker in source."),
}


@dataclass
class SmellFinding:
    smell_id: str
    title: str
    description: str
    file: str
    function: str
    line: int
    severity: str  # high | medium | low
    details: str


def detect_smells(project: ProjectAnalysis) -> list[SmellFinding]:
    findings: list[SmellFinding] = []
    for fn in project.all_functions:
        findings.extend(_function_smells(fn))
    findings.extend(_duplicates(project))
    return sorted(findings, key=lambda f: (f.file, f.line))


def _severity(score: int) -> str:
    if score >= 3:
        return "high"
    if score == 2:
        return "medium"
    return "low"


def _function_smells(fn: Function) -> list[SmellFinding]:
    out: list[SmellFinding] = []
    code = strip_comments_and_strings(fn.source, "py" if fn.file.endswith(".py") else "java")

    def add(smell_id: str, details: str, severity: str | None = None, line: int | None = None):
        title, desc = SMELL_INFO[smell_id]
        fn.smells.append(smell_id)
        out.append(
            SmellFinding(
                smell_id=smell_id,
                title=title,
                description=desc,
                file=fn.file,
                function=fn.qualified_name,
                line=line or fn.line,
                severity=severity or "medium",
                details=details,
            )
        )

    score = 0
    if fn.lines_of_code > THRESHOLDS["long_function"]:
        add("long-function", f"{fn.lines_of_code} lines of code")
        score += 1
    if fn.cyclomatic_complexity > THRESHOLDS["complex_function"]:
        add("high-complexity", f"cyclomatic complexity = {fn.cyclomatic_complexity}", "high")
        score += 2
    if fn.nesting_depth > THRESHOLDS["deep_nesting"]:
        add("deep-nesting", f"nesting depth = {fn.nesting_depth}")
        score += 1
    if fn.parameter_count > THRESHOLDS["many_params"]:
        add("too-many-parameters", f"{fn.parameter_count} parameters")
        score += 1
    if fn.max_line_length > THRESHOLDS["long_line"]:
        add("long-line", f"longest line = {fn.max_line_length} chars", "low")
    if re.search(r"catch\s*\(\s*\w+\s+\w+\s*\)\s*\{\s*\}", code) or re.search(r"except.*:\s*pass", code):
        add("empty-catch", "exception handler body is empty", "high")
        score += 1
    numbers = re.findall(r"(?<![\w.\"\'])(\d{3,})(?![\w.])", code)
    if numbers:
        add("magic-number", f"unexplained literals: {', '.join(sorted(set(numbers))[:5])}", "low")
    if re.search(r"\bprint\(", code) or re.search(r"console\.log\(", code) or re.search(r"System\.out\.print", code):
        add("print-debugging", "debug print statement left in production code", "low")
    if fn.todos:
        add("todo", "; ".join(t[:80] for t in fn.todos[:3]), "low")
    return out


def _duplicates(project: ProjectAnalysis) -> list[SmellFinding]:
    import hashlib

    buckets: dict[str, list[Function]] = {}
    for fn in project.all_functions:
        normalized = _normalize(fn.source)
        if not normalized:
            continue
        h = hashlib.sha256(normalized.encode()).hexdigest()[:16]
        buckets.setdefault(h, []).append(fn)

    findings = []
    for h, group in buckets.items():
        if len(group) > 1:
            first = group[0]
            title, desc = SMELL_INFO["duplicate-code"]
            for other in group[1:]:
                other.smells.append("duplicate-code")
                findings.append(
                    SmellFinding(
                        smell_id="duplicate-code",
                        title=title,
                        description=desc,
                        file=other.file,
                        function=other.qualified_name,
                        line=other.line,
                        severity="high",
                        details=(
                            f"Body identical to {first.qualified_name} ({first.file}:{first.line}) "
                            f"[hash {h}]"
                        ),
                    )
                )
    return findings


def _normalize(source: str) -> str:
    code = strip_comments_and_strings(source)
    lines = [line.strip() for line in code.splitlines() if line.strip()]
    if len(lines) < 5:
        return ""
    # blank out the function name so only-call-differ duplicates compare equal
    lines[0] = re.sub(r"(\bdef\s+|\bfunction\s+)\w+", r"\1NAME", lines[0])
    return "\n".join(lines)


def smell_summary(findings: list[SmellFinding]) -> dict:
    summary = {}
    for f in findings:
        entry = summary.setdefault(f.smell_id, {"count": 0, "severity": f.severity, "title": f.title})
        entry["count"] += 1
        if f.severity == "high":
            entry["severity"] = "high"
    return dict(sorted(summary.items(), key=lambda kv: -kv[1]["count"]))
