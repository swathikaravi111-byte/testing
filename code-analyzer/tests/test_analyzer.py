import os
import tempfile
import unittest

from analyzer.metrics import cyclomatic_complexity, count_lines, nesting_depth, strip_comments_and_strings
from analyzer.models import ProjectAnalysis
from analyzer.parsers import analyze_file, detect_language
from analyzer.report import generate_quality_report, run
from analyzer.refactoring import suggest
from analyzer.smells import detect_smells
from analyzer.scanner import scan


PY_SRC = '''\
"""Module docstring."""
import logging


def add(a: int, b: int = 1) -> int:
    """Add two numbers."""
    if a > 0 and b > 0:
        return a + b
    return 0


class Widget:
    def __init__(self, name: str):
        self.name = name

    @staticmethod
    def helper(x):
        return x
'''


class TestMetrics(unittest.TestCase):
    def test_complexity_counts_branches(self):
        src = "if a:\n    pass\nelif b:\n    pass\nelse:\n    pass\n"
        self.assertEqual(cyclomatic_complexity(src, "python"), 3)

    def test_comments_and_strings_stripped(self):
        src = 'x = "if if if"  # if\ny = 1\n'
        self.assertEqual(cyclomatic_complexity(src, "python"), 1)

    def test_line_counts(self):
        total, blank, comment, code = count_lines(
            "# comment\n\nx = 1\ny = 2\n"
        )
        self.assertEqual((total, blank, comment, code), (4, 1, 1, 2))

    def test_nesting(self):
        self.assertEqual(nesting_depth("if a:\n  if b:\n    if c:\n      pass\n", "python"), 3)


