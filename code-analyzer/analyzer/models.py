"""Core data models for the code analysis system."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Parameter:
    name: str
    type: Optional[str] = None
    default: Optional[str] = None
    is_variadic: bool = False

    def signature(self) -> str:
        s = f"{self.name}: {self.type}" if self.type else self.name
        if self.is_variadic:
            s = f"*{self.name}: {self.type or 'any'}"
        if self.default is not None:
            s += f" = {self.default}"
        return s


@dataclass
class Function:
    name: str
    file: str
    line: int
    end_line: int
    parameters: list[Parameter] = field(default_factory=list)
    return_type: Optional[str] = None
    class_name: Optional[str] = None
    visibility: str = "public"
    is_static: bool = False
    is_abstract: bool = False
    is_constructor: bool = False
    docstring: Optional[str] = None
    source: str = ""
    lines_of_code: int = 0
    cyclomatic_complexity: int = 1
    nesting_depth: int = 0
    parameter_count: int = 0
    max_line_length: int = 0
    comment_lines: int = 0
    has_try_catch: bool = False
    smells: list[str] = field(default_factory=list)
    imports: list[str] = field(default_factory=list)
    raises: list[str] = field(default_factory=list)
    todos: list[str] = field(default_factory=list)

    @property
    def qualified_name(self) -> str:
        return f"{self.class_name}.{self.name}" if self.class_name else self.name

    def signature(self) -> str:
        params = ", ".join(p.signature() for p in self.parameters)
        ret = f" -> {self.return_type}" if self.return_type else ""
        prefix = ""
        if self.class_name:
            prefix = f"{self.class_name}::"
        return f"{prefix}{self.name}({params}){ret}"


@dataclass
class ClassInfo:
    name: str
    file: str
    line: int
    kind: str = "class"  # class | interface | struct | enum | record
    extends: list[str] = field(default_factory=list)
    implements: list[str] = field(default_factory=list)
    methods: list[Function] = field(default_factory=list)
    docstring: Optional[str] = None


@dataclass
class Import:
    module: str
    file: str
    line: int
    symbols: list[str] = field(default_factory=list)
    kind: str = "import"  # import | include | using | from


@dataclass
class FileAnalysis:
    path: str
    language: str
    lines: int = 0
    blank_lines: int = 0
    comment_lines: int = 0
    code_lines: int = 0
    functions: list[Function] = field(default_factory=list)
    classes: list[ClassInfo] = field(default_factory=list)
    imports: list[Import] = field(default_factory=list)
    todos: list[str] = field(default_factory=list)
    error: Optional[str] = None


@dataclass
class ProjectAnalysis:
    root: str
    files: list[FileAnalysis] = field(default_factory=list)
    file_errors: int = 0

    @property
    def all_functions(self) -> list[Function]:
        return [f for fa in self.files for f in fa.functions]

    @property
    def all_classes(self) -> list[ClassInfo]:
        return [c for fa in self.files for c in fa.classes]

    @property
    def all_imports(self) -> list[Import]:
        return [i for fa in self.files for i in fa.imports]

    @property
    def total_loc(self) -> int:
        return sum(f.code_lines for f in self.files)

    def language_stats(self) -> dict:
        stats: dict[str, dict] = {}
        for fa in self.files:
            s = stats.setdefault(
                fa.language, {"files": 0, "loc": 0, "functions": 0, "classes": 0}
            )
            s["files"] += 1
            s["loc"] += fa.code_lines
            s["functions"] += len(fa.functions)
            s["classes"] += len(fa.classes)
        return stats
