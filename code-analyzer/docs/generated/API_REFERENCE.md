# API Reference

Auto-generated for `code-analyzer` — 105 functions across 12 files.

## Python

### `analyze.py`

<a id="main-14"></a>

##### `main(argv = None)` → `int`

`code-analyzer/analyze.py:14` · LOC **14** · complexity **2** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `argv` | `—` | `None` |

**Returns** `int`

**Example**

```py
# main
result = main(argv)
```

---

### `analyzer/architecture.py`

<a id="generate_architecture_doc-9"></a>

##### `generate_architecture_doc(project: ProjectAnalysis)` → `str`

`code-analyzer/analyzer/architecture.py:9` · LOC **15** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `ProjectAnalysis` | `—` |

**Returns** `str`

**Example**

```py
# generate_architecture_doc
result = generate_architecture_doc(project)
```

<a id="_stats-24"></a>

##### `_stats(project)` → `list[str]`

`code-analyzer/analyzer/architecture.py:24` · LOC **18** · complexity **2** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `—` | `—` |

**Returns** `list[str]`

**Example**

```py
# _stats
result = _stats(project)
```

<a id="_module_name-42"></a>

##### `_module_name(path)` → `str`

`code-analyzer/analyzer/architecture.py:42` · LOC **4** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `path` | `—` | `—` |

**Returns** `str`

**Example**

```py
# _module_name
result = _module_name(path)
```

<a id="_dep_graph-46"></a>

##### `_dep_graph(project)` → `list[str]`

`code-analyzer/analyzer/architecture.py:46` · LOC **26** · complexity **7** · nesting **3**

**Description**

Mermaid graph of file-to-file dependencies based on imports.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `—` | `—` |

**Returns** `list[str]`

**Example**

```py
# _dep_graph
result = _dep_graph(project)
```

<a id="_resolve_local-72"></a>

##### `_resolve_local(imp, project)`

`code-analyzer/analyzer/architecture.py:72` · LOC **17** · complexity **8** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `imp` | `—` | `—` |
| `project` | `—` | `—` |

**Example**

```py
# _resolve_local
_resolve_local(imp, project)
```

<a id="_class_diagram-89"></a>

##### `_class_diagram(project)` → `list[str]`

`code-analyzer/analyzer/architecture.py:89` · LOC **17** · complexity **7** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `—` | `—` |

**Returns** `list[str]`

**Example**

```py
# _class_diagram
result = _class_diagram(project)
```

<a id="_module_structure-106"></a>

##### `_module_structure(project)` → `list[str]`

`code-analyzer/analyzer/architecture.py:106` · LOC **17** · complexity **6** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `—` | `—` |

**Returns** `list[str]`

**Example**

```py
# _module_structure
result = _module_structure(project)
```

---

### `analyzer/docs.py`

<a id="generate_api_docs-8"></a>

##### `generate_api_docs(project: ProjectAnalysis)` → `str`

`code-analyzer/analyzer/docs.py:8` · LOC **32** · complexity **8** · nesting **5**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `ProjectAnalysis` | `—` |

**Returns** `str`

**Example**

```py
# generate_api_docs
result = generate_api_docs(project)
```

<a id="_class_doc-40"></a>

##### `_class_doc(project)` → `list[str]`

`code-analyzer/analyzer/docs.py:40` · LOC **15** · complexity **5** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `—` | `—` |

**Returns** `list[str]`

**Example**

```py
# _class_doc
result = _class_doc(project)
```

<a id="_function_doc-55"></a>

##### `_function_doc(fn: Function, project, depth: int)` → `list[str]`

`code-analyzer/analyzer/docs.py:55` · LOC **54** · complexity **8** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `fn` | `Function` | `—` |
| `project` | `—` | `—` |
| `depth` | `int` | `—` |

**Returns** `list[str]`

**Example**

```py
# _function_doc
result = _function_doc(fn, project, depth)
```

<a id="_example-109"></a>

##### `_example(fn: Function, lang_ext: str)` → `list[str]`

`code-analyzer/analyzer/docs.py:109` · LOC **24** · complexity **11** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `fn` | `Function` | `—` |
| `lang_ext` | `str` | `—` |

**Returns** `list[str]`

**Example**

```py
# _example
result = _example(fn, lang_ext)
```

<a id="_rel-133"></a>

##### `_rel(project, path)` → `str`

`code-analyzer/analyzer/docs.py:133` · LOC **2** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `—` | `—` |
| `path` | `—` | `—` |

**Returns** `str`

**Example**

```py
# _rel
result = _rel(project, path)
```

---

### `analyzer/metrics.py`

<a id="cyclomatic_complexity-13"></a>

##### `cyclomatic_complexity(source: str, language: str)` → `int`

`code-analyzer/analyzer/metrics.py:13` · LOC **7** · complexity **1** · nesting **0**

**Description**

