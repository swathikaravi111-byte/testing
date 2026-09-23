"""Filesystem scanner: walks a source tree and analyzes supported files."""

import os
import sys

from .models import ProjectAnalysis, FileAnalysis
from .parsers import LANGUAGES, analyze_file

DEFAULT_EXCLUDE_DIRS = {
    ".git", "node_modules", "venv", ".venv", "__pycache__", "build",
    "dist", "target", ".idea", ".vscode", "vendor", "code-analyzer",
}


def scan(root: str, exclude_dirs=None) -> ProjectAnalysis:
    exclude_dirs = DEFAULT_EXCLUDE_DIRS if exclude_dirs is None else set(exclude_dirs)
    project = ProjectAnalysis(root=os.path.abspath(root))
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        for filename in sorted(filenames):
            path = os.path.join(dirpath, filename)
            if not _supported(filename):
                continue
            try:
                with open(path, encoding="utf-8", errors="replace") as fh:
                    source = fh.read()
                project.files.append(analyze_file(path, source))
            except Exception as exc:  # noqa: BLE001 - analyzer must not crash on one file
                project.file_errors += 1
                project.files.append(
                    FileAnalysis(path=path, language="unknown", error=str(exc))
                )
    return project


def _supported(filename: str) -> bool:
    lower = filename.lower()
    for exts in LANGUAGES.values():
        if isinstance(exts, str):
            exts = (exts,)
        if any(lower.endswith(e) for e in exts):
            return True
    return False
