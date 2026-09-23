# Refactoring Suggestions

36 suggestions.

## 1. Replace Magic Number with Named Constant

- **Location**: `code-analyzer/analyzer/refactoring.py:216 · Refactoring._duplicate`
- **Why**: unexplained literals: 800

**Before**

```java
if len(items) > 86400: ...
```

**After**

```java
MAX_CACHE_SECONDS = 86_400

if len(items) > MAX_CACHE_SECONDS: ...

```

---

## 2. Format Long Lines

- **Location**: `code-analyzer/analyzer/refactoring.py:193 · Refactoring._high_complexity`
- **Why**: longest line = 146 chars

**Before**

```java
result = some_function(argument_one, argument_two, argument_three, argument_four, argument_five, argument_six, keyword=seventy_chars_long_value)
```

**After**

```java
result = some_function(
    argument_one, argument_two, argument_three,
    argument_four, argument_five, argument_six,
    keyword=short_value,
)
```

---

## 3. Format Long Lines

- **Location**: `code-analyzer/analyzer/refactoring.py:91 · Refactoring._long_function`
- **Why**: longest line = 127 chars

**Before**

```java
result = some_function(argument_one, argument_two, argument_three, argument_four, argument_five, argument_six, keyword=seventy_chars_long_value)
```

**After**

```java
result = some_function(
    argument_one, argument_two, argument_three,
    argument_four, argument_five, argument_six,
    keyword=short_value,
)
```

---

## 4. Replace Magic Number with Named Constant

- **Location**: `code-analyzer/analyzer/refactoring.py:91 · Refactoring._long_function`
- **Why**: unexplained literals: 1500

**Before**

```java
if len(items) > 86400: ...
```

**After**

```java
MAX_CACHE_SECONDS = 86_400

if len(items) > MAX_CACHE_SECONDS: ...

```

---

## 5. Format Long Lines

- **Location**: `code-analyzer/analyzer/refactoring.py:285 · Refactoring._long_line`
- **Why**: longest line = 167 chars

**Before**

```java
result = some_function(argument_one, argument_two, argument_three, argument_four, argument_five, argument_six, keyword=seventy_chars_long_value)
```

**After**

```java
result = some_function(
    argument_one, argument_two, argument_three,
    argument_four, argument_five, argument_six,
    keyword=short_value,
)
```

---

## 6. Resolve Outstanding TODOs

- **Location**: `code-analyzer/analyzer/refactoring.py:297 · Refactoring._print_debug`
- **Why**: TODO/FIXME markers indicate unfinished work or known debt.

**Before**

```java
bug(f: SmellFinding, fn: Function) -> Refactoring:; bug prints leak into production output and lack severity/levels.",
```

**After**

```python
# Convert into a tracked issue, then implement or remove the marker.
```

---

## 7. Resolve Outstanding TODOs

- **Location**: `code-analyzer/analyzer/refactoring.py:309 · Refactoring._todo`
- **Why**: TODO/FIXME markers indicate unfinished work or known debt.

**Before**

```java
todo(f: SmellFinding, fn: Function) -> Refactoring:; TODO/FIXME markers indicate unfinished work or known debt.",
```

**After**

```python
# Convert into a tracked issue, then implement or remove the marker.
```

---

## 8. Resolve Outstanding TODOs

- **Location**: `code-analyzer/analyzer/refactoring.py:48 · Refactoring.recipe_title`
- **Why**: TODO/FIXME markers indicate unfinished work or known debt.

**Before**

```java
todo": "Resolve Outstanding TODOs",
```

**After**

```python
# Convert into a tracked issue, then implement or remove the marker.
```

---

## 9. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/smells.py:60 · SmellFinding._function_smells`
- **Why**: Cyclomatic complexity is 12 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 10. Resolve Outstanding TODOs

- **Location**: `code-analyzer/analyzer/smells.py:60 · SmellFinding._function_smells`
- **Why**: TODO/FIXME markers indicate unfinished work or known debt.

**Before**

```java
bug print statement left in production code", "low"); todo", "; ".join(t[:80] for t in fn.todos[:3]), "low")
```

**After**

```python
# Convert into a tracked issue, then implement or remove the marker.
```

---

## 11. Replace Magic Number with Named Constant

- **Location**: `code-analyzer/tests/test_analyzer.py:214 · TestEndToEnd.test_full_run_generates_docs`
- **Why**: unexplained literals: 100

**Before**

```java
if len(items) > 86400: ...
```

**After**

```java
MAX_CACHE_SECONDS = 86_400

if len(items) > MAX_CACHE_SECONDS: ...

```

---

## 12. Resolve Outstanding TODOs

