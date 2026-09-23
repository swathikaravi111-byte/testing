"""Regex-based parsers for Java, Python, TypeScript and C++ source files."""

import re
from typing import Optional

from .metrics import (
    count_lines,
    count_try_catch,
    cyclomatic_complexity,
    extract_raises,
    find_todos,
    nesting_depth,
)
from .models import ClassInfo, FileAnalysis, Function, Import, Parameter

LANGUAGES = {
    "java": ".java",
    "python": ".py",
    "typescript": (".ts", ".tsx"),
    "cpp": (".cpp", ".cc", ".cxx", ".hpp", ".h", ".hh"),
}


def detect_language(path: str) -> Optional[str]:
    lower = path.lower()
    for lang, exts in LANGUAGES.items():
        if isinstance(exts, str):
            exts = (exts,)
        if any(lower.endswith(e) for e in exts):
            if lang == "cpp" and lower.endswith(".h") and _looks_like_c_header(lower):
                return "cpp"
            return lang
    return None


def _looks_like_c_header(path: str) -> bool:
    return True  # .h treated as C++ headers by default


def _match_n(text: str, pattern: str) -> str:
    m = re.search(pattern, text)
    return m.group(1).strip() if m else ""


def analyze_file(path: str, source: str) -> FileAnalysis:
    lang = detect_language(path)
    if lang is None:
        raise ValueError(f"Unsupported file type: {path}")
    if lang == "python":
        return _parse_python(path, source)
    if lang == "java":
        return _parse_java(path, source)
    if lang == "typescript":
        return _parse_typescript(path, source)
    return _parse_cpp(path, source)


# ---------------------------------------------------------------- Python ----

PY_FUNC = re.compile(
    r"^[ \t]*def\s+(?P<name>\w+)\s*\((?P<params>[^)]*)\)"
    r"(?:\s*->\s*(?P<ret>[^\n:]+))?\s*:\s*(?P<rest>.*)$",
    re.MULTILINE,
)
PY_CLASS = re.compile(r"^[ \t]*class\s+(?P<name>\w+)\s*(\((?P<bases>[^)]*)\))?\s*:", re.MULTILINE)
PY_DEF_LINE = re.compile(r"^\s*(async\s+)?def\s+\w+")
PY_DECORATOR = re.compile(r"^\s*@([\w.]+)")


def _parse_python(path: str, source: str) -> FileAnalysis:
    total, blank, comment, code = count_lines(source)
    lines = source.splitlines()

    # classes
    classes: list[ClassInfo] = []
    class_matches = list(PY_CLASS.finditer(source))
    for idx, m in enumerate(class_matches):
        line_no = source[: m.start()].count("\n") + 1
        end_line = (
            source[: class_matches[idx + 1].start()].count("\n") + 1
            if idx + 1 < len(class_matches)
            else total
        )
        bases = [b.strip() for b in (m.group("bases") or "").split(",") if b.strip()]
        classes.append(
            ClassInfo(name=m.group("name"), file=path, line=line_no, extends=bases)
        )
    class_at_line = [(c.line, c.name) for c in classes]

    def owning_class(line_no: int) -> Optional[str]:
        owner = None
        for start, name in class_at_line:
            if line_no >= start:
                owner = name
            else:
                break
        return owner

    functions: list[Function] = []
    for m in PY_FUNC.finditer(source):
        line_no = source[: m.start()].count("\n") + 1
        # find end: next def/class at same or lower indent
        def_line = lines[line_no - 1]
        indent = len(def_line) - len(def_line.lstrip())
        end_line = _python_block_end(lines, line_no - 1, indent)
        body = "\n".join(lines[line_no - 1 : end_line])
        params = _py_params(m.group("params"))
        cls = owning_class(line_no)
        is_static = "staticmethod" in _decorators_before(lines, line_no - 1)
        is_abstract = "abstractmethod" in _decorators_before(lines, line_no - 1)
        doc = _py_docstring(body)
        functions.append(
            _build_function(
                name=m.group("name"),
                file=path,
                line=line_no,
                end_line=end_line,
                params=params,
                return_type=(m.group("ret") or "").strip() or None,
                class_name=cls,
                is_static=is_static,
                is_abstract=is_abstract,
                is_constructor=bool(cls and m.group("name") == "__init__"),
                docstring=doc,
                source=body,
                language="python",
            )
        )

    imports = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"^\s*from\s+([\w.]+)\s+import\s+(.+)$", line)
        if m:
            syms = [s.strip() for s in m.group(2).split(",")]
            imports.append(Import(module=m.group(1), file=path, line=i, symbols=syms, kind="from"))
            continue
        m = re.match(r"^\s*import\s+([\w., ]+)$", line)
        if m:
            for mod in m.group(1).split(","):
                imports.append(Import(module=mod.strip(), file=path, line=i, kind="import"))

    return FileAnalysis(
        path=path,
        language="python",
        lines=total,
        blank_lines=blank,
        comment_lines=comment,
        code_lines=code,
        functions=functions,
        classes=classes,
        imports=imports,
        todos=find_todos(source),
    )


