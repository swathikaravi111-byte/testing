"""API documentation generator (markdown with examples)."""

import os

from .models import Function, ProjectAnalysis


def generate_api_docs(project: ProjectAnalysis) -> str:
    sections = [
        "# API Reference",
        "",
        f"Auto-generated for `{os.path.basename(project.root)}` — "
        f"{len(project.all_functions)} functions across {len(project.files)} files.",
        "",
    ]

    by_language = {}
    for fa in project.files:
        if fa.functions or fa.classes:
            by_language.setdefault(fa.language, []).append(fa)

    for language in sorted(by_language):
        sections.append(f"## {language.title()}")
        sections.append("")
        for fa in sorted(by_language[language], key=lambda x: x.path):
            rel = _rel(project, fa.path)
            if fa.functions or fa.classes:
                sections.append(f"### `{rel}`")
                sections.append("")
                for cls in fa.classes:
                    sections.extend(_class_doc(cls, project))
                for fn in fa.functions:
                    sections.extend(_function_doc(fn, project, depth=0))
                sections.append("---")
                sections.append("")

    return "\n".join(sections).rstrip() + "\n"


def _class_doc(cls, project) -> list[str]:
    out = [f"#### {' 🔧' if cls.kind == 'class' else ' 📐'} `{cls.kind} {cls.name}`"]
    if cls.docstring:
        out += ["", f"> {cls.docstring.splitlines()[0]}"]
    if cls.extends or cls.implements:
        rels = []
        if cls.extends:
            rels.append(f"extends **{', '.join(cls.extends)}**")
        if cls.implements:
            rels.append(f"implements **{', '.join(cls.implements)}**")
        out += ["", " ".join(rels)]
    out.append("")
    return out


def _function_doc(fn: Function, project, depth: int) -> list[str]:
    lang = fn.file.rsplit(".", 1)[-1]
    anchor = f"{fn.qualified_name}-{fn.line}".replace("::", "-").replace(".", "-")
    out = [f"<a id=\"{anchor}\"></a>", ""]
    out.append(
        f"{'#' * (5 + depth)} "
        f"`{fn.qualified_name}("
        f"{', '.join(p.signature() for p in fn.parameters)})`"
        + (f" → `{fn.return_type}`" if fn.return_type else "")
    )
    out.append("")
    meta = [
        f"`{fn.file}:{fn.line}`",
        f"LOC **{fn.lines_of_code}**",
        f"complexity **{fn.cyclomatic_complexity}**",
        f"nesting **{fn.nesting_depth}**",
    ]
    if fn.class_name:
        meta.insert(0, f"member of `{fn.class_name}`")
    out.append(" · ".join(meta))
    out.append("")

    if fn.docstring:
        out.append("**Description**")
        out.append("")
        out.append(fn.docstring.strip())
        out.append("")

    if fn.parameters:
        out.append("**Parameters**")
        out.append("")
        out.append("| Name | Type | Default |")
        out.append("|------|------|---------|")
        for p in fn.parameters:
            out.append(f"| `{p.name}` | `{p.type or '—'}` | `{p.default or '—'}` |")
        out.append("")

    if fn.return_type:
        out.append(f"**Returns** `{fn.return_type}`")
        out.append("")

    if fn.raises:
        out.append(f"**Raises/Throws**: {', '.join(f'`{r}`' for r in fn.raises)}")
        out.append("")

    out.append("**Example**")
    out.append("")
    out.append(f"```{lang}")
    out.extend(_example(fn, lang))
    out.append("```")
    out.append("")
    return out


def _example(fn: Function, lang_ext: str) -> list[str]:
    py = lang_ext == "py"
    args = ", ".join(p.name for p in fn.parameters)
    call = f"{fn.name}({args})"
    if py:
        ret = " = " if fn.return_type else ""
        lines = [f"# {fn.qualified_name}", f"result{ret}{call}" if fn.return_type else f"{call}"]
        if fn.class_name:
            lines = [f"obj = {fn.class_name}()", f"result = obj.{call}"]
    elif lang_ext in ("ts", "tsx"):
        lines = [f"const result = {call};"]
        if fn.class_name:
            lines = [f"const obj = new {fn.class_name}();", f"const result = obj.{call};"]
    elif lang_ext == "java":
        lines = [f"var result = {fn.name}({args});"]
        if fn.class_name:
            lines = [f"var obj = new {fn.class_name}();", f"var result = obj.{fn.name}({args});"]
    else:  # cpp
        lines = [f"auto result = {fn.name}({args});"]
        if fn.class_name:
            lines = [f"{fn.class_name} obj;", f"auto result = obj.{fn.name}({args});"]
    return lines


def _rel(project, path) -> str:
    return os.path.relpath(path, project.root)
