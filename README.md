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

Then install the Python runtime dependencies:

```bash
pip install python-pptx lxml PyYAML
```

### Manual Install

```bash
git clone https://github.com/William-Yeh/hackmd-to-pptx.git
cd hackmd-to-pptx
pip install -r requirements.txt
```

## Usage

After installing, try these prompts with your agent:

- `Convert my slides.md to a PowerPoint presentation`
- `Turn this HackMD markdown file into a PPTX`
- `Create a presentation from my Marp slides with syntax highlighting`

### CLI Usage

```bash
# Convert a file
python skill/scripts/convert.py input.md output.pptx

# Try the included example
python skill/scripts/convert.py examples/demo.md output.pptx

# Output name defaults to input.pptx
python skill/scripts/convert.py presentation.md
```

## Documentation

- **[skill/SKILL.md](skill/SKILL.md)** — Skill guide: syntax, config, output format
- **[skill/references/SETUP.md](skill/references/SETUP.md)** — Virtual environments, CI setup
- **[skill/references/SYNTAX.md](skill/references/SYNTAX.md)** — Full markdown syntax reference
- **[skill/references/TROUBLESHOOTING.md](skill/references/TROUBLESHOOTING.md)** — Common issues and solutions
- **[examples/](examples/)** — Sample markdown and config files

## Requirements

- Python 3.8+
- python-pptx, lxml, PyYAML (optional for YAML config)

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
