from pathlib import Path

import pytest

from convert import parse_markdown
from merge import (
    MergeError,
    _join_title_with_subtitle,
    build_toc_slide,
    derive_deck_title,
    extract_style_block,
    flatten_deck,
    main,
    merge_decks,
    override_title,
    split_frontmatter,
)


class TestSplitFrontmatter:
    def test_no_frontmatter(self):
        fm, body = split_frontmatter("# Title\n\ncontent")
        assert fm is None
        assert body == "# Title\n\ncontent"

    def test_with_frontmatter(self):
        fm, body = split_frontmatter("---\ntitle: Foo\ntheme: x\n---\n\n# Title")
        assert fm == "title: Foo\ntheme: x"
        assert body == "# Title"

    def test_empty_input(self):
        fm, body = split_frontmatter("")
        assert fm is None
        assert body == ""


class TestOverrideTitle:
    def test_replaces_existing_title(self):
        out = override_title("title: Old\ntheme: x", "New")
        assert "title: New" in out
        assert "theme: x" in out
        assert "title: Old" not in out

    def test_replaces_quoted_title(self):
        out = override_title('title: "Old"\ntheme: x', "New")
        assert "title: New" in out
        assert "Old" not in out

    def test_adds_title_when_absent(self):
        out = override_title("theme: x\npaginate: true", "Brand New")
        assert out.startswith("title: Brand New")
        assert "theme: x" in out

    def test_leaves_nested_title_alone(self):
        out = override_title("meta:\n  title: nested\ntheme: x", "TopLevel")
        assert "title: TopLevel" in out
        assert "nested" in out

    def test_none_input(self):
        assert override_title(None, "Solo") == "title: Solo"

    def test_title_appears_first(self):
        out = override_title("theme: x\nother: y", "First")
        assert out.splitlines()[0] == "title: First"


class TestJoinTitleWithSubtitle:
    def test_uses_fullwidth_vertical_bar(self):
        # Pin the in-file convention for the separator. If we ever swap
        # the glyph (｜ → ：, em dash, etc.), this is the single test to
        # update; integration tests below assert behavior rather than
        # the literal character.
        assert _join_title_with_subtitle("A", "B") == "A｜B"


class TestDeriveDeckTitle:
    """Tests for the title-derivation rule.

    The parametrized `test_join_rule` table covers the H1±H2 combination
    matrix: when the next non-blank line after the H1 is `## H2`, the result
    is the joined label; otherwise it's the H1 alone. Each row's id documents
    the authoring pattern in the wild. Fence-handling and fallback cases
    document distinct invariants and stay as named tests below.
    """

    _JOIN_RULE_CASES = [
        pytest.param(
            "# Unit 3\n\n## Context Management",
            _join_title_with_subtitle("Unit 3", "Context Management"),
            id="hackmd-split-title-pattern",
        ),
        pytest.param(
            "# A\n\n\n## B",
            _join_title_with_subtitle("A", "B"),
            id="multiple-blank-lines-between-headings",
        ),
        pytest.param(
            "# Real Title\n\nparagraph here",
            "Real Title",
            id="non-heading-content-after-h1",
        ),
        pytest.param(
            "# Real Title",
            "Real Title",
            id="end-of-body-h1",
        ),
        pytest.param(
            "# Real Title\n\nsome intro text\n\n## later subtitle",
            "Real Title",
            id="paragraph-then-h2-belongs-to-different-slide",
        ),
        pytest.param(
            "# A\n\n### sub-sub",
            "A",
            id="h3-is-not-a-subtitle",
        ),
        pytest.param(
            "# Real Title\n\n<!-- _class: lead -->\n\n## later subtitle",
            "Real Title",
            id="marp-html-directive-bails",
        ),
        pytest.param(
            "# Real Title\n\n---\n\n## later subtitle",
            "Real Title",
            id="slide-separator-bails",
        ),
        pytest.param(
            "# Real Title\n\n----\n\n## later subtitle",
            "Real Title",
            id="sub-slide-separator-bails",
        ),
    ]

    @pytest.mark.parametrize("body,expected", _JOIN_RULE_CASES)
    def test_join_rule(self, body, expected):
        assert derive_deck_title(body, "fb") == expected

    def test_no_h1_uses_fallback(self):
        assert derive_deck_title("## only h2\ntext", "fb") == "fb"

    def test_skips_h1_inside_fence(self):
        body = "```md\n# Fake H1\n```\n\n## Real first slide\n"
        assert derive_deck_title(body, "fb") == "fb"

    def test_finds_h1_after_fenced_block(self):
        body = "```md\n# Fake H1\n```\n\n# Real Title\n"
        assert derive_deck_title(body, "fb") == "Real Title"

    def test_unterminated_fence_skips_everything_after(self):
        # Fail-soft: an unterminated fence is treated as if the rest of the
        # body is inside the fence. The alternative would silently misidentify
        # an H1 that the author intended as code.
        body = "```md\n# Inside\n\n# Also inside"
        assert derive_deck_title(body, "fb") == "fb"