def _python_block_end(lines: list[str], start: int, indent: int) -> int:
    end = start + 1
    for j in range(start + 1, len(lines)):
        line = lines[j]
        if not line.strip():
            continue
        cur_indent = len(line) - len(line.lstrip())
        if cur_indent <= indent and not line.lstrip().startswith((")", "]")):
            end = j
            break
        end = j + 1
    return end


def _decorators_before(lines: list[str], idx: int) -> str:
    out = []
    j = idx - 1
    while j >= 0:
        if PY_DECORATOR.match(lines[j]):
            out.append(lines[j])
            j -= 1
        else:
            break
    return "\n".join(out)


def _py_docstring(body: str) -> Optional[str]:
    m = re.search(r'^\s*("""|\'\'\')(.*?)\1', body, re.DOTALL | re.MULTILINE)
    return m.group(2).strip() if m else None


def _py_params(raw: str) -> list[Parameter]:
    params: list[Parameter] = []
    depth = 0
    current = ""
    parts: list[str] = []
    for ch in raw:
        if ch in "([{":
            depth += 1
        elif ch in ")]}":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current)

    for part in parts:
        part = part.strip()
        if not part or part == "self" or part == "cls":
            continue
        is_variadic = part.startswith("*")
        part = part.lstrip("*")
        default = None
        if "=" in part and ":" not in part.split("=")[0]:
            name, default = part.split("=", 1)
        elif ":" in part:
            name = part.split(":", 1)[0]
            if "=" in part:
                rest = part.split(":", 1)[1]
                if "=" in rest:
                    name, default = part.split("=", 1)[0], part.split("=", 1)[1]
        else:
            name = part
        name = name.strip()
        ptype = None
        m = re.match(r"(\w+)\s*:\s*([^=]+)", part.lstrip("*"))
        if m:
            ptype = m.group(2).strip()
            name = m.group(1)
        params.append(
            Parameter(
                name=name,
                type=ptype,
                default=default.strip() if isinstance(default, str) and default.strip() else default,
                is_variadic=is_variadic,
            )
        )
    return params


# ------------------------------------------------------------------ Java ----

JAVA_METHOD = re.compile(
    r"(?P<mods>(?:(?:public|protected|private|static|final|abstract|synchronized|native|default)\s+)+)"
    r"(?P<ret>[\w<>\[\],.\s?]+?)\s+"
    r"(?P<name>\w+)\s*\((?P<params>[^;)]*)\)\s*"
    r"(?:throws\s+[\w,\s.]+)?\s*(?P<body>\{|;)"
)
JAVA_CLASS = re.compile(
    r"(?P<kind>class|interface|enum|record)\s+(?P<name>\w+)"
    r"(?:\s*<[^>]+>)?"
    r"(?:\s+extends\s+([\w.<>\s,]+?))?"
    r"(?:\s+implements\s+([\w.<>\s,]+?))?\s*\{"
)
JAVA_IMPORT = re.compile(r"^\s*import\s+(?:static\s+)?([\w.*]+);", re.MULTILINE)
JAVA_PACKAGE = re.compile(r"^\s*package\s+([\w.]+);", re.MULTILINE)


