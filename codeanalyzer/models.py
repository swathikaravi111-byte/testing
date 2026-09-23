"""Data model for analysis results."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class Parameter:
    name: str
    type: Optional[str] = None
    default: Optional[str] = None
    kind: str = "positional"  # positional | keyword | variadic


@dataclass
class FunctionInfo:
    name: str
    file: str
    line: int
    end_line: int
    language: str
    params: List[Parameter] = field(default_factory=list)
    return_type: Optional[str] = None
    docstring: Optional[str] = None
    visibility: str = "public"  # public | private | protected | internal
    is_static: bool = False
    is_abstract: bool = False
    is_async: bool = False
    parent_class: Optional[str] = None
    body_lines: List[str] = field(default_factory=list)
    cyclomatic: int = 1
    cognitive: int = 0
    loc: int = 0
    param_count: int = 0
    max_nesting: int = 0
    smells: List[Dict[str, Any]] = field(default_factory=list)
    refactorings: List[Dict[str, Any]] = field(default_factory=list)

    @property
    def full_name(self) -> str:
        if self.parent_class:
            return f"{self.parent_class}.{self.name}"
        return self.name

    @property
    def signature(self) -> str:
        ps = ", ".join(
            (f"{p.name}: {p.type}" if p.type else p.name) +
            (f" = {p.default}" if p.default else "")
            for p in self.params
        )
        ret = f" -> {self.return_type}" if self.return_type else ""
        prefix = "async " if self.is_async else ""
        return f"{prefix}{self.full_name}({ps}){ret}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.full_name,
            "file": self.file,
            "line": self.line,
            "signature": self.signature,
            "params": [
                {"name": p.name, "type": p.type, "default": p.default}
                for p in self.params
            ],
            "return_type": self.return_type,
            "visibility": self.visibility,
            "async": self.is_async,
            "metrics": {
                "cyclomatic": self.cyclomatic,
                "cognitive": self.cognitive,
                "loc": self.loc,
                "params": self.param_count,
                "max_nesting": self.max_nesting,
            },
        }


@dataclass
class ClassInfo:
    name: str
    file: str
    line: int
    language: str
    parent: Optional[str] = None
    interfaces: List[str] = field(default_factory=list)
    methods: List[FunctionInfo] = field(default_factory=list)
    fields: List[str] = field(default_factory=list)
    docstring: Optional[str] = None
    visibility: str = "public"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "file": self.file,
            "line": self.line,
            "extends": self.parent,
            "implements": self.interfaces,
            "visibility": self.visibility,
            "methods": len(self.methods),
            "fields": len(self.fields),
        }


@dataclass
class ModuleInfo:
    name: str
    file: str
    language: str
    imports: List[str] = field(default_factory=list)
    classes: List[ClassInfo] = field(default_factory=list)
    functions: List[FunctionInfo] = field(default_factory=list)

    @property
    def all_functions(self) -> List[FunctionInfo]:
        return self.functions + [m for c in self.classes for m in c.methods]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "file": self.file,
            "language": self.language,
            "imports": self.imports,
            "classes": [c.to_dict() for c in self.classes],
            "functions": [f.to_dict() for f in self.functions],
        }


@dataclass
class AnalysisResult:
    modules: List[ModuleInfo] = field(default_factory=list)
    total_files: int = 0
    total_functions: int = 0
    total_classes: int = 0
    total_loc: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_files": self.total_files,
            "total_functions": self.total_functions,
            "total_classes": self.total_classes,
            "total_loc": self.total_loc,
            "modules": [m.to_dict() for m in self.modules],
        }