Approximate McCabe cyclomatic complexity: 1 + decision points.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |
| `language` | `str` | `—` |

**Returns** `int`

**Example**

```py
# cyclomatic_complexity
result = cyclomatic_complexity(source, language)
```

<a id="nesting_depth-26"></a>

##### `nesting_depth(source: str, language: str)` → `int`

`code-analyzer/analyzer/metrics.py:26` · LOC **43** · complexity **13** · nesting **4**

**Description**

Maximum nesting depth inside a function body.

    For Python (indentation-delimited), depth is derived from the leading
    indentation of control-flow statements, so sequential if/elif chains
    at the same level do not accumulate. For brace languages, brace counting
    on control statements is used.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |
| `language` | `str` | `—` |

**Returns** `int`

**Example**

```py
# nesting_depth
result = nesting_depth(source, language)
```

<a id="strip_comments_and_strings-69"></a>

##### `strip_comments_and_strings(source: str, language: str = "python")` → `str`

`code-analyzer/analyzer/metrics.py:69` · LOC **42** · complexity **13** · nesting **5**

**Description**

Remove comments and string/char literals so token counting is accurate.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |
| `language` | `str` | `"python"` |

**Returns** `str`

**Example**

```py
# strip_comments_and_strings
result = strip_comments_and_strings(source, language)
```

<a id="count_lines-111"></a>

##### `count_lines(source: str)` → `tuple[int, int, int, int]`

`code-analyzer/analyzer/metrics.py:111` · LOC **32** · complexity **9** · nesting **4**

**Description**

Return (total, blank, comment, code) line counts.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |

**Returns** `tuple[int, int, int, int]`

**Example**

```py
# count_lines
result = count_lines(source)
```

<a id="count_try_catch-143"></a>

##### `count_try_catch(source: str)` → `bool`

`code-analyzer/analyzer/metrics.py:143` · LOC **5** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |

**Returns** `bool`

**Example**

```py
# count_try_catch
result = count_try_catch(source)
```

<a id="find_todos-148"></a>

##### `find_todos(source: str)` → `list[str]`

`code-analyzer/analyzer/metrics.py:148` · LOC **9** · complexity **2** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |

**Returns** `list[str]`

**Example**

```py
# find_todos
result = find_todos(source)
```

<a id="extract_raises-157"></a>

##### `extract_raises(source: str, language: str)` → `list[str]`

`code-analyzer/analyzer/metrics.py:157` · LOC **12** · complexity **4** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |
| `language` | `str` | `—` |

**Returns** `list[str]`

**Example**

```py
# extract_raises
result = extract_raises(source, language)
```

---

### `analyzer/models.py`

####  🔧 `class Parameter`

####  🔧 `class Function`

####  🔧 `class ClassInfo`

####  🔧 `class Import`

####  🔧 `class FileAnalysis`

####  🔧 `class ProjectAnalysis`

<a id="Parameter-signature-14"></a>

##### `Parameter.signature()` → `str`

member of `Parameter` · `code-analyzer/analyzer/models.py:14` · LOC **9** · complexity **4** · nesting **3**

**Returns** `str`

**Example**

```py
obj = Parameter()
result = obj.signature()
```

<a id="Function-qualified_name-51"></a>

##### `Function.qualified_name()` → `str`

member of `Function` · `code-analyzer/analyzer/models.py:51` · LOC **3** · complexity **2** · nesting **0**

**Returns** `str`

**Example**

```py
obj = Function()
result = obj.qualified_name()
```

<a id="Function-signature-54"></a>

##### `Function.signature()` → `str`

member of `Function` · `code-analyzer/analyzer/models.py:54` · LOC **9** · complexity **4** · nesting **3**

**Returns** `str`

**Example**

```py
obj = Function()
result = obj.signature()
```

<a id="ProjectAnalysis-all_functions-106"></a>

##### `ProjectAnalysis.all_functions()` → `list[Function]`

member of `ProjectAnalysis` · `code-analyzer/analyzer/models.py:106` · LOC **3** · complexity **3** · nesting **0**

**Returns** `list[Function]`

**Example**

```py
obj = ProjectAnalysis()
result = obj.all_functions()
```

<a id="ProjectAnalysis-all_classes-110"></a>

##### `ProjectAnalysis.all_classes()` → `list[ClassInfo]`

member of `ProjectAnalysis` · `code-analyzer/analyzer/models.py:110` · LOC **3** · complexity **3** · nesting **0**

**Returns** `list[ClassInfo]`

**Example**

```py
obj = ProjectAnalysis()
result = obj.all_classes()
```

<a id="ProjectAnalysis-all_imports-114"></a>

##### `ProjectAnalysis.all_imports()` → `list[Import]`

member of `ProjectAnalysis` · `code-analyzer/analyzer/models.py:114` · LOC **3** · complexity **3** · nesting **0**

**Returns** `list[Import]`

**Example**

