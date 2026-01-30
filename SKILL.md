---
name: hackmd-to-pptx
description: Convert HackMD/Marp-style markdown to professional PowerPoint presentations with syntax highlighting, custom themes, and slide master support. Use when converting markdown slides to PPTX, creating presentations from markdown, or working with HackMD/Marp format.
license: MIT
compatibility: Requires Python 3.8+, python-pptx, lxml, PyYAML
metadata:
  author: William Yeh
  version: "1.0.0"
  languages: python,javascript,java,kotlin,go,rust,ruby,php,sql,bash,yaml,html,cpp
---

# HackMD to PowerPoint Converter

Convert HackMD/Marp-style markdown slides to professional PowerPoint presentations with full formatting support, syntax highlighting, and slide master compatibility.

## What This Skill Does

This skill converts markdown slide files into PowerPoint presentations with:

1. **Full Markdown Formatting** - Bold, italic, inline code, hyperlinks, checkboxes
2. **Syntax Highlighting** - Code blocks with language-specific coloring for 20+ languages
3. **Smart Slide Layouts** - Section slides and content slides with proper PowerPoint placeholders
4. **Collapsible Sections** - Organize related slides with `---` separators
5. **Speaker Notes** - Preserve `note:` blocks as presenter notes
6. **Slide Master Support** - Edit slide master to customize all slides at once
7. **Custom Themes** - Configure colors and fonts via JSON or YAML files

## Quick Start

### Installation

```bash
# Install Python dependencies
pip install python-pptx lxml PyYAML

# Or install to user directory
pip install --user python-pptx lxml PyYAML
```

See `references/SETUP.md` for detailed installation instructions including virtual environments.

### Basic Conversion

```bash
# Convert markdown to PowerPoint
python scripts/convert.py input.md output.pptx

# Use default output name (replaces .md with .pptx)
python scripts/convert.py presentation.md
```

### With Custom Configuration

Create `config.json` in the same directory as your markdown file:

```json
{
  "colors": {
    "accent": "0891B2",
    "codeBlock": "F1F5F9"
  },
  "fonts": {
    "header": "Arial",
    "body": "Calibri",
    "code": "Consolas"
  }
}
```

Then run the conversion as normal - the config will be automatically detected.

## Markdown Syntax

### Slide Separators

```markdown
---                  # Creates major section (collapsible group)
# Section Title
### Optional Subtitle

Plain text without bullets

----                 # Creates sub-slide within section

## Content Slide

- Bullet points here
```

- `---` (three hyphens) - Major section separator, creates collapsible groups
- `----` (four hyphens) - Sub-slide separator within a section

### Slide Types

**Section Slide** (Title Slide layout):
```markdown
# Main Title
### Subtitle

Plain text description without bullet prefixes.
This creates a title slide with no content placeholder.
```

**Content Slide** (Title and Content layout):
```markdown
## Slide Title

- Bullet point with **bold** and _italic_
- Inline `code` and [links](https://example.com)
- Checkboxes: [ ] Todo and [x] Done

note:
Speaker notes for presenter view (not visible on slide)
```

### Inline Formatting

| Markdown | Result | Notes |
|----------|--------|-------|
| `**bold**` | **Bold** text | Strong emphasis |
| `_italic_` | *Italic* text | Light emphasis |
| `` `code` `` | `Monospace` | Rendered in accent color |
| `[text](url)` | Clickable hyperlink | Opens in browser |
| `[ ]` | ☐ | Unchecked checkbox |
| `[x]` | ☑ | Checked checkbox |

### Code Blocks with Syntax Highlighting

Specify language for syntax highlighting:

````markdown
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

```javascript
const greet = (name) => `Hello, ${name}!`;
```

```diff
- old line (shown in red)
+ new line (shown in green)
```
````

**Supported Languages:**
- Python, JavaScript, TypeScript
- Java, Kotlin, Scala, Haskell
- Go, Rust, Ruby, Perl, PHP
- SQL, Bash/Shell
- YAML, JSON, HTML
- C++, diff format