def _parse_java(path: str, source: str) -> FileAnalysis:
    total, blank, comment, code = count_lines(source)
    lines = source.splitlines()

    classes: list[ClassInfo] = []
    for m in JAVA_CLASS.finditer(source):
        line_no = source[: m.start()].count("\n") + 1
        extends = [m.group(3).strip()] if m.group(3) else []
        implements = [i.strip() for i in (m.group(4) or "").split(",") if i.strip()]
        classes.append(
            ClassInfo(
                name=m.group("name"),
                file=path,
                line=line_no,
                kind=m.group("kind"),
                extends=extends,
                implements=implements,
                docstring=_block_comment_before(source, m.start()),
            )
        )

    class_spans = [(m.start(), m.group("name")) for m in JAVA_CLASS.finditer(source)]

    def owning_class(pos: int) -> Optional[str]:
        owner = None
        for start, name in class_spans:
            if pos > start:
                owner = name
            else:
                break
        return owner

    functions = []
    for m in JAVA_METHOD.finditer(source):
        if m.group("body") == ";":  # interface/abstract declaration
            continue
        line_no = source[: m.start()].count("\n") + 1
        mods = m.group("mods").split()
        end_line = _braces_end(source, m.end("body") - 1)
        body = source[m.start() : _offset_of_line_end(source, end_line)]
        params = _java_ts_params(m.group("params"))
        cls = owning_class(m.start())
        functions.append(
            _build_function(
                name=m.group("name"),
                file=path,
                line=line_no,
                end_line=end_line,
                params=params,
                return_type=m.group("ret").strip(),
                class_name=cls,
                visibility=next((v for v in ("public", "protected", "private") if v in mods), "package"),
                is_static="static" in mods,
                is_abstract="abstract" in mods,
                is_constructor=m.group("name") == cls,
                docstring=_block_comment_before(source, m.start()),
                source=body,
                language="java",
            )
        )

    imports = [
        Import(module=m.group(1), file=path, line=source[: m.start()].count("\n") + 1)
        for m in JAVA_IMPORT.finditer(source)
    ]
    return FileAnalysis(
        path=path,
        language="java",
        lines=total,
        blank_lines=blank,
        comment_lines=comment,
        code_lines=code,
        functions=functions,
        classes=classes,
        imports=imports,
        todos=find_todos(source),
    )


# ------------------------------------------------------------ TypeScript ----

TS_METHOD = re.compile(
    r"(?P<mods>(?:(?:public|private|protected|static|abstract|async|readonly|export)\s+)*)"
    r"(?P<name>\w+)\s*\((?P<params>[^;)]*)\)"
    r"(?:\s*:\s*(?P<ret>[\w<>\[\],.\s|?&]+?))?\s*\{"
)
TS_FUNC = re.compile(
    r"(?P<export>export\s+)?(?P<async>async\s+)?function\s+(?P<name>\w+)\s*"
    r"\((?P<params>[^;)]*)\)"
    r"(?:\s*:\s*(?P<ret>[\w<>\[\],.\s|?&]+?))?\s*\{"
)
TS_CLASS = re.compile(
    r"(?P<export>export\s+)?(?P<abstract>abstract\s+)?"
    r"(?P<kind>class|interface)\s+(?P<name>\w+)"
    r"(?:\s+extends\s+([\w.]+))?(?:\s+implements\s+([\w.,\s]+?))?\s*\{"
)
TS_IMPORT = re.compile(
    r"^\s*import\s+(?:type\s+)?(?:\{([^}]+)\}|(\w+)|\*\s+as\s+(\w+))?\s*(?:from)?\s*[\"']([^\"']+)[\"']",
    re.MULTILINE,
)


def _parse_typescript(path: str, source: str) -> FileAnalysis:
    total, blank, comment, code = count_lines(source)
    functions: list[Function] = []
    classes: list[ClassInfo] = []

    for m in TS_CLASS.finditer(source):
        line_no = source[: m.start()].count("\n") + 1
        classes.append(
            ClassInfo(
                name=m.group("name"),
                file=path,
                line=line_no,
                kind=m.group("kind"),
                extends=[m.group(5)] if m.group(5) else [],
                implements=[i.strip() for i in (m.group(6) or "").split(",") if i.strip()],
                docstring=_block_comment_before(source, m.start()),
            )
        )

    class_spans = [(m.start(), m.group("name")) for m in TS_CLASS.finditer(source)]

    def owning_class(pos: int) -> Optional[str]:
        owner = None
        for start, name in class_spans:
            if pos > start:
                owner = name
            else:
                break
        return owner

    for m in TS_FUNC.finditer(source):
        line_no = source[: m.start()].count("\n") + 1
        end_line = _braces_end(source, m.end() - 1)
        functions.append(
            _build_function(
                name=m.group("name"),
                file=path,
                line=line_no,
                end_line=end_line,
                params=_java_ts_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                docstring=_block_comment_before(source, m.start()),
                source=source[m.start() : _offset_of_line_end(source, end_line)],
                language="typescript",
                visibility="export" if m.group("export") else "module",
            )
        )

    for m in TS_METHOD.finditer(source):
        line_no = source[: m.start()].count("\n") + 1
        if line_no in (f.line for f in functions):  # already matched as function
            continue
        mods = m.group("mods").split()
        cls = owning_class(m.start())
        if not cls:
            continue
        end_line = _braces_end(source, m.end() - 1)
        functions.append(
            _build_function(
                name=m.group("name"),
                file=path,
                line=line_no,
                end_line=end_line,
                params=_java_ts_params(m.group("params")),
                return_type=(m.group("ret") or "").strip() or None,
                class_name=cls,
                visibility=next((v for v in ("public", "protected", "private") if v in mods), "public"),
                is_static="static" in mods,
                is_abstract="abstract" in mods,
                docstring=_block_comment_before(source, m.start()),
                source=source[m.start() : _offset_of_line_end(source, end_line)],
                language="typescript",
            )
        )

    imports = []
    for m in TS_IMPORT.finditer(source):
        syms = [s.strip() for s in (m.group(1) or m.group(2) or m.group(3) or "").split(",") if s.strip()]
        imports.append(
            Import(module=m.group(4), file=path, line=source[: m.start()].count("\n") + 1, symbols=syms)
        )
    return FileAnalysis(
        path=path,
        language="typescript",
        lines=total,
        blank_lines=blank,
        comment_lines=comment,
        code_lines=code,
        functions=functions,
        classes=classes,
        imports=imports,
        todos=find_todos(source),
    )


