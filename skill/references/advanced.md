# Advanced
---

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
