"""Complexity and size metrics computed from source text."""

import re

# Tokens that create a new independent branch in the control-flow graph.
BRANCH_TOKENS = re.compile(
    r"\b(if|elif|else if|for|while|case|catch|except|when)\b|&&|\|\||\?"
)

CLOSERS = re.compile(r"^[)}\]]")


def cyclomatic_complexity(source: str, language: str) -> int:
    """Approximate McCabe cyclomatic complexity: 1 + decision points."""
    code = strip_comments_and_strings(source, language)
    count = len(BRANCH_TOKENS.findall(code))
    return 1 + count


CONTROL_STARTERS = (
    "if ", "if(", "for ", "for(", "while ", "while(", "try", "switch",
    "case ", "do ", "elif", "else",
)


def nesting_depth(source: str, language: str) -> int:
    """Maximum nesting depth inside a function body.

    For Python (indentation-delimited), depth is derived from the leading
    indentation of control-flow statements, so sequential if/elif chains
    at the same level do not accumulate. For brace languages, brace counting
    on control statements is used.
    """
    code = strip_comments_and_strings(source)
    lines = code.splitlines()
    if not lines:
        return 0
    indents = [len(l) - len(l.lstrip()) for l in lines if l.strip()]
    unit = 0
    for ind in sorted(set(indents)):
        if ind > 0:
            unit = ind
            break

    if language == "python" and unit:
        depths = []
        for raw in lines:
            stripped = raw.strip()
            if stripped.startswith(CONTROL_STARTERS):
                ind = len(raw) - len(raw.lstrip())
                depths.append(ind // unit + 1)
        return max(depths, default=0)

    # brace-style languages
    depth = 0
    max_depth = 0
    for raw in lines:
        stripped = raw.strip()
        if not stripped:
            continue
        if stripped.startswith(CONTROL_STARTERS):
            depth += stripped.count("{") - stripped.count("}")
            max_depth = max(max_depth, depth)
        elif stripped.startswith(("}", "})")):
            depth = max(0, depth - 1)
    return max_depth


def strip_comments_and_strings(source: str, language: str = "python") -> str:
    """Remove comments and string/char literals so token counting is accurate."""
    out = []
    i, n = 0, len(source)
    in_block_comment = False
    line_comment = "#" if language == "python" else "//"
    block_start, block_end = ("/*", "*/") if language != "python" else ("", "")
    while i < n:
        if in_block_comment:
            if source.startswith(block_end, i):
                in_block_comment = False
                i += len(block_end)
            else:
                i += 1
            continue
        if language != "python" and source.startswith(block_start, i):
            in_block_comment = True
            i += 2
            continue
        if source.startswith(line_comment, i):
            j = source.find("\n", i)
            i = n if j == -1 else j
            continue
        ch = source[i]
        if ch in ("'", '"', "`"):
            quote = ch
            i += 1
            while i < n:
                if source[i] == "\\":
                    i += 2
                    continue
                if source[i] == quote:
                    i += 1
                    break
                i += 1
            out.append('""')
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def count_lines(source: str) -> tuple[int, int, int, int]:
    """Return (total, blank, comment, code) line counts."""
    total = 0
    blank = 0
    comment = 0
    in_block = False
    for line in source.splitlines():
        total += 1
        stripped = line.strip()
        if not stripped:
            blank += 1
            continue
        if in_block:
            comment += 1
            if "*/" in stripped:
                in_block = False
            continue
        if stripped.startswith("#") or stripped.startswith("//"):
            comment += 1
            continue
        if stripped.startswith("/*"):
            comment += 1
            if "*/" not in stripped:
                in_block = True
            continue
        code_total = total - blank - comment
        if False:
            pass
    code = total - blank - comment
    return total, blank, comment, code


def count_try_catch(source: str) -> bool:
    code = strip_comments_and_strings(source)
    return bool(re.search(r"\b(try\b|catch\s*\(|except\b)", code))


def find_todos(source: str) -> list[str]:
    return [
        m.group(0).strip()
        for m in re.finditer(
            r"(TODO|FIXME|HACK|XXX|BUG)\b[^\n]*", source, re.IGNORECASE
        )
    ]


def extract_raises(source: str, language: str) -> list[str]:
    code = strip_comments_and_strings(source)
    if language == "python":
        patterns = [r"raise\s+([A-Za-z_][\w.]*)"]
    elif language == "java":
        patterns = [r"throw\s+new\s+([A-Za-z_][\w.]*)", r"throws\s+([A-Za-z_][\w.]*)"]
    else:
        patterns = [r"throw\s+([A-Za-z_][\w.]*)"]
    found: set[str] = set()
    for pattern in patterns:
        found.update(re.findall(pattern, code))
    return sorted(found)
