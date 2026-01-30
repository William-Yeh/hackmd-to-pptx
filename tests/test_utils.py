from pptx.dml.color import RGBColor

from convert import hex_to_rgb, parse_inline_formatting


class TestHexToRgb:
    def test_six_char_hex(self):
        assert hex_to_rgb("1E2761") == RGBColor(0x1E, 0x27, 0x61)

    def test_with_hash_prefix(self):
        assert hex_to_rgb("#0891B2") == RGBColor(0x08, 0x91, 0xB2)

    def test_black(self):
        assert hex_to_rgb("000000") == RGBColor(0, 0, 0)

    def test_white(self):
        assert hex_to_rgb("FFFFFF") == RGBColor(255, 255, 255)

    def test_lowercase(self):
        assert hex_to_rgb("ff00aa") == RGBColor(255, 0, 170)


class TestParseInlineFormatting:
    def test_plain_text(self):
        result = parse_inline_formatting("hello world")
        assert result == [{"text": "hello world", "type": "text"}]

    def test_bold(self):
        result = parse_inline_formatting("some **bold** text")
        assert result[0] == {"text": "some ", "type": "text"}
        assert result[1] == {"text": "bold", "type": "bold"}
        assert result[2] == {"text": " text", "type": "text"}

    def test_italic(self):
        result = parse_inline_formatting("some _italic_ text")
        assert result[1] == {"text": "italic", "type": "italic"}

    def test_code(self):
        result = parse_inline_formatting("use `pip install` here")
        assert result[1] == {"text": "pip install", "type": "code"}

    def test_link(self):
        result = parse_inline_formatting("click [here](https://example.com)")
        link_seg = [s for s in result if s["type"] == "link"][0]
        assert link_seg["text"] == "here"
        assert link_seg["url"] == "https://example.com"

    def test_mixed_formatting(self):
        result = parse_inline_formatting("**bold** and _italic_")
        types = [s["type"] for s in result]
        assert "bold" in types
        assert "italic" in types

    def test_empty_string(self):
        result = parse_inline_formatting("")
        assert result == [{"text": "", "type": "text"}]
