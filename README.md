# HackMD to PowerPoint Converter

Convert HackMD/Marp-style markdown slides to professional PowerPoint presentations with syntax highlighting and slide master support.

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 📝 **Full Markdown Support** - Bold, italic, code, links, checkboxes
- 🎨 **Syntax Highlighting** - 20+ programming languages with customizable colors
- 🎯 **Smart Layouts** - Auto-detects section vs content slides
- 📂 **Collapsible Sections** - Organize slides with `---` separators
- 🎤 **Speaker Notes** - Preserve `note:` blocks for presenter view
- 🖼️ **Slide Master** - Edit once, apply to all slides
- ⚙️ **Custom Themes** - Configure colors and fonts via JSON/YAML

## Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/William-Yeh/hackmd-to-pptx.git
cd hackmd-to-pptx

# Install dependencies
pip install -r requirements.txt
```

Or install to user directory:

```bash
pip install --user python-pptx lxml PyYAML
```

### Basic Usage

```bash
# Convert markdown to PowerPoint
python convert.py input.md output.pptx

# Output name defaults to input.pptx
python convert.py presentation.md
```

### Try the Example

```bash
# Convert example slides
python convert.py examples/demo.md test-output.pptx

# Open result
open test-output.pptx  # macOS
# xdg-open test-output.pptx  # Linux
# start test-output.pptx  # Windows
```

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

- `---` - Creates section (collapsible group)
- `----` - Creates slide within section
- `# Title` - Section slide (title layout)
- `## Title` - Content slide (title + content layout)

### Code Blocks

````markdown
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```
````

**Supported Languages:**
Python, JavaScript, TypeScript, Java, Kotlin, Go, Rust, Ruby, PHP, SQL, Bash, YAML, HTML, C++, and more.

See `references/SYNTAX.md` for complete syntax reference.

## Configuration

Create `config.json` in the same directory as your markdown:

```json
{
  "colors": {
    "accent": "0891B2",
    "codeBlock": "F1F5F9",
    "syntaxKeyword": "7C3AED",
    "syntaxString": "059669"
  },
  "fonts": {
    "header": "Arial",
    "body": "Calibri",
    "code": "Consolas"
  }
}
```

Or use YAML format (`config.yaml`):

```yaml
colors:
  accent: "0891B2"
  codeBlock: "F1F5F9"

fonts:
  header: Arial
  body: Calibri
  code: Consolas
```

See `examples/config.json` and `examples/config.yaml` for complete examples.

## Output

Generated PowerPoint presentations include:

- **16:9 aspect ratio** (10" × 5.625")
- **Real placeholders** for slide master compatibility
- **Collapsible sections** based on `---` separators
- **Syntax-highlighted code blocks**
- **Formatted text** with bold, italic, links, checkboxes

### Slide Master Support

Content uses PowerPoint placeholders, so you can:

1. Open PPTX in PowerPoint
2. Go to **View → Slide Master**
3. Edit "Title Slide" and "Title and Content" layouts
4. **All slides update automatically**

Perfect for applying brand styles without regenerating files.

## Documentation

- **[SKILL.md](SKILL.md)** - Complete usage guide and API reference
- **[references/SETUP.md](references/SETUP.md)** - Installation and environment setup
- **[references/TROUBLESHOOTING.md](references/TROUBLESHOOTING.md)** - Common issues and solutions
- **[references/SYNTAX.md](references/SYNTAX.md)** - Complete markdown syntax reference
- **[examples/](examples/)** - Sample files and configurations

## Examples

Example files are in the `examples/` directory:

```bash
# View example markdown
cat examples/demo.md

# Convert with default settings
python convert.py examples/demo.md

# Convert with custom config
cp examples/config.json .
python convert.py examples/demo.md
```

## Requirements

- Python 3.8 or higher
- python-pptx
- lxml
- PyYAML (optional, for YAML config files)

## Common Issues

**Bullets not showing?**
- Only lines with `-` or `*` get bullets (intentional)
- Plain text has no prefix

**Code not highlighted?**
- Specify language: ` ```python ` not ` ``` `
- Use lowercase language names

**Config not applied?**
- Place `config.json` in same directory as markdown
- Use 6-digit hex colors WITHOUT `#` prefix
- Ensure valid JSON/YAML syntax

See [TROUBLESHOOTING.md](references/TROUBLESHOOTING.md) for more help.

## Contributing

Contributions welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

William Yeh <william.pjyeh@gmail.com>

## Acknowledgments

- [python-pptx](https://python-pptx.readthedocs.io/) - PowerPoint generation library
- [HackMD](https://hackmd.io/) - Markdown collaboration platform
- [Marp](https://marp.app/) - Markdown presentation ecosystem

## Links

- **GitHub:** https://github.com/William-Yeh/hackmd-to-pptx
- **Issues:** https://github.com/William-Yeh/hackmd-to-pptx/issues
- **AgentSkills.io:** Universal skill format for AI agents