```py
obj = ProjectAnalysis()
result = obj.all_imports()
```

<a id="ProjectAnalysis-total_loc-118"></a>

##### `ProjectAnalysis.total_loc()` → `int`

member of `ProjectAnalysis` · `code-analyzer/analyzer/models.py:118` · LOC **3** · complexity **2** · nesting **0**

**Returns** `int`

**Example**

```py
obj = ProjectAnalysis()
result = obj.total_loc()
```

<a id="ProjectAnalysis-language_stats-121"></a>

##### `ProjectAnalysis.language_stats()` → `dict`

member of `ProjectAnalysis` · `code-analyzer/analyzer/models.py:121` · LOC **11** · complexity **2** · nesting **3**

**Returns** `dict`

**Example**

```py
obj = ProjectAnalysis()
result = obj.language_stats()
```

---

### `analyzer/parsers.py`

<a id="detect_language-24"></a>

##### `detect_language(path: str)` → `Optional[str]`

`code-analyzer/analyzer/parsers.py:24` · LOC **12** · complexity **6** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `path` | `str` | `—` |

**Returns** `Optional[str]`

**Example**

```py
# detect_language
result = detect_language(path)
```

<a id="_looks_like_c_header-36"></a>

##### `_looks_like_c_header(path: str)` → `bool`

`code-analyzer/analyzer/parsers.py:36` · LOC **4** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `path` | `str` | `—` |

**Returns** `bool`

**Example**

```py
# _looks_like_c_header
result = _looks_like_c_header(path)
```

<a id="_match_n-40"></a>

##### `_match_n(text: str, pattern: str)` → `str`

`code-analyzer/analyzer/parsers.py:40` · LOC **5** · complexity **2** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `text` | `str` | `—` |
| `pattern` | `str` | `—` |

**Returns** `str`

**Example**

```py
# _match_n
result = _match_n(text, pattern)
```

<a id="analyze_file-45"></a>

##### `analyze_file(path: str, source: str)` → `FileAnalysis`

`code-analyzer/analyzer/parsers.py:45` · LOC **13** · complexity **5** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `path` | `str` | `—` |
| `source` | `str` | `—` |

**Returns** `FileAnalysis`

**Raises/Throws**: `ValueError`

**Example**

```py
# analyze_file
result = analyze_file(path, source)
```

<a id="_parse_python-70"></a>

##### `_parse_python(path: str, source: str)` → `FileAnalysis`

`code-analyzer/analyzer/parsers.py:70` · LOC **86** · complexity **14** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `path` | `str` | `—` |
| `source` | `str` | `—` |

**Returns** `FileAnalysis`

**Example**

```py
# _parse_python
result = _parse_python(path, source)
```

<a id="owning_class-90"></a>

##### `owning_class(line_no: int)` → `Optional[str]`

`code-analyzer/analyzer/parsers.py:90` · LOC **9** · complexity **3** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `line_no` | `int` | `—` |

**Returns** `Optional[str]`

**Example**

```py
# owning_class
result = owning_class(line_no)
```

<a id="_python_block_end-156"></a>

##### `_python_block_end(lines: list[str], start: int, indent: int)` → `int`

`code-analyzer/analyzer/parsers.py:156` · LOC **14** · complexity **4** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `lines` | `list[str]` | `—` |
| `start` | `int` | `—` |
| `indent` | `int` | `—` |

**Returns** `int`

**Example**

```py
# _python_block_end
result = _python_block_end(lines, start, indent)
```

<a id="_decorators_before-170"></a>

##### `_decorators_before(lines: list[str], idx: int)` → `str`

`code-analyzer/analyzer/parsers.py:170` · LOC **12** · complexity **3** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `lines` | `list[str]` | `—` |
| `idx` | `int` | `—` |

**Returns** `str`

**Example**

```py
# _decorators_before
result = _decorators_before(lines, idx)
```

<a id="_py_docstring-182"></a>

##### `_py_docstring(body: str)` → `Optional[str]`

`code-analyzer/analyzer/parsers.py:182` · LOC **5** · complexity **2** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `body` | `str` | `—` |

**Returns** `Optional[str]`

**Example**

```py
# _py_docstring
result = _py_docstring(body)
```

<a id="_py_params-187"></a>

##### `_py_params(raw: str)` → `list[Parameter]`

`code-analyzer/analyzer/parsers.py:187` · LOC **52** · complexity **14** · nesting **5**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `raw` | `str` | `—` |

**Returns** `list[Parameter]`

**Example**

```py
# _py_params
result = _py_params(raw)
```

<a id="_parse_java-257"></a>

##### `_parse_java(path: str, source: str)` → `FileAnalysis`

`code-analyzer/analyzer/parsers.py:257` · LOC **79** · complexity **13** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `path` | `str` | `—` |
| `source` | `str` | `—` |

**Returns** `FileAnalysis`