class TestFlattenDeck:
    def test_demotes_internal_section_separator(self):
        body = "# Cover\n\n## A\n\n---\n\n## B"
        out = flatten_deck(body, "fb")
        # Behavioural check: after flatten + parse, the deck has exactly one
        # section (the synthetic cover), with the internal `---` collapsed.
        slides = parse_markdown(out)
        sections = {s["section"] for s in slides}
        assert sections == {"fb"}

    def test_prepends_synthetic_cover_even_with_leading_h1(self):
        # The synthetic cover guarantees section detection regardless of the
        # input deck's first-slide shape (convert.py only fires section
        # detection when a sub-slide's final heading is H1).
        body = "# Cover\n\n## first"
        out = flatten_deck(body, "Synthetic")
        assert out.startswith("# Synthetic\n\n----\n\n# Cover")

    def test_preamble_before_h1_raises(self):
        body = "Some preamble\n\n# Real\n\n## slide"
        with pytest.raises(MergeError, match="preamble"):
            flatten_deck(body, "fb")

    def test_no_h1_synthesises_cover(self):
        body = "## only content\n- bullet"
        out = flatten_deck(body, "synth")
        assert out.startswith("# synth\n\n----\n\n## only content")

    def test_dashes_inside_fence_preserved(self):
        body = "# Cover\n\n```yaml\n---\nkey: val\n---\n```\n\n----\n\n## next"
        out = flatten_deck(body, "fb")
        # The fenced `---` lines must survive demotion.
        assert "---\nkey: val\n---" in out
        # `----` count: 1 from the synthetic-cover separator, 1 from the
        # original sub-slide boundary in the input.
        assert out.count("----") == 2

    def test_empty_body_emits_bare_cover(self):
        assert flatten_deck("", "mydeck") == "# mydeck"


