"""Language-aware source parsing for Java, Python, TypeScript and C++.

Regex-based structural extraction tuned for common real-world style.
"""
import re
from typing import List, Optional, Tuple

from .models import FunctionInfo, ClassInfo, Parameter, ModuleInfo

JAVA_FILES = (".java",)
PYTHON_FILES = (".py",)
TS_FILES = (".ts", ".tsx")
CPP_FILES = (".cpp", ".cc", ".cxx", ".c", ".h", ".hpp", ".hxx")

LANG_BY_EXT = {}
for exts, lang in ((JAVA_FILES, "java"), (PYTHON_FILES, "python"),
                   (TS_FILES, "typescript"), (CPP_FILES, "cpp")):
    for e in exts:
        LANG_BY_EXT[e] = lang


def detect_language(path: str) -> Optional[str]:
    for ext, lang in LANG_BY_EXT.items():
        if path.endswith(ext):
            return lang
    return None


def strip_comments_and_strings(src: str) -> str:
    """Replace comment and string contents with spaces, preserving layout.

    Keeps line/column numbers intact so extracted line numbers stay valid.
    """
    out = []
    i, n = 0, len(src)
    mode = None  # None | 'line' | 'block' | '"' | "'" | '`'
    while i < n:
        c = src[i]
        nxt = src[i + 1] if i + 1 < n else ""
        if mode is None:
            if c == "/" and nxt == "/":
                mode = "line"; out.append("  "); i += 2; continue
            if c == "/" and nxt == "*":
                mode = "block"; out.append("  "); i += 2; continue
            if c in "\"'`":
                mode = c; out.append(c); i += 1; continue
            out.append(c); i += 1
        elif mode == "line":
            if c == "\n":
                mode = None; out.append(c)
            else:
                out.append(" ")
            i += 1
        elif mode == "block":
            if c == "*" and nxt == "/":
                mode = None; out.append("  "); i += 2; continue
            out.append(c if c == "\n" else " "); i += 1
        else:  # inside a string
            if c == "\\" and i + 1 < n:
                out.append("  "); i += 2; continue
            if c == mode:
                mode = None
            out.append(c if c == mode or c == "\n" else c)
            i += 1
    return "".join(out)


def _indent_of(line: str) -> int:
    return len(line) - len(line.lstrip(" \t"))


def _match_indent_block(lines: List[str], start_idx: int) -> int:
    """Return index of last line of the indented block starting at start_idx."""
    base = _indent_of(lines[start_idx])
    last = start_idx
    for j in range(start_idx + 1, len(lines)):
        if lines[j].strip() == "":
            continue
        if _indent_of(lines[j]) <= base:
            break
        last = j
    return last


def _brace_block(lines: List[str], start_idx: int) -> int:
    """Return index of last line of the braced block starting at/after start_idx."""
    depth = 0
    opened = False
    for j in range(start_idx, len(lines)):
        depth += lines[j].count("{") - lines[j].count("}")
        if "{" in lines[j]:
            opened = True
        if opened and depth == 0:
            return j
    return min(start_idx, len(lines) - 1)


# ---------------------------------------------------------------- Python

_PY_FUNC = re.compile(
    r"^\s*(async\s+def|def)\s+(\w+)\s*\(([^)]*)\)\s*(->\s*[^:]+)?\s*:")
_PY_CLASS = re.compile(r"^\s*class\s+(\w+)(\s*\(([^)]*)\))?\s*:")
_PY_DECORATOR = re.compile(r"^\s*@(\w+)")
_VIS_RE = re.compile(
    r"^\s*(public|private|protected|internal)\b")


def _py_param(raw: str) -> Parameter:
    raw = raw.strip()
    if not raw:
        return Parameter("__unknown__")
    kind = "positional"
    default = None
    if "=" in raw:
        raw, _, default = raw.partition("=")
        raw, default = raw.strip(), default.strip()
        kind = "keyword"
    if raw.startswith("*"):
        kind = "variadic"
        raw = raw.lstrip("*").strip()
    if ":" in raw:
        name, _, ptype = raw.partition(":")
        return Parameter(name.strip(), ptype.strip(), default, kind)
    return Parameter(raw, None, default, kind)


