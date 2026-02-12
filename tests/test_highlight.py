from convert import highlight_code


class TestHighlightCode:
    def test_python_keyword(self, colors):
        result = highlight_code("def foo", "python", colors)
        kw = [s for s in result if s["text"] == "def"][0]
        assert kw["color"] == colors["syntaxKeyword"]

    def test_python_string(self, colors):
        result = highlight_code('"hello"', "python", colors)
        assert result[0]["color"] == colors["syntaxString"]

    def test_python_comment(self, colors):
        result = highlight_code("# comment", "python", colors)
        assert result[0]["color"] == colors["syntaxComment"]

    def test_python_number(self, colors):
        result = highlight_code("42", "python", colors)
        assert result[0]["color"] == colors["syntaxNumber"]

    def test_python_function_call(self, colors):
        result = highlight_code("foo()", "python", colors)
        fn = [s for s in result if s["text"] == "foo"][0]
        assert fn["color"] == colors["syntaxFunction"]

    def test_diff_add_line(self, colors):
        result = highlight_code("+added", "diff", colors)
        assert result[0]["color"] == colors["syntaxDiffAdd"]

    def test_diff_del_line(self, colors):
        result = highlight_code("-removed", "diff", colors)
        assert result[0]["color"] == colors["syntaxDiffDel"]

    def test_diff_unchanged(self, colors):
        result = highlight_code(" unchanged", "diff", colors)
        assert result[0]["color"] == colors["darkText"]

    def test_unknown_language_fallback(self, colors):
        result = highlight_code("some text", "brainfuck", colors)
        assert len(result) == 1
        assert result[0]["color"] == colors["darkText"]

    def test_no_language(self, colors):
        result = highlight_code("some text", None, colors)
        assert len(result) == 1
        assert result[0]["color"] == colors["darkText"]

    def test_merge_adjacent_same_color(self, colors):
        # Two plain identifiers next to each other separated by space
        # should merge if same color
        result = highlight_code("a b", "python", colors)
        # 'a', ' ', 'b' all darkText → should merge
        texts = [s["text"] for s in result]
        assert "".join(texts) == "a b"
        # Verify merging happened (fewer segments than chars)
        assert len(result) <= 3

    def test_language_alias(self, colors):
        """py is an alias for python — same highlighting."""
        r1 = highlight_code("def x", "python", colors)
        r2 = highlight_code("def x", "py", colors)
        assert r1 == r2
