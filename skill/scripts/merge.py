#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.9"
# dependencies = [
#   "PyYAML>=6.0",
# ]
# ///
"""Merge multiple HackMD/Marp decks into a single deck.

Each input deck becomes one top-level section (separated by `---`) in the
merged output. All slides inside a deck become `----` sub-slides under that
section, so the deck title is the sole horizontal pivot in the resulting
PowerPoint.

Usage:
    uv run scripts/merge.py deck1.md deck2.md deck3.md -o merged.md
    uv run scripts/merge.py *.md -o merged.md --title "Combined Deck"

Paths are resolved relative to the current working directory.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections.abc import Iterator
from pathlib import Path

import yaml

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
STYLE_BLOCK_RE = re.compile(r"<style>(.*?)</style>", re.DOTALL | re.IGNORECASE)


class MergeError(Exception):
    """Raised when an input deck cannot be safely merged."""


def split_frontmatter(text: str) -> tuple[str | None, str]:
    """Return (frontmatter_block_without_fences, body)."""
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text.lstrip("\n")
    return m.group(1), text[m.end():].lstrip("\n")


def _is_fence_line(line: str) -> bool:
    """Triple-backtick fence open/close. Matches convert.py:413."""
    return line.lstrip().startswith("```")


def _iter_lines_outside_fences(text: str) -> Iterator[tuple[int, str]]:
    """Yield (index, line) for each line outside a fenced code block."""
    in_fence = False
    for idx, line in enumerate(text.split("\n")):
        if _is_fence_line(line):
            in_fence = not in_fence
            continue
        if not in_fence:
            yield idx, line


def extract_style_block(body: str) -> tuple[str | None, str]:
    """Return (style_html, body_without_style).

    Lifts the first `<style>...</style>` block out of the body. The block must
    sit before the first `# ` heading (outside fenced code blocks) — only a
    top-of-deck style block is treated as deck-level theming. Inline `<style>`
    blocks deeper in the deck are left alone.

    Returns (None, body) if no qualifying style block is found.
    """
    first_h1_offset: int | None = None
    offset = 0
    for line in body.split("\n"):
        if not _is_fence_line(line) and line.startswith("# "):
            # Computed only via lines we've already walked, so accumulating
            # offset as we go keeps the slice boundary aligned with the body.
            first_h1_offset = offset
            break
        offset += len(line) + 1
    # NB: this loop can't reuse _iter_lines_outside_fences — that iterator
    # discards fence-toggle lines, but the offset accumulator needs every line
    # (including fences) to stay in sync with the source bytes.

    search_window = body if first_h1_offset is None else body[:first_h1_offset]
    m = STYLE_BLOCK_RE.search(search_window)
    if not m:
        return None, body

    style_html = m.group(0)
    cleaned = (body[:m.start()] + body[m.end():]).lstrip("\n")
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return style_html, cleaned


def override_title(frontmatter_yaml: str | None, new_title: str) -> str:
    """Return a YAML block with the top-level `title:` key set to new_title.

    Uses PyYAML to avoid regex-based mutation pitfalls (quoted values, comments,
    nested keys, flow style). The output is a top-level mapping with keys in
    insertion order; existing nested `title:` keys are left untouched.
    """
    data = yaml.safe_load(frontmatter_yaml) if frontmatter_yaml else None
    if not isinstance(data, dict):
        data = {}
    new_data: dict = {"title": new_title}
    for k, v in data.items():
        if k != "title":
            new_data[k] = v
    dumped = yaml.safe_dump(new_data, sort_keys=False, default_flow_style=False, allow_unicode=True)
    return dumped.rstrip("\n")


def _join_title_with_subtitle(h1: str, h2: str) -> str:
    """Combine an H1 and immediately-following H2 into one deck-title label.

    Uses U+FF5C (full-width vertical bar) to match the in-file convention used
    by decks that inline their subtitle, e.g. "Unit 1｜AI 副駕駛...". Keeps
    synthesised composites visually consistent with hand-authored ones.
    """
    return f"{h1}｜{h2}"


def derive_deck_title(body: str, fallback: str) -> str:
    """Return the deck's display title.

    Rules (in order):
      1. If the first H1 (outside fenced code blocks) is *immediately* followed
         by an `## H2` — with only blank lines in between — return the joined
         label produced by `_join_title_with_subtitle`. This handles the
         HackMD/Marp pattern where a cover slide splits title and subtitle
         across two heading levels:

             # Unit 3
             ## Context Management：讓 AI 看懂你的專案

      2. Otherwise return the first H1 alone.
      3. If no H1 exists outside fenced blocks, return `fallback`.

    "Immediately followed" deliberately ignores intervening blank lines (real
    decks usually have one between headings) but bails on any non-blank,
    non-H2 content — including paragraphs, lists, slide separators (`---`,
    `----`), HTML/Marp directive comments, or other heading levels — so we
    never pull a subtitle from an unrelated slide.
    """
    pending_h1: str | None = None
    for _, line in _iter_lines_outside_fences(body):
        if pending_h1 is not None:
            if not line.strip():
                continue
            if line.startswith("## "):
                return _join_title_with_subtitle(pending_h1, line[3:].strip())
            return pending_h1
        if line.startswith("# "):
            pending_h1 = line[2:].strip()
    return pending_h1 if pending_h1 is not None else fallback


def flatten_deck(body: str, deck_title: str) -> str:
    """Convert a single deck's body into a flat sequence of `----`-separated slides.

    Rules:
      1. Internal `---` section separators (lines outside fenced code blocks)
         are demoted to `----`. PowerPoint sections can't nest; this preserves
         slide content while making the deck title the only section boundary.
      2. The deck always begins with a synthetic H1-only cover slide
         (`# {deck_title}`) followed by `----`. This guarantees that
         convert.py's section detection (which only fires when a sub-slide's
         final heading is an H1) sees a clear section anchor — even if the
         deck's own first slide mixes `# H1` with `## H2`. The cost is one
         extra cover slide per deck.
      3. The result has its outer whitespace stripped; the caller joins decks
         with `\\n\\n---\\n\\n` for human readability of the merged file.

    Raises:
        MergeError: if the body has non-blank preamble before its first H1
            (e.g. a paragraph then a `# Title`). The two reasonable
            interpretations — synthesise a cover, or use the later H1 — both
            corrupt the deck. Caller must clean up the input.
    """
    lines = body.split("\n")
    first_meaningful: str | None = None
    has_h1 = False
    for idx, line in _iter_lines_outside_fences(body):
        if line == "---":
            lines[idx] = "----"
        if first_meaningful is None and line.strip():
            first_meaningful = line
        if line.startswith("# "):
            has_h1 = True

    if first_meaningful is None:
        return f"# {deck_title}"

    if not first_meaningful.startswith("# ") and has_h1:
        raise MergeError(
            "deck has content before its first H1; remove the preamble or "
            "move the `# Title` to the top of the file"
        )

    flattened = "\n".join(lines).strip()
    return f"# {deck_title}\n\n----\n\n{flattened}"


def build_toc_slide(merged_title: str, deck_titles: list[str]) -> str:
    """Return the TOC slide markdown body.

    Shape:
        # {merged_title}

        TOC
        - deck 1 title
        - deck 2 title
        ...

    Deck titles are emitted verbatim — markdown formatting in a deck's H1
    (e.g. `**bold**`, `[link](url)`) will render live in the TOC. This is
    deliberate: deck authors who format their titles probably want that
    formatting preserved. Callers wanting plain-text TOC entries should
    sanitise titles before passing them in.
    """
    bullets = "\n".join(f"- {t}" for t in deck_titles)
    return f"# {merged_title}\n\nTOC\n{bullets}"


def merge_decks(
    paths: list[Path],
    explicit_title: str | None,
    *,
    emit_toc: bool = True,
) -> str:
    """Merge decks at `paths` into one markdown string."""
    if not paths:
        raise ValueError("merge_decks requires at least one input path")

    first_fm: str | None = None
    first_style: str | None = None
    flattened_bodies: list[str] = []
    deck_titles: list[str] = []

    for idx, path in enumerate(paths):
        # Normalize CRLF/CR to LF so downstream byte-offset math (e.g. in
        # extract_style_block) can trust line breaks are single characters.
        raw = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
        fm, body = split_frontmatter(raw)
        style, body = extract_style_block(body)
        if idx == 0:
            first_fm = fm
            first_style = style
        deck_title = derive_deck_title(body, fallback=path.stem)
        deck_titles.append(deck_title)
        try:
            flattened_bodies.append(flatten_deck(body, deck_title))
        except MergeError as exc:
            raise MergeError(f"{path}: {exc}") from None

    sections: list[str] = []
    if emit_toc:
        toc_title = explicit_title if explicit_title is not None else deck_titles[0]
        sections.append(build_toc_slide(toc_title, deck_titles))
    sections.extend(flattened_bodies)
    merged_body = "\n\n---\n\n".join(sections)

    head_parts: list[str] = []
    if explicit_title is not None or first_fm is not None:
        fm_yaml = (
            override_title(first_fm, explicit_title)
            if explicit_title is not None
            else first_fm
        )
        head_parts.append(f"---\n{fm_yaml}\n---")
    if first_style is not None:
        head_parts.append(first_style)

    if head_parts:
        return "\n\n".join(head_parts) + "\n\n" + merged_body + "\n"
    return merged_body + "\n"


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("inputs", nargs="+", type=Path, help="Input deck markdown files (order preserved)")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output merged markdown file")
    parser.add_argument("--title", default=None, help="Override the `title:` field in the merged frontmatter")
    parser.add_argument(
        "--no-toc",
        dest="emit_toc",
        action="store_false",
        help="Suppress the auto-generated Table of Contents slide (emitted by default)",
    )
    args = parser.parse_args(argv)

    for p in args.inputs:
        if not p.is_file():
            print(f"error: input not found: {p}", file=sys.stderr)
            return 2
        if p.stat().st_size == 0:
            print(f"error: empty input file: {p}", file=sys.stderr)
            return 2

    title = args.title or None  # treat --title "" as if --title was not passed
    try:
        merged = merge_decks(args.inputs, explicit_title=title, emit_toc=args.emit_toc)
    except MergeError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    try:
        args.output.write_text(merged, encoding="utf-8")
    except OSError as exc:
        print(f"error: cannot write {args.output}: {exc}", file=sys.stderr)
        return 2
    print(f"merged {len(args.inputs)} deck(s) -> {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