def _py_docstring(body_lines: List[str]) -> Optional[str]:
    if not body_lines:
        return None
    first = body_lines[0].strip()
    if first.startswith(('"""', "'''")):
        quote = first[:3]
        text = [first[3:]]
        if quote in first[3:]:
            return text[0].strip()
        for ln in body_lines[1:]:
            if quote in ln:
                text.append(ln.split(quote)[0])
                return "\n".join(t for t in text).strip()
            text.append(ln.strip())
        return None
    return None


def parse_python(path: str, src: str) -> ModuleInfo:
    clean = strip_comments_and_strings(src)
    lines = clean.split("\n")
    module = ModuleInfo(name=path, file=path, language="python")
    # imports
    for ln in lines:
        m = re.match(r"^\s*(?:from\s+[\w.]+\s+)?import\s+([\w., *]+)", ln)
        if m:
            module.imports.append(m.group(1).strip())
    stack: List[ClassInfo] = []
    for i, ln in enumerate(lines):
        cm = _PY_CLASS.match(ln)
        if cm:
            bases = (cm.group(3) or "").strip()
            cls = ClassInfo(name=cm.group(1), file=path, line=i + 1, language="python")
            if bases:
                parts = [b.strip() for b in bases.split(",") if b.strip()]
                cls.parent = parts[0] if parts else None
                cls.interfaces = [b for b in parts[1:]]
            last = _match_indent_block(lines, i + 1)
            cls.docstring = _py_docstring(lines[i + 1:last + 1])
            module.classes.append(cls)
            stack.append(cls)
            continue
        fm = _PY_FUNC.match(ln)
        if fm:
            f = FunctionInfo(
                name=fm.group(2), file=path, line=i + 1, language="python",
                is_async=fm.group(1).startswith("async"),
                parent_class=stack[-1].name if stack else None,
            )
            for raw in _split_params(fm.group(3)):
                f.params.append(_py_param(raw))
            f.return_type = (fm.group(4) or "").lstrip("-> ").strip() or None
            end = _match_indent_block(lines, i + 1)
            f.end_line = end + 1
            f.body_lines = lines[i + 1:end + 1]
            f.docstring = _py_docstring(f.body_lines)
            f.param_count = len(f.params)
            if stack:
                stack[-1].methods.append(f)
            else:
                module.functions.append(f)
        if ln.strip() and _indent_of(ln) <= (0 if not stack else _indent_of(
                lines[stack[-1].line - 1])) and i and not _PY_CLASS.match(ln):
            # dedent below class header -> pop class scope
            while stack and _PY_CLASS.match(lines[stack[-1].line - 1]) and \
                    _indent_of(ln) <= _indent_of(lines[stack[-1].line - 1]):
                stack.pop()
    return module


def _split_params(raw: str) -> List[str]:
    raw = raw.strip()
    if not raw:
        return []
    parts, depth, cur = [], 0, []
    for ch in raw:
        if ch in "<([":
            depth += 1
        elif ch in ">)]":
            depth -= 1
        if ch == "," and depth == 0:
            parts.append("".join(cur)); cur = []
        else:
            cur.append(ch)
    if cur:
        parts.append("".join(cur))
    return parts


# ---------------------------------------------------------------- Java

_JAVA_METHOD = re.compile(
    r"^\s*(?:(?:public|private|protected|static|final|abstract|synchronized|"
    r"native|default)\s+)+(?:<[^>]+>\s+)?([\w<>\[\],.?\s]+?)\s+(\w+)\s*\(([^)]*)\)\s*(?:throws\s+[\w.,\s]+)?\s*[;{]")
_JAVA_CLASS = re.compile(
    r"^\s*(?:(?:public|private|protected|static|final|abstract)\s+)*"
    r"(?:class|interface|enum)\s+(\w+)(?:\s+extends\s+([\w<>,.\s]+?))?"
    r"(?:\s+implements\s+([\w<>,.\s]+?))?\s*\{")