**Example**

```py
# _parse_java
result = _parse_java(path, source)
```

<a id="owning_class-280"></a>

##### `owning_class(pos: int)` → `Optional[str]`

`code-analyzer/analyzer/parsers.py:280` · LOC **9** · complexity **3** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `pos` | `int` | `—` |

**Returns** `Optional[str]`

**Example**

```py
# owning_class
result = owning_class(pos)
```

<a id="_parse_typescript-359"></a>

##### `_parse_typescript(path: str, source: str)` → `FileAnalysis`

`code-analyzer/analyzer/parsers.py:359` · LOC **95** · complexity **19** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `path` | `str` | `—` |
| `source` | `str` | `—` |

**Returns** `FileAnalysis`

**Example**

```py
# _parse_typescript
result = _parse_typescript(path, source)
```

<a id="owning_class-380"></a>

##### `owning_class(pos: int)` → `Optional[str]`

`code-analyzer/analyzer/parsers.py:380` · LOC **9** · complexity **3** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `pos` | `int` | `—` |

**Returns** `Optional[str]`

**Example**

```py
# owning_class
result = owning_class(pos)
```

<a id="_parse_cpp-470"></a>

##### `_parse_cpp(path: str, source: str)` → `FileAnalysis`

`code-analyzer/analyzer/parsers.py:470` · LOC **77** · complexity **15** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `path` | `str` | `—` |
| `source` | `str` | `—` |

**Returns** `FileAnalysis`

**Example**

```py
# _parse_cpp
result = _parse_cpp(path, source)
```

<a id="owning_class-484"></a>

##### `owning_class(pos: int)` → `Optional[str]`

`code-analyzer/analyzer/parsers.py:484` · LOC **9** · complexity **3** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `pos` | `int` | `—` |

**Returns** `Optional[str]`

**Example**

```py
# owning_class
result = owning_class(pos)
```

<a id="_cpp_params-547"></a>

##### `_cpp_params(raw: str)` → `list[Parameter]`

`code-analyzer/analyzer/parsers.py:547` · LOC **21** · complexity **5** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `raw` | `str` | `—` |

**Returns** `list[Parameter]`

**Example**

```py
# _cpp_params
result = _cpp_params(raw)
```

<a id="_java_ts_params-568"></a>

##### `_java_ts_params(raw: str)` → `list[Parameter]`

`code-analyzer/analyzer/parsers.py:568` · LOC **46** · complexity **13** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `raw` | `str` | `—` |

**Returns** `list[Parameter]`

**Example**

```py
# _java_ts_params
result = _java_ts_params(raw)
```

<a id="_build_function-614"></a>

##### `_build_function(*: any, name: str, file: str, line: int, end_line: int, params: list[Parameter], return_type, language: str, source: str, class_name = None, visibility = "public", is_static = False, is_abstract = False, is_constructor = False, docstring = None)` → `Function`

`code-analyzer/analyzer/parsers.py:614` · LOC **43** · complexity **2** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `` | `—` | `—` |
| `name` | `str` | `—` |
| `file` | `str` | `—` |
| `line` | `int` | `—` |
| `end_line` | `int` | `—` |
| `params` | `list[Parameter]` | `—` |
| `return_type` | `—` | `—` |
| `language` | `str` | `—` |
| `source` | `str` | `—` |
| `class_name` | `—` | `None` |
| `visibility` | `—` | `"public"` |
| `is_static` | `—` | `False` |
| `is_abstract` | `—` | `False` |
| `is_constructor` | `—` | `False` |
| `docstring` | `—` | `None` |

**Returns** `Function`

**Example**

```py
# _build_function
result = _build_function(, name, file, line, end_line, params, return_type, language, source, class_name, visibility, is_static, is_abstract, is_constructor, docstring)
```

<a id="_braces_end-657"></a>

##### `_braces_end(source: str, open_pos: int)` → `int`

`code-analyzer/analyzer/parsers.py:657` · LOC **31** · complexity **12** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |
| `open_pos` | `int` | `—` |

**Returns** `int`

**Example**

```py
# _braces_end
result = _braces_end(source, open_pos)
```

<a id="_offset_of_line_end-688"></a>

##### `_offset_of_line_end(source: str, line_no: int)` → `int`

`code-analyzer/analyzer/parsers.py:688` · LOC **8** · complexity **3** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |
| `line_no` | `int` | `—` |

**Returns** `int`

**Example**

```py
# _offset_of_line_end
result = _offset_of_line_end(source, line_no)
```

<a id="_block_comment_before-696"></a>

##### `_block_comment_before(source: str, pos: int)` → `Optional[str]`

`code-analyzer/analyzer/parsers.py:696` · LOC **7** · complexity **3** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |
| `pos` | `int` | `—` |

**Returns** `Optional[str]`

**Example**

```py
# _block_comment_before
result = _block_comment_before(source, pos)
```

