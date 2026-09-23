"""Intelligent code analysis system.

Scans Java, Python, TypeScript and C++ sources, extracts signatures and
complexity metrics, generates API documentation, architecture diagrams,
code-smell detection and refactoring suggestions.
"""

__version__ = "1.0.0"

from .analyzer import Analyzer
from .report import ReportGenerator

__all__ = ["Analyzer", "ReportGenerator", "__version__"]
