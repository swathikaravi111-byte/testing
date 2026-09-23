"""Refactoring suggestion engine with concrete code samples."""

import textwrap
from dataclasses import dataclass

from .models import Function
from .smells import SmellFinding, smell_summary


@dataclass
class Refactoring:
    title: str
    smell_id: str
    location: str
    rationale: str
    before: str
    after: str


def suggest(project, findings: list[SmellFinding]) -> list[Refactoring]:
    by_key = {}
    for f in findings:
        by_key.setdefault((f.function, f.smell_id), f)

    out: list[Refactoring] = []
    fn_map = {f"{fn.file}|{fn.qualified_name}|{fn.line}": fn for fn in project.all_functions}

    for (qualified, smell_id), finding in sorted(by_key.items()):
        fn = fn_map.get(f"{finding.file}|{finding.function}|{finding.line}")
        recipe = RECIPES.get(smell_id)
        if not recipe:
            continue
        out.append(
            recipe(finding, fn)
            if fn
            else Refactoring(
                title=recipe_title(smell_id),
                smell_id=smell_id,
                location=f"{finding.file}:{finding.line}",
                rationale=finding.description,
                before="",
                after="",
            )
        )
    return out


def recipe_title(smell_id: str) -> str:
    return {
        "long-function": "Extract Method",
        "high-complexity": "Decompose Conditional / Replace Conditional with Polymorphism",
        "deep-nesting": "Replace Nested Conditionals with Guard Clauses",
        "too-many-parameters": "Introduce Parameter Object",
        "long-line": "Format Long Lines",
        "duplicate-code": "Extract Shared Function",
        "magic-number": "Replace Magic Number with Named Constant",
        "empty-catch": "Handle or Propagate the Exception",
        "print-debugging": "Replace Print with Structured Logging",
        "todo": "Resolve Outstanding TODOs",
    }.get(smell_id, "Review")


def _sig(fn: Function) -> str:
    lang = "python" if fn.file.endswith(".py") else "java"
    if lang == "python":
        params = ", ".join(
            (f"{p.name}: {p.type}" if p.type else p.name) for p in fn.parameters
        )
        ret = f" -> {fn.return_type}" if fn.return_type else ""
        return f"def {fn.name}({params}){ret}:"
    params = ", ".join(
        f"{p.type} {p.name}" if p.type and p.type != "void" else p.name
        for p in fn.parameters
    )
    ret = fn.return_type or "void"
    return f"{ret} {fn.name}({params})"


RECIPES = {}


def _register(smell_id):
    def deco(fn):
        RECIPES[smell_id] = fn
        return fn

    return deco


@_register("long-function")
def _long_function(f: SmellFinding, fn: Function) -> Refactoring:
    return Refactoring(
        title="Extract Method",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale=f"{f.function} is {fn.lines_of_code} lines long. Split it into focused sub-functions, each doing one thing.",
        before=textwrap.indent(fn.source[:1500], "    "),
        after=textwrap.dedent(
            f"""\
            # Split into logical steps:
            def {fn.name}(self, ...):
                data = _load_input(...)
                result = _apply_business_rules(data)
                return _format_output(result)

            def _apply_business_rules(data):
                ...  # one cohesive responsibility per helper
            """
        )
        if fn.file.endswith(".py")
        else textwrap.dedent(
            f"""\
            // Split into logical steps:
            {(_sig(fn).replace(fn.name, fn.name)).strip('')} {{
                var data = loadInput();
                var result = applyBusinessRules(data);
                return formatOutput(result);
            }}

            private Result applyBusinessRules(Data data) {{
                // one cohesive responsibility per helper
            }}
            """
        ),
    )


@_register("deep-nesting")
def _deep_nesting(f: SmellFinding, fn: Function) -> Refactoring:
    return Refactoring(
        title="Replace Nested Conditionals with Guard Clauses",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale=f"Nesting reaches depth {fn.nesting_depth}. Invert conditions and return early to flatten the body.",
        before=textwrap.dedent(
            """\
            def process(user, order):
                if user is not None:
                    if order is not None:
                        if order.paid:
                            if user.active:
                                ship(order)
            """
        ),
        after=textwrap.dedent(
            """\
            def process(user, order):
                if user is None or order is None:
                    return None
                if not order.paid:
                    return None
                if not user.active:
                    return None
                ship(order)
            """
        ),
    )


