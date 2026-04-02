# Fix Templates
---

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
