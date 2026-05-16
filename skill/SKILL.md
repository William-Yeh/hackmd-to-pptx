---
name: hackmd-to-pptx
description: Use when converting HackMD/Marp markdown slides to PowerPoint presentations, or when merging multiple HackMD/Marp decks into one combined deck.
license: MIT
compatibility: Requires Python 3.9+, uv
metadata:
  author: William Yeh
  languages: python,javascript,java,kotlin,go,rust,ruby,php,sql,bash,yaml,html,cpp
---

# HackMD to PowerPoint Converter

Convert HackMD/Marp-style markdown slides to professional PowerPoint presentations.

## Invocation

### Basic Conversion

```bash
# Convert with explicit output name
uv run scripts/convert.py input.md output.pptx

# Output name defaults to input.pptx
uv run scripts/convert.py presentation.md
```

### Merging Multiple Decks

Combine several HackMD/Marp files into one deck where each input becomes a top-level section (`---`) and its slides become sub-slides (`----`):

```bash
uv run scripts/merge.py deck1.md deck2.md deck3.md -o merged.md
uv run scripts/merge.py deck1.md deck2.md -o merged.md --title "Combined Deck"
uv run scripts/merge.py deck1.md deck2.md -o merged.md --no-toc
```

The first input's frontmatter (theme, paginate, etc.) is preserved; `--title` overrides the `title:` field. Each deck's first H1 becomes the section title; if absent, the filename stem is used. Internal `---` sections inside an input deck are demoted to `----` (PowerPoint sections can't nest).

**Table of Contents (default on):** A TOC slide is emitted as the first section, listing every deck's title as a bullet. Its heading is the `--title` value, or deck 1's title if `--title` is absent. Pass `--no-toc` to suppress.

**Style preservation:** If deck 1 has a `<style>...</style>` block at the top of its body (between frontmatter and first heading), the block is lifted into the merged file's head verbatim. Style blocks in other input decks are discarded (same precedent as frontmatter).

**Synthetic cover slides:** Every input deck gets a synthetic `# Deck Title` cover slide prepended, even if the deck already starts with `# Title`. This guarantees PowerPoint section grouping works correctly regardless of how the input deck's first slide is structured (e.g. `# H1` + `## H2`).

**Input requirements:**
- Decks with content *before* their first H1 are rejected; remove the preamble or move the title to the top.
- Empty files are rejected.
- `---` lines inside fenced code blocks are preserved (they are not treated as slide separators).

## Configuration

Place `config.json` or `config.yaml` in the same directory as the markdown file:

```json
{
  "colors": {
    "accent": "0891B2",
    "codeBlock": "F1F5F9",
    "syntaxKeyword": "7C3AED",
    "syntaxString": "059669",
    "syntaxComment": "6B7280",
    "syntaxNumber": "DC2626",
    "syntaxFunction": "2563EB",
    "syntaxType": "D97706"
  },
  "fonts": {
    "header": "Trebuchet MS",
    "body": "Calibri",
    "code": "Consolas"
  }
}
```

**Colors:** 6-digit hex without `#`, all keys optional. **Fonts:** system font names, all keys optional.