- **Location**: `code-analyzer/tests/test_analyzer.py:153 · TestSmells.test_smells_detected`
- **Why**: TODO/FIXME markers indicate unfinished work or known debt.

**Before**

```java
todo", ids)
```

**After**

```python
# Convert into a tracked issue, then implement or remove the marker.
```

---

## 13. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/parsers.py:657 · _braces_end`
- **Why**: Cyclomatic complexity is 12 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 14. Introduce Parameter Object

- **Location**: `code-analyzer/analyzer/parsers.py:614 · _build_function`
- **Why**: 15 parameters (, name, file, line, end_line, params, return_type, language, source, class_name, visibility, is_static, is_abstract, is_constructor, docstring) — group related data into a dataclass/record.

**Before**

```python
def _build_function(, name: str, file: str, line: int, end_line: int, params: list[Parameter], return_type, language: str, source: str, class_name, visibility, is_static, is_abstract, is_constructor, docstring) -> Function:
```

**After**

```python
            @dataclass
            class BuildFunctionConfig:
                : Any
name: str
file: str
line: int
end_line: int
params: list[Parameter]
return_type: Any
language: str
source: str
class_name: Any
visibility: Any
is_static: Any
is_abstract: Any
is_constructor: Any
docstring: Any

            def _build_function(config: BuildFunctionConfig) -> Function:
                ...

```

---

## 15. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/docs.py:109 · _example`
- **Why**: Cyclomatic complexity is 11 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 16. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/parsers.py:568 · _java_ts_params`
- **Why**: Cyclomatic complexity is 13 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 17. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/parsers.py:470 · _parse_cpp`
- **Why**: Cyclomatic complexity is 15 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 18. Extract Method

- **Location**: `code-analyzer/analyzer/parsers.py:470 · _parse_cpp`
- **Why**: _parse_cpp is 77 lines long. Split it into focused sub-functions, each doing one thing.

**Before**

```python
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
            if name in cpp
```

**After**

```python
# Split into logical steps:
def _parse_cpp(self, ...):
    data = _load_input(...)
    result = _apply_business_rules(data)
    return _format_output(result)

def _apply_business_rules(data):
    ...  # one cohesive responsibility per helper

```

---

## 19. Format Long Lines

- **Location**: `code-analyzer/analyzer/parsers.py:470 · _parse_cpp`
- **Why**: longest line = 134 chars

**Before**

```java
result = some_function(argument_one, argument_two, argument_three, argument_four, argument_five, argument_six, keyword=seventy_chars_long_value)
```

**After**

```java
result = some_function(
    argument_one, argument_two, argument_three,
    argument_four, argument_five, argument_six,
    keyword=short_value,
)
```

---

## 20. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/parsers.py:257 · _parse_java`
- **Why**: Cyclomatic complexity is 13 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 21. Extract Method

- **Location**: `code-analyzer/analyzer/parsers.py:257 · _parse_java`
- **Why**: _parse_java is 79 lines long. Split it into focused sub-functions, each doing one thing.

**Before**

```python
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
            params = _java_ts_params(m.group("p
```

**After**

```python
# Split into logical steps:
def _parse_java(self, ...):
    data = _load_input(...)
    result = _apply_business_rules(data)
    return _format_output(result)

def _apply_business_rules(data):
    ...  # one cohesive responsibility per helper

```

---

## 22. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/parsers.py:70 · _parse_python`
- **Why**: Cyclomatic complexity is 14 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 23. Extract Method

- **Location**: `code-analyzer/analyzer/parsers.py:70 · _parse_python`
- **Why**: _parse_python is 86 lines long. Split it into focused sub-functions, each doing one thing.

**Before**

```python
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
   
```

**After**

```python
# Split into logical steps:
def _parse_python(self, ...):
    data = _load_input(...)
    result = _apply_business_rules(data)
    return _format_output(result)

def _apply_business_rules(data):
    ...  # one cohesive responsibility per helper

```

---

## 24. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/parsers.py:359 · _parse_typescript`
- **Why**: Cyclomatic complexity is 19 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 25. Extract Method

- **Location**: `code-analyzer/analyzer/parsers.py:359 · _parse_typescript`
- **Why**: _parse_typescript is 95 lines long. Split it into focused sub-functions, each doing one thing.

**Before**

```python
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
                    docstri
```

**After**

```python
# Split into logical steps:
def _parse_typescript(self, ...):
    data = _load_input(...)
    result = _apply_business_rules(data)
    return _format_output(result)

def _apply_business_rules(data):
    ...  # one cohesive responsibility per helper

```

---

## 26. Replace Nested Conditionals with Guard Clauses