_JAVA_FIELD = re.compile(
    r"^\s*(?:(?:private|protected|public)\s+)?(?:static\s+)?(?:final\s+)?"
    r"[\w<>\[\],.]+\s+(\w+)\s*(?:=[^;]*)?;")


def parse_java(path: str, src: str) -> ModuleInfo:
    clean = strip_comments_and_strings(src)
    lines = clean.split("\n")
    module = ModuleInfo(name=path, file=path, language="java")
    pkg = re.search(r"^\s*package\s+([\w.]+);", clean, re.M)
    if pkg:
        module.imports.append(pkg.group(1))
    for ln in lines:
        im = re.match(r"^\s*import\s+([\w.*]+);", ln)
        if im:
            module.imports.append(im.group(1))
    current_class: Optional[ClassInfo] = None
    for i, ln in enumerate(lines):
        cm = _JAVA_CLASS.match(ln)
        if cm:
            cls = ClassInfo(
                name=cm.group(1), file=path, line=i + 1, language="java",
                parent=(cm.group(2) or "").strip() or None,
                interfaces=[s.strip() for s in (cm.group(3) or "").split(",")
                            if s.strip()],
                visibility="private" if " private " in f" {ln} " else "public",
            )
            module.classes.append(cls)
            current_class = cls
            continue
        fm = _JAVA_METHOD.match(ln)
        if fm and "{" in ln or (fm and ln.rstrip().endswith(";")):
            ret = fm.group(1).strip()
            name = fm.group(2)
            if ret.split()[-1] == "new" or name in ("if", "while", "for",
                                                    "switch", "catch", "return"):
                continue
            f = FunctionInfo(
                name=name, file=path, line=i + 1, language="java",
                return_type=None if ret == "void" else ret,
                visibility=("private" if " private " in f" {ln} "
                            else "protected" if " protected " in f" {ln} "
                            else "public"),
                is_static=" static " in f" {ln} ",
                is_abstract=" abstract " in f" {ln} " or ln.rstrip().endswith(";"),
                parent_class=current_class.name if current_class else None,
            )
            for raw in _split_params(fm.group(3)):
                raw = raw.strip()
                if not raw:
                    continue
                if " " in raw:
                    ptype, _, pname = raw.rpartition(" ")
                    f.params.append(Parameter(pname.strip(), ptype.strip()))
                else:
                    f.params.append(Parameter(raw, None))
            f.param_count = len(f.params)
            if ln.rstrip().endswith(";"):
                f.end_line = i + 1
            else:
                end = _brace_block(lines, i)
                f.end_line = end + 1
                f.body_lines = lines[i + 1:end + 1]
            if current_class:
                current_class.methods.append(f)
            else:
                module.functions.append(f)
        elif current_class and not ln.strip().startswith(("//", "*")):
            vm = re.match(
                r"^\s*(?:(?:public|private|protected)\s+)?(?:static\s+)?"
                r"[\w<>\[\],.]+\s+(\w+)\s*(?:=\s*[^;]+)?;", ln)
            if vm and "(" not in ln:
                current_class.fields.append(vm.group(1))
    return module


# ---------------------------------------------------------------- TypeScript

_TS_METHOD = re.compile(
    r"^\s*(?:(?:public|private|protected|static|readonly|abstract|async)\s+)*"
    r"(\w+)\s*(?:<[^>]*>)?\s*\(([^)]*)\)\s*(?::\s*[^{=;]+)?\s*[{;=]")
_TS_CLASS = re.compile(
    r"^\s*(?:(?:export\s+)?(?:default\s+)?)?(?:abstract\s+)?"
    r"(?:class|interface)\s+(\w+)(?:\s+extends\s+([\w<>,.\s]+?))?"
    r"(?:\s+implements\s+([\w<>,.\s]+?))?\s*\{")
_TS_FUNC = re.compile(
    r"^\s*(?:export\s+)?(?:default\s+)?(?:async\s+)?function\s+(\w+)"
    r"\s*(?:<[^>]*>)?\s*\(([^)]*)\)\s*(?::\s*[^{=;]+)?\s*[{;]")