---

### `analyzer/refactoring.py`

####  🔧 `class Refactoring`

<a id="Refactoring-suggest-20"></a>

##### `Refactoring.suggest(project, findings: list[SmellFinding])` → `list[Refactoring]`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:20` · LOC **28** · complexity **6** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `—` | `—` |
| `findings` | `list[SmellFinding]` | `—` |

**Returns** `list[Refactoring]`

**Example**

```py
obj = Refactoring()
result = obj.suggest(project, findings)
```

<a id="Refactoring-recipe_title-48"></a>

##### `Refactoring.recipe_title(smell_id: str)` → `str`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:48` · LOC **15** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `smell_id` | `str` | `—` |

**Returns** `str`

**Example**

```py
obj = Refactoring()
result = obj.recipe_title(smell_id)
```

<a id="Refactoring-_sig-63"></a>

##### `Refactoring._sig(fn: Function)` → `str`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:63` · LOC **16** · complexity **8** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `fn` | `Function` | `—` |

**Returns** `str`

**Example**

```py
obj = Refactoring()
result = obj._sig(fn)
```

<a id="Refactoring-_register-82"></a>

##### `Refactoring._register(smell_id)`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:82` · LOC **8** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `smell_id` | `—` | `—` |

**Example**

```py
obj = Refactoring()
result = obj._register(smell_id)
```

<a id="Refactoring-_long_function-91"></a>

##### `Refactoring._long_function(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:91` · LOC **37** · complexity **2** · nesting **3**