@_register("too-many-parameters")
def _too_many_params(f: SmellFinding, fn: Function) -> Refactoring:
    names = ", ".join(p.name for p in fn.parameters)
    return Refactoring(
        title="Introduce Parameter Object",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale=f"{fn.parameter_count} parameters ({names}) — group related data into a dataclass/record.",
        before=f"{_sig(fn)}",
        after=textwrap.dedent(
            f"""\
            @dataclass
            class {fn.name.title().replace('_','')}Config:
                {chr(10).join(f'{p.name}: {p.type or "Any"}' for p in fn.parameters)}

            def {fn.name}(config: {fn.name.title().replace('_','')}Config) -> {fn.return_type or "None"}:
                ...
            """
        )
        if fn.file.endswith(".py")
        else textwrap.dedent(
            f"""\
            public record {fn.name}Config(
                {', '.join((f'{p.type or "Object"} {p.name}') for p in fn.parameters)}
            ) {{ }}

            public {fn.return_type or "void"} {fn.name}({fn.name}Config cfg) {{ ... }}
            """
        ),
    )


@_register("high-complexity")
def _high_complexity(f: SmellFinding, fn: Function) -> Refactoring:
    return Refactoring(
        title="Decompose Conditional / Strategy Pattern",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale=f"Cyclomatic complexity is {fn.cyclomatic_complexity} (> {10}). Extract condition arms into named helpers or a dispatch table.",
        before="if a: ...\nelif b: ...\nelif c: ...\nelse: ...  # many arms inline",
        after=textwrap.dedent(
            """\
            HANDLERS = {
                "case_a": handle_a,
                "case_b": handle_b,
                "case_c": handle_c,
            }

            def dispatch(case, payload):
                return HANDLERS.get(case, default_handler)(payload)
            """
        ),
    )


@_register("duplicate-code")
def _duplicate(f: SmellFinding, fn: Function) -> Refactoring:
    return Refactoring(
        title="Extract Shared Function",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale=f.details,
        before=fn.source[:800],
        after=textwrap.dedent(
            """\
            # Move the shared logic into one place and delegate from both call sites:
            def shared_logic(...):
                    ...  # single canonical implementation

            def original_a(...):
                return shared_logic(...)

            def original_b(...):
                return shared_logic(...)
            """
        ),
    )


@_register("empty-catch")
def _empty_catch(f: SmellFinding, fn: Function) -> Refactoring:
    return Refactoring(
        title="Handle or Propagate the Exception",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale="An exception is caught and silently ignored, hiding real failures.",
        before=textwrap.dedent(
            """\
            try:
                risky()
            except Exception:
                pass  # swallowed
            """
        ),
        after=textwrap.dedent(
            """\
            try:
                risky()
            except SpecificError as exc:
                logger.warning("risky() failed: %s", exc)
                raise  # or convert to a domain error
            """
        ),
    )


@_register("magic-number")
def _magic_number(f: SmellFinding, fn: Function) -> Refactoring:
    return Refactoring(
        title="Replace Magic Number with Named Constant",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale=f.details,
        before="if len(items) > 86400: ...",
        after=textwrap.dedent(
            """\
            MAX_CACHE_SECONDS = 86_400

            if len(items) > MAX_CACHE_SECONDS: ...
            """
        ),
    )


@_register("long-line")
def _long_line(f: SmellFinding, fn: Function) -> Refactoring:
    return Refactoring(
        title="Format Long Lines",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale=f.details,
        before="result = some_function(argument_one, argument_two, argument_three, argument_four, argument_five, argument_six, keyword=seventy_chars_long_value)",
        after="result = some_function(\n    argument_one, argument_two, argument_three,\n    argument_four, argument_five, argument_six,\n    keyword=short_value,\n)",
    )


@_register("print-debugging")
def _print_debug(f: SmellFinding, fn: Function) -> Refactoring:
    return Refactoring(
        title="Replace Print with Structured Logging",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale="Debug prints leak into production output and lack severity/levels.",
        before='print("value:", x)  # or console.log / System.out.println',
        after='logger.info("value", extra={"value": x})  # or log.info(f"value={x}")',
    )


@_register("todo")
def _todo(f: SmellFinding, fn: Function) -> Refactoring:
    return Refactoring(
        title="Resolve Outstanding TODOs",
        smell_id=f.smell_id,
        location=f"{f.file}:{f.line} · {f.function}",
        rationale="TODO/FIXME markers indicate unfinished work or known debt.",
        before=f.details,
        after="# Convert into a tracked issue, then implement or remove the marker.",
    )