_TS_ARROW = re.compile(
    r"^\s*(?:export\s+)?(?:const|let)\s+(\w+)\s*(?::\s*[^=]+)?"
    r"=\s*(?:async\s+)?\(([^)]*)\)\s*(?::\s*[^=]+)?\s*=>")
_TS_FIELD = re.compile(
    r"^\s*(?:(?:public|private|protected)\s+)?(?:static\s+)?(?:readonly\s+)?"
    r"(\w+)\s*(?::\s*[^=;{]+)?\s*(?:=\s*[^;]+)?;")


def _ts_param(raw: str) -> Parameter:
    raw = raw.strip()
    if not raw:
        return Parameter("__unknown__")
    default = None
    kind = "positional"
    if "=" in raw:
        raw, _, default = raw.partition("=")
        raw, default = raw.strip(), default.strip()
        kind = "keyword"
    if raw.startswith("..."):
        kind = "variadic"
        raw = raw[3:].strip()
    if ":" in raw:
        name, _, ptype = raw.partition(":")
        return Parameter(name.strip(), ptype.strip(), default, kind)
    return Parameter(raw, None, default, kind)


def parse_typescript(path: str, src: str) -> ModuleInfo:
    clean = strip_comments_and_strings(src)
    lines = clean.split("\n")
    module = ModuleInfo(name=path, file=path, language="typescript")
    for ln in lines:
        im = re.match(r"^\s*(?:import\s+[\w{},*\s]+\s+from\s+)?['\"](.+)['\"]", ln)
        if im and ("import" in ln or "require" in ln):
            module.imports.append(im.group(1))
        elif re.match(r"^\s*import\s+[\w{}\s,]+\s+from\s+", ln):
            module.imports.append(ln.split("from")[-1].strip().strip("';\" "))
    current_class: Optional[ClassInfo] = None
    for i, ln in enumerate(lines):
        cm = _TS_CLASS.match(ln)
        if cm:
            cls = ClassInfo(
                name=cm.group(1), file=path, line=i + 1, language="typescript",
                parent=(cm.group(2) or "").strip() or None,
                interfaces=[s.strip() for s in (cm.group(3) or "").split(",")
                            if s.strip()],
                visibility="private" if " private " in f" {ln} " else "public",
            )
            module.classes.append(cls)
            current_class = cls
            continue
        made = None
        fm = _TS_FUNC.match(ln)
        if fm:
            made = FunctionInfo(name=fm.group(1), file=path, line=i + 1,
                                language="typescript",
                                is_async=" async " in f" {ln} ",
                                parent_class=None)
            params_raw, ret = fm.group(2), None
            rest = ln[ln.index("(", ln.index(fm.group(1))):]
            rm = re.search(r"\)\s*:\s*([^{=;]+)[{=;]", rest)
            if rm:
                ret = rm.group(1).strip()
            made.return_type = ret
        elif _TS_ARROW.match(ln):
            am = _TS_ARROW.match(ln)
            made = FunctionInfo(name=am.group(1), file=path, line=i + 1,
                                language="typescript",
                                is_async="async" in ln.split("=")[0],
                                parent_class=None)
            params_raw = am.group(2)
            retm = re.search(r"\)\s*:\s*([^=]+)?=", ln)
            made.return_type = retm.group(1).strip() if retm and retm.group(1) else None
        elif current_class and _TS_METHOD.match(ln) and "{" in ln:
            tm = _TS_METHOD.match(ln)
            made = FunctionInfo(
                name=tm.group(1), file=path, line=i + 1, language="typescript",
                is_async=" async " in f" {ln} ",
                visibility=("private" if " private " in f" {ln} "
                            else "protected" if " protected " in f" {ln} "
                            else "public"),
                is_static=" static " in f" {ln} ",
                parent_class=current_class.name)
            params_raw = tm.group(2)
            ret = tm.group(3) if tm.lastindex and tm.lastindex >= 3 else None
            rest = ln[ln.index(tm.group(1)):]
            rm = re.search(r"\)\s*:\s*([^{=;]+)\s*[{;=]", rest)
            made.return_type = rm.group(1).strip() if rm else None
        elif current_class and _TS_FIELD.match(ln) and "(" not in ln:
            current_class.fields.append(_TS_FIELD.match(ln).group(1))
            continue
        if made:
            for raw in _split_params(params_raw):
                made.params.append(_ts_param(raw))
            made.param_count = len(made.params)
            end = _brace_block(lines, i)
            made.end_line = end + 1
            made.body_lines = lines[i + 1:end + 1]
            if made.parent_class:
                current_class.methods.append(made)
            else:
                module.functions.append(made)
    return module


