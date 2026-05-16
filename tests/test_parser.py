from convert import parse_slide, parse_markdown


class TestParseSlide:
    def test_title(self):
        slide = parse_slide("## My Title\n\n- bullet")
        assert slide["title"] == "## My Title"

    def test_subtitle(self):
        slide = parse_slide("# Main\n### Sub")
        assert slide["subtitle"] == "Sub"

    def test_bullets(self):
        slide = parse_slide("## T\n- one\n- two")
        bullets = [c for c in slide["content"] if c["type"] == "bullet"]
        assert len(bullets) == 2
        assert bullets[0]["text"] == "one"

    def test_numbered_list(self):
        slide = parse_slide("## T\n1. first\n2. second")
        nums = [c for c in slide["content"] if c["type"] == "numbered"]
        assert len(nums) == 2
        assert nums[0]["number"] == "1"

    def test_code_block(self):
        slide = parse_slide("## T\n```python\nprint('hi')\n```")
        blocks = [c for c in slide["content"] if c["type"] == "codeblock"]
        assert len(blocks) == 1
        assert blocks[0]["lang"] == "python"
        assert blocks[0]["content"] == "print('hi')"

    def test_notes(self):
        slide = parse_slide("## T\nnote:\nSpeaker notes here")
        assert slide["notes"] == "Speaker notes here"

    def test_checkbox_unchecked(self):
        slide = parse_slide("## T\n- [ ] todo")
        assert slide["content"][0]["text"].startswith("☐")

    def test_checkbox_checked(self):
        slide = parse_slide("## T\n- [x] done")
        assert slide["content"][0]["text"].startswith("☑")

    def test_indented_bullet(self):
        slide = parse_slide("## T\n  - nested")
        assert slide["content"][0]["indent"] == 1

    def test_table_basic(self):
        md = (
            "## T\n"
            "| a | b |\n"
            "|---|---|\n"
            "| 1 | 2 |\n"
            "| 3 | 4 |\n"
        )
        slide = parse_slide(md)
        tables = [c for c in slide["content"] if c["type"] == "table"]
        assert len(tables) == 1
        assert tables[0]["header"] == ["a", "b"]
        assert tables[0]["rows"] == [["1", "2"], ["3", "4"]]

    def test_table_empty_cells(self):
        md = (
            "## T\n"
            "| 類型 | 我看到的問題 | 為什麼這是風險？ |\n"
            "|---|---|---|\n"
            "| 看不懂 |  |  |\n"
            "| 需求不明 |  |  |\n"
        )
        slide = parse_slide(md)
        table = next(c for c in slide["content"] if c["type"] == "table")
        assert table["header"] == ["類型", "我看到的問題", "為什麼這是風險？"]
        assert table["rows"][0] == ["看不懂", "", ""]
        assert table["rows"][1] == ["需求不明", "", ""]

    def test_table_alignment_separator_accepted(self):
        # GFM allows :--- / :---: / ---: in the separator row
        md = (
            "## T\n"
            "| a | b | c |\n"
            "|:---|:---:|---:|\n"
            "| L | C | R |\n"
        )
        slide = parse_slide(md)
        tables = [c for c in slide["content"] if c["type"] == "table"]
        assert len(tables) == 1
        assert tables[0]["rows"] == [["L", "C", "R"]]

    def test_table_escaped_pipe_in_cell(self):
        md = (
            "## T\n"
            "| a | b |\n"
            "|---|---|\n"
            r"| x \| y | z |"
            "\n"
        )
        slide = parse_slide(md)
        table = next(c for c in slide["content"] if c["type"] == "table")
        assert table["rows"][0] == ["x | y", "z"]

    def test_single_pipe_line_is_not_a_table(self):
        # Without a following separator row, a "| ... |" line stays as text
        md = "## T\n| not a table |\n- after"
        slide = parse_slide(md)
        assert not any(c["type"] == "table" for c in slide["content"])

    def test_single_column_table(self):
        md = (
            "## T\n"
            "| col |\n"
            "|---|\n"
            "| a |\n"
            "| b |\n"
        )
        slide = parse_slide(md)
        table = next(c for c in slide["content"] if c["type"] == "table")
        assert table["header"] == ["col"]
        assert table["rows"] == [["a"], ["b"]]

    def test_table_terminated_by_blank_line(self):
        md = (
            "## T\n"
            "| a | b |\n"
            "|---|---|\n"
            "| 1 | 2 |\n"
            "\n"
            "- bullet after table\n"
        )
        slide = parse_slide(md)
        table = next(c for c in slide["content"] if c["type"] == "table")
        assert table["rows"] == [["1", "2"]]
        bullets = [c for c in slide["content"] if c["type"] == "bullet"]
        assert len(bullets) == 1


class TestParseMarkdown:
    def test_frontmatter_removal(self):
        md = "---\ntype: slide\n---\n\n## Hello\n- world"
        slides = parse_markdown(md)
        # Should not have frontmatter as content
        assert all("type: slide" not in str(s) for s in slides)

    def test_section_splitting(self):
        md = "# Sec1\n\n---\n\n# Sec2"
        slides = parse_markdown(md)
        assert len(slides) == 2

    def test_sub_slide_splitting(self):
        md = "# Sec\n\n----\n\n## Sub"
        slides = parse_markdown(md)
        assert len(slides) == 2

    def test_section_detection(self):
        md = "# Section Only"
        slides = parse_markdown(md)
        assert slides[0]["is_section"] is True

    def test_section_with_bullets_is_content(self):
        md = "# Title\n\n- bullet"
        slides = parse_markdown(md)
        assert slides[0]["is_section"] is False

    def test_empty_slide_skipped(self):
        md = "# Sec\n\n---\n\n\n\n---\n\n# Sec2"
        slides = parse_markdown(md)
        # Empty section between two --- should be skipped
        assert len(slides) == 2

    def test_demo_md_slide_count(self):
        demo = (Path(__file__).resolve().parent.parent / "examples" / "demo.md").read_text()
        slides = parse_markdown(demo)
        # Verify we get the expected number of slides
        assert len(slides) >= 8


from pathlib import Path
