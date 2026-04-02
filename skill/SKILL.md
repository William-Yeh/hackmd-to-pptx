---
name: hackmd-to-pptx
description: Use when converting HackMD/Marp markdown slides to PowerPoint presentations.
license: MIT
compatibility: Requires Python 3.8+, python-pptx, lxml, PyYAML
metadata:
  author: William Yeh
  version: "1.2.0"
  languages: python,javascript,java,kotlin,go,rust,ruby,php,sql,bash,yaml,html,cpp
---

# HackMD to PowerPoint Converter

Convert HackMD/Marp-style markdown slides to professional PowerPoint presentations.

## Quick Start

### Installation

```bash
npx skills add William-Yeh/hackmd-to-pptx
pip install python-pptx lxml PyYAML
```

See `references/SETUP.md` for virtual environment and CI setup.

### Basic Conversion

```bash
# Convert with explicit output name
python scripts/convert.py input.md output.pptx

# Output name defaults to input.pptx
python scripts/convert.py presentation.md
```

### With Custom Configuration

Create `config.json` in the same directory as the markdown file — it is auto-detected at runtime.

## Markdown Syntax

### Slide Structure

```markdown
---
# Section Title
### Optional Subtitle

Plain text for title slide.

----

## Content Slide

- Bullet point with **bold** and _italic_
- Inline `code` and [links](https://example.com)

note:
Speaker notes (presenter view only)
```

- `---` — Major section separator, creates collapsible groups
- `----` — Sub-slide within a section
- `# Title` — Section slide (Title Slide layout, no content placeholder)
- `## Title` — Content slide (Title and Content layout)

### Content Formatting

| Markdown | Result |
|----------|--------|
| `**bold**` | Bold text |
| `_italic_` | Italic text |
| `` `code` `` | Inline code (accent color) |
| `[text](url)` | Hyperlink |
| `[ ]` / `[x]` | Unchecked / checked checkbox |
| `- item` or `* item` | Bullet point |
| `1. item` | Numbered list item |

Lines without a `-`, `*`, or `1.` prefix render as plain text without bullets.

### Code Blocks

Specify language after the opening fence for syntax highlighting:

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

Supported languages: Python, JavaScript, TypeScript, Java, Kotlin, Go, Rust, Ruby, PHP, SQL, Bash, YAML, HTML, C++, diff.

See `references/SYNTAX.md` for the full language list and color defaults.

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

## Output Format

- **Aspect ratio:** 16:9 (10" × 5.625")
- **Section slides:** "Title Slide" layout (placeholder index 0)
- **Content slides:** "Title and Content" layout (placeholder index 1)
- **Sections:** collapsible groups derived from `---` separators
- **Placeholders:** real PowerPoint placeholders, enabling slide master customization

## Slide Master Support

Because content uses real placeholders:

1. Open the generated PPTX in PowerPoint
2. Go to **View → Slide Master**
3. Edit "Title Slide" and "Title and Content" layouts
4. **Changes propagate to all slides automatically**

## Tips

1. Start from `examples/demo.md` and modify it
2. Group related slides with `---` separators
3. Use `note:` blocks for presenter guidance
4. Make bulk style changes via Slide Master rather than regenerating

## References

- `references/SETUP.md` — Installation and environment setup
- `references/SYNTAX.md` — Full syntax reference and language list
- `references/TROUBLESHOOTING.md` — Common issues and solutions
- `references/advanced.md` — Batch conversion, custom languages, CI integration
