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