class TestParsers(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()

    def _write(self, name, src):
        path = os.path.join(self.tmp, name)
        os.makedirs(os.path.dirname(path), exist_ok=True) if os.path.dirname(name) else None
        with open(path, "w") as fh:
            fh.write(src)
        return path

    def test_language_detection(self):
        self.assertEqual(detect_language("a.py"), "python")
        self.assertEqual(detect_language("a.java"), "java")
        self.assertEqual(detect_language("a.ts"), "typescript")
        self.assertEqual(detect_language("a.cpp"), "cpp")
        self.assertEqual(detect_language("a.hpp"), "cpp")
        self.assertIsNone(detect_language("a.txt"))

    def test_python_parse(self):
        path = self._write("mod.py", PY_SRC)
        fa = analyze_file(path, PY_SRC)
        names = [f.name for f in fa.functions]
        self.assertIn("add", names)
        self.assertIn("__init__", names)
        self.assertIn("helper", names)
        add = next(f for f in fa.functions if f.name == "add")
        self.assertEqual(add.return_type, "int")
        self.assertEqual(len(add.parameters), 2)
        self.assertEqual(add.parameters[0].type, "int")
        self.assertEqual(add.parameters[1].default, "1")
        self.assertEqual(add.cyclomatic_complexity, 2)
        self.assertEqual(add.docstring, "Add two numbers.")
        w = next(f for f in fa.functions if f.name == "helper")
        self.assertTrue(w.is_static)
        self.assertEqual(w.class_name, "Widget")

    def test_java_parse(self):
        src = (
            "public class Foo {\n"
            "    /** Doc. */\n"
            "    public int compute(int a, String b) throws Exception {\n"
            "        if (a > 0) { return a; }\n"
            "        return 0;\n"
            "    }\n"
            "    private static void helper() { }\n"
            "}\n"
        )
        path = self._write("Foo.java", src)
        fa = analyze_file(path, src)
        compute = next(f for f in fa.functions if f.name == "compute")
        self.assertEqual(compute.class_name, "Foo")
        self.assertEqual(compute.return_type, "int")
        self.assertEqual(compute.visibility, "public")
        self.assertIn("Exception", compute.raises)
        self.assertEqual(fa.classes[0].name, "Foo")

    def test_typescript_parse(self):
        src = (
            "export class Svc {\n"
            "  get(id: number): string { return ''; }\n"
            "}\n"
            "export function norm(raw: string, opts?: object): string { return raw; }\n"
        )
        path = self._write("svc.ts", src)
        fa = analyze_file(path, src)
        self.assertEqual(fa.classes[0].name, "Svc")
        get_fn = next(f for f in fa.functions if f.name == "get")
        self.assertEqual(get_fn.return_type, "string")
        self.assertEqual(get_fn.class_name, "Svc")
        norm = next(f for f in fa.functions if f.name == "norm")
        self.assertEqual(norm.return_type, "string")
        self.assertEqual(len(norm.parameters), 2)

    def test_cpp_parse(self):
        src = (
            "class Eng {\n"
            "public:\n"
            "    double calc(double price, int qty) const {\n"
            "        if (price > 0) { return price * qty; }\n"
            "        return 0;\n"
            "    }\n"
            "};\n"
        )
        path = self._write("eng.cpp", src)
        fa = analyze_file(path, src)
        self.assertEqual(fa.classes[0].name, "Eng")
        calc = fa.functions[0]
        self.assertEqual(calc.name, "calc")
        self.assertEqual(calc.return_type, "double")
        self.assertEqual(calc.class_name, "Eng")


class TestSmells(unittest.TestCase):
    def _fn_from_source(self, src, filename="m.py"):
        fa = analyze_file(os.path.join("/tmp", filename), src)
        return fa

    def test_smells_detected(self):
        path = os.path.join(os.path.dirname(__file__), "..", "..", "sample-project")
        if not os.path.isdir(path):
            self.skipTest("sample project missing")
        project = scan(path)
        findings = detect_smells(project)
        ids = {f.smell_id for f in findings}
        self.assertIn("deep-nesting", ids)
        self.assertIn("empty-catch", ids)
        self.assertIn("magic-number", ids)
        self.assertIn("high-complexity", ids)
        self.assertIn("print-debugging", ids)
        self.assertIn("todo", ids)

    def test_duplicates(self):
        body = (
            "def a(x):\n"
            "    y = x + 1\n"
            "    z = y * 2\n"
            "    w = z - 3\n"
            "    return w\n\n\n"
            "def b(x):\n"
            "    y = x + 1\n"
            "    z = y * 2\n"
            "    w = z - 3\n"
            "    return w\n"
        )
        src_path = os.path.join(tempfile.mkdtemp(), "dup.py")
        with open(src_path, "w") as fh:
            fh.write(body)
        fa = analyze_file(src_path, body)
        project = ProjectAnalysis(root="/tmp")
        project.files.append(fa)
        findings = detect_smells(project)
        self.assertTrue(any(f.smell_id == "duplicate-code" for f in findings))

    def test_refactoring_suggestions_generated(self):
        path = os.path.join(os.path.dirname(__file__), "..", "..", "sample-project")
        if not os.path.isdir(path):
            self.skipTest("sample project missing")
        project = scan(path)
        findings = detect_smells(project)
        refactorings = suggest(project, findings)
        self.assertTrue(len(refactorings) > 5)
        titles = {r.title for r in refactorings}
        self.assertIn("Introduce Parameter Object", titles)
        self.assertIn("Replace Nested Conditionals with Guard Clauses", titles)
        self.assertTrue(all(r.before or r.after for r in refactorings))

    def test_quality_report_renders(self):
        path = os.path.join(os.path.dirname(__file__), "..", "..", "sample-project")
        if not os.path.isdir(path):
            self.skipTest("sample project missing")
        project = scan(path)
        findings = detect_smells(project)
        report = generate_quality_report(project, findings)
        self.assertIn("# Code Quality Report", report)
        self.assertIn("Hotspots", report)


class TestEndToEnd(unittest.TestCase):
    def test_full_run_generates_docs(self):
        sample = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "sample-project")
        )
        if not os.path.isdir(sample):
            self.skipTest("sample project missing")
        import tempfile

        out = tempfile.mkdtemp()
        result = run(sample, out)
        outputs = result["outputs"]
        self.assertEqual(len(outputs), 4)
        for name, path in outputs.items():
            self.assertTrue(os.path.isfile(path), name)
            content = open(path).read()
            self.assertTrue(len(content) > 100, name)
        arch = open(outputs["ARCHITECTURE.md"]).read()
        self.assertIn("```mermaid", arch)
        api = open(outputs["API_REFERENCE.md"]).read()
        self.assertIn("place_order", api)
        self.assertIn("authorizePayment", api)
        self.assertIn("applyDiscount", api)
        self.assertIn("registerUser", api)
        self.assertIn("**Example**", api)
        quality = open(outputs["QUALITY_REPORT.md"]).read()
        self.assertIn("Findings Detail", quality)
        refactor = open(outputs["REFACTORING.md"]).read()
        self.assertIn("Refactoring Suggestions", refactor)


if __name__ == "__main__":
    unittest.main()