# ---------------------------------------------------------------- C++

_CPP_FUNC = re.compile(
    r"^\s*(?:(?:inline|virtual|static|explicit|constexpr|const)\s+)*"
    r"([\w:<>*\s&]+?)\s+(\w+)\s*\(([^;{}]*)\)\s*"
    r"(?:const)?\s*(?:noexcept)?\s*(?:override)?\s*(?:->\s*\w+)?\s*\{")
_CPP_CLASS = re.compile(
    r"^\s*(?:class|struct)\s+(\w+)(?:\s*:\s*((?:public|private|protected)\s+[\w:]+"
    r"(?:\s*,\s*(?:public|private|protected)\s+[\w:]+)*))?\s*\{")
_CPP_SKIP = ("if", "while", "for", "switch", "catch", "return", "else",
             "do", "sizeof", "new", "delete", "throw", "case", "using",
             "namespace", "template")


def parse_cpp(path: str, src: str) -> ModuleInfo:
    clean = strip_comments_and_strings(src)
    lines = clean.split("\n")
    module = ModuleInfo(name=path, file=path, language="cpp")
    for ln in lines:
        im = re.match(r"^\s*#include\s*[<\"]([^>\"]+)[>\"]", ln)
        if im:
            module.imports.append(im.group(1))
    current_class: Optional[ClassInfo] = None
    for i, ln in enumerate(lines):
        cm = _CPP_CLASS.match(ln)
        if cm:
            cls = ClassInfo(name=cm.group(1), file=path, line=i + 1, language="cpp")
            if cm.group(2):
                for part in cm.group(2).split(","):
                    kw, _, base = part.strip().partition(" ")
                    base = base.strip()
                    (cls.parent, cls.interfaces)[base in cls.interfaces] if False else None
                # split first base as parent, rest as interfaces
                bases = re.findall(r"(?:public|private|protected)\s+([\w:]+)",
                                   cm.group(2))
                if bases:
                    cls.parent = bases[0]
                    cls.interfaces = bases[1:]
            module.classes.append(cls)
            current_class = cls
            continue
        fm = _CPP_FUNC.match(ln)
        if fm and fm.group(2) not in _CPP_SKIP and fm.group(1).strip() not in ("", "="):
            ret = fm.group(1).strip()
            f = FunctionInfo(
                name=fm.group(2), file=path, line=i + 1, language="cpp",
                return_type=None if ret == "void" else ret,
                parent_class=current_class.name if current_class else None,
            )
            for raw in _split_params(fm.group(3)):
                raw = raw.strip()
                if not raw:
                    continue
                if " " in raw or "*" in raw.replace(" ", ""):
                    toks = raw.replace("*", " * ").split()
                    if len(toks) >= 2:
                        ptype = " ".join(toks[:-1])
                        f.params.append(Parameter(toks[-1], ptype))
                    else:
                        f.params.append Parameter(raw, None) if False else Parameter(toks[0], None)
                else:
                    f.params.append(Parameter(raw, None))
            f.param_count = len(f.params)
            end = _brace_block(lines, i)
            f.end_line = end + 1
            f.body_lines = lines[i + 1:end + 1]
            if current_class:
                current_class.methods.append(f)
            else:
                module.functions.append(f)
    return module


PARSERS = {
    "python": parse_python,
    "java": parse_java,
    "typescript": parse_typescript,
    "cpp": parse_cpp,
}
