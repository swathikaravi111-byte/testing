"""Architecture diagram generator producing Mermaid + markdown."""

import os
from collections import defaultdict

from .models import ProjectAnalysis


def generate_architecture_doc(project: ProjectAnalysis) -> str:
    out = ["# Architecture Overview", ""]
    out.extend(_stats(project))
    out.append("## Module Dependency Graph")
    out.append("")
    out.extend(_dep_graph(project))
    out.append("## Class Hierarchy")
    out.append("")
    out.extend(_class_diagram(project))
    out.append("## Internal Call Structure (per module)")
    out.append("")
    out.extend(_module_structure(project))
    return "\n".join(out) + "\n"


def _stats(project) -> list[str]:
    stats = project.language_stats()
    rows = ["| Language | Files | LOC | Functions | Classes |", "|---|---|---|---|---|"]
    for lang, s in sorted(stats.items()):
        rows.append(f"| {lang.title()} | {s['files']} | {s['loc']} | {s['functions']} | {s['classes']} |")
    return [
        "## Project Statistics",
        "",
        *rows,
        "",
        f"**Total analyzed LOC**: {project.total_loc} · "
        f"**Functions**: {len(project.all_functions)} · "
        f"**Classes**: {len(project.all_classes)} · "
        f"**Parse errors**: {project.file_errors}",
        "",
    ]


def _module_name(path) -> str:
    return os.path.splitext(os.path.basename(path))[0]


def _dep_graph(project) -> list[str]:
    """Mermaid graph of file-to-file dependencies based on imports."""
    edges = set()
    nodes = set()
    file_modules = {fa.path: _module_name(fa.path) for fa in project.files}

    for imp in project.all_imports:
        source_mod = file_modules.get(imp.file)
        if not source_mod:
            continue
        nodes.add(source_mod)
        # local import resolution: matches a module/file name in the project
        target = _resolve_local(imp, project)
        if target and target != source_mod:
            nodes.add(target)
            edges.add((source_mod, target))

    lines = ["```mermaid", "graph LR"]
    for src, dst in sorted(edges):
        lines.append(f"    {src} --> {dst}")
    if not edges:
        lines.append("    NoInterModuleDeps[No cross-module imports detected]")
    lines += ["```", ""]
    return lines


def _resolve_local(imp, project):
    stem = imp.module.replace("/", ".").split(".")[-1]
    for fa in project.files:
        if _module_name(fa.path) == stem or os.path.basename(fa.path) == f"{stem}.py":
            return _module_name(fa.path)
        for base in (stem, os.path.basename(fa.path)):
            if base and base.split(".")[0] == stem:
                return _module_name(fa.path)
    # TS/Java relative imports like './services/user'
    if imp.kind in ("import", "from") and ("/" in imp.module or imp.module.startswith(".")):
        clean = imp.module.strip("./").split("/")[-1]
        for fa in project.files:
            if _module_name(fa.path) == clean:
                return clean
    return None


def _class_diagram(project) -> list[str]:
    lines = ["```mermaid", "classDiagram"]
    for cls in project.all_classes:
        lines.append(f"    class {cls.name} {{")
        for m in cls.methods:
            lines.append(f"        {m.name}()")
        lines.append("    }")
    # inheritance edges
    names = {c.name for c in project.all_classes}
    for cls in project.all_classes:
        for base in cls.extends + cls.implements:
            if base in names:
                lines.append(f"    {base} <|-- {cls.name}")
    lines += ["```", ""]
    return lines


def _module_structure(project) -> list[str]:
    out = []
    for fa in sorted(project.files, key=lambda x: x.path):
        if not fa.functions:
            continue
        rel = os.path.relpath(fa.path, project.root)
        out.append(f"**`{rel}`** ({fa.language}, {fa.code_lines} LOC)")
        out.append("")
        out.append("```")
        out.append(f"imports: {', '.join(i.module for i in fa.imports) or 'none'}")
        for cls in fa.classes:
            out.append(f"{cls.kind} {cls.name}" + (f" : {', '.join(cls.extends)}" if cls.extends else ""))
        for fn in fa.functions:
            out.append(f"  {fn.signature()}  [L{fn.line}, cx={fn.cyclomatic_complexity}]")
        out.append("```")
        out.append("")
    return out
