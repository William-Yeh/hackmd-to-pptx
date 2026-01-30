# Complete Markdown Syntax Reference

Comprehensive guide to markdown syntax supported by the HackMD to PowerPoint converter.

## Document Structure

### Slide Separators

| Separator | Purpose | Creates |
|-----------|---------|---------|
| `---` | Major section | Collapsible section group in PowerPoint |
| `----` | Sub-slide | Individual slide within current section |

**Example:**
```markdown
---
# Section 1: Introduction

This is the section slide (title slide layout).

----

## First Content Slide

- Bullet point one
- Bullet point two

----

## Second Content Slide

- More content here

---

# Section 2: Details

New section starts here.
```

**Output:** Two collapsible sections, each containing slides.

### YAML Frontmatter (Auto-Stripped)

If your markdown has YAML frontmatter, it will be automatically stripped:

```markdown
---
title: My Presentation
author: Jane Doe
date: 2024-01-30
---

# First Actual Slide

Content starts here.
```

The frontmatter between the first `---` pair is removed before processing.

## Slide Types

### Section Slide (Title Slide Layout)

**Requirements:**
- Single `#` heading (H1)
- Optional `###` subtitle (H3)
- NO bullet points
- Plain text only

**Syntax:**
```markdown
---
# Main Section Title
### Optional Subtitle or Tagline

You can add plain descriptive text here.
No bullets, just paragraphs.
```

**PowerPoint Layout:** Uses "Title Slide" layout (index 0)

**Placeholders:**
- Title placeholder: H1 text
- Subtitle placeholder: H3 text + plain text

### Content Slide (Title and Content Layout)

**Requirements:**
- Double `##` heading (H2)
- Can have bullets, code, lists, plain text

**Syntax:**
```markdown
----

## Content Slide Title

- Bullet point one
- Bullet point two

Plain text paragraph.

More content...
```

**PowerPoint Layout:** Uses "Title and Content" layout (index 1)

**Placeholders:**
- Title placeholder: H2 text
- Content placeholder: Body content

## Text Formatting

### Headers

| Markdown | Usage | PowerPoint Result |
|----------|-------|-------------------|
| `# Text` | Section title | Title slide, large font |
| `## Text` | Slide title | Content slide title |
| `### Text` | Subtitle | Smaller text below title |
| `#### Text` | Not recommended | Treated as plain text |

**Best Practice:** Use only `#`, `##`, and `###`.

### Emphasis

| Markdown | Result | Visual |
|----------|--------|--------|
| `**bold text**` | Bold | **bold text** |
| `_italic text_` | Italic | *italic text* |
| `***bold italic***` | Bold + Italic | ***bold italic*** |

**Important:** No spaces between markers and text.

✅ Correct: `**bold**`
❌ Wrong: `** bold **`

### Inline Code

```markdown
Use `backticks` for inline code
```

**Result:** Monospace font in accent color (default: cyan)

**Rules:**
- One backtick on each side: `` `code` ``
- No spaces: `` `word` `` not `` ` word ` ``
- Accent color from config (default: `0891B2`)

### Hyperlinks

```markdown
[Link text](https://example.com)
[Click here](https://google.com)
```

**Result:** Clickable hyperlink in PowerPoint

**Rules:**
- Format: `[text](URL)`
- URL must be complete: `https://example.com`
- Text is what's displayed on slide
- No spaces between `]` and `(`

**Note:** Plain URLs are NOT auto-linked. You must use the `[text](url)` format.

### Strikethrough (Limited Support)

```markdown
~~strikethrough~~
```

**Status:** Not fully supported. May appear as plain text.

## Lists

### Bullet Lists

```markdown
- First level bullet
- Another first level
  - Second level (indent 2 spaces)
  - Another second level
    - Third level (indent 4 spaces)
```

**Result:** Nested bullets with proper indentation

**Bullet Markers:**
- First level: `•` (filled circle)
- Second level: `◦` (hollow circle)
- Third level: `▪` (filled square)

**Alternative:** Use `*` instead of `-`:
```markdown
* First bullet
* Second bullet
  * Nested bullet
```

**Important:** ONLY lines with `-` or `*` prefix get bullets.

### Numbered Lists

```markdown
1. First item
2. Second item
3. Third item
   - Nested bullet under number 3
4. Fourth item
```

**Result:** Automatically numbered list

**Rules:**
- Start with `1.`, `2.`, etc.
- Can nest bullets under numbers
- Numbers auto-increment in PowerPoint

### Plain Text (No Bullets)

```markdown
## My Slide

This is plain text without a bullet.
This is another line without a bullet.

- Now this has a bullet
- And this one too

Back to plain text without bullets.
```

**Key Point:** No prefix = no bullet. This is intentional for flexibility.

## Code Blocks

### Basic Code Block

````markdown
```python
def hello(name):
    return f"Hello, {name}!"
```
````

**Result:** Code block with syntax highlighting

### Supported Languages