# ------------------------------------------------------------------- C++ ----

CPP_FUNC = re.compile(
    r"(?:(?P<mods>inline|static|virtual|explicit)\s+)*"
    r"(?P<ret>[\w:<>\[\],*&\s]+?)\s+"
    r"(?P<name>[\w:~]+)\s*\((?P<params>[^;{)]*)\)\s*"
    r"(?:const|noexcept|override|final)?\s*(?P<body>\{|;)"
)
CPP_CLASS = re.compile(
    r"(?P<kind>class|struct)\s+(?P<name>\w+)"
    r"(?::\s*(?:public|protected|private)?\s*([\w:,<>\s]+))?\s*\{"
)
CPP_INCLUDE = re.compile(r'^\s*#include\s*[<"]([^>"]+)[>"]', re.MULTILINE)
CPP_CONTROL = re.compile(r"^\s*(if|for|while|switch|else)\b")


def _parse_cpp(path: str, source: str) -> FileAnalysis:
    total, blank, comment, code = count_lines(source)
    functions: list[Function] = []
    classes: list[ClassInfo] = []

    class_spans = []
    for m in CPP_CLASS.finditer(source):
        line_no = source[: m.start()].count("\n") + 1
        bases = []
        if m.group(3):
            bases = [b.split()[-1] for b in m.group(3).split(",") if b.strip()]
        classes.append(ClassInfo(name=m.group("name"), file=path, line=line_no, kind=m.group("kind"), extends=bases))
        class_spans.append((m.start(), m.group("name")))

    def owning_class(pos: int) -> Optional[str]:
        owner = None
        for start, name in class_spans:
            if pos > start:
                owner = name
            else:
                break
        return owner

    keywords_with_body = ("if", "for", "while", "switch", "catch", "return", "else", "do")
    cpp_noise = ("public", "private", "protected", "class", "struct", "template",
                 "using", "namespace", "enum", "virtual", "explicit", "inline", "static", "throw", "new", "delete", "const", "return")
    for m in CPP_FUNC.finditer(source):
        name = m.group("name")
        ret = m.group("ret").strip()
        # strip a leading access-specifier the regex may have swallowed
        ret = re.sub(r"^(public|private|protected)\s*:?\s*", "", ret).strip()
        if name in keywords_with_body or "::" in ret or ":" in ret:
            continue
        if name in cpp_noise or any(w in ret.split() for w in cpp_noise):
            continue
        if not ret:
            continue
        if m.group("body") == ";":
            continue
        line_no = source[: m.start()].count("\n") + 1
        cls = owning_class(m.start())
        end_line = _braces_end(source, m.end() - 1)
        params = _cpp_params(m.group("params"))
        functions.append(
            _build_function(
                name=name.split("::")[-1],
                file=path,
                line=line_no,
                end_line=end_line,
                params=params,
                return_type=ret,
                class_name=cls if "::" not in name else name.split("::")[0],
                visibility="public",
                docstring=_block_comment_before(source, m.start()),
                source=source[m.start() : _offset_of_line_end(source, end_line)],
                language="cpp",
            )
        )

    imports = [
        Import(module=m.group(1), file=path, line=source[: m.start()].count("\n") + 1, kind="include")
        for m in CPP_INCLUDE.finditer(source)
    ]
    return FileAnalysis(
        path=path,
        language="cpp",
        lines=total,
        blank_lines=blank,
        comment_lines=comment,
        code_lines=code,
        functions=functions,
        classes=classes,
        imports=imports,
        todos=find_todos(source),
    )


