"""Top-level orchestrator: scan -> analyze -> write all reports."""

import os
from datetime import datetime, timezone

from . import smells as smells_mod
from .architecture import generate_architecture_doc
from .docs import generate_api_docs
from .models import ProjectAnalysis
from .refactoring import suggest
from .scanner import scan
from .smells import detect_smells, smell_summary


def analyze_project(root: str) -> ProjectAnalysis:
    return scan(root)


def generate_quality_report(project: ProjectAnalysis, findings) -> str:
    summary = smell_summary(findings)
    hotspots = sorted(
        project.all_functions,
        key=lambda f: f.cyclomatic_complexity + f.lines_of_code // 10,
        reverse=True,
    )[:10]

    out = ["# Code Quality Report", "", f"_Generated {datetime.now(timezone.utc).isoformat(timespec='seconds')}_", ""]

    out += ["## Smell Summary", "", "| Smell | Occurrences | Severity |", "|---|---|---|"]
    if summary:
        for sid, info in summary.items():
            out.append(f"| {info['title']} | {info['count']} | {info['severity']} |")
    else:
        out.append("| No code smells detected | — | — |")
    out += ["", f"**Total findings**: {len(findings)}", ""]

    out += ["## Findings Detail", ""]
    for f in findings:
        out.append(
            f"- **[{f.severity.upper()}] {f.title}** — `{f.function}` "
            f"(`{os.path.relpath(f.file, project.root)}:{f.line}`) — {f.details}"
        )
    out += ["", "## Complexity Hotspots", "", "| Function | File | CX | LOC | Nesting |", "|---|---|---|---|---|"]
    for fn in hotspots:
        out.append(
            f"| `{fn.qualified_name}` | `{os.path.relpath(fn.file, project.root)}` | "
            f"{fn.cyclomatic_complexity} | {fn.lines_of_code} | {fn.nesting_depth} |"
        )
    return "\n".join(out) + "\n"


def run(root: str, out_dir: str = "docs/generated") -> dict:
    project = analyze_project(root)
    findings = detect_smells(project)
    refactorings = suggest(project, findings)

    os.makedirs(out_dir, exist_ok=True)
    outputs = {}
    for name, content in [
        ("API_REFERENCE.md", generate_api_docs(project)),
        ("ARCHITECTURE.md", generate_architecture_doc(project)),
        ("QUALITY_REPORT.md", generate_quality_report(project, findings)),
        ("REFACTORING.md", _refactoring_doc(refactorings)),
    ]:
        path = os.path.join(out_dir, name)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(content)
        outputs[name] = path

    _summary_line(project, findings, refactorings, outputs)
    return {
        "project": project,
        "findings": findings,
        "refactorings": refactorings,
        "outputs": outputs,
    }


def _refactoring_doc(refactorings) -> str:
    out = ["# Refactoring Suggestions", "", f"{len(refactorings)} suggestions.", ""]
    for i, r in enumerate(refactorings, 1):
        out += [
            f"## {i}. {r.title}",
            "",
            f"- **Location**: `{r.location}`",
            f"- **Why**: {r.rationale}",
            "",
        ]
        if r.before:
            out += ["**Before**", "", "```python" if "def " in r.before or "#" in r.before else "```java", r.before, "```", ""]
        if r.after:
            out += ["**After**", "", "```python" if r.after.strip().startswith(("def", "#", "@", "class ")) else "```java", r.after, "```", ""]
        out.append("---")
        out.append("")
    return "\n".join(out) + "\n"


def _summary_line(project, findings, refactorings, outputs):
    print(
        f"Analyzed {len(project.files)} files ({project.total_loc} LOC), "
        f"{len(project.all_functions)} functions, "
        f"{len(findings)} smell findings, "
        f"{len(refactorings)} refactorings."
    )
    for name, path in outputs.items():
        print(f"  wrote {name}: {path}")
