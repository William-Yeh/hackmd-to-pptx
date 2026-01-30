---
name: hackmd-to-pptx
description: Use when converting HackMD/Marp markdown slides to PowerPoint presentations.
license: MIT
compatibility: Requires Python 3.9+, uv
metadata:
  author: William Yeh
  version: "1.3.0"
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