- **Location**: `code-analyzer/analyzer/parsers.py:187 · _py_params`
- **Why**: Nesting reaches depth 5. Invert conditions and return early to flatten the body.

**Before**

```python
def process(user, order):
    if user is not None:
        if order is not None:
            if order.paid:
                if user.active:
                    ship(order)

```

**After**

```python
def process(user, order):
    if user is None or order is None:
        return None
    if not order.paid:
        return None
    if not user.active:
        return None
    ship(order)

```

---

## 27. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/parsers.py:187 · _py_params`
- **Why**: Cyclomatic complexity is 14 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 28. Format Long Lines

- **Location**: `code-analyzer/analyzer/report.py:79 · _refactoring_doc`
- **Why**: longest line = 143 chars

**Before**

```java
result = some_function(argument_one, argument_two, argument_three, argument_four, argument_five, argument_six, keyword=seventy_chars_long_value)
```

**After**

```java
result = some_function(
    argument_one, argument_two, argument_three,
    argument_four, argument_five, argument_six,
    keyword=short_value,
)
```

---

## 29. Replace Print with Structured Logging

- **Location**: `code-analyzer/analyzer/report.py:98 · _summary_line`
- **Why**: Debug prints leak into production output and lack severity/levels.

**Before**

```python
print("value:", x)  # or console.log / System.out.println
```

**After**

```java
logger.info("value", extra={"value": x})  # or log.info(f"value={x}")
```

---

## 30. Resolve Outstanding TODOs

- **Location**: `code-analyzer/analyzer/metrics.py:148 · find_todos`
- **Why**: TODO/FIXME markers indicate unfinished work or known debt.

**Before**

```java
TODO|FIXME|HACK|XXX|BUG)\b[^\n]*", source, re.IGNORECASE
```

**After**

```python
# Convert into a tracked issue, then implement or remove the marker.
```

---

## 31. Replace Nested Conditionals with Guard Clauses

- **Location**: `code-analyzer/analyzer/docs.py:8 · generate_api_docs`
- **Why**: Nesting reaches depth 5. Invert conditions and return early to flatten the body.

**Before**

```python
def process(user, order):
    if user is not None:
        if order is not None:
            if order.paid:
                if user.active:
                    ship(order)

```

**After**

```python
def process(user, order):
    if user is None or order is None:
        return None
    if not order.paid:
        return None
    if not user.active:
        return None
    ship(order)

```

---

## 32. Replace Print with Structured Logging

- **Location**: `code-analyzer/analyze.py:14 · main`
- **Why**: Debug prints leak into production output and lack severity/levels.

**Before**

```python
print("value:", x)  # or console.log / System.out.println
```

**After**

```java
logger.info("value", extra={"value": x})  # or log.info(f"value={x}")
```

---

## 33. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/metrics.py:26 · nesting_depth`
- **Why**: Cyclomatic complexity is 13 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

## 34. Extract Shared Function

- **Location**: `code-analyzer/analyzer/parsers.py:380 · owning_class`
- **Why**: Body identical to owning_class (code-analyzer/analyzer/parsers.py:280) [hash d76272db35ea343b]

**Before**

```python
    def owning_class(pos: int) -> Optional[str]:
        owner = None
        for start, name in class_spans:
            if pos > start:
                owner = name
            else:
                break
        return owner

```

**After**

```python
# Move the shared logic into one place and delegate from both call sites:
def shared_logic(...):
        ...  # single canonical implementation

def original_a(...):
    return shared_logic(...)

def original_b(...):
    return shared_logic(...)

```

---

## 35. Replace Nested Conditionals with Guard Clauses

- **Location**: `code-analyzer/analyzer/metrics.py:69 · strip_comments_and_strings`
- **Why**: Nesting reaches depth 5. Invert conditions and return early to flatten the body.

**Before**

```python
def process(user, order):
    if user is not None:
        if order is not None:
            if order.paid:
                if user.active:
                    ship(order)

```

**After**

```python
def process(user, order):
    if user is None or order is None:
        return None
    if not order.paid:
        return None
    if not user.active:
        return None
    ship(order)

```

---

## 36. Decompose Conditional / Strategy Pattern

- **Location**: `code-analyzer/analyzer/metrics.py:69 · strip_comments_and_strings`
- **Why**: Cyclomatic complexity is 13 (> 10). Extract condition arms into named helpers or a dispatch table.

**Before**

```python
if a: ...
elif b: ...
elif c: ...
else: ...  # many arms inline
```

**After**

```java
HANDLERS = {
    "case_a": handle_a,
    "case_b": handle_b,
    "case_c": handle_c,
}

def dispatch(case, payload):
    return HANDLERS.get(case, default_handler)(payload)

```

---