class TestMergeDecks:
    def test_three_decks_produce_three_sections(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d3 = tmp_path / "d3.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text("# Deck Two\n\n----\n\n## 2.1")
        d3.write_text("# Deck Three\n\n----\n\n## 3.1")
        merged = merge_decks([d1, d2, d3], explicit_title=None)
        slides = parse_markdown(merged)
        sections = [s for s in slides if s["is_section"]]
        assert len(sections) == 3
        assert [s["section"] for s in sections] == ["Deck One", "Deck Two", "Deck Three"]

    def test_first_decks_frontmatter_preserved(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d1.write_text("---\ntitle: Original\ntheme: gaia\n---\n\n# Deck One\n\n----\n\n## 1.1")
        d2.write_text("# Deck Two\n\n----\n\n## 2.1")
        merged = merge_decks([d1, d2], explicit_title="Combined")
        assert merged.startswith("---\n")
        head, _, _ = merged.partition("\n---\n")
        assert "title: Combined" in head
        assert "theme: gaia" in head

    def test_second_decks_frontmatter_discarded(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text("---\ntitle: Should Vanish\n---\n\n# Deck Two\n\n----\n\n## 2.1")
        merged = merge_decks([d1, d2], explicit_title=None)
        assert "Should Vanish" not in merged

    def test_filename_stem_fallback_for_missing_h1(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "fallback_stem.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text("## Slide without leading H1")
        merged = merge_decks([d1, d2], explicit_title=None)
        slides = parse_markdown(merged)
        sections = [s["section"] for s in slides if s["is_section"]]
        assert "fallback_stem" in sections

    def test_internal_section_flattened_to_sub_slide(self, tmp_path):
        d = tmp_path / "deck.md"
        d.write_text(
            "# Deck One\n\n----\n\n## 1.1\n\n---\n\n# Internal\n\n----\n\n## 1.2"
        )
        merged = merge_decks([d], explicit_title=None)
        slides = parse_markdown(merged)
        sections = [s for s in slides if s["is_section"]]
        assert len(sections) == 1
        assert sections[0]["section"] == "Deck One"
        titles = [s["title"] for s in slides]
        assert "# Internal" in titles


class TestExtractStyleBlock:
    def test_no_style(self):
        style, body = extract_style_block("# Title\n\ncontent")
        assert style is None
        assert body == "# Title\n\ncontent"

    def test_top_of_deck_style_extracted(self):
        body = "<style>\n.foo { color: red; }\n</style>\n\n# Title\n\ncontent"
        style, cleaned = extract_style_block(body)
        assert style == "<style>\n.foo { color: red; }\n</style>"
        assert cleaned.startswith("# Title")

    def test_style_after_first_h1_left_alone(self):
        body = "# Title\n\n<style>.inline { }</style>\n\nmore"
        style, cleaned = extract_style_block(body)
        assert style is None
        assert "<style>" in cleaned

    def test_multiline_style_with_braces(self):
        body = (
            "<style>\n"
            ".reveal .slides h1 {\n    color: #FFC500;\n}\n"
            ".reveal .slides code {\n    font-size: 24px;\n}\n"
            "</style>\n\n# Title"
        )
        style, _ = extract_style_block(body)
        assert style is not None
        assert "color: #FFC500" in style
        assert "font-size: 24px" in style


class TestBuildTocSlide:
    def test_shape(self):
        out = build_toc_slide("My Title", ["A", "B", "C"])
        assert out == "# My Title\n\nTOC\n- A\n- B\n- C"

    def test_single_deck(self):
        out = build_toc_slide("Solo", ["Only"])
        assert out == "# Solo\n\nTOC\n- Only"


class TestTocIntegration:
    def test_toc_emitted_by_default(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text("# Deck Two\n\n----\n\n## 2.1")
        merged = merge_decks([d1, d2], explicit_title="Combined")
        assert "TOC\n- Deck One\n- Deck Two" in merged
        # Section ordering is covered by test_toc_produces_distinct_pptx_sections.

    def test_no_toc_flag_suppresses(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text("# Deck Two\n\n----\n\n## 2.1")
        merged = merge_decks([d1, d2], explicit_title=None, emit_toc=False)
        assert "TOC\n-" not in merged

    def test_toc_title_falls_back_to_deck_one(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text("# Deck Two\n\n----\n\n## 2.1")
        merged = merge_decks([d1, d2], explicit_title=None)
        # No explicit title; TOC heading should use deck 1's derived title.
        toc_index = merged.find("TOC\n")
        h1_before_toc = merged.rfind("# ", 0, toc_index)
        toc_heading_line = merged[h1_before_toc:].splitlines()[0]
        assert toc_heading_line == "# Deck One"

    def test_toc_produces_distinct_pptx_sections(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d3 = tmp_path / "d3.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text("# Deck Two\n\n----\n\n## 2.1")
        d3.write_text("# Deck Three\n\n----\n\n## 3.1")
        merged = merge_decks([d1, d2, d3], explicit_title="Combined")
        slides = parse_markdown(merged)
        section_order: list[str | None] = []
        for s in slides:
            if not section_order or section_order[-1] != s["section"]:
                section_order.append(s["section"])
        assert section_order == ["Combined", "Deck One", "Deck Two", "Deck Three"]

    def test_style_block_extracted_from_deck_one(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d1.write_text(
            "---\ntitle: A\n---\n\n<style>\n.foo { color: red; }\n</style>\n\n"
            "# Deck One\n\n----\n\n## 1.1"
        )
        d2.write_text("# Deck Two\n\n----\n\n## 2.1")
        merged = merge_decks([d1, d2], explicit_title=None)
        # Structural: split at the frontmatter close-fence, then check the body
        # opens with the <style> block before any TOC heading.
        assert merged.startswith("---\n")
        _, _, body = merged.partition("\n---\n")
        body = body.lstrip()
        assert body.startswith("<style>")
        assert "</style>" in body
        style_end = body.index("</style>") + len("</style>")
        assert "TOC" in body[style_end:]

    def test_style_block_from_deck_two_discarded(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text(
            "<style>\n.discarded { color: red; }\n</style>\n\n"
            "# Deck Two\n\n----\n\n## 2.1"
        )
        merged = merge_decks([d1, d2], explicit_title=None)
        assert "<style>" not in merged
        assert "discarded" not in merged


class TestMainCli:
    def test_rejects_missing_input(self, tmp_path, capsys):
        out = tmp_path / "out.md"
        rc = main(["does-not-exist.md", "-o", str(out)])
        assert rc == 2
        assert "not found" in capsys.readouterr().err

    def test_rejects_empty_input(self, tmp_path, capsys):
        empty = tmp_path / "empty.md"
        empty.write_text("")
        out = tmp_path / "out.md"
        rc = main([str(empty), "-o", str(out)])
        assert rc == 2
        assert "empty" in capsys.readouterr().err

    def test_reports_preamble_error_with_filename(self, tmp_path, capsys):
        bad = tmp_path / "bad.md"
        bad.write_text("preamble paragraph\n\n# Title later\n\n## slide")
        out = tmp_path / "out.md"
        rc = main([str(bad), "-o", str(out)])
        assert rc == 2
        err = capsys.readouterr().err
        assert "bad.md" in err
        assert "preamble" in err

    def test_happy_path_writes_output(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text("# Deck Two\n\n----\n\n## 2.1")
        out = tmp_path / "merged.md"
        rc = main([str(d1), str(d2), "-o", str(out), "--title", "Combined"])
        assert rc == 0
        merged = out.read_text()
        assert merged.startswith("---\n")
        assert "title: Combined" in merged
        assert "TOC\n- Deck One\n- Deck Two" in merged

    def test_no_toc_flag(self, tmp_path):
        d1 = tmp_path / "d1.md"
        d2 = tmp_path / "d2.md"
        d1.write_text("# Deck One\n\n----\n\n## 1.1")
        d2.write_text("# Deck Two\n\n----\n\n## 2.1")
        out = tmp_path / "merged.md"
        rc = main([str(d1), str(d2), "-o", str(out), "--no-toc"])
        assert rc == 0
        assert "TOC\n-" not in out.read_text()

    def test_empty_title_treated_as_absent(self, tmp_path):
        # Regression: `--title ""` must not produce `---\nNone\n---` in the
        # merged frontmatter. Empty string collapses to None at the CLI boundary.
        d = tmp_path / "d.md"
        d.write_text("# Deck One\n\n----\n\n## 1.1")
        out = tmp_path / "merged.md"
        rc = main([str(d), "-o", str(out), "--title", ""])
        assert rc == 0
        merged = out.read_text()
        assert "None" not in merged.splitlines()

    def test_crlf_input_handled(self, tmp_path):
        # Regression: CRLF-encoded input must not break extract_style_block's
        # byte-offset accumulator or the fence-aware demotion.
        d = tmp_path / "d.md"
        body = (
            "<style>\r\n.foo { color: red; }\r\n</style>\r\n\r\n"
            "# Deck One\r\n\r\n----\r\n\r\n## 1.1\r\n"
        )
        d.write_bytes(body.encode("utf-8"))
        out = tmp_path / "merged.md"
        rc = main([str(d), "-o", str(out)])
        assert rc == 0
        merged = out.read_text()
        assert "\r" not in merged
        assert "<style>" in merged
        assert ".foo { color: red; }" in merged
        slides = parse_markdown(merged)
        assert any(s["section"] == "Deck One" for s in slides)

    def test_output_is_directory(self, tmp_path, capsys):
        # Regression: --output pointing at a directory must surface a clean
        # `error: cannot write ...` message, not a raw traceback.
        d = tmp_path / "d.md"
        d.write_text("# Deck One\n\n----\n\n## 1.1")
        rc = main([str(d), "-o", str(tmp_path)])
        assert rc == 2
        assert "cannot write" in capsys.readouterr().err

    def test_output_parent_missing(self, tmp_path, capsys):
        d = tmp_path / "d.md"
        d.write_text("# Deck One\n\n----\n\n## 1.1")
        missing_parent = tmp_path / "nonexistent" / "merged.md"
        rc = main([str(d), "-o", str(missing_parent)])
        assert rc == 2
        assert "cannot write" in capsys.readouterr().err