**Highlighting Colors:**
- Keywords (if, def, class) → Purple
- Strings ("text") → Green
- Comments (# comment) → Gray
- Numbers (42) → Red
- Functions (myFunc) → Blue
- Types (String, int) → Orange

### Lists

```markdown
- Bullet item (gets • bullet)
- Another bullet
  - Nested bullet (indent with 2 spaces)

1. Numbered item
2. Another numbered item

Plain text line (NO bullet - no prefix needed)
```

**Important:** Only lines starting with `-`, `*`, or `1.` get bullets/numbers. Plain text without prefixes is intentionally displayed without bullets.

## Configuration

### Configuration Files

Place `config.json` or `config.yaml` in the same directory as your markdown file:

**config.json:**
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

**config.yaml:**
```yaml
colors:
  accent: "0891B2"
  codeBlock: "F1F5F9"
  syntaxKeyword: "7C3AED"
  syntaxString: "059669"
  syntaxComment: "6B7280"
  syntaxNumber: "DC2626"
  syntaxFunction: "2563EB"
  syntaxType: "D97706"

fonts:
  header: Trebuchet MS
  body: Calibri
  code: Consolas
```

### Color Configuration

- Use 6-digit hex codes **without** the `#` prefix
- All color keys are optional (defaults will be used for missing values)
- Colors must be valid hex format: `0-9A-F` (case insensitive)

**Available Color Keys:**
- `accent` - Inline code, highlights (default: `0891B2` - cyan)
- `codeBlock` - Code block background (default: `F1F5F9` - light gray)
- `syntaxKeyword` - Code keywords (default: `7C3AED` - purple)
- `syntaxString` - String literals (default: `059669` - green)
- `syntaxComment` - Comments (default: `6B7280` - gray)
- `syntaxNumber` - Numbers (default: `DC2626` - red)
- `syntaxFunction` - Function names (default: `2563EB` - blue)
- `syntaxType` - Type names (default: `D97706` - orange)

### Font Configuration

- Use system font names (fonts that exist on the target system)
- Fonts are optional (defaults will be used)

**Available Font Keys:**
- `header` - Slide titles (default: `Trebuchet MS`)
- `body` - Bullet points and paragraphs (default: `Calibri`)
- `code` - Code blocks (default: `Consolas`)

**Common System Fonts:**
- Windows: Arial, Calibri, Consolas, Trebuchet MS, Verdana
- macOS: Arial, Helvetica, Monaco, Menlo
- Cross-platform: Arial, Courier New, Times New Roman

See `examples/config.json` and `examples/config.yaml` for complete configuration examples.

## Output Format

Generated PowerPoint files have:

- **Aspect Ratio:** 16:9 (10" × 5.625")
- **Section Slides:** Use "Title Slide" layout (placeholder index 0)
- **Content Slides:** Use "Title and Content" layout (placeholder index 1)
- **Sections:** Collapsible groups based on `---` separators
- **Real Placeholders:** Content uses PowerPoint placeholders for slide master support

## Slide Master Support

Content is placed in **real PowerPoint placeholders**, meaning:

1. Open the generated PPTX in PowerPoint
2. Go to **View → Slide Master** (or 檢視 → 投影片母片)
3. Edit "Title Slide" layout for section slides
4. Edit "Title and Content" layout for content slides
5. **Changes to fonts, colors, positions propagate to ALL slides automatically**

This allows bulk customization without regenerating the file.

## Common Issues

### Bullets Not Showing

**Problem:** Text appears without bullet points

**Cause:** Only lines with `-` or `*` prefix get bullets (this is intentional)

**Solution:**
```markdown
## My Slide

- This gets a bullet ✓
- This also gets one ✓

This is plain text (no bullet) ✓
```

Plain text without prefixes is meant to appear without bullets for flexibility.

### Code Not Highlighted

**Problem:** Code block appears in monochrome

**Solutions:**
1. Specify language: ` ```python ` instead of ` ``` `
2. Check language is supported (see list above)
3. Ensure language name is lowercase: ` ```python ` not ` ```Python `

### Wrong Slide Layout

**Problem:** Section slide has bullet placeholder or vice versa

**Cause:** Layout choice is based on content structure

**Solution:** Section slides require:
```markdown
---
# Section Title
### Optional Subtitle

Plain text only (no bullets)
```

Content slides require:
```markdown
----
## Slide Title

- At least one bullet point
```

### Configuration Not Applied

**Problem:** Custom colors/fonts not showing in output

**Solutions:**
1. Place config file in **same directory** as markdown file
2. Name it exactly `config.json`, `config.yaml`, or `config.yml`
3. Verify JSON/YAML syntax is valid
4. Use 6-digit hex colors without `#` prefix
5. Ensure font names are valid system fonts

## Examples

Example files are provided in the `examples/` directory:

- `examples/demo.md` - Sample markdown with all features demonstrated
- `examples/config.json` - Sample JSON configuration
- `examples/config.yaml` - Sample YAML configuration

Try converting the demo:

```bash
python scripts/convert.py examples/demo.md test-output.pptx
open test-output.pptx  # macOS
# xdg-open test-output.pptx  # Linux
# start test-output.pptx  # Windows
```

## Tips & Best Practices

1. **Start with examples** - Copy `examples/demo.md` and modify it
2. **Use section breaks** - Group related slides with `---` separators
3. **Test incrementally** - Convert small sections first, then expand
4. **Leverage slide master** - Make bulk changes via slide master instead of regenerating
5. **Keep it simple** - Don't over-format markdown; let the converter handle styling
6. **Version control** - Keep markdown in git, generate PPTX on demand
7. **Consistent formatting** - Use either `-` or `*` for bullets, not both
8. **Speaker notes** - Use `note:` blocks for presenter guidance

## Advanced Usage

### Batch Conversion

Convert multiple files with a shell loop:

```bash
for file in slides/*.md; do
  python scripts/convert.py "$file" "output/$(basename "$file" .md).pptx"
done
```

### Custom Color Schemes

Create themed configs:

**dark-theme.json:**
```json
{
  "colors": {
    "accent": "00D9FF",
    "codeBlock": "1E1E1E",
    "syntaxKeyword": "C678DD",
    "syntaxString": "98C379",
    "syntaxComment": "5C6370"
  }
}
```

Copy as `config.json` before conversion for dark theme slides.

### Adding Language Support

Edit `scripts/convert.py` to add new languages to `SYNTAX_KEYWORDS` dictionary:

```python
SYNTAX_KEYWORDS = {
    # ... existing languages ...
    'elixir': ['def', 'defp', 'defmodule', 'do', 'end', 'if', 'else'],
    'ex': ['def', 'defp', 'defmodule', 'do', 'end', 'if', 'else'],  # alias
}
```

## Documentation

- **SKILL.md** (this file) - Main skill documentation
- **references/SETUP.md** - Detailed installation and environment setup
- **references/TROUBLESHOOTING.md** - Common issues and solutions
- **references/SYNTAX.md** - Complete markdown syntax reference
- **README.md** - Project overview

## Support & Contributing

For issues, questions, or contributions:

- **GitHub:** https://github.com/William-Yeh/hackmd-to-pptx
- **Issues:** Report bugs or request features
- **Pull Requests:** Contributions welcome

## License

MIT License - see LICENSE file for details.

## Author

William Yeh <william.pjyeh@gmail.com>
