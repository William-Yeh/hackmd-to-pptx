# HackMD to PowerPoint Converter

[![CI](https://github.com/William-Yeh/hackmd-to-pptx/actions/workflows/ci.yml/badge.svg)](https://github.com/William-Yeh/hackmd-to-pptx/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-compatible-blue)](https://agentskills.io)

Convert HackMD/Marp-style markdown slides to professional PowerPoint presentations with syntax highlighting and slide master support.

## Features

- **Full Markdown Support** — Bold, italic, code, links, checkboxes
- **Syntax Highlighting** — 20+ programming languages with customizable colors
- **Smart Layouts** — Auto-detects section vs content slides
- **Collapsible Sections** — Organize slides with `---` separators
- **Speaker Notes** — Preserve `note:` blocks for presenter view
- **Slide Master** — Edit once, apply to all slides
- **Custom Themes** — Configure colors and fonts via JSON/YAML


## Installation

### Recommended: `npx skills`

```bash
npx skills add William-Yeh/hackmd-to-pptx
```

Dependencies are managed automatically by `uv` — no `pip install` needed.

### Manual Install

```bash
git clone https://github.com/William-Yeh/hackmd-to-pptx.git
cd hackmd-to-pptx
uv sync
```

## Usage

After installing, try these prompts with your agent:

- `Convert my slides.md to a PowerPoint presentation`
- `Turn this HackMD markdown file into a PPTX`
- `Create a presentation from my Marp slides with syntax highlighting`

### CLI Usage

```bash
# Convert a file
uv run skill/scripts/convert.py input.md output.pptx

# Output name defaults to input.pptx
uv run skill/scripts/convert.py presentation.md
```

### Try the Example

The `examples/` directory contains ready-to-run files:

- `examples/demo.md` — sample markdown with all features demonstrated
- `examples/config.json` — sample JSON configuration
- `examples/config.yaml` — sample YAML configuration

```bash
uv run skill/scripts/convert.py examples/demo.md test-output.pptx
open test-output.pptx        # macOS
# xdg-open test-output.pptx  # Linux
# start test-output.pptx     # Windows
```

## Advanced Usage

### Batch Conversion

```bash
for file in slides/*.md; do
  uv run skill/scripts/convert.py "$file" "output/$(basename "$file" .md).pptx"
done
```

### Custom Color Schemes

Create a themed config and copy it as `config.json` before conversion:

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

For the full configuration schema (all color and font keys), see [skill/SKILL.md](skill/SKILL.md).

The converter looks for config files in this order: `config.json` → `config.yaml` → `config.yml` → built-in defaults.

### Slide Master

The generated PPTX uses real PowerPoint placeholders, so theme changes propagate automatically:

1. Open the PPTX in PowerPoint
2. Go to **View → Slide Master**
3. Edit "Title Slide" and "Title and Content" layouts
4. Changes apply to all slides

### Output Format

- **Aspect ratio:** 16:9 (10" × 5.625")
- **Section slides:** "Title Slide" layout
- **Content slides:** "Title and Content" layout
- **Sections:** collapsible groups derived from `---` separators

### Adding Language Support

Edit `skill/scripts/convert.py` to add new languages to the `SYNTAX_KEYWORDS` dictionary:

```python
SYNTAX_KEYWORDS = {
    # ... existing languages ...
    'elixir': ['def', 'defp', 'defmodule', 'do', 'end', 'if', 'else'],
    'ex': ['def', 'defp', 'defmodule', 'do', 'end', 'if', 'else'],  # alias
}
```

## Documentation

- **[skill/SKILL.md](skill/SKILL.md)** — Agent skill: conversion commands and configuration schema
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** — Common issues and solutions
- **[SYNTAX.md](SYNTAX.md)** — Full markdown syntax reference
- **[examples/](examples/)** — Sample markdown and config files

## Requirements

- Python 3.9+
- [uv](https://github.com/astral-sh/uv) (manages dependencies automatically)

## Updating

If installed via `npx skills`:

```bash
npx skills update William-Yeh/hackmd-to-pptx
```

If installed manually:

```bash
git pull origin main
uv sync --upgrade
```

## Uninstallation

```bash
rm -rf .venv/
uv cache clean
rm -rf /path/to/hackmd-to-pptx/
```

## Contributing

Contributions welcome. Fork, branch, change, add tests, open a PR.

## License

MIT — see [LICENSE](LICENSE).

## Author

William Yeh <william.pjyeh@gmail.com>

## Acknowledgments

- [python-pptx](https://python-pptx.readthedocs.io/) — PowerPoint generation library
- [HackMD](https://hackmd.io/) — Markdown collaboration platform
- [Marp](https://marp.app/) — Markdown presentation ecosystem