def _cpp_params(raw: str) -> list[Parameter]:
    if not raw.strip() or raw.strip() == "void":
        return []
    params = []
    for part in raw.split(","):
        part = " ".join(part.split())
        if not part:
            continue
        m = re.match(r"(.+?)(\w+)$", part)
        if m and m.group(1).strip():
            params.append(
                Parameter(
                    name=m.group(2),
                    type=m.group(1).strip().rstrip("&").rstrip("*").strip(),
                )
            )
        else:
            params.append(Parameter(type=part))
    return params


def _java_ts_params(raw: str) -> list[Parameter]:
    params = []
    depth = 0
    current = ""
    parts = []
    for ch in raw:
        if ch in "([{<":
            depth += 1
        elif ch in ")]}>":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append(current)
            current = ""
        else:
            current += ch
    if current.strip():
        parts.append(current)
    for part in parts:
        part = part.strip()
        if not part:
            continue
        is_variadic = "..." in part or "*" in part.split(":")[0] or "..." in part.split(":")[0]
        clean = part.replace("...", "")
        if ":" in clean:
            name, ptype = clean.split(":", 1)
        elif part.strip().startswith("final "):
            name = part.strip().split()[-1]
            ptype = " ".join(part.strip().split()[1:-1]) or None
        else:
            pieces = part.split()
            name = pieces[-1].lstrip("*")
            ptype = " ".join(pieces[:-1]) or None
        default = None
        if "=" in name:
            name, default = name.split("=", 1)
        params.append(
            Parameter(
                name=name.strip(),
                type=ptype.strip() if ptype else None,
                default=default.strip() if default else None,
                is_variadic=is_variadic,
            )
        )
    return params


def _build_function(
    *,
    name: str,
    file: str,
    line: int,
    end_line: int,
    params: list[Parameter],
    return_type,
    language: str,
    source: str,
    class_name=None,
    visibility="public",
    is_static=False,
    is_abstract=False,
    is_constructor=False,
    docstring=None,
) -> Function:
    fn = Function(
        name=name,
        file=file,
        line=line,
        end_line=end_line,
        parameters=params,
        return_type=return_type,
        class_name=class_name,
        visibility=visibility,
        is_static=is_static,
        is_abstract=is_abstract,
        is_constructor=is_constructor,
        docstring=docstring,
        source=source,
    )
    fn.parameter_count = len(params)
    fn.lines_of_code = max(end_line - line + 1, 1)
    fn.cyclomatic_complexity = cyclomatic_complexity(source, language)
    fn.nesting_depth = nesting_depth(source, language)
    fn.max_line_length = max((len(l) for l in source.splitlines()), default=0)
    fn.has_try_catch = count_try_catch(source)
    fn.raises = extract_raises(source, language)
    fn.todos = find_todos(source)
    return fn


def _braces_end(source: str, open_pos: int) -> int:
    depth = 0
    i = open_pos
    n = len(source)
    while i < n:
        ch = source[i]
        if ch in "'\"":
            quote = ch
            i += 1
            while i < n and source[i] != quote:
                i += 2 if source[i] == "\\" else 1
            i += 1
            continue
        if source.startswith("//", i):
            j = source.find("\n", i)
            i = n if j == -1 else j
            continue
        if source.startswith("/*", i):
            j = source.find("*/", i)
            i = n if j == -1 else j + 2
            continue
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return source[: i + 1].count("\n")
        i += 1
    return source.count("\n")


def _offset_of_line_end(source: str, line_no: int) -> int:
    pos = 0
    for _ in range(line_no):
        nl = source.find("\n", pos)
        pos = nl + 1 if nl != -1 else len(source)
    return pos


def _block_comment_before(source: str, pos: int) -> Optional[str]:
    before = source[:pos].rstrip()
    if before.endswith("*/"):
        start = before.rfind("/**")
        if start != -1:
            return re.sub(r"^\s*\*?\s*|^\s*/\*+\s?", "", before[start:], flags=re.M).split("*/")[0].strip()
    return None