**Tier 1 (Full Support):**
- `python`, `py` - Python
- `javascript`, `js` - JavaScript
- `typescript`, `ts` - TypeScript
- `java` - Java
- `kotlin`, `kt` - Kotlin
- `go` - Go
- `rust`, `rs` - Rust
- `ruby`, `rb` - Ruby
- `php` - PHP
- `sql` - SQL
- `bash`, `sh`, `shell` - Shell scripts
- `cpp`, `c++` - C++

**Tier 2 (Good Support):**
- `scala` - Scala
- `haskell`, `hs` - Haskell
- `perl`, `pl` - Perl
- `yaml`, `yml` - YAML
- `json` - JSON
- `html` - HTML

**Special:**
- `diff` - Diff format (unified diff)

### Syntax Highlighting Colors

When a language is specified, keywords are highlighted:

| Element | Color | Default Hex | Example |
|---------|-------|-------------|---------|
| Keywords | Purple | `7C3AED` | `if`, `def`, `class` |
| Strings | Green | `059669` | `"hello"`, `'world'` |
| Comments | Gray | `6B7280` | `# comment`, `// note` |
| Numbers | Red | `DC2626` | `42`, `3.14` |
| Functions | Blue | `2563EB` | `myFunction()` |
| Types | Orange | `D97706` | `String`, `int` |

Colors are customizable via config.json.

### Code Block Without Language

````markdown
```
This is plain monospace text
No syntax highlighting
```
````

**Result:** Monospace font on gray background, no color highlighting.

### Diff Format

````markdown
```diff
- This line was removed
+ This line was added
  This line is unchanged
```
````

**Result:**
- Lines with `-` prefix: Red
- Lines with `+` prefix: Green
- Lines with no prefix: Normal

### Code Block Sizing

- **Default height:** Automatically sized based on content
- **Maximum height:** 3.5 inches (to fit on slide)
- **Font:** Consolas (or config `fonts.code`)
- **Background:** Light gray `F1F5F9` (or config `colors.codeBlock`)

**Note:** Very long code blocks (>30 lines) may overflow. Split into multiple slides if needed.

## Special Elements

### Checkboxes

```markdown
- [ ] Unchecked task
- [x] Completed task
- [ ] Another unchecked
- [X] Capital X also works
```

**Result:**
- `[ ]` → ☐ (unchecked box)
- `[x]` or `[X]` → ☑ (checked box)

**Requirements:**
- Must be part of a bullet list (line starts with `-` or `*`)
- Exactly one space: `[ ]` not `[]`
- Lowercase or uppercase `x`

**Note:** Checkbox must be at the start of the bullet text:

✅ Correct:
```markdown
- [ ] Task description
```

❌ Wrong:
```markdown
- Task description [ ]
```

### Speaker Notes

```markdown
## Slide Title

- Visible content here
- More visible content

note:
This is a speaker note.
Only visible in presenter view.
Can span multiple lines.
```

**Result:** Text after `note:` appears in PowerPoint's presenter notes (not on slide).

**Rules:**
- Must be at the end of a slide
- Use lowercase `note:`
- All text after `note:` until next separator is a note
- Can span multiple paragraphs

### Horizontal Rules (Not Supported)

```markdown
---
```

**Warning:** `---` is a slide separator, NOT a horizontal rule.

For visual separation, use empty lines or plain text.

## Advanced Formatting

### Mixing Formatting

You can combine formatting types:

```markdown
- **Bold** text with _italic_ and `code`
- [**Bold link**](https://example.com)
- **See `function_name()` for details**
```

**Limitations:**
- Can't nest same type: `**bold **nested** bold**` won't work well
- Complex nesting may not render perfectly

### Escaping Special Characters

To display literal markdown characters:

```markdown
Use \*asterisks\* to show *asterisks*
Use \`backticks\` to show `backticks`
```

**Note:** Escaping support is limited. For literal text, use code blocks.

### Unicode and Emojis

```markdown
## Unicode Support ✓

- Checkmark: ✓
- Cross: ✗
- Arrow: →
- Emoji: 😀 🎉 ⚠️
```

**Result:** Unicode characters render as-is if font supports them.

**Recommendation:** Test with your target system's fonts.

## Best Practices

### 1. Consistent Bullet Style

Choose one and stick with it:

✅ Good:
```markdown
- All bullets use dash
- Consistent throughout
- Easy to read
```

❌ Avoid mixing:
```markdown
- Mixed dash
* and asterisk
- looks inconsistent
```

### 2. Proper Indentation

Use exactly 2 spaces per nesting level:

✅ Correct:
```markdown
- Level 1
  - Level 2 (2 spaces)
    - Level 3 (4 spaces)
```

❌ Wrong:
```markdown
- Level 1
   - Level 2 (3 spaces - inconsistent)
        - Level 3 (8 spaces - too much)
```

### 3. Specify Code Languages

Always specify language for syntax highlighting:

✅ Best:
````markdown
```python
print("Hello")
```
````

❌ Suboptimal:
````markdown
```
print("Hello")  # No highlighting
```
````

### 4. Section Organization

Group related slides with sections:

```markdown
---
# Chapter 1: Introduction

----
## What is X?

----
## Why use X?

---
# Chapter 2: Getting Started

----
## Installation

----
## First Steps
```

**Result:** Collapsible sections in PowerPoint for better organization.

### 5. Speaker Notes Usage

Add context for presenters:

```markdown
## Complex Topic

- Main point one
- Main point two

note:
Remember to:
- Explain point one in detail
- Give example for point two
- Allow time for questions
```

**Result:** Clean slides + detailed notes for presenter.

## Common Patterns

### Title Slide

```markdown
---
# Presentation Title
### Subtitle or Tagline

Presenter: Your Name
Date: 2024-01-30
```

### Agenda Slide

```markdown
----
## Agenda

1. Introduction
2. Main Content
3. Conclusion
4. Q&A
```

### Two-Column Layout (Workaround)

PowerPoint layouts are fixed, but you can simulate columns:

```markdown
----
## Features Comparison

**Column 1:**
- Feature A
- Feature B

**Column 2:**
- Feature C
- Feature D
```

**Note:** True multi-column requires manual PowerPoint editing.

### Code Example Slide

````markdown
----
## Code Example

Here's how to use the function:

```python
result = my_function(arg1, arg2)
print(result)
```

Key points:
- `arg1` is required
- `arg2` is optional
````

### Thank You Slide

```markdown
---
# Thank You
### Questions?

Contact: your.email@example.com
GitHub: github.com/yourname
```

## Limitations

### Not Supported

- Tables (use code blocks or plain text)
- Images (add manually in PowerPoint)
- Videos (add manually in PowerPoint)
- Multi-column layouts (edit in PowerPoint)
- Custom slide sizes (fixed at 16:9)
- Animations (add manually in PowerPoint)
- Footnotes (use speaker notes)
- Block quotes `>` (use plain text)

### Partial Support

- Nested formatting (simple nesting works)
- Very long code blocks (may overflow)
- Complex Unicode (depends on fonts)

## Configuration Impact on Syntax

### Custom Colors

Colors defined in config.json affect:

```json
{
  "colors": {
    "accent": "0891B2",          // `inline code` color
    "codeBlock": "F1F5F9",       // ```code``` background
    "syntaxKeyword": "7C3AED",   // if, def, class
    "syntaxString": "059669",    // "strings"
    "syntaxComment": "6B7280",   // # comments
    "syntaxNumber": "DC2626",    // 123
    "syntaxFunction": "2563EB",  // function_names
    "syntaxType": "D97706"       // TypeNames
  }
}
```

### Custom Fonts

Fonts defined in config.json affect:

```json
{
  "fonts": {
    "header": "Trebuchet MS",  // # ## ### headers
    "body": "Calibri",         // bullets and paragraphs
    "code": "Consolas"         // ``` ``` and ` ` code
  }
}
```

## Examples by Use Case

### Technical Presentation

````markdown
---
# API Documentation
### RESTful API Guide

----
## Authentication

Use Bearer tokens:

```bash
curl -H "Authorization: Bearer TOKEN" \
  https://api.example.com/data
```

- [ ] Obtain token from `/auth`
- [x] Include in all requests

----
## Endpoints

1. `GET /users` - List users
2. `POST /users` - Create user
3. `DELETE /users/{id}` - Remove user
````

### Educational Slides

```markdown
---
# Introduction to Python
### Programming Fundamentals

----
## Variables and Types

Variables store data:

- `x = 42` - Integer
- `name = "Alice"` - String
- `pi = 3.14` - Float

note:
Explain that Python is dynamically typed.
Give examples of each type.

----
## Control Flow

```python
if x > 10:
    print("Large")
else:
    print("Small")
```
```

### Business Presentation

```markdown
---
# Q4 Results
### Financial Overview

----
## Key Metrics

- Revenue: **$1.2M** (+15%)
- Users: **50K** (+10%)
- Retention: **85%** (+5%)

note:
Revenue growth driven by enterprise customers.
User growth from marketing campaign.
Retention improved with new features.

----
## Next Steps

1. Expand to new markets
2. Launch mobile app
3. Improve onboarding

[View roadmap](https://example.com/roadmap)
```

## Quick Reference Card

| Element | Markdown | Result |
|---------|----------|--------|
| Section | `---` + `# Title` | Title slide |
| Slide | `----` + `## Title` | Content slide |
| Bold | `**text**` | **text** |
| Italic | `_text_` | *text* |
| Code | `` `text` `` | `text` |
| Link | `[text](url)` | Clickable link |
| Bullet | `- text` | • text |
| Number | `1. text` | 1. text |
| Checkbox | `- [ ]`, `- [x]` | ☐, ☑ |
| Code block | ` ```lang` | Highlighted code |
| Note | `note:` + text | Speaker note |

## See Also

- **SKILL.md** - Main skill documentation
- **SETUP.md** - Installation and configuration
- **TROUBLESHOOTING.md** - Common issues and fixes
- **examples/demo.md** - Working examples of all features