**Description**

)
        if fn.file.endswith(".py")
        else textwrap.dedent(
            f

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._long_function(f, fn)
```

<a id="Refactoring-_apply_business_rules-106"></a>

##### `Refactoring._apply_business_rules(data)`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:106` · LOC **2** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `data` | `—` | `—` |

**Example**

```py
obj = Refactoring()
result = obj._apply_business_rules(data)
```

<a id="Refactoring-_deep_nesting-129"></a>

##### `Refactoring._deep_nesting(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:129` · LOC **31** · complexity **1** · nesting **0**

**Description**

\
            def process(user, order):
                if user is not None:
                    if order is not None:
                        if order.paid:
                            if user.active:
                                ship(order)

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._deep_nesting(f, fn)
```

<a id="Refactoring-process-137"></a>

##### `Refactoring.process(user, order)`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:137` · LOC **6** · complexity **5** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `user` | `—` | `—` |
| `order` | `—` | `—` |

**Example**

```py
obj = Refactoring()
result = obj.process(user, order)
```

<a id="Refactoring-process-147"></a>

##### `Refactoring.process(user, order)`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:147` · LOC **8** · complexity **4** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `user` | `—` | `—` |
| `order` | `—` | `—` |

**Example**

```py
obj = Refactoring()
result = obj.process(user, order)
```

<a id="Refactoring-_too_many_params-161"></a>

##### `Refactoring._too_many_params(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:161` · LOC **31** · complexity **3** · nesting **3**

**Description**

)
        if fn.file.endswith(".py")
        else textwrap.dedent(
            f

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._too_many_params(f, fn)
```

<a id="Refactoring-_high_complexity-193"></a>

##### `Refactoring._high_complexity(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:193` · LOC **22** · complexity **1** · nesting **0**

**Description**

\
            HANDLERS = {
                "case_a": handle_a,
                "case_b": handle_b,
                "case_c": handle_c,
            }

            def dispatch(case, payload):
                return HANDLERS.get(case, default_handler)(payload)

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._high_complexity(f, fn)
```

<a id="Refactoring-dispatch-208"></a>

##### `Refactoring.dispatch(case, payload)`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:208` · LOC **2** · complexity **3** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `case` | `—` | `—` |
| `payload` | `—` | `—` |

**Example**

```py
obj = Refactoring()
result = obj.dispatch(case, payload)
```

<a id="Refactoring-_duplicate-216"></a>

##### `Refactoring._duplicate(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:216` · LOC **23** · complexity **1** · nesting **0**

**Description**

\
            # Move the shared logic into one place and delegate from both call sites:
            def shared_logic(...):
                    ...  # single canonical implementation

            def original_a(...):
                return shared_logic(...)

            def original_b(...):
                return shared_logic(...)

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._duplicate(f, fn)
```

<a id="Refactoring-shared_logic-226"></a>

##### `Refactoring.shared_logic(...)`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:226` · LOC **3** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `...` | `—` | `—` |

**Example**

```py
obj = Refactoring()
result = obj.shared_logic(...)
```

<a id="Refactoring-original_a-229"></a>

##### `Refactoring.original_a(...)`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:229` · LOC **3** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `...` | `—` | `—` |

**Example**

```py
obj = Refactoring()
result = obj.original_a(...)
```

<a id="Refactoring-original_b-232"></a>

##### `Refactoring.original_b(...)`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:232` · LOC **2** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `...` | `—` | `—` |

**Example**

```py
obj = Refactoring()
result = obj.original_b(...)
```

<a id="Refactoring-_empty_catch-240"></a>

##### `Refactoring._empty_catch(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:240` · LOC **26** · complexity **1** · nesting **0**

**Description**

\
            try:
                risky()
            except Exception:
                pass  # swallowed

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._empty_catch(f, fn)
```

<a id="Refactoring-_magic_number-267"></a>

##### `Refactoring._magic_number(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:267` · LOC **17** · complexity **1** · nesting **0**

**Description**

\
            MAX_CACHE_SECONDS = 86_400

            if len(items) > MAX_CACHE_SECONDS: ...

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._magic_number(f, fn)
```

<a id="Refactoring-_long_line-285"></a>

##### `Refactoring._long_line(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:285` · LOC **11** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._long_line(f, fn)
```

<a id="Refactoring-_print_debug-297"></a>

##### `Refactoring._print_debug(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:297` · LOC **11** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._print_debug(f, fn)
```

<a id="Refactoring-_todo-309"></a>

##### `Refactoring._todo(f: SmellFinding, fn: Function)` → `Refactoring`

member of `Refactoring` · `code-analyzer/analyzer/refactoring.py:309` · LOC **9** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `f` | `SmellFinding` | `—` |
| `fn` | `Function` | `—` |

**Returns** `Refactoring`

**Example**

```py
obj = Refactoring()
result = obj._todo(f, fn)
```

---

### `analyzer/report.py`

<a id="analyze_project-15"></a>

##### `analyze_project(root: str)` → `ProjectAnalysis`

`code-analyzer/analyzer/report.py:15` · LOC **4** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `root` | `str` | `—` |

**Returns** `ProjectAnalysis`

**Example**

```py
# analyze_project
result = analyze_project(root)
```

<a id="generate_quality_report-19"></a>

##### `generate_quality_report(project: ProjectAnalysis, findings)` → `str`

`code-analyzer/analyzer/report.py:19` · LOC **33** · complexity **5** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `ProjectAnalysis` | `—` |
| `findings` | `—` | `—` |

**Returns** `str`

**Example**

```py
# generate_quality_report
result = generate_quality_report(project, findings)
```

<a id="run-52"></a>

##### `run(root: str, out_dir: str = "docs/generated")` → `dict`

`code-analyzer/analyzer/report.py:52` · LOC **27** · complexity **2** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `root` | `str` | `—` |
| `out_dir` | `str` | `"docs/generated"` |

**Returns** `dict`

**Example**

```py
# run
result = run(root, out_dir)
```

<a id="_refactoring_doc-79"></a>

##### `_refactoring_doc(refactorings)` → `str`

`code-analyzer/analyzer/report.py:79` · LOC **19** · complexity **6** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `refactorings` | `—` | `—` |

**Returns** `str`

**Example**

```py
# _refactoring_doc
result = _refactoring_doc(refactorings)
```

<a id="_summary_line-98"></a>

##### `_summary_line(project, findings, refactorings, outputs)`

`code-analyzer/analyzer/report.py:98` · LOC **9** · complexity **2** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `—` | `—` |
| `findings` | `—` | `—` |
| `refactorings` | `—` | `—` |
| `outputs` | `—` | `—` |

**Example**

```py
# _summary_line
_summary_line(project, findings, refactorings, outputs)
```

---

### `analyzer/scanner.py`

<a id="scan-15"></a>

##### `scan(root: str, exclude_dirs = None)` → `ProjectAnalysis`

`code-analyzer/analyzer/scanner.py:15` · LOC **21** · complexity **8** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `root` | `str` | `—` |
| `exclude_dirs` | `—` | `None` |

**Returns** `ProjectAnalysis`

**Example**

```py
# scan
result = scan(root, exclude_dirs)
```

<a id="_supported-36"></a>

##### `_supported(filename: str)` → `bool`

`code-analyzer/analyzer/scanner.py:36` · LOC **8** · complexity **5** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `filename` | `str` | `—` |

**Returns** `bool`

**Example**

```py
# _supported
result = _supported(filename)
```

---

### `analyzer/smells.py`

####  🔧 `class SmellFinding`

<a id="SmellFinding-detect_smells-44"></a>

##### `SmellFinding.detect_smells(project: ProjectAnalysis)` → `list[SmellFinding]`

member of `SmellFinding` · `code-analyzer/analyzer/smells.py:44` · LOC **8** · complexity **2** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `ProjectAnalysis` | `—` |

**Returns** `list[SmellFinding]`

**Example**

```py
obj = SmellFinding()
result = obj.detect_smells(project)
```

<a id="SmellFinding-_severity-52"></a>

##### `SmellFinding._severity(score: int)` → `str`

member of `SmellFinding` · `code-analyzer/analyzer/smells.py:52` · LOC **8** · complexity **3** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `score` | `int` | `—` |

**Returns** `str`

**Example**

```py
obj = SmellFinding()
result = obj._severity(score)
```

<a id="SmellFinding-_function_smells-60"></a>

##### `SmellFinding._function_smells(fn: Function)` → `list[SmellFinding]`

member of `SmellFinding` · `code-analyzer/analyzer/smells.py:60` · LOC **48** · complexity **12** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `fn` | `Function` | `—` |

**Returns** `list[SmellFinding]`

**Example**

```py
obj = SmellFinding()
result = obj._function_smells(fn)
```

<a id="SmellFinding-add-64"></a>

##### `SmellFinding.add(smell_id: str, details: str, severity: str | None = None, line: int | None = None)`

member of `SmellFinding` · `code-analyzer/analyzer/smells.py:64` · LOC **16** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `smell_id` | `str` | `—` |
| `details` | `str` | `—` |
| `severity` | `str | None` | `None` |
| `line` | `int | None` | `None` |

**Example**

```py
obj = SmellFinding()
result = obj.add(smell_id, details, severity, line)
```

<a id="SmellFinding-_duplicates-108"></a>

##### `SmellFinding._duplicates(project: ProjectAnalysis)` → `list[SmellFinding]`

member of `SmellFinding` · `code-analyzer/analyzer/smells.py:108` · LOC **36** · complexity **6** · nesting **4**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `project` | `ProjectAnalysis` | `—` |

**Returns** `list[SmellFinding]`

**Example**

```py
obj = SmellFinding()
result = obj._duplicates(project)
```

<a id="SmellFinding-_normalize-144"></a>

##### `SmellFinding._normalize(source: str)` → `str`

member of `SmellFinding` · `code-analyzer/analyzer/smells.py:144` · LOC **10** · complexity **4** · nesting **2**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `source` | `str` | `—` |

**Returns** `str`

**Example**

```py
obj = SmellFinding()
result = obj._normalize(source)
```

<a id="SmellFinding-smell_summary-154"></a>

##### `SmellFinding.smell_summary(findings: list[SmellFinding])` → `dict`

member of `SmellFinding` · `code-analyzer/analyzer/smells.py:154` · LOC **8** · complexity **3** · nesting **3**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `findings` | `list[SmellFinding]` | `—` |

**Returns** `dict`

**Example**

```py
obj = SmellFinding()
result = obj.smell_summary(findings)
```

---

### `tests/test_analyzer.py`

####  🔧 `class Widget`

####  🔧 `class TestMetrics`

extends **unittest.TestCase**

####  🔧 `class TestParsers`

extends **unittest.TestCase**

####  🔧 `class TestSmells`

extends **unittest.TestCase**

####  🔧 `class TestEndToEnd`

extends **unittest.TestCase**

<a id="add-19"></a>

##### `add(a: int, b: int = 1)` → `int`

`code-analyzer/tests/test_analyzer.py:19` · LOC **7** · complexity **2** · nesting **2**

**Description**

Add two numbers.

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `a` | `int` | `—` |
| `b` | `int` | `1` |

**Returns** `int`

**Example**

```py
# add
result = add(a, b)
```

<a id="Widget-__init__-27"></a>

##### `Widget.__init__(name: str)`

member of `Widget` · `code-analyzer/tests/test_analyzer.py:27` · LOC **3** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `name` | `str` | `—` |

**Example**

```py
obj = Widget()
result = obj.__init__(name)
```

<a id="Widget-helper-31"></a>

##### `Widget.helper(x)`

member of `Widget` · `code-analyzer/tests/test_analyzer.py:31` · LOC **2** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `x` | `—` | `—` |

**Example**

```py
obj = Widget()
result = obj.helper(x)
```

<a id="TestMetrics-test_complexity_counts_branches-37"></a>

##### `TestMetrics.test_complexity_counts_branches()`

member of `TestMetrics` · `code-analyzer/tests/test_analyzer.py:37` · LOC **4** · complexity **1** · nesting **0**

**Example**

```py
obj = TestMetrics()
result = obj.test_complexity_counts_branches()
```

<a id="TestMetrics-test_comments_and_strings_stripped-41"></a>

##### `TestMetrics.test_comments_and_strings_stripped()`

member of `TestMetrics` · `code-analyzer/tests/test_analyzer.py:41` · LOC **4** · complexity **1** · nesting **0**

**Example**

```py
obj = TestMetrics()
result = obj.test_comments_and_strings_stripped()
```

<a id="TestMetrics-test_line_counts-45"></a>

##### `TestMetrics.test_line_counts()`

member of `TestMetrics` · `code-analyzer/tests/test_analyzer.py:45` · LOC **6** · complexity **1** · nesting **0**

**Example**

```py
obj = TestMetrics()
result = obj.test_line_counts()
```

<a id="TestMetrics-test_nesting-51"></a>

##### `TestMetrics.test_nesting()`

member of `TestMetrics` · `code-analyzer/tests/test_analyzer.py:51` · LOC **4** · complexity **1** · nesting **0**

**Example**

```py
obj = TestMetrics()
result = obj.test_nesting()
```

<a id="TestParsers-setUp-56"></a>

##### `TestParsers.setUp()`

member of `TestParsers` · `code-analyzer/tests/test_analyzer.py:56` · LOC **3** · complexity **1** · nesting **0**

**Example**

```py
obj = TestParsers()
result = obj.setUp()
```

<a id="TestParsers-_write-59"></a>

##### `TestParsers._write(name, src)`

member of `TestParsers` · `code-analyzer/tests/test_analyzer.py:59` · LOC **7** · complexity **2** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `name` | `—` | `—` |
| `src` | `—` | `—` |

**Example**

```py
obj = TestParsers()
result = obj._write(name, src)
```

<a id="TestParsers-test_language_detection-66"></a>

##### `TestParsers.test_language_detection()`

member of `TestParsers` · `code-analyzer/tests/test_analyzer.py:66` · LOC **8** · complexity **1** · nesting **0**

**Example**

```py
obj = TestParsers()
result = obj.test_language_detection()
```

<a id="TestParsers-test_python_parse-74"></a>

##### `TestParsers.test_python_parse()`

member of `TestParsers` · `code-analyzer/tests/test_analyzer.py:74` · LOC **18** · complexity **6** · nesting **0**

**Example**

```py
obj = TestParsers()
result = obj.test_python_parse()
```

<a id="TestParsers-test_java_parse-92"></a>

##### `TestParsers.test_java_parse()`

member of `TestParsers` · `code-analyzer/tests/test_analyzer.py:92` · LOC **20** · complexity **3** · nesting **0**

**Example**

```py
obj = TestParsers()
result = obj.test_java_parse()
```

<a id="TestParsers-test_typescript_parse-112"></a>

##### `TestParsers.test_typescript_parse()`

member of `TestParsers` · `code-analyzer/tests/test_analyzer.py:112` · LOC **17** · complexity **5** · nesting **0**

**Example**

```py
obj = TestParsers()
result = obj.test_typescript_parse()
```

<a id="TestParsers-test_cpp_parse-129"></a>

##### `TestParsers.test_cpp_parse()`

member of `TestParsers` · `code-analyzer/tests/test_analyzer.py:129` · LOC **19** · complexity **1** · nesting **0**

**Example**

```py
obj = TestParsers()
result = obj.test_cpp_parse()
```

<a id="TestSmells-_fn_from_source-149"></a>

##### `TestSmells._fn_from_source(src, filename = "m.py")`

member of `TestSmells` · `code-analyzer/tests/test_analyzer.py:149` · LOC **4** · complexity **1** · nesting **0**

**Parameters**

| Name | Type | Default |
|------|------|---------|
| `src` | `—` | `—` |
| `filename` | `—` | `"m.py"` |

**Example**

```py
obj = TestSmells()
result = obj._fn_from_source(src, filename)
```

<a id="TestSmells-test_smells_detected-153"></a>

##### `TestSmells.test_smells_detected()`

member of `TestSmells` · `code-analyzer/tests/test_analyzer.py:153` · LOC **14** · complexity **3** · nesting **3**

**Example**

```py
obj = TestSmells()
result = obj.test_smells_detected()
```

<a id="TestSmells-test_duplicates-167"></a>

##### `TestSmells.test_duplicates()`

member of `TestSmells` · `code-analyzer/tests/test_analyzer.py:167` · LOC **22** · complexity **2** · nesting **0**

**Example**

```py
obj = TestSmells()
result = obj.test_duplicates()
```

<a id="TestSmells-test_refactoring_suggestions_generated-189"></a>

##### `TestSmells.test_refactoring_suggestions_generated()`

member of `TestSmells` · `code-analyzer/tests/test_analyzer.py:189` · LOC **13** · complexity **4** · nesting **3**

**Example**

```py
obj = TestSmells()
result = obj.test_refactoring_suggestions_generated()
```

<a id="TestSmells-test_quality_report_renders-202"></a>

##### `TestSmells.test_quality_report_renders()`

member of `TestSmells` · `code-analyzer/tests/test_analyzer.py:202` · LOC **11** · complexity **2** · nesting **3**

**Example**

```py
obj = TestSmells()
result = obj.test_quality_report_renders()
```

<a id="TestEndToEnd-test_full_run_generates_docs-214"></a>

##### `TestEndToEnd.test_full_run_generates_docs()`

member of `TestEndToEnd` · `code-analyzer/tests/test_analyzer.py:214` · LOC **30** · complexity **3** · nesting **3**

**Example**

```py
obj = TestEndToEnd()
result = obj.test_full_run_generates_docs()
```

---
